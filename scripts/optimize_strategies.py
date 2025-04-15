import vectorbtpro as vbt
import pandas as pd
import numpy as np
import importlib
import logging
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import argparse

# --- Basic Setup ---
# Add project root to sys.path if needed (adjust path as necessary)
ROOT_DIR = Path(__file__).resolve().parent.parent 
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()] # Add FileHandler later if needed
)
logger = logging.getLogger(__name__)

# Placeholder for data fetching/loading function (reuse existing ones)
# from backtest_stoch_sma_vbt_pro import fetch_historical_data
def fetch_historical_data(symbol, start_date, end_date, granularity):
    # Replace with actual data loading logic (e.g., from cache or API)
    logger.warning("Using placeholder data fetching. Implement actual logic.")
    # Example using a known existing function if path is correct:
    try:
        from scripts.backtest_stoch_sma_vbt_pro import fetch_historical_data as fetch_actual
        return fetch_actual(symbol, start_date, end_date, granularity)
    except ImportError:
         logger.error("Could not import fetch_historical_data. Falling back to sample.")
         from scripts.backtest_stoch_sma_vbt_pro import create_sample_data # Assuming this exists
         return create_sample_data(start_date, end_date)
    except Exception as e:
        logger.error(f"Error during actual data fetch: {e}")
        from scripts.backtest_stoch_sma_vbt_pro import create_sample_data # Assuming this exists
        return create_sample_data(start_date, end_date)

# --- Strategy Configuration ---
# Define strategies to test and their parameters
# Keys: 'module_path', 'class_name', 'param_grid'
# param_grid values should be arrays/lists/ranges for vectorbtpro optimization
STRATEGY_CONFIG = {
    "StochSMA": {
        "module_path": "scripts.backtest_stoch_sma_vbt_pro", # Assumes refactoring
        "class_name": "StochSMAStrategy", # Assumes refactoring
        "param_grid": {
            'stoch_k': np.arange(5, 26, 10), # Example: [5, 15, 25]
            'stoch_d': np.arange(3, 8, 2), # Example: [3, 5, 7]
            'stoch_lower_th': np.arange(20, 31, 10), # Example: [20, 30]
            'stoch_upper_th': np.arange(70, 81, 10), # Example: [70, 80]
            # --- Non-Optimized Params (passed to __init__) ---
            'trend_filter_window': 200, 
            'use_stops': True,
            'sl_atr_multiplier': 2.0,
            'tsl_atr_multiplier': 3.0,
        }
    },
    "RSIMomentum": {
         "module_path": "scripts.backtest_rsi_vbt",
         "class_name": "RSIMomentumVBT", # Needs refactoring for optimization
         "param_grid": {
             'window': np.arange(10, 21, 5),      # Example: [10, 15, 20]
             'lower_threshold': np.arange(20, 36, 5), # Example: [20, 25, 30, 35]
             'upper_threshold': np.arange(65, 81, 5), # Example: [65, 70, 75, 80]
             # --- Non-Optimized Params (passed to __init__) ---
             'ma_window': 50, 
             # Add other fixed params needed by RSIMomentumVBT.__init__
         }
    },
    # Add more strategies here...
    # "EnhancedRSI": { ... } 
}

# --- Main Optimizer Class ---
class StrategyOptimizer:
    def __init__(self, config, symbol, start_date, end_date, granularity, 
                 initial_capital, commission, slippage, optimize_metric):
        self.config = config
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.granularity = granularity
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.optimize_metric = optimize_metric
        self.results = {}
        self.price_data = None

    def _load_data(self):
        logger.info(f"Loading data for {self.symbol} from {self.start_date} to {self.end_date} ({self.granularity}s granularity)")
        # Assuming fetch_historical_data is available and works
        self.price_data = fetch_historical_data(
            self.symbol, self.start_date, self.end_date, self.granularity
        )
        if self.price_data is None or self.price_data.empty:
            raise ValueError("Failed to load price data.")
        logger.info(f"Data loaded successfully. Shape: {self.price_data.shape}")

    def _import_strategy_class(self, module_path, class_name):
        try:
            module = importlib.import_module(module_path)
            StrategyClass = getattr(module, class_name)
            return StrategyClass
        except ImportError:
            logger.error(f"Failed to import module: {module_path}")
            raise
        except AttributeError:
            logger.error(f"Failed to find class '{class_name}' in module '{module_path}'")
            raise
        except Exception as e:
            logger.error(f"Error importing {class_name} from {module_path}: {e}")
            raise

    def run_optimizations(self):
        self._load_data()
        
        for name, cfg in self.config.items():
            logger.info(f"--- Optimizing Strategy: {name} ---")
            try:
                StrategyClass = self._import_strategy_class(cfg['module_path'], cfg['class_name'])
                
                # Separate optimized params from fixed init params
                param_grid = cfg['param_grid']
                init_params = {k: v for k, v in param_grid.items() if not isinstance(v, (np.ndarray, list, range))}
                optimize_params = {k: v for k, v in param_grid.items() if isinstance(v, (np.ndarray, list, range))}

                # Add global portfolio settings to init_params if needed by constructor
                init_params['initial_capital'] = self.initial_capital
                init_params['commission_pct'] = self.commission # Adjust name if needed
                init_params['slippage_pct'] = self.slippage   # Adjust name if needed

                logger.info(f"Instantiating {cfg['class_name']} with fixed params: {init_params}")
                strategy_instance = StrategyClass(**init_params)

                # Check if strategy instance has the required 'optimize' method
                if not hasattr(strategy_instance, 'optimize') or not callable(getattr(strategy_instance, 'optimize')):
                    logger.error(f"Strategy class {cfg['class_name']} does not have a required 'optimize' method.")
                    self.results[name] = {"error": "Missing 'optimize' method"}
                    continue

                logger.info(f"Running optimization with param grid: {optimize_params}")
                # The optimize method should handle the vbt internal optimization
                # It needs to accept data and the optimization parameter grid
                optimization_results = strategy_instance.optimize(
                    data=self.price_data, 
                    param_grid=optimize_params, 
                    optimize_metric=self.optimize_metric 
                    # Pass other portfolio settings if optimize method needs them
                )
                
                if optimization_results is None:
                     logger.warning(f"Optimization for {name} returned None.")
                     self.results[name] = {"error": "Optimization returned None"}
                else:
                     # Store results (e.g., performance summary or best params)
                     # This depends on what the 'optimize' method returns
                     logger.info(f"Optimization for {name} completed.")
                     # Example: Storing the raw result object for later analysis
                     self.results[name] = optimization_results 

            except Exception as e:
                logger.error(f"Error optimizing strategy {name}: {e}", exc_info=True)
                self.results[name] = {"error": str(e)}
            logger.info(f"--- Finished Strategy: {name} ---\
")
            
    def report_results(self, save_summary=True, summary_filename="reports/optimization_summary.csv"):
        logger.info("\n--- Generating Optimization Summary Report --- ")
        
        summary_data = []
        overall_best_strategy = None
        # Initialize best score based on metric direction (lower is better for drawdown)
        lower_is_better = 'drawdown' in self.optimize_metric.lower()
        overall_best_score = np.inf if lower_is_better else -np.inf
        overall_best_params = None
        
        report_path = Path(os.path.dirname(summary_filename))
        report_path.mkdir(parents=True, exist_ok=True)

        for name, result in self.results.items():
            logger.info(f"\nStrategy: {name}")
            if isinstance(result, dict) and 'error' in result:
                logger.error(f"  Optimization Error: {result['error']}")
                summary_data.append({
                    'strategy': name, 
                    'error': result['error']
                 })
                continue
            
            # Check if result is None before proceeding
            if result is None:
                logger.warning(f"  Result object is None for strategy {name}.")
                summary_data.append({
                    'strategy': name, 
                    'error': "Invalid/missing result object"
                })
                continue

            try:
                # --- Debugging Portfolio Object --- 
                logger.debug(f"  Processing result for {name}. Type: {type(result)}")
                
                # --- Try accessing stats and metric directly --- 
                try:
                    # Get stats per parameter combination (index=metrics, columns=parameters)
                    portfolio_stats_by_param = result.stats(agg_func=None) 
                except AttributeError:
                    logger.error(f"  Result object for {name} does not have a callable .stats() method.")
                    summary_data.append({'strategy': name, 'error': "Missing or non-callable .stats() method"})
                    continue
                except Exception as stats_err:
                    logger.error(f"  Error calling .stats() for {name}: {stats_err}", exc_info=True)
                    summary_data.append({'strategy': name, 'error': f"Error calling stats(): {stats_err}"})
                    continue

                if portfolio_stats_by_param is None or portfolio_stats_by_param.empty:
                    logger.warning(f"  Portfolio stats are empty or None for {name}.")
                    summary_data.append({'strategy': name, 'error': "Empty portfolio stats"})
                    continue
                    
                # --- DO NOT Transpose --- 
                # portfolio_stats = portfolio_stats_by_param.T
                # logger.debug(f" Transposed stats shape: {portfolio_stats.shape}, Index: {portfolio_stats.index.names}, Columns: {portfolio_stats.columns}")
                # available_metrics_cols = portfolio_stats.columns.tolist()
                # logger.debug(f" Available metrics in stats columns: {available_metrics_cols}")
 
                # Check if the optimize_metric exists in the stats index
                available_metrics = portfolio_stats_by_param.index.tolist()
                logger.debug(f" Available metrics in stats index: {available_metrics}")
                if self.optimize_metric not in available_metrics:
                    logger.error(f"  Metric '{self.optimize_metric}' not found in available stats index: {available_metrics}.")
                    summary_data.append({'strategy': name, 'error': f"Metric '{self.optimize_metric}' not found in stats"})
                    continue
                     
                # Get the performance series (row) for the specific metric
                perf_series = portfolio_stats_by_param.loc[self.optimize_metric]
 
                # Find the best column index (parameter tuple) based on the metric direction
                if not isinstance(perf_series, pd.Series):
                    logger.error(f"  Performance data for metric '{self.optimize_metric}' is not a Series (type: {type(perf_series)}). Cannot find best.")
                    summary_data.append({'strategy': name, 'error': f"Metric '{self.optimize_metric}' is not a Series"})
                    continue
                if perf_series.isna().all():
                    logger.warning(f"  Performance series for metric '{self.optimize_metric}' contains only NaNs.")
                    summary_data.append({'strategy': name, 'error': f"Metric '{self.optimize_metric}' is all NaN"})
                    continue
 
                best_col_idx = perf_series.idxmax() if not lower_is_better else perf_series.idxmin()
                 
                if best_col_idx is None:
                    logger.warning(f"  Could not determine best column index for metric '{self.optimize_metric}'.")
                    summary_data.append({'strategy': name, 'error': f"Could not find best index for {self.optimize_metric}"})
                    continue
 
                # Get stats column and params for the single best run
                best_perf_stats_col = portfolio_stats_by_param[best_col_idx] # Get stats Series for the best run using column index
                score = best_perf_stats_col[self.optimize_metric] # Score is the value in the metric's row for the best column
 
                # Reconstruct params from the best column index (which is the parameter tuple)
                best_params = None
                best_params_str = f"Index: {best_col_idx}" # Default if reconstruction fails
                
                # Get parameter names from the columns MultiIndex levels
                if isinstance(portfolio_stats_by_param.columns, pd.MultiIndex):
                    optimize_params_names = portfolio_stats_by_param.columns.names # Get names from columns
                    if isinstance(best_col_idx, tuple) and len(best_col_idx) == len(optimize_params_names):
                         best_params = dict(zip(optimize_params_names, best_col_idx))
                         best_params_str = json.dumps(best_params)
                    else:
                         logger.warning(f"  Could not reconstruct params dictionary from column index {best_col_idx} and param names {optimize_params_names}.")
                else:
                     logger.warning("  Could not reconstruct params: Columns are not a MultiIndex.")
 
                logger.info(f"  Best Score ({self.optimize_metric}): {score:.4f}")
                logger.info(f"  Best Params: {best_params_str}")
                # Extract other metrics using the metric name index from the best stats column
                total_return = best_perf_stats_col.get('Total Return [%]', np.nan)
                max_dd = best_perf_stats_col.get('Max Drawdown [%]', np.nan)
                win_rate = best_perf_stats_col.get('Win Rate [%]', np.nan)
                num_trades = best_perf_stats_col.get('Total Trades', 0)
                logger.info(f"  Total Return: {total_return:.2f}% | Max Drawdown: {max_dd:.2f}% | Win Rate: {win_rate:.2f}% | Trades: {num_trades}")
                
                summary_data.append({
                    'strategy': name,
                    'best_score': score,
                    'metric': self.optimize_metric,
                    'total_return_pct': total_return,
                    'max_drawdown_pct': max_dd,
                    'win_rate_pct': win_rate,
                    'num_trades': num_trades,
                    'best_params': best_params_str,
                    'error': None
                })
                
                # Update overall best
                is_better = (score < overall_best_score) if lower_is_better else (score > overall_best_score)

                if overall_best_strategy is None or is_better:
                     overall_best_strategy = name
                     overall_best_score = score
                     overall_best_params = best_params # Store the dict

            except Exception as e:
                logger.error(f"  Error processing results for {name}: {e}", exc_info=True)
                summary_data.append({
                    'strategy': name, 
                    'error': f"Reporting error: {e}"
                 })

        logger.info("\n--- Overall Best --- ")
        if overall_best_strategy:
            logger.info(f"Best Performing Strategy: {overall_best_strategy}")
            logger.info(f"Best Score ({self.optimize_metric}): {overall_best_score:.4f}")
            logger.info(f"Best Parameters: {overall_best_params}")
        else:
            logger.info("No successful optimizations found to determine overall best.")
            
        # Save summary DataFrame to CSV
        if save_summary and summary_data:
            try:
                summary_df = pd.DataFrame(summary_data)
                # Define column order for clarity
                cols = ['strategy', 'metric', 'best_score', 'total_return_pct', 'max_drawdown_pct', 'win_rate_pct', 'num_trades', 'best_params', 'error']
                # Reorder and add missing columns if necessary
                summary_df = summary_df.reindex(columns=cols)
                summary_df.sort_values(by='best_score', ascending=lower_is_better, inplace=True)
                summary_df.to_csv(summary_filename, index=False)
                logger.info(f"\nSaved optimization summary to: {summary_filename}")
            except Exception as e:
                 logger.error(f"Failed to save summary file '{summary_filename}': {e}")
        elif not summary_data:
            logger.warning("No summary data generated to save.")

# --- Granularity Mapping ---
GRANULARITY_MAP_SECONDS = {
    '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
    '1h': 3600, '2h': 7200, '4h': 14400, '6h': 21600, '1d': 86400
}

# --- Command Line Interface ---
def main():
    parser = argparse.ArgumentParser(description="Run multi-strategy vectorbtpro optimization.")
    parser.add_argument("--symbol", type=str, default="BTC-USD", help="Trading symbol (e.g., BTC-USD)")
    parser.add_argument("--start_date", type=str, default="2022-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, default=datetime.now().strftime('%Y-%m-%d'), help="End date (YYYY-MM-DD)")
    parser.add_argument("--granularity", type=str, nargs='+', default=['1d'], 
                        help="List of granularities to test (e.g., 1d 4h 1h)", 
                        choices=GRANULARITY_MAP_SECONDS.keys())
    parser.add_argument("--capital", type=float, default=10000, help="Initial capital")
    parser.add_argument("--commission", type=float, default=0.001, help="Commission per trade (e.g., 0.001 for 0.1%)")
    parser.add_argument("--slippage", type=float, default=0.0005, help="Slippage per trade (e.g., 0.0005 for 0.05%)")
    parser.add_argument("--metric", type=str, default="sharpe_ratio", help="Metric to optimize for (e.g., 'sharpe_ratio', 'total_return')") # Use vbt metric names

    args = parser.parse_args()
    
    all_results_across_timeframes = [] # Store results from all timeframes

    for gran_str in args.granularity:
        granularity_seconds = GRANULARITY_MAP_SECONDS.get(gran_str.lower())
        if granularity_seconds is None:
             logger.error(f"Invalid granularity string provided: {gran_str}. Skipping.")
             continue
             
        logger.info(f"\n===== Starting Optimization for Granularity: {gran_str} ({granularity_seconds}s) =====")

        optimizer = StrategyOptimizer(
            config=STRATEGY_CONFIG,
            symbol=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date,
            granularity=granularity_seconds,
            initial_capital=args.capital,
            commission=args.commission,
            slippage=args.slippage,
            optimize_metric=args.metric
        )

        optimizer.run_optimizations()
        
        # Modify report filename to include granularity
        summary_filename = f"reports/optimization_summary_{gran_str}.csv"
        optimizer.report_results(save_summary=True, summary_filename=summary_filename)
        
        # Optional: Store results if needed for a final combined report later
        # all_results_across_timeframes.append({'granularity': gran_str, 'results': optimizer.results})
        
    logger.info("\n===== All Timeframe Optimizations Complete =====")
    # Optional: Add code here to process `all_results_across_timeframes` for a combined report

if __name__ == "__main__":
    # Example Usage:
    # python scripts/optimize_strategies.py --symbol ETH-USD --start_date 2021-01-01 --granularity 3600 --metric "Total Return [%]"
    main() 