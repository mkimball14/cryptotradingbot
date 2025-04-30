"""
Unit tests for the position_sizing module.

Tests the core functionality of the position sizing module including:
- Risk-based position sizing
- Integrated position sizing with volatility and regime adjustment
- Kelly criterion calculation
- Edge cases and error handling
"""
import unittest
import numpy as np
import pandas as pd
from scripts.strategies.refactored_edge.position_sizing import (
    calculate_kelly_fraction,
    get_regime_position_multiplier,
    calculate_risk_based_size,
    calculate_integrated_position_size,
    PositionSizeMethod,
    MarketRegimeType
)


class TestPositionSizing(unittest.TestCase):
    """Test cases for position sizing functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Common test parameters
        self.equity = 10000.0
        self.entry_price = 50000.0
        self.atr = 1000.0
        self.stop_loss_price = 49000.0
    
    def test_calculate_risk_based_size(self):
        """Test risk-based position sizing."""
        # Test with $100 risk on a $1000 price difference
        risk_amount = 100.0
        expected_size = 0.1  # $100 / $1000 = 0.1 units
        
        position_size = calculate_risk_based_size(
            entry_price=self.entry_price,
            stop_loss_price=self.stop_loss_price,
            risk_amount=risk_amount
        )
        
        self.assertAlmostEqual(position_size, expected_size, places=5)
        print(f"Risk-based size calculation - Risk: ${risk_amount}, Position size: {position_size}")
        
        # Test with constraints
        position_size_constrained = calculate_risk_based_size(
            entry_price=self.entry_price,
            stop_loss_price=self.stop_loss_price,
            risk_amount=risk_amount,
            min_size=0.05,
            max_size=0.08
        )
        
        self.assertEqual(position_size_constrained, 0.08)
        print(f"Constrained risk-based size: {position_size_constrained} (capped at max_size)")
    
    def test_risk_based_size_validation(self):
        """Test validation in risk-based position sizing."""
        # Test with negative entry price
        with self.assertRaises(ValueError):
            calculate_risk_based_size(-1.0, 100.0, 100.0)
        
        # Test with negative stop loss
        with self.assertRaises(ValueError):
            calculate_risk_based_size(100.0, -1.0, 100.0)
        
        # Test with negative risk amount
        with self.assertRaises(ValueError):
            calculate_risk_based_size(100.0, 90.0, -100.0)
        
        # Test with zero price difference (avoid division by zero)
        position_size = calculate_risk_based_size(100.0, 100.0, 100.0, min_size=0.01)
        self.assertEqual(position_size, 0.01)
        print(f"Position size with zero stop distance (should be min_size): {position_size}")
    
    def test_kelly_fraction(self):
        """Test Kelly Criterion calculation."""
        # Win rate of 60%, win/loss ratio of 2.0
        win_rate = 0.6
        win_loss_ratio = 2.0
        # Expected Kelly fraction: 0.6 - (0.4/2.0) = 0.6 - 0.2 = 0.4
        expected_kelly = 0.4
        
        kelly = calculate_kelly_fraction(win_rate, win_loss_ratio)
        self.assertAlmostEqual(kelly, expected_kelly, places=5)
        print(f"Kelly fraction with win rate {win_rate} and win/loss ratio {win_loss_ratio}: {kelly}")
        
        # Test negative Kelly (should be capped at 0)
        kelly_negative = calculate_kelly_fraction(0.3, 1.0)
        self.assertGreaterEqual(kelly_negative, 0.0)
        print(f"Kelly fraction with unfavorable parameters: {kelly_negative}")
    
    def test_regime_multiplier(self):
        """Test regime-specific position multipliers."""
        # Test trending regime
        trending_multiplier = get_regime_position_multiplier(MarketRegimeType.TRENDING)
        self.assertEqual(trending_multiplier, 1.0)
        
        # Test ranging regime
        ranging_multiplier = get_regime_position_multiplier(MarketRegimeType.RANGING)
        self.assertEqual(ranging_multiplier, 0.75)
        
        # Test unknown regime
        unknown_multiplier = get_regime_position_multiplier("unknown_regime")
        self.assertEqual(unknown_multiplier, 0.5)
        print(f"Multipliers - Trending: {trending_multiplier}, Ranging: {ranging_multiplier}, Unknown: {unknown_multiplier}")
        
        # Test custom multipliers
        custom_multipliers = {
            MarketRegimeType.TRENDING: 1.5,
            MarketRegimeType.RANGING: 0.5
        }
        custom_trending = get_regime_position_multiplier(
            MarketRegimeType.TRENDING, 
            custom_multipliers
        )
        self.assertEqual(custom_trending, 1.5)
        print(f"Custom trending multiplier: {custom_trending}")
    
    def test_integrated_position_size(self):
        """Test the integrated position sizing approach."""
        # Test with trending market regime - using smaller risk percentage to avoid hitting caps
        trending_size = calculate_integrated_position_size(
            equity=self.equity,
            entry_price=self.entry_price,
            atr=self.atr,
            market_regime=MarketRegimeType.TRENDING,
            risk_percentage=0.001,  # Small risk to avoid cap
            stop_loss_price=self.stop_loss_price,
            min_size=0.0001,  # Very small minimum
            max_size=1.0      # Large maximum
        )
        
        # Test with ranging market regime
        ranging_size = calculate_integrated_position_size(
            equity=self.equity,
            entry_price=self.entry_price,
            atr=self.atr,
            market_regime=MarketRegimeType.RANGING,
            risk_percentage=0.001,  # Small risk to avoid cap
            stop_loss_price=self.stop_loss_price,
            min_size=0.0001,  # Very small minimum
            max_size=1.0      # Large maximum
        )
        
        # Ranging market should have smaller size than trending
        self.assertGreater(trending_size, ranging_size)
        print(f"Trending size: {trending_size}, Ranging size: {ranging_size}")
        
        # Test with zone confidence in ranging market
        ranging_with_zone = calculate_integrated_position_size(
            equity=self.equity,
            entry_price=self.entry_price,
            atr=self.atr,
            market_regime=MarketRegimeType.RANGING,
            risk_percentage=0.001,  # Small risk to avoid cap
            stop_loss_price=self.stop_loss_price,
            zone_confidence=0.8,
            min_size=0.0001,        # Very small minimum
            max_size=1.0            # Large maximum
        )
        
        # Higher zone confidence should increase size compared to standard ranging
        self.assertGreater(ranging_with_zone, ranging_size)
        print(f"Ranging with zone confidence: {ranging_with_zone}, Regular ranging: {ranging_size}")
        
        # Test with Kelly adjustment
        kelly_size = calculate_integrated_position_size(
            equity=self.equity,
            entry_price=self.entry_price,
            atr=self.atr,
            market_regime=MarketRegimeType.TRENDING,
            risk_percentage=0.001,  # Small risk to avoid cap
            stop_loss_price=self.stop_loss_price,
            kelly_enabled=True,
            win_rate=0.6,
            win_loss_ratio=2.0,
            max_kelly_percentage=0.5,
            min_size=0.0001,        # Very small minimum
            max_size=1.0            # Large maximum
        )
        
        # Kelly should reduce size (0.5 * 0.4 = 0.2 multiplier effect)
        self.assertLess(kelly_size, trending_size)
        print(f"Kelly-adjusted size: {kelly_size}, Regular trending: {trending_size}")
    
    def test_integrated_size_validation(self):
        """Test validation in integrated position sizing."""
        # Test with negative equity
        with self.assertRaises(ValueError):
            calculate_integrated_position_size(
                equity=-1.0,
                entry_price=self.entry_price,
                atr=self.atr,
                market_regime=MarketRegimeType.TRENDING
            )
        
        # Test with negative entry price
        with self.assertRaises(ValueError):
            calculate_integrated_position_size(
                equity=self.equity,
                entry_price=-1.0,
                atr=self.atr,
                market_regime=MarketRegimeType.TRENDING
            )
        
        # Test with negative ATR
        with self.assertRaises(ValueError):
            calculate_integrated_position_size(
                equity=self.equity,
                entry_price=self.entry_price,
                atr=-1.0,
                market_regime=MarketRegimeType.TRENDING
            )
    
    def test_automatic_stop_calculation(self):
        """Test automatic stop loss price calculation with ATR."""
        # Test without explicit stop loss (should calculate from ATR)
        position_size = calculate_integrated_position_size(
            equity=self.equity,
            entry_price=self.entry_price,
            atr=self.atr,
            market_regime=MarketRegimeType.TRENDING,
            risk_percentage=0.001,  # Small risk to avoid cap
            stop_atr_multiple=1.5,  # Stop is 1.5 ATR below entry
            min_size=0.0001,        # Very small minimum
            max_size=1.0            # Large maximum
        )
        
        # Verify position size is reasonable (not zero or too large)
        self.assertGreater(position_size, 0.0)
        
        # With 1.5 ATR stop and 1% risk, position should be smaller than 
        # our standard test with 1 ATR stop
        standard_size = calculate_integrated_position_size(
            equity=self.equity,
            entry_price=self.entry_price,
            atr=self.atr,
            market_regime=MarketRegimeType.TRENDING,
            risk_percentage=0.001,  # Small risk to avoid cap
            stop_loss_price=self.entry_price - self.atr,
            min_size=0.0001,        # Very small minimum
            max_size=1.0            # Large maximum
        )
        
        # Since 1.5 ATR stop is further away, position should be smaller
        self.assertLess(position_size, standard_size)
        print(f"Position with 1.5 ATR stop: {position_size}, Position with 1 ATR stop: {standard_size}")


if __name__ == '__main__':
    unittest.main()
