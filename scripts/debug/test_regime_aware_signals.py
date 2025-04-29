"""
Test script for demonstrating regime-aware signal generation.

This script compares standard signal generation with regime-aware signal generation
to show the performance improvements possible when adapting parameters to market conditions.
"""

import sys
import os
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Import vectorbtpro at the global level to ensure it's available throughout the script
import vectorbtpro as vbt

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import local modules
from scripts.strategies.refactored_edge import indicators
from scripts.strategies.refactored_edge.utils import normalize_regime_type, calculate_regime_percentages
from scripts.strategies.refactored_edge.regime import determine_market_regime, determine_market_regime_advanced
from scripts.strategies.refactored_edge.wfo_optimization import determine_market_regime_for_params
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('regime_aware_signals_test')

def generate_sample_data(length=1000, trending_percentage=0.5):
    """
    Generate sample price data with controllable trending/ranging segments.
    
    Args:
        length: Number of data points
        trending_percentage: Percentage of data that should be trending (0-1)
    
    Returns:
        DataFrame with OHLCV data and market regime labels
    """
    # Create date index
    dates = pd.date_range(start='2025-01-01', periods=length, freq='4h')
    
    # Initialize data
    data = {
        'open': np.zeros(length),
        'high': np.zeros(length),
        'low': np.zeros(length),
        'close': np.zeros(length),
        'volume': np.random.normal(1000, 200, size=length),
        'regime': ['ranging'] * length  # Default regime
    }
    
    # Determine trending segments
    trending_points = int(length * trending_percentage)
    trending_indices = sorted(np.random.choice(range(length), trending_points, replace=False))
    for idx in trending_indices:
        data['regime'][idx] = 'trending'
    
    # Generate price data
    price = 100.0  # Starting price
    trend_direction = 1  # 1 for up, -1 for down
    
    for i in range(length):
        # Price volatility depends on regime
        if data['regime'][i] == 'trending':
            # Strong trend with low noise
            price += trend_direction * (0.05 + np.random.normal(0, 0.02))
            
            # Occasionally change trend direction
            if np.random.random() < 0.01:  # 1% chance of trend reversal
                trend_direction *= -1
        else:
            # Ranging with higher noise
            price += np.random.normal(0, 0.15)
        
        # Set OHLC values
        data['close'][i] = price
        data['open'][i] = price * (1 + np.random.normal(0, 0.01))
        data['high'][i] = max(data['open'][i], data['close'][i]) * (1 + abs(np.random.normal(0, 0.01)))
        data['low'][i] = min(data['open'][i], data['close'][i]) * (1 - abs(np.random.normal(0, 0.01)))
    
    # Create DataFrame
    df = pd.DataFrame(data, index=dates)
    
    # Add technical indicators needed for regime detection
    df['adx'] = np.random.normal(25, 10, size=length)  # Random ADX values
    df.loc[df['regime'] == 'trending', 'adx'] += 15  # Higher ADX in trending periods
    
    # Add other indicators needed for full regime detection
    df['plus_di'] = np.random.normal(20, 10, size=length)
    df['minus_di'] = np.random.normal(20, 10, size=length)
    df['atr'] = np.random.normal(2, 0.5, size=length)
    
    return df

def run_comparison_test(data, plot_results=True):
    """
    Run a comparison between standard and regime-aware signal generation.
    
    Args:
        data: DataFrame with OHLCV data and market indicators
        plot_results: Whether to display performance plots
    
    Returns:
        Dictionary of performance metrics for both methods
    """
    logger.info("Starting comparison between standard and regime-aware signal generation")
    
    # Create a configuration object for indicator calculation
    from types import SimpleNamespace
    config = SimpleNamespace(
        rsi_window=14,
        bb_window=20,
        bb_std_dev=2.0,
        ma_window=50,
        atr_window=14,
        trend_ma_window=50,  # Added this required parameter
        rsi_entry_threshold=30,
        rsi_exit_threshold=70,
        adx_window=14,
        adx_threshold=25.0,
        strong_adx_threshold=40.0,  # Added for enhanced regime detection
        volatility_threshold=0.02,
        momentum_lookback=5,
        momentum_threshold=0.01,
        use_enhanced_regimes=True,
        use_regime_filter=False,  # Will toggle this for comparison
        signal_strictness='balanced',
        trend_strict=True,
        zone_influence=0.5,
        min_hold_period=2,
        atr_window_sizing=14  # Added for indicator calculation
    )
    
    # Ensure we have all necessary indicators
    logger.info("Calculating technical indicators")
    try:
        data_with_indicators = indicators.add_indicators(data.copy(), config)
        if data_with_indicators is None:
            logger.error("Indicator calculation returned None")
            raise ValueError("Failed to calculate indicators")
        
        # Verify that all required indicators exist
        required_indicators = ['rsi', 'bb_upper', 'bb_lower', 'trend_ma', 'adx', 'plus_di', 'minus_di', 'atr']
        missing = [ind for ind in required_indicators if ind not in data_with_indicators.columns]
        if missing:
            logger.error(f"Missing indicators: {missing}")
            # Add missing indicators directly if they're already in our source data
            for ind in missing:
                if ind in data.columns:
                    logger.info(f"Using pre-calculated {ind} from source data")
                    data_with_indicators[ind] = data[ind]
            
            # Recheck for missing indicators
            missing = [ind for ind in required_indicators if ind not in data_with_indicators.columns]
            if missing:
                logger.error(f"Still missing indicators after fix attempt: {missing}")
                raise ValueError(f"Missing required indicators: {missing}")
    except Exception as e:
        logger.error(f"Failed to calculate indicators: {str(e)}")
        logger.info("Creating simplified dataset with minimal indicators for demonstration")
        
        # Create a simplified dataset if indicator calculation fails
        data_with_indicators = data.copy()
        data_with_indicators['rsi'] = np.random.normal(50, 15, size=len(data))
        data_with_indicators['bb_upper'] = data['close'] + data['close'] * 0.02
        data_with_indicators['bb_lower'] = data['close'] - data['close'] * 0.02
        data_with_indicators['trend_ma'] = data['close'].rolling(window=50).mean().fillna(data['close'])
    
    # Determine market regimes using enhanced detection
    logger.info("Detecting market regimes")
    try:
        # Make sure all required fields exist
        missing_fields = []
        required_fields = ['adx', 'plus_di', 'minus_di', 'atr', 'close', 'high', 'low']
        for field in required_fields:
            if field not in data_with_indicators.columns:
                missing_fields.append(field)
                # Create simple fallbacks for missing fields
                if field == 'adx':
                    data_with_indicators[field] = pd.Series(
                        np.where(data['regime'] == 'trending', 35, 20), 
                        index=data.index
                    )
                elif field in ['plus_di', 'minus_di']:
                    data_with_indicators[field] = pd.Series(
                        np.random.normal(25, 10, size=len(data)), 
                        index=data.index
                    )
                elif field == 'atr':
                    data_with_indicators[field] = (data['high'] - data['low']).abs()

        if missing_fields:
            logger.warning(f"Created fallback values for missing fields: {missing_fields}")
        
        regimes = determine_market_regime_advanced(
            adx=data_with_indicators['adx'],
            plus_di=data_with_indicators['plus_di'],
            minus_di=data_with_indicators['minus_di'],
            atr=data_with_indicators['atr'],
            close=data_with_indicators['close'],
            high=data_with_indicators['high'],
            low=data_with_indicators['low'],
            volume=data_with_indicators.get('volume', None),
            adx_threshold=config.adx_threshold,
            strong_adx_threshold=40.0,
            volatility_threshold=config.volatility_threshold,
            momentum_lookback=config.momentum_lookback,
            momentum_threshold=config.momentum_threshold
        )

        # Calculate regime percentages
        regime_info = calculate_regime_percentages(regimes)
        logger.info(f"Detected regime distribution: {regime_info}")
        
        # Prepare regime info for the params dictionary
        regime_stats = determine_market_regime_for_params(data_with_indicators, config)
    except Exception as e:
        logger.error(f"Error in regime detection: {str(e)}")
        logger.info("Creating fallback regime data based on simulated regimes")
        
        # Use the pre-generated regime data from our synthetic dataset
        regimes = pd.Series(data['regime'].values, index=data.index)
        regime_info = {'trending': 40.0, 'ranging': 60.0}
        logger.info(f"Using simulated regime distribution: {regime_info}")
        
        # Create fallback regime stats
        regime_stats = {
            'predominant_regime': 'ranging',
            'trending_pct': 40.0,
            'ranging_pct': 60.0,
            'strong_trending_pct': 15.0,
            'weak_trending_pct': 25.0,
            'ranging_volatile_pct': 30.0,
            'ranging_normal_pct': 30.0
        }
    
    logger.info(f"Overall market regime: {regime_stats['predominant_regime']} "
               f"(trending: {regime_stats['trending_pct']:.1f}%, ranging: {regime_stats['ranging_pct']:.1f}%)")

    
    # Run standard signals (without regime awareness)
    logger.info("Generating standard signals (no regime awareness)")
    params_standard = vars(config).copy()
    params_standard['_regime_info'] = regime_stats.copy()
    params_standard['use_regime_filter'] = False
    
    long_entries_std, long_exits_std, short_entries_std, short_exits_std = generate_signals(
        close=data_with_indicators['close'],
        rsi=data_with_indicators['rsi'],
        bb_upper=data_with_indicators['bb_upper'],
        bb_lower=data_with_indicators['bb_lower'],
        trend_ma=data_with_indicators['trend_ma'],
        price_in_demand_zone=pd.Series(False, index=data.index),
        price_in_supply_zone=pd.Series(False, index=data.index),
        params=params_standard
    )
    
    # Run regime-aware signals
    logger.info("Generating regime-aware signals")
    params_regime_aware = vars(config).copy()
    params_regime_aware['_regime_info'] = regime_stats.copy()
    params_regime_aware['use_regime_filter'] = True
    
    long_entries_regime, long_exits_regime, short_entries_regime, short_exits_regime = generate_signals(
        close=data_with_indicators['close'],
        rsi=data_with_indicators['rsi'],
        bb_upper=data_with_indicators['bb_upper'],
        bb_lower=data_with_indicators['bb_lower'],
        trend_ma=data_with_indicators['trend_ma'],
        price_in_demand_zone=pd.Series(False, index=data.index),
        price_in_supply_zone=pd.Series(False, index=data.index),
        params=params_regime_aware
    )
    
    # Create portfolios with both signal sets
    logger.info("Creating portfolios for performance comparison")
    pf_standard = vbt.Portfolio.from_signals(
        close=data_with_indicators['close'],
        entries=long_entries_std,
        exits=long_exits_std,
        short_entries=short_entries_std,
        short_exits=short_exits_std,
        init_cash=10000.0,
        fees=0.0015,  # 0.15% commission
        slippage=0.0005  # 0.05% slippage
    )
    
    pf_regime = vbt.Portfolio.from_signals(
        close=data_with_indicators['close'],
        entries=long_entries_regime,
        exits=long_exits_regime,
        short_entries=short_entries_regime,
        short_exits=short_exits_regime,
        init_cash=10000.0,
        fees=0.0015,  # 0.15% commission
        slippage=0.0005  # 0.05% slippage
    )
    
    # Compile performance metrics
    stats_standard = pf_standard.stats()
    stats_regime = pf_regime.stats()
    
    logger.info("Performance Comparison:")
    logger.info(f"Standard Signals: Return={stats_standard['Total Return [%]']:.2f}%, "
               f"Sharpe={stats_standard.get('Sharpe Ratio', 0.0):.2f}, "
               f"Trades={pf_standard.trades.count()}, "
               f"Win Rate={stats_standard['Win Rate [%]']:.2f}%")
    
    logger.info(f"Regime-Aware: Return={stats_regime['Total Return [%]']:.2f}%, "
               f"Sharpe={stats_regime.get('Sharpe Ratio', 0.0):.2f}, "
               f"Trades={pf_regime.trades.count()}, "
               f"Win Rate={stats_regime['Win Rate [%]']:.2f}%")
    
    # Percentage improvement
    return_improvement = (
        (stats_regime['Total Return [%]'] - stats_standard['Total Return [%]']) / 
        abs(stats_standard['Total Return [%]'] + 1e-10)  # Avoid division by zero
    ) * 100
    
    sharpe_improvement = (
        (stats_regime.get('Sharpe Ratio', 0.0) - stats_standard.get('Sharpe Ratio', 0.0)) / 
        abs(stats_standard.get('Sharpe Ratio', 0.0) + 1e-10)  # Avoid division by zero
    ) * 100
    
    win_rate_improvement = stats_regime['Win Rate [%]'] - stats_standard['Win Rate [%]']
    
    logger.info(f"Improvement with Regime-Aware Approach:")
    logger.info(f"Return: {return_improvement:.2f}%")
    logger.info(f"Sharpe: {sharpe_improvement:.2f}%")
    logger.info(f"Win Rate: {win_rate_improvement:.2f} percentage points")
    
    # Plot equity curves if requested
    if plot_results:
        try:
            # Create a results directory if it doesn't exist
            os.makedirs('results', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Plot standard portfolio
            logger.info("Generating equity curve plot for standard signals")
            fig_standard = pf_standard.plot(title="Performance with Standard Signals", 
                                            plot_drawdowns=True, 
                                            plot_zloc=-0.3,
                                            plot_drawdown_kwargs=dict(plot_zones=True))
            fig_standard.write_image(f'results/standard_performance_{timestamp}.png')
            
            # Plot regime-aware portfolio
            logger.info("Generating equity curve plot for regime-aware signals")
            fig_regime = pf_regime.plot(title="Performance with Regime-Aware Signals", 
                                        plot_drawdowns=True, 
                                        plot_zloc=-0.3,
                                        plot_drawdown_kwargs=dict(plot_zones=True))
            fig_regime.write_image(f'results/regime_aware_performance_{timestamp}.png')
            
            # Use vectorbtpro's plots module to create a signal comparison chart
            logger.info("Generating trade signals visualization")
            
            # Format the signals data for display
            entries_data = pd.DataFrame({
                'Standard': long_entries_std.astype(int),
                'Regime-Aware': long_entries_regime.astype(int)
            })
            
            exits_data = pd.DataFrame({
                'Standard': long_exits_std.astype(int),
                'Regime-Aware': long_exits_regime.astype(int)
            })
            
            # Create and save signal comparison visualization
            import vectorbtpro as vbt
            fig_signals = vbt.Signals.plot(
                data_with_indicators['close'],
                entries_data, exits_data,
                title="Signal Comparison: Standard vs Regime-Aware",
                width=1000, height=500
            )
            fig_signals.write_image(f'results/signal_comparison_{timestamp}.png')
            
            logger.info(f"Plots saved to results directory with timestamp {timestamp}")
        except Exception as e:
            logger.error(f"Error generating plots: {str(e)}")
            logger.info("Continuing without visualization...")

        
        try:
            # Create a regime visualization using vectorbtpro
            logger.info("Generating regime visualization")
            
            # Create a column to identify regime type for coloring
            regime_column = pd.Series(
                data_with_indicators.index.map(
                    lambda idx: 'Trending' if regimes.loc[idx] in ('trending', 'strong_uptrend', 'weak_uptrend', 
                                                              'strong_downtrend', 'weak_downtrend') 
                             else 'Ranging'
                ),
                index=data_with_indicators.index,
                name='Regime'
            )
            
            # Create a trade visualization
            logger.info("Generating regime-based trade visualization")
            
            # Prepare data for visualization
            visualization_data = pd.DataFrame({
                'Close': data_with_indicators['close'],
                'Regime': regime_column,
                'StandardLongEntry': long_entries_std,
                'StandardLongExit': long_exits_std,
                'RegimeLongEntry': long_entries_regime,
                'RegimeLongExit': long_exits_regime,
                # Also include short signals if they exist
                'StandardShortEntry': short_entries_std,
                'StandardShortExit': short_exits_std,
                'RegimeShortEntry': short_entries_regime,
                'RegimeShortExit': short_exits_regime,
            })
            
            # Save the visualization data to a CSV for reference
            visualization_data.to_csv(f'results/regime_signals_data_{timestamp}.csv')
            
            logger.info("Regime and trade visualization data saved to file")
            logger.info("Note: Use vectorbtpro's Signals.plot to visualize this data interactively")
        except Exception as e:
            logger.error(f"Error generating regime visualization: {str(e)}")
            logger.info("Continuing without regime visualization...")

    
    # Return results dictionary
    return {
        'standard': {
            'return': stats_standard['Total Return [%]'],
            'sharpe': stats_standard.get('Sharpe Ratio', 0.0),
            'drawdown': stats_standard['Max Drawdown [%]'],
            'trades': pf_standard.trades.count(),
            'win_rate': stats_standard['Win Rate [%]']
        },
        'regime_aware': {
            'return': stats_regime['Total Return [%]'],
            'sharpe': stats_regime.get('Sharpe Ratio', 0.0),
            'drawdown': stats_regime['Max Drawdown [%]'],
            'trades': pf_regime.trades.count(),
            'win_rate': stats_regime['Win Rate [%]']
        },
        'improvement': {
            'return': return_improvement,
            'sharpe': sharpe_improvement,
            'win_rate': win_rate_improvement
        }
    }


def main():
    """Main function to run the regime-aware signal testing."""
    logger.info("Starting Regime-Aware Signal Test")
    
    # Generate sample data
    logger.info("Generating sample data with both trending and ranging regimes")
    sample_data = generate_sample_data(length=1000, trending_percentage=0.4)
    logger.info(f"Generated {len(sample_data)} data points")
    
    # Run comparison test
    results = run_comparison_test(sample_data, plot_results=True)
    
    # Display results
    logger.info("Test complete! Results saved to 'results' directory.")
    logger.info(f"Improvement summary: Return: {results['improvement']['return']:.2f}%, "
               f"Sharpe: {results['improvement']['sharpe']:.2f}%, "
               f"Win Rate: {results['improvement']['win_rate']:.2f} percentage points")
    
    return results


if __name__ == "__main__":
    main()
