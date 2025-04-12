import pandas as pd
import numpy as np
import pandas_ta as ta # Import pandas-ta

# --- Configuration --- 
# Threshold for identifying base candles: Body size relative to total range (high-low)
# E.g., 0.3 means body must be less than 30% of the candle's full range.
BASE_CANDLE_BODY_THRESHOLD = 0.3

def is_base_candle(candle: pd.Series) -> bool:
    """Checks if a candle is a 'base' candle (small body relative to range).

    Args:
        candle: A pandas Series representing a single candle 
                (must contain 'open', 'close', 'high', 'low').

    Returns:
        True if the candle is considered a base candle, False otherwise.
    """
    try:
        body_size = abs(candle['close'] - candle['open'])
        total_range = candle['high'] - candle['low']

        # Avoid division by zero for candles with no range (e.g., price didn't move)
        if total_range <= 0:
            # Consider it a base candle if body is also zero, otherwise not.
            return body_size == 0

        return (body_size / total_range) < BASE_CANDLE_BODY_THRESHOLD
    except KeyError as e:
        print(f"Error: Candle data missing required key: {e}")
        return False
    except Exception as e:
        print(f"Error checking base candle: {e}")
        return False

def is_leg_candle(candle: pd.Series) -> bool:
    """Checks if a candle is a 'leg' candle (opposite of base).

    Args:
        candle: A pandas Series representing a single candle.

    Returns:
        True if the candle is considered a leg candle, False otherwise.
    """
    # Simply the inverse of is_base_candle
    return not is_base_candle(candle)

def get_candle_direction(candle: pd.Series) -> str:
    """Determines the direction of a candle.

    Args:
        candle: A pandas Series representing a single candle.

    Returns:
        'up' if close > open, 'down' if close < open, 'doji' if close == open.
    """
    if candle['close'] > candle['open']:
        return 'up'
    elif candle['close'] < candle['open']:
        return 'down'
    else:
        return 'doji'

# --- Indicator Calculations ---

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculates the Relative Strength Index (RSI) using pandas-ta.

    Args:
        series: A pandas Series of prices (e.g., close prices).
        period: The RSI lookback period.

    Returns:
        A pandas Series containing the RSI values.
    """
    if series.empty or len(series) < period:
        # Return an empty Series or Series of NaNs if not enough data
        return pd.Series([np.nan] * len(series), index=series.index)
    try:
        rsi_series = ta.rsi(series, length=period)
        # Fill initial NaNs if desired, though pandas-ta handles this
        # rsi_series = rsi_series.fillna(50) # Or another default
        return rsi_series
    except Exception as e:
        print(f"Error calculating RSI: {e}")
        # Return NaNs on error
        return pd.Series([np.nan] * len(series), index=series.index)

# --- Scoring Functions ---

def calculate_freshness_score(zone: dict, ohlcv_df: pd.DataFrame) -> int:
    """Calculates the freshness score of a detected zone.
    Counts how many candles after the leg-out have touched or penetrated the zone.
    Score: 10 (0 touches), 5 (1 touch), 1 (2+ touches).
    """
    touches = 0
    zone_low = zone['zone_low']
    zone_high = zone['zone_high']
    leg_out_index = zone['leg_out_index']

    # Iterate through candles *after* the leg-out candle
    for i in range(leg_out_index + 1, len(ohlcv_df)):
        candle = ohlcv_df.iloc[i]
        # Check if the candle's range overlaps with the zone
        if candle['low'] <= zone_high and candle['high'] >= zone_low:
            touches += 1
            # Optimization: if we reach 2 touches, the score is minimal, no need to check further
            if touches >= 2:
                break 
    
    if touches == 0:
        return 10 # Max score for untouched
    elif touches == 1:
        return 5  # Medium score for one touch
    else:
        return 1  # Min score for 2+ touches

def calculate_strength_score(zone: dict, ohlcv_df: pd.DataFrame) -> int:
    """Calculates the strength score based on the leg-out candle.
    Score is the leg-out body size as a percentage of its total range (0-100).
    """
    leg_out_index = zone['leg_out_index']
    leg_out_candle = ohlcv_df.iloc[leg_out_index]

    try:
        body_size = abs(leg_out_candle['close'] - leg_out_candle['open'])
        total_range = leg_out_candle['high'] - leg_out_candle['low']

        if total_range <= 0:
            return 0 # No range, no strength

        strength_percentage = round((body_size / total_range) * 100)
        return int(strength_percentage)
    except KeyError as e:
        print(f"Error: Leg-out candle data missing required key: {e}")
        return 0
    except Exception as e:
        print(f"Error calculating strength score: {e}")
        return 0

# --- Main Detection Logic ---
def detect_base_patterns(ohlcv_df: pd.DataFrame) -> list:
    """Detects Rally-Base-Drop (Supply) and Drop-Base-Rally (Demand) patterns,
       including RSI at formation time.

    Args:
        ohlcv_df: DataFrame with OHLCV data, sorted by timestamp ascending. 
                  Must include columns: ['timestamp', 'open', 'high', 'low', 'close'].

    Returns:
        A list of dictionaries, each representing a detected zone.
        Each dictionary contains:
            - type: 'supply' or 'demand'
            - leg_in_index: DataFrame index of the leg-in candle
            - base_start_index: DataFrame index of the first base candle
            - base_end_index: DataFrame index of the last base candle
            - leg_out_index: DataFrame index of the leg-out candle
            - zone_low: The lowest low price within the base candle(s)
            - zone_high: The highest high price within the base candle(s)
            - base_timestamps: List of timestamps for the base candles
            - rsi_at_formation: RSI(14) value at the time of the leg-out candle (or NaN)
    """
    zones = []
    if len(ohlcv_df) < 3: # Need at least 3 candles for a pattern
        return zones

    # Calculate RSI for the entire DataFrame first
    ohlcv_df['rsi_14'] = calculate_rsi(ohlcv_df['close'], period=14)

    i = 0
    while i < len(ohlcv_df) - 2:
        candle1 = ohlcv_df.iloc[i]
        direction1 = get_candle_direction(candle1)
        is_leg1 = is_leg_candle(candle1)

        if not is_leg1 or direction1 == 'doji':
            i += 1
            continue

        # Look for base candles starting from the next index
        j = i + 1
        base_indices = []
        while j < len(ohlcv_df):
            candle_base_candidate = ohlcv_df.iloc[j]
            if is_base_candle(candle_base_candidate):
                base_indices.append(j)
                j += 1
            else:
                break # Stop looking for base candles
        
        # Check if we found at least one base candle and have a candle after the base(s)
        if not base_indices or j >= len(ohlcv_df):
            # If no base found after leg1, just advance i
            # If base found but no candle after, advance i past the base
            i = j if base_indices else i + 1 
            continue

        # Now check the leg-out candle (candle at index j)
        candle3 = ohlcv_df.iloc[j]
        direction3 = get_candle_direction(candle3)
        is_leg3 = is_leg_candle(candle3)

        if not is_leg3 or direction3 == 'doji':
            # If candle3 is not a valid leg-out, advance i past the base sequence
            i = j 
            continue
        
        # --- Pattern Matching --- 
        base_start_index = base_indices[0]
        base_end_index = base_indices[-1]
        base_candles_df = ohlcv_df.iloc[base_start_index : base_end_index + 1]
        zone_low = base_candles_df['low'].min()
        zone_high = base_candles_df['high'].max()
        base_timestamps = base_candles_df['timestamp'].tolist()

        zone_info = {
            'leg_in_index': i,
            'base_start_index': base_start_index,
            'base_end_index': base_end_index,
            'leg_out_index': j,
            'zone_low': zone_low,
            'zone_high': zone_high,
            'base_timestamps': base_timestamps
        }

        pattern_found = False
        # Check for Demand (Drop-Base-Rally)
        if direction1 == 'down' and direction3 == 'up' and candle3['high'] > zone_high:
            zone_info['type'] = 'demand'
            pattern_found = True
            # zones.append(zone_info) # Append after scoring
            # i = j + 1 # Advance index after scoring
            # continue

        # Check for Supply (Rally-Base-Drop)
        if direction1 == 'up' and direction3 == 'down' and candle3['low'] < zone_low:
            zone_info['type'] = 'supply'
            pattern_found = True
            # zones.append(zone_info) # Append after scoring
            # i = j + 1 # Advance index after scoring
            # continue

        # If a pattern was found, calculate scores, get RSI, and append
        if pattern_found:
            zone_info['freshness_score'] = calculate_freshness_score(zone_info, ohlcv_df)
            zone_info['strength_score'] = calculate_strength_score(zone_info, ohlcv_df)
            # Get RSI value at the leg-out candle index (j)
            zone_info['rsi_at_formation'] = ohlcv_df.iloc[j].get('rsi_14', np.nan) # Use .get with default NaN
            zones.append(zone_info)
            # Advance index past the identified pattern
            i = j + 1
            continue

        # If no pattern matched, advance index past the base sequence found
        # This prevents re-evaluating the same base candles immediately
        i = j

    # Optional: Drop the RSI column if it shouldn't persist outside this function
    # Ensure the RSI column is dropped to prevent side effects
    ohlcv_df.drop(columns=['rsi_14'], inplace=True, errors='ignore') 

    return zones 