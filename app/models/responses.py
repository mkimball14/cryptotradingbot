from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Account Models
class AccountResponse(BaseModel):
    id: str
    currency: str
    balance: float
    available: float
    hold: float
    profile_id: str
    trading_enabled: bool

class PositionResponse(BaseModel):
    product_id: str
    position_size: float
    entry_price: float
    mark_price: float
    unrealized_pl: float
    realized_pl: float
    initial_margin: float
    maintenance_margin: float

class AccountsResponse(BaseModel):
    accounts: List[AccountResponse]

class PositionsResponse(BaseModel):
    positions: List[PositionResponse]

# Order Models
class OrderResponse(BaseModel):
    order_id: str
    client_order_id: Optional[str] = None
    product_id: str
    side: str
    order_type: str
    status: str
    time_in_force: str
    created_time: datetime
    price: Optional[float] = None
    size: float
    filled_size: float
    average_filled_price: Optional[float] = None

class OrdersResponse(BaseModel):
    orders: List[OrderResponse]

class OrderDetailResponse(BaseModel):
    order: OrderResponse

# Market Data Models
class ProductResponse(BaseModel):
    id: str
    display_name: str
    base_currency: str
    quote_currency: str
    status: str
    trading_disabled: bool
    price_increment: float
    quote_increment: float
    min_market_funds: float
    min_size: float

class ProductsResponse(BaseModel):
    products: List[Dict[str, Any]]

class ProductDetailResponse(BaseModel):
    id: str
    base_currency: str
    quote_currency: str
    base_min_size: str
    base_max_size: str
    quote_increment: str
    base_increment: str
    display_name: str
    min_market_funds: str
    max_market_funds: str
    margin_enabled: bool
    post_only: bool
    limit_only: bool
    cancel_only: bool
    trading_disabled: bool
    status: str
    status_message: str

class CandleBase(BaseModel):
    """Base candle data that's always present"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class EnrichedCandle(CandleBase):
    """Candle data with additional technical indicators"""
    typical_price: Optional[float] = Field(None, description="(High + Low + Close) / 3")
    body_size: Optional[float] = Field(None, description="Absolute difference between open and close")
    upper_shadow: Optional[float] = Field(None, description="Distance from high to the higher of open/close")
    lower_shadow: Optional[float] = Field(None, description="Distance from the lower of open/close to low")
    price_change: Optional[float] = Field(None, description="Price change from previous candle")
    returns: Optional[float] = Field(None, description="Percentage return from previous candle")
    volume_ma: Optional[float] = Field(None, description="20-period volume moving average")
    volume_std: Optional[float] = Field(None, description="20-period volume standard deviation")
    is_doji: Optional[bool] = Field(None, description="Whether the candle is a doji pattern")

class CandlesResponse(BaseModel):
    """Response model for OHLCV data endpoints"""
    candles: List[EnrichedCandle]
    symbol: str
    timeframe: str
    cleaned: bool = Field(True, description="Whether the data has been cleaned and enriched")
    count: int = Field(..., description="Number of candles returned")

class TradeResponse(BaseModel):
    trade_id: str
    product_id: str
    price: float
    size: float
    time: datetime
    side: str
    bid: Optional[float] = None
    ask: Optional[float] = None

class TradesResponse(BaseModel):
    trades: List[Dict[str, Any]]

class OrderBookResponse(BaseModel):
    bids: List[List[str]]
    asks: List[List[str]]
    sequence: int

# Common API Response
class ApiResponse(BaseModel):
    status: str
    message: str = "Success"
    data: Optional[Dict[str, Any]] = None

# Error Responses
class ErrorResponse(BaseModel):
    error: str
    code: Optional[int] = None
    details: Optional[Dict[str, Any]] = None 