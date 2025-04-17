import sys
import os
from pathlib import Path
import vectorbtpro as vbt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import itertools
import logging
from typing import Dict, Any, List, Tuple, Optional
# Import tqdm
from tqdm.auto import tqdm

# --- Setup Paths ---
# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Add the directory *containing* the 'strategies' module
# which is the parent of the 'scripts' directory (i.e., the ROOT_DIR)
# No need for SCRIPTS_DIR here if imports are relative to ROOT_DIR

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Import Strategy and Data Fetcher ---
try:
    from scripts.strategies.edge_multi_factor import EdgeMultiFactorStrategy
    logger.info("Successfully imported refactored EdgeMultiFactorStrategy.")
except ImportError as e:
    logger.error(f"Could not import EdgeMultiFactorStrategy: {e}")
    sys.exit(1)

try:
    from data.data_fetcher import fetch_historical_data, get_granularity_str, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    logger.info("Using data_fetcher from data module.")
except ImportError:
    try:
        from scripts.backtest_stoch_sma_vbt_pro import fetch_historical_data, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
        logger.info("Using functions from scripts.backtest_stoch_sma_vbt_pro.")
    except ImportError as e:
        logger.error(f"ERROR: Could not import data fetching functions: {e}")
        sys.exit(1)

# Remove incorrect/unused optimizer import
# from vectorbtpro.portfolio.pfopt.base import PortfolioOptimizer
# from vectorbtpro.generic import WFOOptimizer # Previous attempt
# from vectorbtpro.portfolio.pfopt import WFOOptimizer # Previous attempt

# --- Configuration ---
# WFO Parameters
IN_SAMPLE_DAYS = 365
OUT_SAMPLE_DAYS = 90
STEP_DAYS = 90 # How much the window slides forward
# WFOOptimizer requires window lengths, not start/end dates directly
IN_SAMPLE_LEN = pd.Timedelta(days=IN_SAMPLE_DAYS)
OUT_SAMPLE_LEN = pd.Timedelta(days=OUT_SAMPLE_DAYS)
STEP_LEN = pd.Timedelta(days=STEP_DAYS)

# Data Parameters
# Fetch slightly more data initially to accommodate the first IS window
WFO_START_DATE = (datetime.now() - timedelta(days=IN_SAMPLE_DAYS + OUT_SAMPLE_DAYS * 6)).strftime('%Y-%m-%d')
# WFO_START_DATE = "2020-01-01" # Or set a fixed earlier date
WFO_END_DATE = datetime.now().strftime('%Y-%m-%d')
SYMBOL = "BTC-USD"
GRANULARITY_STR = "1h"
GRANULARITY_SECONDS = 3600
INITIAL_CAPITAL = 3000
COMMISSION_PCT = 0.001
SLIPPAGE_PCT = 0.0005
BENCHMARK_SYMBOL = "BTC-USD" # For benchmark comparison

# Trading Parameters
SIZE_GRANULARITY = 0.00001
RISK_FRACTION = 0.01
ATR_WINDOW_SIZING = 14
# ATR_MULTIPLE_SIZING is now implicitly handled via atr_multiple_sl in the sizing % calculation

# Optimization Parameters
OPTIMIZATION_METRIC = 'sharpe_ratio'
WEIGHT_OPT_STEPS = 3
PARAM_GRID = {
    'lookback_window': [15, 25, 35],
    'volatility_threshold': [0.3, 0.5, 0.7],
    'tsl_stop': [0.05, 0.07, 0.10],
    'tp_stop': [0.05, 0.10, 0.15],
    'atr_multiple_sl': [1.5, 2.0, 2.5], # This now also influences target % size
    # 'factor_weights': 'auto' # Handle weight generation separately before passing to decorator
}
# Get factor names for weight generation
FACTOR_NAMES = ['volatility_regime', 'consolidation_breakout', 'volume_divergence', 'market_microstructure']

def generate_weight_combinations(factors, num_steps):
    """
    Generate valid factor weight combinations that sum to 1.0.
    """
    if not factors:
        return []
    step = 1.0 / num_steps
    points = [i * step for i in range(num_steps + 1)]
    valid_combinations = []
    # Use combinations_with_replacement for efficiency if needed, but product is clearer here
    for combo in itertools.product(points, repeat=len(factors)):
        if np.isclose(sum(combo), 1.0):
            valid_combinations.append(dict(zip(factors, combo)))

    # Add default equal weights if not already present and valid
    default_weights_dict = {factor: 1.0/len(factors) for factor in factors}
    is_default_present = any(
        all(np.isclose(combo.get(factor, 0), weight) for factor, weight in default_weights_dict.items())
        for combo in valid_combinations
    )
    if np.isclose(sum(default_weights_dict.values()), 1.0) and not is_default_present:
         # Ensure keys match exactly for comparison
         valid_combinations.append({factor: default_weights_dict.get(factor, 0) for factor in factors})

    # Deduplicate just in case float precision caused issues
    unique_combos = []
    seen_tuples = set()
    for combo_dict in valid_combinations:
        # Create a sorted tuple of (key, value) pairs for reliable hashing/comparison
        combo_tuple = tuple(sorted(combo_dict.items()))
        if combo_tuple not in seen_tuples:
            unique_combos.append(combo_dict)
            seen_tuples.add(combo_tuple)

    return unique_combos

# --- Refactored WFO Function using @vbt.cv_split ---

def setup_wfo_splitter(index):
    """
    Create a simple time-based split for walk-forward optimization.
    
    Instead of using splitter, we'll manually implement a custom walk-forward optimizer
    that works with time-series data with DatetimeIndex.
    """
    try:
        logging.info(f"Original index type: {type(index)}")
        logging.info(f"Original index dtype: {index.dtype}")
        logging.info(f"First few original values: {index[:5]}")
        
        # First, ensure the index is a DatetimeIndex with correct timezone
        if not isinstance(index, pd.DatetimeIndex):
            index = pd.DatetimeIndex(index)
            
        # Preserve the timezone information
        timezone_info = getattr(index, 'tz', None)
        logging.info(f"Index timezone info: {timezone_info}")
        
        # Define time windows
        train_days = 365
        test_days = 90
        step_days = 90
        
        # Create a manual splitter class that imitates what we need
        class CustomSplitter:
            def __init__(self, ts_index, train_days, test_days, step_days):
                self.ts_index = ts_index
                self.train_days = train_days
                self.test_days = test_days
                self.step_days = step_days
                
                # Calculate the splits in advance
                self.splits = []
                start_time = ts_index[0]
                
                for i in range(20):  # Maximum 20 splits to prevent infinite loops
                    # Create timedelta with timezone preservation
                    train_start_time = start_time + pd.Timedelta(days=(i * step_days))
                    train_end_time = train_start_time + pd.Timedelta(days=train_days)
                    test_end_time = train_end_time + pd.Timedelta(days=test_days)
                    
                    # Skip if we're past the end of the data
                    if test_end_time > ts_index[-1]:
                        break
                    
                    self.splits.append({
                        "split_idx": i,
                        "train_start": train_start_time,
                        "train_end": train_end_time,
                        "test_start": train_end_time,
                        "test_end": test_end_time
                    })
                
                logging.info(f"Created {len(self.splits)} splits")
            
            def get_indices(self, split_idx=None, set_label=None):
                """Get indices for a specific split and set (train/test)"""
                if split_idx is None or set_label is None:
                    return None
                
                if split_idx < 0 or split_idx >= len(self.splits):
                    return None
                
                split = self.splits[split_idx]
                
                if set_label == "train":
                    # Use np.where to get integer indices
                    train_mask = (self.ts_index >= split["train_start"]) & (self.ts_index < split["train_end"])
                    return np.where(train_mask)[0]
                elif set_label == "test":
                    # Use np.where to get integer indices
                    test_mask = (self.ts_index >= split["test_start"]) & (self.ts_index < split["test_end"])
                    return np.where(test_mask)[0]
                else:
                    return None
            
            def get_split_idxs(self):
                """Get all split indices"""
                return list(range(len(self.splits)))
                
        # Create our custom splitter
        splitter = CustomSplitter(index, train_days, test_days, step_days)
        
        return splitter
        
    except Exception as e:
        logging.error(f"Failed to create splitter: {str(e)}")
        raise

def create_pf_for_params(data, lookback_window, volatility_threshold, tsl_stop, tp_stop, atr_multiple_sl, factor_weights, **kwargs):
    """Helper to create portfolio for one parameter set."""
    try:
        # 1. Initialize strategy with current parameters
        strategy = EdgeMultiFactorStrategy(
            lookback_window=lookback_window,
            volatility_threshold=volatility_threshold,
            initial_capital=INITIAL_CAPITAL,
            default_factor_weights=factor_weights,
            commission_pct=COMMISSION_PCT,
            slippage_pct=SLIPPAGE_PCT
        )

        # 2. Generate signals for the current data slice
        long_entries, short_entries = strategy.generate_signals(data)

        # Skip if no signals to avoid errors
        if long_entries.sum() + short_entries.sum() == 0:
            return None # Indicate no portfolio was generated

        # 3. Calculate sizing and stops
        target_amount = strategy.calculate_target_amount(
            data,
            risk_fraction=RISK_FRACTION,
            atr_window=ATR_WINDOW_SIZING,
            atr_multiple_stop=atr_multiple_sl
        )
        
        # Keep SL % calculation for the sl_stop parameter
        atr = vbt.ATR.run(data['high'], data['low'], data['close'], window=ATR_WINDOW_SIZING, wtype='wilder').atr.bfill().ffill()
        sl_stop_dist = (atr * atr_multiple_sl)
        sl_stop_pct = (sl_stop_dist / data['close']).replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
        sl_stop_pct = np.clip(sl_stop_pct, 0.001, 0.5) 

        # 4. Run Portfolio Simulation
        vbt_freq = pd.infer_freq(data.index) # Infer freq from data slice
        if not vbt_freq: vbt_freq = get_vbt_freq_str(GRANULARITY_SECONDS) # Fallback

        pf = vbt.Portfolio.from_signals(
            data['close'], # Use close price from the data slice
            entries=long_entries,
            short_entries=short_entries,
            sl_stop=sl_stop_pct, # Pass SL as percentage
            tsl_stop=tsl_stop if tsl_stop > 0 else None,
            tp_stop=tp_stop if tp_stop > 0 else None,
            size=target_amount, # Pass target dollar amount
            size_type='Amount',   # Use Amount sizing
            init_cash=INITIAL_CAPITAL,
            fees=COMMISSION_PCT,
            slippage=SLIPPAGE_PCT,
            freq=vbt_freq,
            # Comment out size_granularity as it might not apply to Amount
            # size_granularity=SIZE_GRANULARITY,
            stop_exit_type='close',
            accumulate=False,
            call_seq='auto',
        )
        return pf
    except Exception as e:
        # Log the error with parameters for debugging
        logger.error(f"Error in create_pf_for_params with params: lw={lookback_window}, vt={volatility_threshold}, tsl={tsl_stop}, tp={tp_stop}, atr_sl={atr_multiple_sl}, weights={factor_weights}. Error: {e}", exc_info=False) # Set exc_info=True for full traceback if needed
        return None # Return None on error

# Define the main WFO function decorated with @vbt.cv_split
@vbt.cv_split(
    # splitter is defined dynamically based on data below
    takeable_args=["data"],         # Which arguments should be split
    param_product=True,             # Test all combinations of params passed below
    merge_func="concat",            # Combine results into one Series/DataFrame
    # Add chunking/parallel options if needed: engine='ray', chunk_len=...
)
def run_wfo_split(data, lookback_window, volatility_threshold, tsl_stop, tp_stop, atr_multiple_sl, factor_weights, metric_to_return):
    """
    Function for each parameter combination on each train/test slice.
    It calls create_pf_for_params and then extracts the desired metric.
    Used by the original CV split approach.
    """
    pf = create_pf_for_params(
        data=data, 
        lookback_window=lookback_window, 
        volatility_threshold=volatility_threshold, 
        tsl_stop=tsl_stop, 
        tp_stop=tp_stop, 
        atr_multiple_sl=atr_multiple_sl, 
        factor_weights=factor_weights
    )

    if pf is None:
        return np.nan # Return NaN if portfolio creation failed

    # Evaluate portfolio using the specified metric
    try:
        stats = pf.stats()
        metric_value = stats.get(metric_to_return)

        if metric_value is None and metric_to_return != 'Sharpe Ratio':
            logger.warning(f"Metric '{metric_to_return}' not found, falling back to Sharpe Ratio")
            metric_value = stats.get('Sharpe Ratio')

        if metric_value is None or not np.isfinite(metric_value):
            metric_value = np.nan # Use NaN for invalid scores

        # Handle drawdown metric (less negative is better)
        if metric_to_return == 'max_drawdown':
             metric_value = -abs(metric_value)

        return metric_value
    except Exception as e:
        logger.error(f"Error evaluating portfolio for metric '{metric_to_return}': {e}", exc_info=False)
        return np.nan


def run_wfo_refactored():
    """Run the Walk-Forward Optimization process with manual splitting."""
    try:
        logger.info("--- Starting Manual WFO Process ---")
        logger.info(f"Symbol: {SYMBOL}, Granularity: {GRANULARITY_STR}")
        logger.info(f"Date Range: {WFO_START_DATE} to {WFO_END_DATE}")
        logger.info(f"IS: {IN_SAMPLE_LEN}, OOS: {OUT_SAMPLE_LEN}, Step: {STEP_LEN}")
        logger.info(f"Benchmark Symbol: {BENCHMARK_SYMBOL}")
        logger.info(f"Optimization Metric: {OPTIMIZATION_METRIC}")

        # 1. Fetch Data
        logger.info("\nFetching historical data...")
        price_data = fetch_historical_data(SYMBOL, WFO_START_DATE, WFO_END_DATE, GRANULARITY_SECONDS)
        if price_data is None or price_data.empty:
            logger.error("Failed to fetch data. Exiting.")
            return
        logger.info(f"Data fetched successfully. Shape: {price_data.shape}")
        
        # Ensure index is properly formatted
        price_data.index = pd.DatetimeIndex(pd.to_datetime(price_data.index, utc=True))
        price_data = price_data.sort_index()  # Ensure data is sorted

        # Fetch Benchmark Data
        logger.info(f"Fetching benchmark data for {BENCHMARK_SYMBOL}...")
        benchmark_data = fetch_historical_data(BENCHMARK_SYMBOL, WFO_START_DATE, WFO_END_DATE, GRANULARITY_SECONDS)
        benchmark_rets = None
        if benchmark_data is not None and not benchmark_data.empty:
            benchmark_data.index = pd.DatetimeIndex(pd.to_datetime(benchmark_data.index, utc=True))
            benchmark_data = benchmark_data.sort_index()  # Ensure data is sorted
            benchmark_close = benchmark_data['close'].reindex(price_data.index, method='ffill')
            benchmark_rets = benchmark_close.pct_change().fillna(0)
            logger.info(f"Benchmark data fetched. Shape: {benchmark_data.shape}")
        else:
            logger.warning("Could not fetch benchmark data. Proceeding without benchmark.")

        # Create our custom splitter
        logging.info(f"Price data index type: {type(price_data.index)}")
        logging.info(f"Price data index dtype: {price_data.index.dtype}")
        logging.info(f"First few price data index values: {price_data.index[:5]}")
        
        splitter = setup_wfo_splitter(price_data.index)
        
        # 2. Generate Weight Combinations
        weight_combinations = generate_weight_combinations(FACTOR_NAMES, WEIGHT_OPT_STEPS)
        logger.info(f"Generated {len(weight_combinations)} factor weight combinations.")
        if not weight_combinations:
            logger.warning("No valid weight combinations generated, using default equal weights.")
            weight_combinations = [{factor: 1.0/len(FACTOR_NAMES) for factor in FACTOR_NAMES}]

        # 3. Manual WFO process
        logger.info("Running manual WFO process...")
        
        # Create a DataFrame to store results
        all_train_results = []
        all_test_results = []
        best_params_per_split = pd.DataFrame()
        
        # Get all parameter combinations
        param_combinations = []
        for lw in PARAM_GRID['lookback_window']:
            for vt in PARAM_GRID['volatility_threshold']:
                for tsl in PARAM_GRID['tsl_stop']:
                    for tp in PARAM_GRID['tp_stop']:
                        for atr_sl in PARAM_GRID['atr_multiple_sl']:
                            for weights in weight_combinations:
                                param_combinations.append({
                                    'lookback_window': lw,
                                    'volatility_threshold': vt,
                                    'tsl_stop': tsl,
                                    'tp_stop': tp,
                                    'atr_multiple_sl': atr_sl,
                                    'factor_weights': weights
                                })
        
        logger.info(f"Created {len(param_combinations)} parameter combinations")
        
        # Run optimization for each split
        split_indices = splitter.get_split_idxs()
        
        for split_idx in split_indices:
            logger.info(f"\nProcessing split {split_idx}...")
            
            # Get training and test indices
            train_indices = splitter.get_indices(split_idx=split_idx, set_label="train")
            test_indices = splitter.get_indices(split_idx=split_idx, set_label="test")
            
            # Skip if either is empty
            if train_indices is None or len(train_indices) == 0 or test_indices is None or len(test_indices) == 0:
                logger.warning(f"Split {split_idx} has empty train or test set. Skipping.")
                continue
                
            # Slice the data
            train_data = price_data.iloc[train_indices]
            test_data = price_data.iloc[test_indices]
            
            logger.info(f"Train data: {train_data.shape}, Test data: {test_data.shape}")
            
            # Initialize variables to track best parameters
            best_metric_value = float('-inf')
            best_params = None
            
            train_results = []
            
            # Wrap param_combinations with tqdm for progress bar
            param_iterator = tqdm(param_combinations, desc=f"Split {split_idx} Train", leave=False, unit="combo")
            # Run all parameter combinations on training data
            # Use the tqdm iterator
            for params in param_iterator:
                pf = create_pf_for_params(
                    data=train_data,
                    lookback_window=params['lookback_window'],
                    volatility_threshold=params['volatility_threshold'],
                    tsl_stop=params['tsl_stop'],
                    tp_stop=params['tp_stop'],
                    atr_multiple_sl=params['atr_multiple_sl'],
                    factor_weights=params['factor_weights']
                )
                
                if pf is None:
                    continue
                    
                # Evaluate portfolio
                try:
                    stats = pf.stats()
                    metric_value = stats.get(OPTIMIZATION_METRIC)
                    
                    if metric_value is None and OPTIMIZATION_METRIC != 'Sharpe Ratio':
                        logger.warning(f"Metric '{OPTIMIZATION_METRIC}' not found, falling back to Sharpe Ratio")
                        metric_value = stats.get('Sharpe Ratio')
                        
                    if metric_value is None or not np.isfinite(metric_value):
                        metric_value = float('-inf')
                        
                    # Handle drawdown metric (less negative is better)
                    if OPTIMIZATION_METRIC == 'max_drawdown':
                        metric_value = -abs(metric_value)
                        
                    # Track results
                    result = params.copy()
                    result['split_idx'] = split_idx
                    result['set'] = 'train'
                    result['metric_value'] = metric_value
                    train_results.append(result)
                    
                    # Update best parameters if better
                    if metric_value > best_metric_value:
                        best_metric_value = metric_value
                        best_params = params
                        
                except Exception as e:
                    logger.error(f"Error evaluating portfolio: {e}")
                    continue
            
            # If no valid parameters found, skip this split
            if best_params is None:
                logger.warning(f"No valid parameters found for split {split_idx}. Skipping.")
                continue
                
            logger.info(f"Best parameters for split {split_idx}: {best_params}")
            
            # Add best parameters to DataFrame
            best_params_row = best_params.copy()
            best_params_row['split_idx'] = split_idx
            best_params_per_split = pd.concat([best_params_per_split, pd.DataFrame([best_params_row])], ignore_index=True)
            
            # Evaluate best parameters on test data
            test_pf = create_pf_for_params(
                data=test_data,
                lookback_window=best_params['lookback_window'],
                volatility_threshold=best_params['volatility_threshold'],
                tsl_stop=best_params['tsl_stop'],
                tp_stop=best_params['tp_stop'],
                atr_multiple_sl=best_params['atr_multiple_sl'],
                factor_weights=best_params['factor_weights']
            )
            
            if test_pf is not None:
                # Evaluate test portfolio
                try:
                    test_stats = test_pf.stats()
                    test_metric_value = test_stats.get(OPTIMIZATION_METRIC)
                    
                    if test_metric_value is None and OPTIMIZATION_METRIC != 'Sharpe Ratio':
                        test_metric_value = test_stats.get('Sharpe Ratio')
                        
                    if test_metric_value is None or not np.isfinite(test_metric_value):
                        test_metric_value = float('-inf')
                        
                    # Handle drawdown metric
                    if OPTIMIZATION_METRIC == 'max_drawdown':
                        test_metric_value = -abs(test_metric_value)
                        
                    # Track result
                    test_result = best_params.copy()
                    test_result['split_idx'] = split_idx
                    test_result['set'] = 'test'
                    test_result['metric_value'] = test_metric_value
                    all_test_results.append(test_result)
                    
                    logger.info(f"Test {OPTIMIZATION_METRIC} for split {split_idx}: {test_metric_value:.4f}")
                    
                except Exception as e:
                    logger.error(f"Error evaluating test portfolio for split {split_idx}: {e}")
            else:
                logger.warning(f"Could not create test portfolio for split {split_idx}")
                
            # Add train results
            all_train_results.extend(train_results)
            
        # Convert to DataFrames
        all_train_results_df = pd.DataFrame(all_train_results)
        all_test_results_df = pd.DataFrame(all_test_results)
        
        if all_test_results_df.empty:
            logger.error("No valid test results. Aborting.")
            return
            
        # Print summary of OOS performance
        logger.info("\n--- OOS Performance Summary ---")
        logger.info(f"Mean OOS {OPTIMIZATION_METRIC}: {all_test_results_df['metric_value'].mean():.4f}")
        logger.info(f"Std Dev OOS {OPTIMIZATION_METRIC}: {all_test_results_df['metric_value'].std():.4f}")
        
        # Reconstruct OOS portfolios
        logger.info("\nReconstructing OOS Portfolio...")
        oos_portfolios = []
        
        for _, row in all_test_results_df.iterrows():
            split_idx = int(row['split_idx'])
            test_indices = splitter.get_indices(split_idx=split_idx, set_label="test")
            
            if test_indices is None or len(test_indices) == 0:
                logger.warning(f"No test indices found for split {split_idx}, skipping portfolio reconstruction.")
                continue
                
            oos_data_slice = price_data.iloc[test_indices]
            
            # Use the helper function to create the portfolio for this OOS slice with best params
            pf_oos = create_pf_for_params(
                data=oos_data_slice,
                lookback_window=int(row['lookback_window']),
                volatility_threshold=float(row['volatility_threshold']),
                tsl_stop=float(row['tsl_stop']),
                tp_stop=float(row['tp_stop']),
                atr_multiple_sl=float(row['atr_multiple_sl']),
                factor_weights=row['factor_weights']
            )
            
            if pf_oos is not None:
                oos_portfolios.append(pf_oos)
            else:
                logger.warning(f"Failed to create portfolio for OOS split {split_idx}")

        if not oos_portfolios:
            logger.error("Could not reconstruct any OOS portfolios.")
            return

        # Combine the OOS portfolio segments
        final_oos_pf = vbt.Portfolio.combine(oos_portfolios)
        logger.info("\n--- Final OOS Combined Portfolio Stats ---")
        final_stats = final_oos_pf.stats(benchmark_rets=benchmark_rets)
        print(final_stats) # Use print for potentially large DataFrame output

        # Save stats and generate plots for the combined OOS portfolio
        logger.info("\nSaving final OOS results and plots...")
        try:
            # Save Stats
            stats_df = pd.DataFrame([final_stats])
            stats_df.to_csv('edge_strategy_wfo_refactored_stats.csv')
            logger.info("Saved: edge_strategy_wfo_refactored_stats.csv")

            # Save Parameter Evolution
            best_params_per_split.to_csv('edge_strategy_wfo_refactored_parameters.csv')
            logger.info("Saved: edge_strategy_wfo_refactored_parameters.csv")

            # Save Plots
            fig = final_oos_pf.plot(benchmark_rets=benchmark_rets, title="Edge Strategy WFO - Combined OOS Equity")
            fig.write_image('edge_strategy_wfo_refactored_equity.png')
            fig_dd = final_oos_pf.plot_drawdowns(title="Edge Strategy WFO - Combined OOS Drawdowns")
            fig_dd.write_image('edge_strategy_wfo_refactored_drawdowns.png')
            fig_trades = final_oos_pf.trades.plot(title="Edge Strategy WFO - Combined OOS Trades")
            fig_trades.write_image('edge_strategy_wfo_refactored_trades.png')
            # Add more plots if needed (rolling sharpe, etc.)
            logger.info("Saved OOS plots.")

        except Exception as save_err:
           logger.error(f"Error saving final OOS results: {save_err}")

    except Exception as e:
        logging.error(f"Error in run_wfo_refactored: {str(e)}")
        raise


# --- Main Execution Block ---
if __name__ == "__main__":
    # Run the refactored WFO
    run_wfo_refactored() 