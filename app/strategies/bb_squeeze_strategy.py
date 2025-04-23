import logging
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional, List

from app.strategies.base.strategy import Strategy, StrategyState
from app.strategies.indicators.technical import (
    calculate_bb_squeeze,
    calculate_atr,
    calculate_bbands
)
from app.core.indicators import calculate_rsi

logger = logging.getLogger(__name__)

@dataclass
class BBSqueezeState(StrategyState):
    """Extended state for the Bollinger Bands Squeeze strategy."""
    is_in_squeeze: bool = False
    squeeze_length: int = 0
    squeeze_intensity: float = 0.0
    squeeze_momentum: float = 0.0
    rsi: float = 50.0
    atr: float = 0.0
    trailing_stop: Optional[float] = None
    last_signal_price: Optional[float] = None

class BBSqueezeStrategy(Strategy):
    """
    Bollinger Bands Squeeze Strategy.
    
    This strategy identifies periods of low volatility (the squeeze) using Bollinger Bands
    and Keltner Channels, then takes positions when volatility expands in either direction.
    
    Entry Rules:
    - Long: When price breaks out of a squeeze with positive momentum and RSI > 50
    - Short: When price breaks out of a squeeze with negative momentum and RSI < 50
    
    Exit Rules:
    - Trailing stop based on ATR
    - Take profit when momentum reverses
    - Stop loss based on maximum risk
    """
    
    def __init__(self, 
                 params: Dict[str, Any] = None,
                 name: str = "BB_Squeeze"):
        """
        Initialize the Bollinger Bands Squeeze strategy.
        
        Args:
            params: Dictionary of strategy parameters
            name: Name of the strategy
        """
        default_params = {
            # BB Squeeze parameters
            "bb_period": 20,
            "bb_std_dev": 2.0,
            "kc_period": 20,
            "kc_factor": 1.5,
            "use_ema": True,
            
            # RSI parameters
            "rsi_period": 14,
            "rsi_entry_threshold": 50,
            
            # Entry parameters
            "min_squeeze_length": 5,
            "momentum_threshold": 0.5,
            "entry_confirmation_bars": 2,
            
            # Position sizing and risk management
            "position_size_pct": 0.02,
            "max_risk_pct": 0.01,
            "trailing_stop_atr_factor": 2.0,
            "take_profit_atr_factor": 3.0,
            "stop_loss_atr_factor": 1.5
        }
        
        # Override default parameters with provided parameters
        if params:
            default_params.update(params)
            
        super().__init__(default_params, name=name)
        self.state = BBSqueezeState()
        
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate strategy indicators.
        
        Args:
            data: OHLC price data
            
        Returns:
            DataFrame with calculated indicators
        """
        df = data.copy()
        
        # Calculate BB Squeeze indicator
        is_squeeze, squeeze_intensity, momentum = calculate_bb_squeeze(
            df,
            bb_period=self.params["bb_period"],
            bb_std_dev=self.params["bb_std_dev"],
            kc_period=self.params["kc_period"],
            kc_factor=self.params["kc_factor"],
            use_ema=self.params["use_ema"]
        )
        
        df['is_squeeze'] = is_squeeze
        df['squeeze_intensity'] = squeeze_intensity
        df['squeeze_momentum'] = momentum
        
        # Calculate RSI
        df['rsi'] = calculate_rsi(df['close'], period=self.params["rsi_period"])
        
        # Calculate ATR for position sizing and stop loss
        df['atr'] = calculate_atr(df, period=self.params["bb_period"])
        
        # Calculate basic Bollinger Bands for reference
        bb_df = calculate_bbands(
            df,
            period=self.params["bb_period"],
            std_dev=self.params["bb_std_dev"]
        )
        
        df = pd.concat([df, bb_df], axis=1)
        
        return df
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the BB Squeeze indicator.
        
        Args:
            data: DataFrame with price data and calculated indicators
            
        Returns:
            DataFrame with signals added
        """
        df = data.copy()
        
        # Initialize signal columns
        df['signal'] = 0  # 1 for buy, -1 for sell, 0 for no action
        df['entry_price'] = np.nan
        df['stop_loss'] = np.nan
        df['take_profit'] = np.nan
        
        # Track the squeeze state
        squeeze_length = 0
        was_in_squeeze = False
        
        for i in range(1, len(df)):
            current_close = df['close'].iloc[i]
            current_atr = df['atr'].iloc[i]
            
            # Update squeeze length counter
            if df['is_squeeze'].iloc[i]:
                if was_in_squeeze:
                    squeeze_length += 1
                else:
                    squeeze_length = 1
                    was_in_squeeze = True
            else:
                # If we were in a squeeze and now we're breaking out
                if was_in_squeeze and squeeze_length >= self.params["min_squeeze_length"]:
                    # Check momentum direction
                    momentum = df['squeeze_momentum'].iloc[i]
                    rsi = df['rsi'].iloc[i]
                    
                    # Generate signals based on momentum and RSI
                    if momentum > self.params["momentum_threshold"] and rsi > self.params["rsi_entry_threshold"]:
                        # Bullish breakout
                        df.loc[df.index[i], 'signal'] = 1
                        df.loc[df.index[i], 'entry_price'] = current_close
                        df.loc[df.index[i], 'stop_loss'] = current_close - (current_atr * self.params["stop_loss_atr_factor"])
                        df.loc[df.index[i], 'take_profit'] = current_close + (current_atr * self.params["take_profit_atr_factor"])
                        
                    elif momentum < -self.params["momentum_threshold"] and rsi < self.params["rsi_entry_threshold"]:
                        # Bearish breakout
                        df.loc[df.index[i], 'signal'] = -1
                        df.loc[df.index[i], 'entry_price'] = current_close
                        df.loc[df.index[i], 'stop_loss'] = current_close + (current_atr * self.params["stop_loss_atr_factor"])
                        df.loc[df.index[i], 'take_profit'] = current_close - (current_atr * self.params["take_profit_atr_factor"])
                
                # Reset squeeze tracking
                was_in_squeeze = False
                squeeze_length = 0
        
        return df
    
    def should_enter_trade(self, data: pd.DataFrame) -> Tuple[bool, dict]:
        """
        Determine if we should enter a trade based on current signals.
        
        Args:
            data: DataFrame with price and indicator data
            
        Returns:
            Tuple of (should_enter, entry_params)
        """
        if len(data) < 2:
            return False, {}
            
        current_bar = data.iloc[-1]
        current_signal = current_bar['signal']
        
        # No signal, no trade
        if current_signal == 0:
            return False, {}
            
        # Update state
        self.state.is_in_squeeze = current_bar['is_squeeze']
        self.state.squeeze_intensity = current_bar['squeeze_intensity']
        self.state.squeeze_momentum = current_bar['squeeze_momentum']
        self.state.rsi = current_bar['rsi']
        self.state.atr = current_bar['atr']
        self.state.last_signal_price = current_bar['close']
        
        # Calculate position size
        position_size = self.calculate_position_size(
            current_bar['close'],
            stop_price=current_bar['stop_loss'],
            risk_pct=self.params["max_risk_pct"]
        )
        
        entry_params = {
            "direction": 1 if current_signal > 0 else -1,
            "entry_price": current_bar['entry_price'],
            "position_size": position_size,
            "stop_loss": current_bar['stop_loss'],
            "take_profit": current_bar['take_profit']
        }
        
        # Set trailing stop
        self.state.trailing_stop = current_bar['stop_loss']
        
        logger.info(f"BB Squeeze strategy: Entry signal generated - {entry_params}")
        return True, entry_params
    
    def should_exit_trade(self, data: pd.DataFrame, position_data: dict) -> Tuple[bool, dict]:
        """
        Determine if we should exit an existing trade.
        
        Args:
            data: DataFrame with price and indicator data
            position_data: Dictionary containing current position information
            
        Returns:
            Tuple of (should_exit, exit_params)
        """
        if len(data) < 2:
            return False, {}
            
        current_bar = data.iloc[-1]
        previous_bar = data.iloc[-2]
        
        direction = position_data.get("direction", 0)
        if direction == 0:
            return False, {}
            
        current_close = current_bar['close']
        current_momentum = current_bar['squeeze_momentum']
        previous_momentum = previous_bar['squeeze_momentum']
        
        exit_reason = None
        
        # Update trailing stop based on ATR
        if direction > 0:  # Long position
            new_stop = current_close - (current_bar['atr'] * self.params["trailing_stop_atr_factor"])
            if self.state.trailing_stop is None or new_stop > self.state.trailing_stop:
                self.state.trailing_stop = new_stop
                
            # Check stop loss hit
            if current_close <= self.state.trailing_stop:
                exit_reason = "trailing_stop"
                
            # Check momentum reversal for long positions
            elif previous_momentum > 0 and current_momentum < 0:
                exit_reason = "momentum_reversal"
                
        else:  # Short position
            new_stop = current_close + (current_bar['atr'] * self.params["trailing_stop_atr_factor"])
            if self.state.trailing_stop is None or new_stop < self.state.trailing_stop:
                self.state.trailing_stop = new_stop
                
            # Check stop loss hit
            if current_close >= self.state.trailing_stop:
                exit_reason = "trailing_stop"
                
            # Check momentum reversal for short positions
            elif previous_momentum < 0 and current_momentum > 0:
                exit_reason = "momentum_reversal"
        
        # If we have an exit reason, exit the trade
        if exit_reason:
            exit_params = {
                "exit_price": current_close,
                "reason": exit_reason
            }
            
            logger.info(f"BB Squeeze strategy: Exit signal generated - {exit_params}")
            
            # Reset state for next trade
            self.state.trailing_stop = None
            
            return True, exit_params
            
        return False, {}
    
    def calculate_position_size(self, price: float, stop_price: float, risk_pct: float) -> float:
        """
        Calculate position size based on risk percentage.
        
        Args:
            price: Current price
            stop_price: Stop loss price
            risk_pct: Risk percentage (0-1)
            
        Returns:
            Position size
        """
        if price <= 0 or stop_price <= 0 or risk_pct <= 0:
            return 0
            
        # Simple position sizing based on fixed percentage risk
        risk_per_share = abs(price - stop_price)
        if risk_per_share <= 0:
            return 0
            
        # Position size = (Account * Risk%) / Risk per share
        # Using 10000 as a placeholder for account size
        account_size = 10000  # This should come from account management module
        position_size = (account_size * risk_pct) / risk_per_share
        
        return position_size
    
    def process_bar(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Process a new price bar and return any signals or state updates.
        
        Args:
            data: DataFrame with price data for the latest bar(s)
            
        Returns:
            Dict with processing results and any signals
        """
        if len(data) < self.params["bb_period"] + 10:
            return {"status": "waiting_for_data"}
        
        # Calculate indicators
        data_with_indicators = self.calculate_indicators(data)
        
        # Generate signals
        data_with_signals = self.generate_signals(data_with_indicators)
        
        # Get the latest record
        latest = data_with_signals.iloc[-1]
        
        results = {
            "timestamp": latest.name,
            "close": latest['close'],
            "is_squeeze": latest['is_squeeze'],
            "squeeze_intensity": latest['squeeze_intensity'],
            "squeeze_momentum": latest['squeeze_momentum'],
            "rsi": latest['rsi'],
            "signal": latest['signal'],
            "bb_upper": latest.get(f'BBU_{self.params["bb_period"]}_{self.params["bb_std_dev"]}', None),
            "bb_lower": latest.get(f'BBL_{self.params["bb_period"]}_{self.params["bb_std_dev"]}', None)
        }
        
        return results 