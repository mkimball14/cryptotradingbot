# Crypto Trading Bot Framework

A comprehensive framework for developing, backtesting, and deploying cryptocurrency trading bots, with a focus on the Coinbase Advanced Trade API.

## Overview

This project provides a structured environment for building automated trading strategies. It includes components for:

*   **Exchange Integration:** Connecting to Coinbase via REST API (JWT Auth) and WebSocket for market data and order execution.
*   **Data Management:** Fetching, processing, storing (SQLAlchemy), and retrieving historical and real-time OHLCV data.
*   **Trading Strategies:** Implementing custom trading logic (examples: RSI Momentum, BB Reversion).
*   **Signal Generation & Confirmation:** Detecting supply/demand zones and using technical indicators (RSI, MACD, Volume Profile) to validate signals.
*   **Order Execution:** Placing market, limit, and potentially bracket orders with simulated (dry-run) and live execution capabilities.
*   **Risk Management:** Calculating position sizes, stop-losses, and implementing risk controls (e.g., drawdown limits).
*   **Backtesting:** Evaluating strategy performance against historical data.
*   **API Interface:** Exposing core functionalities through a FastAPI web server.

## Project Structure

*   **`app/`**: Main application source code.
    *   `main.py`: FastAPI application entry point.
    *   `core/`: Core logic (API clients, data handling, execution, strategies interface, backtesting, risk).
    *   `models/`: Pydantic and dataclass definitions (Order, Position, Zone, etc.).
    *   `routers/`: FastAPI endpoints (orders, market, account, websocket).
    *   `strategies/`: Specific trading strategy implementations.
    *   `database/`: SQLAlchemy models and database interaction setup (within `app/core/`).
*   **`tests/`**: Unit and integration tests (using `pytest`).
*   **`scripts/`**: Utility scripts (e.g., log analysis).
*   **`logs/`**: Runtime application logs (add to `.gitignore`).
*   **`reports/`**: Generated reports and images (e.g., backtest results) (add to `.gitignore`).
*   **`docs/`**: Project documentation (PRDs, notes).
*   **`.env`**: Environment variables (API keys, JWT secrets, DB connection strings - **DO NOT COMMIT**).
*   **`requirements.txt`**: Python dependencies.
*   **`setup.py`**: Project installation configuration.

## Key Components

*   **Coinbase Clients (`app/core/coinbase.py`, `app/core/websocket_client.py`):** Handles authenticated REST and WebSocket communication.
*   **DataManager (`app/core/data_manager.py`)**: Manages OHLCV data fetching and storage.
*   **DataProcessor (`app/core/data_processor.py`)**: Normalizes and cleans OHLCV data.
*   **ZoneDetector (`app/core/zone_detector.py`)**: Identifies supply and demand zones.
*   **SignalManager (`app/core/signal_manager.py`)**: Confirms trading signals based on zones and indicators.
*   **OrderExecutor / DryRunExecutor (`app/core/order_executor.py`, `app/core/dry_run_executor.py`)**: Executes real or simulated trades.
*   **RiskManager (`app/core/risk_manager.py`)**: Provides risk calculation functions.
*   **Backtester (`app/core/backtester.py`)**: Runs strategies against historical data.
*   **LiveTrader (`app/core/live_trader.py`)**: Orchestrates live trading logic.

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
4.  **Install Python dependencies:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt --pre # --pre needed for pandas-ta beta
    ```
5.  **Install in Editable Mode:** This makes the `app` package importable for tests and scripts.
    ```bash
    pip install -e .
    ```

## Configuration

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  **Edit `.env`** and add your specific credentials and settings:
    *   **Coinbase API Keys:** Generate JWT-based API keys from Coinbase Advanced Trade.
        *   `COINBASE_JWT_KEY_NAME`: Your full API key name (e.g., `organizations/.../apiKeys/...`).
        *   `COINBASE_JWT_PRIVATE_KEY`: Your API private key (PEM format, including `-----BEGIN EC PRIVATE KEY-----` and `-----END EC PRIVATE KEY-----` lines, often needs newline characters represented as `\n` within the `.env` file if stored on a single line).
    *   `COINBASE_API_URL`: Should typically be `https://api.coinbase.com/api/v3/brokerage`.
    *   `COINBASE_WS_URL`: Should be `wss://advanced-trade-ws.coinbase.com`.
    *   (Optional) Database connection string if using database features.
    *   Other settings like trading parameters.

**IMPORTANT:** Ensure `.env` is listed in your `.gitignore` file and never commit it to version control.

## Usage

*(This section might need expansion based on how the application/scripts are intended to be run)*

**Running the FastAPI Server (Example):**
```bash
# Make sure your .env file is configured
uvicorn app.main:app --reload
```

**Running a Backtest (Example - Actual script may vary):**
```bash
# Assuming a backtest script exists
python scripts/run_backtest.py --strategy rsi_momentum --symbol BTC-USD --timeframe 1h --start 2023-01-01 --end 2023-12-31
```

**Running the Live Trader (Example - Actual script/entry point may vary):**
```bash
# Assuming a live trading script or main entry point
python app/main.py --live --strategy bb_reversion --symbol ETH-USD
```

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