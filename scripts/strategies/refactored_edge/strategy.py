import vectorbtpro as vbt
import pandas as pd
import numpy as np

# Import from our refactored modules
from . import indicators as ind
from . import signals as sig
from . import regime as rg

# ==============================================================================
# Refactored Edge Strategy Class
# ==============================================================================

class RefactoredEdgeStrategy:
    """Encapsulates the logic for the refactored Edge Multi-Factor strategy.

    This class takes market data and parameters, calculates indicators,
    determines market regimes, generates signals, combines them, and returns
    final entry/exit signals ready for backtesting with vbt.Portfolio.
    """
    DEFAULT_PARAMS = {
        # Add other parameters as needed (e.g., for custom indicators, regime filters)
        'rsi_window': 14,
        'rsi_entry': 30,
        'rsi_exit': 70, # Also used for short entry
        'bb_window': 20,
        'bb_std_dev': 2.0,
        'adx_window': 14,
        'adx_threshold': 25,
        'macd_fast_window': 12,
        'macd_slow_window': 26,
        'macd_signal_window': 9,
        # Weights for signal combination
        'rsi_weight': 1.0,
        'bb_weight': 1.0,
        'macd_weight': 1.0,
        # Combined signal threshold
        'signal_threshold': 0.1, # Lowered threshold
        # Stop Loss / Take Profit (used by Portfolio, not Strategy directly)
        'stop_loss_pct': 0.03,
        'take_profit_pct': 0.06,
    }

    def __init__(self, data: pd.DataFrame, params: dict):
        """Initialize the strategy with data and parameters.

        Args:
            data (pd.DataFrame): DataFrame with OHLCV columns.
            params (dict): Dictionary containing strategy parameters (e.g., window sizes, thresholds).
        """
        if not isinstance(data, pd.DataFrame) or not all(col in data.columns for col in ['open', 'high', 'low', 'close', 'volume']):
            raise ValueError("Data must be a pandas DataFrame with OHLCV columns")
        if not isinstance(params, dict):
            raise ValueError("Params must be a dictionary")

        self.data = data
        self.params = {**self.DEFAULT_PARAMS, **params}  # Merge default and user params
        self.close = data['close']
        self.high = data['high']
        self.low = data['low']

        # --- Calculated Attributes (Indicators, Signals, etc.) ---
        self.rsi = None
        self.bb_upper = None
        self.bb_middle = None
        self.bb_lower = None
        self.adx = None
        self.is_trending = None
        self.macd_line = None
        self.signal_line = None
        self.hist = None
        self.entries = None
        self.exits = None
        # Add placeholders for other indicators/signals as they are implemented

    def run(self, **kwargs) -> tuple[pd.Series, pd.Series]:
        """Runs the full strategy calculation pipeline.

        Calculates indicators, determines regime, generates and combines signals.

        Returns:
            tuple[pd.Series, pd.Series]: Final boolean entry and exit signals.
        """
        self._calculate_indicators()
        self._determine_regime()
        return self._generate_signals()

    def _calculate_indicators(self):
        """Calculate all required indicators.
        Uses indicator factories/functions defined in indicators.py
        """
        print("Calculating indicators...")
        # RSI
        self.rsi = ind.RSI.run(
            self.close,
            timeperiod=self.params.get('rsi_window', 14) # Use timeperiod for TA-Lib
        ).rsi

        # Bollinger Bands
        bb_std = self.params.get('bb_std_dev', 2.0)
        bbands_output = ind.BBANDS.run(
            self.close,
            timeperiod=self.params.get('bb_window', 20), # Use timeperiod
            nbdevup=bb_std,                             # Use nbdevup
            nbdevdn=bb_std                              # Use nbdevdn
        )
        # Access using TA-Lib output names
        self.bb_upper = bbands_output.upperband
        self.bb_middle = bbands_output.middleband
        self.bb_lower = bbands_output.lowerband

        # ADX
        self.adx = ind.ADX.run(
            self.high,
            self.low,
            self.close,
            timeperiod=self.params.get('adx_window', 14) # Use timeperiod for TA-Lib
        ).adx

        # MACD
        macd_output = ind.MACD.run(
            self.close,
            fastperiod=self.params.get('macd_fast_window', 12),
            slowperiod=self.params.get('macd_slow_window', 26),
            signalperiod=self.params.get('macd_signal_window', 9)
        )
        self.macd_line = macd_output.macd
        self.signal_line = macd_output.macdsignal # Use macdsignal
        self.hist = macd_output.macdhist      # Use macdhist

        # TODO: Calculate other indicators (ATR, SMA, Custom, etc.)
        # Remember to use 'timeperiod' for window-based TA-Lib indicators
        print("Indicators calculated.")

    def _determine_regime(self):
        """Determine the market regime based on ADX."""
        regime_series = rg.determine_market_regime(self.adx, self.params.get('adx_threshold', 25))
        self.is_trending = (regime_series == 'trending') # Convert to boolean
        trending_pct = self.is_trending.mean() * 100
        print(f"Regime determined: {trending_pct:.2f}% trending")

    def _generate_signals(self):
        """Generate entry and exit signals based on simple confluence of indicators."""
        print("Generating simple confluence signals...")
        
        # --- Generate individual factor signals (long/short entry/exit) ---
        rsi_le, rsi_lx, rsi_se, rsi_sx = sig.generate_rsi_signals(
            rsi=self.rsi,
            entry_threshold=self.params.get('rsi_entry', 30),
            exit_threshold=self.params.get('rsi_exit', 70)
        )
        
        bb_le, bb_lx, bb_se, bb_sx = sig.generate_bbands_signals(
            close=self.close, 
            lower_band=self.bb_lower, 
            upper_band=self.bb_upper
        )
        
        macd_le, macd_lx, macd_se, macd_sx = sig.generate_macd_signals(
            macd_line=self.macd_line,
            signal_line=self.signal_line
        )
        
        # --- Simple Confluence Logic --- 
        # Long Entry: Require both RSI and MACD entry signals to be True
        # We ignore BBands signal for now for simplicity
        self.entries = rsi_le & macd_le 
        
        # Long Exit: Use MACD exit signal (MACD crosses below signal line)
        # Portfolio SL/TP will handle price-based exits
        self.exits = macd_lx
        
        # TODO: Implement Short Signal Generation if needed
        # short_entries = combined_signal.vbt.crossed_below(-signal_threshold)
        # short_exits = combined_signal.vbt.crossed_above(signal_threshold)
        
        print(f"Simple confluence signals generated.")
        print(f"Entries: {self.entries.sum()}, Exits: {self.exits.sum()}")
        return self.entries, self.exits

# --- Example Usage (for testing) ---
if __name__ == '__main__':
    # This block is for basic testing of the class itself.
    # Actual backtesting should use backtest_runner.py

    # Create dummy data
    dates = pd.date_range('2023-01-01', periods=500, freq='h')
    price = 100 + np.random.randn(500).cumsum()
    dummy_data = pd.DataFrame({
        'open': price - np.random.rand(500) * 0.1,
        'high': price + np.random.rand(500) * 0.1,
        'low': price - np.random.rand(500) * 0.1,
        'close': price,
        'volume': np.random.rand(500) * 100 + 10
    }, index=dates)

    # Define dummy parameters
    dummy_params = {
        'rsi_window': 14,
        'rsi_entry': 30,
        'rsi_exit': 70,
        'bb_window': 20,
        'bb_std_dev': 2.0,
        'adx_window': 14,
        'adx_threshold': 25,
        'macd_fast_window': 12,
        'macd_slow_window': 26,
        'macd_signal_window': 9,
        'rsi_weight': 1.0,
        'bb_weight': 1.0,
        'macd_weight': 1.0,
        'signal_threshold': 0.1,
    }

    print("--- Testing RefactoredEdgeStrategy --- ")
    try:
        strategy = RefactoredEdgeStrategy(data=dummy_data, params=dummy_params)
        entries, exits = strategy.run()

        print("\n--- Strategy Object Attributes --- ")
        print(f"RSI (first 5):\n{strategy.rsi.head()}")
        print(f"\nBB Lower (first 5):\n{strategy.bb_lower.head()}")
        print(f"\nADX (first 5):\n{strategy.adx.head()}")
        print(f"\nMACD Line (first 5):\n{strategy.macd_line.head()}")
        print(f"\nSignal Line (first 5):\n{strategy.signal_line.head()}")
        print(f"\nIs Trending (counts):\n{strategy.is_trending.value_counts()}")
        print(f"\nFinal Entries (sum): {entries.sum()}")
        print(f"Final Exits (sum): {exits.sum()}")

        # Example: Create a portfolio (using default settings for simplicity here)
        # In a real runner, use parameters from config/params files
        if entries.sum() > 0:
            pf = vbt.Portfolio.from_signals(strategy.close, entries, exits, freq='h')
            print("\n--- Basic Portfolio Stats (Dummy Data) ---")
            print(pf.stats())
        else:
            print("\nNo entries generated, skipping portfolio creation.")

    except Exception as e:
        print(f"\nError during test run: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- Test Complete --- ")
