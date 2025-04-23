#!/usr/bin/env python3
"""
Simple trading strategy using only pandas (no vectorbtpro)
to test the basic concept of the adaptive strategy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PandasSimpleStrategy:
    def __init__(self, data, initial_capital=10000):
        self.data = data.copy()
        self.initial_capital = initial_capital
        
    def calculate_indicators(self):
        # Calculate a simple moving average
        self.data['SMA20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA50'] = self.data['Close'].rolling(window=50).mean()
        
        # Generate trading signals
        self.data['Signal'] = 0
        self.data.loc[self.data['SMA20'] > self.data['SMA50'], 'Signal'] = 1  # Buy signal
        self.data.loc[self.data['SMA20'] < self.data['SMA50'], 'Signal'] = -1  # Sell signal
        
        # Create entry/exit points
        self.data['Trade'] = self.data['Signal'].diff()
        
        # Remove NaN values
        self.data = self.data.dropna()
        
        return self.data
    
    def backtest_strategy(self):
        """
        Run a backtest of the strategy and return performance metrics
        """
        self.calculate_indicators()
        
        # Initialize portfolio metrics
        self.data['Position'] = 0
        self.data['Cash'] = self.initial_capital
        self.data['Holdings'] = 0
        self.data['Portfolio'] = self.initial_capital
        
        position = 0
        entry_price = 0
        
        # Loop through the data to calculate positions and portfolio value
        for i in range(len(self.data)):
            # Update position based on signals
            if self.data['Trade'].iloc[i] == 2:  # Entry signal (from -1 to 1)
                position = 1
                entry_price = self.data['Close'].iloc[i]
                
                # Calculate number of shares to buy (use 95% of cash to account for fees)
                cash = self.data['Cash'].iloc[i-1] if i > 0 else self.initial_capital
                shares = int((cash * 0.95) / entry_price)
                
                # Update metrics
                self.data.loc[self.data.index[i], 'Position'] = position
                self.data.loc[self.data.index[i], 'Cash'] = cash - (shares * entry_price * 1.001)  # 0.1% fee
                self.data.loc[self.data.index[i], 'Holdings'] = shares * self.data['Close'].iloc[i]
                
            elif self.data['Trade'].iloc[i] == -2:  # Exit signal (from 1 to -1)
                position = 0
                
                # Calculate proceeds from sale
                prev_holdings = self.data['Holdings'].iloc[i-1] if i > 0 else 0
                cash = self.data['Cash'].iloc[i-1] if i > 0 else self.initial_capital
                sale_proceeds = prev_holdings * 0.999  # 0.1% fee
                
                # Update metrics
                self.data.loc[self.data.index[i], 'Position'] = position
                self.data.loc[self.data.index[i], 'Cash'] = cash + sale_proceeds
                self.data.loc[self.data.index[i], 'Holdings'] = 0
            else:
                # No change in position, just update metrics
                if i > 0:
                    self.data.loc[self.data.index[i], 'Position'] = self.data['Position'].iloc[i-1]
                    self.data.loc[self.data.index[i], 'Cash'] = self.data['Cash'].iloc[i-1]
                    
                    if self.data['Position'].iloc[i] == 1:
                        # If in position, update holdings value based on current price
                        shares = self.data['Holdings'].iloc[i-1] / self.data['Close'].iloc[i-1]
                        self.data.loc[self.data.index[i], 'Holdings'] = shares * self.data['Close'].iloc[i]
                    else:
                        self.data.loc[self.data.index[i], 'Holdings'] = 0
            
            # Calculate total portfolio value
            self.data.loc[self.data.index[i], 'Portfolio'] = \
                self.data['Cash'].iloc[i] + self.data['Holdings'].iloc[i]
        
        # Calculate performance metrics
        stats = {
            'Initial Capital': self.initial_capital,
            'Final Portfolio Value': self.data['Portfolio'].iloc[-1],
            'Total Return': (self.data['Portfolio'].iloc[-1] / self.initial_capital - 1) * 100,
            'Max Drawdown': self._calculate_max_drawdown(),
            'Sharpe Ratio': self._calculate_sharpe_ratio(),
            'Number of Trades': len(self.data[self.data['Trade'] != 0])
        }
        
        return pd.Series(stats)
    
    def _calculate_max_drawdown(self):
        """
        Calculate the maximum drawdown of the strategy
        """
        portfolio = self.data['Portfolio']
        cummax = portfolio.cummax()
        drawdown = (portfolio - cummax) / cummax
        return drawdown.min() * 100
    
    def _calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """
        Calculate the Sharpe ratio of the strategy
        """
        portfolio = self.data['Portfolio']
        returns = portfolio.pct_change().dropna()
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        if len(excess_returns) > 0:
            return np.sqrt(252) * excess_returns.mean() / returns.std()
        return 0
    
    def plot_equity_curve(self):
        """
        Plot the equity curve of the strategy
        """
        if 'Portfolio' not in self.data.columns:
            self.backtest_strategy()
            
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.data.index, self.data['Portfolio'], label='Portfolio Value')
        
        # Plot buy and sell signals
        buy_signals = self.data[self.data['Trade'] == 2]
        sell_signals = self.data[self.data['Trade'] == -2]
        
        ax.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', s=100, label='Buy')
        ax.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', s=100, label='Sell')
        
        ax.set_title('Portfolio Value and Trading Signals')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value ($)')
        ax.legend()
        ax.grid(True)
        
        return fig 