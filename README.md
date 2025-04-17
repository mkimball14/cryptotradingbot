# Crypto Trading Bot with AI-Powered Optimization

A cryptocurrency trading bot with walk-forward optimization and AI-assisted strategy development using VectorBT Pro and OpenAI/OpenRouter APIs.

## Features

- **Edge Multi-Factor Strategy**: Combines RSI, Bollinger Bands, and volatility indicators for robust trading signals
- **Walk-Forward Optimization**: Dynamic parameter optimization across multiple market regimes
- **AI Strategy Assistant**: Uses LLMs to help optimize strategies and analyze market conditions
- **Backtest Analysis**: Comprehensive performance metrics and visualization
- **Parameter Research**: AI-assisted research for optimal indicator settings
- **Adaptive Strategies**: Generation of strategies that adapt to changing market conditions

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
OPENAI_API_KEY=your_openai_api_key_here
# OR
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Architecture

The system consists of several key components:

1. **Edge Strategy Assistant**: AI-powered strategy development and optimization
   - ChatVBT integration for parameter suggestions
   - SearchVBT for researching optimal indicator settings
   - Strategy enhancement and adaptation

2. **Walk-Forward Optimization**: Robust parameter optimization
   - Multiple in-sample/out-of-sample splits
   - Comprehensive performance metrics
   - Parameter stability analysis

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

### Understanding the Results

Analysis results are saved in the `analysis_results` directory:
- Complete strategy analysis in JSON format
- Backtesting results with performance metrics
- Market analysis and recommendations
- Adaptive strategy implementations

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
2. Update the signal generation logic in `create_pf_for_params()`
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
- Check that the .env file is being loaded correctly
- Verify API key format and subscription status

### VectorBT Issues
- Make sure VectorBT Pro is properly licensed and installed
- Check for version compatibility issues
- Ensure data inputs are in the correct format

### Performance Issues
- Reduce parameter space for faster optimization
- Use more efficient data preparation methods
- Consider parallel processing for parameter optimization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.