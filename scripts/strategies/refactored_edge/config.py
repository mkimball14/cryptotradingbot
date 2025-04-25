import os
import multiprocessing
from datetime import datetime, timedelta
from dotenv import load_dotenv
import itertools

load_dotenv(verbose=True)

# ==============================================================================
# Configuration Constants for Refactored Edge Strategy
# ==============================================================================

# --- WFO Parameters ---
IN_SAMPLE_DAYS = 100       # Training period
OUT_SAMPLE_DAYS = 40      # Testing period
STEP_DAYS = 50            # Step forward
OPTIMIZATION_METRIC = 'sharpe_ratio' # Metric to optimize during WFO

# --- Data Parameters ---
TOTAL_HISTORY_DAYS = 500 # Total days of historical data to fetch for WFO
WFO_END_DATE = datetime.now().strftime('%Y-%m-%d')
WFO_START_DATE = (datetime.now() - timedelta(days=TOTAL_HISTORY_DAYS)).strftime('%Y-%m-%d')
SYMBOL = "BTC-USD"          # Default symbol for trading
GRANULARITY_STR = "1h"      # Default granularity
BENCHMARK_SYMBOL = "BTC-USD" # Symbol for benchmark comparison

# Map granularity strings to seconds (add more as needed)
GRANULARITY_MAP_SECONDS = {
    '1m': 60,
    '5m': 300,
    '15m': 900,
    '1h': 3600,
    '4h': 14400,
    '1d': 86400
}

try:
    GRANULARITY_SECONDS = GRANULARITY_MAP_SECONDS[GRANULARITY_STR]
except KeyError:
    print(f"Warning: Invalid GRANULARITY_STR '{GRANULARITY_STR}' in config. Defaulting to 1h (3600s).")
    GRANULARITY_STR = "1h"
    GRANULARITY_SECONDS = 3600

# --- Trading Parameters ---
INITIAL_CAPITAL = 3000.0    # Starting capital for backtests/WFO
COMMISSION_PCT = 0.001      # Trading commission percentage
SLIPPAGE_PCT = 0.0005       # Slippage percentage
RISK_FRACTION = 0.01        # Default fraction of capital to risk per trade
ATR_WINDOW_SIZING = 14      # ATR window for position sizing/stop loss

# --- Strategy Selection --- 
# This might be overridden by runner scripts or command-line args
DEFAULT_STRATEGY_TYPE = "edge_multi_factor"  # Options: "edge_multi_factor", "candlestick"

# --- Performance Optimization Settings ---
USE_PARALLEL = True         # Use multiprocessing for WFO
NUM_CORES = max(1, multiprocessing.cpu_count() - 1) # Cores for parallel processing
ENABLE_CACHING = True       # Enable vectorbt caching where applicable
VERBOSE_DEBUG = False       # Enable verbose debug logging
QUICK_TEST = False          # Use smaller parameter grid and data for quick tests (override in runner)

# --- WFO Performance Constraints ---
# Minimum requirements for a parameter set to be considered valid in WFO
MIN_TOTAL_TRADES = 3
MIN_WIN_RATE = 0.30
MAX_DRAWDOWN = -0.35

# --- File Paths ---
# Assuming standard project structure relative to this config file's location
# Adjust if your structure differs
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
CHECKPOINT_DIR = os.path.join(PROJECT_ROOT, 'checkpoints')
RESULTS_DIR = os.path.join(PROJECT_ROOT, 'results')

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "refactored_wfo_run.log")
WFO_CHECKPOINT_FILE = os.path.join(CHECKPOINT_DIR, "refactored_wfo_checkpoint.json")
WFO_RESULTS_FILE = os.path.join(RESULTS_DIR, "refactored_wfo_results.json")
WFO_PLOT_FILE = os.path.join(RESULTS_DIR, "refactored_wfo_performance.png")
BACKTEST_PLOT_FILE = os.path.join(RESULTS_DIR, "refactored_backtest.png")

# --- API Keys (Loaded from .env) ---
# Example keys - replace with your actual environment variable names
COINBASE_API_KEY = os.getenv("COINBASE_ADVANCED_API_KEY")
COINBASE_API_SECRET_PEM = os.getenv("COINBASE_ADVANCED_API_SECRET_PEM")
COINBASE_API_PASSPHRASE = os.getenv("COINBASE_ADVANCED_API_PASSPHRASE")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# ==============================================================================
# Parameter Grids for Optimization
# ==============================================================================

EDGE_MULTI_FACTOR_PARAM_GRID = {
    # RSI parameters
    'rsi_window': (10, 25, 5),      # Range: 10, 15, 20, 25 (4 steps)
    'rsi_entry_threshold': (25, 40, 5),       # Range: 25, 30, 35, 40 (4 steps)
    'rsi_exit_threshold': (60, 75, 5),        # Range: 60, 65, 70, 75 (4 steps)

    # Bollinger Band parameters
    'bb_window': (15, 30, 5),       # Range: 15, 20, 25, 30 (4 steps)
    'bb_std_dev': (1.8, 2.5, 0.2),      # Range: 1.8, 2.0, 2.2, 2.4 (4 steps) - Adjusted endpoint slightly for step

    # Volatility parameters
    'vol_window': (10, 30, 10),     # Range: 10, 20, 30 (3 steps)
    'vol_threshold': (0.8, 1.6, 0.4),# Range: 0.8, 1.2, 1.6 (3 steps)

    # Trend parameters
    'trend_window': [200],          # Example: Fixed 200 period SMA for trend

    # Stop loss and take profit
    'sl_stop': (0.01, 0.04, 0.01),    # Range: 1.0, 2.0, 3.0, 4.0 (4 steps)
    'tp_stop': (0.02, 0.08, 0.02),    # Range: 2.0, 4.0, 6.0, 8.0 (4 steps)

    # Position sizing
    'risk_per_trade': [0.01, 0.02]  # 2 steps
}

CANDLESTICK_PARAM_GRID = {
    # Candlestick pattern parameters
    'lookback_periods': [20, 30, 50],
    'min_strength': [0.005, 0.01, 0.02, 0.05],
    'use_strength': [True, False],
    'use_confirmation': [True, False],
    'confirmation_window': [2, 3, 5],

    # Risk management parameters
    'stop_loss_pct': [0.02, 0.03, 0.05], # Note: original used 'stop_loss_pct'
    'take_profit_pct': [0.04, 0.06, 0.1],# Note: original used 'take_profit_pct'
    'risk_per_trade': [0.01, 0.02, 0.03]
}

QUICK_TEST_PARAM_GRID = {
    'rsi_window': [14, 21],         # 2 steps
    'rsi_entry_threshold': [30, 35],          # 2 steps
    'rsi_exit_threshold': [65, 70],           # 2 steps
    'bb_window': [20],             # 1 step
    'bb_std_dev': [2.0, 2.2],           # 2 steps
    'vol_window': [20],           # 1 step
    'vol_threshold': [1.0],       # 1 step

    # Trend parameters
    'trend_window': [200],          # Keep fixed for quick test

    'sl_stop': [0.02, 0.03],           # 2 steps (Reduced from 3)
    'tp_stop': [0.04, 0.06],           # 2 steps (Reduced from 3)
    'risk_per_trade': [0.01]      # 1 step
    # Total combinations: 2*2*2*1*2*1*1*1*2*2*1 = 64 combinations
}

# ==============================================================================
# Select Active Parameter Grid and Apply Quick Test Overrides
# ==============================================================================

# Select the base parameter grid based on the default strategy type
if DEFAULT_STRATEGY_TYPE == "candlestick":
    PARAM_GRID = CANDLESTICK_PARAM_GRID
else: # Default to edge_multi_factor
    PARAM_GRID = EDGE_MULTI_FACTOR_PARAM_GRID

# Apply QUICK_TEST overrides if the flag is set
if QUICK_TEST:
    print("--- QUICK TEST MODE ACTIVE ---")
    print("Overriding PARAM_GRID with QUICK_TEST_PARAM_GRID.")
    PARAM_GRID = QUICK_TEST_PARAM_GRID

    # Override WFO and Data parameters
    print("Overriding WFO/Data parameters for quick test.")
    IN_SAMPLE_DAYS = 50
    OUT_SAMPLE_DAYS = 20
    STEP_DAYS = 25
    TOTAL_HISTORY_DAYS = 180
    # Recalculate WFO_START_DATE based on the new TOTAL_HISTORY_DAYS
    WFO_START_DATE = (datetime.now() - timedelta(days=TOTAL_HISTORY_DAYS)).strftime('%Y-%m-%d')
    # Reduce cores potentially for quicker setup/teardown in testing
    # NUM_CORES = max(1, NUM_CORES // 2)
    # MIN_TOTAL_TRADES = 1 # Relax constraints for quick testing

    print(f"QUICK TEST ACTIVE: Using {len(list(itertools.product(*PARAM_GRID.values())))} parameter combinations.")
    print(f"QUICK TEST WFO Params: In-Sample={IN_SAMPLE_DAYS}, Out-Sample={OUT_SAMPLE_DAYS}, Step={STEP_DAYS}, History={TOTAL_HISTORY_DAYS} days")
    print("-----------------------------")


print("Configuration loaded.")
