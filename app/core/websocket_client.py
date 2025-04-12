import json
import asyncio
import time
import logging
from typing import Dict, Optional, List, Callable, Any, Union, Set
import websockets
from websockets.exceptions import ConnectionClosed
from pydantic import BaseModel
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import base64
import hmac
import hashlib
import os
import uuid
from urllib.parse import urlparse
from app.core.config import Settings, get_settings
import random
import secrets

# Configure logging for WebSocket client
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create file handler
websocket_handler = logging.FileHandler('websocket.log')
websocket_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
websocket_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(websocket_handler)
logger.addHandler(console_handler)

class WebSocketMessage(BaseModel):
    type: str
    channel: str
    timestamp: str
    sequence_num: int
    product_id: str
    data: Dict[str, Any]

class CoinbaseWebSocketClient:
    """
    WebSocket client for Coinbase Advanced Trade API
    
    This client supports connection to the Coinbase Advanced Trade WebSocket API,
    which provides real-time market data and user account updates.
    
    Available channels:
    - ticker: Real-time price updates
    - level2: Order book updates
    - user: User account updates
    - status: Platform status updates
    - market_trades: Real-time trade execution data
    - candles: Candlestick updates (1m, 5m, 15m, 1h, etc.)
    """
    def __init__(
        self, 
        settings: Optional[Settings] = None,
        on_message: Optional[Callable[[Dict], Any]] = None,
        on_error: Optional[Callable[[Exception], Any]] = None,
        on_connect: Optional[Callable[[], Any]] = None,
        on_disconnect: Optional[Callable[[], Any]] = None,
        auto_reconnect: bool = True,
        max_reconnect_attempts: int = 5,
        reconnect_delay: int = 5  # seconds
    ):
        """
        Initialize WebSocket client.
        
        Args:
            settings: Application settings
            on_message: Callback function for received messages
            on_error: Callback function for errors
            on_connect: Callback function for successful connections
            on_disconnect: Callback function for disconnections
            auto_reconnect: Whether to automatically reconnect on disconnection
            max_reconnect_attempts: Maximum number of reconnection attempts
            reconnect_delay: Delay between reconnection attempts in seconds
        """
        self.settings = settings or get_settings()
        self.on_message = on_message or self._default_message_handler
        self.on_error = on_error or self._default_error_handler
        self.on_connect = on_connect or self._default_connect_handler
        self.on_disconnect = on_disconnect or self._default_disconnect_handler
        
        # Connection settings
        self.websocket = None
        self.is_connected = False
        self.is_authenticating = False
        self.base_url = self.settings.COINBASE_WS_URL
        self.auto_reconnect = auto_reconnect
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self.reconnect_attempts = 0
        
        # Subscription tracking
        self.active_subscriptions: Dict[str, Set[str]] = {}  # channel -> set of product_ids
        self.message_queue = asyncio.Queue()
        self.message_processor_task = None
        self.heartbeat_task = None
        
        # Configure JWT key if available
        self.private_key = None
        if self.settings.COINBASE_JWT_PRIVATE_KEY:
            try:
                self.private_key = serialization.load_pem_private_key(
                    self.settings.COINBASE_JWT_PRIVATE_KEY.encode(),
                    password=None,
                    backend=default_backend()
                )
                logger.info("Loaded JWT private key for authentication")
            except Exception as e:
                logger.error(f"Failed to load JWT private key: {str(e)}")
                self.private_key = None
        
        logger.debug(f"Initialized WebSocket client with Coinbase Advanced Trade API")

    async def connect(self) -> bool:
        """
        Connect to the WebSocket server.
        
        Returns:
            bool: True if connection was successful, False otherwise
        """
        if self.is_connected:
            logger.debug("Already connected to WebSocket server")
            return True

        try:
            logger.info("Connecting to Coinbase WebSocket server...")
            self.websocket = await websockets.connect(self.base_url, ping_interval=20)
            logger.info("WebSocket TCP connection established.")
            
            self.is_connected = True
            self.reconnect_attempts = 0
            
            # Start message receiver task
            self.message_processor_task = asyncio.create_task(self._message_processor())
            
            # Start heartbeat task
            self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            
            # Call connection callback
            logger.debug("Attempting to call on_connect callback...")
            await self._on_connect(self.websocket)
            logger.debug("Finished calling on_connect callback.")
            
            logger.info("Successfully connected to Coinbase WebSocket server (post-callback)")
            return True
            
        except Exception as e:
            logger.error(f"Failed during connect sequence: {str(e)}", exc_info=True)
            self.is_connected = False
            
            await self._safe_callback(self.on_error, e)
            
            if self.auto_reconnect and self.reconnect_attempts < self.max_reconnect_attempts:
                self.reconnect_attempts += 1
                delay = self.reconnect_delay * self.reconnect_attempts  # Exponential backoff
                logger.info(f"Reconnecting in {delay} seconds... (Attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})")
                await asyncio.sleep(delay)
                return await self.connect()  # Retry connection
                
            return False

    async def disconnect(self) -> None:
        """
        Disconnect from the WebSocket server and clean up resources.
        """
        logger.info("Disconnecting from WebSocket server...")
        
        # Cancel tasks
        if self.message_processor_task and not self.message_processor_task.done():
            self.message_processor_task.cancel()
            
        if self.heartbeat_task and not self.heartbeat_task.done():
            self.heartbeat_task.cancel()
            
        # Close WebSocket connection
        if self.websocket:
            try:
                await self.websocket.close()
            except Exception as e:
                logger.error(f"Error while closing WebSocket connection: {str(e)}")
                
        # Reset state
        self.is_connected = False
        self.websocket = None
        
        # Call disconnect callback
        await self._safe_callback(self.on_disconnect)
        logger.info("Disconnected from WebSocket server")

    async def subscribe(self, product_ids: Union[str, List[str]], channels: Union[str, List[str]]) -> bool:
        """
        Subscribe to specific channels for the given product IDs.
        
        Args:
            product_ids: Single product ID or list of product IDs (e.g., "BTC-USD")
            channels: Single channel name or list of channel names (e.g., "ticker", "level2")
            
        Returns:
            bool: True if subscription request was sent successfully, False otherwise
        """
        logger.info(f"Subscribe method called for channels: {channels}, products: {product_ids}")
        
        # Add a delay since Coinbase recommends waiting after connection is established
        await asyncio.sleep(1)
        
        if not self.is_connected:
            logger.warning("WebSocket not connected. Attempting connection before subscribe...")
            if not await self.connect():
                 logger.error("Failed to connect, cannot subscribe.")
                 return False
            # Add a small delay after connecting before subscribing
            await asyncio.sleep(2)
            if not self.is_connected:
                logger.error("Still not connected after explicit connect attempt in subscribe.")
                return False
        
        # Normalize inputs to lists
        if isinstance(product_ids, str):
            product_ids = [product_ids]
            
        if isinstance(channels, str):
            channels = [channels]
            
        # Generate JWT token for authentication
        try:
            jwt_token = self._generate_jwt()
            logger.debug(f"Generated JWT for subscription (first 50 chars): {jwt_token[:50]}...")
        except Exception as e:
            logger.error(f"Failed to generate JWT for subscription: {str(e)}")
            await self._safe_callback(self.on_error, e)
            return False
        
        # Verify channels are valid
        valid_channels = ["ticker", "level2", "market_trades", "status", "user", "candles"]
        invalid_channels = [c for c in channels if c not in valid_channels]
        if invalid_channels:
            logger.warning(f"Invalid channels requested: {invalid_channels}. Will be ignored.")
            channels = [c for c in channels if c in valid_channels]
            
            if not channels:
                logger.error("No valid channels to subscribe to.")
                return False
                
        # Verify product IDs are formatted correctly (e.g., "BTC-USD")
        product_ids = [pid.upper() if "-" in pid else f"{pid.upper()}-USD" for pid in product_ids]
            
        # Send subscription requests (one per channel as recommended by Coinbase)
        try:
            for channel in channels:
                # Update subscription tracking
                if channel not in self.active_subscriptions:
                    self.active_subscriptions[channel] = set()
                
                self.active_subscriptions[channel].update(product_ids)
                
                # Create subscription message
                subscription_message = {
                    "type": "subscribe",
                    "channel": channel,
                    "product_ids": product_ids,
                    "jwt": jwt_token
                }
                
                # Add channel-specific parameters if needed
                if channel == "candles":
                    # For candles, specify the granularity if not provided
                    subscription_message["granularity"] = "ONE_HOUR"  # Options: ONE_MINUTE, FIVE_MINUTE, FIFTEEN_MINUTE, ONE_HOUR, etc.
                
                # Log full message for better debugging
                logger.debug(f"Sending subscription message: {json.dumps(subscription_message)}")
                
                # Log the full payload for detailed debugging
                logger.info(f"FULL SUBSCRIPTION PAYLOAD: {json.dumps(subscription_message)}")
                
                if self.websocket:
                    await self.websocket.send(json.dumps(subscription_message))
                    logger.info(f"Successfully sent subscription request for channel '{channel}'")
                    # Add a small delay between subscription requests to avoid rate limiting
                    await asyncio.sleep(0.5)
                else:
                    logger.error(f"Cannot send subscription for {channel}: WebSocket is None.")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Failed to send subscription request: {str(e)}", exc_info=True)
            await self._safe_callback(self.on_error, e)
            return False

    async def unsubscribe(self, product_ids: Union[str, List[str]], channels: Union[str, List[str]]) -> bool:
        """
        Unsubscribe from specific channels for the given product IDs.
        
        Args:
            product_ids: Single product ID or list of product IDs (e.g., "BTC-USD")
            channels: Single channel name or list of channel names (e.g., "ticker", "level2")
            
        Returns:
            bool: True if unsubscription request was sent successfully, False otherwise
        """
        if not self.is_connected:
            logger.error("Cannot unsubscribe: not connected to WebSocket server")
            return False
            
        # Normalize inputs to lists
        if isinstance(product_ids, str):
            product_ids = [product_ids]
            
        if isinstance(channels, str):
            channels = [channels]
        
        # Send unsubscription requests (one per channel as recommended by Coinbase)
        try:
            for channel in channels:
                # Update subscription tracking
                if channel in self.active_subscriptions:
                    for product_id in product_ids:
                        self.active_subscriptions[channel].discard(product_id)
                        
                    # Remove channel if no products left
                    if not self.active_subscriptions[channel]:
                        del self.active_subscriptions[channel]
                
                # Create unsubscription message
                unsubscription_message = {
                    "type": "unsubscribe",
                    "channel": channel,
                    "product_ids": product_ids
                }
                
                logger.debug(f"Sending unsubscription for channel '{channel}' with products: {product_ids}")
                await self.websocket.send(json.dumps(unsubscription_message))
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to send unsubscription request: {str(e)}")
            await self._safe_callback(self.on_error, e)
            return False

    async def resubscribe_all(self) -> bool:
        """
        Resubscribe to all active subscriptions.
        Useful after reconnection.
        
        Returns:
            bool: True if all resubscription requests were sent successfully, False otherwise
        """
        if not self.active_subscriptions:
            logger.debug("No active subscriptions to resubscribe to")
            return True
            
        success = True
        for channel, product_ids in self.active_subscriptions.items():
            channel_success = await self.subscribe(list(product_ids), channel)
            success = success and channel_success
            
        return success

    def _generate_jwt(self) -> str:
        """
        Generate a JWT token for WebSocket authentication.
        
        Returns:
            str: JWT token string
        """
        timestamp = int(time.time())
        
        # Per Advanced Trade API Docs, service should be "cdp"
        # uri claim is NOT needed for websocket auth
        
        payload = {
            "sub": self.settings.COINBASE_JWT_KEY_NAME,
            "iss": "cdp", # Corrected: Use "cdp" as per REST API rules
            "nbf": timestamp,
            "exp": timestamp + 120, # Corrected: Use 120 seconds expiry like REST
            "aud": ["websocket"] # Audience might still be needed for WS context
        }
        
        headers = {
            "kid": self.settings.COINBASE_JWT_KEY_NAME,
            "nonce": secrets.token_hex() # Corrected: Use unique hex nonce like REST
        }
        
        # Log the payload for debugging
        logger.debug(f"JWT payload for WebSocket: {json.dumps(payload)}")
        logger.debug(f"JWT headers for WebSocket: {json.dumps(headers)}")
        
        # Generate the token
        try:
            jwt_token = jwt.encode(
                payload=payload,
                key=self.private_key, # Use the loaded private key object
                algorithm="ES256",
                headers=headers
            )
            logger.debug(f"Generated JWT for WebSocket (first 50): {jwt_token[:50]}...")
            return jwt_token
        except Exception as e:
            logger.error(f"Error generating WebSocket JWT: {e}", exc_info=True)
            raise

    async def _message_processor(self) -> None:
        """
        Process incoming messages from the WebSocket connection.
        """
        if not self.websocket:
            logger.error("Cannot process messages: WebSocket not connected")
            return
            
        try:
            async for message in self.websocket:
                try:
                    # Parse message
                    msg_data = json.loads(message)
                    
                    # Determine message type/channel
                    msg_type = msg_data.get("type")
                    channel = msg_data.get("channel")
                    log_identifier = msg_type if msg_type else channel  # Use channel if type is missing

                    logger.debug(f"Received raw message (type/channel: {log_identifier})")
                    
                    # Handle based on type or channel
                    if msg_type == "error":
                        logger.error(f"WebSocket error message: {msg_data.get('message', 'Unknown error')}")
                        error = Exception(f"WebSocket error: {msg_data.get('message', 'Unknown error')}")
                        await self._safe_callback(self.on_error, error)
                        
                    elif msg_type == "heartbeat" or channel == "heartbeat":
                        logger.debug(f"Received heartbeat message: {msg_data}")

                    elif channel == "subscriptions":
                        # This confirms successful subscriptions
                        logger.info(f"Subscription confirmation received: {msg_data.get('events', [])}")
                        # Optionally update internal state based on confirmation
                        confirmed_subs = msg_data.get('events', [{}])[0].get('subscriptions', {})
                        logger.debug(f"Confirmed subscriptions: {confirmed_subs}")

                    elif channel == "ticker":
                        product_id = msg_data.get("events", [{}])[0].get("tickers", [{}])[0].get("product_id", "unknown")
                        logger.debug(f"Received ticker data for {product_id}")
                        
                    elif channel == "candles":
                        product_id = msg_data.get("events", [{}])[0].get("candles", [{}])[0].get("product_id", "unknown")
                        logger.debug(f"Received candle data for {product_id}")
                        
                    elif channel == "market_trades":
                        product_id = msg_data.get("events", [{}])[0].get("trades", [{}])[0].get("product_id", "unknown")
                        logger.debug(f"Received market trades for {product_id}")
                        
                    elif channel == "level2":
                        # Level2 data often comes as snapshots and updates
                        event_type = msg_data.get("events", [{}])[0].get("type", "unknown_level2_event")
                        product_ids = msg_data.get("events", [{}])[0].get("product_id", "unknown") # Coinbase might use product_id directly here
                        logger.debug(f"Received level2 data ({event_type}) for {product_ids}")
                        
                    elif channel == "user":
                        logger.debug(f"Received user account update: {msg_data}")
                        
                    elif channel == "status":
                        logger.debug(f"Received status update: {msg_data}")
                        
                    else:
                        # Log unknown message with more details for debugging
                        logger.warning(f"Received unhandled message (type: {msg_type}, channel: {channel}): {json.dumps(msg_data)[:200]}...")
                    
                    # Always process message with the main callback
                    await self._safe_callback(self.on_message, msg_data)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse WebSocket message: {e}")
                    logger.debug(f"Raw message causing decode error: {message[:100]}...")
                except Exception as e:
                    logger.error(f"Error processing WebSocket message: {e}", exc_info=True) # Add exc_info for more detail
                    
        except asyncio.CancelledError:
            logger.debug("Message processor task was cancelled")
        except ConnectionClosed as e:
             logger.warning(f"WebSocket connection closed: {e.code} {e.reason}")
             # Handle disconnection and potential reconnect
             self.is_connected = False
             await self._safe_callback(self.on_disconnect)
             if self.auto_reconnect:
                 asyncio.create_task(self._reconnect())
        except Exception as e:
            logger.error(f"WebSocket message processor encountered critical error: {str(e)}", exc_info=True)
            # Handle disconnection and potential reconnect
            self.is_connected = False
            await self._safe_callback(self.on_disconnect)
            if self.auto_reconnect:
                asyncio.create_task(self._reconnect())

    async def _heartbeat_loop(self) -> None:
        """
        Send periodic heartbeats to keep the connection alive.
        """
        try:
            while self.is_connected and self.websocket:
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
                
                if not self.is_connected or not self.websocket:
                    break
                    
                try:
                    heartbeat = {"type": "heartbeat"}
                    await self.websocket.send(json.dumps(heartbeat))
                    logger.debug("Sent heartbeat to WebSocket server")
                except Exception as e:
                    logger.error(f"Failed to send heartbeat: {str(e)}")
                    
                    # Connection might be dead, attempt reconnection
                    if self.auto_reconnect:
                        self.is_connected = False
                        await self._safe_callback(self.on_disconnect)
                        
                        # Schedule reconnection
                        asyncio.create_task(self._reconnect())
                        break
                        
        except asyncio.CancelledError:
            logger.debug("Heartbeat task was cancelled")
        except Exception as e:
            logger.error(f"Heartbeat loop failed: {str(e)}")

    async def _reconnect(self) -> None:
        """
        Attempt to reconnect to the WebSocket server with exponential backoff.
        """
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error(f"Maximum reconnection attempts ({self.max_reconnect_attempts}) reached")
            return
            
        self.reconnect_attempts += 1
        delay = self.reconnect_delay * self.reconnect_attempts
        
        logger.info(f"Attempting to reconnect in {delay} seconds... (Attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})")
        await asyncio.sleep(delay)
        
        # Clean up old connection
        if self.websocket:
            try:
                await self.websocket.close()
            except:
                pass
            self.websocket = None
            
        # Connect and resubscribe
        if await self.connect():
            if self.active_subscriptions:
                await self.resubscribe_all()

    async def _safe_callback(self, callback: Optional[Callable], *args, **kwargs) -> None:
        """
        Safely execute a callback function.
        
        Args:
            callback: Callback function to execute
            *args: Positional arguments for the callback
            **kwargs: Keyword arguments for the callback
        """
        if callback:
            callback_name = getattr(callback, '__name__', 'unknown_callback')
            logger.debug(f"Executing safe callback: {callback_name}")
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(*args, **kwargs)
                else:
                    callback(*args, **kwargs)
                logger.debug(f"Finished safe callback: {callback_name}")
            except Exception as e:
                logger.error(f"Error in callback {callback_name}: {str(e)}", exc_info=True)
        else:
             logger.debug("Skipping safe callback: callback is None")

    # Default handlers
    def _default_message_handler(self, message: Dict) -> None:
        """Default handler for received messages."""
        channel = message.get("channel", "")
        product_id = message.get("product_id", "")
        logger.debug(f"Received {channel} message for {product_id}")

    def _default_error_handler(self, error: Exception) -> None:
        """Default handler for errors."""
        logger.error(f"WebSocket error: {str(error)}")

    def _default_connect_handler(self) -> None:
        """Default handler for successful connections."""
        logger.info("Connected to WebSocket server")

    def _default_disconnect_handler(self) -> None:
        """Default handler for disconnections."""
        logger.info("Disconnected from WebSocket server")

    async def _on_connect(self, websocket):
        """Handler for connection established events."""
        self.is_connected = True
        logger.info("WebSocket connection established")
        
        # If we have pending subscriptions, restore them with a delay
        if self.active_subscriptions:
            logger.info(f"Connection established. Restoring {len(self.active_subscriptions)} active subscriptions after delay...")
            
            # Wait for connection to fully stabilize before sending subscriptions
            await asyncio.sleep(2)
            
            try:
                # Generate a new JWT token for authentication
                jwt_token = self._generate_jwt()
                
                for channel, products in self.active_subscriptions.items():
                    product_list = list(products)
                    
                    subscription_message = {
                        "type": "subscribe",
                        "channel": channel,
                        "product_ids": product_list,
                        "jwt": jwt_token
                    }
                    
                    logger.debug(f"Restoring subscription for channel '{channel}': {json.dumps(subscription_message)}")
                    await websocket.send(json.dumps(subscription_message))
                    logger.info(f"Restored subscription for channel '{channel}' with {len(product_list)} products")
                    
                    # Small delay between subscription messages
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"Failed to restore subscriptions: {str(e)}", exc_info=True)
                await self._safe_callback(self.on_error, e)
                
        # Notify any listeners only after attempting to restore subscriptions
        logger.info("Calling on_connect callback")
        await self._safe_callback(self.on_connect)
        logger.debug("on_connect callback completed")

    async def _on_error(self, websocket, error):
        """Handler for WebSocket errors.
        
        Args:
            websocket: The WebSocket connection where the error occurred
            error: The error that occurred
        """
        logger.error(f"WebSocket error: {str(error)}", exc_info=True)
        
        # Check if error is related to connection - if so, attempt to reconnect
        if isinstance(error, (websockets.exceptions.ConnectionClosedError, 
                             websockets.exceptions.ConnectionClosedOK,
                             websockets.exceptions.InvalidStatusCode)):
            logger.warning(f"Connection error detected: {error.__class__.__name__}: {str(error)}")
            self.is_connected = False
            
            # Schedule reconnection attempt with exponential backoff
            if self.reconnect_attempts < self.max_reconnect_attempts:
                backoff_seconds = (2 ** self.reconnect_attempts) + (random.random() * 0.5)
                self.reconnect_attempts += 1
                logger.info(f"Scheduling reconnection attempt {self.reconnect_attempts}/{self.max_reconnect_attempts} in {backoff_seconds:.2f} seconds")
                
                # Schedule reconnection
                asyncio.create_task(self._delayed_reconnect(backoff_seconds))
            else:
                logger.error(f"Maximum reconnection attempts ({self.max_reconnect_attempts}) reached. Giving up.")
                # Reset reconnect counter for future connection attempts
                self.reconnect_attempts = 0
        
        # Notify any error handlers
        await self._safe_callback(self.on_error, error)
    
    async def _delayed_reconnect(self, delay_seconds):
        """Attempt to reconnect after a delay.
        
        Args:
            delay_seconds: Number of seconds to wait before reconnecting
        """
        logger.info(f"Waiting {delay_seconds:.2f} seconds before reconnection attempt...")
        await asyncio.sleep(delay_seconds)
        logger.info("Attempting to reconnect now...")
        
        try:
            await self.connect()
            logger.info("Reconnection successful")
            self.reconnect_attempts = 0  # Reset retry counter on successful connection
        except Exception as e:
            logger.error(f"Reconnection attempt failed: {str(e)}", exc_info=True)
            # The next error will trigger another reconnection attempt if needed 