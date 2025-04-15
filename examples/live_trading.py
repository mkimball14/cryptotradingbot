import asyncio
import logging
import os
import json # Import json library
from pathlib import Path # For path handling
import pandas as pd # Add pandas import
# Remove dotenv import
# from dotenv import load_dotenv
from app.core.config import Settings
from app.core.coinbase import CoinbaseClient
from app.core.websocket_client import CoinbaseWebSocketClient
from app.core.live_trader import LiveTrader
# Imports for DB and OrderExecutor
from app.core.order_executor import OrderExecutor
from app.core.trade_log.database import AsyncSessionFactory, init_db 
# Import logging specifics
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.trade_log.crud import create_log_entry
from app.core.trade_log.models import EventType, TradeSide, OrderStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Modify main to accept session_factory
async def main(session_factory: sessionmaker):
    # Load credentials from JSON file instead of .env
    # load_dotenv()
    creds = None
    creds_file_path = Path("cdp_api_key.json") # Assuming it's in the root
    if creds_file_path.exists():
        try:
            with open(creds_file_path, 'r') as f:
                creds = json.load(f)
            logger.info(f"Loaded credentials from {creds_file_path}")
        except Exception as e:
            logger.error(f"Failed to load credentials from {creds_file_path}: {e}")
            creds = None # Ensure creds is None if loading fails
    else:
        logger.error(f"Credentials file not found: {creds_file_path}")

    # Create settings object using JSON creds or None if failed
    settings = Settings(
        # Use creds if available, otherwise None (will cause error later if needed)
        COINBASE_JWT_KEY_NAME=creds.get("name") if creds else None, 
        COINBASE_JWT_PRIVATE_KEY=creds.get("privateKey") if creds else None,
        # Keep loading other settings from environment variables as fallback
        TRADING_ENABLED=os.getenv('TRADING_ENABLED', 'false').lower() == 'true',
        RISK_PERCENTAGE=float(os.getenv('RISK_PERCENTAGE', '1.0')),
        MAX_OPEN_POSITIONS=int(os.getenv('MAX_OPEN_POSITIONS', '3'))
    )
    
    # Add a check here to ensure credentials loaded successfully before proceeding
    if not settings.COINBASE_JWT_KEY_NAME or not settings.COINBASE_JWT_PRIVATE_KEY:
        logger.critical("API credentials could not be loaded from JSON file. Exiting.")
        return # Stop execution if creds are missing
    
    # Initialize clients
    rest_client = CoinbaseClient(settings)
    ws_client = CoinbaseWebSocketClient(
        settings=settings,
        auto_reconnect=True,
        max_reconnect_attempts=10
    )
    
    # --- Add OrderExecutor --- 
    order_executor = OrderExecutor(client=rest_client)
    # --- End Add --- 
    
    # Initialize and start live trader
    # Pass order_executor and session_factory
    trader = LiveTrader(
        settings=settings,
        rest_client=rest_client,
        ws_client=ws_client,
        order_executor=order_executor, 
        session_factory=session_factory # Pass session factory
    )
    
    try:
        # Start trading BTC-USD by default
        await trader.start("BTC-USD")
        
        # --- Remove Message Queue Processing Loop --- 
        # Fill processing is now handled by the background task started in the lifespan
        # logger.info("Starting message queue processing loop...")
        # while trader.ws_client and trader.ws_client._is_running: # Check if trader and ws_client are active
        #     try:
        #         message = await asyncio.wait_for(trader.ws_client.message_queue.get(), timeout=1.0)
        #         if message:
        #              # ... (removed logging logic) ...
        #         if trader.ws_client.message_queue.empty():
        #             await asyncio.sleep(0.1)
        #         trader.ws_client.message_queue.task_done()
        #     except asyncio.TimeoutError:
        #         if not (trader.ws_client and trader.ws_client._is_running):
        #             break
        #         continue
        #     except Exception as e:
        #          logger.error(f"Error processing queue message: {e}", exc_info=True)
        #          await asyncio.sleep(1) 
        # --- End Removed Loop --- 
                 
    except KeyboardInterrupt:
        logger.info("Stopping trader due to keyboard interrupt...")
    except Exception as e:
        logger.error(f"Error in live trading: {e}")
    finally:
        await trader.stop()

if __name__ == "__main__":
    async def run_main():
        # Initialize DB first
        logger.info("Initializing trade log database...")
        await init_db()
        logger.info("Database initialized.")
        
        # Run the main trader logic, passing the session factory
        await main(AsyncSessionFactory)
        
    asyncio.run(run_main()) 