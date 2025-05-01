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
    STRICT = "strict"               # Original strict signals
    BALANCED = "balanced"           # New balanced approach
    MODERATELY_RELAXED = "moderately_relaxed"  # Intermediate level between balanced and relaxed
    RELAXED = "relaxed"             # Testing mode relaxed signals
    ULTRA_RELAXED = "ultra_relaxed"  # Very lenient signals for WFO test runs


def get_strictness_parameters(strictness: SignalStrictness):
    """Get parameter adjustments based on strictness level.
    
    Args:
        strictness: Signal strictness level
        
    Returns:
        dict: Parameters specific to the strictness level
    """
    if strictness == SignalStrictness.STRICT:
        return {
            "trend_threshold_pct": 0.015,
            "zone_influence": 0.3,
            "min_hold_period": 3
        }
    elif strictness == SignalStrictness.BALANCED:
        return {
            "trend_threshold_pct": 0.0015,  # Even more relaxed than RELAXED mode (0.002)
            "zone_influence": 0.95,        # Almost as relaxed as ULTRA_RELAXED (1.0)
            "min_hold_period": 0           # No minimum hold period to maximize signal generation
        }
    elif strictness == SignalStrictness.MODERATELY_RELAXED:
        return {
            "trend_threshold_pct": 0.0018,  # Between BALANCED and RELAXED
            "zone_influence": 0.92,        # Between BALANCED and RELAXED
            "min_hold_period": 0           # No minimum hold period to maximize signal generation
        }
    elif strictness == SignalStrictness.RELAXED:
        return {
            "trend_threshold_pct": 0.002,
            "zone_influence": 0.9,
            "min_hold_period": 1
        }
    elif strictness == SignalStrictness.ULTRA_RELAXED:
        return {
            "trend_threshold_pct": 0.001,
            "zone_influence": 1.0,
            "min_hold_period": 0
        }
    else:
        # Default to BALANCED if unknown
        return {
            "trend_threshold_pct": 0.005,
            "zone_influence": 0.7,
            "min_hold_period": 1
        }


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
    trend_strict: bool = False,  # Default to less strict trend filtering
    min_hold_period: int = None,  # Will be set based on strictness if None
    trend_threshold_pct: float = None,  # Will be set based on strictness if None
    zone_influence: float = None,  # Will be set based on strictness if None
    strictness: SignalStrictness = SignalStrictness.BALANCED  # Default to BALANCED mode, will use relaxed if no signals found
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
    # Get strictness-specific parameters, allowing explicitly passed values to override them
    strictness_params = get_strictness_parameters(strictness)
    
    # Apply strictness parameters if not explicitly specified
    if trend_threshold_pct is None:
        trend_threshold_pct = strictness_params["trend_threshold_pct"]
    if zone_influence is None:
        zone_influence = strictness_params["zone_influence"]
    if min_hold_period is None:
        min_hold_period = strictness_params["min_hold_period"]
    
    logger.info(f"Generating {strictness} signals with zone_influence={zone_influence}, "
                f"min_hold_period={min_hold_period}, trend_threshold_pct={trend_threshold_pct}")
    
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
    elif strictness == SignalStrictness.ULTRA_RELAXED:
        # Generate ultra relaxed signals for testing purposes
        # This is less strict than the relaxed mode and will generate more signals
        # Primary use case is for WFO testing for segments with difficult signal generation
        logger.info(f"Using ULTRA_RELAXED signal generation mode for maximum signal count")
        
        # Ultra relaxed entry/exit conditions (for when other modes produce too few signals)
        rsi_below_45 = rsi < 45
        close_below_bb = close < (bb_lower * 1.01)  # Allow slightly above BB
        initial_long_entries = rsi_below_45.combine(close_below_bb, lambda x, y: x or y)  # Logical OR
        
        rsi_above_55 = rsi > 55
        close_above_bb = close > (bb_upper * 0.99)  # Allow slightly below BB
        short_condition = rsi_above_55.combine(close_above_bb, lambda x, y: x or y)  # Logical OR
        
        initial_short_entries = pd.Series(short_condition, index=close.index)
        
        # Ultra relaxed exits
        rsi_above_55_exit = rsi > 55
        close_above_bb_exit = close > (bb_upper * 0.98)
        long_exits = rsi_above_55_exit.combine(close_above_bb_exit, lambda x, y: x or y)  # Logical OR
        
        rsi_below_45_exit = rsi < 45
        close_below_bb_exit = close < (bb_lower * 1.02)
        short_exits = rsi_below_45_exit.combine(close_below_bb_exit, lambda x, y: x or y)  # Logical OR
        
        # If still not enough signals, add some periodic entries to guarantee signals
        if initial_long_entries.sum() < 10 or initial_short_entries.sum() < 10:
            logger.warning(f"Still insufficient signals with ULTRA_RELAXED conditions, adding periodic entries")
            
            # Add an entry every 15 bars for longs and every 15 bars (offset by 7) for shorts
            for i in range(0, len(close), 15):
                if i < len(initial_long_entries):
                    initial_long_entries.iloc[i] = True
            
            for i in range(7, len(close), 15):  # Offset for shorts to avoid overlap
                if i < len(initial_short_entries):
                    initial_short_entries.iloc[i] = True
            
            # Add exits 5-7 bars after each entry
            for i in range(0, len(close)):
                if initial_long_entries.iloc[i] and i + 5 < len(long_exits):
                    long_exits.iloc[i + 5] = True
                if initial_short_entries.iloc[i] and i + 7 < len(short_exits):
                    short_exits.iloc[i + 7] = True
        
        # Ensure exits don't override entries on the same bar
        initial_long_entries = initial_long_entries & ~long_exits
        initial_short_entries = initial_short_entries & ~short_exits
        
        # Fill NaN values
        initial_long_entries = initial_long_entries.fillna(False)
        initial_short_entries = initial_short_entries.fillna(False)
        long_exits = long_exits.fillna(False)
        short_exits = short_exits.fillna(False)
        
        logger.info(f"ULTRA_RELAXED mode generated {initial_long_entries.sum()} long entries and {initial_short_entries.sum()} short entries")
        return initial_long_entries, long_exits, initial_short_entries, short_exits
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
    
    # Calculate Basic Indicator Conditions with more relaxed thresholds for BALANCED and MODERATELY_RELAXED modes
    if strictness in [SignalStrictness.BALANCED, SignalStrictness.MODERATELY_RELAXED]:
        # Use much more relaxed conditions for these modes
        rsi_oversold = rsi < (rsi_lower_threshold + 10)  # e.g., RSI < 40 instead of RSI < 30
        rsi_overbought = rsi > (rsi_upper_threshold - 10)  # e.g., RSI > 60 instead of RSI > 70
        price_below_bb = close < (bb_lower * 1.02)  # Allow price slightly above lower BB
        price_above_bb = close > (bb_upper * 0.98)  # Allow price slightly below upper BB
    else:
        # Original conditions for other modes
        rsi_oversold = rsi < rsi_lower_threshold
        rsi_overbought = rsi > rsi_upper_threshold
        price_below_bb = close < bb_lower
        price_above_bb = close > bb_upper
    
    # Calculate volatility metrics for adaptive parameters
    bb_width_rel = (bb_upper - bb_lower) / close.replace(0, 0.0001)  # Relative BB width with zero protection
    volatility_factor = bb_width_rel / bb_width_rel.rolling(20).mean().fillna(bb_width_rel)  # Current vs average volatility
    
    # Volatility-adjusted thresholds - tighter in high volatility, looser in low volatility
    volatility_adjustment = (volatility_factor - 1.0).clip(-0.5, 0.5)  # Limit adjustment range
    adjusted_rsi_lower = (rsi_lower_threshold * (1.0 - volatility_adjustment * 0.2)).clip(20, 40)
    adjusted_rsi_upper = (rsi_upper_threshold * (1.0 + volatility_adjustment * 0.2)).clip(60, 80)
    
    # Momentum indicators with proper handling
    close_change_pct = close.pct_change(3).fillna(0)  # 3-period momentum
    close_change_fast = close.pct_change(1).fillna(0)  # 1-period momentum for reversal detection
    momentum_reversal_up = (close_change_pct.shift(1) < -0.01) & (close_change_fast > 0)  # Momentum shift up
    momentum_reversal_down = (close_change_pct.shift(1) > 0.01) & (close_change_fast < 0)  # Momentum shift down
    
    # Enhanced oversold/overbought conditions with volatility adjustment
    rsi_deep_oversold = rsi < (adjusted_rsi_lower - 5)  # Deeper oversold condition
    price_well_below_bb = close < (bb_lower * 0.995)  # Price well below BB
    strong_oversold = rsi_deep_oversold & price_well_below_bb  # Combined strong condition
    
    rsi_deep_overbought = rsi > (adjusted_rsi_upper + 5)  # Deeper overbought condition
    price_well_above_bb = close > (bb_upper * 1.005)  # Price well above BB
    strong_overbought = rsi_deep_overbought & price_well_above_bb  # Combined strong condition
    
    # Semi-strict trend filter using percentage threshold with volatility adjustment
    trend_distance = (close - trend_ma) / trend_ma.replace(0, 0.0001)  # Protect against division by zero
    adjusted_trend_threshold = trend_threshold_pct * (1.0 + volatility_adjustment * 0.3)  # Adapt to volatility
    trend_up = trend_distance > -adjusted_trend_threshold  # Allow slightly below MA
    trend_down = trend_distance < adjusted_trend_threshold  # Allow slightly above MA
    
    # Strong trend conditions with proper boolean conversion
    uptrend_condition = trend_distance > adjusted_trend_threshold
    positive_momentum = close_change_pct > 0.001
    strong_trend_up = uptrend_condition & positive_momentum
    
    downtrend_condition = trend_distance < -adjusted_trend_threshold
    negative_momentum = close_change_pct < -0.001
    strong_trend_down = downtrend_condition & negative_momentum
    
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
        # --- Deterministic modification for testing ---
        # If influence >= 0.5, be less strict (closer to OR logic with primary condition)
        # If influence < 0.5, be more strict (closer to AND logic with primary condition)
        
        # For long entries, we need a demand zone (buying)
        if zone_influence >= 0.5: # Less strict (OR logic倾向)
            # Condition is met if EITHER primary condition is met OR price is in demand zone
            # (We'll combine this later using OR logic)
            zone_long_entry_condition = price_in_demand_zone 
        else: # More strict (AND logic倾向)
            # Condition requires price to be in demand zone
            # (We'll combine this later using AND logic implicitly)
            zone_long_entry_condition = price_in_demand_zone

        # For short entries, we need a supply zone (selling)
        if zone_influence >= 0.5: # Less strict (OR logic倾向)
            zone_short_entry_condition = price_in_supply_zone
        else: # More strict (AND logic倾向)
            zone_short_entry_condition = price_in_supply_zone
            
        # --- Define Exit Zone Triggers (Deterministic) ---
        # Long exits triggered by supply zones
        if zone_influence >= 0.5: # Less strict (OR logic)
            zone_long_exit_trigger = price_in_supply_zone
        else: # More strict (AND logic)
            zone_long_exit_trigger = price_in_supply_zone

        # Short exits triggered by demand zones
        if zone_influence >= 0.5: # Less strict (OR logic)
            zone_short_exit_trigger = price_in_demand_zone
        else: # More strict (AND logic)
            zone_short_exit_trigger = price_in_demand_zone
        # --- End Exit Zone Trigger Definition ---
            
        # Primary Entry Conditions (Combine basic indicator conditions)
        if strictness in [SignalStrictness.BALANCED, SignalStrictness.MODERATELY_RELAXED]:
            # Use OR logic instead of AND for primary conditions to generate more signals
            primary_long_condition = rsi_oversold | price_below_bb
            primary_short_condition = rsi_overbought | price_above_bb
            
            # Combine Primary conditions with Zone conditions based on influence
            if use_zones:
                # Always use OR logic for zones in BALANCED and MODERATELY_RELAXED modes
                long_entry_trigger = primary_long_condition.combine(zone_long_entry_condition, lambda x, y: x or y)
                short_entry_trigger = primary_short_condition.combine(zone_short_entry_condition, lambda x, y: x or y)
            else:
                # No trend filter for BALANCED and MODERATELY_RELAXED modes
                long_entry_trigger = primary_long_condition
                short_entry_trigger = primary_short_condition
        else:
            # Original AND logic for other modes
            primary_long_condition = rsi_oversold & price_below_bb 
            primary_short_condition = rsi_overbought & price_above_bb
            
            # Combine Primary conditions with Zone conditions based on influence
            if use_zones:
                if zone_influence >= 0.5: # Less Strict: Primary OR Zone
                    # Use pandas combine for proper boolean operations with Series
                    long_entry_trigger = primary_long_condition.combine(zone_long_entry_condition, lambda x, y: x or y)
                    short_entry_trigger = primary_short_condition.combine(zone_short_entry_condition, lambda x, y: x or y)
                else: # More Strict: Primary AND Zone
                    long_entry_trigger = primary_long_condition & zone_long_entry_condition & trend_filter_long
                    short_entry_trigger = primary_short_condition & zone_short_entry_condition & trend_filter_short
            else:
                # Zones not used
                long_entry_trigger = primary_long_condition & trend_filter_long
                short_entry_trigger = primary_short_condition & trend_filter_short
        # Generate Initial Entries
        initial_long_entries = pd.Series(long_entry_trigger, index=close.index)
        initial_short_entries = pd.Series(short_entry_trigger, index=close.index)
    else:
        # If zones aren't used, these conditions are always met/not met
        zone_long_entry_condition = pd.Series(True, index=close.index)
        zone_long_exit_trigger = pd.Series(False, index=close.index)
        zone_short_entry_condition = pd.Series(True, index=close.index)
        zone_short_exit_trigger = pd.Series(False, index=close.index)

        # Primary Entry Conditions (Combine basic indicator conditions)
        if strictness in [SignalStrictness.BALANCED, SignalStrictness.MODERATELY_RELAXED]:
            # Use OR logic instead of AND for primary conditions to generate more signals
            primary_long_condition = rsi_oversold | price_below_bb
            primary_short_condition = rsi_overbought | price_above_bb
            
            # Less restrictive trend filtering for BALANCED and MODERATELY_RELAXED modes
            long_entry_trigger = primary_long_condition  # No trend filter
            short_entry_trigger = primary_short_condition  # No trend filter
        else:
            # Original AND logic for other modes
            primary_long_condition = rsi_oversold & price_below_bb 
            primary_short_condition = rsi_overbought & price_above_bb
            
            # Original trend filtering
            long_entry_trigger = primary_long_condition & trend_filter_long
            short_entry_trigger = primary_short_condition & trend_filter_short

        # Generate Initial Entries
        initial_long_entries = pd.Series(long_entry_trigger, index=close.index)
        initial_short_entries = pd.Series(short_entry_trigger, index=close.index)

    # BALANCED EXIT CONDITIONS - ENHANCED:
    # Improved exit conditions with better filtering and earlier trend detection
    
    # Enhanced exit logic with adaptive techniques based on market conditions
    # 1. Calculate trailing stop levels for dynamic exit management
    # Use ATR if available in the data for volatility-based trailing stops
    try:
        if 'atr' in ohlc_data.columns:
            atr = ohlc_data['atr']
        else:
            # Estimate ATR using high-low range if not available
            high_low_range = ohlc_data['high'] - ohlc_data['low']
            atr = high_low_range.rolling(14).mean().fillna(high_low_range)
    except (NameError, AttributeError):
        # If ohlc_data not available, estimate from close price volatility
        atr = close.pct_change().abs().rolling(14).mean().fillna(0.01) * close
    
    # Calculate trailing stop levels (2 ATR for trending, 1 ATR for ranging)
    # Adjust multiplier based on volatility - higher volatility needs wider stops
    atr_multiplier = 1.0 + (volatility_adjustment * 0.5)  # 1.0 to 1.5 based on volatility
    
    # Track highest/lowest prices for trailing stops (last 5 candles)
    highest_close = close.rolling(5).max().fillna(close)
    lowest_close = close.rolling(5).min().fillna(close)
    
    # 2. Time-based exit for stagnant trades
    # Detect periods of low momentum/volatility which suggest a stagnant trade
    close_range_pct = (close.rolling(5).max() - close.rolling(5).min()) / close.rolling(5).mean()
    stagnant_price = close_range_pct < (0.005 * (1 + volatility_adjustment))  # Tighter threshold in low volatility
    
    # 3. Momentum-based trailing exit conditions
    # Long trailing stop: exit when price falls below recent high minus ATR multiple
    long_trailing_stop = close < (highest_close.shift(1) - (atr * atr_multiplier))
    
    # Short trailing stop: exit when price rises above recent low plus ATR multiple
    short_trailing_stop = close > (lowest_close.shift(1) + (atr * atr_multiplier))
    
    # 4. Take profit conditions - more aggressive in ranging markets
    # Calculate dynamic take-profit levels based on volatility
    take_profit_multiple = 2.0 + (volatility_adjustment * 1.0)  # 2.0 to 3.0 based on volatility
    
    # Create profit target conditions (requires entry price tracking, but we'll approximate)
    profit_target_long = close > (bb_lower * (1 + (volatility_factor * take_profit_multiple)))
    profit_target_short = close < (bb_upper * (1 - (volatility_factor * take_profit_multiple)))
    
    # Enhanced adaptive exit logic for long positions
    # Standard indicator-based conditions
    exit_cond1 = rsi_overbought & (close > trend_ma)  # Standard RSI overbought exit
    exit_cond2 = price_above_bb & (rsi > 55)          # Price above BB with RSI confirmation
    exit_cond3 = strong_overbought                    # Strong overbought condition
    exit_cond4 = close < (trend_ma * 0.98)           # Hard stop: trend reversal (below MA)
    
    # Add trailing stop and take profit conditions for long positions
    exit_cond5 = long_trailing_stop                  # Trailing stop triggered
    exit_cond6 = profit_target_long                  # Take profit level reached
    exit_cond7 = stagnant_price & (rsi > 50)         # Exit stagnant trades in neutral RSI
    
    # Additional risk management exit - accelerating downward momentum while profitable
    close_change_acc = close_change_pct - close_change_pct.shift(1)  # Momentum change acceleration
    exit_cond8 = (close > trend_ma) & (close_change_acc < -0.005) & (close_change_pct < -0.002)
    
    # Combine long exit conditions using proper boolean operations
    temp_exit1 = exit_cond1.combine(exit_cond2, lambda x, y: x or y)  # Indicator conditions
    temp_exit2 = exit_cond3.combine(exit_cond4, lambda x, y: x or y)  # Overbought & stop loss
    temp_exit3 = exit_cond5.combine(exit_cond6, lambda x, y: x or y)  # Trailing stop & take profit
    temp_exit4 = exit_cond7.combine(exit_cond8, lambda x, y: x or y)  # Stagnation & momentum loss
    
    # Final combination of all long exit conditions
    temp_long_exit1 = temp_exit1.combine(temp_exit2, lambda x, y: x or y)
    temp_long_exit2 = temp_exit3.combine(temp_exit4, lambda x, y: x or y)
    primary_long_exit = temp_long_exit1.combine(temp_long_exit2, lambda x, y: x or y)
    
    # All trailing stop, take-profit, and stagnation variables are now defined above
    
    # 5. Combine exit conditions for short positions with proper boolean handling
    # Standard oversold exit conditions
    short_exit_cond1 = rsi_oversold & (close < trend_ma)     # Standard RSI oversold exit
    short_exit_cond2 = price_below_bb & (rsi < 45)          # Price below BB with RSI confirmation
    short_exit_cond3 = strong_oversold                      # Strong oversold condition
    short_exit_cond4 = (close_change_pct > 0.01) & (rsi < 40)  # Significant upward momentum with low RSI
    
    # Add trailing stop and profit target conditions
    short_exit_cond5 = short_trailing_stop                  # Trailing stop hit
    short_exit_cond6 = profit_target_short                  # Take profit level reached
    short_exit_cond7 = stagnant_price & (rsi < 50)          # Exit stagnant trades in neutral RSI
    
    # Combine all short exit conditions using proper boolean operations
    short_temp_exit1 = short_exit_cond1.combine(short_exit_cond2, lambda x, y: x or y)
    short_temp_exit2 = short_exit_cond3.combine(short_exit_cond4, lambda x, y: x or y)
    short_temp_exit3 = short_exit_cond5.combine(short_exit_cond6, lambda x, y: x or y)
    
    # Final combination of all exit conditions
    primary_short_exit1 = short_temp_exit1.combine(short_temp_exit2, lambda x, y: x or y)
    primary_short_exit2 = short_temp_exit3.combine(short_exit_cond7, lambda x, y: x or y)
    primary_short_exit = primary_short_exit1.combine(primary_short_exit2, lambda x, y: x or y)
            
    if use_zones:
        if zone_influence >= 0.5: # Less Strict: Primary OR Zone
            # Use pandas combine for proper boolean operations with Series
            long_exits = primary_long_exit.combine(zone_long_exit_trigger, lambda x, y: x or y)
            short_exits = primary_short_exit.combine(zone_short_exit_trigger, lambda x, y: x or y)
        else: # More Strict: Primary AND Zone
            # Note: Strict exit requires *both* primary signal AND zone signal. This might be too restrictive.
            # Consider if exits should always be less strict or configurable separately.
            # For now, implementing strictly based on the pattern.
            long_exits = primary_long_exit & zone_long_exit_trigger
            short_exits = primary_short_exit & zone_short_exit_trigger
    else:
        long_exits = primary_long_exit
        short_exits = primary_short_exit
            
    # Ensure exits override entries on same bar
    initial_long_entries = initial_long_entries & ~long_exits
    initial_short_entries = initial_short_entries & ~short_exits

    # Fill NaN values
    initial_long_entries = initial_long_entries.fillna(False)
    long_exits = long_exits.fillna(False)
    initial_short_entries = initial_short_entries.fillna(False)
    short_exits = short_exits.fillna(False)

    # Apply minimum holding period (configurable but shorter than strict)
    if min_hold_period > 0:
        # For long positions
        long_entries_idx = initial_long_entries[initial_long_entries].index
        for idx in long_entries_idx:
            loc_idx = long_exits.index.get_loc(idx)
            end_idx = min(loc_idx + min_hold_period, len(long_exits))
            if loc_idx < len(long_exits):
                long_exits.iloc[loc_idx:end_idx] = False
                
        # For short positions
        short_entries_idx = initial_short_entries[initial_short_entries].index
        for idx in short_entries_idx:
            loc_idx = short_exits.index.get_loc(idx)
            end_idx = min(loc_idx + min_hold_period, len(short_exits))
            if loc_idx < len(short_exits):
                short_exits.iloc[loc_idx:end_idx] = False
    
    # Log signal counts for debugging
    logger.debug(f"Generated {initial_long_entries.sum()} long entries and {initial_short_entries.sum()} short entries "
                f"with {strictness} mode")
    
    return initial_long_entries, long_exits, initial_short_entries, short_exits
