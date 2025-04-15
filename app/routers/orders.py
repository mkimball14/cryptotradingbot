from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
import json

from app.core.coinbase import CoinbaseClient
from app.core.deps import get_coinbase_client
from app.models.order import OrderSide, OrderType, TimeInForce, OrderStatus
from app.models.responses import OrderDetailResponse, OrdersResponse, ErrorResponse

router = APIRouter(prefix="/orders", tags=["orders"])

class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "product_id": "BTC-USD",
                "side": OrderSide.BUY.value,
                "order_type": OrderType.LIMIT.value,
                "size": "0.01",
                "price": "50000.0",
                "time_in_force": TimeInForce.GTC.value
            }
        }
    )

    product_id: str = Field(..., description="Trading pair ID (e.g., BTC-USD)")
    side: OrderSide
    order_type: OrderType
    size: Decimal = Field(..., gt=Decimal(0), description="Order size in base currency (use string for precision)")
    price: Optional[Decimal] = Field(None, gt=Decimal(0), description="Limit price (required for LIMIT orders, use string for precision)")
    stop_price: Optional[Decimal] = Field(None, gt=Decimal(0), description="Stop price (required for STOP/STOP_LIMIT orders, use string for precision)")
    client_order_id: Optional[str] = Field(None, description="Client-specified order ID")
    time_in_force: TimeInForce = Field(TimeInForce.GTC, description="Time in force policy")

@router.post(
    "/",
    response_model=OrderDetailResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": OrderDetailResponse, "description": "Order created successfully"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid order parameters"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Create new order",
    description="Place a new order with the specified parameters"
)
async def create_order(
    order: CreateOrderRequest,
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> OrderDetailResponse:
    """
    Place a new order
    
    Creates a new order with the specified parameters. For LIMIT orders, price is required.
    For STOP/STOP_LIMIT orders, stop_price is required.
    """
    try:
        if order.order_type == OrderType.LIMIT and order.price is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Price is required for LIMIT orders"}
            )
            
        if order.order_type in [OrderType.STOP, OrderType.STOP_LIMIT] and order.stop_price is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Stop price is required for STOP/STOP_LIMIT orders"}
            )
            
        price_float = float(order.price) if order.price is not None else None
        stop_price_float = float(order.stop_price) if order.stop_price is not None else None
        size_float = float(order.size)
        
        result = await client.create_order(
            product_id=order.product_id,
            side=order.side,
            order_type=order.order_type,
            size=size_float,
            price=price_float,
            stop_price=stop_price_float,
            client_order_id=order.client_order_id,
            time_in_force=order.time_in_force
        )
        return OrderDetailResponse(order=result)
    except Exception as e:
        logger.error(f"Error creating order: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={"error": "Failed to create order due to an internal error."}
        )

@router.get(
    "/",
    response_model=OrdersResponse,
    responses={
        status.HTTP_200_OK: {"model": OrdersResponse, "description": "Successfully retrieved orders"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="List orders",
    description="Get a list of orders, optionally filtered by product"
)
async def list_orders(
    product_id: Optional[str] = Query(None, description="Filter orders by product ID"),
    status_filter: Optional[List[OrderStatus]] = Query(None, description="Filter orders by status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of orders to return"),
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> OrdersResponse:
    """
    List all orders, optionally filtered by product_id
    
    Returns a list of orders with their details. Can be filtered by product ID and status.
    """
    try:
        orders = await client.get_orders(product_id=product_id, status=status_filter, limit=limit)
        return OrdersResponse(orders=orders)
    except Exception as e:
        logger.error(f"Error listing orders: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to list orders due to an internal error."}
        )

@router.get(
    "/{order_id}",
    response_model=OrderDetailResponse,
    responses={
        status.HTTP_200_OK: {"model": OrderDetailResponse, "description": "Successfully retrieved order details"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Order not found"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get order details",
    description="Retrieve details of a specific order by ID"
)
async def get_order(
    order_id: str,
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> OrderDetailResponse:
    """
    Get details of a specific order
    
    Returns detailed information about a specific order by its ID.
    """
    try:
        order_data = await client.get_order(order_id)
        if not order_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Order with ID {order_id} not found"}
            )
        return OrderDetailResponse(order=order_data)
    except Exception as e:
        logger.error(f"Error getting order {order_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to retrieve order due to an internal error."}
        ) 