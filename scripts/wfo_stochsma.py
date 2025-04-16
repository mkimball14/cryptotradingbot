import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from tqdm.auto import tqdm
import argparse
from typing import Optional # Added for potential type hints if needed

# Add project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
import vectorbtpro as vbt
from pathlib import Path
import logging
from tqdm import tqdm
import time

# Assuming data fetching and strategy class are in these locations
from data.data_fetcher import fetch_historical_data, get_vbt_freq_str, get_granularity_str
from strategies.stoch_sma_strategy import StochSMAStrategy
from reporting.report_generator import calculate_risk_metrics # Reuse risk metrics calc

# Setup Logging
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"wfo_stochsma_{datetime.now():%Y%m%d_%H%M%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Removed setting for interactive plotting as it was causing errors
vbt.settings.plotting['layout']['width'] = 1200
vbt.settings.plotting['layout']['height'] = 600

# --- Strategy Class Import ---
# Assuming StochSMAStrategy is correctly defined in the specified file
try:
    from scripts.backtest_stoch_sma_vbt_pro import StochSMAStrategy
    logger.info("Successfully imported StochSMAStrategy.")
except ImportError as e:
    logger.error(f"Failed to import StochSMAStrategy: {e}. Ensure backtest_stoch_sma_vbt_pro.py is in the correct path.")
    sys.exit(1)
except AttributeError as e:
    logger.error(f"AttributeError importing StochSMAStrategy: {e}. Check class definition.")
    sys.exit(1)

# --- Data Fetching Functions Removed (Now Imported) ---
# [Code for GRANULARITY_MAP_SECONDS, get_granularity_str, get_vbt_freq_str, create_sample_data, fetch_historical_data was here]

# --- Main WFO Execution ---

def run_stochsma_wfo(
    symbol: str, 
    start_date: str, 
    end_date: str, 
    granularity: int, # Seconds
    best_params: dict, # Fixed best parameters
    initial_capital: float = 10000, 
    commission_pct: float = 0.001, 
    slippage_pct: float = 0.0005,
    use_stops: bool = True, # Keep consistent with optimization runs
    sl_atr_multiplier: float = 1.5, # Keep consistent
    tsl_atr_multiplier: float = 2.0, # Keep consistent
    trend_sma_window: int = 50, # Keep consistent
    wfo_test_days: int = 90, 
    wfo_window_years: float = 1.5 # Removed reports_dir parameter
):
    """Performs Walk-Forward Optimization for StochSMA using FIXED parameters."""
    
    granularity_str = get_granularity_str(granularity) or f"{granularity}s"
    vbt_freq_str = get_vbt_freq_str(granularity)
    if not vbt_freq_str:
        logger.error(f"Cannot map granularity {granularity}s to vbt freq string.")
        return None, None
        
    logger.info(f"--- Running WFO (StochSMA - Fixed Params) for {symbol} ({granularity_str}) --- ")
    logger.info(f"Date Range: {start_date} to {end_date}")
    logger.info(f"Fixed Parameters: {best_params}")
    logger.info(f"Initial Capital: ${initial_capital:,.2f}, Commission: {commission_pct*100:.3f}%, Slippage: {slippage_pct*100:.3f}%")
    logger.info(f"Stops: {'Enabled' if use_stops else 'Disabled'} (SL: {sl_atr_multiplier}*ATR, TSL: {tsl_atr_multiplier}*ATR)")
    logger.info(f"Trend Filter: SMA({trend_sma_window})")
    logger.info(f"WFO: Test Days={wfo_test_days}, Total Window={wfo_window_years:.1f} years")

    # 1. Fetch Full Data
    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: 
        logger.error("Failed to fetch price data for WFO.")
        return None, None
        
    # --- ADDED: Adjust granularity if using daily sample data ---
    is_sample_data = False
    try:
        inferred_freq = pd.infer_freq(full_price_data.index)
        if inferred_freq == 'D':
            # Heuristic: If freq is daily and original granularity wasn't daily, assume fallback
            if granularity != 86400:
                logger.warning("Detected daily sample data fallback. Adjusting WFO granularity to daily (86400s).")
                granularity = 86400
                granularity_str = get_granularity_str(granularity) or f"{granularity}s"
                vbt_freq_str = get_vbt_freq_str(granularity) # Should be '1D'
                is_sample_data = True
                if not vbt_freq_str:
                    logger.error("Failed to get vbt_freq_str for daily sample data!")
                    return None, None
    except Exception as freq_err:
         logger.warning(f"Could not infer frequency from data index, proceeding with original granularity: {freq_err}")
    # --- END ADDED SECTION ---
        
    if isinstance(full_price_data.index, pd.DatetimeIndex):
        logger.info("Price data index is confirmed to be DatetimeIndex.")
    else:
        logger.warning("Price data index is not confirmed to be DatetimeIndex.")

    # --- Explicit frequency setting REMOVED --- 

    close = full_price_data['close']
    high = full_price_data['high']
    low = full_price_data['low']
    open_ = full_price_data['open'] # Needed for StochSMA strategy run
    
    # 2. Define WFO Splits
    periods_per_day = 86400 // granularity # Recalculate based on potentially adjusted granularity
    window_len_periods = int(wfo_window_years * 365.25 * periods_per_day)
    test_len_periods = int(wfo_test_days * periods_per_day)
    # Ensure train_len is calculated correctly and is positive
    train_len_periods = max(1, window_len_periods - test_len_periods) 
    
    if train_len_periods + test_len_periods > len(close):
         logger.warning(f"WFO window length ({window_len_periods} periods) exceeds data length ({len(close)} periods). Adjusting...")
         # Adjust window or split logic if needed, or just proceed if rolling_split handles it
    
    # 4. Initialize Strategy Instance (outside loop)
    # Use parameters appropriate for the *detected* data granularity
    strategy = StochSMAStrategy(
        initial_capital=initial_capital, 
        commission_pct=commission_pct, 
        slippage_pct=slippage_pct,
        use_stops=use_stops, 
        sl_atr_multiplier=sl_atr_multiplier, 
        tsl_atr_multiplier=tsl_atr_multiplier, 
        trend_sma_window=trend_sma_window
    )

    # 5. Run WFO Loop
    all_fold_results = []
    logger.info("--- Starting WFO Loop --- ")
    # --- Calculate splits manually ---
    n_datapoints = len(full_price_data)
    if window_len_periods > n_datapoints:
        logger.error(f"Data length ({n_datapoints}) is shorter than the WFO window length ({window_len_periods}). Cannot perform WFO.")
        return
    
    # Calculate the number of steps the test window can take
    n_manual_splits = ((n_datapoints - window_len_periods) // test_len_periods) + 1
    logger.info(f"Calculated {n_manual_splits} manual WFO splits.")
    if n_manual_splits <= 0:
         logger.error("WFO parameters result in 0 or negative splits.")
         return
         
    try:
        # --- Loop using manual index calculation ---
        for i in tqdm(range(n_manual_splits), desc="Running WFO Segments"):
            # Calculate integer indices for train/test slices
            train_start_idx = i * test_len_periods
            train_end_idx = train_start_idx + train_len_periods 
            test_start_idx = train_end_idx
            test_end_idx = test_start_idx + test_len_periods

            # Ensure test_end_idx does not exceed data length
            test_end_idx = min(test_end_idx, n_datapoints)
            # Adjust train_end_idx/test_start_idx if test window gets truncated at the end
            test_start_idx = min(test_start_idx, test_end_idx)
            train_end_idx = test_start_idx
            
            # Ensure train start index is valid
            train_start_idx = max(0, train_start_idx)
            train_end_idx = max(train_start_idx, train_end_idx)

            # Check if slices are valid
            if train_start_idx >= train_end_idx or test_start_idx >= test_end_idx:
                 logger.warning(f"Split {i+1}: Invalid indices calculated. Train: {train_start_idx}-{train_end_idx}, Test: {test_start_idx}-{test_end_idx}. Skipping.")
                 continue

            fold_num = i + 1
            logger.info(f"\n--- Running Fold {fold_num}/{n_manual_splits} --- ")

            # Slice data for this fold using iloc with the calculated indices
            train_data = full_price_data.iloc[train_start_idx:train_end_idx]
            test_data = full_price_data.iloc[test_start_idx:test_end_idx]

            # Check for empty slices after iloc
            if train_data.empty or test_data.empty:
                 logger.warning(f"Fold {fold_num}: Train or Test data slice is empty after iloc. Skipping fold.")
                 all_fold_results.append(None)
                 continue

            logger.info(f"Fold {fold_num}: Train Data {train_data.index[0]} to {train_data.index[-1]} ({len(train_data)} periods)")
            logger.info(f"Fold {fold_num}: Test Data  {test_data.index[0]} to {test_data.index[-1]} ({len(test_data)} periods)")

            # Check for sufficient data length in train split
            if len(train_data) < train_len_periods:
                logger.warning(f"Fold {fold_num}: Insufficient data in train split. Skipping fold.")
                all_fold_results.append(None)
                continue

            # Use the FIXED best_params found from prior optimization
            current_params = best_params.copy() 
            logger.info(f"Applying fixed params: {current_params}")

            try:
                # Run the StochSMA strategy.optimize on the TEST data using fixed parameters
                # The optimize method handles single parameters sets when passed as lists
                single_param_grid = {k: [v] for k, v in current_params.items() if k not in ['trend_filter_window', 'use_stops', 'sl_atr_multiplier', 'tsl_atr_multiplier']}

                logger.debug(f"Fold {fold_num}: Calling strategy.optimize for test data...")
                segment_pf = strategy.optimize(
                    data=test_data.copy(), # Pass testing data
                    param_grid=single_param_grid, # Use the single set of parameters
                    optimize_metric='sharpe_ratio', # Metric doesn't matter for single run
                    granularity_seconds=granularity
                )

                if segment_pf is None:
                     logger.warning(f"Fold {fold_num}: Strategy optimize run returned None. Skipping.")
                     all_fold_results.append(None)
                     continue

                # Portfolio is generated by optimize, no need for from_signals here
                segment_metrics = calculate_risk_metrics(segment_pf)
                logger.info(f"Fold {fold_num} Metrics: {segment_metrics}")

                # Check if any trades were made using len()
                if len(segment_pf.trades) > 0:
                     all_fold_results.append(segment_pf)
                     # all_metrics.append(segment_metrics) # Metrics are derived from combined pf later
                else:
                     logger.info(f"Fold {fold_num}: No trades executed. Storing None for segment.")
                     all_fold_results.append(None) # Store None if no trades, to avoid issues with combine

            except TypeError as te:
                 logger.error(f"TypeError during WFO loop iteration: {te}", exc_info=True)
                 all_fold_results.append(None)
            except Exception as loop_err:
                 logger.error(f"Error during WFO loop iteration: {loop_err}", exc_info=True)
                 all_fold_results.append(None)

    except Exception as e:
        logger.error(f"Error during WFO loop: {e}", exc_info=True)
        return None, None

    logger.info(f"Completed iterating through {n_manual_splits} WFO segments.") # Log total splits processed

    # 6. Aggregate Results
    logger.info("\n--- Aggregating WFO Results ---")
    if not all_fold_results or all(result is None for result in all_fold_results):
         logger.error("WFO finished, but no valid portfolio segments were generated.")
         return None, None
         
    # --- Manual Aggregation (Simpler Approach for Fixed Params WFO) ---
    # Concatenate returns from each segment's test period
    
    # Define the key for the fixed parameters used in this WFO run
    param_key_list = ['stoch_k', 'stoch_d', 'stoch_lower_th', 'stoch_upper_th']
    param_key = tuple(best_params[k] for k in param_key_list)
    logger.info(f"Extracting returns for parameter key: {param_key}")
    
    # Extract the specific returns column corresponding to the fixed parameters
    all_returns_list = []
    for pf in all_fold_results:
        if pf is not None:
            if isinstance(pf.returns, pd.Series) and isinstance(pf.returns.name, tuple) and pf.returns.name == param_key:
                # Handle case where pf.returns might be a Series with the tuple as name
                all_returns_list.append(pf.returns)
            elif isinstance(pf.returns, pd.DataFrame) and param_key in pf.returns.columns:
                 # Handle case where pf.returns is a DataFrame with MultiIndex columns
                all_returns_list.append(pf.returns[param_key])
            elif isinstance(pf.returns, pd.Series) and len(pf.returns.name) == 1 and pf.returns.name[0] == param_key: # Check if it's a single column DataFrame-like Series
                 all_returns_list.append(pf.returns)
            else:
                 logger.warning(f"Could not find returns for key {param_key} in portfolio segment. Index/Columns: {pf.returns.index}, {getattr(pf.returns, 'columns', 'N/A')}")

    if not all_returns_list:
        logger.error("Failed to extract any valid return series for the specified parameters.")
        return None # Or return empty metrics

    # Concatenate the list of simple Series
    all_returns = pd.concat(all_returns_list)
    # all_returns = pd.concat([pf.returns for pf in all_fold_results if pf is not None]) # Original line
    all_returns = all_returns.sort_index().drop_duplicates() # Ensure chronological order and uniqueness

    # Reindex to the full data range to handle potential gaps if segments were skipped
    all_returns = all_returns.reindex(full_price_data.index).fillna(0)
    
    # Create a final portfolio from the combined returns
    # Note: This doesn't perfectly reconstruct orders/logs across boundaries, 
    # but gives the correct overall equity curve and performance from returns.
    logger.info("Creating final portfolio from combined returns...")
    # final_pf = all_returns.vbt.to_portfolio( # Incorrect accessor method
    # Revert to using the class method Portfolio.from_returns
    # final_pf = vbt.Portfolio.from_returns(
    #     returns=all_returns, # Pass the returns series
    #     init_cash=initial_capital,
    #     freq=vbt_freq_str,
    #     fees=commission_pct, # Apply fees/slippage notionally
    #     slippage=slippage_pct,
    # )

    # Calculate metrics directly from the aggregated returns series
    try:
        # Correctly CALL .metrics() as a method
        # overall_metrics = all_returns.vbt.returns(freq=vbt_freq_str).metrics()
        # Use .stats() to get metrics from the returns accessor
        overall_metrics = all_returns.vbt.returns(freq=vbt_freq_str).stats()
        logger.info(f"Overall WFO Performance Metrics:\n{overall_metrics}")
    except Exception as metrics_err:
        logger.error(f"Failed to calculate metrics from combined returns: {metrics_err}", exc_info=True)
        overall_metrics = pd.Series(name="Metrics Calculation Failed") # Placeholder

    # overall_metrics = calculate_risk_metrics(final_pf) # Removed, metrics calculated directly above
    # logger.info(f"Overall WFO Performance Metrics: {overall_metrics}") # Logging moved up
    
    # --- Save Results ---
    # Define reports_dir INSIDE the function, using the potentially adjusted granularity_str
    reports_dir = f"reports/wfo_stochsma/{symbol}_{granularity_str}"
    logger.info(f"Attempting to save results to directory: {reports_dir}")
    reports_path = Path(reports_dir)
    try:
        reports_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured report directory exists: {reports_path}")
    except Exception as mkdir_err:
        logger.error(f"Failed to create report directory {reports_path}: {mkdir_err}", exc_info=True)
        # Optionally return here if directory creation is critical
        return overall_metrics
    
    # Save aggregated metrics
    metrics_df = pd.DataFrame([overall_metrics])
    metrics_file = reports_path / f"wfo_{symbol}_{granularity_str}_metrics.csv"
    metrics_df.to_csv(metrics_file, index=False)
    logger.info(f"Saved aggregated WFO metrics to {metrics_file}")

    # --- ADD DEBUGGING ---
    logger.info(f"Debugging all_returns before saving to CSV:")
    logger.info(f"Length: {len(all_returns)}")
    logger.info(f"Non-zero count: {(all_returns != 0).sum()}")
    logger.info(f"Max value: {all_returns.max()}")
    logger.info(f"Min value: {all_returns.min()}")
    logger.info(f"Describe:\n{all_returns.describe()}")
    # --- END DEBUGGING ---
    
    # Save the raw returns series
    returns_file = reports_path / f"wfo_{symbol}_{granularity_str}_returns.csv"
    all_returns.to_csv(returns_file)
    logger.info(f"Saved aggregated WFO returns series to {returns_file}")
    
    # Return metrics (final_pf is no longer returned)
    return overall_metrics


if __name__ == "__main__":
    # --- Configuration ---
    SYMBOL = "BTC-USD" 
    START_DATE = "2021-01-01" # Adjust as needed
    END_DATE = "2024-06-01"   # Adjust as needed
    GRANULARITY_SECONDS = 14400 # 4 hours
    
    # Best parameters identified from optimization
    BEST_STOCHSMA_PARAMS = {
        'stoch_k': 5, 
        'stoch_d': 4, 
        'stoch_lower_th': 35, 
        'stoch_upper_th': 65
    }

    # Strategy fixed parameters (consistent with optimization)
    INITIAL_CAPITAL = 10000
    COMMISSION_PCT = 0.001 # Example for Coinbase Advanced
    SLIPPAGE_PCT = 0.0005
    USE_STOPS = True 
    SL_ATR_MULTIPLIER = 1.5 # From StochSMA defaults or optimization? Assume default
    TSL_ATR_MULTIPLIER = 2.0 # From StochSMA defaults or optimization? Assume default
    TREND_SMA_WINDOW = 50 # From StochSMA defaults or optimization? Assume default
    
    # WFO specific parameters
    WFO_TEST_DAYS = 90 # How many days for each out-of-sample test period
    WFO_WINDOW_YEARS = 1.5 # Total length of each train+test window
    
    logger.info("Starting StochSMA Walk-Forward Optimization Script")
    
    # Adjusted to only receive metrics back
    overall_metrics = run_stochsma_wfo(
        symbol=SYMBOL, 
        start_date=START_DATE, 
        end_date=END_DATE, 
        granularity=GRANULARITY_SECONDS, 
        best_params=BEST_STOCHSMA_PARAMS, 
        initial_capital=INITIAL_CAPITAL, 
        commission_pct=COMMISSION_PCT, 
        slippage_pct=SLIPPAGE_PCT,
        use_stops=USE_STOPS, 
        sl_atr_multiplier=SL_ATR_MULTIPLIER, 
        tsl_atr_multiplier=TSL_ATR_MULTIPLIER, 
        trend_sma_window=TREND_SMA_WINDOW,
        wfo_test_days=WFO_TEST_DAYS, 
        wfo_window_years=WFO_WINDOW_YEARS # Removed reports_dir argument
    )

    logger.info("StochSMA Walk-Forward Optimization Script Finished") 