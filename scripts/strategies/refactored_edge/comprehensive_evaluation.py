#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive Performance Evaluation Framework

This module provides advanced performance evaluation tools for comparing different
strategy configurations, with a focus on regime-aware vs. standard approaches.
It generates detailed statistical validation, visualizations, and performance reports.

Author: Max Kimball
Date: 2025-04-30
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Any, Optional, Union, Callable
from datetime import datetime, timedelta
from pathlib import Path
import logging
import json
from scipy import stats
import argparse

# Setup path to ensure imports work correctly
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Local imports
from scripts.strategies.refactored_edge.wfo import run_wfo
from scripts.strategies.refactored_edge.config import EdgeConfig, OPTIMIZATION_PARAMETER_GRID, get_param_combinations
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.regime import MarketRegimeType
from scripts.strategies.refactored_edge.wfo_utils import (
    SYMBOL, TIMEFRAME, START_DATE, END_DATE, INIT_CAPITAL, N_JOBS,
    ensure_output_dir, get_adaptive_window_size
)
from scripts.strategies.refactored_edge.utils import validate_dataframe, with_error_handling
from scripts.strategies.refactored_edge.run_wfo_real_data import run_real_data_wfo, visualize_wfo_results

# Constants
OUTPUT_DIR = 'data/results/comprehensive_evaluation'
REPORT_FILENAME = 'comprehensive_evaluation_report.html'
RESULTS_CSV_FILENAME = 'comparative_results.csv'
PARAMETER_STABILITY_FILENAME = 'parameter_stability.csv'
STATISTICAL_VALIDATION_FILENAME = 'statistical_validation.csv'

# Configuration variants
CONFIG_VARIANTS = {
    'standard': {
        'name': 'Standard (No Regime Adaptation)',
        'use_regime_adaptation': False,
        'signal_strictness': SignalStrictness.BALANCED,
        'color': 'blue'
    },
    'regime_aware': {
        'name': 'Regime-Aware Adaptation',
        'use_regime_adaptation': True,
        'signal_strictness': SignalStrictness.BALANCED,
        'color': 'green'
    },
    'enhanced': {
        'name': 'Enhanced (Regime + Relaxed Signals)',
        'use_regime_adaptation': True,
        'signal_strictness': SignalStrictness.RELAXED,
        'color': 'orange'
    }
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(ensure_output_dir(OUTPUT_DIR), 'comprehensive_evaluation.log'))
    ]
)
logger = logging.getLogger("comprehensive_evaluation")

# Basic utility function
def ensure_directories():
    """Ensure all required directories exist."""
    directories = [
        OUTPUT_DIR,
        os.path.join(OUTPUT_DIR, 'visualizations'),
        os.path.join(OUTPUT_DIR, 'data'),
        os.path.join(OUTPUT_DIR, 'reports')
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")
    return True

# Configuration Functions
def create_enhanced_parameter_grid() -> Dict[str, List[Any]]:
    """
    Create an enhanced parameter grid with expanded options for comprehensive testing.
    
    This expands on the default grid in config.py to test a wider range of parameter values,
    particularly for RSI thresholds, trend parameters, and regime adaptation settings.
    
    Returns:
        Dict[str, List[Any]]: Enhanced parameter grid for optimization
    """
    # Start with the default grid
    enhanced_grid = OPTIMIZATION_PARAMETER_GRID.copy()
    
    # Expand RSI threshold options
    enhanced_grid['rsi_entry_threshold'] = [25, 30, 35, 40, 45]  # More entry options
    enhanced_grid['rsi_exit_threshold'] = [55, 60, 65, 70, 75]   # More exit options
    
    # Expand trend parameters
    enhanced_grid['trend_ma_window'] = [20, 50, 100, 200]        # Test more MA periods
    enhanced_grid['trend_threshold_pct'] = [0.005, 0.01, 0.015, 0.02, 0.025] # More thresholds
    
    # Expand regime detection parameters
    enhanced_grid['adx_threshold'] = [20, 25, 30]                # Test different ADX thresholds
    enhanced_grid['volatility_threshold'] = [0.005, 0.01, 0.015] # Test different volatility thresholds
    
    # Add more signal strictness options
    enhanced_grid['signal_strictness'] = [
        SignalStrictness.BALANCED,
        SignalStrictness.RELAXED,
        SignalStrictness.ULTRA_RELAXED
    ]
    
    logger.info(f"Created enhanced parameter grid with {len(enhanced_grid)} parameters")
    return enhanced_grid

def create_strategy_configuration(
    config_variant: str,
    grid_size: str = 'medium'
) -> Dict[str, Any]:
    """
    Create a complete configuration for a strategy variant.
    
    Args:
        config_variant: Which configuration variant to use ('standard', 'regime_aware', or 'enhanced')
        grid_size: Parameter grid size ('small', 'medium', 'large')
        
    Returns:
        Dict[str, Any]: Complete strategy configuration
    """
    # Get base configuration from CONFIG_VARIANTS
    if config_variant not in CONFIG_VARIANTS:
        raise ValueError(f"Unknown configuration variant: {config_variant}")
    
    base_config = CONFIG_VARIANTS[config_variant].copy()
    
    # Add parameter grid based on grid size
    if grid_size == 'large':
        base_config['parameter_grid'] = create_enhanced_parameter_grid()
    else:
        # Use default grid from config.py
        base_config['parameter_grid'] = OPTIMIZATION_PARAMETER_GRID.copy()
        
    # Add additional configuration options
    base_config['grid_size'] = grid_size
    
    # For enhanced mode, also modify some default parameters
    if config_variant == 'enhanced':
        # Get edge config defaults and update them
        edge_config = EdgeConfig().model_dump()
        edge_config.update({
            'use_regime_adaptation': True,
            'use_dynamic_sizing': True,
            'signal_strictness': SignalStrictness.RELAXED,
            'zone_influence': 0.7,  # Higher zone influence for more signals
            'min_hold_period': 1,    # Shorter hold period for more flexibility
        })
        base_config['edge_config'] = edge_config
    
    logger.info(f"Created {config_variant} configuration with {grid_size} grid")
    return base_config

def configure_wfo_parameters(
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
    n_splits: int = 4,
    train_ratio: float = 0.7,
    initial_capital: float = 10000.0
) -> Dict[str, Any]:
    """
    Configure common WFO parameters for all strategy configurations.
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Time granularity (e.g., '1h')
        start_date: Start date for analysis
        end_date: End date for analysis
        n_splits: Number of WFO splits
        train_ratio: Ratio of training data to total window size
        initial_capital: Initial capital for backtesting
        
    Returns:
        Dict[str, Any]: Common WFO parameters
    """
    # Calculate adaptive window sizes based on timeframe and data range
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    total_days = (end_dt - start_dt).days
    
    # Get appropriate window sizes
    # Get appropriate window sizes as tuple (train_points, test_points, step_points)
    train_points, test_points, step_points = get_adaptive_window_size(
        timeframe=timeframe,
        available_days=total_days
    )
    
    wfo_config = {
        'symbol': symbol,
        'timeframe': timeframe,
        'start_date': start_date,
        'end_date': end_date,
        'n_splits': n_splits,
        'train_ratio': train_ratio,
        'initial_capital': initial_capital,
        'n_jobs': N_JOBS,
        'train_points': train_points,
        'test_points': test_points,
        'step_points': step_points
    }
    
    logger.info(f"Configured WFO parameters: {n_splits} splits, {train_ratio:.1f} train ratio")
    logger.info(f"Window sizes: train={train_points}, test={test_points}, step={step_points}")
    
    return wfo_config

# Run Comparison Functions
def save_results_to_csv(
    results_dict: Dict[str, List[Dict[str, Any]]],
    output_dir: str,
    filename: str = RESULTS_CSV_FILENAME
) -> str:
    """
    Save comparative WFO results to a CSV file.
    
    Args:
        results_dict: Dictionary mapping configuration variants to results lists
        output_dir: Directory to save the results
        filename: Name of the CSV file
        
    Returns:
        str: Path to the saved CSV file
    """
    # Prepare data for CSV
    all_results = []
    
    for variant, results in results_dict.items():
        for result in results:
            # Add variant info to each result row
            result_copy = result.copy()
            result_copy['variant'] = variant
            result_copy['variant_name'] = CONFIG_VARIANTS[variant]['name']
            all_results.append(result_copy)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)
    logger.info(f"Saved comparative results to {output_path}")
    
    return output_path

@with_error_handling()
def run_single_wfo_configuration(
    config_variant: str,
    wfo_config: Dict[str, Any],
    grid_size: str = 'medium'
) -> Tuple[List[Dict[str, Any]], Dict[int, Dict[str, Any]], List[Any]]:
    """
    Run a single WFO configuration and return the results.
    
    Args:
        config_variant: Which configuration variant to use
        wfo_config: WFO parameters from configure_wfo_parameters
        grid_size: Parameter grid size
        
    Returns:
        Tuple containing:
        - List of results dictionaries
        - Dictionary of best parameters by split
        - List of test portfolios
    """
    # Create strategy configuration
    strategy_config = create_strategy_configuration(config_variant, grid_size)
    
    # Extract WFO parameters
    wfo_params = wfo_config.copy()
    
    # Add strategy-specific parameters
    wfo_params['use_regime_filter'] = strategy_config['use_regime_adaptation']  # Map to correct parameter name
    wfo_params['signal_strictness'] = strategy_config['signal_strictness']
    
    # Convert train_points/test_points to custom_train_points/custom_test_points
    if 'train_points' in wfo_params:
        wfo_params['custom_train_points'] = wfo_params.pop('train_points')
    if 'test_points' in wfo_params:
        wfo_params['custom_test_points'] = wfo_params.pop('test_points')
    # Remove step_points as it's not used by run_real_data_wfo
    if 'step_points' in wfo_params:
        wfo_params.pop('step_points')
    
    # For enhanced mode, use specific edge config if available
    if 'edge_config' in strategy_config:
        config_obj = EdgeConfig(**strategy_config['edge_config'])
        wfo_params['config'] = config_obj
    
    logger.info(f"Running {config_variant} configuration with {grid_size} grid")
    
    # Run WFO with these parameters
    try:
        results, portfolios, best_params = run_real_data_wfo(**wfo_params)
        
        # Add information about which configuration was used
        for result in results:
            result['config_variant'] = config_variant
            result['grid_size'] = grid_size
        
        return results, best_params, portfolios
    except Exception as e:
        logger.error(f"Error running {config_variant} configuration: {str(e)}")
        logger.exception("Detailed error information:")
        # Return empty results
        return [], {}, []

def run_comparative_wfo(
    symbol: str = SYMBOL,
    timeframe: str = TIMEFRAME,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    n_splits: int = 4,
    train_ratio: float = 0.7,
    initial_capital: float = INIT_CAPITAL,
    output_dir: Optional[str] = None,
    grid_size: str = 'medium',
    run_variants: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Run comprehensive WFO evaluation with multiple configurations for comparison.
    
    This function runs the WFO process with different parameter configurations:
    1. Standard: No regime adaptation
    2. Regime-Aware: Adaptation based on detected market regime
    3. Enhanced: Regime-aware with expanded parameter grid
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Time granularity (e.g., '1h')
        start_date: Start date for analysis (YYYY-MM-DD)
        end_date: End date for analysis (YYYY-MM-DD)
        n_splits: Number of WFO splits
        train_ratio: Ratio of training data to total window size
        initial_capital: Initial capital for backtesting
        output_dir: Directory to save results (created if doesn't exist)
        grid_size: Parameter grid size ('small', 'medium', 'large')
        run_variants: List of variants to run (default: all in CONFIG_VARIANTS)
        
    Returns:
        Dict with results from all configurations
    """
    # Ensure output directory exists
    if output_dir is None:
        output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure common WFO parameters
    wfo_config = configure_wfo_parameters(
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        n_splits=n_splits,
        train_ratio=train_ratio,
        initial_capital=initial_capital
    )
    
    # Determine which variants to run
    if run_variants is None:
        run_variants = list(CONFIG_VARIANTS.keys())
    
    # Initialize results dictionary
    all_results = {}
    all_portfolios = {}
    all_best_params = {}
    
    # Run each configuration variant
    for variant in run_variants:
        logger.info(f"\n{'='*50}\nRunning {variant} configuration\n{'='*50}")
        
        results, best_params, portfolios = run_single_wfo_configuration(
            config_variant=variant,
            wfo_config=wfo_config,
            grid_size=grid_size
        )
        
        # Store the results
        all_results[variant] = results
        all_portfolios[variant] = portfolios
        all_best_params[variant] = best_params
        
        # Save interim results after each variant
        save_results_to_csv(
            {variant: results},
            os.path.join(output_dir, 'data'),
            f"{variant}_results.csv"
        )
    
    # Save combined results
    comparative_results_path = save_results_to_csv(
        all_results,
        os.path.join(output_dir, 'data')
    )
    
    # Save parameter data if available
    has_param_data = any(bool(params) for params in all_best_params.values())
    if has_param_data:
        # Serialize parameter data (this is complex nested data, so just save as JSON)
        param_data_path = os.path.join(output_dir, 'data', 'best_parameters.json')
        with open(param_data_path, 'w') as f:
            # Convert to a serializable format
            serializable_params = {}
            for variant, params in all_best_params.items():
                serializable_params[variant] = {}
                for split, split_params in params.items():
                    if hasattr(split_params, 'items'):
                        # It's a dict-like object
                        serializable_params[variant][str(split)] = {
                            k: str(v) for k, v in split_params.items()
                            if not k.startswith('_')
                        }
                    else:
                        # It's some other object
                        serializable_params[variant][str(split)] = str(split_params)
            
            json.dump(serializable_params, f, indent=2)
        logger.info(f"Saved best parameters to {param_data_path}")
    
    # Return all results data for further processing
    return {
        'results': all_results,
        'portfolios': all_portfolios,
        'best_params': all_best_params,
        'results_path': comparative_results_path
    }

# Statistical Analysis Functions
def analyze_parameter_stability(
    best_params_by_split: Dict[int, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Analyze parameter stability across WFO splits.
    
    Args:
        best_params_by_split: Dictionary mapping split numbers to best parameters
        
    Returns:
        Dictionary with stability metrics for each parameter
    """
    # If no parameters provided, return empty analysis
    if not best_params_by_split:
        return {'stability_score': 0, 'parameters': {}}
    
    # Extract parameter names from the first split (assuming all splits have same parameters)
    first_split = next(iter(best_params_by_split.values()))
    if not hasattr(first_split, 'items'):
        return {'stability_score': 0, 'parameters': {}}
    
    param_names = [k for k in first_split.keys() if not k.startswith('_')]
    
    # Collect values for each parameter across splits
    param_values = {param: [] for param in param_names}
    for split, params in best_params_by_split.items():
        if not hasattr(params, 'items'):
            continue
        for param in param_names:
            if param in params:
                # Try to convert to appropriate type for analysis
                try:
                    if isinstance(params[param], bool):
                        param_values[param].append(int(params[param]))
                    elif isinstance(params[param], (int, float)):
                        param_values[param].append(params[param])
                    else:
                        # For string/enum parameters, just track occurrences
                        param_values[param].append(str(params[param]))
                except (ValueError, TypeError):
                    param_values[param].append(str(params[param]))
    
    # Calculate stability metrics for each parameter
    stability_metrics = {}
    for param, values in param_values.items():
        if not values:
            continue
            
        # For numerical parameters
        if all(isinstance(v, (int, float)) for v in values):
            # Convert to numpy array for analysis
            values_array = np.array(values)
            metrics = {
                'mean': float(np.mean(values_array)),
                'std': float(np.std(values_array)),
                'min': float(np.min(values_array)),
                'max': float(np.max(values_array)),
                'coefficient_of_variation': float(np.std(values_array) / np.mean(values_array)) if np.mean(values_array) != 0 else float('inf'),
                'values': values
            }
        # For categorical parameters
        else:
            # Count frequencies
            value_counts = {}
            for v in values:
                value_counts[str(v)] = value_counts.get(str(v), 0) + 1
                
            # Calculate entropy as a measure of stability (lower is more stable)
            total = len(values)
            entropy = 0
            for count in value_counts.values():
                p = count / total
                entropy -= p * np.log2(p)
                
            metrics = {
                'most_common': max(value_counts.items(), key=lambda x: x[1])[0],
                'entropy': float(entropy),  # Lower entropy means more stability
                'unique_values': len(value_counts),
                'value_counts': value_counts
            }
            
        stability_metrics[param] = metrics
    
    # Calculate an overall stability score (0-1, where 1 is perfectly stable)
    if stability_metrics:
        # For numeric params: use average coefficient of variation (inverted)
        cv_scores = [1 / (1 + metrics['coefficient_of_variation']) 
                    for param, metrics in stability_metrics.items() 
                    if 'coefficient_of_variation' in metrics]
        
        # For categorical params: use normalized entropy scores (1 - normalized entropy)
        entropy_scores = [1 - (metrics['entropy'] / np.log2(metrics['unique_values'])) 
                         for param, metrics in stability_metrics.items() 
                         if 'entropy' in metrics and metrics['unique_values'] > 1]
        
        # If either list is empty, use only the available one
        if cv_scores and entropy_scores:
            overall_score = (np.mean(cv_scores) + np.mean(entropy_scores)) / 2
        elif cv_scores:
            overall_score = np.mean(cv_scores)
        elif entropy_scores:
            overall_score = np.mean(entropy_scores)
        else:
            overall_score = 0
    else:
        overall_score = 0
    
    return {
        'stability_score': float(overall_score),
        'parameters': stability_metrics
    }

def calculate_statistical_significance(
    standard_results: List[Dict[str, Any]],
    regime_aware_results: List[Dict[str, Any]],
    metric: str = 'test_sharpe'
) -> Dict[str, Any]:
    """
    Calculate statistical significance of performance differences.
    
    Args:
        standard_results: Results from standard WFO run
        regime_aware_results: Results from regime-aware WFO run
        metric: Performance metric to compare (e.g., 'test_sharpe', 'test_return')
        
    Returns:
        Dictionary with statistical test results
    """
    # Extract metric values
    standard_values = [r.get(metric, np.nan) for r in standard_results]
    regime_values = [r.get(metric, np.nan) for r in regime_aware_results]
    
    # Filter out NaN values
    standard_values = [v for v in standard_values if not np.isnan(v)]
    regime_values = [v for v in regime_values if not np.isnan(v)]
    
    # If not enough data for statistical tests, return simple comparison
    if len(standard_values) < 2 or len(regime_values) < 2:
        return {
            'standard_mean': np.mean(standard_values) if standard_values else np.nan,
            'regime_mean': np.mean(regime_values) if regime_values else np.nan,
            'improvement': np.mean(regime_values) - np.mean(standard_values) if (standard_values and regime_values) else np.nan,
            'percent_improvement': (np.mean(regime_values) - np.mean(standard_values)) / abs(np.mean(standard_values)) * 100 
                                   if (standard_values and regime_values and np.mean(standard_values) != 0) else np.nan,
            'sample_size_too_small': True
        }
    
    # Calculate basic statistics
    standard_mean = np.mean(standard_values)
    regime_mean = np.mean(regime_values)
    standard_std = np.std(standard_values)
    regime_std = np.std(regime_values)
    
    # Perform t-test to determine if the difference is statistically significant
    t_stat, p_value = stats.ttest_ind(regime_values, standard_values, equal_var=False)
    
    # Calculate effect size (Cohen's d)
    pooled_std = np.sqrt((standard_std**2 + regime_std**2) / 2)
    cohens_d = (regime_mean - standard_mean) / pooled_std if pooled_std != 0 else np.nan
    
    # Interpret the effect size
    if np.isnan(cohens_d):
        effect_interpretation = "Cannot calculate"
    elif abs(cohens_d) < 0.2:
        effect_interpretation = "Negligible"
    elif abs(cohens_d) < 0.5:
        effect_interpretation = "Small"
    elif abs(cohens_d) < 0.8:
        effect_interpretation = "Medium"
    else:
        effect_interpretation = "Large"
    
    # Calculate improvement
    improvement = regime_mean - standard_mean
    percent_improvement = (improvement / abs(standard_mean)) * 100 if standard_mean != 0 else np.nan
    
    return {
        'standard_mean': float(standard_mean),
        'regime_mean': float(regime_mean),
        'standard_std': float(standard_std),
        'regime_std': float(regime_std),
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'significant_at_0.05': p_value < 0.05,
        'significant_at_0.01': p_value < 0.01,
        'cohens_d': float(cohens_d) if not np.isnan(cohens_d) else None,
        'effect_size': effect_interpretation,
        'improvement': float(improvement),
        'percent_improvement': float(percent_improvement) if not np.isnan(percent_improvement) else None,
        'sample_size': {"standard": len(standard_values), "regime": len(regime_values)}
    }

def calculate_performance_consistency(
    results: List[Dict[str, Any]],
    metric: str = 'test_sharpe'
) -> Dict[str, Any]:
    """
    Calculate performance consistency metrics across WFO splits.
    
    Args:
        results: List of result dictionaries from WFO
        metric: Performance metric to analyze
        
    Returns:
        Dictionary with consistency metrics
    """
    # Extract metric values
    values = [r.get(metric, np.nan) for r in results]
    
    # Filter out NaN values
    values = [v for v in values if not np.isnan(v)]
    
    # If not enough data, return simple statistics
    if len(values) < 2:
        return {
            'mean': np.mean(values) if values else np.nan,
            'sample_size_too_small': True
        }
    
    # Calculate basic statistics
    mean_value = np.mean(values)
    median_value = np.median(values)
    std_value = np.std(values)
    min_value = np.min(values)
    max_value = np.max(values)
    range_value = max_value - min_value
    
    # Calculate consistency metrics
    positive_count = sum(1 for v in values if v > 0)
    positive_percent = (positive_count / len(values)) * 100
    
    # Calculate interquartile range
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    
    # Calculate coefficient of variation (lower is more consistent)
    cv = (std_value / abs(mean_value)) * 100 if mean_value != 0 else np.nan
    
    # Calculate robustness ratio (measure of consistency across different conditions)
    robustness_ratio = median_value / range_value if range_value != 0 else np.nan
    
    return {
        'mean': float(mean_value),
        'median': float(median_value),
        'std': float(std_value),
        'min': float(min_value),
        'max': float(max_value),
        'range': float(range_value),
        'interquartile_range': float(iqr),
        'positive_percent': float(positive_percent),
        'coefficient_of_variation': float(cv) if not np.isnan(cv) else None,
        'robustness_ratio': float(robustness_ratio) if not np.isnan(robustness_ratio) else None,
        'sample_size': len(values)
    }

def calculate_comprehensive_statistics(
    results_dict: Dict[str, List[Dict[str, Any]]],
    best_params_dict: Dict[str, Dict[int, Dict[str, Any]]],
    metrics: List[str] = ['test_return', 'test_sharpe', 'robustness_ratio']
) -> Dict[str, Any]:
    """
    Calculate comprehensive statistical analysis for all configuration variants.
    
    Args:
        results_dict: Dictionary mapping configuration variants to results lists
        best_params_dict: Dictionary mapping configuration variants to best parameters
        metrics: List of metrics to analyze
        
    Returns:
        Dictionary with comprehensive statistical analysis
    """
    # Initialize results
    stats_results = {
        'parameter_stability': {},
        'performance_consistency': {},
        'statistical_significance': {}
    }
    
    # Calculate parameter stability for each variant
    for variant, params in best_params_dict.items():
        stats_results['parameter_stability'][variant] = analyze_parameter_stability(params)
    
    # Calculate performance consistency for each variant and metric
    for variant, results in results_dict.items():
        stats_results['performance_consistency'][variant] = {}
        for metric in metrics:
            stats_results['performance_consistency'][variant][metric] = \
                calculate_performance_consistency(results, metric)
    
    # Calculate statistical significance between variants
    if 'standard' in results_dict and len(results_dict) > 1:
        standard_results = results_dict['standard']
        for variant, results in results_dict.items():
            if variant != 'standard':
                stats_results['statistical_significance'][f'standard_vs_{variant}'] = {}
                for metric in metrics:
                    stats_results['statistical_significance'][f'standard_vs_{variant}'][metric] = \
                        calculate_statistical_significance(standard_results, results, metric)
    
    # Calculate overall scores
    variant_scores = {}
    for variant in results_dict.keys():
        # Combine stability and consistency scores
        stability_score = stats_results['parameter_stability'].get(variant, {}).get('stability_score', 0)
        
        # Average consistency scores across metrics
        consistency_scores = []
        for metric in metrics:
            metric_stats = stats_results['performance_consistency'].get(variant, {}).get(metric, {})
            if 'robustness_ratio' in metric_stats and metric_stats['robustness_ratio'] is not None:
                # Scale robustness ratio to 0-1 range (higher is better)
                robustness_score = min(metric_stats['robustness_ratio'], 1) if metric_stats['robustness_ratio'] > 0 else 0
                consistency_scores.append(robustness_score)
                
            if 'positive_percent' in metric_stats:
                # Scale positive percent to 0-1 range
                positive_score = metric_stats['positive_percent'] / 100
                consistency_scores.append(positive_score)
        
        consistency_score = np.mean(consistency_scores) if consistency_scores else 0
        
        # Calculate performance score (based on Sharpe ratio)
        sharpe_stats = stats_results['performance_consistency'].get(variant, {}).get('test_sharpe', {})
        mean_sharpe = sharpe_stats.get('mean', 0)
        performance_score = max(0, min(mean_sharpe / 2, 1))  # Scale Sharpe 0-2 to 0-1 range
        
        # Calculate overall score (weighted average)
        overall_score = (0.3 * stability_score) + (0.3 * consistency_score) + (0.4 * performance_score)
        
        variant_scores[variant] = {
            'stability_score': float(stability_score),
            'consistency_score': float(consistency_score),
            'performance_score': float(performance_score),
            'overall_score': float(overall_score)
        }
    
    stats_results['variant_scores'] = variant_scores
    
    return stats_results

# Visualization Functions
def create_performance_comparison_chart(
    results_dict: Dict[str, List[Dict[str, Any]]],
    metric: str,
    output_dir: str,
    title: Optional[str] = None,
    y_axis_label: Optional[str] = None
) -> str:
    """
    Create an interactive chart comparing a specific performance metric between different approaches.
    
    Args:
        results_dict: Dictionary mapping configuration variants to results lists
        metric: Metric to compare (e.g., 'test_return', 'test_sharpe')
        output_dir: Directory to save the chart
        title: Custom title for the chart
        y_axis_label: Label for the y-axis
        
    Returns:
        Path to the saved chart file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data for plotting
    chart_data = []
    for variant, results in results_dict.items():
        for result in results:
            if metric in result:
                # Add result with variant information
                chart_entry = {
                    'split': result.get('split', 0),
                    'variant': variant,
                    'variant_name': CONFIG_VARIANTS[variant]['name'],
                    'value': result.get(metric, np.nan),
                    'color': CONFIG_VARIANTS[variant]['color']
                }
                chart_data.append(chart_entry)
    
    # Convert to DataFrame for easier plotting
    df = pd.DataFrame(chart_data)
    
    if df.empty:
        logger.warning(f"No data available for metric '{metric}'")
        return ""
    
    # Set title and labels
    if title is None:
        title = f"Comparison of {metric} across Different Configurations"
    
    if y_axis_label is None:
        y_axis_label = metric.replace('_', ' ').title()
    
    # Create the plot
    fig = px.line(df, x='split', y='value', color='variant_name', title=title,
                 labels={'split': 'Split Number', 'value': y_axis_label, 'variant_name': 'Configuration'},
                 markers=True)
    
    # Add further customization
    fig.update_layout(
        width=1000,
        height=600,
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified'
    )
    
    # Save the figure
    output_path = os.path.join(output_dir, f"{metric}_comparison.html")
    fig.write_html(output_path)
    
    logger.info(f"Created performance comparison chart for {metric} at {output_path}")
    return output_path

def create_split_performance_heatmap(
    results_dict: Dict[str, List[Dict[str, Any]]],
    metric: str,
    output_dir: str
) -> str:
    """
    Create a heatmap showing performance across splits for each configuration variant.
    
    Args:
        results_dict: Dictionary mapping configuration variants to results lists
        metric: Metric to compare (e.g., 'test_return', 'test_sharpe')
        output_dir: Directory to save the heatmap
        
    Returns:
        Path to the saved heatmap file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data for heatmap
    variants = list(results_dict.keys())
    
    # Find all split numbers
    all_splits = set()
    for results in results_dict.values():
        for result in results:
            if 'split' in result:
                all_splits.add(result['split'])
    
    splits = sorted(all_splits)
    
    if not splits:
        logger.warning("No split information available for heatmap")
        return ""
    
    # Create matrix for heatmap
    heatmap_data = np.full((len(variants), len(splits)), np.nan)
    
    for i, variant in enumerate(variants):
        results = results_dict[variant]
        for result in results:
            if 'split' in result and metric in result:
                split_idx = splits.index(result['split'])
                heatmap_data[i, split_idx] = result[metric]
    
    # Create the heatmap using plotly
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=[f"Split {s}" for s in splits],
        y=[CONFIG_VARIANTS[v]['name'] for v in variants],
        colorscale='RdBu',
        zmid=0,  # Center at 0 for metrics like return/sharpe where negative is bad
        text=[[f"{val:.4f}" if not np.isnan(val) else "N/A" for val in row] for row in heatmap_data],
        hoverinfo='text+x+y',
        colorbar=dict(title=metric.replace('_', ' ').title())
    ))
    
    # Update layout
    fig.update_layout(
        title=f"{metric.replace('_', ' ').title()} by Split and Configuration",
        width=1000,
        height=500,
        template='plotly_white',
        xaxis=dict(title='Split Number'),
        yaxis=dict(title='Configuration')
    )
    
    # Save the figure
    output_path = os.path.join(output_dir, f"{metric}_heatmap.html")
    fig.write_html(output_path)
    
    logger.info(f"Created split performance heatmap for {metric} at {output_path}")
    return output_path

def create_regime_comparison_chart(
    results_dict: Dict[str, List[Dict[str, Any]]],
    output_dir: str
) -> str:
    """
    Create a chart showing performance differences between configurations in different regimes.
    
    Args:
        results_dict: Dictionary mapping configuration variants to results lists
        output_dir: Directory to save the chart
        
    Returns:
        Path to the saved chart file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract regime breakdown information if available
    chart_data = []
    
    for variant, results in results_dict.items():
        for result in results:
            # Try to extract regime breakdown information
            if 'regime_breakdown' in result and isinstance(result['regime_breakdown'], dict):
                regime_data = result['regime_breakdown']
                
                # Add entries for each regime
                for regime, metrics in regime_data.items():
                    if isinstance(metrics, dict):
                        for metric_name, value in metrics.items():
                            if isinstance(value, (int, float)) and not np.isnan(value):
                                chart_entry = {
                                    'split': result.get('split', 0),
                                    'variant': variant,
                                    'variant_name': CONFIG_VARIANTS[variant]['name'],
                                    'regime': regime,
                                    'metric': metric_name,
                                    'value': value
                                }
                                chart_data.append(chart_entry)
    
    # If no regime data is available, return early
    if not chart_data:
        logger.warning("No regime breakdown data available for visualization")
        return ""
    
    # Convert to DataFrame
    df = pd.DataFrame(chart_data)
    
    # Create separate charts for different metrics
    unique_metrics = df['metric'].unique()
    output_paths = []
    
    for metric in unique_metrics:
        # Filter for this metric
        metric_df = df[df['metric'] == metric]
        
        # Create the plot
        fig = px.bar(metric_df, x='regime', y='value', color='variant_name', barmode='group',
                   facet_col='split', facet_col_wrap=3,
                   title=f"{metric.replace('_', ' ').title()} by Regime and Configuration",
                   labels={'regime': 'Market Regime', 'value': metric.replace('_', ' ').title(), 
                          'variant_name': 'Configuration'})
        
        # Update layout
        fig.update_layout(
            width=1200,
            height=800,
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        # Save the figure
        output_path = os.path.join(output_dir, f"regime_{metric}_comparison.html")
        fig.write_html(output_path)
        output_paths.append(output_path)
        
        logger.info(f"Created regime comparison chart for {metric} at {output_path}")
    
    return output_paths[0] if output_paths else ""

def create_parameter_stability_chart(
    stability_data: Dict[str, Dict[str, Any]],
    output_dir: str
) -> str:
    """
    Create a visualization of parameter stability across different configurations.
    
    Args:
        stability_data: Dictionary with parameter stability metrics
        output_dir: Directory to save the chart
        
    Returns:
        Path to the saved chart file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract overall stability scores
    stability_scores = []
    
    for variant, data in stability_data.items():
        if 'stability_score' in data:
            entry = {
                'variant': variant,
                'variant_name': CONFIG_VARIANTS[variant]['name'],
                'stability_score': data['stability_score']
            }
            stability_scores.append(entry)
    
    if not stability_scores:
        logger.warning("No stability score data available for visualization")
        return ""
    
    # Create DataFrame
    df = pd.DataFrame(stability_scores)
    
    # Create bar chart of stability scores
    fig = px.bar(df, x='variant_name', y='stability_score', color='variant_name',
               title='Parameter Stability Scores by Configuration',
               labels={'variant_name': 'Configuration', 'stability_score': 'Stability Score (0-1)'})
    
    # Add a horizontal line at 0.7 (good stability threshold)
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=0.7,
        x1=len(df) - 0.5,
        y1=0.7,
        line=dict(color="green", width=2, dash="dash"),
    )
    
    # Add annotation for the threshold line
    fig.add_annotation(
        x=len(df) - 0.5,
        y=0.72,
        text="Good Stability Threshold",
        showarrow=False,
        font=dict(color="green")
    )
    
    # Update layout
    fig.update_layout(
        width=800,
        height=500,
        template='plotly_white',
        yaxis=dict(range=[0, 1.05]),  # Fix y-axis range from 0 to 1
        showlegend=False
    )
    
    # Save the figure
    output_path = os.path.join(output_dir, "parameter_stability_scores.html")
    fig.write_html(output_path)
    
    logger.info(f"Created parameter stability chart at {output_path}")
    return output_path

def create_comprehensive_visualizations(
    results_dict: Dict[str, List[Dict[str, Any]]],
    stats_results: Dict[str, Any],
    output_dir: str
) -> Dict[str, str]:
    """
    Create a comprehensive set of visualizations for comparing configurations.
    
    Args:
        results_dict: Dictionary mapping configuration variants to results lists
        stats_results: Statistics results from calculate_comprehensive_statistics
        output_dir: Directory to save visualizations
        
    Returns:
        Dictionary mapping visualization types to file paths
    """
    # Ensure output directory exists
    vis_dir = os.path.join(output_dir, 'visualizations')
    os.makedirs(vis_dir, exist_ok=True)
    
    # Initialize output paths dictionary
    visualization_paths = {}
    
    # Create performance comparison charts for key metrics
    metrics_to_visualize = ['test_return', 'test_sharpe', 'robustness_ratio', 'regime_aware_improvement']
    for metric in metrics_to_visualize:
        # Check if this metric exists in the results
        exists = False
        for results in results_dict.values():
            for result in results:
                if metric in result:
                    exists = True
                    break
            if exists:
                break
                
        if exists:
            path = create_performance_comparison_chart(results_dict, metric, vis_dir)
            if path:
                visualization_paths[f"{metric}_chart"] = path
    
    # Create heatmap visualizations
    for metric in ['test_return', 'test_sharpe']:
        path = create_split_performance_heatmap(results_dict, metric, vis_dir)
        if path:
            visualization_paths[f"{metric}_heatmap"] = path
    
    # Create regime comparison chart
    path = create_regime_comparison_chart(results_dict, vis_dir)
    if path:
        visualization_paths["regime_chart"] = path
    
    # Create parameter stability chart
    if 'parameter_stability' in stats_results:
        path = create_parameter_stability_chart(stats_results['parameter_stability'], vis_dir)
        if path:
            visualization_paths["stability_chart"] = path
    
    # Create index HTML file linking to all visualizations
    index_path = os.path.join(vis_dir, 'index.html')
    with open(index_path, 'w') as f:
        f.write('<html><head><title>Comprehensive Evaluation Visualizations</title></head>\n')
        f.write('<body><h1>Comprehensive Evaluation Visualizations</h1>\n')
        f.write('<ul>\n')
        for name, path in visualization_paths.items():
            rel_path = os.path.basename(path)
            f.write(f'<li><a href="{rel_path}">{name.replace("_", " ").title()}</a></li>\n')
        f.write('</ul></body></html>')
    
    visualization_paths["index"] = index_path
    logger.info(f"Created visualization index at {index_path}")
    
    return visualization_paths

def generate_comprehensive_report(
    results_dict: Dict[str, List[Dict[str, Any]]],
    stats_results: Dict[str, Any],
    visualization_paths: Dict[str, str],
    output_dir: str
) -> str:
    """
    Generate a comprehensive HTML report with results, statistics, and visualizations.
    
    Args:
        results_dict: Dictionary mapping configuration variants to results lists
        stats_results: Statistics results from calculate_comprehensive_statistics
        visualization_paths: Dictionary mapping visualization types to file paths
        output_dir: Directory to save the report
        
    Returns:
        Path to the saved report file
    """
    # Ensure output directory exists
    report_dir = os.path.join(output_dir, 'reports')
    os.makedirs(report_dir, exist_ok=True)
    
    # Create report filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"comprehensive_report_{timestamp}.html")
    
    # Generate HTML content
    with open(report_path, 'w') as f:
        # HTML header
        f.write('<!DOCTYPE html>\n<html>\n<head>\n')
        f.write('<title>Edge Multi-Factor Strategy: Comprehensive Evaluation Report</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; margin: 20px; }\n')
        f.write('h1, h2, h3 { color: #2c3e50; }\n')
        f.write('table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }\n')
        f.write('th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n')
        f.write('th { background-color: #f2f2f2; }\n')
        f.write('tr:nth-child(even) { background-color: #f9f9f9; }\n')
        f.write('.metric-good { color: green; }\n')
        f.write('.metric-bad { color: red; }\n')
        f.write('.metric-neutral { color: orange; }\n')
        f.write('.summary-box { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; background-color: #f8f9fa; }\n')
        f.write('</style>\n')
        f.write('</head>\n<body>\n')
        
        # Report header
        f.write('<h1>Edge Multi-Factor Strategy: Comprehensive Evaluation Report</h1>\n')
        f.write(f'<p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>\n')
        
        # Executive summary
        f.write('<div class="summary-box">\n')
        f.write('<h2>Executive Summary</h2>\n')
        
        # Find best configuration
        best_variant = None
        best_score = -float('inf')
        for variant, scores in stats_results.get('variant_scores', {}).items():
            if scores.get('overall_score', 0) > best_score:
                best_score = scores.get('overall_score', 0)
                best_variant = variant
        
        if best_variant:
            variant_name = CONFIG_VARIANTS[best_variant]['name']
            f.write(f'<p><strong>Best Configuration:</strong> {variant_name}</p>\n')
            
            # Get performance improvement stats
            if 'statistical_significance' in stats_results and f'standard_vs_{best_variant}' in stats_results['statistical_significance']:
                sharpe_stats = stats_results['statistical_significance'][f'standard_vs_{best_variant}'].get('test_sharpe', {})
                if 'percent_improvement' in sharpe_stats and sharpe_stats['percent_improvement'] is not None:
                    pct_improvement = sharpe_stats['percent_improvement']
                    f.write(f'<p><strong>Performance Improvement:</strong> {pct_improvement:.2f}% in Sharpe Ratio</p>\n')
                    
                    significance = sharpe_stats.get('significant_at_0.05', False)
                    if significance:
                        f.write('<p><strong>Statistical Significance:</strong> <span class="metric-good">Significant (p < 0.05)</span></p>\n')
                    else:
                        f.write('<p><strong>Statistical Significance:</strong> <span class="metric-neutral">Not Significant</span></p>\n')
        
        f.write('</div>\n')
        
        # Configuration comparison
        f.write('<h2>Configuration Comparison</h2>\n')
        
        # Performance metrics table
        f.write('<h3>Performance Metrics</h3>\n')
        f.write('<table>\n')
        f.write('<tr><th>Configuration</th><th>Avg. Test Return</th><th>Avg. Test Sharpe</th>')
        f.write('<th>Positive Split %</th><th>Consistency</th><th>Overall Score</th></tr>\n')
        
        for variant in results_dict.keys():
            variant_name = CONFIG_VARIANTS[variant]['name']
            
            # Get performance metrics
            sharpe_stats = stats_results.get('performance_consistency', {}).get(variant, {}).get('test_sharpe', {})
            return_stats = stats_results.get('performance_consistency', {}).get(variant, {}).get('test_return', {})
            
            avg_return = return_stats.get('mean', 0)
            avg_sharpe = sharpe_stats.get('mean', 0)
            positive_pct = sharpe_stats.get('positive_percent', 0)
            
            # Get overall score
            overall_score = stats_results.get('variant_scores', {}).get(variant, {}).get('overall_score', 0)
            consistency_score = stats_results.get('variant_scores', {}).get(variant, {}).get('consistency_score', 0)
            
            # Format row with conditional coloring
            return_class = 'metric-good' if avg_return > 0 else 'metric-bad'
            sharpe_class = 'metric-good' if avg_sharpe > 1 else ('metric-neutral' if avg_sharpe > 0 else 'metric-bad')
            
            f.write(f'<tr><td>{variant_name}</td>')
            f.write(f'<td class="{return_class}">{avg_return:.2%}</td>')
            f.write(f'<td class="{sharpe_class}">{avg_sharpe:.2f}</td>')
            f.write(f'<td>{positive_pct:.0f}%</td>')
            f.write(f'<td>{consistency_score:.2f}</td>')
            f.write(f'<td>{overall_score:.2f}</td></tr>\n')
            
        f.write('</table>\n')
        
        # Link to visualizations
        f.write('<h2>Interactive Visualizations</h2>\n')
        f.write('<p>Click on the links below to view interactive visualizations:</p>\n')
        f.write('<ul>\n')
        vis_relative_dir = '../visualizations/'
        for name, path in visualization_paths.items():
            if 'index' in name.lower():
                index_path = os.path.join(vis_relative_dir, os.path.basename(path))
                f.write(f'<li><a href="{index_path}">All Visualizations Index</a></li>\n')
                break
        f.write('</ul>\n')
        
        # Report footer
        f.write('<hr>\n')
        f.write('<p><em>This report was generated automatically by the Edge Multi-Factor Strategy ' +
              'Comprehensive Evaluation Framework.</em></p>\n')
        f.write('</body>\n</html>')
    
    logger.info(f"Generated comprehensive report at {report_path}")
    return report_path

def run_comprehensive_evaluation(
    symbol: str = SYMBOL,
    timeframe: str = TIMEFRAME,
    start_date: str = START_DATE, 
    end_date: str = END_DATE,
    n_splits: int = 4,
    train_ratio: float = 0.7,
    output_dir: Optional[str] = None,
    run_variants: Optional[List[str]] = None,
    grid_size: str = 'medium'
) -> Dict[str, Any]:
    """
    Run a complete comprehensive evaluation pipeline.
    
    This function orchestrates the entire evaluation process:
    1. Run comparative WFO with different configurations
    2. Calculate comprehensive statistics
    3. Create visualizations
    4. Generate final report
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Time granularity (e.g., '1h')
        start_date: Start date for analysis (YYYY-MM-DD)
        end_date: End date for analysis (YYYY-MM-DD)
        n_splits: Number of WFO splits
        train_ratio: Ratio of training data to total window size
        output_dir: Directory to save results (created if doesn't exist)
        run_variants: List of variants to run (default: all in CONFIG_VARIANTS)
        grid_size: Parameter grid size ('small', 'medium', 'large')
        
    Returns:
        Dict with paths to generated files and results
    """
    # Ensure directories exist
    if output_dir is None:
        output_dir = OUTPUT_DIR
    ensure_directories()
    
    # 1. Run comparative WFO
    logger.info("\n===== STEP 1: Running Comparative WFO =====\n")
    wfo_results = run_comparative_wfo(
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        n_splits=n_splits,
        train_ratio=train_ratio,
        output_dir=output_dir,
        run_variants=run_variants,
        grid_size=grid_size
    )
    
    results_dict = wfo_results['results']
    best_params_dict = wfo_results['best_params']
    
    # 2. Calculate comprehensive statistics
    logger.info("\n===== STEP 2: Calculating Statistics =====\n")
    stats_results = calculate_comprehensive_statistics(
        results_dict=results_dict,
        best_params_dict=best_params_dict
    )
    
    # Save statistics to JSON
    stats_path = os.path.join(output_dir, 'data', 'statistical_validation.json')
    with open(stats_path, 'w') as f:
        # Convert numpy values to Python native types for JSON serialization
        stats_json = json.dumps(stats_results, default=lambda x: float(x) if isinstance(x, np.number) else x, indent=2)
        f.write(stats_json)
    
    # 3. Create visualizations
    logger.info("\n===== STEP 3: Creating Visualizations =====\n")
    visualization_paths = create_comprehensive_visualizations(
        results_dict=results_dict,
        stats_results=stats_results,
        output_dir=output_dir
    )
    
    # 4. Generate final report
    logger.info("\n===== STEP 4: Generating Report =====\n")
    report_path = generate_comprehensive_report(
        results_dict=results_dict,
        stats_results=stats_results,
        visualization_paths=visualization_paths,
        output_dir=output_dir
    )
    
    return {
        'results': results_dict,
        'statistics': stats_results,
        'visualizations': visualization_paths,
        'report_path': report_path,
        'data_path': os.path.join(output_dir, 'data'),
        'output_dir': output_dir
    }

def parse_arguments():
    """
    Parse command line arguments for the comprehensive evaluation script.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Run comprehensive evaluation of Edge Multi-Factor Strategy")
    
    parser.add_argument('--symbol', type=str, default=SYMBOL,
                        help=f"Trading symbol (default: {SYMBOL})")
    parser.add_argument('--timeframe', type=str, default=TIMEFRAME,
                        help=f"Time granularity (default: {TIMEFRAME})")
    parser.add_argument('--start-date', type=str, default=START_DATE,
                        help=f"Start date (YYYY-MM-DD) (default: {START_DATE})")
    parser.add_argument('--end-date', type=str, default=END_DATE,
                        help=f"End date (YYYY-MM-DD) (default: {END_DATE})")
    parser.add_argument('--n-splits', type=int, default=4,
                        help="Number of WFO splits (default: 4)")
    parser.add_argument('--train-ratio', type=float, default=0.7,
                        help="Ratio of training data to total window size (default: 0.7)")
    parser.add_argument('--output-dir', type=str, default=None,
                        help=f"Directory to save results (default: {OUTPUT_DIR})")
    parser.add_argument('--variants', type=str, nargs='+', default=None, 
                        choices=list(CONFIG_VARIANTS.keys()),
                        help="List of variants to run (default: all)")
    parser.add_argument('--grid-size', type=str, default='medium',
                        choices=['small', 'medium', 'large'],
                        help="Parameter grid size (default: medium)")
    parser.add_argument('--quick-test', action='store_true',
                        help="Run a quick test with reduced parameters (for debugging)")
    
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Print banner
    print("\n" + "=" * 80)
    print("Edge Multi-Factor Strategy: Comprehensive Performance Evaluation")
    print("=" * 80 + "\n")
    
    # Run comprehensive evaluation
    if args.quick_test:
        print("QUICK TEST MODE: Using minimal parameters for faster execution\n")
        # Use only two variants and smaller grid size for quick testing
        results = run_comprehensive_evaluation(
            symbol=args.symbol,
            timeframe=args.timeframe,
            start_date=args.start_date,
            end_date=args.end_date,
            n_splits=2,  # Fewer splits for quicker execution
            train_ratio=args.train_ratio,
            output_dir=args.output_dir,
            run_variants=['standard', 'regime_aware'],  # Just two variants
            grid_size='small'  # Smallest grid
        )
    else:
        # Run full evaluation
        results = run_comprehensive_evaluation(
            symbol=args.symbol,
            timeframe=args.timeframe,
            start_date=args.start_date,
            end_date=args.end_date,
            n_splits=args.n_splits,
            train_ratio=args.train_ratio,
            output_dir=args.output_dir,
            run_variants=args.variants,
            grid_size=args.grid_size
        )
    
    # Show final report path
    print("\n" + "=" * 80)
    print(f"Comprehensive evaluation complete!")
    print(f"Report saved to: {results['report_path']}")
    print(f"All result files saved to: {results['output_dir']}")
    print("=" * 80 + "\n")
    
    # Open the report in the default browser
    try:
        import webbrowser
        webbrowser.open('file://' + os.path.abspath(results['report_path']))
        print("The report has been opened in your web browser.\n")
    except:
        print("Could not automatically open the report. Please open it manually.\n")
