import pandas as pd
import numpy as np
from enum import Enum
from typing import Optional, Tuple, Dict, List, Union, Any
import logging

logger = logging.getLogger(__name__)

# ==============================================================================
# Market Regime Detection Classes and Constants
# ==============================================================================

class MarketRegimeType(str, Enum):
    """Enum for different market regime types.
    
    This provides a standardized set of regime classifications that can be used
    throughout the codebase for consistency.    
    """
    # Basic regimes (for backward compatibility)
    TRENDING = 'trending'
    RANGING = 'ranging'
    
    # Advanced regimes (for enhanced classification)
    STRONG_UPTREND = 'strong_uptrend'
    WEAK_UPTREND = 'weak_uptrend'
    STRONG_DOWNTREND = 'strong_downtrend'
    WEAK_DOWNTREND = 'weak_downtrend'
    VOLATILE_RANGE = 'volatile_range'
    QUIET_RANGE = 'quiet_range'
    BREAKOUT = 'breakout'
    BREAKDOWN = 'breakdown'
    UNKNOWN = 'unknown'


# Default thresholds for regime detection
DEFAULT_ADX_THRESHOLD = 25.0
DEFAULT_VOLATILITY_THRESHOLD = 0.01  # 1% relative volatility (e.g., ATR/price)
DEFAULT_MOMENTUM_THRESHOLD = 0.005   # 0.5% price change over lookback
DEFAULT_STRONG_ADX_THRESHOLD = 35.0  # Strong trend threshold

# ==============================================================================
# Market Regime Detection Functions
# ==============================================================================

def determine_market_regime(adx: pd.Series, threshold: float = DEFAULT_ADX_THRESHOLD) -> pd.Series:
    """Determines the market regime based on the ADX indicator.

    Args:
        adx (pd.Series): Average Directional Index (ADX) values.
        threshold (float, optional): The ADX level above which the market is considered trending.
            Defaults to DEFAULT_ADX_THRESHOLD (25.0).

    Returns:
        pd.Series: A series with values 'trending' or 'ranging'.
    """
    regime = pd.Series(np.where(adx >= threshold, 'trending', 'ranging'), index=adx.index)
    return regime


def determine_market_regime_advanced(
    adx: pd.Series,
    plus_di: pd.Series,
    minus_di: pd.Series,
    atr: pd.Series,
    close: pd.Series,
    high: Optional[pd.Series] = None,
    low: Optional[pd.Series] = None,
    volume: Optional[pd.Series] = None,
    adx_threshold: float = DEFAULT_ADX_THRESHOLD,
    strong_adx_threshold: float = DEFAULT_STRONG_ADX_THRESHOLD,
    volatility_threshold: float = DEFAULT_VOLATILITY_THRESHOLD,
    momentum_lookback: int = 5,
    momentum_threshold: float = DEFAULT_MOMENTUM_THRESHOLD,
    use_enhanced_classification: bool = True
) -> pd.Series:
    """Determines the market regime using multiple indicators for a more nuanced classification.
    
    This function extends the basic trending/ranging classification by considering:
    1. ADX and directional indicators (DI+/DI-) for trend direction and strength
    2. Volatility (ATR relative to price) for distinguishing between quiet and volatile regimes
    3. Recent price momentum for detecting breakouts/breakdowns
    
    Args:
        adx (pd.Series): Average Directional Index (ADX) values.
        plus_di (pd.Series): Positive Directional Indicator (DI+) values.
        minus_di (pd.Series): Negative Directional Indicator (DI-) values.
        atr (pd.Series): Average True Range values for volatility.
        close (pd.Series): Close prices.
        high (pd.Series, optional): High prices, used for additional calculations.
        low (pd.Series, optional): Low prices, used for additional calculations.
        volume (pd.Series, optional): Volume data, used for additional confirmation.
        adx_threshold (float, optional): The ADX threshold for trend detection. 
            Defaults to DEFAULT_ADX_THRESHOLD (25.0).
        strong_adx_threshold (float, optional): Threshold for strong trend classification. 
            Defaults to DEFAULT_STRONG_ADX_THRESHOLD (35.0).
        volatility_threshold (float, optional): Relative volatility threshold (ATR/price). 
            Defaults to DEFAULT_VOLATILITY_THRESHOLD (0.01).
        momentum_lookback (int, optional): Period for momentum calculation. 
            Defaults to 5 periods.
        momentum_threshold (float, optional): Price change threshold for momentum detection. 
            Defaults to DEFAULT_MOMENTUM_THRESHOLD (0.005).
        use_enhanced_classification (bool, optional): Whether to use detailed regime 
            classification or fall back to basic trending/ranging. Defaults to True.
            
    Returns:
        pd.Series: A series with market regime classifications for each data point.
    """
    # Calculate relative volatility (ATR as percentage of price)
    relative_volatility = atr / close
    
    # Calculate momentum (percent change over lookback period)
    momentum = close.pct_change(periods=momentum_lookback)
    
    # Initialize with basic regime classification (for fallback)
    basic_regime = determine_market_regime(adx, adx_threshold)
    
    if not use_enhanced_classification:
        return basic_regime
    
    # Initialize the enhanced regime series
    enhanced_regime = pd.Series(MarketRegimeType.UNKNOWN, index=adx.index)
    
    # Create masks for different regime conditions
    is_trending = adx >= adx_threshold
    is_strong_trend = adx >= strong_adx_threshold
    is_uptrend = plus_di > minus_di
    is_downtrend = minus_di > plus_di
    is_volatile = relative_volatility >= volatility_threshold
    is_breakout = momentum >= momentum_threshold
    is_breakdown = momentum <= -momentum_threshold
    
    # Apply classification rules
    # Strong uptrend: High ADX, DI+ > DI-
    enhanced_regime[is_strong_trend & is_uptrend] = MarketRegimeType.STRONG_UPTREND
    
    # Weak uptrend: Moderate ADX, DI+ > DI-
    enhanced_regime[(is_trending & ~is_strong_trend) & is_uptrend] = MarketRegimeType.WEAK_UPTREND
    
    # Strong downtrend: High ADX, DI- > DI+
    enhanced_regime[is_strong_trend & is_downtrend] = MarketRegimeType.STRONG_DOWNTREND
    
    # Weak downtrend: Moderate ADX, DI- > DI+
    enhanced_regime[(is_trending & ~is_strong_trend) & is_downtrend] = MarketRegimeType.WEAK_DOWNTREND
    
    # Volatile range: Not trending, high volatility
    enhanced_regime[~is_trending & is_volatile] = MarketRegimeType.VOLATILE_RANGE
    
    # Quiet range: Not trending, low volatility
    enhanced_regime[~is_trending & ~is_volatile] = MarketRegimeType.QUIET_RANGE
    
    # Breakout/Breakdown: significant price movement regardless of current regime
    # These override other classifications when detected
    enhanced_regime[is_breakout] = MarketRegimeType.BREAKOUT
    enhanced_regime[is_breakdown] = MarketRegimeType.BREAKDOWN
    
    return enhanced_regime


def get_regime_specific_params(
    regimes: pd.Series,
    regime_params: Dict[str, Dict[str, Any]],
    default_params: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """Groups data points by regime and returns regime-specific parameters.
    
    This helper function is useful for applying different parameters to different
    market regimes when evaluating a strategy.
    
    Args:
        regimes (pd.Series): Series of market regime classifications.
        regime_params (Dict[str, Dict[str, Any]]): Dictionary mapping regime types to parameter sets.
        default_params (Dict[str, Any]): Default parameters to use for regimes not in regime_params.
        
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary with regime types as keys and parameters as values.
    """
    result = {}
    
    # Get unique regimes in the data
    unique_regimes = regimes.unique()
    
    # For each unique regime, get the appropriate parameters
    for regime in unique_regimes:
        if regime in regime_params:
            result[regime] = regime_params[regime]
        else:
            # Map advanced regimes to basic regimes if specific params not available
            if regime in (MarketRegimeType.STRONG_UPTREND, MarketRegimeType.WEAK_UPTREND) and \
               MarketRegimeType.TRENDING in regime_params:
                result[regime] = regime_params[MarketRegimeType.TRENDING]
            elif regime in (MarketRegimeType.STRONG_DOWNTREND, MarketRegimeType.WEAK_DOWNTREND) and \
                 MarketRegimeType.TRENDING in regime_params:
                result[regime] = regime_params[MarketRegimeType.TRENDING]
            elif regime in (MarketRegimeType.VOLATILE_RANGE, MarketRegimeType.QUIET_RANGE) and \
                 MarketRegimeType.RANGING in regime_params:
                result[regime] = regime_params[MarketRegimeType.RANGING]
            else:
                # Fall back to default parameters
                result[regime] = default_params
    
    return result


def simplify_regimes(enhanced_regimes: pd.Series) -> pd.Series:
    """Converts enhanced regime classifications to basic trending/ranging classification.
    
    This function is useful for backward compatibility with code that expects
    only trending or ranging classifications.
    
    Args:
        enhanced_regimes (pd.Series): Series with enhanced regime classifications.
        
    Returns:
        pd.Series: Series with simplified 'trending' or 'ranging' classifications.
    """
    # Create a mapping from enhanced to basic regimes
    regime_mapping = {
        MarketRegimeType.STRONG_UPTREND: MarketRegimeType.TRENDING,
        MarketRegimeType.WEAK_UPTREND: MarketRegimeType.TRENDING,
        MarketRegimeType.STRONG_DOWNTREND: MarketRegimeType.TRENDING,
        MarketRegimeType.WEAK_DOWNTREND: MarketRegimeType.TRENDING,
        MarketRegimeType.VOLATILE_RANGE: MarketRegimeType.RANGING,
        MarketRegimeType.QUIET_RANGE: MarketRegimeType.RANGING,
        MarketRegimeType.BREAKOUT: MarketRegimeType.TRENDING,
        MarketRegimeType.BREAKDOWN: MarketRegimeType.TRENDING,
        MarketRegimeType.UNKNOWN: MarketRegimeType.RANGING,
    }
    
    # Apply mapping with a fallback to original value if not in mapping
    return enhanced_regimes.map(lambda x: regime_mapping.get(x, x))


def detect_market_regimes(data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes market data and detects market regimes (trending vs ranging) for the entire dataset.
    
    This is a higher-level function that calculates necessary indicators if they don't exist
    in the input data and returns a dataframe with regime classifications.
    
    Supports both basic regime detection using ADX and enhanced regime detection using
    multiple indicators (VHF, Choppiness Index, ADX, pattern recognition).
    
    Args:
        data (pd.DataFrame): DataFrame containing OHLCV price data. Should include columns:
                           'open', 'high', 'low', 'close', 'volume'
                           For enhanced regime detection, should also include:
                           'vhf', 'choppiness', 'pattern_strength', 'pattern_signal'
    
    Returns:
        pd.DataFrame: DataFrame with the original data plus additional columns for regime information.
                     Includes 'regime', 'regime_simple', and potentially additional regime-related columns.
    """
    try:
        # Check if the data already has enhanced regime detection columns
        has_enhanced_regime_columns = all(col in data.columns for col in ['vhf', 'choppiness', 'pattern_strength', 'pattern_signal'])
        
        # Ensure we have the required indicators to determine regimes
        if 'adx' not in data.columns:
            # Import the indicators module to calculate missing indicators
            from scripts.strategies.refactored_edge import indicators
            
            # Calculate ADX and DI indicators if they don't exist
            adx_window = 14  # Default ADX window
            if 'adx' not in data.columns or 'plus_di' not in data.columns or 'minus_di' not in data.columns:
                adx_data = indicators.add_adx(data, adx_window)
                data['adx'] = adx_data['adx']
                data['plus_di'] = adx_data['plus_di']
                data['minus_di'] = adx_data['minus_di']
                
            # Calculate ATR if it doesn't exist
            atr_window = 14  # Default ATR window
            if 'atr' not in data.columns:
                atr_data = indicators.add_atr(data, atr_window)
                data['atr'] = atr_data['atr']
        
        # Check if we can use enhanced regime detection
        if has_enhanced_regime_columns:
            # Import enhanced_indicators module for advanced regime detection
            from scripts.strategies.refactored_edge.enhanced_indicators import detect_enhanced_regime
            
            logger.info("Using enhanced regime detection with multiple indicators")
            
            # Apply enhanced regime detection
            enhanced_regime_data = detect_enhanced_regime(
                data=data,
                vhf_threshold=0.24,  # Default threshold for Vertical Horizontal Filter
                choppy_threshold=61.8,  # Default threshold for Choppiness Index
                adx_threshold=25.0,  # Default threshold for ADX
                pattern_threshold=60  # Default threshold for pattern strength
            )
            
            # Copy enhanced regime columns to our data
            enhanced_regime_columns = [
                'regime_enhanced', 'regime_enhanced_numeric', 'regime_strength',
                'regime_transition_signal', 'regime_transition_direction'
            ]
            
            for col in enhanced_regime_columns:
                if col in enhanced_regime_data.columns:
                    data[col] = enhanced_regime_data[col]
            
            # Set the standard regime column to match enhanced regime
            data['regime'] = data['regime_enhanced']
            data['regime_simple'] = np.where(data['regime_enhanced'] == 'TRENDING', 'trending', 'ranging')
            
        else:
            # Use the standard market regime detection
            logger.info("Using standard regime detection with ADX only")
            
            # Determine market regimes using the advanced method
            regimes = determine_market_regime_advanced(
                adx=data['adx'],
                plus_di=data['plus_di'],
                minus_di=data['minus_di'],
                atr=data['atr'],
                close=data['close'],
                high=data['high'],
                low=data['low'],
                volume=data.get('volume', None),  # Volume is optional
                use_enhanced_classification=True
            )
            
            # Add the regimes to the data
            data['regime'] = regimes
            
            # Add simplified regimes (trending/ranging) for backward compatibility
            data['regime_simple'] = simplify_regimes(regimes)
        
        # Calculate percentage of time in each regime type
        regime_counts = data['regime_simple'].value_counts(normalize=True) * 100
        regime_percents = {regime: f"{percent:.2f}%" for regime, percent in regime_counts.items()}
        
        # Add metadata about the regime distribution
        data.attrs['regime_percentages'] = regime_percents
        data.attrs['predominant_regime'] = regime_counts.idxmax()
        
        return data
    
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error detecting market regimes: {e}")
        logger.info("Falling back to basic regime detection with ADX only")
        
        # Fallback to basic regime detection
        try:
            # Calculate ADX if it doesn't exist
            if 'adx' not in data.columns:
                from scripts.strategies.refactored_edge import indicators
                adx_data = indicators.add_adx(data)
                data['adx'] = adx_data['adx']
            
            # Use the simple regime detection method
            data['regime'] = determine_market_regime(data['adx'])
            data['regime_simple'] = data['regime']  # They're the same in this case
            
            # Calculate percentage of time in each regime type
            regime_counts = data['regime'].value_counts(normalize=True) * 100
            regime_percents = {regime: f"{percent:.2f}%" for regime, percent in regime_counts.items()}
            
            # Add metadata about the regime distribution
            data.attrs['regime_percentages'] = regime_percents
            data.attrs['predominant_regime'] = regime_counts.idxmax()
            
            return data
        except Exception as nested_e:
            logger.error(f"Fallback regime detection also failed: {nested_e}")
            # Create default regime data
            data['regime'] = pd.Series(MarketRegimeType.UNKNOWN, index=data.index)
            data['regime_simple'] = pd.Series(MarketRegimeType.RANGING, index=data.index)  # Default to ranging when uncertain
            data.attrs['regime_percentages'] = {MarketRegimeType.UNKNOWN: "100.00%"}
            data.attrs['predominant_regime'] = MarketRegimeType.RANGING
            return data

print("Market regime functions loaded.")
