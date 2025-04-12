import pytest
from decimal import Decimal
from app.core.dry_run_executor import DryRunExecutor
from app.models.order import OrderSide, OrderType, OrderStatus, TimeInForce
from app.models.position import Position

# ... existing code ... 