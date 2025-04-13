import pytest
import pandas as pd
from collections import deque
from typing import Dict, Any

# Add project root to sys.path to allow importing app modules
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from app.strategies.rsi_momentum import RSIMomentumStrategy

# --- Test Fixtures ---

@pytest.fixture
def strategy_config() -> Dict[str, Any]:
    """Provides a default configuration for the strategy tests."""
    return {
        "rsi_period": 5, # Use a shorter period for easier testing
        "oversold_threshold": 30,
        "overbought_threshold": 70,
        "signal_threshold": 50,
        "trade_size": 0.1
    }

@pytest.fixture
def rsi_strategy(strategy_config: Dict[str, Any]) -> RSIMomentumStrategy:
    """Provides an instance of the RSIMomentumStrategy."""
    return RSIMomentumStrategy(product_id="TEST-USD", config=strategy_config)

# --- Test Cases ---

def test_strategy_initialization(rsi_strategy: RSIMomentumStrategy, strategy_config: Dict[str, Any]):
    """Test if the strategy initializes with correct parameters."""
    assert rsi_strategy.product_id == "TEST-USD"
    assert rsi_strategy.rsi_period == strategy_config["rsi_period"]
    assert rsi_strategy.oversold_threshold == strategy_config["oversold_threshold"]
    assert rsi_strategy.overbought_threshold == strategy_config["overbought_threshold"]
    assert rsi_strategy.signal_threshold == strategy_config["signal_threshold"]
    assert rsi_strategy.trade_size == strategy_config["trade_size"]
    assert isinstance(rsi_strategy.price_history, deque)
    assert rsi_strategy.current_rsi is None
    assert not rsi_strategy.in_position

def test_rsi_calculation_insufficient_data(rsi_strategy: RSIMomentumStrategy):
    """Test RSI calculation when there is not enough price history."""
    prices = [100, 101, 102] # Less than rsi_period (5)
    for price in prices:
        rsi_strategy.price_history.append(price)
    assert rsi_strategy._calculate_rsi() is None

def test_rsi_calculation_sufficient_data(rsi_strategy: RSIMomentumStrategy):
    """Test RSI calculation with a known sequence of prices."""
    # Prices designed to give a roughly known RSI (e.g., trending up strongly)
    prices = [100, 101, 102, 103, 104, 105, 106] # More than rsi_period (5)
    for price in prices:
        rsi_strategy.price_history.append(price)
        
    rsi_value = rsi_strategy._calculate_rsi()
    assert rsi_value is not None
    assert isinstance(rsi_value, float)
    # For a strong uptrend like this, RSI should be high (likely > 70, often near 100)
    assert rsi_value > 70 

def test_buy_signal_oversold_cross(rsi_strategy: RSIMomentumStrategy):
    """Test generating a BUY signal when RSI crosses above oversold threshold."""
    # Simulate prices leading to RSI dropping below 30, then crossing back up
    prices = [50, 48, 46, 45, 44, 43, 45] # Period=5. Last 5: 46,45,44,43,45 -> RSI should cross 30
    signal = None
    for price in prices:
        signal = rsi_strategy.process_market_data({'type': 'ticker', 'product_id': 'TEST-USD', 'price': str(price)})
    
    assert signal is not None
    assert signal['action'] == 'BUY'
    assert signal['type'] == 'MARKET'
    assert signal['size'] == rsi_strategy.trade_size
    assert signal['product_id'] == rsi_strategy.product_id
    # State should NOT change here, only on fill confirmation
    assert not rsi_strategy.in_position 

def test_sell_signal_overbought_cross(rsi_strategy: RSIMomentumStrategy):
    """Test generating a SELL signal when RSI crosses below overbought threshold while in position."""
    # Assume we are already in position
    rsi_strategy.in_position = True 
    
    # Simulate prices leading to RSI rising above 70, then crossing back down
    prices = [100, 102, 104, 105, 106, 107, 105] # Period=5. Last 5: 104,105,106,107,105 -> RSI should cross below 70
    signal = None
    for price in prices:
        signal = rsi_strategy.process_market_data({'type': 'ticker', 'product_id': 'TEST-USD', 'price': str(price)})
    
    assert signal is not None
    assert signal['action'] == 'SELL'
    assert signal['type'] == 'MARKET'
    assert signal['size'] == rsi_strategy.trade_size
    assert signal['product_id'] == rsi_strategy.product_id
    # State should NOT change here
    assert rsi_strategy.in_position 

def test_no_signal_when_already_in_position(rsi_strategy: RSIMomentumStrategy):
    """Test that no BUY signal is generated if already in position, even if RSI crosses up."""
    # Assume we are already in position
    rsi_strategy.in_position = True 
    
    # Simulate prices leading to RSI crossing above oversold (should not trigger BUY)
    prices = [50, 48, 46, 45, 44, 43, 45] 
    signal = None
    for price in prices:
        signal = rsi_strategy.process_market_data({'type': 'ticker', 'product_id': 'TEST-USD', 'price': str(price)})
        
    assert signal is None # No BUY signal should be generated
    assert rsi_strategy.in_position # Should remain in position

def test_no_signal_when_not_in_position(rsi_strategy: RSIMomentumStrategy):
    """Test that no SELL signal is generated if not in position, even if RSI crosses down."""
    # Assume we are not in position (default)
    assert not rsi_strategy.in_position
    
    # Simulate prices leading to RSI crossing below overbought (should not trigger SELL)
    prices = [100, 102, 104, 105, 106, 107, 105] 
    signal = None
    for price in prices:
        signal = rsi_strategy.process_market_data({'type': 'ticker', 'product_id': 'TEST-USD', 'price': str(price)})
        
    assert signal is None # No SELL signal should be generated
    assert not rsi_strategy.in_position # Should remain out of position

def test_state_update_on_buy_fill(rsi_strategy: RSIMomentumStrategy):
    """Test that `in_position` becomes True after a BUY order fill message."""
    assert not rsi_strategy.in_position # Start not in position
    fill_message = {
        'type': 'user_order_update',
        'order_id': 'buy-order-123',
        'client_order_id': 'client-buy-abc',
        'product_id': 'TEST-USD', # Match strategy product ID
        'side': 'BUY',
        'status': 'FILLED',
        'cumulative_quantity': '0.1',
        'time': '...'
    }
    signal = rsi_strategy.process_market_data(fill_message)
    assert signal is None # Fill messages don't generate signals
    assert rsi_strategy.in_position # State should now be True

def test_state_update_on_sell_fill(rsi_strategy: RSIMomentumStrategy):
    """Test that `in_position` becomes False after a SELL order fill message."""
    rsi_strategy.in_position = True # Start in position
    fill_message = {
        'type': 'user_order_update',
        'order_id': 'sell-order-456',
        'client_order_id': 'client-sell-def',
        'product_id': 'TEST-USD', # Match strategy product ID
        'side': 'SELL',
        'status': 'FILLED',
        'cumulative_quantity': '0.1',
        'time': '...'
    }
    signal = rsi_strategy.process_market_data(fill_message)
    assert signal is None # Fill messages don't generate signals
    assert not rsi_strategy.in_position # State should now be False

def test_state_no_change_on_other_product_fill(rsi_strategy: RSIMomentumStrategy):
    """Test that state doesn't change on fill messages for other products."""
    assert not rsi_strategy.in_position # Start not in position
    fill_message = {
        'type': 'user_order_update',
        'order_id': 'other-order-789',
        'product_id': 'OTHER-COIN', # Different product ID
        'side': 'BUY',
        'status': 'FILLED',
        'time': '...'
    }
    signal = rsi_strategy.process_market_data(fill_message)
    assert signal is None
    assert not rsi_strategy.in_position # State should remain False 