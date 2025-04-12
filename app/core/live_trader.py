import asyncio
import logging
import pandas as pd
from collections import deque
from typing import Optional, Dict, List

from app.core.config import Settings, get_settings
from app.models.order import OrderSide, OrderType
from app.core.coinbase import CoinbaseClient, CoinbaseError
from app.core.websocket_client import CoinbaseWebSocketClient
from app.strategies.rsi_momentum import RSIMomentumStrategy

logger = logging.getLogger(__name__)

class LiveTrader:
    """
    Handles live trading based on real-time data and strategy signals.
    """
    def __init__(self, settings: Settings, rest_client: CoinbaseClient, ws_client: CoinbaseWebSocketClient):
        self.settings = settings
        self.rest_client = rest_client
        self.ws_client = ws_client
        self.product_id = "BTC-USD"  # Default, can be changed
        
        # Initialize strategy with default parameters from RSIMomentumStrategy
        self.strategy = RSIMomentumStrategy(
            # Use the default values defined in RSIMomentumStrategy
            # timeframe='1h',  # Timeframe is not directly used in live ticker processing
            # rsi_period=14,
            # rsi_entry_threshold=60.0,
            # rsi_exit_threshold=40.0,
            # ma_period=20,
            # atr_period=14,
            # risk_per_trade=self.settings.RISK_PERCENTAGE / 100, # Use setting
            # atr_stop_multiplier=2.0
        )
        
        # Determine buffer size needed for the strategy's indicators
        # Needs at least MA period + ATR period for regime, or RSI period
        required_buffer_size = max(self.strategy.ma_period + self.strategy.atr_period, self.strategy.rsi_period) * 2
        self.data_buffer = deque(maxlen=required_buffer_size)  # Buffer for OHLCV data
        
        self.current_position = 0  # 0: Flat, 1: Long (Strategy is long-only)
        # self.last_signal = 0 # Strategy state handles this implicitly now

        # Link WebSocket message handler
        self.ws_client.on_message = self._handle_websocket_message
        self.ws_client.on_error = self._handle_websocket_error
        self.ws_client.on_connect = self._handle_websocket_connect
        self.ws_client.on_disconnect = self._handle_websocket_disconnect

    async def _handle_websocket_message(self, message: Dict):
        """Callback for processing incoming WebSocket messages."""
        msg_type = message.get("type")
        if msg_type == "ticker" and message.get("product_id") == self.product_id:
            try:
                # Create OHLCV-like data point from ticker
                price = float(message.get("price"))
                # Note: Live ticker doesn't provide true OHLCV, use price for all
                # Volume might be useful but is 24h volume, not interval volume
                volume = float(message.get("volume_24h", 0))
                timestamp = pd.Timestamp.now(tz='UTC')
                
                # Append new data point
                self.data_buffer.append({
                    'timestamp': timestamp,
                    'open': price,
                    'high': price,
                    'low': price,
                    'close': price,
                    'volume': volume # Using 24h volume, might not be ideal for indicators
                })
                
                logger.debug(f"Buffer size: {len(self.data_buffer)}, Price: {price:.2f}")

                # Only run strategy if we have enough data for all indicators
                if len(self.data_buffer) >= self.strategy.ma_period + self.strategy.atr_period: # Ensure enough data for longest indicator dependency (regime)
                    await self._run_live_strategy()

            except (TypeError, ValueError) as e:
                logger.error(f"Error processing ticker message: {e} - Message: {message}")
        elif msg_type == "error":
            logger.error(f"Received WebSocket error message: {message.get('message')}")
        elif msg_type == "subscriptions":
            logger.info(f"Subscription update: {message}")
        else:
            logger.debug(f"Received other message type: {msg_type}")

    async def _handle_websocket_error(self, error: Exception):
        """Callback for WebSocket errors."""
        logger.error(f"LiveTrader WebSocket error: {error}")
        # Add custom error handling/notification logic here if needed

    async def _handle_websocket_connect(self):
        """Callback for successful WebSocket connection."""
        logger.info("LiveTrader WebSocket connected. Preparing to subscribe...")
        try:
            # Subscribe automatically on connection
            await self.ws_client.subscribe(self.product_id, "ticker") # Subscribe to ticker channel
            logger.info(f"Subscription request sent for {self.product_id} on 'ticker' channel.")
        except Exception as e:
            logger.error(f"Error during automatic subscription: {e}")

    async def _handle_websocket_disconnect(self):
        """Callback for WebSocket disconnection."""
        logger.warning("LiveTrader WebSocket disconnected.")
        # Reconnection is handled by the ws_client itself if auto_reconnect=True

    async def _run_live_strategy(self):
        """Runs the RSI Momentum strategy on the current data buffer."""
        try:
            # Convert deque to DataFrame
            df = pd.DataFrame(list(self.data_buffer))
            df.set_index('timestamp', inplace=True)

            # Generate signals using the strategy instance
            signals_df = self.strategy.generate_signals(df)
            latest_row = signals_df.iloc[-1]

            logger.info(f"Strategy Check: RSI={latest_row.get('rsi', float('nan')):.2f}, Regime={latest_row.get('regime', 'N/A')}, Signal={latest_row.get('signal', 0)}, Pos={self.strategy.state.is_in_position}")

            # Use strategy methods to determine entry/exit
            if self.strategy.should_enter_trade(latest_row):
                logger.info("BUY SIGNAL DETECTED by strategy")
                await self._execute_trade(OrderSide.BUY, latest_row)
                # Update strategy state after trade attempt
                # Position size/entry price are unknown until order fills, update basic state
                self.strategy.update_state(latest_row.name, True, 0, None, latest_row.get('regime')) 
            elif self.strategy.should_exit_trade(latest_row):
                logger.info("SELL SIGNAL DETECTED by strategy")
                await self._execute_trade(OrderSide.SELL, latest_row)
                # Update strategy state after trade attempt
                self.strategy.update_state(latest_row.name, False, 0, None, latest_row.get('regime'))

        except Exception as e:
            logger.error(f"Error running live strategy: {e}", exc_info=True)

    async def _execute_trade(self, side: OrderSide, strategy_row: pd.Series):
        """Executes a trade based on the signal."""
        if not self.settings.TRADING_ENABLED:
            logger.warning(f"TRADING DISABLED: Would place {side.value} order for {self.product_id}")
            return

        logger.info(f"Attempting to place {side.value} MARKET order for {self.product_id}")
        try:
            # Use strategy's risk management to calculate size
            # Note: Requires account balance and current price
            accounts = await self.rest_client.get_accounts()
            usd_account = next((acc for acc in accounts if acc.get('currency') == 'USD'), None)
            
            if not usd_account or 'available_balance' not in usd_account:
                logger.error("Could not find USD account or available balance.")
                return
                
            available_balance = float(usd_account['available_balance'])
            
            # Get current price (more accurately from latest ticker?)
            # Using strategy_row['close'] which is the latest price from the buffer
            current_price = strategy_row['close']
            
            if current_price <= 0:
                logger.error(f"Invalid current price for trade calculation: {current_price}")
                return

            # Calculate position size using strategy's method
            stop_loss_price = self.strategy.calculate_stop_loss(strategy_row)
            position_size = self.strategy.calculate_position_size(
                account_balance=available_balance,
                entry_price=current_price,
                stop_loss_price=stop_loss_price
            )

            if position_size <= 0:
                logger.warning(f"Calculated position size is zero or negative ({position_size}). Skipping trade.")
                return
            
            # Coinbase API requires size as string
            order_size_str = f"{position_size:.8f}" 
            
            # Check minimum order size (e.g., $1 USD for Coinbase)
            notional_value = position_size * current_price
            if notional_value < 1.0:
                logger.warning(f"Order notional value ${notional_value:.2f} is below minimum threshold ($1.00). Skipping trade.")
                return

            logger.info(f"Calculated trade details: Balance={available_balance:.2f}, Price={current_price:.2f}, SL={stop_loss_price:.2f}, Size={order_size_str}")

            # Place the order
            order = await self.rest_client.create_order(
                product_id=self.product_id,
                side=side, # Pass the enum directly
                order_type=OrderType.MARKET,
                size=order_size_str # Pass size as string
            )
            logger.info(f"Successfully placed {side.value} order: {order}")
            # TODO: Need to monitor order status and update strategy state accurately on fill

        except CoinbaseError as e:
             logger.error(f"Coinbase API error placing {side.value} order: {e.status_code} - {e.message} - {e.response}")
        except Exception as e:
            logger.error(f"Failed to place {side.value} order for {self.product_id}: {e}", exc_info=True)

    async def start(self, product_id: str = "BTC-USD"):
        """Starts the live trading bot."""
        self.product_id = product_id
        logger.info(f"Starting Live Trader for {self.product_id}...")
        logger.info(f"Trading Enabled: {self.settings.TRADING_ENABLED}")
        logger.info(f"Risk Per Trade: {self.strategy.risk_per_trade * 100}%")
        logger.info(f"Strategy Parameters: RSI Period={self.strategy.rsi_period}, Entry={self.strategy.rsi_entry_threshold}, Exit={self.strategy.rsi_exit_threshold}, MA={self.strategy.ma_period}, ATR={self.strategy.atr_period}")

        # Ensure ws_client has correct callbacks assigned (in case re-initialized)
        self.ws_client.on_message = self._handle_websocket_message
        self.ws_client.on_error = self._handle_websocket_error
        self.ws_client.on_connect = self._handle_websocket_connect
        self.ws_client.on_disconnect = self._handle_websocket_disconnect
        
        if not await self.ws_client.connect():
            logger.error("Failed to connect WebSocket. Live Trader cannot start.")
            return

        try:
            while True:
                await asyncio.sleep(60)  # Keep alive loop
                if not self.ws_client.is_connected:
                    logger.warning("WebSocket appears disconnected. Reconnect should be handled by ws_client.")
        except asyncio.CancelledError:
            logger.info("Live Trader task cancelled.")
        except KeyboardInterrupt:
            logger.info("Live Trader stopped by user.")
        finally:
            logger.info("Shutting down Live Trader...")
            await self.ws_client.disconnect()

    async def stop(self):
        """Stops the live trading bot."""
        logger.info("Stopping Live Trader...")
        await self.ws_client.disconnect() 