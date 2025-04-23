"""
Custom Portfolio class with enhanced functionality for trading strategies.

Extends vectorbt's Portfolio class to add support for:
- Stop loss (percentage-based)
- Take profit (percentage-based)
"""

import numpy as np
import pandas as pd
from typing import Optional, Union, Tuple, Dict, Any, List
import vectorbtpro as vbt
import logging

# Setup logger
logger = logging.getLogger(__name__)

class CustomPortfolio:
    """Extended Portfolio class with stop-loss and take-profit functionality.
    
    Uses vectorbtpro.Portfolio and adds support for:
    - Stop loss (percentage-based)
    - Take profit (percentage-based)
    
    Usage is identical to vectorbtpro.Portfolio.from_signals or from_orders
    with added parameters for stop_loss and take_profit.
    """
    
    @classmethod
    def from_signals(cls, 
                    close: Union[pd.Series, pd.DataFrame],
                    entries: Union[pd.Series, pd.DataFrame], 
                    exits: Union[pd.Series, pd.DataFrame] = None,
                    **kwargs) -> "vbt.Portfolio":
        """Create a Portfolio from entry and exit signals with SL/TP support.
        
        Parameters are identical to vectorbtpro.Portfolio.from_signals with additional:
        
        Args:
            close: Price series for valuation of assets
            entries: Entry signals (True for entry)
            exits: Exit signals (True for exit)
            **kwargs: Additional parameters for Portfolio.from_signals
                stop_loss: Optional[float] - Stop loss percentage (e.g., 0.05 for 5%)
                take_profit: Optional[float] - Take profit percentage (e.g., 0.1 for 10%)
                
        Returns:
            vbt.Portfolio instance
        """
        # Extract SL/TP parameters
        stop_loss = kwargs.pop('stop_loss', None)
        take_profit = kwargs.pop('take_profit', None)
        
        # If no SL/TP, just use regular Portfolio.from_signals
        if stop_loss is None and take_profit is None:
            return vbt.Portfolio.from_signals(close, entries, exits, **kwargs)
        
        # Process SL/TP
        processed_entries, processed_exits = cls._process_sl_tp(
            close=close,
            entries=entries,
            exits=exits,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        
        # Create portfolio using processed signals
        return vbt.Portfolio.from_signals(
            close, 
            processed_entries, 
            processed_exits, 
            **kwargs
        )
    
    @classmethod
    def _process_sl_tp(cls,
                      close: Union[pd.Series, pd.DataFrame],
                      entries: Union[pd.Series, pd.DataFrame],
                      exits: Optional[Union[pd.Series, pd.DataFrame]] = None,
                      stop_loss: Optional[float] = None,
                      take_profit: Optional[float] = None) -> Tuple[Union[pd.Series, pd.DataFrame], Union[pd.Series, pd.DataFrame]]:
        """Process signals to implement stop-loss and take-profit.
        
        Args:
            close: Price series
            entries: Entry signals
            exits: Exit signals
            stop_loss: Stop loss percentage (0.05 = 5%)
            take_profit: Take profit percentage (0.1 = 10%)
            
        Returns:
            Tuple of processed (entries, exits)
        """
        # Handle case where no SL/TP
        if stop_loss is None and take_profit is None:
            return entries, exits
        
        # If exits is None, create empty signals
        if exits is None:
            exits = pd.Series(False, index=close.index)
            if isinstance(entries, pd.DataFrame) and isinstance(close, pd.Series):
                # Broadcast to match entries
                exits = pd.DataFrame(False, index=close.index, columns=entries.columns)
            elif isinstance(entries, pd.DataFrame) and isinstance(close, pd.DataFrame):
                # Match the broadcast that entries would get
                exits = pd.DataFrame(False, index=close.index, columns=entries.columns)
        
        # Convert to pandas if numpy
        if not isinstance(close, (pd.Series, pd.DataFrame)):
            close = pd.Series(close)
        if not isinstance(entries, (pd.Series, pd.DataFrame)):
            entries = pd.Series(entries, index=close.index)
        if not isinstance(exits, (pd.Series, pd.DataFrame)):
            exits = pd.Series(exits, index=close.index)
            
        # Work with both Series and DataFrame
        if isinstance(entries, pd.Series) and isinstance(close, pd.Series):
            return cls._process_sl_tp_series(close, entries, exits, stop_loss, take_profit)
        elif isinstance(entries, pd.DataFrame) or isinstance(close, pd.DataFrame):
            return cls._process_sl_tp_frame(close, entries, exits, stop_loss, take_profit)
        else:
            raise TypeError("Unsupported types for close, entries, or exits")
    
    @classmethod
    def _process_sl_tp_series(cls,
                             close: pd.Series,
                             entries: pd.Series,
                             exits: pd.Series,
                             stop_loss: Optional[float] = None,
                             take_profit: Optional[float] = None) -> Tuple[pd.Series, pd.Series]:
        """Process signals for a single asset/column.
        
        Args:
            close: Price series
            entries: Entry signals
            exits: Exit signals
            stop_loss: Stop loss percentage
            take_profit: Take profit percentage
            
        Returns:
            Tuple of processed (entries, exits)
        """
        processed_exits = exits.copy()
        
        # Find entry points
        entry_idx = entries[entries].index
        if len(entry_idx) == 0:
            return entries, processed_exits  # No entries, nothing to process
        
        for i, entry_time in enumerate(entry_idx):
            # Get entry price
            entry_price = close.loc[entry_time]
            
            # Calculate SL/TP levels
            sl_price = entry_price * (1 - stop_loss) if stop_loss is not None else None
            tp_price = entry_price * (1 + take_profit) if take_profit is not None else None
            
            # Find next entry or end of data
            next_entry_idx = entry_idx[i+1] if i < len(entry_idx) - 1 else close.index[-1]
            
            # Slice of prices after entry until next entry
            price_slice = close.loc[entry_time:next_entry_idx]
            
            # Apply SL/TP
            for time, price in price_slice.items():
                if time == entry_time:
                    continue  # Skip entry candle
                    
                # Check if SL or TP hit
                sl_hit = sl_price is not None and price <= sl_price
                tp_hit = tp_price is not None and price >= tp_price
                
                if sl_hit or tp_hit:
                    processed_exits.loc[time] = True
                    break  # Exit position
                    
                # If regular exit already present, stop processing
                if exits.loc[time]:
                    break
                
        return entries, processed_exits
    
    @classmethod
    def _process_sl_tp_frame(cls,
                            close: Union[pd.Series, pd.DataFrame],
                            entries: Union[pd.Series, pd.DataFrame],
                            exits: Union[pd.Series, pd.DataFrame],
                            stop_loss: Optional[float] = None,
                            take_profit: Optional[float] = None) -> Tuple[Union[pd.Series, pd.DataFrame], Union[pd.Series, pd.DataFrame]]:
        """Process signals for multiple assets/columns.
        
        Handles various combinations of Series/DataFrame for close, entries, and exits.
        
        Args:
            close: Price Series or DataFrame
            entries: Entry signals Series or DataFrame
            exits: Exit signals Series or DataFrame
            stop_loss: Stop loss percentage
            take_profit: Take profit percentage
            
        Returns:
            Tuple of processed (entries, exits)
        """
        # Normalize to ensure we have DataFrames with aligned columns
        if isinstance(close, pd.Series):
            close = pd.DataFrame({0: close})
            if isinstance(entries, pd.Series):
                entries = pd.DataFrame({0: entries})
            if isinstance(exits, pd.Series):
                exits = pd.DataFrame({0: exits})
        elif isinstance(close, pd.DataFrame):
            if isinstance(entries, pd.Series):
                entries = pd.DataFrame({col: entries for col in close.columns})
            if isinstance(exits, pd.Series):
                exits = pd.DataFrame({col: exits for col in close.columns})
                
        # Ensure columns are aligned
        common_columns = entries.columns.intersection(close.columns).intersection(exits.columns)
        entries = entries[common_columns]
        close = close[common_columns]
        exits = exits[common_columns]
        
        processed_exits = exits.copy()
        
        # Process each column
        for col in common_columns:
            entries_col = entries[col]
            exits_col = exits[col]
            close_col = close[col]
            
            _, processed_exits_col = cls._process_sl_tp_series(
                close_col, entries_col, exits_col, 
                stop_loss, take_profit
            )
            
            processed_exits[col] = processed_exits_col
            
        return entries, processed_exits
    
    @staticmethod
    def get_trades_df(portfolio: "vbt.Portfolio") -> pd.DataFrame:
        """Helper method to get trades DataFrame with more readable format.
        
        Args:
            portfolio: Portfolio instance
            
        Returns:
            DataFrame with trade information
        """
        # Get the trades
        trades = portfolio.trades
        
        # Create a dictionary of data
        data = {}
        
        # Map field names
        field_mapping = {
            'Entry Time': 'entry_idx',
            'Exit Time': 'exit_idx',
            'Entry Price': 'entry_price',
            'Exit Price': 'exit_price',
            'PnL': 'pnl',
            'Return': 'return_',
            'Size': 'size',
            'Direction': 'direction',
            'Status': 'status',
            'Position Index': 'col'
        }
        
        # Extract data for each field
        for display_name, field_name in field_mapping.items():
            if hasattr(trades, field_name):
                value = getattr(trades, field_name)
                # MappedArray objects have a .values property
                if hasattr(value, 'values'):
                    data[display_name] = value.values
        
        # Create DataFrame
        trades_df = pd.DataFrame(data)
        
        # Convert index timestamps to datetime if available
        if hasattr(portfolio, 'wrapper') and hasattr(portfolio.wrapper, 'index'):
            idx = portfolio.wrapper.index
            if 'Entry Time' in trades_df.columns:
                trades_df['Entry Time'] = trades_df['Entry Time'].apply(
                    lambda x: idx[int(x)] if isinstance(x, (int, np.integer)) and 0 <= int(x) < len(idx) else x
                )
            if 'Exit Time' in trades_df.columns:
                trades_df['Exit Time'] = trades_df['Exit Time'].apply(
                    lambda x: idx[int(x)] if isinstance(x, (int, np.integer)) and 0 <= int(x) < len(idx) else x
                )
                        
        return trades_df