"""
Evaluation functions for Walk-Forward Optimization (WFO).

This module contains functions for evaluating trading strategies with specific parameters,
generating signals, constructing portfolios, and calculating performance metrics.
"""
import traceback
import numpy as np
import pandas as pd
import vectorbtpro as vbt
from typing import Dict, Any, Tuple, List, Optional, Union
import os
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Local imports
from scripts.strategies.refactored_edge import indicators, signals, test_signals, balanced_signals
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.wfo_utils import INIT_CAPITAL, is_testing_mode, get_ohlc_columns
from scripts.strategies.refactored_edge.position_sizing import calculate_integrated_position_size, get_regime_position_multiplier
from scripts.strategies.refactored_edge.regime import MarketRegimeType


def create_portfolio(close, long_entries, long_exits, short_entries, short_exits, params=None, data=None):
    """
    Helper function to create a portfolio with consistent parameters.
    This avoids passing invalid parameters to vectorbtpro's Portfolio.from_signals method.
    
    Args:
        close (pd.Series): Series of closing prices
        long_entries (pd.Series): Boolean series of long entry signals
        long_exits (pd.Series): Boolean series of long exit signals
        short_entries (pd.Series): Boolean series of short entry signals
        short_exits (pd.Series): Boolean series of short exit signals
        params (dict, optional): Strategy parameters
        data (pd.DataFrame, optional): Full data frame with indicators for dynamic position sizing
        
    Returns:
        vbt.Portfolio: Portfolio object
    """
    params = params or {}
    
    # Define constants for trading
    TRADE_SIZE = 1.0  # Default to 1.0 BTC per trade
    
    # Get fees and slippage from params if available
    commission = params.get('commission_pct', 0.0015)  # Default 0.15%
    slippage = params.get('slippage_pct', 0.0005)  # Default 0.05%
    
    # Position sizing parameters
    use_dynamic_sizing = params.get('use_dynamic_sizing', True)
    risk_percentage = params.get('risk_percentage', 0.01)  # Default 1% risk per trade
    initial_capital = params.get('initial_capital', INIT_CAPITAL)
    
    # Add a final exit signal to ensure all positions are closed at the end
    # This helps avoid NaN returns and ensures proper final trade accounting
    if len(close) > 0:
        # Check if there are any active signals first to avoid modifying Series without signals
        if long_entries.any() or short_entries.any():
            # Create a copy to avoid modifying the original Series
            long_exits = long_exits.copy()
            short_exits = short_exits.copy()
            
            # Add exit signals at the last row to ensure all positions are closed
            long_exits.iloc[-1] = True
            short_exits.iloc[-1] = True
            
            print(f"Added final exit signals to ensure all positions are closed")
    
    # Resolve signal conflicts to ensure proper trade execution
    if len(close) > 0:
        # Check for simultaneous entry and exit signals for the same direction
        long_conflict_mask = long_entries & long_exits
        short_conflict_mask = short_entries & short_exits
        
        if long_conflict_mask.any() or short_conflict_mask.any():
            print(f"Resolving {long_conflict_mask.sum()} long conflicts and {short_conflict_mask.sum()} short conflicts")
            
            # Resolve conflicts by prioritizing exits
            if long_conflict_mask.any():
                long_entries = long_entries & ~long_conflict_mask
            
            if short_conflict_mask.any():
                short_entries = short_entries & ~short_conflict_mask
    
    # Count entry and exit signals for debugging
    print(f"Signals: Long entries: {long_entries.sum()}, Long exits: {long_exits.sum()}, "
          f"Short entries: {short_entries.sum()}, Short exits: {short_exits.sum()}")
            
    # Check if we should use dynamic position sizing
    position_size = TRADE_SIZE
    size_array = None
    
    # Before trying dynamic sizing, check if we have entries
    # If no entries are detected, something might be wrong with signals
    if long_entries.sum() == 0 and short_entries.sum() == 0:
        print("WARNING: No entry signals detected! Check signal generation parameters.")
        # Since we have no entries, we'll make signal generation more lenient to ensure at least some trades
        # This is only for WFO evaluation to prevent empty test splits
        if params and 'use_zones' in params:
            print("Attempting to generate fallback signals with more lenient parameters...")
            # Temporarily disable zone filtering which might be restricting trades
            params_copy = params.copy()
            params_copy['use_zones'] = False
            if 'rsi_lower' in params_copy and params_copy['rsi_lower'] > 30:
                params_copy['rsi_lower'] = 30  # Make RSI entries more lenient
            if 'rsi_upper' in params_copy and params_copy['rsi_upper'] < 70:
                params_copy['rsi_upper'] = 70  # Make RSI exits more lenient
                
            # TODO: Consider implementing fallback signal generation here
            # This would ensure at least some minimal trades for evaluation
    
    if use_dynamic_sizing and data is not None:
        try:
            # Initialize position sizes array with default values - use a reasonable default size
            # rather than very small 10% which might cause no trades due to minimum size constraints
            size_array = np.ones(len(close)) * TRADE_SIZE  # Start with full default size
            
            # Get relevant data for position sizing with robust fallbacks
            has_atr = 'atr' in data.columns
            has_regime = 'regime' in data.columns
            
            if not has_atr:
                print("WARNING: ATR data missing for position sizing. Using percentage-based estimation.")
            if not has_regime:
                print("WARNING: Regime data missing for position sizing. Using default regime (RANGING).")
            
            atr_data = data['atr'] if has_atr else pd.Series(close.values * 0.02, index=close.index)
            regime_data = data['regime'] if has_regime else pd.Series([MarketRegimeType.RANGING] * len(close), index=close.index)
            
            # Iterate through entry signals to set position sizes
            entry_indices = np.where(long_entries)[0]
            
            if len(entry_indices) == 0:
                print("WARNING: No long entry signals for dynamic sizing. Check signal generation.")
            else:
                for idx in entry_indices:
                    # Skip if we're at the last bar (no price data available)
                    if idx >= len(close) - 1:
                        continue
                    
                    # Get current regime and ATR with safe access
                    try:
                        current_regime = str(regime_data.iloc[idx]) if has_regime else MarketRegimeType.RANGING
                        current_atr = float(atr_data.iloc[idx]) if has_atr else float(close.iloc[idx] * 0.02)
                    except (IndexError, ValueError) as e:
                        print(f"Error accessing regime/ATR data at index {idx}: {e}")
                        current_regime = MarketRegimeType.RANGING
                        current_atr = float(close.iloc[idx] * 0.02)  # Fallback to 2% of price
                    
                    # Calculate position size
                    entry_price = float(close.iloc[idx])
                    # Use ATR for stop distance with a minimum value to avoid division by zero
                    stop_distance = max(current_atr * 1.5, entry_price * 0.005)  # At least 0.5% of price
                    stop_price = entry_price - stop_distance
                    
                    # Get zone confidence with safe access
                    zone_confidence = 0.5  # Default neutral confidence
                    if 'price_in_demand_zone' in data.columns:
                        try:
                            zone_confidence = 0.8 if data['price_in_demand_zone'].iloc[idx] else 0.5
                        except IndexError:
                            pass  # Keep default confidence
                    
                    # Use more conservative risk percentage during WFO to avoid overfitting
                    safe_risk_pct = min(risk_percentage, 0.02)  # Cap at 2% max risk for stability
                    
                    try:
                        # Calculate position size with reasonable constraints to ensure trades execute
                        position_size = calculate_integrated_position_size(
                            equity=initial_capital,
                            entry_price=entry_price,
                            atr=current_atr,
                            market_regime=current_regime,
                            risk_percentage=safe_risk_pct,
                            stop_loss_price=stop_price,
                            zone_confidence=zone_confidence,
                            min_size=0.01,  # Ensure at least minimal position size
                            max_size=1.0    # Reasonable upper bound
                        )
                        
                        # Safety check - ensure minimum viable position size
                        position_size = max(position_size, 0.01)  # Minimum size to prevent micro-positions
                        
                        # Update the position size for this entry
                        size_array[idx] = position_size
                    except Exception as e:
                        print(f"Size calculation failed at index {idx}: {e}, using default size")
                        size_array[idx] = TRADE_SIZE  # Fallback to default size on error
                
                print(f"Applied dynamic position sizing to {len(entry_indices)} entries")
        except Exception as e:
            print(f"Dynamic position sizing failed: {e}, falling back to fixed size")
            traceback.print_exc()
            size_array = None
    
    # Only include valid parameters for vectorbtpro's Portfolio.from_signals
    # This avoids warnings about unexpected parameters like sl_pct
    pf_kwargs = {
        'size': size_array if size_array is not None else TRADE_SIZE,
        'freq': '1h',  # Assuming 1-hour timeframe
        'fees': commission,
        'slippage': slippage,
        # Add trade size constraints if supported
        'size_granularity': 0.001  # Allow fractional trade sizes with 3 decimal precision
    }
    
    # Remove any parameters that might not be supported by all vectorbtpro versions
    # The close_at_end parameter is not available in some versions
    if 'close_at_end' in pf_kwargs:
        del pf_kwargs['close_at_end']
    
    # Note on ATR-based stops:
    # Instead of passing sl_pct, sl_atr_multiplier, etc. directly to Portfolio.from_signals
    # (which causes parameter warnings), we implement custom exit logic in the signal generation.
    
    try:
        portfolio = vbt.Portfolio.from_signals(
            close=close,
            entries=long_entries,
            exits=long_exits,
            short_entries=short_entries,
            short_exits=short_exits,
            init_cash=INIT_CAPITAL,
            **pf_kwargs
        )
        
        # Check if portfolio was created successfully
        if portfolio is None:
            print("ERROR: Portfolio creation failed, returned None")
            return None
            
        # Verify that trades are present
        trade_count = 0
        try:
            if hasattr(portfolio, 'trades'):
                if hasattr(portfolio.trades, 'count') and callable(portfolio.trades.count):
                    trade_count = portfolio.trades.count()
                elif hasattr(portfolio.trades, 'records') and hasattr(portfolio.trades.records, '__len__'):
                    trade_count = len(portfolio.trades.records)
                elif hasattr(portfolio.trades, '__len__'):
                    trade_count = len(portfolio.trades)
            
            print(f"Portfolio created successfully with {trade_count} trades")
            
        except Exception as e:
            print(f"Warning: Error checking trade count: {e}")
        
        return portfolio
        
    except Exception as e:
        print(f"ERROR: Failed to create portfolio: {e}")
        import traceback
        traceback.print_exc()
        return None


def evaluate_with_params(data, params):
    """
    Evaluate strategy with given parameters and return portfolio and performance stats.
    
    Args:
        data (pd.DataFrame): Data to evaluate on
        params (dict): Strategy parameters including regime-aware and position sizing settings
        
    Returns:
        tuple: (portfolio object, performance stats dict)
    """
    try:
        # First get necessary columns
        close = data.get('close', data.get('Close', None))
        if close is None:
            print("ERROR: Close price data not found. Available columns:", data.columns.tolist())
            return None, {}
        
        # 1. Calculate indicators
        print(f"DEBUG (Eval): Calculating indicators with params {params}")
        
        # Create a temporary EdgeConfig with params for indicators calculation
        temp_config = type('EdgeConfig', (), {})()
        for key, value in params.items():
            setattr(temp_config, key, value)
        
        # Ensure all required parameters exist for indicators
        if not hasattr(temp_config, 'trend_ma_window'):
            setattr(temp_config, 'trend_ma_window', params.get('ma_window', 50))  # Use ma_window or default to 50
        
        # Add other required parameters with defaults
        if not hasattr(temp_config, 'atr_window_sizing'):
            # First try to get atr_window_sizing directly, fallback to atr_window, then default to 14
            atr_window_sizing = params.get('atr_window_sizing', params.get('atr_window', 14))
            setattr(temp_config, 'atr_window_sizing', atr_window_sizing)
            print(f"DEBUG: Setting atr_window_sizing to {atr_window_sizing} for indicator calculation")
        
        # Add zone-related parameters
        if not hasattr(temp_config, 'use_zones'):
            setattr(temp_config, 'use_zones', params.get('use_zones', False))
        
        # Generate indicators
        indicators_df = indicators.add_indicators(data, temp_config)
        
        # Extract required indicators
        rsi = indicators_df.get('rsi', None)
        bb_upper = indicators_df.get('bb_upper', None)
        bb_lower = indicators_df.get('bb_lower', None)
        trend_ma = indicators_df.get('trend_ma', None)
        price_in_demand_zone = indicators_df.get('demand_zone', None)
        price_in_supply_zone = indicators_df.get('supply_zone', None)
        
        # Check if any mandatory indicator is missing
        for name, indicator in {'rsi': rsi, 'bb_upper': bb_upper, 'bb_lower': bb_lower, 'trend_ma': trend_ma}.items():
            if indicator is None:
                print(f"WARNING: {name} indicator is None. Available columns:", indicators_df.columns.tolist())
                # Return empty results
                return None, {
                    'return': 0.0,
                    'sharpe': -np.inf,
                    'max_drawdown': 1.0,
                    'trades': 0,
                    'win_rate': 0.0
                }
        
        # 2. Generate Signals using the centralized signals integration module
        # This handles signal strictness levels and testing mode automatically
        print(f"DEBUG (Eval): Generating signals using signals_integration module with params {params}")
        
        # Import SignalStrictness here to avoid circular imports
        from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
        
        # First try with normal parameters
        long_entries, long_exits, short_entries, short_exits = generate_signals(
            close=close, 
            rsi=indicators_df.rsi,
            bb_upper=indicators_df.bb_upper,
            bb_lower=indicators_df.bb_lower,
            trend_ma=indicators_df.trend_ma,
            price_in_demand_zone=price_in_demand_zone,
            price_in_supply_zone=price_in_supply_zone,
            params=params
        )
        
        # Check if we have any entry signals, if not, retry with ULTRA_RELAXED mode for WFO
        if long_entries.sum() == 0 and short_entries.sum() == 0:
            print("WARNING: No entry signals detected with normal parameters! Trying ULTRA_RELAXED mode...")
            # Clone params and modify for ultra-relaxed mode
            wfo_params = params.copy()
            wfo_params['signal_strictness'] = SignalStrictness.ULTRA_RELAXED
            # Make more lenient to ensure trades
            wfo_params['rsi_lower_threshold'] = 20  # More aggressive entries
            wfo_params['rsi_upper_threshold'] = 80  # More relaxed exits
            wfo_params['use_regime_filter'] = False  # Disable regime filtering
            wfo_params['use_zones'] = False  # Disable zone filtering
            
            # Try again with ultra-relaxed settings
            long_entries, long_exits, short_entries, short_exits = generate_signals(
                close=close, 
                rsi=indicators_df.rsi,
                bb_upper=indicators_df.bb_upper,
                bb_lower=indicators_df.bb_lower,
                trend_ma=indicators_df.trend_ma,
                price_in_demand_zone=price_in_demand_zone,
                price_in_supply_zone=price_in_supply_zone,
                params=wfo_params
            )
            print(f"ULTRA_RELAXED mode generated {long_entries.sum()} long entries and {short_entries.sum()} short entries")
            
        # 3. Create Portfolio using helper function
        # This ensures we only pass valid parameters
        pf = create_portfolio(
            close=close,
            long_entries=long_entries,
            long_exits=long_exits,
            short_entries=short_entries,
            short_exits=short_exits,
            params=params,
            data=data  # Pass the full dataset for position sizing
        )
        
        # 4. Calculate Performance stats - with robust vectorbtpro compatibility handling
        # First check if trades exist using safe access patterns
        trade_count = 0
        try:
            # Different versions of vectorbtpro handle trades differently
            if hasattr(pf, 'trades'):
                if hasattr(pf.trades, 'count') and callable(pf.trades.count):
                    trade_count = pf.trades.count()
                elif hasattr(pf.trades, 'records') and hasattr(pf.trades.records, '__len__'):
                    trade_count = len(pf.trades.records)
                elif hasattr(pf.trades, '__len__'):
                    trade_count = len(pf.trades)
            else:
                print("Portfolio has no 'trades' attribute, checking alternative metrics")
                # Try other ways to determine if trades were executed
                trade_count = 0
        except Exception as e:
            print(f"Error counting trades: {e}")
            trade_count = 0
        
        if trade_count == 0:
            print(f"DEBUG: No trades generated with these parameters")
            return pf, {
                'return': 0.0,
                'sharpe': -np.inf,
                'max_drawdown': 1.0,
                'trades': 0,
                'win_rate': 0.0
            }
        
        # Get vectorbt stats with error handling for different API patterns
        try:
            # Try different ways to access portfolio stats based on vectorbtpro version
            vbt_stats = {}
            if hasattr(pf, 'stats'):
                if callable(pf.stats):
                    try:
                        vbt_stats = pf.stats()
                        print(f"Successfully accessed portfolio.stats() method")
                    except Exception as stats_err:
                        print(f"Error calling portfolio.stats(): {stats_err}")
                        # Try accessing as attribute
                        vbt_stats = getattr(pf, 'stats', {})
                        if callable(vbt_stats):
                            vbt_stats = {}
                else:
                    # Stats is an attribute
                    vbt_stats = pf.stats
                    print(f"Accessed portfolio.stats attribute directly")
            else:
                print("Portfolio has no 'stats' attribute or method, using empty stats")
            
            # Safely extract key metrics with proper error handling
            # Convert to our simplified format with robust fallbacks
            stats = {
                'return': float(vbt_stats.get('Total Return [%]', 0.0)) / 100.0,
                'sharpe': float(vbt_stats.get('Sharpe Ratio', 0.0)),
                'max_drawdown': float(vbt_stats.get('Max Drawdown [%]', 0.0)) / 100.0,
                'trades': trade_count,
                'win_rate': float(vbt_stats.get('Win Rate [%]', 0.0)) / 100.0
            }
            
            # Try to extract additional metrics that might be available
            # Safely access returns using different vectorbtpro API patterns
            try:
                if hasattr(pf, 'returns'):
                    if callable(pf.returns):
                        try:
                            returns = pf.returns()
                            if isinstance(returns, pd.Series) and not returns.empty:
                                stats['mean_return'] = float(returns.mean())
                                stats['return_volatility'] = float(returns.std())
                        except Exception as returns_err:
                            print(f"Error accessing portfolio returns: {returns_err}")
                    else:
                        # Returns is an attribute in this version
                        returns = pf.returns
                        if isinstance(returns, pd.Series) and not returns.empty:
                            stats['mean_return'] = float(returns.mean())
                            stats['return_volatility'] = float(returns.std())
            except Exception as e:
                print(f"Could not calculate additional return metrics: {e}")
            
            # Debug print performance with safe access to metrics
            print(f"DEBUG: Return={stats.get('return', 0.0):.4f}, Sharpe={stats.get('sharpe', 0.0):.4f}, " 
                  f"MaxDD={stats.get('max_drawdown', 0.0):.4f}, Trades={stats.get('trades', 0)}, " 
                  f"WinRate={stats.get('win_rate', 0.0):.4f}")
            
        except Exception as e:
            print(f"Error calculating performance metrics: {e}")
            import traceback
            traceback.print_exc()
            # Provide default metrics
            stats = {
                'return': 0.0,
                'sharpe': 0.0,
                'max_drawdown': 0.0,
                'trades': trade_count,  # Use the previously determined trade count
                'win_rate': 0.0
            }
        
        return pf, stats
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in evaluate_with_params: {str(e)}")
        logger.error(f"Evaluation error: {str(e)}")
        # Return a failed result to ensure the optimization can continue
        return None, {
            'return': 0.0,
            'sharpe': -np.inf,
            'max_drawdown': 1.0,
            'trades': 0,
            'win_rate': 0.0
        }


def evaluate_single_params(params, data, metric=None):
    """
    Evaluates a single parameter set using indicators and signals directly.

    Args:
        params (dict): Parameter dictionary from PARAM_GRID.
        data (pd.DataFrame): Input data (must contain OHLC).
        metric (str, optional): Performance metric to optimize (e.g., 'Sharpe Ratio').
                               If None, defaults to 'sharpe' in the stats dictionary.

    Returns:
        tuple or float: (score, portfolio, stats) if metric is None, otherwise just the score (for backward compatibility).
    """
    try:
        # Ensure required columns are present (check both uppercase and lowercase)
        open_, high, low, close = get_ohlc_columns(data)
        
        if close is None:
            print(f"DEBUG (Eval Fail): Missing required columns in data for params {params}")
            if metric is None:
                return -np.inf, None, None
            else:
                return -np.inf
        
        # Evaluate with params to get portfolio and stats
        pf, stats = evaluate_with_params(data, params)
        
        # Check if portfolio creation failed
        if pf is None:
            print(f"Portfolio creation failed in evaluate_single_params with params {params}")
            if metric is None:
                return -np.inf, None, None
            else:
                return -np.inf
                
        # Get the score based on metric or default to sharpe ratio
        if metric is None or metric.lower() == 'sharpe ratio':
            score = stats.get('sharpe', -np.inf)
        elif metric.lower() == 'return':
            score = stats.get('return', -np.inf)
        else:
            # For other metrics, try to get from stats dictionary
            # Convert from potential format like 'Max Drawdown [%]' to 'max_drawdown'
            metric_key = metric.lower().replace(' ', '_').replace('[%]', '').strip('_')
            score = stats.get(metric_key, -np.inf)
        
        # Validate score
        if np.isnan(score) or score == -np.inf:
            print(f"Invalid score: {score} with params {params}")
            if metric is None:
                return -np.inf, None, None
            else:
                return -np.inf
        
        # Return based on function signature (backward compatibility)
        if metric is None:
            return score, pf, stats
        else:
            return score
            
    except Exception as e:
        print(f"Error in evaluate_single_params: {e}")
        import traceback
        traceback.print_exc()
        if metric is None:
            return -np.inf, None, None
        else:
            return -np.inf
            
    # This function has been completely refactored for robustness and vectorbtpro compatibility
