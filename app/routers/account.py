from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.coinbase import CoinbaseClient, CoinbaseError
from app.core.deps import get_coinbase_client
from app.models.responses import AccountsResponse, PositionsResponse, ErrorResponse

router = APIRouter(prefix="/account", tags=["account"])

@router.get(
    "/balance", 
    response_model=AccountsResponse,
    responses={
        status.HTTP_200_OK: {"model": AccountsResponse, "description": "Successfully retrieved account balances"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get account balances",
    description="Retrieve account balances for all currencies"
)
async def get_account_balance(
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> AccountsResponse:
    """
    Get account balances for all currencies
    
    Returns a list of all account balances with their respective currencies, 
    available and hold amounts.
    """
    try:
        accounts = await client.get_accounts()
        return {"accounts": accounts}
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
    "/positions",
    response_model=PositionsResponse,
    responses={
        status.HTTP_200_OK: {"model": PositionsResponse, "description": "Successfully retrieved positions"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get open positions",
    description="Retrieve all current open positions"
)
async def get_positions(
    client: CoinbaseClient = Depends(get_coinbase_client)
) -> PositionsResponse:
    """
    Get current open positions
    
    Returns a list of all open positions with details including product ID,
    position size, entry price, and unrealized profit/loss.
    """
    try:
        positions = await client.get_positions()
        return {"positions": positions}
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