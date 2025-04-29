"""
Test script for signals integration module.

This test demonstrates how the signals_integration module provides a consistent interface
for signal generation with configurable strictness levels.
"""

import os
import pandas as pd
import numpy as np
import pytest
import matplotlib.pyplot as plt
from pathlib import Path

from scripts.strategies.refactored_edge import indicators
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge import signals, test_signals


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
    
    # Create config with default parameters
    config = EdgeConfig()
    
    # Add indicators to data
    indicators_df = indicators.add_indicators(data, config)
    
    return data, indicators_df, config


def test_signals_with_different_strictness_levels():
    """Test signal generation with different strictness levels."""
    # Create sample data
    data, indicators_df, config = create_sample_data()
    
    # Extract necessary series
    close = data['close']
    rsi = indicators_df['rsi']
    bb_upper = indicators_df['bb_upper']
    bb_lower = indicators_df['bb_lower']
    trend_ma = indicators_df['trend_ma']
    price_in_demand_zone = indicators_df.get('demand_zone', pd.Series(False, index=close.index))
    price_in_supply_zone = indicators_df.get('supply_zone', pd.Series(False, index=close.index))
    
    # Base parameters
    base_params = {
        'rsi_lower_threshold': 30,
        'rsi_upper_threshold': 70,
        'use_zones': True,
        'trend_strict': True,
        'min_hold_period': 2,
        'trend_threshold_pct': 0.01,
        'zone_influence': 0.5
    }
    
    # Generate signals with different strictness levels
    results = {}
    
    # STRICT mode
    strict_params = base_params.copy()
    strict_params['signal_strictness'] = SignalStrictness.STRICT
    
    strict_long, strict_long_exit, strict_short, strict_short_exit = generate_signals(
        close=close,
        rsi=rsi,
        bb_upper=bb_upper,
        bb_lower=bb_lower,
        trend_ma=trend_ma,
        price_in_demand_zone=price_in_demand_zone,
        price_in_supply_zone=price_in_supply_zone,
        params=strict_params
    )
    
    # BALANCED mode
    balanced_params = base_params.copy()
    balanced_params['signal_strictness'] = SignalStrictness.BALANCED
    
    balanced_long, balanced_long_exit, balanced_short, balanced_short_exit = generate_signals(
        close=close,
        rsi=rsi,
        bb_upper=bb_upper,
        bb_lower=bb_lower,
        trend_ma=trend_ma,
        price_in_demand_zone=price_in_demand_zone,
        price_in_supply_zone=price_in_supply_zone,
        params=balanced_params
    )
    
    # RELAXED mode
    relaxed_params = base_params.copy()
    relaxed_params['signal_strictness'] = SignalStrictness.RELAXED
    
    relaxed_long, relaxed_long_exit, relaxed_short, relaxed_short_exit = generate_signals(
        close=close,
        rsi=rsi,
        bb_upper=bb_upper,
        bb_lower=bb_lower,
        trend_ma=trend_ma,
        price_in_demand_zone=price_in_demand_zone,
        price_in_supply_zone=price_in_supply_zone,
        params=relaxed_params
    )
    
    # Count signals
    strict_count = strict_long.sum() + strict_short.sum()
    balanced_count = balanced_long.sum() + balanced_short.sum()
    relaxed_count = relaxed_long.sum() + relaxed_short.sum()
    
    print(f"STRICT mode: {strict_count} signals")
    print(f"BALANCED mode: {balanced_count} signals")
    print(f"RELAXED mode: {relaxed_count} signals")
    
    # Assert proper ordering
    assert balanced_count > strict_count, "Balanced mode should generate more signals than strict mode"
    assert relaxed_count > balanced_count, "Relaxed mode should generate more signals than balanced mode"
    
    # Return results for plotting
    return close, {
        'STRICT': (strict_long, strict_short),
        'BALANCED': (balanced_long, balanced_short),
        'RELAXED': (relaxed_long, relaxed_short)
    }


def plot_signals(close, signal_dict, output_dir=None):
    """Plot signals from different strictness levels for comparison."""
    if output_dir is None:
        output_dir = Path('data/signals_comparison')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create new figure
    plt.figure(figsize=(14, 8))
    
    # Plot price
    plt.plot(close.index, close.values, label='Price', color='black', alpha=0.5)
    
    # Define colors and markers for signals
    colors = {
        'STRICT': 'blue',
        'BALANCED': 'green',
        'RELAXED': 'red'
    }
    
    # Plot signals for each strictness level
    for name, (long_entries, short_entries) in signal_dict.items():
        long_indices = close.index[long_entries]
        short_indices = close.index[short_entries]
        
        # Plot long entries (triangle up)
        plt.scatter(long_indices, close.loc[long_indices], 
                   marker='^', s=100, color=colors[name], alpha=0.7,
                   label=f'{name} Long ({len(long_indices)})')
        
        # Plot short entries (triangle down)
        plt.scatter(short_indices, close.loc[short_indices], 
                   marker='v', s=100, color=colors[name], alpha=0.7,
                   label=f'{name} Short ({len(short_indices)})')
    
    plt.title('Signal Comparison by Strictness Level')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best')
    
    # Save the plot
    output_path = os.path.join(output_dir, 'signal_strictness_comparison.png')
    plt.savefig(output_path)
    plt.close()
    
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    # Run test and plot results
    close, signal_dict = test_signals_with_different_strictness_levels()
    plot_signals(close, signal_dict)
