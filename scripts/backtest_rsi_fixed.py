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
        logger = logging.getLogger() # Initialize logger in case it's not initialized yet
        logger.warning(f"Could not load Settings: {settings_err}. Some features might be limited.")
        settings = None
except ImportError as e:
    logger = logging.getLogger() # Initialize logger in case it's not initialized yet
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

# Helper function to map seconds to granularity strings
def get_granularity_str(granularity_seconds: int) -> Optional[str]:
    gran_map = {
        60: "ONE_MINUTE",
        300: "FIVE_MINUTES",
        900: "FIFTEEN_MINUTES",
        1800: "THIRTY_MINUTES",
        3600: "ONE_HOUR",
        7200: "TWO_HOURS",
        21600: "SIX_HOURS",
        86400: "ONE_DAY"
    }
    return gran_map.get(granularity_seconds)

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

    # Create and return sample data for simplicity in this fixed script
    return create_sample_data(start_date, end_date)

# NEW: Combined RSI + Bollinger Bands Function
def rsi_bb_func(close, rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std):
    """ 
    Calculates RSI and Bollinger Bands, generates combined entry/exit signals.
    Entry: RSI crosses below lower threshold AND Close crosses below lower BB.
    Exit: RSI crosses above upper threshold OR Close crosses above middle BB.
    """
    logger.debug(f"Running rsi_bb_func: RSI_W={rsi_window}, L={rsi_lower_th}, U={rsi_upper_th}, BB_W={bb_window}, STD={bb_std}")
    
    # Calculate Indicators
    rsi = vbt.RSI.run(close, window=rsi_window, short_name='RSI').rsi
    bb = vbt.BBANDS.run(close, window=bb_window, alpha=bb_std, short_name='BB') # alpha corresponds to std devs

    # Entry Signal: RSI Oversold AND Price Below Lower Band
    rsi_entry_signal = rsi.vbt.crossed_below(rsi_lower_th)
    bb_entry_signal = close.vbt.crossed_below(bb.lower)
    entries = rsi_entry_signal & bb_entry_signal

    # Exit Signal: RSI Overbought OR Price Above Middle Band
    rsi_exit_signal = rsi.vbt.crossed_above(rsi_upper_th)
    bb_exit_signal = close.vbt.crossed_above(bb.middle) # Exit when price reverts to mean
    exits = rsi_exit_signal | bb_exit_signal
    
    raw_entries_count = entries.sum()
    raw_exits_count = exits.sum()
    logger.debug(f"  RSI ({rsi_window}) + BB ({bb_window}, {bb_std}) Signals: Entries={raw_entries_count}, Exits={raw_exits_count}")

    # Ensure we return boolean Series
    entries = entries.astype(bool)
    exits = exits.astype(bool)
    
    # Return indicators and signals
    return rsi, bb.lower, bb.middle, bb.upper, entries, exits

# Create Indicator Factory for the new strategy
RSIBBStrategyFactory = vbt.IndicatorFactory(
    class_name='RSIBBStrategy',       # Changed class name
    short_name='rsi_bb',              # Changed short name
    input_names=['close'],
    param_names=['rsi_window', 'rsi_lower_th', 'rsi_upper_th', 'bb_window', 'bb_std'], # Added BB params
    output_names=['rsi', 'bb_lower', 'bb_middle', 'bb_upper', 'entries', 'exits']      # Added BB outputs
).with_apply_func(rsi_bb_func) # Use the new combined function

def get_best_index(performance, higher_better=True):
    """Find best index."""
    if performance is None or performance.empty:
        logger.warning("Performance data is empty.")
        return None
    try:
        if not performance.notna().any():
            logger.warning("Performance data contains only NaNs.")
            return None 
            
        if higher_better:
            return performance.idxmax()
        else:
            return performance.idxmin()
    except Exception as e:
        logger.error(f"Error getting best index: {e}")
        return None

def simulate_all_params_single_split(price_data, param_grid, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier, metric='sharpe_ratio', higher_better=True):
    """Simulates RSI+BB param combinations on a SINGLE split, using fixed stop settings."""
    logger.debug(f"Simulating RSI+BB params (fixed stops) on single split data shape: {price_data.shape}")
    close = price_data['close']; high = price_data['high']; low = price_data['low']
    all_entries = []; all_exits = []; all_params = []
    param_names = list(param_grid.keys()); param_values = list(param_grid.values())
    param_combinations = list(product(*param_values)); total_combs = len(param_combinations)
    if total_combs == 0: return None
    
    # ATR calculation
    atr = None
    if use_stops:
        try: 
            atr = vbt.ATR.run(high, low, close, window=14).atr
            logger.debug(f"Split ATR calculated: Mean={atr.mean():.4f}, Max={atr.max():.4f}")
        except Exception: 
            logger.warning(f"Could not calculate ATR for split, disabling stops for this split.")
            use_stops = False
    
    # Calculate ATR-based stops if possible
    sl_stop_pct = None; tsl_stop_pct = None
    if use_stops and atr is not None:
        if sl_atr_multiplier > 0: sl_stop_pct = (atr * sl_atr_multiplier) / close
        if tsl_atr_multiplier > 0: tsl_stop_pct = (atr * tsl_atr_multiplier) / close

    # Loop through RSI parameter combinations
    for params_tuple in param_combinations:
        current_params = dict(zip(param_names, params_tuple))
        all_params.append(current_params)
        # Extract all parameters
        rsi_window = int(current_params['rsi_window'])
        rsi_lower_th = float(current_params['rsi_lower_th'])
        rsi_upper_th = float(current_params['rsi_upper_th'])
        bb_window = int(current_params['bb_window'])
        bb_std = float(current_params['bb_std'])
        try:
            # Call the function with all required params
            rsi, bb_lower, bb_middle, bb_upper, entries, exits = rsi_bb_func(
                close, rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std
            )
            all_entries.append(entries); all_exits.append(exits)
        except Exception: 
            all_entries.append(pd.Series(False, index=close.index))
            all_exits.append(pd.Series(False, index=close.index))

    # Combine signals
    if not all_entries: return None
    param_multi_index = pd.MultiIndex.from_tuples([tuple(p.values()) for p in all_params], names=param_names)
    try:
         entries_output = pd.concat(all_entries, axis=1, keys=param_multi_index)
         exits_output = pd.concat(all_exits, axis=1, keys=param_multi_index)
    except Exception as concat_err:
        logger.error(f"Error combining signals: {concat_err}")
        return None

    # Run Portfolio Simulation
    try:
        # Pass ATR-based stop Series (or None)
        pf = vbt.Portfolio.from_signals(
            close=close, entries=entries_output, exits=exits_output,
            freq='1D', init_cash=initial_capital, fees=commission_pct, slippage=slippage_pct,
            sl_stop=sl_stop_pct,
            tsl_stop=tsl_stop_pct,
            group_by=True
        )
        perf = getattr(pf, metric, None)
        if perf is None: return pd.Series(np.nan, index=param_multi_index)
        if isinstance(perf, (int, float)): perf = pd.Series(perf, index=param_multi_index)
        elif not isinstance(perf, pd.Series): perf = pd.Series(np.nan, index=param_multi_index)
        if not perf.index.equals(param_multi_index): perf = perf.reindex(param_multi_index)
        return perf
    except Exception as pf_err:
        logger.error(f"Error during portfolio sim: {pf_err}")
        return None

def simulate_best_params_single_split(price_data, best_params_dict, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier):
    """Simulates the single best RSI+BB param set on a SINGLE split, using fixed stop settings."""
    logger.debug(f"Simulating best RSI+BB params (fixed stops) on split data shape: {price_data.shape}")
    close = price_data['close']; high = price_data['high']; low = price_data['low']
    
    # Extract parameters from the best_params_dict
    rsi_window = int(best_params_dict['rsi_window'])
    rsi_lower_th = float(best_params_dict['rsi_lower_th'])
    rsi_upper_th = float(best_params_dict['rsi_upper_th'])
    bb_window = int(best_params_dict['bb_window'])
    bb_std = float(best_params_dict['bb_std'])

    try:
        # Call the function with all required params
        rsi, bb_lower, bb_middle, bb_upper, entries, exits = rsi_bb_func(
            close, rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std
        )
    except Exception: 
        entries = pd.Series(False, index=close.index)
        exits = pd.Series(False, index=close.index)
    
    # Re-introduce ATR calculation for the single best run
    sl_stop_pct = None; tsl_stop_pct = None
    if use_stops:
        try:
             atr = vbt.ATR.run(high, low, close, window=14).atr
             if sl_atr_multiplier > 0: sl_stop_pct = (atr * sl_atr_multiplier) / close
             if tsl_atr_multiplier > 0: tsl_stop_pct = (atr * tsl_atr_multiplier) / close
        except Exception:
            logger.warning("Could not calculate ATR, running without stops.")

    pf = vbt.Portfolio.from_signals(
        close, 
        entries, 
        exits, 
        freq='1D', 
        init_cash=initial_capital, 
        fees=commission_pct, 
        slippage=slippage_pct, 
        sl_stop=sl_stop_pct,
        tsl_stop=tsl_stop_pct
    )
    stats = pf.stats()
    metrics_dict = {
        'sharpe_ratio': stats.get('Sharpe Ratio', np.nan),
        'total_return': stats.get('Total Return [%]', np.nan) / 100.0,
        'max_drawdown': stats.get('Max Drawdown [%]', np.nan) / 100.0
    }
    return metrics_dict

def run_backtest(
    symbol, start_date, end_date, granularity=86400,
    initial_capital=10000, commission_pct=0.001, slippage_pct=0.0005,
    param_grid=None, optimize_metric='sharpe_ratio',
    use_stops=True,
    sl_atr_multiplier=1.0, tsl_atr_multiplier=1.0,
    wfo_test_days=180, wfo_window_years=2
):
    """Manual WFO: Optimizes RSI + Bollinger Band params, IS, tests OOS using FIXED stops."""
    logger.info(f"--- Running Manual WFO (Optimizing RSI + BB, Fixed Stops) for {symbol} ---")
    logger.info(f"Period: {start_date} to {end_date} | Granularity: {granularity}s")
    logger.info(f"Portfolio Settings: IC={initial_capital}, Comm={commission_pct*100:.3f}%, Slip={slippage_pct*100:.3f}% | Stops Enabled={use_stops}")
    logger.info(f"Fixed Stop Params: SL ATR Mult={sl_atr_multiplier}, TSL ATR Mult={tsl_atr_multiplier}")
    logger.info(f"WFO Params: Test Days={wfo_test_days}, Window Years={wfo_window_years}")

    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: return None, None, None

    # Define Parameter Grid (RSI and Trend Filter)
    if param_grid is None:
        param_grid = {
            'rsi_window': np.arange(10, 21, 5),  # 10, 15, 20
            'rsi_lower_th': np.arange(25, 41, 5), # 25, 30, 35, 40
            'rsi_upper_th': np.arange(60, 76, 5),  # 60, 65, 70, 75
            'bb_window': np.arange(15, 31, 5),     # 15, 20, 25, 30
            'bb_std': np.arange(1.5, 3.1, 0.5)      # 1.5, 2.0, 2.5, 3.0
        }
    logger.info(f"Optimization Parameter Grid: {param_grid}")
    param_names_ordered = list(param_grid.keys())
    logger.info(f"Parameter Order for Optimization: {param_names_ordered}")

    metric_map = {'sharpe ratio': 'sharpe_ratio', 'total return': 'total_return', 'max drawdown': 'max_drawdown'}
    vbt_metric = metric_map.get(optimize_metric.lower(), 'sharpe_ratio')
    higher_better = vbt_metric not in ['max_drawdown']
    logger.info(f"Using '{vbt_metric}' as optimization metric (higher_better={higher_better}).")

    logger.info("Manually calculating split indices...")
    n_total = len(full_price_data); window_len = int(wfo_window_years * 365.25)
    test_len = wfo_test_days; train_len = window_len - test_len
    if train_len <= 0 or window_len > n_total: return None, None, full_price_data
    split_indices = []
    current_start = 0
    while current_start + window_len <= n_total:
        train_start = current_start; train_end = current_start + train_len
        test_start = train_end; test_end = min(current_start + window_len, n_total)
        if test_start >= test_end: break
        split_indices.append((np.arange(train_start, train_end), np.arange(test_start, test_end)))
        current_start += test_len
    n_splits = len(split_indices)
    if n_splits == 0: return None, None, full_price_data
    logger.info(f"Manual calculation generated {n_splits} splits.")

    oos_results_sharpe = {}; oos_results_return = {}; oos_results_drawdown = {}
    best_params_history = {}

    logger.info("Starting Walk-Forward Iteration (Manual Indices)...")
    for i, (train_idx, test_idx) in enumerate(tqdm(split_indices, total=n_splits, desc="WFO Splits")):
        in_price_split = full_price_data.iloc[train_idx]
        out_price_split = full_price_data.iloc[test_idx]
        if in_price_split.empty or out_price_split.empty: continue

        # 1. Optimize on In-Sample Data
        in_performance = simulate_all_params_single_split(
            in_price_split, param_grid, initial_capital,
            commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
            vbt_metric,
            higher_better=higher_better
        )
        if in_performance is None: continue
        if in_performance.empty: continue

        # 2. Find Best Parameters Index (tuple)
        best_index_split = get_best_index(in_performance, higher_better=higher_better)
        if best_index_split is None: continue

        # 3. Create Best Parameters Dict
        if isinstance(best_index_split, tuple) and len(best_index_split) == len(param_names_ordered):
            best_params_split = dict(zip(param_names_ordered, best_index_split))
        else: 
            logger.warning(f"Split {i}: Best index {best_index_split} is not a tuple or length mismatch with params {param_names_ordered}. Skipping.")
            continue
        best_params_history[i] = best_params_split

        # 4. Test Best Parameters on Out-of-Sample Data
        oos_metrics_dict = simulate_best_params_single_split(
            out_price_split, best_params_split, initial_capital,
            commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
        )
        oos_results_sharpe[i] = oos_metrics_dict.get('sharpe_ratio', np.nan)
        oos_results_return[i] = oos_metrics_dict.get('total_return', np.nan)
        oos_results_drawdown[i] = oos_metrics_dict.get('max_drawdown', np.nan)

    logger.info("Walk-Forward Iteration Complete.")
    if not best_params_history: return None, None, full_price_data
    oos_sharpe_series = pd.Series(oos_results_sharpe).sort_index()
    oos_return_series = pd.Series(oos_results_return).sort_index()
    oos_drawdown_series = pd.Series(oos_results_drawdown).sort_index()
    oos_mean_sharpe = oos_sharpe_series.mean(); oos_std_sharpe = oos_sharpe_series.std()
    oos_mean_return = oos_return_series.mean(); oos_std_return = oos_return_series.std()
    oos_mean_drawdown = oos_drawdown_series.mean(); oos_std_drawdown = oos_drawdown_series.std()
    logger.info("--- Final Aggregated OOS Performance (RSI + BB, Fixed Stops) ---")
    logger.info(f"Fixed Stop Params: SL={sl_atr_multiplier}, TSL={tsl_atr_multiplier}")
    logger.info(f"Chosen Optimization Metric: {vbt_metric}")
    logger.info(f"Sharpe Ratio  : Mean={oos_mean_sharpe:.4f}, Std={oos_std_sharpe:.4f}")
    logger.info(f"Total Return  : Mean={oos_mean_return:.4f}, Std={oos_std_return:.4f}")
    logger.info(f"Max Drawdown  : Mean={oos_mean_drawdown:.4f}, Std={oos_std_drawdown:.4f}")
    wfo_results_dict = {
        'optimized_metric': vbt_metric,
        'fixed_sl_atr_multiplier': sl_atr_multiplier,
        'fixed_tsl_atr_multiplier': tsl_atr_multiplier,
        'best_params_per_split': best_params_history,
        'oos_sharpe': oos_sharpe_series.to_dict(), 'oos_return': oos_return_series.to_dict(), 'oos_drawdown': oos_drawdown_series.to_dict(),
        'oos_mean_sharpe': oos_mean_sharpe, 'oos_std_sharpe': oos_std_sharpe,
        'oos_mean_return': oos_mean_return, 'oos_std_return': oos_std_return,
        'oos_mean_drawdown': oos_mean_drawdown, 'oos_std_drawdown': oos_std_drawdown,
    }
    return None, wfo_results_dict, full_price_data

def main():
    # Set root logger level to DEBUG to capture detailed logs
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(description='Backtest RSI+BB strategy using VectorBT Pro with Manual WFO.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1d', help='Data granularity (1d only supported)')
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--optimize_metric', type=str, default='Sharpe Ratio', help='Metric to optimize for IS')
    parser.add_argument('--no_stops', action='store_true', help='Disable stop loss usage globally')
    parser.add_argument('--sl_atr', type=float, default=3.5, help='ATR multiplier for stop loss')
    parser.add_argument('--tsl_atr', type=float, default=3.5, help='ATR multiplier for trailing stop loss')
    parser.add_argument('--reports_dir', type=str, default='reports', help='Directory to save reports')
    parser.add_argument('--wfo_test_days', type=int, default=90, help='Days in OOS test set') 
    parser.add_argument('--wfo_window_years', type=float, default=2.0, help='Total years in each rolling window')
    args = parser.parse_args()
    granularity_map = {'1d': 86400}
    granularity_seconds = granularity_map.get(args.granularity.lower())
    if granularity_seconds is None: logger.error("Use '1d' granularity."); sys.exit(1)
    reports_path = Path(args.reports_dir); reports_path.mkdir(parents=True, exist_ok=True)

    _, wfo_results, _ = run_backtest(
        symbol=args.symbol, start_date=args.start_date, end_date=args.end_date,
        granularity=granularity_seconds, initial_capital=args.initial_capital,
        commission_pct=args.commission, slippage_pct=args.slippage, param_grid=None, 
        optimize_metric=args.optimize_metric, use_stops=(not args.no_stops),
        sl_atr_multiplier=args.sl_atr,
        tsl_atr_multiplier=args.tsl_atr,
        wfo_test_days=args.wfo_test_days, wfo_window_years=args.wfo_window_years
    )

    if wfo_results:
        logger.info("--- Manual WFO Results Summary ---")
        logger.info(f"Optimization Metric Used: {wfo_results.get('optimized_metric', 'N/A')}")
        logger.info(f"Fixed Stop Params: SL={wfo_results.get('fixed_sl_atr_multiplier','N/A')}, TSL={wfo_results.get('fixed_tsl_atr_multiplier','N/A')}")
        logger.info(f"OOS Sharpe Ratio: Mean={wfo_results.get('oos_mean_sharpe', np.nan):.4f}, Std={wfo_results.get('oos_std_sharpe', np.nan):.4f}")
        logger.info(f"OOS Total Return: Mean={wfo_results.get('oos_mean_return', np.nan):.4f}, Std={wfo_results.get('oos_std_return', np.nan):.4f}")
        logger.info(f"OOS Max Drawdown: Mean={wfo_results.get('oos_mean_drawdown', np.nan):.4f}, Std={wfo_results.get('oos_std_drawdown', np.nan):.4f}")
        try:
            save_path = reports_path / f"manual_wfo_fixed_stops_results_{args.symbol}_SL{args.sl_atr}_TSL{args.tsl_atr}.json"
            results_to_save = {}
            results_to_save['optimized_metric'] = wfo_results.get('optimized_metric')
            results_to_save['fixed_sl_atr_multiplier'] = args.sl_atr
            results_to_save['fixed_tsl_atr_multiplier'] = args.tsl_atr
            for metric_key in ['oos_sharpe', 'oos_return', 'oos_drawdown']:
                 if metric_key in wfo_results:
                     results_to_save[metric_key] = {str(k): (None if pd.isna(v) else v) for k, v in wfo_results[metric_key].items()}
                 else: results_to_save[metric_key] = {}
            if 'best_params_per_split' in wfo_results:
                 results_to_save['best_params_per_split'] = {str(k): {p_name: (int(p_val) if isinstance(p_val, np.integer) else float(p_val)) for p_name, p_val in params.items()} for k, params in wfo_results['best_params_per_split'].items()}
            else: results_to_save['best_params_per_split'] = {}
            for metric_key in ['oos_mean_sharpe', 'oos_std_sharpe', 'oos_mean_return', 'oos_std_return', 'oos_mean_drawdown', 'oos_std_drawdown']:
                 results_to_save[metric_key] = None if pd.isna(wfo_results.get(metric_key)) else wfo_results.get(metric_key)

            with open(save_path, 'w') as f: json.dump(results_to_save, f, indent=2)
            logger.info(f"WFO results saved to {save_path}")
        except Exception as save_err:
            logger.error(f"Error saving WFO results: {save_err}")
    else:
        logger.warning("Manual WFO did not produce results.")
    logger.info("--- Backtest Script Finished ---")

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
    main() 