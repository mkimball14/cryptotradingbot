import hmac
import hashlib
import time
import base64
import json
import requests
import sys

# Get credentials from .env
api_key = 'organizations/3d4c3ac1-5ed0-400a-8f61-c2571d877bf8/apiKeys/cddb37c8-9861-4754-9e25-8ac50e0edb17'
api_secret = 'MHcCAQEEIGApfaJBdEkooKWqdYGw5Yqb+j2q5F6hKJuTQ+4TiMnYoAoGCCqGSM49AwEHoUQDQgAEl/YoXnvVYmfoy1YsvJ/o2c1pZhUrcSrhrtIlfRGFl2ugToe2+XtMU+Ije7riM+NMNH640GL1/bXEbHDtlAguAg=='
passphrase = 'your_passphrase_here'

try:
    # Generate signature for the request
    url = 'https://api.exchange.coinbase.com/products'
    timestamp = str(int(time.time()))
    method = 'GET'
    path = '/products'
    body = ''
    
    print(f'Testing connection to {url}')
    print(f'API Key: {api_key[:10]}...')
    print(f'API Secret length: {len(api_secret)}')
    
    # Test base64 decoding
    try:
        secret_key = base64.b64decode(api_secret)
        print(f'Successfully decoded API secret, length: {len(secret_key)}')
    except Exception as e:
        print(f'Error decoding API secret: {str(e)}')
        sys.exit(1)
    
    # Create signature
    message = f'{timestamp}{method}{path}{body}'
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
    response = requests.get(url, headers=headers)
    
    print(f'Response status code: {response.status_code}')
    if response.status_code == 200:
        print('Connection successful!')
        data = response.json()
        print(f'Found {len(data)} products')
        # Print a few sample products for verification
        for product in data[:3]:
            print(f"Product ID: {product.get('id', 'unknown')}")
    else:
        print(f'Error: {response.text}')
except Exception as e:
    print(f'Unexpected error: {str(e)}') 