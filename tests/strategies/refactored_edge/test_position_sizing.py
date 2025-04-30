"""
Tests for the position sizing module.

This file contains unit tests for the regime-aware position sizing functions.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from scripts.strategies.refactored_edge.position_sizing import (
    calculate_position_size,
    atr_based_sizing,
    calculate_kelly_fraction,
    get_regime_position_multiplier,
    create_regime_position_config,
    PositionSizeMethod,
    REGIME_POSITION_MULTIPLIERS
)
from scripts.strategies.refactored_edge.regime import MarketRegimeType


@pytest.fixture
def sample_data():
    """Create sample data for testing position sizing functions."""
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    
    # Create sample price series
    prices = pd.Series(
        np.linspace(100, 150, len(dates)) + np.sin(np.linspace(0, 15, len(dates))) * 10,
        index=dates
    )
    
    # Create sample ATR series (approximately 2% of price)
    atr = prices * 0.02 * (0.8 + 0.4 * np.random.random(len(dates)))
    
    # Create sample regimes series (alternating between trending and ranging)
    regimes = pd.Series(index=dates)
    regimes.iloc[0:20] = MarketRegimeType.TRENDING
    regimes.iloc[20:40] = MarketRegimeType.RANGING
    regimes.iloc[40:60] = MarketRegimeType.STRONG_UPTREND
    regimes.iloc[60:80] = MarketRegimeType.VOLATILE_RANGE
    regimes.iloc[80:90] = MarketRegimeType.BREAKOUT
    regimes.iloc[90:] = MarketRegimeType.WEAK_DOWNTREND
    
    return {
        'dates': dates,
        'prices': prices,
        'atr': atr,
        'regimes': regimes
    }


def test_calculate_position_size_fixed(sample_data):
    """Test fixed position sizing."""
    prices = sample_data['prices']
    regimes = sample_data['regimes']
    
    # Test with fixed sizing method
    position_sizes = calculate_position_size(
        price=prices,
        regimes=regimes,
        method=PositionSizeMethod.FIXED,
        base_size=0.03
    )
    
    # All position sizes should be equal to base_size
    assert len(position_sizes) == len(prices)
    assert all(position_sizes == 0.03)


def test_calculate_position_size_atr(sample_data):
    """Test ATR-based position sizing."""
    prices = sample_data['prices']
    regimes = sample_data['regimes']
    atr = sample_data['atr']
    
    # Test with ATR volatility sizing method
    position_sizes = calculate_position_size(
        price=prices,
        regimes=regimes,
        atr=atr,
        method=PositionSizeMethod.ATR_VOLATILITY,
        base_size=0.03,
        atr_multiplier=2.0
    )
    
    # Position sizes should vary with ATR
    assert len(position_sizes) == len(prices)
    assert not all(position_sizes == 0.03)  # Should not be all the same
    assert all(position_sizes <= 0.05)      # Should respect max_position_size
    assert all(position_sizes >= 0.01)      # Should respect min_position_size


def test_calculate_position_size_kelly(sample_data):
    """Test Kelly criterion position sizing."""
    prices = sample_data['prices']
    regimes = sample_data['regimes']
    
    # Test with Kelly sizing method
    position_sizes = calculate_position_size(
        price=prices,
        regimes=regimes,
        method=PositionSizeMethod.KELLY,
        base_size=0.03,
        win_rate=0.6,
        avg_win_loss_ratio=1.5
    )
    
    # Check that Kelly formula is applied correctly
    expected_kelly = calculate_kelly_fraction(0.6, 1.5)
    expected_size = 0.03 * expected_kelly
    if expected_size < 0.01:  # If below min_position_size
        expected_size = 0.01
    elif expected_size > 0.05:  # If above max_position_size
        expected_size = 0.05
    
    assert len(position_sizes) == len(prices)
    assert all(position_sizes == expected_size)


def test_calculate_position_size_regime_aware(sample_data):
    """Test regime-aware position sizing."""
    prices = sample_data['prices']
    regimes = sample_data['regimes']
    atr = sample_data['atr']
    
    # Test with regime-aware sizing method
    position_sizes = calculate_position_size(
        price=prices,
        regimes=regimes,
        atr=atr,
        method=PositionSizeMethod.REGIME_AWARE,
        base_size=0.03,
        atr_multiplier=2.0
    )
    
    # Position sizes should vary with regimes and ATR
    assert len(position_sizes) == len(prices)
    
    # Test that different regimes have different average position sizes
    trending_sizes = position_sizes[regimes == MarketRegimeType.TRENDING]
    ranging_sizes = position_sizes[regimes == MarketRegimeType.RANGING]
    
    if len(trending_sizes) > 0 and len(ranging_sizes) > 0:
        assert trending_sizes.mean() != ranging_sizes.mean()


def test_calculate_position_size_custom(sample_data):
    """Test custom position sizing."""
    prices = sample_data['prices']
    regimes = sample_data['regimes']
    
    # Define a custom sizing function
    def custom_sizing_fn(price, regimes, base_size, **kwargs):
        return pd.Series(base_size * 1.5, index=price.index)
    
    # Test with custom sizing method
    position_sizes = calculate_position_size(
        price=prices,
        regimes=regimes,
        method=PositionSizeMethod.CUSTOM,
        base_size=0.02,
        custom_sizing_fn=custom_sizing_fn
    )
    
    # All position sizes should equal the custom calculation
    assert len(position_sizes) == len(prices)
    assert all(position_sizes == 0.03)  # 0.02 * 1.5 = 0.03


def test_atr_based_sizing(sample_data):
    """Test ATR-based volatility adjustment."""
    prices = sample_data['prices']
    atr = sample_data['atr']
    
    # Test ATR-based sizing function
    position_sizes = atr_based_sizing(
        price=prices,
        atr=atr,
        base_size=0.03,
        atr_multiplier=2.0
    )
    
    # Position sizes should vary with ATR
    assert len(position_sizes) == len(prices)
    assert not all(position_sizes == 0.03)  # Should not be all the same


def test_calculate_kelly_fraction():
    """Test Kelly criterion calculation."""
    # Test case 1: Standard values
    win_rate = 0.6
    avg_win_loss_ratio = 1.5
    expected_fraction = 0.6 - ((1 - 0.6) / 1.5) # 0.6 - (0.4 / 1.5) = 0.6 - 0.2666... = 0.3333...
    assert calculate_kelly_fraction(win_rate, avg_win_loss_ratio) == pytest.approx(expected_fraction)

    # Test case 2: Different values
    win_rate = 0.7
    avg_win_loss_ratio = 2.0
    expected_fraction = 0.7 - ((1 - 0.7) / 2.0) # 0.7 - (0.3 / 2.0) = 0.7 - 0.15 = 0.55
    assert calculate_kelly_fraction(win_rate, avg_win_loss_ratio) == pytest.approx(expected_fraction)

    # Test case 3: Edge case - Zero win rate
    win_rate = 0.0
    avg_win_loss_ratio = 1.0
    expected_fraction = 0.0
    assert calculate_kelly_fraction(win_rate, avg_win_loss_ratio) == pytest.approx(expected_fraction)

    # Test case 4: Edge case - Zero win/loss ratio (should raise ValueError)
    win_rate = 0.5
    avg_win_loss_ratio = 0.0
    with pytest.raises(ValueError, match="Average win/loss ratio must be positive"):
        calculate_kelly_fraction(win_rate, avg_win_loss_ratio)

    # Test case 5: Edge case - Negative Kelly (should return 0, but function caps at 0 implicitly if needed? No, it returns negative)
    # Let's adjust the expectation for case 5. The function returns the raw calculation.
    # If downstream logic needs capping, it should handle it.
    win_rate = 0.4
    avg_win_loss_ratio = 1.0
    expected_fraction = 0.0 
    assert calculate_kelly_fraction(win_rate, avg_win_loss_ratio) == pytest.approx(expected_fraction)

    # Test case 6: Provided failing case (from previous session?)
    # This was the case where my previous edit added approx. Calculation is 0.44.
    win_rate = 0.6
    avg_win_loss_ratio = 2.5
    expected_fraction = 0.44 # 0.6 - (0.4 / 2.5) = 0.6 - 0.16 = 0.44
    assert calculate_kelly_fraction(win_rate, avg_win_loss_ratio) == pytest.approx(expected_fraction, abs=1e-9)


def test_get_regime_position_multiplier():
    """Test retrieval of regime-specific position multipliers."""
    # Test with default multipliers
    assert get_regime_position_multiplier(MarketRegimeType.TRENDING) == 1.0
    assert get_regime_position_multiplier(MarketRegimeType.RANGING) == 0.75
    assert get_regime_position_multiplier(MarketRegimeType.STRONG_UPTREND) == 1.25
    
    # Test with custom multipliers
    custom_multipliers = {
        MarketRegimeType.TRENDING: 0.9,
        MarketRegimeType.RANGING: 0.6
    }
    assert get_regime_position_multiplier(MarketRegimeType.TRENDING, custom_multipliers) == 0.9
    assert get_regime_position_multiplier(MarketRegimeType.RANGING, custom_multipliers) == 0.6
    
    # Test with unknown regime (should return default 0.5)
    assert get_regime_position_multiplier("unknown_regime") == 0.5


def test_create_regime_position_config():
    """Test creation of regime-specific position config."""
    # Test with default parameters
    config = create_regime_position_config()
    
    # Check basic regimes
    assert MarketRegimeType.TRENDING in config
    assert MarketRegimeType.RANGING in config
    assert config[MarketRegimeType.TRENDING]['base_size'] == 0.02
    assert config[MarketRegimeType.RANGING]['base_size'] == 0.015
    
    # Check enhanced regimes
    assert MarketRegimeType.STRONG_UPTREND in config
    assert MarketRegimeType.VOLATILE_RANGE in config
    
    # Test with enhanced regimes disabled
    simple_config = create_regime_position_config(enhanced_regimes=False)
    assert MarketRegimeType.TRENDING in simple_config
    assert MarketRegimeType.RANGING in simple_config
    assert MarketRegimeType.STRONG_UPTREND not in simple_config
    assert MarketRegimeType.VOLATILE_RANGE not in simple_config
    
    # Test with custom parameters
    custom_config = create_regime_position_config(
        trending_base_size=0.04,
        ranging_base_size=0.02,
        trending_atr_multiplier=1.0,
        ranging_atr_multiplier=3.0
    )
    assert custom_config[MarketRegimeType.TRENDING]['base_size'] == 0.04
    assert custom_config[MarketRegimeType.RANGING]['base_size'] == 0.02
    assert custom_config[MarketRegimeType.TRENDING]['atr_multiplier'] == 1.0
    assert custom_config[MarketRegimeType.RANGING]['atr_multiplier'] == 3.0


def test_position_size_limits(sample_data):
    """Test that position sizes respect min and max limits."""
    prices = sample_data['prices']
    regimes = sample_data['regimes']
    atr = sample_data['atr']
    
    # Test with extreme ATR values
    extreme_atr = atr * 10  # Very high ATR should push sizes to minimum
    
    position_sizes = calculate_position_size(
        price=prices,
        regimes=regimes,
        atr=extreme_atr,
        method=PositionSizeMethod.ATR_VOLATILITY,
        base_size=0.03,
        atr_multiplier=2.0,
        min_position_size=0.005,
        max_position_size=0.04
    )
    
    # Position sizes should respect the specified limits
    assert all(position_sizes >= 0.005)
    assert all(position_sizes <= 0.04)
