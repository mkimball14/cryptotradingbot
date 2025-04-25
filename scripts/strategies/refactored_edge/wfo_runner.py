import vectorbtpro as vbt
from vectorbtpro import Splitter
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import traceback
import itertools
from joblib import Parallel, delayed
from tqdm import tqdm
import os
from sklearn.model_selection import ParameterGrid

# --- Ensure the project root is in the Python path ---
# This allows importing modules from the project root (e.g., scripts.strategies...)
# Adjust the number of `parent` calls based on the script's depth
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# Also add the 'scripts' directory parent to find the 'data' module directly
scripts_parent = Path(__file__).resolve().parents[2] # scripts/ dir
if str(scripts_parent) not in sys.path:
    sys.path.append(str(scripts_parent))

# --- Imports from our strategy modules ---
from scripts.strategies.refactored_edge import config, indicators, signals

# --- Try importing the actual data fetcher --- 
try:
    from data.data_fetcher import fetch_historical_data
    print("Successfully imported fetch_historical_data from data.data_fetcher")
    DATA_FETCHER_AVAILABLE = True
except ImportError:
    print("Warning: Could not import fetch_historical_data from data.data_fetcher.")
    print("WFO requires actual historical data. Please ensure data/data_fetcher.py exists and is correct.")
    fetch_historical_data = None # Define as None if not available
    DATA_FETCHER_AVAILABLE = False

# --- Configuration ---
SYMBOL = 'BTC-USD'
TIMEFRAME = '15m' # Adjusted from '15T'
START_DATE = '2022-01-01' # Adjust as needed
END_DATE = '2024-01-01'   # Adjust as needed
INIT_CAPITAL = 10000
FEES_PCT = 0.001 # Example fee
N_JOBS = -1 # Number of cores for parallel processing (-1 uses all available)

# --- WFO Configuration ---
WFO_TRAIN_POINTS = 34560 # Approx 360 days of 15-min data
WFO_TEST_POINTS = 8640   # Approx 90 days of 15-min data
STEP_POINTS = WFO_TEST_POINTS # Step forward by test length for non-overlapping test sets
MAX_LOOKBACK = None # Or set a specific period like '90d' if indicators need it
SET_BEST_PARAMS = True # Apply best params from training to test set
REFIT = True # Refit on each split - NOTE: Actual refitting logic not implemented in this version

# --- Results Saving ---
OUTPUT_DIR = "data/results" # Directory to save results
RESULTS_FILENAME = "wfo_results.csv" # Filename for the results CSV

# --- Helper function for parallel parameter evaluation ---
def evaluate_single_params(params, data, metric):
    """Evaluates a single parameter set using indicators and signals directly.

    Args:
        params (dict): Parameter dictionary from PARAM_GRID.
        data (pd.DataFrame): Input data (must contain OHLC).
        metric (str): Performance metric to optimize (e.g., 'Sharpe Ratio').

    Returns:
        float or None: The performance score (metric value) or None if error.
    """
    try:
        # Ensure required columns are present
        required_cols = ['open', 'high', 'low', 'close']
        if not all(col in data.columns for col in required_cols):
            print(f"DEBUG (Eval Fail): Missing required columns in data for params {params}")
            return -np.inf
        
        close = data['close']
        high = data['high']
        low = data['low']
        # open_ = data['open'] # Not directly used in current signals/indicators

        # 1. Calculate Indicators using factories and params
        rsi = indicators.RSI.run(close, timeperiod=params['rsi_window']).rsi
        bb = indicators.BBANDS.run(close, window=params['bb_window'], std_dev=params['bb_std_dev'])
        volatility = indicators.Volatility.run(close, timeperiod=params['vol_window']).volatility
        trend_ma = indicators.SMA.run(close, timeperiod=params['trend_window']).sma

        # 2. Generate Signals
        print(f"DEBUG (Eval): Attempting to call generate_edge_signals for params {params}")
        entries, exits = signals.generate_edge_signals(
            close=close,
            rsi=rsi,
            bb_upper=bb.upper,
            bb_lower=bb.lower,
            volatility=volatility,
            trend_ma=trend_ma,
            rsi_entry_threshold=params['rsi_entry_threshold'],
            rsi_exit_threshold=params['rsi_exit_threshold'],
            volatility_threshold=params['vol_threshold'],
            # trend_strict=params.get('trend_strict', True) # Add if needed in grid
        )

        # 3. Create Portfolio
        pf_kwargs = {
            'fees': FEES_PCT,
            'sl_stop': params.get('sl_stop'), # Use get for optional params
            'tp_stop': params.get('tp_stop'),
            'freq': '15T' # Ensure frequency matches data
        }
        pf = vbt.Portfolio.from_signals(
            close=close,
            entries=entries,
            exits=exits,
            init_cash=INIT_CAPITAL,
            **pf_kwargs
        )

        # Check if any trades were made
        if pf.trades.count() == 0:
            print(f"DEBUG (Eval Fail): No trades for params {params}")
            return -np.inf # Penalize heavily if no trades

        # 4. Calculate Performance
        performance_stats = pf.stats()
        score = performance_stats.get(metric)

        # Check for NaN or infinite scores
        if score is None or not np.isfinite(score):
            print(f"DEBUG (Eval Fail): Invalid score ({score}) for metric '{metric}' with params {params}")
            return -np.inf

        # Optional: Apply constraints (e.g., minimum trades, max drawdown)
        if pf.trades.count() < config.MIN_TOTAL_TRADES:
            print(f"DEBUG (Eval Fail): Min trades constraint ({pf.trades.count()} < {config.MIN_TOTAL_TRADES}) for params {params}")
            return -np.inf
        # Note: Max Drawdown in vbt stats is positive, config is negative threshold
        if performance_stats['Max Drawdown [%]'] > abs(config.MAX_DRAWDOWN * 100.0):
            print(f"DEBUG (Eval Fail): Max drawdown constraint ({performance_stats['Max Drawdown [%]']:.2f}% > {abs(config.MAX_DRAWDOWN*100.0):.2f}%) for params {params}")
            return -np.inf
        if performance_stats['Win Rate [%]'] < config.MIN_WIN_RATE * 100.0:
            print(f"DEBUG (Eval Fail): Min win rate constraint ({performance_stats['Win Rate [%]']:.2f}% < {config.MIN_WIN_RATE*100.0:.2f}%) for params {params}")
            return -np.inf

        # print(f"DEBUG (Eval OK): Returning score={score} for params={params}. Stats keys: {list(performance_stats.keys())}")
        return score

    except Exception as e:
        traceback.print_exc()
        return -np.inf # Penalize heavily on any error


def optimize_params_parallel(data, param_combinations, metric, n_jobs=-1):
    """Finds the best parameters using parallel processing.

    Args:
        data (pd.DataFrame): Training data.
        param_combinations (list): List of parameter dictionaries.
        metric (str): Performance metric to optimize.
        n_jobs (int): Number of parallel jobs.

    Returns:
        dict or None: The best parameter dictionary found, or None if no valid params.
    """
    print(f"Optimizing {len(param_combinations)} parameter combinations using metric '{metric}'...")
    
    results = Parallel(n_jobs=n_jobs)(
        delayed(evaluate_single_params)(params, data.copy(), metric) 
        for params in tqdm(param_combinations, desc="Evaluating parameters")
    )

    valid_results = [(score, params) for score, params in zip(results, param_combinations) if score is not None and np.isfinite(score) and score > -np.inf]

    if not valid_results:
        print("No valid parameter combinations found during optimization.")
        # --- Debugging: Show why no valid results --- 
        print(f"  Attempted {len(param_combinations)} parameter combinations.")
        print(f"  Raw results count: {len(results)}")
        # Print first few raw results to avoid flooding console if list is huge
        print(f"  First 5 raw results (score): {results[:5]}") 
        # --- End Debugging ---
        return None, None, None # Return None for params, score, and stats

    # Find the best score and corresponding parameters
    best_score, best_params = max(valid_results, key=lambda item: item[0])
    print(f"Optimization complete. Best score ({metric}): {best_score:.4f}")
    print(f"Best parameters found: {best_params}")

    # --- Re-run the best parameters to get full stats --- #
    try:
        # Recalculate indicators and signals with best params
        close = data['close']
        rsi = indicators.RSI.run(close, timeperiod=best_params['rsi_window']).rsi
        bb = indicators.BBANDS.run(close, window=best_params['bb_window'], std_dev=best_params['bb_std_dev'])
        volatility = indicators.Volatility.run(close, timeperiod=best_params['vol_window']).volatility
        trend_ma = indicators.SMA.run(close, timeperiod=best_params['trend_window']).sma
        
        entries, exits = signals.generate_edge_signals(
            close=close,
            rsi=rsi,
            bb_upper=bb.upper,
            bb_lower=bb.lower,
            volatility=volatility,
            trend_ma=trend_ma,
            rsi_entry_threshold=best_params['rsi_entry_threshold'],
            rsi_exit_threshold=best_params['rsi_exit_threshold'],
            volatility_threshold=best_params['vol_threshold'],
        )

        pf_kwargs = {
            'fees': FEES_PCT,
            'sl_stop': best_params.get('sl_stop'),
            'tp_stop': best_params.get('tp_stop'),
            'freq': '15T'
        }
        best_pf = vbt.Portfolio.from_signals(
            close=close,
            entries=entries,
            exits=exits,
            init_cash=INIT_CAPITAL,
            **pf_kwargs
        )
        best_stats = best_pf.stats()
        print("--- Best Train Performance Stats --- ")
        print(best_stats[['Total Return [%]', 'Sharpe Ratio', 'Max Drawdown [%]', 'Win Rate [%]', 'Total Trades']])
        print("-------------------------------------")
        return best_params, best_score, best_stats
    except Exception as e:
        print(f"Error re-running best parameters to get stats: {e}")
        return best_params, best_score, None # Return stats as None if error
    # -------------------------------------------------- #

# ==============================================================================
# Main WFO Execution Logic
# ==============================================================================
if __name__ == "__main__":
    print("--- Starting Refactored Strategy WFO Runner ---")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Results will be saved to: {os.path.join(OUTPUT_DIR, RESULTS_FILENAME)}")

    # 1. Load Data using the fetcher
    print("Fetching data...")
    if not DATA_FETCHER_AVAILABLE:
        print("Error: Data fetcher is not available. Exiting.")
        sys.exit(1)

    try:
        # Convert granularity string to seconds if needed by fetcher
        # This depends on the signature of your fetch_historical_data function
        # Example: Assuming fetch_historical_data expects granularity in seconds
        granularity_map_seconds = {'1m': 60, '5m': 300, '15m': 900, '1h': 3600, '4h': 14400, '1d': 86400}
        try:
            granularity_seconds = granularity_map_seconds[TIMEFRAME.lower()]
        except KeyError:
            print(f"Error: Invalid TIMEFRAME '{TIMEFRAME}'. Cannot map to seconds.")
            sys.exit(1)

        price_data = fetch_historical_data(SYMBOL, START_DATE, END_DATE, granularity_seconds)

        if price_data is None or price_data.empty:
            print("Error: Failed to fetch historical data or data is empty. Exiting.")
            sys.exit(1)

        # Optional: Basic Data Validation (similar to original script)
        if price_data.isnull().values.any():
            print("Warning: Data contains NaN values. Attempting to forward fill.")
            price_data.ffill(inplace=True)
            price_data.bfill(inplace=True)
            if price_data.isnull().values.any():
                 print("Error: Data still contains NaN values after fill. Exiting.")
                 sys.exit(1)

        # Ensure required columns exist (adjust if fetcher returns different names)
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in price_data.columns for col in required_cols):
            print(f"Error: Fetched data missing required columns: {required_cols}. Found: {price_data.columns}")
            sys.exit(1)
        price_data = price_data[required_cols] # Ensure correct columns

        print(f"Successfully fetched and validated {len(price_data)} data points for {SYMBOL}.")

    except Exception as e:
        print(f"Error during data fetching or validation: {e}")
        traceback.print_exc() # Print detailed traceback
        sys.exit(1)

    print("Splitting data for Walk-Forward Optimization...")

    # Calculate split parameters in terms of data points
    freq_delta = price_data.index.to_series().diff().median() # Estimate data frequency
    if pd.isna(freq_delta) or freq_delta.total_seconds() == 0:
        print("Warning: Could not reliably estimate data frequency. Assuming 1 point per day.")
        points_per_day = 1.0
    else:
        points_per_day = pd.Timedelta(days=1) / freq_delta
        print(f"Estimated points per day: {points_per_day:.2f}")

    train_points = int(config.IN_SAMPLE_DAYS * points_per_day)
    test_points = int(config.OUT_SAMPLE_DAYS * points_per_day)
    step_points = int(config.STEP_DAYS * points_per_day)

    # Ensure lengths are positive
    train_points = max(1, train_points)
    test_points = max(1, test_points)
    step_points = max(1, step_points) # Step must be at least 1

    initial_window_points = train_points + test_points
    total_data_points = len(price_data)

    print(f"WFO Params (Points): Train={train_points}, Test={test_points}, Step={step_points}, Initial Window={initial_window_points}")

    if initial_window_points > total_data_points:
        print(f"Error: Initial window size ({initial_window_points} points) is larger than total data ({total_data_points} points).")
        print("Adjust IN_SAMPLE_DAYS/OUT_SAMPLE_DAYS or fetch more data.")
        sys.exit(1)

    # Explicitly calculate n_splits
    available_range = total_data_points - initial_window_points
    if available_range < 0:
        # This case should be caught by the previous check, but good practice
        n_splits = 0
    else:
        num_steps = available_range // step_points # Integer division for full steps
        n_splits = 1 + num_steps # Initial split + number of steps

    print(f"Explicitly calculated n_splits: {n_splits}")

    if n_splits <= 0:
        print(f"Error: Calculated number of splits ({n_splits}) is not positive. Check data length and WFO parameters.")
        sys.exit(1)

    # --- Manual Split Calculation --- #
    print("Manually calculating rolling window splits...")
    split_indices_list = []
    current_train_start_idx = 0
    for i in range(n_splits):
        train_start_idx = current_train_start_idx
        train_end_idx = train_start_idx + train_points
        test_start_idx = train_end_idx
        test_end_idx = test_start_idx + test_points

        # Ensure we don't exceed data bounds (shouldn't happen with correct n_splits calc, but safety check)
        if train_end_idx > total_data_points or test_end_idx > total_data_points:
            print(f"Warning: Split {i+1} calculation exceeded data bounds. Stopping split generation.")
            break

        # Get the actual index objects for slicing the DataFrame later
        train_indices = price_data.index[train_start_idx:train_end_idx]
        test_indices = price_data.index[test_start_idx:test_end_idx]

        if len(train_indices) < train_points or len(test_indices) < test_points:
             print(f"Warning: Split {i+1} resulted in fewer points than expected. Train: {len(train_indices)}/{train_points}, Test: {len(test_indices)}/{test_points}. This might happen at the end of the data.")
             # Decide whether to continue or break if partial splits are not desired
             # break # Uncomment to stop if partial splits are unwanted

        split_indices_list.append((train_indices, test_indices))

        # Move the window start for the next iteration
        current_train_start_idx += step_points

    print(f"Manually generated {len(split_indices_list)} splits.")

    if not split_indices_list:
        print("Error: Manual split generation resulted in zero splits.")
        sys.exit(1)

    # Update n_splits in case the loop broke early
    n_splits = len(split_indices_list)

    # --- Main WFO Loop ---
    results_list = []

    # Generate parameter combinations from the grid
    param_grid_list = list(ParameterGrid(config.PARAM_GRID))
    print(f"Total parameter combinations to evaluate per split: {len(param_grid_list)}")

    # --- WFO Loop --- 
    print("\n--- Starting Walk-Forward Optimization Loop ---")
    # Iterate directly over the list of splits
    for i, (train_indices, test_indices) in enumerate(split_indices_list):
        current_pair_label = f"Split {i+1}"
        train_data = price_data.loc[train_indices]
        test_data = price_data.loc[test_indices]
        
        print(f"\n--- Processing {current_pair_label} ---")
        print(f"  Train Period: {train_data.index.min()} to {train_data.index.max()} ({len(train_data)} points)")
        print(f"  Test Period:  {test_data.index.min()} to {test_data.index.max()} ({len(test_data)} points)")
        
        # Find best parameters on training data
        best_params, best_train_score, best_train_performance_stats = optimize_params_parallel(
            data=train_data,
            param_combinations=param_grid_list[:1], # <<< ONLY EVALUATE FIRST PARAM COMBINATION
            metric='Sharpe Ratio', # Optimizing for risk-adjusted return
            n_jobs=1 # <<< FORCE SERIAL EXECUTION
        )

        if best_params is None:
            print(f"  No valid parameters found for {current_pair_label}. Skipping test evaluation.")
            # --- Store Results for this Split (No Valid Params) ---
            split_result_dict = {
                'split': current_pair_label,
                'train_start': train_data.index.min().strftime('%Y-%m-%d %H:%M:%S%z'),
                'train_end': train_data.index.max().strftime('%Y-%m-%d %H:%M:%S%z'),
                'test_start': test_data.index.min().strftime('%Y-%m-%d %H:%M:%S%z'),
                'test_end': test_data.index.max().strftime('%Y-%m-%d %H:%M:%S%z'),
                'best_params': 'None Found',
                'train_return': np.nan,
                'train_sharpe': np.nan,
                'train_max_drawdown': np.nan,
                'test_return': np.nan,
                'test_sharpe': np.nan,
                'test_max_drawdown': np.nan
            }
            print(f"DEBUG: Appending results (No Valid Params): {split_result_dict}")
            results_list.append(split_result_dict)
            continue # Move to the next split
        
        print(f"  Best parameters for {current_pair_label}: {best_params}")
        
        # Evaluate best parameters on test data
        print(f"  Evaluating best parameters on test data for {current_pair_label}...")
        try:
            # --- Replicate indicator and signal calculation for TEST data --- #
            test_close = test_data['close']
            test_high = test_data['high']
            test_low = test_data['low']

            test_rsi = indicators.RSI.run(test_close, timeperiod=best_params['rsi_window']).rsi
            test_bb = indicators.BBANDS.run(test_close, window=best_params['bb_window'], std_dev=best_params['bb_std_dev'])
            test_volatility = indicators.Volatility.run(test_close, timeperiod=best_params['vol_window']).volatility
            test_trend_ma = indicators.SMA.run(test_close, timeperiod=best_params['trend_window']).sma

            test_entries, test_exits = signals.generate_edge_signals(
                close=test_close,
                rsi=test_rsi,
                bb_upper=test_bb.upper,
                bb_lower=test_bb.lower,
                volatility=test_volatility,
                trend_ma=test_trend_ma,
                rsi_entry_threshold=best_params['rsi_entry_threshold'],
                rsi_exit_threshold=best_params['rsi_exit_threshold'],
                volatility_threshold=best_params['vol_threshold'],
            )

            test_pf_kwargs = {
                'fees': FEES_PCT,
                'sl_stop': best_params.get('sl_stop'),
                'tp_stop': best_params.get('tp_stop'),
                'freq': '15T'
            }
            test_pf = vbt.Portfolio.from_signals(
                close=test_close,
                entries=test_entries,
                exits=test_exits,
                init_cash=INIT_CAPITAL,
                **test_pf_kwargs
            )
            # ---------------------------------------------------------------- #

            if test_pf.trades.count() == 0:
                print(f"  No trades executed on test data for {current_pair_label}.")
                test_performance = None
                test_return = 0.0 # Or NaN? Let's use 0 if no trades.
            else:
                test_performance = test_pf.stats()
                test_return = test_performance['Total Return [%]'] / 100.0 # Convert % to decimal
                print(f"  Test Performance ({current_pair_label}): Return={test_return:.4f}, Sharpe={test_performance['Sharpe Ratio']:.2f}, Trades={test_pf.trades.count()}")
            
            # --- Store Results for this Split (Test Success/No Trades) --- #
            split_result_dict = {
                'split': current_pair_label,
                'train_start': train_data.index.min().strftime('%Y-%m-%d %H:%M:%S%z'),
                'train_end': train_data.index.max().strftime('%Y-%m-%d %H:%M:%S%z'),
                'test_start': test_data.index.min().strftime('%Y-%m-%d %H:%M:%S%z'),
                'test_end': test_data.index.max().strftime('%Y-%m-%d %H:%M:%S%z'),
                'best_params': str(best_params), # Store as string for CSV compatibility
                # Training Performance Metrics
                'train_return': best_train_performance_stats['Total Return [%]'] / 100.0 if best_train_performance_stats is not None else np.nan,
                'train_sharpe': best_train_performance_stats['Sharpe Ratio'] if best_train_performance_stats is not None and np.isfinite(best_train_performance_stats['Sharpe Ratio']) else np.nan,
                'train_max_drawdown': best_train_performance_stats['Max Drawdown [%]'] / 100.0 if best_train_performance_stats is not None else np.nan,
                # Test Performance Metrics
                'test_return': test_return,
                'test_sharpe': test_performance['Sharpe Ratio'] if test_performance is not None and np.isfinite(test_performance['Sharpe Ratio']) else np.nan,
                'test_max_drawdown': test_performance['Max Drawdown [%]'] / 100.0 if test_performance is not None else np.nan
            }
            print(f"DEBUG: Appending results (Test Success): {split_result_dict}")
            results_list.append(split_result_dict)
            # ------------------------------------

        except Exception as e:
            print(f"  Error running test simulation for {current_pair_label}: {e}")
                  
            # --- Store Results for this Split (Test Error Case) ---
            # Still save train performance as optimization was successful
            split_result_dict = {
                'split': current_pair_label,
                'train_start': train_data.index.min().strftime('%Y-%m-%d %H:%M:%S%z'),
                'train_end': train_data.index.max().strftime('%Y-%m-%d %H:%M:%S%z'),
                'test_start': test_data.index.min().strftime('%Y-%m-%d %H:%M:%S%z'),
                'test_end': test_data.index.max().strftime('%Y-%m-%d %H:%M:%S%z'),
                'best_params': str(best_params), # Save the params that were found
                # Save train results if they exist, otherwise NaN
                'train_return': best_train_performance_stats['Total Return [%]'] / 100.0 if 'best_train_performance_stats' in locals() and best_train_performance_stats is not None else np.nan,
                'train_sharpe': best_train_performance_stats['Sharpe Ratio'] if 'best_train_performance_stats' in locals() and best_train_performance_stats is not None and np.isfinite(best_train_performance_stats['Sharpe Ratio']) else np.nan,
                'train_max_drawdown': best_train_performance_stats['Max Drawdown [%]'] / 100.0 if 'best_train_performance_stats' in locals() and best_train_performance_stats is not None else np.nan,
                'test_return': np.nan, # Indicate test failure
                'test_sharpe': np.nan,
                'test_max_drawdown': np.nan
            }
            print(f"DEBUG: Appending results (Test Error): {split_result_dict}")
            results_list.append(split_result_dict)
            # ------------------------------------

    # --- Aggregate Results --- 
    print("\n--- WFO Results ---")
    valid_test_returns = [r['test_return'] for r in results_list if not np.isnan(r['test_return'])] # Use the tracked list
    if valid_test_returns:
        avg_return = np.mean(valid_test_returns)
        std_return = np.std(valid_test_returns)
        print(f"Average Test Return across {len(valid_test_returns)} valid splits: {avg_return:.4f}")
        print(f"Std Dev of Test Returns: {std_return:.4f}")
    else:
        print("No test results were generated.")

    # --- Save Detailed Results to CSV ---
    if results_list:
        results_df = pd.DataFrame(results_list)
        output_path = os.path.join(OUTPUT_DIR, RESULTS_FILENAME)
        try:
            results_df.to_csv(output_path, index=False)
            print(f"\nDetailed WFO results saved to: {output_path}")
        except Exception as e:
            print(f"\nError saving results to {output_path}: {e}")
    else:
        print("\nNo results to save.")
    # ------------------------------------

    print("--- WFO Runner Finished ---")
