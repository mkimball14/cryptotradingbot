import logging
import sys

# Verify Python version and environment
if not (sys.version_info.major == 3 and sys.version_info.minor == 11):
    raise RuntimeError(
        "This script requires Python 3.11\n"
        "Current version: {}.{}.{}".format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
        )
    )

try:
    import vectorbtpro as vbt
except ImportError:
    raise ImportError(
        "vectorbtpro not found. Please activate the correct environment:\n"
        "conda activate vectorbtpro"
    )

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
class BBSqueezeOptimizedState(StrategyState):
    """Extended state for the optimized Bollinger Bands Squeeze strategy."""
    is_in_squeeze: bool = False
    squeeze_length: int = 0
    squeeze_intensity: float = 0.0
    squeeze_momentum: float = 0.0
    rsi: float = 50.0
    atr: float = 0.0
    volume_trend: str = "neutral"  # "up", "down", or "neutral"
    trailing_stop: Optional[float] = None
    last_signal_price: Optional[float] = None
    current_trend: str = "neutral"  # "up", "down", or "neutral"
    in_position: bool = False
    position_type: Optional[str] = None  # "long" or "short"
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

class BBSqueezeOptimizedStrategy(Strategy):
    """
    Optimized Bollinger Bands Squeeze Strategy for Cryptocurrencies.
    
    This strategy is optimized based on testing results with cryptocurrency data.
    It identifies periods of low volatility (the squeeze) using Bollinger Bands
    and Keltner Channels, then takes positions when volatility expands.
    
    Key optimizations:
    - Adjusted default parameters for crypto volatility
    - Added volume confirmation for entry signals
    - Improved exit strategy with trailing stops
    - Added volatility-based position sizing
    
    Entry Rules:
    - Long: When price breaks out of a squeeze with positive momentum, RSI > 50, and volume confirmation
    - Short: When price breaks out of a squeeze with negative momentum, RSI < 50, and volume confirmation
    
    Exit Rules:
    - Trailing stop based on ATR (dynamically adjusted with volatility)
    - Take profit at 1.5x risk
    - Stop loss based on ATR
    """
    
    def __init__(self, 
                 params: Dict[str, Any] = None,
                 name: str = "BB_Squeeze_Optimized"):
        """
        Initialize the optimized Bollinger Bands Squeeze strategy.
        
        Args:
            params: Dictionary of strategy parameters
            name: Name of the strategy
        """
        # Default parameters optimized for cryptocurrencies based on testing
        default_params = {
            # BB Squeeze parameters - conservative settings for crypto
            "bb_period": 20,
            "bb_std_dev": 2.0,
            "kc_period": 20,
            "kc_factor": 1.8,  # Wider Keltner Channels for crypto volatility
            "use_ema": True,
            
            # RSI parameters
            "rsi_period": 14,
            "rsi_entry_threshold": 50,
            
            # Entry parameters
            "min_squeeze_length": 4,  # Longer minimum squeeze for stronger breakouts
            "momentum_threshold": 0.5,  # Higher threshold for better signal quality
            "entry_confirmation_bars": 1,  # Wait for confirmation
            
            # Volume filter
            "use_volume_filter": True,
            "volume_ma_period": 20,
            "volume_threshold": 1.5,  # Volume should be 1.5x average
            
            # Position sizing and risk management
            "position_size_pct": 0.02,  # 2% of account per trade
            "max_risk_pct": 0.01,  # 1% maximum risk per trade
            "trailing_stop_atr_factor": 2.0,  # Trailing stop at 2x ATR
            "take_profit_atr_factor": 3.0,  # Take profit at 3x ATR (1.5x risk)
            "stop_loss_atr_factor": 2.0,  # Stop loss at 2x ATR
            "enable_trailing_stop": True,
            
            # Timeframe-specific settings
            "is_higher_timeframe": False,  # Set to True for daily charts
        }
        
        # Override default parameters with provided parameters
        if params:
            default_params.update(params)
            
        super().__init__(default_params, name=name)
        self.state = BBSqueezeOptimizedState()
        
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
        
        # Volume analysis (if volume data is available)
        if 'volume' in df.columns:
            # Calculate volume moving average
            df['volume_ma'] = df['volume'].rolling(window=self.params["volume_ma_period"]).mean()
            # Volume ratio (current volume relative to average)
            df['volume_ratio'] = df['volume'] / df['volume_ma']
            # Volume trend (rising or falling)
            df['volume_trend'] = np.where(
                df['volume'] > df['volume'].shift(1), 
                np.where(df['volume'] > df['volume_ma'], 'up', 'neutral'),
                np.where(df['volume'] < df['volume_ma'], 'down', 'neutral')
            )
        
        # Determine overall market trend using moving averages
        if self.params["is_higher_timeframe"]:
            # For daily timeframe, use longer MAs
            df['ma_short'] = df['close'].ewm(span=20, adjust=False).mean()
            df['ma_long'] = df['close'].ewm(span=50, adjust=False).mean()
        else:
            # For intraday, use shorter MAs
            df['ma_short'] = df['close'].ewm(span=8, adjust=False).mean()
            df['ma_long'] = df['close'].ewm(span=21, adjust=False).mean()
            
        # Determine trend
        df['trend'] = np.where(
            df['ma_short'] > df['ma_long'], 'up',
            np.where(df['ma_short'] < df['ma_long'], 'down', 'neutral')
        )
        
        # Combine with BB data
        df = pd.concat([df, bb_df], axis=1)
        
        return df
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the optimized BB Squeeze indicator.
        
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
        df['trailing_stop'] = np.nan
        
        # Track the squeeze state
        squeeze_length = 0
        was_in_squeeze = False
        
        for i in range(1, len(df)):
            current_close = df['close'].iloc[i]
            current_atr = df['atr'].iloc[i]
            current_trend = df['trend'].iloc[i]
            
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
                    
                    # Check volume confirmation if available
                    volume_confirmed = True
                    if self.params["use_volume_filter"] and 'volume_ratio' in df.columns:
                        volume_confirmed = df['volume_ratio'].iloc[i] > self.params["volume_threshold"]
                    
                    # Generate signals based on momentum, RSI, trend and volume
                    if (momentum > self.params["momentum_threshold"] and 
                        rsi > self.params["rsi_entry_threshold"] and 
                        volume_confirmed and
                        (current_trend == 'up' or not self.params["is_higher_timeframe"])):
                        # Bullish breakout
                        df.loc[df.index[i], 'signal'] = 1
                        df.loc[df.index[i], 'entry_price'] = current_close
                        
                        # Calculate stop loss and take profit levels
                        stop_distance = current_atr * self.params["stop_loss_atr_factor"]
                        df.loc[df.index[i], 'stop_loss'] = current_close - stop_distance
                        df.loc[df.index[i], 'take_profit'] = current_close + (stop_distance * 1.5)
                        df.loc[df.index[i], 'trailing_stop'] = current_close - stop_distance
                        
                    elif (momentum < -self.params["momentum_threshold"] and 
                          rsi < self.params["rsi_entry_threshold"] and 
                          volume_confirmed and
                          (current_trend == 'down' or not self.params["is_higher_timeframe"])):
                        # Bearish breakout
                        df.loc[df.index[i], 'signal'] = -1
                        df.loc[df.index[i], 'entry_price'] = current_close
                        
                        # Calculate stop loss and take profit levels
                        stop_distance = current_atr * self.params["stop_loss_atr_factor"]
                        df.loc[df.index[i], 'stop_loss'] = current_close + stop_distance
                        df.loc[df.index[i], 'take_profit'] = current_close - (stop_distance * 1.5)
                        df.loc[df.index[i], 'trailing_stop'] = current_close + stop_distance
                
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
            
        # Already in a position
        if self.state.in_position:
            return False, {}
            
        # Update state
        self.state.is_in_squeeze = current_bar['is_squeeze']
        self.state.squeeze_intensity = current_bar['squeeze_intensity']
        self.state.squeeze_momentum = current_bar['squeeze_momentum']
        self.state.rsi = current_bar['rsi']
        self.state.atr = current_bar['atr']
        self.state.last_signal_price = current_bar['close']
        
        if 'volume_trend' in current_bar:
            self.state.volume_trend = current_bar['volume_trend']
            
        self.state.current_trend = current_bar['trend']
        
        # Calculate position size (more conservative in crypto markets)
        position_size = self.calculate_position_size(
            current_bar['close'],
            stop_price=current_bar['stop_loss'],
            risk_pct=self.params["max_risk_pct"]
        )
        
        direction = 1 if current_signal > 0 else -1
        
        entry_params = {
            "direction": direction,
            "entry_price": current_bar['entry_price'],
            "position_size": position_size,
            "stop_loss": current_bar['stop_loss'],
            "take_profit": current_bar['take_profit']
        }
        
        # Update state for trade tracking
        self.state.in_position = True
        self.state.position_type = "long" if direction > 0 else "short"
        self.state.entry_price = current_bar['entry_price']
        self.state.stop_loss = current_bar['stop_loss']
        self.state.take_profit = current_bar['take_profit']
        self.state.trailing_stop = current_bar['trailing_stop']
        
        logger.info(f"BB Squeeze Optimized strategy: Entry signal generated - {entry_params}")
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
            
        if not self.state.in_position:
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
        
        # 1. Take profit hit
        if (direction > 0 and current_close >= self.state.take_profit) or \
           (direction < 0 and current_close <= self.state.take_profit):
            exit_reason = "take_profit"
            
        # 2. Stop loss hit
        elif (direction > 0 and current_close <= self.state.stop_loss) or \
             (direction < 0 and current_close >= self.state.stop_loss):
            exit_reason = "stop_loss"
            
        # 3. Trailing stop (if enabled)
        elif self.params["enable_trailing_stop"]:
            if direction > 0:  # Long position
                # Update trailing stop if price moves in our favor
                if current_close > self.state.entry_price:
                    new_trailing_stop = current_close - (current_bar['atr'] * self.params["trailing_stop_atr_factor"])
                    if new_trailing_stop > self.state.trailing_stop:
                        self.state.trailing_stop = new_trailing_stop
                
                # Check if trailing stop is hit
                if current_close < self.state.trailing_stop:
                    exit_reason = "trailing_stop"
                    
            else:  # Short position
                # Update trailing stop if price moves in our favor
                if current_close < self.state.entry_price:
                    new_trailing_stop = current_close + (current_bar['atr'] * self.params["trailing_stop_atr_factor"])
                    if new_trailing_stop < self.state.trailing_stop:
                        self.state.trailing_stop = new_trailing_stop
                
                # Check if trailing stop is hit
                if current_close > self.state.trailing_stop:
                    exit_reason = "trailing_stop"
            
        # 4. Momentum reversal
        if not exit_reason:
            # For long positions
            if direction > 0 and previous_momentum > 0 and current_momentum < 0:
                exit_reason = "momentum_reversal"
                
            # For short positions
            elif direction < 0 and previous_momentum < 0 and current_momentum > 0:
                exit_reason = "momentum_reversal"
            
        # If we have an exit reason, exit the trade
        if exit_reason:
            exit_params = {
                "exit_price": current_close,
                "reason": exit_reason
            }
            
            logger.info(f"BB Squeeze Optimized strategy: Exit signal generated - {exit_params}")
            
            # Reset position state
            self.state.in_position = False
            self.state.position_type = None
            self.state.entry_price = None
            self.state.stop_loss = None
            self.state.take_profit = None
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
            
        # Risk per unit calculation
        risk_per_unit = abs(price - stop_price)
        if risk_per_unit <= 0:
            return 0
            
        # Get account balance (should come from account management module)
        # Using placeholder value for now
        account_size = 10000  # This should come from account management module
        
        # Calculate risk amount
        risk_amount = account_size * risk_pct
        
        # Calculate position size
        position_size = risk_amount / risk_per_unit
        
        # Adjust position size for cryptocurrency volatility
        # For higher volatile markets, we reduce position size further
        if self.state.atr > 0 and price > 0:
            volatility_ratio = (self.state.atr / price) * 100  # Volatility as percentage of price
            
            # If volatility is high, reduce position size
            if volatility_ratio > 5:  # 5% daily volatility is high
                position_size = position_size * (5 / volatility_ratio)
        
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
            "trend": latest['trend'],
            "bb_upper": latest.get(f'BBU_{self.params["bb_period"]}_{self.params["bb_std_dev"]}', None),
            "bb_lower": latest.get(f'BBL_{self.params["bb_period"]}_{self.params["bb_std_dev"]}', None)
        }
        
        # Add volume information if available
        if 'volume_ratio' in latest:
            results["volume_ratio"] = latest['volume_ratio']
            results["volume_trend"] = latest['volume_trend']
        
        # Add position information if in a position
        if self.state.in_position:
            results["position"] = {
                "type": self.state.position_type,
                "entry_price": self.state.entry_price,
                "current_price": latest['close'],
                "stop_loss": self.state.stop_loss,
                "take_profit": self.state.take_profit,
                "trailing_stop": self.state.trailing_stop,
                "profit_pct": ((latest['close'] / self.state.entry_price - 1) * 100) 
                              if self.state.position_type == "long" 
                              else ((self.state.entry_price / latest['close'] - 1) * 100)
            }
        
        return results 