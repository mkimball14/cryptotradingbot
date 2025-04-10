import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from app.core.performance_metrics import PerformanceMetrics

@pytest.fixture
def sample_trade_history():
    """Create a sample trade history for testing."""
    base_time = datetime(2023, 1, 1)
    trades = []
    
    # Create a series of profitable trades
    initial_portfolio = 10000.0
    current_portfolio = initial_portfolio
    
    # Trade 1: Profitable
    trades.extend([
        {
            'timestamp': base_time,
            'price': 50000.0,
            'size': 0.1,
            'side': 'buy',
            'fee': 2.5,
            'portfolio_value': current_portfolio
        },
        {
            'timestamp': base_time + timedelta(hours=1),
            'price': 51000.0,
            'size': 0.1,
            'side': 'sell',
            'fee': 2.5,
            'portfolio_value': current_portfolio + (51000.0 - 50000.0) * 0.1 - 5.0
        }
    ])
    current_portfolio = trades[-1]['portfolio_value']
    
    # Trade 2: Loss
    trades.extend([
        {
            'timestamp': base_time + timedelta(hours=2),
            'price': 51000.0,
            'size': 0.1,
            'side': 'buy',
            'fee': 2.5,
            'portfolio_value': current_portfolio
        },
        {
            'timestamp': base_time + timedelta(hours=3),
            'price': 50000.0,
            'size': 0.1,
            'side': 'sell',
            'fee': 2.5,
            'portfolio_value': current_portfolio + (50000.0 - 51000.0) * 0.1 - 5.0
        }
    ])
    current_portfolio = trades[-1]['portfolio_value']
    
    # Trade 3: Profitable
    trades.extend([
        {
            'timestamp': base_time + timedelta(hours=4),
            'price': 50000.0,
            'size': 0.1,
            'side': 'buy',
            'fee': 2.5,
            'portfolio_value': current_portfolio
        },
        {
            'timestamp': base_time + timedelta(hours=5),
            'price': 52000.0,
            'size': 0.1,
            'side': 'sell',
            'fee': 2.5,
            'portfolio_value': current_portfolio + (52000.0 - 50000.0) * 0.1 - 5.0
        }
    ])
    
    return trades

def test_initialization(sample_trade_history):
    """Test PerformanceMetrics initialization."""
    metrics = PerformanceMetrics(sample_trade_history)
    assert len(metrics.trades_df) == len(sample_trade_history)
    assert all(col in metrics.trades_df.columns for col in ['timestamp', 'price', 'size', 'side', 'fee', 'portfolio_value'])

def test_empty_trade_history():
    """Test metrics calculation with empty trade history."""
    metrics = PerformanceMetrics([])
    all_metrics = metrics.get_all_metrics()
    
    assert all_metrics['total_return'] == 0.0
    assert all_metrics['annualized_return'] == 0.0
    assert all_metrics['sharpe_ratio'] == 0.0
    assert all_metrics['max_drawdown'] == 0.0
    assert all_metrics['win_rate'] == 0.0
    assert all_metrics['profit_factor'] == 0.0
    assert all_metrics['total_trades'] == 0
    assert all_metrics['total_volume'] == 0.0
    assert all_metrics['total_fees'] == 0.0

def test_returns_calculation(sample_trade_history):
    """Test calculation of returns."""
    metrics = PerformanceMetrics(sample_trade_history)
    returns = metrics.calculate_returns()
    
    assert len(returns) == len(sample_trade_history) - 1
    assert all(isinstance(r, float) for r in returns)

def test_total_return(sample_trade_history):
    """Test total return calculation."""
    metrics = PerformanceMetrics(sample_trade_history)
    total_return = metrics.calculate_total_return()
    
    initial_value = sample_trade_history[0]['portfolio_value']
    final_value = sample_trade_history[-1]['portfolio_value']
    expected_return = ((final_value - initial_value) / initial_value) * 100
    
    assert total_return == pytest.approx(expected_return)

def test_win_rate(sample_trade_history):
    """Test win rate calculation."""
    metrics = PerformanceMetrics(sample_trade_history)
    win_rate = metrics.calculate_win_rate()
    
    # In our sample data, we have 2 winning trades and 1 losing trade
    assert win_rate == pytest.approx(66.67, rel=1e-2)

def test_profit_factor(sample_trade_history):
    """Test profit factor calculation."""
    metrics = PerformanceMetrics(sample_trade_history)
    profit_factor = metrics.calculate_profit_factor()
    
    # Calculate expected profit factor manually
    total_profit = 0
    total_loss = 0
    current_position = None
    
    for trade in sample_trade_history:
        if trade['side'].lower() == 'buy':
            current_position = trade
        elif trade['side'].lower() == 'sell' and current_position is not None:
            profit = (trade['price'] - current_position['price']) * trade['size'] - \
                    (trade['fee'] + current_position['fee'])
            if profit > 0:
                total_profit += profit
            else:
                total_loss += abs(profit)
            current_position = None
    
    expected_profit_factor = total_profit / total_loss if total_loss != 0 else float('inf')
    assert profit_factor == pytest.approx(expected_profit_factor)

def test_max_drawdown(sample_trade_history):
    """Test maximum drawdown calculation."""
    metrics = PerformanceMetrics(sample_trade_history)
    max_dd = metrics.calculate_max_drawdown()
    
    # Calculate expected max drawdown manually
    portfolio_values = [trade['portfolio_value'] for trade in sample_trade_history]
    peak = portfolio_values[0]
    expected_max_dd = 0.0
    
    for value in portfolio_values[1:]:
        if value > peak:
            peak = value
        dd = (peak - value) / peak * 100
        expected_max_dd = max(expected_max_dd, dd)
    
    assert max_dd == pytest.approx(expected_max_dd)

def test_average_trade_metrics(sample_trade_history):
    """Test average trade metrics calculation."""
    metrics = PerformanceMetrics(sample_trade_history)
    trade_metrics = metrics.calculate_average_trade()
    
    assert 'average_profit' in trade_metrics
    assert 'average_win' in trade_metrics
    assert 'average_loss' in trade_metrics
    
    # Verify the values are reasonable based on our sample data
    assert trade_metrics['average_win'] > 0
    assert trade_metrics['average_loss'] < 0
    assert trade_metrics['average_profit'] > trade_metrics['average_loss']

def test_all_metrics(sample_trade_history):
    """Test the comprehensive metrics calculation."""
    metrics = PerformanceMetrics(sample_trade_history)
    all_metrics = metrics.get_all_metrics()
    
    required_metrics = [
        'total_return',
        'annualized_return',
        'sharpe_ratio',
        'max_drawdown',
        'win_rate',
        'profit_factor',
        'trade_metrics',
        'total_trades',
        'total_volume',
        'total_fees'
    ]
    
    assert all(metric in all_metrics for metric in required_metrics)
    assert all_metrics['total_trades'] == 3  # We have 3 complete trades in our sample
    assert all_metrics['total_fees'] == sum(trade['fee'] for trade in sample_trade_history)
    assert isinstance(all_metrics['trade_metrics'], dict) 