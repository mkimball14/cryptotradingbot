import os
import sys
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Add the project root to the Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

# Import our modules
from crypto_factor_strategy.strategies.factors import calculate_mean_reversion, calculate_momentum
from crypto_factor_strategy.data.coinbase_data import load_price_data
from crypto_factor_strategy.backtest.portfolio import calculate_portfolio_weights, backtest_strategy
from crypto_factor_strategy.analysis.performance import calculate_performance_metrics
from crypto_factor_strategy.utils.logging_config import configure_logging
from crypto_factor_strategy.factors.mean_reversion import calculate_mean_reversion
from crypto_factor_strategy.factors.momentum import calculate_momentum
from crypto_factor_strategy.strategies.portfolio import combine_factors, calculate_portfolio_weights
from crypto_factor_strategy.analysis import calculate_factor_ic

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Define the universe
UNIVERSE = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'XRP-USD', 'DOGE-USD', 'MATIC-USD', 'DOT-USD', 'AVAX-USD', 'LINK-USD']

def test_mean_reversion_calculation(ma_windows=[20, 50, 100], z_windows=[10, 20, 30]):
    """
    Test the mean reversion calculation with different moving average and z-score window sizes.
    Plot the results and log insights.
    """
    logger.info("Starting mean reversion calculation test")
    
    # Load data
    start_date = "2023-01-01"
    end_date = "2023-03-01"
    
    try:
        price_data = load_price_data(UNIVERSE, start_date, end_date)
        
        if price_data is None or price_data.empty:
            logger.error("Failed to load price data")
            return
            
        # Ensure the index is correctly formatted as MultiIndex
        if not isinstance(price_data.index, pd.MultiIndex):
            logger.info("Converting price data to MultiIndex")
            # First reset the index to get date and symbol as columns
            if 'date' not in price_data.columns and 'symbol' not in price_data.columns:
                logger.info("Adding date and symbol as explicit columns")
                price_data = price_data.reset_index()
                
            # Convert to MultiIndex
            price_data = price_data.set_index(['date', 'symbol'])
            
        logger.info(f"Data shape: {price_data.shape}")
        logger.info(f"Data index: {price_data.index.names}")
        
        # Plot the results for different window sizes
        plt.figure(figsize=(15, 10))
        plot_count = 0
        
        # Get the first few symbols for plotting
        plot_symbols = UNIVERSE[:5]  # Use the first 5 symbols
        
        for ma_window in ma_windows:
            for z_window in z_windows:
                plot_count += 1
                plt.subplot(len(ma_windows), len(z_windows), plot_count)
                
                # Calculate mean reversion
                mean_reversion = calculate_mean_reversion(
                    price_data['close'], 
                    ma_window=ma_window, 
                    z_window=z_window
                )
                
                if mean_reversion is None:
                    logger.error(f"Failed to calculate mean reversion with ma_window={ma_window}, z_window={z_window}")
                    continue
                
                # Plot only the first few symbols for clarity
                for symbol in plot_symbols:
                    try:
                        # Use xs to extract data for a specific symbol
                        symbol_data = mean_reversion.xs(symbol, level='symbol')
                        plt.plot(symbol_data.index, symbol_data.values, label=symbol)
                    except KeyError:
                        logger.warning(f"Symbol {symbol} not found in mean reversion data")
                
                plt.title(f"MA Window: {ma_window}, Z-score Window: {z_window}")
                plt.grid(True)
                
                # Only add legend to the first subplot to save space
                if plot_count == 1:
                    plt.legend(loc='best')
                
                # Log statistics
                logger.info(f"Mean reversion stats (MA: {ma_window}, Z: {z_window}):")
                logger.info(f"  Mean: {mean_reversion.mean():.4f}")
                logger.info(f"  Std: {mean_reversion.std():.4f}")
                logger.info(f"  Min: {mean_reversion.min():.4f}")
                logger.info(f"  Max: {mean_reversion.max():.4f}")
        
        plt.tight_layout()
        plt.savefig("mean_reversion_test.png")
        logger.info("Saved mean reversion test plot to mean_reversion_test.png")
        plt.close()
        
    except Exception as e:
        logger.error(f"Error in test_mean_reversion_calculation: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

def analyze_mean_reversion_effectiveness():
    """
    Analyze the effectiveness of the mean reversion factor by comparing 
    to the momentum factor over a 2-year period.
    """
    logger.info("Starting mean reversion effectiveness analysis")
    
    # Load data for a 2-year period
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    
    try:
        price_data = load_price_data(UNIVERSE, start_date, end_date)
        
        if price_data is None or price_data.empty:
            logger.error("Failed to load price data")
            return
            
        # Ensure the index is correctly formatted as MultiIndex
        if not isinstance(price_data.index, pd.MultiIndex):
            logger.info("Converting price data to MultiIndex")
            # First reset the index to get date and symbol as columns
            if 'date' not in price_data.columns and 'symbol' not in price_data.columns:
                logger.info("Adding date and symbol as explicit columns")
                price_data = price_data.reset_index()
                
            # Convert to MultiIndex
            price_data = price_data.set_index(['date', 'symbol'])
            
        # Calculate factors
        mean_reversion = calculate_mean_reversion(price_data['close'], ma_window=50, z_window=20)
        momentum = calculate_momentum(price_data['close'], window=20)
        
        if mean_reversion is None or momentum is None:
            logger.error("Failed to calculate one or more factors")
            return
        
        # Create a MultiIndex DataFrame to store both factors
        # First, ensure both factors have the same index
        common_index = mean_reversion.index.intersection(momentum.index)
        
        mean_reversion = mean_reversion.reindex(common_index)
        momentum = momentum.reindex(common_index)
        
        # Create DataFrame with both factors
        factors_df = pd.DataFrame({
            'mean_reversion': mean_reversion,
            'momentum': momentum
        }, index=common_index)
        
        # Calculate factor ranks (higher is better)
        # For mean reversion, higher z-score means more oversold, so we want to rank it in reverse
        factors_df['mean_reversion_rank'] = factors_df.groupby(level='date')['mean_reversion'].rank(ascending=False)
        factors_df['momentum_rank'] = factors_df.groupby(level='date')['momentum'].rank(ascending=True)
        
        # Calculate correlation between factors
        correlation = factors_df.groupby(level='date').apply(
            lambda x: x['mean_reversion'].corr(x['momentum'])
        )
        
        logger.info(f"Average correlation between mean reversion and momentum: {correlation.mean():.4f}")
        
        # Plot the correlation over time
        plt.figure(figsize=(12, 6))
        correlation.plot()
        plt.title('Correlation between Mean Reversion and Momentum Factors')
        plt.grid(True)
        plt.axhline(y=0, color='r', linestyle='-')
        plt.savefig("factor_correlation.png")
        logger.info("Saved factor correlation plot to factor_correlation.png")
        plt.close()
        
        # Calculate Information Coefficient (IC) for each factor
        # Get forward returns (1-day ahead)
        forward_returns = price_data.groupby(level='symbol')['close'].pct_change(periods=1).shift(-1)
        
        # Align forward returns with factors
        forward_returns = forward_returns.reindex(common_index)
        
        # Calculate IC (correlation between factor and future returns)
        ic_mean_reversion = factors_df.groupby(level='date').apply(
            lambda x: x['mean_reversion'].corr(forward_returns.loc[x.index])
        )
        
        ic_momentum = factors_df.groupby(level='date').apply(
            lambda x: x['momentum'].corr(forward_returns.loc[x.index])
        )
        
        logger.info(f"Average IC for mean reversion: {ic_mean_reversion.mean():.4f}")
        logger.info(f"Average IC for momentum: {ic_momentum.mean():.4f}")
        
        # Plot IC comparison
        plt.figure(figsize=(12, 6))
        ic_mean_reversion.plot(label='Mean Reversion IC')
        ic_momentum.plot(label='Momentum IC')
        plt.title('Information Coefficient Comparison')
        plt.grid(True)
        plt.axhline(y=0, color='r', linestyle='-')
        plt.legend()
        plt.savefig("factor_ic_comparison.png")
        logger.info("Saved factor IC comparison plot to factor_ic_comparison.png")
        plt.close()
        
        # Backtest strategies based on individual factors
        # Mean Reversion strategy
        mean_reversion_weights = calculate_portfolio_weights(
            factor_data={
                'mean_reversion': mean_reversion
            },
            factor_weights={'mean_reversion': 1.0},
            universe=UNIVERSE
        )
        
        # Momentum strategy
        momentum_weights = calculate_portfolio_weights(
            factor_data={
                'momentum': momentum
            },
            factor_weights={'momentum': 1.0},
            universe=UNIVERSE
        )
        
        # Backtest both strategies
        mean_reversion_results = backtest_strategy(
            price_data['close'], 
            mean_reversion_weights,
            trade_fee=0.0015  # 15 bps fee
        )
        
        momentum_results = backtest_strategy(
            price_data['close'], 
            momentum_weights,
            trade_fee=0.0015  # 15 bps fee
        )
        
        # Calculate performance metrics
        mean_reversion_metrics = calculate_performance_metrics(mean_reversion_results)
        momentum_metrics = calculate_performance_metrics(momentum_results)
        
        # Print and log performance metrics
        logger.info("Mean Reversion Strategy Performance:")
        for metric, value in mean_reversion_metrics.items():
            logger.info(f"  {metric}: {value:.4f}")
            
        logger.info("Momentum Strategy Performance:")
        for metric, value in momentum_metrics.items():
            logger.info(f"  {metric}: {value:.4f}")
            
        # Create performance comparison DataFrame
        performance_df = pd.DataFrame({
            'Mean Reversion': mean_reversion_metrics,
            'Momentum': momentum_metrics
        })
        
        # Save performance metrics
        performance_df.to_csv("factor_performance_metrics.csv")
        logger.info("Saved factor performance metrics to factor_performance_metrics.csv")
        
        # Plot strategy equity curves
        plt.figure(figsize=(12, 6))
        mean_reversion_results['cum_return'].plot(label='Mean Reversion')
        momentum_results['cum_return'].plot(label='Momentum')
        plt.title('Strategy Performance Comparison')
        plt.grid(True)
        plt.legend()
        plt.savefig("factor_performance_comparison.png")
        logger.info("Saved factor performance comparison plot to factor_performance_comparison.png")
        plt.close()
        
    except Exception as e:
        logger.error(f"Error in analyze_mean_reversion_effectiveness: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

def analyze_market_regimes():
    """
    Analyze how mean reversion and momentum factors perform across different market regimes.
    """
    logger.info("Starting market regime analysis")
    
    # Load data for a 2-year period
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    
    try:
        price_data = load_price_data(UNIVERSE, start_date, end_date)
        
        if price_data is None or price_data.empty:
            logger.error("Failed to load price data")
            return
            
        # Ensure the index is correctly formatted as MultiIndex
        if not isinstance(price_data.index, pd.MultiIndex):
            logger.info("Converting price data to MultiIndex")
            # First reset the index to get date and symbol as columns
            if 'date' not in price_data.columns and 'symbol' not in price_data.columns:
                logger.info("Adding date and symbol as explicit columns")
                price_data = price_data.reset_index()
                
            # Convert to MultiIndex
            price_data = price_data.set_index(['date', 'symbol'])
            
        # Use BTC as proxy for market conditions
        btc_price = price_data.xs('BTC-USD', level='symbol')['close']
        
        # Calculate market state factors
        btc_returns = btc_price.pct_change(20)  # 20-day returns
        btc_volatility = btc_price.pct_change().rolling(20).std()  # 20-day volatility
        
        # Define market regimes
        # 1. High volatility, up trend
        # 2. High volatility, down trend
        # 3. Low volatility, up trend
        # 4. Low volatility, down trend
        
        # Determine thresholds based on median values
        vol_threshold = btc_volatility.median()
        ret_threshold = 0  # 0% return as threshold between up/down trend
        
        # Classify market regimes
        market_regimes = pd.DataFrame(index=btc_returns.index)
        market_regimes['volatility'] = np.where(btc_volatility > vol_threshold, 'high', 'low')
        market_regimes['trend'] = np.where(btc_returns > ret_threshold, 'up', 'down')
        market_regimes['regime'] = market_regimes['volatility'] + '_' + market_regimes['trend']
        
        # Calculate factors
        mean_reversion = calculate_mean_reversion(price_data['close'], ma_window=50, z_window=20)
        momentum = calculate_momentum(price_data['close'], window=20)
        
        if mean_reversion is None or momentum is None:
            logger.error("Failed to calculate one or more factors")
            return
        
        # Get forward returns
        forward_returns = price_data.groupby(level='symbol')['close'].pct_change(periods=1).shift(-1)
        
        # Calculate IC for each regime
        ic_by_regime = {'mean_reversion': {}, 'momentum': {}}
        
        for regime in market_regimes['regime'].unique():
            # Get dates for this regime
            regime_dates = market_regimes[market_regimes['regime'] == regime].index
            
            # Calculate IC for mean reversion in this regime
            mean_rev_data = []
            momentum_data = []
            returns_data = []
            
            for date in regime_dates:
                # Get data for this date
                try:
                    date_idx = pd.IndexSlice[:, date]
                    
                    # Handle case where data might not exist for some dates
                    if date not in mean_reversion.index.get_level_values('date').unique():
                        continue
                        
                    mean_rev_slice = mean_reversion.xs(date, level='date')
                    momentum_slice = momentum.xs(date, level='date')
                    returns_slice = forward_returns.xs(date, level='date')
                    
                    # Ensure they have same index (symbols)
                    common_symbols = mean_rev_slice.index.intersection(returns_slice.index)
                    common_symbols = common_symbols.intersection(momentum_slice.index)
                    
                    if len(common_symbols) > 0:
                        mean_rev_data.extend(mean_rev_slice.loc[common_symbols].values)
                        momentum_data.extend(momentum_slice.loc[common_symbols].values)
                        returns_data.extend(returns_slice.loc[common_symbols].values)
                except Exception as e:
                    logger.warning(f"Error processing date {date} for regime {regime}: {e}")
            
            # Calculate correlation if we have enough data
            if len(mean_rev_data) > 5:  # Require at least 5 data points
                ic_mean_rev = np.corrcoef(mean_rev_data, returns_data)[0, 1]
                ic_momentum = np.corrcoef(momentum_data, returns_data)[0, 1]
                
                ic_by_regime['mean_reversion'][regime] = ic_mean_rev
                ic_by_regime['momentum'][regime] = ic_momentum
        
        # Create DataFrame for IC by regime
        ic_df = pd.DataFrame(ic_by_regime)
        
        # Log the results
        logger.info("Information Coefficient by Market Regime:")
        logger.info(ic_df)
        
        # Save results
        ic_df.to_csv("ic_by_market_regime.csv")
        logger.info("Saved IC by market regime to ic_by_market_regime.csv")
        
        # Plot IC by regime
        plt.figure(figsize=(12, 6))
        ic_df.plot(kind='bar')
        plt.title('IC by Market Regime')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("ic_by_market_regime.png")
        logger.info("Saved IC by market regime plot to ic_by_market_regime.png")
        plt.close()
        
    except Exception as e:
        logger.error(f"Error in analyze_market_regimes: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    logger.info("Starting mean reversion factor evaluation")
    
    # Test mean reversion calculation
    test_mean_reversion_calculation()
    
    # Analyze mean reversion effectiveness
    analyze_mean_reversion_effectiveness()
    
    # Analyze performance across market regimes
    analyze_market_regimes()
    
    logger.info("Completed mean reversion factor evaluation") 