import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, List, Tuple, Union

logger = logging.getLogger(__name__)

def calculate_relative_strength(
    prices: pd.DataFrame,
    lookback_periods: List[int] = [20, 60, 120],
    weights: Optional[List[float]] = None
) -> pd.DataFrame:
    """
    Calculate relative strength by comparing an asset's performance to the market average.
    
    Parameters:
    -----------
    prices : pandas.DataFrame
        DataFrame with price data. Must have a MultiIndex of (date, symbol).
    lookback_periods : list, default=[20, 60, 120]
        List of lookback periods (in days) to calculate returns.
    weights : list, optional
        List of weights for each lookback period. If None, equal weights are used.
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with relative strength values. Has the same index as prices.
    """
    try:
        logger.info(f"Calculating relative strength with lookback periods: {lookback_periods}")
        
        # Ensure prices has the right index structure
        if not isinstance(prices.index, pd.MultiIndex) or prices.index.names != ['date', 'symbol']:
            logger.error("Prices DataFrame must have a MultiIndex with levels ['date', 'symbol']")
            # Try to fix the index if possible
            if not isinstance(prices.index, pd.MultiIndex) and 'date' in prices.columns and 'symbol' in prices.columns:
                logger.warning("Attempting to set MultiIndex from columns")
                prices = prices.set_index(['date', 'symbol'])
            else:
                return pd.DataFrame()
        
        # Get unique dates and symbols
        dates = prices.index.get_level_values('date').unique()
        symbols = prices.index.get_level_values('symbol').unique()
        
        logger.info(f"Price data contains {len(dates)} dates and {len(symbols)} symbols")
        
        # Create empty DataFrame to store results
        rs_data = []
        
        # If weights not provided, use equal weights
        if weights is None:
            weights = [1.0 / len(lookback_periods)] * len(lookback_periods)
        
        # Normalize weights to sum to 1
        weights = [w / sum(weights) for w in weights]
        
        logger.info(f"Using weights: {weights}")
        
        # Convert prices to a series
        prices_series = prices.iloc[:, 0] if isinstance(prices, pd.DataFrame) and prices.shape[1] > 0 else prices
        
        # Calculate returns for each lookback period
        returns_by_period = {}
        for period in lookback_periods:
            # Safely calculate returns with proper date handling
            try:
                # Resample by date to get the last price of each day
                prices_resampled = prices_series.groupby(['symbol', pd.Grouper(level='date')]).last()
                
                # Calculate returns using pct_change, which is safer for MultiIndex
                returns = prices_resampled.groupby(level='symbol').pct_change(periods=period)
                
                # Store returns for this period
                returns_by_period[period] = returns
                
                logger.debug(f"Calculated {period}-day returns")
            except Exception as e:
                logger.error(f"Error calculating {period}-day returns: {str(e)}")
                returns_by_period[period] = pd.Series(index=prices_series.index, dtype=float)
        
        # Ensure all returns are properly aligned
        all_returns = pd.DataFrame({f'return_{period}': returns_by_period[period] 
                                    for period in lookback_periods})
        
        # Handle NaN values that might exist in the early periods
        all_returns = all_returns.fillna(0)
        
        # Calculate market average return for each period and date
        market_returns = {}
        for period in lookback_periods:
            col_name = f'return_{period}'
            
            try:
                # Group by date and calculate mean return across all symbols
                market_returns[period] = all_returns.groupby(level='date')[col_name].mean()
                
                logger.debug(f"Calculated market average for {period}-day returns")
            except Exception as e:
                logger.error(f"Error calculating market average for {period}-day returns: {str(e)}")
                # Create empty series with the correct dates
                market_returns[period] = pd.Series(index=dates, dtype=float).fillna(0)
        
        # Calculate relative strength as return minus market return
        for symbol in symbols:
            for i, period in enumerate(lookback_periods):
                col_name = f'return_{period}'
                
                try:
                    # Get symbol returns for this period
                    symbol_returns = all_returns.loc[(slice(None), symbol), col_name]
                    
                    # Calculate excess return (symbol return - market return)
                    for dt in symbol_returns.index.get_level_values('date'):
                        # Handle potential KeyError for dates
                        try:
                            market_return = market_returns[period].loc[dt] if dt in market_returns[period].index else 0
                            symbol_return = symbol_returns.loc[dt] if dt in symbol_returns.index else 0
                            
                            # Calculate relative strength and weighted value
                            rel_strength = symbol_return - market_return
                            weighted_rs = rel_strength * weights[i]
                            
                            rs_data.append({
                                'date': dt,
                                'symbol': symbol,
                                f'rs_{period}': rel_strength,
                                f'weighted_rs_{period}': weighted_rs
                            })
                        except KeyError as e:
                            logger.warning(f"Date not found in market returns: {dt}, error: {str(e)}")
                            continue
                except Exception as e:
                    logger.error(f"Error calculating relative strength for {symbol}, {period}-day: {str(e)}")
                    continue
        
        # Convert list of dictionaries to DataFrame
        rs_df = pd.DataFrame(rs_data)
        
        # Calculate combined relative strength
        rs_df['relative_strength'] = sum(rs_df[f'weighted_rs_{period}'] for period in lookback_periods)
        
        # Set index to match original prices index
        rs_df = rs_df.set_index(['date', 'symbol'])
        
        # Keep only the combined relative strength column
        final_rs = rs_df['relative_strength']
        
        logger.info(f"Successfully calculated relative strength for {len(final_rs)} entries")
        
        return final_rs
        
    except Exception as e:
        logger.error(f"Error calculating relative strength: {str(e)}")
        return pd.DataFrame() 