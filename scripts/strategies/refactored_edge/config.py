import pandas as pd # Added for type hinting in get_param_combinations
import vectorbtpro as vbt # Added to resolve NameError
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any

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
    initial_capital: float = Field(default=INITIAL_CAPITAL, description="Initial capital for backtesting.")
    
    # Storage for parameter combinations (added for WFO compatibility)
    param_combinations: Optional[List[Dict[str, Any]]] = None

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
        
    def get_param_combinations(self, grid_size: str = 'medium', is_quick_test: bool = False):
        """Return a list of parameter combinations for optimization.
        
        This provides access to the parameter grid for WFO optimization.
        Supports different grid sizes for balancing optimization quality with runtime.
        
        Args:
            grid_size: Size of parameter grid ('small', 'medium', 'large')
            is_quick_test: If True, returns a minimal grid for testing
            
        Returns:
            list: List of parameter dictionaries for optimization
        """
        import pandas as pd
        import vectorbtpro as vbt
        import logging
        
        logger = logging.getLogger(__name__)
        
        # For quick testing, return a minimal set of 2 combinations
        if is_quick_test:
            logger.info("Using minimal test parameter grid (2 combinations)")
            return [
                {
                    # Required indicator parameters
                    'rsi_window': 14,
                    'bb_window': 20,
                    'bb_std_dev': 2.0,
                    'ma_window': 50,
                    'atr_window': 14,
                    'rsi_entry_threshold': 30,
                    'rsi_exit_threshold': 70,
                    'adx_window': 14,
                    'adx_threshold': 25.0,
                    'use_regime_filter': self.use_regime_adaptation,
                    'use_enhanced_regimes': self.use_enhanced_regimes
                },
                {
                    'rsi_window': 14,
                    'bb_window': 20,
                    'bb_std_dev': 2.0,
                    'ma_window': 50,
                    'atr_window': 14,
                    'rsi_entry_threshold': 40,
                    'rsi_exit_threshold': 60,
                    'adx_window': 14,
                    'adx_threshold': 25.0,
                    'use_regime_filter': self.use_regime_adaptation,
                    'use_enhanced_regimes': self.use_enhanced_regimes
                }
            ]
            
        # Define grid sizes based on parameter selection
        if grid_size == 'small':
            logger.info("Using small parameter grid (limited combinations)")
            grid = {
                # Core parameters with limited options
                'rsi_window': [14],
                'bb_window': [20],
                'bb_std_dev': [2.0],
                'ma_window': [50, 100],
                'atr_window': [14],
                'rsi_entry_threshold': [30, 35, 40],
                'rsi_exit_threshold': [60, 65, 70],
                'adx_window': [14],
                'adx_threshold': [25.0],
                'use_regime_filter': [self.use_regime_adaptation],
                'use_enhanced_regimes': [self.use_enhanced_regimes],
                # Signal generation parameters
                'signal_strictness': [SignalStrictness.BALANCED, SignalStrictness.RELAXED],
                'trend_threshold_pct': [0.01],
                'zone_influence': [0.5],
                'min_hold_period': [2]
            }
            
        elif grid_size == 'large':
            logger.info("Using large parameter grid (comprehensive optimization)")
            # Use full OPTIMIZATION_PARAMETER_GRID
            grid = OPTIMIZATION_PARAMETER_GRID
            
        else:  # 'medium' (default)
            logger.info("Using medium parameter grid (balanced optimization)")
            grid = {
                # Core parameters with moderate options
                'rsi_window': [14],
                'bb_window': [20],
                'bb_std_dev': [2.0, 2.5],
                'ma_window': [21, 50, 100],
                'atr_window': [14],
                # Signal parameters with more options
                'rsi_entry_threshold': [25, 30, 35, 40, 45],
                'rsi_exit_threshold': [55, 60, 65, 70, 75],
                'adx_window': [14],
                'adx_threshold': [20.0, 25.0, 30.0],
                'use_regime_filter': [True, False],
                'use_enhanced_regimes': [True, False],
                # Signal generation parameters
                'signal_strictness': [SignalStrictness.BALANCED, SignalStrictness.RELAXED, SignalStrictness.ULTRA_RELAXED],
                'trend_threshold_pct': [0.005, 0.01, 0.015],
                'zone_influence': [0.3, 0.5, 0.7],
                'min_hold_period': [1, 2, 3]
            }
        
        # Generate parameter combinations using vectorbtpro functionality
        try:
            # Create list of parameter combinations using a more compatible approach
            import itertools
            param_keys = list(grid.keys())
            param_values = list(grid.values())
            all_combinations = list(itertools.product(*param_values))
            combinations = []
            
            # Convert to list of dictionaries
            for combo in all_combinations:
                param_dict = {}
                for i, key in enumerate(param_keys):
                    param_dict[key] = combo[i]
                combinations.append(param_dict)
                
            logger.info(f"Generated {len(combinations)} parameter combinations for optimization")
            return combinations
        except Exception as e:
            logger.error(f"Error generating parameter combinations: {str(e)}")
            # Fallback to minimal test parameters if there's an error
            logger.warning("Falling back to minimal test parameter grid")
            return self.get_param_combinations(is_quick_test=True)

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
    'bb_std_dev': [2.0, 2.5],      # Standard BB deviation with a slightly wider option
    'rsi_window': [14],            # Standard RSI window
    
    # --- Core Parameters (expanded to ensure more trades are generated) ---
    # RSI thresholds with broader ranges to ensure signal generation across conditions
    'rsi_lower_threshold': [25, 28, 30, 33, 35, 38, 40, 42, 45],  # Broadened range from 25-45 for more entry opportunities
    'rsi_upper_threshold': [55, 58, 60, 62, 65, 68, 70, 72, 75],  # Broadened range from 55-75 for more exit opportunities
    
    # Trend identification window - keeping this variable as it's important
    'ma_window': [21, 50, 100, 200],   # Added shorter and longer-term trend options
    
    # --- Risk Management Parameters (expanded) ---
    'sl_pct': [0.015, 0.02, 0.025],  # More options for stop loss percentage
    'risk_reward_ratio': [1.5, 2.0, 2.5],  # More options for R:R ratio
    
    # --- S/D Zone Parameters ---
    'use_zones': [True, False],    # Test both with and without S/D zones
    
    # --- Position Sizing Parameters ---
    'use_dynamic_sizing': [True, False],  # Test both with and without dynamic position sizing
    'risk_percentage': [0.005, 0.01, 0.015],  # Risk percentage options (0.5%, 1%, 1.5%)
    
    # --- Regime Parameters ---
    'use_regime_adaptation': [True, False],  # Test both with and without regime adaptation
    
    # --- Signal Generation Parameters ---
    'signal_strictness': [SignalStrictness.BALANCED, SignalStrictness.RELAXED, SignalStrictness.ULTRA_RELAXED],  # Focus on less strict modes
    'trend_threshold_pct': [0.005, 0.01, 0.015, 0.02],  # More options from less strict to more strict
    'zone_influence': [0.3, 0.5, 0.7, 0.9],   # Broader range for zone influence testing
    'min_hold_period': [0, 1, 2, 3],         # Include option for no minimum hold and longer holds
}

# --- Helper to get parameter combinations ---
def get_param_combinations() -> List[Dict]:
    """Generates all parameter combinations from the grid.
    
    Uses vectorbtpro.utils.params module for parameter combination generation.
    """
    import vectorbtpro as vbt
    from itertools import product
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Use vectorbtpro's params module for robust parameter grid generation
    try:
        # Method 1: Using vectorbtpro.utils.params.combine_params
        # First convert each parameter list to a Param object
        param_dct = {}
        for k, v in OPTIMIZATION_PARAMETER_GRID.items():
            param_dct[k] = vbt.utils.params.Param(v)
        
        # Use combine_params to generate parameter combinations
        param_tuples, param_idx = vbt.utils.params.combine_params(param_dct)
        
        # Convert the result to a list of parameter dictionaries
        combinations = []
        for i in range(len(param_tuples[0])):
            param_dict = {}
            for j, k in enumerate(param_dct.keys()):
                param_dict[k] = param_tuples[j][i]  # Note the reversed indices compared to previous version
            combinations.append(param_dict)
        
        logger.info(f"Generated {len(combinations)} parameter combinations using VectorBTpro params module")
        return combinations
    except Exception as e:
        # Fallback method using itertools if vectorbtpro method fails
        logger.warning(f"Falling back to itertools for parameter generation: {str(e)}")
        
        param_keys = list(OPTIMIZATION_PARAMETER_GRID.keys())
        param_values = list(OPTIMIZATION_PARAMETER_GRID.values())
        all_combinations = list(product(*param_values))
        
        combinations = [dict(zip(param_keys, combo)) for combo in all_combinations]
        logger.info(f"Generated {len(combinations)} parameter combinations using itertools")
        return combinations


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
