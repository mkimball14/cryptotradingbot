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
@njit
def bbands_talib_wrapper(close, window, std_dev):
    # Map to TA-Lib's parameter names
    # Assuming nbdevup and nbdevdn are the same
    upper, middle, lower = vbt.talib('BBANDS').run(close, timeperiod=window, nbdevup=std_dev, nbdevdn=std_dev)
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
@njit
def rolling_volatility_nb(close, window):
    """Calculate rolling annualized volatility using Numba."""
    returns = np.diff(close) / close[:-1]
    # Need to handle the initial window size where rolling std is NaN
    rolling_std = np.full_like(close, np.nan, dtype=np.float_)
    if len(close) > window:
        for i in range(window, len(close)):
             # Calculate std dev on the *returns* slice
            rolling_std[i] = np.std(returns[i-window:i])
    # Annualize (assuming daily returns -> 252 trading days)
    # If using intraday, adjust sqrt factor (e.g., sqrt(252*X) where X is bars per day)
    # For now, let's not annualize here, do it in signals if needed.
    # annualized_vol = rolling_std * np.sqrt(252)
    return rolling_std

Volatility = vbt.IndicatorFactory(
    class_name="Volatility",
    short_name="volatility",
    input_names=["close"],
    param_names=["window"],
    output_names=["vol"]
).with_apply_func(
    rolling_volatility_nb,
    keep_pd=True,
    window=20 # Default window, will be overridden by params
)

# TODO:
# 1. Implement Supply/Demand Zone detection logic (likely in signals.py or zones.py)
# 2. Add Candlestick pattern recognition if needed (check vbt/pandas_ta)
# 3. Implement any other custom indicators required by the strategy

print("Indicator definitions loaded.")
