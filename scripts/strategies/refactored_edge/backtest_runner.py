import vectorbtpro as vbt
import pandas as pd
import numpy as np
import sys
import os

# Import refactored components
try:
    from .strategy import RefactoredEdgeStrategy
    from . import parameters as p # Use parameter grids from parameters.py
    from . import config as cfg # Use configuration if needed (e.g., for data loading)
except ImportError:
    # Fallback for running the script directly
    # This fallback might still fail if not run as a module
    print("Warning: Running script directly, imports might fail. Use 'python -m scripts.strategies.refactored_edge.backtest_runner'", file=sys.stderr)
    from strategy import RefactoredEdgeStrategy
    import parameters as p
    import config as cfg

# ==============================================================================
# Configuration
# ==============================================================================

# --- Data --- 
# TODO: Replace with actual data loading using paths from config.py
# For now, use the same dummy data generator as in strategy.py
print("Generating dummy data for backtest...")
dates = pd.date_range('2023-01-01', periods=1000, freq='h') # Longer period for better stats
price = 100 + np.random.randn(1000).cumsum()
dummy_data = pd.DataFrame({
    'open': price - np.random.rand(1000) * 0.1,
    'high': price + np.random.rand(1000) * 0.1,
    'low': price - np.random.rand(1000) * 0.1,
    'close': price,
    'volume': np.random.rand(1000) * 100 + 10
}, index=dates)
data_freq = 'h' # Frequency of the data

# --- Parameters ---
# Select a parameter set (e.g., first combo from the quick test grid)
# In a real scenario, you might loop through these or select based on optimization results
# Using the structure defined in parameters.py
backtest_params = {
    'rsi_window': p.QUICK_TEST_EDGE_PARAM_GRID['rsi_window'][0],
    'rsi_entry': p.QUICK_TEST_EDGE_PARAM_GRID['rsi_entry'][0],
    'rsi_exit': p.QUICK_TEST_EDGE_PARAM_GRID['rsi_exit'][0],
    'bb_window': p.QUICK_TEST_EDGE_PARAM_GRID['bb_window'][0],
    'bb_std_dev': p.QUICK_TEST_EDGE_PARAM_GRID['bb_std_dev'][0],
    'adx_window': p.QUICK_TEST_EDGE_PARAM_GRID.get('adx_window', [14])[0], # Add default if missing
    'adx_threshold': p.QUICK_TEST_EDGE_PARAM_GRID.get('adx_threshold', [25])[0], # Add default
    # Add other parameters required by the strategy as they are implemented
    'stop_loss_pct': p.QUICK_TEST_EDGE_PARAM_GRID['stop_loss_pct'][0],
    'take_profit_pct': p.QUICK_TEST_EDGE_PARAM_GRID['take_profit_pct'][0],
}
print(f"Using parameters: {backtest_params}")

# --- Portfolio Settings ---
# TODO: Load these from config.py
initial_capital = 10000
fees = 0.001 # Example fee (0.1%)
sl_stop = backtest_params.get('stop_loss_pct', None) # Get from params if available
tp_stop = backtest_params.get('take_profit_pct', None)

# ==============================================================================
# Backtest Execution
# ==============================================================================

print("\n--- Starting Backtest --- ")

try:
    # 1. Instantiate the Strategy
    print("Instantiating strategy...")
    strategy_instance = RefactoredEdgeStrategy(data=dummy_data, params=backtest_params)

    # 2. Run the Strategy to get signals
    print("Running strategy logic...")
    entries, exits = strategy_instance.run()

    if entries.sum() == 0:
        print("\nStrategy generated no entry signals. Backtest cannot proceed.")
    else:
        # 3. Create Portfolio
        print("Creating portfolio from signals...")
        portfolio = vbt.Portfolio.from_signals(
            close=strategy_instance.close,
            entries=entries,
            exits=exits,
            freq=data_freq,
            init_cash=initial_capital,
            fees=fees,
            sl_stop=backtest_params.get('stop_loss_pct', None),  # Add Stop Loss
            tp_stop=backtest_params.get('take_profit_pct', None) # Add Take Profit
        )

        # 4. Analyze Results
        print("\n--- Backtest Results --- ")
        stats = portfolio.stats()
        print(stats)

        # Optional: Plotting (uncomment if needed and display is available)
        # try:
        #     print("Plotting portfolio...")
        #     fig = portfolio.plot()
        #     fig.show()
        # except Exception as plot_err:
        #     print(f"Could not generate plot: {plot_err}")

except Exception as e:
    print(f"\nError during backtest execution: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Backtest Runner Finished --- ")
