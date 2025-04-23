import pandas as pd
import numpy as np # Import numpy
import logging

logger = logging.getLogger(__name__)

def calculate_equal_weights(symbols, dates):
    """
    Calculate equal weights for all symbols on all dates.
    
    Args:
        symbols: List of symbols to include
        dates: List of dates to create weights for
        
    Returns:
        MultiIndex Series with equal weights for all symbols on all dates
    """
    try:
        # Create a MultiIndex with all combinations of date and symbol
        multi_index = pd.MultiIndex.from_product(
            [dates, symbols], 
            names=['date', 'symbol']
        )
        
        # Create equal weights (1/n for each symbol)
        weight_value = 1.0 / len(symbols)
        weights = pd.Series(weight_value, index=multi_index)
        
        return weights
    except Exception as e:
        logger.error(f"Error calculating equal weights: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def calculate_top_n_weights(scores, n=3, max_weight_per_asset=None):
    """Calculates equal weights for the top N assets based on score, with optional capping."""
    if not isinstance(scores.index, pd.MultiIndex):
        logger.error("Scores input must be a MultiIndex Series/DataFrame.")
        return None
    if scores.isnull().all():
        logger.warning("All scores are NaN, cannot calculate weights.")
        return pd.Series(0.0, index=scores.index)

    try:
        # Use the appropriate level name
        date_level = scores.index.names[0] if scores.index.names[0] == 'date' else 'date'
        
        ranks = scores.groupby(level=date_level).rank(ascending=False, method='first')
        is_top_n = (ranks <= n)
        
        # Count number of assets selected each day
        assets_per_day = is_top_n.groupby(level=date_level).sum()
        
        # Calculate base equal weight
        base_weight = (1.0 / assets_per_day).replace([np.inf, -np.inf, np.nan], 0)
        
        # Apply weights only to top N assets
        target_weights = pd.Series(0.0, index=scores.index)
        
        # Iterate through dates to apply weights - ensure this works with any valid MultiIndex structure
        for date in scores.index.get_level_values(date_level).unique():
            day_assets = is_top_n.xs(date, level=date_level)
            if day_assets.sum() > 0:
                weight = base_weight.loc[date]
                
                # Build multi-index selectors properly
                for symbol, selected in day_assets.items():
                    if selected:
                        # Match the original index structure
                        if date_level == 'date':
                            idx = (date, symbol)
                        else:
                            idx = (symbol, date)
                        target_weights.loc[idx] = weight
        
        # Apply max weight cap if specified
        if max_weight_per_asset is not None:
            target_weights = target_weights.clip(upper=max_weight_per_asset)
            # Optional: Re-normalize weights per day if capping occurred
            # total_weights = target_weights.groupby(level='date').sum()
            # target_weights = target_weights.div(total_weights, level='date')
            
        return target_weights
    
    except Exception as e:
        logger.error(f"Error calculating top N weights: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def calculate_long_short_quintile_weights(scores, leverage=1.0):
    """Calculates weights for a long/short portfolio based on score quintiles."""
    if not isinstance(scores.index, pd.MultiIndex):
        logger.error("Scores input must be a MultiIndex Series/DataFrame.")
        return None
    if scores.isnull().all():
        logger.warning("All scores are NaN, cannot calculate weights.")
        return pd.Series(0.0, index=scores.index)

    try:
        # Use the appropriate level name
        date_level = scores.index.names[0] if scores.index.names[0] == 'date' else 'date'
        
        ranks = scores.groupby(level=date_level).rank(method='first', pct=True)
        
        long_quintile = ranks >= 0.8  # Top 20%
        short_quintile = ranks <= 0.2  # Bottom 20%
        
        raw_weights = pd.Series(0.0, index=scores.index)
        raw_weights[long_quintile] = 1.0
        raw_weights[short_quintile] = -1.0
        
        # Create dollar-neutral portfolio weights
        def normalize_ls_weights(group):
            longs = group[group > 0]
            shorts = group[group < 0]
            
            # Equal weight longs and shorts
            if len(longs) > 0:
                group[group > 0] = (leverage / 2.0) / len(longs)
            if len(shorts) > 0:
                group[group < 0] = (-leverage / 2.0) / len(shorts)
                
            return group
            
        target_weights = raw_weights.groupby(level=date_level).transform(normalize_ls_weights)
        return target_weights
        
    except Exception as e:
        logger.error(f"Error calculating long/short quintile weights: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def predict_asset_volatility(returns, window=60, min_periods=20, std_type='ewm', halflife=30):
    """
    Predicts asset volatility based on historical returns.
    
    Args:
        returns: DataFrame or Series of asset returns
        window: Window size for rolling volatility
        min_periods: Minimum number of periods required for calculation
        std_type: Type of standard deviation calculation ('rolling' or 'ewm')
        halflife: Halflife for exponentially weighted calculations
        
    Returns:
        DataFrame or Series of predicted volatilities (annualized)
    """
    if not isinstance(returns.index, pd.MultiIndex):
        logger.error("Returns input must be a MultiIndex Series/DataFrame.")
        return None
        
    try:
        # Sort index to ensure time-series operations work correctly
        returns_sorted = returns.sort_index()
        
        # Calculate volatility based on specified method
        if std_type == 'rolling':
            # Simple rolling window volatility
            volatility = returns_sorted.groupby(level='symbol').rolling(
                window=window, 
                min_periods=min_periods
            ).std().droplevel(0)
            
        elif std_type == 'ewm':
            # Exponentially weighted volatility (gives more weight to recent observations)
            volatility = returns_sorted.groupby(level='symbol').apply(
                lambda x: x.ewm(halflife=halflife, min_periods=min_periods).std()
            ).droplevel(0)
        
        else:
            raise ValueError(f"Invalid std_type: {std_type}. Use 'rolling' or 'ewm'.")
        
        # Annualize volatility (√252 for daily returns)
        annualized_vol = volatility * np.sqrt(252)
        
        return annualized_vol
        
    except Exception as e:
        logger.error(f"Error predicting asset volatility: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def calculate_portfolio_volatility(weights, returns, cov_window=60, min_periods=20, method='simple'):
    """
    Calculates predicted portfolio volatility based on weights and covariance matrix.
    
    Args:
        weights: MultiIndex Series with portfolio weights
        returns: MultiIndex DataFrame with asset returns
        cov_window: Window for covariance calculation
        min_periods: Minimum periods for calculation
        method: 'simple' for historical cov, 'ewm' for exponentially weighted
        
    Returns:
        Series of predicted portfolio volatility per date (annualized)
    """
    if not isinstance(weights.index, pd.MultiIndex) or not isinstance(returns.index, pd.MultiIndex):
        logger.error("Weights and returns inputs must be MultiIndex Series/DataFrames.")
        return None
        
    try:
        # Group by date to calculate portfolio volatility for each date
        result = {}
        
        # Get unique dates from weights
        dates = weights.index.get_level_values('date').unique()
        
        for date in dates:
            # Get weights for this date
            date_weights = weights.xs(date, level='date')
            
            # Skip dates with no positions
            if date_weights.sum() == 0:
                result[date] = 0.0
                continue
                
            # Get historical returns for covariance calculation 
            # (lookback from current date based on cov_window)
            hist_dates = returns.index.get_level_values('date')
            historical_dates = hist_dates[hist_dates <= date].unique()[-cov_window:]
            
            if len(historical_dates) < min_periods:
                # Not enough history yet
                result[date] = np.nan
                continue
                
            # Get returns for symbols with weights on relevant historical dates
            symbols = date_weights.index
            historical_returns = {}
            
            for symbol in symbols:
                if date_weights[symbol] == 0:
                    continue
                    
                try:
                    # Extract historical returns for this symbol
                    symbol_returns = returns.xs(symbol, level='symbol')
                    symbol_hist = symbol_returns.loc[symbol_returns.index.isin(historical_dates)]
                    
                    if not symbol_hist.empty:
                        historical_returns[symbol] = symbol_hist
                except:
                    # Symbol might not have data for this period
                    continue
            
            # Convert returns to a dataframe for covariance calculation
            if len(historical_returns) < 2:
                # Need at least 2 assets for meaningful covariance
                if len(historical_returns) == 1:
                    # For one asset, just use its own volatility
                    symbol = list(historical_returns.keys())[0]
                    result[date] = historical_returns[symbol].std() * np.sqrt(252) * date_weights[symbol]
                else:
                    result[date] = np.nan
                continue
                
            # Create returns dataframe for covariance calculation
            returns_df = pd.DataFrame(historical_returns)
            
            # Calculate covariance matrix
            if method == 'ewm':
                # Exponentially weighted covariance (more weight to recent data)
                cov_matrix = returns_df.ewm(halflife=cov_window/2).cov()
                # Get the last period's covariance matrix
                last_date = returns_df.index[-1]
                cov_matrix = cov_matrix.loc[last_date]
            else:
                # Simple historical covariance
                cov_matrix = returns_df.cov()
            
            # Extract weights for symbols with data
            active_symbols = returns_df.columns
            active_weights = date_weights[active_symbols]
            
            # Normalize weights to sum to 1
            if active_weights.sum() > 0:
                active_weights = active_weights / active_weights.sum()
            
            # Calculate portfolio variance (w^T * Cov * w)
            # Convert to NumPy for matrix multiplication
            w = active_weights.values
            C = cov_matrix.values
            
            try:
                portfolio_variance = w.T @ C @ w
                # Convert to annualized volatility
                portfolio_vol = np.sqrt(portfolio_variance * 252)
                result[date] = portfolio_vol
            except:
                result[date] = np.nan
        
        # Convert result to Series
        return pd.Series(result)
        
    except Exception as e:
        logger.error(f"Error calculating portfolio volatility: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def calculate_volatility_targeted_weights(weights, returns, target_vol=0.15, max_leverage=1.5, cov_window=60, vol_cap=0.5):
    """
    Scales portfolio weights to target a specific volatility level.
    
    Args:
        weights: MultiIndex Series with portfolio weights
        returns: MultiIndex DataFrame with asset returns
        target_vol: Target annualized volatility (e.g., 0.15 for 15%)
        max_leverage: Maximum allowed sum of absolute weights
        cov_window: Window for covariance calculation
        vol_cap: Maximum allowed predicted volatility for scaling calculation
        
    Returns:
        MultiIndex Series with scaled weights targeting specific volatility
    """
    if weights is None or returns is None:
        logger.error("Weights and returns inputs cannot be None")
        return None
        
    if not isinstance(weights.index, pd.MultiIndex) or not isinstance(returns.index, pd.MultiIndex):
        logger.error("Weights and returns inputs must be MultiIndex Series/DataFrames")
        return None
        
    try:
        # Calculate predicted portfolio volatility
        predicted_vol = calculate_portfolio_volatility(weights, returns, cov_window=cov_window)
        
        if predicted_vol is None:
            logger.error("Failed to calculate portfolio volatility")
            return weights
            
        # Create new weights Series with same index as original
        scaled_weights = pd.Series(0.0, index=weights.index)
        
        # Get unique dates
        dates = weights.index.get_level_values('date').unique()
        
        for date in dates:
            # Get original weights for this date
            date_weights = weights.xs(date, level='date')
            
            # Skip if no positions on this date
            if date_weights.sum() == 0:
                continue
                
            # Get predicted vol for this date
            if date in predicted_vol.index:
                vol = predicted_vol[date]
                
                # Skip if vol is NaN or zero
                if pd.isna(vol) or vol == 0:
                    # Copy original weights
                    for symbol, weight in date_weights.items():
                        idx = (date, symbol)
                        scaled_weights.loc[idx] = weight
                    continue
                    
                # Cap volatility for scaling calculation to avoid extreme leverage
                vol = min(vol, vol_cap)
                
                # Calculate scaling factor
                scaling_factor = target_vol / vol
                
                # Apply leverage cap
                scaling_factor = min(scaling_factor, max_leverage)
                
                # Scale weights
                for symbol, weight in date_weights.items():
                    idx = (date, symbol)
                    scaled_weights.loc[idx] = weight * scaling_factor
            else:
                # If we don't have predicted vol for this date, use original weights
                for symbol, weight in date_weights.items():
                    idx = (date, symbol)
                    scaled_weights.loc[idx] = weight
        
        return scaled_weights
        
    except Exception as e:
        logger.error(f"Error calculating volatility targeted weights: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return weights  # Fall back to original weights


def combine_factors(factor_data, factor_weights, z_score=True):
    """
    Combine multiple factors into a single factor using a weighted average.
    
    Parameters:
    -----------
    factor_data : dict
        Dictionary of factor DataFrames with MultiIndex (date, symbol)
    factor_weights : dict
        Dictionary of factor weights, keys should match factor_data keys
    z_score : bool, default=True
        Whether to normalize factors to z-scores before combining
        
    Returns:
    --------
    combined_factor : pandas.DataFrame
        DataFrame with combined factor values, MultiIndex (date, symbol)
    """
    logger.info(f"Combining factors with weights: {factor_weights}")
    
    # Validate inputs
    if not factor_data or not factor_weights:
        logger.error("Empty factor data or weights provided")
        return None
    
    # Ensure all factors exist in factor_data
    missing_factors = [f for f in factor_weights if f not in factor_data]
    if missing_factors:
        logger.error(f"The following factors are missing in factor_data: {missing_factors}")
        return None
    
    # Initialize with the first factor to get the index structure
    first_factor = list(factor_data.keys())[0]
    
    # Create a copy to avoid modifying the original data
    processed_factors = {}
    
    for factor_name, factor_df in factor_data.items():
        if factor_name not in factor_weights:
            logger.warning(f"Factor {factor_name} has no weight, skipping")
            continue
            
        # Skip factors with zero weight
        if factor_weights[factor_name] == 0:
            logger.info(f"Skipping factor {factor_name} due to zero weight")
            continue
            
        # Deep copy to avoid modifying original data
        processed_factors[factor_name] = factor_df.copy()
    
    # Ensure we have at least one factor with non-zero weight
    if not processed_factors:
        logger.error("No factors with non-zero weights found")
        return None
    
    # Normalize factors if requested
    if z_score:
        for factor_name in processed_factors:
            try:
                # Group by date and apply z-score normalization
                if len(processed_factors[factor_name]) > 0:
                    # Count NaN values before normalization
                    nan_count_before = processed_factors[factor_name].isna().sum().sum()
                    logger.debug(f"Factor {factor_name} has {nan_count_before} NaN values before normalization")
                    
                    # Group by date and calculate z-scores
                    processed_factors[factor_name] = processed_factors[factor_name].groupby(
                        level='date'
                    ).transform(
                        lambda x: (x - x.mean()) / x.std() if x.std() != 0 else 0
                    )
                    
                    # Count NaN values after normalization
                    nan_count_after = processed_factors[factor_name].isna().sum().sum()
                    logger.debug(f"Factor {factor_name} has {nan_count_after} NaN values after normalization")
                    
                    # If normalization introduced new NaNs (likely due to all values being the same)
                    if nan_count_after > nan_count_before:
                        logger.warning(f"Normalization introduced {nan_count_after - nan_count_before} new NaN values for factor {factor_name}")
                        
                        # Replace NaNs with zeros where std was zero (all values the same)
                        group_std = processed_factors[factor_name].groupby(level='date').std()
                        zero_std_dates = group_std[group_std == 0].index
                        
                        # For dates with zero std, replace NaNs with zeros
                        for date in zero_std_dates:
                            idx = pd.IndexSlice
                            processed_factors[factor_name].loc[idx[date, :]] = processed_factors[factor_name].loc[idx[date, :]].fillna(0)
            except Exception as e:
                logger.error(f"Error normalizing factor {factor_name}: {str(e)}")
                # If normalization fails, use the original factor
                processed_factors[factor_name] = factor_data[factor_name].copy()
    
    # Find the common index across all factors
    common_idx = None
    
    for factor_df in processed_factors.values():
        if common_idx is None:
            common_idx = factor_df.index
        else:
            common_idx = common_idx.intersection(factor_df.index)
    
    if common_idx is None or len(common_idx) == 0:
        logger.error("No common index across factors")
        return None
    
    logger.info(f"Common index has {len(common_idx)} entries")
    
    # Align all factors to the common index
    aligned_factors = {}
    for factor_name, factor_df in processed_factors.items():
        aligned_factors[factor_name] = factor_df.reindex(common_idx)
        
        # Count NaN values after alignment
        nan_count = aligned_factors[factor_name].isna().sum().sum()
        logger.debug(f"Factor {factor_name} has {nan_count} NaN values after alignment")
    
    # Create a DataFrame to store all aligned factors
    factor_columns = {f: aligned_factors[f] for f in aligned_factors}
    all_factors_df = pd.DataFrame(factor_columns)
    
    # Handle NaN values before combining
    # Strategy 1: Fill NaNs with neutral values (0 for z-scored factors)
    for factor_name in all_factors_df.columns:
        nan_count = all_factors_df[factor_name].isna().sum()
        if nan_count > 0:
            logger.warning(f"Filling {nan_count} NaN values in factor {factor_name} with 0")
            all_factors_df[factor_name] = all_factors_df[factor_name].fillna(0)
    
    # Combine factors using weighted average
    weights_sum = sum(factor_weights[f] for f in all_factors_df.columns)
    
    # Ensure weights sum to 1
    normalized_weights = {f: factor_weights[f] / weights_sum for f in all_factors_df.columns}
    logger.info(f"Normalized weights: {normalized_weights}")
    
    # Apply weights and sum
    combined_factor = pd.Series(0, index=common_idx)
    for factor_name in all_factors_df.columns:
        combined_factor += all_factors_df[factor_name] * normalized_weights[factor_name]
    
    # Final check for any remaining NaNs
    nan_count = combined_factor.isna().sum()
    if nan_count > 0:
        logger.warning(f"Combined factor still has {nan_count} NaN values, filling with 0")
        combined_factor = combined_factor.fillna(0)
    
    logger.info(f"Successfully combined {len(all_factors_df.columns)} factors")
    return combined_factor

def calculate_portfolio_weights(factor_data, factor_weights, universe, equal_weighted=False):
    """
    Calculate portfolio weights based on combined factor values.
    
    Parameters:
    -----------
    factor_data : dict
        Dictionary of factor DataFrames with MultiIndex (date, symbol)
    factor_weights : dict
        Dictionary of factor weights, keys should match factor_data keys
    universe : list
        List of symbols to include in the portfolio
    equal_weighted : bool, default=False
        If True, ignore factors and use equal weights for all assets
        
    Returns:
    --------
    weights : pandas.DataFrame
        DataFrame with portfolio weights, MultiIndex (date, symbol)
    """
    logger.info(f"Calculating portfolio weights for universe of {len(universe)} assets")
    
    if equal_weighted:
        logger.info("Using equal weights for all assets")
        
        # Get the dates from the first factor
        first_factor = list(factor_data.values())[0]
        dates = first_factor.index.get_level_values('date').unique()
        
        # Create equal weights for all assets in the universe
        weights_data = []
        for date in dates:
            for symbol in universe:
                weights_data.append({
                    'date': date,
                    'symbol': symbol,
                    'weight': 1.0 / len(universe)
                })
        
        weights = pd.DataFrame(weights_data)
        weights = weights.set_index(['date', 'symbol'])['weight']
        return weights
    
    # Combine factors
    combined_factor = combine_factors(factor_data, factor_weights)
    
    if combined_factor is None or combined_factor.empty:
        logger.error("Failed to combine factors, cannot calculate weights")
        return None
    
    # Calculate weights based on combined factor
    weights = pd.DataFrame(index=combined_factor.index)
    weights['combined_factor'] = combined_factor
    
    # Filter to include only universe symbols
    universe_set = set(universe)
    weights = weights.reset_index()
    weights = weights[weights['symbol'].isin(universe_set)]
    
    # Handle dates with no symbols in universe
    if weights.empty:
        logger.error("No symbols in universe found in factor data")
        return None
    
    # Group by date and calculate weights
    weights_grouped = weights.groupby('date')
    
    # Initialize weights DataFrame
    weight_data = []
    
    for date, group in weights_grouped:
        # Rank assets for this date (higher factor value = higher weight)
        ranked = group.sort_values('combined_factor', ascending=False)
        
        # Calculate weights (can be customized based on ranking)
        # For simplicity, use linear weights based on rank
        n = len(ranked)
        if n == 0:
            continue
            
        # Simple linear weighting based on rank
        ranked['weight'] = (n - ranked.reset_index().index) / (n * (n + 1) / 2)
        
        # Alternative: use factor values directly (assuming they are normalized)
        # First, ensure all factor values are positive by shifting
        # min_factor = ranked['combined_factor'].min()
        # if min_factor < 0:
        #     ranked['combined_factor'] = ranked['combined_factor'] - min_factor + 0.001
        
        # Then calculate weights based on factor values
        # ranked['weight'] = ranked['combined_factor'] / ranked['combined_factor'].sum()
        
        # Store the weights
        for _, row in ranked.iterrows():
            weight_data.append({
                'date': date,
                'symbol': row['symbol'],
                'weight': row['weight']
            })
    
    # Convert to DataFrame and set index
    weights_df = pd.DataFrame(weight_data)
    weights_df = weights_df.set_index(['date', 'symbol'])['weight']
    
    logger.info(f"Successfully calculated weights for {len(weights_df)} entries")
    return weights_df

# --- Example Usage --- (Commented out, run from main script/notebook)
# if __name__ == '__main__':
#     # Requires factor_data calculated from factors.py example
#     # Placeholder for factor_data and combined_score if needed for testing
#     # combined_score = factor_data['combined_score'] # Assuming factor_data is loaded/calculated
#
#     # Dummy data for standalone testing
#     dates = pd.to_datetime(['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'])
#     symbols = ['BTC-USD', 'ETH-USD', 'BTC-USD', 'ETH-USD']
#     scores_data = [0.6, 0.4, 0.3, 0.7] # Example scores
#     index = pd.MultiIndex.from_arrays([dates, symbols], names=['date', 'symbol'])
#     combined_score_example = pd.Series(scores_data, index=index)
#
#     logger.info("Running portfolio.py example with dummy data...")
#     target_weights_top1 = calculate_top_n_weights(combined_score_example, n=1, max_weight_per_asset=0.8)
#     target_weights_ls = calculate_long_short_quintile_weights(combined_score_example, leverage=1.0)
#
#     print("\n--- Top 1 Target weights sample: ---")
#     print(target_weights_top1.unstack('symbol'))
#     print("\n--- Long/Short Quintile Target weights sample: ---")
#     print(target_weights_ls.unstack('symbol')) 