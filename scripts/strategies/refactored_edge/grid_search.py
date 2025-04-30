#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parameter Grid Search for Edge Strategy

This script provides a systematic approach to exploring different parameter combinations
for the Edge trading strategy. It generates parameter grids of various sizes,
runs the strategy with these parameters, and analyzes the results.

Author: Max Kimball
Date: 2025-04-30
"""
import os
import sys
import logging
import itertools
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the path to ensure imports work correctly
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import local modules
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.wfo import run_wfo
from scripts.strategies.refactored_edge.wfo_utils import (
    SYMBOL, TIMEFRAME, START_DATE, END_DATE, INIT_CAPITAL, N_JOBS,
    WFO_TRAIN_POINTS, WFO_TEST_POINTS, STEP_POINTS, ensure_output_dir
)
from scripts.strategies.refactored_edge.data.data_fetcher import fetch_historical_data, GRANULARITY_MAP_SECONDS

# Import VectorBTpro for advanced features
import vectorbtpro as vbt

# Import parallelization engines
from vectorbtpro.utils import ProcessPoolEngine, ThreadPoolEngine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("grid_search")

def create_parameter_grid(size: str = 'medium', is_quick_test: bool = False) -> List[Dict[str, Any]]:
    """
    Generate a parameter grid of the specified size.
    
    Args:
        size: Size of the grid ('small', 'medium', 'large')
        is_quick_test: Whether to use a minimal grid for testing
        
    Returns:
        List of parameter dictionaries
    """
    if is_quick_test:
        logger.info("Using minimal test parameter grid (2 combinations)")
        return [
            {
                'rsi_window': 14,
                'bb_window': 20,
                'bb_std_dev': 2.0,
                'ma_window': 50,
                'atr_window': 14,
                'rsi_entry_threshold': 30,
                'rsi_exit_threshold': 70,
                'adx_window': 14,
                'adx_threshold': 25.0,
                'use_regime_filter': True,
                'use_enhanced_regimes': True
            },
            {
                'rsi_window': 14,
                'bb_window': 20,
                'bb_std_dev': 2.0,
                'ma_window': 50,
                'atr_window': 14,
                'rsi_entry_threshold': 40,
                'rsi_exit_threshold': 60,
                'adx_window': 14,
                'adx_threshold': 25.0,
                'use_regime_filter': True,
                'use_enhanced_regimes': True
            }
        ]
    
    # Define different grid sizes
    if size == 'small':
        logger.info("Using small parameter grid (limited combinations)")
        grid = {
            # Core parameters with limited options
            'rsi_window': [14],
            'bb_window': [20],
            'bb_std_dev': [2.0],
            'ma_window': [50, 100],
            'atr_window': [14],
            'rsi_entry_threshold': [30, 35, 40],
            'rsi_exit_threshold': [60, 65, 70],
            'adx_window': [14],
            'adx_threshold': [25.0],
            'use_regime_filter': [True],
            'use_enhanced_regimes': [True],
            # Signal generation parameters
            'signal_strictness': [SignalStrictness.BALANCED, SignalStrictness.RELAXED],
            'trend_threshold_pct': [0.01],
            'zone_influence': [0.5],
            'min_hold_period': [2]
        }
    elif size == 'large':
        logger.info("Using large parameter grid (comprehensive optimization)")
        grid = {
            # Core parameters with comprehensive options
            'rsi_window': [7, 14, 21],
            'bb_window': [20, 30],
            'bb_std_dev': [1.5, 2.0, 2.5],
            'ma_window': [21, 50, 100, 200],
            'atr_window': [7, 14, 21],
            # Signal parameters with comprehensive options
            'rsi_entry_threshold': [25, 30, 35, 40, 45],
            'rsi_exit_threshold': [55, 60, 65, 70, 75],
            'adx_window': [7, 14, 21],
            'adx_threshold': [15.0, 20.0, 25.0, 30.0, 35.0],
            'use_regime_filter': [True, False],
            'use_enhanced_regimes': [True, False],
            # Signal generation parameters
            'signal_strictness': [
                SignalStrictness.BALANCED,
                SignalStrictness.RELAXED,
                SignalStrictness.ULTRA_RELAXED
            ],
            'trend_threshold_pct': [0.005, 0.01, 0.015, 0.02],
            'zone_influence': [0.3, 0.5, 0.7, 0.9],
            'min_hold_period': [0, 1, 2, 3]
        }
    else:  # medium (default)
        logger.info("Using medium parameter grid (balanced optimization)")
        grid = {
            # Core parameters with moderate options
            'rsi_window': [14],
            'bb_window': [20],
            'bb_std_dev': [2.0, 2.5],
            'ma_window': [21, 50, 100],
            'atr_window': [14],
            # Signal parameters with moderate options
            'rsi_entry_threshold': [25, 30, 35, 40, 45],
            'rsi_exit_threshold': [55, 60, 65, 70, 75],
            'adx_window': [14],
            'adx_threshold': [20.0, 25.0, 30.0],
            'use_regime_filter': [True, False],
            'use_enhanced_regimes': [True, False],
            # Signal generation parameters
            'signal_strictness': [
                SignalStrictness.BALANCED,
                SignalStrictness.RELAXED,
                SignalStrictness.ULTRA_RELAXED
            ],
            'trend_threshold_pct': [0.005, 0.01, 0.015],
            'zone_influence': [0.3, 0.5, 0.7],
            'min_hold_period': [1, 2, 3]
        }
    
    # Generate parameter combinations
    try:
        # Create list of parameter combinations
        param_keys = list(grid.keys())
        param_values = list(grid.values())
        all_combinations = list(itertools.product(*param_values))
        combinations = []
        
        # Convert to list of dictionaries
        for combo in all_combinations:
            param_dict = {}
            for i, key in enumerate(param_keys):
                param_dict[key] = combo[i]
            combinations.append(param_dict)
        
        total_combinations = len(combinations)
        logger.info(f"Generated {total_combinations} parameter combinations for optimization")
        
        # For large grids, sample a subset to make computation feasible
        max_combinations = 100  # Adjust based on computational resources
        if total_combinations > max_combinations and not size == 'small':
            import random
            logger.warning(f"Grid too large ({total_combinations} combinations). Sampling {max_combinations} combinations.")
            combinations = random.sample(combinations, max_combinations)
        
        return combinations
    except Exception as e:
        logger.error(f"Error generating parameter combinations: {str(e)}")
        # Fallback to minimal test parameters
        logger.warning("Falling back to minimal test parameter grid")
        return create_parameter_grid(is_quick_test=True)


def run_grid_search(
    symbol: str = SYMBOL,
    timeframe: str = TIMEFRAME,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    n_splits: int = 1,
    grid_size: str = 'medium',
    is_quick_test: bool = False,
    custom_train_points: Optional[int] = None,
    custom_test_points: Optional[int] = None,
    max_combinations: int = 50,  # Maximum number of parameter combinations to test
    n_jobs: int = -1,            # Default to using all available cores
    use_caching: bool = True,    # Enable VectorBTpro caching for faster repeated calculations
    use_chunking: bool = True,   # Enable chunking for large datasets
    parallel_mode: str = 'process'  # Options: 'process', 'thread', 'ray'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Run a grid search over parameter combinations and evaluate performance.
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Data granularity (e.g., '1h', '4h', '1d')
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        n_splits: Number of WFO splits to run
        grid_size: Size of parameter grid ('small', 'medium', 'large')
        is_quick_test: Whether to use a minimal grid for testing
        custom_train_points: Custom number of data points for training window
        custom_test_points: Custom number of data points for testing window
        max_combinations: Maximum number of parameter combinations to test
        
    Returns:
        DataFrame with evaluation results for each parameter combination,
        Dictionary with best parameter combinations by metric
    """
    logger.info(f"Starting grid search for {symbol} from {start_date} to {end_date}")
    logger.info(f"Using {grid_size} parameter grid, {n_splits} splits")
    
    # Step 1: Fetch or use provided data
    try:
        # Convert timeframe string to granularity in seconds
        if timeframe in GRANULARITY_MAP_SECONDS:
            granularity = GRANULARITY_MAP_SECONDS[timeframe]
        else:
            # Default to 1h if timeframe is not recognized
            logger.warning(f"Unrecognized timeframe: {timeframe}, defaulting to '1h'")
            granularity = GRANULARITY_MAP_SECONDS['1h']
            
        logger.info(f"Fetching data for {symbol} from {start_date} to {end_date} with timeframe {timeframe} (granularity={granularity})")
        data = fetch_historical_data(
            product_id=symbol,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity
        )
        
        if data is None or data.empty:
            logger.error("Failed to fetch data or data is empty")
            return pd.DataFrame(), {}
            
        logger.info(f"Successfully fetched {len(data)} data points")
        
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame(), {}
    
    # Step 2: Generate parameter grid
    param_combinations = create_parameter_grid(
        size=grid_size,
        is_quick_test=is_quick_test
    )
    
    # Limit the number of combinations if needed
    if len(param_combinations) > max_combinations and not is_quick_test:
        import random
        logger.warning(f"Limiting to {max_combinations} out of {len(param_combinations)} parameter combinations")
        param_combinations = random.sample(param_combinations, max_combinations)
    
    logger.info(f"Testing {len(param_combinations)} parameter combinations")
    
    # Step 3: Run evaluations for each parameter combination
    results = []
    best_params = {}
    
    for i, params in enumerate(param_combinations):
        logger.info(f"Evaluating parameter combination {i+1}/{len(param_combinations)}")
        
        # Create configuration with these parameters
        try:
            config = EdgeConfig(
                granularity_str=timeframe,
                **{k: v for k, v in params.items() if k in EdgeConfig.__annotations__}
            )
            
            # Configure parallel processing based on mode and number of jobs
            parallel_engine = None
            n_workers = n_jobs if n_jobs > 0 else None  # Use all cores if n_jobs=-1
            
            if n_jobs != 1:
                try:
                    if parallel_mode == 'process':
                        # Process-based parallelization (better for CPU-bound tasks)
                        parallel_engine = ProcessPoolEngine(n_workers=n_workers)
                        logger.info(f"Using process-based parallelization with {n_workers or 'all'} workers")
                    elif parallel_mode == 'thread':
                        # Thread-based parallelization (better for I/O-bound tasks)
                        parallel_engine = ThreadPoolEngine(n_workers=n_workers)
                        logger.info(f"Using thread-based parallelization with {n_workers or 'all'} workers")
                    elif parallel_mode == 'ray':
                        # Try to use Ray if available
                        try:
                            import ray
                            if not ray.is_initialized():
                                ray.init(num_cpus=n_workers)
                            logger.info(f"Using Ray-based parallelization with {n_workers or 'all'} workers")
                            # Note: Ray integration would need custom implementation beyond this example
                        except ImportError:
                            logger.warning("Ray not installed. Falling back to process-based parallelism.")
                            parallel_engine = ProcessPoolEngine(n_workers=n_workers)
                except Exception as e:
                    logger.warning(f"Failed to initialize parallel engine: {str(e)}. Running in single-process mode.")
                    n_jobs = 1
            
            # Apply caching decorator if enabled
            run_wfo_func = run_wfo
            if use_caching and hasattr(vbt.utils, 'cached'):
                run_wfo_func = vbt.utils.cached(run_wfo)
                logger.info("Using cached execution for WFO runs")
                
            # Run WFO for this parameter combination with optimized settings
            wfo_results, portfolios, _ = run_wfo_func(
                symbol=symbol,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date,
                initial_capital=INIT_CAPITAL,
                config=config,
                n_splits=n_splits,
                train_ratio=0.7,
                n_jobs=1 if parallel_engine else (n_jobs if n_jobs > 0 else N_JOBS),
                data=data,
                # Pass parallel engine if available
                **({
                    'parallel_engine': parallel_engine
                } if parallel_engine is not None else {})
            )
            
            # Extract metrics for this parameter combination
            if wfo_results and len(wfo_results) > 0:
                for wfo_result in wfo_results:
                    result = {
                        'params': params,
                        'split': wfo_result.get('split', 0),
                        'train_return': wfo_result.get('train_return', np.nan),
                        'train_sharpe': wfo_result.get('train_sharpe', np.nan),
                        'train_max_drawdown': wfo_result.get('train_max_drawdown', np.nan),
                        'test_return': wfo_result.get('test_return', np.nan),
                        'test_sharpe': wfo_result.get('test_sharpe', np.nan),
                        'test_max_drawdown': wfo_result.get('test_max_drawdown', np.nan),
                        'robustness_ratio': wfo_result.get('robustness_ratio', np.nan)
                    }
                    results.append(result)
                    
        except Exception as e:
            logger.error(f"Error evaluating parameter combination {i+1}: {str(e)}")
            continue
    
    # Step 4: Compile and analyze results
    if not results:
        logger.warning("No valid results were generated during grid search")
        return pd.DataFrame(), {}
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Calculate average metrics across splits for each parameter combination
    avg_results = []
    for i, params in enumerate(param_combinations):
        param_results = results_df[results_df['params'] == params]
        
        if not param_results.empty:
            avg_result = {
                'param_set': i+1,
                'params': str(params),
                'avg_train_return': param_results['train_return'].mean(),
                'avg_train_sharpe': param_results['train_sharpe'].mean(),
                'avg_train_drawdown': param_results['train_max_drawdown'].mean(),
                'avg_test_return': param_results['test_return'].mean(),
                'avg_test_sharpe': param_results['test_sharpe'].mean(),
                'avg_test_drawdown': param_results['test_max_drawdown'].mean(),
                'avg_robustness': param_results['robustness_ratio'].mean()
            }
            avg_results.append(avg_result)
    
    avg_results_df = pd.DataFrame(avg_results)
    
    # Find best parameter sets for different metrics
    metrics = {
        'return': 'avg_test_return',
        'sharpe': 'avg_test_sharpe',
        'drawdown': 'avg_test_drawdown',
        'robustness': 'avg_robustness'
    }
    
    for name, metric in metrics.items():
        if not avg_results_df.empty:
            if name in ['drawdown']:  # Lower is better
                best_idx = avg_results_df[metric].idxmin()
            else:  # Higher is better
                best_idx = avg_results_df[metric].idxmax()
            
            if best_idx is not None:
                best_params[name] = avg_results_df.loc[best_idx, 'params']
    
    # Save results to CSV
    output_dir = ensure_output_dir("data/results/grid_search")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(output_dir, f"grid_search_results_{timestamp}.csv")
    
    if not avg_results_df.empty:
        avg_results_df.to_csv(results_file, index=False)
        logger.info(f"Grid search results saved to {results_file}")
    
    return avg_results_df, best_params


if __name__ == "__main__":
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run parameter grid search for Edge strategy')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to run (default: BTC-USD)')
    parser.add_argument('--timeframe', type=str, default='1h', help='Timeframe to use (e.g., 1h, 4h, 1d)')
    parser.add_argument('--start_date', type=str, help='Start date (format: YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, help='End date (format: YYYY-MM-DD)')
    parser.add_argument('--n_splits', type=int, default=1, help='Number of WFO splits to run')
    parser.add_argument('--grid_size', type=str, choices=['small', 'medium', 'large'], default='small',
                      help='Parameter grid size: small (few combinations), medium (balanced), large (comprehensive)')
    parser.add_argument('--quick_test', action='store_true', help='Run a quick test with minimal data and parameters')
    parser.add_argument('--max_combinations', type=int, default=50, help='Maximum number of parameter combinations to test')
    
    args = parser.parse_args()
    
    # Set default dates if not provided
    end_date = args.end_date or datetime.now().strftime('%Y-%m-%d')
    start_date = args.start_date or (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    # Run grid search
    results_df, best_params = run_grid_search(
        symbol=args.symbol,
        timeframe=args.timeframe,
        start_date=start_date,
        end_date=end_date,
        n_splits=args.n_splits,
        grid_size=args.grid_size,
        is_quick_test=args.quick_test,
        max_combinations=args.max_combinations
    )
    
    # Print results
    print("\n=== Grid Search Results Summary ===")
    
    if results_df.empty:
        print("No valid results were generated during grid search.")
    else:
        print(f"Tested {len(results_df)} parameter combinations")
        
        # Print top 3 parameter sets by Sharpe ratio
        print("\nTop 3 Parameter Sets by Sharpe Ratio:")
        top_sharpe = results_df.sort_values('avg_test_sharpe', ascending=False).head(3)
        for i, row in top_sharpe.iterrows():
            print(f"  #{i+1}: Sharpe = {row['avg_test_sharpe']:.4f}, Return = {row['avg_test_return']:.4f}, MaxDD = {row['avg_test_drawdown']:.4f}")
            print(f"  Parameters: {row['params']}\n")
        
        # Print best parameter sets for different metrics
        print("\nBest Parameter Sets by Metric:")
        for metric, params in best_params.items():
            print(f"  Best for {metric}: {params}")
    
    print("\nGrid search completed. Results saved to data/results/grid_search/")
