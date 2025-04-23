"""
Debug script to understand the structure of trades in VectorBTPro
"""

import numpy as np
import pandas as pd
import vectorbtpro as vbt
import logging
import inspect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Debug trades properties"""
    # Generate sample data
    np.random.seed(42)
    price = pd.Series(np.random.randn(100).cumsum() + 100)
    price.index = pd.date_range('2020-01-01', periods=100)
    
    # Generate random entry/exit signals
    entries = pd.Series(False, index=price.index)
    entries.iloc[10] = True  # Buy at index 10
    entries.iloc[40] = True  # Buy at index 40
    
    exits = pd.Series(False, index=price.index)
    exits.iloc[30] = True  # Sell at index 30
    exits.iloc[60] = True  # Sell at index 60
    
    # Create portfolio
    pf = vbt.Portfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=10000,
        fees=0.001,
        freq='1D'
    )
    
    # Get trades
    trades = pf.trades
    
    # Log the trades type
    logger.info(f"Type of trades: {type(trades)}")
    
    # Log trades attributes
    attributes = dir(trades)
    logger.info(f"Attributes of trades: {[attr for attr in attributes if not attr.startswith('_')]}")
    
    # Log number of trades
    logger.info(f"Number of trades: {len(trades)}")
    
    # Check if trades is iterable
    try:
        for i, trade in enumerate(trades):
            logger.info(f"Trade {i}: {trade}")
            if i >= 2:  # Just show first 3 trades
                break
    except Exception as e:
        logger.error(f"Error iterating trades: {str(e)}")
    
    # Check if we can access trades by index
    try:
        logger.info(f"First trade: {trades[0]}")
    except Exception as e:
        logger.error(f"Error accessing trades by index: {str(e)}")
    
    # Inspect key properties
    for prop in ['entry_idx', 'exit_idx', 'entry_price', 'exit_price', 'pnl', 'return_', 'size', 'direction', 'status', 'col']:
        if hasattr(trades, prop):
            value = getattr(trades, prop)
            logger.info(f"Property '{prop}':")
            logger.info(f"  Type: {type(value)}")
            logger.info(f"  Shape/Length: {getattr(value, 'shape', len(value) if hasattr(value, '__len__') else 'N/A')}")
            
            # Try to convert to list or numpy array
            try:
                if hasattr(value, 'values'):
                    logger.info(f"  First few values (from .values): {value.values[:3]}")
                elif hasattr(value, 'to_numpy'):
                    logger.info(f"  First few values (from to_numpy): {value.to_numpy()[:3]}")
                elif hasattr(value, '__array__'):
                    logger.info(f"  First few values (from __array__): {np.asarray(value)[:3]}")
                else:
                    logger.info(f"  Could not convert to array")
            except Exception as e:
                logger.error(f"  Error converting to array: {str(e)}")
    
    # Try to create a DataFrame safely
    try:
        # Create a dictionary of data
        data = {}
        for prop in ['entry_idx', 'exit_idx', 'entry_price', 'exit_price', 'pnl', 'return_', 'status', 'col']:
            if hasattr(trades, prop):
                try:
                    # Try different methods to get values
                    value = getattr(trades, prop)
                    if hasattr(value, 'to_numpy'):
                        data[prop] = value.to_numpy()
                    elif hasattr(value, 'values'):
                        data[prop] = value.values
                    elif hasattr(value, '__array__'):
                        data[prop] = np.asarray(value)
                    else:
                        data[prop] = [getattr(trades, prop).iloc[i] for i in range(len(trades))]
                except Exception as e:
                    logger.error(f"Error getting values for {prop}: {str(e)}")
        
        df = pd.DataFrame(data)
        logger.info(f"Created DataFrame with keys: {df.columns.tolist()}")
        logger.info(f"DataFrame:\n{df.head()}")
    except Exception as e:
        logger.error(f"Error creating DataFrame: {str(e)}")
    
    return True

if __name__ == "__main__":
    main() 