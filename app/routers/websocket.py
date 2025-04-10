from typing import Dict, List, Optional
from contextlib import asynccontextmanager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.config import Settings, get_settings
from app.core.websocket_client import CoinbaseWebSocketClient
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.market_data_cache: Dict[str, Dict] = {}  # product_id -> latest data
        self.coinbase_client: Optional[CoinbaseWebSocketClient] = None
        
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
        product_id = message.get("product_id")
        if product_id and message.get("type") == "ticker":
            self.market_data_cache[product_id] = message
            await self.broadcast(message)
        
    async def initialize_coinbase_client(self, settings: Settings):
        """Initialize Coinbase WebSocket client if not already initialized"""
        if not self.coinbase_client:
            self.coinbase_client = CoinbaseWebSocketClient(
                settings=settings,
                on_message=self.handle_coinbase_message,
                retry=True
            )
            # Start the connection
            await self.coinbase_client.connect()
            logger.info("WebSocket manager initialized successfully")
            
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
    try:
        await manager.initialize_coinbase_client(settings)
        await manager.connect(websocket)
        
        # Subscribe to product updates
        if manager.coinbase_client:
            await manager.coinbase_client.subscribe([product_id], ["ticker"])
            logger.info(f"Subscribed to {product_id} ticker updates")
        
        # Send cached data if available
        if product_id in manager.market_data_cache:
            await websocket.send_json(manager.market_data_cache[product_id])
        
        # Keep connection alive and handle client messages if needed
        while True:
            try:
                data = await websocket.receive_json()
                await manager.broadcast(data)
            except Exception as e:
                logger.error(f"Error in WebSocket communication: {str(e)}")
                break
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
    finally:
        if manager.coinbase_client:
            await manager.coinbase_client.unsubscribe_from_products([product_id])
        manager.disconnect(websocket)

@asynccontextmanager
async def lifespan(app):
    """Lifespan context manager for FastAPI application"""
    try:
        # Startup: Initialize WebSocket client on application startup
        settings = get_settings()
        await manager.initialize_coinbase_client(settings)
        
        # Start with some default product subscriptions if needed
        default_products = ["BTC-USD", "ETH-USD"]
        if manager.coinbase_client:
            await manager.coinbase_client.subscribe_to_products(default_products)
        
        yield
        
    except Exception as e:
        logger.error(f"Error in WebSocket lifespan: {str(e)}")
        raise
    finally:
        # Shutdown: Close WebSocket client
        if manager.coinbase_client:
            await manager.coinbase_client.close()
            manager.coinbase_client = None
        logger.info("WebSocket manager cleaned up")

@router.get("/websocket-status")
async def websocket_status():
    """
    Get the status of the WebSocket connection and active subscriptions
    """
    if not manager.coinbase_client:
        return {
            "status": "disconnected",
            "active_connections": len(manager.active_connections),
            "cached_products": list(manager.market_data_cache.keys()),
            "subscribed_channels": []
        }
        
    return {
        "status": "connected" if manager.coinbase_client.is_connected else "disconnected",
        "active_connections": len(manager.active_connections),
        "cached_products": list(manager.market_data_cache.keys()),
        "subscribed_channels": manager.coinbase_client.subscribed_channels,
        "subscribed_products": manager.coinbase_client.product_ids if manager.coinbase_client.is_connected else []
    }

@router.post("/subscribe/{product_id}")
async def subscribe_to_product(product_id: str, settings: Settings = Depends(get_settings)):
    """
    Subscribe to a product's ticker channel
    """
    if not manager.coinbase_client:
        await manager.initialize_coinbase_client(settings)
        
    await manager.coinbase_client.subscribe_to_products([product_id])
    return {"status": "subscribed", "product_id": product_id}

@router.post("/unsubscribe/{product_id}")
async def unsubscribe_from_product(product_id: str, settings: Settings = Depends(get_settings)):
    """
    Unsubscribe from a product's ticker channel
    """
    if not manager.coinbase_client:
        return {"status": "not_connected", "message": "WebSocket client not initialized"}
        
    await manager.coinbase_client.unsubscribe_from_products([product_id])
    return {"status": "unsubscribed", "product_id": product_id} 