#!/usr/bin/env python3
"""
Cryptocurrency Factor-Based Quant Strategy
------------------------------------------
Main script that orchestrates the full strategy pipeline:
1. Data acquisition from Coinbase
2. Factor calculation (momentum, volatility, relative strength)
3. Portfolio construction
4. Backtest simulation
5. Performance analysis
"""

import os
import logging
import pandas as pd
import numpy as np
import vectorbtpro as vbt
import matplotlib.pyplot as plt
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crypto_factor_strategy.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import strategy modules
from strategies.data_utils import load_coinbase_data
from strategies.factors import (
    UNIVERSE,
    calculate_momentum, 
    calculate_volatility, 
    calculate_custom_factor,
    calculate_relative_strength,
    calculate_mean_reversion,  # New mean reversion factor
    cross_sectional_rank, 
    cross_sectional_zscore
)
from strategies.portfolio import (
    calculate_top_n_weights,
    calculate_long_short_quintile_weights,
    calculate_volatility_targeted_weights  # New volatility targeting
)
from strategies.backtester import (
    run_factor_backtest,
    analyze_portfolio_performance
)

def print_index_info(dataframe, name):
    """Helper function to print index structure information"""
    print(f"\n--- {name} index info ---")
    if isinstance(dataframe, pd.DataFrame) or isinstance(dataframe, pd.Series):
        if isinstance(dataframe.index, pd.MultiIndex):
            print(f"MultiIndex with levels: {dataframe.index.names}")
            print(f"Level values: {[name for name in dataframe.index.names]}")
            print(f"Shape: {dataframe.shape}")
            print(f"Sample index (first 2 entries):")
            try:
                print(dataframe.index[:2])
            except:
                print("Could not print sample index")
        else:
            print(f"Single-level index with name: {dataframe.index.name}")
            print(f"Shape: {dataframe.shape}")
    else:
        print(f"Not a DataFrame or Series: {type(dataframe)}")

def run_strategy(
    universe=None,
    start_date='2022-01-01T00:00:00Z',
    end_date='2023-12-31T00:00:00Z',
    granularity='ONE_DAY',
    momentum_window=63,   # ~3 months
    volatility_window=21, # ~1 month
    rel_strength_window=30, # ~1 month
    mean_reversion_window=50,  # ~2 months (new parameter)
    top_n=3,              # Number of assets to include
    max_weight=0.5,       # Maximum weight per asset
    init_cash=100000,
    fees=0.001,           # 0.1%
    slippage=0.0005,      # 0.05%
    factor_weights=None,  # Optional dict of factor weights
    use_volatility_targeting=False,  # Whether to use volatility targeting
    target_volatility=0.15,  # Target annualized volatility (15%)
    max_leverage=1.5,     # Maximum leverage for volatility targeting
    save_results=True
):
    """Run the complete factor-based strategy pipeline.
    
    Args:
        universe: List of symbols to include
        start_date: Start date in ISO format
        end_date: End date in ISO format
        granularity: Data granularity (ONE_DAY, ONE_HOUR, etc.)
        momentum_window: Lookback period for momentum factor
        volatility_window: Lookback period for volatility factor
        rel_strength_window: Lookback period for relative strength factor
        mean_reversion_window: Lookback period for mean reversion factor
        top_n: Number of assets to include in portfolio
        max_weight: Maximum weight per asset
        init_cash: Initial capital
        fees: Trading fee percentage
        slippage: Slippage percentage
        factor_weights: Dict with weights for each factor
        use_volatility_targeting: Whether to target specific portfolio volatility
        target_volatility: Target annualized volatility (decimal form)
        max_leverage: Maximum allowed portfolio leverage
        save_results: Whether to save results to disk
        
    Returns:
        dict: Strategy results containing the portfolio object, performance metrics,
              weights, factors, and other data. If strategy fails, returns a dict
              with None for 'portfolio' and zeros for all metrics.
    """
    
    # Set default universe if not provided
    if universe is None:
        universe = UNIVERSE
    
    # Set default factor weights if not provided
    if factor_weights is None:
        factor_weights = {
            'momentum': 0.30,
            'volatility': 0.20,
            'rel_strength': 0.25,
            'mean_reversion': 0.25  # Add weight for mean reversion
        }
    
    # Default metrics in case of failure (needed for optimizer)
    default_metrics = {
        'Sharpe Ratio': 0.0,
        'Sortino Ratio': 0.0,
        'Max Drawdown (%)': -100.0,
        'Total Return (%)': 0.0,
        'Annual Return (%)': 0.0,
        'Annual Volatility (%)': 100.0,
        'Calmar Ratio': 0.0,
        'Win Rate (%)': 0.0
    }
        
    try:
        # 1. Load Data
        logger.info(f"Starting strategy run from {start_date} to {end_date}")
        logger.info(f"Universe: {universe}")
        logger.info(f"Parameters: momentum_window={momentum_window}, "
                   f"volatility_window={volatility_window}, "
                   f"rel_strength_window={rel_strength_window}, "
                   f"mean_reversion_window={mean_reversion_window}, "
                   f"top_n={top_n}")
        logger.info(f"Factor weights: {factor_weights}")
        if use_volatility_targeting:
            logger.info(f"Using volatility targeting with target vol={target_volatility*100}%, max_leverage={max_leverage}")
        
        ohlcv_data = load_coinbase_data(
            symbols=universe,
            start_iso=start_date,
            end_iso=end_date,
            granularity=granularity
        )
        
        if ohlcv_data is None or ohlcv_data.empty:
            logger.error("Failed to load data. Exiting.")
            return {
                'portfolio': None,
                'metrics': default_metrics,
                'momentum_window': momentum_window,
                'volatility_window': volatility_window,
                'rel_strength_window': rel_strength_window,
                'mean_reversion_window': mean_reversion_window,
                'top_n': top_n,
                'factor_weights': factor_weights
            }
            
        logger.info(f"Data loaded successfully: {ohlcv_data.shape}")
        print_index_info(ohlcv_data, "ohlcv_data")
        
        # Fix index naming if the first level is None
        if isinstance(ohlcv_data.index, pd.MultiIndex) and ohlcv_data.index.names[0] is None:
            ohlcv_data.index.names = ['date', 'symbol']
            logger.info("Renamed index levels to ['date', 'symbol']")
            print_index_info(ohlcv_data, "ohlcv_data (after renaming)")
            
        # Extract close prices
        close_prices = ohlcv_data['close']
        print_index_info(close_prices, "close_prices")
        
        # 2. Calculate Factors
        logger.info("Calculating factors...")
        
        # Calculate momentum
        momentum = calculate_momentum(close_prices, window=momentum_window)
        
        # Calculate volatility (lower is better)
        volatility = calculate_volatility(close_prices, window=volatility_window)
        
        # Calculate relative strength
        rel_strength = calculate_relative_strength(close_prices, window=rel_strength_window, benchmark_symbol='BTC-USD')
        
        # Calculate mean reversion
        mean_reversion = calculate_mean_reversion(close_prices, ma_window=mean_reversion_window, z_window=max(15, int(mean_reversion_window/3)))
        
        # Combine factors into a DataFrame
        factor_data = pd.DataFrame({
            'momentum': momentum,
            'volatility': volatility,
            'rel_strength': rel_strength,
            'mean_reversion': mean_reversion
        })
        print_index_info(factor_data, "factor_data")
        
        # Ensure factor_data has date as first level
        if isinstance(factor_data.index, pd.MultiIndex) and 'date' in factor_data.index.names and 'symbol' in factor_data.index.names:
            if factor_data.index.names[0] != 'date':
                factor_data = factor_data.reorder_levels(['date', 'symbol']).sort_index()
                logger.info("Reordered factor_data index levels to ['date', 'symbol']")
                print_index_info(factor_data, "factor_data (after reordering)")
        
        # Drop rows with NaNs in factors
        original_count = len(factor_data)
        factor_data = factor_data.dropna()
        logger.info(f"Dropped {original_count - len(factor_data)} rows with NaNs in factors.")
        
        if factor_data.empty:
            logger.error("No valid factor data remaining after dropping NaNs. Exiting.")
            return {
                'portfolio': None,
                'metrics': default_metrics,
                'momentum_window': momentum_window,
                'volatility_window': volatility_window,
                'rel_strength_window': rel_strength_window,
                'mean_reversion_window': mean_reversion_window,
                'top_n': top_n,
                'factor_weights': factor_weights
            }
        
        # 3. Process Factors
        logger.info("Processing factors (ranking & combining)...")
        
        # Create a copy of factor_data to process
        factor_data_processed = factor_data.copy()
        
        # Make sure the index levels are named properly
        if isinstance(factor_data_processed.index, pd.MultiIndex):
            # Fix the level names if not already correct
            if factor_data_processed.index.names[0] is None:
                factor_data_processed.index.names = ['date', 'symbol']
                logger.info("Renamed index levels to ['date', 'symbol']")
                print_index_info(factor_data_processed, "factor_data_processed (after renaming)")
        
        # Add negative volatility (lower volatility is better)
        factor_data_processed['-volatility'] = -factor_data_processed['volatility']
        
        # Rank factors cross-sectionally
        processed_factors = pd.DataFrame(index=factor_data_processed.index)
        
        # Get first level name for groupby (should be 'date')
        date_level = factor_data_processed.index.names[0]
        
        # Rank using the appropriate level name
        processed_factors['momentum_rank'] = factor_data_processed.groupby(level=date_level)['momentum'].rank(method='first', pct=True)
        # Invert volatility for ranking (lower volatility is better)
        processed_factors['volatility_rank'] = factor_data_processed.groupby(level=date_level)['-volatility'].rank(method='first', pct=True)
        # Rank relative strength
        processed_factors['rel_strength_rank'] = factor_data_processed.groupby(level=date_level)['rel_strength'].rank(method='first', pct=True)
        # Rank mean reversion
        processed_factors['mean_reversion_rank'] = factor_data_processed.groupby(level=date_level)['mean_reversion'].rank(method='first', pct=True)
        
        print_index_info(processed_factors, "processed_factors")
        
        # Combine factors with specified weights
        # First, ensure we only use factors that exist in processed_factors
        valid_factors = {}
        for factor, weight in factor_weights.items():
            factor_col = f"{factor}_rank"
            if factor_col in processed_factors.columns:
                valid_factors[factor_col] = weight
        
        # Normalize weights to sum to 1
        if valid_factors:
            total_weight = sum(valid_factors.values())
            valid_factors = {k: v/total_weight for k, v in valid_factors.items()}
            
            # Calculate weighted average
            combined_score = pd.Series(0.0, index=processed_factors.index)
            for factor_col, weight in valid_factors.items():
                combined_score += processed_factors[factor_col] * weight
        else:
            # Fallback to equal weighting if no valid factors found
            logger.warning("No valid factors found in factor_weights. Using equal weights.")
            num_factors = len(processed_factors.columns)
            combined_score = processed_factors.sum(axis=1) / num_factors
        
        print_index_info(combined_score, "combined_score")
        
        # 4. Calculate Target Weights
        logger.info(f"Calculating portfolio weights (top {top_n} assets, max weight {max_weight})...")
        
        # Ensure combined_score has proper index names
        if isinstance(combined_score.index, pd.MultiIndex) and combined_score.index.names[0] is None:
            combined_score.index.names = ['date', 'symbol']
            logger.info("Renamed combined_score index levels to ['date', 'symbol']")
            print_index_info(combined_score, "combined_score (after renaming)")
        
        # Calculate base weights
        target_weights = calculate_top_n_weights(
            scores=combined_score, 
            n=top_n, 
            max_weight_per_asset=max_weight
        )
        
        if target_weights is None:
            logger.error("Failed to calculate target weights. Exiting.")
            return {
                'portfolio': None,
                'metrics': default_metrics,
                'momentum_window': momentum_window,
                'volatility_window': volatility_window,
                'rel_strength_window': rel_strength_window,
                'mean_reversion_window': mean_reversion_window,
                'top_n': top_n,
                'factor_weights': factor_weights
            }
            
        print_index_info(target_weights, "target_weights")
        
        # Apply volatility targeting if enabled
        if use_volatility_targeting:
            logger.info(f"Applying volatility targeting (target vol: {target_volatility*100}%)...")
            
            # Calculate daily returns (needed for volatility calculation)
            returns = close_prices.groupby(level='symbol').pct_change()
            
            # Calculate volatility-targeted weights
            vol_targeted_weights = calculate_volatility_targeted_weights(
                weights=target_weights,
                returns=returns,
                target_vol=target_volatility,
                max_leverage=max_leverage,
                cov_window=63,  # ~3 months of data for covariance
                vol_cap=0.5     # Cap predicted vol to avoid extreme leverage
            )
            
            if vol_targeted_weights is not None:
                target_weights = vol_targeted_weights
                logger.info("Volatility targeting applied successfully.")
            else:
                logger.warning("Failed to apply volatility targeting. Using base weights.")
        
        
        # 5. Run Backtest
        logger.info("Running backtest simulation...")
        
        portfolio = run_factor_backtest(
            close_prices=close_prices,
            target_weights=target_weights,
            init_cash=init_cash,
            fees=fees,
            slippage=slippage,
            freq='D' if granularity == 'ONE_DAY' else '1H'  # Simplified mapping
        )
        
        if portfolio is None:
            logger.error("Backtest simulation failed. Exiting.")
            return {
                'portfolio': None,
                'metrics': default_metrics,
                'momentum_window': momentum_window,
                'volatility_window': volatility_window,
                'rel_strength_window': rel_strength_window,
                'mean_reversion_window': mean_reversion_window,
                'top_n': top_n,
                'factor_weights': factor_weights
            }
            
        # 6. Analyze Results
        logger.info("Analyzing backtest results...")
        
        # Use BTC-USD as benchmark (if available in the data)
        benchmark_returns = None
        if 'BTC-USD' in close_prices.index.get_level_values('symbol'):
            btc_data = close_prices.xs('BTC-USD', level='symbol')
            benchmark_returns = btc_data.pct_change().dropna()
            logger.info("Using BTC-USD as benchmark.")
        
        # Calculate and display performance metrics
        metrics = analyze_portfolio_performance(portfolio, benchmark_returns)
        
        # 7. Save Results (if requested)
        if save_results:
            logger.info("Saving results...")
            
            # Create unique timestamp for this run
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_dir = f"results_{timestamp}"
            os.makedirs(results_dir, exist_ok=True)
            
            # Save report
            with open(f"{results_dir}/report.txt", "w") as f:
                f.write(f"Crypto Factor Strategy Report\n")
                f.write(f"============================\n\n")
                f.write(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Period: {start_date} to {end_date}\n")
                f.write(f"Universe: {universe}\n")
                f.write(f"Top N: {top_n}\n")
                f.write(f"Max Weight: {max_weight}\n\n")
                f.write(f"Parameters:\n")
                f.write(f"- Momentum Window: {momentum_window}\n")
                f.write(f"- Volatility Window: {volatility_window}\n")
                f.write(f"- Relative Strength Window: {rel_strength_window}\n")
                f.write(f"- Mean Reversion Window: {mean_reversion_window}\n")
                f.write(f"- Factor Weights: {factor_weights}\n")
                if use_volatility_targeting:
                    f.write(f"- Volatility Targeting: Enabled\n")
                    f.write(f"- Target Volatility: {target_volatility*100}%\n")
                    f.write(f"- Max Leverage: {max_leverage}\n")
                else:
                    f.write(f"- Volatility Targeting: Disabled\n")
                f.write(f"\nPerformance Metrics:\n")
                f.write(f"-----------------\n")
                for metric, value in metrics.items():
                    f.write(f"{metric}: {value}\n")
            
            # Generate and save equity curve plot
            try:
                fig = portfolio.plot()
                fig.write_image(f"{results_dir}/equity_curve.png")
                logger.info(f"Results saved to {results_dir} directory")
            except Exception as e:
                logger.error(f"Error saving plot: {e}")
        
        # Add strategy parameters to metrics
        result_metrics = {
            **metrics,
            'momentum_window': momentum_window,
            'volatility_window': volatility_window,
            'rel_strength_window': rel_strength_window,
            'mean_reversion_window': mean_reversion_window,
            'top_n': top_n
        }
        
        return {
            'portfolio': portfolio,
            'metrics': result_metrics,
            'weights': target_weights,
            'factors': factor_data,
            'processed_factors': processed_factors,
            'combined_score': combined_score
        }
        
    except Exception as e:
        logger.error(f"Error running strategy: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Return a result dict with default metrics and the param values
        # This helps the optimizer track the failed run
        return {
            'portfolio': None,
            'metrics': {
                **default_metrics,
                'momentum_window': momentum_window,
                'volatility_window': volatility_window,
                'rel_strength_window': rel_strength_window,
                'mean_reversion_window': mean_reversion_window,
                'top_n': top_n,
                'factor_weights': factor_weights,
                'error': str(e)
            }
        }


if __name__ == "__main__":
    # Run the strategy with default settings
    print("\n=== Crypto Factor Strategy ===\n")
    
    # Use reduced universe for quicker testing
    test_universe = UNIVERSE[:5]  # Use first 5 symbols
    
    # Use recent 1-year period for quicker testing
    test_start_date = '2023-01-01T00:00:00Z'
    test_end_date = '2023-12-31T00:00:00Z'
    
    # Try different factor weights, now including mean reversion
    factor_weights = {
        'momentum': 0.3,
        'volatility': 0.2,
        'rel_strength': 0.25,
        'mean_reversion': 0.25  # Add mean reversion with 25% weight
    }
    
    results = run_strategy(
        universe=test_universe,
        start_date=test_start_date,
        end_date=test_end_date,
        top_n=2,  # Allocate to top 2 assets
        init_cash=100000,
        factor_weights=factor_weights,
        use_volatility_targeting=True,  # Enable volatility targeting
        target_volatility=0.15,  # Target 15% annualized volatility
        max_leverage=1.5,  # Allow up to 150% leverage
        save_results=True
    )
    
    if results and results['portfolio'] is not None:
        print("\nStrategy run completed successfully.")
        print("See the 'results_*' directory for detailed reports.")
        
        # Print key metrics
        print("\nPerformance Metrics:")
        metrics = results['metrics']
        print(f"Sharpe Ratio: {metrics.get('Sharpe Ratio', 'N/A')}")
        print(f"Total Return: {metrics.get('Total Return (%)', 'N/A')}%")
        print(f"Max Drawdown: {metrics.get('Max Drawdown (%)', 'N/A')}%")
        
        # Show equity curve plot (interactive session)
        try:
            results['portfolio'].plot().show()
        except:
            pass
        
        # Show final portfolio composition
        try:
            final_date = results['weights'].index.get_level_values('date').max()
            final_weights = results['weights'].xs(final_date, level='date')
            
            print("\nFinal Portfolio Allocation:")
            for symbol, weight in final_weights[final_weights > 0].items():
                print(f"  {symbol}: {weight*100:.2f}%")
        except Exception as e:
            print(f"Error displaying final weights: {e}")
    else:
        print("\nStrategy run failed. Check log for details.") 