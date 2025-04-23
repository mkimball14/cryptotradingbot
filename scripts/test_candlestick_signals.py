#!/usr/bin/env python
"""
Test script for the candlestick pattern strategy.
This script tests the strategy's ability to generate signals from test data.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Import the strategy
from scripts.strategies.candlestick_pattern_strategy import CandlestickPatternStrategy

def load_or_generate_test_data():
    """Load existing test data or generate if not available"""
    try:
        # Try to load from the test_candle_patterns module
        from scripts.test_candle_patterns import load_test_data
        data = load_test_data()
        print(f"Loaded test data with {len(data)} data points")
        return data
    except Exception as e:
        print(f"Error loading test data: {e}")
        print("Generating synthetic test data...")
        
        # Generate synthetic test data
        dates = pd.date_range(start='2020-01-01', periods=500, freq='D')
        df = pd.DataFrame(index=dates)
        
        # Start with a base price and add random walk
        np.random.seed(42)
        close = 100.0
        closes = [close]
        
        for _ in range(1, 500):
            pct_change = np.random.normal(0, 0.015)
            close = close * (1 + pct_change)
            closes.append(close)
        
        df['close'] = closes
        
        # Generate open, high, low
        for i in range(len(df)):
            if i == 0:
                df.loc[df.index[i], 'open'] = df.loc[df.index[i], 'close'] * (1 - 0.005)
            else:
                df.loc[df.index[i], 'open'] = df.loc[df.index[i-1], 'close'] * (1 + np.random.normal(0, 0.003))
            
            # Add some randomness to create high and low
            daily_volatility = abs(df.loc[df.index[i], 'close'] - df.loc[df.index[i], 'open']) * 2
            if daily_volatility < 0.001 * df.loc[df.index[i], 'close']:
                daily_volatility = 0.001 * df.loc[df.index[i], 'close']
                
            # Create high and low
            df.loc[df.index[i], 'high'] = max(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) + np.random.random() * daily_volatility
            df.loc[df.index[i], 'low'] = min(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) - np.random.random() * daily_volatility
            
        # Add volume
        df['volume'] = np.random.exponential(scale=1000000, size=len(df))
        
        print(f"Generated synthetic test data with {len(df)} data points")
        return df

def test_candlestick_strategy():
    """Test the candlestick pattern strategy's signal generation"""
    print("Testing CandlestickPatternStrategy signal generation")
    
    # Load or generate test data
    data = load_or_generate_test_data()
    
    # Define test parameter sets
    test_configs = [
        {
            "name": "Default Config",
            "config": {
                'lookback_periods': 30,
                'min_strength': 0.01,
                'use_strength': True,
                'use_confirmation': False,
                'stop_loss_pct': 0.03,
                'take_profit_pct': 0.06
            }
        },
        {
            "name": "High Strength Threshold",
            "config": {
                'lookback_periods': 30,
                'min_strength': 0.05,
                'use_strength': True,
                'use_confirmation': False,
                'stop_loss_pct': 0.03,
                'take_profit_pct': 0.06
            }
        },
        {
            "name": "No Strength Consideration",
            "config": {
                'lookback_periods': 30,
                'min_strength': 0.01,
                'use_strength': False,
                'use_confirmation': False,
                'stop_loss_pct': 0.03,
                'take_profit_pct': 0.06
            }
        }
    ]
    
    # Test each configuration
    results = {}
    
    for test in test_configs:
        print(f"\nTesting configuration: {test['name']}")
        
        # Initialize strategy with test config
        strategy = CandlestickPatternStrategy(config=test['config'])
        
        # Prepare data
        prepared_data = strategy.prepare_data(data)
        
        # Generate signals
        signal_data = strategy.generate_signals(prepared_data)
        
        # Get summary of signals
        buy_signals = (signal_data['signal'] == 1).sum()
        sell_signals = (signal_data['signal'] == -1).sum()
        
        print(f"Generated {buy_signals} buy signals and {sell_signals} sell signals")
        
        # Store results
        results[test['name']] = {
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'data': signal_data
        }
        
        # Plot signals if we have any
        if buy_signals > 0 or sell_signals > 0:
            plot_signals(signal_data, test['name'])
    
    return results

def plot_signals(data, config_name):
    """Plot price chart with buy/sell signals"""
    try:
        # Create output directory
        output_dir = Path('output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Plot price and signals
        plt.figure(figsize=(14, 7))
        
        # Plot price
        plt.plot(data.index, data['close'], label='Close Price', color='blue')
        
        # Plot buy signals
        buy_signals = data.index[data['signal'] == 1]
        if len(buy_signals) > 0:
            plt.scatter(buy_signals, data.loc[buy_signals, 'close'], 
                        color='green', marker='^', s=100, label='Buy Signal')
        
        # Plot sell signals
        sell_signals = data.index[data['signal'] == -1]
        if len(sell_signals) > 0:
            plt.scatter(sell_signals, data.loc[sell_signals, 'close'], 
                        color='red', marker='v', s=100, label='Sell Signal')
        
        # Add titles and legends
        plt.title(f'Candlestick Pattern Signals - {config_name}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        
        # Save plot
        safe_config_name = config_name.lower().replace(' ', '_')
        plt.savefig(output_dir / f'candlestick_signals_{safe_config_name}.png')
        plt.close()
        
        print(f"Signal chart saved to output/candlestick_signals_{safe_config_name}.png")
        
    except Exception as e:
        print(f"Error plotting signals: {e}")

if __name__ == "__main__":
    results = test_candlestick_strategy() 