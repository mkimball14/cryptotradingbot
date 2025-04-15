import subprocess
import itertools
import json
import os
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# --- Configuration ---
TARGET_SCRIPT = "scripts/backtest_stoch_sma_vbt_pro.py" # Script to run
REPORTS_DIR = "reports"
SUMMARY_FILE = "reports/backtest_summary.csv"
SYMBOL = "BTC-USD"
START_DATE = "2020-01-01"
END_DATE = datetime.now().strftime('%Y-%m-%d')
INITIAL_CAPITAL = 10000
COMMISSION = 0.001
SLIPPAGE = 0.0005
WFO_TEST_DAYS = 180 # Increased to allow for longer trend filters
WFO_WINDOW_YEARS = 2.0
OPTIMIZE_METRIC = "Sharpe Ratio"

# --- Parameters to Iterate Over ---
GRANULARITY_OPTIONS = ['1d', '4h', '1h'] # e.g., ['1d', '4h']
TREND_FILTER_OPTIONS = [0, 50, 100, 200] # 0 means no filter
SL_ATR_OPTIONS = [1.5, 2.0, 2.5, 3.0]
TSL_ATR_OPTIONS = [2.0, 2.5, 3.0, 3.5]
# Add other parameter ranges here if needed

# --- Logging Setup ---
log_file = Path(REPORTS_DIR) / "multi_backtest_log.txt"
log_file.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler() # Also print to console
    ]
)

# --- Helper Functions ---
def get_granularity_suffix(granularity: str) -> str:
    return f"_{granularity.upper()}"

def get_stops_suffix(use_stops: bool, sl: float, tsl: float) -> str:
    return f"_SL{sl}_TSL{tsl}" if use_stops else "_NoStops"

def get_trend_suffix(trend_window: int) -> str:
    return f"_SMA{trend_window}" if trend_window > 0 else "_NoTrend"

def parse_results(report_path: Path) -> dict:
    """Parses key metrics from the JSON report file."""
    metrics = {
        'oos_mean_sharpe': None,
        'oos_mean_return': None,
        'oos_mean_drawdown': None,
        'oos_std_sharpe': None,
        'oos_std_return': None,
        'oos_std_drawdown': None,
        'error': None
    }
    if not report_path.exists():
        metrics['error'] = "Report file not found"
        return metrics
    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
        metrics['oos_mean_sharpe'] = data.get('oos_mean_sharpe')
        metrics['oos_mean_return'] = data.get('oos_mean_return')
        metrics['oos_mean_drawdown'] = data.get('oos_mean_drawdown')
        metrics['oos_std_sharpe'] = data.get('oos_std_sharpe')
        metrics['oos_std_return'] = data.get('oos_std_return')
        metrics['oos_std_drawdown'] = data.get('oos_std_drawdown')
    except json.JSONDecodeError:
        metrics['error'] = "Failed to decode JSON"
    except Exception as e:
        metrics['error'] = str(e)
    return metrics

# Helper to safely format metrics for logging
def format_metric(value, precision=4):
    if value is None:
        return "N/A"
    try:
        return f"{value:.{precision}f}"
    except (TypeError, ValueError):
        return str(value) # Return as string if formatting fails

# --- Main Loop ---
def main():
    results_summary = []
    reports_path = Path(REPORTS_DIR)
    reports_path.mkdir(parents=True, exist_ok=True)

    # Generate all combinations of parameters
    param_combinations = list(itertools.product(
        GRANULARITY_OPTIONS,
        TREND_FILTER_OPTIONS,
        SL_ATR_OPTIONS,
        TSL_ATR_OPTIONS
    ))

    total_runs = len(param_combinations)
    logging.info(f"Starting multiple backtests. Total runs planned: {total_runs}")

    for i, params in enumerate(param_combinations):
        granularity, trend_window, sl_atr, tsl_atr = params
        run_num = i + 1

        # Basic validation: Ensure trend window is calculable within test days if granularity > 1h
        # For simplicity, we'll just require test_days > trend_window for daily/4h
        # A more robust check would convert days to periods based on granularity
        if granularity in ['1d', '4h'] and trend_window > 0 and WFO_TEST_DAYS <= trend_window:
            logging.warning(f"Run {run_num}/{total_runs}: Skipping Gran={granularity}, Trend={trend_window} because WFO_TEST_DAYS ({WFO_TEST_DAYS}) <= Trend Window. Increase WFO_TEST_DAYS.")
            continue
        
        # Basic validation: Ensure TSL >= SL if both > 0
        if tsl_atr > 0 and sl_atr > 0 and tsl_atr < sl_atr:
            logging.warning(f"Run {run_num}/{total_runs}: Skipping SL={sl_atr}, TSL={tsl_atr} because TSL < SL.")
            continue

        # Construct command
        cmd = [
            "python", TARGET_SCRIPT,
            "--symbol", SYMBOL,
            "--start_date", START_DATE,
            "--end_date", END_DATE,
            "--granularity", granularity,
            "--initial_capital", str(INITIAL_CAPITAL),
            "--commission", str(COMMISSION),
            "--slippage", str(SLIPPAGE),
            "--optimize_metric", OPTIMIZE_METRIC,
            "--wfo_test_days", str(WFO_TEST_DAYS),
            "--wfo_window_years", str(WFO_WINDOW_YEARS),
            "--reports_dir", REPORTS_DIR
        ]

        use_stops = True
        if sl_atr <= 0 and tsl_atr <= 0:
            cmd.append("--no_stops")
            use_stops = False
        else:
            cmd.extend(["--sl_atr", str(sl_atr)])
            cmd.extend(["--tsl_atr", str(tsl_atr)])

        if trend_window > 0:
            cmd.extend(["--trend_filter_window", str(trend_window)])
        # Add --no_trend_filter or similar if window is 0? Script handles 0 correctly.

        logging.info(f"--- Run {run_num}/{total_runs} --- Start ---")
        logging.info(f"Params: Gran={granularity}, Trend={trend_window}, SL={sl_atr}, TSL={tsl_atr}")
        logging.debug(f"Command: {' '.join(cmd)}")

        # --- Execute the script ---
        try:
            process = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logging.info(f"Run {run_num}/{total_runs}: Script executed successfully.")
            logging.debug(f"stdout:\n{process.stdout[-1000:]}") # Log last 1000 chars
            logging.debug(f"stderr:\n{process.stderr}")
            run_error = None
        except subprocess.CalledProcessError as e:
            logging.error(f"Run {run_num}/{total_runs}: Script execution failed! Error code: {e.returncode}")
            logging.error(f"stdout:\n{e.stdout}")
            logging.error(f"stderr:\n{e.stderr}")
            run_error = f"Subprocess Error Code {e.returncode}"
        except Exception as e:
            logging.error(f"Run {run_num}/{total_runs}: An unexpected error occurred during execution: {e}")
            run_error = f"Execution Error: {e}"

        # --- Parse results --- 
        # Construct expected report filename based on script's naming convention
        strategy_name_part = "stoch_sma" # Update if TARGET_SCRIPT changes
        g_suffix = get_granularity_suffix(granularity)
        s_suffix = get_stops_suffix(use_stops, sl_atr, tsl_atr)
        t_suffix = get_trend_suffix(trend_window)
        report_filename = f"manual_{strategy_name_part}_wfo_results_{SYMBOL}{g_suffix}{s_suffix}{t_suffix}.json"
        report_path = reports_path / report_filename

        logging.info(f"Run {run_num}/{total_runs}: Attempting to parse results from: {report_path}")
        metrics = parse_results(report_path)
        
        # If subprocess failed, override parsing error message
        if run_error:
             metrics['error'] = run_error 

        # Store results
        result_data = {
            "run": run_num,
            "script": os.path.basename(TARGET_SCRIPT),
            "symbol": SYMBOL,
            "start_date": START_DATE,
            "end_date": END_DATE,
            "granularity": granularity,
            "trend_filter_window": trend_window,
            "sl_atr": sl_atr if use_stops else None,
            "tsl_atr": tsl_atr if use_stops else None,
            "wfo_test_days": WFO_TEST_DAYS,
            "wfo_window_years": WFO_WINDOW_YEARS,
            **metrics # Add parsed metrics
        }
        results_summary.append(result_data)
        # Use helper function for safe formatting
        sharpe_str = format_metric(metrics['oos_mean_sharpe'])
        return_str = format_metric(metrics['oos_mean_return'], 4) # Keep 4 decimals for return
        drawdown_str = format_metric(metrics['oos_mean_drawdown'])
        error_str = metrics['error'] if metrics['error'] else "None"
        
        logging.info(f"Run {run_num}/{total_runs}: Sharpe={sharpe_str} | Return={return_str} | Drawdown={drawdown_str} | Error={error_str}")
        logging.info(f"--- Run {run_num}/{total_runs} --- End ---\
")

        # Save summary incrementally
        try:
            summary_df = pd.DataFrame(results_summary)
            summary_df.to_csv(SUMMARY_FILE, index=False)
        except Exception as e:
            logging.error(f"Failed to save intermediate summary: {e}")

    # Final save
    logging.info(f"Finished all {total_runs} backtest runs.")
    try:
        summary_df = pd.DataFrame(results_summary)
        summary_df.to_csv(SUMMARY_FILE, index=False)
        logging.info(f"Final summary saved to {SUMMARY_FILE}")
    except Exception as e:
        logging.error(f"Failed to save final summary: {e}")

if __name__ == "__main__":
    main() 