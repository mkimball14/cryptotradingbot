import numpy as np

# Parameter grid for RefactoredEdgeStrategy Optimization
# Define ranges or specific values for each parameter to be optimized.
# Keys should match the parameter names expected by the strategy's __init__ method.

# --- START OF MINIMAL DEBUG GRID (4 combinations) ---
PARAM_GRID = {
    # RSI Parameters (Fixed)
    'rsi_window': [14],          
    'rsi_entry': [30],           
    'rsi_exit': [70],            
    
    # Bollinger Bands Parameters (Fixed)
    'bb_window': [20],            
    'bb_std_dev': [2.0],         
    
    # MACD Parameters (FIXED for faster runs)
    'macd_fast_window': [12],         # Fixed to 1
    'macd_slow_window': [26],         # Fixed to 1
    'macd_signal_window': [9],         # Fixed to 1

    # ADX Parameters (Commented out)
    # 'adx_window': [14],
    # 'adx_threshold': [25],

    # Signal Combination Weights (FIXED for faster runs)
    'rsi_weight': [1.0],              # Fixed to 1
    'bb_weight': [1.0],               # Fixed to 1
    'macd_weight': [1.0],             # Fixed to 1

    # Combined Signal Threshold (Varying)
    'signal_threshold': [0.1, 0.15],   # Varying (2 values)

    # Stop Loss / Take Profit (Passed to Portfolio)
    'stop_loss_pct': [0.02],    # Fixed
    'take_profit_pct': [0.05, 0.10],  # Varying (2 values) - Let's vary this too for a small grid
}
# --- END OF MINIMAL DEBUG GRID ---

# Example of how to generate combinations (if needed outside WFO runner)
# from vectorbtpro.utils.params import create_param_combs
# if __name__ == "__main__":
#     param_combs = create_param_combs(PARAM_GRID)
#     print(f"Generated {len(param_combs)} parameter combinations.")
#     print("First combination:", param_combs[0])
