#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test asset profiles functionality.

This test suite validates the asset-specific configuration framework including
volatility profiling, parameter recommendations, and config generation.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import json
from pathlib import Path

import pandas as pd
import numpy as np

# Add project root to path for imports
current_file = Path(__file__).resolve()
project_root = current_file.parents[4]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from scripts.strategies.refactored_edge.asset_profiles import (
    VolatilityProfile, AssetConfig, analyze_asset_volatility,
    recommend_signal_parameters, load_asset_profile, save_asset_profile,
    get_asset_specific_config
)
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.config import EdgeConfig


class TestAssetProfiles(unittest.TestCase):
    """Tests for asset profiles module functionality."""
    
    def setUp(self):
        """Set up test data."""
        # Create synthetic price data with different volatility profiles
        np.random.seed(42)  # For reproducibility
        
        # Create date range
        dates = pd.date_range(start='2023-01-01', periods=1000, freq='1h')
        
        # Low volatility data
        self.low_vol_data = self._create_synthetic_data(dates, vol_factor=0.005)
        
        # Medium volatility data
        self.medium_vol_data = self._create_synthetic_data(dates, vol_factor=0.015)
        
        # High volatility data
        self.high_vol_data = self._create_synthetic_data(dates, vol_factor=0.035)
        
        # Extreme volatility data
        self.extreme_vol_data = self._create_synthetic_data(dates, vol_factor=0.06)
        
        # Sample asset config for testing
        self.sample_asset_config = AssetConfig(
            symbol="TEST-USD",
            volatility_profile=VolatilityProfile.MEDIUM,
            avg_daily_volatility=0.02,
            signal_strictness=SignalStrictness.BALANCED,
            trend_threshold_pct=0.01,
            zone_influence=0.5,
            min_hold_period=2
        )
        
    def _create_synthetic_data(self, dates, vol_factor=0.01):
        """Create synthetic OHLCV data with specified volatility."""
        close = 1000
        prices = []
        
        # Generate random walk with specified volatility
        for i in range(len(dates)):
            close += np.random.normal(0, close * vol_factor)
            prices.append(close)
        
        close_series = pd.Series(prices, index=dates)
        
        # Create OHLC data (with some noise around close price)
        df = pd.DataFrame({
            'open': close_series * (1 + np.random.normal(0, vol_factor/2, len(dates))),
            'high': close_series * (1 + np.random.normal(vol_factor, vol_factor/2, len(dates))),
            'low': close_series * (1 - np.random.normal(vol_factor, vol_factor/2, len(dates))),
            'close': close_series,
            'volume': np.random.randint(1000, 5000, len(dates))
        })
        
        return df
    
    def test_volatility_profile_classification(self):
        """Test volatility profile classification based on price data."""
        # Test low volatility classification
        low_vol_metrics = analyze_asset_volatility(self.low_vol_data)
        self.assertEqual(low_vol_metrics["volatility_profile"], VolatilityProfile.LOW)
        
        # Test medium volatility classification
        medium_vol_metrics = analyze_asset_volatility(self.medium_vol_data)
        self.assertEqual(medium_vol_metrics["volatility_profile"], VolatilityProfile.MEDIUM)
        
        # Test high volatility classification
        high_vol_metrics = analyze_asset_volatility(self.high_vol_data)
        self.assertEqual(high_vol_metrics["volatility_profile"], VolatilityProfile.HIGH)
        
        # Test extreme volatility classification
        extreme_vol_metrics = analyze_asset_volatility(self.extreme_vol_data)
        self.assertEqual(extreme_vol_metrics["volatility_profile"], VolatilityProfile.EXTREME)
    
    def test_recommended_parameters(self):
        """Test parameter recommendations based on volatility profile."""
        # Test low volatility recommendations
        low_vol_params = recommend_signal_parameters(
            VolatilityProfile.LOW, 0.005
        )
        self.assertEqual(low_vol_params["signal_strictness"], SignalStrictness.RELAXED)
        self.assertLess(low_vol_params["trend_threshold_pct"], 0.01)  # Should be lower for low vol
        
        # Test medium volatility recommendations
        medium_vol_params = recommend_signal_parameters(
            VolatilityProfile.MEDIUM, 0.015
        )
        self.assertEqual(medium_vol_params["signal_strictness"], SignalStrictness.BALANCED)
        
        # Test high volatility recommendations
        high_vol_params = recommend_signal_parameters(
            VolatilityProfile.HIGH, 0.035
        )
        self.assertEqual(high_vol_params["signal_strictness"], SignalStrictness.BALANCED)
        self.assertGreater(high_vol_params["zone_influence"], medium_vol_params["zone_influence"])
        
        # Test extreme volatility recommendations
        extreme_vol_params = recommend_signal_parameters(
            VolatilityProfile.EXTREME, 0.05
        )
        self.assertEqual(extreme_vol_params["signal_strictness"], SignalStrictness.STRICT)
        self.assertGreater(extreme_vol_params["min_hold_period"], high_vol_params["min_hold_period"])
    
    def test_save_and_load_profile(self):
        """Test saving and loading asset profiles."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch the project_root to use a temporary directory
            with patch('scripts.strategies.refactored_edge.asset_profiles.project_root', Path(temp_dir)):
                # Test saving
                save_success = save_asset_profile(self.sample_asset_config)
                self.assertTrue(save_success)
                
                # Check that file was created
                profiles_dir = Path(temp_dir) / 'data' / 'asset_profiles'
                expected_file = profiles_dir / 'test_usd_profile.json'
                self.assertTrue(expected_file.exists())
                
                # Test loading
                loaded_profile = load_asset_profile("TEST-USD")
                self.assertIsNotNone(loaded_profile)
                self.assertEqual(loaded_profile.symbol, "TEST-USD")
                self.assertEqual(loaded_profile.volatility_profile, VolatilityProfile.MEDIUM)
                self.assertEqual(loaded_profile.signal_strictness, SignalStrictness.BALANCED)
    
    def test_get_asset_specific_config(self):
        """Test generating asset-specific EdgeConfig."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch the project_root to use a temporary directory
            with patch('scripts.strategies.refactored_edge.asset_profiles.project_root', Path(temp_dir)):
                # Test without existing profile (should analyze data)
                with patch('scripts.strategies.refactored_edge.asset_profiles.analyze_asset_volatility') as mock_analyze:
                    # Setup mock
                    mock_analyze.return_value = {
                        "volatility_profile": VolatilityProfile.HIGH,
                        "avg_daily_volatility": 0.03
                    }
                    
                    # Test with historical data
                    config = get_asset_specific_config(
                        symbol="ETH-USD",
                        historical_data=self.high_vol_data
                    )
                    
                    # Verify analysis was called
                    mock_analyze.assert_called_once()
                    
                    # Check that parameters were applied
                    self.assertIsInstance(config, EdgeConfig)
                    self.assertEqual(config.signal_strictness, SignalStrictness.BALANCED)
                
                # Save a test profile
                save_asset_profile(self.sample_asset_config)
                
                # Test with existing profile
                config = get_asset_specific_config(symbol="TEST-USD")
                
                # Verify parameters from profile were applied
                self.assertEqual(config.signal_strictness, SignalStrictness.BALANCED)
                self.assertEqual(config.zone_influence, 0.5)
                self.assertEqual(config.min_hold_period, 2)
                
                # Test with override parameters
                config = get_asset_specific_config(
                    symbol="TEST-USD",
                    override_params={"zone_influence": 0.8}
                )
                
                # Verify override was applied
                self.assertEqual(config.zone_influence, 0.8)
    
    def test_edge_case_no_historical_data(self):
        """Test edge case when no historical data or profile is available."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch the project_root to use a temporary directory
            with patch('scripts.strategies.refactored_edge.asset_profiles.project_root', Path(temp_dir)):
                # Test with no data and no profile
                config = get_asset_specific_config(symbol="UNKNOWN-TOKEN")
                
                # Should still return a valid config with defaults
                self.assertIsInstance(config, EdgeConfig)
                
                # Default values should be from EdgeConfig defaults
                self.assertEqual(config.signal_strictness, SignalStrictness.BALANCED)
    
    def test_invalid_profile_json(self):
        """Test handling of corrupted profile JSON files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch the project_root to use a temporary directory
            with patch('scripts.strategies.refactored_edge.asset_profiles.project_root', Path(temp_dir)):
                # Create profiles directory
                profiles_dir = Path(temp_dir) / 'data' / 'asset_profiles'
                profiles_dir.mkdir(parents=True, exist_ok=True)
                
                # Create an invalid JSON file
                bad_file = profiles_dir / 'bad_usd_profile.json'
                with open(bad_file, 'w') as f:
                    f.write('{"this is not valid json')
                
                # Test loading invalid profile
                loaded_profile = load_asset_profile("BAD-USD")
                self.assertIsNone(loaded_profile)


if __name__ == '__main__':
    unittest.main()
