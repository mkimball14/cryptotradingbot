#!/usr/bin/env python3
"""
Parameter Optimization for Crypto Trading Strategy

This script performs parameter optimization for the cryptocurrency trading strategy.
It supports both parameter sweep optimization (grid search) and walk-forward optimization
to find the most robust parameters that perform well across different market conditions.

Usage:
    python optimize.py --type sweep --momentum-windows 20,40,60 --volatility-windows 10,20,30 --top-n-values 3,5,10
    python optimize.py --type walk-forward --start-date 2022-01-01 --end-date 2023-01-01
    python optimize.py --type both --train-window-days 90 --test-window-days 30
"""

import os
import sys
import logging
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import itertools

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from strategies.crypto_factor_strategy import run_strategy
from strategies.optimizer import StrategyOptimizer

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_dir, f'optimize_{timestamp}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command-line arguments for the optimization."""
    parser = argparse.ArgumentParser(description='Optimize parameters for crypto trading strategy')
    
    # Optimization type
    parser.add_argument('--type', choices=['sweep', 'walk-forward', 'both'], default='both',
                        help='Type of optimization to perform (default: both)')
    
    # Parameter ranges
    parser.add_argument('--momentum-windows', type=str, default='20,40,60',
                        help='Comma-separated list of momentum windows to test (default: 20,40,60)')
    parser.add_argument('--volatility-windows', type=str, default='10,20,30',
                        help='Comma-separated list of volatility windows to test (default: 10,20,30)')
    parser.add_argument('--top-n-values', type=str, default='3,5,10',
                        help='Comma-separated list of top-N values to test (default: 3,5,10)')
    parser.add_argument('--rebalance-days', type=str, default='7,14,30',
                        help='Comma-separated list of rebalance frequencies to test (default: 7,14,30)')
                        
    # Date ranges
    parser.add_argument('--start-date', type=str, default='2021-01-01',
                        help='Start date for backtesting (default: 2021-01-01)')
    parser.add_argument('--end-date', type=str, default='2023-12-31',
                        help='End date for backtesting (default: 2023-12-31)')
                        
    # Walk-forward optimization parameters
    parser.add_argument('--train-window-days', type=int, default=180,
                        help='Number of days for training window in walk-forward optimization (default: 180)')
    parser.add_argument('--test-window-days', type=int, default=60,
                        help='Number of days for test window in walk-forward optimization (default: 60)')
    parser.add_argument('--overlap-pct', type=int, default=30,
                        help='Percentage of overlap between consecutive windows (default: 30)')
                        
    # Other parameters
    parser.add_argument('--initial-capital', type=float, default=10000.0,
                        help='Initial capital for backtesting (default: 10000.0)')
    parser.add_argument('--metric', type=str, default='Sharpe Ratio',
                        help='Metric to optimize (default: Sharpe Ratio)')
    parser.add_argument('--cache-data', action='store_true',
                        help='Cache data to speed up optimization runs')
    parser.add_argument('--plot', action='store_true',
                        help='Generate and save parameter impact plots')
    
    return parser.parse_args()

def parse_list(comma_separated_str, dtype=int):
    """Parse a comma-separated string into a list of values."""
    return [dtype(x.strip()) for x in comma_separated_str.split(',')]

def main():
    """Main function to run parameter optimization."""
    args = parse_args()
    
    # Create results directory
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', f'optimize_{timestamp}')
    os.makedirs(results_dir, exist_ok=True)
    
    logger.info("Starting parameter optimization with the following configuration:")
    logger.info(f"Optimization type: {args.type}")
    logger.info(f"Time period: {args.start_date} to {args.end_date}")
    
    # Parse parameter ranges
    momentum_windows = parse_list(args.momentum_windows)
    volatility_windows = parse_list(args.volatility_windows)
    top_n_values = parse_list(args.top_n_values)
    rebalance_days = parse_list(args.rebalance_days)
    
    logger.info(f"Parameter ranges:")
    logger.info(f"  Momentum windows: {momentum_windows}")
    logger.info(f"  Volatility windows: {volatility_windows}")
    logger.info(f"  Top N values: {top_n_values}")
    logger.info(f"  Rebalance days: {rebalance_days}")
    
    # Create parameter grid
    param_grid = {
        'momentum_window': momentum_windows,
        'volatility_window': volatility_windows,
        'top_n': top_n_values,
        'rebalance_days': rebalance_days
    }
    
    # Fixed parameters
    fixed_params = {
        'initial_capital': args.initial_capital,
        'cache_data': args.cache_data
    }
    
    # Create optimizer
    optimizer = StrategyOptimizer(run_strategy, metric_to_optimize=args.metric)
    
    # Perform parameter sweep
    if args.type in ['sweep', 'both']:
        logger.info("Starting parameter sweep optimization")
        
        # Add date range to fixed parameters
        sweep_params = {
            **fixed_params,
            'start_date': args.start_date,
            'end_date': args.end_date
        }
        
        # Run parameter sweep
        sweep_results = optimizer.parameter_sweep(param_grid, sweep_params)
        
        # Save results
        sweep_file = os.path.join(results_dir, 'parameter_sweep_results.csv')
        sweep_results.to_csv(sweep_file, index=False)
        logger.info(f"Parameter sweep results saved to {sweep_file}")
        
        # Display top results
        top_n = min(5, len(sweep_results))
        print(f"\nTop {top_n} parameter combinations:")
        print(sweep_results.head(top_n)[[*param_grid.keys(), args.metric]])
        
        # Generate parameter impact plot
        if args.plot:
            plot_file = os.path.join(results_dir, 'parameter_impact.png')
            optimizer.generate_parameter_impact_plot(sweep_results, plot_file)
            logger.info(f"Parameter impact plot saved to {plot_file}")
    
    # Perform walk-forward optimization
    if args.type in ['walk-forward', 'both']:
        logger.info("Starting walk-forward optimization")
        
        # Run walk-forward optimization
        wfo_results = optimizer.walk_forward_optimization(
            param_grid, 
            fixed_params,
            args.start_date,
            args.end_date,
            train_window_days=args.train_window_days,
            test_window_days=args.test_window_days,
            overlap_pct=args.overlap_pct
        )
        
        # Save window results
        if wfo_results['window_results']:
            window_results_file = os.path.join(results_dir, 'walk_forward_window_results.csv')
            window_df = pd.DataFrame(wfo_results['window_results'])
            window_df.to_csv(window_results_file, index=False)
            logger.info(f"Walk-forward window results saved to {window_results_file}")
            
            # Plot train vs test metrics
            if args.plot:
                train_col = f'train_{args.metric}'
                test_col = f'test_{args.metric}'
                
                if train_col in window_df.columns and test_col in window_df.columns:
                    plt.figure(figsize=(12, 6))
                    plt.plot(window_df['window'], window_df[train_col], marker='o', label='Training')
                    plt.plot(window_df['window'], window_df[test_col], marker='x', label='Testing')
                    plt.title('Training vs Testing Performance Across Windows')
                    plt.xlabel('Window Number')
                    plt.ylabel(args.metric)
                    plt.grid(True, linestyle='--', alpha=0.7)
                    plt.legend()
                    train_test_plot = os.path.join(results_dir, 'train_test_comparison.png')
                    plt.savefig(train_test_plot, dpi=300, bbox_inches='tight')
                    logger.info(f"Train vs test comparison plot saved to {train_test_plot}")
            
        # Save overall results
        overall_results_file = os.path.join(results_dir, 'walk_forward_results.json')
        with open(overall_results_file, 'w') as f:
            # Extract only serializable parts
            json_results = {
                'overall_stats': wfo_results['overall_stats'],
                'robust_params': wfo_results['robust_params']
            }
            json.dump(json_results, f, indent=4)
        logger.info(f"Walk-forward optimization results saved to {overall_results_file}")
        
        # Display results
        print("\nWalk-Forward Optimization Results:")
        print("\nOverall Statistics:")
        for stat, value in wfo_results['overall_stats'].items():
            print(f"  {stat}: {value:.4f}" if isinstance(value, float) else f"  {stat}: {value}")
        
        print("\nMost Robust Parameters:")
        for param, value in wfo_results['robust_params'].items():
            print(f"  {param}: {value}")
        
        if wfo_results['window_results']:
            print("\nPerformance by Window:")
            window_df = pd.DataFrame(wfo_results['window_results'])
            print(window_df[['window', f'test_{args.metric}', *param_grid.keys()]].head(10))
    
    logger.info("Optimization complete")
    print(f"\nAll results saved to {results_dir}")
    print(f"Log file: {log_file}")

if __name__ == "__main__":
    main() 