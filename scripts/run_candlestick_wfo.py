#!/usr/bin/env python
"""
Candlestick Pattern Strategy - Walk-Forward Optimization Runner

This script runs walk-forward optimization (WFO) on the CandlestickPatternStrategy
using the WFO framework from wfo_edge_strategy.py.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
import multiprocessing
from itertools import product
from tqdm import tqdm
import matplotlib.pyplot as plt
import vectorbtpro as vbt

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Import WFO modules
from scripts.strategies.wfo_edge_strategy import (
    create_portfolio_for_strategy,  # New function that selects right strategy
    calculate_performance_metrics,
    analyze_parameter_stability,
    recommend_final_parameters,
    save_final_parameters,
    generate_wfo_report,
    setup_chat_provider,
    ask_chat_model
)

# Import data fetcher
try:
    from data.data_fetcher import fetch_historical_data, get_vbt_freq_str
    print("Using data_fetcher from data module")
except ImportError as e:
    print(f"Could not import data_fetcher: {e}. Using backup implementations.")
    
    def fetch_historical_data(symbol, granularity, start_date, end_date):
        """Backup implementation for fetching data"""
        print(f"Fetching data for {symbol} from {start_date} to {end_date}")
        # If data fetcher is not available, try to load test data
        test_data_path = Path(__file__).resolve().parent / 'test_data' / 'sample_ohlc_data.csv'
        if test_data_path.exists():
            df = pd.read_csv(test_data_path, index_col=0, parse_dates=True)
            return df
        else:
            # Create synthetic data
            days = pd.date_range(start=start_date, end=end_date, freq='D')
            df = pd.DataFrame(index=days)
            
            # Generate price data
            np.random.seed(42)
            close = 100.0
            closes = [close]
            
            for _ in range(1, len(days)):
                pct_change = np.random.normal(0, 0.015)
                close = close * (1 + pct_change)
                closes.append(close)
            
            df['close'] = closes
            
            # Generate open, high, low
            for i in range(len(df)):
                if i == 0:
                    df.loc[df.index[i], 'open'] = df.loc[df.index[i], 'close'] * (1 - 0.005)
                else:
                    df.loc[df.index[i], 'open'] = df.loc[df.index[i-1], 'close'] * (1 + np.random.normal(0, 0.003))
                
                price_range = df.loc[df.index[i], 'close'] * 0.02
                df.loc[df.index[i], 'high'] = max(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) + np.random.random() * price_range
                df.loc[df.index[i], 'low'] = min(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) - np.random.random() * price_range
            
            # Add volume
            df['volume'] = np.random.exponential(scale=1000000, size=len(df))
            
            return df
    
    def get_vbt_freq_str(granularity_str):
        """Backup implementation for getting vbt frequency string"""
        return "1d"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('candlestick_wfo')

# WFO Configuration
config = {
    # Data parameters
    "symbol": "BTC-USD",
    "granularity": "1h",
    "start_date": (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
    "end_date": datetime.now().strftime('%Y-%m-%d'),
    
    # WFO parameters
    "in_sample_days": 100,
    "out_sample_days": 40,
    "step_days": 50,
    
    # Trading parameters
    "initial_capital": 3000,
    "commission_pct": 0.001,
    "slippage_pct": 0.0005,
    
    # Strategy parameters
    "strategy_type": "candlestick",  # Use the candlestick strategy
    
    # Performance criteria
    "optimization_metric": "sharpe_ratio",
    "min_sharpe_ratio": 0.0,
    "min_total_trades": 3,
    "min_win_rate": 0.3,
    "max_drawdown": -0.35,
    
    # Optimization settings
    "use_parallel": True,
    "num_cores": max(1, multiprocessing.cpu_count() - 1)
}

# Parameter grid for optimization
param_grid = {
    # Candlestick pattern parameters
    'lookback_periods': [20, 30, 50],
    'min_strength': [0.005, 0.01, 0.02, 0.05],
    'use_strength': [True, False],
    'use_confirmation': [False],  # No confirmation for WFO to keep it simple
    
    # Risk management parameters
    'stop_loss_pct': [0.02, 0.03, 0.05],
    'take_profit_pct': [0.04, 0.06, 0.1],
    'risk_per_trade': [0.01, 0.02, 0.03]
}

def build_param_combinations(param_grid):
    """Build all parameter combinations from the grid"""
    # Get all parameter names and possible values
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    
    # Generate all combinations
    combinations = []
    for values in product(*param_values):
        combination = dict(zip(param_names, values))
        combinations.append(combination)
    
    return combinations

def create_wfo_splits(data, in_sample_days, out_sample_days, step_days):
    """Create walk-forward optimization splits"""
    splits = []
    
    # Calculate total number of splits
    total_days = len(data)
    start_idx = 0
    
    while start_idx + in_sample_days + out_sample_days <= total_days:
        train_start = start_idx
        train_end = start_idx + in_sample_days
        test_start = train_end
        test_end = test_start + out_sample_days
        
        train_data = data.iloc[train_start:train_end]
        test_data = data.iloc[test_start:test_end]
        
        splits.append((train_data, test_data))
        
        start_idx += step_days
    
    return splits

def evaluate_params(params, data, param_json, window_size=50, is_optimization=False, use_sizing=True):
    """Evaluate a set of parameters against the data."""
    try:
        signals = get_signals_for_params(data, params)
        df = data.copy()
        df = add_signals_columns(df, signals)
        pf = create_pf_for_candlestick_strategy(df, signals['entries'], signals['exits'], 
                                               sl_stop=params.get('stop_loss_pct', None), 
                                               tp_stop=params.get('take_profit_pct', None))
        
        if pf is None:
            logger.error("Portfolio creation failed")
            return None
        
        # Check if this is a vectorbt Portfolio or our CustomPortfolio
        # Handle different attribute access methods based on the portfolio type
        total_return = pf.total_return if hasattr(pf, 'total_return') else pf.stats.total_return if hasattr(pf, 'stats') else 0
        sharpe = pf.sharpe_ratio() if callable(getattr(pf, 'sharpe_ratio', None)) else \
                pf.stats.sharpe_ratio if hasattr(pf, 'stats') and hasattr(pf.stats, 'sharpe_ratio') else 0
        
        # Process key performance metrics
        metrics = {
            'total_return': total_return,
            'sharpe_ratio': sharpe,
            'trade_count': len(df[df['entries']]),
            'win_rate': getattr(pf, 'win_rate', lambda: 0)() if callable(getattr(pf, 'win_rate', None)) else 0,
            'max_drawdown': getattr(pf, 'drawdown', lambda: 0)() if callable(getattr(pf, 'drawdown', None)) else 0,
            'avg_profit': getattr(pf, 'avg_profit_per_trade', lambda: 0)() if callable(getattr(pf, 'avg_profit_per_trade', None)) else 0,
            'params': param_json
        }
        
        # Calculate additional metrics for optimization
        if is_optimization:
            # Calculate performance metrics over windows
            if window_size > 0 and len(df) > window_size:
                window_returns = []
                for i in range(0, len(df) - window_size, window_size):
                    window_df = df.iloc[i:i+window_size]
                    window_signals = get_signals_for_params(window_df, params)
                    window_df = add_signals_columns(window_df, window_signals)
                    window_pf = create_pf_for_candlestick_strategy(window_df, window_signals['entries'], 
                                                                 window_signals['exits'], 
                                                                 sl_stop=params.get('stop_loss_pct', None), 
                                                                 tp_stop=params.get('take_profit_pct', None))
                    if window_pf is not None:
                        window_return = window_pf.total_return if hasattr(window_pf, 'total_return') else \
                                        window_pf.stats.total_return if hasattr(window_pf, 'stats') else 0
                        window_returns.append(window_return)
                
                if window_returns:
                    # Calculate consistency as the percentage of windows with positive returns
                    metrics['consistency'] = sum(1 for r in window_returns if r > 0) / len(window_returns) if window_returns else 0
                    # Calculate stability as the standard deviation of window returns (lower is better)
                    metrics['stability'] = -np.std(window_returns) if window_returns else 0
            
            # Add trade efficiency score (reward-to-risk ratio)
            metrics['efficiency'] = metrics['total_return'] / abs(metrics['max_drawdown']) if metrics['max_drawdown'] != 0 else 0
            
            # Calculate aggregate fitness score
            metrics['fitness'] = calculate_fitness_score(metrics)
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error in evaluate_params: {str(e)}")
        return None

def find_best_params_for_split(param_combinations, train_data, test_data, split_id):
    """Find the best parameters for a specific WFO split"""
    logger.info(f"Optimizing parameters for split {split_id}")
    
    best_params = None
    best_train_metrics = None
    best_test_metrics = None
    best_score = -np.inf
    
    # Process each parameter combination
    for params in tqdm(param_combinations, desc=f"Split {split_id} Progress"):
        train_metrics, test_metrics = evaluate_parameter_set(params, train_data, test_data)
        
        if train_metrics is not None and test_metrics is not None:
            # Use specified optimization metric
            score = test_metrics[config["optimization_metric"]]
            
            if score > best_score:
                best_score = score
                best_params = params.copy()
                best_train_metrics = train_metrics
                best_test_metrics = test_metrics
    
    if best_params is not None:
        logger.info(f"Best parameters for split {split_id}:")
        logger.info(f"Parameters: {best_params}")
        logger.info(f"Training {config['optimization_metric']}: {best_train_metrics[config['optimization_metric']]}")
        logger.info(f"Testing {config['optimization_metric']}: {best_test_metrics[config['optimization_metric']]}")
    else:
        logger.warning(f"No valid parameter set found for split {split_id}")
    
    return best_params, best_train_metrics, best_test_metrics

def run_process_split(args):
    """Process a single split (for parallel execution)"""
    param_combinations, train_data, test_data, split_id = args
    return find_best_params_for_split(param_combinations, train_data, test_data, split_id)

def run_wfo():
    """Run the Walk-Forward Optimization process"""
    logger.info("Starting Walk-Forward Optimization for Candlestick Pattern Strategy")
    
    # Set the strategy type globally in the wfo_edge_strategy module
    import scripts.strategies.wfo_edge_strategy as wfo_module
    wfo_module.STRATEGY_TYPE = config["strategy_type"]
    
    # Instead of fetching data, use test data
    logger.info("Loading test data for optimization")
    try:
        from scripts.test_candle_patterns import load_test_data
        data = load_test_data()
        logger.info(f"Loaded test data with {len(data)} data points")
    except Exception as e:
        logger.error(f"Error loading test data: {e}")
        return None
    
    # Create WFO splits
    splits = create_wfo_splits(
        data,
        config['in_sample_days'],
        config['out_sample_days'],
        config['step_days']
    )
    
    logger.info(f"Created {len(splits)} WFO splits")
    
    # Build parameter combinations
    param_combinations = build_param_combinations(param_grid)
    logger.info(f"Generated {len(param_combinations)} parameter combinations")
    
    # Run optimization for each split
    all_best_params = []
    train_portfolios = []
    test_portfolios = []
    
    # Prepare arguments for parallel processing
    split_args = [(param_combinations, train_data, test_data, i) 
                 for i, (train_data, test_data) in enumerate(splits)]
    
    if config['use_parallel']:
        logger.info(f"Running optimization in parallel with {config['num_cores']} cores")
        with multiprocessing.Pool(config['num_cores']) as pool:
            results = pool.map(run_process_split, split_args)
    else:
        logger.info("Running optimization sequentially")
        results = [run_process_split(args) for args in split_args]
    
    # Process results
    for split_id, (best_params, best_train_metrics, best_test_metrics) in enumerate(results):
        if best_params is not None:
            all_best_params.append(best_params)
            
            train_data, test_data = splits[split_id]
            
            # Create best portfolios for reporting
            best_train_portfolio = create_portfolio_for_strategy(train_data, best_params, config["initial_capital"])
            best_test_portfolio = create_portfolio_for_strategy(test_data, best_params, config["initial_capital"])
            
            train_portfolios.append((best_train_portfolio, best_train_metrics, best_params, split_id))
            test_portfolios.append((best_test_portfolio, best_test_metrics, best_params, split_id))
    
    # Check if any valid parameters were found
    if len(all_best_params) == 0:
        logger.error("No valid parameter sets found across any split. Try relaxing performance criteria.")
        return
    
    # Analyze parameter stability
    logger.info("Analyzing parameter stability")
    stability_metrics = analyze_parameter_stability(all_best_params)
    
    # Recommend final parameters
    logger.info("Generating final parameter recommendations")
    final_params = recommend_final_parameters(all_best_params, stability_metrics)
    
    # Save final parameters
    save_final_parameters(final_params)
    
    # Generate comprehensive report
    generate_wfo_report(train_portfolios, test_portfolios, all_best_params)
    
    # Generate charts with aggregate results
    generate_wfo_charts(test_portfolios)
    
    # Get AI insights if available
    if setup_chat_provider():
        get_ai_insights(all_best_params, stability_metrics, final_params)
    
    logger.info("Walk-Forward Optimization complete!")
    
    return final_params, train_portfolios, test_portfolios

def generate_wfo_charts(test_portfolios):
    """Generate charts visualizing WFO performance"""
    try:
        # Create output directory
        output_dir = Path('output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract metrics
        metrics = []
        for portfolio, portfolio_metrics, params, split_id in test_portfolios:
            metrics.append({
                'split_id': split_id,
                'total_return': portfolio_metrics['total_return'],
                'sharpe_ratio': portfolio_metrics['sharpe'],
                'max_drawdown': portfolio_metrics['max_dd'],
                'win_rate': portfolio_metrics['win_rate'],
                'num_trades': portfolio_metrics['num_trades']
            })
        
        metrics_df = pd.DataFrame(metrics)
        
        # Plot metrics over splits
        plt.figure(figsize=(12, 10))
        
        plt.subplot(2, 2, 1)
        plt.plot(metrics_df['split_id'], metrics_df['total_return'], marker='o')
        plt.title('Total Return by Split')
        plt.xlabel('Split ID')
        plt.ylabel('Total Return')
        plt.grid(True)
        
        plt.subplot(2, 2, 2)
        plt.plot(metrics_df['split_id'], metrics_df['sharpe_ratio'], marker='o', color='green')
        plt.title('Sharpe Ratio by Split')
        plt.xlabel('Split ID')
        plt.ylabel('Sharpe Ratio')
        plt.grid(True)
        
        plt.subplot(2, 2, 3)
        plt.plot(metrics_df['split_id'], metrics_df['win_rate'], marker='o', color='purple')
        plt.title('Win Rate by Split')
        plt.xlabel('Split ID')
        plt.ylabel('Win Rate')
        plt.grid(True)
        
        plt.subplot(2, 2, 4)
        plt.plot(metrics_df['split_id'], metrics_df['num_trades'], marker='o', color='orange')
        plt.title('Number of Trades by Split')
        plt.xlabel('Split ID')
        plt.ylabel('Number of Trades')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'wfo_metrics_chart.png')
        plt.close()
        
        logger.info("WFO charts saved to output directory")
    
    except Exception as e:
        logger.error(f"Error generating WFO charts: {e}")

def get_ai_insights(all_best_params, stability_metrics, final_params):
    """Get AI insights on WFO results"""
    try:
        # Prepare context
        context = {
            "parameter_sets": len(all_best_params),
            "stability_metrics": stability_metrics,
            "final_params": final_params,
            "strategy_type": config["strategy_type"]
        }
        
        # Ask for insights
        logger.info("Getting AI insights on optimization results...")
        query = """
        Analyze these Walk-Forward Optimization results for a candlestick pattern trading strategy:
        1. What patterns do you notice in parameter stability?
        2. What recommendations would you make for improving the strategy?
        3. Which parameters seem most important for performance?
        4. Are there any potential issues or concerns with these results?
        5. How might these results be affected by market conditions?
        
        Keep your analysis focused on the parameters and their stability across splits.
        """
        
        insights = ask_chat_model(query, context)
        
        # Save insights to file
        output_dir = Path('output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / 'wfo_ai_insights.txt', 'w') as f:
            f.write(insights)
        
        logger.info("AI insights saved to output/wfo_ai_insights.txt")
        
    except Exception as e:
        logger.error(f"Error getting AI insights: {e}")

def calculate_fitness_score(metrics):
    """
    Calculate an overall fitness score for parameter optimization.
    
    Args:
        metrics: Dictionary of performance metrics
        
    Returns:
        Fitness score (higher is better)
    """
    # Define weights for different metrics
    weights = {
        'total_return': 0.40,    # 40% weight on total return
        'sharpe_ratio': 0.20,    # 20% weight on risk-adjusted performance
        'consistency': 0.15,     # 15% weight on consistently positive windows
        'stability': 0.10,       # 10% weight on low variation between windows
        'efficiency': 0.10,      # 10% weight on return per unit of drawdown risk
        'win_rate': 0.05        # 5% weight on win rate
    }
    
    # Normalize metrics to 0-1 scale where possible
    normalized = {
        'total_return': min(max(metrics.get('total_return', 0), 0), 1),  # Cap at 100% return for normalization
        'sharpe_ratio': min(max(metrics.get('sharpe_ratio', 0) / 3.0, 0), 1),  # Normalize to 0-1 with 3.0 being excellent
        'consistency': metrics.get('consistency', 0),  # Already 0-1
        'stability': min(max(metrics.get('stability', 0) / -0.2 + 1, 0), 1),  # Convert negative values to positive 0-1
        'efficiency': min(metrics.get('efficiency', 0), 5) / 5,  # Cap at 5:1 ratio and normalize
        'win_rate': metrics.get('win_rate', 0)  # Already 0-1
    }
    
    # Calculate weighted sum
    fitness = sum(normalized[metric] * weight for metric, weight in weights.items() if metric in normalized)
    
    # Apply penalties for extreme values
    # Penalty for too few trades
    if metrics.get('trade_count', 0) < 5:
        fitness *= max(0.5, metrics.get('trade_count', 0) / 10)
    
    # Penalty for excessive drawdown
    if metrics.get('max_drawdown', 0) < -0.25:  # If drawdown worse than -25%
        fitness *= max(0.5, 1 - (abs(metrics.get('max_drawdown', 0)) - 0.25))
        
    return fitness

if __name__ == "__main__":
    final_params, train_portfolios, test_portfolios = run_wfo() 