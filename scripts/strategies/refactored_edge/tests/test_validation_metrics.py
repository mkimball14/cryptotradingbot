#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for enhanced validation metrics.

This test suite validates the functions in the validation_metrics module
that provide signal quality evaluation, parameter stability analysis,
and strategy robustness assessment.
"""

import os
import sys
import unittest
from pathlib import Path

import pandas as pd
import numpy as np

# Add project root to path for imports
current_file = Path(__file__).resolve()
project_root = current_file.parents[4]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from scripts.strategies.refactored_edge.validation_metrics import (
    calculate_signal_quality_metrics,
    evaluate_parameter_stability,
    evaluate_robustness_across_regimes,
    statistical_significance_test
)


class TestValidationMetrics(unittest.TestCase):
    """Tests for validation metrics module functionality."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample data for testing
        self.dates = pd.date_range(start='2023-01-01', periods=1000, freq='1h')
        self.entries = pd.Series(False, index=self.dates)
        self.exits = pd.Series(False, index=self.dates)
        
        # Set some random entries and exits
        np.random.seed(42)
        entry_points = np.random.choice(range(900), size=10, replace=False)
        exit_points = entry_points + np.random.randint(10, 50, size=10)
        
        for i, j in zip(entry_points, exit_points):
            if j < len(self.dates):
                self.entries.iloc[i] = True
                self.exits.iloc[j] = True
        
        # Create sample equity curve and returns
        self.equity = pd.Series(1000, index=self.dates)
        for i in range(1, len(self.dates)):
            change = np.random.normal(0.0001, 0.001)
            if self.entries.iloc[i-1]:
                change = np.random.normal(0.001, 0.002)  # Positive bias after entry
            self.equity.iloc[i] = self.equity.iloc[i-1] * (1 + change)
        
        # Sample trade returns
        self.returns = pd.Series(np.random.normal(0.02, 0.05, size=10))
        
        # Sample optimization results for parameter stability testing
        self.optimization_results = [
            {
                'best_value': 1.5,
                'param_rsi_window': 14,
                'param_atr_window': 20,
                'param_trend_threshold_pct': 0.01,
                'param_zone_influence': 0.5
            },
            {
                'best_value': 1.7,
                'param_rsi_window': 15,
                'param_atr_window': 21,
                'param_trend_threshold_pct': 0.012,
                'param_zone_influence': 0.52
            },
            {
                'best_value': 1.6,
                'param_rsi_window': 14,
                'param_atr_window': 19,
                'param_trend_threshold_pct': 0.011,
                'param_zone_influence': 0.48
            }
        ]
        
        # Sample regime performance results
        self.regime_results = {
            'bullish': {
                'sharpe_ratio': 2.1,
                'win_rate': 0.65,
                'num_trades': 20,
                'profit_factor': 1.8
            },
            'bearish': {
                'sharpe_ratio': 1.2,
                'win_rate': 0.55,
                'num_trades': 15,
                'profit_factor': 1.3
            },
            'sideways': {
                'sharpe_ratio': 1.5,
                'win_rate': 0.60,
                'num_trades': 25,
                'profit_factor': 1.5
            }
        }
    
    def test_signal_quality_metrics(self):
        """Test signal quality metric calculation."""
        metrics = calculate_signal_quality_metrics(
            entries=self.entries,
            exits=self.exits,
            equity_curve=self.equity,
            returns=self.returns,
            parameters={'signal_strictness': 'BALANCED'}
        )
        
        # Verify required metrics are present
        self.assertIn('num_signals', metrics)
        self.assertIn('signal_quality_score', metrics)
        self.assertIn('signal_efficiency', metrics)
        self.assertIn('parameter_sensitivity', metrics)
        self.assertIn('signal_consistency', metrics)
        
        # Check expected signal count
        expected_signal_count = self.entries.sum() + self.exits.sum()
        self.assertEqual(metrics['num_signals'], expected_signal_count)
        
        # Signal quality score should be between 0 and 100
        self.assertGreaterEqual(metrics['signal_quality_score'], 0)
        self.assertLessEqual(metrics['signal_quality_score'], 100)
        
        # Test with empty signals
        empty_entries = pd.Series(False, index=self.dates)
        empty_exits = pd.Series(False, index=self.dates)
        empty_metrics = calculate_signal_quality_metrics(
            entries=empty_entries,
            exits=empty_exits,
            equity_curve=self.equity,
            returns=pd.Series(),
            parameters={'signal_strictness': 'BALANCED'}
        )
        
        # Should have appropriate default values for empty case
        self.assertEqual(empty_metrics['num_signals'], 0)
        self.assertEqual(empty_metrics['signal_quality_score'], 0.0)
    
    def test_parameter_stability(self):
        """Test parameter stability evaluation."""
        stability_metrics = evaluate_parameter_stability(
            optimization_results=self.optimization_results,
            parameter_names=['rsi_window', 'atr_window', 'trend_threshold_pct', 'zone_influence']
        )
        
        # Verify required metrics are present
        self.assertIn('stability_score', stability_metrics)
        self.assertIn('parameter_variance', stability_metrics)
        
        # Stability score should be between 0 and 1
        self.assertGreaterEqual(stability_metrics['stability_score'], 0)
        self.assertLessEqual(stability_metrics['stability_score'], 1)
        
        # Variance should be calculated for each parameter
        self.assertIn('rsi_window', stability_metrics['parameter_variance'])
        self.assertIn('atr_window', stability_metrics['parameter_variance'])
        self.assertIn('trend_threshold_pct', stability_metrics['parameter_variance'])
        self.assertIn('zone_influence', stability_metrics['parameter_variance'])
        
        # Test with empty optimization results
        empty_stability = evaluate_parameter_stability(
            optimization_results=[],
            parameter_names=['rsi_window', 'atr_window']
        )
        
        # Should have appropriate default values for empty case
        self.assertEqual(empty_stability['stability_score'], 0.0)
        self.assertEqual(empty_stability['parameter_variance'], {})
    
    def test_robustness_across_regimes(self):
        """Test robustness evaluation across market regimes."""
        robustness_metrics = evaluate_robustness_across_regimes(
            results_by_regime=self.regime_results
        )
        
        # Verify required metrics are present
        self.assertIn('robustness_score', robustness_metrics)
        self.assertIn('regime_performance', robustness_metrics)
        self.assertIn('regime_consistency', robustness_metrics)
        
        # Robustness score should be between 0 and 100
        self.assertGreaterEqual(robustness_metrics['robustness_score'], 0)
        self.assertLessEqual(robustness_metrics['robustness_score'], 100)
        
        # Test with custom weights
        weights = {'bullish': 0.5, 'bearish': 0.3, 'sideways': 0.2}
        weighted_robustness = evaluate_robustness_across_regimes(
            results_by_regime=self.regime_results,
            regime_weights=weights
        )
        
        # Weighted result should be different from unweighted
        self.assertNotEqual(
            weighted_robustness['weighted_performance'],
            robustness_metrics['weighted_performance']
        )
        
        # Test with empty results
        empty_robustness = evaluate_robustness_across_regimes(
            results_by_regime={}
        )
        
        # Should have appropriate default values for empty case
        self.assertEqual(empty_robustness['robustness_score'], 0.0)
        self.assertEqual(empty_robustness['regime_performance'], {})
    
    def test_statistical_significance(self):
        """Test statistical significance testing."""
        # Create two sets of trade returns
        np.random.seed(42)
        returns_a = np.random.normal(0.02, 0.05, size=30)
        returns_b = np.random.normal(0.01, 0.05, size=30)
        
        # Simple metrics
        metrics_a = {'sharpe_ratio': 1.5, 'win_rate': 0.6}
        metrics_b = {'sharpe_ratio': 1.2, 'win_rate': 0.55}
        
        # Run significance test
        sig_results = statistical_significance_test(
            performance_metrics_a=metrics_a,
            performance_metrics_b=metrics_b,
            trade_returns_a=returns_a.tolist(),
            trade_returns_b=returns_b.tolist()
        )
        
        # Verify required metrics are present
        self.assertIn('is_significant', sig_results)
        self.assertIn('p_value', sig_results)
        self.assertIn('test_method', sig_results)
        
        # Test with insufficient data
        small_sig_results = statistical_significance_test(
            performance_metrics_a=metrics_a,
            performance_metrics_b=metrics_b,
            trade_returns_a=[0.01, 0.02],
            trade_returns_b=[0.01, 0.02]
        )
        
        # Should indicate insufficient data
        self.assertEqual(small_sig_results['test_method'], 'insufficient_data')
        self.assertFalse(small_sig_results['is_significant'])


if __name__ == '__main__':
    unittest.main()
