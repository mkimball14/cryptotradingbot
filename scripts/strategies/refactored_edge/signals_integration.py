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
    based on the specified strictness level or testing mode.
    
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
