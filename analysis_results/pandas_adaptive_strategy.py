#!/usr/bin/env python3
"""
Adaptive trading strategy using only pandas (no vectorbtpro)
to implement the adaptive edge concepts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PandasAdaptiveStrategy:
    def __init__(self, data, initial_capital=10000):
        self.data = data.copy()
        self.initial_capital = initial_capital
        
        # Strategy parameters (will be adjusted based on volatility)
        self.atr_period = 14
        self.rsi_period = 14
        self.bollinger_window = 20
        self.bollinger_std = 2
        self.position_size = 0.1  # 10% of portfolio by default
        self.atr_multiplier = 3   # For stop loss/take profit
        
    def _calculate_atr(self, window=14):
        """Calculate Average True Range for volatility measurement"""
        high = self.data['High']
        low = self.data['Low']
        close = self.data['Close']
        
        # Calculate True Range
        tr1 = abs(high - low)
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate ATR using simple moving average
        atr = tr.rolling(window=window).mean()
        return atr
        
    def _calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index"""
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        # Calculate average gain and loss
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    def _calculate_bollinger_bands(self, prices, window=20, num_std=2):
        """Calculate Bollinger Bands"""
        middle_band = prices.rolling(window=window).mean()
        std_dev = prices.rolling(window=window).std()
        
        upper_band = middle_band + (std_dev * num_std)
        lower_band = middle_band - (std_dev * num_std)
        
        return upper_band, middle_band, lower_band
    
    def calculate_indicators(self):
        """Calculate all indicators needed for the strategy"""
        # Calculate ATR for volatility
        self.data['ATR'] = self._calculate_atr(window=self.atr_period)
        
        # Calculate RSI
        self.data['RSI'] = self._calculate_rsi(self.data['Close'], window=self.rsi_period)
        
        # Calculate Bollinger Bands
        upper, middle, lower = self._calculate_bollinger_bands(
            self.data['Close'], 
            window=self.bollinger_window,
            num_std=self.bollinger_std
        )
        
        self.data['BB_Upper'] = upper
        self.data['BB_Middle'] = middle
        self.data['BB_Lower'] = lower
        
        # Detect market regime
        self.data['Market_Regime'] = np.where(
            self.data['Close'] > self.data['BB_Middle'], 
            'Trending', 'Ranging'
        )
        
        # Create entry/exit signals
        self.data['Signal'] = 0
        self.data.loc[self.data['Market_Regime'] == 'Trending', 'Signal'] = 1  # Buy signal
        self.data.loc[self.data['Market_Regime'] == 'Ranging', 'Signal'] = -1  # Sell signal
        
        # Create trade signals (for entries and exits)
        self.data['Trade'] = self.data['Signal'].diff()
        
        # Calculate stop loss and take profit levels
        self.data['Stop_Loss'] = self.data['Close'] - (self.data['ATR'] * self.atr_multiplier)
        self.data['Take_Profit'] = self.data['Close'] + (self.data['ATR'] * self.atr_multiplier)
        
        # Remove NaN values
        self.data = self.data.dropna()
        
        return self.data
    
    def adjust_parameters_based_on_volatility(self):
        """Dynamically adjust strategy parameters based on market volatility"""
        # Identify high volatility periods (ATR > rolling 10-day average ATR)
        high_volatility = self.data['ATR'].rolling(window=10).mean() > self.data['ATR'].mean()
        
        # Adjust parameters for high volatility periods
        # We'll store these in separate columns
        self.data['Adjusted_RSI_Period'] = np.where(high_volatility, 10, 14)
        self.data['Adjusted_Bollinger_Window'] = np.where(high_volatility, 15, 20)
        self.data['Adjusted_ATR_Multiplier'] = np.where(high_volatility, 2, 3)
        
        # For each row, adjust position size based on volatility
        # Lower position size during high volatility
        avg_atr = self.data['ATR'].rolling(window=10).mean()
        # Scale position size inversely with volatility
        self.data['Adjusted_Position_Size'] = 0.05 + (1 / (avg_atr + 0.0001)) * 0.05
        
        # Cap the position size between 0.02 (2%) and 0.15 (15%)
        self.data['Adjusted_Position_Size'] = self.data['Adjusted_Position_Size'].clip(0.02, 0.15)
        
    def backtest_strategy(self):
        """
        Run a backtest of the strategy and return performance metrics
        """
        # Calculate indicators and adjust parameters
        self.calculate_indicators()
        self.adjust_parameters_based_on_volatility()
        
        # Initialize portfolio metrics
        self.data['Position'] = 0
        self.data['Cash'] = self.initial_capital
        self.data['Holdings'] = 0
        self.data['Portfolio'] = self.initial_capital
        
        position = 0
        entry_price = 0
        stop_loss = 0
        take_profit = 0
        
        # Loop through the data to calculate positions and portfolio value
        for i in range(len(self.data)):
            # Get current row
            current = self.data.iloc[i]
            
            # Check for stop loss or take profit if in a position
            if position > 0 and i > 0:
                prev_stop_loss = stop_loss
                prev_take_profit = take_profit
                
                # Check if price hit stop loss
                if current['Low'] <= prev_stop_loss:
                    # Trigger stop loss
                    position = 0
                    
                    # Calculate proceeds from sale
                    prev_holdings = self.data['Holdings'].iloc[i-1]
                    cash = self.data['Cash'].iloc[i-1]
                    sale_proceeds = prev_holdings * 0.999  # 0.1% fee
                    
                    # Update metrics
                    self.data.loc[self.data.index[i], 'Position'] = position
                    self.data.loc[self.data.index[i], 'Cash'] = cash + sale_proceeds
                    self.data.loc[self.data.index[i], 'Holdings'] = 0
                    self.data.loc[self.data.index[i], 'Trade'] = -10  # Special code for stop loss
                    continue
                
                # Check if price hit take profit
                elif current['High'] >= prev_take_profit:
                    # Trigger take profit
                    position = 0
                    
                    # Calculate proceeds from sale
                    prev_holdings = self.data['Holdings'].iloc[i-1]
                    cash = self.data['Cash'].iloc[i-1]
                    sale_proceeds = prev_holdings * 0.999  # 0.1% fee
                    
                    # Update metrics
                    self.data.loc[self.data.index[i], 'Position'] = position
                    self.data.loc[self.data.index[i], 'Cash'] = cash + sale_proceeds
                    self.data.loc[self.data.index[i], 'Holdings'] = 0
                    self.data.loc[self.data.index[i], 'Trade'] = 10  # Special code for take profit
                    continue
            
            # Update position based on signals
            if current['Trade'] == 2:  # Entry signal (from -1 to 1)
                position = 1
                entry_price = current['Close']
                stop_loss = current['Stop_Loss']
                take_profit = current['Take_Profit']
                
                # Use adjusted position size based on volatility
                position_size = current['Adjusted_Position_Size']
                
                # Calculate number of shares to buy
                cash = self.data['Cash'].iloc[i-1] if i > 0 else self.initial_capital
                shares = int((cash * position_size) / entry_price)
                
                # Update metrics
                self.data.loc[self.data.index[i], 'Position'] = position
                self.data.loc[self.data.index[i], 'Cash'] = cash - (shares * entry_price * 1.001)  # 0.1% fee
                self.data.loc[self.data.index[i], 'Holdings'] = shares * current['Close']
                
            elif current['Trade'] == -2:  # Exit signal (from 1 to -1)
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
                        self.data.loc[self.data.index[i], 'Holdings'] = shares * current['Close']
                    else:
                        self.data.loc[self.data.index[i], 'Holdings'] = 0
            
            # Calculate total portfolio value
            self.data.loc[self.data.index[i], 'Portfolio'] = \
                self.data['Cash'].iloc[i] + self.data['Holdings'].iloc[i]
        
        # Calculate performance metrics
        stats = {
            'Initial Capital': self.initial_capital,
            'Final Portfolio Value': self.data['Portfolio'].iloc[-1],
            'Total Return (%)': (self.data['Portfolio'].iloc[-1] / self.initial_capital - 1) * 100,
            'Max Drawdown (%)': self._calculate_max_drawdown(),
            'Sharpe Ratio': self._calculate_sharpe_ratio(),
            'Number of Trades': len(self.data[(self.data['Trade'] == 2) | 
                                              (self.data['Trade'] == -2) | 
                                              (self.data['Trade'] == 10) | 
                                              (self.data['Trade'] == -10)])
        }
        
        return pd.Series(stats)
    
    def _calculate_max_drawdown(self):
        """Calculate the maximum drawdown of the strategy"""
        portfolio = self.data['Portfolio']
        cummax = portfolio.cummax()
        drawdown = (portfolio - cummax) / cummax
        return drawdown.min() * 100  # Convert to percentage
    
    def _calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """Calculate the Sharpe ratio of the strategy"""
        portfolio = self.data['Portfolio']
        returns = portfolio.pct_change().dropna()
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        
        if len(excess_returns) > 0 and returns.std() > 0:
            return np.sqrt(252) * excess_returns.mean() / returns.std()
        return 0
    
    def plot_equity_curve(self):
        """Plot the equity curve of the strategy with trade signals"""
        if 'Portfolio' not in self.data.columns:
            self.backtest_strategy()
            
        fig, ax1 = plt.subplots(figsize=(12, 8))
        
        # Plot portfolio value
        ax1.plot(self.data.index, self.data['Portfolio'], label='Portfolio Value', color='blue')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Portfolio Value ($)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # Create second y-axis for price
        ax2 = ax1.twinx()
        ax2.plot(self.data.index, self.data['Close'], label='Price', color='gray', alpha=0.5)
        ax2.set_ylabel('Price ($)', color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')
        
        # Plot buy signals
        buy_signals = self.data[self.data['Trade'] == 2]
        ax2.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', s=100, label='Buy')
        
        # Plot sell signals
        sell_signals = self.data[self.data['Trade'] == -2]
        ax2.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', s=100, label='Sell')
        
        # Plot stop loss triggers
        stop_loss_signals = self.data[self.data['Trade'] == -10]
        ax2.scatter(stop_loss_signals.index, stop_loss_signals['Close'], marker='x', color='purple', s=100, label='Stop Loss')
        
        # Plot take profit triggers
        take_profit_signals = self.data[self.data['Trade'] == 10]
        ax2.scatter(take_profit_signals.index, take_profit_signals['Close'], marker='*', color='orange', s=100, label='Take Profit')
        
        # Add volatility indicator
        ax3 = ax1.twinx()
        ax3.spines["right"].set_position(("axes", 1.1))  # Offset the right spine
        ax3.plot(self.data.index, self.data['ATR'], label='ATR', color='purple', alpha=0.5)
        ax3.set_ylabel('ATR', color='purple')
        ax3.tick_params(axis='y', labelcolor='purple')
        
        # Add title and legend
        plt.title('Adaptive Strategy Performance')
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines3, labels3 = ax3.get_legend_handles_labels()
        ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc='best')
        
        plt.tight_layout()
        return fig 