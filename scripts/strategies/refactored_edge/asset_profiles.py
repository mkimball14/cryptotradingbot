"""
Asset-specific configuration and volatility profiling module.

This module provides functionality to analyze cryptocurrency assets based on their
volatility characteristics and recommend optimal signal generation parameters for each asset.
The goal is to customize the trading strategy's behavior for different types of assets,
improving performance across the portfolio.
"""

import os
import json
import logging
from enum import Enum
from typing import Dict, Optional, Any, List, Tuple
from pathlib import Path

import pandas as pd
import numpy as np
from pydantic import BaseModel, Field

from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
import talib

# Configure logging
logger = logging.getLogger(__name__)

# Determine project root for data storage
try:
    from scripts.strategies.refactored_edge.wfo_utils import PROJECT_ROOT
    project_root = PROJECT_ROOT
except ImportError:
    # Fallback if not available
    project_root = Path(__file__).parents[4]


class VolatilityProfile(str, Enum):
    """Classification of cryptocurrency assets by their volatility characteristics."""
    LOW = "low"           # Lower volatility assets like stablecoins or BTC in certain regimes
    MEDIUM = "medium"     # Average volatility assets like ETH, BTC (typical)
    HIGH = "high"         # Higher volatility assets like altcoins
    EXTREME = "extreme"   # Extremely volatile assets or assets in volatile market conditions


class AssetConfig(BaseModel):
    """Asset-specific configuration parameters."""
    symbol: str
    volatility_profile: VolatilityProfile
    avg_daily_volatility: float = Field(..., description="Average daily volatility (ATR/price)")
    signal_strictness: SignalStrictness
    trend_threshold_pct: float = Field(..., description="% distance from MA to consider in trend")
    zone_influence: float = Field(..., description="How strongly zones influence signals (0-1)")
    min_hold_period: int = Field(..., description="Minimum holding period in bars")
    
    # Metrics for strategy validation (optional)
    avg_trades_per_month: Optional[float] = None
    win_rate: Optional[float] = None
    expected_drawdown: Optional[float] = None


def calculate_atr(ohlc_data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range (ATR) for volatility analysis.
    
    Args:
        ohlc_data: DataFrame with OHLC data
        period: Period for ATR calculation
        
    Returns:
        Series with ATR values
    """
    # Handle different column naming conventions
    if 'high' in ohlc_data.columns:
        high = ohlc_data['high'].values
        low = ohlc_data['low'].values
        close = ohlc_data['close'].values
    else:  # Handle uppercase column names
        high = ohlc_data['High'].values
        low = ohlc_data['Low'].values
        close = ohlc_data['Close'].values
    
    # Calculate ATR using talib
    atr = talib.ATR(high, low, close, timeperiod=period)
    return pd.Series(atr, index=ohlc_data.index)


def analyze_asset_volatility(
    ohlc_data: pd.DataFrame,
    atr_window: int = 14,
    analysis_period_days: int = 90,
    volatility_thresholds: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Analyze asset volatility characteristics from historical price data.
    
    Args:
        ohlc_data: DataFrame with OHLCV data
        atr_window: Window period for ATR calculation
        analysis_period_days: Number of days to analyze
        volatility_thresholds: Optional custom thresholds for volatility classification
        
    Returns:
        Dict with volatility metrics including:
        - avg_daily_volatility: Average daily volatility (ATR/price)
        - volatility_profile: Classified volatility profile (LOW, MEDIUM, HIGH, EXTREME)
        - volatility_regime_distribution: Percentage of time in different volatility regimes
    """
    # Default thresholds if not provided
    if volatility_thresholds is None:
        volatility_thresholds = {
            "low_threshold": 0.01,     # 1% daily volatility
            "medium_threshold": 0.02,  # 2% daily volatility
            "high_threshold": 0.04     # 4% daily volatility
        }
    
    # Calculate ATR
    atr = calculate_atr(ohlc_data, atr_window)
    
    # Calculate relative volatility (ATR as percentage of price)
    close = ohlc_data['close']
    relative_volatility = atr / close
    
    # Calculate average volatility
    avg_volatility = relative_volatility.mean()
    
    # Classify based on average volatility
    if avg_volatility < volatility_thresholds["low_threshold"]:
        profile = VolatilityProfile.LOW
    elif avg_volatility < volatility_thresholds["medium_threshold"]:
        profile = VolatilityProfile.MEDIUM
    elif avg_volatility < volatility_thresholds["high_threshold"]:
        profile = VolatilityProfile.HIGH
    else:
        profile = VolatilityProfile.EXTREME
    
    # Calculate volatility regime distribution
    low_vol_pct = (relative_volatility < volatility_thresholds["low_threshold"]).mean() * 100
    medium_vol_pct = ((relative_volatility >= volatility_thresholds["low_threshold"]) & 
                      (relative_volatility < volatility_thresholds["medium_threshold"])).mean() * 100
    high_vol_pct = ((relative_volatility >= volatility_thresholds["medium_threshold"]) & 
                   (relative_volatility < volatility_thresholds["high_threshold"])).mean() * 100
    extreme_vol_pct = (relative_volatility >= volatility_thresholds["high_threshold"]).mean() * 100
    
    return {
        "avg_daily_volatility": avg_volatility,
        "volatility_profile": profile,
        "volatility_regime_distribution": {
            "low_volatility_pct": low_vol_pct,
            "medium_volatility_pct": medium_vol_pct,
            "high_volatility_pct": high_vol_pct, 
            "extreme_volatility_pct": extreme_vol_pct
        }
    }


def recommend_signal_parameters(
    volatility_profile: VolatilityProfile,
    avg_daily_volatility: float
) -> Dict[str, Any]:
    """
    Recommend signal generation parameters based on asset volatility profile.
    
    Different assets require different signal strictness and parameters:
    - Low volatility assets: More aggressive (RELAXED) signals to capture smaller moves
    - Medium volatility assets: Balanced approach
    - High/Extreme volatility assets: More conservative (STRICT) signals to filter noise
    
    Args:
        volatility_profile: Classified volatility profile
        avg_daily_volatility: Average daily volatility metric
        
    Returns:
        Dict with recommended parameters:
        - signal_strictness: Recommended SignalStrictness level
        - trend_threshold_pct: Recommended trend threshold
        - zone_influence: Recommended zone influence
        - min_hold_period: Recommended minimum hold period
    """
    # Base parameters dictionary
    params = {}
    
    # Set signal strictness based on volatility profile
    if volatility_profile == VolatilityProfile.LOW:
        # Low volatility assets need more signals (less strict)
        params["signal_strictness"] = SignalStrictness.RELAXED
        params["trend_threshold_pct"] = 0.005  # 0.5% threshold (more sensitive)
        params["zone_influence"] = 0.3  # Lower zone influence (more signals)
        params["min_hold_period"] = 1  # Shorter hold period
        
    elif volatility_profile == VolatilityProfile.MEDIUM:
        # Medium volatility assets use balanced approach
        params["signal_strictness"] = SignalStrictness.BALANCED
        params["trend_threshold_pct"] = 0.01  # 1% threshold
        params["zone_influence"] = 0.5  # Moderate zone influence
        params["min_hold_period"] = 2  # Standard hold period
        
    elif volatility_profile == VolatilityProfile.HIGH:
        # High volatility assets need stronger filters
        params["signal_strictness"] = SignalStrictness.BALANCED
        params["trend_threshold_pct"] = 0.02  # 2% threshold (less sensitive)
        params["zone_influence"] = 0.7  # Higher zone influence (fewer signals)
        params["min_hold_period"] = 3  # Longer hold period
        
    else:  # EXTREME
        # Extreme volatility needs strictest filters
        params["signal_strictness"] = SignalStrictness.STRICT
        params["trend_threshold_pct"] = 0.03  # 3% threshold (much less sensitive)
        params["zone_influence"] = 0.9  # Very high zone influence (few signals)
        params["min_hold_period"] = 4  # Much longer hold period
    
    return params


def load_asset_profile(symbol: str) -> Optional[AssetConfig]:
    """
    Load asset profile from storage.
    
    Args:
        symbol: Trading symbol to load profile for
        
    Returns:
        AssetConfig if found, None otherwise
    """
    # Determine profile storage directory
    profiles_dir = Path(project_root) / 'data' / 'asset_profiles'
    os.makedirs(profiles_dir, exist_ok=True)
    
    # Normalized filename
    filename = f"{symbol.replace('-', '_').lower()}_profile.json"
    profile_path = profiles_dir / filename
    
    if not profile_path.exists():
        return None
    
    try:
        with open(profile_path, 'r') as f:
            profile_data = json.load(f)
        
        # Convert string enum values to enum objects
        if 'volatility_profile' in profile_data:
            profile_data['volatility_profile'] = VolatilityProfile(profile_data['volatility_profile'])
        if 'signal_strictness' in profile_data:
            profile_data['signal_strictness'] = SignalStrictness(profile_data['signal_strictness'])
            
        return AssetConfig(**profile_data)
    except Exception as e:
        logger.error(f"Error loading asset profile for {symbol}: {e}")
        return None


def save_asset_profile(asset_config: AssetConfig) -> bool:
    """
    Save asset profile to storage.
    
    Args:
        asset_config: AssetConfig to save
        
    Returns:
        True if successful, False otherwise
    """
    # Determine profile storage directory
    profiles_dir = Path(project_root) / 'data' / 'asset_profiles'
    os.makedirs(profiles_dir, exist_ok=True)
    
    # Normalized filename
    symbol = asset_config.symbol
    filename = f"{symbol.replace('-', '_').lower()}_profile.json"
    profile_path = profiles_dir / filename
    
    try:
        # Convert to dict, ensuring enums are serialized as strings
        profile_dict = asset_config.model_dump()
        
        with open(profile_path, 'w') as f:
            json.dump(profile_dict, f, indent=2)
        
        logger.info(f"Saved asset profile for {symbol}")
        return True
    except Exception as e:
        logger.error(f"Error saving asset profile for {symbol}: {e}")
        return False


def get_asset_specific_config(
    symbol: str,
    base_config: Optional[EdgeConfig] = None,
    historical_data: Optional[pd.DataFrame] = None,
    override_params: Optional[Dict[str, Any]] = None
) -> EdgeConfig:
    """
    Create an asset-specific configuration based on volatility profile.
    
    This function will either analyze provided historical data to determine
    optimal parameters, or load pre-calculated asset profiles if available.
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        base_config: Optional base configuration to extend
        historical_data: Optional historical data for volatility analysis
        override_params: Optional parameters to override recommendations
        
    Returns:
        EdgeConfig with asset-specific optimal parameters
    """
    # Start with base config or create default
    config_dict = {}
    if base_config:
        config_dict = base_config.model_dump()
    
    # Try to load asset profile from storage if available
    asset_profile = load_asset_profile(symbol)
    
    # If no stored profile and historical data provided, analyze it
    if asset_profile is None and historical_data is not None:
        # Analyze volatility
        volatility_metrics = analyze_asset_volatility(historical_data)
        
        # Get recommended parameters
        recommended_params = recommend_signal_parameters(
            volatility_metrics["volatility_profile"],
            volatility_metrics["avg_daily_volatility"]
        )
        
        # Create and save asset profile for future use
        asset_profile = AssetConfig(
            symbol=symbol,
            volatility_profile=volatility_metrics["volatility_profile"],
            avg_daily_volatility=volatility_metrics["avg_daily_volatility"],
            **recommended_params
        )
        save_asset_profile(asset_profile)
    
    # If we have an asset profile, update config with recommended parameters
    if asset_profile:
        # Update config with asset-specific parameters
        config_dict.update({
            "signal_strictness": asset_profile.signal_strictness,
            "trend_threshold_pct": asset_profile.trend_threshold_pct,
            "zone_influence": asset_profile.zone_influence,
            "min_hold_period": asset_profile.min_hold_period,
        })
        
        logger.info(f"Applied asset-specific parameters for {symbol} "
                   f"(Volatility: {asset_profile.volatility_profile}, "
                   f"Strictness: {asset_profile.signal_strictness})")
    else:
        logger.warning(f"No asset profile available for {symbol}, using default parameters")
    
    # Apply any override parameters
    if override_params:
        config_dict.update(override_params)
    
    # Create EdgeConfig from parameters dictionary
    return EdgeConfig(**config_dict)


def analyze_common_crypto_assets() -> List[AssetConfig]:
    """
    Pre-analyze common cryptocurrency assets and create standard profiles.
    
    This is useful for projects that don't have extensive historical data.
    Returns predefined profiles based on typical crypto asset behavior.
    
    Returns:
        List of AssetConfig objects for common crypto assets
    """
    # Predefined profiles based on typical crypto behavior
    # These can be refined based on actual analysis of historical data
    profiles = [
        # Majors
        AssetConfig(
            symbol="BTC-USD",
            volatility_profile=VolatilityProfile.MEDIUM,
            avg_daily_volatility=0.018,  # 1.8% typical
            signal_strictness=SignalStrictness.BALANCED,
            trend_threshold_pct=0.01,
            zone_influence=0.5,
            min_hold_period=2
        ),
        AssetConfig(
            symbol="ETH-USD",
            volatility_profile=VolatilityProfile.MEDIUM,
            avg_daily_volatility=0.025,  # 2.5% typical
            signal_strictness=SignalStrictness.BALANCED,
            trend_threshold_pct=0.015,
            zone_influence=0.6,
            min_hold_period=2
        ),
        # Large Altcoins
        AssetConfig(
            symbol="SOL-USD",
            volatility_profile=VolatilityProfile.HIGH,
            avg_daily_volatility=0.035,  # 3.5% typical
            signal_strictness=SignalStrictness.BALANCED,
            trend_threshold_pct=0.02,
            zone_influence=0.7,
            min_hold_period=3
        ),
        # Mid-cap Altcoins
        AssetConfig(
            symbol="LINK-USD",
            volatility_profile=VolatilityProfile.HIGH,
            avg_daily_volatility=0.038,  # 3.8% typical
            signal_strictness=SignalStrictness.BALANCED,
            trend_threshold_pct=0.025,
            zone_influence=0.75,
            min_hold_period=3
        ),
        # Small-cap/Newer assets
        AssetConfig(
            symbol="AVAX-USD",
            volatility_profile=VolatilityProfile.EXTREME,
            avg_daily_volatility=0.045,  # 4.5% typical
            signal_strictness=SignalStrictness.STRICT,
            trend_threshold_pct=0.03,
            zone_influence=0.8,
            min_hold_period=4
        ),
    ]
    
    return profiles


def generate_and_save_default_profiles() -> None:
    """
    Generate and save default profiles for common crypto assets.
    
    This is a utility function to initialize the asset profile system
    with sensible defaults for common trading pairs.
    """
    profiles = analyze_common_crypto_assets()
    for profile in profiles:
        save_asset_profile(profile)
    logger.info(f"Generated and saved {len(profiles)} default asset profiles")


if __name__ == "__main__":
    # Setup basic logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Generate default profiles
    generate_and_save_default_profiles()
    
    # Example of loading an asset profile
    btc_profile = load_asset_profile("BTC-USD")
    if btc_profile:
        print(f"Loaded BTC profile: {btc_profile}")
    
    # Example parameters for BTC
    print("Recommended parameters for BTC:", recommend_signal_parameters(
        VolatilityProfile.MEDIUM, 0.018
    ))
    
    # Example of asset-specific config
    config = get_asset_specific_config("BTC-USD")
    print("BTC-specific config:", config)
