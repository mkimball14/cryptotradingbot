import numpy as np
import pandas as pd

def create_relative_volume_indicator(volume, lookback_window=20, volume_threshold=1.5, 
                                     short_lookback=None, short_threshold=1.2,
                                     roc_lookback=3, roc_threshold=0.1):
    """
    Calculate relative volume indicator to detect significant volume increases.
    
    This function creates a relative volume indicator that compares current volume
    to historical averages. It can detect volume spikes and patterns that might
    signal significant price movements.
    
    Args:
        volume (pd.Series): Series of volume data
        lookback_window (int): Window for main volume average calculation
        volume_threshold (float): Threshold for main volume ratio (current/average)
        short_lookback (int, optional): Window for short-term volume average
                                       If None, defaults to lookback_window//2
        short_threshold (float): Threshold for short-term volume ratio
        roc_lookback (int): Lookback period for rate of change calculation
        roc_threshold (float): Threshold for volume rate of change
        
    Returns:
        tuple: (
            volume_signal (pd.Series): Boolean indicator True when volume is significantly above average,
            rel_volume (pd.Series): Relative volume ratio compared to lookback_window,
            rel_volume_short (pd.Series): Relative volume ratio compared to short_lookback,
            volume_strength (pd.Series): Numeric score (0-1) indicating strength of volume signal
        )
    """
    # Set default short lookback if not provided
    if short_lookback is None:
        short_lookback = max(3, lookback_window // 2)
    
    # Calculate rolling average volumes with minimum periods to avoid early NaN values
    volume_ma = volume.rolling(window=lookback_window, min_periods=lookback_window // 2).mean()
    volume_short_ma = volume.rolling(window=short_lookback, min_periods=max(2, short_lookback // 2)).mean()
    
    # Handle zeros to avoid division by zero
    volume_ma_safe = volume_ma.replace(0, np.nan).ffill().bfill()
    volume_short_ma_safe = volume_short_ma.replace(0, np.nan).ffill().bfill()
    
    # Calculate relative volume ratios
    rel_volume = (volume / volume_ma_safe).fillna(1.0)
    rel_volume_short = (volume / volume_short_ma_safe).fillna(1.0)
    
    # Calculate volume rate of change
    volume_roc = volume.pct_change(roc_lookback).fillna(0)
    
    # Calculate consecutive increasing volume bars
    vol_diff = volume.diff().fillna(0)
    consecutive_increasing = (vol_diff > 0) & (vol_diff.shift(1) > 0)
    
    # Generate enhanced volume signal
    volume_signal = (
        # High volume relative to longer lookback
        (rel_volume > volume_threshold) | 
        # High volume relative to shorter lookback
        (rel_volume_short > short_threshold) |
        # Volume increasing at significant rate
        ((volume_roc > roc_threshold) & consecutive_increasing)
    )
    
    # Calculate volume strength score (0-1)
    base_score = np.minimum(rel_volume / volume_threshold, 1.0) * 0.7 + \
                 np.minimum(rel_volume_short / short_threshold, 1.0) * 0.3
    
    # Add modifiers for patterns
    pattern_score = pd.Series(0.0, index=volume.index)
    pattern_score.loc[consecutive_increasing] += 0.1
    pattern_score.loc[volume_roc > roc_threshold * 1.5] += 0.15  # Much higher ROC
    
    # Normalize to ensure 0-1 range
    volume_strength = np.minimum(base_score + pattern_score, 1.0)
    
    return volume_signal, rel_volume, rel_volume_short, volume_strength


def create_volume_divergence_indicator(volume, lookback_window, breakout_up, breakout_down, 
                                      volume_threshold=1.5, volume_threshold_short=1.2, 
                                      volume_roc_threshold=0.1, is_trending=None, is_ranging=None, 
                                      price=None, hour_of_day=None, volatility_data=None, 
                                      session_filter=True, adaptive_threshold=True):
    """
    Calculates volume confirmation signals based on pre-calculated breakouts with enhanced detection.
    
    This is a more comprehensive volume indicator that builds on relative volume but adds
    breakout confirmation, market regime awareness, and time-based filtering.
    
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
    volume_short_ma = volume.rolling(window=lookback_window//2, min_periods=max(3, lookback_window//4)).mean()
    volume_ma = volume.rolling(window=lookback_window, min_periods=lookback_window // 2).mean()
    volume_ma_safe = volume_ma.replace(0, np.nan).ffill().bfill()
    
    # Calculate volume ratios against different lookback periods
    vol_ratio_vol = (volume / volume_ma_safe).fillna(1.0)
    vol_ratio_short = (volume / volume_short_ma.replace(0, np.nan).ffill().bfill()).fillna(1.0)
    
    # Calculate longer-term volume reference (e.g., 50 periods)
    long_window = min(lookback_window * 5, 50)  # Cap at 50 periods or 5x lookback
    volume_long_ma = volume.rolling(window=long_window, min_periods=long_window // 2).mean()
    volume_long_ma_safe = volume_long_ma.replace(0, np.nan).ffill().bfill()
    vol_ratio_long = (volume / volume_long_ma_safe).fillna(1.0)
    
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
    
    return volume_confirms_up, volume_confirms_down, volume_strength


def calculate_volume_anomaly(volume, lookback_window=20, z_score_threshold=2.0):
    """
    Detect abnormal volume patterns using statistical measures.
    
    Args:
        volume (pd.Series): Series of volume data
        lookback_window (int): Window for calculating moving average and standard deviation
        z_score_threshold (float): Threshold for z-score to consider volume anomalous
        
    Returns:
        pd.Series: Boolean series indicating anomalous volume
    """
    # Calculate moving average and standard deviation
    volume_ma = volume.rolling(window=lookback_window).mean()
    volume_std = volume.rolling(window=lookback_window).std()
    
    # Calculate z-score
    z_score = (volume - volume_ma) / volume_std.replace(0, np.nan)
    z_score = z_score.fillna(0)
    
    # Identify anomalies
    volume_anomaly = z_score > z_score_threshold
    
    return volume_anomaly


def calculate_price_volume_divergence(price, volume, lookback_window=20):
    """
    Detect price-volume divergences which can signal potential reversals.
    
    Args:
        price (pd.Series): Series of price data
        volume (pd.Series): Series of volume data
        lookback_window (int): Window for moving averages
        
    Returns:
        tuple: (bullish_divergence, bearish_divergence)
    """
    # Calculate price and volume changes
    price_change = price.pct_change().fillna(0)
    volume_change = volume.pct_change().fillna(0)
    
    # Calculate moving averages
    price_ma = price.rolling(window=lookback_window).mean()
    volume_ma = volume.rolling(window=lookback_window).mean()
    
    # Bullish divergence: price making lower lows but volume making higher lows
    # This can indicate accumulation and potential bullish reversal
    price_lower_lows = (price < price.shift(1)) & (price.shift(1) < price.shift(2))
    volume_higher_lows = (volume > volume.shift(1)) & (volume > volume_ma)
    bullish_divergence = price_lower_lows & volume_higher_lows
    
    # Bearish divergence: price making higher highs but volume making lower highs
    # This can indicate distribution and potential bearish reversal
    price_higher_highs = (price > price.shift(1)) & (price.shift(1) > price.shift(2))
    volume_lower_highs = (volume < volume.shift(1)) & (volume > volume_ma)
    bearish_divergence = price_higher_highs & volume_lower_highs
    
    return bullish_divergence, bearish_divergence 