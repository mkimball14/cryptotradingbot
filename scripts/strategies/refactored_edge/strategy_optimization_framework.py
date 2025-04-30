#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Edge Multi-Factor Strategy Optimization Framework

This module provides a comprehensive framework for optimizing the Edge Multi-Factor
trading strategy across different market regimes, timeframes, and assets.

Author: Max Kimball
Date: 2025-04-28
"""

import os
import sys
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List, Tuple, Optional, Union, Any

# Add the parent directory to the path to ensure imports work correctly
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import WFO components and utility functions
from scripts.strategies.refactored_edge.wfo import run_wfo, calculate_wfo_splits
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.wfo_utils import (
    SYMBOL, TIMEFRAME, START_DATE, END_DATE, INIT_CAPITAL, N_JOBS,
    ensure_output_dir, standardize_column_names
)
from scripts.strategies.refactored_edge.data.data_fetcher import fetch_historical_data
from scripts.strategies.refactored_edge.regime import determine_market_regime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("strategy_optimization")

# Define output directories
OPTIMIZATION_OUTPUT_DIR = "data/optimization"
OPTIMIZATION_PLOTS_DIR = os.path.join(OPTIMIZATION_OUTPUT_DIR, "plots")
OPTIMIZATION_RESULTS_FILE = os.path.join(OPTIMIZATION_OUTPUT_DIR, "optimization_results.csv")
OPTIMIZATION_SUMMARY_FILE = os.path.join(OPTIMIZATION_OUTPUT_DIR, "optimization_summary.csv")


def ensure_optimization_dirs():
    """Ensure optimization directories exist."""
    os.makedirs(OPTIMIZATION_OUTPUT_DIR, exist_ok=True)
    os.makedirs(OPTIMIZATION_PLOTS_DIR, exist_ok=True)
    logger.info(f"Optimization directories created/verified.")


class StrategyOptimizer:
    """
    Edge Multi-Factor Strategy Optimizer
    
    This class provides methods for systematic strategy optimization,
    performance evaluation, and regime-aware parameter adaptation.
    """
    
    def __init__(self, 
                 symbols: List[str] = None,
                 timeframes: List[str] = None,
                 start_date: str = None,
                 end_date: str = None,
                 train_days: List[int] = None,
                 test_days: List[int] = None,
                 initial_capital: float = 10000.0,
                 n_jobs: int = -1):
        """
        Initialize the strategy optimizer.
        
        Args:
            symbols: List of trading symbols to optimize for
            timeframes: List of timeframes to optimize on
            start_date: Start date for historical data
            end_date: End date for historical data
            train_days: List of training window sizes (in days) to test
            test_days: List of testing window sizes (in days) to test
            initial_capital: Initial capital for backtesting
            n_jobs: Number of parallel jobs for optimization
        """
        # Set default values if not provided
        self.symbols = symbols or ['BTC-USD', 'ETH-USD']
        self.timeframes = timeframes or ['1h', '4h', '1d']
        self.start_date = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.train_days = train_days or [60, 90, 120]
        self.test_days = test_days or [21, 30, 45]
        self.initial_capital = initial_capital
        self.n_jobs = n_jobs
        
        # Initialize results storage
        self.results = []
        self.data_cache = {}  # Cache for fetched data
        
        # Ensure output directories exist
        ensure_optimization_dirs()
        
        logger.info(f"Initialized Strategy Optimizer with {len(self.symbols)} symbols, "
                   f"{len(self.timeframes)} timeframes, and {len(self.train_days)} training windows.")
    
    def fetch_data(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        """
        Fetch historical data for a symbol and timeframe.
        
        Args:
            symbol: Trading symbol
            timeframe: Data granularity
            
        Returns:
            DataFrame with historical OHLCV data or None if fetch fails
        """
        cache_key = f"{symbol}_{timeframe}"
        
        # Return cached data if available
        if cache_key in self.data_cache:
            logger.info(f"Using cached data for {cache_key}")
            return self.data_cache[cache_key]
        
        logger.info(f"Fetching {timeframe} data for {symbol} from {self.start_date} to {self.end_date}")
        
        try:
            # Convert timeframe to granularity in seconds for fetching
            granularity_map = {
                '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
                '1h': 3600, '2h': 7200, '4h': 14400, '6h': 21600, '1d': 86400
            }
            
            granularity = granularity_map.get(timeframe, 3600)  # Default to 1h if not found
            
            # Fetch data
            data = fetch_historical_data(
                product_id=symbol,
                start_date=self.start_date,
                end_date=self.end_date,
                granularity=granularity
            )
            
            if data is None or data.empty:
                logger.error(f"Failed to fetch data for {symbol} ({timeframe})")
                return None
            
            # Standardize column names to snake_case
            data = standardize_column_names(data)
            
            # Cache the data
            self.data_cache[cache_key] = data
            
            logger.info(f"Successfully fetched {len(data)} data points for {symbol} ({timeframe})")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol} ({timeframe}): {e}")
            return None
    
    def calculate_wfo_parameters(self, timeframe: str, train_days: int, test_days: int) -> Tuple[int, int, int]:
        """
        Calculate WFO parameters (points) based on timeframe and day settings.
        
        Args:
            timeframe: Data granularity
            train_days: Number of days for training
            test_days: Number of days for testing
            
        Returns:
            Tuple of (train_points, test_points, step_points)
        """
        # Calculate points based on timeframe
        points_per_day = {
            '1m': 1440,    # 1 minute
            '5m': 288,     # 5 minutes
            '15m': 96,     # 15 minutes
            '1h': 24,      # 1 hour
            '4h': 6,       # 4 hours
            '1d': 1        # 1 day
        }
        
        # Get points per day for the timeframe
        ppd = points_per_day.get(timeframe, 24)  # Default to 1h if unknown
        
        train_points = train_days * ppd
        test_points = test_days * ppd
        step_points = test_points  # Default step size is one test period
        
        logger.info(f"Calculated WFO parameters for {timeframe}: train_points={train_points}, "
                   f"test_points={test_points}, step_points={step_points}")
        
        return train_points, test_points, step_points
    
    def run_optimization_case(self, 
                             symbol: str, 
                             timeframe: str, 
                             train_days: int, 
                             test_days: int, 
                             n_splits: int = 3) -> Dict[str, Any]:
        """
        Run a single optimization case and return results.
        
        Args:
            symbol: Trading symbol
            timeframe: Data granularity
            train_days: Number of days for training
            test_days: Number of days for testing
            n_splits: Number of WFO splits
            
        Returns:
            Dictionary with optimization results
        """
        logger.info(f"Starting optimization case: {symbol} ({timeframe}), train_days={train_days}, test_days={test_days}")
        
        # Fetch data
        data = self.fetch_data(symbol, timeframe)
        if data is None:
            logger.error(f"No data available for {symbol} ({timeframe}). Skipping optimization case.")
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'train_days': train_days,
                'test_days': test_days,
                'success': False,
                'error': 'No data available'
            }
        
        # Calculate WFO parameters
        train_points, test_points, step_points = self.calculate_wfo_parameters(timeframe, train_days, test_days)
        
        # Override WFO points in wfo_utils and wfo modules
        import scripts.strategies.refactored_edge.wfo_utils as wfo_utils
        import scripts.strategies.refactored_edge.wfo as wfo
        
        # Save original values for restoration
        original_values = {
            'wfo_utils': {
                'WFO_TRAIN_POINTS': wfo_utils.WFO_TRAIN_POINTS,
                'WFO_TEST_POINTS': wfo_utils.WFO_TEST_POINTS,
                'STEP_POINTS': wfo_utils.STEP_POINTS
            },
            'wfo': {
                'WFO_TRAIN_POINTS': wfo.WFO_TRAIN_POINTS,
                'WFO_TEST_POINTS': wfo.WFO_TEST_POINTS,
                'STEP_POINTS': wfo.STEP_POINTS
            }
        }
        
        # Set new values in both modules
        wfo_utils.WFO_TRAIN_POINTS = train_points
        wfo_utils.WFO_TEST_POINTS = test_points
        wfo_utils.STEP_POINTS = step_points
        wfo.WFO_TRAIN_POINTS = train_points
        wfo.WFO_TEST_POINTS = test_points
        wfo.STEP_POINTS = step_points
        
        try:
            # Create default config
            config = EdgeConfig()
            
            # Calculate how many splits we can reasonably have
            data_length = len(data)
            total_needed = train_points + test_points
            max_possible_splits = (data_length - total_needed) // step_points + 1
            actual_splits = min(n_splits, max_possible_splits)
            
            if actual_splits < 1:
                logger.error(f"Not enough data for even 1 split. Skipping optimization case.")
                return {
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'train_days': train_days,
                    'test_days': test_days,
                    'success': False,
                    'error': 'Not enough data for splits'
                }
            
            # Run WFO
            results, portfolios, best_params = run_wfo(
                symbol=symbol,
                timeframe=timeframe,
                start_date=self.start_date,
                end_date=self.end_date,
                initial_capital=self.initial_capital,
                config=config,
                n_splits=actual_splits,
                train_ratio=0.7,  # Use 70/30 train/test split
                n_jobs=self.n_jobs,
                data=data
            )
            
            # Process results
            if not results:
                logger.warning(f"No results returned for {symbol} ({timeframe})")
                return {
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'train_days': train_days,
                    'test_days': test_days,
                    'success': False,
                    'error': 'No results returned'
                }
            
            # Calculate performance metrics
            avg_train_return = np.mean([r.get('train_return', 0) for r in results])
            avg_test_return = np.mean([r.get('test_return', 0) for r in results])
            avg_train_sharpe = np.mean([r.get('train_sharpe', 0) for r in results])
            avg_test_sharpe = np.mean([r.get('test_sharpe', 0) for r in results])
            avg_robustness = np.mean([r.get('robustness_ratio', 0) for r in results])
            
            # Detect market regime over the entire period
            regime_data = determine_market_regime(
                close=data['close'] if 'close' in data.columns else data['Close'],
                adx=data.get('adx'), 
                volatility=data.get('atr'),
                adx_threshold=config.adx_threshold,
                volatility_threshold=config.volatility_threshold
            )
            
            trending_pct = (regime_data['is_trending'].sum() / len(regime_data)) * 100
            ranging_pct = 100 - trending_pct
            
            # Create result object
            result = {
                'symbol': symbol,
                'timeframe': timeframe,
                'train_days': train_days,
                'test_days': test_days,
                'data_points': len(data),
                'splits': len(results),
                'avg_train_return': avg_train_return,
                'avg_test_return': avg_test_return,
                'avg_train_sharpe': avg_train_sharpe,
                'avg_test_sharpe': avg_test_sharpe,
                'avg_robustness': avg_robustness,
                'regime_trending_pct': trending_pct,
                'regime_ranging_pct': ranging_pct,
                'success': True,
                'error': None
            }
            
            logger.info(f"Optimization case completed: {symbol} ({timeframe}), "
                       f"avg_test_return={avg_test_return:.2f}%, "
                       f"avg_test_sharpe={avg_test_sharpe:.2f}, "
                       f"avg_robustness={avg_robustness:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in optimization case: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'train_days': train_days,
                'test_days': test_days,
                'success': False,
                'error': str(e)
            }
            
        finally:
            # Restore original values in both modules
            wfo_utils.WFO_TRAIN_POINTS = original_values['wfo_utils']['WFO_TRAIN_POINTS']
            wfo_utils.WFO_TEST_POINTS = original_values['wfo_utils']['WFO_TEST_POINTS']
            wfo_utils.STEP_POINTS = original_values['wfo_utils']['STEP_POINTS']
            wfo.WFO_TRAIN_POINTS = original_values['wfo']['WFO_TRAIN_POINTS']
            wfo.WFO_TEST_POINTS = original_values['wfo']['WFO_TEST_POINTS']
            wfo.STEP_POINTS = original_values['wfo']['STEP_POINTS']
    
    def run_optimization_matrix(self):
        """
        Run optimization for all combinations of parameters.
        """
        logger.info("Starting optimization matrix run...")
        
        # Generate all combinations
        total_cases = len(self.symbols) * len(self.timeframes) * len(self.train_days) * len(self.test_days)
        logger.info(f"Total optimization cases: {total_cases}")
        
        # Counter for progress tracking
        completed = 0
        
        # Run each case
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                for train_days in self.train_days:
                    for test_days in self.test_days:
                        # Run this optimization case
                        result = self.run_optimization_case(
                            symbol=symbol,
                            timeframe=timeframe,
                            train_days=train_days,
                            test_days=test_days
                        )
                        
                        # Add to results
                        self.results.append(result)
                        
                        # Update progress
                        completed += 1
                        logger.info(f"Progress: {completed}/{total_cases} cases completed ({completed/total_cases*100:.1f}%)")
        
        # Process and save results
        self.save_results()
        self.create_visualizations()
        
        logger.info(f"Optimization matrix completed. Results saved to {OPTIMIZATION_RESULTS_FILE}")
    
    def save_results(self):
        """
        Process and save optimization results.
        """
        if not self.results:
            logger.warning("No results to save.")
            return
        
        # Convert to DataFrame
        results_df = pd.DataFrame(self.results)
        
        # Save to CSV
        results_df.to_csv(OPTIMIZATION_RESULTS_FILE, index=False)
        logger.info(f"Results saved to {OPTIMIZATION_RESULTS_FILE}")
        
        # Create summary statistics
        successful_results = results_df[results_df['success'] == True]
        
        if not successful_results.empty:
            # Group by symbol and timeframe
            summary = successful_results.groupby(['symbol', 'timeframe']).agg({
                'avg_train_return': 'mean',
                'avg_test_return': 'mean',
                'avg_train_sharpe': 'mean',
                'avg_test_sharpe': 'mean',
                'avg_robustness': 'mean',
                'regime_trending_pct': 'mean',
                'regime_ranging_pct': 'mean',
                'success': 'sum'
            }).reset_index()
            
            # Add number of cases column
            summary['cases'] = successful_results.groupby(['symbol', 'timeframe']).size().values
            
            # Save summary to CSV
            summary.to_csv(OPTIMIZATION_SUMMARY_FILE, index=False)
            logger.info(f"Summary statistics saved to {OPTIMIZATION_SUMMARY_FILE}")
    
    def create_visualizations(self):
        """
        Create visualizations from optimization results.
        """
        if not self.results:
            logger.warning("No results to visualize.")
            return
        
        # Convert to DataFrame
        results_df = pd.DataFrame(self.results)
        
        # Filter successful results
        successful_results = results_df[results_df['success'] == True]
        
        if successful_results.empty:
            logger.warning("No successful results to visualize.")
            return
        
        # 1. Performance by Symbol and Timeframe
        plt.figure(figsize=(14, 10))
        
        # Plot test returns
        plt.subplot(2, 1, 1)
        sns.barplot(data=successful_results, x='symbol', y='avg_test_return', hue='timeframe')
        plt.title('Average Test Return by Symbol and Timeframe')
        plt.ylabel('Average Test Return (%)')
        plt.xlabel('Symbol')
        plt.grid(alpha=0.3)
        
        # Plot test Sharpe ratios
        plt.subplot(2, 1, 2)
        sns.barplot(data=successful_results, x='symbol', y='avg_test_sharpe', hue='timeframe')
        plt.title('Average Test Sharpe Ratio by Symbol and Timeframe')
        plt.ylabel('Average Test Sharpe Ratio')
        plt.xlabel('Symbol')
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(OPTIMIZATION_PLOTS_DIR, 'performance_by_symbol_timeframe.png'))
        
        # 2. Performance by Training Window Size
        plt.figure(figsize=(14, 10))
        
        # Plot test returns
        plt.subplot(2, 1, 1)
        sns.barplot(data=successful_results, x='train_days', y='avg_test_return', hue='timeframe')
        plt.title('Average Test Return by Training Window Size')
        plt.ylabel('Average Test Return (%)')
        plt.xlabel('Training Window (days)')
        plt.grid(alpha=0.3)
        
        # Plot test Sharpe ratios
        plt.subplot(2, 1, 2)
        sns.barplot(data=successful_results, x='train_days', y='avg_test_sharpe', hue='timeframe')
        plt.title('Average Test Sharpe Ratio by Training Window Size')
        plt.ylabel('Average Test Sharpe Ratio')
        plt.xlabel('Training Window (days)')
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(OPTIMIZATION_PLOTS_DIR, 'performance_by_train_window.png'))
        
        # 3. Robustness Analysis
        plt.figure(figsize=(14, 10))
        
        # Plot robustness ratio
        plt.subplot(2, 1, 1)
        sns.barplot(data=successful_results, x='symbol', y='avg_robustness', hue='timeframe')
        plt.title('Average Robustness Ratio by Symbol and Timeframe')
        plt.ylabel('Average Robustness Ratio')
        plt.xlabel('Symbol')
        plt.axhline(y=1.0, color='green', linestyle='--', alpha=0.5)
        plt.axhline(y=0.7, color='orange', linestyle='--', alpha=0.5)
        plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
        plt.grid(alpha=0.3)
        
        # Plot train vs test return scatter
        plt.subplot(2, 1, 2)
        for symbol in successful_results['symbol'].unique():
            symbol_data = successful_results[successful_results['symbol'] == symbol]
            plt.scatter(symbol_data['avg_train_return'], symbol_data['avg_test_return'], 
                       label=symbol, alpha=0.7)
        
        # Add diagonal reference line
        min_val = min(successful_results['avg_train_return'].min(), successful_results['avg_test_return'].min())
        max_val = max(successful_results['avg_train_return'].max(), successful_results['avg_test_return'].max())
        plt.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5)
        
        plt.title('Train vs Test Returns')
        plt.xlabel('Average Train Return (%)')
        plt.ylabel('Average Test Return (%)')
        plt.legend()
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(OPTIMIZATION_PLOTS_DIR, 'robustness_analysis.png'))
        
        # 4. Regime Analysis
        plt.figure(figsize=(14, 10))
        
        # Create regime distribution stacked bar chart
        plt.subplot(2, 1, 1)
        successful_results_copy = successful_results.copy()
        
        # Set up the bar chart data
        regime_data = []
        for _, row in successful_results_copy.iterrows():
            regime_data.append({
                'symbol_timeframe': f"{row['symbol']} ({row['timeframe']})",
                'regime': 'Trending',
                'percentage': row['regime_trending_pct']
            })
            regime_data.append({
                'symbol_timeframe': f"{row['symbol']} ({row['timeframe']})",
                'regime': 'Ranging',
                'percentage': row['regime_ranging_pct']
            })
        
        regime_df = pd.DataFrame(regime_data)
        
        # Create the stacked bar chart
        regime_pivot = regime_df.pivot(index='symbol_timeframe', columns='regime', values='percentage')
        regime_pivot.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='viridis')
        
        plt.title('Regime Distribution by Symbol and Timeframe')
        plt.xlabel('Symbol and Timeframe')
        plt.ylabel('Percentage')
        plt.legend(title='Regime')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        
        # Plot performance by regime percentage
        plt.subplot(2, 1, 2)
        plt.scatter(successful_results['regime_trending_pct'], successful_results['avg_test_return'], 
                   alpha=0.7, s=60)
        
        # Add trendline
        z = np.polyfit(successful_results['regime_trending_pct'], successful_results['avg_test_return'], 1)
        p = np.poly1d(z)
        plt.plot(successful_results['regime_trending_pct'], p(successful_results['regime_trending_pct']), 
                 "r--", alpha=0.7)
        
        plt.title('Test Return vs. Trending Percentage')
        plt.xlabel('Trending Percentage (%)')
        plt.ylabel('Average Test Return (%)')
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(OPTIMIZATION_PLOTS_DIR, 'regime_analysis.png'))
        
        logger.info(f"Optimization visualizations saved to {OPTIMIZATION_PLOTS_DIR}")


def main():
    """
    Main function to run the optimization framework.
    """
    logger.info("Starting Edge Multi-Factor Strategy Optimization Framework")
    
    # Create optimizer with default settings
    optimizer = StrategyOptimizer(
        symbols=['BTC-USD', 'ETH-USD'],
        timeframes=['1h', '4h'],
        start_date=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
        end_date=datetime.now().strftime('%Y-%m-%d'),
        train_days=[30, 60],
        test_days=[15, 30],
        n_jobs=-1
    )
    
    # Run optimization
    optimizer.run_optimization_matrix()
    
    logger.info("Optimization framework execution completed.")


if __name__ == "__main__":
    main()
