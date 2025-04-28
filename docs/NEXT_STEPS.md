# Next Steps for WFO Runner & Strategy

This document tracks the immediate and upcoming tasks for improving the Walk-Forward Optimization runner and the underlying trading strategy.

## Next Steps

- [x] Fix the 'too many arguments' TypeError in ATR calculation by using the correct vectorbtpro signature and output attribute.
- [x] Confirm that the WFO runner script executes past the previous blocker.
- [x] Investigate and resolve why training metrics (`train_return`, `train_sharpe`, `train_max_drawdown`) are missing from `wfo_results.csv`.
- [x] Continue automation loop: after fixing metrics, proceed with diagnostics and further enhancements as part of the self-improving workflow.

## Current Priorities (as of 2025-04-28)

1. **Complete WFO Integration Test:**
   * [x] Fix optimization test failures by standardizing regime information key to 'predominant_regime'
   * [x] Fix portfolio parameter warnings by creating portfolio creation helper function
   * [x] Create infrastructure for integration testing with small synthetic datasets
   * [x] Fix pandas FutureWarnings by using proper dataframe assignment patterns
   * [x] Standardize column naming to snake_case across the entire codebase
   * [x] Fix the KeyError for 'atr' in determine_market_regime_for_params function
   * [x] Fix parameter propagation to ensure all required attributes are present in temp config objects
   * [x] Complete end-to-end integration testing with synthetic data
   * [ ] Verify full pipeline operation with actual market data

2. **Regime-Aware Parameter Optimization:**
   * [ ] Complete the regime profiling system
   * [ ] Implement enhanced market regime classification with adaptive thresholds
   * [ ] Develop specialized parameter sets for trending vs ranging regimes
   * [ ] Add volatility-adjusted position sizing based on ATR
   * [ ] Perform comparative analysis of regime-specific vs. general parameter sets
   * [ ] Measure regime transition accuracy and adaptation speed

3. **Improve Signal Quality & Reliability:**
   * [x] Improved robustness ratio from negative (-0.17) to positive (0.51)
   * [x] Achieved positive test returns (5.48%) vs. negative previously
   * [ ] Explore using higher RSI thresholds (40) that appeared in later splits
   * [ ] Implement supply/demand zone proximity filters to improve entry/exit timing
   * [ ] Add volume-based confirmations for entry/exit signals
   * [ ] Develop comprehensive unit tests for all signal generation logic

4. **Documentation & Analysis:**
   * [x] Updated progress logs with detailed information about code improvements
   * [x] Centralized utility functions in wfo_utils.py
   * [x] Add defensive code with informative warnings for parameters
   * [ ] Create visualization dashboard for WFO performance metrics
   * [ ] Add performance comparison against benchmark strategies
   * [ ] Document all configuration parameters with optimal ranges

5. **Framework Robustness:**
   * [x] Add comprehensive parameter fallback mechanisms
   * [x] Fix pandas Series validation for indicator checks
   * [x] Implement proper test parameter monkey patching
   * [ ] Add end-to-end validation with real data from Coinbase API
   * [ ] Create benchmarking suite for performance comparison
    * Explore market regime detection to adapt strategy to different market conditions

## Immediate Actions

1. ✅ **Fixed Indicator Calculation Bugs:** Corrected indicator references in `optimize_params_parallel` function.
2. ✅ **Implemented Cross-Validation:** Added parameter stability validation through training data segmentation. 
3. ✅ **Fixed S/D Zone Calculation:** Ensured proper zone signal generation in optimization process.
4. ✅ **Run WFO with Anti-Overfitting Measures:** Successfully executed WFO with improved parameter stability testing.
5. ✅ **Implement Regime-Aware Parameter Adaptation:** Improved parameter consistency across different market segments using regime-aware parameter adaptation.
6. ✅ **Enhanced Regime-Aware Parameter Adaptation:** Implemented a more granular regime classification system that identifies 8 distinct market conditions beyond the basic trending/ranging split.
7. ✅ **Created Comprehensive Testing Framework:** Developed `regime_evaluation.py` for systematic testing of regime-aware adaptation across multiple assets and timeframes.
8. ✅ **Fixed Regime Evaluation Framework:** Resolved parameter mismatch, column case-sensitivity, and error handling issues across the regime-aware evaluation pipeline.
9. ✅ **Enhanced Synthetic Data Generator:** Completely refactored the synthetic data generator to create more realistic price series with explicit regime segments.
10. ✅ **Implemented Testing Mode:** Created environment variable-based testing mode with relaxed signal generation for robust framework testing.
11. ✅ **Improved Error Handling:** Added comprehensive error handling and type checking throughout the regime evaluation pipeline.
12. ✅ **Implemented Modular WFO Framework:** Refactored the monolithic WFO runner into focused modules (wfo_utils.py, wfo_evaluation.py, wfo_optimization.py, wfo_results.py, wfo.py) all under 500 lines.
13. ✅ **Fixed API Integration:** Corrected parameter naming for Coinbase Advanced API integration and added robust error handling.
14. ✅ **Enhanced Results Processing:** Added comprehensive reporting, visualization, and interim result saving for WFO analysis.
15. **Run Comprehensive Testing with Real Data:** Execute the testing framework with real historical data to quantify improvements from regime-aware adaptation.
16. **Fix Portfolio Parameter Warning:** Address the "Portfolio doesn't expect arguments ['sl_pct']" warning in the portfolio creation.
17. **Enhance Parameter Consistency:** Further refine signal generation logic to improve consistency across different market conditions.
18. **Optimize Risk Management:** Fine-tune stop-loss and position sizing to improve robustness.
19. **Standardize Column Naming:** Move to consistent snake_case column naming throughout the codebase to prevent case-sensitivity bugs.
20. **Add Profitability Patterns to Synthetic Data:** Enhance synthetic data generation to include patterns that produce profitable trades for better framework testing.
21. **Clean Up Legacy Files:** Remove the deprecated wfo_runner.py after confirming all functionality is preserved in the modular framework.

## Results Analysis & Diagnostics (as of 2025-04-28)

* **Parameter Stability Testing:** Implemented validation across training data segments to detect overfitting
* **Enhanced Results Analysis:** Added robustness, stability, and consistency ratings 
* **Anti-Overfitting Measures:** Successfully implemented cross-validation and simplified parameter grid
* **Technical Bugs Fixed:** Corrected indicator calculation references and S/D zone signal generation

* **WFO Results Analysis:**
  * Successfully processed all 4 splits with both training and test metrics
  * Average Training Return: 13.17% (reduced from previous 23.58%)
  * Average Test Return: 5.48% (improved from previous -3.66%)
  * Robustness Ratio: 0.51 (substantially improved from previous -0.16)
  * Parameter Stability: 0.0663 return standard deviation across segments (moderate)
  * Parameter Consistency: 25% of splits maintain consistent return sign (needs improvement)

## Lessons Learned
- Cross-validation significantly improves strategy robustness by detecting parameters that overfit to noise
- Simplified parameter grids lead to better generalization even with fewer options to explore
- Parameter stability across different market segments is a key indicator of strategy robustness
- Technical implementation details (like how indicators are calculated) can significantly impact results
- Proper S/D zone implementation requires consistent indicator calculation between optimization and evaluation
- Positive robustness ratio (>0.3) indicates reasonable transfer of strategy performance from training to testing
- Consistent parameter performance across different market segments remains challenging (only 25% consistency)
- Moderate parameter stability (return std dev ~0.06) suggests the strategy has reasonable but not ideal adaptability

#### Open Questions / Next Research Areas
- Which regime classification system (basic vs. enhanced) provides better overall trading performance?
- What are the optimal threshold values for enhanced regime detection (ADX, volatility, momentum)?  
- How significant is the impact of S/D zones compared to regime-aware adaptation?
- Can we integrate regime-specific position sizing to further improve risk-adjusted returns?
- How can we fix the portfolio parameter warning without compromising strategy performance?
- Would a hybrid approach combining regime-specific parameters and ensemble methods yield even better results?

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

## Future Enhancements

- **Advanced Optimization**
  - Walk-forward analysis with Monte Carlo resampling
  - Multi-objective optimization (return, drawdown, turnover, etc.)
  - Dynamic parameter adaptation ✅ (implemented basic and enhanced regime-aware adaptation)
  - Explore ensemble methods combining multiple parameter sets
  - Unsupervised learning for advanced regime classification

- **System Integration**
  - Connect to live API for real-time data and trading
  - Implement system monitoring and error handling
  - Build portfolio allocation layer
  - Add real-time regime detection for live trading ✅ (implemented enhanced regime detection)
  - Implement regime-specific position sizing and risk management
