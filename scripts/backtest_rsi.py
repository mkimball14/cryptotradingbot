import pandas as pd
import logging
from datetime import datetime, timedelta
import time
import pandas_ta as ta
import json
from types import SimpleNamespace

# Add project root to sys.path to allow importing app modules
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import Backtesting library components
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# from app.core.config import get_settings # No longer needed here
from app.core.coinbase import CoinbaseClient
# from app.strategies.rsi_momentum import RSIMomentumStrategy # We'll define a new one here

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Backtesting Strategy Definition ---
# Define the strategy using the backtesting library's structure
class RsiMomentumBacktestingStrategy(Strategy):
    # --- Strategy Parameters (Tunable) ---
    rsi_period = 14
    oversold_threshold = 30
    overbought_threshold = 70
    risk_per_trade = 0.01  # Risk % of equity per trade
    stop_loss_atr_multiplier = 2.0 # SL based on ATR
    atr_period = 14
    fast_sma_period = 10  # Fast SMA for quick trend changes
    slow_sma_period = 50  # Slow SMA for overall trend
    volume_ma_period = 20  # For volume confirmation
    volume_threshold = 1.1  # Only need 10% above average volume
    min_position_size = 0.01  # Minimum position size as fraction of equity

    def init(self):
        # Precompute indicators
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), length=self.rsi_period)
        
        # Dual SMA system
        self.fast_sma = self.I(ta.sma, pd.Series(self.data.Close), length=self.fast_sma_period)
        self.slow_sma = self.I(ta.sma, pd.Series(self.data.Close), length=self.slow_sma_period)
        
        # Volume moving average for confirmation
        self.volume_ma = self.I(ta.sma, pd.Series(self.data.Volume), length=self.volume_ma_period)
        
        # Calculate ATR using pandas_ta
        atr_series = ta.atr(high=pd.Series(self.data.High),
                            low=pd.Series(self.data.Low),
                            close=pd.Series(self.data.Close),
                            length=self.atr_period)
        self.atr = self.I(lambda: atr_series)

    def next(self):
        current_price = self.data.Close[-1]
        current_atr = self.atr[-1]
        current_volume = self.data.Volume[-1]
        current_volume_ma = self.volume_ma[-1]

        # Skip if ATR is invalid
        if pd.isna(current_atr) or current_atr <= 0:
            return

        # Calculate stop loss and position size
        stop_loss_price = current_price - current_atr * self.stop_loss_atr_multiplier
        risk_amount = self.equity * self.risk_per_trade
        dollars_at_risk_per_unit = current_price - stop_loss_price
        
        if dollars_at_risk_per_unit <= 0:
            position_size = 0
        else:
            position_dollars = risk_amount / (dollars_at_risk_per_unit / current_price)
            position_size = position_dollars / self.equity
            position_size = max(0, min(position_size, 1.0))

        # --- Entry Logic with Multiple Confirmations ---
        if not self.position:
            # 1. Check for strong uptrend (fast SMA > slow SMA)
            strong_trend = self.fast_sma[-1] > self.slow_sma[-1]
            
            # 2. Check for immediate trend (price > fast SMA)
            immediate_trend = current_price > self.fast_sma[-1]
            
            # 3. Check for RSI oversold crossover
            rsi_signal = crossover(self.rsi, self.oversold_threshold)
            
            # 4. Check for above-average volume (relaxed requirement)
            volume_confirmed = current_volume > (current_volume_ma * self.volume_threshold)
            
            # 5. Check for trend momentum (fast SMA slope)
            fast_sma_slope = (self.fast_sma[-1] - self.fast_sma[-2]) / self.fast_sma[-2]
            trend_momentum = fast_sma_slope > 0
            
            # Enter if conditions are met
            if (position_size > self.min_position_size and 
                strong_trend and 
                immediate_trend and
                (rsi_signal or self.rsi[-1] < 25) and  # Either crossover or very oversold
                (volume_confirmed or trend_momentum)):  # Either volume or strong momentum
                self.buy(size=position_size, sl=stop_loss_price)

        # --- Exit Logic ---
        else:
            # Exit on any of these conditions:
            # 1. RSI overbought
            # 2. Price drops below fast SMA significantly
            # 3. Fast SMA crosses below slow SMA (trend reversal)
            if (crossover(self.overbought_threshold, self.rsi) or 
                current_price < self.fast_sma[-1] * 0.99 or  # 1% below fast SMA
                (self.fast_sma[-1] < self.slow_sma[-1] and self.fast_sma[-2] > self.slow_sma[-2])):  # SMA crossover
                self.position.close()


def run_backtest(
    product_id: str,
    granularity: str, # e.g., "ONE_HOUR", "ONE_DAY"
    start_date_str: str, # "YYYY-MM-DD"
    end_date_str: str,   # "YYYY-MM-DD"
    strategy_params: dict, # Combined strategy and backtest engine params
    initial_capital: float = 10000.0,
    fee_percentage: float = 0.005, # Example fee (0.5%)
    slippage_percentage: float = 0.001 # Example slippage (0.1%) - applied via commission
):
    """Runs a backtest using the backtesting library."""
    
    logger.info(f"--- Starting Backtest (using backtesting library) --- ")
    logger.info(f"Product: {product_id}, Granularity: {granularity}")
    logger.info(f"Period: {start_date_str} to {end_date_str}")
    logger.info(f"Strategy Params: {strategy_params}")
    logger.info(f"Initial Capital=${initial_capital:.2f}, Commission={fee_percentage*100}%, Slippage Approx={slippage_percentage*100}%")

    # --- 1. Initialization (Keep client for data fetch) ---
    KEY_FILE_PATH = "cdp_api_key.json"
    rest_client = None # Initialize
    logger.info(f"Loading credentials from {KEY_FILE_PATH}...")
    try:
        if not os.path.exists(KEY_FILE_PATH):
            raise FileNotFoundError(f"Key file not found: {KEY_FILE_PATH}")
        with open(KEY_FILE_PATH, 'r') as f:
            key_data = json.load(f)
        api_key_name = key_data.get('name')
        private_key_pem = key_data.get('privateKey')
        if not api_key_name or not private_key_pem:
             raise ValueError("Key file missing 'name' or 'privateKey' field.")

        temp_settings = SimpleNamespace()
        temp_settings.COINBASE_JWT_KEY_NAME = api_key_name
        temp_settings.COINBASE_JWT_PRIVATE_KEY = private_key_pem
        temp_settings.COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage"

        rest_client = CoinbaseClient(temp_settings)
        logger.info("REST Client initialized for data fetching.")

    except Exception as e:
        logger.error(f"Failed to initialize REST client: {e}", exc_info=True)
        return # Cannot proceed without client

    # --- 2. Fetch Historical Data (Keep caching logic) ---
    CACHE_DIR = os.path.join(project_root, 'data', 'cache')
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_filename = f"{product_id}_{granularity}_{start_date_str}_{end_date_str}.csv"
    cache_filepath = os.path.join(CACHE_DIR, cache_filename)

    df = None
    if os.path.exists(cache_filepath):
        try:
            logger.info(f"Loading cached data from: {cache_filepath}")
            df = pd.read_csv(cache_filepath,
                             parse_dates=['timestamp'],
                             index_col='timestamp')
            for col in ['low', 'high', 'open', 'close', 'volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col])
            logger.info(f"Loaded {len(df)} data points from cache.")
        except Exception as e:
            logger.error(f"Failed to load data from cache file {cache_filepath}: {e}. Fetching from API.")
            df = None

    if df is None:
        logger.info(f"Cache not found or failed. Fetching historical data for {product_id}...")
        try:
            start_dt = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
            end_dt = end_dt.replace(hour=23, minute=59, second=59)

            granularity_map = {
                "ONE_MINUTE": 60, "FIVE_MINUTE": 300, "FIFTEEN_MINUTE": 900,
                "THIRTY_MINUTE": 1800, "ONE_HOUR": 3600, "TWO_HOUR": 7200,
                "SIX_HOUR": 21600, "ONE_DAY": 86400
            }
            granularity_seconds = granularity_map.get(granularity)
            if not granularity_seconds:
                raise ValueError(f"Unsupported granularity: {granularity}")

            max_duration_seconds = 349 * granularity_seconds
            all_candles_data = []
            current_start_dt = start_dt

            while current_start_dt <= end_dt:
                chunk_start_ts = int(current_start_dt.timestamp())
                chunk_end_dt = min(current_start_dt + timedelta(seconds=max_duration_seconds), end_dt)
                chunk_end_ts = int(chunk_end_dt.timestamp())

                logger.info(f"Fetching chunk: {current_start_dt.strftime('%Y-%m-%d %H:%M')} to {chunk_end_dt.strftime('%Y-%m-%d %H:%M')}")

                candles_response = rest_client.get_product_candles(
                    product_id=product_id,
                    start=str(chunk_start_ts),
                    end=str(chunk_end_ts),
                    granularity=granularity
                )
                chunk_data = getattr(candles_response, 'candles', [])
                if not chunk_data:
                     logger.warning(f"No candle data received for chunk starting {current_start_dt}. Stopping fetch.")
                     break

                all_candles_data.extend(chunk_data)
                logger.info(f"Fetched {len(chunk_data)} candles. Total: {len(all_candles_data)}")

                last_candle_in_chunk = chunk_data[-1]
                last_candle_ts = int(getattr(last_candle_in_chunk, 'start', 0))
                if last_candle_ts == 0:
                    logger.error("Could not determine timestamp of last candle. Cannot proceed.")
                    break
                current_start_dt = datetime.fromtimestamp(last_candle_ts) + timedelta(seconds=granularity_seconds)
                time.sleep(0.5)

            if not all_candles_data:
                 logger.error("No candle data received from API.")
                 return

            logger.info("Processing fetched data into DataFrame...")
            df = pd.DataFrame([candle.to_dict() if hasattr(candle, 'to_dict') else candle for candle in all_candles_data])
            df.rename(columns={'start': 'timestamp'}, inplace=True)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            df.sort_index(inplace=True)
            for col in ['low', 'high', 'open', 'close', 'volume']:
                 if col in df.columns:
                     df[col] = pd.to_numeric(df[col])

            try:
                logger.info(f"Saving fetched data to cache: {cache_filepath}")
                df.to_csv(cache_filepath)
            except Exception as e:
                logger.error(f"Failed to save data to cache: {e}")

            logger.info(f"Fetched {len(df)} data points from API.")

        except Exception as e:
            logger.error(f"Failed to fetch or process historical data: {e}", exc_info=True)
            return

    if df is None or df.empty:
        logger.error("No data available for backtest.")
        return

    # --- 3. Prepare Data for Backtesting Library ---
    # Rename columns to match backtesting.py requirements (must be capitalized)
    # Convert prices to satoshis (1 BTC = 100,000,000 satoshis) to handle Bitcoin's high price
    SATS_PER_BTC = 100_000_000
    df_bt = df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    })
    
    # Convert prices to satoshis
    for col in ['Open', 'High', 'Low', 'Close']:
        df_bt[col] = df_bt[col] / SATS_PER_BTC

    # Ensure required columns exist
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df_bt.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df_bt.columns]
        logger.error(f"Dataframe missing required columns for backtesting: {missing}")
        return

    # Drop rows with NaN values that might interfere with the library
    df_bt.dropna(subset=required_cols, inplace=True)
    logger.info(f"Data prepared for backtesting library ({len(df_bt)} rows).")
    logger.info("Prices converted to satoshis for better handling of position sizes.")
    # logger.info(f"Prepared Data Head:\n{df_bt.head()}")

    # --- 4. Run Backtest using the library ---
    logger.info("Initializing Backtest object...")
    # Note: Slippage is simulated via commission in backtesting.py
    # A commission of 0.002 means 0.2% fee per side (buy/sell)
    # We add slippage estimate to the fee here
    total_commission_per_side = fee_percentage + slippage_percentage
    
    bt = Backtest(
        df_bt,                          # Dataframe with OHLCV columns
        RsiMomentumBacktestingStrategy, # Your strategy class
        cash=initial_capital,           # Initial capital
        commission=total_commission_per_side, # Commission per trade (includes slippage)
        exclusive_orders=True           # Ensure one order at a time
    )

    logger.info(f"Running backtest with strategy parameters: {strategy_params}")
    # Run the backtest, passing strategy parameters
    # These parameters will override the defaults defined in the strategy class
    stats = bt.run(**strategy_params)

    # --- 5. Display Results ---
    logger.info("--- Backtest Results (backtesting library) ---")
    print(stats) # Print the detailed statistics dataframe

    # Convert final equity back to USD for reporting
    final_equity_usd = stats['Equity Final [$]'] * SATS_PER_BTC
    peak_equity_usd = stats['Equity Peak [$]'] * SATS_PER_BTC

    # Optionally, access specific stats:
    logger.info(f"Final Equity (USD): ${final_equity_usd:.2f}")
    logger.info(f"Peak Equity (USD): ${peak_equity_usd:.2f}")
    logger.info(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    logger.info(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
    logger.info(f"Profit Factor: {stats['Profit Factor']:.2f}")
    
    # Plot the results (optional, requires matplotlib)
    try:
        logger.info("Generating plot...")
        bt.plot()
        logger.info("Plot generated and should display.")
    except Exception as e:
        logger.warning(f"Could not generate plot (matplotlib might be missing or display issue): {e}")

    # You can also access the trade list if needed
    # trades_df = stats['_trades']
    # logger.info(f"Trades:\n{trades_df}")


if __name__ == "__main__":
    # =====================================
    # === BACKTEST PARAMETER DEFINITION ===
    # =====================================

    # --- General Settings ---
    product_id_to_test = "BTC-USD"
    start_date_to_test = "2023-01-01"
    end_date_to_test = "2023-12-31"
    granularity_to_test = "ONE_DAY"

    # --- Backtest Engine Settings ---
    initial_capital_setting = 10000.0
    fee_percentage_setting = 0.005      # 0.5% taker fee estimate
    slippage_percentage_setting = 0.001   # 0.1% slippage estimate

    # --- Strategy Specific Configuration ---
    # These will be passed to the Backtest run and override strategy defaults
    strategy_params_to_test = {
        "rsi_period": 14,             # Standard RSI period
        "oversold_threshold": 30,      # Standard oversold
        "overbought_threshold": 70,    # Standard overbought
        "risk_per_trade": 0.015,      # 1.5% risk per trade
        "stop_loss_atr_multiplier": 2.5, # 2.5x ATR for stops
        "atr_period": 14,             # Standard ATR period
        "fast_sma_period": 10,        # 10-day SMA for quick signals
        "slow_sma_period": 50,        # 50-day SMA for trend
        "volume_ma_period": 20,        # 20-day volume MA
        "volume_threshold": 1.1        # Only require 10% above average volume
    }

    # =====================================
    # === RUN THE BACKTEST ===
    # =====================================

    run_backtest(
        product_id=product_id_to_test,
        granularity=granularity_to_test,
        start_date_str=start_date_to_test,
        end_date_str=end_date_to_test,
        strategy_params=strategy_params_to_test,
        initial_capital=initial_capital_setting,
        fee_percentage=fee_percentage_setting,
        slippage_percentage=slippage_percentage_setting
    )

    # Run a second backtest with even more aggressive parameters
    logger.info("\n\n=== Running Second Backtest with More Aggressive Params ===")
    second_strategy_params = {
        "rsi_period": 14,             # Standard RSI period
        "oversold_threshold": 35,      # More aggressive entry
        "overbought_threshold": 65,    # More aggressive exit
        "risk_per_trade": 0.02,       # 2% risk per trade
        "stop_loss_atr_multiplier": 2.0, # Tighter stops
        "atr_period": 14,             # Standard ATR period
        "fast_sma_period": 5,         # Very fast 5-day SMA
        "slow_sma_period": 20,        # Shorter overall trend
        "volume_ma_period": 10,        # Shorter volume lookback
        "volume_threshold": 1.2        # Require 20% above average volume
    }
    run_backtest(
        product_id=product_id_to_test,
        granularity=granularity_to_test,
        start_date_str=start_date_to_test,
        end_date_str=end_date_to_test,
        strategy_params=second_strategy_params,
        initial_capital=initial_capital_setting,
        fee_percentage=fee_percentage_setting,
        slippage_percentage=slippage_percentage_setting
    )