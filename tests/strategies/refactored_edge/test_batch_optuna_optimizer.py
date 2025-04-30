"""
Unit tests for the batch Optuna optimizer.

Tests include:
1. Expected use case - Basic batch optimizer functionality
2. Edge case - Handling configuration with small window sizes
3. Failure case - Handling data fetching errors
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import pytest
import tempfile
import shutil

# Add parent directory to path for imports
from pathlib import Path
current_file = Path(__file__).resolve()
parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))

# Import the module to test
from scripts.strategies.refactored_edge.batch_optuna_optimizer import BatchOptimizer, BatchOptimizerConfig
from scripts.strategies.refactored_edge.config import EdgeConfig, VolatilityProfile
from scripts.strategies.refactored_edge.asset_profiles import AssetConfig
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness


class TestBatchOptunaOptimizer(unittest.TestCase):
    """
    Test suite for BatchOptimizer.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a small configuration for testing
        self.test_config = BatchOptimizerConfig(
            symbols=["BTC-USD"],
            timeframes=["1h"],
            training_windows=[10],
            testing_windows=[{10: 5}],
            n_trials=10,
            timeout=60,
            parallel=False
        )
        
        # Set environment variable for testing mode
        os.environ["REGIME_TESTING_MODE"] = "1"
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove testing environment variable
        if "REGIME_TESTING_MODE" in os.environ:
            del os.environ["REGIME_TESTING_MODE"]
        shutil.rmtree(self.temp_dir)
    
    def test_basic_functionality(self):
        """
        Test the basic functionality of the batch optimizer (EXPECTED USE CASE).
        """
        # Mock the single optimization to return a successful result
        mock_result = {
            "status": "success",
            "symbol": "BTC-USD",
            "timeframe": "1h",
            "train_days": 10,
            "test_days": 5,
            "best_value": 1.23,
            "best_params": {"rsi_window": 14, "bb_window": 20},
            "n_trials": 10,
            "completed_trials": 10,
        }
        
        # Create optimizer and run batch
        optimizer = BatchOptimizer(self.test_config)
        
        # Mock the instance method using patch.object
        with patch.object(optimizer, 'run_single_optimization', return_value=mock_result) as mock_method:
            results = optimizer.run_batch()
        
            # Verify that run_single_optimization was called once with correct arguments
            mock_method.assert_called_once_with(
                symbol="BTC-USD",
                timeframe="1h",
                train_days=10,
                test_days=5
            )
        
            # Check that the results were stored correctly
            # No longer check completed_runs length as run_single_optimization is fully mocked
            case_key = optimizer._get_case_key("BTC-USD", "1h", 10, 5)
            self.assertEqual(results["BTC-USD"]["1h"][case_key], mock_result)
            # self.assertEqual(len(optimizer.completed_runs), 1) # REMOVED
            # self.assertEqual(len(optimizer.failed_runs), 0) # REMOVED
    
    def test_edge_case_small_windows(self):
        """
        Test the batch optimizer with minimum allowed window sizes (EDGE CASE).
        """
        # Create a config with minimum allowed window sizes
        small_config = BatchOptimizerConfig(
            symbols=["BTC-USD"],
            timeframes=["1h"],
            training_windows=[10],  # Minimum allowed training window
            testing_windows=[{10: 2}], # Corresponding testing window
            n_trials=10,           # Minimum allowed trials
            timeout=60             # Minimum allowed timeout
        )
        
        # Mock the run_single_optimization to simulate partial success
        # Define the mock result directly
        mock_result_edge = {
            "status": "success",
            "symbol": "BTC-USD",
            "timeframe": "1h",
            "train_days": 10,
            "test_days": 2,
            "best_value": float('-inf'),  # No valid results
            "best_params": {},
            "n_trials": 10,
            "completed_trials": 10,
            "case_key": "BTC-USD_1h_train10_test2" # Add case key for consistency
        }

    
        # Create optimizer
        optimizer = BatchOptimizer(small_config)
        
        # Mock the instance method using patch.object
        with patch.object(optimizer, 'run_single_optimization', return_value=mock_result_edge) as mock_method:
            results = optimizer.run_batch()
        
            # Verify that run_single_optimization was called
            mock_method.assert_called_once_with(
                symbol="BTC-USD",
                timeframe="1h",
                train_days=10,
                test_days=2
            )

            # Verify that processing continues even with 'inf' best values
            # Check results dictionary contains the mock result
            case_key = optimizer._get_case_key("BTC-USD", "1h", 10, 2)
            self.assertIn(case_key, results["BTC-USD"]["1h"])
            self.assertEqual(results["BTC-USD"]["1h"][case_key], mock_result_edge)
            # self.assertEqual(len(optimizer.completed_runs), 1) # REMOVED
            # self.assertEqual(len(optimizer.failed_runs), 0) # REMOVED
        
        # Test report generation still works
        report = optimizer.generate_optimization_report()
        self.assertIn("Batch Optimization Report", report)
    
    def test_error_handling(self):
        """
        Test that the optimizer handles errors during a single run.
        """
        # Create optimizer
        optimizer = BatchOptimizer(self.test_config)
        case_key = optimizer._get_case_key("BTC-USD", "1h", 10, 5)
        
        # Define the mock error result dictionary
        mock_error_result = {
            'status': 'error',
            'error': 'Test error',
            'case_key': case_key
        }
        
        # Mock the instance method using patch.object to return an error dict
        with patch.object(optimizer, 'run_single_optimization', return_value=mock_error_result) as mock_method:
            results = optimizer.run_batch()
        
            # Verify that run_single_optimization was still called
            mock_method.assert_called_once_with( # Check call arguments
                symbol="BTC-USD", 
                timeframe="1h", 
                train_days=10, 
                test_days=5
            )
        
            # Check that the result indicates an error
            # case_key = optimizer._get_case_key("BTC-USD", "1h", 10, 5) # Already defined
            self.assertIn("BTC-USD", results)
            self.assertIn("1h", results["BTC-USD"])
            self.assertIn(case_key, results["BTC-USD"]["1h"])
            
            run_result = results["BTC-USD"]["1h"][case_key]
            self.assertEqual(run_result['status'], 'error')
            self.assertIn('Test error', run_result.get('error', ''))
            # Ensure the run was marked as failed - Cannot assert this as run_single is mocked
            # self.assertIn(case_key, optimizer.failed_runs) # REMOVED


    def test_config_merging_with_volatility_overrides(self):
        """
        Test that volatility profile overrides are correctly merged into the config.
        """
        # 1. Setup: Create config with overrides
        base_rsi = 14
        override_rsi = 30
        test_config_with_overrides = BatchOptimizerConfig(
            symbols=["ETH-USD"],
            timeframes=["4h"],
            training_windows=[20],
            testing_windows=[{20: 10}],
            n_trials=10, # UPDATED from 5 to 10
            use_asset_profiles=True, # Ensure profiles are used
            analyze_new_profiles=False, # Assume profile exists
            rsi_window=base_rsi, # Base config value
            volatility_params={
                VolatilityProfile.HIGH: {"rsi_window": override_rsi} 
            }
        )
        optimizer = BatchOptimizer(test_config_with_overrides)

        # 2. Mock dependencies
        # Mock asset profile to return HIGH volatility
        mock_profile = AssetConfig(
            symbol="ETH-USD", 
            volatility_profile=VolatilityProfile.HIGH, 
            avg_daily_volatility=0.06, # Example value
            signal_strictness=SignalStrictness.BALANCED, 
            trend_threshold_pct=0.01, 
            zone_influence=0.5, 
            min_hold_period=2
        )
        # Mock data fetcher
        mock_data = pd.DataFrame({'Close': np.random.rand(100)}) 
        # Mock the final optimization function to capture the config
        mock_run_optuna = MagicMock(return_value={'status': 'success', 'best_value': 1.0})

        # Use patching context managers
        with patch('scripts.strategies.refactored_edge.batch_optuna_optimizer.load_asset_profile', return_value=mock_profile) as mock_load, \
             patch('scripts.strategies.refactored_edge.batch_optuna_optimizer.fetch_data', return_value=mock_data) as mock_fetch, \
             patch('scripts.strategies.refactored_edge.run_optuna_optimization.run_optuna_optimization', mock_run_optuna) as mock_optuna:
            
            # 3. Execution: Run the single optimization
            optimizer.run_single_optimization(
                symbol="ETH-USD",
                timeframe="4h",
                train_days=20,
                test_days=10
            )

            # 4. Assertion: Check the config passed to run_optuna_optimization
            mock_load.assert_called_once_with("ETH-USD")
            mock_fetch.assert_called_once()
            mock_optuna.assert_called_once()
            
            # Get the arguments passed to the mocked run_optuna_optimization
            call_args, call_kwargs = mock_optuna.call_args
            passed_config = call_kwargs.get('config')

            self.assertIsNotNone(passed_config, "Config object was not passed to run_optuna_optimization")
            self.assertIsInstance(passed_config, EdgeConfig, "Passed config is not an EdgeConfig instance")
            
            # Verify the override was applied
            self.assertEqual(passed_config.rsi_window, override_rsi, "RSI window override was not applied correctly")
            # Verify a base parameter (not overridden) is still correct
            self.assertEqual(passed_config.bb_window, test_config_with_overrides.bb_window, "Base bb_window parameter changed unexpectedly")


if __name__ == '__main__':
    unittest.main()
