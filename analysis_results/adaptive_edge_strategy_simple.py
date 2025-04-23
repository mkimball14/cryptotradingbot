#!/usr/bin/env python3
"""
Simplified Adaptive Edge Strategy for testing
"""

import numpy as np
import pandas as pd
import vectorbtpro as vbt

class SimpleAdaptiveStrategy:
    def __init__(self, data, initial_capital=10000):
        self.data = data
        self.initial_capital = initial_capital
        
    def calculate_indicators(self):
        # Calculate a simple moving average
        self.data['SMA20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA50'] = self.data['Close'].rolling(window=50).mean()
        
        # Generate trading signals
        self.data['Signal'] = 0
        self.data.loc[self.data['SMA20'] > self.data['SMA50'], 'Signal'] = 1  # Buy signal
        self.data.loc[self.data['SMA20'] < self.data['SMA50'], 'Signal'] = -1  # Sell signal
        
        # Create entry/exit conditions
        self.data['Entry'] = (self.data['Signal'] == 1) & (self.data['Signal'].shift(1) != 1)
        self.data['Exit'] = (self.data['Signal'] == -1) & (self.data['Signal'].shift(1) != -1)
    
    def backtest_strategy(self):
        """Run a backtest of the strategy and return performance metrics"""
        self.calculate_indicators()
        
        # Drop any rows with NaN values (from the rolling calculations)
        data = self.data.dropna()
        
        # Run the backtest
        pf = vbt.Portfolio.from_signals(
            data['Close'],
            entries=data['Entry'],
            exits=data['Exit'],
            init_cash=self.initial_capital,
            fees=0.001  # 0.1% trading fee
        )
        
        # Return performance statistics
        return pf.stats()
    
    def plot_equity_curve(self):
        """Plot the equity curve of the strategy"""
        self.calculate_indicators()
        
        # Drop any rows with NaN values
        data = self.data.dropna()
        
        # Run the backtest
        pf = vbt.Portfolio.from_signals(
            data['Close'],
            entries=data['Entry'],
            exits=data['Exit'],
            init_cash=self.initial_capital,
            fees=0.001
        )
        
        # Plot the equity curve
        fig = pf.plot()
        return fig 