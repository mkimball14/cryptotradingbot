#!/usr/bin/env python3
"""
Test script to evaluate the effectiveness of volatility targeting for risk management
using Yahoo Finance data
"""

import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import strategy modules - Use relative import syntax for the crypto_factor_strategy package
from strategies.data_utils import load_yahoo_finance_data  # Changed to use Yahoo Finance
from strategies.factors import (
    UNIVERSE,
    calculate_momentum,
    calculate_volatility,
    calculate_mean_reversion,
    cross_sectional_rank
)
from strategies.portfolio import (
    calculate_equal_weights,
    calculate_top_n_weights, 
    calculate_volatility_targeted_weights,
    predict_asset_volatility
)
from strategies.backtester import run_factor_backtest

# Define Yahoo Finance compatible universe
# Replace Coinbase symbols with Yahoo Finance equivalents if needed
YF_UNIVERSE = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'XRP-USD', 
               'DOGE-USD', 'MATIC-USD', 'DOT-USD', 'AVAX-USD', 'LINK-USD']

def test_volatility_prediction(volatility_methods=['rolling', 'ewm'], windows=[30, 60, 90]):
    """
    Test different volatility prediction methods and window sizes.
    
    Args:
        volatility_methods: List of methods to test
        windows: List of window sizes to test
    """
    logger.info("Testing volatility prediction methods...")
    
    # Load data for testing
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    
    ohlcv_data = load_yahoo_finance_data(
        symbols=YF_UNIVERSE,
        start_date=start_date,
        end_date=end_date,
        interval='1d'
    )
    
    if ohlcv_data is None or ohlcv_data.empty:
        logger.error("Failed to load data for volatility prediction testing")
        return
    
    close_prices = ohlcv_data['close']
    
    # Plot actual volatility for a sample asset (BTC-USD)
    btc_close = close_prices.xs('BTC-USD', level='symbol')
    btc_returns = btc_close.pct_change().dropna()
    
    # Calculate rolling realized volatility (annualized)
    realized_vol = btc_returns.rolling(window=30).std() * np.sqrt(365)
    
    # Calculate predicted volatility with different methods
    vol_predictions = {}
    for method in volatility_methods:
        for window in windows:
            logger.info(f"Calculating volatility with method={method}, window={window}")
            
            # Calculate for all assets first
            # First calculate returns from close prices
            returns = close_prices.pct_change().dropna()
            
            all_predictions = predict_asset_volatility(
                returns=returns,
                window=window,
                std_type=method
            )
            
            # Extract BTC for comparison
            try:
                btc_vol = all_predictions.xs('BTC-USD', level='symbol')
                vol_predictions[f"{method}_{window}"] = btc_vol
            except:
                logger.error(f"Could not extract BTC volatility for {method}_{window}")
    
    # Plot volatility predictions
    plt.figure(figsize=(12, 6))
    plt.plot(realized_vol.index, realized_vol, 'k-', label='Realized (30-day)', alpha=0.7)
    
    for label, vol in vol_predictions.items():
        plt.plot(vol.index, vol, label=f'Predicted ({label})')
    
    plt.title('BTC-USD Volatility: Realized vs Predicted')
    plt.xlabel('Date')
    plt.ylabel('Annualized Volatility')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("volatility_prediction_comparison.png")
    plt.close()
    
    # Calculate prediction errors
    errors = {}
    for label, vol in vol_predictions.items():
        # Align dates
        merged = pd.merge(
            realized_vol.rename('realized'),
            vol.rename('predicted'),
            left_index=True,
            right_index=True,
            how='inner'
        )
        
        if merged.empty:
            logger.warning(f"No overlapping data for {label}")
            continue
            
        # Calculate error metrics
        mae = np.mean(np.abs(merged['realized'] - merged['predicted']))
        rmse = np.sqrt(np.mean((merged['realized'] - merged['predicted'])**2))
        
        errors[label] = {
            'MAE': mae,
            'RMSE': rmse
        }
    
    # Print error metrics
    error_df = pd.DataFrame(errors).T
    logger.info(f"\nVolatility Prediction Errors:\n{error_df}")
    
    return {
        'realized': realized_vol,
        'predictions': vol_predictions,
        'errors': error_df
    }

def test_portfolio_volatility_targeting(target_vols=[0.2, 0.3, 0.4], max_leverages=[1.0, 1.5, 2.0]):
    """
    Test the performance of volatility targeting with different target levels and max leverage.
    
    Args:
        target_vols: List of target volatility levels to test
        max_leverages: List of maximum leverage values to test
    """
    logger.info("Testing portfolio volatility targeting...")
    
    # Load data for backtesting
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    
    ohlcv_data = load_yahoo_finance_data(
        symbols=YF_UNIVERSE,
        start_date=start_date,
        end_date=end_date,
        interval='1d'
    )
    
    if ohlcv_data is None or ohlcv_data.empty:
        logger.error("Failed to load data for volatility targeting testing")
        return
    
    close_prices = ohlcv_data['close']
    
    # Calculate momentum and mean reversion factors
    momentum = calculate_momentum(close_prices, window=60)
    mean_rev = calculate_mean_reversion(close_prices, ma_window=50, z_window=20)
    
    # Rank factors and combine with equal weights
    mom_rank = cross_sectional_rank(momentum)
    mr_rank = cross_sectional_rank(mean_rev)
    combined_rank = (mom_rank + mr_rank) / 2
    
    # Calculate base weights (top 3 assets)
    base_weights = calculate_top_n_weights(combined_rank, n=3)
    
    # Run baseline backtest (no volatility targeting)
    baseline_portfolio = run_factor_backtest(
        close_prices=close_prices,
        target_weights=base_weights,
        init_cash=100000,
        fees=0.001,
        slippage=0.0005
    )
    
    # Run backtests with different volatility targeting settings
    portfolios = {'Baseline': baseline_portfolio}
    
    for target_vol in target_vols:
        for max_leverage in max_leverages:
            logger.info(f"Testing target_vol={target_vol}, max_leverage={max_leverage}")
            
            # Calculate volatility-targeted weights
            vol_weights = calculate_volatility_targeted_weights(
                weights=base_weights,
                returns=close_prices.pct_change().dropna(),
                target_vol=target_vol,
                max_leverage=max_leverage,
                cov_window=60,
                vol_cap=0.6
            )
            
            # Run backtest
            portfolio = run_factor_backtest(
                close_prices=close_prices,
                target_weights=vol_weights,
                init_cash=100000,
                fees=0.001,
                slippage=0.0005
            )
            
            portfolio_name = f"Vol_{target_vol}_Lev_{max_leverage}"
            portfolios[portfolio_name] = portfolio
    
    # Analyze results
    equity_curves = {}
    metrics = {}
    
    for name, portfolio in portfolios.items():
        if portfolio is None:
            logger.warning(f"Portfolio {name} is None, skipping")
            continue
        
        # Access the equity curve based on the portfolio object type
        try:
            # According to VectorBT docs, value is the proper way to access equity curve
            if hasattr(portfolio, 'value'):
                equity = portfolio.value
            # Try other possible properties based on VectorBT documentation
            elif hasattr(portfolio, 'asset_value'):
                # Only call if it's a method, otherwise use as property
                if callable(getattr(portfolio, 'asset_value')):
                    equity = portfolio.asset_value()
                else:
                    equity = portfolio.asset_value
            elif hasattr(portfolio, 'equity_curve'):
                equity = portfolio.equity_curve
            elif hasattr(portfolio, 'cum_returns'):
                equity = portfolio.cum_returns
            else:
                # If none of the above work, try to access the stats and calculate equity
                logger.warning(f"Couldn't find equity curve directly. Trying to calculate from stats.")
                stats = portfolio.stats()
                # Print available attributes to help debug
                logger.info(f"Portfolio object has attributes: {dir(portfolio)}")
                logger.info(f"Stats keys: {list(stats.keys())}")
                
                # Last resort: reconstruct from initial value and returns if available
                if hasattr(portfolio, 'returns'):
                    returns = portfolio.returns
                    # In VectorBT, typical starting value is 100.0
                    equity = (1 + returns).cumprod() * 100.0
                else:
                    raise AttributeError("Couldn't find a way to access portfolio equity curve")
        except Exception as e:
            logger.error(f"Error accessing equity curve: {e}")
            raise
        
        equity_curves[name] = equity
        
        # Calculate metrics
        stats = portfolio.stats()
        metrics[name] = {
            'Total Return (%)': ((equity.iloc[-1] / equity.iloc[0]) - 1) * 100,
        }
        
        # Add more metrics based on what's available in the stats dictionary
        # Check for common metric keys with different naming patterns
        for key in stats:
            if 'annual' in key.lower() and 'return' in key.lower():
                metrics[name]['Annual Return (%)'] = stats[key]
            elif 'sharpe' in key.lower():
                metrics[name]['Sharpe Ratio'] = stats[key]
            elif 'max' in key.lower() and 'drawdown' in key.lower():
                metrics[name]['Max Drawdown (%)'] = stats[key]
            elif 'volatility' in key.lower() or 'std' in key.lower():
                metrics[name]['Volatility (%)'] = stats[key]
                
        # Ensure all metrics exist (use reasonable defaults if not found)
        if 'Annual Return (%)' not in metrics[name]:
            # Calculate annualized return manually if not in stats
            daily_returns = equity.pct_change().dropna()
            ann_return = ((1 + daily_returns.mean()) ** 252 - 1) * 100
            metrics[name]['Annual Return (%)'] = ann_return
            
        if 'Sharpe Ratio' not in metrics[name]:
            metrics[name]['Sharpe Ratio'] = 0.0
            
        if 'Max Drawdown (%)' not in metrics[name]:
            # Calculate max drawdown manually
            peak = equity.expanding(min_periods=1).max()
            drawdown = ((equity / peak) - 1) * 100
            metrics[name]['Max Drawdown (%)'] = drawdown.min()
            
        if 'Volatility (%)' not in metrics[name]:
            # Calculate annualized volatility manually
            daily_returns = equity.pct_change().dropna()
            ann_vol = daily_returns.std() * np.sqrt(252) * 100
            metrics[name]['Volatility (%)'] = ann_vol
    
    # Plot equity curves
    plt.figure(figsize=(12, 6))
    
    for name, equity in equity_curves.items():
        if name == 'Baseline':
            plt.plot(equity.index, equity, 'k-', label=name, linewidth=2)
        else:
            plt.plot(equity.index, equity, label=name)
    
    plt.title('Performance Comparison: Volatility Targeting')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("volatility_targeting_equity_curves.png")
    plt.close()
    
    # Plot actual volatility
    realized_vols = {}
    window = 30  # 30-day rolling window for realized volatility
    
    for name, equity in equity_curves.items():
        returns = equity.pct_change().dropna()
        vol = returns.rolling(window=window).std() * np.sqrt(365)  # Annualize
        realized_vols[name] = vol
    
    plt.figure(figsize=(12, 6))
    
    for name, vol in realized_vols.items():
        if name == 'Baseline':
            plt.plot(vol.index, vol, 'k-', label=name, linewidth=2)
        else:
            plt.plot(vol.index, vol, label=name)
    
    plt.title(f'Realized {window}-day Volatility Comparison')
    plt.xlabel('Date')
    plt.ylabel('Annualized Volatility')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("volatility_targeting_realized_vols.png")
    plt.close()
    
    # Create metrics DataFrame
    metrics_df = pd.DataFrame(metrics)
    logger.info(f"\nPerformance Comparison:\n{metrics_df}")
    
    # Save metrics to file
    metrics_df.to_csv("volatility_targeting_metrics.csv")
    
    # Additional analysis: Calculate average leverage over time
    leverage_df = pd.DataFrame(index=base_weights.index.get_level_values('date').unique())
    
    for name, portfolio in portfolios.items():
        if portfolio is None or name == 'Baseline':
            continue
            
        # Check if weights is a method or property, or access from results
        try:
            if hasattr(portfolio, 'weights'):
                if callable(getattr(portfolio, 'weights')):
                    weights = portfolio.weights()
                else:
                    weights = portfolio.weights
            elif hasattr(portfolio, 'results') and hasattr(portfolio.results, 'weights'):
                weights = portfolio.results.weights
            elif hasattr(portfolio, 'holdings'):
                weights = portfolio.holdings
            else:
                logger.warning(f"Could not find weights for portfolio {name}, skipping leverage calculation")
                continue
                
            # Sum absolute weights per day to get leverage
            # Make sure weights has a correct index
            if hasattr(weights, 'groupby'):
                daily_leverage = weights.groupby('date').apply(lambda x: np.sum(np.abs(x)))
                leverage_df[name] = daily_leverage
            else:
                logger.warning(f"Weights format for {name} not compatible with groupby")
        except Exception as e:
            logger.warning(f"Error calculating leverage for portfolio {name}: {e}")
            continue
    
    # Plot leverage over time
    if not leverage_df.empty:
        plt.figure(figsize=(12, 6))
        
        for name in leverage_df.columns:
            plt.plot(leverage_df.index, leverage_df[name], label=name)
        
        plt.title('Portfolio Leverage Over Time')
        plt.xlabel('Date')
        plt.ylabel('Leverage (Sum of Absolute Weights)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("volatility_targeting_leverage.png")
        plt.close()
    
    return {
        'equity_curves': equity_curves,
        'realized_vols': realized_vols,
        'metrics': metrics_df,
        'portfolios': portfolios,
        'leverage': leverage_df
    }

def analyze_volatility_targeting_in_market_regimes():
    """
    Analyze how volatility targeting performs in different market regimes.
    """
    logger.info("Analyzing volatility targeting across market regimes...")
    
    # Load data for market regime detection
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    
    # First get BTC data for regime detection
    btc_data = load_yahoo_finance_data(
        symbols=['BTC-USD'],
        start_date=start_date,
        end_date=end_date,
        interval='1d'
    )
    
    if btc_data is None or btc_data.empty:
        logger.error("Failed to load data for market regime analysis")
        return
    
    # Define market regimes
    btc_close = btc_data.xs('BTC-USD', level='symbol')['close']
    btc_returns = btc_close.pct_change().dropna()
    
    # Volatility regime (30-day rolling, annualized)
    vol = btc_returns.rolling(window=30).std() * np.sqrt(365)
    vol_threshold = vol.quantile(0.7)  # 70th percentile
    
    # Trend regime (30d vs 90d moving average)
    ma_short = btc_close.rolling(window=30).mean()
    ma_long = btc_close.rolling(window=90).mean()
    trend = ma_short - ma_long
    
    # Create regime DataFrame
    regimes = pd.DataFrame(index=vol.index)
    regimes['Volatility'] = vol
    regimes['Trend'] = trend
    regimes['High_Vol'] = vol > vol_threshold
    regimes['Up_Trend'] = trend > 0
    
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
    
    # Now load full data for strategy
    full_data = load_yahoo_finance_data(
        symbols=YF_UNIVERSE,
        start_date=start_date,
        end_date=end_date,
        interval='1d'
    )
    
    if full_data is None or full_data.empty:
        logger.error("Failed to load full data for strategy testing")
        return
    
    close_prices = full_data['close']
    
    # Calculate base weights using 60% momentum, 40% mean reversion
    momentum = calculate_momentum(close_prices, window=60)
    mean_rev = calculate_mean_reversion(close_prices, ma_window=50, z_window=20)
    
    mom_rank = cross_sectional_rank(momentum)
    mr_rank = cross_sectional_rank(mean_rev)
    combined_rank = 0.6 * mom_rank + 0.4 * mr_rank
    
    base_weights = calculate_top_n_weights(combined_rank, n=3)
    
    # Calculate volatility-targeted weights with target vol = 30% and max leverage = 1.5
    vol_weights = calculate_volatility_targeted_weights(
        weights=base_weights,
        returns=close_prices.pct_change().dropna(),
        target_vol=0.3,
        max_leverage=1.5,
        cov_window=60,
        vol_cap=0.6
    )
    
    # Run backtests
    baseline_portfolio = run_factor_backtest(
        close_prices=close_prices,
        target_weights=base_weights,
        init_cash=100000,
        fees=0.001,
        slippage=0.0005
    )
    
    vol_portfolio = run_factor_backtest(
        close_prices=close_prices,
        target_weights=vol_weights,
        init_cash=100000,
        fees=0.001,
        slippage=0.0005
    )
    
    if baseline_portfolio is None or vol_portfolio is None:
        logger.error("One or more backtests failed")
        return
    
    # Calculate weights for the regime analysis function
    def extract_portfolio_returns(portfolio):
        """Helper function to extract returns from different portfolio implementations"""
        if portfolio is None:
            return None
            
        try:
            if hasattr(portfolio, 'returns'):
                # Check if returns is a property or a method
                if callable(getattr(portfolio, 'returns')):
                    returns = portfolio.returns()
                else:
                    returns = portfolio.returns
                return returns.dropna()
            elif hasattr(portfolio, 'results') and hasattr(portfolio.results, 'returns'):
                return portfolio.results.returns.dropna()
            else:
                logger.warning("Could not find returns attribute")
                # Try reconstructing from equity if available
                if hasattr(portfolio, 'equity'):
                    equity = portfolio.equity
                    return equity.pct_change().dropna()
                else:
                    logger.error("Could not extract returns from portfolio")
                    return None
        except Exception as e:
            logger.error(f"Error extracting returns: {e}")
            return None
    
    # Replace the direct returns access with the helper function
    baseline_returns = extract_portfolio_returns(baseline_portfolio)
    vol_returns = extract_portfolio_returns(vol_portfolio)
    
    if baseline_returns is None or vol_returns is None:
        logger.error("Failed to extract returns from portfolios")
        return
        
    # Add regime information
    returns_with_regime = pd.DataFrame({
        'Baseline': baseline_returns,
        'Vol_Targeted': vol_returns
    })
    
    # Add regime column
    returns_with_regime['Regime'] = np.nan
    for date in returns_with_regime.index:
        if date in regimes.index:
            returns_with_regime.loc[date, 'Regime'] = regimes.loc[date, 'Regime']
    
    # Remove rows with missing regime data
    returns_with_regime = returns_with_regime.dropna()
    
    # Calculate performance metrics by regime
    regime_metrics = {}
    
    for regime in returns_with_regime['Regime'].unique():
        regime_data = returns_with_regime[returns_with_regime['Regime'] == regime]
        
        # Calculate metrics
        regime_metrics[regime] = {
            'Baseline': {
                'Mean Return (%)': regime_data['Baseline'].mean() * 100,
                'Volatility (%)': regime_data['Baseline'].std() * np.sqrt(252) * 100,
                'Sharpe Ratio': (regime_data['Baseline'].mean() / regime_data['Baseline'].std()) * np.sqrt(252),
                'Win Rate (%)': (regime_data['Baseline'] > 0).mean() * 100,
                'Count': len(regime_data)
            },
            'Vol_Targeted': {
                'Mean Return (%)': regime_data['Vol_Targeted'].mean() * 100,
                'Volatility (%)': regime_data['Vol_Targeted'].std() * np.sqrt(252) * 100,
                'Sharpe Ratio': (regime_data['Vol_Targeted'].mean() / regime_data['Vol_Targeted'].std()) * np.sqrt(252),
                'Win Rate (%)': (regime_data['Vol_Targeted'] > 0).mean() * 100,
                'Count': len(regime_data)
            }
        }
    
    # Print metrics by regime
    for regime, metrics in regime_metrics.items():
        logger.info(f"\n=== Performance in {regime} Regime ===")
        logger.info(f"Number of days: {metrics['Baseline']['Count']}")
        logger.info(f"Baseline - Mean Return: {metrics['Baseline']['Mean Return (%)']:.2f}%, "
                   f"Volatility: {metrics['Baseline']['Volatility (%)']:.2f}%, "
                   f"Sharpe: {metrics['Baseline']['Sharpe Ratio']:.2f}, "
                   f"Win Rate: {metrics['Baseline']['Win Rate (%)']:.2f}%")
        logger.info(f"Vol Targeted - Mean Return: {metrics['Vol_Targeted']['Mean Return (%)']:.2f}%, "
                   f"Volatility: {metrics['Vol_Targeted']['Volatility (%)']:.2f}%, "
                   f"Sharpe: {metrics['Vol_Targeted']['Sharpe Ratio']:.2f}, "
                   f"Win Rate: {metrics['Vol_Targeted']['Win Rate (%)']:.2f}%")
    
    # Create comparison plots
    # 1. Return distribution by regime
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    regime_order = ['Strong Bull', 'Weak Bull', 'Weak Bear', 'Strong Bear']
    
    for i, regime in enumerate(regime_order):
        if regime not in returns_with_regime['Regime'].unique():
            continue
            
        row, col = i // 2, i % 2
        ax = axes[row, col]
        
        regime_data = returns_with_regime[returns_with_regime['Regime'] == regime]
        
        # Plot histograms
        ax.hist(regime_data['Baseline'] * 100, bins=30, alpha=0.5, label='Baseline')
        ax.hist(regime_data['Vol_Targeted'] * 100, bins=30, alpha=0.5, label='Vol Targeted')
        
        ax.set_title(f'{regime} Regime')
        ax.set_xlabel('Daily Return (%)')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("volatility_targeting_regime_histograms.png")
    plt.close()
    
    # 2. Comparative metrics across regimes
    metrics_for_plot = ['Mean Return (%)', 'Volatility (%)', 'Sharpe Ratio', 'Win Rate (%)']
    
    for metric in metrics_for_plot:
        plt.figure(figsize=(10, 6))
        
        baseline_values = [regime_metrics[r]['Baseline'][metric] for r in regime_order if r in regime_metrics]
        vol_values = [regime_metrics[r]['Vol_Targeted'][metric] for r in regime_order if r in regime_metrics]
        regimes_present = [r for r in regime_order if r in regime_metrics]
        
        x = np.arange(len(regimes_present))
        width = 0.35
        
        plt.bar(x - width/2, baseline_values, width, label='Baseline')
        plt.bar(x + width/2, vol_values, width, label='Vol Targeted')
        
        plt.xlabel('Market Regime')
        plt.ylabel(metric)
        plt.title(f'Comparison of {metric} Across Market Regimes')
        plt.xticks(x, regimes_present)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"volatility_targeting_{metric.lower().replace(' ', '_').replace('(%)', '')}_by_regime.png")
        plt.close()
    
    return {
        'regimes': regimes,
        'regime_metrics': regime_metrics,
        'returns_with_regime': returns_with_regime,
        'baseline_portfolio': baseline_portfolio,
        'vol_portfolio': vol_portfolio
    }

if __name__ == "__main__":
    logger.info("=== Volatility Targeting Evaluation using Yahoo Finance Data ===")
    
    # Test volatility prediction
    vol_prediction_results = test_volatility_prediction()
    
    # Test volatility targeting with different parameters
    targeting_results = test_portfolio_volatility_targeting()
    
    # Analyze performance in different market regimes
    regime_analysis = analyze_volatility_targeting_in_market_regimes()
    
    logger.info("Evaluation complete. Check the generated plots for visual results.") 