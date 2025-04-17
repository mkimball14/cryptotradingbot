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


def create_pf_for_params(data, params, init_cash=100000):
    """Create portfolio for given parameters."""
    try:
        # Extract parameters
        rsi_window = params['rsi_window']
        rsi_entry = params['rsi_entry']
        rsi_exit = params['rsi_exit']
        bb_window = params['bb_window']
        bb_dev = params['bb_dev']
        vol_window = params['vol_window']
        vol_threshold = params['vol_threshold']
        sl_pct = params['sl_pct']
        tp_pct = params['tp_pct']
        risk_per_trade = params['risk_per_trade']
        
        # Make sure data is a DataFrame, not a dict
        if isinstance(data, dict):
            # If data is a dict of DataFrames, we need to structure it properly
            price_data = data.get('close', None)
            if price_data is None:
                logging.error("No 'close' price data available in the data dictionary")
                return None
        else:
            # Assuming data is already a DataFrame
            price_data = data
        
        # Log data info
        logging.debug(f"Price data: {len(price_data)} points from {price_data.index[0]} to {price_data.index[-1]}")
        
        # Generate entry signals
        rsi = vbt.RSI.run(price_data, window=rsi_window)
        
        # Use try/except to handle different versions of vectorbtpro
        try:
            # Try BBands (newer versions)
            bb = vbt.BBands.run(price_data, window=bb_window, alpha=bb_dev)
        except AttributeError:
            try:
                # Try BBANDS (older versions)
                bb = vbt.BBANDS.run(price_data, window=bb_window, alpha=bb_dev)
            except AttributeError:
                # Last resort, calculate manually
                logging.warning("Bollinger Bands indicators not found, calculating manually")
                bb_middle = price_data.rolling(window=bb_window).mean()
                bb_std = price_data.rolling(window=bb_window).std()
                bb_upper = bb_middle + (bb_std * bb_dev)
                bb_lower = bb_middle - (bb_std * bb_dev)
                # Create a compatible result object
                from types import SimpleNamespace
                bb = SimpleNamespace(
                    middle=bb_middle,
                    upper=bb_upper,
                    lower=bb_lower
                )
        
        # Calculate volume signals
        vol_zscore = None
        if 'volume' in data:
            volume = data['volume']
            # Safe handling of standard deviation calculation
            rolling_vol = volume.rolling(window=vol_window)
            vol_mean = rolling_vol.mean()
            vol_std = rolling_vol.std()
            # Handle zero standard deviation
            safe_std = vol_std.replace(0, 1)
            vol_zscore = (volume - vol_mean) / safe_std
            is_vol_high = vol_zscore > vol_threshold
        else:
            # If no volume data, assume all are valid
            is_vol_high = pd.Series(True, index=price_data.index)
        
        # Generate entry and exit signals - MORE FLEXIBLE CONDITIONS
        # RSI condition
        rsi_condition = rsi.rsi < rsi_entry
        
        # BB condition
        bb_condition = price_data < bb.lower
        
        # More flexible entry criteria - either RSI & BB conditions together, or very low RSI
        entries = ((rsi_condition & bb_condition) | 
                  (rsi.rsi < (rsi_entry - 5)))  # Also trigger on very low RSI
        
        # Apply volume filter only if there are some entry signals
        if entries.sum() > 0 and 'volume' in data:
            # Make volume filter less restrictive - only apply if it doesn't eliminate all signals
            entries_with_vol = entries & is_vol_high
            if entries_with_vol.sum() > 0:
                entries = entries_with_vol
            else:
                logging.debug(f"Volume filter would eliminate all {entries.sum()} signals, keeping original signals")
        
        # Exit logic - more permissive
        exits = (rsi.rsi > rsi_exit) | (price_data > bb.middle * 0.98)  # Exit near middle band
        
        # Ensure entries and exits are boolean Series
        entries = entries.astype(bool)
        exits = exits.astype(bool)
        
        # Log signal counts
        logging.debug(f"Generated {entries.sum()} entry signals and {exits.sum()} exit signals")
        
        # Check if we have entry signals
        if entries.sum() == 0:
            logging.warning(f"No entry signals generated with parameters: {params}")
            # Additional diagnostics to understand why
            logging.debug(f"RSI condition met {rsi_condition.sum()} times")
            logging.debug(f"BB condition met {bb_condition.sum()} times")
            logging.debug(f"Very low RSI condition met {(rsi.rsi < (rsi_entry - 5)).sum()} times")
            if 'volume' in data:
                logging.debug(f"Volume condition met {is_vol_high.sum()} times") 
            return None
        
        # Calculate stop-loss and take-profit levels
        sl_stop = sl_pct / 100
        tp_stop = tp_pct / 100
        tsl_stop = None  # Not using trailing stop for now
        
        # Calculate position size based on risk
        target_amount = calculate_target_amount(
            price_data, 
            entries,
            sl_stop,
            risk_per_trade,
            init_cash
        )
        
        # Log parameters being used
        logging.info(f"Creating portfolio with params: {params}")
        
        # Create portfolio
        pf = vbt.Portfolio.from_signals(
            price_data,
            entries,
            exits,
            sl_stop=sl_stop,
            tp_stop=tp_stop,
            tsl_stop=tsl_stop,
            size=target_amount,
            init_cash=init_cash,
            fees=0.001,
            slippage=0.001,
            freq='1D'
        )
        
        return pf

    except Exception as e:
        logging.error(f"Portfolio creation error: {str(e)}")
        error_context = inspect.getsource(create_pf_for_params)
        debug_suggestion = debug_with_chat(e, error_context, params)
        logging.debug(f"Debug suggestion: {debug_suggestion}")
        return None


# =============================================================================
# Parallel Optimization Functions
# =============================================================================
def evaluate_params(trial_params, data, split_data=None):
    """
    Evaluate a single parameter set for parallel processing.
    
    Args:
        trial_params: Dictionary of parameters to evaluate
        data: Data to backtest on
        split_data: If provided, uses this data instead of the full dataset
        
    Returns:
        float: Performance metric value or -inf if invalid
    """
    try:
        # Use split data if provided
        eval_data = split_data if split_data is not None else data
        
        # Create portfolio using these parameters
        pf = create_pf_for_params(eval_data, trial_params)
        
        if pf is None:
            logging.warning(f"No entry signals generated with parameters: {', '.join([f'{k}={v}' for k, v in trial_params.items()])}")
            return float('-inf')
        
        # Calculate performance metric
        sharpe = pf.stats().get('sharpe_ratio', np.nan)
        if not np.isfinite(sharpe) or sharpe <= 0:
            return float('-inf')
            
        return sharpe
    except Exception as e:
        logging.warning(f"Parameter evaluation failed: {str(e)}")
        return float('-inf')


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
    Optimize strategy parameters using efficient parameter search.
    
    Args:
        data (dict): Dictionary containing OHLCV data
        params_space (dict): Parameter space to search
        n_trials (int): Number of optimization trials
        progress_callback (callable, optional): Callback for reporting progress
        
    Returns:
        tuple: (best_params, all_results)
    """
    import optuna
    from concurrent.futures import ProcessPoolExecutor
    import numpy as np
    import warnings
    
    # Suppress warnings during optimization
    warnings.filterwarnings('ignore', category=FutureWarning)
    
    logging.info(f"Starting parameter optimization with {n_trials} trials")
    
    # Initialize results storage
    all_results = []
    
    # Create Optuna study
    study = optuna.create_study(direction='maximize')
    
    def objective(trial):
        # Sample parameters from parameter space
        current_params = {}
        for param_name, param_range in params_space.items():
            if isinstance(param_range, tuple) and len(param_range) == 3:
                param_type = type(param_range[0])
                if param_type == int:
                    current_params[param_name] = trial.suggest_int(param_name, param_range[0], param_range[1], step=param_range[2])
                elif param_type == float:
                    current_params[param_name] = trial.suggest_float(param_name, param_range[0], param_range[1], step=param_range[2])
            elif isinstance(param_range, list):
                current_params[param_name] = trial.suggest_categorical(param_name, param_range)
        
        # Create portfolio with current parameters
        try:
            portfolio = create_pf_for_params(data, current_params)
            
            # Calculate objective metric (Sharpe ratio or custom metric)
            if portfolio is None:
                return float('-inf')
            
            # Get key performance metrics
            sharpe = portfolio.stats().get('sharpe_ratio', np.nan)
            if np.isnan(sharpe) or np.isinf(sharpe):
                return float('-inf')
                
            # Calculate profit factor as another metric
            stats = portfolio.stats()
            total_profit = stats.get('total_profit', 0)
            gross_profit = stats.get('gross_profit', 0)
            gross_loss = abs(stats.get('gross_loss', 0))
            
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            # Calculate custom score
            score = sharpe
            if profit_factor > 1.5:  # Bonus for good profit factor
                score *= 1.2
                
            # Store results
            result = {
                'params': current_params,
                'sharpe': sharpe,
                'profit_factor': profit_factor,
                'total_profit': total_profit,
                'score': score
            }
            all_results.append(result)
            
            return score
            
        except Exception as e:
            logging.warning(f"Parameter evaluation failed: {e}")
            return float('-inf')
    
    # Use parallel processing with ThreadPoolExecutor
    try:
        logging.info("Running optimization with parallel processing")
        study.optimize(objective, n_trials=n_trials, n_jobs=-1, show_progress_bar=True)
    except Exception as e:
        logging.error(f"Parallel optimization failed: {e}")
        logging.info("Falling back to sequential optimization")
        # Fall back to sequential processing
        study.optimize(objective, n_trials=n_trials)
    
    # Get best parameters
    if study.best_params and len(all_results) > 0:
        # Sort results by score
        sorted_results = sorted(all_results, key=lambda x: x.get('score', float('-inf')), reverse=True)
        best_params = sorted_results[0]['params']
        
        # Log best parameters
        logging.info(f"Optimization complete. Best parameters: {best_params}")
        logging.info(f"Best Sharpe: {sorted_results[0].get('sharpe', 'N/A')}")
        logging.info(f"Best profit factor: {sorted_results[0].get('profit_factor', 'N/A')}")
        
        # Return best parameters and all results
        return best_params, sorted_results
    else:
        if chat_model_available():
            chat_msg = "Optimization failed to find valid parameters. Suggestions for improving parameter search?"
            response = ask_chat_model(chat_msg)
            logging.info(f"Chat model suggestion: {response}")
        
        logging.warning("No valid parameters found during optimization")
        return None, all_results

def run_walk_forward_optimization():
    """
    Run the walk-forward optimization process for the edge strategy.
    Uses the vectorbtpro chat model for debugging when available.
    """
    init_logging()
    
    # --- Configure Chat Provider --- Call the new setup function
    chat_configured = setup_chat_provider()
    if not chat_configured:
        wfo_logger.warning("Chat provider setup failed, continuing without chat features.")

    # Define parameter space for optimization
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
    
    # Check if chat model is available
    if chat_model_available():
        logging.info("Chat model initialized successfully")
        # Ask for optimization suggestions
        query = "What parameter ranges should I focus on for optimizing a crypto trading strategy using RSI and Bollinger Bands?"
        suggestions = ask_chat_model(query)
        logging.info(f"Chat model suggestions: {suggestions}")
    else:
        logging.warning("Chat model not available, continuing without it")
    
    try:
        # Load data
        symbol = "BTC/USD"
        data = load_data(symbol)
        
        if data is None:
            logging.error("Failed to load data for walk-forward optimization")
            return
            
        # Additional data validation after successful loading
        close_series = data.get('close', None)
        if close_series is None or len(close_series) < 100:
            logging.error(f"Insufficient data length: {len(close_series) if close_series is not None else 'No close data'}")
            return

        # Check for NaN values
        nan_count = close_series.isna().sum()
        if nan_count > 0:
            logging.warning(f"Data contains {nan_count} NaN values. Filling with forward fill method.")
            for key in ['open', 'high', 'low', 'close']:
                if key in data:
                    data[key] = data[key].fillna(method='ffill').fillna(method='bfill')
        
        # Configure walk-forward optimization
        num_splits = 3
        train_size = 0.7
        
        # Create splits
        splits = create_wfo_splits(data, num_splits, train_size)
        
        # Storage for OOS portfolios
        oos_portfolios = []
        
        # Process each split
        for i, (train_data, test_data) in enumerate(splits):
            split_num = i + 1
            logging.info(f"Processing split {split_num}/{num_splits}")
            
            # Define progress callback
            def progress_callback(progress):
                logging.info(f"Split {split_num} Train Opt: {int(progress * 100)}%")
            
            # Optimize parameters on training data
            best_params, all_results = optimize_parameters(
                data=train_data,
                params_space=PARAM_GRID,
                n_trials=50,
                progress_callback=progress_callback
            )
            
            # Apply best parameters to test data
            if best_params:
                logging.info(f"Applying best parameters to OOS data: {best_params}")
                oos_pf = create_pf_for_params(test_data, best_params)
                
                if oos_pf is not None:
                    oos_portfolios.append((oos_pf, best_params, split_num))
                    
                    # Log OOS performance
                    stats = oos_pf.stats()
                    sharpe = stats.get('sharpe_ratio', 0)
                    total_return = stats.get('total_return', 0)
                    max_dd = stats.get('max_drawdown', 0)
                    trades = stats.get('total_trades', 0)
                    
                    logging.info(f"OOS metrics - Split {split_num}")
                    logging.info(f"  Sharpe: {sharpe:.2f}")
                    logging.info(f"  Return: {total_return:.2%}")
                    logging.info(f"  Max DD: {max_dd:.2%}")
                    logging.info(f"  Trades: {trades}")
                else:
                    logging.critical(f"Failed to create OOS portfolio for split {split_num}")
            else:
                logging.critical(f"No valid parameters found for split {split_num}, skipping OOS")
        
        # Final results
        if not oos_portfolios:
            logging.critical("No OOS portfolios generated. WFO failed. Check parameters and data.")
            if chat_model_available():
                query = "My walk-forward optimization failed to generate any valid portfolios. What could be wrong with my strategy?"
                advice = ask_chat_model(query)
                logging.info(f"Chat model advice: {advice}")
            return
            
        # Aggregate OOS results
        logging.info(f"WFO complete. Generated {len(oos_portfolios)} OOS portfolios.")
        
        # Calculate aggregate metrics
        total_sharpe = sum(pf[0].stats('sharpe_ratio') for pf in oos_portfolios)
        avg_sharpe = total_sharpe / len(oos_portfolios)
        
        logging.info(f"Average OOS Sharpe: {avg_sharpe:.2f}")
        
        # Ask chat model for interpretation
        if chat_model_available() and len(oos_portfolios) > 0:
            metrics = {f"Split {pf[2]}": {
                "sharpe": pf[0].stats('sharpe_ratio'),
                "return": pf[0].stats('total_return'),
                "drawdown": pf[0].stats('max_drawdown'),
                "trades": pf[0].stats('total_trades')
            } for pf in oos_portfolios}
            
            query = f"Interpret these walk-forward optimization results: {metrics}"
            interpretation = ask_chat_model(query)
            logging.info(f"Chat model interpretation: {interpretation}")
    
    except Exception as e:
        logging.error(f"Error during walk-forward optimization: {e}")
        if chat_model_available():
            context = {"error_location": "walk-forward optimization"}
            debug_with_chat(e, "Error during walk-forward optimization process", context)

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


def create_wfo_splits(data, num_splits=3, train_size=0.7):
    """
    Create walk-forward optimization splits from historical data.
    
    Args:
        data (dict): Dictionary containing OHLCV data
        num_splits (int): Number of splits to create
        train_size (float): Proportion of each split to use for training (0.0-1.0)
        
    Returns:
        list: List of tuples (train_data, test_data) for each split
    """
    import pandas as pd
    import numpy as np
    
    logging.info(f"Creating {num_splits} WFO splits with train size {train_size:.1%}")
    
    # Ensure we have a pandas DataFrame with a DatetimeIndex
    if 'close' not in data:
        logging.error("Data must contain 'close' prices")
        return []
        
    # Calculate total length and period lengths
    total_length = len(data['close'])
    period_length = total_length // num_splits
    
    if period_length < 100:
        logging.warning(f"Small period length: {period_length}. Consider reducing the number of splits.")
    
    # Create splits
    splits = []
    for i in range(num_splits):
        # Calculate indices for this split
        start_idx = i * period_length
        end_idx = (i + 1) * period_length if i < num_splits - 1 else total_length
        
        # Calculate train/test split point
        split_idx = start_idx + int(period_length * train_size)
        
        # Create train and test dictionaries with data slices
        train_data = {}
        test_data = {}
        
        # Copy all data columns
        for key, values in data.items():
            if isinstance(values, pd.Series) or isinstance(values, pd.DataFrame):
                train_data[key] = values.iloc[start_idx:split_idx].copy()
                test_data[key] = values.iloc[split_idx:end_idx].copy()
            elif isinstance(values, np.ndarray):
                train_data[key] = values[start_idx:split_idx].copy()
                test_data[key] = values[split_idx:end_idx].copy()
            else:
                # For other types, just reference the original
                train_data[key] = values
                test_data[key] = values
        
        # Log split info
        train_len = len(train_data['close'])
        test_len = len(test_data['close'])
        logging.info(f"Split {i+1}: Train size {train_len}, Test size {test_len}")
        
        splits.append((train_data, test_data))
    
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

def debug_with_chat(error, context=None, params=None):
    """Debug an error with assistance from the chat model.
    
    Args:
        error (Exception): The error that occurred.
        context (str, optional): Context of where the error occurred.
        params (dict, optional): Parameters that were used when the error occurred.
    
    Returns:
        str: The debugging advice from the chat model, or a default message if chat is not available.
    """
    chat_model = get_chat_model()
    
    if chat_model is None:
        wfo_logger.warning("Chat model not available for debugging. Check API key configuration.")
        return "Chat model not available. Please check configuration and API keys."
    
    try:
        # Prepare the error message
        error_message = f"Error: {str(error)}\n"
        if context:
            error_message += f"Context: {context}\n"
        if params:
            error_message += f"Parameters: {str(params)}\n"
        
        # Get traceback information
        import traceback
        tb_str = traceback.format_exc()
        error_message += f"Traceback:\n{tb_str}"
        
        # Query the chat model
        response = chat_model(f"""
        Please help debug this error in my trading strategy:
        
        {error_message}
        
        What might be causing this error and how can I fix it?
        """)
        
        wfo_logger.info(f"Received debugging advice from chat model")
        return response
    
    except Exception as e:
        wfo_logger.error(f"Error using chat model for debugging: {e}", exc_info=True)
        return f"Failed to get debugging assistance. Error: {str(e)}" 

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