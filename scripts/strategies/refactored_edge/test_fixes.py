#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify the fixes for tuple indexing and Pydantic validators.
Uses a small dataset and reduced number of trials to quickly validate functionality.
"""

import os
import sys
from pathlib import Path

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

# Import the fixed modules
from scripts.strategies.refactored_edge.run_optuna_optimization import (
    run_optimization, ensure_directories
)
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness

# Enable testing mode for faster execution
os.environ["REGIME_TESTING_MODE"] = "1"

def run_test():
    """Run a minimal test with reduced parameters."""
    print("Starting test of tuple indexing fix and Pydantic validator updates...")
    
    # Make sure directories exist
    ensure_directories()
    
    # Run with minimal settings for quick validation
    result = run_optimization(
        symbol="BTC-USD",
        timeframe="1h",
        train_days=7,          # Small window for faster testing
        test_days=3,           # Small window for faster testing
        n_trials=3,            # Minimal trials for a quick test
        n_splits=2,            # Minimal splits for a quick test
        timeout=300            # Short timeout (5 minutes)
    )
    
    # Check the result
    if result["status"] == "success":
        print("\n✅ Test passed! The tuple indexing fix and Pydantic validator updates are working correctly.")
        print(f"Best value (penalized Sharpe ratio): {result['best_value']}")
        print("\nBest parameters:")
        for param, value in result["best_params"].items():
            print(f"  {param}: {value}")
    else:
        print("\n❌ Test failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return result

if __name__ == "__main__":
    run_test()
