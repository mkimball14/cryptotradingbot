# Coinbase Advanced Trade API Integration

This readme explains how to use the Coinbase Advanced Trade API in this project, covering both the REST API for historical data and the WebSocket API for real-time data.

## Overview

Coinbase Advanced Trade API provides two main ways to interact with the exchange:

1. **REST API** - Used for historical data, account management, and order placement/management
2. **WebSocket API** - Used for real-time market data including ticker updates, order book changes, and trade execution notifications

## Setup and Authentication

Both APIs use JWT (JSON Web Token) authentication. You need to:

1. Create a Coinbase Developer Platform (CDP) API key from your Coinbase account
2. Set up the JWT credentials in your `.env` file:

```
COINBASE_JWT_KEY_NAME=organizations/{org_id}/apiKeys/{key_id}
COINBASE_JWT_PRIVATE_KEY=-----BEGIN EC PRIVATE KEY-----\n...\n-----END EC PRIVATE KEY-----
```

> **Note**: As of June 10, 2024, Coinbase is removing legacy API keys. This implementation uses the CDP Keys with JWT authentication.

## REST API Usage

The REST API client (`CoinbaseClient`) handles authentication, request signing, and endpoint access:

```python
from app.core.config import get_settings
from app.core.coinbase import CoinbaseClient

# Initialize the client
settings = get_settings()
client = CoinbaseClient(settings)

# Example: Get historical candle data
async def get_historical_data():
    product_id = "BTC-USD"
    start_time = "2023-01-01T00:00:00Z"
    end_time = "2023-01-10T00:00:00Z"
    
    candles = await client.get_product_candles(
        product_id=product_id,
        start=start_time,
        end=end_time,
        granularity="ONE_HOUR"
    )
    
    return candles
```

### Available REST Endpoints

- **Account Endpoints**
  - `get_accounts()` - Get list of trading accounts
  - `get_account(account_id)` - Get specific account details

- **Product Endpoints**
  - `get_products()` - Get list of available products
  - `get_product(product_id)` - Get product details
  - `get_product_candles(product_id, start, end, granularity)` - Get historical candles

- **Order Endpoints**
  - `create_order(product_id, side, order_type, size, price, ...)` - Create a new order
  - `cancel_order(order_id)` - Cancel an order
  - `get_orders(product_id, status, limit)` - Get list of orders
  - `get_order(order_id)` - Get order details

- **Market Data Endpoints**
  - `get_market_trades(product_id, limit)` - Get recent trades
  - `get_order_book(product_id, level)` - Get order book

## WebSocket API Usage

The WebSocket API client (`CoinbaseWebSocketClient`) provides real-time market data:

```python
from app.core.config import get_settings
from app.core.websocket_client import CoinbaseWebSocketClient
import asyncio

# Define callback functions
async def handle_message(message):
    print(f"Received message: {message}")

async def handle_error(error):
    print(f"Error: {str(error)}")

# Initialize the client with callbacks
settings = get_settings()
ws_client = CoinbaseWebSocketClient(
    settings=settings,
    on_message=handle_message,
    on_error=handle_error
)

# Example: Connect and subscribe to ticker updates
async def get_real_time_data():
    # Connect to WebSocket server
    if await ws_client.connect():
        # Subscribe to ticker channel for BTC-USD
        await ws_client.subscribe("BTC-USD", "ticker")
        
        # Keep connection open for 60 seconds
        await asyncio.sleep(60)
        
        # Unsubscribe and disconnect
        await ws_client.unsubscribe("BTC-USD", "ticker")
        await ws_client.disconnect()
```

### Available WebSocket Channels

- **ticker** - Real-time price updates for specified products
- **level2** - Order book updates showing real-time market depth
- **user** - User account updates including orders and fills (authenticated only)
- **status** - Platform status updates
- **market_trades** - Real-time trade execution data
- **candles** - Candlestick updates (1m, 5m, 15m, 1h, etc.)

## Full Example

See `app/examples/coinbase_api_example.py` for a complete example that:

1. Loads historical data using the REST API
2. Connects to real-time WebSocket feed
3. Combines and plots both historical and real-time data

## Common Usage Patterns

### Backtesting with Historical Data

```python
# Load historical data for backtesting
candles = await client.get_product_candles(
    product_id="BTC-USD",
    start="2023-01-01T00:00:00Z",
    end="2023-12-31T23:59:59Z",
    granularity="ONE_DAY"
)

# Process candles for backtesting
# ...
```

### Live Trading with Real-time Data

```python
# Process real-time updates
async def handle_ticker(message):
    if message.get("type") == "ticker":
        price = float(message.get("price", 0))
        product_id = message.get("product_id")
        print(f"Latest price for {product_id}: ${price:.2f}")
        
        # Implement trading logic
        # ...

# Connect and subscribe
ws_client = CoinbaseWebSocketClient(
    settings=settings,
    on_message=handle_ticker
)

await ws_client.connect()
await ws_client.subscribe(["BTC-USD", "ETH-USD"], "ticker")
```

## Error Handling and Reconnection

The WebSocket client includes automatic reconnection logic with exponential backoff. You can customize the behavior:

```python
ws_client = CoinbaseWebSocketClient(
    settings=settings,
    on_message=handle_message,
    auto_reconnect=True,  # Enable automatic reconnection
    max_reconnect_attempts=10,  # Maximum reconnection attempts
    reconnect_delay=5  # Initial delay in seconds (will increase with each attempt)
)
```

## API Rate Limits

- REST API: Rate limits vary by endpoint, generally 10-100 requests per second
- WebSocket API: No strict message limits, but best practices:
  - Subscribe to only the channels you need
  - Process messages efficiently
  - Implement proper error handling and reconnection logic

---

For more information, see the [Coinbase Advanced Trade API Documentation](https://docs.cloud.coinbase.com/advanced-trade/docs/welcome). 