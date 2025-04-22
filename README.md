# Crypto Trading Bot with AI-Powered Optimization and Live Trading

A comprehensive cryptocurrency trading bot with walk-forward optimization, AI-assisted strategy development, and live trading via Coinbase Advanced API. Built with VectorBT Pro and OpenAI/OpenRouter APIs for backtesting and optimization, and Coinbase Advanced API for market data and order execution.

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)

## Features

- **Edge Multi-Factor Strategy**: Combines RSI, Bollinger Bands, and volatility indicators for robust trading signals
- **Walk-Forward Optimization**: Dynamic parameter optimization across multiple market regimes
- **AI Strategy Assistant**: Uses LLMs to help optimize strategies and analyze market conditions
- **Enhanced Parameter Suggestions**: Market-aware parameter recommendations with validation and performance verification
- **Backtest Analysis**: Comprehensive performance metrics and visualization
- **Parameter Research**: AI-assisted research for optimal indicator settings
- **Adaptive Strategies**: Generation of strategies that adapt to changing market conditions
- **Direct Chat API Integration**: Flexible communication with LLMs via OpenRouter/OpenAI APIs
- **Robust Performance Metrics**: Handles vectorbt API inconsistencies for reliable trade analysis
- **Live Trading Integration**: Real-time trading through Coinbase Advanced API
- **WebSocket Market Data**: Real-time data streaming for responsive strategy execution
- **Task-Driven Development**: Structured development workflow using task-master for efficient implementation

## Version History

### v1.4.0 (Current)
- Added Coinbase Advanced API integration for live trading
- Implemented WebSocket API for real-time market data
- Added order management system with risk controls
- Integrated user configuration options for trading preferences
- Added position and portfolio monitoring
- Implemented task-master for structured development workflow

### v1.3.0
- Added Enhanced Parameter Suggestion system with market context awareness
- Implemented parameter validation against predefined constraints
- Added performance validation to verify AI suggestions actually improve results
- Created comparison framework to evaluate different optimization approaches
- Added detailed market regime analysis for more targeted parameter suggestions

### v1.2.1
- Added parameter type validation to ensure window parameters are integers
- Implemented robust parameter conversion in test workflows 
- Fixed NumbaTypeError in rolling_std calculation during optimization
- Enhanced end-to-end test for better verification of AI suggestions
- Improved parameter mapping from AI suggestions to strategy implementation

### v1.2.0
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
- Coinbase Advanced API key and secret for live trading
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
# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Coinbase API Keys 
COINBASE_API_KEY="organizations/{org_id}/apiKeys/{key_id}"
COINBASE_API_SECRET="-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n"
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

4. **Live Trading System**: Real-time execution through Coinbase
   - REST API client for order management
   - WebSocket API for real-time market data
   - Account management and position tracking
   - Risk control and trade execution

## Getting Started

### Backtesting and Optimization

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

### Live Trading

To run the live trading system with the optimized strategy:

```bash
python scripts/live_trading/run_trading_system.py
```

To monitor active positions and account status:

```bash
python scripts/live_trading/monitor_positions.py
```

To test the Coinbase API connection:

```bash
python scripts/live_trading/test_api_connection.py
```

### Understanding the Results

Analysis results are saved in the `analysis_results` directory:
- Complete strategy analysis in JSON format
- Backtesting results with performance metrics
- Market analysis and recommendations
- Adaptive strategy implementations

Trading results are saved in the `trading_logs` directory:
- Order history and execution details
- Position performance metrics
- Account balance history
- WebSocket data logs

## Task-Master Development Workflow

This project uses Task-Master for structured, task-driven development. This system helps manage complex implementation tasks, track dependencies, and ensure systematic progress.

### Task Management Overview

Task-Master provides a comprehensive CLI for managing development tasks:

```bash
# List all tasks with status
task-master list

# Show the next task to work on
task-master next

# View details of a specific task
task-master show <task_id>

# Mark a task as completed
task-master set-status --id=<task_id> --status=done
```

### Development Process

The recommended workflow for contributing to this project:

1. **Start Session**: Begin by reviewing current tasks and their dependencies
   ```bash
   task-master list
   ```

2. **Select Next Task**: Choose the highest priority task with all dependencies satisfied
   ```bash
   task-master next
   ```

3. **Understand Requirements**: Review the task's details and test strategy
   ```bash
   task-master show <task_id>
   ```

4. **Analyze Complexity**: For complex tasks, perform complexity analysis
   ```bash
   task-master analyze-complexity --id=<task_id> --research
   ```

5. **Break Down Complex Tasks**: Divide large tasks into manageable subtasks
   ```bash
   task-master expand --id=<task_id> --num=5 --research
   ```

6. **Implementation**: Develop the required code following the task specifications
   - Follow the implementation details in the task description
   - Use the recommended approach from subtask breakdown
   - Adhere to project coding standards and patterns

7. **Testing**: Verify implementation against the test strategy
   - Implement unit tests as required
   - Ensure all existing tests pass
   - Verify any performance metrics or requirements

8. **Mark Progress**: Update task status when completed
   ```bash
   task-master set-status --id=<task_id> --status=done
   ```

9. **Handle Implementation Changes**: If your implementation differs from the plan
   ```bash
   task-master update --from=<task_id> --prompt="Changed implementation approach to use WebSockets instead of polling"
   ```

### Determining the Next Task

The `task-master next` command identifies the most appropriate task to work on using a sophisticated prioritization algorithm:

```bash
task-master next
```

This command:
- Identifies tasks with all dependencies satisfied
- Prioritizes tasks by priority level (high, medium, low)
- Considers dependency chains to optimize development flow
- Shows comprehensive task information for immediate implementation

The output includes:
- Task details and description
- Implementation guidance
- Subtasks (if they exist)
- Suggested next actions

This is the recommended way to start each development session, as it ensures you're always working on the most important task that can be implemented right now.

### Common Workflow Patterns

Depending on the development phase, use these established workflow patterns:

#### For New Features:

```bash
# Begin by checking what to work on
task-master next

# Understand the task details
task-master show <task_id>

# For complex tasks, analyze and break down
task-master analyze-complexity --id=<task_id> --research
task-master expand --id=<task_id> --research

# As you complete subtasks, mark them done
task-master set-status --id=<task_id>.<subtask_num> --status=done

# When the entire feature is complete
task-master set-status --id=<task_id> --status=done
```

#### For Bug Fixes:

```bash
# Add a new bug fix task
task-master add-task --prompt="Fix WebSocket reconnection issue after network interruption" --priority=high

# Or link to an existing task
task-master show <related_task_id>

# When fixed, mark as complete
task-master set-status --id=<task_id> --status=done
```

#### For Refactoring:

```bash
# Create refactoring tasks
task-master add-task --prompt="Refactor the position management system for improved reliability" --dependencies=<dependent_task_ids>

# Check for related tasks that might be affected
task-master list --status=pending

# After refactoring, update dependent tasks if implementation changed
task-master update --from=<first_affected_task> --prompt="Position management now uses event-driven architecture"
```

### Task Structure

Each task in this project contains the following components:

- **ID**: Unique identifier for the task
- **Title**: Brief description of the task
- **Status**: Current state (pending, in_progress, done, or deferred)
- **Dependencies**: List of tasks that must be completed first
- **Priority**: Importance level (high, medium, low)
- **Description**: Brief summary of what the task involves
- **Details**: In-depth implementation instructions
- **Test Strategy**: Approach for verifying correct implementation

### Task File Format

Task files are generated in the `tasks/` directory and follow this standardized format:

```
# Task ID: 5
# Title: Implement WebSocket Connection Handler
# Status: pending
# Dependencies: 3, 4
# Priority: high
# Description: Create a robust WebSocket connection handler for real-time market data.

# Details:
Implement a WebSocket connection handler class that will:
1. Establish secure connections to Coinbase Advanced API
2. Handle authentication using JWT tokens
3. Implement automatic reconnection with exponential backoff
4. Process incoming messages and route to appropriate handlers
5. Provide clean error handling and logging

The implementation should follow the WebSocket client pattern described in the Coinbase API documentation.
Use the abstract factory pattern to allow for future exchange integrations.

# Test Strategy:
1. Create unit tests verifying connection establishment
2. Test authentication flow with mock credentials
3. Verify reconnection logic works with simulated disconnects
4. Ensure message routing correctly delivers to registered handlers
5. Test error conditions and verify appropriate logging/handling
```

Task files can be viewed directly or through the task-master CLI:

```bash
# View task file directly
cat tasks/task_5.md

# Or use the task-master CLI
task-master show 5
```

All tasks are also centrally defined in `tasks/tasks.json`, which serves as the source of truth for the project's task structure.

### Managing Task Dependencies

The project maintains a clear dependency structure:

```bash
# Add a dependency relationship
task-master add-dependency --id=<task_id> --depends-on=<dependency_id>

# Remove a dependency relationship
task-master remove-dependency --id=<task_id> --depends-on=<dependency_id>

# Validate the dependency structure
task-master validate-dependencies

# Fix any invalid dependencies
task-master fix-dependencies
```

### Adding New Tasks

To add new functionality to the project:

```bash
# Add a new task with AI assistance
task-master add-task --prompt="Implement real-time position dashboard with React" --dependencies=12,15 --priority=high
```

### Integration with Cursor AI

When using Cursor AI to assist with development:

1. **Provide Task Context**: Share the task file with Cursor AI to provide implementation context
   ```bash
   # First, view the task
   task-master show <task_id> > task_details.md
   
   # Then share this with Cursor AI
   ```

2. **Include Dependencies**: Mention dependency relationships to ensure proper integration
   ```bash
   task-master show <dependency_id> > dependency_details.md
   ```

3. **Verify Implementation**: Use Cursor AI to review implementation against task requirements
   ```python
   # Example prompt to Cursor AI
   """
   I've implemented the feature according to task #5. Here's my implementation:
   
   [paste code]
   
   The task requirements are:
   [paste from task_details.md]
   
   Does my implementation meet all the requirements? Are there any improvements needed?
   """
   ```

### Task-Master Environment Configuration

Task-Master requires certain environment variables for optimal functioning. Add these to your `.env` file alongside the other configuration variables:

```
# Task-Master Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
MODEL=claude-3-7-sonnet-20250219
MAX_TOKENS=4000
TEMPERATURE=0.7
DEBUG=false
LOG_LEVEL=info
DEFAULT_SUBTASKS=3
DEFAULT_PRIORITY=medium
PROJECT_NAME=Crypto Trading Bot
PROJECT_VERSION=1.4.0
PERPLEXITY_API_KEY=your_perplexity_api_key_here  # Optional, for research features
```

These variables control:

- **API Access**: Anthropic API key for Claude model access
- **Model Settings**: Which Claude model to use and its parameters
- **Development Settings**: Logging levels and debugging options
- **Default Values**: Standard configurations for new tasks
- **Project Metadata**: Information used in generated documentation
- **Research Capabilities**: Optional Perplexity API integration for enhanced research

You can modify these settings to suit your specific development requirements. For example:
- Use `MODEL=claude-3-opus-20240229` for more complex task expansion
- Set `MAX_TOKENS=8000` for more detailed responses
- Use `DEBUG=true` and `LOG_LEVEL=debug` for troubleshooting
- Adjust `DEFAULT_SUBTASKS` based on your typical task complexity

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

## Coinbase API Integration

The system integrates with Coinbase Advanced API for live trading and market data access:

### REST API Client

The REST API client handles order management, account queries, and trading execution:

```python
from coinbase.rest import RESTClient
from trading_system.config import get_api_credentials

# Load credentials from secure environment
api_key, api_secret = get_api_credentials()

# Initialize the client
client = RESTClient(api_key=api_key, api_secret=api_secret)

# Get account information
accounts = client.get_accounts()

# Place a market order
order = client.market_order_buy(
    client_order_id="", # Empty string auto-generates a unique ID
    product_id="BTC-USD", 
    quote_size="100"  # $100 worth of BTC
)
```

### WebSocket Client

The WebSocket client provides real-time market data for responsive trading:

```python
from coinbase.websocket import WSClient
from trading_system.config import get_api_credentials

# Load credentials from secure environment
api_key, api_secret = get_api_credentials()

# Define message handler
def on_message(msg):
    # Process real-time data
    print(msg)

# Initialize the client
client = WSClient(
    api_key=api_key, 
    api_secret=api_secret, 
    on_message=on_message
)

# Connect and subscribe to market data
client.open()
client.ticker(product_ids=["BTC-USD", "ETH-USD"])

# Keep the connection running with error handling
try:
    client.run_forever_with_exception_check()
except Exception as e:
    print(f"WebSocket error: {e}")
    client.close()
```

### Order Execution Engine

The order execution engine translates strategy signals into actual trades:

```python
from trading_system.execution import OrderExecutor
from trading_system.config import get_trade_settings

# Initialize with risk parameters
executor = OrderExecutor(
    rest_client=client,
    risk_per_trade=0.02,  # 2% risk per trade
    max_positions=3       # Maximum of 3 open positions
)

# Execute a trade based on strategy signal
executor.execute_signal(
    symbol="BTC-USD",
    signal_type="LONG",
    entry_price=50000.0,
    stop_loss=49000.0,
    take_profit=52000.0
)
```

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

### LiveTradingSystem

Manages the live trading operations including data feeds, execution, and monitoring:

```python
from trading_system.live import LiveTradingSystem
from trading_system.strategies import EdgeMultiFactorStrategy

# Create strategy with optimized parameters
strategy = EdgeMultiFactorStrategy(**optimized_params)

# Initialize trading system
trading_system = LiveTradingSystem(
    strategy=strategy,
    api_key=api_key,
    api_secret=api_secret,
    symbols=["BTC-USD", "ETH-USD"],
    risk_manager=default_risk_manager
)

# Start the trading system
trading_system.start()

# Run for a specified time or until stopped
trading_system.run_until_stopped()
```

## Configuration

Key configuration options:

- **Parameters Space**: Defined in `run_walk_forward_optimization()` in `wfo_edge_strategy.py`
- **Data Settings**: Configure symbol, timeframe and lookback period
- **Optimization Settings**: Number of trials, performance metrics, and validation criteria
- **Chat Models**: Configure API keys in the .env file
- **Trading Parameters**: Configure risk settings, order types, and trading schedule
- **API Settings**: Configure API keys, rate limits, and timeout settings

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

### Adding Additional Exchanges

The system can be extended to support additional exchanges:

1. Create a new exchange adapter class in `trading_system/exchanges/`
2. Implement the required methods (place_order, get_account, etc.)
3. Update the configuration to include the new exchange

## Troubleshooting

Common issues and solutions:

### API Key Issues
- Ensure API keys are properly set in the .env file
- The system will automatically use OPENROUTER_API_KEY if OPENAI_API_KEY is not available
- Verify that your API keys are valid and have sufficient credits
- Ensure Coinbase API keys have the correct permissions enabled
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

### Coinbase API Issues
- Check that the API key is in the correct format: `"organizations/{org_id}/apiKeys/{key_id}"`
- Ensure the API secret is properly formatted with newlines: `"-----BEGIN EC PRIVATE KEY-----\nYOUR KEY\n-----END EC PRIVATE KEY-----\n"`
- Verify that the API key has the appropriate permissions for the actions you're attempting
- For WebSocket connection issues, check your network configuration and firewall settings
- Enable verbose logging for detailed debugging information: `client = RESTClient(verbose=True)`

### Dependencies
- The system now automatically checks for and installs required dependencies
- If you encounter missing package errors, manually install them with:
  ```bash
  pip install lmdbm vectorbtpro pandas-ta coinbase-advanced-py
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

## System Flow and Component Integration

The Crypto Trading Bot integrates multiple components in a cohesive workflow that handles data acquisition, strategy implementation, performance measurement, and AI-assisted optimization. Here's a detailed breakdown of the entire system flow:

### 1. Data Flow

```
Data Source → Data Fetcher → Data Processing → Strategy Implementation → Backtesting/Live Trading → Performance Analysis
```

#### Data Acquisition Process
1. **Data Source Selection**:
   - Historical data from Coinbase via API
   - Real-time data from WebSocket connections
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
Market Data → Technical Indicators → Signal Generation → Position Sizing → Order Execution → Performance Tracking
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

### 3. Live Trading Flow

```
Strategy Signals → Risk Management → Order Creation → API Communication → Order Execution → Position Monitoring
```

#### Trade Execution Process
1. **Order Preparation**:
   - Validate signal against current market conditions
   - Apply risk management rules (position size, max positions)
   - Calculate appropriate order parameters (size, price)

2. **API Interaction**:
   - Create and sign API requests with proper JWT authentication
   - Submit orders via REST API
   - Handle response status and confirmation

3. **Position Tracking**:
   - Monitor open positions through WebSocket feeds
   - Update stop-loss/take-profit levels as needed
   - Record execution details for performance analysis

### 4. AI Integration Flow

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

### 5. Integrated Parameter Optimization Workflow (NEW)

The system now incorporates a two-stage optimization process:

1.  **Enhanced Parameter Suggestion (Initial Tuning):**
    *   Run `python scripts/strategies/enhanced_parameter_suggestions.py`.
    *   This script analyzes the current market conditions (over the last 30 days) to identify the market regime.
    *   It generates strategy parameter suggestions tailored to this regime.
    *   These suggestions are then validated against a longer historical backtest (365 days by default).
    *   If the backtest shows improved performance (Return and Sharpe Ratio) compared to baseline parameters, the suggested parameters are saved to `config/optimized_strategy_params.json`.

2.  **Walk-Forward Optimization (Fine-tuning & Adaptation):**
    *   Run `python scripts/strategies/wfo_edge_strategy.py`.
    *   Before optimizing each walk-forward window, the script attempts to load the parameters from `config/optimized_strategy_params.json`.
    *   If found, these parameters are used as the *initial guess* (first trial) for the Optuna optimization process within that specific WFO window.
    *   If the file is not found, Optuna starts its search from scratch for that window.
    *   The WFO process then proceeds as usual, optimizing parameters for each training split and evaluating on the subsequent out-of-sample period.

**Benefits of this workflow:**

*   **Better Starting Point:** WFO starts its optimization search from a more informed position based on recent market analysis and long-term validation, potentially leading to faster convergence and better final parameters.
*   **Adaptation + Robustness:** Combines long-term validation (from the suggestion script) with rolling window adaptation (from WFO).
*   **Flexibility:** You can run the suggestion script periodically to update the baseline optimized parameters used by WFO.

## Future Roadmap

The Crypto Trading Bot system is continuously evolving. Here are the planned enhancements for upcoming releases:

### Upcoming in v1.5.0
- **Multi-Exchange Support**: Integration with additional cryptocurrency exchanges
- **Enhanced Position Management**: Dynamic adjustment of positions based on real-time market conditions
- **Portfolio Optimization**: Cross-asset allocation optimization for improved risk-adjusted returns
- **Improved Data Analytics**: Advanced visualization and reporting of trading performance

### Planned for v2.0.0
- **Strategy Marketplace**: Platform for sharing and subscribing to trading strategies
- **Web Dashboard**: Complete web interface for monitoring and controlling the trading system
- **Custom Indicator Builder**: AI-assisted creation of custom technical indicators
- **Sentiment Analysis Integration**: Incorporate market sentiment from news and social media

### Long-term Vision
- **Automated Strategy Evolution**: Self-improving strategies using reinforcement learning
- **Advanced Market Regime Detection**: ML-based classification of market conditions
- **Cross-Exchange Arbitrage**: Identify and exploit price differences across exchanges
- **Options and Derivatives Integration**: Support for advanced trading instruments

These roadmap items represent our commitment to continuously improve the system based on user feedback and market developments. Contributions aligned with these goals are particularly welcome.