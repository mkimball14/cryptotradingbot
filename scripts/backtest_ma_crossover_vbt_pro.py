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

# Helper function to map seconds to vectorbt frequency strings (Needed by optimize method)
def get_vbt_freq_str(granularity_seconds: int) -> Optional[str]:
    # Map seconds to pandas frequency strings suitable for vectorbt
    vbt_freq_map = {
        60: "1T", 300: "5T", 900: "15T", 1800: "30T",
        3600: "1H", 7200: "2H", 14400: "4H", 21600: "6H", 86400: "1D"
    }
    return vbt_freq_map.get(granularity_seconds)

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

# --- Strategy Class Definition (Replaces simulation functions) ---
class MACrossoverStrategy:
    def __init__(self, 
                 initial_capital=10000, 
                 commission_pct=0.001, 
                 slippage_pct=0.0005,
                 use_stops=True, 
                 sl_atr_multiplier=1.5, 
                 tsl_atr_multiplier=2.0,
                 trend_filter_window=200,
                 **kwargs): # Absorb unused params from optimizer
        """Initialize strategy with fixed parameters."""
        self.initial_capital = initial_capital
        self.commission_pct = commission_pct
        self.slippage_pct = slippage_pct
        self.use_stops = use_stops
        self.sl_atr_multiplier = sl_atr_multiplier
        self.tsl_atr_multiplier = tsl_atr_multiplier
        self.trend_filter_window = trend_filter_window
        logger.info(f"Initialized MACrossoverStrategy: Trend={self.trend_filter_window}, Stops={self.use_stops}, SL={self.sl_atr_multiplier}, TSL={self.tsl_atr_multiplier}")

    def optimize(self, data: pd.DataFrame, param_grid: Dict, optimize_metric: str, granularity_seconds: int = 86400):
        """
        Run vectorized backtest optimization for MA Crossover.
        (Manual parameter iteration approach)
        """
        freq_str = get_vbt_freq_str(granularity_seconds) # Assumes get_vbt_freq_str is available
        if not freq_str:
            logger.error(f"Invalid granularity seconds ({granularity_seconds}) for freq string. Cannot optimize MA Crossover.")
            return None

        close = data['close']
        high = data['high']
        low = data['low']

        logger.info(f"Running MA Crossover optimization with grid (manual iteration): {param_grid}")

        # Initialize base indicators
        sl_stop_pct = None
        tsl_stop_pct = None
        local_use_stops = self.use_stops
        trend_filter_active = False
        trend_filter_sma = None
        
        try:
            # --- 1. Calculate Base Indicators (Stops, Trend Filter) ---
            if local_use_stops:
                try:
                    atr = vbt.ATR.run(high, low, close, window=14).atr
                    if atr is not None and not atr.isnull().all():
                        if self.sl_atr_multiplier > 0:
                            sl_stop_pct = (atr * self.sl_atr_multiplier) / close
                            sl_stop_pct = sl_stop_pct.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                        if self.tsl_atr_multiplier > 0:
                            tsl_stop_pct = (atr * self.tsl_atr_multiplier) / close
                            tsl_stop_pct = tsl_stop_pct.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                        if (sl_stop_pct is not None and sl_stop_pct.isnull().all()) or \
                           (tsl_stop_pct is not None and tsl_stop_pct.isnull().all()):
                            local_use_stops = False
                            sl_stop_pct = None
                            tsl_stop_pct = None
                    else:
                        local_use_stops = False
                except Exception as atr_err:
                    logger.warning(f"ATR error: {atr_err}, disabling stops.")
                    local_use_stops = False

            if self.trend_filter_window > 0:
                if self.trend_filter_window < 2 or self.trend_filter_window >= len(close):
                    logger.warning(f"Trend SMA window {self.trend_filter_window} invalid. Filter disabled.")
                else:
                    try:
                        trend_filter_sma = vbt.MA.run(close, window=self.trend_filter_window).ma
                        trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                    except Exception as sma_err:
                        logger.error(f"Trend SMA calculation error: {sma_err}")
                        trend_filter_active = False
            
            # --- 2. Pre-Calculate All Unique MAs Needed --- 
            required_ma_keys = ['short_ma_window', 'long_ma_window']
            if not all(key in param_grid for key in required_ma_keys):
                 logger.error(f"Missing required MA keys in param_grid: {required_ma_keys}")
                 return None
                 
            all_ma_windows = sorted(list(set(param_grid['short_ma_window']) | set(param_grid['long_ma_window'])))
            # Filter out invalid windows
            all_ma_windows = [w for w in all_ma_windows if w >= 2 and w < len(close)]
            if not all_ma_windows:
                 logger.error("No valid MA windows found after length check.")
                 return None

            ma_indicator = vbt.MA.run(close, window=all_ma_windows, short_name='ma')
            if ma_indicator is None or ma_indicator.ma is None:
                 logger.error("Failed to pre-calculate moving averages.")
                 return None
            precalculated_mas = ma_indicator.ma # DataFrame with columns named by window size
            
            # --- 3. Generate Parameter Combinations for MA Crossover ---
            param_names = required_ma_keys # Order matters
            param_arrays = [param_grid[key] for key in param_names]
            param_combinations = list(product(*param_arrays))
            logger.info(f"Generated {len(param_combinations)} MA Crossover parameter combinations.")

            all_entries = []
            all_exits = []
            valid_combinations = [] # Store valid tuples

            # --- 4. Loop Through Combinations and Generate Signals ---
            for short_w, long_w in tqdm(param_combinations, desc="Simulating MA Crossover"):
                # Skip invalid combinations
                if short_w >= long_w or short_w not in precalculated_mas.columns or long_w not in precalculated_mas.columns:
                    continue
                
                valid_combinations.append((short_w, long_w))
                
                try:
                    current_short_ma = precalculated_mas[short_w]
                    current_long_ma = precalculated_mas[long_w]
                    
                    # Generate signals
                    entry_signal = current_short_ma.vbt.crossed_above(current_long_ma)
                    exit_signal = current_short_ma.vbt.crossed_below(current_long_ma)
                    
                    # Apply trend filter
                    if trend_filter_active:
                        valid_trend_idx = trend_filter_sma.dropna().index
                        temp_entry = entry_signal.copy()
                        temp_entry.loc[:] = False
                        common_idx = valid_trend_idx.intersection(entry_signal.index)
                        if not common_idx.empty:
                             trend_condition = (close.loc[common_idx] > trend_filter_sma.loc[common_idx])
                             temp_entry.loc[common_idx] = entry_signal.loc[common_idx] & trend_condition
                        entry_signal = temp_entry

                    all_entries.append(entry_signal)
                    all_exits.append(exit_signal)

                except Exception as loop_err:
                    logger.warning(f"Error in loop for MA params ({short_w},{long_w}): {loop_err}. Appending False signals.")
                    # Need to append False signals with the same length as others for concat
                    all_entries.append(pd.Series(False, index=close.index))
                    all_exits.append(pd.Series(False, index=close.index))

            if not all_entries:
                logger.error("No signals generated for any valid MA Crossover parameter combination.")
                return None
             
            # --- 5. Combine Signals --- 
            param_multi_index = pd.MultiIndex.from_tuples(valid_combinations, names=param_names)
            entries_output = pd.concat(all_entries, axis=1, keys=param_multi_index)
            exits_output = pd.concat(all_exits, axis=1, keys=param_multi_index)

            # --- 6. Run Portfolio Simulation --- 
            pf_kwargs = {
                'close': close,
                'entries': entries_output,
                'exits': exits_output,
                'freq': freq_str,
                'init_cash': self.initial_capital,
                'fees': self.commission_pct,
                'slippage': self.slippage_pct,
            }

            if local_use_stops:
                if sl_stop_pct is not None and sl_stop_pct.notna().any():
                    pf_kwargs['sl_stop'] = sl_stop_pct
                if tsl_stop_pct is not None and tsl_stop_pct.notna().any():
                    pf_kwargs['tsl_stop'] = tsl_stop_pct

            logger.info(f"Running Portfolio.from_signals with {entries_output.shape[1]} parameter combinations.")
            pf = vbt.Portfolio.from_signals(**pf_kwargs)
            logger.info("Portfolio simulation complete.")

            return pf

        except Exception as e:
            logger.error(f"Error during MA Crossover optimization: {e}", exc_info=True)
            return None
            
# --- Removed old simulation functions: ---
# - simulate_all_params_single_split_direct
# - simulate_best_params_single_split_direct
# - run_backtest

# --- WFO Helper Functions: Get Best Index (Keep for potential future WFO use) ---
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
    parser = argparse.ArgumentParser(description='Backtest MA Crossover strategy with Fixed SMA Trend Filter using VectorBT Pro with Manual WFO (Direct Calc).')
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
    parser.add_argument('--trend_filter_window', type=int, default=200, help='Fixed SMA window for trend filter (0 to disable)')

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
        trend_filter_window=args.trend_filter_window,
        wfo_test_days=args.wfo_test_days, 
        wfo_window_years=args.wfo_window_years
    )

    if wfo_results:
        logger.info(f"--- Manual WFO ({wfo_results.get('strategy_name', 'MA Crossover + SMA Filter')}) Results Summary ---")
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
            save_filename = f"manual_ma_crossover_sma_wfo_results_{args.symbol}{stops_suffix}{trend_suffix}.json"
            save_path = reports_path / save_filename
            
            # Prepare dict for JSON serialization (handle NaNs and numpy types)
            results_to_save = {}
            for k, v in wfo_results.items():
                if k == 'best_params_per_split':
                     results_to_save[k] = {str(split_k): {p_name: (int(p_val) if isinstance(p_val, (np.integer, np.int64)) else float(p_val)) for p_name, p_val in params.items()} for split_k, params in v.items()}
                elif isinstance(v, dict):
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
                           plot_title = f"OOS {plot_metric} per Split (MA Crossover + SMA{args.trend_filter_window} {stops_suffix})"
                           fig = plot_series.vbt.plot(title=plot_title)
                           plot_filename = f"manual_ma_crossover_sma_wfo_oos_{plot_metric}{stops_suffix}{trend_suffix}_{args.symbol}.html"
                           plot_path = reports_path / plot_filename
                           fig.write_html(str(plot_path)); logger.info(f"OOS {plot_metric} plot saved to {plot_path}")
                      else:
                          logger.warning(f"No valid data to plot for OOS metric: {plot_metric_key}")
                 except Exception as plot_err: logger.warning(f"Could not plot OOS {plot_metric}: {plot_err}", exc_info=True)
            else:
                 logger.warning(f"OOS metric data key '{plot_metric_key}' not found or empty in results.")

        except Exception as save_err: logger.error(f"Error saving/plotting WFO results: {save_err}", exc_info=True)
    else: logger.warning("Manual WFO (MA Crossover + Fixed SMA Filter - Direct Calc) did not produce results.")

    logger.info("--- Backtest Script Finished ---")

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    warnings.simplefilter(action='ignore', category=UserWarning) 
    main() 