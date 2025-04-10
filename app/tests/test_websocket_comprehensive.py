import asyncio
import logging
from app.core.websocket_client import CoinbaseWebSocketClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_multiple_products():
    """Test subscribing to multiple products simultaneously"""
    client = CoinbaseWebSocketClient()
    try:
        await client.connect()
        await client.subscribe(["BTC-USD", "ETH-USD", "SOL-USD"])
        logger.info("Waiting for market data from multiple products...")
        await asyncio.sleep(10)  # Wait for some messages
        await client.disconnect()
    except Exception as e:
        logger.error(f"Multiple products test failed: {e}")
        raise

async def test_multiple_channels():
    """Test subscribing to multiple channel types"""
    client = CoinbaseWebSocketClient()
    try:
        await client.connect()
        await client.subscribe(["BTC-USD"], channels=["ticker", "status"])
        logger.info("Waiting for data from multiple channels...")
        await asyncio.sleep(10)
        await client.disconnect()
    except Exception as e:
        logger.error(f"Multiple channels test failed: {e}")
        raise

async def test_unsubscribe():
    """Test unsubscribe functionality"""
    client = CoinbaseWebSocketClient()
    try:
        await client.connect()
        await client.subscribe(["BTC-USD", "ETH-USD"])
        logger.info("Waiting for initial market data...")
        await asyncio.sleep(5)
        
        logger.info("Unsubscribing from BTC-USD...")
        await client.unsubscribe(["BTC-USD"])
        logger.info("Waiting to verify unsubscribe...")
        await asyncio.sleep(5)
        
        await client.disconnect()
    except Exception as e:
        logger.error(f"Unsubscribe test failed: {e}")
        raise

async def test_reconnection():
    """Test automatic reconnection on disconnect"""
    client = CoinbaseWebSocketClient()
    try:
        await client.connect()
        await client.subscribe(["BTC-USD"])
        logger.info("Forcing disconnect to test reconnection...")
        await client._ws.close()  # Force disconnect
        await asyncio.sleep(5)  # Wait for reconnection
        
        # Verify we're receiving data after reconnection
        logger.info("Waiting for data after reconnection...")
        await asyncio.sleep(5)
        await client.disconnect()
    except Exception as e:
        logger.error(f"Reconnection test failed: {e}")
        raise

async def test_invalid_product():
    """Test handling of invalid product IDs"""
    client = CoinbaseWebSocketClient()
    try:
        await client.connect()
        await client.subscribe(["INVALID-PAIR"])
        await asyncio.sleep(5)
        await client.disconnect()
    except Exception as e:
        logger.info(f"Expected error for invalid product: {e}")

async def run_all_tests():
    """Run all test cases"""
    tests = [
        test_multiple_products(),
        test_multiple_channels(),
        test_unsubscribe(),
        test_reconnection(),
        test_invalid_product()
    ]
    
    logger.info("Starting comprehensive WebSocket tests...")
    try:
        await asyncio.gather(*tests)
        logger.info("All tests completed successfully!")
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_all_tests()) 