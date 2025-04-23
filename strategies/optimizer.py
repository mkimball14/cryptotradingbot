#!/usr/bin/env python3
"""
Strategy Optimizer Module

This module provides optimization capabilities for cryptocurrency factor-based trading strategies.
It implements parameter sweep and walk-forward optimization to find optimal strategy parameters
while evaluating performance over time to avoid overfitting.
"""

import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import itertools
import json

# Configure logging
logger = logging.getLogger(__name__)

class StrategyOptimizer:
    """
    Class to optimize trading strategy parameters using various techniques.
    
    Supports:
    - Parameter sweep (grid search)
    - Walk-forward optimization
    - Parameter robustness analysis
    """
    
    def __init__(self, strategy_function, metric_to_optimize='Sharpe Ratio'):
        """
        Initialize the optimizer.
        
        Args:
            strategy_function: Function that runs the strategy with parameters and returns performance metrics
            metric_to_optimize: Performance metric to optimize for
        """
        self.strategy_function = strategy_function
        self.metric_to_optimize = metric_to_optimize
        self.results_df = None
    
    def parameter_sweep(self, param_grid, fixed_params=None):
        """
        Run the strategy with different parameter combinations and return the results.
        
        Args:
            param_grid: Dictionary where keys are parameter names and values are lists of parameter values
            fixed_params: Dictionary of parameters that remain fixed across all runs
            
        Returns:
            DataFrame with results for each parameter combination, sorted by the optimization metric
        """
        fixed_params = fixed_params or {}
        
        # Create all combinations of parameters
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        param_combinations = list(itertools.product(*param_values))
        
        logger.info(f"Running parameter sweep with {len(param_combinations)} combinations")
        
        results = []
        
        # Run strategy with each parameter combination
        for i, combination in enumerate(param_combinations):
            params = dict(zip(param_names, combination))
            full_params = {**fixed_params, **params}
            
            # Create a unique run ID
            run_id = f"run_{i+1:04d}"
            
            try:
                logger.info(f"Run {i+1}/{len(param_combinations)}: Testing {params}")
                
                # Run the strategy with these parameters
                strategy_result = self.strategy_function(**full_params)
                
                if strategy_result and 'metrics' in strategy_result:
                    # Get performance metrics
                    metrics = strategy_result['metrics']
                    
                    # Combine parameters and metrics
                    result_row = {**params, **metrics, 'run_id': run_id}
                    results.append(result_row)
                    
                    logger.info(f"Run {i+1} completed: {self.metric_to_optimize}={metrics.get(self.metric_to_optimize, 'N/A')}")
                else:
                    logger.warning(f"Run {i+1} failed: No valid metrics returned")
            
            except Exception as e:
                logger.error(f"Error in run {i+1}: {str(e)}")
        
        if not results:
            logger.error("No valid results from parameter sweep")
            return pd.DataFrame()
        
        # Convert results to DataFrame
        results_df = pd.DataFrame(results)
        
        # Sort by the optimization metric (descending)
        if self.metric_to_optimize in results_df.columns:
            results_df = results_df.sort_values(by=self.metric_to_optimize, ascending=False)
        
        self.results_df = results_df
        return results_df
    
    def walk_forward_optimization(self, param_grid, fixed_params, start_date, end_date, 
                                  train_window_days=180, test_window_days=60, overlap_pct=30):
        """
        Perform walk-forward optimization.
        
        Args:
            param_grid: Dictionary of parameters to optimize
            fixed_params: Dictionary of fixed parameters
            start_date: Start date for the entire period
            end_date: End date for the entire period
            train_window_days: Number of days in training window
            test_window_days: Number of days in test window
            overlap_pct: Percentage of overlap between consecutive windows
            
        Returns:
            Dictionary containing:
                - window_results: List of results for each window
                - overall_stats: Overall performance statistics
                - robust_params: Most robust parameters across windows
        """
        # Parse dates
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt = pd.to_datetime(end_date)
        
        # Calculate window shifts
        shift_days = int(test_window_days * (1 - overlap_pct/100))
        if shift_days <= 0:
            shift_days = 1
            logger.warning("Overlap percentage too high, setting shift to 1 day")
        
        # Calculate window start and end dates
        current_start = start_date_dt
        window_results = []
        window_count = 0
        
        while current_start + timedelta(days=train_window_days + test_window_days) <= end_date_dt:
            window_count += 1
            train_start = current_start
            train_end = train_start + timedelta(days=train_window_days)
            test_start = train_end
            test_end = test_start + timedelta(days=test_window_days)
            
            logger.info(f"Window {window_count}:")
            logger.info(f"  Training: {train_start.strftime('%Y-%m-%d')} to {train_end.strftime('%Y-%m-%d')}")
            logger.info(f"  Testing: {test_start.strftime('%Y-%m-%d')} to {test_end.strftime('%Y-%m-%d')}")
            
            # Create parameters for training period
            train_params = {
                **fixed_params,
                'start_date': train_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'end_date': train_end.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
            # Run parameter sweep on training period
            train_results = self.parameter_sweep(param_grid, train_params)
            
            if train_results.empty:
                logger.warning(f"No valid results for training window {window_count}, skipping")
                current_start += timedelta(days=shift_days)
                continue
            
            # Get best parameters from training
            best_params = {}
            for param in param_grid.keys():
                if param in train_results.columns:
                    best_params[param] = train_results.iloc[0][param]
            
            best_train_metric = train_results.iloc[0].get(self.metric_to_optimize, float('nan'))
            
            # Create parameters for test period
            test_params = {
                **fixed_params,
                **best_params,
                'start_date': test_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'end_date': test_end.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
            # Run strategy on test period with best parameters
            try:
                test_result = self.strategy_function(**test_params)
                
                if test_result and 'metrics' in test_result:
                    test_metrics = test_result['metrics']
                    test_metric = test_metrics.get(self.metric_to_optimize, float('nan'))
                    
                    # Record window results
                    window_result = {
                        'window': window_count,
                        'train_start': train_start.strftime('%Y-%m-%d'),
                        'train_end': train_end.strftime('%Y-%m-%d'),
                        'test_start': test_start.strftime('%Y-%m-%d'),
                        'test_end': test_end.strftime('%Y-%m-%d'),
                        f'train_{self.metric_to_optimize}': best_train_metric,
                        f'test_{self.metric_to_optimize}': test_metric,
                        **best_params
                    }
                    
                    # Add all test metrics with test_ prefix
                    for metric, value in test_metrics.items():
                        if metric != self.metric_to_optimize:
                            window_result[f'test_{metric}'] = value
                    
                    window_results.append(window_result)
                    
                    logger.info(f"Window {window_count} completed:")
                    logger.info(f"  Best training {self.metric_to_optimize}: {best_train_metric:.4f}")
                    logger.info(f"  Test {self.metric_to_optimize}: {test_metric:.4f}")
                    
                else:
                    logger.warning(f"No valid test metrics for window {window_count}")
            
            except Exception as e:
                logger.error(f"Error in test window {window_count}: {str(e)}")
            
            # Move to next window
            current_start += timedelta(days=shift_days)
        
        # If no valid windows, return empty result
        if not window_results:
            logger.error("No valid windows in walk-forward optimization")
            return {'window_results': [], 'overall_stats': {}, 'robust_params': {}}
        
        # Calculate overall statistics
        window_df = pd.DataFrame(window_results)
        
        train_metric_col = f'train_{self.metric_to_optimize}'
        test_metric_col = f'test_{self.metric_to_optimize}'
        
        avg_train_metric = window_df[train_metric_col].mean()
        avg_test_metric = window_df[test_metric_col].mean()
        
        # Calculate decay from train to test
        train_test_decay = 1 - (avg_test_metric / avg_train_metric) if avg_train_metric > 0 else float('nan')
        
        # Calculate percentage of windows where test performance maintains at least 70% of train performance
        consistent_windows = (window_df[test_metric_col] >= 0.7 * window_df[train_metric_col]).mean()
        
        # Find most robust parameters across windows
        robust_params = self._find_robust_parameters(window_df, param_grid.keys())
        
        # Compile overall results
        overall_stats = {
            'total_windows': len(window_results),
            'avg_train_metric': avg_train_metric,
            'avg_test_metric': avg_test_metric,
            'train_test_decay': train_test_decay,
            'consistent_windows': consistent_windows
        }
        
        return {
            'window_results': window_results,
            'overall_stats': overall_stats,
            'robust_params': robust_params
        }
    
    def _find_robust_parameters(self, window_df, param_names):
        """
        Find the most robust parameters across all windows.
        
        A robust parameter is one that consistently performs well in the test period.
        
        Args:
            window_df: DataFrame containing window results
            param_names: Names of parameters to analyze
            
        Returns:
            Dictionary of most robust parameter values
        """
        test_metric_col = f'test_{self.metric_to_optimize}'
        robust_params = {}
        
        for param in param_names:
            if param in window_df.columns:
                # Group by parameter value and get mean test metric
                if window_df[param].nunique() > 1:
                    grouped = window_df.groupby(param)[test_metric_col].mean()
                    
                    # The most robust value is the one with highest mean test metric
                    best_value = grouped.idxmax()
                    robust_params[param] = best_value
                else:
                    # If there's only one value, it's the most robust by default
                    robust_params[param] = window_df[param].iloc[0]
        
        return robust_params
        
    def generate_parameter_impact_plot(self, results_df=None, save_path=None):
        """
        Generate plots showing the impact of each parameter on performance.
        
        Args:
            results_df: DataFrame with results. If None, uses the stored results.
            save_path: Path to save the plot. If None, plot is not saved.
            
        Returns:
            Matplotlib figure object, or None if plotting fails
        """
        df = results_df if results_df is not None else self.results_df
        
        if df is None or df.empty:
            logger.error("No results available for plotting")
            return None
        
        # Get parameter columns (those that vary in the DataFrame)
        param_cols = [col for col in df.columns if col not in 
                      ['run_id', self.metric_to_optimize] and 
                      df[col].nunique() > 1]
        
        if not param_cols:
            logger.warning("No varying parameters found for plotting")
            return None
        
        # Create plot with a subplot for each parameter
        n_params = len(param_cols)
        fig, axes = plt.subplots(nrows=n_params, figsize=(10, 5 * n_params))
        if n_params == 1:
            axes = [axes]  # Ensure axes is a list for single subplot
            
        for i, param in enumerate(param_cols):
            # Group by parameter and calculate mean of the optimization metric
            grouped = df.groupby(param)[self.metric_to_optimize].mean().reset_index()
            
            # Sort by parameter value for plotting
            grouped = grouped.sort_values(param)
            
            # Plot parameter vs. optimization metric
            ax = axes[i]
            
            # Use seaborn barplot for discrete parameters, line plot for others
            if df[param].dtype in [np.int64, np.int32, np.float64, np.float32]:
                sns.lineplot(data=grouped, x=param, y=self.metric_to_optimize, 
                            marker='o', ax=ax, color='steelblue')
            else:
                sns.barplot(data=grouped, x=param, y=self.metric_to_optimize, ax=ax)
            
            ax.set_title(f"Impact of {param} on {self.metric_to_optimize}")
            ax.set_xlabel(param)
            ax.set_ylabel(self.metric_to_optimize)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Add labels above each bar/point
            for j, p in enumerate(grouped[param]):
                metric_val = grouped[self.metric_to_optimize].iloc[j]
                ax.annotate(f"{metric_val:.4f}", 
                           (p, metric_val),
                           ha='center', va='bottom',
                           fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Parameter impact plot saved to {save_path}")
        
        return fig


# --- Example Usage ---
if __name__ == "__main__":
    # This would be replaced with the actual run_strategy function
    def dummy_run_strategy(**params):
        """Dummy strategy execution function for testing."""
        import time
        import random
        time.sleep(0.1)  # Simulate computation time
        
        # Simulate success/failure
        if random.random() < 0.9:  # 90% success rate
            # Generate dummy metrics based on parameters
            sharpe = params.get('momentum_window', 60) / 100.0 + random.normalvariate(0, 0.2)
            ret = params.get('top_n', 3) * 0.05 + random.normalvariate(0, 0.1)
            dd = params.get('volatility_window', 20) / 100.0 + random.normalvariate(0, 0.05)
            
            return {
                'metrics': {
                    'Sharpe Ratio': sharpe,
                    'Total Return (%)': ret * 100,
                    'Max Drawdown (%)': dd * 100
                }
            }
        else:
            return None  # Simulate failure
    
    # Create optimizer with dummy function
    optimizer = StrategyOptimizer(dummy_run_strategy)
    
    # Define parameter grid
    param_grid = {
        'momentum_window': [30, 45, 60, 90],
        'volatility_window': [15, 21, 30],
        'top_n': [2, 3, 4]
    }
    
    # Base parameters (constants)
    base_params = {
        'universe': ['BTC-USD', 'ETH-USD'],
        'start_date': '2022-01-01T00:00:00Z',
        'end_date': '2022-12-31T00:00:00Z',
        'max_weight': 0.5,
        'init_cash': 100000
    }
    
    # Run parameter sweep
    print("Running parameter sweep...")
    sweep_results = optimizer.parameter_sweep(param_grid, base_params)
    
    if not sweep_results.empty:
        print(f"Parameter sweep complete with {len(sweep_results)} results")
        print("\nTop 5 parameter sets by Sharpe Ratio:")
        print(sweep_results.sort_values('Sharpe Ratio', ascending=False).head())
        
        # Save results
        results_dir = optimizer.save_results(sweep_results)
        
        # Plot parameter impact
        fig = optimizer.generate_parameter_impact_plot(sweep_results)
        plt.close(fig)
    
    # Run walk-forward optimization
    print("\nRunning walk-forward optimization...")
    wfo_results = optimizer.walk_forward_optimization(
        param_grid=param_grid,
        fixed_params=base_params,
        start_date='2021-01-01T00:00:00Z',
        end_date='2022-12-31T00:00:00Z',
        train_window_days=180,
        test_window_days=90,
        overlap_pct=30
    )
    
    if wfo_results['window_results']:
        print(f"Walk-forward optimization complete with {len(wfo_results['window_results'])} windows")
        print("\nResults by window:")
        print(pd.DataFrame(wfo_results['window_results'])[['window', 'test_metric', 'momentum_window', 'volatility_window', 'top_n']])
        
        # Save WFO results
        optimizer.save_results(pd.DataFrame(wfo_results['window_results']), "walk_forward_results.csv")
        
        # Plot WFO results
        fig = optimizer.generate_parameter_impact_plot(pd.DataFrame(wfo_results['window_results']))
        plt.close(fig)
        
        print("\nOverall statistics:")
        print(pd.Series(wfo_results['overall_stats']))
        
        print("\nParameter robustness:")
        for param, robustness in wfo_results['robust_params'].items():
            print(f"{param}: {robustness}")
        
        print("\nMost robust parameters:")
        for param, value in wfo_results['robust_params'].items():
            print(f"{param}: {value}")
    
    print(f"\nAll results saved to {results_dir}") 