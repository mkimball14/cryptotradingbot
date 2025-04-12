import os
import sys
import json
import requests
import urllib.parse
from datetime import datetime, timezone
import pandas as pd

try:
    from coinbase import jwt_generator
except ImportError:
    print("Error: coinbase module not found. Please install with 'pip install coinbase'")
    sys.exit(1)

# Load API keys from .env file manually
key_name = "organizations/3d4c3ac1-5ed0-400a-8f61-c2571d877bf8/apiKeys/36b41c78-3173-4b10-9dbd-13934a34e07f"
private_key = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEINQMpf3Api4XuCCOTfWZSLQw7mtLo23vSUesMp1lAurYoAoGCCqGSM49
AwEHoUQDQgAEGK4qtbP0qXOWc0CWkqK7e9xm3oXLvg34+dptaPfsgswBzTs639tY
y1C2L3QoUI2zsNf06CRT9PE3vtc8N/maTg==
-----END EC PRIVATE KEY-----"""

def make_coinbase_request(jwt_token, endpoint, params=None):
    """
    Make an authenticated request to Coinbase API using JWT token.
    """
    base_url = "https://api.coinbase.com"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}{endpoint}"
    print(f"Sending request to: {url}")
    print(f"With params: {params}")
    print(f"Headers: {headers}")
    
    response = requests.get(url, headers=headers, params=params)
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {response.headers}")
    
    # Print response content for debugging
    print(f"Response content: {response.text[:1000]}...")
    
    try:
        return response.json()
    except:
        return {"error": "Invalid JSON response", "text": response.text}

def main():
    # Test with the candles endpoint
    symbol = "BTC-USD"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    granularity = "ONE_HOUR"
    
    # Convert dates to ISO 8601 format
    start_dt = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
    end_dt = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()
    
    # Convert granularity to seconds
    granularity_map = {
        "ONE_MINUTE": 60,
        "FIVE_MINUTE": 300,
        "FIFTEEN_MINUTE": 900,
        "ONE_HOUR": 3600,
        "SIX_HOUR": 21600,
        "ONE_DAY": 86400
    }
    granularity_seconds = granularity_map.get(granularity, 3600)
    
    # Prepare parameters
    params = {
        "granularity": granularity_seconds,
        "start": start_iso,
        "end": end_iso
    }
    
    # Build endpoint path with query params included for JWT
    endpoint = f"/api/v3/brokerage/products/{symbol}/candles"
    
    # Format query string for JWT URI
    query_parts = []
    for key in sorted(params.keys()):
        encoded_key = urllib.parse.quote(str(key))
        encoded_value = urllib.parse.quote(str(params[key]))
        query_parts.append(f"{encoded_key}={encoded_value}")
    query_string = "&".join(query_parts)
    
    # Create the full URI for JWT generation - including query params
    request_method = "GET"
    jwt_uri = f"{request_method} {endpoint}?{query_string}"
    print(f"JWT URI: {jwt_uri}")
    
    # Generate JWT token
    try:
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, key_name, private_key)
        print(f"JWT Token (first 50 chars): {jwt_token[:50]}...")
        
        # Make the request
        candles_data = make_coinbase_request(jwt_token, endpoint, params)
        
        if isinstance(candles_data, list) and len(candles_data) > 0:
            print(f"Successfully fetched {len(candles_data)} candles!")
            print(f"First few candles: {json.dumps(candles_data[:5], indent=2)}")
            
            # Try to convert to DataFrame
            try:
                df = pd.DataFrame(candles_data, columns=['timestamp', 'low', 'high', 'open', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
                df.set_index('timestamp', inplace=True)
                print(f"\nSample data as DataFrame:\n{df.head()}")
            except Exception as e:
                print(f"Error converting to DataFrame: {e}")
        else:
            print(f"Got unexpected response format: {candles_data}")
            
    except Exception as e:
        print(f"Error testing candles endpoint: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 