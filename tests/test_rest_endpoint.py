import asyncio
import logging
from app.core.config import get_settings
from app.core.coinbase import CoinbaseClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def test_different_endpoints():
    """Test different Coinbase REST API endpoints"""
    settings = get_settings()
    logger.info("Testing alternative Coinbase REST API endpoints...")
    
    try:
        # Initialize REST client
        client = CoinbaseClient(settings)
        
        # Try multiple endpoints to see which ones work
        
        # Test 1: Get accounts (requires different permissions)
        logger.info("\n1. Testing get_accounts() endpoint:")
        try:
            accounts = await client.get_accounts()
            logger.info(f"✅ get_accounts() successful: {accounts[:2]}")
        except Exception as e:
            logger.error(f"❌ get_accounts() failed: {str(e)}")
        
        # Test 2: Get product candles for BTC-USD
        logger.info("\n2. Testing get_product_candles() endpoint:")
        try:
            candles = await client.get_product_candles(
                product_id="BTC-USD",
                granularity="ONE_HOUR"
            )
            logger.info(f"✅ get_product_candles() successful: {candles[:2] if candles else 'No data'}")
        except Exception as e:
            logger.error(f"❌ get_product_candles() failed: {str(e)}")
        
        # Test 3: Get market trades
        logger.info("\n3. Testing get_market_trades() endpoint:")
        try:
            trades = await client.get_market_trades("BTC-USD")
            logger.info(f"✅ get_market_trades() successful: {trades[:2] if trades else 'No data'}")
        except Exception as e:
            logger.error(f"❌ get_market_trades() failed: {str(e)}")
            
        # Test 4: Get order book
        logger.info("\n4. Testing get_order_book() endpoint:")
        try:
            order_book = await client.get_order_book("BTC-USD")
            logger.info(f"✅ get_order_book() successful: {str(order_book)[:100]}...")
        except Exception as e:
            logger.error(f"❌ get_order_book() failed: {str(e)}")
            
    except Exception as e:
        logger.error(f"General error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_different_endpoints()) 