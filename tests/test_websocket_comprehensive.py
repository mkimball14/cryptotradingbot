import asyncio
import logging
import json
import time
from datetime import datetime
from app.core.config import get_settings
from app.core.websocket_client import CoinbaseWebSocketClient
from collections import defaultdict

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('websocket_debug.log')
    ]
)
logger = logging.getLogger("websocket_test")

# Global stats dictionary
stats = {
    "connection_attempts": 0,
    "successful_connections": 0,
    "errors": 0,
    "messages_received": 0, # Total messages received by the main handler
    "message_types": defaultdict(int),
    "products": defaultdict(int),
    "message_intervals": [],
    "last_message_time": 0
}

async def main_on_message(message):
    """Main callback that updates global stats, always called."""
    stats["messages_received"] += 1
    msg_type = message.get("type")
    channel = message.get("channel")
    identifier = msg_type if msg_type else channel
    
    stats["message_types"][identifier] += 1

    if identifier == "error":
        stats["errors"] += 1
        logger.error(f"Main Handler - WebSocket error: {message.get('message', 'Unknown error')}")
    elif identifier == "subscriptions":
        logger.info(f"Main Handler - Subscription update: {json.dumps(message)}")
    elif identifier in ["ticker", "candles", "market_trades", "level2"]:
        # Extract product ID from the events list (structure varies slightly by channel)
        product_id = "unknown_product"
        events = message.get("events", [])
        if events:
            first_event = events[0]
            if identifier == "ticker":
                product_id = first_event.get("tickers", [{}])[0].get("product_id", product_id)
            elif identifier == "candles":
                product_id = first_event.get("candles", [{}])[0].get("product_id", product_id)
            elif identifier == "market_trades":
                 product_id = first_event.get("trades", [{}])[0].get("product_id", product_id)
            elif identifier == "level2":
                 product_id = first_event.get("product_id", product_id) # Level2 often has product_id directly in the event
        
        if product_id != "unknown_product":
            stats["products"][product_id] += 1
            logger.info(f"Main Handler - Received {identifier} for {product_id}")
    elif identifier == "unknown":
        logger.warning(f"Main Handler - Unknown message type/channel: {json.dumps(message)[:200]}...")
            
    # Record timing and sequence of messages
    current_time = time.time()
    if stats["last_message_time"] > 0:
        time_diff = current_time - stats["last_message_time"]
        stats["message_intervals"].append(time_diff)
    stats["last_message_time"] = current_time

async def on_connect():
    """Callback for when connection is established"""
    stats["successful_connections"] += 1
    stats["connection_attempts"] += 1 # Increment attempts on successful connect too
    logger.info("✅ CONNECTED to WebSocket server!")

async def on_error(error):
    """Callback for when an error occurs"""
    stats["errors"] += 1
    logger.error(f"❌ WebSocket Error: {error}", exc_info=True)

async def on_disconnect():
    """Callback for when the connection is closed"""
    logger.info("DISCONNECTED from WebSocket server")

async def test_websocket_channels():
    """Test different WebSocket channels with detailed diagnostics"""
    logger.info("Starting comprehensive WebSocket channel test...")
    
    # Reset stats at the beginning of the test
    global stats
    stats = {
        "connection_attempts": 0,
        "successful_connections": 0,
        "errors": 0,
        "messages_received": 0, 
        "message_types": defaultdict(int),
        "products": defaultdict(int),
        "message_intervals": [],
        "last_message_time": 0
    }
    
    client = CoinbaseWebSocketClient(
        on_message=main_on_message, # Use the main handler here
        on_connect=on_connect,
        on_error=on_error,
        on_disconnect=on_disconnect,
        auto_reconnect=True,
        max_reconnect_attempts=3
    )
    
    try:
        # Connect to WebSocket
        logger.info("Connecting to WebSocket...")
        stats["connection_attempts"] += 1 # Log initial attempt
        connected = await client.connect()
        if not connected:
            logger.error("Failed to connect to WebSocket")
            return
        
        # Wait for connection to stabilize
        logger.info("Waiting for connection to stabilize...")
        await asyncio.sleep(2)
        
        # Subscribe to channels one by one with delay between
        test_channels = [
            # Channel name, product ID list, expected message count (approximate)
            ("ticker", ["BTC-USD"], 5),
            ("candles", ["ETH-USD"], 2),
            ("market_trades", ["BTC-USD"], 5),
        ]
        
        # Test each channel in sequence
        for channel, products, expected_msgs in test_channels:
            logger.info(f"Testing channel: {channel} for products: {products}")
            
            # Use a simple counter for this specific channel test, separate from global stats
            channel_message_count = 0
            channel_start_time = time.time()
            
            # --- Define a temporary handler just for logging during this channel's test --- 
            async def temp_channel_logger(message):
                # This handler *only* logs messages relevant to the current channel test
                # It does NOT modify the global stats dictionary.
                nonlocal channel_message_count
                msg_channel = message.get("channel")
                if msg_channel == channel:
                     channel_message_count += 1
                     logger.info(f"[Test Logger] Received message #{channel_message_count} for channel {channel}")
                # Important: Call the main handler to update global stats
                await main_on_message(message)
            
            # Temporarily override the client's handler
            original_handler = client.on_message
            client.on_message = temp_channel_logger
            # ---------------------------------------------------------------------------
            
            # Subscribe to the channel
            subscribe_success = await client.subscribe(products, channel)
            logger.info(f"Subscription to {channel} {'successful' if subscribe_success else 'failed'}")
            
            if subscribe_success:
                # Wait for messages (with timeout)
                max_wait = 15  # seconds
                wait_interval = 0.5
                waited = 0
                
                logger.info(f"Waiting for messages on channel {channel}...")
                while waited < max_wait and channel_message_count < expected_msgs:
                    await asyncio.sleep(wait_interval)
                    waited += wait_interval
                    
                    # Progress update every 3 seconds
                    if waited % 3 < wait_interval:
                        logger.info(f"Waiting for {channel} messages: {channel_message_count}/{expected_msgs} received, {waited:.1f}s elapsed")
                
                # Results for this channel
                elapsed = time.time() - channel_start_time
                logger.info(f"Channel {channel} test results:")
                logger.info(f"  - Logged {channel_message_count} messages for this test in {elapsed:.1f} seconds")
                logger.info(f"  - Expected approx: {expected_msgs} messages")
                
                if channel_message_count == 0:
                    logger.error(f"NO MESSAGES LOGGED BY TEMP HANDLER FOR CHANNEL {channel}")
                elif channel_message_count < expected_msgs:
                    logger.warning(f"FEWER MESSAGES LOGGED THAN EXPECTED FOR CHANNEL {channel}")
                else:
                    logger.info(f"Channel {channel} test logging PASSED")
                
                # Unsubscribe before moving to next channel
                await client.unsubscribe(products, channel)
                logger.info(f"Unsubscribed from channel {channel}")
                
                # Wait between tests
                await asyncio.sleep(2)
            
            # Restore original message handler
            client.on_message = original_handler
        
        # Final statistics (should now be accurate)
        logger.info("\n" + "="*50)
        logger.info("WEBSOCKET TEST SUMMARY")
        logger.info("="*50)
        logger.info(f"Total messages received by main handler: {stats['messages_received']}")
        logger.info(f"Connection attempts: {stats['connection_attempts']}")
        logger.info(f"Successful connections: {stats['successful_connections']}")
        logger.info(f"Errors reported by client/callbacks: {stats['errors']}")
        logger.info(f"Message types/channels received by main handler: {dict(stats['message_types'])}") # Convert defaultdict for printing
            
        logger.info("Products with data received by main handler:")
        for product, count in stats['products'].items():
            logger.info(f"  - {product}: {count} messages")
            
        if stats['message_intervals']:
            avg_interval = sum(stats['message_intervals']) / len(stats['message_intervals'])
            logger.info(f"Average message interval: {avg_interval:.3f} seconds")
            
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Error during WebSocket test: {str(e)}", exc_info=True)
    finally:
        # Disconnect cleanly
        logger.info("Test complete, disconnecting...")
        await client.disconnect()
        logger.info("Disconnected from WebSocket")

if __name__ == "__main__":
    asyncio.run(test_websocket_channels()) 