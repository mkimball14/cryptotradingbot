import requests
import time
import hmac
import hashlib
import base64
import json
import uuid  # Added for nonce generation
from urllib.parse import urlencode

from .config import settings

class BloFinAPIClient:
    # Updated BASE_URL based on documentation
    BASE_URL = "https://openapi.blofin.com"
    # Optional: Add DEMO_BASE_URL if needed
    # DEMO_BASE_URL = "https://demo-trading-openapi.blofin.com"

    def __init__(self, use_demo=False):
        self.base_url = self.BASE_URL # Adjust if using demo
        self.api_key = settings.BLOFIN_API_KEY
        self.secret_key = settings.BLOFIN_SECRET_KEY
        self.passphrase = settings.BLOFIN_PASSPHRASE

        if not self.api_key or not self.secret_key or not self.passphrase:
            raise ValueError("BloFin API Key, Secret Key, and Passphrase must be set in .env")

    def _get_timestamp_ms(self) -> str:
        """Generates the required timestamp format (milliseconds) for BloFin API."""
        return str(int(time.time() * 1000))

    def _sign_request(self, method: str, request_path: str, body: str = ""):
        """Generates the signature components for an API request according to BloFin docs."""
        timestamp = self._get_timestamp_ms()
        nonce = str(uuid.uuid4())
        method_upper = method.upper()

        # Construct prehash string: requestPath + method + timestamp + nonce + body
        # Note: request_path must include query parameters for GET requests
        prehash = f"{request_path}{method_upper}{timestamp}{nonce}{body}"

        # Generate HMAC-SHA256 signature
        mac = hmac.new(bytes(self.secret_key, encoding='utf-8'), bytes(prehash, encoding='utf-8'), digestmod=hashlib.sha256)

        # Convert binary hash to hexadecimal string
        hex_signature = mac.hexdigest()

        # Base64 encode the hexadecimal string
        signature = base64.b64encode(bytes(hex_signature, 'utf-8')).decode('utf-8')

        return timestamp, nonce, signature

    def _make_request(self, method: str, endpoint: str, params: dict | None = None, data: dict | None = None):
        """Makes an authenticated request to the BloFin API."""
        full_url_path = endpoint # Path without base URL
        request_url = self.base_url + endpoint # Full URL for the request
        body_str = ""

        if params:
            query_string = urlencode(params)
            full_url_path += '?' + query_string
            request_url += '?' + query_string

        # For POST requests, use the JSON string body
        if method.upper() == 'POST' and data:
            body_str = json.dumps(data)
        # GET requests have an empty body string for signing
        elif method.upper() == 'GET':
            body_str = ""

        # Generate signature components using the path *with query params* for GET
        timestamp, nonce, signature = self._sign_request(method, full_url_path, body_str)

        # Updated headers based on documentation
        headers = {
            'ACCESS-KEY': self.api_key,
            'ACCESS-SIGN': signature,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-NONCE': nonce,
            'ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json; charset=utf-8' # Specify charset
            # Add any other required headers based on specific endpoints if needed
        }

        try:
            # Use request_url for the actual request
            response = requests.request(method, request_url, headers=headers, data=body_str.encode('utf-8'))
            # Check for specific BloFin error codes in the response body
            response_data = response.json()
            if isinstance(response_data, dict) and response_data.get('code') != '0': # Assuming '0' means success
                 print(f"BloFin API Error: Code={response_data.get('code')}, Msg={response_data.get('msg')}, Request: {method} {request_url}")
                 # Consider raising a custom exception here
                 return response_data # Return error details

            response.raise_for_status()  # Raise HTTPError for non-2xx responses not caught by BloFin codes
            return response_data

        except requests.exceptions.RequestException as e:
            print(f"HTTP Request Error making request to {request_url}: {e}")
            # Consider more robust error handling/logging
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON response from {request_url}: {response.text}")
            return None

    # --- Public Methods (Implement based on Task 1.3) ---
    def get_futures_account_balance(self):
        """Example: Fetch futures account balance."""
        # Example Endpoint from Docs: /api/v1/account/futures-balance
        # IMPORTANT: Verify actual endpoint path from documentation!
        endpoint = "/api/v1/account/futures-balance" # Replace with actual endpoint if different
        return self._make_request('GET', endpoint)

    def get_positions(self, inst_id: str | None = None):
        """Example: Fetch open positions."""
        # Example Endpoint from Docs: /api/v1/account/positions
        endpoint = "/api/v1/account/positions"
        params = {}
        if inst_id:
            params['instId'] = inst_id
        return self._make_request('GET', endpoint, params=params)

    # Add other methods like place_order, cancel_order, get_tickers etc.
    # based on the documentation and Task 1.3 requirements.