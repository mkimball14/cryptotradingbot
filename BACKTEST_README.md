# Backtest Files Organization

## Main File
- **scripts/backtest_rsi_vbt.py** - The primary RSI backtesting implementation

## Other Backtest Files
- **scripts/backtest_bb_rsi_vbt.py** - Bollinger Bands + RSI combined strategy
- **scripts/backtest_rsi.py** - Simpler RSI implementation without vectorbtpro

## Test Files
- **tests/test_fetch_data.py** - Test for the fetch_historical_data function

## Backup Files
Old versions and duplicates have been moved to backup directories:
- **scripts/backup_files/** - Contains old versions of scripts
- **backup_files/** - Contains files that were in the root directory

## Logs
- Backtest log files are stored in the **logs/** directory

## Running the Backtest
To run the main RSI backtest:
```bash
python scripts/backtest_rsi_vbt.py --symbol BTC-USD --start_date 2023-01-01 --end_date 2023-12-31 --dashboard
```

For more options, run:
```bash
python scripts/backtest_rsi_vbt.py --help
```

## Generated Reports
Reports are saved to the `reports/` directory. 