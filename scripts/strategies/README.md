# Strategy Components Quick Reference

## File Overview

### Core Strategy Files
1. `edge_multi_factor_fixed.py` (24KB)
   - Base strategy implementation
   - Core trading logic and indicators
   - Position sizing and risk management

2. `wfo_edge_strategy.py` (108KB)
   - Walk-forward optimization (WFO)
   - Parameter optimization with Optuna
   - Performance metrics calculation

3. `edge_strategy_assistant.py` (47KB)
   - AI-powered strategy enhancement
   - Market regime analysis
   - Parameter suggestions

### Optimization Files
4. `enhanced_parameter_suggestions.py` (84KB)
   - Market-aware parameter optimization
   - AI model integration
   - Parameter validation

5. `chat_optimize_edge_strategy.py` (15KB)
   - Interactive optimization interface
   - AI chat model integration
   - Manual parameter tuning

6. `scheduled_optimization.py` (13KB)
   - Automated optimization scheduling
   - Regular parameter updates
   - Performance monitoring

### Analysis Files
7. `backtest_edge_strategy.py` (11KB)
   - Strategy backtesting
   - Performance analysis
   - Results visualization

### Test Files
8. `test_edge_multi_factor_fixed.py` (22KB)
   - Core strategy tests
   - Signal generation validation
   - Risk management tests

9. `test_edge_assistant.py` (7.5KB)
   - AI assistant tests
   - Parameter suggestion validation
   - Market analysis tests

## Quick Start

1. **Run Basic Strategy:**
   ```bash
   python edge_multi_factor_fixed.py
   ```

2. **Optimize Parameters:**
   ```bash
   python wfo_edge_strategy.py
   ```

3. **Interactive Optimization:**
   ```bash
   python chat_optimize_edge_strategy.py
   ```

4. **Run Scheduled Optimization:**
   ```bash
   python scheduled_optimization.py
   ```

## Common Workflows

1. **Initial Strategy Testing:**
   ```
   edge_multi_factor_fixed.py → backtest_edge_strategy.py
   ```

2. **Parameter Optimization:**
   ```
   wfo_edge_strategy.py → enhanced_parameter_suggestions.py
   ```

3. **AI-Assisted Tuning:**
   ```
   chat_optimize_edge_strategy.py → edge_strategy_assistant.py
   ```

For detailed documentation, see: `docs/strategy_architecture.md` 