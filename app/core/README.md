# Order Execution System

This module provides a robust order execution system for cryptocurrency trading, with support for various order types including bracket orders.

## Bracket Orders

A bracket order is a set of three orders that bracket a trading position:
1. Entry order (market or limit)
2. Stop loss order to limit downside risk
3. Take profit order to secure gains

### Usage

```python
from app.core.order_executor import OrderExecutor
from app.core.coinbase import CoinbaseClient, OrderSide, OrderType

# Initialize
client = CoinbaseClient(api_key="your_key", api_secret="your_secret")
executor = OrderExecutor(client)

# Market Entry Bracket Order
result = await executor.execute_bracket_order(
    product_id="BTC-USD",
    side=OrderSide.BUY,
    size=0.1,
    stop_loss_price=45000.0,
    take_profit_price=55000.0
)

# Limit Entry Bracket Order
result = await executor.execute_bracket_order(
    product_id="BTC-USD",
    side=OrderSide.BUY,
    size=0.1,
    entry_price=50000.0,
    stop_loss_price=45000.0,
    take_profit_price=55000.0,
    entry_type=OrderType.LIMIT
)

# Check result
if result.success:
    print(f"Entry Order ID: {result.entry_order.order_id}")
    print(f"Stop Loss Order ID: {result.stop_loss_order.order_id}")
    print(f"Take Profit Order ID: {result.take_profit_order.order_id}")
else:
    print(f"Error: {result.error}")
```

### Features

1. **Order Types**
   - Market entry with stop loss and take profit
   - Limit entry with stop loss and take profit
   - Customizable time in force settings

2. **Validation**
   - Price validation for long/short positions
   - Account balance validation
   - Order size validation
   - Price level validation

3. **Monitoring**
   - Automatic monitoring of bracket orders
   - Cancellation of remaining orders when one is filled
   - Error handling and recovery

4. **Error Handling**
   - Validation errors with descriptive messages
   - API error handling
   - Partial fill handling
   - Order status monitoring

### Error Recovery

The system includes automatic error recovery mechanisms:

1. **Entry Order Cancellation**
   - If the entry order is cancelled, all related orders are automatically cancelled

2. **Exit Order Fills**
   - When either stop loss or take profit order is filled, the other is automatically cancelled

3. **Error States**
   - If an error occurs during monitoring, the system attempts to cancel all related orders
   - All errors are logged for debugging

### Best Practices

1. **Position Sizing**
   - Always validate position size against account balance
   - Consider fees in calculations
   - Use appropriate precision for the trading pair

2. **Price Levels**
   - Set reasonable stop loss and take profit levels
   - Consider market volatility when setting prices
   - Use current market price as reference for validation

3. **Monitoring**
   - Monitor order status changes
   - Handle partial fills appropriately
   - Implement proper error recovery

### Testing

The system includes both unit tests and integration tests:

1. **Unit Tests**
   ```bash
   pytest app/tests/test_order_executor.py -v
   ```

2. **Integration Tests**
   ```bash
   # Set environment variables first
   export COINBASE_API_KEY="your_key"
   export COINBASE_API_SECRET="your_secret"
   
   # Run integration tests
   pytest app/tests/test_order_executor.py -v -m integration
   ```

### Error Messages

Common error messages and their meanings:

1. **Validation Errors**
   - "Invalid order side" - Side must be BUY or SELL
   - "Invalid order size" - Size must be positive
   - "Invalid price" - Price must be positive
   - "Insufficient funds" - Account balance too low

2. **Price Level Errors**
   - "Stop loss must be below entry price for long positions"
   - "Take profit must be above entry price for long positions"
   - "Stop loss must be above entry price for short positions"
   - "Take profit must be below entry price for short positions"

3. **API Errors**
   - "Coinbase API error" - Error from Coinbase API
   - "Order execution error" - General execution error

### Monitoring Output

The system logs important events during order monitoring:

```
INFO: Entry order filled for bracket order <order_id>
INFO: Stop loss triggered for bracket order <order_id>
INFO: Take profit triggered for bracket order <order_id>
INFO: Both exit orders cancelled for bracket order <order_id>
ERROR: Error monitoring bracket order <order_id>: <error_message>
``` 