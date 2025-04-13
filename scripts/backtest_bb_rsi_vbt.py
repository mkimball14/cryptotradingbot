import vectorbt as vbt
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backtest_bb_rsi_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BollingerRSIVBT:
    def __init__(self, params=None):
        # Initialize default parameters
        self.params = {
            'bb_window': 20,           # Bollinger Bands window
            'bb_std': 2.0,             # Standard deviation multiplier
            'rsi_period': 14,          # RSI period
            'oversold_threshold': 30,  # RSI oversold threshold
            'overbought_threshold': 70, # RSI overbought threshold
            'volume_ma_period': 20,    # Volume moving average period
            'atr_period': 14,          # ATR period for volatility
            'fee_rate': 0.001,         # Trading fee rate
            'initial_capital': 10000   # Initial capital for backtest
        }
        
        # Update with provided parameters
        if params is not None:
            self.params.update(params)

    def run(self, data):
        # Calculate indicators
        close = data['close']
        volume = data['volume']
        
        # Set consistent fill method for NaN values
        close = close.ffill()
        volume = volume.fillna(0)
        
        # Calculate RSI
        rsi = vbt.RSI.run(close, window=self.params['rsi_period']).rsi
        rsi = rsi.fillna(50)  # Neutral value for RSI
        
        # Calculate Bollinger Bands
        bb = vbt.BBANDS.run(
            close, 
            window=self.params['bb_window'], 
            alpha=self.params['bb_std']
        )
        
        # Fill NaN values in Bollinger Bands - create filled versions instead of modifying properties
        upper_filled = bb.upper.ffill()
        middle_filled = bb.middle.ffill()
        lower_filled = bb.lower.ffill()
        
        # Calculate volume moving average for confirmation
        volume_ma = vbt.MA.run(volume, window=self.params['volume_ma_period']).ma
        volume_ma = volume_ma.ffill().fillna(0)
        
        # Calculate Average True Range for volatility
        atr = vbt.ATR.run(
            data['high'], 
            data['low'], 
            data['close'], 
            window=self.params['atr_period']
        ).atr.ffill()
        
        # Add trend filters - multiple timeframes
        sma_50 = vbt.MA.run(close, window=50).ma.ffill()
        sma_100 = vbt.MA.run(close, window=100).ma.ffill()
        sma_200 = vbt.MA.run(close, window=200).ma.ffill()
        
        # Calculate EMAs for more responsive trend indications - using ewm=True for exponential moving average
        ema_20 = vbt.MA.run(close, window=20, ewm=True).ma.ffill()
        ema_50 = vbt.MA.run(close, window=50, ewm=True).ma.ffill()
        
        # Strong uptrend condition
        strong_uptrend = (close > sma_50) & (ema_20 > ema_50)
        # Moderate uptrend condition
        moderate_uptrend = close > sma_200
        # Overall trend
        uptrend = strong_uptrend | moderate_uptrend
        
        # Calculate momentum indicators
        momentum_1d = close.pct_change(1)
        momentum_5d = close.pct_change(5)
        momentum_10d = close.pct_change(10)
        
        # Market regime filter - avoid extreme volatility
        bb_width = (upper_filled - lower_filled) / middle_filled
        normal_volatility = (bb_width < bb_width.rolling(20).mean() * 3.0) & (bb_width > bb_width.rolling(20).mean() * 0.3)
        
        # Entry conditions with improved logic
        # 1. Price near or below lower band (oversold)
        price_near_lower_band = close <= lower_filled * 1.05  # Within 5% of lower band
        
        # 2. RSI showing oversold and rising (bullish divergence)
        rsi_oversold = rsi < self.params['oversold_threshold']
        rsi_rising = rsi > rsi.shift(1)
        oversold_condition = rsi_oversold
        
        # 3. Volume confirmation (higher than average)
        volume_high = volume > volume_ma * 1.05  # More permissive volume requirement
        
        # 4. Bullish momentum setup
        positive_reversal = momentum_1d > 0  # Simple short-term positive momentum
        
        # Combined entry conditions - much more permissive
        entry_condition1 = price_near_lower_band & oversold_condition
        entry_condition2 = price_near_lower_band & positive_reversal & volume_high
        entry_condition3 = (close < middle_filled * 0.98) & uptrend & volume_high
        
        # Final entry condition - any of the three conditions
        entry = entry_condition1 | entry_condition2 | entry_condition3
        
        # Exit conditions with improved logic
        # 1. Price reaches middle band or higher (target achieved)
        price_reaches_target = close >= middle_filled
        
        # 2. RSI overbought condition
        rsi_overbought = rsi > self.params['overbought_threshold']
        
        # 3. Price near upper band (extended)
        price_near_upper_band = close >= upper_filled * 0.95
        
        # 4. Momentum reversal (to catch trend changes)
        momentum_reversal = momentum_1d < -0.01
        
        # Combined exit condition - more permissive
        exit = price_reaches_target | rsi_overbought | price_near_upper_band | momentum_reversal
        
        # Implement improved stop-loss and take-profit based on ATR and volatility
        # Use more asymmetric risk-reward - small stop loss, larger take profit
        sl_stop = 1.0 * atr / close  # Tight stop loss at 1x ATR
        tp_stop = 3.0 * atr / close  # More generous take profit at 3x ATR
        
        # Dynamic position sizing based on volatility
        bb_width_ma = bb_width.rolling(20).mean().fillna(bb_width)
        volatility_ratio = bb_width / bb_width_ma
        volatility_ratio = volatility_ratio.fillna(1.0)  # Default to neutral if NaN
        
        # Cap the ratio to avoid extreme values
        volatility_ratio = volatility_ratio.clip(0.5, 2.0)
        
        # Adjust position size by volatility and trend conviction
        base_size = 0.1
        position_size = np.where(strong_uptrend, base_size * 1.2, base_size)
        position_size = position_size * (1.0 / volatility_ratio.to_numpy())
        
        # Convert to numpy array and clip to reasonable range
        position_size = np.clip(position_size, 0.05, 0.15)
        
        # Backtest the strategy with improved risk management
        portfolio = vbt.Portfolio.from_signals(
            close,
            entry,
            exit,
            size=position_size,  # Dynamic position sizing
            fees=self.params['fee_rate'],
            freq='1D',
            init_cash=self.params['initial_capital'],
            sl_stop=sl_stop,
            tp_stop=tp_stop
        )
        
        return portfolio

def optimize_strategy(data, param_grid):
    """
    Optimize strategy parameters using grid search.
    
    Args:
        data (pd.DataFrame): Historical OHLCV data
        param_grid (dict): Dictionary of parameter ranges to test
        
    Returns:
        dict: Best performing parameters
    """
    best_score = -np.inf
    best_params = None
    
    total_combinations = 1
    for param_values in param_grid.values():
        total_combinations *= len(param_values)
    
    logger.info(f"Running optimization with {total_combinations} parameter combinations")
    
    # Progress tracking
    progress_step = max(1, total_combinations // 20)  # Report every 5%
    progress_counter = 0
    start_time = datetime.now()
    
    results = []
    
    # Implement grid search for BB parameters
    for bb_window in param_grid.get('bb_window', [20]):
        for bb_std in param_grid.get('bb_std', [2.0]):
            for rsi_period in param_grid.get('rsi_period', [14]):
                for oversold in param_grid.get('oversold_threshold', [30]):
                    for overbought in param_grid.get('overbought_threshold', [70]):
                        # Track progress
                        progress_counter += 1
                        if progress_counter % progress_step == 0 or progress_counter == total_combinations:
                            elapsed = datetime.now() - start_time
                            pct_complete = progress_counter / total_combinations * 100
                            eta = (elapsed / progress_counter) * (total_combinations - progress_counter) if progress_counter > 0 else timedelta(0)
                            logger.info(f"Progress: {pct_complete:.1f}% ({progress_counter}/{total_combinations}), ETA: {eta}")
                            
                        params = {
                            'bb_window': bb_window,
                            'bb_std': bb_std,
                            'rsi_period': rsi_period,
                            'oversold_threshold': oversold,
                            'overbought_threshold': overbought,
                            'volume_ma_period': 20,
                            'atr_period': 14,
                            'fee_rate': 0.001,
                            'initial_capital': 10000
                        }
                        
                        strategy = BollingerRSIVBT(params)
                        portfolio = strategy.run(data)
                        
                        # Calculate performance metrics
                        total_return = portfolio.total_return()
                        sharpe = portfolio.sharpe_ratio()
                        sortino = portfolio.sortino_ratio()
                        max_dd = portfolio.max_drawdown()
                        num_trades = portfolio.trades.count()
                        
                        # Skip invalid parameter combinations
                        if num_trades < 5 or np.isnan(sharpe) or sharpe <= 0:
                            continue
                            
                        # Calculate additional metrics 
                        if num_trades > 0:
                            winning_trades = portfolio.trades.records[portfolio.trades.records['pnl'] > 0]
                            win_rate = len(winning_trades) / num_trades * 100
                            avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
                            
                            losing_trades = portfolio.trades.records[portfolio.trades.records['pnl'] <= 0]
                            avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
                            
                            # Calculate profit factor and expectancy
                            gross_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
                            gross_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0
                            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
                            
                            expectancy = (win_rate/100 * avg_win + (1-win_rate/100) * avg_loss) if num_trades > 0 else 0
                        else:
                            win_rate = 0
                            profit_factor = 0
                            expectancy = 0
                            
                        # Create a custom score that balances different metrics
                        custom_score = (
                            0.3 * min(sharpe, 3.0) +  # Cap Sharpe influence 
                            0.2 * min(sortino, 4.0) +  # Cap Sortino influence
                            0.2 * min(profit_factor, 5.0) / 5.0 +  # Normalize profit factor
                            0.1 * min(total_return, 0.5) / 0.5 +  # Normalize returns
                            0.1 * min(win_rate / 100, 0.8) +  # Normalize win rate
                            0.1 * min(num_trades, 100) / 100  # Encourage more trades
                        )
                            
                        results.append({
                            'params': params.copy(),
                            'total_return': total_return,
                            'sharpe_ratio': sharpe,
                            'sortino_ratio': sortino,
                            'max_drawdown': max_dd,
                            'num_trades': num_trades,
                            'win_rate': win_rate,
                            'profit_factor': profit_factor,
                            'expectancy': expectancy,
                            'custom_score': custom_score
                        })
                        
                        # Update best parameters based on custom score
                        if custom_score > best_score:
                            best_score = custom_score
                            best_params = params.copy()
    
    # Sort results by custom score
    if results:
        results.sort(key=lambda x: x['custom_score'], reverse=True)
        logger.info(f"Top 5 parameter combinations (out of {len(results)}):")
        for i, result in enumerate(results[:5]):
            logger.info(f"#{i+1}: {result['params']} - Score: {result['custom_score']:.2f}, Sharpe: {result['sharpe_ratio']:.2f}, Return: {result['total_return']:.2%}, Trades: {result['num_trades']}, Win Rate: {result['win_rate']:.2f}%")
    else:
        logger.warning("No valid parameter combinations found!")
    
    return best_params

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

def main():
    # Test parameters
    product_id_to_test = "BTC-USD"
    start_date = "2023-01-01" 
    end_date = "2023-12-31"
    granularity = "ONE_DAY"
    
    # Get historical data
    data = fetch_historical_data(product_id_to_test, start_date, end_date, granularity)
    if data is None:
        logger.error("No data available for backtest. Exiting.")
        return
    
    # Run with default parameters first, then try variations
    logger.info("Running with default parameters first...")
    
    # Define default strategy parameters
    params = {
        'bb_window': 20,
        'bb_std': 2.0,
        'rsi_period': 14,
        'oversold_threshold': 30,
        'overbought_threshold': 70,
        'volume_ma_period': 20,
        'atr_period': 14,
        'fee_rate': 0.001,
        'initial_capital': 10000
    }
    
    # Test a range of variations for the improved BB+RSI strategy
    variations = [
        {'bb_window': 10, 'bb_std': 2.0},  # Faster Bollinger Bands
        {'bb_window': 30, 'bb_std': 2.0},  # Slower Bollinger Bands
        {'bb_window': 20, 'bb_std': 1.5},  # Tighter bands
        {'bb_window': 20, 'bb_std': 2.5},  # Wider bands
        {'rsi_period': 7, 'oversold_threshold': 30, 'overbought_threshold': 70},  # Faster RSI
        {'rsi_period': 21, 'oversold_threshold': 30, 'overbought_threshold': 70},  # Slower RSI
        {'rsi_period': 14, 'oversold_threshold': 20, 'overbought_threshold': 80},  # More extreme RSI thresholds
        {'rsi_period': 14, 'oversold_threshold': 40, 'overbought_threshold': 60},  # Less extreme RSI thresholds
        # Add new parameter combinations for testing
        {'bb_window': 20, 'bb_std': 1.0, 'rsi_period': 14, 'oversold_threshold': 15, 'overbought_threshold': 85},  # Very tight bands, extreme RSI
        {'bb_window': 40, 'bb_std': 3.0, 'rsi_period': 21, 'oversold_threshold': 25, 'overbought_threshold': 75},  # Very wide bands
        {'bb_window': 15, 'bb_std': 1.8, 'rsi_period': 9, 'oversold_threshold': 25, 'overbought_threshold': 75},  # Medium settings
        {'bb_window': 25, 'bb_std': 2.2, 'rsi_period': 18, 'oversold_threshold': 35, 'overbought_threshold': 65},  # Medium-conservative settings
    ]
    
    # Track best result
    best_return = -np.inf
    best_params = params.copy()
    best_portfolio = None
    
    # Test default params first
    strategy = BollingerRSIVBT(params)
    portfolio = strategy.run(data)
    
    if portfolio.trades.count() > 0:
        total_return = portfolio.total_return()
        sharpe = portfolio.sharpe_ratio()
        logger.info(f"Default parameters - Return: {total_return * 100:.2f}%, Sharpe: {sharpe:.2f}, Trades: {portfolio.trades.count()}")
        
        best_return = total_return
        best_params = params
        best_portfolio = portfolio
    else:
        logger.info("Default parameters - No trades generated")
    
    # Test each variation
    for i, var_params in enumerate(variations):
        test_params = params.copy()
        test_params.update(var_params)
        
        logger.info(f"Testing variation {i+1}: {var_params}")
        strategy = BollingerRSIVBT(test_params)
        portfolio = strategy.run(data)
        
        if portfolio.trades.count() > 0:
            total_return = portfolio.total_return()
            sharpe = portfolio.sharpe_ratio()
            logger.info(f"Variation {i+1} - Return: {total_return * 100:.2f}%, Sharpe: {sharpe:.2f}, Trades: {portfolio.trades.count()}")
            
            if total_return > best_return:
                best_return = total_return
                best_params = test_params.copy()
                best_portfolio = portfolio
        else:
            logger.info(f"Variation {i+1} - No trades generated")
    
    logger.info(f"Best parameters: {best_params} with return: {best_return * 100:.2f}%")
    
    # Use the best portfolio for reporting
    portfolio = best_portfolio if best_portfolio is not None else portfolio
    
    # Compute metrics
    stats_df = portfolio.stats()
    
    # Display results
    logger.info("\n=== Backtest Results ===")
    logger.info(f"Total Return: {portfolio.total_return() * 100:.2f}%")
    logger.info(f"Sharpe Ratio: {portfolio.sharpe_ratio():.2f}")
    logger.info(f"Max Drawdown: {portfolio.max_drawdown() * 100:.2f}%")
    
    # These metrics might not be directly available, get them from stats_df if possible
    # or calculate ourselves
    if "Win Rate [%]" in stats_df.index:
        logger.info(f"Win Rate: {stats_df.loc['Win Rate [%]']:.2f}%")
    else:
        # Calculate win rate manually if needed
        if portfolio.trades.count() > 0:
            winning_trades = portfolio.trades.records[portfolio.trades.records['pnl'] > 0]
            win_rate = len(winning_trades) / portfolio.trades.count() * 100
            logger.info(f"Win Rate: {win_rate:.2f}%")
        else:
            logger.info("Win Rate: N/A (no trades)")
    
    logger.info(f"Sortino Ratio: {portfolio.sortino_ratio():.2f}")
    
    if "Calmar Ratio" in stats_df.index:
        logger.info(f"Calmar Ratio: {stats_df.loc['Calmar Ratio']:.2f}")
    else:
        logger.info("Calmar Ratio: N/A")
    
    if "Profit Factor" in stats_df.index:
        logger.info(f"Profit Factor: {stats_df.loc['Profit Factor']:.2f}")
    else:
        logger.info("Profit Factor: N/A")
        
    if "Expectancy" in stats_df.index:
        logger.info(f"Expectancy: {stats_df.loc['Expectancy']:.4f}")
    else:
        logger.info("Expectancy: N/A")
    
    logger.info(f"Total Trades: {portfolio.trades.count()}")
    
    # Average trade duration handling
    avg_duration = portfolio.trades.avg_duration
    if callable(avg_duration):
        avg_duration = avg_duration()
    logger.info(f"Avg Trade Duration: {avg_duration}")
    
    # Generate plots
    logger.info("Generating plots...")
    try:
        # Check if there are trades before plotting
        if portfolio.trades.count() > 0:
            # Create and show main plot
            fig = portfolio.plot()
            fig.show()
            
            # Only attempt drawdown plot if there are sufficient trades
            if portfolio.trades.count() > 5:
                drawdown_fig = portfolio.plot_drawdowns()
                drawdown_fig.show()
            else:
                logger.warning("Not enough trades for detailed drawdown analysis")
        else:
            logger.warning("No trades to plot")
        
        logger.info("Plots generated and displayed.")
    except Exception as e:
        logger.error(f"Error generating plots: {str(e)}")
        logger.info("Continuing with analysis despite plotting error...")
    
    # Detailed trade analysis
    logger.info("\n=== Detailed Trade Analysis ===")
    if portfolio.trades.count() > 0:
        trades_df = portfolio.trades.records
        logger.info(f"Trade breakdown: {trades_df}")
    else:
        logger.info("No trades to analyze")

if __name__ == "__main__":
    main() 