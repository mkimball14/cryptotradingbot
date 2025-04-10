import pytest
import json
import base64
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket, WebSocketDisconnect
import websockets
from websockets.exceptions import ConnectionClosed
import asyncio

from app.core.config import Settings
from app.core.websocket_client import CoinbaseWebSocketClient, WebSocketMessage
from app.routers.websocket import ConnectionManager, router, websocket_endpoint

@pytest.fixture
def settings():
    return Settings(
        COINBASE_API_KEY="organizations/3d4c3ac1-5ed0-400a-8f61-c2571d877bf8/apiKeys/cddb37c8-9861-4754-9e25-8ac50e0edb17",
        COINBASE_API_SECRET="MHcCAQEEIGApfaJBdEkooKWqdYGw5Yqb+j2q5F6hKJuTQ+4TiMnYoAoGCCqGSM49AwEHoUQDQgAEl/YoXnvVYmfoy1YsvJ/o2c1pZhUrcSrhrtIlfRGFl2ugToe2+XtMU+Ije7riM+NMNH640GL1/bXEbHDtlAguAg=="
    )

@pytest.fixture
def websocket_client(settings):
    return CoinbaseWebSocketClient(settings)

@pytest.fixture
def connection_manager():
    return ConnectionManager()

@pytest.mark.asyncio
async def test_websocket_client_authentication(websocket_client):
    # Test authentication message generation
    auth_message = await websocket_client._authenticate()
    assert auth_message["type"] == "subscribe"
    assert auth_message["api_key"] == "test_key"
    assert "timestamp" in auth_message
    assert "signature" in auth_message
    assert auth_message["passphrase"] == "test_passphrase"

@pytest.mark.asyncio
async def test_websocket_client_connect(websocket_client):
    mock_ws = AsyncMock()
    mock_ws.recv.return_value = json.dumps({"type": "subscribed"})
    
    with patch("websockets.connect", AsyncMock(return_value=mock_ws)):
        await websocket_client.connect()
        assert websocket_client.is_connected
        assert websocket_client.ws == mock_ws

@pytest.mark.asyncio
async def test_websocket_client_subscribe(websocket_client):
    mock_ws = AsyncMock()
    websocket_client.ws = mock_ws
    websocket_client.is_connected = True
    
    product_ids = ["BTC-USD"]
    channels = ["market_data"]
    
    await websocket_client.subscribe(product_ids, channels)
    
    # Verify subscription message was sent
    mock_ws.send.assert_called_once()
    sent_message = json.loads(mock_ws.send.call_args[0][0])
    assert sent_message["type"] == "subscribe"
    assert sent_message["product_ids"] == product_ids
    assert sent_message["channels"] == channels

@pytest.mark.asyncio
async def test_websocket_client_message_handling(websocket_client):
    # Create a mock message handler
    mock_handler = AsyncMock()
    websocket_client.add_message_handler(mock_handler)
    
    # Test message handling
    test_message = {
        "type": "ticker",
        "channel": "market_data",
        "timestamp": "2024-01-01T00:00:00Z",
        "sequence_num": 1,
        "product_id": "BTC-USD",
        "data": {"price": "50000.00"}
    }
    
    await websocket_client._handle_message(test_message)
    mock_handler.assert_called_once()
    
    # Verify handler was called with parsed message
    called_message = mock_handler.call_args[0][0]
    assert called_message["type"] == "ticker"
    assert called_message["product_id"] == "BTC-USD"

@pytest.mark.asyncio
async def test_connection_manager(connection_manager):
    # Test WebSocket connection management
    mock_ws = AsyncMock()
    await connection_manager.connect(mock_ws)
    assert mock_ws in connection_manager.active_connections
    
    connection_manager.disconnect(mock_ws)
    assert mock_ws not in connection_manager.active_connections

@pytest.mark.asyncio
async def test_connection_manager_broadcast(connection_manager):
    # Add mock connections
    mock_ws1 = AsyncMock()
    mock_ws2 = AsyncMock()
    
    connection_manager.active_connections = [mock_ws1, mock_ws2]
    
    # Test broadcasting
    test_message = {"type": "ticker", "data": {"price": "50000.00"}}
    await connection_manager.broadcast(test_message)
    
    mock_ws1.send_json.assert_called_once_with(test_message)
    mock_ws2.send_json.assert_called_once_with(test_message)

@pytest.mark.asyncio
async def test_connection_manager_handle_message(connection_manager):
    # Test message handling and caching
    test_message = {
        "type": "ticker",
        "product_id": "BTC-USD",
        "data": {"price": "50000.00"}
    }
    
    # Mock broadcast method
    connection_manager.broadcast = AsyncMock()
    
    await connection_manager.handle_coinbase_message(test_message)
    
    # Verify message was cached
    assert "BTC-USD" in connection_manager.market_data_cache
    assert connection_manager.market_data_cache["BTC-USD"] == test_message
    
    # Verify message was broadcast
    connection_manager.broadcast.assert_called_once_with(test_message)

@pytest.mark.asyncio
async def test_websocket_endpoint_lifecycle():
    # Create mock objects
    mock_ws = AsyncMock()
    mock_settings = Settings(
        COINBASE_API_KEY="test_key",
        COINBASE_API_SECRET=base64.b64encode(b"test_secret").decode(),
        COINBASE_API_PASSPHRASE="test_passphrase",
        DEBUG=False
    )
    
    # Test normal connection lifecycle
    with patch("app.routers.websocket.manager") as mock_manager:
        mock_manager.initialize_coinbase_client = AsyncMock()
        mock_manager.connect = AsyncMock()
        mock_manager.coinbase_client = AsyncMock()
        
        # Simulate WebSocket disconnect after some time
        mock_ws.receive_text = AsyncMock(side_effect=WebSocketDisconnect())
        
        await websocket_endpoint(mock_ws, "BTC-USD", mock_settings)
        
        # Verify client initialization
        mock_manager.initialize_coinbase_client.assert_called_once()
        mock_manager.connect.assert_called_once_with(mock_ws)
        
        # Verify subscription
        mock_manager.coinbase_client.subscribe.assert_called_once_with(
            product_ids=["BTC-USD"],
            channels=["market_data", "ticker"]
        )

@pytest.mark.asyncio
async def test_websocket_connection(settings):
    """Test WebSocket connection and basic functionality"""
    client = CoinbaseWebSocketClient(settings)
    
    try:
        # Test connection
        await client.connect()
        assert client.is_connected
        
        # Test subscription
        await client.subscribe(["BTC-USD"], ["ticker"])
        assert "ticker" in client.subscribed_channels
        assert "BTC-USD" in client.subscribed_channels
        
        # Wait for some messages
        await asyncio.sleep(5)
        
        # Test unsubscribe
        await client.unsubscribe_from_products(["BTC-USD"])
        assert "BTC-USD" not in client.subscribed_channels
        
    finally:
        await client.close()
        assert not client.is_connected 