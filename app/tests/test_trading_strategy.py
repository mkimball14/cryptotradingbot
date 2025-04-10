import asyncio
import logging
import json
from datetime import datetime
from app.core.websocket_client import CoinbaseWebSocketClient
from app.core.trading_strategy import TradingStrategy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_trading_strategy():
    """Test the trading strategy with live market data."""
    
    # Initialize strategy with shorter windows for testing
    strategy = TradingStrategy(short_window=5, long_window=10)
    signals = []
    
    # Initialize WebSocket client
    client = CoinbaseWebSocketClient()
    
    try:
        # Connect and subscribe
        await client.connect()
        products = ["BTC-USD", "ETH-USD"]
        await client.subscribe(products)
        
        logger.info("Collecting market data and generating signals...")
        
        # Process messages for 2 minutes
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < 120:  # 2 minutes
            try:
                # Get message directly from the client's queue
                message_data = await client.get_next_message(timeout=1.0)
                if not message_data:
                    # No message received within timeout, continue
                    continue
                
                logger.debug(f"Received message type: {message_data.get('type', 'unknown')}")
                    
                # Check if it's a ticker message with the expected structure
                if message_data.get("channel") == "ticker" and message_data.get("events"):
                    logger.debug(f"Processing ticker message: {json.dumps(message_data, indent=2)}")
                    
                    for event in message_data["events"]:
                        if event.get("type") == "update" and event.get("tickers"):
                            for ticker in event["tickers"]:
                                logger.debug(f"Processing ticker: {json.dumps(ticker, indent=2)}")
                                
                                # Analyze ticker data
                                signal = strategy.analyze_ticker(ticker)
                                if signal:
                                    signals.append(signal)
                                    logger.info(f"Trading signal generated: {signal}")
                
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                continue
        
        # Log results
        logger.info(f"Test completed. Generated {len(signals)} signals:")
        for signal in signals:
            logger.info(f"Signal: {signal}")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_trading_strategy()) 