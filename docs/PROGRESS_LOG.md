# Progress Log: WFO Runner & Strategy Development

This log tracks significant changes, improvements, and lessons learned during the development and optimization of the WFO runner and associated trading strategies.

## Session: 2025-04-24

**Goal:** Improve WFO runner performance and robustness.

**Changes & Improvements:**

1.  **2025-04-25: Restored full automation of training metrics recording in WFO runner (Task #13).** Fixed `optimize_params_parallel` to re-run the best parameter set on training data and return stats (return, Sharpe, max drawdown, etc.), ensuring these metrics are saved in `wfo_results.csv` for all splits. This enables reliable WFO diagnostics and further automation cycles.
2.  **Identified Performance Bottleneck:** Initial WFO runs with the full parameter grid (`scripts/strategies/refactored_edge/param_grid.py`) were impractically slow (>10 hours per split estimate).
3.  **Reduced Parameter Grid:** Drastically reduced the `PARAM_GRID` from ~470k+ combinations to 256 by fixing MACD parameters and weights, and reducing options for other indicators/thresholds. This made runtimes manageable (minutes).
4.  **Implemented Parallel Optimization:** Modified `scripts/strategies/refactored_edge/wfo_runner.py` to use `joblib.Parallel` and `joblib.delayed` for evaluating parameter combinations concurrently across CPU cores.
5.  **Added Progress Bar:** Integrated `tqdm` to provide visual feedback during the lengthy parameter optimization phase of each WFO split.
6.  **Added Detailed Results Saving:** Enhanced `wfo_runner.py` to save key information for each WFO split (dates, best params, train/test performance metrics) to `data/results/wfo_results.csv` using `pandas`.
7.  **Bug Fixes:**
    *   Resolved `TypeError: 'numpy.float64' object is not callable` when saving results by correctly calling portfolio metric methods (`sharpe_ratio()`, `max_drawdown()`).
    *   Resolved `NameError: name 'best_pf_train' is not defined` by initializing loop variables correctly and improving logic flow for handling optimization/simulation success and failures.
8.  **Refactor:** Replaced the problematic `vbt.Splitter.from_n_rolling` call in `scripts/strategies/refactored_edge/wfo_runner.py` with a manual loop to calculate rolling train/test split indices. This resolves a `ValueError` caused by incorrect argument passing in the vectorbtpro factory method and ensures the WFO proceeds correctly. (Related to debugging Task 50).
9.  **Documentation Update:** Added a link in the main `README.md` pointing to `scripts/README.md` for detailed Task-Master CLI documentation, improving discoverability.

**Findings & Lessons Learned:**

*   Grid search optimization is highly sensitive to the number of parameters and their value ranges. Even with parallelization, millions of combinations are impractical for WFO.
*   The reduced parameter grid (256 combos) resulted in negative average returns, indicating the need for more exploration or strategy refinement.
*   The last WFO split (Pair 4/4) failed optimization (no valid parameters found) even with the reduced grid, suggesting potential issues with the strategy logic or its suitability for the specific market data in that period (~mid-2023 to mid-2024).
*   Saving detailed WFO results is crucial for diagnosing issues and comparing performance across runs.

## Session: 2025-04-24

*   **WFO Debugging:** Successfully ran the `refactored_edge/wfo_runner.py` script end-to-end.
    *   Resolved the `TypeError` related to `calculate_volatility` argument passing.
    *   Identified and fixed the issue where the `vol_threshold` parameter was set too high, preventing any trades.
    *   Adjusted the `vol_threshold` range in `config.py`'s `EDGE_MULTI_FACTOR_PARAM_GRID` to `(0.002, 0.02, 0.004)` based on observed indicator values.
    *   Confirmed that trades are now generated and the WFO process completes for all splits.
    *   Results are successfully saved to `data/results/wfo_results.csv`.
    *   **Finding:** Initial test run with a *single parameter set* (due to debugging focus) showed consistently negative performance across most splits, indicating the need for full grid optimization.

## Session: 2025-04-24 (Continued) - Strategy Logic Refinement

**Goal:** Improve WFO profitability by refining the `generate_edge_signals` logic in `scripts/strategies/refactored_edge/signals.py`.

**Experiments & Changes:**

1.  **Added Debug Prints:** Enhanced `generate_edge_signals` with detailed print statements to track signal counts after each condition/filter step, aiding diagnosis.
2.  **Experiment 1: Inverted Volatility Filter:**
    *   Changed entry condition to require *low* volatility (`volatility < volatility_threshold`).
    *   Adjusted `EDGE_MULTI_FACTOR_PARAM_GRID` in `config.py` to explore lower parameter values.
    *   **Result:** Performance worsened significantly. Optimizer still hit boundaries, and most splits failed performance constraints (e.g., min trades).
3.  **Experiment 2: Removed Volatility Filter (Entry):**
    *   Reverted volatility calculation but removed it from the `trade_allowed` check for entry signals. Entry relied on RSI, BB, and Trend Filter.
    *   **Result:** WFO completed for all splits, but performance remained consistently negative (Avg Test Return: -3.39%). Optimizer still selected boundary parameters.
4.  **Experiment 3: Stricter Exit Logic:**
    *   Changed the exit condition from `rsi_exit | bb_exit` to `rsi_exit & bb_exit` (requiring both).
    *   **Result:** WFO completed, but performance still consistently negative (Avg Test Return: -3.19%). Optimizer still selected boundary parameters.

**Findings & Lessons Learned:**

*   Modifying entry/exit filters (volatility, trend, exit condition logic) did not lead to profitability with the existing RSI/BB core logic and previous parameter ranges.
*   The consistent selection of boundary parameters (lowest windows, thresholds) strongly suggests the strategy, as defined by these indicators and ranges, lacks robustness or isn't well-suited for finding a stable optimum across different market conditions.

**Decision & Current Status:**

*   Decided to shift focus from minor logic tweaks to significantly revising the parameter grid (`EDGE_MULTI_FACTOR_PARAM_GRID` in `config.py`).
*   The new grid explores less sensitive ranges (longer windows, wider BB deviations, higher RSI thresholds) and fixes several parameters (volatility, trend, SL/TP) to reduce the search space (now 243 combinations).
*   Attempted to run WFO with the new grid but encountered a `TypeError` because fixed parameter values in the grid were not wrapped in lists as required by `sklearn.model_selection.ParameterGrid`.

## 2025-04-25

**WFO Results CSV and Entry Logic Debugging:**
- Ran WFO with updated entry logic and reduced parameter grid; results are now saved in `data/results/wfo_results.csv` for all splits.
- Observed that some splits still fail to generate trades or yield negative returns, even with `use_zones=False` and loosened entry logic.
- Updated `NEXT_STEPS.md` to focus on analyzing the new CSV results and printed indicator/entry signal values.
- Blockers: Entry logic may still be too restrictive, or parameter grid too narrow for current market data. No trades or negative test returns remain a core issue.
- Next: Analyze the CSV for splits/params that do produce trades, document findings, and further adjust grid or logic as needed. Continue to log all changes and insights.
- See `NEXT_STEPS.md` for current priorities and open questions.

## 2025-04-25 (WFO Now Producing Trades, But Poor Performance)

- Entry signal logic now produces trades for many parameter sets (e.g., up to 8152 short trades in a split).
- However, performance is highly negative (e.g., -43.74% return, Sharpe -5.01, MDD 46.60%).
- Results are now saved to CSV, enabling easier cross-run analysis.
- Next focus: analyze which parameter sets are least bad, visualize trades, and refine exit/risk logic to reduce overtrading and improve profitability.
- See NEXT_STEPS.md for actionable items.

## 2025-04-25 (Post-Exit Logic Enhancement, Automation Loop)

- Enhanced exit/risk logic: stricter exits (RSI & BB required), minimum holding period (3 bars).
- WFO run completed after changes. Test return improved slightly (now -43.25%), but performance is still highly negative.
- Overtrading reduced: debug output shows some parameter sets with as few as 6-14 trades, but others still generate thousands.
- Next: further restrict entry logic, add volatility or regime filter, and continue to reduce overtrading.
- Automation loop is running: Cascade is automatically analyzing results, enhancing logic, and iterating without user prompts.

---

## Session: 2025-04-25 (Debugging Signal Generation)

- Added debug prints for test signal components (RSI, BBands, S/D zones) in `wfo_runner.py` after signal generation for the test split.
- Forced `use_zones=False` in test split to test if zone logic is blocking entries.
- Observed: No long/short entries generated; indicator and zone values printed for further analysis.
- Parameter grid was reduced significantly (from >470k to <256 combinations) for performance/memory reasons, but this may have made the search space too restrictive.
- Noted that optimizer tends to pick boundary parameter values, suggesting robustness/generalization issues.
- Signal/indicator logic (e.g., entry/exit conditions, volatility filter) was tweaked in previous sessions to try to improve trade generation and profitability.
- No new pytest warnings or test failures encountered; previous warnings (FutureWarning, Pydantic deprecation) remain to be cleaned up.
- Next: Analyze printed values to determine if parameter grid, logic, or zone thresholds need adjustment. Consider visualizing indicator/entry signals or further loosening parameter grid.

## Session: 2025-04-27 (Fixed Split Processing and Training Metrics Extraction)

- **Fixed All Splits Processing:** Restructured the WFO loop in `scripts/strategies/refactored_edge/wfo_runner.py` to properly process all splits instead of just the last one. Each split now correctly executes through the entire pipeline: parameter optimization, signal generation, portfolio creation, and results recording.

- **Fixed Training Metrics Extraction:** Resolved the issue with training metrics not being properly extracted and recorded in the results CSV. The script now correctly extracts `train_return`, `train_sharpe`, and `train_max_drawdown` directly from `best_train_stats` for each split.

- **Enhanced Error Handling:** Implemented comprehensive error handling with nested try/except blocks to ensure processing continues even when issues occur in individual splits. Errors are logged but don't prevent the script from continuing to the next split.

- **Added Interim Results Saving:** Enhanced the results recording to save interim results after each split, enabling recovery in case of script crashes.

- **WFO Results Analysis:**
  - Successfully processed all 4 splits with complete metrics for both training and test periods
  - Average Training Return: 23.58%
  - Average Test Return: -3.66%
  - Robustness Ratio (Test/Train Return): -0.16
  - Parameter consistency across splits suggests some stability in the optimization process

- **Key Findings:**
  - Significant overfitting is still present (positive training returns vs. negative test returns)
  - Most splits favor similar parameters: bb_std_dev: 2.0, bb_window: 20, risk_reward_ratio: 2.5
  - Later splits (3 and 4) show preference for higher RSI thresholds (40 vs 20 for lower bound)
  - The negative robustness ratio confirms the strategy isn't transferring well from training to test periods

