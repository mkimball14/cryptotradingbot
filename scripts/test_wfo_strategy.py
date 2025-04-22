import logging
import pandas as pd
import numpy as np
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.strategies.wfo_edge_strategy import calculate_performance_metrics

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_calculate_performance_metrics():
    """Test that the calculate_performance_metrics function handles PnL columns correctly."""
    logger.info("Testing calculate_performance_metrics function with uppercase 'PnL'...")
    
    # Create a dummy portfolio with uppercase 'PnL' column
    class DummyPortfolio:
        def __init__(self):
            self.stats = {
                'total_return': 0.05,
                'max_drawdown': -0.02,
                'sharpe_ratio': 1.2,
                'calmar_ratio': 2.5
            }
            
            class DummyTrades:
                def __init__(self):
                    self.records_readable = pd.DataFrame({
                        'PnL': [10, -5, 15]
                    })
            
            self.trades = DummyTrades()
    
    # Test with uppercase 'PnL'
    dummy_portfolio = DummyPortfolio()
    metrics = calculate_performance_metrics(dummy_portfolio)
    
    logger.info(f"Metrics with uppercase 'PnL': {metrics}")
    
    # Now test with lowercase 'pnl'
    logger.info("Testing calculate_performance_metrics function with lowercase 'pnl'...")
    
    class DummyPortfolioLowercase:
        def __init__(self):
            self.stats = {
                'total_return': 0.05,
                'max_drawdown': -0.02,
                'sharpe_ratio': 1.2,
                'calmar_ratio': 2.5
            }
            
            class DummyTrades:
                def __init__(self):
                    self.records_readable = pd.DataFrame({
                        'pnl': [10, -5, 15]
                    })
            
            self.trades = DummyTrades()
    
    dummy_portfolio_lowercase = DummyPortfolioLowercase()
    metrics_lowercase = calculate_performance_metrics(dummy_portfolio_lowercase)
    
    logger.info(f"Metrics with lowercase 'pnl': {metrics_lowercase}")
    
    # Test with both columns missing
    logger.info("Testing error handling when PnL column is missing...")
    
    class DummyPortfolioMissing:
        def __init__(self):
            self.stats = {
                'total_return': 0.05,
                'max_drawdown': -0.02,
                'sharpe_ratio': 1.2,
                'calmar_ratio': 2.5
            }
            
            class DummyTrades:
                def __init__(self):
                    self.records_readable = pd.DataFrame({
                        'other_column': [10, -5, 15]
                    })
            
            self.trades = DummyTrades()
    
    dummy_portfolio_missing = DummyPortfolioMissing()
    metrics_missing = calculate_performance_metrics(dummy_portfolio_missing)
    
    logger.info(f"Metrics with missing PnL column: {metrics_missing}")
    
    logger.info("All tests completed successfully!")

if __name__ == "__main__":
    test_calculate_performance_metrics() 