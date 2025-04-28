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

# Local imports
from scripts.strategies.refactored_edge import regime
from scripts.strategies.refactored_edge.wfo_evaluation import evaluate_single_params


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


def determine_market_regime_for_params(data, regime_window=None):
    """
    Determine the market regime for the given data and add it to parameter information.
    
    Args:
        data (pd.DataFrame): The price data
        regime_window (int, optional): Window for regime calculation
        
    Returns:
        dict: Regime information including percentages and predominant regime
    """
    try:
        # Make sure we have the necessary indicators
        # We need adx, plus_di, minus_di, atr and close for regime detection
        if not all(col in data.columns for col in ['adx', 'plus_di', 'minus_di', 'atr']):
            print("Adding indicators for regime detection...")
            # Create a complete temporary config with all required attributes
            from scripts.strategies.refactored_edge import indicators
            temp_config = type('EdgeConfig', (), {})()
            # Standard indicator parameters
            temp_config.rsi_window = 14
            temp_config.bb_window = 20
            temp_config.bb_std_dev = 2.0
            temp_config.trend_ma_window = 50  # Different name from ma_window
            temp_config.atr_window = 14
            temp_config.atr_window_sizing = 14
            temp_config.adx_window = 14
            # Signal parameters
            temp_config.rsi_entry_threshold = 30
            temp_config.rsi_exit_threshold = 70
            # Disable zone calculations for simplicity
            temp_config.use_zones = False
            
            # Get indicators including ADX for regime detection
            indicator_df = indicators.add_indicators(data, temp_config)
            
            # Extract indicators (ensuring lowercase names)
            adx = indicator_df['adx']
            plus_di = indicator_df['plus_di']
            minus_di = indicator_df['minus_di']
            atr = indicator_df['atr']
        else:
            # Extract existing indicators
            adx = data['adx']
            plus_di = data['plus_di']
            minus_di = data['minus_di']
            atr = data['atr']
        
        # Use appropriate case for close price
        close = data.get('close', data.get('Close', None))
        if close is None:
            print("WARNING: Close price not found for regime detection")
            return {'trending_pct': 0, 'ranging_pct': 100, 'predominant_regime': 'ranging'}
        
        # Determine market regime (using regime.py's function)
        # Check if we should use the advanced regime detection or the simple one
        if hasattr(temp_config, 'use_enhanced_regimes') and temp_config.use_enhanced_regimes:
            # Use advanced regime detection with all indicators
            regimes = regime.determine_market_regime_advanced(
                adx=adx,
                plus_di=plus_di, 
                minus_di=minus_di,
                atr=atr,
                close=close,
                threshold=temp_config.adx_threshold if hasattr(temp_config, 'adx_threshold') else 25.0,
                strong_threshold=temp_config.strong_adx_threshold if hasattr(temp_config, 'strong_adx_threshold') else 35.0,
                volatility_threshold=temp_config.volatility_threshold if hasattr(temp_config, 'volatility_threshold') else 0.01
            )
        else:
            # Use simple regime detection with just ADX
            regimes = regime.determine_market_regime(
                adx=adx,
                threshold=temp_config.adx_threshold if hasattr(temp_config, 'adx_threshold') else 25.0
            )
        
        # Calculate percentage of each regime
        total_periods = len(regimes)
        if total_periods == 0:
            return {'trending_pct': 0, 'ranging_pct': 100, 'predominant_regime': 'ranging'}
            
        trending_periods = (regimes == 'trending').sum()
        ranging_periods = (regimes == 'ranging').sum()
        
        trending_pct = 100 * trending_periods / total_periods
        ranging_pct = 100 * ranging_periods / total_periods
        
        # Determine the predominant regime (for simplicity, just use majority)
        predominant = 'trending' if trending_pct > ranging_pct else 'ranging'
        
        return {
            'trending_pct': trending_pct,
            'ranging_pct': ranging_pct,
            'predominant_regime': predominant
        }
        
    except Exception as e:
        print(f"Error detecting market regime: {str(e)}")
        traceback.print_exc()
        # Default to ranging (it's usually the safer assumption)
        return {'trending_pct': 0, 'ranging_pct': 100, 'predominant_regime': 'ranging'}
