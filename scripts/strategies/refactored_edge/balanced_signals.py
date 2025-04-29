"""
Balanced signal generation module for the Edge Multi-Factor strategy.

This module provides a configurable approach to signal generation that balances
between the strict (standard) and relaxed (test) approaches, allowing for
more flexible strategy tuning while maintaining signal quality.
"""

import logging
import pandas as pd
from typing import Tuple, Optional, Literal
from enum import Enum
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

class SignalStrictness(str, Enum):
    """Enum for signal strictness levels."""
    STRICT = "strict"       # Original strict signals
    BALANCED = "balanced"   # New balanced approach
    RELAXED = "relaxed"     # Testing mode relaxed signals


def generate_balanced_signals(
    close: pd.Series,
    rsi: pd.Series,
    bb_upper: pd.Series,
    bb_lower: pd.Series,
    trend_ma: pd.Series,
    price_in_demand_zone: pd.Series,
    price_in_supply_zone: pd.Series,
    rsi_lower_threshold: float = 30,
    rsi_upper_threshold: float = 70,
    use_zones: bool = False,
    trend_strict: bool = True,
    min_hold_period: int = 2,
    trend_threshold_pct: float = 0.01,  # % distance from MA to consider in trend
    zone_influence: float = 0.5,  # How strongly zones influence signals (0-1)
    strictness: SignalStrictness = SignalStrictness.BALANCED
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Generates entry and exit signals with configurable strictness for the Edge Multi-Factor strategy.
    
    This balanced approach allows for more trades than the strict approach, but
    with higher quality filters than the fully relaxed approach. Signal generation
    strictness and other parameters can be adjusted to fine-tune the strategy.
    
    Args:
        close: Series of closing prices
        rsi: Series of RSI values
        bb_upper: Series of Bollinger Band upper values
        bb_lower: Series of Bollinger Band lower values
        trend_ma: Series of trend moving average values
        price_in_demand_zone: Boolean Series indicating if price is in a demand zone
        price_in_supply_zone: Boolean Series indicating if price is in a supply zone
        rsi_lower_threshold: RSI threshold for oversold condition (default: 30)
        rsi_upper_threshold: RSI threshold for overbought condition (default: 70)
        use_zones: Whether to use zone filters (default: False)
        trend_strict: Whether to strictly enforce trend filter (default: True)
        min_hold_period: Minimum holding period in bars (default: 2)
        trend_threshold_pct: Percentage threshold for trend determination (default: 0.01)
        zone_influence: Strength of zone influence from 0-1 (default: 0.5)
        strictness: Signal strictness level (strict, balanced, relaxed)

    Returns:
        tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
            Boolean Series for (long_entries, long_exits, short_entries, short_exits).
    """
    logger.info(f"Generating {strictness} signals with zone_influence={zone_influence}, "
                f"min_hold_period={min_hold_period}")
    
    # If strict or relaxed is specified, delegate to appropriate function
    if strictness == SignalStrictness.STRICT:
        # Import here to avoid circular import
        from scripts.strategies.refactored_edge.signals import generate_edge_signals
        return generate_edge_signals(
            close=close, rsi=rsi, bb_upper=bb_upper, bb_lower=bb_lower,
            trend_ma=trend_ma, price_in_demand_zone=price_in_demand_zone,
            price_in_supply_zone=price_in_supply_zone,
            rsi_lower_threshold=rsi_lower_threshold,
            rsi_upper_threshold=rsi_upper_threshold,
            use_zones=use_zones, trend_strict=trend_strict
        )
    elif strictness == SignalStrictness.RELAXED:
        # Import here to avoid circular import
        from scripts.strategies.refactored_edge.test_signals import generate_test_edge_signals
        return generate_test_edge_signals(
            close=close, rsi=rsi, bb_upper=bb_upper, bb_lower=bb_lower,
            trend_ma=trend_ma, price_in_demand_zone=price_in_demand_zone,
            price_in_supply_zone=price_in_supply_zone,
            rsi_lower_threshold=rsi_lower_threshold,
            rsi_upper_threshold=rsi_upper_threshold,
            use_zones=use_zones, trend_strict=trend_strict,
            relaxed_mode=True
        )
    
    # Calculate Basic Indicator Conditions
    rsi_oversold = rsi < rsi_lower_threshold
    rsi_overbought = rsi > rsi_upper_threshold
    price_below_bb = close < bb_lower
    price_above_bb = close > bb_upper
    
    # Semi-strict trend filter using percentage threshold
    trend_distance = (close - trend_ma) / trend_ma
    trend_up = trend_distance > -trend_threshold_pct  # Allow slightly below MA
    trend_down = trend_distance < trend_threshold_pct  # Allow slightly above MA
    
    if trend_strict:
        trend_filter_long = trend_up
        trend_filter_short = trend_down
    else:
        # Less strict trend filter but not completely ignored
        trend_filter_long = pd.Series(True, index=close.index)
        trend_filter_short = pd.Series(True, index=close.index)

    # Zone conditions with configurable influence
    if use_zones:
        # Create zone signals with adjustable strength
        # At zone_influence=1, behaves like strict mode
        # At zone_influence=0, zones have no effect 
        
        # For long entries, we need a demand zone (buying)
        if zone_influence >= 1.0:
            # Strict: must be in the zone
            zone_long_entry_condition = price_in_demand_zone
        elif zone_influence <= 0.0:
            # Ignore zones completely
            zone_long_entry_condition = pd.Series(True, index=close.index)
        else:
            # Create probabilistic zone entry based on influence factor
            # If in a zone, always True; if not, use influence factor
            zone_long_entry_condition = price_in_demand_zone | np.random.random(len(close)) > zone_influence
            
        # For short entries, we need a supply zone (selling)
        if zone_influence >= 1.0:
            zone_short_entry_condition = price_in_supply_zone
        elif zone_influence <= 0.0:
            zone_short_entry_condition = pd.Series(True, index=close.index)
        else:
            zone_short_entry_condition = price_in_supply_zone | np.random.random(len(close)) > zone_influence
            
        # For exits, we use the opposite zones
        zone_long_exit_trigger = price_in_supply_zone & (np.random.random(len(close)) < zone_influence)
        zone_short_exit_trigger = price_in_demand_zone & (np.random.random(len(close)) < zone_influence)
    else:
        # If zones aren't used, these conditions are always met/not met
        zone_long_entry_condition = pd.Series(True, index=close.index)
        zone_long_exit_trigger = pd.Series(False, index=close.index)
        zone_short_entry_condition = pd.Series(True, index=close.index)
        zone_short_exit_trigger = pd.Series(False, index=close.index)

    # BALANCED ENTRY CONDITIONS:
    # Require RSI signal AND (price OR trend) - more trades than strict but better quality than relaxed
    long_entries = (
        rsi_oversold & (price_below_bb | trend_filter_long) & zone_long_entry_condition
    )
    
    short_entries = (
        rsi_overbought & (price_above_bb | trend_filter_short) & zone_short_entry_condition
    )
    
    # BALANCED EXIT CONDITIONS:
    # Require either RSI OR price (more exits than strict) but with some filtering
    # Difference from relaxed: not purely OR conditions, adds some filtering
    long_exits = (
        (rsi_overbought & close > trend_ma) |  # RSI overbought when above trend
        (price_above_bb & rsi > 50) |          # Above upper band with RSI above neutral
        zone_long_exit_trigger                  # Zone exit with influence factor
    )
    
    short_exits = (
        (rsi_oversold & close < trend_ma) |    # RSI oversold when below trend
        (price_below_bb & rsi < 50) |          # Below lower band with RSI below neutral
        zone_short_exit_trigger                 # Zone exit with influence factor
    )

    # Ensure exits override entries on same bar
    long_entries = long_entries & ~long_exits
    short_entries = short_entries & ~short_exits

    # Fill NaN values
    long_entries = long_entries.fillna(False)
    long_exits = long_exits.fillna(False)
    short_entries = short_entries.fillna(False)
    short_exits = short_exits.fillna(False)

    # Apply minimum holding period (configurable but shorter than strict)
    if min_hold_period > 0:
        # For long positions
        long_entries_idx = long_entries[long_entries].index
        for idx in long_entries_idx:
            loc_idx = long_exits.index.get_loc(idx)
            end_idx = min(loc_idx + min_hold_period, len(long_exits))
            if loc_idx < len(long_exits):
                long_exits.iloc[loc_idx:end_idx] = False
                
        # For short positions
        short_entries_idx = short_entries[short_entries].index
        for idx in short_entries_idx:
            loc_idx = short_exits.index.get_loc(idx)
            end_idx = min(loc_idx + min_hold_period, len(short_exits))
            if loc_idx < len(short_exits):
                short_exits.iloc[loc_idx:end_idx] = False
    
    # Log signal counts for debugging
    logger.debug(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries "
                f"with {strictness} mode")
    
    return long_entries, long_exits, short_entries, short_exits
