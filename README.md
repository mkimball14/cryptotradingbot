# Crypto Trading Bot with AI-Powered Optimization

A cryptocurrency trading bot with walk-forward optimization and AI-assisted strategy development using VectorBT Pro and OpenAI/OpenRouter APIs.

## Features

- **Edge Multi-Factor Strategy**: Combines RSI, Bollinger Bands, and volatility indicators for robust trading signals
- **Walk-Forward Optimization**: Dynamic parameter optimization across multiple market regimes
- **AI Strategy Assistant**: Uses LLMs to help optimize strategies and analyze market conditions
- **Backtest Analysis**: Comprehensive performance metrics and visualization
- **Parameter Research**: AI-assisted research for optimal indicator settings
- **Adaptive Strategies**: Generation of strategies that adapt to changing market conditions
- **Direct Chat API Integration**: Flexible communication with LLMs via OpenRouter/OpenAI APIs

## System Requirements

- Python 3.8+
- VectorBT Pro license (or use the limited features with vectorbt open source)
- OpenAI API key or OpenRouter API key for AI features
- Pandas, NumPy, and other data science libraries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-trading-bot.git
cd crypto-trading-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create a `.env` file):
```
# Either OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
# OR OpenRouter API key (will be used if OpenAI key is not available)
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Architecture

The system consists of several key components:

1. **Edge Strategy Assistant**: AI-powered strategy development and optimization
   - ChatVBT integration for parameter suggestions
   - SearchVBT for researching optimal indicator settings
   - Direct Chat API for flexible LLM interactions
   - Strategy enhancement and adaptation

2. **Walk-Forward Optimization**: Robust parameter optimization
   - Multiple in-sample/out-of-sample splits
   - Comprehensive performance metrics
   - Parameter stability analysis
   - Enhanced portfolio validity checks

3. **Multi-Factor Strategy**: Combines multiple trading signals
   - RSI (Relative Strength Index)
   - Bollinger Bands
   - Volatility (ATR)
   - Risk management with stop-loss and take-profit

## Getting Started

### Basic Usage

To run a walk-forward optimization:

```bash
python scripts/strategies/wfo_edge_strategy.py
```

To optimize strategy with AI assistance:

```bash
python scripts/strategies/chat_optimize_edge_strategy.py
```

To test the AI strategy assistant:

```bash
python scripts/strategies/test_edge_assistant.py
```

To test direct chat functionality:

```bash
python scripts/strategies/test_direct_chat.py
```

### Understanding the Results

Analysis results are saved in the `analysis_results` directory:
- Complete strategy analysis in JSON format
- Backtesting results with performance metrics
- Market analysis and recommendations
- Adaptive strategy implementations

## AI-Assisted Strategy Development with VectorBT

This section provides a comprehensive explanation of how the AI assistance system works with VectorBT and how you can leverage it using Cursor for strategy enhancement, debugging, and development.

### ChatVBT and SearchVBT Architecture

#### ChatVBT Implementation

ChatVBT is VectorBT Pro's built-in integration with language models (LLMs) like OpenAI's GPT or models accessed through OpenRouter. The system implements this functionality through several key components:

1. **ChatVBT Configuration** (`setup_chat_provider()` in `wfo_edge_strategy.py`):
   - Initializes the LLM connection through VectorBT's API
   - Configures API keys from environment variables
   - Sets up knowledge base paths and settings

2. **ChatVBT Usage Flow**:
   ```
   User Request → wfo_edge_strategy.py → ask_chat_model() → VectorBT ChatProvider → API Response
   ```

3. **Fallback Mechanism**:
   - If ChatVBT initialization fails, system falls back to direct API calls
   - Failures detected in `setup_chat_provider()` trigger the fallback system
   - Direct calls bypass VectorBT's chat infrastructure entirely

#### SearchVBT Implementation

SearchVBT allows semantic search across VectorBT's documentation to find relevant information for strategy development:

1. **SearchVBT Configuration** (`search_vectorbt_docs()` in `edge_strategy_assistant.py`):
   - Initializes VectorBT's search functionality
   - Configures search parameters (max results, search depth)
   - Sets up result formatting

2. **Usage Flow**:
   ```
   Search Query → EdgeStrategyAssistant → search_vectorbt_docs() → VectorBT Search API → Formatted Results
   ```

### When Each System is Used

The system intelligently selects which AI interaction method to use based on context and availability:

1. **ChatVBT is used when**:
   - Running the walk-forward optimization process
   - Getting parameter suggestions via `get_optimization_advice_from_chat_model()`
   - Debugging portfolio creation issues via `debug_with_chat()`
   - Analyzing market conditions via `EnhancedEdgeStrategy.optimize_for_market_condition()`

2. **SearchVBT is used when**:
   - Researching optimal indicator settings via `research_indicator_settings()`
   - Looking up VectorBT documentation for specific functions
   - Finding parameter ranges and best practices from the knowledge base

3. **Direct API Calls are used when**:
   - ChatVBT initialization fails (API key issues, missing dependencies)
   - The `direct_chat()` function is explicitly called
   - Advanced prompts require bypassing VectorBT's formatting

### AI Integration Points

The system integrates AI at several critical decision points:

1. **Parameter Optimization**:
   - Before optimization: Get advice on parameter ranges
   - During optimization: Analyze intermediate results
   - After optimization: Interpret results and suggest improvements

2. **Strategy Development**:
   - Generate new strategy components
   - Enhance existing factor calculations
   - Create adaptive strategies for different market conditions

3. **Error Handling and Debugging**:
   - Analyze portfolio creation failures
   - Debug data processing issues
   - Suggest fixes for implementation errors

### Using With Cursor for Strategy Enhancement

Cursor is an AI-powered IDE that can help you enhance and debug the trading system. Here are detailed workflows for common tasks:

#### 1. Enhancing an Existing Strategy

**Workflow**:
1. Open the strategy file (e.g., `edge_multi_factor.py`) in Cursor
2. Use Cursor to analyze the existing factor functions
3. Ask Cursor to suggest improvements based on financial principles
4. Test modifications with `test_edge_assistant.py`

**Example Query to Cursor**:
```
Analyze the RSI implementation in create_volatility_regime_indicator() and suggest improvements for detecting market regime changes more accurately.
```

#### 2. Debugging VectorBT Integration Issues

**Workflow**:
1. If you encounter ChatVBT failures, examine the error logs
2. Open related files in Cursor (e.g., `wfo_edge_strategy.py`)
3. Focus on the `setup_chat_provider()` and `ask_chat_model()` functions
4. Ask Cursor to analyze potential failure points

**Example Query to Cursor**:
```
Analyze the setup_chat_provider() function and help me identify why the ChatVBT initialization is failing with a KeyError on 'kb'.
```

#### 3. Adding New Technical Indicators

**Workflow**:
1. Research the indicator you want to add
2. Use Cursor to help implement it in the appropriate file
3. Update the `EdgeMultiFactorStrategy` class to incorporate the new indicator
4. Use direct chat or ChatVBT to test parameter ranges

**Example Query to Cursor**:
```
Help me implement the Chaikin Money Flow (CMF) indicator and integrate it into the EdgeMultiFactorStrategy class.
```

#### 4. Creating Custom AI Prompts

The system can be enhanced with better prompts for specific tasks:

1. Open `wfo_edge_strategy.py` in Cursor
2. Locate the `get_optimization_advice_from_chat_model()` function
3. Ask Cursor to help improve the prompt template
4. Test with `test_direct_chat.py`

**Example Implementation**:
```python
def get_optimization_advice_from_chat_model():
    """Get optimization advice from ChatVBT."""
    prompt = """
    [SYSTEM: You are an expert in algorithmic trading and optimization.
    Your task is to analyze the current market conditions for BTC/USD and recommend 
    parameter ranges for the Edge Multi-Factor Strategy.
    
    Format your response as a JSON object with these sections:
    1. market_analysis - Brief analysis of current market conditions
    2. parameter_recommendations - Specific parameter ranges for RSI, BB, and ATR
    3. optimization_strategy - Suggested approach for parameter optimization
    
    Make your recommendations specific and actionable.]
    
    Please analyze the current market conditions for BTC/USD and provide 
    optimization advice for our trading strategy.
    """
    
    response = ask_chat_model(prompt)
    return response
```

### Practical Example: Market Regime Detection Enhancement

Here's a complete example of using the AI system to enhance the trading strategy:

1. **Question Definition**:
   "How can we improve market regime detection in our strategy?"

2. **Using SearchVBT**:
   ```python
   from scripts.strategies.edge_strategy_assistant import EdgeStrategyAssistant
   
   assistant = EdgeStrategyAssistant()
   search_results = assistant.search_vectorbt_docs("market regime detection methods")
   print(search_results)
   ```

3. **Using ChatVBT for Analysis**:
   ```python
   from scripts.strategies.wfo_edge_strategy import ask_chat_model
   
   # Current implementation
   with open("scripts/strategies/edge_multi_factor.py", "r") as f:
       current_code = f.read()
   
   prompt = f"""
   Here is our current market regime detection code:
   ```python
   {current_code}
   ```
   
   How can we improve this to better detect market regime changes? Please suggest specific code modifications.
   """
   
   suggestions = ask_chat_model(prompt)
   print(suggestions)
   ```

4. **Implementing Changes with Cursor**:
   - Open `edge_multi_factor.py` in Cursor
   - Ask Cursor to implement the suggested changes
   - Test the modified strategy

### Debugging Optimization Issues

When encountering optimization problems (like the "name 'create_portfolio' is not defined" error), use this workflow:

1. **Error Analysis**:
   ```python
   from scripts.strategies.wfo_edge_strategy import debug_with_chat
   
   error_message = "name 'create_portfolio' is not defined"
   context = {
       "function": "optimize_parameters",
       "file": "wfo_edge_strategy.py",
       "line": 899
   }
   
   analysis = debug_with_chat(error_message, context)
   print(analysis)
   ```

2. **Solution Implementation with Cursor**:
   - Open the file in Cursor
   - Ask Cursor to analyze the error and suggest fixes
   - Apply the changes and test again

## Key Components

### EdgeMultiFactorStrategy

Base trading strategy that combines multiple technical indicators:

```python
strategy = EdgeMultiFactorStrategy(
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
```

### EnhancedEdgeStrategy

Extends the base strategy with AI capabilities:

```python
enhanced = EnhancedEdgeStrategy()
suggestions = enhanced.get_parameter_suggestions()
adaptive_strategy = enhanced.generate_adaptive_strategy()
```

### Strategy Optimization

Example of optimizing parameters for specific market conditions:

```python
# Optimize for trending markets
trending_params = enhanced.optimize_for_market_condition("trending")

# Optimize for ranging markets
ranging_params = enhanced.optimize_for_market_condition("ranging")

# Optimize for volatile markets
volatile_params = enhanced.optimize_for_market_condition("volatile")
```

### Market Analysis

Analyze current market conditions:

```python
from scripts.strategies.chat_optimize_edge_strategy import analyze_current_market

analysis = analyze_current_market("BTC-USD")
print(analysis["market_data"])
print(analysis["analysis"]["market_regime"])
```

### Direct Chat API Integration

The system now supports direct interaction with language models via API, bypassing VectorBT's built-in chat functionality when needed:

```python
from scripts.strategies.wfo_edge_strategy import ask_chat_model

# Simple query
response = ask_chat_model("What is the best RSI period for BTC?")

# With context
market_data = {"price": 50000, "volatility": "high", "trend": "bullish"}
response = ask_chat_model(
    "Suggest trading parameters for the current market", 
    context=market_data
)
```

## Advanced Features

### Adaptive Strategy Generation

Generate a strategy that adapts to changing market conditions:

```python
from scripts.strategies.edge_strategy_assistant import EnhancedEdgeStrategy

strategy = EnhancedEdgeStrategy()
adaptive_code = strategy.generate_adaptive_strategy()

# Save to file
with open("adaptive_strategy.py", "w") as f:
    f.write(adaptive_code)
```

### Indicator Research

Research optimal settings for technical indicators:

```python
rsi_research = strategy.research_indicator_settings("RSI")
bb_research = strategy.research_indicator_settings("Bollinger Bands")
```

### Backtest Analysis

Analyze backtest results with AI:

```python
backtest_results = {
    "total_return": 78.5,
    "sharpe_ratio": 1.8,
    "max_drawdown": -15.2,
    "win_rate": 0.65
}

analysis = strategy.analyze_backtest_results(backtest_results)
```

## Configuration

Key configuration options:

- **Parameters Space**: Defined in `run_walk_forward_optimization()` in `wfo_edge_strategy.py`
- **Data Settings**: Configure symbol, timeframe and lookback period
- **Optimization Settings**: Number of trials, performance metrics, and validation criteria
- **Chat Models**: Configure API keys in the .env file

## Extending the System

### Adding New Indicators

To add new indicators to the strategy:

1. Add parameters to the `EdgeMultiFactorStrategy` class
2. Update the signal generation logic in `generate_signals()`
3. Add the new parameters to the parameter space in `run_walk_forward_optimization()`

### Creating Custom Strategies

Create your own strategy by extending the base classes:

```python
class MyCustomStrategy(EdgeMultiFactorStrategy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add custom initialization
        
    def generate_signals(self, data):
        # Custom signal generation logic
        pass
```

## Troubleshooting

Common issues and solutions:

### API Key Issues
- Ensure API keys are properly set in the .env file
- The system will automatically use OPENROUTER_API_KEY if OPENAI_API_KEY is not available
- Verify that your API keys are valid and have sufficient credits
- Check error logs for specific API-related errors

### VectorBT Issues
- Make sure VectorBT Pro is properly licensed and installed
- Check for version compatibility issues
- Ensure data inputs are in the correct format
- Note that all column names should be lowercase (`close` instead of `Close`)
- If ChatVBT fails, the system will fall back to direct API calls

### WFO Process Issues
- If the WFO process fails with no valid parameters, try:
  - Relaxing the portfolio validation criteria
  - Expanding the parameter search space
  - Checking for data quality issues
  - Running with fewer splits or larger training windows
- Check the log files for specific error messages

### Dependencies
- The system now automatically checks for and installs required dependencies
- If you encounter missing package errors, manually install them with:
  ```bash
  pip install lmdbm vectorbtpro pandas-ta
  ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.