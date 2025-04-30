"""
Evaluation functions for Walk-Forward Optimization (WFO).

This module contains functions for evaluating trading strategies with specific parameters,
generating signals, constructing portfolios, and calculating performance metrics.
"""
import traceback
import pandas as pd
import numpy as np
import vectorbtpro as vbt

# Local imports
from scripts.strategies.refactored_edge import indicators, signals, test_signals, balanced_signals
from scripts.strategies.refactored_edge.balanced_signals import SignalStrictness
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.wfo_utils import INIT_CAPITAL, is_testing_mode, get_ohlc_columns


def create_portfolio(close, long_entries, long_exits, short_entries, short_exits, params=None):
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
        
    Returns:
        vbt.Portfolio: Portfolio object
    """
    params = params or {}
    
    # Define constants for trading
    TRADE_SIZE = 1.0  # Default to 1.0 BTC per trade
    
    # Get fees and slippage from params if available
    commission = params.get('commission_pct', 0.0015)  # Default 0.15%
    slippage = params.get('slippage_pct', 0.0005)  # Default 0.05%
    
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
            
    # Only include valid parameters for vectorbtpro's Portfolio.from_signals
    # This avoids warnings about unexpected parameters like sl_pct
    pf_kwargs = {
        'size': TRADE_SIZE,
        'freq': '1h',  # Assuming 1-hour timeframe
        'fees': commission,
        'slippage': slippage,
        # Ensure close positions at the end even without explicit signals
        'close_at_end': True,  
        # Add trade size constraints
        'size_granularity': 0.001  # Allow fractional trade sizes with 3 decimal precision
    }
    
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
        params (dict): Strategy parameters
        
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
        print(f"DEBUG: Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries")
        
        # 3. Create Portfolio using helper function
        # This ensures we only pass valid parameters to avoid warnings
        pf = create_portfolio(
            close=close,
            long_entries=long_entries,
            long_exits=long_exits,
            short_entries=short_entries,
            short_exits=short_exits,
            params=params
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
        traceback.print_exc()
        print(f"Error in evaluate_with_params: {str(e)}")
        return None, {
            'return': 0.0,
            'sharpe': -np.inf,
            'max_drawdown': 1.0,
            'trades': 0,
            'win_rate': 0.0
        }


def evaluate_single_params(params, data, metric):
    """
    Evaluates a single parameter set using indicators and signals directly.

    Args:
        params (dict): Parameter dictionary from PARAM_GRID.
        data (pd.DataFrame): Input data (must contain OHLC).
        metric (str): Performance metric to optimize (e.g., 'Sharpe Ratio').

    Returns:
        float or None: The performance score (metric value) or None if error.
    """
    try:
        # Ensure required columns are present (check both uppercase and lowercase)
        open_, high, low, close = get_ohlc_columns(data)
        
        if close is None:
            print(f"DEBUG (Eval Fail): Missing required columns in data for params {params}")
            return -np.inf
            
        # 1. Calculate indicators with params
        print(f"DEBUG (Eval): Calculating indicators with params {params}")
            
        # Create a temporary EdgeConfig with params
        temp_config = type('EdgeConfig', (), {})()
        for key, value in params.items():
            setattr(temp_config, key, value)
            
        # Map essential parameters
        if not hasattr(temp_config, 'rsi_lower_threshold'):
            setattr(temp_config, 'rsi_lower_threshold', params.get('rsi_entry_threshold', 30))
            
        if not hasattr(temp_config, 'rsi_upper_threshold'):
            setattr(temp_config, 'rsi_upper_threshold', params.get('rsi_exit_threshold', 70))
        
        # Ensure trend_ma_window is set correctly     
        if not hasattr(temp_config, 'trend_ma_window'):
            setattr(temp_config, 'trend_ma_window', params.get('ma_window', 50))
            
        # Create the indicator DataFrame
        try:
            indicators_df = indicators.add_indicators(data, temp_config)
            rsi = indicators_df.get('rsi') 
            bb_upper = indicators_df.get('bb_upper')
            bb_lower = indicators_df.get('bb_lower')
            trend_ma = indicators_df.get('trend_ma')
            price_in_demand_zone = indicators_df.get('demand_zone', None)
            price_in_supply_zone = indicators_df.get('supply_zone', None)
        except Exception as e:
            print(f"DEBUG (Eval Fail): Error calculating indicators: {e}")
            return -np.inf
            
        # Check if any required indicator is missing - proper pandas check
        missing_indicators = []
        for name, indicator in {'rsi': rsi, 'bb_upper': bb_upper, 'bb_lower': bb_lower, 'trend_ma': trend_ma}.items():
            if indicator is None or (hasattr(indicator, 'empty') and indicator.empty):
                missing_indicators.append(name)
                
        if missing_indicators:
            print(f"DEBUG (Eval Fail): Missing indicators for params {params}")
            print(f"Missing indicators: {missing_indicators}")
            return -np.inf

        # 2. Generate Signals using the centralized signals integration module
        # This handles signal strictness levels and testing mode automatically
        print(f"DEBUG (Eval): Generating signals using signals_integration module with params {params}")
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
        print(f"DEBUG: Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries")
            
        # 3. Create Portfolio using helper function
        # This ensures we only pass valid parameters to avoid warnings
        pf = create_portfolio(
            close=close,
            long_entries=long_entries,
            long_exits=long_exits,
            short_entries=short_entries,
            short_exits=short_exits,
            params=params
        )

        # Check if any trades were made
        if pf.trades.count() == 0:
            print(f"DEBUG (Eval Fail): No trades for params {params}")
            return -np.inf # Penalize heavily if no trades
        
        # 4. Calculate Performance
        performance_stats = pf.stats()
        score = performance_stats.get(metric)
        
        # Check for NaN or infinite scores
        if score is None or not np.isfinite(score):
            print(f"DEBUG (Eval Fail): Invalid score ({score}) for metric '{metric}' with params {params}")
            return -np.inf

        # Check if we're running in testing mode (via environment variable)
        testing_mode = is_testing_mode()
        
        # Optional: Apply constraints (minimum trades, acceptable drawdown)
        MIN_TOTAL_TRADES = 5 if not testing_mode else 1  # Reduced minimum trades in testing mode
        MAX_DRAWDOWN = 0.30 if not testing_mode else 1.0  # No drawdown limit in testing mode
        MIN_WIN_RATE = 0.30 if not testing_mode else 0.0  # No win rate requirement in testing mode
        
        # Always print trade stats for debugging
        print(f"DEBUG (Stats): Trades={pf.trades.count()}, Win Rate={performance_stats['Win Rate [%]']}%, "  
              f"Drawdown={performance_stats['Max Drawdown [%]']}%, Return={performance_stats['Total Return [%]']}%")
        
        # Skip validation checks in testing mode
        if not testing_mode:
            if pf.trades.count() < MIN_TOTAL_TRADES:
                print(f"DEBUG (Eval Fail): Not enough trades ({pf.trades.count()}) for params {params}")
                return -np.inf
            
            # For vectorbtpro, max drawdown is returned as positive percent value
            if performance_stats['Max Drawdown [%]'] > abs(MAX_DRAWDOWN * 100.0):
                print(f"DEBUG (Eval Fail): Drawdown too high ({performance_stats['Max Drawdown [%]']}%) for params {params}")
                return -np.inf
            
            if performance_stats['Win Rate [%]'] < MIN_WIN_RATE * 100.0:
                print(f"DEBUG (Eval Fail): Win rate too low ({performance_stats['Win Rate [%]']}%) for params {params}")
                return -np.inf
        else:
            # In testing mode, just log that we're skipping validation
            print(f"DEBUG (Testing): Skipping validation checks for {pf.trades.count()} trades in testing mode")

        return score

    except Exception as e:
        traceback.print_exc()
        return -np.inf # Penalize heavily on any error
