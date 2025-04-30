#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extended Multi-Asset Batch Optimization

This script runs a comprehensive production-quality optimization across multiple assets
with a larger number of trials to find robust asset-specific parameter sets. It builds
on the successfully verified fixes for tuple indexing and Pydantic validators.

Features:
- Runs 50+ trials per asset for thorough parameter space exploration
- Tests multiple timeframes for each asset
- Uses longer training/testing windows for more reliable optimization
- Saves detailed asset profiles for each asset/timeframe combination
- Generates comprehensive comparison reports
"""

import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Set up Python path
current_file = Path(__file__).resolve()
current_dir = current_file.parent
project_root = current_dir.parents[3]
scripts_dir = current_dir.parents[2]
data_dir = project_root / "data"
results_dir = data_dir / "results"

# Create results directory if it doesn't exist
results_dir.mkdir(parents=True, exist_ok=True)

# Add paths to allow imports
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# Import modules
from scripts.strategies.refactored_edge.batch_optuna_optimizer import (
    BatchOptimizerConfig, BatchOptimizer
)
from scripts.strategies.refactored_edge.asset_profiles import (
    load_asset_profile, save_asset_profile, get_asset_specific_config
)

def run_extended_multi_asset_optimization(
    symbols: Optional[List[str]] = None,
    timeframes: Optional[List[str]] = None,
    n_trials: int = 50,
    save_interval: int = 10,
    parallel: bool = True,
    n_jobs: int = -1,
    create_visualizations: bool = True
) -> Dict[str, Any]:
    """
    Run extended batch optimization with multiple assets for production use.
    
    Args:
        symbols: List of assets to optimize. Defaults to a predefined list if None.
        timeframes: List of timeframes to test. Defaults to a predefined list if None.
        n_trials: Number of optimization trials per asset/timeframe combination.
        save_interval: Save intermediate results after this many trials.
        parallel: Whether to run optimizations in parallel.
        n_jobs: Number of parallel jobs (-1 for all cores).
        create_visualizations: Whether to create comparison visualizations.
        
    Returns:
        Dictionary with optimization results and statistics.
    """
    print("=" * 80)
    print("EXTENDED MULTI-ASSET BATCH OPTIMIZATION")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Default asset list if none provided
    if symbols is None:
        symbols = [
            "BTC-USD",    # Bitcoin (high market cap, moderate volatility)
            "ETH-USD",    # Ethereum (high market cap, moderate volatility)
            "SOL-USD",    # Solana (mid market cap, high volatility)
            "LINK-USD",   # Chainlink (mid market cap, moderate volatility)
            "MATIC-USD",  # Polygon (mid market cap, high volatility)
            "AAVE-USD",   # Aave (lower market cap, high volatility)
        ]
    
    # Default timeframes if none provided    
    if timeframes is None:
        timeframes = ["15m", "1h", "4h"]
    
    # Production-grade optimization configuration
    config = BatchOptimizerConfig(
        # Asset list
        symbols=symbols,
        
        # Multiple timeframes for comprehensive testing
        timeframes=timeframes,
        
        # Use longer training windows for more robust parameter sets
        training_windows=[30, 60],  # 30 and 60 days
        
        # Test windows that are reasonable fractions of training windows
        # Adjusted 60-day test window from 20 to 19 days to fit data length
        testing_windows=[{30: 10}, {60: 19}],
        
        # Data range for optimization
        start_date="2022-01-01",
        
        # More trials for thorough parameter space exploration
        n_trials=n_trials,
        
        # Longer timeout for more complex optimizations
        timeout=1800,  # 30 minutes
        
        # Use more splits for better validation
        n_splits=3,
        
        # Enable asset-specific parameter optimization
        use_asset_profiles=True,
        analyze_new_profiles=True,
        
        # Run in parallel for faster execution
        parallel=parallel,
        n_jobs=n_jobs,
        
        # Save intermediate results
        save_interval=save_interval
    )
    
    # Create and run the batch optimizer
    optimizer = BatchOptimizer(config)
    
    # Run the batch optimization
    start_time = time.time()
    optimizer.run_batch()
    
    # Save results and generate report
    optimizer.save_results()
    
    print("\nResults for all assets:")
    # Access the run_results list which contains all results
    results = optimizer.run_results if hasattr(optimizer, 'run_results') else []
    
    # Calculate total runtime
    runtime = time.time() - start_time
    hours, remainder = divmod(runtime, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Organize results for analysis
    results_by_asset = {}
    for symbol in config.symbols:
        symbol_results = [r for r in results if r.get('symbol') == symbol and r.get('status') == 'success']
        if symbol_results:
            results_by_asset[symbol] = symbol_results
    
    # Print summary
    print("\n" + "=" * 80)
    print("EXTENDED BATCH OPTIMIZATION RESULTS")
    print("=" * 80)
    print(f"Total runtime: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"Assets tested: {len(config.symbols)}")
    print(f"Timeframes tested: {len(config.timeframes)}")
    print(f"Total configurations: {len(config.symbols) * len(config.timeframes) * len(config.training_windows)}")
    print(f"Completed runs: {len(optimizer.completed_runs)}")
    print(f"Failed runs: {len(optimizer.failed_runs)}")
    
    # Create a detailed results DataFrame
    all_results = []
    for result in results:
        if result.get('status') != 'success':
            continue
            
        # Extract basic information
        basic_info = {
            'symbol': result.get('symbol'),
            'timeframe': result.get('timeframe'),
            'training_window': result.get('training_window'),
            'best_value': result.get('best_value'),
            'trial_count': result.get('trial_count', 0)
        }
        
        # Extract best parameters
        best_params = result.get('best_params', {})
        for param, value in best_params.items():
            basic_info[f'param_{param}'] = value
            
        all_results.append(basic_info)
    
    # Create DataFrame for analysis
    if all_results:
        results_df = pd.DataFrame(all_results)
        
        # Save detailed results to CSV
        results_file = results_dir / "extended_optimization_results.csv"
        results_df.to_csv(results_file, index=False)
        print(f"\nDetailed results saved to: {results_file}")
        
        # Generate visualization if requested
        if create_visualizations and not results_df.empty:
            create_parameter_comparison_charts(results_df, results_dir)
    
    # Print asset-specific best results
    print("\nBest Results by Asset:")
    
    for symbol, symbol_results in results_by_asset.items():
        if not symbol_results:
            continue
            
        best_result = max(symbol_results, key=lambda x: x.get('best_value', -float('inf')))
        print(f"\n{symbol} Best Result:")
        print(f"  Best value: {best_result.get('best_value', 'N/A')}")
        print(f"  Timeframe: {best_result.get('timeframe', 'N/A')}")
        print(f"  Training window: {best_result.get('training_window', 'N/A')} days")
        
        # Show top parameters
        print("  Top parameters:")
        if 'best_params' in best_result:
            for param, value in best_result['best_params'].items():
                print(f"    {param}: {value}")
        else:
            print("    No parameters available")
    
    # Update STRATEGY_OVERVIEW.md with optimal parameters
    update_strategy_overview(results_by_asset)
    
    print(f"\nExtended optimization complete!")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return results for further analysis
    return {
        'config': config,
        'results': results,
        'results_by_asset': results_by_asset,
        'runtime': runtime,
        'completed_runs': len(optimizer.completed_runs),
        'failed_runs': len(optimizer.failed_runs)
    }

def create_parameter_comparison_charts(results_df: pd.DataFrame, output_dir: Path) -> None:
    """
    Create visualization charts comparing parameters across assets.
    
    Args:
        results_df: DataFrame containing optimization results
        output_dir: Directory to save charts
    """
    print("\nGenerating parameter comparison visualizations...")
    
    # Create charts directory
    charts_dir = output_dir / "charts"
    charts_dir.mkdir(exist_ok=True)
    
    # Get parameter columns (those starting with 'param_')
    param_cols = [col for col in results_df.columns if col.startswith('param_')]
    
    # Skip if no parameter columns
    if not param_cols:
        print("  No parameter columns found for visualization")
        return
        
    # 1. Create parameter distribution charts by asset
    for param_col in param_cols:
        param_name = param_col.replace('param_', '')
        
        try:
            # Skip parameters that aren't numeric
            if not pd.api.types.is_numeric_dtype(results_df[param_col]):
                continue
                
            plt.figure(figsize=(12, 8))
            
            # Create boxplot for parameter by asset
            ax = results_df.boxplot(column=param_col, by='symbol', 
                                   grid=False, return_type='axes')
            
            plt.title(f'Distribution of {param_name} by Asset', fontsize=14)
            plt.suptitle('')  # Remove default suptitle
            plt.xlabel('Asset', fontsize=12)
            plt.ylabel(param_name, fontsize=12)
            plt.xticks(rotation=45)
            
            # Save figure
            chart_file = charts_dir / f"param_distribution_{param_name}.png"
            plt.tight_layout()
            plt.savefig(chart_file)
            plt.close()
            print(f"  Created chart: {chart_file.name}")
        except Exception as e:
            print(f"  Error creating chart for {param_name}: {e}")
    
    # 2. Create correlation matrix for parameters
    try:
        # Select only numeric parameter columns
        numeric_params = results_df[param_cols].select_dtypes(include=['number'])
        
        if not numeric_params.empty and len(numeric_params.columns) > 1:
            plt.figure(figsize=(12, 10))
            
            # Calculate correlation matrix
            corr = numeric_params.corr()
            
            # Plot heatmap
            plt.imshow(corr, cmap='coolwarm', interpolation='none', aspect='auto')
            plt.colorbar(label='Correlation coefficient')
            
            # Add correlation values
            for i in range(len(corr.columns)):
                for j in range(len(corr.columns)):
                    plt.text(j, i, f'{corr.iloc[i, j]:.2f}', 
                             ha='center', va='center', 
                             color='white' if abs(corr.iloc[i, j]) > 0.5 else 'black')
            
            # Add labels
            plt.xticks(range(len(corr.columns)), [c.replace('param_', '') for c in corr.columns], rotation=90)
            plt.yticks(range(len(corr.columns)), [c.replace('param_', '') for c in corr.columns])
            
            plt.title('Parameter Correlation Matrix', fontsize=14)
            plt.tight_layout()
            
            # Save figure
            chart_file = charts_dir / "parameter_correlation_matrix.png"
            plt.savefig(chart_file)
            plt.close()
            print(f"  Created correlation matrix: {chart_file.name}")
    except Exception as e:
        print(f"  Error creating correlation matrix: {e}")
    
    # 3. Create best value comparison by asset and timeframe
    try:
        plt.figure(figsize=(14, 8))
        
        # Pivot data to create heatmap
        pivot_data = results_df.pivot_table(
            values='best_value', 
            index='symbol', 
            columns='timeframe', 
            aggfunc='max'
        )
        
        # Plot heatmap
        plt.imshow(pivot_data, cmap='YlGn', interpolation='none', aspect='auto')
        plt.colorbar(label='Best value (Sharpe or metric)')
        
        # Add values
        for i in range(len(pivot_data.index)):
            for j in range(len(pivot_data.columns)):
                try:
                    value = pivot_data.iloc[i, j]
                    plt.text(j, i, f'{value:.2f}', 
                             ha='center', va='center', 
                             color='black' if value < pivot_data.values.max() * 0.7 else 'white')
                except:
                    pass
        
        # Add labels
        plt.xticks(range(len(pivot_data.columns)), pivot_data.columns)
        plt.yticks(range(len(pivot_data.index)), pivot_data.index)
        
        plt.title('Best Value by Asset and Timeframe', fontsize=14)
        plt.xlabel('Timeframe', fontsize=12)
        plt.ylabel('Asset', fontsize=12)
        
        plt.tight_layout()
        
        # Save figure
        chart_file = charts_dir / "best_value_by_asset_timeframe.png"
        plt.savefig(chart_file)
        plt.close()
        print(f"  Created best value comparison: {chart_file.name}")
    except Exception as e:
        print(f"  Error creating best value comparison: {e}")
        
    print("Visualization generation complete!")

def update_strategy_overview(results_by_asset: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Update the STRATEGY_OVERVIEW.md document with optimal parameters from the optimization.
    
    Args:
        results_by_asset: Dictionary of optimization results organized by asset
    """
    strategy_overview_path = project_root / "docs" / "STRATEGY_OVERVIEW.md"
    
    # Check if file exists
    if not strategy_overview_path.exists():
        print(f"Warning: {strategy_overview_path} does not exist. Skipping update.")
        return
    
    # Read existing content
    with open(strategy_overview_path, 'r') as f:
        content = f.read()
    
    # Check if Asset-Specific Parameters section exists, otherwise add it
    asset_section_header = "## Asset-Specific Optimal Parameters"
    if asset_section_header not in content:
        # Add section at the end
        content += f"\n\n{asset_section_header}\n\n"
        content += "This section contains asset-specific optimal parameters determined through extended batch optimization.\n\n"
    
    # Split content to insert at the right position
    before_section, after_section = content.split(asset_section_header)
    
    # Further split after_section to preserve content after parameter tables
    after_header_parts = after_section.split("\n\n", 2)
    section_intro = after_header_parts[0] + "\n\n" if len(after_header_parts) > 0 else "\n\n"
    remaining_content = "\n\n" + after_header_parts[2] if len(after_header_parts) > 2 else ""
    
    # Create updated section with parameter tables
    updated_section = f"{asset_section_header}\n{section_intro}"
    updated_section += f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n\n"
    
    # Add parameter tables for each asset
    for symbol, results in results_by_asset.items():
        if not results:
            continue
            
        # Find best result for the asset
        best_result = max(results, key=lambda x: x.get('best_value', -float('inf')))
        
        updated_section += f"### {symbol}\n\n"
        updated_section += f"**Best configuration:**\n"
        updated_section += f"- Timeframe: {best_result.get('timeframe', 'N/A')}\n"
        updated_section += f"- Training window: {best_result.get('training_window', 'N/A')} days\n"
        updated_section += f"- Performance metric: {best_result.get('best_value', 'N/A'):.4f}\n\n"
        
        # Add parameter table
        if 'best_params' in best_result and best_result['best_params']:
            updated_section += "| Parameter | Value |\n"
            updated_section += "|-----------|-------|\n"
            
            for param, value in sorted(best_result['best_params'].items()):
                # Format value based on type
                if isinstance(value, bool):
                    formatted_value = "✓" if value else "✗"
                elif isinstance(value, (int, float)):
                    formatted_value = f"{value:g}"
                else:
                    formatted_value = str(value)
                    
                updated_section += f"| {param} | {formatted_value} |\n"
            
            updated_section += "\n"
        else:
            updated_section += "No parameters available\n\n"
    
    # Combine updated content
    updated_content = before_section + updated_section + remaining_content
    
    # Write updated content
    with open(strategy_overview_path, 'w') as f:
        f.write(updated_content)
    
    print(f"\nUpdated {strategy_overview_path} with asset-specific parameters")

if __name__ == "__main__":
    run_extended_multi_asset_optimization()
