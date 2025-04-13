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

# from app.core.config import get_settings # No longer needed here
from app.core.coinbase import CoinbaseClient
from app.strategies.rsi_momentum import RSIMomentumStrategy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_backtest(
    product_id: str,
    granularity: str, # e.g., "ONE_HOUR", "ONE_DAY"
    start_date_str: str, # "YYYY-MM-DD"
    end_date_str: str,   # "YYYY-MM-DD"
    strategy_config: dict,
    # New parameters for advanced backtesting
    initial_capital: float = 10000.0,
    risk_per_trade: float = 0.01, # Risk 1% of capital per trade
    stop_loss_atr_multiplier: float = 2.0, # Stop loss at 2x ATR
    atr_period: int = 14, # Default ATR period
    fee_percentage: float = 0.005, # Example fee (0.5%)
    slippage_percentage: float = 0.001 # Example slippage (0.1%)
):
    """Runs a backtest for the given strategy and parameters."""
    
    logger.info(f"--- Starting Backtest --- ")
    logger.info(f"Product: {product_id}, Granularity: {granularity}")
    logger.info(f"Period: {start_date_str} to {end_date_str}")
    logger.info(f"Strategy Config: {strategy_config}")
    logger.info(f"Backtest Params: Initial Capital=${initial_capital:.2f}, Risk={risk_per_trade*100}%, SL={stop_loss_atr_multiplier}xATR({atr_period}), Fee={fee_percentage*100}%, Slippage={slippage_percentage*100}%")
    
    # --- 1. Initialization --- 
    # Load credentials directly from JSON file to bypass potential .env issues
    KEY_FILE_PATH = "cdp_api_key.json"
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

        # Create a temporary settings object matching CoinbaseClient expectation
        temp_settings = SimpleNamespace()
        temp_settings.COINBASE_JWT_KEY_NAME = api_key_name
        temp_settings.COINBASE_JWT_PRIVATE_KEY = private_key_pem
        temp_settings.COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage" # Match default

        rest_client = CoinbaseClient(temp_settings)
        logger.info("REST Client initialized using JSON key file.")

    except Exception as e:
        logger.error(f"Failed to initialize REST client from JSON: {e}", exc_info=True)
        return # Cannot proceed without client

    strategy = RSIMomentumStrategy(product_id=product_id, config=strategy_config)
    
    # --- 2. Fetch Historical Data --- 
    logger.info("Fetching historical data in chunks...")
    try:
        # Convert dates to Unix timestamps (seconds since epoch)
        start_dt = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
        end_dt = end_dt.replace(hour=23, minute=59, second=59) # Include full end day

        # Define granularity to seconds mapping
        granularity_map = {
            "ONE_MINUTE": 60,
            "FIVE_MINUTE": 300,
            "FIFTEEN_MINUTE": 900,
            "THIRTY_MINUTE": 1800,
            "ONE_HOUR": 3600,
            "TWO_HOUR": 7200,
            "SIX_HOUR": 21600,
            "ONE_DAY": 86400
        }
        granularity_seconds = granularity_map.get(granularity)
        if not granularity_seconds:
            raise ValueError(f"Unsupported granularity: {granularity}")

        # Calculate max duration per API call (350 candles * seconds_per_candle)
        max_duration_seconds = 349 * granularity_seconds

        all_candles_data = []
        current_start_dt = start_dt

        while current_start_dt <= end_dt:
            chunk_start_ts = int(current_start_dt.timestamp())
            # Calculate end timestamp for the current chunk
            chunk_end_dt = current_start_dt + timedelta(seconds=max_duration_seconds)
            # Ensure chunk end does not exceed the overall end date
            chunk_end_dt = min(chunk_end_dt, end_dt)
            chunk_end_ts = int(chunk_end_dt.timestamp())

            logger.info(f"Fetching chunk: {current_start_dt.strftime('%Y-%m-%d %H:%M')} to {chunk_end_dt.strftime('%Y-%m-%d %H:%M')}")

            candles_response = rest_client.get_product_candles(
                product_id=product_id,
                start=str(chunk_start_ts),
                end=str(chunk_end_ts),
                granularity=granularity
            )

            # Extract candles list from response object
            chunk_data = getattr(candles_response, 'candles', [])
            if not chunk_data:
                 logger.warning(f"No candle data received for chunk starting {current_start_dt}. Stopping fetch.")
                 # Optionally break or continue depending on how you want to handle gaps
                 break # Stop fetching if a chunk is empty

            all_candles_data.extend(chunk_data)
            logger.info(f"Fetched {len(chunk_data)} candles in chunk. Total: {len(all_candles_data)}")

            # --- Debug: Log advancement --- 
            # Move to the next chunk start time (start of the next candle after the current chunk end)
            # We need the timestamp of the *last* candle received to determine the next start
            last_candle_in_chunk = chunk_data[-1]
            last_candle_ts = int(getattr(last_candle_in_chunk, 'start', 0)) # Assumes 'start' attribute has epoch time
            logger.debug(f"Last candle TS: {last_candle_ts}, advancing from {current_start_dt}")
            # --- End Debug --- 
            
            if last_candle_ts == 0:
                logger.error("Could not determine timestamp of last candle. Cannot proceed.")
                break # Cannot calculate next chunk start
                
            # Next chunk starts one granularity step after the last candle's start time
            current_start_dt = datetime.fromtimestamp(last_candle_ts) + timedelta(seconds=granularity_seconds)
            
            # Add a small delay to respect rate limits
            time.sleep(0.5) # Adjust as needed
         
        # Extract candles list from response object
        if not all_candles_data:
             logger.error("No candle data received from API after fetching chunks.")
             return

        logger.info("Data fetching complete. Processing into DataFrame...")
        # Convert raw candle data (assuming list of dicts from .to_dict()) to DataFrame
        # Coinbase candle format: [timestamp, low, high, open, close, volume]
        # Need to verify the actual structure from the SDK response object
        df = pd.DataFrame([
            candle.to_dict() if hasattr(candle, 'to_dict') else candle 
            for candle in all_candles_data
        ])
        # Rename columns based on expected SDK structure (adjust if necessary)
        # Common names: 'start', 'low', 'high', 'open', 'close', 'volume'
        # Assuming keys like candle.start, candle.low etc exist after conversion or directly
        df.rename(columns={
            'start': 'timestamp',
            # Add other potential renames based on actual object attributes...
        }, inplace=True)
        
        # Convert timestamp (assuming it's epoch seconds) and set as index
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        
        # Ensure numeric types
        for col in ['low', 'high', 'open', 'close', 'volume']:
             df[col] = pd.to_numeric(df[col])

        # --- Calculate Indicators --- 
        logger.info("Calculating indicators (ATR)...")
        df.ta.atr(length=atr_period, append=True) # Calculates and appends 'ATR_14' column
        # Rename ATR column for convenience
        atr_col_name = f"ATRr_{atr_period}" # pandas_ta default naming convention
        df.rename(columns={atr_col_name: 'atr'}, inplace=True)
        df.dropna(inplace=True) # Remove rows with NaN indicators (usually at the start)

        logger.info(f"Fetched {len(df)} data points.")
        # logger.info(f"Data Head:\n{df.head()}")

    except Exception as e:
        logger.error(f"Failed to fetch or process historical data: {e}", exc_info=True)
        return

    # --- 3. Backtesting Loop --- 
    logger.info("Running backtesting loop...")
    trades = []

    # Backtest State
    capital = initial_capital
    in_position = False         # Currently holding the base asset?
    position_size = 0.0       # Size of the current position in base currency (e.g., BTC)
    entry_price = 0.0         # Price at which the current position was entered
    entry_time = None         # Timestamp when the current position was entered
    stop_loss_price = 0.0     # Stop-loss level for the current position
    entry_fees = 0.0          # Fees paid for entering the current position

    # Performance Tracking
    equity_curve = [initial_capital]
    peak_equity = initial_capital
    max_drawdown = 0.0

    # Iterate through each candle (row)
    for timestamp, row in df.iterrows():
        current_low_price = row['low']
        current_close_price = row['close']
        current_atr = row['atr']

        # --- I. Check Stop Loss --- 
        if in_position and current_low_price <= stop_loss_price:
            logger.info(f"{timestamp}: STOP LOSS triggered at {stop_loss_price:.2f} (Low: {current_low_price:.2f})")
            # Assume stop loss executes at the stop price (worst case for slippage already included)
            exit_price_sl = stop_loss_price 
            # Apply slippage (making exit price slightly worse)
            exit_price_sl *= (1 - slippage_percentage)
            exit_time_sl = timestamp # Exit occurs during this candle

            # Calculate fees for exit
            exit_value = exit_price_sl * position_size
            exit_fees = exit_value * fee_percentage

            # Calculate PnL
            entry_value = entry_price * position_size
            pnl = (exit_value - entry_value) - entry_fees - entry_fees
            capital += pnl

            trades.append({
                'entry_time': entry_time,
                'exit_time': exit_time_sl,
                'entry_price': entry_price,
                'exit_price': exit_price_sl,
                'size': position_size,
                'pnl': pnl,
                'side': 'long',
                'exit_reason': 'stop_loss'
            })

            logger.info(f"--> STOPPED OUT: PnL={pnl:.2f}, Capital={capital:.2f}")

            # Reset position state
            in_position = False
            position_size = 0.0
            entry_price = 0.0
            entry_time = None
            stop_loss_price = 0.0
            entry_fees = 0.0

            # Simulate fill for strategy state
            strategy.process_market_data({
                'type': 'user_order_update', 'product_id': product_id, 'side': 'SELL', 'status': 'FILLED'
            })

            # Update equity curve and drawdown after stop loss
            equity_curve.append(capital)
            peak_equity = max(peak_equity, capital)
            drawdown = (peak_equity - capital) / peak_equity if peak_equity > 0 else 0
            max_drawdown = max(max_drawdown, drawdown)

            continue # Skip strategy signal check for this candle as we were stopped out

        # --- II. Process Strategy Signal --- 
        # Simulate receiving the close price for the current candle
        ticker_data = {
            'type': 'ticker',
            'product_id': product_id,
            'price': str(current_close_price), # Use close price for signal generation
            'time': timestamp.isoformat() 
        }
        
        signal = strategy.process_market_data(ticker_data)

        # --- III. Simulate Order Execution (Based on Signal) --- 
        # Assume orders execute at the OPEN price of the *next* candle
        # Get next candle's open price (if available)
        next_timestamp = timestamp + pd.Timedelta(minutes=1) # Rough estimate, depends on granularity
        next_open_price = df.loc[df.index > timestamp, 'open'].iloc[0] if not df.loc[df.index > timestamp].empty else None

        if next_open_price is None:
            # If it's the last candle, maybe close any open position?
            if in_position and timestamp == df.index[-1]:
                logger.info(f"{timestamp}: End of data. Closing open position at final close price: {current_close_price:.2f}")
                exit_price_eod = current_close_price * (1 - slippage_percentage)
                exit_value = exit_price_eod * position_size
                exit_fees = exit_value * fee_percentage
                pnl = (exit_value - entry_value) - entry_fees - exit_fees
                capital += pnl
                trades.append({
                    'entry_time': entry_time,
                    'exit_time': timestamp,
                    'entry_price': entry_price,
                    'exit_price': exit_price_eod,
                    'size': position_size,
                    'pnl': pnl,
                    'side': 'long',
                    'exit_reason': 'end_of_data'
                })
                in_position = False # Mark as closed
            # logger.debug(f"No next candle found for {timestamp}, skipping execution check.")
            # Break or continue depends on whether we forced close above
            break # Stop processing if no more candles

        # --- Execute BUY signal --- 
        if signal and signal['action'] == 'BUY' and not in_position:
            # Calculate entry price with slippage
            sim_entry_price = next_open_price * (1 + slippage_percentage)

            # Calculate Stop Loss
            if pd.isna(current_atr) or current_atr == 0:
                 logger.warning(f"{timestamp}: ATR is zero or NaN ({current_atr}), cannot calculate stop loss or position size. Skipping BUY.")
                 continue
            sim_stop_loss_price = sim_entry_price - current_atr * stop_loss_atr_multiplier

            # Calculate Position Size based on risk
            risk_amount_per_trade = capital * risk_per_trade
            dollars_at_risk_per_unit = sim_entry_price - sim_stop_loss_price
            if dollars_at_risk_per_unit <= 0:
                logger.warning(f"{timestamp}: Stop loss ({sim_stop_loss_price:.2f}) is above or equal to entry price ({sim_entry_price:.2f}). Cannot calculate position size. Skipping BUY.")
                continue
            sim_position_size = risk_amount_per_trade / dollars_at_risk_per_unit

            # Calculate entry fees
            sim_entry_value = sim_entry_price * sim_position_size
            sim_entry_fees = sim_entry_value * fee_percentage

            # Check if affordable (basic check, real check needs available balance)
            if sim_entry_value + sim_entry_fees > capital:
                 logger.warning(f"{timestamp}: Insufficient capital ({capital:.2f}) for calculated trade value ({sim_entry_value + sim_entry_fees:.2f}). Skipping BUY.")
                 continue

            # --- Update State --- 
            capital -= sim_entry_fees # Deduct fees immediately
            in_position = True
            position_size = sim_position_size
            entry_price = sim_entry_price # Store price *after* slippage
            entry_time = timestamp # Signal generated at close of this candle
            stop_loss_price = sim_stop_loss_price
            entry_fees = sim_entry_fees # Store fees paid for this entry

            logger.info(f"{timestamp}: BUY signal triggered. Simulating entry @ {entry_price:.2f}, Size={position_size:.6f}, SL={stop_loss_price:.2f}, Fee={entry_fees:.2f}, Capital={capital:.2f}")
            
            # Simulate fill confirmation for strategy state update
            fill_message = {
                'type': 'user_order_update',
                'product_id': product_id,
                'side': 'BUY',
                'status': 'FILLED',
                'average_filled_price': str(entry_price), # Use simulated price
                'cumulative_quantity': str(position_size)
            }
            strategy.process_market_data(fill_message) # Update strategy's internal state
            
        # --- Execute SELL signal --- 
        elif signal and signal['action'] == 'SELL' and in_position:
            # Calculate exit price with slippage
            sim_exit_price = next_open_price * (1 - slippage_percentage)
            exit_time = timestamp # Signal generated at close of this candle

            # Calculate exit fees
            sim_exit_value = sim_exit_price * position_size
            sim_exit_fees = sim_exit_value * fee_percentage
            
            # Calculate PnL (including entry and exit fees)
            sim_entry_value = entry_price * position_size # Value at actual entry price
            pnl = (sim_exit_value - sim_entry_value) - entry_fees - sim_exit_fees
            capital += pnl # Update capital with net PnL

            trades.append({
                'entry_time': entry_time,
                'exit_time': exit_time,
                'entry_price': entry_price,
                'exit_price': sim_exit_price,
                'size': position_size,
                'pnl': pnl,
                'side': 'long',
                'exit_reason': 'signal'
            })
            
            logger.info(f"{timestamp}: SELL signal triggered. Simulating exit @ {sim_exit_price:.2f}, PnL={pnl:.2f}, Capital={capital:.2f}")

            # Reset position state
            in_position = False
            position_size = 0.0
            entry_price = 0.0
            entry_time = None
            stop_loss_price = 0.0
            entry_fees = 0.0
            
            # Simulate fill confirmation for strategy state update
            fill_message = {
                'type': 'user_order_update',
                'product_id': product_id,
                'side': 'SELL',
                'status': 'FILLED',
                'average_filled_price': str(sim_exit_price),
                'cumulative_quantity': str(position_size) # Reflects size exited
            }
            strategy.process_market_data(fill_message) # Update strategy's internal state

        # --- Update Equity Curve & Max Drawdown --- 
        # Record capital at the end of each candle's processing
        current_portfolio_value = capital
        if in_position:
            # Estimate current value including unrealized PnL of open position
            current_value = current_close_price * position_size
            entry_value = entry_price * position_size
            unrealized_pnl = current_value - entry_value - entry_fees # Only entry fees paid so far
            current_portfolio_value += unrealized_pnl
            
        equity_curve.append(current_portfolio_value)
        peak_equity = max(peak_equity, current_portfolio_value)
        drawdown = (peak_equity - current_portfolio_value) / peak_equity if peak_equity > 0 else 0
        max_drawdown = max(max_drawdown, drawdown)

    # --- 4. Calculate Results --- 
    logger.info("--- Backtest Results --- ")
    total_trades = len(trades)
    if total_trades == 0:
        logger.info("No trades executed.")
        return

    trade_df = pd.DataFrame(trades)
    total_pnl = trade_df['pnl'].sum()
    wins = trade_df[trade_df['pnl'] > 0]
    losses = trade_df[trade_df['pnl'] <= 0]
    win_rate = (len(wins) / total_trades) * 100 if total_trades > 0 else 0
    avg_win = wins['pnl'].mean() if len(wins) > 0 else 0
    avg_loss = losses['pnl'].mean() if len(losses) > 0 else 0
    total_profit = wins['pnl'].sum()
    total_loss = abs(losses['pnl'].sum())
    profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')

    logger.info(f"Total Trades: {total_trades}")
    logger.info(f"Total Net PnL: {total_pnl:.2f}")
    logger.info(f"Final Capital: {capital:.2f}")
    logger.info(f"Max Drawdown: {max_drawdown*100:.2f}%")
    logger.info(f"Win Rate: {win_rate:.2f}%")
    logger.info(f"Average Win: {avg_win:.2f}")
    logger.info(f"Average Loss: {avg_loss:.2f}")
    logger.info(f"Profit Factor: {profit_factor:.2f}")
    logger.info(f"Trades:\n{trade_df}") # Uncomment to see all trades

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
    # Note: Granularity options: ONE_MINUTE, FIVE_MINUTE, FIFTEEN_MINUTE, THIRTY_MINUTE, ONE_HOUR, TWO_HOUR, SIX_HOUR, ONE_DAY
    backtest_params = {
        "initial_capital": 10000.0,
        "risk_per_trade": 0.01,       # Risk 1% of capital per trade
        "stop_loss_atr_multiplier": 2.0, # Stop loss at 2x ATR
        "atr_period": 14,
        "fee_percentage": 0.005,      # 0.5% taker fee estimate
        "slippage_percentage": 0.001   # 0.1% slippage estimate
    }
    
    # --- Strategy Specific Configuration ---
    # Modify these values to tune the strategy
    strategy_params_to_test = {
        "rsi_period": 14,
        "oversold_threshold": 30,
        "overbought_threshold": 70,
        # "trade_size" is calculated dynamically based on risk and stop-loss
    }

    # =====================================
    # === RUN THE BACKTEST ===
    # =====================================

    run_backtest(
        product_id=product_id_to_test,
        granularity=granularity_to_test,
        start_date_str=start_date_to_test,
        end_date_str=end_date_to_test,
        strategy_config=strategy_params_to_test,
        **backtest_params # Unpack the dictionary
    )

    # --- Example: Run with different parameters (uncomment to run) --- 
    # logger.info("\n\n=== Running Second Backtest with Different Params ===")
    # second_strategy_params = {
    #     "rsi_period": 9,
    #     "oversold_threshold": 25,
    #     "overbought_threshold": 75,
    # }
    # second_backtest_params = backtest_params.copy()
    # second_backtest_params["stop_loss_atr_multiplier"] = 1.5
    # second_backtest_params["risk_per_trade"] = 0.02
    # run_backtest(
    #     product_id=product_id_to_test,
    #     granularity=granularity_to_test,
    #     start_date_str=start_date_to_test,
    #     end_date_str=end_date_to_test,
    #     strategy_config=second_strategy_params,
    #     **second_backtest_params
    # ) 