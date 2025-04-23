# Cryptocurrency Factor-Based Trading Strategy

This project implements a comprehensive factor-based quantitative strategy for cryptocurrency trading. It uses multiple factors (momentum, volatility, mean reversion, and relative strength) to rank assets and construct portfolios with volatility targeting for risk management.

## Directory Structure

```
crypto_factor_strategy/
├── config/              # Configuration files
├── data/                # Data storage directory
├── docs/                # Documentation
│   └── ADVANCED_STRATEGY_GUIDE.md  # Detailed implementation guide
├── notebooks/           # Jupyter notebooks for analysis
├── strategies/          # Strategy implementation modules
│   ├── __init__.py
│   ├── backtester.py    # Backtesting implementation
│   ├── data_utils.py    # Data loading utilities
│   ├── factors.py       # Factor calculation functions
│   ├── optimizer.py     # Strategy optimization logic
│   └── portfolio.py     # Portfolio construction logic
├── tests/               # Test scripts
│   ├── test_volatility_targeting.py
│   ├── test_mean_reversion.py
│   ├── test_relative_strength.py
│   ├── test_optimizer.py
│   └── test_data_fetch.py
├── __init__.py          # Package initialization
├── coinbase_helper.py   # Coinbase API integration
├── main.py              # Main script to run the strategy
├── optimize.py          # Script for parameter optimization
├── requirements.txt     # Python dependencies
└── run_strategy.sh      # Shell script to run the strategy
```

## Installation

1. Set up a Python virtual environment (Python 3.11 recommended):
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API keys:
   - Create a `.env` file in the config directory
   - Add your Coinbase API keys (see docs/ADVANCED_STRATEGY_GUIDE.md for format)

## Usage

### Running the Strategy

Use the provided shell script:

```bash
./run_strategy.sh
```

Or run the main script directly:

```bash
python main.py
```

### Running Tests

Test scripts are provided to evaluate different components:

```bash
# Run volatility targeting test
python tests/test_volatility_targeting.py

# Run mean reversion factor test
python tests/test_mean_reversion.py

# Run relative strength factor test
python tests/test_relative_strength.py
```

## Documentation

See `docs/ADVANCED_STRATEGY_GUIDE.md` for detailed information on:
- Data acquisition
- Factor calculation
- Portfolio construction
- Backtesting methodology
- Live trading integration

## Key Features

- Multi-factor strategy combining momentum, volatility, mean reversion, and relative strength
- Volatility targeting for risk management
- Cross-sectional factor ranking
- Yahoo Finance and Coinbase data integration
- Comprehensive backtesting framework
- Parameter optimization capabilities

## Disclaimer

Trading cryptocurrencies involves significant risk. This strategy is provided for educational and research purposes only and should not be considered financial advice. Use at your own risk. 