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
        """Consumes messages from the queue and triggers strategy/orders."""
        logger.info("Starting strategy loop...")
        while True:
            try:
                message = await self.message_queue.get()
                logger.debug(f"Strategy loop received: {message}")

                if message is None:
                    logger.info("Received stop signal in strategy loop.")
                    break

                if self.strategy and self.coinbase_rest_client:
                    signal = self.strategy.process_market_data(message)
                    
                    if signal and isinstance(signal, dict):
                        action = signal.get('action')
                        order_type_str = signal.get('type', 'MARKET').upper()
                        size = signal.get('size')
                        price = signal.get('price')
                        product_id = signal.get('product_id', self.strategy.product_id)
                        
                        logger.info(f"Strategy generated signal: {signal}")

                        if action == 'BUY':
                            side = OrderSide.BUY
                        elif action == 'SELL':
                            side = OrderSide.SELL
                        else:
                            logger.warning(f"Invalid action '{action}' in signal, ignoring.")
                            continue

                        try:
                            order_type = OrderType(order_type_str)
                        except ValueError:
                            logger.warning(f"Invalid order type '{order_type_str}' in signal, defaulting to MARKET.")
                            order_type = OrderType.MARKET

                        if not size or not product_id:
                            logger.error(f"Signal missing required fields (size, product_id): {signal}")
                            continue

                        try:
                            # --- Determine Correct Size Parameter for SDK --- 
                            order_params = {
                                "client_order_id": effective_client_order_id,
                                "product_id": product_id,
                            }
                            size_value = float(size)
                            price_value = float(price) if price is not None else None
                            stop_price_value = None # TODO: Add stop_price if strategy provides it
 
                            # Map generic signal to specific SDK method and parameters
                            sdk_method = None
                            if order_type == OrderType.MARKET:
                                if side == OrderSide.BUY:
                                    order_params["quote_size"] = str(size_value) # Market BUY uses quote size
                                    sdk_method = self.coinbase_rest_client.client.market_order_buy
                                elif side == OrderSide.SELL:
                                    order_params["base_size"] = str(size_value) # Market SELL uses base size
                                    sdk_method = self.coinbase_rest_client.client.market_order_sell
                            elif order_type == OrderType.LIMIT:
                                if price_value is None: raise ValueError("Limit price required for LIMIT order")
                                order_params["base_size"] = str(size_value) # Limit uses base size
                                order_params["limit_price"] = str(price_value)
                                # TODO: Handle TIF (GTC/GTD/etc.) - requires different methods or params
                                if side == OrderSide.BUY:
                                    sdk_method = self.coinbase_rest_client.client.limit_order_gtc_buy
                                elif side == OrderSide.SELL:
                                     sdk_method = self.coinbase_rest_client.client.limit_order_gtc_sell
                            elif order_type == OrderType.STOP_LIMIT:
                                if price_value is None or stop_price_value is None: raise ValueError("Limit and Stop price required for STOP_LIMIT order")
                                order_params["base_size"] = str(size_value) # StopLimit uses base size
                                order_params["limit_price"] = str(price_value)
                                order_params["stop_price"] = str(stop_price_value)
                                # TODO: Handle TIF (GTC/GTD/etc.)
                                # TODO: Handle stop direction if needed
                                if side == OrderSide.BUY:
                                    sdk_method = self.coinbase_rest_client.client.stop_limit_order_gtc_buy
                                elif side == OrderSide.SELL:
                                     sdk_method = self.coinbase_rest_client.client.stop_limit_order_gtc_sell

                            # --- Execute Order --- 
                            if sdk_method:
                                logger.info(f"Executing order via SDK: {sdk_method.__name__} with params: {order_params}")
                                order_result = sdk_method(**order_params)
                                logger.info(f"Order placement response: {order_result}") # Log raw response object
                            else:
                                logger.error(f"Could not determine SDK method for signal: {signal}")

                        except Exception as e:
                            logger.error(f"Failed to execute order from signal {signal}: {e}", exc_info=True)
                
                self.message_queue.task_done()
                
            except asyncio.CancelledError:
                 logger.info("Strategy loop cancelled.")
                 break
            except Exception as e:
                logger.error(f"Error in strategy loop: {e}", exc_info=True)
                await asyncio.sleep(5)

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
        settings = get_settings()
        manager.message_queue = asyncio.Queue()

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

        ws_product_ids = ["BTC-USD", "ETH-USD"]
        ws_channels = ["ticker", "heartbeats", "user"]
        manager.coinbase_ws_client = CoinbaseWebSocketClient(
            api_key=settings.COINBASE_JWT_KEY_NAME,
            api_secret=settings.COINBASE_JWT_PRIVATE_KEY,
            product_ids=ws_product_ids,
            channels=ws_channels,
            message_queue=manager.message_queue,
            retry=True,
            verbose=settings.DEBUG
        )
        manager.coinbase_ws_client.connect()
        logger.info("Coinbase WebSocket Client connection initiated.")

        manager.strategy_loop_task = asyncio.create_task(manager._strategy_loop())
        logger.info("Strategy processing loop started.")
        
        yield
        
    except Exception as e:
        logger.error(f"Error in WebSocket lifespan: {str(e)}")
        raise
    finally:
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