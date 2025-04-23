#!/usr/bin/env python3
"""
Test Script for the Strategy Optimizer

This script tests the StrategyOptimizer class with a simple mock strategy function
to ensure it's working correctly before using it with the actual trading strategy.
"""

import os
import sys
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the optimizer
from strategies.optimizer import StrategyOptimizer

def mock_strategy(**params):
    """
    A mock strategy function that returns random performance metrics
    but with some correlation to input parameters to simulate a real strategy.
    
    This is used to test the optimizer without running the full strategy.
    """
    # Extract parameters
    param_a = params.get('param_a', 10)
    param_b = params.get('param_b', 5)
    param_c = params.get('param_c', 3)
    
    # Simulate a dependency between parameters and performance
    # Best performance around param_a=30, param_b=10, param_c=5
    # with some randomness added
    
    # Base performance - higher is better
    sharpe_base = -0.5 + 0.1 * (param_a / 10) - 0.005 * ((param_a - 30) ** 2)
    sharpe_base += 0.05 * (param_b / 5) - 0.01 * ((param_b - 10) ** 2)
    sharpe_base += 0.03 * (param_c) - 0.02 * ((param_c - 5) ** 2)
    
    # Add some noise to simulate market randomness
    noise = random.uniform(-0.5, 0.5)
    sharpe = max(0, sharpe_base + noise)
    
    # Calculate other metrics based on Sharpe
    returns = sharpe * 0.05
    volatility = returns / sharpe if sharpe > 0 else 0.2
    max_drawdown = -0.1 - (0.1 * (1 - sharpe/3)) if sharpe < 3 else -0.1
    
    # Create results dictionary similar to what the real strategy would return
    results = {
        'metrics': {
            'Sharpe Ratio': sharpe,
            'Total Return': returns,
            'Volatility': volatility,
            'Max Drawdown': max_drawdown,
            'Win Rate': min(0.9, 0.3 + sharpe * 0.1)
        },
        'parameters': {
            'param_a': param_a,
            'param_b': param_b,
            'param_c': param_c
        }
    }
    
    # Print progress update
    print(f"Testing parameters: a={param_a}, b={param_b}, c={param_c}, Sharpe={sharpe:.2f}")
    
    return results

def test_parameter_sweep():
    """Test the parameter_sweep method of StrategyOptimizer."""
    print("\n=== Testing Parameter Sweep Optimization ===")
    
    # Create optimizer with mock strategy
    optimizer = StrategyOptimizer(mock_strategy, metric_to_optimize='Sharpe Ratio')
    
    # Define parameter grid
    param_grid = {
        'param_a': [10, 20, 30, 40],
        'param_b': [5, 10, 15],
        'param_c': [2, 5, 8]
    }
    
    # Define fixed parameters
    fixed_params = {
        'other_param': 'test'
    }
    
    # Run parameter sweep
    results = optimizer.parameter_sweep(param_grid, fixed_params)
    
    # Display results
    print("\nTop 5 parameter combinations:")
    print(results.head(5))
    
    # Generate and show parameter impact plot
    plt.figure(figsize=(12, 10))
    optimizer.generate_parameter_impact_plot(results, show_plot=True)
    
    return results

def test_walk_forward_optimization():
    """Test the walk_forward_optimization method of StrategyOptimizer."""
    print("\n=== Testing Walk-Forward Optimization ===")
    
    # Create optimizer with mock strategy
    optimizer = StrategyOptimizer(mock_strategy, metric_to_optimize='Sharpe Ratio')
    
    # Define parameter grid - smaller for faster testing
    param_grid = {
        'param_a': [20, 30, 40],
        'param_b': [5, 10],
        'param_c': [3, 5]
    }
    
    # Define fixed parameters
    fixed_params = {
        'other_param': 'test'
    }
    
    # Define date range
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    
    # Run walk-forward optimization
    results = optimizer.walk_forward_optimization(
        param_grid, 
        fixed_params,
        start_date,
        end_date,
        train_window_days=60,
        test_window_days=30,
        overlap_pct=0  # No overlap for simplicity in testing
    )
    
    # Display results
    print("\nWalk-Forward Optimization Results:")
    print("\nOverall Statistics:")
    for stat, value in results['overall_stats'].items():
        print(f"  {stat}: {value:.4f}" if isinstance(value, float) else f"  {stat}: {value}")
    
    print("\nMost Robust Parameters:")
    for param, value in results['robust_params'].items():
        print(f"  {param}: {value}")
    
    if results['window_results']:
        print("\nWindow Results (sample):")
        window_df = pd.DataFrame(results['window_results'])
        print(window_df.head())
        
        # Plot train vs test metrics
        plt.figure(figsize=(10, 6))
        plt.plot(window_df['window'], window_df['train_Sharpe Ratio'], marker='o', label='Training')
        plt.plot(window_df['window'], window_df['test_Sharpe Ratio'], marker='x', label='Testing')
        plt.title('Training vs Testing Performance Across Windows')
        plt.xlabel('Window Number')
        plt.ylabel('Sharpe Ratio')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.show()
    
    return results

def main():
    """Run all tests."""
    print("Starting optimizer tests...")
    
    # Test parameter sweep
    sweep_results = test_parameter_sweep()
    
    # Test walk-forward optimization
    wfo_results = test_walk_forward_optimization()
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main() 