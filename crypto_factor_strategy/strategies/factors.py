import pandas as pd
import numpy as np
from numba import njit # Import njit
import logging # Added for logging

logger = logging.getLogger(__name__)

# Step 3: Universe Definition (Static Example)
# Define your universe (choose symbols with good data availability on Coinbase)
UNIVERSE = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'XRP-USD', 'DOGE-USD', 'MATIC-USD', 'DOT-USD', 'AVAX-USD', 'LINK-USD']
# Ensure these symbols exist on Coinbase Advanced Trading and have sufficient history via API.


# Step 4: Factor Definition & Calculation

# Example Factor 1: Momentum (Pandas is usually efficient enough)
def calculate_momentum(close_prices, window=63): # Approx 3 months of trading days
    """Calculates price momentum (percent change) over a window."""
    if not isinstance(close_prices.index, pd.MultiIndex):
        logger.error("Momentum input must be a MultiIndex DataFrame [date, symbol].")
        return None
    # Ensure data is sorted for correct rolling calculations within groups
    close_prices_sorted = close_prices.sort_index()
    try:
        # Calculate percentage change within each symbol group
        momentum = close_prices_sorted.groupby(level='symbol', group_keys=False).pct_change(periods=window, fill_method=None)
        return momentum
    except Exception as e:
        logger.error(f"Error calculating momentum: {e}")
        return None

# Example Factor 2: Volatility (Pandas rolling is often efficient)
def calculate_volatility(close_prices, window=21): # Approx 1 month
    """Calculates rolling historical volatility (std dev of daily returns)."""
    if not isinstance(close_prices.index, pd.MultiIndex):
        logger.error("Volatility input must be a MultiIndex DataFrame [date, symbol].")
        return None
    # Ensure data is sorted
    close_prices_sorted = close_prices.sort_index()
    try:
        # Calculate daily returns within each group
        returns = close_prices_sorted.groupby(level='symbol', group_keys=False).pct_change(fill_method=None)
        # Calculate rolling standard deviation on returns within each group
        volatility = returns.groupby(level='symbol', group_keys=False).rolling(window=window, min_periods=int(window*0.8)).std()
        # Rolling adds the original index levels back, drop the 'symbol' level added by groupby inside rolling if needed
        # volatility = volatility.reset_index(level=0, drop=True) # This might be needed depending on pandas version
        return volatility.droplevel(0) # simpler way to remove symbol level added by rolling
    except Exception as e:
        logger.error(f"Error calculating volatility: {e}")
        return None


# Example Factor 3: Custom Factor using Numba for potential speedup
@njit # Decorator to compile this function with Numba
def _custom_factor_logic_nb(close_array, window):
    """Numba-compiled function for custom factor logic (example: price / rolling max)."""
    # Numba works best with NumPy arrays and supported operations
    num_rows = close_array.shape[0]
    output = np.full(num_rows, np.nan, dtype=np.float64)
    if window <= 0 or window > num_rows:
         return output

    for i in range(window - 1, num_rows):
        window_slice = close_array[i - window + 1 : i + 1]
        # Ignore NaNs in the window slice for max calculation
        if np.all(np.isnan(window_slice)):
             continue # Skip if window is all NaNs
        rolling_max = np.nanmax(window_slice)
        if rolling_max > 1e-9: # Avoid division by zero or tiny numbers
             output[i] = close_array[i] / rolling_max
    return output

def calculate_custom_factor(close_prices, window=30):
     """Calculates a custom factor, using Numba for core logic."""
     if not isinstance(close_prices.index, pd.MultiIndex):
        logger.error("Custom Factor input must be a MultiIndex DataFrame [date, symbol].")
        return None
     # Ensure data is sorted
     close_prices_sorted = close_prices.sort_index()
     try:
         # Apply the Numba function to the NumPy array of each group
         # group_keys=False prevents adding the group key back into the index
         custom_factor = close_prices_sorted.groupby(level='symbol', group_keys=False).apply(
             lambda x: pd.Series(_custom_factor_logic_nb(x.to_numpy(), window), index=x.index)
         )
         return custom_factor
     except Exception as e:
         logger.error(f"Error calculating custom factor: {e}")
         return None

# New Factor: Mean Reversion - Z-score of price deviation from moving average
@njit
def _mean_reversion_logic_nb(close_array, ma_window=50, z_window=20):
    """
    Numba-compiled function for mean reversion logic.
    Calculates z-score of price deviation from its moving average.
    
    Args:
        close_array: Array of closing prices
        ma_window: Window for calculating the moving average
        z_window: Window for calculating the z-score
        
    Returns:
        Array of mean reversion z-scores
    """
    num_rows = close_array.shape[0]
    # Initialize output arrays
    ma_array = np.full(num_rows, np.nan, dtype=np.float64)
    deviation = np.full(num_rows, np.nan, dtype=np.float64)
    z_scores = np.full(num_rows, np.nan, dtype=np.float64)
    
    # Calculate moving average
    for i in range(ma_window - 1, num_rows):
        window_slice = close_array[i - ma_window + 1 : i + 1]
        if not np.all(np.isnan(window_slice)):
            ma_array[i] = np.nanmean(window_slice)
    
    # Calculate deviation from moving average
    for i in range(ma_window - 1, num_rows):
        if not np.isnan(ma_array[i]) and not np.isnan(close_array[i]):
            # Deviation as percentage from moving average
            deviation[i] = (close_array[i] / ma_array[i]) - 1.0
    
    # Calculate z-score of deviation using rolling window
    for i in range(ma_window + z_window - 2, num_rows):
        window_slice = deviation[i - z_window + 1 : i + 1]
        if not np.all(np.isnan(window_slice)):
            mean_dev = np.nanmean(window_slice)
            std_dev = np.nanstd(window_slice)
            if std_dev > 1e-9:  # Avoid division by near-zero
                z_scores[i] = (deviation[i] - mean_dev) / std_dev
    
    return z_scores

def calculate_mean_reversion(close_prices, ma_window=50, z_window=20):
    """
    Calculates the mean reversion factor using z-scores of price deviations from moving averages.
    Mean reversion is negative when price is above its average (expecting reversion down)
    and positive when price is below its average (expecting reversion up).
    
    Args:
        close_prices: MultiIndex DataFrame with ['date', 'symbol'] index and close prices
        ma_window: Window for calculating the moving average
        z_window: Window for calculating the z-score
        
    Returns:
        Series with mean reversion values (negative values suggest overbought conditions)
    """
    if not isinstance(close_prices.index, pd.MultiIndex):
        logger.error("Mean Reversion input must be a MultiIndex DataFrame [date, symbol].")
        return None
        
    # Ensure data is sorted
    close_prices_sorted = close_prices.sort_index()
    
    try:
        # Apply the Numba function to each symbol group
        mean_reversion = close_prices_sorted.groupby(level='symbol', group_keys=False).apply(
            lambda x: pd.Series(
                _mean_reversion_logic_nb(x.to_numpy(), ma_window=ma_window, z_window=z_window), 
                index=x.index
            )
        )
        
        # Negate the z-score so positive values indicate expected price increase
        # (aligns with other factors where higher = better)
        return -mean_reversion
        
    except Exception as e:
        logger.error(f"Error calculating mean reversion: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

# New Factor: Relative Strength - Compare each asset's performance to BTC-USD
def calculate_relative_strength(close_prices, window=30, benchmark_symbol='BTC-USD'):
    """
    Calculates relative strength by comparing each asset's return to the benchmark (BTC-USD).
    
    Args:
        close_prices: MultiIndex DataFrame with ['date', 'symbol'] index and close prices
        window: Lookback period in days
        benchmark_symbol: Symbol to use as benchmark (default: 'BTC-USD')
        
    Returns:
        Series with relative strength values (>1 means outperforming the benchmark)
    """
    if not isinstance(close_prices.index, pd.MultiIndex):
        logger.error("Relative strength input must be a MultiIndex DataFrame [date, symbol].")
        return None
        
    try:
        # Ensure data is sorted
        close_prices_sorted = close_prices.sort_index()
        
        # Calculate returns for each symbol
        returns = close_prices_sorted.groupby(level='symbol').pct_change(periods=window, fill_method=None)
        
        # Extract benchmark returns if available
        if benchmark_symbol not in close_prices_sorted.index.get_level_values('symbol').unique():
            logger.warning(f"Benchmark symbol {benchmark_symbol} not found in data. Using first symbol instead.")
            benchmark_symbol = close_prices_sorted.index.get_level_values('symbol').unique()[0]
        
        try:    
            benchmark_returns = returns.xs(benchmark_symbol, level='symbol')
            
            # Create a MultiIndex DataFrame to properly align benchmark returns with all symbols
            dates = returns.index.get_level_values('date').unique()
            symbols = returns.index.get_level_values('symbol').unique()
            
            # Initialize the benchmark return DataFrame with proper MultiIndex
            multi_idx = pd.MultiIndex.from_product([symbols, dates], names=['symbol', 'date'])
            benchmark_df = pd.DataFrame(index=multi_idx, columns=['benchmark_return'])
            
            # Fill benchmark returns for each date
            for date in dates:
                if date in benchmark_returns.index:
                    benchmark_value = benchmark_returns.loc[date]
                    # Set the same benchmark value for all symbols on this date
                    idx = pd.IndexSlice
                    benchmark_df.loc[idx[:, date], 'benchmark_return'] = benchmark_value
            
            # Reindex and align benchmark returns with original returns
            benchmark_df = benchmark_df.reindex(returns.index)
            
            # Calculate relative strength (asset return - benchmark return)
            # Adding 1 to both sides to get a ratio (>1 means outperforming)
            benchmark_returns_aligned = benchmark_df['benchmark_return']
            relative_strength = (1 + returns) / (1 + benchmark_returns_aligned)
            
            return relative_strength
        except KeyError as e:
            logger.error(f"KeyError in relative strength calculation: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            # Fallback approach in case of index issues
            benchmark_returns = []
            for date in returns.index.get_level_values('date').unique():
                try:
                    # Get benchmark return for this date
                    benchmark_return = returns.xs((benchmark_symbol, date), level=['symbol', 'date'])
                    benchmark_returns.append((date, benchmark_return))
                except:
                    # Skip dates where benchmark is not available
                    continue
            
            # Create aligned series
            benchmark_series = pd.Series(
                data=[x[1] for x in benchmark_returns],
                index=[x[0] for x in benchmark_returns]
            )
            
            # Calculate relative strength manually for each symbol and date
            result = []
            for symbol in returns.index.get_level_values('symbol').unique():
                if symbol == benchmark_symbol:
                    # Skip benchmark itself
                    continue
                
                symbol_returns = returns.xs(symbol, level='symbol')
                for date, ret in symbol_returns.items():
                    if date in benchmark_series.index:
                        benchmark_ret = benchmark_series[date]
                        relative_str = (1 + ret) / (1 + benchmark_ret)
                        result.append(((symbol, date), relative_str))
            
            # Convert to Series with MultiIndex
            result_idx = pd.MultiIndex.from_tuples([x[0] for x in result], names=['symbol', 'date'])
            relative_strength = pd.Series(
                data=[x[1] for x in result],
                index=result_idx
            )
            
            return relative_strength
            
    except Exception as e:
        logger.error(f"Error calculating relative strength: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


# Step 5: Factor Preprocessing & Combination

def cross_sectional_rank(factor_series):
    """Ranks factor values cross-sectionally at each time step."""
    if not isinstance(factor_series.index, pd.MultiIndex):
        logger.error("Cross-sectional rank input must be a MultiIndex Series/DataFrame.")
        return None
    try:
        # Group by date and rank within each date group
        ranked = factor_series.groupby(level='date', group_keys=False).rank(method='first', pct=True, na_option='keep')
        return ranked
    except Exception as e:
        logger.error(f"Error calculating cross-sectional rank: {e}")
        return None

def cross_sectional_zscore(factor_series):
    """Z-scores factor values cross-sectionally at each time step."""
    if not isinstance(factor_series.index, pd.MultiIndex):
        logger.error("Cross-sectional z-score input must be a MultiIndex Series/DataFrame.")
        return None
    try:
        group = factor_series.groupby(level='date', group_keys=False)
        # Handle dates with zero std dev robustly
        def zscore(x):
            std = x.std()
            if std < 1e-9: # Check for near-zero std dev to avoid division by zero
                # Return zeros or NaNs, depending on desired handling. Zeros might be safer.
                return np.zeros_like(x)
            return (x - x.mean()) / std

        zscored = group.transform(zscore)
        return zscored
    except Exception as e:
        logger.error(f"Error calculating cross-sectional z-score: {e}")
        return None


# --- Example Usage within a class or main script (demonstration) ---
# if __name__ == '__main__':
#     # This block only runs if the script is executed directly
#     logger.info("Running factors.py example...")
#
#     # We need data to run this example. Let's try importing from data_utils
#     # Use relative import for direct script execution
#     from .data_utils import load_coinbase_data
#
#     # Use the same test parameters as in data_utils
#     example_universe = UNIVERSE[:2] # Use first 2 symbols for speed
#     start_dt_iso = '2023-01-01T00:00:00Z'
#     end_dt_iso = '2024-01-01T00:00:00Z'
#     data_granularity = 'ONE_DAY'
#
#     logger.info(f"Loading data for {example_universe}...")
#     ohlcv_data = load_coinbase_data(
#         symbols=example_universe,
#         start_iso=start_dt_iso,
#         end_iso=end_dt_iso,
#         granularity=data_granularity
#     )
#
#     if ohlcv_data is not None and not ohlcv_data.empty:
#         logger.info("Data loaded successfully. Calculating factors...")
#         close = ohlcv_data['close'] # Ensure 'close' column exists
#
#         # Calculate factors
#         mom_factor = calculate_momentum(close, window=63)
#         vol_factor = calculate_volatility(close, window=21)
#         custom_factor = calculate_custom_factor(close, window=30)
#
#         # Combine into a DataFrame
#         factor_data = pd.DataFrame({
#             'momentum_3m': mom_factor,
#             'volatility_1m': vol_factor,
#             'custom_factor': custom_factor
#         })
#
#         print("\n--- Raw Factor Data Sample (Tail) ---")
#         print(factor_data.tail())
#
#         # Drop rows with NaNs resulting from lookback periods
#         original_count = len(factor_data)
#         factor_data = factor_data.dropna()
#         print(f"\nDropped {original_count - len(factor_data)} rows with NaNs in factors.")
#
#         if not factor_data.empty:
#             print("\n--- Cleaned Factor Data Sample (Tail) ---")
#             print(factor_data.tail())
#
#             # Preprocess factors (Example: Ranking)
#             processed_factors = pd.DataFrame(index=factor_data.index)
#             processed_factors['momentum_rank'] = cross_sectional_rank(factor_data['momentum_3m'])
#             # Invert volatility rank if lower is better (multiply by -1 before ranking)
#             processed_factors['volatility_rank'] = cross_sectional_rank(-factor_data['volatility_1m'])
#             processed_factors['custom_rank'] = cross_sectional_rank(factor_data['custom_factor'])
#
#             # Drop any potential remaining NaNs after processing (e.g., if a whole day had NaNs)
#             processed_factors = processed_factors.dropna()
#
#             if not processed_factors.empty:
#                  print("\n--- Processed (Ranked) Factor Data Sample (Tail) ---")
#                  print(processed_factors.tail())
#
#                  # Combine factors (Example: Equal Weighting)
#                  num_factors = len(processed_factors.columns)
#                  combined_score = processed_factors.sum(axis=1) / num_factors
#
#                  # Add to the main factor data frame (or keep separate)
#                  factor_data_aligned = factor_data.loc[combined_score.index] # Align index
#                  factor_data_aligned['combined_score'] = combined_score
#
#                  print("\n--- Combined Score Sample (Tail) ---")
#                  print(factor_data_aligned[['combined_score']].tail())
#
#             else:
#                  logger.warning("No data remaining after processing factors.")
#         else:
#             logger.warning("No data remaining after dropping NaNs from raw factors.")
#
#     else:
#         logger.error("Failed to load data for factor calculation example.") 