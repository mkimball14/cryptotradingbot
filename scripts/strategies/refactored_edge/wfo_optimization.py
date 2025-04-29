"""
Parameter optimization functions for Walk-Forward Optimization (WFO).

This module contains functions for optimizing strategy parameters, including
parallel processing, regime-aware optimization, and parameter grid handling.
"""
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm
import traceback
import logging
from typing import Dict, Any, Union, List, Optional, Tuple

# Local imports
from scripts.strategies.refactored_edge import regime
from scripts.strategies.refactored_edge.wfo_evaluation import evaluate_single_params
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge import indicators

# Configure logger
log = logging.getLogger(__name__)

def optimize_params_parallel(data, param_combinations, metric, n_jobs=-1):
    """
    Finds the best parameters using parallel processing.

    Args:
        data (pd.DataFrame): Training data.
        param_combinations (list): List of parameter dictionaries.
        metric (str): Performance metric to optimize.
        n_jobs (int): Number of parallel jobs.

    Returns:
        tuple: (best_params, best_score, best_params_by_regime) or (None, None, None) if no valid results
    """
    print(f"Optimizing {len(param_combinations)} parameter combinations using metric '{metric}'...")
    
    # Run evaluations in parallel
    results = Parallel(n_jobs=n_jobs)(
        delayed(evaluate_single_params)(params, data, metric)
        for params in tqdm(param_combinations, desc="Evaluating parameters")
    )
    
    # Combine parameters with their scores
    param_scores = list(zip(param_combinations, results))
    
    # Filter out invalid scores (non-finite values)
    valid_results = [(params, score) for params, score in param_scores if np.isfinite(score)]
    
    if not valid_results:
        print("No valid parameter combinations found during optimization.")
        return (None, None, None)
    
    # Find best overall parameters
    best_params, best_score = max(valid_results, key=lambda x: x[1])
    
    # Organize results by market regime if regime info is available
    regime_results = {
        'trending': [],
        'ranging': []
    }
    
    # Try to detect regime for each valid parameter set
    for params, score in valid_results:
        regime_info = params.get('_regime_info', None)
        if regime_info:
            # If we have regime info, categorize the result
            predominant = regime_info.get('predominant_regime', 'ranging')
            regime_results[predominant].append((params, score))
    
    # Count results by regime
    trending_count = len(regime_results['trending'])
    ranging_count = len(regime_results['ranging'])
    total_valid = len(valid_results)
    
    # Display regime distribution
    print("Regime distribution of valid results:")
    print(f"  - Trending: {trending_count}/{total_valid} results ({100*trending_count/total_valid if total_valid else 0:.1f}%)")
    print(f"  - Ranging: {ranging_count}/{total_valid} results ({100*ranging_count/total_valid if total_valid else 0:.1f}%)")
    
    # Find best params by regime (if we have enough data)
    best_params_by_regime = {}
    
    # Only consider a regime if we have enough samples (at least 2)
    if trending_count >= 2:
        best_trending_params, _ = max(regime_results['trending'], key=lambda x: x[1])
        best_params_by_regime['trending'] = best_trending_params
    
    if ranging_count >= 2:
        best_ranging_params, _ = max(regime_results['ranging'], key=lambda x: x[1])
        best_params_by_regime['ranging'] = best_ranging_params
    
    # If we couldn't get regime-specific params, use the overall best
    if not best_params_by_regime:
        best_params_by_regime['overall'] = best_params
    
    # Add the debug information about attempted params and raw results
    print(f"Optimization complete. Best overall score ({metric}): {best_score:.4f}")
    print(f"Best overall parameters found: {best_params}")
    print(f"Best parameters by regime: {list(best_params_by_regime.keys())}")
    
    # If valid results exist but best_score is still negative, warn about potential issues
    if valid_results and best_score < 0:
        print(f"WARNING: Best score is negative ({best_score:.4f}). Strategy may not be profitable.")
        
    # Debug info about failed optimizations
    if len(valid_results) < len(param_combinations):
        print(f"  Attempted {len(param_combinations)} parameter combinations.")
        print(f"  Raw results count: {len(results)}")
        print(f"  First 5 raw results (score): {results[:5]}")
    
    return best_params, best_score, best_params_by_regime


def determine_market_regime_for_params(data, config):
    """
    Determine the market regime for the given data using the provided configuration.
    
    Args:
        data (pd.DataFrame): The price data
        config: The configuration object for the current trial/split
        
    Returns:
        dict: Regime information including percentages and predominant regime
    """
    # Import modules inside function to avoid circular dependencies
    from scripts.strategies.refactored_edge.utils import (
        safe_get_column, get_numeric_column, ensure_config_attributes,
        calculate_regime_percentages, determine_predominant_regime,
        logger, with_error_handling
    )
    
    @with_error_handling(default_return={'trending_pct': 0, 'ranging_pct': 100, 'predominant_regime': 'ranging'})
    def _determine_regime():
        # Validate configuration attributes first
        required_config_attrs = [
            'use_enhanced_regimes', 'adx_threshold', 'volatility_threshold', 
            'momentum_lookback', 'momentum_threshold'
        ]
        
        # If using enhanced regimes, also check for strong_adx_threshold
        if hasattr(config, 'use_enhanced_regimes') and config.use_enhanced_regimes:
            required_config_attrs.append('strong_adx_threshold')
            
        if not ensure_config_attributes(config, required_config_attrs):
            logger.warning("Using default configuration attributes for missing values")
        
        # We need adx, plus_di, minus_di, atr and close for regime detection
        required_indicators = ['adx', 'plus_di', 'minus_di', 'atr']
        
        # Check if we need to add indicators
        if not all(col in data.columns for col in required_indicators):
            logger.info("Adding indicators for regime detection using provided config...")
            # Import here to avoid circular dependencies
            from scripts.strategies.refactored_edge import indicators
            
            # Get indicators using the passed config - make a copy to avoid side effects
            indicator_df = indicators.add_indicators(data.copy(), config)
            
            # Verify indicators were properly generated
            if not all(col in indicator_df.columns for col in required_indicators):
                logger.error(f"Required regime indicators {required_indicators} not generated by add_indicators")
                return {'trending_pct': 0, 'ranging_pct': 100, 'predominant_regime': 'ranging'}
            
            # Extract the required indicators safely
            adx = safe_get_column(indicator_df, 'adx')
            plus_di = safe_get_column(indicator_df, 'plus_di')
            minus_di = safe_get_column(indicator_df, 'minus_di')
            atr = safe_get_column(indicator_df, 'atr')
            close = safe_get_column(indicator_df, 'close', alternatives=['Close'])
        else:
            # Extract existing indicators safely
            adx = safe_get_column(data, 'adx')
            plus_di = safe_get_column(data, 'plus_di')
            minus_di = safe_get_column(data, 'minus_di')
            atr = safe_get_column(data, 'atr')
            close = safe_get_column(data, 'close', alternatives=['Close'])
        
        # Validate required data
        if close is None or adx is None:
            logger.warning("Missing critical data for regime detection (close price or ADX)")
            return {'trending_pct': 0, 'ranging_pct': 100, 'predominant_regime': 'ranging'}
        
        # Import regime module here to avoid circular dependencies
        from scripts.strategies.refactored_edge import regime
        
        # Determine market regime based on configuration
        use_enhanced = getattr(config, 'use_enhanced_regimes', False)
        adx_threshold = getattr(config, 'adx_threshold', 25.0)  # Default if not in config
        
        if use_enhanced:
            # Get other config parameters with defaults
            strong_adx_threshold = getattr(config, 'strong_adx_threshold', 35.0)
            volatility_threshold = getattr(config, 'volatility_threshold', 0.01)
            momentum_lookback = getattr(config, 'momentum_lookback', 5)
            momentum_threshold = getattr(config, 'momentum_threshold', 0.005)
            
            # Use advanced regime detection with all indicators
            regimes = regime.determine_market_regime_advanced(
                adx=adx,
                plus_di=plus_di, 
                minus_di=minus_di,
                atr=atr,
                close=close,
                high=safe_get_column(data, 'high', alternatives=['High']),
                low=safe_get_column(data, 'low', alternatives=['Low']),
                volume=safe_get_column(data, 'volume', alternatives=['Volume']),
                adx_threshold=adx_threshold,
                strong_adx_threshold=strong_adx_threshold,
                volatility_threshold=volatility_threshold,
                momentum_lookback=momentum_lookback,
                momentum_threshold=momentum_threshold,
                use_enhanced_classification=True
            )
        else:
            # Use simple regime detection with just ADX
            regimes = regime.determine_market_regime(adx, adx_threshold)
        
        # Calculate regime distribution
        regime_percentages = calculate_regime_percentages(regimes)
        logger.debug(f"Raw regime percentages: {regime_percentages}")
        
        # Initialize result with default values
        result = {
            'trending_pct': 0,
            'ranging_pct': 0,
            'predominant_regime': 'ranging'  # Default to ranging
        }
        
        # Update with actual regime percentages based on classification type
        if not use_enhanced:
            # Simple trending/ranging classification
            result['trending_pct'] = regime_percentages.get('trending', 0)
            result['ranging_pct'] = regime_percentages.get('ranging', 0)
        else:
            # Enhanced classification - group regimes into trending and ranging categories
            trending_regimes = [
                'trending', 'strong_uptrend', 'weak_uptrend', 'strong_downtrend', 'weak_downtrend',
                'breakout', 'breakdown', 'TRENDING', 'STRONG_UPTREND', 'WEAK_UPTREND', 'STRONG_DOWNTREND', 
                'WEAK_DOWNTREND', 'BREAKOUT', 'BREAKDOWN'
            ]
            ranging_regimes = [
                'ranging', 'volatile_range', 'quiet_range', 'RANGING', 'VOLATILE_RANGE', 'QUIET_RANGE'
            ]
            
            # Calculate trending and ranging percentages
            for regime_type in trending_regimes:
                result['trending_pct'] += regime_percentages.get(regime_type, 0)
            
            for regime_type in ranging_regimes:
                result['ranging_pct'] += regime_percentages.get(regime_type, 0)
        
        # Safety check to ensure percentages add up to something reasonable
        total_pct = result['trending_pct'] + result['ranging_pct']
        if total_pct < 1:  # Less than 1% is suspiciously low
            logger.warning(f"Total regime percentages ({total_pct}%) are too low, using defaults")
            # Default to ranging when data is inadequate
            result['ranging_pct'] = 100
            result['trending_pct'] = 0
        
        # Determine predominant regime
        result['predominant_regime'] = 'trending' if result['trending_pct'] > result['ranging_pct'] else 'ranging'
        
        logger.debug(f"Final regime distribution: {result}")
        return result
    
    # Execute the inner function with error handling
    return _determine_regime()
