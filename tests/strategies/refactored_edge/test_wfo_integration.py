#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WFO Integration Test

This script performs a full integration test of the refactored WFO pipeline
using synthetic data to verify that all components work together correctly.

Author: Max Kimball
Date: 2025-04-28
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
import pytest
import importlib
from datetime import datetime, timedelta

# Add the parent directory to the path to ensure imports work correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Local imports
from scripts.strategies.refactored_edge.test_regime_detection import create_synthetic_data
from scripts.strategies.refactored_edge.wfo import run_wfo
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.wfo_utils import is_testing_mode

# Import modules where constants are defined
import scripts.strategies.refactored_edge.wfo_utils as wfo_utils
import scripts.strategies.refactored_edge.wfo as wfo
import scripts.strategies.refactored_edge.config as config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("wfo_integration_test")


def generate_test_data(days=10):
    """
    Generate synthetic data for WFO integration testing.
    
    Args:
        days (int): Number of days of data to generate
        
    Returns:
        pd.DataFrame: DataFrame with OHLCV data
    """
    logger.info(f"Generating synthetic data for {days} days...")
    
    # Use the create_synthetic_data function from test_regime_detection.py
    # This gives us data with known regime segments
    df = create_synthetic_data(days=days, volatility=0.02, trend_cycle_days=5, include_regimes=True)
    
    logger.info(f"Generated synthetic data with shape: {df.shape}")
    logger.info(f"Data columns: {df.columns.tolist()}")
    
    # Make sure all required columns are present
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Required column {col} not found in synthetic data")
            raise ValueError(f"Required column {col} not found in synthetic data")
    
    return df


def create_test_config():
    """
    Create a configuration suitable for testing.
    
    Returns:
        EdgeConfig: Configuration with test parameters
    """
    # Create config with smaller parameter grid for faster testing
    return EdgeConfig(
        granularity_str='1h',
        # Indicator parameters
        rsi_window=14, 
        bb_window=20,
        bb_std_dev=2.0,
        trend_ma_window=50,
        atr_window=14,
        atr_window_sizing=14,  # Added for ATR-based position sizing
        # Regime parameters
        adx_window=14,
        adx_threshold=25.0,
        strong_adx_threshold=35.0,  # Added for enhanced regime detection
        volatility_threshold=0.01,  # Added for regime volatility detection
        momentum_lookback=5,       # Added for momentum calculation
        momentum_threshold=0.005,  # Added for momentum threshold
        use_regime_filter=True,
        use_enhanced_regimes=False,
        use_regime_adaptation=False,
        # Entry/exit thresholds
        rsi_entry_threshold=30,
        rsi_exit_threshold=70,
        # S/D zone parameters 
        use_zones=False,  # Disable zones for simplicity in testing
        pivot_lookback=10,
        pivot_prominence=0.01,
        zone_merge_proximity=0.005,
        min_zone_width_candles=5,
        min_zone_strength=2,
        zone_extend_candles=50,
        zone_proximity_pct=0.001,
        # Risk parameters
        pct_risk_per_trade=0.02,
        use_atr_stops=True,
        sl_atr_multiplier=1.5,
        tp_atr_multiplier=3.0,
        # Fees and slippage
        commission_pct=0.0015,
        slippage_pct=0.0005,
        # Capital
        initial_capital=10000.0
    )




def validate_results(results_list, portfolios, best_params):
    """
    Validate WFO results to ensure the pipeline worked as expected.
    
    Args:
        results_list (list): List of results dictionaries from WFO
        portfolios (dict): Dictionary of portfolio objects
        best_params (dict): Dictionary of best parameters by split
        
    Returns:
        bool: True if validation passed, False otherwise
    """
    # Check if we got valid results
    if not results_list:
        logger.error("No results returned from WFO run")
        return False
    
    if not portfolios:
        logger.error("No portfolios returned from WFO run")
        return False
    
    if not best_params:
        logger.error("No best parameters returned from WFO run")
        return False
    
    # Validate basic structure of results
    for i, result in enumerate(results_list):
        logger.info(f"Validating results for split {i+1}...")
        
        # Check for required result fields
        required_fields = ['split', 'train_start', 'train_end', 'test_start', 
                           'test_end', 'best_params']
        for field in required_fields:
            if field not in result:
                logger.error(f"Required field '{field}' missing from results")
                return False
        
        # Validate that we have corresponding portfolio
        if i not in portfolios:
            logger.error(f"No portfolio found for split {i+1}")
            return False
            
        # Validate that we have corresponding best_params
        if i not in best_params:
            logger.error(f"No best parameters found for split {i+1}")
            return False
    
    logger.info("Results validation passed!")
    return True


def override_test_parameters():
    """
    Override both WFO parameters and optimization parameter grid for testing.
    This function handles all test-specific overrides needed for the integration test.
    
    Returns:
        dict: Original parameter values for restoration
    """
    # Set smaller values appropriate for our synthetic dataset (240 points)
    # Use approximately 60% for training, 30% for testing, 10% step
    train_points = 144  # 60% of 240
    test_points = 72    # 30% of 240
    step_points = 24    # 10% of 240
    
    # Create a test-specific parameter grid that includes atr_window_sizing
    test_param_grid = {
        # --- Fixed Parameters ---
        'granularity_str': ['1h'],
        'atr_window': [14],
        'atr_window_sizing': [14],  # Critical: Include this for ATR-based sizing
        'bb_window': [20],
        'bb_std_dev': [2.0],
        'rsi_window': [14],
        'trend_ma_window': [50],  # Use consistent naming (trend_ma_window not ma_window)
        
        # --- Core Parameters ---
        'rsi_entry_threshold': [30, 40],  # Just two values for testing
        'rsi_exit_threshold': [60, 70],  # Just two values for testing
        
        # --- Regime Parameters ---
        'adx_window': [14],
        'adx_threshold': [25.0],
        'use_regime_filter': [False],  # Simplify by turning off regime filter
        'use_enhanced_regimes': [False],  # Simplify by using basic regime detection
        
        # --- Risk Parameters ---
        'sl_atr_multiplier': [1.5],
        'tp_atr_multiplier': [3.0],
        
        # --- S/D Zone Parameters ---
        'use_zones': [False],  # Disable zones for simplicity in testing
    }
    
    # Store original values from modules and config
    original_values = {
        'wfo_utils': {
            'WFO_TRAIN_POINTS': wfo_utils.WFO_TRAIN_POINTS,
            'WFO_TEST_POINTS': wfo_utils.WFO_TEST_POINTS,
            'STEP_POINTS': wfo_utils.STEP_POINTS
        },
        'wfo': {
            'WFO_TRAIN_POINTS': wfo.WFO_TRAIN_POINTS,
            'WFO_TEST_POINTS': wfo.WFO_TEST_POINTS,
            'STEP_POINTS': wfo.STEP_POINTS
        },
        'config': {
            'OPTIMIZATION_PARAMETER_GRID': config.OPTIMIZATION_PARAMETER_GRID.copy()
        }
    }
    
    # Override WFO parameters in wfo_utils module
    wfo_utils.WFO_TRAIN_POINTS = train_points
    wfo_utils.WFO_TEST_POINTS = test_points
    wfo_utils.STEP_POINTS = step_points
    
    # Override WFO parameters in wfo module (these are imported directly)
    wfo.WFO_TRAIN_POINTS = train_points
    wfo.WFO_TEST_POINTS = test_points
    wfo.STEP_POINTS = step_points
    
    # Override optimization parameter grid in config module
    config.OPTIMIZATION_PARAMETER_GRID = test_param_grid
    
    logger.info(f"Overriding test parameters for integration test:")
    logger.info(f"  WFO Train points: {train_points}")
    logger.info(f"  WFO Test points: {test_points}")
    logger.info(f"  WFO Step points: {step_points}")
    logger.info(f"  Parameter grid: Custom grid with {len(test_param_grid)} parameters including atr_window_sizing")
    
    return original_values


def restore_test_parameters(original_values):
    """
    Restore original parameter values in all modules.
    
    Args:
        original_values (dict): Original parameter values
    """
    # Restore in wfo_utils module
    wfo_utils.WFO_TRAIN_POINTS = original_values['wfo_utils']['WFO_TRAIN_POINTS']
    wfo_utils.WFO_TEST_POINTS = original_values['wfo_utils']['WFO_TEST_POINTS']
    wfo_utils.STEP_POINTS = original_values['wfo_utils']['STEP_POINTS']
    
    # Restore in wfo module
    wfo.WFO_TRAIN_POINTS = original_values['wfo']['WFO_TRAIN_POINTS']
    wfo.WFO_TEST_POINTS = original_values['wfo']['WFO_TEST_POINTS']
    wfo.STEP_POINTS = original_values['wfo']['STEP_POINTS']
    
    # Restore config parameter grid
    if 'config' in original_values:
        config.OPTIMIZATION_PARAMETER_GRID = original_values['config']['OPTIMIZATION_PARAMETER_GRID']
    
    logger.info("Restored all original parameters")


def run_integration_test():
    """
    Run a complete integration test of the WFO pipeline.
    """
    # Enable testing mode via environment variable
    os.environ["REGIME_TESTING_MODE"] = "1"
    
    # Override both WFO parameters and optimization parameter grid with test-appropriate values
    original_params = override_test_parameters()
    
    try:
        logger.info("Starting WFO integration test...")
        
        # Generate synthetic test data (10 days of hourly data = 240 data points)
        # This is smaller than normal for quick testing
        test_data = generate_test_data(days=10)
        logger.info(f"Generated test data with {len(test_data)} data points")
        
        # Create test configuration
        config = create_test_config()
        logger.info("Created test configuration")
        
        # Run WFO with smaller train/test sizes and fewer splits for quick testing
        # Use a small train_ratio and only 2 splits for faster testing
        logger.info("Running WFO pipeline with synthetic data...")
        results, portfolios, best_params = run_wfo(
            symbol='TEST-USD',  # Dummy symbol
            timeframe='1h',
            start_date=None,   # Not needed since we're passing data directly
            end_date=None,     # Not needed since we're passing data directly
            initial_capital=10000,
            config=config,
            n_splits=2,       # Only run 2 splits for faster testing
            train_ratio=0.6,  # Smaller train ratio for smaller dataset
            n_jobs=1,         # Single-threaded for predictable testing
            data=test_data    # Pass our synthetic data directly
        )
        
        # Validate results
        if validate_results(results, portfolios, best_params):
            logger.info("✅ WFO integration test completed successfully!")
            return True
        else:
            logger.error("❌ WFO integration test failed!")
            return False
            
    except Exception as e:
        logger.error(f"Error in WFO integration test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up environment variable
        if "REGIME_TESTING_MODE" in os.environ:
            del os.environ["REGIME_TESTING_MODE"]
        # Restore all original parameters (WFO and parameter grid)
        restore_test_parameters(original_params)
        # Reset testing mode
        os.environ["REGIME_TESTING_MODE"] = "0"


def test_wfo_integration():
    """
    Pytest function for running the WFO integration test.
    """
    assert run_integration_test(), "WFO integration test failed"


if __name__ == "__main__":
    # Run test directly if script is executed
    success = run_integration_test()
    exit(0 if success else 1)
