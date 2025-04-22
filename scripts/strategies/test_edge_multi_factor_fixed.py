import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import os

# Add project root to path to allow importing strategy module
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Import the strategy class and helper functions
try:
    from scripts.strategies.edge_multi_factor_fixed import (
        EdgeMultiFactorStrategy,
        create_volatility_regime_indicator,
        create_consolidation_breakout_indicator,
        create_volume_divergence_indicator,
        create_market_microstructure_indicator
    )
    STRATEGY_AVAILABLE = True
except ImportError as e:
    print(f"Error importing strategy: {e}. Tests might fail.")
    STRATEGY_AVAILABLE = False

# Helper function to create sample data
def create_test_data(num_rows=100):
    dates = pd.date_range(start='2023-01-01', periods=num_rows, freq='D')
    data = pd.DataFrame(index=dates)
    data['open'] = np.random.rand(num_rows) * 100 + 50000
    data['high'] = data['open'] * (1 + np.random.rand(num_rows) * 0.02)
    data['low'] = data['open'] * (1 - np.random.rand(num_rows) * 0.02)
    data['close'] = data['low'] + (data['high'] - data['low']) * np.random.rand(num_rows)
    data['volume'] = np.random.rand(num_rows) * 1000 + 100
    return data

@unittest.skipIf(not STRATEGY_AVAILABLE, "Strategy module not available")
class TestEdgeMultiFactorFixed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up data for all tests."""
        cls.test_data = create_test_data(num_rows=200) # Use enough data for lookbacks

    def test_strategy_initialization(self):
        """Test if the strategy initializes without errors."""
        try:
            strategy = EdgeMultiFactorStrategy()
            self.assertIsInstance(strategy, EdgeMultiFactorStrategy)
            # Check some default parameters
            self.assertEqual(strategy.lookback_window, 20)
            self.assertEqual(strategy.volatility_threshold, 0.5)
        except Exception as e:
            self.fail(f"Strategy initialization failed: {e}")

    def test_generate_signals_output_structure(self):
        """Test the output structure and types of generate_signals."""
        strategy = EdgeMultiFactorStrategy()
        signals_output = strategy.generate_signals(self.test_data)

        self.assertIsInstance(signals_output, tuple, "Output should be a tuple")
        self.assertEqual(len(signals_output), 4, "Output tuple should have 4 elements")

        long_entries, short_entries, is_trending, is_ranging = signals_output

        self.assertIsInstance(long_entries, pd.Series, "long_entries should be a pandas Series")
        self.assertTrue(pd.api.types.is_bool_dtype(long_entries.dtype), "long_entries should have boolean dtype")
        self.assertEqual(len(long_entries), len(self.test_data), "long_entries length mismatch")

        self.assertIsInstance(short_entries, pd.Series, "short_entries should be a pandas Series")
        self.assertTrue(pd.api.types.is_bool_dtype(short_entries.dtype), "short_entries should have boolean dtype")
        self.assertEqual(len(short_entries), len(self.test_data), "short_entries length mismatch")

        self.assertIsInstance(is_trending, pd.Series, "is_trending should be a pandas Series")
        self.assertTrue(pd.api.types.is_bool_dtype(is_trending.dtype), "is_trending should have boolean dtype")
        self.assertEqual(len(is_trending), len(self.test_data), "is_trending length mismatch")

        self.assertIsInstance(is_ranging, pd.Series, "is_ranging should be a pandas Series")
        self.assertTrue(pd.api.types.is_bool_dtype(is_ranging.dtype), "is_ranging should have boolean dtype")
        self.assertEqual(len(is_ranging), len(self.test_data), "is_ranging length mismatch")

    # --- Placeholder tests for indicator functions ---
    # TODO: Add specific tests for each indicator function with edge cases

    def test_create_volatility_regime_indicator(self):
        """Test the volatility regime indicator function."""
        # --- Test 1: Basic output check (already exists) ---
        close = self.test_data['close']
        lookback_window = 20
        vol_filter_window = 50
        volatility_threshold = 0.5
        signal = create_volatility_regime_indicator(close, lookback_window, vol_filter_window, volatility_threshold)
        self.assertIsInstance(signal, pd.Series)
        self.assertTrue(pd.api.types.is_bool_dtype(signal.dtype))
        self.assertEqual(len(signal), len(close))

        # --- Test 2: Specific scenario - Volatility Expansion after Compression ---
        num_rows = 100
        dates = pd.date_range(start='2023-01-01', periods=num_rows, freq='D')
        
        # Stable period (0-59): Minimal oscillation
        stable_prices = np.array([100.0 if i % 2 == 0 else 100.1 for i in range(60)])
        
        # Volatile period (60-99): Increasing oscillation amplitude
        volatile_prices = []
        last_stable_price = stable_prices[-1]
        amplitude = 1.0
        for i in range(40):
            if i > 0 and i % 10 == 0:
                amplitude += 1.0 # Increase amplitude every 10 days
            price = last_stable_price + (amplitude * (1 if i % 2 == 0 else -1))
            volatile_prices.append(price)
        
        prices = np.concatenate([stable_prices, np.array(volatile_prices)])
        close_specific = pd.Series(prices, index=dates)

        # Parameters for test
        lookback_window_s = 10
        vol_filter_window_s = 20
        volatility_threshold_s = 0.8 # Revert back from 0.1 - low vol might not be THAT low

        signal_specific = create_volatility_regime_indicator(
            close_specific, lookback_window_s, vol_filter_window_s, volatility_threshold_s
        )

        # --- Debugging Prints --- #
        try:
            # Calculate intermediate values needed for the signal
            returns_specific = close_specific.pct_change()
            vol_specific = returns_specific.vbt.rolling_std(window=lookback_window_s)
            vol_ma_specific = vol_specific.vbt.rolling_mean(window=vol_filter_window_s)
            vol_ma_safe_specific = vol_ma_specific.replace(0, np.nan).ffill().bfill()
            vol_ratio_specific = (vol_specific / vol_ma_safe_specific).fillna(1.0)
            vol_compressed_specific = vol_ratio_specific < volatility_threshold_s
            vol_expansion_specific = vol_ratio_specific.diff().fillna(0) > 0
            vol_compressed_shifted_specific = vol_compressed_specific.shift(1).fillna(False)

            debug_df = pd.DataFrame({
                'close': close_specific,
                'vol': vol_specific,
                'vol_ma': vol_ma_specific,
                'vol_ratio': vol_ratio_specific,
                'vol_compressed': vol_compressed_specific,
                'vol_expansion': vol_expansion_specific,
                'vol_compressed_shifted': vol_compressed_shifted_specific,
                'SIGNAL': signal_specific
            })
            print("\n--- Debugging Volatility Regime Indicator (Indices 55-70) ---")
            print(debug_df.iloc[55:71])
            print("-------------------------------------------------------------")
        except Exception as debug_e:
            print(f"Error during debug printing: {debug_e}")
        # --- End Debugging Prints ---

        # Expected behavior:
        # - Signal should be False during the initial stable period (first ~60 days, minus lookbacks)
        # - Signal should become True shortly after volatility increases (around index 60 + lookbacks)

        # Check initial period is False (allowing for indicator warmup)
        # Start check after the filter window has enough data
        self.assertFalse(signal_specific.iloc[vol_filter_window_s + 1 : 60].any(),
                         "Signal should be False during the initial stable period")

        # Check if signal triggers True sometime after volatility increases
        trigger_point_actual_start = 60 # Volatility increase starts at index 60

        # Find the first True signal after the price change begins
        first_true_index = signal_specific.iloc[trigger_point_actual_start:].idxmax() if signal_specific.iloc[trigger_point_actual_start:].any() else None

        self.assertIsNotNone(first_true_index, "Signal should trigger True after volatility increases")

        # We expect the trigger to happen shortly after the increase, allowing for lookbacks
        # The trigger requires expansion AFTER compression. Compression is met in stable phase.
        # Expansion starts immediately at index 60. Trigger should be possible soon after.
        # Earliest possible trigger index is vol_filter_window + 1 (due to diff/shift)
        # Check if the first True is within a reasonable range after the price change
        expected_trigger_window_start = trigger_point_actual_start + 1 # Allow one day for diff calc
        expected_trigger_window_end = trigger_point_actual_start + lookback_window_s + 5 # Allow some lag for MA

        # Get the integer location of the first True index
        first_true_loc = signal_specific.index.get_loc(first_true_index)
        self.assertTrue(expected_trigger_window_start <= first_true_loc <= expected_trigger_window_end,
                        f"Signal trigger at index {first_true_loc} is outside expected window [{expected_trigger_window_start}, {expected_trigger_window_end}]")

    def test_create_consolidation_breakout_indicator(self):
        """Test the consolidation breakout indicator function."""
        # --- Test 1: Basic output check (already exists) ---
        high = self.test_data['high']
        low = self.test_data['low']
        close = self.test_data['close']
        lookback_window = 20
        breakout_up, breakout_down = create_consolidation_breakout_indicator(high, low, close, lookback_window)
        self.assertIsInstance(breakout_up, pd.Series)
        self.assertTrue(pd.api.types.is_bool_dtype(breakout_up.dtype))
        self.assertEqual(len(breakout_up), len(close))
        self.assertIsInstance(breakout_down, pd.Series)
        self.assertTrue(pd.api.types.is_bool_dtype(breakout_down.dtype))
        self.assertEqual(len(breakout_down), len(close))

        # --- Test 2: Specific Scenario - Breakout Up ---
        num_rows = 50
        dates_up = pd.date_range(start='2023-01-01', periods=num_rows, freq='D')
        # Wider range (0-19), then Tight consolidation (20-39), then breakout (40+)
        prices_close_up = np.concatenate([
            np.linspace(99, 102, 20),  # Wider range initially
            np.linspace(100, 101, 20), # Tight range consolidation
            np.array([105, 106, 107, 108, 109, 110, 111, 112, 113, 114]) # Breakout up
        ])
        prices_high_up = np.concatenate([
            prices_close_up[:20] * 1.02, # Wider high range
            np.full(20, 101.0),         # Tighter Consolidation high (was 101.5)
            prices_close_up[40:] * 1.01  # Breakout higher highs
        ])
        prices_low_up = np.concatenate([
            prices_close_up[:20] * 0.98, # Wider low range
            np.full(20, 100.0),         # Tighter Consolidation low (was 99.5)
            prices_close_up[40:] * 0.99   # Breakout higher lows
        ])

        close_up = pd.Series(prices_close_up, index=dates_up)
        high_up = pd.Series(prices_high_up, index=dates_up)
        low_up = pd.Series(prices_low_up, index=dates_up)

        lookback_window_s = 25 # Increased from 15 to capture earlier wider range
        breakout_up_s, breakout_down_s = create_consolidation_breakout_indicator(
            high_up, low_up, close_up, lookback_window_s
        )

        # Expected: breakout_up should trigger True at index 40 (first bar of breakout)
        # Needs index 39 to be consolidating, and index 40 close > index 39 rolling high
        expected_breakout_up_index = 40

        # Find the first index where breakout_up is True
        # Adjust slice start index based on the new lookback window
        first_true_up_index = breakout_up_s.iloc[lookback_window_s:].idxmax() if breakout_up_s.iloc[lookback_window_s:].any() else None

        self.assertIsNotNone(first_true_up_index, "Breakout Up signal did not trigger True")
        self.assertEqual(breakout_up_s.index.get_loc(first_true_up_index), expected_breakout_up_index,
                         f"Breakout Up signal expected at index {expected_breakout_up_index} but triggered at {breakout_up_s.index.get_loc(first_true_up_index)}")
        self.assertFalse(breakout_down_s.any(), "Breakout Down signal should be False during Breakout Up scenario")

        # --- Test 3: Specific Scenario - Breakout Down ---
        dates_down = pd.date_range(start='2023-03-01', periods=num_rows, freq='D')
        # Wider range (0-19), then Tight consolidation (20-39), then breakdown (40+)
        prices_close_down = np.concatenate([
            np.linspace(99, 102, 20),  # Wider range initially
            np.linspace(100, 101, 20), # Tight range consolidation (keep close same)
            np.array([95, 94, 93, 92, 91, 90, 89, 88, 87, 86]) # Breakout down
        ])
        prices_high_down = np.concatenate([
            prices_close_down[:20] * 1.02, # Wider high range
            np.full(20, 101.0),         # Tighter Consolidation high (was 101.5)
            prices_close_down[40:] * 1.01  # Breakdown lower highs
        ])
        prices_low_down = np.concatenate([
            prices_close_down[:20] * 0.98, # Wider low range
            np.full(20, 100.0),         # Tighter Consolidation low (was 99.5)
            prices_close_down[40:] * 0.99   # Breakdown lower lows
        ])

        close_down = pd.Series(prices_close_down, index=dates_down)
        high_down = pd.Series(prices_high_down, index=dates_down)
        low_down = pd.Series(prices_low_down, index=dates_down)

        # Use the same increased lookback window for the breakdown test
        breakout_up_s2, breakout_down_s2 = create_consolidation_breakout_indicator(
            high_down, low_down, close_down, lookback_window_s
        )

        # Expected: breakout_down should trigger True at index 40
        expected_breakdown_down_index = 40

        # Find the first index where breakout_down is True
        # Adjust slice start index based on the new lookback window
        first_true_down_index = breakout_down_s2.iloc[lookback_window_s:].idxmax() if breakout_down_s2.iloc[lookback_window_s:].any() else None

        self.assertIsNotNone(first_true_down_index, "Breakout Down signal did not trigger True")
        self.assertEqual(breakout_down_s2.index.get_loc(first_true_down_index), expected_breakdown_down_index,
                         f"Breakout Down signal expected at index {expected_breakdown_down_index} but triggered at {breakout_down_s2.index.get_loc(first_true_down_index)}")
        self.assertFalse(breakout_up_s2.any(), "Breakout Up signal should be False during Breakout Down scenario")

    def test_create_volume_divergence_indicator(self):
        """Test the volume divergence confirmation indicator function."""
        num_rows = 50
        dates = pd.date_range(start='2023-01-01', periods=num_rows, freq='D')
        lookback_window_s = 10

        # Create volume data: low volume, then high volume spike, then low
        volume_s = pd.Series(np.concatenate([
            np.full(25, 100.0),  # Low volume
            np.array([1000.0]), # High volume spike at index 25
            np.full(24, 100.0)   # Back to low volume
        ]), index=dates)

        # --- Case 1: Breakout Up WITH high volume --- #
        breakout_up_s1 = pd.Series(False, index=dates)
        breakout_up_s1.iloc[25] = True # Breakout occurs at the volume spike
        breakout_down_s1 = pd.Series(False, index=dates)

        vol_conf_up1, vol_conf_down1 = create_volume_divergence_indicator(
            volume_s, lookback_window_s, breakout_up_s1, breakout_down_s1
        )
        self.assertTrue(vol_conf_up1.iloc[25], "Volume should confirm breakout up at index 25")
        self.assertFalse(vol_conf_up1.iloc[:25].any(), "No confirmation before index 25 (Up)")
        self.assertFalse(vol_conf_up1.iloc[26:].any(), "No confirmation after index 25 (Up)")
        self.assertFalse(vol_conf_down1.any(), "No confirmation down when breakout is up")

        # --- Case 2: Breakout Up WITHOUT high volume --- #
        breakout_up_s2 = pd.Series(False, index=dates)
        breakout_up_s2.iloc[20] = True # Breakout occurs during low volume
        breakout_down_s2 = pd.Series(False, index=dates)

        vol_conf_up2, vol_conf_down2 = create_volume_divergence_indicator(
            volume_s, lookback_window_s, breakout_up_s2, breakout_down_s2
        )
        self.assertFalse(vol_conf_up2.any(), "Volume should NOT confirm breakout up with low volume")
        self.assertFalse(vol_conf_down2.any(), "No confirmation down")

        # --- Case 3: Breakout Down WITH high volume --- #
        breakout_up_s3 = pd.Series(False, index=dates)
        breakout_down_s3 = pd.Series(False, index=dates)
        breakout_down_s3.iloc[25] = True # Breakdown occurs at the volume spike

        vol_conf_up3, vol_conf_down3 = create_volume_divergence_indicator(
            volume_s, lookback_window_s, breakout_up_s3, breakout_down_s3
        )
        self.assertTrue(vol_conf_down3.iloc[25], "Volume should confirm breakout down at index 25")
        self.assertFalse(vol_conf_down3.iloc[:25].any(), "No confirmation before index 25 (Down)")
        self.assertFalse(vol_conf_down3.iloc[26:].any(), "No confirmation after index 25 (Down)")
        self.assertFalse(vol_conf_up3.any(), "No confirmation up when breakout is down")

        # --- Case 4: High Volume WITHOUT breakout --- #
        breakout_up_s4 = pd.Series(False, index=dates)
        breakout_down_s4 = pd.Series(False, index=dates)

        vol_conf_up4, vol_conf_down4 = create_volume_divergence_indicator(
            volume_s, lookback_window_s, breakout_up_s4, breakout_down_s4
        )
        self.assertFalse(vol_conf_up4.any(), "Volume should NOT confirm if there is no breakout up signal")
        self.assertFalse(vol_conf_down4.any(), "Volume should NOT confirm if there is no breakout down signal")

    def test_create_market_microstructure_indicator(self):
        """Test the market microstructure (candle shadow) indicator function."""
        num_rows = 5
        dates = pd.date_range(start='2023-01-01', periods=num_rows, freq='D')

        # Test Data Setup:
        # Index 0: Neutral (balanced shadows)
        # Index 1: Strong Buying Pressure (Hammer)
        # Index 2: Strong Selling Pressure (Shooting Star)
        # Index 3: Neutral (Large body, small shadows)
        # Index 4: Edge case (Zero range - should not cause error)

        open_s = pd.Series([102, 101, 109, 100, 100], index=dates)
        high_s = pd.Series([103, 102, 110, 102, 100], index=dates)
        low_s =  pd.Series([ 97,  95,  98,  98, 100], index=dates)
        close_s =pd.Series([ 98, 101.5,99, 101.5,100], index=dates)
        # H-L:             [  6,   7,  12,   4,   0]
        # Upper Shadow:    [  1, 0.5,   1, 0.5,   0] (H - max(O,C))
        # Lower Shadow:    [  1,   0,   1,   0,   0] (min(O,C) - L)
        # Shadow Ratio:    [  0,-0.07,  0, 0.125, 0] ((Upper - Lower) / (H-L))
        # Buying Pressure: [ F,   F,   F,   F,   F]
        # Selling Pressure:[ F,   F,   F,   F,   F]

        # Recalculate based on logic for specific candles:
        # Index 1 (Hammer): H=102, L=95, O=101, C=101.5. H-L=7. Upper=H-C=0.5. Lower=O-L=6. Ratio=(0.5-6)/7 = -5.5/7 = -0.78 -> Buying Pressure=True
        # Index 2 (Shooting Star): H=110, L=98, O=109, C=99. H-L=12. Upper=H-O=1. Lower=C-L=1. Ratio=(1-1)/12 = 0 -> Neither
        # Let's adjust Index 2 to be a better shooting star: O=99, C=98.5
        # Index 2 (Shooting Star): H=110, L=98, O=99, C=98.5. H-L=12. Upper=H-O=11. Lower=C-L=0.5. Ratio=(11-0.5)/12 = 10.5/12 = 0.875 -> Selling Pressure=True

        open_s_adj = pd.Series([102, 101,  99, 100, 100], index=dates)
        high_s_adj = pd.Series([103, 102, 110, 102, 100], index=dates)
        low_s_adj =  pd.Series([ 97,  95,  98,  98, 100], index=dates)
        close_s_adj =pd.Series([ 98, 101.5,98.5,101.5,100], index=dates)

        buying_p, selling_p = create_market_microstructure_indicator(
            open_s_adj, high_s_adj, low_s_adj, close_s_adj
        )

        # --- Assertions --- #
        # Index 0 (Neutral)
        self.assertFalse(buying_p.iloc[0], "Neutral candle should not have buying pressure")
        self.assertFalse(selling_p.iloc[0], "Neutral candle should not have selling pressure")

        # Index 1 (Hammer/Buying Pressure)
        self.assertTrue(buying_p.iloc[1], "Hammer candle should have buying pressure")
        self.assertFalse(selling_p.iloc[1], "Hammer candle should not have selling pressure")

        # Index 2 (Shooting Star/Selling Pressure)
        self.assertFalse(buying_p.iloc[2], "Shooting Star candle should not have buying pressure")
        self.assertTrue(selling_p.iloc[2], "Shooting Star candle should have selling pressure")

        # Index 3 (Large Body)
        self.assertFalse(buying_p.iloc[3], "Large body candle should not have buying pressure")
        self.assertFalse(selling_p.iloc[3], "Large body candle should not have selling pressure")

        # Index 4 (Zero Range)
        self.assertFalse(buying_p.iloc[4], "Zero range candle should not have buying pressure")
        self.assertFalse(selling_p.iloc[4], "Zero range candle should not have selling pressure")

    def test_calculate_target_percent(self):
        """Test the calculate_target_percent method."""
        strategy = EdgeMultiFactorStrategy()
        target_pct = strategy.calculate_target_percent(self.test_data)
        self.assertIsInstance(target_pct, pd.Series)
        self.assertTrue(pd.api.types.is_float_dtype(target_pct.dtype))
        self.assertEqual(len(target_pct), len(self.test_data))
        self.assertFalse(target_pct.isna().any(), "Target percent should not contain NaNs")
        self.assertTrue((target_pct >= 0).all(), "Target percent should be non-negative")
        # Check if values are capped (default max is 0.25)
        self.assertTrue((target_pct <= 0.25).all(), "Target percent should be capped")

if __name__ == '__main__':
    unittest.main() 