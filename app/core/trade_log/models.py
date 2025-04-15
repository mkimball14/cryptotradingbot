from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from .base import Base
import enum

# Define enums for specific fields to ensure consistency
class TradeSide(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str, enum.Enum):
    SIGNAL = "SIGNAL"
    ORDER_SENT = "ORDER_SENT"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    ERROR = "ERROR"

class EventType(str, enum.Enum):
    ENTRY_SIGNAL = "ENTRY_SIGNAL"
    EXIT_SIGNAL = "EXIT_SIGNAL"
    ENTRY_ORDER = "ENTRY_ORDER"
    EXIT_ORDER = "EXIT_ORDER"
    ENTRY_FILL = "ENTRY_FILL"
    EXIT_FILL = "EXIT_FILL"
    STOP_LOSS_TRIGGERED = "STOP_LOSS_TRIGGERED"
    TAKE_PROFIT_TRIGGERED = "TAKE_PROFIT_TRIGGERED"
    ORDER_UPDATE = "ORDER_UPDATE"
    SYSTEM_STATUS = "SYSTEM_STATUS"
    WARNING = "WARNING"
    ERROR = "ERROR"

class TradeLog(Base):
    __tablename__ = "trade_logs"

    id = Column(Integer, primary_key=True, index=True)
    # Timestamp of the log entry creation
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    # Timestamp of the event itself (e.g., signal time, fill time)
    event_timestamp = Column(DateTime(timezone=True), nullable=True)

    # Identifiers
    trade_id = Column(String, index=True, nullable=True, comment="Links related events (e.g., entry signal to fill to exit)")
    order_id = Column(String, index=True, nullable=True, comment="Exchange Order ID")
    client_order_id = Column(String, index=True, nullable=True, comment="Client-generated Order ID")

    # Strategy & Market Info
    strategy_name = Column(String, index=True, nullable=True)
    symbol = Column(String, index=True, nullable=False)

    # Event Details
    event_type = Column(SQLEnum(EventType), nullable=False, index=True)
    status = Column(SQLEnum(OrderStatus), nullable=True, index=True, comment="Specific status, e.g., for orders")
    side = Column(SQLEnum(TradeSide), nullable=True, comment="BUY or SELL for trades")

    # Quantitative Info
    quantity = Column(Float, nullable=True)
    price = Column(Float, nullable=True)
    fees = Column(Float, nullable=True)
    slippage = Column(Float, nullable=True, comment="Difference between signal price and fill price")
    pnl = Column(Float, nullable=True, comment="Realized PnL for closing trades")

    # Additional Context
    notes = Column(Text, nullable=True)

    def __repr__(self):
        return f"<TradeLog(id={self.id}, ts='{self.timestamp}', event='{self.event_type}', symbol='{self.symbol}', status='{self.status}')>"

# You can add more models here later, e.g., for Positions, PerformanceSnapshots, etc. 