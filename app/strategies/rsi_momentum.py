from typing import Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
import logging
import pandas_ta as ta # Using pandas_ta for convenience
from collections import deque

from .base.strategy import Strategy, StrategyState
from .indicators.technical import calculate_rsi, detect_regime, calculate_atr, calculate_ma

logger = logging.getLogger(__name__)

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
                 atr_stop_multiplier: float = 2.0,
                 product_id: str = "",
                 config: Optional[Dict] = None):
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
        
        self.config = config or {}
        self.product_id = product_id
        
        # Explicitly assign strategy parameters from config or use defaults
        # Ensure type conversion if necessary (e.g., period to int)
        self.rsi_period = int(self.config.get("rsi_period", 14))
        self.oversold_threshold = self.config.get("oversold_threshold", 30)
        self.overbought_threshold = self.config.get("overbought_threshold", 70)
        self.signal_threshold = self.config.get("signal_threshold", 50)
        self.trade_size = self.config.get("trade_size", 0.01)

        # State Variables
        # Use the assigned rsi_period for maxlen calculation
        self.price_history = deque(maxlen=self.rsi_period + 5)
        self.current_rsi: Optional[float] = None
        self.in_position: bool = False # Track if we are currently holding the base asset
        
        logger.info(
            f"Initialized RSIMomentumStrategy for {self.product_id} with config: "
            f"Period={self.rsi_period}, OS={self.oversold_threshold}, OB={self.overbought_threshold}, TradeSize={self.trade_size}"
        )
    
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
        
        # --- Entry Signal Logic ---
        entry_condition = (
            (df['rsi'] > self.rsi_entry_threshold) &
            (df['rsi'].shift(1) <= self.rsi_entry_threshold) &
            (df['regime'] == "uptrend")
        )
        df.loc[entry_condition, 'signal'] = 1
        
        # --- Exit Signal Logic ---
        # Condition 1: RSI crosses BELOW the exit threshold
        rsi_cross_below_exit = (
            (df['rsi'] < self.rsi_exit_threshold) &
            (df['rsi'].shift(1) >= self.rsi_exit_threshold) 
        )
        # Condition 2: Regime changes to downtrend
        regime_downtrend = (df['regime'] == "downtrend")

        exit_condition = ( rsi_cross_below_exit | regime_downtrend )
        
        # Generate exit signal (-1) only on the first bar the condition is met after being in a trade
        # NOTE: This exit logic doesn't account for the trailing stop; that's checked in should_exit_trade during simulation.
        # We might simplify signal generation further later if needed.
        # Find bars where we *were* in a trade (signal was 1 previously) and the exit condition is now met
        # Need to handle the state properly - how do we know if we were in a trade based *only* on the dataframe?
        # The original logic used df['signal'].shift(1) == 1, which isn't quite right as signal represents *entry* signal.
        # Backtesting loop manages actual position state. Here, we just flag *potential* exit points.
        # Let's flag any bar where the exit condition is met. The backtest loop will decide based on actual position status.
        df.loc[exit_condition, 'signal'] = -1 # Mark potential exit points

        # --- Reconcile signals ---
        # If an entry and exit signal occur on the same bar (e.g., RSI crosses > 60 then < 40 immediately), prioritize exit? Or hold?
        # For now, let's assume entry takes precedence if both conditions met simultaneously (unlikely with crossover logic).
        # Overwrite exit signal if entry condition is also met on the same bar
        df.loc[entry_condition, 'signal'] = 1 
                
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

    def _calculate_rsi(self) -> Optional[float]:
        """Calculates RSI using pandas_ta based on the price history."""
        if len(self.price_history) < self.rsi_period:
            # Not enough data yet
            return None
        
        try:
            # Convert deque to pandas Series
            prices = pd.Series(list(self.price_history), dtype=float)
            # Calculate RSI
            rsi_series = ta.rsi(prices, length=self.rsi_period)
            if rsi_series is not None and not rsi_series.empty:
                # Get the latest RSI value
                latest_rsi = rsi_series.iloc[-1]
                return float(latest_rsi) if pd.notna(latest_rsi) else None
            else:
                return None
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return None

    def process_market_data(self, data: Dict[str, Any]) -> Optional[Dict]:
        """
        Processes incoming market data (ticker) and generates trade signals.

        Args:
            data (Dict[str, Any]): The market data message (expecting ticker type).

        Returns:
            Optional[Dict]: An action dictionary (e.g., {'action': 'BUY', ...}) or None.
        """
        message_type = data.get('type')
        
        # --- State Update from Order Fills --- 
        if message_type == 'user_order_update':
            # Only process fills for this strategy's product
            if data.get('product_id') == self.product_id:
                order_status = data.get('status')
                order_side = data.get('side')
                
                # If a BUY order was filled, we are now in position
                if order_status == "FILLED" and order_side == "BUY":
                    if not self.in_position:
                        logger.info(f"Strategy [{self.product_id}]: Received BUY fill notification. Updating state to IN POSITION.")
                        self.in_position = True
                    else:
                        logger.warning(f"Strategy [{self.product_id}]: Received BUY fill notification, but already in position.")
                # If a SELL order was filled, we are now out of position
                elif order_status == "FILLED" and order_side == "SELL":
                    if self.in_position:
                        logger.info(f"Strategy [{self.product_id}]: Received SELL fill notification. Updating state to OUT OF POSITION.")
                        self.in_position = False
                    else:
                        logger.warning(f"Strategy [{self.product_id}]: Received SELL fill notification, but already out of position.")
                # Handle other closed statuses (optional, maybe just log)
                elif order_status in ["CANCELLED", "EXPIRED", "FAILED"]:
                     logger.info(f"Strategy [{self.product_id}]: Received non-fill order closure: {order_status}")
                     # Decide if state needs changing (e.g., failed BUY means not in position)
                     # For simplicity, we only change state on FILLED for now.
            return None # No trade signal generated from order updates

        # --- Signal Generation from Ticker Data --- 
        elif message_type == 'ticker':
            if data.get('product_id') != self.product_id:
                # Ignore tickers for other products
                return None

            price_str = data.get('price')
            if not price_str:
                logger.warning("Ticker message missing price.")
                return None

            try:
                current_price = float(price_str)
                self.price_history.append(current_price)
                
                # Store previous RSI for crossover detection
                previous_rsi = self.current_rsi
                self.current_rsi = self._calculate_rsi()

                if self.current_rsi is None or previous_rsi is None:
                    logger.debug("RSI not calculated yet or insufficient data.")
                    return None

                logger.info(f"Strategy [{self.product_id}]: Price={current_price:.2f}, RSI={self.current_rsi:.2f}, InPosition={self.in_position}")
                
                # --- RSI Momentum Logic --- 
                signal = None
                # Simplified Buy Signal: RSI is in oversold region and we are not in position
                if not self.in_position and self.current_rsi <= self.oversold_threshold:
                    logger.info(f"BUY SIGNAL: RSI ({self.current_rsi:.2f}) <= Oversold ({self.oversold_threshold}).")
                    signal = {
                        'action': 'BUY',
                        'type': 'MARKET', # Or 'LIMIT' with calculated price
                        'size': self.trade_size, # NOTE: For MARKET BUY, this needs to be QUOTE size!
                        'product_id': self.product_id
                        # Add price if LIMIT order
                    }
                    # DO NOT change self.in_position here - wait for user_order_update confirmation

                # Simplified Sell Signal: RSI is in overbought region and we are in position
                elif self.in_position and self.current_rsi >= self.overbought_threshold:
                    logger.info(f"SELL SIGNAL: RSI ({self.current_rsi:.2f}) >= Overbought ({self.overbought_threshold}).")
                    signal = {
                        'action': 'SELL',
                        'type': 'MARKET', # Or 'LIMIT'
                        'size': self.trade_size, # Size in BASE currency for MARKET SELL / LIMIT
                        'product_id': self.product_id
                        # Add price if LIMIT order
                    }
                    # DO NOT change self.in_position here - wait for user_order_update confirmation
                # ---------------------------
                
                return signal

            except ValueError:
                logger.error(f"Could not convert price '{price_str}' to float.")
                return None
            except Exception as e:
                logger.error(f"Error processing ticker data: {e}", exc_info=True)
                return None
        else:
            # Ignore other message types for now
            return None 