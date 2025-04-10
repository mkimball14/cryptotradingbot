import logging
from typing import Dict, List, Optional
from collections import deque
import numpy as np
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class TradingStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50):
        """
        Initialize the trading strategy.
        
        Args:
            short_window: Number of periods for short moving average
            long_window: Number of periods for long moving average
        """
        self.short_window = short_window
        self.long_window = long_window
        
        # Price history for each product
        self.price_history: Dict[str, deque] = {}
        
        # Moving averages for each product
        self.short_ma: Dict[str, Optional[float]] = {}
        self.long_ma: Dict[str, Optional[float]] = {}
        
        # Current positions for each product
        self.positions: Dict[str, str] = {}  # 'long', 'short', or None
        
        logger.info(f"Initialized trading strategy with SMA{short_window}/{long_window}")

    def initialize_product(self, product_id: str) -> None:
        """Initialize data structures for a new product."""
        self.price_history[product_id] = deque(maxlen=self.long_window)
        self.short_ma[product_id] = None
        self.long_ma[product_id] = None
        self.positions[product_id] = None
        logger.info(f"Initialized tracking for {product_id}")

    def calculate_moving_averages(self, product_id: str) -> None:
        """Calculate short and long moving averages for a product."""
        if len(self.price_history[product_id]) >= self.long_window:
            prices = list(self.price_history[product_id])
            self.short_ma[product_id] = np.mean(prices[-self.short_window:])
            self.long_ma[product_id] = np.mean(prices)
            logger.debug(f"{product_id} - Short MA: {self.short_ma[product_id]:.2f}, Long MA: {self.long_ma[product_id]:.2f}")

    def analyze_ticker(self, ticker_data: Dict) -> Optional[Dict]:
        """
        Analyze new ticker data and generate trading signals.
        
        Args:
            ticker_data: Ticker data from WebSocket
        
        Returns:
            Dict with trading signal if generated, None otherwise
        """
        try:
            # Extract relevant data
            product_id = ticker_data.get("product_id")
            price = float(ticker_data.get("price", 0))
            # Use current time if timestamp not available
            timestamp = datetime.now()
            
            # Additional logging for debugging
            logger.debug(f"Analyzing ticker: {json.dumps(ticker_data)}")
            
            # Skip processing if missing essential data
            if not product_id or price == 0:
                logger.warning(f"Skipping ticker with missing data: {ticker_data}")
                return None
            
            # Initialize product if not seen before
            if product_id not in self.price_history:
                self.initialize_product(product_id)
            
            # Add price to history
            self.price_history[product_id].append(price)
            
            # Only generate signals once we have enough data
            if len(self.price_history[product_id]) < self.long_window:
                return None
            
            # Calculate moving averages
            self.calculate_moving_averages(product_id)
            
            # Generate trading signals
            signal = self.generate_signal(product_id)
            if signal:
                signal["timestamp"] = timestamp
                logger.info(f"Generated signal for {product_id}: {signal}")
                return signal
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing ticker data: {str(e)}")
            return None

    def generate_signal(self, product_id: str) -> Optional[Dict]:
        """
        Generate trading signal based on moving average crossover.
        
        Returns:
            Dict with signal details if a signal is generated, None otherwise
        """
        if not (self.short_ma[product_id] and self.long_ma[product_id]):
            return None
            
        current_price = self.price_history[product_id][-1]
        
        # Check for crossover
        if self.short_ma[product_id] > self.long_ma[product_id]:
            # Golden cross - buy signal
            if self.positions[product_id] != "long":
                self.positions[product_id] = "long"
                return {
                    "product_id": product_id,
                    "signal": "buy",
                    "price": current_price,
                    "reason": "Golden cross - short MA crossed above long MA",
                    "short_ma": self.short_ma[product_id],
                    "long_ma": self.long_ma[product_id]
                }
        else:
            # Death cross - sell signal
            if self.positions[product_id] != "short":
                self.positions[product_id] = "short"
                return {
                    "product_id": product_id,
                    "signal": "sell",
                    "price": current_price,
                    "reason": "Death cross - short MA crossed below long MA",
                    "short_ma": self.short_ma[product_id],
                    "long_ma": self.long_ma[product_id]
                }
        
        return None 