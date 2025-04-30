#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced Signal Generation for Testing

This module contains simplified, more relaxed signal generation logic to ensure
sufficient trades during testing and evaluation of the regime-aware strategy.

Author: Max Kimball
Date: 2025-04-28
"""

import vectorbtpro as vbt
import pandas as pd
import numpy as np
import logging

# Setup logging
logger = logging.getLogger("test_signals")

def generate_test_edge_signals(
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
    trend_strict: bool = False,  # Less strict by default
    relaxed_mode: bool = True
) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Generates entry and exit signals with relaxed conditions for testing purposes.
    
    This version intentionally generates more trades to facilitate testing of the
    regime-aware parameter adaptation framework.
    
    Args:
        close: Series of closing prices
        rsi: Series of RSI values
        bb_upper: Series of Bollinger Band upper values
        bb_lower: Series of Bollinger Band lower values
        trend_ma: Series of trend moving average values
        price_in_demand_zone: Boolean Series indicating if price is in a demand zone
        price_in_supply_zone: Boolean Series indicating if price is in a supply zone
        rsi_lower_threshold: RSI threshold for oversold condition
        rsi_upper_threshold: RSI threshold for overbought condition
        use_zones: Whether to use zone filters
        trend_strict: Whether to strictly enforce trend filter
        relaxed_mode: Whether to use relaxed conditions for more trade generation

    Returns:
        tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
            Boolean Series for (long_entries, long_exits, short_entries, short_exits).
    """
    # 1. Calculate Basic Indicator Conditions
    rsi_oversold = rsi < rsi_lower_threshold
    rsi_overbought = rsi > rsi_upper_threshold
    price_below_bb = close < bb_lower
    price_above_bb = close > bb_upper
    
    # 2. Define Relaxed Trend Filters (allow more trades)
    trend_up = close > trend_ma
    trend_down = close < trend_ma
    
    # Use less strict trend filters in relaxed mode
    if relaxed_mode:
        trend_filter_long = pd.Series(True, index=close.index)  # Always True in relaxed mode
        trend_filter_short = pd.Series(True, index=close.index)  # Always True in relaxed mode
    else:
        trend_filter_long = trend_up if trend_strict else pd.Series(True, index=close.index)
        trend_filter_short = trend_down if trend_strict else pd.Series(True, index=close.index)

    # 3. Define Zone Filters/Triggers (if zones are used)
    # In relaxed mode, we'll use less restrictive zone conditions
    if use_zones and not relaxed_mode:
        zone_long_entry_condition = price_in_demand_zone
        zone_long_exit_trigger = price_in_supply_zone
        zone_short_entry_condition = price_in_supply_zone
        zone_short_exit_trigger = price_in_demand_zone
    else:
        # If zones aren't used or in relaxed mode, these conditions are always met
        zone_long_entry_condition = pd.Series(True, index=close.index)
        zone_long_exit_trigger = pd.Series(False, index=close.index)
        zone_short_entry_condition = pd.Series(True, index=close.index)
        zone_short_exit_trigger = pd.Series(False, index=close.index)

    # 4. Combine Conditions for Long Signals - MORE RELAXED
    # In relaxed mode, we only require one condition to be true
    if relaxed_mode:
        long_entries = (rsi_oversold | price_below_bb) & zone_long_entry_condition
    else:
        long_entries = ((rsi_oversold & trend_filter_long) | (price_below_bb & trend_filter_long)) & zone_long_entry_condition

    # 5. Combine Conditions for Short Signals - MORE RELAXED
    if relaxed_mode:
        short_entries = (rsi_overbought | price_above_bb) & zone_short_entry_condition
    else:
        short_entries = ((rsi_overbought & trend_filter_short) | (price_above_bb & trend_filter_short)) & zone_short_entry_condition

    # Exits are also more relaxed in relaxed mode
    if relaxed_mode:
        # In relaxed mode, just use overbought OR above upper band for long exits
        long_exits = rsi_overbought | price_above_bb | zone_long_exit_trigger
        # And oversold OR below lower band for short exits
        short_exits = rsi_oversold | price_below_bb | zone_short_exit_trigger
    else:
        # Standard exit logic from original signals.py
        long_exits = (rsi_overbought & price_above_bb) | zone_long_exit_trigger
        short_exits = (rsi_oversold & price_below_bb) | zone_short_exit_trigger

    # Ensure exits override entries on the same bar
    long_entries = long_entries & ~long_exits
    short_entries = short_entries & ~short_exits

    # Fill NaN values with False
    long_entries = long_entries.fillna(False)
    long_exits = long_exits.fillna(False)
    short_entries = short_entries.fillna(False)
    short_exits = short_exits.fillna(False)

    # In relaxed mode, no minimum holding period
    if not relaxed_mode:
        # Apply minimum holding period to prevent immediate exit after entry
        min_hold = 3
        long_entries_idx = long_entries[long_entries].index
        for idx in long_entries_idx:
            exit_idx = long_exits.index.get_loc(idx) + min_hold
            if exit_idx < len(long_exits):
                long_exits.iloc[exit_idx] = False  # Prevent exit for min_hold bars after entry
        
        short_entries_idx = short_entries[short_entries].index
        for idx in short_entries_idx:
            exit_idx = short_exits.index.get_loc(idx) + min_hold
            if exit_idx < len(short_exits):
                short_exits.iloc[exit_idx] = False
    
    # Generate some additional signals in relaxed mode
    if relaxed_mode:
        # Add RSI crossovers as additional signals
        rsi_mid = (rsi_lower_threshold + rsi_upper_threshold) / 2
        rsi_cross_up = rsi.vbt.crossed_above(rsi_mid)
        rsi_cross_down = rsi.vbt.crossed_below(rsi_mid)
        
        # Add crossover signals (but don't override existing signals)
        additional_long_entries = rsi_cross_up & ~long_entries & ~long_exits
        additional_short_entries = rsi_cross_down & ~short_entries & ~short_exits
        
        # Combine with existing signals
        long_entries = long_entries | additional_long_entries
        short_entries = short_entries | additional_short_entries
        
        # Log how many signals we have
        logger.info(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries in relaxed test mode")

    return long_entries, long_exits, short_entries, short_exits
