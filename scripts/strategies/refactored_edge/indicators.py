import vectorbtpro as vbt
import numpy as np
import pandas as pd
from numba import njit

# ==============================================================================
# Indicator Definitions using vectorbtpro and TA-Lib
# ==============================================================================

# --- Standard TA-Lib Indicators via vbt.IndicatorFactory ---

# Relative Strength Index (RSI)
RSI = vbt.IndicatorFactory(
    class_name="RSI",
    short_name="rsi",
    input_names=["close"],
    param_names=["window"],
    output_names=["rsi"]
).from_talib("RSI")

# Bollinger Bands (BBands)
# Modified to accept window and std_dev for consistency with typical vbt usage
def bbands_talib_wrapper(close, window, std_dev):
    """
    Numba-compatible wrapper for TA-Lib BBANDS.

    Args:
        close (np.ndarray or pd.Series): Closing prices.
        window (int): Rolling window size.
        std_dev (float): Number of standard deviations for bands.

    Returns:
        tuple: (upper, middle, lower) band arrays.
    """
    # Ensure input is a NumPy array
    if hasattr(close, "values"):
        close_np = close.values
    else:
        close_np = close
    # Call TA-Lib BBANDS function directly via vbt.talib
    # It returns an object, not a tuple directly
    bbands_result = vbt.talib('BBANDS').run(
        close_np,
        timeperiod=window,
        nbdevup=std_dev,
        nbdevdn=std_dev,
        matype=0 # SMA
    )
    # Access the output bands from the result object
    upper = bbands_result.upperband
    middle = bbands_result.middleband
    lower = bbands_result.lowerband

    # Return the results as a tuple expected by vbt.IndicatorFactory
    return upper, middle, lower

BBANDS = vbt.IndicatorFactory(
    class_name="BBANDS",
    short_name="bbands",
    input_names=["close"],
    param_names=["window", "std_dev"], # Use consistent names
    output_names=["upper", "middle", "lower"] # Use more intuitive names
).with_apply_func(bbands_talib_wrapper, keep_pd=True) # Pass window and std_dev

# Moving Average Convergence Divergence (MACD)
# Note: TA-Lib MACD requires fastperiod, slowperiod, signalperiod
MACD = vbt.IndicatorFactory(
    class_name="MACD",
    short_name="macd",
    input_names=["close"],
    param_names=["fast_period", "slow_period", "signal_period"],
    output_names=["macd", "signal", "hist"]
).from_talib("MACD")

# Average True Range (ATR)
ATR = vbt.IndicatorFactory(
    class_name="ATR",
    short_name="atr",
    input_names=["high", "low", "close"],
    param_names=["window"],
    output_names=["atr"]
).from_talib("ATR")

# Average Directional Movement Index (ADX)
ADX = vbt.IndicatorFactory(
    class_name="ADX",
    short_name="adx",
    input_names=["high", "low", "close"],
    param_names=["window"],
    output_names=["adx"]
).from_talib("ADX")

# Simple Moving Average (SMA)
SMA = vbt.IndicatorFactory(
    class_name="SMA",
    short_name="sma",
    input_names=["close"],
    param_names=["window"],
    output_names=["sma"]
).from_talib("SMA")

# ==============================================================================
# Custom Indicator Definitions
# ==============================================================================

# --- Volatility Indicator ---
def calculate_volatility(close, timeperiod):
    """Calculates rolling standard deviation of percentage returns."""
    returns = close.pct_change()
    timeperiod = int(timeperiod)
    volatility = returns.rolling(window=timeperiod).std() * np.sqrt(timeperiod) # Annualized Std Dev
    return volatility

Volatility = vbt.IndicatorFactory(
    class_name="Volatility",
    short_name="volatility",
    input_names=["close"],
    param_names=["timeperiod"],
    output_names=["vol"]
).with_apply_func(
    calculate_volatility,
    keep_pd=True,
    timeperiod=20 # Default window, will be overridden by params
)

# TODO:
# 1. Implement Supply/Demand Zone detection logic (likely in signals.py or zones.py)
# 2. Add Candlestick pattern recognition if needed (check vbt/pandas_ta)
# 3. Implement any other custom indicators required by the strategy

print("Indicator definitions loaded.")
