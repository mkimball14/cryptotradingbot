import asyncio
import logging
import json
import time
from datetime import datetime
from app.core.config import get_settings
from app.core.websocket_client import CoinbaseWebSocketClient
from collections import defaultdict
import asyncio # Added Queue
from asyncio import Queue # Added Queue

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
    "successful_connections": 0, # Note: Direct callback for success is gone
    "errors": 0,
    "messages_received": 0, # Total messages processed from the queue
    "message_types": defaultdict(int),
    "products": defaultdict(int),
    "message_intervals": [],
    "last_message_time": 0
}

async def main_on_message(message):
    """Main processor for messages from the queue, updates global stats."""
    # Message format is now a dictionary from the client's queue
    # e.g., {'type': 'ticker', 'product_id': ..., 'price': ..., ...}
    # e.g., {'type': 'user_order_update', ...}
    # Errors from the WS feed itself might not be put on the queue, only processing errors via _on_error_callback
    
    stats["messages_received"] += 1
    
    msg_type = message.get("type") # e.g., 'ticker', 'user_order_update'
    product_id = message.get("product_id", "unknown_product")

    if not msg_type:
        logger.warning(f"Main Handler - Received message with no type from queue: {message}")
        return # Cannot process further without type

    stats["message_types"][msg_type] += 1
    
    # Note: Error messages from the WS feed might not appear here. Errors are handled by on_error callback.
    # This section now primarily counts data messages.
    
    if msg_type in ["ticker", "user_order_update"]: # Add other types if client puts them on queue
        if product_id != "unknown_product":
            stats["products"][product_id] += 1
            logger.info(f"Main Handler - Processed {msg_type} for {product_id} from queue")
        else:
            logger.warning(f"Main Handler - Processed {msg_type} with unknown product_id from queue: {message}")
    else:
        # Log other message types received from the queue if any
         logger.info(f"Main Handler - Processed message type {msg_type} from queue: {message}")

    # Record timing and sequence of messages processed from the queue
    current_time = time.time()
    if stats["last_message_time"] > 0:
        time_diff = current_time - stats["last_message_time"]
        stats["message_intervals"].append(time_diff)
    stats["last_message_time"] = current_time

# Note: on_connect is no longer directly used by the client wrapper.
# We infer connection success if connect() doesn't immediately error out via on_error.
# async def on_connect():
#     """Callback for when connection is established"""
#     stats["successful_connections"] += 1
#     stats["connection_attempts"] += 1 # Increment attempts on successful connect too
#     logger.info("✅ CONNECTED to WebSocket server!")

async def on_error(error):
    """Callback for when an error occurs (passed to client)"""
    stats["errors"] += 1
    logger.error(f"❌ WebSocket Client Error Callback: {error}", exc_info=True)

# Note: on_disconnect is no longer directly used. Closure is logged by the client itself.
# async def on_disconnect():
#     """Callback for when the connection is closed"""
#     logger.info("DISCONNECTED from WebSocket server")

async def test_websocket_channels():
    """Test different WebSocket channels with detailed diagnostics using queue."""
    logger.info("Starting comprehensive WebSocket channel test...")
    
    # Reset stats at the beginning of the test
    global stats
    stats = {
        "connection_attempts": 0,
        "successful_connections": 0, # This stat might be less reliable now
        "errors": 0,
        "messages_received": 0, 
        "message_types": defaultdict(int),
        "products": defaultdict(int),
        "message_intervals": [],
        "last_message_time": 0
    }
    
    # Load settings
    try:
        settings = get_settings()
        # Use JWT key name/secret for WebSocket auth as per Coinbase docs for WSClient
        api_key = settings.COINBASE_JWT_KEY_NAME
        api_secret = settings.COINBASE_JWT_PRIVATE_KEY
        if not api_key or not api_secret:
            raise ValueError("API Key or Secret not found in settings.")
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        return

    message_queue = Queue()
    connection_event = asyncio.Event() # Create the event

    # Initialize the client wrapper
    loop = asyncio.get_running_loop() # Get the current event loop
    client = CoinbaseWebSocketClient(
        api_key=api_key,
        api_secret=api_secret,
        product_ids=[], # Start with empty, subscribe per test
        channels=[],    # Start with empty, subscribe per test
        message_queue=message_queue,
        on_error=on_error, # Pass our error handler
        loop=loop,         # Pass the event loop
        retry=True,        # Enable auto-reconnect
        connection_established_event=connection_event, # Pass the event
        verbose=True      # Set True for more SDK logs if needed
    )
    
    try:
        # Connect to WebSocket (starts in background thread)
        logger.info("Connecting to WebSocket...")
        stats["connection_attempts"] += 1 # Log initial attempt
        client.connect() # Doesn't return status directly, relies on internal logging/on_error
        
        # Wait for the connection to be fully established using the event
        logger.info("Waiting for connection to be established...")
        try:
            await asyncio.wait_for(connection_event.wait(), timeout=10.0) # Wait up to 10 seconds
        except asyncio.TimeoutError:
            logger.error("Connection timed out after 10 seconds. Aborting test.")
            # Close client if possible
            if client: client.close()
            return
        except Exception as e:
            logger.error(f"Error waiting for connection event: {e}", exc_info=True)
            if client: client.close()
            return
        
        # Check if the client seems to be running (basic check)
        if not client._is_running:
             logger.error("Client failed to start or connect (check logs above). Aborting test.")
             # Manually increment error count if needed, although on_error should handle it
             if stats["errors"] == 0: stats["errors"] += 1 # Ensure connect failure is counted
             return # Exit if connection failed

        # Assuming connection likely succeeded if no error was logged by on_error
        stats["successful_connections"] += 1 # Increment success count here (best guess)
        logger.info("✅ Connection likely established (no immediate error). Proceeding with tests.")


        # Subscribe to channels one by one
        test_channels = [
            # Channel name, product ID list, expected message count (approximate)
            ("ticker", ["BTC-USD"], 5),
            # ("candles", ["ETH-USD"], 2), # Candles might not be directly supported or put on queue by WSClient wrapper
            ("market_trades", ["BTC-USD"], 5), # Market trades might also not be on queue
            # ("user", ["BTC-USD"], 1) # User channel requires specific setup/orders
            ("heartbeats", ["BTC-USD"], 3) # Heartbeats are processed internally but good for testing connection
        ]
        
        # Test each channel in sequence
        for channel, products, expected_msgs in test_channels:
            logger.info(f"Testing channel: {channel} for products: {products}")
            
            channel_message_count = 0
            channel_start_time = time.time()
            
            # Subscribe to the channel
            # Note: subscribe() in the wrapper might not return success status directly
            logger.info(f"Attempting to subscribe to {channel}...")
            client.subscribe(product_ids=products, channels=[channel])
            await asyncio.sleep(2) # Wait for subscription confirmation (logged internally)

            # Wait for messages by consuming from the queue
            max_wait = 20  # Increased wait time per channel
            wait_interval = 1.0 # Check queue every second
            waited = 0
            
            logger.info(f"Waiting for messages on channel {channel} via queue...")
            while waited < max_wait:
                try:
                    # Wait for a message from the queue
                    message = await asyncio.wait_for(message_queue.get(), timeout=wait_interval)
                    if message:
                        # Process the message using our handler to update stats
                        await main_on_message(message)
                        # Check if the message is relevant to the current test channel
                        # This requires main_on_message to correctly parse type/product
                        msg_type = message.get("type") 
                        msg_product = message.get("product_id")
                        
                        # Determine if message matches current test criteria
                        # This logic might need refinement based on actual queued messages
                        is_match = False
                        if channel == "ticker" and msg_type == "ticker" and msg_product in products:
                            is_match = True
                        elif channel == "heartbeats": # Heartbeats might not appear in queue, check client logs
                             pass # No specific message expected in queue for heartbeats usually
                        elif channel == "market_trades" and msg_type == "market_trade" and msg_product in products: # Corrected type check to singular
                            is_match = True 
                        # Add checks for other channels like 'user' if tested and queued

                        if is_match:
                             channel_message_count += 1
                             logger.info(f"[Test Runner] Processed message #{channel_message_count} matching {channel}/{products} from queue.")

                    message_queue.task_done() # Mark message as processed

                    # Check if we've received enough messages for this channel
                    if channel_message_count >= expected_msgs:
                        logger.info(f"Reached expected message count for {channel}.")
                        break 

                except asyncio.TimeoutError:
                    # No message received in the last interval
                    logger.debug(f"No message for {channel} in the last {wait_interval}s...")
                    waited += wait_interval
                    if waited % 5 < wait_interval: # Log progress less frequently
                        logger.info(f"Still waiting for {channel} messages: {channel_message_count}/{expected_msgs} processed, {waited:.1f}s elapsed")
                except Exception as e:
                     logger.error(f"Error processing queue message during {channel} test: {e}", exc_info=True)
                     stats["errors"] += 1
                     break # Exit channel test on processing error
            
            # --- End of message wait loop ---

            # Results for this channel
            elapsed = time.time() - channel_start_time
            logger.info(f"Channel {channel} test results:")
            logger.info(f"  - Processed {channel_message_count} matching messages from queue in {elapsed:.1f} seconds")
            logger.info(f"  - Expected approx: {expected_msgs} messages")
            
            if channel_message_count == 0 and expected_msgs > 0:
                # Check if the channel is expected to put messages on the queue
                if channel not in ["heartbeats"]: # Adjust if other channels don't queue
                     logger.error(f"NO MATCHING MESSAGES PROCESSED FROM QUEUE FOR CHANNEL {channel}")
                else:
                     logger.info(f"No messages expected in queue for {channel}, check client logs for activity.")
            elif channel_message_count < expected_msgs:
                logger.warning(f"FEWER MESSAGES PROCESSED THAN EXPECTED FOR CHANNEL {channel}")
            else:
                logger.info(f"Channel {channel} message count test PASSED")
            
            # Unsubscribe before moving to next channel
            logger.info(f"Unsubscribing from channel {channel}...")
            client.unsubscribe(product_ids=products, channels=[channel])
            await asyncio.sleep(2) # Wait for unsubscribe action
        
        # --- End of channel loop ---

        # Final statistics (should now be based on queued messages processed)
        logger.info("\n" + "="*50)
        logger.info("WEBSOCKET TEST SUMMARY")
        logger.info("="*50)
        logger.info(f"Total messages processed from queue: {stats['messages_received']}")
        logger.info(f"Connection attempts: {stats['connection_attempts']}")
        logger.info(f"Successful connections (inferred): {stats['successful_connections']}")
        logger.info(f"Errors reported by client/callbacks: {stats['errors']}")
        logger.info(f"Message types processed from queue: {dict(stats['message_types'])}") 
            
        logger.info("Products with data processed from queue:")
        if stats['products']:
            for product, count in stats['products'].items():
                logger.info(f"  - {product}: {count} messages")
        else:
            logger.info("  - No product-specific messages processed from queue.")
            
        if stats['message_intervals']:
            avg_interval = sum(stats['message_intervals']) / len(stats['message_intervals'])
            logger.info(f"Average message processing interval: {avg_interval:.3f} seconds")
            
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Error during WebSocket test execution: {str(e)}", exc_info=True)
        stats["errors"] += 1 # Ensure test execution errors are counted
    finally:
        # Disconnect cleanly using close()
        logger.info("Test complete, closing connection...")
        if client: # Check if client was initialized
             client.close()
        logger.info("WebSocket client closed.")

if __name__ == "__main__":
    asyncio.run(test_websocket_channels()) 