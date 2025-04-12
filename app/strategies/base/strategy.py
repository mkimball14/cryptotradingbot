from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import logging
# Import Position model
from app.models.position import Position

# ... (logging setup)
logger = logging.getLogger(__name__)

@dataclass
class StrategyState:
    """Represents the current state of a strategy."""
    is_in_position: bool = False
    current_position_size: float = 0.0
    entry_price: Optional[float] = None
    last_update_time: Optional[pd.Timestamp] = None
    regime: str = "unknown"
    trailing_stop_price: Optional[float] = None

class Strategy(ABC):
    """Base class for all trading strategies."""
    
    def __init__(self, 
                 timeframe: str = "4h",
                 risk_per_trade: float = 0.02,  # 2% risk per trade
                 max_position_size: float = 1.0):  # 100% of available balance
        self.timeframe = timeframe
        self.risk_per_trade = risk_per_trade
        self.max_position_size = max_position_size
        self.state = StrategyState()
        
    @abstractmethod
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate strategy-specific indicators."""
        pass
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on indicators."""
        pass
    
    @abstractmethod
    def should_enter_trade(self, row: pd.Series) -> bool:
        """Determine if we should enter a trade."""
        pass
    
    @abstractmethod
    def should_exit_trade(self, row: pd.Series) -> bool:
        """Determine if we should exit a trade."""
        pass
    
    def calculate_position_size(self, 
                              account_balance: float,
                              entry_price: float,
                              stop_loss_price: float) -> float:
        """Calculate position size based on risk parameters."""
        risk_amount = account_balance * self.risk_per_trade
        price_risk = abs(entry_price - stop_loss_price)
        position_size = risk_amount / price_risk
        
        # Ensure we don't exceed max position size
        max_size = account_balance * self.max_position_size / entry_price
        return min(position_size, max_size)
    
    def update_state(self, 
                    timestamp: pd.Timestamp,
                    is_in_position: bool,
                    position_size: float = 0.0,
                    entry_price: Optional[float] = None,
                    regime: Optional[str] = None,
                    trailing_stop_price: Optional[float] = None) -> None:
        """Update the strategy state."""
        self.state.is_in_position = is_in_position
        self.state.current_position_size = position_size
        self.state.entry_price = entry_price
        self.state.last_update_time = timestamp
        if regime is not None:
            self.state.regime = regime
        if trailing_stop_price is not None:
            self.state.trailing_stop_price = trailing_stop_price
        elif not is_in_position:
            self.state.trailing_stop_price = None
    
    def get_state(self) -> StrategyState:
        """Get current strategy state."""
        return self.state 