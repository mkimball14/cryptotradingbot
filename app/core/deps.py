from functools import lru_cache
from typing import AsyncGenerator
import logging

from app.core.config import Settings
from app.core.coinbase import CoinbaseClient
from app.core.websocket_client import CoinbaseWebSocketClient

# Configure logging
logger = logging.getLogger(__name__)

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching
    """
    try:
        settings = Settings()
        logger.debug("Settings loaded successfully")
        return settings
    except Exception as e:
        logger.error(f"Error loading settings: {str(e)}")
        raise

def get_coinbase_client() -> CoinbaseClient:
    """
    Get Coinbase client instance
    """
    try:
        settings = get_settings()
        client = CoinbaseClient(settings)
        logger.debug("Coinbase REST client initialized")
        return client
    except Exception as e:
        logger.error(f"Error initializing Coinbase client: {str(e)}")
        raise

async def get_websocket_client() -> AsyncGenerator[CoinbaseWebSocketClient, None]:
    """
    Get Coinbase WebSocket client instance as an async context manager
    """
    try:
        settings = get_settings()
        ws_client = CoinbaseWebSocketClient(settings)
        logger.debug("Coinbase WebSocket client initialized")
        yield ws_client
    except Exception as e:
        logger.error(f"Error initializing WebSocket client: {str(e)}")
        raise
    finally:
        if ws_client and ws_client.is_connected:
            await ws_client.close()
            logger.debug("WebSocket client closed") 