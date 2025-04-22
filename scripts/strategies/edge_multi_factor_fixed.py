import vectorbtpro as vbt
import numpy as np
import pandas as pd
import sys
import os
import logging
from pathlib import Path
import argparse
from datetime import datetime
import itertools

# --- Basic Setup ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Configure pandas to avoid the FutureWarning about downcasting
pd.set_option('future.no_silent_downcasting', True)

# --- Import centralized data fetcher ---
try:
    from data.data_fetcher import fetch_historical_data, get_granularity_str, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    logger = logging.getLogger(__name__)
    logger.info("Successfully imported data_fetcher.")
except ImportError as e:
    print(f"WARNING: Could not import data_fetcher: {e}. Main block requires it.")
    def fetch_historical_data(*args, **kwargs):
        print("ERROR: fetch_historical_data is not available.")
        return None
    GRANULARITY_MAP_SECONDS = {'1h': 3600, '1d': 86400}
    def get_vbt_freq_str(*args, **kwargs): return "1h"

# ==============================================================================
# Factor Indicator Functions (Plain Python/Numba)
# ==============================================================================

def create_volatility_regime_indicator(close, lookback_window, vol_filter_window, volatility_threshold):
    """Calculates the volatility regime signal."""
    returns = close.pct_change()
    vol = returns.vbt.rolling_std(window=lookback_window, minp=lookback_window // 2)
    vol_ma = vol.vbt.rolling_mean(window=vol_filter_window, minp=vol_filter_window // 2)
    vol_ma_safe = vol_ma.replace(0, np.nan).ffill().bfill()
    vol_ratio = (vol / vol_ma_safe).fillna(1.0)
    vol_compressed = vol_ratio < volatility_threshold
    vol_expansion = vol_ratio.diff().fillna(0) > 0
    
    # Fix: Completely restructure to avoid the warning
    vol_compressed_bool = vol_compressed.astype(bool)
    vol_compressed_shifted = vol_compressed_bool.shift(1)
    # Fill NaN values after shifting with False
    vol_compressed_shifted = vol_compressed_shifted.fillna(False)
    vol_signal = vol_compressed_shifted & vol_expansion
    
    return vol_signal

def create_consolidation_breakout_indicator(high, low, close, lookback_window):
    """Calculates consolidation breakout signals."""
    hl_range = (high - low) / close.replace(0, np.nan)
    hl_range_ma = hl_range.vbt.rolling_mean(window=lookback_window, minp=lookback_window // 2)
    is_consolidating = hl_range < hl_range_ma * 0.8
    upper_level = high.vbt.rolling_max(window=lookback_window, minp=lookback_window // 2)
    lower_level = low.vbt.rolling_min(window=lookback_window, minp=lookback_window // 2)
    upper_level_shifted = upper_level.shift(1).bfill()
    lower_level_shifted = lower_level.shift(1).bfill()
    
    # Fix: Completely restructure to avoid the warning
    is_consolidating_bool = is_consolidating.astype(bool)
    is_consolidating_shifted = is_consolidating_bool.shift(1)
    # Fill NaN values after shifting with False 
    is_consolidating_shifted = is_consolidating_shifted.fillna(False)
    
    breakout_up = (close > upper_level_shifted) & is_consolidating_shifted
    breakout_down = (close < lower_level_shifted) & is_consolidating_shifted
    return breakout_up, breakout_down

def create_volume_divergence_indicator(volume, lookback_window, breakout_up, breakout_down):
    """Calculates volume confirmation signals based on pre-calculated breakouts."""
    volume_ma = volume.vbt.rolling_mean(window=lookback_window, minp=lookback_window // 2)
    volume_ma_safe = volume_ma.replace(0, np.nan).ffill().bfill()
    vol_ratio_vol = (volume / volume_ma_safe).fillna(1.0)
    volume_confirms_up = (vol_ratio_vol > 1.5) & breakout_up
    volume_confirms_down = (vol_ratio_vol > 1.5) & breakout_down
    return volume_confirms_up, volume_confirms_down

def create_market_microstructure_indicator(open, high, low, close):
    """Calculates market microstructure signals (candle shadows)."""
    upper_shadow = high - np.maximum(open, close)
    lower_shadow = np.minimum(open, close) - low
    hl_range_nonzero = (high - low).replace(0, np.nan)
    shadow_ratio = ((upper_shadow - lower_shadow) / hl_range_nonzero).fillna(0)
    buying_pressure = shadow_ratio < -0.5
    selling_pressure = shadow_ratio > 0.5
    return buying_pressure, selling_pressure

# ==============================================================================
# Strategy Class with Simplified Interface to Match Backtest Expectations
# ==============================================================================
class EdgeMultiFactorStrategy:
    """
    Edge multi-factor strategy with simplified API to match backtest expectations.
    """
    def __init__(self,
                 lookback_window=20,
                 vol_filter_window=100,
                 volatility_threshold=0.5,
                 initial_capital=3000,
                 default_factor_weights=None,
                 commission_pct=0.001,
                 slippage_pct=0.0005):

        self.lookback_window = int(lookback_window)
        self.vol_filter_window = int(vol_filter_window)
        self.volatility_threshold = float(volatility_threshold)
        self.initial_capital = float(initial_capital)
        self.commission_pct = float(commission_pct)
        self.slippage_pct = float(slippage_pct)
        self.signal_threshold = 0.3  # Lower threshold to generate more signals

        if default_factor_weights is None:
            self.factor_weights = {
                'volatility_regime': 0.25,
                'consolidation_breakout': 0.25,
                'volume_divergence': 0.25,
                'market_microstructure': 0.25
            }
        else:
            total_weight = sum(default_factor_weights.values())
            if not np.isclose(total_weight, 1.0):
                print(f"Warning: Provided weights sum to {total_weight}, normalizing.")
                self.factor_weights = {k: v / total_weight for k, v in default_factor_weights.items()}
            else:
                self.factor_weights = default_factor_weights
                
        if not (0 < self.volatility_threshold < 1):
             raise ValueError("volatility_threshold must be between 0 and 1")
        if self.lookback_window <= 0 or self.vol_filter_window <= 0:
             raise ValueError("Window parameters must be positive integers")
        if self.initial_capital <= 0:
             raise ValueError("Initial capital must be positive")

    def generate_signals(self, data: pd.DataFrame):
        """
        Simplified generate_signals that returns a tuple matching what backtest expects.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Tuple of (long_entries, short_entries, is_trending, is_ranging)
        """
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"Data missing required columns: {set(required_cols) - set(data.columns)}")

        # Store data for later use in backtest_signals
        self._data = data.copy()

        min_required_data = max(self.lookback_window, self.vol_filter_window) + 5
        if len(data) < min_required_data:
             print(f"Warning: Data length ({len(data)}) might be insufficient for lookbacks ({min_required_data}).")

        # Calculate ADX for market regime detection
        adx_period = 14
        adx = vbt.ADX.run(data['high'], data['low'], data['close'], window=adx_period).adx

        # Define market regimes
        is_trending = (adx > 25).fillna(False)
        is_ranging = (adx < 20).fillna(False)

        # Calculate individual factor signals
        vol_signal = create_volatility_regime_indicator(
            data['close'], 
            lookback_window=self.lookback_window,
            vol_filter_window=self.vol_filter_window,
            volatility_threshold=self.volatility_threshold
        )
        
        breakout_up, breakout_down = create_consolidation_breakout_indicator(
            data['high'], data['low'], data['close'], 
            lookback_window=self.lookback_window
        )
        
        volume_confirms_up, volume_confirms_down = create_volume_divergence_indicator(
            data['volume'],
            lookback_window=self.lookback_window,
            breakout_up=breakout_up,
            breakout_down=breakout_down
        )
        
        buying_pressure, selling_pressure = create_market_microstructure_indicator(
            data['open'], data['high'], data['low'], data['close']
        )

        # Debug signal components (optional)
        print(f"Signal components - Vol: {vol_signal.sum()}, Breakout Up: {breakout_up.sum()}, " + 
              f"Volume Up: {volume_confirms_up.sum()}, Buying: {buying_pressure.sum()}")
        print(f"Signal components - Breakout Down: {breakout_down.sum()}, " + 
              f"Volume Down: {volume_confirms_down.sum()}, Selling: {selling_pressure.sum()}")

        # Combine signals using weights
        long_signal = pd.Series(0.0, index=data.index)
        short_signal = pd.Series(0.0, index=data.index)
        
        # Ensure results are float/boolean before weighting
        long_signal += vol_signal.astype(float) * self.factor_weights.get('volatility_regime', 0)
        long_signal += breakout_up.astype(float) * self.factor_weights.get('consolidation_breakout', 0)
        long_signal += volume_confirms_up.astype(float) * self.factor_weights.get('volume_divergence', 0)
        long_signal += buying_pressure.astype(float) * self.factor_weights.get('market_microstructure', 0)
        
        short_signal += vol_signal.astype(float) * self.factor_weights.get('volatility_regime', 0)
        short_signal += breakout_down.astype(float) * self.factor_weights.get('consolidation_breakout', 0)
        short_signal += volume_confirms_down.astype(float) * self.factor_weights.get('volume_divergence', 0)
        short_signal += selling_pressure.astype(float) * self.factor_weights.get('market_microstructure', 0)

        # Generate entries based on signal threshold
        long_entries = long_signal > self.signal_threshold
        short_entries = short_signal > self.signal_threshold
        
        # Prevent simultaneous entries
        simultaneous = long_entries & short_entries
        long_entries[simultaneous] = False
        short_entries[simultaneous] = False
        
        # Apply market regime adaptation (optional)
        trend_up = is_trending & (data['close'] > data['close'].shift(self.lookback_window))
        trend_down = is_trending & (data['close'] < data['close'].shift(self.lookback_window))
        
        # Fix: Create temporary boolean masks to avoid dtype incompatibility warnings
        long_adjusted_up = (long_signal[trend_up] > (self.signal_threshold * 0.7)).astype(bool)
        short_adjusted_up = (short_signal[trend_up] > (self.signal_threshold * 1.3)).astype(bool)
        long_adjusted_down = (long_signal[trend_down] > (self.signal_threshold * 1.3)).astype(bool)
        short_adjusted_down = (short_signal[trend_down] > (self.signal_threshold * 0.7)).astype(bool)
        
        # Apply the adjusted thresholds using loc to avoid warning
        long_entries.loc[trend_up] = long_adjusted_up
        short_entries.loc[trend_up] = short_adjusted_up
        long_entries.loc[trend_down] = long_adjusted_down
        short_entries.loc[trend_down] = short_adjusted_down
        
        # Log signal counts
        print(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries.")
        
        return long_entries, short_entries, is_trending, is_ranging

    def calculate_target_percent(self, data: pd.DataFrame, risk_fraction=0.01, atr_window=14, atr_multiple_stop=2.0):
        """
        Calculates the target percent for each position based on risk.
        
        Args:
            data: DataFrame with OHLCV data
            risk_fraction: Fraction of capital to risk per trade
            atr_window: Window for ATR calculation
            atr_multiple_stop: ATR multiple for stop loss distance
            
        Returns:
            Series of target percentages
        """
        close = data['close']
        high = data['high']
        low = data['low']
        
        # Calculate ATR for volatility-based position sizing
        atr = vbt.ATR.run(
            high, low, close,
            window=int(atr_window),
            wtype='wilder'
        ).atr.bfill().ffill()
        
        # Calculate stop distance in price terms
        stop_distance = atr * atr_multiple_stop
        
        # Calculate percent risk (stop distance as percentage of price)
        percent_risk = stop_distance / close
        
        # Calculate target percentage based on risk fraction
        # If we're risking risk_fraction (e.g., 1%) of capital
        # And our stop is percent_risk (e.g., 2%) below entry
        # Then position size should be risk_fraction/percent_risk of our capital
        target_percent = risk_fraction / percent_risk
        
        # Cap the target percent to avoid excessive leverage
        max_target_percent = 0.25  # Maximum 25% of capital per trade
        target_percent = np.minimum(target_percent, max_target_percent)
        
        # Ensure no invalid values
        target_percent = target_percent.replace([np.inf, -np.inf], 0).fillna(0)
        
        return target_percent
        
    def backtest_signals(self, entry_signals, exit_signals=None, data=None):
        """
        Backtest the signals using vectorbt.
        
        Args:
            entry_signals (pd.Series): Entry signals (True/False)
            exit_signals (pd.Series, optional): Exit signals (True/False)
            data (pd.DataFrame, optional): Market data
            
        Returns:
            tuple: (Portfolio object with backtest results, metrics dictionary)
        """
        try:
            if data is None and hasattr(self, '_data'):
                data = self._data
            
            if data is None:
                raise ValueError("Data not provided for backtest_signals and no cached data available.")
                
            # Create default exit signals if not provided
            if exit_signals is None:
                # Simple exit after N bars
                exit_after_bars = 10
                exit_signals = entry_signals.shift(exit_after_bars).fillna(False)
            
            # Ensure signals are properly cast to boolean
            entry_signals = entry_signals.astype(bool)
            exit_signals = exit_signals.astype(bool)
            
            # Use a fixed size approach (amount per trade)
            fixed_size = 1.0  # 1 unit per trade
            
            # Create a portfolio using vectorbt
            portfolio = vbt.Portfolio.from_signals(
                close=data['close'],
                entries=entry_signals,
                exits=exit_signals,
                size=fixed_size,
                init_cash=self.initial_capital,
                fees=self.commission_pct,
                slippage=self.slippage_pct
            )
            
            # Calculate metrics
            metrics = calculate_performance_metrics(portfolio)
            
            return portfolio, metrics
            
        except Exception as e:
            import logging
            logging.error(f"Error in backtest_signals: {str(e)}")
            import traceback
            logging.debug(traceback.format_exc())
            return None, {}

def calculate_performance_metrics(portfolio):
    """
    Calculate performance metrics from a vectorbt portfolio, handling both 'pnl' and 'PnL' column names.
    
    Args:
        portfolio: A vectorbt portfolio object
        
    Returns:
        dict: A dictionary of performance metrics
    """
    metrics = {}
    
    if portfolio is None:
        return {
            'total_return': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'total_trades': 0
        }
    
    # Extract trades from portfolio
    if hasattr(portfolio, 'trades'):
        trades = portfolio.trades
        
        # Handle both direct property access and dataframe access
        try:
            # Try to get metrics directly from trades object
            if hasattr(trades, 'count'):
                # Handle count as both method and attribute
                if callable(trades.count):
                    metrics['total_trades'] = trades.count()
                else:
                    metrics['total_trades'] = trades.count
                
                metrics['win_rate'] = trades.win_rate
                metrics['profit_factor'] = trades.profit_factor
            # If that fails, use the records_readable DataFrame
            elif hasattr(trades, 'records_readable'):
                trades_df = trades.records_readable
                
                # Handle both 'pnl' and 'PnL' column names
                pnl_col = None
                if 'PnL' in trades_df.columns:
                    pnl_col = 'PnL'
                elif 'pnl' in trades_df.columns:
                    pnl_col = 'pnl'
                
                if pnl_col is not None:
                    winning_trades = trades_df[trades_df[pnl_col] > 0]
                    losing_trades = trades_df[trades_df[pnl_col] <= 0]
                    
                    metrics['total_trades'] = len(trades_df)
                    metrics['winning_trades'] = len(winning_trades)
                    metrics['losing_trades'] = len(losing_trades)
                    metrics['win_rate'] = len(winning_trades) / len(trades_df) if len(trades_df) > 0 else 0
                    
                    # Calculate profit factor
                    total_profit = winning_trades[pnl_col].sum() if len(winning_trades) > 0 else 0
                    total_loss = abs(losing_trades[pnl_col].sum()) if len(losing_trades) > 0 else 0
                    metrics['profit_factor'] = total_profit / total_loss if total_loss > 0 else (1.0 if total_profit > 0 else 0.0)
                else:
                    # Fallback if no pnl column is found
                    metrics['total_trades'] = len(trades_df)
                    metrics['win_rate'] = 0.0
                    metrics['profit_factor'] = 0.0
        except Exception as e:
            import logging
            logging.warning(f"Error calculating trade metrics: {str(e)}")
            metrics['total_trades'] = 0
            metrics['win_rate'] = 0.0
            metrics['profit_factor'] = 0.0
    
    # Portfolio-level metrics
    try:
        # Get total return - handle both property and method
        if callable(getattr(portfolio, 'total_return', None)):
            metrics['total_return'] = portfolio.total_return()
        else:
            metrics['total_return'] = portfolio.total_return
            
        # Get max drawdown - handle both property and method
        if callable(getattr(portfolio, 'max_drawdown', None)):
            metrics['max_drawdown'] = portfolio.max_drawdown()
        else:
            metrics['max_drawdown'] = portfolio.max_drawdown
            
        # Get Sharpe ratio - handle both property and method
        if callable(getattr(portfolio, 'sharpe_ratio', None)):
            metrics['sharpe_ratio'] = portfolio.sharpe_ratio()
        else:
            metrics['sharpe_ratio'] = getattr(portfolio, 'sharpe_ratio', 0.0)
    except Exception as e:
        import logging
        logging.warning(f"Error calculating portfolio metrics: {str(e)}")
        metrics['total_return'] = 0.0
        metrics['max_drawdown'] = 0.0
        metrics['sharpe_ratio'] = 0.0
    
    return metrics

# --- Main block for single run testing ---
if __name__ == "__main__":
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description='Test Fixed EdgeMultiFactorStrategy.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2023-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1h', help='Data granularity (e.g., 1h, 4h, 1d)')
    parser.add_argument('--lookback', type=int, default=15, help='Lookback window for factors')
    parser.add_argument('--vol_thresh', type=float, default=0.7, help='Volatility ratio threshold')
    parser.add_argument('--plot', action='store_true', help='Generate and show plot')
    
    args = parser.parse_args()

    # --- Data Fetching ---
    granularity_seconds = GRANULARITY_MAP_SECONDS.get(args.granularity.lower())
    if granularity_seconds is None:
        print(f"Error: Unsupported granularity: {args.granularity}.")
        sys.exit(1)
    
    print(f"Fetching data for {args.symbol} from {args.start_date} to {args.end_date} ({args.granularity})...")
    price_data = fetch_historical_data(args.symbol, args.start_date, args.end_date, granularity_seconds)
    
    if price_data is None or price_data.empty:
        print("Failed to fetch data. Exiting.")
        sys.exit(1)
    
    print(f"Data fetched successfully. Shape: {price_data.shape}")
    price_data.index = pd.to_datetime(price_data.index, utc=True)

    # --- Strategy Initialization ---
    print("Initializing fixed EdgeMultiFactorStrategy...")
    strategy = EdgeMultiFactorStrategy(
        lookback_window=args.lookback,
        vol_filter_window=50,  # Reduced from 100 for faster signal generation
        volatility_threshold=args.vol_thresh,
        initial_capital=3000,
        default_factor_weights={
            'volatility_regime': 0.25,
            'consolidation_breakout': 0.25,
            'volume_divergence': 0.25,
            'market_microstructure': 0.25
        }
    )

    # --- Signal Generation --- 
    print("Generating signals...")
    long_entries, short_entries, is_trending, is_ranging = strategy.generate_signals(price_data)
    
    if long_entries.sum() + short_entries.sum() == 0:
        print("No entry signals generated.")
        sys.exit(0)
    
    # --- Calculate Target Percentage Size ---
    print("Calculating target percentage size...")
    target_pct = strategy.calculate_target_percent(
        price_data,
        risk_fraction=0.01,
        atr_window=14,
        atr_multiple_stop=2.0
    )
    
    # --- Results ---
    print(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries.")
    print(f"Trending periods: {is_trending.sum()} days")
    print(f"Ranging periods: {is_ranging.sum()} days")
    
    # --- Backtest the strategy ---
    print("Backtesting the strategy...")
    portfolio, metrics = strategy.backtest_signals(long_entries, data=price_data)
    
    # --- Display metrics ---
    if portfolio is not None:
        print("\nBacktest Results:")
        print(f"Total Return: {metrics['total_return']:.2%}")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
        print(f"Total Trades: {metrics['total_trades']}")
        print(f"Win Rate: {metrics['win_rate']:.2%}")
        print(f"Profit Factor: {metrics['profit_factor']:.2f}")
    else:
        print("Backtest failed.")
    
    # --- Plotting ---
    if args.plot:
        print("Generating plot...")
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        
        # Plot price and signals
        plt.subplot(2, 1, 1)
        plt.plot(price_data.index, price_data['close'], label='Close Price')
        plt.scatter(price_data.index[long_entries], 
                    price_data.loc[long_entries, 'close'],
                    color='green', marker='^', label='Long Entry')
        plt.scatter(price_data.index[short_entries], 
                    price_data.loc[short_entries, 'close'],
                    color='red', marker='v', label='Short Entry')
        plt.title('Price and Signals')
        plt.legend()
        
        # Plot trending and ranging periods
        plt.subplot(2, 1, 2)
        plt.plot(price_data.index, is_trending, label='Trending', color='blue')
        plt.plot(price_data.index, is_ranging, label='Ranging', color='orange')
        plt.title('Market Regimes')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('edge_strategy_fixed_test.png')
        print("Plot saved to edge_strategy_fixed_test.png")
    
    print("Test completed successfully.") 