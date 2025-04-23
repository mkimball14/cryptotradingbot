import numpy as np
import pandas as pd
from typing import Dict, Any, List, Union, Tuple, Optional
import logging
from abc import ABC, abstractmethod

# Configure logging
logger = logging.getLogger("strategy_base")

class StrategyBase(ABC):
    """
    Base class for all trading strategies.
    Provides common functionality and defines the interface that all strategies should implement.
    """
    
    def __init__(self, 
                config: Dict[str, Any] = None, 
                **kwargs):
        """
        Initialize the strategy with configuration parameters.
        
        Args:
            config: Dictionary containing strategy parameters
            **kwargs: Additional keyword arguments
        """
        # Initialize config dictionary
        self.config = config or {}
        
        # Common strategy attributes
        self.name = "Base Strategy"
        self.description = "Base strategy class"
        
        # Log initialization
        logger.info(f"Initialized strategy base class with config: {self.config}")
    
    @abstractmethod
    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare input data for the strategy. This typically involves calculating
        indicators, features, or transforming the data in some way.
        
        Args:
            data: DataFrame with price/market data
            
        Returns:
            DataFrame with prepared data (indicators, features, etc.)
        """
        pass
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on prepared data.
        
        Args:
            data: DataFrame with prepared data
            
        Returns:
            DataFrame with added signal columns
        """
        pass
    
    @abstractmethod
    def execute_trades(self, data: pd.DataFrame, broker=None) -> List[Dict[str, Any]]:
        """
        Execute trades based on signals.
        
        Args:
            data: DataFrame with signals
            broker: Broker interface for executing trades
            
        Returns:
            List of executed trade dictionaries
        """
        pass
    
    @abstractmethod
    def backtest(self, data: pd.DataFrame, initial_capital: float = 10000.0) -> Dict[str, Any]:
        """
        Run a backtest of the strategy on historical data.
        
        Args:
            data: DataFrame with OHLCV data
            initial_capital: Initial capital for the backtest
            
        Returns:
            Dictionary with backtest results
        """
        pass
    
    def calculate_position_size(self, 
                               account_balance: float,
                               entry_price: float,
                               stop_loss_price: float,
                               risk_per_trade: float = 0.02) -> float:
        """
        Calculate position size based on risk parameters.
        
        Args:
            account_balance: Current account balance
            entry_price: Entry price for the trade
            stop_loss_price: Stop loss price for the trade
            risk_per_trade: Percentage of account to risk per trade
            
        Returns:
            Calculated position size
        """
        # Calculate risk amount in currency
        risk_amount = account_balance * risk_per_trade
        
        # Calculate price risk (difference between entry and stop loss)
        price_risk = abs(entry_price - stop_loss_price)
        
        # Ensure price risk is not zero
        if price_risk == 0:
            logger.warning("Price risk is zero. Using default 1% of entry price.")
            price_risk = entry_price * 0.01
        
        # Calculate position size
        position_size = risk_amount / price_risk
        
        return position_size
    
    def evaluate_performance(self, 
                           equity_curve: List[float], 
                           trades: List[Dict[str, Any]],
                           initial_capital: float = 10000.0) -> Dict[str, Any]:
        """
        Calculate performance metrics from backtest results.
        
        Args:
            equity_curve: List of equity values over time
            trades: List of trade dictionaries
            initial_capital: Initial capital for the backtest
            
        Returns:
            Dictionary of performance metrics
        """
        # Convert to numpy arrays for calculations
        equity = np.array(equity_curve)
        
        # Calculate returns
        returns = np.diff(equity) / equity[:-1]
        
        # Calculate total return
        total_return = (equity[-1] / initial_capital - 1) * 100
        
        # Calculate annualized return (assuming 252 trading days per year)
        days = len(equity)
        annual_return = ((1 + total_return / 100) ** (252 / days) - 1) * 100 if days > 0 else 0
        
        # Calculate max drawdown
        peak = equity[0]
        max_drawdown = 0
        
        for value in equity:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)
        
        max_drawdown_pct = max_drawdown * 100
        
        # Calculate Sharpe ratio (assuming risk-free rate of 0)
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252) if len(returns) > 0 and np.std(returns) > 0 else 0
        
        # Calculate win rate
        if trades:
            profitable_trades = sum(1 for t in trades if t.get('profit_loss', 0) > 0)
            win_rate = profitable_trades / len(trades)
            
            # Calculate average win/loss
            wins = [t.get('profit_loss', 0) for t in trades if t.get('profit_loss', 0) > 0]
            losses = [t.get('profit_loss', 0) for t in trades if t.get('profit_loss', 0) < 0]
            
            avg_win = np.mean(wins) if wins else 0
            avg_loss = np.mean(losses) if losses else 0
            
            # Calculate profit factor
            profit_sum = sum(wins)
            loss_sum = abs(sum(losses)) if losses else 1  # Avoid division by zero
            
            profit_factor = profit_sum / loss_sum if loss_sum > 0 else float('inf')
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            profit_factor = 0
        
        # Return all metrics
        return {
            'initial_capital': initial_capital,
            'final_capital': equity[-1],
            'total_return_pct': total_return,
            'annual_return_pct': annual_return,
            'max_drawdown_pct': max_drawdown_pct,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'total_trades': len(trades),
            'profitable_trades': profitable_trades if trades else 0,
            'equity_curve': equity_curve,
            'trades': trades
        } 