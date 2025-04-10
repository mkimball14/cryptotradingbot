import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Union
from datetime import datetime

class PerformanceMetrics:
    """
    A class to calculate various trading performance metrics from trade history.
    """
    
    def __init__(self, trade_history: List[Dict]):
        """
        Initialize the PerformanceMetrics calculator with trade history.
        
        Args:
            trade_history: List of trade dictionaries containing at least:
                - timestamp: datetime
                - price: float
                - size: float
                - side: str ('buy' or 'sell')
                - fee: float
                - portfolio_value: float
        """
        self.trade_history = trade_history
        self.trades_df = pd.DataFrame(trade_history)
        if not trade_history:
            self.trades_df = pd.DataFrame(columns=['timestamp', 'price', 'size', 'side', 'fee', 'portfolio_value'])
        
        # Convert timestamp strings to datetime if needed
        if 'timestamp' in self.trades_df.columns and isinstance(self.trades_df['timestamp'].iloc[0], str):
            self.trades_df['timestamp'] = pd.to_datetime(self.trades_df['timestamp'])
            
    def calculate_returns(self) -> List[float]:
        """Calculate the returns between consecutive portfolio values."""
        if len(self.trades_df) < 2:
            return []
            
        portfolio_values = self.trades_df['portfolio_value'].values
        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        return returns.tolist()
    
    def calculate_total_return(self) -> float:
        """Calculate the total return percentage."""
        if len(self.trades_df) < 2:
            return 0.0
            
        initial_value = self.trades_df['portfolio_value'].iloc[0]
        final_value = self.trades_df['portfolio_value'].iloc[-1]
        return ((final_value - initial_value) / initial_value) * 100
    
    def calculate_annualized_return(self) -> float:
        """Calculate the annualized return percentage."""
        if len(self.trades_df) < 2:
            return 0.0
            
        total_days = (self.trades_df['timestamp'].iloc[-1] - self.trades_df['timestamp'].iloc[0]).days
        if total_days == 0:
            return 0.0
            
        total_return = self.calculate_total_return() / 100  # Convert percentage to decimal
        annualized_return = ((1 + total_return) ** (365 / total_days) - 1) * 100
        return annualized_return
    
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """
        Calculate the Sharpe ratio using daily returns.
        
        Args:
            risk_free_rate: Annual risk-free rate (default: 2%)
        """
        returns = self.calculate_returns()
        if not returns:
            return 0.0
            
        returns_series = pd.Series(returns)
        daily_rf_rate = (1 + risk_free_rate) ** (1/365) - 1
        excess_returns = returns_series - daily_rf_rate
        
        if excess_returns.std() == 0:
            return 0.0
            
        sharpe = np.sqrt(365) * (excess_returns.mean() / excess_returns.std())
        return sharpe
    
    def calculate_max_drawdown(self) -> float:
        """Calculate the maximum drawdown percentage."""
        if len(self.trades_df) < 2:
            return 0.0
            
        portfolio_values = self.trades_df['portfolio_value'].values
        peak = portfolio_values[0]
        max_dd = 0.0
        
        for value in portfolio_values[1:]:
            if value > peak:
                peak = value
            dd = (peak - value) / peak * 100
            max_dd = max(max_dd, dd)
            
        return max_dd
    
    def calculate_win_rate(self) -> float:
        """Calculate the win rate percentage."""
        if len(self.trades_df) < 2:
            return 0.0
            
        # Group trades into completed trades (buy + sell)
        completed_trades = []
        current_position = None
        
        for _, trade in self.trades_df.iterrows():
            if trade['side'].lower() == 'buy':
                current_position = trade
            elif trade['side'].lower() == 'sell' and current_position is not None:
                # Calculate profit/loss
                profit = (trade['price'] - current_position['price']) * trade['size'] - \
                        (trade['fee'] + current_position['fee'])
                completed_trades.append(profit)
                current_position = None
        
        if not completed_trades:
            return 0.0
            
        winning_trades = sum(1 for profit in completed_trades if profit > 0)
        return (winning_trades / len(completed_trades)) * 100
    
    def calculate_profit_factor(self) -> float:
        """Calculate the profit factor (gross profit / gross loss)."""
        if len(self.trades_df) < 2:
            return 0.0
            
        # Group trades into completed trades
        completed_trades = []
        current_position = None
        
        for _, trade in self.trades_df.iterrows():
            if trade['side'].lower() == 'buy':
                current_position = trade
            elif trade['side'].lower() == 'sell' and current_position is not None:
                profit = (trade['price'] - current_position['price']) * trade['size'] - \
                        (trade['fee'] + current_position['fee'])
                completed_trades.append(profit)
                current_position = None
        
        if not completed_trades:
            return 0.0
            
        gross_profit = sum(profit for profit in completed_trades if profit > 0)
        gross_loss = abs(sum(profit for profit in completed_trades if profit < 0))
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0
            
        return gross_profit / gross_loss
    
    def calculate_average_trade(self) -> Dict[str, float]:
        """Calculate average trade metrics."""
        if len(self.trades_df) < 2:
            return {
                'average_profit': 0.0,
                'average_win': 0.0,
                'average_loss': 0.0
            }
            
        # Group trades into completed trades
        completed_trades = []
        current_position = None
        
        for _, trade in self.trades_df.iterrows():
            if trade['side'].lower() == 'buy':
                current_position = trade
            elif trade['side'].lower() == 'sell' and current_position is not None:
                profit = (trade['price'] - current_position['price']) * trade['size'] - \
                        (trade['fee'] + current_position['fee'])
                completed_trades.append(profit)
                current_position = None
        
        if not completed_trades:
            return {
                'average_profit': 0.0,
                'average_win': 0.0,
                'average_loss': 0.0
            }
            
        winning_trades = [profit for profit in completed_trades if profit > 0]
        losing_trades = [profit for profit in completed_trades if profit < 0]
        
        return {
            'average_profit': np.mean(completed_trades) if completed_trades else 0.0,
            'average_win': np.mean(winning_trades) if winning_trades else 0.0,
            'average_loss': np.mean(losing_trades) if losing_trades else 0.0
        }
    
    def get_all_metrics(self) -> Dict[str, Union[float, Dict[str, float]]]:
        """Calculate and return all performance metrics."""
        metrics = {
            'total_return': self.calculate_total_return(),
            'annualized_return': self.calculate_annualized_return(),
            'sharpe_ratio': self.calculate_sharpe_ratio(),
            'max_drawdown': self.calculate_max_drawdown(),
            'win_rate': self.calculate_win_rate(),
            'profit_factor': self.calculate_profit_factor(),
            'trade_metrics': self.calculate_average_trade(),
            'total_trades': len(self.trades_df) // 2,  # Divide by 2 since each complete trade has a buy and sell
            'total_volume': (self.trades_df['price'] * self.trades_df['size']).sum(),
            'total_fees': self.trades_df['fee'].sum()
        }
        return metrics 