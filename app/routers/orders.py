from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

from app.core.coinbase import CoinbaseClient, OrderSide, OrderType, CoinbaseError
from app.core.deps import get_coinbase_client
from app.models.responses import OrderDetailResponse, OrdersResponse, ErrorResponse

router = APIRouter(prefix="/orders", tags=["orders"])

class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "product_id": "BTC-USD",
                "side": "BUY",
                "order_type": "LIMIT",
                "size": 0.01,
                "price": 50000.0,
                "time_in_force": "GTC"
            }
        }
    )

    product_id: str = Field(..., description="Trading pair ID (e.g., BTC-USD)")
    side: Literal["BUY", "SELL"] = Field(..., description="Order side (BUY/SELL)")
    order_type: Literal["MARKET", "LIMIT", "STOP", "STOP_LIMIT"] = Field(..., description="Order type")
    size: float = Field(..., gt=0, description="Order size in base currency")
    price: Optional[float] = Field(None, gt=0, description="Limit price (required for LIMIT orders)")
    stop_price: Optional[float] = Field(None, gt=0, description="Stop price (required for STOP/STOP_LIMIT orders)")
    client_order_id: Optional[str] = Field(None, description="Client-specified order ID")
    time_in_force: str = Field("GTC", description="Time in force policy (GTC/GTT/IOC/FOK)")

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
        # Validate order parameters
        if order.order_type == "LIMIT" and order.price is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Price is required for LIMIT orders"}
            )
            
        if order.order_type in ["STOP", "STOP_LIMIT"] and order.stop_price is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Stop price is required for STOP/STOP_LIMIT orders"}
            )
            
        result = await client.create_order(
            product_id=order.product_id,
            side=order.side,
            order_type=order.order_type,
            size=order.size,
            price=order.price,
            stop_price=order.stop_price,
            client_order_id=order.client_order_id,
            time_in_force=order.time_in_force
        )
        return {"order": result}
    except CoinbaseError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "code": e.status_code, "details": e.response}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
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
    status_filter: Optional[List[str]] = Query(None, description="Filter orders by status (comma-separated)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of orders to return"),
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> OrdersResponse:
    """
    List all orders, optionally filtered by product_id
    
    Returns a list of orders with their details. Can be filtered by product ID and status.
    """
    try:
        orders = await client.get_orders(product_id=product_id, status=status_filter, limit=limit)
        return {"orders": orders}
    except CoinbaseError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "code": e.status_code, "details": e.response}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
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
        order = await client.get_order(order_id)
        return {"order": order}
    except CoinbaseError as e:
        status_code = e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        if status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Order with ID {order_id} not found"}
            )
        raise HTTPException(
            status_code=status_code,
            detail={"error": str(e), "code": e.status_code, "details": e.response}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
        ) 