"""
Utility functions and common constants for Walk-Forward Optimization.

This module provides utility functions, path handling, data validation, and common constants
used across the WFO framework. It serves as the foundation for the modular WFO implementation.
"""
import os
import sys
import traceback
from pathlib import Path
import pandas as pd
import numpy as np

# --- Path Setup ---

def setup_project_paths():
    """
    Ensure the project root is in the Python path.
    
    This allows importing modules from the project root and scripts directory.
    
    Returns:
        tuple: (project_root, scripts_parent) paths
    """
    # Get the current file's directory
    current_dir = Path(__file__).resolve().parent
    
    # Add project root to path (3 levels up)
    project_root = current_dir.parents[3]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
    
    # Add scripts parent to path (2 levels up)
    scripts_parent = current_dir.parents[2]  # scripts/ dir
    if str(scripts_parent) not in sys.path:
        sys.path.append(str(scripts_parent))
    
    return project_root, scripts_parent

# Run path setup when the module is imported
PROJECT_ROOT, SCRIPTS_PARENT = setup_project_paths()

# --- Data Fetcher Handling ---

def import_data_fetcher():
    """
    Try to import the data fetcher module.
    
    Returns:
        tuple: (fetch_historical_data function, availability flag)
    """
    try:
        from data.data_fetcher import fetch_historical_data
        print("Successfully imported fetch_historical_data from data.data_fetcher")
        return fetch_historical_data, True
    except ImportError:
        print("Warning: Could not import fetch_historical_data from data.data_fetcher.")
        print("WFO requires actual historical data. Please ensure data/data_fetcher.py exists and is correct.")
        return None, False

# --- Common Constants ---

# Trading parameters
SYMBOL = 'BTC-USD'
TIMEFRAME = '15m'  # Adjusted from '15T'
START_DATE = '2022-01-01'
END_DATE = '2024-01-01'
INIT_CAPITAL = 10000
FEES_PCT = 0.001  # Example fee
N_JOBS = -1  # Number of cores for parallel processing (-1 uses all available)

# WFO Configuration
WFO_TRAIN_POINTS = 34560  # Approx 360 days of 15-min data
WFO_TEST_POINTS = 8640    # Approx 90 days of 15-min data
STEP_POINTS = WFO_TEST_POINTS  # Step forward by test length for non-overlapping test sets

# Results Configuration
OUTPUT_DIR = "data/results"  # Directory to save results
RESULTS_FILENAME = "wfo_results.csv"  # Filename for the results CSV

# --- Data Validation ---

def validate_ohlc_data(data, verbose=True):
    """
    Validate that a DataFrame contains required OHLC columns.
    
    Checks for both uppercase (OHLC) and lowercase (ohlc) column versions.
    
    Args:
        data (pd.DataFrame): DataFrame to validate
        verbose (bool): Whether to print debug information
        
    Returns:
        tuple: (is_valid, missing_cols)
            - is_valid: Boolean indicating if data is valid
            - missing_cols: List of missing column names, or None if all required columns are present
    """
    required_cols_lower = ['open', 'high', 'low', 'close']
    required_cols_upper = ['Open', 'High', 'Low', 'Close']
    
    # Check for lowercase columns
    lower_missing = [col for col in required_cols_lower if col.lower() not in [c.lower() for c in data.columns]]
    # Check for uppercase columns
    upper_missing = [col for col in required_cols_upper if col not in data.columns]
    
    # Determine if we have a complete set in either case format
    has_lower = len(lower_missing) == 0
    has_upper = len(upper_missing) == 0
    
    if not (has_lower or has_upper):
        # Choose the case format with the fewest missing columns to report
        missing_cols = lower_missing if len(lower_missing) <= len(upper_missing) else upper_missing
        
        if verbose:
            print(f"ERROR: Missing required OHLC columns in data")
            print(f"Expected one of: {required_cols_lower} or {required_cols_upper}")
            print(f"Found: {list(data.columns)}")
            print(f"Missing: {missing_cols}")
        
        return False, missing_cols
    
    # All required columns are present
    return True, None

def get_ohlc_columns(data):
    """
    Get OHLC columns from a DataFrame, handling both uppercase and lowercase cases.
    
    Args:
        data (pd.DataFrame): DataFrame with OHLC data
        
    Returns:
        tuple: (open, high, low, close) Series, or (None, None, None, None) if not found
    """
    is_valid, missing_cols = validate_ohlc_data(data, verbose=False)
    
    if not is_valid:
        print(f"ERROR: Cannot extract OHLC columns. DataFrame has columns: {list(data.columns)}")
        return None, None, None, None
    
    # Since we've validated the data has all required columns, check which case format is available
    if 'Open' in data.columns and 'High' in data.columns and 'Low' in data.columns and 'Close' in data.columns:
        return data['Open'], data['High'], data['Low'], data['Close']
    else:
        return data['open'], data['high'], data['low'], data['close']

def ensure_output_dir(dir_path=None):
    """
    Ensure the output directory exists.
    
    Args:
        dir_path (str, optional): Directory path. Defaults to OUTPUT_DIR.
        
    Returns:
        str: Path to the output directory
    """
    output_dir = dir_path or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def calculate_wfo_points(timeframe, train_days=240, test_days=60):
    """
    Calculate the number of data points for a given timeframe.
    
    Args:
        timeframe (str): Timeframe string (e.g., '1h', '15m')
        train_days (int): Number of days for training
        test_days (int): Number of days for testing
        
    Returns:
        tuple: (train_points, test_points, step_points)
    """
    # Calculate points based on timeframe
    points_per_day = {
        '1m': 1440,    # 1 minute
        '5m': 288,     # 5 minutes
        '15m': 96,     # 15 minutes
        '1h': 24,      # 1 hour
        '4h': 6,       # 4 hours
        '1d': 1        # 1 day
    }
    
    # Get points per day for the timeframe
    ppd = points_per_day.get(timeframe, 96)  # Default to 15m if unknown
    
    train_points = train_days * ppd
    test_points = test_days * ppd
    step_points = test_points  # Default step size is one test period
    
    return train_points, test_points, step_points

# --- Standardize Column Names ---

def to_snake_case(name):
    """
    Converts a column name to snake_case format.
    
    Args:
        name (str): Column name to convert
        
    Returns:
        str: snake_case formatted name
    """
    import re
    # Replace any non-alphanumeric with underscore
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Ensure uppercase followed by lowercase is separated by underscore
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    # Convert to lowercase and replace any non-alphanumeric with underscore
    return re.sub('[^0-9a-zA-Z]+', '_', s2).lower()


def standardize_column_names(df):
    """
    Standardize all column names in a DataFrame to snake_case format.
    
    Args:
        df (pd.DataFrame): DataFrame with columns to standardize
        
    Returns:
        pd.DataFrame: DataFrame with standardized column names
    """
    if df is None or df.empty:
        return df
        
    # Create a mapping of old column names to new snake_case names
    col_mapping = {col: to_snake_case(col) for col in df.columns}
    
    # Rename columns using the mapping
    df = df.rename(columns=col_mapping)
    
    return df

# --- Testing Mode ---

def is_testing_mode():
    """
    Check if we're running in testing mode via environment variable.
    
    Returns:
        bool: True if REGIME_TESTING_MODE environment variable is set
    """
    return os.environ.get('REGIME_TESTING_MODE', '0').lower() in ('1', 'true', 'yes')


def set_testing_mode(enabled=True):
    """
    Set the testing mode environment variable.
    
    Args:
        enabled (bool): Whether testing mode should be enabled
    """
    os.environ['REGIME_TESTING_MODE'] = str(enabled)
    mode_str = "ENABLED" if enabled else "DISABLED"
    print(f"Testing mode {mode_str}")
