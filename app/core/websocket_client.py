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

from coinbase.websocket import WSClient, WebsocketResponse, WSClientException, WSClientConnectionClosedException

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
    Manages connection and data handling for Coinbase Advanced Trade WebSocket API.
    """
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        product_ids: List[str],
        channels: List[str],
        message_queue: Optional[asyncio.Queue] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        retry: bool = True,
        verbose: bool = False # Set to True for detailed SDK logging
    ):
        """
        Initializes the WebSocket client.

        Args:
            api_key (str): Coinbase API Key (e.g., "organizations/.../apiKeys/...").
            api_secret (str): Coinbase API Secret (the multi-line private key string).
            product_ids (List[str]): List of product IDs to subscribe to (e.g., ["BTC-USD"]).
            channels (List[str]): List of channels to subscribe to (e.g., ["ticker", "heartbeats"]).
            message_queue (Optional[asyncio.Queue]): Queue to put processed messages onto.
            on_error (Optional[Callable[[Exception], None]]): Optional callback for handling errors.
            retry (bool): Whether the client should automatically attempt reconnection. Defaults to True.
            verbose (bool): Enable verbose logging from the underlying WSClient. Defaults to False.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.product_ids = product_ids
        self.channels = channels
        self.message_queue = message_queue
        self._on_error_callback = on_error
        self._should_retry = retry
        self._verbose = verbose
        
        self.ws_client: Optional[WSClient] = None
        self._is_running = False

    def _on_open(self):
        """Callback executed when the WebSocket connection is opened."""
        logger.info("WebSocket connection opened. Subscribing...")
        self.subscribe()

    def _on_close(self):
        """Callback executed when the WebSocket connection is closed."""
        logger.warning("WebSocket connection closed.")
        self._is_running = False
        # Reconnection is handled internally by WSClient if retry=True

    def _on_message(self, msg: str):
        """Callback executed when a message is received."""
        try:
            # logger.debug(f"Raw WS message: {msg}") # Log raw for debugging if needed
            data = json.loads(msg)
            
            # Optionally parse using WebsocketResponse for easier access
            ws_response = WebsocketResponse(data)
            channel = ws_response.channel
            
            # Basic logging to reduce noise, increase level if needed
            if channel not in ["ticker", "heartbeats"]:
                logger.info(f"Received message on channel '{channel}'")
            else:
                logger.debug(f"Received message on channel '{channel}'")

            # Process based on channel type
            if channel == "ticker" and self.message_queue:
                for event in ws_response.events:
                    for ticker in event.tickers:
                        # Put relevant ticker data onto the queue
                        ticker_data = {
                            'type': 'ticker',
                            'product_id': ticker.product_id,
                            'price': ticker.price,
                            'volume_24_h': ticker.volume_24_h,
                            'time': ws_response.timestamp # Use message timestamp
                        }
                        try:
                            # Use asyncio.create_task for non-blocking put
                            # Requires the main application to have a running event loop
                            asyncio.create_task(self.message_queue.put(ticker_data))
                        except Exception as e:
                            logger.error(f"Error putting message on queue: {e}")

            elif channel == "heartbeats":
                # Heartbeats are useful for checking connection health, but maybe not needed in queue
                logger.debug(f"Heartbeat received: {ws_response.timestamp}")
                
            elif channel == "user" and self.message_queue:
                for event in ws_response.events:
                    if event.type == "snapshot": # Initial order state (ignore for now)
                        logger.info("User channel snapshot received.")
                        continue 
                    # Process actual order updates
                    for order in event.orders:
                        # Check if order is considered filled/closed
                        if order.status in ["FILLED", "CANCELLED", "EXPIRED", "FAILED"]:
                            order_data = {
                                'type': 'user_order_update',
                                'order_id': order.order_id,
                                'client_order_id': order.client_order_id,
                                'product_id': order.product_id,
                                'side': order.side,
                                'status': order.status,
                                'cumulative_quantity': order.cumulative_quantity,
                                'total_fees': order.total_fees,
                                'average_filled_price': order.average_filled_price,
                                'time': ws_response.timestamp
                            }
                            logger.info(f"Putting order update onto queue: {order.order_id} ({order.status})")
                            asyncio.create_task(self.message_queue.put(order_data))

            elif channel == "subscriptions":
                 logger.info(f"Subscription confirmation received: {data}")

            else:
                logger.debug(f"Unhandled message on channel '{channel}': {data}")

        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON message: {msg}")
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {e}", exc_info=True)
            if self._on_error_callback:
                self._on_error_callback(e)

    def connect(self):
        """Establishes the WebSocket connection and starts listening."""
        if self._is_running:
            logger.warning("WebSocket client is already running.")
            return

        logger.info(f"Connecting to WebSocket with products={self.product_ids}, channels={self.channels}...")
        self.ws_client = WSClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            on_message=self._on_message,
            on_open=self._on_open,
            on_close=self._on_close,
            retry=self._should_retry,
            verbose=self._verbose
            # TODO: Consider adding on_error handling if WSClient provides it
        )
        
        try:
            # open() starts the client in a separate thread
            self.ws_client.open()
            self._is_running = True
            logger.info("WebSocket client opened successfully.")
            # Keep the main thread alive or manage lifecycle via FastAPI/other framework
            # For simple testing, could use: self.ws_client.run_forever_with_exception_check()
            # but that blocks. We want it running in the background.
        except (WSClientException, WSClientConnectionClosedException) as e:
             logger.error(f"WebSocket connection failed: {e}")
             self._is_running = False
             if self._on_error_callback:
                 self._on_error_callback(e)
        except Exception as e:
            logger.error(f"Unexpected error during WebSocket connect: {e}", exc_info=True)
            self._is_running = False
            if self._on_error_callback:
                self._on_error_callback(e)


    def subscribe(self):
        """Subscribes to the specified products and channels."""
        if not self.ws_client:
            logger.error("WebSocket client not initialized. Call connect() first.")
            return
            
        logger.info(f"Subscribing to channels {self.channels} for products {self.product_ids}")
        try:
            self.ws_client.subscribe(product_ids=self.product_ids, channels=self.channels)
        except Exception as e:
            logger.error(f"Error subscribing to WebSocket channels: {e}", exc_info=True)
            if self._on_error_callback:
                 self._on_error_callback(e)

    def unsubscribe(self):
        """Unsubscribes from the specified products and channels."""
        if not self.ws_client or not self._is_running :
            logger.warning("WebSocket client not connected or running.")
            return
            
        logger.info(f"Unsubscribing from channels {self.channels} for products {self.product_ids}")
        try:
            self.ws_client.unsubscribe(product_ids=self.product_ids, channels=self.channels)
        except Exception as e:
            logger.error(f"Error unsubscribing from WebSocket channels: {e}", exc_info=True)
            if self._on_error_callback:
                 self._on_error_callback(e)

    def close(self):
        """Closes the WebSocket connection."""
        if not self.ws_client or not self._is_running:
            logger.warning("WebSocket client not connected or running.")
            return
            
        logger.info("Closing WebSocket connection...")
        try:
            self.ws_client.close()
            # _on_close callback will set self._is_running to False
        except Exception as e:
            logger.error(f"Error closing WebSocket connection: {e}", exc_info=True)
            if self._on_error_callback:
                 self._on_error_callback(e)
            # Force state update even if close fails
            self._is_running = False
        finally:
             self.ws_client = None


# Example Usage (for testing purposes, normally integrated into FastAPI)
async def example_ws_run():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Load credentials (replace with your actual key loading mechanism)
    # Ensure these are set correctly
    settings = Settings() # Uses .env
    api_key = settings.COINBASE_JWT_KEY_NAME
    api_secret = settings.COINBASE_JWT_PRIVATE_KEY
    
    if not api_key or not api_secret:
        logger.error("API Key or Secret not found. Set COINBASE_JWT_KEY_NAME and COINBASE_JWT_PRIVATE_KEY environment variables.")
        return

    message_queue = asyncio.Queue()
    product_ids = ["BTC-USD", "ETH-USD"]
    channels = ["ticker", "heartbeats"] # Add "user" for order updates

    def handle_error(e: Exception):
        logger.error(f"WebSocket Error Callback: {e}")

    ws_client_wrapper = CoinbaseWebSocketClient(
        api_key=api_key,
        api_secret=api_secret,
        product_ids=product_ids,
        channels=channels,
        message_queue=message_queue,
        on_error=handle_error,
        verbose=False # Set to True for more logs
    )

    try:
        ws_client_wrapper.connect()
        
        # Keep running and process messages from the queue
        start_time = time.time()
        while ws_client_wrapper._is_running and (time.time() - start_time) < 30: # Run for 30 seconds
            try:
                message = await asyncio.wait_for(message_queue.get(), timeout=1.0)
                if message:
                     logger.info(f"Received from queue: {message}")
                message_queue.task_done()
            except asyncio.TimeoutError:
                # No message received in the last second, continue loop
                continue
            except Exception as e:
                 logger.error(f"Error processing queue message: {e}")
                 # Potentially break or handle differently
                 break
                 
        logger.info("Example run finished or client stopped.")

    except Exception as e:
        logger.error(f"An error occurred during example run: {e}")
    finally:
        logger.info("Cleaning up WebSocket client...")
        ws_client_wrapper.close()
        # Ensure background tasks are cancelled if any were created for queue processing
        # (This example uses a simple loop, but in FastAPI you might have tasks)

# To run this example:
# if __name__ == "__main__":
#     asyncio.run(example_ws_run()) 