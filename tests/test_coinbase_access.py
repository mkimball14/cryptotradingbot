import asyncio
import logging
from app.core.config import get_settings
from app.core.coinbase import CoinbaseClient
from app.core.websocket_client import CoinbaseWebSocketClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Flag to track WebSocket connection status
ws_connected = False
ws_received_message = False

# Callback function for WebSocket messages
async def handle_message(message):
    global ws_received_message
    logger.info(f"WebSocket message received: {message.get('type', 'unknown')}")
    ws_received_message = True

# Callback for WebSocket connection
async def handle_connect():
    global ws_connected
    logger.info("Connected to Coinbase WebSocket!")
    ws_connected = True

async def test_rest_api():
    """Test access to Coinbase REST API"""
    settings = get_settings()
    logger.info("Testing Coinbase REST API access...")
    
    try:
        # Initialize REST client
        client = CoinbaseClient(settings)
        
        # Test getting products (simple endpoint that doesn't require specific permissions)
        response = await client.get_products()
        
        # Debug response type and content
        logger.debug(f"Response type: {type(response)}")
        logger.debug(f"Response preview: {str(response)[:200]}...")
        
        # Handle different response formats
        if isinstance(response, list):
            # Direct list of products
            product_list = response
        elif isinstance(response, dict):
            # Dict with products key
            if "products" in response:
                product_list = response["products"]
            else:
                product_list = []
        else:
            product_list = []
        
        if product_list:
            logger.info(f"✅ REST API access successful! Received {len(product_list)} products.")
            # Print first 3 products as a sample
            for i, product in enumerate(product_list[:3]):
                # Handle different product formats
                if isinstance(product, dict):
                    product_id = product.get("id", product.get("product_id", "unknown"))
                    logger.info(f"  - {product_id}")
                else:
                    logger.info(f"  - Product {i+1}: {str(product)[:50]}...")
            return True
        else:
            logger.error(f"❌ REST API returned no products")
            logger.error(f"Response content: {str(response)[:200]}...")
            return False
            
    except Exception as e:
        logger.error(f"❌ REST API access failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

async def test_websocket_api():
    """Test access to Coinbase WebSocket API"""
    global ws_connected, ws_received_message
    settings = get_settings()
    logger.info("Testing Coinbase WebSocket API access...")
    
    try:
        # Initialize WebSocket client with callbacks
        ws_client = CoinbaseWebSocketClient(
            settings=settings,
            on_message=handle_message,
            on_connect=handle_connect
        )
        
        # Try to connect
        await ws_client.connect()
        
        # Wait a moment for connection to establish
        await asyncio.sleep(2)
        
        if not ws_connected:
            logger.error("❌ WebSocket connection failed")
            return False
            
        # Try to subscribe to ticker for BTC-USD
        success = await ws_client.subscribe("BTC-USD", "ticker")
        
        if not success:
            logger.error("❌ WebSocket subscription failed")
            await ws_client.disconnect()
            return False
            
        logger.info("Waiting for messages (5 seconds)...")
        
        # Wait for messages
        await asyncio.sleep(5)
        
        # Clean up
        await ws_client.unsubscribe("BTC-USD", "ticker")
        await ws_client.disconnect()
        
        if ws_received_message:
            logger.info("✅ WebSocket API access successful! Received messages.")
            return True
        else:
            logger.warning("⚠️ WebSocket connected but no messages received in test period")
            return True  # Still consider this a success as connection worked
            
    except Exception as e:
        logger.error(f"❌ WebSocket API access failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    logger.info("=== Coinbase API Access Test ===")
    
    # Test REST API
    rest_success = await test_rest_api()
    
    # Add a separator
    logger.info("\n" + "-" * 50 + "\n")
    
    # Test WebSocket API
    ws_success = await test_websocket_api()
    
    # Summarize results
    logger.info("\n=== Test Results ===")
    logger.info(f"REST API Access: {'✅ SUCCESS' if rest_success else '❌ FAILED'}")
    logger.info(f"WebSocket API Access: {'✅ SUCCESS' if ws_success else '❌ FAILED'}")
    
    if rest_success and ws_success:
        logger.info("\n✅ YOU HAVE FULL ACCESS TO COINBASE API! ✅")
    elif rest_success:
        logger.info("\n⚠️ You have REST API access but WebSocket API is not working.")
    elif ws_success:
        logger.info("\n⚠️ You have WebSocket API access but REST API is not working.")
    else:
        logger.info("\n❌ No access to Coinbase API. Please check your API credentials.")

if __name__ == "__main__":
    asyncio.run(main()) 