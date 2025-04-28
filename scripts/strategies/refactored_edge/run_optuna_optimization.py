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
    # Define the parameter space
    params = {
        'rsi_window': trial.suggest_int('rsi_window', 5, 30),
        'bb_window': trial.suggest_int('bb_window', 10, 50),
        'bb_std_dev': trial.suggest_float('bb_std_dev', 1.0, 3.0),
        'ma_window': trial.suggest_int('ma_window', 20, 200),
        'atr_window': trial.suggest_int('atr_window', 5, 30),
        'atr_window_sizing': trial.suggest_int('atr_window_sizing', 5, 30),
        'rsi_entry_threshold': trial.suggest_int('rsi_entry_threshold', 20, 40),
        'rsi_exit_threshold': trial.suggest_int('rsi_exit_threshold', 60, 80),
        'adx_window': trial.suggest_int('adx_window', 5, 30),
        'adx_threshold': trial.suggest_float('adx_threshold', 15.0, 35.0),
        'use_regime_filter': trial.suggest_categorical('use_regime_filter', [True, False]),
        'use_enhanced_regimes': trial.suggest_categorical('use_enhanced_regimes', [True, False]),
        'use_zones': trial.suggest_categorical('use_zones', [True, False]),
    }
    
    try:
        # Create config from params
        config_obj = EdgeConfig(**params)
        
        # Save original WFO parameters
        original_wfo_train = wfo.WFO_TRAIN_POINTS
        original_wfo_test = wfo.WFO_TEST_POINTS
        original_wfo_step = wfo.STEP_POINTS
        
        original_utils_train = wfo_utils.WFO_TRAIN_POINTS
        original_utils_test = wfo_utils.WFO_TEST_POINTS
        original_utils_step = wfo_utils.STEP_POINTS
        
        # Override WFO parameters for this run
        wfo.WFO_TRAIN_POINTS = train_points
        wfo.WFO_TEST_POINTS = test_points
        wfo.STEP_POINTS = step_points
        
        wfo_utils.WFO_TRAIN_POINTS = train_points
        wfo_utils.WFO_TEST_POINTS = test_points
        wfo_utils.STEP_POINTS = step_points
        
        try:
            # Run WFO with these parameters
            results, portfolios, best_params = run_wfo(
                symbol=symbol,
                timeframe=timeframe,
                data=data,
                config=config_obj,
                n_splits=n_splits,
                n_jobs=1  # Use single process within Optuna
            )
            
            # Extract different metrics from results
            sharpe_ratios = [res.get('test_sharpe_ratio', float('-inf')) for res in results]
            returns = [res.get('test_return_pct', 0.0) for res in results]
            win_rates = [res.get('test_win_rate', 0.0) for res in results]
            trade_counts = [res.get('test_trade_count', 0) for res in results]
            
            # Check if we have any valid metrics
            valid_sharpes = [s for s in sharpe_ratios if s != float('-inf') and not np.isnan(s)]
            valid_returns = [r for r in returns if r != float('-inf') and not np.isnan(r)]
            
            # Calculate overall score based on available metrics
            if len(valid_sharpes) > 0:
                # Ideal case: We have valid Sharpe ratios
                avg_sharpe = np.mean(valid_sharpes)
                stability_ratio = len(valid_sharpes) / len(sharpe_ratios)
                score = avg_sharpe * stability_ratio
            elif sum(trade_counts) > 0:
                # Less ideal: At least we have some trades, use returns
                avg_return = np.mean([r for r, c in zip(returns, trade_counts) if c > 0] or [0])
                avg_win_rate = np.mean([w for w, c in zip(win_rates, trade_counts) if c > 0] or [0.5])
                # Construct a score that prefers higher returns and win rates
                score = (avg_return * 0.01) * (avg_win_rate * 2)  # Scale to be in a similar range as Sharpe
                stability_ratio = sum(1 for c in trade_counts if c > 0) / len(trade_counts)
            else:
                # No valid trades at all
                logger.warning(f"Trial {trial.number}: No valid trades generated with these parameters")
                # Return a small negative value so it's not completely rejected but ranked low
                return -1.0
            
            # Store additional info in trial
            trial.set_user_attr('valid_splits', len(valid_sharpes))
            trial.set_user_attr('total_splits', len(sharpe_ratios))
            trial.set_user_attr('stability', stability_ratio)
            trial.set_user_attr('avg_sharpe', np.mean(valid_sharpes) if valid_sharpes else float('nan'))
            trial.set_user_attr('avg_return', np.mean(valid_returns) if valid_returns else float('nan'))
            trial.set_user_attr('total_trades', sum(trade_counts))
            
            logger.info(f"Trial {trial.number}: score={score:.4f}, "
                      f"stability={stability_ratio:.2f}, "
                      f"trades={sum(trade_counts)}")
            
            return score
            
        finally:
            # Restore original parameters
            wfo.WFO_TRAIN_POINTS = original_wfo_train
            wfo.WFO_TEST_POINTS = original_wfo_test
            wfo.STEP_POINTS = original_wfo_step
            
            wfo_utils.WFO_TRAIN_POINTS = original_utils_train
            wfo_utils.WFO_TEST_POINTS = original_utils_test
            wfo_utils.STEP_POINTS = original_utils_step
            
    except Exception as e:
        logger.error(f"Error in trial {trial.number}: {e}")
        return float('-inf')


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


def run_optimization(symbol, timeframe, train_days, test_days, n_trials=100, n_splits=3, timeout=3600):
    """
    Run Optuna optimization for a specific configuration.
    
    Args:
        symbol: Trading symbol
        timeframe: Timeframe
        train_days: Training window size in days
        test_days: Testing window size in days
        n_trials: Number of trials to run
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
