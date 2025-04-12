from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict
import asyncio
import logging
import numpy as np
import uuid
import time
import random
from decimal import Decimal, ROUND_DOWN

from app.models.order import OrderSide, OrderStatus, OrderType, TimeInForce, OrderBase
from app.models.position import Position
from .order_executor import OrderExecutionResult, BracketOrderResult, OrderState, OrderExecutionError

logger = logging.getLogger(__name__)

class DryRunExecutor:
    """
    Simulates order execution for testing and dry-run purposes.
    Implements the same interface as OrderExecutor but without real API calls.
    """
    
    def __init__(
        self,
        initial_balance: Dict[str, float] = None,
        default_time_in_force: str = "GTC",
        min_signal_confidence: float = 0.7,
        simulated_latency: float = 0.1,  # Simulated API latency in seconds
        fill_probability: float = 0.95,   # Probability of order being filled
        slippage_std: float = 0.001,     # Standard deviation for price slippage
        price_trend_bias: float = 0.0,    # Bias for price trend (-1.0 to 1.0)
        volatility_factor: float = 1.0    # Multiplier for price volatility
    ):
        """
        Initialize the DryRunExecutor.
        
        Args:
            initial_balance: Dictionary of currency -> balance (e.g., {"BTC": 1.0, "USD": 50000.0})
            default_time_in_force: Default time in force setting for orders
            min_signal_confidence: Minimum confidence score required for signal confirmation
            simulated_latency: Artificial delay to simulate API latency (seconds)
            fill_probability: Probability of order being filled (0.0-1.0)
            slippage_std: Standard deviation for simulated price slippage
            price_trend_bias: Bias for price movement (-1.0 bearish to 1.0 bullish)
            volatility_factor: Multiplier for price volatility (default 1.0)
        """
        self.default_time_in_force = default_time_in_force
        self.min_signal_confidence = min_signal_confidence
        self.simulated_latency = simulated_latency
        self.fill_probability = fill_probability
        self.slippage_std = slippage_std
        self.price_trend_bias = max(-1.0, min(1.0, price_trend_bias))
        self.volatility_factor = max(0.1, volatility_factor)
        
        # Initialize balances
        self._balances = initial_balance or {"BTC": 1.0, "USD": 50000.0}
        
        # State tracking
        self._positions: Dict[str, Position] = {}
        self._order_states: Dict[str, OrderState] = {}
        self._historical_orders: Dict[str, List[OrderState]] = {}
        self._order_modifications: Dict[str, List[Dict]] = {}
        self._next_order_id = 1
        self._trading_enabled = True
        
        # Market simulation
        self._simulated_prices: Dict[str, float] = {}
        self._position_monitors: Dict[str, asyncio.Task] = {}
        self._position_events: List[Dict] = []
        
        # Enhanced logging setup
        self._trade_log: List[Dict] = []
        self._simulation_stats = {
            'total_trades': 0,
            'successful_trades': 0,
            'failed_trades': 0,
            'total_volume': 0.0,
            'total_fees': 0.0,
            'start_time': datetime.utcnow(),
            'price_updates': 0
        }
        
    def _generate_order_id(self) -> str:
        """Generate a unique order ID for simulation"""
        order_id = f"dry-run-{self._next_order_id}"
        self._next_order_id += 1
        return order_id
        
    async def _simulate_api_latency(self):
        """Simulate network latency for more realistic testing"""
        await asyncio.sleep(self.simulated_latency)
        
    def _update_balance(self, currency: str, amount: float):
        """Update simulated balance for a currency"""
        if currency not in self._balances:
            self._balances[currency] = 0.0
        self._balances[currency] += amount
        
    async def execute_market_order(
        self,
        product_id: str,
        side: Union[str, OrderSide],
        size: float,
        client_order_id: Optional[str] = None
    ) -> OrderExecutionResult:
        """Simulate market order execution"""
        try:
            if not self._trading_enabled:
                raise OrderExecutionError("Trading is currently halted")
                
            await self._simulate_api_latency()
            start_time = datetime.utcnow()
            
            # Validate inputs
            side_str = side if isinstance(side, str) else str(side)
            if side_str not in [OrderSide.BUY, OrderSide.SELL]:
                raise OrderExecutionError(f"Invalid order side: {side_str}")
            
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
                
            # Get currencies from product_id
            base_currency, quote_currency = product_id.split("-")
            
            # Check balance
            if side_str == OrderSide.BUY:
                required_quote = size * self._simulated_prices.get(product_id, 50000.0)  # Default price for testing
                if self._balances.get(quote_currency, 0) < required_quote:
                    raise OrderExecutionError(f"Insufficient {quote_currency} balance")
            else:
                if self._balances.get(base_currency, 0) < size:
                    raise OrderExecutionError(f"Insufficient {base_currency} balance")
                    
            # Create simulated order
            order_id = self._generate_order_id()
            order = Order(
                order_id=order_id,
                client_order_id=client_order_id,
                product_id=product_id,
                side=side_str,
                order_type=OrderType.MARKET.value,
                status=OrderStatus.FILLED.value,  # Market orders are filled immediately in simulation
                time_in_force=self.default_time_in_force,
                created_time=datetime.utcnow().isoformat(),
                size=str(size),
                filled_size=str(size),
                price=str(self._simulated_prices.get(product_id, 50000.0)),
                average_filled_price=str(self._simulated_prices.get(product_id, 50000.0))
            )
            
            # Update balances
            if side_str == OrderSide.BUY:
                self._update_balance(quote_currency, -required_quote)
                self._update_balance(base_currency, size)
            else:
                self._update_balance(base_currency, -size)
                self._update_balance(quote_currency, size * float(order.price))
                
            # Track order state
            order_state = OrderState(
                order_id=order_id,
                product_id=product_id,
                side=side_str,
                type=OrderType.MARKET.value,
                size=size,
                price=float(order.price),
                status=OrderStatus.FILLED,
                filled_size=size,
                remaining_size=0.0,
                average_fill_price=float(order.price),
                created_time=datetime.utcnow(),
                last_update_time=datetime.utcnow(),
                state_transitions=[]
            )
            
            self._order_states[order_id] = order_state
            
            self._log_trade(order, OrderExecutionResult(
                success=True,
                order=order,
                execution_time=start_time,
                metadata={
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds(),
                    "order_type": OrderType.MARKET.value.lower(),
                    "simulated": True
                }
            ))
            
            return OrderExecutionResult(
                success=True,
                order=order,
                execution_time=start_time,
                metadata={
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds(),
                    "order_type": OrderType.MARKET.value.lower(),
                    "simulated": True
                }
            )
            
        except OrderExecutionError as e:
            self._log_trade(Order(
                order_id=self._generate_order_id(),
                client_order_id=None,
                product_id=product_id,
                side=side,
                order_type=OrderType.MARKET.value,
                status=OrderStatus.CANCELLED.value,
                time_in_force=self.default_time_in_force,
                created_time=datetime.utcnow().isoformat(),
                size=str(size),
                filled_size="0",
                price=None,
                average_filled_price=None
            ), OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={"error_type": "validation_error", "simulated": True}
            ))
            return OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={"error_type": "validation_error", "simulated": True}
            )
        except Exception as e:
            logger.error(f"Error in dry run market order execution: {str(e)}")
            self._log_trade(Order(
                order_id=self._generate_order_id(),
                client_order_id=None,
                product_id=product_id,
                side=side,
                order_type=OrderType.MARKET.value,
                status=OrderStatus.CANCELLED.value,
                time_in_force=self.default_time_in_force,
                created_time=datetime.utcnow().isoformat(),
                size=str(size),
                filled_size="0",
                price=None,
                average_filled_price=None
            ), OrderExecutionResult(
                success=False,
                error=f"Simulation error: {str(e)}",
                execution_time=datetime.utcnow(),
                metadata={"error_type": "simulation_error", "simulated": True}
            ))
            return OrderExecutionResult(
                success=False,
                error=f"Simulation error: {str(e)}",
                execution_time=datetime.utcnow(),
                metadata={"error_type": "simulation_error", "simulated": True}
            )
            
    async def execute_limit_order(
        self,
        product_id: str,
        side: Union[str, OrderSide],
        size: float,
        price: float,
        client_order_id: Optional[str] = None,
        time_in_force: Optional[str] = None
    ) -> OrderExecutionResult:
        """Simulate limit order execution"""
        try:
            if not self._trading_enabled:
                raise OrderExecutionError("Trading is currently halted")
                
            await self._simulate_api_latency()
            start_time = datetime.utcnow()
            
            # Validate inputs
            side_str = side if isinstance(side, str) else str(side)
            if side_str not in [OrderSide.BUY, OrderSide.SELL]:
                raise OrderExecutionError(f"Invalid order side: {side_str}")
            
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
            if price <= 0:
                raise OrderExecutionError(f"Invalid price: {price}")
                
            # Get currencies from product_id
            base_currency, quote_currency = product_id.split("-")
            
            # Check balance
            if side_str == OrderSide.BUY:
                required_quote = size * price
                if self._balances.get(quote_currency, 0) < required_quote:
                    raise OrderExecutionError(f"Insufficient {quote_currency} balance")
            else:
                if self._balances.get(base_currency, 0) < size:
                    raise OrderExecutionError(f"Insufficient {base_currency} balance")
                    
            # Create simulated order
            order_id = self._generate_order_id()
            order = Order(
                order_id=order_id,
                client_order_id=client_order_id,
                product_id=product_id,
                side=side_str,
                order_type=OrderType.LIMIT.value,
                status=OrderStatus.OPEN.value,  # Limit orders start as open
                time_in_force=time_in_force or self.default_time_in_force,
                created_time=datetime.utcnow().isoformat(),
                size=str(size),
                filled_size="0",
                price=str(price),
                average_filled_price=None
            )
            
            # Track order state
            order_state = OrderState(
                order_id=order_id,
                product_id=product_id,
                side=side_str,
                type=OrderType.LIMIT.value,
                size=size,
                price=price,
                status=OrderStatus.OPEN,
                filled_size=0.0,
                remaining_size=size,
                average_fill_price=None,
                created_time=datetime.utcnow(),
                last_update_time=datetime.utcnow(),
                state_transitions=[]
            )
            
            self._order_states[order_id] = order_state
            
            # Start fill simulation for limit order
            asyncio.create_task(self._simulate_limit_order_fills(order_state))
            
            self._log_trade(order, OrderExecutionResult(
                success=True,
                order=order,
                execution_time=start_time,
                metadata={
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds(),
                    "order_type": OrderType.LIMIT.value.lower(),
                    "simulated": True
                }
            ))
            
            return OrderExecutionResult(
                success=True,
                order=order,
                execution_time=start_time,
                metadata={
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds(),
                    "order_type": OrderType.LIMIT.value.lower(),
                    "simulated": True
                }
            )
            
        except OrderExecutionError as e:
            self._log_trade(Order(
                order_id=self._generate_order_id(),
                client_order_id=client_order_id,
                product_id=product_id,
                side=side,
                order_type=OrderType.LIMIT.value,
                status=OrderStatus.CANCELLED.value,
                time_in_force=time_in_force,
                created_time=datetime.utcnow().isoformat(),
                size=str(size),
                filled_size="0",
                price=str(price),
                average_filled_price=None
            ), OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={"error_type": "validation_error", "simulated": True}
            ))
            return OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={"error_type": "validation_error", "simulated": True}
            )
        except Exception as e:
            logger.error(f"Error in dry run limit order execution: {str(e)}")
            self._log_trade(Order(
                order_id=self._generate_order_id(),
                client_order_id=client_order_id,
                product_id=product_id,
                side=side,
                order_type=OrderType.LIMIT.value,
                status=OrderStatus.CANCELLED.value,
                time_in_force=time_in_force,
                created_time=datetime.utcnow().isoformat(),
                size=str(size),
                filled_size="0",
                price=str(price),
                average_filled_price=None
            ), OrderExecutionResult(
                success=False,
                error=f"Simulation error: {str(e)}",
                execution_time=datetime.utcnow(),
                metadata={"error_type": "simulation_error", "simulated": True}
            ))
            return OrderExecutionResult(
                success=False,
                error=f"Simulation error: {str(e)}",
                execution_time=datetime.utcnow(),
                metadata={"error_type": "simulation_error", "simulated": True}
            )
            
    async def _simulate_limit_order_fills(self, order_state: OrderState):
        """Simulate limit order fills over time"""
        try:
            while order_state.status == OrderStatus.OPEN and order_state.remaining_size > 0:
                await asyncio.sleep(1.0)  # Check every second
                
                # Simulate whether order gets filled
                if self.fill_probability > 0.0:
                    current_price = self._simulated_prices.get(order_state.product_id, 50000.0)
                    
                    # Check if price conditions are met
                    if ((order_state.side == OrderSide.BUY and current_price <= order_state.price) or
                        (order_state.side == OrderSide.SELL and current_price >= order_state.price)):
                        
                        # Simulate partial fill
                        fill_size = min(order_state.remaining_size, order_state.size * 0.25)
                        order_state.filled_size += fill_size
                        order_state.remaining_size -= fill_size
                        order_state.average_fill_price = current_price
                        
                        if order_state.remaining_size <= 0:
                            order_state.status = OrderStatus.FILLED
                            # Move to historical orders
                            if order_state.product_id not in self._historical_orders:
                                self._historical_orders[order_state.product_id] = []
                            self._historical_orders[order_state.product_id].append(order_state)
                            del self._order_states[order_state.order_id]
                            
                            # Update balances
                            base_currency, quote_currency = order_state.product_id.split("-")
                            if order_state.side == OrderSide.BUY:
                                self._update_balance(quote_currency, -order_state.size * order_state.price)
                                self._update_balance(base_currency, order_state.size)
                            else:
                                self._update_balance(base_currency, -order_state.size)
                                self._update_balance(quote_currency, order_state.size * order_state.price)
                                
        except Exception as e:
            logger.error(f"Error in limit order fill simulation: {str(e)}")
            
    async def cancel_order(self, order_id: str) -> OrderExecutionResult:
        """Simulate order cancellation"""
        try:
            await self._simulate_api_latency()
            start_time = datetime.utcnow()
            
            if order_id not in self._order_states:
                raise OrderExecutionError(f"Order {order_id} not found")
                
            order_state = self._order_states[order_id]
            if order_state.status not in [OrderStatus.OPEN, OrderStatus.PENDING]:
                raise OrderExecutionError(f"Cannot cancel order in status: {order_state.status}")
                
            order_state.status = OrderStatus.CANCELLED
            
            # Move to historical orders
            if order_state.product_id not in self._historical_orders:
                self._historical_orders[order_state.product_id] = []
            self._historical_orders[order_state.product_id].append(order_state)
            del self._order_states[order_id]
            
            self._log_trade(Order(
                order_id=order_id,
                client_order_id=None,
                product_id=order_state.product_id,
                side=order_state.side,
                order_type=order_state.type,
                status=order_state.status.value,
                time_in_force=self.default_time_in_force,
                created_time=order_state.created_time.isoformat(),
                size=str(order_state.size),
                filled_size=str(order_state.filled_size),
                price=str(order_state.price) if order_state.price else None,
                average_filled_price=str(order_state.average_fill_price) if order_state.average_fill_price else None
            ), OrderExecutionResult(
                success=True,
                execution_time=start_time,
                metadata={
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds(),
                    "action": "cancel",
                    "simulated": True
                }
            ))
            
            return OrderExecutionResult(
                success=True,
                execution_time=start_time,
                metadata={
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds(),
                    "action": "cancel",
                    "simulated": True
                }
            )
            
        except OrderExecutionError as e:
            self._log_trade(Order(
                order_id=order_id,
                client_order_id=None,
                product_id=order_state.product_id,
                side=order_state.side,
                order_type=order_state.type,
                status=order_state.status.value,
                time_in_force=self.default_time_in_force,
                created_time=order_state.created_time.isoformat(),
                size=str(order_state.size),
                filled_size=str(order_state.filled_size),
                price=str(order_state.price) if order_state.price else None,
                average_filled_price=str(order_state.average_fill_price) if order_state.average_fill_price else None
            ), OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={"error_type": "validation_error", "simulated": True}
            ))
            return OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={"error_type": "validation_error", "simulated": True}
            )
        except Exception as e:
            logger.error(f"Error in dry run order cancellation: {str(e)}")
            self._log_trade(Order(
                order_id=order_id,
                client_order_id=None,
                product_id=order_state.product_id,
                side=order_state.side,
                order_type=order_state.type,
                status=order_state.status.value,
                time_in_force=self.default_time_in_force,
                created_time=order_state.created_time.isoformat(),
                size=str(order_state.size),
                filled_size=str(order_state.filled_size),
                price=str(order_state.price) if order_state.price else None,
                average_filled_price=str(order_state.average_fill_price) if order_state.average_fill_price else None
            ), OrderExecutionResult(
                success=False,
                error=f"Simulation error: {str(e)}",
                execution_time=datetime.utcnow(),
                metadata={"error_type": "simulation_error", "simulated": True}
            ))
            return OrderExecutionResult(
                success=False,
                error=f"Simulation error: {str(e)}",
                execution_time=datetime.utcnow(),
                metadata={"error_type": "simulation_error", "simulated": True}
            )
            
    async def get_order_status(self, order_id: str) -> Optional[Dict]:
        """Get the status and details of a specific simulated order."""
        logger.debug(f"DryRun: Getting status for order ID: {order_id}")
        with self._lock:
            order_state = self._order_states.get(order_id)
            if not order_state:
                logger.warning(f"DryRun: Order {order_id} not found.")
                return None
            # Return a copy of the state as a dictionary
            # Ensure datetime objects are handled if needed (e.g., isoformat)
            return order_state.model_dump()
        
    def set_simulated_price(self, product_id: str, price: float):
        """Set the simulated price for a product"""
        self._simulated_prices[product_id] = price
        
    def get_simulated_balance(self, currency: str) -> float:
        """Get the simulated balance for a currency"""
        return self._balances.get(currency, 0.0)
        
    async def halt_trading(self, reason: str = "Emergency halt triggered"):
        """Emergency kill-switch to halt all trading activity"""
        self._trading_enabled = False
        logger.critical(f"Trading halted in dry run mode: {reason}")
        
    async def resume_trading(self, confirmation: str = "Manual resume"):
        """Resume trading after a halt"""
        self._trading_enabled = True
        logger.info(f"Resuming trading in dry run mode: {confirmation}")
        
    async def _simulate_price_update(self, product_id: str):
        """Simulate realistic price movements with trend and volatility"""
        if product_id not in self._simulated_prices:
            return
        
        current_price = self._simulated_prices[product_id]
        
        # Calculate price change based on trend bias and volatility
        trend_component = self.price_trend_bias * 0.001  # 0.1% base trend
        volatility_component = np.random.normal(0, 0.002 * self.volatility_factor)
        price_change = current_price * (trend_component + volatility_component)
        
        # Update price
        new_price = max(0.01, current_price + price_change)
        self._simulated_prices[product_id] = new_price
        self._simulation_stats['price_updates'] += 1
        
        # Log significant price movements
        if abs(price_change / current_price) > 0.005:  # Log 0.5% or larger moves
            logger.info(
                f"Significant price movement in {product_id}: {current_price:.2f} -> {new_price:.2f} "
                f"({(price_change/current_price)*100:.2f}%)"
            )

    def _log_trade(self, order: OrderBase, execution_result: OrderExecutionResult):
        """Log executed trade details."""
        # Ensure order has necessary attributes before logging
        order_id = getattr(order, 'order_id', 'N/A')
        product_id = getattr(order, 'product_id', 'N/A')
        side = getattr(order, 'side', 'N/A')
        order_type = getattr(order, 'type', 'N/A') # Assuming type attribute exists
        size = getattr(order, 'size', 'N/A')
        price = getattr(order, 'price', 'N/A') # Assuming price attribute exists
        
        trade_log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "order_id": order_id,
            "product_id": product_id,
            "side": side.value if hasattr(side, 'value') else side, # Handle enum or string
            "type": order_type.value if hasattr(order_type, 'value') else order_type,
            "size": str(size), # Convert Decimal/float to string
            "price": str(price),
            "success": execution_result.success,
            "error": execution_result.error,
            "simulated": True
        }
        self._trade_log.append(trade_log)
        
        # Update simulation statistics
        self._simulation_stats['total_trades'] += 1
        if execution_result.success:
            self._simulation_stats['successful_trades'] += 1
            self._simulation_stats['total_volume'] += float(order.filled_size or 0)
            # Assume 0.1% fee for simulation
            self._simulation_stats['total_fees'] += float(order.filled_size or 0) * float(order.price or 0) * 0.001
        else:
            self._simulation_stats['failed_trades'] += 1

    def get_simulation_stats(self) -> Dict:
        """Get current simulation statistics"""
        stats = self._simulation_stats.copy()
        stats['duration'] = (datetime.utcnow() - stats['start_time']).total_seconds()
        stats['success_rate'] = (stats['successful_trades'] / stats['total_trades'] * 100 
                               if stats['total_trades'] > 0 else 0)
        return stats

    def get_trade_history(self) -> List[Dict]:
        """Get the full trade history log"""
        return self._trade_log.copy()

    async def start_price_simulation(self, product_id: str):
        """Start background price simulation for a product"""
        while True:
            await self._simulate_price_update(product_id)
            await asyncio.sleep(1)  # Update price every second 