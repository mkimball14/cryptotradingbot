#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Optuna-based optimization for the Edge Multi-Factor strategy.

This script properly integrates with the existing project structure to provide
Bayesian optimization for strategy parameters using Optuna.
"""

import os
import sys
import time
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
import multiprocessing as mp

import pandas as pd
import numpy as np
import optuna

# Set up Python path to match integration test pattern
current_file = Path(__file__).resolve()
current_dir = current_file.parent
project_root = current_dir.parents[3]
scripts_dir = current_dir.parents[2]

# Add paths to allow imports
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))
    
# Import required modules - Use the same pattern as in test_wfo_integration.py
from scripts.strategies.refactored_edge import (
    config, wfo, wfo_utils, indicators, signals, regime
)
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.wfo import run_wfo
from scripts.strategies.refactored_edge.wfo_utils import validate_ohlc_data
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger('optuna_optimization')

# Define constants
OUTPUT_DIR = os.path.join(project_root, 'data', 'optuna_optimization')
PLOTS_DIR = os.path.join(OUTPUT_DIR, 'plots')
RESULTS_DIR = os.path.join(OUTPUT_DIR, 'results')


def ensure_directories():
    """Create necessary directories for Optuna results."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    logger.info(f"Created output directories at {OUTPUT_DIR}")


def fetch_historical_data(symbol, timeframe, days=120):
    """
    Fetch historical data for a symbol and timeframe.
    
    Args:
        symbol: Trading symbol
        timeframe: Timeframe
        days: Number of days to fetch
        
    Returns:
        DataFrame with OHLCV data or None if fetching fails
    """
    # Import utilities within function to avoid circular dependencies
    from scripts.strategies.refactored_edge.utils import with_error_handling, validate_dataframe
    
    @with_error_handling(default_return=None)
    def _fetch_data():
        # Validate input parameters
        if not symbol or not isinstance(symbol, str):
            logger.error(f"Invalid symbol: {symbol}")
            return None
            
        if not timeframe or not isinstance(timeframe, str):
            logger.error(f"Invalid timeframe: {timeframe}")
            return None
            
        if days <= 0:
            logger.warning(f"Invalid days value: {days}, defaulting to 120")
            days = 120
        
        # Check for mock data first for testing
        mock_file = os.path.join(project_root, 'tests', 'data', f"{symbol}_{timeframe}_mock.csv")
        if os.path.exists(mock_file):
            logger.info(f"Using mock data from {mock_file}")
            try:
                data = pd.read_csv(mock_file, index_col=0, parse_dates=True)
                # Validate that we have all required columns
                required_cols = ['open', 'high', 'low', 'close', 'volume']
                alt_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                
                # Check if columns exist in either lowercase or uppercase
                has_required = all(col.lower() in map(str.lower, data.columns) for col in required_cols)
                
                if not has_required:
                    # Try to rename columns to lowercase if uppercase variants exist
                    for orig, alt in zip(required_cols, alt_cols):
                        if alt in data.columns and orig not in data.columns:
                            data[orig] = data[alt]
                
                # Final validation
                if not all(col in data.columns for col in required_cols):
                    logger.warning(f"Mock data missing required columns. Found: {data.columns.tolist()}")
                    return None
                    
                return data
            except Exception as e:
                logger.error(f"Error reading mock data: {e}")
                return None
                
        # Use cached data if available
        cache_dir = os.path.join(project_root, 'data', 'cache')
        os.makedirs(cache_dir, exist_ok=True)
        
        cache_file = os.path.join(cache_dir, f"{symbol}_{timeframe}_{days}days.csv")
        
        # Check if cache file exists and is recent (less than 1 day old)
        if os.path.exists(cache_file):
            file_age = time.time() - os.path.getmtime(cache_file)
            if file_age < 86400:  # 1 day in seconds
                logger.info(f"Using cached data from {cache_file}")
                try:
                    data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                    # Validate DataFrame has required columns
                    required_cols = ['open', 'high', 'low', 'close', 'volume']
                    validate_dataframe(data, required_cols)
                    return data
                except Exception as e:
                    logger.warning(f"Error reading cached data, will fetch fresh data: {e}")
                    # Continue to fetch fresh data
        
        # If we get here, we need to fetch fresh data
        logger.info(f"Fetching {days} days of {timeframe} data for {symbol}")
        
        try:
            # Import data fetching functionality - dynamic import to avoid circular dependencies
            import importlib
            vbt_spec = importlib.util.find_spec('vectorbtpro')
            
            if vbt_spec is None:
                logger.error("vectorbtpro module not found")
                return None
                
            vbt = importlib.import_module('vectorbtpro')
            
            # Get time range
            end_ts = int(time.time())
            start_ts = end_ts - (days * 86400)  # days in seconds
            
            # Fetch from Coinbase with timeout handling
            try:
                data = vbt.CCXTData.download(
                    symbols=symbol,
                    timeframe=timeframe,
                    start=start_ts,
                    end=end_ts,
                    exchange="coinbase"
                ).get()
                
                # Validate the fetched data
                if data is None or data.empty:
                    logger.error(f"No data returned from CCXT for {symbol} {timeframe}")
                    return None
                    
                # Ensure we have all required columns (case-insensitive)
                required_cols = ['open', 'high', 'low', 'close', 'volume']
                if not all(col.lower() in map(str.lower, data.columns) for col in required_cols):
                    # Try to fix column names if they're in a different case
                    for col in required_cols:
                        matches = [c for c in data.columns if c.lower() == col.lower()]
                        if matches and col not in data.columns:
                            data[col] = data[matches[0]]
                    
                # Final validation
                validate_dataframe(data, required_cols)
                
                # Save to cache
                try:
                    data.to_csv(cache_file)
                    logger.info(f"Data cached to {cache_file}")
                except Exception as e:
                    logger.warning(f"Could not cache data: {e}")
                
                return data
                
            except Exception as e:
                logger.error(f"Error downloading data from CCXT: {e}")
                return None
                
        except ImportError as e:
            logger.error(f"Required module not available: {e}")
            return None
    
    # Execute the inner function which has proper error handling
    return _fetch_data()


def calculate_wfo_parameters(timeframe, train_days, test_days):
    """
    Calculate WFO parameters based on timeframe and window sizes in days.
    
    Args:
        timeframe: Timeframe
        train_days: Training window size in days
        test_days: Testing window size in days
        
    Returns:
        Tuple of (train_points, test_points, step_points)
    """
    # Store inputs in local variables that can be safely accessed by the inner function
    tf = timeframe  # Create a copy for inner function to safely access
    tr_days = train_days
    tst_days = test_days
    
    # Map of timeframe to points per day - define outside inner function
    points_per_day = {
        '1m': 1440,   # 60 * 24
        '5m': 288,    # 12 * 24
        '15m': 96,    # 4 * 24
        '30m': 48,    # 2 * 24
        '1h': 24,     # 1 * 24
        '2h': 12,     # 0.5 * 24
        '4h': 6,      # 0.25 * 24
        '6h': 4,      # 0.167 * 24
        '8h': 3,      # 0.125 * 24
        '12h': 2,     # 0.083 * 24
        '1d': 1       # 1 day = 1 candle
    }
    
    try:
        # Without using the decorator, just handle errors directly
        # Get points per day for the timeframe with safety check
        if not tf or not isinstance(tf, str):
            logger.warning(f"Invalid timeframe: {tf}, defaulting to 1h")
            tf = '1h'
            
        ppd = points_per_day.get(tf.lower(), 24)  # default to 1h, case-insensitive
        
        # Validate inputs to avoid negative or zero values
        if tr_days <= 0 or tst_days <= 0:
            logger.warning(f"Invalid train_days ({tr_days}) or test_days ({tst_days}), using defaults")
            tr_days = max(tr_days, 30) if tr_days > 0 else 30
            tst_days = max(tst_days, 15) if tst_days > 0 else 15
        
        # Calculate points
        train_points = tr_days * ppd
        test_points = tst_days * ppd
        step_points = test_points  # Use test window size as step
        
        logger.info(f"Calculated WFO parameters: {train_points} train points, "
                   f"{test_points} test points, {step_points} step points")
        
        return train_points, test_points, step_points
    except Exception as e:
        logger.error(f"Error calculating WFO parameters: {str(e)}")
        # Return default values
        return 720, 360, 360


def objective(trial, data, train_points, test_points, step_points, symbol, timeframe, n_splits=3):
    """
    Objective function for Optuna.
    
    Args:
        trial: Optuna trial
        data: OHLCV data
        train_points: Training window size in points
        test_points: Testing window size in points
        step_points: Step size in points
        symbol: Trading symbol
        timeframe: Timeframe
        n_splits: Number of WFO splits
        
    Returns:
        Optimization score (higher is better)
    """
    # Import utilities within function to avoid circular dependencies
    from scripts.strategies.refactored_edge.utils import (
        validate_dataframe, safe_get_column, with_error_handling,
        ensure_config_attributes
    )
    
    # Nested inner function with error handling
    @with_error_handling(default_return=-np.inf)
    def _run_objective():
        # Validate input data first
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        # Check both lowercase and uppercase column names
        alt_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        all_columns = data.columns.tolist()
        
        # Check if we have required columns (either lowercase or uppercase)
        has_required = all(col in all_columns or alt.capitalize() in all_columns 
                          for col, alt in zip(required_columns, alt_columns))
        if not has_required:
            logger.warning(f"Missing required OHLCV columns in data - available: {all_columns}")
        
        # Save original WFO parameters
        # Import these modules dynamically to avoid circular dependencies
        from scripts.strategies.refactored_edge import wfo, wfo_utils
        
        original_wfo_train = getattr(wfo, 'WFO_TRAIN_POINTS', None)
        original_wfo_test = getattr(wfo, 'WFO_TEST_POINTS', None)
        original_wfo_step = getattr(wfo, 'STEP_POINTS', None)
        
        original_utils_train = getattr(wfo_utils, 'WFO_TRAIN_POINTS', None)
        original_utils_test = getattr(wfo_utils, 'WFO_TEST_POINTS', None)
        original_utils_step = getattr(wfo_utils, 'STEP_POINTS', None)
        
        try:
            # Override WFO parameters for this run
            if hasattr(wfo, 'WFO_TRAIN_POINTS'):
                wfo.WFO_TRAIN_POINTS = train_points
            if hasattr(wfo, 'WFO_TEST_POINTS'):
                wfo.WFO_TEST_POINTS = test_points
            if hasattr(wfo, 'STEP_POINTS'):
                wfo.STEP_POINTS = step_points
            
            if hasattr(wfo_utils, 'WFO_TRAIN_POINTS'):
                wfo_utils.WFO_TRAIN_POINTS = train_points
            if hasattr(wfo_utils, 'WFO_TEST_POINTS'):
                wfo_utils.WFO_TEST_POINTS = test_points
            if hasattr(wfo_utils, 'STEP_POINTS'):
                wfo_utils.STEP_POINTS = step_points
            
            # Dynamically import balanced signals to ensure we have the latest version
            from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
            from scripts.strategies.refactored_edge.config import EdgeConfig
            
            config_dict = {
                # RSI parameters
                'rsi_window': trial.suggest_int('rsi_window', 7, 21),
                'rsi_entry_threshold': trial.suggest_int('rsi_entry_threshold', 20, 40),
                'rsi_exit_threshold': trial.suggest_int('rsi_exit_threshold', 60, 80),
                
                # Bollinger Bands parameters
                'bb_window': trial.suggest_int('bb_window', 10, 30),
                'bb_std_dev': trial.suggest_float('bb_std_dev', 1.5, 3.0),
                
                # Trend MA parameters
                'trend_ma_window': trial.suggest_int('trend_ma_window', 20, 100),
                
                # ATR parameters
                'atr_window': trial.suggest_int('atr_window', 7, 21),
                
                # ADX parameters
                'adx_window': trial.suggest_int('adx_window', 7, 21),
                'adx_threshold': trial.suggest_float('adx_threshold', 15.0, 40.0),
                
                # Regime filter parameters
                'use_regime_filter': trial.suggest_categorical('use_regime_filter', [True, False]),
                'use_enhanced_regimes': trial.suggest_categorical('use_enhanced_regimes', [True, False])
            }
            
            # Optionally include Supply/Demand zones - preserved as per MEMORY
            config_dict['use_zones'] = trial.suggest_categorical('use_zones', [True, False])
            
            if config_dict['use_zones']:
                config_dict['zone_proximity_pct'] = trial.suggest_float('zone_proximity_pct', 0.001, 0.01)
            
            # Add signal balancing parameters (from asset profiles) - preserved as per MEMORY
            config_dict['signal_strictness'] = trial.suggest_categorical(
                'signal_strictness', 
                [SignalStrictness.STRICT, SignalStrictness.BALANCED, SignalStrictness.RELAXED]
            )
            
            # Configure signal parameters based on strictness level, as per MEMORY
            if config_dict['signal_strictness'] == SignalStrictness.STRICT:
                default_trend_threshold = 0.03
                default_zone_influence = 0.8
                default_min_hold = 4
            elif config_dict['signal_strictness'] == SignalStrictness.RELAXED:
                default_trend_threshold = 0.005
                default_zone_influence = 0.3
                default_min_hold = 1
            else:  # BALANCED
                default_trend_threshold = 0.015
                default_zone_influence = 0.5
                default_min_hold = 2
            
            # Add the parameters with defaults that match the strictness level
            config_dict['trend_threshold_pct'] = trial.suggest_float(
                'trend_threshold_pct', 0.005, 0.03, step=0.005, 
                log=False  # Linear scale for better coverage
            )
            
            config_dict['zone_influence'] = trial.suggest_float(
                'zone_influence', 0.1, 0.9, step=0.1
            )
            
            config_dict['min_hold_period'] = trial.suggest_int(
                'min_hold_period', 1, 5
            )
            
            # Create and validate config object
            config = EdgeConfig(**config_dict)
            
            # Ensure all required attributes are present
            required_config_attrs = [
                'rsi_window', 'bb_window', 'atr_window', 'adx_window',
                'signal_strictness', 'trend_threshold_pct', 'zone_influence', 'min_hold_period'
            ]
            ensure_config_attributes(config, required_config_attrs)
            
            # Import run_wfo dynamically to avoid circular dependencies
            from scripts.strategies.refactored_edge.wfo import run_wfo
            
            # Run WFO using the parameters it actually accepts
            wfo_results = run_wfo(
                data=data,       # Pre-fetched data
                config=config,  # Configuration with parameters
                n_splits=n_splits,  # Number of WFO splits
                symbol=symbol,     # Symbol for reporting
                timeframe=timeframe  # Timeframe for reporting
            )
            
            # Unpack the tuple returned by run_wfo with safety check
            if not isinstance(wfo_results, tuple) or len(wfo_results) != 3:
                logger.error(f"Unexpected WFO result format: {type(wfo_results)}")
                return -np.inf
                
            results_list, test_portfolios, all_best_params = wfo_results
            
            # Check if we have valid results
            if not results_list:
                logger.warning("WFO returned empty results list, returning -inf score.")
                return -np.inf
            
            # Calculate metrics from results with safety checks for missing data
            train_metrics = {'return': [], 'sharpe': [], 'max_drawdown': []}
            test_metrics = {'return': [], 'sharpe': [], 'max_drawdown': []}
            
            for result in results_list:
                # Safely get metrics, default to NaN if missing
                train_metrics['return'].append(result.get('train_return', np.nan))
                train_metrics['sharpe'].append(result.get('train_sharpe', np.nan))
                train_metrics['max_drawdown'].append(result.get('train_max_drawdown', np.nan))
                test_metrics['return'].append(result.get('test_return', np.nan))
                test_metrics['sharpe'].append(result.get('test_sharpe', np.nan))
                test_metrics['max_drawdown'].append(result.get('test_max_drawdown', np.nan))
            
            # Calculate aggregate metrics with safe handling of empty or all-NaN arrays
            def safe_mean(values):
                if not values or np.all(np.isnan(values)):
                    return np.nan
                return np.nanmean(values)
            
            avg_train_return = safe_mean(train_metrics['return'])
            avg_train_sharpe = safe_mean(train_metrics['sharpe'])
            avg_train_max_drawdown = safe_mean(train_metrics['max_drawdown'])
            avg_test_return = safe_mean(test_metrics['return'])
            avg_test_sharpe = safe_mean(test_metrics['sharpe'])
            avg_test_max_drawdown = safe_mean(test_metrics['max_drawdown'])
            
            # Calculate stability (standard deviation of test returns)
            test_returns = test_metrics['return']
            if len(test_returns) > 1 and not np.all(np.isnan(test_returns)):
                stability_std = np.nanstd(test_returns)
            else:
                stability_std = 0
            
            # Define the final score for Optuna - prioritize Sharpe, penalize instability
            # Ensure Sharpe is not NaN or infinite before using it
            if np.isfinite(avg_test_sharpe):
                score = avg_test_sharpe
                # Penalize score based on stability (higher std dev = more penalty)
                if stability_std > 1e-6: 
                    score -= (stability_std * 0.5)  # Adjust penalty weight as needed
            else:
                # Fallback score if Sharpe is invalid
                score = -np.inf
                
            # Record detailed metrics for analysis
            logger.debug(f"Trial {trial.number}: Avg Train Ret={avg_train_return:.4f}, "
                         f"Avg Test Sharpe={avg_test_sharpe:.4f}, Stability={stability_std:.4f}, "
                         f"Signal Mode={config_dict['signal_strictness']}, Final Score={score:.4f}")
            
            # Store attributes for later analysis
            trial.set_user_attr("avg_train_return", float(avg_train_return) if np.isfinite(avg_train_return) else -999.0)
            trial.set_user_attr("avg_test_sharpe", float(avg_test_sharpe) if np.isfinite(avg_test_sharpe) else -999.0)
            trial.set_user_attr("stability_std", float(stability_std) if np.isfinite(stability_std) else 999.0)
            trial.set_user_attr("signal_mode", str(config_dict['signal_strictness']))
            trial.set_user_attr("use_zones", config_dict['use_zones'])
            
            return score
            
        except optuna.exceptions.TrialPruned as e:
            logger.warning(f"Trial pruned: {e}")
            raise e  # Re-raise TrialPruned to let Optuna handle it appropriately
        finally:
            # Always restore original WFO parameters, even in case of errors
            if original_wfo_train is not None and hasattr(wfo, 'WFO_TRAIN_POINTS'):
                wfo.WFO_TRAIN_POINTS = original_wfo_train
            if original_wfo_test is not None and hasattr(wfo, 'WFO_TEST_POINTS'):
                wfo.WFO_TEST_POINTS = original_wfo_test
            if original_wfo_step is not None and hasattr(wfo, 'STEP_POINTS'):
                wfo.STEP_POINTS = original_wfo_step
                
            if original_utils_train is not None and hasattr(wfo_utils, 'WFO_TRAIN_POINTS'):
                wfo_utils.WFO_TRAIN_POINTS = original_utils_train
            if original_utils_test is not None and hasattr(wfo_utils, 'WFO_TEST_POINTS'):
                wfo_utils.WFO_TEST_POINTS = original_utils_test
            if original_utils_step is not None and hasattr(wfo_utils, 'STEP_POINTS'):
                wfo_utils.STEP_POINTS = original_utils_step
    
    # Execute the inner function which has its own error handling
    return _run_objective()


def save_study_visualizations(study, study_name):
    """
    Save visualization plots for the study.
    
    Args:
        study: Optuna study
        study_name: Name of the study
    """
    # Create study plots directory
    study_plots_dir = os.path.join(PLOTS_DIR, study_name)
    os.makedirs(study_plots_dir, exist_ok=True)
    
    try:
        # Optimization history
        fig = optuna.visualization.plot_optimization_history(study)
        fig.write_image(os.path.join(study_plots_dir, 'optimization_history.png'))
        
        # Parameter importances
        fig = optuna.visualization.plot_param_importances(study)
        fig.write_image(os.path.join(study_plots_dir, 'param_importances.png'))
        
        # Parallel coordinate plot
        fig = optuna.visualization.plot_parallel_coordinate(study)
        fig.write_image(os.path.join(study_plots_dir, 'parallel_coordinate.png'))
        
        # Try to save contour plot (may fail if not enough trials)
        try:
            fig = optuna.visualization.plot_contour(study)
            fig.write_image(os.path.join(study_plots_dir, 'contour.png'))
        except Exception as e:
            logger.warning(f"Could not generate contour plot: {e}")
        
        logger.info(f"Visualizations saved to {study_plots_dir}")
        
    except Exception as e:
        logger.error(f"Error saving visualizations: {e}")


def save_results(result, study_name):
    """
    Save optimization results to file.
    
    Args:
        result: Result dictionary
        study_name: Name of the study
    """
    # Save as JSON
    json_file = os.path.join(RESULTS_DIR, f"{study_name}_result.json")
    with open(json_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    # Save as CSV for easy viewing
    if 'best_params' in result and result['best_params']:
        params_df = pd.DataFrame([result['best_params']])
        params_df['best_value'] = result.get('best_value', np.nan)
        params_df['symbol'] = result.get('symbol', '')
        params_df['timeframe'] = result.get('timeframe', '')
        
        csv_file = os.path.join(RESULTS_DIR, f"{study_name}_params.csv")
        params_df.to_csv(csv_file, index=False)
    
    logger.info(f"Results saved to {json_file}")


def run_optuna_optimization(data, symbol, timeframe, n_trials=100, timeout=3600, n_splits=3, train_days=30, test_days=15,
                            signal_strictness=None, trend_threshold_pct=None, zone_influence=None, min_hold_period=None):
    """
    Run Optuna optimization with support for asset-specific configuration.
    
    This function is designed to work seamlessly with the asset profiles system,
    allowing for customized signal generation parameters for each asset based on
    its volatility profile.
    
    Args:
        data (pd.DataFrame): OHLCV DataFrame (already fetched)
        symbol (str): Trading symbol
        timeframe (str): Timeframe
        n_trials (int): Number of trials
        timeout (int): Timeout in seconds
        n_splits (int): Number of WFO splits
        train_days (int): Training window size in days
        test_days (int): Testing window size in days
        signal_strictness (SignalStrictness, optional): Asset-specific signal strictness level
        trend_threshold_pct (float, optional): Asset-specific trend threshold percentage
        zone_influence (float, optional): Asset-specific zone influence factor
        min_hold_period (int, optional): Asset-specific minimum holding period
        
    Returns:
        dict: Optimization results including status, parameters, and metrics
    """
    # Import utilities within function to avoid circular dependencies
    from scripts.strategies.refactored_edge.utils import (
        with_error_handling, validate_dataframe, ensure_config_attributes
    )
    
    @with_error_handling(default_return={"status": "failed", "error": "Unexpected error in optimization"})
    def _run_optimization():
        # Validate input data
        if data is None or data.empty:
            error_msg = "Data is None or empty"
            logger.error(error_msg)
            return {"status": "failed", "error": error_msg}
            
        # Validate data has required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        alt_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # Check if we have all required columns (case-insensitive)
        all_cols_lower = [col.lower() for col in data.columns]
        missing_cols = [col for col in required_cols if col.lower() not in all_cols_lower]
            
        if missing_cols:
            # Try to fix column names if they exist in a different case
            for col in missing_cols.copy():
                alt_col = next((c for c in data.columns if c.lower() == col.lower()), None)
                if alt_col:
                    data[col] = data[alt_col]
                    missing_cols.remove(col)
                    
        # If we still have missing columns, log and return an error
        if missing_cols:
            error_msg = f"Missing required columns: {missing_cols}. Available: {data.columns.tolist()}"
            logger.error(error_msg)
            return {"status": "failed", "error": error_msg}
        
        # Ensure output directories exist
        ensure_directories()
        
        # Calculate WFO parameters with improved error handling
        train_points, test_points, step_points = calculate_wfo_parameters(
            timeframe, train_days, test_days
        )
        
        # Log optimization parameters
        logger.info(f"Starting optimization for {symbol} ({timeframe})")
        logger.info(f"WFO parameters: {train_points} train points, "
                   f"{test_points} test points, {step_points} step points")
        logger.info(f"Using {n_splits} splits, {n_trials} trials, {timeout}s timeout")
        
        # Safely import balanced signals to avoid circular dependencies
        try:
            from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
        except ImportError as e:
            logger.warning(f"Could not import SignalStrictness: {e}. Asset-specific optimization may be limited.")
            # Create a fallback enum-like class if import fails
            class SignalStrictness:
                STRICT = "STRICT"
                BALANCED = "BALANCED"
                RELAXED = "RELAXED"
        
        # Log and validate asset-specific parameters
        asset_specific_params = {}
        
        # Validate signal_strictness - make a local copy to avoid scope issues
        local_signal_strictness = signal_strictness  
        if local_signal_strictness is not None:
            # Convert to string for storage if it's an enum
            if hasattr(local_signal_strictness, "value"):
                str_strictness = local_signal_strictness.value
            else:
                str_strictness = str(local_signal_strictness)
                
            asset_specific_params['signal_strictness'] = local_signal_strictness
            logger.info(f"Using asset-specific signal strictness: {str_strictness}")
            
        # Validate trend_threshold_pct - make a local copy to avoid scope issues
        local_trend_threshold = trend_threshold_pct
        if local_trend_threshold is not None:
            try:
                local_trend_val = float(local_trend_threshold)
                if local_trend_val < 0 or local_trend_val > 1:
                    logger.warning(f"trend_threshold_pct should be between 0 and 1, got {local_trend_val}")
                    local_trend_val = max(0, min(local_trend_val, 1))
                asset_specific_params['trend_threshold_pct'] = local_trend_val
                logger.info(f"Using asset-specific trend threshold: {local_trend_val}")
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid trend_threshold_pct: {e}, ignoring this parameter")
        
        # Validate zone_influence - make a local copy to avoid scope issues
        local_zone_influence = zone_influence
        if local_zone_influence is not None:
            try:
                zone_val = float(local_zone_influence)
                if zone_val < 0 or zone_val > 1:
                    logger.warning(f"zone_influence should be between 0 and 1, got {zone_val}")
                    zone_val = max(0, min(zone_val, 1))
                asset_specific_params['zone_influence'] = zone_val
                logger.info(f"Using asset-specific zone influence: {zone_val}")
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid zone_influence: {e}, ignoring this parameter")
        
        # Validate min_hold_period - make a local copy to avoid scope issues
        local_min_hold = min_hold_period
        if local_min_hold is not None:
            try:
                hold_val = int(local_min_hold)
                if hold_val < 1:
                    logger.warning(f"min_hold_period should be at least 1, got {hold_val}")
                    hold_val = max(1, hold_val)
                asset_specific_params['min_hold_period'] = hold_val
                logger.info(f"Using asset-specific min hold period: {hold_val}")
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid min_hold_period: {e}, ignoring this parameter")
        
        # Create unique study name with timestamp to avoid conflicts
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        study_name = f"{symbol}_{timeframe}_train{train_days}_test{test_days}_{timestamp}"
        
        try:
            # Safely create Optuna study with retry logic
            try:
                storage_name = f"sqlite:///{os.path.join(RESULTS_DIR, f'{study_name}.db')}"
                study = optuna.create_study(
                    direction="maximize", 
                    study_name=study_name,
                    storage=storage_name,
                    load_if_exists=True
                )
            except Exception as e:
                logger.warning(f"Failed to create study with SQLite storage: {e}. Using in-memory storage.")
                study = optuna.create_study(direction="maximize", study_name=study_name)
            
            # Create enhanced objective function with asset-specific handling
            def asset_specific_objective(trial):
                try:
                    # Call the main objective function
                    base_objective = objective(
                        trial, data, train_points, test_points, 
                        step_points, symbol, timeframe, n_splits
                    )
                    
                    # Apply weighted bonus for asset-specific parameters based on memory system
                    if asset_specific_params and hasattr(trial, 'params'):
                        bonus = 0.0
                        bonus_weights = {
                            'signal_strictness': 0.02,  # Higher weight for signal strictness
                            'trend_threshold_pct': 0.01,
                            'zone_influence': 0.01,
                            'min_hold_period': 0.01
                        }
                        
                        for param, value in asset_specific_params.items():
                            if param in trial.params and trial.params[param] == value:
                                # Apply weighted bonus for following asset-specific recommendations
                                bonus += bonus_weights.get(param, 0.01)
                                
                        # Add bonus to objective value
                        if np.isfinite(base_objective):
                            return base_objective + bonus
                    
                    return base_objective
                except optuna.exceptions.TrialPruned:
                    raise  # Re-raise pruned exception for Optuna
                except Exception as e:
                    logger.error(f"Error in asset_specific_objective for trial {trial.number}: {e}")
                    return -np.inf
            
            # Run optimization with progress tracking
            logger.info(f"Starting optimization with asset-specific parameters: {list(asset_specific_params.keys())}")
            study.optimize(
                asset_specific_objective, 
                n_trials=n_trials, 
                timeout=timeout,
                show_progress_bar=True
            )
            
            # Verify we have valid results
            if len(study.trials) == 0:
                logger.error("No trials completed successfully")
                return {"status": "failed", "error": "No trials completed successfully"}
            
            # Extract and validate best parameters
            try:
                best_params = study.best_params
                best_value = study.best_value
                
                # Check parameter validity
                if not best_params:
                    logger.warning("Best parameters not found, using first completed trial")
                    for trial in study.trials:
                        if trial.state == optuna.trial.TrialState.COMPLETE:
                            best_params = trial.params
                            best_value = trial.value
                            break
                
                # Incorporate asset-specific parameters into best_params for reporting
                for param, value in asset_specific_params.items():
                    if param not in best_params:
                        best_params[param] = value
                
                # Log best results
                logger.info(f"Optimization completed with best value: {best_value}")
                logger.info(f"Best parameters: {best_params}")
                
                # Save visualizations with error handling
                try:
                    save_study_visualizations(study, study_name)
                except Exception as e:
                    logger.warning(f"Error saving visualizations: {e}")
                
                # Build comprehensive result dictionary
                result = {
                    "status": "success",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "train_days": train_days,
                    "test_days": test_days,
                    "study_name": study_name,
                    "best_value": best_value,
                    "best_params": best_params,
                    "n_trials": n_trials,
                    "completed_trials": len(study.trials),
                    "successful_trials": len([t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]),
                    "failed_trials": len([t for t in study.trials if t.state == optuna.trial.TrialState.FAIL]),
                    "pruned_trials": len([t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED]),
                    "timestamp": datetime.datetime.now().isoformat(),
                    "asset_specific_params": asset_specific_params,
                    "wall_clock_time": f"{time.time() - study.trials[0].datetime_start.timestamp():.2f} seconds"
                }
                
                # Save results with error handling
                try:
                    save_results(result, study_name)
                except Exception as e:
                    logger.warning(f"Error saving results: {e}")
                
                return result
                
            except Exception as e:
                logger.error(f"Error extracting results: {e}")
                return {"status": "partial", "error": str(e), "completed_trials": len(study.trials)}
                
        except Exception as e:
            # Handle any unexpected errors during the optimization process
            logger.error(f"Error during optimization: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {"status": "failed", "error": str(e)}
    
    # Execute the inner function with proper error handling
    return _run_optimization()


def run_optimization(symbol, timeframe, train_days, test_days, n_trials=100, n_splits=3, timeout=3600):
    """
    Run Optuna optimization for a specific configuration.
    
    Args:
        symbol: Trading symbol
        timeframe: Timeframe
        train_days: Training window size in days
        test_days: Testing window size in days
        n_trials: Number of trials
        n_splits: Number of WFO splits
        timeout: Timeout in seconds
        
    Returns:
        Dict with optimization results
    """
    # Import utilities within function to avoid circular dependencies
    from scripts.strategies.refactored_edge.utils import with_error_handling, validate_dataframe
    
    @with_error_handling(default_return={"status": "failed", "error": "Unexpected error in optimization"})
    def _run_optimization():
        # Input validation
        if not symbol or not isinstance(symbol, str):
            logger.error(f"Invalid symbol: {symbol}")
            return {"status": "failed", "error": f"Invalid symbol: {symbol}"}
            
        if not timeframe or not isinstance(timeframe, str):
            logger.error(f"Invalid timeframe: {timeframe}")
            return {"status": "failed", "error": f"Invalid timeframe: {timeframe}"}
            
        # Log optimization parameters
        logger.info(f"Starting optimization for {symbol} ({timeframe}), "
                  f"train_days={train_days}, test_days={test_days}")
        
        # Ensure output directories exist
        ensure_directories()
        
        # Fetch data - now with improved error handling
        data = fetch_historical_data(symbol, timeframe)
        if data is None or data.empty:
            error_msg = "Failed to fetch data or data is empty"
            logger.error(f"{error_msg}, aborting optimization")
            return {"status": "failed", "error": error_msg}
        
        # Validate data has required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        try:
            validate_dataframe(data, required_cols)
        except Exception as e:
            error_msg = f"Data validation failed: {str(e)}"
            logger.error(error_msg)
            return {"status": "failed", "error": error_msg}
        
        # Calculate WFO parameters with improved error handling
        train_points, test_points, step_points = calculate_wfo_parameters(
            timeframe, train_days, test_days
        )
        
        # Verify calculated parameters are reasonable
        if train_points <= 0 or test_points <= 0:
            error_msg = f"Invalid WFO parameters: train_points={train_points}, test_points={test_points}"
            logger.error(error_msg)
            return {"status": "failed", "error": error_msg}
        
        # Create unique study name with timestamp to avoid conflicts
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        study_name = f"{symbol}_{timeframe}_train{train_days}_test{test_days}_{timestamp}"
        storage_name = f"sqlite:///{os.path.join(RESULTS_DIR, f'{study_name}.db')}"
        
        try:
            # Safely create Optuna study with retry logic
            try:
                study = optuna.create_study(
                    study_name=study_name,
                    storage=storage_name,
                    direction='maximize',
                    load_if_exists=True
                )
            except Exception as e:
                # If database creation fails, try with in-memory storage
                logger.warning(f"Failed to create study with SQLite storage: {e}. Using in-memory storage instead.")
                study = optuna.create_study(direction='maximize', study_name=study_name)
            
            # Run optimization with more detailed logging
            logger.info(f"Starting optimization with {n_trials} trials, timeout={timeout}s")
            
            # Create wrapped objective function with better error handling
            def safe_objective(trial):
                try:
                    return objective(
                        trial, data, train_points, test_points, step_points,
                        symbol, timeframe, n_splits
                    )
                except optuna.exceptions.TrialPruned:
                    # Re-raise pruned exceptions for Optuna's pruning mechanism
                    raise
                except Exception as e:
                    logger.error(f"Error in objective function for trial {trial.number}: {e}")
                    return -np.inf
            
            # Run optimization with progress tracking
            study.optimize(
                safe_objective,
                n_trials=n_trials,
                timeout=timeout,
                show_progress_bar=True
            )
            
            # Verify we have valid results
            if len(study.trials) == 0:
                logger.error("No trials completed successfully")
                return {"status": "failed", "error": "No trials completed successfully"}
            
            # Extract best parameters with validation
            try:
                best_params = study.best_params
                best_value = study.best_value
                
                # Check parameter validity (in case of unexpected trial behaviors)
                if not best_params or not isinstance(best_params, dict):
                    logger.warning("Best parameters not found or invalid, using first completed trial")
                    for trial in study.trials:
                        if trial.state == optuna.trial.TrialState.COMPLETE:
                            best_params = trial.params
                            best_value = trial.value
                            break
                
                # Final validation of parameters
                if not best_params or not isinstance(best_params, dict):
                    logger.error("Could not extract valid parameters from any trial")
                    return {"status": "partial", "error": "No valid parameters found", 
                            "completed_trials": len(study.trials)}
                
                logger.info(f"Optimization complete: best_value={best_value}")
                logger.info(f"Best parameters: {best_params}")
                
                # Save visualizations with error handling
                try:
                    save_study_visualizations(study, study_name)
                except Exception as e:
                    logger.warning(f"Error saving visualizations: {e}")
                
                # Build comprehensive result dictionary
                result = {
                    "status": "success",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "train_days": train_days,
                    "test_days": test_days,
                    "study_name": study_name,
                    "best_value": best_value,
                    "best_params": best_params,
                    "n_trials": n_trials,
                    "completed_trials": len(study.trials),
                    "successful_trials": len([t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]),
                    "failed_trials": len([t for t in study.trials if t.state == optuna.trial.TrialState.FAIL]),
                    "pruned_trials": len([t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED]),
                    "timestamp": datetime.datetime.now().isoformat(),
                    "wall_clock_time": f"{time.time() - study.trials[0].datetime_start.timestamp():.2f} seconds"
                }
                
                # Save results with error handling
                try:
                    save_results(result, study_name)
                except Exception as e:
                    logger.warning(f"Error saving results: {e}")
                
                return result
                
            except Exception as e:
                logger.error(f"Error extracting results: {e}")
                return {"status": "partial", "error": str(e), "completed_trials": len(study.trials)}
                
        except Exception as e:
            # Handle any unexpected errors during the optimization process
            logger.error(f"Error during optimization: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {"status": "failed", "error": str(e)}
    
    # Execute the inner function with proper error handling
    return _run_optimization()


def compare_with_default(best_params):
    """Compare optimized parameters with default parameters."""
    default_params = {
        'rsi_window': 14,
        'bb_window': 20,
        'bb_std_dev': 2.0,
        'ma_window': 50,
        'atr_window': 14,
        'rsi_entry_threshold': 30,
        'rsi_exit_threshold': 70,
        'adx_window': 14,
        'adx_threshold': 25.0,
        'use_regime_filter': False,
        'use_enhanced_regimes': False,
        'use_zones': False,
    }
    
    changes = []
    for param, default_val in default_params.items():
        if param in best_params:
            optimized_val = best_params[param]
            if default_val != optimized_val:
                changes.append(f"{param}: {default_val} → {optimized_val}")
    
    return changes


def main():
    """Main function for running Optuna optimization."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Optuna Optimization for Edge Strategy')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to optimize for')
    parser.add_argument('--timeframe', type=str, default='1h', help='Timeframe to optimize for')
    parser.add_argument('--train-days', type=int, default=30, help='Training window size in days')
    parser.add_argument('--test-days', type=int, default=15, help='Testing window size in days')
    parser.add_argument('--n-trials', type=int, default=50, help='Number of Optuna trials')
    parser.add_argument('--n-splits', type=int, default=3, help='Number of WFO splits')
    parser.add_argument('--timeout', type=int, default=1800, help='Timeout in seconds')
    
    args = parser.parse_args()
    
    # Enable testing mode for faster execution
    os.environ["REGIME_TESTING_MODE"] = "1"
    
    start_time = time.time()
    
    # Run optimization
    result = run_optimization(
        symbol=args.symbol,
        timeframe=args.timeframe,
        train_days=args.train_days,
        test_days=args.test_days,
        n_trials=args.n_trials,
        n_splits=args.n_splits,
        timeout=args.timeout
    )
    
    # Print final results
    elapsed_time = time.time() - start_time
    
    if result["status"] == "success":
        print("\n" + "=" * 80)
        print(f"Optimization completed successfully in {elapsed_time:.2f} seconds!")
        print(f"Best value (penalized Sharpe ratio): {result['best_value']}")
        print("\nBest parameters:")
        for param, value in result["best_params"].items():
            print(f"  {param}: {value}")
        
        print("\nParameter changes from default:")
        changes = compare_with_default(result["best_params"])
        if changes:
            for change in changes:
                print(f"  {change}")
        else:
            print("  No changes from default parameters")
        
        print("\nResults and visualizations saved to:")
        print(f"  {RESULTS_DIR}")
        print(f"  {PLOTS_DIR}/{result['study_name']}")
        print("=" * 80 + "\n")
    else:
        print("\n" + "=" * 80)
        print(f"Optimization failed after {elapsed_time:.2f} seconds")
        print(f"Error: {result.get('error', 'Unknown error')}")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
