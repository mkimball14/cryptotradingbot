import hmac
import hashlib
import time
import base64
import json
import requests
import sys
from datetime import datetime, timedelta

# Get credentials from .env
api_key = 'organizations/3d4c3ac1-5ed0-400a-8f61-c2571d877bf8/apiKeys/cddb37c8-9861-4754-9e25-8ac50e0edb17'
api_secret = 'MHcCAQEEIGApfaJBdEkooKWqdYGw5Yqb+j2q5F6hKJuTQ+4TiMnYoAoGCCqGSM49AwEHoUQDQgAEl/YoXnvVYmfoy1YsvJ/o2c1pZhUrcSrhrtIlfRGFl2ugToe2+XtMU+Ije7riM+NMNH640GL1/bXEbHDtlAguAg=='
passphrase = 'your_passphrase_here'

try:
    # Generate signature for the request
    symbol = 'BTC-USD'
    granularity = 3600  # 1 hour in seconds
    
    # Set time parameters
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=10)  # Get last 10 hours of data
    
    # Format timestamps for Coinbase API
    start_str = start_time.isoformat()
    end_str = end_time.isoformat()
    
    url = f'https://api.exchange.coinbase.com/products/{symbol}/candles'
    params = {
        'granularity': granularity,
        'start': start_str,
        'end': end_str
    }
    
    timestamp = str(int(time.time()))
    method = 'GET'
    path = f'/products/{symbol}/candles'
    body = ''
    
    print(f'Testing candle data fetch for {symbol}')
    print(f'API Key: {api_key[:10]}...')
    print(f'Timeframe: 1h (granularity={granularity})')
    print(f'Start: {start_str}')
    print(f'End: {end_str}')
    
    # Test base64 decoding
    try:
        secret_key = base64.b64decode(api_secret)
        print(f'Successfully decoded API secret, length: {len(secret_key)}')
    except Exception as e:
        print(f'Error decoding API secret: {str(e)}')
        sys.exit(1)
    
    # Create signature (with params in query string)
    query_string = f'?granularity={granularity}&start={start_str}&end={end_str}'
    message = f'{timestamp}{method}{path}{query_string}{body}'
    signature = hmac.new(secret_key, message.encode('utf-8'), hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    
    # Headers
    headers = {
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }
    
    # Make request
    print('Making API request...')
    response = requests.get(url, headers=headers, params=params)
    
    print(f'Response status code: {response.status_code}')
    if response.status_code == 200:
        print('Connection successful!')
        data = response.json()
        print(f'Received {len(data)} candles')
        
        # Print a few sample candles
        print("\nSample candles (time, low, high, open, close, volume):")
        for candle in data[:3]:
            timestamp, low, high, open_price, close, volume = candle
            time_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{time_str}: Open={open_price}, High={high}, Low={low}, Close={close}, Volume={volume}")
    else:
        print(f'Error: {response.text}')
except Exception as e:
    print(f'Unexpected error: {str(e)}') 