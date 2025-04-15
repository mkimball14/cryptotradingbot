import vectorbtpro as vbt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import logging
import sys
import os
import json
from datetime import datetime
from typing import Tuple, Dict, List, Optional, Any
from pathlib import Path
from tqdm import tqdm  # For progress bars
import argparse
from functools import lru_cache
import traceback
from plotly.subplots import make_subplots
import warnings
import time
from itertools import product

# Add project root to sys.path to allow importing app modules
# Assume the script is run from the project root or the path is adjusted accordingly
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Import the base SDK client directly for this script
    from coinbase.rest import RESTClient
    # We might still need Settings for other parts, keep import for now
    # from app.core.coinbase import CoinbaseClient # No longer needed for data fetching here
    from app.core.config import Settings
    try:
        settings = Settings() # Load settings if available (might be needed elsewhere)
    except Exception as settings_err:
        logger.warning(f"Could not load Settings: {settings_err}. Some features might be limited.")
        settings = None
except ImportError as e:
    logger.warning(f"Could not import coinbase.rest.RESTClient or Settings: {e}. Ensure paths/dependencies.")
    # Define placeholders if import fails
    class RESTClient:
        def __init__(self, *args, **kwargs):
            logger.warning("Using placeholder RESTClient.")
        def get_public_candles(self, *args, **kwargs):
            logger.warning("Placeholder RESTClient cannot fetch data.")
            return None
    settings = None # Indicate settings failed to load

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Utility Functions (Copied from backtest_rsi_vbt.py, potentially modify later) ---

def fetch_historical_data(product_id, start_date, end_date, granularity=86400):
    """
    Fetch historical price data from Coinbase or from cache.
    (Modified to read credentials directly from cdp_api_key.json)
    """
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    granularity_str = get_granularity_str(granularity)
    if not granularity_str:
        logger.error(f"Invalid granularity seconds: {granularity}. Cannot create cache key.")
        return create_sample_data(start_date, end_date)
    cache_file = cache_dir / f"{product_id.replace('-', '')}_{start_date}_{end_date}_{granularity_str}.csv"

    if cache_file.exists():
        logger.info(f"Loading cached data from: {cache_file}")
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if all(col in data.columns for col in required_cols):
                 logger.info(f"Successfully loaded cached data with shape: {data.shape}")
                 return data
            else:
                logger.warning(f"Cached data missing columns: {set(required_cols) - set(data.columns)}. Refetching.")
                cache_file.unlink()
        except Exception as e:
            logger.warning(f"Error loading cached data: {e}, will fetch fresh data")

    if "sample" in product_id.lower():
        return create_sample_data(start_date, end_date)

    # Read credentials directly from the JSON file
    creds_file = "cdp_api_key.json"
    if not os.path.exists(creds_file):
        logger.warning(f"Credentials file not found: {creds_file}. Generating sample data.")
        return create_sample_data(start_date, end_date)

    try:
        with open(creds_file, 'r') as f:
            creds = json.load(f)
        # Use the exact key names from the JSON file
        key_name = creds.get('name')
        private_key = creds.get('privateKey')

        if not key_name or not private_key:
            logger.warning(f"Missing 'name' or 'privateKey' in {creds_file}. Generating sample data.")
            return create_sample_data(start_date, end_date)

        # Initialize the base RESTClient directly using SDK arguments
        client = RESTClient(api_key=key_name, api_secret=private_key)
        logger.info(f"Requesting candles from Coinbase API (Granularity: {granularity_str}) using keys from {creds_file}")

        # Convert dates to Unix timestamps for the API call
        start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

        # --- Re-implement Chunking Logic --- 
        max_candles_per_request = 300 # API limit (use slightly less than 350 to be safe)
        total_seconds = end_timestamp - start_timestamp
        total_candles_needed = total_seconds // granularity 
        chunks = (total_candles_needed + max_candles_per_request - 1) // max_candles_per_request
        logger.info(f"Need {total_candles_needed} candles, fetching in {chunks} chunks of max {max_candles_per_request}...")

        all_candles = []
        current_start_timestamp = start_timestamp

        for i in tqdm(range(chunks), desc="Fetching Candles"):
            # Calculate end timestamp for this chunk
            # Add max_candles * granularity seconds to the start
            current_end_timestamp = current_start_timestamp + (max_candles_per_request * granularity) 
            # Ensure chunk end doesn't exceed the overall end time
            current_end_timestamp = min(current_end_timestamp, end_timestamp)

            # If the calculated end is less than or same as start, break (shouldn't happen with proper logic but safety check)
            if current_end_timestamp <= current_start_timestamp:
                if i == 0 and total_candles_needed <= 0: # Handle edge case of 0 duration
                     logger.warning("Date range results in zero candles needed.")
                else: 
                     logger.warning(f"Chunk {i+1} calculation resulted in end <= start timestamp. Breaking fetch loop.")
                break

            logger.debug(f"Fetching chunk {i+1}/{chunks}: {datetime.fromtimestamp(current_start_timestamp)} to {datetime.fromtimestamp(current_end_timestamp)}")

            # Prepare parameters for this chunk
            params = {
                "granularity": granularity_str,
                "start": str(current_start_timestamp),
                "end": str(current_end_timestamp)
            }

            try:
                # Use the SDK's get_public_candles method for the chunk
                candles_response = client.get_public_candles(product_id=product_id, **params)
                
                # Process the response
                if hasattr(candles_response, 'candles') and candles_response.candles:
                     chunk_data = [c.to_dict() for c in candles_response.candles]
                     all_candles.extend(chunk_data)
                     logger.debug(f"Got {len(chunk_data)} candles for chunk {i+1}")
                else:
                     logger.warning(f"No candles returned for chunk {i+1}. Response: {candles_response}")
                     # Optionally break or continue based on requirements
            except Exception as chunk_error:
                logger.error(f"Error fetching chunk {i+1}: {chunk_error}")
                if i == 0: # If first chunk fails, fallback to sample data
                     logger.info("First chunk fetch failed critically, falling back to sample data")
                     return create_sample_data(start_date, end_date)
                # Decide if we should break or just skip this chunk
                break 
            
            # Update start timestamp for the next chunk
            # Start next chunk right after the end of the current one
            current_start_timestamp = current_end_timestamp
            
            # Break if we have reached or passed the overall end timestamp
            if current_start_timestamp >= end_timestamp:
                break

            # Add a small delay to avoid rate limiting
            time.sleep(0.3) 

        # Check if any candles were fetched
        if not all_candles:
            logger.warning("No candles fetched after attempting all chunks. Generating sample data.")
            return create_sample_data(start_date, end_date)

        # --- Candle processing logic (should be fine if candle dicts are correct) ---
        df = pd.DataFrame(all_candles)
        expected_cols = ['start', 'low', 'high', 'open', 'close', 'volume'] # SDK uses 'start' for time
        if not all(col in df.columns for col in expected_cols):
            logger.error(f"Candle data missing expected columns (start,low,high,open,close,volume). Got: {df.columns.tolist()}")
            return create_sample_data(start_date, end_date)

        # Rename 'start' to 'time' and convert
        df.rename(columns={'start': 'time'}, inplace=True)
        try:
            df['time'] = pd.to_datetime(pd.to_numeric(df['time']), unit='s')
        except (ValueError, TypeError):
            df['time'] = pd.to_datetime(df['time'])
            
        df.set_index('time', inplace=True)
        # Select only the necessary OHLCV columns in the standard order
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        df.sort_index(inplace=True)

        # Ensure OHLC integrity
        df['high'] = df[['open', 'high', 'low', 'close']].max(axis=1)
        df['low'] = df[['open', 'high', 'low', 'close']].min(axis=1)

        df.to_csv(cache_file)
        logger.info(f"Cached {len(df)} data points to: {cache_file}")
        return df

    except Exception as e:
        logger.error(f"General error fetching data via RESTClient: {e}")
        logger.debug(traceback.format_exc())
        logger.info("Generating sample data due to error.")
        return create_sample_data(start_date, end_date)

# Helper function to map seconds to granularity strings
def get_granularity_str(granularity_seconds: int) -> Optional[str]:
    gran_map = {
        60: "ONE_MINUTE",
        300: "FIVE_MINUTES",
        900: "FIFTEEN_MINUTES",
        1800: "THIRTY_MINUTES",
        3600: "ONE_HOUR",
        7200: "TWO_HOURS",
        21600: "SIX_HOURS",
        86400: "ONE_DAY"
    }
    return gran_map.get(granularity_seconds)

def create_sample_data(start_date, end_date, initial_price=20000.0, daily_vol=0.02):
    """Creates sample daily OHLCV data."""
    logger.info(f"Creating sample price data from {start_date} to {end_date}...")
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"sample_{start_date}_{end_date}.csv"

    if cache_file.exists():
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if all(col in data.columns for col in required_cols):
                 logger.info(f"Loaded {len(data)} days of cached sample data from: {cache_file}")
                 return data
            else:
                 logger.warning("Cached sample data invalid. Regenerating...")
                 cache_file.unlink()
        except Exception as e:
            logger.warning(f"Error loading cached sample data: {e}. Regenerating...")


    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    # Ensure the date range includes the end date
    daterange = pd.date_range(start=start, end=end + pd.Timedelta(days=1) , freq='D')[:-1]


    np.random.seed(42)
    price = initial_price
    prices = []
    for _ in range(len(daterange)):
        daily_return = np.random.normal(0.0002, daily_vol)
        price *= (1 + daily_return)
        prices.append(price)

    close_prices = pd.Series(prices, index=daterange)
    data = pd.DataFrame(index=daterange)
    data['close'] = close_prices
    data['open'] = data['close'].shift(1).fillna(method='bfill') # Backfill first open
    rand_h = np.random.uniform(0, 0.03, len(data))
    rand_l = np.random.uniform(0, 0.03, len(data))
    data['high'] = np.maximum(data['open'], data['close']) * (1 + rand_h)
    data['low'] = np.minimum(data['open'], data['close']) * (1 - rand_l)

    price_changes = np.abs(data['close'].pct_change().fillna(0.01))
    base_volume = 1000
    data['volume'] = base_volume * (1 + 5 * price_changes) + np.random.uniform(0, base_volume * 0.1, len(data))

    try:
        data.to_csv(cache_file)
        logger.info(f"Cached {len(data)} days of sample data to: {cache_file}")
    except Exception as e:
        logger.error(f"Error caching sample data: {e}")

    logger.info(f"Generated {len(data)} days of sample price data.")
    return data


def calculate_risk_metrics(portfolio):
    """
    Calculate key risk and performance metrics from a VectorBT portfolio.
    Handles potential missing stats gracefully.
    """
    metrics = {
        'total_return': 0, 'sharpe': 0, 'max_dd': 0, 'win_rate': 0,
        'trades': 0, 'annual_return': 0, 'sortino': 0, 'profit_factor': 0,
        'recovery_factor': 0
    }
    if portfolio is None:
        return metrics

    try:
        stats = portfolio.stats()
        returns = portfolio.returns

        # Basic metrics
        metrics['total_return'] = stats.get('Total Return [%]', 0) / 100
        metrics['sharpe'] = stats.get('Sharpe Ratio', 0)
        metrics['max_dd'] = stats.get('Max Drawdown [%]', 0) / 100
        metrics['trades'] = stats.get('Total Trades', 0)
        metrics['win_rate'] = stats.get('Win Rate [%]', 0) / 100
        metrics['profit_factor'] = stats.get('Profit Factor', 0)
        
        # Calculated metrics
        if metrics['max_dd'] > 0:
            metrics['recovery_factor'] = metrics['total_return'] / metrics['max_dd']
        else:
             metrics['recovery_factor'] = float('inf') if metrics['total_return'] > 0 else 0
             
        # Annualized Return
        start_date = portfolio.wrapper.index[0]
        end_date = portfolio.wrapper.index[-1]
        years = (end_date - start_date).days / 365.25
        if years > 0:
             metrics['annual_return'] = (1 + metrics['total_return'])**(1/years) - 1
        else:
             metrics['annual_return'] = 0 # Avoid division by zero for short periods

        # Sortino Ratio
        metrics['sortino'] = stats.get('Sortino Ratio', 0) # VBT Pro often calculates this

    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}", exc_info=True)
        # Return defaults if error occurs
        
    return metrics


def create_dashboard(results, opt_results=None, price_data=None, symbol="BTC-USD", start_date=None, end_date=None, reports_dir=None):
    """
    Create an interactive dashboard for strategy analysis.
    (Adapted for potentially different results structure from VBT Pro optimization)
    """
    if results is None or 'portfolio' not in results or results['portfolio'] is None:
        logger.error("Cannot create dashboard: Invalid base strategy results.")
        return None
        
    if price_data is None:
         logger.error("Cannot create dashboard: Missing price data.")
         return None

    try:
        reports_dir = Path(reports_dir) if reports_dir else Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)

        basic_portfolio = results['portfolio']
        basic_metrics = calculate_risk_metrics(basic_portfolio)

        # Benchmark
        benchmark_returns = price_data['close'].pct_change().dropna()
        benchmark_cum_returns = (1 + benchmark_returns).cumprod() - 1

        # Setup figure
        fig = make_subplots(
            rows=4, cols=2,
            vertical_spacing=0.08,
            horizontal_spacing=0.05,
            subplot_titles=(
                "Cumulative Returns", "Drawdowns",
                "RSI Indicator", "Price and Trades",
                "Daily Returns", "Monthly Returns Heatmap",
                "Strategy Metrics", "Optimization Heatmap (Sharpe)"
            ),
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "xy", "secondary_y": True}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "heatmap"}], # Changed daily returns to bar
                [{"type": "table"}, {"type": "heatmap"}]
            ],
            row_heights=[0.25, 0.25, 0.25, 0.25]
        )

        opt_portfolio = None
        opt_metrics = None
        if opt_results and 'portfolio' in opt_results and opt_results['portfolio'] is not None:
            opt_portfolio = opt_results['portfolio']
            opt_metrics = calculate_risk_metrics(opt_portfolio)
            logger.info("Optimized portfolio found for dashboard.")
        else:
             logger.warning("No optimized portfolio found, dashboard will only show basic results.")


        # 1. Cumulative Returns
        basic_cum_returns = basic_portfolio.returns.cumsum()
        fig.add_trace(go.Scatter(x=basic_cum_returns.index, y=basic_cum_returns, mode='lines', name='Basic RSI', line=dict(color='blue')), row=1, col=1)
        if opt_portfolio:
            opt_cum_returns = opt_portfolio.returns.cumsum()
            fig.add_trace(go.Scatter(x=opt_cum_returns.index, y=opt_cum_returns, mode='lines', name='Optimized RSI', line=dict(color='green')), row=1, col=1)
        fig.add_trace(go.Scatter(x=benchmark_cum_returns.index, y=benchmark_cum_returns, mode='lines', name='Buy & Hold', line=dict(color='grey', dash='dash')), row=1, col=1)

        # 2. Drawdowns
        basic_dd = basic_portfolio.drawdown * 100 # As Percentage - Access as attribute
        fig.add_trace(go.Scatter(x=basic_dd.index, y=basic_dd, mode='lines', name='Basic DD (%)', line=dict(color='red'), fill='tozeroy', fillcolor='rgba(255,0,0,0.1)'), row=1, col=2)
        if opt_portfolio:
            opt_dd = opt_portfolio.drawdown * 100 # Access as attribute
            fig.add_trace(go.Scatter(x=opt_dd.index, y=opt_dd, mode='lines', name='Optimized DD (%)', line=dict(color='orange'), fill='tozeroy', fillcolor='rgba(255,165,0,0.1)'), row=1, col=2)

        # 3. RSI Indicator & Thresholds
        if 'rsi_indicator' in results:
             rsi = results['rsi_indicator']
             fig.add_trace(go.Scatter(x=rsi.index, y=rsi, mode='lines', name='RSI', line=dict(color='purple')), secondary_y=False, row=2, col=1)
             lower = results.get('lower_threshold', 30)
             upper = results.get('upper_threshold', 70)
             fig.add_trace(go.Scatter(x=rsi.index, y=[lower]*len(rsi), mode='lines', name=f'Lower ({lower})', line=dict(color='green', dash='dash')), secondary_y=False, row=2, col=1)
             fig.add_trace(go.Scatter(x=rsi.index, y=[upper]*len(rsi), mode='lines', name=f'Upper ({upper})', line=dict(color='red', dash='dash')), secondary_y=False, row=2, col=1)
        # Add price on secondary axis
        fig.add_trace(go.Scatter(x=price_data.index, y=price_data['close'], mode='lines', name='Price (RHS)', line=dict(color='black', width=1)), secondary_y=True, row=2, col=1)
        fig.update_yaxes(title_text="RSI", secondary_y=False, row=2, col=1, range=[0, 100])
        fig.update_yaxes(title_text="Price", secondary_y=True, row=2, col=1, showgrid=False)


        # 4. Price and Trades (Using optimized portfolio if available, else basic)
        plot_pf = opt_portfolio if opt_portfolio else basic_portfolio
        plot_name = "Optimized" if opt_portfolio else "Basic"
        fig.add_trace(go.Scatter(x=price_data.index, y=price_data['close'], mode='lines', name=f'{plot_name} Price', line=dict(color='black')), row=2, col=2)
        if hasattr(plot_pf, 'trades') and plot_pf.trades.count() > 0:
            try:
                trades = plot_pf.trades.records_arr
                entry_idx = trades['entry_idx'][trades['entry_idx'] < len(price_data)]
                exit_idx = trades['exit_idx'][trades['exit_idx'] < len(price_data)]

                fig.add_trace(go.Scatter(x=price_data.index[entry_idx], y=price_data['close'].iloc[entry_idx],
                                         mode='markers', name=f'{plot_name} Entries', marker=dict(symbol='triangle-up', size=8, color='green')), row=2, col=2)
                fig.add_trace(go.Scatter(x=price_data.index[exit_idx], y=price_data['close'].iloc[exit_idx],
                                         mode='markers', name=f'{plot_name} Exits', marker=dict(symbol='triangle-down', size=8, color='red')), row=2, col=2)
            except Exception as trade_plot_err:
                 logger.warning(f"Could not plot trades: {trade_plot_err}")

        # 5. Daily Returns (Bar Chart)
        daily_ret = basic_portfolio.returns * 100 # Percentage
        colors = ['green' if r >= 0 else 'red' for r in daily_ret]
        fig.add_trace(go.Bar(x=daily_ret.index, y=daily_ret, name='Basic Daily Ret (%)', marker_color=colors), row=3, col=1)
        # Add MA of returns? (Optional, might clutter bar chart)
        # returns_ma = basic_portfolio.returns.rolling(7).mean() * 100
        # fig.add_trace(go.Scatter(x=returns_ma.index, y=returns_ma.values, mode='lines', name='7-day MA', line=dict(color='orange', width=1)), row=3, col=1)


        # 6. Monthly Returns Heatmap
        try:
            # Calculate monthly returns matrix manually using pandas
            monthly_returns = basic_portfolio.returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
            # Create year and month columns for pivoting
            monthly_returns.index = pd.to_datetime(monthly_returns.index)
            df_monthly = pd.DataFrame({'returns': monthly_returns})
            df_monthly['year'] = df_monthly.index.year
            df_monthly['month'] = df_monthly.index.month
            # Pivot to get Year x Month matrix
            monthly_returns_matrix = df_monthly.pivot(index='year', columns='month', values='returns')
            monthly_returns_matrix *= 100 # Convert to percentage
            monthly_returns_matrix = monthly_returns_matrix.fillna(0) # Fill NaNs for missing months
            
            # Ensure columns are 1-12
            monthly_returns_matrix = monthly_returns_matrix.reindex(columns=range(1, 13), fill_value=0)
            
            fig.add_trace(go.Heatmap(
                z=monthly_returns_matrix.values,
                x=monthly_returns_matrix.columns, # Months (1-12)
                y=monthly_returns_matrix.index,   # Years
                colorscale='RdYlGn',
                colorbar=dict(title='Return %'),
                text=[[f"{val:.2f}%" for val in row] for row in monthly_returns_matrix.values],
                hoverinfo='text',
                zmin=-15, # Adjust color scale limits as needed
                zmax=15
            ), row=3, col=2)
            # Set month names for x-axis ticks
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=month_names, row=3, col=2)

        except Exception as heatmap_err:
             logger.warning(f"Could not generate monthly heatmap: {heatmap_err}", exc_info=True)


        # 7. Strategy Metrics Table
        metrics_data = {
            'Metric': ['Total Return (%)', 'Annual Return (%)', 'Sharpe Ratio', 'Sortino Ratio', 'Max Drawdown (%)', 'Win Rate (%)', 'Profit Factor', 'Total Trades'],
            'Basic': [f"{basic_metrics['total_return']*100:.2f}", f"{basic_metrics['annual_return']*100:.2f}", f"{basic_metrics['sharpe']:.2f}", f"{basic_metrics['sortino']:.2f}", f"{basic_metrics['max_dd']*100:.2f}", f"{basic_metrics['win_rate']*100:.2f}", f"{basic_metrics['profit_factor']:.2f}", f"{basic_metrics['trades']}"]
        }
        if opt_metrics:
            metrics_data['Optimized'] = [f"{opt_metrics['total_return']*100:.2f}", f"{opt_metrics['annual_return']*100:.2f}", f"{opt_metrics['sharpe']:.2f}", f"{opt_metrics['sortino']:.2f}", f"{opt_metrics['max_dd']*100:.2f}", f"{opt_metrics['win_rate']*100:.2f}", f"{opt_metrics['profit_factor']:.2f}", f"{opt_metrics['trades']}"]

        fig.add_trace(go.Table(
            header=dict(values=list(metrics_data.keys()), fill_color='blue', font=dict(color='white'), align='left'),
            cells=dict(values=list(metrics_data.values()), fill_color='lightblue', align='left')),
            row=4, col=1
        )

        # 8. Optimization Heatmap (Example: Sharpe Ratio)
        if opt_results and 'param_perf' in opt_results:
             try:
                 # Use the DataFrame before reset_index, with parameters in index
                 param_perf_df = opt_results['all_portfolios'].stats(agg_func=None)
                 optimize_metric_col = opt_results.get('optimize_metric', 'Sharpe Ratio') # Get the metric used

                 # Check if required index levels and metric column exist
                 required_levels = ['rsi_window', 'rsi_lower_th'] # Focus on these two for 2D heatmap
                 if all(level in param_perf_df.index.names for level in required_levels) and optimize_metric_col in param_perf_df.columns:

                      # Create pivot table for heatmap (average over other params if needed)
                      # Use mean() to aggregate over rsi_upper_th if present
                      heatmap_data = pd.pivot_table(
                          param_perf_df,
                          values=optimize_metric_col,
                          index='rsi_window',
                          columns='rsi_lower_th'
                          # aggfunc=np.mean # Use mean if multiple upper_th exist for same window/lower_th
                      )
                      heatmap_data = heatmap_data.sort_index(axis=0).sort_index(axis=1) # Sort for clarity
                      
                      fig.add_trace(go.Heatmap(
                          z=heatmap_data.values,
                          x=heatmap_data.columns,
                          y=heatmap_data.index,
                          colorscale='RdYlGn',
                          colorbar=dict(title=optimize_metric_col),
                          text=[[f"{val:.3f}" for val in row] for row in heatmap_data.values],
                          hoverinfo='text'
                      ), row=4, col=2)
                      # Update axes for heatmap
                      fig.update_xaxes(title_text='Lower Threshold', type='category', row=4, col=2)
                      fig.update_yaxes(title_text='Window Size', type='category', row=4, col=2)
                 else:
                      missing = [l for l in required_levels if l not in param_perf_df.index.names]
                      if optimize_metric_col not in param_perf_df.columns:
                           missing.append(optimize_metric_col + " (column)")
                      logger.warning(f"Optimization results DataFrame missing expected levels/columns for heatmap: {missing}")
                      fig.add_trace(go.Table(cells=dict(values=[['Heatmap data structure error']])), row=4, col=2)

             except Exception as opt_heatmap_err:
                  logger.warning(f"Could not generate optimization heatmap: {opt_heatmap_err}", exc_info=True)
                  fig.add_trace(go.Table(cells=dict(values=[['Heatmap generation error']])), row=4, col=2)
        else:
             # Add placeholder text if no optimization heatmap
              fig.add_trace(go.Table(cells=dict(values=[['Optimization results not available']])), row=4, col=2)


        # Update layout
        param_info = f" // Basic: W={results.get('window', 'N/A')}, L={results.get('lower_threshold', 'N/A')}, U={results.get('upper_threshold', 'N/A')}"
        if opt_results and opt_results.get('best_params'):
             bp = opt_results['best_params']
             param_info += f" // Opt: W={bp.get('rsi_window','N/A')}, L={bp.get('rsi_lower_th','N/A')}, U={bp.get('rsi_upper_th','N/A')}"

        fig.update_layout(
            title=f"VectorBT Pro RSI Strategy Dashboard - {symbol} ({start_date} to {end_date}){param_info}",
            height=1200, width=1400, showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            yaxis1_title="Cum. Return", yaxis2_title="Drawdown (%)",
            yaxis3_title="RSI", yaxis4_title="Price",
            yaxis5_title="Daily Ret (%)", yaxis6_title="Month",
            xaxis7_visible=False, yaxis7_visible=False, # Hide axes for table
            # xaxis8_title="Lower Threshold" if 'rsi_lower' in opt_results.get('param_perf', pd.DataFrame()).columns else "Param Value", # Invalid axis number
            # yaxis8_title="Window", # Invalid axis number
            xaxis1_rangeslider_visible=False,
            xaxis2_rangeslider_visible=False,
            xaxis3_rangeslider_visible=False,
            xaxis4_rangeslider_visible=False,
            xaxis5_rangeslider_visible=False,
            xaxis6_rangeslider_visible=False,
        )

        # Save dashboard
        dashboard_filename = f"vbtpro_rsi_dashboard_{symbol.replace('-', '_')}.html"
        dashboard_file = reports_dir / dashboard_filename
        fig.write_html(str(dashboard_file), include_plotlyjs='cdn', full_html=True)
        logger.info(f"Dashboard saved to: {dashboard_file}")
        return str(dashboard_file)

    except Exception as e:
        logger.error(f"Error creating dashboard: {e}", exc_info=True)
        return None


# --- Strategy Definition using IndicatorFactory ---

# --- Start of Edit: Restore RSI+BB --- 
# NEW: Combined RSI + Bollinger Bands Function
def rsi_bb_func(close, rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std):
    """ 
    Calculates RSI and Bollinger Bands, generates combined entry/exit signals.
    Entry: RSI crosses below lower threshold AND Close crosses below lower BB.
    Exit: RSI crosses above upper threshold OR Close crosses above middle BB.
    """
    logger.debug(f"Running rsi_bb_func: RSI_W={rsi_window}, L={rsi_lower_th}, U={rsi_upper_th}, BB_W={bb_window}, STD={bb_std}")
    
    # Calculate Indicators
    rsi = vbt.RSI.run(close, window=rsi_window, short_name='RSI').rsi
    bb = vbt.BBANDS.run(close, window=bb_window, alpha=bb_std, short_name='BB') # alpha corresponds to std devs

    # Entry Signal: RSI Oversold AND Price Below Lower Band
    rsi_entry_signal = rsi.vbt.crossed_below(rsi_lower_th)
    bb_entry_signal = close.vbt.crossed_below(bb.lower)
    entries = rsi_entry_signal & bb_entry_signal

    # Exit Signal: RSI Overbought OR Price Above Middle Band
    rsi_exit_signal = rsi.vbt.crossed_above(rsi_upper_th)
    bb_exit_signal = close.vbt.crossed_above(bb.middle) # Exit when price reverts to mean
    exits = rsi_exit_signal | bb_exit_signal
    
    raw_entries_count = entries.sum()
    raw_exits_count = exits.sum()
    logger.debug(f"  RSI ({rsi_window}) + BB ({bb_window}, {bb_std}) Signals: Entries={raw_entries_count}, Exits={raw_exits_count}")

    # Ensure we return boolean Series
    entries = entries.astype(bool)
    exits = exits.astype(bool)
    
    # Return indicators and signals
    return rsi, bb.lower, bb.middle, bb.upper, entries, exits

# Create Indicator Factory for the new strategy
RSIBBStrategyFactory = vbt.IndicatorFactory(
    class_name='RSIBBStrategy',       # Changed class name
    short_name='rsi_bb',              # Changed short name
    input_names=['close'],
    param_names=['rsi_window', 'rsi_lower_th', 'rsi_upper_th', 'bb_window', 'bb_std'], # Added BB params
    output_names=['rsi', 'bb_lower', 'bb_middle', 'bb_upper', 'entries', 'exits']      # Added BB outputs
).with_apply_func(rsi_bb_func) # Use the new combined function
# --- End of Edit ---


# --- Main Execution Logic ---

def run_backtest(
    symbol, start_date, end_date, granularity=86400,
    initial_capital=10000, commission_pct=0.001, slippage_pct=0.0005,
    param_grid=None, optimize_metric='sharpe_ratio',
    use_stops=True,
    sl_atr_multiplier=1.0, tsl_atr_multiplier=1.0,
    wfo_test_days=180, wfo_window_years=2
):
    """
    Manual WFO: Optimizes RSI + Bollinger Band params, IS, tests OOS using FIXED stops.
    """
    logger.info(f"--- Running Manual WFO (Optimizing RSI + BB, Fixed Stops) for {symbol} ---") # Updated title
    logger.info(f"Period: {start_date} to {end_date} | Granularity: {granularity}s")
    logger.info(f"Portfolio Settings: IC={initial_capital}, Comm={commission_pct*100:.3f}%, Slip={slippage_pct*100:.3f}% | Stops Enabled={use_stops}")
    logger.info(f"Fixed Stop Params: SL ATR Mult={sl_atr_multiplier}, TSL ATR Mult={tsl_atr_multiplier}")
    logger.info(f"WFO Params: Test Days={wfo_test_days}, Window Years={wfo_window_years}")

    full_price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if full_price_data is None or full_price_data.empty: return None, None, None

    # Define Parameter Grid (RSI and Trend Filter)
    if param_grid is None:
        # --- Start of Edit: Correct Parameter Grid for Basic RSI ---
        # Revert to RSI+BB Grid
        param_grid = {
            'rsi_window': np.arange(10, 21, 5),  # 10, 15, 20
            'rsi_lower_th': np.arange(25, 41, 5), # 25, 30, 35, 40
            'rsi_upper_th': np.arange(60, 76, 5),  # 60, 65, 70, 75
            'bb_window': np.arange(15, 31, 5),     # 15, 20, 25, 30
            'bb_std': np.arange(1.5, 3.1, 0.5)      # 1.5, 2.0, 2.5, 3.0
            # Remove BB params
            # 'bb_window': np.arange(15, 31, 5), # 15, 20, 25, 30
            # 'bb_std': np.arange(1.5, 3.1, 0.5) # 1.5, 2.0, 2.5, 3.0
        }
        # --- End of Edit ---
    logger.info(f"Optimization Parameter Grid: {param_grid}")
    param_names_ordered = list(param_grid.keys())
    logger.info(f"Parameter Order for Optimization: {param_names_ordered}")

    metric_map = {'sharpe ratio': 'sharpe_ratio', 'total return': 'total_return', 'max drawdown': 'max_drawdown'}
    vbt_metric = metric_map.get(optimize_metric.lower(), 'sharpe_ratio')
    higher_better = vbt_metric not in ['max_drawdown']
    logger.info(f"Using '{vbt_metric}' as optimization metric (higher_better={higher_better}).")

    logger.info("Manually calculating split indices...")
    n_total = len(full_price_data); window_len = int(wfo_window_years * 365.25)
    test_len = wfo_test_days; train_len = window_len - test_len
    if train_len <= 0 or window_len > n_total: return None, None, full_price_data
    split_indices = []
    current_start = 0
    while current_start + window_len <= n_total:
        train_start = current_start; train_end = current_start + train_len
        test_start = train_end; test_end = min(current_start + window_len, n_total)
        if test_start >= test_end: break
        split_indices.append((np.arange(train_start, train_end), np.arange(test_start, test_end)))
        current_start += test_len
    n_splits = len(split_indices)
    if n_splits == 0: return None, None, full_price_data
    logger.info(f"Manual calculation generated {n_splits} splits.")

    oos_results_sharpe = {}; oos_results_return = {}; oos_results_drawdown = {}
    best_params_history = {}

    logger.info("Starting Walk-Forward Iteration (Manual Indices)...")
    for i, (train_idx, test_idx) in enumerate(tqdm(split_indices, total=n_splits, desc="WFO Splits")):
        in_price_split = full_price_data.iloc[train_idx]
        out_price_split = full_price_data.iloc[test_idx]
        if in_price_split.empty or out_price_split.empty: continue

        # 1. Optimize on In-Sample Data (No longer pass fixed long_sma_window)
        in_performance = simulate_all_params_single_split(
            in_price_split, param_grid, initial_capital,
            commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
            vbt_metric,
            higher_better=higher_better
        )
        if in_performance is None: continue
        if in_performance.empty: continue

        # 2. Find Best Parameters Index (tuple)
        best_index_split = get_best_index(in_performance, higher_better=higher_better)
        if best_index_split is None: continue

        # 3. Create Best Parameters Dict
        if isinstance(best_index_split, tuple) and len(best_index_split) == len(param_names_ordered):
            best_params_split = dict(zip(param_names_ordered, best_index_split))
            # --- Add Logging Here ---
            try:
                best_is_performance = in_performance.loc[best_index_split]
                logger.debug(f"Split {i}: Best Params IS -> {best_params_split} | IS Performance ({vbt_metric}): {best_is_performance:.4f}")
            except Exception as log_err:
                logger.warning(f"Split {i}: Could not log IS performance for best params {best_params_split}: {log_err}")
            # --- End Logging ---
        else: 
            logger.warning(f"Split {i}: Best index {best_index_split} is not a tuple or length mismatch with params {param_names_ordered}. Skipping.")
            continue
        best_params_history[i] = best_params_split

        # 4. Test Best Parameters on Out-of-Sample Data (No longer pass fixed long_sma_window)
        oos_metrics_dict = simulate_best_params_single_split(
            out_price_split, best_params_split, initial_capital,
            commission_pct, slippage_pct,
            use_stops, sl_atr_multiplier, tsl_atr_multiplier,
        )
        oos_results_sharpe[i] = oos_metrics_dict.get('sharpe_ratio', np.nan)
        oos_results_return[i] = oos_metrics_dict.get('total_return', np.nan)
        oos_results_drawdown[i] = oos_metrics_dict.get('max_drawdown', np.nan)

    logger.info("Walk-Forward Iteration Complete.")
    # ... (Aggregate and Prepare Final Results - update title/description) ...
    if not best_params_history: return None, None, full_price_data
    oos_sharpe_series = pd.Series(oos_results_sharpe).sort_index(); oos_return_series = pd.Series(oos_results_return).sort_index(); oos_drawdown_series = pd.Series(oos_results_drawdown).sort_index()
    oos_mean_sharpe = oos_sharpe_series.mean(); oos_std_sharpe = oos_sharpe_series.std()
    oos_mean_return = oos_return_series.mean(); oos_std_return = oos_return_series.std()
    oos_mean_drawdown = oos_drawdown_series.mean(); oos_std_drawdown = oos_drawdown_series.std()
    logger.info("--- Final Aggregated OOS Performance (RSI + BB, Fixed Stops) ---") # Updated Title
    logger.info(f"Fixed Stop Params: SL={sl_atr_multiplier}, TSL={tsl_atr_multiplier}")
    logger.info(f"Chosen Optimization Metric: {vbt_metric}")
    logger.info(f"Sharpe Ratio  : Mean={oos_mean_sharpe:.4f}, Std={oos_std_sharpe:.4f}")
    logger.info(f"Total Return  : Mean={oos_mean_return:.4f}, Std={oos_std_return:.4f}")
    logger.info(f"Max Drawdown  : Mean={oos_mean_drawdown:.4f}, Std={oos_std_drawdown:.4f}")
    wfo_results_dict = {
        'optimized_metric': vbt_metric,
        'fixed_sl_atr_multiplier': sl_atr_multiplier,
        'fixed_tsl_atr_multiplier': tsl_atr_multiplier,
        'best_params_per_split': best_params_history,
        'oos_sharpe': oos_sharpe_series.to_dict(), 'oos_return': oos_return_series.to_dict(), 'oos_drawdown': oos_drawdown_series.to_dict(),
        'oos_mean_sharpe': oos_mean_sharpe, 'oos_std_sharpe': oos_std_sharpe,
        'oos_mean_return': oos_mean_return, 'oos_std_return': oos_std_return,
        'oos_mean_drawdown': oos_mean_drawdown, 'oos_std_drawdown': oos_std_drawdown,
    }
    return None, wfo_results_dict, full_price_data

# --- WFO Helper Function: Simulate All Parameters (Using Fixed Stop Args) ---
def simulate_all_params_single_split(price_data, param_grid, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier, metric='sharpe_ratio', higher_better=True):
    """
    Simulates RSI+BB param combinations on a SINGLE split, using fixed stop settings.
    """
    logger.debug(f"Simulating RSI+BB params (fixed stops) on single split data shape: {price_data.shape}")
    close = price_data['close']; high = price_data['high']; low = price_data['low']
    all_entries = []; all_exits = []; all_params = []
    param_names = list(param_grid.keys()); param_values = list(param_grid.values())
    param_combinations = list(product(*param_values)); total_combs = len(param_combinations)
    if total_combs == 0: return None
    
    # Re-introduce ATR calculation
    atr = None
    if use_stops:
        try: 
            atr = vbt.ATR.run(high, low, close, window=14).atr
            logger.debug(f"Split ATR calculated: Mean={atr.mean():.4f}, Max={atr.max():.4f}")
        except Exception: 
            logger.warning(f"Could not calculate ATR for split, disabling stops for this split.")
            use_stops = False # Disable stops if ATR fails
    
    # Calculate ATR-based stops if possible
    sl_stop_pct = None; tsl_stop_pct = None
    if use_stops and atr is not None:
        if sl_atr_multiplier > 0: sl_stop_pct = (atr * sl_atr_multiplier) / close
        if tsl_atr_multiplier > 0: tsl_stop_pct = (atr * tsl_atr_multiplier) / close
        if sl_stop_pct is not None: logger.debug(f"Calculated SL Stop Pct: Mean={sl_stop_pct.mean():.4%}, Max={sl_stop_pct.max():.4%}")
        if tsl_stop_pct is not None: logger.debug(f"Calculated TSL Stop Pct: Mean={tsl_stop_pct.mean():.4%}, Max={tsl_stop_pct.max():.4%}")

    # Loop through RSI parameter combinations
    for params_tuple in param_combinations:
        current_params = dict(zip(param_names, params_tuple))
        all_params.append(current_params)
        # Extract all parameters for the rsi_bb_func call
        rsi_window = int(current_params['rsi_window'])
        rsi_lower_th = float(current_params['rsi_lower_th'])
        rsi_upper_th = float(current_params['rsi_upper_th'])
        bb_window = int(current_params['bb_window'])
        bb_std = float(current_params['bb_std'])
        try:
            # Call the correct function with all required params
            rsi, bb_lower, bb_middle, bb_upper, entries, exits = rsi_bb_func(
                close, rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std
            )
            logger.debug(f"  Params {params_tuple}: RSI+BB Entries={entries.sum()}, Exits={exits.sum()}")
            all_entries.append(entries); all_exits.append(exits)
        except Exception: all_entries.append(pd.Series(False, index=close.index)); all_exits.append(pd.Series(False, index=close.index))

    # Combine signals ---
    if not all_entries: return None
    param_multi_index = pd.MultiIndex.from_tuples([tuple(p.values()) for p in all_params], names=param_names)
    try:
         entries_output = pd.concat(all_entries, axis=1, keys=param_multi_index)
         exits_output = pd.concat(all_exits, axis=1, keys=param_multi_index)
    except Exception as concat_err:
        logger.error(f"Simulate_all_single: Error combining signals: {concat_err}")
        return None

    # Run Portfolio Simulation ---
    try:
        # Pass ATR-based stop Series (or None)
        pf = vbt.Portfolio.from_signals(
            close=close, entries=entries_output, exits=exits_output,
            freq='1D', init_cash=initial_capital, fees=commission_pct, slippage=slippage_pct,
            sl_stop=sl_stop_pct,
            tsl_stop=tsl_stop_pct,
            group_by=True
        )
        perf = getattr(pf, metric, None)
        if perf is None: return pd.Series(np.nan, index=param_multi_index)
        if isinstance(perf, (int, float)): perf = pd.Series(perf, index=param_multi_index)
        elif not isinstance(perf, pd.Series): perf = pd.Series(np.nan, index=param_multi_index)
        if not perf.index.equals(param_multi_index): perf = perf.reindex(param_multi_index)
        sorted_perf = perf.sort_values(ascending=not higher_better)
        top_5 = sorted_perf.head(5)
        logger.debug(f"  Top 5 IS Param Sets ({metric}):")
        for idx, val in top_5.items():
            logger.debug(f"    Params: {dict(zip(param_names, idx))} -> {metric}: {val:.4f}")
        return perf
    except Exception as pf_err:
        logger.error(f"Simulate_all_single: Error during portfolio sim: {pf_err}", exc_info=True)
        return None

# --- WFO Helper Function: Simulate Best Parameters (Using Fixed Stop Args) ---
def simulate_best_params_single_split(price_data, best_params_dict, initial_capital, commission_pct, slippage_pct, use_stops, sl_atr_multiplier, tsl_atr_multiplier):
    """
    Simulates the single best RSI+BB param set on a SINGLE split, using fixed stop settings."
    logger.debug(f"Simulating best RSI+BB params (fixed stops) on single split data shape: {price_data.shape}") # Updated docstring
    close = price_data['close']; high = price_data['high']; low = price_data['low']
    logger.debug(f"Split Price Data Stats:\n{price_data[['open', 'high', 'low', 'close', 'volume']].describe()}")
    
    # Extract all parameters from the best_params_dict
    rsi_window = int(best_params_dict['rsi_window'])
    rsi_lower_th = float(best_params_dict['rsi_lower_th'])
    rsi_upper_th = float(best_params_dict['rsi_upper_th'])
    bb_window = int(best_params_dict['bb_window'])
    bb_std = float(best_params_dict['bb_std'])

    try:
        # Call the correct function with all required params
        rsi, bb_lower, bb_middle, bb_upper, entries, exits = rsi_bb_func(
            close, rsi_window, rsi_lower_th, rsi_upper_th, bb_window, bb_std
        )
        logger.debug(f"Best Params {best_params_dict}: Signals -> RSI+BB Entries={entries.sum()}, Exits={exits.sum()}")
    except Exception: entries = pd.Series(False, index=close.index); exits = pd.Series(False, index=close.index)
    
    # Re-introduce ATR calculation for the single best run
    sl_stop_pct = None; tsl_stop_pct = None
    atr = None # Define atr here
    if use_stops:
        try:
             # Use a common ATR window (e.g., 14)
             atr = vbt.ATR.run(high, low, close, window=14).atr
             if sl_atr_multiplier > 0: sl_stop_pct = (atr * sl_atr_multiplier) / close
             if tsl_atr_multiplier > 0: tsl_stop_pct = (atr * tsl_atr_multiplier) / close
             if atr is not None: logger.debug(f"Split Best Params ATR: Mean={atr.mean():.4f}, Max={atr.max():.4f}")
             if sl_stop_pct is not None: logger.debug(f"Split Best Params SL Stop Pct: Mean={sl_stop_pct.mean():.4%}, Max={sl_stop_pct.max():.4%}")
             if tsl_stop_pct is not None: logger.debug(f"Split Best Params TSL Stop Pct: Mean={tsl_stop_pct.mean():.4%}, Max={tsl_stop_pct.max():.4%}")
        except Exception:
            logger.warning("Could not calculate ATR for best param split, running without stops.")
            pass # Proceed without stops if ATR fails

    # --- Add Detailed Logging Before Simulation ---
    logger.debug(f"->>> Pre-Simulation Check for Split (Params: {best_params_dict})")
    logger.debug(f"     Price Data Shape: {price_data.shape}")
    logger.debug(f"     Price Data Index Range: {price_data.index.min()} to {price_data.index.max()}")
    logger.debug(f"     Entries Sum: {entries.sum()}")
    logger.debug(f"     Exits Sum: {exits.sum()}")
    if atr is not None:
        logger.debug(f"     ATR Stats: Mean={atr.mean():.4f}, Max={atr.max():.4f}, Min={atr.min():.4f}, NaNs={atr.isna().sum()}")
    else:
        logger.debug("     ATR: Not calculated or failed.")
    if sl_stop_pct is not None:
        logger.debug(f"     SL Stop Pct Stats: Mean={sl_stop_pct.mean():.4%}, Max={sl_stop_pct.max():.4%}, Min={sl_stop_pct.min():.4%}, NaNs={sl_stop_pct.isna().sum()}")
        logger.debug(f"     Sample SL Stop Pct values (first 5 non-NaN): {sl_stop_pct.dropna().head().tolist()}")
    else:
        logger.debug("     SL Stop Pct: Not calculated or not used.")
    if tsl_stop_pct is not None:
        logger.debug(f"     TSL Stop Pct Stats: Mean={tsl_stop_pct.mean():.4%}, Max={tsl_stop_pct.max():.4%}, Min={tsl_stop_pct.min():.4%}, NaNs={tsl_stop_pct.isna().sum()}")
        logger.debug(f"     Sample TSL Stop Pct values (first 5 non-NaN): {tsl_stop_pct.dropna().head().tolist()}")
    else:
        logger.debug("     TSL Stop Pct: Not calculated or not used.")
    logger.debug(f"->>> Calling Portfolio.from_signals...")

    pf = vbt.Portfolio.from_signals(
        close, 
        entries, 
        exits, 
        freq='1D', 
        init_cash=initial_capital, 
        fees=commission_pct, 
        slippage=slippage_pct, 
        sl_stop=sl_stop_pct, # Pass ATR-based stop Series (or None)
        tsl_stop=tsl_stop_pct # Pass ATR-based stop Series (or None)
    )
    stats = pf.stats()
    logger.debug(f"Raw pf.stats() for split: {stats}") # Log the entire stats dict
    metrics_dict = {
        'sharpe_ratio': stats.get('Sharpe Ratio', np.nan),
        'total_return': stats.get('Total Return [%]', np.nan) / 100.0,
        'max_drawdown': stats.get('Max Drawdown [%]', np.nan) / 100.0
    }
    logger.debug(f"Finished simulate_best_single. Metrics: {metrics_dict}")
    return metrics_dict

# --- WFO Helper Functions: Get Best Index (No changes needed here) ---
def get_best_index(performance, higher_better=True):
    """Find best performing parameters index."""
    if performance is None or performance.empty:
        logger.warning("Get_best_index: Performance data is empty.")
        return None
    try:
        # Handle potential all-NaN series
        if not performance.notna().any():
            logger.warning("Get_best_index: Performance data contains only NaNs.")
            return None 
            
        if higher_better:
            return performance.idxmax()
        else:
            return performance.idxmin()
    except Exception as e:
        logger.error(f"Error getting best index: {e}")
        return None

# --- Main function ---
def main():
    # Set root logger level to DEBUG to capture detailed logs
    logging.getLogger().setLevel(logging.DEBUG)
    # Configure vectorbtpro logger specifically if needed
    # logging.getLogger('vectorbtpro').setLevel(logging.INFO) # Example: Keep VBT logs less verbose
    parser = argparse.ArgumentParser(description='Backtest RSI strategy using VectorBT Pro with Manual WFO (Optimizing Stops).')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1d', help='Data granularity (1d only supported)')
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--optimize_metric', type=str, default='Sharpe Ratio', help='Metric to optimize for IS')
    parser.add_argument('--no_stops', action='store_true', help='Disable stop loss usage globally')
    parser.add_argument('--sl_atr', type=float, default=3.5, help='ATR multiplier for stop loss')
    parser.add_argument('--tsl_atr', type=float, default=3.5, help='ATR multiplier for trailing stop loss')
    parser.add_argument('--reports_dir', type=str, default='reports', help='Directory to save reports')
    parser.add_argument('--wfo_test_days', type=int, default=90, help='Days in OOS test set') 
    parser.add_argument('--wfo_window_years', type=float, default=2.0, help='Total years in each rolling window')
    args = parser.parse_args()
    granularity_map = {'1d': 86400}; granularity_seconds = granularity_map.get(args.granularity.lower())
    if granularity_seconds is None: logger.error("Use '1d' granularity."); sys.exit(1)
    reports_path = Path(args.reports_dir); reports_path.mkdir(parents=True, exist_ok=True)

    _, wfo_results, _ = run_backtest(
        symbol=args.symbol, start_date=args.start_date, end_date=args.end_date,
        granularity=granularity_seconds, initial_capital=args.initial_capital,
        commission_pct=args.commission, slippage_pct=args.slippage, param_grid=None, 
        optimize_metric=args.optimize_metric, use_stops=(not args.no_stops),
        sl_atr_multiplier=args.sl_atr,
        tsl_atr_multiplier=args.tsl_atr,
        wfo_test_days=args.wfo_test_days, wfo_window_years=args.wfo_window_years
    )

    if wfo_results:
        logger.info("--- Manual WFO (Fixed Stops, Trend Filter) Results Summary ---")
        logger.info(f"Optimization Metric Used: {wfo_results.get('optimized_metric', 'N/A')}")
        logger.info(f"Fixed Stop Params: SL={wfo_results.get('fixed_sl_atr_multiplier','N/A')}, TSL={wfo_results.get('fixed_tsl_atr_multiplier','N/A')}")
        logger.info(f"OOS Sharpe Ratio: Mean={wfo_results.get('oos_mean_sharpe', np.nan):.4f}, Std={wfo_results.get('oos_std_sharpe', np.nan):.4f}")
        logger.info(f"OOS Total Return: Mean={wfo_results.get('oos_mean_return', np.nan):.4f}, Std={wfo_results.get('oos_std_return', np.nan):.4f}")
        logger.info(f"OOS Max Drawdown: Mean={wfo_results.get('oos_mean_drawdown', np.nan):.4f}, Std={wfo_results.get('oos_std_drawdown', np.nan):.4f}")
        try:
            # Update filename to remove specific SMA, SL, TSL values since SMA is optimized and stops are fixed
            save_path = reports_path / f"manual_wfo_fixed_stops_results_{args.symbol}_SL{args.sl_atr}_TSL{args.tsl_atr}.json"
            results_to_save = {}
            results_to_save['optimized_metric'] = wfo_results.get('optimized_metric')
            results_to_save['fixed_sl_atr_multiplier'] = args.sl_atr
            results_to_save['fixed_tsl_atr_multiplier'] = args.tsl_atr
            for metric_key in ['oos_sharpe', 'oos_return', 'oos_drawdown']:
                 if metric_key in wfo_results:
                     results_to_save[metric_key] = {str(k): (None if pd.isna(v) else v) for k, v in wfo_results[metric_key].items()}
                 else: results_to_save[metric_key] = {}
            if 'best_params_per_split' in wfo_results:
                 results_to_save['best_params_per_split'] = {str(k): {p_name: (int(p_val) if isinstance(p_val, np.integer) else float(p_val)) for p_name, p_val in params.items()} for k, params in wfo_results['best_params_per_split'].items()}
            else: results_to_save['best_params_per_split'] = {}
            for metric_key in ['oos_mean_sharpe', 'oos_std_sharpe', 'oos_mean_return', 'oos_std_return', 'oos_mean_drawdown', 'oos_std_drawdown']:
                 results_to_save[metric_key] = None if pd.isna(wfo_results.get(metric_key)) else wfo_results.get(metric_key)

            with open(save_path, 'w') as f: json.dump(results_to_save, f, indent=2)
            logger.info(f"WFO results saved to {save_path}")
            plot_metric = wfo_results.get('optimized_metric', 'sharpe_ratio')
            plot_metric_key = f'oos_{plot_metric}'
            if plot_metric_key in wfo_results and wfo_results[plot_metric_key]:
                 try:
                      plot_series = pd.Series(wfo_results[plot_metric_key]).sort_index()
                      if not plot_series.empty:
                           # Update plot title and filename
                           plot_title = f"OOS {plot_metric} per Split (Basic RSI, ATR Stops SL={args.sl_atr} TSL={args.tsl_atr})"
                           fig = plot_series.vbt.plot(title=plot_title)
                           plot_path = reports_path / f"manual_wfo_basic_rsi_atr_stops_oos_{plot_metric}_{args.symbol}_SL{args.sl_atr}_TSL{args.tsl_atr}.html"
                           fig.write_html(str(plot_path)); logger.info(f"OOS {plot_metric} plot saved to {plot_path}")
                 except Exception as plot_err: logger.warning(f"Could not plot OOS {plot_metric}: {plot_err}")
        except Exception as save_err: logger.error(f"Error saving/plotting WFO: {save_err}")
    else:
        # Update warning message
        logger.warning("Manual WFO (Optimized Trend Filter, Fixed Stops) did not produce results.")
    logger.info("--- Backtest Script Finished ---")

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
    main() 