import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from app.core.market_simulator import MarketSimulator
from app.core.backtest_engine import BacktestEngine
from app.core.models import OrderSide, OrderStatus  # Import necessary enums
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf # Add yfinance import

# --- Indicator Calculations ---
def calculate_atr(data, period=14):
    """Calculates Average True Range (ATR)."""
    high_low = data['high'] - data['low']
    high_close = np.abs(data['high'] - data['close'].shift())
    low_close = np.abs(data['low'] - data['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def calculate_rsi(data, period=14):
    """Calculates Relative Strength Index (RSI)."""
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --- Data Loading ---
def load_historical_data(symbol='BTC-USD', start_date='2023-01-01', end_date='2023-12-31'):
    """Load real historical cryptocurrency data from Yahoo Finance"""
    try:
        # Download data
        data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True, progress=False)
        if data.empty:
            print(f"No data downloaded for {symbol}.")
            return None

        # Check if columns are MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            # Select the relevant symbol level if multiple symbols were downloaded (though we only request one)
            # And drop the top level (like 'Open', 'Close') leaving only the symbol
            # data.columns = data.columns.droplevel(0)
            # Or, more directly for single symbol:
            df = pd.DataFrame()
            df['open'] = data[('Open', symbol)]
            df['high'] = data[('High', symbol)]
            df['low'] = data[('Low', symbol)]
            df['close'] = data[('Close', symbol)]
            df['volume'] = data[('Volume', symbol)]
            df.index.name = 'timestamp' # Name the index
            data = df.reset_index() # Reset index to make timestamp a column
        else:
             # Simple columns, reset index and lowercase
            data = data.reset_index()
            data.columns = [str(col).lower().replace('date', 'timestamp') for col in data.columns] # Convert Date to timestamp

        # Final check for required columns (after potential multi-index handling)
        data.columns = [str(col).lower() for col in data.columns] # Ensure lowercase
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_columns if col not in data.columns]

        if missing_cols:
            print(f"Warning: Missing required columns after processing: {missing_cols}")
            print(f"Available columns: {data.columns.tolist()}")
            if 'close' in missing_cols and 'adj close' in data.columns:
                 print("Using 'adj close' as 'close'.")
                 data['close'] = data['adj close']
                 missing_cols.remove('close')
            elif 'close' in missing_cols and 'adj_close' in data.columns: # Check underscore version too
                 print("Using 'adj_close' as 'close'.")
                 data['close'] = data['adj_close']
                 missing_cols.remove('close')
                 
            if missing_cols:
                return None

        print(f"Loaded {len(data)} records for {symbol}")
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        for col in ['open', 'high', 'low', 'close', 'volume']:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        data = data.dropna(subset=required_columns)
        
        return data[required_columns].copy()
    except Exception as e:
        print(f"Error loading data for {symbol}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

# --- Strategy Definition ---
def create_ma_crossover_signals(data, fast_period=20, slow_period=50):
    """
    Generates MA crossover signals.
    Returns: pd.Series with 1 for buy signal, -1 for sell signal, 0 otherwise.
    """
    if fast_period >= slow_period:
        raise ValueError("Fast MA period must be less than Slow MA period")
        
    fast_ma_col = f'MA{fast_period}'
    slow_ma_col = f'MA{slow_period}'
    
    data[fast_ma_col] = data['close'].rolling(window=fast_period).mean()
    data[slow_ma_col] = data['close'].rolling(window=slow_period).mean()
    
    signals = pd.Series(0, index=data.index)
    # Buy signal: Fast MA crosses above Slow MA
    signals[(data[fast_ma_col] > data[slow_ma_col]) & (data[fast_ma_col].shift(1) <= data[slow_ma_col].shift(1))] = 1
    # Sell signal: Fast MA crosses below Slow MA
    signals[(data[fast_ma_col] < data[slow_ma_col]) & (data[fast_ma_col].shift(1) >= data[slow_ma_col].shift(1))] = -1
    
    return signals

def main():
    # --- Configuration ---
    initial_balance = 10000
    trading_fee = 0.001
    slippage_std = 0.001 
    risk_per_trade = 0.01 
    take_profit_ratio = 3.0 # Target 1:3 Risk:Reward
    atr_period = 14
    atr_multiplier = 2.0 # Stop loss at 2x ATR
    rsi_period = 14
    # RSI filter: Longs only if RSI > 50, Shorts only if RSI < 50
    use_rsi_filter = True 
    # MA periods
    ma_fast_period = 20
    ma_slow_period = 50
    # Optional Crossover Exit (keep False for now)
    use_crossover_exit = False
    
    # --- Data Preparation ---
    print("Loading historical data...")
    data = load_historical_data(symbol='BTC-USD', start_date='2022-01-01', end_date='2023-12-31')
    if data is None:
        sys.exit("Failed to load data.")

    # --- Calculate Indicators ---
    data['ATR'] = calculate_atr(data, period=atr_period)
    data['RSI'] = calculate_rsi(data, period=rsi_period)
    signals = create_ma_crossover_signals(data, fast_period=ma_fast_period, slow_period=ma_slow_period)
    
    # --- Backtesting ---
    backtest = BacktestEngine(
        historical_data=data, # Pass DataFrame directly
        initial_balance=initial_balance,
        trading_fee=trading_fee,
        slippage_std=slippage_std
    )

    stop_loss_price = None
    take_profit_price = None
    skip_period = max(ma_slow_period, atr_period, rsi_period)
    
    print("Running MA Crossover Backtest...")
    for i in range(len(data)):
        backtest.current_index = i
        current_candle = data.iloc[i]
        current_price = current_candle['close']
        current_low = current_candle['low']
        current_high = current_candle['high']
        current_atr = current_candle['ATR']
        current_rsi = current_candle['RSI']
        
        if i < skip_period or pd.isna(current_atr) or pd.isna(current_rsi):
            continue

        # --- SL/TP Exit Check ---
        position_closed_by_sl_tp = False
        if backtest.position_size > 0: # Check Long SL/TP
            if stop_loss_price is not None and current_low <= stop_loss_price:
                print(f"[{current_candle['timestamp'].date()}] LONG Stop Loss triggered at {stop_loss_price:.2f}")
                backtest.execute_market_order(backtest.position_size, stop_loss_price, 'sell')
                position_closed_by_sl_tp = True
            elif take_profit_price is not None and current_high >= take_profit_price:
                print(f"[{current_candle['timestamp'].date()}] LONG Take Profit triggered at {take_profit_price:.2f}")
                backtest.execute_market_order(backtest.position_size, take_profit_price, 'sell')
                position_closed_by_sl_tp = True
        elif backtest.position_size < 0: # Check Short SL/TP
            if stop_loss_price is not None and current_high >= stop_loss_price: 
                print(f"[{current_candle['timestamp'].date()}] SHORT Stop Loss triggered at {stop_loss_price:.2f}")
                backtest.execute_market_order(abs(backtest.position_size), stop_loss_price, 'buy')
                position_closed_by_sl_tp = True
            elif take_profit_price is not None and current_low <= take_profit_price: 
                print(f"[{current_candle['timestamp'].date()}] SHORT Take Profit triggered at {take_profit_price:.2f}")
                backtest.execute_market_order(abs(backtest.position_size), take_profit_price, 'buy')
                position_closed_by_sl_tp = True

        if position_closed_by_sl_tp:
            stop_loss_price = None
            take_profit_price = None
            backtest.update_portfolio_value() 
            continue 
            
        # --- Crossover Exit Check (Optional) ---
        signal = signals.iloc[i] # Get signal for *current* bar for exit check
        position_closed_by_crossover = False
        if use_crossover_exit:
            if signal == -1 and backtest.position_size > 0: # Sell crossover while Long
                 print(f"[{current_candle['timestamp'].date()}] LONG Crossover Exit at {current_price:.2f}")
                 backtest.execute_market_order(backtest.position_size, current_price, 'sell')
                 position_closed_by_crossover = True
            elif signal == 1 and backtest.position_size < 0: # Buy crossover while Short
                 print(f"[{current_candle['timestamp'].date()}] SHORT Crossover Exit at {current_price:.2f}")
                 backtest.execute_market_order(abs(backtest.position_size), current_price, 'buy')
                 position_closed_by_crossover = True

        if position_closed_by_crossover:
            stop_loss_price = None
            take_profit_price = None
            backtest.update_portfolio_value()
            continue
                 
        # --- Entry Signal Execution ---
        # Use signal from the *previous* bar to avoid lookahead bias if crossover exit is off
        # If crossover exit is ON, using current bar signal is fine as exit happens first
        entry_signal = signals.iloc[i] if use_crossover_exit else signals.iloc[i-1]
        
        # Buy Entry: Crossover signal + Optional RSI Filter
        if entry_signal == 1 and backtest.position_size == 0:
            rsi_check_passed = not use_rsi_filter or (use_rsi_filter and current_rsi > 50)
            if rsi_check_passed:
                entry_price = current_price
                sl_distance = current_atr * atr_multiplier
                sl_price = entry_price - sl_distance
                tp_price = entry_price + sl_distance * take_profit_ratio
                
                portfolio_value = backtest.available_balance
                risk_amount = portfolio_value * risk_per_trade
                stop_loss_distance_points = entry_price - sl_price
                
                if stop_loss_distance_points > 0:
                    shares_to_trade = risk_amount / stop_loss_distance_points
                    if shares_to_trade * entry_price <= backtest.available_balance * 0.99:
                        print(f"[{current_candle['timestamp'].date()}] Attempting LONG entry at {entry_price:.2f} (RSI: {current_rsi:.2f}). SL: {sl_price:.2f}, TP: {tp_price:.2f}")
                        order = backtest.execute_market_order(shares_to_trade, entry_price, 'buy')
                        if order.status == OrderStatus.FILLED:
                            stop_loss_price = sl_price
                            take_profit_price = tp_price
                    else: print(f"[{current_candle['timestamp'].date()}] Long signal skipped - insufficient funds.")
                else: print(f"[{current_candle['timestamp'].date()}] Long signal skipped - zero/negative stop distance.")

        # Sell Entry: Crossover signal + Optional RSI Filter
        elif entry_signal == -1 and backtest.position_size == 0:
             rsi_check_passed = not use_rsi_filter or (use_rsi_filter and current_rsi < 50)
             if rsi_check_passed:
                 entry_price = current_price
                 sl_distance = current_atr * atr_multiplier
                 sl_price = entry_price + sl_distance
                 tp_price = entry_price - sl_distance * take_profit_ratio

                 portfolio_value = backtest.available_balance
                 risk_amount = portfolio_value * risk_per_trade
                 stop_loss_distance_points = sl_price - entry_price

                 if stop_loss_distance_points > 0:
                     shares_to_trade = risk_amount / stop_loss_distance_points
                     print(f"[{current_candle['timestamp'].date()}] Attempting SHORT entry at {entry_price:.2f} (RSI: {current_rsi:.2f}). SL: {sl_price:.2f}, TP: {tp_price:.2f}")
                     order = backtest.execute_market_order(shares_to_trade, entry_price, 'sell')
                     if order.status == OrderStatus.FILLED:
                         stop_loss_price = sl_price
                         take_profit_price = tp_price
                 else: print(f"[{current_candle['timestamp'].date()}] Short signal skipped - zero/negative stop distance.")

        # Update portfolio value daily
        backtest.update_portfolio_value()
            
    # --- Results ---
    metrics = backtest.get_performance_metrics()
    
    print("\nBacktest Results (MA Crossover + RSI Filter + ATR SL/TP):")
    print(f"Parameters: FastMA={ma_fast_period}, SlowMA={ma_slow_period}, RSI Filter={use_rsi_filter}, ATR Mult={atr_multiplier}, TP Ratio={take_profit_ratio}")
    print(f"Total Return: {metrics['total_return']:.2%}")
    print(f"Annualized Return: {metrics['annualized_return']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"Number of Trades: {metrics['num_trades']}")
    # Add win rate calculation
    if metrics['num_trades'] > 0:
        profitable_trades = sum(1 for trade in backtest.trades if hasattr(trade, 'realized_pnl') and trade.realized_pnl is not None and trade.realized_pnl > 0)
        win_rate = profitable_trades / (metrics['num_trades'] / 2) * 100 # Trades come in pairs (entry/exit)
        print(f"Win Rate: {win_rate:.2f}%")
    else:
        print("Win Rate: N/A (No trades)")

    
    # --- Plotting ---
    plt.figure(figsize=(14, 10))
    
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(data['timestamp'], data['close'], label='Close Price', alpha=0.8, linewidth=1)
    ax1.plot(data['timestamp'], data[f'MA{ma_fast_period}'], label=f'{ma_fast_period}-day MA', linestyle='--', alpha=0.7)
    ax1.plot(data['timestamp'], data[f'MA{ma_slow_period}'], label=f'{ma_slow_period}-day MA', linestyle=':', alpha=0.7)
    
    if backtest.trades:
        buy_timestamps = [t.timestamp for t in backtest.trades if t.side == OrderSide.BUY and t.status == OrderStatus.FILLED]
        buy_prices = [t.filled_price for t in backtest.trades if t.side == OrderSide.BUY and t.status == OrderStatus.FILLED]
        sell_timestamps = [t.timestamp for t in backtest.trades if t.side == OrderSide.SELL and t.status == OrderStatus.FILLED]
        sell_prices = [t.filled_price for t in backtest.trades if t.side == OrderSide.SELL and t.status == OrderStatus.FILLED]
        
        ax1.plot(buy_timestamps, buy_prices, '^', markersize=8, color='lime', label='Buy', markeredgecolor='black', lw=0)
        ax1.plot(sell_timestamps, sell_prices, 'v', markersize=8, color='red', label='Sell', markeredgecolor='black', lw=0)
    
    ax1.set_title(f'MA Crossover ({ma_fast_period}/{ma_slow_period}) Strategy with ATR SL/TP')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True)

    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    # Ensure portfolio values series has correct index before plotting
    portfolio_values_aligned = backtest.portfolio_values.copy()
    portfolio_values_aligned.index = data['timestamp'][:len(portfolio_values_aligned)] # Align index
    ax2.plot(portfolio_values_aligned.index, portfolio_values_aligned.values, label='Portfolio Value')
    ax2.set_title('Portfolio Value Over Time')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Portfolio Value ($)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main() 