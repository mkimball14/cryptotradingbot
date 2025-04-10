import numpy as np
import pandas as pd
from typing import Tuple, List, Dict
from dataclasses import dataclass

@dataclass
class VolumeProfile:
    price_levels: np.ndarray
    volume_at_price: np.ndarray
    poc_price: float  # Point of Control price
    value_area: Tuple[float, float]  # (lower, upper) bounds of value area
    
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) for a price series.
    
    Args:
        prices: Series of closing prices
        period: RSI period (default 14)
        
    Returns:
        Series containing RSI values
    """
    delta = prices.diff()
    
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_macd(prices: pd.Series,
                  fast_period: int = 12,
                  slow_period: int = 26,
                  signal_period: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate MACD (Moving Average Convergence Divergence) for a price series.
    
    Args:
        prices: Series of closing prices
        fast_period: Fast EMA period
        slow_period: Slow EMA period
        signal_period: Signal line period
        
    Returns:
        Tuple of (MACD line, Signal line, Histogram)
    """
    fast_ema = prices.ewm(span=fast_period, adjust=False).mean()
    slow_ema = prices.ewm(span=slow_period, adjust=False).mean()
    
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calculate_volume_profile(ohlcv_data: pd.DataFrame,
                           price_levels: int = 100,
                           value_area_volume_ratio: float = 0.68) -> VolumeProfile:
    """
    Calculate Volume Profile (Volume by Price) analysis.
    
    Args:
        ohlcv_data: DataFrame with OHLCV data
        price_levels: Number of price levels to analyze
        value_area_volume_ratio: Ratio of volume to include in value area (default 68%)
        
    Returns:
        VolumeProfile object with price levels, volumes, POC, and value area
    """
    high = ohlcv_data['high'].max()
    low = ohlcv_data['low'].min()
    price_increment = (high - low) / price_levels
    
    # Create price levels
    price_levels_array = np.linspace(low, high, price_levels)
    volume_at_price = np.zeros(price_levels)
    
    # Calculate volume at each price level
    for idx, row in ohlcv_data.iterrows():
        level_low = int((row['low'] - low) / price_increment)
        level_high = int((row['high'] - low) / price_increment)
        volume_per_level = row['volume'] / (level_high - level_low + 1)
        
        for level in range(level_low, level_high + 1):
            if 0 <= level < price_levels:
                volume_at_price[level] += volume_per_level
    
    # Find Point of Control (price level with highest volume)
    poc_index = np.argmax(volume_at_price)
    poc_price = price_levels_array[poc_index]
    
    # Calculate Value Area
    total_volume = np.sum(volume_at_price)
    target_volume = total_volume * value_area_volume_ratio
    current_volume = volume_at_price[poc_index]
    
    lower_idx = upper_idx = poc_index
    while current_volume < target_volume and (lower_idx > 0 or upper_idx < price_levels - 1):
        lower_vol = volume_at_price[lower_idx - 1] if lower_idx > 0 else 0
        upper_vol = volume_at_price[upper_idx + 1] if upper_idx < price_levels - 1 else 0
        
        if lower_vol > upper_vol:
            lower_idx -= 1
            current_volume += lower_vol
        else:
            upper_idx += 1
            current_volume += upper_vol
    
    value_area = (price_levels_array[lower_idx], price_levels_array[upper_idx])
    
    return VolumeProfile(
        price_levels=price_levels_array,
        volume_at_price=volume_at_price,
        poc_price=poc_price,
        value_area=value_area
    )

def detect_divergence(prices: pd.Series,
                     indicator: pd.Series,
                     lookback_period: int = 10) -> Dict[str, float]:
    """
    Detect regular and hidden divergences between price and an indicator.
    
    Args:
        prices: Series of closing prices
        indicator: Series of indicator values (e.g. RSI)
        lookback_period: Number of periods to look back for divergence
        
    Returns:
        Dictionary with divergence type and strength
    """
    # Find local extrema
    price_highs = pd.Series([
        i for i in range(1, len(prices)-1)
        if prices.iloc[i] > prices.iloc[i-1] and prices.iloc[i] > prices.iloc[i+1]
    ])
    price_lows = pd.Series([
        i for i in range(1, len(prices)-1)
        if prices.iloc[i] < prices.iloc[i-1] and prices.iloc[i] < prices.iloc[i+1]
    ])
    
    ind_highs = pd.Series([
        i for i in range(1, len(indicator)-1)
        if indicator.iloc[i] > indicator.iloc[i-1] and indicator.iloc[i] > indicator.iloc[i+1]
    ])
    ind_lows = pd.Series([
        i for i in range(1, len(indicator)-1)
        if indicator.iloc[i] < indicator.iloc[i-1] and indicator.iloc[i] < indicator.iloc[i+1]
    ])
    
    # Look for regular bearish divergence (higher highs in price, lower highs in indicator)
    bearish_div = 0.0
    if len(price_highs) >= 2 and len(ind_highs) >= 2:
        if (prices.iloc[price_highs[-1]] > prices.iloc[price_highs[-2]] and 
            indicator.iloc[ind_highs[-1]] < indicator.iloc[ind_highs[-2]]):
            price_change = (prices.iloc[price_highs[-1]] - prices.iloc[price_highs[-2]]) / prices.iloc[price_highs[-2]]
            ind_change = (indicator.iloc[ind_highs[-1]] - indicator.iloc[ind_highs[-2]]) / indicator.iloc[ind_highs[-2]]
            bearish_div = abs(price_change - ind_change)
    
    # Look for regular bullish divergence (lower lows in price, higher lows in indicator)
    bullish_div = 0.0
    if len(price_lows) >= 2 and len(ind_lows) >= 2:
        if (prices.iloc[price_lows[-1]] < prices.iloc[price_lows[-2]] and 
            indicator.iloc[ind_lows[-1]] > indicator.iloc[ind_lows[-2]]):
            price_change = (prices.iloc[price_lows[-1]] - prices.iloc[price_lows[-2]]) / prices.iloc[price_lows[-2]]
            ind_change = (indicator.iloc[ind_lows[-1]] - indicator.iloc[ind_lows[-2]]) / indicator.iloc[ind_lows[-2]]
            bullish_div = abs(price_change - ind_change)
    
    return {
        'bearish_divergence': min(bearish_div, 1.0),
        'bullish_divergence': min(bullish_div, 1.0)
    } 