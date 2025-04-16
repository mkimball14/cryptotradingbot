import vectorbtpro as vbt
import pandas as pd
import numpy as np
import importlib
import logging
import sys
import os
import json
import signal
from pathlib import Path
from datetime import datetime
import argparse
from contextlib import contextmanager
import time

# Define a timeout context manager to prevent hanging
class TimeoutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    """
    Context manager that raises a TimeoutException if execution takes longer than specified seconds.
    Only works on Unix systems due to signal usage.
    """
    def signal_handler(signum, frame):
        raise TimeoutException(f"Timed out after {seconds} seconds")
    
    # Register the signal function handler
    try:
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        yield
    finally:
        # Unregister by setting alarm to 0
        signal.alarm(0)

# Helper function to convert numpy types to native Python types for JSON serialization
def convert_numpy_types(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(i) for i in obj]
    return obj

# --- Basic Setup ---
# Add project root to sys.path if needed (adjust path as necessary)
ROOT_DIR = Path(__file__).resolve().parent.parent 
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# --- Import centralized data fetcher ---
from data.data_fetcher import fetch_historical_data, get_granularity_str, get_vbt_freq_str, GRANULARITY_MAP_SECONDS

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()] # Add FileHandler later if needed
)
logger = logging.getLogger(__name__)

# Placeholder for data fetching/loading function (reuse existing ones)
# from backtest_stoch_sma_vbt_pro import fetch_historical_data
# def fetch_historical_data(symbol, start_date, end_date, granularity):
#     # Replace with actual data loading logic (e.g., from cache or API)
#     logger.warning("Using placeholder data fetching. Implement actual logic.")
#     # Example using a known existing function if path is correct:
#     try:
#         from scripts.backtest_stoch_sma_vbt_pro import fetch_historical_data as fetch_actual
#         return fetch_actual(symbol, start_date, end_date, granularity)
#     except ImportError:
#          logger.error("Could not import fetch_historical_data. Falling back to sample.")
#          from scripts.backtest_stoch_sma_vbt_pro import create_sample_data # Assuming this exists
#          return create_sample_data(start_date, end_date)
#     except Exception as e:
#         logger.error(f"Error during actual data fetch: {e}")
#         from scripts.backtest_stoch_sma_vbt_pro import create_sample_data # Assuming this exists
#         return create_sample_data(start_date, end_date)

# --- Strategy Configuration ---
# Define strategies to test and their parameters
# Keys: 'module_path', 'class_name', 'param_grid'
# param_grid values should be arrays/lists/ranges for vectorbtpro optimization
STRATEGY_CONFIG = {
    "StochSMA": {
        "module_path": "scripts.backtest_stoch_sma_vbt_pro", 
        "class_name": "StochSMAStrategy", 
        "param_grid": {
            # Finer grid around best found params (k=5, d=3, lower=30, upper=70)
            'stoch_k': np.arange(3, 8, 1), # [3, 4, 5, 6, 7]
            'stoch_d': np.arange(1, 6, 1), # [1, 2, 3, 4, 5]
            'stoch_lower_th': np.arange(25, 36, 5), # [25, 30, 35]
            'stoch_upper_th': np.arange(65, 76, 5), # [65, 70, 75]
            # --- Non-Optimized Params (passed to __init__) ---
            'trend_filter_window': 200, 
            'use_stops': True,
            'sl_atr_multiplier': 2.0, 
            'tsl_atr_multiplier': 3.0, 
        }
    },
    # --- Other strategies commented out for focused run ---
    # "RSIMomentum": { ... },
    # "MACrossover": { ... },
    # "RsiBB": { ... },
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
        # Now using the imported version from data.data_fetcher
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
            strategy_instance = None # Initialize
            optimization_results = None # Initialize
            try:
                logger.debug(f"Importing strategy {cfg['class_name']} from {cfg['module_path']}")
                StrategyClass = self._import_strategy_class(cfg['module_path'], cfg['class_name'])
                
                # Separate optimized params from fixed init params
                param_grid = cfg['param_grid']
                init_params = {k: v for k, v in param_grid.items() if not isinstance(v, (np.ndarray, list, range))}
                optimize_params = {k: v for k, v in param_grid.items() if isinstance(v, (np.ndarray, list, range))}

                # Add global portfolio settings to init_params if needed by constructor
                # Ensure keys match expected names in strategy __init__ methods
                init_params['initial_capital'] = self.initial_capital
                init_params['commission_pct'] = self.commission # Adjust name if needed
                init_params['slippage_pct'] = self.slippage   # Adjust name if needed

                logger.info(f"Instantiating {cfg['class_name']} with fixed params: {init_params}")
                strategy_instance = StrategyClass(**init_params)

                # Check if strategy instance has the required 'optimize' method
                if not hasattr(strategy_instance, 'optimize') or not callable(getattr(strategy_instance, 'optimize')):
                    logger.error(f"Strategy class {cfg['class_name']} does not have a required callable 'optimize' method.")
                    self.results[name] = {"error": "Missing or non-callable 'optimize' method"}
                    continue # Skip to next strategy

                logger.info(f"Running optimization with param grid: {optimize_params}")
                logger.debug(f"Calling {name}.optimize() method...")
                
                # Add extra logging for RsiBB specifically
                if name == "RsiBB":
                    logger.info(f"Extra debugging for RsiBB strategy")
                    logger.info(f"Data shape: {self.price_data.shape}")
                    logger.info(f"Data columns: {self.price_data.columns}")
                    logger.info(f"Data index range: {self.price_data.index[0]} to {self.price_data.index[-1]}")
                    
                # The optimize method should handle the vbt internal optimization
                # Add a timeout for RsiBB strategy
                if name == "RsiBB":
                    logger.info(f"Setting 60-second timeout for RsiBB optimization")
                    try:
                        with time_limit(60):  # 60 seconds timeout
                            optimization_results = strategy_instance.optimize(
                                data=self.price_data.copy(),
                                param_grid=optimize_params,
                                optimize_metric=self.optimize_metric
                            )
                    except TimeoutException as te:
                        logger.error(f"RsiBB optimization timed out: {te}")
                        self.results[name] = {"error": f"Optimization timed out after 60 seconds"}
                        continue  # Skip to next strategy
                    except Exception as e:
                        logger.error(f"RsiBB optimization error: {e}", exc_info=True)
                        self.results[name] = {"error": f"Optimization error: {e}"}
                        continue  # Skip to next strategy
                else:
                    # For other strategies, no timeout
                    optimization_results = strategy_instance.optimize(
                        data=self.price_data.copy(),
                        param_grid=optimize_params, 
                        optimize_metric=self.optimize_metric
                    )
                
                logger.debug(f"{name}.optimize() method finished.")
                
                if name == "RsiBB":
                    logger.info(f"RsiBB optimization completed with result type: {type(optimization_results)}")
                    if optimization_results is not None:
                        if hasattr(optimization_results, 'shape'):
                            logger.info(f"RsiBB result shape: {optimization_results.shape}")
                
                if optimization_results is None:
                     logger.warning(f"Optimization for {name} returned None.")
                     self.results[name] = {"error": "Optimization returned None"}
                else:
                     logger.info(f"Optimization for {name} completed successfully.")
                     # Store results (e.g., performance summary or best params)
                     # This depends on what the 'optimize' method returns
                     self.results[name] = optimization_results # Store the Portfolio object

            except ImportError as e:
                logger.error(f"ImportError for strategy {name}: {e}", exc_info=True)
                self.results[name] = {"error": f"ImportError: {e}"}
            except AttributeError as e:
                 logger.error(f"AttributeError during setup/run for strategy {name}: {e}", exc_info=True)
                 self.results[name] = {"error": f"AttributeError: {e}"}
            except TypeError as e:
                 logger.error(f"TypeError during setup/run for strategy {name} (check __init__ params?): {e}", exc_info=True)
                 self.results[name] = {"error": f"TypeError: {e}"}
            except Exception as e:
                # Catch any other exceptions during the process for this strategy
                logger.error(f"Unhandled exception optimizing strategy {name}: {e}", exc_info=True)
                self.results[name] = {"error": f"Unhandled Exception: {e}"}
            
            logger.info(f"--- Finished Strategy: {name} ---") # Moved slightly for clarity
            
    def report_results(self, save_summary=True, summary_filename="reports/optimization_summary.csv"):
        logger.info("\n--- Generating Optimization Summary Report --- ")
        
        summary_data = []
        overall_best_strategy = None
        lower_is_better = 'drawdown' in self.optimize_metric.lower() # Check if metric implies lower is better
        overall_best_score = np.inf if lower_is_better else -np.inf
        overall_best_params = None
        
        report_path = Path(os.path.dirname(summary_filename))
        report_path.mkdir(parents=True, exist_ok=True)

        for name, result in self.results.items():
            logger.info(f"\nStrategy: {name}")
            
            # Add extra debugging for RsiBB reporting
            if name == "RsiBB":
                logger.info(f"RsiBB result type in reporting: {type(result)}")
                if isinstance(result, dict) and 'error' in result:
                    logger.info(f"RsiBB has error: {result['error']}")
                
            if isinstance(result, dict) and 'error' in result:
                logger.error(f"  Optimization Error: {result['error']}")
                summary_data.append({
                    'strategy': name, 
                    'error': result['error']
                 })
                continue
            
            if result is None:
                logger.warning(f"  Result object is None for strategy {name}.")
                summary_data.append({
                    'strategy': name, 
                    'error': "Invalid/missing result object"
                })
                continue

            try:
                logger.debug(f"  Processing result for {name}. Type: {type(result)}")
                
                # --- Get stats per parameter combination ---
                # The result should be a Portfolio object
                try:
                    # Use per_column=True to get params in COLUMNS, metrics in INDEX
                    
                    # Add timeout protection for stats calculation
                    if name == "RsiBB":
                        logger.info(f"About to call stats() for RsiBB")
                        try:
                            with time_limit(120):  # Increased timeout for RsiBB
                                # Calculate only specific metrics for RsiBB instead of the full stats
                                # This is much faster than calculating all metrics
                                try:
                                    # Try to calculate just the essential metrics using specific methods
                                    logger.info("Calculating specific metrics for RsiBB instead of full stats")
                                    
                                    # Get returns directly from the portfolio - check if it's callable or an attribute
                                    if callable(getattr(result, 'returns', None)):
                                        returns = result.returns(cache=False)
                                    else:
                                        returns = getattr(result, 'returns', None)
                                        if returns is None:
                                            logger.warning("RsiBB result has no 'returns' attribute")
                                    
                                    # Check if methods are callable before using them
                                    if callable(getattr(result, 'total_return', None)):
                                        total_return = result.total_return(cache=False) * 100  # as percentage
                                    else:
                                        logger.warning("total_return method not callable in RsiBB result")
                                        total_return = 0
                                    
                                    if callable(getattr(result, 'max_drawdown', None)):
                                        max_dd = result.max_drawdown(cache=False) * 100  # as percentage
                                    else:
                                        logger.warning("max_drawdown method not callable in RsiBB result")
                                        max_dd = 0
                                    
                                    if callable(getattr(result, 'sharpe_ratio', None)):
                                        sharpe = result.sharpe_ratio(cache=False)
                                    else:
                                        logger.warning("sharpe_ratio method not callable in RsiBB result")
                                        sharpe = 0
                                    
                                    if callable(getattr(result, 'sortino_ratio', None)):
                                        sortino = result.sortino_ratio(cache=False)
                                    else:
                                        logger.warning("sortino_ratio method not callable in RsiBB result")
                                        sortino = 0
                                    
                                    trades_df = getattr(result, 'trades', None)
                                    total_trades = len(trades_df) if trades_df is not None else 0
                                    
                                    if callable(getattr(result, 'win_rate', None)) and total_trades > 0:
                                        win_rate = result.win_rate(cache=False) * 100
                                    else:
                                        if total_trades == 0:
                                            logger.warning("No trades found for RsiBB")
                                        else:
                                            logger.warning("win_rate method not callable in RsiBB result")
                                        win_rate = 0
                                    
                                    # Create a custom stats DataFrame with these metrics
                                    metrics = [
                                        'Total Return [%]',
                                        'Max Drawdown [%]',
                                        'Win Rate [%]',
                                        'Total Trades',
                                        'Sharpe Ratio',
                                        'Sortino Ratio'
                                    ]
                                    
                                    values = [
                                        total_return,
                                        max_dd,
                                        win_rate,
                                        total_trades,
                                        sharpe,
                                        sortino
                                    ]
                                    
                                    # Create a custom Portfolio stats as a DataFrame with params as columns
                                    # --- Get params and names AFTER stats calculation ---
                                    # This relies on the portfolio_stats DataFrame being successfully calculated (either custom or fallback)
                                    params = None
                                    param_names = None
                                    if isinstance(portfolio_stats.columns, pd.MultiIndex):
                                        params = portfolio_stats.columns.tolist() # Get param tuples from columns
                                        param_names = portfolio_stats.columns.names # Get names from columns
                                    elif isinstance(portfolio_stats.columns, pd.Index):
                                        # Handle single parameter case
                                        params = portfolio_stats.columns.tolist()
                                        param_names = [portfolio_stats.columns.name] if portfolio_stats.columns.name else ['param_0']
                                    else:
                                        logger.error(f"Could not extract parameters from portfolio_stats columns (type: {type(portfolio_stats.columns)}) for RsiBB")
                                        raise ValueError("Failed to extract parameters from stats columns")

                                    # Rebuild the DataFrame using extracted params/names and calculated values
                                    portfolio_stats = pd.DataFrame(
                                        index=metrics,
                                        columns=pd.MultiIndex.from_tuples(params, names=param_names)
                                    )
                                    
                                    # Fill in values for each parameter combination
                                    for i, col_tuple in enumerate(params):
                                        # Correctly handle single vs multi-param indexing
                                        col_key = col_tuple[0] if len(param_names) == 1 else col_tuple
                                        for j, metric_name in enumerate(metrics):
                                            # Ensure values[j] is indexed correctly if it's an array
                                            value_to_assign = values[j] if not isinstance(values[j], (np.ndarray, pd.Series)) else values[j][i]
                                            portfolio_stats.loc[metric_name, col_key] = value_to_assign
                                    
                                    logger.info("Custom stats calculation for RsiBB completed successfully")
                                except Exception as custom_err:
                                    logger.error(f"Custom stats calculation for RsiBB failed: {custom_err}")
                                    # Fall back to regular stats if custom calculation fails
                                    portfolio_stats = result.stats(per_column=True)
                            
                            logger.info(f"RsiBB stats call completed successfully")
                        except TimeoutException as te:
                            logger.error(f"RsiBB stats calculation timed out: {te}")
                            summary_data.append({
                                'strategy': name, 
                                'error': f"Stats calculation timed out after 120 seconds"
                            })
                            continue
                    else:
                        try:
                            portfolio_stats = result.stats(per_column=True)
                        except Exception as stats_err:
                            logger.error(f"Error calling .stats() for {name}: {stats_err}", exc_info=True)
                            summary_data.append({'strategy': name, 'error': f"Error calling stats(): {stats_err}"})
                            continue
                        
                    logger.debug(f"  portfolio_stats type: {type(portfolio_stats)}, shape: {getattr(portfolio_stats, 'shape', None)}")
                except AttributeError:
                    logger.error(f"  Result object for {name} does not have a callable .stats() method.")
                    summary_data.append({'strategy': name, 'error': "Missing or non-callable .stats() method"})
                    continue
                except Exception as stats_err:
                    logger.error(f"Error in RsiBB stats calculation: {stats_err}", exc_info=True)
                    summary_data.append({
                        'strategy': name, 
                        'error': f"Stats calculation error: {stats_err}"
                    })
                    continue
                
                # --- Check if stats DataFrame is valid ---
                if not isinstance(portfolio_stats, pd.DataFrame):
                    logger.error(f"  portfolio_stats is not a DataFrame (type: {type(portfolio_stats)}). Skipping strategy {name}.")
                    summary_data.append({'strategy': name, 'error': "Portfolio stats is not a DataFrame. Check strategy output."})
                    continue

                if portfolio_stats.empty:
                    logger.warning(f"  Portfolio stats are empty for {name}.")
                    summary_data.append({'strategy': name, 'error': "Empty portfolio stats"})
                    continue
                
                # Corrected: Index = Metrics, Columns = Parameter Tuples
                logger.debug(f" Stats index (metrics): {portfolio_stats.index.tolist()[:20]}...") # Log metrics index
                logger.debug(f" Stats columns (params): {portfolio_stats.columns.names} {portfolio_stats.columns.tolist()[:5]}...") # Log params columns

                # -- Determine the actual key for the desired metric in the INDEX --
                metric_key_actual = None
                available_metrics_idx = portfolio_stats.index.tolist() # Check INDEX now
                
                # Exact match first
                if self.optimize_metric in available_metrics_idx:
                    metric_key_actual = self.optimize_metric
                else:
                    # Try common variations
                    variations_to_try = [
                        self.optimize_metric.lower().replace(' ', ''),
                        self.optimize_metric.lower().replace(' ', '_'),
                        self.optimize_metric.replace(" [%]", ""),
                        # Add other potential variations if needed
                    ]
                    for var in variations_to_try:
                        if var in available_metrics_idx: 
                             metric_key_actual = var
                             logger.warning(f"  Using metric key '{metric_key_actual}' (found in index) instead of requested '{self.optimize_metric}'.")
                             break
                        # Check case-insensitive variation
                        try:
                            lower_idx = [idx.lower() for idx in available_metrics_idx if isinstance(idx, str)] # Apply lower only to strings
                            logger.debug(f"  [find_metric_key] Lowercase string keys: {lower_idx}")
                            if var.lower() in lower_idx:
                                original_case_metric = available_metrics_idx[lower_idx.index(var.lower())]
                                metric_key_actual = original_case_metric
                                logger.warning(f"  Using metric key '{metric_key_actual}' (case-insensitive match in index) instead of requested '{self.optimize_metric}'.")
                                break
                        except Exception as e_find:
                            # Log any error during the case-insensitive check specifically
                            logger.error(f"  [find_metric_key] Error during case-insensitive check for '{var}': {e_find}", exc_info=False) # Keep log concise
                            
                    if metric_key_actual is None:
                        logger.error(f"  Metric '{self.optimize_metric}' (or variations) not found in available stats index: {available_metrics_idx}.") # Changed log message
                        summary_data.append({'strategy': name, 'error': f"Metric '{self.optimize_metric}' not found in stats index"})
                        continue
                     
                # Get the performance series (ROW) for the specific metric
                try:
                    perf_series = portfolio_stats.loc[metric_key_actual] # Select ROW using metric key
                except KeyError as ke:
                    logger.error(f"  KeyError accessing metric '{metric_key_actual}' in stats: {ke}")
                    summary_data.append({'strategy': name, 'error': f"KeyError accessing metric: {ke}"})
                    continue
                except Exception as e:
                    logger.error(f"  Error accessing metric '{metric_key_actual}' in stats: {e}")
                    summary_data.append({'strategy': name, 'error': f"Error accessing metric: {e}"})
                    continue
 
                # Find the best COLUMN (parameter tuple in the COLUMNS) based on the metric direction
                if not isinstance(perf_series, pd.Series):
                    logger.error(f"  Performance data for metric '{metric_key_actual}' is not a Series (type: {type(perf_series)}). Cannot find best.")
                    summary_data.append({'strategy': name, 'error': f"Metric '{metric_key_actual}' data is not a Series"})
                    continue
                if perf_series.isna().all():
                    logger.warning(f"  Performance series for metric '{metric_key_actual}' contains only NaNs.")
                    summary_data.append({'strategy': name, 'error': f"Metric '{metric_key_actual}' is all NaN"})
                    continue
                
                # Add specific RsiBB debugging for performance series
                if name == "RsiBB":
                    logger.info(f"RsiBB perf_series type: {type(perf_series)}")
                    logger.info(f"RsiBB perf_series head: {perf_series.head() if hasattr(perf_series, 'head') else 'No head method'}")
                    logger.info(f"RsiBB perf_series contains NaN: {perf_series.isna().any() if hasattr(perf_series, 'isna') else 'Cannot check NaN'}")
                    logger.info(f"RsiBB perf_series NaN count: {perf_series.isna().sum() if hasattr(perf_series, 'isna') else 'Cannot count NaN'}")
                
                # Use skipna=True to handle potential NaNs during comparison
                best_col_idx = perf_series.idxmax(skipna=True) if not lower_is_better else perf_series.idxmin(skipna=True) # Find best COLUMN index
                 
                # Check if idxmax/idxmin returned NaN (happens if all values are NaN)
                if pd.isna(best_col_idx):
                    logger.warning(f"  Could not determine best column (parameter tuple) for metric '{metric_key_actual}', likely due to all NaNs.")
                    summary_data.append({'strategy': name, 'error': f"Could not find best column (params) for {metric_key_actual} (all NaN?)"})
                    continue
 
                # Get stats COLUMN for the single best run using the best parameter column index
                best_perf_stats = portfolio_stats[best_col_idx] # Get stats Series (COLUMN) for the best run 
                score = best_perf_stats.loc[metric_key_actual] # Get score from that column's specific metric row
 
                # Reconstruct params from the best COLUMN index (which is the parameter tuple or single value)
                best_params = None
                best_params_str = f"Column Index: {best_col_idx}" # Default if reconstruction fails
                
                # Get parameter names from the columns MultiIndex levels (if applicable)
                param_names = []
                if isinstance(portfolio_stats.columns, pd.MultiIndex):
                    param_names = portfolio_stats.columns.names # Get names from COLUMNS now
                else:
                    # Handle case where columns might be single level (e.g., single param optimization)
                    param_names = [portfolio_stats.columns.name] if portfolio_stats.columns.name else ['param_0']
 
                # Handle potential unnamed levels
                if not param_names or all(name is None for name in param_names):
                     num_levels = portfolio_stats.columns.nlevels if isinstance(portfolio_stats.columns, pd.MultiIndex) else 1
                     param_names = [f'param_{i}' for i in range(num_levels)]
                     logger.debug(f" Column levels were unnamed, assigned names: {param_names}")

                if isinstance(best_col_idx, tuple) and len(best_col_idx) == len(param_names):
                    best_params = dict(zip(param_names, best_col_idx))
                    # Convert numpy types before JSON serialization
                    best_params_native = convert_numpy_types(best_params)
                    best_params_str = json.dumps(best_params_native)
                elif not isinstance(best_col_idx, tuple) and len(param_names) == 1: # Handle single parameter optimization (column index is not a tuple)
                     best_params = {param_names[0]: best_col_idx}
                     # Convert numpy types before JSON serialization
                     best_params_native = convert_numpy_types(best_params)
                     best_params_str = json.dumps(best_params_native)
                else:
                     logger.warning(f"  Could not reconstruct params dictionary from column index {best_col_idx} (type: {type(best_col_idx)}, levels: {len(param_names)}) and param names {param_names}.")
 
                logger.info(f"  Best Score ({metric_key_actual}): {score:.4f}") # Use the actual metric key found
                logger.info(f"  Best Params: {best_params_str}")
                
                # Extract other common metrics using their likely names from the best stats COLUMN (best_perf_stats Series)
                def find_metric_key(possible_names, stats_series):
                    # Check index of the Series (which represents the metrics)
                    if not isinstance(stats_series, pd.Series):
                        logger.error(f"  [find_metric_key] Input is not a Series: {type(stats_series)}")
                        return None
                        
                    available_keys = stats_series.index.tolist()
                    logger.debug(f"  [find_metric_key] Available keys: {available_keys}")
                    logger.debug(f"  [find_metric_key] Searching for: {possible_names}")
                    
                    for name in possible_names:
                        # Direct match (case-sensitive)
                        if name in available_keys:
                            logger.debug(f"  [find_metric_key] Found direct match: '{name}'")
                            return name
                            
                        # Try case-insensitive match (only on string keys)
                        try:
                            lower_index = [idx.lower() for idx in available_keys if isinstance(idx, str)]
                            logger.debug(f"  [find_metric_key] Lowercase string keys: {lower_index}")
                            if name.lower() in lower_index:
                                original_case_idx = lower_index.index(name.lower())
                                # Find the original key corresponding to the lowercased index
                                str_keys = [idx for idx in available_keys if isinstance(idx, str)]
                                if original_case_idx < len(str_keys):
                                    original_case = str_keys[original_case_idx]
                                    logger.debug(f"  [find_metric_key] Found '{original_case}' via case-insensitive search for '{name}'")
                                    return original_case
                                else:
                                     logger.warning(f"  [find_metric_key] Index mismatch finding original case for '{name.lower()}'")
                        except Exception as e_find:
                            # Log any error during the case-insensitive check specifically
                            logger.error(f"  [find_metric_key] Error during case-insensitive check for '{name}': {e_find}", exc_info=False) # Keep log concise
                            
                    logger.debug(f"  [find_metric_key] Could not find any of {possible_names} in stats index: {available_keys}")
                    return None

                total_return_key = find_metric_key(['Total Return [%]', 'Total Return', 'total_return', 'total_return_pct'], best_perf_stats)
                max_dd_key = find_metric_key(['Max Drawdown [%]', 'Max Drawdown', 'max_drawdown', 'max_drawdown_pct'], best_perf_stats)
                win_rate_key = find_metric_key(['Win Rate [%]', 'Win Rate', 'win_rate', 'win_rate_pct'], best_perf_stats)
                trades_key = find_metric_key(['Total Trades', 'Trades', 'num_trades'], best_perf_stats)
                sharpe_key = find_metric_key(['Sharpe Ratio', 'sharpe_ratio', 'sharpe'], best_perf_stats)
                sortino_key = find_metric_key(['Sortino Ratio', 'sortino_ratio', 'sortino'], best_perf_stats)

                # Extract values using the found keys from the best_perf_stats Series (the column)
                total_return = best_perf_stats.get(total_return_key, np.nan) if total_return_key else np.nan
                max_dd = best_perf_stats.get(max_dd_key, np.nan) if max_dd_key else np.nan
                win_rate = best_perf_stats.get(win_rate_key, np.nan) if win_rate_key else np.nan
                num_trades = best_perf_stats.get(trades_key, 0) if trades_key else 0 # Default to 0
                sharpe_ratio = best_perf_stats.get(sharpe_key, np.nan) if sharpe_key else np.nan
                sortino_ratio = best_perf_stats.get(sortino_key, np.nan) if sortino_key else np.nan

                logger.info(f"  Total Return: {total_return:.2f}% | Max Drawdown: {max_dd:.2f}% | Win Rate: {win_rate:.2f}% | Trades: {int(num_trades)} | Sharpe: {sharpe_ratio:.3f} | Sortino: {sortino_ratio:.3f}")
                
                summary_data.append({
                    'strategy': name,
                    'best_score': score,
                    'metric': metric_key_actual, # Report the metric key actually used
                    'total_return_pct': total_return,
                    'max_drawdown_pct': max_dd,
                    'win_rate_pct': win_rate,
                    'num_trades': int(num_trades),
                    'sharpe_ratio': sharpe_ratio,
                    'sortino_ratio': sortino_ratio,
                    'best_params': best_params_str,
                    'error': None
                })
                
                # Update overall best if the current score is better
                is_better = False
                if not pd.isna(score): # Only compare valid scores
                     if lower_is_better:
                         is_better = score < overall_best_score
                     else:
                         is_better = score > overall_best_score

                if is_better:
                     overall_best_strategy = name
                     overall_best_score = score
                     overall_best_params = convert_numpy_types(best_params) # Store dict with native types

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
            logger.info(f"Best Parameters: {overall_best_params}") # Now holds dict
        else:
            logger.info("No successful optimizations found to determine overall best.")
            
        # Save summary DataFrame to CSV
        if save_summary and summary_data:
            try:
                summary_df = pd.DataFrame(summary_data)
                # Define column order for clarity
                cols = ['strategy', 'metric', 'best_score', 
                        'total_return_pct', 'max_drawdown_pct', 'win_rate_pct', 
                        'num_trades', 'sharpe_ratio', 'sortino_ratio', 
                        'best_params', 'error']
                # Reorder and add missing columns if necessary
                summary_df = summary_df.reindex(columns=cols)
                # Sort by the actual score, handling NaNs (put them last)
                summary_df.sort_values(by='best_score', ascending=lower_is_better, inplace=True, na_position='last')
                
                summary_df.to_csv(summary_filename, index=False, float_format='%.4f') # Add float formatting
                logger.info(f"\nSaved optimization summary to: {summary_filename}")
            except Exception as e:
                logger.error(f"Failed to save summary file '{summary_filename}': {e}", exc_info=True) # Log traceback
        elif not summary_data:
            logger.warning("No summary data generated to save.")

# --- Granularity Mapping ---
# GRANULARITY_MAP_SECONDS = {
#     '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
#     '1h': 3600, '2h': 7200, '4h': 14400, '6h': 21600, '1d': 86400
# }
# Using the imported version from data.data_fetcher now

# --- Command Line Interface ---
def main():
    parser = argparse.ArgumentParser(description="Run multi-strategy vectorbtpro optimization.")
    parser.add_argument("--symbol", type=str, default="BTC-USD", help="Trading symbol (e.g., BTC-USD)")
    parser.add_argument("--start_date", type=str, default="2022-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, default=datetime.now().strftime('%Y-%m-%d'), help="End date (YYYY-MM-DD)")
    parser.add_argument("--granularity", type=str, nargs='+', default=['1d'], 
                        help="List of granularities to test (e.g., 1d 4h 1h)", 
                        choices=list(GRANULARITY_MAP_SECONDS.keys())) # Ensure choices is a list
    parser.add_argument("--capital", type=float, default=10000, help="Initial capital")
    parser.add_argument("--commission", type=float, default=0.001, help="Commission per trade (e.g., 0.001 for 0.1%)")
    parser.add_argument("--slippage", type=float, default=0.0005, help="Slippage per trade (e.g., 0.0005 for 0.05%)")
    # Changed default metric to Sharpe Ratio as it's common and usually present
    parser.add_argument("--metric", type=str, default="Sharpe Ratio", help="Metric to optimize for (e.g., 'Sharpe Ratio', 'Total Return [%]', 'Sortino Ratio')") # Use vbt metric names

    args = parser.parse_args()
    
    all_results_across_timeframes = [] # Store results from all timeframes
    start_time = time.time()

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
        
    elapsed = time.time() - start_time
    logger.info(f"\n===== All Timeframe Optimizations Complete =====")
    logger.info(f"Script completed in {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
    logger.info(f"Results saved to reports/ directory")
    logger.info(f"SCRIPT EXECUTION COMPLETED SUCCESSFULLY!")
    # Optional: Add code here to process `all_results_across_timeframes` for a combined report

if __name__ == "__main__":
    # Example Usage:
    # python scripts/optimize_strategies.py --symbol ETH-USD --start_date 2021-01-01 --granularity 3600 --metric "Total Return [%]"
    main() 