from datetime import datetime
from typing import Dict, List, Optional, Union
import pandas as pd
import numpy as np
import logging

from .models import Order, OrderSide, OrderStatus, OrderType, Position
from .order_executor import OrderExecutionResult
from .exceptions import OrderExecutionError

logger = logging.getLogger(__name__)

class BacktestEngine:
    """
    Simulates trading using historical price data for strategy backtesting.
    Implements similar interface as OrderExecutor but uses historical data.
    """
    
    def __init__(
        self,
        historical_data: pd.DataFrame,
        initial_balance: Dict[str, float] = None,
        trading_fee: float = 0.001,  # 0.1% trading fee
        slippage_std: float = 0.001  # 0.1% standard deviation for slippage
    ):
        """
        Initialize the BacktestEngine.
        
        Args:
            historical_data: DataFrame with columns [timestamp, open, high, low, close, volume]
            initial_balance: Dictionary of currency -> balance (e.g., {"BTC": 1.0, "USD": 50000.0})
            trading_fee: Fee percentage per trade (default 0.1%)
            slippage_std: Standard deviation for price slippage simulation
        """
        self._validate_historical_data(historical_data)
        self.data = historical_data
        self.current_index = 0
        self.trading_fee = trading_fee
        self.slippage_std = slippage_std
        
        # Initialize balances
        self._balances = initial_balance or {"BTC": 1.0, "USD": 50000.0}
        
        # State tracking
        self._positions: Dict[str, Position] = {}
        self._order_states: Dict[str, Dict] = {}
        self._historical_orders: List[Dict] = []
        self._next_order_id = 1
        self._trading_enabled = True
        
        # Performance tracking
        self._portfolio_values = []
        self._trade_log = []
        self._stats = {
            'total_trades': 0,
            'successful_trades': 0,
            'failed_trades': 0,
            'total_volume': 0.0,
            'total_fees': 0.0,
            'start_time': datetime.utcnow(),
            'initial_portfolio_value': self._calculate_portfolio_value()
        }
        
    def _validate_historical_data(self, data: pd.DataFrame):
        """Validate historical data format"""
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in historical data: {missing_columns}")
            
    def _generate_order_id(self) -> str:
        """Generate a unique order ID for simulation"""
        order_id = f"backtest-{self._next_order_id}"
        self._next_order_id += 1
        return order_id
        
    def _calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value in quote currency"""
        current_price = self.data.iloc[self.current_index]['close']
        portfolio_value = self._balances.get("USD", 0.0)
        portfolio_value += self._balances.get("BTC", 0.0) * current_price
        return portfolio_value
        
    def _simulate_slippage(self, base_price: float) -> float:
        """Simulate price slippage"""
        slippage = np.random.normal(0, self.slippage_std)
        return base_price * (1 + slippage)
        
    def _calculate_fee(self, price: float, size: float) -> float:
        """Calculate trading fee for a transaction"""
        return price * size * self.trading_fee
        
    async def execute_market_order(
        self,
        product_id: str,
        side: Union[str, OrderSide],
        size: float,
        client_order_id: Optional[str] = None
    ) -> OrderExecutionResult:
        """Execute a market order using historical data"""
        try:
            if not self._trading_enabled:
                raise OrderExecutionError("Trading is currently halted")
                
            # Validate inputs
            side_str = side if isinstance(side, str) else str(side)
            if side_str not in [OrderSide.BUY, OrderSide.SELL]:
                raise OrderExecutionError(f"Invalid order side: {side_str}")
            
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
                
            # Get current price from historical data
            current_bar = self.data.iloc[self.current_index]
            execution_price = self._simulate_slippage(current_bar['close'])
            
            # Calculate fees
            fee = self._calculate_fee(execution_price, size)
            
            # Check balance
            base_currency, quote_currency = product_id.split("-")
            if side_str == OrderSide.BUY:
                required_quote = (size * execution_price) + fee
                if self._balances.get(quote_currency, 0) < required_quote:
                    raise OrderExecutionError(f"Insufficient {quote_currency} balance")
            else:
                if self._balances.get(base_currency, 0) < size:
                    raise OrderExecutionError(f"Insufficient {base_currency} balance")
                    
            # Create order record
            order_id = self._generate_order_id()
            order = Order(
                order_id=order_id,
                client_order_id=client_order_id,
                product_id=product_id,
                side=side_str,
                order_type=OrderType.MARKET.value,
                status=OrderStatus.FILLED.value,
                time_in_force="GTC",
                created_time=current_bar['timestamp'].isoformat(),
                size=str(size),
                filled_size=str(size),
                price=str(execution_price),
                average_filled_price=str(execution_price)
            )
            
            # Update balances
            if side_str == OrderSide.BUY:
                self._balances[quote_currency] -= required_quote
                self._balances[base_currency] = self._balances.get(base_currency, 0) + size
            else:
                self._balances[base_currency] -= size
                received_quote = (size * execution_price) - fee
                self._balances[quote_currency] = self._balances.get(quote_currency, 0) + received_quote
                
            # Record trade
            self._log_trade(order, True, execution_price, fee)
            
            # Update portfolio value history
            self._portfolio_values.append({
                'timestamp': current_bar['timestamp'],
                'value': self._calculate_portfolio_value()
            })
            
            return OrderExecutionResult(
                success=True,
                order=order,
                execution_time=current_bar['timestamp'],
                metadata={
                    'execution_price': execution_price,
                    'fee': fee,
                    'slippage': execution_price / current_bar['close'] - 1
                }
            )
            
        except Exception as e:
            logger.error(f"Error in backtest market order execution: {str(e)}")
            self._log_trade(
                Order(
                    order_id=self._generate_order_id(),
                    product_id=product_id,
                    side=side_str,
                    order_type=OrderType.MARKET.value,
                    status=OrderStatus.FAILED.value,
                    size=str(size)
                ),
                False,
                None,
                0.0,
                str(e)
            )
            return OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=self.data.iloc[self.current_index]['timestamp']
            )
            
    def _log_trade(
        self,
        order: Order,
        success: bool,
        execution_price: Optional[float],
        fee: float,
        error: str = None
    ):
        """Log trade details for analysis"""
        trade_entry = {
            'timestamp': self.data.iloc[self.current_index]['timestamp'],
            'order_id': order.order_id,
            'product_id': order.product_id,
            'side': order.side,
            'type': order.order_type,
            'size': float(order.size),
            'price': execution_price,
            'fee': fee,
            'success': success,
            'error': error,
            'portfolio_value': self._calculate_portfolio_value()
        }
        self._trade_log.append(trade_entry)
        
        # Update statistics
        self._stats['total_trades'] += 1
        if success:
            self._stats['successful_trades'] += 1
            self._stats['total_volume'] += float(order.size) * (execution_price or 0)
            self._stats['total_fees'] += fee
        else:
            self._stats['failed_trades'] += 1
            
    def get_performance_metrics(self) -> Dict:
        """Calculate and return backtest performance metrics"""
        if not self._portfolio_values:
            return {}
            
        portfolio_values = pd.DataFrame(self._portfolio_values)
        returns = portfolio_values['value'].pct_change().dropna()
        
        metrics = {
            'total_return': (portfolio_values['value'].iloc[-1] / self._stats['initial_portfolio_value']) - 1,
            'annualized_return': None,  # Will calculate if duration > 1 day
            'sharpe_ratio': None,  # Will calculate if we have enough data
            'max_drawdown': None,  # Will calculate from portfolio values
            'win_rate': self._stats['successful_trades'] / self._stats['total_trades'] if self._stats['total_trades'] > 0 else 0,
            'total_trades': self._stats['total_trades'],
            'total_volume': self._stats['total_volume'],
            'total_fees': self._stats['total_fees']
        }
        
        # Calculate annualized metrics if we have enough data
        if len(portfolio_values) > 1:
            duration_days = (portfolio_values['timestamp'].iloc[-1] - portfolio_values['timestamp'].iloc[0]).days
            if duration_days > 0:
                metrics['annualized_return'] = (1 + metrics['total_return']) ** (365 / duration_days) - 1
                
            # Calculate Sharpe Ratio (assuming risk-free rate of 0.02)
            if len(returns) > 30:  # Need enough data for meaningful Sharpe ratio
                rf_daily = 0.02 / 365
                excess_returns = returns - rf_daily
                metrics['sharpe_ratio'] = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
                
            # Calculate Maximum Drawdown
            rolling_max = portfolio_values['value'].expanding().max()
            drawdowns = portfolio_values['value'] / rolling_max - 1
            metrics['max_drawdown'] = drawdowns.min()
            
        return metrics
        
    def get_trade_history(self) -> List[Dict]:
        """Get the full trade history log"""
        return self._trade_log.copy()
        
    def step(self):
        """Advance to the next time step in the historical data"""
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            return True
        return False
        
    def reset(self):
        """Reset the backtest to initial state"""
        self.current_index = 0
        self._balances = self._initial_balance.copy()
        self._positions.clear()
        self._order_states.clear()
        self._historical_orders.clear()
        self._portfolio_values.clear()
        self._trade_log.clear()
        self._stats = {
            'total_trades': 0,
            'successful_trades': 0,
            'failed_trades': 0,
            'total_volume': 0.0,
            'total_fees': 0.0,
            'start_time': datetime.utcnow(),
            'initial_portfolio_value': self._calculate_portfolio_value()
        } 