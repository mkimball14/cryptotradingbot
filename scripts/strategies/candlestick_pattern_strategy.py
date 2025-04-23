import numpy as np
import pandas as pd
from typing import Dict, Any, List, Union, Tuple, Optional
import logging
from pathlib import Path
import os

# Add parent directory to path to import our modules
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Import our candle pattern functions
from scripts.indicators.candle_patterns import (
    extract_candle_patterns,
    get_candle_pattern_strength,
    generate_candle_pattern_signals
)

# Import strategy base class (adjust import path if needed)
from scripts.strategies.strategy_base import StrategyBase

# Configure logging
logger = logging.getLogger("candlestick_strategy")

class CandlestickPatternStrategy(StrategyBase):
    """
    Trading strategy based on candlestick patterns.
    
    This strategy:
    1. Identifies candlestick patterns in price data
    2. Calculates the historical reliability of each pattern
    3. Generates trading signals based on pattern strength and configuration
    """
    
    def __init__(self, 
                config: Dict[str, Any] = None, 
                **kwargs):
        """
        Initialize the candlestick pattern strategy.
        
        Args:
            config: Strategy configuration dictionary
            **kwargs: Additional keyword arguments
        """
        # Default configuration
        default_config = {
            "lookback_periods": 50,          # Periods to look back for calculating pattern strength
            "min_strength": 0.01,            # Minimum pattern strength to generate a signal
            "patterns": "all",               # List of patterns to use or "all"
            "use_strength": True,            # Whether to use pattern strength for signal generation
            "use_confirmation": True,        # Whether to require confirmation from other indicators
            "confirmation_window": 3,        # Periods to wait for confirmation
            "max_trades": 3,                 # Maximum concurrent trades
            "stop_loss_pct": 0.05,           # Stop loss percentage
            "take_profit_pct": 0.10,         # Take profit percentage
            "risk_per_trade": 0.02,          # Percentage of portfolio to risk per trade
        }
        
        # Update default config with provided config
        if config:
            default_config.update(config)
        
        # Initialize base class
        super().__init__(config=default_config, **kwargs)
        
        # Set up strategy-specific attributes
        self.name = "Candlestick Pattern Strategy"
        self.description = "Trading strategy based on candlestick patterns and their historical reliability"
        self.lookback_periods = self.config["lookback_periods"]
        self.min_strength = self.config["min_strength"]
        self.use_strength = self.config["use_strength"]
        self.use_confirmation = self.config["use_confirmation"]
        self.confirmation_window = self.config["confirmation_window"]
        
        # Set up patterns to use
        if isinstance(self.config["patterns"], str) and self.config["patterns"].lower() == "all":
            self.patterns = None  # Use all patterns
        elif isinstance(self.config["patterns"], list):
            self.patterns = self.config["patterns"]
        else:
            self.patterns = None  # Default to all patterns
            
        # Track active trades and signals
        self.active_trades = {}
        self.pending_signals = {}
        self.confirmed_signals = {}
            
        logger.info(f"Initialized {self.name} with config: {self.config}")
    
    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare data for the strategy by extracting candlestick patterns and calculating strength metrics.
        
        Args:
            data: DataFrame with OHLCV price data
            
        Returns:
            DataFrame with added candlestick pattern signals and metrics
        """
        try:
            # Make sure we have enough data
            if len(data) < self.lookback_periods + 10:
                logger.warning(f"Not enough data for reliable pattern strength calculation. Have {len(data)} periods, need at least {self.lookback_periods + 10}.")
            
            # Extract candlestick patterns
            logger.debug("Extracting candlestick patterns")
            df = extract_candle_patterns(data, pattern_list=self.patterns)
            
            # Calculate pattern strength
            logger.debug("Calculating pattern strength")
            df = get_candle_pattern_strength(df, lookback=self.lookback_periods)
            
            # Generate buy/sell signals
            logger.debug("Generating pattern signals")
            buy_signals, sell_signals = generate_candle_pattern_signals(
                df, 
                min_strength=self.min_strength,
                use_strength=self.use_strength
            )
            
            # Add signals to DataFrame
            df['candle_buy_signal'] = buy_signals
            df['candle_sell_signal'] = sell_signals
            
            # Calculate net pattern strength metrics
            pattern_cols = [col for col in df.columns if col.startswith('CDL')]
            strength_cols = [col for col in df.columns if col.endswith('_strength')]
            
            if strength_cols:
                # Initialize net strength columns
                df['net_bullish_strength'] = 0.0
                df['net_bearish_strength'] = 0.0
                
                # Sum up all pattern strengths
                for pattern in pattern_cols:
                    strength_col = f"{pattern}_strength"
                    if strength_col in df.columns:
                        # Add to bullish strength if pattern is bullish and strength is positive
                        bullish_mask = (df[pattern] > 0) & (df[strength_col] > 0)
                        df.loc[bullish_mask, 'net_bullish_strength'] += df.loc[bullish_mask, strength_col]
                        
                        # Add to bearish strength if pattern is bearish and strength is positive
                        bearish_mask = (df[pattern] < 0) & (df[strength_col] > 0)
                        df.loc[bearish_mask, 'net_bearish_strength'] += df.loc[bearish_mask, strength_col]
            
            return df
            
        except Exception as e:
            logger.error(f"Error preparing data for candlestick pattern strategy: {str(e)}")
            # Return original data if preparation fails
            return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on candlestick patterns.
        
        Args:
            data: DataFrame with OHLCV data and extracted candlestick patterns
            
        Returns:
            DataFrame with added signal columns
        """
        try:
            # Make a copy of the input data
            df = data.copy()
            
            # Ensure we have the required columns
            if 'candle_buy_signal' not in df.columns or 'candle_sell_signal' not in df.columns:
                logger.warning("Required signal columns not found. Running prepare_data first.")
                df = self.prepare_data(df)
            
            # Initialize signal columns if they don't exist
            if 'signal' not in df.columns:
                df['signal'] = 0
                
            if 'position' not in df.columns:
                df['position'] = 0
                
            # Apply trading logic
            for i in range(len(df)):
                # Skip if not enough lookback data
                if i < self.lookback_periods:
                    continue
                
                # Check for buy signal
                if df['candle_buy_signal'].iloc[i]:
                    if self.use_confirmation:
                        # Store pending buy signal for confirmation
                        symbol = df.index.name if df.index.name else 'default'
                        timestamp = df.index[i]
                        signal_key = f"{symbol}_{timestamp}"
                        
                        self.pending_signals[signal_key] = {
                            'type': 'buy',
                            'timestamp': timestamp,
                            'price': df['close'].iloc[i],
                            'strength': df.get('net_bullish_strength', pd.Series(0)).iloc[i],
                            'confirmation_count': 0,
                            'max_confirmation_count': self.confirmation_window
                        }
                    else:
                        # Generate immediate buy signal
                        df.loc[df.index[i], 'signal'] = 1
                
                # Check for sell signal
                elif df['candle_sell_signal'].iloc[i]:
                    if self.use_confirmation:
                        # Store pending sell signal for confirmation
                        symbol = df.index.name if df.index.name else 'default'
                        timestamp = df.index[i]
                        signal_key = f"{symbol}_{timestamp}"
                        
                        self.pending_signals[signal_key] = {
                            'type': 'sell',
                            'timestamp': timestamp,
                            'price': df['close'].iloc[i],
                            'strength': df.get('net_bearish_strength', pd.Series(0)).iloc[i],
                            'confirmation_count': 0,
                            'max_confirmation_count': self.confirmation_window
                        }
                    else:
                        # Generate immediate sell signal
                        df.loc[df.index[i], 'signal'] = -1
            
            # Update positions based on signals
            position = 0
            for i in range(len(df)):
                # Update position based on signal
                if df['signal'].iloc[i] == 1:
                    position = 1  # Long position
                elif df['signal'].iloc[i] == -1:
                    position = -1  # Short position
                
                # Set position for this row
                df.iloc[i, df.columns.get_loc('position')] = position
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating signals for candlestick pattern strategy: {str(e)}")
            # Return the input data with no signals
            if 'signal' not in data.columns:
                data['signal'] = 0
            if 'position' not in data.columns:
                data['position'] = 0
            return data
    
    def confirm_signals(self, data: pd.DataFrame, other_indicators: Optional[Dict[str, pd.DataFrame]] = None) -> None:
        """
        Confirm pending signals using other indicators or price action.
        
        Args:
            data: DataFrame with OHLCV data
            other_indicators: Dictionary of DataFrames with other indicator values
        
        Note:
            This method updates the internal confirmed_signals dictionary.
        """
        if not self.use_confirmation or not self.pending_signals:
            return
            
        try:
            # Get symbols from pending signals
            symbols = set()
            for signal_key in self.pending_signals:
                symbol = signal_key.split('_')[0]
                symbols.add(symbol)
            
            # Process each pending signal
            pending_keys = list(self.pending_signals.keys())
            for signal_key in pending_keys:
                signal = self.pending_signals[signal_key]
                symbol = signal_key.split('_')[0]
                
                # Skip if we don't have data for this symbol
                if data.index.name != symbol and symbol != 'default':
                    continue
                
                # Get current price data
                if signal['timestamp'] in data.index:
                    current_idx = data.index.get_loc(signal['timestamp'])
                    
                    # Skip if we're at the end of the data
                    if current_idx + 1 >= len(data):
                        continue
                    
                    # Get next candle data for confirmation
                    next_candle = data.iloc[current_idx + 1]
                    
                    # Check for price confirmation
                    if signal['type'] == 'buy':
                        # Confirm bullish signal if next candle continues upward
                        if next_candle['close'] > next_candle['open']:
                            signal['confirmation_count'] += 1
                    else:  # sell signal
                        # Confirm bearish signal if next candle continues downward
                        if next_candle['close'] < next_candle['open']:
                            signal['confirmation_count'] += 1
                    
                    # Check for confirmation from other indicators
                    if other_indicators:
                        for indicator_name, indicator_df in other_indicators.items():
                            # Skip if we don't have data for this timestamp
                            if signal['timestamp'] not in indicator_df.index:
                                continue
                                
                            # Get indicator value for confirmation
                            indicator_value = indicator_df.loc[signal['timestamp']]
                            
                            # Check if indicator confirms the signal (simple example)
                            # This should be customized based on actual indicators
                            if indicator_name == 'macd' and 'histogram' in indicator_value:
                                if signal['type'] == 'buy' and indicator_value['histogram'] > 0:
                                    signal['confirmation_count'] += 0.5
                                elif signal['type'] == 'sell' and indicator_value['histogram'] < 0:
                                    signal['confirmation_count'] += 0.5
                            
                            elif indicator_name == 'rsi' and 'value' in indicator_value:
                                if signal['type'] == 'buy' and 30 < indicator_value['value'] < 50:
                                    signal['confirmation_count'] += 0.5
                                elif signal['type'] == 'sell' and 50 < indicator_value['value'] < 70:
                                    signal['confirmation_count'] += 0.5
                    
                    # Check if signal is confirmed
                    if signal['confirmation_count'] >= 1:
                        # Move to confirmed signals
                        self.confirmed_signals[signal_key] = signal
                        del self.pending_signals[signal_key]
                    
                    # Remove expired signals
                    elif signal['confirmation_count'] >= signal['max_confirmation_count']:
                        del self.pending_signals[signal_key]
                
                # Remove signals for timestamps not in the data
                else:
                    del self.pending_signals[signal_key]
        
        except Exception as e:
            logger.error(f"Error confirming signals: {str(e)}")
    
    def execute_trades(self, data: pd.DataFrame, broker=None) -> List[Dict[str, Any]]:
        """
        Execute trades based on confirmed signals.
        
        Args:
            data: DataFrame with OHLCV data
            broker: Broker interface for executing trades
            
        Returns:
            List of executed trade dictionaries
        """
        executed_trades = []
        
        if not broker:
            logger.warning("No broker provided for trade execution.")
            return executed_trades
            
        try:
            # Process confirmed signals
            for signal_key, signal in self.confirmed_signals.items():
                symbol = signal_key.split('_')[0]
                if symbol == 'default':
                    symbol = data.index.name
                
                # Get current price
                current_price = data['close'].iloc[-1]
                
                # Execute the trade
                if signal['type'] == 'buy':
                    # Calculate position size based on risk
                    risk_amount = broker.get_portfolio_value() * self.config['risk_per_trade']
                    stop_loss_price = current_price * (1 - self.config['stop_loss_pct'])
                    risk_per_share = current_price - stop_loss_price
                    position_size = risk_amount / risk_per_share
                    
                    # Check if we have enough funds
                    if broker.can_buy(symbol, position_size, current_price):
                        # Execute buy order
                        order_id = broker.place_order(
                            symbol=symbol,
                            order_type='market',
                            side='buy',
                            quantity=position_size
                        )
                        
                        if order_id:
                            trade = {
                                'id': order_id,
                                'symbol': symbol,
                                'type': 'buy',
                                'price': current_price,
                                'size': position_size,
                                'timestamp': data.index[-1],
                                'stop_loss': stop_loss_price,
                                'take_profit': current_price * (1 + self.config['take_profit_pct'])
                            }
                            executed_trades.append(trade)
                            self.active_trades[order_id] = trade
                            logger.info(f"Executed buy trade: {trade}")
                
                elif signal['type'] == 'sell':
                    # For simplicity, we'll just sell any existing position
                    # This should be expanded to handle short selling if that's supported
                    for trade_id, trade in self.active_trades.items():
                        if trade['symbol'] == symbol and trade['type'] == 'buy':
                            # Sell position
                            order_id = broker.place_order(
                                symbol=symbol,
                                order_type='market',
                                side='sell',
                                quantity=trade['size']
                            )
                            
                            if order_id:
                                close_trade = {
                                    'id': order_id,
                                    'symbol': symbol,
                                    'type': 'sell',
                                    'price': current_price,
                                    'size': trade['size'],
                                    'timestamp': data.index[-1],
                                    'pnl': (current_price - trade['price']) * trade['size']
                                }
                                executed_trades.append(close_trade)
                                del self.active_trades[trade_id]
                                logger.info(f"Executed sell trade: {close_trade}")
            
            # Clear confirmed signals after processing
            self.confirmed_signals.clear()
            
            # Manage existing trades (check stop loss/take profit)
            self.manage_active_trades(data, broker)
            
            return executed_trades
            
        except Exception as e:
            logger.error(f"Error executing trades: {str(e)}")
            return executed_trades
    
    def manage_active_trades(self, data: pd.DataFrame, broker=None) -> None:
        """
        Manage active trades, including stop loss and take profit.
        
        Args:
            data: DataFrame with OHLCV data
            broker: Broker interface for executing trades
        """
        if not broker or not self.active_trades:
            return
            
        try:
            # Get current price
            current_price = data['close'].iloc[-1]
            
            # Check each active trade
            trades_to_remove = []
            for trade_id, trade in self.active_trades.items():
                symbol = trade['symbol']
                
                # Check stop loss
                if trade['type'] == 'buy' and current_price <= trade['stop_loss']:
                    # Execute stop loss
                    order_id = broker.place_order(
                        symbol=symbol,
                        order_type='market',
                        side='sell',
                        quantity=trade['size']
                    )
                    
                    if order_id:
                        logger.info(f"Stop loss triggered for trade {trade_id} at price {current_price}")
                        trades_to_remove.append(trade_id)
                
                # Check take profit
                elif trade['type'] == 'buy' and current_price >= trade['take_profit']:
                    # Execute take profit
                    order_id = broker.place_order(
                        symbol=symbol,
                        order_type='market',
                        side='sell',
                        quantity=trade['size']
                    )
                    
                    if order_id:
                        logger.info(f"Take profit triggered for trade {trade_id} at price {current_price}")
                        trades_to_remove.append(trade_id)
            
            # Remove closed trades
            for trade_id in trades_to_remove:
                del self.active_trades[trade_id]
                
        except Exception as e:
            logger.error(f"Error managing active trades: {str(e)}")
    
    def backtest(self, data: pd.DataFrame, initial_capital: float = 10000.0) -> Dict[str, Any]:
        """
        Run a backtest of the strategy on historical data.
        
        Args:
            data: DataFrame with OHLCV data
            initial_capital: Initial capital for the backtest
            
        Returns:
            Dictionary with backtest results
        """
        try:
            # Prepare data
            df = self.prepare_data(data)
            
            # Generate signals
            df = self.generate_signals(df)
            
            # Initialize backtest variables
            capital = initial_capital
            position = 0
            position_size = 0
            entry_price = 0
            trades = []
            equity_curve = [capital]
            
            # Run backtest
            for i in range(1, len(df)):
                # Get current price
                close_price = df['close'].iloc[i]
                
                # Update equity if we have a position
                if position != 0:
                    # Calculate current equity with position
                    current_equity = capital + position * position_size * (close_price - entry_price)
                    equity_curve.append(current_equity)
                else:
                    # No position, equity is just capital
                    equity_curve.append(capital)
                
                # Check for signals
                if df['signal'].iloc[i] == 1 and position <= 0:
                    # Buy signal
                    position = 1
                    
                    # Calculate position size (fixed percentage of capital)
                    position_size = capital * self.config['risk_per_trade'] / (close_price * self.config['stop_loss_pct'])
                    
                    entry_price = close_price
                    
                    # Record trade
                    trades.append({
                        'type': 'buy',
                        'entry_time': df.index[i],
                        'entry_price': entry_price,
                        'size': position_size,
                        'stop_loss': entry_price * (1 - self.config['stop_loss_pct']),
                        'take_profit': entry_price * (1 + self.config['take_profit_pct'])
                    })
                    
                    logger.debug(f"Buy signal at {df.index[i]}, price: {entry_price}, size: {position_size}")
                
                elif df['signal'].iloc[i] == -1 and position >= 0:
                    # Sell signal
                    if position > 0:
                        # Close existing long position
                        exit_price = close_price
                        profit_loss = position_size * (exit_price - entry_price)
                        capital += profit_loss
                        
                        # Update last trade with exit info
                        if trades:
                            trades[-1].update({
                                'exit_time': df.index[i],
                                'exit_price': exit_price,
                                'profit_loss': profit_loss,
                                'return_pct': (exit_price / entry_price - 1) * 100
                            })
                        
                        logger.debug(f"Closed long at {df.index[i]}, price: {exit_price}, P/L: {profit_loss}")
                    
                    # For simplicity, we'll just track short signals but not implement shorting
                    position = 0  # No position (or -1 if implementing shorts)
                
                # Check stop loss and take profit
                elif position > 0:
                    # Check stop loss
                    if close_price <= trades[-1]['stop_loss']:
                        # Stop loss hit
                        exit_price = trades[-1]['stop_loss']  # Assume we exit at exact stop loss
                        profit_loss = position_size * (exit_price - entry_price)
                        capital += profit_loss
                        
                        # Update trade
                        trades[-1].update({
                            'exit_time': df.index[i],
                            'exit_price': exit_price,
                            'profit_loss': profit_loss,
                            'return_pct': (exit_price / entry_price - 1) * 100,
                            'exit_reason': 'stop_loss'
                        })
                        
                        position = 0
                        logger.debug(f"Stop loss at {df.index[i]}, price: {exit_price}, P/L: {profit_loss}")
                    
                    # Check take profit
                    elif close_price >= trades[-1]['take_profit']:
                        # Take profit hit
                        exit_price = trades[-1]['take_profit']  # Assume we exit at exact take profit
                        profit_loss = position_size * (exit_price - entry_price)
                        capital += profit_loss
                        
                        # Update trade
                        trades[-1].update({
                            'exit_time': df.index[i],
                            'exit_price': exit_price,
                            'profit_loss': profit_loss,
                            'return_pct': (exit_price / entry_price - 1) * 100,
                            'exit_reason': 'take_profit'
                        })
                        
                        position = 0
                        logger.debug(f"Take profit at {df.index[i]}, price: {exit_price}, P/L: {profit_loss}")
            
            # Close any open position at the end
            if position != 0:
                final_price = df['close'].iloc[-1]
                profit_loss = position_size * (final_price - entry_price)
                capital += profit_loss
                
                # Update last trade
                if trades:
                    trades[-1].update({
                        'exit_time': df.index[-1],
                        'exit_price': final_price,
                        'profit_loss': profit_loss,
                        'return_pct': (final_price / entry_price - 1) * 100,
                        'exit_reason': 'end_of_backtest'
                    })
            
            # Calculate performance metrics
            if trades:
                profitable_trades = sum(1 for t in trades if t.get('profit_loss', 0) > 0)
                total_trades = len(trades)
                win_rate = profitable_trades / total_trades if total_trades > 0 else 0
                
                profit_factor = sum(t.get('profit_loss', 0) for t in trades if t.get('profit_loss', 0) > 0)
                loss_factor = abs(sum(t.get('profit_loss', 0) for t in trades if t.get('profit_loss', 0) < 0))
                profit_factor_ratio = profit_factor / loss_factor if loss_factor > 0 else float('inf')
                
                # Calculate returns
                total_return = (capital / initial_capital - 1) * 100
                annual_return = total_return * (252 / len(df)) if len(df) > 0 else 0
                
                # Calculate max drawdown
                equity_curve = np.array(equity_curve)
                max_drawdown = 0
                peak = equity_curve[0]
                
                for value in equity_curve:
                    if value > peak:
                        peak = value
                    drawdown = (peak - value) / peak
                    max_drawdown = max(max_drawdown, drawdown)
                
                max_drawdown_pct = max_drawdown * 100
                
                # Calculate Sharpe ratio (assuming risk-free rate of 0)
                if len(equity_curve) > 1:
                    returns = np.diff(equity_curve) / equity_curve[:-1]
                    sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252) if np.std(returns) > 0 else 0
                else:
                    sharpe_ratio = 0
            else:
                win_rate = 0
                profit_factor_ratio = 0
                total_return = 0
                annual_return = 0
                max_drawdown_pct = 0
                sharpe_ratio = 0
            
            # Prepare result dictionary
            results = {
                'initial_capital': initial_capital,
                'final_capital': capital,
                'total_return_pct': total_return,
                'annual_return_pct': annual_return,
                'max_drawdown_pct': max_drawdown_pct,
                'sharpe_ratio': sharpe_ratio,
                'total_trades': len(trades),
                'profitable_trades': profitable_trades if trades else 0,
                'win_rate': win_rate,
                'profit_factor': profit_factor_ratio,
                'equity_curve': equity_curve,
                'trades': trades
            }
            
            logger.info(f"Backtest results: Total return: {total_return:.2f}%, Win rate: {win_rate:.2f}, Sharpe: {sharpe_ratio:.2f}")
            return results
            
        except Exception as e:
            logger.error(f"Error during backtest: {str(e)}")
            return {
                'error': str(e),
                'initial_capital': initial_capital,
                'final_capital': initial_capital,
                'total_return_pct': 0,
                'trades': []
            } 