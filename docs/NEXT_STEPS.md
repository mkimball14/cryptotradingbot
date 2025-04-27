# Next Steps for WFO Runner & Strategy

This document tracks the immediate and upcoming tasks for improving the Walk-Forward Optimization runner and the underlying trading strategy.

## Next Steps

- [x] Fix the 'too many arguments' TypeError in ATR calculation by using the correct vectorbtpro signature and output attribute.
- [x] Confirm that the WFO runner script executes past the previous blocker.
- [x] Investigate and resolve why training metrics (`train_return`, `train_sharpe`, `train_max_drawdown`) are missing from `wfo_results.csv`.
- [x] Continue automation loop: after fixing metrics, proceed with diagnostics and further enhancements as part of the self-improving workflow.

## Current Priorities (as of 2025-04-27)

1.  **Implement Strategy Enhancements Based on WFO Analysis:**
    * Address the overfitting issue observed in the latest WFO results (training: +23.58%, test: -3.66%)
    * Focus on improving the robustness ratio (current: -0.16) to ensure the strategy transfers well from training to test periods
    * Further investigate the preference for higher RSI thresholds (40) in later splits
    * Refine the parameter grid to focus on the most promising regions (bb_std_dev: 2.0, bb_window: 20, risk_reward_ratio: 2.5)

2.  **Reduce Overfitting:**
    * Add regularization techniques to prevent curve-fitting
    * Test simpler strategy variants with fewer parameters
    * Consider adding out-of-sample validation as an additional step
    * Implement cross-validation for parameter selection

3.  **Improve Signal Quality:**
    * Implement additional trend filters based on the observed best parameters
    * Explore using higher RSI thresholds (40) that appeared in later splits
    * Add volume-based confirmations for entry/exit signals
    * Explore market regime detection to adapt strategy to different market conditions
2.  **Refine Strategy/Parameters:** Based on the analysis, potentially refine the parameter grid further or adjust strategy logic if needed.
3.  **Address Pytest Warnings:** Clean up the `FutureWarning` and `PydanticDeprecatedSince20` warnings identified during testing.
4.  **Continue Task #13:** Finalize the refactoring based on WFO results and analysis.
5.  **Proceed to Task #6:** Implement Dry-Run and Backtest Modes, likely using the best parameters found.

## Results Analysis & Diagnostics (as of 2025-04-27)

* **Fixed Split Processing:** All 4 splits are now properly processed and recorded in the results CSV
* **Fixed Training Metrics Extraction:** Training metrics are now correctly extracted from best_train_stats and recorded
* **Enhanced Error Handling:** Comprehensive error handling ensures processing continues even when issues occur
* **Added Interim Results Saving:** Results are saved after each split for recovery in case of script crashes

* **WFO Results Analysis:**
  * Successfully processed all 4 splits with complete metrics for both training and test periods
  * Average Training Return: 23.58%
  * Average Test Return: -3.66%
  * Robustness Ratio (Test/Train Return): -0.16
  * Parameter consistency across splits suggests some stability in the optimization process

## Lessons Learned
- The current strategy shows significant overfitting (positive training returns vs. negative test returns)
- Most splits favor similar parameters (bb_std_dev: 2.0, bb_window: 20, risk_reward_ratio: 2.5), indicating some consistency in optimization
- Later splits (3 and 4) show preference for higher RSI thresholds (40 vs 20), suggesting market conditions may have changed
- The negative robustness ratio confirms the strategy isn't transferring well from training to test periods

## Open Questions / Next Research Areas
- How can we reduce the overfitting to improve the robustness ratio?
- Would a simpler strategy with fewer parameters generalize better?
- Should we explore different optimization metrics beyond Sharpe ratio?
- How can we leverage the parameter consistency across splits to develop a more robust strategy?
- Is market regime detection needed to adapt to changing conditions (as suggested by the shift to higher RSI thresholds in later splits)?

## Longer-Term Goals

*   **Implement Strategy Refactoring Plan:** Continue following the steps outlined in `docs/strategy_refactoring_plan.md` to modularize the strategy code (indicators, signals, regime, config, etc.).
*   **Add Unit Tests:** Implement unit tests for indicator calculations and signal generation logic in `indicators.py` and `signals.py` to ensure robustness.
*   **Configuration Management:** Further refine the configuration management in `config.py` to support different market regimes.
*   **WFO Enhancement:** Improve the WFO process with techniques like:
    * Walk-forward window analysis to better understand parameter stability
    * Anchor points to handle regime changes
    * Ensemble methods combining multiple parameter sets
*   **Advanced Optimization:** Explore more sophisticated optimization techniques beyond grid search (e.g., Bayesian optimization, genetic algorithms).
*   **Machine Learning Integration:** Consider adding ML-based feature selection or parameter optimization to enhance the strategy.
*   **Alternative Data Sources:** Explore incorporating alternative data (e.g., sentiment, on-chain metrics) to improve signal quality.
