import pandas as pd
import numpy as np
import logging
import vectorbtpro as vbt
import sys
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data.data_fetcher import fetch_historical_data

def generate_simple_signals(data, lookback=20):
    """Generate simple signals for testing"""
    close = data['close']
    sma_short = close.rolling(lookback).mean()
    sma_long = close.rolling(lookback*2).mean()
    
    # Generate simple crossover signals
    entries = (sma_short > sma_long) & (sma_short.shift() <= sma_long.shift())
    exits = (sma_short < sma_long) & (sma_short.shift() >= sma_long.shift())
    
    return entries, exits

def create_test_portfolio(data, entries, exits):
    """Create a test portfolio using vectorbt"""
    try:
        # Create portfolio
        portfolio = vbt.Portfolio.from_signals(
            close=data['close'],
            entries=entries,
            exits=exits,
            size=1.0,  # Fixed size of 1 unit per trade
            init_cash=10000,
            fees=0.001,
            slippage=0.0005
        )
        return portfolio
    except Exception as e:
        logger.error(f"Error creating portfolio: {e}")
        return None

def inspect_trades_structure(portfolio):
    """Inspect the trades structure to understand how to access data properly"""
    if portfolio is None or not hasattr(portfolio, 'trades'):
        logger.error("Portfolio has no trades attribute")
        return
    
    trades = portfolio.trades
    
    # Print basic info
    logger.info(f"Trades type: {type(trades)}")
    logger.info(f"Trades has {len(trades)} records")
    
    # Try different ways to access trade information
    try:
        # Method 1: Convert to DataFrame
        logger.info("Method 1: Converting trades to DataFrame")
        trades_df = trades.records_readable
        logger.info(f"Trades DataFrame shape: {trades_df.shape}")
        logger.info(f"Trades DataFrame columns: {trades_df.columns.tolist()}")
        
        # Handle both 'pnl' and 'PnL' column names
        pnl_col = None
        if 'PnL' in trades_df.columns:
            pnl_col = 'PnL'
            logger.info("Found PnL column (uppercase)")
        elif 'pnl' in trades_df.columns:
            pnl_col = 'pnl'
            logger.info("Found pnl column (lowercase)")
        else:
            logger.warning("No PnL or pnl column found, cannot calculate metrics")
            
        if pnl_col is not None:
            # Calculate metrics manually
            winning_trades = trades_df[trades_df[pnl_col] > 0]
            losing_trades = trades_df[trades_df[pnl_col] <= 0]
            
            logger.info(f"Winning trades: {len(winning_trades)}")
            logger.info(f"Losing trades: {len(losing_trades)}")
            logger.info(f"Win rate: {len(winning_trades) / len(trades_df) if len(trades_df) > 0 else 0:.2f}")
            
            # Calculate profit factor
            total_profit = winning_trades[pnl_col].sum() if len(winning_trades) > 0 else 0
            total_loss = abs(losing_trades[pnl_col].sum()) if len(losing_trades) > 0 else 0
            profit_factor = total_profit / total_loss if total_loss > 0 else (1.0 if total_profit > 0 else 0.0)
            logger.info(f"Profit factor: {profit_factor:.2f}")
        
    except Exception as e:
        logger.error(f"Method 1 failed: {e}")
    
    try:
        # Method 2: Use trades properties directly
        logger.info("Method 2: Using trades properties directly")
        
        # List available attributes and methods
        attrs = [attr for attr in dir(trades) if not attr.startswith('_')]
        logger.info(f"Available trade attributes: {sorted(attrs)}")
        
        # Access key properties
        if hasattr(trades, 'count'):
            logger.info(f"Trade count: {trades.count}")
        
        if hasattr(trades, 'win_rate'):
            logger.info(f"Win rate: {trades.win_rate:.2f}")
        
        if hasattr(trades, 'profit_factor'):
            logger.info(f"Profit factor: {trades.profit_factor:.2f}")
            
    except Exception as e:
        logger.error(f"Method 2 failed: {e}")
    
    # Provide recommended approach for accessing trades data
    logger.info("\nRECOMMENDED APPROACH:")
    try:
        recommended_code = """
        # Convert to records if needed
        if hasattr(trades, 'records_readable'):
            trades_df = trades.records_readable
            
            # Handle both 'pnl' and 'PnL' column names
            pnl_col = None
            if 'PnL' in trades_df.columns:
                pnl_col = 'PnL'
            elif 'pnl' in trades_df.columns:
                pnl_col = 'pnl'
            
            if pnl_col is not None:
                winning_trades = trades_df[trades_df[pnl_col] > 0]
                losing_trades = trades_df[trades_df[pnl_col] <= 0]
                
                # Calculate metrics
                win_rate = len(winning_trades) / len(trades_df) if len(trades_df) > 0 else 0
                total_profit = winning_trades[pnl_col].sum() if len(winning_trades) > 0 else 0
                total_loss = abs(losing_trades[pnl_col].sum()) if len(losing_trades) > 0 else 0
                profit_factor = total_profit / total_loss if total_loss > 0 else (1.0 if total_profit > 0 else 0.0)
        # Use properties directly if available
        elif hasattr(trades, 'win_rate') and hasattr(trades, 'profit_factor'):
            win_rate = trades.win_rate
            profit_factor = trades.profit_factor
        else:
            # Fallback method
            win_rate = 0.0
            profit_factor = 0.0
        """
        logger.info(recommended_code)
    except Exception as e:
        logger.error(f"Error showing recommended code: {e}")

def test_with_real_data():
    """Test with real market data"""
    # Fetch data
    try:
        logger.info("Fetching BTC-USD data")
        data = fetch_historical_data('BTC-USD', '2022-01-01', '2022-12-31', 86400)  # Daily data
        if data is None or data.empty:
            logger.error("Failed to fetch data")
            return
        
        logger.info(f"Data fetched successfully. Shape: {data.shape}")
        
        # Generate signals
        entries, exits = generate_simple_signals(data, lookback=20)
        logger.info(f"Generated {entries.sum()} entry signals and {exits.sum()} exit signals")
        
        # Create portfolio
        portfolio = create_test_portfolio(data, entries, exits)
        if portfolio is None:
            logger.error("Failed to create portfolio")
            return
        
        # Inspect trades structure
        inspect_trades_structure(portfolio)
        
        # Test the total_return access
        try:
            if callable(getattr(portfolio, 'total_return', None)):
                total_return = portfolio.total_return()
                logger.info(f"Total return (method): {total_return:.2%}")
            else:
                total_return = portfolio.total_return
                logger.info(f"Total return (property): {total_return:.2%}")
        except Exception as e:
            logger.error(f"Error accessing total_return: {e}")
            
    except Exception as e:
        logger.error(f"Test with real data failed: {e}")

if __name__ == "__main__":
    logger.info("Starting vectorbt trades test...")
    test_with_real_data()
    logger.info("Testing completed") 