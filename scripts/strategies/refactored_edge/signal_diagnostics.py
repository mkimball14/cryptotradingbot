"""
Signal Diagnostics Module for Edge Multi-Factor Strategy.

This module provides diagnostic tools to analyze signal generation effectiveness,
visualize signals across different market regimes, and recommend optimal parameters.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Optional, Any
import os
import logging

# Local imports
from scripts.strategies.refactored_edge.balanced_signals import (
    SignalStrictness, 
    generate_balanced_signals,
    get_strictness_parameters
)
from scripts.strategies.refactored_edge.regime import MarketRegimeType, determine_market_regime, detect_market_regimes
from scripts.strategies.refactored_edge.enhanced_indicators import detect_enhanced_regime

# Configure logging
logger = logging.getLogger(__name__)


def analyze_signal_distribution(
    data: pd.DataFrame,
    strictness_levels: List[SignalStrictness] = None
) -> Dict[str, Dict[str, int]]:
    """
    Analyze signal distribution across different strictness levels and regimes.
    
    Args:
        data: DataFrame with price data and indicators
        strictness_levels: List of strictness levels to analyze
        
    Returns:
        Dict with signal counts by strictness level and regime
    """
    if strictness_levels is None:
        strictness_levels = [
            SignalStrictness.STRICT,
            SignalStrictness.BALANCED,
            SignalStrictness.MODERATELY_RELAXED,
            SignalStrictness.RELAXED,
            SignalStrictness.ULTRA_RELAXED
        ]
    
    # Ensure we have regime data
    if 'market_regime' not in data.columns:
        try:
            # First try using the enhanced regime detection from the enhanced_indicators module
            data['market_regime'] = detect_enhanced_regime(data)
        except Exception as e:
            logger.warning(f"Enhanced regime detection failed: {e}. Falling back to basic regime detection.")
            # Fall back to simple regime detection
            if 'adx' in data.columns:
                data['market_regime'] = determine_market_regime(data['adx'])
            else:
                # If no ADX available, use market_regime from detect_market_regimes
                data = detect_market_regimes(data)
                # Extract the regime column if available, otherwise default to all "RANGING"
                if 'regime' in data.columns:
                    data['market_regime'] = data['regime']
                else:
                    # Last resort - set everything to RANGING as the safest default
                    data['market_regime'] = pd.Series("RANGING", index=data.index)
    
    results = {}
    
    # Run analysis for each strictness level
    for strictness in strictness_levels:
        # Use strictness-specific parameters
        params = get_strictness_parameters(strictness)
        
        # Generate signals
        long_entries, long_exits, short_entries, short_exits = generate_balanced_signals(
            close=data['close'],
            rsi=data['rsi'],
            bb_upper=data['bb_upper'],
            bb_lower=data['bb_lower'],
            trend_ma=data['trend_ma'],
            price_in_demand_zone=data.get('demand_zone', pd.Series(False, index=data.index)),
            price_in_supply_zone=data.get('supply_zone', pd.Series(False, index=data.index)),
            rsi_lower_threshold=30,
            rsi_upper_threshold=70,
            use_zones=True,
            trend_strict=False,
            min_hold_period=params['min_hold_period'],
            trend_threshold_pct=params['trend_threshold_pct'],
            zone_influence=params['zone_influence'],
            strictness=strictness
        )
        
        # Combine signals
        all_entries = long_entries | short_entries
        
        # Count signals by regime
        trending_signals = all_entries[data['market_regime'] == 'TRENDING'].sum()
        ranging_signals = all_entries[data['market_regime'] == 'RANGING'].sum()
        
        # Calculate signal density (signals per day)
        days_in_period = (data.index[-1] - data.index[0]).days
        if days_in_period < 1:
            days_in_period = 1
        
        signal_density = all_entries.sum() / days_in_period
        
        results[strictness.value] = {
            'total_signals': all_entries.sum(),
            'trending_signals': trending_signals,
            'ranging_signals': ranging_signals,
            'signal_density': signal_density,
            'long_entries': long_entries.sum(),
            'short_entries': short_entries.sum()
        }
    
    return results


def visualize_signals_by_regime(
    data: pd.DataFrame,
    strictness: SignalStrictness = SignalStrictness.BALANCED,
    output_file: str = None
) -> None:
    """
    Create a visualization showing signals on price chart with regime backgrounds.
    
    Args:
        data: DataFrame with price and indicator data
        strictness: Strictness level to visualize
        output_file: Path to save the output HTML file, if None, display interactive
    """
    # Check if we have the required data
    required_columns = ['close', 'rsi', 'bb_upper', 'bb_lower', 'trend_ma']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Required column {col} not found in data")
    
    # Generate regime information if missing
    if 'market_regime' not in data.columns:
        data['market_regime'] = detect_enhanced_regime(
            data['close'], 
            data.get('rsi', None), 
            data.get('atr', None),
            data.get('adx', None)
        )
    
    # Generate signals using the specified strictness
    params = get_strictness_parameters(strictness)
    
    long_entries, long_exits, short_entries, short_exits = generate_balanced_signals(
        close=data['close'],
        rsi=data['rsi'],
        bb_upper=data['bb_upper'],
        bb_lower=data['bb_lower'],
        trend_ma=data['trend_ma'],
        price_in_demand_zone=data.get('demand_zone', pd.Series(False, index=data.index)),
        price_in_supply_zone=data.get('supply_zone', pd.Series(False, index=data.index)),
        rsi_lower_threshold=30,
        rsi_upper_threshold=70,
        use_zones=True,
        trend_strict=False,
        min_hold_period=params['min_hold_period'],
        trend_threshold_pct=params['trend_threshold_pct'],
        zone_influence=params['zone_influence'],
        strictness=strictness
    )
    
    # Create a plot with regime backgrounds
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True, 
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=("Price with Signals", "RSI with Bands")
    )
    
    # Price chart
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='black', width=1)
        ),
        row=1, col=1
    )
    
    # Add trend MA
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['trend_ma'],
            mode='lines',
            name='Trend MA',
            line=dict(color='blue', width=1)
        ),
        row=1, col=1
    )
    
    # Add Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['bb_upper'],
            mode='lines',
            name='BB Upper',
            line=dict(color='rgba(0,128,0,0.3)', width=1)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['bb_lower'],
            mode='lines',
            name='BB Lower',
            line=dict(color='rgba(0,128,0,0.3)', width=1),
            fill='tonexty',
            fillcolor='rgba(0,128,0,0.05)'
        ),
        row=1, col=1
    )
    
    # Add regime backgrounds
    for i in range(len(data) - 1):
        if data['market_regime'].iloc[i] == 'TRENDING':
            color = 'rgba(255,192,192,0.2)'  # Light red for trending
        else:
            color = 'rgba(192,192,255,0.2)'  # Light blue for ranging
        
        fig.add_vrect(
            x0=data.index[i],
            x1=data.index[i+1],
            fillcolor=color,
            layer="below",
            line_width=0,
            row=1, col=1
        )
        
        fig.add_vrect(
            x0=data.index[i],
            x1=data.index[i+1],
            fillcolor=color,
            layer="below",
            line_width=0,
            row=2, col=1
        )
    
    # Add signals
    long_entry_idx = data.index[long_entries]
    short_entry_idx = data.index[short_entries]
    
    fig.add_trace(
        go.Scatter(
            x=long_entry_idx,
            y=data.loc[long_entry_idx, 'close'],
            mode='markers',
            name='Long Entries',
            marker=dict(color='green', size=10, symbol='triangle-up')
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=short_entry_idx,
            y=data.loc[short_entry_idx, 'close'],
            mode='markers',
            name='Short Entries',
            marker=dict(color='red', size=10, symbol='triangle-down')
        ),
        row=1, col=1
    )
    
    # Add RSI plot
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['rsi'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=1)
        ),
        row=2, col=1
    )
    
    # Add RSI bands
    fig.add_hline(y=30, line=dict(color='red', width=1, dash='dash'), row=2, col=1)
    fig.add_hline(y=70, line=dict(color='red', width=1, dash='dash'), row=2, col=1)
    fig.add_hline(y=50, line=dict(color='black', width=1, dash='dot'), row=2, col=1)
    
    # Update layout
    fig.update_layout(
        title=f"Signal Analysis with {strictness.value} Mode",
        height=800,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Export or show
    if output_file:
        fig.write_html(output_file)
        print(f"Visualization saved to {output_file}")
    else:
        fig.show()


def recommend_parameters(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze signal generation across different parameters and recommend optimal settings.
    
    Args:
        data: DataFrame with price and indicator data
        
    Returns:
        Dict with recommended parameters
    """
    # Analyze signal distribution
    signal_distribution = analyze_signal_distribution(data)
    
    # Calculate regime distribution
    if 'market_regime' not in data.columns:
        data['market_regime'] = detect_enhanced_regime(
            data['close'], 
            data.get('rsi', None), 
            data.get('atr', None),
            data.get('adx', None)
        )
    
    trending_pct = (data['market_regime'] == 'TRENDING').mean() * 100
    ranging_pct = (data['market_regime'] == 'RANGING').mean() * 100
    
    # Determine target signal density based on timeframe (assume 1 hour)
    # For hourly data, aim for 1-3 signals per day
    target_density = 2.0
    
    # Find closest strictness level to target density
    best_strictness = None
    best_delta = float('inf')
    
    for strictness, stats in signal_distribution.items():
        density_delta = abs(stats['signal_density'] - target_density)
        if density_delta < best_delta:
            best_delta = density_delta
            best_strictness = strictness
    
    # Get parameters for the recommended strictness
    strictness_enum = SignalStrictness(best_strictness)
    recommended_params = get_strictness_parameters(strictness_enum)
    
    # Add additional recommendations for regime-specific parameters
    if trending_pct > 60:
        # Mostly trending market - be more conservative
        recommended_regime_params = {
            'trend_threshold_pct': recommended_params['trend_threshold_pct'] * 1.2,
            'zone_influence': recommended_params['zone_influence'] * 0.9,
            'min_hold_period': max(recommended_params['min_hold_period'], 2),
            'note': "Mostly trending market detected - parameters adjusted for trend following"
        }
    elif ranging_pct > 60:
        # Mostly ranging market - be more aggressive
        recommended_regime_params = {
            'trend_threshold_pct': recommended_params['trend_threshold_pct'] * 0.8,
            'zone_influence': min(recommended_params['zone_influence'] * 1.2, 1.0),
            'min_hold_period': min(recommended_params['min_hold_period'], 1),
            'note': "Mostly ranging market detected - parameters adjusted for range trading"
        }
    else:
        # Mixed market - use balanced approach
        recommended_regime_params = {
            'trend_threshold_pct': recommended_params['trend_threshold_pct'],
            'zone_influence': recommended_params['zone_influence'],
            'min_hold_period': recommended_params['min_hold_period'],
            'note': "Mixed market regime detected - using balanced parameters"
        }
    
    # Combine results
    recommendation = {
        'recommended_strictness': best_strictness,
        'signal_density': signal_distribution[best_strictness]['signal_density'],
        'total_signals': signal_distribution[best_strictness]['total_signals'],
        'market_conditions': {
            'trending_percentage': trending_pct,
            'ranging_percentage': ranging_pct
        },
        'base_parameters': recommended_params,
        'regime_adapted_parameters': recommended_regime_params,
        'signal_distribution': signal_distribution
    }
    
    return recommendation


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Signal Diagnostics Tool")
    parser.add_argument("--data-file", type=str, help="Path to data CSV file")
    parser.add_argument("--output-dir", type=str, default="./reports", help="Output directory for reports")
    parser.add_argument("--strictness", type=str, default="BALANCED", 
                        choices=["STRICT", "BALANCED", "MODERATELY_RELAXED", "RELAXED", "ULTRA_RELAXED"],
                        help="Signal strictness level to analyze")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Load data
    if args.data_file and os.path.exists(args.data_file):
        data = pd.read_csv(args.data_file, index_col=0, parse_dates=True)
        
        # Generate recommendations
        recommendations = recommend_parameters(data)
        
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
        
        # Visualize signals
        strictness_enum = SignalStrictness(args.strictness)
        output_file = os.path.join(args.output_dir, f"signal_analysis_{args.strictness.lower()}.html")
        visualize_signals_by_regime(data, strictness_enum, output_file)
        
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
    else:
        print("Data file not found. Please provide a valid path with --data-file.")
        print("Example usage: python signal_diagnostics.py --data-file=data.csv --strictness=BALANCED")
