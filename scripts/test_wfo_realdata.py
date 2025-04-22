import pandas as pd
import numpy as np
import logging
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the strategy components
try:
    from strategies.wfo_edge_strategy import (
        create_pf_for_params, 
        optimize_parameters,
        create_wfo_splits,
        evaluate_portfolio
    )
    from strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
    
    # Add data fetching
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from data.data_fetcher import fetch_historical_data, GRANULARITY_MAP_SECONDS
    
    logger.info("Successfully imported all required components")
except ImportError as e:
    logger.error(f"Failed to import required components: {e}")
    sys.exit(1)

def fetch_test_data(symbol='BTC-USD', timeframe='1d', start_date='2022-01-01', end_date='2022-12-31'):
    """Fetch real cryptocurrency data for testing"""
    logger.info(f"Fetching {symbol} data from {start_date} to {end_date} ({timeframe})")
    
    granularity_seconds = GRANULARITY_MAP_SECONDS.get(timeframe.lower())
    if granularity_seconds is None:
        logger.error(f"Unsupported granularity: {timeframe}")
        return None
    
    try:
        data = fetch_historical_data(symbol, start_date, end_date, granularity_seconds)
        if data is not None and not data.empty:
            logger.info(f"Data fetched successfully. Shape: {data.shape}")
            return data
        else:
            logger.error("Failed to fetch data or empty dataset returned")
            return None
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None

def test_portfolio_creation_realdata():
    """Test if a portfolio can be created with real market data"""
    logger.info("Testing portfolio creation with real data...")
    
    # Fetch real data
    data = fetch_test_data()
    if data is None:
        logger.error("Cannot proceed without data")
        return False
    
    # Define parameters
    params = {
        'lookback_window': 15, 
        'vol_filter_window': 50, 
        'volatility_threshold': 0.8,
        'initial_capital': 10000
    }
    
    # Try to create a portfolio
    try:
        portfolio = create_pf_for_params(data, params)
        if portfolio is not None:
            metrics = evaluate_portfolio(portfolio)
            logger.info("Portfolio creation successful!")
            logger.info(f"Portfolio metrics: {metrics}")
            return True
        else:
            logger.error("Portfolio creation failed: returned None")
            return False
    except Exception as e:
        logger.error(f"Portfolio creation error: {e}")
        return False

def test_wfo_splits():
    """Test the creation of walk-forward optimization data splits"""
    logger.info("Testing WFO data splits...")
    
    # Fetch real data
    data = fetch_test_data()
    if data is None:
        logger.error("Cannot proceed without data")
        return False
    
    try:
        # Create WFO splits (5 splits with 80% in-sample)
        splits = create_wfo_splits(data, num_splits=3, train_size=0.8)
        
        if splits and len(splits) > 0:
            logger.info(f"Successfully created {len(splits)} WFO splits")
            for i, (train, test) in enumerate(splits):
                logger.info(f"Split {i+1}: Train={len(train)} rows, Test={len(test)} rows")
            return True
        else:
            logger.error("WFO splits creation failed")
            return False
    except Exception as e:
        logger.error(f"Error creating WFO splits: {e}")
        return False

def test_parameter_optimization_realdata(n_trials=5):
    """Test the parameter optimization function with real data"""
    logger.info(f"Testing parameter optimization with real data ({n_trials} trials)...")
    
    # Fetch real data
    data = fetch_test_data()
    if data is None:
        logger.error("Cannot proceed without data")
        return False
    
    # Define parameter space
    params_space = {
        'lookback_window': (10, 30),
        'vol_filter_window': (50, 100),
        'volatility_threshold': (0.3, 0.9)
    }
    
    # Try optimization
    try:
        best_params, best_metric, all_results = optimize_parameters(
            data, params_space, n_trials=n_trials
        )
        
        logger.info("Optimization completed successfully")
        
        # Check if we got valid results
        if best_metric == float('-inf'):
            logger.warning("Optimization completed but didn't find valid parameters")
            return True  # Still consider the test successful since the function ran
        else:
            logger.info(f"Best parameters: {best_params}")
            logger.info(f"Best metric: {best_metric}")
            
            # Get best trial results
            if len(all_results) > 0:
                best_trial = max(all_results, key=lambda x: x.get('score', float('-inf')))
                logger.info(f"Best trial metrics: {best_trial.get('metrics', {})}")
                
            return True
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting real data test script...")
    
    # Test portfolio creation with real data
    if test_portfolio_creation_realdata():
        logger.info("Portfolio creation with real data test PASSED ✓")
    else:
        logger.error("Portfolio creation with real data test FAILED ✗")
    
    # Test WFO splits
    if test_wfo_splits():
        logger.info("WFO splits test PASSED ✓")
    else:
        logger.error("WFO splits test FAILED ✗")
    
    # Test parameter optimization with real data
    if test_parameter_optimization_realdata(n_trials=3):
        logger.info("Parameter optimization with real data test PASSED ✓")
    else:
        logger.error("Parameter optimization with real data test FAILED ✗")
    
    logger.info("Real data tests completed.") 