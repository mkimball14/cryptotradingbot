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
# Use more targeted parameter ranges based on domain knowledge
PARAM_GRID = {
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
FACTOR_NAMES = ['volatility_regime', 'consolidation_breakout', 'volume_divergence', 'market_microstructure']
# Reduce weight combinations to speed up processing
weight_options = [
    # Equal weights
    {'volatility_regime': 0.25, 'consolidation_breakout': 0.25, 'volume_divergence': 0.25, 'market_microstructure': 0.25},
    # Emphasis on volatility regime
    {'volatility_regime': 0.6, 'consolidation_breakout': 0.2, 'volume_divergence': 0.1, 'market_microstructure': 0.1}
]
WEIGHT_COMBINATIONS = weight_options

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


def create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL):
    """
    Create portfolio for specified parameters.
    
    Args:
        data: DataFrame containing OHLCV data and indicators
        params: Dictionary of strategy parameters
        init_cash: Initial capital
        
    Returns:
        Portfolio object or None if creation fails
    """
    try:
        import pandas as pd
        
        # Handle different data types
        if isinstance(data, pd.DataFrame):
            # Make a copy to avoid modifying the original
            df = data.copy()
            
            # Ensure column names are standardized to lowercase
            df.columns = [col.lower() for col in df.columns]
            
            # Check if we have all required columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in required_cols:
                if col not in df.columns:
                    # Try to find a case-insensitive match
                    matching_cols = [c for c in df.columns if c.lower() == col.lower()]
                    if matching_cols:
                        df[col] = df[matching_cols[0]]
                    else:
                        logging.error(f"Required column {col} not found. Available columns: {df.columns.tolist()}")
                        return None
        elif isinstance(data, dict):
            # For dictionary data, create a DataFrame with standardized column names
            df = {}
            column_map = {
                'open': ['open', 'Open', 'OPEN'],
                'high': ['high', 'High', 'HIGH'],
                'low': ['low', 'Low', 'LOW'],
                'close': ['close', 'Close', 'CLOSE'],
                'volume': ['volume', 'Volume', 'VOLUME']
            }
            
            # Try to find matching columns
            for std_col, variants in column_map.items():
                found = False
                for variant in variants:
                    if variant in data:
                        df[std_col] = data[variant]
                        found = True
                        break
                
                if not found:
                    logging.error(f"Required column {std_col} not found in data dictionary")
                    return None
            
            # Include any additional indicators from the data dictionary
            for key, value in data.items():
                if key.lower() not in ['open', 'high', 'low', 'close', 'volume']:
                    df[key.lower()] = value
        else:
            logging.error(f"Unsupported data type: {type(data)}")
            return None
        
        # Use our standardized create_portfolio function
        portfolio, success = create_portfolio(df, params)
        
        if not success or portfolio is None:
            logging.error(f"Failed to create portfolio with params: {params}")
            return None
            
        return portfolio
        
    except Exception as e:
        logging.error(f"Error creating portfolio: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        return None

# =============================================================================
# Parallel Optimization Functions
# =============================================================================
def evaluate_params(data, params, init_cash=INITIAL_CAPITAL):
    """
    Evaluate a set of parameters and return the objective value.
    
    Args:
        data: Dictionary with OHLCV data
        params: Dictionary of strategy parameters
        init_cash: Initial capital
        
    Returns:
        float: Objective value (Sharpe ratio or -inf if invalid)
    """
    try:
        # Log parameters for debugging
        logging.debug(f"Evaluating parameters: {params}")
        
        # Create portfolio with parameters
        pf = create_pf_for_params(data, params, init_cash=init_cash)
        
        if pf is None:
            logging.debug(f"Portfolio creation failed for params: {params}")
            return -float('inf')
        
        # Extract portfolio metrics
        stats = pf.stats()
        
        # Get relevant metrics for filtering
        total_trades = stats['total_trades']
        total_closed_trades = stats['total_closed_trades']
        win_rate = stats['win_rate']
        sharpe_ratio = stats['sharpe_ratio']
        max_dd = stats['max_drawdown']
        profit_factor = stats.get('profit_factor', 0)
        
        # More relaxed filtering - Accept portfolios with fewer trades and lower metrics
        min_trades = 3         # Reduced from 5
        min_win_rate = 0.25    # Reduced from 0.3
        min_sharpe = 0.2       # Reduced from 0.5
        max_dd_allowed = 0.3   # Increased from 0.2
        min_profit_factor = 1.0 # Reduced from 1.5
        
        # Filter valid portfolios
        if total_trades < min_trades:
            logging.debug(f"Rejected: too few trades {total_trades} < {min_trades}")
            return -float('inf')
        if win_rate < min_win_rate:
            logging.debug(f"Rejected: win rate too low {win_rate:.2f} < {min_win_rate:.2f}")
            return -float('inf')
        if sharpe_ratio < min_sharpe:
            logging.debug(f"Rejected: Sharpe ratio too low {sharpe_ratio:.2f} < {min_sharpe:.2f}")
            return -float('inf')
        if max_dd > max_dd_allowed:
            logging.debug(f"Rejected: Max drawdown too high {max_dd:.2f} > {max_dd_allowed:.2f}")
            return -float('inf')
        if profit_factor < min_profit_factor:
            logging.debug(f"Rejected: Profit factor too low {profit_factor:.2f} < {min_profit_factor:.2f}")
            return -float('inf')
        
        # For valid portfolio, log metrics
        logging.info(f"Valid portfolio: trades={total_trades}, win_rate={win_rate:.2f}, sharpe={sharpe_ratio:.2f}, max_dd={max_dd:.2f}, profit_factor={profit_factor:.2f}")
        
        # Use Sharpe ratio as the objective value
        return sharpe_ratio
    
    except Exception as e:
        logging.error(f"Error evaluating parameters: {str(e)}")
        return -float('inf')

# =============================================================================
# Main WFO Function
# =============================================================================

def get_optimization_advice_from_chat_model():
    """Use the VectorBT Pro chat model to get optimization advice."""
    chat_model = get_chat_model()
    if chat_model is None:
        return None
    
    query = """
    I'm running a Walk-Forward Optimization process for a trading strategy using VectorBT Pro. 
    Please provide advice on how to make the optimization process faster and more efficient.
    Specifically, I need tips on:
    1. Parameter grid design to reduce combinations while maintaining effectiveness
    2. Data preprocessing that can speed up calculations
    3. Signal generation optimizations
    4. Any other performance tips for VectorBT Pro
    """
    
    try:
        advice = ask_chat_model(query)
        return advice
    except Exception as e:
        wfo_logger.error(f"Error getting optimization advice: {e}")
        return None

def prepare_data_efficiently(data):
    """
    Prepare data efficiently for faster signal generation and backtesting.
    
    - Uses NumPy arrays where possible
    - Precomputes common values
    - Ensures optimal data types
    """
    if data.empty:
        return data
        
    # Ensure data is sorted by index
    data = data.sort_index()
    
    # Convert to more efficient dtypes
    float_cols = ['open', 'high', 'low', 'close']
    for col in float_cols:
        if col in data.columns:
            data[col] = data[col].astype(np.float64)
    
    if 'volume' in data.columns:
        data['volume'] = data['volume'].astype(np.float64)
    
    # Precompute common values
    data['returns'] = data['close'].pct_change()
    data['log_returns'] = np.log(data['close'] / data['close'].shift(1))
    data['hl_range'] = (data['high'] - data['low']) / data['close'].replace(0, np.nan)
    
    return data

def filter_valid_portfolios(portfolios, param_combinations):
    """Filter out invalid portfolios based on performance metrics."""
    valid_indices = []
    valid_portfolios = []
    valid_params = []
    
    for i, pf in enumerate(portfolios):
        if pf is None:
            continue
        
        try:
            # Get basic metrics
            metrics = pf.metrics()
            total_trades = metrics['total_trades']
            win_rate = metrics['win_rate'] if total_trades > 0 else 0
            sharpe_ratio = metrics['sharpe_ratio']
            max_dd = metrics['max_drawdown']
            
            # Apply less strict filtering criteria
            if (total_trades >= MIN_TOTAL_TRADES and 
                win_rate >= MIN_WIN_RATE and 
                sharpe_ratio >= MIN_SHARPE_RATIO and
                max_dd >= MAX_DRAWDOWN):
                
                valid_indices.append(i)
                valid_portfolios.append(pf)
                valid_params.append(param_combinations[i])
                
                # Log more details about the valid portfolio
                wfo_logger.info(f"Valid portfolio found: Sharpe={sharpe_ratio:.2f}, Win Rate={win_rate:.2f}, Trades={total_trades}, Max DD={max_dd:.2f}")
        except Exception as e:
            wfo_logger.warning(f"Could not evaluate portfolio at index {i}: {str(e)}")
    
    return valid_portfolios, valid_params, valid_indices

def optimize_parameters(data, params_space, n_trials=50, progress_callback=None):
    """
    Optimize strategy parameters using Optuna.
    
    Args:
        data (pd.DataFrame or dict): OHLCV data with indicators
        params_space (dict): Parameter space for optimization
        n_trials (int): Number of optimization trials
        progress_callback (callable, optional): Callback for progress updates
        
    Returns:
        tuple: (best_params, best_score, trial_history)
    """
    import optuna
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
    import multiprocessing
    import signal
    import numpy as np
    import pandas as pd
    
    # Store details of all trials
    trial_history = []
    
    # Set custom signal handler for graceful interruption
    original_sigint_handler = signal.getsignal(signal.SIGINT)
    
    def sigint_handler(sig, frame):
        logging.warning("Received interrupt signal. Finishing current trial and stopping optimization.")
        signal.signal(signal.SIGINT, original_sigint_handler)
    
    # Set signal handler
    signal.signal(signal.SIGINT, sigint_handler)
    
    # Prepare data for optimization
    # Check if data is a dictionary or DataFrame
    if isinstance(data, dict):
        # Keep data as-is for dictionary input, no need to convert columns to lowercase
        data_copy = data
    else:
        # For DataFrame input, standardize column names
        data_copy = data.copy()
        data_copy.columns = [col.lower() for col in data_copy.columns]
        
        # Ensure we have the expected columns for DataFrame
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in data_copy.columns:
                # Try to find a case-insensitive match
                matching_cols = [c for c in data_copy.columns if c.lower() == col.lower()]
                if matching_cols:
                    data_copy[col] = data_copy[matching_cols[0]]
                else:
                    logging.error(f"Required column {col} not found in data. Available columns: {data_copy.columns.tolist()}")
                    return {}, float('-inf'), []
    
    def objective(trial):
        """Sample parameters and evaluate portfolio performance"""
        params = {}
        for param_name, param_range in params_space.items():
            if isinstance(param_range, tuple) and len(param_range) == 2:
                if isinstance(param_range[0], int) and isinstance(param_range[1], int):
                    params[param_name] = trial.suggest_int(param_name, param_range[0], param_range[1])
                else:
                    params[param_name] = trial.suggest_float(param_name, param_range[0], param_range[1])
            elif isinstance(param_range, list):
                params[param_name] = trial.suggest_categorical(param_name, param_range)
        
        try:
            # Use create_pf_for_params function to create the portfolio
            portfolio = create_pf_for_params(data_copy, params)
            
            # Check if portfolio creation was successful
            if portfolio is None or not hasattr(portfolio, 'trades') or len(portfolio.trades) == 0:
                logging.warning(f"No valid portfolio created with parameters: {params}")
                return float('-inf')
            
            # Calculate performance metrics
            metrics = evaluate_portfolio(portfolio)
            
            # Filter based on minimum requirements
            min_trades = 3
            min_win_rate = 0.30
            min_sharpe = 0.1
            max_drawdown_limit = -0.25  # -25% maximum drawdown allowed
            
            total_trades = metrics['total_trades']
            win_rate = metrics['win_rate']
            sharpe_ratio = metrics['sharpe_ratio']
            max_drawdown = metrics['max_drawdown']
            profit_factor = metrics['profit_factor']
            
            # Log all portfolio metrics for debugging
            logging.debug(f"Portfolio metrics: Trades={total_trades}, Win Rate={win_rate:.2f}, "
                          f"Sharpe={sharpe_ratio:.2f}, Max DD={max_drawdown:.2f}, PF={profit_factor:.2f}")
            
            # Filter invalid portfolios
            if total_trades < min_trades:
                logging.debug(f"Rejected: Insufficient trades ({total_trades} < {min_trades})")
                return float('-inf')
            
            if win_rate < min_win_rate:
                logging.debug(f"Rejected: Low win rate ({win_rate:.2f} < {min_win_rate:.2f})")
                return float('-inf')
            
            if sharpe_ratio < min_sharpe:
                logging.debug(f"Rejected: Low Sharpe ratio ({sharpe_ratio:.2f} < {min_sharpe:.2f})")
                return float('-inf')
            
            if max_drawdown < max_drawdown_limit:
                logging.debug(f"Rejected: Excessive drawdown ({max_drawdown:.2f} < {max_drawdown_limit:.2f})")
                return float('-inf')
            
            # Calculate score based on multiple metrics (weighted average)
            # This formula prioritizes Sharpe ratio and win rate
            score = (
                0.4 * sharpe_ratio +               # 40% weight to Sharpe ratio
                0.3 * win_rate +                   # 30% weight to win rate 
                0.1 * (1 + max_drawdown) +         # 10% weight to drawdown (less negative is better)
                0.2 * min(profit_factor, 3.0)/3.0  # 20% weight to profit factor (capped at 3.0)
            )
            
            # Penalize excessive drawdowns
            if max_drawdown < -0.15:  # More than 15% drawdown
                score *= (1 + max_drawdown)  # Reduce score for high drawdowns
            
            # Store trial details for later analysis
            trial_details = {
                'params': params,
                'metrics': metrics,
                'score': score
            }
            trial_history.append(trial_details)
            
            # Log successful evaluation
            logging.info(f"Valid portfolio: score={score:.4f}, return={metrics['total_return']:.4f}, "
                         f"sharpe={metrics['sharpe_ratio']:.2f}, trades={metrics['total_trades']}, "
                         f"win_rate={metrics['win_rate']:.2f}, drawdown={metrics['max_drawdown']:.2f}")
            
            return score
            
        except Exception as e:
            logging.error(f"Error evaluating parameters {params}: {str(e)}")
            import traceback
            logging.debug(traceback.format_exc())
            return float('-inf')
    
    try:
        # Create Optuna study
        study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler())
        
        # Number of processes to use
        n_jobs = min(multiprocessing.cpu_count() - 1, 4)  # Leave 1 CPU free, max 4
        n_jobs = max(1, n_jobs)  # At least 1 job
        
        # Log optimization details
        logging.info(f"Starting parameter optimization with {n_trials} trials using {n_jobs} parallel workers")
        
        # Progress tracking
        last_progress = 0
        
        def progress_monitor(study, trial):
            nonlocal last_progress
            progress = int(100 * (trial.number + 1) / n_trials)
            
            # Only log when progress increases by at least 10%
            if progress >= last_progress + 10 or trial.number == n_trials - 1:
                logging.info(f"Optimization progress: {progress}% ({trial.number + 1}/{n_trials} trials)")
                last_progress = progress
                
                # Update callback if provided
                if progress_callback:
                    progress_callback(progress)
                    
            # Log best score so far
            if study.best_trial and study.best_trial.value > float('-inf'):
                if trial.number % 10 == 0 or trial.number == n_trials - 1:
                    logging.info(f"Current best score: {study.best_value:.4f} (trial #{study.best_trial.number})")
        
        try:
            # Try parallel optimization first
            study.optimize(
                objective, 
                n_trials=n_trials,
                n_jobs=n_jobs,
                callbacks=[progress_monitor]
            )
        except (KeyboardInterrupt, Exception) as e:
            logging.warning(f"Parallel optimization failed or interrupted: {str(e)}. Switching to sequential execution.")
            # Fall back to sequential optimization
            remaining_trials = max(0, n_trials - len(study.trials))
            if remaining_trials > 0:
                logging.info(f"Continuing with {remaining_trials} remaining trials in sequential mode")
                study.optimize(
                    objective,
                    n_trials=remaining_trials,
                    callbacks=[progress_monitor]
                )
        
        # Restore original signal handler
        signal.signal(signal.SIGINT, original_sigint_handler)
        
        # Check if any valid trials were found
        valid_trials = [t for t in study.trials if t.value > float('-inf')]
        
        if not valid_trials:
            logging.critical("No valid parameter sets found during optimization!")
            # Return reasonable defaults instead of failing
            default_params = {param: (param_range[0] + param_range[1]) / 2 if isinstance(param_range, tuple) else param_range[0]
                              for param, param_range in params_space.items()}
            return default_params, float('-inf'), trial_history
        
        # Get best parameters
        best_params = study.best_params
        best_score = study.best_value
        
        # Log optimization results
        logging.info(f"Optimization completed. Best score: {best_score:.4f}")
        logging.info(f"Best parameters: {best_params}")
        logging.info(f"Valid trials: {len(valid_trials)}/{len(study.trials)}")
        
        return best_params, best_score, trial_history
    
    except Exception as e:
        logging.error(f"Error during optimization: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        
        # Return defaults in case of failure
        default_params = {param: (param_range[0] + param_range[1]) / 2 if isinstance(param_range, tuple) else param_range[0]
                          for param, param_range in params_space.items()}
        return default_params, float('-inf'), trial_history

def get_relaxed_parameter_space(params_space):
    """
    Create a more relaxed parameter space to increase chances of finding valid parameters.
    
    Args:
        params_space: Original parameter space
        
    Returns:
        Dictionary with relaxed parameter ranges
    """
    relaxed_space = {}
    
    # For each parameter, expand its range to be more inclusive
    for param_name, param_range in params_space.items():
        if isinstance(param_range, tuple) and len(param_range) == 2:
            if 'rsi_lower' in param_name:
                # Allow higher RSI values for buy signals
                relaxed_space[param_name] = (param_range[0], min(param_range[1] + 10, 40))
            elif 'rsi_upper' in param_name:
                # Allow lower RSI values for sell signals
                relaxed_space[param_name] = (max(param_range[0] - 10, 60), param_range[1])
            elif 'bb_alpha' in param_name or 'bb_dev' in param_name:
                # Wider Bollinger Bands for more signals
                relaxed_space[param_name] = (max(param_range[0] - 0.5, 0.5), param_range[1] + 0.5)
            elif 'stop_loss' in param_name or 'sl_pct' in param_name:
                # Allow larger stop losses
                relaxed_space[param_name] = (param_range[0], min(param_range[1] * 1.5, 0.2))
            elif 'take_profit' in param_name or 'tp_pct' in param_name:
                # Allow smaller take profits
                relaxed_space[param_name] = (max(param_range[0] * 0.5, 0.01), param_range[1])
            elif 'size_pct' in param_name or 'risk_per_trade' in param_name:
                # Allow smaller position sizes
                relaxed_space[param_name] = (max(param_range[0] * 0.5, 0.01), param_range[1])
            else:
                # Default: expand range by 20% on both ends
                range_size = param_range[1] - param_range[0]
                relaxed_space[param_name] = (
                    max(param_range[0] - range_size * 0.2, 0), 
                    param_range[1] + range_size * 0.2
                )
        else:
            # For categorical or other types, keep as is
            relaxed_space[param_name] = param_range
    
    logging.info(f"Created relaxed parameter space: {relaxed_space}")
    return relaxed_space

def check_portfolio_validity(metrics):
    """
    Check if a portfolio meets minimum performance requirements.
    
    Args:
        metrics: Dictionary of portfolio metrics
        
    Returns:
        Tuple of (is_valid, reason)
    """
    # Minimum requirements for a valid portfolio
    min_trades = 2  # At least 2 trades
    min_win_rate = 0.2  # At least 20% win rate
    min_sharpe = 0.1  # At least 0.1 Sharpe ratio
    max_drawdown = 0.4  # Maximum 40% drawdown
    min_profit_factor = 0.8  # At least 0.8 profit factor
    
    # Check each criterion
    if metrics['total_trades'] < min_trades:
        return False, f"Insufficient trades: {metrics['total_trades']} < {min_trades}"
    
    if metrics['win_rate'] < min_win_rate:
        return False, f"Low win rate: {metrics['win_rate']:.2f} < {min_win_rate}"
    
    if metrics['sharpe_ratio'] < min_sharpe:
        return False, f"Low Sharpe ratio: {metrics['sharpe_ratio']:.2f} < {min_sharpe}"
    
    if abs(metrics['max_drawdown']) > max_drawdown:
        return False, f"High drawdown: {abs(metrics['max_drawdown']):.2f} > {max_drawdown}"
    
    if metrics['profit_factor'] < min_profit_factor:
        return False, f"Low profit factor: {metrics['profit_factor']:.2f} < {min_profit_factor}"
    
    return True, "Valid portfolio"

def run_walk_forward_optimization():
    """
    Run the walk-forward optimization process.
    """
    import pandas as pd
    import numpy as np
    import time
    import json
    from datetime import datetime, timedelta
    import os

    # Configure chat provider if available
    chat_provider = None
    try:
        chat_provider = setup_chat_provider()
    except Exception as e:
        logging.warning(f"Chat provider setup failed: {e}. Continuing without chat features.")

    # Define parameter grid for optimization
    params_space = {
        # RSI parameters
        'rsi_lower': (20, 40),  # Buy signal RSI threshold
        'rsi_upper': (60, 80),  # Sell signal RSI threshold
        
        # Bollinger Bands parameters
        'bb_window': (10, 30),  # Window for BB calculation
        'bb_alpha': (1.5, 2.5),  # Number of standard deviations
        
        # Volatility parameters (ATR-based)
        'volatility_lower': (0.005, 0.03),  # Min volatility for entry
        'volatility_upper': (0.02, 0.1),    # Max volatility for entry
        
        # Money management
        'stop_loss_pct': (0.02, 0.10),      # Stop loss percentage
        'take_profit_pct': (0.03, 0.15),    # Take profit percentage
        'size_pct': (0.1, 0.5),             # Position size as % of capital
        'max_holdings': (1, 3)              # Maximum positions allowed
    }

    # Settings for walk-forward optimization
    SYMBOL = "BTC/USD"
    TIMEFRAME = "1d"
    LOOKBACK_DAYS = 365
    TRAIN_SIZE = 0.7  # 70% of data used for training
    WINDOW_DAYS = 120  # Size of each WFO window
    STEP_DAYS = 40     # Number of days to step forward each iteration
    OUT_SAMPLE_DAYS = 40  # Number of days in out-of-sample period
    N_TRIALS = 50      # Number of optimization trials per window

    # Check if STEP_DAYS > OUT_SAMPLE_DAYS which would lead to gaps
    if STEP_DAYS > OUT_SAMPLE_DAYS:
        logging.warning(f"STEP_DAYS ({STEP_DAYS}) > OUT_SAMPLE_DAYS ({OUT_SAMPLE_DAYS}). This will cause out-of-sample periods to overlap.")

    # Load data
    try:
        data = load_data(SYMBOL, TIMEFRAME, LOOKBACK_DAYS)
        if data is None or len(data['close']) < 2:
            logging.error("Failed to load sufficient data")
            return False
        
        # Handle any NaN values
        for key in data:
            if isinstance(data[key], (pd.Series, pd.DataFrame)) and data[key].isna().any().any():
                logging.warning(f"NaN values found in {key}, filling with forward fill")
                data[key] = data[key].ffill().bfill()
                
        logging.info(f"Successfully loaded {len(data['close'])} bars of data for {SYMBOL}")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return False

    # Create sliding windows for walk-forward optimization
    dates = data['close'].index
    total_days = (dates[-1] - dates[0]).days
    
    # Calculate number of windows based on total days and step size
    num_windows = max(1, (total_days - WINDOW_DAYS) // STEP_DAYS + 1)
    logging.info(f"Creating {num_windows} WFO splits with training size {TRAIN_SIZE}")
    
    # Initialize lists to store results
    all_params = []
    oos_portfolios = []
    
    # Process each window
    for i in range(num_windows):
        # Define the window boundaries
        start_idx = i * STEP_DAYS
        end_idx = min(start_idx + WINDOW_DAYS, len(dates) - 1)
        
        # Skip if window is too small
        if end_idx - start_idx < 30:
            logging.warning(f"Window {i+1} too small, skipping")
            continue
            
        # Extract window data
        window_start = dates[start_idx]
        window_end = dates[end_idx]
        window_data = {}
        
        for key, values in data.items():
            # Filter based on dates for Series and DataFrames
            if isinstance(values, (pd.Series, pd.DataFrame)):
                mask = (values.index >= window_start) & (values.index <= window_end)
                window_data[key] = values.loc[mask]
            else:
                window_data[key] = values
        
        # Split into training and testing sets
        split_idx = int(len(window_data['close']) * TRAIN_SIZE)
        if split_idx <= 10:
            logging.warning(f"Training set for window {i+1} too small, skipping")
            continue
            
        train_data = {}
        test_data = {}
        
        for key, values in window_data.items():
            if isinstance(values, (pd.Series, pd.DataFrame)):
                train_data[key] = values.iloc[:split_idx]
                test_data[key] = values.iloc[split_idx:]
            else:
                train_data[key] = values
                test_data[key] = values
        
        # Log split information
        logging.info(f"Split {i+1}: Training size: {len(train_data['close'])}, Testing size: {len(test_data['close'])}")
        logging.info(f"Split {i+1}: Training dates: {train_data['close'].index[0]} to {train_data['close'].index[-1]}")
        logging.info(f"Split {i+1}: Testing dates: {test_data['close'].index[0]} to {test_data['close'].index[-1]}")
        
        # Optimize parameters on training data
        logging.info(f"Optimizing parameters for split {i+1} with {N_TRIALS} trials")
        start_time = time.time()
        
        best_params, best_score, trial_history = optimize_parameters(train_data, params_space, n_trials=N_TRIALS)
        
        logging.info(f"Optimization completed in {time.time() - start_time:.1f} seconds")
        
        # Check if we found valid parameters
        if best_params is None:
            logging.critical(f"No valid parameters found for split {i+1}, skipping OOS processing")
            
            # Try with default parameters as fallback
            logging.info("Attempting with default parameters as fallback")
            default_params = {
                'rsi_lower': 30,
                'rsi_upper': 70,
                'bb_window': 20,
                'bb_alpha': 2.0,
                'volatility_lower': 0.01,
                'volatility_upper': 0.05,
                'stop_loss_pct': 0.05,
                'take_profit_pct': 0.1,
                'size_pct': 0.2,
                'max_holdings': 1
            }
            
            # Test with default parameters on out-of-sample data
            try:
                oos_pf = create_pf_for_params(test_data, default_params)
                if oos_pf is not None:
                    oos_metrics = evaluate_portfolio(oos_pf)
                    oos_portfolios.append((oos_pf, oos_metrics, default_params, i))
                    logging.info(f"Added OOS portfolio for split {i+1} using default parameters")
                    
                    # Store parameters
                    all_params.append((default_params, i, 'default'))
                else:
                    logging.error(f"Default parameters failed for split {i+1}")
            except Exception as e:
                logging.error(f"Error creating OOS portfolio with default parameters: {e}")
            
            continue
            
        # Store the best parameters
        all_params.append((best_params, i, 'optimized'))
        
        # Test optimized parameters on out-of-sample data
        try:
            oos_pf = create_pf_for_params(test_data, best_params)
            if oos_pf is not None:
                oos_metrics = evaluate_portfolio(oos_pf)
                oos_portfolios.append((oos_pf, oos_metrics, best_params, i))
                logging.info(f"Added OOS portfolio for split {i+1}")
            else:
                logging.error(f"Failed to create OOS portfolio for split {i+1}")
        except Exception as e:
            logging.error(f"Error creating OOS portfolio: {e}")
    
    # Check if we have any OOS portfolios
    if not oos_portfolios:
        logging.critical("No OOS portfolios generated - WFO process failed")
        return False
    
    # Combine OOS portfolios to evaluate overall performance
    try:
        # Combine performance metrics
        combined_metrics = {
            'total_return': np.mean([m['total_return'] for _, m, _, _ in oos_portfolios]),
            'sharpe_ratio': np.mean([m['sharpe_ratio'] for _, m, _, _ in oos_portfolios]),
            'sortino_ratio': np.mean([m['sortino_ratio'] for _, m, _, _ in oos_portfolios if 'sortino_ratio' in m]),
            'max_drawdown': np.mean([m['max_drawdown'] for _, m, _, _ in oos_portfolios]),
            'win_rate': np.mean([m['win_rate'] for _, m, _, _ in oos_portfolios]),
            'profit_factor': np.mean([m['profit_factor'] for _, m, _, _ in oos_portfolios if 'profit_factor' in m]),
            'num_portfolios': len(oos_portfolios)
        }
        
        logging.info(f"WFO completed. Overall metrics: Sharpe: {combined_metrics['sharpe_ratio']:.2f}, "
                    f"Return: {combined_metrics['total_return']:.2%}, "
                    f"Win Rate: {combined_metrics['win_rate']:.2%}")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            'timestamp': timestamp,
            'symbol': SYMBOL,
            'timeframe': TIMEFRAME,
            'overall_metrics': combined_metrics,
            'parameters': [{'params': p[0], 'window': p[1], 'type': p[2]} for p in all_params],
            'window_metrics': [{'metrics': m, 'window': i, 'params': p} 
                              for _, m, p, i in oos_portfolios]
        }
        
        # Create results directory if it doesn't exist
        os.makedirs('results', exist_ok=True)
        
        # Save to JSON file
        with open(f'results/wfo_results_{timestamp}.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logging.info(f"Results saved to results/wfo_results_{timestamp}.json")
        return True
        
    except Exception as e:
        logging.error(f"Error in final WFO evaluation: {e}")
        return False

def calculate_performance_metrics(portfolio):
    """Calculate key performance metrics from a portfolio object."""
    metrics = {}
    try:
        # Basic metrics
        stats = portfolio.stats()
        metrics['sharpe'] = stats.get('sharpe_ratio', 0)
        metrics['calmar'] = stats.get('calmar_ratio', 0)
        metrics['max_dd'] = stats.get('max_drawdown', 0)
        metrics['total_return'] = stats.get('total_return', 0)
        metrics['win_rate'] = stats.get('win_rate', 0)
        
        # Risk metrics
        risk = portfolio.get_risk_metrics() if hasattr(portfolio, 'get_risk_metrics') else {}
        metrics['volatility'] = risk.get('volatility', 0)
        metrics['var'] = risk.get('var', 0)
        
        # Add number of trades
        metrics['num_trades'] = len(portfolio.trades) if hasattr(portfolio, 'trades') else 0
        
        # Calculated metrics
        metrics['profit_factor'] = stats.get('profit_factor', 0)
        metrics['avg_trade'] = stats.get('avg_trade', 0)
        
    except Exception as e:
        wfo_logger.warning(f"Error calculating metrics: {str(e)}")
        # Use chat model to help debug metrics calculation issues
        if chat_model_available():
            explanation = ask_chat_model(
                f"Error calculating portfolio metrics: {str(e)}. What might be causing this?")
            wfo_logger.info(f"Metric calculation error explanation: {explanation}")
    
    return metrics

def analyze_parameter_stability(all_parameters):
    """
    Analyze the stability of parameters across WFO splits.
    Returns a dict with stability metrics for each parameter.
    """
    if not all_parameters or len(all_parameters) < 2:
        return {}
    
    # Convert list of parameter dicts to dict of parameter lists
    param_values = {}
    for params in all_parameters:
        for key, value in params.items():
            if key not in param_values:
                param_values[key] = []
            param_values[key].append(value)
    
    # Calculate stability metrics for each parameter
    stability = {}
    for param_name, values in param_values.items():
        # Skip if not enough values
        if len(values) < 2:
            continue
            
        # Convert to numpy array for calculations
        values_array = np.array(values)
        
        # Calculate statistics
        mean = np.mean(values_array)
        std = np.std(values_array)
        cv = std / mean if mean != 0 else float('inf')  # Coefficient of variation
        
        stability[param_name] = {
            'mean': mean,
            'std': std,
            'cv': cv,
            'min': np.min(values_array),
            'max': np.max(values_array),
            'range': np.max(values_array) - np.min(values_array),
            'values': values
        }
    
    return stability

def recommend_final_parameters(all_parameters, stability):
    """
    Recommend final parameters based on WFO results and stability analysis.
    """
    if not all_parameters:
        return {}
    
    # Start with the most recent parameters as the base
    final_params = all_parameters[-1].copy()
    
    # For each parameter, decide whether to use mean, median, or most recent value
    for param_name, metrics in stability.items():
        # Skip if parameter not in most recent set
        if param_name not in final_params:
                continue
                
        # If parameter is highly unstable, maybe ask chat model for help
        if metrics['cv'] > 0.5 and chat_model_available():
            suggestion = ask_chat_model(
                f"Parameter '{param_name}' is unstable across WFO splits (CV={metrics['cv']:.2f}). Values: {metrics['values']}. How should I set the final value?"
            )
            wfo_logger.info(f"Chat model suggestion for unstable parameter '{param_name}': {suggestion}")
        
        # Use median for more stable values
        if metrics['cv'] < 0.3:
            final_params[param_name] = np.median(metrics['values'])
    
    return final_params

def save_final_parameters(params):
    """Save the final recommended parameters to a file."""
    import json
    import os
    
    # Create directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save parameters as JSON
    output_file = f'output/wfo_final_params_{SYMBOL}_{GRANULARITY_STR}.json'
    with open(output_file, 'w') as f:
        json.dump(params, f, indent=4)
    
    wfo_logger.info(f"Final parameters saved to {output_file}")

def generate_wfo_report(train_portfolios, oos_portfolios, all_parameters):
    """Generate a detailed HTML report of the WFO results."""
    wfo_logger.info("Generating detailed WFO report...")
    
    try:
        import os
        from datetime import datetime
        
        # Create directory if it doesn't exist
        report_dir = 'reports'
        os.makedirs(report_dir, exist_ok=True)
        
        # Generate report filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'{report_dir}/wfo_report_{SYMBOL}_{GRANULARITY_STR}_{timestamp}.html'
        
        # Generate HTML report content
        # This would normally use a template engine or HTML generation library
        # Simplified version for demonstration
        html_content = f"""
        <html>
        <head>
            <title>WFO Report - {SYMBOL} {GRANULARITY_STR}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .summary {{ background-color: #e9f7ef; padding: 15px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>Walk-Forward Optimization Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Symbol: {SYMBOL}</p>
                <p>Timeframe: {GRANULARITY_STR}</p>
                <p>Date Range: {WFO_START_DATE} to {WFO_END_DATE}</p>
                <p>Splits Processed: {len(oos_portfolios)}/{len(train_portfolios)}</p>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <!-- Performance metrics would be added here -->
            
            <!-- Parameter stability analysis would be added here -->
            
            <!-- Charts would be added here -->
        </body>
        </html>
        """
        
        # Write report to file
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        wfo_logger.info(f"WFO report generated: {report_file}")
        
    except Exception as e:
        wfo_logger.error(f"Error generating WFO report: {str(e)}")

def calculate_average_metrics(portfolios):
    """Calculate average performance metrics across multiple portfolios."""
    if not portfolios:
        return {}
        
    # Get metrics for each portfolio
    all_metrics = [calculate_performance_metrics(pf) for pf in portfolios]
    
    # Average the metrics
    avg_metrics = {}
    for metric in all_metrics[0].keys():
        values = [m.get(metric, 0) for m in all_metrics]
        avg_metrics[metric] = sum(values) / len(values)
    
    return avg_metrics

# --- Data Loading and Preparation ---
def load_data(symbol, timeframe='1d', lookback_days=365):
    """
    Load market data for the specified symbol and timeframe with improved error handling.
    
    Args:
        symbol (str): Trading symbol (e.g. 'BTC/USD')
        timeframe (str): Chart timeframe (e.g. '1d', '4h', '1h')
        lookback_days (int): Number of days of historical data to load
        
    Returns:
        dict: Dictionary with OHLCV data and derived indicators
    """
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        import vectorbtpro as vbt
        
        logging.info(f"Loading data for {symbol} ({timeframe}) with {lookback_days} days lookback")
        
        # Set date range with a buffer to ensure sufficient data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=int(lookback_days * 1.2))  # Add 20% buffer for data
        
        original_start_date = start_date
        original_symbol = symbol
        data = {}
        data_loaded = False
        
        # Try primary data source
        try:
            # Try to load from vectorbtpro data module
            logging.info(f"Attempting to load data from YFData for {symbol} from {start_date} to {end_date}")
            symbol_formatted = symbol.replace('/', '-')
            ohlcv = vbt.YFData.download(
                symbol_formatted, 
                start=start_date,
                end=end_date,
                timeframe=timeframe
            ).get()
            
            # Validate the data
            if ohlcv is not None and not ohlcv.empty and len(ohlcv) > 50:  # Minimum data requirement
                # Extract OHLCV columns
                data['open'] = ohlcv['Open']
                data['high'] = ohlcv['High']
                data['low'] = ohlcv['Low']
                data['close'] = ohlcv['Close']
                data['volume'] = ohlcv['Volume']
                data_loaded = True
                logging.info(f"Successfully loaded {len(ohlcv)} bars from YFData")
            else:
                logging.warning(f"Data from YFData was empty or insufficient: {len(ohlcv) if ohlcv is not None else 'None'} bars")
            
        except Exception as e:
            logging.warning(f"Failed to load data from YFData: {e}")
        
        # Try alternative data sources if primary failed
        if not data_loaded:
            # Try alternative symbols
            alternative_symbols = [
                symbol.replace('/', '-'),   # Try BTC-USD format
                symbol.replace('/', ''),    # Try BTCUSD format
                symbol.replace('/USD', '/USDT')  # Try USDT pair instead
            ]
            
            for alt_symbol in alternative_symbols:
                if data_loaded:
                    break
                    
                try:
                    logging.info(f"Trying alternative symbol: {alt_symbol}")
                    ohlcv = vbt.YFData.download(
                        alt_symbol, 
                        start=start_date,
                        end=end_date,
                        timeframe=timeframe
                    ).get()
                    
                    if ohlcv is not None and not ohlcv.empty and len(ohlcv) > 50:
                        data['open'] = ohlcv['Open']
                        data['high'] = ohlcv['High']
                        data['low'] = ohlcv['Low']
                        data['close'] = ohlcv['Close']
                        data['volume'] = ohlcv['Volume']
                        data_loaded = True
                        logging.info(f"Successfully loaded {len(ohlcv)} bars using alternative symbol {alt_symbol}")
                except Exception as alt_err:
                    logging.warning(f"Failed to load data for alternative symbol {alt_symbol}: {alt_err}")
            
            # Try to load from CSV if available
            if not data_loaded:
                try:
                    csv_paths = [
                        f"data/{symbol.replace('/', '_')}_{timeframe}.csv",
                        f"data/{symbol.replace('/', '-')}_{timeframe}.csv",
                        f"data/{symbol.replace('/', '')}_{timeframe}.csv"
                    ]
                    
                    for csv_path in csv_paths:
                        try:
                            logging.info(f"Attempting to load from CSV: {csv_path}")
                            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
                            
                            # Validate CSV data
                            if df is not None and not df.empty and len(df) > 50:
                                # Extract OHLCV columns
                                data['open'] = df['open'] if 'open' in df.columns else df['Open']
                                data['high'] = df['high'] if 'high' in df.columns else df['High']
                                data['low'] = df['low'] if 'low' in df.columns else df['Low']
                                data['close'] = df['close'] if 'close' in df.columns else df['Close']
                                
                                # Handle volume column which might be missing
                                if 'volume' in df.columns:
                                    data['volume'] = df['volume']
                                elif 'Volume' in df.columns:
                                    data['volume'] = df['Volume']
                                else:
                                    # Generate synthetic volume
                                    data['volume'] = pd.Series(np.ones(len(df)), index=df.index)
                                
                                data_loaded = True
                                logging.info(f"Successfully loaded {len(df)} bars from CSV: {csv_path}")
                                break
                        except Exception as csv_path_err:
                            logging.warning(f"Failed to load from CSV path {csv_path}: {csv_path_err}")
                    
                except Exception as csv_err:
                    logging.error(f"Failed to load from all CSV options: {csv_err}")
        
        # Generate mock data as last resort
        if not data_loaded:
            logging.warning("All data loading attempts failed. Generating mock data for testing.")
            
            # Add more realistic values for mock data to better simulate real market behavior
            dates = pd.date_range(start=start_date, end=end_date, freq=timeframe)
            n_bars = len(dates)
            
            if n_bars < 100:
                logging.warning(f"Not enough bars ({n_bars}) in date range. Expanding range.")
                start_date = end_date - timedelta(days=lookback_days * 2)  # Double the lookback period
                dates = pd.date_range(start=start_date, end=end_date, freq=timeframe)
                n_bars = len(dates)
            
            # Generate synthetic price data with realistic properties
            np.random.seed(42)  # For reproducibility
            
            # Set base values according to the asset being simulated
            if 'btc' in symbol.lower():
                start_price = 50000.0
                daily_returns = np.random.normal(0.0005, 0.03, n_bars)  
            elif 'eth' in symbol.lower():
                start_price = 3000.0
                daily_returns = np.random.normal(0.0006, 0.04, n_bars)
            else:
                start_price = 100.0
                daily_returns = np.random.normal(0.0003, 0.02, n_bars)
            
            # Generate close prices with momentum effect
            momentum = np.cumsum(np.random.normal(0, 0.005, n_bars))  # Add gradual trends
            close_prices = start_price * (1 + daily_returns + momentum * 0.01).cumprod()
            
            # Generate other OHLCV data with realistic relationships
            high_ratio = 1 + np.abs(np.random.normal(0, 0.015, n_bars))  # High is 0-3% above close
            low_ratio = 1 - np.abs(np.random.normal(0, 0.015, n_bars))   # Low is 0-3% below close
            
            # Add volatility clustering to make price movements more realistic
            volatility = np.abs(np.random.normal(0, 0.01, n_bars))
            for i in range(1, len(volatility)):
                volatility[i] = 0.9 * volatility[i-1] + 0.1 * volatility[i]
            
            # Create OHLCV data
            data['close'] = pd.Series(close_prices, index=dates)
            data['high'] = pd.Series(close_prices * (1 + volatility * high_ratio), index=dates)
            data['low'] = pd.Series(close_prices * (1 - volatility * low_ratio), index=dates)
            data['open'] = pd.Series((data['high'] + data['low']) / 2, index=dates)
            
            # Generate volume with higher volume on larger price movements
            normalized_returns = np.abs(daily_returns) / np.std(daily_returns)
            volume_base = np.random.lognormal(15, 1, n_bars)
            volume_adjusted = volume_base * (1 + normalized_returns)
            data['volume'] = pd.Series(volume_adjusted, index=dates)
            
            logging.info(f"Generated {n_bars} bars of mock data from {dates[0]} to {dates[-1]}")
            data_loaded = True
        
        # Calculate basic indicators
        logging.info("Calculating indicators")
        
        # Ensure no NaN values in price data
        for key in ['open', 'high', 'low', 'close']:
            if key in data:
                # Forward fill, then backward fill to handle any NaNs
                data[key] = data[key].fillna(method='ffill').fillna(method='bfill')
        
        # RSI
        data['rsi'] = vbt.RSI.run(data['close']).rsi
        
        # Bollinger Bands - check for different class names based on vectorbtpro version
        try:
            # Try BBands (newer versions)
            bb = vbt.BBands.run(data['close'])
            data['bb_middle'] = bb.middle
            data['bb_upper'] = bb.upper
            data['bb_lower'] = bb.lower
        except AttributeError:
            try:
                # Try BBANDS (older versions)
                bb = vbt.BBANDS.run(data['close'])
                data['bb_middle'] = bb.middle
                data['bb_upper'] = bb.upper
                data['bb_lower'] = bb.lower
            except AttributeError:
                # Last resort, calculate manually
                logging.warning("Bollinger Bands indicators not found, calculating manually")
                window = 20
                rolling_mean = data['close'].rolling(window=window).mean()
                rolling_std = data['close'].rolling(window=window).std()
                data['bb_middle'] = rolling_mean
                data['bb_upper'] = rolling_mean + (rolling_std * 2)
                data['bb_lower'] = rolling_mean - (rolling_std * 2)
        
        # Volatility (ATR)
        try:
            data['atr'] = vbt.ATR.run(data['high'], data['low'], data['close']).atr
            data['atr_pct'] = data['atr'] / data['close'] * 100  # ATR as percentage of price
        except AttributeError:
            # Calculate manually if not available
            logging.warning("ATR indicator not found, calculating manually")
            window = 14
            tr1 = abs(data['high'] - data['low'])
            tr2 = abs(data['high'] - data['close'].shift())
            tr3 = abs(data['low'] - data['close'].shift())
            tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
            data['atr'] = tr.rolling(window=window).mean()
            data['atr_pct'] = data['atr'] / data['close'] * 100
        
        # Price momentum
        data['returns'] = data['close'].pct_change()
        data['rolling_vol'] = data['returns'].rolling(window=20).std() * np.sqrt(252)  # Annualized vol
        
        # Log data summary
        start_date_str = data['close'].index[0].strftime('%Y-%m-%d')
        end_date_str = data['close'].index[-1].strftime('%Y-%m-%d')
        logging.info(f"Loaded {len(data['close'])} bars from {start_date_str} to {end_date_str}")
        logging.info(f"Price range: {data['close'].min():.2f} to {data['close'].max():.2f}")
        
        return data

    except Exception as e:
        logging.error(f"Error loading market data: {e}")
        if chat_model_available():
            context = {"error_location": "load_market_data"}
            debug_with_chat(e, "Error when loading market data", context)
        return None


def create_wfo_splits(data, num_splits, train_size):
    """
    Create walk-forward optimization splits with improved handling to prevent overlaps.
    
    Args:
        data: DataFrame or dict with OHLCV data
        num_splits: Number of splits to create
        train_size: Size of training set as fraction of split
        
    Returns:
        List of tuples (train_data, test_data)
    """
    import numpy as np
    import pandas as pd
    
    # Get reference series for splitting (using close price)
    if isinstance(data, pd.DataFrame):
        series = data['close'] if 'close' in data.columns else data.iloc[:, 0]
    else:
        series = data['close']
        
    total_rows = len(series)
    logging.info(f"Creating {num_splits} WFO splits with training size of {train_size*100:.0f}%")
    
    # Calculate rows per split to ensure no overlap
    split_size = total_rows // num_splits
    
    # Ensure minimum data size requirements are met
    if split_size < 90:  # Minimum 90 days per split as a rule of thumb
        logging.warning(f"Split size too small: {split_size} days. Consider reducing num_splits or using more data.")
        # Adjust to fewer splits if needed
        original_splits = num_splits
        num_splits = max(2, total_rows // 90)
        split_size = total_rows // num_splits
        logging.warning(f"Adjusted splits from {original_splits} to {num_splits} to ensure at least 90 days per split")
    
    # Calculate train and test sizes
    train_days = int(split_size * train_size)
    test_days = split_size - train_days
    
    logging.info(f"Each split: {split_size} days (Train: {train_days}, Test: {test_days})")
    
    splits = []
    for i in range(num_splits):
        # Calculate split boundaries
        start_idx = i * split_size
        train_end_idx = start_idx + train_days
        test_end_idx = min(train_end_idx + test_days, total_rows)
        
        # Handle last split potentially being smaller
        if i == num_splits - 1:
            test_end_idx = total_rows
            
        # Log split details
        logging.info(f"Split {i+1}: Train [{start_idx}:{train_end_idx}], Test [{train_end_idx}:{test_end_idx}]")
            
        # Extract train and test data
        if isinstance(data, pd.DataFrame):
            train_data = data.iloc[start_idx:train_end_idx].copy()
            test_data = data.iloc[train_end_idx:test_end_idx].copy()
        else:
            # For dict of Series
            train_data = {}
            test_data = {}
            for key, series in data.items():
                train_data[key] = series.iloc[start_idx:train_end_idx].copy()
                test_data[key] = series.iloc[train_end_idx:test_end_idx].copy()
        
        splits.append((train_data, test_data))
        
    # Verify splits
    for i, (train, test) in enumerate(splits):
        if isinstance(train, pd.DataFrame):
            train_size = len(train)
            test_size = len(test)
        else:
            train_size = len(list(train.values())[0])
            test_size = len(list(test.values())[0])
            
        logging.info(f"Split {i+1} sizes - Training: {train_size}, Testing: {test_size}")
    
    return splits

def calculate_target_amount(close, entries, sl_pct, risk_per_trade, init_cash):
    """
    Calculate position size based on risk parameters.
    
    Args:
        close (pd.Series): Close price series
        entries (pd.Series): Boolean series indicating entry points
        sl_pct (float): Stop loss percentage as a decimal (e.g., 0.02 for 2%)
        risk_per_trade (float): Fraction of capital to risk per trade (e.g., 0.01 for 1%)
        init_cash (float): Initial capital
        
    Returns:
        pd.Series: Position sizes at each entry point
    """
    # Create a Series of zeros with the same index as close
    amount = pd.Series(0.0, index=close.index)
    
    # For each entry point, calculate the position size
    entry_indices = entries[entries].index
    
    for idx in entry_indices:
        # Get entry price
        entry_price = close[idx]
        
        # Calculate risk amount in dollars
        risk_amount = init_cash * risk_per_trade
        
        # Calculate max loss per unit
        max_loss_per_unit = entry_price * sl_pct
        
        # Calculate units to trade
        if max_loss_per_unit > 0:
            units = risk_amount / max_loss_per_unit
        else:
            units = 0
            
        # Set the amount at this entry point
        amount[idx] = units
    
    return amount

# =============================================================================
# Main Execution Block
# =============================================================================
if __name__ == "__main__":
    wfo_logger.info("Executing WFO script...")
    try:
        # Enable vectorbtpro caching if configured
        if ENABLE_CACHING:
            wfo_logger.info("Enabling VectorBT Pro caching for faster calculations")
            try:
                # Use the simplest caching option
                if hasattr(vbt, 'settings'):
                    if hasattr(vbt.settings, 'set_option'):
                        vbt.settings.set_option('caching', True)
                    elif hasattr(vbt.settings, 'caching'):
                        if not isinstance(vbt.settings.caching, dict):
                            vbt.settings.caching = True
            except Exception as cache_err:
                wfo_logger.warning(f"Could not enable VectorBT Pro caching: {cache_err}")
        
        # Set debug verbosity
        if not VERBOSE_DEBUG:
            wfo_logger.info("Setting lower verbosity for production run")
            wfo_logger.setLevel(logging.INFO)
        
        run_walk_forward_optimization()
        wfo_logger.info("Script execution completed successfully.")
    except Exception as main_err:
        wfo_logger.critical(f"Script failed with error: {main_err}")
        # Optionally exit with error code
        sys.exit(1) 

def initialize_chat_model():
    """Initialize the chat model for the strategy.
    
    This function attempts to initialize the chat model using vectorbtpro.
    If successful, it will return the chat model instance.
    If unsuccessful, it will return None.
    
    Returns:
        object: The chat model instance if successful, None otherwise.
    """
    try:
        # Just use the get_chat_model function
        chat_model = get_chat_model()
        if chat_model:
            wfo_logger.info("Successfully initialized chat model.")
            return chat_model
        else:
            wfo_logger.warning("Failed to initialize chat model.")
            return None
    except Exception as e:
        wfo_logger.error(f"Failed to initialize chat model: {e}", exc_info=True)
        return None

def debug_with_chat(error_message, context_data=None):
    """Use the chat provider to debug an error with additional context"""
    try:
        # Only use if we have a chat provider configured
        if not hasattr(debug_with_chat, "chat_fn"):
            # Try to create a chat function if we haven't already
            chat_fn = setup_chat_provider()
            if chat_fn:
                debug_with_chat.chat_fn = chat_fn
            else:
                logging.warning("No chat provider available for debugging")
                return f"Debugging failed: {error_message}"
        
        # Create a debugging prompt with error context
        prompt = f"""
        I'm encountering an error in my cryptocurrency trading strategy optimization:
        
        ERROR: {error_message}
        
        Additional context:
        {json.dumps(context_data, indent=2) if context_data else 'No additional context provided'}
        
        Please help me understand what might be causing this issue and suggest potential solutions.
        """
        
        # Send to chat provider and get response
        response = debug_with_chat.chat_fn(prompt)
        logging.info(f"AI debugging suggestion: {response.strip()}")
        return response
    except Exception as e:
        logging.error(f"Error in debug_with_chat: {str(e)}")
        return f"Debugging failed: {error_message}"

def handle_portfolio_error(error, params):
    """Handle errors that occur during portfolio creation.
    
    Args:
        error (Exception): The error that occurred.
        params (dict): The parameters that were used for portfolio creation.
    
    Returns:
        str: Debugging advice for the portfolio error.
    """
    # Get specific context for portfolio creation errors
    context = "Error occurred during portfolio creation. "
    
    # Add more context based on common portfolio errors
    if "truth value of a Series is ambiguous" in str(error):
        context += (
            "This is likely due to a boolean operation on a pandas Series. "
            "Check entry/exit condition calculations and ensure proper boolean operations."
        )
    elif "cannot reindex from a duplicate axis" in str(error):
        context += "This may be due to duplicate index values in the data."
    elif "Input contains NaN" in str(error):
        context += "Check for NaN values in price data or signal generation."
    
    # Get debugging advice using the chat model
    return debug_with_chat(error, context=context, params=params) 

# --- Create portfolios with modified signal generation ---
def create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL):
    """
    Create portfolio for specified parameters.
    
    Args:
        data: DataFrame containing OHLCV data and indicators
        params: Dictionary of strategy parameters
        init_cash: Initial capital
        
    Returns:
        Portfolio object or None if creation fails
    """
    try:
        import pandas as pd
        
        # Handle different data types
        if isinstance(data, pd.DataFrame):
            # Make a copy to avoid modifying the original
            df = data.copy()
            
            # Ensure column names are standardized to lowercase
            df.columns = [col.lower() for col in df.columns]
            
            # Check if we have all required columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in required_cols:
                if col not in df.columns:
                    # Try to find a case-insensitive match
                    matching_cols = [c for c in df.columns if c.lower() == col.lower()]
                    if matching_cols:
                        df[col] = df[matching_cols[0]]
                    else:
                        logging.error(f"Required column {col} not found. Available columns: {df.columns.tolist()}")
                        return None
        elif isinstance(data, dict):
            # For dictionary data, create a DataFrame with standardized column names
            df = {}
            column_map = {
                'open': ['open', 'Open', 'OPEN'],
                'high': ['high', 'High', 'HIGH'],
                'low': ['low', 'Low', 'LOW'],
                'close': ['close', 'Close', 'CLOSE'],
                'volume': ['volume', 'Volume', 'VOLUME']
            }
            
            # Try to find matching columns
            for std_col, variants in column_map.items():
                found = False
                for variant in variants:
                    if variant in data:
                        df[std_col] = data[variant]
                        found = True
                        break
                
                if not found:
                    logging.error(f"Required column {std_col} not found in data dictionary")
                    return None
            
            # Include any additional indicators from the data dictionary
            for key, value in data.items():
                if key.lower() not in ['open', 'high', 'low', 'close', 'volume']:
                    df[key.lower()] = value
        else:
            logging.error(f"Unsupported data type: {type(data)}")
            return None
        
        # Use our standardized create_portfolio function
        portfolio, success = create_portfolio(df, params)
        
        if not success or portfolio is None:
            logging.error(f"Failed to create portfolio with params: {params}")
            return None
            
        return portfolio
        
    except Exception as e:
        logging.error(f"Error creating portfolio: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        return None

# Fix the progress callback function to accept the study and trial parameters
def progress_callback(study, trial=None):
    """Callback function for Optuna to track optimization progress"""
    logging.info(f"Completed {len(study.trials)} trials so far")
    if len(study.trials) % 10 == 0:
        best_trial = study.best_trial
        if best_trial.value != float('-inf'):
            logging.info(f"Best value so far: {best_trial.value} with params: {best_trial.params}")
        else:
            logging.warning("No valid portfolio found yet")
            
    # Return true to continue optimization
    return True

def evaluate_portfolio(portfolio):
    """
    Calculate performance metrics for a portfolio.
    
    Args:
        portfolio: The portfolio object with trades data
        
    Returns:
        dict: Performance metrics
    """
    import numpy as np
    
    metrics = {}
    
    try:
        # Basic metrics
        metrics['total_return'] = portfolio.total_return()
        metrics['max_drawdown'] = portfolio.max_drawdown()
        
        # Trading metrics
        trades = portfolio.trades
        if trades is not None and len(trades) > 0:
            metrics['total_trades'] = len(trades)
            winning_trades = trades[trades.pnl > 0]
            losing_trades = trades[trades.pnl <= 0]
            metrics['winning_trades'] = len(winning_trades)
            metrics['losing_trades'] = len(losing_trades)
            
            # Win rate
            metrics['win_rate'] = len(winning_trades) / len(trades) if len(trades) > 0 else 0
            
            # Profit factor
            total_profit = winning_trades.pnl.sum() if len(winning_trades) > 0 else 0
            total_loss = abs(losing_trades.pnl.sum()) if len(losing_trades) > 0 else 0
            metrics['profit_factor'] = total_profit / total_loss if total_loss > 0 else (1.0 if total_profit > 0 else 0.0)
        else:
            # Default values if no trades
            metrics['total_trades'] = 0
            metrics['winning_trades'] = 0
            metrics['losing_trades'] = 0
            metrics['win_rate'] = 0.0
            metrics['profit_factor'] = 0.0
        
        # Risk metrics
        returns = portfolio.returns()
        if returns is not None and len(returns) > 0:
            # Annualized returns (assuming daily data)
            annualized_return = np.mean(returns) * 252
            annualized_vol = np.std(returns) * np.sqrt(252)
            risk_free_rate = 0.02  # 2% risk-free rate assumption
            
            # Sharpe ratio
            metrics['sharpe_ratio'] = (annualized_return - risk_free_rate) / annualized_vol if annualized_vol != 0 else 0
            
            # Sortino ratio (downside risk)
            downside_returns = returns[returns < 0]
            downside_vol = np.std(downside_returns) * np.sqrt(252) if len(downside_returns) > 0 else annualized_vol
            metrics['sortino_ratio'] = (annualized_return - risk_free_rate) / downside_vol if downside_vol != 0 else 0
            
            # Average trade
            if metrics['total_trades'] > 0:
                metrics['avg_trade_pct'] = metrics['total_return'] / metrics['total_trades']
            else:
                metrics['avg_trade_pct'] = 0.0
        else:
            metrics['sharpe_ratio'] = 0.0
            metrics['sortino_ratio'] = 0.0
            metrics['avg_trade_pct'] = 0.0
        
        # Exposure metrics
        if hasattr(portfolio, 'cash') and hasattr(portfolio, 'value'):
            cash_series = portfolio.cash
            value_series = portfolio.value
            
            # Average market exposure
            if len(cash_series) > 0 and len(value_series) > 0:
                exposure = 1 - (cash_series / value_series)
                metrics['avg_exposure'] = np.mean(exposure)
                metrics['max_exposure'] = np.max(exposure)
            else:
                metrics['avg_exposure'] = 0.0
                metrics['max_exposure'] = 0.0
        else:
            metrics['avg_exposure'] = 0.0
            metrics['max_exposure'] = 0.0
        
    except Exception as e:
        logging.error(f"Error calculating metrics: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        
        # Return basic metrics if calculation fails
        if 'total_return' not in metrics:
            metrics['total_return'] = 0.0
        if 'max_drawdown' not in metrics:
            metrics['max_drawdown'] = 0.0
        if 'total_trades' not in metrics:
            metrics['total_trades'] = 0
        if 'win_rate' not in metrics:
            metrics['win_rate'] = 0.0
        if 'sharpe_ratio' not in metrics:
            metrics['sharpe_ratio'] = 0.0
        if 'profit_factor' not in metrics:
            metrics['profit_factor'] = 0.0
    
    return metrics

def create_portfolio(data, params, debug=False):
    """
    Create a portfolio using the edge strategy with the given parameters.
    
    Args:
        data: Market data (DataFrame or dictionary)
        params: Strategy parameters
        debug: Whether to print debug information
        
    Returns:
        tuple: (portfolio, success_flag)
    """
    try:
        # Check if data is valid
        if data is None:
            logging.error("Insufficient data for portfolio creation")
            return None, False
            
        # Convert dictionary to DataFrame if needed
        import pandas as pd
        if isinstance(data, dict):
            # Create DataFrame from dictionary of Series
            df = pd.DataFrame({k: v for k, v in data.items() if isinstance(v, (pd.Series, pd.DataFrame))})
        else:
            # Make a copy to avoid modifying the original
            df = data.copy()
        
        # Ensure all required columns are present and numeric
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        
        # Standardize column names (convert to lowercase)
        df.columns = [col.lower() for col in df.columns]
        
        for col in required_columns:
            if col not in df.columns:
                # Try to find a case-insensitive match
                if isinstance(data, dict) and col.capitalize() in data:
                    df[col] = data[col.capitalize()]
                else:
                    matching_cols = [c for c in df.columns if c.lower() == col.lower()]
                    if matching_cols:
                        df[col] = df[matching_cols[0]]
                    else:
                        logging.error(f"Missing required column: {col}")
                        return None, False
            
            # Convert to numeric and handle any errors
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for NaN values
        if df[required_columns].isna().any().any():
            logging.warning("Data contains NaN values. Filling with forward fill method.")
            df[required_columns] = df[required_columns].fillna(method='ffill')
            # After filling, check again for any remaining NaNs
            if df[required_columns].isna().any().any():
                logging.error("Data still contains NaN values after filling")
                return None, False
        
        # Apply edge strategy with parameters
        from scripts.strategies.edge_strategy import EdgeMultiFactorStrategy
        
        # Convert parameters to appropriate types if needed
        strategy_params = params.copy()
        
        # Create the strategy
        strategy = EdgeMultiFactorStrategy(df, **strategy_params)
        
        # Run the strategy to get entry/exit signals
        entry_signals, exit_signals = strategy.generate_signals()
        
        # Check if any signals were generated
        if entry_signals.sum() == 0:
            logging.warning(f"No entry signals generated with parameters: {params}")
            return None, False
            
        # Create portfolio from signals
        portfolio = strategy.backtest_signals(entry_signals, exit_signals)
        
        # Debug info if requested
        if debug:
            metrics = evaluate_portfolio(portfolio)
            logging.debug(f"Portfolio metrics: {metrics}")
            
        return portfolio, True
        
    except Exception as e:
        logging.error(f"Error creating portfolio: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        return None, False