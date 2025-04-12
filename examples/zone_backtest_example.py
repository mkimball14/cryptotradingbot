import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import yfinance as yf

from app.core.backtest_engine import BacktestEngine
from src.zone_detector import detect_base_patterns, calculate_rsi
from app.core.models import OrderStatus

def load_historical_data(symbol='BTC-USD', start_date='2023-01-01', end_date='2023-12-31'):
    """Load real historical cryptocurrency data from Yahoo Finance"""
    try:
        # Download data from Yahoo Finance
        data = yf.download(symbol, start=start_date, end=end_date)
        
        # Check if the dataframe has multi-level columns (happens with multiple symbols)
        if isinstance(data.columns, pd.MultiIndex):
            # We're only downloading one symbol, so we can select that level
            # If 'Close' is a multi-index column, it'll look like ('Close', 'BTC-USD')
            # Extract just the basic columns we need from the first level
            data = pd.DataFrame({
                'open': data['Open'][symbol] if ('Open', symbol) in data.columns else data['Open'],
                'high': data['High'][symbol] if ('High', symbol) in data.columns else data['High'],
                'low': data['Low'][symbol] if ('Low', symbol) in data.columns else data['Low'],
                'close': data['Close'][symbol] if ('Close', symbol) in data.columns else data['Close'],
                'volume': data['Volume'][symbol] if ('Volume', symbol) in data.columns else data['Volume'],
                'timestamp': data.index
            })
        else:
            # Simple columns
            data = data.reset_index()
            data.columns = [str(col).lower() for col in data.columns]
        
        # Ensure all column names are lowercase
        data.columns = [str(col).lower() for col in data.columns]
        
        # Check required columns
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in data.columns:
                print(f"Warning: Required column '{col}' not found in downloaded data.")
                print(f"Available columns: {data.columns.tolist()}")
                return None
        
        print(f"Loaded {len(data)} records of historical data for {symbol}")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        if 'data' in locals():
            print(f"Data columns: {data.columns.tolist() if hasattr(data, 'columns') else 'No columns'}")
        return None

class ZoneBacktestStrategy:
    """Supply/Demand Zone trading strategy with MA trend filter"""
    
    def __init__(self, zone_strength_threshold=50, zone_freshness_threshold=5, 
                 rsi_oversold=30, rsi_overbought=70, rsi_confirmation=False,
                 stop_loss_atr_multiplier=2.0, take_profit_atr_multiplier=3.0,
                 fast_ma_period=20, slow_ma_period=50): # Add MA periods
        """
        Initialize zone-based strategy parameters
        
        Args:
            zone_strength_threshold: Minimum strength score to consider a zone valid
            zone_freshness_threshold: Minimum freshness score to consider a zone valid
            rsi_oversold: RSI level below which is considered oversold
            rsi_overbought: RSI level above which is considered overbought
            rsi_confirmation: Whether to use RSI confirmation for entries
            stop_loss_atr_multiplier: ATR multiplier for stop loss placement
            take_profit_atr_multiplier: ATR multiplier for take profit placement
            fast_ma_period: Period for the fast moving average
            slow_ma_period: Period for the slow moving average
        """
        self.zone_strength_threshold = zone_strength_threshold
        self.zone_freshness_threshold = zone_freshness_threshold
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.rsi_confirmation = rsi_confirmation
        self.stop_loss_atr_multiplier = stop_loss_atr_multiplier
        self.take_profit_atr_multiplier = take_profit_atr_multiplier
        self.fast_ma_period = fast_ma_period # Store MA periods
        self.slow_ma_period = slow_ma_period # Store MA periods
        
        # State variables
        self.zones = []
        self.current_zone = None
        self.atr_value = None
        self.rsi_values = None
        self.fast_ma = None # Add MA series
        self.slow_ma = None # Add MA series
        self.stop_loss_level = None
        self.take_profit_level = None
        
    def detect_zones(self, ohlcv_data: pd.DataFrame) -> List[Dict]:
        """Detect supply and demand zones in the data"""
        detected_zones = detect_base_patterns(ohlcv_data.copy())
        
        # Filter zones based on strength and freshness
        filtered_zones = [
            zone for zone in detected_zones 
            if zone['strength_score'] >= self.zone_strength_threshold 
            and zone['freshness_score'] >= self.zone_freshness_threshold
        ]
        
        return filtered_zones
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> List[float]:
        """Calculate Average True Range for stop loss and take profit levels"""
        atr_values = []
        for i in range(len(data)):
            if i == 0:
                atr_values.append(data.iloc[0]['high'] - data.iloc[0]['low'])
                continue
                
            tr1 = data.iloc[i]['high'] - data.iloc[i]['low']  # Current high - low
            tr2 = abs(data.iloc[i]['high'] - data.iloc[i-1]['close'])  # Current high - prev close
            tr3 = abs(data.iloc[i]['low'] - data.iloc[i-1]['close'])  # Current low - prev close
            
            true_range = max(tr1, tr2, tr3)
            
            if i < period:
                atr_values.append(np.mean(atr_values + [true_range]))
            else:
                atr_values.append((atr_values[-1] * (period - 1) + true_range) / period)
                
        return atr_values
    
    def calculate_sma(self, series: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        return series.rolling(window=period).mean()
    
    def run_backtest(self, data: pd.DataFrame) -> tuple:
        """
        Run backtest with supply/demand zone strategy, MA trend filter, and entry confirmation candle.
        
        Returns:
            tuple: (backtest_engine, zones_detected)
        """
        # Prepare data
        self.zones = self.detect_zones(data)
        self.rsi_values = calculate_rsi(data['close'])
        self.atr_values = self.calculate_atr(data)
        self.fast_ma = self.calculate_sma(data['close'], self.fast_ma_period)
        self.slow_ma = self.calculate_sma(data['close'], self.slow_ma_period)
        
        backtest = BacktestEngine(data)
        
        start_index = max(14, self.slow_ma_period) 
        for i in range(start_index, len(data)-1):
            backtest.current_index = i
            
            # Update current state
            current_candle = data.iloc[i]
            current_price = current_candle['close']
            current_time = current_candle['timestamp']
            current_high = current_candle['high']
            current_low = current_candle['low']
            current_open = current_candle['open'] # Needed for confirmation candle check
            current_atr = self.atr_values[i]
            current_fast_ma = self.fast_ma.iloc[i]
            current_slow_ma = self.slow_ma.iloc[i]
            
            # --- Check for Exits First --- 
            if backtest.has_position:
                exit_reason = None
                if backtest.position_size > 0: # Long exit check
                    if current_low <= self.stop_loss_level:
                        exit_reason = f"LONG Stop Loss triggered at {self.stop_loss_level:.2f}"
                        exit_price = self.stop_loss_level
                    elif current_high >= self.take_profit_level:
                        exit_reason = f"LONG Take Profit triggered at {self.take_profit_level:.2f}"
                        exit_price = self.take_profit_level
                    
                    if exit_reason:
                        print(f"[{current_time.date()}] {exit_reason}")
                        backtest.execute_market_order(backtest.position_size, exit_price, 'sell')
                        self.stop_loss_level = None; self.take_profit_level = None; self.current_zone = None
                        continue 
                elif backtest.position_size < 0: # Short exit check
                    if current_high >= self.stop_loss_level:
                        exit_reason = f"SHORT Stop Loss triggered at {self.stop_loss_level:.2f}"
                        exit_price = self.stop_loss_level
                    elif current_low <= self.take_profit_level:
                        exit_reason = f"SHORT Take Profit triggered at {self.take_profit_level:.2f}"
                        exit_price = self.take_profit_level
                        
                    if exit_reason:
                        print(f"[{current_time.date()}] {exit_reason}")
                        backtest.execute_market_order(abs(backtest.position_size), exit_price, 'buy') 
                        self.stop_loss_level = None; self.take_profit_level = None; self.current_zone = None
                        continue 
            
            # --- Check for Entries --- 
            if backtest.has_position: 
                continue
            
            # --- Define Trend --- 
            is_uptrend = current_fast_ma > current_slow_ma
            is_downtrend = current_fast_ma < current_slow_ma

            # Check for zone interactions
            potential_entry_zone = None
            confirmation_candle_valid = False
            for zone in self.zones:
                # Skip zones that haven't formed yet or are too old
                if i <= zone['leg_out_index'] or (i - zone['leg_out_index']) > 100: 
                    continue
                
                # --- Apply Trend Filter --- 
                if zone['type'] == 'demand' and not is_uptrend:
                    continue 
                if zone['type'] == 'supply' and not is_downtrend:
                    continue 

                # Check if price entered the zone recently (e.g., previous bar or current)
                entered_zone_recently = (
                    (zone['zone_low'] <= current_high and zone['zone_high'] >= current_low) or 
                    (zone['zone_low'] <= data.iloc[i-1]['high'] and zone['zone_high'] >= data.iloc[i-1]['low'])
                )
                
                if not entered_zone_recently:
                    continue

                # Check if the *current* candle closed within the zone AND shows confirmation
                closed_in_zone = zone['zone_low'] <= current_price <= zone['zone_high']
                if not closed_in_zone:
                    continue

                # --- Add Confirmation Candle Check --- 
                if zone['type'] == 'demand':
                    # Look for a bullish confirmation candle (Close > Open)
                    if current_price > current_open:
                        confirmation_candle_valid = True
                    # else: print(f"[{current_time.date()}] In Demand Zone, Trend UP, but candle not bullish ({current_open:.2f} -> {current_price:.2f})")
                elif zone['type'] == 'supply':
                    # Look for a bearish confirmation candle (Close < Open)
                    if current_price < current_open:
                        confirmation_candle_valid = True
                    # else: print(f"[{current_time.date()}] In Supply Zone, Trend DOWN, but candle not bearish ({current_open:.2f} -> {current_price:.2f})")

                # Check RSI confirmation (optional - currently off)
                # ... (RSI logic)

                if confirmation_candle_valid: # Found a potential entry zone aligned with trend and confirmed by candle
                    potential_entry_zone = zone
                    break
            
            # If a potential entry zone was found with confirmation, execute the trade
            if potential_entry_zone:
                zone = potential_entry_zone
                
                # --- Entry Execution (remains largely the same) --- 
                if zone['type'] == 'demand':
                    entry_price = current_price 
                    stop_loss = zone['zone_low'] - (current_atr * self.stop_loss_atr_multiplier)
                    take_profit = entry_price + (current_atr * self.take_profit_atr_multiplier)
                    
                    risk_amount = backtest.available_balance * 0.01
                    price_risk = entry_price - stop_loss
                    if price_risk <= 0: continue
                    position_size = risk_amount / price_risk
                    
                    print(f"[{current_time.date()}] Attempting LONG entry at {entry_price:.2f} " +
                          f"(Zone: {zone['zone_low']:.2f}-{zone['zone_high']:.2f}, Trend: UP, Confirm: Bullish Candle). " +
                          f"SL: {stop_loss:.2f}, TP: {take_profit:.2f}")
                    
                    order = backtest.execute_market_order(position_size, entry_price, 'buy')
                    
                    if order.status == OrderStatus.FILLED:
                        self.stop_loss_level = stop_loss
                        self.take_profit_level = take_profit
                    
                elif zone['type'] == 'supply':
                    entry_price = current_price
                    stop_loss = zone['zone_high'] + (current_atr * self.stop_loss_atr_multiplier)
                    take_profit = entry_price - (current_atr * self.take_profit_atr_multiplier)
                    
                    risk_amount = backtest.available_balance * 0.01
                    price_risk = stop_loss - entry_price
                    if price_risk <= 0: continue
                    position_size = risk_amount / price_risk
                    
                    print(f"[{current_time.date()}] Attempting SHORT entry at {entry_price:.2f} " +
                          f"(Zone: {zone['zone_low']:.2f}-{zone['zone_high']:.2f}, Trend: DOWN, Confirm: Bearish Candle). " +
                          f"SL: {stop_loss:.2f}, TP: {take_profit:.2f}")
                    
                    order = backtest.execute_market_order(position_size, entry_price, 'sell')
                    
                    if order.status == OrderStatus.FILLED:
                        self.stop_loss_level = stop_loss
                        self.take_profit_level = take_profit
        
        # Final portfolio update
        backtest.current_index = len(data) - 1
        backtest.update_portfolio_value()
        
        return backtest, self.zones

def visualize_backtest_results(data, backtest_engine, zones):
    """Visualize the backtest results with zones, MAs, and trades"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # Plot price and MAs
    ax1.plot(data['timestamp'], data['close'], label='Close Price', color='blue', alpha=0.8)
    ax1.plot(data['timestamp'], backtest_engine.strategy.fast_ma, label=f'{backtest_engine.strategy.fast_ma_period}-day MA', color='orange', linestyle='--', alpha=0.7)
    ax1.plot(data['timestamp'], backtest_engine.strategy.slow_ma, label=f'{backtest_engine.strategy.slow_ma_period}-day MA', color='purple', linestyle=':', alpha=0.7)

    # Plot Zones (simplified for clarity)
    for zone in zones:
        if len(zones) > 100 and zone['strength_score'] < 50: # Reduce clutter further
            continue
            
        zone_start_idx = zone['base_start_index']
        # Find end timestamp index robustly
        zone_end_plot_idx = min(len(data)-1, zone['leg_out_index'] + 20)
        zone_start_time = data.iloc[zone_start_idx]['timestamp']
        zone_end_time = data.iloc[zone_end_plot_idx]['timestamp']
        
        color = 'green' if zone['type'] == 'demand' else 'red'
        alpha = 0.15
        
        ax1.fill_between(data['timestamp'], zone['zone_low'], zone['zone_high'], 
                         where=(data['timestamp'] >= zone_start_time) & (data['timestamp'] <= zone_end_time),
                         alpha=alpha, color=color, label=f"_Zone {zone['type']}")
    
    # Plot Trades
    buy_dates = []
    buy_prices = []
    sell_dates = []
    sell_prices = []
    
    for trade in backtest_engine.trades:
        if trade.side.value == 'buy':
            buy_dates.append(trade.timestamp)
            buy_prices.append(trade.filled_price)
        else:
            sell_dates.append(trade.timestamp)
            sell_prices.append(trade.filled_price)
    
    ax1.scatter(buy_dates, buy_prices, marker='^', color='lime', s=100, label='Buy', edgecolors='black', zorder=5)
    ax1.scatter(sell_dates, sell_prices, marker='v', color='red', s=100, label='Sell', edgecolors='black', zorder=5)
    
    # Plot Portfolio Value
    ax2.plot(data['timestamp'], backtest_engine.portfolio_values, label='Portfolio Value', color='purple')
    
    # Formatting
    ax1.set_title('Supply/Demand Zones, MAs, and Trades')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True)
    
    ax2.set_title('Portfolio Value')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Value ($)')
    ax2.grid(True)
    
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()

def print_performance_metrics(backtest_engine):
    """Print the performance metrics of the backtest"""
    metrics = backtest_engine.get_performance_metrics()
    
    print("\nBacktest Performance Metrics:")
    print(f"Total Return: {metrics['total_return']*100:.2f}%")
    print(f"Annualized Return: {metrics['annualized_return']*100:.2f}%")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {metrics['max_drawdown']*100:.2f}%")
    print(f"Number of Trades: {metrics['num_trades']}")
    
    # Calculate win rate
    profitable_trades = sum(1 for trade in backtest_engine.trades if hasattr(trade, 'realized_pnl') and trade.realized_pnl > 0)
    if metrics['num_trades'] > 0:
        win_rate = profitable_trades / metrics['num_trades'] * 100
        print(f"Win Rate: {win_rate:.2f}%")
    
    # Calculate average profit/loss
    if metrics['num_trades'] > 0:
        total_pnl = sum(trade.realized_pnl for trade in backtest_engine.trades if hasattr(trade, 'realized_pnl'))
        avg_pnl = total_pnl / metrics['num_trades']
        print(f"Average P&L per Trade: ${avg_pnl:.2f}")

if __name__ == "__main__":
    # Load data
    print("Loading historical cryptocurrency data...")
    data = load_historical_data(symbol='BTC-USD', start_date='2022-01-01', end_date='2023-12-31')
    
    if data is None or len(data) == 0:
        print("Failed to load historical data. Exiting.")
        sys.exit(1)
    
    # Run backtest with the combined strategy
    print("Running backtest with Supply/Demand Zone + MA Trend Filter strategy...")
    strategy = ZoneBacktestStrategy(
        zone_strength_threshold=30,  # Keep slightly lower threshold
        zone_freshness_threshold=1,
        rsi_oversold=30,
        rsi_overbought=70,
        rsi_confirmation=False, 
        stop_loss_atr_multiplier=2.0, # Adjusted SL
        take_profit_atr_multiplier=3.0, # Adjusted TP
        fast_ma_period=20,
        slow_ma_period=50
    )
    
    # Assign strategy to backtest engine for visualization access
    backtest, zones = strategy.run_backtest(data)
    backtest.strategy = strategy # Store strategy instance for MA access in plotting
    
    # Print results
    print(f"\nDetected {len(zones)} zones ({sum(1 for z in zones if z['type'] == 'demand')} demand, {sum(1 for z in zones if z['type'] == 'supply')} supply)")
    print_performance_metrics(backtest)
    
    # Visualize results
    visualize_backtest_results(data, backtest, zones) 