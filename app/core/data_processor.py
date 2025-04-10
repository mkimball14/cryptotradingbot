import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Union
from datetime import datetime, timezone
import logging
import time
from coinbase.rest import RESTClient
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)

class OHLCVProcessor:
    """Process and normalize OHLCV (Open, High, Low, Close, Volume) data"""
    
    def __init__(self, decimal_places: int = 8):
        """
        Initialize the OHLCV processor
        
        Args:
            decimal_places: Number of decimal places to round price values to
        """
        self.decimal_places = decimal_places
        self.client = RESTClient()
        self.rate_limit_wait = 0.1  # Initial wait time between requests
        self.max_retries = 3
        
    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start_time: datetime,
        end_time: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV data from Coinbase Advanced API
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC-USD')
            timeframe: Candle timeframe ('15m', '1h', '4h')
            start_time: Start time for data retrieval
            end_time: Optional end time for data retrieval (defaults to current time)
            
        Returns:
            DataFrame with columns [timestamp, open, high, low, close, volume]
        """
        try:
            # Input validation
            if not isinstance(start_time, datetime):
                raise ValueError("start_time must be a datetime object")
            
            if end_time and not isinstance(end_time, datetime):
                raise ValueError("end_time must be a datetime object")
                
            # Validate timeframe
            valid_timeframes = {
                '15m': 'FIFTEEN_MINUTE',
                '1h': 'ONE_HOUR',
                '4h': 'FOUR_HOUR'
            }
            if timeframe not in valid_timeframes:
                raise ValueError(f"Invalid timeframe. Must be one of {list(valid_timeframes.keys())}")
            
            # Ensure times are in UTC
            start_time = start_time.astimezone(timezone.utc)
            if end_time:
                end_time = end_time.astimezone(timezone.utc)
            else:
                end_time = datetime.now(timezone.utc)
                
            # Validate time range
            if start_time >= end_time:
                raise ValueError("start_time must be before end_time")
                
            if start_time > datetime.now(timezone.utc):
                raise ValueError("start_time cannot be in the future")
            
            # Initialize empty list for candles
            all_candles = []
            current_start = start_time
            logger.debug(f"[{symbol}] Starting data fetch loop. Initial start: {current_start}, Target end: {end_time}")
            
            while current_start < end_time:
                loop_start_time = time.time()
                logger.debug(f"[{symbol}] Fetching chunk starting: {current_start}")
                
                chunk_end_time = min(current_start + pd.Timedelta(days=1), end_time)
                logger.debug(f"[{symbol}] Calculated chunk end: {chunk_end_time}")
                
                for attempt in range(self.max_retries):
                    logger.debug(f"[{symbol}] Attempt {attempt + 1}/{self.max_retries} for chunk starting {current_start}")
                    try:
                        # Get candles from Coinbase API
                        api_call_start = time.time()
                        logger.debug(f"[{symbol}] Calling get_public_candles: product_id={symbol}, start={int(current_start.timestamp())}, end={int(chunk_end_time.timestamp())}, granularity={valid_timeframes[timeframe]}")
                        
                        candles = self.client.get_public_candles(
                            product_id=symbol,
                            start=str(int(current_start.timestamp())),  # Convert to Unix timestamp string
                            end=str(int(chunk_end_time.timestamp())), # Use calculated chunk end
                            granularity=valid_timeframes[timeframe],
                            timeout=30 # Add a 30-second timeout to the API request
                        )
                        api_call_duration = time.time() - api_call_start
                        logger.debug(f"[{symbol}] API call successful. Duration: {api_call_duration:.2f}s")

                        # Check if 'candles' key exists and is a list
                        if 'candles' in candles and isinstance(candles['candles'], list):
                           fetched_count = len(candles['candles'])
                           logger.debug(f"[{symbol}] Fetched {fetched_count} candles in this chunk.")
                           all_candles.extend(candles['candles'])
                        else:
                           logger.warning(f"[{symbol}] API response did not contain a list under 'candles' key: {candles}")
                        
                        # Move to the next time chunk
                        logger.debug(f"[{symbol}] Successfully processed chunk. Moving current_start from {current_start} to {chunk_end_time}")
                        current_start = chunk_end_time # Move start to the end of the successfully fetched chunk
                        time.sleep(self.rate_limit_wait)  # Respect rate limits
                        break # Exit retry loop on success

                    except HTTPError as e:
                        api_call_duration = time.time() - api_call_start
                        logger.warning(f"[{symbol}] API call failed (HTTPError). Duration: {api_call_duration:.2f}s. Error: {e}")
                        # Check for rate limiting first
                        if e.response is not None and e.response.status_code == 429:
                            if attempt < self.max_retries - 1:
                                self.rate_limit_wait *= 2 # Exponential backoff
                                logger.warning(f"[{symbol}] Rate limit hit. Retrying attempt {attempt + 2}/{self.max_retries} in {self.rate_limit_wait:.2f}s...")
                                time.sleep(self.rate_limit_wait)
                                continue # Continue to the next attempt
                            else:
                                logger.error(f"[{symbol}] Max retries exceeded due to rate limiting.")
                                raise # Re-raise the last HTTPError after max retries

                        # Check for invalid product_id error
                        elif e.response is not None and e.response.status_code == 400:
                           try:
                               error_details = e.response.json()
                               if error_details.get("error") == "INVALID_ARGUMENT" and "product_id" in error_details.get("error_details", ""):
                                   logger.error(f"[{symbol}] Invalid symbol provided. API error: {error_details}")
                                   raise ValueError(f"Invalid symbol provided: {symbol}") from e
                           except Exception:
                               logger.error(f"[{symbol}] Received 400 Bad Request, but couldn't parse error details. Original error: {e}")
                               raise
                        
                        # Re-raise other HTTP errors
                        logger.error(f"[{symbol}] Unhandled HTTPError during API call: {e}", exc_info=True)
                        raise

                    except Exception as e:
                        api_call_duration = time.time() - api_call_start
                        logger.error(f"[{symbol}] Unexpected error during API call. Duration: {api_call_duration:.2f}s. Error: {e}", exc_info=True)
                        raise # Re-raise the unexpected error
                else:
                    # This block executes if the retry loop completes without a `break` (i.e., all retries failed)
                    logger.error(f"[{symbol}] All {self.max_retries} retries failed for chunk starting {current_start}. Stopping fetch for this symbol.")
                    # Decide how to handle this: return partially fetched data or raise error/return empty?
                    # For now, let's proceed with whatever data we have gathered so far.
                    break # Exit the outer while loop
                    
            logger.debug(f"[{symbol}] Finished data fetch loop. Total candles gathered: {len(all_candles)}")

            # ---- DataFrame Creation and Initial Processing ----

            if not all_candles:
                # Return empty DataFrame with correct columns if no data fetched
                logger.warning(f"No candle data retrieved for {symbol} in the specified time range.")
                return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Convert list of candle dicts to DataFrame
            try:
                df = pd.DataFrame(all_candles)
            except Exception as e:
                 logger.error(f"Failed to create DataFrame from candle list for {symbol}: {e}", exc_info=True)
                 return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Check if DataFrame is empty after creation (possible if all_candles had strange data)
            if df.empty:
                 logger.warning(f"DataFrame created from candle list for {symbol} is empty.")
                 return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])


            # Check if essential 'start' column exists from API data
            if 'start' not in df.columns:
                 logger.error(f"API candle data for {symbol} missing 'start' column. Cannot process.")
                 # Return empty DataFrame if core data is missing
                 return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Rename 'start' (Unix timestamp string) to 'timestamp'
            df.rename(columns={'start': 'timestamp'}, inplace=True)

            # Convert timestamp column (Unix strings) to datetime objects (UTC)
            # Errors='coerce' will turn unparsable timestamps into NaT (Not a Time)
            try:
                 # Ensure the column exists before conversion
                 if 'timestamp' in df.columns:
                      df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True, errors='coerce')
                      # Drop rows where timestamp conversion failed (became NaT)
                      initial_rows = len(df)
                      df.dropna(subset=['timestamp'], inplace=True)
                      dropped_rows = initial_rows - len(df)
                      if dropped_rows > 0:
                           logger.warning(f"Dropped {dropped_rows} rows for {symbol} due to invalid timestamps.")
                 else:
                      # This case should ideally be caught by the 'start' check, but safeguard here
                      logger.error(f"Timestamp column missing after rename for {symbol}. Cannot convert to datetime.")
                      return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            except Exception as e:
                 logger.error(f"Failed to convert timestamp column to datetime for {symbol}: {e}", exc_info=True)
                 # Returning empty if timestamp conversion fails critically
                 return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # If all rows were dropped due to bad timestamps, return empty
            if df.empty:
                 logger.warning(f"DataFrame for {symbol} became empty after timestamp conversion/dropping NaT.")
                 return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Ensure all expected data columns exist, adding them with NaNs if necessary before normalization
            expected_data_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in expected_data_cols:
                if col not in df.columns:
                    logger.warning(f"Data column '{col}' missing from API response for {symbol}. Adding as NaN.")
                    df[col] = np.nan # Add missing columns, they'll be handled by cleaning/normalization

            # Select and reorder columns to the standard format BEFORE normalization
            expected_cols = ['timestamp'] + expected_data_cols
            try:
                df = df[expected_cols]
            except KeyError as e:
                logger.error(f"Failed to select expected columns for {symbol} after processing API data. Missing: {e}. Columns present: {df.columns.tolist()}", exc_info=True)
                return pd.DataFrame(columns=expected_cols) # Return empty standard frame


            # ----- Data Processing Steps -----

            # Step 1: Normalize the data (handles types, rounding - assumes timestamp is datetime)
            try:
                df = self.normalize_data(df)
                if df.empty:
                     logger.warning(f"DataFrame for {symbol} became empty after normalization.")
                     return pd.DataFrame(columns=expected_cols) # Return empty if normalization empties it
            except Exception as e:
                 logger.error(f"Error during data normalization for {symbol}: {e}", exc_info=True)
                 return pd.DataFrame(columns=expected_cols) # Return empty if normalization fails


            # Step 2: Validate and get issues
            try:
                validation_issues = self.validate_data(df)
                 # Log validation issues if any
                has_issues = False
                for issue_type, issues_list in validation_issues.items():
                     if issues_list:
                          has_issues = True
                          logger.warning(f"Validation for {symbol} found {len(issues_list)} issues of type: {issue_type}")
                if not has_issues:
                     logger.info(f"Data validation passed for {symbol} with no issues.")
            except Exception as e:
                 logger.error(f"Error during data validation for {symbol}: {e}", exc_info=True)
                 validation_issues = {} # Proceed with cleaning without validation info


            # Step 3: Clean the data
            try:
                df = self.clean_data(df, validation_issues)
                if df.empty:
                     logger.warning(f"DataFrame for {symbol} became empty after cleaning.")
                     return pd.DataFrame(columns=expected_cols) # Return empty if cleaning empties it
            except Exception as e:
                 logger.error(f"Error during data cleaning for {symbol}: {e}", exc_info=True)
                 return pd.DataFrame(columns=expected_cols) # Return empty if cleaning fails

            logger.info(f"Successfully processed {len(df)} rows of OHLCV data for {symbol} timeframe {timeframe}.")
            return df

        except ValueError as e:
            # Catch specific ValueErrors raised for invalid inputs (timeframe, times, symbol)
            logger.error(f"Input validation error for {symbol}: {str(e)}")
            raise # Re-raise ValueError to be caught by tests or calling code

        except Exception as e:
            # Catch-all for unexpected errors during the entire process
            logger.error(f"Unhandled error processing {symbol}: {str(e)}", exc_info=True)
            # Ensure an empty DataFrame with correct columns is returned on failure
            return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize OHLCV data by ensuring consistent data types and standardizing decimal precision.
        Assumes 'timestamp' column is already datetime.
        
        Args:
            df: DataFrame with columns [timestamp, open, high, low, close, volume]
            
        Returns:
            Normalized DataFrame
        """
        try:
            # Create a copy to avoid modifying the original
            df = df.copy()
            
            # Timestamp conversion is now done earlier in get_ohlcv
            # Add a check to ensure it's the correct type
            if not df.empty and 'timestamp' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                 logger.error("Timestamp column is not datetime dtype in normalize_data.")
                 raise TypeError("Timestamp column must be datetime dtype for normalization.")

            # Convert price columns to float and round to specified precision
            price_columns = ['open', 'high', 'low', 'close']
            for col in price_columns:
                 if col in df.columns:
                     # Coerce errors to NaN, which will be handled by cleaning later
                     df[col] = pd.to_numeric(df[col], errors='coerce').round(self.decimal_places)
                 else:
                     logger.warning(f"Price column '{col}' not found during normalization.")


            # Convert volume to float and round to 8 decimal places
            if 'volume' in df.columns:
                 df['volume'] = pd.to_numeric(df['volume'], errors='coerce').round(8)
            else:
                 logger.warning("Volume column not found during normalization.")

            # Sort by timestamp and reset index (already checked if timestamp exists and is datetime)
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error normalizing data: {str(e)}")
            raise
            
    def validate_data(self, df: pd.DataFrame) -> Dict[str, List[Dict]]:
        """
        Validate OHLCV data integrity and identify potential issues
        
        Args:
            df: DataFrame with columns [timestamp, open, high, low, close, volume]
            
        Returns:
            Dictionary containing validation issues found
        """
        issues = {
            'missing_values': [],
            'price_anomalies': [],
            'volume_anomalies': [],
            'timestamp_gaps': [],
            'high_low_violations': []
        }
        
        try:
            # Check for missing values
            for col in df.columns:
                missing = df[col].isnull()
                if missing.any():
                    issues['missing_values'].append({
                        'column': col,
                        'count': missing.sum(),
                        'indices': missing[missing].index.tolist()
                    })
            
            # Check price anomalies (using 3 standard deviations)
            price_columns = ['open', 'high', 'low', 'close']
            for col in price_columns:
                mean = df[col].mean()
                std = df[col].std()
                threshold = 3 * std
                anomalies = df[abs(df[col] - mean) > threshold]
                if not anomalies.empty:
                    issues['price_anomalies'].append({
                        'column': col,
                        'anomalies': [{
                            'index': idx,
                            'timestamp': ts.isoformat(),
                            'value': val,
                            'mean': mean,
                            'std': std
                        } for idx, ts, val in zip(
                            anomalies.index,
                            anomalies['timestamp'],
                            anomalies[col]
                        )]
                    })
            
            # Check volume anomalies
            volume_mean = df['volume'].mean()
            volume_std = df['volume'].std()
            volume_threshold = 3 * volume_std
            volume_anomalies = df[abs(df['volume'] - volume_mean) > volume_threshold]
            if not volume_anomalies.empty:
                issues['volume_anomalies'] = [{
                    'index': idx,
                    'timestamp': ts.isoformat(),
                    'value': val,
                    'mean': volume_mean,
                    'std': volume_std
                } for idx, ts, val in zip(
                    volume_anomalies.index,
                    volume_anomalies['timestamp'],
                    volume_anomalies['volume']
                )]
            
            # Check for timestamp gaps
            if len(df) > 1:
                time_diff = df['timestamp'].diff()
                expected_diff = pd.Timedelta(time_diff.mode()[0])  # Most common time difference
                gaps = df[time_diff > expected_diff * 1.5][1:]  # Skip first row and check gaps
                if not gaps.empty:
                    issues['timestamp_gaps'] = [{
                        'index': idx,
                        'start': prev_ts.isoformat(),
                        'end': ts.isoformat(),
                        'gap_seconds': (ts - prev_ts).total_seconds()
                    } for idx, (prev_ts, ts) in enumerate(zip(
                        df['timestamp'].shift(),
                        gaps['timestamp']
                    ))]
            
            # Check high/low violations
            violations = df[
                (df['high'] < df['low']) |  # High should not be less than low
                (df['open'] > df['high']) |  # Open should not exceed high
                (df['open'] < df['low']) |   # Open should not be below low
                (df['close'] > df['high']) |  # Close should not exceed high
                (df['close'] < df['low'])     # Close should not be below low
            ]
            if not violations.empty:
                issues['high_low_violations'] = [{
                    'index': idx,
                    'timestamp': ts.isoformat(),
                    'open': o,
                    'high': h,
                    'low': l,
                    'close': c
                } for idx, ts, o, h, l, c in zip(
                    violations.index,
                    violations['timestamp'],
                    violations['open'],
                    violations['high'],
                    violations['low'],
                    violations['close']
                )]
            
            return issues
            
        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            raise
            
    def clean_data(self, df: pd.DataFrame, validation_results: Dict) -> pd.DataFrame:
        """Clean OHLCV data based on validation results."""
        df = df.copy()
        
        # Handle missing values
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_columns] = df[numeric_columns].fillna(method='ffill').fillna(method='bfill')
        
        # Handle price anomalies if detected
        if 'price_anomalies' in validation_results:
            for anomaly in validation_results['price_anomalies']:
                idx = anomaly['index']
                if idx > 0 and idx < len(df) - 1:
                    # Replace anomalous values with interpolated values
                    for col in ['open', 'high', 'low', 'close']:
                        df.loc[idx, col] = (df.loc[idx-1, col] + df.loc[idx+1, col]) / 2
                    df.loc[idx, 'volume'] = (df.loc[idx-1, 'volume'] + df.loc[idx+1, 'volume']) / 2
        
        # Ensure high/low consistency
        df['high'] = df[['high', 'open', 'close']].max(axis=1)
        df['low'] = df[['low', 'open', 'close']].min(axis=1)
        
        return df
            
    def enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich OHLCV data with additional technical indicators and metrics
        
        Args:
            df: DataFrame with columns [timestamp, open, high, low, close, volume]
            
        Returns:
            Enriched DataFrame with additional columns
        """
        try:
            # Create a copy to avoid modifying the original
            df = df.copy()
            
            # Calculate typical price (TP)
            df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
            
            # Calculate candle body and shadows
            df['body_size'] = abs(df['close'] - df['open'])
            df['upper_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
            df['lower_shadow'] = df[['open', 'close']].min(axis=1) - df['low']
            
            # Calculate price change and returns
            df['price_change'] = df['close'] - df['close'].shift(1)
            df['returns'] = df['close'].pct_change()
            
            # Calculate volume metrics
            df['volume_ma'] = df['volume'].rolling(window=20).mean()
            df['volume_std'] = df['volume'].rolling(window=20).std()
            
            # Flag potential doji candles
            df['is_doji'] = df['body_size'] <= 0.1 * (df['high'] - df['low'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error enriching data: {str(e)}")
            raise
            
    def process_ohlcv(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Complete OHLCV processing pipeline: normalize, validate, clean, and enrich
        
        Args:
            df: DataFrame with columns [timestamp, open, high, low, close, volume]
            
        Returns:
            Processed DataFrame with additional metrics
        """
        try:
            # Step 1: Normalize the data
            df = self.normalize_data(df)
            
            # Step 2: Validate and get issues
            validation_issues = self.validate_data(df)
            
            # Log validation issues if any
            for issue_type, issues in validation_issues.items():
                if issues:
                    logger.warning(f"Found {len(issues)} {issue_type}")
                    
            # Step 3: Clean the data
            df = self.clean_data(df, validation_issues)
            
            # Step 4: Enrich with additional metrics
            df = self.enrich_data(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Error in OHLCV processing pipeline: {str(e)}")
            raise 