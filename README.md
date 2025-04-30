# Crypto Trading Bot with WFO and Task-Driven Development

A comprehensive cryptocurrency trading bot featuring advanced Walk-Forward Optimization (WFO) and Edge Multi-Factor strategies, designed with Coinbase Advanced API integration for paper trading and live execution. This project utilizes a task-driven development workflow managed by the Task-Master CLI.

## Features

### Core Trading Strategy

- **Edge Multi-Factor Strategy**: A sophisticated trading system that combines multiple technical indicators, market context awareness, and adaptive parameterization to identify high-probability trading opportunities across different market regimes.
  - **Primary Signal Indicators**: RSI, Bollinger Bands, Moving Averages, and ATR
  - **Signal Validation**: Supply/Demand Zones, Trend Analysis, and ADX confirmation
  - **Signal Strictness Modes**: Configurable STRICT, BALANCED, and RELAXED signal generation approaches
  - **Market Regime Detection**: Automated classification of trending vs. ranging market conditions

### System Architecture

- **Modular Design**: Core strategy logic separated from execution and optimization components
- **Robust Error Handling**: Comprehensive utilities for data validation and exception management
- **Dependency Management**: Elimination of circular dependencies through dynamic imports
- **Market Regime Classification**: Enhanced regime detection with percentage calculations and safe fallbacks

### Risk Management

- **Advanced Position Sizing Module**: Comprehensive sizing framework combining risk percentage, volatility (ATR), market regime, zone confidence, and optional Kelly criterion
- **Regime-Aware Position Adjustments**: Automatically modifies position size based on detected market regime (larger in trending, smaller in ranging)
- **Risk-Based Calculation**: Determines optimal size based on account equity and stop-loss distance
- **Comprehensive Stop-Loss System**: Fixed percentage, ATR-based, and zone-based exit mechanisms
- **Global Risk Controls**: Maximum concurrent positions, drawdown circuit breakers, and correlation-based exposure limits

### Framework & Infrastructure

- **Walk-Forward Optimization Engine**: Systematic approach to strategy validation with time-series partitioning and parameter stability analysis
- **Coinbase Advanced API Integration**: Robust WebSocket and REST API connectivity with secure JWT authentication
- **Supply/Demand Zone Detection**: Algorithmic identification of high-probability support/resistance zones
- **Backtesting System**: Historical performance simulation with realistic market conditions modeling
- **Task-Master CLI**: AI-powered task-driven development workflow for planning and tracking
- **AWS Lambda Integration**: Framework for potential serverless deployment
- **Session Persistence**: Mechanisms for saving and restoring system state
- **Web UI Dashboard (Planned)**: Future interface for monitoring system status

## Walk-Forward Optimization (WFO) Framework

The project implements a sophisticated Walk-Forward Optimization framework to ensure strategy robustness and adaptability across changing market conditions:

### Methodology

1. **Data Partitioning**:
   - Historical data is systematically divided into multiple time windows
   - Each window contains in-sample (training) and out-of-sample (testing) periods
   - Windows may overlap to increase statistical significance while preventing overfitting

2. **Optimization Process**:
   - Parameters are optimized on in-sample data for each window using Optuna
   - Multi-objective optimization balances return, Sharpe ratio, drawdown, and win rate
   - Parameter stability is measured across windows to prevent curve-fitting
   - Asset-specific optimizations adapt parameters to individual market characteristics

3. **Validation and Regime Analysis**:
   - Out-of-sample performance is evaluated using a comprehensive metrics suite
   - Market regimes are classified (trending vs. ranging) for regime-specific parameter sets
   - Monte Carlo simulations assess strategy robustness to randomness
   - Robustness ratio calculations identify strategies with consistent performance

4. **Implementation Features**:
   - Circular dependency prevention through robust architecture
   - Error-resistant design with comprehensive validation and fallbacks
   - Configurable optimization metrics and validation criteria
   - Parallel processing for efficient multi-asset optimization

## Version History

### v0.5.6 (Current - April 2025)
- **Advanced Position Sizing Implementation**:
  - Developed comprehensive position sizing module with multiple calculation methods
  - Implemented regime-aware position sizing with market condition adaptation
  - Created ATR-based volatility adjustment to reduce size in choppy markets
  - Added zone confidence integration to improve position sizing for high-quality entries
  - Integrated optional Kelly Criterion for mathematical position optimization
  - Created extensive unit testing for all position sizing components
  - Integrated position sizing into backtest runner and WFO evaluation modules

### v0.5.5 (April 2025)
- **Architectural Robustness Improvements**:
  - Created comprehensive utils.py module with robust data validation and error handling
  - Fixed circular dependencies throughout the codebase using dynamic imports
  - Resolved regime detection issues with proper percentage calculations
  - Added safe attribute/method access patterns for vectorbtpro compatibility
  - Implemented consistent error handling with detailed logging
- **Enhanced Signal Generation**:
  - Developed balanced signal framework with configurable strictness levels (STRICT, BALANCED, RELAXED)
  - Implemented regime-aware parameter adaptation
  - Added visual comparison tools for signal validation
  - Fixed signal determinism issues for reproducible testing
  - Created summary statistics to quantify signal differences by regime

### v0.5.0
- Enhanced Walk-Forward Optimization with parameter stability analysis and robustness checks
- Implemented advanced risk management protocols including dynamic position sizing
- Integrated Trading Journal functionality for better performance tracking
- Developed AI assistance features for enhanced parameter suggestions

### v0.4.0
- Enabled live trading capabilities via Coinbase Advanced API.
- Integrated WebSocket for real-time market data streams.
- Enhanced backtesting engine with Monte Carlo simulation features.
- Added multi-timeframe analysis capabilities for signal confirmation.

### v0.3.0
- Implemented the core Edge Multi-Factor Strategy.
- Developed the initial Supply/Demand zone detection algorithm.
- Set up SQLite database for persistent market data storage.
- Created the initial framework for AWS Lambda deployment.

### v0.2.0
- Built the backtesting system for historical performance analysis.
- Implemented the foundational risk management framework with position sizing.
- Developed algorithms for basic candlestick pattern detection.
- Integrated initial Coinbase API connectivity.

### v0.1.0
- Initialized project structure and base architecture using FastAPI.
- Implemented basic data fetching and normalization processes.
- Created the configuration management system using environment variables.
- Set up foundational logging and monitoring components.

## System Requirements

- **Python**: Version 3.10 or higher.
- **Database**: SQLite (default for local storage). Other databases can be configured.
- **Operating System**: Linux, macOS, or Windows.
- **API Credentials**: Valid Coinbase Advanced API key, secret (PEM format), and passphrase.
- **AI Assistance**: Anthropic API key (required for Task-Master's AI features).
- **Dependencies**: See `requirements.txt` (includes FastAPI, Uvicorn, httpx, websockets, pandas, numpy, sqlalchemy, pydantic-settings, coinbase-advanced-py, etc.).

## Environment Setup and Installation

Follow these steps to set up the development environment:

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and Activate Virtual Environment**:
    ```bash
    python -m venv venv
    # On Linux/macOS
    source venv/bin/activate
    # On Windows
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the project root directory. Add the following variables, replacing placeholders with your actual credentials. **Ensure the PEM secret key includes the `\n` characters exactly as shown for newlines.**

    ```dotenv
    # Coinbase Advanced API Credentials
    COINBASE_API_KEY="organizations/{org_id}/apiKeys/{key_id}"  # Replace with your Key Name/Path
    # Ensure the secret includes literal \n for newlines
    COINBASE_API_SECRET="-----BEGIN EC PRIVATE KEY-----\nYOUR_PRIVATE_KEY_LINE_1\nYOUR_PRIVATE_KEY_LINE_2\n...\n-----END EC PRIVATE KEY-----\n"
    COINBASE_API_PASSPHRASE="your_passphrase_here" # If you set one during key creation

    # Task-Master AI Configuration
    ANTHROPIC_API_KEY="sk-ant-api03-..." # Replace with your Anthropic key

    # Optional Task-Master Settings (defaults shown)
    # MODEL="claude-3-7-sonnet-20250219"
    # MAX_TOKENS=4000
    # TEMPERATURE=0.7
    # DEBUG=false
    # LOG_LEVEL=info
    # PROJECT_NAME="Crypto Trading Bot"
    # PROJECT_VERSION="0.5.0"

    # Database Configuration (default is SQLite)
    # DATABASE_URL="sqlite:///./trading_data.db"

    # Other System Settings (optional)
    # LOG_FILE_PATH="./logs/trading_bot.log"
    # MAX_CONCURRENT_TASKS=4
    ```

5.  **Initialize Database**:
    Run the database migration script (if applicable, e.g., using Alembic or Django migrations) or ensure the application creates the SQLite file on first run.
    ```bash
    # Example command (if using Alembic)
    # alembic upgrade head
    ```

6.  **Verify Setup**:
    Run basic tests or a simple command to confirm installation and configuration.
    ```bash
    # Example: Run Task-Master list command
    task-master list
    ```

## Architecture Overview: The MCP Server and Core Components

The system is built around a central Market Control Panel (MCP) server implemented using FastAPI. This server coordinates data fetching, strategy execution, risk management, and order placement.

### 1. MCP Server (FastAPI Application)

The core of the system, responsible for:

-   **REST API Endpoints**: Provides endpoints for configuration, status monitoring, manual control, and data retrieval.
    -   `/status`: Get current system status, active strategies, positions.
    -   `/config`: View and potentially update system configuration.
    -   `/trades`: Retrieve historical trade data.
    -   `/orders`: View open and historical orders.
    -   `/control`: Endpoints for starting/stopping strategies, pausing trading.
-   **WebSocket Integration**: Manages WebSocket connections to Coinbase for real-time data and potentially exposes WebSocket endpoints for UI clients.
-   **Authentication & Security**: Handles API key validation and secure communication.
-   **Configuration Management**: Loads settings from `.env` file and validates them using Pydantic.
-   **Task Scheduling**: Manages periodic tasks like data fetching, strategy evaluation, and risk checks.
-   **Logging**: Centralized logging configuration for all components.
-   **Error Handling**: Global error handling middleware.

### 2. Data Fetcher & Management
Responsible for acquiring and managing market data:

-   **Coinbase API Client**: A dedicated module (`coinbase_client.py`) handles interactions with the Coinbase Advanced API.
    -   **Authentication**: Implements JWT (ES256) signing for all requests.
    -   **REST Requests**: Functions for fetching historical data, account info, orders.
    -   **WebSocket Client**: Connects to Coinbase WebSocket feeds (e.g., `level2`, `ticker`, `user`) for real-time data.
        -   Handles subscription management.
        -   Implements heartbeat checks and automatic reconnection logic with exponential backoff.
    -   **Rate Limiting**: Respects Coinbase API rate limits.
-   **OHLCV Data System**: Manages candle data.
    -   **Fetching**: Retrieves historical OHLCV data using the REST client.
    -   **Normalization**: Cleans data (handles NaNs, outliers), ensures consistent timestamp formats (UTC).
    -   **Storage**: Persists data in the configured database (SQLite default) using SQLAlchemy or similar ORM. Includes indexing for efficient querying.
    -   **Multi-Timeframe**: Manages data for various intervals (15m, 1H, 4H, etc.), potentially resampling lower timeframes.
    -   **Maintenance**: Includes logic for detecting and filling data gaps, managing data freshness.
s, S/D Zones, Trend, and Volatility components.
    -   Uses configurable parameters optimized via WFO.
    -   Includes signal generation logic based on confluence rules.
-   **Exploratory Strategy Framework**: Allows testing new ideas in isolation.
-   **Signal Generation**: Logic to produce buy/sell/hold signals base
### 3. Strategy Implementation Module
Contains the trading logic:

-   **Edge Multi-Factor Strategy**: The core strategy implementation.
    -   Combines signals from RSI, Bollinger Bandd on strategy rules.
-   **Parameter Management**: Handles loading and applying strategy parameters.

### 4. Supply/Demand Zone Detection
Identifies potential support and resistance areas:

-   **Pattern Recognition**: Detects Drop-Base-Rally (Demand) and Rally-Base-Drop (Supply) patterns.
-   **Scoring**: Assigns quality scores based on 'freshness' (time since formation) and 'confidence' (pattern characteristics).
-   **Multi-Timeframe Confluence**: Looks for zones aligning across different timeframes.
-   **Status Tracking**: Updates zone status (untested, tested, broken) based on price interaction.

### 5. Walk-Forward Optimization (WFO) Engine
Optimizes and validates strategy parameters:

-   **Time-Series Partitioning**: Splits historical data into sequential training (in-sample) and validation (out-of-sample) windows.
-   **Parameter Optimization**: Uses search algorithms (grid search, genetic algorithms) to find optimal parameters within each in-sample window based on defined metrics (e.g., Sharpe Ratio, Profit Factor).
-   **Out-of-Sample Validation**: Tests the optimized parameters on the subsequent unseen out-of-sample window to check for overfitting.
-   **Parameter Stability Analysis**: Analyzes how parameters change across different optimization windows to assess robustness.
-   **Reporting**: Generates detailed reports on performance, stability, and recommended parameters.
-   **Resumable Processing**: Saves state to allow long optimizations to be paused and resumed.

### 6. Risk Management System
Enforces comprehensive risk controls:

-   **Advanced Position Sizing**: Integrated position sizing module with multiple calculation approaches:
    -   **Risk-Based Sizing**: Calculates optimal position size based on account equity risk percentage and stop-loss distance
    -   **Regime-Aware Multipliers**: Adapts position size to market conditions (larger in trending, smaller in ranging)
    -   **Volatility Adjustment**: Uses ATR to reduce position size in volatile conditions
    -   **Zone Confidence Integration**: Increases position size for entries with higher zone confidence
    -   **Kelly Criterion (Optional)**: Mathematical optimization based on win rate and win/loss ratio
-   **Dynamic Stop-Loss Calculation**: Determines optimal stop levels using ATR multiples, zone boundaries, or fixed percentages
-   **Adaptive Exit Logic**: Modifies exit criteria based on detected market regime
-   **Take-Profit Targeting**: Sets profit targets based on risk-reward ratios or key technical levels (e.g., opposing S/D zones).
-   **Circuit Breakers**: Implements rules to temporarily halt trading based on conditions like consecutive losses, daily drawdown limits, or extreme volatility spikes.
-   **Account Monitoring**: Tracks overall account exposure and drawdown.

### 7. Order Execution Framework
Manages the process of placing and tracking trades:

-   **Order Placement**: Functions to submit various order types (Market, Limit, Stop-Limit) via the Coinbase API Client.
-   **Bracket Orders**: Implements logic to place an entry order along with linked stop-loss and take-profit orders (often using OCO - One-Cancels-the-Other logic if supported, or managed locally).
-   **Signal Confirmation**: Validates signals against risk management rules and market conditions before placing trades.
-   **Order Tracking**: Monitors the status of open orders (pending, filled, cancelled, rejected) by querying the API or using WebSocket user channel updates.
-   **Position Monitoring**: Tracks open positions, calculating real-time P&L.
-   **Emergency Controls**: Provides functionality to quickly cancel all open orders and potentially flatten all positions (kill-switch).

### 8. Performance Analysis & Reporting
Calculates and presents trading performance:

-   **Metrics Calculation**: Computes standard metrics like Win Rate, Profit Factor, Sharpe Ratio, Sortino Ratio, Maximum Drawdown, Average Win/Loss, etc.
-   **Trade Logging**: Records detailed information about each trade (entry/exit times, prices, size, P&L, reason for entry/exit, associated signal data).
-   **Reporting Engine**: Generates performance summaries (e.g., daily, weekly, monthly) and visualizations (equity curves, drawdown charts).
-   **Data Export**: Allows exporting trade logs and performance data.

### 9. Session Persistence & Recovery
Ensures system resilience:

-   **State Storage**: Saves critical system state (open orders, positions, strategy parameters, current data pointers) to a persistent store (e.g., database or file).
-   **Serialization**: Converts in-memory objects to a storable format.
-   **Recovery Logic**: On startup, loads the last known state and reconciles it with the exchange (fetching current orders/positions) to resume operations accurately after a crash or restart.

### 10. Task-Master CLI
Manages the development workflow:

-   **Task Management**: Parses, lists, updates, and tracks development tasks stored in `tasks.json`.
-   **AI Assistance**: Uses an LLM (via Anthropic API) for tasks like complexity analysis, task breakdown (`expand`), and generating new tasks (`add-task`).
-   **Dependency Handling**: Manages and validates dependencies between tasks.
-   **Reporting**: Generates markdown reports and diagrams visualizing the task structure and progress.

**For full command details and usage examples, please refer to the [Task-Master Documentation](./scripts/README.md).**

#### Key Task-Master Commands

-   `task-master list`: Display all project tasks with status, ID, title, and dependencies.
    -   `--status=<status>`: Filter tasks by status (e.g., `pending`, `in_progress`, `done`).
    -   `--with-subtasks`: Show subtasks nested under parent tasks.
-   `task-master next`: Show the recommended next task to work on, based on dependencies, priority, and status.
-   `task-master show <id>`: View detailed information about a specific task (including description, details, test strategy, and subtasks). Use dot notation for subtasks (e.g., `task-master show 6.3`).
-   `task-master set-status --id=<id> --status=<status>`: Update the status of a specific task or subtask.
    -   Common statuses: `pending`, `in_progress`, `done`, `deferred`, `blocked`.
-   `task-master expand --id=<id>`: Break down a complex task into smaller, manageable subtasks using AI assistance.
    -   `--num=<number>`: Specify the desired number of subtasks.
    -   `--research`: Leverage Perplexity AI for research-backed expansion (requires PERPLEXITY_API_KEY).
    -   `--prompt="<context>"`: Provide additional context for the AI.
    -   `--force`: Regenerate subtasks even if they already exist.
-   `task-master analyze-complexity`: Evaluate the complexity of pending tasks using AI and generate recommendations for expansion.
    -   `--research`: Use Perplexity AI for analysis.
-   `task-master complexity-report`: Display the results of the complexity analysis in a formatted way.
-   `task-master add-task --prompt="<description>"`: Add a new task based on a natural language description using AI.
    -   `--dependencies=<ids>`: Specify dependencies (comma-separated).
    -   `--priority=<level>`: Set priority (high, medium, low).
-   `task-master add-dependency --id=<id> --depends-on=<id>`: Add a dependency relationship.
-   `task-master remove-dependency --id=<id> --depends-on=<id>`: Remove a dependency.
-   `task-master fix-dependencies`: Automatically find and remove invalid dependency references.
-   `task-master generate`: Regenerate individual task files in the `tasks/` directory based on `tasks.json` (useful after manual edits or dependency changes).
-   `task-master init`: Initialize Task-Master structure in a new project.

## Development Process with Task-Master

This project uses a task-driven development workflow powered by the Task-Master CLI. This approach facilitates structured development, better planning, and AI-assisted productivity.

### Key Task Workflow

1.  **Start Session**: Run `task-master list` to review the current state of tasks.
2.  **Select Task**: Use `task-master next` to identify the next logical task based on dependencies and priority.
3.  **Understand Requirements**: Run `task-master show <id>` for the selected task to fully understand the scope, details, and testing strategy.
4.  **Analyze & Expand**: If the task is complex (check `analyze-complexity` report or use judgment), break it down using `task-master expand --id=<id> --research`.
5.  **Begin Implementation**: Set the task status to `in_progress` using `task-master set-status --id=<id> --status=in_progress`. Work on the code, following the task details.
6.  **Test Rigorously**: Verify the implementation against the specified `testStrategy` in the task details. Write unit/integration tests as needed.
7.  **Mark Complete**: Once implemented and tested, update the status to `done` using `task-master set-status --id=<id> --status=done`.
8.  **Handle Changes**: If implementation details deviate significantly, potentially affecting future tasks, consider using `task-master update --from=<future_task_id> --prompt="<explanation>"` to adjust subsequent tasks.

### Contributing to the Project

Follow the task-driven workflow:

1.  Identify an available task (`task-master list --status=pending` or `task-master next`).
2.  Ensure all its dependencies are `done`.
3.  Claim the task by setting its status to `in_progress`.
4.  Implement the feature/fix according to task details and existing code standards.
5.  Write or update tests as per the task's `testStrategy`.
6.  Update any relevant documentation.
7.  Commit changes with clear messages, potentially referencing the task ID.
8.  Submit a Pull Request for review (if applicable).
9.  Once merged/verified, mark the task as `done`.

## Strategy Implementation Guide

The Edge Multi-Factor Strategy combines multiple technical indicators and market factors to create a robust trading system with adaptive parameter optimization. This approach provides a systematic framework for identifying high-probability trading opportunities while managing risk.

### Core Strategy Components

1.  **RSI Component**: Identifies overbought/oversold conditions
    -   Configurable period settings (default: 14, 21, and 50-period)
    -   Dynamic thresholds based on market volatility
    -   Divergence detection between price and RSI
    -   Signal filtering based on RSI slope and rate of change
    -   Multiple timeframe confirmation (higher TF for trend, lower TF for entry)

2.  **Bollinger Band Component**: Detects volatility contractions and expansions
    -   Adaptive standard deviation multipliers (1.5, 2.0, 2.5, 3.0)
    -   Band squeeze detection for breakout anticipation
    -   Mean reversion signals from band touches
    -   Dynamic band width tracking for volatility regime detection
    -   Trend direction confirmation using band slope

3.  **Supply/Demand Zones**: Identifies key support/resistance levels
    -   Pattern recognition for rally-base-drop and drop-base-rally formations
    -   Zone quality scoring based on formation characteristics
    -   Zone "freshness" tracking with score decay over time
    -   Multi-timeframe zone confluence detection
    -   Dynamic zone strength adjustment based on price interactions
    -   Zone visualization with color-coding by strength

4.  **Trend Analysis**: Determines market direction across timeframes
    -   Multiple moving average systems (SMA, EMA, VWMA)
    -   Higher timeframe trend alignment checks
    -   Pullback detection within established trends
    -   Trend strength metrics using ADX and similar indicators
    -   Market structure analysis (higher highs/higher lows, etc.)
    -   Range detection for sideways markets

5.  **Volatility Adjustment**: Adapts parameters based on current volatility
    -   ATR-based volatility measurement across multiple periods
    -   Parameter scaling based on volatility regime
    -   Position sizing adjustment for high-volatility environments
    -   Stop-loss distance calculation using ATR multiples
    -   Volatility breakout detection
    -   Rejection of signals during extreme volatility events

### Strategy Signal Generation

The Edge Multi-Factor Strategy generates signals through the following process:

1.  **Initial Filtering**: Screen for basic conditions across all components
    -   RSI values within specified ranges
    -   Price relative to Bollinger Bands
    -   Proximity to Supply/Demand zones
    -   Current volatility assessment

2.  **Confluence Analysis**: Combine signals from multiple components
    -   Minimum required confluence score configuration
    -   Weighted scoring based on historical component performance
    -   Priority rules for conflicting signals
    -   Time-based weighting (recent signals given higher weight)

3.  **Entry Confirmation**: Final validation before trade execution
    -   Volume confirmation requirements
    -   Minimum risk/reward ratio check
    -   Pattern completion verification
    -   Rejection criteria for false signals
    -   Timeframe alignment confirmation

4.  **Signal Strength Calculation**: Determine position sizing multiplier
    -   Base position size from risk management rules
    -   Adjustment factor from signal strength score
    -   Maximum position size caps
    -   Signal decay handling for delayed execution

### Exploratory Strategy Framework

The project includes an exploratory strategy framework that enables systematic investigation of new trading concepts before incorporation into the main Edge Multi-Factor Strategy:

1.  **Isolated Component Testing**: Test individual indicators or concepts
    -   Standalone backtesting environment
    -   Performance comparison against benchmark strategies
    -   Sensitivity analysis for parameter variations
    -   Correlation analysis with existing components

2.  **Concept Validation Process**:
    -   Define clear hypothesis for the trading concept
    -   Create minimal viable implementation
    -   Backtest across multiple markets and timeframes
    -   Evaluate using consistent performance metrics
    -   Document findings in standardized format

3.  **Integration Pathway**:
    -   Test correlation with existing strategy components
    -   Determine optimal weighting in combined strategy
    -   Perform incremental backtesting during integration
    -   Monitor live performance in parallel before full integration
    -   Establish fallback mechanisms for unexpected behavior

4.  **Exploratory Strategy Toolbox**:
    -   Reusable testing frameworks for quick concept validation
    -   Benchmarking system for performance comparison
    -   Statistical analysis tools for result validation
    -   Parameter grid search automation
    -   Result visualization and reporting tools

### Walk-Forward Optimization Process

The WFO process follows a systematic approach to validate strategy performance while avoiding curve-fitting:

1.  **Data Preparation and Segmentation**
    -   Divide historical data into multiple in-sample/out-of-sample segments
    -   Configure segment sizes appropriately (typical IS/OS ratio: 70/30)
    -   Ensure sufficient history for meaningful optimization (typically 6+ months)
    -   Apply data cleaning procedures (handling gaps, outliers, etc.)
    -   Normalize data features when necessary

2.  **In-Sample Optimization Process**:
    -   Define parameter search space with appropriate ranges
    -   For each in-sample segment:
        -   Apply grid search or genetic algorithm optimization
        -   Optimize parameters for primary metrics (Sharpe, profit factor, etc.)
        -   Apply ancillary metrics as filters (min. trades, max drawdown, etc.)
        -   Rank parameter sets by combined performance score
        -   Select top N parameter sets for out-of-sample testing

3.  **Out-of-Sample Validation**:
    -   Apply optimal in-sample parameters to corresponding out-of-sample data
    -   Calculate performance metrics on unseen data
    -   Measure performance degradation from in-sample to out-of-sample
    -   Flag excessive degradation as potential overfitting
    -   Store all results for stability analysis

4.  **Parameter Stability Analysis**:
    -   Track how optimal parameters change across segments
    -   Calculate stability metrics for each parameter:
        -   Standard deviation normalized to parameter range
        -   Maximum parameter deviation percentage
        -   Consistency of direction in parameter changes
    -   Identify most stable parameters across all segments
    -   Assign stability weights to each parameter

5.  **Robustness Evaluation**:
    -   Test performance across various market conditions
        -   Trending vs. ranging markets
        -   High vs. low volatility periods
        -   Bull vs. bear market phases
    -   Analyze sensitivity to parameter variations
    -   Perform Monte Carlo simulations with parameter perturbations
    -   Evaluate strategy resilience to execution delays and slippage

6.  **Final Parameter Selection**:
    -   Combine performance metrics with stability scores
    -   Weigh recent segments more heavily than older ones
    -   Calculate expected performance ranges rather than point estimates
    -   Select parameters with best balance of performance and stability
    -   Document all findings with visualizations and summary statistics

### WFO Implementation Tips

1.  **Avoiding Curve-Fitting**:
    -   Use sufficient historical data spanning multiple market regimes
    -   Limit parameter count to prevent overfitting (parsimony principle)
    -   Implement strict out-of-sample validation
    -   Apply complexity penalties to parameter sets
    -   Watch for excessive performance degradation in out-of-sample testing

2.  **Computational Optimization**:
    -   Implement parallel processing for faster optimization
    -   Use smart search algorithms (Bayesian optimization, particle swarm)
    -   Store intermediate results to enable resumable processing
    -   Apply early stopping for clearly underperforming parameter sets
    -   Use parameter sensitivity analysis to reduce search space

3.  **Results Interpretation**:
    -   Focus on consistency across segments rather than maximum performance
    -   Look for clusters of parameters that perform well
    -   Pay attention to parameter stability in recent market conditions
    -   Consider the trade-off between performance and robustness
    -   Analyze failure modes in poor-performing segments

4.  **Practical Implementation**:
    -   Schedule regular re-optimization (monthly or quarterly)
    -   Implement gradual parameter updates rather than sudden changes
    -   Monitor tracking error between expected and actual performance
    -   Create alerts for significant market regime changes
    -   Document all optimization runs with detailed metadata

## Configuration Requirements

The system requires proper configuration of:

1.  **Coinbase Advanced API Credentials**: With appropriate permissions.
    -   Required permissions: view, trade, transfer management (adjust as needed for security).
    -   JWT authentication with ES256 algorithm must be used.
    -   Private key must be in PEM format with literal `\n` characters for newlines in the `.env` file.
    -   Ensure system clock is synchronized (e.g., using NTP) for JWT timestamp validation.

2.  **Risk Parameters**: Defined in configuration files or environment variables.
    -   Maximum position size per trade (e.g., `$1000` or `5%` of equity).
    -   Account risk percentage per trade (e.g., `1%`).
    -   Maximum drawdown threshold (e.g., `10%` daily, `25%` total).
    -   Circuit breaker conditions (e.g., halt after `5` consecutive losses, halt if daily loss exceeds `3%`).
    -   Trade frequency limits (e.g., max `10` trades per day).
    -   Correlation exposure limits (e.g., max `20%` exposure to highly correlated assets).

3.  **Strategy Parameters**: Specific settings for the Edge Multi-Factor strategy.
    -   RSI periods and overbought/oversold levels.
    -   Bollinger Band period and standard deviation multipliers.
    -   Supply/Demand zone detection settings (strength thresholds, decay rates).
    -   Trend identification parameters (MA lengths, timeframe weights).
    -   Signal confirmation rules (min confluence score, volume multipliers).

4.  **Backtesting Settings**: Configuration for running simulations.
    -   Historical data date ranges (ensure sufficient length).
    -   WFO segment sizes (in-sample days, out-of-sample days, step days).
    -   Exchange fee structure (maker/taker fees).
    -   Slippage model (e.g., fixed points, percentage, volatility-based).
    -   Performance metrics to track and report.
    -   Benchmark strategy or index for comparison.
    -   Monte Carlo simulation settings (number of runs, parameter perturbation ranges).

## Current Project Status

Based on the `tasks.json` file, the project has the following status:

-   **Completed** (9 tasks):
    -   Project scaffold and Coinbase API integration (Task 1)
    -   OHLCV data retrieval and storage (Task 2)
    -   Supply/Demand zone detection algorithm (Task 3)
    -   Risk management system (Task 4)
    -   Order execution framework (Task 5)
    -   AWS Lambda deployment framework (Conceptual - Task related to deployment)
    -   Data visualization dashboard (Conceptual - Task related to UI/Reporting)
    -   Strategy monitoring system (Conceptual - Part of execution/logging)
    -   Trading Journal Integration (Task 12 - Basic logging likely part of Task 7)

-   **In Progress** (4 tasks):
    -   Dry-run and backtest modes with Edge Multi-Factor optimization (Task 6)
    -   Signal generation algorithm refinement (Part of Task 3/Strategy Implementation)
    -   AI-assisted parameter optimization (Part of AI Assistance / WFO)
    -   Multi-exchange integration (Likely a future task, not explicitly listed as in progress in provided JSON)

*Note: Status mapping assumes conceptual links where direct task IDs aren't listed.* 

## Troubleshooting Common Issues

### API Authentication Problems
-   **Key Format**: Verify `COINBASE_API_SECRET` in `.env` has literal `\n` for newlines. Ensure no extra quotes or spaces.
-   **Permissions**: Confirm the API key has the necessary permissions (view, trade) enabled in Coinbase.
-   **Clock Skew**: Ensure the server's clock is synchronized (e.g., using NTP) for JWT timestamp validation.

### Backtesting Performance & Accuracy
-   **Data Quality**: Check historical data for gaps, duplicate entries, or outliers. Implement cleaning procedures.
-   **Lookahead Bias**: Ensure indicators and strategy logic only use data available *at or before* the current simulation time step. Be careful with pandas functions that might implicitly use future data.
-   **Slippage & Fees**: Use realistic models. Fixed slippage is often too simplistic; consider percentage-based or volatility-adjusted models. Include accurate commission costs.
-   **Sample Size**: Ensure enough trades are generated in backtests for statistical significance. Low trade counts make results unreliable.
-   **Benchmark**: Compare results against a relevant benchmark (e.g., buy-and-hold for the asset) to assess value-add.
-   **WFO Settings**: Ensure appropriate WFO segment lengths. Too short segments may not capture market dynamics; too long may obscure parameter drift.

### Optimization Challenges (WFO)
-   **Overfitting**: Monitor the performance drop between in-sample and out-of-sample results. Large drops indicate overfitting. Reduce parameter complexity or increase data/segment length.
-   **Computational Cost**: WFO is intensive. Use parallel processing, efficient code (vectorization with numpy/pandas), and consider cloud resources. Implement checkpointing.
-   **Parameter Stability**: If optimal parameters vary wildly between segments, the strategy might not be robust. Favor parameter sets that show consistency.
-   **Local Optima**: Grid search can be trapped in local optima. Consider more advanced methods like genetic algorithms or Bayesian optimization if needed.
-   **Search Space**: Ensure the defined parameter ranges are sensible and cover potentially optimal values without being excessively large.

### Task Management (Task-Master)
-   **API Key**: Ensure `ANTHROPIC_API_KEY` is correctly set in `.env` for AI features.
-   **Dependencies**: Run `task-master fix-dependencies` if you encounter errors related to task linkage after manual edits to `tasks.json`.
-   **Task Files**: Remember that `task-master generate` overwrites files in `tasks/`. Keep primary edits in `tasks.json`.
-   **Complexity**: Use `analyze-complexity` and `expand` to break down large tasks *before* starting implementation to improve planning.
-   **Status Updates**: Keep task statuses (`set-status`) updated frequently to reflect actual progress accurately.

## Position Sizing Implementation

The position sizing module (`position_sizing.py`) offers these key features:

1. **Risk-Based Position Sizing**: `calculate_risk_based_size()`
   - Calculates optimal position size based on risk amount and stop distance
   - Enforces minimum and maximum size constraints
   - Includes validation and error handling for robust calculation

2. **Regime-Specific Position Multipliers**: `get_regime_position_multiplier()`
   - Automatically adjusts position size based on market regime
   - Default multipliers: 1.0 for trending, 0.75 for ranging markets
   - Supports custom multiplier configuration for fine-tuned control

3. **Integrated Position Sizing**: `calculate_integrated_position_size()`
   - Combines all sizing approaches into a comprehensive calculation
   - Integrates regime awareness, ATR volatility, and zone confidence
   - Optional Kelly Criterion integration for mathematical optimization
   - Detailed parameter validation and error handling

4. **Backtest & WFO Integration**:
   - Seamlessly integrated into the backtest runner and WFO evaluation modules
   - Dynamic position sizing in backtests with detailed logging
   - Supports both fixed size and dynamic sizing modes

## Strategy Development Workflow

Follow this structured process for developing and refining trading strategies within this framework:

1.  **Research Phase**
    -   Identify a market inefficiency or pattern hypothesis.
    -   Review relevant research papers, articles, or existing indicators.
    -   Define the core logic, required inputs, and expected outputs/signals.
    -   Determine suitable markets and timeframes for the concept.

2.  **Prototyping (using Exploratory Framework)**
    -   Implement the core logic as a standalone component.
    -   Use the exploratory backtesting tools to perform initial validation on historical data.
    -   Identify preliminary parameter ranges that show promise.
    -   Document initial findings, including potential weaknesses or edge cases.

3.  **Rigorous Testing & Optimization**
    -   Perform Walk-Forward Optimization on the isolated component or strategy.
    -   Analyze performance across diverse market conditions (trends, ranges, volatility levels).
    -   Evaluate parameter stability and robustness.
    -   Conduct sensitivity analysis around optimal parameters.
    -   Compare results against benchmarks.
    -   Document all results, configurations, and findings thoroughly.

4.  **Integration (if successful)**
    -   Analyze the correlation of the new component's signals with the existing Edge Multi-Factor Strategy.
    -   Determine how to best combine the signals (e.g., as a filter, a confirmation, or an additive factor).
    -   Define interaction rules and weighting within the combined strategy.
    -   Re-run WFO on the integrated strategy.
    -   Test the integrated strategy in dry-run mode before considering live deployment.

5.  **Monitoring and Refinement (Live/Dry-Run)**
    -   Continuously monitor the strategy's performance against WFO expectations (tracking error).
    -   Use the trading journal and performance metrics to identify strengths and weaknesses.
    -   Analyze losing trades and periods of underperformance.
    -   Periodically re-run WFO (e.g., quarterly) to adapt to changing market conditions.
    -   Make data-driven adjustments to parameters or logic based on ongoing monitoring.

## License

This project is licensed under the MIT License - see the LICENSE file for details.