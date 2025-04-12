# examples/rsi_momentum_backtest.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from datetime import datetime, timezone
from dataclasses import asdict
import ccxt # Import the CCXT library
import time # Import time for potential rate limiting delays
from app.models.order import OrderSide
import argparse
import io

# --- Adjust path to import from app --- 
# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path of the project root (assuming examples/ is one level down from root)
project_root = os.path.dirname(script_dir)
# Add the project root to the Python path
sys.path.insert(0, project_root)

from app.core.backtest_engine import BacktestEngine
# Ensure BBReversionStrategy is NOT imported if it was left accidentally
# from app.strategies.bb_reversion import BBReversionStrategy 
from app.strategies.rsi_momentum import RSIMomentumStrategy # Import the correct strategy

def load_ccxt_data(symbol='BTC/USDT', start_date_str='2021-01-01', end_date_str='2023-12-31', timeframe='1d', exchange_id='binance'):
    """Load historical OHLCV data from a specified exchange using CCXT."""
    print(f"Loading {exchange_id} data for {symbol} from {start_date_str} to {end_date_str} ({timeframe})...")
    print("Make sure you have CCXT installed: pip install ccxt")
    
    # Instantiate the exchange
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'enableRateLimit': True, # Enable built-in rate limiting
            # Add API keys here if needed for private data or higher rate limits
            # 'apiKey': 'YOUR_API_KEY',
            # 'secret': 'YOUR_SECRET',
        })
        # Load markets to ensure the symbol is valid and get metadata
        exchange.load_markets()
        if symbol not in exchange.markets:
             print(f"Error: Symbol {symbol} not found on {exchange_id}. Available symbols: {list(exchange.markets.keys())[:10]}...") # Show first 10 symbols
             return None
    except AttributeError:
        print(f"Error: Exchange '{exchange_id}' not found in CCXT.")
        return None
    except ccxt.ExchangeError as e:
        print(f"Error initializing exchange {exchange_id}: {e}")
        return None
    
    # Convert dates to ISO 8601 format if needed
    try:
        start_dt = datetime.fromisoformat(start_date_str).replace(tzinfo=timezone.utc)
        end_dt = datetime.fromisoformat(end_date_str).replace(tzinfo=timezone.utc)
        # Convert to milliseconds timestamp required by CCXT
        since = int(start_dt.timestamp() * 1000)
        end_milli = int(end_dt.timestamp() * 1000) 
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return None
        
    # Fetch data using CCXT, handling pagination
    all_ohlcv = []
    limit = 1000 # Set limit per request (adjust based on exchange)
    current_since = since
    
    print(f"Fetching data in chunks up to {end_dt.strftime('%Y-%m-%d %H:%M:%S')}...")

    while current_since < end_milli:
        try:
            # Fetch OHLCV data
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=current_since, limit=limit)
            
            if not ohlcv: # No more data or empty response
                print("No more data received from exchange.")
                break
                
            print(f"Fetched {len(ohlcv)} candles starting from {datetime.fromtimestamp(ohlcv[0][0]/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Filter out candles beyond the end date (sometimes exchanges return extra)
            ohlcv = [candle for candle in ohlcv if candle[0] <= end_milli]
            
            if not ohlcv: # Stop if all filtered out
                 print("All fetched candles were beyond the end date.")
                 break
            
            all_ohlcv.extend(ohlcv)
            
            # Update the 'since' timestamp for the next iteration
            # Add 1 millisecond to avoid fetching the last candle again
            current_since = ohlcv[-1][0] + 1 
            
            # Optional: add a small delay to respect rate limits if needed
            # time.sleep(exchange.rateLimit / 1000) 
            
        except ccxt.RateLimitExceeded as e:
            print(f"Rate limit exceeded: {e}. Waiting...")
            time.sleep(exchange.rateLimit / 1000 * 2) # Wait longer on rate limit error
        except ccxt.NetworkError as e:
            print(f"Network error: {e}. Retrying after delay...")
            time.sleep(5) # Wait before retrying network error
        except ccxt.ExchangeError as e:
            print(f"Exchange error fetching data: {e}")
            all_ohlcv = [] # Clear potentially partial data on error
            break # Exit loop on other exchange errors
        except Exception as e:
            print(f"An unexpected error occurred during fetch: {e}")
            all_ohlcv = []
            break

    if not all_ohlcv:
        print(f"Could not fetch data using CCXT for {symbol} on {exchange_id}. Falling back to mock data...")
        
        # --- Calculate seconds from timeframe for mock data generation ---
        timeframe_map_seconds = {
            '1m': 60,
            '3m': 180,
            '5m': 300,
            '15m': 900,
            '30m': 1800,
            '1h': 3600,
            '2h': 7200,
            '4h': 14400,
            '6h': 21600,
            '12h': 43200,
            '1d': 86400,
            '1w': 604800,
            '1M': 2592000 # Approximate for monthly
        }
        granularity_seconds = timeframe_map_seconds.get(timeframe, 86400) # Default to 1 day if not found
        # ----------------------------------------------------------------

        # Generate mock candle data
        # Start with a reasonable BTC price
        start_price = 16500.0  # Start of 2023 price approximation
        end_price = 42000.0    # End of 2023 price approximation
        
        # Calculate price trend factor
        days = (end_dt - start_dt).days
        hours = days * 24
        
        # Create a linear price trend with some randomness
        np.random.seed(42)  # For reproducible results
        
        # Generate timestamps
        timestamps = pd.date_range(start=start_dt, end=end_dt, freq=f"{granularity_seconds}S")
        
        # Generate mildly realistic price data
        price_trend = np.linspace(start_price, end_price, len(timestamps))
        # Add some random walk and volatility
        random_walk = np.random.normal(0, 1, len(timestamps)).cumsum() * 500
        # Add some periodic patterns (e.g., weekly cycles)
        periodic = np.sin(np.linspace(0, 52*2*np.pi, len(timestamps))) * 1000
        
        close_prices = price_trend + random_walk + periodic
        
        # Generate OHLCV data
        data = {
            'timestamp': timestamps,
            'open': close_prices * (1 + np.random.normal(0, 0.01, len(timestamps))),
            'high': close_prices * (1 + np.random.normal(0.02, 0.01, len(timestamps))),
            'low': close_prices * (1 - np.random.normal(0.02, 0.01, len(timestamps))),
            'close': close_prices,
            'volume': np.random.normal(100, 50, len(timestamps)) * (1 + np.abs(random_walk/5000))
        }
        
        # Ensure high >= open, close and low <= open, close
        for i in range(len(timestamps)):
            data['high'][i] = max(data['high'][i], data['open'][i], data['close'][i])
            data['low'][i] = min(data['low'][i], data['open'][i], data['close'][i])
        
        # Create DataFrame
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        print(f"Generated {len(df)} mock candle records")
        print(f"Sample data:\n{df.head()}")
        
        return df

    # If CCXT fetch was successful, convert to DataFrame
    print(f"Successfully fetched a total of {len(all_ohlcv)} candles using CCXT.")

    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df.set_index('timestamp', inplace=True) # Set index before converting types

    # Ensure correct data types
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col])

    print(f"Sample data from CCXT:\n{df.head()}") # Keep original print
    return df

if __name__ == "__main__":
    # --- Setup Argument Parser ---
    parser = argparse.ArgumentParser(description='Run RSI Momentum Strategy Backtest')
    parser.add_argument('--symbol', type=str, default='BTC/USD',
                      help='Trading pair symbol (default: BTC/USD)')
    parser.add_argument('--exchange', type=str, default='coinbase',
                      help='Exchange to use (default: coinbase)')
    parser.add_argument('--start-date', type=str, default='2023-01-01',
                      help='Start date in YYYY-MM-DD format (default: 2023-01-01)')
    parser.add_argument('--end-date', type=str, default='2023-12-31',
                      help='End date in YYYY-MM-DD format (default: 2023-12-31)')
    parser.add_argument('--timeframe', type=str, default='1d',
                      help='Timeframe for candles (default: 1d)')
    
    args = parser.parse_args()

    # --- Use Parsed Arguments ---
    SYMBOL_TO_TEST = args.symbol
    EXCHANGE_ID = args.exchange
    START_DATE = args.start_date
    END_DATE = args.end_date
    TIMEFRAME = args.timeframe 

    print(f"Running backtest for {SYMBOL_TO_TEST} on {EXCHANGE_ID} from {START_DATE} to {END_DATE} with {TIMEFRAME} timeframe.")

    print(f"Loading historical data for {SYMBOL_TO_TEST} from {EXCHANGE_ID}...")
    # Call the updated function with new arguments
    historical_data = load_ccxt_data(
        symbol=SYMBOL_TO_TEST, 
        start_date_str=START_DATE, 
        end_date_str=END_DATE, 
        timeframe=TIMEFRAME, 
        exchange_id=EXCHANGE_ID
    )

    if historical_data is None or historical_data.empty:
        print("Failed to load data. Exiting.")
        sys.exit(1) 

    # --- INITIALIZE RSI MOMENTUM STRATEGY --- 
    print("Initializing RSI Momentum Strategy...")
    rsi_momentum_strategy = RSIMomentumStrategy(
        timeframe=TIMEFRAME, 
        rsi_period=14,
        rsi_entry_threshold=60.0,
        rsi_exit_threshold=40.0,
        ma_period=20, # For regime detection
        atr_period=14, # For regime detection and stops
        risk_per_trade=0.02,
        atr_stop_multiplier=2.0
    )
    
    # --- INITIALIZE BACKTEST ENGINE with RSI STRATEGY --- 
    print("Initializing Backtest Engine...")
    backtest_engine = BacktestEngine(
        historical_data=historical_data,
        strategy=rsi_momentum_strategy, # Use the RSI strategy instance
        initial_balance=10000.0,
        trading_fee=0.001, 
        slippage_std=0.0005 
    )
    
    # --- RUN BACKTEST --- 
    print("--- Starting Backtest Run --- ")
    backtest_engine.run()
    print("--- Backtest Run Finished --- ")

    # --- Calculate and Print Metrics ---
    print("\nCalculating performance metrics...")
    metrics = backtest_engine.get_performance_metrics()

    print("\n--- Backtest Results ---")
    print(f"Initial Balance: ${backtest_engine.initial_balance:,.2f}")
    print(f"Final Portfolio Value: ${backtest_engine.portfolio_values.iloc[-1]:,.2f}")
    print(f"Total Return: {metrics['total_return']:.2%}")
    print(f"Annualized Return: {metrics['annualized_return']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"Number of Trades: {metrics['num_trades']}")

    # --- Print Trade Details --- 
    print("\n--- Trade Details ---")
    trade_num = 1
    # Iterate through trades list in steps of 2 (entry, exit)
    for i in range(0, len(backtest_engine.trades), 2):
        if i + 1 < len(backtest_engine.trades): # Check if exit order exists
            trade_entry = backtest_engine.trades[i]
            trade_exit = backtest_engine.trades[i+1]

            # Basic check for long entry/exit pair (can be made more robust)
            if trade_entry.side == OrderSide.BUY and trade_exit.side == OrderSide.SELL:
                print(f"Trade {trade_num}:")
                print(f"  Entry Timestamp: {trade_entry.timestamp}")
                print(f"  Entry Price: {trade_entry.filled_price:.2f}") # Use filled_price
                print(f"  Exit Timestamp: {trade_exit.timestamp}")
                print(f"  Exit Price: {trade_exit.filled_price:.2f}") # Use filled_price
                print(f"  Quantity: {trade_entry.quantity:.4f}") # Use entry quantity
                print(f"  PnL: {trade_exit.realized_pnl:.2f}") # Use realized_pnl from exit
                print("---")
                trade_num += 1
            else:
                # Handle unexpected order sequence if necessary
                print(f"Warning: Unexpected order sequence at index {i}. Entry: {trade_entry.side}, Exit: {trade_exit.side}")
        else:
            # Handle potentially open position at the end
            print(f"Info: Last order at index {i} might be an open position: {backtest_engine.trades[i].side}")

    # --- PLOTTING BLOCK WILL BE ADDED SEPARATELY --- 

    # --- Plotting for RSI Momentum --- 
    print("\nPlotting results...")
    # Adjust plot for RSI Momentum with Regime Filter
    fig, (ax1, ax_rsi, ax_regime) = plt.subplots(3, 1, figsize=(14, 12), sharex=True, 
                                                 gridspec_kw={'height_ratios': [3, 1, 1]})
    
    # --- Top Plot: Portfolio Value and Price ---
    color = 'tab:blue'
    ax1.set_ylabel('Portfolio Value', color=color)
    ax1.plot(backtest_engine.portfolio_values.index, backtest_engine.portfolio_values, color=color, label='Portfolio Value')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    ax_price = ax1.twinx() # Price axis
    color = 'tab:gray'
    ax_price.set_ylabel('Price', color=color)
    # Plot Price
    ax_price.plot(historical_data.index, historical_data['close'], color=color, alpha=0.6, label='Price')
    ax_price.tick_params(axis='y', labelcolor=color)

    # Add trade markers to ax_price
    trades_list = [trade.model_dump() for trade in backtest_engine.trades]
    trades_df = pd.DataFrame(trades_list) 
    if not trades_df.empty:
        trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp'])
        trades_df = trades_df.set_index('timestamp')
        
        buy_signals = trades_df[(trades_df['side'] == OrderSide.BUY.value) & trades_df['filled_price'].notna()]
        sell_signals = trades_df[(trades_df['side'] == OrderSide.SELL.value) & trades_df['filled_price'].notna()]
        
        if not buy_signals.empty:
            ax_price.plot(buy_signals.index, buy_signals['filled_price'], '^g', markersize=8, label='Buy Fill')
        if not sell_signals.empty:
            ax_price.plot(sell_signals.index, sell_signals['filled_price'], 'vr', markersize=8, label='Sell Fill')

    # --- Middle Plot: RSI --- 
    ax_rsi.set_ylabel('RSI')
    if hasattr(backtest_engine, 'data_with_signals') and 'rsi' in backtest_engine.data_with_signals.columns:
        ax_rsi.plot(backtest_engine.data_with_signals.index, backtest_engine.data_with_signals['rsi'], color='purple', label=f'RSI({rsi_momentum_strategy.rsi_period})')
        ax_rsi.axhline(rsi_momentum_strategy.rsi_entry_threshold, color='red', linestyle='--', linewidth=1, label=f'Entry ({rsi_momentum_strategy.rsi_entry_threshold})')
        ax_rsi.axhline(rsi_momentum_strategy.rsi_exit_threshold, color='green', linestyle='--', linewidth=1, label=f'Exit ({rsi_momentum_strategy.rsi_exit_threshold})')
        ax_rsi.axhline(50, color='gray', linestyle=':', linewidth=1)
        ax_rsi.set_ylim(0, 100) # RSI range
        ax_rsi.grid(True)
        ax_rsi.legend(loc='lower right')
    else:
         print("Warning: Could not find 'rsi' data for plotting.")

    # --- Bottom Plot: Regime --- 
    ax_regime.set_ylabel('Regime')
    if hasattr(backtest_engine, 'data_with_signals') and 'regime' in backtest_engine.data_with_signals.columns:
        regime_map = {"uptrend": 1, "sideways": 0, "downtrend": -1}
        regime_numeric = backtest_engine.data_with_signals['regime'].map(regime_map).fillna(0)
        ax_regime.plot(regime_numeric.index, regime_numeric, color='blue', drawstyle='steps-post', label='Regime (1:Up, 0:Side, -1:Down)')
        ax_regime.set_ylim(-1.5, 1.5)
        ax_regime.set_yticks([-1, 0, 1])
        ax_regime.set_yticklabels(['Down', 'Side', 'Up'])
        ax_regime.grid(True)
        ax_regime.legend(loc='lower right')
    else:
        print("Warning: Could not find 'regime' data for plotting.")

    # --- Final Touches --- 
    fig.suptitle(f'RSI Momentum Strategy ({SYMBOL_TO_TEST} {TIMEFRAME} on {EXCHANGE_ID.capitalize()} {START_DATE}-{END_DATE})', fontsize=16)
    # Combine legends from ax1 and ax_price
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax_price.get_legend_handles_labels()
    ax_price.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95]) 
    
    # Update plot filename for RSI Momentum
    plot_filename = f"rsi_momentum_{EXCHANGE_ID}_{SYMBOL_TO_TEST.replace('/', '-')}_{TIMEFRAME}_{START_DATE}_to_{END_DATE}_results.png"
    print(f"Saving plot to {plot_filename}...")
    plt.savefig(plot_filename)
    
    # plt.show() 

    print("Done.") 