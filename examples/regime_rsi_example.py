import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import pandas_ta as ta # Import pandas_ta
import matplotlib.pyplot as plt
import yfinance as yf
from app.core.backtest_engine import BacktestEngine
from app.core.models import OrderStatus
import itertools # For grid search

# --- Indicator Calculations ---
def calculate_atr(data, period=14):
    """Calculates Average True Range (ATR)."""
    try:
        atr_series = ta.atr(data['high'], data['low'], data['close'], length=period)
        return atr_series if atr_series is not None else pd.Series(index=data.index)
    except Exception as e:
        print(f"Error calculating ATR: {e}", file=sys.stderr)
        return pd.Series(index=data.index)

def calculate_rsi(data, period=14):
    """Calculates Relative Strength Index (RSI)."""
    try:
        rsi_series = ta.rsi(data['close'], length=period)
        return rsi_series if rsi_series is not None else pd.Series(index=data.index)
    except Exception as e:
        print(f"Error calculating RSI: {e}", file=sys.stderr)
        return pd.Series(index=data.index)

def calculate_adx(data, period=14):
    """Calculates ADX and DMI (+DI, -DI)."""
    try:
        adx_df = ta.adx(data['high'], data['low'], data['close'], length=period)
        # Ensure column names are consistent and lowercase
        if adx_df is not None:
             adx_df.columns = [f'adx_{period}', f'dmp_{period}', f'dmn_{period}']
        else:
             adx_df = pd.DataFrame(index=data.index, columns=[f'adx_{period}', f'dmp_{period}', f'dmn_{period}'])
        return adx_df
    except Exception as e:
        print(f"Error calculating ADX: {e}", file=sys.stderr)
        return pd.DataFrame(index=data.index, columns=[f'adx_{period}', f'dmp_{period}', f'dmn_{period}'])

# --- Data Loading (same as before) ---
def load_historical_data(symbol='BTC-USD', start_date='2022-01-01', end_date='2023-12-31'):
    """Load real historical cryptocurrency data from Yahoo Finance"""
    try:
        data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True, progress=False)
        if data.empty:
            print(f"No data downloaded for {symbol}.")
            return None

        if isinstance(data.columns, pd.MultiIndex):
            df = pd.DataFrame()
            df['open'] = data[('Open', symbol)]
            df['high'] = data[('High', symbol)]
            df['low'] = data[('Low', symbol)]
            df['close'] = data[('Close', symbol)]
            df['volume'] = data[('Volume', symbol)]
            df.index.name = 'timestamp' 
            data = df.reset_index() 
        else:
            data = data.reset_index()
            data.columns = [str(col).lower().replace('date', 'timestamp') for col in data.columns]

        data.columns = [str(col).lower() for col in data.columns] 
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_columns if col not in data.columns]

        if missing_cols:
            print(f"Warning: Missing required columns after processing: {missing_cols}")
            if 'close' in missing_cols and ('adj close' in data.columns or 'adj_close' in data.columns):
                 adj_col = 'adj close' if 'adj close' in data.columns else 'adj_close'
                 print(f"Using '{adj_col}' as 'close'.")
                 data['close'] = data[adj_col]
                 missing_cols.remove('close')
                 
            if missing_cols:
                print(f"Final missing columns: {missing_cols}. Cannot proceed.")
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

# --- Single Backtest Function ---
def run_single_backtest(data: pd.DataFrame, params: dict):
    """Runs the Regime RSI backtest for a given set of parameters."""
    initial_balance = 10000
    trading_fee = 0.001
    slippage_std = 0.001 
    risk_per_trade = 0.01
    
    # Unpack parameters
    atr_period = params.get('atr_period', 14)
    atr_multiplier_sl = params['atr_multiplier_sl']
    take_profit_ratio = params['take_profit_ratio']
    rsi_period = params.get('rsi_period', 14)
    rsi_ob = params.get('rsi_ob', 70)
    rsi_os = params.get('rsi_os', 30)
    rsi_trend_entry_level = params.get('rsi_trend_entry_level', 50)
    adx_period = params.get('adx_period', 14)
    adx_threshold = params['adx_threshold']

    # --- Calculate Indicators ---
    # Note: Ensure columns are unique if running multiple times or create copies
    local_data = data.copy()
    atr_col = f'ATR_{atr_period}'
    rsi_col = f'RSI_{rsi_period}'
    adx_col = f'adx_{adx_period}'
    dmp_col = f'dmp_{adx_period}'
    dmn_col = f'dmn_{adx_period}'

    local_data[atr_col] = calculate_atr(local_data, period=atr_period)
    local_data[rsi_col] = calculate_rsi(local_data, period=rsi_period)
    adx_df = calculate_adx(local_data, period=adx_period)
    local_data = pd.concat([local_data, adx_df], axis=1)

    # --- Backtesting Engine Setup ---
    backtest = BacktestEngine(local_data, initial_balance, trading_fee, slippage_std)
    stop_loss_price = None
    take_profit_price = None
    skip_period = max(rsi_period, adx_period, atr_period)
    
    for i in range(skip_period, len(local_data)):
        backtest.current_index = i
        current_candle = local_data.iloc[i]
        prev_candle = local_data.iloc[i-1]
        
        # --- Add Progress Indicator ---
        if i % 100 == 0: # Print every 100 bars
            print(f".", end="", flush=True)
        # --- End Progress Indicator ---

        current_price = current_candle['close']
        current_low = current_candle['low']
        current_high = current_candle['high']
        current_atr = current_candle[atr_col]
        current_rsi = current_candle[rsi_col]
        current_adx = current_candle[adx_col]
        current_dmp = current_candle[dmp_col]
        current_dmn = current_candle[dmn_col]
        prev_rsi = prev_candle[rsi_col]

        if pd.isna(current_atr) or pd.isna(current_rsi) or pd.isna(current_adx) or pd.isna(prev_rsi):
            continue

        # --- SL/TP Exit Check --- 
        position_closed_by_sl_tp = False
        if backtest.position_size > 0: # Long exit
            if stop_loss_price is not None and current_low <= stop_loss_price:
                backtest.execute_market_order(backtest.position_size, stop_loss_price, 'sell')
                position_closed_by_sl_tp = True
            elif take_profit_price is not None and current_high >= take_profit_price:
                backtest.execute_market_order(backtest.position_size, take_profit_price, 'sell')
                position_closed_by_sl_tp = True
        elif backtest.position_size < 0: # Short exit
            if stop_loss_price is not None and current_high >= stop_loss_price: 
                backtest.execute_market_order(abs(backtest.position_size), stop_loss_price, 'buy')
                position_closed_by_sl_tp = True
            elif take_profit_price is not None and current_low <= take_profit_price: 
                backtest.execute_market_order(abs(backtest.position_size), take_profit_price, 'buy')
                position_closed_by_sl_tp = True

        if position_closed_by_sl_tp:
            stop_loss_price = None; take_profit_price = None
            backtest.update_portfolio_value(); continue 
            
        # --- Entry Logic --- 
        if backtest.position_size == 0: 
            is_trending = current_adx > adx_threshold
            is_ranging = not is_trending
            is_uptrend = is_trending and current_dmp > current_dmn
            is_downtrend = is_trending and current_dmn > current_dmp
            entry_signal = 0

            if is_ranging:
                if prev_rsi < rsi_os and current_rsi >= rsi_os: entry_signal = 1
                elif prev_rsi > rsi_ob and current_rsi <= rsi_ob: entry_signal = -1
            elif is_trending:
                if is_uptrend and (prev_rsi < rsi_trend_entry_level and current_rsi >= rsi_trend_entry_level):
                    entry_signal = 1
                elif is_downtrend and (prev_rsi > rsi_trend_entry_level and current_rsi <= rsi_trend_entry_level):
                    entry_signal = -1

            if entry_signal != 0:
                entry_price = current_price
                sl_distance = current_atr * atr_multiplier_sl
                if sl_distance <= 0: continue 

                if entry_signal == 1: # Long entry
                    sl_price = entry_price - sl_distance
                    tp_price = entry_price + sl_distance * take_profit_ratio
                    price_risk = entry_price - sl_price
                    if price_risk <= 0: continue
                    position_size = (backtest.available_balance * risk_per_trade) / price_risk
                    order = backtest.execute_market_order(position_size, entry_price, 'buy')
                    if order.status == OrderStatus.FILLED:
                        stop_loss_price = sl_price; take_profit_price = tp_price

                elif entry_signal == -1: # Short entry
                    sl_price = entry_price + sl_distance
                    tp_price = entry_price - sl_distance * take_profit_ratio
                    price_risk = sl_price - entry_price
                    if price_risk <= 0: continue
                    position_size = (backtest.available_balance * risk_per_trade) / price_risk
                    order = backtest.execute_market_order(position_size, entry_price, 'sell')
                    if order.status == OrderStatus.FILLED:
                        stop_loss_price = sl_price; take_profit_price = tp_price

        backtest.update_portfolio_value()
            
    # --- Return Results --- 
    metrics = backtest.get_performance_metrics()
    # Add win rate calculation to metrics
    if metrics['num_trades'] > 0:
        profitable_trades = sum(1 for trade in backtest.trades if hasattr(trade, 'realized_pnl') and trade.realized_pnl is not None and trade.realized_pnl > 0)
        # Ensure division by zero is avoided if only entry trades exist
        num_closed_trades = metrics['num_trades'] / 2
        metrics['win_rate'] = (profitable_trades / num_closed_trades * 100) if num_closed_trades > 0 else 0
    else:
        metrics['win_rate'] = 0
        
    return metrics, backtest # Return metrics and the backtest instance

# --- Optimization Main Block ---
def main():
    # --- Use Best Parameters Found --- 
    best_params = {
        'adx_threshold': 30,
        'atr_multiplier_sl': 2.5,
        'take_profit_ratio': 2.0
        # Assuming other params like rsi_period=14, adx_period=14 are kept default
    }
    
    # --- Load Data for Different Symbol ---
    symbol_to_test = 'ETH-USD' # Test on ETH-USD
    print(f"Loading historical data for {symbol_to_test}...")
    data = load_historical_data(symbol=symbol_to_test, start_date='2022-01-01', end_date='2023-12-31')
    if data is None:
        sys.exit("Failed to load data.")
    print("\nData loaded. Running backtest with best parameters...")
    
    # --- Run Backtest with Best Params ---
    final_metrics, final_backtest = run_single_backtest(data, best_params)

    # --- Print Results ---
    print("\n--- Backtest Complete for ETH-USD using Best BTC Params ---")
    print("Parameters Used:")
    print(best_params)
    print("\nPerformance Metrics:")
    if final_metrics:
        print(f"  Total Return: {final_metrics['total_return']:.2%}")
        print(f"  Annualized Return: {final_metrics['annualized_return']:.2%}")
        print(f"  Sharpe Ratio: {final_metrics['sharpe_ratio']:.2f}")
        print(f"  Max Drawdown: {final_metrics['max_drawdown']:.2%}")
        print(f"  Number of Trades: {final_metrics['num_trades']}")
        print(f"  Win Rate: {final_metrics['win_rate']:.2f}%")
    else:
        print("Backtest failed to produce metrics.")

    # --- Plotting --- 
    if final_metrics:
        print("\nPlotting results...")
        fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True, gridspec_kw={'height_ratios': [3, 1, 1]})
        ax1, ax2, ax3 = axes
        
        # Plot Price and Trades
        ax1.plot(data['timestamp'], data['close'], label='Close Price', alpha=0.9, linewidth=1)
        if final_backtest.trades:
            buy_ts = [t.timestamp for t in final_backtest.trades if t.side.value == 'buy' and t.status == OrderStatus.FILLED]
            buy_pr = [t.filled_price for t in final_backtest.trades if t.side.value == 'buy' and t.status == OrderStatus.FILLED]
            sell_ts = [t.timestamp for t in final_backtest.trades if t.side.value == 'sell' and t.status == OrderStatus.FILLED]
            sell_pr = [t.filled_price for t in final_backtest.trades if t.side.value == 'sell' and t.status == OrderStatus.FILLED]
            ax1.plot(buy_ts, buy_pr, '^', markersize=8, color='lime', label='Buy', markeredgecolor='black', lw=0)
            ax1.plot(sell_ts, sell_pr, 'v', markersize=8, color='red', label='Sell', markeredgecolor='black', lw=0)
        ax1.set_title(f'Regime RSI Strategy on {symbol_to_test} - Params: {best_params}')
        ax1.set_ylabel('Price'); ax1.legend(); ax1.grid(True)

        # Plot Portfolio Value
        portfolio_values_aligned = final_backtest.portfolio_values.copy()
        portfolio_values_aligned.index = data['timestamp'][:len(portfolio_values_aligned)]
        ax2.plot(portfolio_values_aligned.index, portfolio_values_aligned.values, label='Portfolio Value')
        ax2.set_ylabel('Portfolio Value ($)'); ax2.legend(); ax2.grid(True)

        # Plot RSI and ADX
        rsi_period = best_params.get('rsi_period', 14) 
        adx_period = best_params.get('adx_period', 14)
        rsi_col = f'RSI_{rsi_period}'
        adx_col = f'adx_{adx_period}'
        # Recalculate indicators just in case they weren't added to original `data`
        if rsi_col not in data.columns: data[rsi_col] = calculate_rsi(data, period=rsi_period)
        if adx_col not in data.columns: 
             adx_df_final = calculate_adx(data, period=adx_period)
             data = pd.concat([data, adx_df_final], axis=1)
        
        ax3.plot(data['timestamp'], data[rsi_col], label=f'RSI({rsi_period})', color='purple', alpha=0.7)
        ax3.axhline(best_params.get('rsi_ob', 70), color='red', linestyle='--', alpha=0.5, label='Overbought')
        ax3.axhline(best_params.get('rsi_os', 30), color='green', linestyle='--', alpha=0.5, label='Oversold')
        ax3.axhline(best_params.get('rsi_trend_entry_level', 50), color='gray', linestyle=':', alpha=0.5, label='Trend Level')
        ax3.set_ylabel('RSI', color='purple'); ax3.tick_params(axis='y', labelcolor='purple'); ax3.legend(loc='upper left')
        
        ax3b = ax3.twinx()
        ax3b.plot(data['timestamp'], data[adx_col], label=f'ADX({adx_period})', color='blue', alpha=0.6)
        ax3b.axhline(best_params['adx_threshold'], color='black', linestyle='--', alpha=0.5, label='Trend Threshold')
        ax3b.set_ylabel('ADX', color='blue'); ax3b.tick_params(axis='y', labelcolor='blue'); ax3b.legend(loc='upper right')

        ax3.set_xlabel('Date'); ax3.grid(True)
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main() 