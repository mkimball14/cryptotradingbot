from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from typing import List, Optional
import datetime

from app.core.coinbase import CoinbaseClient, CoinbaseError
from app.core.deps import get_coinbase_client
from app.models.responses import (
    ProductsResponse, ProductDetailResponse, CandlesResponse,
    TradesResponse, OrderBookResponse, ErrorResponse
)
from app.core.ohlcv import get_ohlcv

router = APIRouter(prefix="/market", tags=["market"])

@router.get(
    "/products",
    response_model=ProductsResponse,
    responses={
        status.HTTP_200_OK: {"model": ProductsResponse, "description": "Successfully retrieved products"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="List trading products",
    description="Get a list of available trading products"
)
async def get_products(
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> ProductsResponse:
    """
    Get list of available trading products
    
    Returns information about all available trading products including
    their ID, name, base/quote currencies, and trading parameters.
    """
    try:
        products = await client.get_products()
        return {"products": products}
    except CoinbaseError as e:
        raise HTTPException(
            status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e), "code": e.status_code, "details": e.response}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
        )

@router.get(
    "/products/{product_id}",
    response_model=ProductDetailResponse,
    responses={
        status.HTTP_200_OK: {"model": ProductDetailResponse, "description": "Successfully retrieved product details"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Product not found"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get product details",
    description="Get detailed information about a specific trading product"
)
async def get_product(
    product_id: str,
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> ProductDetailResponse:
    """
    Get details for a specific product
    
    Returns detailed information about a specific product including
    minimum order size, price/size increments, and trading status.
    """
    try:
        product = await client.get_product(product_id)
        return {"product": product}
    except CoinbaseError as e:
        status_code = e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        if status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Product {product_id} not found"}
            )
        raise HTTPException(
            status_code=status_code,
            detail={"error": str(e), "code": e.status_code, "details": e.response}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
        )

@router.get(
    "/ohlcv",
    responses={
        status.HTTP_200_OK: {"description": "Successfully retrieved mock candle data"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid parameters"}
    },
    summary="Get mock OHLCV candle data",
    description="Get simulated OHLCV candle data for testing purposes"
)
async def get_mock_ohlcv(
    symbol: str = Query("BTC-USD", description="Trading pair symbol"),
    timeframe: str = Query("1h", description="Candle timeframe (1m, 5m, 15m, 1h, 6h, 1d)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of candles to return"),
    clean_data: bool = Query(True, description="Whether to clean and normalize the data")
):
    """
    Get simulated OHLCV candles for testing
    
    Returns mock Open, High, Low, Close, Volume data for a specified symbol and timeframe.
    This is for testing purposes when you don't have valid Coinbase API credentials.
    
    When clean_data is True (default), the response includes:
    - Normalized and validated OHLCV data
    - Additional technical indicators (typical price, shadows, etc.)
    - Volume metrics and candlestick patterns
    """
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    from app.core.data_processor import OHLCVProcessor
    
    # Generate timestamps for each candle (most recent first)
    end_time = datetime.utcnow()
    
    # Map timeframe to timedelta
    timeframe_map = {
        "1m": timedelta(minutes=1),
        "5m": timedelta(minutes=5),
        "15m": timedelta(minutes=15),
        "1h": timedelta(hours=1),
        "6h": timedelta(hours=6),
        "1d": timedelta(days=1)
    }
    
    if timeframe not in timeframe_map:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid timeframe: {timeframe}. Valid options: {', '.join(timeframe_map.keys())}"
        )
    
    delta = timeframe_map[timeframe]
    timestamps = [end_time - i * delta for i in range(limit)]
    
    # Generate mock price data (starting at a realistic BTC price)
    base_price = 65000.0  # Example BTC price
    np.random.seed(42)  # For reproducible results
    
    # Generate random walk for price movement
    price_changes = np.random.normal(0, 300, limit)  # Normal distribution with mean 0, std 300
    cumulative_changes = np.cumsum(price_changes)
    
    # Generate candle data
    data = []
    for i, timestamp in enumerate(timestamps):
        price = base_price + cumulative_changes[i]
        candle = {
            "timestamp": timestamp,
            "open": price,
            "high": price * (1 + abs(np.random.normal(0, 0.005))),  # High is above open
            "low": price * (1 - abs(np.random.normal(0, 0.005))),   # Low is below open
            "close": price * (1 + np.random.normal(0, 0.002)),      # Close is randomly distributed
            "volume": abs(np.random.normal(100, 30))                # Random volume
        }
        data.append(candle)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Clean data if requested
    if clean_data:
        processor = OHLCVProcessor(decimal_places=2)
        df = processor.process_ohlcv(df)
    
    # Convert DataFrame to list of dictionaries
    candles = df.to_dict(orient="records")
    
    # Convert timestamps to ISO strings for JSON serialization
    for candle in candles:
        candle["timestamp"] = candle["timestamp"].isoformat()
    
    return {
        "candles": candles,
        "symbol": symbol,
        "timeframe": timeframe,
        "cleaned": clean_data,
        "count": len(candles)
    }

@router.get(
    "/api/v1/market/ohlcv",
    responses={
        status.HTTP_200_OK: {"description": "Successfully retrieved mock candle data"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid parameters"}
    },
    summary="Get mock OHLCV candle data with v1 API path",
    description="Get simulated OHLCV candle data for testing using v1 API path"
)
async def get_mock_ohlcv_v1(
    symbol: str = Query("BTC-USD", description="Trading pair symbol"),
    timeframe: str = Query("1h", description="Candle timeframe (1m, 5m, 15m, 1h, 6h, 1d)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of candles to return"),
    clean_data: bool = Query(True, description="Whether to clean and normalize the data")
):
    """
    Get simulated OHLCV candles for testing using v1 API path
    
    Returns mock Open, High, Low, Close, Volume data for a specified symbol and timeframe.
    This endpoint matches the /api/v1/market/ohlcv path structure.
    
    When clean_data is True (default), the response includes:
    - Normalized and validated OHLCV data
    - Additional technical indicators (typical price, shadows, etc.)
    - Volume metrics and candlestick patterns
    """
    # Reuse the logic from the original endpoint
    return await get_mock_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit,
        clean_data=clean_data
    )

@router.get(
    "/products/{product_id}/candles",
    responses={
        status.HTTP_200_OK: {"description": "Successfully retrieved candle data"},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid parameters"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Product not found"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get OHLCV candle data",
    description="Get historical OHLCV candle data with custom timeframes and optional data cleaning"
)
async def get_product_candles(
    product_id: str,
    timeframe: str = Query("1h", description="Candle timeframe (1m, 5m, 15m, 1h, 6h, 1d)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of candles to return"),
    start: Optional[str] = Query(None, description="Start time in ISO format (e.g., 2023-01-01T00:00:00Z)"),
    end: Optional[str] = Query(None, description="End time in ISO format (e.g., 2023-01-01T00:00:00Z)"),
    clean_data: bool = Query(True, description="Whether to clean and normalize the data")
):
    """
    Get historical OHLCV candles for a product with flexible timeframes
    
    Returns Open, High, Low, Close, Volume data for the specified product and timeframe.
    Supports common timeframes like 1m, 5m, 15m, 1h, 6h, 1d.
    
    When clean_data is True (default), the response includes:
    - Normalized and validated OHLCV data
    - Additional technical indicators (typical price, shadows, etc.)
    - Volume metrics and candlestick patterns
    """
    client = get_coinbase_client()
    try:
        # Convert dates if provided
        start_time = None
        end_time = None
        
        if start:
            try:
                start_time = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid start time format. Use ISO format (e.g., 2023-01-01T00:00:00Z)")
                
        if end:
            try:
                end_time = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid end time format. Use ISO format (e.g., 2023-01-01T00:00:00Z)")
        
        # Fetch OHLCV data
        df = await get_ohlcv(
            client=client, 
            symbol=product_id, 
            timeframe=timeframe, 
            limit=limit,
            start_time=start_time,
            end_time=end_time,
            clean_data=clean_data
        )
        
        # Convert DataFrame to list of dictionaries
        candles = df.to_dict(orient="records")
        
        # Convert timestamps to ISO strings for JSON serialization
        for candle in candles:
            candle["timestamp"] = candle["timestamp"].isoformat()
            
        return {
            "candles": candles,
            "symbol": product_id,
            "timeframe": timeframe,
            "cleaned": clean_data,
            "count": len(candles)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except CoinbaseError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get(
    "/products/{product_id}/trades",
    response_model=TradesResponse,
    responses={
        status.HTTP_200_OK: {"model": TradesResponse, "description": "Successfully retrieved trades"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Product not found"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get recent trades",
    description="Get recent trades for a product"
)
async def get_trades(
    product_id: str,
    limit: int = Query(100, ge=1, le=1000, description="Number of trades to return"),
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> TradesResponse:
    """
    Get recent trades for a product
    
    Returns a list of the most recent trades for the specified product.
    Limited to a maximum of 1000 trades.
    """
    try:
        trades = await client.get_market_trades(product_id=product_id, limit=limit)
        return {"trades": trades}
    except CoinbaseError as e:
        status_code = e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        if status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Product {product_id} not found"}
            )
        raise HTTPException(
            status_code=status_code,
            detail={"error": str(e), "code": e.status_code, "details": e.response}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
        )

@router.get(
    "/products/{product_id}/book",
    response_model=OrderBookResponse,
    responses={
        status.HTTP_200_OK: {"model": OrderBookResponse, "description": "Successfully retrieved order book"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Product not found"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get order book",
    description="Get order book for a product with specified level of detail"
)
async def get_order_book(
    product_id: str,
    level: int = Query(2, ge=1, le=3, description="Order book level (1=best bid/ask, 2=top 50, 3=full)"),
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> OrderBookResponse:
    """
    Get order book for a product
    
    Returns the order book for the specified product with varying levels of detail:
    - Level 1: Only the best bid and ask
    - Level 2: Top 50 bids and asks (aggregated)
    - Level 3: Full order book (non-aggregated)
    """
    try:
        book = await client.get_order_book(product_id=product_id, level=level)
        return book
    except CoinbaseError as e:
        status_code = e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        if status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Product {product_id} not found"}
            )
        raise HTTPException(
            status_code=status_code,
            detail={"error": str(e), "code": e.status_code, "details": e.response}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
        ) 