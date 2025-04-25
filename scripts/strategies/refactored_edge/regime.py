import pandas as pd
import numpy as np

# ==============================================================================
# Market Regime Detection Functions
# ==============================================================================

def determine_market_regime(adx: pd.Series, threshold: float) -> pd.Series:
    """Determines the market regime based on the ADX indicator.

    Args:
        adx (pd.Series): Average Directional Index (ADX) values.
        threshold (float): The ADX level above which the market is considered trending.

    Returns:
        pd.Series: A series with values 'trending' or 'ranging'.
    """
    regime = pd.Series(np.where(adx >= threshold, 'trending', 'ranging'), index=adx.index)
    return regime

# TODO:
# 1. Consider adding more sophisticated regime detection methods if needed
#    (e.g., combining ADX with volatility measures).
# 2. Implement specific logic or filters based on the detected regime, potentially
#    as separate functions called by the main strategy class.

print("Market regime functions loaded.")
