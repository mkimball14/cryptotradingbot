from typing import Dict, Optional, List
from datetime import datetime
import logging
from pydantic import BaseModel

from app.core.coinbase import (
    CoinbaseClient,
    Order,
    OrderSide,
    OrderType,
    OrderStatus,
    CoinbaseError
)

logger = logging.getLogger(__name__)

class OrderExecutionError(Exception):
    """Custom exception for order execution errors"""
    pass

class OrderExecutionResult(BaseModel):
    """Model for order execution results"""
    success: bool
    order: Optional[Order] = None
    error: Optional[str] = None
    execution_time: datetime
    metadata: Optional[Dict] = None

class OrderExecutor:
    """
    Handles order execution and management for the trading system.
    Implements various order types and execution strategies.
    """
    
    def __init__(self, client: CoinbaseClient):
        """
        Initialize the OrderExecutor.
        
        Args:
            client: Initialized CoinbaseClient instance
        """
        self.client = client
        self.default_time_in_force = "GTC"  # Good Till Cancelled
        
    async def execute_market_order(
        self,
        product_id: str,
        side: str,
        size: float,
        **kwargs
    ) -> OrderExecutionResult:
        """
        Execute a market order.
        
        Args:
            product_id: Trading pair ID (e.g., BTC-USD)
            side: Order side (BUY/SELL)
            size: Order size in base currency
            **kwargs: Additional parameters to pass to the order
            
        Returns:
            OrderExecutionResult with execution details
            
        Raises:
            OrderExecutionError: If validation fails
        """
        try:
            start_time = datetime.now()
            
            # Validate inputs
            if side not in [OrderSide.BUY, OrderSide.SELL]:
                raise OrderExecutionError(f"Invalid order side: {side}")
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
                
            # Place market order
            order = await self.client.create_order(
                product_id=product_id,
                side=side,
                order_type=OrderType.MARKET,
                size=size,
                time_in_force=self.default_time_in_force,
                **kwargs
            )
            
            return OrderExecutionResult(
                success=True,
                order=order,
                execution_time=datetime.now(),
                metadata={
                    "execution_latency": (datetime.now() - start_time).total_seconds(),
                    "order_type": "market"
                }
            )
            
        except OrderExecutionError:
            raise
        except CoinbaseError as e:
            logger.error(f"Coinbase API error executing market order: {str(e)}")
            return OrderExecutionResult(
                success=False,
                error=f"Coinbase API error: {str(e)}",
                execution_time=datetime.now(),
                metadata={"error_type": "api_error"}
            )
        except Exception as e:
            logger.error(f"Error executing market order: {str(e)}")
            return OrderExecutionResult(
                success=False,
                error=f"Order execution error: {str(e)}",
                execution_time=datetime.now(),
                metadata={"error_type": "execution_error"}
            )
            
    async def execute_limit_order(
        self,
        product_id: str,
        side: str,
        size: float,
        price: float,
        **kwargs
    ) -> OrderExecutionResult:
        """
        Execute a limit order.
        
        Args:
            product_id: Trading pair ID (e.g., BTC-USD)
            side: Order side (BUY/SELL)
            size: Order size in base currency
            price: Limit price for the order
            **kwargs: Additional parameters to pass to the order
            
        Returns:
            OrderExecutionResult with execution details
            
        Raises:
            OrderExecutionError: If validation fails
        """
        try:
            start_time = datetime.now()
            
            # Validate inputs
            if side not in [OrderSide.BUY, OrderSide.SELL]:
                raise OrderExecutionError(f"Invalid order side: {side}")
            if size <= 0:
                raise OrderExecutionError(f"Invalid order size: {size}")
            if price <= 0:
                raise OrderExecutionError(f"Invalid price: {price}")
                
            # Place limit order
            order = await self.client.create_order(
                product_id=product_id,
                side=side,
                order_type=OrderType.LIMIT,
                size=size,
                price=price,
                time_in_force=self.default_time_in_force,
                **kwargs
            )
            
            return OrderExecutionResult(
                success=True,
                order=order,
                execution_time=datetime.now(),
                metadata={
                    "execution_latency": (datetime.now() - start_time).total_seconds(),
                    "order_type": "limit"
                }
            )
            
        except OrderExecutionError:
            raise
        except CoinbaseError as e:
            logger.error(f"Coinbase API error executing limit order: {str(e)}")
            return OrderExecutionResult(
                success=False,
                error=f"Coinbase API error: {str(e)}",
                execution_time=datetime.now(),
                metadata={"error_type": "api_error"}
            )
        except Exception as e:
            logger.error(f"Error executing limit order: {str(e)}")
            return OrderExecutionResult(
                success=False,
                error=f"Order execution error: {str(e)}",
                execution_time=datetime.now(),
                metadata={"error_type": "execution_error"}
            )
            
    async def cancel_order(self, order_id: str) -> OrderExecutionResult:
        """
        Cancel an existing order.
        
        Args:
            order_id: ID of the order to cancel
            
        Returns:
            OrderExecutionResult with cancellation details
        """
        try:
            start_time = datetime.now()
            
            # Cancel the order
            result = await self.client.cancel_order(order_id)
            
            return OrderExecutionResult(
                success=True,
                execution_time=datetime.now(),
                metadata={
                    "execution_latency": (datetime.now() - start_time).total_seconds(),
                    "action": "cancel",
                    "cancel_response": result
                }
            )
            
        except CoinbaseError as e:
            logger.error(f"Coinbase API error cancelling order: {str(e)}")
            return OrderExecutionResult(
                success=False,
                error=f"Coinbase API error: {str(e)}",
                execution_time=datetime.now(),
                metadata={"error_type": "api_error"}
            )
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            return OrderExecutionResult(
                success=False,
                error=f"Order cancellation error: {str(e)}",
                execution_time=datetime.now(),
                metadata={"error_type": "execution_error"}
            )
            
    async def get_order_status(self, order_id: str) -> Optional[Order]:
        """
        Get the current status of an order.
        
        Args:
            order_id: ID of the order to check
            
        Returns:
            Order object if found, None if not found
        """
        try:
            return await self.client.get_order(order_id)
        except CoinbaseError as e:
            logger.error(f"Error getting order status: {str(e)}")
            return None
            
    async def get_open_orders(
        self,
        product_id: Optional[str] = None
    ) -> List[Order]:
        """
        Get list of open orders.
        
        Args:
            product_id: Optional product ID to filter by
            
        Returns:
            List of open orders
        """
        try:
            return await self.client.get_orders(
                product_id=product_id,
                status=[OrderStatus.PENDING, OrderStatus.OPEN]
            )
        except CoinbaseError as e:
            logger.error(f"Error getting open orders: {str(e)}")
            return [] 