from typing import Dict, List, Optional, Union
import asyncio
from contextlib import asynccontextmanager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, FastAPI
from app.core.config import Settings, get_settings
from app.core.websocket_client import CoinbaseWebSocketClient
from app.core.coinbase import CoinbaseClient
from app.core.order_executor import OrderExecutor
from app.core.dry_run_executor import DryRunExecutor
from app.strategies.rsi_momentum import RSIMomentumStrategy
from app.models.order import OrderSide, OrderType
import logging
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.trade_log.database import AsyncSessionFactory, init_db
from app.core.trade_log.crud import create_log_entry
from app.core.trade_log.models import EventType, TradeSide, OrderStatus
from app.core.live_trader import LiveTrader

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
        self.live_trader: Optional[LiveTrader] = None
        self.order_executor: Optional[Union[OrderExecutor, DryRunExecutor]] = None
        
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

        # --- Conditional Executor Initialization --- 
        if settings.DRY_RUN_MODE:
            logger.warning("DRY RUN MODE ENABLED. Orders will be simulated.")
            # Configure DryRunExecutor - potentially use settings for initial balance etc.
            manager.order_executor = DryRunExecutor(
                initial_balance={"USD": 50000.0, "BTC": 0.0}, # Example initial balance
                simulated_latency=0.05, # Example latency
                fill_probability=0.98, # Example fill probability
                slippage_std=0.0005 # Example slippage
            )
        else:
            logger.info("LIVE TRADING MODE ENABLED.")
            # Ensure the real OrderExecutor gets the REST client
            manager.order_executor = OrderExecutor(manager.coinbase_rest_client) 
        logger.info(f"Order Executor initialized ({type(manager.order_executor).__name__}).")
        # --- End Conditional Initialization --- 

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
        
        # Create connection event for synchronization
        connection_event = asyncio.Event()
        manager.coinbase_ws_client = CoinbaseWebSocketClient(
            api_key=settings.COINBASE_JWT_KEY_NAME,
            api_secret=settings.COINBASE_JWT_PRIVATE_KEY,
            product_ids=ws_product_ids, # Initial subscribe list (can be modified later)
            channels=ws_channels,       # Initial subscribe list
            message_queue=manager.message_queue, # Pass the shared queue
            loop=asyncio.get_running_loop(),
            connection_established_event=connection_event,
            retry=True,
            verbose=settings.DEBUG
        )

        # Initialize LiveTrader (AFTER strategy and executor are ready)
        logger.info("Initializing LiveTrader...")
        manager.live_trader = LiveTrader(
            settings=settings,
            strategy=manager.strategy,
            db_session_factory=AsyncSessionFactory, # Pass the factory
            product_id=strategy_product_id, # Use the configured product ID
            # Pass the conditionally initialized executor
            order_executor=manager.order_executor,
            # Pass the REST client
            rest_client=manager.coinbase_rest_client,
            # Pass the WS client and message queue (LiveTrader can handle messages)
            ws_client=manager.coinbase_ws_client,
            message_queue=manager.message_queue
        )
        logger.info("LiveTrader initialized.")

        logger.info("Attempting to connect Coinbase WebSocket Client...")
        try:
            manager.coinbase_ws_client.connect() # Starts in background thread
            logger.info("Coinbase WebSocket Client connect() method called.")
            # Wait for connection using the event
            logger.info("Waiting for WebSocket connection...")
            await asyncio.wait_for(connection_event.wait(), timeout=15.0) # Wait up to 15s
            logger.info("WebSocket connection established.")
        except asyncio.TimeoutError:
            logger.error("WebSocket connection timed out during startup.")
            # Decide if app should fail or continue without WebSocket
            raise ConnectionError("WebSocket timed out") # Example: Halt startup
        except Exception as ws_connect_err:
            logger.error(f"Error calling CoinbaseWebSocketClient.connect(): {ws_connect_err}", exc_info=True)
            raise # Re-raise to prevent startup if connect method itself fails
        
        # Assign LiveTrader's handler to the WS client AFTER connection is confirmed
        if manager.live_trader and manager.coinbase_ws_client:
            logger.info("Assigning LiveTrader message handler to WebSocket client.")
            # Ensure the LiveTrader's handler is used for processing messages
            # This might override the default manager.handle_coinbase_message used for broadcasting
            manager.coinbase_ws_client.on_message = manager.live_trader._handle_websocket_message
            # Assign other handlers if LiveTrader implements them
            if hasattr(manager.live_trader, '_handle_websocket_error'):
                manager.coinbase_ws_client.on_error = manager.live_trader._handle_websocket_error
            if hasattr(manager.live_trader, '_handle_websocket_connect'):
                # Note: _on_open is handled internally by the client for connection_event
                # We might not need to re-assign on_connect unless LiveTrader needs specific logic here.
                # manager.coinbase_ws_client.on_connect = manager.live_trader._handle_websocket_connect
                pass
            if hasattr(manager.live_trader, '_handle_websocket_disconnect'):
                manager.coinbase_ws_client.on_disconnect = manager.live_trader._handle_websocket_disconnect
        else:
            logger.error("LiveTrader or WebSocket client not initialized in lifespan. Cannot assign handlers.")
        
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