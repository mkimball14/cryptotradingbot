# Crypto Trading Bot Framework

A comprehensive framework for developing, backtesting, and deploying cryptocurrency trading bots, with a focus on the Coinbase Advanced Trade API.

## Overview

This project provides a structured environment for building automated trading strategies. It includes components for:

*   **Exchange Integration:** Connecting to Coinbase via REST API (JWT Auth using `.env`) and WebSocket for market data and order execution within the main `app/`.
*   **Data Management:** Fetching (using `coinbase` SDK directly in backtest scripts), processing, caching (`data/cache/`), storing (SQLAlchemy - planned/optional), and retrieving historical OHLCV data.
*   **Trading Strategies:** Implementing custom trading logic. Currently focused on an RSI strategy within the advanced backtesting script.
*   **Signal Generation & Confirmation:** Detecting supply/demand zones and using technical indicators (RSI, MACD, Volume Profile) to validate signals (core app components).
*   **Order Execution:** Placing market, limit, and potentially bracket orders with simulated (dry-run) and live execution capabilities (core app components).
*   **Risk Management:** Calculating position sizes, stop-losses (including ATR-based stops in backtests), and implementing risk controls.
*   **Backtesting:** Evaluating strategy performance using `vectorbtpro`, featuring Walk-Forward Optimization (WFO) in the primary backtesting script `scripts/backtest_rsi_vbt_pro.py`.
*   **API Interface:** Exposing core functionalities through a FastAPI web server (`app/main.py`).
*   **Development Workflow:** Utilizes a task-driven approach managed via the `task-master` CLI tool (see `.cursor/rules/dev_workflow.mdc`).

## Project Structure

*   **`app/`**: Main application source code (FastAPI server, core logic, basic strategies).
    *   `main.py`: FastAPI application entry point.
    *   `core/`: Core application logic (API clients using `.env`, data handling, basic execution, strategies interface, basic backtesting, risk).
    *   `models/`: Pydantic and dataclass definitions.
    *   `routers/`: FastAPI endpoints.
    *   `strategies/`: Specific trading strategy implementations for the core app.
    *   `database/`: SQLAlchemy models and database interaction setup (within `app/core/`).
*   **`tests/`**: Unit and integration tests (using `pytest`).
*   **`scripts/`**: Standalone utility and analysis scripts. Includes the primary `vectorbtpro` backtesting script (`backtest_rsi_vbt_pro.py`).
*   **`data/cache/`**: Cached historical data fetched from Coinbase (add to `.gitignore`).
*   **`logs/`**: Runtime application logs (add to `.gitignore`).
*   **`reports/`**: Generated reports and images, including backtest results and WFO plots (add to `.gitignore`).
*   **`tasks/`**: Task definitions used by `task-master` for development tracking.
*   **`keys/`**: Contains API credentials, like `cdp_api_key.json`, used directly by some scripts (e.g., backtesting) (**DO NOT COMMIT**).
*   **`docs/`**: Project documentation (PRDs, notes).
*   **`.env`**: Environment variables for the main `app/` (API keys, DB strings - **DO NOT COMMIT**).
*   **`.gitignore`**: Specifies intentionally untracked files.
*   **`requirements.txt`**: Python dependencies.
*   **`setup.py`**: Project installation configuration.

## Key Components

*   **Coinbase Clients (`app/core/coinbase.py`, `app/core/websocket_client.py`):** Handles authenticated REST and WebSocket communication for the FastAPI app (using `.env`).
*   **Coinbase REST Client (`coinbase.rest.RESTClient`):** Used directly in `scripts/backtest_rsi_vbt_pro.py` for fetching historical data (using `keys/cdp_api_key.json`).
*   **DataManager (`app/core/data_manager.py`)**: Manages OHLCV data fetching and storage for the core app.
*   **DataProcessor (`app/core/data_processor.py`)**: Normalizes and cleans OHLCV data (core app).
*   **ZoneDetector (`app/core/zone_detector.py`)**: Identifies supply and demand zones (core app).
*   **SignalManager (`app/core/signal_manager.py`)**: Confirms trading signals based on zones and indicators (core app).
*   **OrderExecutor / DryRunExecutor (`app/core/order_executor.py`, `app/core/dry_run_executor.py`)**: Executes real or simulated trades (core app).
*   **RiskManager (`app/core/risk_manager.py`)**: Provides risk calculation functions (core app).
*   **Backtester (`scripts/backtest_rsi_vbt_pro.py`)**: Primary script for running advanced strategy backtests using `vectorbtpro`, including parameter optimization and Walk-Forward Optimization (WFO). Implements ATR-based stops.
*   **LiveTrader (`app/core/live_trader.py`)**: Orchestrates live trading logic (core app).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install TA-Lib:** This library is required for some technical indicators. Installation varies by OS:
    *   **macOS:** `brew install ta-lib`
    *   **Linux (Debian/Ubuntu):** `sudo apt-get update && sudo apt-get install -y ta-lib`
    *   **Windows:** Download binaries from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib) and install the appropriate `.whl` file using pip.
4.  **Install Python dependencies:** Note: `vectorbtpro` might require a separate installation/license beyond `requirements.txt`.
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt --pre # --pre needed for pandas-ta beta
    # If using vectorbtpro, ensure it's installed according to its documentation
    ```
5.  **Install in Editable Mode:** This makes the `app` package importable for tests and scripts.
    ```bash
    pip install -e .
    ```

## Configuration

1.  **Main Application (`app/`)**:
    *   Copy the example environment file: `cp .env.example .env`
    *   Edit `.env` and add your specific credentials and settings for the FastAPI application (used by `app/core/coinbase.py`, etc.).
        *   **Coinbase API Keys (JWT):** Generate keys from Coinbase Advanced Trade.
            *   `COINBASE_JWT_KEY_NAME`: Your full API key name.
            *   `COINBASE_JWT_PRIVATE_KEY`: Your API private key (PEM format, handle newlines correctly).
        *   `COINBASE_API_URL`: e.g., `https://api.coinbase.com/api/v3/brokerage`.
        *   `COINBASE_WS_URL`: e.g., `wss://advanced-trade-ws.coinbase.com`.
        *   (Optional) Database connection string.
2.  **Backtesting Script (`scripts/backtest_rsi_vbt_pro.py`)**:
    *   This script reads Coinbase API credentials directly from a JSON file.
    *   Create a file named `keys/cdp_api_key.json` (ensure `keys/` directory exists).
    *   The JSON structure should be:
        ```json
        {
          "name": "organizations/YOUR_ORG_ID/apiKeys/YOUR_KEY_ID",
          "privateKey": "-----BEGIN EC PRIVATE KEY-----\\nYOUR_PRIVATE_KEY_CONTENT\\n-----END EC PRIVATE KEY-----\\n",
          "passphrase": "YOUR_PASSPHRASE_IF_ANY"
        }
        ```
        *Replace placeholders with your actual Coinbase Advanced Trade API key details.*

**IMPORTANT:** Ensure both `.env` and the `keys/` directory are listed in your `.gitignore` file and never commit sensitive credentials to version control.

## Usage

**Running the FastAPI Server (Example):**
```bash
# Make sure your .env file is configured for the app
uvicorn app.main:app --reload
```

**Running the Advanced Backtest (Example):**
```bash
# Make sure keys/cdp_api_key.json is configured
python scripts/backtest_rsi_vbt_pro.py \\
    --symbol BTC-USD \\
    --start_date 2023-01-01 \\
    --end_date 2023-12-31 \\
    --granularity 1h \\
    --wfo_splits 8 \\
    --wfo_in_sample_pct 0.75 \\
    --optimize_metric "Sharpe Ratio" \\
    --sl_atr 2.0 \\
    --tsl_atr 1.5
# Output: WFO summary statistics printed to console.
# WFO plot saved to reports/vbtpro_rsi_wfo_summary_BTC_USD.html (example filename)
```

**Running the Live Trader (Example - Conceptual):**
```bash
# This part likely needs further development within the app/ structure
# python app/main.py --live --strategy bb_reversion --symbol ETH-USD
```

## Development Workflow

This project utilizes a task-driven development workflow managed by the `task-master` CLI tool. Tasks are defined in the `tasks/` directory and managed using commands like `task-master list`, `task-master next`, `task-master expand`, and `task-master set-status`. Refer to the [dev_workflow.mdc](.cursor/rules/dev_workflow.mdc) rule for detailed usage and commands.

## Testing

Run the test suite using pytest from the root directory:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

*(Note: Some tests might be skipped if they require live API keys or specific environment setup.)*

## Contributing

1.  Fork the repository
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`)
3.  Make your changes
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5.  Push to the branch (`git push origin feature/AmazingFeature`)
6.  Run tests (`pytest`)
7.  Open a Pull Request

## License

MIT License - see LICENSE file for details