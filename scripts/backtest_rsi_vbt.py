import vectorbtpro as vbt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import logging
import sys
import os
import json
from datetime import datetime, timedelta
from typing import Tuple, Dict, List, Optional
from pathlib import Path

# Add project root to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.coinbase import CoinbaseClient
from types import SimpleNamespace

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RSIMomentumVBT:
    def __init__(self, params=None):
        # Initialize default parameters with improved values
        self.params = {
            'rsi_period': 14,
            'oversold_threshold': 30,
            'overbought_threshold': 70,
            'fast_sma_period': 10,
            'slow_sma_period': 50,
            'volume_ma_period': 20,
            'atr_period': 14,
            'fee_rate': 0.001,
            'initial_capital': 10000,
            'risk_per_trade': 0.02,  # 2% risk per trade
            'sl_atr_multiplier': 2.0,  # Stop loss ATR multiplier
            'tp_atr_multiplier': 4.0,  # Take profit ATR multiplier (2:1 reward-risk)
            'trend_ema_period': 200,   # Long-term trend filter
            'volume_threshold': 1.5,    # Volume must be 1.5x average for entry
            'rsi_trend_period': 100,    # RSI trend analysis period
            'min_bounces': 2,          # Minimum RSI bounces for support/resistance
            'rsi_divergence_period': 14 # Period for RSI divergence calculation
        }
        
        # Update with provided parameters
        if params is not None:
            self.params.update(params)

    def run(self, data):
        # Calculate indicators
        close = data['close']
        high = data['high']
        low = data['low']
        volume = data['volume']
        
        # Set consistent fill method for NaN values
        close = close.ffill()
        volume = volume.fillna(0)
        
        # Calculate RSI with Pro features - removed chunked parameter as it's causing issues
        rsi = vbt.RSI.run(
            close, 
            window=self.params['rsi_period']
        ).rsi
        
        # Calculate RSI trend
        rsi_trend = vbt.RSI.run(
            close,
            window=self.params['rsi_trend_period']
        ).rsi
        
        # Calculate RSI divergence
        price_change = close.pct_change(self.params['rsi_divergence_period'])
        rsi_change = rsi.diff(self.params['rsi_divergence_period'])
        bullish_divergence = (price_change < 0) & (rsi_change > 0)
        bearish_divergence = (price_change > 0) & (rsi_change < 0)
        
        # Calculate Moving Averages with Pro features
        fast_sma = vbt.MA.run(
            close, 
            window=self.params['fast_sma_period']
        ).ma
        
        slow_sma = vbt.MA.run(
            close, 
            window=self.params['slow_sma_period']
        ).ma
        
        trend_ema = vbt.MA.run(
            close,
            window=self.params['trend_ema_period'],
            ewm=True  # Use EMA for trend
        ).ma
        
        # Volume analysis
        volume_ma = vbt.MA.run(
            volume,
            window=self.params['volume_ma_period']
        ).ma
        
        volume_signal = volume > (volume_ma * self.params['volume_threshold'])
        
        # ATR for volatility-based position sizing
        atr = vbt.ATR.run(
            high,
            low,
            close,
            window=self.params['atr_period']
        ).atr
        
        # Advanced entry conditions
        oversold_condition = rsi < self.params['oversold_threshold']
        bullish_trend = (fast_sma > slow_sma) & (close > trend_ema)
        rsi_support_bounce = (rsi > rsi.rolling(window=20).min()) & (rsi < 40)
        
        # Entry signals
        entry = (
            # Primary RSI condition
            oversold_condition &
            # Trend confirmation
            bullish_trend &
            # Volume confirmation
            volume_signal &
            # Additional confirmations (any of these)
            (
                bullish_divergence |  # Bullish divergence
                rsi_support_bounce |  # RSI bouncing from support
                (rsi_trend > rsi_trend.shift(1))  # RSI trend improving
            )
        )
        
        # Advanced exit conditions
        overbought_condition = rsi > self.params['overbought_threshold']
        bearish_trend = (fast_sma < slow_sma) & (close < trend_ema)
        rsi_resistance_hit = (rsi < rsi.rolling(window=20).max()) & (rsi > 60)
        
        # Exit signals
        exit = (
            # Primary RSI condition
            overbought_condition |
            # Trend break
            bearish_trend |
            # Additional confirmations (any of these)
            (
                bearish_divergence |  # Bearish divergence
                rsi_resistance_hit |  # RSI hitting resistance
                (rsi_trend < rsi_trend.shift(1))  # RSI trend deteriorating
            )
        )
        
        # Dynamic position sizing based on ATR and volatility
        volatility_factor = 1 / (atr / close).rolling(window=20).std()
        volatility_factor = volatility_factor.clip(0.5, 2.0)  # Limit position size adjustment
        
        base_position_size = (self.params['initial_capital'] * self.params['risk_per_trade']) / (atr * close)
        position_size = base_position_size * volatility_factor
        
        # Risk management stops based on ATR
        sl_stop = self.params['sl_atr_multiplier'] * (atr / close)
        tp_stop = self.params['tp_atr_multiplier'] * (atr / close)
        
        # Backtest the strategy with Pro features - removed chunked parameter
        portfolio = vbt.Portfolio.from_signals(
            close,
            entry,
            exit,
            size=position_size,  # Dynamic position sizing
            fees=self.params['fee_rate'],
            freq='1D',
            init_cash=self.params['initial_capital'],
            sl_stop=sl_stop,  # Dynamic stop loss
            tp_stop=tp_stop,  # Dynamic take profit
            sl_trail=True    # Pro feature: Trailing stop loss
        )
        
        return portfolio

def optimize_strategy(data, param_grid):
    """
    Optimize strategy parameters using VectorBT Pro.
    
    Args:
        data (pd.DataFrame): Historical OHLCV data
        param_grid (dict): Dictionary of parameter ranges to test
        
    Returns:
        dict: Best performing parameters
    """
    logger.info(f"Starting parameter optimization with enhanced criteria")
    
    # Create combinations manually due to VectorBT Pro API changes
    # Generate parameter combinations using pandas approach
    params_list = []
    
    # Core RSI parameters
    rsi_periods = param_grid.get('rsi_period', [14])
    oversold_thresholds = param_grid.get('oversold_threshold', [30])
    overbought_thresholds = param_grid.get('overbought_threshold', [70])
    
    # Moving average parameters
    fast_sma_periods = param_grid.get('fast_sma_period', [10])
    slow_sma_periods = param_grid.get('slow_sma_period', [50])
    
    # Generate valid combinations
    for rsi_period in rsi_periods:
        for oversold in oversold_thresholds:
            for overbought in overbought_thresholds:
                for fast_sma in fast_sma_periods:
                    for slow_sma in slow_sma_periods:
                        # Skip invalid combinations
                        if fast_sma >= slow_sma or oversold >= overbought:
                            continue
                            
                        params_list.append({
                            'rsi_period': rsi_period,
                            'oversold_threshold': oversold,
                            'overbought_threshold': overbought,
                            'fast_sma_period': fast_sma,
                            'slow_sma_period': slow_sma
                        })
    
    logger.info(f"Testing {len(params_list)} parameter combinations")
    
    if len(params_list) == 0:
        logger.error("No valid parameter combinations to test")
        return {}
    
    # Optimization function
    def run_strategy(params):
        try:
            strategy = RSIMomentumVBT(params)
            portfolio = strategy.run(data)
            
            # Calculate metrics
            metrics = vbt.Metrics.from_portfolio(portfolio)
            
            return {
                'total_return': metrics.total_return,
                'sharpe_ratio': metrics.sharpe_ratio,
                'sortino_ratio': metrics.sortino_ratio,
                'max_drawdown': metrics.max_drawdown,
                'win_rate': metrics.win_rate,
                'profit_factor': metrics.profit_factor,
                'num_trades': metrics.num_trades
            }
        except Exception as e:
            logger.error(f"Error with parameters {params}: {e}")
            return None
    
    # Run sequential optimization for stability
    results = []
    for params in params_list:
        result = run_strategy(params)
        if result is not None:
            results.append({**params, **result})
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Handle case with no valid results
    if len(results_df) == 0:
        logger.error("No valid parameter combinations found. Try with simpler parameters.")
        return {}
    
    # Find best parameters by total return for simplicity
    best_idx = results_df['total_return'].idxmax()
    best_params = results_df.iloc[best_idx].to_dict()
    
    # Log detailed optimization results
    logger.info("Optimization complete!")
    logger.info("\nBest Parameters:")
    for param, value in best_params.items():
        if param in param_grid:
            logger.info(f"{param}: {value}")
    
    logger.info("\nBest Metrics:")
    logger.info(f"Total Return: {best_params['total_return']:.2%}")
    logger.info(f"Sharpe Ratio: {best_params['sharpe_ratio']:.2f}")
    logger.info(f"Max Drawdown: {best_params['max_drawdown']:.2%}")
    logger.info(f"Win Rate: {best_params['win_rate']:.2%}")
    logger.info(f"Profit Factor: {best_params['profit_factor']:.2f}")
    logger.info(f"Number of Trades: {best_params['num_trades']}")
    
    # Create filtered best_params with only strategy parameters
    filtered_best_params = {k: v for k, v in best_params.items() 
                           if k in param_grid}
    
    return filtered_best_params

def fetch_historical_data(product_id, start_date_str, end_date_str, granularity):
    """
    Fetch historical price data for backtesting.
    
    Args:
        product_id (str): The product ID (e.g., "BTC-USD")
        start_date_str (str): Start date in format 'YYYY-MM-DD'
        end_date_str (str): End date in format 'YYYY-MM-DD'
        granularity (str): Time granularity (e.g., "ONE_DAY", "ONE_HOUR")
        
    Returns:
        pd.DataFrame: Historical data with OHLCV columns
    """
    try:
        # Load credentials
        logger.info("Loading credentials from cdp_api_key.json...")
        # Initialize REST client
        rest_client = None
        KEY_FILE_PATH = "cdp_api_key.json"
        try:
            if not os.path.exists(KEY_FILE_PATH):
                raise FileNotFoundError(f"Key file not found: {KEY_FILE_PATH}")
            with open(KEY_FILE_PATH, 'r') as f:
                key_data = json.load(f)
            api_key_name = key_data.get('name')
            private_key_pem = key_data.get('privateKey')
            if not api_key_name or not private_key_pem:
                raise ValueError("Key file missing 'name' or 'privateKey' field.")

            # Use SimpleNamespace as a lightweight settings object
            temp_settings = SimpleNamespace()
            temp_settings.COINBASE_JWT_KEY_NAME = api_key_name
            temp_settings.COINBASE_JWT_PRIVATE_KEY = private_key_pem
            temp_settings.COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage"

            rest_client = CoinbaseClient(temp_settings)
            logger.info("Coinbase RESTClient initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize REST client: {e}")
            return None
        
        # Construct cache filename
        cache_dir = Path("data/cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f"{product_id}_{granularity}_{start_date_str}_{end_date_str}.csv"
        
        # Check for cached data
        if cache_file.exists():
            logger.info(f"Loading cached data from: {cache_file}")
            df = pd.read_csv(cache_file)
            logger.info(f"Loaded {len(df)} data points from cache.")
            
            # Ensure all columns are lowercase
            df.columns = [col.lower() for col in df.columns]
            
            # Handle missing columns
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in required_cols:
                if col not in df.columns:
                    logger.warning(f"Missing column {col}, adding with placeholder values")
                    if col == 'volume':
                        df[col] = 0
                    else:
                        df[col] = df['close'] if 'close' in df.columns else 0
            
            # Set index and sort
            if 'time' in df.columns:
                df['time'] = pd.to_datetime(df['time'])
                df.set_index('time', inplace=True)
            
            return df
        
        # If not cached, fetch new data
        logger.info(f"Fetching new data for {product_id}...")
        
        # Convert date strings to datetime
        start_dt = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        # Fetch data
        # Code for fetching data from the API would go here
        # ...
        
        # For now, we'll raise an exception as we're working with cached data only
        raise NotImplementedError("Live data fetching not yet implemented, please use cached data")
        
    except Exception as e:
        logger.error(f"Failed to fetch or process data: {str(e)}")
        return None

def create_sample_data(start_date_str, end_date_str):
    """
    Create sample price data for backtesting when no cached data is available.
    
    Args:
        start_date_str (str): Start date in format 'YYYY-MM-DD'
        end_date_str (str): End date in format 'YYYY-MM-DD'
        
    Returns:
        pd.DataFrame: Sample historical data with OHLCV columns
    """
    logger.info("Creating sample BTC-USD price data for backtesting...")
    
    # Convert date strings to datetime
    start_dt = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    # Create date range
    date_range = pd.date_range(start=start_dt, end=end_dt, freq='D')
    
    # Seed for reproducibility
    np.random.seed(42)
    
    # Initial price and volatility
    initial_price = 20000.0
    volatility = 0.02
    
    # Generate random price movement with trend
    trend = 0.0002  # Slight upward bias
    returns = np.random.normal(trend, volatility, size=len(date_range))
    
    # Calculate price series
    price_series = initial_price * (1 + returns).cumprod()
    
    # Create OHLCV data
    df = pd.DataFrame(index=date_range)
    df['close'] = price_series
    df['high'] = price_series * (1 + np.random.uniform(0, 0.03, size=len(date_range)))
    df['low'] = price_series * (1 - np.random.uniform(0, 0.03, size=len(date_range)))
    df['open'] = price_series * (1 + np.random.uniform(-0.01, 0.01, size=len(date_range)))
    
    # Generate volume data (correlated with price changes)
    mean_volume = 2000
    df['volume'] = mean_volume * (1 + 5 * np.abs(returns)) * (1 + np.random.uniform(-0.5, 1.5, size=len(date_range)))
    
    # Add some spikes and dips to make it more realistic
    for i in range(5):
        spike_idx = np.random.randint(20, len(date_range) - 20)
        spike_duration = np.random.randint(3, 7)
        spike_magnitude = np.random.uniform(0.05, 0.15) * (-1 if np.random.random() < 0.5 else 1)
        
        for j in range(spike_duration):
            idx = min(spike_idx + j, len(date_range) - 1)
            df.iloc[idx, 0:4] = df.iloc[idx, 0:4] * (1 + spike_magnitude * (1 - j/spike_duration))
    
    logger.info(f"Created sample data with {len(df)} days of price data")
    
    return df

def test_rsi_strategy(data, window=14, wtype="wilder", lower_th=30, upper_th=70):
    """
    Simple RSI strategy: 
    - Enter when RSI crosses below lower_th
    - Exit when RSI crosses above upper_th
    
    Args:
        data (pd.DataFrame): OHLCV data
        window (int): RSI window length
        wtype (str): Type of smoothing for RSI ('wilder', 'simple', 'exp')
        lower_th (int): Lower RSI threshold for entry signals
        upper_th (int): Upper RSI threshold for exit signals
        
    Returns:
        vbt.Portfolio: Portfolio with backtest results
    """
    # Use open price for signals and close price for execution
    open_price = data['open']
    close_price = data['close']
    
    # Calculate RSI on open price
    rsi = vbt.RSI.run(open_price, window=window, wtype=wtype)
    
    # Generate entry/exit signals
    entries = rsi.rsi_crossed_below(lower_th)
    exits = rsi.rsi_crossed_above(upper_th)
    
    # Create portfolio
    portfolio = vbt.Portfolio.from_signals(
        close=close_price,
        entries=entries,
        exits=exits,
        size=100,  # Buy $100 worth of asset
        size_type='value',
        init_cash='auto',
        fees=0.001  # 0.1% trading fee
    )
    
    return portfolio

def optimize_rsi_strategy(data):
    """
    Optimize RSI strategy parameters using vectorized backtesting.
    
    Args:
        data (pd.DataFrame): OHLCV data
        
    Returns:
        tuple: (best_params, stats_df)
    """
    logger.info("Running RSI strategy optimization")
    
    # Use smaller parameter set for quicker testing
    windows = [7, 14, 21]
    wtypes = ["wilder"]
    lower_ths = [20, 25, 30]
    upper_ths = [70, 75, 80]
    
    # Use open price for signals and close price for execution
    open_price = data['open']
    close_price = data['close']
    
    logger.info(f"Testing combinations of RSI parameters: windows={windows}, lower_ths={lower_ths}, upper_ths={upper_ths}")
    
    # Run individual backtests instead of vectorized approach
    from itertools import product
    results = []
    
    for window, wtype, lower_th, upper_th in product(windows, wtypes, lower_ths, upper_ths):
        # Skip invalid combinations
        if lower_th >= upper_th:
            continue
            
        params = (window, wtype, lower_th, upper_th)
        logger.info(f"Testing parameters: {params}")
        
        try:
            # Run backtest with these parameters
            pf = test_rsi_strategy(data, window=window, wtype=wtype, lower_th=lower_th, upper_th=upper_th)
            
            # Get stats
            stats = pf.stats()
            
            # Extract key metrics
            metrics = {}
            metrics['window'] = window
            metrics['wtype'] = wtype
            metrics['lower_th'] = lower_th
            metrics['upper_th'] = upper_th
            
            # Extract common metrics with error handling
            try:
                metrics['total_return'] = stats.loc['Total Return [%]'] / 100 if 'Total Return [%]' in stats.index else stats.loc['Return [%]'] / 100 
                metrics['sharpe'] = stats.loc['Sharpe Ratio'] if 'Sharpe Ratio' in stats.index else 0
                metrics['sortino'] = stats.loc['Sortino Ratio'] if 'Sortino Ratio' in stats.index else 0
                metrics['max_dd'] = stats.loc['Max Drawdown [%]'] / 100 if 'Max Drawdown [%]' in stats.index else 0
                metrics['win_rate'] = stats.loc['Win Rate [%]'] / 100 if 'Win Rate [%]' in stats.index else 0
                metrics['num_trades'] = stats.loc['# Trades'] if '# Trades' in stats.index else 0
                
                # Calculate expectancy as our optimization target
                avg_win = stats.loc['Avg Winning Trade [%]'] / 100 if 'Avg Winning Trade [%]' in stats.index else 0
                avg_loss = stats.loc['Avg Losing Trade [%]'] / 100 if 'Avg Losing Trade [%]' in stats.index else 0
                metrics['expectancy'] = (metrics['win_rate'] * avg_win) - ((1 - metrics['win_rate']) * abs(avg_loss))
                
                results.append(metrics)
            except Exception as e:
                logger.error(f"Error extracting metrics for {params}: {e}")
                logger.info(f"Available stats: {stats}")
                
        except Exception as e:
            logger.error(f"Error testing parameters {params}: {e}")
    
    # Convert results to DataFrame
    if not results:
        logger.error("No valid results found during optimization")
        return (14, "wilder", 30, 70), None
        
    results_df = pd.DataFrame(results)
    
    # Find best parameters by expectancy
    best_idx = results_df['expectancy'].idxmax()
    best_params = (
        int(results_df.loc[best_idx, 'window']),
        results_df.loc[best_idx, 'wtype'],
        int(results_df.loc[best_idx, 'lower_th']),
        int(results_df.loc[best_idx, 'upper_th'])
    )
    
    # Create multi-index DataFrame for heatmap visualization
    try:
        multi_idx = pd.MultiIndex.from_tuples(
            [(row['lower_th'], row['upper_th']) for _, row in results_df.iterrows()],
            names=['lower_th', 'upper_th']
        )
        stats_df = pd.DataFrame(
            results_df['expectancy'].values,
            index=multi_idx,
            columns=['expectancy']
        )
    except Exception as e:
        logger.error(f"Error creating multi-index DataFrame: {e}")
        stats_df = results_df
    
    # Log optimization results
    logger.info(f"Optimization complete, tested {len(results_df)} combinations")
    logger.info(f"Best parameters: window={best_params[0]}, wtype={best_params[1]}, "
                f"lower_th={best_params[2]}, upper_th={best_params[3]}")
    logger.info(f"Best expectancy: {results_df.loc[best_idx, 'expectancy']:.4f}")
    logger.info(f"Best total return: {results_df.loc[best_idx, 'total_return']:.2%}")
    
    return best_params, stats_df

def main():
    # Test parameters
    product_id_to_test = "BTC-USD"
    start_date = "2022-01-01"
    end_date = "2023-12-31"
    granularity = "ONE_DAY"
    
    logger.info(f"Starting RSI backtest for {product_id_to_test} from {start_date} to {end_date}")
    
    # Get historical data or create sample data
    data = fetch_historical_data(product_id_to_test, start_date, end_date, granularity)
    if data is None:
        logger.info("No cached data available, creating sample data for testing")
        data = create_sample_data(start_date, end_date)
    
    try:
        # 1. Run basic RSI strategy with default parameters
        logger.info("Running basic RSI strategy with default parameters")
        portfolio = test_rsi_strategy(data)
        
        # Display basic results
        stats = portfolio.stats()
        logger.info("\n=== Basic RSI Strategy Results ===")
        
        # Access metrics safely
        try:
            # Log the stats index for debugging
            logger.info(f"Available metrics: {stats.index.tolist()}")
            
            # Total return
            if 'Total Return [%]' in stats.index:
                total_return = stats.loc['Total Return [%]'] / 100
                logger.info(f"Total Return: {total_return:.2%}")
            elif 'Return [%]' in stats.index:
                total_return = stats.loc['Return [%]'] / 100
                logger.info(f"Total Return: {total_return:.2%}")
            
            # Sharpe ratio
            if 'Sharpe Ratio' in stats.index:
                sharpe = stats.loc['Sharpe Ratio']
                logger.info(f"Sharpe Ratio: {sharpe:.2f}")
            
            # Max drawdown
            if 'Max Drawdown [%]' in stats.index:
                max_dd = stats.loc['Max Drawdown [%]'] / 100
                logger.info(f"Max Drawdown: {max_dd:.2%}")
            
            # Win rate
            if 'Win Rate [%]' in stats.index:
                win_rate = stats.loc['Win Rate [%]'] / 100
                logger.info(f"Win Rate: {win_rate:.2%}")
            
            # Number of trades - use Total Trades if available
            if 'Total Trades' in stats.index:
                total_trades = int(stats.loc['Total Trades'])
                logger.info(f"Total Trades: {total_trades}")
            
        except Exception as e:
            logger.error(f"Error extracting metrics: {e}")
        
        # Plot basic strategy results
        try:
            fig = portfolio.plot()
            fig.write_html('rsi_strategy_results.html')
            logger.info("Strategy plot saved as 'rsi_strategy_results.html'")
        except Exception as e:
            logger.error(f"Error generating plot: {e}")
        
        # Run parameter optimization with a reduced parameter set
        logger.info("\nRunning parameter optimization")
        best_params, stats_df = optimize_rsi_strategy(data)
        
        if best_params and stats_df is not None:
            # Unpack parameters
            window, wtype, lower_th, upper_th = best_params
            
            # Run optimized strategy
            logger.info(f"Running optimized strategy with parameters: window={window}, type={wtype}, lower_threshold={lower_th}, upper_threshold={upper_th}")
            opt_portfolio = test_rsi_strategy(
                data, 
                window=window, 
                wtype=wtype, 
                lower_th=lower_th, 
                upper_th=upper_th
            )
            
            # Display optimized results
            opt_stats = opt_portfolio.stats()
            logger.info("\n=== Optimized RSI Strategy Results ===")
            
            # Access metrics safely
            try:
                # Total return
                if 'Total Return [%]' in opt_stats.index:
                    total_return = opt_stats.loc['Total Return [%]'] / 100
                    logger.info(f"Total Return: {total_return:.2%}")
                elif 'Return [%]' in opt_stats.index:
                    total_return = opt_stats.loc['Return [%]'] / 100
                    logger.info(f"Total Return: {total_return:.2%}")
                
                # Sharpe ratio
                if 'Sharpe Ratio' in opt_stats.index:
                    sharpe = opt_stats.loc['Sharpe Ratio']
                    logger.info(f"Sharpe Ratio: {sharpe:.2f}")
                
                # Max drawdown
                if 'Max Drawdown [%]' in opt_stats.index:
                    max_dd = opt_stats.loc['Max Drawdown [%]'] / 100
                    logger.info(f"Max Drawdown: {max_dd:.2%}")
                
                # Win rate
                if 'Win Rate [%]' in opt_stats.index:
                    win_rate = opt_stats.loc['Win Rate [%]'] / 100
                    logger.info(f"Win Rate: {win_rate:.2%}")
                
                # Number of trades - use Total Trades if available
                if 'Total Trades' in opt_stats.index:
                    total_trades = int(opt_stats.loc['Total Trades'])
                    logger.info(f"Total Trades: {total_trades}")
                
            except Exception as e:
                logger.error(f"Error extracting optimized metrics: {e}")
            
            # Plot optimized strategy results
            try:
                opt_fig = opt_portfolio.plot()
                opt_fig.write_html('rsi_optimized_strategy_results.html')
                logger.info("Optimized strategy plot saved as 'rsi_optimized_strategy_results.html'")
            except Exception as e:
                logger.error(f"Error generating optimized plot: {e}")
        
        logger.info("\nBacktest completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during backtesting: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main() 