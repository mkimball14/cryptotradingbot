"""
Tests for the balanced signals generation module.

This module tests the balanced signal generation approach, ensuring it:
1. Properly generates signals with different strictness levels
2. Creates more signals than strict mode but fewer than relaxed mode
3. Handles different parameter combinations correctly
4. Properly processes zone information
"""

import pytest
import pandas as pd
import numpy as np
from pandas import DatetimeIndex
from scripts.strategies.refactored_edge.balanced_signals import (
    generate_balanced_signals,
    SignalStrictness
)
from scripts.strategies.refactored_edge.signals import generate_edge_signals
from scripts.strategies.refactored_edge.test_signals import generate_test_edge_signals


@pytest.fixture
def mock_price_data():
    """Creates a mock price dataset for testing signal generation."""
    # Create date range for test data
    dates = pd.date_range(start="2023-01-01", periods=100, freq="1H")
    
    # Create oscillating price data to trigger different signals
    close = pd.Series(
        data=[100 + 10 * np.sin(i / 5) for i in range(100)],
        index=dates
    )
    
    # Create RSI that oscillates between oversold and overbought
    rsi = pd.Series(
        data=[30 + 40 * np.sin(i / 10) for i in range(100)],
        index=dates
    )
    
    # Create Bollinger Bands
    bb_upper = close + 5
    bb_lower = close - 5
    
    # Create trend MA that crosses price
    trend_ma = pd.Series(
        data=[100 + 5 * np.sin(i / 15) for i in range(100)],
        index=dates
    )
    
    # Create zones that alternate
    demand_zone_periods = [10, 30, 50, 70, 90]
    supply_zone_periods = [20, 40, 60, 80]
    
    price_in_demand_zone = pd.Series(False, index=dates)
    price_in_supply_zone = pd.Series(False, index=dates)
    
    for i in demand_zone_periods:
        start_idx = max(0, i-2)
        end_idx = min(len(dates), i+3)
        price_in_demand_zone.iloc[start_idx:end_idx] = True
        
    for i in supply_zone_periods:
        start_idx = max(0, i-2)
        end_idx = min(len(dates), i+3)
        price_in_supply_zone.iloc[start_idx:end_idx] = True
    
    return {
        "close": close,
        "rsi": rsi,
        "bb_upper": bb_upper,
        "bb_lower": bb_lower,
        "trend_ma": trend_ma,
        "price_in_demand_zone": price_in_demand_zone,
        "price_in_supply_zone": price_in_supply_zone,
        "dates": dates
    }


def test_balanced_signals_generates_intermediate_signal_count(mock_price_data):
    """Test that balanced signals generate more signals than strict but fewer than relaxed."""
    # Get signal counts with strict approach
    long_entries_strict, _, short_entries_strict, _ = generate_edge_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=True
    )
    
    # Get signal counts with relaxed approach
    long_entries_relaxed, _, short_entries_relaxed, _ = generate_test_edge_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=False,
        relaxed_mode=True
    )
    
    # Get signal counts with balanced approach
    long_entries_balanced, _, short_entries_balanced, _ = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=True,
        strictness=SignalStrictness.BALANCED
    )
    
    strict_count = long_entries_strict.sum() + short_entries_strict.sum()
    balanced_count = long_entries_balanced.sum() + short_entries_balanced.sum()
    relaxed_count = long_entries_relaxed.sum() + short_entries_relaxed.sum()
    
    print(f"Signal counts - Strict: {strict_count}, Balanced: {balanced_count}, Relaxed: {relaxed_count}")
    
    # Balanced should be between strict and relaxed
    assert balanced_count > strict_count, "Balanced signals should generate more signals than strict"
    assert balanced_count < relaxed_count, "Balanced signals should generate fewer signals than relaxed"


def test_strictness_parameter_delegates_correctly(mock_price_data):
    """Test that the strictness parameter properly delegates to strict/relaxed functions."""
    # Use balanced signals with STRICT strictness
    strict_via_balanced_long, _, strict_via_balanced_short, _ = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=True,
        strictness=SignalStrictness.STRICT
    )
    
    # Call the strict function directly
    direct_strict_long, _, direct_strict_short, _ = generate_edge_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=True
    )
    
    # Signals should be identical when delegating to strict
    pd.testing.assert_series_equal(strict_via_balanced_long, direct_strict_long)
    pd.testing.assert_series_equal(strict_via_balanced_short, direct_strict_short)
    
    # Similarly, test RELAXED delegation
    relaxed_via_balanced_long, _, relaxed_via_balanced_short, _ = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=True,
        strictness=SignalStrictness.RELAXED
    )
    
    direct_relaxed_long, _, direct_relaxed_short, _ = generate_test_edge_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=True,
        relaxed_mode=True
    )
    
    pd.testing.assert_series_equal(relaxed_via_balanced_long, direct_relaxed_long)
    pd.testing.assert_series_equal(relaxed_via_balanced_short, direct_relaxed_short)


def test_zone_influence_affects_signal_count(mock_price_data):
    """Test that zone influence parameter affects signal generation."""
    # Generate signals with high zone influence
    high_influence_long, _, high_influence_short, _ = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        zone_influence=0.9,  # High influence
        strictness=SignalStrictness.BALANCED
    )
    
    # Generate signals with low zone influence
    low_influence_long, _, low_influence_short, _ = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        zone_influence=0.1,  # Low influence
        strictness=SignalStrictness.BALANCED
    )
    
    high_count = high_influence_long.sum() + high_influence_short.sum()
    low_count = low_influence_long.sum() + low_influence_short.sum()
    
    # Should generate more signals with lower zone influence
    assert low_count >= high_count, "Lower zone influence should generate more signals"


def test_min_hold_period_affects_signal_timing(mock_price_data):
    """Test that minimum holding period affects exit signal timing."""
    # Generate signals with longer hold period
    _, long_exits_long_hold, _, short_exits_long_hold = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        min_hold_period=5,  # Longer hold
        strictness=SignalStrictness.BALANCED
    )
    
    # Generate signals with shorter hold period
    _, long_exits_short_hold, _, short_exits_short_hold = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        min_hold_period=1,  # Shorter hold
        strictness=SignalStrictness.BALANCED
    )
    
    # More exits with shorter hold period
    assert long_exits_short_hold.sum() >= long_exits_long_hold.sum()
    assert short_exits_short_hold.sum() >= short_exits_long_hold.sum()


def test_edge_case_all_params_at_extremes(mock_price_data):
    """Test edge case with extreme parameter values."""
    # Try extreme parameter values
    long_entries, long_exits, short_entries, short_exits = generate_balanced_signals(
        close=mock_price_data["close"],
        rsi=mock_price_data["rsi"],
        bb_upper=mock_price_data["bb_upper"],
        bb_lower=mock_price_data["bb_lower"],
        trend_ma=mock_price_data["trend_ma"],
        price_in_demand_zone=mock_price_data["price_in_demand_zone"],
        price_in_supply_zone=mock_price_data["price_in_supply_zone"],
        rsi_lower_threshold=1,       # Extreme low
        rsi_upper_threshold=99,      # Extreme high
        trend_threshold_pct=0.5,     # Very loose trend
        zone_influence=0.0,          # No zone influence
        min_hold_period=0            # No hold period
    )
    
    # Should not crash and should return valid boolean series
    assert isinstance(long_entries, pd.Series)
    assert long_entries.dtype == bool
    assert isinstance(long_exits, pd.Series)
    assert long_exits.dtype == bool
    assert isinstance(short_entries, pd.Series)
    assert short_entries.dtype == bool
    assert isinstance(short_exits, pd.Series)
    assert short_exits.dtype == bool


def test_failure_case_with_mismatched_indexes(mock_price_data):
    """Test that a ValueError is raised with mismatched series indexes."""
    shifted_dates = pd.date_range(start="2023-01-02", periods=100, freq="1H")
    mismatched_rsi = pd.Series(
        data=mock_price_data["rsi"].values,
        index=shifted_dates
    )
    
    with pytest.raises(Exception):
        # Should raise exception due to index mismatch
        generate_balanced_signals(
            close=mock_price_data["close"],
            rsi=mismatched_rsi,  # Different index
            bb_upper=mock_price_data["bb_upper"],
            bb_lower=mock_price_data["bb_lower"],
            trend_ma=mock_price_data["trend_ma"],
            price_in_demand_zone=mock_price_data["price_in_demand_zone"],
            price_in_supply_zone=mock_price_data["price_in_supply_zone"]
        )
