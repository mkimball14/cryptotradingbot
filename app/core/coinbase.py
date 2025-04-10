import hmac
import hashlib
import time
import base64
import json
import logging
from typing import Dict, Optional, List, Union, Any
from datetime import datetime
import httpx
from pydantic import BaseModel, Field
from app.core.config import Settings

# Get logger
logger = logging.getLogger(__name__)

class CoinbaseError(Exception):
    """Base exception for Coinbase API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

class OrderSide(str):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"

class OrderStatus(str):
    PENDING = "PENDING"
    OPEN = "OPEN"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"

class Order(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    client_order_id: Optional[str] = Field(None, description="Client-specified order ID")
    product_id: str = Field(..., description="Trading pair identifier")
    side: str = Field(..., description="Order side (BUY/SELL)")
    order_type: str = Field(..., description="Order type")
    status: str = Field(..., description="Current order status")
    time_in_force: str = Field(..., description="Time in force policy")
    created_time: datetime = Field(..., description="Order creation timestamp")
    price: Optional[float] = Field(None, description="Limit price for the order")
    size: float = Field(..., description="Order size in base currency")
    filled_size: float = Field(0.0, description="Amount of order that has been filled")
    average_filled_price: Optional[float] = Field(None, description="Average price of filled size")

class Position(BaseModel):
    product_id: str = Field(..., description="Trading pair identifier")
    position_size: float = Field(..., description="Current position size")
    entry_price: float = Field(..., description="Average entry price")
    mark_price: float = Field(..., description="Current market price")
    unrealized_pl: float = Field(..., description="Unrealized profit/loss")
    realized_pl: float = Field(..., description="Realized profit/loss")
    initial_margin: float = Field(..., description="Initial margin requirement")
    maintenance_margin: float = Field(..., description="Maintenance margin requirement")

class CoinbaseClient:
    def __init__(self, settings: Settings):
        """
        Initialize Coinbase API client with settings
        
        Args:
            settings (Settings): Application settings containing API credentials
        """
        self.settings = settings
        self.api_key = settings.COINBASE_API_KEY
        self.api_secret = settings.COINBASE_API_SECRET
        self.passphrase = settings.COINBASE_API_PASSPHRASE
        self.api_url = settings.COINBASE_API_URL
        
    def _generate_signature(self, timestamp: str, method: str, request_path: str, body: str = "") -> str:
        """
        Generate signature for API request
        
        Args:
            timestamp (str): Request timestamp
            method (str): HTTP method
            request_path (str): API endpoint path
            body (str): Request body
            
        Returns:
            str: Base64 encoded signature
        """
        message = f"{timestamp}{method.upper()}{request_path}{body}"
        signature = hmac.new(
            base64.b64decode(self.api_secret),
            message.encode('utf-8'),
            hashlib.sha256
        )
        return base64.b64encode(signature.digest()).decode('utf-8')
        
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Make authenticated request to Coinbase API
        
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            params (Optional[Dict]): Query parameters
            data (Optional[Dict]): Request body data
            
        Returns:
            Dict: API response
            
        Raises:
            CoinbaseError: If the API request fails
        """
        timestamp = str(int(time.time()))
        url = f"{self.api_url}{endpoint}"
        
        # Convert data to JSON string for signature
        body = json.dumps(data) if data else ""
        
        # Debug 
        logger.debug(f"API URL: {url}")
        logger.debug(f"Method: {method}")
        logger.debug(f"API Key: {self.api_key[:10]}...")
        logger.debug(f"API Secret length: {len(self.api_secret)}")
        
        try:
            # Test base64 decoding here to catch issues early
            try:
                base64.b64decode(self.api_secret)
                logger.debug("Base64 decoding successful")
            except Exception as e:
                logger.error(f"Base64 decoding failed: {str(e)}")
                raise CoinbaseError(f"Invalid API secret format: {str(e)}")
                
            headers = {
                "CB-ACCESS-KEY": self.api_key,
                "CB-ACCESS-SIGN": self._generate_signature(timestamp, method, endpoint, body),
                "CB-ACCESS-TIMESTAMP": timestamp,
                "Content-Type": "application/json",
            }
            
            if self.passphrase:
                headers["CB-ACCESS-PASSPHRASE"] = self.passphrase
            
            # Debug headers (safely - not showing full values)
            logger.debug(f"Headers: {', '.join(headers.keys())}")
                
            async with httpx.AsyncClient() as client:
                logger.debug(f"Sending request to {url}")
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    timeout=30.0
                )
                
                logger.debug(f"Response status: {response.status_code}")
                
                # For 4xx and 5xx responses, print the response body for debugging
                if response.status_code >= 400:
                    logger.error(f"Error response: {response.text}")
                    
                response.raise_for_status()
                return await response.json()
                
        except httpx.HTTPStatusError as e:
            error_data = {}
            try:
                error_data = await e.response.json()
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
        return response.get("products", [])
        
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
        side: str,
        order_type: str,
        size: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        client_order_id: Optional[str] = None,
        time_in_force: str = "GTC"
    ) -> Order:
        """
        Create a new order
        
        Args:
            product_id (str): Trading pair ID
            side (str): Order side (BUY/SELL)
            order_type (str): Order type (MARKET/LIMIT/STOP/STOP_LIMIT)
            size (float): Order size in base currency
            price (Optional[float]): Limit price (required for LIMIT orders)
            stop_price (Optional[float]): Stop price (required for STOP/STOP_LIMIT orders)
            client_order_id (Optional[str]): Client-specified order ID
            time_in_force (str): Time in force policy (GTC/GTT/IOC/FOK)
            
        Returns:
            Order: Created order details
        """
        data = {
            "product_id": product_id,
            "side": side,
            "order_configuration": {
                order_type.lower(): {
                    "size": str(size),
                    "time_in_force": time_in_force
                }
            }
        }
        
        if price is not None:
            data["order_configuration"][order_type.lower()]["limit_price"] = str(price)
            
        if stop_price is not None:
            data["order_configuration"][order_type.lower()]["stop_price"] = str(stop_price)
            
        if client_order_id:
            data["client_order_id"] = client_order_id
            
        response = await self._request("POST", "/orders", data=data)
        return Order(**response["order"])
        
    async def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order by ID"""
        return await self._request("DELETE", f"/orders/{order_id}")
        
    async def get_orders(
        self,
        product_id: Optional[str] = None,
        status: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Order]:
        """
        Get list of orders
        
        Args:
            product_id (Optional[str]): Filter by product ID
            status (Optional[List[str]]): Filter by order status
            limit (int): Maximum number of orders to return
            
        Returns:
            List[Order]: List of orders
        """
        params = {"limit": limit}
        if product_id:
            params["product_id"] = product_id
        if status:
            params["status"] = ",".join(status)
            
        response = await self._request("GET", "/orders", params=params)
        return [Order(**order) for order in response.get("orders", [])]
        
    async def get_order(self, order_id: str) -> Order:
        """Get order details by ID"""
        response = await self._request("GET", f"/orders/{order_id}")
        return Order(**response["order"])
        
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
        return [Position(**pos) for pos in response.get("positions", [])]
        
    async def get_position(self, product_id: str) -> Position:
        """Get position for specific product"""
        response = await self._request("GET", f"/positions/{product_id}")
        return Position(**response["position"]) 