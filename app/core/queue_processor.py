import asyncio
import logging
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.trade_log.crud import create_log_entry
from app.core.trade_log.models import EventType, TradeSide, OrderStatus

logger = logging.getLogger(__name__)

async def process_message_queue(
    queue: asyncio.Queue,
    session_factory: sessionmaker
):
    """Continuously processes messages from the WebSocket queue."""
    logger.info("Starting WebSocket message queue processor...")
    while True:
        try:
            message = await queue.get()
            if message is None: # Add a way to signal shutdown
                logger.info("Received shutdown signal. Exiting queue processor.")
                break
                
            logger.debug(f"Queue Processor received: {message}")
            
            # --- Log Order Fills --- 
            if isinstance(message, dict) and message.get('type') == 'user_order_update' and message.get('status') == 'FILLED':
                logger.info(f"Processing FILL message for order {message.get('order_id')}")
                try:
                    async with session_factory() as db: # Create session for this log entry
                        side_str = message.get('side', '').upper()
                        event_type = EventType.ENTRY_FILL if side_str == 'BUY' else EventType.EXIT_FILL if side_str == 'SELL' else EventType.ORDER_UPDATE
                        
                        # Convert side string to Enum for logging
                        try:
                            side_enum = TradeSide(side_str) if side_str else None
                        except ValueError:
                            side_enum = None 
                            logger.warning(f"Invalid side '{message.get('side')}' received in fill message.")
                            
                        await create_log_entry(
                            db=db,
                            event_type=event_type,
                            symbol=message.get('product_id'),
                            status=OrderStatus.FILLED, 
                            order_id=message.get('order_id'), 
                            client_order_id=message.get('client_order_id'),
                            side=side_enum,
                            quantity=float(message.get('cumulative_quantity', 0)),
                            price=float(message.get('average_filled_price', 0)), 
                            fees=float(message.get('total_fees', 0)), 
                            # strategy_name= ? # Still needs association logic
                            event_timestamp=pd.to_datetime(message.get('time')), 
                            notes=f"Order filled via WebSocket update."
                        )
                        logger.info(f"Logged FILL event for order {message.get('order_id')}")
                except Exception as log_err:
                    logger.error(f"Error logging fill event: {log_err}", exc_info=True)
            # --- End Log Order Fills --- 
            # TODO: Add handlers for other message types if needed
            else:
                logger.debug(f"Skipping message processing for type: {message.get('type')}")

            queue.task_done() # Indicate message processing is complete

        except asyncio.CancelledError:
            logger.info("Queue processor task cancelled.")
            break
        except Exception as e:
            logger.error(f"Error in queue processor: {e}", exc_info=True)
            # Avoid tight loop on continuous error
            await asyncio.sleep(1) 