import numpy as np
import pandas as pd

def create_volatility_regime_indicator(
    price: pd.Series, 
    volatility_lookback: int = 20, 
    threshold_percentile: float = 20.0, 
    ratio_threshold: float = 0.8, 
    return_lookback: int = 10, 
    n_lookback_periods: int = 5,
    verbose: bool = False
) -> tuple:
    """
    Creates a volatility regime indicator that identifies periods of volatility expansion
    following volatility compression.
    
    Args:
        price (pd.Series): Time series of price data
        volatility_lookback (int): Lookback window for calculating volatility (standard deviation)
        threshold_percentile (float): Percentile threshold for identifying volatility compression (0-100)
        ratio_threshold (float): Ratio threshold below which volatility is considered compressed
        return_lookback (int): Lookback window for calculating returns
        n_lookback_periods (int): Number of lookback periods for longer-term volatility comparison
        verbose (bool): Whether to print diagnostic information
        
    Returns:
        tuple: (
            vol_expansion_signal (pd.Series): Boolean series indicating volatility expansion after compression,
            vol_ratio (pd.Series): Ratio of current volatility to recent volatility,
            vol_compressed (pd.Series): Boolean series indicating when volatility is compressed
        )
    """
    # Calculate returns and rolling volatility
    returns = price.pct_change(return_lookback).fillna(0)
    volatility = returns.rolling(window=volatility_lookback).std()
    
    # Calculate a longer-term volatility lookback for comparison
    long_vol_window = volatility_lookback * n_lookback_periods
    volatility_long = returns.rolling(window=long_vol_window).std()
    
    # Calculate the ratio of recent volatility to longer-term volatility
    # This identifies when current volatility is low compared to historical
    vol_ratio = (volatility / volatility_long).fillna(1.0)
    
    # Get the percentile threshold value for volatility ratio
    if threshold_percentile > 0:
        threshold_value = np.nanpercentile(vol_ratio, threshold_percentile)
        actual_ratio_threshold = min(threshold_value, ratio_threshold)
    else:
        actual_ratio_threshold = ratio_threshold
    
    if verbose:
        print(f"Volatility ratio min: {vol_ratio.min():.4f}, max: {vol_ratio.max():.4f}")
        print(f"Volatility ratio threshold: {actual_ratio_threshold:.4f}")
    
    # Identify volatility compression (volatility ratio below threshold)
    vol_compressed = vol_ratio < actual_ratio_threshold
    
    # Count periods of compression to ensure enough compression events
    n_compression_periods = vol_compressed.rolling(window=30).sum()
    
    # If no compression periods are found, reduce the threshold adaptively
    # to ensure some compression signals are detected
    if n_compression_periods.max() < 2:
        # Find a threshold that would give at least some compression events
        adaptive_threshold = np.nanpercentile(vol_ratio, min(threshold_percentile * 2, 40))
        vol_compressed = vol_ratio < adaptive_threshold
        
        if verbose:
            print(f"Adjusting threshold to {adaptive_threshold:.4f} to get some compression events")
    
    # Create signal: True when volatility is expanding (increasing) after compression
    # 1. Identify when vol_ratio is rising (current higher than previous)
    vol_ratio_rising = vol_ratio > vol_ratio.shift(1)
    
    # 2. Identify when compression just ended (was compressed in previous period)
    compression_just_ended = vol_compressed.shift(1) & ~vol_compressed
    
    # 3. Identify when we're near the end of compression (still compressed but ratio rising)
    near_end_of_compression = vol_compressed & vol_ratio_rising
    
    # 4. The signal is triggered when compression ends or is near ending with rising volatility
    vol_expansion_signal = compression_just_ended | near_end_of_compression
    
    # Handle NaN values
    vol_expansion_signal = vol_expansion_signal.fillna(False)
    vol_compressed = vol_compressed.fillna(False)
    
    return vol_expansion_signal, vol_ratio, vol_compressed


def create_volatility_percentile_indicator(
    price: pd.Series, 
    short_lookback: int = 10,
    long_lookback: int = 100,
    high_percentile: float = 80,
    low_percentile: float = 20,
    return_period: int = 1,
    ema_smoothing: bool = True,
    ema_span: int = 5
) -> tuple:
    """
    Creates a volatility percentile indicator that identifies high and low volatility regimes
    based on historical percentile rankings.
    
    Args:
        price (pd.Series): Time series of price data
        short_lookback (int): Lookback window for short-term volatility calculation
        long_lookback (int): Lookback window for long-term percentile comparison
        high_percentile (float): Percentile threshold to identify high volatility (0-100)
        low_percentile (float): Percentile threshold to identify low volatility (0-100)
        return_period (int): Period for calculating returns
        ema_smoothing (bool): Whether to apply EMA smoothing to volatility
        ema_span (int): EMA span parameter for smoothing
        
    Returns:
        tuple: (
            vol_percentile (pd.Series): Current volatility percentile (0-100),
            high_vol_regime (pd.Series): Boolean series indicating high volatility regime,
            low_vol_regime (pd.Series): Boolean series indicating low volatility regime,
            vol_value (pd.Series): The actual volatility value
        )
    """
    # Calculate returns
    returns = price.pct_change(return_period).fillna(0)
    
    # Calculate absolute returns for volatility estimation
    abs_returns = returns.abs()
    
    # Calculate short-term volatility (standard deviation of returns)
    volatility = abs_returns.rolling(window=short_lookback).std()
    
    # Apply exponential smoothing if requested
    if ema_smoothing:
        volatility = volatility.ewm(span=ema_span, adjust=False).mean()
    
    # Calculate rolling percentile over the long lookback period
    vol_percentile = volatility.rolling(window=long_lookback).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1] * 100
    )
    
    # Identify high and low volatility regimes
    high_vol_regime = vol_percentile > high_percentile
    low_vol_regime = vol_percentile < low_percentile
    
    # Handle NaN values
    high_vol_regime = high_vol_regime.fillna(False)
    low_vol_regime = low_vol_regime.fillna(True)  # Default to low vol when insufficient data
    
    return vol_percentile, high_vol_regime, low_vol_regime, volatility


def create_atr_volatility_bands(
    price: pd.Series,
    high: pd.Series = None,
    low: pd.Series = None,
    atr_period: int = 14,
    band_multiplier: float = 2.0,
    smoothing: int = 2
) -> tuple:
    """
    Creates Average True Range (ATR) volatility bands around price.
    
    If high and low series are not provided, the function uses the price series
    to approximate high and low values based on close-to-close ranges.
    
    Args:
        price (pd.Series): Time series of price data (typically close prices)
        high (pd.Series, optional): Time series of high prices
        low (pd.Series, optional): Time series of low prices
        atr_period (int): Period for ATR calculation
        band_multiplier (float): Multiplier for band width
        smoothing (int): Smoothing factor for ATR (1=simple, 2=Wilder's)
        
    Returns:
        tuple: (
            upper_band (pd.Series): Upper volatility band,
            lower_band (pd.Series): Lower volatility band,
            atr (pd.Series): Average True Range values
        )
    """
    # If high and low are not provided, approximate them from the price series
    if high is None or low is None:
        # Approximate high and low using daily volatility
        daily_range = price.pct_change().abs() * price
        high = price + daily_range / 2
        low = price - daily_range / 2
    
    # Calculate True Range
    tr1 = high - low                      # Current high-low range
    tr2 = (high - price.shift(1)).abs()   # Current high vs previous close
    tr3 = (low - price.shift(1)).abs()    # Current low vs previous close
    
    # Combine to get True Range
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR - Different calculation based on smoothing type
    if smoothing == 1:
        # Simple moving average
        atr = tr.rolling(window=atr_period).mean()
    else:
        # Wilder's smoothing
        atr = tr.ewm(alpha=1/atr_period, min_periods=atr_period, adjust=False).mean()
    
    # Calculate bands
    upper_band = price + (atr * band_multiplier)
    lower_band = price - (atr * band_multiplier)
    
    return upper_band, lower_band, atr


def calculate_implied_volatility_rank(
    volatility: pd.Series, 
    lookback_days: int = 252  # Typical trading days in a year
) -> pd.Series:
    """
    Calculates the implied volatility rank (IV rank) or its equivalent for any volatility series.
    
    The IV Rank shows the current volatility relative to its historical range over a lookback period.
    
    Args:
        volatility (pd.Series): Time series of volatility data
        lookback_days (int): Number of days to look back for high/low volatility
        
    Returns:
        pd.Series: IV Rank as a percentage (0-100)
    """
    # Calculate rolling min and max over the lookback period
    rolling_min = volatility.rolling(window=lookback_days).min()
    rolling_max = volatility.rolling(window=lookback_days).max()
    
    # Calculate IV Rank: (current - min) / (max - min) * 100
    iv_rank = (volatility - rolling_min) / (rolling_max - rolling_min) * 100
    
    # Handle cases where max=min (to avoid division by zero)
    iv_rank = iv_rank.replace([np.inf, -np.inf], np.nan).fillna(50)  # Default to mid-range
    
    # Ensure values are within 0-100 range
    iv_rank = np.maximum(0, np.minimum(100, iv_rank))
    
    return iv_rank


def detect_volatility_breakout(
    price: pd.Series,
    lookback: int = 20,
    threshold_multiple: float = 2.0,
    smoothing: bool = True,
    ema_span: int = 5
) -> tuple:
    """
    Detects breakouts in volatility that could signal significant price moves.
    
    Args:
        price (pd.Series): Time series of price data
        lookback (int): Lookback period for volatility calculation
        threshold_multiple (float): Multiple of average volatility to trigger breakout
        smoothing (bool): Whether to apply smoothing to volatility
        ema_span (int): EMA span for smoothing
        
    Returns:
        tuple: (
            vol_breakout (pd.Series): Boolean series indicating volatility breakouts,
            current_volatility (pd.Series): Current volatility values,
            volatility_threshold (pd.Series): Threshold levels that trigger breakouts
        )
    """
    # Calculate returns
    returns = price.pct_change().fillna(0)
    
    # Calculate current volatility (standard deviation of returns)
    current_volatility = returns.rolling(window=lookback).std()
    
    # Apply smoothing if requested
    if smoothing:
        current_volatility = current_volatility.ewm(span=ema_span, adjust=False).mean()
    
    # Calculate average volatility over a longer period
    avg_volatility = current_volatility.rolling(window=lookback*3).mean()
    
    # Calculate threshold for volatility breakout
    volatility_threshold = avg_volatility * threshold_multiple
    
    # Detect volatility breakout
    vol_breakout = current_volatility > volatility_threshold
    
    return vol_breakout, current_volatility, volatility_threshold


def calculate_historical_volatility(
    price: pd.Series,
    period: int = 30,
    annualize: bool = True,
    trading_periods_per_year: int = 365
) -> pd.Series:
    """
    Calculates historical volatility of a price series.
    
    Args:
        price (pd.Series): Time series of price data
        period (int): Lookback period for volatility calculation
        annualize (bool): Whether to annualize the volatility
        trading_periods_per_year (int): Number of trading periods in a year 
                                       (365 for daily crypto, 252 for stock market days)
        
    Returns:
        pd.Series: Historical volatility
    """
    # Calculate log returns
    log_returns = np.log(price / price.shift(1)).fillna(0)
    
    # Calculate standard deviation of log returns
    volatility = log_returns.rolling(window=period).std()
    
    # Annualize if requested
    if annualize:
        volatility = volatility * np.sqrt(trading_periods_per_year)
    
    return volatility 