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

def rsi_func(close, window, lower_th, upper_th):
    """Calculates RSI and generates basic entry/exit signals."""
    rsi = vbt.RSI.run(close, window=window, wtype='wilder').rsi # Using wilder RSI
    # Use standard VBT crossing methods
    entries = rsi.vbt.crossed_below(lower_th)
    exits = rsi.vbt.crossed_above(upper_th)
    # Return RSI along with signals
    return rsi, entries, exits

# Create Indicator Factory
RSIStrategyFactory = vbt.IndicatorFactory(
    class_name='RSIStrategy',
    short_name='rsi',
    input_names=['close'],
    param_names=['window', 'lower_th', 'upper_th'],
    output_names=['rsi', 'entries', 'exits'] # Added 'rsi' to outputs
).with_apply_func(rsi_func)


# --- Main Execution Logic ---

def run_backtest(symbol, start_date, end_date, granularity=86400,
                 initial_capital=10000, commission_pct=0.001, slippage_pct=0.0005,
                 param_grid=None, optimize_metric='Sharpe Ratio', min_trades=5, # Changed default metric name to match VBT output
                 use_stops=True, sl_atr_multiplier=2.0, tsl_atr_multiplier=1.5):
    """
    Runs the backtest with optimization using VBT Pro features.
    """
    logger.info(f"--- Running VBT Pro Backtest for {symbol} ---")
    logger.info(f"Period: {start_date} to {end_date} | Granularity: {granularity}s")
    logger.info(f"Initial Capital: {initial_capital} | Commission: {commission_pct*100:.3f}% | Slippage: {slippage_pct*100:.3f}%")

    # Fetch Data
    price_data = fetch_historical_data(symbol, start_date, end_date, granularity)
    if price_data is None or price_data.empty:
        logger.error("Failed to fetch or generate price data. Exiting.")
        return None, None, None

    # Prepare data for VBT
    close = price_data['close']
    high = price_data['high']
    low = price_data['low']

    # Define Parameter Grid for Optimization
    if param_grid is None:
        param_grid = {
            'window': np.arange(7, 25, 3),        # RSI Windows: 7, 10, 13, 16, 19, 22
            'lower_th': np.arange(20, 45, 5),     # Lower Th: 20, 25, 30, 35, 40
            'upper_th': np.arange(60, 85, 5),     # Upper Th: 60, 65, 70, 75, 80
        }
    logger.info(f"Optimization Parameter Grid: {param_grid}")

    # Instantiate RSI Strategy Factory
    rsi_indicator = RSIStrategyFactory.run(
        close,
        window=param_grid['window'],
        lower_th=param_grid['lower_th'],
        upper_th=param_grid['upper_th'],
        param_product=True # Test all combinations
    )

    # --- Portfolio Simulation with Optimization and Pro Features ---
    logger.info("Running portfolio simulation across parameter combinations...")

    # Calculate Stops (ATR based) if required
    stop_loss_price = None
    trailing_stop_loss_price = None
    if use_stops:
        atr = vbt.ATR.run(high, low, close, window=14).atr # Use a fixed ATR window for stops
        if sl_atr_multiplier > 0:
             stop_loss_pct = (atr * sl_atr_multiplier) / close
             stop_loss_price = stop_loss_pct # VBT takes percentage
             logger.info(f"Using ATR ({sl_atr_multiplier}x) based Stop Loss.")
        if tsl_atr_multiplier > 0:
             trailing_stop_loss_pct = (atr * tsl_atr_multiplier) / close
             trailing_stop_loss_price = trailing_stop_loss_pct # VBT takes percentage
             logger.info(f"Using ATR ({tsl_atr_multiplier}x) based Trailing Stop Loss.")


    # Run portfolio simulation across all parameter combinations
    # VBT Pro automatically aligns parameters from the indicator factory
    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=rsi_indicator.entries,
        exits=rsi_indicator.exits,
        freq='1D', # Adapt if granularity changes significantly
        init_cash=initial_capital,
        fees=commission_pct,
        slippage=slippage_pct,
        sl_stop=stop_loss_price,         # Use calculated stop loss percentages
        # tp_stop=tp_price,            # Take profit can be added similarly
        tsl_stop=trailing_stop_loss_price, # Use calculated trailing stop loss percentages
        # size=position_size,          # Can add dynamic sizing based on ATR or other logic here
        # size_type='targetpercent',   # Example size type
        # group_by='rsi_group',        # Removed: Let VBT handle grouping based on factory params
        # use_stats=True               # Removed: Not a valid argument
    )

    # --- Analyze Optimization Results ---
    if portfolio.trades.count().sum() == 0:
        logger.warning("No trades were executed across all parameter combinations.")
        return None, None, price_data # Return price data for potential dashboard

    # Filter results based on minimum trades
    valid_trades_mask = portfolio.trades.count() >= min_trades
    if not valid_trades_mask.any():
         logger.warning(f"No parameter combination resulted in >= {min_trades} trades.")
         # Optionally, return the unfiltered portfolio if you still want analysis
         # return portfolio, None, price_data
         return None, None, price_data


    # Access performance metrics for each parameter combination
    performance_metrics = portfolio.stats(agg_func=None) # Don't aggregate, get per-column stats

    # Select the best parameters based on the chosen metric
    # Ensure the metric exists in the stats output (which is now the columns)
    if optimize_metric not in performance_metrics.columns:
         logger.error(f"Optimization metric '{optimize_metric}' not found in portfolio stats columns. Available: {performance_metrics.columns.tolist()}")
         # Fallback to Sharpe Ratio if available
         if 'Sharpe Ratio' in performance_metrics.columns:
              optimize_metric = 'Sharpe Ratio'
              logger.warning(f"Falling back to optimizing for 'Sharpe Ratio'.")
         else:
              logger.error("Cannot determine best parameters. Exiting optimization analysis.")
              return None, None, price_data # Return None for results


    # Find the best combination (handle NaN, inf)
    # Select the column for the metric, resulting in a Series indexed by parameter combinations
    metric_values = performance_metrics[optimize_metric].replace([np.inf, -np.inf], np.nan).dropna()
    
    if metric_values.empty:
        logger.warning(f"No valid values found for optimization metric '{optimize_metric}' after filtering.")
        return None, None, price_data

    best_idx = metric_values.idxmax() # Find index (parameter combination tuple) of best metric value
    # Access the row corresponding to the best parameter index
    best_performance = performance_metrics.loc[best_idx]
    
    # Extract best parameters from the multi-index 'best_idx'
    # The names are in the index of the performance_metrics DataFrame
    # The multi-index created by VBT uses the factory param names
    best_params = dict(zip(performance_metrics.index.names, best_idx))

    logger.info(f"--- Optimization Complete ---")
    logger.info(f"Best Parameters ({optimize_metric}={best_performance[optimize_metric]:.4f}): {best_params}")
    # Log other metrics for the best row (Series)
    best_metrics_series = best_performance[best_performance.index != optimize_metric]
    logger.info(f"Best Performance Metrics:\n{best_metrics_series}")

    # --- Prepare Results ---
    # Portfolio for the best parameters
    # Portfolio columns are also indexed by the parameter tuples
    best_portfolio = portfolio[best_idx]

    # Get RSI indicator for the best parameters
    # rsi_indicator columns should match portfolio columns
    best_rsi_indicator = rsi_indicator[best_idx]

    # Structure basic_results around the single best portfolio
    basic_results = {
        'portfolio': best_portfolio,
        # Access the RSI output from the factory result
        'rsi_indicator': best_rsi_indicator.rsi,
        'lower_threshold': best_params.get('lower_th'),
        'upper_threshold': best_params.get('upper_th'),
        'window': best_params.get('window'),
    }

    # DataFrame for dashboard heatmap (parameters as index, metrics as columns)
    # No transpose needed now
    param_perf_for_dashboard = performance_metrics
    # Ensure index names match parameter names derived from best_params keys
    # Note: The performance_metrics index might already have names from the factory
    if isinstance(performance_metrics.index, pd.MultiIndex):
        param_perf_for_dashboard.index.names = list(best_params.keys())
    
    optimization_summary = {
        'best_params': best_params,
        'best_metrics': calculate_risk_metrics(best_portfolio),
        'portfolio': best_portfolio,
        # Use the original DataFrame (parameters in index) for the dashboard heatmap
        'param_perf': param_perf_for_dashboard.reset_index(),
        'all_portfolios': portfolio, # Keep the full portfolio object
        'optimize_metric': optimize_metric # Pass the metric used for optimization
    }

    return basic_results, optimization_summary, price_data


def main():
    parser = argparse.ArgumentParser(description='Backtest RSI strategy using VectorBT Pro.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2022-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1d', help='Data granularity (e.g., 1m, 5m, 1h, 1d)')
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--optimize_metric', type=str, default='Sharpe Ratio', help='Metric to optimize for')
    parser.add_argument('--min_trades', type=int, default=5, help='Min trades for valid optimization result')
    parser.add_argument('--no_stops', action='store_true', help='Disable stop loss and trailing stop loss')
    parser.add_argument('--sl_atr', type=float, default=2.0, help='ATR multiplier for stop loss (0 to disable)')
    parser.add_argument('--tsl_atr', type=float, default=1.5, help='ATR multiplier for trailing stop loss (0 to disable)')
    parser.add_argument('--dashboard', action='store_true', default=True, help='Generate interactive dashboard')
    parser.add_argument('--reports_dir', type=str, default='reports', help='Directory to save reports')

    args = parser.parse_args()

    # Map granularity string to seconds for Coinbase API
    granularity_map = {
        '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
        '1h': 3600, '2h': 7200, '6h': 21600, '12h': 43200,
        '1d': 86400
    }
    granularity_seconds = granularity_map.get(args.granularity.lower())
    if granularity_seconds is None:
        logger.error(f"Invalid granularity: {args.granularity}. Use one of {list(granularity_map.keys())}")
        sys.exit(1)
        
    # Make sure reports dir exists
    reports_path = Path(args.reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)


    # Run the backtest
    basic_results, opt_results, price_data = run_backtest(
        symbol=args.symbol,
        start_date=args.start_date,
        end_date=args.end_date,
        granularity=granularity_seconds,
        initial_capital=args.initial_capital,
        commission_pct=args.commission,
        slippage_pct=args.slippage,
        param_grid=None, # Use default grid in run_backtest
        optimize_metric=args.optimize_metric,
        min_trades=args.min_trades,
        use_stops=(not args.no_stops),
        sl_atr_multiplier=args.sl_atr,
        tsl_atr_multiplier=args.tsl_atr
    )

    # Generate dashboard if results are valid
    if args.dashboard and basic_results is not None and price_data is not None:
        create_dashboard(
            results=basic_results,
            opt_results=opt_results,
            price_data=price_data,
            symbol=args.symbol,
            start_date=args.start_date,
            end_date=args.end_date,
            reports_dir=reports_path
        )
    elif args.dashboard:
         logger.warning("Dashboard generation skipped due to invalid backtest results or missing price data.")

    logger.info("--- Backtest Script Finished ---")


if __name__ == "__main__":
    # Suppress specific warnings if needed
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=RuntimeWarning) # Often from NaNs in metrics
    main() 