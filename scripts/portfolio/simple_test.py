"""
Simple test script for CustomPortfolio
"""

import numpy as np
import pandas as pd
import vectorbtpro as vbt
import logging
from scripts.portfolio.custom_portfolio import CustomPortfolio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run a simple test of CustomPortfolio"""
    logger.info("Testing CustomPortfolio class with simple example...")
    
    # Create sample data
    n = 100
    price = pd.Series(np.random.normal(100, 5, n).cumsum() + 1000)
    price.index = pd.date_range('2020-01-01', periods=n)
    
    # Create simple entry/exit signals
    entries = pd.Series(False, index=price.index)
    exits = pd.Series(False, index=price.index)
    
    # Set a few entry/exit points
    entries.iloc[10] = True  # Buy after 10 days
    entries.iloc[50] = True  # Buy after 50 days
    exits.iloc[30] = True    # Sell after 30 days
    exits.iloc[80] = True    # Sell after 80 days
    
    try:
        # Test basic functionality (no SL/TP)
        logger.info("Testing basic functionality...")
        pf = CustomPortfolio.from_signals(
            close=price,
            entries=entries,
            exits=exits,
            size=1.0,
            fees=0.001,
            freq='1D'
        )
        
        # Print basic stats
        logger.info(f"Total return: {pf.total_return:.2%}")
        logger.info(f"Number of trades: {len(pf.trades)}")
        
        # Test with SL/TP
        logger.info("Testing with stop-loss and take-profit...")
        pf_sltp = CustomPortfolio.from_signals(
            close=price,
            entries=entries,
            exits=exits,
            size=1.0,
            fees=0.001,
            freq='1D',
            stop_loss=0.05,     # 5% stop loss
            take_profit=0.10    # 10% take profit
        )
        
        # Print basic stats
        logger.info(f"Total return with SL/TP: {pf_sltp.total_return:.2%}")
        logger.info(f"Number of trades with SL/TP: {len(pf_sltp.trades)}")
        
        logger.info("All tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main() 