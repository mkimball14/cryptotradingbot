import vectorbtpro as vbt
import numpy as np
import pandas as pd
import sys
import os
import logging
from pathlib import Path
import argparse
from datetime import datetime
import itertools
from collections import defaultdict
import ta
import traceback

# --- Basic Setup ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Configure pandas to avoid the FutureWarning about downcasting
pd.set_option('future.no_silent_downcasting', True)

# --- Import centralized data fetcher ---
try:
    from data.data_fetcher import fetch_historical_data, get_granularity_str, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    logger = logging.getLogger(__name__)
    logger.info("Successfully imported data_fetcher.")
except ImportError as e:
    print(f"WARNING: Could not import data_fetcher: {e}. Main block requires it.")
    def fetch_historical_data(*args, **kwargs):
        print("ERROR: fetch_historical_data is not available.")
        return None
    GRANULARITY_MAP_SECONDS = {'1h': 3600, '1d': 86400}
    def get_vbt_freq_str(*args, **kwargs): return "1h"

# ==============================================================================
# Factor Indicator Functions (Plain Python/Numba)
# ==============================================================================

def create_volatility_regime_indicator(close, lookback_window, vol_filter_window, volatility_threshold):
    """Calculates the volatility regime signal."""
    returns = close.pct_change()
    vol = returns.vbt.rolling_std(window=lookback_window, minp=lookback_window // 2)
    vol_ma = vol.vbt.rolling_mean(window=vol_filter_window, minp=vol_filter_window // 2)
    vol_ma_safe = vol_ma.replace(0, np.nan).ffill().bfill()
    vol_ratio = (vol / vol_ma_safe).fillna(1.0)
    
    # Print diagnostics about vol_ratio to help debug
    print(f"Volatility ratio stats - min: {vol_ratio.min():.4f}, max: {vol_ratio.max():.4f}, mean: {vol_ratio.mean():.4f}")
    print(f"Volatility threshold: {volatility_threshold}")
    
    # Count periods where vol_ratio is below threshold (volatility compression)
    compressed_count = (vol_ratio < volatility_threshold).sum()
    print(f"Volatility compression periods: {compressed_count}/{len(vol_ratio)} ({compressed_count/len(vol_ratio)*100:.2f}%)")
    
    # More sensitive detection - use a higher threshold if no compressions detected with current threshold
    if compressed_count == 0 and volatility_threshold < 0.9:
        adjusted_threshold = min(volatility_threshold * 1.5, 0.9)
        print(f"No compressions detected! Adjusting threshold to {adjusted_threshold:.4f}")
        vol_compressed = vol_ratio < adjusted_threshold
    else:
        vol_compressed = vol_ratio < volatility_threshold
    
    vol_expansion = vol_ratio.diff().fillna(0) > 0
    
    # Fix: Completely restructure to avoid the warning
    vol_compressed_bool = vol_compressed.astype(bool)
    vol_compressed_shifted = vol_compressed_bool.shift(1)
    # Fill NaN values after shifting with False
    vol_compressed_shifted = vol_compressed_shifted.fillna(False)
    vol_signal = vol_compressed_shifted & vol_expansion
    
    return vol_signal

def create_consolidation_breakout_indicator(high, low, close, lookback_window):
    """Calculates consolidation breakout signals."""
    hl_range = (high - low) / close.replace(0, np.nan)
    hl_range_ma = hl_range.vbt.rolling_mean(window=lookback_window, minp=lookback_window // 2)
    is_consolidating = hl_range < hl_range_ma * 0.8
    upper_level = high.vbt.rolling_max(window=lookback_window, minp=lookback_window // 2)
    lower_level = low.vbt.rolling_min(window=lookback_window, minp=lookback_window // 2)
    upper_level_shifted = upper_level.shift(1).bfill()
    lower_level_shifted = lower_level.shift(1).bfill()
    
    # Fix: Completely restructure to avoid the warning
    is_consolidating_bool = is_consolidating.astype(bool)
    is_consolidating_shifted = is_consolidating_bool.shift(1)
    # Fill NaN values after shifting with False 
    is_consolidating_shifted = is_consolidating_shifted.fillna(False)
    
    breakout_up = (close > upper_level_shifted) & is_consolidating_shifted
    breakout_down = (close < lower_level_shifted) & is_consolidating_shifted
    return breakout_up, breakout_down

def create_volume_divergence_indicator(volume, lookback_window, breakout_up, breakout_down, 
                               volume_threshold=1.1, volume_threshold_short=1.05, volume_roc_threshold=0.1,
                               is_trending=None, is_ranging=None):
    """Calculates volume confirmation signals based on pre-calculated breakouts.
    
    Args:
        volume: Series of volume data
        lookback_window: Window for lookback period
        breakout_up: Boolean series indicating upward breakouts
        breakout_down: Boolean series indicating downward breakouts
        volume_threshold: Main volume ratio threshold
        volume_threshold_short: Short-term volume ratio threshold
        volume_roc_threshold: Rate of change threshold for volume
        is_trending: Boolean series indicating trending market periods
        is_ranging: Boolean series indicating ranging market periods
    """
    # Get shorter window MA for faster reaction to volume changes
    volume_short_ma = volume.vbt.rolling_mean(window=lookback_window//2, minp=max(3, lookback_window//4))
    volume_ma = volume.vbt.rolling_mean(window=lookback_window, minp=lookback_window // 2)
    volume_ma_safe = volume_ma.replace(0, np.nan).ffill().bfill()
    
    # Calculate volume ratios against different lookback periods
    vol_ratio_vol = (volume / volume_ma_safe).fillna(1.0)
    vol_ratio_short = (volume / volume_short_ma.replace(0, np.nan).ffill().bfill()).fillna(1.0)
    
    # Print volume ratio statistics for debugging
    print(f"Volume ratio stats - min: {vol_ratio_vol.min():.4f}, max: {vol_ratio_vol.max():.4f}, mean: {vol_ratio_vol.mean():.4f}")
    print(f"Short-term volume ratio - min: {vol_ratio_short.min():.4f}, max: {vol_ratio_short.max():.4f}, mean: {vol_ratio_short.mean():.4f}")
    print(f"Base volume thresholds - main: {volume_threshold}, short-term: {volume_threshold_short}, ROC: {volume_roc_threshold}")
    
    # Apply market regime-based threshold adjustments if regime data is provided
    adapted_volume_threshold = pd.Series(volume_threshold, index=volume.index)
    adapted_volume_threshold_short = pd.Series(volume_threshold_short, index=volume.index)
    adapted_roc_threshold = pd.Series(volume_roc_threshold, index=volume.index)
    
    if is_trending is not None and is_ranging is not None:
        # Make volume thresholds more strict during trending periods (reduce false signals)
        trending_adjustment = 1.2  # Increase threshold by 20% during trends
        ranging_adjustment = 0.85  # Decrease threshold by 15% during ranges
        
        # Apply adjustments based on market regimes
        adapted_volume_threshold[is_trending] *= trending_adjustment
        adapted_volume_threshold[is_ranging] *= ranging_adjustment
        
        adapted_volume_threshold_short[is_trending] *= trending_adjustment
        adapted_volume_threshold_short[is_ranging] *= ranging_adjustment
        
        # Adjust ROC threshold as well
        adapted_roc_threshold[is_trending] *= 1.1
        adapted_roc_threshold[is_ranging] *= 0.9
        
        print(f"Market regime adjustments - Trending: +20%, Ranging: -15%")
        print(f"Adjusted volume threshold range: {adapted_volume_threshold.min():.4f} to {adapted_volume_threshold.max():.4f}")
    
    # Count periods where volume ratio exceeds threshold
    high_volume_count = (vol_ratio_vol > adapted_volume_threshold).sum()
    high_volume_short_count = (vol_ratio_short > adapted_volume_threshold_short).sum()
    print(f"High volume periods: {high_volume_count}/{len(vol_ratio_vol)} ({high_volume_count/len(vol_ratio_vol)*100:.2f}%)")
    print(f"High short-term volume periods: {high_volume_short_count}/{len(vol_ratio_short)} ({high_volume_short_count/len(vol_ratio_short)*100:.2f}%)")
    
    # Enhanced volume detection - consider multiple volume indicators
    # 1. Relative volume compared to lookback period
    # 2. Relative volume compared to short-term lookback
    # 3. Rate of change in volume
    # 4. Consecutive increasing volume bars
    
    # Calculate volume rate of change
    volume_roc = volume.pct_change(3).fillna(0)  # 3-period rate of change
    volume_increasing = volume_roc > adapted_roc_threshold  # ROC threshold
    
    # Detect consecutive increasing volume (2 or more bars)
    vol_change = volume.diff().fillna(0)
    consecutive_increasing = (vol_change > 0) & (vol_change.shift(1) > 0)
    
    # More sensitive volume confirmation using multiple indicators
    volume_confirms_up = (
        (vol_ratio_vol > adapted_volume_threshold) | 
        (vol_ratio_short > adapted_volume_threshold_short) | 
        volume_increasing | 
        consecutive_increasing
    ) & breakout_up
    
    volume_confirms_down = (
        (vol_ratio_vol > adapted_volume_threshold) | 
        (vol_ratio_short > adapted_volume_threshold_short) | 
        volume_increasing | 
        consecutive_increasing
    ) & breakout_down
    
    return volume_confirms_up, volume_confirms_down

def create_market_microstructure_indicator(open, high, low, close):
    """Calculates market microstructure signals (candle shadows)."""
    upper_shadow = high - np.maximum(open, close)
    lower_shadow = np.minimum(open, close) - low
    hl_range_nonzero = (high - low).replace(0, np.nan)
    shadow_ratio = ((upper_shadow - lower_shadow) / hl_range_nonzero).fillna(0)
    buying_pressure = shadow_ratio < -0.5
    selling_pressure = shadow_ratio > 0.5
    return buying_pressure, selling_pressure

def create_regime_specific_exits(close, high, low, volume, 
                             long_entries, short_entries,
                             is_trending, is_ranging,
                             volume_threshold, volume_threshold_short,
                             lookback_window,
                             trending_tp_multiplier, trending_sl_multiplier,
                             ranging_tp_multiplier, ranging_sl_multiplier,
                             max_bars_exit):
    """
    Generate exit signals based on market conditions.
    
    This function creates exit signals for both long and short positions based on:
    1. Market regime (trending vs ranging)
    2. Volatility-based stops and targets
    3. Volume-based exhaustion signals
    4. Time-based exits
    
    Args:
        close: Series of closing prices
        high: Series of high prices
        low: Series of low prices
        volume: Series of volume data
        long_entries: Series of boolean long entry signals
        short_entries: Series of boolean short entry signals
        is_trending: Series of boolean trending market signals
        is_ranging: Series of boolean ranging market signals
        volume_threshold: Volume threshold for detecting breakouts
        volume_threshold_short: Short-term volume threshold
        lookback_window: Window for lookback calculations
        trending_tp_multiplier: ATR multiplier for take profit in trending markets
        trending_sl_multiplier: ATR multiplier for stop loss in trending markets
        ranging_tp_multiplier: ATR multiplier for take profit in ranging markets
        ranging_sl_multiplier: ATR multiplier for stop loss in ranging markets
        max_bars_exit: Maximum number of bars to hold a position
        
    Returns:
        Tuple of (long_exits, short_exits)
    """
    # Initialize exit signals
    long_exits = pd.Series(False, index=close.index)
    short_exits = pd.Series(False, index=close.index)
    
    # Calculate ATR for volatility-based exits
    atr = vbt.ATR.run(high, low, close, window=14).atr.bfill()
    
    # Initialize position tracking
    in_long_position = pd.Series(False, index=close.index)
    in_short_position = pd.Series(False, index=close.index)
    position_entry_price = pd.Series(0.0, index=close.index)
    position_bars = pd.Series(0, index=close.index)
    
    # Process each bar
    for i in range(1, len(close)):
        # Skip first few bars due to lookback requirements
        if i < lookback_window:
            continue
            
        # Update position tracking
        if long_entries.iloc[i-1]:
            in_long_position.iloc[i] = True
            position_entry_price.iloc[i] = close.iloc[i-1]
            position_bars.iloc[i] = 1
        elif short_entries.iloc[i-1]:
            in_short_position.iloc[i] = True
            position_entry_price.iloc[i] = close.iloc[i-1]
            position_bars.iloc[i] = 1
        elif in_long_position.iloc[i-1] and not long_exits.iloc[i-1]:
            in_long_position.iloc[i] = True
            position_entry_price.iloc[i] = position_entry_price.iloc[i-1]
            position_bars.iloc[i] = position_bars.iloc[i-1] + 1
        elif in_short_position.iloc[i-1] and not short_exits.iloc[i-1]:
            in_short_position.iloc[i] = True
            position_entry_price.iloc[i] = position_entry_price.iloc[i-1]
            position_bars.iloc[i] = position_bars.iloc[i-1] + 1
            
        # Skip if not in position
        if not in_long_position.iloc[i] and not in_short_position.iloc[i]:
            continue
            
        # Get current ATR and regime state
        current_atr = atr.iloc[i]
        current_trending = is_trending.iloc[i]
        current_ranging = is_ranging.iloc[i]
        
        # Calculate regime-specific exit levels
        if in_long_position.iloc[i]:
            entry_price = position_entry_price.iloc[i]
            
            # Calculate take profit and stop loss levels based on market regime
            if current_trending:
                take_profit = entry_price + (current_atr * trending_tp_multiplier)
                stop_loss = entry_price - (current_atr * trending_sl_multiplier)
            else:  # ranging market
                take_profit = entry_price + (current_atr * ranging_tp_multiplier)
                stop_loss = entry_price - (current_atr * ranging_sl_multiplier)
                
            # Check for price-based exits
            if close.iloc[i] >= take_profit or close.iloc[i] <= stop_loss:
                long_exits.iloc[i] = True
                
            # Check for volume exhaustion in long position (declining volume after surge)
            volume_ma = volume.iloc[i-lookback_window:i].mean()
            recent_volume_ma = volume.iloc[i-5:i].mean()
            
            # Volume exhaustion exit for longs: volume drying up after position entry
            if current_trending and recent_volume_ma < volume_ma * 0.7:
                long_exits.iloc[i] = True
                
            # Faster exits in ranging markets if the trade isn't working quickly
            if current_ranging and close.iloc[i] < entry_price and position_bars.iloc[i] > 3:
                long_exits.iloc[i] = True
                
        # Similar logic for short positions
        if in_short_position.iloc[i]:
            entry_price = position_entry_price.iloc[i]
            
            # Calculate take profit and stop loss levels based on market regime
            if current_trending:
                take_profit = entry_price - (current_atr * trending_tp_multiplier)
                stop_loss = entry_price + (current_atr * trending_sl_multiplier)
            else:  # ranging market
                take_profit = entry_price - (current_atr * ranging_tp_multiplier)
                stop_loss = entry_price + (current_atr * ranging_sl_multiplier)
                
            # Check for price-based exits
            if close.iloc[i] <= take_profit or close.iloc[i] >= stop_loss:
                short_exits.iloc[i] = True
                
            # Check for volume exhaustion in short position (declining volume after surge)
            volume_ma = volume.iloc[i-lookback_window:i].mean()
            recent_volume_ma = volume.iloc[i-5:i].mean()
            
            # Volume exhaustion exit for shorts: volume drying up after position entry
            if current_trending and recent_volume_ma < volume_ma * 0.7:
                short_exits.iloc[i] = True
                
            # Faster exits in ranging markets if the trade isn't working quickly
            if current_ranging and close.iloc[i] > entry_price and position_bars.iloc[i] > 3:
                short_exits.iloc[i] = True
        
        # Time-based exit - max holding period
        if (in_long_position.iloc[i] and position_bars.iloc[i] >= max_bars_exit):
            long_exits.iloc[i] = True
        if (in_short_position.iloc[i] and position_bars.iloc[i] >= max_bars_exit):
            short_exits.iloc[i] = True
            
    return long_exits, short_exits

def create_rsi_signals(close, window=14, overbought=70, oversold=30, smoothing=2):
    """
    Create RSI-based signals.
    
    Args:
        close: Series of closing prices
        window: RSI calculation window
        overbought: Overbought threshold
        oversold: Oversold threshold
        smoothing: Signal smoothing period
        
    Returns:
        tuple: (long_signals, short_signals)
    """
    try:
        from app.strategies.indicators.technical import calculate_rsi
        
        # Calculate RSI
        rsi = calculate_rsi(pd.DataFrame({'close': close}), period=window)
        
        # Generate signals
        long_signal = rsi < oversold
        short_signal = rsi > overbought
        
        # Apply smoothing if needed
        if smoothing > 1:
            long_signal = long_signal.rolling(window=smoothing).sum() > 0
            short_signal = short_signal.rolling(window=smoothing).sum() > 0
            
        return long_signal, short_signal
    except Exception as e:
        print(f"Error generating RSI signals: {e}")
        return pd.Series(False, index=close.index), pd.Series(False, index=close.index)

def create_bollinger_signals(close, window=20, std_dev=2.0, smoothing=2):
    """
    Create Bollinger Bands signals.
    
    Args:
        close: Series of closing prices
        window: Bollinger Bands window
        std_dev: Standard deviation multiplier
        smoothing: Signal smoothing period
        
    Returns:
        tuple: (long_signals, short_signals)
    """
    try:
        # Calculate Bollinger Bands
        ma = close.rolling(window=window).mean()
        std = close.rolling(window=window).std()
        
        upper_band = ma + (std * std_dev)
        lower_band = ma - (std * std_dev)
        
        # Generate signals
        long_signal = close < lower_band
        short_signal = close > upper_band
        
        # Apply smoothing if needed
        if smoothing > 1:
            long_signal = long_signal.rolling(window=smoothing).sum() > 0
            short_signal = short_signal.rolling(window=smoothing).sum() > 0
            
        return long_signal, short_signal
    except Exception as e:
        print(f"Error generating Bollinger Bands signals: {e}")
        return pd.Series(False, index=close.index), pd.Series(False, index=close.index)

def create_macd_signals(close, fast_period=12, slow_period=26, signal_period=9, smoothing=2):
    """
    Create MACD signals.
    
    Args:
        close: Series of closing prices
        fast_period: Fast EMA period
        slow_period: Slow EMA period
        signal_period: Signal line period
        smoothing: Signal smoothing period
        
    Returns:
        tuple: (long_signals, short_signals)
    """
    try:
        # Calculate MACD components
        fast_ema = close.ewm(span=fast_period, adjust=False).mean()
        slow_ema = close.ewm(span=slow_period, adjust=False).mean()
        
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        
        # Generate signals
        long_signal = macd_line > signal_line
        short_signal = macd_line < signal_line
        
        # Apply smoothing if needed
        if smoothing > 1:
            long_signal = long_signal.rolling(window=smoothing).sum() >= smoothing
            short_signal = short_signal.rolling(window=smoothing).sum() >= smoothing
            
        return long_signal, short_signal
    except Exception as e:
        print(f"Error generating MACD signals: {e}")
        return pd.Series(False, index=close.index), pd.Series(False, index=close.index)

# ==============================================================================
# Strategy Class with Simplified Interface to Match Backtest Expectations
# ==============================================================================
class EdgeMultiFactorStrategy:
    """
    EdgeMultiFactorStrategy is a multi-factor strategy that combines RSI, Bollinger Bands,
    MACD and Volume Divergence to generate buy and sell signals for trading.
    """
    def __init__(self, **kwargs):
        """
        Initialize the strategy with parameters.
        
        Args:
            **kwargs: Keyword arguments to override default parameters.
        """
        # Basic configuration params
        self.symbol = kwargs.get('symbol', 'BTCUSDT')
        self.timeframe = kwargs.get('timeframe', '1h')
        self.lookback_window = kwargs.get('lookback_window', 10)
        self.signal_threshold = kwargs.get('signal_threshold', 0.2)
        self.signal_smoothing = kwargs.get('signal_smoothing', 2)
        
        # Factor weights
        self.trend_weight = kwargs.get('trend_weight', 0.25)  # For RSI
        self.momentum_weight = kwargs.get('momentum_weight', 0.25)  # For BBands
        self.mean_reversion_weight = kwargs.get('mean_reversion_weight', 0.25)  # For MACD
        self.volume_weight = kwargs.get('volume_weight', 0.25)  # For Volume Divergence
        
        # Volume parameters
        self.volume_threshold = kwargs.get('volume_threshold', 1.5)
        self.volume_threshold_short = kwargs.get('volume_threshold_short', 1.2)
        
        # RSI parameters
        self.rsi_period = kwargs.get('rsi_period', 14)
        
        # Bollinger Bands parameters
        self.bbands_period = kwargs.get('bbands_period', 20)
        self.bbands_dev = kwargs.get('bbands_dev', 2.0)
        
        # MACD parameters
        self.fast_ma_period = kwargs.get('fast_ma_period', 12)
        self.slow_ma_period = kwargs.get('slow_ma_period', 26)
        self.macd_signal = kwargs.get('macd_signal', 9)
        
        # Regime adaptation parameters
        self.use_regime_filter = kwargs.get('use_regime_filter', True)
        self.adx_threshold = kwargs.get('adx_threshold', 25)
        self.ranging_signal_discount = kwargs.get('ranging_signal_discount', 0.5)
        self.ranging_market_adjustment = kwargs.get('ranging_market_adjustment', True)
        self.disable_shorts_in_uptrend = kwargs.get('disable_shorts_in_uptrend', False)
        self.disable_longs_in_downtrend = kwargs.get('disable_longs_in_downtrend', False)
        self.ranging_factor = kwargs.get('ranging_factor', 0.5)  # Factor to reduce signal strength in ranging markets
        
        # Exit strategy parameters
        self.use_regime_exits = kwargs.get('use_regime_exits', True)
        self.trending_tp_multiplier = kwargs.get('trending_tp_multiplier', 3.0)
        self.trending_sl_multiplier = kwargs.get('trending_sl_multiplier', 2.0)
        self.ranging_tp_multiplier = kwargs.get('ranging_tp_multiplier', 1.5)
        self.ranging_sl_multiplier = kwargs.get('ranging_sl_multiplier', 1.0)
        self.max_bars_exit = kwargs.get('max_bars_exit', 20)
        
        # Position sizing
        self.base_capital = kwargs.get('base_capital', 10000.0)
        self.risk_per_trade = kwargs.get('risk_per_trade', 0.01)  # 1% risk per trade
        self.commission_pct = kwargs.get('commission_pct', 0.001)  # 0.1% trading fee
        self.slippage_pct = kwargs.get('slippage_pct', 0.0005)    # 0.05% slippage
        
        # Data storage
        self._data = None

    def generate_signals(self, data):
        """
        Generate signals based on combined factors
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            tuple: (long_entries, short_entries, is_trending, is_ranging)
                - long_entries (pd.Series): Boolean series of long entry signals
                - short_entries (pd.Series): Boolean series of short entry signals
                - is_trending (pd.Series): Boolean series indicating trending market
                - is_ranging (pd.Series): Boolean series indicating ranging market
        """
        # Step 1: Calculate individual factor signals
        signals = self.calculate_factor_signals(data)
        
        # Step 2: Apply weights to create combined signal
        combined_signal = self.combine_factor_signals(signals)
        
        # Step 3: Generate entry signals based on thresholds
        entries = pd.Series(0, index=data.index)
        
        # Long signals when combined value exceeds threshold
        long_entries = combined_signal > self.signal_threshold
        
        # Short signals when combined value is below negative threshold
        short_entries = combined_signal < -self.signal_threshold
        
        # Step 4: Detect market regime
        is_trending = self.detect_market_regime(data)
        is_ranging = ~is_trending
        
        # Apply regime filter if enabled
        if self.use_regime_filter:
            # In ranging markets, reduce signal strength or disable certain types of trades
            if self.ranging_market_adjustment:
                # Reduce signal strength in ranging markets
                combined_signal = combined_signal.where(~is_ranging, combined_signal * self.ranging_factor)
                
                # Recalculate entries with adjusted signals
                long_entries = combined_signal > self.signal_threshold
                short_entries = combined_signal < -self.signal_threshold
            
            # Optional: Completely disable trades in certain regimes
            if self.disable_shorts_in_uptrend or self.disable_longs_in_downtrend:
                trend_direction = self.detect_trend_direction(data)
                
                # Disable shorts in uptrend if configured
                if self.disable_shorts_in_uptrend:
                    is_uptrend = trend_direction > 0
                    short_entries = short_entries & ~is_uptrend
                
                # Disable longs in downtrend if configured
                if self.disable_longs_in_downtrend:
                    is_downtrend = trend_direction < 0
                    long_entries = long_entries & ~is_downtrend
        
        # Convert to unique signals (avoid multiple entries while in position)
        long_entries = self.process_signals_to_unique_entries_bool(long_entries)
        short_entries = self.process_signals_to_unique_entries_bool(short_entries)
        
        return long_entries, short_entries, is_trending, is_ranging
        
    def calculate_target_percent(self, price_data, risk_fraction=0.01, atr_window=14, atr_multiple_stop=2.0):
        """
        Calculates the target percent for each position based on risk and ATR.
        
        Args:
            price_data (pd.DataFrame): DataFrame with OHLCV data
            risk_fraction (float): Fraction of capital to risk per trade (e.g., 0.01 = 1%)
            atr_window (int): Window for ATR calculation
            atr_multiple_stop (float): Multiple of ATR for stop loss distance
            
        Returns:
            Series of target percentages
        """
        # Calculate ATR
        try:
            from app.strategies.indicators.technical import calculate_atr
            atr = calculate_atr(price_data, period=atr_window)
        except ImportError:
            # Fallback if the import fails
            high = price_data['high']
            low = price_data['low']
            close = price_data['close']
            
            # True Range
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=atr_window).mean()
        
        # Stop loss distance in price points
        stop_distance = atr * atr_multiple_stop
        
        # Stop loss as percentage of price
        stop_percent = stop_distance / price_data['close']
        
        # Position size as percentage of capital
        # If we're risking risk_fraction (e.g. 1%) per trade, and stop is stop_percent away,
        # then position size should be risk_fraction / stop_percent
        target_percent = risk_fraction / stop_percent
        
        # Cap the target percent to avoid excessive leverage
        max_target_percent = 0.25  # Maximum 25% of capital per trade
        target_percent = np.minimum(target_percent, max_target_percent)
        
        # Ensure no invalid values
        target_percent = target_percent.replace([np.inf, -np.inf], 0).fillna(0)
        
        return target_percent
        
    def backtest_signals(self, df, signals_df, plot=False):
        """
        Backtest the signals using vectorbt.
        
        Args:
            df (pd.DataFrame): OHLCV dataframe
            signals_df (pd.DataFrame): DataFrame containing signals and exits
            plot (bool): Whether to plot the results
            
        Returns:
            dict: Backtest results
        """
        try:
            import vectorbt as vbt
        except ImportError:
            logger.error("vectorbt is required for backtesting. Install with 'pip install vectorbt'")
            return None
            
        price = df['close'].copy()
        
        # Extract signals
        entries_long = signals_df['long_signal'].copy()
        entries_short = signals_df['short_signal'].copy()
        exits_long = signals_df['long_exit'].copy()
        exits_short = signals_df['short_exit'].copy()
            
        # Set up vectorbt portfolio
        pf_kwargs = dict(
            close=price,
            size=np.abs(signals_df['target_pct'].values),
            fees=self.params.get('trading_fee', 0.001),
            freq='1D'  # Adjust based on your data frequency
        )
        
        results = {}
        
        # Long strategy
        if entries_long.sum() > 0:
            long_pf = vbt.Portfolio.from_signals(
                entries=entries_long,
                exits=exits_long,
                **pf_kwargs
            )
            results['long'] = {
                'total_return': long_pf.total_return(),
                'sharpe_ratio': long_pf.sharpe_ratio(),
                'max_drawdown': long_pf.max_drawdown(),
                'win_rate': long_pf.win_rate() if hasattr(long_pf, 'win_rate') else None
            }
            
            if plot:
                long_pf.plot().show()
        
        # Short strategy
        if entries_short.sum() > 0:
            short_pf = vbt.Portfolio.from_signals(
                entries=entries_short,
                exits=exits_short,
                short=True,
                **pf_kwargs
            )
            results['short'] = {
                'total_return': short_pf.total_return(),
                'sharpe_ratio': short_pf.sharpe_ratio(),
                'max_drawdown': short_pf.max_drawdown(),
                'win_rate': short_pf.win_rate() if hasattr(short_pf, 'win_rate') else None
            }
            
            if plot:
                short_pf.plot().show()
                
        # Combined strategy
        if entries_long.sum() > 0 and entries_short.sum() > 0:
            # For combined, we can use the combined signals
            combined_pf = vbt.Portfolio.from_signals(
                entries=entries_long,
                exits=exits_long,
                short_entries=entries_short,
                short_exits=exits_short,
                **pf_kwargs
            )
            results['combined'] = {
                'total_return': combined_pf.total_return(),
                'sharpe_ratio': combined_pf.sharpe_ratio(),
                'max_drawdown': combined_pf.max_drawdown(),
                'win_rate': combined_pf.win_rate() if hasattr(combined_pf, 'win_rate') else None
            }
            
            if plot:
                combined_pf.plot().show()
                
        return results

    def generate_regime_exits(self, df, long_signals, short_signals, market_regimes):
        """
        Generate exit signals based on market regimes.
        
        Args:
            df (pd.DataFrame): OHLCV data
            long_signals (pd.Series): Long entry signals
            short_signals (pd.Series): Short entry signals
            market_regimes (pd.Series): Market regime classifications (1 for trending, 0 for ranging)
            
        Returns:
            tuple: (long_exits, short_exits)
        """
        # Initialize empty exit signals series
        long_exits = pd.Series(False, index=df.index)
        short_exits = pd.Series(False, index=df.index)
        
        # Calculate ATR for dynamic stops
        atr = self.calculate_atr(df, window=14)
        
        # Get close prices
        close = df['close']
        
        # Track active positions and their entry prices
        long_active = False
        short_active = False
        long_entry_price = 0
        short_entry_price = 0
        long_entry_idx = None
        short_entry_idx = None
        
        # Iterate through dataframe to determine exits
        for i in range(1, len(df)):
            # Check for long entry
            if long_signals[i] and not long_active:
                long_active = True
                long_entry_price = close[i]
                long_entry_idx = i
            
            # Check for short entry
            if short_signals[i] and not short_active:
                short_active = True
                short_entry_price = close[i]
                short_entry_idx = i
            
            # Skip if no active positions
            if not long_active and not short_active:
                continue
            
            # Define regime-specific exit parameters
            if market_regimes[i]:  # Trending regime
                # Wider stops in trending markets, trailing stops
                long_take_profit = 0.03  # 3% take profit in trending markets
                long_stop_loss = 0.015   # 1.5% stop loss
                short_take_profit = 0.03
                short_stop_loss = 0.015
                
                # Add trailing stop logic for trending markets
                if long_active and i > long_entry_idx:
                    # Update stop loss based on trailing ATR
                    highest_since_entry = close[long_entry_idx:i+1].max()
                    trailing_stop = highest_since_entry - 2 * atr[i]
                    if close[i] <= trailing_stop and highest_since_entry > long_entry_price * 1.01:
                        long_exits[i] = True
                        long_active = False
                
                if short_active and i > short_entry_idx:
                    # Update stop loss based on trailing ATR
                    lowest_since_entry = close[short_entry_idx:i+1].min()
                    trailing_stop = lowest_since_entry + 2 * atr[i]
                    if close[i] >= trailing_stop and lowest_since_entry < short_entry_price * 0.99:
                        short_exits[i] = True
                        short_active = False
            else:  # Ranging regime
                # Tighter stops in ranging markets, quicker to take profits
                long_take_profit = 0.015  # 1.5% take profit in ranging markets
                long_stop_loss = 0.01    # 1% stop loss
                short_take_profit = 0.015
                short_stop_loss = 0.01
            
            # Check for take profit and stop loss for long positions
            if long_active:
                if close[i] >= long_entry_price * (1 + long_take_profit):
                    long_exits[i] = True
                    long_active = False
                elif close[i] <= long_entry_price * (1 - long_stop_loss):
                    long_exits[i] = True
                    long_active = False
            
            # Check for take profit and stop loss for short positions
            if short_active:
                if close[i] <= short_entry_price * (1 - short_take_profit):
                    short_exits[i] = True
                    short_active = False
                elif close[i] >= short_entry_price * (1 + short_stop_loss):
                    short_exits[i] = True
                    short_active = False
            
            # Additional regime-based exits
            if long_active:
                # Exit long positions when entering ranging market after profit
                if not market_regimes[i] and market_regimes[i-1] and close[i] > long_entry_price:
                    long_exits[i] = True
                    long_active = False
            
            if short_active:
                # Exit short positions when entering ranging market after profit
                if not market_regimes[i] and market_regimes[i-1] and close[i] < short_entry_price:
                    short_exits[i] = True
                    short_active = False
        
        return long_exits, short_exits

    def detect_market_regime(self, data):
        """
        Detect market regime using ADX indicator
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.Series: Boolean series where True indicates trending market, False indicates ranging
        """
        # Calculate ADX
        adx_values = vbt.ADX.run(data['high'], data['low'], data['close'], window=14).adx
        
        # Define regime thresholds
        trending_threshold = 25  # ADX above 25 indicates trending market
        
        # Create regime boolean series (True = trending, False = ranging)
        is_trending = adx_values > trending_threshold
        
        # Log regime statistics
        trending_pct = is_trending.mean() * 100
        ranging_pct = 100 - trending_pct
        
        logger.info(f"Market regime statistics: Trending: {trending_pct:.1f}%, Ranging: {ranging_pct:.1f}%")
        
        return is_trending
        
    def detect_trend_direction(self, data):
        """
        Detect trend direction using moving averages
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pd.Series: Series where positive values indicate uptrend, negative values indicate downtrend
        """
        # Calculate short and long MAs
        short_ma = data['close'].rolling(window=20).mean()
        long_ma = data['close'].rolling(window=50).mean()
        
        # Calculate trend direction (positive = uptrend, negative = downtrend)
        trend_direction = short_ma - long_ma
        
        return trend_direction
        
    def calculate_factor_signals(self, data):
        """
        Calculate individual factor signals
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            
        Returns:
            dict: Dictionary of factor signals
        """
        close = data['close']
        high = data['high']
        low = data['low']
        volume = data['volume']
        
        # Generate component signals
        rsi_long, rsi_short = create_rsi_signals(
            close=close,
            window=self.rsi_period,
            overbought=70,
            oversold=30,
            smoothing=self.signal_smoothing
        )
        
        bb_long, bb_short = create_bollinger_signals(
            close=close,
            window=self.bbands_period,
            std_dev=self.bbands_dev,
            smoothing=self.signal_smoothing
        )
        
        macd_long, macd_short = create_macd_signals(
            close=close,
            fast_period=self.fast_ma_period,
            slow_period=self.slow_ma_period,
            signal_period=self.macd_signal,
            smoothing=self.signal_smoothing
        )
        
        # Get breakout signals for volume divergence
        breakout_up, breakout_down = create_consolidation_breakout_indicator(
            high=high,
            low=low,
            close=close,
            lookback_window=self.lookback_window
        )
        
        voldiv_long, voldiv_short = create_volume_divergence_indicator(
            volume=volume,
            lookback_window=self.lookback_window,
            breakout_up=breakout_up,
            breakout_down=breakout_down,
            volume_threshold=self.volume_threshold,
            volume_threshold_short=self.volume_threshold_short
        )
        
        return {
            'rsi_long': rsi_long,
            'rsi_short': rsi_short,
            'bb_long': bb_long,
            'bb_short': bb_short,
            'macd_long': macd_long,
            'macd_short': macd_short,
            'voldiv_long': voldiv_long,
            'voldiv_short': voldiv_short
        }
        
    def combine_factor_signals(self, signals):
        """
        Combine factor signals using weights
        
        Args:
            signals (dict): Dictionary of factor signals
            
        Returns:
            pd.Series: Combined signal strength (-1 to 1)
        """
        # Create the weighted signal
        weights = {
            'rsi': self.trend_weight,
            'bb': self.momentum_weight,
            'macd': self.mean_reversion_weight,
            'voldiv': self.volume_weight
        }
        
        # Calculate weighted average of long signals
        long_signals = (
            weights['rsi'] * signals['rsi_long'] +
            weights['bb'] * signals['bb_long'] +
            weights['macd'] * signals['macd_long'] +
            weights['voldiv'] * signals['voldiv_long']
        )
        
        # Calculate weighted average of short signals
        short_signals = (
            weights['rsi'] * signals['rsi_short'] +
            weights['bb'] * signals['bb_short'] +
            weights['macd'] * signals['macd_short'] +
            weights['voldiv'] * signals['voldiv_short']
        )
        
        # Normalize signals by the sum of weights
        total_weight = sum(weights.values())
        long_signals = long_signals / total_weight
        short_signals = short_signals / total_weight
        
        # Combine into a single signal (-1 to 1)
        combined_signal = long_signals - short_signals
        
        return combined_signal
        
    def process_signals_to_unique_entries_bool(self, entries):
        """
        Process boolean signals to ensure unique entries (no consecutive entries)
        
        Args:
            entries (pd.Series): Boolean series of entry signals
            
        Returns:
            pd.Series: Processed entry signals
        """
        # Create a copy to avoid modifying the original
        processed = entries.copy()
        
        # Track current position state (False = no position, True = in position)
        in_position = False
        
        for i in range(len(processed)):
            # If we have a new entry signal
            if processed.iloc[i]:
                # If we're already in a position, cancel the entry
                if in_position:
                    processed.iloc[i] = False
                else:
                    # Otherwise update our position state
                    in_position = True
            
            # If we have an exit signal (could add explicit exits later)
            elif not processed.iloc[i] and in_position:
                # Reset position state
                in_position = False
                
        return processed

    def run_strategy(self, df, test_mode=False):
        """
        Run the complete strategy including signal generation, market regime classification, 
        and regime-specific exits.
        
        Args:
            df (pd.DataFrame): OHLCV dataframe
            test_mode (bool): If True, runs a backtest and returns results
            
        Returns:
            tuple: (signals_df, market_regimes, backtest_results)
        """
        logger.info(f"Running strategy on {len(df)} candles")
        
        # Step 1: Classify market regimes
        market_regimes = self.detect_market_regime(df)
        
        # Step 2: Generate entry signals
        long_entries, short_entries, is_trending, is_ranging = self.generate_signals(df)
        
        # Step 3: Generate regime-specific exit signals
        long_exits, short_exits = self.generate_regime_exits(df, long_entries, short_entries, market_regimes)
        
        # Step 4: Create signals dataframe
        signals_df = pd.DataFrame({
            'long_signal': long_entries,
            'short_signal': short_entries,
            'long_exit': long_exits,
            'short_exit': short_exits,
            'market_regime': market_regimes
        }, index=df.index)
        
        # Step 5: Calculate target percentages
        target_pct = self.calculate_target_percent(df)
        signals_df['target_pct'] = target_pct
        
        # Step 6: Run backtest if in test mode
        results = None
        if test_mode:
            logger.info("Running backtest")
            results = self.backtest_signals(df, signals_df)
            
        return signals_df, market_regimes, results

def calculate_performance_metrics(portfolio):
    """
    Calculate performance metrics from a vectorbt portfolio, handling both 'pnl' and 'PnL' column names.
    
    Args:
        portfolio: A vectorbt portfolio object
        
    Returns:
        dict: A dictionary of performance metrics
    """
    metrics = {}
    
    if portfolio is None:
        return {
            'total_return': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'total_trades': 0
        }
    
    # Extract trades from portfolio
    if hasattr(portfolio, 'trades'):
        trades = portfolio.trades
        
        # Handle both direct property access and dataframe access
        try:
            # Try to get metrics directly from trades object
            if callable(trades.count):
                # Handle count as both method and attribute
                metrics['total_trades'] = trades.count()
            else:
                metrics['total_trades'] = trades.count
            
            metrics['win_rate'] = trades.win_rate
            metrics['profit_factor'] = trades.profit_factor
        except Exception as e:
            import logging
            logging.warning(f"Error calculating trade metrics: {str(e)}")
            metrics['total_trades'] = 0
            metrics['win_rate'] = 0.0
            metrics['profit_factor'] = 0.0
    
    # Portfolio-level metrics
    try:
        # Get total return - handle both property and method
        if callable(getattr(portfolio, 'total_return', None)):
            metrics['total_return'] = portfolio.total_return()
        else:
            metrics['total_return'] = portfolio.total_return
            
        # Get max drawdown - handle both property and method
        if callable(getattr(portfolio, 'max_drawdown', None)):
            metrics['max_drawdown'] = portfolio.max_drawdown()
        else:
            metrics['max_drawdown'] = portfolio.max_drawdown
            
        # Get Sharpe ratio - handle both property and method
        if callable(getattr(portfolio, 'sharpe_ratio', None)):
            metrics['sharpe_ratio'] = portfolio.sharpe_ratio()
        else:
            metrics['sharpe_ratio'] = getattr(portfolio, 'sharpe_ratio', 0.0)
    except Exception as e:
        import logging
        logging.warning(f"Error calculating portfolio metrics: {str(e)}")
        metrics['total_return'] = 0.0
        metrics['max_drawdown'] = 0.0
        metrics['sharpe_ratio'] = 0.0
    
    return metrics

# --- Main block for single run testing ---
if __name__ == "__main__":
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description='Test Fixed EdgeMultiFactorStrategy.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2023-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1h', help='Data granularity (e.g., 1h, 4h, 1d)')
    parser.add_argument('--lookback', type=int, default=None, help='Lookback window for factors (overrides profile)')
    parser.add_argument('--vol_thresh', type=float, default=None, help='Volatility ratio threshold (overrides profile)')
    parser.add_argument('--plot', action='store_true', help='Generate and show plot')
    
    # Add parameter profile support
    parser.add_argument('--profile', type=str, default='optimized_hourly', 
                        help='Parameter profile name from config/strategy_params.json')
    parser.add_argument('--list_profiles', action='store_true', 
                        help='List available parameter profiles and exit')
    
    args = parser.parse_args()
    
    # Import the parameter loader
    try:
        from scripts.strategies.param_loader import load_strategy_params, list_available_profiles, get_profile_description
    except ImportError:
        # If we're running from the strategies directory
        import sys
        sys.path.append(str(ROOT_DIR / 'scripts' / 'strategies'))
        try:
            from param_loader import load_strategy_params, list_available_profiles, get_profile_description
        except ImportError:
            print("Could not import param_loader. Using default parameters.")
            load_strategy_params = lambda profile, file=None: {
                "lookback_window": 20,
                "vol_filter_window": 100,
                "volatility_threshold": 0.5,
                "signal_threshold": 0.3,
            }
            list_available_profiles = lambda: []
            get_profile_description = lambda profile: ""
    
    # List available profiles if requested
    if args.list_profiles:
        print("\nAvailable Parameter Profiles:")
        profiles = list_available_profiles()
        
        for profile in profiles:
            desc = get_profile_description(profile)
            print(f"- {profile}: {desc}")
        sys.exit(0)
    
    # --- Data Fetching ---
    granularity_seconds = GRANULARITY_MAP_SECONDS.get(args.granularity.lower())
    if granularity_seconds is None:
        print(f"Error: Unsupported granularity: {args.granularity}.")
        sys.exit(1)
    
    print(f"Fetching data for {args.symbol} from {args.start_date} to {args.end_date} ({args.granularity})...")
    price_data = fetch_historical_data(args.symbol, args.start_date, args.end_date, granularity_seconds)
    
    if price_data is None or price_data.empty:
        print("Failed to fetch data. Exiting.")
        sys.exit(1)
    
    print(f"Data fetched successfully. Shape: {price_data.shape}")
    price_data.index = pd.to_datetime(price_data.index, utc=True)

    # --- Load Parameters from Profile ---
    params = load_strategy_params(args.profile)
    
    # Override parameters from command line if provided
    if args.lookback is not None:
        params["lookback_window"] = args.lookback
    if args.vol_thresh is not None:
        params["volatility_threshold"] = args.vol_thresh
    
    # --- Strategy Initialization ---
    print("Initializing fixed EdgeMultiFactorStrategy...")
    print(f"Using parameter profile: {args.profile}")
    print(f"Parameters: lookback_window={params['lookback_window']}, " + 
          f"vol_filter_window={params.get('vol_filter_window', 100)}, " +
          f"volatility_threshold={params['volatility_threshold']}, " +
          f"signal_threshold={params.get('signal_threshold', 0.3)}, " +
          f"volume_threshold={params.get('volume_threshold', 1.1)}, " +
          f"volume_threshold_short={params.get('volume_threshold_short', 1.05)}, " +
          f"volume_roc_threshold={params.get('volume_roc_threshold', 0.1)}")
          
    strategy = EdgeMultiFactorStrategy(
        lookback_window=params["lookback_window"],
        vol_filter_window=params.get("vol_filter_window", 100),
        volatility_threshold=params["volatility_threshold"],
        initial_capital=params.get("initial_capital", 3000),
        default_factor_weights=params.get("default_factor_weights", None),
        signal_threshold=params.get("signal_threshold", 0.3),
        volume_threshold=params.get("volume_threshold", 1.1),
        volume_threshold_short=params.get("volume_threshold_short", 1.05),
        volume_roc_threshold=params.get("volume_roc_threshold", 0.1)
    )

    # --- Signal Generation --- 
    print("Generating signals...")
    signals_df, market_regimes, results = strategy.run_strategy(price_data)
    
    if signals_df['long_signal'].sum() + signals_df['short_signal'].sum() == 0:
        print("No entry signals generated.")
        sys.exit(0)
    
    # --- Calculate Target Percentage Size ---
    print("Calculating target percentage size...")
    target_pct = strategy.calculate_target_percent(price_data)
    
    # --- Results ---
    print(f"Generated {signals_df['long_signal'].sum()} long entries and {signals_df['short_signal'].sum()} short entries.")
    print(f"Trending periods: {market_regimes.mean() * 100:.2f}%")
    
    # --- Backtest the strategy ---
    print("Backtesting the strategy...")
    if results is not None:
        print("\nBacktest Results:")
        print(f"Total Return: {results['total_return']:.2%}")
        print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
        print(f"Max Drawdown: {results['max_drawdown']:.2%}")
        print(f"Total Trades: {results['num_trades']}")
        print(f"Win Rate: {results['win_rate']:.2%}")
        print(f"Profit Factor: {results['profit_factor']:.2f}")
    else:
        print("Backtest failed.")
    
    # --- Plotting ---
    if args.plot:
        print("Generating plot...")
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        
        # Plot price and signals
        plt.subplot(2, 1, 1)
        plt.plot(price_data.index, price_data['close'], label='Close Price')
        plt.scatter(price_data.index[signals_df['long_signal'] > 0], 
                    price_data.loc[signals_df['long_signal'] > 0, 'close'],
                    color='green', marker='^', label='Long Entry')
        plt.scatter(price_data.index[signals_df['short_signal'] > 0], 
                    price_data.loc[signals_df['short_signal'] > 0, 'close'],
                    color='red', marker='v', label='Short Entry')
        plt.title('Price and Signals')
        plt.legend()
        
        # Plot trending and ranging periods
        plt.subplot(2, 1, 2)
        plt.plot(price_data.index, market_regimes, label='Market Regimes', color='blue')
        plt.title('Market Regimes')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('edge_strategy_fixed_test.png')
        print("Plot saved to edge_strategy_fixed_test.png")
    
    print("Test completed successfully.") 