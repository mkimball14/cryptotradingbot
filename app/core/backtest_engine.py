import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
from uuid import uuid4
from decimal import Decimal

from app.models.order import OrderSide, OrderStatus, OrderType, TimeInForce, OrderBase # Using OrderBase
from app.models.position import Position
# Removed incorrect calculate_atr import
# from app.core.indicators import calculate_atr # Assuming ATR might be used
# Import Strategy base class from the correct file
from app.strategies.base.strategy import Strategy 

logger = logging.getLogger(__name__)

class BacktestEngine:
    """
    A backtesting engine that simulates trading with historical data,
    supporting both long and short positions, driven by a strategy object.
    """
    
    def __init__(self, 
                 historical_data: pd.DataFrame, 
                 strategy: Strategy, # Add strategy object
                 initial_balance: float = 10000.0,
                 trading_fee: float = 0.001, 
                 slippage_std: float = 0.001):
        """
        Initialize the backtest engine.
        
        Args:
            historical_data: DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            strategy: An instance of a class derived from Strategy.
            initial_balance: Starting account balance
            trading_fee: Fee per trade as a decimal (e.g., 0.001 for 0.1%)
            slippage_std: Standard deviation for slippage simulation
        """
        self.data = historical_data.copy()
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.available_balance = initial_balance
        self.trading_fee = trading_fee
        self.slippage_std = slippage_std
        
        # Trading state
        self.position: Optional[Position] = None
        self.position_size = 0.0 # Can be positive (long) or negative (short)
        self.current_index = 0
        
        # Performance tracking
        self.portfolio_values = pd.Series(index=self.data.index, dtype=float)
        self.portfolio_values.iloc[0] = initial_balance
        self.trades: List[Order] = []
        
        # --- Pre-calculate signals --- 
        print("Calculating strategy signals...")
        self.data_with_signals = self.strategy.generate_signals(self.data)
        print("Signals calculated.")
        # --- Debug Prints --- 
        if 'signal' in self.data_with_signals.columns:
            print(f"Signal Counts:\n{self.data_with_signals['signal'].value_counts()}")
        if 'regime' in self.data_with_signals.columns:
            print(f"Regime Counts:\n{self.data_with_signals['regime'].value_counts()}")
        entry_signals_in_uptrend = len(self.data_with_signals[(self.data_with_signals.get('signal') == 1) & (self.data_with_signals.get('regime') == 'uptrend')])
        print(f"Entry Signals (signal=1) during Uptrend: {entry_signals_in_uptrend}")
        # --- End Debug Prints ---
        
        # Determine first valid index after indicator calculations (e.g., SMA period)
        self.first_valid_index = self.data_with_signals.first_valid_index()
        if self.first_valid_index is None:
            # Find the first index where all essential signal columns are not NaN
            essential_cols = ['signal', 'rsi', 'regime', 'atr'] # Adapt as needed per strategy
            valid_indices = self.data_with_signals.dropna(subset=essential_cols).index
            self.first_valid_index = valid_indices.min() if not valid_indices.empty else 0
        else: # if pandas found one, use it directly
            self.first_valid_index = self.data.index.get_loc(self.first_valid_index)
            
        print(f"Starting backtest from index: {self.first_valid_index}")

    @property
    def has_position(self) -> bool:
        """Returns True if currently holding a long or short position."""
        return self.position_size != 0

    def execute_market_order(self, quantity: float, price: float, side: str) -> OrderBase:
        """
        Execute a market order with simulated slippage and fees.
        Handles opening/closing long and short positions.
        
        Args:
            quantity: Number of units to trade (always positive)
            price: Current market price
            side: 'buy' or 'sell'
        """
        if quantity <= 0:
            print(f"Warning: Attempted to execute order with quantity {quantity}. Skipping.")
            # Return a dummy rejected order
            timestamp = self.data.index[self.current_index]
            order = OrderBase(
                id=str(uuid4()), type=OrderType.MARKET, side=OrderSide(side),
                symbol="BACKTEST", quantity=quantity, price=price,
                status=OrderStatus.REJECTED, timestamp=timestamp
            )
            self.trades.append(order)
            return order

        # Simulate slippage
        slippage = np.random.normal(0, self.slippage_std)
        executed_price = price * (1 + slippage)
        
        # Calculate fees
        trade_value = quantity * executed_price
        fee_amount = trade_value * self.trading_fee
        
        order_side = OrderSide(side)
        timestamp = self.data.index[self.current_index]

        # Create base order object (status may change)
        order = OrderBase(
            id=str(uuid4()), type=OrderType.MARKET, side=order_side,
            symbol="BACKTEST", quantity=quantity, price=price,
            status=OrderStatus.PENDING, # Start as pending, update later
            timestamp=timestamp, filled_price=executed_price,
            filled_quantity=quantity, filled_timestamp=timestamp,
            fees=fee_amount
        )

        # --- Logic based on order side and current position --- 

        if order_side == OrderSide.BUY:
            # --- Buy Logic --- 
            if self.position_size == 0: # Buy to Open Long
                cost = trade_value + fee_amount
                if cost > self.available_balance:
                    order.status = OrderStatus.REJECTED
                    # print(f"[{timestamp.date()}] Buy order REJECTED - Insufficient funds.")
                else:
                    self.available_balance -= cost
                    self.position = Position(
                        symbol="BACKTEST", quantity=quantity, entry_price=executed_price,
                        current_price=executed_price, timestamp=timestamp, fees=fee_amount
                    )
                    self.position_size = quantity
                    order.status = OrderStatus.FILLED
                    self.trades.append(order)
                    # Update strategy state
                    self.strategy.update_state(timestamp=timestamp, is_in_position=True, position_size=quantity, entry_price=executed_price)
                    print(f"[{timestamp.date()}] Opened LONG @ {executed_price:.2f}, Size: {quantity:.4f}")

            elif self.position_size < 0: # Buy to Close Short
                close_quantity = min(quantity, abs(self.position_size))
                if close_quantity <= 0: # Avoid zero or negative close quantity
                     order.status = OrderStatus.REJECTED
                     # print(f"[{timestamp.date()}] Buy to close REJECTED - Invalid quantity: {close_quantity}")
                     return order
                 
                order.quantity = close_quantity # Adjust order quantity if needed
                trade_value = close_quantity * executed_price
                fee_amount = trade_value * self.trading_fee
                order.fees = fee_amount
                
                cost = trade_value + fee_amount
                # P&L for Short: (Entry Sell Price - Exit Buy Price) * Size - Fees
                entry_value = self.position.entry_price * close_quantity
                exit_value = executed_price * close_quantity
                # Pro-rate entry fees based on the proportion of the position being closed
                entry_fee_proportion = self.position.fees * (close_quantity / abs(self.position.quantity))
                realized_pnl = entry_value - exit_value - fee_amount - entry_fee_proportion
                
                self.available_balance -= cost # Cost of buying back
                # We already received cash when opening short, PnL adjusts balance here
                self.available_balance += (entry_value - exit_value)
                
                order.realized_pnl = realized_pnl # Store PnL on the closing order
                order.status = OrderStatus.FILLED
                self.trades.append(order)
                self.position_size += close_quantity # Reduce the magnitude of negative size
                print(f"[{timestamp.date()}] Closed SHORT @ {executed_price:.2f}, Size: {close_quantity:.4f}, PnL: {realized_pnl:.2f}")

                if np.isclose(self.position_size, 0): # Check for close to zero float comparison
                    self.position = None # Clear position details
                    self.position_size = 0.0
                    self.strategy.update_state(timestamp=timestamp, is_in_position=False, position_size=0.0, entry_price=None)
                else: # Update remaining position details (e.g., average price could be recalculated if needed)
                     self.position.quantity = self.position_size # Update remaining quantity
                     self.strategy.update_state(timestamp=timestamp, is_in_position=True, position_size=self.position_size, entry_price=self.position.entry_price)

            else: # Already long, cannot buy more (simple model assumes one position)
                order.status = OrderStatus.REJECTED
                # print(f"[{timestamp.date()}] Buy order REJECTED - Already long.")

        elif order_side == OrderSide.SELL:
            # --- Sell Logic ---
            if self.position_size == 0: # Sell to Open Short
                # Assuming futures/margin - no need to check for asset ownership
                # Calculate cash change from opening short
                cash_received = trade_value - fee_amount
                self.available_balance += cash_received 
                self.position = Position(
                    symbol="BACKTEST", quantity=quantity, entry_price=executed_price,
                    current_price=executed_price, timestamp=timestamp, fees=fee_amount
                )
                self.position_size = -quantity # Negative size for short
                order.status = OrderStatus.FILLED
                self.trades.append(order)
                # Update strategy state
                self.strategy.update_state(timestamp=timestamp, is_in_position=True, position_size=-quantity, entry_price=executed_price)
                print(f"[{timestamp.date()}] Opened SHORT @ {executed_price:.2f}, Size: {quantity:.4f}")

            elif self.position_size > 0: # Sell to Close Long
                close_quantity = min(quantity, self.position_size)
                if close_quantity <= 0:
                    order.status = OrderStatus.REJECTED
                    # print(f"[{timestamp.date()}] Sell to close REJECTED - Invalid quantity: {close_quantity}")
                    return order
                
                order.quantity = close_quantity # Adjust order quantity if needed
                trade_value = close_quantity * executed_price
                fee_amount = trade_value * self.trading_fee
                order.fees = fee_amount
                
                revenue = trade_value - fee_amount
                # P&L for Long: (Exit Sell Price - Entry Buy Price) * Size - Fees
                entry_value = self.position.entry_price * close_quantity
                exit_value = executed_price * close_quantity
                # Pro-rate entry fees based on the proportion of the position being closed
                entry_fee_proportion = self.position.fees * (close_quantity / self.position.quantity)
                realized_pnl = exit_value - entry_value - fee_amount - entry_fee_proportion
                
                self.available_balance += revenue
                order.realized_pnl = realized_pnl # Store PnL on the closing order
                order.status = OrderStatus.FILLED
                self.trades.append(order)
                self.position_size -= close_quantity
                print(f"[{timestamp.date()}] Closed LONG @ {executed_price:.2f}, Size: {close_quantity:.4f}, PnL: {realized_pnl:.2f}")
                
                if np.isclose(self.position_size, 0):
                    self.position = None # Clear position details
                    self.position_size = 0.0
                    self.strategy.update_state(timestamp=timestamp, is_in_position=False, position_size=0.0, entry_price=None)
                else: # Update remaining position details
                    self.position.quantity = self.position_size
                    self.strategy.update_state(timestamp=timestamp, is_in_position=True, position_size=self.position_size, entry_price=self.position.entry_price)

            else: # Already short, cannot sell more (simple model assumes one position)
                order.status = OrderStatus.REJECTED
                # print(f"[{timestamp.date()}] Sell order REJECTED - Already short.")
                
        # Update portfolio value after any state change that resulted in a fill
        if order.status == OrderStatus.FILLED:
            self.update_portfolio_value()
        
        return order
    
    def update_portfolio_value(self):
        """Updates the portfolio value for the current index."""
        # Ensure index is valid
        if self.current_index < 0 or self.current_index >= len(self.data):
             return
             
        total_value = self.available_balance
        if self.position_size != 0 and self.position is not None:
            current_close = self.data.iloc[self.current_index]['close'] 
            # MTM value = (Current Price - Entry Price) * Size
            mtm_value = (current_close - self.position.entry_price) * self.position_size
            # Total value = Cash + Initial Cost + MTM Value 
            # For Long: Initial Cost was cash outflow, so Cash + MTM Value + (Entry * Size)
            # For Short: Initial Cost was cash inflow, so Cash + MTM Value + (Entry * Size)
            # This simplifies to: Cash + Current Value of Position
            total_value += self.position_size * current_close 
        
        # Ensure index exists in portfolio_values Series before assignment
        current_timestamp = self.data.index[self.current_index]
        if current_timestamp in self.portfolio_values.index:
             self.portfolio_values.loc[current_timestamp] = total_value
        else:
             # Handle cases where timestamp might not align perfectly, though self.data.index should be correct
             print(f"Warning: Timestamp {current_timestamp} not found in portfolio_values index.")
             # Optionally, append or reindex, but ideally the index should match
             pass 

    def run(self):
        """Run the backtest simulation."""
        print(f"Running backtest for {len(self.data_with_signals)} periods...")
        
        # Skip initial periods where indicators might be NaN
        start_index = max(self.first_valid_index, 0) 
        
        for i in range(start_index, len(self.data_with_signals)):
            self.current_index = i
            current_row = self.data_with_signals.iloc[i]
            current_price = current_row['close'] # Use close price for decisions/execution
            timestamp = current_row.name # Get timestamp from the index name
            
            # --- Debug Print --- 
            # print(f"[{timestamp.date()}] Price: {current_price:.2f}, RSI: {current_row.get('rsi', 'N/A'):.2f}, Regime: {current_row.get('regime', 'N/A')}, Signal: {current_row.get('signal', 'N/A')}, InPos: {self.strategy.state.is_in_position}")
            # --- End Debug Print --- 

            # --- Strategy Logic --- 
            # 1. Check for Exit Signal (includes stop check via strategy state)
            if self.strategy.state.is_in_position and self.strategy.should_exit_trade(current_row):
                # print(f"[{timestamp.date()}] Exit signal detected @ {current_price:.2f}")
                if self.position_size > 0: # Exit Long
                    self.execute_market_order(quantity=self.position_size, price=current_price, side='sell')
                    # state updated within execute_market_order, including resetting trailing stop
                # Add short exit logic if needed in the future
                # elif self.position_size < 0: # Exit Short
                #     self.execute_market_order(quantity=abs(self.position_size), price=current_price, side='buy')
                    
            # 2. Check for Entry Signal (only if not already in position)
            elif not self.strategy.state.is_in_position and self.strategy.should_enter_trade(current_row):
                # print(f"[{timestamp.date()}] Entry signal detected @ {current_price:.2f}")
                # Use the pre-calculated stop_loss from generate_signals for consistency
                initial_stop_loss_price = current_row.get('stop_loss', np.nan)
                
                if pd.isna(initial_stop_loss_price) or initial_stop_loss_price >= current_price:
                    print(f"Warning: Invalid initial stop loss ({initial_stop_loss_price}) vs entry ({current_price:.2f}). Skipping trade.")
                    self.update_portfolio_value() 
                    continue 
                
                position_size = self.strategy.calculate_position_size(
                    account_balance=self.available_balance, 
                    entry_price=current_price, 
                    stop_loss_price=initial_stop_loss_price
                )
                
                if position_size > 0:
                    order = self.execute_market_order(quantity=position_size, price=current_price, side='buy')
                    # If filled, set the initial stop in the strategy state 
                    # (using the name trailing_stop_price for now, though it's fixed for this strategy)
                    if order.status == OrderStatus.FILLED:
                         self.strategy.update_state(timestamp=timestamp,
                                                    is_in_position=True,
                                                    position_size=self.position_size,
                                                    entry_price=self.position.entry_price, 
                                                    regime=current_row.get('regime'),
                                                    trailing_stop_price=initial_stop_loss_price) # Set initial stop
                else:
                    print(f"Warning: Calculated position size is {position_size:.4f}. Skipping trade.")
            
            # 3. Update portfolio value
            self.update_portfolio_value()
                 
            # Update strategy state with current regime (trailing stop is set on entry or reset on exit)
            if 'regime' in current_row and not self.strategy.state.is_in_position:
                 # Only update regime if not in position, otherwise keep entry regime state?
                 # Or always update? Let's always update for now.
                 self.strategy.update_state(timestamp=timestamp, 
                                            is_in_position=self.strategy.state.is_in_position, 
                                            position_size=self.strategy.state.current_position_size,
                                            entry_price=self.strategy.state.entry_price,
                                            regime=current_row['regime']) 
                                            # Trailing stop state persists until explicitly reset on exit by execute_market_order

        print("Backtest finished.")
        # Fill any remaining NaNs at the end
        self.portfolio_values.ffill(inplace=True)

    def get_performance_metrics(self) -> Dict:
        """Calculate and return performance metrics for the backtest."""
        # Ensure the last value is updated before filling forward
        # Call update_portfolio_value one last time for the final index? Or handle in run loop end?
        # self.update_portfolio_value() 
        # Fill forward portfolio values for periods with no updates (e.g., initial skip)
        self.portfolio_values.ffill(inplace=True)
        
        # Calculate returns
        # Filter out potential initial NaN or zero values before calculating pct_change
        valid_portfolio_values = self.portfolio_values.loc[self.portfolio_values.notna() & (self.portfolio_values != 0)]
        if len(valid_portfolio_values) < 2:
            # Not enough data points to calculate meaningful metrics
            return {
                 'total_return': 0.0,
                 'annualized_return': 0.0,
                 'sharpe_ratio': 0.0,
                 'max_drawdown': 0.0,
                 'num_trades': len(self.trades)
             }

        returns = valid_portfolio_values.pct_change().dropna()
        if returns.empty:
             return {
                 'total_return': (self.portfolio_values.iloc[-1] / self.initial_balance) - 1 if len(self.portfolio_values) > 0 and self.portfolio_values.iloc[-1] else 0.0,
                 'annualized_return': 0.0,
                 'sharpe_ratio': 0.0,
                 'max_drawdown': 0.0,
                 'num_trades': len(self.trades)
             }

        
        # Calculate metrics
        total_return = (self.portfolio_values.iloc[-1] / self.initial_balance) - 1
        # Use number of trading days in the returns series for annualization
        trading_days_in_data = (self.data.index[-1] - self.data.index[0]).days
        # Use number of trading days observed in returns for annualization factor
        observed_trading_days = len(returns) if len(returns) > 0 else 1 # Avoid division by zero
        annualization_factor = 252 / observed_trading_days # Assuming 252 trading days/year

        annualized_return = ((1 + total_return) ** annualization_factor) - 1 if total_return is not None else 0.0
        
        # Calculate Sharpe Ratio (assuming risk-free rate of 0.0)
        excess_returns = returns # Simpler assumption for now
        returns_std = returns.std()
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns_std if returns_std != 0 and returns_std is not np.nan else 0.0
        
        # Calculate Maximum Drawdown
        # Ensure we start calculation from initial balance to capture full drawdown
        portfolio_to_analyze = pd.concat([pd.Series([self.initial_balance], index=[self.data.index[0] - pd.Timedelta(days=1)]), self.portfolio_values])
        portfolio_to_analyze.ffill(inplace=True)
        rolling_max = portfolio_to_analyze.cummax()
        drawdowns = portfolio_to_analyze / rolling_max - 1
        max_drawdown = drawdowns.min()
        
        return {
            'total_return': total_return if total_return is not None else 0.0,
            'annualized_return': annualized_return if annualized_return is not None else 0.0,
            'sharpe_ratio': sharpe_ratio if sharpe_ratio is not None else 0.0,
            'max_drawdown': max_drawdown if max_drawdown is not None else 0.0,
            'num_trades': len(self.trades)
        } 