#!/usr/bin/env python3
"""
Test file for CustomPortfolio class.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import vectorbtpro as vbt

from scripts.portfolio import CustomPortfolio

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_stop_loss():
    """Test that stop-loss orders are executed correctly."""
    logger.info("Testing stop-loss...")
    
    # Create a simple price series
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    prices = pd.Series([100, 101, 102, 103, 104, 103, 102, 101, 100, 99], index=dates)
    
    # Create entry and exit signals
    entries = pd.Series(False, index=dates)
    entries.iloc[0] = True  # Enter on first day
    
    exits = pd.Series(False, index=dates)
    
    # Create portfolio with 2% stop-loss
    portfolio = CustomPortfolio.from_signals(
        close=prices,
        entries=entries,
        exits=exits,
        stop_loss=0.02,  # 2% stop-loss
        freq='1D',
        size=1.0,
        fees=0.001,
        slippage=0.001
    )
    
    # Get trades
    trades = portfolio.trades
    
    # Check if the stop-loss was triggered on day 7 (when price drops to 101, a 2.88% drop from 104)
    assert len(trades) > 0, "No trades were executed"
    assert trades['exit_idx'][0] == 6, f"Stop-loss not triggered at correct date. Exit idx: {trades['exit_idx'][0]}"
    
    # Check exit type
    exit_types = portfolio.get_exit_types()
    assert exit_types[0] == 'stop_loss', f"Exit type not identified as stop-loss: {exit_types[0]}"
    
    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    prices.plot(ax=ax, label='Price')
    
    # Plot entry and exit points
    entry_price = prices.iloc[trades['entry_idx'][0]]
    exit_price = prices.iloc[trades['exit_idx'][0]]
    
    ax.plot(dates[trades['entry_idx'][0]], entry_price, '^', markersize=10, color='green', label='Entry')
    ax.plot(dates[trades['exit_idx'][0]], exit_price, 'v', markersize=10, color='red', label='Stop-Loss Exit')
    
    # Plot stop-loss level
    stop_level = entry_price * (1 - 0.02)
    ax.axhline(y=stop_level, color='red', linestyle='--', label='Stop-Loss Level')
    
    ax.set_title('Stop-Loss Test')
    ax.legend()
    
    plt.savefig('stop_loss_test.png')
    logger.info("Stop-loss test passed!")
    
def test_take_profit():
    """Test that take-profit orders are executed correctly."""
    logger.info("Testing take-profit...")
    
    # Create a simple price series
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    prices = pd.Series([100, 101, 102, 103, 104, 105, 106, 105, 104, 103], index=dates)
    
    # Create entry and exit signals
    entries = pd.Series(False, index=dates)
    entries.iloc[0] = True  # Enter on first day
    
    exits = pd.Series(False, index=dates)
    
    # Create portfolio with 5% take-profit
    portfolio = CustomPortfolio.from_signals(
        close=prices,
        entries=entries,
        exits=exits,
        take_profit=0.05,  # 5% take-profit
        freq='1D',
        size=1.0,
        fees=0.001,
        slippage=0.001
    )
    
    # Get trades
    trades = portfolio.trades
    
    # Check if the take-profit was triggered on day 6 (when price rises to 105, a 5% rise from 100)
    assert len(trades) > 0, "No trades were executed"
    assert trades['exit_idx'][0] == 5, f"Take-profit not triggered at correct date. Exit idx: {trades['exit_idx'][0]}"
    
    # Check exit type
    exit_types = portfolio.get_exit_types()
    assert exit_types[0] == 'take_profit', f"Exit type not identified as take-profit: {exit_types[0]}"
    
    # Visualize
    fig, ax = plt.subplots(figsize=(10, 6))
    prices.plot(ax=ax, label='Price')
    
    # Plot entry and exit points
    entry_price = prices.iloc[trades['entry_idx'][0]]
    exit_price = prices.iloc[trades['exit_idx'][0]]
    
    ax.plot(dates[trades['entry_idx'][0]], entry_price, '^', markersize=10, color='green', label='Entry')
    ax.plot(dates[trades['exit_idx'][0]], exit_price, 'v', markersize=10, color='blue', label='Take-Profit Exit')
    
    # Plot take-profit level
    tp_level = entry_price * (1 + 0.05)
    ax.axhline(y=tp_level, color='blue', linestyle='--', label='Take-Profit Level')
    
    ax.set_title('Take-Profit Test')
    ax.legend()
    
    plt.savefig('take_profit_test.png')
    logger.info("Take-profit test passed!")

def test_both_sl_tp():
    """Test both stop-loss and take-profit together."""
    logger.info("Testing both stop-loss and take-profit...")
    
    # Create price scenarios
    # Scenario 1: Price rises then falls (take-profit should trigger)
    dates1 = pd.date_range('2023-01-01', periods=10, freq='D')
    prices1 = pd.Series([100, 102, 104, 105, 103, 102, 101, 100, 99, 98], index=dates1)
    
    # Scenario 2: Price falls then rises (stop-loss should trigger)
    dates2 = pd.date_range('2023-02-01', periods=10, freq='D')
    prices2 = pd.Series([100, 99, 97, 96, 98, 99, 101, 102, 103, 104], index=dates2)
    
    # Combine scenarios
    all_dates = dates1.append(dates2)
    all_prices = pd.Series(
        list(prices1.values) + list(prices2.values), 
        index=all_dates
    )
    
    # Create entry signals for both scenarios
    entries = pd.Series(False, index=all_dates)
    entries.iloc[0] = True  # Enter at start of scenario 1
    entries.iloc[10] = True  # Enter at start of scenario 2
    
    exits = pd.Series(False, index=all_dates)
    
    # Create portfolio with both SL and TP
    portfolio = CustomPortfolio.from_signals(
        close=all_prices,
        entries=entries,
        exits=exits,
        stop_loss=0.03,     # 3% stop-loss
        take_profit=0.04,   # 4% take-profit
        freq='1D',
        size=1.0,
        fees=0.001,
        slippage=0.001
    )
    
    # Get trades and exit types
    trades = portfolio.trades
    exit_types = portfolio.get_exit_types()
    
    # Check if we have 2 trades
    assert len(trades) == 2, f"Expected 2 trades, got {len(trades)}"
    
    # Check if the first trade was a take-profit exit
    assert exit_types[0] == 'take_profit', f"First exit should be take-profit, got {exit_types[0]}"
    
    # Check if the second trade was a stop-loss exit
    assert exit_types[1] == 'stop_loss', f"Second exit should be stop-loss, got {exit_types[1]}"
    
    # Get exit statistics
    exit_stats = portfolio.get_exit_stats()
    logger.info(f"Exit statistics: {exit_stats}")
    
    # Visualize
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Scenario 1
    prices1.plot(ax=ax1, label='Scenario 1 Prices')
    entry_price1 = prices1.iloc[0]
    exit_price1 = prices1.iloc[trades['exit_idx'][0] % 10]  # Modulo to get index within scenario 1
    
    ax1.plot(dates1[0], entry_price1, '^', markersize=10, color='green', label='Entry')
    ax1.plot(dates1[trades['exit_idx'][0] % 10], exit_price1, 'v', markersize=10, color='blue', label='Take-Profit Exit')
    
    ax1.axhline(y=entry_price1 * (1 + 0.04), color='blue', linestyle='--', label='Take-Profit Level')
    ax1.axhline(y=entry_price1 * (1 - 0.03), color='red', linestyle='--', label='Stop-Loss Level')
    
    ax1.set_title('Scenario 1: Price rises then falls (Take-Profit)')
    ax1.legend()
    
    # Scenario 2
    prices2.plot(ax=ax2, label='Scenario 2 Prices')
    entry_price2 = prices2.iloc[0]
    exit_price2 = prices2.iloc[trades['exit_idx'][1] % 10]  # Modulo to get index within scenario 2
    
    ax2.plot(dates2[0], entry_price2, '^', markersize=10, color='green', label='Entry')
    ax2.plot(dates2[trades['exit_idx'][1] % 10], exit_price2, 'v', markersize=10, color='red', label='Stop-Loss Exit')
    
    ax2.axhline(y=entry_price2 * (1 + 0.04), color='blue', linestyle='--', label='Take-Profit Level')
    ax2.axhline(y=entry_price2 * (1 - 0.03), color='red', linestyle='--', label='Stop-Loss Level')
    
    ax2.set_title('Scenario 2: Price falls then rises (Stop-Loss)')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('sl_tp_test.png')
    logger.info("Combined stop-loss and take-profit test passed!")

def main():
    """Run all tests."""
    logger.info("Starting CustomPortfolio tests...")
    
    try:
        test_stop_loss()
        test_take_profit()
        test_both_sl_tp()
        logger.info("All tests passed successfully!")
    except AssertionError as e:
        logger.error(f"Test failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main() 