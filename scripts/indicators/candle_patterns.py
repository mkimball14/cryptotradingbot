import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import pandas_ta as ta
import logging

# Setup logging
logger = logging.getLogger("candle_patterns")

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
        rename_map = {}
        for col in required_cols:
            if col not in df.columns and col.upper() in df.columns:
                rename_map[col.upper()] = col
        
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
        logger.error(f"Error extracting candle patterns: {str(e)}")
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
            logger.warning("No candle pattern columns found. Run extract_candle_patterns first.")
            return result_df
            
        # Create forward returns for 1, 3, and 5 days
        # First check if 'close' column exists
        if 'close' not in df.columns:
            logger.error("Missing 'close' column required for calculating returns")
            return result_df

        # Create return columns first
        result_df['return_1d'] = df['close'].pct_change(1).shift(-1)
        result_df['return_3d'] = df['close'].pct_change(3).shift(-3)
        result_df['return_5d'] = df['close'].pct_change(5).shift(-5)
        
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
                    # Calculate the average return after pattern
                    if current_value > 0:  # Bullish pattern
                        avg_return_1d = result_df.loc[hist_indices, 'return_1d'].mean()
                        avg_return_3d = result_df.loc[hist_indices, 'return_3d'].mean()
                        avg_return_5d = result_df.loc[hist_indices, 'return_5d'].mean()
                    else:  # Bearish pattern
                        avg_return_1d = -result_df.loc[hist_indices, 'return_1d'].mean()
                        avg_return_3d = -result_df.loc[hist_indices, 'return_3d'].mean()
                        avg_return_5d = -result_df.loc[hist_indices, 'return_5d'].mean()
                    
                    # Handle NaN values
                    avg_return_1d = 0 if pd.isna(avg_return_1d) else avg_return_1d
                    avg_return_3d = 0 if pd.isna(avg_return_3d) else avg_return_3d
                    avg_return_5d = 0 if pd.isna(avg_return_5d) else avg_return_5d
                    
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
        
        return result_df
        
    except Exception as e:
        logger.error(f"Error calculating candle pattern strength: {str(e)}")
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
            logger.warning("No candle pattern columns found. Run extract_candle_patterns first.")
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
        logger.error(f"Error generating candle pattern signals: {str(e)}")
        return pd.Series(False, index=df.index), pd.Series(False, index=df.index)


def optimize_pattern_signal_parameters(df: pd.DataFrame, 
                                      test_length: int = 252,
                                      min_trades: int = 10) -> Dict[str, Any]:
    """
    Optimize parameters for candle pattern signal generation.
    
    Args:
        df: DataFrame with candle pattern signals and price data
        test_length: Number of days to use for testing
        min_trades: Minimum number of trades required for valid optimization
    
    Returns:
        Dictionary of optimized parameters
    """
    try:
        # Split data into train and test
        train_df = df.iloc[:-test_length]
        test_df = df.iloc[-test_length:]
        
        # Define parameter ranges to test
        min_strength_values = [0.005, 0.01, 0.02, 0.03, 0.05, 0.1]
        lookback_values = [10, 20, 30, 50, 100]
        
        # Initialize best parameters and metrics
        best_params = {
            'min_strength': 0.01,
            'lookback': 20,
            'use_strength': True
        }
        best_sharpe = -np.inf
        
        # Test each parameter combination
        for min_strength in min_strength_values:
            for lookback in lookback_values:
                for use_strength in [True, False]:
                    # Generate strength metrics on training data
                    train_with_strength = get_candle_pattern_strength(train_df, lookback=lookback)
                    
                    # Apply to test data (simulating real-world scenario)
                    test_with_strength = get_candle_pattern_strength(test_df, lookback=lookback)
                    
                    # Generate signals on test data
                    buy_signals, sell_signals = generate_candle_pattern_signals(
                        test_with_strength, 
                        min_strength=min_strength,
                        use_strength=use_strength
                    )
                    
                    # Count number of signals
                    num_buys = buy_signals.sum()
                    num_sells = sell_signals.sum()
                    
                    # Skip if too few trades
                    if num_buys + num_sells < min_trades:
                        continue
                    
                    # Calculate returns based on signals
                    # Simple implementation: buy on buy signal, sell on sell signal, hold otherwise
                    positions = pd.Series(0, index=test_df.index)
                    positions[buy_signals] = 1
                    positions[sell_signals] = -1
                    
                    # Calculate daily returns
                    daily_returns = test_df['close'].pct_change() * positions.shift(1)
                    
                    # Skip if not enough data points
                    if daily_returns.count() < 20:
                        continue
                    
                    # Calculate Sharpe ratio (annualized)
                    sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
                    
                    # Update best parameters if better Sharpe
                    if pd.notna(sharpe) and sharpe > best_sharpe:
                        best_sharpe = sharpe
                        best_params = {
                            'min_strength': min_strength,
                            'lookback': lookback,
                            'use_strength': use_strength,
                            'sharpe': sharpe,
                            'num_buys': num_buys,
                            'num_sells': num_sells
                        }
        
        logger.info(f"Optimized candle pattern parameters: {best_params}")
        return best_params
        
    except Exception as e:
        logger.error(f"Error optimizing pattern signal parameters: {str(e)}")
        return {
            'min_strength': 0.01,
            'lookback': 20,
            'use_strength': True
        } 