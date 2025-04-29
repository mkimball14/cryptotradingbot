"""
Signal Generation Integration module for Edge Multi-Factor Strategy.

This module provides a centralized interface for generating trading signals
using different strictness levels (strict, balanced, relaxed) to optimize
the trade-off between signal quantity and quality.
"""

import logging
import pandas as pd
from typing import Tuple, Dict, Any, Optional

# Local imports
from scripts.strategies.refactored_edge import signals, test_signals, balanced_signals
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
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
    params: Dict[str, Any]
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Centralized signal generation function that handles signal generation
    based on the specified strictness level, regime information, and testing mode.
    
    Args:
        close: Series of closing prices
        rsi: Series of RSI values
        bb_upper: Series of Bollinger Bands upper values
        bb_lower: Series of Bollinger Bands lower values
        trend_ma: Series of trend-defining moving average values
        price_in_demand_zone: Boolean series indicating price is in a demand zone
        price_in_supply_zone: Boolean series indicating price is in a supply zone
        params: Dictionary of strategy parameters
    
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
    
    # Apply regime-specific parameter adjustments if regime filtering is enabled
    if use_regime_filter and '_regime_info' in params:
        # Get regime information
        regime_info = params.get('_regime_info', {})
        predominant_regime = regime_info.get('predominant_regime', 'ranging')
        trending_pct = regime_info.get('trending_pct', 50)
        ranging_pct = regime_info.get('ranging_pct', 50)
        
        # Log regime information
        logger.info(f"Applying regime-specific adjustments for {predominant_regime} market "  
                   f"(trending: {trending_pct:.1f}%, ranging: {ranging_pct:.1f}%)")
        
        # Adjust parameters based on predominant market regime
        if predominant_regime == 'trending':
            # In trending markets:
            # - Use wider RSI thresholds to avoid premature exits
            # - Enforce trend direction more strictly
            # - Use longer hold periods to capture trends
            rsi_lower_threshold = max(25, rsi_lower_threshold - 5)  # More aggressive entry
            rsi_upper_threshold = min(75, rsi_upper_threshold + 5)  # Less aggressive exit
            trend_strict = True  # Always respect trend
            min_hold_period = max(min_hold_period, 3)  # Hold longer in trends
            zone_influence = min(0.3, zone_influence)  # Reduce zone influence in trending markets
            
            logger.debug(f"Adjusted parameters for trending market: rsi_lower={rsi_lower_threshold}, "  
                        f"rsi_upper={rsi_upper_threshold}, hold_period={min_hold_period}")
            
        else:  # ranging regime
            # In ranging markets:
            # - Use tighter RSI thresholds for more selective entries/exits
            # - Reduce trend strictness to allow counter-trend trades
            # - Use shorter hold periods to capture reversals
            rsi_lower_threshold = min(35, rsi_lower_threshold + 5)  # More selective entry
            rsi_upper_threshold = max(65, rsi_upper_threshold - 5)  # More selective exit
            trend_strict = False  # Allow counter-trend trades in ranges
            min_hold_period = min(min_hold_period, 2)  # Hold shorter in ranges
            zone_influence = max(0.7, zone_influence)  # Increase zone influence in ranging markets
            
            logger.debug(f"Adjusted parameters for ranging market: rsi_lower={rsi_lower_threshold}, "  
                        f"rsi_upper={rsi_upper_threshold}, hold_period={min_hold_period}")
    
    logger.info(f"Generating signals with strictness={signal_strictness}, "
                f"use_zones={use_zones}, trend_strict={trend_strict}")
    
    # Use the balanced_signals module with appropriate strictness setting
    long_entries, long_exits, short_entries, short_exits = balanced_signals.generate_balanced_signals(
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
        strictness=signal_strictness
    )
    
    # Log signal counts for debugging
    logger.debug(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries "
                 f"with {signal_strictness} mode")
    
    return long_entries, long_exits, short_entries, short_exits
