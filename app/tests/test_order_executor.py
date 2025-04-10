import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from app.core.order_executor import OrderExecutor, OrderExecutionError
from app.core.coinbase import (
    CoinbaseClient,
    Order,
    OrderSide,
    OrderType,
    OrderStatus,
    CoinbaseError
)

@pytest.fixture
def mock_coinbase_client():
    client = Mock(spec=CoinbaseClient)
    # Set up async mock methods
    client.create_order = AsyncMock()
    client.cancel_order = AsyncMock()
    client.get_order = AsyncMock()
    client.get_orders = AsyncMock()
    return client

@pytest.fixture
def order_executor(mock_coinbase_client):
    return OrderExecutor(mock_coinbase_client)

@pytest.fixture
def sample_order():
    now = datetime.now()
    return Order(
        order_id="test-order-id",
        product_id="BTC-USD",
        side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        size=1.0,
        price=50000.0,
        status=OrderStatus.PENDING,
        time_in_force="GTC",
        created_time=now,
        metadata={}
    )

@pytest.mark.asyncio
async def test_execute_market_order_success(order_executor, mock_coinbase_client, sample_order):
    mock_coinbase_client.create_order.return_value = sample_order
    
    result = await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    assert result.success is True
    assert result.order == sample_order
    assert result.error is None
    assert "execution_latency" in result.metadata
    assert result.metadata["order_type"] == "market"
    
    mock_coinbase_client.create_order.assert_called_once()

@pytest.mark.asyncio
async def test_execute_market_order_validation_error(order_executor):
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_market_order(
            product_id="BTC-USD",
            side="INVALID_SIDE",
            size=1.0
        )
    assert "Invalid order side" in str(exc_info.value)
        
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=-1.0
        )
    assert "Invalid order size" in str(exc_info.value)

@pytest.mark.asyncio
async def test_execute_limit_order_success(order_executor, mock_coinbase_client, sample_order):
    mock_coinbase_client.create_order.return_value = sample_order
    
    result = await order_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        price=50000.0
    )
    
    assert result.success is True
    assert result.order == sample_order
    assert result.error is None
    assert "execution_latency" in result.metadata
    assert result.metadata["order_type"] == "limit"
    
    mock_coinbase_client.create_order.assert_called_once()

@pytest.mark.asyncio
async def test_execute_limit_order_validation_error(order_executor):
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_limit_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=1.0,
            price=-50000.0
        )
    assert "Invalid price" in str(exc_info.value)

@pytest.mark.asyncio
async def test_cancel_order_success(order_executor, mock_coinbase_client):
    mock_coinbase_client.cancel_order.return_value = {"success": True}
    
    result = await order_executor.cancel_order("test-order-id")
    
    assert result.success is True
    assert result.error is None
    assert "execution_latency" in result.metadata
    assert result.metadata["action"] == "cancel"
    
    mock_coinbase_client.cancel_order.assert_called_once_with("test-order-id")

@pytest.mark.asyncio
async def test_cancel_order_failure(order_executor, mock_coinbase_client):
    mock_coinbase_client.cancel_order.side_effect = CoinbaseError("Order not found")
    
    result = await order_executor.cancel_order("test-order-id")
    
    assert result.success is False
    assert "Coinbase API error" in result.error
    assert result.metadata["error_type"] == "api_error"

@pytest.mark.asyncio
async def test_get_order_status(order_executor, mock_coinbase_client, sample_order):
    mock_coinbase_client.get_order.return_value = sample_order
    
    order = await order_executor.get_order_status("test-order-id")
    
    assert order == sample_order
    mock_coinbase_client.get_order.assert_called_once_with("test-order-id")

@pytest.mark.asyncio
async def test_get_open_orders(order_executor, mock_coinbase_client, sample_order):
    mock_coinbase_client.get_orders.return_value = [sample_order]
    
    orders = await order_executor.get_open_orders(product_id="BTC-USD")
    
    assert len(orders) == 1
    assert orders[0] == sample_order
    mock_coinbase_client.get_orders.assert_called_once_with(
        product_id="BTC-USD",
        status=[OrderStatus.PENDING, OrderStatus.OPEN]
    ) 