from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict, Any
from decimal import Decimal

class TimeInForce(str, Enum):
    """Time in force options for orders."""
    GTC = "GTC"  # Good Till Cancelled
    GTT = "GTT"  # Good Till Time
    IOC = "IOC"  # Immediate Or Cancel
    FOK = "FOK"  # Fill Or Kill

class OrderSide(str, Enum):
    """Order side - buy or sell."""
    BUY = "buy"
    SELL = "sell"

class OrderType(str, Enum):
    """Type of order."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderStatus(str, Enum):
    """Status of an order."""
    PENDING = "pending"
    OPEN = "open"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"

class OrderBase(BaseModel):
    """Base model for orders."""
    product_id: str
    side: OrderSide
    type: OrderType
    size: Decimal
    time_in_force: Optional[TimeInForce] = TimeInForce.GTC
    client_order_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MarketOrder(OrderBase):
    """Market order model."""
    type: OrderType = OrderType.MARKET

class LimitOrder(OrderBase):
    """Limit order model."""
    type: OrderType = OrderType.LIMIT
    price: Decimal
    post_only: Optional[bool] = False 