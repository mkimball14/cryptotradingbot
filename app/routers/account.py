from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.coinbase import CoinbaseClient
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
    except Exception as e:
        logger.error(f"Error getting account balance: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to retrieve account balance due to an internal error."}
        )

# Remove the /positions endpoint as get_positions is not implemented in the client
# @router.get(
#     "/positions",
#     response_model=PositionsResponse,
#     responses={
#         status.HTTP_200_OK: {"model": PositionsResponse, "description": "Successfully retrieved positions"},
#         status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Authentication failed"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
#     },
#     summary="Get open positions",
#     description="Retrieve all current open positions"
# )
# async def get_positions(
#     client: CoinbaseClient = Depends(get_coinbase_client)
# ) -> PositionsResponse:
#     """
#     Get current open positions
#     
#     Returns a list of all open positions with details including product ID,
#     position size, entry price, and unrealized profit/loss.
#     """
#     try:
#         # Make client call async if get_positions is async
#         positions = await client.get_positions()
#         return {"positions": positions}
#     # Change CoinbaseError to generic Exception
#     except Exception as e:
#         # Log the error for debugging
#         logger.error(f"Error getting positions: {e}", exc_info=True)
#          # Return a generic 500 error
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail={"error": "Failed to retrieve positions due to an internal error."}
#         ) 