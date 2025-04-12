from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from decimal import Decimal

class TimeInForce(str, Enum):
    """Time in force options for orders."""
    GTC = "gtc"  # Good Till Canceled
    GTD = "gtd"  # Good Till Date
    IOC = "ioc"  # Immediate or Cancel
    FOK = "fok"  # Fill or Kill

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
    id: str = Field(default_factory=lambda: str(uuid4()))
    product_id: str = Field(default="BTC-USD")
    type: OrderType
    side: OrderSide
    size: float = Field(default=0.0)
    price: Optional[float] = None
    stop_price: Optional[float] = None
    filled_price: Optional[float] = None
    quantity: Optional[float] = None
    status: OrderStatus = OrderStatus.OPEN
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    done_at: Optional[datetime] = None
    done_reason: Optional[str] = None
    time_in_force: Optional[TimeInForce] = TimeInForce.GTC
    filled_size: float = 0
    filled_value: float = 0
    fees: float = 0
    realized_pnl: float = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    client_oid: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MarketOrder(OrderBase):
    """Market order model."""
    type: OrderType = OrderType.MARKET

class LimitOrder(OrderBase):
    """Limit order model."""
    type: OrderType = OrderType.LIMIT
    price: float
    post_only: bool = False 