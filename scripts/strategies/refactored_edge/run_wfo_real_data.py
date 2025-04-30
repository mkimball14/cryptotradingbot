#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WFO Runner with Real Data

This script runs the Walk-Forward Optimization pipeline with real Coinbase data
and creates visualizations of the results, leveraging the refactored modular components.

The runner supports regime-aware parameter adaptation and uses the signals_integration
module for signal generation with configurable strictness levels.

Author: Max Kimball
Date: 2025-04-29
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import vectorbtpro as vbt
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Any, Optional, Union

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("wfo_real_data_runner")

# Add the project root to the path to ensure imports work correctly
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import WFO components using relative imports where appropriate
from scripts.strategies.refactored_edge.wfo import run_wfo
from scripts.strategies.refactored_edge.config import EdgeConfig, OPTIMIZATION_PARAMETER_GRID
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.regime import determine_market_regime, determine_market_regime_advanced, MarketRegimeType
from scripts.strategies.refactored_edge.wfo_utils import (
    SYMBOL, TIMEFRAME, START_DATE, END_DATE, INIT_CAPITAL, N_JOBS,
    WFO_TRAIN_POINTS, WFO_TEST_POINTS, STEP_POINTS, get_adaptive_window_size,
    ensure_output_dir, is_testing_mode
)
from scripts.strategies.refactored_edge.utils import validate_dataframe, with_error_handling

# Define RESULTS_FILENAME constant
RESULTS_FILENAME = "wfo_results.csv"

# Import data fetcher
from scripts.strategies.refactored_edge.data.data_fetcher import fetch_historical_data

def visualize_wfo_results(results_file: str, output_dir: Optional[str] = None) -> None:
    """
    Create visualizations of WFO results with regime information.
    
    Args:
        results_file: Path to the WFO results CSV file
        output_dir: Directory to save visualizations, created if it doesn't exist
    """
    logger.info(f"Visualizing WFO results from {results_file}")
    
    # Ensure output directory exists
    output_dir = ensure_output_dir(output_dir)
    
    try:
        # Read results data
        results_df = pd.read_csv(results_file)
        
        if results_df.empty:
            logger.error("Results file is empty")
            return
            
        logger.info(f"Loaded results with {len(results_df)} splits")
        
        # 1. Performance Metrics by Split
        plt.figure(figsize=(14, 8))
        
        # Plot returns
        plt.subplot(3, 1, 1)
        plt.plot(results_df['split'], results_df['train_return'], 'b-', marker='o', label='Train Return')
        plt.plot(results_df['split'], results_df['test_return'], 'r-', marker='x', label='Test Return')
        plt.xlabel('Split Number')
        plt.ylabel('Return (%)')
        plt.title('WFO Performance: Train vs Test Returns')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Plot Sharpe ratio
        plt.subplot(3, 1, 2)
        plt.plot(results_df['split'], results_df['train_sharpe'], 'b-', marker='o', label='Train Sharpe')
        plt.plot(results_df['split'], results_df['test_sharpe'], 'r-', marker='x', label='Test Sharpe')
        plt.xlabel('Split Number')
        plt.ylabel('Sharpe Ratio')
        plt.title('WFO Performance: Train vs Test Sharpe Ratio')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Plot Max Drawdown
        plt.subplot(3, 1, 3)
        plt.plot(results_df['split'], results_df['train_max_drawdown'], 'b-', marker='o', label='Train Max DD')
        plt.plot(results_df['split'], results_df['test_max_drawdown'], 'r-', marker='x', label='Test Max DD')
        plt.xlabel('Split Number')
        plt.ylabel('Max Drawdown (%)')
        plt.title('WFO Performance: Train vs Test Max Drawdown')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.tight_layout()
        metrics_file = os.path.join(output_dir, 'wfo_performance_metrics.png')
        plt.savefig(metrics_file)
        logger.info(f"Saved performance metrics chart to {metrics_file}")
        
        # 2. Robustness Analysis
        plt.figure(figsize=(14, 6))
        
        plt.subplot(1, 2, 1)
        plt.scatter(results_df['train_sharpe'], results_df['test_sharpe'])
        plt.xlabel('Train Sharpe')
        plt.ylabel('Test Sharpe')
        plt.title('Robustness: Train vs Test Sharpe')
        plt.grid(True, alpha=0.3)
        
        # Add 45-degree line
        min_val = min(results_df['train_sharpe'].min(), results_df['test_sharpe'].min())
        max_val = max(results_df['train_sharpe'].max(), results_df['test_sharpe'].max())
        plt.plot([min_val, max_val], [min_val, max_val], 'g--', alpha=0.5)
        
        # Calculate robustness metrics
        robustness_ratio = results_df['test_sharpe'] / results_df['train_sharpe']
        sign_consistent = (results_df['train_sharpe'] * results_df['test_sharpe']) > 0
        
        plt.subplot(1, 2, 2)
        # Filter out NaN, inf and -inf values before plotting
        valid_robustness = robustness_ratio[~np.isnan(robustness_ratio) & ~np.isinf(robustness_ratio)]
        
        if len(valid_robustness) > 0:
            plt.hist(valid_robustness, bins=min(10, len(valid_robustness)))
            plt.axvline(x=1.0, color='g', linestyle='--', alpha=0.7) # Ideal ratio = 1.0
        else:
            # If no valid data, display a message instead of plotting
            plt.text(0.5, 0.5, 'No valid robustness data available', 
                     ha='center', va='center', transform=plt.gca().transAxes)
            logger.warning("No valid robustness ratio data for histogram.")
            
        plt.xlabel('Test/Train Sharpe Ratio')
        plt.ylabel('Frequency')
        plt.title('Robustness Ratio Distribution')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        robustness_file = os.path.join(output_dir, 'wfo_robustness_analysis.png')
        plt.savefig(robustness_file)
        logger.info(f"Saved robustness analysis chart to {robustness_file}")
        
        # 3. Parameter Stability Analysis
        # Extract parameter values from the string representation
        param_columns = {}
        
        # Try to extract common parameter values
        for split_idx, param_str in enumerate(results_df['best_params']):
            try:
                # Convert string representation to dictionary safely
                param_str = param_str.replace('nan', 'None')
                param_dict = eval(param_str) if isinstance(param_str, str) else {}
                
                # Add each parameter as a column
                for param_name, param_value in param_dict.items():
                    if param_name not in param_columns:
                        param_columns[param_name] = [None] * len(results_df)
                    param_columns[param_name][split_idx] = param_value
            except Exception as e:
                logger.warning(f"Could not parse parameters for split {split_idx+1}: {e}")
        
        # Add parameter columns to the results DataFrame
        for param_name, values in param_columns.items():
            results_df[f'param_{param_name}'] = values
        
        # Select numeric parameter columns
        param_cols = [col for col in results_df.columns if col.startswith('param_') 
                     and pd.api.types.is_numeric_dtype(results_df[col])]
        
        if param_cols:
            # Create a parameter stability chart
            plt.figure(figsize=(14, 8))
            
            # Plot each parameter over splits
            for i, param_col in enumerate(param_cols):
                param_name = param_col.replace('param_', '')
                plt.subplot(len(param_cols), 1, i+1)
                plt.plot(results_df['split'], results_df[param_col], marker='o')
                plt.ylabel(param_name)
                plt.grid(True, alpha=0.3)
                
                # Calculate stability metrics
                param_mean = results_df[param_col].mean()
                param_std = results_df[param_col].std()
                param_cv = param_std / param_mean if param_mean != 0 else float('nan')
                plt.title(f'{param_name} Stability (CV: {param_cv:.3f})')
            
            plt.xlabel('Split Number')
            plt.tight_layout()
            param_stability_file = os.path.join(output_dir, 'wfo_parameter_stability.png')
            plt.savefig(param_stability_file)
            logger.info(f"Saved parameter stability chart to {param_stability_file}")
        else:
            logger.warning("No numeric parameters found for stability analysis")
            
        # 4. Regime Analysis (if available in the results)
        if 'regime_breakdown' in results_df.columns or 'regime_aware_improvement' in results_df.columns:
            try:
                plt.figure(figsize=(14, 6))
                
                # Plot regime-aware improvement if available
                if 'regime_aware_improvement' in results_df.columns:
                    plt.subplot(1, 2, 1)
                    plt.bar(results_df['split'], results_df['regime_aware_improvement'])
                    plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
                    plt.xlabel('Split Number')
                    plt.ylabel('Improvement (%)')
                    plt.title('Regime-Aware Parameter Adaptation Improvement')
                    plt.grid(True, alpha=0.3)
                
                # Parse and plot regime breakdown if available
                if 'regime_breakdown' in results_df.columns:
                    # This is a simplified approach - in practice, you'd need a more robust parser
                    regime_data = []
                    for split_idx, regime_str in enumerate(results_df['regime_breakdown']):
                        try:
                            if isinstance(regime_str, str) and regime_str.strip():
                                regime_dict = eval(regime_str.replace('nan', 'None'))
                                regime_dict['split'] = split_idx + 1
                                regime_data.append(regime_dict)
                        except Exception as e:
                            logger.warning(f"Could not parse regime data for split {split_idx+1}: {e}")
                    
                    if regime_data:
                        regime_df = pd.DataFrame(regime_data)
                        
                        plt.subplot(1, 2, 2)
                        if 'trending_pct' in regime_df.columns and 'ranging_pct' in regime_df.columns:
                            plt.bar(regime_df['split'], regime_df['trending_pct'], label='Trending %')
                            plt.bar(regime_df['split'], regime_df['ranging_pct'], 
                                   bottom=regime_df['trending_pct'], label='Ranging %')
                            plt.xlabel('Split Number')
                            plt.ylabel('Percentage (%)')
                            plt.title('Market Regime Breakdown by Split')
                            plt.legend()
                            plt.grid(True, alpha=0.3)
                
                plt.tight_layout()
                regime_file = os.path.join(output_dir, 'wfo_regime_analysis.png')
                plt.savefig(regime_file)
                logger.info(f"Saved regime analysis chart to {regime_file}")
            except Exception as e:
                logger.warning(f"Error creating regime analysis chart: {e}")
        
        # 5. Create Summary Statistics Table
        summary_stats = {
            'Metric': ['Mean Return (%)', 'Mean Sharpe', 'Mean Max Drawdown (%)', 
                      'Return Std', 'Sharpe Std', 'Max Drawdown Std',
                      'Robustness Ratio Mean', 'Sign Consistency (%)'],
            'Train': [results_df['train_return'].mean(), 
                     results_df['train_sharpe'].mean(),
                     results_df['train_max_drawdown'].mean(),
                     results_df['train_return'].std(),
                     results_df['train_sharpe'].std(),
                     results_df['train_max_drawdown'].std(),
                     'N/A',
                     'N/A'],
            'Test': [results_df['test_return'].mean(), 
                    results_df['test_sharpe'].mean(),
                    results_df['test_max_drawdown'].mean(),
                    results_df['test_return'].std(),
                    results_df['test_sharpe'].std(),
                    results_df['test_max_drawdown'].std(),
                    robustness_ratio.mean() if not robustness_ratio.empty else 'N/A',
                    sign_consistent.mean() * 100 if not sign_consistent.empty else 'N/A']
        }
        
        # Add regime-specific metrics if available
        if 'regime_aware_improvement' in results_df.columns:
            summary_stats['Metric'].append('Mean Regime-Aware Improvement (%)')
            summary_stats['Train'].append('N/A')
            summary_stats['Test'].append(results_df['regime_aware_improvement'].mean())
        
        summary_df = pd.DataFrame(summary_stats)
        
        # Save summary to CSV
        summary_file = os.path.join(output_dir, 'wfo_summary_stats.csv')
        summary_df.to_csv(summary_file, index=False)
        logger.info(f"Saved summary statistics to {summary_file}")
        
        # Display summary
        logger.info("\nWFO Summary Statistics:")
        for _, row in summary_df.iterrows():
            logger.info(f"{row['Metric']}: Train = {row['Train']}, Test = {row['Test']}")
        
    except Exception as e:
        logger.error(f"Error visualizing WFO results: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_real_data_wfo(
    symbol: str = SYMBOL, 
    timeframe: str = TIMEFRAME, 
    start_date: str = START_DATE, 
    end_date: str = END_DATE, 
    initial_capital: float = INIT_CAPITAL, 
    n_splits: int = 3, 
    train_ratio: float = 0.7, 
    n_jobs: int = N_JOBS, 
    custom_train_points: Optional[int] = None, 
    custom_test_points: Optional[int] = None,
    use_regime_filter: bool = True,
    signal_strictness: SignalStrictness = SignalStrictness.BALANCED,
    grid_size: str = 'medium',
    is_quick_test: bool = False
) -> Tuple[List[Dict[str, Any]], Dict[int, Any], Dict[int, Dict[str, Any]]]:
    """
    Run Walk-Forward Optimization with real Coinbase data using refactored components.
    
    This function fetches historical data, runs WFO with regime-aware parameter adaptation,
    and visualizes the results. It leverages the refactored modular components for signal
    generation and regime detection.
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Data granularity (e.g., '1h', '4h', '1d')
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        initial_capital: Initial capital for backtesting
        n_splits: Number of WFO splits to run
        train_ratio: Train/test split ratio (e.g., 0.7 = 70% train, 30% test)
        n_jobs: Number of parallel jobs for optimization
        custom_train_points: Custom number of data points for training window
        custom_test_points: Custom number of data points for testing window
        use_regime_filter: Whether to enable regime-aware signal adaptation
        signal_strictness: Strictness level for signal generation (STRICT, BALANCED, RELAXED)
        grid_size: Parameter grid size: small (few combinations), medium (balanced), large (comprehensive)
        
    Returns:
        Tuple containing:
            - results_list: List of results dictionaries for each split
            - portfolios: Dictionary of vectorbtpro Portfolio objects for test periods, keyed by split number
            - best_params: Dictionary of best parameter dictionaries for each split, keyed by split number
    """
    logger.info(f"Fetching real Coinbase data for {symbol} from {start_date} to {end_date}")
    
    # Create config
    config = EdgeConfig()
    
    try:
        # Directly fetch data - handle possible issues with fetching
        try:
            # Convert timeframe to granularity in seconds for fetching
            granularity_map = {
                '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
                '1h': 3600, '2h': 7200, '4h': 14400, '6h': 21600, '1d': 86400
            }
            
            granularity = granularity_map.get(timeframe, 3600)  # Default to 1h if timeframe not found
            
            # Fetch data using the directly imported fetch_historical_data
            data = fetch_historical_data(
                product_id=symbol,
                start_date=start_date,
                end_date=end_date,
                granularity=granularity
            )
            
            if data is None or data.empty:
                logger.error("Failed to fetch data from Coinbase or data is empty")
                return None, None, None
                
            logger.info(f"Successfully fetched {len(data)} data points from Coinbase")
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            import traceback
            return None, None, None
            
        if data is None or data.empty:
            logger.error(f"Failed to fetch data for {symbol} from {start_date} to {end_date}")
            return None, None, None
        
        logger.info(f"Fetched {len(data)} data points with columns: {data.columns.tolist()}")
        
        # Calculate window sizes based on timeframe and available data
        # First determine roughly how many days of data we're working with
        try:
            from datetime import datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            available_days = (end_dt - start_dt).days
        except Exception as e:
            logger.warning(f"Failed to calculate date range: {e}. Using default of 90 days.")
            available_days = 90
        
        # Use adaptive window sizing logic based on timeframe and available data
        # Only use custom values if explicitly provided, otherwise use adaptive sizing
        if custom_train_points and custom_test_points:
            logger.info(f"Using custom window sizes: train={custom_train_points}, test={custom_test_points}")
            train_points = custom_train_points
            test_points = custom_test_points
            step_points = test_points
        else:
            logger.info(f"Calculating adaptive window sizes for {timeframe} timeframe with {available_days} days of data")
            train_points, test_points, step_points = get_adaptive_window_size(timeframe, available_days)
        
        # Calculate actual splits possible
        actual_splits = max(1, int((len(data) - (train_points + test_points)) / step_points) + 1)
        actual_splits = min(actual_splits, n_splits)  # Cap at requested splits
        
        logger.info(f"Running WFO with: {actual_splits} splits, "
                   f"train window: {train_points} points, "
                   f"test window: {test_points} points, "
                   f"step size: {step_points} points")
        
        # Log parameter grid size configuration
        logger.info(f"Using {grid_size} parameter grid size for optimization")
        if is_quick_test:
            logger.info("Quick test mode enabled - using minimal parameter grid")
        
        # Define window and step points for WFO
        wfo_train_points = custom_train_points or WFO_TRAIN_POINTS
        wfo_test_points = custom_test_points or WFO_TEST_POINTS
        wfo_step_points = STEP_POINTS
        
        # Log configuration
        logger.info(f"Using window sizes: train={wfo_train_points}, test={wfo_test_points}, step={wfo_step_points}")
        logger.info("Running WFO with regime-aware signal generation...")
        
        # Create config object for this run
        config = EdgeConfig(
            granularity_str=timeframe,
            signal_strictness=signal_strictness,
            use_regime_adaptation=use_regime_filter,
            use_enhanced_regimes=use_regime_filter  # Use enhanced regime detection when regime filtering is enabled
        )
        
        # Store the generated parameter combinations in the config object
        config.param_combinations = config.get_param_combinations(grid_size=grid_size, is_quick_test=is_quick_test)
        logger.info(f"Generated {len(config.param_combinations)} parameter combinations for optimization")
        
        # Run WFO with the fetched data and refactored configuration
        results, portfolios, best_params = run_wfo(
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            config=config,  # Pass the config object with parameters
            n_splits=n_splits,
            train_ratio=train_ratio,
            n_jobs=n_jobs,
            data=data  # Pass the fetched data
        )
            
        logger.info(f"WFO completed with {len(results) if results else 0} splits")
        
        # Enhance results with additional regime information if needed
        if results and use_regime_filter and isinstance(best_params, dict):
            for result in results:
                split_num = result.get('split', 0)
                # Add regime information if not already present
                if 'regime_breakdown' not in result and split_num in best_params:
                    params = best_params[split_num]
                    if isinstance(params, dict) and '_regime_info' in params:
                        result['regime_breakdown'] = str(params['_regime_info'])
        
        # Restore original WFO parameters if needed
        logger.info("Restored original WFO parameters")
        
        # Visualize the results with enhanced regime visualizations
        results_file = os.path.join(ensure_output_dir(), RESULTS_FILENAME)
        if os.path.exists(results_file):
            logger.info("Visualizing WFO results with regime information...")
            # Use ensure_output_dir() as the default output directory
            visualize_wfo_results(results_file, ensure_output_dir())
        else:
            logger.warning(f"Results file not found at {results_file}")
        
        return results, portfolios, best_params
    
    except Exception as e:
        logger.error(f"Error in run_real_data_wfo: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

if __name__ == "__main__":
    import argparse
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run WFO with real cryptocurrency data')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to run (default: BTC-USD)')
    parser.add_argument('--timeframe', type=str, default='1h', help='Timeframe to use (e.g., 1h, 4h, 1d)')
    parser.add_argument('--start_date', type=str, help='Start date (format: YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, help='End date (format: YYYY-MM-DD)')
    parser.add_argument('--n_splits', type=int, default=3, help='Number of WFO splits to run')
    parser.add_argument('--train_ratio', type=float, default=0.7, help='Train/test ratio (default: 0.7)')
    parser.add_argument('--n_jobs', type=int, default=-1, help='Number of parallel jobs (-1 for all cores)')
    parser.add_argument('--no_regime', action='store_true', help='Disable regime-aware parameter adaptation')
    parser.add_argument('--quick_test', action='store_true', help='Run a quick test with minimal data and parameters')
    parser.add_argument('--grid_size', type=str, choices=['small', 'medium', 'large'], default='medium',
                        help='Parameter grid size: small (few combinations), medium (balanced), large (comprehensive)')
    
    args = parser.parse_args()
    
    # Run WFO with real data for the past year
    print("--- Starting Walk-Forward Optimization with Real Data ---")
    
    # Use shorter time period for testing
    symbol = args.symbol
    timeframe = args.timeframe
    end_date = args.end_date or datetime.now().strftime('%Y-%m-%d')
    start_date = args.start_date or (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')  # Last 3 months
    
    print(f"Running WFO on {symbol} from {start_date} to {end_date} with {timeframe} timeframe")
    
    # Run WFO with regime-aware signal generation enabled
    results, portfolios, best_params = run_real_data_wfo(
        # Basic parameters
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        n_splits=args.n_splits,
        train_ratio=0.7,  # Use 70/30 train/test split for real data
        n_jobs=-1,        # Use all available cores
        # Window sizes for 1 year of hourly data:
        custom_train_points=1440,  # 60 days of hourly data
        custom_test_points=504,    # 21 days of hourly data
        # Regime-aware configuration:
        use_regime_filter=not args.no_regime,  # Enable regime-aware parameter adaptation
        signal_strictness=SignalStrictness.BALANCED,  # Use balanced signal generation approach
        # Grid size configuration:
        grid_size=args.grid_size,  # Use the specified grid size
        is_quick_test=args.quick_test  # Whether to use minimal parameter grid
    )
    
    if results:
        print("--- WFO with Real Data Completed Successfully ---")
        
        # Print summary of best parameters from the last split
        # Check if best_params exists and has valid entries
        if best_params and isinstance(best_params, dict) and len(best_params) > 0:
            try:
                last_split = max(best_params.keys())
                # Check if the value at last_split is None or not a dict
                if best_params[last_split] is None:
                    print(f"\nNo valid parameters found for the last split (#{last_split})")
                else:
                    print(f"\nBest parameters for the last split (#{last_split}):")
                    # Safety check to make sure the dict has an items method
                    if hasattr(best_params[last_split], 'items'):
                        for param, value in best_params[last_split].items():
                            if not param.startswith('_'):  # Skip internal parameters
                                print(f"  {param}: {value}")
                        
                        # Print regime information if available
                        if '_regime_info' in best_params[last_split]:
                            regime_info = best_params[last_split]['_regime_info']
                            if isinstance(regime_info, dict):
                                print(f"\nRegime information for the last split:")
                                for key, value in regime_info.items():
                                    print(f"  {key}: {value}")
                    else:
                        print(f"Best parameters data type: {type(best_params[last_split])}")
                        print(f"Content: {best_params[last_split]}")
            except Exception as e:
                print(f"Error while displaying best parameters: {e}")
                print(f"Best parameters data type: {type(best_params)}")
                print(f"Contents: {best_params}")
        else:
            print("\nNo valid parameter combinations were found during optimization.")
            print("Consider expanding the parameter grid or relaxing signal generation criteria.")
            print("You can also use a shorter test period or more training data.")
            if best_params is None:
                print("best_params is None")
            elif not isinstance(best_params, dict):
                print(f"best_params is not a dictionary: {type(best_params)}")
            else:
                print(f"best_params is empty: {best_params}")
                # Show the internal structure for debugging
                for k, v in best_params.items() if isinstance(best_params, dict) else []:
                    print(f"  Split {k}: {type(v)}")
        
    else:
        print("--- WFO with Real Data Failed ---")
