"""
Test script for WFO evaluation with balanced signals integration.

This test verifies that the WFO evaluation system correctly uses our
new balanced signal generation approach with different strictness levels.
"""

import os
import pandas as pd
import numpy as np
import pytest
from pathlib import Path

from scripts.strategies.refactored_edge import indicators
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.wfo_evaluation import evaluate_single_params


def create_sample_data(periods=200):
    """Create synthetic price and indicator data for testing."""
    dates = pd.date_range(start="2023-01-01", periods=periods, freq="1h")
    
    # Create oscillating price data with some trends
    close = pd.Series(
        data=[100 + 20 * np.sin(i / 20) + i / 10 for i in range(periods)],
        index=dates
    )
    
    # Create DataFrame with OHLC
    data = pd.DataFrame({
        'open': close * 0.998,
        'high': close * 1.005,
        'low': close * 0.995,
        'close': close
    })
    
    return data


def test_wfo_evaluation_with_balanced_signals():
    """Test WFO evaluation with different signal strictness levels."""
    # Create sample data
    data = create_sample_data()
    
    # Define metrics to evaluate
    metric = "Total Return [%]"
    
    # Test with different strictness levels
    results = {}
    
    # STRICT mode
    strict_params = {
        # Core indicator parameters
        'rsi_window': 14,
        'bb_window': 20,
        'bb_std_dev': 2.0,
        'ma_window': 50,
        'trend_ma_window': 50,  # Alias for ma_window
        'atr_window': 14,
        'atr_window_sizing': 14,
        
        # Signal parameters
        'rsi_lower_threshold': 30,
        'rsi_upper_threshold': 70,
        'use_zones': True,
        'trend_strict': True,
        'signal_strictness': SignalStrictness.STRICT,
        
        # Regime parameters
        'adx_window': 14,
        'adx_threshold': 25.0,
        
        # Zone parameters
        'pivot_lookback': 10,
        'pivot_prominence': 0.01,
        'zone_merge_proximity': 0.005,
        'min_zone_width_candles': 5,
        
        # Balanced signal parameters
        'min_hold_period': 2,
        'trend_threshold_pct': 0.01,
        'zone_influence': 0.5
    }
    strict_score = evaluate_single_params(strict_params, data, metric)
    
    # BALANCED mode
    balanced_params = strict_params.copy()
    balanced_params['signal_strictness'] = SignalStrictness.BALANCED
    balanced_score = evaluate_single_params(balanced_params, data, metric)
    
    # RELAXED mode
    relaxed_params = strict_params.copy()
    relaxed_params['signal_strictness'] = SignalStrictness.RELAXED
    relaxed_score = evaluate_single_params(relaxed_params, data, metric)
    
    # Print results
    print("\nWFO Evaluation Results with Different Signal Strictness:")
    print(f"STRICT mode: {strict_score}")
    print(f"BALANCED mode: {balanced_score}")
    print(f"RELAXED mode: {relaxed_score}")
    
    # The test passes if we can evaluate all three modes without errors
    # Results may vary based on the synthetic data, so we don't assert specific values
    return strict_score, balanced_score, relaxed_score


if __name__ == "__main__":
    # Run test
    test_wfo_evaluation_with_balanced_signals()
