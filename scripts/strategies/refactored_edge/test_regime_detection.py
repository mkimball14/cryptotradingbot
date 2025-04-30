#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simplified Regime Detection Test Script

This script tests the enhanced regime detection functionality using 
synthetic data, without requiring external data fetching.

Author: Max Kimball
Date: 2025-04-28
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import logging
from pathlib import Path

# Add the parent directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Local imports
from strategies.refactored_edge.regime import (
    determine_market_regime,
    determine_market_regime_advanced,
    MarketRegimeType,
    get_regime_specific_params
)
from strategies.refactored_edge.config import EdgeConfig
from strategies.refactored_edge import indicators

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("regime_detection_test")

def create_synthetic_data(days=100, volatility=0.02, trend_cycle_days=30, include_regimes=True):
    """
    Create synthetic price data with different market regimes for testing.
    
    Args:
        days (int): Number of days of hourly data to generate
        volatility (float): Base volatility level (will be dynamically adjusted)
        trend_cycle_days (int): Days per trend cycle
        include_regimes (bool): Whether to include explicit regime sections
        
    Returns:
        pd.DataFrame: DataFrame with OHLCV data and indicators
    """
    # Generate dates and initial close prices
    periods = days * 24  # Hourly data
    dates = [datetime.now() - timedelta(hours=periods-i) for i in range(periods)]
    
    # Create arrays for prices and volatility
    close_prices = np.zeros(periods)
    volatility_series = np.zeros(periods)
    regime_labels = np.zeros(periods, dtype=int)
    
    # Set seed for reproducibility
    np.random.seed(42)
    
    # Starting price
    base_price = 100
    current_price = base_price
    
    # If including explicit regimes, divide the periods into segments with different characteristics
    if include_regimes:
        # Create segments with different market regimes
        segment_length = periods // 8  # 8 distinct segments
        
        for i in range(8):
            start_idx = i * segment_length
            end_idx = (i + 1) * segment_length if i < 7 else periods
            segment_size = end_idx - start_idx
            
            # Set regime characteristics based on segment number
            if i == 0:  # Strong uptrend
                trend_factor = 0.001  # Daily upward drift
                vol_factor = volatility * 0.8  # Lower volatility during trend
                regime_labels[start_idx:end_idx] = 1
                
            elif i == 1:  # Volatile range
                trend_factor = 0.0  # No trend
                vol_factor = volatility * 2.5  # Higher volatility
                regime_labels[start_idx:end_idx] = 2
                
            elif i == 2:  # Weak downtrend
                trend_factor = -0.0005  # Mild downward drift
                vol_factor = volatility * 1.2
                regime_labels[start_idx:end_idx] = 3
                
            elif i == 3:  # Quiet range
                trend_factor = 0.0001  # Slight upward bias
                vol_factor = volatility * 0.5  # Low volatility
                regime_labels[start_idx:end_idx] = 4
                
            elif i == 4:  # Strong downtrend
                trend_factor = -0.0015  # Strong downward drift
                vol_factor = volatility * 1.0
                regime_labels[start_idx:end_idx] = 5
                
            elif i == 5:  # Breakout
                # First create a tight range, then break out upward
                breakout_point = start_idx + int(segment_size * 0.7)
                
                # Range part
                vol_factor_range = volatility * 0.4
                for j in range(start_idx, breakout_point):
                    volatility_series[j] = vol_factor_range
                    # Random walk with slight mean reversion in the range
                    price_change = np.random.normal(0, vol_factor_range) - (current_price - base_price) * 0.01
                    current_price += price_change
                    close_prices[j] = current_price
                    regime_labels[j] = 6
                
                # Breakout part
                for j in range(breakout_point, end_idx):
                    # Accelerating upward move with increasing volatility
                    days_in_breakout = j - breakout_point
                    breakout_vol = volatility * (1.0 + days_in_breakout * 0.1)
                    breakout_drift = 0.002 * (1.0 + days_in_breakout * 0.05)
                    
                    volatility_series[j] = breakout_vol
                    price_change = np.random.normal(breakout_drift, breakout_vol)
                    current_price += price_change
                    close_prices[j] = current_price
                    regime_labels[j] = 6
                
                # Skip the normal segment processing
                continue
                
            elif i == 6:  # Breakdown
                # Similar to breakout but downward
                breakdown_point = start_idx + int(segment_size * 0.6)
                
                # Range part
                vol_factor_range = volatility * 0.4
                for j in range(start_idx, breakdown_point):
                    volatility_series[j] = vol_factor_range
                    # Random walk with slight mean reversion in the range
                    price_change = np.random.normal(0, vol_factor_range) - (current_price - base_price) * 0.01
                    current_price += price_change
                    close_prices[j] = current_price
                    regime_labels[j] = 7
                
                # Breakdown part
                for j in range(breakdown_point, end_idx):
                    # Accelerating downward move with increasing volatility
                    days_in_breakdown = j - breakdown_point
                    breakdown_vol = volatility * (1.0 + days_in_breakdown * 0.1)
                    breakdown_drift = -0.003 * (1.0 + days_in_breakdown * 0.05)
                    
                    volatility_series[j] = breakdown_vol
                    price_change = np.random.normal(breakdown_drift, breakdown_vol)
                    current_price += price_change
                    close_prices[j] = current_price
                    regime_labels[j] = 7
                
                # Skip the normal segment processing
                continue
                
            elif i == 7:  # Recovery uptrend
                trend_factor = 0.0008  # Moderate upward drift
                vol_factor = volatility * 1.3  # Moderate-high volatility
                regime_labels[start_idx:end_idx] = 8
            
            # Fill the segment with appropriate price action
            for j in range(start_idx, end_idx):
                volatility_series[j] = vol_factor
                # Add both trend and random components
                price_change = np.random.normal(trend_factor, vol_factor)
                current_price += price_change
                close_prices[j] = current_price
    
    else:  # Standard synthetic data with sine waves and random walk
        # Create price with both trend and range components
        trend = np.sin(np.linspace(0, days/trend_cycle_days * 2 * np.pi, periods))
        base_price = 100 + trend * 20  # Oscillate between 80 and 120
        
        # Add volatility that changes with the trend (higher at tops and bottoms)
        trend_volatility = 0.5 + 0.5 * np.abs(np.cos(np.linspace(0, days/trend_cycle_days * 2 * np.pi, periods)))
        volatility_series = volatility * trend_volatility
        
        # Generate the random walk component with varying volatility
        for i in range(periods):
            if i == 0:
                close_prices[i] = base_price[i]
            else:
                price_change = np.random.normal(0, volatility_series[i])
                close_prices[i] = close_prices[i-1] + price_change + (base_price[i] - base_price[i-1]) * 0.3
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': dates,
        'close': close_prices,
        'volatility': volatility_series,
        'regime': regime_labels if include_regimes else None
    })
    
    # Set timestamp as index
    df.set_index('timestamp', inplace=True)
    
    # Generate synthetic OHLC based on close
    df['open'] = df['close'].shift(1).fillna(df['close'] * 0.99)
    df['high'] = df['close'] * (1 + df['volatility'] * np.random.random(periods) * 0.5)
    df['low'] = df['close'] * (1 - df['volatility'] * np.random.random(periods) * 0.5)
    
    # Make sure high is always >= close and open
    df['high'] = df[['high', 'open', 'close']].max(axis=1)
    
    # Make sure low is always <= close and open
    df['low'] = df[['low', 'open', 'close']].min(axis=1)
    
    # Generate volume that increases with volatility
    normalized_vol = (df['volatility'] - df['volatility'].min()) / (df['volatility'].max() - df['volatility'].min())
    df['volume'] = 1000 + normalized_vol * 9000
    df['volume'] = df['volume'].astype(int)
    
    # Ensure all required columns exist and have proper capitalization
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df.columns = [col.capitalize() for col in df.columns]
    
    return df

def add_test_indicators(df):
    """
    Add indicators needed for regime detection.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        
    Returns:
        pd.DataFrame: DataFrame with added indicators
    """
    logger.info("Calculating indicators for regime detection...")
    
    # Create a basic config with default values
    config = EdgeConfig()
    
    # Add indicators (ADX, DI+, DI-, ATR)
    df_with_indicators = indicators.add_indicators(df, config)
    
    return df_with_indicators

def test_basic_regime_detection():
    """Test the basic (trending/ranging) regime detection."""
    logger.info("Testing basic regime detection...")
    
    # Create test data
    df = create_synthetic_data()
    df_with_ind = add_test_indicators(df)
    
    # Extract needed indicators
    adx = df_with_ind.get('adx')
    
    # Check if indicators were calculated successfully
    if adx is None:
        logger.error("Failed to calculate ADX indicator")
        return False
    
    # Detect basic market regime
    market_regime = determine_market_regime(adx)
    
    # Calculate regime statistics
    trending_periods = (market_regime == 'trending').sum()
    ranging_periods = (market_regime == 'ranging').sum()
    total_periods = len(market_regime)
    
    logger.info(f"Basic regime detection results:")
    logger.info(f"  Total periods: {total_periods}")
    logger.info(f"  Trending periods: {trending_periods} ({trending_periods/total_periods*100:.1f}%)")
    logger.info(f"  Ranging periods: {ranging_periods} ({ranging_periods/total_periods*100:.1f}%)")
    
    return True

def test_enhanced_regime_detection():
    """Test the enhanced (multi-class) regime detection."""
    logger.info("Testing enhanced regime detection...")
    
    # Create test data
    df = create_synthetic_data()
    df_with_ind = add_test_indicators(df)
    
    # Debug column names
    logger.info(f"Available columns in df_with_ind: {df_with_ind.columns.tolist()}")
    
    # Extract needed indicators
    adx = df_with_ind.get('adx')
    plus_di = df_with_ind.get('plus_di')
    minus_di = df_with_ind.get('minus_di')
    # Use atr_stops as our ATR value since 'atr' doesn't exist
    atr = df_with_ind.get('atr_stops')
    # Get the close price from df_with_ind, not from df
    close = df_with_ind.get('Close')
    
    # Check if indicators were calculated successfully
    if adx is None or plus_di is None or minus_di is None or atr is None or close is None:
        logger.error("Failed to calculate indicators required for enhanced regime detection")
        if adx is None: logger.error("ADX is missing")
        if plus_di is None: logger.error("+DI is missing")
        if minus_di is None: logger.error("-DI is missing")
        if atr is None: logger.error("ATR is missing")
        if close is None: logger.error("Close price is missing")
        return False
    
    # Detect enhanced market regime
    market_regime = determine_market_regime_advanced(
        adx, plus_di, minus_di, atr, close
    )
    
    # Calculate regime statistics
    regime_counts = market_regime.value_counts()
    total_periods = len(market_regime)
    
    logger.info(f"Enhanced regime detection results:")
    logger.info(f"  Total periods: {total_periods}")
    
    for regime_type in regime_counts.index:
        count = regime_counts[regime_type]
        logger.info(f"  {regime_type}: {count} ({count/total_periods*100:.1f}%)")
    
    # Test that we can get parameters for a specific regime
    test_params = {'rsi_lower_threshold': 30, 'ma_window': 50}
    test_regimes = {
        MarketRegimeType.STRONG_UPTREND: {'rsi_lower_threshold': 40, 'ma_window': 20},
        MarketRegimeType.VOLATILE_RANGE: {'rsi_lower_threshold': 20, 'ma_window': 100}
    }
    
    # Test parameter retrieval for all detected regimes
    unique_regimes = market_regime.unique()
    # Create a Series for testing parameter retrieval
    test_series = pd.Series(market_regime.iloc[0:5].values, index=market_regime.index[0:5])
    regime_params = get_regime_specific_params(test_series, test_regimes, test_params)
    logger.info(f"Parameters for sample regimes: {regime_params}")
    
    return True

def plot_regimes(df, market_regime, title="Market Regime Classification"):
    """
    Create a plot of price with market regimes highlighted.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data
        market_regime (pd.Series): Series containing market regime classifications
        title (str): Plot title
    """
    try:
        plt.figure(figsize=(12, 8))
        
        # Plot close price
        ax1 = plt.subplot(211)
        ax1.plot(df.index, df['Close'], label='Close Price')
        ax1.set_title(title)
        ax1.legend()
        
        # Plot regime classifications
        ax2 = plt.subplot(212, sharex=ax1)
        ax2.plot(market_regime.index, market_regime.astype(str), 'o-', markersize=2)
        
        if market_regime.dtype == object:  # String classifications
            regimes = market_regime.unique()
            ax2.set_yticks(range(len(regimes)))
            ax2.set_yticklabels(regimes)
        else:  # Enum classifications
            regime_values = sorted(list({r.value for r in market_regime}))
            regime_names = sorted(list({r.name for r in market_regime}))
            ax2.set_yticks(regime_values)
            ax2.set_yticklabels(regime_names)
            
        ax2.set_title('Market Regime Classification')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('regime_classification.png')
        logger.info("Saved regime classification plot to regime_classification.png")
        plt.close()
    except Exception as e:
        logger.error(f"Error creating regime plot: {e}")

def main():
    """Main execution function."""
    logger.info("Starting regime detection test")
    
    # Test create_synthetic_data
    df = create_synthetic_data()
    logger.info(f"Synthetic data created with columns: {df.columns.tolist()}")
    logger.info(f"Synthetic data shape: {df.shape}")
    
    print("=== Testing Basic Regime Detection ===")
    if test_basic_regime_detection():
        print("✅ Basic regime detection test completed successfully")
    else:
        print("❌ Basic regime detection test failed")
    
    print("\n=== Testing Enhanced Regime Detection ===")
    if test_enhanced_regime_detection():
        print("✅ Enhanced regime detection test completed successfully")
    else:
        print("❌ Enhanced regime detection test failed")
    
    # Create and plot regimes for visual inspection
    df = create_synthetic_data()
    df_with_ind = add_test_indicators(df)
    
    # Extract needed indicators for both methods
    adx = df_with_ind.get('adx')
    plus_di = df_with_ind.get('plus_di') 
    minus_di = df_with_ind.get('minus_di')
    atr = df_with_ind.get('atr')
    close = df['Close']
    
    if adx is not None:
        # Plot basic regimes
        basic_regime = determine_market_regime(adx)
        plot_regimes(df, basic_regime, "Basic Market Regime (Trending/Ranging)")
        
        # Plot enhanced regimes if all required indicators are available
        if plus_di is not None and minus_di is not None and atr is not None:
            enhanced_regime = determine_market_regime_advanced(adx, plus_di, minus_di, atr, close)
            # Convert enum to string for plotting
            enhanced_regime_str = enhanced_regime.apply(lambda x: x.name)
            plot_regimes(df, enhanced_regime_str, "Enhanced Market Regime Classification")
    
    logger.info("Regime detection test completed")

if __name__ == "__main__":
    main()
