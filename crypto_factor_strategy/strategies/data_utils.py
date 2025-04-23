import pandas as pd
import time
from datetime import datetime, timezone, timedelta
import os
import logging
import sys
from dotenv import load_dotenv
import yfinance as yf  # Add import for yfinance

# Add project root to path to make imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our Coinbase helper module
import coinbase_helper

# Configure logging
logger = logging.getLogger(__name__)

# Define example universe
UNIVERSE = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'XRP-USD', 'DOGE-USD', 'MATIC-USD', 'DOT-USD', 'AVAX-USD', 'LINK-USD']

def load_coinbase_data(symbols, start_iso, end_iso, granularity='ONE_DAY'):
    """
    Loads historical OHLCV data from Coinbase Advanced API for multiple symbols.

    Args:
        symbols (list): List of Coinbase product IDs (e.g., ['BTC-USD', 'ETH-USD']).
        start_iso (str): Start date in ISO 8601 format (e.g., '2020-01-01T00:00:00Z').
        end_iso (str): End date in ISO 8601 format (e.g., '2024-01-01T00:00:00Z').
        granularity (str): Coinbase granularity string ('ONE_MINUTE', 'FIVE_MINUTE',
                          'FIFTEEN_MINUTE', 'THIRTY_MINUTE', 'ONE_HOUR', 'TWO_HOUR',
                          'SIX_HOUR', 'ONE_DAY').

    Returns:
        pd.DataFrame: Multi-index DataFrame with ['date', 'symbol'] index and
                     lowercase ohlcv columns, or None if loading fails.
    """
    # Convert ISO dates to timestamps
    try:
        start_dt = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
        start_ts = int(start_dt.timestamp())
        end_ts = int(end_dt.timestamp())
    except ValueError as e:
        logger.error(f"Error parsing dates: {e}")
        return None

    # Coinbase API has a limit of 300 candles per request
    granularity_seconds_map = {
        'ONE_MINUTE': 60, 'FIVE_MINUTE': 300, 'FIFTEEN_MINUTE': 900,
        'THIRTY_MINUTE': 1800, 'ONE_HOUR': 3600, 'TWO_HOUR': 7200,
        'SIX_HOUR': 21600, 'ONE_DAY': 86400
    }
    seconds_per_candle = granularity_seconds_map.get(granularity, 86400)
    max_candles_per_req = 300
    step_seconds = max_candles_per_req * seconds_per_candle

    logger.info(f"Fetching data for {len(symbols)} symbols from {start_iso} to {end_iso} ({granularity})")

    all_data = {}

    for symbol in symbols:
        logger.info(f"Fetching {symbol}...")
        symbol_data = []
        current_start_ts = start_ts

        while current_start_ts < end_ts:
            current_end_ts = min(current_start_ts + step_seconds - seconds_per_candle, end_ts)
            current_start_dt = datetime.fromtimestamp(current_start_ts, tz=timezone.utc)
            current_end_dt = datetime.fromtimestamp(current_end_ts, tz=timezone.utc)
            logger.info(f"Fetching chunk: {current_start_dt} to {current_end_dt}")
            
            # Pass datetime objects directly to get_candles
            candles = coinbase_helper.get_candles(
                product_id=symbol,
                start_time=current_start_dt,
                end_time=current_end_dt,
                granularity=granularity
            )

            if not candles:
                logger.warning(f"No data returned for chunk in {symbol}. Adjusting start or stopping fetch.")
                # If it's the first request and no data, stop for this symbol
                if current_start_ts == start_ts:
                    break
                # Otherwise, try advancing start time slightly beyond the failed chunk end
                current_start_ts = current_end_ts + seconds_per_candle
                continue

            # Process candles
            if not candles:
                logger.warning(f"Empty candles response for {symbol}")
                current_start_ts = current_end_ts + seconds_per_candle
                continue
                
            df_chunk = pd.DataFrame(candles)
            symbol_data.append(df_chunk)

            # Get timestamp of last candle to set as next start time
            last_candle_ts = int(df_chunk['start'].iloc[-1])
            current_start_ts = last_candle_ts + seconds_per_candle

            # Sleep to respect rate limits
            time.sleep(0.2)

        if symbol_data:
            # Combine all chunks for this symbol
            df_symbol = pd.concat(symbol_data, ignore_index=True)
            
            # Convert timestamp to datetime
            df_symbol['start'] = pd.to_datetime(df_symbol['start'].astype(int), unit='s', utc=True)
            
            # Rename and select columns
            df_symbol = df_symbol.rename(columns={
                'start': 'date', 'low': 'low', 'high': 'high',
                'open': 'open', 'close': 'close', 'volume': 'volume'
            })
            df_symbol = df_symbol[['date', 'open', 'high', 'low', 'close', 'volume']]
            
            # Convert to appropriate data types
            df_symbol[['open', 'high', 'low', 'close', 'volume']] = df_symbol[['open', 'high', 'low', 'close', 'volume']].astype(float)
            
            # Sort and drop duplicates
            df_symbol = df_symbol.sort_values('date').drop_duplicates('date').set_index('date')
            all_data[symbol] = df_symbol
        else:
            logger.warning(f"No data loaded for {symbol}.")

    # Check if we got any data
    if not all_data:
        logger.error("Failed to load data for any symbol.")
        return None

    # Combine all symbol data into a multi-index DataFrame
    try:
        combined_df = pd.concat(all_data, names=['symbol', 'date']).swaplevel().sort_index()
        
        # Data alignment and cleaning
        combined_df_unstacked = combined_df.unstack('symbol')
        full_date_range = pd.date_range(
            start=combined_df_unstacked.index.min(),
            end=combined_df_unstacked.index.max(),
            freq=pd.Timedelta(seconds=seconds_per_candle),
            tz='UTC'
        )
        combined_df_reindexed = combined_df_unstacked.reindex(full_date_range)
        
        # Forward fill, then backward fill
        combined_df_filled = combined_df_reindexed.ffill().bfill()
        final_df = combined_df_filled.stack('symbol', future_stack=True)
        
        # Ensure the MultiIndex has 'date' as first level, 'symbol' as second level
        if final_df.index.names != ['date', 'symbol']:
            if 'date' in final_df.index.names and 'symbol' in final_df.index.names:
                final_df = final_df.reorder_levels(['date', 'symbol']).sort_index()
        
        # Final Type Conversion & Null Check
        for col in ['open', 'high', 'low', 'close', 'volume']:
             if col in final_df.columns:
                 final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
        
        # Drop rows with missing core price data
        final_df.dropna(subset=['open', 'high', 'low', 'close'], inplace=True)
        
        # Fill missing volume with 0
        final_df['volume'] = final_df['volume'].fillna(0)
        
        logger.info(f"Data loading complete. Final shape after cleaning: {final_df.shape}")
        return final_df
        
    except Exception as e:
        logger.error(f"Error creating multi-index DataFrame: {e}")
        return None

def get_historical_data(product_id, granularity='ONE_MINUTE', days_back=1):
    """
    Get historical candle data for a product
    
    Args:
        product_id (str): Product ID (e.g., 'BTC-USD')
        granularity (str): Candle granularity (e.g., 'ONE_MINUTE', 'FIVE_MINUTE')
        days_back (int): Number of days of historical data to fetch
        
    Returns:
        pandas.DataFrame or None: Historical data as DataFrame or None if error
    """
    try:
        # Calculate time range
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=days_back)
        
        logger.info(f"Fetching {days_back} days of {granularity} data for {product_id}")
        logger.debug(f"Time range: {start_time.isoformat()} to {end_time.isoformat()}")
        
        # Get candle data from Coinbase, passing datetime objects directly
        candles = coinbase_helper.get_candles(
            product_id=product_id,
            start_time=start_time,
            end_time=end_time,
            granularity=granularity
        )
        
        if not candles:
            logger.error(f"Failed to get historical data for {product_id}")
            return None
        
        # Extract candles from response
        if not candles:
            logger.warning(f"No candle data returned for {product_id}")
            return None
            
        logger.info(f"Retrieved {len(candles)} candles")
        
        # Convert to DataFrame
        df = pd.DataFrame(candles)
        
        # Rename columns to standard OHLCV format
        if 'start' in df.columns:
            df['timestamp'] = pd.to_datetime(df['start'], unit='s')
        
        # Ensure we have all required columns
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Missing required column: {col}")
                return None
        
        # Convert price and volume columns to numeric
        for col in required_columns:
            df[col] = pd.to_numeric(df[col])
            
        # Sort by timestamp (newest data last)
        if 'timestamp' in df.columns:
            df.sort_values('timestamp', inplace=True)
            
        logger.debug(f"DataFrame shape: {df.shape}")
        return df
        
    except Exception as e:
        logger.error(f"Exception in get_historical_data: {str(e)}", exc_info=True)
        return None

def load_yahoo_finance_data(symbols, start_date, end_date, interval='1d'):
    """
    Loads historical OHLCV data from Yahoo Finance for multiple symbols.

    Args:
        symbols (list): List of ticker symbols (e.g., ['BTC-USD', 'ETH-USD']).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval ('1d', '1h', etc.).

    Returns:
        pd.DataFrame: Multi-index DataFrame with ['date', 'symbol'] index and
                      lowercase ohlcv columns, or None if loading fails.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Loading data for {len(symbols)} symbols from Yahoo Finance...")
    
    try:
        # Convert ISO format dates to YYYY-MM-DD if needed
        if 'T' in start_date:
            start_date = start_date.split('T')[0]
        if 'T' in end_date:
            end_date = end_date.split('T')[0]
            
        # Download data for all symbols
        data = yf.download(
            tickers=symbols,
            start=start_date,
            end=end_date,
            interval=interval,
            group_by='ticker'
        )
        
        if data.empty:
            logger.error("No data returned from Yahoo Finance")
            return None
            
        # Check if we got panel data (multiple symbols) or single symbol data
        if isinstance(data.columns, pd.MultiIndex):
            # Multiple symbols - restructure into our desired format
            all_symbol_data = []
            
            for symbol in symbols:
                if symbol in data.columns.levels[0]:
                    symbol_data = data[symbol].copy()
                    symbol_data.columns = symbol_data.columns.str.lower()  # Lowercase column names
                    
                    # Add symbol as a column for later MultiIndex creation
                    symbol_data['symbol'] = symbol
                    all_symbol_data.append(symbol_data)
                else:
                    logger.warning(f"No data for {symbol}")
            
            if not all_symbol_data:
                logger.error("No valid data for any symbol")
                return None
                
            # Combine all symbol data
            combined_data = pd.concat(all_symbol_data)
            
            # Reset index to get date as column, then set MultiIndex
            combined_data = combined_data.reset_index()
            combined_data = combined_data.rename(columns={"Date": "date"})
            combined_data = combined_data.set_index(['date', 'symbol'])
            
        else:
            # Single symbol - simpler restructuring
            combined_data = data.copy()
            combined_data.columns = combined_data.columns.str.lower()  # Lowercase column names
            combined_data['symbol'] = symbols[0]
            combined_data = combined_data.reset_index()
            combined_data = combined_data.rename(columns={"Date": "date"})
            combined_data = combined_data.set_index(['date', 'symbol'])
            
        # Rename Yahoo Finance columns to match our expected format
        column_mapping = {
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'adj close': 'close',  # Use adjusted close as 'close'
            'volume': 'volume'
        }
        combined_data = combined_data.rename(columns=column_mapping)
        
        # Keep only OHLCV columns
        ohlcv_cols = ['open', 'high', 'low', 'close', 'volume']
        combined_data = combined_data[ohlcv_cols]
        
        # Check for missing data and fill if needed
        if combined_data.isnull().sum().sum() > 0:
            logger.warning(f"Found {combined_data.isnull().sum().sum()} missing values. Forward filling...")
            combined_data = combined_data.fillna(method='ffill').fillna(method='bfill')
            
        logger.info(f"Data loading complete. Shape: {combined_data.shape}")
        return combined_data
        
    except Exception as e:
        logger.error(f"Error loading data from Yahoo Finance: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

# --- Example Usage (can be run from main.py or a notebook) ---
if __name__ == '__main__':
    # This block runs only when the script is executed directly
    logger.info("Running data_utils.py example...")

    # Define parameters for the example run
    # Use a smaller, more recent date range for testing
    universe = ['BTC-USD', 'ETH-USD'] #, 'SOL-USD'] # Start small
    start_dt_iso = '2023-01-01T00:00:00Z'
    end_dt_iso = '2024-01-01T00:00:00Z'
    data_granularity = 'ONE_DAY' # Use Coinbase specific granularity

    # Load data
    ohlcv_data = load_coinbase_data(
        symbols=universe,
        start_iso=start_dt_iso,
        end_iso=end_dt_iso,
        granularity=data_granularity
    )

    if ohlcv_data is not None:
        logger.info("Example data loaded and processed successfully.")
        print("\n--- Data Head ---")
        print(ohlcv_data.head())
        print("\n--- Data Tail ---")
        print(ohlcv_data.tail())
        print("\n--- Data Info ---")
        ohlcv_data.info()
        print("\n--- Null Value Check ---")
        print(ohlcv_data.isnull().sum())

        # Example: Save to Parquet for faster loading later
        # parquet_path = '../data/example_ohlcv.parquet' # Assumes data dir exists at ../data/
        # try:
        #     os.makedirs(os.path.dirname(parquet_path), exist_ok=True)
        #     ohlcv_data.to_parquet(parquet_path)
        #     logger.info(f"Data saved to {parquet_path}")
        # except Exception as e:
        #     logger.error(f"Failed to save data to Parquet: {e}")

    else:
        logger.error("Example data loading failed.") 