import pytest
import asyncio
from datetime import datetime
from decimal import Decimal

from app.core.dry_run_executor import DryRunExecutor
from app.core.models import OrderSide, OrderType, OrderStatus
from app.core.exceptions import OrderExecutionError

@pytest.fixture
def dry_run_executor():
    """Create a DryRunExecutor instance with test settings"""
    executor = DryRunExecutor(
        initial_balance={"BTC": 1.0, "USD": 50000.0},
        simulated_latency=0.01,  # Fast latency for tests
        fill_probability=1.0,     # Always fill orders in tests
        slippage_std=0.0         # No slippage in tests
    )
    # Set a default price for BTC-USD
    executor.set_simulated_price("BTC-USD", 50000.0)
    return executor

@pytest.mark.asyncio
async def test_market_buy_order(dry_run_executor):
    """Test market buy order execution"""
    # Initial balances
    initial_usd = dry_run_executor.get_simulated_balance("USD")
    initial_btc = dry_run_executor.get_simulated_balance("BTC")
    
    # Execute market buy
    result = await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1
    )
    
    assert result.success
    assert result.order is not None
    assert result.order.status == OrderStatus.FILLED.value
    assert float(result.order.size) == 0.1
    assert float(result.order.filled_size) == 0.1
    
    # Check balance updates
    assert dry_run_executor.get_simulated_balance("USD") == initial_usd - (0.1 * 50000.0)
    assert dry_run_executor.get_simulated_balance("BTC") == initial_btc + 0.1

@pytest.mark.asyncio
async def test_market_sell_order(dry_run_executor):
    """Test market sell order execution"""
    # Initial balances
    initial_usd = dry_run_executor.get_simulated_balance("USD")
    initial_btc = dry_run_executor.get_simulated_balance("BTC")
    
    # Execute market sell
    result = await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.SELL,
        size=0.1
    )
    
    assert result.success
    assert result.order is not None
    assert result.order.status == OrderStatus.FILLED.value
    assert float(result.order.size) == 0.1
    assert float(result.order.filled_size) == 0.1
    
    # Check balance updates
    assert dry_run_executor.get_simulated_balance("USD") == initial_usd + (0.1 * 50000.0)
    assert dry_run_executor.get_simulated_balance("BTC") == initial_btc - 0.1

@pytest.mark.asyncio
async def test_limit_buy_order(dry_run_executor):
    """Test limit buy order execution"""
    # Initial balances
    initial_usd = dry_run_executor.get_simulated_balance("USD")
    initial_btc = dry_run_executor.get_simulated_balance("BTC")
    
    # Execute limit buy
    result = await dry_run_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1,
        price=49000.0  # Below current price to ensure fill
    )
    
    assert result.success
    assert result.order is not None
    assert result.order.status == OrderStatus.OPEN.value
    assert float(result.order.size) == 0.1
    assert float(result.order.filled_size) == 0.0
    
    # Wait for fill simulation
    await asyncio.sleep(2)
    
    # Check order status
    order = await dry_run_executor.get_order_status(result.order.order_id)
    assert order is not None
    assert order.status == OrderStatus.FILLED.value
    assert float(order.filled_size) == 0.1
    
    # Check balance updates
    assert dry_run_executor.get_simulated_balance("USD") == initial_usd - (0.1 * 49000.0)
    assert dry_run_executor.get_simulated_balance("BTC") == initial_btc + 0.1

@pytest.mark.asyncio
async def test_limit_sell_order(dry_run_executor):
    """Test limit sell order execution"""
    # Initial balances
    initial_usd = dry_run_executor.get_simulated_balance("USD")
    initial_btc = dry_run_executor.get_simulated_balance("BTC")
    
    # Execute limit sell
    result = await dry_run_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.SELL,
        size=0.1,
        price=51000.0  # Above current price to ensure fill
    )
    
    assert result.success
    assert result.order is not None
    assert result.order.status == OrderStatus.OPEN.value
    assert float(result.order.size) == 0.1
    assert float(result.order.filled_size) == 0.0
    
    # Wait for fill simulation
    await asyncio.sleep(2)
    
    # Check order status
    order = await dry_run_executor.get_order_status(result.order.order_id)
    assert order is not None
    assert order.status == OrderStatus.FILLED.value
    assert float(order.filled_size) == 0.1
    
    # Check balance updates
    assert dry_run_executor.get_simulated_balance("USD") == initial_usd + (0.1 * 51000.0)
    assert dry_run_executor.get_simulated_balance("BTC") == initial_btc - 0.1

@pytest.mark.asyncio
async def test_insufficient_balance(dry_run_executor):
    """Test order rejection due to insufficient balance"""
    # Try to buy more than we can afford
    result = await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=100.0  # Much larger than our balance allows
    )
    
    assert not result.success
    assert "Insufficient USD balance" in result.error

@pytest.mark.asyncio
async def test_cancel_order(dry_run_executor):
    """Test order cancellation"""
    # Place a limit order
    order_result = await dry_run_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1,
        price=45000.0  # Well below market to avoid immediate fill
    )
    
    assert order_result.success
    
    # Cancel the order
    cancel_result = await dry_run_executor.cancel_order(order_result.order.order_id)
    assert cancel_result.success
    
    # Verify order status
    order = await dry_run_executor.get_order_status(order_result.order.order_id)
    assert order is not None
    assert order.status == OrderStatus.CANCELLED.value

@pytest.mark.asyncio
async def test_trading_halt(dry_run_executor):
    """Test trading halt functionality"""
    # Halt trading
    await dry_run_executor.halt_trading("Test halt")
    
    # Try to place an order
    result = await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1
    )
    
    assert not result.success
    assert "Trading is currently halted" in result.error
    
    # Resume trading
    await dry_run_executor.resume_trading("Test resume")
    
    # Try to place an order again
    result = await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1
    )
    
    assert result.success

@pytest.mark.asyncio
async def test_price_simulation(dry_run_executor):
    """Test price simulation functionality"""
    # Set a new price
    dry_run_executor.set_simulated_price("BTC-USD", 55000.0)
    
    # Execute a market order
    result = await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1
    )
    
    assert result.success
    assert float(result.order.price) == 55000.0
    
    # Check limit order behavior with new price
    limit_result = await dry_run_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1,
        price=54000.0
    )
    
    assert limit_result.success
    
    # Wait for potential fill
    await asyncio.sleep(2)
    
    # Order should not be filled as price is above limit
    order = await dry_run_executor.get_order_status(limit_result.order.order_id)
    assert order.status == OrderStatus.OPEN.value
    
    # Update price below limit
    dry_run_executor.set_simulated_price("BTC-USD", 53000.0)
    
    # Wait for fill
    await asyncio.sleep(2)
    
    # Order should now be filled
    order = await dry_run_executor.get_order_status(limit_result.order.order_id)
    assert order.status == OrderStatus.FILLED.value

@pytest.mark.asyncio
async def test_price_simulation_with_trend(dry_run_executor):
    """Test price simulation with trend bias"""
    # Set bullish trend
    executor = DryRunExecutor(
        initial_balance={"BTC": 1.0, "USD": 50000.0},
        simulated_latency=0.01,
        price_trend_bias=0.8,  # Strong bullish bias
        volatility_factor=0.5   # Reduced volatility for testing
    )
    
    # Set initial price
    initial_price = 50000.0
    executor.set_simulated_price("BTC-USD", initial_price)
    
    # Run price updates
    for _ in range(100):  # Simulate 100 price updates
        await executor._simulate_price_update("BTC-USD")
    
    # Check that price has generally increased
    final_price = executor._simulated_prices["BTC-USD"]
    assert final_price > initial_price

@pytest.mark.asyncio
async def test_price_simulation_with_volatility(dry_run_executor):
    """Test price simulation with different volatility levels"""
    # Set high volatility
    executor = DryRunExecutor(
        initial_balance={"BTC": 1.0, "USD": 50000.0},
        simulated_latency=0.01,
        price_trend_bias=0.0,     # No trend bias
        volatility_factor=2.0      # High volatility
    )
    
    # Set initial price
    initial_price = 50000.0
    executor.set_simulated_price("BTC-USD", initial_price)
    
    price_changes = []
    
    # Run price updates and collect changes
    for _ in range(100):
        old_price = executor._simulated_prices["BTC-USD"]
        await executor._simulate_price_update("BTC-USD")
        new_price = executor._simulated_prices["BTC-USD"]
        price_changes.append(abs((new_price - old_price) / old_price))
    
    # Calculate average price change
    avg_change = sum(price_changes) / len(price_changes)
    assert avg_change > 0.0001  # Verify significant price movement

@pytest.mark.asyncio
async def test_trade_logging(dry_run_executor):
    """Test trade logging functionality"""
    # Execute a series of trades
    await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1
    )
    
    await dry_run_executor.execute_limit_order(
        product_id="BTC-USD",
        side=OrderSide.SELL,
        size=0.1,
        price=55000.0
    )
    
    # Get trade history
    trade_history = dry_run_executor.get_trade_history()
    assert len(trade_history) >= 2
    
    # Verify trade log entries
    for trade in trade_history:
        assert 'timestamp' in trade
        assert 'order_id' in trade
        assert 'product_id' in trade
        assert 'side' in trade
        assert 'type' in trade
        assert 'size' in trade
        assert 'success' in trade
        assert trade['simulated'] is True

@pytest.mark.asyncio
async def test_simulation_statistics(dry_run_executor):
    """Test simulation statistics tracking"""
    # Execute some trades
    await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1
    )
    
    # Try to execute an invalid trade
    await dry_run_executor.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=100.0  # Too large, should fail
    )
    
    # Get simulation stats
    stats = dry_run_executor.get_simulation_stats()
    
    assert stats['total_trades'] == 2
    assert stats['successful_trades'] == 1
    assert stats['failed_trades'] == 1
    assert stats['success_rate'] == 50.0
    assert stats['total_volume'] > 0
    assert stats['total_fees'] > 0
    assert 'duration' in stats
    assert stats['price_updates'] >= 0 