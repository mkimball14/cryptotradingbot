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
import multiprocessing
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import inspect
from dotenv import load_dotenv
import time
import pandas_ta as ta

# Note: This is a partial file containing the optimized configuration. 
# The rest of the original script's functions need to be added.

# Placeholder imports - replace with actual imports from original script if needed
try:
    from scripts.strategies.edge_strategy_assistant import create_portfolio
except ModuleNotFoundError:
    from edge_strategy_assistant import create_portfolio
try:
    from scripts.strategies.candlestick_pattern_strategy import CandlestickPatternStrategy
except ModuleNotFoundError:
    from candlestick_pattern_strategy import CandlestickPatternStrategy
try:
    from scripts.portfolio.custom_portfolio import CustomPortfolio
except ImportError:
    CustomPortfolio = None # Placeholder
    pass # Define dummy functions if needed

def fetch_historical_data(*args, **kwargs): return pd.DataFrame({'open': [], 'high': [], 'low': [], 'close': [], 'volume': []})
def get_vbt_freq_str(*args, **kwargs): return "1h"
GRANULARITY_MAP_SECONDS = {'1h': 3600}

load_dotenv(verbose=True)

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
wfo_logger = logging.getLogger('wfo_edge_strategy_optimized')
wfo_logger.setLevel(logging.INFO)

# =============================================================================
# Optimized Configuration Constants
# =============================================================================

# --- WFO Parameters (Optimized for Speed) ---
IN_SAMPLE_DAYS = 50       # Shorter training period
OUT_SAMPLE_DAYS = 20      # Shorter testing period
STEP_DAYS = 25            # Shorter step

# --- Data Parameters (Optimized for Speed) ---
TOTAL_HISTORY_DAYS = 180 # Significantly reduced history
WFO_END_DATE = datetime.now().strftime('%Y-%m-%d')
WFO_START_DATE = (datetime.now() - timedelta(days=TOTAL_HISTORY_DAYS)).strftime('%Y-%m-%d')
SYMBOL = "BTC-USD"
GRANULARITY_STR = "1h" 
try:
    GRANULARITY_SECONDS = GRANULARITY_MAP_SECONDS[GRANULARITY_STR]
except KeyError:
    wfo_logger.error(f"Invalid GRANULARITY_STR: {GRANULARITY_STR}. Defaulting to 1h (3600s).")
    GRANULARITY_SECONDS = 3600
BENCHMARK_SYMBOL = "BTC-USD" 

# --- Trading Parameters ---
INITIAL_CAPITAL = 3000
COMMISSION_PCT = 0.001
SLIPPAGE_PCT = 0.0005
RISK_FRACTION = 0.01      
ATR_WINDOW_SIZING = 14   

# --- Strategy Selection ---
STRATEGY_TYPE = "candlestick"  # Options: "edge_multi_factor", "candlestick"

# --- Optimization Parameters (Optimized for Speed) ---
OPTIMIZATION_METRIC = 'sharpe_ratio' 

# Define parameter grids (Simplified for speed)
EDGE_MULTI_FACTOR_PARAM_GRID_FAST = {
    'rsi_window': [10, 20],      
    'rsi_entry': [25, 35],      
    'rsi_exit': [60, 70],       
    'bb_window': [15, 25],      
    'bb_dev': [2.0, 2.5],     
    'vol_window': [10, 20],      
    'vol_threshold': [0.5, 1.0], 
    'sl_pct': [1.0, 2.0],     
    'tp_pct': [2.0, 4.0],     
    'risk_per_trade': [0.01, 0.02]  
}

CANDLESTICK_PARAM_GRID_FAST = {
    'lookback_periods': [20, 40],
    'min_strength': [0.01, 0.03],
    'use_strength': [True, False],
    'use_confirmation': [True, False], 
    'confirmation_window': [2, 3], 
    'stop_loss_pct': [0.02, 0.04],
    'take_profit_pct': [0.05, 0.08],
    'risk_per_trade': [0.01, 0.02]
}

# Use the appropriate parameter grid based on strategy type
PARAM_GRID = CANDLESTICK_PARAM_GRID_FAST if STRATEGY_TYPE == "candlestick" else EDGE_MULTI_FACTOR_PARAM_GRID_FAST

# --- Performance Optimization Settings ---
USE_PARALLEL = True
NUM_CORES = max(1, multiprocessing.cpu_count() - 1)  
ENABLE_CACHING = True
VERBOSE_DEBUG = False  

# Force quick test settings 
QUICK_TEST = True # Set to True to force fast settings
if QUICK_TEST:
    # Override PARAM_GRID with the fast version 
    PARAM_GRID = CANDLESTICK_PARAM_GRID_FAST if STRATEGY_TYPE == "candlestick" else EDGE_MULTI_FACTOR_PARAM_GRID_FAST
    
    # Override WFO and Data parameters specifically for QUICK_TEST
    IN_SAMPLE_DAYS = 50
    OUT_SAMPLE_DAYS = 20
    STEP_DAYS = 25
    TOTAL_HISTORY_DAYS = 180 
    WFO_START_DATE = (datetime.now() - timedelta(days=TOTAL_HISTORY_DAYS)).strftime('%Y-%m-%d')
    wfo_logger.info("QUICK_TEST settings are active. Using reduced parameter grid and data range.")

# Adjust performance criteria (lenient for testing)
MIN_SHARPE_RATIO = 0.1   
MIN_TOTAL_TRADES = 3     
MIN_WIN_RATE = 0.3       
MAX_DRAWDOWN = -0.35     

# =============================================================================
# Helper Functions (Copied from original)
# =============================================================================

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


def extract_candle_patterns(df: pd.DataFrame, pattern_list: List[str] = None) -> pd.DataFrame:
    """
    Extract candle patterns from OHLCV data using pandas_ta.
    
    Args:
        df: DataFrame with open, high, low, close columns
        pattern_list: List of patterns to identify. If None, all patterns will be extracted.
            Available patterns: 'doji', 'hammer', 'inverted_hammer', 'hanging_man', 
            'shooting_star', 'engulfing', 'morning_star', 'evening_star', etc.
            Or use 'all' to get all available patterns.
    
    Returns:
        DataFrame with candle pattern signals (1 for bullish, -1 for bearish, 0 for none)
    """
    # Create a copy of the input DataFrame
    result_df = df.copy()
    
    try:
        # Convert column names to lowercase if needed
        required_cols = ['open', 'high', 'low', 'close']
        rename_map = {col.upper(): col for col in required_cols if col not in df.columns and col.upper() in df.columns}
        
        if rename_map:
            # Create a temporary DataFrame with lowercase columns
            temp_df = df.rename(columns=rename_map)
        else:
            temp_df = df.copy()
            
        # Ensure required columns exist
        missing_cols = [col for col in required_cols if col not in temp_df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Handle pattern_list input
        if pattern_list is None or 'all' in pattern_list:
            # Run cdl_pattern for all available patterns
            patterns = temp_df.ta.cdl_pattern(name="all")
        else:
            # Run for specific patterns
            patterns = pd.DataFrame(index=temp_df.index)
            for pattern in pattern_list:
                pattern_result = temp_df.ta.cdl_pattern(name=pattern)
                if not pattern_result.empty:
                    for col in pattern_result.columns:
                        patterns[col] = pattern_result[col]
        
        # Merge the patterns with the result DataFrame
        if not patterns.empty:
            for col in patterns.columns:
                result_df[col] = patterns[col]
                
        return result_df
        
    except Exception as e:
        wfo_logger.error(f"Error extracting candle patterns: {str(e)}")
        # Return the original DataFrame if there's an error
        return result_df


def get_candle_pattern_strength(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """
    Calculate the strength of candle patterns based on historical reliability.
    
    Args:
        df: DataFrame with candle pattern signals and price data
        lookback: Number of past occurrences to analyze for each pattern
    
    Returns:
        DataFrame with pattern strength metrics
    """
    result_df = df.copy()
    
    try:
        # Get all pattern columns
        pattern_cols = [col for col in df.columns if col.startswith('CDL')]
        
        if not pattern_cols:
            wfo_logger.warning("No candle pattern columns found. Run extract_candle_patterns first.")
            return result_df
            
        # Create forward returns for 1, 3, and 5 days
        try:
            result_df['return_1d'] = df['close'].pct_change(1).shift(-1)
            result_df['return_3d'] = df['close'].pct_change(3).shift(-3)
            result_df['return_5d'] = df['close'].pct_change(5).shift(-5)
        except Exception as e:
            wfo_logger.warning(f"Error calculating returns: {e}. Using default strength values.")
            # Set default strength values
            for pattern in pattern_cols:
                strength_col = f"{pattern}_strength"
                result_df[strength_col] = df[pattern].abs() * 0.01  # Simple default strength
            return result_df
        
        # Calculate pattern strength for each pattern
        for pattern in pattern_cols:
            # Create columns for pattern strength
            strength_col = f"{pattern}_strength"
            result_df[strength_col] = 0.0
            
            # Process each day
            for i in range(lookback, len(df)):
                # Get the current pattern value
                current_value = df[pattern].iloc[i]
                
                # Skip if no pattern detected
                if current_value == 0:
                    continue
                    
                # Get historical pattern occurrences (same sign)
                hist_window = df[pattern].iloc[i-lookback:i]
                hist_indices = hist_window[hist_window == current_value].index
                
                if len(hist_indices) > 0:
                    try:
                        # Calculate the average return after pattern
                        if current_value > 0:  # Bullish pattern
                            avg_return_1d = df.loc[hist_indices, 'return_1d'].mean()
                            avg_return_3d = df.loc[hist_indices, 'return_3d'].mean()
                            avg_return_5d = df.loc[hist_indices, 'return_5d'].mean()
                        else:  # Bearish pattern
                            avg_return_1d = -df.loc[hist_indices, 'return_1d'].mean()
                            avg_return_3d = -df.loc[hist_indices, 'return_3d'].mean()
                            avg_return_5d = -df.loc[hist_indices, 'return_5d'].mean()
                        
                        # Handle NaN values using nanmean if available or check pd.isna
                        avg_return_1d = 0.0 if pd.isna(avg_return_1d) else avg_return_1d
                        avg_return_3d = 0.0 if pd.isna(avg_return_3d) else avg_return_3d
                        avg_return_5d = 0.0 if pd.isna(avg_return_5d) else avg_return_5d
                        
                        # Calculate weighted strength based on returns
                        weighted_strength = (
                            0.5 * avg_return_1d + 
                            0.3 * avg_return_3d + 
                            0.2 * avg_return_5d
                        )
                        
                        # Account for frequency
                        frequency = len(hist_indices) / lookback
                        
                        # Calculate final strength
                        strength = weighted_strength * frequency * abs(current_value)
                        
                        # Store the strength value
                        result_df.loc[df.index[i], strength_col] = strength
                    except Exception as inner_e:
                        # If calculation fails, use a default strength value
                        default_strength = abs(current_value) * 0.01  # Simple default based on pattern value
                        result_df.loc[df.index[i], strength_col] = default_strength
        
        return result_df
        
    except Exception as e:
        wfo_logger.error(f"Error calculating candle pattern strength: {str(e)}")
        # Return the original DataFrame with default strength values if available
        for pattern in [col for col in df.columns if col.startswith('CDL')]:
            strength_col = f"{pattern}_strength"
            if strength_col not in result_df.columns:
                result_df[strength_col] = df[pattern].abs() * 0.01  # Simple default strength
        return result_df


def generate_candle_pattern_signals(df: pd.DataFrame, min_strength: float = 0.01, 
                                    use_strength: bool = True) -> Tuple[pd.Series, pd.Series]:
    """
    Generate trading signals based on candle patterns and their strength.
    
    Args:
        df: DataFrame with candle pattern signals and strength metrics
        min_strength: Minimum strength threshold for generating signals
        use_strength: Whether to use pattern strength for signal generation
    
    Returns:
        Tuple containing (buy_signals, sell_signals)
    """
    try:
        # Get all pattern columns
        pattern_cols = [col for col in df.columns if col.startswith('CDL')]
        strength_cols = [col for col in df.columns if col.endswith('_strength')]
        
        if not pattern_cols:
            wfo_logger.warning("No candle pattern columns found. Run extract_candle_patterns first.")
            return pd.Series(False, index=df.index), pd.Series(False, index=df.index)
            
        # Initialize signal series
        buy_signals = pd.Series(False, index=df.index)
        sell_signals = pd.Series(False, index=df.index)
        
        if use_strength and strength_cols:
            # Using pattern strength for signals
            
            # Calculate net pattern strength
            df['net_bullish_strength'] = 0.0
            df['net_bearish_strength'] = 0.0
            
            for pattern in pattern_cols:
                strength_col = f"{pattern}_strength"
                if strength_col in df.columns:
                    # Add to bullish strength if pattern is bullish and strength is positive
                    bullish_mask = (df[pattern] > 0) & (df[strength_col] > 0)
                    df.loc[bullish_mask, 'net_bullish_strength'] += df.loc[bullish_mask, strength_col]
                    
                    # Add to bearish strength if pattern is bearish and strength is positive
                    bearish_mask = (df[pattern] < 0) & (df[strength_col] > 0)
                    df.loc[bearish_mask, 'net_bearish_strength'] += df.loc[bearish_mask, strength_col]
            
            # Generate signals based on net strength
            buy_signals = df['net_bullish_strength'] > min_strength
            sell_signals = df['net_bearish_strength'] > min_strength
            
        else:
            # Using raw pattern signals
            for pattern in pattern_cols:
                # Add buy signals for bullish patterns
                buy_signals = buy_signals | (df[pattern] > 0)
                
                # Add sell signals for bearish patterns
                sell_signals = sell_signals | (df[pattern] < 0)
        
        return buy_signals, sell_signals
        
    except Exception as e:
        wfo_logger.error(f"Error generating candle pattern signals: {str(e)}")
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index)


# --- Remaining functions placeholder ---


# Example placeholder for main execution
if __name__ == "__main__":
    # ... (original placeholder code) ...
    pass

# --- Functions copied from original wfo_edge_strategy.py --- 

# Check and install missing dependencies
def check_and_install_dependencies():
    """Check for required dependencies and install if missing."""
    try:
        import lmdbm
        logging.getLogger().info("lmdbm package is already installed.")
    except ImportError:
        logging.getLogger().warning("lmdbm package is missing. Attempting to install...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "lmdbm"])
            logging.getLogger().info("Successfully installed lmdbm package.")
            # Import it now to make sure it's available
            import lmdbm
        except Exception as e:
            logging.getLogger().error(f"Failed to install lmdbm package: {e}")

# Check and install dependencies
check_and_install_dependencies()

# Ensure OpenAI API key is set, using OpenRouter API key if needed
openai_api_key = os.environ.get("OPENAI_API_KEY")
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
github_token = os.environ.get("GITHUB_TOKEN")

# If OPENAI_API_KEY is not set but OPENROUTER_API_KEY is available, use it
if not openai_api_key and openrouter_api_key:
    # Explicitly set in os.environ
    os.environ["OPENAI_API_KEY"] = openrouter_api_key
    logging.getLogger().info("Set OPENAI_API_KEY from OPENROUTER_API_KEY for compatibility.")
    openai_api_key = openrouter_api_key

if openai_api_key:
    # Explicitly set OPENAI_API_KEY in os.environ
    os.environ["OPENAI_API_KEY"] = openai_api_key
    logging.getLogger().info("Explicitly set OPENAI_API_KEY in os.environ.")
else:
    logging.getLogger().warning("Neither OPENAI_API_KEY nor OPENROUTER_API_KEY found. Chat features will be disabled.")

if github_token:
    os.environ["GITHUB_TOKEN"] = github_token
    logging.getLogger().info("Explicitly set GITHUB_TOKEN in os.environ.")
else:
    logging.getLogger().warning("GITHUB_TOKEN not found. Chat features may be limited.")

# NOTE: init_logging is already handled at the top of the optimized file
# --- Setup Paths ---
# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Define output directory relative to this script
OUTPUT_DIR = Path(__file__).resolve().parent / 'wfo_results_optimized'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Create if it doesn't exist

# --- Import Strategy and Data Fetcher (Ensure correct paths/imports if different) ---
try:
    # Use the correct relative path based on standard project structure
    from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
    wfo_logger.info("Successfully imported refactored EdgeMultiFactorStrategy.")
except ImportError as e:
    wfo_logger.error(f"Could not import EdgeMultiFactorStrategy: {e}")
    # Attempt fallback if path structure is different
    try:
        from edge_multi_factor_fixed import EdgeMultiFactorStrategy
        wfo_logger.info("Imported EdgeMultiFactorStrategy from current directory.")
    except ImportError:
        wfo_logger.warning("EdgeMultiFactorStrategy not found. Candlestick strategy will be used if selected.")
        EdgeMultiFactorStrategy = None # Set to None if unavailable

# --- NEW JSON DEFAULT FUNCTION ---
def json_encoder_default(obj):
    """Custom default function for json.dump to handle non-serializable types."""
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float16, np.float32, np.float64)):
        # Handle potential infinity/NaN from numpy floats
        if np.isinf(obj) or np.isnan(obj):
            return None
        return float(obj)
    elif hasattr(np, 'floating') and isinstance(obj, np.floating):
        if np.isinf(obj) or np.isnan(obj):
            return None
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return str(obj) # Explicitly convert numpy and python bools to string
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (pd.Timestamp, datetime)):
        return obj.isoformat()
    elif isinstance(obj, (pd.Timedelta, timedelta)):
        return str(obj)
    elif pd.isna(obj):
        return None
    elif obj is pd.NA:
        return None
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
# --- END NEW JSON DEFAULT FUNCTION ---

# --- VectorBT Pro Chat Model Configuration --- NEW FUNCTION
def setup_chat_provider():
    """Configure the chat provider for debugging and optimization advice."""
    try:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        if not openai_api_key and not openrouter_api_key:
            wfo_logger.warning("Neither OPENAI_API_KEY nor OPENROUTER_API_KEY found. Chat features disabled.")
            return False
        api_key = openai_api_key or openrouter_api_key
        os.environ["OPENAI_API_KEY"] = api_key
        use_openrouter = bool(openrouter_api_key)
        api_base_url = openrouter_base_url if use_openrouter else None
        model = "openrouter/auto" if use_openrouter else "gpt-3.5-turbo"
        try:
            from openai import OpenAI
            if use_openrouter:
                try:
                    client = OpenAI(api_key=openrouter_api_key, base_url=api_base_url)
                    client.chat.completions.create(model="openrouter/auto", messages=[{"role": "user", "content": "Test"}], max_tokens=5)
                    wfo_logger.info("OpenRouter API key validated.")
                except Exception as e:
                    wfo_logger.error(f"OpenRouter direct API test failed: {e}")
                    return False
        except ImportError:
            wfo_logger.warning("OpenAI package not available.")
        import vectorbtpro as vbt
        configured = False
        # Simplified configuration attempts (add more if needed based on original)
        if hasattr(vbt, 'settings') and hasattr(vbt.settings, 'knowledge') and hasattr(vbt.settings.knowledge, 'chat'):
             vbt.settings.knowledge.chat.openai_key = api_key
             if api_base_url: vbt.settings.knowledge.chat.openai_base_url = api_base_url
             vbt.settings.knowledge.chat.model = model
             configured = True
             wfo_logger.info("Configured chat via knowledge.chat.")
        # Add other config paths (kb.chat, litellm, direct openai) if present in original
        if configured: return True
        wfo_logger.warning("Could not configure chat provider.")
        return False
    except Exception as e:
        wfo_logger.error(f"Failed to configure chat provider: {str(e)}")
        return False

def get_chat_model():
    """Get a configured chat model instance."""
    try:
        if not setup_chat_provider(): return None
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        if openrouter_api_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openrouter_api_key, base_url=openrouter_base_url)
                def direct_chat(prompt):
                    try:
                        completion = client.chat.completions.create(model="openrouter/auto", messages=[{"role": "user", "content": prompt}], max_tokens=1000)
                        return completion.choices[0].message.content
                    except Exception as e:
                        wfo_logger.error(f"OpenRouter direct chat error: {e}")
                        return f"Error: {str(e)}"
                wfo_logger.info("Using direct OpenRouter chat function.")
                return direct_chat
            except Exception as e:
                wfo_logger.error(f"Failed to create direct_chat: {e}")
        import vectorbtpro as vbt
        if hasattr(vbt, 'chat') and callable(vbt.chat):
            wfo_logger.info("Using vbt.chat function.")
            return vbt.chat
        try:
            from vectorbtpro.utils.knowledge.chatting import ChatModel
            chat_model = ChatModel()
            wfo_logger.info("Using ChatModel from utils.knowledge.chatting.")
            return chat_model
        except (ImportError, AttributeError):
             wfo_logger.warning("Could not find any chat model in vectorbtpro.")
             return None
    except Exception as e:
        wfo_logger.error(f"Error getting chat model: {e}")
        return None

def ask_chat_model(query, context=None):
    """Query the chat model."""
    full_prompt = query
    if context: full_prompt += "\n\nContext:\n" + "\n".join([f"{k}: {v}" for k, v in context.items()])
    chat_model = get_chat_model()
    if chat_model is None: return "Chat model not available."
    try:
        return chat_model(full_prompt)
    except Exception as e:
        wfo_logger.error(f"Error querying chat model: {e}")
        return f"Error querying chat model: {e}"

def chat_model_available():
    """Check if chat model is available."""
    return get_chat_model() is not None

def optimize_pattern_signal_parameters(df: pd.DataFrame, test_length: int = 252, min_trades: int = 10) -> Dict[str, Any]:
    """Optimize parameters for candle pattern signal generation."""
    try:
        train_df = df.iloc[:-test_length]
        test_df = df.iloc[-test_length:]
        min_strength_values = [0.005, 0.01, 0.02, 0.03, 0.05, 0.1]
        lookback_values = [10, 20, 30, 50, 100]
        best_params = {'min_strength': 0.01, 'lookback': 20, 'use_strength': True}
        best_sharpe = -np.inf
        for min_strength in min_strength_values:
            for lookback in lookback_values:
                for use_strength in [True, False]:
                    train_with_strength = get_candle_pattern_strength(train_df, lookback=lookback)
                    test_with_strength = get_candle_pattern_strength(test_df, lookback=lookback)
                    buy_signals, sell_signals = generate_candle_pattern_signals(test_with_strength, min_strength=min_strength, use_strength=use_strength)
                    num_buys, num_sells = buy_signals.sum(), sell_signals.sum()
                    if num_buys + num_sells < min_trades: continue
                    positions = pd.Series(0, index=test_df.index)
                    positions[buy_signals], positions[sell_signals] = 1, -1
                    daily_returns = test_df['close'].pct_change() * positions.shift(1)
                    if daily_returns.count() < 20: continue
                    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252) if daily_returns.std() != 0 else 0
                    if pd.notna(sharpe) and sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_params = {'min_strength': min_strength, 'lookback': lookback, 'use_strength': use_strength, 'sharpe': sharpe, 'num_buys': num_buys, 'num_sells': num_sells}
        wfo_logger.info(f"Optimized candle pattern parameters: {best_params}")
        return best_params
    except Exception as e:
        wfo_logger.error(f"Error optimizing pattern signals: {str(e)}")
        return {'min_strength': 0.01, 'lookback': 20, 'use_strength': True}

def create_portfolio_for_strategy(data, entries, exits, init_cash=INITIAL_CAPITAL, size=None, stop_loss=None, take_profit=None, direction='long'):
    """Create a portfolio using vectorbt or CustomPortfolio."""
    try:
        if not isinstance(data, pd.DataFrame) or 'close' not in data.columns: raise ValueError("Data must be DataFrame with 'close' column")
        entries = pd.Series(entries, index=data.index).astype(np.bool_) if not isinstance(entries, pd.Series) else entries.astype(np.bool_)
        exits = pd.Series(exits, index=data.index).astype(np.bool_) if not isinstance(exits, pd.Series) else exits.astype(np.bool_)
        direction_value = 1 if direction == 'long' else -1
        freq = get_vbt_freq_str(GRANULARITY_STR)
        pf_kwargs = dict(close=data['close'], entries=entries, exits=exits, size=size, size_type='amount' if size is not None else 'value',
                         init_cash=init_cash, fees=COMMISSION_PCT, slippage=SLIPPAGE_PCT, freq=freq, direction=direction_value)
        
        # Attempt to use CustomPortfolio if SL/TP are set and it's available
        use_custom_pf = (stop_loss is not None or take_profit is not None) and CustomPortfolio is not None
        
        if use_custom_pf:
             try:
                 pf_kwargs['stop_loss'] = stop_loss
                 pf_kwargs['take_profit'] = take_profit
                 portfolio = CustomPortfolio.from_signals(**pf_kwargs)
                 wfo_logger.debug(f"Created CustomPortfolio with SL={stop_loss}, TP={take_profit}")
                 return portfolio
             except Exception as e:
                 wfo_logger.warning(f"Failed CustomPortfolio: {e}, falling back to standard Portfolio.")
                 if 'stop_loss' in pf_kwargs: del pf_kwargs['stop_loss']
                 if 'take_profit' in pf_kwargs: del pf_kwargs['take_profit']
        
        # Standard portfolio creation or fallback
        portfolio = vbt.Portfolio.from_signals(**pf_kwargs)
        wfo_logger.debug("Created standard vbt.Portfolio.")
        return portfolio
        
    except Exception as e:
        wfo_logger.error(f"Error creating portfolio: {str(e)}")
        return None

def create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL):
    """Create a vectorbt Portfolio object for EdgeMultiFactorStrategy params."""
    try:
        df = data.copy()
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if any(col not in df.columns for col in required_columns): raise ValueError("Missing OHLCV columns")
        
        # Extract params safely with defaults
        rsi_window = int(params.get('rsi_window', 14))
        rsi_entry = float(params.get('rsi_entry', 30))
        rsi_exit = float(params.get('rsi_exit', 70))
        bb_window = int(params.get('bb_window', 20))
        bb_dev = float(params.get('bb_dev', 2.0))
        vol_window = int(params.get('vol_window', 20))
        vol_threshold = float(params.get('vol_threshold', 0.5))
        sl_pct = float(params.get('sl_pct', 0.05))
        tp_pct = float(params.get('tp_pct', 0.1))
        risk_per_trade = float(params.get('risk_per_trade', 0.02))
        
        # Calculate indicators
        rsi = vbt.RSI.run(df['close'], window=rsi_window).rsi
        bb = vbt.BollingerBands.run(df['close'], window=bb_window, alpha=bb_dev)
        df['volatility'] = df['close'].pct_change().rolling(window=vol_window).std()
        
        # Generate signals
        long_entry = (rsi < rsi_entry) & (df['close'] < bb.lower) & (df['volatility'] > vol_threshold)
        long_exit = (rsi > rsi_exit) | (df['close'] > bb.upper)
        
        # Calculate position size
        size = calculate_position_size(signal=long_entry, price=df['close'], stop_loss_pct=sl_pct, risk_pct=risk_per_trade, capital=init_cash)
        
        # Create portfolio using the unified function
        return create_portfolio_for_strategy(df, long_entry, long_exit, init_cash, size, sl_pct, tp_pct)
        
    except Exception as e:
        wfo_logger.error(f"Error in create_pf_for_params: {str(e)}")
        return None

def calculate_position_size(signal, price, stop_loss_pct, risk_pct, capital):
    """Calculate position size based on risk per trade."""
    size = pd.Series(0.0, index=signal.index)
    entry_indices = signal[signal].index
    if entry_indices.empty: return size
    
    entry_prices = price.loc[entry_indices]
    risk_amount = capital * risk_pct
    price_distance = entry_prices * stop_loss_pct
    
    # Ensure no division by zero or negative distance (use small epsilon)
    valid_distance_mask = price_distance > 1e-9 
    valid_indices = entry_indices[valid_distance_mask]
    
    if not valid_indices.empty:
        calculated_size = risk_amount / price_distance.loc[valid_indices]
        size.loc[valid_indices] = calculated_size
        
    return size

def evaluate_parameter_set(data, params, split_id=None):
    """Evaluate a parameter set on the given data."""
    try:
        if STRATEGY_TYPE == "candlestick":
            lookback_periods = params.get('lookback_periods', 20)
            min_strength = params.get('min_strength', 0.01)
            use_strength = params.get('use_strength', True)
            use_confirmation = params.get('use_confirmation', True)
            confirmation_window = params.get('confirmation_window', 3)
            stop_loss_pct = params.get('stop_loss_pct', 0.03)
            take_profit_pct = params.get('take_profit_pct', 0.06)
            risk_per_trade = params.get('risk_per_trade', 0.02)
            
            df_with_patterns = extract_candle_patterns(data)
            if use_strength: df_with_patterns = get_candle_pattern_strength(df_with_patterns, lookback=lookback_periods)
            entries, exits = generate_candle_pattern_signals(df_with_patterns, min_strength=min_strength, use_strength=use_strength)
            
            if use_confirmation:
                # Simple confirmation: Check if the next `confirmation_window` candles close higher/lower
                price_change = data['close'].diff(confirmation_window).shift(-confirmation_window)
                confirmed_entries = pd.Series(False, index=entries.index)
                confirmed_entries[(entries > 0) & (price_change > 0)] = True # Bullish confirmation
                confirmed_entries[(entries < 0) & (price_change < 0)] = True # Bearish confirmation - Needs adjustment for sell signal logic
                # Note: generating sell signals (entries < 0) wasn't fully implemented for confirmation, 
                # assuming long-only for this confirmation part for now. 
                # If shorting, bearish entry confirmation needs careful definition.
                entries = confirmed_entries & entries # Keep only confirmed entries
            
            size = calculate_position_size(signal=entries, price=data['close'], stop_loss_pct=stop_loss_pct, risk_pct=risk_per_trade, capital=INITIAL_CAPITAL)
            portfolio = create_pf_for_candlestick_strategy(data=data, entries=entries, exits=exits, init_cash=INITIAL_CAPITAL, size=size, sl_stop=stop_loss_pct, tp_stop=take_profit_pct)
        
        elif STRATEGY_TYPE == "edge_multi_factor" and EdgeMultiFactorStrategy: # Check if the class exists
             portfolio = create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL)
        else:
             wfo_logger.error(f"Strategy type '{STRATEGY_TYPE}' not supported or EdgeMultiFactorStrategy unavailable.")
             return None, None, params, split_id
             
        metrics = calculate_performance_metrics(portfolio)
        return portfolio, metrics, params, split_id
        
    except Exception as e:
        wfo_logger.error(f"Error evaluating param set {params} for split {split_id}: {str(e)}")
        return None, None, params, split_id

def calculate_performance_metrics(portfolio):
    """Calculate key performance metrics."""
    metrics = {
        'sharpe': 0, 'calmar': 0, 'max_dd': 0, 'total_return': 0, 
        'win_rate': 0, 'volatility': 0, 'var': 0, 'num_trades': 0, 
        'profit_factor': 0, 'avg_trade': 0
    }
    if portfolio is None: return metrics
    
    try:
        # Get basic stats
        stats = portfolio.stats() if callable(getattr(portfolio, 'stats', None)) else getattr(portfolio, 'stats', {})
        metrics.update({
            'sharpe': stats.get('sharpe_ratio', 0),
            'calmar': stats.get('calmar_ratio', 0),
            'max_dd': stats.get('max_drawdown', 0),
            'total_return': stats.get('total_return', 0),
            'win_rate': stats.get('win_rate', 0),
            'profit_factor': stats.get('profit_factor', 0),
            'avg_trade': stats.get('avg_trade', 0)
        })

        # Get risk metrics
        risk = portfolio.get_risk_metrics() if hasattr(portfolio, 'get_risk_metrics') else {}
        metrics['volatility'] = risk.get('annual_volatility', risk.get('volatility', 0))
        metrics['var'] = risk.get('value_at_risk', risk.get('var', 0))
        
        # Get trade count from trades object if possible
        if hasattr(portfolio, 'trades') and hasattr(portfolio.trades, 'count'):
             metrics['num_trades'] = portfolio.trades.count() if callable(portfolio.trades.count) else portfolio.trades.count
        elif hasattr(portfolio, 'trades') and hasattr(portfolio.trades, 'records_readable'):
             metrics['num_trades'] = len(portfolio.trades.records_readable)
        elif 'total_trades' in stats: # Fallback to stats if available
             metrics['num_trades'] = stats.get('total_trades', 0)

        # Clean up NaN/inf values
        for k, v in metrics.items():
            if pd.isna(v) or np.isinf(v):
                metrics[k] = 0

    except Exception as e:
        wfo_logger.warning(f"Error calculating metrics: {str(e)}")
        # Return default zeroed metrics on error
        metrics = {k: 0 for k in metrics}
        
    return metrics

def create_pf_for_candlestick_strategy(data, entries, exits, init_cash=INITIAL_CAPITAL, size=None, sl_stop=None, tp_stop=None):
    """Wrapper for create_portfolio_for_strategy for candlestick strategy."""
    # Convert percentage strings to floats if necessary
    if isinstance(sl_stop, str) and '%' in sl_stop:
        sl_stop = float(sl_stop.strip(' %')) / 100
    if isinstance(tp_stop, str) and '%' in tp_stop:
        tp_stop = float(tp_stop.strip(' %')) / 100
        
    # Ensure they are floats if not None
    sl_stop = float(sl_stop) if sl_stop is not None else None
    tp_stop = float(tp_stop) if tp_stop is not None else None
    
    return create_portfolio_for_strategy(data, entries, exits, init_cash, size, sl_stop, tp_stop)

# Wrapper for parallel processing (Needs to be defined at the top level)
def evaluate_single_param_set_wrapper(args):
    """Wrapper for evaluate_parameter_set suitable for multiprocessing."""
    data, params, split_id = args
    # Use try-except to handle potential errors during evaluation in parallel process
    try:
        # Ensure data is copied if needed for true parallelism without side effects
        result = evaluate_parameter_set(data.copy(), params, split_id)
        return result
    except Exception as e:
        # Log the error from within the worker process if possible
        # Or return None/Structure indicating failure
        # print(f"Error in worker for split {split_id}, params {params}: {e}") # Simple print for debug
        return None, None, params, split_id # Match expected return structure on failure

# --- Main Execution Block --- 
if __name__ == "__main__":
    wfo_logger.info("Optimized WFO script starting...")
    
    # Ensure actual data fetcher is available, otherwise use placeholder
    try:
        from data.data_fetcher import fetch_historical_data as actual_fetch_historical_data
        wfo_logger.info("Using actual data_fetcher from data module.")
    except ImportError:
        wfo_logger.error("Actual data_fetcher not found. Using placeholder data function.")
        # Define a placeholder if the import fails, ensuring it matches expected signature
        def actual_fetch_historical_data(symbol, start_date, end_date, granularity_seconds):
            wfo_logger.warning(f"Using placeholder data for {symbol}")
            # Generate simple random walk data
            dates = pd.date_range(start=start_date, end=end_date, freq=pd.Timedelta(seconds=granularity_seconds))
            if not dates.empty:
                price = 100 + np.random.randn(len(dates)).cumsum() * 0.5
                return pd.DataFrame({
                    'open': price - np.random.rand(len(dates)) * 0.1,
                    'high': price + np.random.rand(len(dates)) * 0.1,
                    'low': price - np.random.rand(len(dates)) * 0.1,
                    'close': price,
                    'volume': np.random.rand(len(dates)) * 100 + 10
                }, index=dates)
            else:
                return pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        
    # Check chat model availability
    if chat_model_available():
        wfo_logger.info("Chat model is configured and available.")
    else:
        wfo_logger.warning("Chat model is not available or not configured.")
    
    # Fetch data
    wfo_logger.info(f"Fetching historical data for {SYMBOL} | {GRANULARITY_STR} | {WFO_START_DATE} to {WFO_END_DATE}")
    try:
        data = actual_fetch_historical_data(SYMBOL, WFO_START_DATE, WFO_END_DATE, GRANULARITY_SECONDS)
        
        if data is None or data.empty:
            wfo_logger.error("Failed to fetch historical data or data is empty. Exiting.")
            sys.exit(1)
        
        # Data Validation/Cleaning 
        if data.isnull().values.any():
            wfo_logger.warning("Data contains NaN values. Attempting to forward fill.")
            data.ffill(inplace=True)
            data.bfill(inplace=True) 
            if data.isnull().values.any():
                 wfo_logger.error("Data still contains NaN values after fill. Exiting.")
                 sys.exit(1)
                 
        wfo_logger.info(f"Successfully fetched and validated {len(data)} data points.")
        
        # Run the main WFO process
        wfo_logger.info("Starting Walk-Forward Optimization run...")
        train_results, oos_results, all_params = run_walk_forward_optimization(
            data, 
            PARAM_GRID, 
            OPTIMIZATION_METRIC, 
            IN_SAMPLE_DAYS, 
            OUT_SAMPLE_DAYS, 
            STEP_DAYS
        )
        
        # Summarize overall results
        wfo_logger.info("--- WFO Run Summary ---")
        if all_params:
            wfo_logger.info(f"Completed {len(all_params)} valid WFO splits.")
            if oos_results:
                oos_metrics_list = [m[1] for m in oos_results if m and m[1] is not None]
                if oos_metrics_list:
                    valid_oos_metrics = [m for m in oos_metrics_list if isinstance(m, dict)]
                    if valid_oos_metrics:
                        avg_oos_metrics = pd.DataFrame(valid_oos_metrics).mean().to_dict()
                        wfo_logger.info("Average Out-of-Sample Performance Metrics:")
                        for k, v in avg_oos_metrics.items():
                            wfo_logger.info(f"  - {k}: {v:.4f}")
                    else:
                        wfo_logger.warning("No valid OOS metrics dictionaries found.")
                else:
                     wfo_logger.warning("No valid Out-of-Sample metrics lists found to summarize.")
            else:
                 wfo_logger.warning("No Out-of-Sample results were generated or stored successfully.")
        else:
            wfo_logger.warning("Walk-Forward Optimization failed to produce any valid results or complete any splits.")
            
    except Exception as e:
        wfo_logger.exception(f"A critical error occurred during the WFO execution: {str(e)}") # Log full traceback
        if chat_model_available():
            try:
                explanation = ask_chat_model(f"The WFO script encountered a critical error: {str(e)}. What are common causes and potential fixes based on the script structure?")
                wfo_logger.info(f"AI Suggested Explanation/Fixes: {explanation}")
            except Exception as chat_err:
                wfo_logger.error(f"Failed to get explanation from chat model: {chat_err}")
        sys.exit(1) # Exit with error status
    
    wfo_logger.info("Optimized WFO script finished successfully.")
    sys.exit(0) # Exit successfully

def evaluate_parameter_sets(data, param_grid, optimization_metric='sharpe_ratio', split_id=None, use_parallel=USE_PARALLEL, num_cores=NUM_CORES):
    """Evaluate multiple parameter sets."""
    param_combinations = []
    temp_grid = param_grid.copy() # Work on a copy to avoid modifying the original grid
    for param_name, param_values in temp_grid.items():
        if isinstance(param_values, tuple) and len(param_values) == 3:
            # Handle range specifications (start, stop, step)
            start, stop, step = param_values
            if isinstance(step, int):
                values = list(range(start, stop + 1, step))
            else:
                # For float steps, use numpy arange and round to avoid precision issues
                values = np.arange(start, stop + step/2, step)
            temp_grid[param_name] = [round(v, 8) for v in values] # Round values for consistency
    
    # Generate combinations from the processed grid
    keys = list(temp_grid.keys())
    values = list(temp_grid.values())
    param_combinations = [dict(zip(keys, combo)) for combo in itertools.product(*values)]
    
    wfo_logger.info(f"Evaluating {len(param_combinations)} parameter combinations for split {split_id}")
    
    results = []
    # Use partial to pass fixed arguments to the worker function
    evaluate_func = partial(evaluate_single_param_set_wrapper) 
    # Prepare arguments, copying data for each process to ensure isolation
    param_args = [(data.copy(), params, split_id) for params in param_combinations]

    if use_parallel and num_cores > 1 and len(param_combinations) > num_cores: # Only use parallel if beneficial
        try:
            with ProcessPoolExecutor(max_workers=num_cores) as executor:
                # Use tqdm for progress bars
                results = list(tqdm(executor.map(evaluate_func, param_args), total=len(param_combinations), desc=f"Split {split_id}"))
        except Exception as e:
             wfo_logger.error(f"Parallel execution failed: {e}. Falling back to sequential processing.")
             # Fallback to sequential execution if parallel fails
             results = [evaluate_func(args) for args in tqdm(param_args, desc=f"Split {split_id} (Sequential)")]
    else:
        # Sequential evaluation
        results = [evaluate_func(args) for args in tqdm(param_args, desc=f"Split {split_id} (Sequential)")]
    
    # Filter out failed evaluations (where portfolio or metrics are None)
    valid_results = [res for res in results if res is not None and res[0] is not None and res[1] is not None]
    
    if not valid_results:
        wfo_logger.warning(f"No valid parameter sets found for split {split_id}")
        return None, None, None, split_id
    
    # Handle potential NaN or inf values in the optimization metric before finding the max
    for r in valid_results: 
        metric_value = r[1].get(optimization_metric)
        if metric_value is None or pd.isna(metric_value) or np.isinf(metric_value):
             r[1][optimization_metric] = -np.inf # Assign a very low value to penalize
             
    # Find the best result based on the optimization metric
    best_result = max(valid_results, key=lambda x: x[1].get(optimization_metric, -np.inf))
    
    return best_result

def analyze_parameter_stability(all_params):
    """Analyze parameter stability across WFO splits."""
    if not all_params or len(all_params) < 2:
        wfo_logger.warning("Not enough parameter sets (<2) to analyze stability.")
        return {}
    
    params_df = pd.DataFrame(all_params)
    stability = {}
    
    for param in params_df.columns:
        # Skip non-optimizable params if they somehow got included
        if param in ['initial_capital', 'commission_pct', 'slippage_pct']: continue
        
        if params_df[param].dtype == 'object' or isinstance(params_df[param].iloc[0], bool):
            # Categorical parameter stability (based on mode frequency)
            value_counts = params_df[param].value_counts()
            mode_val = value_counts.index[0]
            mode_freq = value_counts.iloc[0] / len(params_df)
            stability[param] = {
                'type': 'categorical',
                'mode': mode_val,
                'mode_frequency': mode_freq,
                'unique_values': len(value_counts),
                'stability_score': mode_freq # Higher is more stable
            }
        else:
            # Numerical parameter stability (based on coefficient of variation)
            try:
                 values = params_df[param].astype(float).values # Ensure numeric, handle potential errors
            except ValueError:
                 wfo_logger.warning(f"Could not convert parameter '{param}' to float for stability analysis. Skipping.")
                 continue
                 
            mean_val = np.nanmean(values)
            median_val = np.nanmedian(values)
            std_val = np.nanstd(values)
            
            # Coefficient of Variation (normalized standard deviation)
            cov = abs(std_val / mean_val) if mean_val != 0 else float('inf')
            stability_score = max(0, 1.0 - min(1.0, cov)) # Scale to 0-1, higher is more stable
            
            stability[param] = {
                'type': 'numerical',
                'mean': mean_val,
                'median': median_val,
                'std': std_val,
                'cov': cov,
                'stability_score': stability_score
            }
    return stability

def recommend_final_parameters(all_params, stability_metrics):
    """Recommend final parameters based on stability."""
    if not all_params or not stability_metrics:
        wfo_logger.error("Cannot recommend parameters without results or stability metrics.")
        return {}
        
    params_df = pd.DataFrame(all_params)
    final_params = {}
    
    # Add fixed parameters if they were in the grid (though they shouldn't be)
    for param in ['initial_capital', 'commission_pct', 'slippage_pct']:
        if param in params_df.columns: final_params[param] = params_df[param].iloc[0]

    for param, metrics in stability_metrics.items():
        if param not in params_df.columns: continue # Skip if param wasn't actually varied
        
        if metrics['type'] == 'categorical':
            # Use the most frequent value (mode)
            final_params[param] = metrics['mode']
        else:
            # Numerical: Use median for high stability, mean for medium, last value for low
            stability_score = metrics['stability_score']
            if stability_score >= 0.75: 
                final_params[param] = metrics['median']
            elif stability_score >= 0.5: 
                final_params[param] = metrics['mean']
            else: # Low stability
                final_params[param] = params_df[param].iloc[-1] # Use the last split's best value
                
            # Attempt to round to a reasonable precision based on original grid step if possible
            # This part requires knowing the original grid definition - difficult here.
            # Basic rounding for floats:
            if isinstance(final_params[param], float):
                final_params[param] = round(final_params[param], 4) 

    # Ensure all varied parameters from the first split are included
    first_split_params = all_params[0].keys()
    for param in first_split_params:
         if param not in final_params and param not in ['initial_capital', 'commission_pct', 'slippage_pct']:
             wfo_logger.warning(f"Parameter '{param}' missing from stability metrics, using median as fallback.")
             if param in params_df.columns: # Check if it exists in the dataframe
                 if params_df[param].dtype == 'object' or isinstance(params_df[param].iloc[0], bool):
                     final_params[param] = params_df[param].mode().iloc[0]
                 else:
                     try:
                         final_params[param] = params_df[param].astype(float).median()
                     except ValueError:
                          final_params[param] = params_df[param].iloc[-1] # Fallback to last value if cannot convert
             else:
                 wfo_logger.error(f"Cannot determine fallback for missing parameter '{param}'.")

    wfo_logger.info(f"Recommended final parameters: {final_params}")
    return final_params

def save_final_parameters(params):
    """Save final parameters to JSON."""
    try:
        output_path = OUTPUT_DIR # Use the defined OUTPUT_DIR
        output_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Add strategy type to filename for clarity
        filename = output_path / f"wfo_params_{STRATEGY_TYPE}_optimized_{timestamp}.json"
        latest_filename = output_path / f"latest_wfo_params_{STRATEGY_TYPE}_optimized.json"
        
        # Use the custom JSON encoder
        with open(filename, 'w') as f: 
            json.dump(params, f, indent=4, default=json_encoder_default)
        with open(latest_filename, 'w') as f: 
            json.dump(params, f, indent=4, default=json_encoder_default)
            
        wfo_logger.info(f"Final optimized parameters saved to {filename} and {latest_filename}")
        return True
    except TypeError as te:
        wfo_logger.error(f"JSON Serialization Error saving parameters: {str(te)}")
        wfo_logger.error(f"Problematic parameters: {params}")
        return False
    except Exception as e:
        wfo_logger.error(f"Error saving final parameters: {str(e)}")
        return False

def generate_wfo_report(train_portfolios, oos_portfolios, all_params):
    """Generate a text report for WFO results."""
    try:
        output_path = OUTPUT_DIR # Use the defined OUTPUT_DIR
        output_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = output_path / f"wfo_report_{STRATEGY_TYPE}_optimized_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Walk-Forward Optimization Report (Optimized {STRATEGY_TYPE}) - {timestamp}\n")
            f.write("====================================================================\n")
            f.write(f"Symbol: {SYMBOL}, Granularity: {GRANULARITY_STR}\n")
            f.write(f"Period: {WFO_START_DATE} to {WFO_END_DATE}\n")
            f.write(f"WFO Settings: In-Sample={IN_SAMPLE_DAYS}d, Out-Sample={OUT_SAMPLE_DAYS}d, Step={STEP_DAYS}d\n")
            f.write(f"Optimization Metric: {OPTIMIZATION_METRIC}\n")
            f.write("--------------------------------------------------------------------\n")
            
            if not all_params:
                f.write("No valid splits completed.\n")
                return True

            f.write(f"Number of Splits Completed: {len(all_params)}\n")
            
            # OOS Performance Summary
            oos_metrics_list = [m[1] for m in oos_portfolios if m[1] is not None]
            if oos_metrics_list:
                avg_oos_metrics = pd.DataFrame(oos_metrics_list).mean().to_dict()
                f.write("\n--- Average Out-of-Sample Performance ---\n")
                for k, v in avg_oos_metrics.items():
                    f.write(f"  {k}: {v:.4f}\n")
            else:
                f.write("\n--- No valid Out-of-Sample results found ---\n")
                
            f.write("\n--- Split Details ---\n")
            for i, params in enumerate(all_params):
                f.write(f"\nSplit {i}:\n")
                f.write(f"  Best Params: {json.dumps(params, default=json_encoder_default)}\n")
                if i < len(train_portfolios) and train_portfolios[i][1]: 
                    f.write(f"  Train Metrics: {json.dumps(train_portfolios[i][1], default=json_encoder_default)}\n")
                if i < len(oos_portfolios) and oos_portfolios[i][1]: 
                    f.write(f"  OOS Metrics: {json.dumps(oos_portfolios[i][1], default=json_encoder_default)}\n")
            
            # Parameter Stability and Final Recommendation
            stability = analyze_parameter_stability(all_params)
            final = recommend_final_parameters(all_params, stability)
            f.write("\n--- Parameter Stability ---\n")
            f.write(json.dumps(stability, indent=2, default=json_encoder_default))
            f.write("\n\n--- Final Recommended Parameters ---\n")
            f.write(json.dumps(final, indent=2, default=json_encoder_default))
            f.write("\n====================================================================\n")
            
        wfo_logger.info(f"WFO report saved to {filename}")
        return True
        
    except Exception as e:
        wfo_logger.error(f"Error generating WFO report: {str(e)}")
        return False

# --- Remaining functions placeholder ---

# Example placeholder for main execution
if __name__ == "__main__":
    # ... (original placeholder code) ...
    pass 

def run_walk_forward_optimization(data, param_grid, optimization_metric='sharpe_ratio', in_sample_days=IN_SAMPLE_DAYS, out_sample_days=OUT_SAMPLE_DAYS, step_days=STEP_DAYS):
    """Run walk-forward optimization."""
    wfo_logger.info(f"Starting walk-forward optimization ({STRATEGY_TYPE} strategy)")
    
    # Ensure data has a DatetimeIndex
    if not isinstance(data.index, pd.DatetimeIndex):
        try:
            data.index = pd.to_datetime(data.index)
            wfo_logger.info("Converted data index to DatetimeIndex.")
        except Exception as e:
             wfo_logger.error(f"Failed to convert data index to DatetimeIndex: {e}")
             return [], [], []
             
    # Use unique dates for splitting to handle potential gaps or non-continuous data
    unique_dates = data.index.normalize().unique()
    if len(unique_dates) < in_sample_days + out_sample_days:
         wfo_logger.error(f"Not enough unique dates for WFO. Need {in_sample_days + out_sample_days}, have {len(unique_dates)}")
         return [], [], []
         
    start_date = unique_dates[0]
    end_date = unique_dates[-1]
    wfo_logger.info(f"Data range: {start_date.date()} to {end_date.date()}")

    train_results, oos_results, all_params = [], [], []
    current_train_start_date = start_date
    split_id = 0
    
    while True:
        # Define date ranges for the split
        train_end_date = current_train_start_date + timedelta(days=in_sample_days - 1) 
        oos_end_date = train_end_date + timedelta(days=out_sample_days)

        # Check if the next OOS period goes beyond the available data
        if oos_end_date > end_date:
            wfo_logger.info(f"Reached end of data for split {split_id}. Last possible OOS date {oos_end_date.date()} > actual end date {end_date.date()}")
            break 
        
        # Find actual start/end timestamps in the data corresponding to these dates
        try:
            actual_train_start = data.index[data.index >= current_train_start_date][0]
            actual_train_end = data.index[data.index <= train_end_date][-1]
            actual_oos_start = data.index[data.index > actual_train_end][0]
            actual_oos_end = data.index[data.index <= oos_end_date][-1]
        except IndexError:
            wfo_logger.warning(f"Split {split_id}: Could not find data for the calculated date range ({current_train_start_date.date()} to {oos_end_date.date()}). Might be due to market closures or data gaps. Trying next step.")
            current_train_start_date += timedelta(days=step_days)
            split_id += 1 # Increment split_id even if skipped
            continue
             
        train_data = data.loc[actual_train_start:actual_train_end].copy()
        oos_data = data.loc[actual_oos_start:actual_oos_end].copy()
        
        # Basic check for sufficient data points in each split
        min_train_points = 10 # Example threshold
        min_oos_points = 5   # Example threshold
        if len(train_data) < min_train_points or len(oos_data) < min_oos_points:
             wfo_logger.warning(f"Split {split_id}: Insufficient data points. Train: {len(train_data)} (min {min_train_points}), OOS: {len(oos_data)} (min {min_oos_points}). Skipping.")
             current_train_start_date += timedelta(days=step_days)
             split_id += 1 # Increment split_id
             continue

        wfo_logger.info(f"Running Split {split_id}: Train [{actual_train_start} to {actual_train_end}], OOS [{actual_oos_start} to {actual_oos_end}]")
        
        # Evaluate parameters on training data
        best_train_pf, best_train_metrics, best_params, _ = evaluate_parameter_sets(
            train_data, param_grid.copy(), optimization_metric, split_id
        )

        if best_params is None:
            wfo_logger.warning(f"Split {split_id}: No valid parameters found during training optimization. Skipping OOS evaluation for this split.")
        else:
            wfo_logger.info(f"Split {split_id}: Best Train Params => {best_params}")
            wfo_logger.info(f"Split {split_id}: Best Train Metrics => {best_train_metrics}")
            all_params.append(best_params) # Store best params even if OOS fails
            train_results.append((best_train_pf, best_train_metrics, best_params, split_id))
            
            # Evaluate best parameters on out-of-sample data
            oos_portfolio, oos_metrics, _, _ = evaluate_parameter_set(oos_data, best_params, split_id)
            if oos_portfolio is not None and oos_metrics is not None:
                oos_results.append((oos_portfolio, oos_metrics, best_params, split_id))
                wfo_logger.info(f"Split {split_id}: OOS Metrics => {oos_metrics}")
                wfo_logger.info(f"Split {split_id}: Train {optimization_metric}={best_train_metrics.get(optimization_metric, 'N/A'):.2f}, OOS {optimization_metric}={oos_metrics.get(optimization_metric, 'N/A'):.2f}")
            else: 
                 wfo_logger.warning(f"Split {split_id}: OOS evaluation failed for best train parameters: {best_params}")
        
        # Move to the next split start date
        current_train_start_date += timedelta(days=step_days)
        split_id += 1
    
    # Final analysis and reporting after all splits
    if all_params:
        wfo_logger.info("Performing final parameter stability analysis and reporting...")
        stability_metrics = analyze_parameter_stability(all_params)
        final_params = recommend_final_parameters(all_params, stability_metrics)
        save_final_parameters(final_params) # Save the recommended parameters
        generate_wfo_report(train_results, oos_results, all_params) # Generate the final report
    else:
        wfo_logger.warning("WFO finished but no valid parameters were found across all splits.")
    
    return train_results, oos_results, all_params 