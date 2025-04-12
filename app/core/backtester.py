import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List

from app.core.coinbase import CoinbaseClient
from app.core.config import Settings

logger = logging.getLogger(__name__)

class Backtester:
    """
    Handles backtesting trading strategies using historical data.
    """
    def __init__(self, client: CoinbaseClient, settings: Settings):
        self.client = client
        self.settings = settings

    async def load_data(
        self,
        product_id: str,
        start_time: datetime,
        end_time: datetime,
        granularity: str = "ONE_HOUR"
    ) -> pd.DataFrame:
        """
        Load historical OHLCV data for backtesting, handling pagination.

        Args:
            product_id: Trading pair (e.g., "BTC-USD").
            start_time: Start datetime for data.
            end_time: End datetime for data.
            granularity: Candle granularity (e.g., "ONE_HOUR", "ONE_DAY").

        Returns:
            DataFrame with OHLCV data.
        """
        logger.info(f"Loading historical data for {product_id} from {start_time} to {end_time} ({granularity})...")
        
        granularity_map_seconds = {
            "ONE_MINUTE": 60,
            "FIVE_MINUTE": 300,
            "FIFTEEN_MINUTE": 900,
            "ONE_HOUR": 3600,
            "SIX_HOUR": 21600,
            "ONE_DAY": 86400
        }
        
        if granularity not in granularity_map_seconds:
            raise ValueError(f"Invalid granularity: {granularity}")
            
        granularity_seconds = granularity_map_seconds[granularity]
        max_candles_per_request = 300
        all_candles = []
        current_start = start_time

        while current_start < end_time:
            # Calculate the end time for this chunk (max 300 candles)
            max_chunk_end = current_start + timedelta(seconds=granularity_seconds * (max_candles_per_request -1))
            current_end = min(max_chunk_end, end_time)
            
            logger.debug(f"Fetching chunk: {current_start.isoformat()} to {current_end.isoformat()}")

            try:
                candles_chunk = await self.client.get_product_candles(
                    product_id=product_id,
                    start=current_start.isoformat(),
                    end=current_end.isoformat(),
                    granularity=granularity
                )

                if not candles_chunk or not isinstance(candles_chunk, list):
                    logger.warning(f"No candle data received for chunk or invalid format: {candles_chunk}")
                    # Potentially break or retry depending on desired robustness
                    break # Stop if a chunk fails
                
                all_candles.extend(candles_chunk)
                logger.debug(f"Fetched {len(candles_chunk)} candles in this chunk.")
                
                # Check if we received fewer candles than expected, might mean end of available data
                if len(candles_chunk) < max_candles_per_request:
                    # Find the timestamp of the last candle received
                    if candles_chunk:
                        last_candle_time = datetime.fromtimestamp(candles_chunk[-1][0], tz=timezone.utc)
                        # If the last candle time is significantly before the chunk end, assume end of data
                        if current_end - last_candle_time > timedelta(seconds=granularity_seconds * 2):
                            logger.info("Reached end of available data based on last candle timestamp.")
                            break
                    else: # No candles received in the last request
                         logger.info("No candles received in the last chunk request. Assuming end of data.")
                         break

                # Update the start time for the next chunk
                # Use the timestamp of the last candle + granularity to avoid overlap/missing candles
                if candles_chunk:
                     # Timestamp is the start time of the candle
                     last_candle_start_ts = candles_chunk[-1][0]
                     current_start = datetime.fromtimestamp(last_candle_start_ts + granularity_seconds, tz=timezone.utc)
                else:
                    # If no candles, advance by the maximum chunk duration to avoid infinite loop
                    current_start = current_end + timedelta(seconds=granularity_seconds)

            except Exception as e:
                logger.error(f"Error loading chunk from {current_start} to {current_end}: {e}")
                # Optionally add retry logic here
                break # Stop fetching on error
        
        if not all_candles:
            logger.error("Failed to load any historical data.")
            return pd.DataFrame()
            
        # Process all collected candles
        df = pd.DataFrame(all_candles, columns=["timestamp", "low", "high", "open", "close", "volume"])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
        df = df.drop_duplicates(subset=['timestamp']) # Ensure unique timestamps
        df.set_index('timestamp', inplace=True)

        # Ensure numeric types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.sort_index()
        # Filter final DataFrame to the originally requested range
        df = df[(df.index >= start_time) & (df.index <= end_time)]
        logger.info(f"Successfully loaded and combined {len(df)} data points for {product_id}.")
        return df

    def run_strategy(self, data: pd.DataFrame, short_window: int = 10, long_window: int = 30) -> pd.DataFrame:
        """
        Run a simple Moving Average Crossover strategy.

        Args:
            data: DataFrame with OHLCV data (must have 'close' column).
            short_window: Period for the short moving average.
            long_window: Period for the long moving average.

        Returns:
            DataFrame with strategy signals ('signal' column: 1 for buy, -1 for sell, 0 for hold).
        """
        if 'close' not in data.columns or data.empty:
            logger.error("Data must contain a 'close' column and not be empty.")
            return data

        logger.info(f"Running MA Crossover strategy (Short: {short_window}, Long: {long_window})...")
        data['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1).mean()
        data['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1).mean()

        # Generate signals
        data['signal'] = 0
        # Buy signal: short MA crosses above long MA
        data.loc[data['short_mavg'] > data['long_mavg'], 'signal'] = 1
        # Sell signal: short MA crosses below long MA
        data.loc[data['short_mavg'] < data['long_mavg'], 'signal'] = -1

        # Calculate position changes (shift signal to avoid lookahead bias)
        data['positions'] = data['signal'].diff()
        logger.info("Strategy signals generated.")
        return data

    def calculate_performance(self, data: pd.DataFrame) -> Dict:
        """
        Calculate basic performance metrics for the backtest.

        Args:
            data: DataFrame with strategy signals and price data.

        Returns:
            Dictionary containing performance metrics.
        """
        if 'positions' not in data.columns or 'close' not in data.columns:
            logger.error("Data must contain 'positions' and 'close' columns.")
            return {}

        logger.info("Calculating performance metrics...")
        # Calculate returns
        data['returns'] = data['close'].pct_change()
        # Calculate strategy returns (assuming position held from signal)
        data['strategy_returns'] = data['returns'] * data['signal'].shift(1)

        # Calculate cumulative returns
        cumulative_returns = (1 + data['strategy_returns']).cumprod()
        total_return = cumulative_returns.iloc[-1] - 1 if not cumulative_returns.empty else 0

        # Calculate Sharpe Ratio (simple approximation)
        risk_free_rate = 0.0 # Assume 0 for simplicity
        mean_return = data['strategy_returns'].mean()
        std_dev = data['strategy_returns'].std()
        sharpe_ratio = (mean_return - risk_free_rate) / std_dev * np.sqrt(252) if std_dev != 0 else 0 # Annualized

        # Number of trades
        trades = data['positions'].abs().sum() / 2 # Each position change is buy/sell

        performance = {
            "total_return": f"{total_return:.2%}",
            "sharpe_ratio": f"{sharpe_ratio:.2f}",
            "num_trades": int(trades),
            "final_cumulative_return": cumulative_returns.iloc[-1] if not cumulative_returns.empty else 1
        }
        logger.info(f"Performance: {performance}")
        return performance

    async def run_backtest(
        self,
        product_id: str,
        start_time: datetime,
        end_time: datetime,
        granularity: str = "ONE_HOUR",
        short_window: int = 10,
        long_window: int = 30
    ) -> Optional[Dict]:
        """
        Run the full backtest process.

        Args:
            product_id: Trading pair.
            start_time: Backtest start time.
            end_time: Backtest end time.
            granularity: Candle granularity.
            short_window: Short MA window.
            long_window: Long MA window.

        Returns:
            Dictionary with performance metrics or None if failed.
        """
        data = await self.load_data(product_id, start_time, end_time, granularity)
        if data.empty:
            logger.error("Failed to load data for backtest.")
            return None

        data_with_signals = self.run_strategy(data, short_window, long_window)
        performance = self.calculate_performance(data_with_signals)

        return performance 