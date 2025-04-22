import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from tqdm.auto import tqdm
import argparse
from typing import Optional, Tuple, Dict # Added Tuple, Dict

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
from reporting.report_generator import calculate_risk_metrics # Reuse risk metrics calc

# Setup Logging
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"adaptive_wfo_stochsma_{datetime.now():%Y%m%d_%H%M%S}.log"
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

# --- Helper Function (Moved from backtest script) ---
def get_best_index(performance: pd.Series, higher_better: bool = True) -> Optional[Tuple]:
    """Finds index (tuple) of best performing parameters for a single split's performance Series."""
    if performance is None or performance.empty:
        logger.warning("Get_best_index: Performance data is empty.")
        return None
    try:
        # Check for any non-NaN values safely
        if not performance.notna().any().item():  # Add .item() to convert to scalar boolean
            logger.warning("Get_best_index: Performance data contains only NaNs.")
            return None
            
        # Ensure performance index is a MultiIndex before accessing levels
        is_multi_index = isinstance(performance.index, pd.MultiIndex)
        if not is_multi_index:
            logger.warning(f"Get_best_index: Performance index is not a MultiIndex. Index type: {type(performance.index)}")
            # Handle Series with simple index (single parameter run)
            if len(performance) == 1:
                 # If it was a single run, the index might be the tuple itself if vbt returned it that way
                 if isinstance(performance.index[0], tuple):
                      return performance.index[0]
                 else: # Or just wrap the simple index value in a tuple
                      return (performance.index[0],) 
            else:
                 # Cannot reliably get best index from non-MultiIndex with multiple values
                 return None 
                 
        if higher_better:
            # Get best performing parameter combination - handle case where result may be a Series
            try:
                idx = performance.idxmax() # Returns the tuple index or might return Series for MultiColumns
                
                # If idxmax returns a Series, we need to find the maximum value's index
                if isinstance(idx, pd.Series):
                    logger.info("get_best_index: idxmax returned a Series, finding the best value")
                    max_val = performance.max()
                    # Filter for the maximum value and get the first matching index
                    matching_indices = performance[performance == max_val].index
                    if len(matching_indices) > 0:
                        idx = matching_indices[0]
                    else:
                        logger.warning("get_best_index: Could not find matching index for max value")
                        return None
            except Exception as e:
                logger.error(f"Error in get_best_index using idxmax: {e}", exc_info=True)
                return None
        else:
            # Same for minimum
            try:
                idx = performance.idxmin() # Returns the tuple index
                
                # If idxmin returns a Series, we need to find the minimum value's index
                if isinstance(idx, pd.Series):
                    logger.info("get_best_index: idxmin returned a Series, finding the best value")
                    min_val = performance.min()
                    # Filter for the minimum value and get the first matching index
                    matching_indices = performance[performance == min_val].index
                    if len(matching_indices) > 0:
                        idx = matching_indices[0]
                    else:
                        logger.warning("get_best_index: Could not find matching index for min value")
                        return None
            except Exception as e:
                logger.error(f"Error in get_best_index using idxmin: {e}", exc_info=True)
                return None
            
        # Ensure the result is always a tuple, even if only one parameter level exists
        return idx if isinstance(idx, tuple) else (idx,)
    except Exception as e:
        logger.error(f"Error getting best index: {e}", exc_info=True)
        return None

# --- Main WFO Execution ---

def run_stochsma_wfo(
    symbol: str, 
    start_date: str, 
    end_date: str, 
    granularity: int, # Seconds
    initial_capital: float = 10000, 
    commission_pct: float = 0.001, 
    slippage_pct: float = 0.0005,
    use_stops: bool = True, 
    sl_atr_multiplier: float = 1.5, 
    tsl_atr_multiplier: float = 2.0, 
    trend_sma_window: int = 50, 
    wfo_test_days: int = 90, 
    wfo_window_years: float = 1.5 
):
    """Performs Adaptive Walk-Forward Optimization for StochSMA (re-optimizes each fold)."""
    
    granularity_str = get_granularity_str(granularity) or f"{granularity}s"
    vbt_freq_str = get_vbt_freq_str(granularity)
    if not vbt_freq_str:
        logger.error(f"Cannot map granularity {granularity}s to vbt freq string.")
        return None
        
    logger.info(f"--- Running Adaptive WFO (StochSMA) for {symbol} ({granularity_str}) --- ")
    logger.info(f"Date Range: {start_date} to {end_date}")
    logger.info(f"Initial Capital: ${initial_capital:,.2f}, Commission: {commission_pct*100:.3f}%, Slippage: {slippage_pct*100:.3f}%")
    logger.info(f"Stops: {'Enabled' if use_stops else 'Disabled'} (SL: {sl_atr_multiplier}*ATR, TSL: {tsl_atr_multiplier}*ATR)")
    logger.info(f"Trend Filter: SMA({trend_sma_window})")
    logger.info(f"WFO: Test Days={wfo_test_days}, Total Window={wfo_window_years:.1f} years")

    # --- Define Optimization Grid and Metric ---
    # Reduced parameter grid to avoid Numba JIT compilation errors
    OPTIMIZATION_PARAM_GRID = {
        'stoch_k': np.arange(5, 24, 6),       # Reduced from [5,8,11,14,17,20,23] to [5,11,17,23]
        'stoch_d': np.arange(3, 10, 3),       # Reduced from [3,5,7,9] to [3,6,9]
        'stoch_lower_th': np.arange(15, 40, 10), # Reduced from [15,20,25,30,35] to [15,25,35]
        'stoch_upper_th': np.arange(60, 85, 10)  # Reduced from [60,65,70,75,80] to [60,70,80]
    }
    OPTIMIZATION_METRIC = 'sharpe_ratio' # Metric to optimize for in training folds
    logger.info(f"Optimization Metric for Training Folds: {OPTIMIZATION_METRIC}")
    logger.info(f"Optimization Parameter Grid: {OPTIMIZATION_PARAM_GRID}")
    
    # Calculate total parameter combinations to log
    param_combinations_count = 1
    for param_values in OPTIMIZATION_PARAM_GRID.values():
        param_combinations_count *= len(param_values)
    logger.info(f"Total parameter combinations to evaluate: {param_combinations_count} (reduced grid)")
    
    # 1. Fetch Full Data
    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: 
        logger.error("Failed to fetch price data for WFO.")
        return None
        
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
                    return None
    except Exception as freq_err:
         logger.warning(f"Could not infer frequency from data index, proceeding with original granularity: {freq_err}")
    # --- END ADDED SECTION ---
        
    if isinstance(full_price_data.index, pd.DatetimeIndex):
        logger.info("Price data index is confirmed to be DatetimeIndex.")
    else:
        logger.warning("Price data index is not confirmed to be DatetimeIndex.")
        return None # Exit if index is not correct type

    close = full_price_data['close']
    high = full_price_data['high']
    low = full_price_data['low']
    open_ = full_price_data['open'] # Needed for StochSMA strategy run
    
    # 2. Define WFO Splits
    periods_per_day = 86400 // granularity
    window_len_periods = int(wfo_window_years * 365.25 * periods_per_day)
    test_len_periods = int(wfo_test_days * periods_per_day)
    train_len_periods = max(1, window_len_periods - test_len_periods) 
    
    if train_len_periods + test_len_periods > len(close):
         logger.warning(f"WFO window length ({window_len_periods} periods) exceeds data length ({len(close)} periods). Adjusting...")
    
    # 4. Initialize Strategy Instance (outside loop)
    strategy = StochSMAStrategy(
        initial_capital=initial_capital, 
        commission_pct=commission_pct, 
        slippage_pct=slippage_pct,
        use_stops=use_stops, 
        sl_atr_multiplier=sl_atr_multiplier, 
        tsl_atr_multiplier=tsl_atr_multiplier, 
        trend_sma_window=trend_sma_window
    )

    # 5. Run WFO Loop (Modified for Adaptive Optimization)
    all_fold_results = []
    all_fold_best_params = {} # Store best params for each fold
    logger.info("--- Starting Adaptive WFO Loop --- ")
    n_datapoints = len(full_price_data)
    if window_len_periods > n_datapoints:
        logger.error(f"Data length ({n_datapoints}) is shorter than the WFO window length ({window_len_periods}). Cannot perform WFO.")
        return None # Return None instead of exiting
    
    n_manual_splits = ((n_datapoints - window_len_periods) // test_len_periods) + 1
    logger.info(f"Calculated {n_manual_splits} manual WFO splits.")
    if n_manual_splits <= 0:
         logger.error("WFO parameters result in 0 or negative splits.")
         return None # Return None instead of exiting
         
    try:
        for i in tqdm(range(n_manual_splits), desc="Running Adaptive WFO Segments"):
            train_start_idx = i * test_len_periods
            train_end_idx = train_start_idx + train_len_periods 
            test_start_idx = train_end_idx
            test_end_idx = test_start_idx + test_len_periods
            test_end_idx = min(test_end_idx, n_datapoints)
            test_start_idx = min(test_start_idx, test_end_idx)
            train_end_idx = test_start_idx
            train_start_idx = max(0, train_start_idx)
            train_end_idx = max(train_start_idx, train_end_idx)

            if train_start_idx >= train_end_idx or test_start_idx >= test_end_idx:
                 logger.warning(f"Split {i+1}: Invalid indices calculated. Skipping.")
                 continue

            fold_num = i + 1
            logger.info(f"\n--- Running Fold {fold_num}/{n_manual_splits} --- ")

            train_data = full_price_data.iloc[train_start_idx:train_end_idx]
            test_data = full_price_data.iloc[test_start_idx:test_end_idx]

            if train_data.empty or test_data.empty:
                 logger.warning(f"Fold {fold_num}: Train or Test data slice is empty. Skipping fold.")
                 all_fold_results.append(None)
                 all_fold_best_params[fold_num] = None
                 continue

            logger.info(f"Fold {fold_num}: Train Data {train_data.index[0]} to {train_data.index[-1]} ({len(train_data)} periods)")
            logger.info(f"Fold {fold_num}: Test Data  {test_data.index[0]} to {test_data.index[-1]} ({len(test_data)} periods)")

            # --- A) Optimize on Training Data ---
            logger.info(f"Fold {fold_num}: Optimizing parameters on training data...")
            try:
                # First try using vectorized optimization
                train_pf = strategy.optimize(
                    data=train_data.copy(), 
                    param_grid=OPTIMIZATION_PARAM_GRID, 
                    optimize_metric=OPTIMIZATION_METRIC, 
                    granularity_seconds=granularity
                )
                
                # Check if vectorized optimization failed
                if train_pf is None or not hasattr(train_pf, 'stats') or train_pf.stats().empty:
                    logger.warning(f"Fold {fold_num}: Vectorized optimization failed. Attempting sequential optimization...")
                    
                    # Try sequential optimization instead
                    train_pf = strategy.optimize_sequential(
                        data=train_data.copy(), 
                        param_grid=OPTIMIZATION_PARAM_GRID, 
                        optimize_metric=OPTIMIZATION_METRIC, 
                        granularity_seconds=granularity
                    )
                    
                    # Check if sequential optimization also failed
                    if train_pf is None or not hasattr(train_pf, 'stats'):
                         logger.warning(f"Fold {fold_num}: Both optimization methods failed. Skipping fold.")
                         all_fold_results.append(None)
                         all_fold_best_params[fold_num] = None
                         continue
                         
                # --- Extract Best Parameters ---
                # Get stats per column (parameter combination)
                try:
                    # First try with primary optimization metric
                    performance = train_pf.stats(OPTIMIZATION_METRIC, per_column=True) 
                    
                    # Add detailed debugging
                    if performance is not None:
                        logger.info(f"Fold {fold_num}: Performance shape: {performance.shape if hasattr(performance, 'shape') else 'no shape'}")
                        logger.info(f"Fold {fold_num}: Performance type: {type(performance)}")
                        logger.info(f"Fold {fold_num}: Performance contains NaNs: {performance.isna().any() if hasattr(performance, 'isna') else 'unknown'}")
                        if not performance.empty and len(performance) > 0:
                            logger.info(f"Fold {fold_num}: First few performance values: {performance.head(3) if hasattr(performance, 'head') else str(performance)[:100]}")
                            
                            # Check for all zero values which might indicate no trades
                            all_zeros = False
                            if hasattr(performance, 'values'):
                                all_zeros = (performance.values == 0).all() if hasattr(performance.values, 'all') else False
                            if all_zeros:
                                logger.warning(f"Fold {fold_num}: All performance values are zero. Possible no-trade scenario.")
                    
                    # Check if we need a fallback metric - use a simpler approach
                    need_fallback = False
                    if performance is None:
                        need_fallback = True
                    elif hasattr(performance, 'empty') and performance.empty:
                        need_fallback = True
                    elif hasattr(performance, 'isna'):
                        # For DataFrames/Series, check if all values are NaN in a safe way
                        try:
                            # If performance is a DataFrame, check if all values are NaN
                            if hasattr(performance, 'values') and performance.size > 0:
                                need_fallback = np.isnan(performance.values).all()
                            else:
                                need_fallback = True
                        except:
                            # If any error occurs, assume fallback is needed
                            need_fallback = True
                    
                    if need_fallback:
                        # Try fallback metrics in order of preference
                        fallback_metrics = ['total_return', 'win_rate', 'profit_factor']
                        
                        for fallback_metric in fallback_metrics:
                            logger.info(f"Fold {fold_num}: Trying fallback metric '{fallback_metric}'")
                            fallback_performance = train_pf.stats(fallback_metric, per_column=True)
                            
                            # Check if fallback performance is valid using same safe approach
                            fallback_is_valid = False
                            if fallback_performance is not None:
                                if not hasattr(fallback_performance, 'empty') or not fallback_performance.empty:
                                    # Check if it has usable values (not all NaN)
                                    try:
                                        if hasattr(fallback_performance, 'values') and fallback_performance.size > 0:
                                            fallback_is_valid = not np.isnan(fallback_performance.values).all()
                                    except:
                                        fallback_is_valid = False
                                        
                            if fallback_is_valid:
                                logger.info(f"Fold {fold_num}: Using fallback metric '{fallback_metric}' instead of '{OPTIMIZATION_METRIC}'")
                                performance = fallback_performance
                                # Update higher_better flag for the metric
                                higher_better = fallback_metric not in ['max_dd']
                                break
                                
                        # If all fallbacks failed, continue with original empty performance
                        fallback_still_needed = False
                        if performance is None:
                            fallback_still_needed = True
                        elif hasattr(performance, 'empty') and performance.empty:
                            fallback_still_needed = True
                        elif hasattr(performance, 'isna'):
                            # For DataFrames/Series, check if all values are NaN in a safe way
                            try:
                                # If performance is a DataFrame, check if all values are NaN
                                if hasattr(performance, 'values') and performance.size > 0:
                                    fallback_still_needed = np.isnan(performance.values).all()
                                else:
                                    fallback_still_needed = True
                            except:
                                # If any error occurs, assume fallback is needed
                                fallback_still_needed = True
                            
                        if need_fallback and fallback_still_needed:
                            logger.warning(f"Fold {fold_num}: All fallback metrics failed. Skipping fold.")
                            all_fold_results.append(None)
                            all_fold_best_params[fold_num] = None
                            continue
                    
                except Exception as stats_err:
                     logger.error(f"Fold {fold_num}: Error getting per-column stats for {OPTIMIZATION_METRIC}: {stats_err}", exc_info=True)
                     all_fold_results.append(None)
                     all_fold_best_params[fold_num] = None
                     continue
                 
                # Use the defined higher_better value based on the metric used
                best_param_idx_tuple = get_best_index(performance, higher_better=(OPTIMIZATION_METRIC not in ['max_dd']))

                if best_param_idx_tuple is None:
                    logger.warning(f"Fold {fold_num}: Could not determine best parameters from training optimization ({OPTIMIZATION_METRIC}). Skipping fold.")
                    all_fold_results.append(None)
                    all_fold_best_params[fold_num] = None
                    continue

                # Convert tuple index back to dict
                best_params_fold = dict(zip(OPTIMIZATION_PARAM_GRID.keys(), best_param_idx_tuple))
                logger.info(f"Fold {fold_num}: Best params from training: {best_params_fold}")
                all_fold_best_params[fold_num] = best_params_fold # Store best params for this fold
                
            except Exception as train_opt_err:
                logger.error(f"Fold {fold_num}: Error during training optimization: {train_opt_err}", exc_info=True)
                all_fold_results.append(None)
                all_fold_best_params[fold_num] = None
                continue

            # --- B) Test on Test Data using Best Params from Training ---
            logger.info(f"Fold {fold_num}: Testing with best parameters ({best_params_fold}) on test data...")
            try:
                 # Run optimize again, but with a single parameter set derived from training
                single_param_grid_test = {k: [v] for k, v in best_params_fold.items()}
                
                # First try with vectorized method
                test_pf = strategy.optimize(
                    data=test_data.copy(), # Pass TESTING data
                    param_grid=single_param_grid_test, # Use the single best set found in training
                    optimize_metric=OPTIMIZATION_METRIC, # Metric doesn't matter for single run
                    granularity_seconds=granularity
                )

                # If vectorized method fails, use sequential method as fallback
                if test_pf is None:
                     logger.warning(f"Fold {fold_num}: Vectorized test run failed. Trying sequential method...")
                     test_pf = strategy.optimize_sequential(
                         data=test_data.copy(),
                         param_grid=single_param_grid_test,
                         optimize_metric=OPTIMIZATION_METRIC,
                         granularity_seconds=granularity
                     )
                
                # Check if both methods failed
                if test_pf is None:
                     logger.warning(f"Fold {fold_num}: Both test methods failed. Skipping.")
                     all_fold_results.append(None)
                     continue

                # Extract the returns series for this single run
                # The column name should match the best_param_idx_tuple
                if best_param_idx_tuple in test_pf.returns.columns:
                     test_returns = test_pf.returns[best_param_idx_tuple]
                     all_fold_results.append(test_returns) # Append the Series of returns
                     segment_metrics = test_pf.stats() # Get stats for this segment (optional logging)
                     logger.info(f"Fold {fold_num} Test Metrics (using best train params): {segment_metrics[best_param_idx_tuple]}") # Log the specific column stats
                else:
                     logger.warning(f"Fold {fold_num}: Could not find returns column {best_param_idx_tuple} in test portfolio. Skipping.")
                     all_fold_results.append(None)
            
            except Exception as test_run_err:
                 logger.error(f"Fold {fold_num}: Error during test run with best params: {test_run_err}", exc_info=True)
                 all_fold_results.append(None)

    except Exception as e:
        logger.error(f"Error during Adaptive WFO loop: {e}", exc_info=True)
        return None

    logger.info(f"Completed iterating through {n_manual_splits} Adaptive WFO segments.") 

    # 6. Aggregate Results
    logger.info("\n--- Aggregating Adaptive WFO Results ---")
    # Filter out None results before concatenation
    valid_fold_returns = [r for r in all_fold_results if r is not None and isinstance(r, pd.Series)]
    
    # Explicitly log the number of valid returns series found
    logger.info(f"Found {len(valid_fold_returns)} valid fold return series out of {len(all_fold_results)} total folds")
    
    if len(valid_fold_returns) == 0:
         logger.error(f"Adaptive WFO finished for {symbol}, but no valid return series were generated for aggregation.")
         return None
         
    logger.info(f"Aggregating returns from {len(valid_fold_returns)} valid folds.")
    
    # Concatenate the list of returns Series
    all_returns = pd.concat(valid_fold_returns)
    all_returns = all_returns.sort_index() 
    
    # Remove potential overlaps if test windows slightly overlapped or duplicates exist
    all_returns = all_returns[~all_returns.index.duplicated(keep='first')]

    # Reindex to the full data range to handle potential gaps if segments were skipped
    # Ensure the index range covers the *test periods* accurately
    first_test_start_idx = train_len_periods # Index of the start of the first test period
    last_test_end_idx = n_datapoints # End of the last test period
    full_test_index = full_price_data.index[first_test_start_idx:last_test_end_idx]
    
    if not full_test_index.empty:
        all_returns = all_returns.reindex(full_test_index).fillna(0)
        logger.info(f"Combined returns reindexed to full test range: {full_test_index[0]} to {full_test_index[-1]}")
    else:
        logger.warning("Could not determine full test index range for reindexing.")
        # Proceed without reindexing, might have gaps
    
    # Calculate overall metrics directly from the aggregated returns series
    try:
        overall_metrics = all_returns.vbt.returns(freq=vbt_freq_str).stats()
        logger.info(f"Overall Adaptive WFO Performance Metrics: {overall_metrics}")
    except Exception as metrics_err:
        logger.error(f"Failed to calculate metrics from combined returns: {metrics_err}", exc_info=True)
        overall_metrics = pd.Series(name="Metrics Calculation Failed") 

    # --- Save Results ---
    reports_dir = f"reports/adaptive_wfo_stochsma/{symbol}_{granularity_str}" # New report directory
    logger.info(f"Attempting to save results to directory: {reports_dir}")
    reports_path = Path(reports_dir)
    try:
        reports_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured report directory exists: {reports_path}")
    except Exception as mkdir_err:
        logger.error(f"Failed to create report directory {reports_path}: {mkdir_err}", exc_info=True)
        return overall_metrics 
    
    # Save aggregated metrics
    metrics_df = pd.DataFrame([overall_metrics])
    metrics_file = reports_path / f"adaptive_wfo_{symbol}_{granularity_str}_metrics.csv" 
    metrics_df.to_csv(metrics_file, index=False)
    logger.info(f"Saved aggregated Adaptive WFO metrics to {metrics_file}")

    # Save the best parameters found for each fold
    params_file = reports_path / f"adaptive_wfo_{symbol}_{granularity_str}_best_params.json"
    try:
        # Convert numpy types to standard types for JSON serialization
        serializable_params = {}
        for fold, params in all_fold_best_params.items():
            if params:
                serializable_params[fold] = {k: (int(v) if isinstance(v, np.integer) else float(v) if isinstance(v, np.floating) else v) for k, v in params.items()}
            else:
                serializable_params[fold] = None
                
        with open(params_file, 'w') as f:
            json.dump(serializable_params, f, indent=4)
        logger.info(f"Saved best parameters per fold to {params_file}")
    except Exception as json_err:
        logger.error(f"Failed to save best parameters JSON: {json_err}")

    # Save the raw returns series
    returns_file = reports_path / f"adaptive_wfo_{symbol}_{granularity_str}_returns.csv" 
    all_returns.to_csv(returns_file)
    logger.info(f"Saved aggregated Adaptive WFO returns series to {returns_file}")
    
    return overall_metrics


if __name__ == "__main__":
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description='Run Adaptive Walk-Forward Optimization for StochSMA.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Trading pair symbol (e.g., BTC-USD, ETH-USD)')
    parser.add_argument('--start_date', type=str, default='2021-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default='2024-06-01', help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=int, default=14400, help='Data granularity in seconds (e.g., 14400 for 4H)')
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--no_stops', action='store_true', help='Disable stop loss usage')
    parser.add_argument('--sl_atr', type=float, default=1.5, help='ATR multiplier for stop loss')
    parser.add_argument('--tsl_atr', type=float, default=2.0, help='ATR multiplier for trailing stop loss')
    parser.add_argument('--trend_window', type=int, default=50, help='SMA window for trend filter')
    parser.add_argument('--wfo_test_days', type=int, default=90, help='Days for each WFO test period')
    parser.add_argument('--wfo_window_years', type=float, default=1.5, help='Total years for each WFO train+test window')
    args = parser.parse_args()

    # --- Configuration (using args or defaults) ---
    logger.info("Starting Adaptive StochSMA Walk-Forward Optimization Script")
    
    # Call the WFO function with parsed arguments (no best_params)
    overall_metrics = run_stochsma_wfo(
        symbol=args.symbol, 
        start_date=args.start_date, 
        end_date=args.end_date, 
        granularity=args.granularity, 
        initial_capital=args.initial_capital, 
        commission_pct=args.commission, 
        slippage_pct=args.slippage,
        use_stops=(not args.no_stops), 
        sl_atr_multiplier=args.sl_atr, 
        tsl_atr_multiplier=args.tsl_atr, 
        trend_sma_window=args.trend_window, 
        wfo_test_days=args.wfo_test_days, 
        wfo_window_years=args.wfo_window_years 
    )

    logger.info(f"Adaptive StochSMA Walk-Forward Optimization Script Finished for {args.symbol}") 