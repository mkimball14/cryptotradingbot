# Next Steps for WFO Runner & Strategy

This document tracks the immediate and upcoming tasks for improving the Walk-Forward Optimization runner and the underlying trading strategy.

## Current Priorities (as of 2025-04-24)

1.  **Inspect `data/results/wfo_results.csv`:** Review the saved CSV from the last run to analyze the performance of the first 3 splits and confirm the Pair 4 failure resulted in NaNs.
2.  **Investigate Pair 4 WFO Failure:** Determine why all parameter combinations failed during the optimization phase for the last WFO split (training data from ~mid-2023 to ~mid-2024).
    *   Check market conditions during that period.
    *   Review strategy logic for edge cases.
    *   Consider if fixed parameters (MACD, weights) are problematic for that period.
3.  **Expand `PARAM_GRID` Cautiously:** Gradually re-introduce more parameter values in `scripts/strategies/refactored_edge/param_grid.py`. Test run after each small change.
    *   *Suggestion:* Start by adding 1-2 more `signal_threshold` values or 1-2 `macd_signal_window` options.
4.  **Refine Strategy Logic:** Based on results (especially if consistently poor even after grid expansion), consider refactoring or adjusting the core logic within `RefactoredEdgeStrategy`.

## Longer-Term Goals

*   **Implement Strategy Refactoring Plan:** Follow the steps outlined in `docs/strategy_refactoring_plan.md` to modularize the strategy code (indicators, signals, regime, config, etc.).
*   **Configuration Management:** Move hardcoded settings from `wfo_runner.py` to a dedicated config file (`config.py` or similar).
*   **WFO Checkpointing:** Implement saving/loading of WFO progress to allow resuming long runs.
*   **Advanced Optimization:** Explore more sophisticated optimization techniques beyond grid search if needed (e.g., Bayesian optimization, genetic algorithms).
