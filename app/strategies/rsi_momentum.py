from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np

from .base.strategy import Strategy, StrategyState
from .indicators.technical import calculate_rsi, detect_regime, calculate_atr, calculate_ma

class RSIMomentumStrategy(Strategy):
    """
    RSI Momentum strategy with market regime filter.
    
    Entry Rules:
    - RSI(14) crosses above 60
    - Market regime must be "uptrend"
    
    Exit Rules:
    - RSI falls below 40
    - Market regime changes to "downtrend"
    """
    
    def __init__(self,
                 timeframe: str = "4h",
                 rsi_period: int = 14,
                 rsi_entry_threshold: float = 60.0,
                 rsi_exit_threshold: float = 40.0,
                 ma_period: int = 20,
                 atr_period: int = 14,
                 risk_per_trade: float = 0.02,
                 atr_stop_multiplier: float = 2.0):
        """
        Initialize RSI Momentum strategy.
        """
        super().__init__(timeframe=timeframe, risk_per_trade=risk_per_trade)
        
        self.rsi_period = rsi_period
        self.rsi_entry_threshold = rsi_entry_threshold
        self.rsi_exit_threshold = rsi_exit_threshold
        self.ma_period = ma_period
        self.atr_period = atr_period
        self.atr_stop_multiplier = atr_stop_multiplier
        self.state = StrategyState() # Initialize state
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate necessary indicators: RSI, Regime, ATR."""
        df = data.copy()
        df['rsi'] = calculate_rsi(df, period=self.rsi_period)
        df['regime'], df['volatility'] = detect_regime(
            df, ma_period=self.ma_period, atr_period=self.atr_period
        )
        df['atr'] = calculate_atr(df, period=self.atr_period)
        return df
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate entry and exit signals based on RSI and regime."""
        df = self.calculate_indicators(data)
        df['signal'] = 0  # Default to hold
        df['stop_loss'] = np.nan # Store initial stop calculated at entry signal
        
        # --- Entry Signal Logic ---
        entry_condition = (
            (df['rsi'] > self.rsi_entry_threshold) &
            (df['rsi'].shift(1) <= self.rsi_entry_threshold) &
            (df['regime'] == "uptrend")
        )
        df.loc[entry_condition, 'signal'] = 1
        
        # --- Exit Signal Logic ---
        exit_condition = (
            (df['rsi'] < self.rsi_exit_threshold) | 
            (df['regime'] == "downtrend")
        )
        # Generate exit signal (-1) only on the first bar the condition is met after being in a trade
        df.loc[exit_condition & (df['signal'].shift(1) == 1), 'signal'] = -1 
        
        # --- Calculate Initial Stop Loss for Potential Entries ---
        df.loc[entry_condition, 'stop_loss'] = (
            df['low'] - df['atr'] * self.atr_stop_multiplier
        )
        
        return df

    # Override update_state to handle trailing stop state
    def update_state(self, 
                     timestamp: pd.Timestamp, 
                     is_in_position: bool, 
                     position_size: float, 
                     entry_price: Optional[float],
                     regime: Optional[str] = None,
                     trailing_stop_price: Optional[float] = None): 
        super().update_state(timestamp, is_in_position, position_size, entry_price, regime)
        # Set/update/reset trailing stop price in the state
        if trailing_stop_price is not None:
             self.state.trailing_stop_price = trailing_stop_price
        elif not is_in_position: # Reset trailing stop if position closed
             self.state.trailing_stop_price = None

    def should_enter_trade(self, row: pd.Series) -> bool:
        """Check if we should enter a trade based on the generated signal and regime."""
        # Signal incorporates regime check from generate_signals
        return (
            row['signal'] == 1 and
            not self.state.is_in_position 
        )
    
    def should_exit_trade(self, row: pd.Series) -> bool:
        """
        Check if we should exit based on RSI, Regime, OR TRAILING STOP.
        """
        if not self.state.is_in_position:
            return False
            
        # 1. Check Trailing Stop Loss first
        stop_hit = self.state.trailing_stop_price is not None and row['low'] <= self.state.trailing_stop_price
        if stop_hit:
            # print(f"[{row.name.date()}] Exit signal: Trailing Stop Hit @ {self.state.trailing_stop_price:.2f} (Low: {row['low']:.2f})")
            return True
            
        # 2. Check Original RSI / Regime Exit Conditions
        rsi_exit = row['rsi'] < self.rsi_exit_threshold # Check against 40
        regime_exit = row['regime'] == "downtrend"
        
        if rsi_exit:
            # print(f"[{row.name.date()}] Exit signal: RSI < {self.rsi_exit_threshold}")
            return True
        if regime_exit:
            # print(f"[{row.name.date()}] Exit signal: Regime Downtrend")
            return True
            
        return False
    
    def calculate_stop_loss(self, row: pd.Series) -> float:
        """Calculate initial stop loss price for a potential trade."""
        # Use the pre-calculated stop_loss value from the signal generation step
        if 'stop_loss' in row and not pd.isna(row['stop_loss']):
            return row['stop_loss']
        else:
            # Fallback calculation if needed (should use pre-calculated value)
            print(f"Warning: Using dynamic stop loss calculation for row {row.name}.")
            return row['low'] - row['atr'] * self.atr_stop_multiplier 