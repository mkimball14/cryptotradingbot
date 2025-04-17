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

# Try to import VectorBT Pro
try:
    import vectorbtpro as vbt
    # Don't import EdgeMultiFactorStrategy anymore since we'll create our own version
    VECTORBT_AVAILABLE = True
    logger.info("VectorBTpro successfully imported")
except ImportError as e:
    logger.warning(f"Failed to import VectorBTpro: {e}")
    logger.warning("Limited functionality available")
    VECTORBT_AVAILABLE = False

# Silence VBT warnings for cleaner output
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Check for API keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if OPENAI_API_KEY:
    logger.info("Found OPENAI_API_KEY environment variable")
else:
    logger.warning("OPENAI_API_KEY not found in environment variables")

if OPENROUTER_API_KEY:
    logger.info("Found OPENROUTER_API_KEY environment variable")
else:
    logger.warning("OPENROUTER_API_KEY not found in environment variables")

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

def chat_with_vectorbt(prompt: str, model=None, temperature=0.7, max_tokens=1500) -> str:
    """
    Chat with VectorBT using ChatVBT.
    
    Args:
        prompt: The prompt to send to ChatVBT
        model: Optional model name (defaults to ChatVBT default)
        temperature: Temperature for generation
        max_tokens: Maximum tokens in response
        
    Returns:
        Response from ChatVBT
    """
    logger.info(f"Sending prompt to ChatVBT: {prompt[:50]}...")
    
    # Function to handle direct OpenAI API calls as fallback
    def query_openai_api(api_key, prompt):
        try:
            logger.info("Trying OpenAI API directly")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
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
                return response.json()["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error querying OpenAI API: {e}")
            return None
    
    # Function to handle direct OpenRouter API calls as fallback
    def query_openrouter_api(api_key, prompt):
        try:
            logger.info("Trying OpenRouter API")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
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
                return response.json()["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error querying OpenRouter API: {e}")
            return None
    
    try:
        # Method 1: Try to use vectorbtpro's ChatVBT if available
        if VECTORBT_AVAILABLE and hasattr(vbt, 'ChatVBT'):
            try:
                logger.info("Attempting to use VectorBT's ChatVBT")
                response = vbt.ChatVBT.chat(prompt=prompt)
                if response:
                    logger.info("Received response from ChatVBT")
                    return response
                logger.warning("ChatVBT returned empty response")
            except Exception as e:
                logger.warning(f"Error using ChatVBT: {e}")
        elif VECTORBT_AVAILABLE:
            logger.warning("ChatVBT not available in this version of VectorBT")
        
        # Method 2: Try OpenAI API directly
        if OPENAI_API_KEY:
            response = query_openai_api(OPENAI_API_KEY, prompt)
            if response:
                return response
        
        # Method 3: Try OpenRouter API
        if OPENROUTER_API_KEY:
            response = query_openrouter_api(OPENROUTER_API_KEY, prompt)
            if response:
                return response
        
        # No methods worked
        logger.error("All methods failed to get a response from LLM")
        return "Error: Unable to get a response from any available LLM service."
    
    except Exception as e:
        logger.error(f"Error in chat_with_vectorbt: {e}")
        return f"Error: {str(e)}"

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
        
        # Try to parse JSON from the response
        try:
            # First try direct JSON parsing
            suggestions = json.loads(response)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from text response
            try:
                import re
                json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
                if json_match:
                    suggestions = json.loads(json_match.group(1))
                else:
                    # Create a fallback structure
                    suggestions = {
                        "parameter_suggestions": "Could not parse JSON from response",
                        "original_response": response
                    }
            except Exception:
                suggestions = {
                    "parameter_suggestions": "Could not parse JSON from response",
                    "original_response": response
                }
        
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
        
        # Try to parse JSON from the response
        try:
            # Attempt to parse JSON directly
            result = json.loads(response)
        except json.JSONDecodeError:
            # If parsing fails, return the raw response
            result = {
                "market_condition": market_condition,
                "raw_response": response
            }
        
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
        
        # Try to parse JSON from the response
        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            # If parsing fails, return a structured response with the raw text
            result = {
                "diagnosis": "Error parsing JSON response",
                "solution": "See raw response for details",
                "raw_response": response
            }
        
        return result
    
    def generate_adaptive_strategy(self) -> str:
        """
        Generate an adaptive strategy implementation based on ChatVBT recommendations.
        
        Returns:
            Python code as a string for an adaptive version of the edge strategy
        """
        logger.info("Generating adaptive strategy implementation")
        
        prompt = """
        Create a Python class for an adaptive trading strategy that:
        
        1. Inherits from EdgeMultiFactorStrategy
        2. Adjusts RSI, Bollinger Bands, and ATR parameters based on current market volatility
        3. Uses market regime detection to identify trending vs ranging conditions
        4. Adjusts stop loss and take profit levels dynamically based on ATR
        5. Includes position sizing that adapts to changing market conditions
        6. Implements trailing stops for trending markets
        
        The implementation should:
        - Use vectorbtpro for backtesting and optimization
        - Include detailed comments explaining the adaptive logic
        - Implement all methods needed for a complete class
        - Be ready to run with minimal modifications
        
        Return ONLY valid Python code without explanations or markdown formatting.
        """
        
        response = chat_with_vectorbt(prompt)
        
        # Clean up the response to extract just the code
        import re
        
        # Try to extract code block if it exists
        code_match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
        if code_match:
            code = code_match.group(1)
        else:
            # If no code block, assume the entire response is code
            code = response
        
        # Add a header comment
        header = f"""#!/usr/bin/env python3
# Adaptive Edge Strategy
# Generated by EdgeStrategyAssistant on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
# This strategy automatically adapts parameters based on market conditions

"""
        return header + code
    
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
        
        # Compile the research results
        try:
            # Try to parse chat response as JSON
            parsed_response = json.loads(chat_response)
        except json.JSONDecodeError:
            # If parsing fails, use the raw response
            parsed_response = {"raw_analysis": chat_response}
        
        # Create the complete research package
        research = {
            "indicator": indicator,
            "documentation_search": search_results,
            "expert_analysis": parsed_response,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
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
            
            # Try to parse JSON from the response
            try:
                analysis = json.loads(response)
            except json.JSONDecodeError:
                # If parsing fails, use the raw response
                analysis = {"raw_analysis": response}
            
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