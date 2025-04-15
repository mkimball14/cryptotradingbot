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
import pandas_ta as ta # Import pandas-ta

# Add project root to sys.path to allow importing app modules
# Assume the script is run from the project root or the path is adjusted accordingly
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Import the base SDK client directly for this script
    from coinbase.rest import RESTClient
    # We might still need Settings for other parts, keep import for now
    # from app.core.coinbase import CoinbaseClient # No longer needed for data fetching here
    from app.core.config import Settings
    try:
        settings = Settings() # Load settings if available (might be needed elsewhere)
    except Exception as settings_err:
        logger.warning(f"Could not load Settings: {settings_err}. Some features might be limited.")
        settings = None
except ImportError as e:
    logger = logging.getLogger() # Use basic logger if setup failed
    logger.warning(f"Could not import coinbase.rest.RESTClient or Settings: {e}. Ensure paths/dependencies.")
    # Define placeholders if import fails
    class RESTClient:
        def __init__(self, *args, **kwargs):
            logger.warning("Using placeholder RESTClient.")
        def get_public_candles(self, *args, **kwargs):
            logger.warning("Placeholder RESTClient cannot fetch data.")
            return None
    settings = None # Indicate settings failed to load

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Utility Functions (Copied from backtest_rsi_vbt_pro.py, potentially modify later) ---

def fetch_historical_data(product_id, start_date, end_date, granularity=86400): # Default to 1 day (86400 seconds)
    """
    Fetch historical price data from Coinbase or from cache.
    (Handles different granularities)
    """
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    granularity_str = get_granularity_str(granularity)
    if not granularity_str:
        logger.error(f"Invalid granularity seconds: {granularity}. Cannot create cache key or fetch data.")
        return None # Cannot proceed without valid granularity
    
    # Update cache file naming for granularity
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
        # Use the exact key names from the JSON file
        key_name = creds.get('name')
        private_key = creds.get('privateKey')

        if not key_name or not private_key:
            logger.warning(f"Missing 'name' or 'privateKey' in {creds_file}. Generating sample data.")
            return create_sample_data(start_date, end_date)

        # Initialize the base RESTClient directly using SDK arguments
        client = RESTClient(api_key=key_name, api_secret=private_key)
        logger.info(f"Requesting candles from Coinbase API (Granularity: {granularity_str}) using keys from {creds_file}")

        # Convert dates to Unix timestamps for the API call
        start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

        # --- Re-implement Chunking Logic ---
        max_candles_per_request = 300 # API limit (use slightly less than 350 to be safe)
        total_seconds = end_timestamp - start_timestamp
        total_candles_needed = total_seconds // granularity
        chunks = (total_candles_needed + max_candles_per_request - 1) // max_candles_per_request
        logger.info(f"Need {total_candles_needed} candles ({granularity_str}), fetching in {chunks} chunks of max {max_candles_per_request}...")

        all_candles = []
        current_start_timestamp = start_timestamp

        for i in tqdm(range(chunks), desc="Fetching Candles"):
            # Calculate end timestamp for this chunk
            # Add max_candles * granularity seconds to the start
            current_end_timestamp = current_start_timestamp + (max_candles_per_request * granularity)
            # Ensure chunk end doesn't exceed the overall end time
            current_end_timestamp = min(current_end_timestamp, end_timestamp)

            # If the calculated end is less than or same as start, break (shouldn't happen with proper logic but safety check)
            if current_end_timestamp <= current_start_timestamp:
                if i == 0 and total_candles_needed <= 0: # Handle edge case of 0 duration
                     logger.warning("Date range results in zero candles needed.")
                else:
                     logger.warning(f"Chunk {i+1} calculation resulted in end <= start timestamp. Breaking fetch loop.")
                break

            logger.debug(f"Fetching chunk {i+1}/{chunks}: {datetime.fromtimestamp(current_start_timestamp)} to {datetime.fromtimestamp(current_end_timestamp)}")

            # Prepare parameters for this chunk
            params = {
                "granularity": granularity_str,
                "start": str(current_start_timestamp),
                "end": str(current_end_timestamp)
            }

            try:
                # Use the SDK's get_public_candles method for the chunk
                candles_response = client.get_public_candles(product_id=product_id, **params)

                # Process the response
                if hasattr(candles_response, 'candles') and candles_response.candles:
                     chunk_data = [c.to_dict() for c in candles_response.candles]
                     all_candles.extend(chunk_data)
                     logger.debug(f"Got {len(chunk_data)} candles for chunk {i+1}")
                else:
                     logger.warning(f"No candles returned for chunk {i+1}. Response: {candles_response}")
                     # Optionally break or continue based on requirements
            except Exception as chunk_error:
                logger.error(f"Error fetching chunk {i+1}: {chunk_error}")
                if i == 0: # If first chunk fails, fallback to sample data
                     logger.info("First chunk fetch failed critically, falling back to sample data")
                     return create_sample_data(start_date, end_date)
                # Decide if we should break or just skip this chunk
                break

            # Update start timestamp for the next chunk
            # Start next chunk right after the end of the current one
            current_start_timestamp = current_end_timestamp

            # Break if we have reached or passed the overall end timestamp
            if current_start_timestamp >= end_timestamp:
                break

            # Add a small delay to avoid rate limiting
            time.sleep(0.3)

        # Check if any candles were fetched
        if not all_candles:
            logger.warning("No candles fetched after attempting all chunks. Generating sample data.")
            return create_sample_data(start_date, end_date)

        # --- Candle processing logic (should be fine if candle dicts are correct) ---
        df = pd.DataFrame(all_candles)
        expected_cols = ['start', 'low', 'high', 'open', 'close', 'volume'] # SDK uses 'start' for time
        if not all(col in df.columns for col in expected_cols):
            logger.error(f"Candle data missing expected columns (start,low,high,open,close,volume). Got: {df.columns.tolist()}")
            return create_sample_data(start_date, end_date)

        # Rename 'start' to 'time' and convert
        df.rename(columns={'start': 'time'}, inplace=True)
        try:
            df['time'] = pd.to_datetime(pd.to_numeric(df['time']), unit='s')
        except (ValueError, TypeError):
            df['time'] = pd.to_datetime(df['time'])

        df.set_index('time', inplace=True)
        # Select only the necessary OHLCV columns in the standard order
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        df.sort_index(inplace=True)

        # Ensure OHLC integrity
        df['high'] = df[['open', 'high', 'low', 'close']].max(axis=1)
        df['low'] = df[['open', 'high', 'low', 'close']].min(axis=1)

        df.to_csv(cache_file)
        logger.info(f"Cached {len(df)} data points to: {cache_file}")
        return df

    except Exception as e:
        logger.error(f"General error fetching data via RESTClient: {e}")
        logger.debug(traceback.format_exc())
        logger.info("Generating sample data due to error.")
        return create_sample_data(start_date, end_date)

# Helper function to map seconds to granularity strings
def get_granularity_str(granularity_seconds: int) -> Optional[str]:
    # Ensure 1H is present and correct
    gran_map = {
        60: "ONE_MINUTE", 300: "FIVE_MINUTES", 900: "FIFTEEN_MINUTES",
        1800: "THIRTY_MINUTES", 3600: "ONE_HOUR", 7200: "TWO_HOURS",
        14400: "FOUR_HOURS", # Keep 4H in case it's supported later or needed elsewhere
        21600: "SIX_HOURS", 86400: "ONE_DAY"
    }
    return gran_map.get(granularity_seconds)

# Helper function to map seconds to vectorbt frequency strings
def get_vbt_freq_str(granularity_seconds: int) -> Optional[str]:
    # Map seconds to pandas frequency strings suitable for vectorbt
    vbt_freq_map = {
        60: "1T", 300: "5T", 900: "15T", 1800: "30T",
        3600: "1H", 7200: "2H", 14400: "4H", 21600: "6H", 86400: "1D"
    }
    return vbt_freq_map.get(granularity_seconds)

def create_sample_data(start_date, end_date, initial_price=20000.0, daily_vol=0.02):
    """Creates sample daily OHLCV data."""
    logger.info(f"Creating sample price data from {start_date} to {end_date}...")
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"sample_{start_date}_{end_date}.csv"

    if cache_file.exists():
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if all(col in data.columns for col in required_cols):
                 logger.info(f"Loaded {len(data)} days of cached sample data from: {cache_file}")
                 return data
            else:
                 logger.warning("Cached sample data invalid. Regenerating...")
                 cache_file.unlink()
        except Exception as e:
            logger.warning(f"Error loading cached sample data: {e}. Regenerating...")


    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    # Ensure the date range includes the end date
    daterange = pd.date_range(start=start, end=end + pd.Timedelta(days=1) , freq='D')[:-1]


    np.random.seed(42)
    price = initial_price
    prices = []
    for _ in range(len(daterange)):
        daily_return = np.random.normal(0.0002, daily_vol)
        price *= (1 + daily_return)
        prices.append(price)

    close_prices = pd.Series(prices, index=daterange)
    data = pd.DataFrame(index=daterange)
    data['close'] = close_prices
    data['open'] = data['close'].shift(1).fillna(method='bfill') # Backfill first open
    rand_h = np.random.uniform(0, 0.03, len(data))
    rand_l = np.random.uniform(0, 0.03, len(data))
    data['high'] = np.maximum(data['open'], data['close']) * (1 + rand_h)
    data['low'] = np.minimum(data['open'], data['close']) * (1 - rand_l)

    price_changes = np.abs(data['close'].pct_change().fillna(0.01))
    base_volume = 1000
    data['volume'] = base_volume * (1 + 5 * price_changes) + np.random.uniform(0, base_volume * 0.1, len(data))

    try:
        data.to_csv(cache_file)
        logger.info(f"Cached {len(data)} days of sample data to: {cache_file}")
    except Exception as e:
        logger.error(f"Error caching sample data: {e}")

    logger.info(f"Generated {len(data)} days of sample price data.")
    return data


def calculate_risk_metrics(portfolio):
    """
    Calculate key risk and performance metrics from a VectorBT portfolio.
    Handles potential missing stats gracefully.
    """
    metrics = {
        'total_return': 0, 'sharpe': 0, 'max_dd': 0, 'win_rate': 0,
        'trades': 0, 'annual_return': 0, 'sortino': 0, 'profit_factor': 0,
        'recovery_factor': 0
    }
    if portfolio is None:
        return metrics

    try:
        stats = portfolio.stats()
        returns = portfolio.returns

        # Basic metrics
        metrics['total_return'] = stats.get('Total Return [%]', 0) / 100
        metrics['sharpe'] = stats.get('Sharpe Ratio', 0)
        metrics['max_dd'] = stats.get('Max Drawdown [%]', 0) / 100
        metrics['trades'] = stats.get('Total Trades', 0)
        metrics['win_rate'] = stats.get('Win Rate [%]', 0) / 100
        metrics['profit_factor'] = stats.get('Profit Factor', 0)

        # Calculated metrics
        if metrics['max_dd'] > 0:
            metrics['recovery_factor'] = metrics['total_return'] / metrics['max_dd']
        else:
             metrics['recovery_factor'] = float('inf') if metrics['total_return'] > 0 else 0

        # Annualized Return
        start_date = portfolio.wrapper.index[0]
        end_date = portfolio.wrapper.index[-1]
        years = (end_date - start_date).days / 365.25
        if years > 0:
             metrics['annual_return'] = (1 + metrics['total_return'])**(1/years) - 1
        else:
             metrics['annual_return'] = 0 # Avoid division by zero for short periods

        # Sortino Ratio
        metrics['sortino'] = stats.get('Sortino Ratio', 0) # VBT Pro often calculates this

    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}", exc_info=True)
        # Return defaults if error occurs

    return metrics


# --- Strategy Definition (No longer using IndicatorFactory) ---
# The logic is now embedded in the simulation functions.

# --- Main Execution Logic ---

def run_backtest(
    symbol, start_date, end_date, granularity=3600,
    initial_capital=10000, commission_pct=0.001, slippage_pct=0.0005,
    param_grid=None, optimize_metric='sharpe_ratio',
    use_stops=True, sl_atr_multiplier=1.0, tsl_atr_multiplier=1.0,
    trend_sma_window=100,
    wfo_test_days=180, wfo_window_years=2
):
    """
    Manual WFO: Optimizes RSI+BB params IS, tests OOS using FIXED stops.
    (Calculates indicators directly, RSI VBT, BBands pandas-ta). Runs on specified granularity.
    """
    granularity_str = get_granularity_str(granularity) or f"{granularity}s" # Get string for logging
    logger.info(f"--- Running Manual WFO (RSI + Bollinger Bands - pandas-ta, Fixed Stops) for {symbol} ({granularity_str}) ---")
    logger.info(f"Period: {start_date} to {end_date} | Granularity: {granularity_str}")
    logger.info(f"Portfolio Settings: IC={initial_capital}, Comm={commission_pct*100:.3f}%, Slip={slippage_pct*100:.3f}% | Stops Enabled={use_stops}")
    if use_stops:
        logger.info(f"Fixed Stop Params: SL ATR Mult={sl_atr_multiplier}, TSL ATR Mult={tsl_atr_multiplier}")
    logger.info(f"WFO Params: Test Days={wfo_test_days}, Window Years={wfo_window_years}")
    logger.info(f"Trend Filter: Fixed Long SMA Window={trend_sma_window}")

    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: return None, None, None

    # --- Define Parameter Grid (RSI + BB - Wider) ---
    if param_grid is None:
        param_grid = {
            'rsi_window': np.arange(10, 25, 4),      # [10, 14, 18, 22]
            'rsi_lower_th': np.arange(15, 40, 5),     # [15, 20, 25, 30, 35] - Wider range
            'rsi_upper_th': np.arange(65, 86, 5),     # [65, 70, 75, 80, 85] - Wider range
            'bb_window': np.arange(15, 31, 5),       # [15, 20, 25, 30]
            'bb_std': np.arange(1.0, 3.6, 0.5)       # [1.0, 1.5, 2.0, 2.5, 3.0, 3.5] - Wider range
        }
    logger.info(f"Optimization Parameter Grid: {param_grid}")
    param_names_ordered = list(param_grid.keys())
    logger.info(f"Parameter Order for Optimization: {param_names_ordered}")

    metric_map = {'sharpe ratio': 'sharpe_ratio', 'total return': 'total_return', 'max drawdown': 'max_drawdown'}
    vbt_metric = metric_map.get(optimize_metric.lower(), 'sharpe_ratio')
    higher_better = vbt_metric not in ['max_drawdown']
    logger.info(f"Using '{vbt_metric}' as optimization metric (higher_better={higher_better}).")

    # --- WFO Split Calculation --- 
    # Note: WFO days/years are now relative to the granularity 
    logger.info("Manually calculating split indices...")
    n_total = len(full_price_data)
    # Calculate window/test lengths in number of periods based on granularity
    periods_per_day = 86400 // granularity
    window_len_periods = int(wfo_window_years * 365.25 * periods_per_day) 
    test_len_periods = int(wfo_test_days * periods_per_day)
    train_len_periods = window_len_periods - test_len_periods
    
    if train_len_periods <= 0 or window_len_periods > n_total:
        logger.error(f"WFO train length ({train_len_periods} periods) invalid or window ({window_len_periods} periods) too large for data ({n_total} periods).")
        return None, None, full_price_data
    
    split_indices = []
    current_start_period = 0
    while current_start_period + window_len_periods <= n_total:
        train_start = current_start_period
        train_end = current_start_period + train_len_periods
        test_start = train_end
        test_end = min(current_start_period + window_len_periods, n_total)
        if test_start >= test_end: break 
        split_indices.append((np.arange(train_start, train_end), np.arange(test_start, test_end)))
        current_start_period += test_len_periods # Step forward by test periods
        
    n_splits = len(split_indices)
    if n_splits == 0: 
        logger.error("Could not generate any WFO splits with the given parameters.")
        return None, None, full_price_data
    logger.info(f"Manual calculation generated {n_splits} splits (Train: {train_len_periods}, Test: {test_len_periods} periods @ {granularity_str}).")

    oos_results_sharpe = {}; oos_results_return = {}; oos_results_drawdown = {}
    best_params_history = {}

    logger.info("Starting Walk-Forward Iteration (Manual Indices)...")
    for i, (train_idx, test_idx) in enumerate(tqdm(split_indices, total=n_splits, desc="WFO Splits")):
        in_price_split = full_price_data.iloc[train_idx]
        out_price_split = full_price_data.iloc[test_idx]
        if in_price_split.empty or out_price_split.empty: continue

        # 1. Optimize on In-Sample Data (No trend window passed)
        in_performance = simulate_all_params_single_split_direct(
            in_price_split, param_grid, 
            initial_capital, commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
            trend_sma_window, # Pass the trend window
            vbt_metric
        )
        if in_performance is None or in_performance.empty:
             logger.warning(f"Split {i}: In-sample simulation returned no performance data.")
             continue

        # 2. Find Best Parameters Index (tuple)
        best_index_split = get_best_index(in_performance, higher_better=higher_better)
        if best_index_split is None:
             logger.warning(f"Split {i}: Could not find best index from in-sample performance.")
             continue

        # 3. Create Best Parameters Dict
        if isinstance(best_index_split, tuple) and len(best_index_split) == len(param_names_ordered):
            best_params_split = dict(zip(param_names_ordered, best_index_split))
        else:
            logger.warning(f"Split {i}: Best index {best_index_split} length mismatch with params {param_names_ordered}. Skipping.")
            continue
        best_params_history[i] = best_params_split

        # 4. Test Best Parameters on Out-of-Sample Data (No trend window passed)
        oos_metrics_dict = simulate_best_params_single_split_direct(
            out_price_split, best_params_split, 
            initial_capital, commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
            trend_sma_window # Pass the trend window
        )
        oos_results_sharpe[i] = oos_metrics_dict.get('sharpe_ratio', np.nan)
        oos_results_return[i] = oos_metrics_dict.get('total_return', np.nan)
        oos_results_drawdown[i] = oos_metrics_dict.get('max_drawdown', np.nan)

    logger.info("Walk-Forward Iteration Complete.")
    if not best_params_history: return None, None, full_price_data

    # --- Aggregate and Prepare Final Results ---
    oos_sharpe_series = pd.Series(oos_results_sharpe).sort_index()
    oos_return_series = pd.Series(oos_results_return).sort_index()
    oos_drawdown_series = pd.Series(oos_results_drawdown).sort_index()
    oos_mean_sharpe = oos_sharpe_series.mean(); oos_std_sharpe = oos_sharpe_series.std()
    oos_mean_return = oos_return_series.mean(); oos_std_return = oos_return_series.std()
    oos_mean_drawdown = oos_drawdown_series.mean(); oos_std_drawdown = oos_drawdown_series.std()

    logger.info("--- Final Aggregated OOS Performance (RSI+BB + Fixed SMA Filter - pandas-ta, Fixed Stops) ---")
    if use_stops:
        logger.info(f"Fixed Stop Params: SL={sl_atr_multiplier}, TSL={tsl_atr_multiplier}")
    else:
        logger.info("Stops Disabled.")
    logger.info(f"Chosen Optimization Metric: {vbt_metric}")
    logger.info(f"Sharpe Ratio  : Mean={oos_mean_sharpe:.4f}, Std={oos_std_sharpe:.4f}")
    logger.info(f"Total Return  : Mean={oos_mean_return:.4f}, Std={oos_std_return:.4f}")
    logger.info(f"Max Drawdown  : Mean={oos_mean_drawdown:.4f}, Std={oos_std_drawdown:.4f}")
    logger.info(f"Trend Filter SMA: {trend_sma_window}")

    wfo_results_dict = {
        'strategy_name': f'RSI + BBands + Fixed SMA{trend_sma_window} Filter (pandas-ta)',
        'trend_sma_window': trend_sma_window,
        'optimized_metric': vbt_metric,
        'stops_enabled': use_stops,
        'fixed_sl_atr_multiplier': sl_atr_multiplier if use_stops else None,
        'fixed_tsl_atr_multiplier': tsl_atr_multiplier if use_stops else None,
        'best_params_per_split': best_params_history,
        'oos_sharpe': oos_sharpe_series.to_dict(),
        'oos_return': oos_return_series.to_dict(),
        'oos_drawdown': oos_drawdown_series.to_dict(),
        'oos_mean_sharpe': oos_mean_sharpe, 'oos_std_sharpe': oos_std_sharpe,
        'oos_mean_return': oos_mean_return, 'oos_std_return': oos_std_return,
        'oos_mean_drawdown': oos_mean_drawdown, 'oos_std_drawdown': oos_std_drawdown,
    }
    return None, wfo_results_dict, full_price_data

# --- WFO Helper Function: Simulate All Parameters (Direct Calculation + pandas-ta) ---
def simulate_all_params_single_split_direct(price_data, param_grid, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier, trend_sma_window, metric='sharpe_ratio', granularity_seconds=3600): # Add granularity_seconds param
    freq_str = get_vbt_freq_str(granularity_seconds) # Get frequency string dynamically
    if not freq_str:
        logger.error(f"Invalid granularity seconds ({granularity_seconds}) for freq string. Cannot simulate.")
        return None
    logger.debug(f"Simulating RSI+BB params (pandas-ta, fixed stops) on single split data shape: {price_data.shape} ({freq_str})")
    close = price_data['close']; high = price_data['high']; low = price_data['low']

    # --- Calculate Stops Once --- 
    sl_stop_pct = None; tsl_stop_pct = None
    local_use_stops = use_stops 
    if local_use_stops:
        try:
            atr = vbt.ATR.run(high, low, close, window=14).atr
            if atr is not None and not atr.isnull().all():
                if sl_atr_multiplier > 0:
                    sl_stop_pct = (atr * sl_atr_multiplier) / close
                    sl_stop_pct = sl_stop_pct.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill')
                if tsl_atr_multiplier > 0:
                    tsl_stop_pct = (atr * tsl_atr_multiplier) / close
                    tsl_stop_pct = tsl_stop_pct.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill')
                if (sl_stop_pct is not None and sl_stop_pct.isnull().all()) or \
                   (tsl_stop_pct is not None and tsl_stop_pct.isnull().all()):
                    logger.warning("Stop loss calculation resulted in all NaNs, disabling stops for split.")
                    local_use_stops = False
                    sl_stop_pct = None
                    tsl_stop_pct = None
            else:
                logger.warning("ATR calculation yielded NaNs or was None, disabling stops for split.")
                local_use_stops = False
        except Exception as atr_err:
            logger.warning(f"Could not calculate ATR for split: {atr_err}, disabling stops for split.");
            local_use_stops = False

    # --- Pre-Calculate ALL Indicator Variations ONCE --- 
    rsi_indicators = {}
    lower_bands_dict = {}
    middle_bands_dict = {}

    try:
        # Calculate RSI for all relevant windows using VBT
        for rsi_w in param_grid['rsi_window']:
             if rsi_w < 2 or rsi_w >= len(close):
                  logger.warning(f"Skipping RSI window {rsi_w} due to insufficient data length {len(close)}.")
                  rsi_indicators[rsi_w] = pd.Series(np.nan, index=close.index)
                  continue
             try:
                  rsi_indicators[rsi_w] = vbt.RSI.run(close, window=rsi_w).rsi
             except Exception as rsi_err:
                  logger.error(f"Error calculating RSI for window={rsi_w}: {rsi_err}")
                  rsi_indicators[rsi_w] = pd.Series(np.nan, index=close.index)
        
        # Manually Calculate and Store Each BBands Variation using pandas-ta
        df_close = close.to_frame() # Need DataFrame for pandas-ta

        for w in param_grid['bb_window']:
             if w < 2 or w >= len(df_close): 
                  logger.warning(f"Skipping BBands window {w} due to insufficient data length {len(df_close)}.")
                  for s in param_grid['bb_std']:
                       lower_bands_dict[(w, s)] = pd.Series(np.nan, index=close.index)
                       middle_bands_dict[(w, s)] = pd.Series(np.nan, index=close.index)
                  continue
             for s in param_grid['bb_std']:
                try:
                    # Use a copy to prevent modifying df_close across iterations
                    temp_df = df_close.copy()
                    # Calculate BBands using pandas_ta
                    temp_df.ta.bbands(length=w, std=s, append=True) 
                    # Find the correct column names (pandas-ta uses float format in col name)
                    col_lower = f'BBL_{w}_{s:.1f}' 
                    col_middle = f'BBM_{w}_{s:.1f}'
                    # Handle potential suffixes like .0 added by pandas-ta
                    actual_col_lower = next((c for c in temp_df.columns if c.startswith(col_lower)), None)
                    actual_col_middle = next((c for c in temp_df.columns if c.startswith(col_middle)), None)
                    
                    if actual_col_lower and actual_col_middle:
                         lower_bands_dict[(w, s)] = temp_df[actual_col_lower]
                         middle_bands_dict[(w, s)] = temp_df[actual_col_middle]
                         # Clean up added columns to prevent buildup 
                         columns_to_drop = [actual_col_lower, actual_col_middle] + \
                                           [c for c in temp_df.columns if c.startswith(f'BBU_{w}_{s:.1f}') or 
                                                                        c.startswith(f'BBB_{w}_{s:.1f}') or 
                                                                        c.startswith(f'BBP_{w}_{s:.1f}')]
                         temp_df.drop(columns=[c for c in columns_to_drop if c in temp_df.columns], inplace=True)
                    else:
                         logger.error(f"Could not find BBands columns for window={w}, std={s:.1f}. Columns: {list(temp_df.columns)}")
                         lower_bands_dict[(w, s)] = pd.Series(np.nan, index=close.index)
                         middle_bands_dict[(w, s)] = pd.Series(np.nan, index=close.index)

                except Exception as bb_err:
                    logger.error(f"Error calculating BBANDS with pandas-ta for window={w}, std={s}: {bb_err}")
                    lower_bands_dict[(w, s)] = pd.Series(np.nan, index=close.index)
                    middle_bands_dict[(w, s)] = pd.Series(np.nan, index=close.index)

        # Check all indicator dictionaries
        if not rsi_indicators or not lower_bands_dict or \
           all(v.isnull().all() for v in rsi_indicators.values()) or \
           all(v.isnull().all() for v in lower_bands_dict.values()): 
             raise ValueError("Core Indicator pre-calculation failed or produced no results.")

        # Calculate Trend Filter SMA ONCE
        trend_filter_active = False
        trend_filter_sma = None
        if trend_sma_window > 0:
            if trend_sma_window < 2 or trend_sma_window >= len(close):
                 logger.warning(f"Trend SMA window {trend_sma_window} invalid for data length {len(close)}. Trend filter disabled for split.")
            else:
                 try:
                     trend_filter_sma = vbt.MA.run(close, window=trend_sma_window).ma
                     trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                 except Exception as sma_err:
                     logger.error(f"Error calculating Trend SMA for window={trend_sma_window}: {sma_err}")

    except Exception as ind_err:
        logger.error(f"Simulate_all_direct: Error during pre-calculation of RSI: {ind_err}", exc_info=True)
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
            rsi_w = current_params['rsi_window']
            rsi_l = current_params['rsi_lower_th']
            rsi_u = current_params['rsi_upper_th']
            bb_w = current_params['bb_window']
            bb_s = current_params['bb_std']
            
            # Select the correct pre-calculated series
            current_rsi = rsi_indicators.get(rsi_w) 
            current_lower_bb = lower_bands_dict.get((bb_w, bb_s))
            current_middle_bb = middle_bands_dict.get((bb_w, bb_s))

            # Skip if any required indicator failed calculation or is unavailable
            if current_rsi is None or current_lower_bb is None or current_middle_bb is None or \
               current_rsi.isnull().all() or current_lower_bb.isnull().all() or current_middle_bb.isnull().all() or \
               (trend_filter_active and (trend_filter_sma is None or trend_filter_sma.isnull().all())):
                 all_entries.append(pd.Series(False, index=close.index))
                 all_exits.append(pd.Series(False, index=close.index))
                 continue
            
            # Generate signals for this combination (RSI + BBands + Fixed SMA Filter)
            entry_conditions = (current_rsi < rsi_l) & (close <= current_lower_bb)
            if trend_filter_active:
                entry_conditions = entry_conditions & (close > trend_filter_sma)
            entries = entry_conditions
            exits = (current_rsi > rsi_u) | (close >= current_middle_bb) # Combined exit

            all_entries.append(entries)
            all_exits.append(exits)
            valid_combinations_count += 1
            
        if valid_combinations_count == 0:
             logger.warning("No valid signals generated across all parameter combinations.")
             return None
             
        # Combine signals into DataFrames with parameter multi-index
        param_multi_index = pd.MultiIndex.from_tuples(all_params_tuples, names=param_names_ordered)
        entries_output = pd.concat(all_entries, axis=1, keys=param_multi_index)
        exits_output = pd.concat(all_exits, axis=1, keys=param_multi_index)

    except Exception as signal_err:
         logger.error(f"Simulate_all_direct: Error during signal generation/combination: {signal_err}", exc_info=True)
         return None
        
    # --- Run Portfolio Simulation ---
    try:
        pf_kwargs = {
            'close': close,
            'entries': entries_output,
            'exits': exits_output,
            'freq': freq_str,
            'init_cash': initial_capital,
            'fees': commission_pct,
            'slippage': slippage_pct,
            'group_by': True # Group results by parameters
        }
        if local_use_stops:
            if sl_stop_pct is not None and sl_stop_pct.notna().any():
                 pf_kwargs['sl_stop'] = sl_stop_pct
            if tsl_stop_pct is not None and tsl_stop_pct.notna().any():
                 pf_kwargs['tsl_stop'] = tsl_stop_pct

        pf = vbt.Portfolio.from_signals(**pf_kwargs)

        # Get the desired performance metric
        perf = getattr(pf, metric, None)

        if perf is None:
            logger.warning(f"Metric '{metric}' not found in portfolio stats for split.")
            return None 
        
        # ---- Start: Handle unexpected scalar output ----
        if isinstance(perf, (int, float, np.number)):
            logger.warning(f"Performance metric '{metric}' was a scalar ({type(perf)}), expected Series. Reconstructing Series.")
            # Reconstruct the expected index
            expected_index = pd.MultiIndex.from_tuples(all_params_tuples, names=param_names_ordered)
            # Create a Series filled with the scalar value
            perf = pd.Series(perf, index=expected_index)
        elif not isinstance(perf, pd.Series):
             logger.warning(f"Performance metric '{metric}' was not a Series or scalar. Type: {type(perf)}")
             return None # Unknown type, cannot proceed
        # ---- End: Handle unexpected scalar output ----
             
        # Ensure the index matches the expected combinations, fill missing with NaN
        expected_index = pd.MultiIndex.from_tuples(all_params_tuples, names=param_names_ordered)
        if not perf.index.equals(expected_index):
            logger.debug("Reindexing performance series to match expected parameter index.")
            perf = perf.reindex(expected_index)

        # Check for all NaNs after potential reindexing or reconstruction
        if perf.isnull().all():
            logger.warning(f"Performance metric '{metric}' contains only NaNs after processing.")
            return None
            
        return perf

    except Exception as pf_err:
        logger.error(f"Simulate_all_direct: Error during portfolio simulation: {pf_err}", exc_info=True)
        return None

# --- WFO Helper Function: Simulate Best Parameters (Direct Calculation + pandas-ta) ---
def simulate_best_params_single_split_direct(price_data, best_params_dict, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier, trend_sma_window, granularity_seconds=3600): # Add granularity_seconds param
    freq_str = get_vbt_freq_str(granularity_seconds) # Get frequency string dynamically
    if not freq_str:
        logger.error(f"Invalid granularity seconds ({granularity_seconds}) for freq string. Cannot simulate best params.")
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}
    logger.debug(f"Simulating best RSI+BB params (pandas-ta, fixed stops) on OOS data shape: {price_data.shape} ({freq_str})")
    close = price_data['close']; high = price_data['high']; low = price_data['low']

    try:
        rsi_window = int(best_params_dict['rsi_window'])
        rsi_lower_th = float(best_params_dict['rsi_lower_th'])
        rsi_upper_th = float(best_params_dict['rsi_upper_th'])
        bb_window = int(best_params_dict['bb_window'])
        bb_std = float(best_params_dict['bb_std'])
    except KeyError as ke:
        logger.error(f"Missing key in best_params_dict: {ke}. Params: {best_params_dict}")
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}

    # --- Calculate Indicators for the specific best parameters --- 
    try:
        # Calculate RSI using VBT
        if rsi_window < 2 or rsi_window >= len(close):
            raise ValueError(f"RSI window {rsi_window} invalid for data length {len(close)}")
        rsi = vbt.RSI.run(close, window=rsi_window).rsi
        
        # Calculate BBands using pandas-ta
        if bb_window < 2 or bb_window >= len(close):
             raise ValueError(f"BBands window {bb_window} invalid for data length {len(close)}")
        df_close = close.to_frame()
        df_close.ta.bbands(length=bb_window, std=bb_std, append=True)
        col_lower = f'BBL_{bb_window}_{bb_std:.1f}'
        col_middle = f'BBM_{bb_window}_{bb_std:.1f}'
        actual_col_lower = next((c for c in df_close.columns if c.startswith(col_lower)), None)
        actual_col_middle = next((c for c in df_close.columns if c.startswith(col_middle)), None)
        if not actual_col_lower or not actual_col_middle:
             raise ValueError(f"Could not find pandas-ta BBands columns for {bb_window}/{bb_std:.1f}")
        lower_bb = df_close[actual_col_lower]
        middle_bb = df_close[actual_col_middle]
        
        # Define rsi_u and rsi_l from the unpacked best_params_dict
        rsi_l = rsi_lower_th 
        rsi_u = rsi_upper_th 

        # Calculate Trend Filter SMA (uses passed trend_sma_window)
        trend_filter_active = False
        trend_filter_sma = None
        if trend_sma_window > 0:
            if trend_sma_window < 2 or trend_sma_window >= len(close):
                 logger.warning(f"Trend SMA window {trend_sma_window} invalid for data length {len(close)}. Trend filter disabled for split.")
            else:
                 try:
                     trend_filter_sma = vbt.MA.run(close, window=trend_sma_window).ma
                     trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                 except Exception as sma_err:
                     logger.error(f"Error calculating Trend SMA for window={trend_sma_window}: {sma_err}")

        # Generate signals (RSI + BBands + SMA Filter)
        entries = (rsi < rsi_l) & (close <= lower_bb)
        if trend_filter_active:
            entries = entries & (close > trend_filter_sma)
        exits = (rsi > rsi_u) | (close >= middle_bb) # Combined exit

        # Check validity after calculation (RSI and BBands only)
        if rsi.isnull().all() or lower_bb.isnull().all() or middle_bb.isnull().all(): 
             raise ValueError("Core indicator calculation resulted in all NaNs")
        
    except Exception as ind_err:
        logger.error(f"Indicator calculation error for best params {best_params_dict}: {ind_err}")
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}

    # --- Calculate Stops ---
    sl_stop_pct = None; tsl_stop_pct = None
    local_use_stops = use_stops
    if local_use_stops:
        try:
             atr = vbt.ATR.run(high, low, close, window=14).atr
             if atr is not None and not atr.isnull().all():
                 if sl_atr_multiplier > 0:
                      sl_stop_pct = (atr * sl_atr_multiplier) / close
                      sl_stop_pct = sl_stop_pct.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill')
                 if tsl_atr_multiplier > 0:
                      tsl_stop_pct = (atr * tsl_atr_multiplier) / close
                      tsl_stop_pct = tsl_stop_pct.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill')
                 # Final check if stops are still valid
                 if (sl_stop_pct is not None and sl_stop_pct.isnull().all()) or \
                    (tsl_stop_pct is not None and tsl_stop_pct.isnull().all()):
                     logger.warning("Stop loss calculation resulted in all NaNs for OOS split.")
                     local_use_stops = False
                     sl_stop_pct = None
                     tsl_stop_pct = None
             else:
                 logger.warning("ATR calculation yielded NaNs or was None for OOS split.")
                 local_use_stops = False
        except Exception as atr_err: logger.warning(f"Could not calc ATR for OOS split: {atr_err}"); local_use_stops = False

    # --- Run Portfolio --- 
    try:
        pf_kwargs = {
            'close': close, 'entries': entries, 'exits': exits,
            'freq': freq_str,
            'init_cash': initial_capital, 'fees': commission_pct, 'slippage': slippage_pct
        }
        if local_use_stops:
             if sl_stop_pct is not None and sl_stop_pct.notna().any():
                 pf_kwargs['sl_stop'] = sl_stop_pct
             if tsl_stop_pct is not None and tsl_stop_pct.notna().any():
                 pf_kwargs['tsl_stop'] = tsl_stop_pct

        pf = vbt.Portfolio.from_signals(**pf_kwargs)
        stats = pf.stats()
        metrics_dict = {
            'sharpe_ratio': stats.get('Sharpe Ratio', np.nan),
            'total_return': stats.get('Total Return [%]', np.nan) / 100.0,
            'max_drawdown': stats.get('Max Drawdown [%]', np.nan) / 100.0
        }
        logger.debug(f"Finished simulate_best_direct (RSI+BB). Metrics: {metrics_dict}")
        return metrics_dict
    except Exception as pf_err:
        logger.error(f"Simulate_best_direct (RSI+BB): Error during portfolio sim: {pf_err}", exc_info=True);
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}

# --- WFO Helper Functions: Get Best Index (No changes needed here) ---
def get_best_index(performance, higher_better=True):
    """Finds index of best performing parameters for a single split's performance Series."""
    if performance is None or performance.empty:
        logger.warning("Get_best_index: Performance data is empty.")
        return None
    try:
        # Handle potential all-NaN series
        if not performance.notna().any():
            logger.warning("Get_best_index: Performance data contains only NaNs.")
            return None

        if higher_better:
            idx = performance.idxmax()
        else:
            idx = performance.idxmin()
        # Ensure it's a tuple (for multi-index) even if only one param exists
        return idx if isinstance(idx, tuple) else (idx,)

    except Exception as e:
        logger.error(f"Error getting best index: {e}")
        return None

# --- Main function ---
def main():
    parser = argparse.ArgumentParser(description='Backtest RSI + Bollinger Bands strategy using VectorBT Pro with Manual WFO (Direct Calc).')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1d', help='Data granularity (e.g., 1d, 4h, 1h)') # Changed default to 1d
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--optimize_metric', type=str, default='Sharpe Ratio', help='Metric to optimize for IS')
    parser.add_argument('--no_stops', action='store_true', help='Disable stop loss usage globally')
    parser.add_argument('--sl_atr', type=float, default=1.5, help='ATR multiplier for stop loss (default: 1.5)') # Adjusted default
    parser.add_argument('--tsl_atr', type=float, default=2.0, help='ATR multiplier for trailing stop loss (default: 2.0)') # Adjusted default
    parser.add_argument('--reports_dir', type=str, default='reports', help='Directory to save reports')
    parser.add_argument('--wfo_test_days', type=int, default=90, help='Days in OOS test set')
    parser.add_argument('--wfo_window_years', type=float, default=2.0, help='Total years in each rolling window')
    parser.add_argument('--trend_sma_window', type=int, default=50, help='Fixed SMA window for trend filter (0 to disable)') # Changed default to 50

    args = parser.parse_args()
    # Updated granularity mapping
    granularity_map = {
        '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
        '1h': 3600, '2h': 7200, '4h': 14400, '6h': 21600, '1d': 86400
    }
    granularity_seconds = granularity_map.get(args.granularity.lower())
    if granularity_seconds is None: 
        logger.error(f"Unsupported granularity: {args.granularity}. Use 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, or 1d.")
        sys.exit(1)
    reports_path = Path(args.reports_dir); reports_path.mkdir(parents=True, exist_ok=True)

    _, wfo_results, full_price_data = run_backtest(
        symbol=args.symbol, start_date=args.start_date, end_date=args.end_date,
        granularity=granularity_seconds, initial_capital=args.initial_capital,
        commission_pct=args.commission, slippage_pct=args.slippage, param_grid=None,
        optimize_metric=args.optimize_metric, use_stops=(not args.no_stops),
        sl_atr_multiplier=args.sl_atr,
        tsl_atr_multiplier=args.tsl_atr,
        trend_sma_window=args.trend_sma_window,
        wfo_test_days=args.wfo_test_days, wfo_window_years=args.wfo_window_years
    )

    if wfo_results:
        logger.info(f"--- Manual WFO ({wfo_results.get('strategy_name', 'RSI + BB + Fixed SMA')}) Results Summary ---")
        logger.info(f"Optimization Metric Used: {wfo_results.get('optimized_metric', 'N/A')}")
        logger.info(f"Stops Enabled: {wfo_results.get('stops_enabled', 'N/A')}")
        if wfo_results.get('stops_enabled'):
             logger.info(f"Fixed Stop Params: SL ATR={wfo_results.get('fixed_sl_atr_multiplier','N/A')}, TSL ATR={wfo_results.get('fixed_tsl_atr_multiplier','N/A')}")
        logger.info(f"OOS Sharpe Ratio: Mean={wfo_results.get('oos_mean_sharpe', np.nan):.4f}, Std={wfo_results.get('oos_std_sharpe', np.nan):.4f}")
        logger.info(f"OOS Total Return: Mean={wfo_results.get('oos_mean_return', np.nan):.4f}, Std={wfo_results.get('oos_std_return', np.nan):.4f}")
        logger.info(f"OOS Max Drawdown: Mean={wfo_results.get('oos_mean_drawdown', np.nan):.4f}, Std={wfo_results.get('oos_std_drawdown', np.nan):.4f}")
        logger.info(f"Trend Filter SMA: {wfo_results.get('trend_sma_window', 'N/A')}")
        try:
            # --- Save WFO Results ---
            stops_suffix = f"_SL{args.sl_atr}_TSL{args.tsl_atr}" if (not args.no_stops) else "_NoStops"
            granularity_suffix = f"_{args.granularity.upper()}" # Add granularity to filename
            save_filename = f"manual_rsi_bb_wfo_results_{args.symbol}{granularity_suffix}{stops_suffix}.json"
            save_path = reports_path / save_filename
            
            # Prepare dict for JSON serialization (handle NaNs and numpy types)
            results_to_save = {}
            for k, v in wfo_results.items():
                if k == 'best_params_per_split':
                     # Convert numpy types within nested dict
                     results_to_save[k] = {str(split_k): {p_name: (int(p_val) if isinstance(p_val, (np.integer, np.int64)) else float(p_val)) for p_name, p_val in params.items()} for split_k, params in v.items()}
                elif isinstance(v, dict):
                    # Convert NaNs to None for other dicts (like oos metrics per split)
                    results_to_save[k] = {str(dict_k): (None if pd.isna(dict_v) else dict_v) for dict_k, dict_v in v.items()}
                elif pd.isna(v):
                    results_to_save[k] = None
                elif isinstance(v, (np.float64, np.int64)):
                    results_to_save[k] = v.item() # Convert numpy number types
                else:
                    results_to_save[k] = v # Keep others as is (str, bool, etc.)

            with open(save_path, 'w') as f: json.dump(results_to_save, f, indent=2)
            logger.info(f"WFO results saved to {save_path}")

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
                           plot_title = f"OOS {plot_metric} per Split (RSI+BB {args.granularity.upper()} {stops_suffix})"
                           fig = plot_series.vbt.plot(title=plot_title)
                           plot_filename = f"manual_rsi_bb_wfo_oos_{plot_metric}{granularity_suffix}{stops_suffix}_{args.symbol}.html"
                           plot_path = reports_path / plot_filename
                           fig.write_html(str(plot_path)); logger.info(f"OOS {plot_metric} plot saved to {plot_path}")
                      else:
                          logger.warning(f"No valid data to plot for OOS metric: {plot_metric_key}")
                 except Exception as plot_err: logger.warning(f"Could not plot OOS {plot_metric}: {plot_err}", exc_info=True)
            else:
                 logger.warning(f"OOS metric data key '{plot_metric_key}' not found or empty in results.")

        except Exception as save_err: logger.error(f"Error saving/plotting WFO results: {save_err}", exc_info=True)
    else: 
        logger.warning("Manual WFO (RSI + BB + Fixed SMA - Direct Calc) did not produce results.")

    logger.info("--- Backtest Script Finished ---")

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    warnings.simplefilter(action='ignore', category=UserWarning) # VBT often throws UserWarnings
    main() 