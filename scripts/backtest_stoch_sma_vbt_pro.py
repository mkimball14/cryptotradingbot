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
import talib
# Removed pandas_ta import

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
        # Use basic logger if setup failed before logger is configured
        logging.warning(f"Could not load Settings: {settings_err}. Some features might be limited.") 
        settings = None
except ImportError as e:
    # Use basic logger if setup failed before logger is configured
    logging.warning(f"Could not import coinbase.rest.RESTClient or Settings: {e}. Ensure paths/dependencies.")
    # Define placeholders if import fails
    class RESTClient:
        def __init__(self, *args, **kwargs):
            logging.warning("Using placeholder RESTClient.")
        def get_public_candles(self, *args, **kwargs):
            logging.warning("Placeholder RESTClient cannot fetch data.")
            return None
    settings = None # Indicate settings failed to load

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Utility Functions (Copied from backtest_rsi_bb_vbt_pro.py) ---

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
        return df

    except Exception as e:
        logger.error(f"General error fetching data via RESTClient: {e}")
        logger.debug(traceback.format_exc())
        logger.info("Generating sample data due to error.")
        return create_sample_data(start_date, end_date)

def get_granularity_str(granularity_seconds: int) -> Optional[str]:
    gran_map = {
        60: "ONE_MINUTE", 300: "FIVE_MINUTES", 900: "FIFTEEN_MINUTES",
        1800: "THIRTY_MINUTES", 3600: "ONE_HOUR", 7200: "TWO_HOURS",
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
    data['open'] = data['close'].shift(1).fillna(method='bfill')
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
    metrics = {
        'total_return': 0, 'sharpe': 0, 'max_dd': 0, 'win_rate': 0,
        'trades': 0, 'annual_return': 0, 'sortino': 0, 'profit_factor': 0,
        'recovery_factor': 0
    }
    if portfolio is None:
        return metrics
    try:
        stats = portfolio.stats()
        metrics['total_return'] = stats.get('Total Return [%]', 0) / 100
        metrics['sharpe'] = stats.get('Sharpe Ratio', 0)
        metrics['max_dd'] = stats.get('Max Drawdown [%]', 0) / 100
        metrics['trades'] = stats.get('Total Trades', 0)
        metrics['win_rate'] = stats.get('Win Rate [%]', 0) / 100
        metrics['profit_factor'] = stats.get('Profit Factor', 0)
        if metrics['max_dd'] > 0:
            metrics['recovery_factor'] = metrics['total_return'] / metrics['max_dd']
        else:
             metrics['recovery_factor'] = float('inf') if metrics['total_return'] > 0 else 0
        start_date = portfolio.wrapper.index[0]
        end_date = portfolio.wrapper.index[-1]
        years = (end_date - start_date).days / 365.25
        if years > 0:
             metrics['annual_return'] = (1 + metrics['total_return'])**(1/years) - 1
        else:
             metrics['annual_return'] = 0
        metrics['sortino'] = stats.get('Sortino Ratio', 0)
    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}", exc_info=True)
    return metrics

# --- Strategy Definition (No longer using IndicatorFactory) ---
# The logic is embedded in the simulation functions.

# --- Main Execution Logic ---

def run_backtest(
    symbol, start_date, end_date, granularity=86400,
    initial_capital=10000, commission_pct=0.001, slippage_pct=0.0005,
    param_grid=None, optimize_metric='sharpe_ratio',
    use_stops=True, sl_atr_multiplier=1.0, tsl_atr_multiplier=1.0,
    trend_filter_window=200,
    wfo_test_days=180, wfo_window_years=2
):
    """
    Manual WFO: Optimizes Stochastic Oscillator params IS, tests OOS using FIXED stops and FIXED trend filter.
    (Calculates indicators directly).
    """
    granularity_str = get_granularity_str(granularity) or f"{granularity}s" # Get string for logging
    logger.info(f"--- Running Manual WFO (Stochastic + Fixed SMA{trend_filter_window} Filter - Fixed Stops) for {symbol} ({granularity_str}) ---")
    logger.info(f"Period: {start_date} to {end_date} | Granularity: {granularity_str}")
    logger.info(f"Portfolio Settings: IC={initial_capital}, Comm={commission_pct*100:.3f}%, Slip={slippage_pct*100:.3f}% | Stops Enabled={use_stops}")
    if use_stops:
        logger.info(f"Fixed Stop Params: SL ATR Mult={sl_atr_multiplier}, TSL ATR Mult={tsl_atr_multiplier}")
    logger.info(f"Trend Filter: Fixed Long SMA Window={trend_filter_window}")
    logger.info(f"WFO Params: Test Days={wfo_test_days}, Window Years={wfo_window_years}")

    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: return None, None, None

    # --- Define Parameter Grid (Stochastic Only) ---
    if param_grid is None:
        param_grid = {
            # Wider ranges
            'stoch_k': np.arange(5, 26, 5),          # 5, 10, 15, 20, 25
            'stoch_d': np.arange(3, 10, 2),         # 3, 5, 7, 9
            'stoch_smooth_k': np.arange(3, 10, 2),  # 3, 5, 7, 9 
            'stoch_lower_th': np.arange(15, 36, 5),  # 15, 20, 25, 30, 35
            'stoch_upper_th': np.arange(65, 86, 5),  # 65, 70, 75, 80, 85
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

        # 1. Optimize on In-Sample Data (Pass trend window)
        in_performance = simulate_all_params_single_split_direct(
            in_price_split, param_grid, 
            initial_capital, commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
            vbt_metric,
            trend_filter_window=trend_filter_window,
            granularity_seconds=granularity # Pass granularity here
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

        # 4. Test Best Parameters on Out-of-Sample Data (Pass trend window)
        oos_metrics_dict = simulate_best_params_single_split_direct(
            out_price_split, best_params_split, 
            initial_capital, commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
            trend_filter_window=trend_filter_window,
            granularity_seconds=granularity # Pass granularity here
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

    logger.info(f"--- Final Aggregated OOS Performance (Stochastic + Fixed SMA{trend_filter_window} Filter - Fixed Stops) ---")
    if use_stops:
        logger.info(f"Fixed Stop Params: SL={sl_atr_multiplier}, TSL={tsl_atr_multiplier}")
    else:
        logger.info("Stops Disabled.")
    logger.info(f"Chosen Optimization Metric: {vbt_metric}")
    logger.info(f"Sharpe Ratio  : Mean={oos_mean_sharpe:.4f}, Std={oos_std_sharpe:.4f}")
    logger.info(f"Total Return  : Mean={oos_mean_return:.4f}, Std={oos_std_return:.4f}")
    logger.info(f"Max Drawdown  : Mean={oos_mean_drawdown:.4f}, Std={oos_std_drawdown:.4f}")
    logger.info(f"Trend Filter SMA: {trend_filter_window}")

    wfo_results_dict = {
        'strategy_name': f'Stochastic + Fixed SMA{trend_filter_window} Filter',
        'trend_filter_window': trend_filter_window,
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

# --- WFO Helper Function: Simulate All Parameters (Direct Calculation - Stochastic) ---
def simulate_all_params_single_split_direct(price_data, param_grid, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier, metric='sharpe_ratio', trend_filter_window=200, granularity_seconds=86400):
    """ Simulates Stochastic Oscillator param combinations on a SINGLE split using direct indicator calculation (TA-Lib) and fixed trend filter. """
    freq_str = get_vbt_freq_str(granularity_seconds) # Get frequency string dynamically
    if not freq_str:
        logger.error(f"Invalid granularity seconds ({granularity_seconds}) for freq string. Cannot simulate.")
        return None
    logger.debug(f"Simulating Stochastic + SMA{trend_filter_window} params (fixed stops, TA-Lib) on single split data shape: {price_data.shape} ({freq_str})")
    close = price_data['close']; high = price_data['high']; low = price_data['low']

    # --- Calculate Stops Once --- 
    sl_stop_pct = None; tsl_stop_pct = None
    local_use_stops = use_stops 
    if local_use_stops:
        try:
            atr = vbt.ATR.run(high, low, close, window=14).atr # Use a reasonable default ATR window
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
    stoch_k_results = {}
    try:
        # Calculate Trend Filter SMA ONCE first
        trend_filter_active = False
        trend_filter_sma = None
        if trend_filter_window > 0: 
            if trend_filter_window < 1 or trend_filter_window >= len(close):
                 logger.warning(f"Trend SMA window {trend_filter_window} invalid for data length {len(close)}. Trend filter disabled for split.")
            else:
                 try:
                     trend_filter_sma = vbt.MA.run(close, window=trend_filter_window).ma
                     trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                 except Exception as sma_err:
                     logger.error(f"Error calculating Trend SMA for window={trend_filter_window}: {sma_err}")
                     trend_filter_active = False

        # Iterate through Stochastic parameter combinations
        stoch_combinations = list(product(
            param_grid['stoch_k'], 
            param_grid['stoch_d'], 
            param_grid['stoch_smooth_k']))
        
        logger.debug(f"Calculating {len(stoch_combinations)} Stochastic variations using TA-Lib...")
        for k_w, d_w, smk_w in stoch_combinations:
            param_key = (k_w, d_w, smk_w)
            try:
                # Calculate Stochastic using TA-Lib
                # TALIB STOCH inputs: high, low, close, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype
                # Map: k_w -> fastk_period, smk_w -> slowk_period, d_w -> slowd_period
                # We use SMA (matype=0) for both slowk and slowd
                slowk, slowd = talib.STOCH(
                    high.to_numpy(dtype=float), # Ensure numpy float array
                    low.to_numpy(dtype=float),
                    close.to_numpy(dtype=float),
                    fastk_period=k_w,
                    slowk_period=smk_w, 
                    slowk_matype=0, # 0 = SMA
                    slowd_period=d_w,
                    slowd_matype=0  # 0 = SMA
                )
                
                # Convert result back to pandas Series with correct index
                slowk_series = pd.Series(slowk, index=close.index)
                
                if not slowk_series.isnull().all():
                    stoch_k_results[param_key] = slowk_series
                else:
                    logger.warning(f"TA-Lib Stochastic calculation failed or produced all NaNs for params {param_key}")
                    stoch_k_results[param_key] = pd.Series(np.nan, index=close.index)
            except Exception as stoch_err:
                 logger.error(f"Error calculating TA-Lib Stochastic for params {param_key}: {stoch_err}")
                 stoch_k_results[param_key] = pd.Series(np.nan, index=close.index)

        if not stoch_k_results:
             raise ValueError("TA-Lib Stochastic pre-calculation failed for all combinations.")
        elif all(v.isnull().all() for v in stoch_k_results.values()):
             raise ValueError("All calculated TA-Lib Stochastic slowk lines contain only NaNs.")
        elif trend_filter_active and trend_filter_sma is None:
             raise ValueError("Trend filter enabled but SMA calculation failed.")
             
    except Exception as ind_err:
        logger.error(f"Simulate_all_direct: Error during pre-calculation of TA-Lib Stochastic/SMA: {ind_err}", exc_info=True)
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
            stoch_k_w = current_params['stoch_k']
            stoch_d_w = current_params['stoch_d']
            stoch_smk_w = current_params['stoch_smooth_k']
            stoch_l = current_params['stoch_lower_th']
            stoch_u = current_params['stoch_upper_th']

            # Select the correct pre-calculated Stochastic series (using slowk from TA-Lib)
            param_key_stoch = (stoch_k_w, stoch_d_w, stoch_smk_w)
            current_stoch_k = stoch_k_results.get(param_key_stoch)

            # Skip if required indicators failed calculation or are unavailable
            if current_stoch_k is None or current_stoch_k.isnull().all() or \
               (trend_filter_active and (trend_filter_sma is None or trend_filter_sma.isnull().all())):
                 # Log why we are skipping
                 if current_stoch_k is None:
                     logger.warning(f"Skipping params {params_tuple}: Pre-calculated TA-Lib Stochastic slowk not found for key {param_key_stoch}.")
                 elif current_stoch_k.isnull().all():
                     logger.warning(f"Skipping params {params_tuple}: Pre-calculated TA-Lib Stochastic slowk is all NaNs.")
                 elif trend_filter_active and (trend_filter_sma is None or trend_filter_sma.isnull().all()):
                     logger.warning(f"Skipping params {params_tuple}: Trend filter active but SMA is invalid.")
                     
                 all_entries.append(pd.Series(False, index=close.index))
                 all_exits.append(pd.Series(False, index=close.index))
                 continue
            
            # Generate signals for this combination (Stochastic Oversold/Overbought + Trend Filter)
            # Entry: Stochastic slowk crosses above Lower Threshold AND Price is above Trend SMA
            entry_conditions = current_stoch_k.vbt.crossed_above(stoch_l)
            if trend_filter_active:
                entry_conditions = entry_conditions & (close > trend_filter_sma)
            entries = entry_conditions
            
            # Exit: Stochastic slowk crosses below Upper Threshold
            exits = current_stoch_k.vbt.crossed_below(stoch_u)

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
            'freq': freq_str, # Use dynamic freq string
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
        
        # Handle potential scalar output from getattr(pf, metric)
        if isinstance(perf, (int, float, np.number)):
            logger.warning(f"Performance metric '{metric}' was a scalar ({type(perf)}), expected Series. Reconstructing Series.")
            expected_index = pd.MultiIndex.from_tuples(all_params_tuples, names=param_names_ordered) 
            perf = pd.Series(perf, index=expected_index)
        elif not isinstance(perf, pd.Series):
             logger.warning(f"Performance metric '{metric}' was not a Series or scalar. Type: {type(perf)}")
             return None 
             
        # Ensure the index matches the combinations, fill missing with NaN
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

# --- WFO Helper Function: Simulate Best Parameters (Direct Calculation - Stochastic) ---
def simulate_best_params_single_split_direct(price_data, best_params_dict, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier, trend_filter_window=200, granularity_seconds=86400):
    """ Simulates the single best Stochastic param set on a SINGLE split using TA-Lib calculation and fixed trend filter."""
    freq_str = get_vbt_freq_str(granularity_seconds) # Get frequency string dynamically
    if not freq_str:
        logger.error(f"Invalid granularity seconds ({granularity_seconds}) for freq string. Cannot simulate best params.")
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}
    logger.debug(f"Simulating best Stochastic + SMA{trend_filter_window} params (fixed stops, TA-Lib) on OOS data shape: {price_data.shape} ({freq_str})")
    close = price_data['close']; high = price_data['high']; low = price_data['low']

    try:
        stoch_k_w = int(best_params_dict['stoch_k'])
        stoch_d_w = int(best_params_dict['stoch_d'])
        stoch_smk_w = int(best_params_dict['stoch_smooth_k'])
        stoch_l = float(best_params_dict['stoch_lower_th'])
        stoch_u = float(best_params_dict['stoch_upper_th'])
             
    except KeyError as ke:
        logger.error(f"Missing key in best_params_dict: {ke}. Params: {best_params_dict}")
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}

    # --- Calculate Indicators for the specific best parameters using TA-Lib --- 
    try:
        # Calculate TA-Lib Stochastic
        slowk, slowd = talib.STOCH(
            high.to_numpy(dtype=float),
            low.to_numpy(dtype=float),
            close.to_numpy(dtype=float),
            fastk_period=stoch_k_w,
            slowk_period=stoch_smk_w, 
            slowk_matype=0, # SMA
            slowd_period=stoch_d_w,
            slowd_matype=0  # SMA
        )
        # Use slowk for signals
        stoch_k = pd.Series(slowk, index=close.index) 
        
        if stoch_k.isnull().all():
            raise ValueError("TA-Lib Stochastic slowk calculation resulted in all NaNs")

        # Calculate Trend Filter SMA
        trend_filter_active = False
        trend_filter_sma = None
        if trend_filter_window > 0:
            if trend_filter_window < 1 or trend_filter_window >= len(close):
                 logger.warning(f"Trend SMA window {trend_filter_window} invalid for OOS data length {len(close)}. Disabling filter.")
            else:
                 try:
                     trend_filter_sma = vbt.MA.run(close, window=trend_filter_window).ma
                     trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                 except Exception as sma_err:
                     logger.error(f"Error calculating Trend SMA {trend_filter_window} for OOS split: {sma_err}")
                     trend_filter_active = False
        
        # Generate signals
        entry_conditions = stoch_k.vbt.crossed_above(stoch_l)
        if trend_filter_active:
            entry_conditions = entry_conditions & (close > trend_filter_sma)
        entries = entry_conditions
            
        exits = stoch_k.vbt.crossed_below(stoch_u)
        
        # Check validity 
        if stoch_k.isnull().all() or (trend_filter_active and (trend_filter_sma is None or trend_filter_sma.isnull().all())):
            raise ValueError("Indicator calculation resulted in all NaNs or invalid filter")
        
    except Exception as ind_err:
        logger.error(f"Indicator calculation error (TA-Lib) for best params {best_params_dict}: {ind_err}")
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
            'freq': freq_str, # Use dynamic freq string
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
        logger.debug(f"Finished simulate_best_direct (Stochastic + SMA{trend_filter_window}). Metrics: {metrics_dict}")
        return metrics_dict
    except Exception as pf_err:
        logger.error(f"Simulate_best_direct (Stochastic + SMA{trend_filter_window}): Error during portfolio sim: {pf_err}", exc_info=True);
        return {'sharpe_ratio': np.nan, 'total_return': np.nan, 'max_drawdown': np.nan}

# --- WFO Helper Functions: Get Best Index (No changes needed here) ---
def get_best_index(performance, higher_better=True):
    """Finds index of best performing parameters for a single split's performance Series."""
    if performance is None or performance.empty:
        logger.warning("Get_best_index: Performance data is empty.")
        return None
    try:
        if not performance.notna().any():
            logger.warning("Get_best_index: Performance data contains only NaNs.")
            return None
        if higher_better:
            idx = performance.idxmax()
        else:
            idx = performance.idxmin()
        return idx if isinstance(idx, tuple) else (idx,)
    except Exception as e:
        logger.error(f"Error getting best index: {e}")
        return None

# --- Main function --- 
def main():
    parser = argparse.ArgumentParser(description='Backtest Stochastic Oscillator strategy with Fixed SMA Trend Filter using VectorBT Pro with Manual WFO (Direct Calc).')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1d', help='Data granularity (e.g., 1d, 4h, 1h, 15m)')
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--optimize_metric', type=str, default='Sharpe Ratio', help='Metric to optimize for IS')
    parser.add_argument('--no_stops', action='store_true', help='Disable stop loss usage globally')
    parser.add_argument('--sl_atr', type=float, default=2.0, help='ATR multiplier for stop loss (default: 2.0)')
    parser.add_argument('--tsl_atr', type=float, default=2.5, help='ATR multiplier for trailing stop loss (default: 2.5)')
    parser.add_argument('--reports_dir', type=str, default='reports', help='Directory to save reports')
    parser.add_argument('--wfo_test_days', type=int, default=90, help='Days in OOS test set')
    parser.add_argument('--wfo_window_years', type=float, default=2.0, help='Total years in each rolling window')
    parser.add_argument('--trend_filter_window', type=int, default=100, help='Fixed SMA window for trend filter (0 to disable, default: 100)')

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
        trend_filter_window=args.trend_filter_window,
        wfo_test_days=args.wfo_test_days, 
        wfo_window_years=args.wfo_window_years
    )

    if wfo_results:
        logger.info(f"--- Manual WFO ({wfo_results.get('strategy_name', 'Stochastic + SMA Filter')}) Results Summary ---")
        logger.info(f"Optimization Metric Used: {wfo_results.get('optimized_metric', 'N/A')}")
        logger.info(f"Stops Enabled: {wfo_results.get('stops_enabled', 'N/A')}")
        if wfo_results.get('stops_enabled'):
             logger.info(f"Fixed Stop Params: SL ATR={wfo_results.get('fixed_sl_atr_multiplier','N/A')}, TSL ATR={wfo_results.get('fixed_tsl_atr_multiplier','N/A')}")
        logger.info(f"OOS Sharpe Ratio: Mean={wfo_results.get('oos_mean_sharpe', np.nan):.4f}, Std={wfo_results.get('oos_std_sharpe', np.nan):.4f}")
        logger.info(f"OOS Total Return: Mean={wfo_results.get('oos_mean_return', np.nan):.4f}, Std={wfo_results.get('oos_std_return', np.nan):.4f}")
        logger.info(f"OOS Max Drawdown: Mean={wfo_results.get('oos_mean_drawdown', np.nan):.4f}, Std={wfo_results.get('oos_std_drawdown', np.nan):.4f}")
        logger.info(f"Trend Filter SMA: {wfo_results.get('trend_filter_window', 'N/A')}")
        try:
            # --- Save WFO Results ---
            stops_suffix = f"_SL{args.sl_atr}_TSL{args.tsl_atr}" if (not args.no_stops) else "_NoStops"
            trend_suffix = f"_SMA{args.trend_filter_window}" if args.trend_filter_window > 0 else "_NoTrend"
            granularity_suffix = f"_{args.granularity.upper()}" # Add granularity to filename
            save_filename = f"manual_stoch_sma_wfo_results_{args.symbol}{granularity_suffix}{stops_suffix}{trend_suffix}.json"
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
                    results_to_save[k] = v.item() 
                else:
                    results_to_save[k] = v 

            with open(save_path, 'w') as f: json.dump(results_to_save, f, indent=2)
            logger.info(f"WFO results saved to {save_path}")

            # --- Plot OOS Performance Metric --- 
            plot_metric = wfo_results.get('optimized_metric', 'sharpe_ratio')
            metric_key_map = {
                 'sharpe_ratio': 'oos_sharpe',
                 'total_return': 'oos_return',
                 'max_drawdown': 'oos_drawdown'
            }
            plot_metric_key = metric_key_map.get(plot_metric.lower().replace(" ", "_"), 'oos_sharpe')

            if plot_metric_key in wfo_results and wfo_results[plot_metric_key]:
                 try:
                      plot_data_dict = wfo_results[plot_metric_key]
                      plot_series = pd.Series({int(k): v for k, v in plot_data_dict.items() if v is not None}).sort_index()

                      if not plot_series.empty:
                           plot_title = f"OOS {plot_metric} per Split (Stoch + SMA{args.trend_filter_window} {granularity_suffix} {stops_suffix})"
                           fig = plot_series.vbt.plot(title=plot_title)
                           plot_filename = f"manual_stoch_sma_wfo_oos_{plot_metric}{granularity_suffix}{stops_suffix}{trend_suffix}_{args.symbol}.html"
                           plot_path = reports_path / plot_filename
                           fig.write_html(str(plot_path)); logger.info(f"OOS {plot_metric} plot saved to {plot_path}")
                      else:
                          logger.warning(f"No valid data to plot for OOS metric: {plot_metric_key}")
                 except Exception as plot_err: logger.warning(f"Could not plot OOS {plot_metric}: {plot_err}", exc_info=True)
            else:
                 logger.warning(f"OOS metric data key '{plot_metric_key}' not found or empty in results.")

        except Exception as save_err: logger.error(f"Error saving/plotting WFO results: {save_err}", exc_info=True)
    else: logger.warning("Manual WFO (Stochastic + Fixed SMA Filter - Direct Calc) did not produce results.")

    logger.info("--- Backtest Script Finished ---")

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    warnings.simplefilter(action='ignore', category=UserWarning) 
    main() 