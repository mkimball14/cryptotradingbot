import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import json
from datetime import datetime, timedelta
import time
import logging
from pathlib import Path
import vectorbtpro as vbt

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_historical_data(product_id, start_date, end_date, granularity=86400):
    """
    Fetch historical price data from Coinbase or from cache
    
    Parameters:
    -----------
    product_id : str
        The product ID (e.g., 'BTC-USD')
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    granularity : int
        Granularity in seconds (default: 86400 for daily)
        
    Returns:
    --------
    DataFrame
        Historical price data with columns: open, high, low, close, volume
    """
    # Create cache directory if it doesn't exist
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Define cache file path
    cache_file = cache_dir / f"{product_id.replace('-', '')}_{start_date}_{end_date}_{granularity}.csv"

    # Check sample data cache
    sample_cache = cache_dir / f"sample_{start_date}_{end_date}.csv"
    if sample_cache.exists():
        logger.info(f"Loading cached sample data from: {sample_cache}")
        try:
            data = pd.read_csv(sample_cache, index_col=0, parse_dates=True)
            return data
        except Exception as e:
            logger.warning(f"Error loading sample cache: {e}")
            
    # Try to load API credentials
    logger.info("Loading credentials from cdp_api_key.json...")
    if not os.path.exists("cdp_api_key.json"):
        logger.warning("Credentials file not found: cdp_api_key.json")
        logger.info("Generating sample data instead")
        return create_sample_data(start_date, end_date)

    # Generate sample data as we don't have actual API integration in this example
    logger.info("API integration not implemented - generating sample data")
    return create_sample_data(start_date, end_date)


def create_sample_data(start_date, end_date):
    """
    Create sample price data for backtesting when no real data is available.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        DataFrame with OHLCV data
    """
    logger.info(f"Creating sample BTC-USD price data for backtesting...")
    
    # Create directory for cached data if it doesn't exist
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if we have cached sample data
    cache_file = cache_dir / f"sample_{start_date}_{end_date}.csv"
    
    if cache_file.exists():
        logger.info(f"Loading cached sample data from: {cache_file}")
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            
            # Ensure all required columns exist
            if 'close' not in data.columns and 'Close' in data.columns:
                data['close'] = data['Close']
                data.drop('Close', axis=1, inplace=True, errors='ignore')
            
            # Check for missing OHLCV columns
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in data.columns for col in required_columns):
                logger.warning(f"Cached data missing required columns. Available columns: {data.columns}")
                logger.info("Regenerating sample data...")
                # Delete invalid cache file
                try:
                    cache_file.unlink()
                except:
                    pass
            else:
                logger.info(f"Loaded {len(data)} days of cached sample data")
                return data
        except Exception as e:
            logger.error(f"Error loading cached data: {e}")
    
    # Create date range
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    daterange = pd.date_range(start=start, end=end, freq='D')
    
    # Generate random price data with realistic properties
    np.random.seed(42)  # For reproducibility
    
    # Start with a price and add random changes
    price = 20000.0  # Starting price for BTC
    daily_volatility = 0.02  # 2% daily volatility
    
    prices = []
    for _ in range(len(daterange)):
        daily_return = np.random.normal(0.0002, daily_volatility)  # Slight upward drift
        price *= (1 + daily_return)
        prices.append(price)
    
    close_prices = pd.Series(prices, index=daterange)
    
    # Generate OHLCV data
    data = pd.DataFrame(index=daterange)
    data['close'] = close_prices
    data['high'] = data['close'] * (1 + np.random.uniform(0, 0.03, len(data)))
    data['low'] = data['close'] * (1 - np.random.uniform(0, 0.03, len(data)))
    data['open'] = data['close'].shift(1)
    
    # Handle first row
    data.loc[data.index[0], 'open'] = data.loc[data.index[0], 'close'] * 0.99
    
    # Add volume (proportional to price changes)
    price_changes = np.abs(data['close'].pct_change().fillna(0.01))
    base_volume = 1000  # Base volume in BTC
    data['volume'] = base_volume * (1 + 5 * price_changes)  # Higher volume on bigger price moves
    
    # Cache the generated data
    try:
        data.to_csv(cache_file)
        logger.info(f"Cached sample data to: {cache_file}")
    except Exception as e:
        logger.error(f"Error caching sample data: {e}")
    
    logger.info(f"Generated {len(data)} days of sample price data")
    return data


def run_rsi_strategy(data, rsi_window=14, rsi_lower=30, rsi_upper=70):
    """
    Run an RSI-based trading strategy.
    
    Parameters:
    -----------
    data : DataFrame
        OHLCV data
    rsi_window : int
        RSI lookback window
    rsi_lower : int
        RSI oversold threshold (buy when RSI below this value)
    rsi_upper : int
        RSI overbought threshold (sell when RSI above this value)
        
    Returns:
    --------
    dict
        Results containing portfolio, signals, etc.
    """
    logger.info(f"Running RSI strategy with window={rsi_window}, lower={rsi_lower}, upper={rsi_upper}")
    
    # Calculate RSI
    rsi = vbt.RSI.run(data['close'], window=rsi_window, short_name='rsi').rsi
    
    # Generate entry and exit signals
    entries = rsi < rsi_lower  # Buy when RSI is below lower threshold (oversold)
    exits = rsi > rsi_upper    # Sell when RSI is above upper threshold (overbought)
    
    # Create portfolio
    portfolio = vbt.Portfolio.from_signals(
        data['close'],
        entries,
        exits,
        fees=0.001,  # 0.1% fee
        freq='1D',
        init_cash=10000,  # Initial capital
        sl_stop=0.1,      # 10% stop loss
        tp_stop=0.2,      # 20% take profit
    )
    
    # Store results
    results = {
        'portfolio': portfolio,
        'entries': entries,
        'exits': exits,
        'rsi': rsi,
        'price_data': data,
        'params': {
            'rsi_window': rsi_window,
            'rsi_lower': rsi_lower,
            'rsi_upper': rsi_upper
        }
    }
    
    # Calculate risk metrics
    metrics = portfolio.stats()
    
    # Log key performance indicators
    logger.info(f"Total Return: {metrics['total_return']*100:.2f}%")
    logger.info(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    logger.info(f"Max Drawdown: {metrics['max_drawdown']*100:.2f}%")
    logger.info(f"Win Rate: {metrics['win_rate']*100:.2f}%")
    logger.info(f"# Trades: {metrics['total_trades']}")
    
    return results


def optimize_rsi_strategy(data, param_grid=None, min_trades=5, metric='sharpe_ratio'):
    """
    Optimize RSI strategy parameters using vectorbtpro.
    
    Parameters:
    -----------
    data : DataFrame
        OHLCV data
    param_grid : dict, optional
        Dictionary of parameter ranges to test
    min_trades : int, optional
        Minimum number of trades for a valid strategy
    metric : str, optional
        Metric to optimize ('sharpe_ratio', 'total_return', 'max_drawdown', etc.)
        
    Returns:
    --------
    dict
        Results including best parameters, metrics, etc.
    """
    logger.info(f"Optimizing RSI strategy parameters (optimizing for {metric})")
    
    # Check for valid data
    if data is None or len(data) < 30:
        logger.error("Insufficient data for optimization")
        return None
    
    # Define default parameter grid if none provided
    if param_grid is None:
        param_grid = {
            'rsi_window': range(5, 21, 2),        # RSI windows from 5 to 20
            'rsi_lower': range(20, 41, 5),        # Lower thresholds from 20 to 40
            'rsi_upper': range(60, 81, 5)         # Upper thresholds from 60 to 80
        }
    
    # Extract parameter combinations
    rsi_windows = param_grid.get('rsi_window', [14])
    rsi_lowers = param_grid.get('rsi_lower', [30])
    rsi_uppers = param_grid.get('rsi_upper', [70])
    
    logger.info(f"Testing {len(rsi_windows) * len(rsi_lowers) * len(rsi_uppers)} parameter combinations")
    
    # Initialize variables to track best parameters
    best_metric_value = -np.inf if metric != 'max_drawdown' else 0
    best_params = None
    best_portfolio = None
    best_metrics = None
    all_results = []
    
    # Loop through all parameter combinations
    for window in rsi_windows:
        for lower in rsi_lowers:
            for upper in rsi_uppers:
                # Skip invalid combinations (lower threshold must be < upper threshold)
                if lower >= upper:
                    continue
                
                # Run RSI strategy with current parameters
                try:
                    results = run_rsi_strategy(data, rsi_window=window, rsi_lower=lower, rsi_upper=upper)
                    
                    # Check if portfolio is valid
                    if results is None or 'portfolio' not in results:
                        logger.warning(f"Invalid results for window={window}, lower={lower}, upper={upper}")
                        continue
                    
                    portfolio = results['portfolio']
                    metrics = portfolio.stats()
                    
                    # Check if strategy has minimum number of trades
                    if metrics['total_trades'] < min_trades:
                        logger.info(f"Skipping params (window={window}, lower={lower}, upper={upper}) - too few trades: {metrics['total_trades']}")
                        continue
                    
                    # Store result
                    param_results = {
                        'params': {
                            'rsi_window': window,
                            'rsi_lower': lower,
                            'rsi_upper': upper
                        },
                        'metrics': metrics
                    }
                    all_results.append(param_results)
                    
                    # Update best parameters if current is better
                    metric_value = metrics[metric]
                    
                    # For drawdown, lower is better; for other metrics, higher is better
                    is_better = metric_value < best_metric_value if metric == 'max_drawdown' else metric_value > best_metric_value
                    
                    if best_params is None or is_better:
                        best_metric_value = metric_value
                        best_params = param_results['params']
                        best_metrics = metrics
                        best_portfolio = portfolio
                        
                        logger.info(f"New best parameters found: window={window}, lower={lower}, upper={upper}")
                        logger.info(f"Best {metric}: {best_metric_value}")
                    
                except Exception as e:
                    logger.error(f"Error running strategy with window={window}, lower={lower}, upper={upper}: {e}")
    
    if best_params is None:
        logger.warning("No valid parameter combination found")
        return None
    
    # Run the strategy with best parameters to get full results
    best_results = run_rsi_strategy(
        data, 
        rsi_window=best_params['rsi_window'], 
        rsi_lower=best_params['rsi_lower'], 
        rsi_upper=best_params['rsi_upper']
    )
    
    # Compile optimization results
    opt_results = {
        'best_params': best_params,
        'best_metrics': best_metrics,
        'best_portfolio': best_portfolio,
        'all_results': all_results
    }
    
    logger.info(f"Optimization complete. Best parameters: {best_params}")
    logger.info(f"Best {metric}: {best_metric_value}")
    
    return best_results


def create_dashboard(results, opt_results=None, symbol="BTC-USD", start_date=None, end_date=None, reports_dir="reports"):
    """
    Create an interactive dashboard for strategy analysis.
    
    Parameters:
    -----------
    results : dict
        Results from run_rsi_strategy
    opt_results : dict, optional
        Results from optimize_rsi_strategy
    symbol : str
        The trading symbol (e.g., BTC-USD)
    start_date : str
        Start date in format YYYY-MM-DD
    end_date : str
        End date in format YYYY-MM-DD
    reports_dir : str
        Directory to save reports
    
    Returns:
    --------
    str
        Path to the saved dashboard HTML file
    """
    try:
        # Create reports directory if it doesn't exist
        Path(reports_dir).mkdir(parents=True, exist_ok=True)
        
        # Check for valid portfolio data
        if results is None or 'portfolio' not in results:
            logger.error("Invalid results data for dashboard creation")
            return None
        
        portfolio = results['portfolio']
        
        # Calculate risk metrics for basic strategy
        metrics = portfolio.stats()
        
        # Create figure with subplots
        fig = make_subplots(
            rows=4, cols=2,
            vertical_spacing=0.05,
            horizontal_spacing=0.05,
            subplot_titles=(
                "Cumulative Returns", "Drawdowns",
                "RSI Indicator", "Monthly Returns Heatmap",
                "Daily Returns", "Trading Volume",
                "Strategy Statistics", "Optimized Parameters"
            ),
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "heatmap"}],
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "table"}, {"type": "table"}]
            ],
            row_heights=[0.3, 0.3, 0.3, 0.3]
        )
        
        # ---- 1. Cumulative Returns Plot ----
        fig.add_trace(
            go.Scatter(
                x=portfolio.cumulative_returns().index,
                y=portfolio.cumulative_returns().values,
                mode='lines',
                name='RSI Strategy',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
        
        # Add buy and sell markers for basic strategy
        entries = results['entries']
        exits = results['exits']
        price_data = results['price_data']
        
        # Get entry and exit points
        entry_points = price_data.index[entries]
        exit_points = price_data.index[exits]
        
        # Add entry markers (buys)
        fig.add_trace(
            go.Scatter(
                x=entry_points,
                y=[price_data['close'].loc[idx] for idx in entry_points if idx in price_data.index],
                mode='markers',
                marker=dict(symbol='triangle-up', size=10, color='green'),
                name='Buy Signal'
            ),
            row=1, col=1
        )
        
        # Add exit markers (sells)
        fig.add_trace(
            go.Scatter(
                x=exit_points,
                y=[price_data['close'].loc[idx] for idx in exit_points if idx in price_data.index],
                mode='markers',
                marker=dict(symbol='triangle-down', size=10, color='red'),
                name='Sell Signal'
            ),
            row=1, col=1
        )
        
        # ---- 2. Drawdowns Plot ----
        fig.add_trace(
            go.Scatter(
                x=portfolio.drawdowns.index,
                y=portfolio.drawdowns.values,
                mode='lines',
                name='Drawdowns',
                line=dict(color='red', width=1)
            ),
            row=1, col=2
        )
        
        # ---- 3. RSI Indicator ----
        fig.add_trace(
            go.Scatter(
                x=results['rsi'].index,
                y=results['rsi'].values,
                mode='lines',
                name='RSI',
                line=dict(color='purple', width=1)
            ),
            row=2, col=1
        )
        
        # Add RSI threshold lines
        rsi_lower = results['params']['rsi_lower']
        rsi_upper = results['params']['rsi_upper']
        
        fig.add_trace(
            go.Scatter(
                x=[results['rsi'].index[0], results['rsi'].index[-1]],
                y=[rsi_lower, rsi_lower],
                mode='lines',
                line=dict(color='green', width=1, dash='dash'),
                name=f'RSI Lower ({rsi_lower})'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=[results['rsi'].index[0], results['rsi'].index[-1]],
                y=[rsi_upper, rsi_upper],
                mode='lines',
                line=dict(color='red', width=1, dash='dash'),
                name=f'RSI Upper ({rsi_upper})'
            ),
            row=2, col=1
        )
        
        # ---- 4. Monthly Returns Heatmap ----
        monthly_returns = portfolio.returns.resample('M').sum().to_frame()
        monthly_returns.index = monthly_returns.index.strftime('%Y-%m')
        monthly_returns.columns = ['returns']
        monthly_pivot = pd.DataFrame({
            'year': [d.split('-')[0] for d in monthly_returns.index],
            'month': [d.split('-')[1] for d in monthly_returns.index],
            'returns': monthly_returns['returns'].values
        })
        
        monthly_pivot = monthly_pivot.pivot(index="year", columns="month", values="returns")
        
        months_order = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        monthly_pivot = monthly_pivot.reindex(columns=months_order)
        
        # Create heatmap
        fig.add_trace(
            go.Heatmap(
                z=monthly_pivot.values * 100,  # Convert to percentage
                x=monthly_pivot.columns,
                y=monthly_pivot.index,
                colorscale='RdYlGn',
                colorbar=dict(title='Return %'),
                text=np.round(monthly_pivot.values * 100, 1),
                texttemplate='%{text:.1f}%',
                name='Monthly Returns'
            ),
            row=2, col=2
        )
        
        # ---- 5. Daily Returns ----
        fig.add_trace(
            go.Scatter(
                x=portfolio.returns.index,
                y=portfolio.returns.values * 100,  # Convert to percentage
                mode='lines',
                name='Daily Returns',
                line=dict(color='teal', width=1)
            ),
            row=3, col=1
        )
        
        # ---- 6. Trading Volume ----
        fig.add_trace(
            go.Bar(
                x=price_data.index,
                y=price_data['volume'],
                name='Volume',
                marker=dict(color='rgba(0,0,255,0.3)')
            ),
            row=3, col=2
        )
        
        # ---- 7. Strategy Statistics Table ----
        metrics_to_display = {
            'Metric': [
                'Total Return', 'Annual Return', 'Sharpe Ratio', 
                'Sortino Ratio', 'Max Drawdown', 'Win Rate',
                'Profit Factor', 'Total Trades', 'Exposure Time'
            ],
            'Value': [
                f"{metrics['total_return']*100:.2f}%",
                f"{metrics['annual_return']*100:.2f}%",
                f"{metrics['sharpe_ratio']:.2f}",
                f"{metrics['sortino_ratio']:.2f}",
                f"{metrics['max_drawdown']*100:.2f}%",
                f"{metrics['win_rate']*100:.2f}%",
                f"{metrics['profit_factor']:.2f}",
                f"{metrics['total_trades']}",
                f"{metrics['exposure']*100:.2f}%"
            ]
        }
        
        fig.add_trace(
            go.Table(
                header=dict(
                    values=list(metrics_to_display.keys()),
                    font=dict(size=12, color='white'),
                    fill_color='blue',
                    align='left'
                ),
                cells=dict(
                    values=list(metrics_to_display.values()),
                    font=dict(size=11),
                    fill_color='lightblue',
                    align='left'
                )
            ),
            row=4, col=1
        )
        
        # ---- 8. Optimized Parameters Table (if available) ----
        if opt_results is not None and 'best_params' in opt_results:
            best_params = opt_results['best_params']
            params_display = {
                'Parameter': list(best_params.keys()),
                'Value': list(best_params.values())
            }
            
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=list(params_display.keys()),
                        font=dict(size=12, color='white'),
                        fill_color='green',
                        align='left'
                    ),
                    cells=dict(
                        values=list(params_display.values()),
                        font=dict(size=11),
                        fill_color='lightgreen',
                        align='left'
                    )
                ),
                row=4, col=2
            )
        
        # Update layout
        title_text = f"RSI Strategy Backtest: {symbol} ({start_date} to {end_date})"
        fig.update_layout(
            title=dict(
                text=title_text,
                y=0.99,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=20)
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            height=1600,
            width=1200,
            template="plotly_white"
        )
        
        # Save dashboard
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dashboard_file = f"{reports_dir}/{symbol}_{start_date}_{end_date}_dashboard_{timestamp}.html"
        
        fig.write_html(dashboard_file, include_mathjax=False)
        logger.info(f"Dashboard saved to: {dashboard_file}")
        
        return dashboard_file
        
    except Exception as e:
        logger.error(f"Error creating dashboard: {e}")
        return None


def main():
    # Get command line arguments
    parser = argparse.ArgumentParser(description='Backtest RSI momentum strategy.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='The trading symbol (e.g., BTC-USD)')
    parser.add_argument('--start_date', type=str, required=True, help='Start date in format YYYY-MM-DD')
    parser.add_argument('--end_date', type=str, required=True, help='End date in format YYYY-MM-DD')
    parser.add_argument('--optimize', action='store_true', help='Optimize strategy parameters')
    parser.add_argument('--dashboard', action='store_true', help='Create interactive dashboard')
    args = parser.parse_args()
    
    logger.info(f"Starting backtest for {args.symbol} from {args.start_date} to {args.end_date}")
    
    try:
        # Fetch historical data
        data = fetch_historical_data(args.symbol, args.start_date, args.end_date)
        if data is None or len(data) == 0:
            logger.error("Failed to fetch historical data")
            return
        
        logger.info(f"Fetched {len(data)} days of price data")
        
        # Run basic RSI strategy with default parameters
        results = run_rsi_strategy(data)
        
        # Print basic strategy metrics
        basic_metrics = results['portfolio'].stats()
        logger.info(f"Basic RSI Strategy Results:")
        logger.info(f"Total Return: {basic_metrics['total_return']*100:.2f}%")
        logger.info(f"Sharpe Ratio: {basic_metrics['sharpe_ratio']:.2f}")
        logger.info(f"Max Drawdown: {basic_metrics['max_drawdown']*100:.2f}%")
        
        # Optimize strategy if requested
        opt_results = None
        if args.optimize:
            logger.info("Optimizing RSI strategy parameters...")
            opt_results = run_rsi_strategy(
                data, 
                **optimize_rsi_strategy(data)['params']
            )
            
            # Print optimized strategy metrics
            opt_metrics = opt_results['portfolio'].stats()
            logger.info(f"Optimized RSI Strategy Results:")
            logger.info(f"Total Return: {opt_metrics['total_return']*100:.2f}%")
            logger.info(f"Sharpe Ratio: {opt_metrics['sharpe_ratio']:.2f}")
            logger.info(f"Max Drawdown: {opt_metrics['max_drawdown']*100:.2f}%")
        
        # Create dashboard if requested
        if args.dashboard:
            logger.info("Creating interactive dashboard...")
            dashboard_file = create_dashboard(
                results=results,
                opt_results=opt_results,
                symbol=args.symbol,
                start_date=args.start_date,
                end_date=args.end_date
            )
            logger.info(f"Dashboard created: {dashboard_file}")
        
        logger.info("Backtest completed successfully")
        
    except Exception as e:
        logger.error(f"Error during backtest: {e}")


if __name__ == "__main__":
    main() 