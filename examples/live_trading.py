import asyncio
import logging
import os
from dotenv import load_dotenv
from app.core.config import Settings
from app.core.coinbase import CoinbaseClient
from app.core.websocket_client import CoinbaseWebSocketClient
from app.core.live_trader import LiveTrader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Load environment variables
    load_dotenv()
    
    # Create settings object
    settings = Settings(
        COINBASE_JWT_KEY_NAME=os.getenv('COINBASE_JWT_KEY_NAME'),
        COINBASE_JWT_PRIVATE_KEY=os.getenv('COINBASE_JWT_PRIVATE_KEY'),
        TRADING_ENABLED=os.getenv('TRADING_ENABLED', 'false').lower() == 'true',
        RISK_PERCENTAGE=float(os.getenv('RISK_PERCENTAGE', '1.0')),
        MAX_OPEN_POSITIONS=int(os.getenv('MAX_OPEN_POSITIONS', '3'))
    )
    
    # Initialize clients
    rest_client = CoinbaseClient(settings)
    ws_client = CoinbaseWebSocketClient(
        settings=settings,
        auto_reconnect=True,
        max_reconnect_attempts=10
    )
    
    # Initialize and start live trader
    trader = LiveTrader(settings, rest_client, ws_client)
    
    try:
        # Start trading BTC-USD by default
        await trader.start("BTC-USD")
    except KeyboardInterrupt:
        logger.info("Stopping trader due to keyboard interrupt...")
    except Exception as e:
        logger.error(f"Error in live trading: {e}")
    finally:
        await trader.stop()

if __name__ == "__main__":
    asyncio.run(main()) 