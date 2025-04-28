import pandas as pd
import numpy as np
import vectorbtpro as vbt
import talib
from pydantic import ValidationError
import logging

from .config import EdgeConfig 
from .zones import find_pivot_zones, add_zone_signals 

logger = logging.getLogger(__name__)


def validate_ohlc_columns(df: pd.DataFrame):
    required_cols = ['Open', 'High', 'Low', 'Close'] 
    if not all(col in df.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        raise ValueError(f"Input DataFrame missing one or more required columns: {missing}")


def add_indicators(ohlc_data: pd.DataFrame, config: EdgeConfig):
    try:
        validate_ohlc_columns(ohlc_data)
    except ValueError as e:
        logger.error(f"OHLC column validation failed: {e}")
        return None

    close = ohlc_data['Close'].copy()
    high = ohlc_data['High'].copy()
    low = ohlc_data['Low'].copy()

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
        
        # Get atr_window_sizing - either use the attribute or fall back to atr_window
        atr_window_sizing = config.atr_window
        if hasattr(config, 'atr_window_sizing'):
            atr_window_sizing = config.atr_window_sizing
        else:
            logger.warning(f"atr_window_sizing not found in config, using atr_window ({config.atr_window}) instead")
            
        indicators_df['atr_sizing'] = talib.ATR(high, low, close, timeperiod=atr_window_sizing)
        
        # Add ADX calculation for market regime detection
        indicators_df['adx'] = talib.ADX(high, low, close, timeperiod=config.adx_window if hasattr(config, 'adx_window') else 14)
        # Also add +DI and -DI for additional directional indicators if needed
        indicators_df['plus_di'] = talib.PLUS_DI(high, low, close, timeperiod=config.adx_window if hasattr(config, 'adx_window') else 14)
        indicators_df['minus_di'] = talib.MINUS_DI(high, low, close, timeperiod=config.adx_window if hasattr(config, 'adx_window') else 14)

    except Exception as e:
        logger.error(f"Error calculating standard indicators: {e}", exc_info=True)
        return None

    # Check if use_zones is available, default to False if not
    use_zones = False
    if hasattr(config, 'use_zones'):
        use_zones = config.use_zones
    else:
        logger.warning("use_zones parameter not found in config, defaulting to False")
    
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
    from scripts.strategies.refactored_edge.wfo_utils import standardize_column_names
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
