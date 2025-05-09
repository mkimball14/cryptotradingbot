import pandas as pd
import numpy as np
import vectorbtpro as vbt
import talib
from pydantic import ValidationError
import logging

from .config import EdgeConfig 
from .zones import find_pivot_zones, add_zone_signals
from .enhanced_indicators import add_pattern_recognition, add_volatility_indicators

logger = logging.getLogger(__name__)


def validate_ohlc_columns(df: pd.DataFrame):
    """Validate that the dataframe contains OHLC columns in either uppercase or lowercase format.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        tuple: (column_format, column_map)
            column_format: 'upper' or 'lower' depending on which format was found
            column_map: dictionary mapping standardized column names to actual column names
        
    Raises:
        ValueError: If the dataframe is missing required OHLC columns
    """
    # Check for required columns in both uppercase and lowercase forms
    upper_required = ['Open', 'High', 'Low', 'Close']
    lower_required = ['open', 'high', 'low', 'close']
    
    # Check for uppercase columns
    upper_missing = [col for col in upper_required if col not in df.columns]
    upper_has_all = len(upper_missing) == 0
    
    # Check for lowercase columns
    lower_missing = [col for col in lower_required if col not in df.columns]
    lower_has_all = len(lower_missing) == 0
    
    # If neither format has all required columns, we have a problem
    if not (upper_has_all or lower_has_all):
        # Choose which format had more columns to provide a more helpful error message
        if len(upper_missing) <= len(lower_missing):
            missing = upper_missing
            format_tried = "uppercase"
        else:
            missing = lower_missing
            format_tried = "lowercase"
            
        raise ValueError(f"Input DataFrame missing required OHLC columns (tried {format_tried}): {missing}")
    
    # Determine which format was found and create a mapping
    if upper_has_all:
        column_format = 'upper'
        column_map = {
            'Open': 'Open', 
            'High': 'High', 
            'Low': 'Low', 
            'Close': 'Close'
        }
    else:  # lower_has_all must be True at this point
        column_format = 'lower'
        column_map = {
            'Open': 'open', 
            'High': 'high', 
            'Low': 'low', 
            'Close': 'close'
        }
    
    return column_format, column_map


def add_adx(ohlc_data: pd.DataFrame, window: int = 14, column_map: dict = None) -> pd.DataFrame:
    """
    Calculate Average Directional Index (ADX) and Directional Indicators (DI).
    
    Args:
        ohlc_data: DataFrame with OHLC data
        window: Period for ADX calculation (default: 14)
        column_map: Dictionary mapping standardized column names to actual column names
        
    Returns:
        DataFrame with ADX, +DI, and -DI indicators
    """
    try:
        if column_map is None:
            # Try to detect column format
            try:
                _, column_map = validate_ohlc_columns(ohlc_data)
            except ValueError as e:
                logger.error(f"OHLC column validation failed in add_adx: {e}")
                # Fallback to lowercase columns
                column_map = {
                    'Open': 'open', 
                    'High': 'high', 
                    'Low': 'low', 
                    'Close': 'close'
                }
        
        # Use the column map to get the correct column names
        high = ohlc_data[column_map['High']].copy()
        low = ohlc_data[column_map['Low']].copy()
        close = ohlc_data[column_map['Close']].copy()
        
        # Create result DataFrame
        result = pd.DataFrame(index=ohlc_data.index)
        
        # Calculate ADX and directional indicators using talib
        result['adx'] = talib.ADX(high, low, close, timeperiod=window)
        result['plus_di'] = talib.PLUS_DI(high, low, close, timeperiod=window)
        result['minus_di'] = talib.MINUS_DI(high, low, close, timeperiod=window)
        
        # Fill NaN values that occur at the beginning due to the window
        result = result.bfill()
        
        # Final check for any remaining NaN values
        if result.isnull().any().any():
            # If still have NaNs after bfill, use forward fill
            result = result.ffill()
            # If still have NaNs (beginning of data), fill with default values
            result = result.fillna({
                'adx': 25.0,        # Default to threshold between trending/ranging
                'plus_di': 20.0,    # Default middle value
                'minus_di': 20.0    # Default middle value
            })
        
        logger.debug(f"ADX calculation successful with window={window}")
        return result
        
    except Exception as e:
        logger.error(f"Error calculating ADX: {e}", exc_info=True)
        # Return empty DataFrame with default values
        result = pd.DataFrame(index=ohlc_data.index)
        result['adx'] = 25.0        # Default to threshold between trending/ranging
        result['plus_di'] = 20.0    # Default middle value
        result['minus_di'] = 20.0   # Default middle value
        return result


def add_indicators(ohlc_data: pd.DataFrame, config: EdgeConfig):
    """Add technical indicators to OHLC data based on the provided configuration.
    
    Handles both uppercase and lowercase OHLC column formats.
    
    Args:
        ohlc_data: DataFrame with OHLC data
        config: Configuration with indicator parameters
        
    Returns:
        DataFrame with added indicators or None if validation fails
    """
    try:
        column_format, column_map = validate_ohlc_columns(ohlc_data)
        logger.debug(f"Using {column_format}case OHLC columns")
    except ValueError as e:
        logger.error(f"OHLC column validation failed: {e}")
        return None

    # Use the column map to get the correct column names
    close = ohlc_data[column_map['Close']].copy()
    high = ohlc_data[column_map['High']].copy()
    low = ohlc_data[column_map['Low']].copy()

    indicators_df = pd.DataFrame(index=ohlc_data.index)

    try:
        indicators_df['rsi'] = vbt.RSI.run(close, window=config.rsi_window).rsi

        bbands = vbt.BBANDS.run(close, window=config.bb_window, alpha=config.bb_std_dev)
        indicators_df['bb_upper'] = bbands.upper
        indicators_df['bb_lower'] = bbands.lower
        indicators_df['bb_width'] = bbands.bandwidth 

        indicators_df['trend_ma'] = vbt.MA.run(close, window=config.trend_ma_window).ma

        indicators_df['atr_stops'] = talib.ATR(high, low, close, timeperiod=config.atr_window)
        indicators_df['atr'] = indicators_df['atr_stops'].copy()  # Add atr column for regime detection
        
        # Add ADX and Directional Indicators for regime detection (critical for advanced regime detection)
        adx_window = getattr(config, 'adx_window', 14)  # Default to 14 if not specified
        adx_result = add_adx(ohlc_data, adx_window, column_map=column_map)
        indicators_df['adx'] = adx_result['adx']
        indicators_df['plus_di'] = adx_result['plus_di']
        indicators_df['minus_di'] = adx_result['minus_di']
        
        # Log indicator values for debugging
        logger.debug(f"ADX calculation successful: range [{indicators_df['adx'].min():.1f} - {indicators_df['adx'].max():.1f}]")
        logger.debug(f"PLUS_DI calculation successful: range [{indicators_df['plus_di'].min():.1f} - {indicators_df['plus_di'].max():.1f}]")
        logger.debug(f"MINUS_DI calculation successful: range [{indicators_df['minus_di'].min():.1f} - {indicators_df['minus_di'].max():.1f}]")
        
        # Get atr_window_sizing with proper fallback handling using getattr
        atr_window_sizing = getattr(config, 'atr_window_sizing', config.atr_window)
        if atr_window_sizing != config.atr_window:
            logger.debug(f"Using custom atr_window_sizing={atr_window_sizing} (different from atr_window={config.atr_window})")
        else:
            logger.debug(f"Using atr_window_sizing={atr_window_sizing} (same as atr_window)")
            
        indicators_df['atr_sizing'] = talib.ATR(high, low, close, timeperiod=atr_window_sizing)

    except Exception as e:
        logger.error(f"Error calculating standard indicators: {e}", exc_info=True)
        return None

    # Check for enhanced regime detection with proper fallback handling
    use_enhanced_regimes = getattr(config, 'use_enhanced_regimes', False)
    logger.debug(f"Enhanced regime detection {'enabled' if use_enhanced_regimes else 'disabled'} (use_enhanced_regimes={use_enhanced_regimes})")
    
    # Add enhanced regime detection indicators if enabled
    if use_enhanced_regimes:
        try:
            logger.debug("Adding enhanced regime detection indicators...")
            
            # Add pattern recognition indicators
            pattern_min_strength = getattr(config, 'pattern_min_strength', 60)
            pattern_df = add_pattern_recognition(ohlc_data, min_strength=pattern_min_strength)
            
            # Extract only the pattern columns we need for regime detection
            pattern_columns = ['pattern_signal', 'pattern_strength', 'pattern_bullish', 'pattern_bearish']
            for col in pattern_columns:
                if col in pattern_df.columns:
                    indicators_df[col] = pattern_df[col]
            
            # Add volatility indicators (VHF, Choppiness Index)
            volatility_df = add_volatility_indicators(ohlc_data)
            
            # Extract only the volatility columns we need for regime detection
            volatility_columns = ['vhf', 'choppiness']
            for col in volatility_columns:
                if col in volatility_df.columns:
                    indicators_df[col] = volatility_df[col]
            
            logger.debug(f"Enhanced regime indicators added successfully. Columns: {volatility_columns + pattern_columns}")
        except Exception as e:
            logger.error(f"Error adding enhanced regime indicators: {e}", exc_info=True)
            logger.warning("Proceeding without enhanced regime detection indicators")
    
    # Check for use_zones with proper fallback handling using getattr
    use_zones = getattr(config, 'use_zones', False)
    logger.debug(f"Supply/Demand zone analysis {'enabled' if use_zones else 'disabled'} (use_zones={use_zones})")
    
    if use_zones:
        try:
            logger.debug("Calculating S/D zones...")
            # Check for required zone parameters and use safe defaults if missing
            pivot_lookback = getattr(config, 'pivot_lookback', 10)
            pivot_prominence = getattr(config, 'pivot_prominence', 0.01)
            zone_merge_proximity = getattr(config, 'zone_merge_proximity', 0.005)
            min_zone_width_candles = getattr(config, 'min_zone_width_candles', 5)
            min_zone_strength = getattr(config, 'min_zone_strength', 2)
            zone_extend_candles = getattr(config, 'zone_extend_candles', 50)
            
            zones_df = find_pivot_zones(
                close=close,
                high=high,
                low=low,
                pivot_lookback=pivot_lookback,
                pivot_prominence=pivot_prominence,
                zone_merge_proximity=zone_merge_proximity,
                min_zone_width_candles=min_zone_width_candles,
                min_zone_strength=min_zone_strength,
                zone_extend_candles=zone_extend_candles
            )
            logger.debug(f"Found {len(zones_df)} zones.")

            if not zones_df.empty:
                logger.debug("Adding zone signals...")
                zone_signals_df = add_zone_signals(
                    close=close,
                    zones_df=zones_df,
                    zone_proximity_pct=config.zone_proximity_pct
                )
                indicators_df = pd.merge(indicators_df, zone_signals_df, left_index=True, right_index=True, how='left')
                # Fix chained assignment warnings by using direct assignment instead of inplace operations
                indicators_df['price_in_demand_zone'] = indicators_df['price_in_demand_zone'].fillna(False)
                indicators_df['price_in_supply_zone'] = indicators_df['price_in_supply_zone'].fillna(False)
                logger.debug("Zone signals added.")
            else:
                logger.debug("No zones found, adding placeholder columns.")
                indicators_df['price_in_demand_zone'] = False
                indicators_df['price_in_supply_zone'] = False

        except Exception as e:
            logger.error(f"Error calculating S/D zones or signals: {e}", exc_info=True)
            indicators_df['price_in_demand_zone'] = False
            indicators_df['price_in_supply_zone'] = False
    else:
        indicators_df['price_in_demand_zone'] = False
        indicators_df['price_in_supply_zone'] = False

    # Standardize column names to snake_case using centralized utility function
    from .wfo_utils import standardize_column_names
    indicators_df = standardize_column_names(indicators_df)

    final_df = pd.concat([ohlc_data, indicators_df], axis=1)

    logger.info(f"Indicators added. Final DataFrame shape: {final_df.shape}")
    return final_df


if __name__ == '__main__':
    # Create dummy OHLC data 
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=500, freq='1D')
    price_data = np.random.randn(500).cumsum() + 100
    open_prices = price_data + np.random.randn(500) * 0.1
    high_prices = np.maximum.reduce([open_prices, price_data + np.random.uniform(0.1, 1.0, 500), price_data])
    low_prices = np.minimum.reduce([open_prices, price_data - np.random.uniform(0.1, 1.0, 500), price_data])
    close_prices = price_data 
    volume = np.random.randint(100, 1000, 500)

    ohlc = pd.DataFrame({
        'Open': open_prices,
        'High': high_prices,
        'Low': low_prices,
        'Close': close_prices,
        'Volume': volume
    }, index=dates)

    default_config = EdgeConfig()
    print("--- Using Default Config --- ")

    print("\n--- Calculating Indicators (including Zones & ATR) --- ")
    indicators_data = add_indicators(ohlc, default_config)

    print("\n--- Combined Data with Indicators (Last 5 rows) --- ")
    print(indicators_data.tail().to_string())
    print("\nColumns:", indicators_data.columns.tolist())

    print("\n--- Checking Zone Signals --- ")
    print(f"Price in Demand Zone: {indicators_data['price_in_demand_zone'].sum()} times")
    print(f"Price in Supply Zone: {indicators_data['price_in_supply_zone'].sum()} times")
    print(f"ATR NaN count: {indicators_data['atr_stops'].isnull().sum()}")
