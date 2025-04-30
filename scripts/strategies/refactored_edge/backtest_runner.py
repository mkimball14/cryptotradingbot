#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Backtest Runner for Edge Multi-Factor Strategy

This script runs backtests for the Edge Multi-Factor trading strategy using the
refactored modular components. It supports regime-aware signal generation and
loads real market data instead of using dummy data.

Author: Max Kimball
Date: 2025-04-29
"""

import vectorbtpro as vbt
import pandas as pd
import numpy as np
import sys
import os
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union, cast

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("backtest_runner")

# Add the project root to the path to ensure imports work correctly
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import refactored components
from scripts.strategies.refactored_edge.config import EdgeConfig
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.indicators import add_indicators
from scripts.strategies.refactored_edge.regime import determine_market_regime, determine_market_regime_advanced, MarketRegimeType
from scripts.strategies.refactored_edge.data.data_fetcher import fetch_historical_data
from scripts.strategies.refactored_edge.utils import validate_dataframe, with_error_handling
from scripts.strategies.refactored_edge.asset_profiles import get_asset_specific_config
from scripts.strategies.refactored_edge.wfo_utils import ensure_output_dir
from scripts.strategies.refactored_edge.validation_metrics import calculate_performance_metrics
from scripts.strategies.refactored_edge.position_sizing import calculate_integrated_position_size, get_regime_position_multiplier
# ==============================================================================
# Function Definitions
# ==============================================================================

def load_market_data(symbol: str, timeframe: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Load market data for backtesting from the data fetcher or from cached files.
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Data granularity (e.g., '1h', '4h', '1d')
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        
    Returns:
        DataFrame containing OHLCV data with DatetimeIndex
    """
    logger.info(f"Loading market data for {symbol} from {start_date} to {end_date}")
    
    try:
        # Try to fetch historical data
        data = fetch_historical_data(symbol, start_date, end_date, granularity=GRANULARITY_MAP_SECONDS.get(timeframe, 86400))
        
        # Check if data is None before validation
        if data is None:
            logger.error(f"Failed to fetch data for {symbol} from {start_date} to {end_date}")
            # Return a very small sample dataset for testing
            from scripts.strategies.refactored_edge.data.data_fetcher import create_sample_data
            return create_sample_data(start_date, end_date)
            
        # Validate that the data has required OHLCV columns
        validate_dataframe(data, required_cols=['open', 'high', 'low', 'close', 'volume'])
        logger.info(f"Successfully loaded {len(data)} data points for {symbol}")
        return data
    except Exception as e:
        logger.error(f"Error loading market data: {e}")
        # Return a very small sample dataset for testing
        from scripts.strategies.refactored_edge.data.data_fetcher import create_sample_data
        return create_sample_data(start_date, end_date)


def generate_regime_aware_signals(data: pd.DataFrame, config: EdgeConfig) -> Tuple[pd.Series, pd.Series]:
    """
    Generate regime-aware trading signals using the refactored signals_integration module.
    
    Args:
        data: DataFrame containing OHLCV data with all required indicators
        config: EdgeConfig instance with strategy parameters
        
    Returns:
        Tuple of (entry_signals, exit_signals) as pandas Series
    """
    logger.info("Generating regime-aware trading signals")
    
    try:
        # Extract necessary indicators
        close = data['close']
        
        # Make sure we have all required indicators
        required_indicators = ['rsi', 'bb_upper', 'bb_lower', 'trend_ma']
        if not all(indicator in data.columns for indicator in required_indicators):
            logger.info("Adding indicators to data")
            data = add_indicators(data, config)
            
        # Extract signals from integrated signal generator
        rsi = data['rsi']
        bb_upper = data['bb_upper']
        bb_lower = data['bb_lower']
        trend_ma = data['trend_ma']
        
        # Get demand/supply zones if available, otherwise use default False Series
        price_in_demand_zone = data.get('demand_zone', pd.Series(False, index=data.index))
        price_in_supply_zone = data.get('supply_zone', pd.Series(False, index=data.index))
        
        # Create parameters dictionary from config
        params = config.model_dump()
        
        # Perform regime detection if enabled
        if config.use_regime_filter:
            logger.info("Performing market regime detection")
            
            # Check if we have all required regime detection indicators
            required_regime_indicators = ['adx', 'plus_di', 'minus_di', 'atr']
            missing_indicators = [ind for ind in required_regime_indicators if ind not in data.columns]
            
            # Regime detection based on available indicators
            if missing_indicators:
                logger.warning(f"Missing indicators for advanced regime detection: {missing_indicators}")
                # Fallback to basic regime detection using just ADX if available
                if 'adx' in data.columns:
                    regime_series = determine_market_regime(data['adx'])
                    logger.info(f"Using basic regime detection with ADX")
                else:
                    logger.warning("ADX not available, defaulting to 'trending' regime")
                    regime_series = pd.Series('trending', index=data.index)
            else:
                # Use advanced regime detection with all available indicators
                regime_series = determine_market_regime_advanced(
                    adx=data['adx'],
                    plus_di=data['plus_di'],
                    minus_di=data['minus_di'],
                    atr=data['atr'],
                    close=data['close'],
                    high=data['high'],
                    low=data['low'],
                    volume=data['volume'] if 'volume' in data.columns else None
                )
                logger.info(f"Using advanced regime detection")
            
            # Calculate regime percentages and predominant regime
            from scripts.strategies.refactored_edge.utils import calculate_regime_percentages, determine_predominant_regime
            regime_percentages = calculate_regime_percentages(regime_series)
            predominant_regime = determine_predominant_regime(regime_percentages)
            
            # Create regime information dictionary
            regime_info = {
                'predominant_regime': predominant_regime,
                'trending_pct': regime_percentages.get('trending', 0),
                'ranging_pct': regime_percentages.get('ranging', 0),
                'regimes': regime_series
            }
            
            logger.info(f"Market regime: {predominant_regime} "  
                       f"(trending: {regime_percentages.get('trending', 0):.1f}%, "
                       f"ranging: {regime_percentages.get('ranging', 0):.1f}%)")
            
            # Add regime information to parameters
            params['_regime_info'] = regime_info
        else:
            # If not using regime filter, create a default 'trending' regime series
            regime_series = pd.Series('trending', index=data.index)
            logger.info("Regime filter disabled, using default 'trending' regime")
            
        # Generate signals using signals_integration
        logger.info(f"Generating signals with strictness={config.signal_strictness}, "
                    f"use_zones={config.use_zones}, use_regime_filter={config.use_regime_filter}")
        
        long_entries, long_exits, short_entries, short_exits = generate_signals(
            close=close,
            rsi=rsi,
            bb_upper=bb_upper,
            bb_lower=bb_lower,
            trend_ma=trend_ma,
            price_in_demand_zone=price_in_demand_zone,
            price_in_supply_zone=price_in_supply_zone,
            params=params
        )
        
        # Log signal counts for debugging
        logger.info(f"Raw signal counts - Long entries: {long_entries.sum()}, Long exits: {long_exits.sum()}, " +
                   f"Short entries: {short_entries.sum()}, Short exits: {short_exits.sum()}")
        
        # Combine long and short signals into single entry/exit signals
        # For simplicity in this backtest runner, we'll only use long signals
        # In a more advanced implementation, you might handle both directions
        entry_signals = long_entries
        exit_signals = long_exits
        
        # Ensure signals don't conflict (can't have entry and exit on same candle)
        # This is important for vectorbtpro portfolio performance
        conflict_mask = entry_signals & exit_signals
        if conflict_mask.any():
            logger.warning(f"Found {conflict_mask.sum()} conflicting entry/exit signals. Prioritizing exits.")
            entry_signals = entry_signals & ~conflict_mask
        
        signal_count = entry_signals.sum()
        logger.info(f"Generated {signal_count} entry signals")
        
        return entry_signals, exit_signals
    
    except Exception as e:
        logger.error(f"Error generating signals: {e}")
        raise


def run_backtest(
    symbol: str = 'BTC-USD', 
    timeframe: str = '1h',
    start_date: str = '2023-01-01',
    end_date: str = '2023-04-01',
    initial_capital: float = 10000.0,
    fees: float = 0.001,  # 0.1% trading fee
    use_regime_filter: bool = True,
    signal_strictness: SignalStrictness = SignalStrictness.BALANCED,
    use_dynamic_sizing: bool = True,  # Use the position sizing module
    risk_percentage: float = 0.01,    # 1% risk per trade
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a backtest for the Edge Multi-Factor strategy with regime-aware signal generation.
    
    Args:
        symbol: Trading symbol (e.g., 'BTC-USD')
        timeframe: Data granularity (e.g., '1h', '4h', '1d')
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        initial_capital: Initial capital for backtesting
        fees: Trading fees as a decimal (e.g., 0.001 = 0.1%)
        use_regime_filter: Whether to enable regime-aware signal adaptation
        signal_strictness: Strictness level for signal generation
        use_dynamic_sizing: Whether to use dynamic position sizing (True/False)
        risk_percentage: Risk percentage per trade (0.01 = 1%)
        output_dir: Directory to save backtest results (created if not existing)
        
    Returns:
        Dictionary containing backtest results and metrics
    """
    # Set default date range if not provided (last year)
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Ensure output directory exists
    output_dir = ensure_output_dir(output_dir)
    
    logger.info(f"\n--- Starting Backtest for {symbol} [{start_date} to {end_date}] --- ")
    logger.info(f"Using regime filter: {use_regime_filter}, Signal strictness: {signal_strictness}")
    
    try:
        # 1. Load market data
        data = load_market_data(symbol, timeframe, start_date, end_date)
        
        # 2. Get asset profile for this symbol to use optimized parameters
        asset_config = get_asset_specific_config(symbol)
        if asset_config:
            logger.info(f"Loaded asset profile for {symbol}")
        else:
            logger.warning(f"Could not load asset profile for {symbol}. Using default parameters.")
        
        # 3. Create configuration with proper parameters
        config = EdgeConfig(
            symbol=symbol,
            timeframe=timeframe,
            use_regime_filter=use_regime_filter,
            signal_strictness=signal_strictness
        )
        
        # Apply asset-specific parameters if profile exists
        if asset_config is not None:
            # Apply asset-specific parameters to config
            # For EdgeConfig, we need to set attributes directly
            # Common parameters we might want to apply from asset config
            config.signal_strictness = asset_config.signal_strictness
            config.trend_threshold_pct = asset_config.trend_threshold_pct
            config.zone_influence = asset_config.zone_influence
            config.min_hold_period = asset_config.min_hold_period
            logger.info(f"Applied asset-specific parameters from profile")
        
        # 4. Generate trading signals
        entry_signals, exit_signals = generate_regime_aware_signals(data, config)
        
        if entry_signals.sum() == 0:
            logger.warning("Strategy generated no entry signals. Backtest cannot proceed.")
            return {
                'success': False,
                'error': 'No entry signals generated'
            }
        
        # 5. Set up stop loss and take profit if configured
        sl_stop = getattr(config, 'stop_loss_pct', None)
        tp_stop = getattr(config, 'take_profit_pct', None)
        
        # 6. Create portfolio
        logger.info("Creating portfolio from signals...")
        
        # VectorBT has specific requirements for signal processing to create valid trades
        # We need to make sure our entry and exit signals work correctly
        
        # 1. Make sure we only have one entry at a time (important for vectorbtpro)
        entry_signals_adjusted = entry_signals.copy()
        exit_signals_adjusted = exit_signals.copy()
        
        # 2. Ensure we have an exit for every entry to close all positions
        # Add a final exit at the end if needed
        if entry_signals_adjusted.sum() > exit_signals_adjusted.sum():
            last_idx = exit_signals_adjusted.index[-1]
            exit_signals_adjusted.loc[last_idx] = True
            logger.info(f"Added final exit signal to close all positions")
            
        # 3. Remove any conflicting signals (entry and exit on same bar)
        conflict_mask = entry_signals_adjusted & exit_signals_adjusted
        if conflict_mask.any():
            logger.warning(f"Found {conflict_mask.sum()} conflicting entry/exit signals. Prioritizing exits.")
            entry_signals_adjusted = entry_signals_adjusted & ~conflict_mask
        
        # 4. Log adjusted signal counts for debugging
        logger.info(f"Creating portfolio with {entry_signals_adjusted.sum()} entries and {exit_signals_adjusted.sum()} exits")
        
        # 5. Get position sizing - fractional positions to use fixed percentage of capital per trade
        size = 0.95  # Use 95% of available capital per trade
        
        # Apply dynamic position sizing based on market regime and risk parameters
        try:
            # Initialize position sizes array with default values
            close_series = data['close']
            size_array = np.ones(len(close_series)) * 0.1  # Default size
            equity = initial_capital
            
            # Use position sizing module when enabled
            if use_dynamic_sizing:
                logger.info("Using dynamic position sizing based on regime and risk parameters")
                
                # Get relevant data for position sizing
                atr_data = data['atr'] if 'atr' in data.columns else None
                regime_data = data['regime'] if 'regime' in data.columns else None
                
                logger.info(f"Position sizing data: ATR available: {'atr' in data.columns}, Regime available: {'regime' in data.columns}")
                
                # Iterate through entry signals to set position sizes
                entry_indices = np.where(entry_signals)[0]
                
                for idx in entry_indices:
                    # Skip if we're at the last bar (no price data available)
                    if idx >= len(close_series) - 1:
                        continue
                    
                    # Get current regime and ATR
                    current_regime = regime_data.iloc[idx] if regime_data is not None else MarketRegimeType.RANGING
                    current_atr = atr_data.iloc[idx] if atr_data is not None else close_series.iloc[idx] * 0.02
                    
                    # Calculate position size
                    entry_price = close_series.iloc[idx]
                    # Use ATR for stop distance if no explicit stop provided
                    stop_distance = current_atr * 1.5
                    stop_price = entry_price - stop_distance
                    
                    # Get zone confidence from supply/demand zones if available
                    zone_confidence = 0.5
                    if 'price_in_demand_zone' in data.columns and entry_signals.iloc[idx]:
                        # If in demand zone during long entry, increase confidence
                        zone_confidence = 0.8 if data['price_in_demand_zone'].iloc[idx] else 0.5
                    elif 'price_in_supply_zone' in data.columns and exit_signals.iloc[idx]:
                        # If in supply zone during exit, increase confidence
                        zone_confidence = 0.8 if data['price_in_supply_zone'].iloc[idx] else 0.5
                    
                    # Calculate position size using the integrated approach
                    position_size = calculate_integrated_position_size(
                        equity=equity,
                        entry_price=entry_price,
                        atr=current_atr,
                        market_regime=current_regime,
                        risk_percentage=risk_percentage,
                        stop_loss_price=stop_price,
                        zone_confidence=zone_confidence
                    )
                    
                    # Update the position size for this entry
                    size_array[idx] = position_size
                    
                    # Log position sizing details for significant trades
                    if idx % 5 == 0:  # Log every 5th trade to avoid excessive output
                        logger.info(f"Trade #{idx}: Regime={current_regime}, Size={position_size:.4f}, "
                                  f"ATR={current_atr:.2f}, Zone confidence={zone_confidence:.2f}")
            
            # Create the portfolio with dynamic sizing
            portfolio = vbt.Portfolio.from_signals(
                close=close_series,
                entries=entry_signals_adjusted,
                exits=exit_signals_adjusted,
                size=size_array if use_dynamic_sizing else 1.0,  # Use dynamic sizing or fixed size
                price=close_series,
                init_cash=initial_capital,
                fees=fees,
                freq='1h'  # Assuming 1-hour data
            )
            logger.info(f"Portfolio created with {len(portfolio.trade_records) if hasattr(portfolio, 'trade_records') else 'unknown'} trades")
            if use_dynamic_sizing:
                logger.info(f"Using dynamic position sizing with {len(entry_indices)} entries")
        except Exception as e:
            logger.error(f"Error creating portfolio: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f"Portfolio creation failed: {str(e)}"
            }

        # Check if portfolio has trades
        if hasattr(portfolio, 'trades') and hasattr(portfolio.trades, 'records'):
            trade_count = len(portfolio.trades.records)
            if trade_count > 0:
                logger.info(f"Created portfolio with {trade_count} trades")
            else:
                logger.warning("Portfolio created but no trades were executed! Check signal quality.")
        else:
            logger.warning("Portfolio created but trades attribute not available.")
            
        # Debug signal distribution
        logger.debug(f"Signal distribution - Entries on: {entry_signals_adjusted[entry_signals_adjusted].index}, " 
                   f"Exits on: {exit_signals_adjusted[exit_signals_adjusted].index}")
        
        logger.info(f"Portfolio timeframe: {portfolio.wrapper.freq}")
        logger.info(f"First signal date: {entry_signals_adjusted[entry_signals_adjusted].index[0] if entry_signals_adjusted.any() else 'None'}")
        logger.info(f"Last signal date: {exit_signals_adjusted[exit_signals_adjusted].index[-1] if exit_signals_adjusted.any() else 'None'}")
        
        
        # 7. Analyze results
        logger.info("Calculating portfolio statistics...")
        stats = portfolio.stats()
        
        # 8. Extract key metrics
        metrics = {
            'total_return': stats['Total Return [%]'],
            'sharpe_ratio': stats['Sharpe Ratio'],
            'max_drawdown': stats['Max Drawdown [%]'],
            'win_rate': stats['Win Rate [%]'],
            'expectancy': stats.get('Expectancy [%]', 0.0),
            'total_trades': stats['Total Trades']
        }
        
        # 9. Generate plots and save to output directory
        try:
            logger.info("Generating and saving backtest plots...")
            # Portfolio returns plot
            returns_fig = portfolio.plot()
            returns_path = os.path.join(output_dir, f"{symbol}_{timeframe}_returns.html")
            returns_fig.write_html(returns_path)
            logger.info(f"Saved returns plot to {returns_path}")
            
            # Drawdown plot
            dd_fig = portfolio.plot_drawdowns(top_n=5)
            dd_path = os.path.join(output_dir, f"{symbol}_{timeframe}_drawdowns.html")
            dd_fig.write_html(dd_path)
            logger.info(f"Saved drawdowns plot to {dd_path}")
        except Exception as plot_err:
            logger.warning(f"Could not generate plots: {plot_err}")
        # 10. Calculate additional performance metrics
        additional_metrics = calculate_performance_metrics(portfolio)
        metrics.update(additional_metrics)
        
        # Display and save backtest results
        logger.info("\n--- Backtest Results ---")
        logger.info(f"Symbol: {symbol}, Timeframe: {timeframe}")
        logger.info(f"Period: {start_date} to {end_date}")
        logger.info(f"Regime Filter: {use_regime_filter}, Signal Strictness: {signal_strictness}")
        
        # Get raw stats from portfolio for more accurate metrics
        try:
            # Extract stats directly from portfolio to ensure accuracy
            portfolio_stats = portfolio.stats() if hasattr(portfolio, 'stats') and callable(portfolio.stats) else {}
            # Fall back to calculated metrics if needed
            total_return = portfolio_stats.get('Total Return [%]', metrics.get('total_return', 0.0))
            sharpe_ratio = portfolio_stats.get('Sharpe Ratio', metrics.get('sharpe_ratio', 0.0))
            max_drawdown = portfolio_stats.get('Max Drawdown [%]', metrics.get('max_drawdown', 0.0))
            win_rate = portfolio_stats.get('Win Rate [%]', metrics.get('win_rate', 0.0))
            trade_count = len(portfolio.trades.records) if hasattr(portfolio, 'trades') and hasattr(portfolio.trades, 'records') else metrics.get('total_trades', 0)
            
            # Log the detailed metrics
            logger.info(f"Total Return: {total_return:.2f}%")
            logger.info(f"Sharpe Ratio: {sharpe_ratio:.2f}")
            logger.info(f"Max Drawdown: {max_drawdown:.2f}%")
            logger.info(f"Win Rate: {win_rate:.2f}%")
            logger.info(f"Total Trades: {trade_count}")
            
            # Update performance metrics with the correct values for CSV export
            metrics['total_return'] = total_return
            metrics['sharpe_ratio'] = sharpe_ratio
            metrics['max_drawdown'] = max_drawdown
            metrics['win_rate'] = win_rate
            metrics['total_trades'] = trade_count
        except Exception as e:
            # Fall back to calculated metrics if something goes wrong
            logger.warning(f"Error accessing direct portfolio stats: {e}. Using calculated metrics instead.")
            logger.info(f"Total Return: {metrics.get('total_return', 0.0):.2f}%")
            logger.info(f"Sharpe Ratio: {metrics.get('sharpe_ratio', 0.0):.2f}")
            logger.info(f"Max Drawdown: {metrics.get('max_drawdown', 0.0):.2f}%")
            logger.info(f"Win Rate: {metrics.get('win_rate', 0.0):.2f}%")
            logger.info(f"Total Trades: {metrics.get('total_trades', 0)}")
        
        # Log additional metrics if available
        if 'avg_win' in metrics and metrics['avg_win'] != 0.0:
            logger.info(f"Avg Win: {metrics.get('avg_win', 0.0):.2f}%")
            logger.info(f"Avg Loss: {metrics.get('avg_loss', 0.0):.2f}%")
            logger.info(f"Profit Factor: {metrics.get('profit_factor', 0.0):.2f}")
            
        # 12. Save results to CSV
        results_df = pd.DataFrame([metrics])
        results_path = os.path.join(output_dir, f"{symbol}_{timeframe}_backtest_results.csv")
        results_df.to_csv(results_path, index=False)
        logger.info(f"Saved results to {results_path}")
        
        # Return results
        return {
            'success': True,
            'metrics': metrics,
            'portfolio': portfolio,
            'config': config.model_dump(),
            'signals': {
                'entries': entry_signals,
                'exits': exit_signals
            },
            'output_paths': {
                'results': results_path,
                'returns_plot': returns_path if 'returns_path' in locals() else None,
                'drawdowns_plot': dd_path if 'dd_path' in locals() else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error during backtest execution: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e)
        }


# ==============================================================================
# Main Execution
# ==============================================================================

if __name__ == "__main__":
    logger.info("Starting Edge Multi-Factor Strategy Backtest Runner")
    
    # Import GRANULARITY_MAP_SECONDS from data_fetcher
    from scripts.strategies.refactored_edge.data.data_fetcher import GRANULARITY_MAP_SECONDS
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Edge Multi-Factor Strategy Backtest Runner')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Trading symbol (e.g., BTC-USD)')
    parser.add_argument('--timeframe', type=str, default='1h', help='Data granularity (e.g., 1h, 4h, 1d)')
    parser.add_argument('--start_date', type=str, help='Start date in format YYYY-MM-DD')
    parser.add_argument('--end_date', type=str, help='End date in format YYYY-MM-DD')
    parser.add_argument('--use_regime_filter', type=lambda x: x.lower() == 'true', default=True, 
                        help='Whether to use regime filter (True/False)')
    parser.add_argument('--initial_capital', type=float, default=10000.0, help='Initial capital for backtest')
    parser.add_argument('--use_dynamic_sizing', type=lambda x: x.lower() == 'true', default=True,
                        help='Whether to use dynamic position sizing (True/False)')
    parser.add_argument('--risk_percentage', type=float, default=0.01,
                        help='Risk percentage per trade (0.01 = 1%)')
    
    args = parser.parse_args()
    
    # Set default dates if not provided
    if not args.end_date:
        args.end_date = datetime.now().strftime('%Y-%m-%d')
    if not args.start_date:
        args.start_date = (datetime.strptime(args.end_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
    
    logger.info(f"Parameters: Symbol={args.symbol}, Timeframe={args.timeframe}, "  
               f"Dates={args.start_date} to {args.end_date}, Regime Filter={args.use_regime_filter}")
    
    # Run backtest with regime-aware signal generation
    results = run_backtest(
        symbol=args.symbol,
        timeframe=args.timeframe,
        start_date=args.start_date,
        end_date=args.end_date,
        initial_capital=args.initial_capital,
        use_regime_filter=args.use_regime_filter,
        signal_strictness=SignalStrictness.BALANCED,
        use_dynamic_sizing=args.use_dynamic_sizing,
        risk_percentage=args.risk_percentage
    )
    
    if results['success']:
        logger.info("--- Backtest Runner Finished Successfully ---")
    else:
        logger.error(f"--- Backtest Failed: {results.get('error', 'Unknown error')} ---")
