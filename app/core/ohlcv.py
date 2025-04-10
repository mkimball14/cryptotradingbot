import asyncio
import datetime
import time
from typing import Dict, List, Optional, Union, Any
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

from app.core.config import Settings
from app.core.coinbase import CoinbaseClient, CoinbaseError
from app.core.data_processor import OHLCVProcessor

class RateLimiter:
    """Rate limiter to prevent API throttling"""
    
    def __init__(self, calls_per_second: int = 3):
        """
        Initialize rate limiter
        
        Args:
            calls_per_second: Maximum number of calls allowed per second
        """
        self.calls_per_second = calls_per_second
        self.last_call_time = 0
        self.min_interval = 1.0 / calls_per_second
        
    async def wait(self):
        """Wait if necessary to comply with rate limits"""
        current_time = time.time()
        elapsed = current_time - self.last_call_time
        
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            await asyncio.sleep(wait_time)
            
        self.last_call_time = time.time()

class OHLCVFetcher:
    """Fetch OHLCV (candle) data from Coinbase API"""
    
    # Map Coinbase granularity values to more user-friendly timeframe names
    TIMEFRAME_MAP = {
        "1m": "ONE_MINUTE",
        "5m": "FIVE_MINUTE",
        "15m": "FIFTEEN_MINUTE",
        "1h": "ONE_HOUR",
        "6h": "SIX_HOUR",
        "1d": "ONE_DAY"
    }
    
    def __init__(self, client: CoinbaseClient):
        """
        Initialize OHLCV fetcher
        
        Args:
            client: Authenticated CoinbaseClient instance
        """
        self.client = client
        self.rate_limiter = RateLimiter()
        self.processor = OHLCVProcessor(decimal_places=8)  # Use 8 decimal places for crypto prices
    
    @retry(
        retry=retry_if_exception_type((httpx.RequestError, CoinbaseError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def get_ohlcv(
        self, 
        symbol: str, 
        timeframe: str = "1h", 
        limit: int = 100,
        start_time: Optional[Union[str, datetime.datetime]] = None,
        end_time: Optional[Union[str, datetime.datetime]] = None,
        clean_data: bool = True
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data from Coinbase
        
        Args:
            symbol: Trading pair symbol (e.g., "BTC-USD")
            timeframe: Candle timeframe (e.g., "1m", "5m", "15m", "1h", "6h", "1d")
            limit: Maximum number of candles to retrieve
            start_time: Start time for data (ISO format string or datetime object)
            end_time: End time for data (ISO format string or datetime object)
            clean_data: Whether to clean and normalize the data (default: True)
            
        Returns:
            pandas.DataFrame: OHLCV data with columns [timestamp, open, high, low, close, volume]
            If clean_data is True, additional columns will be added with technical indicators
            
        Raises:
            ValueError: If timeframe is invalid
            CoinbaseError: If API request fails
        """
        # Validate timeframe
        granularity = self.TIMEFRAME_MAP.get(timeframe)
        if not granularity:
            raise ValueError(f"Invalid timeframe: {timeframe}. Valid options: {', '.join(self.TIMEFRAME_MAP.keys())}")
            
        # Format start/end times
        if start_time:
            if isinstance(start_time, datetime.datetime):
                start_time = start_time.isoformat()
        
        if end_time:
            if isinstance(end_time, datetime.datetime):
                end_time = end_time.isoformat()
                
        # Use current time as end_time if not provided
        if not end_time:
            end_time = datetime.datetime.utcnow().isoformat()
            
        # Apply rate limiting
        await self.rate_limiter.wait()
        
        try:
            # Fetch candles from Coinbase API
            candles = await self.client.get_product_candles(
                product_id=symbol,
                start=start_time,
                end=end_time,
                granularity=granularity
            )
            
            # Check for empty response
            if not candles:
                return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
                
            # Process response into a DataFrame
            data = []
            for candle in candles:
                # Check if we're getting the new Exchange API format or the Advanced Trade API format
                if isinstance(candle, dict):
                    # Advanced Trade API format (dict with keys)
                    data.append({
                        "timestamp": pd.to_datetime(candle["start"], utc=True),
                        "open": float(candle["open"]),
                        "high": float(candle["high"]),
                        "low": float(candle["low"]),
                        "close": float(candle["close"]),
                        "volume": float(candle["volume"])
                    })
                else:
                    # Exchange API format (list with values)
                    timestamp, low, high, open_price, close, volume = candle
                    data.append({
                        "timestamp": pd.to_datetime(timestamp, unit='s', utc=True),
                        "open": float(open_price),
                        "high": float(high),
                        "low": float(low),
                        "close": float(close),
                        "volume": float(volume)
                    })
                
            # Create DataFrame and sort by timestamp
            df = pd.DataFrame(data)
            df = df.sort_values("timestamp").reset_index(drop=True)
            
            # Limit number of candles if needed
            if limit and len(df) > limit:
                df = df.tail(limit)
                
            # Clean and process data if requested
            if clean_data and not df.empty:
                try:
                    df = self.processor.process_ohlcv(df)
                except Exception as e:
                    logger.warning(f"Error processing OHLCV data: {str(e)}. Returning raw data.")
                
            return df
            
        except CoinbaseError as e:
            logger.error(f"Coinbase API error: {str(e)}")
            raise
        except httpx.RequestError as e:
            logger.error(f"HTTP request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

async def get_ohlcv(
    client: CoinbaseClient,
    symbol: str,
    timeframe: str = "1h",
    limit: int = 100,
    start_time: Optional[Union[str, datetime.datetime]] = None,
    end_time: Optional[Union[str, datetime.datetime]] = None,
    clean_data: bool = True
) -> pd.DataFrame:
    """
    Utility function to fetch OHLCV data
    
    Args:
        client: Authenticated CoinbaseClient instance
        symbol: Trading pair symbol (e.g., "BTC-USD")
        timeframe: Candle timeframe (e.g., "1m", "5m", "15m", "1h", "6h", "1d")
        limit: Maximum number of candles to retrieve
        start_time: Start time for data (ISO format string or datetime object)
        end_time: End time for data (ISO format string or datetime object)
        clean_data: Whether to clean and normalize the data (default: True)
        
    Returns:
        pandas.DataFrame: OHLCV data with columns [timestamp, open, high, low, close, volume]
        If clean_data is True, additional columns will be added with technical indicators
    """
    fetcher = OHLCVFetcher(client)
    return await fetcher.get_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit,
        start_time=start_time,
        end_time=end_time,
        clean_data=clean_data
    ) 