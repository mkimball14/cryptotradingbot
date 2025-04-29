"""
Simplified test script to demonstrate regime-aware signal generation.

This script shows how trading signals adapt to different market regimes.
"""

import sys
import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import local modules
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('simplified_regime_test')

def generate_sample_data(length=200, with_trend_change=True):
    """Generate synthetic data with trending and ranging segments."""
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=length, freq='1h')
    
    # Starting price
    price = 100.0
    
    # Initialize data
    data = {
        'close': np.zeros(length),
        'high': np.zeros(length),
        'low': np.zeros(length),
        'rsi': np.zeros(length),
        'bb_upper': np.zeros(length),
        'bb_lower': np.zeros(length),
        'trend_ma': np.zeros(length),
        'regime': ['ranging'] * length
    }
    
    # Create trend segments
    if with_trend_change:
        # First segment (ranging: 0-49)
        # Second segment (trending up: 50-99)
        # Third segment (ranging: 100-149)
        # Fourth segment (trending down: 150-199)
        for i in range(length):
            if 50 <= i < 100:
                data['regime'][i] = 'trending'
            elif 150 <= i < 200:
                data['regime'][i] = 'trending'
    
    # Generate price and indicators
    for i in range(length):
        # Price behavior depends on regime
        if data['regime'][i] == 'trending':
            if i < 100:  # Uptrend
                price += 0.1 + np.random.normal(0, 0.03)
            else:  # Downtrend
                price -= 0.1 + np.random.normal(0, 0.03)
        else:  # Ranging
            price += np.random.normal(0, 0.2)
        
        # Set price data
        data['close'][i] = price
        data['high'][i] = price * (1 + abs(np.random.normal(0, 0.005)))
        data['low'][i] = price * (1 - abs(np.random.normal(0, 0.005)))
        
        # Fake indicator data
        if data['regime'][i] == 'trending':
            if i < 100:  # Uptrend
                data['rsi'][i] = 70 + np.random.normal(0, 5)
            else:  # Downtrend
                data['rsi'][i] = 30 + np.random.normal(0, 5)
        else:  # Ranging
            data['rsi'][i] = 50 + np.random.normal(0, 10)
            
        # Moving average
        if i > 10:
            data['trend_ma'][i] = np.mean(data['close'][max(0, i-10):i])
        else:
            data['trend_ma'][i] = data['close'][i]
        
        # Bollinger bands
        data['bb_upper'][i] = data['trend_ma'][i] + 2 * np.std(data['close'][max(0, i-20):i+1])
        data['bb_lower'][i] = data['trend_ma'][i] - 2 * np.std(data['close'][max(0, i-20):i+1])
    
    # Create dataframe
    df = pd.DataFrame(data, index=dates)
    
    return df

def test_regime_aware_signals():
    """Test how signals adapt based on market regime."""
    logger.info("Starting simplified regime-aware signal test")
    
    # Generate sample data
    data = generate_sample_data(length=200)
    logger.info("Generated sample data with both trending and ranging segments")
    
    # Create regime info dicts for each regime type
    trending_regime = {
        'predominant_regime': 'trending',
        'trending_pct': 80.0,
        'ranging_pct': 20.0,
    }
    
    ranging_regime = {
        'predominant_regime': 'ranging',
        'trending_pct': 20.0,
        'ranging_pct': 80.0,
    }
    
    # Define standard parameters (non-regime-aware)
    standard_params = {
        'rsi_entry_threshold': 30,
        'rsi_exit_threshold': 70,
        'signal_strictness': 'balanced',
        'trend_strict': True,
        'zone_influence': 0.5,
        'min_hold_period': 3,
        'use_zones': False,
        'use_regime_filter': False
    }
    
    # Test standard (non-regime-aware) signals
    logger.info("Generating standard signals (no regime awareness)")
    long_entries_std, long_exits_std, short_entries_std, short_exits_std = generate_signals(
        close=data['close'],
        rsi=data['rsi'],
        bb_upper=data['bb_upper'],
        bb_lower=data['bb_lower'],
        trend_ma=data['trend_ma'],
        price_in_demand_zone=pd.Series(False, index=data.index),
        price_in_supply_zone=pd.Series(False, index=data.index),
        params=standard_params
    )
    
    # Test trending regime-aware signals
    trending_params = standard_params.copy()
    trending_params['use_regime_filter'] = True
    trending_params['_regime_info'] = trending_regime
    
    logger.info("Generating regime-aware signals for TRENDING regime")
    long_entries_trending, long_exits_trending, short_entries_trending, short_exits_trending = generate_signals(
        close=data['close'],
        rsi=data['rsi'],
        bb_upper=data['bb_upper'],
        bb_lower=data['bb_lower'],
        trend_ma=data['trend_ma'],
        price_in_demand_zone=pd.Series(False, index=data.index),
        price_in_supply_zone=pd.Series(False, index=data.index),
        params=trending_params
    )
    
    # Test ranging regime-aware signals
    ranging_params = standard_params.copy()
    ranging_params['use_regime_filter'] = True
    ranging_params['_regime_info'] = ranging_regime
    
    logger.info("Generating regime-aware signals for RANGING regime")
    long_entries_ranging, long_exits_ranging, short_entries_ranging, short_exits_ranging = generate_signals(
        close=data['close'],
        rsi=data['rsi'],
        bb_upper=data['bb_upper'],
        bb_lower=data['bb_lower'],
        trend_ma=data['trend_ma'],
        price_in_demand_zone=pd.Series(False, index=data.index),
        price_in_supply_zone=pd.Series(False, index=data.index),
        params=ranging_params
    )
    
    # Calculate trade counts by segment
    ranges = [(0, 49, "Ranging 1"), (50, 99, "Trending Up"), (100, 149, "Ranging 2"), (150, 199, "Trending Down")]
    
    results = {
        "Standard": {},
        "Trending-Optimized": {},
        "Ranging-Optimized": {}
    }
    
    for start, end, label in ranges:
        # Standard signals
        results["Standard"][label] = {
            "long_entries": long_entries_std.iloc[start:end+1].sum(),
            "long_exits": long_exits_std.iloc[start:end+1].sum(),
            "short_entries": short_entries_std.iloc[start:end+1].sum(),
            "short_exits": short_exits_std.iloc[start:end+1].sum()
        }
        
        # Trending regime-aware signals
        results["Trending-Optimized"][label] = {
            "long_entries": long_entries_trending.iloc[start:end+1].sum(),
            "long_exits": long_exits_trending.iloc[start:end+1].sum(),
            "short_entries": short_entries_trending.iloc[start:end+1].sum(),
            "short_exits": short_exits_trending.iloc[start:end+1].sum()
        }
        
        # Ranging regime-aware signals
        results["Ranging-Optimized"][label] = {
            "long_entries": long_entries_ranging.iloc[start:end+1].sum(),
            "long_exits": long_exits_ranging.iloc[start:end+1].sum(),
            "short_entries": short_entries_ranging.iloc[start:end+1].sum(),
            "short_exits": short_exits_ranging.iloc[start:end+1].sum()
        }
    
    # Save trades data to CSV
    trade_data = pd.DataFrame({
        'close': data['close'],
        'regime': data['regime'],
        'rsi': data['rsi'],
        'trend_ma': data['trend_ma'],
        'bb_upper': data['bb_upper'],
        'bb_lower': data['bb_lower'],
        'standard_long_entry': long_entries_std,
        'standard_long_exit': long_exits_std,
        'trending_long_entry': long_entries_trending,
        'trending_long_exit': long_exits_trending,
        'ranging_long_entry': long_entries_ranging,
        'ranging_long_exit': long_exits_ranging,
        'standard_short_entry': short_entries_std,
        'standard_short_exit': short_exits_std,
        'trending_short_entry': short_entries_trending,
        'trending_short_exit': short_exits_trending,
        'ranging_short_entry': short_entries_ranging,
        'ranging_short_exit': short_exits_ranging
    })
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    trade_data.to_csv(f'results/regime_signal_comparison_{timestamp}.csv')
    logger.info(f"Saved trade data to results/regime_signal_comparison_{timestamp}.csv")
    
    # Print results by market segment
    logger.info("\n=== SIGNAL GENERATION RESULTS BY MARKET SEGMENT ===")
    logger.info("Comparing standard vs. regime-optimized signal generation\n")
    
    logger.info("LONG ENTRIES:")
    for segment in [r[2] for r in ranges]:
        logger.info(f"{segment}: Standard={results['Standard'][segment]['long_entries']}, " +
                   f"Trending-Optimized={results['Trending-Optimized'][segment]['long_entries']}, " +
                   f"Ranging-Optimized={results['Ranging-Optimized'][segment]['long_entries']}")
    
    logger.info("\nSHORT ENTRIES:")
    for segment in [r[2] for r in ranges]:
        logger.info(f"{segment}: Standard={results['Standard'][segment]['short_entries']}, " +
                   f"Trending-Optimized={results['Trending-Optimized'][segment]['short_entries']}, " +
                   f"Ranging-Optimized={results['Ranging-Optimized'][segment]['short_entries']}")
    
    # Print summary statistics
    total_standard_trades = sum([
        results['Standard'][segment]['long_entries'] + 
        results['Standard'][segment]['short_entries']
        for segment in [r[2] for r in ranges]
    ])
    
    total_trending_trades = sum([
        results['Trending-Optimized'][segment]['long_entries'] + 
        results['Trending-Optimized'][segment]['short_entries']
        for segment in [r[2] for r in ranges]
    ])
    
    total_ranging_trades = sum([
        results['Ranging-Optimized'][segment]['long_entries'] + 
        results['Ranging-Optimized'][segment]['short_entries']
        for segment in [r[2] for r in ranges]
    ])
    
    trending_segments_trades_std = sum([
        results['Standard'][segment]['long_entries'] + 
        results['Standard'][segment]['short_entries']
        for segment in ["Trending Up", "Trending Down"]
    ])
    
    trending_segments_trades_trend = sum([
        results['Trending-Optimized'][segment]['long_entries'] + 
        results['Trending-Optimized'][segment]['short_entries']
        for segment in ["Trending Up", "Trending Down"]
    ])
    
    ranging_segments_trades_std = sum([
        results['Standard'][segment]['long_entries'] + 
        results['Standard'][segment]['short_entries']
        for segment in ["Ranging 1", "Ranging 2"]
    ])
    
    ranging_segments_trades_range = sum([
        results['Ranging-Optimized'][segment]['long_entries'] + 
        results['Ranging-Optimized'][segment]['short_entries']
        for segment in ["Ranging 1", "Ranging 2"]
    ])
    
    logger.info("\n=== SUMMARY STATISTICS ===")
    logger.info(f"Total trades: Standard={total_standard_trades}, " +
               f"Trending-Optimized={total_trending_trades}, " +
               f"Ranging-Optimized={total_ranging_trades}")
    
    logger.info("\n=== REGIME EFFECTIVENESS ===")
    logger.info(f"Trades in trending segments: Standard={trending_segments_trades_std}, " +
               f"Trending-Optimized={trending_segments_trades_trend}")
    
    if trending_segments_trades_std > 0:
        pct_change_trending = ((trending_segments_trades_trend - trending_segments_trades_std) / 
                              trending_segments_trades_std * 100)
        logger.info(f"Trending regime optimization impact: {pct_change_trending:.1f}% " +
                   f"({'more' if pct_change_trending > 0 else 'fewer'} trades in trending segments)")
    
    logger.info(f"Trades in ranging segments: Standard={ranging_segments_trades_std}, " +
               f"Ranging-Optimized={ranging_segments_trades_range}")
    
    if ranging_segments_trades_std > 0:
        pct_change_ranging = ((ranging_segments_trades_range - ranging_segments_trades_std) / 
                             ranging_segments_trades_std * 100)
        logger.info(f"Ranging regime optimization impact: {pct_change_ranging:.1f}% " +
                   f"({'more' if pct_change_ranging > 0 else 'fewer'} trades in ranging segments)")
    
    logger.info("\nTest complete! Results saved to CSV for further analysis.")
    return results

if __name__ == "__main__":
    test_regime_aware_signals()
