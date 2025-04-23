#!/usr/bin/env python
"""
Test script for the candlestick pattern strategy integration with WFO framework.
This script tests a single parameter set without doing full optimization.
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Import WFO modules
from scripts.strategies.wfo_edge_strategy import (
    create_portfolio_for_strategy,
    calculate_performance_metrics
)

# Import data fetcher
try:
    from data.data_fetcher import fetch_historical_data, get_vbt_freq_str
    print("Using data_fetcher from data module")
except ImportError as e:
    print(f"Could not import data_fetcher: {e}. Using backup implementations.")
    
    def fetch_historical_data(symbol, granularity, start_date, end_date):
        """Backup implementation for fetching data"""
        print(f"Fetching data for {symbol} from {start_date} to {end_date}")
        # If data fetcher is not available, try to load test data
        test_data_path = Path(__file__).resolve().parent / 'test_data' / 'sample_ohlc_data.csv'
        if test_data_path.exists():
            df = pd.read_csv(test_data_path, index_col=0, parse_dates=True)
            return df
        else:
            # Use the test_candle_patterns.py to generate data
            from scripts.test_candle_patterns import load_test_data
            return load_test_data()
    
    def get_vbt_freq_str(granularity_str):
        """Backup implementation for getting vbt frequency string"""
        return "1d"

def test_candlestick_strategy():
    """Test the candlestick pattern strategy with a single parameter set"""
    print("Testing CandlestickPatternStrategy integration with WFO framework")
    
    # Set the strategy type globally in the wfo_edge_strategy module
    import scripts.strategies.wfo_edge_strategy as wfo_module
    wfo_module.STRATEGY_TYPE = "candlestick"
    
    # Fetch data for testing
    symbol = "BTC-USD"
    granularity = "1d"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    print(f"Fetching data for {symbol} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Use the test_candle_patterns.py to generate data
    try:
        from scripts.test_candle_patterns import load_test_data
        data = load_test_data()
        print(f"Using test data with {len(data)} data points")
    except Exception as e:
        print(f"Error loading test data: {e}")
        return None
    
    # Define a test parameter set
    params = {
        'lookback_periods': 30,
        'min_strength': 0.01,
        'use_strength': True,
        'use_confirmation': False,
        'confirmation_window': 3,
        'stop_loss_pct': 0.03,
        'take_profit_pct': 0.06,
        'risk_per_trade': 0.02
    }
    
    # Create portfolio with the test parameters
    initial_capital = 10000
    portfolio = create_portfolio_for_strategy(data, params, initial_capital)
    
    if portfolio is None:
        print("Failed to create portfolio. Exiting.")
        return
    
    # Calculate performance metrics
    metrics = calculate_performance_metrics(portfolio)
    
    # Print results
    print("\nPerformance Metrics:")
    print(f"Total Return: {metrics['total_return']:.2f}%")
    print(f"Sharpe Ratio: {metrics['sharpe']:.2f}")
    print(f"Win Rate: {metrics['win_rate']*100:.2f}%")
    print(f"Number of Trades: {metrics['num_trades']}")
    print(f"Maximum Drawdown: {metrics['max_dd']*100:.2f}%")
    
    # Plot the equity curve if possible
    try:
        # Create output directory if not exists
        output_dir = Path('output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Plot equity curve
        plt.figure(figsize=(12, 6))
        if hasattr(portfolio, 'equity_curve'):
            plt.plot(portfolio.equity_curve)
        else:
            plt.plot(portfolio.asset_value())
        
        plt.title(f"Candlestick Strategy Equity Curve\nTotal Return: {metrics['total_return']:.2f}%")
        plt.grid(True)
        plt.savefig(output_dir / 'candlestick_test_equity.png')
        plt.close()
        
        print("\nEquity curve saved to output/candlestick_test_equity.png")
    except Exception as e:
        print(f"Error plotting equity curve: {e}")
    
    return portfolio, metrics

if __name__ == "__main__":
    portfolio, metrics = test_candlestick_strategy() 