#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test WFO data validation functionality.

This script tests the data validation functions in the refactored WFO modules.
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
from scripts.strategies.refactored_edge.wfo_utils import validate_ohlc_data
from scripts.strategies.refactored_edge.wfo import fetch_data

# Create test data fixtures
@pytest.fixture
def valid_ohlc_data():
    """
    Create valid OHLC data for testing.
    
    Returns:
        pd.DataFrame: DataFrame with valid OHLC columns
    """
    dates = pd.date_range(start='2025-01-01', periods=100, freq='1h')
    return pd.DataFrame({
        'Open': np.random.randn(100).cumsum() + 100,
        'High': np.random.randn(100).cumsum() + 105,
        'Low': np.random.randn(100).cumsum() + 95,
        'Close': np.random.randn(100).cumsum() + 100,
        'Volume': np.random.rand(100) * 1000
    }, index=dates)

@pytest.fixture
def valid_lowercase_data():
    """
    Create valid OHLC data with lowercase column names.
    
    Returns:
        pd.DataFrame: DataFrame with lowercase ohlc columns
    """
    dates = pd.date_range(start='2025-01-01', periods=100, freq='1h')
    return pd.DataFrame({
        'open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 105,
        'low': np.random.randn(100).cumsum() + 95,
        'close': np.random.randn(100).cumsum() + 100,
        'volume': np.random.rand(100) * 1000
    }, index=dates)

@pytest.fixture
def missing_column_data():
    """
    Create invalid OHLC data with missing columns.
    
    Returns:
        pd.DataFrame: DataFrame missing the 'Low' column
    """
    dates = pd.date_range(start='2025-01-01', periods=100, freq='1h')
    return pd.DataFrame({
        'Open': np.random.randn(100).cumsum() + 100,
        'High': np.random.randn(100).cumsum() + 105,
        # Missing 'Low' column
        'Close': np.random.randn(100).cumsum() + 100,
        'Volume': np.random.rand(100) * 1000
    }, index=dates)

@pytest.fixture
def mixed_case_data():
    """
    Create OHLC data with mixed case columns.
    
    Returns:
        pd.DataFrame: DataFrame with mixed case column names
    """
    dates = pd.date_range(start='2025-01-01', periods=100, freq='1h')
    return pd.DataFrame({
        'Open': np.random.randn(100).cumsum() + 100,
        'high': np.random.randn(100).cumsum() + 105,
        'Low': np.random.randn(100).cumsum() + 95,
        'close': np.random.randn(100).cumsum() + 100,
        'Volume': np.random.rand(100) * 1000
    }, index=dates)

# Test cases
def test_validate_ohlc_data_with_valid_data(valid_ohlc_data):
    """
    Test validation with valid OHLC data.
    
    Args:
        valid_ohlc_data: Pytest fixture with valid data
        
    Returns:
        None
    """
    is_valid, _ = validate_ohlc_data(valid_ohlc_data)
    assert is_valid is True, "Valid OHLC data should pass validation"

def test_validate_ohlc_data_with_lowercase_columns(valid_lowercase_data):
    """
    Test validation with lowercase column names.
    
    Args:
        valid_lowercase_data: Pytest fixture with lowercase columns
        
    Returns:
        None
    """
    is_valid, _ = validate_ohlc_data(valid_lowercase_data)
    assert is_valid is True, "Lowercase OHLC column names should pass validation"

def test_validate_ohlc_data_with_mixed_case(mixed_case_data):
    """
    Test validation with mixed case column names.
    
    Args:
        mixed_case_data: Pytest fixture with mixed case columns
        
    Returns:
        None
    """
    is_valid, _ = validate_ohlc_data(mixed_case_data)
    assert is_valid is True, "Mixed case OHLC column names should pass validation"

def test_validate_ohlc_data_with_missing_columns(missing_column_data):
    """
    Test validation with missing columns.
    
    Args:
        missing_column_data: Pytest fixture with missing Low column
        
    Returns:
        None
    """
    is_valid, missing_cols = validate_ohlc_data(missing_column_data)
    assert is_valid is False, "Missing columns should fail validation"
    assert 'Low' in missing_cols or 'low' in missing_cols, "Should detect missing 'Low' column"

def test_fetch_data_with_provided_data(valid_ohlc_data):
    """
    Test fetch_data when data is provided.
    
    Args:
        valid_ohlc_data: Pytest fixture with valid data
        
    Returns:
        None
    """
    result = fetch_data('BTC-USD', '1h', '2025-01-01', '2025-01-05', data=valid_ohlc_data)
    assert result is not None, "Should return provided data"
    assert len(result) == len(valid_ohlc_data), "Should return all rows of provided data"

def test_fetch_data_with_invalid_data(missing_column_data):
    """
    Test fetch_data with invalid provided data.
    
    Args:
        missing_column_data: Pytest fixture with missing columns
        
    Returns:
        None
    """
    with pytest.raises(ValueError, match="missing required OHLC columns"):
        fetch_data('BTC-USD', '1h', '2025-01-01', '2025-01-05', data=missing_column_data)

# Edge case: Empty dataframe
def test_validate_ohlc_data_with_empty_data():
    """
    Test validation with empty dataframe.
    
    Returns:
        None
    """
    empty_df = pd.DataFrame()
    is_valid, missing_cols = validate_ohlc_data(empty_df)
    assert is_valid is False, "Empty dataframe should fail validation"
    assert len(missing_cols) == 4, "Should detect all required OHLC columns as missing"
    assert set(missing_cols) == {'open', 'high', 'low', 'close'}, "Should report all required columns as missing"

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
