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
- **Robust Performance Metrics**: Handles vectorbt API inconsistencies for reliable trade analysis

## Version History

### v1.2.0 (Current)
- Fixed vectorbt PnL column name inconsistency ('PnL' vs 'pnl')
- Enhanced performance metrics calculation with robust fallbacks
- Added comprehensive system flow documentation
- Improved error handling in portfolio creation
- Added test scripts for performance metrics validation

### v1.1.0
- Added direct Chat API integration as fallback for ChatVBT
- Implemented AI-assisted strategy enhancement
- Added parameter stability analysis in walk-forward optimization
- Enhanced market regime detection

### v1.0.0
- Initial release with Edge Multi-Factor Strategy
- Basic walk-forward optimization implementation
- VectorBT Pro integration for backtesting
- Basic AI assistance features

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
- The system handles vectorbt's inconsistent column naming ('PnL' vs 'pnl') for trade records

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

## Performance Metrics and Trade Analysis

The system incorporates a robust implementation for calculating trade performance metrics, addressing several key challenges in vectorbt's API.

### VectorBT Trade Record Processing

VectorBT provides trade records through its Portfolio object, but has inconsistencies in how it exposes data:

1. **Column Name Inconsistencies**:
   - The `records_readable` DataFrame uses uppercase 'PnL' for trade profit/loss values
   - Many vectorbt methods and properties use lowercase 'pnl' 
   - Our system handles both formats seamlessly with a unified interface

2. **Access Method Handling**:
   - Some metrics are exposed as properties, others as methods
   - Count can be either a property or a callable method depending on context
   - Our implementation intelligently handles all variations

### Metrics Calculation Flow

The system calculates performance metrics through a multi-stage process:

1. **Data Collection**: 
   ```
   Portfolio Object → Trade Records → Performance Calculation
   ```

2. **Column Detection**:
   ```python
   # Detect available PnL column format
   pnl_col = None
   if 'PnL' in trades_df.columns:
       pnl_col = 'PnL'
   elif 'pnl' in trades_df.columns:
       pnl_col = 'pnl'
   ```

3. **Metric Extraction**:
   - Basic metrics (Sharpe, Calmar, max drawdown) from portfolio stats
   - Trade-specific metrics (win rate, profit factor) from trade records
   - Risk metrics from portfolio risk functions

4. **Fallback Mechanisms**:
   - If PnL columns aren't found, defaults to zero values
   - If trade counts aren't available, uses DataFrame length
   - If a specific calculation fails, provides sensible defaults

### Performance Metrics Implementation

The `calculate_performance_metrics` function in `wfo_edge_strategy.py` offers a comprehensive approach:

1. **Portfolio Validity Check**: Returns default values if portfolio is None
2. **Flexible Statistics Access**: Handles stats as both property and method
3. **Method/Property Detection**: Uses callable detection to handle count, win_rate, etc.
4. **Column Name Resolution**: Handles both 'PnL' and 'pnl' column formats
5. **Error Handling**: Graceful fallback if any step fails
6. **Comprehensive Metrics**: Calculates all essential trading metrics

This implementation ensures consistent performance analysis regardless of vectorbt API changes or data format variations.

### Testing and Verification

A dedicated test script (`test_wfo_strategy.py`) verifies the metrics calculation:

1. **Uppercase Test**: Verifies handling of 'PnL' (uppercase) column
2. **Lowercase Test**: Verifies handling of 'pnl' (lowercase) column
3. **Missing Column Test**: Validates fallback behavior when PnL data isn't available

The test results confirmed that all formats are handled correctly, with accurate calculations of:
- Win rate (66.7% for test data)
- Profit factor (5.0 for test data)
- Average trade metrics (6.67 for test data)

### System Design Improvements

Several architectural improvements enhance the system's robustness:

1. **Type Safety**: Properly handles both numeric and boolean data types
2. **Error Recovery**: Graceful degradation when data is missing
3. **Logging**: Comprehensive logging for troubleshooting
4. **AI-Assisted Debugging**: Integration with chat models for error analysis

The system now reliably calculates performance metrics in all scenarios, maintaining consistency across different data formats and API behaviors.

## System Flow and Component Integration

The Crypto Trading Bot integrates multiple components in a cohesive workflow that handles data acquisition, strategy implementation, performance measurement, and AI-assisted optimization. Here's a detailed breakdown of the entire system flow:

### 1. Data Flow

```
Data Source → Data Fetcher → Data Processing → Strategy Implementation → Backtesting → Performance Analysis
```

#### Data Acquisition Process
1. **Data Source Selection**:
   - Historical data from Coinbase via API
   - Data cached locally for performance
   - Configurable timeframes and symbols

2. **Data Transformation**:
   - Normalization of column names to lowercase
   - Calculation of derived values (returns, volatility)
   - Splitting into training/testing periods for walk-forward optimization

3. **Data Enhancement**:
   - Addition of technical indicators
   - Market regime identification
   - Volume profile analysis

### 2. Strategy Execution Flow

```
Market Data → Technical Indicators → Signal Generation → Position Sizing → Portfolio Construction → Performance Metrics
```

#### Signal Generation Process
1. **Indicator Calculation**:
   - Calculate RSI, Bollinger Bands, and volatility indicators
   - Apply multiple timeframe analysis when configured
   - Generate boolean signal arrays (entry/exit conditions)

2. **Signal Combination**:
   - Combine multiple indicators using configurable weights
   - Apply regime filters for market condition adaptivity
   - Generate final long/short signals

3. **Position Management**:
   - Calculate position sizes based on risk parameters
   - Implement stop-loss and take-profit levels
   - Handle entry/exit timing logic

### 3. Optimization Flow

```
Parameter Space Definition → Optimization Trial → Portfolio Creation → Performance Evaluation → Parameter Refinement
```

#### Walk-Forward Optimization Process
1. **Split Definition**:
   - Divide historical data into multiple windows
   - Configure in-sample/out-of-sample periods
   - Setup overlapping windows for robustness

2. **Parameter Search**:
   - Define parameter search space
   - Generate parameter combinations
   - Use Optuna for efficient optimization

3. **Performance Assessment**:
   - Calculate key metrics (Sharpe, Calmar, win rate)
   - Filter valid parameter sets
   - Evaluate parameter stability across periods

4. **Parameter Finalization**:
   - Select optimal parameters
   - Balance performance and stability
   - Generate final parameter recommendations

### 4. PnL Calculation and Metrics Flow

```
Portfolio → Trade Records → PnL Extraction → Metric Calculation → Performance Dashboard
```

#### Performance Measurement Process
1. **Trade Identification**:
   - Extract entry and exit points from signals
   - Match entry/exit pairs into complete trades
   - Calculate trade durations and frequencies

2. **PnL Handling**:
   - Extract PnL values, handling both uppercase and lowercase column names
   - Separate winning and losing trades
   - Calculate gross profit and loss values

3. **Metric Production**:
   - Calculate standard metrics (Sharpe, drawdown)
   - Calculate trading-specific metrics (win rate, profit factor)
   - Produce risk metrics (VaR, volatility)

4. **Result Processing**:
   - Format metrics for reporting
   - Log detailed results for each portfolio
   - Generate comparison tables across parameter sets

### 5. AI Integration Flow

```
Trading Context → AI System → Model Selection → Query Processing → Strategy Enhancement
```

#### AI Assistance Process
1. **Context Preparation**:
   - Gather market data and performance metrics
   - Formulate precise queries for AI models
   - Include relevant context for accurate responses

2. **Model Selection**:
   - Choose between ChatVBT (primary) and direct API (fallback)
   - Select appropriate model based on task complexity
   - Handle API authentication and rate limiting

3. **Response Processing**:
   - Parse AI responses into structured formats
   - Extract actionable recommendations
   - Integrate suggestions into strategy parameters

4. **Continuous Improvement**:
   - Log AI interactions for review
   - Feedback loop to improve prompts
   - Evolution of strategy based on AI insights

### 6. End-to-End System Integration

The complete system integrates these flows into a cohesive process:

1. **Initialization Phase**:
   - Load configurations and environment variables
   - Initialize logging and error tracking
   - Setup data connections and API authentication

2. **Data Preparation Phase**:
   - Fetch and process historical data
   - Prepare market analysis for AI context
   - Generate training/testing splits

3. **Optimization Phase**:
   - Generate initial parameter suggestions (AI-assisted)
   - Run walk-forward optimization across splits
   - Analyze parameter stability and performance

4. **Execution Phase**:
   - Implement strategy with optimized parameters
   - Generate trading signals for current market
   - Calculate position sizes and risk metrics

5. **Analysis Phase**:
   - Calculate performance metrics with robust PnL handling
   - Evaluate strategy effectiveness across market regimes
   - Generate reports and visualizations

6. **Improvement Phase**:
   - AI-assisted analysis of results
   - Recommendations for strategy enhancements
   - Implementation of improvements in next iteration

This integrated workflow creates a robust trading system that leverages both technical analysis and AI to adapt to changing market conditions while maintaining reliable performance measurement across all components.

### Testing Performance Metrics Calculation

You can easily test the performance metrics calculation with your own data using this code snippet:

```python
import pandas as pd
import numpy as np
from scripts.strategies.wfo_edge_strategy import calculate_performance_metrics

# Create a dummy portfolio with your own test data
class TestPortfolio:
    def __init__(self, trade_data, stats_data=None):
        self.stats = stats_data or {
            'total_return': 0.05,
            'max_drawdown': -0.02,
            'sharpe_ratio': 1.2,
            'calmar_ratio': 2.5
        }
        
        class TestTrades:
            def __init__(self, trade_data):
                # You can use either 'PnL' or 'pnl' - the system handles both
                self.records_readable = pd.DataFrame(trade_data)
        
        self.trades = TestTrades(trade_data)

# Test with uppercase 'PnL'
test_data_upper = {'PnL': [10, -5, 15, -8, 20]}
portfolio_upper = TestPortfolio(test_data_upper)
metrics_upper = calculate_performance_metrics(portfolio_upper)
print(f"Metrics with uppercase 'PnL': {metrics_upper}")

# Test with lowercase 'pnl'
test_data_lower = {'pnl': [10, -5, 15, -8, 20]}
portfolio_lower = TestPortfolio(test_data_lower)
metrics_lower = calculate_performance_metrics(portfolio_lower)
print(f"Metrics with lowercase 'pnl': {metrics_lower}")

# Both should yield identical results
```

This code allows you to test the system's ability to handle different column name formats with custom trade data. You can extend it to test more complex scenarios by modifying the trade data structure.

## Future Roadmap

The Crypto Trading Bot system is continuously evolving. Here are the planned enhancements for upcoming releases:

### Upcoming in v1.3.0
- **Live Trading Integration**: Implementation of real-time trading through exchange APIs
- **Enhanced Risk Management**: Dynamic position sizing based on market volatility
- **Multi-Asset Strategies**: Support for trading multiple cryptocurrencies with correlated risk management
- **WebSocket API**: Real-time data streaming for faster system responsiveness

### Planned for v1.4.0
- **Strategy Backtesting UI**: Web interface for visualizing backtest results
- **Custom Indicator Builder**: AI-assisted creation of custom technical indicators
- **Portfolio-Wide Optimization**: Optimize parameters across multiple assets simultaneously
- **Sentiment Analysis Integration**: Incorporate market sentiment from news and social media

### Long-term Vision
- **Automated Strategy Evolution**: Self-improving strategies using reinforcement learning
- **Market Regime Detection**: Advanced classification of market conditions using machine learning
- **Cross-Exchange Arbitrage**: Identify and exploit price differences across exchanges
- **Options-Based Strategies**: Incorporate options pricing models for enhanced risk management

These roadmap items represent our commitment to continuously improve the system based on user feedback and market developments. Contributions aligned with these goals are particularly welcome.