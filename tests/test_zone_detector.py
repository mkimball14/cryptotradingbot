import pytest
import pandas as pd
from datetime import datetime, timezone
import numpy as np

# Adjust import based on project structure
from src.zone_detector import (
    detect_base_patterns, 
    BASE_CANDLE_BODY_THRESHOLD, 
    calculate_freshness_score, 
    calculate_strength_score,
    calculate_rsi
)

def create_candle(timestamp, o, h, l, c):
    """Helper to create a candle Series."""
    # Timestamp needs to be timezone-aware for consistency if DataManager provides it
    ts = pd.Timestamp(timestamp, tz=timezone.utc)
    return pd.Series({'timestamp': ts, 'open': float(o), 'high': float(h), 'low': float(l), 'close': float(c)})

def test_detect_demand_zone_simple():
    """Test detecting a simple Drop-Base-Rally pattern."""
    # Leg-In (Down), Base, Leg-Out (Up)
    data = [
        create_candle('2023-01-01 10:00:00', 100, 101, 95, 96),  # Index 0: Leg In (Down)
        create_candle('2023-01-01 11:00:00', 96.5, 97, 96, 96.5), # Index 1: Base
        create_candle('2023-01-01 12:00:00', 97, 105, 96.8, 104) # Index 2: Leg Out (Up, closes > base high)
    ]
    df = pd.DataFrame(data)

    zones = detect_base_patterns(df)

    assert len(zones) == 1
    zone = zones[0]
    assert zone['type'] == 'demand'
    assert zone['leg_in_index'] == 0
    assert zone['base_start_index'] == 1
    assert zone['base_end_index'] == 1
    assert zone['leg_out_index'] == 2
    assert zone['zone_low'] == 96.0 # Low of the base candle(s)
    assert zone['zone_high'] == 97.0 # High of the base candle(s)
    assert len(zone['base_timestamps']) == 1
    assert zone['base_timestamps'][0] == df.iloc[1]['timestamp']

def test_detect_supply_zone_simple():
    """Test detecting a simple Rally-Base-Drop pattern."""
    # Leg-In (Up), Base, Leg-Out (Down)
    data = [
        create_candle('2023-01-01 10:00:00', 100, 105, 99, 104), # Index 0: Leg In (Up)
        create_candle('2023-01-01 11:00:00', 103.5, 104, 103, 103.5), # Index 1: Base
        create_candle('2023-01-01 12:00:00', 103, 103.2, 95, 96)  # Index 2: Leg Out (Down, closes < base low)
    ]
    df = pd.DataFrame(data)

    zones = detect_base_patterns(df)

    assert len(zones) == 1
    zone = zones[0]
    assert zone['type'] == 'supply'
    assert zone['leg_in_index'] == 0
    assert zone['base_start_index'] == 1
    assert zone['base_end_index'] == 1
    assert zone['leg_out_index'] == 2
    assert zone['zone_low'] == 103.0 # Low of the base candle(s)
    assert zone['zone_high'] == 104.0 # High of the base candle(s)
    assert zone['base_timestamps'][0] == df.iloc[1]['timestamp'] 

def test_detect_demand_multiple_bases():
    """Test detecting Drop-Base-Rally with multiple base candles."""
    data = [
        create_candle('2023-01-01 10:00:00', 100, 101, 95, 96),  # Index 0: Leg In (Down)
        create_candle('2023-01-01 11:00:00', 96.5, 97.5, 96, 96.5), # Index 1: Base 1
        create_candle('2023-01-01 12:00:00', 96.6, 97.8, 96.2, 96.8), # Index 2: Base 2 (Highest high)
        create_candle('2023-01-01 13:00:00', 97, 105, 96.8, 104) # Index 3: Leg Out (Up, closes > base high)
    ]
    df = pd.DataFrame(data)

    zones = detect_base_patterns(df)

    assert len(zones) == 1
    zone = zones[0]
    assert zone['type'] == 'demand'
    assert zone['leg_in_index'] == 0
    assert zone['base_start_index'] == 1
    assert zone['base_end_index'] == 2
    assert zone['leg_out_index'] == 3
    assert zone['zone_low'] == 96.0  # Lowest low of base 1 & 2
    assert zone['zone_high'] == 97.8 # Highest high of base 1 & 2
    assert len(zone['base_timestamps']) == 2

def test_detect_supply_multiple_bases():
    """Test detecting Rally-Base-Drop with multiple base candles."""
    data = [
        create_candle('2023-01-01 10:00:00', 100, 105, 99, 104), # Index 0: Leg In (Up)
        create_candle('2023-01-01 11:00:00', 103.5, 104.5, 103, 103.5), # Index 1: Base 1 (Lowest low)
        create_candle('2023-01-01 12:00:00', 103.6, 104.8, 103.2, 104.0), # Index 2: Base 2
        create_candle('2023-01-01 13:00:00', 103, 103.2, 95, 96)  # Index 3: Leg Out (Down, closes < base low)
    ]
    df = pd.DataFrame(data)

    zones = detect_base_patterns(df)

    assert len(zones) == 1
    zone = zones[0]
    assert zone['type'] == 'supply'
    assert zone['leg_in_index'] == 0
    assert zone['base_start_index'] == 1
    assert zone['base_end_index'] == 2
    assert zone['leg_out_index'] == 3
    assert zone['zone_low'] == 103.0 # Lowest low of base 1 & 2
    assert zone['zone_high'] == 104.8 # Highest high of base 1 & 2
    assert len(zone['base_timestamps']) == 2

def test_no_zone_leg_out_fails_breakout():
    """Test that no zone is detected if leg-out doesn't break base high/low."""
    # Demand: Leg-out close <= base high
    data_demand_fail = [
        create_candle('2023-01-01 10:00:00', 100, 101, 95, 96),  # Leg In (Down)
        create_candle('2023-01-01 11:00:00', 96.5, 97, 96, 96.5), # Base (High = 97)
        create_candle('2023-01-01 12:00:00', 97, 98, 96.8, 97)    # Leg Out (Up, but Close !> 97)
    ]
    df_demand_fail = pd.DataFrame(data_demand_fail)
    assert detect_base_patterns(df_demand_fail) == []

    # Supply: Leg-out close >= base low
    data_supply_fail = [
        create_candle('2023-01-01 10:00:00', 100, 105, 99, 104), # Leg In (Up)
        create_candle('2023-01-01 11:00:00', 103.5, 104, 103, 103.5), # Base (Low = 103)
        create_candle('2023-01-01 12:00:00', 103, 103.5, 100, 103) # Leg Out (Down, but Close !< 103)
    ]
    df_supply_fail = pd.DataFrame(data_supply_fail)
    assert detect_base_patterns(df_supply_fail) == []

def test_no_zone_incorrect_candle_types():
    """Test sequences with incorrect candle types (not leg or base where expected)."""
    # Leg-Base-Leg (Wrong direction Leg Out for Demand)
    data1 = [
        create_candle('2023-01-01 10:00:00', 100, 101, 95, 96),  # Leg In (Down)
        create_candle('2023-01-01 11:00:00', 96.5, 97, 96, 96.5), # Base
        create_candle('2023-01-01 12:00:00', 97, 98, 95, 96)    # Leg Out (BUT Down)
    ]
    assert detect_base_patterns(pd.DataFrame(data1)) == []

    # Leg-Leg-Base (Missing Leg Out)
    data2 = [
        create_candle('2023-01-01 10:00:00', 100, 101, 95, 96),  # Leg In (Down)
        create_candle('2023-01-01 11:00:00', 96, 99, 95, 98),   # Leg (Instead of Base)
        create_candle('2023-01-01 12:00:00', 98.5, 99, 98, 98.5) # Base (Instead of Leg Out)
    ]
    assert detect_base_patterns(pd.DataFrame(data2)) == []

    # Base-Base-Leg (Missing Leg In)
    data3 = [
        create_candle('2023-01-01 10:00:00', 100.5, 101, 100, 100.5), # Base
        create_candle('2023-01-01 11:00:00', 100.6, 101.1, 100.2, 100.8),# Base
        create_candle('2023-01-01 12:00:00', 101, 105, 100.8, 104)   # Leg Out (Up)
    ]
    assert detect_base_patterns(pd.DataFrame(data3)) == []

def test_no_zone_insufficient_data():
    """Test with fewer than 3 candles."""
    data = [
        create_candle('2023-01-01 10:00:00', 100, 101, 95, 96),
        create_candle('2023-01-01 11:00:00', 96.5, 97, 96, 96.5)
    ]
    df = pd.DataFrame(data)
    assert detect_base_patterns(df) == [] 

# --- Scoring Tests ---

def test_freshness_score():
    """Test freshness score calculation based on touches after leg-out."""
    # Base Zone: 100-102
    base_zone_info = {
        'type': 'demand',
        'leg_in_index': 0,
        'base_start_index': 1,
        'base_end_index': 1,
        'leg_out_index': 2,
        'zone_low': 100.0,
        'zone_high': 102.0
    }

    # Scenario 1: No touches after leg-out
    data1 = [
        create_candle('10:00', 105, 106, 98, 99),   # Leg In
        create_candle('11:00', 101, 102, 100, 101), # Base
        create_candle('12:00', 101, 108, 100.5, 107),# Leg Out
        create_candle('13:00', 107, 110, 106, 109), # After - No touch
        create_candle('14:00', 109, 112, 108, 111)  # After - No touch
    ]
    df1 = pd.DataFrame(data1)
    assert calculate_freshness_score(base_zone_info, df1) == 10

    # Scenario 2: One touch after leg-out
    data2 = [
        create_candle('10:00', 105, 106, 98, 99),   # Leg In
        create_candle('11:00', 101, 102, 100, 101), # Base
        create_candle('12:00', 101, 108, 100.5, 107),# Leg Out
        create_candle('13:00', 107, 107.5, 101.5, 103), # After - TOUCH (Low <= zone_high, High >= zone_low)
        create_candle('14:00', 103, 105, 102.5, 104)  # After - No touch (Low > zone_high)
    ]
    df2 = pd.DataFrame(data2)
    assert calculate_freshness_score(base_zone_info, df2) == 5

    # Scenario 3: Two touches after leg-out
    data3 = [
        create_candle('10:00', 105, 106, 98, 99),   # Leg In
        create_candle('11:00', 101, 102, 100, 101), # Base
        create_candle('12:00', 101, 108, 100.5, 107),# Leg Out
        create_candle('13:00', 107, 107.5, 101.5, 103), # After - TOUCH 1
        create_candle('14:00', 103, 104, 99.5, 100.5)   # After - TOUCH 2 (High >= zone_low)
    ]
    df3 = pd.DataFrame(data3)
    assert calculate_freshness_score(base_zone_info, df3) == 1

    # Scenario 4: Touch within the zone (penetration)
    data4 = [
        create_candle('10:00', 105, 106, 98, 99),   # Leg In
        create_candle('11:00', 101, 102, 100, 101), # Base
        create_candle('12:00', 101, 108, 100.5, 107),# Leg Out
        create_candle('13:00', 107, 107.5, 100.5, 101.5) # After - TOUCH (Low & High within zone)
    ]
    df4 = pd.DataFrame(data4)
    assert calculate_freshness_score(base_zone_info, df4) == 5 # Counts as one touch

def test_strength_score():
    """Test strength score calculation based on leg-out candle body/range."""
    zone_info = {'leg_out_index': 0} # Only need leg_out_index for this test

    # Scenario 1: Strong leg-out (Body is 80% of range)
    # Range = 10 (110-100), Body = 8 (108-100)
    candle1 = create_candle('10:00', 100, 110, 100, 108)
    df1 = pd.DataFrame([candle1])
    assert calculate_strength_score(zone_info, df1) == 80

    # Scenario 2: Weak leg-out (Body is 20% of range)
    # Range = 10 (110-100), Body = 2 (106-104)
    candle2 = create_candle('10:00', 104, 110, 100, 106)
    df2 = pd.DataFrame([candle2])
    assert calculate_strength_score(zone_info, df2) == 20

    # Scenario 3: Leg-out with zero range (should be 0 strength)
    candle3 = create_candle('10:00', 105, 105, 105, 105)
    df3 = pd.DataFrame([candle3])
    assert calculate_strength_score(zone_info, df3) == 0

    # Scenario 4: Doji leg-out (zero body, should be 0 strength)
    # Range = 10 (110-100), Body = 0 (105-105)
    candle4 = create_candle('10:00', 105, 110, 100, 105)
    df4 = pd.DataFrame([candle4])
    assert calculate_strength_score(zone_info, df4) == 0 

# --- Indicator Tests ---

def test_calculate_rsi():
    """Test RSI calculation using pandas-ta."""
    # Simple linear increase for predictable RSI
    prices = pd.Series(range(100, 130))
    rsi = calculate_rsi(prices, period=14)
    
    # First 13 values should be NaN
    assert rsi.iloc[:13].isnull().all()
    # RSI of a steady uptrend should be high (close to 100)
    assert rsi.iloc[-1] > 90 # Check the last calculated value
    assert len(rsi) == len(prices)

    # Test with insufficient data
    prices_short = pd.Series(range(100, 110)) # Only 10 data points
    rsi_short = calculate_rsi(prices_short, period=14)
    assert rsi_short.isnull().all()
    assert len(rsi_short) == len(prices_short)

    # Test with flat data (RSI should be around 50, pandas-ta might give NaN or specific value)
    prices_flat = pd.Series([100] * 30)
    rsi_flat = calculate_rsi(prices_flat, period=14)
    assert rsi_flat.iloc[:13].isnull().all()
    # pandas-ta typically gives 100.0 for flat series after initial NaNs
    assert rsi_flat.iloc[-1] == 100.0 or np.isnan(rsi_flat.iloc[-1]) # Allow NaN or 100 