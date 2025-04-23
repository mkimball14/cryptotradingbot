#!/usr/bin/env python3
"""
Data Fetcher Module

This module provides helper functions for fetching cryptocurrency historical data
using VectorBT's YFData interface, with fallback to Coinbase API when needed.
"""

import os
import time
import json
import logging
import traceback
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import vectorbtpro for YFData
try:
    import vectorbtpro as vbt
    HAS_VECTORBT = True
except ImportError:
    # Fallback to using vectorbt if vectorbtpro is not available
    try:
        import vectorbt as vbt
        HAS_VECTORBT = True
    except ImportError:
        HAS_VECTORBT = False
        print("Warning: Neither vectorbtpro nor vectorbt is available. Some features will be limited.")

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configure console handler if not already configured
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Mapping between YFData timeframes and Coinbase granularity values
TIMEFRAME_MAP = {
    "1m": "ONE_MINUTE",
    "5m": "FIVE_MINUTE", 
    "15m": "FIFTEEN_MINUTE",
    "30m": "THIRTY_MINUTE",
    "1h": "ONE_HOUR",
    "2h": "TWO_HOUR",
    "6h": "SIX_HOUR",
    "1d": "ONE_DAY"
}

def get_products():
    """
    Get common cryptocurrency product pairs available on both Yahoo Finance and Coinbase.
    
    Returns:
        list: List of product dictionaries with product_id and display_name fields
    """
    # Common crypto pairs that should be available on both platforms
    common_pairs = [
        {"product_id": "BTC-USD", "display_name": "Bitcoin USD"},
        {"product_id": "ETH-USD", "display_name": "Ethereum USD"},
        {"product_id": "SOL-USD", "display_name": "Solana USD"},
        {"product_id": "XRP-USD", "display_name": "Ripple USD"},
        {"product_id": "ADA-USD", "display_name": "Cardano USD"},
        {"product_id": "DOGE-USD", "display_name": "Dogecoin USD"},
        {"product_id": "DOT-USD", "display_name": "Polkadot USD"},
        {"product_id": "MATIC-USD", "display_name": "Polygon USD"},
        {"product_id": "LINK-USD", "display_name": "Chainlink USD"},
        {"product_id": "UNI-USD", "display_name": "Uniswap USD"},
        {"product_id": "AVAX-USD", "display_name": "Avalanche USD"},
        {"product_id": "AAVE-USD", "display_name": "Aave USD"},
        {"product_id": "LTC-USD", "display_name": "Litecoin USD"},
        {"product_id": "BCH-USD", "display_name": "Bitcoin Cash USD"},
        {"product_id": "ALGO-USD", "display_name": "Algorand USD"}
    ]
    
    logger.info(f"Retrieved {len(common_pairs)} common cryptocurrency pairs")
    return common_pairs

def get_candles(product_id, start_time, end_time, granularity):
    """
    Get historical candle data for a product using YFData.
    
    Args:
        product_id (str): Product ID (e.g., 'BTC-USD')
        start_time (datetime or str): Start time for candles
        end_time (datetime or str): End time for candles
        granularity (str): Granularity of candles (ONE_MINUTE, FIVE_MINUTE, etc.)
        
    Returns:
        list: List of candle data or empty list if request failed
    """
    try:
        # Check if VectorBT is available
        if not HAS_VECTORBT:
            logger.error("VectorBT is not available. Cannot fetch historical data.")
            return []
        
        # Convert Coinbase granularity to YFData timeframe
        # Reverse lookup in the mapping
        timeframe = None
        for tf, gran in TIMEFRAME_MAP.items():
            if gran == granularity:
                timeframe = tf
                break
        
        if not timeframe:
            logger.error(f"Unsupported granularity: {granularity}")
            return []
        
        # Format symbol for YFData (use as-is, YFData handles 'BTC-USD' format)
        symbol = product_id
        
        # Make sure start_time and end_time are datetime objects
        if isinstance(start_time, str):
            try:
                # Try to parse ISO format
                from datetime import datetime
                start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            except ValueError:
                logger.error(f"Invalid start_time format: {start_time}")
                return []
        
        if isinstance(end_time, str):
            try:
                # Try to parse ISO format
                from datetime import datetime
                end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            except ValueError:
                logger.error(f"Invalid end_time format: {end_time}")
                return []
        
        logger.info(f"Fetching {timeframe} data for {symbol} from {start_time} to {end_time}")
        
        # Download data using YFData
        ohlcv = vbt.YFData.download(
            symbol, 
            start=start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end=end_time.strftime('%Y-%m-%d %H:%M:%S'),
            timeframe=timeframe
        ).get()
        
        if ohlcv is None or ohlcv.empty:
            logger.warning(f"No data returned for {symbol}")
            return []
        
        # Convert to the format expected by the application
        candles = []
        for timestamp, row in ohlcv.iterrows():
            # Convert to Coinbase API response format
            candle = {
                "start": int(timestamp.timestamp()),
                "low": float(row['Low']),
                "high": float(row['High']),
                "open": float(row['Open']),
                "close": float(row['Close']),
                "volume": float(row['Volume'])
            }
            candles.append(candle)
        
        logger.info(f"Retrieved {len(candles)} candles for {product_id}")
        return candles
            
    except Exception as e:
        logger.error(f"Error in get_candles: {str(e)}")
        logger.error(traceback.format_exc())
        return []

# Simple test code
if __name__ == "__main__":
    try:
        print("Testing Data Fetcher")
        print("==========================")
        
        print("==========================")
        print("\nGetting products...")
        products = get_products()
        
        if products:
            print(f"✅ Successfully retrieved {len(products)} products")
            print("\nFirst 3 products:")
            for product in products[:3]:
                print(f"  {product.get('product_id', 'Unknown')}: {product.get('display_name', 'Unknown')}")
        else:
            print("❌ Failed to retrieve products")
        
        print("\n==========================")
        print("\nGetting candles for BTC-USD...")
        
        # Calculate time range for candles (last 3 days)
        from datetime import datetime, timedelta
        
        end_time = datetime.now()
        start_time = end_time - timedelta(days=3)
        
        candles = get_candles("BTC-USD", start_time, end_time, "ONE_DAY")
        
        if candles:
            print(f"✅ Successfully retrieved {len(candles)} candles")
            if candles:
                # Display the latest candle
                print("\nLatest candle:")
                latest = candles[0]  # Usually the first one is the most recent
                print(f"  Start: {latest.get('start')}")
                print(f"  Low: {latest.get('low')}")
                print(f"  High: {latest.get('high')}")
                print(f"  Open: {latest.get('open')}")
                print(f"  Close: {latest.get('close')}")
                print(f"  Volume: {latest.get('volume')}")
        else:
            print(f"❌ Failed to retrieve candles")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        traceback.print_exc() 