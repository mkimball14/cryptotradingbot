import vectorbtpro as vbt
import pandas as pd
import numpy as np

# Local imports (assuming config might be useful here eventually)
# from .config import EdgeConfig # Import if config needed directly

# ==============================================================================
# Signal Generation Functions
# ==============================================================================

# --- RSI Signals ---
def generate_rsi_signals(rsi: pd.Series, entry_threshold: float, exit_threshold: float) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Generate signals based on RSI crossing entry/exit thresholds.

    Args:
        rsi (pd.Series): RSI indicator values.
        entry_threshold (float): RSI level for long entry (crossed below) and short exit.
        exit_threshold (float): RSI level for long exit (crossed above) and short entry.

    Returns:
        tuple[pd.Series, pd.Series, pd.Series, pd.Series]: 
            Boolean Series for (long_entries, long_exits, short_entries, short_exits).
    """
    # Long entry when RSI crosses below the entry threshold
    long_entries = rsi.vbt.crossed_below(entry_threshold)
    # Long exit when RSI crosses above the exit threshold
    long_exits = rsi.vbt.crossed_above(exit_threshold)
    
    # Short entry when RSI crosses above the exit threshold
    short_entries = rsi.vbt.crossed_above(exit_threshold)
    # Short exit when RSI crosses below the entry threshold
    short_exits = rsi.vbt.crossed_below(entry_threshold)
    
    return long_entries, long_exits, short_entries, short_exits

# --- Bollinger Bands Signals ---
def generate_bbands_signals(close: pd.Series, upper_band: pd.Series, lower_band: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Generate signals based on price crossing Bollinger Bands.

    Args:
        close (pd.Series): Closing prices.
        upper_band (pd.Series): Upper Bollinger Band values.
        lower_band (pd.Series): Lower Bollinger Band values.

    Returns:
        tuple[pd.Series, pd.Series, pd.Series, pd.Series]: 
            Boolean Series for (long_entries, long_exits, short_entries, short_exits).
    """
    # Long entry when close crosses below the lower band (reversal indication)
    long_entries = close.vbt.crossed_below(lower_band)
    # Long exit when close crosses above the upper band (potential overbought)
    long_exits = close.vbt.crossed_above(upper_band)
    
    # Short entry when close crosses above the upper band
    short_entries = close.vbt.crossed_above(upper_band)
    # Short exit when close crosses below the lower band
    short_exits = close.vbt.crossed_below(lower_band)
    
    return long_entries, long_exits, short_entries, short_exits

# --- MACD Signals ---
def generate_macd_signals(macd_line: pd.Series, signal_line: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Generate signals based on MACD line crossing the signal line.

    Args:
        macd_line (pd.Series): MACD line values.
        signal_line (pd.Series): MACD signal line values.

    Returns:
        tuple[pd.Series, pd.Series, pd.Series, pd.Series]: 
            Boolean Series for (long_entries, long_exits, short_entries, short_exits).
    """
    # Long entry when MACD crosses above the signal line
    long_entries = macd_line.vbt.crossed_above(signal_line)
    # Long exit when MACD crosses below the signal line
    long_exits = macd_line.vbt.crossed_below(signal_line)
    
    # Short entry when MACD crosses below the signal line
    short_entries = macd_line.vbt.crossed_below(signal_line)
    # Short exit when MACD crosses above the signal line
    short_exits = macd_line.vbt.crossed_above(signal_line)

    return long_entries, long_exits, short_entries, short_exits

# --- SMA Crossover Signals ---
def generate_sma_crossover_signals(sma_fast: pd.Series, sma_slow: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Generate signals based on a fast SMA crossing a slow SMA.

    Args:
        sma_fast (pd.Series): Fast SMA values.
        sma_slow (pd.Series): Slow SMA values.

    Returns:
        tuple[pd.Series, pd.Series]: Boolean Series for long entries and exits.
    """
    # Long entry when fast SMA crosses above slow SMA (golden cross)
    entries = sma_fast.vbt.crossed_above(sma_slow)
    # Long exit when fast SMA crosses below slow SMA (death cross)
    exits = sma_fast.vbt.crossed_below(sma_slow)
    # For SMA crossover, long exits are short entries and vice-versa
    # short_entries = exits.copy()
    # short_exits = entries.copy()
    return entries, exits

# --- Edge Multi-Factor Strategy Signals ---
def generate_edge_signals(
    close: pd.Series,
    rsi: pd.Series,
    bb_upper: pd.Series,
    bb_lower: pd.Series,
    trend_ma: pd.Series,
    price_in_demand_zone: pd.Series, # Expects boolean series 
    price_in_supply_zone: pd.Series, # Expects boolean series
    rsi_lower_threshold: float, 
    rsi_upper_threshold: float,  
    use_zones: bool,            
    trend_strict: bool = True
) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Generates entry and exit signals for the Edge Multi-Factor strategy.

    NOTE: Removed 'volatility_ok' condition from short_entries logic (was undefined and unused).

    Combines RSI, Bollinger Bands, Trend filters, and optionally Supply/Demand zones.

    Args:
        close (pd.Series): Closing prices.
        rsi (pd.Series): RSI values.
        bb_upper (pd.Series): Upper Bollinger Band values.
        bb_lower (pd.Series): Lower Bollinger Band values.
        trend_ma (pd.Series): Trend-defining moving average values.
        price_in_demand_zone (pd.Series): Boolean series indicating price is near/in a demand zone.
        price_in_supply_zone (pd.Series): Boolean series indicating price is near/in a supply zone.
        rsi_lower_threshold (float): RSI level below which long entry is considered (oversold).
        rsi_upper_threshold (float): RSI level above which long exit is considered (overbought).
        use_zones (bool): Whether to incorporate S/D zone signals into the logic.
        trend_strict (bool): If True, require close > trend_ma for longs, close < trend_ma for shorts.

    Returns:
        tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
            Boolean Series for (long_entries, long_exits, short_entries, short_exits).
    """
    # 1. Calculate Base Indicator Conditions
    rsi_oversold = rsi < rsi_lower_threshold
    rsi_overbought = rsi > rsi_upper_threshold
    price_below_bb = close < bb_lower
    price_above_bb = close > bb_upper

    # 2. Define Trend Filters
    trend_filter_long = close > trend_ma if trend_strict else pd.Series(True, index=close.index)
    trend_filter_short = close < trend_ma if trend_strict else pd.Series(True, index=close.index)

    # 3. Define Zone Filters/Triggers (if zones are used)
    if use_zones:
        # Refined Logic: Require entry within the 'correct' zone
        zone_long_entry_condition = price_in_demand_zone
        zone_long_exit_trigger = price_in_supply_zone
        zone_short_entry_condition = price_in_supply_zone
        zone_short_exit_trigger = price_in_demand_zone
    else:
        # If zones aren't used, these conditions are always met (True for entry, False for exit)
        zone_long_entry_condition = pd.Series(True, index=close.index)
        zone_long_exit_trigger = pd.Series(False, index=close.index)
        zone_short_entry_condition = pd.Series(True, index=close.index)
        zone_short_exit_trigger = pd.Series(False, index=close.index)

    # 4. Combine Conditions for Long Signals
    long_entries = (
        ((rsi_oversold & trend_filter_long) | (price_below_bb & trend_filter_long)) & zone_long_entry_condition
    )

    # 5. Combine Conditions for Short Signals
    short_entries = (
        ((rsi_overbought & trend_filter_short) | (price_above_bb & trend_filter_short)) & 
        zone_short_entry_condition  # Removed volatility_ok, which was undefined and unused
    )
    # Print summary for debugging
    # print(f"DEBUG: long_entries.sum(): {long_entries.sum()}, short_entries.sum(): {short_entries.sum()}")

    # Combine base exit condition OR zone exit trigger
    long_exits = (
        (rsi_overbought & price_above_bb) |  # Stricter: both must be true
        zone_long_exit_trigger                # Or zone exit
    )

    # Combine base exit condition OR zone exit trigger
    short_exits = (
        (rsi_oversold & price_below_bb) |    # Stricter: both must be true
        zone_short_exit_trigger               # Or zone exit
    )

    # Ensure exits override entries on the same bar
    long_entries = long_entries & ~long_exits
    short_entries = short_entries & ~short_exits

    long_entries = long_entries.fillna(False)
    long_exits = long_exits.fillna(False)
    short_entries = short_entries.fillna(False)
    short_exits = short_exits.fillna(False)

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

    return long_entries, long_exits, short_entries, short_exits

# Reason: Stricter exits and a minimum holding period should reduce overtrading and filter out whipsaw losses. Documented and explained for clarity.


# TODO:
# 1. Refine signal combination logic (consider timing, conflicting signals)
# 2. Integrate signals from S/D zones when implemented -> DONE
# 3. Add short signal logic if needed -> DONE
# 4. Add parameters for enabling/disabling specific signal components (RSI, BB, Trend, Zones)
# 5. Potentially add smoothing or confirmation logic (e.g., requiring condition over N bars)
