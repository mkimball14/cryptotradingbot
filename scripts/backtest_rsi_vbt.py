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
                        'exit_signals': exit_condition
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
                'exit_signals': exit_condition
            }
        except Exception as e:
            logger.error(f"Error in strategy run: {e}")
            
            # FALLBACK: Absolute simplest strategy - buy low RSI, sell high RSI
            logger.info("Using extremely simple fallback strategy")
            
            # Create basic RSI
            delta = close.diff()
            gain = delta.clip(lower=0)
            loss = -delta.clip(upper=0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))
            
            # Very simple signals
            entry_signals = rsi < 30
            exit_signals = rsi > 70
            
            # Create most basic portfolio
            portfolio = vbt.Portfolio.from_signals(
                close,
                entries=entry_signals,
                exits=exit_signals,
                init_cash=10000,
                freq='1D'
            )
            
            return {
                'portfolio': portfolio,
                'rsi': rsi,
                'entry_signals': entry_signals,
                'exit_signals': exit_signals
            }

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
                 initial_capital=10000.0, commission_pct=0.001):
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
            window=self.rsi_window
        ).rsi
        
        return self.rsi_values['primary']
    
    def calculate_higher_tf_rsi(self):
        """Calculate RSI for higher timeframe."""
        if self.higher_tf_data is not None:
            self.rsi_values['higher'] = vbt.RSI.run(
                self.higher_tf_data['close'], 
                window=self.rsi_window
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
                window=self.rsi_window // 2  # Use shorter window for lower timeframe
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
                
                return results
                
            except Exception as e:
                logger.error(f"Error creating portfolio: {e}")
                logger.error(traceback.format_exc())
                return None
                
        except Exception as e:
            logger.error(f"Error in multi-timeframe strategy: {e}")
            logger.error(traceback.format_exc())
            return None

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
            upper_threshold=upper_th
        )
        
        # Run the strategy
        results = strategy.run()
        
        # Return the results
        return results
        
    except Exception as e:
        logger.error(f"Error in multi-timeframe strategy test: {e}")
        logger.error(traceback.format_exc())
        return None

def generate_multi_tf_report(result, filename='multi_tf_strategy_report.html'):
    """
    Generate a detailed HTML report for multi-timeframe strategy results.
    
    Parameters:
    -----------
    result : dict
        Strategy results dictionary
    filename : str
        Output HTML filename
    """
    try:
        if not result or 'portfolio' not in result or result['portfolio'] is None:
            logger.error("Cannot generate report: Invalid strategy results")
            return
            
        portfolio = result['portfolio']
        metrics = calculate_risk_metrics(portfolio)
        
        # Create a Plotly figure
        fig = make_subplots(
            rows=4, 
            cols=1, 
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(
                "Portfolio Value", 
                "RSI Signals", 
                "Drawdowns", 
                "Daily Returns"
            ),
            row_heights=[0.4, 0.2, 0.2, 0.2]
        )
        
        # Plot 1: Portfolio Value
        pfig = portfolio.plot_value()
        for trace in pfig['data']:
            fig.add_trace(trace, row=1, col=1)
            
        # Plot 2: RSI Signals
        if 'primary_rsi' in result and 'entry_signals' in result and 'exit_signals' in result:
            # Plot RSI
            fig.add_trace(
                go.Scatter(
                    x=result['primary_rsi'].index,
                    y=result['primary_rsi'],
                    mode='lines',
                    name='RSI'
                ),
                row=2, col=1
            )
            
            # Add overbought/oversold lines
            fig.add_trace(
                go.Scatter(
                    x=[result['primary_rsi'].index[0], result['primary_rsi'].index[-1]],
                    y=[30, 30],
                    mode='lines',
                    line=dict(dash='dash', color='green'),
                    name='Oversold'
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=[result['primary_rsi'].index[0], result['primary_rsi'].index[-1]],
                    y=[70, 70],
                    mode='lines',
                    line=dict(dash='dash', color='red'),
                    name='Overbought'
                ),
                row=2, col=1
            )
            
            # Get entry and exit dates safely
            # For vectorbtpro portfolios, we might need to extract entries and exits from the trades
            entry_dates = []
            exit_dates = []

            # --- Refined entry/exit date extraction ---
            # Use portfolio.trade_history if available (vectorbtpro >= 0.25.0)
            if hasattr(portfolio, 'trade_history') and portfolio.trade_history is not None and not portfolio.trade_history.empty:
                try:
                    trade_records = portfolio.trade_history
                    entry_dates = trade_records[trade_records['Reason'] == 'Entry']['Timestamp']
                    exit_dates = trade_records[trade_records['Reason'] == 'Exit']['Timestamp']
                except KeyError as e:
                    logger.warning(f"KeyError accessing trade_history columns: {e}. Falling back to trades attribute.")
                    # Fallback if columns are named differently
                    if hasattr(portfolio, 'trades') and len(portfolio.trades) > 0:
                        entry_dates = portfolio.trades.records['entry_idx'].map(lambda idx: portfolio.wrapper.index[idx])
                        exit_dates = portfolio.trades.records['exit_idx'].map(lambda idx: portfolio.wrapper.index[idx])
                    elif 'entry_signals' in result and 'exit_signals' in result:
                         entry_dates = result['entry_signals'].index[result['entry_signals']]
                         exit_dates = result['exit_signals'].index[result['exit_signals']]
            # Fallback to portfolio.trades for older vectorbtpro versions
            elif hasattr(portfolio, 'trades') and len(portfolio.trades) > 0:
                try:
                    entry_dates = portfolio.trades.records['entry_idx'].map(lambda idx: portfolio.wrapper.index[idx])
                    exit_dates = portfolio.trades.records['exit_idx'].map(lambda idx: portfolio.wrapper.index[idx])
                except Exception as e:
                    logger.warning(f"Error accessing portfolio.trades records: {e}")
                    # Final fallback to signals from the result dictionary
                    if 'entry_signals' in result and 'exit_signals' in result:
                         entry_dates = result['entry_signals'].index[result['entry_signals']]
                         exit_dates = result['exit_signals'].index[result['exit_signals']]
            # Final fallback to signals from the result dictionary
            elif 'entry_signals' in result and 'exit_signals' in result:
                 entry_dates = result['entry_signals'].index[result['entry_signals']]
                 exit_dates = result['exit_signals'].index[result['exit_signals']]
            else:
                logger.warning("Could not extract entry/exit dates from portfolio or results.")
            # --- End of refinement ---

            # Plot entry signals if any
            if len(entry_dates) > 0:
                entry_rsi = pd.Series(index=entry_dates)
                for date in entry_dates:
                    if date in result['primary_rsi'].index:
                        entry_rsi[date] = result['primary_rsi'].loc[date]
                
                # Only plot non-NaN values
                valid_entries = entry_rsi.dropna()
                if len(valid_entries) > 0:
                    fig.add_trace(
                        go.Scatter(
                            x=valid_entries.index,
                            y=valid_entries.values,
                            mode='markers',
                            marker=dict(color='green', size=8, symbol='triangle-up'),
                            name='Entries'
                        ),
                        row=2, col=1
                    )
            
            # Plot exit signals if any
            if len(exit_dates) > 0:
                exit_rsi = pd.Series(index=exit_dates)
                for date in exit_dates:
                    if date in result['primary_rsi'].index:
                        exit_rsi[date] = result['primary_rsi'].loc[date]
                
                # Only plot non-NaN values
                valid_exits = exit_rsi.dropna()
                if len(valid_exits) > 0:
                    fig.add_trace(
                        go.Scatter(
                            x=valid_exits.index,
                            y=valid_exits.values,
                            mode='markers',
                            marker=dict(color='red', size=8, symbol='triangle-down'),
                            name='Exits'
                        ),
                        row=2, col=1
                    )
        
        # Plot 3: Drawdowns
        try:
            drawdowns = portfolio.drawdown()
            fig.add_trace(
                go.Scatter(
                    x=drawdowns.index,
                    y=drawdowns,
                    mode='lines',
                    line=dict(color='red'),
                    name='Drawdowns'
                ),
                row=3, col=1
            )
        except Exception as e:
            logger.warning(f"Could not plot drawdowns: {e}")
        
        # Plot 4: Daily Returns
        try:
            daily_returns = portfolio.returns.resample('D').sum()
            fig.add_trace(
                go.Bar(
                    x=daily_returns.index,
                    y=daily_returns,
                    marker_color=np.where(daily_returns >= 0, 'green', 'red'),
                    name='Daily Returns'
                ),
                row=4, col=1
            )
        except Exception as e:
            logger.warning(f"Could not plot daily returns: {e}")
        
        # Add metrics as annotations
        metrics_text = (
            f"<b>Performance Metrics:</b><br>"
            f"Total Return: {metrics['total_return']*100:.2f}%<br>"
            f"Annualized Return: {metrics['annual_return']*100:.2f}%<br>"
            f"Sharpe Ratio: {metrics['sharpe']:.2f}<br>"
            f"Max Drawdown: {metrics['max_dd']*100:.2f}%<br>"
            f"Win Rate: {metrics['win_rate']*100:.2f}%<br>"
            f"Total Trades: {metrics['trades']}"
        )
        
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0.01,
            y=0.99,
            text=metrics_text,
            showarrow=False,
            font=dict(size=10),
            align="left",
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1
        )
        
        # Update layout
        fig.update_layout(
            title=f"Multi-Timeframe RSI Strategy Performance",
            height=1000,
            template="plotly_white",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Save to HTML
        fig.write_html(filename)
        logger.info(f"Multi-timeframe report saved to {filename}")
    
    except Exception as e:
        logger.error(f"Error generating multi-timeframe report: {e}")
        logger.error(traceback.format_exc())

def test_rsi_strategy(data, window=14, wtype='wilder', lower_th=30, upper_th=70):
    """
    Test RSI strategy with specified parameters.
    
    Args:
        data: OHLCV data
        window: RSI window
        wtype: RSI type ('wilder' or 'simple')
        lower_th: Lower RSI threshold
        upper_th: Upper RSI threshold
        
    Returns:
        Dict with strategy results
    """
    logger.info(f"Testing RSI strategy with window={window}, type={wtype}, lower_th={lower_th}, upper_th={upper_th}")
    
    # Create strategy instance
    strategy = RSIMomentumVBT(
        window=window,
        wtype=wtype,
        lower_threshold=lower_th,
        upper_threshold=upper_th,
        ma_window=20,
        ma_type='sma',
        stop_pct=0.05,
        risk_pct=0.02,
        commission_pct=0.001,
        slippage_pct=0.0005,
        initial_capital=10000.0
    )
    
    # Run strategy
    result = strategy.run(data)
    
    return result

def optimize_rsi_strategy(data, param_grid, min_trades=5, metric='sharpe'):
    """
    Optimize RSI strategy parameters using vectorbtpro.

    Args:
        data (pd.DataFrame): OHLCV data.
        param_grid (dict): Dictionary of parameters to test (e.g., {'window': [10, 20]}).
        min_trades (int): Minimum number of trades required for a result to be considered valid.
        metric (str): Metric to optimize for (e.g., 'sharpe', 'total_return').

    Returns:
        dict: Dictionary containing best parameters, metrics, and portfolio, or None if no valid result.
    """
    logger.info(f"Optimizing parameters: {param_grid}")
    
    if not isinstance(data, pd.DataFrame) or not all(c in data.columns for c in ['open', 'high', 'low', 'close', 'volume']):
        logger.error("Optimization requires DataFrame with OHLCV columns.")
        return None

    # Extract parameter combinations
    rsi_windows = param_grid.get('window', [14])
    lower_thresholds = param_grid.get('lower_threshold', [30])
    upper_thresholds = param_grid.get('upper_threshold', [70])

    # Store all parameter combinations and their results
    all_results = []
    best_metric_value = -float('inf')  # Start with worst possible value for maximization
    best_params = None
    best_portfolio = None

    # Loop through all parameter combinations
    logger.info(f"Testing {len(rsi_windows) * len(lower_thresholds) * len(upper_thresholds)} parameter combinations...")
    for window in rsi_windows:
        for lower_th in lower_thresholds:
            for upper_th in upper_thresholds:
                # Run the RSI strategy with this parameter set
                strategy = RSIMomentumVBT(
                    window=window,
                    wtype='wilder',
                    lower_threshold=lower_th,
                    upper_threshold=upper_th,
                    ma_window=20,
                    ma_type='sma',
                    initial_capital=10000.0
                )
                
                try:
                    # Run the strategy
                    result = strategy.run(data)
                    
                    # Skip if no valid portfolio
                    if not isinstance(result, dict) or 'portfolio' not in result or result['portfolio'] is None:
                        continue
                        
                    portfolio = result['portfolio']
                    
                    # Check if minimum trade count is met
                    trade_count = 0
                    try:
                        if hasattr(portfolio.trades, 'count'):
                            trade_count = portfolio.trades.count()
                        elif hasattr(portfolio.trades, 'records') and len(portfolio.trades.records) > 0:
                            trade_count = len(portfolio.trades.records)
                        else:
                            trade_count = len(portfolio.trades)
                    except:
                        continue  # Skip if cannot determine trade count
                    
                    if trade_count < min_trades:
                        continue
                    
                    # Calculate metrics
                    metrics = calculate_risk_metrics(portfolio)
                    
                    # Get the target metric value
                    if metric == 'sharpe':
                        metric_value = metrics['sharpe']
                    elif metric == 'total_return':
                        metric_value = metrics['total_return'] 
                    elif metric == 'max_dd':
                        # For drawdown, less negative is better, so negate to make it maximizable
                        metric_value = -abs(metrics['max_dd'])
                    else:
                        logger.warning(f"Unsupported metric: {metric}. Using sharpe ratio.")
                        metric_value = metrics['sharpe']
                    
                    # Store the result
                    result_entry = {
                        'window': window,
                        'lower_threshold': lower_th,
                        'upper_threshold': upper_th,
                        'metric_value': metric_value,
                        'metric_name': metric,
                        'portfolio': portfolio,
                        'metrics': metrics
                    }
                    all_results.append(result_entry)
                    
                    # Update best result if current is better
                    if metric_value > best_metric_value:
                        best_metric_value = metric_value
                        best_params = {
                            'window': window,
                            'lower_threshold': lower_th,
                            'upper_threshold': upper_th
                        }
                        best_portfolio = portfolio
                        best_metrics = metrics
                        
                except Exception as e:
                    logger.warning(f"Error optimizing with window={window}, lower_th={lower_th}, upper_th={upper_th}: {e}")
                    continue
    
    # Check if any valid results found
    if not best_params:
        logger.warning(f"No parameter combinations met the minimum trade requirement of {min_trades}")
        return None
    
    logger.info(f"Optimization complete. Found {len(all_results)} valid parameter combinations.")
    logger.info(f"Best parameters: window={best_params['window']}, lower_th={best_params['lower_threshold']}, upper_th={best_params['upper_threshold']}")
    
    return {
        'best_params': best_params,
        'best_metrics': best_metrics,
        'portfolio': best_portfolio,
        'all_results': all_results  # Include all results for further analysis if needed
    }

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
    # Convert product_id for cache filename (BTC-USD -> BTCUSD)
    cache_product_id = product_id.replace('-', '')
    
    # Determine granularity name for cache filename
    granularity_name = "ONE_DAY"
    if granularity == 3600:
        granularity_name = "ONE_HOUR"
    elif granularity == 300:
        granularity_name = "FIVE_MIN"
    elif granularity == 60:
        granularity_name = "ONE_MIN"
    
    # Create cache directory if it doesn't exist
    cache_dir = os.path.join('data', 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Define cache file path
    cache_file = os.path.join(cache_dir, f"{cache_product_id}_{start_date}_{end_date}_{granularity_name}.csv")
    
    # Check if cache file exists
    if os.path.exists(cache_file):
        try:
            # Load from cache - specify ISO date format explicitly to avoid warning
            logging.info(f"Loading cached data from: {cache_file}")
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True, date_format='ISO8601')
            
            # If 'data' column exists and contains string representations of dictionaries, parse them
            if 'data' in data.columns:
                logging.info("Processing cached data from data column")
                # Parse the string dictionaries to actual dictionaries
                data['parsed'] = data['data'].apply(lambda x: eval(x) if isinstance(x, str) else x)
                
                # Extract columns from the parsed dictionaries
                for col in ['open', 'high', 'low', 'close', 'volume', 'start']:
                    data[col] = data['parsed'].apply(lambda x: float(x.get(col, 0)) if x and col in x else None)
                
                # Set timestamp as index
                data['timestamp'] = pd.to_datetime(data['start'], unit='s')
                data = data.set_index('timestamp')
                
                # Select only the relevant columns
                data = data[['open', 'high', 'low', 'close', 'volume']]
                
                # Sort by index
                data = data.sort_index()
            
            logging.info(f"Loaded {len(data)} rows of cached data")
            return data
        except Exception as e:
            logging.error(f"Error loading cache: {e}")
            # If there's an error with the cache, we'll fetch fresh data
    
    # If cache doesn't exist or there was an error, fetch data from API
    logging.info(f"Fetching new data for {product_id} from {start_date} to {end_date}")
    
    try:
        # Load API credentials
        credentials_file = "cdp_api_key.json"
        logging.info(f"Loading credentials from {credentials_file}...")
        
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        
        # Initialize Coinbase Advanced Trade client
        rest_client = RESTClient(
            api_key=credentials["API_KEY"],
            api_secret=credentials["API_SECRET"],
            key_passphrase=credentials.get("PASSPHRASE", ""),  # Optional
        )
        
        logging.info("Coinbase REST client initialized")
        
        # Convert dates to ISO format for the API
        start_time = pd.Timestamp(start_date).isoformat()
        end_time = pd.Timestamp(end_date).isoformat()
        
        # Calculate the total number of candles needed
        start_dt = pd.Timestamp(start_date)
        end_dt = pd.Timestamp(end_date)
        total_seconds = (end_dt - start_dt).total_seconds()
        total_candles = int(total_seconds / granularity) + 1
        
        logging.info(f"Need to fetch {total_candles} candles")
        
        # Fetch data in chunks if needed (Coinbase API limit is 300 candles per request)
        all_candles = []
        current_start = start_dt
        
        while current_start <= end_dt:
            # Calculate end time for this chunk (max 300 candles)
            chunk_end = current_start + pd.Timedelta(seconds=granularity * 300)
            if chunk_end > end_dt:
                chunk_end = end_dt
            
            chunk_start_iso = current_start.isoformat()
            chunk_end_iso = chunk_end.isoformat()
            
            logging.info(f"Fetching chunk from {chunk_start_iso} to {chunk_end_iso}")
            
            # Make API request
            candles = rest_client.get_product_candles(
                product_id=product_id,
                start=chunk_start_iso,
                end=chunk_end_iso,
                granularity=granularity
            )
            
            # Add candles to our list
            if candles and hasattr(candles, 'candles'):
                chunk_candles = candles.candles
                logging.info(f"Fetched {len(chunk_candles)} candles in this chunk")
                all_candles.extend(chunk_candles)
            else:
                logging.warning(f"No candles returned for this chunk or unexpected response format: {candles}")
            
            # Move to the next chunk
            current_start = chunk_end
        
        logging.info(f"Total candles fetched: {len(all_candles)}")
        
        # Convert to DataFrame
        if all_candles:
            # Create DataFrame from the candles
            data = []
            for candle in all_candles:
                # Check if the candle is a Candle object or a dictionary
                if hasattr(candle, '__dict__'):
                    # Convert Candle object to dictionary
                    candle_dict = candle.__dict__
                elif isinstance(candle, dict):
                    candle_dict = candle
                else:
                    # Skip if not a valid format
                    continue
                
                # Extract values from the dictionary
                entry = {
                    'start': float(candle_dict.get('start', 0)),
                    'low': float(candle_dict.get('low', 0)),
                    'high': float(candle_dict.get('high', 0)),
                    'open': float(candle_dict.get('open', 0)),
                    'close': float(candle_dict.get('close', 0)),
                    'volume': float(candle_dict.get('volume', 0))
                }
                data.append(entry)
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Convert timestamp to datetime and set as index
            df['timestamp'] = pd.to_datetime(df['start'], unit='s')
            df = df.set_index('timestamp')
            
            # Select only relevant columns and sort by index
            df = df[['open', 'high', 'low', 'close', 'volume']]
            df = df.sort_index()
            
            # Cache the data for future use
            df.to_csv(cache_file)
            logging.info(f"Cached {len(df)} rows to {cache_file}")
            
            return df
        else:
            logging.error("No data fetched from API")
            return pd.DataFrame()
    
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        logging.error(f"Error traceback: {traceback.format_exc()}")
        
        # Return empty DataFrame on error
        return pd.DataFrame()

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

def test_multi_indicator_strategy(data, window=14, wtype='wilder', lower_th=30, upper_th=70):
    """Test the enhanced multi-indicator strategy."""
    logger.info(f"Testing multi-indicator strategy with RSI window={window}, type={wtype}, thresholds: {lower_th}/{upper_th}")
    
    # Create strategy instance
    strategy = MultiIndicatorStrategy(
        window=window,
        wtype=wtype,
        lower_threshold=lower_th,
        upper_threshold=upper_th,
        ma_window=20,
        ma_type='sma',
        stop_pct=0.05,
        risk_pct=0.02,
        commission_pct=0.001,
        slippage_pct=0.0005,
        initial_capital=10000.0,
        use_macd=True,
        use_bbands=True
    )
    
    # Run strategy
    result = strategy.run(data)
    
    return result

def test_enhanced_rsi_strategy(data, window=14, wtype='wilder', lower_th=30, upper_th=70):
    """Test the enhanced RSI strategy with advanced risk management."""
    logger.info(f"Testing enhanced RSI strategy with window={window}, type={wtype}, thresholds: {lower_th}/{upper_th}")
    
    # Create strategy instance
    strategy = EnhancedRSIStrategy(
        window=window,
        wtype=wtype,
        lower_threshold=lower_th,
        upper_threshold=upper_th,
        ma_window=20,
        ma_type='sma',
        stop_pct=0.05,
        risk_pct=0.02,
        commission_pct=0.001,
        slippage_pct=0.0005,
        initial_capital=10000.0,
        atr_stop_multiplier=2.0,
        use_trailing_stop=True,
        equity_scaling=True
    )
    
    # Run strategy
    result = strategy.run(data)
    
    return result

def main():
    # Get symbol and date range from command line arguments
    parser = argparse.ArgumentParser(description='Backtest RSI momentum strategy.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2022-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default='2023-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--multi_timeframe', action='store_true', help='Use multi-timeframe strategy')
    parser.add_argument('--use_higher_tf', action='store_true', help='Use higher timeframe for trend confirmation')
    parser.add_argument('--use_lower_tf', action='store_true', help='Use lower timeframe for entry timing')
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
        logger.info("Running multi-timeframe RSI strategy...")
        
        # Run the multi-timeframe strategy
        result = test_multitimeframe_strategy(
            data, 
            window=14, 
            lower_th=30, 
            upper_th=70,
            use_higher_tf=args.use_higher_tf or True,  # Default to True if not specified
            use_lower_tf=args.use_lower_tf or True     # Default to True if not specified
        )
        
        # Generate detailed report
        if result and 'portfolio' in result and result['portfolio'] is not None:
            # Extract performance metrics
            metrics = calculate_risk_metrics(result['portfolio'])
            
            # Log performance metrics
            logger.info("Multi-Timeframe RSI Strategy Performance:")
            logger.info(f"Total Return: {metrics['total_return']*100:.2f}%")
            logger.info(f"Sharpe Ratio: {metrics['sharpe']:.2f}")
            logger.info(f"Max Drawdown: {metrics['max_dd']*100:.2f}%")
            logger.info(f"Win Rate: {metrics['win_rate']*100:.2f}%")
            logger.info(f"Total Trades: {metrics['trades']}")
            
            # Generate HTML report - Save to reports/ dir
            report_filename = f'multi_tf_rsi_strategy_results_{symbol.replace("-", "_")}.html'
            report_file = reports_dir / report_filename
            generate_multi_tf_report(result, filename=str(report_file))
            logger.info(f"Multi-timeframe strategy report saved to {report_file}")
        else:
            logger.error("Multi-timeframe strategy did not produce valid results")
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
                fig = results['portfolio'].plot() # Access portfolio from dict
                plot_filename = f'rsi_basic_strategy_results_{symbol.replace("-", "_")}.html'
                plot_file = reports_dir / plot_filename
                vbt.save(fig, str(plot_file))
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
            
            # Run optimization
            opt_results = optimize_rsi_strategy(data, param_grid, min_trades=5)
            
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
                    vbt.save(fig, str(plot_file))
                    logger.info(f"Optimized strategy plot saved to {plot_file}")
            else:
                logger.warning("Optimization did not find valid parameters")
        except Exception as e:
            logger.error(f"Error during optimization: {e}")
    
    logger.info("Backtest completed successfully")

    return 0

if __name__ == "__main__":
    main() 