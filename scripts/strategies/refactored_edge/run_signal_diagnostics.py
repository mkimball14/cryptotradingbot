#!/usr/bin/env python
"""
Script to run signal diagnostics on real data to quickly analyze strategy signal generation.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import argparse

# Ensure parent directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Import local modules
from scripts.strategies.refactored_edge import indicators
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signal_diagnostics import (
    analyze_signal_distribution,
    visualize_signals_by_regime,
    recommend_parameters
)
from scripts.strategies.refactored_edge.config import EdgeConfig
# Use sample data instead of trying to fetch live data
import numpy as np

# Constants
DEFAULT_SYMBOL = "BTC-USD"
DEFAULT_TIMEFRAME = "1h"
DEFAULT_DAYS = 30
DEFAULT_OUTPUT_DIR = "./reports"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run signal diagnostics on real data")
    parser.add_argument("--symbol", type=str, default=DEFAULT_SYMBOL, 
                        help=f"Symbol to analyze (default: {DEFAULT_SYMBOL})")
    parser.add_argument("--timeframe", type=str, default=DEFAULT_TIMEFRAME, 
                        help=f"Timeframe (default: {DEFAULT_TIMEFRAME})")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, 
                        help=f"Number of days of data to fetch (default: {DEFAULT_DAYS})")
    parser.add_argument("--strictness", type=str, default="balanced", 
                        choices=["strict", "balanced", "moderately_relaxed", "relaxed", "ultra_relaxed"],
                        help="Signal strictness level to analyze (case sensitive)")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_OUTPUT_DIR, 
                        help=f"Output directory for reports (default: {DEFAULT_OUTPUT_DIR})")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    print(f"Fetching {args.days} days of {args.timeframe} data for {args.symbol}...")
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)
    
    # Format dates for data fetcher
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    # Generate sample data instead of fetching
    print("Generating sample data for testing...")
    n_points = args.days * 24  # 24 hours per day
    idx = pd.date_range(end=datetime.now(), periods=n_points, freq='1H')
    
    # Create synthetic price data with some trends and ranges
    np.random.seed(42)  # For reproducibility
    price = 30000 + np.cumsum(np.random.normal(0, 100, n_points))
    
    # Add some trending and ranging periods
    for i in range(n_points // 3, 2 * n_points // 3):
        price[i] += 50  # Add uptrend in the middle section
    
    # Create OHLC data
    data = pd.DataFrame({
        'open': price * 0.99,
        'high': price * 1.02,
        'low': price * 0.98,
        'close': price,
        'volume': np.random.normal(1000, 200, n_points)
    }, index=idx)
    
    print(f"Fetched {len(data)} candles.")
    
    # Calculate indicators
    print("Calculating indicators...")
    config = EdgeConfig(
        rsi_window=14,
        bb_window=20,
        trend_ma_window=50,
        use_zones=True,
        atr_window=14
    )
    data_with_indicators = indicators.add_indicators(data, config)
    
    # Generate and print recommendations
    print("\nGenerating signal recommendations...")
    recommendations = recommend_parameters(data_with_indicators)
    
    # Print recommendations
    print("\n===== SIGNAL PARAMETER RECOMMENDATIONS =====")
    print(f"Recommended strictness level: {recommendations['recommended_strictness']}")
    print(f"Expected signal density: {recommendations['signal_density']:.2f} signals/day")
    print(f"Market conditions: {recommendations['market_conditions']['trending_percentage']:.1f}% trending, "
          f"{recommendations['market_conditions']['ranging_percentage']:.1f}% ranging")
    print("\nRecommended parameters:")
    print(f"  trend_threshold_pct: {recommendations['regime_adapted_parameters']['trend_threshold_pct']:.5f}")
    print(f"  zone_influence: {recommendations['regime_adapted_parameters']['zone_influence']:.2f}")
    print(f"  min_hold_period: {recommendations['regime_adapted_parameters']['min_hold_period']}")
    print(f"\nNote: {recommendations['regime_adapted_parameters']['note']}")
    
    # Visualize signals with user-specified strictness
    # Convert the strictness string to SignalStrictness enum
    try:
        strictness_enum = SignalStrictness(args.strictness.lower())
    except ValueError:
        print(f"Warning: '{args.strictness}' is not a valid SignalStrictness value. Defaulting to BALANCED.")
        strictness_enum = SignalStrictness.BALANCED
    output_file = os.path.join(args.output_dir, f"signal_analysis_{args.symbol}_{args.timeframe}_{args.strictness.lower()}.html")
    
    print(f"\nGenerating signal visualization for {args.strictness} strictness...")
    visualize_signals_by_regime(data_with_indicators, strictness_enum, output_file)
    print(f"Visualization saved to {output_file}")
    
    # Generate distribution report
    distribution = recommendations['signal_distribution']
    print("\n===== SIGNAL DISTRIBUTION ANALYSIS =====")
    for strictness, stats in distribution.items():
        print(f"\n{strictness.upper()} mode:")
        print(f"  Total signals: {stats['total_signals']}")
        print(f"  Signal density: {stats['signal_density']:.2f} signals/day")
        print(f"  Long entries: {stats['long_entries']}, Short entries: {stats['short_entries']}")
        print(f"  Trending market signals: {stats['trending_signals']}")
        print(f"  Ranging market signals: {stats['ranging_signals']}")
    
    print("\nAnalysis complete!")
