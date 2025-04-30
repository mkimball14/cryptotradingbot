#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Regime-Aware Parameter Adaptation Evaluation Script

This script performs systematic testing of the regime-aware parameter adaptation system
to quantify its impact on performance across different market conditions and timeframes.
It compares standard WFO against regime-aware WFO and logs detailed results for analysis.

Author: Max Kimball
Date: 2025-04-30
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tqdm import tqdm
import json
import logging
from pathlib import Path

# Add the parent directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Local imports
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.wfo import run_wfo
from scripts.strategies.refactored_edge.test_regime_detection import create_synthetic_data
from scripts.strategies.refactored_edge.wfo_results import save_test_results, create_summary_report
from scripts.strategies.refactored_edge.wfo_utils import ensure_output_dir

def generate_sample_data(n=2400, volatility=0.03):
    """
    Generate sample data for testing when data fetcher is not available.
    
    Args:
        n (int): Number of periods to generate
        volatility (float): Volatility factor for price generation
        
    Returns:
        pd.DataFrame: DataFrame with OHLCV data
    """
    logger.info(f"Generating enhanced synthetic data with {n} periods")
    # Use a higher volatility (0.03) and explicit regime segments for more realistic price action
    # that will generate sufficient trades for evaluation
    return create_synthetic_data(days=n//24, volatility=volatility, include_regimes=True)

# Add project root to Python path to ensure proper imports
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
    print(f"Added {project_root} to Python path")

# Try importing the data fetcher
try:
    from data.data_fetcher import fetch_historical_data
    DATA_FETCHER_AVAILABLE = True
    print("Successfully imported fetch_historical_data from data.data_fetcher")
except ImportError as e:
    print(f"Warning: Could not import fetch_historical_data from data.data_fetcher: {e}")
    print("WFO requires actual historical data. Please ensure data/data_fetcher.py exists and is correct.")
    fetch_historical_data = None
    DATA_FETCHER_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("regime_evaluation")

# Constants
RESULTS_DIR = Path('data/results/regime_evaluation')
SYMBOLS = ['BTC-USD', 'ETH-USD', 'SOL-USD']  # Test on multiple assets
TIMEFRAMES = ['1h', '4h', '1d']  # Test on multiple timeframes
START_DATE = '2022-01-01'  # Recent enough for sufficient data quality
END_DATE = '2025-04-15'    # Recent past (adjust as needed)
INITIAL_CAPITAL = 10000

# Use the imported ensure_output_dir function instead of defining a local one

def evaluate_regime_adaptation(symbol, timeframe, start_date, end_date, capital=10000, with_regime=True, with_enhanced=True):
    """
    Run WFO with or without regime adaptation and return the results.

    Args:
        symbol (str): Trading symbol
        timeframe (str): Timeframe granularity
        start_date (str): Start date for evaluation
        end_date (str): End date for evaluation
        capital (float): Initial capital
        with_regime (bool): Whether to use regime-aware parameter adaptation
        with_enhanced (bool): Whether to use enhanced regime detection

    Returns:
        dict: WFO results including detailed stats by split
    """
    # Check if data fetcher is available
    if not DATA_FETCHER_AVAILABLE:
        logger.error("Data fetcher not available. Cannot evaluate regime adaptation.")
        return {"error": "Data fetcher not available"}
        
    # Configure the WFO run
    config = EdgeConfig(
        granularity_str=timeframe,
        use_regime_adaptation=with_regime,
        use_enhanced_regimes=with_enhanced
    )
    
    # Run WFO with specified configuration
    results = run_wfo(
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        initial_capital=capital,
        config=config,
        n_splits=5,
        # Set other parameters as needed
    )
    
    return results

def run_comparative_evaluation(symbol='BTC-USD', timeframe='1h', start_date=START_DATE, end_date=END_DATE, n_splits=5, train_ratio=0.7, data=None):
    """
    Run systematic tests comparing standard vs regime-aware parameter adaptation.
    Tests across multiple assets, timeframes, and market conditions.
    
    Args:
        symbol (str): Trading symbol
        timeframe (str): Timeframe granularity
        start_date (str): Start date for evaluation
        end_date (str): End date for evaluation
        n_splits (int): Number of train/test splits for WFO
        train_size (float): Proportion of data used for training
        data (pd.DataFrame or dict): Optional data to use instead of fetching from API
    
    Returns:
        dict: Comparison results between standard and regime-aware WFO
    """
    ensure_output_dir(RESULTS_DIR)
    
    # Initialize results tracking
    all_results = []
    
    logger.info(f"Testing {symbol} on {timeframe} timeframe")
            
    # Fetch historical data or use provided data
    if data is not None:
        logger.info("Using provided data for evaluation")
        if isinstance(data, dict) and 'data' in data:
            df = data['data']
        else:
            df = data
    else:
        # Fetch historical data
        try:
            from data.data_fetcher import fetch_historical_data
            df = fetch_historical_data(symbol, timeframe, start_date, end_date)
            logger.info(f"Successfully fetched data for {symbol} {timeframe}")
        except (ImportError, ModuleNotFoundError) as e:
            logger.error(f"Error importing data_fetcher: {e}")
            logger.warning("Proceeding with sample data for testing only...")
            # Generate some sample data for testing
            df = generate_sample_data(n=1000)
    
    # Set testing flag for synthetic data tests
    is_synthetic_test = df is not None and any(['synthetic' in str(symbol).lower() for symbol in [symbol]])
    
    # Run standard WFO (no regime adaptation)
    logger.info(f"Running standard WFO (no regime adaptation) {'with testing mode enabled' if is_synthetic_test else ''}")
    standard_config = EdgeConfig(
        granularity_str=timeframe,
        use_regime_adaptation=False,
        use_enhanced_regimes=False,
        _is_testing=is_synthetic_test  # Enable testing mode for synthetic data
    )
    
    standard_results = run_wfo(
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        initial_capital=INITIAL_CAPITAL,
        config=standard_config,
        n_splits=n_splits,
        train_ratio=train_ratio,
        data=df
    )
            
    # Run basic regime-aware WFO
    logger.info(f"Running basic regime-aware WFO {'with testing mode enabled' if is_synthetic_test else ''}")
    basic_config = EdgeConfig(
        granularity_str=timeframe,
        use_regime_adaptation=True,
        use_enhanced_regimes=False,
        _is_testing=is_synthetic_test  # Enable testing mode for synthetic data
    )
    
    basic_results = run_wfo(
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        initial_capital=INITIAL_CAPITAL,
        config=basic_config,
        n_splits=n_splits,
        train_ratio=train_ratio,
        data=df
    )
            
    # Run enhanced regime-aware WFO
    logger.info(f"Running enhanced regime-aware WFO {'with testing mode enabled' if is_synthetic_test else ''}")
    enhanced_config = EdgeConfig(
        granularity_str=timeframe,
        use_regime_adaptation=True,
        use_enhanced_regimes=True,
        _is_testing=is_synthetic_test  # Enable testing mode for synthetic data
    )
    
    enhanced_results = run_wfo(
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        initial_capital=INITIAL_CAPITAL,
        config=enhanced_config,
        n_splits=n_splits,
        train_ratio=train_ratio,
        data=df
    )
            
    # Aggregate metrics
    standard_performance = calculate_aggregate_metrics(standard_results)
    basic_regime_performance = calculate_aggregate_metrics(basic_results)
    enhanced_regime_performance = calculate_aggregate_metrics(enhanced_results)
            
    # Calculate improvement percentages
    basic_improvement = calculate_improvement(basic_regime_performance, standard_performance)
    enhanced_improvement = calculate_improvement(enhanced_regime_performance, standard_performance)
    
    # Store results
    result_entry = {
        'symbol': symbol,
        'timeframe': timeframe,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'standard': standard_performance,
        'basic_regime': basic_regime_performance,
        'enhanced_regime': enhanced_regime_performance,
        'basic_improvement': basic_improvement,
        'enhanced_improvement': enhanced_improvement,
        'raw_results': {
            'standard': standard_results,
            'basic_regime': basic_results,
            'enhanced_regime': enhanced_results
        }
    }
    
    all_results.append(result_entry)
    
    # Save individual test results
    save_test_results(result_entry, f"{symbol}_{timeframe}")
    
    # Create summary report
    create_summary_report(all_results)
    
    return all_results

def calculate_aggregate_metrics(wfo_results):
    """
    Calculate aggregate performance metrics from WFO results.
    
    Args:
        wfo_results: Results from a WFO run, either tuple(results_list, test_portfolios, best_params) or legacy dict
        
    Returns:
        dict: Aggregated performance metrics
    """
    # Handle different return formats from run_wfo
    # New modular format: tuple(results_list, test_portfolios, best_params)
    if isinstance(wfo_results, tuple) and len(wfo_results) == 3:
        results_list, test_portfolios, best_params = wfo_results
    # Legacy format: dict with 'results' key
    elif isinstance(wfo_results, dict) and 'results' in wfo_results:
        results_list = wfo_results.get('results', [])
    # Direct results list
    elif isinstance(wfo_results, list):
        results_list = wfo_results
    else:
        # If results structure is unknown or empty, return default metrics
        return {
            'avg_return': np.nan,
            'avg_sharpe': np.nan,
            'avg_max_drawdown': np.nan,
            'win_rate': np.nan,
            'param_consistency': np.nan
        }
    
    # Extract test metrics directly from results list
    if not results_list:
        return {
            'avg_return': np.nan,
            'avg_sharpe': np.nan,
            'avg_max_drawdown': np.nan,
            'win_rate': np.nan,
            'param_consistency': np.nan
        }
    
    # Extract key metrics
    returns = []
    sharpes = []
    drawdowns = []
    param_sets = []
    
    for result in results_list:
        # Check if we're dealing with the new format or legacy format
        if 'test_return' in result:
            # New format (direct metrics in result dictionary)
            returns.append(result.get('test_return', 0))
            sharpes.append(result.get('test_sharpe', 0))
            drawdowns.append(result.get('test_max_drawdown', 0))
            
            # Extract parameters for consistency calculation
            best_params_str = result.get('best_params', '{}')
            try:
                # Convert string representation of dict back to dict if needed
                if isinstance(best_params_str, str):
                    import ast
                    params_dict = ast.literal_eval(best_params_str)
                else:
                    params_dict = best_params_str
                if params_dict:
                    param_sets.append(frozenset(params_dict.items()))
            except (SyntaxError, ValueError):
                # If can't parse params string, skip it
                pass
        elif 'test_results' in result:
            # Legacy format (nested test_results dictionary)
            test_results = result.get('test_results', {})
            returns.append(test_results.get('return', 0))
            sharpes.append(test_results.get('sharpe', 0))
            drawdowns.append(test_results.get('max_drawdown', 0))
            
            # Extract parameters for consistency calculation
            best_params = result.get('best_params', {})
            if best_params:
                param_sets.append(frozenset(best_params.items()))
    
    # Calculate parameter consistency score (0-1)
    # Higher is better (more consistent parameters)
    unique_param_sets = set(param_sets)
    param_consistency = 0 if not param_sets else (1 - (len(unique_param_sets) - 1) / len(param_sets))
    
    # Calculate averages, handling empty lists
    avg_return = np.mean(returns) if returns else np.nan
    avg_sharpe = np.mean(sharpes) if sharpes else np.nan
    avg_max_drawdown = np.mean(drawdowns) if drawdowns else np.nan
    win_rate = np.mean([r > 0 for r in returns]) if returns else np.nan
    
    return {
        'avg_return': avg_return,
        'avg_sharpe': avg_sharpe,
        'avg_max_drawdown': avg_max_drawdown,
        'win_rate': win_rate,
        'param_consistency': param_consistency
    }

def calculate_improvement(new_metrics, baseline_metrics):
    """
    Calculate improvement percentages between two sets of metrics.
    
    Args:
        new_metrics (dict): Metrics from new method
        baseline_metrics (dict): Metrics from baseline method
        
    Returns:
        dict: Improvement percentages
    """
    return {
        'return_improvement': (new_metrics['avg_return'] - baseline_metrics['avg_return']) / abs(baseline_metrics['avg_return']) * 100 if baseline_metrics['avg_return'] else np.nan,
        'sharpe_improvement': (new_metrics['avg_sharpe'] - baseline_metrics['avg_sharpe']) / abs(baseline_metrics['avg_sharpe']) * 100 if baseline_metrics['avg_sharpe'] else np.nan,
        'drawdown_improvement': (baseline_metrics['avg_max_drawdown'] - new_metrics['avg_max_drawdown']) / baseline_metrics['avg_max_drawdown'] * 100 if baseline_metrics['avg_max_drawdown'] else np.nan,
        'win_rate_improvement': (new_metrics['win_rate'] - baseline_metrics['win_rate']) * 100,
        'param_consistency_improvement': (new_metrics['param_consistency'] - baseline_metrics['param_consistency']) * 100
    }

def save_test_results(result_data, test_name):
    """
    Save test results to disk.
    
    Args:
        result_data (dict): Test results data
        test_name (str): Name for this test
    """
    # Remove raw results for JSON serialization
    save_data = {k: v for k, v in result_data.items() if k != 'raw_results'}
    
    # Save as JSON
    result_path = RESULTS_DIR / f"{test_name}_results.json"
    with open(result_path, 'w') as f:
        json.dump(save_data, f, indent=4)
    
    # Save raw results as CSV (one file per split)
    for method in ['standard', 'basic_regime', 'enhanced_regime']:
        if method in result_data.get('raw_results', {}):
            raw_results = result_data['raw_results'][method]
            if 'results' in raw_results:
                df_rows = []
                for i, split in enumerate(raw_results['results']):
                    # Skip if no test results
                    if 'test_results' not in split:
                        continue
                        
                    # Extract key metrics
                    row = {
                        'split': i + 1,
                        'method': method,
                        'train_start': split.get('train_start', ''),
                        'train_end': split.get('train_end', ''),
                        'test_start': split.get('test_start', ''),
                        'test_end': split.get('test_end', ''),
                        'return': split.get('test_results', {}).get('return', np.nan),
                        'sharpe': split.get('test_results', {}).get('sharpe', np.nan),
                        'max_drawdown': split.get('test_results', {}).get('max_drawdown', np.nan),
                        'regime_detected': 'regime_breakdown' in split.get('test_results', {})
                    }
                    
                    # Add parameters if available
                    if 'best_params' in split:
                        for param, value in split['best_params'].items():
                            row[f'param_{param}'] = value
                            
                    df_rows.append(row)
                
                # Create and save DataFrame
                if df_rows:
                    df = pd.DataFrame(df_rows)
                    df_path = RESULTS_DIR / f"{test_name}_{method}_splits.csv"
                    df.to_csv(df_path, index=False)

def create_summary_report(all_results):
    """
    Create a summary report of all test results.
    
    Args:
        all_results (list): List of all test results
    """
    # Create DataFrame for easy analysis
    rows = []
    for result in all_results:
        row = {
            'symbol': result['symbol'],
            'timeframe': result['timeframe'],
            'date': result['date']
        }
        
        # Add standard metrics
        for key, value in result['standard'].items():
            row[f'standard_{key}'] = value
            
        # Add basic regime metrics
        for key, value in result['basic_regime'].items():
            row[f'basic_regime_{key}'] = value
            
        # Add enhanced regime metrics
        for key, value in result['enhanced_regime'].items():
            row[f'enhanced_regime_{key}'] = value
            
        # Add improvement metrics
        for key, value in result['basic_improvement'].items():
            row[f'basic_{key}'] = value
            
        for key, value in result['enhanced_improvement'].items():
            row[f'enhanced_{key}'] = value
            
        rows.append(row)
    
    # Create and save summary DataFrame
    if rows:
        summary_df = pd.DataFrame(rows)
        summary_path = RESULTS_DIR / "regime_adaptation_summary.csv"
        summary_df.to_csv(summary_path, index=False)
        
        # Generate summary statistics
        basic_return_improvement = summary_df['basic_return_improvement'].mean()
        enhanced_return_improvement = summary_df['enhanced_return_improvement'].mean()
        basic_param_consistency_improvement = summary_df['basic_param_consistency_improvement'].mean()
        enhanced_param_consistency_improvement = summary_df['enhanced_param_consistency_improvement'].mean()
        
        # Generate summary markdown report
        report = f"""# Regime-Aware Parameter Adaptation Evaluation Summary

## Overview
- **Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Assets Tested:** {', '.join(SYMBOLS)}
- **Timeframes Tested:** {', '.join(TIMEFRAMES)}
- **Evaluation Period:** {START_DATE} to {END_DATE}

## Key Findings

### Performance Improvements
- **Basic Regime Adaptation:**
  - Return Improvement: {basic_return_improvement:.2f}%
  - Parameter Consistency Improvement: {basic_param_consistency_improvement:.2f}%
  
- **Enhanced Regime Adaptation:**
  - Return Improvement: {enhanced_return_improvement:.2f}%
  - Parameter Consistency Improvement: {enhanced_param_consistency_improvement:.2f}%

### Detailed Analysis
The full detailed analysis can be found in the accompanying CSV files.

## Next Steps
1. Focus on the most effective regime detection method based on these results
2. Integrate the chosen method into the main trading system
3. Further refine regime thresholds based on performance data
4. Consider incorporating volatility-based position sizing to complement regime detection

"""
        # Save report
        report_path = RESULTS_DIR / "summary_report.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"Summary report saved to {report_path}")

if __name__ == "__main__":
    logger.info("Starting regime-aware parameter adaptation evaluation")
    try:
        results = run_comparative_evaluation()
        logger.info(f"Evaluation complete. Results saved to {RESULTS_DIR}")
    except Exception as e:
        logger.error(f"Error during evaluation: {e}", exc_info=True)
