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
import pandas_ta as ta  # Add at the top of the file with other imports

# Import create_portfolio from edge_strategy_assistant
try:
    from scripts.strategies.edge_strategy_assistant import create_portfolio
except ModuleNotFoundError:
    # Handle case when file is run directly from the strategies directory
    from edge_strategy_assistant import create_portfolio

# Import CandlestickPatternStrategy
try:
    from scripts.strategies.candlestick_pattern_strategy import CandlestickPatternStrategy
except ModuleNotFoundError:
    # Handle case when file is run directly from the strategies directory
    from candlestick_pattern_strategy import CandlestickPatternStrategy

# Add dotenv import and loading
load_dotenv(verbose=True)

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

def init_logging():
    """Initialize logging configuration for the WFO module"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create a logger for this module
    logger = logging.getLogger('wfo_edge_strategy')
    logger.setLevel(logging.INFO)
    
    # Set other libraries to be less verbose
    logging.getLogger('vectorbtpro').setLevel(logging.WARNING)
    logging.getLogger('numba').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    return logger

# Global logger
logger = init_logging()

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
    from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
    wfo_logger.info("Successfully imported refactored EdgeMultiFactorStrategy.")
except ImportError as e:
    wfo_logger.error(f"Could not import EdgeMultiFactorStrategy: {e}")
    # Attempt fallback if path structure is different
    try:
        from edge_multi_factor_fixed import EdgeMultiFactorStrategy
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
    # Add other specific type checks if needed
    
    # Default fallback: Raise TypeError so json.dump knows it wasn't handled
    # Or, convert to string as a last resort (less ideal, but might prevent crashes)
    # logger.warning(f"JSON Fallback: Converting type {type(obj)} to string.")
    # return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
# --- END NEW JSON DEFAULT FUNCTION ---

# --- VectorBT Pro Chat Model Configuration --- NEW FUNCTION
def setup_chat_provider():
    """Configure the chat provider for debugging and optimization advice."""
    try:
        # Check for API keys in environment
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        if not openai_api_key and not openrouter_api_key:
            wfo_logger.warning("Neither OPENAI_API_KEY nor OPENROUTER_API_KEY found in environment. Chat features will fail.")
            return False
            
        # Use whichever API key is available
        api_key = openai_api_key or openrouter_api_key
        
        # Make sure OPENAI_API_KEY is set in the environment (required by some libraries)
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Determine if we should use OpenRouter
        use_openrouter = bool(openrouter_api_key)
        api_base_url = openrouter_base_url if use_openrouter else None
        model = "openrouter/auto" if use_openrouter else "gpt-3.5-turbo"
        
        # Try to import OpenAI directly first - this ensures the API client is properly set up
        try:
            from openai import OpenAI
            
            # If using OpenRouter, validate the key with a simple direct API call
            if use_openrouter:
                try:
                    client = OpenAI(
                        api_key=openrouter_api_key,
                        base_url=api_base_url
                    )
                    # Make a minimal test request
                    response = client.chat.completions.create(
                        model="openrouter/auto",
                        messages=[{"role": "user", "content": "Test"}],
                        max_tokens=5
                    )
                    wfo_logger.info("OpenRouter API key validated with direct test.")
                except Exception as e:
                    wfo_logger.error(f"OpenRouter direct API test failed: {e}")
                    if "invalid_api_key" in str(e):
                        wfo_logger.error("Invalid OpenRouter API key. Please check your credentials.")
                        return False
        except ImportError:
            wfo_logger.warning("OpenAI package not available. Continuing without direct API validation.")
        
        import vectorbtpro as vbt
        
        # Try different possible configuration paths
        configured = False
        
        # 1. Try with knowledge.chat settings (newer versions)
        if hasattr(vbt, 'settings') and hasattr(vbt.settings, 'knowledge') and hasattr(vbt.settings.knowledge, 'chat'):
            try:
                # Configure knowledge.chat settings
                vbt.settings.knowledge.chat.openai_key = api_key
                if api_base_url:
                    vbt.settings.knowledge.chat.openai_base_url = api_base_url
                vbt.settings.knowledge.chat.openai_headers = {
                    "HTTP-Referer": "https://vectorbt.pro", 
                    "X-Title": "VectorBT Pro"
                }
                vbt.settings.knowledge.chat.model = model
                configured = True
                wfo_logger.info(f"Successfully configured chat provider with knowledge.chat using {'OpenRouter' if use_openrouter else 'OpenAI'} API.")
            except Exception as e:
                wfo_logger.warning(f"Error configuring knowledge.chat: {e}")
        
        # 2. Try with kb.chat settings (some versions)
        if not configured and hasattr(vbt, 'settings') and hasattr(vbt.settings, 'kb') and hasattr(vbt.settings.kb, 'chat'):
            try:
                # For dictionary-based settings use dict syntax
                vbt.settings.kb.chat.openai_key = api_key
                if api_base_url:
                    vbt.settings.kb.chat.openai_base_url = api_base_url
                vbt.settings.kb.chat.openai_headers = {
                    "HTTP-Referer": "https://vectorbt.pro", 
                    "X-Title": "VectorBT Pro"
                }
                vbt.settings.kb.chat.model = model
                configured = True
                wfo_logger.info(f"Successfully configured chat provider with kb.chat using {'OpenRouter' if use_openrouter else 'OpenAI'} API.")
            except AttributeError:
                try:
                    # Try dictionary access if attribute access fails
                    vbt.settings.kb.chat['openai_key'] = api_key
                    if api_base_url:
                        vbt.settings.kb.chat['openai_base_url'] = api_base_url
                    vbt.settings.kb.chat['openai_headers'] = {
                        "HTTP-Referer": "https://vectorbt.pro", 
                        "X-Title": "VectorBT Pro"
                    }
                    vbt.settings.kb.chat['model'] = model
                    configured = True
                    wfo_logger.info(f"Successfully configured chat provider with kb.chat dictionary using {'OpenRouter' if use_openrouter else 'OpenAI'} API.")
                except Exception as e:
                    wfo_logger.warning(f"Error configuring kb.chat with dictionary: {e}")
        
        # 3. Try with litellm settings (some versions)
        if not configured and hasattr(vbt, 'settings') and hasattr(vbt.settings, 'litellm'):
            try:
                vbt.settings.litellm.api_key = api_key
                if api_base_url:
                    vbt.settings.litellm.api_base = api_base_url
                vbt.settings.litellm.model = "deepseek/deepseek-r1" if use_openrouter else "gpt-3.5-turbo"
                configured = True
                wfo_logger.info(f"Successfully configured chat provider with litellm using {'OpenRouter' if use_openrouter else 'OpenAI'} API.")
            except Exception as e:
                wfo_logger.warning(f"Error configuring litellm: {e}")
        
        # 4. Direct settings access as a fallback
        if not configured and hasattr(vbt, 'settings'):
            try:
                # Try to set OpenAI settings directly
                openai_settings = getattr(vbt.settings, 'openai', None)
                if openai_settings is not None:
                    openai_settings['api_key'] = api_key
                    if api_base_url:
                        openai_settings['base_url'] = api_base_url
                    openai_settings['model'] = "deepseek/deepseek-r1" if use_openrouter else "gpt-3.5-turbo"
                    configured = True
                    wfo_logger.info(f"Successfully configured chat provider with openai settings using {'OpenRouter' if use_openrouter else 'OpenAI'} API.")
            except Exception as e:
                wfo_logger.warning(f"Error configuring openai settings: {e}")
        
        # 5. Last resort - try exposing the API key directly to vectorbtpro's environment
        if not configured:
            try:
                # Some versions of VectorBTPro may use their own environment
                if hasattr(vbt, 'set_env_var'):
                    vbt.set_env_var('OPENAI_API_KEY', api_key)
                    if api_base_url:
                        vbt.set_env_var('OPENAI_BASE_URL', api_base_url)
                    wfo_logger.info("Set API keys directly in VectorBTPro environment.")
                    configured = True
            except Exception as e:
                wfo_logger.warning(f"Error setting environment variables in VectorBTPro: {e}")
        
        if configured:
            wfo_logger.info("Chat provider configuration complete.")
            return True
                
        if not configured:
            wfo_logger.warning("Could not find appropriate settings path in vectorbtpro for chat configuration.")
            return False
        
    except Exception as e:
        wfo_logger.error(f"Failed to configure chat provider: {str(e)}")
        wfo_logger.warning("Chat provider setup failed, continuing without chat features.")
        return False

# Function to get a chat model instance - add this after setup_chat_provider
def get_chat_model():
    """Get a configured chat model instance.
    
    This function attempts to get a configured chat model instance.
    If no chat model is available, it returns None.
    
    Returns:
        object: A chat model instance if available, None otherwise.
    """
    try:
        # Ensure chat provider is properly set up
        setup_success = setup_chat_provider()
        if not setup_success:
            wfo_logger.warning("Chat provider setup failed, cannot get chat model.")
            return None
            
        # First try to create a direct chat function using OpenRouter
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        if openrouter_api_key:
            try:
                from openai import OpenAI
                
                # Create a client with OpenRouter settings
                client = OpenAI(
                    api_key=openrouter_api_key,
                    base_url=openrouter_base_url
                )
                
                # Create a chat function that uses OpenRouter directly
                def direct_chat(prompt):
                    try:
                        completion = client.chat.completions.create(
                            model="openrouter/auto",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=1000
                        )
                        return completion.choices[0].message.content
                    except Exception as e:
                        wfo_logger.error(f"OpenRouter direct chat error: {e}")
                        return f"Error: {str(e)}"
                
                wfo_logger.info("Successfully created direct_chat function using OpenRouter API.")
                return direct_chat
            except Exception as e:
                wfo_logger.error(f"Failed to create direct_chat: {e}")
            
        # If direct_chat creation failed, try VectorBT's chat function
        import vectorbtpro as vbt
        
        # Check if the chat function is available in vectorbtpro
        if hasattr(vbt, 'chat') and callable(vbt.chat):
            # vbt.chat is a function, not a class in newer versions
            wfo_logger.info("Using vbt.chat function as chat model.")
            return vbt.chat
            
        # For older versions, try to get the ChatModel
        try:
            from vectorbtpro.utils.knowledge.chatting import ChatModel
            chat_model = ChatModel()
            wfo_logger.info("Successfully initialized ChatModel from vectorbtpro.utils.knowledge.chatting")
            return chat_model
        except (ImportError, AttributeError):
            wfo_logger.warning("ChatModel not available in utils.knowledge.chatting")
            
        wfo_logger.warning("Could not find any chat model in vectorbtpro.")
        return None
    except Exception as e:
        wfo_logger.error(f"Error getting chat model: {e}")
        return None

def ask_chat_model(query, context=None):
    """Query the chat model with the given question and context."""
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    # Prepare the full prompt
    full_prompt = query
    if context:
        context_str = "\n\nContext:\n" + "\n".join([f"{k}: {v}" for k, v in context.items()])
        full_prompt += context_str
    
    # Always try OpenRouter directly first - most reliable method
    if openrouter_api_key:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=openrouter_api_key,
                base_url=openrouter_base_url
            )
            wfo_logger.debug(f"Using OpenRouter API directly for prompt: {full_prompt[:100]}...")
            completion = client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=1000
            )
            response = completion.choices[0].message.content
            wfo_logger.debug("Received response from OpenRouter")
            return response
        except Exception as e:
            wfo_logger.error(f"Error using OpenRouter API directly: {e}")
            wfo_logger.info("Falling back to chat model.")
    
    # Get the chat model function
    chat_model = get_chat_model()
    if chat_model is None:
        wfo_logger.error("No chat model available")
        return "Chat model not available."
    
    # Use the chat model function
    try:
        wfo_logger.debug(f"Querying chat model with prompt: {full_prompt[:100]}...")
        response = chat_model(full_prompt)
        wfo_logger.debug("Received response from chat model")
        return response
    except Exception as e:
        wfo_logger.error(f"Error querying chat model: {e}")
        return f"Error querying chat model: {e}"

def chat_model_available():
    """Check if the chat model is likely configured (checks settings and environment)."""
    try:
        import vectorbtpro as vbt
        
        # Check for API keys
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        github_token = os.environ.get("GITHUB_TOKEN")
        
        # Log key availability (without revealing the keys)
        if openrouter_api_key:
            wfo_logger.info("OPENROUTER_API_KEY is available in environment")
        else:
            wfo_logger.warning("OPENROUTER_API_KEY not found in environment")
            
        if openai_api_key:
            wfo_logger.info("OPENAI_API_KEY is available in environment")
        else:
            wfo_logger.warning("OPENAI_API_KEY not found in environment")
            
        if github_token:
            wfo_logger.info("GITHUB_TOKEN is available in environment")
        else:
            wfo_logger.warning("GITHUB_TOKEN not found in environment (required for asset pulling)")
        
        # Check if any API key is available
        api_key_available = bool(openrouter_api_key or openai_api_key)
        
        if not api_key_available:
            wfo_logger.warning("No API keys found. Set either OPENROUTER_API_KEY or OPENAI_API_KEY.")
            return False
            
        # Try to verify if the chat model exists
        chat_model = get_chat_model()
        return chat_model is not None
        
    except Exception as e:
        wfo_logger.warning(f"Could not check chat model configuration: {e}")
        return False

# =============================================================================
# Configuration Constants
# =============================================================================

# --- WFO Parameters ---
# Adjust these parameters to ensure we have valid splits
IN_SAMPLE_DAYS = 100      # Shorter training period for faster execution
OUT_SAMPLE_DAYS = 40      # Shorter testing period
STEP_DAYS = 50            # Ensure we can create multiple splits
# Ensure step is not larger than OOS period to avoid gaps, unless intended
if STEP_DAYS > OUT_SAMPLE_DAYS:
    wfo_logger.warning(f"STEP_DAYS ({STEP_DAYS}) > OUT_SAMPLE_DAYS ({OUT_SAMPLE_DAYS}). OOS periods will overlap.")

# --- Data Parameters ---
# Use a longer period to ensure enough data for signal generation
TOTAL_HISTORY_DAYS = 500 # Full year of data
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

# --- Strategy Selection ---
STRATEGY_TYPE = "candlestick"  # Options: "edge_multi_factor", "candlestick"

# --- Optimization Parameters ---
OPTIMIZATION_METRIC = 'sharpe_ratio' # e.g., 'sharpe_ratio', 'total_return', 'max_drawdown'

# Define parameter grids for different strategy types
EDGE_MULTI_FACTOR_PARAM_GRID = {
    # RSI parameters
    'rsi_window': (5, 25, 1),      # Wider range with smaller values included
    'rsi_entry': (20, 40, 2),      # Go lower on entry threshold to catch more oversold conditions
    'rsi_exit': (50, 75, 5),       # More granular exit thresholds
    
    # Bollinger Band parameters
    'bb_window': (10, 30, 2),      # More flexible window size
    'bb_dev': (1.5, 3.0, 0.1),     # Wider range of deviations
    
    # Volatility parameters
    'vol_window': (5, 30, 5),      # Wider range of volatility windows
    'vol_threshold': (0.5, 2.0, 0.2), # Include more permissive volume thresholds
    
    # Stop loss and take profit
    'sl_pct': (0.5, 4.0, 0.5),     # More granular stop loss range
    'tp_pct': (1.0, 8.0, 1.0),     # More granular take profit range
    
    # Position sizing
    'risk_per_trade': [0.005, 0.01, 0.015, 0.02, 0.03]  # More sizing options
}

CANDLESTICK_PARAM_GRID = {
    # Candlestick pattern parameters
    'lookback_periods': [20, 30, 50],
    'min_strength': [0.005, 0.01, 0.02, 0.05],
    'use_strength': [True, False],
    'use_confirmation': [True, False],
    'confirmation_window': [2, 3, 5],
    
    # Risk management parameters
    'stop_loss_pct': [0.02, 0.03, 0.05],
    'take_profit_pct': [0.04, 0.06, 0.1],
    'risk_per_trade': [0.01, 0.02, 0.03]
}

# Use the appropriate parameter grid based on strategy type
PARAM_GRID = CANDLESTICK_PARAM_GRID if STRATEGY_TYPE == "candlestick" else EDGE_MULTI_FACTOR_PARAM_GRID

# --- Performance Optimization Settings ---
# Set to True to enable parallel processing (significantly faster)
USE_PARALLEL = True
NUM_CORES = max(1, multiprocessing.cpu_count() - 1)  # Leave one core free

# Enable vectorbtpro caching for faster repeated calculations
ENABLE_CACHING = True

# Debug control for less output
VERBOSE_DEBUG = False  # Set to False for less output in production runs

# Use a smaller grid for quick testing (set to True for rapid testing/development)
QUICK_TEST = False
if QUICK_TEST:
    PARAM_GRID = {
        'lookback_window': [20],
        'volatility_threshold': [0.5],
        'tsl_stop': [0.05],
        'tp_stop': [0.1],
        'atr_multiple_sl': [2.0],
        'vol_filter_window': [100]
    }
    WEIGHT_COMBINATIONS = [weight_options[0]]  # Just use equal weights
    # Reduce data range
    TOTAL_HISTORY_DAYS = 180
    WFO_START_DATE = (datetime.now() - timedelta(days=TOTAL_HISTORY_DAYS)).strftime('%Y-%m-%d')

# Adjust performance criteria to be much more lenient
MIN_SHARPE_RATIO = 0.1   # Very low Sharpe ratio requirement
MIN_TOTAL_TRADES = 3     # Accept portfolios with just a few trades
MIN_WIN_RATE = 0.3       # Lower win rate requirement significantly
MAX_DRAWDOWN = -0.35     # Allow for larger drawdowns

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
        rename_map = {}
        for col in required_cols:
            if col not in df.columns and col.upper() in df.columns:
                rename_map[col.upper()] = col
        
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
                        
                        # Handle NaN values
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


def optimize_pattern_signal_parameters(df: pd.DataFrame, 
                                      test_length: int = 252,
                                      min_trades: int = 10) -> Dict[str, Any]:
    """
    Optimize parameters for candle pattern signal generation.
    
    Args:
        df: DataFrame with candle pattern signals and price data
        test_length: Number of days to use for testing
        min_trades: Minimum number of trades required for valid optimization
    
    Returns:
        Dictionary of optimized parameters
    """
    try:
        # Split data into train and test
        train_df = df.iloc[:-test_length]
        test_df = df.iloc[-test_length:]
        
        # Define parameter ranges to test
        min_strength_values = [0.005, 0.01, 0.02, 0.03, 0.05, 0.1]
        lookback_values = [10, 20, 30, 50, 100]
        
        # Initialize best parameters and metrics
        best_params = {
            'min_strength': 0.01,
            'lookback': 20,
            'use_strength': True
        }
        best_sharpe = -np.inf
        
        # Test each parameter combination
        for min_strength in min_strength_values:
            for lookback in lookback_values:
                for use_strength in [True, False]:
                    # Generate strength metrics on training data
                    train_with_strength = get_candle_pattern_strength(train_df, lookback=lookback)
                    
                    # Apply to test data (simulating real-world scenario)
                    test_with_strength = get_candle_pattern_strength(test_df, lookback=lookback)
                    
                    # Generate signals on test data
                    buy_signals, sell_signals = generate_candle_pattern_signals(
                        test_with_strength, 
                        min_strength=min_strength,
                        use_strength=use_strength
                    )
                    
                    # Count number of signals
                    num_buys = buy_signals.sum()
                    num_sells = sell_signals.sum()
                    
                    # Skip if too few trades
                    if num_buys + num_sells < min_trades:
                        continue
                    
                    # Calculate returns based on signals
                    # Simple implementation: buy on buy signal, sell on sell signal, hold otherwise
                    positions = pd.Series(0, index=test_df.index)
                    positions[buy_signals] = 1
                    positions[sell_signals] = -1
                    
                    # Calculate daily returns
                    daily_returns = test_df['close'].pct_change() * positions.shift(1)
                    
                    # Skip if not enough data points
                    if daily_returns.count() < 20:
                        continue
                    
                    # Calculate Sharpe ratio (annualized)
                    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
                    
                    # Update best parameters if better Sharpe
                    if pd.notna(sharpe) and sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_params = {
                            'min_strength': min_strength,
                            'lookback': lookback,
                            'use_strength': use_strength,
                            'sharpe': sharpe,
                            'num_buys': num_buys,
                            'num_sells': num_sells
                        }
        
        wfo_logger.info(f"Optimized candle pattern parameters: {best_params}")
        return best_params
        
    except Exception as e:
        wfo_logger.error(f"Error optimizing pattern signal parameters: {str(e)}")
        return {
            'min_strength': 0.01,
            'lookback': 20,
            'use_strength': True
        }

def create_portfolio_for_strategy(data, entries, exits, init_cash=INITIAL_CAPITAL, size=None, stop_loss=None, take_profit=None, direction='long'):
    """
    Create a portfolio for a trading strategy using either vectorbt's Portfolio or our CustomPortfolio.
    
    Args:
        data: DataFrame with at least 'close' column
        entries: Series of entry signals
        exits: Series of exit signals
        init_cash: Initial capital
        size: Optional size series
        stop_loss: Stop loss percentage as decimal
        take_profit: Take profit percentage as decimal
        direction: 'long' or 'short'
        
    Returns:
        Portfolio object or CustomPortfolio object
    """
    try:
        # Ensure we have a DataFrame
        if not isinstance(data, pd.DataFrame):
            logger.error("Data must be a DataFrame")
            return None
            
        # Ensure we have a close column
        if 'close' not in data.columns:
            logger.error("'close' column required in data")
            return None
        
        # Ensure entries and exits are proper boolean Series
        if not isinstance(entries, pd.Series):
            entries = pd.Series(entries, index=data.index)
        if not isinstance(exits, pd.Series):
            exits = pd.Series(exits, index=data.index)
        
        # Convert to numpy boolean arrays for vectorbt compatibility
        entries = entries.astype(np.bool_)
        exits = exits.astype(np.bool_)
        
        # Direction handling - ensure it's in the format VectorBT expects
        # VectorBT uses 1 for long direction and -1 for short
        direction_value = 1 if direction == 'long' else -1
        
        # Determine how to create the portfolio based on the version and requirements
        try:
            # First check if we should use CustomPortfolio
            if stop_loss is not None or take_profit is not None:
                # Import the CustomPortfolio class
                try:
                    from scripts.portfolio.custom_portfolio import CustomPortfolio
                    logger.debug(f"Creating CustomPortfolio with SL={stop_loss}, TP={take_profit}")
                    
                    # Create CustomPortfolio with stop loss and take profit
                    portfolio = CustomPortfolio.from_signals(
                        close=data['close'],
                        entries=entries,
                        exits=exits,
                        size=size,
                        size_type='amount' if size is not None else 'value',
                        init_cash=init_cash,
                        fees=COMMISSION_PCT/100,
                        slippage=SLIPPAGE_PCT/100,
                        freq=get_vbt_freq_str(GRANULARITY_STR),
                        direction=direction_value,  # Use numeric direction
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )
                    logger.debug(f"Successfully created CustomPortfolio with SL/TP")
                except ImportError as e:
                    logger.warning(f"Could not import CustomPortfolio class: {e}, falling back to standard Portfolio")
                    # Fall back to standard Portfolio if CustomPortfolio can't be imported
                    portfolio = vbt.Portfolio.from_signals(
                        close=data['close'],
                        entries=entries,
                        exits=exits,
                        size=size,
                        size_type='amount' if size is not None else 'value',
                        init_cash=init_cash,
                        fees=COMMISSION_PCT/100,
                        slippage=SLIPPAGE_PCT/100,
                        freq=get_vbt_freq_str(GRANULARITY_STR),
                        direction=direction_value  # Use numeric direction
                    )
            else:
                # Use standard vectorbt Portfolio without stop loss/take profit
                logger.debug("Creating standard vectorbt Portfolio")
                
                portfolio = vbt.Portfolio.from_signals(
                    close=data['close'],
                    entries=entries,
                    exits=exits,
                    size=size,
                    size_type='amount' if size is not None else 'value',
                    init_cash=init_cash,
                    fees=COMMISSION_PCT/100,
                    slippage=SLIPPAGE_PCT/100,
                    freq=get_vbt_freq_str(GRANULARITY_STR),
                    direction=direction_value  # Use numeric direction
                )
            
            logger.debug(f"Successfully created portfolio")
            return portfolio
            
        except Exception as e:
            logger.error(f"Error creating portfolio: {str(e)}")
            # Fallback to basic vectorbt Portfolio without stop loss/take profit
            try:
                logger.debug("Attempting fallback to basic vectorbt Portfolio")
                portfolio = vbt.Portfolio.from_signals(
                    close=data['close'],
                    entries=entries,
                    exits=exits,
                    init_cash=init_cash,
                    fees=COMMISSION_PCT/100,
                    slippage=SLIPPAGE_PCT/100,
                    freq=get_vbt_freq_str(GRANULARITY_STR),
                    direction=direction_value  # Use numeric direction
                )
                return portfolio
            except Exception as fallback_error:
                logger.error(f"Fallback portfolio creation also failed: {str(fallback_error)}")
                return None
            
    except Exception as e:
        logger.error(f"Error in create_portfolio_for_strategy: {str(e)}")
        return None

def create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL):
    """
    Create a vectorbt Portfolio object with the given parameters.
    
    Args:
        data: DataFrame with OHLCV data
        params: Dictionary of strategy parameters
        init_cash: Initial capital
        
    Returns:
        vectorbt.Portfolio or None: Portfolio object or None if creation failed
    """
    try:
        # Ensure we have a DataFrame
        if not isinstance(data, pd.DataFrame):
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                logging.error("Data is not a DataFrame or dictionary")
                return None
        else:
            df = data.copy()
            
        # Ensure we have the necessary OHLCV columns
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                logging.error(f"Missing required column: {col}")
                return None
        
        # Extract parameters
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
        
        commission_pct = float(params.get('commission_pct', COMMISSION_PCT))
        slippage_pct = float(params.get('slippage_pct', SLIPPAGE_PCT))
        
        # Calculate indicators
        # RSI
        rsi = vbt.RSI.run(df['close'], window=rsi_window).rsi
        
        # Bollinger Bands
        bb = vbt.BollingerBands.run(df['close'], window=bb_window, alpha=bb_dev)
        
        # Volatility (using 'close' prices and standard deviation)
        df['volatility'] = df['close'].pct_change().rolling(window=vol_window).std()
        
        # Generate entry signals
        # Long entry: RSI below entry threshold and price below lower BB, with volatility above threshold
        long_entry = (rsi < rsi_entry) & (df['close'] < bb.lower) & (df['volatility'] > vol_threshold)
        
        # Exit signals: RSI above exit threshold or price above upper BB
        long_exit = (rsi > rsi_exit) | (df['close'] > bb.upper)
        
        # Generate position sizing based on risk per trade
        size = calculate_position_size(
            signal=long_entry,
            price=df['close'],
            stop_loss_pct=sl_pct,
            risk_pct=risk_per_trade,
            capital=init_cash
        )
        
        # Create portfolio object
        try:
            # Determine whether to use CustomPortfolio
            use_sl_tp = sl_pct is not None and sl_pct > 0 and tp_pct is not None and tp_pct > 0
            
            if use_sl_tp:
                try:
                    # Import CustomPortfolio for stop-loss and take-profit
                    from scripts.portfolio.custom_portfolio import CustomPortfolio
                    
                    # Create portfolio with CustomPortfolio
                    portfolio = CustomPortfolio.from_signals(
                        close=df['close'],
                        entries=long_entry,
                        exits=long_exit,
                        size=size,
                        size_type='amount' if size is not None else 'value',
                        init_cash=init_cash,
                        fees=commission_pct/100,
                        slippage=slippage_pct/100,
                        freq=get_vbt_freq_str(GRANULARITY_STR),
                        stop_loss=sl_pct,
                        take_profit=tp_pct
                    )
                    
                    logging.info("Created portfolio with CustomPortfolio for SL/TP")
                except ImportError:
                    logging.warning("Could not import CustomPortfolio, falling back to standard Portfolio")
                    # Fall back to standard Portfolio
                    portfolio = vbt.Portfolio.from_signals(
                        close=df['close'],
                        entries=long_entry,
                        exits=long_exit,
                        size=size,
                        size_type='amount' if size is not None else 'value',
                        init_cash=init_cash,
                        fees=commission_pct/100,
                        slippage=slippage_pct/100,
                        freq=get_vbt_freq_str(GRANULARITY_STR)
                    )
            else:
                # Use standard Portfolio without SL/TP
                portfolio = vbt.Portfolio.from_signals(
                    close=df['close'],
                    entries=long_entry,
                    exits=long_exit,
                    size=size,
                    size_type='amount' if size is not None else 'value',
                    init_cash=init_cash,
                    fees=commission_pct/100,
                    slippage=slippage_pct/100,
                    freq=get_vbt_freq_str(GRANULARITY_STR)
                )
            
            # Basic validity check
            if portfolio is not None:
                return portfolio
            else:
                logging.error("Portfolio creation returned None")
                return None
                
        except Exception as e:
            logging.error(f"Error creating portfolio: {str(e)}")
            return None
            
    except Exception as e:
        logging.error(f"Error in create_pf_for_params: {str(e)}")
        return None


def calculate_position_size(signal, price, stop_loss_pct, risk_pct, capital):
    """
    Calculate position size based on risk per trade.
    
    Args:
        signal: Boolean Series with entry signals
        price: Series with entry prices
        stop_loss_pct: Stop loss percentage
        risk_pct: Risk percentage per trade
        capital: Total capital
        
    Returns:
        Series: Position sizes in currency units
    """
    # Initialize size Series with zeros
    size = pd.Series(0.0, index=signal.index)
    
    # Only calculate sizes for entry signals
    for i in signal[signal].index:
        # Determine stop loss price
        entry_price = price[i]
        risk_amount = capital * risk_pct
        
        # Calculate the price distance to stop loss
        price_distance = entry_price * stop_loss_pct
        
        if price_distance > 0:
            # Calculate position size in units
            size[i] = risk_amount / price_distance
        else:
            size[i] = 0.0
            
    return size

def evaluate_parameter_set(data, params, split_id=None):
    """
    Evaluate a parameter set on the given data.
    
    Args:
        data: DataFrame with OHLCV data
        params: Dictionary of strategy parameters
        split_id: Optional identifier for the data split
        
    Returns:
        tuple: (portfolio, metrics, params, split_id)
    """
    try:
        # Create portfolio with parameters
        if STRATEGY_TYPE == "candlestick":
            # Extract candlestick specific parameters
            lookback_periods = params.get('lookback_periods', 20)
            min_strength = params.get('min_strength', 0.01)
            use_strength = params.get('use_strength', True)
            use_confirmation = params.get('use_confirmation', True)
            confirmation_window = params.get('confirmation_window', 3)
            stop_loss_pct = params.get('stop_loss_pct', 0.03)
            take_profit_pct = params.get('take_profit_pct', 0.06)
            risk_per_trade = params.get('risk_per_trade', 0.02)
            
            # Extract candle patterns
            df_with_patterns = extract_candle_patterns(data)
            
            # Calculate pattern strength if needed
            if use_strength:
                df_with_patterns = get_candle_pattern_strength(df_with_patterns, lookback=lookback_periods)
            
            # Generate signals
            entries, exits = generate_candle_pattern_signals(
                df_with_patterns, 
                min_strength=min_strength,
                use_strength=use_strength
            )
            
            # Apply confirmation if needed
            if use_confirmation:
                # Shift entries by confirmation window days
                confirmed_entries = entries.copy()
                for i in range(1, confirmation_window):
                    confirmed_entries = confirmed_entries & entries.shift(-i)
                entries = confirmed_entries
            
            # Calculate position sizes based on risk per trade
            size = calculate_position_size(
                signal=entries,
                price=data['close'],
                stop_loss_pct=stop_loss_pct,
                risk_pct=risk_per_trade,
                capital=INITIAL_CAPITAL
            )
            
            # Create portfolio
            portfolio = create_pf_for_candlestick_strategy(
                data=data,
                entries=entries,
                exits=exits,
                init_cash=INITIAL_CAPITAL,
                size=size,
                sl_stop=stop_loss_pct,
                tp_stop=take_profit_pct
            )
        else:
            # Use the EdgeMultiFactorStrategy approach
            portfolio = create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL)
        
        # Calculate performance metrics
        metrics = calculate_performance_metrics(portfolio)
        
        return portfolio, metrics, params, split_id
    
    except Exception as e:
        wfo_logger.error(f"Error evaluating parameter set: {str(e)}")
        return None, None, params, split_id

def calculate_performance_metrics(portfolio):
    """Calculate key performance metrics from a portfolio object."""
    metrics = {}
    
    if portfolio is None:
        return {
            'sharpe': 0,
            'calmar': 0,
            'max_dd': 0,
            'total_return': 0,
            'win_rate': 0,
            'volatility': 0,
            'var': 0,
            'num_trades': 0,
            'profit_factor': 0,
            'avg_trade': 0
        }
    
    try:
        # Basic metrics
        # Try to get stats - handle both property and method
        if callable(getattr(portfolio, 'stats', None)):
            stats = portfolio.stats()
        else:
            stats = getattr(portfolio, 'stats', {})
            
        metrics['sharpe'] = stats.get('sharpe_ratio', 0)
        metrics['calmar'] = stats.get('calmar_ratio', 0)
        metrics['max_dd'] = stats.get('max_drawdown', 0)
        metrics['total_return'] = stats.get('total_return', 0)
        metrics['win_rate'] = stats.get('win_rate', 0)
        
        # Risk metrics
        risk = portfolio.get_risk_metrics() if hasattr(portfolio, 'get_risk_metrics') else {}
        metrics['volatility'] = risk.get('volatility', 0)
        metrics['var'] = risk.get('var', 0)
        
        # Handle trades information
        if hasattr(portfolio, 'trades'):
            trades = portfolio.trades
            
            # Try direct property access first
            if hasattr(trades, 'count'):
                # Handle count as both method and attribute
                if callable(trades.count):
                    metrics['num_trades'] = trades.count()
                else:
                    metrics['num_trades'] = trades.count
                
                # If win_rate wasn't in stats, try to get it from trades
                if metrics['win_rate'] == 0 and hasattr(trades, 'win_rate'):
                    metrics['win_rate'] = trades.win_rate
                
                # Try to get profit factor from trades
                if hasattr(trades, 'profit_factor'):
                    metrics['profit_factor'] = trades.profit_factor
            # If that fails, use the records_readable DataFrame
            elif hasattr(trades, 'records_readable'):
                try:
                    trades_df = trades.records_readable
                    
                    # Handle both 'pnl' and 'PnL' column names
                    pnl_col = None
                    if 'PnL' in trades_df.columns:
                        pnl_col = 'PnL'
                    elif 'pnl' in trades_df.columns:
                        pnl_col = 'pnl'
                    
                    if pnl_col is not None:
                        metrics['num_trades'] = len(trades_df)
                        winning_trades = trades_df[trades_df[pnl_col] > 0]
                        losing_trades = trades_df[trades_df[pnl_col] <= 0]
                        
                        metrics['winning_trades'] = len(winning_trades)
                        metrics['losing_trades'] = len(losing_trades)
                        metrics['win_rate'] = len(winning_trades) / len(trades_df) if len(trades_df) > 0 else 0
                        
                        # Calculate profit factor
                        total_profit = winning_trades[pnl_col].sum() if len(winning_trades) > 0 else 0
                        total_loss = abs(losing_trades[pnl_col].sum()) if len(losing_trades) > 0 else 0
                        metrics['profit_factor'] = total_profit / total_loss if total_loss > 0 else (1.0 if total_profit > 0 else 0.0)
                        
                        # Average trade
                        metrics['avg_trade'] = trades_df[pnl_col].mean() if len(trades_df) > 0 else 0
                    else:
                        metrics['num_trades'] = len(trades_df)
                        metrics['winning_trades'] = 0
                        metrics['losing_trades'] = 0
                        metrics['win_rate'] = 0.0
                        metrics['profit_factor'] = 0.0
                        metrics['avg_trade'] = 0.0
                except Exception as e:
                    wfo_logger.warning(f"Failed to process trades using records_readable: {e}")
                    metrics['num_trades'] = 0
                    metrics['winning_trades'] = 0
                    metrics['losing_trades'] = 0
                    metrics['win_rate'] = 0.0
                    metrics['profit_factor'] = 0.0
                    metrics['avg_trade'] = 0.0
            else:
                metrics['num_trades'] = 0
                metrics['winning_trades'] = 0
                metrics['losing_trades'] = 0
                metrics['win_rate'] = 0.0
                metrics['profit_factor'] = 0.0
                metrics['avg_trade'] = 0.0
        else:
            metrics['num_trades'] = 0
            metrics['winning_trades'] = 0
            metrics['losing_trades'] = 0
            metrics['win_rate'] = 0.0
            metrics['profit_factor'] = 0.0
            metrics['avg_trade'] = 0.0
        
        # Make sure profit_factor is set
        if 'profit_factor' not in metrics:
            metrics['profit_factor'] = stats.get('profit_factor', 0)
            
        # Make sure avg_trade is set
        if 'avg_trade' not in metrics:
            metrics['avg_trade'] = stats.get('avg_trade', 0)
        
    except Exception as e:
        wfo_logger.warning(f"Error calculating metrics: {str(e)}")
        if chat_model_available():
            explanation = ask_chat_model(
                f"Error calculating portfolio metrics: {str(e)}. What might be causing this?")
            wfo_logger.info(f"Metric calculation error explanation: {explanation}")
        
        # Return default metrics if calculation fails
        metrics = {
            'sharpe': 0,
            'calmar': 0,
            'max_dd': 0,
            'total_return': 0,
            'win_rate': 0,
            'volatility': 0,
            'var': 0,
            'num_trades': 0,
            'profit_factor': 0,
            'avg_trade': 0
        }
    
    return metrics

def evaluate_parameter_sets(data, param_grid, optimization_metric='sharpe_ratio', split_id=None, use_parallel=USE_PARALLEL, num_cores=NUM_CORES):
    """
    Evaluate multiple parameter sets and return the best one based on the optimization metric.
    
    Args:
        data: DataFrame with OHLCV data
        param_grid: Dictionary with parameter names and possible values
        optimization_metric: Metric to optimize (e.g., 'sharpe_ratio')
        split_id: Optional identifier for the data split
        use_parallel: Whether to use parallel processing
        num_cores: Number of CPU cores to use for parallel processing
        
    Returns:
        tuple: (best_portfolio, best_metrics, best_params, split_id)
    """
    # Generate all parameter combinations
    param_combinations = []
    for param_name, param_values in param_grid.items():
        if isinstance(param_values, tuple) and len(param_values) == 3:
            # Handle range specifications (start, stop, step)
            start, stop, step = param_values
            if isinstance(step, int):
                values = list(range(start, stop + 1, step))
            else:
                # For float steps, use numpy arange
                values = np.arange(start, stop + step/2, step).tolist()
            param_grid[param_name] = values
    
    # Get all combinations of parameters
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    param_combinations = [dict(zip(keys, combo)) for combo in itertools.product(*values)]
    
    # Log the number of combinations
    wfo_logger.info(f"Evaluating {len(param_combinations)} parameter combinations for split {split_id}")
    
    # Evaluate all parameter sets
    results = []
    if use_parallel and num_cores > 1:
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            # Prepare arguments for parallel processing
            param_args = [(data, params, split_id) for params in param_combinations]
            
            # Use tqdm for progress tracking if available
            if 'tqdm' in sys.modules:
                results = list(tqdm(executor.map(evaluate_single_param_set_wrapper, param_args), 
                                    total=len(param_combinations), desc=f"Split {split_id}"))
            else:
                results = list(executor.map(evaluate_single_param_set_wrapper, param_args))
    else:
        # Sequential evaluation
        for i, params in enumerate(param_combinations):
            if 'tqdm' in sys.modules and i % 10 == 0:
                wfo_logger.info(f"Evaluating combination {i+1}/{len(param_combinations)} for split {split_id}")
            result = evaluate_parameter_set(data, params, split_id)
            results.append(result)
    
    # Filter out failed evaluations
    valid_results = [res for res in results if res[0] is not None and res[1] is not None]
    
    if not valid_results:
        wfo_logger.warning(f"No valid parameter sets found for split {split_id}")
        return None, None, None, split_id
    
    # Find the best result based on the optimization metric
    best_result = max(valid_results, key=lambda x: x[1].get(optimization_metric, -float('inf')))
    
    return best_result

def analyze_parameter_stability(all_params):
    """
    Analyze parameter stability across different WFO splits.
    
    Args:
        all_params: List of parameter dictionaries from each split
        
    Returns:
        dict: Stability metrics for each parameter
    """
    if not all_params or len(all_params) < 2:
        logging.warning("Not enough parameter sets to analyze stability")
        return {}
    
    # Create a DataFrame with all parameters
    params_df = pd.DataFrame(all_params)
    
    # Calculate stability metrics for each parameter
    stability = {}
    
    for param in params_df.columns:
        if param in ['initial_capital', 'commission_pct', 'slippage_pct']:
            # Skip fixed parameters
            continue
            
        # Extract parameter values
        values = params_df[param].values
        
        # Convert categorical parameters to numbers if needed
        if params_df[param].dtype == 'object':
            # For categorical parameters, calculate mode and frequency
            value_counts = params_df[param].value_counts()
            mode_val = value_counts.index[0]
            mode_freq = value_counts.iloc[0] / len(params_df)
            
            stability[param] = {
                'type': 'categorical',
                'mode': mode_val,
                'mode_frequency': mode_freq,
                'unique_values': len(value_counts),
                'stability_score': mode_freq
            }
        else:
            # For numerical parameters
            mean_val = np.mean(values)
            median_val = np.median(values)
            std_val = np.std(values)
            cov = std_val / mean_val if mean_val != 0 else float('inf')
            
            # A better stability metric for numerical parameters
            # Lower is more stable
            stability_score = min(1.0, cov)
            
            # Calculate percentages of values within ranges
            within_5pct = np.mean(np.abs(values - median_val) <= 0.05 * abs(median_val))
            within_10pct = np.mean(np.abs(values - median_val) <= 0.10 * abs(median_val))
            
            stability[param] = {
                'type': 'numerical',
                'mean': mean_val,
                'median': median_val,
                'std': std_val,
                'cov': cov,
                'stability_score': 1.0 - stability_score,  # Convert to 0-1 scale where 1 is most stable
                'within_5pct': within_5pct,
                'within_10pct': within_10pct
            }
    
    return stability


def recommend_final_parameters(all_params, stability_metrics):
    """
    Recommend final parameters based on stability analysis.
    
    Args:
        all_params: List of parameter dictionaries from each split
        stability_metrics: Parameter stability analysis from analyze_parameter_stability
        
    Returns:
        dict: Recommended final parameters
    """
    if not all_params:
        logging.error("No parameter sets available for final recommendation")
        return {}
    
    # Create a DataFrame with all parameters
    params_df = pd.DataFrame(all_params)
    
    # Initialize final parameters dictionary
    final_params = {}
    
    # Add fixed parameters
    for param in ['initial_capital', 'commission_pct', 'slippage_pct']:
        if param in params_df.columns:
            final_params[param] = params_df[param].iloc[0]
    
    # Process each parameter based on stability
    for param, metrics in stability_metrics.items():
        if metrics['type'] == 'categorical':
            # For categorical parameters, use the mode
            final_params[param] = metrics['mode']
        else:
            # For numerical parameters, use weighted approach based on stability
            stability_score = metrics['stability_score']
            
            if stability_score >= 0.8:
                # High stability - use median
                final_params[param] = metrics['median']
            elif stability_score >= 0.5:
                # Medium stability - use mean
                final_params[param] = metrics['mean']
            else:
                # Low stability - use last value (recency bias) or median of last N values
                recent_values = params_df[param].iloc[-3:].values
                final_params[param] = np.median(recent_values)
    
    # Ensure all parameters are present
    for param in PARAM_GRID.keys():
        if param not in final_params and param in params_df.columns:
            # Use median as fallback
            final_params[param] = params_df[param].median()
    
    # Log the final parameters
    logging.info(f"Recommended final parameters: {final_params}")
    
    return final_params


def save_final_parameters(params):
    """
    Save final parameters to a JSON file.
    
    Args:
        params: Dictionary of final parameters
        
    Returns:
        bool: True if successful, False if error encountered
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"output/wfo_params_{timestamp}.json"
        
        # Save parameters to file
        with open(filename, 'w') as f:
            json.dump(params, f, indent=4)
        
        logging.info(f"Final parameters saved to {filename}")
        
        # Also save to a fixed filename for automation
        with open("output/latest_wfo_params.json", 'w') as f:
            json.dump(params, f, indent=4)
        
        return True
    
    except Exception as e:
        logging.error(f"Error saving final parameters: {str(e)}")
        return False


def generate_wfo_report(train_portfolios, oos_portfolios, all_params):
    """
    Generate a comprehensive report on walk-forward optimization results.
    
    Args:
        train_portfolios: List of (portfolio, metrics, params, split_id) tuples for training data
        oos_portfolios: List of (portfolio, metrics, params, split_id) tuples for out-of-sample data
        all_params: List of parameter dictionaries from each split
        
    Returns:
        bool: True if successful, False if error encountered
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"output/wfo_report_{timestamp}.html"
        
        # Initialize report HTML
        report_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Walk-Forward Optimization Report - {timestamp}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #333366; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            </style>
        </head>
        <body>
            <h1>Walk-Forward Optimization Report</h1>
            <h2>Date: {timestamp}</h2>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Value</th>
                </tr>
                {''.join([f"<tr><td>{param}</td><td>{value}</td></tr>" for param, value in params.items()])}
            </table>
            <h2>Results</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                {''.join([f"<tr><td>{metric}</td><td>{value}</td></tr>" for metric, value in metrics.items()])}
            </table>
        </body>
        </html>
        """
        
        # Save report to file
        with open(filename, 'w') as f:
            f.write(report_html)
        
        logging.info(f"Walk-Forward Optimization report saved to {filename}")
        
        return True
    
    except Exception as e:
        logging.error(f"Error generating WFO report: {str(e)}")
        return False

def run_walk_forward_optimization(data, param_grid, optimization_metric='sharpe_ratio', in_sample_days=IN_SAMPLE_DAYS, out_sample_days=OUT_SAMPLE_DAYS, step_days=STEP_DAYS):
    """
    Run walk-forward optimization on the given data.
    
    Args:
        data: DataFrame with OHLCV data
        param_grid: Dictionary with parameter names and possible values
        optimization_metric: Metric to optimize (e.g., 'sharpe_ratio')
        in_sample_days: Number of days for in-sample (training) period
        out_sample_days: Number of days for out-of-sample (testing) period
        step_days: Number of days to step forward for each split
        
    Returns:
        tuple: (train_results, oos_results, all_params)
    """
    wfo_logger.info("Starting walk-forward optimization")
    
    # Create necessary splits
    total_days = len(data)
    min_days_needed = in_sample_days + out_sample_days
    
    if total_days < min_days_needed:
        wfo_logger.error(f"Not enough data for walk-forward optimization. Need at least {min_days_needed} days, but only have {total_days} days.")
        return [], [], []
    
    # Calculate number of splits
    max_start_idx = total_days - min_days_needed
    num_splits = max(1, max_start_idx // step_days + 1)
    
    wfo_logger.info(f"Creating {num_splits} splits for walk-forward optimization")
    
    # Initialize results lists
    train_results = []
    oos_results = []
    all_params = []
    
    # Run optimization for each split
    for split_id in range(num_splits):
        # Calculate indices for this split
        start_idx = split_id * step_days
        train_end_idx = start_idx + in_sample_days
        oos_end_idx = min(train_end_idx + out_sample_days, total_days)
        
        # Skip if we don't have enough data for out-of-sample
        if train_end_idx >= total_days:
            wfo_logger.warning(f"Split {split_id}: Not enough data for training. Skipping.")
            continue
        
        # Extract data for this split
        train_data = data.iloc[start_idx:train_end_idx].copy()
        oos_data = data.iloc[train_end_idx:oos_end_idx].copy()
        
        # Log split information
        wfo_logger.info(f"Split {split_id}: Training {train_data.index[0]} to {train_data.index[-1]} ({len(train_data)} days)")
        wfo_logger.info(f"Split {split_id}: Testing {oos_data.index[0]} to {oos_data.index[-1]} ({len(oos_data)} days)")
        
        # Find optimal parameters on training data
        best_train_portfolio, best_train_metrics, best_params, _ = evaluate_parameter_sets(
            train_data, param_grid, optimization_metric, split_id
        )
        
        # Skip if no valid parameters found
        if best_params is None:
            wfo_logger.warning(f"Split {split_id}: No valid parameters found. Skipping.")
            continue
        
        # Store the best parameters
        all_params.append(best_params)
        
        # Apply best parameters to out-of-sample data
        oos_portfolio, oos_metrics, _, _ = evaluate_parameter_set(oos_data, best_params, split_id)
        
        # Store results
        train_results.append((best_train_portfolio, best_train_metrics, best_params, split_id))
        if oos_portfolio is not None:
            oos_results.append((oos_portfolio, oos_metrics, best_params, split_id))
        
        # Log results
        wfo_logger.info(f"Split {split_id}: Best parameters: {best_params}")
        if best_train_metrics:
            wfo_logger.info(f"Split {split_id}: Training metrics: {best_train_metrics}")
        if oos_metrics:
            wfo_logger.info(f"Split {split_id}: Out-of-sample metrics: {oos_metrics}")
    
    # Analyze parameter stability
    if all_params:
        stability_metrics = analyze_parameter_stability(all_params)
        wfo_logger.info(f"Parameter stability metrics: {stability_metrics}")
        
        # Recommend final parameters
        final_params = recommend_final_parameters(all_params, stability_metrics)
        wfo_logger.info(f"Recommended final parameters: {final_params}")
        
        # Save final parameters
        save_final_parameters(final_params)
        
        # Generate report
        generate_wfo_report(train_results, oos_results, all_params)
    
    return train_results, oos_results, all_params

def create_pf_for_candlestick_strategy(data, entries, exits, init_cash=INITIAL_CAPITAL, size=None, sl_stop=None, tp_stop=None):
    """
    Wrapper function for create_portfolio_for_strategy for the candlestick strategy.
    
    Args:
        data: DataFrame with OHLCV data
        entries: Series of entry signals
        exits: Series of exit signals
        init_cash: Initial capital
        size: Optional size series
        sl_stop: Stop loss percentage (as decimal)
        tp_stop: Take profit percentage (as decimal)
        
    Returns:
        Portfolio object or CustomPortfolio object
    """
    # Ensure data types are correct
    if not isinstance(entries, pd.Series):
        entries = pd.Series(entries, index=data.index)
    if not isinstance(exits, pd.Series):
        exits = pd.Series(exits, index=data.index)
    
    # Convert stop_loss_pct and take_profit_pct to their decimal forms if they're passed as string-formatted percentages
    if isinstance(sl_stop, str) and sl_stop.endswith('%'):
        sl_stop = float(sl_stop.rstrip('%')) / 100
    elif isinstance(sl_stop, (int, float)):
        sl_stop = float(sl_stop)
        
    if isinstance(tp_stop, str) and tp_stop.endswith('%'):
        tp_stop = float(tp_stop.rstrip('%')) / 100
    elif isinstance(tp_stop, (int, float)):
        tp_stop = float(tp_stop)
    
    return create_portfolio_for_strategy(data, entries, exits, init_cash, size, sl_stop, tp_stop)

# This function needs to be outside of evaluate_parameter_sets for parallel processing
def evaluate_single_param_set_wrapper(args):
    """Wrapper for evaluate_parameter_set to use in parallel processing."""
    data, params, split_id = args
    return evaluate_parameter_set(data, params, split_id)

# Main execution
if __name__ == "__main__":
    # Configure chat provider if available
    if chat_model_available():
        wfo_logger.info("Chat model is available and will be used for analysis")
    else:
        wfo_logger.warning("Chat model is not available. Some features will be limited.")
    
    # Fetch historical data
    wfo_logger.info(f"Fetching historical data for {SYMBOL} from {WFO_START_DATE} to {WFO_END_DATE}")
    try:
        data = fetch_historical_data(SYMBOL, WFO_START_DATE, WFO_END_DATE, GRANULARITY_SECONDS)
        
        if data is None or len(data) == 0:
            wfo_logger.error("Failed to fetch historical data. Exiting.")
            sys.exit(1)
        
        wfo_logger.info(f"Fetched {len(data)} periods of historical data")
        
        # Run walk-forward optimization
        train_results, oos_results, all_params = run_walk_forward_optimization(
            data, PARAM_GRID, OPTIMIZATION_METRIC, IN_SAMPLE_DAYS, OUT_SAMPLE_DAYS, STEP_DAYS
        )
        
        # Summarize results
        if all_params:
            wfo_logger.info(f"Walk-forward optimization completed with {len(all_params)} valid splits")
            
            # Calculate overall out-of-sample performance
            if oos_results:
                total_oos_return = sum([m[1].get('total_return', 0) for m in oos_results if m[1] is not None])
                avg_oos_sharpe = np.mean([m[1].get('sharpe', 0) for m in oos_results if m[1] is not None])
                wfo_logger.info(f"Overall out-of-sample performance: Return = {total_oos_return:.2f}%, Sharpe = {avg_oos_sharpe:.2f}")
            
            # Final recommended parameters from stability analysis
            stability_metrics = analyze_parameter_stability(all_params)
            final_params = recommend_final_parameters(all_params, stability_metrics)
            wfo_logger.info(f"Final recommended parameters: {final_params}")
            
            # Save to file
            save_final_parameters(final_params)
        else:
            wfo_logger.warning("Walk-forward optimization failed to produce valid results")
    
    except Exception as e:
        wfo_logger.error(f"Error in walk-forward optimization: {str(e)}")
        if chat_model_available():
            explanation = ask_chat_model(
                f"Error in walk-forward optimization: {str(e)}. What might be causing this error?")
            wfo_logger.info(f"Error explanation: {explanation}")
    
    # Exit successfully
    sys.exit(0)