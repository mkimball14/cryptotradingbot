import vectorbtpro as vbt
import pandas as pd
import numpy as np

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
    volatility: pd.Series,
    trend_ma: pd.Series,
    rsi_entry_threshold: float,
    rsi_exit_threshold: float,
    volatility_threshold: float,
    trend_strict: bool = True # If True, only long when close > trend_ma
) -> tuple[pd.Series, pd.Series]:
    """
    Generates entry and exit signals for the Edge Multi-Factor strategy.

    Combines RSI, Bollinger Bands, Volatility, and Trend filters.

    Args:
        close (pd.Series): Closing prices.
        rsi (pd.Series): RSI values.
        bb_upper (pd.Series): Upper Bollinger Band values.
        bb_lower (pd.Series): Lower Bollinger Band values.
        volatility (pd.Series): Volatility indicator values.
        trend_ma (pd.Series): Trend Moving Average values (e.g., SMA 200).
        rsi_entry_threshold (float): RSI level below which entry is considered.
        rsi_exit_threshold (float): RSI level above which exit is considered.
        volatility_threshold (float): Volatility level above which trading is allowed.
        trend_strict (bool, optional): If True, strictly enforce price > trend_ma for longs. Defaults to True.

    Returns:
        tuple[pd.Series, pd.Series]: Boolean Series for long entries and long exits.
    """
    # 1. Calculate Individual Conditions
    rsi_entry_cond = rsi < rsi_entry_threshold
    rsi_exit_cond = rsi > rsi_exit_threshold
    bb_entry_cond = close < bb_lower # Price touches or below lower band
    bb_exit_cond = close > bb_upper  # Price touches or above upper band

    # 2. Apply Filters
    volatility_filter = volatility > volatility_threshold
    trend_filter = close > trend_ma if trend_strict else pd.Series(True, index=close.index) # Always True if not strict

    # Combine filters
    trade_allowed = volatility_filter & trend_filter

    # 3. Combine Conditions for Entry/Exit (Long Only for now)
    # Entry: RSI oversold AND price near/below lower BB AND filters allow
    entries = rsi_entry_cond & bb_entry_cond & trade_allowed
    # Exit: RSI overbought OR price near/above upper BB
    # (Exit conditions usually don't need the entry filters applied)
    exits = rsi_exit_cond | bb_exit_cond

    # Clean signals: Ensure exit happens after entry if signals overlap
    # entries = entries.vbt.signals.first(True)
    # exits = exits.vbt.signals.first(True)
    # Simple cleaning: remove entry on the same bar as exit
    entries = entries & ~exits

    # Fill NaNs introduced by indicators/filters before returning
    entries = entries.fillna(False)
    exits = exits.fillna(False)

    return entries, exits


# TODO:
# 1. Refine signal combination logic (consider timing, conflicting signals)
# 2. Integrate signals from S/D zones when implemented
# 3. Add short signal logic if needed
# 4. Add parameters for enabling/disabling specific signal components (RSI, BB, Vol, Trend)
# 5. Potentially add smoothing or confirmation logic (e.g., requiring condition over N bars)

print("Signal generation functions loaded.")
