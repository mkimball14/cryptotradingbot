#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debugging script for market regime detection algorithms.

This script tests the regime detection functions with various datasets
to identify and fix issues with regime percentage calculations.
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

# Add project root to path to allow imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("debug_regime_detection")

# Import strategy modules
from scripts.strategies.refactored_edge import regime
from scripts.strategies.refactored_edge.utils import (
    calculate_regime_percentages, 
    normalize_regime_type,
    with_error_handling
)


def create_sample_data(length: int = 100, trending_pct: float = 50) -> pd.DataFrame:
    """
    Create sample price and indicator data with controlled regime characteristics.
    
    Args:
        length: Number of data points to generate
        trending_pct: Percentage of data points that should be in trending regime
        
    Returns:
        DataFrame with price and indicator columns suitable for regime detection
    """
    # Create date range
    dates = pd.date_range(start='2025-01-01', periods=length, freq='4H')
    
    # Initialize random data
    np.random.seed(42)  # For reproducibility
    
    # Calculate how many points should be trending vs ranging
    trending_count = int(length * trending_pct / 100)
    ranging_count = length - trending_count
    
    # Create ADX values - higher for trending periods
    adx_trending = np.random.uniform(30, 50, trending_count)  # Strong ADX for trending
    adx_ranging = np.random.uniform(10, 24, ranging_count)    # Weak ADX for ranging
    adx = np.concatenate([adx_trending, adx_ranging])
    np.random.shuffle(adx)  # Mix trending and ranging periods
    
    # Create directional indicators
    plus_di = np.random.uniform(15, 40, length)
    minus_di = np.random.uniform(15, 40, length)
    
    # Create price data with some trend
    close = np.cumsum(np.random.normal(0, 1, length)) + 100
    high = close + np.random.uniform(0, 2, length)
    low = close - np.random.uniform(0, 2, length)
    
    # Calculate ATR (simplified version)
    atr = np.random.uniform(1, 3, length)
    
    # Create DataFrame
    df = pd.DataFrame({
        'close': close,
        'high': high,
        'low': low,
        'volume': np.random.uniform(1000, 5000, length),
        'adx': adx,
        'plus_di': plus_di,
        'minus_di': minus_di,
        'atr': atr
    }, index=dates)
    
    return df


def test_simple_regime_detection(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Test the basic regime detection function.
    
    Args:
        data: DataFrame with required indicators
        
    Returns:
        Dictionary with test results and metrics
    """
    logger.info("Testing simple regime detection...")
    
    # Get required columns
    adx = data['adx']
    
    # Set threshold
    threshold = 25.0
    
    # Run regime detection
    regimes = regime.determine_market_regime(adx, threshold)
    
    # Calculate and log percentages
    regime_percentages = calculate_regime_percentages(regimes)
    logger.info(f"Simple regime percentages: {regime_percentages}")
    
    # Check if trending + ranging adds up to ~100%
    total_pct = regime_percentages.get('trending', 0) + regime_percentages.get('ranging', 0)
    logger.info(f"Total percentage (should be ~100%): {total_pct:.2f}%")
    
    # Return results
    return {
        'regimes': regimes,
        'percentages': regime_percentages,
        'total_pct': total_pct
    }


def test_enhanced_regime_detection(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Test the enhanced regime detection function.
    
    Args:
        data: DataFrame with required indicators
        
    Returns:
        Dictionary with test results and metrics
    """
    logger.info("Testing enhanced regime detection...")
    
    # Extract required columns
    adx = data['adx']
    plus_di = data['plus_di']
    minus_di = data['minus_di']
    atr = data['atr']
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    # Set parameters
    adx_threshold = 25.0
    strong_adx_threshold = 35.0
    volatility_threshold = 0.01
    momentum_lookback = 5
    momentum_threshold = 0.005
    
    # Run enhanced regime detection
    enhanced_regimes = regime.determine_market_regime_advanced(
        adx=adx,
        plus_di=plus_di,
        minus_di=minus_di,
        atr=atr,
        close=close,
        high=high,
        low=low,
        volume=volume,
        adx_threshold=adx_threshold,
        strong_adx_threshold=strong_adx_threshold,
        volatility_threshold=volatility_threshold,
        momentum_lookback=momentum_lookback,
        momentum_threshold=momentum_threshold,
        use_enhanced_classification=True
    )
    
    # Calculate and log raw regime counts
    logger.info(f"Enhanced regime counts: {enhanced_regimes.value_counts().to_dict()}")
    
    # Calculate percentages
    enhanced_percentages = calculate_regime_percentages(enhanced_regimes)
    logger.info(f"Enhanced regime percentages: {enhanced_percentages}")
    
    # Simplify to basic trending/ranging regimes
    simplified_regimes = regime.simplify_regimes(enhanced_regimes)
    
    # Calculate simplified percentages
    simplified_percentages = calculate_regime_percentages(simplified_regimes)
    logger.info(f"Simplified regime percentages: {simplified_percentages}")
    
    # Categorize enhanced regimes
    trending_regimes = ['trending', 'strong_uptrend', 'weak_uptrend', 'strong_downtrend', 
                        'weak_downtrend', 'breakout', 'breakdown']
    
    ranging_regimes = ['ranging', 'volatile_range', 'quiet_range', 'unknown']
    
    # Calculate trending and ranging totals
    trending_total = sum(enhanced_percentages.get(normalize_regime_type(r), 0) for r in trending_regimes)
    ranging_total = sum(enhanced_percentages.get(normalize_regime_type(r), 0) for r in ranging_regimes)
    
    logger.info(f"Categorized trending total: {trending_total:.2f}%")
    logger.info(f"Categorized ranging total: {ranging_total:.2f}%")
    
    # Return results
    return {
        'enhanced_regimes': enhanced_regimes,
        'simplified_regimes': simplified_regimes,
        'enhanced_percentages': enhanced_percentages,
        'simplified_percentages': simplified_percentages,
        'trending_total': trending_total,
        'ranging_total': ranging_total
    }


def test_regime_detection_with_edge_cases() -> None:
    """Test regime detection functions with edge cases to ensure robustness."""
    logger.info("Testing regime detection with edge cases...")
    
    # Test with empty series
    empty_series = pd.Series([])
    empty_result = calculate_regime_percentages(empty_series)
    logger.info(f"Empty series result: {empty_result}")
    
    # Test with None
    try:
        none_result = calculate_regime_percentages(None)
        logger.info(f"None result: {none_result}")
    except Exception as e:
        logger.error(f"Error with None input: {str(e)}")
    
    # Test with NaN values
    nan_series = pd.Series([np.nan, 'trending', np.nan, 'ranging', 'trending'])
    nan_result = calculate_regime_percentages(nan_series)
    logger.info(f"Series with NaNs result: {nan_result}")
    
    # Test with enum values
    enum_series = pd.Series([
        regime.MarketRegimeType.TRENDING,
        regime.MarketRegimeType.RANGING,
        regime.MarketRegimeType.STRONG_UPTREND,
        regime.MarketRegimeType.QUIET_RANGE
    ])
    enum_result = calculate_regime_percentages(enum_series)
    logger.info(f"Enum series result: {enum_result}")
    
    # Test with mixed case strings
    mixed_series = pd.Series(['Trending', 'RANGING', 'trending', 'ranging'])
    mixed_result = calculate_regime_percentages(mixed_series)
    logger.info(f"Mixed case series result: {mixed_result}")


def test_with_actual_market_data(file_path: Optional[str] = None) -> None:
    """
    Test regime detection with actual market data.
    
    Args:
        file_path: Path to market data CSV file, or None to use default test data
    """
    logger.info("Testing with actual market data...")
    
    # Load actual market data if provided, otherwise use sample data
    if file_path and os.path.exists(file_path):
        data = pd.read_csv(file_path)
        logger.info(f"Loaded {len(data)} data points from {file_path}")
    else:
        logger.info("No file provided or file not found, using synthetic data")
        data = create_sample_data(length=200, trending_pct=60)
    
    # Run tests with this data
    simple_results = test_simple_regime_detection(data)
    enhanced_results = test_enhanced_regime_detection(data)
    
    # Compare results from different methods
    simple_trending = simple_results['percentages'].get('trending', 0)
    enhanced_trending = enhanced_results['trending_total']
    
    logger.info(f"Comparison - Simple trending: {simple_trending:.2f}%, Enhanced trending: {enhanced_trending:.2f}%")
    logger.info(f"Difference: {abs(simple_trending - enhanced_trending):.2f}%")


def main() -> None:
    """Main function to run all regime detection tests."""
    logger.info("Starting regime detection debugging...")
    
    # Test with synthetic data
    data = create_sample_data(length=200, trending_pct=60)
    logger.info(f"Created sample data with {len(data)} data points")
    
    # Run tests
    test_simple_regime_detection(data)
    test_enhanced_regime_detection(data)
    test_regime_detection_with_edge_cases()
    
    # Test with actual data if available
    test_data_path = os.path.join(project_root, "data", "test_data", "sample_ohlc_data.csv")
    if os.path.exists(test_data_path):
        test_with_actual_market_data(test_data_path)
    
    logger.info("Regime detection debugging completed")


if __name__ == "__main__":
    main()
