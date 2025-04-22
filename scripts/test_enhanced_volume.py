#!/usr/bin/env python
"""
Test script for enhanced volume detection in the EdgeMultiFactorStrategy.
This script tests the strategy with the 'enhanced_volume' parameter profile,
including the market regime-aware volume detection.
"""

import sys
import os
import logging
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import vectorbtpro as vbt

# --- Basic Setup ---
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Import modules ---
try:
    from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
    from data.data_fetcher import fetch_historical_data, get_vbt_freq_str
    from scripts.strategies.param_loader import load_strategy_params
except ImportError as e:
    logger.error(f"Error importing required modules: {e}")
    sys.exit(1)

# --- Test Configuration ---
SYMBOL = "BTC-USD"
TIMEFRAME = "1h"
LOOKBACK_DAYS_FOR_TEST = 30  # How many days of data to use for test
GRANULARITY_SECONDS = {
    "1m": 60, "5m": 300, "15m": 900, 
    "1h": 3600, "4h": 14400, "1d": 86400
}.get(TIMEFRAME, 3600)

def main():
    """Main test function."""
    try:
        # Calculate date range for test
        end_date = datetime.now()
        start_date = end_date - timedelta(days=LOOKBACK_DAYS_FOR_TEST)
        
        logger.info(f"Testing market regime-aware volume detection for {SYMBOL} from {start_date.date()} to {end_date.date()} on {TIMEFRAME} timeframe")
        
        # Fetch data
        price_data = fetch_historical_data(SYMBOL, start_date.strftime('%Y-%m-%d'), 
                                          end_date.strftime('%Y-%m-%d'), GRANULARITY_SECONDS)
        
        if price_data is None or price_data.empty:
            logger.error("Failed to fetch data. Exiting.")
            return
        
        logger.info(f"Data fetched successfully. Shape: {price_data.shape}")
        
        # Load enhanced volume profile
        params = load_strategy_params("enhanced_volume")
        logger.info(f"Using enhanced_volume profile with parameters: {params}")
        
        # Initialize strategy with enhanced volume parameters
        strategy = EdgeMultiFactorStrategy(
            lookback_window=params["lookback_window"],
            vol_filter_window=params.get("vol_filter_window", 48),
            volatility_threshold=params["volatility_threshold"],
            signal_threshold=params.get("signal_threshold", 0.15),
            default_factor_weights=params.get("default_factor_weights", None),
            volume_threshold=params.get("volume_threshold", 1.1),
            volume_threshold_short=params.get("volume_threshold_short", 1.05),
            volume_roc_threshold=params.get("volume_roc_threshold", 0.1)
        )
        
        # Generate signals with regime-aware volume detection
        logger.info("Generating signals with market regime-aware volume detection...")
        long_entries, short_entries, is_trending, is_ranging = strategy.generate_signals(price_data)
        
        if long_entries.sum() + short_entries.sum() == 0:
            logger.warning("No entry signals generated.")
            return
        
        logger.info(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries.")
        
        # Backtest the strategy
        logger.info("Backtesting the strategy...")
        portfolio, metrics = strategy.backtest_signals(long_entries, data=price_data)
        
        # Display metrics
        if portfolio is not None:
            logger.info("\nBacktest Results:")
            logger.info(f"Total Return: {metrics['total_return']:.2%}")
            logger.info(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
            logger.info(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
            logger.info(f"Total Trades: {metrics['total_trades']}")
            logger.info(f"Win Rate: {metrics['win_rate']:.2%}")
            logger.info(f"Profit Factor: {metrics['profit_factor']:.2f}")
        else:
            logger.error("Backtest failed.")
        
        # Create comparison with non-regime-aware volume detection
        logger.info("Testing without market regime awareness for comparison...")
        
        # Create version of function that ignores market regimes
        # This is done by modifying the class for this test only
        original_generate_signals = strategy.generate_signals
        
        # Monkey patch to disable market regime awareness temporarily
        def generate_signals_no_regime(self, data):
            # Calculate ADX for market regime detection
            adx_period = 14
            adx = self._calculate_adx(data, adx_period)
            is_trending = (adx > 25).fillna(False)
            is_ranging = (adx < 20).fillna(False)
            
            # Store data for later use
            self._data = data.copy()
            
            # Calculate individual factor signals but don't pass regime info
            vol_signal = self._calculate_volatility_regime(data)
            breakout_up, breakout_down = self._calculate_breakouts(data)
            
            # Use volume detection WITHOUT passing regime info
            from scripts.strategies.edge_multi_factor_fixed import create_volume_divergence_indicator
            volume_confirms_up, volume_confirms_down = create_volume_divergence_indicator(
                data['volume'],
                lookback_window=self.lookback_window,
                breakout_up=breakout_up,
                breakout_down=breakout_down,
                volume_threshold=self.volume_threshold,
                volume_threshold_short=self.volume_threshold_short,
                volume_roc_threshold=self.volume_roc_threshold
                # Not passing is_trending and is_ranging
            )
            
            # Rest of signal generation
            buying_pressure, selling_pressure = self._calculate_microstructure(data)
            
            # Combine signals with weights
            long_signal, short_signal = self._combine_signals(
                vol_signal, breakout_up, breakout_down, 
                volume_confirms_up, volume_confirms_down,
                buying_pressure, selling_pressure
            )
            
            # Generate entries
            long_entries, short_entries = self._generate_entries(
                long_signal, short_signal, data, is_trending, is_ranging
            )
            
            return long_entries, short_entries, is_trending, is_ranging
        
        # Add helper methods to handle the monkey patching
        def _calculate_adx(self, data, period):
            return vbt.ADX.run(data['high'], data['low'], data['close'], window=period).adx
            
        def _calculate_volatility_regime(self, data):
            from scripts.strategies.edge_multi_factor_fixed import create_volatility_regime_indicator
            return create_volatility_regime_indicator(
                data['close'],
                lookback_window=self.lookback_window,
                vol_filter_window=self.vol_filter_window,
                volatility_threshold=self.volatility_threshold
            )
            
        def _calculate_breakouts(self, data):
            from scripts.strategies.edge_multi_factor_fixed import create_consolidation_breakout_indicator
            return create_consolidation_breakout_indicator(
                data['high'], data['low'], data['close'],
                lookback_window=self.lookback_window
            )
            
        def _calculate_microstructure(self, data):
            from scripts.strategies.edge_multi_factor_fixed import create_market_microstructure_indicator
            return create_market_microstructure_indicator(
                data['open'], data['high'], data['low'], data['close']
            )
            
        def _combine_signals(self, vol_signal, breakout_up, breakout_down, 
                           volume_confirms_up, volume_confirms_down,
                           buying_pressure, selling_pressure):
            long_signal = pd.Series(0.0, index=vol_signal.index)
            short_signal = pd.Series(0.0, index=vol_signal.index)
            
            long_signal += vol_signal.astype(float) * self.factor_weights.get('volatility_regime', 0)
            long_signal += breakout_up.astype(float) * self.factor_weights.get('consolidation_breakout', 0)
            long_signal += volume_confirms_up.astype(float) * self.factor_weights.get('volume_divergence', 0)
            long_signal += buying_pressure.astype(float) * self.factor_weights.get('market_microstructure', 0)
            
            short_signal += vol_signal.astype(float) * self.factor_weights.get('volatility_regime', 0)
            short_signal += breakout_down.astype(float) * self.factor_weights.get('consolidation_breakout', 0)
            short_signal += volume_confirms_down.astype(float) * self.factor_weights.get('volume_divergence', 0)
            short_signal += selling_pressure.astype(float) * self.factor_weights.get('market_microstructure', 0)
            
            return long_signal, short_signal
            
        def _generate_entries(self, long_signal, short_signal, data, is_trending, is_ranging):
            # Generate entries based on signal threshold
            long_entries = long_signal > self.signal_threshold
            short_entries = short_signal > self.signal_threshold
            
            # Prevent simultaneous entries
            simultaneous = long_entries & short_entries
            long_entries[simultaneous] = False
            short_entries[simultaneous] = False
            
            # Apply market regime adaptation
            trend_up = is_trending & (data['close'] > data['close'].shift(self.lookback_window))
            trend_down = is_trending & (data['close'] < data['close'].shift(self.lookback_window))
            
            long_adjusted_up = (long_signal[trend_up] > (self.signal_threshold * 0.7)).astype(bool)
            short_adjusted_up = (short_signal[trend_up] > (self.signal_threshold * 1.3)).astype(bool)
            long_adjusted_down = (long_signal[trend_down] > (self.signal_threshold * 1.3)).astype(bool)
            short_adjusted_down = (short_signal[trend_down] > (self.signal_threshold * 0.7)).astype(bool)
            
            long_entries.loc[trend_up] = long_adjusted_up
            short_entries.loc[trend_up] = short_adjusted_up
            long_entries.loc[trend_down] = long_adjusted_down
            short_entries.loc[trend_down] = short_adjusted_down
            
            return long_entries, short_entries
        
        # Add methods to the strategy instance
        strategy._calculate_adx = _calculate_adx.__get__(strategy)
        strategy._calculate_volatility_regime = _calculate_volatility_regime.__get__(strategy)
        strategy._calculate_breakouts = _calculate_breakouts.__get__(strategy)
        strategy._calculate_microstructure = _calculate_microstructure.__get__(strategy)
        strategy._combine_signals = _combine_signals.__get__(strategy)
        strategy._generate_entries = _generate_entries.__get__(strategy)
        
        # Replace the generate_signals method
        strategy.generate_signals = generate_signals_no_regime.__get__(strategy)
        
        # Generate signals without regime awareness
        no_regime_long, no_regime_short, _, _ = strategy.generate_signals(price_data)
        
        # Restore original method
        strategy.generate_signals = original_generate_signals
        
        logger.info(f"Without regime awareness: {no_regime_long.sum()} long entries and {no_regime_short.sum()} short entries")
        
        # Plot comparison
        plot_regime_comparison(price_data, 
                        long_entries, short_entries, 
                        no_regime_long, no_regime_short,
                        is_trending, is_ranging,
                        "regime_aware_volume.png")
        
        logger.info("Test completed successfully.")
    
    except Exception as e:
        logger.exception(f"Error during test: {e}")

def plot_regime_comparison(price_data, regime_long, regime_short, 
                         no_regime_long, no_regime_short,
                         is_trending, is_ranging, filename):
    """Create comparison plot between regime-aware and non-regime-aware volume detection."""
    plt.figure(figsize=(14, 12))
    
    # Plot price chart
    plt.subplot(3, 1, 1)
    plt.plot(price_data.index, price_data['close'], label='Close Price', color='blue', alpha=0.7)
    
    # Plot regime-aware signals
    plt.scatter(price_data.index[regime_long], 
                price_data.loc[regime_long, 'close'],
                color='green', marker='^', s=100, label='Regime-Aware Long')
    plt.scatter(price_data.index[regime_short], 
                price_data.loc[regime_short, 'close'],
                color='red', marker='v', s=100, label='Regime-Aware Short')
    
    # Plot non-regime-aware signals
    plt.scatter(price_data.index[no_regime_long], 
                price_data.loc[no_regime_long, 'close'],
                color='lightgreen', marker='o', s=60, label='Standard Long')
    plt.scatter(price_data.index[no_regime_short], 
                price_data.loc[no_regime_short, 'close'],
                color='lightcoral', marker='o', s=60, label='Standard Short')
    
    plt.title('Price Chart with Signal Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot volume
    plt.subplot(3, 1, 2)
    plt.bar(price_data.index, price_data['volume'], color='blue', alpha=0.5, label='Volume')
    
    # Highlight where regime-aware volume found signals
    regime_volume_points = regime_long | regime_short
    plt.scatter(price_data.index[regime_volume_points],
                price_data.loc[regime_volume_points, 'volume'],
                color='green', marker='*', s=100, label='Regime-Aware Signals')
    
    # Highlight where non-regime-aware found signals
    no_regime_volume_points = no_regime_long | no_regime_short
    plt.scatter(price_data.index[no_regime_volume_points],
                price_data.loc[no_regime_volume_points, 'volume'],
                color='red', marker='o', s=60, label='Standard Signals')
    
    plt.title('Volume with Signal Triggers')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot market regimes
    plt.subplot(3, 1, 3)
    plt.plot(price_data.index, is_trending, label='Trending', color='blue', alpha=0.7)
    plt.plot(price_data.index, is_ranging, label='Ranging', color='orange', alpha=0.7)
    
    # Highlight difference points - where regime-aware found signals but standard didn't
    regime_only = regime_volume_points & ~no_regime_volume_points
    plt.scatter(price_data.index[regime_only],
                np.ones(regime_only.sum()) * 0.5,
                color='green', marker='*', s=120, label='Regime-Only Signals')
    
    # Highlight difference points - where standard found signals but regime-aware didn't
    no_regime_only = no_regime_volume_points & ~regime_volume_points
    plt.scatter(price_data.index[no_regime_only],
                np.ones(no_regime_only.sum()) * 0.5,
                color='red', marker='o', s=80, label='Standard-Only Signals')
    
    plt.title('Market Regimes and Signal Differences')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename)
    logger.info(f"Regime comparison plot saved to {filename}")
    
    # Also create a summary plot of signal differences by regime
    create_regime_summary_plot(price_data, regime_volume_points, no_regime_volume_points, 
                              is_trending, is_ranging, f"regime_summary_{filename}")

def create_regime_summary_plot(price_data, regime_signals, no_regime_signals, 
                             is_trending, is_ranging, filename):
    """Create a summary plot showing signal distribution across market regimes."""
    # Count signals in each regime
    trending_regime_signals = (regime_signals & is_trending).sum()
    ranging_regime_signals = (regime_signals & is_ranging).sum()
    trending_std_signals = (no_regime_signals & is_trending).sum()
    ranging_std_signals = (no_regime_signals & is_ranging).sum()
    
    # Calculate total days in each regime
    total_trending = is_trending.sum()
    total_ranging = is_ranging.sum()
    
    # Create a bar chart
    plt.figure(figsize=(10, 8))
    
    # Plot raw counts
    plt.subplot(2, 1, 1)
    plt.bar(['Trending (Regime-Aware)', 'Trending (Standard)', 
            'Ranging (Regime-Aware)', 'Ranging (Standard)'],
            [trending_regime_signals, trending_std_signals, 
             ranging_regime_signals, ranging_std_signals],
            color=['darkgreen', 'lightgreen', 'darkred', 'lightcoral'])
    
    plt.title('Signal Count by Market Regime')
    plt.ylabel('Number of Signals')
    plt.grid(True, alpha=0.3)
    
    # Plot percentage of days with signals
    plt.subplot(2, 1, 2)
    plt.bar(['Trending (Regime-Aware)', 'Trending (Standard)', 
            'Ranging (Regime-Aware)', 'Ranging (Standard)'],
            [trending_regime_signals/total_trending*100 if total_trending > 0 else 0, 
             trending_std_signals/total_trending*100 if total_trending > 0 else 0, 
             ranging_regime_signals/total_ranging*100 if total_ranging > 0 else 0, 
             ranging_std_signals/total_ranging*100 if total_ranging > 0 else 0],
            color=['darkgreen', 'lightgreen', 'darkred', 'lightcoral'])
    
    plt.title('Signal Frequency (% of Days in Regime)')
    plt.ylabel('% of Days with Signals')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename)
    logger.info(f"Regime summary plot saved to {filename}")

if __name__ == "__main__":
    main() 