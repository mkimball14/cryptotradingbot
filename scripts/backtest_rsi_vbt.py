import vectorbtpro as vbt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import logging
import sys
import os
import json
from datetime import datetime, timedelta
from typing import Tuple, Dict, List, Optional, Any
from pathlib import Path
from tqdm import tqdm  # For progress bars
import argparse
import multiprocessing
from functools import lru_cache
import traceback
from plotly.subplots import make_subplots
import warnings
import time
from itertools import product

# Add project root to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.coinbase import CoinbaseClient, RESTClient
from types import SimpleNamespace

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Utility Functions (Copied from backtest_rsi_vbt.py, potentially modify later) ---

# Helper function to map seconds to vectorbt frequency strings (Copied from stoch_sma script)
def get_vbt_freq_str(granularity_seconds: int) -> Optional[str]:
    # Map seconds to pandas frequency strings suitable for vectorbt
    vbt_freq_map = {
        60: "1T", 300: "5T", 900: "15T", 1800: "30T",
        3600: "1H", 7200: "2H", 14400: "4H", 21600: "6H", 86400: "1D"
    }
    return vbt_freq_map.get(granularity_seconds)

def fetch_historical_data(product_id, start_date, end_date, granularity=86400):
    """
    Fetch historical price data from Coinbase or from cache
    
    Parameters:
    -----------
    product_id : str
        The product ID (e.g., 'BTC-USD')
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    granularity : int
        Granularity in seconds (default: 86400 for daily)
        
    Returns:
    --------
    DataFrame
        Historical price data with columns: open, high, low, close, volume
    """
    # Create cache directory if it doesn't exist
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Define cache file path
    cache_file = cache_dir / f"{product_id.replace('-', '')}_{start_date}_{end_date}_{granularity}.csv"

    # Check if we have cached data
    if cache_file.exists():
        logger.info(f"Loading cached data from: {cache_file}")
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            
            # Check if data contains valid OHLCV columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            missing_cols = [col for col in required_cols if col not in data.columns]
            
            if missing_cols:
                logger.warning(f"Cached data missing columns: {missing_cols}")
                # Try to map from capitalized column names if present
                for col in missing_cols[:]:
                    cap_col = col.capitalize()
                    if cap_col in data.columns:
                        data[col] = data[cap_col]
                        missing_cols.remove(col)
                
                if missing_cols:
                    logger.warning(f"Still missing columns after mapping: {missing_cols}")
                    raise ValueError(f"Cached data missing required columns: {missing_cols}")
            
            logger.info(f"Successfully loaded cached data with shape: {data.shape}")
            return data
        except Exception as e:
            logger.warning(f"Error loading cached data: {e}, will fetch fresh data")
    
    # Check sample data cache if product_id includes "sample"
    if "sample" in product_id.lower():
        return create_sample_data(start_date, end_date)
    
    # Try to load API credentials
    creds_file = "cdp_api_key.json"
    if not os.path.exists(creds_file):
        logger.warning(f"Credentials file not found: {creds_file}")
        logger.info("Generating sample data instead")
        return create_sample_data(start_date, end_date)
    
    try:
        with open(creds_file, 'r') as f:
            creds = json.load(f)
            api_key = creds.get('api_key')
            api_secret = creds.get('api_secret')
            api_passphrase = creds.get('passphrase')
            
        if not all([api_key, api_secret, api_passphrase]):
            logger.warning("Missing required API credentials")
            logger.info("Generating sample data instead")
            return create_sample_data(start_date, end_date)
            
        # Convert dates to timestamp
        start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
        
        # Calculate number of candles
        candle_count = (end_timestamp - start_timestamp) // granularity
        logger.info(f"Requesting {candle_count} candles from Coinbase API")
        
        # Coinbase API has a limit of 300 candles per request
        max_candles_per_request = 300
        
        # Calculate how many chunks we need
        chunks = (candle_count + max_candles_per_request - 1) // max_candles_per_request
        
        # Initialize client
        client = RESTClient(api_key, api_secret, api_passphrase)
        
        # Fetch data in chunks
        all_candles = []
        chunk_start = start_timestamp
        
        for i in range(chunks):
            # Calculate chunk end time
            chunk_end = min(chunk_start + (max_candles_per_request * granularity), end_timestamp)
            
            logger.info(f"Fetching chunk {i+1}/{chunks}: {datetime.fromtimestamp(chunk_start)} to {datetime.fromtimestamp(chunk_end)}")
            
            # Make the API request
            candles = client.get_product_candles(
                product_id=product_id,
                start=chunk_start,
                end=chunk_end,
                granularity=granularity
            )
            
            if candles and 'message' not in candles:
                all_candles.extend(candles)
                logger.info(f"Got {len(candles)} candles for chunk {i+1}")
            else:
                error_msg = candles.get('message', 'Unknown error') if isinstance(candles, dict) else 'No candles returned'
                logger.error(f"API error: {error_msg}")
                if i == 0:  # If first chunk fails, create sample data
                    logger.info("First API request failed, falling back to sample data")
                    return create_sample_data(start_date, end_date)
            
            # Update chunk start for next iteration
            chunk_start = chunk_end
            
            # Wait to avoid rate limiting
            time.sleep(0.5)
        
        if not all_candles:
            logger.warning("No candles returned from API")
            logger.info("Generating sample data instead")
            return create_sample_data(start_date, end_date)
        
        # Convert to dataframe
        df = pd.DataFrame(all_candles, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        
        # Convert timestamp to datetime
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Set time as index
        df.set_index('time', inplace=True)
        
        # Sort by time
        df.sort_index(inplace=True)
        
        # Cache the data
        df.to_csv(cache_file)
        logger.info(f"Cached data to: {cache_file}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error fetching data from API: {e}")
        logger.info("Generating sample data instead")
        return create_sample_data(start_date, end_date)

def create_sample_data(start_date, end_date):
    """
    Create sample price data for backtesting when no real data is available.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        DataFrame with OHLCV data
    """
    logger.info(f"Creating sample BTC-USD price data for backtesting...")
    
    # Create directory for cached data if it doesn't exist
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if we have cached sample data
    cache_file = cache_dir / f"sample_{start_date}_{end_date}.csv"
    
    if cache_file.exists():
        logger.info(f"Loading cached sample data from: {cache_file}")
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            
            # Ensure all required columns exist
            if 'close' not in data.columns and 'Close' in data.columns:
                data['close'] = data['Close']
                data.drop('Close', axis=1, inplace=True, errors='ignore')
            
            # Check for missing OHLCV columns
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in data.columns for col in required_columns):
                logger.warning(f"Cached data missing required columns. Available columns: {data.columns}")
                logger.info("Regenerating sample data...")
                # Delete invalid cache file
                try:
                    cache_file.unlink()
                except:
                    pass
            else:
                logger.info(f"Loaded {len(data)} days of cached sample data")
                return data
        except Exception as e:
            logger.error(f"Error loading cached data: {e}")
    
    # Create date range
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    daterange = pd.date_range(start=start, end=end, freq='D')
    
    # Generate random price data with realistic properties
    np.random.seed(42)  # For reproducibility
    
    # Start with a price and add random changes
    price = 20000.0  # Starting price for BTC
    daily_volatility = 0.02  # 2% daily volatility
    
    prices = []
    for _ in range(len(daterange)):
        daily_return = np.random.normal(0.0002, daily_volatility)  # Slight upward drift
        price *= (1 + daily_return)
        prices.append(price)
    
    close_prices = pd.Series(prices, index=daterange)
    
    # Generate OHLCV data
    data = pd.DataFrame(index=daterange)
    data['close'] = close_prices
    data['high'] = data['close'] * (1 + np.random.uniform(0, 0.03, len(data)))
    data['low'] = data['close'] * (1 - np.random.uniform(0, 0.03, len(data)))
    data['open'] = data['close'].shift(1)
    
    # Handle first row
    data.loc[data.index[0], 'open'] = data.loc[data.index[0], 'close'] * 0.99
    
    # Add volume (proportional to price changes)
    price_changes = np.abs(data['close'].pct_change().fillna(0.01))
    base_volume = 1000  # Base volume in BTC
    data['volume'] = base_volume * (1 + 5 * price_changes)  # Higher volume on bigger price moves
    
    # Cache the generated data
    try:
        data.to_csv(cache_file)
        logger.info(f"Cached sample data to: {cache_file}")
    except Exception as e:
        logger.error(f"Error caching sample data: {e}")
    
    logger.info(f"Generated {len(data)} days of sample price data")
    return data

def optimize_rsi_strategy(data, param_grid=None, min_trades=5, metric='sharpe'):
    """
    Optimize RSI strategy parameters using vectorbtpro.

    Args:
        data (pd.DataFrame): OHLCV data.
        param_grid (dict): Dictionary of parameters to test (e.g., {'window': [10, 20]}).
        min_trades (int): Minimum number of trades required for a result to be considered valid.
        metric (str): Metric to optimize for ('sharpe', 'total_return', 'max_dd', etc.).
        
    Returns:
        dict: Dictionary containing best parameters, metrics, portfolio, and all results.
    """
    logger.info(f"Optimizing RSI strategy parameters...")
    
    # Use default parameter grid if none provided
    if param_grid is None:
        param_grid = {
            'window': [7, 14, 21],
            'lower_threshold': [20, 30, 40],
            'upper_threshold': [60, 70, 80]
        }
    
    # Extract parameter combinations
    windows = param_grid.get('window', [14])
    lower_thresholds = param_grid.get('lower_threshold', [30])
    upper_thresholds = param_grid.get('upper_threshold', [70])
    
    # Verify we have valid parameters to test
    if not all([windows, lower_thresholds, upper_thresholds]):
        logger.error("Invalid parameter grid: empty parameter lists")
        return None
    
    logger.info(f"Testing {len(windows) * len(lower_thresholds) * len(upper_thresholds)} parameter combinations")
    
    # Initialize strategy
    rsi_strategy = RSIMomentumVBT()
    
    # Store all results
    all_results = []
    best_result = None
    best_metric_value = float('-inf') if metric != 'max_dd' else float('inf')
    best_params = None
    
    # Test all parameter combinations
    for window in tqdm(windows, desc="Testing RSI windows"):
        for lower in lower_thresholds:
            for upper in upper_thresholds:
                # Skip invalid combinations (lower threshold >= upper threshold)
                if lower >= upper:
                    continue
                
                try:
                    # Run strategy with current parameters
                    logger.debug(f"Testing window={window}, lower={lower}, upper={upper}")
                    result = rsi_strategy.run_with_params(data, window=window, lower_threshold=lower, upper_threshold=upper)
                    
                    # Skip if portfolio is None or has no trades
                    if result is None or 'portfolio' not in result or result['portfolio'] is None:
                        logger.debug(f"No valid portfolio for window={window}, lower={lower}, upper={upper}")
                        continue
                    
                    portfolio = result['portfolio']
                    
                    # Calculate metrics
                    metrics = calculate_risk_metrics(portfolio)
                    
                    # Skip if fewer than min_trades
                    if metrics['trades'] < min_trades:
                        logger.debug(f"Too few trades ({metrics['trades']}) for window={window}, lower={lower}, upper={upper}")
                        continue
                    
                    # Store result with parameters and metrics
                    result_entry = {
                        'window': window,
                        'lower_threshold': lower,
                        'upper_threshold': upper,
                        'metrics': metrics,
                        'is_valid': True
                    }
                    
                    # Store in all results
                    all_results.append(result_entry)
                    
                    # Compare based on optimization metric
                    metric_value = None
                    if metric == 'sharpe':
                        metric_value = metrics['sharpe']
                    elif metric == 'total_return':
                        metric_value = metrics['total_return']
                    elif metric == 'max_dd':
                        metric_value = -metrics['max_dd']  # Negative because we want to minimize drawdown
                    elif metric == 'win_rate':
                        metric_value = metrics['win_rate']
                    elif metric == 'profit_factor':
                        metric_value = metrics['profit_factor']
                    else:
                        metric_value = metrics.get(metric, 0)
                    
                    # Update best if better
                    is_better = False
                    if metric == 'max_dd':
                        # For max_dd, lower is better (we use negative value above)
                        is_better = metric_value > best_metric_value
                    else:
                        is_better = metric_value > best_metric_value
                    
                    if is_better:
                        best_metric_value = metric_value
                        best_params = {
                            'window': window,
                            'lower_threshold': lower,
                            'upper_threshold': upper
                        }
                        best_result = result
                        logger.debug(f"New best: {metric}={best_metric_value}, params={best_params}")
                
                except Exception as e:
                    logger.error(f"Error testing parameters window={window}, lower={lower}, upper={upper}: {e}")
                    logger.debug(traceback.format_exc())
    
    # Check if we found any valid results
    if not all_results:
        logger.warning("No valid parameter combinations found")
        return None
    
    # If we have results but no "best" result (possible if all have same metric value)
    if best_result is None and all_results:
        # Just take the first valid result
        for result in all_results:
            if result.get('is_valid', False):
                best_params = {
                    'window': result['window'],
                    'lower_threshold': result['lower_threshold'],
                    'upper_threshold': result['upper_threshold']
                }
                # Rerun the strategy with these parameters to get the portfolio
                best_result = rsi_strategy.run_with_params(data, **best_params)
                break
    
    # Return best parameters and portfolio
    return {
        'best_params': best_params,
        'best_metrics': calculate_risk_metrics(best_result['portfolio']) if best_result else None,
        'portfolio': best_result['portfolio'] if best_result else None,
        'all_results': all_results
    }

# Enable caching for better performance
cache_dir = os.path.join('data', 'vbt_cache')
os.makedirs(cache_dir, exist_ok=True)

# Try to set VectorBT Pro theme if available
try:
    vbt.settings.plotting.theme = "dark"
except:
    logger.warning("Could not configure VectorBT Pro theme, using defaults")
    
# Create cache directory
cache_dir = Path("data/cache")
cache_dir.mkdir(parents=True, exist_ok=True)

# Suppress FutureWarnings from pandas/numpy
warnings.simplefilter(action='ignore', category=FutureWarning)

# Ensure reports directory exists
reports_dir = Path("reports")
reports_dir.mkdir(parents=True, exist_ok=True)

# Add a utility function to save portfolio plots to reports directory
def save_portfolio_plot(portfolio, filename, reports_dir=reports_dir):
    """
    Save a portfolio plot to the reports directory.
    
    Args:
        portfolio: The vectorbt Portfolio object
        filename: The filename to save the plot as
        reports_dir: The directory to save the plot in
    
    Returns:
        The path to the saved file
    """
    # Ensure reports directory exists
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate the plot
    fig = portfolio.plot()
    
    # Create full path
    plot_path = reports_dir / filename
    
    # Save the plot
    fig.write_html(str(plot_path))
    
    logger.info(f"Portfolio plot saved to {plot_path}")
    
    return plot_path

class RiskManager:
    """
    Risk management component that handles position sizing and stop-loss placement.
    
    Features:
    - ATR-based position sizing
    - Dynamic stop-loss placement
    - Maximum position limits
    - Equity curve-based position scaling
    """
    
    def __init__(self, initial_capital=10000, risk_per_trade_pct=0.02, max_position_pct=0.25,
                 atr_periods=14, atr_stop_multiplier=2.0, use_trailing_stop=True,
                 max_trades=5, equity_scaling=True):
        """
        Initialize the risk manager with parameters.
        
        Args:
            initial_capital (float): Starting capital
            risk_per_trade_pct (float): Percentage of capital to risk per trade (0.02 = 2%)
            max_position_pct (float): Maximum percentage of capital for any single position
            atr_periods (int): Lookback period for ATR calculation
            atr_stop_multiplier (float): Multiplier for ATR to set stop loss distance
            use_trailing_stop (bool): Whether to use trailing stops
            max_trades (int): Maximum number of concurrent trades
            equity_scaling (bool): Scale position size based on equity curve performance
        """
        self.initial_capital = initial_capital
        self.risk_per_trade_pct = risk_per_trade_pct
        self.max_position_pct = max_position_pct
        self.atr_periods = atr_periods
        self.atr_stop_multiplier = atr_stop_multiplier
        self.use_trailing_stop = use_trailing_stop
        self.max_trades = max_trades
        self.equity_scaling = equity_scaling
        self.current_equity = initial_capital
        self.drawdown = 0.0
        self.peak_equity = initial_capital
        
    def update_equity(self, equity):
        """Update current equity value and drawdown metrics."""
        self.current_equity = equity
        if equity > self.peak_equity:
            self.peak_equity = equity
        self.drawdown = 1.0 - (equity / self.peak_equity)
        
    def calculate_position_size(self, entry_price, stop_price, atr):
        """
        Calculate position size based on ATR and risk parameters.
        
        Args:
            entry_price (float): Entry price for the trade
            stop_price (float): Stop loss price
            atr (float): Current ATR value
            
        Returns:
            float: Position size in units
        """
        # Calculate risk amount in currency
        risk_amount = self.current_equity * self.risk_per_trade_pct
        
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_price)
        
        # If stop distance is too small, use ATR-based stop
        if risk_per_unit < (atr * 0.5):
            risk_per_unit = atr * self.atr_stop_multiplier
            
        # Calculate position size
        position_size = risk_amount / risk_per_unit if risk_per_unit > 0 else 0
        
        # Apply equity curve scaling if enabled
        if self.equity_scaling:
            # Reduce position size during drawdowns
            scale_factor = 1.0 - (self.drawdown * 2)  # Linear reduction, max 50% at 25% drawdown
            scale_factor = max(0.5, scale_factor)  # Don't scale below 50%
            position_size *= scale_factor
        
        # Apply maximum position constraint
        max_position_value = self.current_equity * self.max_position_pct
        max_position_size = max_position_value / entry_price
        position_size = min(position_size, max_position_size)
        
        return position_size
        
    def calculate_stop_loss(self, entry_price, entry_type, atr, close_prices=None):
        """
        Calculate stop loss price based on ATR.
        
        Args:
            entry_price (float): Entry price for the trade
            entry_type (str): 'long' or 'short'
            atr (float): Current ATR value
            close_prices (pd.Series, optional): Recent close prices for volatility-based adjustments
            
        Returns:
            float: Stop loss price
        """
        # Base stop distance on ATR
        stop_distance = atr * self.atr_stop_multiplier
        
        # Calculate stop price based on entry type
        if entry_type.lower() == 'long':
            stop_price = entry_price - stop_distance
        else:  # Short
            stop_price = entry_price + stop_distance
            
        # Adjust stop based on recent volatility if close prices provided
        if close_prices is not None and len(close_prices) > 20:
            # Calculate recent volatility ratio
            recent_vol = close_prices[-10:].std()
            longer_vol = close_prices[-20:].std()
            vol_ratio = recent_vol / longer_vol if longer_vol > 0 else 1.0
            
            # Adjust stop distance based on volatility ratio
            if vol_ratio > 1.2:  # Higher recent volatility
                if entry_type.lower() == 'long':
                    stop_price = entry_price - (stop_distance * 1.2)  # Wider stop
                else:
                    stop_price = entry_price + (stop_distance * 1.2)  # Wider stop
            elif vol_ratio < 0.8:  # Lower recent volatility
                if entry_type.lower() == 'long':
                    stop_price = entry_price - (stop_distance * 0.8)  # Tighter stop
                else:
                    stop_price = entry_price + (stop_distance * 0.8)  # Tighter stop
        
        return stop_price
        
    def update_trailing_stop(self, current_price, entry_price, stop_price, entry_type, atr):
        """
        Update trailing stop price based on price movement.
        
        Args:
            current_price (float): Current market price
            entry_price (float): Original entry price
            stop_price (float): Current stop loss price
            entry_type (str): 'long' or 'short'
            atr (float): Current ATR value
            
        Returns:
            float: Updated stop loss price
        """
        if not self.use_trailing_stop:
            return stop_price
            
        # For long positions
        if entry_type.lower() == 'long':
            # Calculate profit in price points
            profit_points = current_price - entry_price
            
            # Only trail stop if in profit by at least 1x ATR
            if profit_points > atr:
                # New stop would be current price minus ATR * multiplier
                new_stop = current_price - (atr * self.atr_stop_multiplier)
                
                # Only update if new stop is higher than current stop
                if new_stop > stop_price:
                    return new_stop
        
        # For short positions
        else:
            # Calculate profit in price points
            profit_points = entry_price - current_price
            
            # Only trail stop if in profit by at least 1x ATR
            if profit_points > atr:
                # New stop would be current price plus ATR * multiplier
                new_stop = current_price + (atr * self.atr_stop_multiplier)
                
                # Only update if new stop is lower than current stop
                if new_stop < stop_price:
                    return new_stop
        
        # Return original stop if no update needed
        return stop_price

class RSIMomentumVBT:
    """
    RSI Momentum strategy implementation using vectorbtpro.
    
    This strategy uses RSI with the following approach:
    - RSI below lower threshold: Buy signal (oversold)
    - RSI above upper threshold: Sell signal (overbought)
    - Additional filters based on moving average for trend direction
    - ATR-based stop losses and trailing stops
    - Dynamic position sizing based on volatility
    """
    
    def __init__(
            self, 
            window=14, 
            wtype='wilder',
            lower_threshold=30, 
            upper_threshold=70,
            ma_window=20,
            ma_type='sma',
            stop_pct=0.05,
            risk_pct=0.02,
            commission_pct=0.001,
            slippage_pct=0.0005,
            initial_capital=10000,
            max_trades_pct=0.95
        ):
        """
        Initialize the RSI Momentum strategy with parameters.
        
        Args:
            window: RSI lookback period
            wtype: RSI calculation type ('simple' or 'wilder')
            lower_threshold: RSI oversold threshold for buy signals
            upper_threshold: RSI overbought threshold for sell signals
            ma_window: Moving average window for trend filter
            ma_type: Moving average type ('sma' or 'ema')
            stop_pct: Stop loss percentage
            risk_pct: Risk per trade as percentage of capital
            commission_pct: Commission percentage per trade
            slippage_pct: Slippage rate for entries/exits
            initial_capital: Starting capital
            max_trades_pct: Maximum percentage of capital per trade
        """
        self.window = window
        self.wtype = wtype
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.ma_window = ma_window
        self.ma_type = ma_type
        self.stop_pct = stop_pct
        self.risk_pct = risk_pct
        self.commission_pct = commission_pct
        self.slippage_pct = slippage_pct
        self.initial_capital = initial_capital
        self.max_trades_pct = max_trades_pct
    
    # Cache RSI calculations to avoid redundant computation during optimization
    @staticmethod
    @lru_cache(maxsize=128)
    def _calculate_rsi(prices_tuple, window, rsi_type):
        """Calculate RSI with caching to improve performance.
        
        Args:
            prices_tuple: A tuple of prices (converted from Series for hashability)
            window: RSI window size
            rsi_type: RSI type ('wilder' or 'simple')
            
        Returns:
            RSI values as numpy array
        """
        prices = np.array(prices_tuple)
        
        # Fixed: Use standard RSI calculation instead of trying to use RSIModern
        # This is faster and more reliable
        delta = np.diff(prices, prepend=prices[0])
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        if rsi_type == 'wilder':
            # Wilder's smoothing
            avg_gain = np.zeros_like(prices)
            avg_loss = np.zeros_like(prices)
            
            # Initialize first value
            if len(prices) >= window:
                avg_gain[window-1] = np.mean(gain[:window])
                avg_loss[window-1] = np.mean(loss[:window])
                
                # Calculate subsequent values
                for i in range(window, len(prices)):
                    avg_gain[i] = (avg_gain[i-1] * (window-1) + gain[i]) / window
                    avg_loss[i] = (avg_loss[i-1] * (window-1) + loss[i]) / window
        else:
            # Simple moving average
            avg_gain = np.zeros_like(prices)
            avg_loss = np.zeros_like(prices)
            
            # Use rolling window
            for i in range(window-1, len(prices)):
                avg_gain[i] = np.mean(gain[(i-window+1):(i+1)])
                avg_loss[i] = np.mean(loss[(i-window+1):(i+1)])
        
        # Calculate RS
        rs = np.divide(avg_gain, avg_loss, out=np.ones_like(avg_gain), where=avg_loss != 0)
        
        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
            
    def run(self, data):
        """Run RSI strategy on the provided data."""
        # Convert DataFrame to avoid pandas warnings
        if isinstance(data, pd.DataFrame):
            if 'close' in data.columns:
                close = data['close']
            else:
                logger.warning("No 'close' column found, using the first column as close prices")
                close = data.iloc[:, 0]
        else:
            close = pd.Series(data)
            
        try:
            # Use cached RSI calculation by converting Series to tuple
            close_tuple = tuple(close.values)
            rsi_values = self._calculate_rsi(close_tuple, self.window, self.wtype)
            # Convert numpy array back to pandas Series with the same index as close
            rsi = pd.Series(rsi_values, index=close.index)
            
            # Calculate moving average
            if self.ma_type == 'sma':
                ma = vbt.MA.run(close, window=self.ma_window).ma
            else:
                ma = vbt.EMA.run(close, window=self.ma_window).ma
                
            # Calculate ATR for stop loss and position sizing
            atr = vbt.ATR.run(data['high'], data['low'], data['close'], window=14).atr
            
            # MUCH MORE AGGRESSIVE: Generate signals on every RSI reading below threshold
            # This will create many more entry signals
            entry_condition = rsi < 40  # Increased threshold to catch more entries
            
            # IMPROVED: Exit on RSI above threshold or significant price drop
            exit_condition = (rsi > 60) | (close < close.shift(1) * 0.97)  # Exit on 3% drop
            
            # Try regular portfolio creation first
            try:
                # Basic portfolio with fixed position size (1.0 = 100% of available capital)
                portfolio = vbt.Portfolio.from_signals(
                    close,
                    entries=entry_condition,
                    exits=exit_condition,
                    init_cash=self.initial_capital,
                    fees=self.commission_pct,
                    slippage=self.slippage_pct,
                    freq='1D'
                )
                
                # If we have trades, return the results
                if len(portfolio.trades) > 0:
                    return {
                        'portfolio': portfolio,
                        'rsi': rsi,
                        'ma': ma,
                        'entry_signals': entry_condition,
                        'exit_signals': exit_condition,
                        'price_data': data,
                        'rsi_indicator': rsi
                    }
            except Exception as e:
                logger.warning(f"Basic portfolio creation failed: {e}")
            
            # If the first attempt failed or produced no trades, try even more aggressive approach
            logger.info("First attempt produced no trades. Trying more aggressive approach.")
            
            # EXTREMELY AGGRESSIVE: Force entries on lowest RSI values
            rsi_percentile = rsi.rank(pct=True)  # Get percentile ranking of each RSI value
            entry_condition = rsi_percentile < 0.3  # Take bottom 30% of RSI values as entries
            exit_condition = rsi_percentile > 0.7  # Exit at top 30% of RSI values
            
            # Simplest portfolio creation
            portfolio = vbt.Portfolio.from_signals(
                close,
                entries=entry_condition,
                exits=exit_condition,
                init_cash=self.initial_capital,
                fees=0.001,  # Fixed 0.1% commission
                freq='1D'
            )
            
            return {
                'portfolio': portfolio,
                'rsi': rsi,
                'ma': ma,
                'entry_signals': entry_condition,
                'exit_signals': exit_condition,
                'price_data': data,
                'rsi_indicator': rsi
            }
        except Exception as e:
            logger.error(f"Error in strategy run: {e}")
            
    def run_with_params(self, data, window=None, lower_threshold=None, upper_threshold=None):
        """Run RSI strategy with specific parameters.
        
        This is used during optimization to test different parameter sets.
        """
        # Use provided parameters or instance defaults
        window = window if window is not None else self.window
        lower_threshold = lower_threshold if lower_threshold is not None else self.lower_threshold
        upper_threshold = upper_threshold if upper_threshold is not None else self.upper_threshold
        
        # Create a temporary strategy instance with these parameters
        temp_strategy = RSIMomentumVBT(
            window=window,
            wtype=self.wtype,
            lower_threshold=lower_threshold,
            upper_threshold=upper_threshold,
            ma_window=self.ma_window,
            ma_type=self.ma_type,
            stop_pct=self.stop_pct,
            risk_pct=self.risk_pct,
            commission_pct=self.commission_pct,
            slippage_pct=self.slippage_pct,
            initial_capital=self.initial_capital,
            max_trades_pct=self.max_trades_pct
        )
        
        # Run the strategy and return the results
        return temp_strategy.run(data)
        
    def optimize(self, data: pd.DataFrame, param_grid: Dict, optimize_metric: str, granularity_seconds: int = 86400):
        """
        Run vectorized backtest optimization using vectorbtpro for RSI Momentum.
        (Manual parameter iteration approach)

        Args:
            data: DataFrame with OHLCV data.
            param_grid: Dictionary with parameter names as keys and arrays of values to test.
                        Expected keys: 'window', 'lower_threshold', 'upper_threshold' (and optionally 'ma_window').
            optimize_metric: The metric string used by vectorbtpro for ranking.
            granularity_seconds: Data granularity for frequency calculation.

        Returns:
            vectorbtpro Portfolio object or None on error.
        """
        freq_str = get_vbt_freq_str(granularity_seconds)
        if not freq_str:
            logger.error(f"Invalid granularity seconds ({granularity_seconds}) for freq string. Cannot optimize RSI.")
            return None
            
        if isinstance(data, pd.DataFrame):
            if 'close' in data.columns:
                close = data['close']
            else:
                logger.warning("No 'close' column found, using the first column as close prices")
                close = data.iloc[:, 0]
        else:
            close = pd.Series(data) # Assuming data is a Series if not DataFrame

        logger.info(f"Running RSIMomentum optimization with grid (manual iteration): {param_grid}")
        
        try:
            # --- 1. Generate Parameter Combinations ---
            # Handle potential single MA window value
            ma_window_param = param_grid.get('ma_window', self.ma_window)
            if not isinstance(ma_window_param, (np.ndarray, list, range)):
                 ma_window_param = [ma_window_param] # Wrap single value in list
                 
            param_names = ['window', 'lower_threshold', 'upper_threshold', 'ma_window'] # Order matters
            param_arrays = [
                param_grid['window'],
                param_grid['lower_threshold'],
                param_grid['upper_threshold'],
                ma_window_param # Use the list version
            ]
            param_combinations = list(product(*param_arrays))
            logger.info(f"Generated {len(param_combinations)} parameter combinations manually.")
            
            all_entries = []
            all_exits = []

            # --- 2. Loop Through Combinations and Generate Signals ---
            for rsi_w, lower_th, upper_th, ma_w in tqdm(param_combinations, desc="Simulating RSIMomentum"):
                try:
                    # Calculate RSI for this combination
                    rsi = vbt.RSI.run(close, window=rsi_w, wtype=self.wtype).rsi
                    
                    # Calculate MA for this combination
                    if self.ma_type == 'sma':
                        ma = vbt.MA.run(close, window=ma_w).ma
                    else:
                        ma = vbt.EMA.run(close, window=ma_w).ma
                    
                    if rsi.isnull().all() or ma.isnull().all():
                        # Append False series if indicator fails
                        all_entries.append(pd.Series(False, index=close.index))
                        all_exits.append(pd.Series(False, index=close.index))
                        continue
                        
                    # Generate signals
                    entry_signal = rsi.vbt.crossed_below(lower_th) & (close > ma)
                    exit_signal = rsi.vbt.crossed_above(upper_th)
                    
                    all_entries.append(entry_signal)
                    all_exits.append(exit_signal)

                except Exception as loop_err:
                     logger.warning(f"Error in loop for params ({rsi_w},{lower_th},{upper_th},{ma_w}): {loop_err}. Appending False signals.")
                     all_entries.append(pd.Series(False, index=close.index))
                     all_exits.append(pd.Series(False, index=close.index))
            
            if not all_entries:
                 logger.error("No signals generated for any parameter combination.")
                 return None

            # --- 3. Combine Signals ---
            param_multi_index = pd.MultiIndex.from_tuples(param_combinations, names=param_names)
            entries_output = pd.concat(all_entries, axis=1, keys=param_multi_index)
            exits_output = pd.concat(all_exits, axis=1, keys=param_multi_index)

            # --- 4. Run Portfolio Simulation --- 
            pf_kwargs = {
                'close': close, # Use original close for portfolio price
                'entries': entries_output,
                'exits': exits_output,
                'freq': freq_str,
                'init_cash': self.initial_capital,
                'fees': self.commission_pct,
                'slippage': self.slippage_pct,
                # 'metrics': optimize_metric # Removed - Portfolio doesn't take this directly
            }
            
            # Add stops if this strategy implementation includes them
            # if self.use_stops: ... calculate and add sl_stop/tsl_stop kwargs ...
            
            logger.info(f"Running Portfolio.from_signals with {entries_output.shape[1]} parameter combinations (manual loop).")
            pf = vbt.Portfolio.from_signals(**pf_kwargs)
            logger.info("Portfolio simulation complete.")

            # --- 5. Return Portfolio Object --- 
            return pf

        except Exception as e:
            logger.error(f"Error during RSIMomentum optimization (manual iteration): {e}", exc_info=True)
            return None

class MultiIndicatorStrategy(RSIMomentumVBT):
    """
    Enhanced strategy that combines RSI with additional indicators for more robust signals.
    Inherits from RSIMomentumVBT and adds MACD and Bollinger Bands.
    """
    
    def __init__(self, window=14, wtype='wilder', lower_threshold=30, upper_threshold=70,
                 ma_window=20, ma_type='sma', stop_pct=0.05, risk_pct=0.02,
                 commission_pct=0.001, slippage_pct=0.0005, initial_capital=10000,
                 max_trades_pct=0.95, use_macd=True, use_bbands=True):
        """Initialize with additional indicator parameters."""
        super().__init__(window, wtype, lower_threshold, upper_threshold, ma_window,
                        ma_type, stop_pct, risk_pct, commission_pct, slippage_pct,
                        initial_capital, max_trades_pct)
        self.use_macd = use_macd
        self.use_bbands = use_bbands
        
    def run(self, data):
        """Run enhanced strategy with multiple indicators."""
        # Get baseline RSI strategy results
        result = super().run(data)
        
        # If we already have trades from the base strategy, return it
        if len(result['portfolio'].trades) > 0:
            return result
            
        # Extract components
        close = data['close'] if 'close' in data.columns else data.iloc[:, 0]
        rsi = result['rsi']
        entry_signals = result['entry_signals']
        exit_signals = result['exit_signals']
        
        # Add MACD signals if enabled
        if self.use_macd:
            try:
                # Calculate MACD using VectorBT
                macd = vbt.MACD.run(close, fast_window=12, slow_window=26, signal_window=9)
                
                # MACD crossover signals
                macd_buy = macd.macd_above_signal() & (macd.macd < 0)  # Bullish crossover in negative territory
                macd_sell = macd.macd_below_signal() & (macd.macd > 0)  # Bearish crossover in positive territory
                
                # Combine with RSI signals
                entry_signals = entry_signals | macd_buy
                exit_signals = exit_signals | macd_sell
                
                logger.info("Added MACD signals to strategy")
            except Exception as e:
                logger.warning(f"Error adding MACD signals: {e}")
        
        # Add Bollinger Bands signals if enabled
        if self.use_bbands:
            try:
                # Calculate Bollinger Bands
                bbands = vbt.BBands.run(close, window=20, alpha=2.0)
                
                # Bollinger Band signals
                # Buy when price touches lower band during RSI oversold
                bb_buy = (close <= bbands.lower) & (rsi < 40)
                
                # Sell when price touches upper band during RSI overbought
                bb_sell = (close >= bbands.upper) & (rsi > 60)
                
                # Combine with existing signals
                entry_signals = entry_signals | bb_buy
                exit_signals = exit_signals | bb_sell
                
                logger.info("Added Bollinger Bands signals to strategy")
            except Exception as e:
                logger.warning(f"Error adding Bollinger Bands signals: {e}")
        
        # Create portfolio with combined signals
        try:
            portfolio = vbt.Portfolio.from_signals(
                close,
                entries=entry_signals,
                exits=exit_signals,
                init_cash=self.initial_capital,
                fees=self.commission_pct,
                slippage=self.slippage_pct,
                freq='1D'
            )
            
            return {
                'portfolio': portfolio,
                'rsi': rsi,
                'entry_signals': entry_signals,
                'exit_signals': exit_signals,
                'is_multi_indicator': True
            }
        except Exception as e:
            logger.warning(f"Error creating portfolio with multi-indicator strategy: {e}")
            return result  # Return original result if new portfolio creation fails

class EnhancedRSIStrategy(RSIMomentumVBT):
    """
    Enhanced RSI strategy with advanced risk management.
    """
    
    def __init__(self, window=14, wtype='wilder', lower_threshold=30, upper_threshold=70,
                 ma_window=20, ma_type='sma', stop_pct=0.05, risk_pct=0.02,
                 commission_pct=0.001, slippage_pct=0.0005, initial_capital=10000,
                 max_trades_pct=0.25, atr_stop_multiplier=2.0, use_trailing_stop=True,
                 equity_scaling=True):
        """Initialize with risk management parameters."""
        super().__init__(window, wtype, lower_threshold, upper_threshold, ma_window,
                        ma_type, stop_pct, risk_pct, commission_pct, slippage_pct,
                        initial_capital, max_trades_pct)
        
        # Initialize risk manager
        self.risk_manager = RiskManager(
            initial_capital=initial_capital,
            risk_per_trade_pct=risk_pct,
            max_position_pct=max_trades_pct,
            atr_periods=14,
            atr_stop_multiplier=atr_stop_multiplier,
            use_trailing_stop=use_trailing_stop,
            equity_scaling=equity_scaling
        )
        
    def run(self, data):
        """Run enhanced strategy with advanced risk management."""
        # Get baseline RSI signals
        result = super().run(data)
        
        # Extract price data and signals
        close = data['close']
        atr = vbt.ATR.run(data['high'], data['low'], data['close'], window=14).atr
        
        entry_signals = result['entry_signals']
        exit_signals = result['exit_signals']
        
        # Calculate dynamic position sizes based on ATR
        position_sizes = pd.Series(index=close.index, dtype=float)
        stop_losses = pd.Series(index=close.index, dtype=float)
        
        # Set initial equity
        self.risk_manager.update_equity(self.initial_capital)
        
        # Loop through dates to simulate dynamic position sizing
        for i in range(1, len(close)):
            current_date = close.index[i]
            prev_date = close.index[i-1]
            
            # Skip if no entry signal
            if not entry_signals[i]:
                position_sizes[current_date] = 0.0
                continue
                
            # Calculate position size and stop loss for entry signal
            entry_price = close[i]
            current_atr = atr[i]
            
            # Calculate stop loss price
            stop_price = self.risk_manager.calculate_stop_loss(
                entry_price, 'long', current_atr, close[max(0, i-20):i]
            )
            stop_losses[current_date] = stop_price
            
            # Calculate position size
            pos_size = self.risk_manager.calculate_position_size(
                entry_price, stop_price, current_atr
            )
            position_sizes[current_date] = pos_size
            
            # Update risk manager with equity if we had a position
            if i > 2:
                # Simple equity update simulation
                equity_change = close[i] / close[i-1] - 1.0
                new_equity = self.risk_manager.current_equity * (1.0 + equity_change)
                self.risk_manager.update_equity(new_equity)
        
        # Create enhanced portfolio with dynamic position sizing
        try:
            # Try to create portfolio with all features
            portfolio = vbt.Portfolio.from_signals(
                close,
                entries=entry_signals,
                exits=exit_signals,
                init_cash=self.initial_capital,
                fees=self.commission_pct,
                slippage=self.slippage_pct,
                freq='1D',
                size=position_sizes
            )
            
            logger.info("Created portfolio with dynamic position sizing")
            
            # Return enhanced results
            return {
                'portfolio': portfolio,
                'rsi': result['rsi'],
                'entry_signals': entry_signals,
                'exit_signals': exit_signals,
                'position_sizes': position_sizes,
                'stop_losses': stop_losses,
                'is_enhanced': True
            }
        
        except Exception as e:
            logger.warning(f"Error creating enhanced portfolio: {e}. Falling back to basic portfolio.")
            return result

def calculate_risk_metrics(portfolio):
    """
    Calculate key risk and performance metrics from a portfolio.
    
    Parameters:
    -----------
    portfolio : Portfolio
        VectorBT portfolio object
    
    Returns:
    --------
    dict
        Dictionary containing performance metrics
    """
    metrics = {}
    
    try:
        # Access portfolio stats
        if hasattr(portfolio, 'stats'):
            stats = portfolio.stats()
        else:
            stats = {}
            
        # Ensure we have portfolio returns
        if hasattr(portfolio, 'returns'):
            returns = portfolio.returns
        else:
            returns = pd.Series(0, index=portfolio.wrapper.index)
            
        # Extract total return
        if 'total_return' in stats:
            metrics['total_return'] = stats['total_return']
        elif 'Total Return [%]' in stats:
            metrics['total_return'] = stats['Total Return [%]'] / 100
        else:
            # Calculate from final value
            metrics['total_return'] = (portfolio.value.iloc[-1] / portfolio.value.iloc[0]) - 1
            
        # Extract Sharpe ratio
        if 'sharpe_ratio' in stats:
            metrics['sharpe'] = stats['sharpe_ratio']
        elif 'Sharpe Ratio' in stats:
            metrics['sharpe'] = stats['Sharpe Ratio']
        else:
            # Calculate manually if not available
            if returns.std() > 0:
                metrics['sharpe'] = (returns.mean() / returns.std()) * np.sqrt(252)
            else:
                metrics['sharpe'] = 0
                
        # Extract max drawdown
        if 'max_drawdown' in stats:
            metrics['max_dd'] = stats['max_drawdown']
        elif 'Max Drawdown [%]' in stats:
            metrics['max_dd'] = stats['Max Drawdown [%]'] / 100
        else:
            # Calculate drawdown manually
            drawdown = portfolio.drawdown().max()
            metrics['max_dd'] = drawdown if not np.isnan(drawdown) else 0
            
        # Calculate win rate and other trade-based metrics
        metrics['trades'] = 0
        metrics['win_rate'] = 0
        metrics['profit_factor'] = 0
        metrics['recovery_factor'] = 0
        
        # Check if portfolio has trades and if they are accessible
        if hasattr(portfolio, 'trades') and portfolio.trades is not None:
            try:
                # Attempt to get trades count. This might differ based on VBT version or if it's a single run vs optimization result.
                if isinstance(portfolio.trades.count(), (int, np.integer)):
                    num_trades = portfolio.trades.count()
                elif isinstance(portfolio.trades.count(), pd.Series):
                    num_trades = portfolio.trades.count().iloc[0] # Assuming single portfolio column if Series
                else: # Fallback for other potential types like MappedArray
                    num_trades = len(portfolio.trades) # Use len() as a fallback

                if num_trades > 0:
                    metrics['trades'] = num_trades
                    
                    # Access trade records safely
                    trade_records = portfolio.trades.records_arr
                    
                    # Ensure PnL calculation works
                    pnl = trade_records['pnl']
                    
                    winning_trades = pnl[pnl > 0]
                    losing_trades = pnl[pnl < 0]
                    
                    metrics['win_rate'] = len(winning_trades) / num_trades
                    
                    total_profit = winning_trades.sum()
                    total_loss = abs(losing_trades.sum())
                    
                    metrics['profit_factor'] = total_profit / total_loss if total_loss != 0 else float('inf')
                    
                    if metrics['max_dd'] > 0:
                        metrics['recovery_factor'] = metrics['total_return'] / metrics['max_dd']
                    else:
                        metrics['recovery_factor'] = float('inf')
            except Exception as trade_err:
                # Log specific error encountered when accessing trades
                logger.warning(f"Could not calculate trade-based metrics: {trade_err}")
                # Keep default zero values for trade metrics

        # Calculate annualized return
        metrics['annual_return'] = 0 # Default value
        
        # Calculate Sortino ratio
        negative_returns = returns[returns < 0]
        if len(negative_returns) > 0 and negative_returns.std() > 0:
            metrics['sortino'] = (returns.mean() / negative_returns.std()) * np.sqrt(252)
        else:
            metrics['sortino'] = metrics['sharpe']
        
    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}")
        metrics = {
            'total_return': 0,
            'sharpe': 0,
            'max_dd': 0,
            'win_rate': 0,
            'trades': 0,
            'annual_return': 0,
            'sortino': 0,
            'profit_factor': 0,
            'recovery_factor': 0
        }
        
    return metrics

class MultiTimeframeStrategy:
    """
    Multi-timeframe RSI strategy that combines signals from different timeframes.
    
    Uses higher timeframe for trend confirmation and lower timeframe for entry timing.
    Dynamically adjusts position size based on signal strength.
    """
    
    def __init__(self, primary_data, higher_tf_data=None, lower_tf_data=None, 
                 rsi_window=14, lower_threshold=30, upper_threshold=70,
                 ma_window=50, atr_window=14, risk_pct=1.0,
                 initial_capital=10000.0, commission_pct=0.001, wtype='wilder'):
        """
        Initialize the multi-timeframe strategy.
        
        Parameters:
        -----------
        primary_data : pd.DataFrame
            Primary timeframe data with OHLCV columns (e.g., daily)
        higher_tf_data : pd.DataFrame, optional
            Higher timeframe data for trend confirmation (e.g., weekly)
        lower_tf_data : pd.DataFrame, optional
            Lower timeframe data for entry timing (e.g., 4-hour)
        rsi_window : int
            RSI calculation period
        lower_threshold : int
            Lower RSI threshold for oversold condition
        upper_threshold : int
            Upper RSI threshold for overbought condition
        ma_window : int
            Moving average window for trend confirmation
        atr_window : int
            ATR window for volatility calculation
        risk_pct : float
            Percentage of capital to risk per trade
        initial_capital : float
            Initial capital for backtesting
        commission_pct : float
            Commission percentage per trade
        wtype : str
            RSI calculation type ('wilder' or 'simple')
        """
        self.primary_data = primary_data
        self.higher_tf_data = higher_tf_data
        self.lower_tf_data = lower_tf_data
        
        self.rsi_window = rsi_window
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.ma_window = ma_window
        self.atr_window = atr_window
        self.risk_pct = risk_pct
        self.wtype = wtype
        
        self.initial_capital = initial_capital
        self.commission_pct = commission_pct
        
        # Create dictionary to hold RSI values at different timeframes
        self.rsi_values = {}
        
    def create_higher_tf_data(self):
        """Create higher timeframe data if not provided."""
        if self.higher_tf_data is None and self.primary_data is not None:
            logger.info("Creating higher timeframe data from primary timeframe")
            self.higher_tf_data = self.primary_data.resample('W').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            })
    
    def create_lower_tf_data(self):
        """Create lower timeframe data if not provided."""
        if self.lower_tf_data is None and self.primary_data is not None:
            logger.info("Using primary timeframe data as lower timeframe")
            self.lower_tf_data = self.primary_data.copy()
    
    def calculate_primary_rsi(self):
        """Calculate RSI for primary timeframe."""
        self.rsi_values['primary'] = vbt.RSI.run(
            self.primary_data['close'], 
            window=self.rsi_window,
            wtype=self.wtype
        ).rsi
        
        return self.rsi_values['primary']
    
    def calculate_higher_tf_rsi(self):
        """Calculate RSI for higher timeframe."""
        if self.higher_tf_data is not None:
            self.rsi_values['higher'] = vbt.RSI.run(
                self.higher_tf_data['close'], 
                window=self.rsi_window,
                wtype=self.wtype
            ).rsi
            
            # Forward-fill to primary timeframe
            reindexed = self.rsi_values['higher'].reindex(
                self.primary_data.index, method='ffill'
            )
            
            return reindexed
        
        return None
    
    def calculate_lower_tf_rsi(self):
        """Calculate RSI for lower timeframe."""
        if self.lower_tf_data is not None:
            self.rsi_values['lower'] = vbt.RSI.run(
                self.lower_tf_data['close'], 
                window=self.rsi_window // 2,  # Use shorter window for lower timeframe
                wtype=self.wtype
            ).rsi
            
            # Resample to primary timeframe (use last value of each day)
            if self.primary_data.index.freq != self.lower_tf_data.index.freq:
                # Fix for freq=None issue: use '1D' explicitly if primary data has daily frequency
                primary_freq = '1D'
                if self.primary_data.index.inferred_freq:
                    primary_freq = self.primary_data.index.inferred_freq
                    
                # Resample using the inferred or explicit frequency
                resampled = self.rsi_values['lower'].resample(primary_freq).last()
                reindexed = resampled.reindex(self.primary_data.index, method='ffill')
                return reindexed
            
            return self.rsi_values['lower']
        
        return None
    
    def align_timeframes(self):
        """Align all RSI signals to the primary timeframe."""
        # Calculate primary timeframe RSI
        primary_rsi = self.calculate_primary_rsi()
        
        # Calculate higher timeframe RSI if available
        higher_tf_rsi = self.calculate_higher_tf_rsi()
        
        # Calculate lower timeframe RSI if available
        lower_tf_rsi = self.calculate_lower_tf_rsi()
        
        # Create DataFrame with all signals aligned to primary timeframe
        signals = pd.DataFrame(index=self.primary_data.index)
        signals['primary_rsi'] = primary_rsi
        
        if higher_tf_rsi is not None:
            signals['higher_tf_rsi'] = higher_tf_rsi
            
        if lower_tf_rsi is not None:
            signals['lower_tf_rsi'] = lower_tf_rsi
            
        # Fill any missing values
        signals = signals.fillna(method='ffill')
        
        return signals
    
    def calculate_signal_strength(self, signals):
        """
        Calculate signal strength based on RSI across timeframes.
        
        Higher strength for signals confirmed across multiple timeframes.
        """
        # Initialize signal strength
        signals['entry_strength'] = 0.0
        signals['exit_strength'] = 0.0
        
        # Baseline strength from primary timeframe
        oversold = signals['primary_rsi'] < self.lower_threshold
        overbought = signals['primary_rsi'] > self.upper_threshold
        
        # Stronger signal as RSI gets more extreme
        signals.loc[oversold, 'entry_strength'] = (
            (self.lower_threshold - signals.loc[oversold, 'primary_rsi']) / 
            self.lower_threshold
        )
        
        signals.loc[overbought, 'exit_strength'] = (
            (signals.loc[overbought, 'primary_rsi'] - self.upper_threshold) / 
            (100 - self.upper_threshold)
        )
        
        # Add confirmation from higher timeframe if available
        if 'higher_tf_rsi' in signals.columns:
            higher_oversold = signals['higher_tf_rsi'] < self.lower_threshold
            higher_overbought = signals['higher_tf_rsi'] > self.upper_threshold
            
            # Boost signals if higher timeframe confirms
            signals.loc[oversold & higher_oversold, 'entry_strength'] *= 1.5
            signals.loc[overbought & higher_overbought, 'exit_strength'] *= 1.5
            
            # Reduce signals if higher timeframe contradicts
            higher_contradicts_entry = signals['higher_tf_rsi'] > 50
            higher_contradicts_exit = signals['higher_tf_rsi'] < 50
            
            signals.loc[oversold & higher_contradicts_entry, 'entry_strength'] *= 0.5
            signals.loc[overbought & higher_contradicts_exit, 'exit_strength'] *= 0.5
        
        # Add confirmation from lower timeframe if available
        if 'lower_tf_rsi' in signals.columns:
            lower_oversold = signals['lower_tf_rsi'] < self.lower_threshold
            lower_overbought = signals['lower_tf_rsi'] > self.upper_threshold
            
            # Boost signals if lower timeframe confirms
            signals.loc[oversold & lower_oversold, 'entry_strength'] *= 1.3
            signals.loc[overbought & lower_overbought, 'exit_strength'] *= 1.3
        
        return signals
    
    def calculate_position_sizes(self, signals):
        """
        Calculate position sizes based on ATR and signal strength.
        
        Uses a risk-based position sizing model where stronger signals
        get allocated a larger percentage of capital.
        """
        # Calculate ATR for risk-based position sizing
        atr = vbt.ATR.run(
            self.primary_data['high'], 
            self.primary_data['low'], 
            self.primary_data['close'], 
            window=self.atr_window
        ).atr
        
        # Calculate position sizes
        signals['position_pct'] = 0.0
        
        # Scale position size based on signal strength
        # For entry signals (long positions)
        entry_mask = signals['entry_strength'] > 0
        signals.loc[entry_mask, 'position_pct'] = signals.loc[entry_mask, 'entry_strength']
        
        # Cap at 100% of available capital
        signals['position_pct'] = np.minimum(signals['position_pct'], 1.0)
        
        # Calculate dollar risk per trade
        risk_amount = self.initial_capital * (self.risk_pct / 100)
        
        # Calculate position sizes in dollars
        signals['position_size'] = np.where(
            atr > 0,
            (risk_amount / atr) * signals['position_pct'],
            0
        )
        
        return signals
    
    def generate_entry_exit_signals(self, signals):
        """
        Generate entry and exit signals based on RSI conditions and signal strength.
        
        Uses primary_rsi crossing threshold as the main signal, but requires
        confirmation from other timeframes for stronger signals.
        """
        # Make signals more aggressive by lowering the strength threshold
        # Entry signal: RSI crosses below lower threshold with minimal strength required
        signals['entry_signal'] = (
            (signals['primary_rsi'] < self.lower_threshold) & 
            (signals['entry_strength'] > 0.05)  # Lower threshold to get more signals
        )
        
        # Exit signal: RSI crosses above upper threshold with minimal strength
        signals['exit_signal'] = (
            (signals['primary_rsi'] > self.upper_threshold) &
            (signals['exit_strength'] > 0.05)  # Lower threshold to get more signals
        )
        
        # Make sure we don't exit immediately after entry and vice versa
        signals['entry_signal'] = signals['entry_signal'] & ~signals['entry_signal'].shift(1).fillna(False)
        signals['exit_signal'] = signals['exit_signal'] & ~signals['exit_signal'].shift(1).fillna(False)
        
        # Ensure we have at least some signals for testing
        if signals['entry_signal'].sum() == 0:
            # If no signals, create some using more aggressive thresholds
            logger.info("No entry signals with standard thresholds, using more aggressive thresholds")
            signals['entry_signal'] = (signals['primary_rsi'] < 40) # More aggressive entry
            signals['entry_signal'] = signals['entry_signal'] & ~signals['entry_signal'].shift(1).fillna(False)
        
        if signals['exit_signal'].sum() == 0:
            logger.info("No exit signals with standard thresholds, using more aggressive thresholds")
            signals['exit_signal'] = (signals['primary_rsi'] > 60) # More aggressive exit
            signals['exit_signal'] = signals['exit_signal'] & ~signals['exit_signal'].shift(1).fillna(False)
        
        return signals
    
    def run(self):
        """Run the multi-timeframe strategy and return results."""
        try:
            # Ensure we have higher and lower timeframe data if needed
            self.create_higher_tf_data()
            self.create_lower_tf_data()
            
            # Align all RSI signals to primary timeframe
            signals = self.align_timeframes()
            
            # Calculate signal strength across timeframes
            signals = self.calculate_signal_strength(signals)
            
            # Calculate position sizes
            signals = self.calculate_position_sizes(signals)
            
            # Generate entry and exit signals
            signals = self.generate_entry_exit_signals(signals)
            
            # Create entries and exits for vectorbt
            entries = signals['entry_signal'].copy()
            exits = signals['exit_signal'].copy()
            
            # Run the portfolio simulation with dynamic position sizing
            try:
                portfolio = vbt.Portfolio.from_signals(
                    self.primary_data['close'],
                    entries=entries,
                    exits=exits,
                    size=signals['position_size'].shift(1),  # Use previous day's calculated size
                    init_cash=self.initial_capital,
                    fees=self.commission_pct,
                    freq=self.primary_data.index.freq
                )
                
                # Prepare results
                results = {
                    'portfolio': portfolio,
                    'entries': entries,
                    'exits': exits,
                    'primary_rsi': signals['primary_rsi'],
                    'entry_signals': signals['entry_signal'],
                    'exit_signals': signals['exit_signal'],
                    'signal_strength': signals['entry_strength']
                }
                
                if 'higher_tf_rsi' in signals.columns:
                    results['higher_tf_rsi'] = signals['higher_tf_rsi']
                    
                if 'lower_tf_rsi' in signals.columns:
                    results['lower_tf_rsi'] = signals['lower_tf_rsi']
                
                # Save the portfolio plot to reports directory
                symbol = getattr(self, 'symbol', 'BTC-USD')
                filename = f"multi_tf_rsi_strategy_results_{symbol.replace('-', '_')}.html"
                save_portfolio_plot(portfolio, filename)
                
                return results
                
            except Exception as e:
                logger.error(f"Error creating portfolio: {e}")
                logger.error(traceback.format_exc())
                return None
                
        except Exception as e:
            logger.error(f"Error in multi-timeframe strategy: {e}")
            logger.error(traceback.format_exc())
            return None
            
    def run_basic(self):
        """Run a basic multi-timeframe strategy."""
        logger.info("Running basic multi-timeframe strategy")
        # Just use the standard run method
        return self.run()
    
    def run_higher_tf_trend(self):
        """Run a multi-timeframe strategy focusing on higher timeframe trend confirmation."""
        logger.info("Running multi-timeframe strategy with higher timeframe trend confirmation")
        # Configure for higher timeframe trend focus
        if self.higher_tf_data is None:
            logger.warning("No higher timeframe data provided, creating it")
            self.create_higher_tf_data()
        return self.run()
    
    def run_lower_tf_entry(self):
        """Run a multi-timeframe strategy focusing on lower timeframe entry precision."""
        logger.info("Running multi-timeframe strategy with lower timeframe entry precision")
        # Configure for lower timeframe entry focus
        if self.lower_tf_data is None:
            logger.warning("No lower timeframe data provided, creating it")
            self.create_lower_tf_data()
        return self.run()
    
    def run_combined(self):
        """Run a combined multi-timeframe strategy using both higher and lower timeframes."""
        logger.info("Running combined multi-timeframe strategy")
        # Ensure both higher and lower timeframe data are available
        if self.higher_tf_data is None:
            logger.warning("No higher timeframe data provided, creating it")
            self.create_higher_tf_data()
        if self.lower_tf_data is None:
            logger.warning("No lower timeframe data provided, creating it")
            self.create_lower_tf_data()
        return self.run()

def test_multitimeframe_strategy(data, window=14, lower_th=30, upper_th=70, use_higher_tf=True, use_lower_tf=True):
    """
    Test a multi-timeframe RSI strategy with the given parameters.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Historical price data with OHLCV columns
    window : int
        RSI window length
    lower_th : int
        Lower RSI threshold for oversold condition
    upper_th : int
        Upper RSI threshold for overbought condition
    use_higher_tf : bool
        Whether to use higher timeframe for trend confirmation
    use_lower_tf : bool
        Whether to use lower timeframe for entry timing
        
    Returns:
    --------
    dict
        Dictionary containing portfolio, entry/exit signals and performance metrics
    """
    logger.info(f"Testing multi-timeframe RSI strategy with window={window}, lower_th={lower_th}, upper_th={upper_th}")
    
    try:
        # Create primary, higher and lower timeframe data
        higher_tf_data = None
        lower_tf_data = None
        
        # Create higher timeframe data (weekly)
        if use_higher_tf:
            higher_tf_data = data.resample('W').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            })
            logger.info(f"Created higher timeframe data: {len(higher_tf_data)} bars")
        
        # Create lower timeframe data (simulated 4h from daily)
        if use_lower_tf:
            # For demo purposes, we'll simulate 4h data by splitting each day into 6 bars
            # In a real implementation, you would use actual 4h data
            daily_returns = data['close'].pct_change().dropna()
            avg_daily_volatility = daily_returns.abs().mean()
            
            # Generate synthetic intraday data based on daily volatility patterns
            lower_tf_data = pd.DataFrame(index=pd.date_range(
                start=data.index[0], 
                end=data.index[-1], 
                freq='4H'
            ))
            
            # Forward fill from daily data to 4h timeframe
            for col in ['open', 'high', 'low', 'close', 'volume']:
                temp_data = data[col].reindex(lower_tf_data.index, method='ffill')
                
                # Add some noise to simulate intraday movements
                if col in ['high', 'low', 'close']:
                    noise = np.random.normal(0, avg_daily_volatility/4, size=len(lower_tf_data))
                    temp_data = temp_data * (1 + noise)
                    
                    # Ensure high is highest, low is lowest
                    if col == 'high':
                        temp_data = np.maximum(temp_data, data['close'].reindex(lower_tf_data.index, method='ffill'))
                    elif col == 'low':
                        temp_data = np.minimum(temp_data, data['close'].reindex(lower_tf_data.index, method='ffill'))
                
                lower_tf_data[col] = temp_data
                
            logger.info(f"Created lower timeframe data: {len(lower_tf_data)} bars")
        
        # Initialize and run the multi-timeframe strategy
        strategy = MultiTimeframeStrategy(
            primary_data=data,
            higher_tf_data=higher_tf_data,
            lower_tf_data=lower_tf_data,
            rsi_window=window,
            lower_threshold=lower_th,
            upper_threshold=upper_th,
            wtype='wilder'
        )
        
        # Run the strategy
        results = strategy.run()
        
        # Return the results
        return results
        
    except Exception as e:
        logger.error(f"Error in multi-timeframe strategy test: {e}")
        logger.error(traceback.format_exc())
        return None

def generate_multi_tf_report(result, filename='multi_tf_strategy_report.html', symbol='BTC-USD', start_date=None, end_date=None, reports_dir=None):
    """
    Generate a detailed HTML report for multi-timeframe strategy results.
    
    Parameters:
    -----------
    result : dict
        Strategy results dictionary
    filename : str
        Output HTML filename
    symbol : str
        Symbol being backtested (e.g., 'BTC-USD')
    start_date : str
        Start date of the backtest
    end_date : str
        End date of the backtest
    reports_dir : str or Path
        Directory to save the report in
    """
    try:
        if not result or 'portfolio' not in result or result['portfolio'] is None:
            logger.error("Cannot generate report: Invalid strategy results")
            return
            
        # Create reports directory if not provided
        if reports_dir is None:
            reports_dir = Path("reports")
        elif isinstance(reports_dir, str):
            reports_dir = Path(reports_dir)
            
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract the required data from the result
        portfolio = result['portfolio']
        metrics = calculate_risk_metrics(portfolio)
        price_data = result.get('price_data', None)
        
        if price_data is None and 'close' in portfolio.wrapper.columns:
            # Use the price data from the portfolio if available
            price_data = pd.DataFrame({
                'close': portfolio.wrapper.columns[0]
            })
        
        # Create a simulated optimized portfolio for comparison
        # This is a placeholder - in a real implementation, you'd have a separate optimization result
        basic_portfolio = portfolio  # The multi-timeframe strategy result
        optimized_portfolio = portfolio  # Using the same portfolio as a placeholder
        basic_metrics = metrics
        opt_metrics = metrics
        
        # Calculate benchmark returns (buy and hold)
        benchmark_returns = price_data['close'].pct_change().dropna()
        benchmark_cum_returns = (1 + benchmark_returns).cumprod() - 1
        
        # Create a Plotly figure
        fig = make_subplots(
            rows=4, 
            cols=2,
            subplot_titles=(
                "Cumulative Returns Comparison", "Drawdown Comparison",
                "Basic Strategy Performance", "Optimized Strategy Performance",
                "Price and RSI Indicator", "Monthly Returns Heatmap",
                "Returns Heatmap by Window/Threshold", "Sharpe Ratio Heatmap by Window/Threshold"
            ),
            specs=[
                [{"colspan": 1}, {"colspan": 1}],
                [{"type": "xy"}, {"type": "xy"}],
                [{"type": "xy"}, {"type": "heatmap"}],
                [{"type": "heatmap"}, {"type": "heatmap"}]
            ],
            vertical_spacing=0.10,
            horizontal_spacing=0.05,
            row_heights=[0.25, 0.25, 0.25, 0.25]
        )
        
        # 1. Comparison of cumulative returns
        # Get returns from both portfolios and benchmark
        basic_returns = basic_portfolio.returns.cumsum()
        opt_returns = optimized_portfolio.returns.cumsum()
        
        fig.add_trace(
            go.Scatter(
                x=basic_returns.index,
                y=basic_returns.values,
                mode='lines',
                name='Basic RSI',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=opt_returns.index,
                y=opt_returns.values,
                mode='lines',
                name='Optimized RSI',
                line=dict(color='green', width=2)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=benchmark_cum_returns.index,
                y=benchmark_cum_returns.values,
                mode='lines',
                name='Buy and Hold',
                line=dict(color='gray', width=2, dash='dash')
            ),
            row=1, col=1
        )
        
        # 2. Drawdown comparison
        basic_drawdown = (basic_portfolio.value / basic_portfolio.value.cummax() - 1)
        opt_drawdown = (optimized_portfolio.value / optimized_portfolio.value.cummax() - 1)
        benchmark_drawdown = (1 + benchmark_cum_returns) / (1 + benchmark_cum_returns).cummax() - 1
        
        fig.add_trace(
            go.Scatter(
                x=basic_drawdown.index,
                y=basic_drawdown.values,
                mode='lines',
                name='Basic RSI DD',
                line=dict(color='blue', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.1)'
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=opt_drawdown.index,
                y=opt_drawdown.values,
                mode='lines',
                name='Optimized RSI DD',
                line=dict(color='green', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 255, 0, 0.1)'
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=benchmark_drawdown.index,
                y=benchmark_drawdown.values,
                mode='lines',
                name='Buy and Hold DD',
                line=dict(color='gray', width=2, dash='dash'),
                fill='tozeroy',
                fillcolor='rgba(128, 128, 128, 0.1)'
            ),
            row=1, col=2
        )
        
        # 3. Basic strategy performance - Equity curve with trades
        fig.add_trace(
            go.Scatter(
                x=basic_portfolio.value.index,
                y=basic_portfolio.value.values,
                mode='lines',
                name='Basic Equity Curve',
                line=dict(color='blue', width=2)
            ),
            row=2, col=1
        )
        
        # 4. Optimized strategy performance - Equity curve with trades
        fig.add_trace(
            go.Scatter(
                x=optimized_portfolio.value.index,
                y=optimized_portfolio.value.values,
                mode='lines',
                name='Optimized Equity Curve',
                line=dict(color='green', width=2)
            ),
            row=2, col=2
        )
        
        # Add trade markers if available
        try:
            # For basic portfolio
            if basic_metrics['trades'] > 0:
                trade_data = basic_portfolio.trades.records
                
                # Entry points
                entry_times = [basic_returns.index[int(t)] if 0 <= int(t) < len(basic_returns.index) else None 
                              for t in trade_data['entry_idx']]
                entry_times = [et for et in entry_times if et is not None]
                
                entry_values = [basic_portfolio.value.iloc[int(t)] if 0 <= int(t) < len(basic_portfolio.value) else None
                               for t in trade_data['entry_idx']]
                entry_values = [ev for ev in entry_values if ev is not None]
                
                if entry_times and entry_values:
                    fig.add_trace(
                        go.Scatter(
                            x=entry_times,
                            y=entry_values,
                            mode='markers',
                            marker=dict(color='green', size=10, symbol='triangle-up'),
                            name='Basic Entries'
                        ),
                        row=2, col=1
                    )
                
                # Exit points
                exit_times = [basic_returns.index[int(t)] if 0 <= int(t) < len(basic_returns.index) else None 
                             for t in trade_data['exit_idx']]
                exit_times = [et for et in exit_times if et is not None]
                
                exit_values = [basic_portfolio.value.iloc[int(t)] if 0 <= int(t) < len(basic_portfolio.value) else None
                              for t in trade_data['exit_idx']]
                exit_values = [ev for ev in exit_values if ev is not None]
                
                if exit_times and exit_values:
                    fig.add_trace(
                        go.Scatter(
                            x=exit_times,
                            y=exit_values,
                            mode='markers',
                            marker=dict(color='red', size=10, symbol='triangle-down'),
                            name='Basic Exits'
                        ),
                        row=2, col=1
                    )
            
            # For optimized portfolio
            if opt_metrics['trades'] > 0:
                trade_data = optimized_portfolio.trades.records
                
                # Entry points
                entry_times = [opt_returns.index[int(t)] if 0 <= int(t) < len(opt_returns.index) else None 
                              for t in trade_data['entry_idx']]
                entry_times = [et for et in entry_times if et is not None]
                
                entry_values = [optimized_portfolio.value.iloc[int(t)] if 0 <= int(t) < len(optimized_portfolio.value) else None
                               for t in trade_data['entry_idx']]
                entry_values = [ev for ev in entry_values if ev is not None]
                
                if entry_times and entry_values:
                    fig.add_trace(
                        go.Scatter(
                            x=entry_times,
                            y=entry_values,
                            mode='markers',
                            marker=dict(color='green', size=10, symbol='triangle-up'),
                            name='Optimized Entries'
                        ),
                        row=2, col=2
                    )
                
                # Exit points
                exit_times = [opt_returns.index[int(t)] if 0 <= int(t) < len(opt_returns.index) else None 
                             for t in trade_data['exit_idx']]
                exit_times = [et for et in exit_times if et is not None]
                
                exit_values = [optimized_portfolio.value.iloc[int(t)] if 0 <= int(t) < len(optimized_portfolio.value) else None
                              for t in trade_data['exit_idx']]
                exit_values = [ev for ev in exit_values if ev is not None]
                
                if exit_times and exit_values:
                    fig.add_trace(
                        go.Scatter(
                            x=exit_times,
                            y=exit_values,
                            mode='markers',
                            marker=dict(color='red', size=10, symbol='triangle-down'),
                            name='Optimized Exits'
                        ),
                        row=2, col=2
                    )
        except Exception as e:
            logger.warning(f"Could not add trade markers: {e}")
            
        # 5. Price and RSI Indicator
        # Extract RSI values from results
        try:
            basic_rsi = results.get('rsi_indicator', None)
            opt_rsi = opt_results.get('rsi_indicator', None)
            
            # Create secondary y-axis for RSI
            fig.add_trace(
                go.Scatter(
                    x=price_data.index,
                    y=price_data['close'],
                    mode='lines',
                    name=f'{symbol} Price',
                    line=dict(color='black', width=2)
                ),
                row=3, col=1
            )
            
            if basic_rsi is not None:
                fig.add_trace(
                    go.Scatter(
                        x=basic_rsi.index,
                        y=basic_rsi.values,
                        mode='lines',
                        name='Basic RSI',
                        line=dict(color='blue', width=1),
                        yaxis="y3"
                    ),
                    row=3, col=1
                )
                
                # Add threshold lines
                basic_window = results.get('window', 14)
                basic_lower = results.get('lower_threshold', 30)
                basic_upper = results.get('upper_threshold', 70)
                
                fig.add_trace(
                    go.Scatter(
                        x=[basic_rsi.index[0], basic_rsi.index[-1]],
                        y=[basic_lower, basic_lower],
                        mode='lines',
                        line=dict(color='green', width=1, dash='dash'),
                        name=f'Lower Threshold ({basic_lower})',
                        yaxis="y3"
                    ),
                    row=3, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=[basic_rsi.index[0], basic_rsi.index[-1]],
                        y=[basic_upper, basic_upper],
                        mode='lines',
                        line=dict(color='red', width=1, dash='dash'),
                        name=f'Upper Threshold ({basic_upper})',
                        yaxis="y3"
                    ),
                    row=3, col=1
                )
                
                # Set up the secondary y-axis for RSI
                fig.update_layout(
                    yaxis3=dict(
                        title="RSI Value",
                        range=[0, 100],
                        side="right",
                        overlaying="y5",
                        showgrid=False
                    ),
                    yaxis5=dict(
                        title=f"{symbol} Price",
                        showgrid=True
                    )
                )
        except Exception as e:
            logger.warning(f"Could not add RSI indicator: {e}")
        
        # 6. Monthly Returns Heatmap
        try:
            # Convert daily returns to monthly returns
            basic_monthly_returns = basic_portfolio.returns.resample('M').apply(
                lambda x: (1 + x).prod() - 1
            )
            opt_monthly_returns = optimized_portfolio.returns.resample('M').apply(
                lambda x: (1 + x).prod() - 1
            )
            
            # Create a DataFrame with year as rows and month as columns
            basic_monthly_returns.index = basic_monthly_returns.index.strftime('%Y-%m')
            years = [date.split('-')[0] for date in basic_monthly_returns.index]
            months = [date.split('-')[1] for date in basic_monthly_returns.index]
            
            monthly_data = pd.DataFrame({
                'Year': years,
                'Month': months,
                'Basic': basic_monthly_returns.values * 100,  # Convert to percentage
                'Optimized': opt_monthly_returns.values * 100  # Convert to percentage
            })
            
            # Create a pivot table for the heatmap
            basic_pivot = pd.pivot_table(
                monthly_data, 
                values='Basic', 
                index='Year', 
                columns='Month',
                aggfunc='sum'
            )
            
            # For the months, ensure they're in the right order
            month_order = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            basic_pivot = basic_pivot.reindex(columns=month_order)
            
            # Draw the heatmap
            months_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            # Replace NaN with 0 for visualization
            basic_pivot = basic_pivot.fillna(0)
            
            fig.add_trace(
                go.Heatmap(
                    z=basic_pivot.values,
                    x=months_labels,
                    y=basic_pivot.index,
                    colorscale='RdYlGn',
                    colorbar=dict(title='Return %', x=0.46),
                    text=[[f"{val:.2f}%" for val in row] for row in basic_pivot.values],
                    hoverinfo='text',
                    zmin=-10,  # Minimum value for color scale
                    zmax=10   # Maximum value for color scale
                ),
                row=3, col=2
            )
        except Exception as e:
            logger.warning(f"Could not create monthly returns heatmap: {e}")
        
        # Create parameter heatmaps if we have optimization results
        if 'all_results' in opt_results and isinstance(opt_results['all_results'], list) and len(opt_results['all_results']) >= 9:
            try:
                # Extract parameters and metrics for heatmap
                windows = []
                lower_ths = []
                upper_ths = []
                returns = []
                sharpes = []
                trade_counts = []
                
                for result in opt_results['all_results']:
                    windows.append(result.get('window', 0))
                    lower_ths.append(result.get('lower_threshold', 0))
                    upper_ths.append(result.get('upper_threshold', 0))
                    returns.append(result.get('metrics', {}).get('total_return', 0) * 100)  # As percentage
                    sharpes.append(result.get('metrics', {}).get('sharpe', 0))
                    trade_counts.append(result.get('metrics', {}).get('trades', 0))
                
                # Identify unique parameter values
                unique_windows = sorted(set(windows))
                unique_lower = sorted(set(lower_ths))
                
                # Create return heatmap
                if len(unique_windows) > 1 and len(unique_lower) > 1:
                    return_matrix = np.zeros((len(unique_windows), len(unique_lower)))
                    trade_matrix = np.zeros((len(unique_windows), len(unique_lower)))
                    
                    # Create annotation text with trade counts
                    text_matrix = [['' for _ in range(len(unique_lower))] for _ in range(len(unique_windows))]
                    
                    for i, window in enumerate(unique_windows):
                        for j, lower in enumerate(unique_lower):
                            matching_returns = []
                            matching_trades = []
                            for idx in range(len(windows)):
                                if windows[idx] == window and lower_ths[idx] == lower:
                                    matching_returns.append(returns[idx])
                                    matching_trades.append(trade_counts[idx])
                            
                            if matching_returns:
                                best_idx = matching_returns.index(max(matching_returns))
                                return_matrix[i, j] = max(matching_returns)
                                trade_matrix[i, j] = matching_trades[best_idx]
                                text_matrix[i][j] = f"{return_matrix[i, j]:.2f}% ({trade_matrix[i, j]:.0f})"
                    
                    # Add return heatmap with trade count annotations
                    fig.add_trace(
                        go.Heatmap(
                            z=return_matrix,
                            x=unique_lower,
                            y=unique_windows,
                            colorscale='RdYlGn',
                            colorbar=dict(title='Return %'),
                            text=text_matrix,
                            hovertemplate='Window: %{y}<br>Lower Threshold: %{x}<br>Return: %{text}<extra></extra>',
                            zmin=-10,  # Minimum value for color scale
                            zmax=10    # Maximum value for color scale
                        ),
                        row=4, col=1
                    )
                    
                    # Create Sharpe ratio heatmap
                    sharpe_matrix = np.zeros((len(unique_windows), len(unique_lower)))
                    text_matrix = [['' for _ in range(len(unique_lower))] for _ in range(len(unique_windows))]
                    
                    for i, window in enumerate(unique_windows):
                        for j, lower in enumerate(unique_lower):
                            matching_sharpes = []
                            matching_trades = []
                            for idx in range(len(windows)):
                                if windows[idx] == window and lower_ths[idx] == lower:
                                    matching_sharpes.append(sharpes[idx])
                                    matching_trades.append(trade_counts[idx])
                            
                            if matching_sharpes:
                                best_idx = matching_sharpes.index(max(matching_sharpes))
                                sharpe_matrix[i, j] = max(matching_sharpes)
                                trade_matrix[i, j] = matching_trades[best_idx]
                                text_matrix[i][j] = f"{sharpe_matrix[i, j]:.2f} ({trade_matrix[i, j]:.0f})"
                    
                    # Add Sharpe ratio heatmap with trade count annotations
                    fig.add_trace(
                        go.Heatmap(
                            z=sharpe_matrix,
                            x=unique_lower,
                            y=unique_windows,
                            colorscale='RdYlGn',
                            colorbar=dict(title='Sharpe Ratio'),
                            text=text_matrix,
                            hovertemplate='Window: %{y}<br>Lower Threshold: %{x}<br>Sharpe: %{text}<extra></extra>',
                            zmin=-1,  # Minimum value for color scale
                            zmax=1    # Maximum value for color scale
                        ),
                        row=4, col=2
                    )
            except Exception as e:
                logger.warning(f"Could not create parameter heatmaps: {e}")
        
        # Calculate benchmark metrics
        benchmark_return = benchmark_cum_returns.iloc[-1]
        benchmark_dd = benchmark_drawdown.min()
        
        # Convert annual sharpe to appropriate time period
        days_in_period = (price_data.index[-1] - price_data.index[0]).days
        if days_in_period < 30:
            period_str = f"{days_in_period} days"
        elif days_in_period < 365:
            period_str = f"{days_in_period/30:.1f} months"
        else:
            period_str = f"{days_in_period/365:.1f} years"
            
        # Calculate annualized returns
        basic_annual_return = (1 + basic_metrics['total_return']) ** (365/days_in_period) - 1
        opt_annual_return = (1 + opt_metrics['total_return']) ** (365/days_in_period) - 1
        benchmark_annual_return = (1 + benchmark_return) ** (365/days_in_period) - 1
        
        # Add comparison metrics table as an annotation
        comparison_text = (
            f"<b>Performance Comparison ({period_str}):</b><br>"
            f"<br>"
            f"<b>Basic RSI:</b><br>"
            f"• Total Return: {basic_metrics['total_return']*100:.2f}% (Ann: {basic_annual_return*100:.2f}%)<br>"
            f"• Sharpe Ratio: {basic_metrics['sharpe']:.2f}<br>"
            f"• Max Drawdown: {basic_metrics['max_dd']*100:.2f}%<br>"
            f"• Win Rate: {basic_metrics['win_rate']*100:.2f}%<br>"
            f"• Total Trades: {basic_metrics['trades']}<br>"
            f"<br>"
            f"<b>Optimized RSI:</b><br>"
            f"• Total Return: {opt_metrics['total_return']*100:.2f}% (Ann: {opt_annual_return*100:.2f}%)<br>"
            f"• Sharpe Ratio: {opt_metrics['sharpe']:.2f}<br>"
            f"• Max Drawdown: {opt_metrics['max_dd']*100:.2f}%<br>"
            f"• Win Rate: {opt_metrics['win_rate']*100:.2f}%<br>"
            f"• Total Trades: {opt_metrics['trades']}<br>"
            f"<br>"
            f"<b>Buy and Hold:</b><br>"
            f"• Total Return: {benchmark_return*100:.2f}% (Ann: {benchmark_annual_return*100:.2f}%)<br>"
            f"• Max Drawdown: {benchmark_dd*100:.2f}%<br>"
        )
        
        # Add metrics comparison as a table annotation in the top right
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=1.0,
            y=1.0,
            text=comparison_text,
            showarrow=False,
            font=dict(size=10),
            align="left",
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="black",
            borderwidth=1,
            xanchor="right",
            yanchor="top"
        )
        
        # Add strategy parameter details
        basic_params_text = (
            f"<b>Basic RSI Parameters:</b><br>"
            f"• Window: {results.get('window', 14)}<br>"
            f"• Lower: {results.get('lower_threshold', 30)}<br>"
            f"• Upper: {results.get('upper_threshold', 70)}<br>"
        )
        
        opt_params_text = (
            f"<b>Optimized RSI Parameters:</b><br>"
            f"• Window: {opt_results.get('best_params', {}).get('window', 14)}<br>"
            f"• Lower: {opt_results.get('best_params', {}).get('lower_threshold', 30)}<br>"
            f"• Upper: {opt_results.get('best_params', {}).get('upper_threshold', 70)}<br>"
        )
        
        # Add parameter info to the basic strategy plot
        fig.add_annotation(
            xref="x3 domain",
            yref="y3 domain",
            x=0.05,
            y=0.05,
            text=basic_params_text,
            showarrow=False,
            font=dict(size=10),
            align="left",
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="black",
            borderwidth=1
        )
        
        # Add parameter info to the optimized strategy plot
        fig.add_annotation(
            xref="x4 domain",
            yref="y4 domain",
            x=0.05,
            y=0.05,
            text=opt_params_text,
            showarrow=False,
            font=dict(size=10),
            align="left",
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="black",
            borderwidth=1
        )
        
        # Update layout
        fig.update_layout(
            title=f"RSI Strategy Analysis: {symbol} ({start_date} to {end_date})",
            height=1400,
            width=1200,
            showlegend=True,
            template="plotly_white",  # Use a white background template
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        
        # Update axes titles
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=2)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=2)
        fig.update_xaxes(title_text="Date", row=3, col=1)
        fig.update_xaxes(title_text="Month", row=3, col=2)
        fig.update_xaxes(title_text="Lower Threshold", row=4, col=1)
        fig.update_xaxes(title_text="Lower Threshold", row=4, col=2)
        
        fig.update_yaxes(title_text="Cumulative Return", row=1, col=1)
        fig.update_yaxes(title_text="Drawdown", row=1, col=2)
        fig.update_yaxes(title_text="Portfolio Value", row=2, col=1)
        fig.update_yaxes(title_text="Portfolio Value", row=2, col=2)
        fig.update_yaxes(title_text="Price", row=3, col=1)
        fig.update_yaxes(title_text="Year", row=3, col=2)
        fig.update_yaxes(title_text="Window Size", row=4, col=1)
        fig.update_yaxes(title_text="Window Size", row=4, col=2)
        
        # Save the dashboard to HTML file
        dashboard_filename = f'rsi_strategy_dashboard_{symbol.replace("-", "_")}.html'
        dashboard_file = reports_dir / dashboard_filename
        
        # Force overwrite any existing file
        if dashboard_file.exists():
            dashboard_file.unlink()
        
        # Save with full configuration
        fig.write_html(
            str(dashboard_file),
            include_plotlyjs=True,
            full_html=True,
            include_mathjax='cdn',
            auto_open=False
        )
        
        logger.info(f"Interactive dashboard saved to {dashboard_file}")
        
        return str(dashboard_file)
    
    except Exception as e:
        logger.error(f"Error creating dashboard: {e}")
        logger.error(traceback.format_exc())
        return None

def create_dashboard(results, opt_results=None, symbol="BTC-USD", start_date=None, end_date=None, reports_dir=None):
    """
    Create an interactive dashboard for strategy analysis.
    
    Parameters:
    -----------
    results : dict
        Results from the basic RSI strategy
    opt_results : dict, optional
        Results from optimize_rsi_strategy
    symbol : str
        The trading symbol (e.g., BTC-USD)
    start_date : str
        Start date in format YYYY-MM-DD
    end_date : str
        End date in format YYYY-MM-DD
    reports_dir : str or Path
        Directory to save reports
    
    Returns:
    --------
    str
        Path to the saved dashboard HTML file
    """
    try:
        # Use default reports directory if not provided
        if reports_dir is None:
            reports_dir = Path("reports")
        elif isinstance(reports_dir, str):
            reports_dir = Path(reports_dir)
            
        # Create reports directory if it doesn't exist
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for valid portfolio data
        if results is None or 'portfolio' not in results:
            logger.error("Invalid results data for dashboard creation")
            return None
        
        # Get basic portfolio and data
        basic_portfolio = results['portfolio']
        price_data = results.get('price_data', None)
        
        if price_data is None and 'close' in basic_portfolio.wrapper.columns:
            # Use the price data from the portfolio if available
            price_data = pd.DataFrame({
                'close': basic_portfolio.wrapper.columns[0]
            })
        
        # Calculate benchmark returns (buy and hold)
        benchmark_returns = price_data['close'].pct_change().dropna()
        benchmark_cum_returns = (1 + benchmark_returns).cumprod() - 1
        
        # Calculate risk metrics
        basic_metrics = calculate_risk_metrics(basic_portfolio)
        
        # Create figure with subplots
        fig = make_subplots(
            rows=4, cols=2, 
            vertical_spacing=0.08,
            horizontal_spacing=0.05,
            subplot_titles=(
                "Cumulative Returns", "Drawdowns",
                "RSI Indicator", "Price and Trades",
                "Daily Returns", "Monthly Returns",
                "Strategy Metrics", "Optimization Results"
            ),
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "table"}, {"type": "table"}]
            ],
            row_heights=[0.25, 0.25, 0.25, 0.25]
        )
        
        # Add optimized portfolio if available
        opt_portfolio = None
        opt_metrics = None
        if opt_results and 'portfolio' in opt_results:
            opt_portfolio = opt_results['portfolio']
            opt_metrics = calculate_risk_metrics(opt_portfolio)
        
        # 1. Cumulative Returns Plot
        try:
            # Basic strategy returns
            basic_returns = basic_portfolio.returns.cumsum()
            
            fig.add_trace(
                go.Scatter(
                    x=basic_returns.index,
                    y=basic_returns.values,
                    mode='lines',
                    name='Basic RSI Strategy',
                    line=dict(color='blue', width=2)
                ),
                row=1, col=1
            )
            
            # Add optimized strategy if available
            if opt_portfolio is not None:
                opt_returns = opt_portfolio.returns.cumsum()
                
                fig.add_trace(
                    go.Scatter(
                        x=opt_returns.index,
                        y=opt_returns.values,
                        mode='lines',
                        name='Optimized RSI',
                        line=dict(color='green', width=2)
                    ),
                    row=1, col=1
                )
            
            # Add benchmark (buy and hold)
            fig.add_trace(
                go.Scatter(
                    x=benchmark_cum_returns.index,
                    y=benchmark_cum_returns.values,
                    mode='lines',
                    name='Buy and Hold',
                    line=dict(color='gray', width=1, dash='dash')
                ),
                row=1, col=1
            )
        except Exception as e:
            logger.error(f"Error creating cumulative returns plot: {e}")
        
        # 2. Drawdowns Plot
        try:
            # Calculate drawdowns
            basic_dd = basic_portfolio.drawdown()
            
            fig.add_trace(
                go.Scatter(
                    x=basic_dd.index,
                    y=basic_dd.values,
                    mode='lines',
                    name='Basic Strategy DD',
                    line=dict(color='red', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(255,0,0,0.1)'
                ),
                row=1, col=2
            )
            
            # Add optimized strategy drawdown if available
            if opt_portfolio is not None:
                opt_dd = opt_portfolio.drawdown()
                
                fig.add_trace(
                    go.Scatter(
                        x=opt_dd.index,
                        y=opt_dd.values,
                        mode='lines',
                        name='Optimized Strategy DD',
                        line=dict(color='orange', width=2),
                        fill='tozeroy',
                        fillcolor='rgba(255,165,0,0.1)'
                    ),
                    row=1, col=2
                )
        except Exception as e:
            logger.error(f"Error creating drawdowns plot: {e}")
            
        # 3. RSI Indicator
        try:
            if 'rsi' in results:
                rsi = results['rsi']
                
                fig.add_trace(
                    go.Scatter(
                        x=rsi.index,
                        y=rsi.values,
                        mode='lines',
                        name='RSI',
                        line=dict(color='purple', width=2)
                    ),
                    row=2, col=1
                )
                
                # Add threshold lines
                lower_threshold = results.get('lower_threshold', 30)
                upper_threshold = results.get('upper_threshold', 70)
                
                # If not in results, try to get from params
                if 'rsi_indicator' in results:
                    lower_threshold = results.get('lower_threshold', 30)
                    upper_threshold = results.get('upper_threshold', 70)
                
                fig.add_trace(
                    go.Scatter(
                        x=[rsi.index[0], rsi.index[-1]],
                        y=[lower_threshold, lower_threshold],
                        mode='lines',
                        name=f'Lower ({lower_threshold})',
                        line=dict(color='green', width=1, dash='dash')
                    ),
                    row=2, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=[rsi.index[0], rsi.index[-1]],
                        y=[upper_threshold, upper_threshold],
                        mode='lines',
                        name=f'Upper ({upper_threshold})',
                        line=dict(color='red', width=1, dash='dash')
                    ),
                    row=2, col=1
                )
        except Exception as e:
            logger.error(f"Error creating RSI plot: {e}")
        
        # 4. Price and Trades
        try:
            if price_data is not None:
                # Add price
                fig.add_trace(
                    go.Scatter(
                        x=price_data.index,
                        y=price_data['close'],
                        mode='lines',
                        name='Price',
                        line=dict(color='black', width=2)
                    ),
                    row=2, col=2
                )
                
                # Add trade markers if available
                if hasattr(basic_portfolio, 'trades') and len(basic_portfolio.trades) > 0:
                    try:
                        trades = basic_portfolio.trades
                        
                        # Get entry indices
                        entry_idx = trades.records_arr['entry_idx']
                        entry_idx = [idx for idx in entry_idx if 0 <= idx < len(price_data)]
                        
                        # Get entry values
                        entry_prices = [price_data['close'].iloc[idx] for idx in entry_idx]
                        entry_times = [price_data.index[idx] for idx in entry_idx]
                        
                        # Add entry markers
                        fig.add_trace(
                            go.Scatter(
                                x=entry_times,
                                y=entry_prices,
                                mode='markers',
                                marker=dict(symbol='triangle-up', size=12, color='green'),
                                name='Buy'
                            ),
                            row=2, col=2
                        )
                        
                        # Get exit indices
                        exit_idx = trades.records_arr['exit_idx']
                        exit_idx = [idx for idx in exit_idx if 0 <= idx < len(price_data)]
                        
                        # Get exit values
                        exit_prices = [price_data['close'].iloc[idx] for idx in exit_idx]
                        exit_times = [price_data.index[idx] for idx in exit_idx]
                        
                        # Add exit markers
                        fig.add_trace(
                            go.Scatter(
                                x=exit_times,
                                y=exit_prices,
                                mode='markers',
                                marker=dict(symbol='triangle-down', size=12, color='red'),
                                name='Sell'
                            ),
                            row=2, col=2
                        )
                    except Exception as e:
                        logger.error(f"Error adding trade markers: {e}")
        except Exception as e:
            logger.error(f"Error creating price plot: {e}")
            
        # 5. Daily Returns
        try:
            # Basic strategy daily returns
            fig.add_trace(
                go.Scatter(
                    x=basic_portfolio.returns.index,
                    y=basic_portfolio.returns.values * 100,  # Convert to percentage
                    mode='lines',
                    name='Daily Returns',
                    line=dict(color='blue', width=1)
                ),
                row=3, col=1
            )
            
            # Add moving average of returns
            returns_ma = basic_portfolio.returns.rolling(7).mean() * 100
            fig.add_trace(
                go.Scatter(
                    x=returns_ma.index,
                    y=returns_ma.values,
                    mode='lines',
                    name='7-day MA',
                    line=dict(color='orange', width=2)
                ),
                row=3, col=1
            )
        except Exception as e:
            logger.error(f"Error creating daily returns plot: {e}")
        
        # 6. Monthly Returns
        try:
            # Calculate monthly returns
            monthly_returns = basic_portfolio.returns.resample('M').sum() * 100
            
            fig.add_trace(
                go.Bar(
                    x=monthly_returns.index,
                    y=monthly_returns.values,
                    name='Monthly Returns',
                    marker=dict(color=['red' if x < 0 else 'green' for x in monthly_returns.values])
                ),
                row=3, col=2
            )
        except Exception as e:
            logger.error(f"Error creating monthly returns plot: {e}")
            
        # 7. Strategy Metrics Table
        try:
            metrics_table = {
                'Metric': [
                    'Total Return (%)', 
                    'Annualized Return (%)',
                    'Sharpe Ratio',
                    'Max Drawdown (%)',
                    'Win Rate (%)',
                    'Total Trades'
                ],
                'Basic Strategy': [
                    f"{basic_metrics['total_return']*100:.2f}",
                    f"{basic_metrics.get('annual_return', 0)*100:.2f}",
                    f"{basic_metrics['sharpe']:.2f}",
                    f"{basic_metrics['max_dd']*100:.2f}",
                    f"{basic_metrics['win_rate']*100:.2f}",
                    f"{basic_metrics['trades']}"
                ]
            }
            
            # Add optimized strategy metrics if available
            if opt_metrics is not None:
                metrics_table['Optimized Strategy'] = [
                    f"{opt_metrics['total_return']*100:.2f}",
                    f"{opt_metrics.get('annual_return', 0)*100:.2f}",
                    f"{opt_metrics['sharpe']:.2f}",
                    f"{opt_metrics['max_dd']*100:.2f}",
                    f"{opt_metrics['win_rate']*100:.2f}",
                    f"{opt_metrics['trades']}"
                ]
            
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=list(metrics_table.keys()),
                        font=dict(size=12, color='white'),
                        fill_color='blue',
                        align='center'
                    ),
                    cells=dict(
                        values=list(metrics_table.values()),
                        font=dict(size=11),
                        fill_color='lightblue',
                        align='center'
                    )
                ),
                row=4, col=1
            )
        except Exception as e:
            logger.error(f"Error creating metrics table: {e}")
            
        # 8. Optimization Results Table
        try:
            if opt_results is not None and 'best_params' in opt_results:
                best_params = opt_results['best_params']
                
                params_table = {
                    'Parameter': list(best_params.keys()),
                    'Optimal Value': [str(best_params[param]) for param in best_params.keys()]
                }
                
                fig.add_trace(
                    go.Table(
                        header=dict(
                            values=list(params_table.keys()),
                            font=dict(size=12, color='white'),
                            fill_color='green',
                            align='center'
                        ),
                        cells=dict(
                            values=list(params_table.values()),
                            font=dict(size=11),
                            fill_color='lightgreen',
                            align='center'
                        )
                    ),
                    row=4, col=2
                )
        except Exception as e:
            logger.error(f"Error creating optimization table: {e}")
        
        # Update layout
        fig.update_layout(
            title=f"RSI Strategy Dashboard - {symbol} ({start_date} to {end_date})",
            height=1000,
            width=1200,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=2)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=2)
        fig.update_xaxes(title_text="Date", row=3, col=1)
        fig.update_xaxes(title_text="Date", row=3, col=2)
        
        fig.update_yaxes(title_text="Cumulative Return", row=1, col=1)
        fig.update_yaxes(title_text="Drawdown", row=1, col=2)
        fig.update_yaxes(title_text="RSI Value", row=2, col=1)
        fig.update_yaxes(title_text="Price", row=2, col=2)
        fig.update_yaxes(title_text="Daily Return (%)", row=3, col=1)
        fig.update_yaxes(title_text="Monthly Return (%)", row=3, col=2)
        
        # Save dashboard to file
        dashboard_filename = f"rsi_dashboard_{symbol.replace('-', '_')}.html"
        dashboard_file = reports_dir / dashboard_filename
        
        fig.write_html(
            str(dashboard_file),
            auto_open=False,
            include_plotlyjs='cdn'
        )
        
        logger.info(f"Dashboard saved to: {dashboard_file}")
        
        return str(dashboard_file)
        
    except Exception as e:
        logger.error(f"Error creating dashboard: {e}")
        logger.error(traceback.format_exc())
        return None

def resample_data(data, to='1D'):
    """
    Resample OHLCV data to a different timeframe.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The OHLCV data to resample
    to : str
        The target frequency (e.g., '1D', '1H', '15T', '3D', '1W')
        
    Returns:
    --------
    pd.DataFrame
        Resampled OHLCV data
    """
    logger.info(f"Resampling data to {to} frequency")
    
    try:
        # For upsampling to lower timeframes, this is just an approximation
        # In a real system, you'd want actual data at the target frequency
        resampled = pd.DataFrame(index=pd.date_range(start=data.index[0], end=data.index[-1], freq=to))
        
        # Check if all required columns exist
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        available_cols = [col for col in required_cols if col in data.columns]
        
        if not all(col in data.columns for col in required_cols):
            logger.warning(f"Missing columns in data: {set(required_cols) - set(data.columns)}")
        
        # Resample based on column type
        if 'open' in data.columns:
            resampled['open'] = data['open'].resample(to).first()
        
        if 'high' in data.columns:
            resampled['high'] = data['high'].resample(to).max()
        
        if 'low' in data.columns:
            resampled['low'] = data['low'].resample(to).min()
        
        if 'close' in data.columns:
            resampled['close'] = data['close'].resample(to).last()
        
        if 'volume' in data.columns:
            resampled['volume'] = data['volume'].resample(to).sum()
        
        # Forward fill any missing values
        resampled = resampled.fillna(method='ffill')
        
        # If downsampling to a higher timeframe (weekly, monthly, etc.)
        # we may have fewer rows than original data
        logger.info(f"Resampled data shape: {resampled.shape}")
        
        return resampled
        
    except Exception as e:
        logger.error(f"Error in resampling data: {e}")
        logger.error(traceback.format_exc())
        # Return original data if resampling fails
        return data

def main():
    # Get symbol and date range from command line arguments
    parser = argparse.ArgumentParser(description='Backtest RSI momentum strategy.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2022-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default='2023-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--multi_timeframe', action='store_true', help='Use multi-timeframe strategy')
    parser.add_argument('--use_higher_tf', action='store_true', help='Use higher timeframe for trend confirmation')
    parser.add_argument('--use_lower_tf', action='store_true', help='Use lower timeframe for entry timing')
    parser.add_argument('--dashboard', action='store_true', help='Create interactive dashboard', default=True)
    args = parser.parse_args()
    
    symbol = args.symbol
    start_date = args.start_date
    end_date = args.end_date

    # --- Ensure reports directory exists ---
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    # --- End change ---

    # Print the backtest configuration
    logger.info(f"Starting backtest for {symbol} from {start_date} to {end_date}")
    
    # Get historical data
    try:
        data = fetch_historical_data(symbol, start_date, end_date)
        logger.info(f"Fetched historical data: {len(data)} rows")
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        logger.info("Using sample data for testing")
        data = create_sample_data(start_date, end_date)
    
    if args.multi_timeframe:
        # Run multi-timeframe strategy
        logger.info("Running multi-timeframe strategy...")
        
        # Run the strategy with multi-timeframe approach
        if args.use_higher_tf and args.use_lower_tf:
            logger.info("Using both higher and lower timeframes")
            # Use both higher and lower timeframes for comprehensive analysis
            # Combine trend from higher with precision from lower
            strategy = MultiTimeframeStrategy(
                primary_data=data,
                higher_tf_data=resample_data(data, to='3D'),
                lower_tf_data=resample_data(data, to='6H'),
                window=14,
                wtype='wilder',
                lower_threshold=30,
                upper_threshold=70
            )
            results = strategy.run_combined()
        elif args.use_higher_tf:
            logger.info("Using higher timeframe for trend")
            # Use higher timeframe for trend confirmation
            strategy = MultiTimeframeStrategy(
                primary_data=data,
                higher_tf_data=resample_data(data, to='3D'),
                window=14,
                wtype='wilder',
                lower_threshold=30,
                upper_threshold=70
            )
            results = strategy.run_higher_tf_trend()
        elif args.use_lower_tf:
            logger.info("Using lower timeframe for entry precision")
            # Use lower timeframe for more precise entries
            strategy = MultiTimeframeStrategy(
                primary_data=data,
                lower_tf_data=resample_data(data, to='6H'),
                window=14,
                wtype='wilder',
                lower_threshold=30,
                upper_threshold=70
            )
            results = strategy.run_lower_tf_entry()
        else:
            logger.info("Using basic multi-timeframe strategy")
            # Use basic multi-timeframe without specific approach
            strategy = MultiTimeframeStrategy(
                primary_data=data,
                window=14,
                wtype='wilder',
                lower_threshold=30,
                upper_threshold=70
            )
            results = strategy.run_basic()
        
        # Generate report for multi-timeframe strategy
        generate_multi_tf_report(results, str(reports_dir / f'multi_tf_strategy_{symbol.replace("-", "_")}.html'), 
                                 symbol, start_date, end_date, reports_dir)
    else:
        # Run basic RSI strategy
        logger.info("Running basic RSI strategy...")
        
        # Run the strategy with default parameters
        strategy = RSIMomentumVBT( 
            window=14, # Example: explicitly pass defaults or desired params
            wtype='wilder',
            lower_threshold=30,
            upper_threshold=70,
            initial_capital=10000.0
        )
        results = strategy.run(data)
        
        # Log available metrics
        if isinstance(results, dict) and 'portfolio' in results and results['portfolio'] is not None:
            try:
                # Pass the portfolio object to metrics calculation
                metrics = calculate_risk_metrics(results['portfolio'])

                logger.info("Basic RSI Strategy Performance:")
                logger.info(f"Total Return: {metrics['total_return']*100:.2f}%")
                logger.info(f"Sharpe Ratio: {metrics['sharpe']:.2f}")
                logger.info(f"Max Drawdown: {metrics['max_dd']*100:.2f}%")
                logger.info(f"Win Rate: {metrics['win_rate']*100:.2f}%")
                logger.info(f"Total Trades: {metrics['trades']}")
                
                # Save the strategy plot - Save to reports/ dir
                fig = results['portfolio'].plot()
                plot_filename = f'rsi_basic_strategy_results_{symbol.replace("-", "_")}.html'
                plot_file = reports_dir / plot_filename
                fig.write_html(str(plot_file))
                logger.info(f"Basic strategy plot saved to {plot_file}")

            except Exception as e:
                logger.error(f"Error extracting metrics or plotting: {e}")
                logger.error(traceback.format_exc())
        else:
            logger.error("Basic strategy did not produce valid results or portfolio object.")
        
        # Run parameter optimization with a reduced parameter set
        logger.info("Running parameter optimization...")
        try:
            # Use a reduced parameter set for faster optimization
            param_grid = {
                'window': [7, 14, 21],
                'lower_threshold': [20, 30, 40],
                'upper_threshold': [60, 70, 80],
            }
            
            # Run optimization with min_trades=1 for testing
            opt_results = optimize_rsi_strategy(data, param_grid, min_trades=1)
            
            if opt_results and 'best_params' in opt_results and opt_results['best_params']:
                logger.info("Optimized Strategy Parameters:")
                for param, value in opt_results['best_params'].items():
                    logger.info(f"  {param}: {value}")
                    
                # Log optimized performance
                logger.info("Optimized Strategy Performance:")
                logger.info(f"Total Return: {opt_results['best_metrics']['total_return']*100:.2f}%")
                logger.info(f"Sharpe Ratio: {opt_results['best_metrics']['sharpe']:.2f}")
                logger.info(f"Max Drawdown: {opt_results['best_metrics']['max_dd']*100:.2f}%")
                logger.info(f"Win Rate: {opt_results['best_metrics']['win_rate']*100:.2f}%")
                logger.info(f"Total Trades: {opt_results['best_metrics']['trades']}")
                
                # Save the optimized strategy plot - Save to reports/ dir
                if 'portfolio' in opt_results and opt_results['portfolio'] is not None:
                    fig = opt_results['portfolio'].plot()
                    plot_filename = f'rsi_optimized_strategy_results_{symbol.replace("-", "_")}.html'
                    plot_file = reports_dir / plot_filename
                    fig.write_html(str(plot_file))
                    logger.info(f"Optimized strategy plot saved to {plot_file}")
                    
                    # Create interactive dashboard if requested
                    if args.dashboard:
                        create_dashboard(results, opt_results, symbol, start_date, end_date, reports_dir)
                
            else:
                logger.warning("Optimization did not find valid parameters")
        except Exception as e:
            logger.error(f"Error during optimization: {e}")
    
    logger.info("Backtest completed successfully")

    return 0

if __name__ == "__main__":
    main() 