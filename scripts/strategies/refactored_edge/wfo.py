"""
Core Walk-Forward Optimization (WFO) orchestration module.

This module contains the main run_wfo function and supporting functions for conducting 
Walk-Forward Optimization, including split calculation, data handling, and regime-aware
parameter adaptation.
"""
import sys
import os
import traceback
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta

# Local imports 
from scripts.strategies.refactored_edge import config, indicators, signals, regime, test_signals
from scripts.strategies.refactored_edge.wfo_utils import (
    SYMBOL, TIMEFRAME, START_DATE, END_DATE, INIT_CAPITAL, N_JOBS,
    WFO_TRAIN_POINTS, WFO_TEST_POINTS, STEP_POINTS,
    import_data_fetcher, validate_ohlc_data, calculate_wfo_points
)
from scripts.strategies.refactored_edge.wfo_evaluation import evaluate_with_params
from scripts.strategies.refactored_edge.wfo_optimization import (
    optimize_params_parallel, determine_market_regime_for_params
)
from scripts.strategies.refactored_edge.wfo_results import (
    initialize_results_storage, save_wfo_results, save_interim_results,
    print_performance_metrics, generate_summary_report
)

# Import data fetcher
fetch_historical_data, DATA_FETCHER_AVAILABLE = import_data_fetcher()


def calculate_wfo_splits(data_length, train_points, test_points, step_points, n_splits=None):
    """
    Calculate the indices for Walk-Forward Optimization splits.
    
    Args:
        data_length (int): Total number of data points
        train_points (int): Number of points for training
        test_points (int): Number of points for testing
        step_points (int): Number of points to step forward
        n_splits (int, optional): Maximum number of splits to generate
        
    Returns:
        list: List of (train_indices, test_indices) tuples
    """
    # Validate inputs
    train_points = max(1, train_points)
    test_points = max(1, test_points)
    step_points = max(1, step_points)  # Step must be at least 1
    
    initial_window_points = train_points + test_points
    
    if initial_window_points > data_length:
        print(f"ERROR: Initial window ({initial_window_points}) exceeds data length ({data_length}).")
        print(f"Please reduce train_points ({train_points}) or test_points ({test_points}),")
        print(f"or increase the date range to get more data points.")
        return []
    
    # Calculate WFO splits
    split_indices_list = []
    current_train_start_idx = 0
    split_count = 0
    
    while True:
        # Calculate indices for this split
        train_start_idx = current_train_start_idx
        train_end_idx = train_start_idx + train_points
        test_start_idx = train_end_idx
        test_end_idx = test_start_idx + test_points
        
        # Check if we've reached the end of the data
        if test_end_idx > data_length:
            # If we can't fit a full test set, stop here
            break
        
        # Create index arrays for train and test sets
        train_indices = range(train_start_idx, train_end_idx)
        test_indices = range(test_start_idx, test_end_idx)
        
        # Print split information
        print(f"Split {split_count + 1}: Train [{train_start_idx}:{train_end_idx}], Test [{test_start_idx}:{test_end_idx}]")
        
        # Add to our list
        split_indices_list.append((train_indices, test_indices))
        split_count += 1
        
        # Check if we've reached the requested number of splits
        if n_splits is not None and split_count >= n_splits:
            break
        
        # Move the window start for the next iteration
        current_train_start_idx += step_points
    
    print(f"Manually generated {len(split_indices_list)} splits.")
    return split_indices_list


def fetch_data(symbol, timeframe, start_date, end_date, data=None):
    """
    Fetch or validate data for WFO.
    
    Args:
        symbol (str): Trading symbol
        timeframe (str): Data granularity
        start_date (str): Start date
        end_date (str): End date
        data (pd.DataFrame, optional): Data to use if provided
        
    Returns:
        pd.DataFrame: Price data
    """
    if data is not None:
        print("Using provided data for WFO")
        
        # Validate that the data has the required columns
        is_valid, _ = validate_ohlc_data(data)
        
        if not is_valid:
            raise ValueError("Provided data is missing required OHLC columns")
        
        # Basic data validation
        print(f"Data validated: {len(data)} data points with columns {list(data.columns)}")
        return data
    
    if not DATA_FETCHER_AVAILABLE:
        raise ImportError("Data fetcher is not available. Cannot fetch historical data.")
    
    print(f"Fetching data for {symbol} {timeframe} from {start_date} to {end_date}...")
    
    try:
        # Fetch historical data using data_fetcher
        price_data = fetch_historical_data(
            product_id=symbol,  # Use product_id parameter for Coinbase Advanced API
            granularity=timeframe,
            start=start_date,
            end=end_date
        )
        
        # Validate that the data has the required columns
        is_valid, _ = validate_ohlc_data(price_data)
        
        if not is_valid:
            raise ValueError(f"Fetched data is missing required OHLC columns. Found: {list(price_data.columns)}")
        
        print(f"Successfully fetched {len(price_data)} data points")
        return price_data
    
    except Exception as e:
        print(f"Error during data fetching: {str(e)}")
        traceback.print_exc()
        raise


def run_wfo(symbol=SYMBOL, timeframe=TIMEFRAME, start_date=START_DATE, end_date=END_DATE, 
            initial_capital=INIT_CAPITAL, config=None, n_splits=4, train_ratio=0.8, 
            n_jobs=N_JOBS, data=None):
    """
    Run Walk-Forward Optimization with the Edge Multi-Factor strategy.
    
    Args:
        symbol (str): Trading symbol (e.g., 'BTC-USD')
        timeframe (str): Data granularity (e.g., '1h', '4h', '1d')
        start_date (str): Start date for data fetch
        end_date (str): End date for data fetch
        initial_capital (float): Initial capital for backtesting
        config (EdgeConfig, optional): Configuration object with parameters
        n_splits (int): Number of WFO splits
        train_ratio (float): Ratio of training to total window size
        n_jobs (int): Number of parallel jobs for optimization
        data (pd.DataFrame, optional): Data to use if already fetched
        
    Returns:
        tuple: (all_results, test_portfolios, best_params)
    """
    # Initialize results storage
    results_dir = initialize_results_storage()
    print(f"Results will be saved to: {os.path.join(results_dir, 'wfo_results.csv')}")
    
    # Step 1: Get data
    print("Getting data...")
    try:
        price_data = fetch_data(symbol, timeframe, start_date, end_date, data)
    except Exception as e:
        print(f"Error during data fetching: {str(e)}")
        traceback.print_exc()
        return [], {}, {}
    
    # Step 2: Calculate WFO splits
    print("Splitting data for Walk-Forward Optimization...")
    
    # Calculate the number of points for train/test based on timeframe
    if data is None:  # Only recalculate if we're not using provided data
        train_points, test_points, step_points = calculate_wfo_points(
            timeframe, train_days=240, test_days=60
        )
    else:
        # Use the predefined global constants if data is provided
        train_points, test_points, step_points = WFO_TRAIN_POINTS, WFO_TEST_POINTS, STEP_POINTS
    
    # Adjust train/test points if train_ratio is provided
    if train_ratio != 0.8:  # Only adjust if different from default
        total_window = train_points + test_points
        train_points = int(total_window * train_ratio)
        test_points = total_window - train_points
    
    print(f"WFO Params (Points): Train={train_points}, Test={test_points}, Step={step_points}, Initial Window={train_points + test_points}")
    
    # Calculate the splits
    split_indices_list = calculate_wfo_splits(
        data_length=len(price_data),
        train_points=train_points,
        test_points=test_points,
        step_points=step_points,
        n_splits=n_splits
    )
    
    if not split_indices_list:
        print("No valid splits could be generated. Exiting.")
        return [], {}, {}
    
    # Step 3: Get parameter combinations to test
    # Use provided config or create default from config module
    param_config = config if config else config.EdgeConfig()
    param_grid_list = param_config.get_param_combinations()
    
    print(f"Total parameter combinations to evaluate per split: {len(param_grid_list)}")
    
    # --- Prepare for Walk-Forward Loop ---
    results_list = []  # To store all split results
    test_portfolios = {}  # To store test portfolios
    all_best_params = {}  # To store best parameters for each split
    
    print("\n--- Starting Walk-Forward Optimization Loop ---\n")
    
    # --- Walk-Forward Optimization Loop ---
    for split_num, (train_indices, test_indices) in enumerate(split_indices_list):
        # Create descriptive split information
        split_info = f"Split {split_num + 1}/{len(split_indices_list)}"
        print(f"\nProcessing {split_info}")
        
        # Get training and test data
        train_data = price_data.iloc[train_indices].copy()
        test_data = price_data.iloc[test_indices].copy()
        
        # Print split details
        print(f"Train: {len(train_data)} points, Test: {len(test_data)} points")
        
        # Convert indices to dates if datetime index is available
        if hasattr(price_data.index, 'min') and hasattr(price_data.index, 'max'):
            train_start_date = train_data.index.min()
            train_end_date = train_data.index.max()
            test_start_date = test_data.index.min()
            test_end_date = test_data.index.max()
            
            print(f"Train Period: {train_start_date} to {train_end_date}")
            print(f"Test Period: {test_start_date} to {test_end_date}")
        
        # --- 4a. Parameter Optimization ---
        print(f"Starting parameter optimization for split {split_num + 1}...")
        
        # Add market regime information to each parameter set
        # This requires the wfo_optimization module
        from scripts.strategies.refactored_edge.wfo_optimization import determine_market_regime_for_params
        
        # Assuming param_config is the correct EdgeConfig instance for this split
        # Pass the config object to the regime determination function
        regime_info = determine_market_regime_for_params(train_data, param_config)
        
        # Add regime info to the parameters dictionary if needed for evaluation?
        # The current evaluate_single_params doesn't seem to use it directly,
        # but it might be logged or used later.
        # If evaluate_single_params needed it, we'd modify param_grid_list here.
        # For now, we just determine it as per the original structure.
        
        # Prepare arguments for parallel execution
        for params in param_grid_list:
            # Add regime information to parameters
            params['_regime_info'] = regime_info
        
        # Optimize parameters on training data
        best_params, best_score, best_params_by_regime = optimize_params_parallel(
            data=train_data,
            param_combinations=param_grid_list,
            metric='Sharpe Ratio',
            n_jobs=n_jobs
        )
        
        # Store best parameters
        all_best_params[split_num] = best_params
        
        # Check if optimization failed
        if best_params is None:
            print(f"No valid parameters found for split {split_num + 1}. Skipping to next split.")
            
            # Add empty result to maintain split tracking
            results_list.append({
                'split': split_num + 1,
                'train_start': train_start_date if 'train_start_date' in locals() else None,
                'train_end': train_end_date if 'train_end_date' in locals() else None,
                'test_start': test_start_date if 'test_start_date' in locals() else None,
                'test_end': test_end_date if 'test_end_date' in locals() else None,
                'best_params': str({}),
                'train_return': np.nan,
                'train_sharpe': np.nan,
                'train_max_drawdown': np.nan,
                'test_return': np.nan,
                'test_sharpe': np.nan,
                'test_max_drawdown': np.nan,
                'regime_aware_improvement': np.nan,
                'robustness_ratio': np.nan,
                'return_std': np.nan,
                'sharpe_std': np.nan,
                'consistent_sign': False,
                'regime_breakdown': {}
            })
            
            # Save interim results
            save_interim_results(results_list, split_num + 1)
            continue
        
        # Print detailed parameter information
        print(f"Best parameters for split {split_num + 1}:")
        for param, value in best_params.items():
            if not param.startswith('_'):  # Skip internal keys like _regime_info
                print(f"  {param}: {value}")
        
        # Check if we have regime-specific parameters and display them
        if len(best_params_by_regime) > 1:  # More than just 'overall'
            if 'trending' in best_params_by_regime:
                trending_params = best_params_by_regime['trending']
                print("Trending regime parameters:")
                for param, value in trending_params.items():
                    if 'ranging' in best_params_by_regime and param in best_params_by_regime['ranging'] and best_params_by_regime['ranging'][param] != value:
                        print(f"  {param}: {value} (ranging: {best_params_by_regime['ranging'][param]})")
        
        # --- 4b. Test Period Evaluation with Best Parameters ---
        print(f"Evaluating test period with best parameters...")
        
        # Standard evaluation with overall best parameters
        test_pf, test_stats = evaluate_with_params(test_data, best_params)
        
        # Get standard (non-regime) performance metrics
        standard_return = test_stats.get('return', 0)
        standard_sharpe = test_stats.get('sharpe', -np.inf)
        standard_drawdown = test_stats.get('max_drawdown', 1.0)
        
        print(f"Test period results with best parameters:")
        print(f"  Return: {standard_return:.4f}")
        print(f"  Sharpe: {standard_sharpe:.4f}")
        print(f"  Max Drawdown: {standard_drawdown:.4f}")
        
        # Store the portfolio for this split
        test_portfolios[split_num] = test_pf
        
        # --- 4c. Anti-Overfitting Analysis ---
        print("Performing anti-overfitting analysis...")
        
        # Check if best_train_stats is a dictionary or scalar
        train_return = np.nan
        train_sharpe = np.nan
        train_max_drawdown = np.nan
        return_std = np.nan
        sharpe_std = np.nan
        consistent_sign = False
        
        print(f"DEBUG: best_train_stats type: {type(best_score)}")
        
        # Extract metrics if best_train_stats is a dictionary
        if isinstance(best_score, dict):
            train_return = best_score.get('return', np.nan)
            train_sharpe = best_score.get('sharpe', np.nan)
            train_max_drawdown = best_score.get('max_drawdown', np.nan)
            
            # Get cross-validation metrics from optimization (if available)
            return_std = best_score.get('return_std', np.nan)
            sharpe_std = best_score.get('sharpe_std', np.nan)
            consistent_sign = best_score.get('consistent_sign', False)
        elif hasattr(best_score, 'item'):
            # If it's a numpy scalar, use it as Sharpe ratio
            print("Using scalar best_train_stats as Sharpe ratio")
            train_sharpe = best_score.item() if hasattr(best_score, 'item') else float(best_score)
        
        # Calculate robustness ratio (test/train performance)
        robustness_ratio = np.nan
        
        if not np.isnan(train_sharpe) and train_sharpe != 0 and not np.isnan(standard_sharpe):
            robustness_ratio = standard_sharpe / train_sharpe if train_sharpe > 0 else -standard_sharpe / train_sharpe
        
        # Calculate improvement from regime-aware adaptation
        regime_improvement = 0.0  # Default if not using regime-aware params
        
        # --- 4e. Save Results for this Split ---
        # Compile the results for this split
        # Handle the case where best_params might be None (no valid parameter combinations found)
        params_str = "No valid parameters found"
        if best_params is not None:
            try:
                params_str = str({k: v for k, v in best_params.items() if not k.startswith('_')})
            except (AttributeError, TypeError) as e:
                print(f"Error formatting best_params: {e}")
                params_str = str(best_params)
        
        split_results = {
            'split': split_num + 1,
            'train_start': train_start_date if 'train_start_date' in locals() else None,
            'train_end': train_end_date if 'train_end_date' in locals() else None,
            'test_start': test_start_date if 'test_start_date' in locals() else None,
            'test_end': test_end_date if 'test_end_date' in locals() else None,
            'best_params': params_str,
            'train_return': train_return,
            'train_sharpe': train_sharpe,
            'train_max_drawdown': train_max_drawdown,
            'test_return': standard_return,
            'test_sharpe': standard_sharpe, 
            'test_max_drawdown': standard_drawdown,
            'regime_aware_improvement': regime_improvement,
            'robustness_ratio': robustness_ratio,
            'return_std': return_std,
            'sharpe_std': sharpe_std,
            'consistent_sign': consistent_sign,
            'regime_breakdown': best_score.get('regime_breakdown', {}) if isinstance(best_score, dict) else {}
        }
        
        # Add to the list of results
        results_list.append(split_results)
        
        # Save interim results after each split (in case of early termination)
        save_interim_results(results_list, split_num + 1)
    
    # --- End of WFO Loop, Final Processing ---
    
    # Save final results
    if results_list:
        save_wfo_results(results_list)
    
    # Print performance summary
    print_performance_metrics(results_list)
    
    # Generate and save summary report
    generate_summary_report(results_list)
    
    print("--- WFO Runner Finished ---")
    
    return results_list, test_portfolios, all_best_params


if __name__ == "__main__":
    # Example usage when running as script
    print("--- Starting Walk-Forward Optimization ---")
    results, portfolios, best_params = run_wfo()
