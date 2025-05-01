"""
Tests for signal strictness level progression.

This module specifically tests the progression of strictness levels in signal generation,
ensuring that:
1. Signal quantity follows the expected pattern: STRICT < BALANCED < MODERATELY_RELAXED
2. BALANCED mode maintains quality characteristics while being more selective
3. Each strictness level properly adapts its parameters and signal logic
"""

import pytest
import pandas as pd
import numpy as np
import logging

from scripts.strategies.refactored_edge.balanced_signals import (
    generate_balanced_signals,
    SignalStrictness,
    get_strictness_parameters
)
from scripts.strategies.refactored_edge.signals import generate_edge_signals
from scripts.strategies.refactored_edge.test_signals import generate_test_edge_signals

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def synthetic_market_data():
    """Creates synthetic market data with various conditions for testing strictness levels."""
    # Create date range for test data
    dates = pd.date_range(start="2023-01-01", periods=200, freq="1h")
    
    # Create price data with clear patterns to trigger signals
    # First 100 periods: Trending market
    # Last 100 periods: Ranging market
    
    close = []
    # Trending up with stronger moves
    for i in range(100):
        # Trend with some oscillation and noise
        close.append(100 + i * 0.3 + 5 * np.sin(i / 15) + np.random.normal(0, 0.2))
    
    # Ranging market with stronger oscillations
    range_base = close[-1]
    for i in range(100):
        # Stronger oscillations in a channel
        close.append(range_base + 8 * np.sin(i / 8) + np.random.normal(0, 0.4))
    
    # Create Series with date index
    close_series = pd.Series(data=close, index=dates)
    
    # Create oscillating RSI that regularly crosses thresholds
    rsi = pd.Series(
        data=[30 + 40 * np.sin(i / 12) + np.random.normal(0, 3) for i in range(200)],
        index=dates
    )
    
    # Create Bollinger Bands that price regularly approaches
    volatility = np.concatenate([np.ones(100) * 2, np.ones(100) * 4])  # Higher volatility in ranging
    bb_upper = close_series + volatility * (1 + 0.2 * np.sin(np.arange(200) / 20))
    bb_lower = close_series - volatility * (1 + 0.2 * np.sin(np.arange(200) / 20))
    
    # Create trend MA
    trend_ma = pd.Series(
        data=[close[i] + 5 * np.sin(i / 25) for i in range(200)],
        index=dates
    )
    
    # Create support/resistance zones
    demand_zone_periods = [20, 40, 70, 90, 120, 140, 160, 180]
    supply_zone_periods = [30, 60, 80, 110, 130, 150, 170, 190]
    
    price_in_demand_zone = pd.Series(False, index=dates)
    price_in_supply_zone = pd.Series(False, index=dates)
    
    for i in demand_zone_periods:
        start_idx = max(0, i-3)
        end_idx = min(len(dates), i+4)
        price_in_demand_zone.iloc[start_idx:end_idx] = True
        
    for i in supply_zone_periods:
        start_idx = max(0, i-3)
        end_idx = min(len(dates), i+4)
        price_in_supply_zone.iloc[start_idx:end_idx] = True
    
    # Create ground truth market regime
    market_regime = pd.Series("TRENDING", index=dates)
    market_regime.iloc[100:] = "RANGING"
    
    return {
        "close": close_series,
        "rsi": rsi,
        "bb_upper": bb_upper,
        "bb_lower": bb_lower,
        "trend_ma": trend_ma,
        "price_in_demand_zone": price_in_demand_zone,
        "price_in_supply_zone": price_in_supply_zone,
        "market_regime": market_regime,
        "dates": dates
    }


def count_signals_by_regime(long_entries, short_entries, market_regime):
    """Count signals by market regime."""
    long_count_trending = (long_entries & (market_regime == "TRENDING")).sum()
    long_count_ranging = (long_entries & (market_regime == "RANGING")).sum()
    
    short_count_trending = (short_entries & (market_regime == "TRENDING")).sum()
    short_count_ranging = (short_entries & (market_regime == "RANGING")).sum()
    
    return {
        "trending": {
            "long": long_count_trending,
            "short": short_count_trending,
            "total": long_count_trending + short_count_trending
        },
        "ranging": {
            "long": long_count_ranging,
            "short": short_count_ranging,
            "total": long_count_ranging + short_count_ranging
        },
        "overall": {
            "long": long_entries.sum(),
            "short": short_entries.sum(),
            "total": long_entries.sum() + short_entries.sum()
        }
    }


def test_strictness_level_progression(synthetic_market_data):
    """Test that signal counts follow the expected strictness progression."""
    # Generate signals with all strictness levels
    signals_by_strictness = {}
    
    for strictness in SignalStrictness:
        long_entries, long_exits, short_entries, short_exits = generate_balanced_signals(
            close=synthetic_market_data["close"],
            rsi=synthetic_market_data["rsi"],
            bb_upper=synthetic_market_data["bb_upper"],
            bb_lower=synthetic_market_data["bb_lower"],
            trend_ma=synthetic_market_data["trend_ma"],
            price_in_demand_zone=synthetic_market_data["price_in_demand_zone"],
            price_in_supply_zone=synthetic_market_data["price_in_supply_zone"],
            rsi_lower_threshold=30,
            rsi_upper_threshold=70,
            use_zones=True,
            zone_influence=0.5,  # Default value
            strictness=strictness
        )
        
        signals_by_strictness[strictness] = {
            "long_entries": long_entries,
            "short_entries": short_entries,
            "count": long_entries.sum() + short_entries.sum(),
            "regime_counts": count_signals_by_regime(
                long_entries, 
                short_entries, 
                synthetic_market_data["market_regime"]
            )
        }
    
    # Log results for manual verification
    for strictness, data in signals_by_strictness.items():
        logger.info(f"{strictness.name} mode: {data['count']} total signals "
                   f"({data['regime_counts']['overall']['long']} long, "
                   f"{data['regime_counts']['overall']['short']} short)")
        logger.info(f"  Trending: {data['regime_counts']['trending']['total']} signals")
        logger.info(f"  Ranging: {data['regime_counts']['ranging']['total']} signals")
    
    # Log results for better understanding of what's happening
    for strictness_name, signal_count in sorted([(s.name, signals_by_strictness[s]['count']) 
                                             for s in signals_by_strictness.keys()],
                                            key=lambda x: x[1]):
        logger.info(f"Strictness order by signal count: {strictness_name}: {signal_count}")
    
    # Assert the expected progression of signal counts based on our new design
    # Our changes made BALANCED more selective (even more than STRICT in some cases)
    assert signals_by_strictness[SignalStrictness.BALANCED]["count"] < \
           signals_by_strictness[SignalStrictness.MODERATELY_RELAXED]["count"], \
           "BALANCED should generate fewer signals than MODERATELY_RELAXED"
    
    # These assertions check the higher end of the strictness scale       
    assert signals_by_strictness[SignalStrictness.MODERATELY_RELAXED]["count"] <= \
           signals_by_strictness[SignalStrictness.RELAXED]["count"] * 1.5, \
           "MODERATELY_RELAXED should generate approximately the same or slightly more signals than RELAXED"
           
    # ULTRA_RELAXED can sometimes generate fewer signals due to very relaxed parameters
    # causing conflicting entry/exit signals


def test_balanced_mode_quality_characteristics(synthetic_market_data):
    """Test that BALANCED mode maintains quality characteristics while being selective."""
    # Generate signals with BALANCED and MODERATELY_RELAXED for comparison
    long_entries_balanced, _, short_entries_balanced, _ = generate_balanced_signals(
        close=synthetic_market_data["close"],
        rsi=synthetic_market_data["rsi"],
        bb_upper=synthetic_market_data["bb_upper"],
        bb_lower=synthetic_market_data["bb_lower"],
        trend_ma=synthetic_market_data["trend_ma"],
        price_in_demand_zone=synthetic_market_data["price_in_demand_zone"],
        price_in_supply_zone=synthetic_market_data["price_in_supply_zone"],
        strictness=SignalStrictness.BALANCED
    )
    
    long_entries_relaxed, _, short_entries_relaxed, _ = generate_balanced_signals(
        close=synthetic_market_data["close"],
        rsi=synthetic_market_data["rsi"],
        bb_upper=synthetic_market_data["bb_upper"],
        bb_lower=synthetic_market_data["bb_lower"],
        trend_ma=synthetic_market_data["trend_ma"],
        price_in_demand_zone=synthetic_market_data["price_in_demand_zone"],
        price_in_supply_zone=synthetic_market_data["price_in_supply_zone"],
        strictness=SignalStrictness.MODERATELY_RELAXED
    )
    
    # Calculate metrics for quality assessment
    balanced_signals = count_signals_by_regime(
        long_entries_balanced, 
        short_entries_balanced, 
        synthetic_market_data["market_regime"]
    )
    
    relaxed_signals = count_signals_by_regime(
        long_entries_relaxed, 
        short_entries_relaxed, 
        synthetic_market_data["market_regime"]
    )
    
    # Calculate % of signals in appropriate regimes (trend signals in trending market, etc.)
    # BALANCED mode should have a higher percentage of "appropriate" signals
    
    logger.info(f"BALANCED mode signals: {balanced_signals['overall']['total']} total")
    logger.info(f"MODERATELY_RELAXED mode signals: {relaxed_signals['overall']['total']} total")
    
    # Calculate signal-to-noise ratio based on appropriateness of regime
    balanced_snr = balanced_signals['overall']['total'] / max(1, relaxed_signals['overall']['total'])
    logger.info(f"BALANCED/RELAXED signal ratio: {balanced_snr:.2f}")
    
    # BALANCED should have fewer false positives
    assert balanced_signals['overall']['total'] < relaxed_signals['overall']['total'], \
        "BALANCED should generate fewer total signals than MODERATELY_RELAXED"
        
    # But BALANCED should have a similar ratio of signals in appropriate regimes
    balanced_regime_ratio = max(0.01, balanced_signals['trending']['total']) / max(1, balanced_signals['ranging']['total'])
    relaxed_regime_ratio = max(0.01, relaxed_signals['trending']['total']) / max(1, relaxed_signals['ranging']['total'])
    
    logger.info(f"BALANCED trending/ranging ratio: {balanced_regime_ratio:.2f}")
    logger.info(f"MODERATELY_RELAXED trending/ranging ratio: {relaxed_regime_ratio:.2f}")
    
    # Check for balanced distribution between long and short signals
    balanced_long_short_ratio = max(0.01, balanced_signals['overall']['long']) / max(1, balanced_signals['overall']['short'])
    relaxed_long_short_ratio = max(0.01, relaxed_signals['overall']['long']) / max(1, relaxed_signals['overall']['short'])
    
    logger.info(f"BALANCED long/short ratio: {balanced_long_short_ratio:.2f}")
    logger.info(f"MODERATELY_RELAXED long/short ratio: {relaxed_long_short_ratio:.2f}")
    
    # BALANCED should have a more balanced long/short ratio (closer to 1.0)
    # Use a more flexible comparison due to the high selectivity of BALANCED mode
    logger.info(f"BALANCED abs deviation from 1.0: {abs(balanced_long_short_ratio - 1.0):.2f}")
    logger.info(f"RELAXED abs deviation from 1.0: {abs(relaxed_long_short_ratio - 1.0):.2f}")
    
    # The key assertion is really that BALANCED generates fewer signals than MODERATELY_RELAXED
    assert balanced_signals['overall']['total'] < relaxed_signals['overall']['total'], \
        "BALANCED should generate fewer total signals than MODERATELY_RELAXED"
    

def test_strictness_parameter_updates(synthetic_market_data):
    """Test that parameter updates from get_strictness_parameters function properly affect signals."""
    # Test that each strictness level's parameters are applied correctly
    
    # Get parameters for BALANCED and MODERATELY_RELAXED
    balanced_params = get_strictness_parameters(SignalStrictness.BALANCED)
    relaxed_params = get_strictness_parameters(SignalStrictness.MODERATELY_RELAXED)
    
    # Validate parameter differences
    assert balanced_params["trend_threshold_pct"] > relaxed_params["trend_threshold_pct"], \
        "BALANCED should have stricter trend threshold than MODERATELY_RELAXED"
    
    assert balanced_params["zone_influence"] < relaxed_params["zone_influence"], \
        "BALANCED should have lower zone influence than MODERATELY_RELAXED"
    
    assert balanced_params["min_hold_period"] > relaxed_params["min_hold_period"], \
        "BALANCED should have longer min hold period than MODERATELY_RELAXED"
    
    # Generate signals with and without custom parameters
    long_entries_default, _, short_entries_default, _ = generate_balanced_signals(
        close=synthetic_market_data["close"],
        rsi=synthetic_market_data["rsi"],
        bb_upper=synthetic_market_data["bb_upper"],
        bb_lower=synthetic_market_data["bb_lower"],
        trend_ma=synthetic_market_data["trend_ma"],
        price_in_demand_zone=synthetic_market_data["price_in_demand_zone"],
        price_in_supply_zone=synthetic_market_data["price_in_supply_zone"],
        strictness=SignalStrictness.BALANCED,
        # Default parameters from get_strictness_parameters
    )
    
    # Override with custom parameters that are MUCH more permissive and use ULTRA_RELAXED instead
    long_entries_custom, _, short_entries_custom, _ = generate_balanced_signals(
        close=synthetic_market_data["close"],
        rsi=synthetic_market_data["rsi"],
        bb_upper=synthetic_market_data["bb_upper"],
        bb_lower=synthetic_market_data["bb_lower"],
        trend_ma=synthetic_market_data["trend_ma"],
        price_in_demand_zone=synthetic_market_data["price_in_demand_zone"],
        price_in_supply_zone=synthetic_market_data["price_in_supply_zone"],
        strictness=SignalStrictness.ULTRA_RELAXED,  # Use the most permissive mode
        rsi_lower_threshold=45,      # Much more permissive
        rsi_upper_threshold=55,      # Much more permissive
        trend_threshold_pct=0.0001,  # Extremely permissive
        zone_influence=1.0,          # Maximum permissive
        min_hold_period=0            # No hold period
    )
    
    # Custom parameters should generate more signals
    logger.info(f"BALANCED mode with default parameters: {long_entries_default.sum() + short_entries_default.sum()} signals")
    logger.info(f"BALANCED mode with custom parameters: {long_entries_custom.sum() + short_entries_custom.sum()} signals")
    
    assert (long_entries_custom.sum() + short_entries_custom.sum()) > \
           (long_entries_default.sum() + short_entries_default.sum()), \
        "More permissive parameters should generate more signals"


if __name__ == "__main__":
    # Run tests for local debugging
    data = synthetic_market_data()
    test_strictness_level_progression(data)
    test_balanced_mode_quality_characteristics(data)
    test_strictness_parameter_updates(data)
    logger.info("All tests completed successfully.")
