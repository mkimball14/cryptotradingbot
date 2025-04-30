#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced validation metrics for signal quality and strategy robustness.

This module provides specialized metrics to evaluate signal generation quality,
parameter stability across optimization runs, and strategy robustness under
different market conditions.
"""

import logging
import traceback
from typing import Dict, List, Tuple, Optional, Any, Union, Set
import numpy as np
import pandas as pd
import scipy.stats as stats

# Set up logging
logger = logging.getLogger(__name__)


def calculate_signal_quality_metrics(
    entries: pd.Series,
    exits: pd.Series,
    equity_curve: pd.Series,
    returns: pd.Series,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate enhanced signal quality metrics.
    
    This function evaluates signal generation beyond simple win rate and profit,
    focusing on signal timing, efficiency, and robustness.
    
    Args:
        entries: Series of entry signals (True/False)
        exits: Series of exit signals (True/False)
        equity_curve: Series of portfolio equity values
        returns: Series of trade returns
        parameters: Dictionary of strategy parameters
        
    Returns:
        Dictionary of signal quality metrics
    """
    metrics = {}
    
    # Count valid signals
    num_entries = entries.sum()
    num_exits = exits.sum()
    metrics['num_signals'] = int(num_entries + num_exits)
    
    # Check if we have enough signals to calculate metrics
    if metrics['num_signals'] < 2:
        logger.warning("Not enough signals to calculate quality metrics")
        return {
            'num_signals': metrics['num_signals'],
            'signal_quality_score': 0.0,
            'signal_efficiency': 0.0,
            'parameter_sensitivity': 1.0,  # High sensitivity (bad)
            'signal_consistency': 0.0      # Low consistency (bad)
        }
    
    # Calculate signal density (signals per bar)
    signal_density = metrics['num_signals'] / len(entries)
    metrics['signal_density'] = signal_density
    
    # Calculate average holding period
    if num_entries > 0 and num_exits > 0:
        entry_indices = entries[entries].index
        exit_indices = exits[exits].index
        
        # Match each entry with the next exit
        holding_periods = []
        last_entry_idx = None
        
        for i, entry_idx in enumerate(entry_indices):
            # Find the next exit after this entry
            next_exits = exit_indices[exit_indices > entry_idx]
            if len(next_exits) > 0:
                # If there's a next exit, calculate holding period
                exit_idx = next_exits[0]
                holding_period = (exit_idx - entry_idx).total_seconds() / 60 / 60 / 24  # in days
                holding_periods.append(holding_period)
                last_entry_idx = entry_idx
        
        if holding_periods:
            metrics['avg_holding_period'] = np.mean(holding_periods)
            metrics['min_holding_period'] = np.min(holding_periods)
            metrics['max_holding_period'] = np.max(holding_periods)
            metrics['holding_period_std'] = np.std(holding_periods)
        else:
            metrics['avg_holding_period'] = 0
            metrics['min_holding_period'] = 0
            metrics['max_holding_period'] = 0
            metrics['holding_period_std'] = 0
    else:
        metrics['avg_holding_period'] = 0
        metrics['min_holding_period'] = 0
        metrics['max_holding_period'] = 0
        metrics['holding_period_std'] = 0
    
    # Calculate signal efficiency (profit per signal)
    if metrics['num_signals'] > 0 and not equity_curve.empty:
        total_return = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1
        metrics['signal_efficiency'] = total_return / metrics['num_signals']
    else:
        metrics['signal_efficiency'] = 0
    
    # Extract win rate and average profitability
    if not returns.empty and len(returns) > 0:
        metrics['win_rate'] = (returns > 0).mean()
        metrics['avg_profit'] = returns.mean()
        metrics['profit_variability'] = returns.std() / abs(returns.mean()) if returns.mean() != 0 else float('inf')
    else:
        metrics['win_rate'] = 0
        metrics['avg_profit'] = 0
        metrics['profit_variability'] = float('inf')
    
    # Calculate signal consistency (regularity of signal generation)
    if num_entries > 1:
        entry_timestamps = entries[entries].index
        entry_intervals = np.diff(entry_timestamps.astype(np.int64)) / 1e9 / 60 / 60 / 24  # in days
        
        # Use coefficient of variation as a measure of consistency
        if np.mean(entry_intervals) > 0:
            metrics['signal_consistency'] = 1.0 / (np.std(entry_intervals) / np.mean(entry_intervals))
        else:
            metrics['signal_consistency'] = 0
    else:
        metrics['signal_consistency'] = 0
    
    # Calculate parameter sensitivity (experimental)
    # This estimates how sensitive the strategy might be to parameter changes
    # A lower score is better (less sensitive)
    strictness_factor = 1.0
    if 'signal_strictness' in parameters:
        # More strict signals should have lower sensitivity
        if parameters['signal_strictness'] == 'STRICT':
            strictness_factor = 0.5
        elif parameters['signal_strictness'] == 'BALANCED':
            strictness_factor = 0.8
    
    # Estimate sensitivity based on trade consistency and profitability
    if len(returns) > 1:
        profit_consistency = 1.0 / (returns.std() / abs(returns.mean())) if returns.mean() != 0 else 0
        metrics['parameter_sensitivity'] = strictness_factor * (1.0 - min(1.0, profit_consistency))
    else:
        metrics['parameter_sensitivity'] = 0.5  # default midpoint
    
    # Calculate an overall signal quality score (0-100)
    # This combines multiple factors weighted by importance
    if metrics['num_signals'] > 0:
        quality_score = (
            metrics['win_rate'] * 40 +                     # Win rate (40% weight)
            min(1.0, metrics['signal_efficiency'] * 10) * 20 +  # Efficiency (20% weight)
            min(1.0, metrics['signal_consistency']) * 20 +  # Consistency (20% weight)
            (1.0 - metrics['parameter_sensitivity']) * 20   # Low sensitivity (20% weight)
        )
        metrics['signal_quality_score'] = quality_score
    else:
        metrics['signal_quality_score'] = 0
    
    return metrics


def evaluate_parameter_stability(
    optimization_results: List[Dict[str, Any]],
    parameter_names: List[str]
) -> Dict[str, Any]:
    """
    Evaluate parameter stability across multiple optimization runs.
    
    This helps identify how consistent optimal parameters are,
    which indicates robustness of the strategy.
    
    Args:
        optimization_results: List of optimization result dictionaries
        parameter_names: List of parameter names to evaluate
        
    Returns:
        Dictionary with parameter stability metrics
    """
    if not optimization_results or not parameter_names:
        return {
            'stability_score': 0.0,
            'parameter_variance': {},
            'parameter_clusters': {}
        }
    
    # Extract parameter values from results
    param_values = {}
    for param in parameter_names:
        param_values[param] = []
        
        for result in optimization_results:
            if f'param_{param}' in result:
                param_values[param].append(result[f'param_{param}'])
            elif 'best_params' in result and param in result['best_params']:
                param_values[param].append(result['best_params'][param])
    
    # Calculate variance and normalized variance for each parameter
    param_variance = {}
    param_norm_variance = {}
    
    for param, values in param_values.items():
        if len(values) > 1:
            param_variance[param] = np.var(values)
            
            # Calculate parameter range for normalization
            param_range = max(values) - min(values)
            if param_range > 0:
                param_norm_variance[param] = param_variance[param] / (param_range ** 2)
            else:
                param_norm_variance[param] = 0  # All values are the same = perfect stability
        else:
            param_variance[param] = 0
            param_norm_variance[param] = 0
    
    # Try to detect parameter clusters (e.g., multimodal distributions)
    param_clusters = {}
    for param, values in param_values.items():
        if len(values) >= 5:  # Need enough samples for clustering
            try:
                from sklearn.cluster import KMeans
                from sklearn.metrics import silhouette_score
                
                # Reshape for scikit-learn
                X = np.array(values).reshape(-1, 1)
                
                # Try different numbers of clusters
                best_score = -1
                best_n_clusters = 1
                
                for n_clusters in range(2, min(5, len(values) // 2)):
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                    cluster_labels = kmeans.fit_predict(X)
                    
                    # Skip if we have clusters with only one point
                    if min(np.bincount(cluster_labels)) < 2:
                        continue
                    
                    # Calculate silhouette score
                    try:
                        score = silhouette_score(X, cluster_labels)
                        if score > best_score:
                            best_score = score
                            best_n_clusters = n_clusters
                    except:
                        pass
                
                # If we found good clusters
                if best_score > 0.5:  # Only accept reasonably distinct clusters
                    kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
                    cluster_labels = kmeans.fit_predict(X)
                    centers = kmeans.cluster_centers_.flatten()
                    
                    # Count points in each cluster
                    counts = np.bincount(cluster_labels)
                    
                    param_clusters[param] = {
                        'n_clusters': best_n_clusters,
                        'centers': centers.tolist(),
                        'counts': counts.tolist(),
                        'silhouette_score': best_score
                    }
                else:
                    # No significant clustering detected
                    param_clusters[param] = {
                        'n_clusters': 1,
                        'centers': [np.mean(values)],
                        'counts': [len(values)],
                        'silhouette_score': 0
                    }
            except ImportError:
                # Scikit-learn not available
                param_clusters[param] = {
                    'n_clusters': 1,
                    'centers': [np.mean(values)],
                    'counts': [len(values)],
                    'silhouette_score': 0
                }
    
    # Calculate overall stability score
    if param_norm_variance:
        # Lower is better for normalized variance
        avg_norm_variance = np.mean(list(param_norm_variance.values()))
        stability_score = 1.0 - min(1.0, avg_norm_variance * 2)  # Scale to 0-1
        
        # Adjust for multimodal distributions
        multimodal_penalty = 0
        for param_info in param_clusters.values():
            if param_info['n_clusters'] > 1 and param_info['silhouette_score'] > 0.5:
                # Apply penalty for strong multimodal distributions
                multimodal_penalty += 0.1 * (param_info['n_clusters'] - 1)
        
        stability_score = max(0, stability_score - multimodal_penalty)
    else:
        stability_score = 0
    
    return {
        'stability_score': stability_score,
        'parameter_variance': param_variance,
        'parameter_norm_variance': param_norm_variance,
        'parameter_clusters': param_clusters
    }


def evaluate_robustness_across_regimes(
    results_by_regime: Dict[str, Dict[str, Any]],
    regime_weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Evaluate strategy robustness across different market regimes.
    
    Args:
        results_by_regime: Dictionary of performance results by regime
        regime_weights: Optional dictionary of importance weights for each regime
        
    Returns:
        Dictionary with robustness metrics
    """
    if not results_by_regime:
        return {
            'robustness_score': 0.0,
            'regime_performance': {},
            'regime_consistency': 0.0
        }
    
    # Default weights if not provided
    if regime_weights is None:
        regime_weights = {regime: 1.0 for regime in results_by_regime.keys()}
        
    # Normalize weights
    total_weight = sum(regime_weights.values())
    if total_weight > 0:
        regime_weights = {k: v / total_weight for k, v in regime_weights.items()}
    
    # Extract performance metrics by regime
    regime_performance = {}
    for regime, results in results_by_regime.items():
        if 'sharpe_ratio' in results:
            regime_performance[regime] = {
                'sharpe_ratio': results['sharpe_ratio'],
                'win_rate': results.get('win_rate', 0),
                'num_trades': results.get('num_trades', 0),
                'profit_factor': results.get('profit_factor', 0)
            }
    
    # Calculate performance consistency across regimes
    if len(regime_performance) > 1:
        sharpe_ratios = [perf['sharpe_ratio'] for perf in regime_performance.values()]
        win_rates = [perf['win_rate'] for perf in regime_performance.values()]
        
        # Use coefficient of variation as consistency measure
        # Lower CV = higher consistency
        sharpe_cv = np.std(sharpe_ratios) / np.mean(sharpe_ratios) if np.mean(sharpe_ratios) > 0 else float('inf')
        win_rate_cv = np.std(win_rates) / np.mean(win_rates) if np.mean(win_rates) > 0 else float('inf')
        
        # Convert to a 0-1 score where higher is better
        sharpe_consistency = 1.0 / (1.0 + sharpe_cv)
        win_rate_consistency = 1.0 / (1.0 + win_rate_cv)
        
        # Combined consistency score
        regime_consistency = 0.7 * sharpe_consistency + 0.3 * win_rate_consistency
    else:
        regime_consistency = 0.5  # Neutral if only one regime
    
    # Calculate weighted performance
    weighted_performance = 0
    for regime, perf in regime_performance.items():
        if regime in regime_weights:
            weighted_performance += perf['sharpe_ratio'] * regime_weights[regime]
    
    # Calculate overall robustness score
    robustness_score = 0.6 * weighted_performance + 0.4 * regime_consistency
    
    # Scale to 0-100 range
    robustness_score = min(100, max(0, robustness_score * 20))
    
    return {
        'robustness_score': robustness_score,
        'regime_performance': regime_performance,
        'regime_consistency': regime_consistency,
        'weighted_performance': weighted_performance
    }


def statistical_significance_test(
    performance_metrics_a: Dict[str, Any],
    performance_metrics_b: Dict[str, Any],
    trade_returns_a: List[float],
    trade_returns_b: List[float],
    confidence_level: float = 0.95
) -> Dict[str, Any]:
    """
    Perform statistical significance tests between two strategy variants.
    
    Args:
        performance_metrics_a: Performance metrics for strategy A
        performance_metrics_b: Performance metrics for strategy B
        trade_returns_a: List of individual trade returns for strategy A
        trade_returns_b: List of individual trade returns for strategy B
        confidence_level: Confidence level for statistical tests
        
    Returns:
        Dictionary with statistical significance test results
    """
    results = {
        'is_significant': False,
        'p_value': 1.0,
        'confidence_level': confidence_level,
        'test_method': 'unknown'
    }
    
    # Ensure we have enough trades to test
    if len(trade_returns_a) < 10 or len(trade_returns_b) < 10:
        results['test_method'] = 'insufficient_data'
        return results
    
    # Perform Mann-Whitney U test (non-parametric, doesn't assume normal distribution)
    try:
        u_stat, p_value = stats.mannwhitneyu(trade_returns_a, trade_returns_b, alternative='two-sided')
        results['test_method'] = 'mannwhitneyu'
        results['p_value'] = p_value
        results['is_significant'] = p_value < (1 - confidence_level)
        results['u_statistic'] = u_stat
    except:
        # Fallback to t-test if Mann-Whitney fails
        try:
            t_stat, p_value = stats.ttest_ind(trade_returns_a, trade_returns_b, equal_var=False)
            results['test_method'] = 'welch_ttest'
            results['p_value'] = p_value
            results['is_significant'] = p_value < (1 - confidence_level)
            results['t_statistic'] = t_stat
        except:
            # Fallback to simple mean difference
            mean_diff = np.mean(trade_returns_a) - np.mean(trade_returns_b)
            results['mean_difference'] = mean_diff
            results['test_method'] = 'mean_comparison'
            results['is_significant'] = False
    
    # Add effect size calculation
    try:
        # Cohen's d for effect size
        mean_a = np.mean(trade_returns_a)
        mean_b = np.mean(trade_returns_b)
        
        # Pooled standard deviation
        s_a = np.std(trade_returns_a, ddof=1)
        s_b = np.std(trade_returns_b, ddof=1)
        n_a = len(trade_returns_a)
        n_b = len(trade_returns_b)
        
        # Calculate pooled standard deviation
        s_pooled = np.sqrt(((n_a - 1) * s_a**2 + (n_b - 1) * s_b**2) / (n_a + n_b - 2))
        
        # Cohen's d
        if s_pooled > 0:
            cohens_d = (mean_a - mean_b) / s_pooled
            results['effect_size'] = cohens_d
            
            # Interpret effect size
            if abs(cohens_d) < 0.2:
                results['effect_size_interpretation'] = 'negligible'
            elif abs(cohens_d) < 0.5:
                results['effect_size_interpretation'] = 'small'
            elif abs(cohens_d) < 0.8:
                results['effect_size_interpretation'] = 'medium'
            else:
                results['effect_size_interpretation'] = 'large'
        else:
            results['effect_size'] = 0
            results['effect_size_interpretation'] = 'undefined'
            
    except:
        results['effect_size'] = 0
        results['effect_size_interpretation'] = 'calculation_failed'
    
    return results


def calculate_performance_metrics(portfolio) -> Dict[str, Any]:
    """
    Calculate various performance metrics for a vectorbtpro Portfolio object.
    
    Args:
        portfolio: vectorbtpro Portfolio object from a backtest
        
    Returns:
        Dictionary of performance metrics
    """
    metrics = {}
    
    try:
        # Get basic stats from the portfolio object - with safeguards for different vectorbtpro versions
        try:
            if hasattr(portfolio, 'stats'):
                if callable(portfolio.stats):
                    try:
                        # Try calling stats as a method
                        stats = portfolio.stats()
                        logger.info(f"Called portfolio.stats() method successfully, got {len(stats) if stats else 0} metrics")
                    except Exception as e:
                        logger.warning(f"Error calling portfolio.stats(): {e}")
                        # Fallback to accessing stats directly
                        stats = getattr(portfolio, 'stats', {})
                        if callable(stats):
                            stats = {}
                else:
                    # stats is an attribute, not a method
                    stats = portfolio.stats
                    logger.info(f"Got portfolio.stats attribute with {len(stats) if hasattr(stats, '__len__') else 'unknown'} metrics")
            else:
                # No stats attribute/method, use empty dict
                logger.warning("Portfolio object has no 'stats' attribute or method")
                stats = {}
                
        except Exception as e:
            logger.warning(f"Exception accessing portfolio stats: {str(e)}")
            stats = {}
            
        # Safely extract key metrics with proper error handling
        try:
            metrics['total_return'] = float(stats.get('Total Return [%]', 0.0))
            metrics['sharpe_ratio'] = float(stats.get('Sharpe Ratio', 0.0))
            metrics['sortino_ratio'] = float(stats.get('Sortino Ratio', 0.0))
            metrics['calmar_ratio'] = float(stats.get('Calmar Ratio', 0.0))
            metrics['max_drawdown'] = float(stats.get('Max Drawdown [%]', 0.0))
            metrics['annual_return'] = float(stats.get('Annual Return [%]', 0.0))
            metrics['annual_volatility'] = float(stats.get('Annual Volatility [%]', 0.0))
        except Exception as e:
            logger.warning(f"Error extracting stats values: {e}")
            # Set defaults for missing metrics
            metrics['total_return'] = 0.0
            metrics['sharpe_ratio'] = 0.0
            metrics['sortino_ratio'] = 0.0
            metrics['calmar_ratio'] = 0.0
            metrics['max_drawdown'] = 0.0
            metrics['annual_return'] = 0.0
            metrics['annual_volatility'] = 0.0
        metrics['expectancy'] = float(stats.get('Expectancy [%]', 0.0))
        metrics['total_trades'] = int(stats.get('Total Trades', 0))
        metrics['win_rate'] = float(stats.get('Win Rate [%]', 0.0))
        metrics['profit_factor'] = float(stats.get('Profit Factor', 1.0))
        
        # Safely access returns data
        try:
            # Try different ways to access returns data based on vectorbtpro version
            rets = None
            if hasattr(portfolio, 'returns'):
                if callable(portfolio.returns):
                    try:
                        rets = portfolio.returns()
                        logger.info(f"Successfully called portfolio.returns() method")
                    except Exception as e:
                        logger.warning(f"Error calling portfolio.returns(): {e}")
                        # Try to access the returns attribute directly
                        rets = getattr(portfolio, 'returns', pd.Series())
                        if callable(rets):
                            rets = pd.Series()
                else:
                    # Returns is an attribute
                    rets = portfolio.returns
                    logger.info(f"Accessed portfolio.returns attribute directly")
            else:
                # Look for returns in stats
                logger.warning("Portfolio has no returns method or attribute, checking other sources")
                # Try to extract returns from the stats if possible
                rets = pd.Series()
                
            # Calculate return metrics if we have valid returns data
            if isinstance(rets, pd.Series) and not rets.empty:
                logger.info(f"Processing returns Series with {len(rets)} values")
                # Mean return and volatility
                metrics['mean_return'] = float(rets.mean())
                metrics['return_volatility'] = float(rets.std())
                
                # Return stream characteristics
                positive_rets = rets[rets > 0]
                negative_rets = rets[rets < 0]
                metrics['positive_day_ratio'] = len(positive_rets) / len(rets) if len(rets) > 0 else 0
                metrics['avg_positive_return'] = float(positive_rets.mean()) if len(positive_rets) > 0 else 0
                metrics['avg_negative_return'] = float(negative_rets.mean()) if len(negative_rets) > 0 else 0
                
                # Return to risk ratio
                if metrics['return_volatility'] > 0:
                    metrics['return_to_risk'] = metrics['mean_return'] / metrics['return_volatility']
                else:
                    metrics['return_to_risk'] = 0.0
            else:
                logger.warning("No valid returns data available for analysis")
                # Set default metrics
                metrics['mean_return'] = 0.0
                metrics['return_volatility'] = 0.0
                metrics['positive_day_ratio'] = 0.0
                metrics['avg_positive_return'] = 0.0
                metrics['avg_negative_return'] = 0.0
                metrics['return_to_risk'] = 0.0
        except Exception as e:
            logger.warning(f"Error processing returns data: {e}")
            logger.warning(traceback.format_exc())
            # Set default metrics
            metrics['mean_return'] = 0.0
            metrics['return_volatility'] = 0.0
            metrics['positive_day_ratio'] = 0.0
            metrics['avg_positive_return'] = 0.0
            metrics['avg_negative_return'] = 0.0
            metrics['return_to_risk'] = 0.0
            
        # Additional metrics from returns data
        if 'mean_return' in metrics and metrics['mean_return'] != 0.0 and 'return_volatility' in metrics and metrics['return_volatility'] > 0:
            # We already have valid returns data processed above
            metrics['volatility'] = float(metrics['return_volatility'] * np.sqrt(252))  # Annualized vol using already computed value
            
            # Calculate downside deviation if we have mean return and volatility
            if 'annual_return' in metrics:
                # Use pre-calculated stats if possible
                metrics['information_ratio'] = metrics.get('information_ratio', 0.0)  # Keep existing or set to 0
            else:
                metrics['information_ratio'] = 0.0
        else:
            # No valid returns data, use defaults
            metrics['volatility'] = 0.0
            metrics['information_ratio'] = 0.0
        
        # Underwater and drawdown calculations
        if metrics['max_drawdown'] > 0:
            try:
                # Safely check how to access drawdown data
                underwater = None
                try:
                    if hasattr(portfolio, 'drawdowns'):
                        # Try accessing through drawdowns accessor
                        drawdowns = portfolio.drawdowns
                        if hasattr(drawdowns, 'get_drawdown_series') and callable(drawdowns.get_drawdown_series):
                            underwater = drawdowns.get_drawdown_series()
                            logger.info("Got drawdown series from portfolio.drawdowns.get_drawdown_series()")
                        else:
                            # Try other attribute access patterns
                            underwater = getattr(drawdowns, 'drawdown', None)
                            logger.info("Got drawdown series from portfolio.drawdowns.drawdown attribute")
                    elif hasattr(portfolio, 'drawdown'):
                        if callable(portfolio.drawdown):
                            try:
                                underwater = portfolio.drawdown()
                                logger.info("Got drawdown series from portfolio.drawdown() method")
                            except Exception as e:
                                logger.warning(f"Error calling portfolio.drawdown(): {e}")
                                underwater = None
                        else:
                            underwater = portfolio.drawdown
                            logger.info("Got drawdown series from portfolio.drawdown attribute")
                    else:
                        # Try getting from stats
                        stats_obj = getattr(portfolio, 'stats', None)
                        if stats_obj is not None:
                            if callable(stats_obj):
                                stats_dict = stats_obj()
                                underwater = stats_dict.get('drawdown', None)
                            else:
                                underwater = stats_obj.get('drawdown', None)
                except Exception as e:
                    logger.warning(f"Error accessing drawdown data: {e}")
                    underwater = None
                
                # Process underwater periods if we got valid data
                if isinstance(underwater, pd.Series) and not underwater.empty:
                    logger.info(f"Processing drawdown Series with {len(underwater)} values")
                    # Find underwater periods (drawdown > 5%)
                    mask = underwater < -0.05
                    if mask.any():  # Only process if we have any qualifying drawdowns
                        underwater_periods = mask.astype(int).diff().fillna(0).abs().cumsum()
                        period_lengths = underwater_periods[mask].value_counts()
                        metrics['underwater_periods'] = len(period_lengths)
                        metrics['max_underwater_duration'] = period_lengths.max() if len(period_lengths) > 0 else 0
                    else:
                        metrics['underwater_periods'] = 0
                        metrics['max_underwater_duration'] = 0
                else:
                    logger.warning("No valid drawdown data available")
                    metrics['underwater_periods'] = 0
                    metrics['max_underwater_duration'] = 0
            except Exception as e:
                logger.warning(f"Error calculating underwater periods: {e}")
                logger.warning(f"Traceback: {traceback.format_exc()}")
                metrics['underwater_periods'] = 0
                metrics['max_underwater_duration'] = 0
                
        # Risk-adjusted metrics
        if metrics['volatility'] > 0:
            metrics['return_to_risk'] = metrics['total_return'] / metrics['volatility'] 
        else:
            metrics['return_to_risk'] = 0.0
            
        # Evaluate winning and losing trades
        # Get base metrics from portfolio stats
        metrics['total_trades'] = int(stats.get('Total Trades', 0))
        metrics['win_rate'] = float(stats.get('Win Rate [%]', 0.0))
        
        # Access detailed trade data based on vectorbtpro version
        wins = pd.DataFrame()
        losses = pd.DataFrame()
        
        try:
            if hasattr(portfolio, 'trades'):
                if hasattr(portfolio.trades, 'records') and len(portfolio.trades.records) > 0:
                    # Access structured records array
                    trades_records = portfolio.trades.records
                    # Use total trades from records if available
                    metrics['total_trades'] = len(trades_records)
                    
                    # Check if trades has a get_returned method to calculate win/loss stats
                    if hasattr(portfolio.trades, 'get_returns') and callable(portfolio.trades.get_returns):
                        returns = portfolio.trades.get_returns()
                        if isinstance(returns, pd.Series) and not returns.empty:
                            wins_mask = returns > 0
                            if wins_mask.any():
                                wins_returns = returns[wins_mask]
                                metrics['avg_win'] = float(wins_returns.mean())
                                metrics['max_win'] = float(wins_returns.max())
                                metrics['win_rate'] = (len(wins_returns) / len(returns)) * 100
                            
                            losses_mask = returns <= 0
                            if losses_mask.any():
                                losses_returns = returns[losses_mask]
                                metrics['avg_loss'] = float(losses_returns.mean())
                                metrics['max_loss'] = float(losses_returns.min())
                                
                        # Skip the rest of the processing by setting flags
                        wins = pd.DataFrame([1])  # Non-empty dataframe to skip further processing
                        losses = pd.DataFrame([1])
                        # We have processed the returns already
                    
                    # Convert records to DataFrame if needed
                    if not isinstance(trades_records, pd.DataFrame):
                        # Try to convert records array to dataframe
                        try:
                            trade_data = pd.DataFrame(trades_records)
                        except Exception as e:
                            logger.warning(f"Error converting trade records to DataFrame: {e}")
                            trade_data = pd.DataFrame()
                    else:
                        trade_data = trades_records
                    
                    # Process trade data if we have returns information
                    if not trade_data.empty and 'return' in trade_data.columns:
                        wins = trade_data[trade_data['return'] > 0]
                        losses = trade_data[trade_data['return'] <= 0]
                    elif not trade_data.empty and 'pnl' in trade_data.columns:
                        # Try using PnL if return isn't available
                        wins = trade_data[trade_data['pnl'] > 0]
                        losses = trade_data[trade_data['pnl'] <= 0]
                        
            # If we couldn't get trade data from the portfolio, use the stats
            if wins.empty and losses.empty:
                # Set reasonable defaults based on portfolio stats
                logger.warning("Using stats-based metrics as detailed trade data unavailable")
        except Exception as e:
            logger.warning(f"Error processing trade data: {e}")
            # Keep using the stats-based metrics
            
            if len(wins) > 0:
                metrics['avg_win'] = float(wins['return'].mean())
                metrics['max_win'] = float(wins['return'].max())
            else:
                metrics['avg_win'] = 0.0
                metrics['max_win'] = 0.0
                
            if len(losses) > 0:
                metrics['avg_loss'] = float(losses['return'].mean())
                metrics['max_loss'] = float(losses['return'].min())  # Min return = max loss
            else:
                metrics['avg_loss'] = 0.0
                metrics['max_loss'] = 0.0
                
            # Risk of ruin estimate (simplified)
            if metrics['win_rate'] > 0 and metrics['avg_win'] > 0 and abs(metrics['avg_loss']) > 0:
                rr_factor = metrics['win_rate'] / (1 - metrics['win_rate']) * (metrics['avg_win'] / abs(metrics['avg_loss']))
                metrics['risk_of_ruin_factor'] = float(rr_factor)
            else:
                metrics['risk_of_ruin_factor'] = 0.0
                
    except Exception as e:
        logger.error(f"Error calculating performance metrics: {str(e)}")
        # Return basic empty metrics if calculation fails
        metrics = {
            'total_return': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'win_rate': 0.0,
            'total_trades': 0,
            'error': str(e)
        }
        
    return metrics


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    import numpy as np
    
    # Create sample data
    dates = pd.date_range(start='2023-01-01', periods=1000, freq='1h')
    entries = pd.Series(False, index=dates)
    exits = pd.Series(False, index=dates)
    
    # Set some random entries and exits
    np.random.seed(42)
    entry_points = np.random.choice(range(900), size=10, replace=False)
    exit_points = entry_points + np.random.randint(10, 50, size=10)
    
    for i, j in zip(entry_points, exit_points):
        if j < len(dates):
            entries.iloc[i] = True
            exits.iloc[j] = True
    
    # Create sample equity curve and returns
    equity = pd.Series(1000, index=dates)
    for i in range(1, len(dates)):
        change = np.random.normal(0.0001, 0.001)
        if entries.iloc[i-1]:
            change = np.random.normal(0.001, 0.002)  # Positive bias after entry
        equity.iloc[i] = equity.iloc[i-1] * (1 + change)
    
    # Sample trade returns
    returns = pd.Series(np.random.normal(0.02, 0.05, size=10))
    
    # Calculate signal quality metrics
    metrics = calculate_signal_quality_metrics(
        entries=entries,
        exits=exits,
        equity_curve=equity,
        returns=returns,
        parameters={'signal_strictness': 'BALANCED'}
    )
    
    print("Signal quality metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
