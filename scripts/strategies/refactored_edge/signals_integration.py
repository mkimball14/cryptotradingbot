"""
Signal Generation Integration module for Edge Multi-Factor Strategy.

This module provides a centralized interface for generating trading signals
using different strictness levels (strict, balanced, relaxed) to optimize
the trade-off between signal quantity and quality.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

from scripts.strategies.refactored_edge.balanced_signals import (
    generate_balanced_signals,
    SignalStrictness
)

# Import original signals module for strict signals
from scripts.strategies.refactored_edge.signals import generate_edge_signals as generate_strict_signals

# Import enhanced indicators for regime detection
from scripts.strategies.refactored_edge.enhanced_indicators import (
    detect_enhanced_regime,
    add_pattern_recognition,
    add_volatility_indicators,
    adaptive_parameter_mapping
)

from scripts.strategies.refactored_edge.wfo_utils import is_testing_mode

# Configure logging
logger = logging.getLogger(__name__)


def generate_signals(
    close: pd.Series,
    rsi: pd.Series,
    bb_upper: pd.Series,
    bb_lower: pd.Series,
    trend_ma: pd.Series,
    price_in_demand_zone: Optional[pd.Series],
    price_in_supply_zone: Optional[pd.Series],
    params: Dict[str, Any],
    data: Optional[pd.DataFrame] = None,  # Full dataset for enhanced regime detection
    min_signal_threshold: int = 5
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Centralized signal generation function that handles signal generation
    based on the specified strictness level, regime information, and testing mode.
    
    Features automatic progression to more relaxed signal modes when insufficient signals
    are generated with current parameters.
    
    Args:
        close: Series of closing prices
        rsi: Series of RSI values
        bb_upper: Series of Bollinger Bands upper values
        bb_lower: Series of Bollinger Bands lower values
        trend_ma: Series of trend-defining moving average values
        price_in_demand_zone: Boolean series indicating price is in a demand zone
        price_in_supply_zone: Boolean series indicating price is in a supply zone
        params: Dictionary of strategy parameters
        data: Full dataset for enhanced regime detection
        min_signal_threshold: Minimum number of total signals required before attempting more relaxed mode
    
    Returns:
        tuple: (long_entries, long_exits, short_entries, short_exits)
    """
    # Extract parameters with defaults
    rsi_lower_threshold = params.get('rsi_lower_threshold', 30)
    rsi_upper_threshold = params.get('rsi_upper_threshold', 70)
    use_zones = params.get('use_zones', False)
    trend_strict = params.get('trend_strict', True)
    min_hold_period = params.get('min_hold_period', 2)
    trend_threshold_pct = params.get('trend_threshold_pct', 0.01)
    zone_influence = params.get('zone_influence', 0.5)
    use_regime_filter = params.get('use_regime_filter', False)
    
    # Ensure zone data is available, create empty zone data if not
    if price_in_demand_zone is None or price_in_supply_zone is None:
        logger.info("Zone data not available, creating default False series")
        use_zones = False  # Force zones off if data not available
        price_in_demand_zone = pd.Series(False, index=close.index)
        price_in_supply_zone = pd.Series(False, index=close.index)
    
    # Get the strictness level from params or default to BALANCED
    signal_strictness = params.get('signal_strictness', SignalStrictness.BALANCED)
    
    # Check if testing mode is enabled via environment variable
    testing_mode = is_testing_mode()
    if testing_mode:
        logger.info(f"Using RELAXED signals due to testing mode environment variable")
        signal_strictness = SignalStrictness.RELAXED
    
    # Apply enhanced regime-specific parameter adjustments if regime filtering is enabled
    regime = None
    regime_strength = 0.5  # Default medium strength
    transition_signal = 0  # Default no transition
    
    if params.get('use_regime_adaptation', False) and data is not None:
        try:
            # Apply enhanced regime detection if not already done
            if 'regime_enhanced' not in data.columns:
                # Ensure we have all required indicators
                enhanced_data = data.copy()
                if not all(col in enhanced_data.columns for col in ['vhf', 'choppiness']):
                    enhanced_data = add_volatility_indicators(enhanced_data)
                if not all(col in enhanced_data.columns for col in ['pattern_strength', 'pattern_signal']):
                    enhanced_data = add_pattern_recognition(enhanced_data)
                
                # Run enhanced regime detection
                enhanced_data = detect_enhanced_regime(
                    enhanced_data,
                    vhf_threshold=params.get('vhf_threshold', 0.24),
                    choppy_threshold=params.get('choppy_threshold', 61.8),
                    adx_threshold=params.get('adx_threshold', 25.0),
                    pattern_threshold=params.get('pattern_threshold', 60)
                )
                
                # Extract regime information
                regime = enhanced_data['regime_enhanced']
                regime_strength = enhanced_data['regime_strength']
                transition_signal = enhanced_data['regime_transition_signal']
            else:
                # If already calculated, just extract the information
                regime = data['regime_enhanced']
                regime_strength = data['regime_strength']
                transition_signal = data['regime_transition_signal']
        except Exception as e:
            logger.warning(f"Enhanced regime detection failed: {str(e)}. Falling back to basic detection.")
            # Fallback to basic regime detection
            if 'adx' in params and params['adx'] is not None and isinstance(params['adx'], pd.Series):
                adx = params['adx']
                adx_high = adx > params.get('adx_threshold', 25.0)
                # TRENDING when ADX is high, RANGING otherwise
                regime = pd.Series(np.where(adx_high, 'TRENDING', 'RANGING'), index=close.index)
            else:
                # Simplest fallback: TRENDING when price above MA, RANGING otherwise
                price_above_ma = close > trend_ma
                regime = pd.Series(np.where(price_above_ma, 'TRENDING', 'RANGING'), index=close.index)

    # Adapt parameters based on regime
    if regime is not None:
        # Get the most recent regime classification
        current_regime = regime.iloc[-1] if not regime.empty else None
        current_strength = regime_strength.iloc[-1] if isinstance(regime_strength, pd.Series) and not regime_strength.empty else regime_strength
        current_transition = transition_signal.iloc[-1] if isinstance(transition_signal, pd.Series) and not transition_signal.empty else transition_signal
        
        # Adapt parameters for this regime with strength and transition information
        adapted_params = adapt_parameters_for_regime(current_regime, params, current_strength, current_transition)
        
        logger.info(f"Using regime-adapted parameters for {current_regime} market (strength: {current_strength:.2f})")
    else:
        # Use original parameters if no regime adaptation
        adapted_params = params.copy()
        logger.info("Using standard parameters (no regime adaptation)")
    
    # Update parameters with adapted values
    rsi_lower_threshold = adapted_params.get('rsi_entry_threshold', rsi_lower_threshold)
    rsi_upper_threshold = adapted_params.get('rsi_exit_threshold', rsi_upper_threshold)
    zone_influence = adapted_params.get('zone_influence', zone_influence)
    trend_threshold_pct = adapted_params.get('trend_threshold_pct', trend_threshold_pct)
    min_hold_period = adapted_params.get('min_hold_period', min_hold_period)
    trend_strict = False if adapted_params.get('regime', 'TRENDING') == 'RANGING' else True  # Enforce trend direction only in trending markets
    
    logger.debug(f"Enhanced regime parameters: rsi_lower={rsi_lower_threshold:.1f}, "
               f"rsi_upper={rsi_upper_threshold:.1f}, trend_threshold={trend_threshold_pct:.4f}, "
               f"hold_period={min_hold_period}, zone_influence={zone_influence:.2f}")
    
    logger.debug(f"Enhanced ranging market parameters: rsi_lower={rsi_lower_threshold:.1f}, "
                 f"rsi_upper={rsi_upper_threshold:.1f}, trend_threshold={trend_threshold_pct:.4f}, "
                 f"hold_period={min_hold_period}, zone_influence={zone_influence:.2f}")
    
    logger.info(f"Generating signals with strictness={signal_strictness}, "
                f"use_zones={use_zones}, trend_strict={trend_strict}")
    
    # Progressive signal generation with automatic fallback to more relaxed modes if needed
    # Start with the specified strictness level
    current_strictness = signal_strictness
    
    # Define strictness progression order
    strictness_levels = [
        SignalStrictness.BALANCED,
        SignalStrictness.RELAXED,
        SignalStrictness.ULTRA_RELAXED
    ]
    
    # If starting with STRICT, add it to the beginning
    if current_strictness == SignalStrictness.STRICT:
        strictness_levels.insert(0, SignalStrictness.STRICT)
    
    # Find the starting index in our progression
    try:
        start_index = strictness_levels.index(current_strictness)
    except ValueError:
        # Default to BALANCED if the strictness level is not in our progression
        start_index = 0
        current_strictness = strictness_levels[0]
    
    # Try progressively more relaxed signal generation if needed
    for i in range(start_index, len(strictness_levels)):
        current_strictness = strictness_levels[i]
        
        logger.info(f"Attempting signal generation with {current_strictness} mode")
        
        # Generate signals with current strictness level
        long_entries, long_exits, short_entries, short_exits = generate_balanced_signals(
            close=close,
            rsi=rsi,
            bb_upper=bb_upper,
            bb_lower=bb_lower,
            trend_ma=trend_ma,
            price_in_demand_zone=price_in_demand_zone,
            price_in_supply_zone=price_in_supply_zone,
            rsi_lower_threshold=rsi_lower_threshold,
            rsi_upper_threshold=rsi_upper_threshold,
            use_zones=use_zones,
            trend_strict=trend_strict,
            min_hold_period=min_hold_period,
            trend_threshold_pct=trend_threshold_pct,
            zone_influence=zone_influence,
            strictness=current_strictness
        )
        
        # Check if we have enough signals
        total_entries = long_entries.sum() + short_entries.sum()
        if total_entries >= min_signal_threshold:
            logger.info(f"Successfully generated {total_entries} entry signals with {current_strictness} mode")
            break
        
        if i < len(strictness_levels) - 1:
            next_strictness = strictness_levels[i + 1]
            logger.warning(f"No sufficient entry signals detected with {current_strictness} parameters! "
                         f"Only found {total_entries} entries. Trying {next_strictness} mode...")
        else:
            logger.warning(f"Even with {current_strictness} mode, only found {total_entries} entry signals")
    
    # Log signal counts for debugging
    logger.info(f"Final signal generation: {long_entries.sum()} long entries and {short_entries.sum()} short entries "
               f"with {current_strictness} mode")
    
    return long_entries, long_exits, short_entries, short_exits
