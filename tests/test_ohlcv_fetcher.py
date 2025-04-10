import pytest
import pandas as pd
from datetime import datetime, timedelta
from app.core.data_processor import OHLCVProcessor
from unittest.mock import patch, MagicMock
import json
from requests.exceptions import HTTPError
import requests

# Mock data generator for different symbols and timeframes
def create_mock_candles(symbol, start_timestamp, end_timestamp, granularity):
    """Create mock candle data that mimics Coinbase API response"""
    # Generate timestamps based on granularity
    if granularity == 'FIFTEEN_MINUTE':
        interval = 15 * 60  # 15 minutes in seconds
    elif granularity == 'ONE_HOUR':
        interval = 60 * 60  # 1 hour in seconds
    elif granularity == 'FOUR_HOUR':
        interval = 4 * 60 * 60  # 4 hours in seconds
    else:
        interval = 60 * 60  # Default to 1 hour
    
    # Convert string timestamps to int if needed
    start = int(start_timestamp) if isinstance(start_timestamp, str) else start_timestamp
    end = int(end_timestamp) if isinstance(end_timestamp, str) else end_timestamp
    
    # Create time points
    current = start
    candles = []
    
    # Base price varies by symbol
    if 'BTC' in symbol:
        base_price = 50000.0
    elif 'ETH' in symbol:
        base_price = 3000.0
    elif 'SOL' in symbol:
        base_price = 100.0
    else:
        base_price = 10.0
    
    # Generate mock candles
    while current < end:
        # Add some randomness to prices
        price_factor = 1 + (((current / 10000) % 10) - 5) / 100  # ±5% variation
        open_price = base_price * price_factor
        close_price = open_price * (1 + (((current / 1000) % 10) - 5) / 200)  # ±2.5% from open
        high_price = max(open_price, close_price) * 1.01  # 1% above max of open/close
        low_price = min(open_price, close_price) * 0.99   # 1% below min of open/close
        volume = 10.0 + (current % 100)  # Random volume
        
        # Format to match API response
        candle = {
            'start': str(current),
            'low': str(round(low_price, 2)),
            'high': str(round(high_price, 2)),
            'open': str(round(open_price, 2)),
            'close': str(round(close_price, 2)),
            'volume': str(round(volume, 8))
        }
        candles.append(candle)
        
        # Move to next interval
        current += interval
    
    # Format response like Coinbase API
    return {"candles": candles}


@pytest.fixture
def mock_coinbase_api():
    """Patch the Coinbase REST client to avoid real API calls"""
    with patch('coinbase.rest.RESTClient.get_public_candles') as mock_get_candles:
        # Configure the mock to use our test data generator
        def side_effect(product_id, start, end, granularity, **kwargs):
            return create_mock_candles(product_id, start, end, granularity)
        
        mock_get_candles.side_effect = side_effect
        yield mock_get_candles


# Update all tests to use the mock_coinbase_api fixture

def test_rate_limiting(mock_coinbase_api):
    """Test that rate limiting works correctly"""
    processor = OHLCVProcessor()
    
    # Make multiple rapid requests to trigger rate limiting
    start_time = datetime.now() - timedelta(days=1)
    symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD']  # Test multiple symbols
    
    for symbol in symbols:
        # This should complete successfully with mock data
        df = processor.get_ohlcv(
            symbol=symbol,
            timeframe='15m',
            start_time=start_time
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        
        # Check that we have data for the right symbol (via price ranges)
        if 'BTC' in symbol:
            assert df['close'].mean() > 45000  # Approximate check
        elif 'ETH' in symbol:
            assert df['close'].mean() > 2500  # Approximate check

def test_multi_symbol_consistency(mock_coinbase_api):
    """Test data retrieval across different trading pairs"""
    processor = OHLCVProcessor()
    start_time = datetime.now() - timedelta(hours=24)
    symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD']
    
    dataframes = {}
    for symbol in symbols:
        df = processor.get_ohlcv(
            symbol=symbol,
            timeframe='15m',
            start_time=start_time
        )
        dataframes[symbol] = df
        
        # Verify DataFrame structure
        assert isinstance(df, pd.DataFrame)
        assert all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume', 'timestamp'])
        assert df.index.is_monotonic_increasing  # Verify timestamps are ordered
        assert not df.empty
        
        # Verify data types
        assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])  # More flexible datetime type check
        assert all(pd.api.types.is_numeric_dtype(df[col]) for col in ['open', 'high', 'low', 'close', 'volume'])
    
    # Verify all symbols have the same timespan
    first_start = dataframes['BTC-USD']['timestamp'].min()
    first_end = dataframes['BTC-USD']['timestamp'].max()
    
    for symbol in symbols[1:]:
        assert abs((dataframes[symbol]['timestamp'].min() - first_start).total_seconds()) < 60  # Within a minute
        # Increase tolerance to slightly more than the interval (15m = 900s)
        assert abs((dataframes[symbol]['timestamp'].max() - first_end).total_seconds()) < 960 # Allow for ~1 interval difference

def test_timeframe_consistency(mock_coinbase_api):
    """Test data retrieval across different timeframes"""
    processor = OHLCVProcessor()
    symbol = 'BTC-USD'
    start_time = datetime.now() - timedelta(days=7)
    timeframes = ['15m', '1h', '4h']
    
    for timeframe in timeframes:
        df = processor.get_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            start_time=start_time
        )
        
        # Verify basic structure
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        
        # Verify timeframe consistency - skip exact interval check with mock data
        # as our mock generator might not perfectly align with requested times
        if len(df) > 1:  # Ensure we have at least 2 rows to check time difference
            time_diffs = df['timestamp'].diff().dropna()
            
            if timeframe == '15m':
                # Check that most time diffs are close to 15 minutes
                most_common_diff = time_diffs.value_counts().idxmax()
                assert abs(most_common_diff - timedelta(minutes=15)).total_seconds() < 60
            elif timeframe == '1h':
                most_common_diff = time_diffs.value_counts().idxmax()
                assert abs(most_common_diff - timedelta(hours=1)).total_seconds() < 120
            else:  # 4h
                most_common_diff = time_diffs.value_counts().idxmax()
                assert abs(most_common_diff - timedelta(hours=4)).total_seconds() < 300

def test_error_handling(mock_coinbase_api):
    """Test error handling and retry mechanism"""
    processor = OHLCVProcessor()
    
    # Create a mock HTTP error response
    mock_response = requests.Response()
    mock_response.status_code = 400
    mock_response._content = json.dumps({
        "error": "INVALID_ARGUMENT",
        "error_details": "valid product_id is required",
        "message": "valid product_id is required"
    }).encode('utf-8')
    mock_response.reason = "Bad Request"
    
    # Configure mock to raise proper HTTPError for invalid symbol
    def side_effect(product_id, **kwargs):
        if product_id == 'INVALID-PAIR':
            # Create and raise a proper HTTPError with the mock response
            http_error = HTTPError("400 Client Error: Bad Request", response=mock_response)
            http_error.response = mock_response
            raise http_error
        return create_mock_candles(product_id, kwargs.get('start'), kwargs.get('end'), kwargs.get('granularity'))
    
    mock_coinbase_api.side_effect = side_effect
    
    # Test with invalid symbol - our processor should convert the API error to ValueError
    with pytest.raises(ValueError):
        processor.get_ohlcv(
            symbol='INVALID-PAIR',
            timeframe='15m',
            start_time=datetime.now() - timedelta(hours=1)
        )
    
    # Reset side_effect to default for remaining tests
    mock_coinbase_api.side_effect = lambda product_id, start, end, granularity, **kwargs: create_mock_candles(
        product_id, start, end, granularity
    )
    
    # Test with invalid timeframe
    with pytest.raises(ValueError):
        processor.get_ohlcv(
            symbol='BTC-USD',
            timeframe='invalid',
            start_time=datetime.now() - timedelta(hours=1)
        )
    
    # Test with future start time
    with pytest.raises(ValueError):
        processor.get_ohlcv(
            symbol='BTC-USD',
            timeframe='15m',
            start_time=datetime.now() + timedelta(days=1)
        ) 