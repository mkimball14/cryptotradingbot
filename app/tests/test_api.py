import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock

from app.main import app
from app.core.config import Settings

# Use a patched version of the settings for testing
@pytest.fixture(autouse=True)
def mock_settings():
    with patch("app.core.deps.get_settings") as mock:
        mock_settings = MagicMock(spec=Settings)
        mock_settings.COINBASE_API_KEY = "test_key"
        mock_settings.COINBASE_API_SECRET = "test_secret"
        mock_settings.COINBASE_API_PASSPHRASE = "test_passphrase"
        mock_settings.DEBUG = False
        mock.return_value = mock_settings
        yield mock_settings

client = TestClient(app)

# Mock data for tests
MOCK_ACCOUNTS = [
    {
        "id": "test-account-1",
        "currency": "BTC",
        "balance": 1.5,
        "available": 1.0,
        "hold": 0.5,
        "profile_id": "test-profile",
        "trading_enabled": True
    }
]

MOCK_POSITIONS = [
    {
        "product_id": "BTC-USD",
        "position_size": 0.5,
        "entry_price": 48000.00,
        "mark_price": 49000.00,
        "unrealized_pl": 500.00,
        "realized_pl": 0.00,
        "initial_margin": 1000.00,
        "maintenance_margin": 500.00
    }
]

MOCK_PRODUCTS = [
    {
        "id": "BTC-USD",
        "display_name": "BTC/USD",
        "base_currency": "BTC",
        "quote_currency": "USD",
        "status": "online",
        "trading_disabled": False,
        "price_increment": 0.01,
        "quote_increment": 0.01,
        "min_market_funds": 5.0,
        "min_size": 0.0001
    }
]

MOCK_ORDER = {
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


@pytest.fixture
def mock_client():
    """Mock the Coinbase client for testing"""
    with patch("app.core.deps.get_coinbase_client") as mock:
        client_instance = AsyncMock()
        
        # Mock client methods
        client_instance.get_accounts.return_value = MOCK_ACCOUNTS
        client_instance.get_positions.return_value = MOCK_POSITIONS
        client_instance.get_products.return_value = MOCK_PRODUCTS
        client_instance.get_product.return_value = MOCK_PRODUCTS[0]
        client_instance.create_order.return_value = MOCK_ORDER
        client_instance.get_orders.return_value = [MOCK_ORDER]
        client_instance.get_order.return_value = MOCK_ORDER
        
        mock.return_value = client_instance
        yield client_instance


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_account_balance(mock_client):
    """Test getting account balances"""
    response = client.get("/account/balance")
    assert response.status_code == 200
    data = response.json()
    assert "accounts" in data
    assert len(data["accounts"]) == 1
    assert data["accounts"][0]["currency"] == "BTC"


def test_get_positions(mock_client):
    """Test getting positions"""
    response = client.get("/account/positions")
    assert response.status_code == 200
    data = response.json()
    assert "positions" in data
    assert len(data["positions"]) == 1
    assert data["positions"][0]["product_id"] == "BTC-USD"


def test_get_products(mock_client):
    """Test getting products"""
    response = client.get("/market/products")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) == 1
    assert data["products"][0]["id"] == "BTC-USD"


def test_get_product(mock_client):
    """Test getting a specific product"""
    response = client.get("/market/products/BTC-USD")
    assert response.status_code == 200
    data = response.json()
    assert "product" in data
    assert data["product"]["id"] == "BTC-USD"


def test_create_order(mock_client):
    """Test creating an order"""
    order_data = {
        "product_id": "BTC-USD",
        "side": "BUY",
        "order_type": "LIMIT",
        "size": 0.1,
        "price": 50000.0,
        "time_in_force": "GTC"
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert "order" in data
    assert data["order"]["order_id"] == "test-order-1"
    
    # Verify client method was called with correct parameters
    mock_client.create_order.assert_called_once()
    call_args = mock_client.create_order.call_args[1]
    assert call_args["product_id"] == "BTC-USD"
    assert call_args["side"] == "BUY"
    assert call_args["order_type"] == "LIMIT"
    assert call_args["size"] == 0.1
    assert call_args["price"] == 50000.0


def test_get_orders(mock_client):
    """Test getting orders"""
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert "orders" in data
    assert len(data["orders"]) == 1
    assert data["orders"][0]["order_id"] == "test-order-1"


def test_get_order(mock_client):
    """Test getting a specific order"""
    response = client.get("/orders/test-order-1")
    assert response.status_code == 200
    data = response.json()
    assert "order" in data
    assert data["order"]["order_id"] == "test-order-1"


def test_error_handling(mock_client):
    """Test error handling"""
    # Mock client to raise an exception
    mock_client.get_accounts.side_effect = Exception("Test error")
    
    response = client.get("/account/balance")
    assert response.status_code == 500
    data = response.json()
    assert "error" in data 