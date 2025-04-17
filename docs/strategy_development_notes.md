# Strategy Development & Debugging Notes (EdgeMultiFactor + WFO)

This document summarizes the development process and key lessons learned while implementing and debugging the `EdgeMultiFactorStrategy` with Walk-Forward Optimization (WFO) using `vectorbtpro`.

## Strategy Overview

*   **Goal:** Develop and optimize a multi-factor trading strategy (`EdgeMultiFactorStrategy`) for BTC-USD using a robust Walk-Forward Optimization (WFO) framework.
*   **Core Components:**
    *   `scripts/strategies/edge_multi_factor.py`: Contains the core strategy logic, including factor calculation functions and the `EdgeMultiFactorStrategy` class.
    *   `scripts/strategies/wfo_edge_strategy.py`: Implements the WFO process, handling data splitting, parameter optimization over in-sample periods, and evaluation over out-of-sample periods.
*   **Factors Used:**
    *   Volatility Regime Filter
    *   Consolidation Breakout
    *   Volume Divergence Confirmation
    *   Market Microstructure (Candle Shadows)

## Debugging Journey & Key Fixes

The process involved several significant debugging challenges, primarily related to `vectorbtpro`'s `IndicatorFactory` and portfolio simulation details.

1.  **`IndicatorFactory` Argument Mismatch (`TypeError: <lambda>() takes 4 positional arguments but 8 were given`)**:
    *   **Problem:** This was the most persistent error, occurring when `EdgeFactors.run()` was called within the WFO loop. It suggested the lambda function provided to `with_custom_func` was receiving the wrong number of arguments.
    *   **Attempted Fixes:**
        *   Adjusting lambda signature (`**kwargs`).
        *   Adjusting signatures of underlying `create_...` functions (`**kwargs`, specific positional arguments).
        *   Restructuring the factory using chained `with_custom_func` calls and explicit dependencies.
        *   Simplifying the lambda body to isolate the faulty calculation.
        *   Renaming factory parameters to avoid potential name collisions with the calling scope.
        *   Ensuring correct positional arguments were passed within the lambda.
    *   **Hypothesized Root Cause:** Potential complexity or bug in `IndicatorFactory` / `with_custom_func` handling argument passing for functions with *internal dependencies* (like `create_volume_divergence_indicator` needing the results of `create_consolidation_breakout_indicator` calculated within the same lambda), especially when called repeatedly with varying parameters during optimization.
    *   **Resolution:** **Refactoring `generate_signals`**. The `IndicatorFactory` definition (`EdgeFactors`) was removed entirely. The `generate_signals` method in `EdgeMultiFactorStrategy` was rewritten to call the individual `create_...` functions directly, bypassing the factory and giving explicit control over argument passing. This proved to be the most robust solution.

2.  **Portfolio Sizing Error (`Error: Target size types are not supported`)**:
    *   **Problem:** Occurred during `vbt.Portfolio.from_signals` when using `size_type='TargetPercent'` or `'targetpercent'`.
    *   **Cause:** Likely a mismatch between the calculated `target_pct` (based on risk fraction and ATR stop) and what `from_signals` expects for percentage-based sizing (which usually relates to portfolio equity).
    *   **Resolution:** Changed the sizing strategy.
        *   Renamed `calculate_target_percent` to `calculate_target_amount`.
        *   Refactored `calculate_target_amount` to calculate a target *dollar amount* based on `initial_capital * risk_fraction` and the ATR stop distance.
        *   Updated `Portfolio.from_signals` calls (in `create_pf_for_params` and the main script block) to use `size=target_amount` and `size_type='Amount'`.

3.  **Indicator Calculation Errors (`AttributeError: module 'vectorbtpro' has no attribute 'STDDEV'/'MSTD'`)**:
    *   **Problem:** Initial attempts used incorrect methods like `vbt.STDDEV.run` or `vbt.MSTD.run`.
    *   **Resolution:** Updated indicator functions (`create_volatility_regime_indicator`, `create_consolidation_breakout_indicator`, `create_volume_divergence_indicator`) to use the correct `vectorbtpro` accessor methods:
        *   `series.vbt.rolling_std(...)`
        *   `series.vbt.rolling_mean(...)`
        *   `series.vbt.rolling_max(...)`
        *   `series.vbt.rolling_min(...)`

4.  **Accessor Argument Error (`TypeError: ... got an unexpected keyword argument 'min_periods'`)**:
    *   **Problem:** The rolling accessor methods require the `minp` argument, not `min_periods`.
    *   **Resolution:** Changed `min_periods=` to `minp=` in all relevant `.vbt.rolling_...()` calls within the indicator functions.

5.  **Syntax Errors:** Addressed minor syntax issues, such as stray trailing commas within dictionary literals during refactoring attempts.

6.  **Import Errors:** Fixed errors arising from removing unused components (like `EdgeFactors` after the refactor).

## `vectorbtpro` Lessons Learned

*   **`IndicatorFactory` Complexity:** While powerful, using `IndicatorFactory.with_custom_func` for complex indicators with internal dependencies calculated within the custom function can lead to obscure argument-passing errors that are hard to debug. Directly calling calculation functions might be more transparent and reliable in these scenarios. Consider `with_apply_func` for simpler cases where functions operate on one parameter set at a time.
*   **Accessor Methods:** Prefer the `.vbt.*` accessors (`rolling_mean`, `rolling_std`, etc.) for standard rolling calculations on Series/DataFrames over potentially outdated or incorrectly assumed class methods like `vbt.MA.run`. Always verify the correct method name and argument names (e.g., `minp`).
*   **`Portfolio.from_signals` Sizing:** Understand the exact expectation for each `size_type`. `'Amount'` requires a dollar (quote currency) value. `'TargetPercent'` requires a percentage of *current equity*, which is difficult to calculate accurately before the portfolio simulation itself runs. Risk-based sizing might be easier to implement using `'Amount'`. Check documentation for how arguments like `size_granularity` apply to different `size_type` options.
*   **Debugging WFO/Optimization:** These processes are long. Use `tqdm` for progress bars on parameter loops. Implement verbose logging, especially at the start/end of splits and periodically within large parameter loops, to monitor progress and identify where processes might be getting stuck. Isolating components (like testing the factory or strategy signals outside the WFO loop) is crucial.
*   **Warnings vs. Errors:** Pay attention to `FutureWarning`s (like pandas downcasting or deprecated `fillna` methods) as they indicate future breaking changes, but prioritize fixing blocking `Error`s first. Understand warnings like "Metric 'X' not found" during optimization – they often indicate valid edge cases (like no trades) rather than code errors. 