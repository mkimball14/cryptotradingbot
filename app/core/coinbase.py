import time
import json
import logging
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta, timezone
from coinbase.rest import RESTClient
from app.core.config import Settings

# Import consolidated models and enums
from app.models.order import OrderSide, OrderType, OrderStatus, TimeInForce, OrderBase, MarketOrder, LimitOrder # Assuming these cover needed Order details
from app.models.position import Position

# Get logger
logger = logging.getLogger(__name__)

class CoinbaseClient:
    def __init__(self, settings: Settings):
        """
        Initialize Coinbase API client with settings
        
        Args:
            settings (Settings): Application settings containing API credentials
        """
        self.settings = settings
        self.key_name = settings.COINBASE_JWT_KEY_NAME
        self.private_key_pem = settings.COINBASE_JWT_PRIVATE_KEY

        # Initialize the EnhancedRESTClient
        try:
            self.client = RESTClient(
                api_key=self.key_name,
                api_secret=self.private_key_pem
            )
            logger.info("Coinbase RESTClient initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Coinbase RESTClient: {e}", exc_info=True)
            raise

    # Account endpoints
    async def get_accounts(self) -> List[Dict]:
        """Get list of trading accounts"""
        # SDK Method: get_accounts()
        try:
            # Await underlying call
            response_obj = await self.client.get_accounts()
            # Return the raw response object (e.g., ListAccountsResponse)
            # Caller can access response_obj.accounts and convert if needed
            return response_obj
        except Exception as e:
            logger.error(f"Coinbase API error getting accounts: {e}", exc_info=True)
            raise # Re-raise the exception
        
    def get_account(self, account_id: str) -> Dict:
        """Get specific account details"""
        # SDK Method: get_account(account_uuid=...)
        try:
            response_obj = self.client.get_account(account_uuid=account_id)
            # Return the raw response object (e.g., Account)
            return response_obj
        except Exception as e:
            logger.error(f"Coinbase API error getting account {account_id}: {e}", exc_info=True)
            raise
        
    # Product endpoints
    def get_products(self) -> List[Dict]:
        """Get list of available products"""
        # SDK Method: get_products()
        try:
            response_obj = self.client.get_products() # Method confirmed by README
            # Return the raw response object (e.g., ListProductsResponse)
            return response_obj
        except Exception as e:
            logger.error(f"Coinbase API error getting products: {e}", exc_info=True)
            raise # Or return []
        
    def get_product(self, product_id: str) -> Dict:
        """Get product details by ID"""
        # SDK Method: get_product(product_id=...)
        try:
            response_obj = self.client.get_product(product_id=product_id) # Method confirmed by README
            # Return the raw response object (e.g., Product)
            return response_obj
        except Exception as e:
            logger.error(f"Coinbase API error getting product {product_id}: {e}", exc_info=True)
            raise
        
    def get_product_candles(
        self,
        product_id: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
        granularity: str = "ONE_HOUR"
    ) -> List[Dict]:
        """Get historical candles for a product (uses public endpoint)"""
        params = {
            "granularity": granularity
        }
        
        if start:
            params["start"] = start
        if end:
            params["end"] = end
            
        # SDK method confirmed via error message: get_public_candles
        try:
            # Note: Using public endpoint as suggested by error, might not require auth
            response_obj = self.client.get_public_candles(product_id=product_id, **params)
            # Return raw response object
            return response_obj
        except Exception as e:
            logger.error(f"Coinbase API error getting candles for {product_id}: {e}", exc_info=True)
            raise # Or return []
        
    # Order endpoints
    async def create_order(
        self,
        product_id: str,
        side: OrderSide,
        order_type: OrderType,
        size: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        client_order_id: Optional[str] = None,
        time_in_force: TimeInForce = TimeInForce.GTC
    ) -> Dict:
        """
        Create a new order. Routes to specific SDK methods based on order_type and side.
        
        Args:
            product_id (str): Trading pair ID
            side (OrderSide): Order side (BUY/SELL)
            order_type (OrderType): Order type (MARKET/LIMIT/STOP/STOP_LIMIT)
            size (float): Order size in base currency
            price (Optional[float]): Limit price (required for LIMIT orders)
            stop_price (Optional[float]): Stop price (required for STOP/STOP_LIMIT orders)
            client_order_id (Optional[str]): Client-specified order ID
            time_in_force (TimeInForce): Time in force policy (GTC/GTT/IOC/FOK)
            
        Returns:
            Dict: Dictionary representation of the order creation response, or an error dict.
        """
        # Use provided client_order_id or let the SDK generate one if None (pass empty string)
        effective_client_order_id = client_order_id or ""
        
        # Convert size and price to string as often required by API
        size_str = str(size)
        price_str = str(price) if price is not None else None
        stop_price_str = str(stop_price) if stop_price is not None else None
        
        response_obj = None
        
        # Adjust logging to handle side as string and time_in_force/order_type potentially being string or enum
        tif_log_value = time_in_force.value if hasattr(time_in_force, 'value') else time_in_force
        order_type_log_value = order_type.value if hasattr(order_type, 'value') else order_type
        logger.info(f"Attempting to create order: {product_id} {side} {order_type_log_value} {size_str} Price={price_str} Stop={stop_price_str} TIF={tif_log_value}")

        try:
            if order_type == OrderType.MARKET:
                if side == OrderSide.BUY:
                    # Market BUY typically uses quote_size (amount of quote currency)
                    logger.info(f"Executing market_order_buy for {product_id}, quote_size={size_str}")
                    # Await the underlying client call
                    response_obj = await self.client.market_order_buy(client_order_id=effective_client_order_id, product_id=product_id, quote_size=size_str)
                elif side == OrderSide.SELL:
                    # Market SELL typically uses base_size (amount of base currency)
                    logger.info(f"Executing market_order_sell for {product_id}, base_size={size_str}")
                     # Await the underlying client call
                    response_obj = await self.client.market_order_sell(client_order_id=effective_client_order_id, product_id=product_id, base_size=size_str)
            
            elif order_type == OrderType.LIMIT:
                if price is None:
                    raise ValueError("Price must be provided for LIMIT orders.")
                # Handle different TimeInForce values
                if time_in_force == TimeInForce.GTC:
                    # Limit orders use base_size (amount of base currency, e.g., BTC)
                    # Verify SDK method names: limit_order_gtc_buy / limit_order_gtc_sell
                    if side == OrderSide.BUY:
                        logger.info(f"Calling SDK: limit_order_gtc_buy(product_id={product_id}, base_size={size_str}, limit_price={price_str})")
                        # Await the underlying client call
                        response_obj = await self.client.limit_order_gtc_buy(client_order_id=effective_client_order_id, product_id=product_id, base_size=size_str, limit_price=price_str)
                    elif side == OrderSide.SELL:
                        logger.info(f"Calling SDK: limit_order_gtc_sell(product_id={product_id}, base_size={size_str}, limit_price={price_str})")
                         # Await the underlying client call
                        response_obj = await self.client.limit_order_gtc_sell(client_order_id=effective_client_order_id, product_id=product_id, base_size=size_str, limit_price=price_str)
                elif time_in_force == TimeInForce.GTD: # Good Till Date/Time
                     # Requires end_time parameter - not currently supported by this wrapper
                    raise NotImplementedError("LIMIT GTD orders require end_time, which is not supported by this wrapper.")
                # TODO: Add support for IOC/FOK if available in SDK (might be boolean flags like post_only?)
                else:
                    raise NotImplementedError(f"TimeInForce {time_in_force} not implemented for LIMIT orders.")
            
            elif order_type == OrderType.STOP_LIMIT:
                 if price is None or stop_price is None:
                     raise ValueError("Both price (limit) and stop_price must be provided for STOP_LIMIT orders.")
                 # Assuming stop_direction is inferred or not needed for basic STOP_LIMIT
                 if time_in_force == TimeInForce.GTC:
                     # Stop Limit orders use base_size (amount of base currency, e.g., BTC)
                     # Verify SDK method names: stop_limit_order_gtc_buy / stop_limit_order_gtc_sell
                     if side == OrderSide.BUY:
                         logger.info(f"Calling SDK: stop_limit_order_gtc_buy(product_id={product_id}, base_size={size_str}, limit_price={price_str}, stop_price={stop_price_str})")
                          # Await the underlying client call
                         response_obj = await self.client.stop_limit_order_gtc_buy(client_order_id=effective_client_order_id, product_id=product_id, base_size=size_str, limit_price=price_str, stop_price=stop_price_str)
                     elif side == OrderSide.SELL:
                         logger.info(f"Calling SDK: stop_limit_order_gtc_sell(product_id={product_id}, base_size={size_str}, limit_price={price_str}, stop_price={stop_price_str})")
                          # Await the underlying client call
                         response_obj = await self.client.stop_limit_order_gtc_sell(client_order_id=effective_client_order_id, product_id=product_id, base_size=size_str, limit_price=price_str, stop_price=stop_price_str)
                 elif time_in_force == TimeInForce.GTD:
                      raise NotImplementedError("STOP_LIMIT GTD orders require end_time, which is not supported by this wrapper.")
                 else:
                     raise NotImplementedError(f"TimeInForce {time_in_force} not implemented for STOP_LIMIT orders.")

            # TODO: Add handling for simple STOP orders if the SDK supports them distinct from STOP_LIMIT
            else:
                raise NotImplementedError(f"Order type {order_type} not implemented.")

            # Convert the response object to a dictionary if successful
            return response_obj.to_dict() if response_obj and hasattr(response_obj, 'to_dict') else vars(response_obj) if response_obj else {}

        except NotImplementedError as nie:
            logger.error(f"Order creation failed: {nie}")
            raise # Re-raise unimplemented errors
        except ValueError as ve:
            logger.error(f"Order creation failed due to invalid parameters: {ve}")
            # Consider returning an error dictionary or re-raising
            raise
        except Exception as e: # Catch potential API errors from the SDK
            logger.error(f"Coinbase API error creating order: {e}", exc_info=True)
            raise
        
    def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order by ID"""
        # The SDK uses cancel_orders (plural) and expects a list of IDs
        # Verify SDK method name: Assuming cancel_orders is correct
        try:
            response = self.client.cancel_orders(order_ids=[order_id])
            # Returns CancelOrdersResponse object
            return response # Return raw SDK response object
        except Exception as e:
            logger.error(f"Coinbase API error canceling order {order_id}: {e}", exc_info=True)
            raise
        
    # Make async
    async def get_orders(
        self,
        product_id: Optional[str] = None,
        status: Optional[List[OrderStatus]] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get list of orders
        
        Args:
            product_id (Optional[str]): Filter by product ID
            status (Optional[List[OrderStatus]]): Filter by order status
            limit (int): Maximum number of orders to return
            
        Returns:
            List[Dict]: Raw list of orders from API
        """
        params = {"limit": limit}
        if product_id:
            params["product_id"] = product_id
        if status:
            # Convert list of enums to comma-separated string of values
            # The library might expect a list of strings or handle enums
            params["order_status"] = [s.value for s in status] # Assuming list of strings

        # Verify SDK method name: Assuming list_orders is correct (or get_orders)
        # Note: SDK might use list_orders or get_orders
        try:
            # Await underlying call
            response_obj = await self.client.list_orders(**params)
            orders = getattr(response_obj, 'orders', [])
            return [order.to_dict() for order in orders] if orders else []
        except Exception as e:
            logger.error(f"Coinbase API error getting orders: {e}", exc_info=True)
            raise # Or return []
        
    # Make async
    async def get_order(self, order_id: str) -> Dict:
        """Get order details by ID"""
        # Verify SDK method name: Assuming get_order is correct
        try:
            # Await underlying call
            response_obj = await self.client.get_order(order_id=order_id)
            order = getattr(response_obj, 'order', None)
            return order.to_dict() if order else {}
        except Exception as e:
            logger.error(f"Coinbase API error getting order {order_id}: {e}", exc_info=True)
            raise
        
    # Market data endpoints
    def get_market_trades(
        self,
        product_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """Get recent trades for a product"""
        params = {"limit": limit}
        # Verify SDK method name: Assuming list_market_trades is correct (or get_market_trades)
        try:
            response_obj = self.client.list_market_trades(product_id=product_id, limit=limit)
            trades = getattr(response_obj, 'trades', [])
            return [trade.to_dict() for trade in trades] if trades else []
        except Exception as e:
            logger.error(f"Coinbase API error getting market trades for {product_id}: {e}", exc_info=True)
            raise
        
    def get_order_book(
        self,
        product_id: str,
        level: int = 2
    ) -> Dict:
        """
        Get order book for a product
        
        Args:
            product_id (str): Product ID
            level (int): Order book level (1=best bid/ask, 2=top 50, 3=full)
            
        Returns:
            Dict: Order book data
        """
        # Verify SDK method name: Assuming get_product_book is correct
        # Verify SDK parameter name: Assuming limit maps to level
        try:
            response = self.client.get_product_book(product_id=product_id, limit=level)
            # Convert response object to dict if needed
            return response # Return raw SDK response object
        except Exception as e:
            logger.error(f"Coinbase API error getting order book for {product_id}: {e}", exc_info=True)
            raise
        
    # Removed get_positions and get_position methods as they are likely not 
    # part of the standard RESTClient for trading endpoints.
    # Portfolio/account balance details are typically handled by get_accounts/get_account.
        