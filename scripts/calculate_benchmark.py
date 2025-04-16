import sys
import os
import pandas as pd
import vectorbtpro as vbt
import logging
from datetime import datetime
from pathlib import Path

# Add project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the exact data fetcher used by WFO
try:
    from data.data_fetcher import fetch_historical_data, get_vbt_freq_str
except ImportError as e:
    print(f"Error: Could not import from data.data_fetcher: {e}")
    print("Please ensure data/data_fetcher.py exists and is accessible.")
    sys.exit(1)

# Setup Logging
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"benchmark_calc_{datetime.now():%Y%m%d_%H%M%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def calculate_buy_and_hold(symbol: str, start_date: str, end_date: str, granularity: int):
    """
    Calculates Buy & Hold performance metrics for a given symbol and period.

    Args:
        symbol: Trading pair (e.g., 'BTC-USD')
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        granularity: Data granularity in seconds (e.g., 14400 for 4H)

    Returns:
        A pandas Series containing benchmark performance metrics, or None on failure.
    """
    logger.info(f"--- Calculating Buy & Hold Benchmark for {symbol} ---")
    logger.info(f"Period: {start_date} to {end_date}, Granularity: {granularity}s")

    # 1. Fetch data using the same function as WFO
    price_data = fetch_historical_data(symbol, start_date, end_date, granularity)

    if price_data is None or price_data.empty:
        logger.error("Failed to fetch price data for benchmark calculation.")
        return None

    if not isinstance(price_data.index, pd.DatetimeIndex):
        logger.error("Price data index is not a DatetimeIndex. Cannot calculate benchmark.")
        return None
        
    # Ensure data is sorted by time
    price_data = price_data.sort_index()

    close = price_data['close']
    
    # 2. Get the vectorbt frequency string
    vbt_freq_str = get_vbt_freq_str(granularity)
    if not vbt_freq_str:
        logger.error(f"Could not determine vbt frequency string for granularity {granularity}s.")
        return None
        
    # 3. Calculate Buy & Hold metrics using vectorbtpro
    try:
        # Calculate percentage returns
        # price_returns = close.vbt.pct_change() # Requires Pro .vbt accessor? Standard pct_change is fine.
        price_returns = close.pct_change()

        # Use the returns accessor to get stats
        # We need to handle the initial NaN from pct_change()
        # vectorbt often handles this, but let's be safe and fill with 0 for stats calculation
        benchmark_stats = price_returns.fillna(0).vbt.returns(freq=vbt_freq_str).stats()

        logger.info("Benchmark calculation successful.")
        return benchmark_stats

    except Exception as e:
        logger.error(f"Error calculating benchmark stats: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    # --- Configuration (Match WFO script) ---
    SYMBOL = "BTC-USD"
    START_DATE = "2021-01-01"
    END_DATE = "2024-06-01"
    GRANULARITY_SECONDS = 14400 # 4 hours

    benchmark_results = calculate_buy_and_hold(
        symbol=SYMBOL,
        start_date=START_DATE,
        end_date=END_DATE,
        granularity=GRANULARITY_SECONDS
    )

    if benchmark_results is not None:
        # Log the heading without the internal newline
        logger.info("--- Buy & Hold Benchmark Performance ---")
        # Select and rename key metrics for clarity
        metrics_to_display = {
            'Start': 'Start Date',
            'End': 'End Date',
            'Period': 'Duration',
            'Total Return [%]': 'Total Return',
            'Annualized Return [%]': 'Annualized Return',
            'Max Drawdown [%]': 'Max Drawdown',
            'Sharpe Ratio': 'Sharpe Ratio',
            'Sortino Ratio': 'Sortino Ratio'
            # Add others if needed: 'Avg Winning Trade [%]', 'Avg Losing Trade [%]', 'Profit Factor' 
            # Note: Trade-based stats aren't applicable to Buy & Hold returns directly
        }
        
        display_series = pd.Series(dtype=object)
        for key, name in metrics_to_display.items():
             if key in benchmark_results:
                 value = benchmark_results[key]
                 # Format percentages
                 if '%' in key:
                     display_series[name] = f'{value:.2f}%'
                 # Format ratios
                 elif 'Ratio' in key:
                     display_series[name] = f'{value:.3f}'
                 # Format dates/periods
                 elif key in ['Start', 'End', 'Period']:
                      # Check if value is Timestamp or Timedelta before formatting
                      if isinstance(value, pd.Timestamp):
                         display_series[name] = value.strftime('%Y-%m-%d')
                      elif isinstance(value, pd.Timedelta):
                         display_series[name] = str(value) # Keep timedelta as string
                      else:
                         display_series[name] = value # Use raw value if not Timestamp/Timedelta
                 else:
                      display_series[name] = value
             else:
                  display_series[name] = 'N/A'

        print(display_series.to_string())

        # Optionally save the full results
        reports_dir = Path("reports/benchmark")
        reports_dir.mkdir(parents=True, exist_ok=True)
        benchmark_file = reports_dir / f"benchmark_{SYMBOL}_{GRANULARITY_SECONDS}s_{START_DATE}_to_{END_DATE}.csv"
        try:
            benchmark_results.to_frame(name='Value').to_csv(benchmark_file)
            logger.info(f"Saved full benchmark stats to {benchmark_file}")
        except Exception as e:
             logger.error(f"Failed to save benchmark stats: {e}")

    else:
        logger.error("Benchmark calculation failed.") 