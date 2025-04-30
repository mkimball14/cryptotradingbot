# Next Steps for WFO Runner & Strategy

This document tracks the immediate and upcoming tasks for improving the Walk-Forward Optimization runner and the underlying trading strategy.

## Next Steps

- [x] Fix the 'too many arguments' TypeError in ATR calculation by using the correct vectorbtpro signature and output attribute.
- [x] Confirm that the WFO runner script executes past the previous blocker.
- [x] Investigate and resolve why training metrics (`train_return`, `train_sharpe`, `train_max_drawdown`) are missing from `wfo_results.csv`.
- [x] Continue automation loop: after fixing metrics, proceed with diagnostics and further enhancements as part of the self-improving workflow.
- [x] Implement balanced signal generation approach with configurable strictness levels.
- [x] Fix WFO debugging issues and ensure successful trade generation (added ULTRA_RELAXED mode).
- [x] Fix duplicate ADX indicator calculations causing conflicts in indicators.py.
- [x] Enhance regime detection process with proper error handling and fallbacks.
- [x] Fix the detect_market_regimes function issue in the regime module.
- [x] Create a more formal implementation for ATR and regime data in position sizing.
- [x] Test with less strict signal generation criteria as default.
- [x] Reduce WFO window sizes to match available data.
- [x] Test with broader parameter ranges for entry/exit criteria.
- [x] Fix EdgeConfig model to support param_combinations attribute for comprehensive evaluation.

### Comprehensive Evaluation Framework Enhancements (Immediate Priority)

#### Phase 1: Quick Framework Validation
- [ ] Add parameter limiting feature (`--max-params` flag) to comprehensive_evaluation.py
- [ ] Implement parameter sampling logic when combinations exceed the limit
- [ ] Run limited local test with constrained parameters and date range
- [ ] Verify reports, visualizations, and statistics are generated correctly
- [ ] Confirm both standard and regime-aware evaluations complete successfully
- [ ] Check HTML report formatting and content completeness

#### Phase 2: Framework Robustness Enhancements
- [ ] Implement checkpointing mechanism after each WFO split
- [ ] Create resume capability to continue from last checkpoint
- [ ] Save interim results to disk at regular intervals
- [ ] Add periodic garbage collection for memory management
- [ ] Implement memory monitoring to adjust parameter sampling dynamically
- [ ] Create resource-aware execution mode with adaptive behavior
- [ ] Implement sequential parameter optimization per split
- [ ] Add parameter grid pruning based on early results

#### Phase 3: Full Strategy Evaluation
- [ ] Run comprehensive evaluation with full date range and optimized settings
- [ ] Compare regime-aware vs. standard approach performance
- [ ] Generate final report and visualizations
- [ ] Implement strategy improvements based on evaluation insights

- [ ] Investigate why standard signal generation creates no signals across all test periods.
- [ ] Expand parameter grid testing with focus on RSI thresholds (30-40 for entries, 60-70 for exits).
- [ ] Test regime adaptation with datasets showing clear trending and ranging periods.
- [ ] Fine-tune dynamic position sizing with different risk percentages and ATR multipliers.
- [ ] Create asset-specific signal configurations based on volatility profiles.
- [ ] Implement improved validation metrics to better evaluate signal quality.

## Strategy Performance Debug Results (2025-04-30)

### 🔍 Critical Issues Identified

1. **Signal Generation Problems:**
   * Normal parameter settings generate insufficient or no signals across most data segments
   * Strategy consistently falls back to ULTRA_RELAXED mode, which generates arbitrary signals
   * Signal quality is poor with win rates of 29-52% across different segments
   * Signal generation is heavily biased toward long signals (172 long vs 0 short)
   * Type mismatches between float64 arrays and boolean values causing errors in signal logic

2. **Missing/Incorrect Indicator Calculations:**
   * `add_adx` function was missing from indicators.py
   * ADX calculation errors causing regime detection failures
   * ATR data missing for position sizing calculations
   * Regime data missing or incorrect, causing defaults to be used

3. **Strategy Performance Metrics:**
   * Negative mean returns (-18.9%) in testing
   * Very poor Sharpe ratio (-8.30)
   * High max drawdown (21.1%)
   * Anti-overfitting analysis shows poor robustness, stability, and consistency
   * WFO runs now successfully complete but still show poor performance metrics

### ✅ Fixes Implemented

1. **Added the missing `add_adx` function** with robust error handling and NaN value handling
2. **Enhanced signal generation logic** with improved entry/exit conditions and automatic progression through strictness levels (BALANCED → RELAXED → ULTRA_RELAXED)
3. **Improved position sizing fallbacks** for missing ATR/regime data
4. **Added more sophisticated short signal generation** to ULTRA_RELAXED mode
5. **Fixed type mismatch errors in signal generation:**
   * Replaced direct OR (`|`) operations with pandas `.combine(lambda x, y: x or y)` for type compatibility
   * Added explicit boolean conversion for all signal generation conditions
   * Protected ratio calculations against division by zero with `.replace(0, 0.0001)`
   * Fixed logger configuration and imports in wfo_evaluation.py

### 📈 Next Strategy Performance Improvement Steps

1. **Signal Quality Enhancements:** ✅ (Partially Implemented)
   * ✅ Implemented volatility-adjusted thresholds that adapt to changing market conditions
   * ✅ Added enhanced exit logic with trailing stops, take-profit mechanisms, and time-based exits
   * ✅ Added momentum reversal detection for better entry timing
   * ✅ Enhanced regime-specific parameter adaptation with scaling based on regime strength
   * Still needed: Further tuning of signal thresholds and better short signal generation

2. **Exit Strategy Improvements:** ✅ (Implemented)
   * ✅ Added trailing stops based on ATR and volatility
   * ✅ Implemented take-profit logic with dynamic levels based on volatility
   * ✅ Added time-based exits for stagnant trades (low volatility periods)
   * ✅ Enhanced risk management with momentum acceleration detection
   * Still needed: Parameter tuning for exit thresholds

3. **Expanded Parameter Grid Testing:** ✅ (Implemented)
   * ✅ Fixed VectorBTpro parameter interface for compatible grid generation
   * ✅ Implemented configurable grid sizes (small, medium, large) with appropriate sampling
   * ✅ Added robust parallelization for faster grid search using ProcessPoolEngine/ThreadPoolEngine
   * ✅ Implemented caching mechanisms to reduce redundant calculations
   * Still needed: Run separate parameter optimization for trending vs ranging regimes

4. **Position Sizing Improvements:**
   * Implement adaptive risk based on regime and signal strength
   * Add drawdown-based risk reduction logic
   * Test various ATR multipliers for stop placement
   * Integrate Kelly Criterion with win rate estimation from historical performance

## Current Priorities (as of 2025-04-30)

1. **Enhanced Market Regime Detection & Adaptation:** ✅ (Implemented)
   * [x] Enhance signals_integration.py to adapt trading parameters based on market regime
   * [x] Create interactive regime-aware signal visualization tools using Plotly
   * [x] Implement parameter modification logic for trending vs. ranging markets
   * [x] Add visual comparison tools to validate regime-aware parameter adaptation
   * [x] Create summary statistics to quantify signal differences by regime
   * [x] Implement position sizing that adapts to detected market regime
   * [x] Add unit tests for regime-aware position sizing
   * [x] Integrate position sizing into backtest and WFO runners

2. **VectorBTpro & Performance Optimization:** ✅ (Implemented)
   * [x] Fix compatibility issues with VectorBTpro 2025.3.1 APIs
   * [x] Implement proper parallelization using ProcessPoolEngine/ThreadPoolEngine
   * [x] Add caching mechanisms for expensive operations
   * [x] Create configurable performance settings (parallel mode, caching, chunking)
   * [x] Ensure backward compatibility with robust fallbacks
   
3. **Advanced TA-Lib Integration:** ✅ (Implemented)
   * [x] Create enhanced_indicators.py module with advanced TA-Lib pattern recognition
   * [x] Implement multi-factor regime detection (VHF, Choppiness Index, ADX, patterns)
   * [x] Add adaptive parameter mapping based on regime strength
   * [x] Create transition detection for early adaptation to changing markets
   * [x] Connect enhanced indicators to the signal generation pipeline

## Next High-Priority Tasks (as of 2025-04-30)

1. **Comprehensive Performance Evaluation:**
   * [ ] Run full grid search with enhanced parameter grid and new regime detection
   * [ ] Compare results of standard vs. regime-aware parameter adaptation
   * [ ] Generate comprehensive performance reports with statistical validation
   * [ ] Create visual comparisons of different strategy configurations

2. **Signal Quality Enhancement:**
   * [ ] Fine-tune pattern recognition thresholds for better entry/exit timing
   * [ ] Create ensemble approach combining multiple pattern signals
   * [ ] Implement time-series analysis for cyclical market behavior
   * [ ] Test asymmetric parameters for long vs short signals

3. **Cross-Asset Testing & Optimization:**
   * [ ] Apply enhanced regime detection across multiple asset classes
   * [ ] Create asset-specific parameter sets based on volatility profiles
   * [ ] Test portfolio-level optimization with regime-aware allocation
   * [ ] Implement market correlation analysis for risk management
   * [ ] Run optimization with regime-aware settings to quantify performance improvements
   * [ ] Create real-data backtests comparing regime-aware vs. standard approaches
   * [ ] Implement adaptive stop-loss using regime information
   * [ ] Create dynamic trailing stops that adjust based on volatility and regime

2. **Leverage Robust Architecture:**
   * [x] Create comprehensive utilities module with data validation and error handling
   * [x] Fix circular dependencies throughout the codebase
   * [x] Resolve regime detection errors with proper percentage calculations
   * [x] Implement consistent error handling patterns with decorators
   * [x] Fix unbound local variable errors in optimization workflows
   * [ ] Add comprehensive unit tests for utility functions
   * [ ] Implement logging configuration with configurable verbosity levels
   * [ ] Create standardized validation patterns for all configuration objects
   * [ ] Apply consistent error handling across remaining modules

2. **Extended Multi-Asset Optimization & Analysis:**
   * [x] Fix tuple indexing in the objective function of run_optuna_optimization.py
   * [x] Update Pydantic validators to V2 style in batch_optuna_optimizer.py
   * [x] Create test script to verify the fixes with a small-scale optimization run
   * [x] Fix multi-asset test script to use correct functions from asset_profiles.py
   * [x] Run and verify multi-asset batch optimization across BTC-USD, ETH-USD, and SOL-USD
   * [x] Fix regime detection to correctly calculate trending/ranging percentages
   * [ ] Run extended batch optimization with more trials (50+) and additional assets for production use
   * [ ] Analyze optimization results to identify stable parameters across assets
   * [ ] Create visualization dashboard comparing asset-specific parameters
   * [ ] Document asset-specific optimal parameters in STRATEGY_OVERVIEW.md

3. **Backtest Runner Verification:**
   * [x] Debug backtest runner to ensure signals result in actual trades
   * [x] Fix portfolio creation logic to ensure trades execute properly
   * [x] Fix performance metrics calculation for vectorbtpro compatibility
   * [x] Verify trade count, win rate, and return metrics are reported correctly
   * [x] Run real-data tests with 1-hour timeframe for BTC-USD
   * [x] Implement fallback signal generation for guaranteed trade execution
   * [x] Ensure robust indicator calculation with proper logging
   * [x] Fix parameter propagation through the evaluation pipeline
   * [ ] Run comparative tests with original Edge strategy implementation
   * [ ] Perform multi-asset testing across BTC, ETH, SOL, and other major assets
   * [ ] Create documentation on performance characteristics compared to original

4. **WFO Integration Testing:**
   * [x] Fix optimization test failures by standardizing regime information key to 'predominant_regime'
   * [x] Fix portfolio parameter warnings by creating portfolio creation helper function
   * [x] Create infrastructure for integration testing with small synthetic datasets
   * [x] Fix pandas FutureWarnings by using proper dataframe assignment patterns
   * [x] Standardize column naming to snake_case across the entire codebase
   * [x] Fix the KeyError for 'atr' in determine_market_regime_for_params function
   * [x] Fix parameter propagation to ensure all required attributes are present in temp config objects
   * [x] Complete end-to-end integration testing with synthetic data
   * [x] Verify full pipeline operation with actual market data
   * [x] Fix preliminary regime analysis to properly calculate indicators first
   * [x] Add ULTRA_RELAXED signal mode for guaranteed trade generation in WFO
   * [x] Implement fallback mechanisms for no-trade scenarios
   * [x] Fix duplicate ADX and directional indicator calculations
   * [x] Add robust error handling and logging throughout WFO pipeline
   * [x] Integrate advanced position sizing into WFO evaluation process

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
   * [x] Create visualization dashboard for WFO performance metrics
   * [ ] Add performance comparison against benchmark strategies
   * [ ] Document all configuration parameters with optimal ranges

5. **Framework Robustness:**
   * [x] Add comprehensive parameter fallback mechanisms
   * [x] Fix pandas Series validation for indicator checks
   * [x] Implement proper test parameter monkey patching
   * [x] Add end-to-end validation with real data from Coinbase API
   * [x] Implement Optuna-based parameter optimization with improved objective function
   * [x] Create batch optimization framework for systematic parameter discovery
   * [ ] Create benchmarking suite for performance comparison
   * [ ] Migrate Pydantic validators to field_validator for V2 compatibility

## Immediate Actions

1. ✅ **Implement Optuna Optimization:** Replace grid search with Bayesian optimization for more efficient parameter discovery.
2. ✅ **Create Batch Optimization Framework:** Develop system to run optimizations across multiple symbols, timeframes, and window sizes.
3. ✅ **Run Batch Optimization:** Initial run showed parameter propagation issues and produced no valid trades.
4. **Fix Parameter Propagation Issues:**
   - Update WFO to properly handle `atr_window_sizing` and `use_zones` parameters
   - Ensure all strategy parameters are correctly passed through the optimization chain
   - Track and verify parameter propagation with detailed logging
5. **Implement & Test Balanced Signal Generation:** ✅
   - ✅ Created `balanced_signals.py` with configurable strictness levels
   - ✅ Implemented balanced signal approach between strict and relaxed modes
   - ✅ Added configurable parameters for trend threshold, zone influence, and holding period
   - ✅ Created comprehensive unit tests in `test_balanced_signals.py`
   - ✅ Added `signals_integration.py` module for centralized signal generation
   - ✅ Integrated balanced signals into the WFO evaluation pipeline
   - ✅ Verified different strictness levels generate appropriate signal quantities
6. **Run More Targeted Optimization:**
   ```python
   # Modified configuration with looser parameters
   symbols = ['BTC-USD']
   timeframes = ['1h']
   train_days = [90]  # Longer training window
   n_trials = 20      # Fewer trials for faster iteration
   ```
7. **Expand Parameter Ranges:**
   - Update parameter ranges in `config.py` to be significantly wider
   - Add tests for more aggressive parameter combinations
5. **Incorporate Benchmark Comparison:** Add performance comparison against standard benchmarks (buy-and-hold, simple MA crossover) to all evaluation reports.

✅ **Completed Major Tasks:**
- ✅ Task #6: Implement Dry-Run and Backtest Modes (all subtasks completed)
  - ✅ Built robust WFO framework with real data support
  - ✅ Implemented comprehensive visualization tools
  - ✅ Created Edge Multi-Factor Strategy Optimization Framework
  - ✅ Fixed OHLC column case sensitivity issues
  - ✅ Added support for variable market conditions

## Previously Completed Actions

1. ✅ **Implemented Balanced Signal Generation:** Created a configurable approach between strict and relaxed modes with fine-tuning parameters for trend threshold, zone influence, and holding period.

2. ✅ **Fixed Indicator Calculation Bugs:** Corrected indicator references in `optimize_params_parallel` function.
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

### Optuna Optimization Findings
* **Discovered Parameters:** Optuna found significantly different optimal values from defaults:
  * Bollinger Band Width: 2.94 standard deviations (vs default 2.0)
  * Moving Average Window: 108 bars (vs default 50)
  * ADX Threshold: 34.7 (vs default 25.0)
  * RSI Entry/Exit: 38/80 (vs default 30/70)
  * Supply/Demand Zones: Enabled
  * Enhanced Regimes: Enabled but regime filter disabled

* **Optimization Efficiency:** The Bayesian approach explored the parameter space more efficiently than grid search
* **Window Size Requirements:** Confirmed minimum effective training window size of 30+ days for valid optimization

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
- What is the optimal balance between signal quantity and quality for different assets and timeframes?
- Which signal strictness level (strict, balanced, relaxed) performs best in different market regimes?
- How should zone influence vary based on market volatility and trading volume?
- Which regime classification system (basic vs. enhanced) provides better overall trading performance?
- What are the optimal threshold values for enhanced regime detection (ADX, volatility, momentum)?  
- How significant is the impact of S/D zones compared to regime-aware adaptation?
- Can we integrate regime-specific position sizing to further improve risk-adjusted returns?
- How can we fix the portfolio parameter warning without compromising strategy performance?
- Would a hybrid approach combining regime-specific parameters and ensemble methods yield even better results?

## Next Implementation Priorities (as of 2025-04-29 Late Night)

1. **Position Sizing Integration**
   * [x] Implement advanced position sizing module with risk-based approach
   * [x] Add regime-aware position sizing multipliers
   * [x] Create ATR-based volatility adjustment for position sizing
   * [x] Integrate zone confidence into position sizing calculations
   * [x] Add Kelly Criterion option for mathematical optimization
   * [x] Create comprehensive test suite for position sizing module
   * [ ] Integrate position sizing into backtest runner
   * [ ] Integrate position sizing into WFO evaluation module
   * [ ] Test position sizing impact on risk-adjusted returns
   * [ ] Visualize position size differences across market regimes

2. **Risk Management Module**
   * [ ] Create dynamic drawdown protection with adjustable thresholds
   * [ ] Implement regime-aware stop-loss calculation
   * [ ] Add trailing stop functionality with ATR-based distances
   * [ ] Implement correlation-based exposure limits for multi-asset portfolios
   * [ ] Add maximum drawdown circuit breakers

3. **Portfolio Optimization**
   * [ ] Implement asset allocation based on regime-specific performance
   * [ ] Create correlation-aware position sizing
   * [ ] Add volatility targeting for portfolio-level risk management
   * [ ] Implement dynamic rebalancing based on regime shifts

## Longer-Term Goals

*   **Implement Strategy Refactoring Plan:** Continue following the steps outlined in `docs/strategy_refactoring_plan.md` to modularize the strategy code (indicators, signals, regime, config, etc.).
*   **Add Unit Tests:** Implement unit tests for indicator calculations and signal generation logic in `indicators.py` and `signals.py` to ensure robustness.
*   **Configuration Management:** Further refine the configuration management in `config.py` to support different market regimes.
*   **WFO Enhancement:** Improve the WFO process with techniques like:
    * Walk-forward window analysis to better understand parameter stability
    * Anchor points to handle regime changes
    * Ensemble methods combining multiple parameter sets
*  **Advanced Optimization:** ✅ Implemented Bayesian optimization with Optuna for more efficient parameter discovery. Additional future enhancements:
   * Add multi-objective optimization (return, drawdown, turnover, etc.)
   * Incorporate cross-validation within Optuna to reduce overfitting
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
  - Implement regime-specific position sizing ✅ (implemented integrated position sizing module)
  - Add comprehensive risk management system with drawdown protection

- **Advanced vectorbtpro Integration**
  - **Purged Walk-Forward Cross-Validation:** Implement WFO with purging/embargoing (`Splitter.from_purged_kfold`) for improved robustness.
  - **Advanced Portfolio Optimization:** Integrate `PyPortfolioOpt` or `Riskfolio-Lib` for dynamic, risk-based position sizing.
  - **Specialized Indicators:** Explore incorporating Hurst exponent (trend persistence) or Smart Money Concepts (institutional levels).
  - **Conditional Parameter Optimization:** Add `condition` logic to `vbt.Param` to skip illogical parameter combinations during optimization.
  - **Custom Numba Functions:** Investigate writing custom Numba-accelerated functions for unique or performance-critical calculations.
  - **Signal Unraveling:** Explore backtesting individual signal instances for more granular performance analysis.
