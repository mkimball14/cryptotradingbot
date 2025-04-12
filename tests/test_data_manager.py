import pytest
import pandas as pd # Import pandas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import patch, MagicMock
import time
from datetime import datetime, timedelta, timezone
# Correct import for pandas-ta
import pandas_ta as ta
import unittest
import os
import json

# Updated import path
from app.core.database.models import Base, Candle, Zone

# Adjust path to find DataManager in the correct location (now in app/core)
from app.core.data_manager import DataManager, TIMEFRAME_TO_GRANULARITY # Import helper dict from correct location
# Remove Granularity import, import OHLCVProcessor
from app.core.data_processor import OHLCVProcessor
# Import zone detector function from correct location
from app.core.zone_detector import detect_base_patterns # Need this for direct use in test setup

# Define helper function directly in the test file
def create_candle(timestamp, o, h, l, c):
    """Helper to create a candle Series."""
    ts = pd.Timestamp(timestamp, tz=timezone.utc)
    return pd.Series({'timestamp': ts, 'open': float(o), 'high': float(h), 'low': float(l), 'close': float(c)})

# In-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for a test, with tables created."""
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        # Clean up database state
        Base.metadata.drop_all(bind=engine)
        session.close()

@pytest.fixture
def mock_processor(): # Rename fixture
    """Provides a mock OHLCVProcessor instance."""
    # Patch the correct class where it's instantiated in DataManager
    # Use the path relative to where DataManager imports it
    with patch('app.core.data_manager.OHLCVProcessor') as mock:
        instance = mock.return_value
        # Mock the get_ohlcv method
        instance.get_ohlcv = MagicMock()
        # Make the processor have the timeframe map for the helper function
        instance.valid_timeframes = TIMEFRAME_TO_GRANULARITY
        yield instance

# --- Test Cases --- 

def test_store_historical_ohlcv_success(db_session: Session, mock_processor: MagicMock):
    """Test successfully fetching and storing historical data."""
    manager = DataManager(db_session=db_session)
    # No need to inject mock_processor, it's patched during DataManager init

    symbol = "BTC-USD"
    timeframe = "1h" # Use string timeframe
    api_granularity = TIMEFRAME_TO_GRANULARITY[timeframe]
    start_unix = int(time.time()) - 3600 * 5 # 5 hours ago
    end_unix = int(time.time())
    start_dt = datetime.fromtimestamp(start_unix, tz=timezone.utc)
    end_dt = datetime.fromtimestamp(end_unix, tz=timezone.utc)

    # Mock processor response (DataFrame)
    mock_data = {
        'timestamp': [start_dt, start_dt + timedelta(hours=1)],
        'open': [50000.0, 50500.0],
        'high': [51000.0, 51500.0],
        'low': [49000.0, 50000.0],
        'close': [50500.0, 51000.0],
        'volume': [100.0, 120.0]
    }
    mock_df = pd.DataFrame(mock_data)
    mock_processor.get_ohlcv.return_value = mock_df

    # Call the method under test
    manager.store_historical_ohlcv(symbol, timeframe, start_unix, end_unix)

    # Assertions: Check call to processor's get_ohlcv
    mock_processor.get_ohlcv.assert_called_once()
    call_args = mock_processor.get_ohlcv.call_args[1]
    assert call_args['symbol'] == symbol
    assert call_args['timeframe'] == timeframe
    # Allow for slight differences in datetime objects if seconds differ
    assert abs((call_args['start_time'] - start_dt).total_seconds()) < 1
    assert abs((call_args['end_time'] - end_dt).total_seconds()) < 1

    # Verify data in DB
    stored_candles = db_session.query(Candle).order_by(Candle.timestamp).all()
    assert len(stored_candles) == 2
    assert stored_candles[0].symbol == symbol
    assert stored_candles[0].granularity == api_granularity # Check stored granularity string
    assert stored_candles[0].timestamp == int(start_dt.timestamp())
    assert stored_candles[0].open == 50000.0
    assert stored_candles[0].close == 50500.0
    assert stored_candles[1].timestamp == int((start_dt + timedelta(hours=1)).timestamp())
    assert stored_candles[1].volume == 120.0

    manager.close_session() # Clean up

def test_store_historical_ohlcv_duplicates(db_session: Session, mock_processor: MagicMock):
    """Test that storing duplicate data is handled gracefully (IntegrityError)."""
    manager = DataManager(db_session=db_session)

    symbol = "ETH-USD"
    timeframe = "15m" # Use string timeframe
    api_granularity = TIMEFRAME_TO_GRANULARITY[timeframe]
    start_unix = int(time.time()) - 900 * 3 # 3 intervals ago
    end_unix = int(time.time())
    start_dt = datetime.fromtimestamp(start_unix, tz=timezone.utc)

    mock_data = {
        'timestamp': [start_dt],
        'open': [3000.0],
        'high': [3100.0],
        'low': [2900.0],
        'close': [3050.0],
        'volume': [50.0]
    }
    mock_df = pd.DataFrame(mock_data)
    mock_processor.get_ohlcv.return_value = mock_df

    # Call first time (should succeed)
    manager.store_historical_ohlcv(symbol, timeframe, start_unix, end_unix)

    # Verify data in DB
    stored_candles_1 = db_session.query(Candle).all()
    assert len(stored_candles_1) == 1

    # Call second time with the same data (should trigger IntegrityError, but be handled)
    mock_processor.get_ohlcv.reset_mock() # Reset mock for call count check
    mock_processor.get_ohlcv.return_value = mock_df
    manager.store_historical_ohlcv(symbol, timeframe, start_unix, end_unix)

    # Verify data in DB again - should still only have 1 candle
    stored_candles_2 = db_session.query(Candle).all()
    assert len(stored_candles_2) == 1
    assert stored_candles_2[0].symbol == symbol
    assert stored_candles_2[0].granularity == api_granularity
    assert stored_candles_2[0].timestamp == int(start_dt.timestamp())

    # Check that processor was called again
    assert mock_processor.get_ohlcv.call_count == 1

    manager.close_session()

def test_get_stored_ohlcv(db_session: Session, mock_processor: MagicMock):
    """Test retrieving stored OHLCV data with filters."""
    # manager init patches processor, but we don't need the mock return value here
    manager = DataManager(db_session=db_session)

    symbol = "LTC-USD"
    timeframe = "4h" # Use string timeframe
    api_granularity = TIMEFRAME_TO_GRANULARITY[timeframe]
    now = int(datetime.now(timezone.utc).timestamp())
    # Align timestamps roughly to 4h intervals for realism
    start_ts_1 = (now // (3600 * 4) - 3) * 3600 * 4
    start_ts_2 = (now // (3600 * 4) - 2) * 3600 * 4
    start_ts_3 = (now // (3600 * 4) - 1) * 3600 * 4

    # Store some initial data directly
    candles_to_add = [
        Candle(symbol=symbol, granularity=api_granularity, timestamp=start_ts_1, open=100, high=110, low=95, close=105, volume=1000),
        Candle(symbol=symbol, granularity=api_granularity, timestamp=start_ts_2, open=105, high=115, low=100, close=110, volume=1200),
        Candle(symbol=symbol, granularity=api_granularity, timestamp=start_ts_3, open=110, high=120, low=105, close=115, volume=1100),
        # Different symbol
        Candle(symbol="BTC-USD", granularity=api_granularity, timestamp=start_ts_2, open=50000, high=51000, low=49000, close=50500, volume=50),
        # Different granularity
        Candle(symbol=symbol, granularity=TIMEFRAME_TO_GRANULARITY['1h'], timestamp=start_ts_2, open=106, high=107, low=105, close=106.5, volume=100)
    ]
    db_session.add_all(candles_to_add)
    db_session.commit()

    # --- Test retrieval --- 
    # Retrieve last 2 candles for LTC-USD 4h
    retrieve_start = start_ts_2
    retrieve_end = start_ts_3
    retrieved_candles = manager.get_stored_ohlcv(symbol, timeframe, retrieve_start, retrieve_end)

    assert len(retrieved_candles) == 2
    assert retrieved_candles[0].timestamp == start_ts_2
    assert retrieved_candles[0].symbol == symbol
    assert retrieved_candles[0].granularity == api_granularity
    assert retrieved_candles[0].close == 110.0
    assert retrieved_candles[1].timestamp == start_ts_3
    assert retrieved_candles[1].close == 115.0

    # --- Test retrieval with no match (wrong timeframe) ---
    retrieved_candles_wrong_tf = manager.get_stored_ohlcv(symbol, '1h', retrieve_start, retrieve_end)
    assert len(retrieved_candles_wrong_tf) == 1 # Should find the 1h candle we added
    assert retrieved_candles_wrong_tf[0].granularity == TIMEFRAME_TO_GRANULARITY['1h']

    # --- Test retrieval with no match (time range) --- 
    retrieve_start_nomatch = now + 3600 # Future
    retrieve_end_nomatch = now + 7200
    retrieved_candles_nomatch = manager.get_stored_ohlcv(symbol, timeframe, retrieve_start_nomatch, retrieve_end_nomatch)
    assert len(retrieved_candles_nomatch) == 0

    manager.close_session()

def test_update_recent_ohlcv_success(db_session: Session, mock_processor: MagicMock):
    """Test updating recent data when prior data exists."""
    manager = DataManager(db_session=db_session)

    symbol = "BTC-USD"
    timeframe = "1h"
    api_granularity = TIMEFRAME_TO_GRANULARITY[timeframe]
    interval_seconds = 3600
    # Align to the start of an hour for predictable timestamps
    now_dt_aware = datetime.now(timezone.utc)
    start_of_current_hour = now_dt_aware.replace(minute=0, second=0, microsecond=0)

    latest_stored_ts_unix = int((start_of_current_hour - timedelta(hours=2)).timestamp())
    next_expected_dt = start_of_current_hour - timedelta(hours=1)
    next_expected_ts_unix = int(next_expected_dt.timestamp())

    # Store initial candle
    initial_candle = Candle(symbol=symbol, granularity=api_granularity, timestamp=latest_stored_ts_unix, open=50000, high=50100, low=49900, close=50050, volume=50)
    db_session.add(initial_candle)
    db_session.commit()

    # Mock processor response for the *new* candle
    mock_data = {
        'timestamp': [next_expected_dt],
        'open': [50050.0],
        'high': [50500.0],
        'low': [50000.0],
        'close': [50400.0],
        'volume': [60.0]
    }
    mock_df = pd.DataFrame(mock_data)
    mock_processor.get_ohlcv.return_value = mock_df

    # Call the method under test
    manager.update_recent_ohlcv(symbol, timeframe)

    # Assertions
    expected_start_dt = datetime.fromtimestamp(latest_stored_ts_unix, tz=timezone.utc) + timedelta(seconds=1)

    assert mock_processor.get_ohlcv.call_count == 1
    call_args = mock_processor.get_ohlcv.call_args[1]
    assert call_args['symbol'] == symbol
    assert call_args['timeframe'] == timeframe
    assert abs((call_args['start_time'] - expected_start_dt).total_seconds()) < 1
    # End time should be roughly now
    assert abs((call_args['end_time'] - datetime.now(timezone.utc)).total_seconds()) < 5 # Allow 5s diff

    # Verify data in DB - should now have 2 candles
    stored_candles = db_session.query(Candle).filter(Candle.symbol == symbol, Candle.granularity == api_granularity).order_by(Candle.timestamp).all()
    assert len(stored_candles) == 2
    assert stored_candles[0].timestamp == latest_stored_ts_unix
    assert stored_candles[1].timestamp == next_expected_ts_unix
    assert stored_candles[1].close == 50400.0

    manager.close_session()

def test_update_recent_ohlcv_no_prior_data(db_session: Session, mock_processor: MagicMock, caplog):
    """Test update_recent_ohlcv when no prior data exists for the symbol/granularity."""
    manager = DataManager(db_session=db_session)

    symbol = "ADA-USD"
    timeframe = "15m"
    api_granularity = TIMEFRAME_TO_GRANULARITY[timeframe]

    # Ensure DB is empty for this symbol/granularity
    count = db_session.query(Candle).filter(Candle.symbol == symbol, Candle.granularity == api_granularity).count()
    assert count == 0

    # Call the method under test
    with caplog.at_level("WARNING"):
        manager.update_recent_ohlcv(symbol, timeframe)

    # Assertions
    # Processor should NOT have been called
    mock_processor.get_ohlcv.assert_not_called()

    # Verify DB is still empty
    count_after = db_session.query(Candle).filter(Candle.symbol == symbol, Candle.granularity == api_granularity).count()
    assert count_after == 0

    # Check log message
    assert f"No existing data found for {symbol} ({timeframe})" in caplog.text

    manager.close_session()

# --- Zone Management Tests ---

def test_detect_and_store_zones_success(db_session: Session, mock_processor: MagicMock):
    """Test detecting and storing new zones successfully."""
    manager = DataManager(db_session=db_session)
    # We won't use the mock_processor here, providing df directly

    symbol = "XYZ-USD"
    timeframe = "1h"
    api_granularity = TIMEFRAME_TO_GRANULARITY[timeframe]

    # Create DataFrame with a demand zone, including pre-data for RSI(14)
    # Need at least 14+3 = 17 candles total
    pre_data_points = 14
    data = []
    # Add declining prices before the zone
    for i in range(pre_data_points):
        price = 120 - i # Simple linear decline
        ts = pd.Timestamp(f'2023-01-01 {10+i:02d}:00:00', tz=timezone.utc) - timedelta(hours=pre_data_points)
        data.append(pd.Series({'timestamp': ts, 'open': price+1, 'high': price+2, 'low': price-1, 'close': price}))

    # Zone Pattern Data (indices adjusted based on pre_data)
    zone_start_index = pre_data_points
    data.extend([
        create_candle(f'2023-01-01 10:00:00', 105, 106, 98, 99),   # index pre_data_points + 0: Leg In (Down)
        create_candle(f'2023-01-01 11:00:00', 101, 102, 100, 101), # index pre_data_points + 1: Base (Low 100, High 102)
        create_candle(f'2023-01-01 12:00:00', 101, 108, 100.5, 107),# index pre_data_points + 2: Leg Out (Up, Close > Base High)
        create_candle(f'2023-01-01 13:00:00', 107, 110, 106, 109)  # index pre_data_points + 3: After
    ])
    ohlcv_df = pd.DataFrame(data)

    # Calculate expected RSI at formation (leg-out candle)
    # Note: This depends heavily on pandas-ta implementation details & the exact data
    # We expect RSI to be low due to the preceding drop. Exact value isn't critical for the test.
    # Manually run ta.rsi(ohlcv_df['close'], length=14) to find expected value if needed.
    # Let's assume for this data it results in ~25 for testing purposes.
    expected_rsi_at_formation = ta.rsi(ohlcv_df['close'], length=14).iloc[zone_start_index + 2]

    # Call the method under test
    manager.detect_and_store_zones(symbol, timeframe, ohlcv_df=ohlcv_df)

    # Verify zone stored in DB
    stored_zones = db_session.query(Zone).all()
    assert len(stored_zones) == 1
    zone_db = stored_zones[0]

    assert zone_db.symbol == symbol
    assert zone_db.timeframe == timeframe
    assert zone_db.type == 'demand'
    assert zone_db.zone_low == 100.0
    assert zone_db.zone_high == 102.0
    assert zone_db.leg_in_timestamp == int(ohlcv_df.iloc[zone_start_index]['timestamp'].timestamp())
    assert zone_db.base_start_timestamp == int(ohlcv_df.iloc[zone_start_index + 1]['timestamp'].timestamp())
    assert zone_db.base_end_timestamp == int(ohlcv_df.iloc[zone_start_index + 1]['timestamp'].timestamp())
    assert zone_db.formation_timestamp == int(ohlcv_df.iloc[zone_start_index + 2]['timestamp'].timestamp())
    assert zone_db.is_active is True
    assert zone_db.num_touches == 0
    # Check scores 
    assert zone_db.initial_freshness_score == 10 
    assert zone_db.initial_strength_score == 80
    # Check stored RSI value
    assert zone_db.rsi_at_formation == pytest.approx(expected_rsi_at_formation) # Use approx for float comparison

    manager.close_session()

def test_detect_and_store_zones_duplicates(db_session: Session, mock_processor: MagicMock):
    """Test that storing duplicate zones is handled."""
    manager = DataManager(db_session=db_session)

    symbol = "XYZ-USD"
    timeframe = "1h"
    # DataFrame with a demand zone
    data = [
        create_candle('10:00', 105, 106, 98, 99),   # 0: Leg In
        create_candle('11:00', 101, 102, 100, 101), # 1: Base
        create_candle('12:00', 101, 108, 100.5, 107),# 2: Leg Out
        create_candle('13:00', 107, 110, 106, 109)  # 3: After
    ]
    ohlcv_df = pd.DataFrame(data)

    # Call first time
    manager.detect_and_store_zones(symbol, timeframe, ohlcv_df=ohlcv_df)
    assert db_session.query(Zone).count() == 1

    # Call second time with same data
    manager.detect_and_store_zones(symbol, timeframe, ohlcv_df=ohlcv_df)
    # Count should still be 1 due to unique constraint
    assert db_session.query(Zone).count() == 1 

    manager.close_session()

def test_get_active_zones(db_session: Session, mock_processor: MagicMock):
    """Test retrieving active zones."""
    manager = DataManager(db_session=db_session)

    symbol = "ABC-USD"
    timeframe = "15m"

    # Add some zones directly to DB
    zone1 = Zone(symbol=symbol, timeframe=timeframe, type='demand', zone_low=50, zone_high=51, formation_timestamp=1000, leg_in_timestamp=900, base_start_timestamp=950, base_end_timestamp=950, is_active=True)
    zone2 = Zone(symbol=symbol, timeframe=timeframe, type='supply', zone_low=60, zone_high=61, formation_timestamp=1200, leg_in_timestamp=1100, base_start_timestamp=1150, base_end_timestamp=1150, is_active=True)
    zone3 = Zone(symbol=symbol, timeframe=timeframe, type='demand', zone_low=45, zone_high=46, formation_timestamp=800, leg_in_timestamp=700, base_start_timestamp=750, base_end_timestamp=750, is_active=False) # Inactive
    zone4 = Zone(symbol="XYZ-USD", timeframe=timeframe, type='demand', zone_low=20, zone_high=21, formation_timestamp=1100, leg_in_timestamp=1000, base_start_timestamp=1050, base_end_timestamp=1050, is_active=True) # Different symbol
    zone5 = Zone(symbol=symbol, timeframe="1h", type='demand', zone_low=55, zone_high=56, formation_timestamp=1300, leg_in_timestamp=1200, base_start_timestamp=1250, base_end_timestamp=1250, is_active=True) # Different timeframe
    
    db_session.add_all([zone1, zone2, zone3, zone4, zone5])
    db_session.commit()

    # Retrieve active zones for ABC-USD 15m
    active_zones = manager.get_active_zones(symbol, timeframe)

    assert len(active_zones) == 2
    # Should be ordered by formation_timestamp desc
    assert active_zones[0].id == zone2.id
    assert active_zones[0].type == 'supply'
    assert active_zones[1].id == zone1.id
    assert active_zones[1].type == 'demand'
    
    # Retrieve for different timeframe
    active_zones_1h = manager.get_active_zones(symbol, "1h")
    assert len(active_zones_1h) == 1
    assert active_zones_1h[0].id == zone5.id

    # Retrieve for different symbol
    active_zones_xyz = manager.get_active_zones("XYZ-USD", timeframe)
    assert len(active_zones_xyz) == 1
    assert active_zones_xyz[0].id == zone4.id

    manager.close_session()

# --- Zone Status Update Tests ---

def test_update_zone_status_demand_touch(db_session: Session):
    """Test updating demand zone status on a touch."""
    manager = DataManager(db_session=db_session)
    symbol = "TOUCH-USD"
    timeframe = "1h"
    # Zone: Demand 100-102, formed at 1000
    zone = Zone(symbol=symbol, timeframe=timeframe, type='demand', zone_low=100, zone_high=102, formation_timestamp=1000, leg_in_timestamp=900, base_start_timestamp=950, base_end_timestamp=950, is_active=True)
    db_session.add(zone)
    db_session.commit()
    zone_id = zone.id # Get ID after commit

    # Candle touches zone (low=101.5) but closes inside (102.5)
    candle_data = {'timestamp': 1100, 'open': 103, 'high': 104, 'low': 101.5, 'close': 102.5}
    manager.update_zone_status(symbol, candle_data)

    # Verify zone status
    updated_zone = db_session.query(Zone).filter(Zone.id == zone_id).one()
    assert updated_zone.num_touches == 1
    assert updated_zone.last_tested_timestamp == 1100
    assert updated_zone.is_active is True
    manager.close_session()

def test_update_zone_status_demand_break(db_session: Session):
    """Test updating demand zone status on a break."""
    manager = DataManager(db_session=db_session)
    symbol = "BREAK-USD"
    timeframe = "1h"
    # Zone: Demand 100-102, formed at 1000
    zone = Zone(symbol=symbol, timeframe=timeframe, type='demand', zone_low=100, zone_high=102, formation_timestamp=1000, leg_in_timestamp=900, base_start_timestamp=950, base_end_timestamp=950, is_active=True)
    db_session.add(zone)
    db_session.commit()
    zone_id = zone.id

    # Candle closes below zone low (close=99)
    candle_data = {'timestamp': 1100, 'open': 101, 'high': 101.5, 'low': 98, 'close': 99}
    manager.update_zone_status(symbol, candle_data)

    # Verify zone status
    updated_zone = db_session.query(Zone).filter(Zone.id == zone_id).one()
    assert updated_zone.num_touches == 1
    assert updated_zone.last_tested_timestamp == 1100
    assert updated_zone.is_active is False # Should be deactivated
    manager.close_session()

def test_update_zone_status_supply_touch(db_session: Session):
    """Test updating supply zone status on a touch."""
    manager = DataManager(db_session=db_session)
    symbol = "TOUCH-USD"
    timeframe = "1h"
    # Zone: Supply 100-102, formed at 1000
    zone = Zone(symbol=symbol, timeframe=timeframe, type='supply', zone_low=100, zone_high=102, formation_timestamp=1000, leg_in_timestamp=900, base_start_timestamp=950, base_end_timestamp=950, is_active=True)
    db_session.add(zone)
    db_session.commit()
    zone_id = zone.id

    # Candle touches zone (high=100.5) but closes inside (99.5)
    candle_data = {'timestamp': 1100, 'open': 99, 'high': 100.5, 'low': 98, 'close': 99.5}
    manager.update_zone_status(symbol, candle_data)

    # Verify zone status
    updated_zone = db_session.query(Zone).filter(Zone.id == zone_id).one()
    assert updated_zone.num_touches == 1
    assert updated_zone.last_tested_timestamp == 1100
    assert updated_zone.is_active is True
    manager.close_session()

def test_update_zone_status_supply_break(db_session: Session):
    """Test updating supply zone status on a break."""
    manager = DataManager(db_session=db_session)
    symbol = "BREAK-USD"
    timeframe = "1h"
    # Zone: Supply 100-102, formed at 1000
    zone = Zone(symbol=symbol, timeframe=timeframe, type='supply', zone_low=100, zone_high=102, formation_timestamp=1000, leg_in_timestamp=900, base_start_timestamp=950, base_end_timestamp=950, is_active=True)
    db_session.add(zone)
    db_session.commit()
    zone_id = zone.id

    # Candle closes above zone high (close=103)
    candle_data = {'timestamp': 1100, 'open': 101.5, 'high': 104, 'low': 101, 'close': 103}
    manager.update_zone_status(symbol, candle_data)

    # Verify zone status
    updated_zone = db_session.query(Zone).filter(Zone.id == zone_id).one()
    assert updated_zone.num_touches == 1
    assert updated_zone.last_tested_timestamp == 1100
    assert updated_zone.is_active is False # Should be deactivated
    manager.close_session()

def test_update_zone_status_no_interaction(db_session: Session):
    """Test when candle does not interact with the zone."""
    manager = DataManager(db_session=db_session)
    symbol = "NOINT-USD"
    timeframe = "1h"
    # Zone: Demand 100-102, formed at 1000
    zone = Zone(symbol=symbol, timeframe=timeframe, type='demand', zone_low=100, zone_high=102, formation_timestamp=1000, leg_in_timestamp=900, base_start_timestamp=950, base_end_timestamp=950, is_active=True)
    db_session.add(zone)
    db_session.commit()
    zone_id = zone.id

    # Candle is completely above the zone
    candle_data = {'timestamp': 1100, 'open': 103, 'high': 104, 'low': 102.1, 'close': 103.5}
    manager.update_zone_status(symbol, candle_data)

    # Verify zone status (should be unchanged)
    updated_zone = db_session.query(Zone).filter(Zone.id == zone_id).one()
    assert updated_zone.num_touches == 0
    assert updated_zone.last_tested_timestamp is None
    assert updated_zone.is_active is True
    manager.close_session()

def test_update_zone_status_candle_before_formation(db_session: Session):
    """Test candle occurring before zone formation doesn't update status."""
    manager = DataManager(db_session=db_session)
    symbol = "EARLY-USD"
    timeframe = "1h"
    # Zone: Demand 100-102, formed at 1000
    zone = Zone(symbol=symbol, timeframe=timeframe, type='demand', zone_low=100, zone_high=102, formation_timestamp=1000, leg_in_timestamp=900, base_start_timestamp=950, base_end_timestamp=950, is_active=True)
    db_session.add(zone)
    db_session.commit()
    zone_id = zone.id

    # Candle touches zone but occurs *before* formation_timestamp
    candle_data = {'timestamp': 980, 'open': 103, 'high': 104, 'low': 101.5, 'close': 102.5}
    manager.update_zone_status(symbol, candle_data)

    # Verify zone status (should be unchanged)
    updated_zone = db_session.query(Zone).filter(Zone.id == zone_id).one()
    assert updated_zone.num_touches == 0
    assert updated_zone.last_tested_timestamp is None
    assert updated_zone.is_active is True
    manager.close_session()

# --- Test Cases Will Go Here --- 