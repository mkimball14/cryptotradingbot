# Strategy Refactoring Plan: Edge Multi-Factor & WFO

This document outlines the plan to refactor the `wfo_edge_strategy_optimized.py` and `edge_multi_factor_fixed.py` scripts.

**Goals:**

1.  **Improve Performance:** Utilize TA-Lib indicators via `vectorbtpro` for potential speed gains.
2.  **Enhance Maintainability:** Break down large scripts into smaller, focused Python modules (target < 500 lines each).
3.  **Standardize Structure:** Create a clear, reusable structure for strategy components.

**Proposed New Directory Structure:**

```
/Users/maximiliankimball/dev/crypto_bot/Crypto Trading Bot/scripts/strategies/refactored_edge/
├── __init__.py           # Makes the directory a Python package
├── config.py             # Centralized configuration (WFO, data, trading params)
├── parameters.py         # Optimization parameter grids (e.g., EDGE_MULTI_FACTOR_PARAM_GRID)
├── indicators.py         # Indicator calculations (using vbt.IF.from_talib)
├── signals.py            # Primary signal generation logic
├── regime.py             # Market regime detection and specific logic
├── strategy.py           # Core RefactoredEdgeStrategy class (inheriting vbt.Portfolio)
├── wfo.py                # Walk-Forward Optimization logic and execution
├── checkpoint.py         # WFO checkpoint saving/loading functions
├── utils.py              # Common utility functions (logging, data transforms)
├── backtest_runner.py    # Script for simple backtesting with fixed params
└── wfo_runner.py         # Main script to execute the full WFO process
```

**Refactoring Steps:**

1.  **Create Directory Structure:** Set up the `refactored_edge` directory and the empty Python files listed above.
2.  **Migrate Configuration:** Move constants, parameters, and settings from the original scripts into `config.py` and `parameters.py`.
3.  **Refactor Indicators:**
    *   Identify all indicator calculations (RSI, BBands, MACD, ATR, ADX, etc.) in the original scripts.
    *   Re-implement them in `indicators.py` using `vectorbtpro.IndicatorFactory.from_talib(...)` where applicable, referring to the official documentation: [https://vectorbt.pro/pvt_7a467f6b/](https://vectorbt.pro/pvt_7a467f6b/).
    *   Migrate or refactor custom indicators (e.g., S/D zones, volatility regime) into `vbt.IF`-compatible functions or keep them as separate helper functions within `indicators.py` or `utils.py`.
4.  **Migrate Signal Logic:** Move the code that translates indicator values into buy/sell signals into `signals.py`.
5.  **Migrate Regime Logic:** Move market regime detection (e.g., ADX-based) and regime-specific exit logic (from `create_regime_specific_exits`) into `regime.py`.
6.  **Build Strategy Class:** Create the `RefactoredEdgeStrategy` class in `strategy.py`. This class will:
    *   Initialize with necessary parameters (from `config.py`, `parameters.py`).
    *   Utilize functions/indicators from `indicators.py`, `signals.py`, and `regime.py`.
    *   Define `entries` and `exits` based on the combined signals.
7.  **Migrate WFO Logic:** Move the WFO execution loop, segment processing, parameter optimization, and performance analysis from `wfo_edge_strategy_optimized.py` into `wfo.py`.
8.  **Migrate Checkpointing:** Move checkpoint functions (`save_checkpoint`, `load_checkpoint`) into `checkpoint.py`.
9.  **Create Runners:**
    *   Develop `backtest_runner.py` to load data, instantiate `RefactoredEdgeStrategy` with fixed parameters, run a backtest, and print results.
    *   Develop `wfo_runner.py` to orchestrate the WFO process using the functions in `wfo.py`.
10. **Update Imports:** Ensure all relative and absolute imports are correct within the new structure and update any external scripts that might have imported from the old files.
11. **Testing:** Run `backtest_runner.py` and `wfo_runner.py` using the `conda run -n vectorbtpro ...` command to verify functionality.
