import os
import logging
import pandas as pd
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select, func, desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Use updated paths
from app.core.database.database import SessionLocal # Assuming database.py is here
from app.core.database.models import Candle, Zone, Base
from app.core.data_processor import OHLCVProcessor
from app.core.zone_detector import detect_base_patterns
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

    def detect_and_store_zones(
        self,
        symbol: str,
        timeframe: str,
        ohlcv_df: Optional[pd.DataFrame] = None,
        fetch_limit: int = 500 # Fetch last 500 candles if df not provided
    ) -> int:
        """Detects supply/demand zones and stores them.

        Args:
            symbol: Trading symbol (e.g., BTC-USD).
            timeframe: Timeframe string (e.g., '1h').
            ohlcv_df: Optional pre-fetched OHLCV DataFrame.
            fetch_limit: Number of recent candles to fetch if ohlcv_df is None.

        Returns:
            Number of new zones stored.
        """
        if ohlcv_df is None:
            # Fetch recent data if not provided
            # We might need more than fetch_limit if base patterns are long
            # Let's fetch a bit more to be safe, e.g., fetch_limit + 50
            logger.info(f"OHLCV DataFrame not provided for {symbol} {timeframe}, fetching recent data...")
            end_time = int(datetime.now(timezone.utc).timestamp())
            # Calculate a rough start time based on limit and interval
            interval_seconds = self.processor._timeframe_to_seconds(timeframe) # Access protected member for interval
            if not interval_seconds:
                logger.error(f"Could not determine interval seconds for timeframe '{timeframe}'")
                return 0
            start_time = end_time - (fetch_limit + 50) * interval_seconds 
            ohlcv_df = self.get_ohlcv_data(symbol, timeframe, start_time, end_time)
        
        if ohlcv_df is None or ohlcv_df.empty:
            logger.warning(f"No OHLCV data available for zone detection for {symbol} {timeframe}")
            return 0

        logger.debug(f"Detecting zones for {symbol} {timeframe} using {len(ohlcv_df)} candles.")
        # Use the imported function
        detected_zones_info = detect_base_patterns(ohlcv_df) # Pass df directly
        logger.debug(f"Detected {len(detected_zones_info)} potential zone patterns.")

        new_zones_count = 0
        if not detected_zones_info:
            return 0
        
        # Add detected zones to the database
        # Use the existing session stored in self.db
        session = self.db 
        try:
            for zone_info in detected_zones_info:
                # Convert dict info to Zone model object
                leg_in_candle = ohlcv_df.iloc[zone_info['leg_in_index']]
                leg_out_candle = ohlcv_df.iloc[zone_info['leg_out_index']]
                base_start_candle = ohlcv_df.iloc[zone_info['base_start_index']]
                base_end_candle = ohlcv_df.iloc[zone_info['base_end_index']]

                # Create the Zone object
                zone = Zone(
                    symbol=symbol,
                    timeframe=timeframe,
                    type=zone_info['type'],
                    zone_low=zone_info['zone_low'],
                    zone_high=zone_info['zone_high'],
                    leg_in_timestamp=int(leg_in_candle['timestamp'].timestamp()),
                    base_start_timestamp=int(base_start_candle['timestamp'].timestamp()),
                    base_end_timestamp=int(base_end_candle['timestamp'].timestamp()),
                    formation_timestamp=int(leg_out_candle['timestamp'].timestamp()),
                    is_active=True, # New zones start active
                    num_touches=0,
                    # Get scores and RSI from the detected info
                    initial_freshness_score=zone_info.get('freshness_score', 0),
                    initial_strength_score=zone_info.get('strength_score', 0),
                    rsi_at_formation=zone_info.get('rsi_at_formation') # Can be NaN
                )
                
                # Use merge to handle potential duplicates based on unique constraint
                # Assumes a unique constraint exists on (symbol, timeframe, formation_timestamp, type)
                # If merge isn't suitable, use a query check first.
                # session.merge(zone) # Merge might be complex depending on state
                
                # Simpler approach: Check if exists before adding
                exists_query = select(Zone).where(
                    Zone.symbol == symbol,
                    Zone.timeframe == timeframe,
                    Zone.type == zone.type,
                    Zone.formation_timestamp == zone.formation_timestamp,
                    Zone.zone_low == zone.zone_low,
                    Zone.zone_high == zone.zone_high
                )
                existing_zone = session.execute(exists_query).scalar_one_or_none()
                
                if not existing_zone:
                    session.add(zone)
                    new_zones_count += 1
                    logger.debug(f"Adding new {zone.type} zone {zone.zone_low}-{zone.zone_high} formed at {zone.formation_timestamp}")
                else:
                    logger.debug(f"Zone already exists: {zone.type} {zone.zone_low}-{zone.zone_high} formed at {zone.formation_timestamp}")
            
            if new_zones_count > 0:
                session.commit()
                logger.info(f"Successfully stored {new_zones_count} new zones for {symbol} {timeframe}.")
            else:
                logger.info(f"No new unique zones detected to store for {symbol} {timeframe}.")
                
        except IntegrityError as e:
            session.rollback()
            logger.warning(f"Database integrity error storing zones for {symbol} {timeframe} (likely duplicate): {e}")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error storing zones for {symbol} {timeframe}: {e}")
            raise DataManagerError(f"Database error storing zones: {e}") from e
        except Exception as e:
            session.rollback()
            logger.error(f"Unexpected error storing zones for {symbol} {timeframe}: {e}", exc_info=True)
            raise DataManagerError(f"Unexpected error storing zones: {e}") from e
        finally:
            session.close()
            
        return new_zones_count

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