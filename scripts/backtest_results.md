# RSI Momentum Trading Strategy Backtest Results

## Best Strategy Performance

We tested multiple variants of an RSI and moving average crossover strategy on BTC-USD for the period January 1, 2023 to December 31, 2023. The best performing strategy had the following parameters:

- RSI Period: 7 (shorter and more responsive)
- RSI Oversold Threshold: 20 (more selective for oversold conditions)
- RSI Overbought Threshold: 80 (more selective for overbought conditions)
- Fast SMA Period: 5 (very responsive to recent price changes)
- Slow SMA Period: 20 (medium-term trend indicator)

## Performance Metrics

- **Total Return: 7.72%**
- **Sharpe Ratio: 0.06** (low risk-adjusted return)
- **Max Drawdown: -7.96%** (moderate)
- **Win Rate: 31.37%** (lower, but still profitable overall)
- **Sortino Ratio: 0.11** (low downside risk-adjusted return)
- **Profit Factor: 1.17** (winning trades outweigh losing trades)
- **Total Trades: 103** (good number of trades)
- **Avg Trade Duration: ~330 days** (very long - indicates position holding rather than active trading)

## Findings & Observations

1. **Parameter Selection**: Short-term indicators (RSI-7, 5-day SMA) combined with more selective entry/exit thresholds (20/80) performed better than standard settings.

2. **Simple Strategy Works**: Our best strategy used simplified entry/exit conditions:
   - Entry: RSI < 20 OR Fast SMA > Slow SMA
   - Exit: RSI > 80 OR Fast SMA < Slow SMA
   - Plus fixed 5% stop loss and 15% take profit

3. **Trade Duration**: The average trade duration is very long (330 days), which indicates the strategy is more suited for position trading than active trading.

4. **Win Rate**: Despite a low win rate of 31.37%, the strategy is profitable, suggesting that winning trades outperformed losing trades significantly.

5. **Risk-Adjusted Performance**: The Sharpe ratio (0.06) is quite low, suggesting this strategy has room for improvement in terms of risk-adjusted returns.

## Next Steps

1. **Optimize Trade Duration**: Consider adding more intermediate exit conditions to reduce the average trade duration.

2. **Improve Win Rate**: Test additional filter conditions to increase the win rate above 31%.

3. **Risk Management**: Explore dynamic position sizing based on volatility (ATR).

4. **Parameter Optimization**: Conduct more extensive parameter testing, especially for stop loss and take profit levels.

5. **Market Regime Filtering**: Add filters to avoid trading during high volatility periods.

## Conclusion

The RSI-Momentum strategy shows promise with a 7.72% return over the test period, but needs refinement for better risk-adjusted performance. The strategy performs best with more responsive indicators (short RSI and SMA periods) and more selective entry/exit thresholds, combined with simple stop loss and take profit rules. 