#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced Indicators Module

This module extends the basic indicators with advanced TA-Lib pattern recognition,
volatility measurements, and regime detection capabilities to improve signal quality
and market condition awareness.

Author: Max Kimball
Date: 2025-04-30
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Union

# Import TA-Lib for advanced indicators
import talib
import vectorbtpro as vbt

# Configure logger
logger = logging.getLogger(__name__)

def add_pattern_recognition(data: pd.DataFrame, min_strength: int = 60) -> pd.DataFrame:
    """
    Add candlestick pattern recognition indicators using TA-Lib.
    
    Args:
        data: OHLCV DataFrame
        min_strength: Minimum pattern strength to consider (0-100)
        
    Returns:
        DataFrame with added pattern columns
    """
    if not all(col in data.columns for col in ['open', 'high', 'low', 'close']):
        logger.error("DataFrame missing required OHLC columns")
        return data
    
    # Create a copy to avoid modifying the original
    result = data.copy()
    
    try:
        # Add candlestick patterns with bullish/bearish signals
        # 1. Doji patterns (market indecision)
        result['doji'] = talib.CDLDOJI(result['open'], result['high'], result['low'], result['close'])
        
        # 2. Engulfing patterns (potential reversal)
        result['engulfing'] = talib.CDLENGULFING(result['open'], result['high'], result['low'], result['close'])
        
        # 3. Evening/Morning Star (strong reversal patterns)
        result['evening_star'] = talib.CDLEVENINGSTAR(result['open'], result['high'], result['low'], result['close'])
        result['morning_star'] = talib.CDLMORNINGSTAR(result['open'], result['high'], result['low'], result['close'])
        
        # 4. Three Outside (reversal pattern)
        result['three_outside'] = talib.CDL3OUTSIDE(result['open'], result['high'], result['low'], result['close'])
        
        # 5. Hammer/Hanging Man (reversal signals)
        result['hammer'] = talib.CDLHAMMER(result['open'], result['high'], result['low'], result['close'])
        result['hanging_man'] = talib.CDLHANGINGMAN(result['open'], result['high'], result['low'], result['close'])
        
        # Create a composite pattern signal
        # Positive values indicate bullish patterns, negative indicate bearish patterns
        result['pattern_signal'] = (
            result['engulfing'] + 
            result['morning_star'] + 
            result['evening_star'] * -1 +  # Convert to negative for bearish pattern
            result['hammer'] +
            result['hanging_man'] * -1 +  # Convert to negative for bearish pattern
            result['three_outside']
        )
        
        # Create a pattern strength indicator (0-100 scale)
        result['pattern_strength'] = result['pattern_signal'].abs()
        result['pattern_strength'] = result['pattern_strength'] / result['pattern_strength'].max() * 100
        result['pattern_strength'] = result['pattern_strength'].fillna(0).astype(int)
        
        # Create boolean signals based on strength
        result['pattern_bullish'] = (result['pattern_signal'] > 0) & (result['pattern_strength'] >= min_strength)
        result['pattern_bearish'] = (result['pattern_signal'] < 0) & (result['pattern_strength'] >= min_strength)
        
        logger.info(f"Added {result['pattern_bullish'].sum()} bullish and {result['pattern_bearish'].sum()} bearish pattern signals")
        
    except Exception as e:
        logger.error(f"Error adding pattern recognition: {str(e)}")
        
    return result


def add_volatility_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add advanced volatility indicators for regime detection.
    
    Args:
        data: OHLCV DataFrame with standard indicators
        
    Returns:
        DataFrame with added volatility indicators
    """
    if not all(col in data.columns for col in ['close', 'high', 'low']):
        logger.error("DataFrame missing required price columns")
        return data
    
    result = data.copy()
    
    try:
        # 1. Historical Volatility (using standard deviation)
        close_price = result['close']
        result['hist_vol_5'] = close_price.pct_change().rolling(5).std() * np.sqrt(252) * 100
        result['hist_vol_21'] = close_price.pct_change().rolling(21).std() * np.sqrt(252) * 100

        # 2. ATR Percent (ATR relative to price)
        if 'atr' not in result.columns:
            result['atr'] = talib.ATR(result['high'], result['low'], result['close'], timeperiod=14)
        result['atr_pct'] = result['atr'] / result['close'] * 100
        
        # 3. Bollinger Band Width (measure of volatility)
        # Calculate Bollinger Bands
        upper, middle, lower = talib.BBANDS(result['close'], timeperiod=20, nbdevup=2, nbdevdn=2)
        result['bb_width'] = (upper - lower) / middle * 100
        
        # 4. VHF (Vertical Horizontal Filter - measure of trendiness vs. choppiness)
        def calculate_vhf(series, period=28):
            highest = series.rolling(period).max()
            lowest = series.rolling(period).min()
            num = highest - lowest
            
            changes = series.diff().abs()
            denom = changes.rolling(period).sum()
            
            vhf = num / denom
            return vhf
        
        result['vhf'] = calculate_vhf(result['close'], period=28)
        
        # 5. Choppiness Index (0-100 scale, higher values = more choppy/ranging)
        def calculate_choppiness(df, period=14):
            atr_sum = df['atr'].rolling(period).sum()
            high_low_range = df['high'].rolling(period).max() - df['low'].rolling(period).min()
            choppy = 100 * np.log10(atr_sum / high_low_range) / np.log10(period)
            return choppy
        
        result['choppiness'] = calculate_choppiness(result, period=14)
        
        logger.info("Added volatility indicators including VHF and Choppiness Index")
        
    except Exception as e:
        logger.error(f"Error adding volatility indicators: {str(e)}")
        
    return result


def detect_enhanced_regime(
    data: pd.DataFrame,
    vhf_threshold: float = 0.24,
    choppy_threshold: float = 61.8,
    adx_threshold: float = 25.0,
    pattern_threshold: int = 60
) -> pd.DataFrame:
    """
    Enhanced market regime detection using multiple indicators.
    
    Args:
        data: DataFrame with technical indicators
        vhf_threshold: Threshold for Vertical Horizontal Filter (higher = trending)
        choppy_threshold: Threshold for Choppiness Index (higher = more ranging)
        adx_threshold: Threshold for ADX to confirm trend (higher = stronger trend)
        pattern_threshold: Minimum pattern strength to consider for regime shifts
        
    Returns:
        DataFrame with regime classification columns
    """
    required_columns = ['close', 'adx', 'vhf', 'choppiness', 'pattern_strength', 'pattern_signal']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        missing_str = ', '.join(missing_columns)
        logger.warning(f"Missing required columns for enhanced regime detection: {missing_str}")
        
        # Add missing indicators
        if 'vhf' not in data.columns or 'choppiness' not in data.columns:
            data = add_volatility_indicators(data)
            
        if 'pattern_strength' not in data.columns or 'pattern_signal' not in data.columns:
            data = add_pattern_recognition(data)
            
        if 'adx' not in data.columns and all(col in data.columns for col in ['high', 'low', 'close']):
            data['adx'] = talib.ADX(data['high'], data['low'], data['close'], timeperiod=14)
    
    result = data.copy()
    
    # Initialize regime columns
    result['regime_enhanced'] = pd.Series(dtype='object')
    result['regime_enhanced_numeric'] = 0  # 0=ranging, 1=trending
    result['regime_strength'] = 0.0  # 0-1 scale
    
    try:
        # Multi-factor regime classification
        # 1. VHF criterion (trend vs range)
        vhf_trending = result['vhf'] > vhf_threshold
        
        # 2. Choppiness criterion (range vs trend)
        choppy_ranging = result['choppiness'] > choppy_threshold
        
        # 3. ADX criterion (trend strength)
        adx_trending = result['adx'] > adx_threshold
        
        # 4. Pattern signals indicating potential regime shifts
        has_pattern = result['pattern_strength'] >= pattern_threshold
        
        # Combine criteria with weighted approach
        trending_score = (
            (vhf_trending.astype(int) * 0.35) + 
            (~choppy_ranging.astype(int) * 0.35) + 
            (adx_trending.astype(int) * 0.3)
        )
        
        # Determine regime based on combined score
        result['regime_strength'] = trending_score
        result['regime_enhanced_numeric'] = (trending_score > 0.6).astype(int)
        
        # Create categorical regime column
        result['regime_enhanced'] = np.where(
            result['regime_enhanced_numeric'] == 1, 
            'TRENDING', 
            'RANGING'
        )
        
        # Handle regime transitions with pattern recognition
        # If a strong pattern appears, it may signal a regime change is imminent
        potential_transitions = has_pattern & (result['pattern_strength'] >= pattern_threshold)
        
        # Add columns indicating potential regime shifts
        result['regime_transition_signal'] = potential_transitions.astype(int)
        result['regime_transition_direction'] = np.where(
            potential_transitions & (result['pattern_signal'] > 0),
            'TO_TRENDING',
            np.where(
                potential_transitions & (result['pattern_signal'] < 0),
                'TO_RANGING',
                'NONE'
            )
        )
        
        # Calculate percentage of each regime
        total_points = len(result)
        trending_pct = (result['regime_enhanced'] == 'TRENDING').sum() / total_points * 100
        ranging_pct = (result['regime_enhanced'] == 'RANGING').sum() / total_points * 100
        
        logger.info(f"Enhanced regime detection: {trending_pct:.1f}% trending, {ranging_pct:.1f}% ranging")
        
    except Exception as e:
        logger.error(f"Error in enhanced regime detection: {str(e)}")
    
    return result


def adaptive_parameter_mapping(
    regime: str,
    transition_signal: int = 0,
    regime_strength: float = 0.5,
    base_params: Dict = None
) -> Dict:
    """
    Create adaptive parameters based on detected market regime.
    
    Args:
        regime: Detected market regime ('TRENDING' or 'RANGING')
        transition_signal: Whether a regime transition is occurring (0 or 1)
        regime_strength: Strength of current regime (0-1)
        base_params: Base parameters to adapt
        
    Returns:
        Dictionary of adapted parameters for the current market condition
    """
    if base_params is None:
        base_params = {}
        
    adapted_params = base_params.copy()
    
    # Adjust parameters based on regime
    if regime == 'TRENDING':
        # In trending markets, use momentum-following settings
        # 1. More conservative entry criteria
        if 'rsi_entry_threshold' in adapted_params:
            # Scale RSI threshold based on regime strength
            adapted_params['rsi_entry_threshold'] = int(
                max(25, adapted_params.get('rsi_entry_threshold', 30) - 5 * regime_strength)
            )
            
        # 2. Wider exit criteria to let profits run
        if 'rsi_exit_threshold' in adapted_params:
            adapted_params['rsi_exit_threshold'] = int(
                min(75, adapted_params.get('rsi_exit_threshold', 70) + 5 * regime_strength)
            )
            
        # 3. Stronger trend following
        if 'trend_threshold_pct' in adapted_params:
            adapted_params['trend_threshold_pct'] = adapted_params.get('trend_threshold_pct', 0.01) * (1 + regime_strength)
            
        # 4. Reduced zone influence in trending markets
        if 'zone_influence' in adapted_params:
            adapted_params['zone_influence'] = adapted_params.get('zone_influence', 0.5) * (1 - regime_strength * 0.3)
            
        # 5. Longer hold periods in trends
        if 'min_hold_period' in adapted_params:
            adapted_params['min_hold_period'] = int(
                adapted_params.get('min_hold_period', 2) * (1 + regime_strength)
            )
            
    elif regime == 'RANGING':
        # In ranging markets, use mean-reversion settings
        # 1. More relaxed entry criteria
        if 'rsi_entry_threshold' in adapted_params:
            adapted_params['rsi_entry_threshold'] = int(
                min(40, adapted_params.get('rsi_entry_threshold', 30) + 5 * regime_strength)
            )
            
        # 2. Tighter exit criteria to take profits quicker
        if 'rsi_exit_threshold' in adapted_params:
            adapted_params['rsi_exit_threshold'] = int(
                max(60, adapted_params.get('rsi_exit_threshold', 70) - 5 * regime_strength)
            )
            
        # 3. Reduced trend following
        if 'trend_threshold_pct' in adapted_params:
            adapted_params['trend_threshold_pct'] = adapted_params.get('trend_threshold_pct', 0.01) * (1 - regime_strength * 0.5)
            
        # 4. Increased zone influence in ranging markets
        if 'zone_influence' in adapted_params:
            adapted_params['zone_influence'] = min(
                0.9, 
                adapted_params.get('zone_influence', 0.5) * (1 + regime_strength * 0.3)
            )
            
        # 5. Shorter hold periods in ranges
        if 'min_hold_period' in adapted_params:
            adapted_params['min_hold_period'] = max(
                0,
                int(adapted_params.get('min_hold_period', 2) * (1 - regime_strength * 0.5))
            )
    
    # Handle transition periods (when a pattern suggests regime change is imminent)
    if transition_signal == 1:
        # Use more conservative settings during transitions
        if 'signal_strictness' in adapted_params:
            # Make signals more strict during transitions to avoid false signals
            adapted_params['signal_strictness'] = "BALANCED"  # Default to balanced during transitions
            
    return adapted_params


if __name__ == '__main__':
    # Simple demonstration of enhanced indicators with sample data
    import yfinance as yf
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Fetch sample data
    logger.info("Fetching sample data for demonstration")
    sample_data = yf.download('BTC-USD', start='2023-01-01', end='2025-01-01', interval='1d')
    sample_data.columns = [c.lower() for c in sample_data.columns]
    
    # Add indicators
    logger.info("Adding indicators")
    with_patterns = add_pattern_recognition(sample_data)
    with_volatility = add_volatility_indicators(with_patterns)
    
    # Add ADX for regime detection
    with_volatility['adx'] = talib.ADX(
        with_volatility['high'], 
        with_volatility['low'], 
        with_volatility['close'], 
        timeperiod=14
    )
    
    # Detect regimes
    logger.info("Detecting market regimes")
    with_regimes = detect_enhanced_regime(with_volatility)
    
    # Summary statistics
    regime_stats = with_regimes['regime_enhanced'].value_counts()
    transition_count = with_regimes['regime_transition_signal'].sum()
    
    logger.info(f"Regime distribution: {regime_stats.to_dict()}")
    logger.info(f"Detected {transition_count} potential regime transitions")
    
    # Demonstrate parameter adaptation
    base_params = {
        'rsi_entry_threshold': 30,
        'rsi_exit_threshold': 70,
        'trend_threshold_pct': 0.01,
        'zone_influence': 0.5,
        'min_hold_period': 2
    }
    
    # Sample trending and ranging adaptations
    trending_params = adaptive_parameter_mapping('TRENDING', 0, 0.8, base_params)
    ranging_params = adaptive_parameter_mapping('RANGING', 0, 0.8, base_params)
    transition_params = adaptive_parameter_mapping('TRENDING', 1, 0.6, base_params)
    
    logger.info(f"Base parameters: {base_params}")
    logger.info(f"Trending adapted parameters: {trending_params}")
    logger.info(f"Ranging adapted parameters: {ranging_params}")
    logger.info(f"Transition adapted parameters: {transition_params}")
