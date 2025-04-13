import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SimpleStrategy:
    """A basic placeholder strategy that just logs incoming data."""

    def __init__(self, product_id: str, config: Optional[Dict] = None):
        """
        Initialize the strategy.

        Args:
            product_id (str): The product ID this strategy instance is for.
            config (Optional[Dict]): Strategy-specific configuration.
        """
        self.product_id = product_id
        self.config = config or {}
        logger.info(f"Initialized SimpleStrategy for {self.product_id}")

    def process_market_data(self, data: Dict[str, Any]) -> Optional[Dict]:
        """
        Processes incoming market data (e.g., ticker update).

        Args:
            data (Dict[str, Any]): The market data message (e.g., from the queue).

        Returns:
            Optional[Dict]: An action dictionary (e.g., {'action': 'BUY', ...}) or None.
        """
        
        message_type = data.get('type')
        
        if message_type == 'ticker':
            price = data.get('price')
            time = data.get('time')
            logger.info(f"Strategy [{self.product_id}]: Received ticker price {price} at {time}")
            # --- Add actual strategy logic here --- 
            # Example: if float(price) < some_threshold: return {'action': 'BUY', ...}
            # -----------------------------------------
        else:
            logger.debug(f"Strategy [{self.product_id}]: Received unhandled message type '{message_type}'")

        # No action by default
        return None 