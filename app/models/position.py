from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

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