import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from pathlib import Path
import datetime as dt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the system path to import our modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import our strategy
from scripts.strategies.candlestick_pattern_strategy import CandlestickPatternStrategy

def load_test_data():
    """Load sample data for testing the strategy"""
    try:
        # Try to load from a CSV file if available
        csv_path = Path(__file__).resolve().parent / 'test_data' / 'sample_ohlc_data.csv'
        
        if csv_path.exists():
            logger.info(f"Loading test data from {csv_path}")
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            return df
        
        # If no CSV exists, generate synthetic data
        logger.info("Generating synthetic test data")
        
        # Generate datetime index
        days = pd.date_range(start='2020-01-01', periods=500, freq='D')
        
        # Generate synthetic price data with some patterns
        np.random.seed(42)  # For reproducibility
        
        # Start with a base price and add random walk
        close = 100.0
        closes = [close]
        
        for _ in range(1, 500):
            # Random walk with some mean reversion
            pct_change = np.random.normal(0, 0.015)  # 1.5% daily volatility
            if close > 150:  # Mean reversion if price gets too high
                pct_change -= 0.002
            elif close < 50:  # Mean reversion if price gets too low
                pct_change += 0.002
                
            close = close * (1 + pct_change)
            closes.append(close)
        
        # Generate OHLC data with some realistic candle patterns
        df = pd.DataFrame(index=days)
        df['close'] = closes
        
        # Generate realistic open, high, low values
        for i in range(len(df)):
            # First day
            if i == 0:
                df.loc[df.index[i], 'open'] = df.loc[df.index[i], 'close'] * (1 - 0.005)
                continue
                
            # Other days: open near previous close
            prev_close = df.loc[df.index[i-1], 'close']
            
            # Occasionally create gaps up or down (10% chance)
            if np.random.random() < 0.1:
                gap_factor = np.random.normal(0, 0.01)  # 1% gap on average
                df.loc[df.index[i], 'open'] = prev_close * (1 + gap_factor)
            else:
                # Open near previous close
                df.loc[df.index[i], 'open'] = prev_close * (1 + np.random.normal(0, 0.003))
                
            # Determine if bullish or bearish candle
            is_bullish = df.loc[df.index[i], 'close'] > df.loc[df.index[i], 'open']
            
            # Generate high and low
            daily_volatility = abs(df.loc[df.index[i], 'close'] - df.loc[df.index[i], 'open']) * 2
            if daily_volatility < 0.001 * df.loc[df.index[i], 'close']:
                daily_volatility = 0.001 * df.loc[df.index[i], 'close']  # Minimum volatility
                
            # Occasionally create long wicks (hammer, shooting star, etc.)
            upper_wick = daily_volatility * np.random.exponential(0.5)
            lower_wick = daily_volatility * np.random.exponential(0.5)
            
            # 5% chance of a doji
            if np.random.random() < 0.05:
                df.loc[df.index[i], 'open'] = df.loc[df.index[i], 'close'] * (1 + np.random.normal(0, 0.001))
                # Doji often have long wicks
                upper_wick = daily_volatility * np.random.exponential(1.5)
                lower_wick = daily_volatility * np.random.exponential(1.5)
            
            # Set high and low
            if is_bullish:
                df.loc[df.index[i], 'high'] = max(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) + upper_wick
                df.loc[df.index[i], 'low'] = min(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) - lower_wick
            else:
                df.loc[df.index[i], 'high'] = max(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) + upper_wick
                df.loc[df.index[i], 'low'] = min(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) - lower_wick
                
        # Add volume data for completeness
        df['volume'] = np.random.exponential(scale=1000000, size=len(df))
        
        # Occasionally make volume spikes on big price moves
        big_moves = abs(df['close'].pct_change()) > 0.02
        df.loc[big_moves, 'volume'] = df.loc[big_moves, 'volume'] * 2.5
                
        # Save data for future use
        os.makedirs(Path(__file__).resolve().parent / 'test_data', exist_ok=True)
        df.to_csv(csv_path)
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading/generating test data: {str(e)}")
        # Return minimal viable test data
        return pd.DataFrame({
            'open': [100, 101, 99, 102, 103],
            'high': [105, 103, 100, 104, 105],
            'low': [98, 98, 95, 100, 101],
            'close': [101, 99, 100, 103, 102],
            'volume': [1000000, 1200000, 900000, 1500000, 1100000]
        }, index=pd.date_range(start='2020-01-01', periods=5))

class MockBroker:
    """Mock broker for testing strategy execution"""
    def __init__(self, initial_capital=10000.0):
        self.portfolio_value = initial_capital
        self.cash = initial_capital
        self.positions = {}
        self.order_id_counter = 0
        self.orders = {}
        
    def get_portfolio_value(self):
        """Get current portfolio value"""
        return self.portfolio_value
    
    def can_buy(self, symbol, quantity, price):
        """Check if we can buy given position"""
        return self.cash >= quantity * price
    
    def place_order(self, symbol, order_type, side, quantity):
        """Place a new order"""
        self.order_id_counter += 1
        order_id = f"order_{self.order_id_counter}"
        
        # Process market orders immediately
        if order_type == 'market':
            if side == 'buy':
                # Check if we have enough cash
                price = float(quantity)  # Mock price = quantity for simplicity
                cost = price * quantity
                
                if cost <= self.cash:
                    # Add to positions
                    if symbol in self.positions:
                        self.positions[symbol]['quantity'] += quantity
                        self.positions[symbol]['value'] += cost
                    else:
                        self.positions[symbol] = {
                            'quantity': quantity,
                            'value': cost
                        }
                    
                    # Update cash
                    self.cash -= cost
                    
                    # Record order
                    self.orders[order_id] = {
                        'symbol': symbol,
                        'type': order_type,
                        'side': side,
                        'quantity': quantity,
                        'price': price,
                        'status': 'filled',
                        'filled_at': dt.datetime.now()
                    }
                    
                    return order_id
                else:
                    # Not enough cash
                    self.orders[order_id] = {
                        'symbol': symbol,
                        'type': order_type,
                        'side': side,
                        'quantity': quantity,
                        'status': 'rejected',
                        'reason': 'insufficient_funds'
                    }
                    return None
            
            elif side == 'sell':
                # Check if we have the position
                if symbol in self.positions and self.positions[symbol]['quantity'] >= quantity:
                    # Calculate proceeds
                    price = float(quantity)  # Mock price = quantity for simplicity
                    proceeds = price * quantity
                    
                    # Update positions
                    self.positions[symbol]['quantity'] -= quantity
                    avg_price = self.positions[symbol]['value'] / (self.positions[symbol]['quantity'] + quantity)
                    self.positions[symbol]['value'] -= avg_price * quantity
                    
                    # Remove position if quantity is 0
                    if self.positions[symbol]['quantity'] <= 0:
                        del self.positions[symbol]
                    
                    # Update cash
                    self.cash += proceeds
                    
                    # Record order
                    self.orders[order_id] = {
                        'symbol': symbol,
                        'type': order_type,
                        'side': side,
                        'quantity': quantity,
                        'price': price,
                        'status': 'filled',
                        'filled_at': dt.datetime.now()
                    }
                    
                    return order_id
                else:
                    # Insufficient position
                    self.orders[order_id] = {
                        'symbol': symbol,
                        'type': order_type,
                        'side': side,
                        'quantity': quantity,
                        'status': 'rejected',
                        'reason': 'insufficient_position'
                    }
                    return None
        
        # Update portfolio value
        self.portfolio_value = self.cash + sum(pos['value'] for pos in self.positions.values())
        
        return order_id

def test_strategy_preparation():
    """Test the strategy data preparation"""
    # Load test data
    df = load_test_data()
    
    # Initialize strategy
    strategy = CandlestickPatternStrategy()
    
    # Prepare data
    logger.info("Testing strategy data preparation...")
    prepared_df = strategy.prepare_data(df)
    
    # Check if candle pattern columns were added
    pattern_cols = [col for col in prepared_df.columns if col.startswith('CDL')]
    logger.info(f"Found {len(pattern_cols)} candlestick pattern columns")
    
    if len(pattern_cols) == 0:
        logger.warning("No candlestick pattern columns were found!")
    else:
        # Show top patterns
        non_zero_patterns = {}
        for col in pattern_cols:
            non_zero_count = (prepared_df[col] != 0).sum()
            if non_zero_count > 0:
                non_zero_patterns[col] = non_zero_count
        
        top_patterns = sorted(non_zero_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        logger.info(f"Top 5 patterns by frequency: {top_patterns}")
    
    # Check if buy/sell signals were generated
    if 'candle_buy_signal' in prepared_df.columns and 'candle_sell_signal' in prepared_df.columns:
        buy_signals = prepared_df['candle_buy_signal'].sum()
        sell_signals = prepared_df['candle_sell_signal'].sum()
        logger.info(f"Generated {buy_signals} buy signals and {sell_signals} sell signals")
    else:
        logger.warning("Buy/sell signal columns not found!")
    
    return prepared_df

def test_strategy_signals():
    """Test the strategy signal generation"""
    # Load test data
    df = load_test_data()
    
    # Initialize strategy
    strategy = CandlestickPatternStrategy()
    
    # Prepare data
    prepared_df = strategy.prepare_data(df)
    
    # Generate signals
    logger.info("Testing strategy signal generation...")
    signal_df = strategy.generate_signals(prepared_df)
    
    # Check if signal and position columns were added
    if 'signal' in signal_df.columns:
        buy_signals = (signal_df['signal'] == 1).sum()
        sell_signals = (signal_df['signal'] == -1).sum()
        logger.info(f"Generated {buy_signals} buy signals and {sell_signals} sell signals")
    else:
        logger.warning("Signal column not found!")
    
    if 'position' in signal_df.columns:
        long_positions = (signal_df['position'] == 1).sum()
        short_positions = (signal_df['position'] == -1).sum()
        logger.info(f"Generated {long_positions} long positions and {short_positions} short positions")
    else:
        logger.warning("Position column not found!")
    
    return signal_df

def test_strategy_backtest():
    """Test the strategy backtest functionality"""
    # Load test data
    df = load_test_data()
    
    # Test with different configurations
    test_configs = [
        {
            "name": "Default Config",
            "config": None  # Use default config
        },
        {
            "name": "Higher Min Strength",
            "config": {"min_strength": 0.05}
        },
        {
            "name": "No Confirmation",
            "config": {"use_confirmation": False}
        },
        {
            "name": "More Risk",
            "config": {"risk_per_trade": 0.05, "stop_loss_pct": 0.03}
        }
    ]
    
    # Run backtest for each configuration
    results = {}
    for test in test_configs:
        logger.info(f"Testing backtest with {test['name']}...")
        
        # Initialize strategy
        strategy = CandlestickPatternStrategy(config=test['config'])
        
        # Run backtest
        backtest_result = strategy.backtest(df, initial_capital=10000.0)
        
        # Log results
        logger.info(f"Backtest results for {test['name']}:")
        logger.info(f"  Total Return: {backtest_result['total_return_pct']:.2f}%")
        logger.info(f"  Win Rate: {backtest_result['win_rate'] * 100:.2f}%")
        logger.info(f"  Trades: {backtest_result['total_trades']}")
        logger.info(f"  Sharpe Ratio: {backtest_result['sharpe_ratio']:.2f}")
        logger.info(f"  Max Drawdown: {backtest_result['max_drawdown_pct']:.2f}%")
        
        # Store results
        results[test['name']] = backtest_result
    
    return results

def test_trade_execution():
    """Test the strategy trade execution"""
    # Load test data
    df = load_test_data()
    
    # Initialize strategy with no confirmation
    strategy = CandlestickPatternStrategy(config={"use_confirmation": False})
    
    # Prepare data and generate signals
    prepared_df = strategy.prepare_data(df)
    signal_df = strategy.generate_signals(prepared_df)
    
    # Initialize mock broker
    broker = MockBroker(initial_capital=10000.0)
    
    # Execute trades for each signal
    executed_trades = []
    for i in range(len(signal_df)):
        # Skip first 50 rows for lookback
        if i < 50:
            continue
            
        # Get data slice up to this point
        df_slice = signal_df.iloc[:i+1]
        
        # Execute trades based on the current signal
        trades = strategy.execute_trades(df_slice, broker)
        executed_trades.extend(trades)
    
    # Report execution results
    logger.info(f"Executed {len(executed_trades)} trades in total")
    logger.info(f"Final portfolio value: ${broker.portfolio_value:.2f}")
    
    # Count buys and sells
    buys = sum(1 for t in executed_trades if t['type'] == 'buy')
    sells = sum(1 for t in executed_trades if t['type'] == 'sell')
    logger.info(f"Buy trades: {buys}, Sell trades: {sells}")
    
    return {
        'executed_trades': executed_trades,
        'broker': broker
    }

def plot_backtest_results(signal_df, backtest_result):
    """
    Plot the backtest results including price chart, signals, and equity curve.
    
    Args:
        signal_df: DataFrame with price data and signals
        backtest_result: Dictionary with backtest results
    """
    try:
        # Create plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # Plot price
        ax1.plot(signal_df.index, signal_df['close'], label='Price', color='blue')
        
        # Plot buy signals
        buy_signals = signal_df[signal_df['signal'] == 1]
        ax1.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', s=100, label='Buy Signal')
        
        # Plot sell signals
        sell_signals = signal_df[signal_df['signal'] == -1]
        ax1.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', s=100, label='Sell Signal')
        
        # Plot trades
        for trade in backtest_result['trades']:
            if 'entry_time' in trade and 'exit_time' in trade:
                entry_time = trade['entry_time']
                exit_time = trade['exit_time']
                entry_price = trade['entry_price']
                exit_price = trade['exit_price']
                
                # Plot entry point
                ax1.annotate('', xy=(entry_time, entry_price), xytext=(entry_time, entry_price * 0.97),
                            arrowprops=dict(arrowstyle='-|>', color='green' if trade['type'] == 'buy' else 'red'))
                
                # Plot exit point
                ax1.annotate('', xy=(exit_time, exit_price), xytext=(exit_time, exit_price * 1.03),
                            arrowprops=dict(arrowstyle='-|>', color='red'))
                
                # Connect entry and exit with a line
                ax1.plot([entry_time, exit_time], [entry_price, exit_price], 
                         color='green' if exit_price > entry_price else 'red',
                         linewidth=1, linestyle='--')
        
        # Format price chart
        ax1.set_title('Candlestick Pattern Strategy Backtest')
        ax1.set_ylabel('Price')
        ax1.grid(True)
        ax1.legend()
        
        # Plot equity curve
        ax2.plot(signal_df.index[:len(backtest_result['equity_curve'])], 
                 backtest_result['equity_curve'], label='Equity', color='purple')
        
        # Format equity curve
        ax2.set_title('Equity Curve')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Portfolio Value')
        ax2.grid(True)
        
        # Add performance metrics as text
        text = (
            f"Total Return: {backtest_result['total_return_pct']:.2f}%\n"
            f"Annual Return: {backtest_result['annual_return_pct']:.2f}%\n"
            f"Sharpe Ratio: {backtest_result['sharpe_ratio']:.2f}\n"
            f"Max Drawdown: {backtest_result['max_drawdown_pct']:.2f}%\n"
            f"Win Rate: {backtest_result['win_rate'] * 100:.2f}%\n"
            f"Trades: {backtest_result['total_trades']}"
        )
        
        plt.figtext(0.01, 0.01, text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        plot_path = Path(__file__).resolve().parent / 'test_data' / 'backtest_plot.png'
        plt.savefig(plot_path)
        logger.info(f"Backtest plot saved to {plot_path}")
        
        # Close the plot
        plt.close()
        
    except Exception as e:
        logger.error(f"Error plotting backtest results: {str(e)}")

def main():
    """Run all tests"""
    logger.info("Starting candlestick pattern strategy tests")
    
    # Test strategy data preparation
    prepared_df = test_strategy_preparation()
    
    # Test strategy signal generation
    signal_df = test_strategy_signals()
    
    # Test strategy backtest
    backtest_results = test_strategy_backtest()
    
    # Test trade execution
    execution_results = test_trade_execution()
    
    # Plot the backtest results for the default config
    if 'Default Config' in backtest_results:
        plot_backtest_results(signal_df, backtest_results['Default Config'])
    
    logger.info("All tests completed")
    
    # Return results for inspection
    return {
        'prepared_df': prepared_df,
        'signal_df': signal_df,
        'backtest_results': backtest_results,
        'execution_results': execution_results
    }

if __name__ == "__main__":
    test_results = main() 