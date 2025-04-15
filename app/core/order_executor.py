from typing import Dict, Optional, List, Union, Any, Callable
from datetime import datetime
import logging
from pydantic import BaseModel, ConfigDict
import asyncio
import pandas as pd
import statistics
import uuid
import time
from enum import Enum
# SQLAlchemy session for logging
from sqlalchemy.ext.asyncio import AsyncSession 

from app.core.coinbase import (
    CoinbaseClient,
    OrderSide,
    # OrderStatus, # Now imported from trade_log.models
)
# # Import CoinbaseError directly from the library - Removed
# from coinbase.errors import CoinbaseError 

from app.models.order import TimeInForce, OrderType, OrderBase
from app.core.signal_manager import SignalManager, SignalConfirmation
from app.models.zone import Zone
from app.models.position import Position
# Import logging components
from app.core.trade_log.crud import create_log_entry
from app.core.trade_log.models import EventType, OrderStatus, TradeSide

logger = logging.getLogger(__name__)

class OrderExecutionError(Exception):
    """Custom exception for order execution errors"""
    pass

class BracketOrderResult(BaseModel):
    """Model for bracket order execution results"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    entry_order: Optional[OrderBase] = None
    stop_loss_order: Optional[OrderBase] = None
    take_profit_order: Optional[OrderBase] = None
    success: bool
    error: Optional[str] = None
    execution_time: datetime
    metadata: Optional[Dict] = None

class OrderExecutionResult(BaseModel):
    """Model for order execution results"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    success: bool
    order: Optional[OrderBase] = None
    error: Optional[str] = None
    execution_time: datetime
    metadata: Optional[Dict] = None

class Position(BaseModel):
    """Model for tracking trading positions"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    product_id: str
    side: OrderSide
    size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    entry_time: datetime
    last_update_time: datetime
    risk_metrics: Dict[str, float] = {}
    orders: List[str] = []  # List of order IDs associated with this position
    status: str = "OPEN"  # OPEN, CLOSED, PARTIALLY_CLOSED
    metadata: Dict = {}

class OrderState(BaseModel):
    """Model for tracking order state transitions"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    order_id: str
    product_id: str
    side: OrderSide
    size: float
    price: Optional[float]
    type: OrderType
    status: OrderStatus
    filled_size: float = 0.0
    remaining_size: float
    average_fill_price: Optional[float] = None
    last_update_time: datetime
    state_transitions: List[Dict[str, Any]] = []
    position_id: Optional[str] = None
    metadata: Dict = {}

class OrderExecutor:
    """
    Handles order execution and management for the trading system.
    Implements various order types and execution strategies.
    """
    
    def __init__(
        self,
        client: CoinbaseClient,
        signal_manager: Optional['SignalManager'] = None,
        default_time_in_force: str = "GTC",
        min_signal_confidence: float = 0.7
    ):
        """
        Initialize the OrderExecutor.
        
        Args:
            client: Initialized CoinbaseClient instance
            signal_manager: Optional SignalManager for signal confirmation
            default_time_in_force: Default time in force setting for orders
            min_signal_confidence: Minimum confidence score required for signal confirmation
        """
        self.client = client
        self.signal_manager = signal_manager
        self.default_time_in_force = default_time_in_force
        self.min_signal_confidence = min_signal_confidence
        self._positions: Dict[str, Position] = {}  # product_id -> Position
        self._order_states: Dict[str, OrderState] = {}  # order_id -> OrderState
        self._historical_orders: Dict[str, List[OrderState]] = {}  # product_id -> List[OrderState]
        self._order_modifications: Dict[str, List[Dict]] = {}  # order_id -> List of modifications
        self._performance_metrics: Dict[str, List[float]] = {
            "execution_latency": [],
            "fill_rates": [],
            "success_rates": [],
            "modification_success_rates": []
        }
        self._trading_enabled = True
        self._risk_thresholds = {
            'max_position_size': 1.0,  # Maximum position size in BTC
            'max_drawdown_pct': 5.0,   # Maximum drawdown percentage
            'max_daily_loss_pct': 3.0, # Maximum daily loss percentage
            'max_leverage': 3.0        # Maximum allowed leverage
        }
        self._daily_stats = {
            'start_balance': 0.0,
            'current_balance': 0.0,
            'total_pnl': 0.0,
            'trade_count': 0
        }
        self._position_monitors: Dict[str, asyncio.Task] = {}
        self._position_events: List[Dict] = []
        self._risk_metrics_cache: Dict[str, Dict] = {}
        self._last_metrics_update = datetime.now()
        
    async def execute_market_order(
        self,
        db: AsyncSession, # Add database session parameter
        product_id: str,
        side: Union[str, OrderSide],
        size: float,
        client_order_id: Optional[str] = None,
        strategy_name: Optional[str] = None # Add strategy name if available
    ) -> OrderExecutionResult:
        """
        Execute a market order.
        
        Args:
            db: SQLAlchemy async session
            product_id: Trading pair ID (e.g., BTC-USD)
            side: Order side (BUY/SELL)
            size: Order size in base currency
            client_order_id: Client-specified order ID
            strategy_name: Name of the strategy initiating the order
            
        Returns:
            OrderExecutionResult with execution details
            
        Raises:
            OrderExecutionError: If validation fails
        """
        order = None # Initialize order to None
        try:
            # Convert side to enum and string
            side_enum = side if isinstance(side, TradeSide) else TradeSide(side.upper())
            # Validate using the imported TradeSide enum
            if side_enum not in [TradeSide.BUY, TradeSide.SELL]:
                raise OrderExecutionError(f"Invalid order side provided: {side}")
            side_str = side_enum.value # Use the value for API call if needed by client
            
            start_time = datetime.utcnow()
            
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
                
            # Generate a client_order_id if none provided
            if client_order_id is None:
                client_order_id = f"mkt_{product_id.replace('-','')}_{uuid.uuid4().hex[:8]}"
            
            # Place market order
            order = await self.client.create_order(
                product_id=product_id,
                # Pass the string value expected by the client wrapper
                side=side_str, 
                order_type=OrderType.MARKET.value,
                size=size,
                client_order_id=client_order_id,
                # time_in_force=self.default_time_in_force # Market orders don't usually use TIF
            )
            
            # --- Check if order creation actually succeeded --- 
            if not order or not order.get("order_id"):
                # Log the failure
                logger.error(f"Order creation via CoinbaseClient failed or returned invalid data for {product_id}. Response: {order}")
                await create_log_entry(
                    db=db,
                    event_type=EventType.ERROR,
                    symbol=product_id,
                    status=OrderStatus.REJECTED, # Assume rejection if no valid order ID
                    side=side_enum,
                    quantity=size,
                    strategy_name=strategy_name,
                    client_order_id=client_order_id,
                    notes=f"Order creation failed. API Response: {str(order)[:200]}" # Log part of the response
                )
                return OrderExecutionResult(
                    success=False,
                    error="Order creation failed or returned invalid data.",
                    execution_time=start_time,
                    metadata={"api_response": order}
                )
                
            # --- Log Successful Order Submission --- 
            log_event = EventType.ENTRY_ORDER if side_enum == TradeSide.BUY else EventType.EXIT_ORDER
            await create_log_entry(
                db=db,
                event_type=log_event,
                symbol=product_id,
                status=OrderStatus.ORDER_SENT, # Log that the order was sent
                order_id=order.order_id, # Use order_id from the response
                client_order_id=client_order_id,
                side=side_enum,
                quantity=size,
                strategy_name=strategy_name,
                event_timestamp=start_time, # Time when we attempted to send
                notes=f"Market order sent."
            )
            # --- End Log --- 
            
            return OrderExecutionResult(
                success=True,
                order=order,
                execution_time=start_time,
                metadata={
                    "execution_latency": (start_time - datetime.utcnow()).total_seconds(),
                    "order_type": OrderType.MARKET.value.lower()
                }
            )
            
        except OrderExecutionError as e:
            logger.error(f"Validation error executing market order: {e}")
            # Log error if validation fails before API call
            await create_log_entry(
                db=db,
                event_type=EventType.ERROR,
                symbol=product_id,
                status=OrderStatus.ERROR,
                side=side_enum if 'side_enum' in locals() and isinstance(side_enum, TradeSide) else None,
                quantity=size,
                strategy_name=strategy_name,
                client_order_id=client_order_id,
                notes=f"Order validation error: {e}"
            )
            raise
        except Exception as e:
            # Log simple message first
            logger.error(f"Caught exception during market order execution for {product_id}")
            # Log exception details separately
            logger.error(f"Exception Type: {type(e).__name__}, Representation: {repr(e)}", exc_info=True) 
            
            # Log error if API call fails
            await create_log_entry(
                db=db,
                event_type=EventType.ERROR,
                symbol=product_id,
                status=OrderStatus.REJECTED if getattr(e, 'status_code', 500) != 500 else OrderStatus.ERROR,
                side=side_enum if 'side_enum' in locals() and isinstance(side_enum, TradeSide) else None,
                quantity=size,
                strategy_name=strategy_name,
                client_order_id=client_order_id,
                # Safely access order_id only if order object exists and has the attribute
                order_id=getattr(order, 'order_id', None) if order else None,
                notes=f"API call failed: {type(e).__name__}"
            )
            # Re-raise the exception to see the original traceback
            raise 
            
    async def execute_limit_order(
        self,
        db: AsyncSession, # Add database session parameter
        product_id: str,
        side: Union[str, OrderSide],
        size: float,
        price: float,
        client_order_id: Optional[str] = None,
        time_in_force: Optional[str] = None,
        strategy_name: Optional[str] = None # Add strategy name if available
    ) -> OrderExecutionResult:
        """
        Execute a limit order.
        
        Args:
            db: SQLAlchemy async session
            product_id: Trading pair ID (e.g., BTC-USD)
            side: Order side (BUY/SELL)
            size: Order size in base currency
            price: Limit price for the order
            client_order_id: Client-specified order ID
            time_in_force: Time in force setting for the order
            strategy_name: Name of the strategy initiating the order
            
        Returns:
            OrderExecutionResult with execution details
            
        Raises:
            OrderExecutionError: If validation fails
        """
        order = None # Initialize order to None
        try:
            # Convert side to enum and string
            side_enum = side if isinstance(side, TradeSide) else TradeSide(side.upper())
            # Validate using the imported TradeSide enum
            if side_enum not in [TradeSide.BUY, TradeSide.SELL]:
                 raise OrderExecutionError(f"Invalid order side provided: {side}")
            side_str = side_enum.value # Use the value for API call if needed by client
            
            start_time = datetime.utcnow()
            
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
            if price <= 0:
                raise OrderExecutionError(f"Invalid price: {price}")
                
            # Generate a client_order_id if none provided
            if client_order_id is None:
                client_order_id = f"lim_{product_id.replace('-','')}_{uuid.uuid4().hex[:8]}"
                
            # Place limit order
            order = await self.client.create_order(
                product_id=product_id,
                # Pass the string value expected by the client wrapper
                side=side_str, 
                order_type=OrderType.LIMIT.value,
                size=size,
                price=price,
                client_order_id=client_order_id,
                time_in_force=time_in_force or self.default_time_in_force
            )
            
            # --- Check if order creation actually succeeded --- 
            if not order or not order.get("order_id"):
                # Log the failure
                logger.error(f"Limit order creation via CoinbaseClient failed or returned invalid data for {product_id}. Response: {order}")
                await create_log_entry(
                    db=db,
                    event_type=EventType.ERROR,
                    symbol=product_id,
                    status=OrderStatus.REJECTED, # Assume rejection if no valid order ID
                    side=side_enum,
                    quantity=size,
                    price=price,
                    strategy_name=strategy_name,
                    client_order_id=client_order_id,
                    notes=f"Limit order creation failed. API Response: {str(order)[:200]}"
                )
                return OrderExecutionResult(
                    success=False,
                    error="Limit order creation failed or returned invalid data.",
                    execution_time=start_time,
                    metadata={"api_response": order}
                )
                
            # --- Log Successful Order Submission --- 
            log_event = EventType.ENTRY_ORDER if side_enum == TradeSide.BUY else EventType.EXIT_ORDER
            await create_log_entry(
                db=db,
                event_type=log_event,
                symbol=product_id,
                status=OrderStatus.ORDER_SENT, # Log that the order was sent
                order_id=order.order_id, # Use order_id from the response
                client_order_id=client_order_id,
                side=side_enum,
                quantity=size,
                price=price, # Log limit price
                strategy_name=strategy_name,
                event_timestamp=start_time, # Time when we attempted to send
                notes=f"Limit order sent (TIF: {time_in_force or self.default_time_in_force})."
            )
            # --- End Log --- 
            
            return OrderExecutionResult(
                success=True,
                order=order,
                execution_time=start_time,
                metadata={
                    "execution_latency": (start_time - datetime.utcnow()).total_seconds(),
                    "order_type": OrderType.LIMIT.value.lower()
                }
            )
            
        except OrderExecutionError as e:
            logger.error(f"Validation error executing limit order: {e}")
            # Log error if validation fails before API call
            await create_log_entry(
                db=db,
                event_type=EventType.ERROR,
                symbol=product_id,
                status=OrderStatus.ERROR,
                side=side_enum if 'side_enum' in locals() and isinstance(side_enum, TradeSide) else None,
                quantity=size,
                price=price,
                strategy_name=strategy_name,
                client_order_id=client_order_id,
                notes=f"Order validation error: {e}"
            )
            raise
        except Exception as e:
            # Assume exceptions here are likely API related for now.
            logger.error(f"Coinbase API error executing limit order: {str(e)}")
            # Log error if API call fails
            await create_log_entry(
                db=db,
                event_type=EventType.ERROR,
                symbol=product_id,
                status=OrderStatus.REJECTED if getattr(e, 'status_code', 500) != 500 else OrderStatus.ERROR,
                side=side_enum if 'side_enum' in locals() and isinstance(side_enum, TradeSide) else None,
                quantity=size,
                price=price,
                strategy_name=strategy_name,
                client_order_id=client_order_id,
                # Safely access order_id only if order object exists and has the attribute
                order_id=getattr(order, 'order_id', None) if order else None,
                notes=f"API call failed: {type(e).__name__}" 
            )
            return OrderExecutionResult(
                success=False,
                error=f"Coinbase API error: {str(e)}",
                execution_time=datetime.utcnow(),
                metadata={"error_type": "api_error"}
            )
            
    async def execute_bracket_order(
        self,
        product_id: str,
        side: Union[str, OrderSide],
        size: float,
        stop_loss_price: float,
        take_profit_price: float,
        entry_price: Optional[float] = None,
        entry_type: Union[str, OrderType] = OrderType.MARKET,
        time_in_force: Optional[TimeInForce] = None
    ) -> BracketOrderResult:
        """Execute a bracket order with entry, stop loss, and take profit orders.

        A bracket order is a set of three orders that bracket a position:
        1. Entry order (market or limit)
        2. Stop loss order to limit downside
        3. Take profit order to secure gains

        The orders are placed in sequence:
        - First, the entry order is placed
        - Once the entry is confirmed, stop loss and take profit orders are placed
        - If any order fails, the entire bracket is cancelled

        Args:
            product_id (str): Trading pair ID (e.g., BTC-USD)
            side (Union[str, OrderSide]): Order side (BUY/SELL)
            size (float): Order size in base currency
            stop_loss_price (float): Price for the stop-loss order
            take_profit_price (float): Price for the take-profit order
            entry_price (Optional[float]): Required for limit entry orders
            entry_type (Union[str, OrderType]): MARKET or LIMIT (default: MARKET)
            time_in_force (Optional[TimeInForce]): Time in force for limit orders

        Returns:
            BracketOrderResult containing:
            - entry_order: The entry order details
            - stop_loss_order: The stop-loss order details
            - take_profit_order: The take-profit order details
            - success: Whether all orders were placed successfully
            - error: Error message if any
            - execution_time: When the orders were executed
            - metadata: Additional execution details

        Example:
            ```python
            # Market entry bracket order
            result = await executor.execute_bracket_order(
                product_id="BTC-USD",
                side="BUY",
                size=0.1,
                stop_loss_price=45000.0,
                take_profit_price=55000.0
            )

            # Limit entry bracket order
            result = await executor.execute_bracket_order(
                product_id="BTC-USD",
                side="BUY",
                size=0.1,
                entry_price=50000.0,
                stop_loss_price=45000.0,
                take_profit_price=55000.0,
                entry_type="LIMIT"
            )
            ```

        Raises:
            OrderExecutionError: If validation fails or insufficient funds
            CoinbaseError: If API request fails
        """
        start_time = datetime.utcnow()
        
        try:
            # Convert string side to enum if needed
            if isinstance(side, str):
                try:
                    side = OrderSide(side.lower())
                except ValueError:
                    raise OrderExecutionError(f"Invalid order side: {side}")
            elif not isinstance(side, OrderSide):
                raise OrderExecutionError(f"Invalid order side: {side}")
                
            # Convert string entry_type to enum if needed
            if isinstance(entry_type, str):
                try:
                    entry_type = OrderType(entry_type.lower())
                except ValueError:
                    raise OrderExecutionError(f"Invalid entry type: {entry_type}")
            elif not isinstance(entry_type, OrderType):
                raise OrderExecutionError(f"Invalid entry type: {entry_type}")
            
            # Basic input validation
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
            if stop_loss_price <= 0 or take_profit_price <= 0:
                raise OrderExecutionError("Stop loss and take profit prices must be positive")
            if entry_price is not None and entry_price <= 0:
                raise OrderExecutionError(f"Invalid entry price: {entry_price}")
            if entry_type not in [OrderType.MARKET, OrderType.LIMIT]:
                raise OrderExecutionError(f"Invalid entry type: {entry_type}")

            # Get current market price for validation
            product = await self.client.get_product(product_id)
            current_price = float(product.price)
            
            # Validate account balance
            base_currency = product_id.split('-')[0]
            quote_currency = product_id.split('-')[1]
            
            # Get account balances
            accounts = await self.client.get_accounts()
            base_account = next((a for a in accounts if a.currency == base_currency), None)
            quote_account = next((a for a in accounts if a.currency == quote_currency), None)
            
            if not base_account or not quote_account:
                raise OrderExecutionError(f"Unable to find accounts for {base_currency} or {quote_currency}")
            
            # Check if we have enough funds
            if side == OrderSide.BUY:
                required_funds = size * (entry_price or current_price)
                if float(quote_account.available) < required_funds:
                    raise OrderExecutionError(
                        f"Insufficient {quote_currency} funds. Required: {required_funds}, Available: {quote_account.available}"
                    )
            else:  # SELL
                if float(base_account.available) < size:
                    raise OrderExecutionError(
                        f"Insufficient {base_currency} funds. Required: {size}, Available: {base_account.available}"
                    )
                
            # Additional price validation for long/short positions
            if side == OrderSide.BUY:
                if entry_price:
                    if stop_loss_price >= entry_price:
                        raise OrderExecutionError("Stop loss must be below entry price for long positions")
                    if take_profit_price <= entry_price:
                        raise OrderExecutionError("Take profit must be above entry price for long positions")
                else:
                    # For market orders, use current price as reference
                    if stop_loss_price >= current_price:
                        raise OrderExecutionError("Stop loss must be below current price for long positions")
                    if take_profit_price <= current_price:
                        raise OrderExecutionError("Take profit must be above current price for long positions")
            else:  # SELL
                if entry_price:
                    if stop_loss_price <= entry_price:
                        raise OrderExecutionError("Stop loss must be above entry price for short positions")
                    if take_profit_price >= entry_price:
                        raise OrderExecutionError("Take profit must be below entry price for short positions")
                else:
                    # For market orders, use current price as reference
                    if stop_loss_price <= current_price:
                        raise OrderExecutionError("Stop loss must be above current price for short positions")
                    if take_profit_price >= current_price:
                        raise OrderExecutionError("Take profit must be below current price for short positions")

            # Place entry order
            if entry_type == OrderType.MARKET:
                entry_result = await self.execute_market_order(
                    product_id=product_id,
                    side=side,
                    size=size,
                    client_order_id=None
                )
            else:
                if not entry_price:
                    raise OrderExecutionError("Entry price is required for limit orders")
                entry_result = await self.execute_limit_order(
                    product_id=product_id,
                    side=side,
                    size=size,
                    price=entry_price,
                    client_order_id=None,
                    time_in_force=time_in_force or self.default_time_in_force
                )

            if not entry_result.success:
                return BracketOrderResult(
                    success=False,
                    error=entry_result.error or "Failed to place entry order",
                    execution_time=datetime.utcnow(),
                    metadata={
                        "error_type": "entry_order_failed",
                        "entry_type": entry_type.value,
                        "execution_latency": (datetime.utcnow() - start_time).total_seconds()
                    }
                )

            # Place stop loss order
            stop_loss_side = OrderSide.SELL if side == OrderSide.BUY else OrderSide.BUY
            stop_loss_result = await self.execute_limit_order(
                product_id=product_id,
                side=stop_loss_side,
                size=size,
                price=stop_loss_price,
                client_order_id=None,
                time_in_force=time_in_force or self.default_time_in_force
            )

            # Place take profit order
            take_profit_side = OrderSide.SELL if side == OrderSide.BUY else OrderSide.BUY
            take_profit_result = await self.execute_limit_order(
                product_id=product_id,
                side=take_profit_side,
                size=size,
                price=take_profit_price,
                client_order_id=None,
                time_in_force=time_in_force or self.default_time_in_force
            )

            # Start monitoring the bracket order
            asyncio.create_task(self.monitor_bracket_order(BracketOrderResult(
                success=True,
                entry_order=entry_result.order,
                stop_loss_order=stop_loss_result.order,
                take_profit_order=take_profit_result.order,
                execution_time=datetime.utcnow(),
                metadata={
                    "entry_type": entry_type.value,
                    "position_side": side.value,
                    "stop_loss_success": stop_loss_result.success,
                    "take_profit_success": take_profit_result.success,
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds()
                }
            )))

            return BracketOrderResult(
                success=True,
                entry_order=entry_result.order,
                stop_loss_order=stop_loss_result.order,
                take_profit_order=take_profit_result.order,
                execution_time=datetime.utcnow(),
                metadata={
                    "entry_type": entry_type.value,
                    "position_side": side.value,
                    "stop_loss_success": stop_loss_result.success,
                    "take_profit_success": take_profit_result.success,
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds()
                }
            )

        except Exception as e:
            logger.error(f"Error executing bracket order: {str(e)}")
            return BracketOrderResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={
                    "error_type": "execution_error",
                    "entry_type": entry_type.value if isinstance(entry_type, OrderType) else str(entry_type),
                    "execution_latency": (datetime.utcnow() - start_time).total_seconds()
                }
            )

    async def monitor_bracket_order(self, bracket_result: BracketOrderResult):
        """
        Monitor and manage a bracket order set.
        
        This method runs as a background task and:
        1. Monitors the entry order until it's filled or cancelled
        2. Once filled, monitors the stop loss and take profit orders
        3. If one exit order is triggered, cancels the other
        4. Handles any errors during the process
        
        Args:
            bracket_result: The result from execute_bracket_order containing all order details
        """
        try:
            while True:
                # Get current status of entry order
                entry_status = await self.get_order_status(bracket_result.entry_order.order_id)
                
                if entry_status.status == OrderStatus.FILLED:
                    # Entry is filled, monitor exit orders
                    stop_loss_status = await self.get_order_status(bracket_result.stop_loss_order.order_id)
                    take_profit_status = await self.get_order_status(bracket_result.take_profit_order.order_id)
                    
                    # If either exit order is filled, cancel the other
                    if stop_loss_status.status == OrderStatus.FILLED:
                        await self.cancel_order(bracket_result.take_profit_order.order_id)
                        logger.info(f"Stop loss triggered for bracket order {bracket_result.entry_order.order_id}")
                        break
                    elif take_profit_status.status == OrderStatus.FILLED:
                        await self.cancel_order(bracket_result.stop_loss_order.order_id)
                        logger.info(f"Take profit triggered for bracket order {bracket_result.entry_order.order_id}")
                        break
                    elif stop_loss_status.status == OrderStatus.CANCELLED and take_profit_status.status == OrderStatus.CANCELLED:
                        logger.info(f"Both exit orders cancelled for bracket order {bracket_result.entry_order.order_id}")
                        break
                        
                elif entry_status.status == OrderStatus.CANCELLED:
                    # Entry was cancelled, cancel exit orders
                    await self.cancel_bracket_order(
                        bracket_result.entry_order.order_id,
                        bracket_result.stop_loss_order.order_id,
                        bracket_result.take_profit_order.order_id
                    )
                    logger.info(f"Entry order cancelled, cancelling exit orders for bracket order {bracket_result.entry_order.order_id}")
                    break
                    
                # Wait before next check
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error monitoring bracket order {bracket_result.entry_order.order_id}: {str(e)}")
            # Attempt to cancel all orders in case of error
            try:
                await self.cancel_bracket_order(
                    bracket_result.entry_order.order_id,
                    bracket_result.stop_loss_order.order_id,
                    bracket_result.take_profit_order.order_id
                )
            except Exception as cancel_error:
                logger.error(f"Error cancelling orders after monitoring error: {str(cancel_error)}")
            
    async def cancel_bracket_order(
        self,
        entry_order_id: str,
        stop_loss_order_id: str,
        take_profit_order_id: str
    ) -> List[OrderExecutionResult]:
        """
        Cancel all orders in a bracket order set.
        
        Args:
            entry_order_id: ID of the entry order
            stop_loss_order_id: ID of the stop-loss order
            take_profit_order_id: ID of the take-profit order
            
        Returns:
            List of OrderExecutionResults for each cancellation
        """
        results = []
        for order_id in [entry_order_id, stop_loss_order_id, take_profit_order_id]:
            try:
                result = await self.cancel_order(order_id)
                results.append(result)
            except Exception as e:
                logger.error(f"Error cancelling order {order_id}: {str(e)}")
                results.append(OrderExecutionResult(
                    success=False,
                    error=f"Cancel error: {str(e)}",
                    execution_time=datetime.now(),
                    metadata={"error_type": "execution_error"}
                ))
        return results
            
    async def cancel_order(self, order_id: str) -> OrderExecutionResult:
        """
        Cancel an existing order.
        
        Args:
            order_id: ID of the order to cancel
            
        Returns:
            OrderExecutionResult with cancellation details
        """
        try:
            start_time = datetime.utcnow()
            
            # Cancel the order
            result = await self.client.cancel_order(order_id)
            
            return OrderExecutionResult(
                success=True,
                execution_time=start_time,
                metadata={
                    "execution_latency": (start_time - datetime.utcnow()).total_seconds(),
                    "action": "cancel",
                    "cancel_response": result
                }
            )
            
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            return OrderExecutionResult(
                success=False,
                error=f"Order cancellation error: {str(e)}",
                execution_time=datetime.now(),
                metadata={"error_type": "execution_error"}
            )
            
    async def get_order_status(self, order_id: str) -> Optional[Dict]:
        """Get the status and details of a specific order."""
        logger.debug(f"Getting status for order ID: {order_id}")
        # Check internal cache first
        if order_id in self._order_states:
            logger.debug(f"Order {order_id} found in internal state cache.")
            # Return a representation compatible with expected output, might need adjustment
            # For now, just return the state model dict. Might need Pydantic model.
            return self._order_states[order_id].model_dump() # Return dict from Pydantic model
            
        # If not in cache, fetch from API
        try:
            order_data = await self.client.get_order(order_id)
            # TODO: Update internal cache self._order_states here if needed
            # TODO: Potentially parse order_data dict into a consistent Pydantic model before returning
            return order_data # Return raw dict from client
        except Exception as e:
            logger.error(f"Failed to get status for order {order_id} from API: {e}")
            if e.status_code == 404:
                return None # Order not found
            raise OrderExecutionError(f"API error fetching order {order_id}: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error fetching order status for {order_id}: {e}", exc_info=True)
            raise OrderExecutionError(f"Unexpected error fetching order status: {e}") from e

    async def get_open_orders(
        self,
        product_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Get a list of all open orders, optionally filtered by product ID.
        
        Returns:
            List of open order details (raw dictionaries from API).
        """
        logger.debug(f"Getting open orders for product: {product_id or 'all'}")
        try:
            # Filter for non-final statuses
            open_statuses = [
                OrderStatus.PENDING,
                OrderStatus.OPEN,
                # Add other potentially relevant non-final statuses if applicable
            ]
            orders = await self.client.get_orders(product_id=product_id, status=open_statuses)
            # TODO: Potentially parse list of dicts into consistent Pydantic models
            return orders # Return raw list of dicts
        except Exception as e:
            logger.error(f"Failed to get open orders from API: {e}")
            raise OrderExecutionError(f"API error fetching open orders: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error fetching open orders: {e}", exc_info=True)
            raise OrderExecutionError(f"Unexpected error fetching open orders: {e}") from e

    async def validate_signal(
        self,
        db: AsyncSession, 
        product_id: str,
        zone: Zone,
        side: Union[str, OrderSide],
        ohlcv_data: pd.DataFrame,
        min_confidence: Optional[float] = None
    ) -> SignalConfirmation:
        """
        Validate a trading signal before executing an order.
        
        Args:
            db: Database session
            product_id: Trading pair ID (e.g., BTC-USD)
            zone: Supply/Demand zone triggering the signal
            side: Intended order side (BUY/SELL)
            ohlcv_data: Recent OHLCV data for technical analysis
            min_confidence: Optional override for minimum confidence threshold
            
        Returns:
            SignalConfirmation object with validation results
            
        Raises:
            OrderExecutionError: If signal manager is not configured
        """
        if not self.signal_manager:
            raise OrderExecutionError("Signal manager not configured for signal validation")
            
        try:
            # Convert side to enum if needed
            if isinstance(side, str):
                side = OrderSide(side.upper())
                
            # Get signal confirmation
            confirmation = await self.signal_manager.confirm_zone_signal(
                db=db, 
                zone=zone,
                ohlcv_data=ohlcv_data,
                side=side
            )
            
            # Check if signal meets minimum confidence threshold
            threshold = min_confidence or self.min_signal_confidence
            if confirmation.confidence_score < threshold:
                logger.warning(
                    f"Signal confidence {confirmation.confidence_score:.2f} below threshold {threshold}"
                    f" for {product_id} {side.value} signal in zone {zone.zone_id}"
                )
                
            return confirmation
            
        except Exception as e:
            logger.error(f"Error validating signal: {str(e)}")
            raise OrderExecutionError(f"Signal validation failed: {str(e)}")

    async def execute_zone_order(
        self,
        db: AsyncSession, 
        zone: 'Zone',
        size: float,
        ohlcv_data: pd.DataFrame,
        entry_type: Union[str, OrderType] = OrderType.MARKET,
        time_in_force: Optional[TimeInForce] = None,
        skip_signal_confirmation: bool = False
    ) -> BracketOrderResult:
        """
        Execute an order based on a supply/demand zone with signal confirmation.
        
        This method:
        1. Validates the trading signal using technical indicators
        2. Calculates appropriate entry, stop loss, and take profit prices
        3. Places a bracket order with the calculated parameters
        
        Args:
            db: Database session
            zone: The supply/demand zone to trade
            size: Order size in base currency
            ohlcv_data: OHLCV data for signal confirmation
            entry_type: Order type for entry (MARKET/LIMIT)
            time_in_force: Time in force for limit orders
            skip_signal_confirmation: Whether to skip signal confirmation
            
        Returns:
            BracketOrderResult containing the execution details
            
        Raises:
            OrderExecutionError: If validation fails or order execution fails
        """
        try:
            # Confirm signal if required
            if not skip_signal_confirmation:
                # Pass db session down
                confirmation = await self.validate_signal(db=db, product_id=zone.product_id, zone=zone, side=zone.zone_type, ohlcv_data=ohlcv_data)
                if confirmation and not confirmation.is_confirmed:
                    return BracketOrderResult(
                        success=False,
                        error="Signal not confirmed",
                        execution_time=datetime.utcnow(),
                        metadata={
                            "error_type": "signal_validation_failed",
                            "confidence_score": confirmation.confidence_score,
                            "confirmation_factors": confirmation.confirmation_factors
                        }
                    )
            
            # Determine order side based on zone type
            side = OrderSide.SELL if zone.zone_type == "supply" else OrderSide.BUY
            
            # Calculate entry price for limit orders
            entry_price = None
            if entry_type == OrderType.LIMIT:
                entry_price = (
                    zone.price_low if side == OrderSide.BUY else zone.price_high
                )
            
            # Calculate stop loss and take profit prices
            risk_distance = abs(zone.price_high - zone.price_low)
            if side == OrderSide.BUY:
                stop_loss_price = zone.price_low - (risk_distance * 0.1)  # 10% below zone
                take_profit_price = zone.price_high + (risk_distance * 2)  # 2R profit target
            else:
                stop_loss_price = zone.price_high + (risk_distance * 0.1)  # 10% above zone
                take_profit_price = zone.price_low - (risk_distance * 2)  # 2R profit target
            
            # Execute the bracket order
            result = await self.execute_bracket_order(
                product_id=zone.product_id,
                side=side,
                size=size,
                stop_loss_price=stop_loss_price,
                take_profit_price=take_profit_price,
                entry_price=entry_price,
                entry_type=entry_type,
                time_in_force=time_in_force
            )
            
            # Add zone information to metadata
            if result.metadata is None:
                result.metadata = {}
            result.metadata.update({
                "zone_id": zone.id,
                "zone_type": zone.zone_type,
                "zone_price_range": [zone.price_low, zone.price_high],
                "risk_distance": risk_distance
            })
            
            return result
            
        except OrderExecutionError:
            raise
        except Exception as e:
            logger.error(f"Error executing zone order: {str(e)}")
            return BracketOrderResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={
                    "error_type": "execution_error",
                    "zone_id": zone.id,
                    "zone_type": zone.zone_type
                }
            )

    async def _update_position(self, order_state: OrderState, price_update: float) -> None:
        """Update position based on order state changes"""
        position = self._positions.get(order_state.product_id)
        
        if not position and order_state.status == OrderStatus.FILLED:
            # New position
            position = Position(
                product_id=order_state.product_id,
                side=order_state.side,
                size=order_state.filled_size,
                entry_price=order_state.average_fill_price or order_state.price,
                current_price=price_update,
                unrealized_pnl=0.0,
                entry_time=datetime.now(),
                last_update_time=datetime.now(),
                orders=[order_state.order_id]
            )
            self._positions[order_state.product_id] = position
            
        elif position:
            # Update existing position
            if order_state.status == OrderStatus.FILLED:
                if order_state.side == position.side:
                    # Adding to position
                    new_size = position.size + order_state.filled_size
                    new_entry_price = (
                        (position.entry_price * position.size) +
                        (order_state.average_fill_price * order_state.filled_size)
                    ) / new_size
                    position.size = new_size
                    position.entry_price = new_entry_price
                else:
                    # Reducing/closing position
                    realized_pnl = (
                        order_state.average_fill_price - position.entry_price
                    ) * order_state.filled_size
                    if order_state.side == OrderSide.SELL:
                        realized_pnl *= -1
                        
                    position.realized_pnl += realized_pnl
                    position.size -= order_state.filled_size
                    
                    if position.size <= 0:
                        position.status = "CLOSED"
                    else:
                        position.status = "PARTIALLY_CLOSED"
                        
            position.current_price = price_update
            position.last_update_time = datetime.now()
            position.unrealized_pnl = (
                position.current_price - position.entry_price
            ) * position.size
            if position.side == OrderSide.SELL:
                position.unrealized_pnl *= -1
                
            if order_state.order_id not in position.orders:
                position.orders.append(order_state.order_id)

    async def _update_order_state(self, order_id: str, new_status: OrderStatus) -> None:
        """Update the state of an order and record the transition."""
        if order_id not in self._order_states:
            logger.warning(f"Attempted to update non-existent order state: {order_id}")
            return
            
        order_state = self._order_states[order_id]
        old_status = order_state.status
        
        # Record state transition
        transition = {
            "timestamp": datetime.utcnow(),
            "from_status": old_status,
            "to_status": new_status,
            "filled_size": order_state.filled_size,
            "remaining_size": order_state.remaining_size
        }
        order_state.state_transitions.append(transition)
        
        # Update status
        order_state.status = new_status
        order_state.last_update_time = datetime.utcnow()
        
        # Move to historical orders if terminal state
        if new_status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.EXPIRED]:
            if order_state.product_id not in self._historical_orders:
                self._historical_orders[order_state.product_id] = []
            self._historical_orders[order_state.product_id].append(order_state)
            del self._order_states[order_id]
            
        # Update performance metrics
        if new_status == OrderStatus.FILLED:
            self._performance_metrics["fill_rates"].append(
                order_state.filled_size / order_state.size
            )
            self._performance_metrics["success_rates"].append(1.0)
        elif new_status in [OrderStatus.CANCELLED, OrderStatus.EXPIRED]:
            self._performance_metrics["success_rates"].append(0.0)

    async def get_position(self, product_id: str) -> Optional[Position]:
        """Get current position for a product"""
        return self._positions.get(product_id)

    async def get_all_positions(self) -> List[Position]:
        """Get all open positions"""
        return [p for p in self._positions.values() if p.status == "OPEN"]

    async def get_position_risk_metrics(self, product_id: str) -> Dict[str, float]:
        """Get risk metrics for a position"""
        position = await self.get_position(product_id)
        if not position:
            return {}
            
        current_price = float((await self.client.get_product(product_id))["price"])
        position.current_price = current_price
        
        # Calculate risk metrics
        position.risk_metrics.update({
            "unrealized_pnl_pct": (position.unrealized_pnl / (position.entry_price * position.size)) * 100,
            "position_value": position.size * current_price,
            "max_drawdown": min(0, position.unrealized_pnl),
            "time_in_position": (datetime.now() - position.entry_time).total_seconds() / 3600  # hours
        })
        
        return position.risk_metrics

    async def get_performance_metrics(self) -> Dict[str, float]:
        """Get aggregated performance metrics"""
        if not any(self._performance_metrics.values()):
            return {}
            
        return {
            "avg_execution_latency": statistics.mean(self._performance_metrics["execution_latency"]),
            "avg_fill_rate": statistics.mean(self._performance_metrics["fill_rates"]),
            "success_rate": statistics.mean(self._performance_metrics["success_rates"]),
            "total_orders": len(self._performance_metrics["success_rates"])
        }

    async def halt_trading(self, reason: str = "Emergency halt triggered"):
        """Emergency kill-switch to halt all trading activity."""
        self._trading_enabled = False
        # Cancel all open orders
        open_orders = await self.get_open_orders()
        for order in open_orders:
            try:
                await self.cancel_order(order.order_id)
                logger.warning(f"Cancelled order {order.order_id} during trading halt")
            except Exception as e:
                logger.error(f"Failed to cancel order {order.order_id}: {str(e)}")
        
        # Log the halt
        logger.critical(f"Trading halted: {reason}")
        
        # Notify any registered callbacks
        if hasattr(self, '_halt_callbacks'):
            for callback in self._halt_callbacks:
                await callback(reason)

    async def resume_trading(self, confirmation: str = "Manual resume"):
        """Resume trading after a halt."""
        if not self._trading_enabled:
            logger.info(f"Resuming trading: {confirmation}")
            self._trading_enabled = True

    async def check_risk_thresholds(self, position: Position) -> tuple[bool, str]:
        """Check if any risk thresholds are breached."""
        if abs(position.size) > self._risk_thresholds['max_position_size']:
            return False, f"Position size {position.size} exceeds maximum {self._risk_thresholds['max_position_size']}"
        
        if position.unrealized_pnl_pct < -self._risk_thresholds['max_drawdown_pct']:
            return False, f"Position drawdown {position.unrealized_pnl_pct}% exceeds maximum {self._risk_thresholds['max_drawdown_pct']}%"
        
        daily_pnl_pct = (self._daily_stats['total_pnl'] / self._daily_stats['start_balance']) * 100
        if daily_pnl_pct < -self._risk_thresholds['max_daily_loss_pct']:
            return False, f"Daily loss {daily_pnl_pct}% exceeds maximum {self._risk_thresholds['max_daily_loss_pct']}%"
        
        return True, "Risk thresholds within limits"

    async def update_position(self, product_id: str, order_update: dict):
        """Update position based on order updates."""
        position = await self.get_position(product_id)
        if position:
            # Update position based on order
            filled_size = float(order_update.get('filled_size', 0))
            side = order_update.get('side')
            price = float(order_update.get('average_filled_price', 0))
            
            if side == OrderSide.BUY:
                position.size += filled_size
            else:
                position.size -= filled_size
            
            # Update average entry price
            if position.size > 0:
                position.entry_price = ((position.entry_price * (position.size - filled_size)) + 
                                     (price * filled_size)) / position.size
            
            # Check risk thresholds
            is_safe, message = await self.check_risk_thresholds(position)
            if not is_safe:
                await self.halt_trading(message)
                # Initiate emergency position reduction if needed
                await self._emergency_position_reduction(position)

    async def _emergency_position_reduction(self, position: Position):
        """Reduce position size in emergency situations."""
        if abs(position.size) > self._risk_thresholds['max_position_size']:
            reduction_size = abs(position.size) - self._risk_thresholds['max_position_size']
            side = OrderSide.SELL if position.size > 0 else OrderSide.BUY
            
            try:
                await self.execute_market_order(
                    product_id=position.product_id,
                    side=side,
                    size=reduction_size,
                    reduce_only=True
                )
                logger.warning(f"Emergency position reduction executed: {reduction_size} {position.product_id}")
            except Exception as e:
                logger.error(f"Failed emergency position reduction: {str(e)}")

    def register_halt_callback(self, callback: Callable):
        """Register a callback to be notified on trading halts."""
        if not hasattr(self, '_halt_callbacks'):
            self._halt_callbacks = []
        self._halt_callbacks.append(callback)

    async def get_daily_stats(self) -> dict:
        """Get daily trading statistics."""
        return {
            'start_balance': self._daily_stats['start_balance'],
            'current_balance': self._daily_stats['current_balance'],
            'total_pnl': self._daily_stats['total_pnl'],
            'pnl_percentage': (self._daily_stats['total_pnl'] / self._daily_stats['start_balance'] * 100) 
                            if self._daily_stats['start_balance'] > 0 else 0,
            'trade_count': self._daily_stats['trade_count']
        }

    def update_risk_thresholds(self, thresholds: dict):
        """Update risk management thresholds."""
        self._risk_thresholds.update(thresholds)
        logger.info(f"Risk thresholds updated: {self._risk_thresholds}")

    async def start_position_monitoring(self):
        """Start monitoring all positions."""
        for product_id in self._positions:
            if product_id not in self._position_monitors:
                self._position_monitors[product_id] = asyncio.create_task(
                    self._monitor_position(product_id)
                )

    async def stop_position_monitoring(self):
        """Stop all position monitoring tasks."""
        for task in self._position_monitors.values():
            task.cancel()
        self._position_monitors.clear()

    async def _monitor_position(self, product_id: str):
        """Monitor a position continuously."""
        try:
            while True:
                position = self._positions.get(product_id)
                if not position or position.status == "CLOSED":
                    break

                # Update current price
                product = await self.client.get_product(product_id)
                current_price = float(product["price"])
                
                # Update position metrics
                old_pnl = position.unrealized_pnl
                position.current_price = current_price
                position.unrealized_pnl = (current_price - position.entry_price) * position.size
                if position.side == OrderSide.SELL:
                    position.unrealized_pnl *= -1
                
                # Calculate and cache risk metrics
                risk_metrics = await self.get_position_risk_metrics(product_id)
                self._risk_metrics_cache[product_id] = {
                    "metrics": risk_metrics,
                    "timestamp": datetime.now()
                }
                
                # Check for significant P&L changes (>1%)
                pnl_change_pct = abs((position.unrealized_pnl - old_pnl) / (position.entry_price * position.size) * 100)
                if pnl_change_pct > 1.0:
                    self._position_events.append({
                        "type": "pnl_change",
                        "product_id": product_id,
                        "old_pnl": old_pnl,
                        "new_pnl": position.unrealized_pnl,
                        "change_pct": pnl_change_pct,
                        "timestamp": datetime.now()
                    })
                
                # Check risk thresholds
                is_safe, message = await self.check_risk_thresholds(position)
                if not is_safe:
                    self._position_events.append({
                        "type": "risk_threshold_breach",
                        "product_id": product_id,
                        "message": message,
                        "timestamp": datetime.now()
                    })
                    await self.halt_trading(message)
                
                await asyncio.sleep(1)  # Update frequency
                
        except asyncio.CancelledError:
            logger.info(f"Position monitoring stopped for {product_id}")
        except Exception as e:
            logger.error(f"Error monitoring position {product_id}: {str(e)}")
            self._position_events.append({
                "type": "monitor_error",
                "product_id": product_id,
                "error": str(e),
                "timestamp": datetime.now()
            })

    async def get_aggregated_risk_metrics(self) -> Dict[str, Any]:
        """Get aggregated risk metrics across all positions."""
        total_position_value = 0.0
        total_unrealized_pnl = 0.0
        max_drawdown = 0.0
        position_count = 0
        
        for product_id, position in self._positions.items():
            if position.status != "CLOSED":
                position_count += 1
                risk_metrics = await self.get_position_risk_metrics(product_id)
                total_position_value += risk_metrics["position_value"]
                total_unrealized_pnl += position.unrealized_pnl
                max_drawdown = min(max_drawdown, risk_metrics["max_drawdown"])
        
        daily_stats = await self.get_daily_stats()
        
        return {
            "total_position_value": total_position_value,
            "total_unrealized_pnl": total_unrealized_pnl,
            "total_unrealized_pnl_pct": (total_unrealized_pnl / total_position_value * 100) 
                                       if total_position_value > 0 else 0,
            "max_drawdown": max_drawdown,
            "position_count": position_count,
            "daily_pnl": daily_stats["total_pnl"],
            "daily_pnl_pct": daily_stats["pnl_percentage"],
            "risk_exposure": total_position_value / self._daily_stats["start_balance"] 
                           if self._daily_stats["start_balance"] > 0 else 0
        }

    async def get_position_events(
        self,
        product_id: Optional[str] = None,
        event_type: Optional[str] = None,
        start_time: Optional[datetime] = None
    ) -> List[Dict]:
        """Get position-related events with optional filtering."""
        events = self._position_events
        
        if product_id:
            events = [e for e in events if e["product_id"] == product_id]
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        if start_time:
            events = [e for e in events if e["timestamp"] >= start_time]
            
        return events

    def clear_position_events(self):
        """Clear the position events history."""
        self._position_events.clear()

    async def modify_order(
        self,
        order_id: str,
        new_size: Optional[float] = None,
        new_price: Optional[float] = None,
        new_time_in_force: Optional[str] = None
    ) -> OrderExecutionResult:
        """
        Modify an existing order's parameters.
        
        Args:
            order_id: ID of the order to modify
            new_size: New order size (optional)
            new_price: New order price (optional)
            new_time_in_force: New time in force setting (optional)
            
        Returns:
            OrderExecutionResult with modification details
        """
        try:
            if not self._trading_enabled:
                raise OrderExecutionError("Trading is currently halted")
                
            # Get current order state
            current_state = self._order_states.get(order_id)
            if not current_state:
                raise OrderExecutionError(f"Order {order_id} not found")
                
            if current_state.status not in [OrderStatus.OPEN, OrderStatus.PENDING]:
                raise OrderExecutionError(f"Cannot modify order in status: {current_state.status}")
                
            # Cancel existing order
            cancel_result = await self.cancel_order(order_id)
            if not cancel_result.success:
                raise OrderExecutionError(f"Failed to cancel order for modification: {cancel_result.error}")
                
            # Create new order with updated parameters
            new_order = await self.client.create_order(
                product_id=current_state.product_id,
                side=current_state.side,
                order_type=current_state.type,
                size=new_size or current_state.size,
                price=new_price or current_state.price,
                time_in_force=new_time_in_force or self.default_time_in_force
            )
            
            # Record modification
            modification = {
                "timestamp": datetime.utcnow(),
                "original_order_id": order_id,
                "new_order_id": new_order.order_id,
                "changes": {
                    "size": new_size if new_size else "unchanged",
                    "price": new_price if new_price else "unchanged",
                    "time_in_force": new_time_in_force if new_time_in_force else "unchanged"
                }
            }
            
            if order_id not in self._order_modifications:
                self._order_modifications[order_id] = []
            self._order_modifications[order_id].append(modification)
            
            # Update performance metrics
            self._performance_metrics["modification_success_rates"].append(1.0)
            
            return OrderExecutionResult(
                success=True,
                order=new_order,
                execution_time=datetime.utcnow(),
                metadata={"modification": modification}
            )
            
        except (OrderExecutionError, Exception) as e:
            logger.error(f"Error modifying order {order_id}: {str(e)}")
            self._performance_metrics["modification_success_rates"].append(0.0)
            return OrderExecutionResult(
                success=False,
                error=str(e),
                execution_time=datetime.utcnow(),
                metadata={"error_type": "modification_error"}
            )

    async def get_order_history(
        self,
        product_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        status: Optional[Union[str, List[str]]] = None
    ) -> List[OrderState]:
        """
        Retrieve historical orders with optional filtering.
        
        Args:
            product_id: Filter by product ID (optional)
            start_time: Filter by start time (optional)
            end_time: Filter by end time (optional)
            status: Filter by order status or list of statuses (optional)
            
        Returns:
            List of historical OrderState objects
        """
        if isinstance(status, str):
            status = [status]
            
        def matches_filters(order: OrderState) -> bool:
            if product_id and order.product_id != product_id:
                return False
            if start_time and order.last_update_time < start_time:
                return False
            if end_time and order.last_update_time > end_time:
                return False
            if status and order.status not in status:
                return False
            return True
            
        historical_orders = []
        for product_orders in self._historical_orders.values():
            historical_orders.extend(filter(matches_filters, product_orders))
            
        return sorted(historical_orders, key=lambda x: x.last_update_time, reverse=True)

    async def get_order_modifications(self, order_id: str) -> List[Dict]:
        """
        Get modification history for a specific order.
        
        Args:
            order_id: ID of the order
            
        Returns:
            List of modification records
        """
        return self._order_modifications.get(order_id, [])

    async def get_order_analytics(
        self,
        product_id: Optional[str] = None,
        time_window: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get analytics about order execution performance.
        
        Args:
            product_id: Filter by product ID (optional)
            time_window: Time window for analytics (e.g., '1d', '7d', '30d')
            
        Returns:
            Dictionary containing various order analytics
        """
        now = datetime.utcnow()
        if time_window:
            if time_window.endswith('d'):
                days = int(time_window[:-1])
                start_time = now - pd.Timedelta(days=days)
            else:
                raise ValueError("Invalid time window format. Use '1d', '7d', etc.")
        else:
            start_time = None
            
        # Get relevant orders
        orders = await self.get_order_history(
            product_id=product_id,
            start_time=start_time
        )
        
        if not orders:
            return {
                "total_orders": 0,
                "success_rate": 0.0,
                "avg_execution_time": 0.0,
                "fill_rate": 0.0,
                "modification_rate": 0.0
            }
            
        # Calculate analytics
        total_orders = len(orders)
        successful_orders = len([o for o in orders if o.status == OrderStatus.FILLED])
        modified_orders = len([o for o in orders if o.order_id in self._order_modifications])
        
        fill_sizes = [o.filled_size / o.size for o in orders if o.status == OrderStatus.FILLED]
        avg_fill_rate = statistics.mean(fill_sizes) if fill_sizes else 0.0
        
        return {
            "total_orders": total_orders,
            "success_rate": successful_orders / total_orders if total_orders > 0 else 0.0,
            "avg_execution_time": statistics.mean([
                len(o.state_transitions) for o in orders
            ]) if orders else 0.0,
            "fill_rate": avg_fill_rate,
            "modification_rate": modified_orders / total_orders if total_orders > 0 else 0.0,
            "status_distribution": {
                status: len([o for o in orders if o.status == status])
                for status in set(o.status for o in orders)
            }
        } 