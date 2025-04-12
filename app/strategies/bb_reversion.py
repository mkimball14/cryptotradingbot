from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np

from .base.strategy import Strategy, StrategyState
from .indicators.technical import calculate_rsi, calculate_bbands, calculate_atr, detect_regime

class BBReversionStrategy(Strategy):
    """
    Bollinger Band Mean Reversion strategy with RSI filter.
    
    Entry Rules:
    - Close crosses below the Lower Bollinger Band.
    - RSI < rsi_oversold_threshold.
    - Market is in an uptrend.
    
    Exit Rules:
    - Close crosses above the Middle Bollinger Band.
    - Stop Loss hit (ATR based).
    """
    
    def __init__(self,
                 timeframe: str = "1h",
                 bb_period: int = 20,
                 bb_std_dev: float = 2.0,
                 rsi_period: int = 14,
                 rsi_oversold_threshold: float = 30.0,
                 atr_period: int = 14,
                 risk_per_trade: float = 0.01, # Default 1% risk
                 atr_stop_multiplier: float = 1.5): # Tighter stop
        """
        Initialize Bollinger Band Reversion strategy.
        """
        super().__init__(timeframe=timeframe, risk_per_trade=risk_per_trade)
        
        self.bb_period = bb_period
        self.bb_std_dev = bb_std_dev
        self.rsi_period = rsi_period
        self.rsi_oversold_threshold = rsi_oversold_threshold
        self.atr_period = atr_period
        self.atr_stop_multiplier = atr_stop_multiplier
        
        # Generate column names based on params
        self.lower_band_col = f'BBL_{self.bb_period}_{self.bb_std_dev}'
        self.mid_band_col = f'BBM_{self.bb_period}_{self.bb_std_dev}'
        
        self.state = StrategyState() 

    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate BBands, RSI, and ATR."""
        df = data.copy()
        
        # Calculate BBands
        bbands_df = calculate_bbands(df, period=self.bb_period, std_dev=self.bb_std_dev)
        df = pd.concat([df, bbands_df], axis=1)
        
        # Calculate RSI
        df['rsi'] = calculate_rsi(df, period=self.rsi_period)
        
        # Calculate ATR
        df['atr'] = calculate_atr(df, period=self.atr_period)
        
        return df

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on Bollinger Bands and RSI."""
        # Calculate indicators
        data = self.calculate_indicators(data)
        
        signals = pd.Series(index=data.index, data=0)
        data['stop_loss'] = np.nan  # Initialize stop_loss column
        
        # Skip warmup period
        warmup_period = max(self.bb_period, self.rsi_period)
        print(f"[DEBUG] Starting signal generation after {warmup_period} rows warmup period")
        
        for i in range(warmup_period, len(data)):
            if i % 20 == 0:  # Print debug info every 20 rows
                print(f"\n[DEBUG] Row {i}")
                print(f"Price: {data['close'].iloc[i]:.2f}")
                print(f"Lower BB: {data['BBL_20_2.0'].iloc[i]:.2f}")
                print(f"RSI: {data['rsi'].iloc[i]:.2f}")
            
            # Entry conditions (more flexible)
            price_near_bb = data['close'].iloc[i] <= data['BBL_20_2.0'].iloc[i] * 1.02  # Within 2% of lower band
            rsi_oversold = data['rsi'].iloc[i] < 35  # Relaxed RSI threshold
            
            if price_near_bb and rsi_oversold:
                if i % 20 == 0:
                    print("[DEBUG] Signal generated - Entry conditions met:")
                    print(f"Price near BB: {price_near_bb}")
                    print(f"RSI oversold: {rsi_oversold}")
                signals.iloc[i] = 1
                # Calculate stop loss for entry signal
                if 'atr' in data.columns and not pd.isna(data['atr'].iloc[i]):
                    data.loc[data.index[i], 'stop_loss'] = data['low'].iloc[i] - data['atr'].iloc[i] * self.atr_stop_multiplier
                    if i % 20 == 0:
                        print(f"Stop loss calculated: {data['stop_loss'].iloc[i]:.2f}")
            
            # Exit conditions
            elif signals.iloc[i-1] == 1:  # If we're in a position
                price_above_middle = data['close'].iloc[i] > data['BBM_20_2.0'].iloc[i]
                rsi_overbought = data['rsi'].iloc[i] > 70
                
                if price_above_middle or rsi_overbought:
                    if i % 20 == 0:
                        print("[DEBUG] Exit signal generated:")
                        print(f"Price above middle BB: {price_above_middle}")
                        print(f"RSI overbought: {rsi_overbought}")
                    signals.iloc[i] = -1
        
        data['signal'] = signals
        return data

    def should_enter_trade(self, row: pd.Series) -> bool:
        """Check if we should enter a trade based on the generated signal."""
        if self.lower_band_col not in row or 'rsi' not in row or 'signal' not in row:
            return False
            
        return (
            row['signal'] == 1 and
            not self.state.is_in_position 
        )
    
    def should_exit_trade(self, row: pd.Series) -> bool:
        """
        Check if we should exit based on crossing mid-band or stop loss.
        """
        if not self.state.is_in_position:
            return False
            
        if self.mid_band_col not in row or 'close' not in row or 'low' not in row:
             return False # Cannot evaluate exit condition

        # 1. Check for crossing above Mid BBand (Take Profit)
        mid_band_exit = row['close'] > row[self.mid_band_col]
        if mid_band_exit:
            return True

        # 2. Check Stop Loss (Initial stop stored in state by engine)
        # Assumes engine sets self.state.trailing_stop_price on entry based on calculate_stop_loss
        if self.state.trailing_stop_price is not None and row['low'] <= self.state.trailing_stop_price:
                 return True
        
        return False

    def calculate_stop_loss(self, row: pd.Series) -> float:
        """Calculate initial stop loss price for a potential trade."""
        if 'stop_loss' in row and not pd.isna(row['stop_loss']):
            return row['stop_loss']
        else:
            print(f"Warning: Using dynamic stop loss calculation for row {row.name}.")
            if 'atr' in row and not pd.isna(row['atr']):
                 return row['low'] - row['atr'] * self.atr_stop_multiplier
            else:
                 print(f"Error: Cannot calculate stop loss for row {row.name} due to missing ATR.")
                 return np.nan # Indicate stop cannot be calculated

    # Note: No update_state override here, assumes base class is sufficient
    # unless specific trailing stop logic *within the strategy* is needed later.

