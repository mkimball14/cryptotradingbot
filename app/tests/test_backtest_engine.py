import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from app.core.backtest_engine import BacktestEngine
from app.core.models import OrderSide, OrderType, OrderStatus
from app.core.exceptions import OrderExecutionError

@pytest.fixture
def sample_historical_data():
    """Create sample historical price data for testing"""
    dates = pd.date_range(start='2023-01-01', end='2023-01-31', freq='1H')
    data = pd.DataFrame({
        'timestamp': dates,
        'open': np.random.normal(50000, 1000, len(dates)),
        'high': np.random.normal(51000, 1000, len(dates)),
        'low': np.random.normal(49000, 1000, len(dates)),
        'close': np.random.normal(50000, 1000, len(dates)),
        'volume': np.random.normal(10, 2, len(dates))
    })
    # Ensure high is highest and low is lowest
    data['high'] = data[['open', 'high', 'low', 'close']].max(axis=1)
    data['low'] = data[['open', 'high', 'low', 'close']].min(axis=1)
    return data

@pytest.fixture
def backtest_engine(sample_historical_data):
    """Create a BacktestEngine instance with test settings"""
    return BacktestEngine(
        historical_data=sample_historical_data,
        initial_balance={"BTC": 1.0, "USD": 50000.0},
        trading_fee=0.001,
        slippage_std=0.001
    )

@pytest.mark.asyncio
async def test_market_buy_order(backtest_engine):
    """Test market buy order execution in backtest"""
    initial_usd = backtest_engine._balances["USD"]
    initial_btc = backtest_engine._balances["BTC"]
    
    result = await backtest_engine.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.1
    )
    
    assert result.success
    assert result.order is not None
    assert result.order.status == OrderStatus.FILLED.value
    assert float(result.order.size) == 0.1
    assert float(result.order.filled_size) == 0.1
    
    # Verify balance updates
    execution_price = float(result.order.price)
    fee = execution_price * 0.1 * 0.001  # 0.1% fee
    assert backtest_engine._balances["USD"] == pytest.approx(initial_usd - (0.1 * execution_price) - fee, rel=1e-10)
    assert backtest_engine._balances["BTC"] == pytest.approx(initial_btc + 0.1, rel=1e-10)

@pytest.mark.asyncio
async def test_market_sell_order(backtest_engine):
    """Test market sell order execution in backtest"""
    initial_usd = backtest_engine._balances["USD"]
    initial_btc = backtest_engine._balances["BTC"]
    
    result = await backtest_engine.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.SELL,
        size=0.1
    )
    
    assert result.success
    assert result.order is not None
    assert result.order.status == OrderStatus.FILLED.value
    assert float(result.order.size) == 0.1
    assert float(result.order.filled_size) == 0.1
    
    # Verify balance updates
    execution_price = float(result.order.price)
    fee = execution_price * 0.1 * 0.001  # 0.1% fee
    assert backtest_engine._balances["USD"] == pytest.approx(initial_usd + (0.1 * execution_price) - fee, rel=1e-10)
    assert backtest_engine._balances["BTC"] == pytest.approx(initial_btc - 0.1, rel=1e-10)

@pytest.mark.asyncio
async def test_insufficient_balance(backtest_engine):
    """Test order rejection due to insufficient balance"""
    result = await backtest_engine.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=100.0  # Much larger than our balance allows
    )
    
    assert not result.success
    assert "Insufficient USD balance" in result.error

def test_performance_metrics(backtest_engine):
    """Test calculation of performance metrics"""
    # Execute a series of trades
    async def execute_trades():
        # Buy low, sell high pattern
        for _ in range(5):
            await backtest_engine.execute_market_order(
                product_id="BTC-USD",
                side=OrderSide.BUY,
                size=0.1
            )
            backtest_engine.step()  # Move to next timeframe
            await backtest_engine.execute_market_order(
                product_id="BTC-USD",
                side=OrderSide.SELL,
                size=0.1
            )
            backtest_engine.step()  # Move to next timeframe
            
    # Run trades
    import asyncio
    asyncio.run(execute_trades())
    
    # Get metrics
    metrics = backtest_engine.get_performance_metrics()
    
    # Verify metrics structure
    assert 'total_return' in metrics
    assert 'annualized_return' in metrics
    assert 'sharpe_ratio' in metrics
    assert 'max_drawdown' in metrics
    assert 'win_rate' in metrics
    assert 'total_trades' in metrics
    assert 'total_volume' in metrics
    assert 'total_fees' in metrics
    
    # Verify basic metric properties
    assert metrics['total_trades'] == 10  # 5 buys + 5 sells
    assert metrics['win_rate'] == pytest.approx(1.0)  # All trades should succeed
    assert metrics['total_fees'] > 0
    assert isinstance(metrics['total_return'], float)

def test_trade_history(backtest_engine):
    """Test trade history logging"""
    async def execute_sample_trades():
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=0.1
        )
        backtest_engine.step()
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.SELL,
            size=0.1
        )
        
    # Run trades
    import asyncio
    asyncio.run(execute_sample_trades())
    
    # Get trade history
    history = backtest_engine.get_trade_history()
    
    assert len(history) == 2  # Should have 2 trades
    
    # Verify trade log structure
    for trade in history:
        assert 'timestamp' in trade
        assert 'order_id' in trade
        assert 'product_id' in trade
        assert 'side' in trade
        assert 'type' in trade
        assert 'size' in trade
        assert 'price' in trade
        assert 'fee' in trade
        assert 'success' in trade
        assert 'portfolio_value' in trade

def test_reset_functionality(backtest_engine):
    """Test resetting the backtest engine"""
    initial_balance = backtest_engine._balances.copy()
    initial_portfolio_value = backtest_engine._calculate_portfolio_value()
    
    async def execute_trades():
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=0.1
        )
        
    # Run some trades
    import asyncio
    asyncio.run(execute_trades())
    
    # Verify state has changed
    assert backtest_engine._balances != initial_balance
    assert len(backtest_engine._trade_log) > 0
    
    # Reset
    backtest_engine.reset()
    
    # Verify state has been reset
    assert backtest_engine.current_index == 0
    assert backtest_engine._balances == initial_balance
    assert len(backtest_engine._trade_log) == 0
    assert len(backtest_engine._portfolio_values) == 0
    assert backtest_engine._calculate_portfolio_value() == initial_portfolio_value

def test_slippage_simulation(backtest_engine):
    """Test price slippage simulation"""
    base_price = 50000.0
    slippage_samples = [backtest_engine._simulate_slippage(base_price) for _ in range(1000)]
    
    # Calculate statistics
    mean_price = np.mean(slippage_samples)
    std_price = np.std(slippage_samples) / base_price
    
    # Verify slippage properties
    assert mean_price == pytest.approx(base_price, rel=0.01)  # Mean should be close to base price
    assert std_price == pytest.approx(backtest_engine.slippage_std, rel=0.1)  # Standard deviation should match configured value 

def test_historical_data_validation():
    """Test validation of historical data format"""
    # Test missing required columns
    invalid_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', end='2023-01-31', freq='1H'),
        'close': np.random.normal(50000, 1000, 721)  # Missing other required columns
    })
    
    with pytest.raises(ValueError) as exc_info:
        BacktestEngine(historical_data=invalid_data)
    assert "Missing required columns" in str(exc_info.value)

def test_stepping_behavior(backtest_engine):
    """Test stepping through historical data"""
    initial_index = backtest_engine.current_index
    
    # Test successful step
    assert backtest_engine.step() == True
    assert backtest_engine.current_index == initial_index + 1
    
    # Step to end of data
    while backtest_engine.step():
        pass
    
    # Test step at end of data
    assert backtest_engine.step() == False
    assert backtest_engine.current_index == len(backtest_engine.data) - 1

@pytest.mark.asyncio
async def test_zero_size_order(backtest_engine):
    """Test rejection of zero-size orders"""
    result = await backtest_engine.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=0.0
    )
    
    assert not result.success
    assert "Invalid order size" in result.error

@pytest.mark.asyncio
async def test_invalid_order_side(backtest_engine):
    """Test rejection of invalid order side"""
    result = await backtest_engine.execute_market_order(
        product_id="BTC-USD",
        side="INVALID",
        size=0.1
    )
    
    assert not result.success
    assert "Invalid order side" in result.error

def test_portfolio_value_tracking(backtest_engine):
    """Test portfolio value tracking over time"""
    initial_value = backtest_engine._calculate_portfolio_value()
    
    async def execute_trades():
        # Execute a series of trades and steps
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=0.1
        )
        backtest_engine.step()
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.SELL,
            size=0.1
        )
        backtest_engine.step()
    
    # Run trades
    import asyncio
    asyncio.run(execute_trades())
    
    # Verify portfolio value history
    portfolio_values = backtest_engine._portfolio_values
    assert len(portfolio_values) > 0
    assert isinstance(portfolio_values[0]['value'], float)
    assert isinstance(portfolio_values[0]['timestamp'], pd.Timestamp)
    
    # Verify each trade created a portfolio value entry
    assert len(portfolio_values) >= 2  # Should have at least 2 entries for 2 trades

def test_metrics_with_no_trades(backtest_engine):
    """Test performance metrics calculation with no trades"""
    metrics = backtest_engine.get_performance_metrics()
    assert metrics == {}  # Should return empty dict when no trades executed

def test_metrics_calculation_precision(backtest_engine):
    """Test precision of metrics calculations"""
    async def execute_trade():
        # Execute a single trade with known parameters
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=0.1
        )
    
    # Run trade
    import asyncio
    asyncio.run(execute_trade())
    
    metrics = backtest_engine.get_performance_metrics()
    
    # Verify metric precision
    assert isinstance(metrics['total_return'], float)
    assert isinstance(metrics['total_volume'], float)
    assert isinstance(metrics['total_fees'], float)
    assert metrics['total_fees'] == pytest.approx(
        float(backtest_engine._trade_log[0]['price']) * 0.1 * backtest_engine.trading_fee,
        rel=1e-10
    ) 

@pytest.mark.asyncio
async def test_negative_size_order(backtest_engine):
    """Test rejection of negative size orders"""
    result = await backtest_engine.execute_market_order(
        product_id="BTC-USD",
        side=OrderSide.BUY,
        size=-0.1
    )
    
    assert not result.success
    assert "Invalid order size" in result.error

@pytest.mark.asyncio
async def test_invalid_product_id(backtest_engine):
    """Test rejection of invalid product ID"""
    result = await backtest_engine.execute_market_order(
        product_id="INVALID-PAIR",
        side=OrderSide.BUY,
        size=0.1
    )
    
    assert not result.success
    assert "Invalid product ID" in result.error

def test_drawdown_calculation(backtest_engine):
    """Test maximum drawdown calculation with controlled price movement"""
    # Create a sequence of trades that should produce a known drawdown
    async def execute_drawdown_scenario():
        # Initial buy to establish position
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.BUY,
            size=0.5
        )
        
        # Step through multiple periods to simulate price movement
        for _ in range(5):
            backtest_engine.step()
        
        # Sell at a lower price
        await backtest_engine.execute_market_order(
            product_id="BTC-USD",
            side=OrderSide.SELL,
            size=0.5
        )
    
    # Run scenario
    import asyncio
    asyncio.run(execute_drawdown_scenario())
    
    # Get metrics
    metrics = backtest_engine.get_performance_metrics()
    
    # Verify drawdown calculation
    assert 'max_drawdown' in metrics
    assert isinstance(metrics['max_drawdown'], float)
    assert metrics['max_drawdown'] <= 0  # Drawdown should be negative or zero
    assert metrics['max_drawdown'] >= -1  # Drawdown should not exceed -100%

def test_initial_balance_validation():
    """Test validation of initial balance configuration"""
    # Test missing required currency
    with pytest.raises(ValueError) as exc_info:
        BacktestEngine(
            historical_data=sample_historical_data(),
            initial_balance={"BTC": 1.0},  # Missing USD
            trading_fee=0.001
        )
    assert "Missing required currency" in str(exc_info.value)
    
    # Test negative balance
    with pytest.raises(ValueError) as exc_info:
        BacktestEngine(
            historical_data=sample_historical_data(),
            initial_balance={"BTC": -1.0, "USD": 50000.0},
            trading_fee=0.001
        )
    assert "Invalid initial balance" in str(exc_info.value) 