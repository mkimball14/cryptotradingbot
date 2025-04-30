#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parameter Grid Test Runner for the Edge Multi-Factor Strategy.

This script runs a comprehensive test of the expanded parameter grid with a focus on:
1. RSI thresholds (30-40 for entries, 60-70 for exits)
2. Regime adaptation (trending vs. ranging market conditions)
3. Position sizing optimization (risk percentages and ATR multipliers)

The goal is to identify optimal parameter combinations for different market conditions
and compare the performance of regime-aware vs. standard approaches.
"""

import os
import sys
import logging
import time
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# Set up Python path
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

# Import required modules
from scripts.strategies.refactored_edge import (
    wfo, signals, indicators, regime, utils, config, balanced_signals
)
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.run_optuna_optimization import (
    run_optuna_optimization, fetch_historical_data, ensure_directories
)
from scripts.strategies.refactored_edge.run_wfo_real_data import run_real_data_wfo
# Also import data fetcher directly since we'll use it
from scripts.strategies.refactored_edge.data.data_fetcher import fetch_historical_data as fetch_data

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger('parameter_grid_test')

# Define output directories
OUTPUT_DIR = os.path.join(project_root, 'data', 'results', 'parameter_grid_test')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_expanded_grid_test(
    symbol: str = 'BTC-USD',
    timeframe: str = '1h',
    days: int = 120,
    n_trials: int = 30,
    use_regime_adaptation: bool = True
):
    """
    Run a test with the expanded parameter grid to find optimal RSI thresholds.
    
    Args:
        symbol: Trading symbol (default: 'BTC-USD')
        timeframe: Timeframe (default: '1h')
        days: Number of days of historical data to fetch (default: 120)
        n_trials: Number of Optuna trials (default: 30)
        use_regime_adaptation: Whether to use regime adaptation (default: True)
    """
    start_time = time.time()
    logger.info(f"Starting expanded grid test for {symbol} on {timeframe} timeframe")
    logger.info(f"Using {'regime-adaptive' if use_regime_adaptation else 'standard'} parameter approach")
    
    # Fetch historical data
    from datetime import datetime, timedelta
    
    # Calculate date range based on days parameter
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    logger.info(f"Fetching historical data for {symbol} on {timeframe} timeframe from {start_date} to {end_date}")
    
    # Get seconds for granularity
    granularity_seconds = None
    granularity_map = {
        '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
        '1h': 3600, '2h': 7200, '4h': 14400, '6h': 21600, '1d': 86400
    }
    granularity_seconds = granularity_map.get(timeframe, 3600)  # Default to 1h
    
    # Use the fetcher from the data module with the correct parameters
    data = fetch_data(symbol, start_date, end_date, granularity=granularity_seconds)
    if data is None or data.empty:
        logger.error("Failed to fetch historical data. Aborting test.")
        return None
    
    logger.info(f"Data shape: {data.shape}, Date range: {data.index[0]} to {data.index[-1]}")
    
    # Run Optuna optimization with expanded RSI threshold grid
    logger.info(f"Running Optuna optimization with {n_trials} trials")
    optuna_result = run_optuna_optimization(
        data=data,
        symbol=symbol,
        timeframe=timeframe,
        n_trials=n_trials,
        train_days=30,
        test_days=15,
        signal_strictness=None,  # Let Optuna explore all options
        trend_threshold_pct=None,
        zone_influence=None,
        min_hold_period=None,
    )
    
    if optuna_result is None or optuna_result.get('status') != 'success':
        logger.error(f"Optuna optimization failed: {optuna_result}")
        return None
    
    # Extract best parameters
    best_params = optuna_result.get('best_params', {})
    logger.info(f"Best parameters: {best_params}")
    
    # Save best parameters to CSV
    best_params_df = pd.DataFrame([best_params])
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    params_file = os.path.join(
        OUTPUT_DIR, 
        f"{symbol}_{timeframe}_{'regimeaware' if use_regime_adaptation else 'standard'}_params_{timestamp}.csv"
    )
    best_params_df.to_csv(params_file, index=False)
    logger.info(f"Saved best parameters to: {params_file}")
    
    # Run WFO test with best parameters
    logger.info("Running WFO test with best parameters")
    # Get data time frame for dates
    start_date = data.index[0].strftime('%Y-%m-%d')
    end_date = data.index[-1].strftime('%Y-%m-%d')
    
    # Run WFO with real data
    wfo_result, portfolios, wfo_best_params = run_real_data_wfo(
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        n_splits=3,
        train_ratio=0.7,  # 70% train, 30% test
        initial_capital=10000,
        n_jobs=-1,
        use_regime_filter=use_regime_adaptation,
        signal_strictness=best_params.get('signal_strictness', SignalStrictness.BALANCED)
    )
    
    # Save WFO results
    wfo_results_file = os.path.join(
        OUTPUT_DIR, 
        f"{symbol}_{timeframe}_{'regimeaware' if use_regime_adaptation else 'standard'}_wfo_{timestamp}.csv"
    )
    if wfo_result is not None and 'results_df' in wfo_result and wfo_result['results_df'] is not None:
        wfo_result['results_df'].to_csv(wfo_results_file, index=False)
        logger.info(f"Saved WFO results to: {wfo_results_file}")
    
    # Calculate regime-specific metrics
    logger.info("Calculating regime-specific performance metrics")
    regimes = regime.detect_market_regimes(data)
    regime_breakdown = perform_regime_analysis(wfo_result, regimes)
    
    # Log regime-specific performance
    logger.info("=== Regime-Specific Performance ===")
    for regime_type, metrics in regime_breakdown.items():
        logger.info(f"{regime_type} regime performance:")
        for metric_name, value in metrics.items():
            logger.info(f"  {metric_name}: {value}")
    
    # Save regime breakdown
    regime_file = os.path.join(
        OUTPUT_DIR, 
        f"{symbol}_{timeframe}_{'regimeaware' if use_regime_adaptation else 'standard'}_regimes_{timestamp}.csv"
    )
    pd.DataFrame([regime_breakdown]).to_csv(regime_file, index=False)
    logger.info(f"Saved regime breakdown to: {regime_file}")
    
    # Calculate total runtime
    elapsed_time = time.time() - start_time
    logger.info(f"Completed expanded grid test in {elapsed_time:.2f} seconds")
    
    return {
        'best_params': best_params,
        'wfo_result': wfo_result,
        'regime_breakdown': regime_breakdown,
        'runtime': elapsed_time,
        'params_file': params_file,
        'wfo_results_file': wfo_results_file,
        'regime_file': regime_file
    }

def perform_regime_analysis(wfo_result: Dict[str, Any], regimes: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Analyze performance metrics split by market regime.
    
    Args:
        wfo_result: Results from WFO test
        regimes: DataFrame with regime classifications
        
    Returns:
        Dictionary with regime-specific performance metrics
    """
    if wfo_result is None or 'portfolio' not in wfo_result:
        logger.error("Cannot perform regime analysis: missing portfolio in WFO result")
        return {}
    
    portfolio = wfo_result['portfolio']
    if portfolio is None:
        logger.error("Cannot perform regime analysis: portfolio is None")
        return {}
    
    # Extract trade data
    try:
        # Safely access trade data with error handling for API inconsistencies
        trade_records = utils.get_trade_records(portfolio)
        if trade_records is None or len(trade_records) == 0:
            logger.warning("No trades found for regime analysis")
            return {}
        
        trades_df = pd.DataFrame(trade_records)
    except Exception as e:
        logger.error(f"Error extracting trade data: {e}")
        return {}
    
    # Ensure we have datetime index for trades
    if 'entry_time' in trades_df.columns:
        trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time'])
        trades_df.set_index('entry_time', inplace=True)
    
    # Merge trades with regime data
    try:
        # Ensure regimes has datetime index
        if not isinstance(regimes.index, pd.DatetimeIndex):
            if 'timestamp' in regimes.columns:
                regimes['timestamp'] = pd.to_datetime(regimes['timestamp'])
                regimes.set_index('timestamp', inplace=True)
            elif 'date' in regimes.columns:
                regimes['date'] = pd.to_datetime(regimes['date'])
                regimes.set_index('date', inplace=True)
            else:
                logger.error("Cannot convert regimes to datetime index")
                return {}
        
        # Get relevant regime columns
        regime_col = 'predominant_regime'
        if regime_col not in regimes.columns:
            regime_col = 'regime'
            if regime_col not in regimes.columns:
                logger.error(f"No regime column found in {regimes.columns}")
                return {}
        
        # Join trades with the nearest regime data point
        trades_with_regimes = trades_df.join(regimes[regime_col], how='left')
        
        # Fill any missing values with closest regime data
        if trades_with_regimes[regime_col].isna().any():
            logger.warning("Some trades don't have regime data, using method='ffill'")
            trades_with_regimes[regime_col] = trades_with_regimes[regime_col].fillna(method='ffill')
        
        # Split trades by regime
        trending_trades = trades_with_regimes[trades_with_regimes[regime_col] == 'trending']
        ranging_trades = trades_with_regimes[trades_with_regimes[regime_col] == 'ranging']
        
        # Calculate metrics by regime
        result = {}
        
        # Trending regime metrics
        trending_count = len(trending_trades)
        trending_pnl = trending_trades['pnl'].sum() if trending_count > 0 else 0
        trending_win_rate = trending_trades['is_win'].mean() if trending_count > 0 else 0
        trending_avg_win = trending_trades[trending_trades['is_win']]['pnl'].mean() if trending_count > 0 and trending_trades['is_win'].sum() > 0 else 0
        trending_avg_loss = trending_trades[~trending_trades['is_win']]['pnl'].mean() if trending_count > 0 and (~trending_trades['is_win']).sum() > 0 else 0
        
        result['trending'] = {
            'trade_count': trending_count,
            'total_pnl': trending_pnl,
            'win_rate': trending_win_rate,
            'avg_win': trending_avg_win,
            'avg_loss': trending_avg_loss,
        }
        
        # Ranging regime metrics
        ranging_count = len(ranging_trades)
        ranging_pnl = ranging_trades['pnl'].sum() if ranging_count > 0 else 0
        ranging_win_rate = ranging_trades['is_win'].mean() if ranging_count > 0 else 0
        ranging_avg_win = ranging_trades[ranging_trades['is_win']]['pnl'].mean() if ranging_count > 0 and ranging_trades['is_win'].sum() > 0 else 0
        ranging_avg_loss = ranging_trades[~ranging_trades['is_win']]['pnl'].mean() if ranging_count > 0 and (~ranging_trades['is_win']).sum() > 0 else 0
        
        result['ranging'] = {
            'trade_count': ranging_count,
            'total_pnl': ranging_pnl,
            'win_rate': ranging_win_rate,
            'avg_win': ranging_avg_win,
            'avg_loss': ranging_avg_loss,
        }
        
        # Overall metrics
        total_count = trending_count + ranging_count
        result['overall'] = {
            'trade_count': total_count,
            'trending_pct': trending_count / total_count if total_count > 0 else 0,
            'ranging_pct': ranging_count / total_count if total_count > 0 else 0,
            'total_pnl': trending_pnl + ranging_pnl,
            'win_rate': trades_with_regimes['is_win'].mean() if total_count > 0 else 0,
        }
        
        return result
    
    except Exception as e:
        logger.error(f"Error in regime analysis: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {}

def run_comparative_tests():
    """
    Run comparative tests between standard and regime-aware approaches.
    
    This function:
    1. Runs tests with standard parameters (no regime adaptation)
    2. Runs tests with regime-aware parameters
    3. Compares the results between the two approaches
    """
    logger.info("=== Starting Comparative Parameter Tests ===")
    
    # Define symbols and timeframes to test
    symbols = ['BTC-USD', 'ETH-USD']
    timeframe = '1h'
    
    results = {}
    
    # Run tests for each symbol with and without regime adaptation
    for symbol in symbols:
        logger.info(f"Testing {symbol} on {timeframe} timeframe")
        
        # Run standard test (no regime adaptation)
        logger.info(f"Running standard test for {symbol}")
        standard_result = run_expanded_grid_test(
            symbol=symbol,
            timeframe=timeframe,
            days=120,
            n_trials=30,
            use_regime_adaptation=False
        )
        
        # Run regime-aware test
        logger.info(f"Running regime-aware test for {symbol}")
        regime_aware_result = run_expanded_grid_test(
            symbol=symbol,
            timeframe=timeframe,
            days=120,
            n_trials=30,
            use_regime_adaptation=True
        )
        
        results[symbol] = {
            'standard': standard_result,
            'regime_aware': regime_aware_result
        }
    
    # Compare and analyze results
    logger.info("=== Comparative Results ===")
    
    comparison_data = []
    
    for symbol, result_set in results.items():
        standard = result_set.get('standard', {})
        regime_aware = result_set.get('regime_aware', {})
        
        if not standard or not regime_aware:
            logger.warning(f"Missing results for {symbol}, skipping comparison")
            continue
        
        # Get overall metrics
        std_metrics = standard.get('regime_breakdown', {}).get('overall', {})
        ra_metrics = regime_aware.get('regime_breakdown', {}).get('overall', {})
        
        # Calculate performance differences
        pnl_diff = ra_metrics.get('total_pnl', 0) - std_metrics.get('total_pnl', 0)
        pnl_pct_diff = (pnl_diff / abs(std_metrics.get('total_pnl', 1))) * 100 if std_metrics.get('total_pnl', 0) != 0 else 0
        win_rate_diff = ra_metrics.get('win_rate', 0) - std_metrics.get('win_rate', 0)
        
        # Log comparison
        logger.info(f"=== {symbol} Comparison ===")
        logger.info(f"PnL: Standard={std_metrics.get('total_pnl', 0):.4f}, Regime-Aware={ra_metrics.get('total_pnl', 0):.4f}")
        logger.info(f"PnL Difference: {pnl_diff:.4f} ({pnl_pct_diff:.2f}%)")
        logger.info(f"Win Rate: Standard={std_metrics.get('win_rate', 0):.4f}, Regime-Aware={ra_metrics.get('win_rate', 0):.4f}")
        logger.info(f"Win Rate Difference: {win_rate_diff:.4f}")
        
        # Add to comparison data
        comparison_data.append({
            'symbol': symbol,
            'timeframe': timeframe,
            'standard_pnl': std_metrics.get('total_pnl', 0),
            'regime_aware_pnl': ra_metrics.get('total_pnl', 0),
            'pnl_diff': pnl_diff,
            'pnl_pct_diff': pnl_pct_diff,
            'standard_win_rate': std_metrics.get('win_rate', 0),
            'regime_aware_win_rate': ra_metrics.get('win_rate', 0),
            'win_rate_diff': win_rate_diff,
            'standard_trade_count': std_metrics.get('trade_count', 0),
            'regime_aware_trade_count': ra_metrics.get('trade_count', 0),
            'standard_trending_pct': std_metrics.get('trending_pct', 0),
            'regime_aware_trending_pct': ra_metrics.get('trending_pct', 0),
        })
    
    # Save comparison results
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        comparison_file = os.path.join(OUTPUT_DIR, f"regime_comparison_{timestamp}.csv")
        comparison_df.to_csv(comparison_file, index=False)
        logger.info(f"Saved comparison results to: {comparison_file}")
    
    logger.info("=== Comparative Tests Completed ===")
    return results

def test_position_sizing_parameters():
    """
    Test different position sizing parameters to analyze impact on risk-adjusted returns.
    
    This function:
    1. Tests different risk percentage levels (0.5%, 1%, 1.5%, 2%)
    2. Tests different ATR multipliers (1.0, 1.5, 2.0, 2.5, 3.0)
    3. Analyzes the impact on risk-adjusted returns
    """
    logger.info("=== Starting Position Sizing Parameter Tests ===")
    
    symbol = 'BTC-USD'
    timeframe = '1h'
    days = 120
    
    # Fetch data once for all tests
    data = fetch_historical_data(symbol, timeframe, days=days)
    if data is None:
        logger.error("Failed to fetch historical data. Aborting test.")
        return None
    
    # Get best parameters from previous optimization
    # For this test, we'll use a fixed set of parameters and only vary position sizing
    logger.info("Running Optuna optimization to get best base parameters")
    optuna_result = run_optuna_optimization(
        data=data,
        symbol=symbol,
        timeframe=timeframe,
        n_trials=20,
        train_days=30,
        test_days=15
    )
    
    if optuna_result is None or optuna_result.get('status') != 'success':
        logger.error(f"Optuna optimization failed: {optuna_result}")
        return None
    
    base_params = optuna_result.get('best_params', {})
    logger.info(f"Base parameters: {base_params}")
    
    # Define position sizing parameters to test
    risk_percentages = [0.005, 0.01, 0.015, 0.02]
    atr_multipliers = [1.0, 1.5, 2.0, 2.5, 3.0]
    
    results = []
    
    # Run tests for each combination of risk percentage and ATR multiplier
    for risk_pct in risk_percentages:
        for atr_mult in atr_multipliers:
            logger.info(f"Testing risk_percentage={risk_pct}, atr_multiplier={atr_mult}")
            
            # Create parameter set with current position sizing parameters
            test_params = base_params.copy()
            test_params['risk_percentage'] = risk_pct
            test_params['atr_multiplier'] = atr_mult
            test_params['use_dynamic_sizing'] = True
            
            # Run WFO test with current parameter set
            # Get data time frame for dates
            start_date = data.index[0].strftime('%Y-%m-%d')
            end_date = data.index[-1].strftime('%Y-%m-%d')
            
            # Temporarily modify the global parameter grid to test our specific risk settings
            # We'll save the original and restore it after the test
            original_grid = config.OPTIMIZATION_PARAMETER_GRID.copy()
            
            try:
                # Modify the global parameter grid to focus on our current risk parameters
                config.OPTIMIZATION_PARAMETER_GRID['risk_percentage'] = [risk_pct]
                if 'atr_multiplier' in config.OPTIMIZATION_PARAMETER_GRID:
                    config.OPTIMIZATION_PARAMETER_GRID['atr_multiplier'] = [atr_mult]
                config.OPTIMIZATION_PARAMETER_GRID['use_dynamic_sizing'] = [True]
                
                # Run WFO with real data using the modified grid
                wfo_result, portfolios, wfo_best_params = run_real_data_wfo(
                    symbol=symbol,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                    n_splits=3,
                    train_ratio=0.7,  # 70% train, 30% test
                    initial_capital=10000,
                    n_jobs=-1,
                    use_regime_filter=True,
                    signal_strictness=SignalStrictness.BALANCED
                )
            finally:
                # Restore the original parameter grid
                config.OPTIMIZATION_PARAMETER_GRID = original_grid.copy()
            
            # Extract performance metrics
            perf_metrics = {}
            if wfo_result and 'test_metrics' in wfo_result:
                test_metrics = wfo_result['test_metrics']
                perf_metrics = {
                    'risk_percentage': risk_pct,
                    'atr_multiplier': atr_mult,
                    'return': test_metrics.get('return', 0),
                    'sharpe': test_metrics.get('sharpe', 0),
                    'max_drawdown': test_metrics.get('max_drawdown', 0),
                    'calmar': test_metrics.get('calmar', 0),
                    'trade_count': test_metrics.get('trade_count', 0),
                    'risk_adjusted_return': test_metrics.get('return', 0) / (test_metrics.get('max_drawdown', 1) or 1)
                }
            
            results.append(perf_metrics)
            logger.info(f"Results: {perf_metrics}")
    
    # Convert results to DataFrame and save
    if results:
        results_df = pd.DataFrame(results)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        position_sizing_file = os.path.join(OUTPUT_DIR, f"{symbol}_{timeframe}_position_sizing_{timestamp}.csv")
        results_df.to_csv(position_sizing_file, index=False)
        logger.info(f"Saved position sizing results to: {position_sizing_file}")
        
        # Log best combinations by different metrics
        logger.info("=== Best Position Sizing Combinations ===")
        metrics = ['return', 'sharpe', 'risk_adjusted_return', 'calmar']
        for metric in metrics:
            if metric in results_df.columns:
                best_idx = results_df[metric].idxmax()
                best_combo = results_df.loc[best_idx]
                logger.info(f"Best by {metric}: risk_percentage={best_combo['risk_percentage']}, atr_multiplier={best_combo['atr_multiplier']}, {metric}={best_combo[metric]}")
    
    logger.info("=== Position Sizing Tests Completed ===")
    return results

def main():
    """Main function to run all tests."""
    logger.info("=== Starting Parameter Grid Tests ===")
    
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description='Parameter Grid Test Runner')
    parser.add_argument('--test-type', type=str, choices=['grid', 'regime', 'position'], default='all',
                       help='Type of test to run: grid (expanded RSI grid), regime (regime adaptation), position (position sizing), or all')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to test')
    parser.add_argument('--timeframe', type=str, default='1h', help='Timeframe to test')
    parser.add_argument('--days', type=int, default=120, help='Number of days of historical data')
    parser.add_argument('--trials', type=int, default=30, help='Number of Optuna trials')
    
    args = parser.parse_args()
    
    try:
        # Run selected tests
        if args.test_type in ['grid', 'all']:
            logger.info("Running expanded RSI threshold grid test")
            run_expanded_grid_test(
                symbol=args.symbol,
                timeframe=args.timeframe,
                days=args.days,
                n_trials=args.trials,
                use_regime_adaptation=True
            )
        
        if args.test_type in ['regime', 'all']:
            logger.info("Running regime adaptation comparison tests")
            run_comparative_tests()
        
        if args.test_type in ['position', 'all']:
            logger.info("Running position sizing parameter tests")
            test_position_sizing_parameters()
        
        logger.info("=== All Parameter Grid Tests Completed ===")
    
    except Exception as e:
        logger.error(f"Error in main: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
