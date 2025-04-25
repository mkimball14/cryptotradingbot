import sys
import os
from pathlib import Path
import vectorbtpro as vbt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import itertools
import logging
from typing import Dict, Any, List, Tuple, Optional
from tqdm.auto import tqdm # Use tqdm for progress bars
import json
import multiprocessing
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import inspect
from dotenv import load_dotenv
import time
import pandas_ta as ta
import traceback

# Note: This is a partial file containing the optimized configuration. 
# The rest of the original script's functions need to be added.

# Placeholder imports - replace with actual imports from original script if needed
try:
    from scripts.strategies.edge_strategy_assistant import create_portfolio
except ModuleNotFoundError:
    from edge_strategy_assistant import create_portfolio
try:
    from scripts.strategies.candlestick_pattern_strategy import CandlestickPatternStrategy
except ModuleNotFoundError:
    from candlestick_pattern_strategy import CandlestickPatternStrategy
try:
    from scripts.portfolio.custom_portfolio import CustomPortfolio
except ImportError:
    CustomPortfolio = None # Placeholder
    pass # Define dummy functions if needed

# Import refactored configuration
from scripts.strategies.refactored_edge import config

def fetch_historical_data(*args, **kwargs): return pd.DataFrame({'open': [], 'high': [], 'low': [], 'close': [], 'volume': []})
def get_vbt_freq_str(*args, **kwargs): return "1h"
GRANULARITY_MAP_SECONDS = {'1h': 3600}

load_dotenv(verbose=True)

# --- Setup Logging ---
# Remove existing console handler if present (basicConfig adds one by default)
root_logger = logging.getLogger()
if root_logger.hasHandlers():
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

# Configure basic logging to file and console
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File Handler
log_file = "wfo_run.log"
file_handler = logging.FileHandler(log_file, mode='w') # mode='w' overwrites log each run
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO) # Log INFO level and above to file

# Console Handler (optional, set level higher to reduce noise)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO) # Keep INFO on console for now, can increase later if too noisy

# Add handlers to the root logger
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO) # Set root logger level

wfo_logger = logging.getLogger('wfo_edge_strategy_optimized')
# wfo_logger's level will be INFO as inherited from root

# =============================================================================
# Helper Functions
# =============================================================================

# Function to generate weight combinations (if optimizing weights)
def generate_weight_combinations(factors: List[str], num_steps: int) -> List[Dict[str, float]]:
    """Generates valid factor weight combinations that sum to 1.0."""
    if not factors or num_steps <= 0:
        # Return default equal weights if no steps or factors
        return [{factor: 1.0/len(factors) for factor in factors}] if factors else []

    step = 1.0 / num_steps
    points = [round(i * step, 8) for i in range(num_steps + 1)] # Use round for precision
    valid_combinations = []

    for combo in itertools.product(points, repeat=len(factors)):
        if np.isclose(sum(combo), 1.0):
            valid_combinations.append(dict(zip(factors, combo)))

    # Deduplicate (necessary due to potential float precision issues)
    unique_combos_dict = {}
    for combo_dict in valid_combinations:
        combo_tuple = tuple(sorted(combo_dict.items()))
        if combo_tuple not in unique_combos_dict:
             unique_combos_dict[combo_tuple] = combo_dict

    # Ensure default equal weights are included if valid
    default_weights = {factor: 1.0 / len(factors) for factor in factors}
    default_tuple = tuple(sorted(default_weights.items()))
    if np.isclose(sum(default_weights.values()), 1.0) and default_tuple not in unique_combos_dict:
        unique_combos_dict[default_tuple] = default_weights

    return list(unique_combos_dict.values())


def extract_candle_patterns(df: pd.DataFrame, pattern_list: List[str] = None) -> pd.DataFrame:
    """
    Extract candle patterns from OHLCV data using pandas_ta.
    
    Args:
        df: DataFrame with open, high, low, close columns
        pattern_list: List of patterns to identify. If None, all patterns will be extracted.
            Available patterns: 'doji', 'hammer', 'inverted_hammer', 'hanging_man', 
            'shooting_star', 'engulfing', 'morning_star', 'evening_star', etc.
            Or use 'all' to get all available patterns.
    
    Returns:
        DataFrame with candle pattern signals (1 for bullish, -1 for bearish, 0 for none)
    """
    # Create a copy of the input DataFrame
    result_df = df.copy()
    
    try:
        # Convert column names to lowercase if needed
        required_cols = ['open', 'high', 'low', 'close']
        rename_map = {col.upper(): col for col in required_cols if col not in df.columns and col.upper() in df.columns}
        
        if rename_map:
            # Create a temporary DataFrame with lowercase columns
            temp_df = df.rename(columns=rename_map)
        else:
            temp_df = df.copy()
            
        # Ensure required columns exist
        missing_cols = [col for col in required_cols if col not in temp_df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Handle pattern_list input
        if pattern_list is None or 'all' in pattern_list:
            # Run cdl_pattern for all available patterns
            patterns = temp_df.ta.cdl_pattern(name="all")
        else:
            # Run for specific patterns
            patterns = pd.DataFrame(index=temp_df.index)
            for pattern in pattern_list:
                pattern_result = temp_df.ta.cdl_pattern(name=pattern)
                if not pattern_result.empty:
                    for col in pattern_result.columns:
                        patterns[col] = pattern_result[col]
        
        # Merge the patterns with the result DataFrame
        if not patterns.empty:
            for col in patterns.columns:
                result_df[col] = patterns[col]
                
        return result_df
        
    except Exception as e:
        wfo_logger.error(f"Error extracting candle patterns: {str(e)}")
        # Return the original DataFrame if there's an error
        return result_df


def get_candle_pattern_strength(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """
    Calculate the strength of candle patterns based on historical reliability.
    
    Args:
        df: DataFrame with candle pattern signals and price data
        lookback: Number of past occurrences to analyze for each pattern
    
    Returns:
        DataFrame with pattern strength metrics
    """
    result_df = df.copy()
    
    try:
        # Get all pattern columns
        pattern_cols = [col for col in df.columns if col.startswith('CDL')]
        
        if not pattern_cols:
            wfo_logger.warning("No candle pattern columns found. Run extract_candle_patterns first.")
            return result_df
            
        # Create forward returns for 1, 3, and 5 days
        try:
            result_df['return_1d'] = df['close'].pct_change(1).shift(-1)
            result_df['return_3d'] = df['close'].pct_change(3).shift(-3)
            result_df['return_5d'] = df['close'].pct_change(5).shift(-5)
        except Exception as e:
            wfo_logger.warning(f"Error calculating returns: {e}. Using default strength values.")
            # Set default strength values
            for pattern in pattern_cols:
                strength_col = f"{pattern}_strength"
                result_df[strength_col] = df[pattern].abs() * 0.01  # Simple default strength
            return result_df
        
        # Calculate pattern strength for each pattern
        for pattern in pattern_cols:
            # Create columns for pattern strength
            strength_col = f"{pattern}_strength"
            result_df[strength_col] = 0.0
            
            # Process each day
            for i in range(lookback, len(df)):
                # Get the current pattern value
                current_value = df[pattern].iloc[i]
                
                # Skip if no pattern detected
                if current_value == 0:
                    continue
                    
                # Get historical pattern occurrences (same sign)
                hist_window = df[pattern].iloc[i-lookback:i]
                hist_indices = hist_window[hist_window == current_value].index
                
                if len(hist_indices) > 0:
                    try:
                        # Calculate the average return after pattern
                        if current_value > 0:  # Bullish pattern
                            avg_return_1d = df.loc[hist_indices, 'return_1d'].mean()
                            avg_return_3d = df.loc[hist_indices, 'return_3d'].mean()
                            avg_return_5d = df.loc[hist_indices, 'return_5d'].mean()
                        else:  # Bearish pattern
                            avg_return_1d = -df.loc[hist_indices, 'return_1d'].mean()
                            avg_return_3d = -df.loc[hist_indices, 'return_3d'].mean()
                            avg_return_5d = -df.loc[hist_indices, 'return_5d'].mean()
                        
                        # Handle NaN values using nanmean if available or check pd.isna
                        avg_return_1d = 0.0 if pd.isna(avg_return_1d) else avg_return_1d
                        avg_return_3d = 0.0 if pd.isna(avg_return_3d) else avg_return_3d
                        avg_return_5d = 0.0 if pd.isna(avg_return_5d) else avg_return_5d
                        
                        # Calculate weighted strength based on returns
                        weighted_strength = (
                            0.5 * avg_return_1d + 
                            0.3 * avg_return_3d + 
                            0.2 * avg_return_5d
                        )
                        
                        # Account for frequency
                        frequency = len(hist_indices) / lookback
                        
                        # Calculate final strength
                        strength = weighted_strength * frequency * abs(current_value)
                        
                        # Store the strength value
                        result_df.loc[df.index[i], strength_col] = strength
                    except Exception as inner_e:
                        # If calculation fails, use a default strength value
                        default_strength = abs(current_value) * 0.01  # Simple default based on pattern value
                        result_df.loc[df.index[i], strength_col] = default_strength
        
        return result_df
        
    except Exception as e:
        wfo_logger.error(f"Error calculating candle pattern strength: {str(e)}")
        # Return the original DataFrame with default strength values if available
        for pattern in [col for col in df.columns if col.startswith('CDL')]:
            strength_col = f"{pattern}_strength"
            if strength_col not in result_df.columns:
                result_df[strength_col] = df[pattern].abs() * 0.01  # Simple default strength
        return result_df


def generate_candle_pattern_signals(df: pd.DataFrame, min_strength: float = 0.01, 
                                    use_strength: bool = True) -> Tuple[pd.Series, pd.Series]:
    """
    Generate trading signals based on candle patterns and their strength.
    
    Args:
        df: DataFrame with candle pattern signals and strength metrics
        min_strength: Minimum strength threshold for generating signals
        use_strength: Whether to use pattern strength for signal generation
    
    Returns:
        Tuple containing (buy_signals, sell_signals)
    """
    try:
        # Get all pattern columns
        pattern_cols = [col for col in df.columns if col.startswith('CDL')]
        strength_cols = [col for col in df.columns if col.endswith('_strength')]
        
        if not pattern_cols:
            wfo_logger.warning("No candle pattern columns found. Run extract_candle_patterns first.")
            return pd.Series(False, index=df.index), pd.Series(False, index=df.index)
            
        # Initialize signal series
        buy_signals = pd.Series(False, index=df.index)
        sell_signals = pd.Series(False, index=df.index)

        if use_strength and strength_cols:
            # Using pattern strength for signals
            
            # Calculate net pattern strength
            df['net_bullish_strength'] = 0.0
            df['net_bearish_strength'] = 0.0
            
            for pattern in pattern_cols:
                strength_col = f"{pattern}_strength"
                if strength_col in df.columns:
                    # Add to bullish strength if pattern is bullish and strength is positive
                    bullish_mask = (df[pattern] > 0) & (df[strength_col] > 0)
                    df.loc[bullish_mask, 'net_bullish_strength'] += df.loc[bullish_mask, strength_col]
                    
                    # Add to bearish strength if pattern is bearish and strength is positive
                    bearish_mask = (df[pattern] < 0) & (df[strength_col] > 0)
                    df.loc[bearish_mask, 'net_bearish_strength'] += df.loc[bearish_mask, strength_col]
            
            # Generate signals based on net strength
            buy_signals = df['net_bullish_strength'] > min_strength
            sell_signals = df['net_bearish_strength'] > min_strength
            
        else:
            # Using raw pattern signals
            for pattern in pattern_cols:
                # Add buy signals for bullish patterns
                buy_signals = buy_signals | (df[pattern] > 0)
                
                # Add sell signals for bearish patterns
                sell_signals = sell_signals | (df[pattern] < 0)
        
        return buy_signals, sell_signals
        
    except Exception as e:
        wfo_logger.error(f"Error generating candle pattern signals: {str(e)}")
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index)


# --- END NEW JSON DEFAULT FUNCTION ---

# --- Checkpointing Functions ---
def save_checkpoint(split_id, train_results, oos_results, all_params, filename="wfo_checkpoint.json"):
    """Save WFO progress to a checkpoint file."""
    checkpoint_data = {
        'last_split': split_id,
        'train_results': train_results,
        'oos_results': oos_results,
        'all_params': all_params
    }
    try:
        with open(filename, 'w') as f:
            json.dump(checkpoint_data, f, indent=4, default=str) # Use default=str for non-serializable types
        wfo_logger.info(f"Checkpoint saved successfully for split {split_id} to {filename}")
    except Exception as e:
        wfo_logger.error(f"Error saving checkpoint to {filename}: {str(e)}")

def load_checkpoint(filename="wfo_checkpoint.json"):
    """Load WFO progress from a checkpoint file."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                checkpoint_data = json.load(f)
            
            # Validate required keys
            required_keys = ['last_split', 'train_results', 'oos_results', 'all_params']
            if all(key in checkpoint_data for key in required_keys):
                wfo_logger.info(f"Checkpoint loaded successfully from {filename}. Resuming from split {checkpoint_data['last_split'] + 1}.")
                return (
                    checkpoint_data['last_split'],
                    checkpoint_data['train_results'],
                    checkpoint_data['oos_results'],
                    checkpoint_data['all_params']
                )
            else:
                 wfo_logger.warning(f"Checkpoint file {filename} is missing required keys. Starting from scratch.")
                 return -1, [], [], [] # Return defaults if keys missing
        else:
            wfo_logger.info(f"Checkpoint file {filename} not found. Starting WFO from the beginning.")
            return -1, [], [], [] # Return defaults if file doesn't exist
    except json.JSONDecodeError as e:
        wfo_logger.error(f"Error decoding checkpoint file {filename}: {str(e)}. Starting from scratch.")
        return -1, [], [], [] # Return defaults if JSON is invalid
    except Exception as e:
        wfo_logger.error(f"Error loading checkpoint from {filename}: {str(e)}. Starting from scratch.")
        return -1, [], [], [] # Return defaults for other errors

# --- Strategy Specific Calculation Helpers ---
def optimize_pattern_signal_parameters(df: pd.DataFrame, test_length: int = 252, min_trades: int = 10) -> Dict[str, Any]:
    """Optimize parameters for candle pattern signal generation."""
    # ... (Function body remains unchanged) # This placeholder seems correct as it's likely unused in the current config
    pass # Add pass to make it syntactically valid if empty

def create_portfolio_for_strategy(data, entries, exits, init_cash=INITIAL_CAPITAL, size=None, stop_loss=None, take_profit=None, direction='long'):
    """Create a portfolio using vectorbt or CustomPortfolio."""
    # ... (Function body remains unchanged) # This placeholder seems correct as it's likely unused in the current config
    pass # Add pass to make it syntactically valid if empty

def create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL):
    """
    Create a vectorbt Portfolio object with the given parameters.
    
    Args:
        data: DataFrame with OHLCV data
        params: Dictionary of strategy parameters
        init_cash: Initial capital
        
    Returns:
        vectorbt.Portfolio or None: Portfolio object or None if creation failed
    """
    try:
        # Attempt re-import within worker
        from vectorbtpro import IndicatorFactory
        import vectorbtpro as vbt # Re-assign vbt just in case
        
        # Ensure we have a DataFrame
        if not isinstance(data, pd.DataFrame):
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                wfo_logger.error("Data is not a DataFrame or dictionary") # Changed logging level
                return None
        else:
            df = data.copy()
            
        # Ensure we have the necessary OHLCV columns
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        # Ensure columns are lowercase
        df.columns = df.columns.str.lower()

        for col in required_columns:
            if col not in df.columns:
                wfo_logger.error(f"Missing required column: {col}") # Changed logging level
                return None
        
        # Extract parameters
        rsi_window = int(params.get('rsi_window', 14))
        rsi_entry = float(params.get('rsi_entry', 30))
        rsi_exit = float(params.get('rsi_exit', 70))
        
        bb_window = int(params.get('bb_window', 20))
        bb_dev = float(params.get('bb_dev', 2.0))
        
        vol_window = int(params.get('vol_window', 20))
        vol_threshold = float(params.get('vol_threshold', 0.5))
        
        sl_pct = float(params.get('sl_pct', 0.05))
        tp_pct = float(params.get('tp_pct', 0.1))
        
        risk_per_trade = float(params.get('risk_per_trade', 0.02))
        
        commission_pct = float(params.get('commission_pct', COMMISSION_PCT))
        slippage_pct = float(params.get('slippage_pct', SLIPPAGE_PCT))
        
        # Calculate indicators
        # RSI
        rsi = vbt.RSI.run(df['close'], window=rsi_window).rsi
        
        # Bollinger Bands
        # bb = vbt.BollingerBands.run(df['close'], window=bb_window, alpha=bb_dev) # Incorrect access
        # Use the locally imported IndicatorFactory
        bb = IndicatorFactory.from_pandas_ta('bbands').run(df['close'], length=bb_window, std=bb_dev)
        
        # Volatility (using 'close' prices and standard deviation)
        df['volatility'] = df['close'].pct_change().rolling(window=vol_window).std()
        
        # Generate entry signals
        # Long entry: RSI below entry threshold AND volatility above threshold
        # long_entry = (rsi < rsi_entry) & (df['close'] < bb.bbl) & (df['volatility'] > vol_threshold) # Original complex condition
        long_entry = (rsi < rsi_entry) # Simplified condition (RSI only)
        # long_entry = (rsi < rsi_entry) & (df['close'] < bb.bbl) # RSI + BB condition
        # long_entry = (rsi < rsi_entry) & (df['volatility'] > vol_threshold) # RSI + Volatility condition
        
        # Exit signals: RSI above exit threshold or price above upper BB
        long_exit = (rsi > rsi_exit) | (df['close'] > bb.bbu) # Use bb.bbu
        
        # Generate position sizing based on risk per trade
        size = calculate_position_size(
            signal=long_entry,
            price=df['close'],
            stop_loss_pct=sl_pct,
            risk_pct=risk_per_trade,
            capital=init_cash
        )
        
        # Create portfolio object
        try:
            # Determine whether to use CustomPortfolio
            use_sl_tp = sl_pct is not None and sl_pct > 0 and tp_pct is not None and tp_pct > 0
            
            # Always try to use CustomPortfolio first if available and needed
            portfolio = None
            if use_sl_tp and CustomPortfolio is not None:
                try:
                    # Create portfolio with CustomPortfolio
                    portfolio = CustomPortfolio.from_signals(
                        close=df['close'],
                        entries=long_entry,
                        exits=long_exit,
                        size=size,
                        size_type='amount' if size is not None and not size.isnull().all() else 'value', # Check if size has values
                        init_cash=init_cash,
                        fees=commission_pct, # Pass directly, vbt handles % conversion
                        slippage=slippage_pct, # Pass directly
                        freq=get_vbt_freq_str(GRANULARITY_STR),
                        stop_loss=sl_pct,
                        take_profit=tp_pct
                    )
                    wfo_logger.debug("Attempted portfolio creation with CustomPortfolio for SL/TP") # Debug log
                except Exception as cp_error:
                    wfo_logger.warning(f"CustomPortfolio failed: {cp_error}. Falling back.")
                    portfolio = None # Ensure portfolio is None if CustomPortfolio fails

            # Fallback or standard creation if CustomPortfolio not used/failed/unavailable
            if portfolio is None:
                portfolio = vbt.Portfolio.from_signals(
                    close=df['close'],
                    entries=long_entry,
                    exits=long_exit,
                    size=size,
                    size_type='amount' if size is not None and not size.isnull().all() else 'value', # Check if size has values
                    init_cash=init_cash,
                    fees=commission_pct, # Pass directly
                    slippage=slippage_pct, # Pass directly
                    freq=get_vbt_freq_str(GRANULARITY_STR),
                    # Pass sl/tp to standard portfolio if CustomPortfolio wasn't used but SL/TP were defined
                    sl_stop=sl_pct if not use_sl_tp else None, 
                    tp_stop=tp_pct if not use_sl_tp else None
                )
                wfo_logger.debug("Created portfolio with standard vbt.Portfolio") # Debug log
            
            # Basic validity check
            if portfolio is not None:
                wfo_logger.debug(f"Portfolio created successfully for params: {params}")
                return portfolio
            else:
                wfo_logger.error(f"Portfolio creation returned None for params: {params}")
                return None
                
        except Exception as e:
            # Catch errors during portfolio creation itself
            wfo_logger.error(f"Error creating portfolio object for params {params}: {str(e)}")
            wfo_logger.exception("Traceback (Portfolio Creation Inner):") # Add traceback here too
            return None
            
    except Exception as e:
        # Catch errors in the broader function (indicator calculation etc.)
        wfo_logger.error(f"Error in create_pf_for_params for params {params}: {str(e)}")
        wfo_logger.exception("Traceback (create_pf_for_params Outer):")
        return None

def calculate_position_size(signal, price, stop_loss_pct, risk_pct, capital):
    """
    Calculate position size based on risk per trade.
    
    Args:
        signal: Boolean Series with entry signals
        price: Series with entry prices
        stop_loss_pct: Stop loss percentage (as decimal, e.g., 0.05 for 5%)
        risk_pct: Risk percentage per trade (as decimal)
        capital: Total capital
        
    Returns:
        Series: Position sizes in currency units, or None if invalid inputs
    """
    if not isinstance(signal, pd.Series) or not isinstance(price, pd.Series) or signal.empty or price.empty:
        wfo_logger.warning("Invalid input for calculate_position_size (signal or price empty/not Series).")
        return None
    if stop_loss_pct <= 0:
        wfo_logger.warning(f"Invalid stop_loss_pct ({stop_loss_pct}) <= 0. Cannot calculate size.")
        # Return a series of Nones or zeros? Let's return None to signal failure.
        return None 
    if risk_pct <= 0:
         wfo_logger.warning(f"Invalid risk_pct ({risk_pct}) <= 0. Cannot calculate size.")
         return None

    # Initialize size Series with Nones (or Zeros?) Let's use NaN, then fillna(0)
    size = pd.Series(np.nan, index=signal.index)
    
    # Only calculate sizes for entry signals where signal is True
    entry_indices = signal[signal == True].index
    
    if entry_indices.empty:
         #wfo_logger.debug("No entry signals found for sizing.") # Can be very noisy
         return size.fillna(0.0) # Return zeros if no entries

    for i in entry_indices:
        try:
            # Get entry price at index i
            entry_price = price.loc[i]
            
            if pd.isna(entry_price) or entry_price <= 0:
                #wfo_logger.debug(f"Skipping size calculation at index {i}: Invalid entry price {entry_price}")
                continue # Skip if price is invalid

            risk_amount = capital * risk_pct
            
            # Calculate the price distance to stop loss
            price_distance = entry_price * stop_loss_pct
            
            if price_distance > 0:
                # Calculate position size in units (shares/coins)
                position_size_units = risk_amount / price_distance
                # Convert units to currency amount
                size.loc[i] = position_size_units * entry_price 
                #wfo_logger.debug(f"Calculated size at {i}: {size.loc[i]} (Price: {entry_price}, SLDist: {price_distance}, RiskAmt: {risk_amount})")
            else:
                #wfo_logger.debug(f"Skipping size calculation at index {i}: Price distance ({price_distance}) is not positive.")
                size.loc[i] = 0.0 # Set size to 0 if distance is non-positive
                
        except KeyError:
            #wfo_logger.debug(f"Index {i} not found in price series during size calculation.")
            continue # Skip if index is somehow invalid
        except Exception as e:
             wfo_logger.error(f"Error calculating size at index {i}: {e}")
             wfo_logger.exception("Traceback (calculate_position_size loop):")
             size.loc[i] = 0.0 # Set size to 0 on error

    # Fill any remaining NaNs with 0 (e.g., non-entry points or calculation errors)
    return size.fillna(0.0)


def evaluate_parameter_set(data, params, split_id=None):
    """Evaluate a parameter set on the given data."""
    portfolio = None
    metrics = None
    try:
        # Step 1: Create portfolio 
        wfo_logger.debug(f"Evaluating params {params} for split {split_id}") # Added debug log
        portfolio_creation_failed = False
        try:
            if STRATEGY_TYPE == "candlestick":
                # Extract candlestick specific parameters
                lookback_periods = params.get('lookback_periods', 20)
                min_strength = params.get('min_strength', 0.01)
                use_strength = params.get('use_strength', True)
                use_confirmation = params.get('use_confirmation', True)
                confirmation_window = params.get('confirmation_window', 3)
                stop_loss_pct = params.get('stop_loss_pct', 0.03)
                take_profit_pct = params.get('take_profit_pct', 0.06)
                risk_per_trade = params.get('risk_per_trade', 0.02)
                
                # Extract candle patterns
                df_with_patterns = extract_candle_patterns(data)
                
                # Calculate pattern strength if needed
                if use_strength:
                    df_with_patterns = get_candle_pattern_strength(df_with_patterns, lookback=lookback_periods)
                
                # Generate signals
                entries, exits = generate_candle_pattern_signals(
                    df_with_patterns, 
                    min_strength=min_strength,
                    use_strength=use_strength
                )
                
                # Apply confirmation if needed
                if use_confirmation:
                    # Shift entries by confirmation window days
                    confirmed_entries = entries.copy()
                    for i in range(1, confirmation_window + 1): # Inclusive range up to window size
                        confirmed_entries = confirmed_entries & entries.shift(i) # Check previous days
                    entries = confirmed_entries
                
                # Calculate position sizes based on risk per trade
                size = calculate_position_size(
                    signal=entries,
                    price=data['close'], # Use close price for sizing calculation
                    stop_loss_pct=stop_loss_pct,
                    risk_pct=risk_per_trade,
                    capital=INITIAL_CAPITAL
                )
                
                # Create portfolio
                portfolio = create_pf_for_candlestick_strategy(
                    data=data,
                    entries=entries,
                    exits=exits,
                    init_cash=INITIAL_CAPITAL,
                    size=size, # Pass calculated size
                    sl_stop=stop_loss_pct,
                    tp_stop=take_profit_pct
                )
            else:
                 # Use the EdgeMultiFactorStrategy approach
                 portfolio = create_pf_for_params(data, params, init_cash=INITIAL_CAPITAL)
            
            if portfolio is None:
                portfolio_creation_failed = True
                # Log is already inside create_pf_for_params
                # wfo_logger.warning(f"Portfolio creation failed for params: {params}, split: {split_id}")
                
        except Exception as pf_error:
             portfolio_creation_failed = True
             wfo_logger.error(f"Exception during portfolio creation/strategy logic for params {params}, split {split_id}: {pf_error}")
             wfo_logger.exception("Traceback (Portfolio Creation):") # Log traceback specifically for this step
             # Ensure portfolio is None if creation fails
             portfolio = None

        # Step 2: Calculate performance metrics only if portfolio creation succeeded
        if not portfolio_creation_failed and portfolio is not None:
            try:
                metrics = calculate_performance_metrics(portfolio)
                # Log the raw metrics before checking criteria
                wfo_logger.info(f"[Raw Metrics] Split: {split_id}, Params: {params}, Metrics: {metrics}")
            except Exception as metrics_error:
                 wfo_logger.error(f"Exception during metric calculation for params {params}, split {split_id}: {metrics_error}")
                 wfo_logger.exception("Traceback (Metric Calculation):") # Log traceback specifically for this step
                 # Set metrics to None or default error state if calculation fails
                 metrics = None 
        else:
             # If portfolio creation failed, metrics should also be None or default error state
             metrics = None 
             #wfo_logger.debug(f"Skipping metric calculation due to failed portfolio creation for params {params}, split {split_id}") # Can be noisy

        # Step 3: Check minimum requirements (only if metrics were calculated)
        if metrics is not None:
             # Always return the dictionary if metrics were calculated
             return {'metrics': metrics, 'params': params, 'split_id': split_id}
            # passes_criteria = (
            #     metrics.get('num_trades', 0) >= MIN_TOTAL_TRADES and
            #     metrics.get('sharpe_ratio', -np.inf) >= MIN_SHARPE_RATIO and # Corrected key from 'sharpe'
            #     metrics.get('win_rate', 0) >= MIN_WIN_RATE and
            #     metrics.get('max_dd', -np.inf) >= MAX_DRAWDOWN # Drawdown is negative
            # )
            # if not passes_criteria:
            #      #wfo_logger.debug(f"Params {params}, split {split_id} did not meet minimum performance criteria. Metrics: {metrics}") # Can be very noisy
            #      # If it doesn't pass, return None for portfolio/metrics to filter it out later
            #      # Return the dictionary anyway, filtering happens later
            #      return {'metrics': metrics, 'params': params, 'split_id': split_id} # Return dict even if fails criteria
            # else:
            #      #wfo_logger.debug(f"Params {params}, split {split_id} PASSED minimum criteria.") # Can be very noisy
            #      # Passes criteria, return the valid portfolio and metrics
            #      # Return only necessary info for parallel efficiency: portfolio object might be large
            #      return {'metrics': metrics, 'params': params, 'split_id': split_id} # Modified return structure
        else:
             # If metrics are None (due to portfolio failure or metrics calculation failure), return None
             return None # Modified return structure

    except Exception as e:
        # Catch-all for any other unexpected error in the main function body
        wfo_logger.error(f"Unexpected error in evaluate_parameter_set for params {params}, split {split_id}: {e}")
        wfo_logger.exception("Traceback (evaluate_parameter_set):")
        return None # Modified return structure

def calculate_performance_metrics(portfolio):
    """Calculate key performance metrics from a portfolio object."""
    metrics = {}
    default_metrics = {
        'total_return': 0.0, 'sharpe_ratio': 0.0, 'max_drawdown': 0.0,
        'calmar_ratio': 0.0, 'sortino_ratio': 0.0, 'win_rate': 0.0, 
        'num_trades': 0, 'profit_factor': 0.0, 'avg_trade_pnl': 0.0,
        'expectancy': 0.0, 'sqn': 0.0
    }

    if portfolio is None:
        #wfo_logger.debug("Portfolio is None, returning default metrics.")
        return default_metrics
    
    try:
        stats = portfolio.stats()
        if stats is None:
            #wfo_logger.debug("portfolio.stats() returned None.")
            return default_metrics

        # Ensure stats is a dictionary or Series for .get() method
        if isinstance(stats, (pd.Series, dict)):
            metrics['total_return'] = stats.get('Total Return [%]', 0.0) * 0.01 # Convert percentage to decimal
            metrics['sharpe_ratio'] = stats.get('Sharpe Ratio', 0.0)
            metrics['max_drawdown'] = stats.get('Max Drawdown [%]', 0.0) * -0.01 # Convert to negative decimal
            metrics['calmar_ratio'] = stats.get('Calmar Ratio', 0.0)
            metrics['sortino_ratio'] = stats.get('Sortino Ratio', 0.0) # Added Sortino
            metrics['win_rate'] = stats.get('Win Rate [%]', 0.0) * 0.01 # Convert percentage to decimal
            metrics['num_trades'] = int(stats.get('Total Trades', 0))
            metrics['profit_factor'] = stats.get('Profit Factor', 0.0)
            metrics['avg_trade_pnl'] = stats.get('Avg Winning Trade [%]', 0.0) * 0.01 if metrics['win_rate'] > 0 else 0.0 # Approx.
            # Expectancy = (Win Rate * Avg Win) - (Loss Rate * Avg Loss) - approx using avg trade
            metrics['expectancy'] = stats.get('Expectancy', 0.0) # Added Expectancy if available
            # SQN = sqrt(num_trades) * (avg_trade_pnl / std_dev_pnl) - needs pnl std dev
            metrics['sqn'] = stats.get('SQN', 0.0) # Added SQN if available

            # Handle potential NaN values from stats, replacing with 0
            for key in metrics:
                if pd.isna(metrics[key]):
                     metrics[key] = 0.0
                     
            # Ensure num_trades is int
            metrics['num_trades'] = int(metrics.get('num_trades', 0))

        else:
            wfo_logger.warning(f"portfolio.stats() returned unexpected type: {type(stats)}. Returning default metrics.")
            return default_metrics

    except Exception as e:
        wfo_logger.error(f"Error calculating metrics: {str(e)}")
        wfo_logger.exception("Traceback (calculate_performance_metrics):")
        # Return default metrics if calculation fails
        metrics = default_metrics
    
    #wfo_logger.debug(f"Calculated metrics: {metrics}")
    return metrics


def create_pf_for_candlestick_strategy(data, entries, exits, init_cash=INITIAL_CAPITAL, size=None, sl_stop=None, tp_stop=None):
    """
    Wrapper function for create_portfolio_for_strategy for the candlestick strategy.
    
    Args:
        data: DataFrame with OHLCV data
        entries: Series of entry signals
        exits: Series of exit signals
        init_cash: Initial capital
        size: Optional size series (in currency value if not None)
        sl_stop: Stop loss percentage (as decimal)
        tp_stop: Take profit percentage (as decimal)
        
    Returns:
        Portfolio object or CustomPortfolio object
    """
    try:
        # Ensure data types are correct
        if not isinstance(entries, pd.Series):
            entries = pd.Series(entries, index=data.index)
        if not isinstance(exits, pd.Series):
            exits = pd.Series(exits, index=data.index)

        # Data cleaning: ensure boolean signals
        entries = entries.fillna(False).astype(bool)
        exits = exits.fillna(False).astype(bool)

        # Ensure size is appropriate type or None
        if size is not None and not isinstance(size, pd.Series):
             size = pd.Series(size, index=data.index)
             size = size.fillna(0) # Fill NaNs resulting from type conversion or index mismatch

        # Determine size type
        size_type = 'value' # Default to value-based sizing
        if size is not None and not size.isnull().all() and (size > 0).any():
            # If size is provided and has positive values, assume it's currency amount
            size_type = 'amount' 
            wfo_logger.debug(f"Using size_type='amount' based on provided size series.")
        else:
            # If size is None, zero, or all NaN, use default sizing (e.g., fixed value per signal)
             size = 1.0 # Or some fraction of init_cash? Let's default to fixed 1.0 value per signal
             size_type = 'value'
             wfo_logger.debug(f"Using default size=1.0, size_type='value'.")


        # Use CustomPortfolio if available and SL/TP are defined
        portfolio = None
        use_sl_tp = sl_stop is not None and sl_stop > 0 and tp_stop is not None and tp_stop > 0
        
        if use_sl_tp and CustomPortfolio is not None:
             try:
                 portfolio = CustomPortfolio.from_signals(
                     close=data['close'],
                     entries=entries,
                     exits=exits,
                     size=size,
                     size_type=size_type, 
                     init_cash=init_cash,
                     fees=COMMISSION_PCT, 
                     slippage=SLIPPAGE_PCT,
                     freq=get_vbt_freq_str(GRANULARITY_STR),
                     stop_loss=sl_stop,
                     take_profit=tp_stop
                 )
                 wfo_logger.debug("Attempted candlestick portfolio with CustomPortfolio.")
             except Exception as cp_error:
                 wfo_logger.warning(f"CustomPortfolio failed for candlestick: {cp_error}. Falling back.")
                 portfolio = None

        # Fallback or standard creation
        if portfolio is None:
             portfolio = vbt.Portfolio.from_signals(
                 close=data['close'],
                 entries=entries,
                 exits=exits,
                 size=size,
                 size_type=size_type,
                 init_cash=init_cash,
                 fees=COMMISSION_PCT,
                 slippage=SLIPPAGE_PCT,
                 freq=get_vbt_freq_str(GRANULARITY_STR),
                 # Pass sl/tp only if CustomPortfolio wasn't used
                 sl_stop=sl_stop if not use_sl_tp else None, 
                 tp_stop=tp_stop if not use_sl_tp else None
             )
             wfo_logger.debug("Created candlestick portfolio with standard vbt.Portfolio.")
        
        return portfolio

    except Exception as e:
        wfo_logger.error(f"Error in create_pf_for_candlestick_strategy: {e}")
        wfo_logger.exception("Traceback (create_pf_for_candlestick_strategy):")
        return None # Return None on failure


def evaluate_single_param_set_wrapper(args):
    """Wrapper for evaluate_parameter_set to use in parallel processing."""
    data, params, split_id = args
    try:
        # Re-initialize logging within the worker process if needed
        # Basic configuration for the worker process logger (can be enhanced)
        # worker_logger = logging.getLogger(f'wfo_worker_{os.getpid()}')
        # if not worker_logger.hasHandlers():
        #     handler = logging.StreamHandler(sys.stderr) # Log worker errors to stderr
        #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #     handler.setFormatter(formatter)
        #     worker_logger.addHandler(handler)
        #     worker_logger.setLevel(logging.DEBUG) # Log debug messages from worker

        # Optionally log the start of evaluation for this specific param set
        # wfo_logger.debug(f"Worker evaluating params: {params} for split: {split_id}") 
        
        result_dict = evaluate_parameter_set(data, params, split_id) # Expects dict or None
        
        # Optionally log the successful result before returning
        # if result_dict:
        #     wfo_logger.debug(f"Worker finished evaluation successfully for params: {params}, split: {split_id}")
        # else:
        #     wfo_logger.debug(f"Worker finished evaluation with no valid portfolio/metrics for params: {params}, split: {split_id}")
            
        # Return the dictionary containing metrics, params, split_id or None
        return result_dict 
        
    except Exception as e:
        # Log the exception with traceback *within the worker*
        # Standard logging might not reliably reach the main process log file from workers
        # Using print to stderr is often more reliable for seeing errors during testing
        error_message = f"ERROR in evaluate_single_param_set_wrapper (Split: {split_id}, Params: {params}): {e}\n{traceback.format_exc()}"
        print(error_message, file=sys.stderr) 
        
        # Log to the main logger as well, just in case it works
        # Use the already configured wfo_logger
        wfo_logger.error(f"Exception in evaluate_single_param_set_wrapper (Split: {split_id}, Params: {params}): {e}")
        wfo_logger.exception("Traceback:") # Logs the full traceback associated with the current exception
        
        # Return None to indicate failure, matching the expected output structure of evaluate_parameter_set when it fails
        return None 

# --- WFO Core Logic & Reporting Functions (Moved Up) ---
def evaluate_parameter_sets(data, param_grid, optimization_metric='sharpe_ratio', split_id=None, use_parallel=USE_PARALLEL, num_cores=NUM_CORES):
    """
    Evaluate multiple parameter sets using parallel processing if enabled.

    Args:
        data (pd.DataFrame): The time series data for evaluation.
        param_grid (dict): The parameter grid to explore.
        optimization_metric (str): The metric to optimize.
        split_id (int, optional): Identifier for the WFO split. Defaults to None.
        use_parallel (bool): Flag to enable parallel processing.
        num_cores (int): Number of CPU cores to use for parallel processing.

    Returns:
        list: A list of dictionaries, each containing parameters and performance metrics.
    """
    wfo_logger.info(f"Evaluating parameter sets for split {split_id} (Parallel: {use_parallel})...")
    
    # Create all combinations of parameters
    keys = list(param_grid.keys())
    value_lists = []
    for key in keys:
        param_info = param_grid[key]
        if isinstance(param_info, tuple) and len(param_info) == 3:
            # Range definition: (start, stop, step)
            start, stop, step = param_info
            # Use np.arange for floating point steps, linspace if integers preferred
            if isinstance(step, float):
                values = np.arange(start, stop + step * 0.5, step) # Add small epsilon for float endpoint
            else:
                values = np.arange(start, stop + step, step)
            value_lists.append(list(values))
        elif isinstance(param_info, list):
            # List definition
            value_lists.append(param_info)
        else:
            wfo_logger.warning(f"Invalid parameter format for {key}: {param_info}. Skipping.")
            value_lists.append([None]) # Add placeholder to maintain structure

    # Generate parameter combinations
    param_combinations = list(itertools.product(*value_lists))
    param_dicts = [dict(zip(keys, combo)) for combo in param_combinations]
    
    wfo_logger.info(f"Total parameter combinations to evaluate: {len(param_dicts)}")

    # Filter out combinations with None values from invalid formats
    valid_param_dicts = [p for p in param_dicts if all(v is not None for v in p.values())]
    if len(valid_param_dicts) < len(param_dicts):
        wfo_logger.warning(f"Skipped {len(param_dicts) - len(valid_param_dicts)} invalid parameter combinations.")
    
    if not valid_param_dicts:
        wfo_logger.error("No valid parameter combinations generated. Check PARAM_GRID definition.")
        return []

    results = []
    
    if use_parallel:
        # Use ProcessPoolExecutor for parallel execution
        wfo_logger.info(f"Starting parallel evaluation using {num_cores} cores...")
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            # Prepare arguments for the wrapper function
            args_list = [(data, params, split_id) for params in valid_param_dicts]
            
            # Use tqdm to show progress
            futures = [executor.submit(evaluate_single_param_set_wrapper, args) for args in args_list]
            
            # Collect results with progress bar
            for future in tqdm(futures, total=len(futures), desc=f"Split {split_id} Evaluation"):
                try:
                    result = future.result()
                    if result: # Only append if evaluation was successful
                        results.append(result)
                except Exception as e:
                    wfo_logger.error(f"Error in parallel evaluation task: {e}")
                    # Optionally log traceback for detailed debugging
                    # wfo_logger.exception("Traceback for parallel task error:")
    else:
        # Sequential execution
        wfo_logger.info("Starting sequential evaluation...")
        for params in tqdm(valid_param_dicts, desc=f"Split {split_id} Sequential Eval"):
            try:
                result = evaluate_single_param_set_wrapper((data, params, split_id))
                if result:
                    results.append(result)
            except Exception as e:
                wfo_logger.error(f"Error evaluating parameter set {params}: {e}")
                # Optionally log traceback
                # wfo_logger.exception(f"Traceback for error evaluating {params}:")

    wfo_logger.info(f"Finished evaluating {len(results)} parameter sets for split {split_id}.")
    return results


def analyze_parameter_stability(all_params: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    Analyzes the stability of parameters across WFO splits.

    Args:
        all_params (List[Dict[str, Any]]): List of dictionaries, where each dictionary 
                                           contains the best parameters for one WFO split.

    Returns:
        Dict[str, Dict[str, float]]: Dictionary containing stability metrics (mean, std) 
                                      for each numerical parameter.
    """
    wfo_logger.info("Analyzing parameter stability across WFO splits...")
    if not all_params or not isinstance(all_params, list) or len(all_params) == 0:
        wfo_logger.warning("No parameters found to analyze stability.")
        return {}

    # Combine parameters from all splits into a DataFrame
    try:
        # Ensure all dicts in all_params have consistent keys, handle potential errors
        # Extract parameters, assuming each item in all_params is a dict like {'params': {...}, 'metrics': {...}}
        param_dicts = [split_result.get('params', {}) for split_result in all_params if isinstance(split_result, dict)]
        
        if not param_dicts:
            wfo_logger.warning("No valid parameter dictionaries found in all_params.")
            return {}
            
        df_params = pd.DataFrame(param_dicts)
        
        # Identify numerical columns for stability analysis
        numerical_cols = df_params.select_dtypes(include=np.number).columns
        
        if numerical_cols.empty:
            wfo_logger.warning("No numerical parameters found for stability analysis.")
            return {}

        stability_metrics = {}
        for col in numerical_cols:
            param_values = df_params[col].dropna()
            if len(param_values) > 1:  # Need at least 2 points for std dev
                stability_metrics[col] = {
                    'mean': param_values.mean(),
                    'std': param_values.std(),
                    'cv': param_values.std() / param_values.mean() if param_values.mean() != 0 else np.inf # Coefficient of Variation
                }
            elif len(param_values) == 1:
                 stability_metrics[col] = {
                    'mean': param_values.mean(),
                    'std': 0.0, # Standard deviation is 0 for a single point
                    'cv': 0.0
                }
            else:
                 wfo_logger.warning(f"Parameter '{col}' had no valid values across splits.")


        wfo_logger.info("Parameter stability analysis complete.")
        wfo_logger.debug(f"Stability Metrics: {stability_metrics}")
        return stability_metrics

    except Exception as e:
        wfo_logger.error(f"Error during parameter stability analysis: {str(e)}")
        # Log traceback for detailed debugging
        # wfo_logger.exception("Traceback for stability analysis error:")
        return {}


def recommend_final_parameters(all_params: List[Dict[str, Any]], stability_metrics: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
    """
    Recommends final parameters based on stability and performance across splits.

    Args:
        all_params (List[Dict[str, Any]]): List of best parameters from each split.
        stability_metrics (Dict[str, Dict[str, float]]): Stability metrics for numerical parameters.

    Returns:
        Dict[str, Any]: The recommended final parameter set.
    """
    wfo_logger.info("Recommending final parameters...")
    if not all_params:
        wfo_logger.error("Cannot recommend parameters: No parameter sets provided.")
        return {}
        
    # Consider using the parameters from the *last* split as a starting point
    # or averaging stable parameters. Let's try averaging stable ones.
    
    final_params = {}
    
    # Extract parameters from the last split as a base
    last_split_params = all_params[-1].get('params', {})
    if not last_split_params:
         wfo_logger.warning("Could not get parameters from the last split. Using empty base.")
    
    final_params.update(last_split_params) # Start with last split's params

    # Override with mean for stable parameters (low Coefficient of Variation)
    CV_THRESHOLD = 0.5 # Example threshold for stability (lower means more stable)
    
    numerical_params = stability_metrics.keys()
    
    for param_name in numerical_params:
        if param_name in stability_metrics:
            metrics = stability_metrics[param_name]
            cv = metrics.get('cv', np.inf)
            
            if cv < CV_THRESHOLD:
                # Parameter is stable, use the mean value
                mean_value = metrics['mean']
                
                # Round to appropriate precision based on original grid step if possible
                # (This requires access to the original grid, which isn't directly passed here)
                # For simplicity, we can round floats or cast ints
                if isinstance(last_split_params.get(param_name), int):
                    final_params[param_name] = int(round(mean_value))
                elif isinstance(last_split_params.get(param_name), float):
                     # Basic rounding, could be improved with grid step info
                    final_params[param_name] = round(mean_value, 4) # Round to 4 decimal places
                else:
                     final_params[param_name] = mean_value # Keep type if not int/float
                     
                wfo_logger.info(f"Using stable average for '{param_name}': {final_params[param_name]} (CV={cv:.2f})")
            else:
                wfo_logger.info(f"Parameter '{param_name}' is unstable (CV={cv:.2f}). Using value from last split: {final_params.get(param_name)}")
                # Keep the value from the last split if unstable

    wfo_logger.info(f"Recommended final parameters: {final_params}")
    return final_params


def save_final_parameters(params: Dict[str, Any], filename: str = "final_optimized_params.json"):
    """
    Saves the final recommended parameters to a JSON file.

    Args:
        params (Dict[str, Any]): The dictionary of final parameters.
        filename (str): The name of the file to save the parameters to.
    """
    if not params:
        wfo_logger.warning("No final parameters provided to save.")
        return
        
    try:
        # Ensure path exists (create if needed)
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert numpy types to native Python types for JSON serialization
        serializable_params = {}
        for key, value in params.items():
            if isinstance(value, np.integer):
                serializable_params[key] = int(value)
            elif isinstance(value, np.floating):
                serializable_params[key] = float(value)
            elif isinstance(value, np.bool_):
                 serializable_params[key] = bool(value)
            elif isinstance(value, (list, dict, str, int, float, bool, type(None))):
                 serializable_params[key] = value
            else:
                 wfo_logger.warning(f"Parameter '{key}' has non-serializable type {type(value)}. Converting to string.")
                 serializable_params[key] = str(value) # Convert unknown types to string

        with open(filepath, 'w') as f:
            json.dump(serializable_params, f, indent=4)
        wfo_logger.info(f"Final parameters saved successfully to {filepath}")
        
    except Exception as e:
        wfo_logger.error(f"Error saving final parameters to {filename}: {str(e)}")
        # Log traceback for detailed debugging
        # wfo_logger.exception("Traceback for parameter saving error:")

def generate_wfo_report(train_portfolios: List[Any], oos_portfolios: List[Any], all_params: List[Dict[str, Any]], filename: str = "wfo_report.txt"):
    """
    Generates a text report summarizing the WFO results.

    Args:
        train_portfolios (List[Any]): List of portfolio objects from training periods.
        oos_portfolios (List[Any]): List of portfolio objects from out-of-sample periods.
        all_params (List[Dict[str, Any]]): List of best parameters found in each split.
        filename (str): The name of the file to save the report to.
    """
    wfo_logger.info(f"Generating WFO report to {filename}...")
    report_content = []
    
    num_splits = len(oos_portfolios)
    report_content.append(f"Walk-Forward Optimization Report ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    report_content.append("===================================================")
    report_content.append(f"Total Splits: {num_splits}")
    report_content.append(f"Strategy Type: {STRATEGY_TYPE}")
    report_content.append(f"Symbol: {SYMBOL}, Granularity: {GRANULARITY_STR}")
    report_content.append(f"Period: {WFO_START_DATE} to {WFO_END_DATE}")
    report_content.append(f"In-Sample Days: {IN_SAMPLE_DAYS}, Out-of-Sample Days: {OUT_SAMPLE_DAYS}, Step Days: {STEP_DAYS}")
    report_content.append(f"Optimization Metric: {OPTIMIZATION_METRIC}")
    report_content.append("\n---")

    # Analyze Parameter Stability
    try:
        stability_metrics = analyze_parameter_stability(all_params)
        if stability_metrics:
            report_content.append("Parameter Stability Analysis:")
            for param, metrics in stability_metrics.items():
                report_content.append(f"  {param}: Mean={metrics['mean']:.4f}, StdDev={metrics['std']:.4f}, CV={metrics['cv']:.4f}")
            report_content.append("\n---")
        else:
             report_content.append("Parameter stability analysis could not be performed.")
             report_content.append("\n---")
    except Exception as e:
        report_content.append(f"Error during stability analysis: {e}")
        report_content.append("\n---")

    # Recommend Final Parameters
    try:
        final_params = recommend_final_parameters(all_params, stability_metrics)
        if final_params:
            report_content.append("Recommended Final Parameters:")
            report_content.append(json.dumps(final_params, indent=2, default=str))
             # Attempt to save final parameters
            save_final_parameters(final_params)
        else:
            report_content.append("Could not recommend final parameters.")
        report_content.append("\n---")
    except Exception as e:
        report_content.append(f"Error recommending/saving final parameters: {e}")
        report_content.append("\n---")

    # Overall OOS Performance Summary
    if oos_portfolios:
        try:
            # Concatenate OOS results if possible (depends on portfolio object structure)
            # Assuming calculate_performance_metrics works on a list or combined portfolio
            # This part might need adjustment based on the portfolio object type
            # --- Corrected Logic --- 
            # Extract metrics directly from the dictionaries stored in oos_portfolios
            oos_metrics_list = [pf.get('metrics', {}) for pf in oos_portfolios if pf is not None and isinstance(pf, dict)]
            # oos_metrics_list = [calculate_performance_metrics(pf) for pf in oos_portfolios if pf is not None] # <-- Original problematic line
            
            if oos_metrics_list:
                # Calculate average OOS metrics
                avg_metrics = pd.DataFrame(oos_metrics_list).mean().to_dict()
                report_content.append("Average Out-of-Sample Performance Metrics:")
                for metric, value in avg_metrics.items():
                    report_content.append(f"  {metric}: {value:.4f}")
            else:
                report_content.append("No valid OOS portfolios to calculate average metrics.")
        except Exception as e:
            report_content.append(f"Error calculating average OOS metrics: {e}")
    else:
        report_content.append("No Out-of-Sample results available.")

    report_content.append("\n---")
    report_content.append("End of Report")
    report_content.append("===================================================")

    # Save the report to a file
    try:
         # Ensure path exists
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write("\n".join(report_content))
        wfo_logger.info(f"WFO report saved successfully to {filepath}")
    except Exception as e:
        wfo_logger.error(f"Error saving WFO report to {filename}: {str(e)}")

def run_walk_forward_optimization(data, param_grid, optimization_metric='sharpe_ratio', 
                                in_sample_days=IN_SAMPLE_DAYS, out_sample_days=OUT_SAMPLE_DAYS, 
                                step_days=STEP_DAYS, resume_from_split=-1, 
                                initial_train_results=[], initial_oos_results=[], 
                                initial_all_params=[]):
    """
    Runs the walk-forward optimization process.

    Args:
        data (pd.DataFrame): Historical price data.
        param_grid (dict): Parameter grid for optimization.
        optimization_metric (str): Metric to optimize.
        in_sample_days (int): Number of days for in-sample training.
        out_sample_days (int): Number of days for out-of-sample testing.
        step_days (int): Number of days to step forward for the next window.
        resume_from_split (int): The index of the last completed split to resume from.
        initial_train_results (list): Existing training results from checkpoint.
        initial_oos_results (list): Existing OOS results from checkpoint.
        initial_all_params (list): Existing best parameters from checkpoint.


    Returns:
        tuple: (train_portfolios, oos_portfolios, all_best_params)
    """
    if data is None or data.empty:
        wfo_logger.error("Input data is empty. Cannot run Walk-Forward Optimization.")
        return [], [], []
        
    wfo_logger.info(f"Starting Walk-Forward Optimization: {in_sample_days} IS / {out_sample_days} OOS / {step_days} Step")
    
    # Ensure data index is datetime
    if not isinstance(data.index, pd.DatetimeIndex):
        try:
            data.index = pd.to_datetime(data.index)
            wfo_logger.info("Converted data index to DatetimeIndex.")
        except Exception as e:
             wfo_logger.error(f"Failed to convert data index to DatetimeIndex: {e}. Ensure index is date/time parsable.")
             return [], [], []

    # Convert durations to Timedeltas
    in_sample_duration = timedelta(days=in_sample_days)
    out_sample_duration = timedelta(days=out_sample_days)
    step_duration = timedelta(days=step_days)
    
    total_duration_days = (data.index[-1] - data.index[0]).days
    wfo_logger.info(f"Total data duration: {total_duration_days} days")

    # Initialize results lists from checkpoint data
    train_portfolios = list(initial_train_results) # Use list() to ensure mutable copy
    oos_portfolios = list(initial_oos_results)
    all_best_params = list(initial_all_params)
    
    start_date = data.index[0]
    end_date = data.index[-1]
    
    current_split_index = 0
    current_train_start = start_date

    while True:
        train_end = current_train_start + in_sample_duration
        oos_end = train_end + out_sample_duration

        # Check if the OOS period goes beyond the available data
        if oos_end > end_date:
            # Adjust OOS end to the last available date if necessary
            oos_end = end_date
            # If the remaining OOS period is too short, stop
            if train_end >= end_date or (oos_end - train_end) < timedelta(days=max(1, out_sample_days // 4)): # Require at least 1/4 OOS period
                 wfo_logger.info(f"Stopping WFO: Not enough data for OOS period starting at {train_end.strftime('%Y-%m-%d')}. Last data point: {end_date.strftime('%Y-%m-%d')}")
                 break

        # Check if the training period itself is valid
        if train_end > end_date:
             wfo_logger.info(f"Stopping WFO: Not enough data for training period starting at {current_train_start.strftime('%Y-%m-%d')}. Last data point: {end_date.strftime('%Y-%m-%d')}")
             break
             
        # Check if we need to skip this split based on checkpoint
        if current_split_index <= resume_from_split:
            wfo_logger.info(f"Skipping split {current_split_index} (already completed in checkpoint)...")
            current_train_start += step_duration
            current_split_index += 1
            continue # Move to the next iteration

        # Select data for the current split
        train_data = data[current_train_start:train_end]
        oos_data = data[train_end:oos_end] # OOS data starts right after train data ends

        # Ensure we have enough data for both periods
        min_data_points = 30 # Minimum required data points for meaningful analysis
        if len(train_data) < min_data_points or len(oos_data) < min_data_points // 2:
            wfo_logger.warning(f"Split {current_split_index}: Insufficient data (Train: {len(train_data)}, OOS: {len(oos_data)} points). Stopping WFO.")
            break

        wfo_logger.info(f"--- Split {current_split_index} --- ")
        wfo_logger.info(f"Train: {train_data.index[0].strftime('%Y-%m-%d')} - {train_data.index[-1].strftime('%Y-%m-%d')} ({len(train_data)} points)")
        wfo_logger.info(f"OOS:   {oos_data.index[0].strftime('%Y-%m-%d')} - {oos_data.index[-1].strftime('%Y-%m-%d')} ({len(oos_data)} points)")

        # 1. Evaluate parameters on training data
        train_results = evaluate_parameter_sets(train_data, param_grid, optimization_metric, split_id=current_split_index)

        # === DEBUG LOGGING START ===
        wfo_logger.info(f"Split {current_split_index}: Raw train_results received (type: {type(train_results)}):")
        wfo_logger.info(f"{train_results}") 
        # === DEBUG LOGGING END ===

        if not train_results:
            wfo_logger.warning(f"Split {current_split_index}: No valid parameter sets found during training. Skipping OOS evaluation.")
            # Append placeholders or handle as needed
            train_portfolios.append(None) 
            oos_portfolios.append(None)
            all_best_params.append({'params': {}, 'metrics': {}}) # Append empty results
        else:
            # 2. Select the best parameter set based on the optimization metric
            # Filter out None results AND results that don't meet criteria before finding the max
            valid_train_results = [
                res for res in train_results 
                if res is not None 
                and isinstance(res, dict) 
                and 'metrics' in res
                and res['metrics'].get('num_trades', 0) >= MIN_TOTAL_TRADES 
                and res['metrics'].get('sharpe_ratio', -np.inf) >= MIN_SHARPE_RATIO 
                and res['metrics'].get('win_rate', 0) >= MIN_WIN_RATE 
                and res['metrics'].get('max_drawdown', -np.inf) >= MAX_DRAWDOWN # Corrected key from max_dd
            ]
            
            if not valid_train_results:
                wfo_logger.warning(f"Split {current_split_index}: No valid results found after filtering train_results based on criteria. Skipping OOS.")
                best_params = {}
                best_train_metrics = {}
                train_portfolios.append(None)
                all_best_params.append({'params': {}, 'metrics': {}})
            else:
                best_train_result = max(valid_train_results, key=lambda x: x['metrics'].get(optimization_metric, -np.inf))
                best_params = best_train_result.get('params', {})
                best_train_metrics = best_train_result.get('metrics', {})
                wfo_logger.info(f"Split {current_split_index}: Best Train Params -> {best_params}")
                wfo_logger.info(f"Split {current_split_index}: Best Train Metric ({optimization_metric}) -> {best_train_metrics.get(optimization_metric, 'N/A')}")

                # Store the best performing portfolio from training
                # NOTE: Portfolio object is NOT returned by evaluate_parameter_set to save memory/time.
                # We store None here. The report function should handle this.
                train_portfolios.append(None) 
                all_best_params.append({'params': best_params, 'metrics': best_train_metrics})

                # 3. Evaluate the best parameter set on the out-of-sample data
                if best_params: # Only evaluate OOS if we found valid best_params
                    wfo_logger.info(f"Split {current_split_index}: Evaluating best params on OOS data...")
                    # Re-evaluate the best params on OOS data
                    # We need to call the evaluation function again, not just get a stored object
                    oos_result_dict = evaluate_single_param_set_wrapper((oos_data, best_params, f"{current_split_index}_OOS"))
                    
                    if oos_result_dict:
                        # Store OOS metrics and params (Portfolio object isn't returned)
                        oos_portfolios.append({'metrics': oos_result_dict.get('metrics', {}), 'params': best_params}) # Store metrics/params pair
                        wfo_logger.info(f"Split {current_split_index}: OOS Performance -> {oos_result_dict.get('metrics', {})}")
                    else:
                        wfo_logger.warning(f"Split {current_split_index}: OOS evaluation failed for best params.")
                        oos_portfolios.append(None) # Append placeholder if OOS eval fails
                else:
                    wfo_logger.warning(f"Split {current_split_index}: Skipping OOS evaluation as no best params were found.")
                    oos_portfolios.append(None)
                 
        # --- Save Checkpoint After Each Split ---
        save_checkpoint(current_split_index, train_portfolios, oos_portfolios, all_best_params)
        # --- End Save Checkpoint ---

        # Move to the next training window start date
        current_train_start += step_duration
        current_split_index += 1
        
        # Safety break to prevent infinite loops in case of unexpected condition
        if current_split_index > (total_duration_days / step_days) * 2: # Allow some buffer
             wfo_logger.error(f"Potential infinite loop detected after {current_split_index} splits. Breaking WFO.")
             break


    wfo_logger.info("Walk-Forward Optimization finished.")
    
    # Generate final report
    generate_wfo_report(train_portfolios, oos_portfolios, all_best_params)
    
    return train_portfolios, oos_portfolios, all_best_params


# --- Chat integration functions ---
def setup_chat_provider():
    """Set up chat provider based on available environment variables."""
    try:
        # Check for OpenRouter API Key (preferred for diverse model access)
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        if openrouter_api_key:
            wfo_logger.info("Using OpenRouter as provider")
            return "openrouter", openrouter_api_key
            
        # Fallback to OpenAI API Key
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            wfo_logger.info("Using OpenAI as provider")
            return "openai", openai_api_key
            
        # If no API keys found
        wfo_logger.warning("No API keys found. Chat integration will be unavailable.")
        return None, None
        
    except Exception as e:
        wfo_logger.error(f"Error setting up chat provider: {e}")
        return None, None

def get_chat_model():
    """Get a chat model function based on available providers."""
    provider, api_key = setup_chat_provider()
    
    if not provider or not api_key:
        wfo_logger.warning("No chat provider available. Chat-based features will be disabled.")
        return None
    
    try:
        if provider == "openrouter":
            import httpx
            
            # Select preferred model
            model = "openai/gpt-3.5-turbo-0125"  # Default to GPT-3.5 Turbo
            
            # Create chat function
            def openrouter_chat(prompt):
                try:
                    client = httpx.Client(timeout=60.0)  # 60 second timeout
                    
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    }
                    
                    data = {
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    
                    response = client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        wfo_logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                        return f"Error: {response.status_code} - {response.text}"
                        
                except Exception as e:
                    wfo_logger.error(f"OpenRouter chat error: {e}")
                    return f"Error: {str(e)}"
                    
            wfo_logger.info(f"Using OpenRouter with model: {model}")
            return openrouter_chat
            
        elif provider == "openai":
            # Use OpenAI API directly
            try:
                from openai import OpenAI
                
                client = OpenAI(api_key=api_key)
                model = "gpt-3.5-turbo"  # Default model
                
                def direct_chat(prompt):
                    try:
                        response = client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7,
                            max_tokens=1000
                        )
                        return response.choices[0].message.content
                    except Exception as e:
                        wfo_logger.error(f"OpenAI chat error: {e}")
                        return f"Error: {str(e)}"
                
                wfo_logger.info(f"Using OpenAI with model: {model}")
                return direct_chat
                
            except ImportError:
                wfo_logger.error("OpenAI package not installed. Run 'pip install openai'")
                return None
        
        else:
            wfo_logger.warning(f"Unknown provider: {provider}")
            return None
            
    except Exception as e:
        wfo_logger.error(f"Error initializing chat model: {e}")
        return None

def ask_chat_model(query, context=None):
    """Send a query to the chat model with optional context."""
    try:
        chat_model = get_chat_model()
        if not chat_model:
            wfo_logger.warning("Chat model not available. Skipping query.")
            return "Chat model not available."
        
        # Prepare the prompt with appropriate context
        if context:
            full_prompt = f"""
Context:
{context}

Query:
{query}

Please provide a concise, accurate response based on the given context.
"""
        else:
            full_prompt = query
        
        wfo_logger.debug(f"Querying chat model with prompt: {full_prompt[:100]}...")
        response = chat_model(full_prompt)
        wfo_logger.debug("Received response from chat model")
        return response
    except Exception as e:
        wfo_logger.error(f"Error querying chat model: {e}")
        return f"Error querying chat model: {e}"

def chat_model_available():
    """Check if the chat model is likely configured (checks settings and environment)."""
    try:
        # Check for API keys
        openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        github_token = os.environ.get("GITHUB_TOKEN")
        
        # Log key availability (without revealing the keys)
        if openrouter_api_key:
            wfo_logger.info("OPENROUTER_API_KEY is available in environment")
        else:
            wfo_logger.warning("OPENROUTER_API_KEY not found in environment")
            
        if openai_api_key:
            wfo_logger.info("OPENAI_API_KEY is available in environment")
        else:
            wfo_logger.warning("OPENAI_API_KEY not found in environment")
            
        if github_token:
            wfo_logger.info("GITHUB_TOKEN is available in environment")
        else:
            wfo_logger.warning("GITHUB_TOKEN not found in environment (required for asset pulling)")
        
        # Check if any API key is available
        api_key_available = bool(openrouter_api_key or openai_api_key)
        
        if not api_key_available:
            wfo_logger.warning("No API keys found. Set either OPENROUTER_API_KEY or OPENAI_API_KEY.")
            return False
            
        # Try to verify if the chat model exists
        chat_model = get_chat_model()
        return chat_model is not None
        
    except Exception as e:
        wfo_logger.warning(f"Could not check chat model configuration: {e}")
        return False

# --- Main Execution Block --- 
if __name__ == "__main__":
    try: # Add outer try block
        wfo_logger.info("Optimized WFO script starting...")
        
        # Ensure actual data fetcher is available, otherwise use placeholder
        try:
            from data.data_fetcher import fetch_historical_data as actual_fetch_historical_data
            wfo_logger.info("Using actual data_fetcher from data module.")
        except ImportError:
            wfo_logger.error("Actual data_fetcher not found. Using placeholder data function.")
            # Define a placeholder if the import fails, ensuring it matches expected signature
            def actual_fetch_historical_data(symbol, start_date, end_date, granularity_seconds):
                wfo_logger.warning(f"Using placeholder data for {symbol}")
                # Generate simple random walk data
                dates = pd.date_range(start=start_date, end=end_date, freq=pd.Timedelta(seconds=granularity_seconds))
                if not dates.empty:
                    price = 100 + np.random.randn(len(dates)).cumsum() * 0.5
                    return pd.DataFrame({
                        'open': price - np.random.rand(len(dates)) * 0.1,
                        'high': price + np.random.rand(len(dates)) * 0.1,
                        'low': price - np.random.rand(len(dates)) * 0.1,
                        'close': price,
                        'volume': np.random.rand(len(dates)) * 100 + 10
                    }, index=dates)
                else:
                    return pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
            
        # Check chat model availability
        if chat_model_available():
            wfo_logger.info("Chat model is configured and available.")
        else:
            wfo_logger.warning("Chat model is not available or not configured.")
        
        # Fetch data
        wfo_logger.info(f"Fetching historical data for {SYMBOL} | {GRANULARITY_STR} | {WFO_START_DATE} to {WFO_END_DATE}")
        try:
            data = actual_fetch_historical_data(SYMBOL, WFO_START_DATE, WFO_END_DATE, GRANULARITY_SECONDS)
            
            if data is None or data.empty:
                wfo_logger.error("Failed to fetch historical data or data is empty. Exiting.")
                sys.exit(1)
            
            # Data Validation/Cleaning 
            if data.isnull().values.any():
                wfo_logger.warning("Data contains NaN values. Attempting to forward fill.")
                data.ffill(inplace=True)
                data.bfill(inplace=True) 
                if data.isnull().values.any():
                     wfo_logger.error("Data still contains NaN values after fill. Exiting.")
                     sys.exit(1)
                     
            wfo_logger.info(f"Successfully fetched and validated {len(data)} data points.")
            
            # --- Checkpoint Loading ---
            last_split, train_results, oos_results, all_params = load_checkpoint()
            # Ensure results are lists even if checkpoint loading failed
            train_results = train_results or []
            oos_results = oos_results or []
            all_params = all_params or []
            # --- End Checkpoint Loading ---
            
            # Run the main WFO process, passing checkpoint data
            wfo_logger.info("Starting Walk-Forward Optimization run...")
            # Call run_walk_forward_optimization with resume parameters
            run_walk_forward_optimization(
                data, 
                PARAM_GRID, 
                OPTIMIZATION_METRIC, 
                IN_SAMPLE_DAYS, 
                OUT_SAMPLE_DAYS, 
                STEP_DAYS,
                resume_from_split=last_split,
                initial_train_results=train_results,
                initial_oos_results=oos_results,
                initial_all_params=all_params
            )
            
            # Summarize overall results (The function now handles saving/reporting internally)
            # wfo_logger.info("--- WFO Run Summary ---")
            
        except Exception as e:
            wfo_logger.exception(f"A critical error occurred during the WFO execution: {str(e)}") # Log full traceback
            if chat_model_available():
                try:
                    explanation = ask_chat_model(f"The WFO script encountered a critical error: {str(e)}. What are common causes and potential fixes based on the script structure?")
                    wfo_logger.info(f"AI Suggested Explanation/Fixes: {explanation}")
                except Exception as chat_err:
                    wfo_logger.error(f"Failed to get explanation from chat model: {chat_err}")
            sys.exit(1) # Exit with error status
        
        wfo_logger.info("Optimized WFO script finished successfully.")
        sys.exit(0) # Exit successfully 
        
    except Exception as main_error: # Catch any exception in the main block
        print(f"CRITICAL ERROR (captured by outer block): {main_error}", file=sys.stderr)
        traceback.print_exc() # Print traceback to stderr
        # Try to log it too, though file logging might not be working
        if 'wfo_logger' in locals():
            wfo_logger.critical(f"CRITICAL ERROR (captured by outer block): {main_error}")
            wfo_logger.exception("Traceback (Outer Block):")
        sys.exit(1) # Exit with error