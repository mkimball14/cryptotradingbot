#!/usr/bin/env python3
"""
Coinbase WebSocket client for real-time market data.
"""

import json
import asyncio
import logging
import time
import hmac
import hashlib
import base64
from typing import Dict, List, Optional, Callable, Any, Set
import websockets
from websockets.exceptions import ConnectionClosed

from scripts.config.settings import settings
from scripts.utils.coinbase_auth import CoinbaseWebsocketAuth

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CoinbaseWebsocket:
    """
    WebSocket client for Coinbase exchange.
    Handles connection, authentication, and message processing.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 api_secret: Optional[str] = None, 
                 api_passphrase: Optional[str] = None, 
                 ws_url: Optional[str] = None):
        """
        Initialize the WebSocket client.
        
        Args:
            api_key: Coinbase API key (defaults to settings)
            api_secret: Coinbase API secret (defaults to settings)
            api_passphrase: Coinbase API passphrase (defaults to settings)
            ws_url: WebSocket URL (defaults to settings)
        """
        # Use provided values or defaults from settings
        self.api_key = api_key or settings.coinbase.COINBASE_API_KEY
        self.api_secret = api_secret or settings.coinbase.COINBASE_API_SECRET
        self.api_passphrase = api_passphrase or settings.coinbase.COINBASE_API_PASSPHRASE
        self.ws_url = ws_url or settings.coinbase.COINBASE_WS_URL
        
        # Connection state
        self.websocket = None
        self.is_connected = False
        self.is_authenticated = False
        self.keep_running = False
        
        # Subscriptions
        self.subscribed_channels: Set[str] = set()
        self.subscribed_products: Set[str] = set()
        
        # Message handlers
        self.message_handlers: Dict[str, List[Callable]] = {}
        self.default_handler: Optional[Callable] = None
        
        # Auth helper if credentials are provided
        if all([self.api_key, self.api_secret, self.api_passphrase]):
            try:
                self.auth = CoinbaseWebsocketAuth(
                    api_key=self.api_key,
                    api_secret=self.api_secret,
                    api_passphrase=self.api_passphrase
                )
                logger.info("WebSocket authentication configured")
            except Exception as e:
                logger.error(f"WebSocket authentication setup error: {str(e)}")
                self.auth = None
        else:
            logger.warning("WebSocket authentication credentials not provided - using public channels only")
            self.auth = None
    
    async def connect(self) -> bool:
        """
        Establish WebSocket connection.
        
        Returns:
            bool: True if connection successful
        """
        if self.is_connected:
            logger.info("Already connected to WebSocket")
            return True
            
        try:
            # Establish connection
            self.websocket = await websockets.connect(self.ws_url)
            self.is_connected = True
            logger.info(f"Connected to Coinbase WebSocket at {self.ws_url}")
            
            # Subscribe to heartbeat channel for connection monitoring
            if self.auth:
                await self._authenticate()
            
            return True
            
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            self.is_connected = False
            return False
    
    async def _authenticate(self) -> bool:
        """
        Authenticate the WebSocket connection.
        
        Returns:
            bool: True if authentication successful
        """
        if not self.auth:
            logger.warning("Cannot authenticate - auth credentials not configured")
            return False
            
        try:
            # Create authentication message with heartbeat channel
            auth_message = self.auth.get_auth_message(
                channel="heartbeat",
                products=["BTC-USD"]  # Default heartbeat product
            )
            
            # Send authentication message
            await self.websocket.send(json.dumps(auth_message))
            logger.debug(f"Sent authentication message: {auth_message}")
            
            # Wait for authentication response
            response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            if response_data.get("type") == "error":
                logger.error(f"Authentication error: {response_data.get('message')}")
                self.is_authenticated = False
                return False
                
            logger.info("Successfully authenticated WebSocket connection")
            self.is_authenticated = True
            
            # Add heartbeat channel to subscribed channels
            self.subscribed_channels.add("heartbeat")
            self.subscribed_products.add("BTC-USD")
            
            return True
            
        except asyncio.TimeoutError:
            logger.error("WebSocket authentication timed out")
            return False
        except Exception as e:
            logger.error(f"WebSocket authentication error: {str(e)}")
            return False
    
    async def subscribe(self, channels: List[str], products: List[str]) -> bool:
        """
        Subscribe to specified channels and products.
        
        Args:
            channels: List of channel names (ticker, level2, etc.)
            products: List of product IDs (BTC-USD, ETH-USD, etc.)
            
        Returns:
            bool: True if subscription successful
        """
        if not self.is_connected:
            logger.warning("Cannot subscribe - not connected")
            await self.connect()
            
        try:
            # Prepare formatted channels and products
            formatted_channels = []
            for channel in channels:
                channel_obj = {
                    "name": channel,
                    "product_ids": products
                }
                formatted_channels.append(channel_obj)
            
            # Create subscription message
            subscription = {
                "type": "subscribe",
                "channels": formatted_channels
            }
            
            # Add authentication if available
            if self.auth and self.is_authenticated:
                timestamp = str(int(time.time()))
                
                # For each channel, create combined signature
                for channel in channels:
                    # Sort products for consistent signature
                    sorted_products = sorted(products)
                    signature = self.auth.generate_signature(timestamp, channel, sorted_products)
                    
                    # Add auth fields
                    subscription["api_key"] = self.api_key
                    subscription["timestamp"] = timestamp
                    subscription["passphrase"] = self.api_passphrase
                    subscription["signature"] = signature
            
            # Send subscription request
            await self.websocket.send(json.dumps(subscription))
            logger.info(f"Sent subscription request for channels: {channels} and products: {products}")
            
            # Wait for subscription confirmation
            response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            if response_data.get("type") == "error":
                logger.error(f"Subscription error: {response_data.get('message')}")
                return False
                
            # Update subscribed channels and products
            self.subscribed_channels.update(channels)
            self.subscribed_products.update(products)
            
            logger.info(f"Successfully subscribed to {channels} for {products}")
            return True
            
        except asyncio.TimeoutError:
            logger.error("Subscription request timed out")
            return False
        except Exception as e:
            logger.error(f"Subscription error: {str(e)}")
            return False
    
    async def unsubscribe(self, channels: List[str], products: List[str]) -> bool:
        """
        Unsubscribe from specified channels and products.
        
        Args:
            channels: List of channel names to unsubscribe from
            products: List of product IDs to unsubscribe from
            
        Returns:
            bool: True if unsubscription successful
        """
        if not self.is_connected:
            logger.warning("Cannot unsubscribe - not connected")
            return False
            
        try:
            # Prepare formatted channels and products
            formatted_channels = []
            for channel in channels:
                channel_obj = {
                    "name": channel,
                    "product_ids": products
                }
                formatted_channels.append(channel_obj)
            
            # Create unsubscription message
            unsubscription = {
                "type": "unsubscribe",
                "channels": formatted_channels
            }
            
            # Send unsubscription request
            await self.websocket.send(json.dumps(unsubscription))
            logger.info(f"Sent unsubscription request for channels: {channels} and products: {products}")
            
            # Wait for unsubscription confirmation
            response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            if response_data.get("type") == "error":
                logger.error(f"Unsubscription error: {response_data.get('message')}")
                return False
                
            # Update subscribed channels and products
            for channel in channels:
                if channel in self.subscribed_channels:
                    self.subscribed_channels.remove(channel)
                    
            for product in products:
                if product in self.subscribed_products:
                    self.subscribed_products.remove(product)
            
            logger.info(f"Successfully unsubscribed from {channels} for {products}")
            return True
            
        except asyncio.TimeoutError:
            logger.error("Unsubscription request timed out")
            return False
        except Exception as e:
            logger.error(f"Unsubscription error: {str(e)}")
            return False
    
    def add_handler(self, message_type: str, handler: Callable) -> None:
        """
        Add a message handler for a specific message type.
        
        Args:
            message_type: Type of message to handle
            handler: Callback function to process messages
        """
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
            
        self.message_handlers[message_type].append(handler)
        logger.debug(f"Added handler for message type: {message_type}")
    
    def set_default_handler(self, handler: Callable) -> None:
        """
        Set a default handler for any message types without specific handlers.
        
        Args:
            handler: Callback function to process messages
        """
        self.default_handler = handler
        logger.debug("Set default message handler")
    
    async def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process a received message and route to appropriate handlers.
        
        Args:
            message: WebSocket message dictionary
        """
        message_type = message.get("type", "unknown")
        
        # Check for heartbeat
        if message_type == "heartbeat":
            logger.debug(f"Heartbeat received: {message}")
            return
            
        # Check for subscriptions message
        if message_type == "subscriptions":
            logger.info(f"Subscription update: {message}")
            return
            
        # Route to specific handlers if registered
        if message_type in self.message_handlers:
            for handler in self.message_handlers[message_type]:
                try:
                    await handler(message)
                except Exception as e:
                    logger.error(f"Error in message handler for {message_type}: {str(e)}")
        # Use default handler if available
        elif self.default_handler:
            try:
                await self.default_handler(message)
            except Exception as e:
                logger.error(f"Error in default message handler: {str(e)}")
        else:
            logger.debug(f"No handler for message type: {message_type}")
    
    async def _reconnect(self, max_retries: int = 5, delay: float = 1.0) -> bool:
        """
        Attempt to reconnect to the WebSocket.
        
        Args:
            max_retries: Maximum number of reconnection attempts
            delay: Initial delay between retries (exponential backoff)
            
        Returns:
            bool: True if reconnection successful
        """
        # Reset connection state
        self.is_connected = False
        self.is_authenticated = False
        
        # Store current subscriptions
        current_channels = list(self.subscribed_channels)
        current_products = list(self.subscribed_products)
        
        # Attempt to reconnect with exponential backoff
        for attempt in range(1, max_retries + 1):
            logger.info(f"Reconnection attempt {attempt}/{max_retries}...")
            
            try:
                # Close previous connection if it exists
                if self.websocket:
                    await self.websocket.close()
                
                # Connect and authenticate
                connected = await self.connect()
                if not connected:
                    raise Exception("Failed to connect")
                    
                # Resubscribe to previous channels
                if current_channels and current_products:
                    resubscribed = await self.subscribe(current_channels, current_products)
                    if not resubscribed:
                        raise Exception("Failed to resubscribe to channels")
                
                logger.info("Reconnection successful")
                return True
                
            except Exception as e:
                logger.error(f"Reconnection attempt {attempt} failed: {str(e)}")
                
                # Exponential backoff
                wait_time = delay * (2 ** (attempt - 1))
                logger.info(f"Waiting {wait_time} seconds before next attempt")
                await asyncio.sleep(wait_time)
        
        logger.error(f"Failed to reconnect after {max_retries} attempts")
        return False
    
    async def listen(self) -> None:
        """
        Start listening for messages from the WebSocket.
        """
        if not self.is_connected:
            logger.warning("Cannot listen - not connected")
            connected = await self.connect()
            if not connected:
                logger.error("Failed to connect for listening")
                return
        
        self.keep_running = True
        
        # Main message processing loop
        while self.keep_running:
            try:
                # Receive and parse message
                message = await self.websocket.recv()
                message_data = json.loads(message)
                
                # Process the message
                await self.process_message(message_data)
                
            except ConnectionClosed as e:
                logger.warning(f"WebSocket connection closed: {str(e)}")
                
                # Attempt to reconnect
                reconnected = await self._reconnect()
                if not reconnected and self.keep_running:
                    logger.error("Failed to reconnect - stopping listener")
                    self.keep_running = False
                    
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {str(e)}")
                
                # Continue listening for next message
                continue
    
    async def start(self) -> None:
        """
        Start the WebSocket client and begin listening for messages.
        """
        try:
            # Connect to WebSocket
            connected = await self.connect()
            if not connected:
                logger.error("Failed to connect")
                return
                
            # Start listening for messages
            await self.listen()
            
        except Exception as e:
            logger.error(f"Error starting WebSocket client: {str(e)}")
            
        finally:
            # Ensure connection is closed if listener stops
            await self.stop()
    
    async def stop(self) -> None:
        """
        Stop the WebSocket client and close the connection.
        """
        # Signal the listener to stop
        self.keep_running = False
        
        # Close the WebSocket connection
        if self.websocket:
            try:
                await self.websocket.close()
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket connection: {str(e)}")
                
        # Reset connection state
        self.is_connected = False
        self.is_authenticated = False
        self.websocket = None


# Application lifespan for FastAPI integration
async def lifespan(app):
    """
    Lifespan context manager for FastAPI application.
    Sets up and tears down the WebSocket connection.
    """
    # Create WebSocket client
    ws_client = CoinbaseWebsocket()
    
    # Set up event handlers
    async def handle_ticker(message):
        """Handle ticker messages."""
        logger.info(f"Ticker: {message.get('product_id')} - Price: {message.get('price')}")
    
    async def handle_default(message):
        """Handle all other message types."""
        logger.debug(f"Received message: {message}")
    
    # Register handlers
    ws_client.add_handler("ticker", handle_ticker)
    ws_client.set_default_handler(handle_default)
    
    try:
        # Start WebSocket client in background task
        task = asyncio.create_task(ws_client.start())
        
        # Store client in app state
        app.state.ws_client = ws_client
        
        # Subscribe to ticker channel for configured pairs
        if settings.coinbase.COINBASE_API_KEY:
            # Allow time for connection to establish
            await asyncio.sleep(1)
            await ws_client.subscribe(
                channels=["ticker"],
                products=settings.trading.TRADING_PAIRS
            )
        
        # Yield control back to FastAPI
        yield
        
    except Exception as e:
        logger.error(f"Error in WebSocket lifespan: {str(e)}")
        
    finally:
        # Clean up WebSocket connection
        if hasattr(app.state, "ws_client"):
            await app.state.ws_client.stop()


# Factory function for creating a WebSocket client
def create_websocket_client() -> CoinbaseWebsocket:
    """
    Create a new Coinbase WebSocket client instance.
    
    Returns:
        CoinbaseWebsocket: Configured WebSocket client
    """
    return CoinbaseWebsocket() 