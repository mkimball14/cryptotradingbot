import pandas as pd
import numpy as np
import vectorbtpro as vbt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create sample data
def create_test_data(size=100):
    """Create simple test data with random entries/exits."""
    dates = pd.date_range('2020-01-01', periods=size, freq='D')
    close = np.linspace(100, 200, size)
    
    # Create random entries and exits
    rng = np.random.default_rng(42)
    entries = rng.random(size) > 0.9  # Randomly true about 10% of the time
    exits = np.zeros_like(entries)
    
    # Create exits after entries
    for i in range(1, size):
        if entries[i-1] and not exits[i-1]:
            exits[i] = rng.random() > 0.7  # 30% chance of exit after entry
    
    return pd.DataFrame({
        'close': close,
        'entries': entries,
        'exits': exits
    }, index=dates)

def test_portfolio_creation():
    """Test various portfolio creation methods and parameter formats."""
    df = create_test_data(100)
    
    # Test 1: Basic portfolio creation without stop-loss/take-profit
    logger.info("Test 1: Basic portfolio creation")
    try:
        pf1 = vbt.Portfolio.from_signals(
            close=df['close'],
            entries=df['entries'],
            exits=df['exits'],
            size=1.0,
            fees=0.001,
            freq='1D'
        )
        logger.info("Test 1 PASSED")
    except Exception as e:
        logger.error(f"Test 1 FAILED: {str(e)}")
    
    # Test 2: With stop-loss as float scalar
    logger.info("Test 2: With stop-loss as float scalar")
    try:
        pf2 = vbt.Portfolio.from_signals(
            close=df['close'],
            entries=df['entries'],
            exits=df['exits'],
            size=1.0,
            fees=0.001,
            freq='1D',
            stop_loss=0.05
        )
        logger.info("Test 2 PASSED")
    except Exception as e:
        logger.error(f"Test 2 FAILED: {str(e)}")
    
    # Test 3: With stop-loss as array of floats
    logger.info("Test 3: With stop-loss as array of floats")
    try:
        pf3 = vbt.Portfolio.from_signals(
            close=df['close'],
            entries=df['entries'],
            exits=df['exits'],
            size=1.0,
            fees=0.001,
            freq='1D',
            stop_loss=np.full(len(df), 0.05)
        )
        logger.info("Test 3 PASSED")
    except Exception as e:
        logger.error(f"Test 3 FAILED: {str(e)}")
    
    # Test 4: With stop-loss and take-profit as float scalars
    logger.info("Test 4: With stop-loss and take-profit as float scalars")
    try:
        pf4 = vbt.Portfolio.from_signals(
            close=df['close'],
            entries=df['entries'],
            exits=df['exits'],
            size=1.0,
            fees=0.001,
            freq='1D',
            stop_loss=0.05,
            take_profit=0.1
        )
        logger.info("Test 4 PASSED")
    except Exception as e:
        logger.error(f"Test 4 FAILED: {str(e)}")
    
    # Test 5: With stop-loss and take-profit as arrays of floats
    logger.info("Test 5: With stop-loss and take-profit as arrays of floats")
    try:
        pf5 = vbt.Portfolio.from_signals(
            close=df['close'],
            entries=df['entries'],
            exits=df['exits'],
            size=1.0,
            fees=0.001,
            freq='1D',
            stop_loss=np.full(len(df), 0.05),
            take_profit=np.full(len(df), 0.1)
        )
        logger.info("Test 5 PASSED")
    except Exception as e:
        logger.error(f"Test 5 FAILED: {str(e)}")
    
    # Test 6: With entries and exits as numpy boolean arrays
    logger.info("Test 6: With entries and exits as numpy boolean arrays")
    try:
        pf6 = vbt.Portfolio.from_signals(
            close=df['close'],
            entries=df['entries'].to_numpy().astype(np.bool_),
            exits=df['exits'].to_numpy().astype(np.bool_),
            size=1.0,
            fees=0.001,
            freq='1D',
            stop_loss=0.05,
            take_profit=0.1
        )
        logger.info("Test 6 PASSED")
    except Exception as e:
        logger.error(f"Test 6 FAILED: {str(e)}")
        
    # Test 7: Using take_profit_stop=True explicitly
    logger.info("Test 7: Using take_profit_stop=True explicitly")
    try:
        pf7 = vbt.Portfolio.from_signals(
            close=df['close'],
            entries=df['entries'].to_numpy().astype(np.bool_),
            exits=df['exits'].to_numpy().astype(np.bool_),
            size=1.0,
            fees=0.001,
            freq='1D',
            stop_loss=0.05,
            take_profit=0.1,
            stop_type='price', # try using price-based stops
            stop_loss_type='price',
            take_profit_type='price'
        )
        logger.info("Test 7 PASSED")
    except Exception as e:
        logger.error(f"Test 7 FAILED: {str(e)}")
        
    # Print which tests passed and which failed
    logger.info("Test summary complete")

if __name__ == "__main__":
    logger.info("Starting portfolio creation tests")
    test_portfolio_creation()
    logger.info("Tests complete") 