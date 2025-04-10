from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
import logging
import time
from datetime import datetime, timezone, timedelta
import pandas as pd

# Use absolute imports from src
from src.database.database import SessionLocal
from src.database.models import Candle, Zone
# Import OHLCVProcessor from data_processor
from app.core.data_processor import OHLCVProcessor
# Import zone_detector functions
from src.zone_detector import detect_base_patterns
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping from user timeframe to API granularity string (mirroring OHLCVProcessor)
# Needed for storing the correct value in the DB and querying
TIMEFRAME_TO_GRANULARITY = {
    '1m': 'ONE_MINUTE',       # Note: DataManager currently doesn't use all these
    '5m': 'FIVE_MINUTE',
    '15m': 'FIFTEEN_MINUTE',
    '1h': 'ONE_HOUR',
    '4h': 'FOUR_HOUR',        # Note: OHLCVProcessor has 4h, OHLCVFetcher has 6h
    '6h': 'SIX_HOUR',
    '1d': 'ONE_DAY'
}
# Reverse mapping for convenience if needed
GRANULARITY_TO_TIMEFRAME = {v: k for k, v in TIMEFRAME_TO_GRANULARITY.items()}

class DataManager:
    """Handles fetching, storing, and retrieving OHLCV data using OHLCVProcessor."""

    def __init__(self, db_session: Session = SessionLocal()):
        """Initializes the DataManager with a database session."""
        self.db = db_session
        # Use OHLCVProcessor for fetching and processing
        self.processor = OHLCVProcessor()

    def _get_api_granularity(self, timeframe: str) -> Optional[str]:
        """Helper to get the API granularity string from a timeframe string."""
        # Use the processor's internal map if available, otherwise use our local one
        valid_timeframes = getattr(self.processor, 'valid_timeframes', TIMEFRAME_TO_GRANULARITY)
        api_granularity = valid_timeframes.get(timeframe)
        if not api_granularity:
            logger.error(f"Invalid timeframe '{timeframe}' provided.")
        return api_granularity

    def store_historical_ohlcv(self, symbol: str, timeframe: str, start_unix: int, end_unix: int):
        """Fetches historical OHLCV data using OHLCVProcessor and stores it.

        Args:
            symbol: The trading pair symbol (e.g., 'BTC-USD').
            timeframe: The candle timeframe string (e.g., '1h', '15m').
            start_unix: The start timestamp in Unix seconds.
            end_unix: The end timestamp in Unix seconds.
        """
        api_granularity = self._get_api_granularity(timeframe)
        if not api_granularity:
            return # Error logged in helper

        start_dt = datetime.fromtimestamp(start_unix, tz=timezone.utc)
        end_dt = datetime.fromtimestamp(end_unix, tz=timezone.utc)

        logger.info(f"Fetching historical data for {symbol} ({timeframe} / {api_granularity}) from {start_dt} to {end_dt}")
        try:
            # Fetch data using the processor instance - returns a DataFrame
            df = self.processor.get_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                start_time=start_dt,
                end_time=end_dt
            )

            if df.empty:
                logger.warning(f"No data returned or processed for {symbol} ({timeframe}) in the specified range.")
                return

            candles_to_store = []
            # Iterate over DataFrame rows
            for _, row in df.iterrows():
                # Check for NaNs which might result from processing/cleaning
                if row.isnull().any():
                    logger.warning(f"Skipping row due to NaN values: {row.to_dict()}")
                    continue

                # Timestamp from DataFrame is already timezone-aware datetime
                candle_timestamp = int(row['timestamp'].timestamp())

                candle_obj = Candle(
                    symbol=symbol,
                    granularity=api_granularity, # Store the API granularity string
                    timestamp=candle_timestamp,
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    close=float(row['close']),
                    volume=float(row['volume'])
                )
                candles_to_store.append(candle_obj)

            if not candles_to_store:
                 logger.warning(f"No valid candle objects created from DataFrame for {symbol} ({timeframe}).")
                 return

            logger.info(f"Attempting to store {len(candles_to_store)} candles for {symbol} ({timeframe}).")

            # Add all candle objects to the session
            self.db.add_all(candles_to_store)
            # Commit the session to save changes to the database
            self.db.commit()
            logger.info(f"Successfully stored {len(candles_to_store)} candles.")

        except IntegrityError as e:
            self.db.rollback() # Rollback the transaction on integrity error
            logger.warning(f"IntegrityError storing data for {symbol} ({timeframe}): {e}. "
                           f"This likely means some fetched candles already exist in the DB. Skipping duplicates.")

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error storing OHLCV data for {symbol} ({timeframe}): {e}", exc_info=True)

    def get_stored_ohlcv(self, symbol: str, timeframe: str, start_unix: int, end_unix: int) -> List[Candle]:
        """Retrieves stored OHLCV data from the database for a given range.

        Args:
            symbol: The trading pair symbol.
            timeframe: The candle timeframe string (e.g., '1h', '15m').
            start_unix: The start timestamp in Unix seconds.
            end_unix: The end timestamp in Unix seconds.

        Returns:
            A list of Candle objects matching the criteria, ordered by timestamp.
        """
        api_granularity = self._get_api_granularity(timeframe)
        if not api_granularity:
            return [] # Return empty list on invalid timeframe

        logger.info(f"Retrieving stored data for {symbol} ({timeframe} / {api_granularity}) from {start_unix} to {end_unix}")
        try:
            candles = (
                self.db.query(Candle)
                .filter(
                    Candle.symbol == symbol,
                    Candle.granularity == api_granularity, # Query using API granularity string
                    Candle.timestamp >= start_unix,
                    Candle.timestamp <= end_unix
                )
                .order_by(Candle.timestamp)
                .all()
            )
            logger.info(f"Retrieved {len(candles)} candles from DB.")
            return candles
        except Exception as e:
            logger.error(f"Error retrieving OHLCV data for {symbol} ({timeframe}): {e}", exc_info=True)
            return [] # Return empty list on error

    def update_recent_ohlcv(self, symbol: str, timeframe: str):
        """Fetches the latest OHLCV data since the last stored candle and updates the database.

        Args:
            symbol: The trading pair symbol.
            timeframe: The candle timeframe string (e.g., '1h', '15m').
        """
        api_granularity = self._get_api_granularity(timeframe)
        if not api_granularity:
            return

        logger.info(f"Updating recent data for {symbol} ({timeframe} / {api_granularity})")
        try:
            # Find the timestamp of the most recent candle in the DB
            latest_candle = (
                self.db.query(Candle)
                .filter(Candle.symbol == symbol, Candle.granularity == api_granularity)
                .order_by(desc(Candle.timestamp))
                .first()
            )

            if not latest_candle:
                logger.warning(f"No existing data found for {symbol} ({timeframe}). "
                               f"Fetch historical data first using store_historical_ohlcv.")
                return

            # Calculate start time for the next fetch
            # OHLCVProcessor needs datetime objects
            start_dt = datetime.fromtimestamp(latest_candle.timestamp, tz=timezone.utc) + timedelta(seconds=1)
            end_dt = datetime.now(timezone.utc)

            # Avoid fetching if the start time is already in the future
            if start_dt >= end_dt:
                logger.info(f"Latest data for {symbol} ({timeframe}) is already up-to-date (Timestamp: {latest_candle.timestamp}).")
                return

            logger.info(f"Fetching new data for {symbol} ({timeframe}) from {start_dt} to {end_dt}")

            # Fetch new data using the processor
            df = self.processor.get_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                start_time=start_dt,
                end_time=end_dt
            )

            if df.empty:
                logger.info(f"No new candle data returned or processed for {symbol} ({timeframe}) since {start_dt}.")
                return

            candles_to_store = []
            start_unix_for_filter = latest_candle.timestamp + 1
            for _, row in df.iterrows():
                if row.isnull().any():
                    logger.warning(f"Skipping row due to NaN values: {row.to_dict()}")
                    continue

                candle_timestamp = int(row['timestamp'].timestamp())

                # Double-check timestamp to avoid re-inserting the latest known candle
                # or candles older than our calculated start
                if candle_timestamp >= start_unix_for_filter:
                    candle_obj = Candle(
                        symbol=symbol,
                        granularity=api_granularity,
                        timestamp=candle_timestamp,
                        open=float(row['open']),
                        high=float(row['high']),
                        low=float(row['low']),
                        close=float(row['close']),
                        volume=float(row['volume'])
                    )
                    candles_to_store.append(candle_obj)

            if not candles_to_store:
                 logger.info(f"No valid new candles found after filtering for {symbol} ({timeframe}).")
                 return

            logger.info(f"Attempting to store {len(candles_to_store)} new candles for {symbol} ({timeframe}).")

            # Store the new candles
            try:
                self.db.add_all(candles_to_store)
                self.db.commit()
                logger.info(f"Successfully stored {len(candles_to_store)} new candles.")
            except IntegrityError as ie:
                self.db.rollback()
                logger.warning(f"IntegrityError while storing new candles for {symbol} ({timeframe}): {ie}. "
                               f"Likely duplicate data overlap. Skipping duplicates.")
            except Exception as commit_e:
                self.db.rollback()
                logger.error(f"Error committing new candles for {symbol} ({timeframe}): {commit_e}", exc_info=True)

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating recent OHLCV data for {symbol} ({timeframe}): {e}", exc_info=True)

    def detect_and_store_zones(self, symbol: str, timeframe: str, ohlcv_df: Optional[pd.DataFrame] = None):
        """Detects S/D zones for given data and stores new ones in the database.
        
        Args:
            symbol: The trading pair symbol.
            timeframe: The candle timeframe string (e.g., '1h', '15m').
            ohlcv_df: Optional pre-fetched and processed OHLCV DataFrame. 
                      If None, data will be fetched from the DB for the last N candles.
                      (Need to define N or a time range for fetching)
        """
        api_granularity = self._get_api_granularity(timeframe)
        if not api_granularity:
            return

        # If DataFrame is not provided, fetch recent data from DB
        if ohlcv_df is None:
            # Define a reasonable lookback period for zone detection (e.g., 200 candles)
            # Calculate start/end timestamps for fetching
            # TODO: Define how far back to fetch for detection if df not provided
            logger.warning("Fetching OHLCV from DB for zone detection is not yet implemented.")
            # Placeholder: Fetch last ~1 week of data for the given timeframe?
            # candles_db = self.get_stored_ohlcv(symbol, timeframe, start_unix, end_unix)
            # ohlcv_df = self._candles_to_dataframe(candles_db) # Need helper
            return # Exit for now
        
        if ohlcv_df.empty:
             logger.warning(f"Provided OHLCV DataFrame for {symbol} ({timeframe}) is empty. Cannot detect zones.")
             return

        logger.info(f"Detecting zones for {symbol} ({timeframe}) using {len(ohlcv_df)} candles.")
        detected_zones_raw = detect_base_patterns(ohlcv_df)
        logger.info(f"Detected {len(detected_zones_raw)} raw zones.")

        if not detected_zones_raw:
            return

        zones_to_store = []
        for zone_dict in detected_zones_raw:
            try:
                # Extract timestamps from the DataFrame using indices
                leg_in_ts = int(ohlcv_df.iloc[zone_dict['leg_in_index']]['timestamp'].timestamp())
                base_start_ts = int(ohlcv_df.iloc[zone_dict['base_start_index']]['timestamp'].timestamp())
                base_end_ts = int(ohlcv_df.iloc[zone_dict['base_end_index']]['timestamp'].timestamp())
                formation_ts = int(ohlcv_df.iloc[zone_dict['leg_out_index']]['timestamp'].timestamp())

                zone_obj = Zone(
                    symbol=symbol,
                    timeframe=timeframe, # Store the user-friendly timeframe
                    type=zone_dict['type'],
                    zone_low=float(zone_dict['zone_low']),
                    zone_high=float(zone_dict['zone_high']),
                    leg_in_timestamp=leg_in_ts,
                    base_start_timestamp=base_start_ts,
                    base_end_timestamp=base_end_ts,
                    formation_timestamp=formation_ts,
                    initial_freshness_score=zone_dict.get('freshness_score'),
                    initial_strength_score=zone_dict.get('strength_score'),
                    rsi_at_formation=zone_dict.get('rsi_at_formation'),
                    is_active=True,
                    num_touches=0
                )
                zones_to_store.append(zone_obj)
            except (KeyError, IndexError, TypeError, ValueError) as e:
                 logger.error(f"Error processing detected zone dict: {zone_dict}. Error: {e}", exc_info=True)
                 continue # Skip this zone if data is malformed

        if not zones_to_store:
            logger.info("No valid Zone objects created after processing raw detections.")
            return

        logger.info(f"Attempting to store {len(zones_to_store)} new zones for {symbol} ({timeframe}).")
        
        # Store the new zones
        stored_count = 0
        skipped_count = 0
        for zone_obj in zones_to_store:
            try:
                # Add one by one to handle unique constraint violations individually
                self.db.add(zone_obj)
                self.db.commit()
                stored_count += 1
            except IntegrityError:
                self.db.rollback() # Rollback the failed commit
                skipped_count += 1
                # Log sparingly for duplicates
                # logger.debug(f"Skipping duplicate zone: {zone_obj}")
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error storing zone: {zone_obj}. Error: {e}", exc_info=True)

        logger.info(f"Successfully stored {stored_count} new zones. Skipped {skipped_count} duplicates.")

    def get_active_zones(self, symbol: str, timeframe: str) -> List[Zone]:
        """Retrieves active supply and demand zones from the database.

        Args:
            symbol: The trading pair symbol.
            timeframe: The candle timeframe string.

        Returns:
            A list of active Zone objects, ordered by formation time descending.
        """
        logger.info(f"Retrieving active zones for {symbol} ({timeframe})")
        try:
            zones = (
                self.db.query(Zone)
                .filter(
                    Zone.symbol == symbol,
                    Zone.timeframe == timeframe,
                    Zone.is_active == True
                )
                .order_by(desc(Zone.formation_timestamp))
                .all()
            )
            logger.info(f"Retrieved {len(zones)} active zones from DB.")
            return zones
        except Exception as e:
            logger.error(f"Error retrieving active zones for {symbol} ({timeframe}): {e}", exc_info=True)
            return []

    def update_zone_status(self, symbol: str, latest_candle: dict):
        """Checks if the latest candle interacts with active zones and updates their status.

        Args:
            symbol: The trading pair symbol.
            latest_candle: A dictionary representing the most recent candle data 
                           (e.g., {'timestamp': 167..., 'open': ..., 'high': ..., 'low': ..., 'close': ...}).
                           Timestamp should be Unix seconds.
        """
        try:
            candle_low = float(latest_candle['low'])
            candle_high = float(latest_candle['high'])
            candle_close = float(latest_candle['close'])
            candle_ts = int(latest_candle['timestamp'])
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Invalid latest_candle format: {latest_candle}. Error: {e}")
            return

        # Find potentially relevant active zones across all timeframes for the symbol
        # that overlap with the current candle's price range
        try:
            overlapping_zones = (
                self.db.query(Zone)
                .filter(
                    Zone.symbol == symbol,
                    Zone.is_active == True,
                    Zone.zone_low <= candle_high, # Candle high is above zone low
                    Zone.zone_high >= candle_low  # Candle low is below zone high
                )
                .all()
            )
        except Exception as e:
            logger.error(f"Error querying overlapping zones for {symbol}: {e}", exc_info=True)
            return

        if not overlapping_zones:
            # logger.debug(f"No active zones overlap with candle H:{candle_high} L:{candle_low} for {symbol}")
            return

        logger.info(f"Candle ({candle_ts} H:{candle_high} L:{candle_low} C:{candle_close}) potentially interacts with {len(overlapping_zones)} active zone(s) for {symbol}.")
        
        updated_zones = []
        for zone in overlapping_zones:
            # Ensure the candle is *after* the zone formation
            if candle_ts <= zone.formation_timestamp:
                continue

            logger.debug(f"Checking interaction with Zone ID {zone.id} ({zone.type} {zone.timeframe} {zone.zone_low}-{zone.zone_high})")
            # Update touch info regardless of deactivation
            zone.num_touches += 1
            zone.last_tested_timestamp = candle_ts
            updated_zones.append(zone)

            # Check for zone invalidation (candle closing beyond the distal line)
            should_deactivate = False
            if zone.type == 'demand' and candle_close < zone.zone_low:
                logger.info(f"Deactivating Demand Zone ID {zone.id} ({zone.zone_low}-{zone.zone_high}) due to close {candle_close} below zone low.")
                should_deactivate = True
            elif zone.type == 'supply' and candle_close > zone.zone_high:
                logger.info(f"Deactivating Supply Zone ID {zone.id} ({zone.zone_low}-{zone.zone_high}) due to close {candle_close} above zone high.")
                should_deactivate = True
            
            if should_deactivate:
                zone.is_active = False

        # Commit changes if any zones were updated
        if updated_zones:
            try:
                self.db.commit()
                logger.info(f"Committed status updates for {len(updated_zones)} zones.")
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error committing zone status updates: {e}", exc_info=True)

    def close_session(self):
        """Closes the database session."""
        self.db.close()

# Placeholder for more methods (retrieve, update_recent, etc.) 