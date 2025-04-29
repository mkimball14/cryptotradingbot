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


def fetch_historical_data(symbol, timeframe, days=365):
    """
    Fetch historical data for the specified symbol and timeframe.
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Timeframe (e.g., '1h', '4h')
        days: Number of days to fetch
        
    Returns:
        DataFrame with OHLCV data or None if fetch fails
    """
    try:
        # Same approach as in test_wfo_integration.py
        from scripts.strategies.refactored_edge.data.data_fetcher import fetch_historical_data as fetch_data, GRANULARITY_MAP_SECONDS
        
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        logger.info(f"Fetching {timeframe} data for {symbol} from {start_date.date()} to {end_date.date()}")
        
        # Convert timeframe string to seconds (granularity value)
        if timeframe in GRANULARITY_MAP_SECONDS:
            granularity_seconds = GRANULARITY_MAP_SECONDS[timeframe]
            logger.info(f"Using granularity: {timeframe} ({granularity_seconds} seconds)")
        else:
            logger.error(f"Unsupported timeframe: {timeframe}")
            return None
        
        data = fetch_data(
            product_id=symbol,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            granularity=granularity_seconds
        )
        
        if data is not None and len(data) > 0:
            logger.info(f"Successfully fetched {len(data)} data points for {symbol} ({timeframe})")
            return data
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
    
    logger.error(f"Failed to fetch data for {symbol} ({timeframe})")
    return None


def calculate_wfo_parameters(timeframe, train_days, test_days):
    """
    Calculate WFO parameters based on timeframe and window sizes.
    
    Args:
        timeframe: Timeframe (e.g., '1h', '4h')
        train_days: Training window size in days
        test_days: Testing window size in days
        
    Returns:
        Tuple of (train_points, test_points, step_points)
    """
    # Calculate points per day based on timeframe
    points_per_day = {
        '1m': 1440,
        '5m': 288,
        '15m': 96,
        '1h': 24,
        '4h': 6,
        '1d': 1,
    }
    
    ppd = points_per_day.get(timeframe, 24)  # Default to 1h if unknown
    
    train_points = train_days * ppd
    test_points = test_days * ppd
    step_points = test_points  # Use test window size as step size
    
    logger.info(f"Calculated WFO parameters for {timeframe}: "
               f"train_points={train_points}, test_points={test_points}, step_points={step_points}")
    
    return train_points, test_points, step_points


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
    # Save original WFO parameters
    original_wfo_train = getattr(wfo, 'WFO_TRAIN_POINTS', None)
    original_wfo_test = getattr(wfo, 'WFO_TEST_POINTS', None)
    original_wfo_step = getattr(wfo, 'STEP_POINTS', None)
    
    original_utils_train = getattr(wfo_utils, 'WFO_TRAIN_POINTS', None)
    original_utils_test = getattr(wfo_utils, 'WFO_TEST_POINTS', None)
    original_utils_step = getattr(wfo_utils, 'STEP_POINTS', None)
    
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
    
    # Optionally include Supply/Demand zones
    config_dict['use_zones'] = trial.suggest_categorical('use_zones', [True, False])
    
    if config_dict['use_zones']:
        config_dict['zone_proximity_pct'] = trial.suggest_float('zone_proximity_pct', 0.001, 0.01)
    
    # Add signal balancing parameters (from asset profiles)
    config_dict['signal_strictness'] = trial.suggest_categorical(
        'signal_strictness', 
        [SignalStrictness.STRICT, SignalStrictness.BALANCED, SignalStrictness.RELAXED]
    )
    
    # Add additional signal parameters with reasonable defaults based on strictness
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
        
    try:
        # Create config object
        config = EdgeConfig(**config_dict)
        
        # Run WFO using the parameters it actually accepts
        wfo_results = run_wfo(
            data=data,      # Pre-fetched data
            config=config,  # Configuration with parameters
            n_splits=n_splits,  # Number of WFO splits
            symbol=symbol,     # Symbol for reporting
            timeframe=timeframe  # Timeframe for reporting
            # Note: train_points and test_points will be used internally by run_wfo
            # based on the WFO constants that we modified at the beginning of this function
        )
        
        # Extract combined metrics from results
        combined_metrics = wfo_results['combined_metrics']
        
        if not combined_metrics:
            # Failed WFO run
            return -100.0  # Very negative value to indicate failure
        
        # Check for NaN or zero values in critical metrics
        sharpe_ratio = combined_metrics.get('sharpe_ratio', 0.0)
        if pd.isna(sharpe_ratio) or sharpe_ratio == 0.0:
            return -50.0  # Negative value to indicate bad metrics
        
        # Calculate trades per month (to avoid strategies that hardly trade)
        n_trades = combined_metrics.get('n_trades', 0)
        backtest_days = len(data) / 24  # Assuming hourly data
        trades_per_month = (n_trades / backtest_days) * 30  # 30 days in a month
        
        # Calculate trade rate penalty
        # - Too few trades (<1 per month) -> significant penalty
        # - Reasonable trade rate (1-10 per month) -> no penalty or slight bonus
        # - Too many trades (>10 per month) -> increasing penalty with trade frequency
        trade_rate_score = 0.0
        if trades_per_month < 1.0:
            trade_rate_score = -5.0 * (1.0 - trades_per_month)  # Penalize for too few trades
        elif trades_per_month <= 10.0:
            trade_rate_score = 0.2  # Small bonus for optimal trading frequency
        else:
            trade_rate_score = -0.2 * (trades_per_month - 10.0)  # Penalize for too many trades
        
        # Calculate win rate penalty
        win_rate = combined_metrics.get('win_rate', 0.0)
        win_rate_penalty = 0.0
        if win_rate < 0.4:
            win_rate_penalty = -10.0 * (0.4 - win_rate)  # Significant penalty for poor win rates
        
        # Calculate drawdown penalty
        max_drawdown = combined_metrics.get('max_drawdown', 1.0)
        drawdown_penalty = 0.0
        if max_drawdown > 0.2:  # 20% drawdown threshold
            drawdown_penalty = -5.0 * (max_drawdown - 0.2)  # Increasing penalty for large drawdowns
        
        # Calculate profit factor bonus
        profit_factor = combined_metrics.get('profit_factor', 1.0)
        profit_factor_bonus = 0.0
        if profit_factor > 1.5:  # Good profit factor
            profit_factor_bonus = 0.5 * (profit_factor - 1.5)  # Bonus for good profit factor
        
        # Calculate consistency score
        splits_return = wfo_results.get('splits_return', [])
        if len(splits_return) > 1:
            returns_std = np.std(splits_return)
            returns_mean = np.mean(splits_return)
            if returns_mean > 0 and returns_std > 0:
                # Lower coefficient of variation indicates more consistent returns
                cv = returns_std / returns_mean
                consistency_score = 1.0 / (1.0 + cv) - 0.5  # Range: -0.5 to 0.5
            else:
                consistency_score = -0.5  # Penalize negative or zero mean returns
        else:
            consistency_score = 0.0  # Neutral if only one split
        
        # Calculate number of consecutive losing splits
        losing_splits = [r < 0 for r in splits_return]
        max_consecutive_losses = 0
        current_streak = 0
        for is_loss in losing_splits:
            if is_loss:
                current_streak += 1
                max_consecutive_losses = max(max_consecutive_losses, current_streak)
            else:
                current_streak = 0
                
        consecutive_loss_penalty = -0.3 * max_consecutive_losses
        
        # Combine all components
        penalized_sharpe = (
            sharpe_ratio +          # Base score
            trade_rate_score +      # Trade frequency adjustment
            win_rate_penalty +      # Win rate quality
            drawdown_penalty +      # Drawdown risk
            profit_factor_bonus +   # Profit factor quality
            consistency_score +     # Consistency across splits
            consecutive_loss_penalty # Penalty for consecutive losses
        )
        
        # Log the results
        logger.info(f"Trial {trial.number}: penalized_sharpe={penalized_sharpe:.4f}, " 
                   f"sharpe={sharpe_ratio:.2f}, trades={n_trades}")
        
        return penalized_sharpe
    
    except Exception as e:
        logger.error(f"Error in objective function: {e}")
        return -10.0  # Negative value to indicate error
        
    finally:
        # Restore original WFO parameters
        if original_wfo_train is not None and hasattr(wfo, 'WFO_TRAIN_POINTS'):
            wfo.WFO_TRAIN_POINTS = original_wfo_train
        if original_wfo_test is not None and hasattr(wfo, 'WFO_TEST_POINTS'):
            wfo.WFO_TEST_POINTS = original_wfo_test
        if original_wfo_step is not None and hasattr(wfo, 'STEP_POINTS'):
            wfo.STEP_POINTS = original_wfo_step
        
        # Restore original WFO utils parameters
        if original_utils_train is not None and hasattr(wfo_utils, 'WFO_TRAIN_POINTS'):
            wfo_utils.WFO_TRAIN_POINTS = original_utils_train
        if original_utils_test is not None and hasattr(wfo_utils, 'WFO_TEST_POINTS'):
            wfo_utils.WFO_TEST_POINTS = original_utils_test
        if original_utils_step is not None and hasattr(wfo_utils, 'STEP_POINTS'):
            wfo_utils.STEP_POINTS = original_utils_step


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
        data: OHLCV DataFrame (already fetched)
        symbol: Trading symbol
        timeframe: Timeframe
        n_trials: Number of trials
        timeout: Timeout in seconds
        n_splits: Number of WFO splits
        train_days: Training window size in days
        test_days: Testing window size in days
        signal_strictness: Optional asset-specific signal strictness level
        trend_threshold_pct: Optional asset-specific trend threshold percentage
        zone_influence: Optional asset-specific zone influence factor
        min_hold_period: Optional asset-specific minimum holding period
        
    Returns:
        Dict with optimization results
    """
    try:
        # Ensure output directories exist
        ensure_directories()
        
        # Calculate WFO parameters
        train_points, test_points, step_points = calculate_wfo_parameters(
            timeframe, train_days, test_days
        )
        
        # Log optimization parameters
        logger.info(f"Starting optimization for {symbol} ({timeframe})")
        logger.info(f"WFO parameters: {train_points} train points, "
                   f"{test_points} test points, {step_points} step points")
        logger.info(f"Using {n_splits} splits, {n_trials} trials, {timeout}s timeout")
        
        # Log asset-specific parameters if provided
        asset_specific_params = {}
        if signal_strictness is not None:
            asset_specific_params['signal_strictness'] = signal_strictness
            logger.info(f"Using asset-specific signal strictness: {signal_strictness}")
        if trend_threshold_pct is not None:
            asset_specific_params['trend_threshold_pct'] = trend_threshold_pct
            logger.info(f"Using asset-specific trend threshold: {trend_threshold_pct}")
        if zone_influence is not None:
            asset_specific_params['zone_influence'] = zone_influence
            logger.info(f"Using asset-specific zone influence: {zone_influence}")
        if min_hold_period is not None:
            asset_specific_params['min_hold_period'] = min_hold_period
            logger.info(f"Using asset-specific min hold period: {min_hold_period}")
        
        # Create unique study name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        study_name = f"{symbol}_{timeframe}_train{train_days}_test{test_days}_{timestamp}"
        
        # Create Optuna study
        study = optuna.create_study(direction="maximize", study_name=study_name)
        
        # Modify objective function to incorporate asset-specific parameters
        def asset_specific_objective(trial):
            # Call the main objective function with asset-specific parameter hints
            base_objective = objective(trial, data, train_points, test_points, 
                                      step_points, symbol, timeframe, n_splits)
            
            # If we have asset-specific parameters, give a bonus to trials that use them
            if asset_specific_params and hasattr(trial, 'params'):
                bonus = 0.0
                for param, value in asset_specific_params.items():
                    if param in trial.params and trial.params[param] == value:
                        # Small bonus for following asset-specific recommendations
                        bonus += 0.01
                return base_objective + bonus
            
            return base_objective
        
        # Run optimization
        study.optimize(asset_specific_objective, n_trials=n_trials, timeout=timeout)
        
        # Get best parameters and value
        best_params = study.best_params
        best_value = study.best_value
        
        # Incorporate asset-specific parameters into best_params for reporting
        for param, value in asset_specific_params.items():
            if param not in best_params:
                best_params[param] = value
        
        # Log best results
        logger.info(f"Optimization completed with best value: {best_value}")
        logger.info(f"Best parameters: {best_params}")
        
        # Save visualizations
        save_study_visualizations(study, study_name)
        
        # Build result dictionary
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
            "timestamp": datetime.datetime.now().isoformat(),
            "asset_specific_params": asset_specific_params
        }
        
        # Save results
        save_results(result, study_name)
        
        return result
    
    except Exception as e:
        logger.error(f"Error during optimization: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"status": "failed", "error": str(e)}


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
    logger.info(f"Starting optimization for {symbol} ({timeframe}), "
              f"train_days={train_days}, test_days={test_days}")
    
    # Ensure output directories exist
    ensure_directories()
    
    # Fetch data
    data = fetch_historical_data(symbol, timeframe)
    if data is None:
        logger.error("Failed to fetch data, aborting optimization")
        return {"status": "failed", "error": "No data"}
    
    # Calculate WFO parameters
    train_points, test_points, step_points = calculate_wfo_parameters(
        timeframe, train_days, test_days
    )
    
    # Create study name and storage
    study_name = f"{symbol}_{timeframe}_train{train_days}_test{test_days}"
    storage_name = f"sqlite:///{os.path.join(RESULTS_DIR, f'{study_name}.db')}"
    
    try:
        # Create study
        study = optuna.create_study(
            study_name=study_name,
            storage=storage_name,
            direction='maximize',
            load_if_exists=True
        )
        
        # Run optimization
        logger.info(f"Starting optimization with {n_trials} trials, timeout={timeout}s")
        study.optimize(
            lambda trial: objective(
                trial, data, train_points, test_points, step_points,
                symbol, timeframe, n_splits
            ),
            n_trials=n_trials,
            timeout=timeout,
            show_progress_bar=True
        )
        
        # Get best parameters
        best_params = study.best_params
        best_value = study.best_value
        
        logger.info(f"Optimization complete: best_value={best_value}")
        logger.info(f"Best parameters: {best_params}")
        
        # Save visualizations
        save_study_visualizations(study, study_name)
        
        # Build result dictionary
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
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Save results
        save_results(result, study_name)
        
        return result
        
    except Exception as e:
        logger.error(f"Error during optimization: {e}")
        return {"status": "failed", "error": str(e)}


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
