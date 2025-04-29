import pandas as pd # Added for type hinting in get_param_combinations
import vectorbtpro as vbt # Added to resolve NameError
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict

# Import SignalStrictness from balanced_signals
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness

# Global Constants (Consider moving these to a central config file if used across strategies)
COMMISSION_PCT = 0.001 # Example commission per trade
SLIPPAGE_PCT = 0.0005   # Example slippage per trade
INITIAL_CAPITAL = 10000 # Default initial capital
DEFAULT_RISK_PER_TRADE = 0.02 # Default risk percentage per trade

# ==============================================================================
# Edge Strategy Configuration Model
# ==============================================================================

class EdgeConfig(BaseModel):
    """
    Configuration settings for the Edge Multi-Factor Strategy.
    Uses Pydantic for validation and type hinting.
    """
    # --- Data/General Parameters ---
    granularity_str: str = Field(default="1h", description="Data granularity string (e.g., '1h', '4h', '1d').")

    # --- Indicator Parameters ---
    rsi_window: int = Field(default=14, description="Window period for RSI calculation.")
    bb_window: int = Field(default=20, description="Window period for Bollinger Bands calculation.")
    bb_std_dev: float = Field(default=2.0, description="Standard deviation multiplier for Bollinger Bands.")
    trend_ma_window: int = Field(default=50, description="Window period for the trend-following Simple Moving Average.")
    trend_strict: bool = Field(default=True, description="If True, requires price > SMA for longs and price < SMA for shorts.")
    atr_window: int = Field(default=14, description="Window period for ATR calculation (used for stops).")
    atr_window_sizing: int = Field(default=14, description="Window period for ATR calculation (used for sizing - can differ from stop ATR).")
    
    # --- Market Regime Parameters ---
    adx_window: int = Field(default=14, description="Window period for ADX calculation (market regime detection).")
    adx_threshold: float = Field(default=25.0, description="ADX threshold above which market is considered trending.")
    strong_adx_threshold: float = Field(default=35.0, description="Threshold for strong trend classification.")
    volatility_threshold: float = Field(default=0.01, description="Relative volatility threshold (ATR/price) for regime detection.")
    momentum_lookback: int = Field(default=5, description="Period for momentum calculation in regime detection.")
    momentum_threshold: float = Field(default=0.005, description="Price change threshold for momentum-based regime detection.")
    use_regime_filter: bool = Field(default=False, description="Whether to filter signals based on market regime.")
    use_enhanced_regimes: bool = Field(default=False, description="Whether to use advanced multi-factor regime detection.")
    use_regime_adaptation: bool = Field(default=False, description="Whether to dynamically adapt parameters based on detected regime.")

    # --- Entry/Exit Thresholds ---
    rsi_entry_threshold: int = Field(default=30, description="RSI level below which long entries are considered.")
    rsi_exit_threshold: int = Field(default=70, description="RSI level above which long exits are considered.")
    # Add thresholds for short side if strategy includes shorts (e.g., rsi_short_entry > 70, rsi_short_exit < 30)

    # --- Supply/Demand Zone Parameters ---
    use_zones: bool = Field(default=True, description="Whether to use Supply/Demand zone analysis.")
    pivot_lookback: int = Field(default=10, description="Lookback period (candles) to identify pivot points.")
    pivot_prominence: float = Field(default=0.01, description="Minimum price difference (as fraction) for a pivot to be significant.") # Changed from int to float
    zone_merge_proximity: float = Field(default=0.005, description="Proximity (as price fraction) within which zones should be merged.")
    min_zone_width_candles: int = Field(default=5, description="Minimum number of candles a zone must span.")
    
    # --- Signal Generation Parameters ---
    signal_strictness: SignalStrictness = Field(
        default=SignalStrictness.BALANCED, 
        description="Controls the strictness of signal generation (STRICT, BALANCED, RELAXED).")
    trend_threshold_pct: float = Field(
        default=0.01, 
        description="Percentage threshold for trend determination in balanced signal mode.")
    zone_influence: float = Field(
        default=0.5, 
        description="Strength of zone influence from 0-1 in balanced signal mode.")
    min_hold_period: int = Field(
        default=2, 
        description="Minimum holding period in bars for balanced signal mode.")
    min_zone_strength: int = Field(default=2, description="Minimum number of pivots required to form a zone.")
    zone_extend_candles: int = Field(default=50, description="How many future candles to extend the zone visualization/analysis.")
    zone_proximity_pct: float = Field(default=0.001, description="Percentage distance from price to zone edge to consider 'near'.") # 0.1%

    # --- Risk Management Parameters ---
    pct_risk_per_trade: float = Field(default=DEFAULT_RISK_PER_TRADE, description="Maximum percentage of capital to risk on a single trade.")
    # Use ATR-based stops instead of fixed percentage
    use_atr_stops: bool = Field(default=True, description="Whether to use ATR-based stop-loss and take-profit.")
    sl_atr_multiplier: float = Field(default=1.5, description="Multiplier for ATR to set stop-loss distance.") 
    tp_atr_multiplier: float = Field(default=3.0, description="Multiplier for ATR to set take-profit distance.") 

    # --- Fees and Slippage ---
    commission_pct: float = Field(default=COMMISSION_PCT, description="Commission percentage per trade.") 
    slippage_pct: float = Field(default=SLIPPAGE_PCT, description="Slippage percentage per trade.") 

    # --- Meta Parameters ---
    initial_capital: float = Field(default=INITIAL_CAPITAL, description="Initial capital for backtesting.")

    # --- Validators (Optional but Recommended) ---
    @field_validator('rsi_window', 'bb_window', 'trend_ma_window', 'atr_window', 'atr_window_sizing', 'pivot_lookback', 'min_zone_width_candles', 'min_zone_strength', 'zone_extend_candles', mode='after')
    def check_positive_integer(cls, value):
        if value <= 0:
            raise ValueError("Window/Lookback/Count parameters must be positive integers")
        return value

    @field_validator('bb_std_dev', 'pivot_prominence', 'zone_merge_proximity', 'zone_proximity_pct', 'pct_risk_per_trade', 'sl_atr_multiplier', 'tp_atr_multiplier', 'commission_pct', 'slippage_pct', mode='after')
    def check_positive_float(cls, value):
        if value <= 0:
            raise ValueError("Multiplier/Percentage/Threshold parameters must be positive floats")
        return value

    @field_validator('rsi_entry_threshold', 'rsi_exit_threshold', mode='after')
    def check_rsi_thresholds(cls, value):
        if not (0 < value < 100):
            raise ValueError(f"Value must be positive")
        return value
        
    def get_param_combinations(self):
        """Return a list of parameter combinations for optimization.
        
        This provides access to the parameter grid for WFO optimization.
        For testing, we'll use a simplified grid with all required parameters.
        
        Returns:
            list: List of parameter dictionaries for testing
        """
        # For testing, create a simplified parameter grid with all required fields
        test_params = [
            {
                # Required indicator parameters
                'rsi_window': 14,
                'bb_window': 20,
                'bb_std_dev': 2.0,
                'ma_window': 50,  # Also known as trend_window
                'atr_window': 14,
                
                # Signal parameters
                'rsi_entry_threshold': 30,
                'rsi_exit_threshold': 70,
                
                # Regime parameters
                'adx_window': 14,
                'adx_threshold': 25.0,
                'use_regime_filter': self.use_regime_adaptation,
                'use_enhanced_regimes': self.use_enhanced_regimes
            },
            {
                # Required indicator parameters
                'rsi_window': 14,
                'bb_window': 20,
                'bb_std_dev': 2.0,
                'ma_window': 50,
                'atr_window': 14,
                
                # Signal parameters
                'rsi_entry_threshold': 40,
                'rsi_exit_threshold': 60,
                
                # Regime parameters
                'adx_window': 14,
                'adx_threshold': 25.0,
                'use_regime_filter': self.use_regime_adaptation,
                'use_enhanced_regimes': self.use_enhanced_regimes
            }
        ]
        return test_params

    @model_validator(mode='after')
    def check_rsi_entry_exit_logic(self):
        if self.rsi_entry_threshold >= self.rsi_exit_threshold:
            raise ValueError("RSI entry threshold must be less than RSI exit threshold")
        # Add checks for short thresholds if implemented
        return self

    # Example method to get parameters as a dictionary (useful for vbt)
    def get_param_dict(self) -> dict:
        """Returns the configuration as a dictionary suitable for vbt functions."""
        return self.model_dump()

# ==============================================================================
# Optimization Parameter Grid (for vectorbtpro WFO)
# ==============================================================================
# Define ranges for parameters to be optimized

# --- Anti-Overfitting Strategy ---
# We reduce the parameter grid to combat overfitting in several ways:
# 1. Fix some parameters to standard values instead of optimizing them
# 2. Focus on the most influential parameters based on previous WFO results
# 3. Include S/D zones as a parameter to evaluate its impact on robustness
# 4. Ensure parameter ranges are sensible and not too extreme

# ==============================================================================
# Anti-Overfitting: Drastically Simplified Parameter Grid (v2)
# ==============================================================================
# After analyzing WFO results showing high parameter instability and poor robustness,
# we further reduce dimensionality to combat overfitting by:
# 1. Focusing only on the most essential parameters (RSI thresholds and MA window)
# 2. Reducing number of options for each parameter 
# 3. Fixing use_zones to True since testing with S/D zones was a key objective
# 4. Using standard values for technical indicators like BB

OPTIMIZATION_PARAMETER_GRID = {
    # --- Fixed Parameters (not optimized) ---
    'granularity_str': ['1h'],     # Keep timeframe fixed
    'atr_window': [14],            # Standard ATR window
    'bb_window': [20],             # Standard Bollinger Band window
    'bb_std_dev': [2.0],           # Standard BB deviation - fixed to reduce combinations
    'rsi_window': [14],            # Standard RSI window
    
    # --- Core Parameters (only the most influential) ---
    # RSI thresholds reduced to just two options each
    'rsi_lower_threshold': [30, 40],  # Just two values - low oversold and moderate oversold
    'rsi_upper_threshold': [60, 70],  # Just two values - moderate overbought and strong overbought
    
    # Trend identification window - keeping this variable as it's important
    'ma_window': [50, 100],        # Keeping both options as they represent different trend timeframes
    
    # --- Risk Management Parameters (fixed) ---
    'sl_pct': [0.02],              # Fixed 2% stop loss
    'risk_reward_ratio': [2.0],    # Fixed 2:1 reward/risk ratio
    
    # --- S/D Zone Parameters ---
    'use_zones': [True, False],    # Test both with and without S/D zones to compare their impact
                                   # This is a key aspect of our strategy evaluation
    
    # --- Regime Parameters ---
    'use_regime_adaptation': [True, False],  # Test both with and without regime-specific parameter adaptation
    
    # --- Signal Generation Parameters ---
    'signal_strictness': [SignalStrictness.STRICT, SignalStrictness.BALANCED, SignalStrictness.RELAXED],
    'trend_threshold_pct': [0.01],  # Default threshold percentage
    'zone_influence': [0.3, 0.7],   # Test both lower and higher zone influence
    'min_hold_period': [2],         # Default minimum hold period
}

# --- Helper to get parameter combinations ---
def get_param_combinations() -> List[Dict]:
    """Generates all parameter combinations from the grid."""
    import vectorbtpro as vbt
    param_product = vbt.Parameter(OPTIMIZATION_PARAMETER_GRID).product()
    return list(param_product)


# Example Usage
if __name__ == '__main__':
    # Create an instance with default values
    default_config = EdgeConfig()
    print("--- Default EdgeConfig --- ")
    print(default_config.model_dump_json(indent=2))

    # Create an instance with custom values
    custom_values = {
        'granularity_str': '4h', 
        'rsi_window': 21,
        'use_zones': False,
        'pct_risk_per_trade': 0.015,
        'sl_atr_multiplier': 1.2, # Example
        'tp_atr_multiplier': 2.5, # Example
        'commission_pct': 0.0008, # Example
        'slippage_pct': 0.0003   # Example
    }
    try:
        custom_config = EdgeConfig(**custom_values)
        print("\n--- Custom EdgeConfig --- ")
        print(custom_config.model_dump_json(indent=2))
    except Exception as e:
        print(f"\nError creating custom config: {e}")

    # Show parameter combinations
    print("\n--- Optimization Parameter Grid Keys --- ")
    print(list(OPTIMIZATION_PARAMETER_GRID.keys()))

    # Note: Generating all combinations can be large
    # combinations = get_param_combinations()
    # print(f"\nTotal parameter combinations: {len(combinations)}")
    # if combinations:
    #     print("\n--- Example Parameter Combination --- ")
    #     print(combinations[0])

    print("\nEdgeConfig and Optimization Grid defined.")
