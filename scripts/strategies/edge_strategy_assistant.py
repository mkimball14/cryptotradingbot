#!/usr/bin/env python3
import os
import sys
import logging
import json
import time
import pandas as pd
import numpy as np
import requests
from typing import Dict, List, Union, Any, Optional, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("edge_strategy_assistant")

# Load environment variables
load_dotenv(verbose=True)

# --- New Helper Classes and Functions ---

class RateLimiter:
    """Rate limiter to prevent excessive API calls."""
    def __init__(self, max_calls=20, per_seconds=60):
        self.max_calls = max_calls
        self.per_seconds = per_seconds
        self.calls = []
    
    def can_call(self):
        """Check if a call can be made without exceeding rate limits."""
        now = time.time()
        # Remove old calls
        self.calls = [t for t in self.calls if now - t < self.per_seconds]
        # Check if under limit
        return len(self.calls) < self.max_calls
    
    def record_call(self):
        """Record a call for rate limiting purposes."""
        self.calls.append(time.time())
    
    def wait_if_needed(self):
        """Wait if rate limit is exceeded and return whether waiting was needed."""
        if not self.can_call():
            logger.warning("Rate limit exceeded, waiting before next call...")
            time.sleep(10)  # Wait before retry
            return True
        return False

def parse_llm_json(response):
    """Parse JSON from LLM response with robust fallbacks."""
    try:
        # Direct JSON parsing
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from code blocks
        import re
        json_match = re.search(r'```(?:json)?\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to extract JSON-like structures with simpler patterns
        # Look for content within curly braces with reasonable JSON content
        json_pattern = r'\{(?:[^{}]|\{[^{}]*\})*\}'
        try:
            json_match = re.search(json_pattern, response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except (re.error, json.JSONDecodeError):
            pass
        
        # Return structured error
        return {
            "error": "Failed to parse JSON",
            "raw_response": response
        }

def save_metrics(metrics_data):
    """Save performance metrics to a jsonl file."""
    try:
        metrics_file = os.path.join(ROOT_DIR, "data/metrics/chat_metrics.jsonl")
        os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(metrics_data) + '\n')
        return True
    except Exception as e:
        logger.warning(f"Failed to save metrics: {e}")
        return False

def create_task_from_strategy_insight(insight, priority="medium"):
    """Create a task from strategy insight using task-master."""
    try:
        import subprocess
        
        # Format the insight as a task prompt
        prompt = f"Implement strategy improvement: {insight}"
        
        # Create task using task-master CLI
        cmd = [
            "task-master", "add-task",
            "--prompt", prompt,
            "--priority", priority
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Created new task from strategy insight: {insight}")
            return {"success": True, "output": result.stdout}
        else:
            logger.error(f"Failed to create task: {result.stderr}")
            return {"success": False, "error": result.stderr}
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return {"success": False, "error": str(e)}

# Initialize rate limiter for API calls
api_rate_limiter = RateLimiter(max_calls=30, per_seconds=60)

# --- End of New Helper Functions ---

# Check for API keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

if OPENAI_API_KEY:
    logger.info("Found OPENAI_API_KEY environment variable")
else:
    logger.warning("OPENAI_API_KEY not found in environment variables")

if OPENROUTER_API_KEY:
    logger.info("Found OPENROUTER_API_KEY environment variable")
else:
    logger.warning("OPENROUTER_API_KEY not found in environment variables")

# Use OpenRouter as fallback if OpenAI key is not available
API_KEY = OPENAI_API_KEY or OPENROUTER_API_KEY
API_BASE_URL = "https://openrouter.ai/api/v1" if not OPENAI_API_KEY and OPENROUTER_API_KEY else None

# Try to import VectorBT Pro
try:
    import vectorbtpro as vbt
    # Don't import EdgeMultiFactorStrategy anymore since we'll create our own version
    VECTORBT_AVAILABLE = True
    logger.info("VectorBTpro successfully imported")
    
    # Configure VectorBT with API keys if available
    if API_KEY:
        # Configure embeddings API key - but don't fail if settings aren't available
        try:
            # Check if required packages are installed
            try:
                import sentence_transformers
                EMBEDDINGS_AVAILABLE = True
                logger.info("sentence_transformers package is available for embeddings")
            except ImportError:
                EMBEDDINGS_AVAILABLE = False
                logger.warning("sentence_transformers package not installed - embeddings features won't work")
                logger.warning("Install with: pip install sentence-transformers")
            
            # Only try to set embeddings if the package is available
            if EMBEDDINGS_AVAILABLE:
                vbt.settings.set('knowledge.chat.embeddings_configs.openai.api_key', API_KEY)
                logger.info("Configured embeddings API key in vbt.settings")
            
            # Configure GitHub token if available
            if GITHUB_TOKEN:
                vbt.settings.set('knowledge.assets.vbt.token', GITHUB_TOKEN)
                logger.info("GitHub token configured in vbt.settings")
                
            # Configure base URL if using OpenRouter
            if API_BASE_URL:
                vbt.settings.set('knowledge.chat.openai_base_url', API_BASE_URL)
                logger.info(f"Configured API base URL: {API_BASE_URL}")
            
            # Check if vbt.chat is available (this was confirmed working in our tests)
            if hasattr(vbt, 'chat') and callable(vbt.chat):
                NATIVE_CHATVBT_AVAILABLE = True
                logger.info("Native vbt.chat function is available")
            else:
                NATIVE_CHATVBT_AVAILABLE = False
                logger.warning("Native vbt.chat function not available in this version of VectorBT")
                
            # The actual ChatVBT class isn't available in your version
            CHATVBT_AVAILABLE = False
        except Exception as e:
            logger.warning(f"Failed to configure VectorBT settings: {e}")
            EMBEDDINGS_AVAILABLE = False
            NATIVE_CHATVBT_AVAILABLE = False
            CHATVBT_AVAILABLE = False
    else:
        logger.warning("No API keys available, ChatVBT will not be enabled")
        EMBEDDINGS_AVAILABLE = False
        NATIVE_CHATVBT_AVAILABLE = False
        CHATVBT_AVAILABLE = False
except ImportError as e:
    logger.warning(f"Failed to import VectorBTpro: {e}")
    logger.warning("Limited functionality available")
    VECTORBT_AVAILABLE = False
    EMBEDDINGS_AVAILABLE = False
    NATIVE_CHATVBT_AVAILABLE = False
    CHATVBT_AVAILABLE = False

# Silence VBT warnings for cleaner output
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def search_vectorbt_docs(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search VectorBT documentation using SearchVBT.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary containing search results
    """
    logger.info(f"Searching VectorBT docs for: {query}")
    
    if not VECTORBT_AVAILABLE:
        logger.warning("VectorBT not available, cannot search docs")
        return {"error": "VectorBT not available"}
    
    try:
        # Try using VectorBT's SearchVBT if available
        if hasattr(vbt, 'SearchVBT'):
            results = vbt.SearchVBT().search(query, max_results=max_results)
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "description": result.get("content", "")[:200] + "...",
                    "url": result.get("url", ""),
                    "score": result.get("score", 0)
                })
            
            return {
                "query": query,
                "results": formatted_results,
                "timestamp": pd.Timestamp.now().isoformat()
            }
        else:
            # Fallback for when SearchVBT is not available
            logger.warning("SearchVBT not available in this version of VectorBT")
            
            # Return some generic documentation links as fallback
            return {
                "query": query,
                "results": [
                    {
                        "title": "VectorBT Documentation",
                        "description": "The official VectorBT documentation. SearchVBT not available in current installation.",
                        "url": "https://vectorbt.dev/docs/",
                        "score": 1.0
                    },
                    {
                        "title": "RSI Documentation",
                        "description": "Information on the Relative Strength Index (RSI) indicator.",
                        "url": "https://vectorbt.dev/docs/indicators/ta/rsi/",
                        "score": 0.9
                    },
                    {
                        "title": "Bollinger Bands Documentation",
                        "description": "Information on the Bollinger Bands indicator.",
                        "url": "https://vectorbt.dev/docs/indicators/ta/bbands/",
                        "score": 0.8
                    }
                ],
                "timestamp": pd.Timestamp.now().isoformat(),
                "fallback": True
            }
    except Exception as e:
        logger.error(f"Error searching VectorBT docs: {e}")
        return {"error": str(e)}

def chat_with_vectorbt(prompt: str, model=None, temperature=0.7, max_tokens=1500, use_cache=True) -> str:
    """
    Chat with LLM using VectorBT-compatible interface but with optimized fallbacks.
    
    Args:
        prompt: The prompt to send to the model
        model: Optional model name (defaults to ChatVBT default)
        temperature: Temperature for generation
        max_tokens: Maximum tokens in response
        use_cache: Whether to use cached responses if available
        
    Returns:
        Response from the model
    """
    # Start metrics tracking
    metrics = {
        "start_time": time.time(),
        "success": False,
        "method_used": None,
        "prompt_length": len(prompt),
        "model": model or "gpt-4-turbo-preview",
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    logger.info(f"Sending prompt to AI: {prompt[:50]}...")
    
    # Check cache first if enabled
    if use_cache:
        cache_file = os.path.join(ROOT_DIR, "data/cache/chat_cache.json")
        cache_key = f"{prompt}_{model}_{temperature}_{max_tokens}".replace(" ", "_")[:100]  # Keep key reasonable length
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
                    if cache_key in cache:
                        cached_entry = cache[cache_key]
                        # Check if cache entry is less than 24 hours old
                        cache_time = pd.Timestamp(cached_entry.get('timestamp', '2000-01-01'))
                        if pd.Timestamp.now() - cache_time < pd.Timedelta(hours=24):
                            logger.info("Using cached response")
                            metrics["method_used"] = "cache"
                            metrics["success"] = True
                            metrics["end_time"] = time.time()
                            metrics["duration"] = metrics["end_time"] - metrics["start_time"]
                            save_metrics(metrics)
                            return cached_entry['response']
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
    
    # Always check rate limits before making API calls
    api_rate_limiter.wait_if_needed()
    api_rate_limiter.record_call()
    
    # Only try VectorBT native methods if embeddings are available
    if VECTORBT_AVAILABLE and EMBEDDINGS_AVAILABLE:
        # 1. Try native vbt.chat - our tests confirm this works!
        if NATIVE_CHATVBT_AVAILABLE:
            try:
                logger.info("Using native vbt.chat which we know works...")
                # Don't capture the printed response - it's sent to stdout
                vbt.chat(prompt, api_key=API_KEY)
                # Do a direct call to get a capturable response
                response = None
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=API_KEY)
                    completion = client.chat.completions.create(
                        model="gpt-4-turbo-preview",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    response = completion.choices[0].message.content
                    metrics["method_used"] = "native_vbt_with_direct_openai"
                except Exception as e:
                    logger.warning(f"Error getting capturable response: {e}")
                    # Use a placeholder response since vbt.chat already printed the answer
                    response = "Response was sent to console output via vbt.chat"
                    metrics["method_used"] = "native_vbt_only"
                
                logger.info("Successfully completed native vbt.chat query")
                metrics["success"] = True
                metrics["end_time"] = time.time()
                metrics["duration"] = metrics["end_time"] - metrics["start_time"]
                save_metrics(metrics)
                
                # Update cache if enabled
                if use_cache and response:
                    try:
                        cache = {}
                        if os.path.exists(cache_file):
                            with open(cache_file, 'r') as f:
                                cache = json.load(f)
                        
                        cache[cache_key] = {
                            'response': response,
                            'timestamp': pd.Timestamp.now().isoformat()
                        }
                        
                        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                        with open(cache_file, 'w') as f:
                            json.dump(cache, f)
                    except Exception as e:
                        logger.warning(f"Cache write error: {e}")
                
                return response
            except Exception as e:
                logger.warning(f"vbt.chat failed: {e}, trying alternatives")
        
        # 2. Try asset finding approach
        try:
            api_rate_limiter.wait_if_needed()
            api_rate_limiter.record_call()
            
            logger.info("Trying vbt.find_assets().chat approach...")
            relevant_assets = vbt.find_assets(prompt, top_k=10)
            if relevant_assets is not None:
                response = relevant_assets.chat(prompt, api_key=API_KEY)
                if response and len(response) > 0:
                    logger.info("Successfully received response from find_assets().chat")
                    metrics["method_used"] = "find_assets_chat"
                    metrics["success"] = True
                    metrics["end_time"] = time.time()
                    metrics["duration"] = metrics["end_time"] - metrics["start_time"]
                    save_metrics(metrics)
                    
                    # Update cache
                    if use_cache:
                        try:
                            cache = {}
                            if os.path.exists(cache_file):
                                with open(cache_file, 'r') as f:
                                    cache = json.load(f)
                            
                            cache[cache_key] = {
                                'response': response,
                                'timestamp': pd.Timestamp.now().isoformat()
                            }
                            
                            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                            with open(cache_file, 'w') as f:
                                json.dump(cache, f)
                        except Exception as e:
                            logger.warning(f"Cache write error: {e}")
                    
                    return response
            logger.warning("find_assets().chat failed or returned empty, trying alternatives")
        except Exception as e:
            logger.warning(f"find_assets().chat failed: {e}, trying alternatives")
    else:
        if VECTORBT_AVAILABLE:
            logger.info("Skipping native VectorBT chat methods - embeddings not available")
        else:
            logger.info("VectorBT not available, using direct API calls")
    
    # Direct API paths - these are working in your setup
    
    # Direct OpenAI API calls - preferred path
    if OPENAI_API_KEY:
        try:
            api_rate_limiter.wait_if_needed()
            api_rate_limiter.record_call()
            
            logger.info("Using OpenAI API directly")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            
            payload = {
                "model": "gpt-4-turbo-preview",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                logger.info("Successfully received response from OpenAI API")
                result = response.json()["choices"][0]["message"]["content"]
                metrics["method_used"] = "openai_direct"
                metrics["success"] = True
                metrics["end_time"] = time.time()
                metrics["duration"] = metrics["end_time"] - metrics["start_time"]
                save_metrics(metrics)
                
                # Update cache
                if use_cache:
                    try:
                        cache = {}
                        if os.path.exists(cache_file):
                            with open(cache_file, 'r') as f:
                                cache = json.load(f)
                        
                        cache[cache_key] = {
                            'response': result,
                            'timestamp': pd.Timestamp.now().isoformat()
                        }
                        
                        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                        with open(cache_file, 'w') as f:
                            json.dump(cache, f)
                    except Exception as e:
                        logger.warning(f"Cache write error: {e}")
                
                return result
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error querying OpenAI API: {e}")
    
    # OpenRouter API as fallback
    if OPENROUTER_API_KEY:
        try:
            api_rate_limiter.wait_if_needed()
            api_rate_limiter.record_call()
            
            logger.info("Using OpenRouter API")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://github.com/openrouter-dev/openrouter",
                "X-Title": "Edge Strategy Assistant"
            }
            
            payload = {
                "model": "openai/gpt-4-turbo-preview",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                logger.info("Successfully received response from OpenRouter API")
                result = response.json()["choices"][0]["message"]["content"]
                metrics["method_used"] = "openrouter"
                metrics["success"] = True
                metrics["end_time"] = time.time()
                metrics["duration"] = metrics["end_time"] - metrics["start_time"]
                save_metrics(metrics)
                
                # Update cache
                if use_cache:
                    try:
                        cache = {}
                        if os.path.exists(cache_file):
                            with open(cache_file, 'r') as f:
                                cache = json.load(f)
                        
                        cache[cache_key] = {
                            'response': result,
                            'timestamp': pd.Timestamp.now().isoformat()
                        }
                        
                        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                        with open(cache_file, 'w') as f:
                            json.dump(cache, f)
                    except Exception as e:
                        logger.warning(f"Cache write error: {e}")
                
                return result
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error querying OpenRouter API: {e}")
    
    # If all methods fail, return error message
    error_msg = "All chat methods failed, please check API keys and try again."
    logger.error(error_msg)
    metrics["method_used"] = "all_failed"
    metrics["success"] = False
    metrics["error"] = error_msg
    metrics["end_time"] = time.time()
    metrics["duration"] = metrics["end_time"] - metrics["start_time"]
    save_metrics(metrics)
    return error_msg

# Define EdgeStrategy class with RSI, BB, and vol parameters
class EdgeStrategy:
    """Base Edge Strategy with RSI, Bollinger Bands, and Volatility indicators."""
    
    def __init__(self, 
                 rsi_window=14, 
                 rsi_entry=30, 
                 rsi_exit=70, 
                 bb_window=20, 
                 bb_dev=2.0,
                 vol_window=20, 
                 vol_threshold=1.5, 
                 sl_pct=2.0, 
                 tp_pct=4.0, 
                 risk_per_trade=0.02):
        """Initialize the edge strategy with the specified parameters."""
        self.rsi_window = int(rsi_window)
        self.rsi_entry = float(rsi_entry)
        self.rsi_exit = float(rsi_exit)
        self.bb_window = int(bb_window)
        self.bb_dev = float(bb_dev)
        self.vol_window = int(vol_window)
        self.vol_threshold = float(vol_threshold)
        self.sl_pct = float(sl_pct)
        self.tp_pct = float(tp_pct)
        self.risk_per_trade = float(risk_per_trade)
        
        logger.info(f"Initialized EdgeStrategy with parameters: RSI({self.rsi_window}, {self.rsi_entry}, {self.rsi_exit}), BB({self.bb_window}, {self.bb_dev})")
    
    def generate_signals(self, data):
        """Generate entry and exit signals for the strategy."""
        if not VECTORBT_AVAILABLE:
            logger.error("VectorBT not available, cannot generate signals")
            return None, None
        
        try:
            price_data = data['close'] if isinstance(data, pd.DataFrame) else data
            
            # Generate indicators
            rsi = vbt.RSI.run(price_data, window=self.rsi_window)
            
            try:
                bb = vbt.BBands.run(price_data, window=self.bb_window, alpha=self.bb_dev)
            except AttributeError:
                try:
                    bb = vbt.BBANDS.run(price_data, window=self.bb_window, alpha=self.bb_dev)
                except AttributeError:
                    logger.warning("Bollinger Bands indicators not found, calculating manually")
                    bb_middle = price_data.rolling(window=self.bb_window).mean()
                    bb_std = price_data.rolling(window=self.bb_window).std()
                    bb_upper = bb_middle + (bb_std * self.bb_dev)
                    bb_lower = bb_middle - (bb_std * self.bb_dev)
                    from types import SimpleNamespace
                    bb = SimpleNamespace(
                        middle=bb_middle,
                        upper=bb_upper,
                        lower=bb_lower
                    )
            
            # Generate entry signals
            rsi_condition = rsi.rsi < self.rsi_entry
            bb_condition = price_data < bb.lower
            entries = (rsi_condition & bb_condition) | (rsi.rsi < (self.rsi_entry - 5))
            
            # Generate exit signals
            exits = (rsi.rsi > self.rsi_exit) | (price_data > bb.middle * 0.98)
            
            # Convert to boolean
            entries = entries.astype(bool)
            exits = exits.astype(bool)
            
            return entries, exits
            
        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            return None, None
            
    def backtest(self, data, init_cash=100000):
        """Backtest the strategy on the given data."""
        if not VECTORBT_AVAILABLE:
            logger.error("VectorBT not available, cannot backtest")
            return None
            
        try:
            price_data = data['close'] if isinstance(data, pd.DataFrame) else data
            
            # Generate signals
            entries, exits = self.generate_signals(data)
            
            if entries is None or exits is None:
                logger.error("Could not generate signals for backtest")
                return None
                
            if entries.sum() == 0:
                logger.warning("No entry signals generated")
                return None
                
            # Calculate stop-loss and take-profit levels
            sl_stop = self.sl_pct / 100
            tp_stop = self.tp_pct / 100
            
            # Create portfolio
            pf = vbt.Portfolio.from_signals(
                price_data,
                entries,
                exits,
                sl_stop=sl_stop,
                tp_stop=tp_stop,
                size_type='value',
                size=init_cash * self.risk_per_trade,
                init_cash=init_cash,
                fees=0.001,
                slippage=0.001,
                freq='1D'
            )
            
            return pf
            
        except Exception as e:
            logger.error(f"Error backtesting strategy: {e}")
            return None

class EnhancedEdgeStrategy(EdgeStrategy):
    """Enhanced Edge Strategy with AI-powered optimization features."""
    
    def __init__(self, **kwargs):
        """Initialize the enhanced edge strategy with AI capabilities."""
        # Set default parameters if not provided
        default_params = {
            "rsi_window": 14,
            "rsi_entry": 30,
            "rsi_exit": 70,
            "bb_window": 20,
            "bb_dev": 2.0,
            "vol_window": 20,
            "vol_threshold": 1.5,
            "sl_pct": 2.0,
            "tp_pct": 4.0,
            "risk_per_trade": 0.02
        }
        
        # Merge default parameters with any provided parameters
        params = {**default_params, **kwargs}
        
        # Initialize the parent class with the parameters
        super().__init__(**params)
        
        logger.info("Initialized EnhancedEdgeStrategy")
        logger.info(f"Strategy parameters: RSI({self.rsi_window}, {self.rsi_entry}, {self.rsi_exit}), BB({self.bb_window}, {self.bb_dev})")
    
    def get_parameter_suggestions(self) -> Dict[str, Any]:
        """
        Get parameter suggestions from ChatVBT for the current strategy.
        
        Returns:
            Dictionary with parameter suggestions and explanations
        """
        logger.info("Getting parameter suggestions from ChatVBT")
        
        current_params = {
            "rsi_window": self.rsi_window,
            "rsi_entry": self.rsi_entry,
            "rsi_exit": self.rsi_exit,
            "bb_window": self.bb_window,
            "bb_dev": self.bb_dev,
            "vol_window": self.vol_window,
            "vol_threshold": self.vol_threshold,
            "sl_pct": self.sl_pct,
            "tp_pct": self.tp_pct,
            "risk_per_trade": self.risk_per_trade
        }
        
        prompt = f"""
        Analyze these current strategy parameters and suggest potential improvements:
        
        RSI Window: {self.rsi_window}
        RSI Entry (Oversold): {self.rsi_entry}
        RSI Exit (Overbought): {self.rsi_exit}
        Bollinger Bands Window: {self.bb_window}
        Bollinger Bands Deviation: {self.bb_dev}
        Volatility Window (ATR): {self.vol_window}
        Volatility Threshold: {self.vol_threshold}
        Stop Loss Percentage: {self.sl_pct}%
        Take Profit Percentage: {self.tp_pct}%
        Risk Per Trade: {self.risk_per_trade * 100}%
        
        Provide suggestions for each parameter with a brief explanation of why the change would improve performance.
        Also recommend any additional indicators or features that could enhance this strategy.
        Format your response as JSON with parameter names, suggested values, and explanations.
        """
        
        response = chat_with_vectorbt(prompt)
        
        # Use the new JSON parser for more robust parsing
        suggestions = parse_llm_json(response)
        
        # If the suggestions contain high-value improvements, create a task
        if "parameter_suggestions" in suggestions and not isinstance(suggestions["parameter_suggestions"], str):
            try:
                # Extract a summary of the key improvements
                params_improved = list(suggestions["parameter_suggestions"].keys())
                summary = f"Parameter optimization for {', '.join(params_improved[:3])}"
                if len(params_improved) > 3:
                    summary += f" and {len(params_improved) - 3} more parameters"
                
                # Create a task with medium priority
                create_task_from_strategy_insight(summary, priority="medium")
            except Exception as e:
                logger.warning(f"Failed to create task from parameter suggestions: {e}")
        
        return suggestions
    
    def optimize_for_market_condition(self, market_condition: str) -> Dict[str, Any]:
        """
        Optimize strategy parameters for a specific market condition.
        
        Args:
            market_condition: Type of market condition (trending, ranging, volatile)
            
        Returns:
            Dictionary with optimized parameters for the specified market condition
        """
        logger.info(f"Optimizing for {market_condition} market conditions")
        
        prompt = f"""
        Provide optimized parameters for a trading strategy using RSI, Bollinger Bands, and ATR
        for a {market_condition.upper()} market condition in BTC/USD.
        
        Current parameters:
        RSI Window: {self.rsi_window}
        RSI Entry (Oversold): {self.rsi_entry}
        RSI Exit (Overbought): {self.rsi_exit}
        Bollinger Bands Window: {self.bb_window}
        Bollinger Bands Deviation: {self.bb_dev}
        Volatility Window (ATR): {self.vol_window}
        Volatility Threshold: {self.vol_threshold}
        Stop Loss Percentage: {self.sl_pct}%
        Take Profit Percentage: {self.tp_pct}%
        Risk Per Trade: {self.risk_per_trade * 100}%
        
        Explain why each parameter change is suitable for a {market_condition} market.
        Format your response as JSON with parameter names, values, and explanations.
        """
        
        response = chat_with_vectorbt(prompt)
        
        # Use robust JSON parsing
        result = parse_llm_json(response)
        
        # Create task for market condition optimization if it has parameters
        if isinstance(result, dict) and any(k in result for k in ["parameters", "optimized_parameters", "values"]):
            try:
                insight = f"Optimized strategy for {market_condition} market conditions"
                create_task_from_strategy_insight(insight, priority="high")
            except Exception as e:
                logger.warning(f"Failed to create task for market condition optimization: {e}")
        
        return result
    
    def debug_portfolio_creation(self, error_message: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Debug portfolio creation issues with ChatVBT.
        
        Args:
            error_message: The error message encountered
            params: The parameters used when the error occurred
            
        Returns:
            Dictionary with debugging information and suggested fixes
        """
        logger.info(f"Debugging portfolio creation issue: {error_message[:50]}...")
        
        prompt = f"""
        Debug this portfolio creation error in a VectorBT trading strategy:
        
        ERROR: {error_message}
        
        The strategy uses these parameters:
        {json.dumps(params, indent=2)}
        
        The portfolio is created using vbt.Portfolio.from_signals() with entries and exits
        based on RSI, Bollinger Bands, and ATR indicators.
        
        What is likely causing this error? Provide specific code fixes to resolve it.
        Focus on:
        1. Boolean operations with pandas Series
        2. Handling NaN values
        3. Proper signal generation
        4. Type conversion issues
        
        Format your response as a JSON with 'diagnosis', 'solution', and 'code_fix' fields.
        """
        
        response = chat_with_vectorbt(prompt)
        
        # Use robust JSON parsing
        result = parse_llm_json(response)
        
        # Create high priority task for critical errors
        if isinstance(result, dict) and "diagnosis" in result and "solution" in result:
            try:
                insight = f"Fix portfolio creation error: {result['diagnosis'][:50]}..."
                create_task_from_strategy_insight(insight, priority="high")
            except Exception as e:
                logger.warning(f"Failed to create task for error fix: {e}")
        
        return result
    
    def research_indicator_settings(self, indicator: str) -> Dict[str, Any]:
        """
        Research optimal settings for a specific indicator using SearchVBT and ChatVBT.
        
        Args:
            indicator: Name of the indicator to research (e.g., "RSI", "Bollinger Bands")
            
        Returns:
            Dictionary with research results and recommendations
        """
        logger.info(f"Researching optimal settings for {indicator}")
        
        # First search the documentation
        search_results = search_vectorbt_docs(f"optimal {indicator} settings for cryptocurrency trading")
        
        # Then get advice from ChatVBT
        prompt = f"""
        Provide a comprehensive analysis of optimal {indicator} settings for cryptocurrency trading:
        
        1. What are the most effective parameter values for {indicator} when trading Bitcoin?
        2. How should {indicator} parameters be adjusted for different market conditions?
        3. What are common mistakes traders make when using {indicator}?
        4. What complementary indicators work well with {indicator}?
        5. How can {indicator} be used most effectively for entry and exit signals?
        
        Base your analysis on empirical research and best practices in cryptocurrency trading.
        Format your response as a structured JSON with sections for each question.
        """
        
        chat_response = chat_with_vectorbt(prompt)
        
        # Use robust JSON parsing
        parsed_response = parse_llm_json(chat_response)
        
        # Create the complete research package
        research = {
            "indicator": indicator,
            "documentation_search": search_results,
            "expert_analysis": parsed_response,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        # Create task for implementing research findings
        try:
            insight = f"Implement optimal {indicator} settings from research"
            create_task_from_strategy_insight(insight, priority="medium")
        except Exception as e:
            logger.warning(f"Failed to create task for indicator research: {e}")
        
        return research
    
    def analyze_backtest_results(self, portfolio) -> Dict[str, Any]:
        """
        Analyze backtest results with ChatVBT.
        
        Args:
            portfolio: VectorBT Portfolio object or dictionary with backtest results
            
        Returns:
            Dictionary with analysis and improvement recommendations
        """
        logger.info("Analyzing backtest results")
        
        try:
            # Check if portfolio is a dictionary
            if isinstance(portfolio, dict):
                # Use the dictionary directly
                metrics = portfolio
            else:
                # Extract key metrics from portfolio object
                metrics = {
                    "total_return": float(portfolio.total_return),
                    "sharpe_ratio": float(portfolio.sharpe_ratio),
                    "sortino_ratio": float(portfolio.sortino_ratio),
                    "max_drawdown": float(portfolio.max_drawdown),
                    "win_rate": float(portfolio.win_rate),
                    "profit_factor": float(portfolio.profit_factor) if not pd.isna(portfolio.profit_factor) else None,
                    "num_trades": int(portfolio.count)
                }
                
                # Get daily returns for volatility calculation
                returns = portfolio.returns.daily()
                volatility = float(returns.std() * (252 ** 0.5))  # Annualized
                metrics["annualized_volatility"] = volatility
                
                # Add trade analysis
                metrics["avg_win"] = float(portfolio.trades.winning.pnl.mean()) if len(portfolio.trades.winning) > 0 else 0
                metrics["avg_loss"] = float(portfolio.trades.losing.pnl.mean()) if len(portfolio.trades.losing) > 0 else 0
                metrics["avg_trade_duration"] = str(portfolio.trades.duration.mean())
            
            # Send to ChatVBT for analysis
            prompt = f"""
            Analyze these backtest results for a cryptocurrency trading strategy:
            
            {json.dumps(metrics, indent=2)}
            
            The strategy uses RSI, Bollinger Bands, and ATR for signal generation.
            
            Provide a comprehensive analysis including:
            1. Overall performance assessment
            2. Key strengths and weaknesses identified
            3. Specific recommendations to improve performance
            4. Risk management assessment
            5. Parameter optimization suggestions
            
            Format your response as JSON with sections for each analysis component.
            """
            
            response = chat_with_vectorbt(prompt)
            
            # Use robust JSON parsing
            analysis = parse_llm_json(response)
            
            # Create tasks from analysis insights if there are recommendations
            if isinstance(analysis, dict) and "recommendations" in analysis:
                try:
                    # Look for recommendations
                    recommendations = analysis["recommendations"]
                    if isinstance(recommendations, list) and len(recommendations) > 0:
                        # Create task for the first recommendation
                        insight = f"Implement backtest improvement: {recommendations[0][:100]}"
                        create_task_from_strategy_insight(insight, priority="high")
                except Exception as e:
                    logger.warning(f"Failed to create task from backtest analysis: {e}")
            
            # Combine metrics with analysis
            result = {
                "metrics": metrics,
                "analysis": analysis,
                "timestamp": pd.Timestamp.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing backtest results: {str(e)}")
            return {
                "error": str(e),
                "timestamp": pd.Timestamp.now().isoformat()
            }

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
            logger.error("Insufficient data for portfolio creation")
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
                        logger.error(f"Missing required column: {col}")
                        return None, False
            
            # Convert to numeric and handle any errors
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for NaN values
        if df[required_columns].isna().any().any():
            logger.warning("Data contains NaN values. Filling with forward fill method.")
            df[required_columns] = df[required_columns].fillna(method='ffill')
            # After filling, check again for any remaining NaNs
            if df[required_columns].isna().any().any():
                logger.error("Data still contains NaN values after filling")
                return None, False
        
        # Apply edge strategy with parameters
        from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
        
        # Convert parameters to appropriate types if needed
        strategy_params = params.copy()
        
        # Create the strategy
        strategy = EdgeMultiFactorStrategy(**strategy_params)
        
        # Run the strategy to get entry/exit signals
        # --- Unpack all four return values --- (Regime masks not used here yet)
        entry_signals, exit_signals, is_trending, is_ranging = strategy.generate_signals(df)
        # -------------------------------------
        
        # Check if any signals were generated
        if entry_signals.sum() == 0:
            logger.warning(f"No entry signals generated with parameters: {params}")
            return None, False
            
        # Create portfolio from signals
        portfolio, metrics = strategy.backtest_signals(entry_signals, exit_signals)
        
        # Debug info if requested
        if debug:
            if portfolio is not None:
                logger.debug(f"Portfolio metrics: {metrics}")
            else:
                logger.debug("Portfolio creation failed")
            
        return portfolio, True
        
    except Exception as e:
        logger.error(f"Error creating portfolio: {str(e)}")
        import traceback
        logger.debug(traceback.format_exc())
        return None, False

def main():
    """Test the Edge Strategy Assistant."""
    logger.info("Testing Edge Strategy Assistant capabilities")
    
    # Test SearchVBT functionality
    logger.info("Testing SearchVBT...")
    search_results = search_vectorbt_docs("optimal RSI settings for crypto")
    logger.info(f"Found {len(search_results['results'])} search results")
    
    # Test ChatVBT functionality
    logger.info("Testing ChatVBT...")
    chat_response = chat_with_vectorbt("What are the best parameters for RSI when trading Bitcoin?")
    logger.info(f"Received chat response: {chat_response[:100]}...")
    
    # Create EnhancedEdgeStrategy instance
    logger.info("Creating EnhancedEdgeStrategy instance...")
    strategy = EnhancedEdgeStrategy(
        rsi_window=14,
        rsi_entry=30,
        rsi_exit=70,
        bb_window=20,
        bb_dev=2.0,
        vol_window=20,
        vol_threshold=1.5,
        sl_pct=2.0,
        tp_pct=4.0,
        risk_per_trade=0.02
    )
    
    # Get parameter suggestions
    logger.info("Getting parameter suggestions...")
    suggestions = strategy.get_parameter_suggestions()
    logger.info("Parameter suggestions received")
    
    logger.info("Edge Strategy Assistant test complete")

if __name__ == "__main__":
    main() 