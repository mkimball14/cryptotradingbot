import json
import asyncio
import time
import logging
from typing import Dict, Optional, List, Callable, Any
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
    """
    def __init__(self, settings=None, retry=True):
        """
        Initialize WebSocket client.
        
        Args:
            settings: Application settings
            retry: Whether to retry connection on failure
        """
        self.settings = settings or get_settings()
        self.websocket = None
        self.is_connected = False
        self.base_url = "wss://advanced-trade-ws.coinbase.com"
        self.max_retries = 5 if retry else 0
        self.retry_delay = 3  # seconds
        self.retry = retry  # Store retry flag
        self._exception = None
        self.subscribed_channels = {}
        self.message_queue = asyncio.Queue()
        self.message_processor_task = None
        self.receive_lock = asyncio.Lock()
        
        # Set up logging
        logger.debug(f"Initializing WebSocket client with API key: {self.settings.COINBASE_API_KEY[:5]}...")

    async def _load_api_key(self):
        """
        Load API key and secret from settings.
        """
        try:
            api_key = self.settings.COINBASE_API_KEY
            api_secret = self.settings.COINBASE_API_SECRET
            
            if not api_key or not api_secret:
                raise ValueError("API key or secret not found in settings")
                
            logger.debug(f"Successfully loaded API credentials from settings")
            return api_key, api_secret
            
        except Exception as e:
            logger.error(f"Failed to load API credentials: {str(e)}")
            raise

    async def _generate_jwt(self) -> str:
        """
        Generate a JWT token using the EC private key from Coinbase API.
        """
        try:
            # Load API key and secret
            api_key, api_secret = await self._load_api_key()
            
            logger.debug(f"API key: {api_key}")
            logger.debug(f"API secret format: {'PEM format' if api_secret.startswith('-----BEGIN') else 'Raw format'}")
            
            # Ensure API secret is properly formatted with PEM headers
            if not api_secret.startswith("-----BEGIN EC PRIVATE KEY-----"):
                logger.debug("API secret is missing PEM headers, adding them")
                api_secret = f"-----BEGIN EC PRIVATE KEY-----\n{api_secret}\n-----END EC PRIVATE KEY-----"
            
            logger.debug("Loading private key from PEM format")
            
            # Extract private key bytes in correct format
            try:
                private_key = serialization.load_pem_private_key(
                    api_secret.encode(),
                    password=None,
                    backend=default_backend()
                )
                
                # Get private key in correct format for JWT signing
                private_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                # Log key details for debugging
                if isinstance(private_key, ec.EllipticCurvePrivateKey):
                    curve_name = private_key.curve.name
                    key_size = private_key.curve.key_size
                    logger.debug(f"Private key loaded successfully - curve: {curve_name}, size: {key_size} bits")
            except Exception as e:
                logger.error(f"Failed to load private key: {str(e)}")
                raise ValueError(f"Invalid private key format: {str(e)}")
            
            # Current time in seconds
            timestamp = int(time.time())
            
            # Create JWT payload (claims)
            payload = {
                "sub": api_key,  # Subject (API key)
                "iss": "coinbase-cloud",  # Issuer
                "nbf": timestamp,  # Not Before
                "exp": timestamp + 60,  # Expiration (1 minute)
                "iat": timestamp,  # Issued At
                "aud": ["retail_websocket"]  # Audience
            }
            
            # Create simplified JWT header
            header = {
                "alg": "ES256",  # Algorithm (ECDSA with SHA-256)
                "kid": api_key,  # Key ID
                "typ": "JWT"     # Type
            }
            
            logger.debug(f"JWT header: {json.dumps(header)}")
            logger.debug(f"JWT payload: {json.dumps(payload)}")
            
            # Generate the JWT token using PEM string
            token = jwt.encode(
                payload=payload,
                key=private_bytes.decode('utf-8'),  # Use PEM string directly
                algorithm="ES256",
                headers=header
            )
            
            logger.debug(f"JWT token generated successfully, length: {len(token)}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate JWT token: {str(e)}")
            raise

    async def _message_receiver(self):
        """Background task to receive messages and put them in the queue."""
        try:
            logger.debug("Message receiver task started")
            while self.is_connected and self.websocket:
                try:
                    message = await self.websocket.recv()
                    message_data = json.loads(message)
                    await self.message_queue.put(message_data)
                    
                    # Log message type for debugging
                    message_type = message_data.get("type", "unknown")
                    if message_type == "error":
                        logger.error(f"Received error: {message_data.get('message', 'Unknown error')}")
                    elif message_type == "subscriptions":
                        logger.info(f"Subscription update: {message_data}")
                    else:
                        logger.debug(f"Received message type: {message_type}")
                    
                except (websockets.ConnectionClosed, asyncio.CancelledError):
                    logger.debug("WebSocket connection closed in receiver")
                    self.is_connected = False
                    break
                except Exception as e:
                    logger.error(f"Error receiving message: {str(e)}")
                    continue
        except asyncio.CancelledError:
            logger.debug("Message receiver task cancelled")
        except Exception as e:
            logger.error(f"Unexpected error in message receiver: {str(e)}")
        finally:
            logger.debug("Message receiver task ended")

    async def connect(self) -> None:
        """Connect to the WebSocket server."""
        try:
            # Clean up existing connection
            await self.disconnect()

            logger.info("Attempting to connect to WebSocket server...")
            self.websocket = await websockets.connect(self.base_url)
            self.is_connected = True
            logger.info("Successfully connected to WebSocket server")

            # Start message receiver task
            self.message_processor_task = asyncio.create_task(self._message_receiver())
            
            # Authenticate immediately after connection
            await self._authenticate()

        except Exception as e:
            logger.error(f"Failed to connect to WebSocket server: {str(e)}")
            self.is_connected = False
            if self.retry:
                logger.info("Retrying connection in 5 seconds...")
                await asyncio.sleep(5)
                await self.connect() # Retry connection
            else:
                raise

    async def _authenticate(self) -> None:
        """Authenticate with the WebSocket server using JWT."""
        try:
            # Generate JWT token
            token = await self._generate_jwt()
            logger.debug("Generated JWT token for authentication")
            
            # Send authentication message
            auth_message = {
                "type": "subscribe",
                "product_ids": ["BTC-USD"],
                "channel": "ticker",
                "jwt": token
            }
            
            logger.debug(f"Sending authentication message: {json.dumps(auth_message)}")
            await self.websocket.send(json.dumps(auth_message))
            
            # Wait for response from the queue
            try:
                response_data = await asyncio.wait_for(self.message_queue.get(), timeout=5.0)
                logger.debug(f"Received authentication response: {json.dumps(response_data, indent=2)}")
                
                if "error" in response_data:
                    raise ValueError(f"Authentication failed: {response_data['message']}")
                    
                logger.info("Successfully authenticated with WebSocket server")
                
            except asyncio.TimeoutError:
                raise ValueError("Authentication timed out waiting for response")
                
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    async def disconnect(self) -> None:
        """
        Disconnect from the WebSocket server.
        """
        if self.message_processor_task and not self.message_processor_task.done():
            self.message_processor_task.cancel()
            try:
                await self.message_processor_task
            except asyncio.CancelledError:
                logger.debug("Message processor task cancelled")
        
        if self.websocket and not self.websocket.closed:
            await self.websocket.close()
            self.is_connected = False
            logger.info("Disconnected from WebSocket server")

    async def subscribe(self, product_ids: List[str], channels: List[str] = ["ticker"]):
        """
        Subscribe to specified product IDs on specified channels.
        
        Args:
            product_ids: List of product IDs to subscribe to
            channels: List of channels to subscribe to, defaults to ["ticker"]
        """
        if not self.websocket or self.websocket.closed:
            error_msg = "WebSocket is not connected. Call connect() first."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            # Generate JWT token for authentication
            jwt_token = await self._generate_jwt()
            
            # Subscribe to each channel separately as per Coinbase example
            for channel in channels:
                subscription_message = {
                    "type": "subscribe",
                    "channel": channel,
                    "product_ids": product_ids,
                    "jwt": jwt_token
                }
                
                logger.debug(f"Sending subscription message for channel {channel}:\n{json.dumps(subscription_message, indent=2)}")
                await self.websocket.send(json.dumps(subscription_message))
                
                # Wait for subscription confirmation from queue
                try:
                    start_time = time.time()
                    subscription_confirmed = False
                    
                    # Try for up to 5 seconds to get subscription confirmation
                    while not subscription_confirmed and time.time() - start_time < 5:
                        # Use a timeout that's shorter than our overall wait time
                        try:
                            response_data = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                            
                            # Check for subscription confirmation
                            if response_data.get("type") == "subscriptions" or "subscriptions" in response_data:
                                subscription_confirmed = True
                                logger.info(f"Successfully subscribed to {channel} for products: {product_ids}")
                                
                                # Store subscribed products with their channel
                                for product_id in product_ids:
                                    sub_key = f"{channel}:{product_id}"
                                    if sub_key not in self.subscribed_channels:
                                        self.subscribed_channels[sub_key] = product_id
                                        
                            # If it's some other message, put it back in the queue for the next reader
                            elif "error" not in response_data:
                                # Don't put error messages back in queue
                                await self.message_queue.put(response_data)
                                
                            # Check for error
                            if "error" in response_data:
                                error_msg = f"Subscription failed: {response_data.get('message', 'Unknown error')}"
                                logger.error(error_msg)
                                raise ValueError(error_msg)
                        
                        except asyncio.TimeoutError:
                            # Just continue the loop
                            continue
                    
                    if not subscription_confirmed:
                        logger.warning(f"Timed out waiting for subscription confirmation for channel {channel}")
                        # Continue anyway - the subscription might have succeeded
                
                except Exception as e:
                    logger.error(f"Error processing subscription response: {str(e)}")
                    # Continue with other channels
        
        except Exception as e:
            logger.error(f"Error subscribing to products {product_ids} on channels {channels}: {str(e)}")
            raise

    async def unsubscribe(self, product_ids: List[str], channels: List[str] = ["ticker"]) -> None:
        """
        Unsubscribe from specified product IDs and channels
        """
        if not self.websocket or self.websocket.closed:
            raise ValueError("WebSocket is not connected")

        try:
            jwt_token = await self._generate_jwt()
            
            unsubscribe_message = {
                "type": "unsubscribe",
                "product_ids": product_ids,
                "channels": channels,
                "jwt": jwt_token
            }
            
            logger.debug(f"Sending unsubscription message: {json.dumps(unsubscribe_message, indent=2)}")
            await self.websocket.send(json.dumps(unsubscribe_message))
            
            # Wait for unsubscription confirmation
            try:
                start_time = time.time()
                unsubscription_confirmed = False
                
                while not unsubscription_confirmed and time.time() - start_time < 5:
                    try:
                        response_data = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                        
                        # Check for unsubscription confirmation
                        if response_data.get("type") == "subscriptions":
                            unsubscription_confirmed = True
                            logger.info(f"Successfully unsubscribed from channels: {channels} for products: {product_ids}")
                            
                            # Remove from subscribed channels
                            for channel in channels:
                                for product_id in product_ids:
                                    sub_key = f"{channel}:{product_id}"
                                    if sub_key in self.subscribed_channels:
                                        del self.subscribed_channels[sub_key]
                        
                        # If it's some other message, put it back in the queue
                        elif "error" not in response_data:
                            await self.message_queue.put(response_data)
                            
                        # Check for error
                        if "error" in response_data:
                            error_msg = f"Unsubscription failed: {response_data.get('message', 'Unknown error')}"
                            logger.error(error_msg)
                            raise ValueError(error_msg)
                    
                    except asyncio.TimeoutError:
                        continue
                
                if not unsubscription_confirmed:
                    logger.warning(f"Timed out waiting for unsubscription confirmation")
            
            except Exception as e:
                logger.error(f"Error processing unsubscription response: {str(e)}")
            
        except Exception as e:
            logger.error(f"Failed to unsubscribe: {str(e)}")
            raise

    async def get_next_message(self, timeout=1.0):
        """
        Get the next message from the queue.
        
        Args:
            timeout: Timeout in seconds to wait for a message
        
        Returns:
            Message data or None if timeout
        """
        try:
            return await asyncio.wait_for(self.message_queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None 