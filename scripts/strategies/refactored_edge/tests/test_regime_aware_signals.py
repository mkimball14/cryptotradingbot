"""
Test script for regime-aware signal generation.

This test demonstrates how the signals_integration module adapts signal generation
parameters based on detected market regimes (trending vs. ranging).
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import sys

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from scripts.strategies.refactored_edge import indicators
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.config import EdgeConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_synthetic_regime_data(periods=300):
    """
    Create synthetic price data with clear trending and ranging regimes.
    
    Returns:
        tuple: (data, indicators_df, config, regime_annotations)
    """
    dates = pd.date_range(start="2023-01-01", periods=periods, freq="1h")
    
    # Create price data with alternating regimes
    # First 100 periods: trending up (0-99)
    # Next 100 periods: ranging (100-199)
    # Last 100 periods: trending down (200-299)
    
    close = []
    # Trending up
    trend_up_base = 100
    for i in range(100):
        # Strong uptrend with some noise
        close.append(trend_up_base + i * 0.5 + np.random.normal(0, 0.2))
    
    # Ranging
    range_base = close[-1]  # Continue from last price
    for i in range(100):
        # Oscillating price in a channel
        close.append(range_base + 5 * np.sin(i / 10) + np.random.normal(0, 0.3))
    
    # Trending down
    trend_down_base = close[-1]  # Continue from last price
    for i in range(100):
        # Strong downtrend with some noise
        close.append(trend_down_base - i * 0.4 + np.random.normal(0, 0.2))
    
    # Create Series with date index
    close_series = pd.Series(data=close, index=dates)
    
    # Create DataFrame with OHLC
    data = pd.DataFrame({
        'open': close_series * 0.998,
        'high': close_series * 1.005,
        'low': close_series * 0.995,
        'close': close_series
    })
    
    # Create config with default parameters
    config = EdgeConfig()
    
    # Add indicators to data
    indicators_df = indicators.add_indicators(data, config)
    
    # Create regime annotations for plotting
    regime_annotations = {
        'trending_up': (dates[0], dates[99]),
        'ranging': (dates[100], dates[199]),
        'trending_down': (dates[200], dates[299])
    }
    
    return data, indicators_df, config, regime_annotations


def test_regime_aware_signals():
    """
    Test signal generation with regime-aware parameter adaptation.
    
    Generates signals using both standard parameters and regime-adjusted parameters,
    then compares the results to verify adaptation is working as expected.
    
    Returns:
        tuple: (close, standard_signals, regime_signals, regime_annotations)
    """
    # Create sample data
    data, indicators_df, config, regime_annotations = create_synthetic_regime_data()
    
    # Extract necessary series
    close = data['close']
    rsi = indicators_df['rsi']
    bb_upper = indicators_df['bb_upper']
    bb_lower = indicators_df['bb_lower']
    trend_ma = indicators_df['trend_ma']
    price_in_demand_zone = indicators_df.get('demand_zone', pd.Series(False, index=close.index))
    price_in_supply_zone = indicators_df.get('supply_zone', pd.Series(False, index=close.index))
    
    # Base parameters
    base_params = {
        'rsi_lower_threshold': 30,
        'rsi_upper_threshold': 70,
        'use_zones': True,
        'trend_strict': True,
        'min_hold_period': 2,
        'trend_threshold_pct': 0.01,
        'zone_influence': 0.5,
        'signal_strictness': SignalStrictness.BALANCED
    }
    
    # Standard signals - no regime adaptation
    standard_params = base_params.copy()
    standard_params['use_regime_filter'] = False
    
    standard_long, standard_long_exit, standard_short, standard_short_exit = generate_signals(
        close=close,
        rsi=rsi,
        bb_upper=bb_upper,
        bb_lower=bb_lower,
        trend_ma=trend_ma,
        price_in_demand_zone=price_in_demand_zone,
        price_in_supply_zone=price_in_supply_zone,
        params=standard_params
    )
    
    # === Regime-aware signals with manually specified regimes ===
    
    # First 100 periods: trending up
    trending_up_regime = {
        'predominant_regime': 'trending',
        'trending_pct': 80.0,
        'ranging_pct': 20.0
    }
    
    # Next 100 periods: ranging
    ranging_regime = {
        'predominant_regime': 'ranging',
        'trending_pct': 20.0,
        'ranging_pct': 80.0
    }
    
    # Last 100 periods: trending down
    trending_down_regime = {
        'predominant_regime': 'trending',
        'trending_pct': 90.0,
        'ranging_pct': 10.0
    }
    
    # Initialize regime-aware signal series
    regime_long = pd.Series(False, index=close.index)
    regime_short = pd.Series(False, index=close.index)
    
    # Generate signals for trending up segment
    trending_up_params = base_params.copy()
    trending_up_params['use_regime_filter'] = True
    trending_up_params['_regime_info'] = trending_up_regime
    
    tu_long, _, tu_short, _ = generate_signals(
        close=close.iloc[0:100],
        rsi=rsi.iloc[0:100],
        bb_upper=bb_upper.iloc[0:100],
        bb_lower=bb_lower.iloc[0:100],
        trend_ma=trend_ma.iloc[0:100],
        price_in_demand_zone=price_in_demand_zone.iloc[0:100],
        price_in_supply_zone=price_in_supply_zone.iloc[0:100],
        params=trending_up_params
    )
    
    # Generate signals for ranging segment
    ranging_params = base_params.copy()
    ranging_params['use_regime_filter'] = True
    ranging_params['_regime_info'] = ranging_regime
    
    r_long, _, r_short, _ = generate_signals(
        close=close.iloc[100:200],
        rsi=rsi.iloc[100:200],
        bb_upper=bb_upper.iloc[100:200],
        bb_lower=bb_lower.iloc[100:200],
        trend_ma=trend_ma.iloc[100:200],
        price_in_demand_zone=price_in_demand_zone.iloc[100:200],
        price_in_supply_zone=price_in_supply_zone.iloc[100:200],
        params=ranging_params
    )
    
    # Generate signals for trending down segment
    trending_down_params = base_params.copy()
    trending_down_params['use_regime_filter'] = True
    trending_down_params['_regime_info'] = trending_down_regime
    
    td_long, _, td_short, _ = generate_signals(
        close=close.iloc[200:300],
        rsi=rsi.iloc[200:300],
        bb_upper=bb_upper.iloc[200:300],
        bb_lower=bb_lower.iloc[200:300],
        trend_ma=trend_ma.iloc[200:300],
        price_in_demand_zone=price_in_demand_zone.iloc[200:300],
        price_in_supply_zone=price_in_supply_zone.iloc[200:300],
        params=trending_down_params
    )
    
    # Combine segment signals
    regime_long.iloc[0:100] = tu_long
    regime_long.iloc[100:200] = r_long
    regime_long.iloc[200:300] = td_long
    
    regime_short.iloc[0:100] = tu_short
    regime_short.iloc[100:200] = r_short
    regime_short.iloc[200:300] = td_short
    
    # Count signals by segment
    def count_signals_by_segment(long_signals, short_signals):
        return {
            'trending_up': long_signals.iloc[0:100].sum() + short_signals.iloc[0:100].sum(),
            'ranging': long_signals.iloc[100:200].sum() + short_signals.iloc[100:200].sum(),
            'trending_down': long_signals.iloc[200:300].sum() + short_signals.iloc[200:300].sum(),
            'total': long_signals.sum() + short_signals.sum()
        }
    
    standard_counts = count_signals_by_segment(standard_long, standard_short)
    regime_counts = count_signals_by_segment(regime_long, regime_short)
    
    # Log signal counts
    logger.info("Standard signal counts by segment:")
    for segment, count in standard_counts.items():
        logger.info(f"  {segment}: {count}")
    
    logger.info("Regime-aware signal counts by segment:")
    for segment, count in regime_counts.items():
        logger.info(f"  {segment}: {count}")
    
    # Verify regime adaptation effects
    # We expect:
    # 1. More signals in ranging segment with regime adaptation
    # 2. Potentially fewer signals in trending segments with regime adaptation
    # 3. Different signal distribution overall
    
    ranging_ratio = regime_counts['ranging'] / max(1, standard_counts['ranging'])
    logger.info(f"Ranging segment signal ratio (regime/standard): {ranging_ratio:.2f}")
    
    trending_up_ratio = regime_counts['trending_up'] / max(1, standard_counts['trending_up'])
    logger.info(f"Trending Up segment signal ratio (regime/standard): {trending_up_ratio:.2f}")
    
    trending_down_ratio = regime_counts['trending_down'] / max(1, standard_counts['trending_down'])
    logger.info(f"Trending Down segment signal ratio (regime/standard): {trending_down_ratio:.2f}")
    
    # Verify the primary expected adaptation effect:
    # In ranging markets, we expect MORE signals with regime adaptation (looser constraints)
    assert regime_counts['ranging'] >= standard_counts['ranging'], \
        "Regime adaptation should allow more signals in ranging markets"
    
    # Return data for plotting
    return close, {
        'Standard': (standard_long, standard_short),
        'Regime-Aware': (regime_long, regime_short)
    }, regime_annotations


def plot_regime_signals(close, signal_dict, regime_annotations, output_dir=None):
    """
    Plot standard vs. regime-aware signals with background shading for regimes.
    
    Args:
        close: Series of closing prices
        signal_dict: Dictionary of signal tuples (long_entries, short_entries)
        regime_annotations: Dictionary of regime intervals {name: (start_date, end_date)}
        output_dir: Directory to save plot (default: 'data/regime_comparison')
    """
    if output_dir is None:
        output_dir = Path('data/regime_comparison')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Plot price
    ax.plot(close.index, close.values, label='Price', color='black', alpha=0.7, linewidth=1.5)
    
    # Add background shading for regimes
    colors = {
        'trending_up': 'lightblue',
        'ranging': 'lightyellow',
        'trending_down': 'lightgreen'
    }
    
    ylim = ax.get_ylim()
    ax.set_ylim(ylim)  # Keep the current y-limits
    
    # Add background patches
    for regime, (start_date, end_date) in regime_annotations.items():
        ax.axvspan(start_date, end_date, alpha=0.2, color=colors[regime], label=f"{regime.replace('_', ' ').title()} Regime")
    
    # Define colors and markers for signals
    signal_colors = {
        'Standard': 'blue',
        'Regime-Aware': 'red'
    }
    
    # Plot signals for each method
    for name, (long_entries, short_entries) in signal_dict.items():
        long_indices = close.index[long_entries]
        short_indices = close.index[short_entries]
        
        # Plot long entries (triangle up)
        ax.scatter(long_indices, close.loc[long_indices], 
                   marker='^', s=120, color=signal_colors[name], alpha=0.8,
                   label=f'{name} Long ({len(long_indices)})')
        
        # Plot short entries (triangle down)
        ax.scatter(short_indices, close.loc[short_indices], 
                   marker='v', s=120, color=signal_colors[name], alpha=0.8,
                   label=f'{name} Short ({len(short_indices)})')
    
    # Calculate signal counts by regime for annotation
    def count_signals_by_regime(signal_dict):
        result = {}
        for name, (long_entries, short_entries) in signal_dict.items():
            counts = {}
            for regime, (start_date, end_date) in regime_annotations.items():
                start_idx = close.index.get_loc(start_date)
                end_idx = close.index.get_loc(end_date)
                
                long_count = long_entries.iloc[start_idx:end_idx+1].sum()
                short_count = short_entries.iloc[start_idx:end_idx+1].sum()
                total_count = long_count + short_count
                
                counts[regime] = total_count
            result[name] = counts
        return result
    
    # Get signal counts by regime
    regime_signal_counts = count_signals_by_regime(signal_dict)
    
    # Add text annotation for signal counts
    y_pos = ax.get_ylim()[1] * 0.97
    x_text_pos = {
        'trending_up': close.index[30],
        'ranging': close.index[150],
        'trending_down': close.index[250]
    }
    
    for regime, x_pos in x_text_pos.items():
        standard_count = regime_signal_counts['Standard'][regime]
        regime_count = regime_signal_counts['Regime-Aware'][regime]
        
        # Format ratio differently based on whether standard_count is 0
        if standard_count > 0:
            ratio = regime_count / standard_count
            ratio_text = f"{ratio:.2f}x"
        else:
            ratio_text = "N/A"
        
        text = f"Standard: {standard_count}\nRegime-Aware: {regime_count}\nRatio: {ratio_text}"
        ax.text(x_pos, y_pos, text, bbox=dict(facecolor='white', alpha=0.7), ha='center')
    
    # Add labels and legend
    ax.set_title('Comparison of Standard vs. Regime-Aware Signal Generation', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Create legend with two columns
    handles, labels = ax.get_legend_handles_labels()
    # Reorder to group regime backgrounds together and signals together
    regime_idx = [i for i, label in enumerate(labels) if "Regime" in label]
    signal_idx = [i for i, label in enumerate(labels) if "Regime" not in label]
    
    # Combine in preferred order: regimes first, then signals
    ordered_idx = regime_idx + signal_idx
    ax.legend([handles[i] for i in ordered_idx], [labels[i] for i in ordered_idx], 
              loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'regime_aware_signals_comparison.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Plot saved to {output_path}")


if __name__ == "__main__":
    # Run test and plot results
    close, signal_dict, regime_annotations = test_regime_aware_signals()
    plot_regime_signals(close, signal_dict, regime_annotations)
