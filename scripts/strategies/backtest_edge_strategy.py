import sys
import os
from pathlib import Path
import vectorbtpro as vbt # Import vectorbtpro
from datetime import datetime # Import datetime
import logging
import argparse

# Add the parent directory to the path
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Attempt to import data fetcher from multiple potential locations
try:
    from data.data_fetcher import fetch_historical_data, get_granularity_str, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    logger.info("Using data_fetcher from data module.")
except ImportError:
    try:
        # Fallback if not found in data module (adjust path if needed)
        from scripts.utils.historical_data import fetch_historical_data
        logger.info("Using historical_data from scripts.utils module.")
    except ImportError:
        try:
            # Fallback to importing from backtest_stoch_sma_vbt_pro
            from scripts.backtest_stoch_sma_vbt_pro import fetch_historical_data, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
            logger.info("Using functions from backtest_stoch_sma_vbt_pro.")
        except ImportError as e:
            logger.error(f"Could not import data fetching functions: {e}")
            sys.exit(1)

from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy

# Define parameters - Use results from latest TSL optimization
# OR load from best_edge_params.json if available
start_date = "2021-01-01" # Extended start date
end_date = datetime.now().strftime('%Y-%m-%d') # End today
symbol = "BTC-USD"
granularity_str = "1h" # Use string for fetcher
granularity_seconds = 3600 # Use seconds for vbt freq

# --- Default/Optimal parameters --- 
# Ideally, load these from best_edge_params.json
lookback_window = 25
volatility_threshold = 0.5
initial_capital = 3000
optimal_factor_weights = {
    'volatility_regime': 0.3,
    'consolidation_breakout': 0.3,
    'volume_divergence': 0.2,
    'market_microstructure': 0.2
}
tsl_stop = 0.05 # Example optimal TSL
tp_stop = 0.10 # Example optimal TP (or 0 to disable)
atr_multiple_sl = 2.0 # Example optimal SL multiple

# Use default sizing params
risk_fraction = 0.01 
atr_window_sizing = 14 
# atr_multiple_sizing is now implicitly determined by atr_multiple_sl for target %

# Trading parameters
size_granularity = 0.00001  # Minimum size granularity for crypto

def main():
    # --- Argument Parsing (Adjust sizing args) ---
    parser = argparse.ArgumentParser(description='Backtest EdgeMultiFactorStrategy.')
    parser.add_argument('--symbol', type=str, default=symbol, help='Symbol')
    parser.add_argument('--start_date', type=str, default=start_date, help='Start date')
    parser.add_argument('--end_date', type=str, default=end_date, help='End date')
    parser.add_argument('--granularity', type=str, default=granularity_str, help='Granularity')
    parser.add_argument('--initial_capital', type=float, default=initial_capital, help='Initial capital')
    parser.add_argument('--lookback', type=int, default=lookback_window, help='Factor lookback')
    parser.add_argument('--vol_thresh', type=float, default=volatility_threshold, help='Volatility threshold')
    parser.add_argument('--tsl_stop', type=float, default=tsl_stop, help='Trailing Stop Loss % (0 to disable)')
    parser.add_argument('--tp_stop', type=float, default=tp_stop, help='Take Profit % (0 to disable)')
    parser.add_argument('--atr_multiple_sl', type=float, default=atr_multiple_sl, help='ATR Multiple for SL and Target % calc')
    parser.add_argument('--risk_fraction', type=float, default=risk_fraction, help='Risk fraction for target % sizing')
    parser.add_argument('--atr_window', type=int, default=atr_window_sizing, help='ATR window for sizing/SL')
    # parser.add_argument('--atr_multiple_sizing', type=float, default=atr_multiple_sizing, help='ATR multiple for sizing') # No longer needed directly
    parser.add_argument('--plot', action='store_true', help='Show plots')
    
    args = parser.parse_args()
    
    current_granularity_seconds = GRANULARITY_MAP_SECONDS.get(args.granularity.lower())
    if current_granularity_seconds is None:
        logger.error(f"Invalid granularity: {args.granularity}")
        return
        
    logger.info(f"Backtesting EdgeMultiFactorStrategy with parameters:")
    logger.info(f"  Symbol: {args.symbol}")
    logger.info(f"  Date Range: {args.start_date} to {args.end_date}")
    logger.info(f"  Granularity: {args.granularity}")
    logger.info(f"  Lookback Window: {args.lookback}")
    logger.info(f"  Volatility Threshold: {args.vol_thresh}")
    logger.info(f"  Factor Weights: {optimal_factor_weights}") 
    logger.info(f"  SL ATR Multiple: {args.atr_multiple_sl}")
    logger.info(f"  Trailing Stop Loss: {args.tsl_stop*100:.1f}%")
    logger.info(f"  Take Profit: {args.tp_stop*100:.1f}%")
    logger.info(f"  Position Sizing: TargetPercent (Risk Frac: {args.risk_fraction}, ATR Win: {args.atr_window}, ATR Mult SL: {args.atr_multiple_sl})")

    # Fetch data
    logger.info("Fetching data...")
    price_data = fetch_historical_data(args.symbol, args.start_date, args.end_date, current_granularity_seconds)

    if price_data is None or price_data.empty:
        logger.error("Failed to fetch data")
        return

    logger.info(f"Data fetched successfully. Shape: {price_data.shape}")
    price_data.index = pd.to_datetime(price_data.index, utc=True)

    # Create strategy instance
    strategy = EdgeMultiFactorStrategy(
        lookback_window=args.lookback,
        volatility_threshold=args.vol_thresh,
        initial_capital=args.initial_capital,
        default_factor_weights=optimal_factor_weights,
        commission_pct=0.001,
        slippage_pct=0.0005
    )

    # Generate Signals
    logger.info("Generating signals...")
    long_entries, short_entries, is_trending, is_ranging = strategy.generate_signals(price_data)
    logger.info(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries.")

    if long_entries.sum() + short_entries.sum() == 0:
        logger.warning("No entry signals generated.")
        return

    # Calculate Target Percentage Size
    logger.info("Calculating target percentage size...")
    target_pct = strategy.calculate_target_percent(
        price_data,
        risk_fraction=args.risk_fraction,
        atr_window=args.atr_window,
        atr_multiple_stop=args.atr_multiple_sl # Use SL multiple here
    )

    # Calculate ATR-based SL % for the portfolio call
    atr = vbt.ATR.run(
        price_data['high'], price_data['low'], price_data['close'], 
        window=args.atr_window, wtype='wilder'
    ).atr.bfill().ffill()
    sl_stop_dist = (atr * args.atr_multiple_sl)
    sl_stop_pct = (sl_stop_dist / price_data['close']).replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(0)
    sl_stop_pct = np.clip(sl_stop_pct, 0.001, 0.5)

    # Run Backtest with TargetPercent
    logger.info(f"Running backtest with percentage-based sizing...")
    vbt_freq = get_vbt_freq_str(current_granularity_seconds) or pd.infer_freq(price_data.index)

    # Calculate position sizes as percentage of capital (adapted from target percentage)
    avg_target_pct = target_pct.mean()
    logger.info(f"Using average position size of {avg_target_pct*100:.2f}% of capital")
    
    portfolio = vbt.Portfolio.from_signals(
        price_data,
        entries=long_entries,
        short_entries=short_entries,
        sl_stop=sl_stop_pct,
        tp_stop=args.tp_stop if args.tp_stop > 0 else None,
        tsl_stop=args.tsl_stop if args.tsl_stop > 0 else None,
        size=avg_target_pct,  # Use average percentage for simple % sizing
        size_type='percent',  # Use standard percent sizing
        init_cash=args.initial_capital,
        fees=strategy.commission_pct,
        slippage=strategy.slippage_pct,
        freq=vbt_freq,
        size_granularity=size_granularity,
        stop_exit_type='close',
        accumulate=False,
        save_returns=True
    )

    # Generate Comprehensive Analysis
    logger.info("\n--- Performance Metrics ---")
    stats = portfolio.stats() # Add benchmark later if needed
    logger.info(stats)

    # Save detailed stats and trades
    try:
        stats_df = pd.DataFrame([stats])
        stats_df.to_csv('edge_strategy_backtest_stats.csv')
        logger.info("Stats saved to edge_strategy_backtest_stats.csv")
        trade_analysis = portfolio.trades.stats()
        pd.Series(trade_analysis).to_csv('edge_strategy_backtest_trade_analysis.csv')
        logger.info("Trade analysis saved to edge_strategy_backtest_trade_analysis.csv")
        monthly_returns = portfolio.returns.vbt.returns(freq='M')
        monthly_returns.to_csv('edge_strategy_backtest_monthly_returns.csv')
        logger.info("Monthly returns saved to edge_strategy_backtest_monthly_returns.csv")
    except Exception as save_err:
        logger.error(f"Error saving results: {save_err}")
        
    # Generate and Save/Show Multiple Chart Types
    if args.plot:
        logger.info("Generating plots...")
        try:
            fig = portfolio.plot(settings=dict(bm_returns=False))
            fig.write_image('edge_strategy_backtest_equity.png')
            logger.info("Equity curve saved to edge_strategy_backtest_equity.png")
            fig_dd = portfolio.plot_drawdowns()
            fig_dd.write_image('edge_strategy_backtest_drawdowns.png')
            logger.info("Drawdowns plot saved to edge_strategy_backtest_drawdowns.png")
            fig_underwater = portfolio.plot_underwater()
            fig_underwater.write_image('edge_strategy_backtest_underwater.png')
            logger.info("Underwater plot saved to edge_strategy_backtest_underwater.png")
            fig_trades = portfolio.trades.plot()
            fig_trades.write_image('edge_strategy_backtest_trades.png')
            logger.info("Trades plot saved to edge_strategy_backtest_trades.png")
            windows = [30, 60, 90]
            for window in windows:
                periods = int(window * 24 / (current_granularity_seconds / 3600))
                if periods > 0:
                    fig_metrics = portfolio.plot_rolling_sharpe(window=periods)
                    fig_metrics.write_image(f'edge_strategy_backtest_rolling_{window}d.png')
                    logger.info(f"Rolling metrics for {window} days saved")
                else:
                    logger.warning(f"Skipping rolling plot for {window} days")
            fig.show()
            
        except Exception as plot_err:
            logger.error(f"Error generating plots: {plot_err}")

    logger.info("Backtest completed successfully.")

if __name__ == "__main__":
    main() 