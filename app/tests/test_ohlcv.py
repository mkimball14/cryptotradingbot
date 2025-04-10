import pytest
import json
import pandas as pd
import datetime
from unittest.mock import AsyncMock, patch, MagicMock
import base64
import numpy as np
from datetime import timezone

from app.core.config import Settings
from app.core.coinbase import CoinbaseClient
from app.core.ohlcv import OHLCVFetcher, get_ohlcv, RateLimiter

@pytest.fixture
def settings():
    return Settings(
        COINBASE_API_KEY="test_key",
        COINBASE_API_SECRET=base64.b64encode(b"test_secret").decode(),
        COINBASE_API_PASSPHRASE="test_passphrase",
        DEBUG=False
    )

@pytest.fixture
def mock_client(settings):
    client = CoinbaseClient(settings)
    client.get_product_candles = AsyncMock()
    return client

@pytest.fixture
def sample_candles():
    """Sample candle data for testing"""
    return [
        {
            "start": "2024-01-01T00:00:00Z",
            "low": "29000.00",
            "high": "29500.00",
            "open": "29100.00",
            "close": "29400.00",
            "volume": "150.5"
        },
        {
            "start": "2024-01-01T01:00:00Z",
            "low": "29300.00",
            "high": "29800.00",
            "open": "29400.00",
            "close": "29700.00",
            "volume": "220.3"
        },
        {
            "start": "2024-01-01T02:00:00Z",
            "low": "29600.00",
            "high": "30100.00",
            "open": "29700.00",
            "close": "30000.00",
            "volume": "310.8"
        }
    ]

@pytest.mark.asyncio
async def test_rate_limiter():
    """Test the rate limiter functionality"""
    rate_limiter = RateLimiter(calls_per_second=10)
    
    # Record the start time
    start_time = datetime.datetime.now()
    
    # Call wait() multiple times
    for _ in range(5):
        await rate_limiter.wait()
    
    # Calculate the elapsed time
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    
    # For 5 calls at 10 calls/sec, elapsed time should be at least 0.4 seconds
    # (considering the first call doesn't wait)
    assert elapsed < 0.5, "Rate limiter waited too long"
    assert elapsed > 0.3, "Rate limiter didn't wait enough"

@pytest.mark.asyncio
async def test_get_ohlcv_success(mock_client, sample_candles):
    """Test successful OHLCV data retrieval with data cleaning"""
    # Set up mock response
    mock_client.get_product_candles.return_value = sample_candles
    
    # Create fetcher instance
    fetcher = OHLCVFetcher(mock_client)
    
    # Test with data cleaning enabled (default)
    df = await fetcher.get_ohlcv("BTC-USD", "1h", 100)
    
    # Verify API call
    mock_client.get_product_candles.assert_called_once()
    args = mock_client.get_product_candles.call_args[1]
    assert args["product_id"] == "BTC-USD"
    assert args["granularity"] == "ONE_HOUR"
    
    # Verify DataFrame structure and data cleaning
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert all(col in df.columns for col in [
        "timestamp", "open", "high", "low", "close", "volume",
        "typical_price", "body_size", "upper_shadow", "lower_shadow",
        "price_change", "returns", "volume_ma", "volume_std", "is_doji"
    ])
    
    # Test data types
    assert pd.api.types.is_datetime64_dtype(df['timestamp'])
    assert all(pd.api.types.is_float_dtype(df[col]) for col in ['open', 'high', 'low', 'close', 'volume'])
    
    # Test calculated fields
    assert df['typical_price'].equals((df['high'] + df['low'] + df['close']) / 3)
    assert df['body_size'].equals(abs(df['close'] - df['open']))
    
    # Test without data cleaning
    raw_df = await fetcher.get_ohlcv("BTC-USD", "1h", 100, clean_data=False)
    assert len(raw_df.columns) == 6  # Only original columns
    assert all(col in raw_df.columns for col in ["timestamp", "open", "high", "low", "close", "volume"])

@pytest.mark.asyncio
async def test_get_ohlcv_empty_response(mock_client):
    """Test handling of empty response"""
    mock_client.get_product_candles.return_value = []
    fetcher = OHLCVFetcher(mock_client)
    
    df = await fetcher.get_ohlcv("BTC-USD", "1h")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert list(df.columns) == ["timestamp", "open", "high", "low", "close", "volume"]

@pytest.mark.asyncio
async def test_get_ohlcv_invalid_timeframe(mock_client):
    """Test handling of invalid timeframe"""
    fetcher = OHLCVFetcher(mock_client)
    
    with pytest.raises(ValueError) as excinfo:
        await fetcher.get_ohlcv("BTC-USD", "2h")
    assert "Invalid timeframe" in str(excinfo.value)

@pytest.mark.asyncio
async def test_get_ohlcv_date_handling(mock_client, sample_candles):
    """Test date handling in OHLCV fetcher"""
    mock_client.get_product_candles.return_value = sample_candles
    fetcher = OHLCVFetcher(mock_client)
    
    # Test with datetime objects
    start_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_time = datetime(2024, 1, 2, tzinfo=timezone.utc)
    
    await fetcher.get_ohlcv(
        "BTC-USD",
        "1h",
        start_time=start_time,
        end_time=end_time
    )
    
    args = mock_client.get_product_candles.call_args[1]
    assert args["start"] == "2024-01-01T00:00:00+00:00"
    assert args["end"] == "2024-01-02T00:00:00+00:00"
    
    # Test with ISO strings
    await fetcher.get_ohlcv(
        "BTC-USD",
        "1h",
        start_time="2024-01-01T00:00:00Z",
        end_time="2024-01-02T00:00:00Z"
    )
    
    args = mock_client.get_product_candles.call_args[1]
    assert args["start"] == "2024-01-01T00:00:00Z"
    assert args["end"] == "2024-01-02T00:00:00Z"

@pytest.mark.asyncio
async def test_get_ohlcv_limit(mock_client):
    """Test limit parameter handling"""
    # Create sample data with more candles
    sample_data = [
        {
            "start": f"2024-01-01T{i:02d}:00:00Z",
            "low": "29000.00",
            "high": "29500.00",
            "open": "29100.00",
            "close": "29400.00",
            "volume": "150.5"
        } for i in range(10)
    ]
    
    mock_client.get_product_candles.return_value = sample_data
    fetcher = OHLCVFetcher(mock_client)
    
    # Test with limit less than data size
    df = await fetcher.get_ohlcv("BTC-USD", "1h", limit=5)
    assert len(df) == 5
    
    # Test with limit greater than data size
    df = await fetcher.get_ohlcv("BTC-USD", "1h", limit=20)
    assert len(df) == 10

@pytest.mark.asyncio
async def test_get_ohlcv_data_cleaning(mock_client):
    """Test data cleaning with problematic data"""
    # Create sample data with issues
    problematic_data = [
        {
            "start": "2024-01-01T00:00:00Z",
            "low": "29000.00",
            "high": "28000.00",  # Invalid high < low
            "open": "29100.00",
            "close": "29400.00",
            "volume": "150.5"
        },
        {
            "start": "2024-01-01T01:00:00Z",
            "low": "29300.00",
            "high": "29800.00",
            "open": "nan",  # Missing value
            "close": "29700.00",
            "volume": "220.3"
        }
    ]
    
    mock_client.get_product_candles.return_value = problematic_data
    fetcher = OHLCVFetcher(mock_client)
    
    # Test with data cleaning enabled
    df = await fetcher.get_ohlcv("BTC-USD", "1h", clean_data=True)
    
    # Verify data cleaning results
    assert not df.isnull().any().any()  # No NaN values
    assert all(df['high'] >= df['low'])  # High/low violations fixed
    
    # Test with data cleaning disabled
    df_raw = await fetcher.get_ohlcv("BTC-USD", "1h", clean_data=False)
    assert df_raw.isnull().any().any()  # Should still contain NaN values

@pytest.mark.asyncio
async def test_utility_function(mock_client, sample_candles):
    """Test the utility function wrapper"""
    mock_client.get_product_candles.return_value = sample_candles
    
    # Test with default parameters
    df = await get_ohlcv(mock_client, "BTC-USD")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(sample_candles)
    
    # Test with custom parameters
    df = await get_ohlcv(
        client=mock_client,
        symbol="BTC-USD",
        timeframe="1h",
        limit=10,
        start_time="2024-01-01T00:00:00Z",
        end_time="2024-01-02T00:00:00Z",
        clean_data=True
    )
    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(sample_candles)
    assert all(col in df.columns for col in [
        "timestamp", "open", "high", "low", "close", "volume",
        "typical_price", "body_size", "upper_shadow", "lower_shadow"
    ]) 