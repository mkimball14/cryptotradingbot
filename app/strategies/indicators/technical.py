import pandas as pd
import numpy as np
from typing import Tuple

def calculate_rsi(data: pd.DataFrame, period: int = 14, price_col: str = 'close') -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        data: DataFrame with price data
        period: RSI period (default 14)
        price_col: Column name for price data
        
    Returns:
        Series containing RSI values
    """
    print(f"[DEBUG] Calculating RSI with period={period}, price_col={price_col}")
    print(f"[DEBUG] Input data columns: {data.columns.tolist()}")
    print(f"[DEBUG] Input data shape: {data.shape}")
    print(f"[DEBUG] First few rows of input data:\n{data.head()}")
    
    try:
        # Calculate price changes
        delta = data[price_col].diff()
        
        # Separate gains and losses
        gain = (delta.where(delta > 0, 0))
        loss = (-delta.where(delta < 0, 0))
        
        # Calculate average gain and loss using EMA
        avg_gain = gain.ewm(span=period, adjust=False).mean()
        avg_loss = loss.ewm(span=period, adjust=False).mean()
        
        # Calculate RS and RSI, handling division by zero
        rs = avg_gain / avg_loss.replace(0, float('inf'))
        rsi = 100 - (100 / (1 + rs))
        
        # Handle edge cases
        rsi = rsi.replace([np.inf, -np.inf], [100, 0])
        
        print(f"[DEBUG] RSI calculation completed. First few values:\n{rsi.head()}")
        return rsi
        
    except Exception as e:
        print(f"Error calculating RSI: {e}")
        print(f"[DEBUG] Exception details:", e.__class__.__name__, str(e))
        import traceback
        print(f"[DEBUG] Traceback:\n{traceback.format_exc()}")
        return pd.Series(index=data.index)

def calculate_ma(data: pd.DataFrame, period: int = 20, price_col: str = 'close') -> pd.Series:
    """
    Calculate Moving Average.
    
    Args:
        data: DataFrame with price data
        period: MA period
        price_col: Column name for price data
        
    Returns:
        Series containing MA values
    """
    return data[price_col].rolling(window=period).mean()

def calculate_atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range (ATR).
    
    Args:
        data: DataFrame with OHLC data
        period: ATR period (default 14)
        
    Returns:
        Series containing ATR values
    """
    high = data['high']
    low = data['low']
    close = data['close']
    
    # Calculate True Range
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR
    atr = tr.rolling(window=period).mean()
    
    return atr

def detect_regime(data: pd.DataFrame, 
                 ma_period: int = 20,
                 atr_period: int = 14,
                 slope_period: int = 5,
                 volatility_factor: float = 1.5) -> Tuple[pd.Series, pd.Series]:
    """
    Detect market regime using MA slope and ATR.
    
    Args:
        data: DataFrame with OHLC data
        ma_period: Period for moving average
        atr_period: Period for ATR calculation
        slope_period: Period for calculating MA slope
        volatility_factor: Multiplier for ATR to determine high volatility
        
    Returns:
        Tuple of (regime Series, volatility Series)
        Regime values: "uptrend", "downtrend", "sideways"
        Volatility values: "normal", "high"
    """
    # Calculate indicators
    ma = calculate_ma(data, period=ma_period)
    atr = calculate_atr(data, period=atr_period)
    
    # Calculate MA slope
    ma_slope = ma.diff(periods=slope_period) / slope_period
    
    # Initialize regime and volatility series
    regime = pd.Series(index=data.index, data="sideways")
    volatility = pd.Series(index=data.index, data="normal")
    
    # Detect regime based on MA slope
    regime[ma_slope > 0] = "uptrend"
    regime[ma_slope < 0] = "downtrend"
    
    # Detect high volatility periods
    avg_atr = atr.rolling(window=atr_period*2).mean()
    volatility[atr > avg_atr * volatility_factor] = "high"
    
    return regime, volatility

def calculate_adx(data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculate Average Directional Index (ADX), +DI, -DI.
    Requires the pandas_ta library.

    Args:
        data: DataFrame with high, low, close columns.
        period: ADX period (default 14).

    Returns:
        DataFrame with ADX, DMP (+DI), DMN (-DI) columns, prefixed with period.
        Example: ADX_14, DMP_14, DMN_14
    """
    try:
        import pandas_ta as ta
        # Ensure columns are lowercase for pandas_ta
        data_lower = data.copy()
        data_lower.columns = [col.lower() for col in data_lower.columns]
        
        if not all(col in data_lower.columns for col in ['high', 'low', 'close']):
            raise ValueError("Data must contain 'high', 'low', 'close' columns for ADX calculation.")

        adx_df = ta.adx(data_lower['high'], data_lower['low'], data_lower['close'], length=period)
        if adx_df is None or adx_df.empty:
            print("Warning: pandas_ta.adx returned empty DataFrame.")
            # Return empty DataFrame with expected columns if calculation fails
            cols = [f'ADX_{period}', f'DMP_{period}', f'DMN_{period}']
            return pd.DataFrame(index=data.index, columns=cols)
            
        # Rename columns to be more descriptive and include period
        adx_df.columns = [f'{col.replace("+", "P").replace("-", "N")}_{period}' for col in adx_df.columns]
        return adx_df

    except ImportError:
        print("Error: pandas_ta library is required for ADX calculation. Please install it.")
        # Return empty DataFrame with expected columns if import fails
        cols = [f'ADX_{period}', f'DMP_{period}', f'DMN_{period}']
        return pd.DataFrame(index=data.index, columns=cols)
    except Exception as e:
        print(f"Error calculating ADX: {e}")
        cols = [f'ADX_{period}', f'DMP_{period}', f'DMN_{period}']
        return pd.DataFrame(index=data.index, columns=cols)

def calculate_bbands(data: pd.DataFrame, period: int = 20, std_dev: float = 2.0, price_col: str = 'close') -> pd.DataFrame:
    """
    Calculate Bollinger Bands (BBands).
    Requires the pandas_ta library.

    Args:
        data: DataFrame with price data.
        period: BBands period (default 20).
        std_dev: Standard deviation multiplier (default 2.0).
        price_col: Column name for price data (default 'close').

    Returns:
        DataFrame with Lower Band (BBL), Mid Band (BBM), Upper Band (BBU),
        Bandwidth (BBB), and Band Percent (BBP) columns, prefixed with period and std dev.
        Example: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0, BBB_20_2.0, BBP_20_2.0
    """
    try:
        import pandas_ta as ta
        print(f"[DEBUG] Calculating BBands with period={period}, std_dev={std_dev}, price_col={price_col}")
        print(f"[DEBUG] Input data columns: {data.columns.tolist()}")
        print(f"[DEBUG] Input data shape: {data.shape}")
        print(f"[DEBUG] First few rows of input data:\n{data.head()}")
        
        # Calculate BBands manually to ensure correct column names
        ma = data[price_col].rolling(window=period).mean()
        std = data[price_col].rolling(window=period).std()
        
        bbands_df = pd.DataFrame(index=data.index)
        bbands_df[f'BBL_{period}_{std_dev}'] = ma - (std * std_dev)
        bbands_df[f'BBM_{period}_{std_dev}'] = ma
        bbands_df[f'BBU_{period}_{std_dev}'] = ma + (std * std_dev)
        
        # Calculate additional metrics
        bb_range = bbands_df[f'BBU_{period}_{std_dev}'] - bbands_df[f'BBL_{period}_{std_dev}']
        bbands_df[f'BBB_{period}_{std_dev}'] = bb_range / bbands_df[f'BBM_{period}_{std_dev}']
        bbands_df[f'BBP_{period}_{std_dev}'] = (data[price_col] - bbands_df[f'BBL_{period}_{std_dev}']) / bb_range
        
        print(f"[DEBUG] BBands calculation completed. Columns: {bbands_df.columns.tolist()}")
        print(f"[DEBUG] First few rows of output:\n{bbands_df.head()}")
        return bbands_df

    except Exception as e:
        print(f"Error calculating BBands: {e}")
        print(f"[DEBUG] Exception details:", e.__class__.__name__, str(e))
        import traceback
        print(f"[DEBUG] Traceback:\n{traceback.format_exc()}")
        cols = [f'BBL_{period}_{std_dev}', f'BBM_{period}_{std_dev}', f'BBU_{period}_{std_dev}', 
                f'BBB_{period}_{std_dev}', f'BBP_{period}_{std_dev}']
        return pd.DataFrame(index=data.index, columns=cols) 