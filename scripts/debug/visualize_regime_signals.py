"""
Enhanced Regime-Aware Signal Visualization Script

This script provides clear visualizations showing how trading signals adapt to different market regimes.
It uses vectorbtpro's native visualization methods with robust error handling.
"""

import sys
import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime
import traceback

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import vectorbtpro - must be imported earlier to be available throughout
try:
    import vectorbtpro as vbt
except ImportError:
    print("ERROR: vectorbtpro not installed. Please install it to run this script.")
    sys.exit(1)

# Import local modules
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.utils import normalize_regime_type

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('regime_visualization')

def generate_sample_data(length=200, with_trend_change=True):
    """Generate synthetic data with clearly defined trending and ranging segments."""
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
    
    # Create clear regime segments
    segments = [
        (0, 49, 'ranging', 0.0),     # Ranging segment
        (50, 99, 'trending', 0.1),   # Uptrend 
        (100, 149, 'ranging', 0.0),  # Ranging segment
        (150, 199, 'trending', -0.1) # Downtrend
    ]
    
    # Generate price data with clear trends and ranges
    for i in range(length):
        # Find current segment
        for start, end, regime, trend in segments:
            if start <= i <= end:
                data['regime'][i] = regime
                # Add appropriate price movement based on regime
                if regime == 'trending':
                    price += trend + np.random.normal(0, 0.03)  # Trending movement with small noise
                else:
                    price += np.random.normal(0, 0.2)  # Ranging movement (random)
                break
                
        # Set price data
        data['close'][i] = price
        data['high'][i] = price * (1 + abs(np.random.normal(0, 0.005)))
        data['low'][i] = price * (1 - abs(np.random.normal(0, 0.005)))
        
        # Generate RSI-like values based on regime and trend
        if data['regime'][i] == 'trending':
            # In trending segments, create logical RSI values
            current_segment = next((s for s in segments if s[0] <= i <= s[1]), None)
            if current_segment and current_segment[3] > 0:  # Uptrend
                data['rsi'][i] = 70 + np.random.normal(0, 5)  # Higher RSI in uptrend
            else:  # Downtrend
                data['rsi'][i] = 30 + np.random.normal(0, 5)  # Lower RSI in downtrend
        else:  # Ranging
            data['rsi'][i] = 50 + np.random.normal(0, 15)  # More variable RSI in ranging markets
            
        # Calculate reasonable indicators
        # Moving average - 10-period simple moving average
        if i >= 10:
            data['trend_ma'][i] = np.mean(data['close'][max(0, i-10):i+1])
        else:
            data['trend_ma'][i] = data['close'][i]
        
        # Bollinger bands - 20-period, 2 standard deviations
        if i >= 20:
            std = np.std(data['close'][max(0, i-20):i+1])
            data['bb_upper'][i] = data['trend_ma'][i] + 2 * std
            data['bb_lower'][i] = data['trend_ma'][i] - 2 * std
        else:
            data['bb_upper'][i] = data['close'][i] * 1.02  # 2% above price
            data['bb_lower'][i] = data['close'][i] * 0.98  # 2% below price
    
    # Create dataframe
    df = pd.DataFrame(data, index=dates)
    
    return df

def generate_regime_signals(data):
    """Generate standard and regime-aware signals for comparison."""
    logger.info("Generating signals for different regime approaches")
    
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
    
    # Compile results
    signals = {
        'standard': {
            'long_entries': long_entries_std,
            'long_exits': long_exits_std,
            'short_entries': short_entries_std,
            'short_exits': short_exits_std
        },
        'trending': {
            'long_entries': long_entries_trending,
            'long_exits': long_exits_trending,
            'short_entries': short_entries_trending,
            'short_exits': short_exits_trending
        },
        'ranging': {
            'long_entries': long_entries_ranging,
            'long_exits': long_exits_ranging,
            'short_entries': short_entries_ranging,
            'short_exits': short_exits_ranging
        }
    }
    
    return signals

def visualize_signals(data, signals, output_dir):
    """Create visualizations showing how signals adapt to different market regimes."""
    logger.info("Creating visualizations to demonstrate regime-aware trading")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # First, save the underlying data to CSV for reference
    data_with_signals = data.copy()
    
    # Add signal columns for each strategy
    for strategy in signals:
        for signal_type in signals[strategy]:
            data_with_signals[f'{strategy}_{signal_type}'] = signals[strategy][signal_type].astype(int)
    
    # Save to CSV
    csv_path = os.path.join(output_dir, f'regime_signals_{timestamp}.csv')
    data_with_signals.to_csv(csv_path)
    logger.info(f"Saved signal data to {csv_path}")
    
    # Visualization 1: Signal Comparison using vectorbtpro's built-in plotting functions
    try:
        logger.info("Creating Signal Comparison Visualization")
        
        # Create a combined DataFrame with price and signals
        combined_data = pd.DataFrame({
            'Price': data['close'],
            'Standard_Entries': signals['standard']['long_entries'].astype(int),
            'Trending_Entries': signals['trending']['long_entries'].astype(int),
            'Ranging_Entries': signals['ranging']['long_entries'].astype(int),
            'Standard_Exits': signals['standard']['long_exits'].astype(int),
            'Trending_Exits': signals['trending']['long_exits'].astype(int),
            'Ranging_Exits': signals['ranging']['long_exits'].astype(int),
            'Regime': data['regime']
        })
        
        # Use vectorbtpro's basic plotting functionality
        try:
            # Attempt to use regular plotly
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            # Create figure with price data
            fig = make_subplots(rows=1, cols=1)
            
            # Add price line
            fig.add_trace(
                go.Scatter(x=combined_data.index, y=combined_data['Price'], 
                          name='Price', line=dict(color='black', width=1)),
                row=1, col=1
            )
            
            # Add entry markers
            entry_colors = {'Standard': 'blue', 'Trending': 'green', 'Ranging': 'purple'}
            for strategy, color in entry_colors.items():
                entries = combined_data[f'{strategy}_Entries']
                entry_indices = combined_data.index[entries == 1]
                entry_prices = combined_data.loc[entry_indices, 'Price']
                
                if not entry_indices.empty:
                    fig.add_trace(
                        go.Scatter(x=entry_indices, y=entry_prices, 
                                  mode='markers', name=f'{strategy} Entries',
                                  marker=dict(symbol='triangle-up', size=10, color=color)),
                        row=1, col=1
                    )
            
            # Add exit markers
            exit_colors = {'Standard': 'red', 'Trending': 'orange', 'Ranging': 'brown'}
            for strategy, color in exit_colors.items():
                exits = combined_data[f'{strategy}_Exits']
                exit_indices = combined_data.index[exits == 1]
                exit_prices = combined_data.loc[exit_indices, 'Price']
                
                if not exit_indices.empty:
                    fig.add_trace(
                        go.Scatter(x=exit_indices, y=exit_prices, 
                                  mode='markers', name=f'{strategy} Exits',
                                  marker=dict(symbol='triangle-down', size=10, color=color)),
                        row=1, col=1
                    )
            
            # Add background shading for different regimes
            ranging_mask = combined_data['Regime'] == 'ranging'
            trending_mask = combined_data['Regime'] == 'trending'
            
            y_min, y_max = combined_data['Price'].min(), combined_data['Price'].max()
            padding = (y_max - y_min) * 0.1
            y_min -= padding
            y_max += padding
            
            # Identify continuous blocks of regime
            def identify_regime_blocks(mask):
                blocks = []
                in_block = False
                start_idx = None
                
                for i, is_active in enumerate(mask):
                    if is_active and not in_block:
                        in_block = True
                        start_idx = combined_data.index[i]
                    elif not is_active and in_block:
                        in_block = False
                        blocks.append((start_idx, combined_data.index[i-1]))
                
                # Handle case where regime ends at the last data point
                if in_block:
                    blocks.append((start_idx, combined_data.index[-1]))
                
                return blocks
            
            ranging_blocks = identify_regime_blocks(ranging_mask)
            trending_blocks = identify_regime_blocks(trending_mask)
            
            # Add ranging background
            for start, end in ranging_blocks:
                fig.add_vrect(
                    x0=start, x1=end,
                    fillcolor="lightskyblue", opacity=0.2,
                    layer="below", line_width=0,
                )
            
            # Add trending background
            for start, end in trending_blocks:
                fig.add_vrect(
                    x0=start, x1=end,
                    fillcolor="lightgreen", opacity=0.2,
                    layer="below", line_width=0,
                )
            
            # Update layout
            fig.update_layout(
                title="Signal Comparison: Standard vs Regime-Optimized",
                xaxis_title="Date",
                yaxis_title="Price",
                width=1000,
                height=600,
                legend_title="Signals",
                hovermode="x unified"
            )
            
            # Save the figure
            signals_path = os.path.join(output_dir, f'signal_comparison_{timestamp}.html')
            fig.write_html(signals_path)
            logger.info(f"Saved signal comparison plot to {signals_path}")
            
        except ImportError:
            logger.warning("Plotly not available, using vectorbtpro's built-in plotting")
            # Fallback to simpler plotting method if available
            signals_path = os.path.join(output_dir, f'signal_data_{timestamp}.csv')
            combined_data.to_csv(signals_path)
            logger.info(f"Saved signal data to {signals_path} - use external tool for visualization")
            
    except Exception as e:
        logger.error(f"Error creating signal comparison visualization: {str(e)}")
        traceback.print_exc()
        
    except Exception as e:
        logger.error(f"Error creating signal comparison visualization: {str(e)}")
        traceback.print_exc()
    
    # Visualization 2: Create separate signal plots for each market segment to compare strategies
    try:
        logger.info("Creating market segment comparison visualizations")
        
        # Define segments
        segments = [
            (0, 49, "Ranging Segment 1"),
            (50, 99, "Trending Up Segment"),
            (100, 149, "Ranging Segment 2"),
            (150, 199, "Trending Down Segment")
        ]
        
        # Create a comparison visualization for each segment using Plotly directly
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            for start, end, segment_name in segments:
                # Extract segment data
                segment_data = data.iloc[start:end+1].copy()
                segment_regime = segment_data['regime'].iloc[0]  # Get regime type for this segment
                
                # Create figure
                fig = make_subplots(rows=1, cols=1)
                
                # Add price line
                fig.add_trace(
                    go.Scatter(x=segment_data.index, y=segment_data['close'], 
                              name='Price', line=dict(color='black', width=1)),
                    row=1, col=1
                )
                
                # Add entry markers for each strategy
                entry_colors = {'Standard': 'blue', 'Trending': 'green', 'Ranging': 'purple'}
                for strategy, color in entry_colors.items():
                    if strategy == 'Standard':
                        entries = signals['standard']['long_entries'].iloc[start:end+1]
                    elif strategy == 'Trending':
                        entries = signals['trending']['long_entries'].iloc[start:end+1]
                    else:  # Ranging
                        entries = signals['ranging']['long_entries'].iloc[start:end+1]
                    
                    entry_indices = segment_data.index[entries.astype(bool)]
                    if not entry_indices.empty:
                        entry_prices = segment_data.loc[entry_indices, 'close']
                        fig.add_trace(
                            go.Scatter(x=entry_indices, y=entry_prices, 
                                      mode='markers', name=f'{strategy} Entries',
                                      marker=dict(symbol='triangle-up', size=10, color=color)),
                            row=1, col=1
                        )
                
                # Add background color based on regime
                if segment_regime == 'ranging':
                    fig.update_layout(
                        plot_bgcolor='rgba(173, 216, 230, 0.1)'  # Light blue for ranging
                    )
                else:  # trending
                    fig.update_layout(
                        plot_bgcolor='rgba(144, 238, 144, 0.1)'  # Light green for trending
                    )
                
                # Add stats annotation
                standard_entries = signals['standard']['long_entries'].iloc[start:end+1].sum()
                trending_entries = signals['trending']['long_entries'].iloc[start:end+1].sum()
                ranging_entries = signals['ranging']['long_entries'].iloc[start:end+1].sum()
                
                annotation_text = f"<b>{segment_name} ({segment_regime} market)</b><br>"
                annotation_text += f"Standard: {standard_entries} entries<br>"
                annotation_text += f"Trending-Opt: {trending_entries} entries<br>"
                annotation_text += f"Ranging-Opt: {ranging_entries} entries"
                
                fig.add_annotation(
                    xref='paper', yref='paper',
                    x=0.01, y=0.98,
                    text=annotation_text,
                    showarrow=False,
                    bgcolor='white',
                    bordercolor='black',
                    borderwidth=1,
                    font=dict(size=10)
                )
                
                # Update layout
                fig.update_layout(
                    title=f"Signal Comparison: {segment_name} ({segment_regime} market)",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    width=800,
                    height=500,
                    legend_title="Signals",
                    hovermode="x unified"
                )
                
                # Save the figure
                segment_path = os.path.join(output_dir, f'segment_{segment_name.replace(" ", "_").lower()}_{timestamp}.html')
                fig.write_html(segment_path)
                logger.info(f"Saved {segment_name} comparison plot to {segment_path}")
                
        except ImportError as e:
            logger.warning(f"Plotly not available for segment visualization: {str(e)}")
            
            # Create simple CSV files for each segment as a fallback
            for start, end, segment_name in segments:
                segment_data = data.iloc[start:end+1].copy()
                
                # Add signal columns
                segment_data['Standard_Entries'] = signals['standard']['long_entries'].iloc[start:end+1].astype(int)
                segment_data['Trending_Entries'] = signals['trending']['long_entries'].iloc[start:end+1].astype(int)
                segment_data['Ranging_Entries'] = signals['ranging']['long_entries'].iloc[start:end+1].astype(int)
                
                # Save to CSV
                segment_path = os.path.join(output_dir, f'segment_{segment_name.replace(" ", "_").lower()}_{timestamp}.csv')
                segment_data.to_csv(segment_path)
                logger.info(f"Saved {segment_name} data to {segment_path} (CSV fallback)")
                
    except Exception as e:
        logger.error(f"Error creating market segment visualizations: {str(e)}")
        traceback.print_exc()
        
    except Exception as e:
        logger.error(f"Error creating market segment visualizations: {str(e)}")
        traceback.print_exc()
    
    # Visualization 3: Signal distribution by regime (simpler fallback visualization)
    try:
        logger.info("Creating signal distribution summary")
        
        # Count signals in each segment
        distribution = {}
        
        for start, end, segment_name in segments:
            distribution[segment_name] = {
                'regime': data['regime'].iloc[start],  # Just take the first value as the segment regime
                'standard': {
                    'long_entries': signals['standard']['long_entries'].iloc[start:end+1].sum(),
                    'long_exits': signals['standard']['long_exits'].iloc[start:end+1].sum(),
                },
                'trending': {
                    'long_entries': signals['trending']['long_entries'].iloc[start:end+1].sum(),
                    'long_exits': signals['trending']['long_exits'].iloc[start:end+1].sum(),
                },
                'ranging': {
                    'long_entries': signals['ranging']['long_entries'].iloc[start:end+1].sum(),
                    'long_exits': signals['ranging']['long_exits'].iloc[start:end+1].sum(),
                }
            }
        
        # Create a summary table
        summary_data = []
        for segment, stats in distribution.items():
            summary_data.append({
                'Segment': segment,
                'Regime': stats['regime'],
                'Standard Entries': stats['standard']['long_entries'],
                'Trending-Opt Entries': stats['trending']['long_entries'],
                'Ranging-Opt Entries': stats['ranging']['long_entries'],
                'Standard Exits': stats['standard']['long_exits'],
                'Trending-Opt Exits': stats['trending']['long_exits'],
                'Ranging-Opt Exits': stats['ranging']['long_exits'],
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_path = os.path.join(output_dir, f'signal_distribution_{timestamp}.csv')
        summary_df.to_csv(summary_path, index=False)
        logger.info(f"Saved signal distribution summary to {summary_path}")
        
        # Display summary in console for quick reference
        logger.info("\n=== SIGNAL DISTRIBUTION BY MARKET SEGMENT ===")
        for segment, stats in distribution.items():
            logger.info(f"{segment} ({stats['regime']} market):")
            logger.info(f"  Standard: {stats['standard']['long_entries']} entries, {stats['standard']['long_exits']} exits")
            logger.info(f"  Trending-Optimized: {stats['trending']['long_entries']} entries, {stats['trending']['long_exits']} exits")
            logger.info(f"  Ranging-Optimized: {stats['ranging']['long_entries']} entries, {stats['ranging']['long_exits']} exits")
        
    except Exception as e:
        logger.error(f"Error creating signal distribution summary: {str(e)}")
        traceback.print_exc()
    
    logger.info(f"Visualization complete. All results saved to {output_dir}")
    return output_dir

def main():
    """Main function to generate sample data and visualize regime-aware signal generation."""
    logger.info("Starting Enhanced Regime-Aware Signal Visualization")
    
    # Generate clear sample data
    data = generate_sample_data(length=200)
    logger.info("Generated sample data with distinct trending and ranging segments")
    
    # Generate signals for different approaches
    signals = generate_regime_signals(data)
    logger.info("Generated signals using standard and regime-aware approaches")
    
    # Create output directory
    output_dir = os.path.join('results', 'regime_visualization_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    os.makedirs(output_dir, exist_ok=True)
    
    # Create visualizations
    output_path = visualize_signals(data, signals, output_dir)
    logger.info(f"Visualization complete. Results saved to {output_path}")
    
    return output_path

if __name__ == "__main__":
    try:
        output_path = main()
        print(f"\nVisualization complete! Results saved to {output_path}")
        print("Open the HTML files in a browser to view interactive visualizations.")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        traceback.print_exc()
        print("\nERROR: Visualization failed. See logs for details.")
        sys.exit(1)
