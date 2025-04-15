from typing import Dict, List, Optional
import asyncio
from contextlib import asynccontextmanager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, FastAPI
from app.core.config import Settings, get_settings
from app.core.websocket_client import CoinbaseWebSocketClient
from app.core.coinbase import CoinbaseClient
from app.strategies.rsi_momentum import RSIMomentumStrategy
from app.models.order import OrderSide, OrderType
import logging
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.trade_log.database import AsyncSessionFactory, init_db
from app.core.trade_log.crud import create_log_entry
from app.core.trade_log.models import EventType, TradeSide, OrderStatus

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.market_data_cache: Dict[str, Dict] = {}  # product_id -> latest data
        self.message_queue: Optional[asyncio.Queue] = None
        self.coinbase_ws_client: Optional[CoinbaseWebSocketClient] = None
        self.coinbase_rest_client: Optional[CoinbaseClient] = None
        self.strategy: Optional[RSIMomentumStrategy] = None
        self.strategy_loop_task: Optional[asyncio.Task] = None
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("New WebSocket connection established")
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket connection closed")
            
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {str(e)}")
                await self.disconnect(connection)
                
    async def handle_coinbase_message(self, message: Dict):
        """Handle incoming message from Coinbase WebSocket"""
        message_type = message.get("type")
        product_id = message.get("product_id")

        if product_id and message_type == "ticker":
            self.market_data_cache[product_id] = message
            await self.broadcast(message)
            if self.message_queue:
                try:
                    asyncio.create_task(self.message_queue.put(message))
                except Exception as e:
                    logger.error(f"Error putting message onto strategy queue: {e}")
        elif message_type == "user_order":
             logger.info(f"Received user order update: {message}")
        
    async def _strategy_loop(self):
        """Consumes messages from the queue, triggers strategy/orders, and logs fills."""
        logger.info("Starting strategy loop...")
        while True:
            message = None # Initialize message to None
            try:
                message = await self.message_queue.get()
                logger.debug(f"Strategy loop received: {message}")

                if message is None:
                    logger.info("Received stop signal in strategy loop.")
                    break
                    
                # --- Log Order Fills --- 
                if isinstance(message, dict) and message.get('type') == 'user_order_update' and message.get('status') == 'FILLED':
                    logger.info(f"Processing FILL message for order {message.get('order_id')}")
                    try:
                        # Use the globally available session factory
                        async with AsyncSessionFactory() as db: 
                            side_str = message.get('side', '').upper()
                            event_type = EventType.ENTRY_FILL if side_str == 'BUY' else EventType.EXIT_FILL if side_str == 'SELL' else EventType.ORDER_UPDATE
                            
                            try:
                                side_enum = TradeSide(side_str) if side_str else None
                            except ValueError:
                                side_enum = None 
                                logger.warning(f"Invalid side '{message.get('side')}' received in fill message.")
                                
                            await create_log_entry(
                                db=db,
                                event_type=event_type,
                                symbol=message.get('product_id'),
                                status=OrderStatus.FILLED, 
                                order_id=message.get('order_id'), 
                                client_order_id=message.get('client_order_id'),
                                side=side_enum,
                                quantity=float(message.get('cumulative_quantity', 0)),
                                price=float(message.get('average_filled_price', 0)), 
                                fees=float(message.get('total_fees', 0)), 
                                # strategy_name= ? # Still needs association logic
                                event_timestamp=pd.to_datetime(message.get('time')), 
                                notes=f"Order filled via WebSocket update."
                            )
                            logger.info(f"Logged FILL event for order {message.get('order_id')}")
                    except Exception as log_err:
                        logger.error(f"Error logging fill event: {log_err}", exc_info=True)
                # --- End Log Order Fills --- 
                
                # --- Existing Strategy Processing --- 
                elif isinstance(message, dict) and message.get('type') == 'ticker': # Process ticker for strategy
                    if self.strategy and self.coinbase_rest_client:
                        # This part might need adjustment if strategy expects different input
                        # signal = self.strategy.process_market_data(message) 
                        # Simplified for example - assumes strategy runs elsewhere or on ticker receipt
                        logger.debug("Passing ticker data to strategy (if implemented)")
                        pass # Placeholder - strategy logic might run elsewhere
                else:
                    logger.debug(f"Skipping message processing in strategy loop for type: {message.get('type')}")
                # --- End Existing Strategy Processing --- 
                    
                # Mark task as done *after* processing
                if message is not None:
                    self.message_queue.task_done()
                
            except asyncio.CancelledError:
                 logger.info("Strategy loop cancelled.")
                 break # Exit the loop cleanly on cancellation
            except Exception as e:
                # Log any other exceptions that occur during message processing
                logger.error(f"Error processing message in strategy loop: {e}", exc_info=True)
                logger.error(f"Failed message content (if available): {message}")
                # Mark task as done even if processing failed to avoid blocking queue
                if message is not None:
                   try:
                       self.message_queue.task_done()
                   except ValueError: # task_done() might raise if called too many times
                       logger.warning("task_done() called on already completed task in error handler.")
                await asyncio.sleep(1) # Prevent rapid error loops

manager = ConnectionManager()

@router.websocket("/ws/{product_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    product_id: str,
    settings: Settings = Depends(get_settings)
):
    """
    WebSocket endpoint for real-time market data
    
    Args:
        websocket (WebSocket): Client WebSocket connection
        product_id (str): Product ID to subscribe to (e.g., "BTC-USD")
        settings (Settings): Application settings
    """
    if not manager.coinbase_ws_client or not manager.coinbase_rest_client:
        logger.error("Coinbase clients not initialized. Check lifespan setup.")
        await websocket.accept()
        await websocket.close(code=1011, reason="Server setup error")
        return
        
    try:
        await manager.connect(websocket)
        
        if manager.coinbase_ws_client:
            manager.coinbase_ws_client.subscribe(product_ids=[product_id], channels=["ticker"])
            logger.info(f"Subscribed to {product_id} ticker updates")
        
        if product_id in manager.market_data_cache:
            await websocket.send_json(manager.market_data_cache[product_id])
        
        while True:
            try:
                data = await websocket.receive_json()
                await manager.broadcast(data)
            except Exception as e:
                logger.error(f"Error in WebSocket communication: {str(e)}")
                break
                
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from /ws/{product_id}")
    except Exception as e:
        logger.error(f"Error in /ws/{product_id} endpoint: {e}", exc_info=True)
    finally:
        manager.disconnect(websocket)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application"""
    logger.info("Application startup...")
    global manager
    try:
        # --- Initialize Database --- 
        logger.info("Initializing trade log database...")
        await init_db()
        logger.info("Database initialized.")
        # --- End DB Init --- 
        
        settings = get_settings()
        manager.message_queue = asyncio.Queue()

        logger.info("Initializing Coinbase REST Client...")
        manager.coinbase_rest_client = CoinbaseClient(settings)
        logger.info("Coinbase REST Client initialized.")

        strategy_product_id = "BTC-USD"
        strategy_config = {
             "rsi_period": 14,
             "oversold_threshold": 30,
             "overbought_threshold": 70,
             "trade_size": 0.001
        }
        manager.strategy = RSIMomentumStrategy(product_id=strategy_product_id, config=strategy_config)
        logger.info("Trading Strategy initialized.")

        # Restore WebSocket Client initialization and connection
        ws_product_ids = ["BTC-USD", "ETH-USD"]
        ws_channels = ["ticker", "heartbeats", "user"]
        logger.info("Initializing Coinbase WebSocket Client...")
        manager.coinbase_ws_client = CoinbaseWebSocketClient(
            api_key=settings.COINBASE_JWT_KEY_NAME,
            api_secret=settings.COINBASE_JWT_PRIVATE_KEY,
            product_ids=ws_product_ids,
            channels=ws_channels,
            message_queue=manager.message_queue,
            retry=True,
            verbose=settings.DEBUG
        )
        
        logger.info("Attempting to connect Coinbase WebSocket Client...")
        try:
            manager.coinbase_ws_client.connect() # Starts in background thread
            logger.info("Coinbase WebSocket Client connect() method called.")
        except Exception as ws_connect_err:
            logger.error(f"Error calling CoinbaseWebSocketClient.connect(): {ws_connect_err}", exc_info=True)
            raise # Re-raise to prevent startup if connect method itself fails
        
        # Keep the delay for now, might still be useful
        logger.info("Pausing briefly after initiating WebSocket connection...")
        await asyncio.sleep(5) 
        logger.info("Pause complete. Starting strategy loop and yielding...")
        
        # Restore the strategy loop start
        manager.strategy_loop_task = asyncio.create_task(manager._strategy_loop())
        logger.info("Strategy processing loop started.")
        
        # logger.warning("WebSocket Client and Strategy Loop are temporarily disabled for debugging.")
        yield # Yield control to Uvicorn
        
    except Exception as e:
        logger.error(f"Error during application lifespan startup: {str(e)}", exc_info=True)
        # Ensure cleanup happens even if startup fails partially
        # raise # Optional: re-raise to halt FastAPI startup completely on error
    finally:
        logger.info("Application shutdown sequence initiated...")
        # Restore Finally Block logic
        logger.info("Application shutdown...")
        if manager.strategy_loop_task:
            logger.info("Stopping strategy loop...")
            try:
                await manager.message_queue.put(None) 
                manager.strategy_loop_task.cancel()
                await manager.strategy_loop_task
            except asyncio.CancelledError:
                logger.info("Strategy loop task cancelled successfully.")
            except Exception as e:
                logger.error(f"Error during strategy loop shutdown: {e}")

        if manager.coinbase_ws_client:
            logger.info("Closing WebSocket client...")
            manager.coinbase_ws_client.close()
        
        logger.info("Application shutdown complete.")

@router.get("/websocket-status")
async def websocket_status():
    """
    Get the status of the WebSocket connection and active subscriptions
    """
    if not manager.coinbase_ws_client:
        return {
            "status": "disconnected",
            "active_connections": len(manager.active_connections),
            "cached_products": list(manager.market_data_cache.keys()),
            "subscribed_channels": []
        }
        
    return {
        "status": "connected" if manager.coinbase_ws_client._is_running else "disconnected",
        "active_connections": len(manager.active_connections),
        "cached_products": list(manager.market_data_cache.keys()),
        "subscribed_channels": manager.coinbase_ws_client.channels,
        "subscribed_products": manager.coinbase_ws_client.product_ids if manager.coinbase_ws_client._is_running else []
    }

@router.post("/subscribe/{product_id}")
async def subscribe_to_product(product_id: str, settings: Settings = Depends(get_settings)):
    """
    Subscribe to a product's ticker channel
    """
    if not manager.coinbase_ws_client:
        return {"status": "error", "message": "WebSocket client not initialized"}
        
    manager.coinbase_ws_client.subscribe(product_ids=[product_id], channels=["ticker"])
    return {"status": "subscribed", "product_id": product_id}

@router.post("/unsubscribe/{product_id}")
async def unsubscribe_from_product(product_id: str, settings: Settings = Depends(get_settings)):
    """
    Unsubscribe from a product's ticker channel
    """
    if not manager.coinbase_ws_client:
        return {"status": "not_connected", "message": "WebSocket client not initialized"}
        
    manager.coinbase_ws_client.unsubscribe(product_ids=[product_id], channels=["ticker"])
    return {"status": "unsubscribed", "product_id": product_id} 