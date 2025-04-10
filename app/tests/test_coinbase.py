import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, AsyncMock
import base64
import httpx
from app.core.config import Settings
from app.core.coinbase import (
    CoinbaseClient,
    CoinbaseError,
    Order,
    Position,
    OrderSide,
    OrderType,
    OrderStatus
)

@pytest.fixture
def settings():
    return Settings(
        COINBASE_API_KEY="test_key",
        COINBASE_API_SECRET=base64.b64encode(b"test_secret").decode(),
        COINBASE_API_PASSPHRASE="test_passphrase",
        DEBUG=False
    )

@pytest.fixture
def client(settings):
    return CoinbaseClient(settings)

@pytest.mark.asyncio
async def test_get_accounts(client):
    mock_response = {
        "accounts": [
            {
                "uuid": "test-account-1",
                "name": "BTC-USD",
                "currency": "BTC",
                "available_balance": {"value": "1.23", "currency": "BTC"},
                "default": True,
                "active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "deleted_at": None,
                "type": "SPOT"
            }
        ]
    }

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = AsyncMock(
            json=AsyncMock(return_value=mock_response),
            raise_for_status=AsyncMock()
        )

        accounts = await client.get_accounts()
        assert len(accounts) == 1
        assert accounts[0]["uuid"] == "test-account-1"
        assert accounts[0]["currency"] == "BTC"

@pytest.mark.asyncio
async def test_create_order(client):
    mock_order_response = {
        "order": {
            "order_id": "test-order-1",
            "client_order_id": "test-client-1",
            "product_id": "BTC-USD",
            "side": "BUY",
            "order_type": "LIMIT",
            "status": "PENDING",
            "time_in_force": "GTC",
            "created_time": "2024-01-01T00:00:00Z",
            "price": "50000.00",
            "size": "0.1",
            "filled_size": "0.0",
            "average_filled_price": None
        }
    }

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = AsyncMock(
            json=AsyncMock(return_value=mock_order_response),
            raise_for_status=AsyncMock()
        )

        order = await client.create_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            size=0.1,
            price=50000.00
        )
        assert order.order_id == "test-order-1"
        assert order.side == "BUY"
        assert order.order_type == "LIMIT"

@pytest.mark.asyncio
async def test_get_positions(client):
    mock_positions_response = {
        "positions": [
            {
                "product_id": "BTC-USD",
                "position_size": "0.5",
                "entry_price": "48000.00",
                "mark_price": "49000.00",
                "unrealized_pl": "500.00",
                "realized_pl": "0.00",
                "initial_margin": "1000.00",
                "maintenance_margin": "500.00"
            }
        ]
    }

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = AsyncMock(
            json=AsyncMock(return_value=mock_positions_response),
            raise_for_status=AsyncMock()
        )

        positions = await client.get_positions()
        assert len(positions) == 1
        assert positions[0].product_id == "BTC-USD"
        assert positions[0].position_size == 0.5  # Note: converted from string to float

@pytest.mark.asyncio
async def test_api_error_handling(client):
    error_response = {
        "error": "Invalid API Key",
        "code": 401
    }

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        # Create a mock response that will raise an error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json = AsyncMock(return_value=error_response)

        # Create the HTTP error with our mock response
        http_error = httpx.HTTPStatusError(
            "401 Unauthorized",
            request=MagicMock(),
            response=mock_response
        )

        # Make the request raise the error immediately
        mock_request.side_effect = http_error

        with pytest.raises(CoinbaseError) as exc_info:
            await client.get_accounts()
        assert exc_info.value.status_code == 401
        assert exc_info.value.response == error_response

@pytest.mark.asyncio
async def test_get_product_candles(client):
    mock_candles_response = {
        "candles": [
            {
                "start": "2024-01-01T00:00:00Z",
                "low": "47000.00",
                "high": "48000.00",
                "open": "47500.00",
                "close": "47800.00",
                "volume": "100.5"
            }
        ]
    }

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = AsyncMock(
            json=AsyncMock(return_value=mock_candles_response),
            raise_for_status=AsyncMock()
        )

        candles = await client.get_product_candles(
            product_id="BTC-USD",
            start="2024-01-01T00:00:00Z",
            end="2024-01-01T01:00:00Z"
        )
        assert len(candles) == 1
        assert candles[0]["low"] == "47000.00"
        assert candles[0]["high"] == "48000.00" 