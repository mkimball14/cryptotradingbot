import vectorbtpro as vbt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import logging
import sys
import os
import json
from datetime import datetime
from typing import Tuple, Dict, List, Optional, Any
from pathlib import Path
from tqdm import tqdm  # For progress bars
import argparse
from functools import lru_cache
import traceback
from plotly.subplots import make_subplots
import warnings
import time
from itertools import product

# Add project root to sys.path 
# ... (Imports and Setup remain largely the same) ...
# // ... existing code ...

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Utility Functions (Copied) ---

def fetch_historical_data(product_id, start_date, end_date, granularity=86400):
    """
    Fetch historical price data from Coinbase or from cache.
    (Modified to read credentials directly from cdp_api_key.json)
    """
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    granularity_str = get_granularity_str(granularity)
    if not granularity_str:
        logger.error(f"Invalid granularity seconds: {granularity}. Cannot create cache key.")
        return create_sample_data(start_date, end_date)
    cache_file = cache_dir / f"{product_id.replace('-', '')}_{start_date}_{end_date}_{granularity_str}.csv"

    if cache_file.exists():
        logger.info(f"Loading cached data from: {cache_file}")
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if all(col in data.columns for col in required_cols):
                 logger.info(f"Successfully loaded cached data with shape: {data.shape}")
                 return data
            else:
                logger.warning(f"Cached data missing columns: {set(required_cols) - set(data.columns)}. Refetching.")
                cache_file.unlink()
        except Exception as e:
            logger.warning(f"Error loading cached data: {e}, will fetch fresh data")

    if "sample" in product_id.lower():
        return create_sample_data(start_date, end_date)

    # Read credentials directly from the JSON file
    creds_file = "cdp_api_key.json"
    if not os.path.exists(creds_file):
        logger.warning(f"Credentials file not found: {creds_file}. Generating sample data.")
        return create_sample_data(start_date, end_date)

    try:
        with open(creds_file, 'r') as f:
            creds = json.load(f)
        key_name = creds.get('name')
        private_key = creds.get('privateKey')

        if not key_name or not private_key:
            logger.warning(f"Missing 'name' or 'privateKey' in {creds_file}. Generating sample data.")
            return create_sample_data(start_date, end_date)

        client = RESTClient(api_key=key_name, api_secret=private_key)
        logger.info(f"Requesting candles from Coinbase API (Granularity: {granularity_str}) using keys from {creds_file}")

        start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

        max_candles_per_request = 300 
        total_seconds = end_timestamp - start_timestamp
        total_candles_needed = total_seconds // granularity
        chunks = (total_candles_needed + max_candles_per_request - 1) // max_candles_per_request
        logger.info(f"Need {total_candles_needed} candles, fetching in {chunks} chunks of max {max_candles_per_request}...")

        all_candles = []
        current_start_timestamp = start_timestamp

        for i in tqdm(range(chunks), desc="Fetching Candles"):
            current_end_timestamp = current_start_timestamp + (max_candles_per_request * granularity) 
            current_end_timestamp = min(current_end_timestamp, end_timestamp)

            if current_end_timestamp <= current_start_timestamp:
                if i == 0 and total_candles_needed <= 0:
                     logger.warning("Date range results in zero candles needed.")
                else: 
                     logger.warning(f"Chunk {i+1} calculation resulted in end <= start timestamp. Breaking fetch loop.")
                break

            logger.debug(f"Fetching chunk {i+1}/{chunks}: {datetime.fromtimestamp(current_start_timestamp)} to {datetime.fromtimestamp(current_end_timestamp)}")
            params = {"granularity": granularity_str, "start": str(current_start_timestamp), "end": str(current_end_timestamp)}

            try:
                candles_response = client.get_public_candles(product_id=product_id, **params)
                if hasattr(candles_response, 'candles') and candles_response.candles:
                     chunk_data = [c.to_dict() for c in candles_response.candles]
                     all_candles.extend(chunk_data)
                     logger.debug(f"Got {len(chunk_data)} candles for chunk {i+1}")
                else:
                     logger.warning(f"No candles returned for chunk {i+1}. Response: {candles_response}")
            except Exception as chunk_error:
                logger.error(f"Error fetching chunk {i+1}: {chunk_error}")
                if i == 0: 
                     logger.info("First chunk fetch failed critically, falling back to sample data")
                     return create_sample_data(start_date, end_date)
                break 
            
            current_start_timestamp = current_end_timestamp
            if current_start_timestamp >= end_timestamp:
                break
            time.sleep(0.3) 

        if not all_candles:
            logger.warning("No candles fetched after attempting all chunks. Generating sample data.")
            return create_sample_data(start_date, end_date)

        df = pd.DataFrame(all_candles)
        expected_cols = ['start', 'low', 'high', 'open', 'close', 'volume']
        if not all(col in df.columns for col in expected_cols):
            logger.error(f"Candle data missing expected columns (start,low,high,open,close,volume). Got: {df.columns.tolist()}")
            return create_sample_data(start_date, end_date)

        df.rename(columns={'start': 'time'}, inplace=True)
        try:
            df['time'] = pd.to_datetime(pd.to_numeric(df['time']), unit='s')
        except (ValueError, TypeError):
            df['time'] = pd.to_datetime(df['time'])
            
        df.set_index('time', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        df.sort_index(inplace=True)
        df['high'] = df[['open', 'high', 'low', 'close']].max(axis=1)
        df['low'] = df[['open', 'high', 'low', 'close']].min(axis=1)

        df.to_csv(cache_file)
        logger.info(f"Cached {len(df)} data points to: {cache_file}")
        return df # Ensure df is returned here

    except Exception as e:
        logger.error(f"General error fetching data via RESTClient: {e}")
        logger.debug(traceback.format_exc())
        logger.info("Generating sample data due to error.")
        return create_sample_data(start_date, end_date)

def get_granularity_str(granularity_seconds: int) -> Optional[str]:
    # Restore the mapping dictionary
    gran_map = {
        60: "ONE_MINUTE", 300: "FIVE_MINUTES", 900: "FIFTEEN_MINUTES",
        1800: "THIRTY_MINUTES", 3600: "ONE_HOUR", 7200: "TWO_HOURS",
        21600: "SIX_HOURS", 86400: "ONE_DAY"
    }
    return gran_map.get(granularity_seconds)

def create_sample_data(start_date, end_date, initial_price=20000.0, daily_vol=0.02):
    # ... (create_sample_data remains the same) ...
    # // ... existing code ...
    return data

def calculate_risk_metrics(portfolio):
    # ... (calculate_risk_metrics remains the same) ...
    # // ... existing code ...
    return metrics

# --- Strategy Definition (No longer using IndicatorFactory) ---
# The logic is embedded in the simulation functions.

# --- Main Execution Logic ---

def run_backtest(
    symbol, start_date, end_date, granularity=86400,
    initial_capital=10000, commission_pct=0.001, slippage_pct=0.0005,
    param_grid=None, optimize_metric='sharpe_ratio',
    use_stops=True, sl_atr_multiplier=1.0, tsl_atr_multiplier=1.0,
    wfo_test_days=180, wfo_window_years=2
):
    """
    Manual WFO: Optimizes MACD params IS, tests OOS using FIXED stops.
    (Calculates indicators directly).
    """
    logger.info(f"--- Running Manual WFO (MACD Crossover - Fixed Stops) for {symbol} ---") # Updated title
    logger.info(f"Fixed Stop Params: SL ATR Mult={sl_atr_multiplier}, TSL ATR Mult={tsl_atr_multiplier}")
    logger.info(f"WFO Params: Test Days={wfo_test_days}, Window Years={wfo_window_years}")

    # --- Start: Restore data loading ---
    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: 
        logger.error(f"Could not fetch or load data for {symbol}.")
        return None, None, None
    # --- End: Restore data loading ---

    # --- Define Parameter Grid (MACD) ---
    if param_grid is None:
        param_grid = {
            'fast_window': np.arange(5, 26, 5),     # Wider Range: 5, 10, 15, 20, 25 
            'slow_window': np.arange(20, 61, 10),   # Wider Range: 20, 30, 40, 50, 60
            'signal_window': np.arange(5, 16, 3)    # Wider Range: 5, 8, 11, 14
        }
    logger.info(f"Optimization Parameter Grid: {param_grid}") 
    param_names_ordered = list(param_grid.keys())
    logger.info(f"Parameter Order for Optimization: {param_names_ordered}")

    # --- Start: Add back metric mapping --- 
    metric_map = {'sharpe ratio': 'sharpe_ratio', 'total return': 'total_return', 'max drawdown': 'max_drawdown'}
    vbt_metric = metric_map.get(optimize_metric.lower(), 'sharpe_ratio')
    higher_better = vbt_metric not in ['max_drawdown']
    # --- End: Add back metric mapping --- 
    logger.info(f"Using '{vbt_metric}' as optimization metric (higher_better={higher_better}).")

    # --- Start: Add back WFO split calculation logic ---
    logger.info("Manually calculating split indices...")
    n_total = len(full_price_data); window_len = int(wfo_window_years * 365.25)
    test_len = wfo_test_days; train_len = window_len - test_len
    if train_len <= 0 or window_len > n_total: 
        logger.error("WFO train length invalid or window too large for data.")
        return None, None, full_price_data
    split_indices = []
    current_start = 0
    while current_start + window_len <= n_total:
        train_start = current_start; train_end = current_start + train_len
        test_start = train_end; test_end = min(current_start + window_len, n_total)
        if test_start >= test_end: break # Avoid empty test set
        split_indices.append((np.arange(train_start, train_end), np.arange(test_start, test_end)))
        current_start += test_len # Step forward by test length for next split
    n_splits = len(split_indices)
    if n_splits == 0: 
        logger.error("Could not generate any WFO splits with the given parameters.")
        return None, None, full_price_data
    logger.info(f"Manual calculation generated {n_splits} splits.")
    # --- End: Add back WFO split calculation logic ---
    
    oos_results_sharpe = {}; oos_results_return = {}; oos_results_drawdown = {}
    best_params_history = {}

    logger.info("Starting Walk-Forward Iteration (Manual Indices)...")
    for i, (train_idx, test_idx) in enumerate(tqdm(split_indices, total=n_splits, desc="WFO Splits")):
        in_price_split = full_price_data.iloc[train_idx]
        out_price_split = full_price_data.iloc[test_idx]
        if in_price_split.empty or out_price_split.empty: continue

        # 1. Optimize on In-Sample Data
        in_performance = simulate_all_params_single_split_direct(
            in_price_split, param_grid, 
            initial_capital, commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
            vbt_metric
        )
        if in_performance is None or in_performance.empty:
             logger.warning(f"Split {i}: In-sample simulation returned no performance data.")
             continue

        # ... (Best param selection remains the same) ...
        # // ... existing code ...

        # 4. Test Best Parameters on Out-of-Sample Data
        oos_metrics_dict = simulate_best_params_single_split_direct(
            out_price_split, best_params_split, 
            initial_capital, commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier
        )
        # ... (OOS results storage remains the same) ...
        # // ... existing code ...

    # --- Aggregate and Prepare Final Results ---
    # ... (Aggregation remains the same) ...
    logger.info("--- Final Aggregated OOS Performance (MACD Crossover - Fixed Stops) ---") # Updated title
    # ... (Logging for stops and metric remains the same) ...
    # // ... existing code ...

    wfo_results_dict = {
        'strategy_name': 'MACD Crossover', # Updated name
        # ... (Rest of results dict remains the same) ...
    }
    return None, wfo_results_dict, full_price_data 

# --- WFO Helper Function: Simulate All Parameters (Direct Calculation - MACD) ---
def simulate_all_params_single_split_direct(price_data, param_grid, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier, metric='sharpe_ratio'):
    """ Simulates MACD Crossover param combinations (with zero-line filter) on a SINGLE split using direct indicator calculation. """
    logger.debug(f"Simulating MACD Crossover (+Zero Line Filter) params (fixed stops) on single split data shape: {price_data.shape}")
    close = price_data['close']; high = price_data['high']; low = price_data['low']

    # --- Calculate Stops Once --- 
    # ... (Stop loss calculation remains the same) ...
    # // ... existing code ...

    # --- Pre-Calculate ALL Indicator Variations ONCE --- 
    try:
        # Pre-calculate MACD for all combinations 
        macd_all = vbt.MACD.run(
            close, 
            fast_window=param_grid['fast_window'],
            slow_window=param_grid['slow_window'],
            signal_window=param_grid['signal_window'],
            short_name='macd',
            param_product=True,
            hide_params=['macd_ewm', 'signal_ewm'] # Hide less relevant params from column names
        )
        
        if macd_all is None:
             raise ValueError("MACD calculation failed.")

    except Exception as ind_err:
        logger.error(f"Simulate_all_direct: Error during pre-calculation of MACD: {ind_err}", exc_info=True)
        return None

    # --- Generate Signals by Selecting Pre-Calculated Indicators --- 
    all_entries = []
    all_exits = []
    all_params_tuples = []
    param_names_ordered = list(param_grid.keys())
    param_combinations = list(product(*param_grid.values()))
    valid_combinations_count = 0

    try:
        for params_tuple in param_combinations:
            current_params = dict(zip(param_names_ordered, params_tuple))
            all_params_tuples.append(params_tuple)

            # Extract parameters
            fast_w = current_params['fast_window']
            slow_w = current_params['slow_window']
            signal_w = current_params['signal_window']

            # Skip invalid combinations (fast >= slow)
            if fast_w >= slow_w:
                all_entries.append(pd.Series(False, index=close.index))
                all_exits.append(pd.Series(False, index=close.index))
                continue 
            
            # Select the correct pre-calculated series (use tuple for multi-index)
            param_key = (fast_w, slow_w, signal_w)
            try:
                current_macd_line = macd_all.macd.loc[:, param_key]
                current_signal_line = macd_all.signal.loc[:, param_key]
            except KeyError:
                 logger.warning(f"Could not find pre-calculated MACD for key {param_key}. Indices available: {macd_all.macd.columns}")
                 all_entries.append(pd.Series(False, index=close.index))
                 all_exits.append(pd.Series(False, index=close.index))
                 continue

            # Skip if any required indicator failed calculation or is unavailable
            if current_macd_line is None or current_signal_line is None or \
               current_macd_line.isnull().all() or current_signal_line.isnull().all():
                 all_entries.append(pd.Series(False, index=close.index))
                 all_exits.append(pd.Series(False, index=close.index))
                 continue
            
            # Generate signals for this combination (MACD Crossover + Zero Line Filter)
            entries = current_macd_line.vbt.crossed_above(current_signal_line) & (current_macd_line > 0)
            exits = current_macd_line.vbt.crossed_below(current_signal_line)

            all_entries.append(entries)
            all_exits.append(exits)
            valid_combinations_count += 1
            
        if valid_combinations_count == 0:
             logger.warning("No valid signals generated across all parameter combinations.")
             return None
             
        # Combine signals into DataFrames with parameter multi-index
        valid_params_tuples = [t for t in all_params_tuples if t[param_names_ordered.index('fast_window')] < t[param_names_ordered.index('slow_window')]]
        if not valid_params_tuples:
            logger.warning("No valid parameter combinations found (fast_window < slow_window).")
            return None
        param_multi_index = pd.MultiIndex.from_tuples(valid_params_tuples, names=param_names_ordered)
        
        # Filter entries/exits before concatenating
        valid_entries = [all_entries[i] for i, t in enumerate(all_params_tuples) if t in valid_params_tuples]
        valid_exits = [all_exits[i] for i, t in enumerate(all_params_tuples) if t in valid_params_tuples]
        
        # Ensure lists are not empty before concat
        if not valid_entries or not valid_exits:
             logger.warning("No valid entry/exit signals after filtering parameter combinations.")
             return None
             
        entries_output = pd.concat(valid_entries, axis=1, keys=param_multi_index)
        exits_output = pd.concat(valid_exits, axis=1, keys=param_multi_index)

    except Exception as signal_err:
         logger.error(f"Simulate_all_direct: Error during signal generation/combination: {signal_err}", exc_info=True)
         return None
        
    # --- Run Portfolio Simulation --- 
    # ... (Portfolio simulation remains the same) ...
    # // ... existing code ...

# --- WFO Helper Function: Simulate Best Parameters (Direct Calculation - MACD) ---
def simulate_best_params_single_split_direct(price_data, best_params_dict, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier):
    """ Simulates the single best MACD Crossover (+Zero Line) param set on a SINGLE split using direct calculation. """
    logger.debug(f"Simulating best MACD Crossover (+Zero Line Filter) params (fixed stops) on OOS data shape: {price_data.shape}")
    close = price_data['close']; high = price_data['high']; low = price_data['low']

    try:
        fast_w = int(best_params_dict['fast_window'])
        slow_w = int(best_params_dict['slow_window'])
        signal_w = int(best_params_dict['signal_window'])
        
        # Basic validation
        if fast_w >= slow_w:
             logger.error(f"Invalid best params: fast_window {fast_w} >= slow_window {slow_w}")
             return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}
             
    except KeyError as ke:
        logger.error(f"Missing key in best_params_dict: {ke}. Params: {best_params_dict}")
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}

    # --- Calculate Indicators for the specific best parameters --- 
    try:
        # Validate windows against data length
        if fast_w < 1 or slow_w < 1 or signal_w < 1 or \
           fast_w >= len(close) or slow_w >= len(close) or signal_w >= len(close):
            raise ValueError(f"MACD window invalid for data length {len(close)}")
            
        macd_indicator = vbt.MACD.run(close, fast_window=fast_w, slow_window=slow_w, signal_window=signal_w)
        macd_line = macd_indicator.macd
        signal_line = macd_indicator.signal
        
        if macd_line.isnull().all() or signal_line.isnull().all():
            raise ValueError("MACD calculation resulted in all NaNs")

        # Generate signals (MACD Crossover + Zero Line Filter)
        entries = macd_line.vbt.crossed_above(signal_line) & (macd_line > 0)
        exits = macd_line.vbt.crossed_below(signal_line)
        
    except Exception as ind_err:
        logger.error(f"Indicator calculation error for best params {best_params_dict}: {ind_err}")
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}

    # --- Calculate Stops --- 
    # ... (Stop calculation remains the same) ...
    # // ... existing code ...

    # --- Run Portfolio --- 
    # ... (Portfolio simulation remains the same) ...
    logger.debug(f"Finished simulate_best_direct (MACD Crossover). Metrics: {metrics_dict}")
    # // ... existing code ...

# ... (get_best_index remains the same) ...
# // ... existing code ...

# --- Main function --- 
def main():
    parser = argparse.ArgumentParser(description='Backtest MACD Crossover strategy (with Zero Line Filter) using VectorBT Pro with Manual WFO.') # Updated description
    # Restore original argparse definitions
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1d', help='Data granularity (1d only supported)')
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--optimize_metric', type=str, default='Sharpe Ratio', help='Metric to optimize for IS')
    parser.add_argument('--no_stops', action='store_true', help='Disable stop loss usage globally')
    parser.add_argument('--sl_atr', type=float, default=1.5, help='ATR multiplier for stop loss (default: 1.5)')
    parser.add_argument('--tsl_atr', type=float, default=2.0, help='ATR multiplier for trailing stop loss (default: 2.0)')
    parser.add_argument('--reports_dir', type=str, default='reports', help='Directory to save reports')
    parser.add_argument('--wfo_test_days', type=int, default=90, help='Days in OOS test set')
    parser.add_argument('--wfo_window_years', type=float, default=2.0, help='Total years in each rolling window')

    args = parser.parse_args() 
    granularity_map = {'1d': 86400}; granularity_seconds = granularity_map.get(args.granularity.lower())
    if granularity_seconds is None: 
        logger.error("Use '1d' granularity."); 
        sys.exit(1)
    reports_path = Path(args.reports_dir); reports_path.mkdir(parents=True, exist_ok=True)

    # Call the backtest function 
    _, wfo_results, full_price_data = run_backtest(
        symbol=args.symbol, 
        start_date=args.start_date, 
        end_date=args.end_date,
        granularity=granularity_seconds, 
        initial_capital=args.initial_capital,
        commission_pct=args.commission, 
        slippage_pct=args.slippage, 
        param_grid=None, # Use default grid in function
        optimize_metric=args.optimize_metric, 
        use_stops=(not args.no_stops),
        sl_atr_multiplier=args.sl_atr,
        tsl_atr_multiplier=args.tsl_atr,
        wfo_test_days=args.wfo_test_days, 
        wfo_window_years=args.wfo_window_years
    )

    if wfo_results:
        logger.info(f"--- Manual WFO ({wfo_results.get('strategy_name', 'MACD Crossover + Zero')}) Results Summary ---") # Updated title 
        # ... (Logging for stops/metric remains the same) ...
        # // ... existing code ...
        try:
            # --- Save WFO Results ---
            stops_suffix = f"_SL{args.sl_atr}_TSL{args.tsl_atr}" if (not args.no_stops) else "_NoStops"
            save_filename = f"manual_macd_zero_wfo_results_{args.symbol}{stops_suffix}.json" # Updated filename
            # ... (JSON saving logic remains the same) ...
            # // ... existing code ...

            # --- Plot OOS Performance Metric --- 
            plot_metric = wfo_results.get('optimized_metric', 'sharpe_ratio')
            # Correct key mapping based on how metrics are stored
            metric_key_map = {
                 'sharpe_ratio': 'oos_sharpe',
                 'total_return': 'oos_return',
                 'max_drawdown': 'oos_drawdown'
            }
            # Use lower case and underscore for matching metric keys
            plot_metric_key = metric_key_map.get(plot_metric.lower().replace(" ", "_"), 'oos_sharpe') # Default to sharpe

            if plot_metric_key in wfo_results and wfo_results[plot_metric_key]:
                 try:
                      # Convert the dict back to Series for plotting
                      plot_data_dict = wfo_results[plot_metric_key]
                      # Ensure keys are integers for correct plotting order
                      plot_series = pd.Series({int(k): v for k, v in plot_data_dict.items() if v is not None}).sort_index()

                      if not plot_series.empty:
                           plot_title = f"OOS {plot_metric} per Split (MACD Crossover + Zero Line {stops_suffix})" # Updated title
                           fig = plot_series.vbt.plot(title=plot_title)
                           plot_filename = f"manual_macd_zero_wfo_oos_{plot_metric}{stops_suffix}_{args.symbol}.html" # Updated filename
                           plot_path = reports_path / plot_filename
                           fig.write_html(str(plot_path)); logger.info(f"OOS {plot_metric} plot saved to {plot_path}")
                      else:
                          logger.warning(f"No valid data to plot for OOS metric: {plot_metric_key}")
                 except Exception as plot_err: logger.warning(f"Could not plot OOS {plot_metric}: {plot_err}", exc_info=True)
            else:
                 logger.warning(f"OOS metric data key '{plot_metric_key}' not found or empty in results.")

        except Exception as save_err: logger.error(f"Error saving/plotting WFO results: {save_err}", exc_info=True)
    else: logger.warning("Manual WFO (MACD Crossover + Zero Line - Direct Calc) did not produce results.") # Updated message

    # Dashboard creation is removed for now
    logger.info("--- Backtest Script Finished ---")

if __name__ == "__main__":
    # ... (Warnings remain the same) ...
    # // ... existing code ...
    main() 