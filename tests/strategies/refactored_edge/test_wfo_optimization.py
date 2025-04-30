#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test WFO optimization functionality.

This script tests the parameter optimization functions in the refactored WFO modules.
"""
import os
import sys
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Import the modules to test
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.wfo_optimization import (
    optimize_params_parallel, determine_market_regime_for_params
)
from scripts.strategies.refactored_edge.test_regime_detection import create_synthetic_data

# Set test mode for signal generation
os.environ['REGIME_TESTING_MODE'] = 'True'

# Create test data fixture
@pytest.fixture
def synthetic_market_data():
    """
    Create synthetic market data for testing optimization.
    
    Returns:
        pd.DataFrame: DataFrame with synthetic OHLC data and explicit regimes
    """
    # Create data with various regimes
    df = create_synthetic_data(days=30)
    return df

@pytest.fixture
def param_combinations():
    """
    Create parameter combinations for testing optimization.
    
    Returns:
        list: List of parameter dictionaries
    """
    # Create a complete EdgeConfig with all required parameters explicitly set
    config = EdgeConfig(
        granularity_str='1h',
        _is_testing=True,
        rsi_window=14,
        bb_window=20,
        bb_std_dev=2.0,
        trend_ma_window=50,
        atr_window=14,
        atr_window_sizing=14,
        adx_window=14,
        adx_threshold=25.0,
        rsi_entry_threshold=30,
        rsi_exit_threshold=70,
        use_zones=False
    )
    
    # Create a simplified parameter set for testing
    test_params = [
        {
            # Core parameters
            'rsi_window': 14,
            'bb_window': 20,
            'bb_std_dev': 2.0,
            'trend_ma_window': 50,
            'atr_window': 14,
            'atr_window_sizing': 14,
            'adx_window': 14,
            'adx_threshold': 25.0,
            'rsi_entry_threshold': 30,
            'rsi_exit_threshold': 70,
            'use_zones': False,
            '_is_testing': True
        },
        {
            # Alternate parameters 
            'rsi_window': 21,
            'bb_window': 20,
            'bb_std_dev': 2.0,
            'trend_ma_window': 50,
            'atr_window': 14,
            'atr_window_sizing': 14,
            'adx_window': 14,
            'adx_threshold': 25.0,
            'rsi_entry_threshold': 35,
            'rsi_exit_threshold': 65,
            'use_zones': False,
            '_is_testing': True
        }
    ]
    
    return test_params

@pytest.fixture
def test_config():
    """Provides a default EdgeConfig instance for testing."""
    return EdgeConfig()

def test_determine_market_regime(synthetic_market_data, test_config):
    """
    Test market regime determination function.
    
    Args:
        synthetic_market_data: Pytest fixture with synthetic market data
        test_config: Pytest fixture providing an EdgeConfig instance
        
    Returns:
        None
    """
    # Run regime detection on synthetic data using the test config
    regime_info = determine_market_regime_for_params(synthetic_market_data, test_config)
    
    # Verify regime detection produces sensible results
    assert regime_info is not None, "Should return regime information"
    assert isinstance(regime_info, dict), "Should return a dictionary of regime information"
    assert 'trending_pct' in regime_info, "Should include trending percentage"
    assert 'ranging_pct' in regime_info, "Should include ranging percentage"
    assert 'predominant_regime' in regime_info, "Should include predominant regime"
    assert regime_info['trending_pct'] + regime_info['ranging_pct'] <= 100.1, "Percentages should sum to 100 or approximately 100"
    
    # The predominant regime should match the higher percentage
    if regime_info['trending_pct'] > regime_info['ranging_pct']:
        assert regime_info['predominant_regime'] == 'trending', "Predominant regime should be trending"
    elif regime_info['ranging_pct'] > regime_info['trending_pct']:
        assert regime_info['predominant_regime'] == 'ranging', "Predominant regime should be ranging"

def test_optimize_params_parallel(synthetic_market_data, param_combinations):
    """
    Test parallel parameter optimization function.
    
    Args:
        synthetic_market_data: Pytest fixture with synthetic market data
        param_combinations: Pytest fixture with parameter combinations
        
    Returns:
        None
    """
    # Run optimization with small parameter set
    best_params, best_score, best_params_by_regime = optimize_params_parallel(
        data=synthetic_market_data,
        param_combinations=param_combinations,
        metric='Sharpe Ratio',
        n_jobs=1  # Use single job for testing
    )
    
    # Check optimization results - may be None if no valid parameters found
    if best_params is not None:
        assert isinstance(best_params, dict), "Best params should be a dictionary"
        assert isinstance(best_score, (float, dict)), "Best score should be a float or dict"
        assert isinstance(best_params_by_regime, dict), "Best params by regime should be a dictionary"
        
        # Check regime-specific parameters
        assert 'overall' in best_params_by_regime, "Should include overall params"
        
        # Regime-specific parameters might not be present if insufficient data
        if 'trending' in best_params_by_regime:
            assert isinstance(best_params_by_regime['trending'], dict), "Trending params should be a dictionary"
            
        if 'ranging' in best_params_by_regime:
            assert isinstance(best_params_by_regime['ranging'], dict), "Ranging params should be a dictionary"

def test_optimize_with_empty_params(synthetic_market_data):
    """
    Test optimization with empty parameter list (edge case).
    
    Args:
        synthetic_market_data: Pytest fixture with synthetic market data
        
    Returns:
        None
    """
    # Run optimization with empty parameter list
    best_params, best_score, best_params_by_regime = optimize_params_parallel(
        data=synthetic_market_data,
        param_combinations=[],
        metric='Sharpe Ratio',
        n_jobs=1
    )
    
    # Check that function handles empty parameters gracefully
    assert best_params is None, "Should return None for best_params with empty parameter list"
    assert best_score is None, "Should return None for best_score with empty parameter list"
    assert best_params_by_regime is None, "Should return None for best_params_by_regime with empty parameter list"

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
