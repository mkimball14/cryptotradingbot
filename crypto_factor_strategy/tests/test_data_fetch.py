#!/usr/bin/env python3
"""
Coinbase Data Fetch Test

This script tests fetching historical OHLCV data from the Coinbase API
using the configured credentials.
"""

import os
import time
import json
from datetime import datetime, timezone, timedelta
import pandas as pd
from dotenv import load_dotenv

# Try to import the REST client from coinbase library
try:
    from coinbase.rest import RESTClient
except ImportError:
    print("Error: The python-coinbase-advanced package is not installed.")
    print("Install it with: pip install python-coinbase-advanced")
    exit(1)

def get_coinbase_client():
    """Initialize and return a Coinbase REST client using API credentials from .env file."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API credentials
    api_key = os.getenv("COINBASE_API_KEY")
    private_key = os.getenv("COINBASE_PRIVATE_KEY")
    
    if not api_key or not private_key:
        print("Error: Coinbase API credentials not found in .env file.")
        print("Make sure COINBASE_API_KEY and COINBASE_PRIVATE_KEY are set.")
        return None
    
    try:
        # Initialize the REST client
        client = RESTClient(api_key=api_key, api_secret=private_key)
        return client
    except Exception as e:
        print(f"Error initializing Coinbase client: {str(e)}")
        return None

def fetch_product_data(symbol, days=7):
    """Fetch OHLCV data for a specific product (trading pair) from Coinbase."""
    # Initialize the client
    client = get_coinbase_client()
    if not client:
        return None
    
    # Calculate time range (last N days)
    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=days)
    
    # Convert to timestamps
    start_ts = int(start_dt.timestamp())
    end_ts = int(end_dt.timestamp())
    
    print(f"Fetching {days} days of data for {symbol}...")
    print(f"Time range: {start_dt.isoformat()} to {end_dt.isoformat()}")
    
    try:
        # Make the API request
        candles = client.get_candles(
            product_id=symbol,
            start=str(start_ts),
            end=str(end_ts),
            granularity="ONE_DAY"
        )
        
        if 'candles' not in candles or not candles['candles']:
            print(f"No data returned for {symbol}")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(candles['candles'])
        
        # Convert timestamp to datetime
        df['start'] = pd.to_datetime(df['start'].astype(int), unit='s', utc=True)
        
        # Rename columns
        df = df.rename(columns={
            'start': 'timestamp',
            'low': 'low', 
            'high': 'high',
            'open': 'open', 
            'close': 'close', 
            'volume': 'volume'
        })
        
        # Sort by date
        df = df.sort_values('timestamp')
        
        # Set timestamp as index
        df.set_index('timestamp', inplace=True)
        
        return df
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def main():
    """Main function to test data fetching."""
    print("Coinbase Data Fetch Test")
    print("=======================")
    
    # List of symbols to test
    symbols = ["BTC-USD", "ETH-USD", "SOL-USD"]
    days = 7
    
    for symbol in symbols:
        # Fetch data
        df = fetch_product_data(symbol, days)
        
        if df is not None:
            print(f"\n✅ Successfully fetched data for {symbol}:")
            print(f"  - Data shape: {df.shape}")
            print(f"  - Date range: {df.index.min()} to {df.index.max()}")
            print(f"  - Latest close price: {df['close'].iloc[-1]}")
            
            # Display last 3 days of data
            print("\nLast 3 days of data:")
            print(df.tail(3))
        else:
            print(f"\n❌ Failed to fetch data for {symbol}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    main() 