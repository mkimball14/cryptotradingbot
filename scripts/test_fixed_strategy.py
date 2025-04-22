import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import logging
import vectorbtpro as vbt
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))
from data.data_fetcher import fetch_historical_data
from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy, calculate_performance_metrics

def test_edge_strategy():
    """Test the fixed Edge Multi-Factor Strategy implementation"""
    logger.info("Testing Edge Multi-Factor Strategy with PnL column name handling...")
    
    # Fetch test data
    symbol = 'BTC-USD'
    start_date = '2023-01-01'
    end_date = '2023-03-31'
    granularity = 86400  # 1 day
    
    logger.info(f"Fetching data for {symbol} from {start_date} to {end_date}...")
    price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    
    if price_data is None or price_data.empty:
        logger.error("Failed to fetch data. Exiting.")
        return
    
    logger.info(f"Data fetched successfully. Shape: {price_data.shape}")
    
    # Create strategy
    logger.info("Initializing EdgeMultiFactorStrategy...")
    strategy = EdgeMultiFactorStrategy(
        lookback_window=15,
        vol_filter_window=50,
        volatility_threshold=0.7,
        initial_capital=3000,
        default_factor_weights={
            'volatility_regime': 0.25,
            'consolidation_breakout': 0.25,
            'volume_divergence': 0.25,
            'market_microstructure': 0.25
        }
    )
    
    # Generate signals
    logger.info("Generating signals...")
    long_entries, short_entries, is_trending, is_ranging = strategy.generate_signals(price_data)
    
    logger.info(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries.")
    
    # Backtest the strategy
    logger.info("Backtesting the strategy...")
    portfolio, metrics = strategy.backtest_signals(long_entries, data=price_data)
    
    # Display metrics
    if portfolio is not None:
        logger.info("\nBacktest Results:")
        logger.info(f"Total Return: {metrics['total_return']:.2%}")
        logger.info(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        logger.info(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
        logger.info(f"Total Trades: {metrics['total_trades']}")
        logger.info(f"Win Rate: {metrics['win_rate']:.2%}")
        logger.info(f"Profit Factor: {metrics['profit_factor']:.2f}")
        
        # Test direct PnL column access
        logger.info("\nTesting PnL column access:")
        
        if hasattr(portfolio, 'trades') and hasattr(portfolio.trades, 'records_readable'):
            trades_df = portfolio.trades.records_readable
            logger.info(f"Columns in trades DataFrame: {trades_df.columns.tolist()}")
            
            # Check if PnL or pnl exists
            if 'PnL' in trades_df.columns:
                logger.info("Found 'PnL' column (uppercase)")
                pnl_col = 'PnL'
            elif 'pnl' in trades_df.columns:
                logger.info("Found 'pnl' column (lowercase)")
                pnl_col = 'pnl'
            else:
                logger.warning("No PnL column found in trades DataFrame")
                pnl_col = None
                
            if pnl_col:
                winning_trades = trades_df[trades_df[pnl_col] > 0]
                losing_trades = trades_df[trades_df[pnl_col] <= 0]
                
                logger.info(f"PnL summary:")
                logger.info(f"  Winning trades: {len(winning_trades)}")
                logger.info(f"  Losing trades: {len(losing_trades)}")
                logger.info(f"  Total profit: {winning_trades[pnl_col].sum():.2f}")
                logger.info(f"  Total loss: {abs(losing_trades[pnl_col].sum()):.2f}")
        
        # Test our generic performance metrics function directly
        logger.info("\nTesting generic performance metrics function:")
        direct_metrics = calculate_performance_metrics(portfolio)
        logger.info(f"Direct metrics calculation results:")
        for key, value in direct_metrics.items():
            logger.info(f"  {key}: {value}")
    else:
        logger.error("Backtest failed.")
    
    logger.info("Test completed successfully.")

if __name__ == "__main__":
    test_edge_strategy() 