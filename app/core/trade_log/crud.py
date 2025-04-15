from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import TradeLog, EventType, OrderStatus, TradeSide
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def create_log_entry(
    db: AsyncSession,
    event_type: EventType,
    symbol: str,
    timestamp: datetime = None, # Timestamp of log creation
    event_timestamp: datetime = None, # Timestamp of the actual event
    trade_id: str = None,
    order_id: str = None,
    client_order_id: str = None,
    strategy_name: str = None,
    status: OrderStatus = None,
    side: TradeSide = None,
    quantity: float = None,
    price: float = None,
    fees: float = None,
    slippage: float = None,
    pnl: float = None,
    notes: str = None
) -> TradeLog:
    """Creates a new log entry in the database."""
    try:
        # Use event_timestamp if provided, otherwise default to None (DB default will be log creation time)
        db_log = TradeLog(
            event_type=event_type,
            symbol=symbol,
            timestamp=timestamp, # Let DB handle default if None
            event_timestamp=event_timestamp,
            trade_id=trade_id,
            order_id=order_id,
            client_order_id=client_order_id,
            strategy_name=strategy_name,
            status=status,
            side=side,
            quantity=quantity,
            price=price,
            fees=fees,
            slippage=slippage,
            pnl=pnl,
            notes=notes
        )
        db.add(db_log)
        await db.commit()
        await db.refresh(db_log)
        logger.debug(f"Created log entry: {db_log}")
        return db_log
    except Exception as e:
        await db.rollback() # Rollback in case of error
        logger.error(f"Error creating log entry: {e}", exc_info=True)
        raise # Re-raise the exception after logging

# --- Add other CRUD operations as needed --- #

# Example: Get logs by trade_id
async def get_logs_by_trade_id(db: AsyncSession, trade_id: str) -> list[TradeLog]:
    result = await db.execute(select(TradeLog).where(TradeLog.trade_id == trade_id).order_by(TradeLog.timestamp))
    return result.scalars().all()

# Example: Get logs by event type
async def get_logs_by_event_type(db: AsyncSession, event_type: EventType, limit: int = 100) -> list[TradeLog]:
    result = await db.execute(
        select(TradeLog)
        .where(TradeLog.event_type == event_type)
        .order_by(TradeLog.timestamp.desc())
        .limit(limit)
    )
    return result.scalars().all() 