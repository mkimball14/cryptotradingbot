import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta
import os
import asyncio
import pandas as pd
import numpy as np

from app.core.order_executor import OrderExecutor, OrderExecutionError, BracketOrderResult
from app.core.coinbase import (
    CoinbaseClient,
    Order,
    OrderSide,
    OrderType,
    OrderStatus,
    CoinbaseError
)
from app.core.signal_manager import SignalConfirmation
from app.core.zone import Zone

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

@pytest.fixture
async def live_client():
    """Fixture for testing with live Coinbase API."""
    api_key = os.getenv("COINBASE_API_KEY")
    api_secret = os.getenv("COINBASE_API_SECRET")
    if not api_key or not api_secret:
        pytest.skip("Coinbase API credentials not found in environment")
    
    client = CoinbaseClient(api_key=api_key, api_secret=api_secret)
    executor = OrderExecutor(client)
    yield executor
    await client.close()

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

@pytest.mark.asyncio
async def test_execute_bracket_order_market_entry_success(order_executor, mock_coinbase_client, sample_order):
    """Test successful bracket order execution with market entry."""
    # Mock the order responses
    mock_coinbase_client.create_order.return_value = sample_order
    
    result = await order_executor.execute_bracket_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        stop_loss_price=45000.0,
        take_profit_price=55000.0
    )
    
    assert result.success is True
    assert result.entry_order == sample_order
    assert result.stop_loss_order == sample_order
    assert result.take_profit_order == sample_order
    assert result.error is None
    assert "execution_latency" in result.metadata
    assert result.metadata["entry_type"] == "MARKET"
    assert result.metadata["position_side"] == "BUY"
    
    # Verify order creation calls
    assert mock_coinbase_client.create_order.call_count == 3

@pytest.mark.asyncio
async def test_execute_bracket_order_limit_entry_success(order_executor, mock_coinbase_client, sample_order):
    """Test successful bracket order execution with limit entry."""
    mock_coinbase_client.create_order.return_value = sample_order
    
    result = await order_executor.execute_bracket_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        entry_price=50000.0,
        stop_loss_price=45000.0,
        take_profit_price=55000.0,
        entry_type=OrderType.LIMIT
    )
    
    assert result.success is True
    assert result.entry_order == sample_order
    assert result.stop_loss_order == sample_order
    assert result.take_profit_order == sample_order
    assert result.error is None
    assert result.metadata["entry_type"] == "LIMIT"
    
    assert mock_coinbase_client.create_order.call_count == 3

@pytest.mark.asyncio
async def test_execute_bracket_order_validation_errors(order_executor):
    """Test bracket order validation error cases."""
    # Test invalid side
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_bracket_order(
            product_id="BTC-USD",
            side="INVALID",
            size=1.0,
            stop_loss_price=45000.0,
            take_profit_price=55000.0
        )
    assert "Invalid order side" in str(exc_info.value)
    
    # Test invalid size
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_bracket_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=-1.0,
            stop_loss_price=45000.0,
            take_profit_price=55000.0
        )
    assert "Invalid order size" in str(exc_info.value)
    
    # Test missing entry price for limit order
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_bracket_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=1.0,
            stop_loss_price=45000.0,
            take_profit_price=55000.0,
            entry_type=OrderType.LIMIT
        )
    assert "Entry price required" in str(exc_info.value)
    
    # Test invalid stop loss price (above entry for long)
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_bracket_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=1.0,
            entry_price=50000.0,
            stop_loss_price=51000.0,
            take_profit_price=55000.0,
            entry_type=OrderType.LIMIT
        )
    assert "Stop loss must be below entry" in str(exc_info.value)
    
    # Test invalid take profit price (below entry for long)
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_bracket_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=1.0,
            entry_price=50000.0,
            stop_loss_price=45000.0,
            take_profit_price=49000.0,
            entry_type=OrderType.LIMIT
        )
    assert "Take profit must be above entry" in str(exc_info.value)

@pytest.mark.asyncio
async def test_execute_bracket_order_api_error(order_executor, mock_coinbase_client):
    """Test bracket order handling of API errors."""
    mock_coinbase_client.create_order.side_effect = CoinbaseError("API Error")
    
    result = await order_executor.execute_bracket_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        stop_loss_price=45000.0,
        take_profit_price=55000.0
    )
    
    assert result.success is False
    assert "Coinbase API error" in result.error
    assert result.metadata["error_type"] == "api_error"

@pytest.mark.asyncio
async def test_cancel_bracket_order(order_executor, mock_coinbase_client):
    """Test cancellation of all orders in a bracket order."""
    mock_coinbase_client.cancel_order.return_value = {"success": True}
    
    results = await order_executor.cancel_bracket_order(
        entry_order_id="entry-123",
        stop_loss_order_id="sl-123",
        take_profit_order_id="tp-123"
    )
    
    assert len(results) == 3
    assert all(result.success for result in results)
    assert mock_coinbase_client.cancel_order.call_count == 3
    
    # Test partial failure
    mock_coinbase_client.cancel_order.side_effect = [
        {"success": True},
        CoinbaseError("Not found"),
        {"success": True}
    ]
    
    results = await order_executor.cancel_bracket_order(
        entry_order_id="entry-123",
        stop_loss_order_id="sl-123",
        take_profit_order_id="tp-123"
    )
    
    assert len(results) == 3
    assert results[0].success is True
    assert results[1].success is False
    assert results[2].success is True

@pytest.mark.integration
@pytest.mark.asyncio
async def test_bracket_order_integration_market_entry(live_client):
    """Test bracket order execution with market entry against live API."""
    # Get current market price for BTC-USD
    product = await live_client.client.get_product("BTC-USD")
    current_price = float(product["price"])
    
    # Calculate prices for a small test order
    stop_loss_price = current_price * 0.99  # 1% below current price
    take_profit_price = current_price * 1.01  # 1% above current price
    size = 0.001  # Minimum BTC order size
    
    result = await live_client.execute_bracket_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=size,
        stop_loss_price=stop_loss_price,
        take_profit_price=take_profit_price
    )
    
    assert result.success is True
    assert result.entry_order is not None
    assert result.stop_loss_order is not None
    assert result.take_profit_order is not None
    assert result.error is None
    
    # Clean up orders
    await live_client.cancel_order(result.entry_order.order_id)
    await live_client.cancel_order(result.stop_loss_order.order_id)
    await live_client.cancel_order(result.take_profit_order.order_id)

@pytest.mark.integration
@pytest.mark.asyncio
async def test_bracket_order_integration_limit_entry(live_client):
    """Test bracket order execution with limit entry against live API."""
    # Get current market price for BTC-USD
    product = await live_client.client.get_product("BTC-USD")
    current_price = float(product["price"])
    
    # Calculate prices for a small test order
    entry_price = current_price * 0.99  # Limit buy 1% below market
    stop_loss_price = entry_price * 0.99  # Stop loss 1% below entry
    take_profit_price = entry_price * 1.02  # Take profit 2% above entry
    size = 0.001  # Minimum BTC order size
    
    result = await live_client.execute_bracket_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=size,
        entry_price=entry_price,
        entry_type=OrderType.LIMIT,
        stop_loss_price=stop_loss_price,
        take_profit_price=take_profit_price
    )
    
    assert result.success is True
    assert result.entry_order is not None
    assert result.stop_loss_order is not None
    assert result.take_profit_order is not None
    assert result.error is None
    
    # Clean up orders
    await live_client.cancel_order(result.entry_order.order_id)
    await live_client.cancel_order(result.stop_loss_order.order_id)
    await live_client.cancel_order(result.take_profit_order.order_id)

@pytest.mark.integration
@pytest.mark.asyncio
async def test_bracket_order_monitoring(live_client):
    """Test bracket order monitoring functionality."""
    # Get current market price for BTC-USD
    product = await live_client.client.get_product("BTC-USD")
    current_price = float(product["price"])
    
    # Place a limit entry order far from current price
    entry_price = current_price * 0.95  # 5% below market
    stop_loss_price = entry_price * 0.99
    take_profit_price = entry_price * 1.02
    size = 0.001
    
    result = await live_client.execute_bracket_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=size,
        entry_price=entry_price,
        entry_type=OrderType.LIMIT,
        stop_loss_price=stop_loss_price,
        take_profit_price=take_profit_price
    )
    
    assert result.success is True
    
    # Cancel the entry order and verify monitoring updates status
    await live_client.cancel_order(result.entry_order.order_id)
    await asyncio.sleep(2)  # Wait for status update
    
    # Check that all orders are cancelled
    entry_status = await live_client.get_order_status(result.entry_order.order_id)
    stop_status = await live_client.get_order_status(result.stop_loss_order.order_id)
    take_profit_status = await live_client.get_order_status(result.take_profit_order.order_id)
    
    assert entry_status.status == OrderStatus.CANCELLED
    assert stop_status.status == OrderStatus.CANCELLED
    assert take_profit_status.status == OrderStatus.CANCELLED

@pytest.mark.integration
@pytest.mark.asyncio
async def test_bracket_order_insufficient_funds(live_client):
    """Test bracket order validation for insufficient funds."""
    # Get current market price for BTC-USD
    product = await live_client.client.get_product("BTC-USD")
    current_price = float(product["price"])
    
    # Try to place an order with a very large size
    size = 100.0  # Large BTC order that should exceed available funds
    
    with pytest.raises(OrderExecutionError) as exc_info:
        await live_client.execute_bracket_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=size,
            stop_loss_price=current_price * 0.99,
            take_profit_price=current_price * 1.01
        )
    
    assert "Insufficient" in str(exc_info.value)

@pytest.fixture
def signal_manager():
    """Fixture providing a mock signal manager for testing."""
    manager = Mock()
    manager.confirm_signal = AsyncMock()
    manager.confirm_signal.return_value = SignalConfirmation(
        is_valid=True,
        confidence_score=0.85,
        indicators={
            "rsi_divergence": True,
            "volume_spike": True,
            "price_pattern": "double_bottom"
        },
        timestamp=datetime.now()
    )
    return manager

@pytest.fixture
def failing_signal_manager():
    """Fixture providing a mock signal manager that returns failed confirmations."""
    manager = Mock()
    manager.confirm_signal = AsyncMock()
    manager.confirm_signal.return_value = SignalConfirmation(
        is_valid=False,
        confidence_score=0.3,
        indicators={
            "rsi_divergence": False,
            "volume_spike": False,
            "price_pattern": None
        },
        timestamp=datetime.now()
    )
    return manager

@pytest.fixture
def mock_zone():
    """Fixture providing a mock trading zone."""
    return Zone(
        id="test-zone-1",
        type="demand",
        start_time=datetime.now(),
        end_time=datetime.now(),
        high_price=52000.0,
        low_price=51000.0,
        strength=0.8,
        status="active"
    )

@pytest.fixture
def mock_ohlcv_data():
    """Fixture providing mock OHLCV data for testing."""
    timestamps = pd.date_range(start="2024-01-01", periods=100, freq="1H")
    np.random.seed(42)
    
    base_price = 50000.0
    price_changes = np.random.normal(0, 100, len(timestamps))
    prices = base_price + np.cumsum(price_changes)
    
    return pd.DataFrame({
        "timestamp": timestamps,
        "open": prices,
        "high": prices + np.random.uniform(0, 50, len(timestamps)),
        "low": prices - np.random.uniform(0, 50, len(timestamps)),
        "close": prices + np.random.normal(0, 25, len(timestamps)),
        "volume": np.random.uniform(1, 10, len(timestamps))
    })

@pytest.mark.asyncio
async def test_confirm_trading_signal_success(order_executor, signal_manager, mock_zone, mock_ohlcv_data):
    """Test successful confirmation of a trading signal."""
    order_executor.signal_manager = signal_manager
    
    confirmation = await order_executor.confirm_trading_signal(
        zone=mock_zone,
        ohlcv_data=mock_ohlcv_data
    )
    
    assert confirmation is not None
    assert confirmation.is_valid is True
    assert confirmation.confidence_score >= 0.8
    assert "rsi_divergence" in confirmation.indicators
    assert "volume_spike" in confirmation.indicators
    assert confirmation.timestamp is not None
    
    signal_manager.confirm_signal.assert_called_once_with(
        zone=mock_zone,
        ohlcv_data=mock_ohlcv_data
    )

@pytest.mark.asyncio
async def test_confirm_trading_signal_no_manager(order_executor, mock_zone, mock_ohlcv_data):
    """Test behavior when no signal manager is available."""
    order_executor.signal_manager = None
    
    confirmation = await order_executor.confirm_trading_signal(
        zone=mock_zone,
        ohlcv_data=mock_ohlcv_data
    )
    
    assert confirmation is None

@pytest.mark.asyncio
async def test_execute_zone_order_success(
    order_executor, signal_manager, mock_zone, mock_ohlcv_data, sample_order
):
    """Test successful execution of a zone order with signal confirmation."""
    order_executor.signal_manager = signal_manager
    order_executor.client.create_order.return_value = sample_order
    
    result = await order_executor.execute_zone_order(
        zone=mock_zone,
        size=1.0,
        ohlcv_data=mock_ohlcv_data,
        require_confirmation=True
    )
    
    assert result.success is True
    assert result.order == sample_order
    assert result.error is None
    assert "signal_confirmation" in result.metadata
    assert result.metadata["signal_confirmation"]["is_valid"] is True
    assert result.metadata["signal_confirmation"]["confidence_score"] >= 0.8
    assert "zone_id" in result.metadata
    assert result.metadata["zone_id"] == mock_zone.id

@pytest.mark.asyncio
async def test_execute_zone_order_skip_confirmation(
    order_executor, mock_zone, mock_ohlcv_data, sample_order
):
    """Test execution of a zone order when skipping confirmation."""
    order_executor.client.create_order.return_value = sample_order
    
    result = await order_executor.execute_zone_order(
        zone=mock_zone,
        size=1.0,
        ohlcv_data=mock_ohlcv_data,
        require_confirmation=False
    )
    
    assert result.success is True
    assert result.order == sample_order
    assert result.error is None
    assert "signal_confirmation" not in result.metadata
    assert "zone_id" in result.metadata
    assert result.metadata["zone_id"] == mock_zone.id

@pytest.mark.asyncio
async def test_execute_zone_order_signal_validation_failed(
    order_executor, failing_signal_manager, mock_zone, mock_ohlcv_data
):
    """Test handling of failed signal validation during order execution."""
    order_executor.signal_manager = failing_signal_manager
    
    with pytest.raises(OrderExecutionError) as exc_info:
        await order_executor.execute_zone_order(
            zone=mock_zone,
            size=1.0,
            ohlcv_data=mock_ohlcv_data,
            require_confirmation=True
        )
    
    assert "Signal validation failed" in str(exc_info.value)
    assert order_executor.client.create_order.call_count == 0

@pytest.mark.asyncio
async def test_signal_validation_with_confirmation(
    order_executor: OrderExecutor,
    mock_signal_manager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test signal validation with successful confirmation."""
    # Setup mock confirmation
    mock_confirmation = SignalConfirmation(
        is_confirmed=True,
        confidence_score=0.85,
        confirmation_factors={
            "rsi_divergence": 0.8,
            "volume_profile": 0.9,
            "market_context": 0.85
        }
    )
    mock_signal_manager.confirm_zone_signal.return_value = mock_confirmation
    
    # Test validation
    result = await order_executor.validate_signal(
        product_id="BTC-USD",
        zone=sample_supply_zone,
        side=OrderSide.SELL,
        ohlcv_data=sample_ohlcv_data
    )
    
    assert result == mock_confirmation
    assert result.is_confirmed
    assert result.confidence_score >= order_executor.min_signal_confidence
    
@pytest.mark.asyncio
async def test_signal_validation_below_threshold(
    order_executor: OrderExecutor,
    mock_signal_manager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test signal validation with confirmation below threshold."""
    # Setup mock confirmation with low confidence
    mock_confirmation = SignalConfirmation(
        is_confirmed=False,
        confidence_score=0.5,
        confirmation_factors={
            "rsi_divergence": 0.4,
            "volume_profile": 0.5,
            "market_context": 0.6
        }
    )
    mock_signal_manager.confirm_zone_signal.return_value = mock_confirmation
    
    # Test validation
    result = await order_executor.validate_signal(
        product_id="BTC-USD",
        zone=sample_supply_zone,
        side=OrderSide.SELL,
        ohlcv_data=sample_ohlcv_data
    )
    
    assert result == mock_confirmation
    assert not result.is_confirmed
    assert result.confidence_score < order_executor.min_signal_confidence

@pytest.mark.asyncio
async def test_signal_validation_no_signal_manager(
    order_executor: OrderExecutor,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test signal validation without signal manager configured."""
    # Remove signal manager
    order_executor.signal_manager = None
    
    # Test validation
    with pytest.raises(OrderExecutionError, match="Signal manager not configured"):
        await order_executor.validate_signal(
            product_id="BTC-USD",
            zone=sample_supply_zone,
            side=OrderSide.SELL,
            ohlcv_data=sample_ohlcv_data
        )

@pytest.mark.asyncio
async def test_signal_validation_with_custom_threshold(
    order_executor: OrderExecutor,
    mock_signal_manager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test signal validation with custom confidence threshold."""
    # Setup mock confirmation
    mock_confirmation = SignalConfirmation(
        is_confirmed=True,
        confidence_score=0.65,
        confirmation_factors={
            "rsi_divergence": 0.6,
            "volume_profile": 0.7,
            "market_context": 0.65
        }
    )
    mock_signal_manager.confirm_zone_signal.return_value = mock_confirmation
    
    # Test validation with custom threshold
    result = await order_executor.validate_signal(
        product_id="BTC-USD",
        zone=sample_supply_zone,
        side=OrderSide.SELL,
        ohlcv_data=sample_ohlcv_data,
        min_confidence=0.6  # Lower threshold
    )
    
    assert result == mock_confirmation
    assert result.confidence_score >= 0.6

@pytest.mark.asyncio
async def test_position_tracking(order_executor, mock_coinbase_client):
    """Test position tracking functionality"""
    # Setup mock responses
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    mock_coinbase_client.get_product.return_value = {"price": "51000.0"}
    
    # Execute buy order
    order_result = await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Check position creation
    position = await order_executor.get_position("BTC-USD")
    assert position is not None
    assert position.product_id == "BTC-USD"
    assert position.side == OrderSide.BUY
    assert position.size == 1.0
    assert position.entry_price == 50000.0
    assert position.current_price == 51000.0
    assert position.unrealized_pnl == 1000.0  # (51000 - 50000) * 1.0
    assert position.status == "OPEN"
    assert "test_order_1" in position.orders
    
    # Execute sell order to partially close position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_2",
        "product_id": "BTC-USD",
        "side": "SELL",
        "size": "0.5",
        "status": "FILLED",
        "filled_size": "0.5",
        "average_filled_price": "51000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.SELL,
        size=0.5
    )
    
    # Check position update
    position = await order_executor.get_position("BTC-USD")
    assert position.size == 0.5
    assert position.status == "PARTIALLY_CLOSED"
    assert position.realized_pnl == 500.0  # (51000 - 50000) * 0.5
    assert "test_order_2" in position.orders

@pytest.mark.asyncio
async def test_position_tracking_errors(order_executor, mock_coinbase_client):
    """Test error handling in position tracking"""
    # Test closing non-existent position
    with pytest.raises(ValueError, match="No open position found"):
        await order_executor.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.SELL,
            size=1.0
        )
    
    # Test invalid position size
    with pytest.raises(ValueError, match="Invalid position size"):
        await order_executor.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=0.0
        )
    
    # Setup position for partial close tests
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Test closing more than position size
    with pytest.raises(ValueError, match="Close size exceeds position size"):
        await order_executor.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.SELL,
            size=1.5
        )

@pytest.mark.asyncio
async def test_order_state_error_handling(order_executor, mock_coinbase_client):
    """Test error handling in order state management"""
    # Test invalid order status update
    with pytest.raises(ValueError, match="Invalid order status transition"):
        await order_executor._update_order_state("non_existent_order", OrderStatus.FILLED)
    
    # Setup order for testing
    mock_coinbase_client.create_limit_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "price": "50000.0",
        "status": "PENDING"
    }
    
    await order_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        price=50000.0
    )
    
    # Test invalid state transition
    with pytest.raises(ValueError, match="Invalid state transition"):
        await order_executor._update_order_state("test_order_1", OrderStatus.CANCELLED)
        await order_executor._update_order_state("test_order_1", OrderStatus.PENDING)

@pytest.mark.asyncio
async def test_partial_fills(order_executor, mock_coinbase_client):
    """Test handling of partial fills"""
    # Setup initial partial fill
    mock_coinbase_client.create_limit_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "price": "50000.0",
        "status": "PENDING",
        "filled_size": "0.0",
        "remaining_size": "1.0"
    }
    
    await order_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        price=50000.0
    )
    
    # Simulate partial fill
    await order_executor._update_order_state(
        "test_order_1",
        OrderStatus.PARTIALLY_FILLED,
        filled_size=0.5,
        remaining_size=0.5,
        average_fill_price=50000.0
    )
    
    # Check order state
    order_state = order_executor._order_states.get("test_order_1")
    assert order_state.status == OrderStatus.PARTIALLY_FILLED
    assert order_state.filled_size == 0.5
    assert order_state.remaining_size == 0.5
    
    # Check position
    position = await order_executor.get_position("BTC-USD")
    assert position.size == 0.5
    assert position.status == "PARTIALLY_FILLED"
    
    # Complete the fill
    await order_executor._update_order_state(
        "test_order_1",
        OrderStatus.FILLED,
        filled_size=1.0,
        remaining_size=0.0,
        average_fill_price=50000.0
    )
    
    # Check final state
    order_state = order_executor._order_states.get("test_order_1")
    assert order_state.status == OrderStatus.FILLED
    assert order_state.filled_size == 1.0
    assert order_state.remaining_size == 0.0
    
    position = await order_executor.get_position("BTC-USD")
    assert position.size == 1.0
    assert position.status == "OPEN"

@pytest.mark.asyncio
async def test_order_state_tracking(order_executor, mock_coinbase_client):
    """Test order state transition tracking"""
    # Setup mock responses
    mock_coinbase_client.create_limit_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "price": "50000.0",
        "status": "PENDING"
    }
    
    # Place limit order
    order_result = await order_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        price=50000.0
    )
    
    # Check initial order state
    order_state = order_executor._order_states.get("test_order_1")
    assert order_state is not None
    assert order_state.status == OrderStatus.PENDING
    assert len(order_state.state_transitions) == 1
    assert order_state.state_transitions[0]["from"] is None
    assert order_state.state_transitions[0]["to"] == OrderStatus.PENDING
    
    # Update order status to FILLED
    await order_executor._update_order_state("test_order_1", OrderStatus.FILLED)
    
    # Check state transition
    assert order_state.status == OrderStatus.FILLED
    assert len(order_state.state_transitions) == 2
    assert order_state.state_transitions[1]["from"] == OrderStatus.PENDING
    assert order_state.state_transitions[1]["to"] == OrderStatus.FILLED
    
    # Check performance metrics
    metrics = await order_executor.get_performance_metrics()
    assert metrics["total_orders"] == 1
    assert metrics["success_rate"] == 1.0
    assert metrics["avg_fill_rate"] == 1.0
    assert "avg_execution_latency" in metrics

@pytest.mark.asyncio
async def test_position_risk_metrics(order_executor, mock_coinbase_client):
    """Test position risk metrics calculation"""
    # Setup mock responses for initial buy
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    mock_coinbase_client.get_product.return_value = {"price": "51000.0"}
    
    # Execute buy order
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Get risk metrics
    risk_metrics = await order_executor.get_position_risk_metrics("BTC-USD")
    
    # Check risk metrics
    assert "unrealized_pnl_pct" in risk_metrics
    assert risk_metrics["unrealized_pnl_pct"] == pytest.approx(2.0)  # ((51000-50000)/50000) * 100
    assert risk_metrics["position_value"] == 51000.0
    assert risk_metrics["max_drawdown"] == 0.0
    assert "time_in_position" in risk_metrics

@pytest.mark.asyncio
async def test_emergency_controls(order_executor, mock_coinbase_client):
    """Test emergency trading controls and risk management."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "2.0",
        "status": "FILLED",
        "filled_size": "2.0",
        "average_filled_price": "50000.0"
    }
    
    # Create a position that exceeds max size
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=2.0
    )
    
    # Verify trading halt is triggered on risk threshold breach
    position = await order_executor.get_position("BTC-USD")
    is_safe, message = await order_executor.check_risk_thresholds(position)
    assert not is_safe
    assert "Position size" in message
    assert not order_executor._trading_enabled
    
    # Verify emergency position reduction
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_2",
        "product_id": "BTC-USD",
        "side": "SELL",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    # Update position should trigger emergency reduction
    await order_executor.update_position("BTC-USD", {
        "product_id": "BTC-USD",
        "side": OrderSide.BUY,
        "filled_size": "2.0",
        "average_filled_price": "50000.0"
    })
    
    # Verify position was reduced
    position = await order_executor.get_position("BTC-USD")
    assert position.size == 1.0
    
    # Test trading resume
    await order_executor.resume_trading("Test resume")
    assert order_executor._trading_enabled

@pytest.mark.asyncio
async def test_risk_threshold_monitoring(order_executor, mock_coinbase_client):
    """Test risk threshold monitoring and updates."""
    # Update risk thresholds
    order_executor.update_risk_thresholds({
        'max_position_size': 0.5,
        'max_drawdown_pct': 2.0
    })
    
    assert order_executor._risk_thresholds['max_position_size'] == 0.5
    assert order_executor._risk_thresholds['max_drawdown_pct'] == 2.0
    
    # Setup position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "0.4",
        "status": "FILLED",
        "filled_size": "0.4",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.4
    )
    
    # Verify position within limits
    position = await order_executor.get_position("BTC-USD")
    is_safe, message = await order_executor.check_risk_thresholds(position)
    assert is_safe
    assert "within limits" in message
    
    # Test drawdown threshold
    position.unrealized_pnl = -3.0  # Exceeds max_drawdown_pct
    is_safe, message = await order_executor.check_risk_thresholds(position)
    assert not is_safe
    assert "drawdown" in message

@pytest.mark.asyncio
async def test_daily_stats_tracking(order_executor, mock_coinbase_client):
    """Test daily trading statistics tracking."""
    # Initialize daily stats
    order_executor._daily_stats.update({
        'start_balance': 100000.0,
        'current_balance': 100000.0,
        'total_pnl': 0.0,
        'trade_count': 0
    })
    
    # Simulate trades
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Update daily stats
    order_executor._daily_stats['current_balance'] = 102000.0
    order_executor._daily_stats['total_pnl'] = 2000.0
    order_executor._daily_stats['trade_count'] = 1
    
    # Verify daily stats
    stats = await order_executor.get_daily_stats()
    assert stats['start_balance'] == 100000.0
    assert stats['current_balance'] == 102000.0
    assert stats['total_pnl'] == 2000.0
    assert stats['pnl_percentage'] == 2.0
    assert stats['trade_count'] == 1
    
    # Test daily loss threshold
    order_executor._daily_stats['current_balance'] = 96000.0
    order_executor._daily_stats['total_pnl'] = -4000.0
    
    # Should trigger halt due to exceeding max_daily_loss_pct
    position = await order_executor.get_position("BTC-USD")
    is_safe, message = await order_executor.check_risk_thresholds(position)
    assert not is_safe
    assert "Daily loss" in message

@pytest.mark.asyncio
async def test_halt_callbacks(order_executor):
    """Test trading halt callback notifications."""
    halt_reasons = []
    
    async def on_halt(reason: str):
        halt_reasons.append(reason)
    
    # Register callback
    order_executor.register_halt_callback(on_halt)
    
    # Trigger halt
    await order_executor.halt_trading("Test halt reason")
    
    # Verify callback was called
    assert len(halt_reasons) == 1
    assert halt_reasons[0] == "Test halt reason"
    assert not order_executor._trading_enabled

@pytest.mark.asyncio
async def test_position_monitoring(order_executor, mock_coinbase_client):
    """Test position monitoring functionality."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    # Create position
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Setup price updates
    mock_coinbase_client.get_product.side_effect = [
        {"price": "51000.0"},  # +2% (no event)
        {"price": "52500.0"},  # +3% (triggers event)
        {"price": "47500.0"},  # -5% (triggers event and halt)
    ]
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for updates
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Check events
    events = await order_executor.get_position_events(product_id="BTC-USD")
    pnl_events = [e for e in events if e["type"] == "pnl_change"]
    risk_events = [e for e in events if e["type"] == "risk_threshold_breach"]
    
    assert len(pnl_events) >= 2  # Should have at least two significant P&L changes
    assert len(risk_events) >= 1  # Should have triggered risk threshold breach
    
    # Verify trading was halted
    assert not order_executor._trading_enabled

@pytest.mark.asyncio
async def test_risk_metrics_aggregation(order_executor, mock_coinbase_client):
    """Test aggregation of risk metrics across positions."""
    # Setup multiple positions
    mock_coinbase_client.create_market_order.side_effect = [
        {
            "order_id": "test_order_1",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "1.0",
            "status": "FILLED",
            "filled_size": "1.0",
            "average_filled_price": "50000.0"
        },
        {
            "order_id": "test_order_2",
            "product_id": "ETH-USD",
            "side": "BUY",
            "size": "10.0",
            "status": "FILLED",
            "filled_size": "10.0",
            "average_filled_price": "2000.0"
        }
    ]
    
    mock_coinbase_client.get_product.side_effect = [
        {"price": "51000.0"},  # BTC price
        {"price": "2100.0"}    # ETH price
    ]
    
    # Create positions
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    await order_executor.execute_market_order(
        product_id="ETH-USD",
        side=OrderSide.BUY,
        size=10.0
    )
    
    # Initialize daily stats
    order_executor._daily_stats.update({
        'start_balance': 100000.0,
        'current_balance': 102000.0,
        'total_pnl': 2000.0,
        'trade_count': 2
    })
    
    # Get aggregated metrics
    metrics = await order_executor.get_aggregated_risk_metrics()
    
    # Verify metrics
    assert metrics["position_count"] == 2
    assert metrics["total_position_value"] == pytest.approx(72000.0)  # 51000 + (2100 * 10)
    assert metrics["total_unrealized_pnl"] == pytest.approx(2000.0)  # (51000-50000) + 10*(2100-2000)
    assert metrics["total_unrealized_pnl_pct"] == pytest.approx(2.78, rel=0.01)  # 2000/72000 * 100
    assert metrics["daily_pnl"] == 2000.0
    assert metrics["daily_pnl_pct"] == 2.0
    assert metrics["risk_exposure"] == pytest.approx(0.72)  # 72000/100000

@pytest.mark.asyncio
async def test_position_event_filtering(order_executor):
    """Test position event filtering functionality."""
    # Add test events
    test_events = [
        {
            "type": "pnl_change",
            "product_id": "BTC-USD",
            "old_pnl": 1000.0,
            "new_pnl": 1500.0,
            "change_pct": 2.5,
            "timestamp": datetime.now()
        },
        {
            "type": "risk_threshold_breach",
            "product_id": "BTC-USD",
            "message": "Position size exceeded",
            "timestamp": datetime.now()
        },
        {
            "type": "pnl_change",
            "product_id": "ETH-USD",
            "old_pnl": 500.0,
            "new_pnl": 800.0,
            "change_pct": 1.5,
            "timestamp": datetime.now()
        }
    ]
    
    order_executor._position_events.extend(test_events)
    
    # Test filtering by product
    btc_events = await order_executor.get_position_events(product_id="BTC-USD")
    assert len(btc_events) == 2
    
    # Test filtering by event type
    pnl_events = await order_executor.get_position_events(event_type="pnl_change")
    assert len(pnl_events) == 2
    
    # Test filtering by time
    future_time = datetime.now() + timedelta(minutes=1)
    future_events = await order_executor.get_position_events(start_time=future_time)
    assert len(future_events) == 0
    
    # Test clearing events
    order_executor.clear_position_events()
    all_events = await order_executor.get_position_events()
    assert len(all_events) == 0

@pytest.mark.asyncio
async def test_multiple_position_monitoring(order_executor, mock_coinbase_client):
    """Test monitoring of multiple positions simultaneously."""
    # Setup initial positions
    mock_coinbase_client.create_market_order.side_effect = [
        {
            "order_id": "btc_order_1",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "0.5",
            "status": "FILLED",
            "filled_size": "0.5",
            "average_filled_price": "50000.0"
        },
        {
            "order_id": "eth_order_1",
            "product_id": "ETH-USD",
            "side": "BUY",
            "size": "5.0",
            "status": "FILLED",
            "filled_size": "5.0",
            "average_filled_price": "2000.0"
        }
    ]
    
    # Create positions
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.5
    )
    
    await order_executor.execute_market_order(
        product_id="ETH-USD",
        side=OrderSide.BUY,
        size=5.0
    )
    
    # Setup price updates sequence for both assets
    mock_coinbase_client.get_product.side_effect = [
        {"price": "51000.0"},  # BTC +2%
        {"price": "2050.0"},   # ETH +2.5%
        {"price": "52000.0"},  # BTC +4%
        {"price": "1900.0"},   # ETH -5%
        {"price": "49000.0"},  # BTC -2%
        {"price": "1800.0"}    # ETH -10%
    ]
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for updates
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Check events for BTC position
    btc_events = await order_executor.get_position_events(product_id="BTC-USD")
    btc_pnl_events = [e for e in btc_events if e["type"] == "pnl_change"]
    assert len(btc_pnl_events) >= 2  # Should have multiple P&L updates
    
    # Check events for ETH position
    eth_events = await order_executor.get_position_events(product_id="ETH-USD")
    eth_pnl_events = [e for e in eth_events if e["type"] == "pnl_change"]
    eth_risk_events = [e for e in eth_events if e["type"] == "risk_threshold_breach"]
    assert len(eth_pnl_events) >= 2  # Should have multiple P&L updates
    assert len(eth_risk_events) >= 1  # Should have triggered risk threshold breach
    
    # Verify aggregated risk metrics
    metrics = await order_executor.get_aggregated_risk_metrics()
    assert metrics["position_count"] == 2
    assert metrics["total_position_value"] > 0
    assert "total_unrealized_pnl" in metrics
    assert "risk_exposure" in metrics

@pytest.mark.asyncio
async def test_complex_risk_scenarios(order_executor, mock_coinbase_client):
    """Test handling of complex risk scenarios with multiple positions."""
    # Initialize daily stats
    order_executor._daily_stats.update({
        'start_balance': 100000.0,
        'current_balance': 100000.0,
        'total_pnl': 0.0,
        'trade_count': 0
    })
    
    # Set strict risk thresholds
    order_executor.update_risk_thresholds({
        'max_position_size': 1.0,
        'max_drawdown_pct': 5.0,
        'max_daily_loss_pct': 2.0,
        'max_leverage': 2.0
    })
    
    # Setup mock responses for position creation
    mock_coinbase_client.create_market_order.side_effect = [
        {
            "order_id": "btc_long",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "0.8",
            "status": "FILLED",
            "filled_size": "0.8",
            "average_filled_price": "50000.0"
        },
        {
            "order_id": "eth_short",
            "product_id": "ETH-USD",
            "side": "SELL",
            "size": "10.0",
            "status": "FILLED",
            "filled_size": "10.0",
            "average_filled_price": "2000.0"
        }
    ]
    
    # Create positions
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.8
    )
    
    await order_executor.execute_market_order(
        product_id="ETH-USD",
        side=OrderSide.SELL,
        size=10.0
    )
    
    # Simulate price movements that trigger multiple risk scenarios
    price_updates = [
        # Scenario 1: BTC position approaching size limit
        ({"price": "51000.0"}, {"price": "2000.0"}),  # Normal state
        ({"price": "52000.0"}, {"price": "1950.0"}),  # Both profitable
        
        # Scenario 2: ETH position exceeding drawdown limit
        ({"price": "52000.0"}, {"price": "2200.0"}),  # ETH short loss
        
        # Scenario 3: Combined positions approaching daily loss limit
        ({"price": "48000.0"}, {"price": "2300.0"}),  # Both losing
    ]
    
    for btc_price, eth_price in price_updates:
        # Update prices
        mock_coinbase_client.get_product.side_effect = [btc_price, eth_price]
        
        # Update positions
        await order_executor.update_position("BTC-USD", {
            "product_id": "BTC-USD",
            "side": OrderSide.BUY,
            "filled_size": "0.8",
            "average_filled_price": btc_price["price"]
        })
        
        await order_executor.update_position("ETH-USD", {
            "product_id": "ETH-USD",
            "side": OrderSide.SELL,
            "filled_size": "10.0",
            "average_filled_price": eth_price["price"]
        })
        
        # Wait for monitoring updates
        await asyncio.sleep(0.1)
    
    # Get all events
    all_events = await order_executor.get_position_events()
    risk_events = [e for e in all_events if e["type"] == "risk_threshold_breach"]
    
    # Verify risk events were generated
    assert len(risk_events) > 0
    
    # Check if trading was halted
    assert not order_executor._trading_enabled
    
    # Verify emergency position reduction was triggered
    btc_position = await order_executor.get_position("BTC-USD")
    eth_position = await order_executor.get_position("ETH-USD")
    
    # Get final risk metrics
    final_metrics = await order_executor.get_aggregated_risk_metrics()
    
    # Verify risk exposure was reduced
    assert final_metrics["risk_exposure"] < 1.0
    assert "max_drawdown" in final_metrics
    assert "daily_pnl_pct" in final_metrics

@pytest.mark.asyncio
async def test_position_lifecycle_events(order_executor, mock_coinbase_client):
    """Test complete position lifecycle with events and monitoring."""
    # Setup mock responses
    mock_coinbase_client.create_market_order.side_effect = [
        {
            "order_id": "entry_order",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "1.0",
            "status": "FILLED",
            "filled_size": "1.0",
            "average_filled_price": "50000.0"
        },
        {
            "order_id": "partial_close",
            "product_id": "BTC-USD",
            "side": "SELL",
            "size": "0.5",
            "status": "FILLED",
            "filled_size": "0.5",
            "average_filled_price": "52000.0"
        },
        {
            "order_id": "final_close",
            "product_id": "BTC-USD",
            "side": "SELL",
            "size": "0.5",
            "status": "FILLED",
            "filled_size": "0.5",
            "average_filled_price": "53000.0"
        }
    ]
    
    # Create initial position
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Start position monitoring
    await order_executor.start_position_monitoring()
    
    # Simulate price updates and partial close
    mock_coinbase_client.get_product.return_value = {"price": "52000.0"}
    
    # Partial close
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.SELL,
        size=0.5
    )
    
    # Update price and complete close
    mock_coinbase_client.get_product.return_value = {"price": "53000.0"}
    
    # Final close
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.SELL,
        size=0.5
    )
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Get all position events
    events = await order_executor.get_position_events(product_id="BTC-USD")
    
    # Verify event sequence
    entry_events = [e for e in events if "entry" in e.get("message", "").lower()]
    partial_close_events = [e for e in events if "partial" in e.get("message", "").lower()]
    close_events = [e for e in events if "closed" in e.get("message", "").lower()]
    pnl_events = [e for e in events if e["type"] == "pnl_change"]
    
    assert len(entry_events) > 0
    assert len(partial_close_events) > 0
    assert len(close_events) > 0
    assert len(pnl_events) > 0
    
    # Verify position status transitions
    position = await order_executor.get_position("BTC-USD")
    assert position.status == "CLOSED"
    assert position.realized_pnl == 2500.0  # (52000-50000)*0.5 + (53000-50000)*0.5
    
    # Verify monitoring was properly cleaned up
    assert "BTC-USD" not in order_executor._position_monitors

@pytest.mark.asyncio
async def test_position_monitoring_edge_cases(order_executor, mock_coinbase_client):
    """Test edge cases in position monitoring."""
    # Test monitoring non-existent position
    with pytest.raises(ValueError, match="No position found"):
        await order_executor.start_position_monitoring("NON-EXISTENT")
    
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Test starting monitoring twice
    await order_executor.start_position_monitoring()
    await order_executor.start_position_monitoring()  # Should not create duplicate monitor
    
    assert len(order_executor._position_monitors) == 1
    
    # Test monitoring during price API failures
    mock_coinbase_client.get_product.side_effect = CoinbaseError("API Error")
    await asyncio.sleep(1)  # Allow monitor to attempt update
    
    events = await order_executor.get_position_events(product_id="BTC-USD")
    error_events = [e for e in events if e["type"] == "error"]
    assert len(error_events) > 0
    assert "API Error" in error_events[0]["message"]
    
    # Test stopping non-existent monitor
    await order_executor.stop_position_monitoring("ETH-USD")  # Should not raise error
    
    # Clean up
    await order_executor.stop_position_monitoring()

@pytest.mark.asyncio
async def test_risk_threshold_edge_cases(order_executor, mock_coinbase_client):
    """Test edge cases in risk threshold management."""
    # Test invalid threshold updates
    with pytest.raises(ValueError, match="Invalid threshold value"):
        order_executor.update_risk_thresholds({
            'max_position_size': -1.0
        })
    
    with pytest.raises(ValueError, match="Invalid threshold value"):
        order_executor.update_risk_thresholds({
            'max_drawdown_pct': 101.0
        })
    
    # Setup position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Test threshold check with missing metrics
    position = await order_executor.get_position("BTC-USD")
    position.unrealized_pnl = None
    is_safe, message = await order_executor.check_risk_thresholds(position)
    assert is_safe  # Should not trigger threshold breach for missing metrics
    assert "Missing metrics" in message
    
    # Test emergency reduction with API failure
    mock_coinbase_client.create_market_order.side_effect = CoinbaseError("API Error")
    await order_executor._emergency_position_reduction(position)
    
    events = await order_executor.get_position_events(product_id="BTC-USD")
    error_events = [e for e in events if e["type"] == "error"]
    assert len(error_events) > 0
    assert "emergency reduction failed" in error_events[-1]["message"].lower()

@pytest.mark.asyncio
async def test_concurrent_position_updates(order_executor, mock_coinbase_client):
    """Test handling of concurrent position updates."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Simulate concurrent updates
    update_tasks = []
    for price in range(51000, 53000, 100):
        mock_coinbase_client.get_product.return_value = {"price": str(price)}
        task = order_executor.update_position("BTC-USD", {
            "product_id": "BTC-USD",
            "side": OrderSide.BUY,
            "filled_size": "1.0",
            "average_filled_price": str(price)
        })
        update_tasks.append(task)
    
    # Execute updates concurrently
    await asyncio.gather(*update_tasks)
    
    # Verify events are in order
    events = await order_executor.get_position_events(product_id="BTC-USD")
    pnl_events = [e for e in events if e["type"] == "pnl_change"]
    
    # Check timestamps are sequential
    timestamps = [e["timestamp"] for e in pnl_events]
    assert timestamps == sorted(timestamps)

@pytest.mark.asyncio
async def test_risk_metrics_calculation_edge_cases(order_executor, mock_coinbase_client):
    """Test edge cases in risk metrics calculation."""
    # Setup positions with edge case values
    mock_coinbase_client.create_market_order.side_effect = [
        {
            "order_id": "test_order_1",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "0.00001",  # Very small position
            "status": "FILLED",
            "filled_size": "0.00001",
            "average_filled_price": "50000.0"
        },
        {
            "order_id": "test_order_2",
            "product_id": "ETH-USD",
            "side": "SELL",
            "size": "1000.0",  # Very large position
            "status": "FILLED",
            "filled_size": "1000.0",
            "average_filled_price": "2000.0"
        }
    ]
    
    # Create positions
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.00001
    )
    
    await order_executor.execute_market_order(
        product_id="ETH-USD",
        side=OrderSide.SELL,
        size=1000.0
    )
    
    # Test metrics with extreme price movements
    mock_coinbase_client.get_product.side_effect = [
        {"price": "100000.0"},  # BTC +100%
        {"price": "1.0"}        # ETH -99.95%
    ]
    
    # Get metrics
    metrics = await order_executor.get_aggregated_risk_metrics()
    
    # Verify handling of extreme values
    assert metrics["total_position_value"] > 0
    assert -100 <= metrics["total_unrealized_pnl_pct"] <= 100  # Should be capped
    assert 0 <= metrics["risk_exposure"] <= 1  # Should be normalized
    
    # Test with zero prices
    mock_coinbase_client.get_product.side_effect = [
        {"price": "0.0"},
        {"price": "0.0"}
    ]
    
    metrics = await order_executor.get_aggregated_risk_metrics()
    assert metrics["total_position_value"] >= 0
    assert metrics["risk_exposure"] >= 0

@pytest.mark.asyncio
async def test_position_monitoring_stress(order_executor, mock_coinbase_client):
    """Test position monitoring under stress conditions."""
    # Setup multiple positions
    positions = []
    mock_responses = []
    
    # Create 5 positions with different products
    for i, product in enumerate(["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "DOT-USD"]):
        mock_response = {
            "order_id": f"test_order_{i}",
            "product_id": product,
            "side": "BUY",
            "size": "1.0",
            "status": "FILLED",
            "filled_size": "1.0",
            "average_filled_price": f"{1000.0 * (i + 1)}"
        }
        mock_responses.append(mock_response)
        positions.append(product)
    
    mock_coinbase_client.create_market_order.side_effect = mock_responses
    
    # Create positions
    for i, product in enumerate(positions):
        await order_executor.execute_market_order(
            product_id=product,
            side=OrderSide.BUY,
            size=1.0
        )
    
    # Setup rapid price updates
    price_updates = []
    for i in range(10):  # 10 updates per position
        for j, product in enumerate(positions):
            base_price = 1000.0 * (j + 1)
            price_updates.append({"price": str(base_price * (1 + (i * 0.01)))})
    
    mock_coinbase_client.get_product.side_effect = price_updates
    
    # Start monitoring all positions
    await order_executor.start_position_monitoring()
    
    # Simulate rapid updates
    update_tasks = []
    for product in positions:
        for _ in range(10):  # 10 updates per position
            task = order_executor.update_position(product, {
                "product_id": product,
                "side": OrderSide.BUY,
                "filled_size": "1.0",
                "average_filled_price": "1000.0"
            })
            update_tasks.append(task)
    
    # Execute updates concurrently
    await asyncio.gather(*update_tasks)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Verify events for each position
    for product in positions:
        events = await order_executor.get_position_events(product_id=product)
        assert len(events) > 0
        
        # Check event ordering
        timestamps = [e["timestamp"] for e in events]
        assert timestamps == sorted(timestamps)
    
    # Verify aggregated metrics are calculated correctly
    metrics = await order_executor.get_aggregated_risk_metrics()
    assert metrics["position_count"] == len(positions)
    assert metrics["total_position_value"] > 0
    assert "total_unrealized_pnl" in metrics
    assert "risk_exposure" in metrics

@pytest.mark.asyncio
async def test_position_monitoring_error_recovery(order_executor, mock_coinbase_client):
    """Test error recovery in position monitoring."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Setup price update sequence with intermittent failures
    mock_coinbase_client.get_product.side_effect = [
        {"price": "51000.0"},                    # Normal update
        CoinbaseError("API Error"),              # API failure
        CoinbaseError("Rate limit exceeded"),     # Rate limit
        {"price": "52000.0"},                    # Recovery
        CoinbaseError("Network timeout"),        # Network issue
        {"price": "53000.0"}                     # Recovery
    ]
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for updates and recovery attempts
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Check events
    events = await order_executor.get_position_events(product_id="BTC-USD")
    error_events = [e for e in events if e["type"] == "error"]
    recovery_events = [e for e in events if e["type"] == "recovery"]
    price_update_events = [e for e in events if e["type"] == "price_update"]
    
    # Verify error handling
    assert len(error_events) >= 3  # Should have recorded API, rate limit, and network errors
    assert len(recovery_events) >= 2  # Should have recorded successful recoveries
    assert len(price_update_events) >= 3  # Should have recorded successful price updates
    
    # Verify error event details
    api_errors = [e for e in error_events if "API Error" in e["message"]]
    rate_limit_errors = [e for e in error_events if "Rate limit" in e["message"]]
    network_errors = [e for e in error_events if "Network" in e["message"]]
    
    assert len(api_errors) > 0
    assert len(rate_limit_errors) > 0
    assert len(network_errors) > 0
    
    # Verify monitoring continued after errors
    assert order_executor._position_monitors["BTC-USD"] is not None

@pytest.mark.asyncio
async def test_position_monitoring_reconnection(order_executor, mock_coinbase_client):
    """Test reconnection behavior in position monitoring."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Setup connection state simulation
    connection_states = [
        (CoinbaseError("Connection lost"), None),           # Initial disconnect
        (CoinbaseError("Connection lost"), None),           # Failed reconnect
        (None, {"price": "51000.0"}),                      # Successful reconnect
        (CoinbaseError("Connection lost"), None),           # Another disconnect
        (None, {"price": "52000.0"}),                      # Final reconnect
    ]
    
    current_state = 0
    
    def get_product_with_connection_state(*args, **kwargs):
        nonlocal current_state
        error, response = connection_states[current_state]
        current_state = min(current_state + 1, len(connection_states) - 1)
        if error:
            raise error
        return response
    
    mock_coinbase_client.get_product.side_effect = get_product_with_connection_state
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for reconnection attempts
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Check events
    events = await order_executor.get_position_events(product_id="BTC-USD")
    disconnect_events = [e for e in events if e["type"] == "disconnect"]
    reconnect_events = [e for e in events if e["type"] == "reconnect"]
    
    # Verify reconnection handling
    assert len(disconnect_events) >= 2  # Should have recorded disconnections
    assert len(reconnect_events) >= 2  # Should have recorded successful reconnections
    
    # Verify event sequence
    event_sequence = []
    for event in events:
        if event["type"] in ["disconnect", "reconnect", "price_update"]:
            event_sequence.append(event["type"])
    
    # Check that reconnects follow disconnects
    for i, event_type in enumerate(event_sequence):
        if event_type == "reconnect" and i > 0:
            assert "disconnect" in event_sequence[:i]
    
    # Verify monitoring state after reconnections
    assert order_executor._position_monitors["BTC-USD"] is not None

@pytest.mark.asyncio
async def test_position_monitoring_data_consistency(order_executor, mock_coinbase_client):
    """Test data consistency during monitoring interruptions."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Setup price updates with missing data scenarios
    price_updates = [
        {"price": "51000.0"},                    # Normal update
        {"price": None},                         # Missing price
        {"price": ""},                           # Empty price
        {"price": "52000.0"},                    # Normal update
        {"price": "invalid"},                    # Invalid price
        {"price": "53000.0"},                    # Normal update
    ]
    
    current_update = 0
    
    def get_product_with_data_issues(*args, **kwargs):
        nonlocal current_update
        response = price_updates[current_update]
        current_update = min(current_update + 1, len(price_updates) - 1)
        return response
    
    mock_coinbase_client.get_product.side_effect = get_product_with_data_issues
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for updates
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Check events
    events = await order_executor.get_position_events(product_id="BTC-USD")
    data_error_events = [e for e in events if e["type"] == "data_error"]
    price_update_events = [e for e in events if e["type"] == "price_update"]
    
    # Verify data error handling
    assert len(data_error_events) >= 3  # Should have recorded missing, empty, and invalid price errors
    assert len(price_update_events) >= 3  # Should have recorded valid price updates
    
    # Verify position data consistency
    position = await order_executor.get_position("BTC-USD")
    assert position.current_price is not None
    assert isinstance(position.current_price, float)
    assert position.unrealized_pnl is not None
    
    # Verify last valid price was maintained during errors
    last_valid_price = None
    for event in events:
        if event["type"] == "price_update":
            last_valid_price = float(event["price"])
        elif event["type"] == "data_error":
            position = await order_executor.get_position("BTC-USD")
            assert position.current_price == last_valid_price

@pytest.mark.asyncio
async def test_monitoring_error_recovery_with_backoff(order_executor, mock_coinbase_client):
    """Test error recovery with exponential backoff in position monitoring."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Setup sequence of errors with increasing severity
    error_sequence = [
        CoinbaseError("Temporary API Error"),
        CoinbaseError("Rate limit exceeded"),
        CoinbaseError("Service Unavailable"),
        {"price": "51000.0"},  # Recovery
        CoinbaseError("Internal Server Error"),
        {"price": "52000.0"}   # Final recovery
    ]
    
    mock_coinbase_client.get_product.side_effect = error_sequence
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for recovery attempts
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Check events
    events = await order_executor.get_position_events(product_id="BTC-USD")
    error_events = [e for e in events if e["type"] == "error"]
    backoff_events = [e for e in events if "backoff" in e.get("message", "").lower()]
    recovery_events = [e for e in events if e["type"] == "recovery"]
    
    # Verify backoff strategy
    assert len(error_events) >= 3
    assert len(backoff_events) >= 2  # Should show increasing backoff periods
    assert len(recovery_events) >= 2
    
    # Verify backoff periods are increasing
    backoff_times = [
        float(e["message"].split("Retrying in ")[1].split(" seconds")[0])
        for e in backoff_events
    ]
    assert all(backoff_times[i] <= backoff_times[i+1] for i in range(len(backoff_times)-1))

@pytest.mark.asyncio
async def test_monitoring_data_validation(order_executor, mock_coinbase_client):
    """Test data validation and sanitization in position monitoring."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Setup price updates with various data issues
    price_updates = [
        {"price": "51000.0"},                    # Valid price
        {"price": "-1000.0"},                    # Negative price
        {"price": "1e10"},                       # Extremely large price
        {"price": "50000.00000001"},            # Too many decimals
        {"price": "52000.0 "},                   # Extra whitespace
        {"price": "53000.0\n"},                  # Newline character
        {"price": "54,000.0"},                   # Invalid format
        {"price": "55000.0"}                     # Valid price
    ]
    
    mock_coinbase_client.get_product.side_effect = price_updates
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for updates
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Check events
    events = await order_executor.get_position_events(product_id="BTC-USD")
    validation_events = [e for e in events if e["type"] == "validation"]
    price_update_events = [e for e in events if e["type"] == "price_update"]
    
    # Verify data validation
    assert len(validation_events) >= 5  # Should have caught various validation issues
    assert len(price_update_events) >= 3  # Should have recorded valid price updates
    
    # Verify specific validation issues
    validation_messages = [e["message"] for e in validation_events]
    assert any("negative" in msg.lower() for msg in validation_messages)
    assert any("large" in msg.lower() for msg in validation_messages)
    assert any("decimal" in msg.lower() for msg in validation_messages)
    assert any("format" in msg.lower() for msg in validation_messages)
    
    # Verify position data remains valid
    position = await order_executor.get_position("BTC-USD")
    assert position.current_price > 0
    assert isinstance(position.current_price, float)
    assert len(str(position.current_price).split(".")[-1]) <= 8  # Check decimal places

@pytest.mark.asyncio
async def test_monitoring_state_persistence(order_executor, mock_coinbase_client):
    """Test monitoring state persistence across connection issues."""
    # Setup initial position
    mock_coinbase_client.create_market_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "status": "FILLED",
        "filled_size": "1.0",
        "average_filled_price": "50000.0"
    }
    
    await order_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0
    )
    
    # Initialize monitoring state
    initial_state = {
        "last_price": 50000.0,
        "high_price": 50000.0,
        "low_price": 50000.0,
        "price_updates": 0,
        "error_count": 0
    }
    
    order_executor._monitoring_states["BTC-USD"] = initial_state.copy()
    
    # Setup price updates with connection issues
    mock_coinbase_client.get_product.side_effect = [
        {"price": "51000.0"},
        CoinbaseError("Connection lost"),
        CoinbaseError("Connection lost"),
        {"price": "52000.0"},
        {"price": "49000.0"}
    ]
    
    # Start monitoring
    await order_executor.start_position_monitoring()
    
    # Wait for updates
    await asyncio.sleep(3)
    
    # Stop monitoring
    await order_executor.stop_position_monitoring()
    
    # Get final state
    final_state = order_executor._monitoring_states.get("BTC-USD", {})
    
    # Verify state persistence
    assert final_state["last_price"] is not None
    assert final_state["high_price"] >= initial_state["high_price"]
    assert final_state["low_price"] <= initial_state["low_price"]
    assert final_state["price_updates"] > initial_state["price_updates"]
    assert final_state["error_count"] >= 2
    
    # Verify events reflect state changes
    events = await order_executor.get_position_events(product_id="BTC-USD")
    state_events = [e for e in events if e["type"] == "state_update"]
    
    assert len(state_events) > 0
    assert any("high" in e["message"].lower() for e in state_events)
    assert any("low" in e["message"].lower() for e in state_events)

@pytest.mark.asyncio
async def test_order_modification(order_executor, mock_coinbase_client):
    """Test order modification functionality."""
    # Setup initial order
    mock_coinbase_client.create_order.return_value = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "price": "50000.0",
        "type": "LIMIT",
        "status": "OPEN"
    }
    
    # Place initial order
    result = await order_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        price=50000.0
    )
    assert result.success
    original_order_id = result.order.order_id
    
    # Setup modification response
    mock_coinbase_client.create_order.return_value = {
        "order_id": "test_order_2",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.5",
        "price": "51000.0",
        "type": "LIMIT",
        "status": "OPEN"
    }
    
    # Modify order
    mod_result = await order_executor.modify_order(
        order_id=original_order_id,
        new_size=1.5,
        new_price=51000.0
    )
    
    assert mod_result.success
    assert mod_result.order.size == "1.5"
    assert mod_result.order.price == "51000.0"
    
    # Check modification history
    mods = await order_executor.get_order_modifications(original_order_id)
    assert len(mods) == 1
    assert mods[0]["original_order_id"] == original_order_id
    assert mods[0]["new_order_id"] == "test_order_2"
    assert mods[0]["changes"]["size"] == 1.5
    assert mods[0]["changes"]["price"] == 51000.0

@pytest.mark.asyncio
async def test_order_history_tracking(order_executor, mock_coinbase_client):
    """Test order history tracking and filtering."""
    # Setup multiple orders with different statuses
    orders_data = [
        {
            "order_id": f"test_order_{i}",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "1.0",
            "price": "50000.0",
            "type": "LIMIT",
            "status": status
        }
        for i, status in enumerate(["FILLED", "CANCELLED", "EXPIRED", "FILLED"])
    ]
    
    # Create orders and update their states
    for order_data in orders_data:
        mock_coinbase_client.create_order.return_value = order_data
        result = await order_executor.execute_limit_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=1.0,
            price=50000.0
        )
        assert result.success
        await order_executor._update_order_state(
            order_data["order_id"],
            OrderStatus(order_data["status"])
        )
    
    # Test unfiltered history
    all_history = await order_executor.get_order_history()
    assert len(all_history) == 4
    
    # Test filtering by status
    filled_orders = await order_executor.get_order_history(status="FILLED")
    assert len(filled_orders) == 2
    assert all(o.status == OrderStatus.FILLED for o in filled_orders)
    
    # Test filtering by time window
    recent_orders = await order_executor.get_order_history(
        start_time=datetime.utcnow() - pd.Timedelta(minutes=1)
    )
    assert len(recent_orders) == 4

@pytest.mark.asyncio
async def test_order_analytics(order_executor, mock_coinbase_client):
    """Test order analytics calculation."""
    # Setup orders with various states and fill rates
    orders_data = [
        # Filled order with full fill
        {
            "order_id": "test_order_1",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "1.0",
            "filled_size": "1.0",
            "price": "50000.0",
            "type": "LIMIT",
            "status": "FILLED"
        },
        # Filled order with partial fill
        {
            "order_id": "test_order_2",
            "product_id": "BTC-USD",
            "side": "SELL",
            "size": "2.0",
            "filled_size": "1.5",
            "price": "51000.0",
            "type": "LIMIT",
            "status": "FILLED"
        },
        # Cancelled order
        {
            "order_id": "test_order_3",
            "product_id": "BTC-USD",
            "side": "BUY",
            "size": "1.0",
            "filled_size": "0.0",
            "price": "49000.0",
            "type": "LIMIT",
            "status": "CANCELLED"
        }
    ]
    
    # Create orders and update their states
    for order_data in orders_data:
        mock_coinbase_client.create_order.return_value = order_data
        result = await order_executor.execute_limit_order(
            product_id="BTC-USD",
            side=OrderSide[order_data["side"]],
            size=float(order_data["size"]),
            price=float(order_data["price"])
        )
        assert result.success
        
        # Update order state
        state = order_executor._order_states[order_data["order_id"]]
        state.filled_size = float(order_data["filled_size"])
        await order_executor._update_order_state(
            order_data["order_id"],
            OrderStatus(order_data["status"])
        )
    
    # Get analytics
    analytics = await order_executor.get_order_analytics(product_id="BTC-USD")
    
    # Verify analytics
    assert analytics["total_orders"] == 3
    assert analytics["success_rate"] == pytest.approx(2/3)  # 2 filled out of 3
    assert analytics["fill_rate"] == pytest.approx((1.0 + 0.75) / 2)  # Average of 100% and 75% fills
    assert analytics["modification_rate"] == 0.0  # No modifications
    assert analytics["status_distribution"] == {
        OrderStatus.FILLED: 2,
        OrderStatus.CANCELLED: 1
    }

@pytest.mark.asyncio
async def test_order_state_transitions(order_executor, mock_coinbase_client):
    """Test order state transition tracking."""
    # Setup order that goes through multiple states
    initial_order = {
        "order_id": "test_order_1",
        "product_id": "BTC-USD",
        "side": "BUY",
        "size": "1.0",
        "price": "50000.0",
        "type": "LIMIT",
        "status": "PENDING"
    }
    
    mock_coinbase_client.create_order.return_value = initial_order
    
    # Place order
    result = await order_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=1.0,
        price=50000.0
    )
    assert result.success
    
    # Simulate state transitions
    transitions = [
        OrderStatus.OPEN,
        OrderStatus.PARTIALLY_FILLED,
        OrderStatus.FILLED
    ]
    
    for new_status in transitions:
        await order_executor._update_order_state("test_order_1", new_status)
        
    # Get order history
    history = await order_executor.get_order_history(
        status=OrderStatus.FILLED
    )
    assert len(history) == 1
    
    order_history = history[0]
    assert len(order_history.state_transitions) == 3
    
    # Verify transition sequence
    assert order_history.state_transitions[0]["from_status"] == OrderStatus.PENDING
    assert order_history.state_transitions[0]["to_status"] == OrderStatus.OPEN
    
    assert order_history.state_transitions[1]["from_status"] == OrderStatus.OPEN
    assert order_history.state_transitions[1]["to_status"] == OrderStatus.PARTIALLY_FILLED
    
    assert order_history.state_transitions[2]["from_status"] == OrderStatus.PARTIALLY_FILLED
    assert order_history.state_transitions[2]["to_status"] == OrderStatus.FILLED