import hmac
import hashlib
import time
import base64
import json
import logging
from typing import Dict, Optional, List, Union, Any
from datetime import datetime, timedelta, timezone
import httpx
from app.core.config import Settings
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import urllib.parse  # Import for URL encoding
import secrets  # Import for generating nonce

# Import consolidated models and enums
from app.models.order import OrderSide, OrderType, OrderStatus, TimeInForce, OrderBase, MarketOrder, LimitOrder # Assuming these cover needed Order details
from app.models.position import Position

# Get logger
logger = logging.getLogger(__name__)

class CoinbaseError(Exception):
    """Base exception for Coinbase API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

class CoinbaseClient:
    def __init__(self, settings: Settings):
        """
        Initialize Coinbase API client with settings
        
        Args:
            settings (Settings): Application settings containing API credentials
        """
        self.settings = settings
        self.key_name = settings.COINBASE_JWT_KEY_NAME
        self.private_key_pem = settings.COINBASE_JWT_PRIVATE_KEY
        self.api_url = settings.COINBASE_API_URL

        # Load the private key
        try:
            self.private_key = serialization.load_pem_private_key(
                self.private_key_pem.encode('utf-8'),
                password=None
            )
            if not isinstance(self.private_key, ec.EllipticCurvePrivateKey):
                 raise TypeError("Loaded key is not an EC private key.")
        except Exception as e:
            logger.error(f"Failed to load private key: {e}")
            raise CoinbaseError(f"Invalid private key format or content: {e}")
        
    def _generate_jwt(self, method: str, uri: str, body: str = "") -> str:
        """
        Generate a JWT for API request authentication according to Coinbase Advanced Trade API specs.
        
        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            uri (str): Request URI (e.g., "/api/v3/brokerage/orders").
            body (str): Request body (empty string for GET requests).
            
        Returns:
            str: The generated JWT.
        """
        timestamp = int(time.time())
        
        # Build the URI in the format required by Coinbase
        # Extract host from API URL
        host = urllib.parse.urlparse(self.api_url).netloc
        
        # Get the API path from the URL (like "/api/v3/brokerage")
        api_path = urllib.parse.urlparse(self.api_url).path
        
        # Make sure we have the full path for the URI by combining the API path and the endpoint
        full_path = api_path
        if uri:
            # Ensure no double slashes
            if uri.startswith('/') and api_path.endswith('/'):
                full_path = f"{api_path}{uri[1:]}"
            elif not uri.startswith('/') and not api_path.endswith('/'):
                full_path = f"{api_path}/{uri}"
            else:
                full_path = f"{api_path}{uri}"
        
        # Format the URI as "METHOD host/path" according to Coinbase docs
        full_uri = f"{method.upper()} {host}{full_path}"
        logger.debug(f"JWT URI: {full_uri}")
        
        # JWT payload - must match Coinbase requirements exactly
        payload = {
            "sub": self.key_name,        # API key name
            "iss": "cdp",                # Must be exactly "cdp" per docs
            "nbf": timestamp,            # Not before - current time
            "exp": timestamp + 120,      # 2-minute expiration
            "uri": full_uri              # "METHOD host/path" format
        }
        
        # JWT headers - must include key ID and a unique nonce
        headers = {
            "kid": self.key_name,             # Same as sub claim
            "nonce": secrets.token_hex()      # Random hex string for nonce
        }
        
        # ---> ADDED DETAILED LOGGING <---
        logger.info(f"[REST JWT PRE-ENCODE] Payload: {json.dumps(payload)}")
        logger.info(f"[REST JWT PRE-ENCODE] Headers: {json.dumps(headers)}")
        logger.info(f"[REST JWT PRE-ENCODE] Private Key Type: {type(self.private_key)}")
        # ---> END ADDED LOGGING <---

        logger.debug(f"JWT Payload: {json.dumps(payload, indent=2)}")
        logger.debug(f"JWT Headers: {json.dumps(headers, indent=2)}")
        
        try:
            jwt_token = jwt.encode(
                payload=payload,
                key=self.private_key,
                algorithm="ES256",  # Must be ES256 for Coinbase
                headers=headers
            )
            logger.debug(f"Generated JWT token (first 50 chars): {jwt_token[:50]}...")
            return jwt_token
        except Exception as e:
            logger.error(f"Private key type during JWT generation: {type(self.private_key)}")
            logger.error(f"Error generating JWT: {e}", exc_info=True)
            raise CoinbaseError(f"Failed to generate JWT: {e}")

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Make authenticated request to Coinbase API using JWT.
        
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint (e.g., /orders)
            params (Optional[Dict]): Query parameters
            data (Optional[Dict]): Request body data
            
        Returns:
            Dict: API response
            
        Raises:
            CoinbaseError: If the API request fails
        """
        url = f"{self.api_url}{endpoint}"
        body = json.dumps(data) if data else ""
        
        # For JWT generation, we need the path part of the URL
        # First, strip leading slash to avoid double slashes
        clean_endpoint = endpoint.lstrip('/')
        
        # Handle query parameters for both the URL and JWT URI construction
        processed_endpoint = clean_endpoint
        if params:
            # Build the query string for the URL
            query_parts = []
            for key in sorted(params.keys()):
                encoded_key = urllib.parse.quote(str(key))
                encoded_value = urllib.parse.quote(str(params[key]))
                query_parts.append(f"{encoded_key}={encoded_value}")
            
            query_string = "&".join(query_parts)
            # Add query params to endpoint for JWT generation
            processed_endpoint = f"{clean_endpoint}?{query_string}"
        
        logger.debug(f"API URL: {url}")
        logger.debug(f"Method: {method}")
        logger.debug(f"Processed endpoint for JWT: {processed_endpoint}")
        
        try:
            # Generate JWT token with the properly formatted URI
            jwt_token = self._generate_jwt(method, processed_endpoint, body)
            
            # Set up request headers
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            logger.debug(f"Request headers: {', '.join(headers.keys())}")
            
            async with httpx.AsyncClient() as client:
                logger.debug(f"Sending {method} request to {url}")
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    timeout=30.0
                )
                
                logger.info(f"HTTP Request: {method} {url} {response!r}")
                
                # For 4xx and 5xx responses, print the response body for debugging
                if response.status_code >= 400:
                    logger.error(f"Error response: {response.text}")
                    logger.error(f"Response headers: {response.headers}")
                    try:
                        error_json = response.json()
                        logger.error(f"Detailed error: {json.dumps(error_json, indent=2)}")
                    except:
                        logger.error(f"Raw error text: {response.text}")
                    
                response.raise_for_status()
                
                # Handle the response
                try:
                    return response.json()
                except Exception as e:
                    # If the response isn't JSON, return the text content
                    if response.text:
                        return {"text": response.text}
                    else:
                        return {"status": "success", "message": "No content"}
                
        except httpx.HTTPStatusError as e:
            error_data = {}
            try:
                error_data = e.response.json()
                logger.error(f"HTTP error data: {error_data}")
            except:
                logger.error(f"Failed to parse error response: {e.response.text}")
                
            raise CoinbaseError(
                f"HTTP {e.response.status_code}: {str(e)}",
                status_code=e.response.status_code,
                response=error_data
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise CoinbaseError(f"Request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise CoinbaseError(f"Unexpected error: {str(e)}")
            
    # Account endpoints
    async def get_accounts(self) -> List[Dict]:
        """Get list of trading accounts"""
        response = await self._request("GET", "/accounts")
        return response.get("accounts", [])
        
    async def get_account(self, account_id: str) -> Dict:
        """Get specific account details"""
        return await self._request("GET", f"/accounts/{account_id}")
        
    # Product endpoints
    async def get_products(self) -> List[Dict]:
        """Get list of available products"""
        response = await self._request("GET", "/products")
        
        # Handle different response formats
        if isinstance(response, list):
            # Exchange API returns products as a list directly
            return response
        elif isinstance(response, dict) and "products" in response:
            # Advanced Trade API returns products in a dict with 'products' key
            return response.get("products", [])
        else:
            logger.warning(f"Unexpected products response format: {type(response)}")
            return []
        
    async def get_product(self, product_id: str) -> Dict:
        """Get product details by ID"""
        return await self._request("GET", f"/products/{product_id}")
        
    async def get_product_candles(
        self,
        product_id: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
        granularity: str = "ONE_HOUR"
    ) -> List[Dict]:
        """Get historical candles for a product"""
        # Convert granularity to seconds for the API
        granularity_map = {
            "ONE_MINUTE": 60,
            "FIVE_MINUTE": 300,
            "FIFTEEN_MINUTE": 900,
            "ONE_HOUR": 3600,
            "SIX_HOUR": 21600,
            "ONE_DAY": 86400
        }
        
        # Get the granularity in seconds
        granularity_seconds = granularity_map.get(granularity, 3600)
        
        params = {
            "granularity": granularity_seconds
        }
        
        if start:
            params["start"] = start
            
        if end:
            params["end"] = end
            
        # The Exchange API returns candles directly as a list
        response = await self._request("GET", f"/products/{product_id}/candles", params=params)
        return response  # Return the list directly
        
    # Order endpoints
    async def create_order(
        self,
        product_id: str,
        side: OrderSide,
        order_type: OrderType,
        size: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        client_order_id: Optional[str] = None,
        time_in_force: TimeInForce = TimeInForce.GTC
    ) -> Dict:
        """
        Create a new order
        
        Args:
            product_id (str): Trading pair ID
            side (OrderSide): Order side (BUY/SELL)
            order_type (OrderType): Order type (MARKET/LIMIT/STOP/STOP_LIMIT)
            size (float): Order size in base currency
            price (Optional[float]): Limit price (required for LIMIT orders)
            stop_price (Optional[float]): Stop price (required for STOP/STOP_LIMIT orders)
            client_order_id (Optional[str]): Client-specified order ID
            time_in_force (TimeInForce): Time in force policy (GTC/GTT/IOC/FOK)
            
        Returns:
            Dict: Raw response from order creation
        """
        # Convert enums to string values for the API request
        order_type_str = order_type.value.lower()
        
        data = {
            "product_id": product_id,
            "side": side.value.upper(),
            "order_configuration": {
                order_type_str: {
                    "size": str(size),
                    "time_in_force": time_in_force.value
                }
            }
        }
        
        if price is not None and order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
             data["order_configuration"][order_type_str]["limit_price"] = str(price)
            
        if stop_price is not None and order_type in [OrderType.STOP, OrderType.STOP_LIMIT]:
            data["order_configuration"][order_type_str]["stop_price"] = str(stop_price)
            
        if client_order_id:
            data["client_order_id"] = client_order_id
            
        response = await self._request("POST", "/orders", data=data)
        # Return the raw response dict for now, Pydantic parsing can be added later if needed
        return response
        
    async def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order by ID"""
        return await self._request("DELETE", f"/orders/{order_id}")
        
    async def get_orders(
        self,
        product_id: Optional[str] = None,
        status: Optional[List[OrderStatus]] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get list of orders
        
        Args:
            product_id (Optional[str]): Filter by product ID
            status (Optional[List[OrderStatus]]): Filter by order status
            limit (int): Maximum number of orders to return
            
        Returns:
            List[Dict]: Raw list of orders from API
        """
        params = {"limit": limit}
        if product_id:
            params["product_id"] = product_id
        if status:
            # Convert list of enums to comma-separated string of values
            params["status"] = ",".join([s.value for s in status])
            
        response = await self._request("GET", "/orders", params=params)
        return response.get("orders", [])
        
    async def get_order(self, order_id: str) -> Dict:
        """Get order details by ID"""
        response = await self._request("GET", f"/orders/{order_id}")
        return response
        
    # Market data endpoints
    async def get_market_trades(
        self,
        product_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """Get recent trades for a product"""
        params = {"limit": limit}
        response = await self._request("GET", f"/products/{product_id}/trades", params=params)
        return response.get("trades", [])
        
    async def get_order_book(
        self,
        product_id: str,
        level: int = 2
    ) -> Dict:
        """
        Get order book for a product
        
        Args:
            product_id (str): Product ID
            level (int): Order book level (1=best bid/ask, 2=top 50, 3=full)
            
        Returns:
            Dict: Order book data
        """
        params = {"level": level}
        return await self._request("GET", f"/products/{product_id}/book", params=params)
        
    # Position endpoints
    async def get_positions(self, product_id: Optional[str] = None) -> List[Position]:
        """Get open positions"""
        params = {}
        if product_id:
            params["product_id"] = product_id
            
        response = await self._request("GET", "/positions", params=params)
        # Parse raw response into list of Position models
        positions_data = response.get("positions", [])
        return [Position(**pos) for pos in positions_data]
        
    async def get_position(self, product_id: str) -> Position:
        """Get position for specific product"""
        response = await self._request("GET", f"/positions/{product_id}")
        # Parse raw response into Position model
        return Position(**response["position"]) 