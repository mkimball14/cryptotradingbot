#!/usr/bin/env python3
"""
Test script for CustomPortfolio class compatibility with latest vectorbtpro version.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import logging
import vectorbtpro as vbt

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from scripts.portfolio.custom_portfolio import CustomPortfolio

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_test_data(length=100, seed=42):
    """Generate synthetic price and signal data for testing."""
    np.random.seed(seed)
    
    # Create date range
    dates = pd.date_range('2023-01-01', periods=length, freq='D')
    
    # Generate price data with some trend and volatility
    base_price = 100
    trend = np.linspace(0, 20, length)
    noise = np.random.normal(0, 3, length)
    prices = base_price + trend + noise.cumsum()
    
    # Create DataFrame
    df = pd.DataFrame({
        'open': prices * 0.99,
        'high': prices * 1.02,
        'low': prices * 0.98,
        'close': prices,
        'volume': np.random.randint(1000, 10000, length)
    }, index=dates)
    
    # Generate entry and exit signals
    rng = np.random.default_rng(seed)
    entries = pd.Series(False, index=dates)
    exits = pd.Series(False, index=dates)
    
    # Create entry signals with ~10% probability
    entries = pd.Series(rng.random(length) > 0.9, index=dates)
    
    # Create exit signals ~5 periods after entries
    for i in range(length):
        if entries.iloc[i] and i + 5 < length:
            exits.iloc[i + 5] = True
    
    return df, entries, exits

def test_custom_portfolio():
    """Test CustomPortfolio class with different parameter combinations."""
    # Print vectorbtpro version
    logger.info(f"Testing with vectorbtpro version: {vbt.__version__}")
    
    # Generate test data
    df, entries, exits = generate_test_data(length=100)
    logger.info(f"Generated {len(df)} periods of test data with {sum(entries)} entries and {sum(exits)} exits")
    
    # Test parameters
    test_cases = [
        {"name": "Basic (no SL/TP)", "stop_loss": None, "take_profit": None},
        {"name": "With Stop Loss", "stop_loss": 0.02, "take_profit": None},
        {"name": "With Take Profit", "stop_loss": None, "take_profit": 0.03},
        {"name": "With Both SL/TP", "stop_loss": 0.02, "take_profit": 0.05}
    ]
    
    results = []
    
    # Test each parameter combination
    for i, case in enumerate(test_cases):
        logger.info(f"Test Case {i+1}: {case['name']}")
        
        try:
            # Create portfolio
            pf = CustomPortfolio.from_signals(
                close=df['close'],
                entries=entries,
                exits=exits,
                stop_loss=case['stop_loss'],
                take_profit=case['take_profit'],
                init_cash=10000,
                freq='1D'
            )
            
            # Get basic metrics directly from portfolio attributes
            total_return = pf.total_return if hasattr(pf, 'total_return') else None
            final_value = pf.final_value if hasattr(pf, 'final_value') else None
            
            # Get number of trades
            num_trades = len(pf.trades) if hasattr(pf, 'trades') else 0
            
            # Try to get exit types if method exists
            exit_types = {}
            if hasattr(pf, 'get_exit_types'):
                try:
                    exit_types = pf.get_exit_types().value_counts().to_dict()
                except:
                    pass
            
            # Add results
            results.append({
                "case": case['name'],
                "total_return": total_return,
                "final_value": final_value,
                "num_trades": num_trades,
                "status": "Success",
                "exit_types": exit_types
            })
            
            logger.info(f"  - Total Return: {total_return:.2%}" if total_return is not None else "  - Total Return: N/A")
            logger.info(f"  - Final Value: {final_value:.2f}" if final_value is not None else "  - Final Value: N/A")
            logger.info(f"  - Number of Trades: {num_trades}")
            logger.info(f"  - Exit Types: {exit_types}")
            
        except Exception as e:
            logger.error(f"  - Error: {str(e)}")
            results.append({
                "case": case['name'],
                "status": "Error",
                "error": str(e)
            })
    
    # Print summary
    logger.info("Test Summary:")
    for i, result in enumerate(results):
        logger.info(f"{i+1}. {result['case']}: {result['status']}")
    
    # Check if all tests passed
    if all(r['status'] == 'Success' for r in results):
        logger.info("All tests passed ✅")
        return True
    else:
        logger.error("Some tests failed ❌")
        return False

if __name__ == "__main__":
    """Run the test."""
    logger.info("Starting CustomPortfolio compatibility test")
    test_custom_portfolio()
    logger.info("Test completed") 