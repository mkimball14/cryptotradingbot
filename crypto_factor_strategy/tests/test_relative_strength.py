#!/usr/bin/env python3
"""
Test script to evaluate the performance of the relative strength factor
"""

import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import strategy modules
from strategies.data_utils import load_coinbase_data
from strategies.factors import (
    UNIVERSE,
    calculate_momentum,
    calculate_volatility,
    calculate_relative_strength,
    cross_sectional_rank
)
from strategies.backtester import run_backtest

def test_relative_strength_calculation(window_sizes=[10, 30, 60]):
    """
    Test the calculation of relative strength with different window sizes.
    
    Args:
        window_sizes: List of window sizes to test
    """
    logger.info("Testing relative strength calculation with different window sizes...")
    
    # Load a small sample of data for testing
    symbols = UNIVERSE[:5]  # Use first 5 symbols
    start_dt = "2023-01-01T00:00:00Z"
    end_dt = "2023-03-01T00:00:00Z"  # 2 months of data
    
    ohlcv_data = load_coinbase_data(
        symbols=symbols,
        start_iso=start_dt,
        end_iso=end_dt,
        granularity="ONE_DAY"
    )
    
    if ohlcv_data is None or ohlcv_data.empty:
        logger.error("Failed to load data for relative strength testing")
        return
    
    close_prices = ohlcv_data['close']
    
    # Calculate relative strength for different windows
    results = {}
    for window in window_sizes:
        logger.info(f"Calculating relative strength with window={window}")
        start_time = time.time()
        rs = calculate_relative_strength(close_prices, window=window)
        elapsed = time.time() - start_time
        
        results[window] = {
            'data': rs,
            'elapsed': elapsed
        }
        
        logger.info(f"Window {window}: calculated in {elapsed:.4f} seconds")
    
    # Plot the results
    fig, axes = plt.subplots(len(window_sizes), 1, figsize=(12, 4 * len(window_sizes)))
    if len(window_sizes) == 1:
        axes = [axes]
        
    for i, window in enumerate(window_sizes):
        ax = axes[i]
        rs_data = results[window]['data']
        
        # Plot each symbol
        for symbol in symbols:
            if symbol == 'BTC-USD':
                continue  # Skip benchmark
            symbol_data = rs_data.xs(symbol, level='symbol')
            ax.plot(symbol_data.index, symbol_data, label=symbol)
        
        ax.set_title(f"Relative Strength (Window: {window} days)")
        ax.axhline(y=1.0, color='r', linestyle='--', alpha=0.5)  # Reference line
        ax.legend()
        ax.grid(True)
    
    plt.tight_layout()
    plt.savefig("relative_strength_test.png")
    plt.close()
    
    logger.info("Relative strength calculation test completed")
    return results

def compare_strategy_performance():
    """
    Compare the performance of strategies with and without the relative strength factor.
    """
    logger.info("Comparing strategy performance...")
    
    # Load data for all symbols
    start_dt = "2022-01-01T00:00:00Z"
    end_dt = "2023-12-31T00:00:00Z"  # 2 years of data
    
    ohlcv_data = load_coinbase_data(
        symbols=UNIVERSE,
        start_iso=start_dt,
        end_iso=end_dt,
        granularity="ONE_DAY"
    )
    
    if ohlcv_data is None or ohlcv_data.empty:
        logger.error("Failed to load data for strategy comparison")
        return
    
    close_prices = ohlcv_data['close']
    
    # Calculate factors
    momentum = calculate_momentum(close_prices, window=60)  # 60-day momentum
    volatility = calculate_volatility(close_prices, window=30)  # 30-day volatility
    rel_strength = calculate_relative_strength(close_prices, window=30)  # 30-day relative strength
    
    # Create factor rankings
    mom_rank = cross_sectional_rank(momentum)
    vol_rank = cross_sectional_rank(-volatility)  # Invert volatility (lower is better)
    rs_rank = cross_sectional_rank(rel_strength)
    
    # Create combined scores
    # Strategy 1: Momentum + Volatility (baseline)
    baseline_score = (mom_rank + vol_rank) / 2
    # Strategy 2: Momentum + Volatility + Relative Strength
    enhanced_score = (mom_rank + vol_rank + rs_rank) / 3
    
    # Run backtests
    logger.info("Running baseline strategy backtest...")
    baseline_results = run_backtest(
        combined_score=baseline_score,
        prices=close_prices,
        top_n=5,  # Invest in top 5 assets
        rebalance_freq='W-MON',  # Weekly rebalancing
        capital=10000,
        fee_pct=0.001,  # 0.1% trading fee
    )
    
    logger.info("Running enhanced strategy backtest...")
    enhanced_results = run_backtest(
        combined_score=enhanced_score,
        prices=close_prices,
        top_n=5,  # Invest in top 5 assets
        rebalance_freq='W-MON',  # Weekly rebalancing
        capital=10000,
        fee_pct=0.001,  # 0.1% trading fee
    )
    
    # Compare results
    if baseline_results and enhanced_results:
        # Extract key metrics
        metrics = {
            'Baseline': {
                'Sharpe Ratio': baseline_results.get('sharpe_ratio', 0),
                'Total Return': baseline_results.get('total_return', 0) * 100,
                'Max Drawdown': baseline_results.get('max_drawdown', 0) * 100,
                'Annual Volatility': baseline_results.get('annual_volatility', 0) * 100
            },
            'Enhanced': {
                'Sharpe Ratio': enhanced_results.get('sharpe_ratio', 0),
                'Total Return': enhanced_results.get('total_return', 0) * 100,
                'Max Drawdown': enhanced_results.get('max_drawdown', 0) * 100,
                'Annual Volatility': enhanced_results.get('annual_volatility', 0) * 100
            }
        }
        
        # Create DataFrame for easy comparison
        metrics_df = pd.DataFrame(metrics)
        logger.info("\nStrategy Performance Comparison:")
        logger.info(f"\n{metrics_df}")
        
        # Plot equity curves
        plt.figure(figsize=(12, 6))
        plt.plot(baseline_results.get('equity_curve'), label='Baseline Strategy')
        plt.plot(enhanced_results.get('equity_curve'), label='Enhanced with Relative Strength')
        plt.title('Strategy Performance Comparison')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.grid(True)
        plt.savefig("strategy_comparison.png")
        plt.close()
        
        return {
            'metrics': metrics_df,
            'baseline_results': baseline_results,
            'enhanced_results': enhanced_results
        }
    
    logger.error("Failed to compare strategies")
    return None

def analyze_factor_correlations():
    """
    Analyze correlations between momentum, volatility, and relative strength factors.
    """
    logger.info("Analyzing factor correlations...")
    
    # Load data for all symbols
    start_dt = "2022-01-01T00:00:00Z"
    end_dt = "2023-12-31T00:00:00Z"
    
    ohlcv_data = load_coinbase_data(
        symbols=UNIVERSE,
        start_iso=start_dt,
        end_iso=end_dt,
        granularity="ONE_DAY"
    )
    
    if ohlcv_data is None or ohlcv_data.empty:
        logger.error("Failed to load data for correlation analysis")
        return
    
    close_prices = ohlcv_data['close']
    
    # Calculate factors
    momentum = calculate_momentum(close_prices, window=60)
    volatility = calculate_volatility(close_prices, window=30)
    rel_strength = calculate_relative_strength(close_prices, window=30)
    
    # Combine factors into a single DataFrame
    factors_df = pd.DataFrame({
        'Momentum': momentum,
        'Volatility': volatility,
        'Relative Strength': rel_strength
    })
    
    # Drop NaN values
    factors_df = factors_df.dropna()
    
    # Calculate correlation matrix
    corr_matrix = factors_df.corr()
    logger.info("\nFactor Correlation Matrix:")
    logger.info(f"\n{corr_matrix}")
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    
    # Add correlation values
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                     ha='center', va='center', color='black')
    
    plt.colorbar(label='Correlation Coefficient')
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    plt.title('Factor Correlation Matrix')
    plt.tight_layout()
    plt.savefig("factor_correlations.png")
    plt.close()
    
    # Calculate rank correlations as well (Spearman)
    rank_corr = factors_df.rank().corr(method='spearman')
    logger.info("\nFactor Rank Correlation Matrix (Spearman):")
    logger.info(f"\n{rank_corr}")
    
    return {
        'correlation': corr_matrix,
        'rank_correlation': rank_corr
    }

if __name__ == "__main__":
    logger.info("=== Relative Strength Factor Evaluation ===")
    
    # Test relative strength calculation
    rs_results = test_relative_strength_calculation()
    
    # Compare strategy performance
    strategy_comparison = compare_strategy_performance()
    
    # Analyze factor correlations
    correlation_analysis = analyze_factor_correlations()
    
    logger.info("Evaluation complete. Check the generated plots for visual results.") 