# Adaptive Edge Trading Strategy

This directory contains different implementations of the Adaptive Edge Trading Strategy, which automatically adapts parameters based on market conditions.

## Overview

The Adaptive Edge Strategy is designed to dynamically adjust its parameters based on market volatility and market regime detection. The strategy:

1. Detects market regimes using Bollinger Bands (trending vs. ranging)
2. Measures volatility using Average True Range (ATR)
3. Dynamically adjusts parameters based on volatility:
   - Lower risk during high volatility (smaller position sizes)
   - Tighter stops during high volatility
   - Different indicator settings based on market conditions
4. Uses dynamic stop loss and take profit levels based on ATR

## Available Implementations

The repository includes multiple implementations of the strategy to accommodate different environments and requirements:

### 1. AdaptiveTradingStrategy (`adaptive_edge_strategy.py`)

The full-featured implementation using VectorBT Pro:
- Leverages VectorBT Pro's high-performance backtesting engine
- Supports all adaptive features
- Provides comprehensive performance metrics
- Suitable for production use with VectorBT Pro license

```python
from analysis_results.adaptive_edge_strategy import AdaptiveTradingStrategy

# Initialize and backtest
strategy = AdaptiveTradingStrategy(data, initial_capital=10000)
performance = strategy.backtest_strategy()
```

### 2. PandasAdaptiveStrategy (`pandas_adaptive_strategy.py`)

A pure pandas implementation without external dependencies:
- Works without VectorBT Pro or other specialized libraries
- Implements all core adaptive features
- Slower but more accessible and portable
- Suitable for educational purposes or environments without VectorBT Pro

```python
from analysis_results.pandas_adaptive_strategy import PandasAdaptiveStrategy

# Initialize and backtest
strategy = PandasAdaptiveStrategy(data, initial_capital=10000)
performance = strategy.backtest_strategy()
```

### 3. SimpleAdaptiveStrategy (`adaptive_edge_strategy_simple.py`)

A simplified version for testing and educational purposes:
- Uses very basic indicators (moving averages)
- Still implements dynamic parameter adjustment
- Focuses on the adaptive concept without complex indicators
- Suitable for quick testing or understanding core concepts

```python
from analysis_results.adaptive_edge_strategy_simple import SimpleAdaptiveStrategy

# Initialize and backtest
strategy = SimpleAdaptiveStrategy(data, initial_capital=10000)
performance = strategy.backtest_strategy()
```

## Test Scripts

For each strategy implementation, there's a corresponding test script:

1. `test_adaptive_edge_strategy.py` - For testing the VectorBT Pro implementation
2. `test_pandas_adaptive.py` - For testing the pandas implementation
3. `test_simple_strategy.py` - For testing the simplified version

Example usage:
```bash
# Test the pandas implementation with sample data
python test_pandas_adaptive.py --product SAMPLE-BTC-USD --start 2023-01-01 --end 2023-12-31 --capital 10000

# Test with real data (requires API credentials)
python test_pandas_adaptive.py --product BTC-USD --start 2023-01-01 --end 2023-12-31 --capital 10000
```

## Strategy Features

### Market Regime Detection

Uses Bollinger Bands to identify market regimes:
- **Trending**: When price is above the Bollinger middle band
- **Ranging**: When price is below the Bollinger middle band

### Volatility Measurement

Uses ATR (Average True Range) to measure market volatility:
- Compares current ATR to its 10-day average
- Identifies high volatility periods

### Dynamic Parameter Adjustment

Adjusts the following parameters based on volatility:
- **RSI Period**: 10 (high volatility) vs. 14 (normal volatility)
- **Bollinger Window**: 15 (high volatility) vs. 20 (normal volatility)
- **ATR Multiplier**: 2 (high volatility) vs. 3 (normal volatility)
- **Position Size**: Inversely scaled with volatility

### Risk Management

Implements dynamic risk management:
- **Stop Loss**: ATR * multiplier below entry price
- **Take Profit**: ATR * multiplier above entry price
- **Position Sizing**: Smaller positions during high volatility
- **Trailing Stops**: Adjusts with market movement

## Performance Metrics

The strategy outputs the following performance metrics:
- Initial Capital
- Final Portfolio Value
- Total Return (%)
- Max Drawdown (%)
- Sharpe Ratio
- Number of Trades

## Visualization

The strategy provides visualization through the `plot_equity_curve()` method:
- Portfolio value over time
- Entry and exit signals
- Stop loss and take profit triggers
- Volatility indicator (ATR)

## Compatibility

- **Environment**: The pandas implementation works in any Python environment
- **Data Format**: Requires OHLCV data with columns ['Open', 'High', 'Low', 'Close', 'Volume']
- **Timeframe**: Works with any timeframe (daily, hourly, etc.)

## Future Enhancements

Planned enhancements for the strategy:
- Multiple indicator approach for market regime detection
- Machine learning for parameter optimization
- Advanced portfolio management with multiple assets
- Additional risk management techniques 