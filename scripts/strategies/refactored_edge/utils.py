#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility functions for refactored edge strategy.

This module provides common utility functions for data validation, error handling,
and dependency management to ensure robust and error-free operation of the strategy.
"""

import pandas as pd
import numpy as np
import logging
import importlib
from functools import wraps
from typing import Dict, List, Optional, Any, Callable, Tuple, Union, Set
import traceback

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def validate_dataframe(data: pd.DataFrame, required_cols: List[str]) -> pd.DataFrame:
    """
    Validate that a DataFrame contains all required columns.
    
    Args:
        data: DataFrame to validate
        required_cols: List of column names that must be present
        
    Returns:
        The original DataFrame if valid
        
    Raises:
        ValueError: If any required columns are missing
    """
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"DataFrame missing required columns: {missing_cols}")
    return data


def safe_get_column(data: pd.DataFrame, column_name: str, alternatives: Optional[List[str]] = None, 
                  default: Optional[Any] = None) -> Any:
    """
    Safely retrieve a column from a DataFrame with case-insensitive fallbacks.
    
    Args:
        data: Source DataFrame
        column_name: Primary column name to look for
        alternatives: List of alternative column names to try
        default: Default value to return if column not found
        
    Returns:
        Column data if found, otherwise default value
    """
    if column_name in data.columns:
        return data[column_name]
    
    # Try alternative column names if provided
    if alternatives:
        for alt in alternatives:
            if alt in data.columns:
                return data[alt]
    
    # Return default if column not found
    return default


def get_numeric_column(data: pd.DataFrame, column_name: str, alternatives: Optional[List[str]] = None, 
                      default: Optional[Any] = None) -> pd.Series:
    """
    Get a column and ensure it's numeric type.
    
    Args:
        data: Source DataFrame
        column_name: Primary column name to look for
        alternatives: List of alternative column names to try
        default: Default value to return if column not found
        
    Returns:
        Numeric column data
    """
    col = safe_get_column(data, column_name, alternatives, default)
    if col is not None and not pd.api.types.is_numeric_dtype(col):
        try:
            return pd.to_numeric(col, errors='coerce')
        except Exception as e:
            logger.warning(f"Could not convert column {column_name} to numeric: {str(e)}")
            return col
    return col


def ensure_config_attributes(config: Any, required_attrs: List[str]) -> bool:
    """
    Ensure a configuration object has all required attributes.
    
    Args:
        config: Configuration object to validate
        required_attrs: List of attribute names that must be present
        
    Returns:
        True if all attributes are present, False otherwise
        
    Logs:
        Warning messages for any missing attributes
    """
    missing_attrs = [attr for attr in required_attrs if not hasattr(config, attr)]
    if missing_attrs:
        logger.warning(f"Configuration missing required attributes: {missing_attrs}")
        return False
    return True


def safe_import(module_name: str) -> Any:
    """
    Safely import a module to prevent circular dependencies.
    
    Args:
        module_name: Name of the module to import
        
    Returns:
        Imported module or None if import fails
        
    This helps break circular dependencies by dynamically importing
    modules only when needed instead of at the top level.
    """
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        logger.error(f"Error importing module {module_name}: {str(e)}")
        return None


def with_error_handling(default_return: Any = None):
    """
    Decorator to add consistent error handling to functions.
    
    Args:
        default_return: Value to return if function raises an exception
        
    Returns:
        Decorator function
        
    Example:
        @with_error_handling(default_return=-np.inf)
        def calculate_metric(data):
            # ... calculation that might raise an exception
            return result
            
    Important: When applying to functions that use nested inner functions which
    access the outer function's variables, make sure to apply the decorator to
    the inner function directly, not the outer function.
    
    Example with inner function (correct usage):
        def outer_function(x, y):
            @with_error_handling(default_return=0)
            def _inner_calculation():
                # safely access x and y from outer scope
                return complex_calculation(x, y)
            return _inner_calculation()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Pass all arguments unchanged to preserve scope for nested functions
                return func(*args, **kwargs)
            except Exception as e:
                func_name = getattr(func, '__name__', 'unknown')
                logger.error(f"Error in {func_name}: {str(e)}")
                logger.debug(traceback.format_exc())
                return default_return
        return wrapper
    return decorator


def normalize_regime_type(regime_value: Any) -> str:
    """
    Normalize regime type values to a consistent string format.
    
    Handles enum values, string variations, and other types.
    
    Args:
        regime_value: The regime value to normalize
        
    Returns:
        Normalized string representation of the regime value
    """
    if regime_value is None:
        return "unknown"
        
    # Convert to string, ensuring enums are handled properly
    regime_str = str(regime_value)
    
    # Remove any class prefixes that might be present in enum string representations
    # Example: MarketRegimeType.TRENDING becomes TRENDING
    if '.' in regime_str:
        regime_str = regime_str.split('.')[-1]
    
    # Normalize to lowercase for consistent comparison
    return regime_str.lower()


def calculate_regime_percentages(regimes: pd.Series) -> Dict[str, float]:
    """
    Calculate percentage distribution of different regime types in a series.
    
    Args:
        regimes: Series of regime classifications
        
    Returns:
        Dictionary with regime types as keys and percentages as values
    """
    if regimes is None or regimes.empty:
        logger.warning("Received empty or None regimes series in percentage calculation")
        return {}
    
    # Handle potential NaN values
    clean_regimes = regimes.fillna('unknown')
    
    # Normalize all regime values to consistent string format
    normalized_regimes = clean_regimes.apply(normalize_regime_type)
    
    # Calculate regime distribution
    counts = normalized_regimes.value_counts(normalize=True) * 100
    
    # Convert to dictionary with 0 as default for missing regimes
    result = {str(regime): float(pct) for regime, pct in counts.items()}
    
    # Add debug logging
    logger.debug(f"Original regime values: {regimes.value_counts().to_dict()}")
    logger.debug(f"Normalized regime values: {normalized_regimes.value_counts().to_dict()}")
    logger.debug(f"Calculated regime percentages: {result}")
    
    return result


def determine_predominant_regime(regime_percentages: Dict[str, float], 
                                 trending_threshold: float = 50.0) -> str:
    """
    Determine the predominant regime based on percentage distribution.
    
    Args:
        regime_percentages: Dictionary with regime types and their percentages
        trending_threshold: Threshold percentage for a regime to be considered predominant
        
    Returns:
        Name of the predominant regime or 'ranging' if no regime meets the threshold
    """
    # Get trending percentage (sum of all trending-related regimes)
    trending_regimes = [
        'trending', 'strong_uptrend', 'weak_uptrend', 'strong_downtrend', 
        'weak_downtrend', 'breakout', 'breakdown'
    ]
    
    trending_pct = sum(regime_percentages.get(regime, 0) for regime in trending_regimes)
    
    if trending_pct >= trending_threshold:
        return 'trending'
    else:
        return 'ranging'
