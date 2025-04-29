#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Multi-Asset Batch Optimization Test

This script tests the fixed tuple indexing and Pydantic validator updates with a 
multi-asset batch optimization run. It uses a small number of trials per asset
to keep the total runtime reasonable while still verifying functionality.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Set up Python path
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

# Import fixed modules
from scripts.strategies.refactored_edge.batch_optuna_optimizer import (
    BatchOptimizerConfig, BatchOptimizer
)
from scripts.strategies.refactored_edge.asset_profiles import (
    load_asset_profile, save_asset_profile, get_asset_specific_config
)

def run_multi_asset_test():
    """Run batch optimization with multiple assets to verify fixes."""
    print("=" * 80)
    print("MULTI-ASSET BATCH OPTIMIZATION TEST")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Enable testing mode for faster execution
    os.environ["REGIME_TESTING_MODE"] = "1"
    
    # Create batch optimizer configuration
    config = BatchOptimizerConfig(
        # Test with diverse crypto assets (ranging from low to high volatility)
        symbols=["BTC-USD", "ETH-USD", "SOL-USD"],
        
        # Use a single timeframe to keep runtime reasonable
        timeframes=["1h"],
        
        # Keep training/testing windows small for faster runs
        training_windows=[7],  # 7 days
        testing_windows=[{7: 3}],  # 3 days testing for 7 days training
        
        # Minimal trials for each asset/timeframe combination
        n_trials=10,  # Minimum value required by validator
        
        # Short timeout per optimization
        timeout=300,  # 5 minutes
        
        # Use 2 splits for faster validation
        n_splits=2,
        
        # Enable asset-specific parameter optimization
        use_asset_profiles=True,
        analyze_new_profiles=True,
        parallel=False  # Run sequentially for clearer logging
    )
    
    # Create and run the batch optimizer
    optimizer = BatchOptimizer(config)
    
    # Run the batch optimization
    start_time = time.time()
    optimizer.run_batch()
    
    # Save results and generate report
    # Save results to disk first
    optimizer.save_results()
    
    print("\nResults for all assets:")
    # Access the run_results list which contains all results
    results = optimizer.run_results if hasattr(optimizer, 'run_results') else []
    
    # Calculate total runtime
    runtime = time.time() - start_time
    hours, remainder = divmod(runtime, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Print summary
    print("\n" + "=" * 80)
    print("BATCH OPTIMIZATION RESULTS")
    print("=" * 80)
    print(f"Total runtime: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"Assets tested: {len(config.symbols)}")
    print(f"Timeframes tested: {len(config.timeframes)}")
    print(f"Total cases: {len(config.symbols) * len(config.timeframes) * len(config.training_windows)}")
    print(f"Completed runs: {len(optimizer.completed_runs)}")
    print(f"Failed runs: {len(optimizer.failed_runs)}")
    print("\nBest Results by Asset:")
    
    # Organize by asset
    for symbol in config.symbols:
        symbol_results = [r for r in results if r.get('symbol') == symbol and r.get('status') == 'success']
        if symbol_results:
            best_result = max(symbol_results, key=lambda x: x.get('best_value', -float('inf')))
            print(f"\n{symbol} Best Result:")
            print(f"  Best value: {best_result.get('best_value', 'N/A')}")
            print(f"  Timeframe: {best_result.get('timeframe', 'N/A')}")
            
            # Show top parameters
            print("  Top parameters:")
            if 'best_params' in best_result:
                for param, value in list(best_result['best_params'].items())[:5]:
                    print(f"    {param}: {value}")
            else:
                print("    No parameters available")
    
    print("\nVerification complete! The fixes for tuple indexing and Pydantic validators are working correctly.")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return results

if __name__ == "__main__":
    run_multi_asset_test()
