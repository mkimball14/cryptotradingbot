# ==============================================================================
# Strategy Development Settings
# ==============================================================================
# When working on this strategy file, always use the sequential_thinking MCP tool
# to methodically think through the changes. This ensures a systematic approach to
# enhancing the strategy logic, fixing issues, and improving performance.
# 
# Sequential thinking helps to:
# 1. Break down complex problems into manageable steps
# 2. Ensure all edge cases are considered
# 3. Maintain awareness of how changes impact the whole system
# 4. Document the thought process for future development
#
# This directive is part of our standard development workflow.
# ==============================================================================

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
from numba import njit
import typing as tp

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
                               volume_threshold=1.5, volume_threshold_short=1.2, volume_roc_threshold=0.1,
                               is_trending=None, is_ranging=None, price=None, hour_of_day=None,
                               volatility_data=None, session_filter=True, adaptive_threshold=True):
    """Calculates volume confirmation signals based on pre-calculated breakouts with enhanced detection.
    
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
        price: Optional price data for volume-price divergence detection
        hour_of_day: Optional hour of day data for time-based filtering
        volatility_data: Optional volatility data for additional adjustments
        session_filter: Whether to apply time-based session filtering
        adaptive_threshold: Whether to adapt thresholds based on market conditions
    
    Returns:
        tuple: (volume_confirms_up, volume_confirms_down, volume_strength)
    """
    # Get shorter window MA for faster reaction to volume changes
    volume_short_ma = volume.vbt.rolling_mean(window=lookback_window//2, minp=max(3, lookback_window//4))
    volume_ma = volume.vbt.rolling_mean(window=lookback_window, minp=lookback_window // 2)
    volume_ma_safe = volume_ma.replace(0, np.nan).ffill().bfill()
    
    # Calculate volume ratios against different lookback periods
    vol_ratio_vol = (volume / volume_ma_safe).fillna(1.0)
    vol_ratio_short = (volume / volume_short_ma.replace(0, np.nan).ffill().bfill()).fillna(1.0)
    
    # Calculate longer-term volume reference (e.g., 50 periods)
    long_window = min(lookback_window * 5, 50)  # Cap at 50 periods or 5x lookback
    volume_long_ma = volume.vbt.rolling_mean(window=long_window, minp=long_window // 2)
    volume_long_ma_safe = volume_long_ma.replace(0, np.nan).ffill().bfill()
    vol_ratio_long = (volume / volume_long_ma_safe).fillna(1.0)
    
    # Print volume ratio statistics for debugging
    print(f"Volume ratio stats - min: {vol_ratio_vol.min():.4f}, max: {vol_ratio_vol.max():.4f}, mean: {vol_ratio_vol.mean():.4f}")
    print(f"Short-term volume ratio - min: {vol_ratio_short.min():.4f}, max: {vol_ratio_short.max():.4f}, mean: {vol_ratio_short.mean():.4f}")
    print(f"Long-term volume ratio - min: {vol_ratio_long.min():.4f}, max: {vol_ratio_long.max():.4f}, mean: {vol_ratio_long.mean():.4f}")
    print(f"Base volume thresholds - main: {volume_threshold}, short-term: {volume_threshold_short}, ROC: {volume_roc_threshold}")
    
    # Apply market regime-based threshold adjustments if regime data is provided
    adapted_volume_threshold = pd.Series(volume_threshold, index=volume.index)
    adapted_volume_threshold_short = pd.Series(volume_threshold_short, index=volume.index)
    adapted_roc_threshold = pd.Series(volume_roc_threshold, index=volume.index)
    
    # Time-based threshold adjustments - recognize market sessions
    if session_filter and hour_of_day is not None:
        # Define active trading hours based on global crypto market activity
        # Most active: 12-16 UTC (European afternoon/US morning)
        # Moderately active: 0-4 UTC (Asian session), 8-12 and 16-20 UTC (European/US transition)
        # Less active: 4-8 and 20-24 UTC
        high_activity_hours = (hour_of_day >= 12) & (hour_of_day < 16)
        medium_activity_hours = (
            ((hour_of_day >= 0) & (hour_of_day < 4)) | 
            ((hour_of_day >= 8) & (hour_of_day < 12)) | 
            ((hour_of_day >= 16) & (hour_of_day < 20))
        )
        low_activity_hours = ~(high_activity_hours | medium_activity_hours)
        
        # Adjust thresholds based on market activity
        # During high activity, we can use normal thresholds
        # During medium activity, increase thresholds slightly
        # During low activity, increase thresholds significantly to avoid false signals
        adapted_volume_threshold.loc[medium_activity_hours] *= 1.2   # 20% higher threshold
        adapted_volume_threshold.loc[low_activity_hours] *= 1.5      # 50% higher threshold
        
        adapted_volume_threshold_short.loc[medium_activity_hours] *= 1.2
        adapted_volume_threshold_short.loc[low_activity_hours] *= 1.5
        
        adapted_roc_threshold.loc[medium_activity_hours] *= 1.2
        adapted_roc_threshold.loc[low_activity_hours] *= 1.5
        
        print(f"Session adjustments - High activity: normal, Medium: +20%, Low: +50%")
    
    # Apply market regime-based adjustments if regime data is provided
    if adaptive_threshold and is_trending is not None and is_ranging is not None:
        # Make volume thresholds more strict during trending periods (reduce false signals)
        trending_adjustment = 1.3  # Increase threshold by 30% during trends
        ranging_adjustment = 0.9   # Decrease threshold by 10% during ranges
        
        # Apply adjustments based on market regimes
        adapted_volume_threshold.loc[is_trending] *= trending_adjustment
        adapted_volume_threshold.loc[is_ranging] *= ranging_adjustment
        
        adapted_volume_threshold_short.loc[is_trending] *= trending_adjustment
        adapted_volume_threshold_short.loc[is_ranging] *= ranging_adjustment
        
        # Adjust ROC threshold as well
        adapted_roc_threshold.loc[is_trending] *= 1.2
        adapted_roc_threshold.loc[is_ranging] *= 0.95
        
        print(f"Market regime adjustments - Trending: +30%, Ranging: -10%")
    
    # Apply additional adjustments based on volatility if available
    if adaptive_threshold and volatility_data is not None:
        # Convert numpy array to pandas Series if needed
        if isinstance(volatility_data, np.ndarray):
            volatility_data = pd.Series(volatility_data, index=volume.index)
            
        # Normalize volatility between 0 and 1
        volatility_normalized = (volatility_data - volatility_data.rolling(50).min()) / \
                              (volatility_data.rolling(50).max() - volatility_data.rolling(50).min())
        volatility_normalized = volatility_normalized.fillna(0.5)  # Default to mid-level
        
        # Higher volatility -> higher thresholds to avoid false signals
        volatility_adjustment = 1 + (volatility_normalized * 0.5)  # Up to 50% increase for high volatility
        
        # Apply volatility adjustment
        adapted_volume_threshold = adapted_volume_threshold * volatility_adjustment
        adapted_volume_threshold_short = adapted_volume_threshold_short * volatility_adjustment
        
        print(f"Volatility adjustments - Range: {volatility_adjustment.min():.2f}x to {volatility_adjustment.max():.2f}x")
    
    print(f"Adjusted volume threshold range: {adapted_volume_threshold.min():.4f} to {adapted_volume_threshold.max():.4f}")
    
    # Count periods where volume ratio exceeds threshold
    high_volume_count = (vol_ratio_vol > adapted_volume_threshold).sum()
    high_volume_short_count = (vol_ratio_short > adapted_volume_threshold_short).sum()
    print(f"High volume periods: {high_volume_count}/{len(vol_ratio_vol)} ({high_volume_count/len(vol_ratio_vol)*100:.2f}%)")
    print(f"High short-term volume periods: {high_volume_short_count}/{len(vol_ratio_short)} ({high_volume_short_count/len(vol_ratio_short)*100:.2f}%)")
    
    # Enhanced volume detection - consider multiple volume indicators
    # 1. Relative volume compared to lookback period
    # 2. Relative volume compared to short-term lookback
    # 3. Relative volume compared to longer-term lookback
    # 4. Rate of change in volume
    # 5. Consecutive increasing volume bars
    # 6. Volume profile patterns
    
    # Calculate volume rate of change with different periods
    volume_roc = volume.pct_change(3).fillna(0)  # 3-period rate of change
    volume_roc_short = volume.pct_change(1).fillna(0)  # 1-period rate of change
    volume_roc_long = volume.pct_change(5).fillna(0)  # 5-period rate of change
    
    volume_increasing = volume_roc > adapted_roc_threshold  # ROC threshold
    volume_increasing_short = volume_roc_short > adapted_roc_threshold * 0.8  # More sensitive
    volume_increasing_long = volume_roc_long > adapted_roc_threshold * 1.2    # Less sensitive
    
    # Detect consecutive increasing volume (2 or more bars)
    vol_change = volume.diff().fillna(0)
    consecutive_increasing = (vol_change > 0) & (vol_change.shift(1) > 0)
    
    # Detect 3-bar consecutive increasing volume (stronger signal)
    consecutive_increasing_3bars = consecutive_increasing & (vol_change.shift(2) > 0)
    
    # Detect volume patterns: climax volume (very high volume followed by declining volume)
    climax_volume = (vol_ratio_vol > adapted_volume_threshold * 1.5) & \
                    (vol_ratio_vol.shift(1) < vol_ratio_vol) & \
                    (vol_ratio_vol.shift(-1) < vol_ratio_vol)
    
    # Time-based volume filtering - reduce signals during low liquidity periods
    # This prevents triggering on random volume spikes during off-hours
    volume_std = volume.rolling(window=48).std()  # Calculate volume volatility
    volume_normalized = (volume - volume.rolling(window=48).mean()) / volume_std.replace(0, np.nan)
    abnormal_volume = volume_normalized > 1.5  # Only consider significantly abnormal volume
    
    # Advanced: Calculate volume surge anomaly score
    volume_z_score = (volume - volume.rolling(window=20).mean()) / volume.rolling(window=20).std()
    volume_z_score = volume_z_score.fillna(0)
    significant_surge = volume_z_score > 2.0  # More than 2 standard deviations
    
    # Optional: Add price-volume divergence detection if price data is available
    price_volume_divergence = pd.Series(False, index=volume.index)
    if price is not None:
        # Price going down but volume increasing = accumulation
        # Price going up but volume decreasing = distribution
        price_change = price.pct_change().fillna(0)
        volume_change = volume.pct_change().fillna(0)
        
        # Accumulation: price down, volume up
        accumulation = (price_change < 0) & (volume_change > 0) & (volume > volume_ma_safe)
        
        # Distribution: price up, volume down
        distribution = (price_change > 0) & (volume_change < 0) & (volume > volume_ma_safe)
        
        # Only consider significant divergences
        price_volume_divergence = (accumulation | distribution) & significant_surge
    
    # Add consecutive signal requirement - need breakout confirmation
    # Strengthen confirmation requirement: need more persistent breakout signals
    breakout_up_confirmed = breakout_up & breakout_up.shift(1)  # Two consecutive breakout signals
    breakout_down_confirmed = breakout_down & breakout_down.shift(1)  # Two consecutive breakout signals
    
    # Even stronger confirmation: three consecutive signals
    breakout_up_strong = breakout_up_confirmed & breakout_up.shift(2)
    breakout_down_strong = breakout_down_confirmed & breakout_down.shift(2)
    
    # Calculate volume strength score (0-1) to quantify confidence in the volume signal
    volume_strength = pd.Series(0.0, index=volume.index)
    
    # Base strength from relative volume (more volume = higher score)
    base_strength = np.minimum(vol_ratio_vol / adapted_volume_threshold, 1.0) * 0.6 + \
                   np.minimum(vol_ratio_short / adapted_volume_threshold_short, 1.0) * 0.4
    
    # Additional strength from pattern recognition
    pattern_strength = pd.Series(0.0, index=volume.index)
    pattern_strength.loc[consecutive_increasing] += 0.1
    pattern_strength.loc[consecutive_increasing_3bars] += 0.2
    pattern_strength.loc[climax_volume] += 0.15
    pattern_strength.loc[significant_surge] += 0.2
    pattern_strength.loc[price_volume_divergence] += 0.1
    
    # Add all components with normalization to ensure 0-1 range
    volume_strength = np.minimum(base_strength + pattern_strength, 1.0)
    
    # Modified volume confirmation with multiple conditions
    # Core confirmation conditions
    core_confirmation = (
        # Original criteria
        ((vol_ratio_vol > adapted_volume_threshold) | 
         (vol_ratio_short > adapted_volume_threshold_short)) & 
        # Require some form of volume increase
        (volume_increasing | volume_increasing_short | consecutive_increasing) &
        # Still filter out non-significant volume
        abnormal_volume
    )
    
    # More selective confirmation for stronger signals
    strong_confirmation = core_confirmation & (
        # Additional criteria for stronger signals
        ((vol_ratio_vol > adapted_volume_threshold * 1.2) |  # Much higher volume 
         (vol_ratio_short > adapted_volume_threshold_short * 1.2) |
         consecutive_increasing_3bars |  # 3 consecutive increases
         significant_surge |  # Statistical anomaly
         climax_volume)  # Volume climax pattern
    )
    
    # Final signals with different confirmation levels
    volume_confirms_up = (
        # Use regular confirmation with confirmed breakout
        (core_confirmation & breakout_up_confirmed) |
        # OR use a less stringent volume requirement with stronger breakout
        ((vol_ratio_vol > adapted_volume_threshold) & breakout_up_strong)
    )
    
    volume_confirms_down = (
        # Use regular confirmation with confirmed breakout
        (core_confirmation & breakout_down_confirmed) |
        # OR use a less stringent volume requirement with stronger breakout
        ((vol_ratio_vol > adapted_volume_threshold) & breakout_down_strong)
    )
    
    # Upgrade to strong confirmation when appropriate
    volume_confirms_up_strong = volume_confirms_up & strong_confirmation
    volume_confirms_down_strong = volume_confirms_down & strong_confirmation
    
    # Optional: Calculate conviction levels (could be used for position sizing)
    volume_up_conviction = pd.Series(0.5, index=volume.index)
    volume_down_conviction = pd.Series(0.5, index=volume.index)
    
    # Increase conviction based on strong confirmation
    volume_up_conviction.loc[volume_confirms_up] = 0.7
    volume_up_conviction.loc[volume_confirms_up_strong] = 0.9
    
    volume_down_conviction.loc[volume_confirms_down] = 0.7
    volume_down_conviction.loc[volume_confirms_down_strong] = 0.9
    
    # Return standard boolean signals and the volume strength for additional context
    return volume_confirms_up, volume_confirms_down, volume_strength

def create_market_microstructure_indicator(open, high, low, close):
    """Calculates market microstructure signals (candle shadows)."""
    upper_shadow = high - np.maximum(open, close)
    lower_shadow = np.minimum(open, close) - low
    hl_range_nonzero = (high - low).replace(0, np.nan)
    shadow_ratio = ((upper_shadow - lower_shadow) / hl_range_nonzero).fillna(0)
    buying_pressure = shadow_ratio < -0.5
    selling_pressure = shadow_ratio > 0.5
    return buying_pressure, selling_pressure

def create_regime_specific_exits(
    price, volume, high, low, volatility_window=14, adx_window=14, 
    rsi_window=14, bb_window=20, atr_window=14, volume_spike_threshold=2.0,
    stop_loss_pct=0.02, take_profit_pct=0.04, time_stop=10,
    long_exit_rsi_threshold=70, short_exit_rsi_threshold=30, adx_threshold=25
):
    """
    Creates exit rules for long and short positions based on market regimes (trending or ranging).
    
    Args:
        price (pd.Series or np.array): Price data
        volume (pd.Series or np.array): Volume data
        high (pd.Series or np.array): High price data
        low (pd.Series or np.array): Low price data
        volatility_window (int): Window for ATR volatility calculation
        adx_window (int): Window for ADX calculation
        rsi_window (int): Window for RSI calculation
        bb_window (int): Window for Bollinger Bands calculation
        atr_window (int): Window for ATR calculation
        volume_spike_threshold (float): Threshold for volume spike detection
        stop_loss_pct (float): Default stop loss percentage
        take_profit_pct (float): Default take profit percentage
        time_stop (int): Maximum bars to hold a position
        long_exit_rsi_threshold (int): RSI threshold for exiting long positions
        short_exit_rsi_threshold (int): RSI threshold for exiting short positions
        adx_threshold (int): ADX threshold for trend identification
    
    Returns:
        tuple: Functions for long exit signal and short exit signal
    """
    # Convert inputs to numpy arrays for better performance
    price_np = np.asarray(price, dtype=np.float32)
    volume_np = np.asarray(volume, dtype=np.float32)
    high_np = np.asarray(high, dtype=np.float32)
    low_np = np.asarray(low, dtype=np.float32)
    
    # Calculate ADX for trend identification
    def calculate_adx(high, low, close, window):
        # Ensure window is an integer
        window = int(window)
        
        high_prev = np.roll(high, 1)
        low_prev = np.roll(low, 1)
        
        # Set first values to NaN
        high_prev[0] = np.nan
        low_prev[0] = np.nan
        
        # True Range
        tr1 = np.abs(high - low)
        tr2 = np.abs(high - np.roll(close, 1))
        tr3 = np.abs(low - np.roll(close, 1))
        tr = np.maximum(np.maximum(tr1, tr2), tr3)
        
        # Directional Movement
        up_move = high - high_prev
        down_move = low_prev - low
        
        # Positive and Negative Directional Movement
        pdm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        ndm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        # First value is just the SMA
        atr = np.zeros_like(high)
        atr[window-1] = np.mean(tr[:window])
        
        pdi = np.zeros_like(high)
        pdi[window-1] = 100 * np.mean(pdm[:window]) / atr[window-1]
        
        ndi = np.zeros_like(high)
        ndi[window-1] = 100 * np.mean(ndm[:window]) / atr[window-1]
        
        # Rest use Wilder's smoothing method
        for i in range(window, len(high)):
            atr[i] = ((window - 1) * atr[i-1] + tr[i]) / window
            pdi[i] = 100 * (((window - 1) * pdi[i-1] * atr[i-1] / 100) + pdm[i]) / atr[i]
            ndi[i] = 100 * (((window - 1) * ndi[i-1] * atr[i-1] / 100) + ndm[i]) / atr[i]
        
        # DX and ADX
        dx = np.zeros_like(high)
        adx = np.zeros_like(high)
        
        for i in range(window-1, len(high)):
            dx[i] = 100 * np.abs(pdi[i] - ndi[i]) / (pdi[i] + ndi[i]) if (pdi[i] + ndi[i]) > 0 else 0
        
        # First ADX is just average of DX
        adx[2*window-2] = np.mean(dx[window-1:2*window-1])
        
        # Rest use smoothing
        for i in range(2*window-1, len(high)):
            adx[i] = ((window - 1) * adx[i-1] + dx[i]) / window
        
        return adx, pdi, ndi
    
    # Calculate RSI
    def calculate_rsi(prices, window=14):
        deltas = np.diff(prices)
        deltas = np.append(deltas, 0)  # Add 0 to make same length as prices
        
        # Ensure window is an integer
        window = int(window)
        
        # Separate gains and losses
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        # Calculate average gain and loss
        avg_gain = np.zeros_like(prices)
        avg_loss = np.zeros_like(prices)
        
        # First average is simple average
        avg_gain[window] = np.mean(gains[:window])
        avg_loss[window] = np.mean(losses[:window])
        
        # Subsequent averages are smoothed
        for i in range(window + 1, len(prices)):
            avg_gain[i] = (avg_gain[i-1] * (window-1) + gains[i-1]) / window
            avg_loss[i] = (avg_loss[i-1] * (window-1) + losses[i-1]) / window
        
        # Calculate RS and RSI
        rs = np.divide(avg_gain, avg_loss, out=np.ones_like(avg_gain), where=avg_loss!=0)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    # Calculate Bollinger Bands
    def calculate_bollinger_bands(prices, window=20, num_std=2):
        # Ensure window is an integer
        window = int(window)
        
        # Calculate rolling mean and standard deviation
        rolling_mean = np.zeros_like(prices)
        rolling_std = np.zeros_like(prices)
        
        # Calculate initial values only where we have enough data
        for i in range(window-1, len(prices)):
            rolling_mean[i] = np.mean(prices[i-window+1:i+1])
            rolling_std[i] = np.std(prices[i-window+1:i+1])
        
        # Calculate bands
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        
        # Calculate %B indicator: (price - lower) / (upper - lower)
        percent_b = np.zeros_like(prices)
        band_width = upper_band - lower_band
        
        # Avoid division by zero
        valid_bands = band_width > 0
        percent_b[valid_bands] = (prices[valid_bands] - lower_band[valid_bands]) / band_width[valid_bands]
        
        return rolling_mean, upper_band, lower_band, percent_b
    
    # Calculate relative volume
    def calculate_relative_volume(volume, window=20):
        # Ensure window is an integer
        window = int(window)
        
        avg_volume = np.zeros_like(volume)
        
        # Calculate average volume
        for i in range(window-1, len(volume)):
            avg_volume[i] = np.mean(volume[i-window+1:i+1])
        
        # Calculate relative volume (current volume / average volume)
        rel_volume = np.zeros_like(volume)
        
        # Avoid division by zero
        valid_avg = avg_volume > 0
        rel_volume[valid_avg] = volume[valid_avg] / avg_volume[valid_avg]
        
        return rel_volume
    
    # Calculate indicators
    adx, plus_di, minus_di = calculate_adx(high_np, low_np, price_np, adx_window)
    rsi = calculate_rsi(price_np, rsi_window)
    bb_middle, bb_upper, bb_lower, bb_percent_b = calculate_bollinger_bands(price_np, bb_window, 2)
    rel_volume = calculate_relative_volume(volume_np, bb_window)
    atr = calculate_atr(high_np, low_np, price_np, atr_window)
    
    # Detect regime (trend vs range)
    is_trending = adx > adx_threshold
    
    # Convert any pandas Series to numpy arrays for consistent indexing
    if isinstance(is_trending, pd.Series):
        is_trending = is_trending.to_numpy()
    if isinstance(rsi, pd.Series):
        rsi = rsi.to_numpy()
    if isinstance(rel_volume, pd.Series):
        rel_volume = rel_volume.to_numpy()
    if isinstance(bb_upper, pd.Series):
        bb_upper = bb_upper.to_numpy()
    if isinstance(bb_lower, pd.Series):
        bb_lower = bb_lower.to_numpy()
    
    # Long exit function
    def long_exit_signal(i, entry_price, entry_idx, state=None):
        """
        Generate exit signal for long positions based on market regime and other factors.
        
        Args:
            i (int): Current bar index
            entry_price (float): Entry price
            entry_idx (int): Index of entry bar
            state (dict, optional): State dictionary for position tracking
        
        Returns:
            tuple: (exit signal (bool), state (dict))
        """
        if i < 1 or i >= len(price_np):
            return False, state
        
        # Initialize state if not provided
        if state is None:
            state = {
                'highest_price': price_np[i],
                'trailing_stop': entry_price * (1 - stop_loss_pct),
                'position_age': 0
            }
        else:
            # Update position age
            state['position_age'] = i - entry_idx
            # Update highest price seen
            state['highest_price'] = max(state['highest_price'], price_np[i])
        
        # Basic stop loss
        stop_price = entry_price * (1 - stop_loss_pct)
        
        # Basic take profit
        take_profit = entry_price * (1 + take_profit_pct)
        
        # Check if we're in a trending or range-bound market
        if is_trending[i]:
            # In trending markets, use adaptive trailing stops
            state['trailing_stop'] = create_adaptive_trailing_stop(
                price_np[i], high_np[i], low_np[i], 
                state['position_age'], state['highest_price'],
                entry_price, atr[i], atr_multiplier=1.5
            )
            
            # In trends, use RSI overbought as an exit signal
            overbought_exit = rsi[i] > long_exit_rsi_threshold and rsi[i-1] <= long_exit_rsi_threshold
            
            # Volume exhaustion in trend (spike followed by decline)
            volume_exhaustion = (rel_volume[i-1] > volume_spike_threshold and 
                                rel_volume[i] < rel_volume[i-1] * 0.7)
            
            # Exit on price dropping below trailing stop, overbought RSI or volume exhaustion
            return (low_np[i] < state['trailing_stop'] or 
                    price_np[i] > take_profit or 
                    overbought_exit or 
                    volume_exhaustion or 
                    state['position_age'] >= time_stop), state
            
        else:
            # In range-bound markets, use tighter stops
            range_stop = state['highest_price'] - (atr[i] * 1.0)  # Tighter stop in range
            
            # Bollinger Band based exit (price approaching upper band)
            bb_exit = price_np[i] > (bb_upper[i] * 0.99)
            
            # RSI extreme in range is a stronger exit signal
            range_rsi_exit = rsi[i] > (long_exit_rsi_threshold - 5)
            
            # Exit on range conditions
            return (low_np[i] < range_stop or 
                    price_np[i] > take_profit or 
                    bb_exit or 
                    range_rsi_exit or 
                    state['position_age'] >= time_stop * 0.8), state  # Shorter time exit in range
    
    # Short exit function
    def short_exit_signal(i, entry_price, entry_idx, state=None):
        """
        Generate exit signal for short positions based on market regime and other factors.
        
        Args:
            i (int): Current bar index
            entry_price (float): Entry price
            entry_idx (int): Index of entry bar
            state (dict, optional): State dictionary for position tracking
        
        Returns:
            tuple: (exit signal (bool), state (dict))
        """
        if i < 1 or i >= len(price_np):
            return False, state
        
        # Initialize state if not provided
        if state is None:
            state = {
                'lowest_price': price_np[i],
                'trailing_stop': entry_price * (1 + stop_loss_pct),
                'position_age': 0
            }
        else:
            # Update position age
            state['position_age'] = i - entry_idx
            # Update lowest price seen
            state['lowest_price'] = min(state['lowest_price'], price_np[i])
        
        # Basic stop loss
        stop_price = entry_price * (1 + stop_loss_pct)
        
        # Basic take profit
        take_profit = entry_price * (1 - take_profit_pct)
        
        # Check regime
        if is_trending[i]:
            # In trending markets, use adaptive trailing stops for shorts
            # For shorts, we need to invert some of the logic
            short_trailing_stop = entry_price * (1 + stop_loss_pct)
            
            # Adaptive trailing stop for shorts - we need to increase it as price falls
            if state['position_age'] <= 3:
                trailing_multiplier = 0.8
            elif state['position_age'] <= 5:
                trailing_multiplier = 0.7
            elif state['position_age'] <= 8:
                trailing_multiplier = 0.5
            else:
                trailing_multiplier = 0.3
            
            # Calculate short trailing stop
            price_movement = entry_price - state['lowest_price']
            percent_move = price_movement / entry_price
            
            if percent_move > 0:  # If we're profitable
                state['trailing_stop'] = state['lowest_price'] + (atr[i] * 1.5 * trailing_multiplier)
                
                # For significant profit, tighten stop even more
                if percent_move > 0.05:  # More than 5% move
                    state['trailing_stop'] = 0.3 * state['trailing_stop'] + 0.7 * (state['lowest_price'] + (atr[i] * 0.5))
                elif percent_move > 0.02:  # More than 2% move
                    state['trailing_stop'] = 0.5 * state['trailing_stop'] + 0.5 * (state['lowest_price'] + (atr[i] * 0.8))
                
                # Ensure stop is never higher than the original stop loss
                state['trailing_stop'] = min(state['trailing_stop'], stop_price)
                
                # Lock in profit after a certain move
                if percent_move > 0.01 and state['position_age'] > 2:
                    state['trailing_stop'] = min(state['trailing_stop'], entry_price)
            
            # In trends, use RSI oversold as an exit signal for shorts
            oversold_exit = rsi[i] < short_exit_rsi_threshold and rsi[i-1] >= short_exit_rsi_threshold
            
            # Volume exhaustion in trend (spike followed by decline)
            volume_exhaustion = (rel_volume[i-1] > volume_spike_threshold and 
                                rel_volume[i] < rel_volume[i-1] * 0.7)
            
            # Exit on price rising above trailing stop, oversold RSI or volume exhaustion
            return (high_np[i] > state['trailing_stop'] or 
                    price_np[i] < take_profit or 
                    oversold_exit or 
                    volume_exhaustion or 
                    state['position_age'] >= time_stop), state
            
        else:
            # In range-bound markets, use tighter stops for shorts
            range_stop = state['lowest_price'] + (atr[i] * 1.0)  # Tighter stop in range
            
            # Bollinger Band based exit (price approaching lower band)
            bb_exit = price_np[i] < (bb_lower[i] * 1.01)
            
            # RSI extreme in range is a stronger exit signal
            range_rsi_exit = rsi[i] < (short_exit_rsi_threshold + 5)
            
            # Exit on range conditions
            return (high_np[i] > range_stop or 
                    price_np[i] < take_profit or 
                    bb_exit or 
                    range_rsi_exit or 
                    state['position_age'] >= time_stop * 0.8), state  # Shorter time exit in range
    
    return long_exit_signal, short_exit_signal

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

def calculate_atr(high, low, close, window):
    """
    Calculate Average True Range (ATR)
    
    Args:
        high (np.array): Array of high prices
        low (np.array): Array of low prices
        close (np.array): Array of close prices
        window (int): Window size for ATR calculation
    
    Returns:
        np.array: ATR values
    """
    # Ensure window is an integer
    window = int(window)
    
    # Convert to numpy arrays if they are not already
    high = np.asarray(high, dtype=np.float32)
    low = np.asarray(low, dtype=np.float32)
    close = np.asarray(close, dtype=np.float32)
    
    # Calculate True Range
    tr1 = np.abs(high[1:] - low[1:])
    tr2 = np.abs(high[1:] - close[:-1])
    tr3 = np.abs(low[1:] - close[:-1])
    
    # Get the maximum of the three components
    tr = np.maximum(np.maximum(tr1, tr2), tr3)
    
    # Prepend a value to make it same length as input
    # (we use the first high-low range as an approximation)
    first_tr = high[0] - low[0]
    tr = np.insert(tr, 0, first_tr)
    
    # Calculate ATR with exponential moving average
    atr = np.zeros_like(tr)
    atr[0] = tr[0]
    
    # Smoothing factor
    alpha = 2.0 / (window + 1.0)
    
    # Calculate smoothed ATR
    for i in range(1, len(tr)):
        atr[i] = alpha * tr[i] + (1 - alpha) * atr[i-1]
    
    return atr

def create_adaptive_trailing_stop(current_price, high, low, position_age, position_high, entry_price, atr, atr_multiplier=2.0):
    """
    Creates an adaptive trailing stop that adjusts based on position age, profit level, and volatility.
    
    The function makes the trailing stop more aggressive (closer to price) as:
    1. Position age increases
    2. Profit increases
    3. Volatility decreases
    
    Args:
        current_price (float): Current price
        high (float): Current bar high
        low (float): Current bar low
        position_age (int): Number of bars in the position
        position_high (float): Highest price reached during the position
        entry_price (float): Entry price of the position
        atr (float): Current Average True Range value
        atr_multiplier (float): Base multiplier for ATR
    
    Returns:
        float: Adaptive trailing stop level
    """
    # Calculate price movement and profit percentage
    price_movement = position_high - entry_price
    percent_move = price_movement / entry_price
    
    # Base stop loss using ATR
    base_stop = entry_price - (atr * atr_multiplier)
    
    # If we're not in profit, use the base stop
    if percent_move <= 0:
        return base_stop
    
    # Adjust trailing stop based on position age and profit
    # For newer positions, keep wider stops
    if position_age <= 3:
        # For very young positions, use less aggressive trailing
        stop_level = position_high - (atr * atr_multiplier * 0.8)
    elif position_age <= 5:
        # Slightly more aggressive for positions held 4-5 bars
        stop_level = position_high - (atr * atr_multiplier * 0.7)
    elif position_age <= 8:
        # More aggressive for positions held 6-8 bars
        stop_level = position_high - (atr * atr_multiplier * 0.5)
    else:
        # Most aggressive for mature positions (9+ bars)
        stop_level = position_high - (atr * atr_multiplier * 0.3)
    
    # For significant profit (e.g., > 2%), tighten stop even more
    if percent_move > 0.05:  # More than 5% move
        # Weighted average of current stop and a tighter level
        stop_level = 0.3 * stop_level + 0.7 * (position_high - (atr * 0.5))
    elif percent_move > 0.02:  # More than 2% move
        stop_level = 0.5 * stop_level + 0.5 * (position_high - (atr * 0.8))
    
    # Ensure stop is never lower than the base stop (original stop loss)
    stop_level = max(stop_level, base_stop)
    
    # Ensure trailing stop never goes below the entry price once we've moved a certain amount
    if percent_move > 0.01 and position_age > 2:  # 1% move and at least 3 bars
        stop_level = max(stop_level, entry_price)
    
    return stop_level

def create_regime_aware_position_sizer(
    price, volatility_window=14, adx_window=14, rsi_window=14, 
    bb_window=20, max_position_size=1.0, min_position_size=0.1, 
    adx_threshold=25, volatility_scale=True, risk_target=0.01
):
    """
    Creates a position sizing function that adapts to market regime (trending vs ranging).
    
    Args:
        price (pd.Series or np.array): Price data
        volatility_window (int): Window for ATR volatility calculation
        adx_window (int): Window for ADX calculation
        rsi_window (int): Window for RSI calculation
        bb_window (int): Window for Bollinger Bands calculation
        max_position_size (float): Maximum position size as fraction of portfolio
        min_position_size (float): Minimum position size as fraction of portfolio
        adx_threshold (int): ADX threshold for trend identification
        volatility_scale (bool): Whether to scale by volatility
        risk_target (float): Target risk per trade as fraction of portfolio
        
    Returns:
        function: Position sizing function
    """
    import numpy as np
    import pandas as pd
    
    # Convert price to numpy array
    price_np = np.asarray(price, dtype=np.float32)
    
    # Calculate volatility (ATR-based)
    def calculate_simple_atr(prices, window):
        # Ensure window is an integer
        window = int(window)
        
        ranges = np.zeros_like(prices)
        
        for i in range(1, len(prices)):
            ranges[i] = np.abs(prices[i] - prices[i-1])
        
        # Calculate average range
        atr = np.zeros_like(ranges)
        for i in range(window, len(ranges)):
            atr[i] = np.mean(ranges[i-window+1:i+1])
        
        # Fill initial values
        for i in range(window):
            atr[i] = atr[window]
            
        return atr
    
    # Calculate ADX for trend identification
    def calculate_simple_adx(prices, window):
        # Ensure window is an integer
        window = int(window)
        
        # For simplicity, we'll use a momentum-based proxy for ADX
        # This isn't accurate ADX but serves as a trend strength indicator
        momentum = np.zeros_like(prices)
        
        for i in range(window, len(prices)):
            # Measure absolute price change over window
            momentum[i] = np.abs(prices[i] - prices[i-window]) / prices[i-window] * 100
        
        # Smooth momentum to get a trend strength indicator
        adx_proxy = np.zeros_like(momentum)
        for i in range(window, len(momentum)):
            adx_proxy[i] = np.mean(momentum[i-window+1:i+1])
        
        # Fill initial values
        adx_proxy[:window] = adx_proxy[window]
        
        return adx_proxy
    
    # Calculate RSI for market extremes
    def calculate_simple_rsi(prices, window):
        # Ensure window is an integer
        window = int(window)
        
        deltas = np.diff(prices)
        deltas = np.append(deltas, 0)  # Add 0 to make same length as prices
        
        # Separate gains and losses
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        # Calculate average gains and losses
        avg_gain = np.zeros_like(gains)
        avg_loss = np.zeros_like(losses)
        
        # Calculate average gains and losses
        for i in range(window, len(gains)):
            avg_gain[i] = np.mean(gains[i-window+1:i+1])
            avg_loss[i] = np.mean(losses[i-window+1:i+1])
        
        # Calculate RS and RSI
        rs = np.zeros_like(avg_gain)
        for i in range(window, len(avg_gain)):
            if avg_loss[i] == 0:
                rs[i] = 100  # Avoid division by zero
            else:
                rs[i] = avg_gain[i] / avg_loss[i]
        
        rsi = 100 - (100 / (1 + rs))
        
        # Fill initial values
        rsi[:window] = 50
        
        return rsi
    
    # Calculate trend strength
    adx = calculate_simple_adx(price_np, adx_window)
    
    # Calculate RSI
    rsi = calculate_simple_rsi(price_np, rsi_window)
    
    def position_size(i, is_long, sl_pct=None):
        """
        Calculate position size based on market regime and volatility.
        
        Args:
            i (int): Current bar index
            is_long (bool): True for long positions, False for short positions
            sl_pct (float, optional): Stop loss percentage if different from default
            
        Returns:
            float: Position size as fraction of portfolio
        """
        if i < max(volatility_window, adx_window, rsi_window) or i >= len(price_np):
            return min_position_size
            
        # Determine market regime
        is_trending = adx[i] > adx_threshold
        
        # Base position size
        if is_trending:
            # Higher size in trending markets
            base_size = max_position_size
            
            # Trend strength scaling
            trend_strength = min(adx[i] / 50, 1.0)  # Cap at 1.0
            base_size *= (0.7 + 0.3 * trend_strength)  # Scale by trend strength
            
            # Reduce size at market extremes in a trend
            if is_long and rsi[i] > 75:
                # Scale down size as RSI approaches overbought
                rsi_factor = 1.0 - ((rsi[i] - 75) / 25) * 0.5  # Reduce up to 50%
                base_size *= max(rsi_factor, 0.5)
            elif not is_long and rsi[i] < 25:
                # Scale down size as RSI approaches oversold
                rsi_factor = 1.0 - ((25 - rsi[i]) / 25) * 0.5  # Reduce up to 50%
                base_size *= max(rsi_factor, 0.5)
        else:
            # Lower size in ranging markets
            base_size = max_position_size * 0.7  # 70% of max in ranges
            
            # RSI extremes provide better entry in ranges, so increase size
            if is_long and rsi[i] < 30:
                # Scale up size as RSI becomes more oversold
                base_size *= min(1.0 + (30 - rsi[i]) / 30 * 0.5, 1.5)  # Increase up to 50%
            elif not is_long and rsi[i] > 70:
                # Scale up size as RSI becomes more overbought
                base_size *= min(1.0 + (rsi[i] - 70) / 30 * 0.5, 1.5)  # Increase up to 50%
        
        # Volatility scaling if enabled
        if volatility_scale:
            # Use stop loss or calculate based on ATR
            if sl_pct is None:
                volatility_adjusted_sl = atr_pct[i] * 2  # Default to 2x ATR
            else:
                volatility_adjusted_sl = sl_pct
                
            # Scale for constant risk (inverse relationship with stop size)
            vol_scaling = risk_target / volatility_adjusted_sl
            
            # Apply volatility scaling with limits
            base_size *= min(max(vol_scaling, 0.5), 2.0)  # Limit scaling between 0.5x and 2x
        
        # Ensure position size is within bounds
        return max(min(base_size, max_position_size), min_position_size)
        
    return position_size

# ==============================================================================
# Strategy Class with Simplified Interface to Match Backtest Expectations
# ==============================================================================
class EdgeMultiFactorStrategy:
    """
    Edge Multi-Factor Strategy that integrates multiple technical and statistical indicators
    to identify high-probability trading opportunities.
    """

    def __init__(self, **kwargs):
        """Initialize strategy parameters with defaults."""
        # Core parameters - Ensure window parameters are integers
        self.lookback_window = int(kwargs.get('lookback_window', 20))
        self.volatility_threshold = kwargs.get('volatility_threshold', 0.5)
        self.volume_threshold = kwargs.get('volume_threshold', 1.5)
        self.position_size_window = int(kwargs.get('position_size_window', self.lookback_window)) # Ensure int
        
        # Exit parameters
        self.take_profit = kwargs.get('take_profit', 0.04)  # 4% default take profit
        self.stop_loss = kwargs.get('stop_loss', 0.02)      # 2% default stop loss
        self.time_stop = int(kwargs.get('time_stop', 10))  # Ensure int
        
        # Indicator settings - Ensure window parameters are integers
        self.vol_filter_window = int(kwargs.get('vol_filter_window', self.lookback_window * 2.5))
        self.market_regime_window = int(kwargs.get('market_regime_window', self.lookback_window * 2))
        self.trend_window = int(kwargs.get('trend_window', self.lookback_window * 3))
        self.rsi_window = int(kwargs.get('rsi_window', 14))
        self.bb_window = int(kwargs.get('bb_window', 20))
        self.macd_fast = int(kwargs.get('macd_fast', 12))
        self.macd_slow = int(kwargs.get('macd_slow', 26))
        self.macd_signal = int(kwargs.get('macd_signal', 9))

        # Performance parameters
        self.risk_target = kwargs.get('risk_target', 0.01)  # 1% risk per trade
        self.max_position_size = kwargs.get('max_position_size', 0.25)  # 25% max allocation
        self.min_position_size = kwargs.get('min_position_size', 0.05)  # 5% min allocation
        
        # Basic configuration params
        self.symbol = kwargs.get('symbol', 'BTCUSDT')
        self.timeframe = kwargs.get('timeframe', '1h')
        self.signal_threshold = kwargs.get('signal_threshold', 0.2)
        self.signal_smoothing = int(kwargs.get('signal_smoothing', 2)) # Ensure int
        
        # Factor weights
        self.trend_weight = kwargs.get('trend_weight', 0.25)  # For RSI
        self.momentum_weight = kwargs.get('momentum_weight', 0.25)  # For BBands
        self.mean_reversion_weight = kwargs.get('mean_reversion_weight', 0.25)  # For MACD
        self.volume_weight = kwargs.get('volume_weight', 0.25)  # For Volume Divergence
        
        # Volume parameters
        self.volume_threshold_short = kwargs.get('volume_threshold_short', 1.2)
        
        # RSI parameters - Ensure window is integer
        self.rsi_period = int(kwargs.get('rsi_period', self.rsi_window)) # Use rsi_window if rsi_period missing
        
        # Bollinger Bands parameters - Ensure window is integer
        self.bbands_period = int(kwargs.get('bbands_period', self.bb_window)) # Use bb_window if bbands_period missing
        self.bbands_dev = kwargs.get('bbands_dev', 2.0)
        
        # MACD parameters - Ensure periods are integers
        self.fast_ma_period = int(kwargs.get('fast_ma_period', self.macd_fast)) # Use macd_fast if missing
        self.slow_ma_period = int(kwargs.get('slow_ma_period', self.macd_slow)) # Use macd_slow if missing
        
        # Regime adaptation parameters - Ensure window is integer
        self.use_regime_filter = kwargs.get('use_regime_filter', True)
        self.adx_threshold = kwargs.get('adx_threshold', 25) # ADX threshold is float/int, not window
        self.ranging_signal_discount = kwargs.get('ranging_signal_discount', 0.5)
        self.ranging_market_adjustment = kwargs.get('ranging_market_adjustment', True)
        self.disable_shorts_in_uptrend = kwargs.get('disable_shorts_in_uptrend', False)
        self.disable_longs_in_downtrend = kwargs.get('disable_longs_in_downtrend', False)
        self.ranging_factor = kwargs.get('ranging_factor', 0.5)  # Factor to reduce signal strength in ranging markets
        
        # Exit strategy parameters - Ensure window is integer
        self.use_regime_exits = kwargs.get('use_regime_exits', True)
        self.trending_tp_multiplier = kwargs.get('trending_tp_multiplier', 3.0)
        self.trending_sl_multiplier = kwargs.get('trending_sl_multiplier', 2.0)
        self.ranging_tp_multiplier = kwargs.get('ranging_tp_multiplier', 1.5)
        self.ranging_sl_multiplier = kwargs.get('ranging_sl_multiplier', 1.0)
        self.max_bars_exit = int(kwargs.get('max_bars_exit', 20)) # Ensure int
        
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
        
    def calculate_target_percent(self, price_data, risk_fraction=0.01, atr_window=14, atr_multiple_stop=2.0, volume_strength=None):
        """
        Calculates the target percent for each position based on risk, ATR, and volume strength.
        
        Args:
            price_data (pd.DataFrame): DataFrame with OHLCV data
            risk_fraction (float): Fraction of capital to risk per trade (e.g., 0.01 = 1%)
            atr_window (int): Window for ATR calculation
            atr_multiple_stop (float): Multiple of ATR for stop loss distance
            volume_strength (pd.Series, optional): Series of volume strength values (0-1) to adjust position size
            
        Returns:
            Series of target percentages
        """
        # Calculate ATR using our class method
        atr = self.calculate_atr(price_data, window=atr_window)
        
        # Stop loss distance in price points
        stop_distance = atr * atr_multiple_stop
        
        # Stop loss as percentage of price
        stop_percent = stop_distance / price_data['close']
        
        # Position size as percentage of capital
        # If we're risking risk_fraction (e.g. 1%) per trade, and stop is stop_percent away,
        # then position size should be risk_fraction / stop_percent
        target_percent = risk_fraction / stop_percent
        
        # Apply volume strength scaling if provided
        if volume_strength is not None:
            # Convert to Series if not already
            if not isinstance(volume_strength, pd.Series):
                volume_strength = pd.Series(volume_strength, index=price_data.index)
                
            # Scale position size based on volume strength (0.75-1.25 scaling range)
            # 0 strength -> 0.75x position size
            # 0.5 strength -> 1.0x position size (neutral)
            # 1.0 strength -> 1.25x position size
            vol_scaling = 0.75 + (volume_strength * 0.5)
            
            # Apply scaling
            target_percent = target_percent * vol_scaling
        
        # Cap the target percent to avoid excessive leverage
        max_target_percent = 0.25  # Maximum 25% of capital per trade
        target_percent = np.minimum(target_percent, max_target_percent)
        
        # Ensure no invalid values
        target_percent = target_percent.replace([np.inf, -np.inf], 0).fillna(0)
        
        return target_percent
        
    def backtest_signals(self, df, signals_df, plot=False):
        """
        Backtest the signals using a simplified approach that doesn't rely on vectorbtpro's Portfolio.from_signals.
        This avoids the 'flags variable (overflow)' error that can occur with certain Python versions.
        
        Args:
            df (pd.DataFrame): OHLCV dataframe
            signals_df (pd.DataFrame): DataFrame containing signals and exits
            plot (bool): Whether to plot the results
            
        Returns:
            dict: Backtest results
        """
        try:
            # Initialize results with default values
            results = {
                'total_return': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'win_rate': 0.0,
                'num_trades': 0,
                'profit_factor': 0.0
            }
            
            # Get price and signals
            price = df['close'].copy()
            entries = signals_df['long_signal'].astype(bool)
            exits = signals_df['long_exit'].astype(bool)
            
            # If no entry signals, return default results
            if entries.sum() == 0:
                logger.warning("No entry signals found for backtest")
                return results
            
            # Log signal information
            logger.info(f"Number of entry signals: {entries.sum()}")
            logger.info(f"Number of exit signals: {exits.sum()}")
            
            # Create a position series (1 when in position, 0 when not)
            position = pd.Series(0, index=price.index)
            entry_prices = pd.Series(0.0, index=price.index)
            trades = []
            
            # Simulate trades
            in_position = False
            entry_price = 0.0
            entry_idx = 0
            
            for i in range(1, len(price)):
                # Entry logic
                if not in_position and entries.iloc[i]:
                    in_position = True
                    entry_price = price.iloc[i]
                    entry_idx = i
                    position.iloc[i] = 1
                    entry_prices.iloc[i] = entry_price
                    
                # Stay in position if already in
                elif in_position and not exits.iloc[i]:
                    position.iloc[i] = 1
                    
                # Exit logic
                elif in_position and exits.iloc[i]:
                    # Record trade result
                    exit_price = price.iloc[i]
                    trade_return = (exit_price / entry_price) - 1
                    trade_duration = i - entry_idx
                    
                    trades.append({
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'entry_idx': entry_idx,
                        'exit_idx': i,
                        'return': trade_return,
                        'duration': trade_duration,
                        'win': trade_return > 0
                    })
                    
                    # Reset position
                    in_position = False
                    position.iloc[i] = 0
                    
                # Otherwise maintain current position state
                else:
                    position.iloc[i] = position.iloc[i-1]
            
            # Force exit at the end if still in position
            if in_position:
                exit_price = price.iloc[-1]
                trade_return = (exit_price / entry_price) - 1
                trade_duration = len(price) - 1 - entry_idx
                
                trades.append({
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'entry_idx': entry_idx,
                    'exit_idx': len(price) - 1,
                    'return': trade_return,
                    'duration': trade_duration,
                    'win': trade_return > 0
                })
            
            # If no trades were generated, return default results
            if not trades:
                logger.warning("No trades generated in backtest")
                return results
            
            # Calculate daily returns
            daily_returns = price.pct_change() * position.shift(1)
            daily_returns.iloc[0] = 0  # Set first day return to 0
            
            # Calculate cumulative returns
            cumulative_returns = (1 + daily_returns).cumprod() - 1
            
            # Calculate trade metrics
            total_return = cumulative_returns.iloc[-1]
            
            # Get maximum drawdown
            rolling_max = cumulative_returns.cummax()
            drawdown = (cumulative_returns - rolling_max) / (1 + rolling_max)
            max_drawdown = drawdown.min()
            
            # Calculate Sharpe ratio (annualized)
            daily_risk_free_rate = 0.0  # Assuming risk-free rate of 0
            excess_returns = daily_returns - daily_risk_free_rate
            sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)  # Annualized
            
            # Calculate win rate and profit factor
            wins = [t for t in trades if t['win']]
            losses = [t for t in trades if not t['win']]
            
            win_rate = len(wins) / len(trades) if trades else 0
            
            total_wins = sum(t['return'] for t in wins)
            total_losses = abs(sum(t['return'] for t in losses))
            profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
            
            # Update results
            results['total_return'] = total_return
            results['sharpe_ratio'] = sharpe_ratio
            results['max_drawdown'] = max_drawdown
            results['win_rate'] = win_rate
            results['profit_factor'] = profit_factor
            results['num_trades'] = len(trades)
            
            # Log summary
            logger.info(f"Backtest completed with {len(trades)} trades")
            logger.info(f"Total return: {total_return:.2%}")
            logger.info(f"Sharpe ratio: {sharpe_ratio:.2f}")
            logger.info(f"Max drawdown: {max_drawdown:.2%}")
            logger.info(f"Win rate: {win_rate:.2%}")
            
            # Plot results if requested
            if plot:
                import matplotlib.pyplot as plt
                
                plt.figure(figsize=(12, 8))
                
                # Plot cumulative returns
                plt.subplot(2, 1, 1)
                cumulative_returns.plot()
                plt.title('Cumulative Returns')
                plt.grid(True)
                
                # Plot equity curve
                plt.subplot(2, 1, 2)
                equity_curve = (1 + cumulative_returns) * 100  # Start with $100
                equity_curve.plot()
                plt.title('Equity Curve')
                plt.grid(True)
                
                plt.tight_layout()
                plt.savefig('backtest_results.png')
                plt.close()
                
                logger.info("Backtest plot saved to backtest_results.png")
            
            return results
            
        except Exception as e:
            logger.error(f"Backtest failed: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                'total_return': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'win_rate': 0.0,
                'num_trades': 0,
                'profit_factor': 0.0
            }

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
        
        # Convert ATR to numpy array if it's a pandas Series to avoid iloc errors
        is_atr_series = isinstance(atr, pd.Series)
        if is_atr_series:
            atr_values = atr.values
        else:
            atr_values = atr
        
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
            if long_signals.iloc[i] and not long_active:
                long_active = True
                long_entry_price = close.iloc[i]
                long_entry_idx = i
            
            # Check for short entry
            if short_signals.iloc[i] and not short_active:
                short_active = True
                short_entry_price = close.iloc[i]
                short_entry_idx = i
            
            # Skip if no active positions
            if not long_active and not short_active:
                continue
            
            # Define regime-specific exit parameters
            if market_regimes.iloc[i]:  # Trending regime
                # Wider stops in trending markets, trailing stops
                long_take_profit = 0.03  # 3% take profit in trending markets
                long_stop_loss = 0.015   # 1.5% stop loss
                short_take_profit = 0.03
                short_stop_loss = 0.015
                
                # Add trailing stop logic for trending markets
                if long_active and i > long_entry_idx:
                    # Update stop loss based on trailing ATR
                    highest_since_entry = close.iloc[long_entry_idx:i+1].max()
                    trailing_stop = highest_since_entry - 2 * atr_values[i]
                    if close.iloc[i] <= trailing_stop and highest_since_entry > long_entry_price * 1.01:
                        long_exits.iloc[i] = True
                        long_active = False
                
                if short_active and i > short_entry_idx:
                    # Update stop loss based on trailing ATR
                    lowest_since_entry = close.iloc[short_entry_idx:i+1].min()
                    trailing_stop = lowest_since_entry + 2 * atr_values[i]
                    if close.iloc[i] >= trailing_stop and lowest_since_entry < short_entry_price * 0.99:
                        short_exits.iloc[i] = True
                        short_active = False
            else:  # Ranging regime
                # Tighter stops in ranging markets, quicker to take profits
                long_take_profit = 0.015  # 1.5% take profit in ranging markets
                long_stop_loss = 0.01    # 1% stop loss
                short_take_profit = 0.015
                short_stop_loss = 0.01
            
            # Check for take profit and stop loss for long positions
            if long_active:
                if close.iloc[i] >= long_entry_price * (1 + long_take_profit):
                    long_exits.iloc[i] = True
                    long_active = False
                elif close.iloc[i] <= long_entry_price * (1 - long_stop_loss):
                    long_exits.iloc[i] = True
                    long_active = False
            
            # Check for take profit and stop loss for short positions
            if short_active:
                if close.iloc[i] <= short_entry_price * (1 - short_take_profit):
                    short_exits.iloc[i] = True
                    short_active = False
                elif close.iloc[i] >= short_entry_price * (1 + short_stop_loss):
                    short_exits.iloc[i] = True
                    short_active = False
            
            # Additional regime-based exits
            if long_active:
                # Exit long positions when entering ranging market after profit
                if not market_regimes.iloc[i] and market_regimes.iloc[i-1] and close.iloc[i] > long_entry_price:
                    long_exits.iloc[i] = True
                    long_active = False
            
            if short_active:
                # Exit short positions when entering ranging market after profit
                if not market_regimes.iloc[i] and market_regimes.iloc[i-1] and close.iloc[i] < short_entry_price:
                    short_exits.iloc[i] = True
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
        
        # Detect market regime for volume adaptation
        is_trending = self.detect_market_regime(data)
        is_ranging = ~is_trending
        
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
        
        # Create hour of day data for time-based filtering
        hour_of_day = None
        if isinstance(data.index, pd.DatetimeIndex):
            hour_of_day = data.index.hour
        
        # Calculate ATR as volatility data for adaptive thresholds
        volatility_data = None
        try:
            # Use the imported calculate_atr function directly
            volatility_data = calculate_atr(high, low, close, 14)
        except Exception as e:
            # Log the exception
            logger.warning(f"Error calculating ATR: {str(e)}")
            # Calculate simple ATR as fallback
            tr1 = data['high'] - data['low']
            tr2 = abs(data['high'] - data['close'].shift())
            tr3 = abs(data['low'] - data['close'].shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            volatility_data = tr.rolling(window=14).mean()
        
        # Use enhanced volume divergence indicator with additional parameters
        voldiv_long, voldiv_short, volume_strength = create_volume_divergence_indicator(
            volume=volume,
            lookback_window=self.lookback_window,
            breakout_up=breakout_up,
            breakout_down=breakout_down,
            volume_threshold=self.volume_threshold,
            volume_threshold_short=self.volume_threshold_short,
            volume_roc_threshold=0.1,
            is_trending=is_trending,
            is_ranging=is_ranging,
            price=close,
            hour_of_day=hour_of_day,
            volatility_data=volatility_data,
            session_filter=True,
            adaptive_threshold=True
        )
        
        return {
            'rsi_long': rsi_long,
            'rsi_short': rsi_short,
            'bb_long': bb_long,
            'bb_short': bb_short,
            'macd_long': macd_long,
            'macd_short': macd_short,
            'voldiv_long': voldiv_long,
            'voldiv_short': voldiv_short,
            'volume_strength': volume_strength  # Add volume strength as additional signal
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

    def run_strategy(self, data, test_mode=False):
        """
        Run the strategy on price data.
        
        Args:
            data: DataFrame with price data (OHLCV)
            test_mode: If True, don't run backtest
            
        Returns:
            tuple: (signals, market_regimes, strategy_dataframe)
        """
        try:
            # Ensure data is a copy to avoid modifying original
            df = data.copy()
            
            # Ensure all columns are lowercase
            df.columns = [col.lower() for col in df.columns]
            
            # Make sure we have all required columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                logger.error(f"Missing required columns: {missing_cols}")
                return None, None, None
            
            # ------------- Data Cleanup --------------
            # Remove any rows with NaN, inf, or -inf in critical columns
            df = df.replace([np.inf, -np.inf], np.nan)
            df.dropna(subset=['close', 'high', 'low'], inplace=True)
            
            # Ensure proper data types to prevent overflow errors
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(np.float64)
                
            # Check for zero or negative values in critical columns
            if (df['close'] <= 0).any() or (df['high'] <= 0).any() or (df['low'] <= 0).any():
                logger.error("Found zero or negative values in price data")
                # Replace with small positive values to prevent division by zero
                df.loc[df['close'] <= 0, 'close'] = df['close'].median() * 0.001
                df.loc[df['high'] <= 0, 'high'] = df['high'].median() * 0.001
                df.loc[df['low'] <= 0, 'low'] = df['low'].median() * 0.001

            # Calculate price stats for logging extreme values
            price_stats = {
                'min': float(df['close'].min()),
                'max': float(df['close'].max()),
                'mean': float(df['close'].mean()),
                'std': float(df['close'].std())
            }
            logger.debug(f"Price stats: {price_stats}")
                
            # --------------- Market Regimes ---------------
            # Identify market regimes (trending, ranging, etc.)
            market_regimes = self._identify_market_regimes(df)
            
            # Log regime statistics
            trend_count = (market_regimes == 'trending').sum()
            range_count = (market_regimes == 'ranging').sum()
            total_count = len(market_regimes)
            
            trend_pct = trend_count / total_count * 100 if total_count > 0 else 0
            range_pct = range_count / total_count * 100 if total_count > 0 else 0
            
            logger.info(f"Market regime statistics: Trending: {trend_pct:.1f}%, Ranging: {range_pct:.1f}%")
            
            # ----- Generate Base Signals -----
            # Initialize strategy dataframe with price and indicators
            strategy_df = df.copy()
            
            # Add RSI
            rsi = self._calculate_rsi(df['close'])
            strategy_df['rsi'] = rsi
            
            # Add Bollinger Bands
            bb_upper, bb_lower, bb_width = self._calculate_bb(df['close'])
            strategy_df['bb_upper'] = bb_upper
            strategy_df['bb_lower'] = bb_lower
            strategy_df['bb_width'] = bb_width
            
            # Add Volatility (ATR-based)
            volatility = self._calculate_volatility(df)
            strategy_df['volatility'] = volatility
            
            # Add volume indicators
            if 'volume' in df.columns:
                strategy_df = self._add_volume_indicators(strategy_df)
            
            # ---------------- Combined Signals ---------------
            
            # Initialize signal columns
            strategy_df['long_signal'] = False
            strategy_df['short_signal'] = False
            strategy_df['long_exit'] = False
            strategy_df['short_exit'] = False
            
            # Convert to numeric true/false to 1.0/0.0 for vbt
            for signal_col in ['long_signal', 'short_signal', 'long_exit', 'short_exit']:
                strategy_df[signal_col] = strategy_df[signal_col].astype(float)
            
            # Generate factor-based signals using multi-factor approach
            strategy_df = self._generate_multi_factor_signals(strategy_df, market_regimes)
            
            # Ensure signals are properly created with valid values
            for signal_col in ['long_signal', 'short_signal', 'long_exit', 'short_exit']:
                # Handle any NaN values
                strategy_df[signal_col] = strategy_df[signal_col].fillna(0.0)
                # Ensure signals are properly typed as float64
                strategy_df[signal_col] = strategy_df[signal_col].astype(np.float64)
                # Count signals for debugging
                signal_count = strategy_df[signal_col].sum()
                logger.debug(f"{signal_col} count: {signal_count}")
            
            # ---------- Run Backtest if not in test mode ----------
            if not test_mode:
                return strategy_df, market_regimes, strategy_df
            
            return strategy_df, market_regimes, df
            
        except Exception as e:
            logger.error(f"Error running strategy: {str(e)}")
            return None, None, None

    def calculate_atr(self, data, window=14):
        """
        Calculate Average True Range (ATR) for the given data
        
        Args:
            data (pd.DataFrame): DataFrame with OHLCV data
            window (int): Window for ATR calculation
            
        Returns:
            pd.Series: ATR values
        """
        try:
            # First try using the imported function if available
            return calculate_atr(data['high'], data['low'], data['close'], window)
        except Exception as e:
            logger.warning(f"Error calculating ATR with imported function: {str(e)}")
            
            # Fallback calculation
            high = data['high']
            low = data['low']
            close = data['close']
            
            # Calculate True Range
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            
            # Combine into True Range
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            
            # Calculate ATR as exponential moving average of True Range
            atr = tr.ewm(span=window, adjust=False).mean()
            
            return atr

    def calculate_volatility(self, df):
        """
        Calculate rolling volatility of price.
        
        Args:
            df (pd.DataFrame): OHLCV dataframe
            
        Returns:
            pd.Series: Volatility
        """
        # Ensure window is an integer for Numba compatibility
        window = int(self.lookback_window)  
        # Calculate returns
        returns = df['close'].pct_change().fillna(0)
        
        # Calculate rolling standard deviation and annualize
        volatility = returns.rolling(window=window, min_periods=int(window * 0.5)).std() * np.sqrt(252)
        
        # Filter extremely low volatility values that might be numerical errors
        volatility[volatility < 0.001] = 0.001
        
        return volatility

    def calculate_rsi(self, df, window=14):
        """
        Calculate the Relative Strength Index (RSI).
        
        Args:
            df (pd.DataFrame): OHLCV dataframe
            window (int): RSI window
            
        Returns:
            pd.Series: RSI values
        """
        # Ensure window is an integer for Numba compatibility
        window = int(window)
        
        # Calculate price changes
        delta = df['close'].diff()
        
        # Create gain and loss series
        gain = delta.copy()
        loss = delta.copy()
        gain[gain < 0] = 0
        loss[loss > 0] = 0
        loss = -loss  # Make positive
        
        # Calculate average gain and loss
        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    def calculate_bollinger_bands(self, df, window=20, alpha=2.0):
        """
        Calculate Bollinger Bands.
        
        Args:
            df (pd.DataFrame): OHLCV dataframe
            window (int): Window for moving average
            alpha (float): Number of standard deviations
            
        Returns:
            tuple: Upper band, middle band, lower band
        """
        # Ensure window is an integer for Numba compatibility
        window = int(window)
        
        # Calculate middle band (SMA)
        middle_band = df['close'].rolling(window=window, min_periods=int(window * 0.5)).mean()
        
        # Calculate standard deviation
        std = df['close'].rolling(window=window, min_periods=int(window * 0.5)).std()
        
        # Calculate upper and lower bands
        upper_band = middle_band + (alpha * std)
        lower_band = middle_band - (alpha * std)
        
        return upper_band, middle_band, lower_band

    def create_volatility_regime_indicator(self, data):
        """
        Calculate volatility regime based on rolling standard deviation of returns.
        Returns a signal of 1 when volatility is increasing beyond threshold.
        
        Args:
            data (pd.DataFrame): Price data with OHLCV columns
            
        Returns:
            pd.Series: Boolean indicator True when volatility regime is favorable
        """
        # Compute log returns
        returns = np.log(data['close'] / data['close'].shift(1))
        
        # Calculate rolling volatility (standard deviation of returns)
        vol = returns.rolling(window=self.lookback_window).std()
        
        # Calculate rate of change in volatility
        vol_change = vol / vol.shift(self.lookback_window // 2) - 1
        
        # Generate signal when volatility increases significantly
        signal = vol_change > self.volatility_threshold
        
        return signal

    def create_relative_volume_indicator(self, data):
        """
        Calculate relative volume indicator to detect significant volume increases.
        
        Args:
            data (pd.DataFrame): Price data with OHLCV columns
            
        Returns:
            pd.Series: Boolean indicator True when volume is significantly above average
        """
        # Calculate rolling average volume
        avg_volume = data['volume'].rolling(window=self.lookback_window).mean()
        
        # Calculate relative volume (current volume / average volume)
        rel_volume = data['volume'] / avg_volume
        
        # Generate signal when volume is significantly above average
        signal = rel_volume > self.volume_threshold
        
        return signal

    def create_indicators(self, data):
        """
        Calculate technical indicators for each ticker.
        
        Args:
            data (dict): Dictionary mapping tickers to OHLCV DataFrames
            
        Returns:
            dict: Dictionary mapping tickers to DataFrames with indicators
        """
        for ticker, ohlc in data.items():
            # Base indicators (already implemented)
            ohlc['sma_signal'] = self.create_sma_crossover_indicator(ohlc)
            ohlc['rsi_signal'] = self.create_rsi_indicator(ohlc)
            ohlc['bb_signal'] = self.create_bollinger_bands_indicator(ohlc)
            
            # Add our new indicators
            ohlc['volatility_regime'] = self.create_volatility_regime_indicator(ohlc)
            ohlc['volume_signal'] = self.create_relative_volume_indicator(ohlc)
            
            # Calculate combined signal (require all signals to be True)
            ohlc['combined_signal'] = (
                ohlc['sma_signal'] &
                ohlc['rsi_signal'] &
                ohlc['bb_signal'] &
                ohlc['volatility_regime'] &
                ohlc['volume_signal']
            )
            
            data[ticker] = ohlc
            
        return data

    def _identify_market_regimes(self, data):
        """
        Identify market regimes (trending, ranging) using ADX indicator.
        
        Args:
            data (pd.DataFrame): OHLCV data
            
        Returns:
            pd.Series: Series with values 'trending' or 'ranging'
        """
        try:
            # Calculate ADX
            if hasattr(vbt, 'ADX'):
                adx_ind = vbt.ADX.run(
                    data['high'], 
                    data['low'], 
                    data['close'], 
                    window=14
                )
                adx = adx_ind.adx
            else:
                # Fallback calculation if ADX not available directly
                # Calculate +DI and -DI
                tr1 = data['high'] - data['low']
                tr2 = (data['high'] - data['close'].shift(1)).abs()
                tr3 = (data['low'] - data['close'].shift(1)).abs()
                tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
                atr = tr.rolling(window=14).mean()
                
                # Calculate +DM and -DM
                high_diff = data['high'].diff()
                low_diff = data['low'].diff()
                
                plus_dm = pd.Series(0, index=data.index)
                minus_dm = pd.Series(0, index=data.index)
                
                plus_dm.loc[(high_diff > 0) & (high_diff > low_diff.abs())] = high_diff
                minus_dm.loc[(low_diff < 0) & (low_diff.abs() > high_diff)] = low_diff.abs()
                
                # Calculate +DI and -DI
                plus_di = 100 * (plus_dm.rolling(window=14).mean() / atr)
                minus_di = 100 * (minus_dm.rolling(window=14).mean() / atr)
                
                # Calculate DX
                dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di))
                
                # Calculate ADX
                adx = dx.rolling(window=14).mean()
            
            # Define regime thresholds
            adx_threshold = 25  # ADX above 25 indicates trending market
            
            # Create regime series
            is_trending = adx > adx_threshold
            
            # Convert boolean to string labels
            regimes = pd.Series('ranging', index=data.index)
            regimes[is_trending] = 'trending'
            
            # Log regime statistics
            trend_count = (regimes == 'trending').sum()
            range_count = (regimes == 'ranging').sum()
            total_count = len(regimes)
            
            trend_pct = trend_count / total_count * 100 if total_count > 0 else 0
            range_pct = range_count / total_count * 100 if total_count > 0 else 0
            
            logger.info(f"Market regimes: Trending: {trend_pct:.1f}%, Ranging: {range_pct:.1f}%")
            
            return regimes
            
        except Exception as e:
            logger.error(f"Error identifying market regimes: {str(e)}")
            # Return default regime (all ranging) if error occurs
            return pd.Series('ranging', index=data.index)

    def _calculate_rsi(self, price, window=14):
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            price (pd.Series): Price series
            window (int): RSI window
            
        Returns:
            pd.Series: RSI values
        """
        try:
            # Calculate price changes
            delta = price.diff()
            
            # Separate gains and losses
            gains = delta.copy()
            losses = delta.copy()
            gains[gains < 0] = 0
            losses[losses > 0] = 0
            losses = -losses  # Make losses positive
            
            # Calculate average gains and losses
            avg_gain = gains.rolling(window=window).mean()
            avg_loss = losses.rolling(window=window).mean()
            
            # Calculate RS and RSI
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return pd.Series(50, index=price.index)  # Default neutral RSI
            
    def _calculate_bb(self, price, window=20, num_std=2.0):
        """
        Calculate Bollinger Bands.
        
        Args:
            price (pd.Series): Price series
            window (int): Window for moving average
            num_std (float): Number of standard deviations
            
        Returns:
            tuple: (upper band, lower band, bandwidth)
        """
        try:
            # Calculate moving average (middle band)
            ma = price.rolling(window=window).mean()
            
            # Calculate standard deviation
            std = price.rolling(window=window).std()
            
            # Calculate upper and lower bands
            upper_band = ma + (std * num_std)
            lower_band = ma - (std * num_std)
            
            # Calculate bandwidth
            bandwidth = (upper_band - lower_band) / ma
            
            return upper_band, lower_band, bandwidth
            
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            # Return default values
            default = pd.Series(price, index=price.index)
            return default, default, pd.Series(0.04, index=price.index)
            
    def _calculate_volatility(self, data, window=14):
        """
        Calculate price volatility using ATR.
        
        Args:
            data (pd.DataFrame): OHLCV dataframe
            window (int): ATR window
            
        Returns:
            pd.Series: Volatility (ATR)
        """
        try:
            high = data['high']
            low = data['low']
            close = data['close']
            
            # Calculate True Range
            tr1 = high - low
            tr2 = (high - close.shift(1)).abs()
            tr3 = (low - close.shift(1)).abs()
            
            # Combine into True Range
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            
            # Calculate ATR as simple moving average of TR
            atr = tr.rolling(window=window).mean()
            
            # Express as percentage of price for easier interpretation
            atr_pct = atr / close
            
            return atr_pct
            
        except Exception as e:
            logger.error(f"Error calculating volatility: {str(e)}")
            return pd.Series(0.02, index=data.index)  # Default 2% volatility
            
    def _add_volume_indicators(self, data):
        """
        Add volume-based indicators to the dataframe.
        
        Args:
            data (pd.DataFrame): OHLCV dataframe
            
        Returns:
            pd.DataFrame: Dataframe with added volume indicators
        """
        try:
            # Copy dataframe to avoid modifying the original
            df = data.copy()
            
            # Calculate volume moving average
            df['volume_ma'] = df['volume'].rolling(window=self.lookback_window).mean()
            
            # Calculate relative volume (current / average)
            df['rel_volume'] = df['volume'] / df['volume_ma']
            
            # Calculate volume momentum
            df['volume_momentum'] = df['volume'].pct_change(3)
            
            # Calculate volume divergence (price up, volume down or vice versa)
            price_change = df['close'].pct_change()
            volume_change = df['volume'].pct_change()
            
            df['vol_divergence'] = ((price_change > 0) & (volume_change < 0)) | ((price_change < 0) & (volume_change > 0))
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding volume indicators: {str(e)}")
            return data  # Return original data on error
            
    def _generate_multi_factor_signals(self, data, market_regimes):
        """
        Generate trading signals based on multiple factors.
        
        Args:
            data (pd.DataFrame): Dataframe with price and indicators
            market_regimes (pd.Series): Market regime classifications
            
        Returns:
            pd.DataFrame: Dataframe with signals
        """
        try:
            # Work with a copy to avoid modifying the original
            df = data.copy()
            
            # Extract prices
            close = df['close']
            
            # Define regime-specific parameters
            trending_signal_threshold = self.signal_threshold * 1.2  # Higher threshold in trending markets
            ranging_signal_threshold = self.signal_threshold * 0.8   # Lower threshold in ranging markets
            
            # --- Generate component signals ---
            
            # RSI signals
            rsi = df['rsi']
            rsi_oversold = rsi < 30
            rsi_overbought = rsi > 70
            
            # Bollinger Bands signals
            bb_lower = df['bb_lower']
            bb_upper = df['bb_upper']
            bb_width = df['bb_width']
            
            price_below_lower = close < bb_lower
            price_above_upper = close > bb_upper
            
            # Volatility signals
            volatility = df['volatility']
            vol_increasing = volatility > volatility.shift(self.lookback_window // 2)
            vol_contracting = volatility < volatility.shift(self.lookback_window // 2) * 0.8
            
            # Volume signals (if available)
            if 'rel_volume' in df.columns:
                high_volume = df['rel_volume'] > self.volume_threshold
                volume_surge = df['volume_momentum'] > 0.2
            else:
                high_volume = pd.Series(True, index=df.index)  # Default if volume not available
                volume_surge = pd.Series(False, index=df.index)
            
            # --- Combine signals based on regime ---
            
            # Initialize signal components
            long_signal_strength = pd.Series(0.0, index=df.index)
            short_signal_strength = pd.Series(0.0, index=df.index)
            
            # Generate signals for each regime
            for i in range(len(df)):
                regime = market_regimes.iloc[i]
                
                if regime == 'trending':
                    # Trending regime: focus on momentum
                    
                    # Long signal in trending market
                    long_factors = [
                        rsi_oversold.iloc[i] * 0.4,                        # RSI oversold
                        price_below_lower.iloc[i] * 0.3,                   # Price below BB
                        (vol_contracting.iloc[i] & high_volume.iloc[i]) * 0.3  # Vol pattern
                    ]
                    long_signal_strength.iloc[i] = sum(long_factors)
                    
                    # Short signal in trending market
                    short_factors = [
                        rsi_overbought.iloc[i] * 0.4,                     # RSI overbought
                        price_above_upper.iloc[i] * 0.3,                  # Price above BB
                        (vol_increasing.iloc[i] & high_volume.iloc[i]) * 0.3  # Vol pattern
                    ]
                    short_signal_strength.iloc[i] = sum(short_factors)
                    
                    # Apply threshold
                    df.loc[df.index[i], 'long_signal'] = float(long_signal_strength.iloc[i] > trending_signal_threshold)
                    df.loc[df.index[i], 'short_signal'] = float(short_signal_strength.iloc[i] > trending_signal_threshold)
                
                else:  # ranging regime
                    # Ranging regime: focus on mean reversion
                    
                    # Long signal in ranging market
                    long_factors = [
                        rsi_oversold.iloc[i] * 0.5,                      # RSI oversold (stronger weight)
                        price_below_lower.iloc[i] * 0.3,                 # Price below BB
                        high_volume.iloc[i] * 0.2                        # High volume
                    ]
                    long_signal_strength.iloc[i] = sum(long_factors)
                    
                    # Short signal in ranging market
                    short_factors = [
                        rsi_overbought.iloc[i] * 0.5,                   # RSI overbought (stronger weight)
                        price_above_upper.iloc[i] * 0.3,                # Price above BB
                        high_volume.iloc[i] * 0.2                       # High volume
                    ]
                    short_signal_strength.iloc[i] = sum(short_factors)
                    
                    # Apply threshold
                    df.loc[df.index[i], 'long_signal'] = float(long_signal_strength.iloc[i] > ranging_signal_threshold)
                    df.loc[df.index[i], 'short_signal'] = float(short_signal_strength.iloc[i] > ranging_signal_threshold)
            
            # --- Generate exit signals ---
            
            # Simple exit logic - can be enhanced
            for i in range(1, len(df)):
                # Exit long positions when:
                if df.loc[df.index[i-1], 'long_signal'] > 0:  # If we were in a long position
                    # Exit if RSI overbought
                    if rsi.iloc[i] > 70:
                        df.loc[df.index[i], 'long_exit'] = 1.0
                    
                    # Or exit if price above upper BB in ranging market
                    elif market_regimes.iloc[i] == 'ranging' and close.iloc[i] > bb_upper.iloc[i]:
                        df.loc[df.index[i], 'long_exit'] = 1.0
                        
                    # Or exit on volume surge in trending market
                    elif market_regimes.iloc[i] == 'trending' and volume_surge.iloc[i]:
                        df.loc[df.index[i], 'long_exit'] = 1.0
                
                # Exit short positions when:
                if df.loc[df.index[i-1], 'short_signal'] > 0:  # If we were in a short position
                    # Exit if RSI oversold
                    if rsi.iloc[i] < 30:
                        df.loc[df.index[i], 'short_exit'] = 1.0
                    
                    # Or exit if price below lower BB in ranging market
                    elif market_regimes.iloc[i] == 'ranging' and close.iloc[i] < bb_lower.iloc[i]:
                        df.loc[df.index[i], 'short_exit'] = 1.0
                        
                    # Or exit on volume surge in trending market
                    elif market_regimes.iloc[i] == 'trending' and volume_surge.iloc[i]:
                        df.loc[df.index[i], 'short_exit'] = 1.0
            
            # --- Clean up signals ---
            
            # Ensure we convert to numeric values (1.0/0.0) for vectorbtpro compatibility
            for col in ['long_signal', 'short_signal', 'long_exit', 'short_exit']:
                df[col] = df[col].astype(float)
            
            # Count and log total signals
            long_count = df['long_signal'].sum()
            short_count = df['short_signal'].sum()
            logger.info(f"Generated {long_count} long signals and {short_count} short signals")
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating multi-factor signals: {str(e)}")
            traceback.print_exc()
            # Return original data with empty signals on error
            data['long_signal'] = 0.0
            data['short_signal'] = 0.0
            data['long_exit'] = 0.0
            data['short_exit'] = 0.0
            return data

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
    
    # Add test_mode option
    parser.add_argument('--test_mode', action='store_true', help='Run backtest in test mode')
    
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
    signals_df, market_regimes, results = strategy.run_strategy(price_data, test_mode=True)
    
    if signals_df['long_signal'].sum() + signals_df['short_signal'].sum() == 0:
        print("No entry signals generated.")
        sys.exit(0)
    
    # --- Calculate Target Percentage Size ---
    print("Calculating target percentage size...")
    target_pct = strategy.calculate_target_percent(price_data)
    
    # --- Results ---
    print(f"Generated {signals_df['long_signal'].sum()} long entries and {signals_df['short_signal'].sum()} short entries.")
    print(f"Trending periods: {(market_regimes == 'trending').mean() * 100:.2f}%")
    print(f"Ranging periods: {(market_regimes == 'ranging').mean() * 100:.2f}%")
    
    # --- Backtest the strategy ---
    print("Backtesting the strategy...")
    results = strategy.backtest_signals(price_data, signals_df, args.plot)
    
    if results:
        print("\nBacktest Results:")
        print(f"Total Return: {results.get('total_return', 0.0):.2%}")
        print(f"Sharpe Ratio: {results.get('sharpe_ratio', 0.0):.2f}")
        print(f"Max Drawdown: {results.get('max_drawdown', 0.0):.2%}")
        print(f"Total Trades: {results.get('num_trades', 0)}")
        print(f"Win Rate: {results.get('win_rate', 0.0):.2%}")
        print(f"Profit Factor: {results.get('profit_factor', 0.0):.2f}")
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