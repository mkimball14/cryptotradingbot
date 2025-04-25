# Progress Log: WFO Runner & Strategy Development

This log tracks significant changes, improvements, and lessons learned during the development and optimization of the WFO runner and associated trading strategies.

## Session: 2025-04-24

**Goal:** Improve WFO runner performance and robustness.

**Changes & Improvements:**

1.  **Identified Performance Bottleneck:** Initial WFO runs with the full parameter grid (`scripts/strategies/refactored_edge/param_grid.py`) were impractically slow (>10 hours per split estimate).
2.  **Reduced Parameter Grid:** Drastically reduced the `PARAM_GRID` from ~470k+ combinations to 256 by fixing MACD parameters and weights, and reducing options for other indicators/thresholds. This made runtimes manageable (minutes).
3.  **Implemented Parallel Optimization:** Modified `scripts/strategies/refactored_edge/wfo_runner.py` to use `joblib.Parallel` and `joblib.delayed` for evaluating parameter combinations concurrently across CPU cores.
4.  **Added Progress Bar:** Integrated `tqdm` to provide visual feedback during the lengthy parameter optimization phase of each WFO split.
5.  **Added Detailed Results Saving:** Enhanced `wfo_runner.py` to save key information for each WFO split (dates, best params, train/test performance metrics) to `data/results/wfo_results.csv` using `pandas`.
6.  **Bug Fixes:**
    *   Resolved `TypeError: 'numpy.float64' object is not callable` when saving results by correctly calling portfolio metric methods (`sharpe_ratio()`, `max_drawdown()`).
    *   Resolved `NameError: name 'best_pf_train' is not defined` by initializing loop variables correctly and improving logic flow for handling optimization/simulation success and failures.
7.  **Refactor:** Replaced the problematic `vbt.Splitter.from_n_rolling` call in `scripts/strategies/refactored_edge/wfo_runner.py` with a manual loop to calculate rolling train/test split indices. This resolves a `ValueError` caused by incorrect argument passing in the vectorbtpro factory method and ensures the WFO proceeds correctly. (Related to debugging Task 50).
8.  **Documentation Update:** Added a link in the main `README.md` pointing to `scripts/README.md` for detailed Task-Master CLI documentation, improving discoverability.

**Findings & Lessons Learned:**

*   Grid search optimization is highly sensitive to the number of parameters and their value ranges. Even with parallelization, millions of combinations are impractical for WFO.
*   The reduced parameter grid (256 combos) resulted in negative average returns, indicating the need for more exploration or strategy refinement.
*   The last WFO split (Pair 4/4) failed optimization (no valid parameters found) even with the reduced grid, suggesting potential issues with the strategy logic or its suitability for the specific market data in that period (~mid-2023 to mid-2024).
*   Saving detailed WFO results is crucial for diagnosing issues and comparing performance across runs.

**Next Steps:** See `docs/NEXT_STEPS.md`.
