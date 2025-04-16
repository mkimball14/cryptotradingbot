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


# --- Strategy Definition (Replaces Factory and run_backtest) ---
class RsiBbStrategy:
    def __init__(self, 
                 initial_capital=10000, 
                 commission_pct=0.001, 
                 slippage_pct=0.0005,
                 use_stops=True, 
                 sl_atr_multiplier=1.5, 
                 tsl_atr_multiplier=2.0, 
                 trend_sma_window=50,
                 **kwargs): # Absorb unused params
        """Initialize strategy with fixed parameters."""
        self.initial_capital = initial_capital
        self.commission_pct = commission_pct
        self.slippage_pct = slippage_pct
        self.use_stops = use_stops
        self.sl_atr_multiplier = sl_atr_multiplier
        self.tsl_atr_multiplier = tsl_atr_multiplier
        self.trend_sma_window = trend_sma_window # Added trend filter param
        logger.info(f"Initialized RsiBbStrategy: Trend={self.trend_sma_window}, Stops={self.use_stops}, SL={self.sl_atr_multiplier}, TSL={self.tsl_atr_multiplier}")

    def optimize(self, data: pd.DataFrame, param_grid: Dict, optimize_metric: str, granularity_seconds: int = 86400):
        """
        Run vectorized backtest optimization for RSI + Bollinger Bands.
        (Manual parameter iteration approach, uses pandas-ta for BBands)
        """
        freq_str = get_vbt_freq_str(granularity_seconds)
        if not freq_str:
            logger.error(f"Invalid granularity seconds ({granularity_seconds}). Cannot optimize RSI+BB.")
            return None

        close = data['close']
        high = data['high']
        low = data['low']

        logger.info(f"Running RSI+BB optimization with grid (manual iteration): {param_grid}")

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

            if self.trend_sma_window > 0:
                if self.trend_sma_window < 2 or self.trend_sma_window >= len(close):
                    logger.warning(f"Trend SMA window {self.trend_sma_window} invalid. Filter disabled.")
                else:
                    try:
                        trend_filter_sma = vbt.MA.run(close, window=self.trend_sma_window).ma
                        trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                    except Exception as sma_err:
                        logger.error(f"Trend SMA calculation error: {sma_err}")
                        trend_filter_active = False

            # --- 2. Generate Parameter Combinations ---
            required_keys = ['rsi_window', 'rsi_lower_th', 'rsi_upper_th', 'bb_window', 'bb_std']
            if not all(key in param_grid for key in required_keys):
                logger.error(f"Missing required keys in param_grid for RSI+BB: {required_keys}")
                return None
            param_names = required_keys
            param_arrays = [param_grid[key] for key in param_names]
            param_combinations = list(product(*param_arrays))
            logger.info(f"Generated {len(param_combinations)} RSI+BB parameter combinations.")

            all_entries = []
            all_exits = []

            # --- 3. Loop Through Combinations and Generate Signals ---
            df_close = close.to_frame() # Need DataFrame for pandas-ta
            for rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std in tqdm(param_combinations, desc="Simulating RSI+BB"):
                try:
                    # Calculate RSI (VBT)
                    if rsi_window < 2 or rsi_window >= len(close):
                        raise ValueError("Invalid RSI window")
                    current_rsi = vbt.RSI.run(close, window=int(rsi_window)).rsi

                    # --- Use vectorbt BBands instead of pandas-ta ---
                    if bb_window < 2 or bb_window >= len(close):
                        raise ValueError("Invalid BBands window")
                    bbands = vbt.BBANDS.run(close, window=int(bb_window), alpha=float(bb_std)) # Use vbt BBands
                    current_lower_bb = bbands.lower # Get lower band directly
                    current_middle_bb = bbands.middle # Get middle band directly
                    # -------------------------------------------------

                    if current_rsi.isnull().all() or current_lower_bb.isnull().all() or current_middle_bb.isnull().all():
                        raise ValueError("Indicator calculation resulted in all NaNs")

                    # --- Restore Original Signals --- 
                    entry_signal = (current_rsi < rsi_lower_th) & (close <= current_lower_bb)
                    # entry_signal = (current_rsi < rsi_lower_th) # Only use RSI condition (Commented out)
                    # --- DEBUG: Log initial entry signal count ---
                    initial_entry_count = entry_signal.sum()
                    logger.debug(f"    Params ({rsi_window},{rsi_lower_th},{rsi_upper_th},{bb_window},{bb_std}): Initial Entries = {initial_entry_count}")
                    # --------------------------------------------
                    
                    # --- Restore Trend Filter --- 
                    if trend_filter_active:
                        valid_trend_idx = trend_filter_sma.dropna().index
                        temp_entry = entry_signal.copy(); temp_entry.loc[:] = False
                        common_idx = valid_trend_idx.intersection(entry_signal.index)
                        if not common_idx.empty:
                            trend_condition = (close.loc[common_idx] > trend_filter_sma.loc[common_idx])
                            temp_entry.loc[common_idx] = entry_signal.loc[common_idx] & trend_condition
                        entry_signal = temp_entry
                        # --- DEBUG: Log entry signal count after trend filter ---
                        filtered_entry_count = entry_signal.sum()
                        logger.debug(f"    Params ({rsi_window},{rsi_lower_th},{rsi_upper_th},{bb_window},{bb_std}): Filtered Entries = {filtered_entry_count}")
                        # ------------------------------------------------------
                        
                    # --- Restore Original Exit Signal --- 
                    exit_signal = (current_rsi > rsi_upper_th) | (close >= current_middle_bb)
                    # exit_signal = (current_rsi > rsi_upper_th) # Only use RSI condition (Commented out)
                    # --- DEBUG: Log exit signal count ---
                    exit_count = exit_signal.sum()
                    logger.debug(f"    Params ({rsi_window},{rsi_lower_th},{rsi_upper_th},{bb_window},{bb_std}): Exits = {exit_count}")
                    # --- DEBUG: Check for overlapping signals --- 
                    if initial_entry_count > 0 and exit_count > 0: # Only check if both signals exist
                        entry_times = entry_signal[entry_signal].index
                        exit_times = exit_signal[exit_signal].index
                        overlap = entry_times.intersection(exit_times)
                        if not overlap.empty:
                            logger.debug(f"    Params ({rsi_window},{rsi_lower_th},{rsi_upper_th},{bb_window},{bb_std}): Overlapping entry/exit signals detected at: {overlap.tolist()}")
                        # Log first few entry/exit times for inspection
                        if len(entry_times) > 0:
                            logger.debug(f"      First 5 Entry Times: {entry_times[:5].tolist()}")
                        if len(exit_times) > 0:
                            logger.debug(f"      First 5 Exit Times: {exit_times[:5].tolist()}")
                    # -----------------------------------------

                    all_entries.append(entry_signal)
                    all_exits.append(exit_signal)

                except Exception as loop_err:
                    logger.warning(f"Error in loop for RSI+BB params ({rsi_window},{rsi_lower_th},{rsi_upper_th},{bb_window},{bb_std}): {loop_err}. Appending False signals.")
                    all_entries.append(pd.Series(False, index=close.index))
                    all_exits.append(pd.Series(False, index=close.index))
            
            if not all_entries:
                logger.error("No signals generated for any parameter combination.")
                return None
             
            # --- 4. Combine Signals ---
            param_multi_index = pd.MultiIndex.from_tuples(param_combinations, names=param_names)
            entries_output = pd.concat(all_entries, axis=1, keys=param_multi_index)
            exits_output = pd.concat(all_exits, axis=1, keys=param_multi_index)
            # --- DEBUG: Log final signal shapes and counts ---
            logger.debug(f"  Final entries_output shape: {entries_output.shape}, total entries: {entries_output.values.sum()}")
            logger.debug(f"  Final exits_output shape: {exits_output.shape}, total exits: {exits_output.values.sum()}")
            # -----------------------------------------------

            # --- Ensure Correct Dtypes before passing to Portfolio ---
            try:
                # Ensure index is DatetimeIndex
                if not isinstance(close.index, pd.DatetimeIndex):
                    close.index = pd.to_datetime(close.index)
                if not isinstance(entries_output.index, pd.DatetimeIndex):
                     entries_output.index = pd.to_datetime(entries_output.index)
                     exits_output.index = pd.to_datetime(exits_output.index)
                
                # Ensure close is float64
                close = close.astype(np.float64)
                # Ensure entries/exits are boolean
                entries_output = entries_output.astype(bool)
                exits_output = exits_output.astype(bool)
                logger.debug(" Ensured standard dtypes for close, entries, exits.")
            except Exception as dtype_err:
                logger.error(f"Error ensuring dtypes: {dtype_err}")
                return None # Cannot proceed if dtypes are wrong
            # --------------------------------------------------------
            
            # --- 5. Run Portfolio Simulation --- 
            pf_kwargs = {
                'close': close,
                'entries': entries_output,
                'exits': exits_output,
                'freq': freq_str,
                'init_cash': self.initial_capital,
                'fees': self.commission_pct,
                'slippage': self.slippage_pct,
                'call_seq': 'entries_first', # Explicitly set call sequence
            }

            # Temporarily disable stops for debugging RsiBB zero trades
            # if local_use_stops:
            #     if sl_stop_pct is not None and sl_stop_pct.notna().any():
            #         pf_kwargs['sl_stop'] = sl_stop_pct
            #     if tsl_stop_pct is not None and tsl_stop_pct.notna().any():
            #         pf_kwargs['tsl_stop'] = tsl_stop_pct
            logger.warning("Temporarily disabled stops for RsiBB optimization debugging.") # Add warning

            # --- DEBUG: Log Portfolio Kwargs ---
            logger.debug(f"  Portfolio kwargs: { {k: type(v) if isinstance(v, (pd.Series, pd.DataFrame)) else v for k, v in pf_kwargs.items()} }")
            # ----------------------------------
            logger.info(f"Running Portfolio.from_signals with {entries_output.shape[1]} parameter combinations.")
            pf = vbt.Portfolio.from_signals(**pf_kwargs)
            logger.info("Portfolio simulation complete.")

            return pf

        except Exception as e:
            logger.error(f"Error during RSI+BB optimization: {e}", exc_info=True)
            return None


# --- WFO Signal Generation Function ---
def generate_rsi_bb_signals(close, high, low, rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std, trend_sma_window):
    """ 
    Generates entry/exit signals for one parameter combination. 
    Needed for Portfolio.from_signals_wfo.
    Uses pandas-ta for BBands.
    """
    try:
        # Calculate RSI (VBT)
        if rsi_window < 2 or rsi_window >= len(close):
             raise ValueError("Invalid RSI window")
        current_rsi = vbt.RSI.run(close, window=int(rsi_window)).rsi
        
        # Calculate BBands (pandas-ta)
        if bb_window < 2 or bb_window >= len(close):
             raise ValueError("Invalid BBands window")
        df_close = close.to_frame()
        df_close.ta.bbands(length=int(bb_window), std=float(bb_std), append=True)
        col_lower = f'BBL_{int(bb_window)}_{float(bb_std):.1f}'
        col_middle = f'BBM_{int(bb_window)}_{float(bb_std):.1f}'
        actual_col_lower = next((c for c in df_close.columns if c.startswith(col_lower)), None)
        actual_col_middle = next((c for c in df_close.columns if c.startswith(col_middle)), None)
        if not actual_col_lower or not actual_col_middle:
            raise ValueError(f"Could not find BBands columns for {bb_window}/{bb_std:.1f}")
        current_lower_bb = df_close[actual_col_lower]
        current_middle_bb = df_close[actual_col_middle]

        if current_rsi.isnull().all() or current_lower_bb.isnull().all() or current_middle_bb.isnull().all():
            raise ValueError("Indicator calculation resulted in all NaNs")
        
        # Calculate Trend Filter SMA
        trend_filter_active = False
        trend_filter_sma = None
        if trend_sma_window > 0:
            if trend_sma_window < 2 or trend_sma_window >= len(close):
                 logger.warning(f"Trend SMA window {trend_sma_window} invalid. Disabling filter for this combo.")
            else:
                 try:
                     trend_filter_sma = vbt.MA.run(close, window=trend_sma_window).ma
                     trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                 except Exception:
                     trend_filter_active = False # Disable if error

        # Generate signals (RSI + BBands + Trend Filter)
        entry_signal = (current_rsi < rsi_lower_th) & (close <= current_lower_bb)
        if trend_filter_active:
            valid_trend_idx = trend_filter_sma.dropna().index
            temp_entry = entry_signal.copy(); temp_entry.loc[:] = False
            common_idx = valid_trend_idx.intersection(entry_signal.index)
            if not common_idx.empty:
                 trend_condition = (close.loc[common_idx] > trend_filter_sma.loc[common_idx])
                 temp_entry.loc[common_idx] = entry_signal.loc[common_idx] & trend_condition
            entry_signal = temp_entry
            
        exit_signal = (current_rsi > rsi_upper_th) | (close >= current_middle_bb)

        return entry_signal, exit_signal

    except Exception as e:
         # Return False signals if any error occurs for this param set
         logger.warning(f"Error generating signals for {rsi_window},{rsi_lower_th},{rsi_upper_th},{bb_window},{bb_std}: {e}")
         return pd.Series(False, index=close.index), pd.Series(False, index=close.index)


# --- Main WFO Execution Function ---
def run_rsi_bb_wfo(
    symbol, start_date, end_date, granularity=14400, # Default to 4h
    initial_capital=10000, commission_pct=0.001, slippage_pct=0.0005,
    use_stops=True, sl_atr_multiplier=1.5, tsl_atr_multiplier=2.0,
    trend_sma_window=50,
    wfo_test_days=90, wfo_window_years=1.5, # Adjusted WFO window
    optimize_metric='Sharpe Ratio', 
    reports_dir="reports"
    ):
    """Performs Walk-Forward Optimization using vectorbtpro."""
    
    granularity_str = get_granularity_str(granularity) or f"{granularity}s"
    vbt_freq_str = get_vbt_freq_str(granularity) # For portfolio freq
    if not vbt_freq_str:
         logger.error(f"Cannot map granularity {granularity}s to vbt freq string.")
         return None
         
    logger.info(f"--- Running VBT WFO (RSI+BB + Fixed SMA{trend_sma_window}) for {symbol} ({granularity_str}) ---")
    # ... (log other parameters) ...

    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: 
         logger.error("Failed to fetch price data.")
         return None
         
    close = full_price_data['close']
    high = full_price_data['high']
    low = full_price_data['low']
    
    # --- Define Refined Parameter Grid for In-Sample Optimization ---
    # Centered around 4h/6h best params: rsi_window=14, rsi_lower_th=25, rsi_upper_th=80, bb_window=15, bb_std=2.5
    param_grid = {
        'rsi_window': np.arange(12, 17, 2),      # [12, 14, 16]
        'rsi_lower_th': np.arange(20, 31, 5),     # [20, 25, 30]
        'rsi_upper_th': np.arange(75, 86, 5),     # [75, 80, 85]
        'bb_window': np.arange(10, 21, 5),       # [10, 15, 20]
        'bb_std': np.arange(2.0, 3.1, 0.5),      # [2.0, 2.5, 3.0]
    }
    logger.info(f"Refined In-Sample Optimization Grid: {param_grid}")
    # Fixed trend window for this strategy version
    fixed_params = {'trend_sma_window': trend_sma_window}
    param_names = list(param_grid.keys()) + list(fixed_params.keys())
    
    # --- Define WFO Splits --- 
    periods_per_day = 86400 // granularity
    window_len_periods = int(wfo_window_years * 365.25 * periods_per_day)
    test_len_periods = int(wfo_test_days * periods_per_day)
    train_len_periods = window_len_periods - test_len_periods
    n_splits = vbt.rolling_split(close, window_len=window_len_periods, set_lens=(train_len_periods, test_len_periods), left_to_right=True)
    logger.info(f"WFO Setup: {n_splits} splits | Train={train_len_periods}, Test={test_len_periods} periods @ {granularity_str}")
    if n_splits == 0:
        logger.error("Could not generate WFO splits with current settings.")
        return None

    # --- Calculate Stops Once (if used) --- 
    sl_stop = None; tsl_stop = None
    if use_stops:
        try:
             atr = vbt.ATR.run(high, low, close, window=14).atr
             if atr is not None and not atr.isnull().all():
                 if sl_atr_multiplier > 0:
                      sl_stop = (atr * sl_atr_multiplier) / close
                      sl_stop = sl_stop.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                 if tsl_atr_multiplier > 0:
                      tsl_stop = (atr * tsl_atr_multiplier) / close
                      tsl_stop = tsl_stop.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                 if (sl_stop is not None and sl_stop.isnull().all()) or \
                    (tsl_stop is not None and tsl_stop.isnull().all()):
                     logger.warning("Stop calculation resulted in all NaNs, disabling stops.")
                     sl_stop = None; tsl_stop = None; use_stops = False
             else:
                 logger.warning("ATR calculation failed, disabling stops.")
                 sl_stop = None; tsl_stop = None; use_stops = False
        except Exception as atr_err: 
             logger.warning(f"ATR error: {atr_err}, disabling stops."); 
             sl_stop = None; tsl_stop = None; use_stops = False
    
    # --- Run WFO --- 
    try:
        wfo_portfolio = vbt.Portfolio.from_signals_wfo(
            close, 
            generate_rsi_bb_signals, # Function to generate signals
            param_grid, 
            *fixed_params.values(), # Pass fixed params as positional args after param_grid
            param_product=True,
            pre_segment_kwargs=dict(obj=close, arg_names=['close']), # Pass close to signal func per segment
            pre_group_kwargs=dict(group_by=vbt.ArrayWrapper.from_obj(close).grouper.group_names), # Ensure grouping if needed
            split_kwargs=dict(n=n_splits, window_len=window_len_periods, set_lens=(train_len_periods, test_len_periods), left_to_right=True),
            opt_metric=optimize_metric, # Metric for IS optimization
            freq=vbt_freq_str,
            init_cash=initial_capital,
            fees=commission_pct,
            slippage=slippage_pct,
            sl_stop=sl_stop,
            tsl_stop=tsl_stop,
            use_sl_stop=use_stops, # Whether to apply SL based on calculation success
            use_tsl_stop=use_stops, # Whether to apply TSL based on calculation success
        )
        
        logger.info("WFO Simulation Complete.")
        
        # --- Report and Save --- 
        reports_path = Path(reports_dir)
        reports_path.mkdir(parents=True, exist_ok=True)
        
        wfo_stats = wfo_portfolio.stats()
        print("\n--- WFO Out-of-Sample Performance Summary ---")
        print(wfo_stats)
        
        # Save summary stats
        stops_suffix = f"_SL{sl_atr_multiplier}_TSL{tsl_atr_multiplier}" if use_stops else "_NoStops"
        trend_suffix = f"_SMA{trend_sma_window}" if trend_sma_window > 0 else "_NoTrend"
        wfo_stats_filename = f"wfo_rsi_bb_stats_{symbol.replace('-','')}_{granularity_str}{stops_suffix}{trend_suffix}.txt"
        with open(reports_path / wfo_stats_filename, 'w') as f:
             f.write(str(wfo_stats))
        logger.info(f"Saved WFO stats to {reports_path / wfo_stats_filename}")
        
        # Save plot
        try:
             fig = wfo_portfolio.plot()
             plot_filename = f"wfo_rsi_bb_plot_{symbol.replace('-','')}_{granularity_str}{stops_suffix}{trend_suffix}.html"
             fig.write_html(reports_path / plot_filename)
             logger.info(f"Saved WFO plot to {reports_path / plot_filename}")
        except Exception as plot_err:
             logger.warning(f"Could not generate WFO plot: {plot_err}")
             
        return wfo_portfolio # Return the WFO portfolio object

    except Exception as e:
        logger.error(f"Error during WFO execution: {e}", exc_info=True)
        return None


# --- Main function (Updated to call WFO) ---
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

    strategy = RsiBbStrategy(
        initial_capital=args.initial_capital,
        commission_pct=args.commission,
        slippage_pct=args.slippage,
        use_stops=(not args.no_stops),
        sl_atr_multiplier=args.sl_atr,
        tsl_atr_multiplier=args.tsl_atr,
        trend_sma_window=args.trend_sma_window
    )

    param_grid = {
        'rsi_window': np.arange(10, 25, 4),      # [10, 14, 18, 22]
        'rsi_lower_th': np.arange(15, 40, 5),     # [15, 20, 25, 30, 35] - Wider range
        'rsi_upper_th': np.arange(65, 86, 5),     # [65, 70, 75, 80, 85] - Wider range
        'bb_window': np.arange(15, 31, 5),       # [15, 20, 25, 30]
        'bb_std': np.arange(1.0, 3.6, 0.5)       # [1.0, 1.5, 2.0, 2.5, 3.0, 3.5] - Wider range
    }
    logger.info(f"Optimization Parameter Grid: {param_grid}")

    optimized_portfolio = strategy.optimize(fetch_historical_data(args.symbol, args.start_date, args.end_date, granularity_seconds), param_grid, args.optimize_metric, granularity_seconds)

    if optimized_portfolio:
        logger.info("--- RSI+BB Optimization Results ---")
        logger.info(f"Optimized Portfolio: {optimized_portfolio}")
        logger.info(f"Optimized Metric: {args.optimize_metric}")

        # Calculate risk metrics
        metrics = calculate_risk_metrics(optimized_portfolio)
        logger.info(f"Calculated Risk Metrics: {metrics}")

        # Save results
        try:
            # --- Save Optimization Results ---
            save_filename = f"rsi_bb_optimization_results_{args.symbol}_{args.granularity}_{'NoStops' if args.no_stops else 'Stops'}_SL{args.sl_atr}_TSL{args.tsl_atr}.json"
            save_path = reports_path / save_filename
            
            # Prepare dict for JSON serialization (handle NaNs and numpy types)
            results_to_save = {
                'optimized_portfolio': optimized_portfolio.to_dict(),
                'optimized_metric': args.optimize_metric,
                'stops_enabled': not args.no_stops,
                'fixed_sl_atr_multiplier': args.sl_atr if not args.no_stops else None,
                'fixed_tsl_atr_multiplier': args.tsl_atr if not args.no_stops else None,
                'trend_sma_window': args.trend_sma_window,
                'risk_metrics': metrics
            }

            with open(save_path, 'w') as f: json.dump(results_to_save, f, indent=2)
            logger.info(f"Optimization results saved to {save_path}")

            # --- Plot Portfolio Performance ---
            fig = optimized_portfolio.vbt.plot(title="Optimized Portfolio Performance")
            plot_filename = f"rsi_bb_optimization_portfolio_performance_{args.symbol}_{args.granularity}_{'NoStops' if args.no_stops else 'Stops'}_SL{args.sl_atr}_TSL{args.tsl_atr}.html"
            plot_path = reports_path / plot_filename
            fig.write_html(str(plot_path)); logger.info(f"Portfolio performance plot saved to {plot_path}")

        except Exception as save_err: logger.error(f"Error saving optimization results: {save_err}", exc_info=True)
    else: 
        logger.warning("RSI+BB optimization did not produce a valid portfolio.")

    logger.info("--- Backtest Script Finished ---")

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    warnings.simplefilter(action='ignore', category=UserWarning) # VBT often throws UserWarnings
    main() 