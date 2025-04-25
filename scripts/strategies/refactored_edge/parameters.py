import numpy as np

# ==============================================================================
# Parameter Grids for Walk-Forward Optimization
# ==============================================================================

# --- Full Parameter Grids (from original wfo_edge_strategy_optimized.py) ---

# Grid for the Edge Multi-Factor Strategy
EDGE_MULTI_FACTOR_PARAM_GRID = {
    # RSI parameters
    'rsi_window': (10, 25, 5),      # Range: 10, 15, 20, 25 (4 steps)
    'rsi_entry': (25, 40, 5),       # Range: 25, 30, 35, 40 (4 steps)
    'rsi_exit': (60, 75, 5),        # Range: 60, 65, 70, 75 (4 steps)

    # Bollinger Bands parameters
    'bb_window': (15, 30, 5),       # Range: 15, 20, 25, 30 (4 steps)
    'bb_std_dev': (1.8, 2.5, 0.2),  # Range: 1.8, 2.0, 2.2, 2.4 (4 steps)

    # Supply/Demand parameters (Example - adjust based on S/D implementation)
    # Assuming S/D zones are identified separately and signals are generated
    # These might control sensitivity or confirmation requirements
    # 'sd_strength_threshold': (0.5, 0.8, 0.1), # Example
    # 'sd_confirmation_bars': (1, 3, 1),        # Example

    # Trend Filter parameters (Example - using SMA crossover)
    # 'trend_fast_sma': (20, 50, 10), # Example
    # 'trend_slow_sma': (50, 200, 50), # Example

    # Volatility Filter parameters (Example - using ATR)
    'volatility_atr_window': [10, 14, 20],
    # 'volatility_atr_multiplier': (1.0, 2.0, 0.5), # Example threshold

    # Weighting for combined signal (if applicable - requires specific implementation)
    # 'weight_rsi': (0.1, 0.5, 0.1),
    # 'weight_bb': (0.1, 0.5, 0.1),
    # ... other weights

    # Risk management parameters
    'stop_loss_pct': [0.02, 0.03, 0.05],
    'take_profit_pct': [0.04, 0.06, 0.1],
    # 'risk_per_trade': [0.01, 0.02, 0.03] # Risk fraction is often handled by portfolio
}

# Grid for the Candlestick Pattern Strategy (Example, update with actual params)
CANDLESTICK_PARAM_GRID = {
    'min_strength': np.arange(0.005, 0.025, 0.005), # Pattern strength threshold
    'lookback': [10, 20, 30],                       # Lookback for strength calc
    'stop_loss_pct': [0.015, 0.025, 0.04],
    'take_profit_pct': [0.03, 0.05, 0.08],
    # Add other relevant candlestick strategy parameters here
}

# --- Quick Test Parameter Grids (Reduced sets for faster testing) ---

QUICK_TEST_EDGE_PARAM_GRID = {
    'rsi_window': [14, 21],         # 2 steps
    'rsi_entry': [30, 35],          # 2 steps
    'rsi_exit': [65, 70],           # 2 steps
    'bb_window': [20, 25],          # 2 steps
    'bb_std_dev': [2.0, 2.2],       # 2 steps
    'volatility_atr_window': [14],  # 1 step
    'stop_loss_pct': [0.03],        # 1 step
    'take_profit_pct': [0.06],      # 1 step
    # Add reduced S/D, Trend, Weights parameters if used
}

QUICK_TEST_CANDLESTICK_PARAM_GRID = {
    'min_strength': [0.01, 0.015],
    'lookback': [20],
    'stop_loss_pct': [0.025],
    'take_profit_pct': [0.05],
}

print("Parameter grids loaded.")
