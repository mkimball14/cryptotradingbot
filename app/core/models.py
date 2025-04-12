from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, Dict

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

@dataclass
class Order:
    id: str
    type: OrderType
    side: OrderSide
    symbol: str
    quantity: float
    price: Optional[float]
    status: OrderStatus
    timestamp: datetime
    filled_price: Optional[float] = None
    filled_quantity: Optional[float] = None
    filled_timestamp: Optional[datetime] = None
    fees: float = 0.0
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class Position:
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    timestamp: datetime
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    fees: float = 0.0
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {} 