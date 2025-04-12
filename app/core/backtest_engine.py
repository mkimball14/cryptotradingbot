import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from .models import Order, OrderSide, OrderStatus, OrderType, Position

class BacktestEngine:
    """
    A backtesting engine that simulates trading with historical data,
    supporting both long and short positions.
    """
    
    def __init__(self, historical_data: pd.DataFrame, initial_balance: float = 10000.0,
                 trading_fee: float = 0.001, slippage_std: float = 0.001):
        """
        Initialize the backtest engine.
        
        Args:
            historical_data: DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            initial_balance: Starting account balance
            trading_fee: Fee per trade as a decimal (e.g., 0.001 for 0.1%)
            slippage_std: Standard deviation for slippage simulation
        """
        self.data = historical_data.copy()
        self.current_index = 0
        self.initial_balance = initial_balance
        self.available_balance = initial_balance
        self.trading_fee = trading_fee
        self.slippage_std = slippage_std
        
        # Trading state
        self.position: Optional[Position] = None
        self.position_size = 0.0
        
        # Performance tracking
        self.portfolio_values = pd.Series(index=self.data.index, dtype=float)
        self.portfolio_values.iloc[0] = initial_balance
        self.trades: List[Order] = []
        
    @property
    def has_position(self) -> bool:
        """Returns True if currently holding a long or short position."""
        return self.position_size != 0

    def execute_market_order(self, quantity: float, price: float, side: str) -> Order:
        """
        Execute a market order with simulated slippage and fees.
        Handles opening/closing long and short positions.
        
        Args:
            quantity: Number of units to trade (always positive)
            price: Current market price
            side: 'buy' or 'sell'
        """
        if quantity <= 0:
            raise ValueError("Order quantity must be positive.")

        # Simulate slippage
        slippage = np.random.normal(0, self.slippage_std)
        executed_price = price * (1 + slippage)
        
        # Calculate fees
        trade_value = quantity * executed_price
        fee_amount = trade_value * self.trading_fee
        
        order_side = OrderSide(side)
        timestamp = self.data.iloc[self.current_index]['timestamp']

        # Create base order object (status may change)
        order = Order(
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
                    print(f"[{timestamp.date()}] Buy order REJECTED - Insufficient funds.")
                else:
                    self.available_balance -= cost
                    self.position = Position(
                        symbol="BACKTEST", quantity=quantity, entry_price=executed_price,
                        current_price=executed_price, timestamp=timestamp, fees=fee_amount
                    )
                    self.position_size = quantity
                    order.status = OrderStatus.FILLED
                    self.trades.append(order)
                    print(f"[{timestamp.date()}] Opened LONG @ {executed_price:.2f}")

            elif self.position_size < 0: # Buy to Close Short
                if quantity > abs(self.position_size):
                    order.status = OrderStatus.REJECTED # Cannot buy more than shorted
                    print(f"[{timestamp.date()}] Buy to close REJECTED - Quantity too large.")
                else:
                    cost = trade_value + fee_amount
                    # P&L for Short: (Entry Sell Price - Exit Buy Price) * Size - Fees
                    entry_value = self.position.entry_price * quantity
                    exit_value = executed_price * quantity
                    realized_pnl = entry_value - exit_value - fee_amount - (self.position.fees * (quantity / abs(self.position_size))) # Pro-rate entry fees
                    
                    self.available_balance -= cost # Cost of buying back
                    # We already received cash when opening short, PnL adjusts balance here
                    self.available_balance += (entry_value - exit_value) 
                    
                    order.realized_pnl = realized_pnl # Store PnL on the closing order
                    order.status = OrderStatus.FILLED
                    self.trades.append(order)
                    self.position_size += quantity # Reduce the magnitude of negative size
                    print(f"[{timestamp.date()}] Closed SHORT @ {executed_price:.2f}, PnL: {realized_pnl:.2f}")

                    if self.position_size == 0:
                        self.position = None # Clear position details
            else: # Already long, cannot buy more (simple model assumes one position)
                order.status = OrderStatus.REJECTED
                print(f"[{timestamp.date()}] Buy order REJECTED - Already long.")

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
                print(f"[{timestamp.date()}] Opened SHORT @ {executed_price:.2f}")

            elif self.position_size > 0: # Sell to Close Long
                if quantity > self.position_size:
                    order.status = OrderStatus.REJECTED # Cannot sell more than held
                    print(f"[{timestamp.date()}] Sell to close REJECTED - Quantity too large.")
                else:
                    revenue = trade_value - fee_amount
                    # P&L for Long: (Exit Sell Price - Entry Buy Price) * Size - Fees
                    entry_value = self.position.entry_price * quantity
                    exit_value = executed_price * quantity
                    realized_pnl = exit_value - entry_value - fee_amount - (self.position.fees * (quantity / self.position_size)) # Pro-rate entry fees
                    
                    self.available_balance += revenue
                    order.realized_pnl = realized_pnl # Store PnL on the closing order
                    order.status = OrderStatus.FILLED
                    self.trades.append(order)
                    self.position_size -= quantity
                    print(f"[{timestamp.date()}] Closed LONG @ {executed_price:.2f}, PnL: {realized_pnl:.2f}")
                    
                    if self.position_size == 0:
                        self.position = None # Clear position details
            else: # Already short, cannot sell more (simple model assumes one position)
                order.status = OrderStatus.REJECTED
                print(f"[{timestamp.date()}] Sell order REJECTED - Already short.")
                
        # Update portfolio value after any state change
        if order.status == OrderStatus.FILLED:
            self.update_portfolio_value()
        
        return order
    
    def update_portfolio_value(self):
        """Updates the portfolio value for the current index."""
        total_value = self.available_balance
        if self.position_size != 0:
            current_close = self.data.iloc[self.current_index]['close'] 
            # Value is cash + mark-to-market value of position
            # For short: position_size is negative, represents liability at current_close
            total_value += self.position_size * current_close
        self.portfolio_values.iloc[self.current_index] = total_value

    def get_performance_metrics(self) -> Dict:
        """Calculate and return performance metrics for the backtest."""
        # Ensure the last value is updated before filling forward
        self.update_portfolio_value() 
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
                 'total_return': (self.portfolio_values.iloc[-1] / self.initial_balance) - 1 if self.portfolio_values.iloc[-1] else 0.0,
                 'annualized_return': 0.0,
                 'sharpe_ratio': 0.0,
                 'max_drawdown': 0.0,
                 'num_trades': len(self.trades)
             }

        
        # Calculate metrics
        total_return = (self.portfolio_values.iloc[-1] / self.initial_balance) - 1
        # Use number of trading days in the returns series for annualization
        annualized_return = ((1 + total_return) ** (252 / len(returns))) - 1 if len(returns) > 0 else 0.0
        
        # Calculate Sharpe Ratio (assuming risk-free rate of 0.0)
        excess_returns = returns # Simpler assumption for now
        returns_std = returns.std()
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / returns_std if returns_std != 0 else 0.0
        
        # Calculate Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = cumulative_returns / rolling_max - 1
        max_drawdown = drawdowns.min()
        
        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'num_trades': len(self.trades)
        } 