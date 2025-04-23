#!/usr/bin/env python3
"""
Test script to evaluate the performance of the mean reversion factor
"""

import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    calculate_mean_reversion,
    cross_sectional_rank
)
from strategies.portfolio import (
    calculate_equal_weights,
    calculate_top_n_weights
)
from strategies.backtester import run_factor_backtest

def test_mean_reversion_calculation(ma_windows=[20, 50, 100], z_windows=[10, 20, 30]):
    """
    Test the calculation of mean reversion with different window sizes.
    
    Args:
        ma_windows: List of moving average window sizes to test
        z_windows: List of z-score window sizes to test
    """
    logger.info("Testing mean reversion calculation with different window sizes...")
    
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
        logger.error("Failed to load data for mean reversion testing")
        return
    
    close_prices = ohlcv_data['close']
    
    # Calculate mean reversion for different parameter combinations
    results = {}
    for ma_window in ma_windows:
        for z_window in z_windows:
            if z_window > ma_window:
                continue  # Skip invalid combinations
                
            logger.info(f"Calculating mean reversion with ma_window={ma_window}, z_window={z_window}")
            start_time = time.time()
            mr = calculate_mean_reversion(close_prices, ma_window=ma_window, z_window=z_window)
            elapsed = time.time() - start_time
            
            results[(ma_window, z_window)] = {
                'data': mr,
                'elapsed': elapsed
            }
            
            logger.info(f"Parameters ({ma_window}, {z_window}): calculated in {elapsed:.4f} seconds")
    
    # Plot the results
    fig, axes = plt.subplots(len(ma_windows), 1, figsize=(12, 4 * len(ma_windows)))
    if len(ma_windows) == 1:
        axes = [axes]
        
    for i, ma_window in enumerate(ma_windows):
        ax = axes[i]
        
        # Get a valid z_window
        valid_z_windows = [z for z in z_windows if z <= ma_window]
        if not valid_z_windows:
            continue
            
        z_window = valid_z_windows[0]
        mr_data = results.get((ma_window, z_window), {}).get('data')
        
        if mr_data is None:
            continue
            
        # Plot each symbol
        for symbol in symbols:
            try:
                symbol_data = mr_data.xs(symbol, level='symbol')
                ax.plot(symbol_data.index, symbol_data, label=symbol)
            except:
                logger.warning(f"Could not plot data for {symbol}")
        
        ax.set_title(f"Mean Reversion (MA Window: {ma_window}, Z Window: {z_window})")
        ax.axhline(y=0.0, color='r', linestyle='--', alpha=0.5)  # Reference line
        ax.legend()
        ax.grid(True)
    
    plt.tight_layout()
    plt.savefig("mean_reversion_test.png")
    plt.close()
    
    logger.info("Mean reversion calculation test completed")
    return results

def analyze_mean_reversion_effectiveness():
    """
    Analyze the effectiveness of the mean reversion factor by testing it against momentum factor.
    """
    logger.info("Analyzing mean reversion factor effectiveness...")
    
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
        logger.error("Failed to load data for factor analysis")
        return
    
    close_prices = ohlcv_data['close']
    
    # Calculate factors with different parameters
    momentum_60d = calculate_momentum(close_prices, window=60)  # 60-day momentum
    mean_rev_50d = calculate_mean_reversion(close_prices, ma_window=50, z_window=20)  # 50-day mean reversion
    
    # Calculate factor ranks
    mom_rank = cross_sectional_rank(momentum_60d)
    mean_rev_rank = cross_sectional_rank(mean_rev_50d)
    
    # Analyze factor correlations
    combined_df = pd.DataFrame({
        'Momentum': mom_rank,
        'Mean Reversion': mean_rev_rank
    }).dropna()
    
    corr = combined_df.corr()
    logger.info(f"Factor correlation:\n{corr}")
    
    # Calculate IC (Information Coefficient) - correlation with future returns
    # For each day, get the correlation between factor value and next 5-day return
    future_returns = close_prices.groupby(level='symbol').pct_change(periods=5).shift(-5)
    
    # Create DataFrame with factors and future returns
    ic_data = pd.DataFrame({
        'Momentum': mom_rank,
        'Mean Reversion': mean_rev_rank,
        'Future_Return': future_returns
    }).dropna()
    
    # Calculate IC per day
    ic_by_day = {}
    for date in ic_data.index.get_level_values('date').unique():
        day_data = ic_data.xs(date, level='date')
        mom_ic = day_data['Momentum'].corr(day_data['Future_Return'])
        mr_ic = day_data['Mean Reversion'].corr(day_data['Future_Return'])
        ic_by_day[date] = {'Momentum': mom_ic, 'Mean Reversion': mr_ic}
    
    ic_df = pd.DataFrame(ic_by_day).T
    
    # Calculate average IC
    avg_ic = ic_df.mean()
    logger.info(f"Average Information Coefficient (IC):\n{avg_ic}")
    
    # Plot IC over time
    plt.figure(figsize=(12, 6))
    plt.plot(ic_df.index, ic_df['Momentum'], label='Momentum IC')
    plt.plot(ic_df.index, ic_df['Mean Reversion'], label='Mean Reversion IC')
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    plt.title('Information Coefficient (IC) Over Time')
    plt.xlabel('Date')
    plt.ylabel('IC Value')
    plt.legend()
    plt.grid(True)
    plt.savefig("factor_ic_comparison.png")
    plt.close()
    
    # Run single-factor backtests
    # Momentum only
    mom_weights = calculate_top_n_weights(mom_rank, n=3)
    mom_portfolio = run_factor_backtest(
        close_prices=close_prices,
        target_weights=mom_weights,
        init_cash=100000,
        fees=0.001,
        slippage=0.0005
    )
    
    # Mean Reversion only
    mr_weights = calculate_top_n_weights(mean_rev_rank, n=3)
    mr_portfolio = run_factor_backtest(
        close_prices=close_prices,
        target_weights=mr_weights,
        init_cash=100000,
        fees=0.001,
        slippage=0.0005
    )
    
    # Combined (50/50)
    combined_rank = (mom_rank + mean_rev_rank) / 2
    combined_weights = calculate_top_n_weights(combined_rank, n=3)
    combined_portfolio = run_factor_backtest(
        close_prices=close_prices,
        target_weights=combined_weights,
        init_cash=100000,
        fees=0.001,
        slippage=0.0005
    )
    
    # Extract equity curves
    if mom_portfolio and mr_portfolio and combined_portfolio:
        mom_equity = mom_portfolio.asset_value()
        mr_equity = mr_portfolio.asset_value()
        combined_equity = combined_portfolio.asset_value()
        
        # Plot equity curves
        plt.figure(figsize=(12, 6))
        plt.plot(mom_equity.index, mom_equity, label='Momentum Only')
        plt.plot(mr_equity.index, mr_equity, label='Mean Reversion Only')
        plt.plot(combined_equity.index, combined_equity, label='Combined (50/50)')
        plt.title('Factor Strategy Performance Comparison')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.grid(True)
        plt.savefig("factor_performance_comparison.png")
        plt.close()
        
        # Calculate performance metrics
        metrics = {
            'Momentum': {
                'Total Return (%)': ((mom_equity.iloc[-1] / mom_equity.iloc[0]) - 1) * 100,
                'Annual Return (%)': mom_portfolio.stats()['Annual Return (%)'],
                'Sharpe Ratio': mom_portfolio.stats()['Sharpe Ratio'],
                'Max Drawdown (%)': mom_portfolio.stats()['Max Drawdown (%)']
            },
            'Mean Reversion': {
                'Total Return (%)': ((mr_equity.iloc[-1] / mr_equity.iloc[0]) - 1) * 100,
                'Annual Return (%)': mr_portfolio.stats()['Annual Return (%)'],
                'Sharpe Ratio': mr_portfolio.stats()['Sharpe Ratio'],
                'Max Drawdown (%)': mr_portfolio.stats()['Max Drawdown (%)']
            },
            'Combined': {
                'Total Return (%)': ((combined_equity.iloc[-1] / combined_equity.iloc[0]) - 1) * 100,
                'Annual Return (%)': combined_portfolio.stats()['Annual Return (%)'],
                'Sharpe Ratio': combined_portfolio.stats()['Sharpe Ratio'],
                'Max Drawdown (%)': combined_portfolio.stats()['Max Drawdown (%)']
            }
        }
        
        metrics_df = pd.DataFrame(metrics)
        logger.info(f"\nPerformance Comparison:\n{metrics_df}")
        
        # Save metrics to file
        metrics_df.to_csv("factor_performance_metrics.csv")
        
        return {
            'correlation': corr,
            'ic': avg_ic,
            'ic_over_time': ic_df,
            'metrics': metrics_df,
            'portfolios': {
                'momentum': mom_portfolio,
                'mean_reversion': mr_portfolio,
                'combined': combined_portfolio
            }
        }
    
    logger.error("One or more backtests failed")
    return None

def analyze_market_regimes():
    """
    Analyze how mean reversion and momentum factors perform in different market regimes.
    """
    logger.info("Analyzing factor performance across market regimes...")
    
    # Load data for all symbols
    start_dt = "2022-01-01T00:00:00Z"
    end_dt = "2023-12-31T00:00:00Z"  # 2 years of data
    
    ohlcv_data = load_coinbase_data(
        symbols=['BTC-USD'],  # Use BTC as market proxy
        start_iso=start_dt,
        end_iso=end_dt,
        granularity="ONE_DAY"
    )
    
    if ohlcv_data is None or ohlcv_data.empty:
        logger.error("Failed to load data for market regime analysis")
        return
    
    # Define market regimes based on BTC volatility and trend
    btc_close = ohlcv_data.xs('BTC-USD', level='symbol')['close']
    btc_returns = btc_close.pct_change().dropna()
    
    # 30-day volatility (annualized)
    btc_vol = btc_returns.rolling(window=30).std() * np.sqrt(365)
    
    # 30-day trend (simple moving average direction)
    sma_30 = btc_close.rolling(window=30).mean()
    sma_90 = btc_close.rolling(window=90).mean()
    btc_trend = sma_30 - sma_90
    
    # Define regimes
    # High Vol + Up Trend = Strong Bull
    # High Vol + Down Trend = Strong Bear
    # Low Vol + Up Trend = Weak Bull
    # Low Vol + Down Trend = Weak Bear
    
    # Define thresholds (can be adjusted based on historical distribution)
    vol_threshold = btc_vol.quantile(0.7)  # 70th percentile for high vol
    
    regimes = pd.DataFrame(index=btc_vol.index)
    regimes['Volatility'] = btc_vol
    regimes['Trend'] = btc_trend
    regimes['High_Vol'] = btc_vol > vol_threshold
    regimes['Up_Trend'] = btc_trend > 0
    
    # Create regime categories
    def assign_regime(row):
        if row['High_Vol'] and row['Up_Trend']:
            return 'Strong Bull'
        elif row['High_Vol'] and not row['Up_Trend']:
            return 'Strong Bear'
        elif not row['High_Vol'] and row['Up_Trend']:
            return 'Weak Bull'
        else:
            return 'Weak Bear'
    
    regimes['Regime'] = regimes.apply(assign_regime, axis=1)
    
    # Plot regime distribution
    plt.figure(figsize=(10, 6))
    regime_counts = regimes['Regime'].value_counts()
    plt.bar(regime_counts.index, regime_counts.values)
    plt.title('Market Regime Distribution')
    plt.ylabel('Number of Days')
    plt.tight_layout()
    plt.savefig("market_regime_distribution.png")
    plt.close()
    
    logger.info(f"Regime distribution:\n{regime_counts}")
    
    # Get full data for factor calculation
    full_data = load_coinbase_data(
        symbols=UNIVERSE,
        start_iso=start_dt,
        end_iso=end_dt,
        granularity="ONE_DAY"
    )
    
    if full_data is None or full_data.empty:
        logger.error("Failed to load full data for factor calculation")
        return
    
    close_prices = full_data['close']
    
    # Calculate factors 
    momentum = calculate_momentum(close_prices, window=60)
    mean_reversion = calculate_mean_reversion(close_prices, ma_window=50, z_window=20)
    
    # Calculate factor ranks
    mom_rank = cross_sectional_rank(momentum)
    mr_rank = cross_sectional_rank(mean_reversion)
    
    # Calculate future returns (5-day)
    future_returns = close_prices.groupby(level='symbol').pct_change(periods=5).shift(-5)
    
    # Combine factor data with regimes and future returns
    factor_data = pd.DataFrame({
        'Momentum': mom_rank,
        'Mean_Reversion': mr_rank,
        'Future_Return': future_returns
    }).dropna()
    
    # Add regime information to factor data
    factor_data_with_regime = pd.DataFrame()
    for date in factor_data.index.get_level_values('date').unique():
        if date in regimes.index:
            date_data = factor_data.xs(date, level='date')
            regime = regimes.loc[date, 'Regime']
            date_data['Regime'] = regime
            factor_data_with_regime = pd.concat([factor_data_with_regime, date_data])
    
    # Calculate IC by regime
    ic_by_regime = {}
    for regime in factor_data_with_regime['Regime'].unique():
        regime_data = factor_data_with_regime[factor_data_with_regime['Regime'] == regime]
        mom_ic = regime_data['Momentum'].corr(regime_data['Future_Return'])
        mr_ic = regime_data['Mean_Reversion'].corr(regime_data['Future_Return'])
        ic_by_regime[regime] = {'Momentum': mom_ic, 'Mean_Reversion': mr_ic}
    
    ic_regime_df = pd.DataFrame(ic_by_regime).T
    logger.info(f"Information Coefficient by Regime:\n{ic_regime_df}")
    
    # Plot IC by regime
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    x = np.arange(len(ic_regime_df.index))
    
    plt.bar(x - bar_width/2, ic_regime_df['Momentum'], bar_width, label='Momentum')
    plt.bar(x + bar_width/2, ic_regime_df['Mean_Reversion'], bar_width, label='Mean Reversion')
    
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)
    plt.xlabel('Market Regime')
    plt.ylabel('Information Coefficient')
    plt.title('Factor Effectiveness by Market Regime')
    plt.xticks(x, ic_regime_df.index)
    plt.legend()
    plt.tight_layout()
    plt.savefig("factor_effectiveness_by_regime.png")
    plt.close()
    
    return {
        'regimes': regimes,
        'ic_by_regime': ic_regime_df
    }

if __name__ == "__main__":
    logger.info("=== Mean Reversion Factor Evaluation ===")
    
    # Test mean reversion calculation
    mr_results = test_mean_reversion_calculation()
    
    # Analyze mean reversion effectiveness
    effectiveness = analyze_mean_reversion_effectiveness()
    
    # Analyze performance in different market regimes
    regime_analysis = analyze_market_regimes()
    
    logger.info("Evaluation complete. Check the generated plots for visual results.") 