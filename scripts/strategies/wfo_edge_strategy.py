import sys
import os
from pathlib import Path
import vectorbtpro as vbt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import itertools
import logging
from typing import Dict, Any, List, Tuple, Optional
from tqdm.auto import tqdm # Use tqdm for progress bars
import json

# --- Setup Paths ---
# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Define output directory relative to this script
OUTPUT_DIR = Path(__file__).resolve().parent / 'wfo_results'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Create if it doesn't exist

# --- Setup Logging ---
# Define a unique logger for this script to avoid conflicts
wfo_logger = logging.getLogger('wfo_edge_strategy')
wfo_logger.setLevel(logging.DEBUG)  # Change to DEBUG level
# Prevent logging propagation to root logger if already configured
wfo_logger.propagate = False 
# Add handler if not already added (basic console handler)
if not wfo_logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    wfo_logger.addHandler(ch)
# Optionally, add a file handler
# log_file_path = OUTPUT_DIR / f"wfo_edge_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
# fh = logging.FileHandler(log_file_path)
# fh.setFormatter(formatter)
# wfo_logger.addHandler(fh)

# --- Import Strategy and Data Fetcher ---
try:
    # Use the correct relative path based on standard project structure
    from scripts.strategies.edge_multi_factor import EdgeMultiFactorStrategy
    wfo_logger.info("Successfully imported refactored EdgeMultiFactorStrategy.")
except ImportError as e:
    wfo_logger.error(f"Could not import EdgeMultiFactorStrategy: {e}")
    # Attempt fallback if path structure is different
    try:
        from edge_multi_factor import EdgeMultiFactorStrategy
        wfo_logger.info("Imported EdgeMultiFactorStrategy from current directory.")
    except ImportError:
        wfo_logger.critical("Failed to import EdgeMultiFactorStrategy from both locations. Exiting.")
        sys.exit(1)

try:
    from data.data_fetcher import fetch_historical_data, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    wfo_logger.info("Using data_fetcher from data module.")
except ImportError as e:
    wfo_logger.error(f"Could not import data_fetcher: {e}. Functionality may be limited.")
    # Define dummy functions if data_fetcher is critical and missing
    def fetch_historical_data(*args, **kwargs): return None
    def get_vbt_freq_str(*args, **kwargs): return "1h"
    GRANULARITY_MAP_SECONDS = {'1h': 3600}

# --- VectorBT Pro Chat Model Integration ---
def initialize_chat_model():
    """Initialize the chat model for debugging assistance."""
    try:
        # Check if the knowledge.chatting module is available and has ChatModel
        if hasattr(vbt, 'utils') and hasattr(vbt.utils, 'knowledge') and hasattr(vbt.utils.knowledge, 'chatting') and hasattr(vbt.utils.knowledge.chatting, 'ChatModel'):
            return vbt.utils.knowledge.chatting.ChatModel()
        else:
            wfo_logger.warning("ChatModel not found in vectorbtpro.utils.knowledge.chatting. Using fallback debugging approach.")
            return None
    except Exception as e:
        wfo_logger.error(f"Could not initialize chat model: {e}")
        return None

def get_chat_model():
    """Get an instance of the chat model or return None if not available."""
    try:
        return initialize_chat_model()
    except Exception as e:
        wfo_logger.error(f"Could not initialize chat model: {e}")
        return None

def ask_chat_model(chat_model, query, context=None):
    """Query the chat model with the given question and context."""
    if chat_model is None:
        return "Chat model not available for debugging assistance."
    
    try:
        # Call the chat model with the query and context
        # This is a placeholder implementation based on typical NLP model interfaces
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            response = chat_model.query(f"{query}\n\nContext:\n{context_str}")
        else:
            response = chat_model.query(query)
        return response
    except Exception as e:
        return f"Error querying chat model: {e}"

def debug_with_chat(error: Exception, context: Dict[str, Any]) -> str:
    """
    Use VectorBT Pro's chat model to analyze and suggest fixes for errors.
    
    Args:
        error: The exception that occurred
        context: Dictionary with relevant context (params, data info, etc.)
        
    Returns:
        str: Debugging suggestions from the chat model
    """
    chat_model = get_chat_model()
    if chat_model is None:
        return "Chat model not available for debugging assistance."
        
    error_msg = f"Error Type: {type(error).__name__}\nError Message: {str(error)}"
    question = f"""
    Please analyze this error and suggest potential fixes:
    
    {error_msg}
    
    The error occurred in the WFO Edge Strategy implementation.
    Please consider the context provided and suggest specific fixes.
    """
    
    return ask_chat_model(chat_model, question, context)

# --- Error Handling with Chat Model ---
def handle_portfolio_error(error: Exception, params: Dict[str, Any], data_info: Dict[str, Any]) -> str:
    """
    Handle portfolio creation/simulation errors with chat model assistance.
    
    Args:
        error: The exception that occurred
        params: Dictionary of strategy and trading parameters
        data_info: Dictionary with information about the data being used
        
    Returns:
        str: Debugging suggestions from the chat model
    """
    context = {
        "parameters": params,
        "data_info": {
            "shape": data_info.get("shape"),
            "date_range": data_info.get("date_range"),
            "has_nulls": data_info.get("has_nulls", False),
            "frequency": data_info.get("frequency")
        }
    }
    
    return debug_with_chat(error, context)

# =============================================================================
# Configuration Constants
# =============================================================================

# --- WFO Parameters ---
# Use reasonably short periods for quicker testing based on notes
IN_SAMPLE_DAYS = 180      # Length of the training period
OUT_SAMPLE_DAYS = 60      # Length of the testing period
STEP_DAYS = 60            # How much to shift the window each step
# Ensure step is not larger than OOS period to avoid gaps, unless intended
if STEP_DAYS > OUT_SAMPLE_DAYS:
    wfo_logger.warning(f"STEP_DAYS ({STEP_DAYS}) > OUT_SAMPLE_DAYS ({OUT_SAMPLE_DAYS}). OOS periods will overlap.")

# --- Data Parameters ---
# Use a longer period to ensure enough data for signal generation
TOTAL_HISTORY_DAYS = 365 # Full year of data
WFO_END_DATE = datetime.now().strftime('%Y-%m-%d')
WFO_START_DATE = (datetime.now() - timedelta(days=TOTAL_HISTORY_DAYS)).strftime('%Y-%m-%d')
SYMBOL = "BTC-USD"
GRANULARITY_STR = "1h" # Ensure this matches strategy needs
try:
    GRANULARITY_SECONDS = GRANULARITY_MAP_SECONDS[GRANULARITY_STR]
except KeyError:
    wfo_logger.error(f"Invalid GRANULARITY_STR: {GRANULARITY_STR}. Defaulting to 1h (3600s).")
    GRANULARITY_SECONDS = 3600
BENCHMARK_SYMBOL = "BTC-USD" # Or None

# --- Trading Parameters ---
INITIAL_CAPITAL = 3000
COMMISSION_PCT = 0.001
SLIPPAGE_PCT = 0.0005
RISK_FRACTION = 0.01      # Fraction of capital to risk per trade for sizing
ATR_WINDOW_SIZING = 14    # ATR period used in sizing calculation

# --- Optimization Parameters ---
OPTIMIZATION_METRIC = 'sharpe_ratio' # e.g., 'sharpe_ratio', 'total_return', 'max_drawdown'
# Expand parameter space for better optimization chances
PARAM_GRID = {
    'lookback_window': [14, 20, 30, 40], # Expanded options
    'volatility_threshold': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], # More options, especially lower values
    'tsl_stop': [0.03, 0.05, 0.07, 0.1], # Trailing Stop Loss % (0 to disable)
    'tp_stop': [0.08, 0.10, 0.15, 0], # Take Profit % (0 to disable)
    'atr_multiple_sl': [1.0, 1.5, 2.0, 2.5], # ATR multiple for initial stop distance
    'vol_filter_window': [50, 100, 150] # Add vol_filter_window parameter
}
FACTOR_NAMES = ['volatility_regime', 'consolidation_breakout', 'volume_divergence', 'market_microstructure']
# Generate multiple weight combinations instead of just equal weights
weight_options = [
    # Equal weights
    {'volatility_regime': 0.25, 'consolidation_breakout': 0.25, 'volume_divergence': 0.25, 'market_microstructure': 0.25},
    # Emphasis on volatility and consolidation
    {'volatility_regime': 0.4, 'consolidation_breakout': 0.4, 'volume_divergence': 0.1, 'market_microstructure': 0.1},
    # Emphasis on volatility regime
    {'volatility_regime': 0.6, 'consolidation_breakout': 0.2, 'volume_divergence': 0.1, 'market_microstructure': 0.1}, 
    # Emphasis on consolidation breakout
    {'volatility_regime': 0.2, 'consolidation_breakout': 0.6, 'volume_divergence': 0.1, 'market_microstructure': 0.1}
]
WEIGHT_COMBINATIONS = weight_options
# To optimize weights:
# WEIGHT_OPT_STEPS = 1 # Set > 0 to generate combinations
# WEIGHT_COMBINATIONS = generate_weight_combinations(FACTOR_NAMES, WEIGHT_OPT_STEPS)


# =============================================================================
# Helper Functions
# =============================================================================

# Function to generate weight combinations (if optimizing weights)
def generate_weight_combinations(factors: List[str], num_steps: int) -> List[Dict[str, float]]:
    """Generates valid factor weight combinations that sum to 1.0."""
    if not factors or num_steps <= 0:
        # Return default equal weights if no steps or factors
        return [{factor: 1.0/len(factors) for factor in factors}] if factors else []

    step = 1.0 / num_steps
    points = [round(i * step, 8) for i in range(num_steps + 1)] # Use round for precision
    valid_combinations = []

    for combo in itertools.product(points, repeat=len(factors)):
        if np.isclose(sum(combo), 1.0):
            valid_combinations.append(dict(zip(factors, combo)))

    # Deduplicate (necessary due to potential float precision issues)
    unique_combos_dict = {}
    for combo_dict in valid_combinations:
        combo_tuple = tuple(sorted(combo_dict.items()))
        if combo_tuple not in unique_combos_dict:
             unique_combos_dict[combo_tuple] = combo_dict

    # Ensure default equal weights are included if valid
    default_weights = {factor: 1.0 / len(factors) for factor in factors}
    default_tuple = tuple(sorted(default_weights.items()))
    if np.isclose(sum(default_weights.values()), 1.0) and default_tuple not in unique_combos_dict:
        unique_combos_dict[default_tuple] = default_weights

    return list(unique_combos_dict.values())


def create_pf_for_params(
    data: pd.DataFrame,
    strategy_params: Dict[str, Any],
    trade_params: Dict[str, Any]
    ) -> Optional[vbt.Portfolio]:
    """
    Helper function to create and run a vectorbt Portfolio for a given set of parameters.

    Args:
        data: DataFrame with OHLCV data for the current period (train or test).
        strategy_params: Dictionary containing parameters for EdgeMultiFactorStrategy
                         (lookback_window, volatility_threshold, factor_weights).
        trade_params: Dictionary containing parameters for portfolio execution
                      (tsl_stop, tp_stop, atr_multiple_sl, risk_fraction, atr_window).

    Returns:
        A vectorbt Portfolio object, or None if an error occurs or no trades are generated.
    """
    try:
        # 1. Initialize strategy with current strategy parameters
        strategy = EdgeMultiFactorStrategy(
            lookback_window=int(strategy_params['lookback_window']),
            volatility_threshold=float(strategy_params['volatility_threshold']),
            default_factor_weights=strategy_params['factor_weights'], # Pass weights
            vol_filter_window=int(strategy_params.get('vol_filter_window', 100)), # Use get() with default
            initial_capital=INITIAL_CAPITAL, # Needed for sizing calc
            commission_pct=COMMISSION_PCT,
            slippage_pct=SLIPPAGE_PCT
        )

        # 2. Generate signals using the strategy's method (no factory)
        # Ensure data covers the lookback period needed by generate_signals internal calls
        if len(data) < strategy.lookback_window + 2: # Add buffer
             wfo_logger.warning(f"Data length ({len(data)}) insufficient for lookback ({strategy.lookback_window}). Skipping PF creation.")
             return None
             
        long_entries, short_entries = strategy.generate_signals(data)

        # Enhanced signal tracking for debugging
        signal_count = long_entries.sum() + short_entries.sum()
        if signal_count == 0:
            wfo_logger.debug(f"No entry signals generated with params: lookback={strategy_params['lookback_window']}, " +
                           f"vol_thresh={strategy_params['volatility_threshold']}, " +
                           f"vol_filter={strategy_params.get('vol_filter_window', 100)}")
            return None
        else:
            wfo_logger.debug(f"Generated {long_entries.sum()} long and {short_entries.sum()} short signals with params: " +
                           f"lookback={strategy_params['lookback_window']}, vol_thresh={strategy_params['volatility_threshold']}")

        # Skip if no entry signals
        if long_entries.sum() + short_entries.sum() == 0:
            # wfo_logger.debug("No entry signals generated for this parameter set.")
            return None

        # 3. Calculate sizing ('Amount') and SL % (for sl_stop param)
        target_amount = strategy.calculate_target_amount(
            data,
            risk_fraction=float(trade_params['risk_fraction']),
            atr_window=int(trade_params['atr_window']),
            atr_multiple_stop=float(trade_params['atr_multiple_sl'])
        )

        # Calculate SL % based on ATR for the sl_stop parameter
        atr = vbt.ATR.run(
            data['high'], data['low'], data['close'],
            window=int(trade_params['atr_window']), wtype='wilder'
            ).atr.bfill().ffill()
        sl_stop_dist = (atr * float(trade_params['atr_multiple_sl']))
        # Use .replace before division, handle potential NaNs/Infs after division
        close_safe = data['close'].replace(0, np.nan)
        sl_stop_pct = (sl_stop_dist / close_safe).replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
        sl_stop_pct = np.clip(sl_stop_pct, 0.001, 0.5) # Apply bounds

        # 4. Run Portfolio Simulation
        vbt_freq = pd.infer_freq(data.index)
        if not vbt_freq:
            try:
                # Attempt to get freq from GRANULARITY_SECONDS if index freq fails
                vbt_freq = get_vbt_freq_str(GRANULARITY_SECONDS)
            except NameError: # Fallback if get_vbt_freq_str is not available
                 vbt_freq = "1h" # Default fallback
            wfo_logger.debug(f"Could not infer frequency for portfolio, using '{vbt_freq}'.")

        # Prepare TSL and TP stops (use None if 0)
        tsl_stop_val = float(trade_params['tsl_stop']) if float(trade_params['tsl_stop']) > 0 else None
        tp_stop_val = float(trade_params['tp_stop']) if float(trade_params['tp_stop']) > 0 else None

        pf = vbt.Portfolio.from_signals(
            data['close'],
            entries=long_entries,
            short_entries=short_entries,
            sl_stop=sl_stop_pct,
            tsl_stop=tsl_stop_val,
            tp_stop=tp_stop_val,
            size=target_amount,
            size_type='Amount',
            init_cash=INITIAL_CAPITAL,
            fees=COMMISSION_PCT,
            slippage=SLIPPAGE_PCT,
            freq=vbt_freq,
            call_seq='auto',
            accumulate=False,
            stop_exit_type='close',
            save_state=True,
            save_returns=True,
            fillna_close=True,
            seed=42
        )
        return pf

    except Exception as e:
        # Enhanced error handling with chat model
        data_info = {
            "shape": data.shape if isinstance(data, pd.DataFrame) else None,
            "date_range": f"{data.index[0]} to {data.index[-1]}" if len(data.index) > 0 else None,
            "has_nulls": data.isnull().any().any() if isinstance(data, pd.DataFrame) else None,
            "frequency": vbt_freq if 'vbt_freq' in locals() else None
        }
        
        debug_suggestions = handle_portfolio_error(e, 
            params={**strategy_params, **trade_params},
            data_info=data_info
        )
        
        # Log the error with parameters and chat model suggestions
        wfo_logger.error(
            f"Error in create_pf_for_params:\n"
            f"Parameters: StrategyP:{strategy_params}, TradeP:{trade_params}\n"
            f"Error: {e}\n"
            f"Debug Suggestions:\n{debug_suggestions}",
            exc_info=True
        )
        return None # Return None on error


# =============================================================================
# Main WFO Function
# =============================================================================

def run_walk_forward_optimization():
    """
    Performs the Walk-Forward Optimization process.
    1. Fetches data.
    2. Splits data into training and testing sets according to WFO parameters.
    3. Optimizes strategy parameters on each training set.
    4. Evaluates the best parameters on the corresponding testing set.
    5. Combines out-of-sample results and evaluates the final portfolio.
    6. Saves results.
    """
    try:
        wfo_logger.info("--- Starting Walk-Forward Optimization ---")
        wfo_logger.info(f"Symbol: {SYMBOL}, Granularity: {GRANULARITY_STR}")
        wfo_logger.info(f"Date Range: {WFO_START_DATE} to {WFO_END_DATE}")
        wfo_logger.info(f"WFO Config: IS={IN_SAMPLE_DAYS}d, OOS={OUT_SAMPLE_DAYS}d, Step={STEP_DAYS}d")
        wfo_logger.info(f"Optimization Metric: {OPTIMIZATION_METRIC}")
        wfo_logger.info(f"Output Directory: {OUTPUT_DIR}")

        # Initialize chat model for the optimization process
        chat_model = get_chat_model()
        if chat_model:
            wfo_logger.info("VectorBT Pro chat model initialized for optimization assistance.")
        else:
            wfo_logger.warning("Chat model not available. Proceeding without optimization assistance.")

        # 1. Fetch Data
        wfo_logger.info("Fetching historical data...")
        price_data = fetch_historical_data(SYMBOL, WFO_START_DATE, WFO_END_DATE, GRANULARITY_SECONDS)
        if price_data is None or price_data.empty:
            if chat_model:
                suggestions = ask_chat_model(chat_model, 
                    "Failed to fetch price data. What could be the potential issues?",
                    {"symbol": SYMBOL, "dates": f"{WFO_START_DATE} to {WFO_END_DATE}"}
                )
                wfo_logger.error(f"Failed to fetch price data. Chat model suggestions:\n{suggestions}")
            wfo_logger.critical("Failed to fetch price data. Exiting.")
            return
        # Basic data cleaning and validation
        price_data = price_data[['open', 'high', 'low', 'close', 'volume']].copy()
        price_data.index = pd.to_datetime(price_data.index, utc=True)
        price_data = price_data.sort_index()
        price_data.dropna(inplace=True) # Drop rows with any NaNs
        wfo_logger.info(f"Price data fetched and cleaned. Shape: {price_data.shape}")
        if price_data.empty:
             wfo_logger.critical("Price data is empty after cleaning. Exiting.")
             return

        # Fetch Benchmark Data (Optional)
        benchmark_rets = None
        if BENCHMARK_SYMBOL:
            wfo_logger.info(f"Fetching benchmark data for {BENCHMARK_SYMBOL}...")
            benchmark_data = fetch_historical_data(BENCHMARK_SYMBOL, WFO_START_DATE, WFO_END_DATE, GRANULARITY_SECONDS)
            if benchmark_data is not None and not benchmark_data.empty:
                benchmark_data.index = pd.to_datetime(benchmark_data.index, utc=True)
                benchmark_data = benchmark_data.sort_index()
                benchmark_close = benchmark_data['close'].reindex(price_data.index).ffill().bfill()
                benchmark_rets = benchmark_close.pct_change().fillna(0)
                wfo_logger.info(f"Benchmark data fetched. Shape: {benchmark_data.shape}")
            else:
                wfo_logger.warning("Could not fetch benchmark data. Proceeding without benchmark.")

        # 2. Setup WFO Splitter
        # Use vbt.rolling_split for standard WFO
        # Ensure offset parameters are Timedeltas
        in_sample_len = pd.Timedelta(days=IN_SAMPLE_DAYS)
        out_sample_len = pd.Timedelta(days=OUT_SAMPLE_DAYS)
        step_len = pd.Timedelta(days=STEP_DAYS)

        # Calculate n based on available data and step size (approximate)
        total_duration_available = price_data.index[-1] - price_data.index[0]
        num_steps_possible = max(0, (total_duration_available - in_sample_len - out_sample_len) // step_len) + 1
        n_splits = int(num_steps_possible)
        wfo_logger.info(f"Calculated number of WFO splits: {n_splits}")
        if n_splits <= 0:
            wfo_logger.error("Not enough data for the specified WFO parameters. Exiting.")
            return
            
        # Create the splitter
        try:
            # Convert time-based parameters to number of rows
            rows_per_day = 24  # Since we're using hourly data
            in_sample_rows = IN_SAMPLE_DAYS * rows_per_day
            out_sample_rows = OUT_SAMPLE_DAYS * rows_per_day
            step_rows = STEP_DAYS * rows_per_day
            
            # Create splits manually using simple lists
            splits = []
            total_rows = len(price_data)
            start_idx = 0
            
            while start_idx + in_sample_rows + out_sample_rows <= total_rows:
                train_end = start_idx + in_sample_rows
                test_end = min(train_end + out_sample_rows, total_rows)
                
                # Create lists of indices for train and test sets
                train_indices = list(range(start_idx, train_end))
                test_indices = list(range(train_end, test_end))
                
                # Create split using simple lists
                splits.append([train_indices, test_indices])
                start_idx += step_rows
            
            if not splits:
                wfo_logger.error("No valid splits could be created with the given parameters.")
                return
            
            # Create splitter using only supported parameters
            splitter = vbt.Splitter.from_splits(
                price_data.index,
                splits=splits
            )
            
            # Log split information
            wfo_logger.info(f"Created splitter with {len(splits)} splits.")
            
            # Verify splits with chat model assistance
            if chat_model:
                splits_info = {
                    "total_splits": len(splits),
                    "first_split": {
                        "train": f"{price_data.index[splits[0][0][0]]} to {price_data.index[splits[0][0][-1]]}",
                        "test": f"{price_data.index[splits[0][1][0]]} to {price_data.index[splits[0][1][-1]]}"
                    } if splits else None
                }
                validation = ask_chat_model(chat_model,
                    "Please validate these WFO splits. Are they reasonable?",
                    splits_info
                )
                wfo_logger.info(f"Split Validation:\n{validation}")
                
        except Exception as split_err:
            if chat_model:
                suggestions = ask_chat_model(chat_model,
                    f"Error creating splits: {split_err}. What might be wrong?",
                    {"data_length": len(price_data), "wfo_params": {
                        "in_sample_days": IN_SAMPLE_DAYS,
                        "out_sample_days": OUT_SAMPLE_DAYS,
                        "step_days": STEP_DAYS
                    }}
                )
                wfo_logger.error(f"Split creation error. Chat model suggestions:\n{suggestions}")
            wfo_logger.error(f"Error creating vbt.Splitter: {split_err}. Check WFO parameters and data length.", exc_info=True)
            return
            
        # 3. Prepare Parameter Combinations
        param_combinations = []
        param_keys = list(PARAM_GRID.keys())
        # Use product to generate all combinations from the grid values
        for combo_values in itertools.product(*[PARAM_GRID[key] for key in param_keys]):
            param_set = dict(zip(param_keys, combo_values))
            # Add the fixed factor weights to each parameter set
            param_set['factor_weights'] = WEIGHT_COMBINATIONS[0] # Assuming fixed weights for now
            param_combinations.append(param_set)

        # Add trade parameters needed by create_pf_for_params
        trade_param_template = {
            'risk_fraction': RISK_FRACTION,
            'atr_window': ATR_WINDOW_SIZING
        }
        wfo_logger.info(f"Generated {len(param_combinations)} parameter combinations to test per split.")

        # 4. Run WFO Loop with chat model assistance
        all_oos_portfolios = []
        best_params_per_split = []
        
        for split_idx, (train_indices, test_indices) in enumerate(splits):
            wfo_logger.info(f"--- Processing Split {split_idx + 1}/{len(splits)} ---")
            
            train_data = price_data.iloc[train_indices]
            test_data = price_data.iloc[test_indices]
            
            if chat_model and (split_idx == 0 or split_idx == len(splits) - 1):  # Check first and last splits
                period_check = ask_chat_model(chat_model,
                    "Please validate these training and testing periods:",
                    {
                        "split": split_idx + 1,
                        "train_period": f"{train_data.index[0]} to {train_data.index[-1]}",
                        "test_period": f"{test_data.index[0]} to {test_data.index[-1]}",
                        "train_rows": len(train_data),
                        "test_rows": len(test_data)
                    }
                )
                wfo_logger.info(f"Period Validation (Split {split_idx + 1}):\n{period_check}")

            # --- In-Sample Optimization ---
            best_split_metric = -np.inf
            best_split_params = None
            valid_params_count = 0
            param_iterator = tqdm(param_combinations, desc=f"Split {split_idx + 1} Train Opt", leave=False, unit="combo")

            for params in param_iterator:
                # Separate strategy params from trade params based on PARAM_GRID keys
                current_strategy_params = {k: v for k, v in params.items() if k in ['lookback_window', 'volatility_threshold', 'factor_weights', 'vol_filter_window']}
                current_trade_params = {k: v for k, v in params.items() if k in ['tsl_stop', 'tp_stop', 'atr_multiple_sl']}
                # Add fixed trade params
                current_trade_params.update(trade_param_template)

                # Create portfolio for this param set on training data
                train_pf = create_pf_for_params(train_data, current_strategy_params, current_trade_params)

                if train_pf is None:
                    continue # Skip if PF creation failed or no trades

                # Evaluate metric
                try:
                    stats = train_pf.stats(settings=dict(freq=train_pf.wrapper.freq)) # Pass freq explicitly
                    metric_value = stats.get(OPTIMIZATION_METRIC)

                    # Handle cases where metric might not exist (e.g., no trades)
                    if metric_value is None or not np.isfinite(metric_value):
                        metric_value = -np.inf # Treat missing/invalid metrics as worst score
                    
                    # Count valid parameter sets
                    valid_params_count += 1
                    wfo_logger.debug(f"Valid params found: {current_strategy_params} with metric {OPTIMIZATION_METRIC}={metric_value:.4f}")

                    # Handle metrics where higher is worse (e.g., Max Drawdown)
                    if OPTIMIZATION_METRIC == 'max_drawdown' and metric_value != -np.inf:
                         current_metric = -abs(metric_value) # More negative is worse
                    else:
                         current_metric = metric_value

                    if current_metric > best_split_metric:
                        best_split_metric = current_metric
                        best_split_params = params # Store the full parameter dict

                except Exception as eval_err:
                    wfo_logger.error(f"Error evaluating training portfolio for split {split_idx + 1}: {eval_err}", exc_info=False) # Don't need full traceback here usually
                    continue
            
            # Log the number of valid parameter sets found
            wfo_logger.info(f"Split {split_idx + 1}: Found {valid_params_count} valid parameter sets out of {len(param_combinations)} combinations.")

            # --- Out-of-Sample Evaluation ---
            if best_split_params is not None:
                wfo_logger.info(f"Best metric ({OPTIMIZATION_METRIC}) in split {split_idx + 1}: {best_split_metric:.4f}")
                wfo_logger.info(f"Best params: {best_split_params}")
                best_params_per_split.append({**best_split_params, 'split': split_idx + 1, 'metric_value': best_split_metric})

                # Separate best params for OOS run
                oos_strategy_params = {k: v for k, v in best_split_params.items() if k in ['lookback_window', 'volatility_threshold', 'factor_weights', 'vol_filter_window']}
                oos_trade_params = {k: v for k, v in best_split_params.items() if k in ['tsl_stop', 'tp_stop', 'atr_multiple_sl']}
                oos_trade_params.update(trade_param_template)

                # Run portfolio on test data with best params
                test_pf = create_pf_for_params(test_data, oos_strategy_params, oos_trade_params)

                if test_pf is not None:
                    wfo_logger.info(f"Successfully created OOS portfolio for split {split_idx + 1}.")
                    # Add benchmark returns to the OOS portfolio if available
                    if benchmark_rets is not None:
                         test_benchmark_rets = benchmark_rets.reindex(test_data.index).fillna(0)
                         test_pf.benchmark_returns = test_benchmark_rets
                    all_oos_portfolios.append(test_pf)
                else:
                    wfo_logger.warning(f"Could not create OOS portfolio for split {split_idx + 1} (likely no trades).")

            else:
                wfo_logger.warning(f"No valid parameters found during optimization for split {split_idx + 1}. Skipping OOS.")

            # Enhanced error handling in optimization loop
            if best_split_params is None and chat_model:
                optimization_analysis = ask_chat_model(chat_model,
                    f"No valid parameters found for split {split_idx + 1}. What might be the issue?",
                    {
                        "metric": OPTIMIZATION_METRIC,
                        "param_combinations_tested": len(param_combinations),
                        "data_period": f"{train_data.index[0]} to {train_data.index[-1]}"
                    }
                )
                wfo_logger.warning(f"Optimization Analysis (Split {split_idx + 1}):\n{optimization_analysis}")
            
            # Save checkpoint after each split
            if best_params_per_split:
                try:
                    checkpoint_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    checkpoint_filename = f"edge_wfo_checkpoint_split{split_idx+1}_{checkpoint_timestamp}.json"
                    checkpoint_path = OUTPUT_DIR / checkpoint_filename
                    
                    checkpoint_data = {
                        "best_params_per_split": best_params_per_split,
                        "completed_splits": split_idx + 1,
                        "total_splits": len(splits),
                        "optimization_metric": OPTIMIZATION_METRIC,
                        "timestamp": checkpoint_timestamp
                    }
                    
                    with open(checkpoint_path, 'w') as f:
                        json.dump(checkpoint_data, f, indent=2, default=str)
                    
                    wfo_logger.info(f"Saved checkpoint after split {split_idx+1}: {checkpoint_path}")
                except Exception as checkpoint_err:
                    wfo_logger.error(f"Error saving checkpoint: {checkpoint_err}")

        # --- Final Aggregation and Evaluation ---
        if not all_oos_portfolios:
            if chat_model:
                failure_analysis = ask_chat_model(chat_model,
                    "WFO failed to generate any OOS portfolios. What could be wrong?",
                    {
                        "splits_processed": len(splits),
                        "param_combinations": len(param_combinations),
                        "optimization_metric": OPTIMIZATION_METRIC
                    }
                )
                wfo_logger.critical(f"WFO failed. Analysis:\n{failure_analysis}")
            else:
                wfo_logger.critical("No OOS portfolios were generated. WFO failed. Check parameters and data.")
            return

        wfo_logger.info("--- Aggregating Out-of-Sample Results ---")
        # Combine the list of Portfolio objects into a single WFO portfolio
        # Note: This automatically handles concatenating returns, trades, logs etc.
        final_oos_pf = vbt.Portfolio.concat(*all_oos_portfolios,
                                            keys=[f'split_{i+1}' for i in range(len(all_oos_portfolios))], # Label each segment
                                            concat_func='concat', # Standard pandas concat
                                            save_state=True)      # Ensure state is saved for combined

        wfo_logger.info("Combined OOS portfolio created.")

        # --- Final Stats and Plots ---
        wfo_logger.info("--- Final Combined OOS Portfolio Stats ---")
        
        # Recalculate benchmark for the combined OOS period index
        if benchmark_rets is not None:
            final_oos_benchmark_rets = benchmark_rets.reindex(final_oos_pf.wrapper.index).fillna(0)
            final_oos_pf.benchmark_returns = final_oos_benchmark_rets # Set benchmark on the final object
        else:
            final_oos_pf.benchmark_returns = None # Ensure no stale benchmark data

        # Calculate final stats
        final_stats = final_oos_pf.stats() # Benchmark is included if set above
        # Use print for potentially large DataFrame output
        print("Final OOS Stats:")
        print(final_stats)

        # Calculate and log enhanced performance metrics from the final stats
        try:
            metrics = final_stats # Already calculated
            # Access returns stats if returns were saved (should be default)
            risk_metrics = final_oos_pf.returns.stats()

            calmar_ratio = metrics.get('calmar_ratio', np.nan)
            sortino_ratio = metrics.get('sortino_ratio', np.nan)
            omega_ratio = metrics.get('omega_ratio', np.nan)
            var_95 = risk_metrics.get('var_95', np.nan)
            cvar_95 = risk_metrics.get('cvar_95', np.nan)

            wfo_logger.info(f"Enhanced Performance Metrics for Combined OOS Period:")
            wfo_logger.info(f"Calmar Ratio: {calmar_ratio:.4f}")
            wfo_logger.info(f"Sortino Ratio: {sortino_ratio:.4f}")
            wfo_logger.info(f"Omega Ratio: {omega_ratio:.4f}")
            wfo_logger.info(f"Value at Risk (95%): {var_95:.4f}")
            wfo_logger.info(f"Conditional VaR (95%): {cvar_95:.4f}")
            
            # Add enhanced metrics to stats DataFrame before saving
            enhanced_metrics_dict = {
                'calmar_ratio': calmar_ratio,
                'sortino_ratio': sortino_ratio,
                'omega_ratio': omega_ratio,
                'var_95': var_95,
                'cvar_95': cvar_95
            }
            # Add as new rows or columns depending on preference
            # As rows (like original stats):
            for k, v in enhanced_metrics_dict.items():
                if k not in final_stats.index: # Avoid overwriting if already present
                    final_stats.loc[k] = v

        except Exception as metric_err:
            wfo_logger.error(f"Error calculating/accessing enhanced metrics: {metric_err}", exc_info=False)


        # --- Saving Results ---
        wfo_logger.info("Saving final WFO results...")
        try:
            run_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f"edge_wfo_{SYMBOL}_{GRANULARITY_STR}_{run_timestamp}"

            # Save Final Stats
            stats_df = pd.DataFrame(final_stats) # Ensure it's a DataFrame
            stats_path = OUTPUT_DIR / f'{base_filename}_stats.csv'
            stats_df.to_csv(stats_path)
            wfo_logger.info(f"Saved final stats: {stats_path}")

            # Save Parameter Evolution
            if best_params_per_split:
                params_df = pd.DataFrame(best_params_per_split)
                params_path = OUTPUT_DIR / f'{base_filename}_params.csv'
                params_df.to_csv(params_path, index=False)
                wfo_logger.info(f"Saved best parameters per split: {params_path}")

            # Save Plots (use vectorbtpro's built-in saving)
            # Ensure kaleido is installed (`pip install -U kaleido`) for image saving
            plot_settings = {'show': False, 'return_fig': True} # Don't show, just get fig

            equity_path = OUTPUT_DIR / f'{base_filename}_equity.png'
            fig_eq = final_oos_pf.plot(**plot_settings)
            fig_eq.write_image(str(equity_path))
            wfo_logger.info(f"Saved equity plot: {equity_path}")

            dd_path = OUTPUT_DIR / f'{base_filename}_drawdowns.png'
            fig_dd = final_oos_pf.plot_drawdowns(**plot_settings)
            fig_dd.write_image(str(dd_path))
            wfo_logger.info(f"Saved drawdowns plot: {dd_path}")

            trades_path = OUTPUT_DIR / f'{base_filename}_trades.png'
            # Plotting trades can be slow for many trades
            if final_oos_pf.trades.count() > 0:
                 try:
                     fig_trades = final_oos_pf.trades.plot(**plot_settings)
                     fig_trades.write_image(str(trades_path))
                     wfo_logger.info(f"Saved trades plot: {trades_path}")
                 except Exception as trade_plot_err:
                     wfo_logger.warning(f"Could not generate trades plot: {trade_plot_err}")
            else:
                 wfo_logger.info("Skipping trades plot as there were no trades in the combined OOS period.")

            # Optional: Save the final portfolio object itself
            # pf_path = OUTPUT_DIR / f'{base_filename}_portfolio.pkl'
            # final_oos_pf.save(pf_path)
            # wfo_logger.info(f"Saved final portfolio object: {pf_path}")

        except Exception as save_err:
           wfo_logger.error(f"Error saving final WFO results: {save_err}", exc_info=True)

        wfo_logger.info("--- Walk-Forward Optimization Finished ---")

    except Exception as e:
        if chat_model:
            error_analysis = ask_chat_model(chat_model,
                "An unhandled error occurred in WFO. Please analyze:",
                {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "wfo_config": {
                        "symbol": SYMBOL,
                        "granularity": GRANULARITY_STR,
                        "dates": f"{WFO_START_DATE} to {WFO_END_DATE}",
                        "is_days": IN_SAMPLE_DAYS,
                        "oos_days": OUT_SAMPLE_DAYS
                    }
                }
            )
            wfo_logger.critical(f"WFO Error Analysis:\n{error_analysis}")
        wfo_logger.critical(f"An unhandled error occurred in run_walk_forward_optimization: {e}", exc_info=True)
        raise


# =============================================================================
# Main Execution Block
# =============================================================================
if __name__ == "__main__":
    wfo_logger.info("Executing WFO script...")
    try:
        run_walk_forward_optimization()
        wfo_logger.info("Script execution completed successfully.")
    except Exception as main_err:
        wfo_logger.critical(f"Script failed with error: {main_err}")
        # Optionally exit with error code
        sys.exit(1) 