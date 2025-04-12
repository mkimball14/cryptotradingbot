import os
import sys
import json
import requests

try:
    from coinbase import jwt_generator
except ImportError:
    print("Error: coinbase module not found. Please install with 'pip install coinbase'")
    sys.exit(1)

# Load API keys from .env file manually 
# You can adjust this to use your Settings class if preferred
key_name = "organizations/3d4c3ac1-5ed0-400a-8f61-c2571d877bf8/apiKeys/36b41c78-3173-4b10-9dbd-13934a34e07f"
private_key = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEINQMpf3Api4XuCCOTfWZSLQw7mtLo23vSUesMp1lAurYoAoGCCqGSM49
AwEHoUQDQgAEGK4qtbP0qXOWc0CWkqK7e9xm3oXLvg34+dptaPfsgswBzTs639tY
y1C2L3QoUI2zsNf06CRT9PE3vtc8N/maTg==
-----END EC PRIVATE KEY-----"""

def make_coinbase_request(jwt_token, endpoint):
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
    print(f"Headers: {headers}")
    
    response = requests.get(url, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {response.headers}")
    
    # Print response content for debugging
    print(f"Response content: {response.text[:1000]}...")
    
    try:
        return response.json()
    except:
        return {"error": "Invalid JSON response", "text": response.text}

def main():
    # First test with v2 API (which seems more consistent)
    request_method = "GET"
    request_path = "/v2/accounts"  # Common v2 endpoint
    
    print(f"Testing v2 API endpoint: {request_path}")
    try:
        # Generate JWT for the v2 endpoint
        jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
        print(f"JWT URI: {jwt_uri}")
        
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, key_name, private_key)
        print(f"JWT Token (first 50 chars): {jwt_token[:50]}...")
        
        # Make the request
        accounts = make_coinbase_request(jwt_token, request_path)
        print("v2 Accounts response:", json.dumps(accounts, indent=2))
    except Exception as e:
        print(f"Error testing v2 endpoint: {e}")
        import traceback
        print(traceback.format_exc())
        
    # Then test with v3 API (Advanced Trade)
    print("\n" + "-"*50 + "\n")
    request_method = "GET"
    request_path = "/api/v3/brokerage/products"  # Advanced Trade endpoint
    
    print(f"Testing v3 API endpoint: {request_path}")
    try:
        # Generate JWT for the v3 endpoint
        jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
        print(f"JWT URI: {jwt_uri}")
        
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, key_name, private_key)
        print(f"JWT Token (first 50 chars): {jwt_token[:50]}...")
        
        # Make the request
        products = make_coinbase_request(jwt_token, request_path)
        print("v3 Products response:", json.dumps(products, indent=2))
    except Exception as e:
        print(f"Error testing v3 endpoint: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 