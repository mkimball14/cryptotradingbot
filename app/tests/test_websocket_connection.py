import asyncio
import logging
import os
from app.core.websocket_client import CoinbaseWebSocketClient
from app.core.config import Settings
from pydantic_settings import SettingsConfigDict

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the path to the key file
KEY_FILE = "cdp_api_key (3).json"

async def test_websocket_connection():
    """Test WebSocket connection and subscription."""
    # Check if key file exists
    if not os.path.exists(KEY_FILE):
        logger.error(f"API key file not found: {KEY_FILE}")
        logger.error("Make sure the API key file is in the project root directory.")
        return
        
    logger.info(f"Using API key file: {os.path.abspath(KEY_FILE)}")
    
    # Initialize client with key file
    client = CoinbaseWebSocketClient(
        key_file=KEY_FILE,
        on_message=lambda msg: logger.info(f"Received message: {msg}")
    )
    
    try:
        # Connect to WebSocket
        await client.connect()
        assert client.is_connected, "WebSocket should be connected"
        
        # Subscribe to a test product
        product_ids = ["BTC-USD"]
        channels = ["ticker"]
        await client.subscribe(product_ids=product_ids, channels=channels)
        
        # Wait for a few messages
        message_count = 0
        max_messages = 3
        timeout = 10  # seconds
        
        async def message_handler():
            nonlocal message_count
            try:
                while message_count < max_messages:
                    message = await asyncio.wait_for(client.websocket.recv(), timeout=timeout)
                    logger.info(f"Received message: {message}")
                    message_count += 1
            except asyncio.TimeoutError:
                logger.warning("Timeout waiting for messages")
            except Exception as e:
                logger.error(f"Error in message handler: {str(e)}")
                raise
        
        # Run message handler
        await message_handler()
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        # Cleanup
        if client.is_connected:
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_websocket_connection()) 