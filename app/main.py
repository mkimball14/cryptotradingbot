from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from app.routers import account, orders, market, websocket
from app.core.config import Settings
from app.core.deps import get_settings

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Crypto Trading Bot",
    lifespan=websocket.lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(account.router)
app.include_router(orders.router)
app.include_router(market.router)
app.include_router(websocket.router, tags=["websocket"])

# Include v1 API routers with prefix
app.include_router(market.router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Root endpoint - health check
    """
    return {"status": "ok", "message": "Crypto Trading Bot API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    settings = get_settings()
    return {
        "status": "healthy",
        "debug_mode": settings.DEBUG,
        "websocket_enabled": True
    }

# Import and include API routers here
# from app.api.v1.router import api_router
# app.include_router(api_router, prefix="/api/v1")

# End of file 