#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Optuna optimization for the Edge Multi-Factor strategy.

This script performs systematic parameter optimization across multiple symbols,
timeframes, and window sizes using Optuna's Bayesian optimization approach.
"""

import os
import sys
import time
import json
import logging
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union, Set
import concurrent.futures
from dataclasses import dataclass, field

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pydantic import BaseModel, Field, field_validator
from tqdm import tqdm

# Set up Python path to match integration test pattern
current_file = Path(__file__).resolve()
current_dir = current_file.parent
project_root = current_dir.parents[3]
scripts_dir = current_dir.parents[2]

# Add paths to allow imports
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# Import required modules
from scripts.strategies.refactored_edge import config
from scripts.strategies.refactored_edge.data.data_fetcher import GRANULARITY_MAP_SECONDS
from scripts.strategies.refactored_edge.wfo_utils import set_testing_mode, is_testing_mode
from scripts.strategies.refactored_edge.asset_profiles import (
    analyze_asset_volatility, recommend_signal_parameters,
    get_asset_specific_config, load_asset_profile, save_asset_profile,
    generate_and_save_default_profiles
)
from scripts.strategies.refactored_edge.data.fetch_data import fetch_data

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger('batch_optimizer')

# Define constants
BATCH_DIR = os.path.join(project_root, 'data', 'batch_optimization')
PLOTS_DIR = os.path.join(BATCH_DIR, 'plots')
RESULTS_DIR = os.path.join(BATCH_DIR, 'results')


class BatchOptimizerConfig(BaseModel):
    """Configuration for batch optimization using Pydantic for validation."""
    
    symbols: List[str] = Field(
        default=["BTC-USD", "ETH-USD", "SOL-USD"],
        description="List of trading symbols to optimize for"
    )
    
    timeframes: List[str] = Field(
        default=["1h", "4h", "1d"],
        description="List of timeframes to optimize for"
    )
    
    training_windows: List[int] = Field(
        default=[30, 60],
        description="List of training window sizes in days"
    )
    
    testing_windows: List[Dict[int, int]] = Field(
        default=[{30: 15}, {60: 30}],
        description="Dictionary mapping training window to testing window size"
    )
    
    n_trials: int = Field(
        default=50,
        description="Number of Optuna trials per optimization case",
        ge=10
    )
    
    timeout: int = Field(
        default=1800,
        description="Timeout in seconds per optimization case",
        ge=60
    )
    
    n_splits: int = Field(
        default=3,
        description="Number of WFO splits per optimization",
        ge=2
    )
    
    parallel: bool = Field(
        default=False,
        description="Whether to run optimizations in parallel"
    )
    
    max_workers: int = Field(
        default=2,
        description="Maximum number of parallel workers if parallel=True",
        ge=1
    )
    
    use_asset_profiles: bool = Field(
        default=True,
        description="Whether to use asset-specific volatility profiles for configuration"
    )
    
    analyze_new_profiles: bool = Field(
        default=True,
        description="Whether to analyze and create new asset profiles if they don't exist"
    )
    
    @field_validator('timeframes')
    def timeframes_must_be_supported(cls, v):
        """Validate that timeframes are supported by the data fetcher."""
        for tf in v:
            if tf not in GRANULARITY_MAP_SECONDS:
                raise ValueError(f"Timeframe {tf} is not supported. "
                               f"Supported timeframes: {list(GRANULARITY_MAP_SECONDS.keys())}")
        return v
    
    @field_validator('testing_windows')
    def validate_testing_windows(cls, v, info):
        """Ensure testing windows match training windows."""
        values = info.data
        if 'training_windows' in values:
            train_windows = values['training_windows']
            # Convert list of dicts to a single dict
            test_windows_dict = {}
            for d in v:
                test_windows_dict.update(d)
            
            # Check that all training windows have a testing window
            for train in train_windows:
                if train not in test_windows_dict:
                    raise ValueError(f"Training window {train} has no matching testing window")
            
            # Reconstruct as original format
            return [test_windows_dict]
        return v


class BatchOptimizer:
    """
    Batch optimizer for running multiple Optuna optimizations systematically.
    
    This class orchestrates optimization runs across different symbols, timeframes,
    and window sizes, aggregating and analyzing the results.
    
    Attributes:
        config: BatchOptimizerConfig object with optimization parameters
        results: Dictionary to store optimization results
    """
    
    def __init__(self, config: BatchOptimizerConfig):
        """
        Initialize the batch optimizer.
        
        Args:
            config: BatchOptimizerConfig with optimization parameters
        """
        self.config = config
        self.results = {}
        self.completed_runs = set()
        self.failed_runs = set()
        
        # Consolidate testing windows
        self.testing_windows = {}
        for d in config.testing_windows:
            self.testing_windows.update(d)
        
        # Create output directories
        self._ensure_directories()
        
        logger.info(f"Initialized Batch Optimizer with {len(config.symbols)} symbols, "
                   f"{len(config.timeframes)} timeframes, and "
                   f"{len(config.training_windows)} training windows")
    
    def _ensure_directories(self) -> None:
        """Create necessary directories for batch optimization results."""
        os.makedirs(BATCH_DIR, exist_ok=True)
        os.makedirs(PLOTS_DIR, exist_ok=True)
        os.makedirs(RESULTS_DIR, exist_ok=True)
        logger.info(f"Created output directories at {BATCH_DIR}")
    
    def _get_case_key(self, symbol: str, timeframe: str, 
                     train_days: int, test_days: int) -> str:
        """
        Generate a unique key for an optimization case.
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe
            train_days: Training window in days
            test_days: Testing window in days
            
        Returns:
            String key uniquely identifying the optimization case
        """
        return f"{symbol}_{timeframe}_train{train_days}_test{test_days}"
    
    def run_single_optimization(self, symbol: str, timeframe: str, 
                           train_days: int, test_days: int) -> Dict[str, Any]:
        """
        Run a single optimization case.
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe
            train_days: Training window in days
            test_days: Testing window in days
            
        Returns:
            Dictionary with optimization results
        """
        case_key = self._get_case_key(symbol, timeframe, train_days, test_days)
        
        # Save current testing mode state before doing anything else
        previous_testing_mode = is_testing_mode()
        
        try:
            logger.info(f"Starting optimization case: {case_key}")
            
            # Import only what's needed here to avoid circular imports
            from scripts.strategies.refactored_edge.run_optuna_optimization import (
                run_optuna_optimization,
                ensure_directories,
                save_results,
                save_study_visualizations
            )
            
            # Check if we already have a result for this case
            if case_key in self.completed_runs:
                logger.info(f"Optimization case {case_key} already completed, skipping")
                return self.results[symbol][timeframe][case_key]
            
            # Always set testing mode to True for optimization
            set_testing_mode(True)
            logger.info(f"Set testing mode to True for optimization")
            
            # Fetch data for optimization
            data = fetch_data(
                symbol=symbol,
                timeframe=timeframe,
                days=train_days + test_days
            )
            
            if data is None or len(data) < 100:  # Minimum data threshold
                logger.error(f"Insufficient data for {symbol} {timeframe}")
                # Create a basic result with error status
                error_result = {
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'train_days': train_days,
                    'test_days': test_days,
                    'case_key': case_key,
                    'status': 'error',
                    'error': 'Insufficient data',
                    'asset_specific_params': {}
                }
                # Add to failed runs set
                self.failed_runs.add(case_key)
                # Restore testing mode
                set_testing_mode(previous_testing_mode)
                return error_result
                
            # Apply asset-specific configuration if enabled
            asset_specific_params = {}
            if self.config.use_asset_profiles:
                # Check if we already have a profile for this asset
                asset_profile = load_asset_profile(symbol)
                
                # If no profile exists and analysis is enabled, create one
                if asset_profile is None and self.config.analyze_new_profiles:
                    try:
                        logger.info(f"Creating new asset profile for {symbol}")
                        volatility_metrics = analyze_asset_volatility(data)
                        recommended_params = recommend_signal_parameters(
                            volatility_metrics["volatility_profile"],
                            volatility_metrics["avg_daily_volatility"]
                        )
                        
                        # Create asset profile model
                        from scripts.strategies.refactored_edge.asset_profiles import AssetConfig
                        asset_profile = AssetConfig(
                            symbol=symbol,
                            volatility_profile=volatility_metrics["volatility_profile"],
                            avg_daily_volatility=volatility_metrics["avg_daily_volatility"],
                            **recommended_params
                        )
                        save_asset_profile(asset_profile)
                        
                        logger.info(f"Created asset profile for {symbol}: "  
                                   f"Volatility={asset_profile.volatility_profile}, "
                                   f"Strictness={asset_profile.signal_strictness}")
                    except Exception as e:
                        logger.error(f"Error creating asset profile for {symbol}: {e}")
                        # Continue with default parameters if profile creation fails
                
                # If we have a profile, use its parameters to guide optimization
                if asset_profile:
                    asset_specific_params = {
                        "signal_strictness": asset_profile.signal_strictness,
                        "trend_threshold_pct": asset_profile.trend_threshold_pct,
                        "zone_influence": asset_profile.zone_influence,
                        "min_hold_period": asset_profile.min_hold_period
                    }
                    logger.info(f"Using asset-specific parameters for {symbol}: {asset_specific_params}")
            
            # Run optimization with asset-specific parameters if available
            try:
                result = run_optuna_optimization(
                    data=data,
                    symbol=symbol,
                    timeframe=timeframe,
                    n_trials=self.config.n_trials,
                    timeout=self.config.timeout,
                    n_splits=self.config.n_splits,
                    train_days=train_days,
                    test_days=test_days,
                    **asset_specific_params
                )
                
                # Add case information
                result['symbol'] = symbol
                result['timeframe'] = timeframe
                result['train_days'] = train_days
                result['test_days'] = test_days
                result['case_key'] = case_key
                result['status'] = 'success'
                result['asset_specific_params'] = asset_specific_params if self.config.use_asset_profiles else {}
                
                # Add to completed runs set
                self.completed_runs.add(case_key)
                
                return result
            except Exception as e:
                logger.error(f"Error in optimization run for {case_key}: {e}")
                error_result = {
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'train_days': train_days,
                    'test_days': test_days,
                    'case_key': case_key,
                    'status': 'error',
                    'error': str(e),
                    'asset_specific_params': asset_specific_params
                }
                # Add to failed runs set
                self.failed_runs.add(case_key)
                return error_result
            
        except Exception as e:
            logger.error(f"Error in optimization case {case_key}: {e}")
            # Create a basic result with error status
            error_result = {
                'symbol': symbol,
                'timeframe': timeframe,
                'train_days': train_days,
                'test_days': test_days,
                'case_key': case_key,
                'status': 'error',
                'error': str(e),
                'asset_specific_params': {}
            }
            # Add to failed runs set
            self.failed_runs.add(case_key)
            return error_result
        finally:
            # Always restore previous testing mode state
            set_testing_mode(previous_testing_mode)
            logger.info(f"Restored testing mode to previous state: {previous_testing_mode}")
    
    def run_batch_sequential(self) -> Dict[str, Dict[str, Any]]:
        """
        Run all optimization cases sequentially.
        
        Returns:
            Dictionary of results indexed by case keys
        """
        results = {}
        total_cases = len(self.config.symbols) * len(self.config.timeframes) * len(self.config.training_windows)
        
        logger.info(f"Starting sequential batch optimization with {total_cases} cases")
        
        with tqdm(total=total_cases, desc="Optimizations") as pbar:
            for symbol in self.config.symbols:
                results[symbol] = {}
                
                for timeframe in self.config.timeframes:
                    results[symbol][timeframe] = {}
                    
                    for train_days in self.config.training_windows:
                        test_days = self.testing_windows.get(train_days)
                        
                        # Run the optimization
                        case_result = self.run_single_optimization(
                            symbol=symbol,
                            timeframe=timeframe,
                            train_days=train_days,
                            test_days=test_days
                        )
                        
                        # Store the result
                        case_key = self._get_case_key(symbol, timeframe, train_days, test_days)
                        results[symbol][timeframe][case_key] = case_result
                        
                        # Update progress
                        pbar.update(1)
        
        self.results = results
        return results
    
    def run_batch_parallel(self) -> Dict[str, Dict[str, Any]]:
        """
        Run all optimization cases in parallel.
        
        Returns:
            Dictionary of results indexed by case keys
        """
        cases = []
        for symbol in self.config.symbols:
            for timeframe in self.config.timeframes:
                for train_days in self.config.training_windows:
                    test_days = self.testing_windows.get(train_days)
                    cases.append((symbol, timeframe, train_days, test_days))
        
        total_cases = len(cases)
        logger.info(f"Starting parallel batch optimization with {total_cases} cases "
                   f"using {self.config.max_workers} workers")
        
        results = {}
        for symbol in self.config.symbols:
            results[symbol] = {}
            for timeframe in self.config.timeframes:
                results[symbol][timeframe] = {}
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = {executor.submit(self.run_single_optimization, symbol, timeframe, train_days, test_days): 
                      (symbol, timeframe, train_days, test_days) for symbol, timeframe, train_days, test_days in cases}
            
            with tqdm(total=total_cases, desc="Optimizations") as pbar:
                for future in concurrent.futures.as_completed(futures):
                    symbol, timeframe, train_days, test_days = futures[future]
                    try:
                        case_result = future.result()
                        case_key = self._get_case_key(symbol, timeframe, train_days, test_days)
                        results[symbol][timeframe][case_key] = case_result
                    except Exception as e:
                        logger.error(f"Error processing result: {e}")
                    pbar.update(1)
        
        self.results = results
        return results
    
    def run_batch(self) -> Dict[str, Dict[str, Any]]:
        """
        Run all optimization cases using either sequential or parallel execution.
        
        Returns:
            Dictionary of results indexed by case keys
        """
        if self.config.parallel:
            return self.run_batch_parallel()
        else:
            return self.run_batch_sequential()
    
    def save_results(self) -> None:
        """Save batch optimization results to files."""
        if not self.results:
            logger.warning("No results to save")
            return
        
        # Create timestamp for this batch
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Save the full results dictionary
            results_file = os.path.join(RESULTS_DIR, f'batch_results_{timestamp}.json')
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            logger.info(f"Full results saved to {results_file}")
            
            # Create a summary DataFrame
            summary_rows = []
            
            for symbol in self.results:
                for timeframe in self.results[symbol]:
                    for case_key, case_result in self.results[symbol][timeframe].items():
                        if case_result.get("status") == "success":
                            row = {
                                "symbol": symbol,
                                "timeframe": timeframe,
                                "case_key": case_key,
                                "train_days": case_result.get("train_days"),
                                "test_days": case_result.get("test_days"),
                                "best_value": case_result.get("best_value"),
                                "n_trials": case_result.get("n_trials"),
                                "completed_trials": case_result.get("completed_trials"),
                                "elapsed_time": case_result.get("elapsed_time"),
                            }
                            
                            # Add best parameters
                            best_params = case_result.get("best_params", {})
                            for param, value in best_params.items():
                                row[f"param_{param}"] = value
                            
                            summary_rows.append(row)
            
            if summary_rows:
                summary_df = pd.DataFrame(summary_rows)
                summary_file = os.path.join(RESULTS_DIR, f'batch_summary_{timestamp}.csv')
                summary_df.to_csv(summary_file, index=False)
                logger.info(f"Summary saved to {summary_file}")
                
                # Also save a parameter-focused CSV
                param_cols = [col for col in summary_df.columns if col.startswith('param_')]
                if param_cols:
                    param_df = summary_df[['symbol', 'timeframe', 'case_key', 'best_value'] + param_cols]
                    param_file = os.path.join(RESULTS_DIR, f'batch_params_{timestamp}.csv')
                    param_df.to_csv(param_file, index=False)
                    logger.info(f"Parameter summary saved to {param_file}")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def create_visualizations(self) -> None:
        """Generate visualizations for batch optimization results."""
        if not self.results:
            logger.warning("No results to visualize")
            return
        
        # Create a timestamp for this batch
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_plots_dir = os.path.join(PLOTS_DIR, f'batch_{timestamp}')
        os.makedirs(batch_plots_dir, exist_ok=True)
        
        try:
            # Extract data for visualization
            rows = []
            
            for symbol in self.results:
                for timeframe in self.results[symbol]:
                    for case_key, case_result in self.results[symbol][timeframe].items():
                        if case_result.get("status") == "success":
                            train_days = case_result.get("train_days")
                            test_days = case_result.get("test_days")
                            best_value = case_result.get("best_value")
                            
                            if best_value not in (float('-inf'), float('inf'), None):
                                row = {
                                    "symbol": symbol,
                                    "timeframe": timeframe,
                                    "train_days": train_days,
                                    "test_days": test_days,
                                    "best_value": best_value,
                                    "window_ratio": train_days / test_days if test_days else 0,
                                }
                                
                                # Add selected best parameters
                                best_params = case_result.get("best_params", {})
                                important_params = [
                                    'rsi_window', 'bb_window', 'ma_window', 
                                    'rsi_entry_threshold', 'use_regime_filter'
                                ]
                                
                                for param in important_params:
                                    if param in best_params:
                                        row[param] = best_params[param]
                                
                                rows.append(row)
            
            if not rows:
                logger.warning("No valid results for visualization")
                return
                
            df = pd.DataFrame(rows)
            
            # Visualizations to create:
            
            # 1. Performance by Symbol and Timeframe
            plt.figure(figsize=(12, 8))
            pivot_df = df.pivot_table(
                values='best_value', 
                index='symbol', 
                columns='timeframe', 
                aggfunc='mean'
            )
            sns.heatmap(pivot_df, annot=True, cmap='viridis', fmt=".4f")
            plt.title('Average Performance by Symbol and Timeframe')
            plt.tight_layout()
            plt.savefig(os.path.join(batch_plots_dir, 'performance_by_symbol_timeframe.png'))
            plt.close()
            
            # 2. Performance by Training Window Size
            plt.figure(figsize=(10, 6))
            sns.boxplot(x='train_days', y='best_value', data=df)
            plt.title('Performance by Training Window Size')
            plt.xlabel('Training Days')
            plt.ylabel('Performance Metric (Sharpe Ratio)')
            plt.tight_layout()
            plt.savefig(os.path.join(batch_plots_dir, 'performance_by_training_window.png'))
            plt.close()
            
            # 3. Parameter Distribution by Performance
            for param in [col for col in df.columns if col in important_params]:
                if param in df.columns and len(df[param].unique()) > 1:
                    plt.figure(figsize=(10, 6))
                    
                    if df[param].dtype == bool:
                        # For boolean parameters
                        sns.boxplot(x=param, y='best_value', data=df)
                    else:
                        # For numeric parameters
                        sns.scatterplot(x=param, y='best_value', hue='symbol', data=df)
                        plt.axhline(y=df['best_value'].mean(), color='r', linestyle='--', 
                                   label=f'Avg: {df["best_value"].mean():.4f}')
                        plt.legend()
                    
                    plt.title(f'Performance by {param}')
                    plt.xlabel(param)
                    plt.ylabel('Performance Metric (Sharpe Ratio)')
                    plt.tight_layout()
                    plt.savefig(os.path.join(batch_plots_dir, f'performance_by_{param}.png'))
                    plt.close()
            
            # 4. Symbol Performance Comparison
            plt.figure(figsize=(12, 6))
            sns.boxplot(x='symbol', y='best_value', hue='timeframe', data=df)
            plt.title('Symbol Performance Comparison by Timeframe')
            plt.xlabel('Symbol')
            plt.ylabel('Performance Metric (Sharpe Ratio)')
            plt.tight_layout()
            plt.savefig(os.path.join(batch_plots_dir, 'symbol_performance_comparison.png'))
            plt.close()
            
            logger.info(f"Visualizations saved to {batch_plots_dir}")
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
    
    def generate_optimization_report(self) -> str:
        """
        Generate a markdown report for batch optimization results.
        
        Returns:
            String containing markdown report
        """
        if not self.results:
            return "# Batch Optimization Report\n\nNo results available."
        
        # Extract data for report
        total_cases = len(self.config.symbols) * len(self.config.timeframes) * len(self.config.training_windows)
        completed_cases = len(self.completed_runs)
        failed_cases = len(self.failed_runs)
        
        # Build markdown report
        report = [
            "# Batch Optimization Report",
            f"\nReport Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n## Summary",
            f"- Total Cases: {total_cases}",
            f"- Completed: {completed_cases}",
            f"- Failed: {failed_cases}",
            f"- Success Rate: {completed_cases/total_cases*100:.1f}%",
            f"\n## Configuration",
            f"- Symbols: {', '.join(self.config.symbols)}",
            f"- Timeframes: {', '.join(self.config.timeframes)}",
            f"- Training Windows: {', '.join(map(str, self.config.training_windows))} days",
            f"- Trials per Case: {self.config.n_trials}",
            f"- Timeout per Case: {self.config.timeout} seconds",
            f"\n## Top Performing Configurations",
        ]
        
        # Find top configurations
        top_configs = []
        
        for symbol in self.results:
            for timeframe in self.results[symbol]:
                for case_key, case_result in self.results[symbol][timeframe].items():
                    if case_result.get("status") == "success":
                        best_value = case_result.get("best_value")
                        
                        if best_value not in (float('-inf'), float('inf'), None):
                            top_configs.append((case_key, best_value, case_result))
        
        # Sort by best value
        top_configs.sort(key=lambda x: x[1], reverse=True)
        
        # Add top 5 or fewer if less than 5 available
        for i, (case_key, best_value, case_result) in enumerate(top_configs[:5]):
            report.append(f"\n### {i+1}. {case_key} (Score: {best_value:.4f})")
            report.append(f"- Symbol: {case_result.get('symbol')}")
            report.append(f"- Timeframe: {case_result.get('timeframe')}")
            report.append(f"- Training Days: {case_result.get('train_days')}")
            report.append(f"- Testing Days: {case_result.get('test_days')}")
            
            report.append("\nKey Parameters:")
            best_params = case_result.get("best_params", {})
            for param, value in sorted(best_params.items()):
                report.append(f"- {param}: {value}")
        
        # Add a section for recommendations
        report.append("\n## Recommendations")
        
        if top_configs:
            # Add general recommendations based on optimization results
            best_case = top_configs[0][2]
            report.append(f"\nBased on the optimization results, we recommend:")
            report.append(f"1. Using the {best_case.get('symbol')} symbol with {best_case.get('timeframe')} timeframe")
            report.append(f"2. Training window of {best_case.get('train_days')} days with testing window of {best_case.get('test_days')} days")
            
            # Analyze parameter trends
            report.append(f"\nKey parameter trends observed:")
            
            # Add specific parameter notes if we can analyze them
            try:
                # Create DataFrame from top configs
                param_rows = []
                for _, _, case_result in top_configs:
                    if "best_params" in case_result:
                        row = {"case_key": case_result.get("case_key")}
                        for param, value in case_result.get("best_params", {}).items():
                            row[param] = value
                        param_rows.append(row)
                
                if param_rows:
                    param_df = pd.DataFrame(param_rows)
                    
                    # Check for boolean parameters first
                    bool_params = [col for col in param_df.columns if param_df[col].dtype == bool]
                    for param in bool_params:
                        true_count = param_df[param].sum()
                        total = len(param_df)
                        if true_count > total / 2:
                            report.append(f"- {param}: Enable this feature ({true_count}/{total} top configurations use it)")
                        else:
                            report.append(f"- {param}: Consider disabling this feature (only {true_count}/{total} top configurations use it)")
                    
                    # Check for numeric parameters
                    num_params = [col for col in param_df.columns if col not in bool_params and col != 'case_key' and pd.api.types.is_numeric_dtype(param_df[col])]
                    for param in num_params:
                        mean_val = param_df[param].mean()
                        report.append(f"- {param}: Average value across top configurations is {mean_val:.2f}")
            
            except Exception as e:
                logger.warning(f"Error analyzing parameter trends: {e}")
                report.append("- Unable to perform detailed parameter trend analysis")
        else:
            report.append("\nNo successful optimizations were completed. Please review configuration and try again.")
        
        # Join all report lines
        return "\n".join(report)
    
    def save_report(self) -> None:
        """Generate and save the batch optimization report."""
        report = self.generate_optimization_report()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(RESULTS_DIR, f'batch_report_{timestamp}.md')
        
        try:
            with open(report_file, 'w') as f:
                f.write(report)
            
            logger.info(f"Report saved to {report_file}")
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Batch Optuna Optimization for Edge Strategy')
    
    parser.add_argument('--symbols', nargs='+', default=["BTC-USD", "ETH-USD", "SOL-USD"],
                       help='List of symbols to optimize for')
    
    parser.add_argument('--timeframes', nargs='+', default=["1h", "4h", "1d"],
                       help='List of timeframes to optimize for')
    
    parser.add_argument('--train-days', nargs='+', type=int, default=[30, 60],
                       help='List of training window sizes in days')
    
    parser.add_argument('--n-trials', type=int, default=50,
                       help='Number of Optuna trials per optimization case')
    
    parser.add_argument('--timeout', type=int, default=1800,
                       help='Timeout in seconds per optimization case')
    
    parser.add_argument('--parallel', action='store_true',
                       help='Run optimizations in parallel')
    
    parser.add_argument('--max-workers', type=int, default=2,
                       help='Maximum number of parallel workers if using parallel mode')
    
    parser.add_argument('--use-asset-profiles', action='store_true', 
                       help='Use asset-specific volatility profiles for optimization')
    
    parser.add_argument('--no-asset-profiles', action='store_true',
                       help='Disable asset-specific volatility profiles')
    
    parser.add_argument('--analyze-new-profiles', action='store_true',
                       help='Analyze and create new asset profiles if they do not exist')
    
    return parser.parse_args()


def main():
    """Main function to run batch optimization."""
    # Parse arguments
    args = parse_args()
    
    # Create testing windows mapping based on training windows
    # Use 1:2 ratio (e.g., 30-day training → 15-day testing)
    test_windows = [{train: train // 2} for train in args.train_days]
    
    # Determine asset profile settings
    use_asset_profiles = True
    if args.no_asset_profiles:
        use_asset_profiles = False
    elif args.use_asset_profiles:
        use_asset_profiles = True
    
    # Create configuration
    config = BatchOptimizerConfig(
        symbols=args.symbols,
        timeframes=args.timeframes,
        training_windows=args.train_days,
        testing_windows=test_windows,
        n_trials=args.n_trials,
        timeout=args.timeout,
        parallel=args.parallel,
        max_workers=args.max_workers,
        use_asset_profiles=use_asset_profiles,
        analyze_new_profiles=args.analyze_new_profiles
    )
    
    # Create and run batch optimizer
    optimizer = BatchOptimizer(config)
    
    start_time = time.time()
    optimizer.run_batch()
    elapsed_time = time.time() - start_time
    
    # Save results
    optimizer.save_results()
    optimizer.create_visualizations()
    optimizer.save_report()
    
    # Print summary
    total_cases = len(config.symbols) * len(config.timeframes) * len(config.training_windows)
    completed_cases = len(optimizer.completed_runs)
    failed_cases = len(optimizer.failed_runs)
    
    print("\n" + "=" * 80)
    print(f"Batch Optimization completed in {elapsed_time:.2f} seconds")
    print(f"Total Cases: {total_cases}")
    print(f"Completed: {completed_cases}")
    print(f"Failed: {failed_cases}")
    print(f"Success Rate: {completed_cases/total_cases*100:.1f}%")
    print("=" * 80 + "\n")
    
    print("Results, visualizations, and report saved to:")
    print(f"  {RESULTS_DIR}")
    print(f"  {PLOTS_DIR}")


if __name__ == "__main__":
    main()
