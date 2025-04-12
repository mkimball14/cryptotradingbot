import pandas as pd
import numpy as np
import itertools
from tqdm import tqdm # Progress bar
import matplotlib.pyplot as plt # Import for plotting
import matplotlib.patches as patches # Import for zone rectangles

from app.core.market_simulator import MarketSimulator
from app.core.backtest_engine import BacktestEngine
from app.core.models import OrderSide, OrderStatus

# --- Import shared functions from the example script ---
# Adjust import path if necessary
from market_simulation_example import calculate_atr, calculate_rsi # Keep ATR for SL sizing
# Remove MA crossover strategy import
# from market_simulation_example import create_sample_strategy 

# --- Import Zone Detection --- 
# Assuming src is accessible in PYTHONPATH or relative path works
# If not, copy detect_base_patterns and its helpers here
try:
    from src.zone_detector import detect_base_patterns, is_leg_candle, is_base_candle, get_candle_direction # Import necessary functions
except ImportError:
    print("ERROR: Could not import from src.zone_detector. Make sure PYTHONPATH is set or copy functions.")
    # Define dummy function if import fails to avoid immediate crash
    def detect_base_patterns(df): 
        print("WARNING: Using dummy detect_base_patterns function.")
        return [] 

def run_zone_backtest(params, base_data, detected_zones):
    """
    Runs a single backtest simulation for the S/D Zone strategy.
    Returns:
        tuple: (performance metrics dict, BacktestEngine instance)
    """
    # --- Extract parameters ---
    atr_period = params['atr_p']
    atr_multiplier = params['atr_m'] # Used for SL distance *from zone edge*
    take_profit_ratio = params['tp_r']
    risk_per_trade = params['risk_per_trade']
    min_freshness = params['min_fresh'] # New
    min_strength = params['min_strength'] # New
    rsi_period = params['rsi_p'] # New - Needed for confirmation
    # Rename parameters for clarity
    # rsi_confirm_long_threshold = params['rsi_cl'] 
    # rsi_confirm_short_threshold = params['rsi_cs']
    # Remove extraction of unused RSI threshold params
    # rsi_oversold_threshold = params['rsi_os'] # New name
    # rsi_overbought_threshold = params['rsi_ob'] # New name
    
    # --- Simulation & Indicators (using the provided base_data) ---
    data = base_data.copy() # Use fresh copy
    simulator = MarketSimulator(data, random_seed=42)
    scenarios = [
        {'type': 'trend', 'start_idx': 30, 'duration': 60, 'parameters': {'trend_strength': 0.005}},
        {'type': 'volatility', 'start_idx': 100, 'duration': 30, 'parameters': {'intensity': 1.5}},
        {'type': 'gap', 'start_idx': 150, 'parameters': {'gap_percent': -2.0}}
    ]
    simulated_data = simulator.combine_scenarios(scenarios)
    simulated_data[f'ATR{atr_period}'] = calculate_atr(simulated_data, period=atr_period)
    # Calculate RSI needed for confirmation
    simulated_data[f'RSI{rsi_period}'] = calculate_rsi(simulated_data, period=rsi_period)
    
    # --- Backtesting Setup ---
    backtest = BacktestEngine(
        historical_data=simulated_data.reset_index(),
        initial_balance=10000,
        trading_fee=0.001,
        slippage_std=0.001
    )

    stop_loss_price = None
    take_profit_price = None
    # Skip period needs to account for RSI now too
    skip_period = max(atr_period, rsi_period) 
    
    active_trade_zone_indices = set() # Track indices of zones currently being traded
    ohlcv_df_for_indices = base_data.reset_index() # Need this for zone timestamps
    previous_rsi = np.nan # Initialize previous RSI tracker
    
    # --- Backtest Loop --- 
    for i in range(len(simulated_data)):
        backtest.current_index = i
        current_time = simulated_data.index[i]
        current_price = simulated_data.iloc[i]['close']
        current_low = simulated_data.iloc[i]['low']
        current_high = simulated_data.iloc[i]['high']
        current_atr = simulated_data.iloc[i][f'ATR{atr_period}']
        current_rsi = simulated_data.iloc[i][f'RSI{rsi_period}'] # Get RSI
        
        # Update skip condition for RSI
        if i < skip_period or pd.isna(current_atr) or pd.isna(current_rsi):
            previous_rsi = current_rsi # Update previous RSI even during skip
            backtest.update_portfolio_value()
            continue

        # --- SL/TP Exit Check --- (Same as before)
        position_closed_by_sl_tp = False
        if backtest.position_size > 0: # Long exit check
            if stop_loss_price is not None and current_low <= stop_loss_price:
                backtest.execute_market_order(backtest.position_size, stop_loss_price, 'sell')
                position_closed_by_sl_tp = True
            elif take_profit_price is not None and current_high >= take_profit_price:
                backtest.execute_market_order(backtest.position_size, take_profit_price, 'sell')
                position_closed_by_sl_tp = True
        elif backtest.position_size < 0: # Short exit check
            if stop_loss_price is not None and current_high >= stop_loss_price:
                backtest.execute_market_order(abs(backtest.position_size), stop_loss_price, 'buy')
                position_closed_by_sl_tp = True
            elif take_profit_price is not None and current_low <= take_profit_price:
                backtest.execute_market_order(abs(backtest.position_size), take_profit_price, 'buy')
                position_closed_by_sl_tp = True

        if position_closed_by_sl_tp:
            stop_loss_price = None
            take_profit_price = None
            active_trade_zone_indices.clear() # Clear traded zones on exit
            backtest.update_portfolio_value()
            continue 
            
        # --- S/D Zone Entry Logic --- 
        if backtest.position_size == 0: # Only look for entries if flat
            potential_entry_zone = None
            trade_side = None
            zone_idx_to_trade = -1 # Keep track of which zone index we are trading

            # Find the *most recently formed* zone that price is currently touching
            # Iterate zones in reverse (assuming detect_base_patterns returns chronologically)
            for zone_idx, zone in reversed(list(enumerate(detected_zones))):
                 # Skip if this zone has already resulted in the current/last trade
                 # or if zone formed after current time (shouldn't happen if zones pre-calculated)
                 zone_formation_time = ohlcv_df_for_indices.iloc[zone['leg_out_index']]['timestamp']
                 if zone_idx in active_trade_zone_indices or zone_formation_time > current_time:
                     continue 
                     
                 # --- Filter Zone by Score --- 
                 freshness = zone.get('freshness_score', 0)
                 strength = zone.get('strength_score', 0)
                 if freshness < min_freshness or strength < min_strength:
                     print(f"[{current_time.date()}] Zone {zone_idx} rejected: freshness={freshness}<{min_freshness} or strength={strength}<{min_strength}")
                     continue # Skip low-quality zone
                     
                 print(f"[{current_time.date()}] Zone {zone_idx} passed filtering: freshness={freshness}, strength={strength}. Range: {zone['zone_low']:.2f}-{zone['zone_high']:.2f}, Type: {zone['type']}")
                 zone_low_price = zone['zone_low']
                 zone_high_price = zone['zone_high']
                 closed_in_zone = zone_low_price <= current_price <= zone_high_price

                 if closed_in_zone:
                      # --- Check RSI Crossover Confirmation --- 
                      entry_confirmed = False
                      # Check for Demand Zone + RSI crossing ABOVE oversold
                      # if zone['type'] == 'demand' and previous_rsi <= rsi_oversold_threshold and current_rsi > rsi_oversold_threshold:
                      #      entry_confirmed = True
                      #      trade_side = 'buy'
                      # Check for Supply Zone + RSI crossing BELOW overbought
                      # elif zone['type'] == 'supply' and previous_rsi >= rsi_overbought_threshold and current_rsi < rsi_overbought_threshold:
                      #      entry_confirmed = True
                      #      trade_side = 'sell'
                      
                      # --- MODIFIED: Remove RSI check, confirm based on zone type only --- 
                      if zone['type'] == 'demand':
                          trade_side = 'buy'
                          entry_confirmed = True # Confirm if closed in valid demand zone
                      elif zone['type'] == 'supply':
                           trade_side = 'sell'
                           entry_confirmed = True # Confirm if closed in valid supply zone
                      # --- End MODIFICATION ---
                      
                      if entry_confirmed:
                           potential_entry_zone = zone
                           zone_idx_to_trade = zone_idx
                           break # Found valid zone and confirmation
                      # else: print(f"[{current_time.date()}] Closed in zone but RSI ({previous_rsi:.1f}->{current_rsi:.1f}) failed crossover.")
            
            # Execute trade if entry found and confirmed
            if potential_entry_zone and trade_side:
                active_trade_zone_indices.add(zone_idx_to_trade)
                zone = potential_entry_zone
                entry_price = current_price
                sl_distance_atr = current_atr * atr_multiplier
                if trade_side == 'buy':
                    sl_price = zone['zone_low'] - sl_distance_atr
                    tp_distance = abs(entry_price - sl_price) * take_profit_ratio # Use abs for safety
                    tp_price = entry_price + tp_distance
                else: 
                    sl_price = zone['zone_high'] + sl_distance_atr
                    tp_distance = abs(sl_price - entry_price) * take_profit_ratio # Use abs for safety
                    tp_price = entry_price - tp_distance

                portfolio_value = backtest.available_balance
                risk_amount = portfolio_value * risk_per_trade
                stop_loss_distance_points = abs(entry_price - sl_price)

                if stop_loss_distance_points > 0:
                    shares_to_trade = risk_amount / stop_loss_distance_points
                    print(f"[{current_time.date()}] Attempting {trade_side.upper()} entry... Zone ({zone['zone_low']:.2f}-{zone['zone_high']:.2f}) Confirmed RSI: {current_rsi:.1f}. SL: {sl_price:.2f}, TP: {tp_price:.2f}")
                    order = backtest.execute_market_order(shares_to_trade, entry_price, trade_side)
                    if order.status == OrderStatus.FILLED:
                        stop_loss_price = sl_price
                        take_profit_price = tp_price
                    else:
                        active_trade_zone_indices.remove(zone_idx_to_trade) 
                else:
                    print(f"[{current_time.date()}] {trade_side.upper()} signal skipped - zero stop distance.")
                    active_trade_zone_indices.remove(zone_idx_to_trade) 
                    
        # Update portfolio value & previous RSI for next iteration
        backtest.update_portfolio_value()
        previous_rsi = current_rsi # Update previous RSI at the end of the loop
            
    # --- Return Results --- 
    metrics = backtest.get_performance_metrics()
    metrics.update(params) # Include params in results
    # Return the engine instance as well for later plotting
    return metrics, backtest, simulated_data, ohlcv_df_for_indices

# --- Main Optimization --- 
if __name__ == "__main__":
    # --- Define Parameters for Zone Strategy --- 
    param_grid = {
        'atr_p': [14],
        'atr_m': [0.5, 1.0], # SL buffer multiplier
        'tp_r': [1.0, 1.5], # R:R ratio
        'risk_per_trade': [0.01],
        'min_fresh': [1], # Only test with minimum freshness (all zones have freshness=1)
        'min_strength': [10, 30], # Significantly lower minimum strength thresholds
        'rsi_p': [14],
        # Rename RSI params for crossover logic
        # 'rsi_cl': [30], 
        # 'rsi_cs': [70]
        # 'rsi_os': [30, 40], # Oversold threshold to cross above - REMOVED
        # 'rsi_ob': [70, 60]  # Overbought threshold to cross below - REMOVED
    }

    keys, values = zip(*param_grid.items())
    param_combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
    print(f"Starting S/D Zone strategy optimization (Score Filter Only) with {len(param_combinations)} parameter combinations...")

    # --- Prepare Base Data & Detect Zones (Once) --- 
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    base_data = pd.DataFrame({
        'timestamp': dates,
        'open': np.random.normal(100, 2, len(dates)),
        'high': np.random.normal(105, 3, len(dates)),
        'low': np.random.normal(95, 3, len(dates)),
        'close': np.random.normal(102, 2, len(dates)),
        'volume': np.random.normal(1000, 200, len(dates))
    })
    base_data['high'] = base_data[['high', 'open', 'close']].max(axis=1)
    base_data['low'] = base_data[['low', 'open', 'close']].min(axis=1)
    base_data.set_index('timestamp', inplace=True)
    
    # Need a copy with timestamp column for zone detection function
    ohlcv_df = base_data.reset_index().copy()
    print("Detecting S/D zones...")
    # Ensure necessary columns for detector exist
    if not all(col in ohlcv_df.columns for col in ['timestamp', 'open', 'high', 'low', 'close']):
        raise ValueError("Input DataFrame missing required OHLCV columns for zone detection.")
        
    detected_zones = detect_base_patterns(ohlcv_df) 
    print(f"Detected {len(detected_zones)} zones.")
    
    # --- DEBUG: Print zone details ---
    print("--- Detected Zone Details ---")
    if detected_zones:
        for idx, zone in enumerate(detected_zones):
            print(f"Zone {idx}: {zone}")
    else:
        print("No zones to detail.")
    print("---------------------------")
    # --- End DEBUG ---

    if not detected_zones:
        print("No zones detected, cannot run backtest.")
        exit()

    # --- Run Optimization Backtests --- 
    results_list = []
    best_backtest_instance = None # Store the engine instance for the best run
    best_simulated_data = None
    best_ohlcv_df = None
    best_params_run = None
    best_sharpe = -np.inf # Initialize best Sharpe ratio

    for params in tqdm(param_combinations, desc="Optimizing Zone Strategy"):
        try:
            metrics, backtest_instance, sim_data_run, ohlcv_df_run = run_zone_backtest(params, base_data, detected_zones)
            results_list.append(metrics)
            
            # Check if this run is the best so far based on Sharpe
            current_sharpe = metrics.get('sharpe_ratio', -np.inf)
            if pd.notna(current_sharpe) and current_sharpe > best_sharpe:
                best_sharpe = current_sharpe
                best_backtest_instance = backtest_instance
                best_simulated_data = sim_data_run
                best_ohlcv_df = ohlcv_df_run # Store df used for indices
                best_params_run = params
                
        except Exception as e:
            print(f"\nError during backtest with params {params}: {e}")

    # --- Analyze Optimization Results --- 
    if not results_list:
        print("No backtests completed successfully.")
    else:
        results_df = pd.DataFrame(results_list)
        results_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        results_df_sorted = results_df.sort_values(by=['sharpe_ratio', 'total_return'], ascending=[False, False]).dropna(subset=['sharpe_ratio', 'total_return'])
        
        print("\n--- Optimization Results (S/D Zone Strategy) ---")
        print(f"Total combinations tested: {len(param_combinations)}")
        print(f"Successful runs: {len(results_df)}")
        
        print("\n--- Top Results (Sorted by Sharpe Ratio) ---")
        display_cols = ['sharpe_ratio', 'total_return', 'max_drawdown', 'num_trades', 
                        'atr_m', 'tp_r', 'min_fresh', 'min_strength'] # Removed RSI params 
        for col in display_cols:
            if col not in results_df_sorted.columns:
                results_df_sorted[col] = np.nan 
        print(results_df_sorted[display_cols].head().to_string(index=False))

        # You can add more analysis here, like saving results_df to CSV
        # results_df.to_csv("optimization_results.csv", index=False) 

    # --- Plotting Results for Best Parameters --- 
    if best_backtest_instance:
        print(f"\nPlotting results for best parameters: {best_params_run}")
        
        # --- DEBUG: Print the trades list --- 
        print("\n--- Trades List from Best Run ---")
        if best_backtest_instance.trades:
            for trade in best_backtest_instance.trades:
                print(trade)
        else:
            print("No trades found in the best run instance.")
        print("---------------------------------")
        # --- End DEBUG ---
        
        plt.figure(figsize=(14, 10))
        
        # Price Chart (ax1)
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(best_simulated_data.index, best_simulated_data['close'], label='Simulated Close Price', alpha=0.7, linewidth=1)
        
        # Plot Zones
        for zone in detected_zones:
            zone_low = zone['zone_low']
            zone_high = zone['zone_high']
            # Get timestamps from the OHLCV df using the stored indices
            base_start_time = best_ohlcv_df.iloc[zone['base_start_index']]['timestamp']
            base_end_time = best_ohlcv_df.iloc[zone['base_end_index']]['timestamp']
            # Extend zone plotting slightly for visibility if base is short
            time_delta = pd.Timedelta(days=1) # Extend by 1 day
            plot_end_time = max(base_end_time + time_delta, best_simulated_data.index[-1]) # Don't plot past data end
            
            color = 'green' if zone['type'] == 'demand' else 'red'
            ax1.fill_between(best_simulated_data.index, zone_low, zone_high, 
                             where=(best_simulated_data.index >= base_start_time) & (best_simulated_data.index <= plot_end_time),
                             color=color, alpha=0.15, label=f"_Zone {zone['type']}") # Underscore hides duplicate labels

        # Plot Trades
        if best_backtest_instance.trades:
            # --- DEBUG: Check trade list contents before plotting --- 
            print("\n--- Checking Trades for Plotting ---")
            print(f"Total trades in list: {len(best_backtest_instance.trades)}")
            buy_timestamps = [t.timestamp for t in best_backtest_instance.trades if t.side == OrderSide.BUY and t.status == OrderStatus.FILLED]
            buy_prices = [t.filled_price for t in best_backtest_instance.trades if t.side == OrderSide.BUY and t.status == OrderStatus.FILLED]
            sell_timestamps = [t.timestamp for t in best_backtest_instance.trades if t.side == OrderSide.SELL and t.status == OrderStatus.FILLED]
            sell_prices = [t.filled_price for t in best_backtest_instance.trades if t.side == OrderSide.SELL and t.status == OrderStatus.FILLED]
            
            print(f"Found {len(buy_timestamps)} Buy markers to plot.")
            # print(f"Buy Timestamps: {buy_timestamps}") # Can be verbose
            # print(f"Buy Prices: {buy_prices}")
            print(f"Found {len(sell_timestamps)} Sell markers to plot.")
            # print(f"Sell Timestamps: {sell_timestamps}") # Can be verbose
            print(f"Sell Prices: {sell_prices}")
            print("------------------------------------")
            # --- End DEBUG --- 
            
            # Try using scatter instead of plot for markers
            # if buy_timestamps: ax1.plot(buy_timestamps, buy_prices, '^', markersize=8, color='lime', label='Buy')
            # if sell_timestamps: ax1.plot(sell_timestamps, sell_prices, 'v', markersize=8, color='red', label='Sell')
            if buy_timestamps: ax1.scatter(buy_timestamps, buy_prices, marker='^', s=60, color='lime', label='Buy', zorder=3)
            if sell_timestamps: ax1.scatter(sell_timestamps, sell_prices, marker='v', s=60, color='red', label='Sell', zorder=3)

        ax1.set_title(f"S/D Zone Strategy Backtest (Best Params: {best_params_run})")
        ax1.set_ylabel("Price")
        ax1.legend()
        ax1.grid(True)

        # Portfolio Value Chart (ax2)
        ax2 = plt.subplot(2, 1, 2, sharex=ax1)
        portfolio_dates = best_simulated_data.index[:len(best_backtest_instance.portfolio_values)]
        ax2.plot(portfolio_dates, best_backtest_instance.portfolio_values.values, label='Portfolio Value')
        ax2.set_title("Portfolio Value Over Time")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Portfolio Value ($)")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()
    else:
        print("\nCould not generate plot - no successful backtest run found.") 