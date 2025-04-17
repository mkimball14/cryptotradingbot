import sys
import os
from pathlib import Path
import vectorbtpro as vbt
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import argparse

# --- Basic Setup ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Import Strategy and Data Fetcher ---
try:
    # Use the refactored strategy class
    from scripts.strategies.edge_multi_factor import EdgeMultiFactorStrategy
    logger.info("Successfully imported EdgeMultiFactorStrategy.")
except ImportError as e:
    logger.error(f"Could not import EdgeMultiFactorStrategy: {e}")
    sys.exit(1)

try:
    from data.data_fetcher import fetch_historical_data, get_granularity_str, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    logger.info("Using data_fetcher from data module.")
except ImportError:
    try:
        from scripts.backtest_stoch_sma_vbt_pro import fetch_historical_data, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
        logger.info("Using functions from scripts.backtest_stoch_sma_vbt_pro.")
    except ImportError as e:
        logger.error(f"Could not import data fetching functions: {e}")
        sys.exit(1)

# --- Optimization Configuration ---
# Define the parameter grid for optimization
OPTIMIZATION_PARAM_GRID = {
    'lookback_window': [15, 20, 25, 30],
    'volatility_threshold': [0.3, 0.4, 0.5, 0.6, 0.7],
    'tsl_stop': [0.03, 0.05, 0.07, 0.10, 0.12], # Keep TSL
    'tp_stop': [0.05, 0.10, 0.15, 0.20], # Added Take Profit % 
    'atr_multiple_sl': [1.5, 2.0, 2.5, 3.0], # Added ATR multiple for SL
    'factor_weights': 'auto'
}
OPTIMIZATION_METRIC = 'sharpe_ratio'
WEIGHT_OPT_STEPS = 3

# --- Main Optimization Function ---
def run_optimization(args):
    logger.info(f"Starting optimization for {args.symbol}...")
    logger.info(f"Date Range: {args.start_date} to {args.end_date}")
    logger.info(f"Granularity: {args.granularity}")
    logger.info(f"Optimization Metric: {OPTIMIZATION_METRIC}")
    logger.info(f"Parameter Grid: {OPTIMIZATION_PARAM_GRID}")
    logger.info(f"Weight Optimization Steps: {WEIGHT_OPT_STEPS}")

    # --- Data Fetching ---
    granularity_seconds = GRANULARITY_MAP_SECONDS.get(args.granularity.lower())
    if granularity_seconds is None:
        logger.error(f"Error: Unsupported granularity: {args.granularity}.")
        sys.exit(1)

    logger.info("Fetching data...")
    price_data = fetch_historical_data(args.symbol, args.start_date, args.end_date, granularity_seconds)

    if price_data is None or price_data.empty:
        logger.error("Failed to fetch data. Exiting.")
        sys.exit(1)
        
    logger.info(f"Data fetched successfully. Shape: {price_data.shape}")
    price_data.index = pd.to_datetime(price_data.index, utc=True)

    # --- Strategy Initialization ---
    strategy = EdgeMultiFactorStrategy(
        initial_capital=args.initial_capital,
        commission_pct=args.commission,
        slippage_pct=args.slippage
    )

    # --- Run Optimization ---
    logger.info("Running optimization...")
    best_params = strategy.optimize(
        data=price_data,
        param_grid=OPTIMIZATION_PARAM_GRID,
        optimize_metric=OPTIMIZATION_METRIC,
        weight_opt_steps=WEIGHT_OPT_STEPS,
        risk_fraction=args.risk_fraction,
        atr_window=args.atr_window,
        atr_multiple=args.atr_multiple,
        verbose=True
    )

    # --- Results ---
    if best_params:
        logger.info("\n--- Optimization Complete ---")
        logger.info(f"Best parameters found for {OPTIMIZATION_METRIC}: ")
        for key, value in best_params.items():
            if isinstance(value, float):
                logger.info(f"  {key}: {value:.4f}")
            elif isinstance(value, dict):
                 logger.info(f"  {key}:")
                 for sub_key, sub_value in value.items():
                      logger.info(f"    {sub_key}: {sub_value:.4f}")
            else:
                logger.info(f"  {key}: {value}")
        
        # Optionally save best params to a file
        try:
            pd.Series(best_params).to_json('best_edge_params.json', indent=4)
            logger.info("Best parameters saved to best_edge_params.json")
        except Exception as e:
            logger.error(f"Error saving parameters: {e}")
            
    else:
        logger.warning("Optimization did not find any suitable parameters.")

    logger.info("Optimization script finished.")

# --- Main Execution Block ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Optimize EdgeMultiFactorStrategy Parameters.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to optimize on')
    parser.add_argument('--start_date', type=str, default='2022-01-01', help='Start date for optimization data (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date for optimization data (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1h', help='Data granularity (e.g., 1h, 4h, 1d)')
    parser.add_argument('--initial_capital', type=float, default=3000, help='Initial capital for backtests during optimization')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--risk_fraction', type=float, default=0.01, help='Fixed risk fraction for sizing')
    parser.add_argument('--atr_window', type=int, default=14, help='Fixed ATR window for sizing')
    parser.add_argument('--atr_multiple', type=float, default=2.0, help='Fixed ATR multiple for sizing')

    args = parser.parse_args()

    run_optimization(args) 