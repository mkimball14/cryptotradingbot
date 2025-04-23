#!/usr/bin/env python3
"""
Settings management for the crypto trading bot.
Uses Pydantic for validation and type checking.
"""

import os
import logging
from typing import Optional, List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, validator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoinbaseSettings(BaseSettings):
    """Coinbase API settings."""
    
    # Coinbase Advanced API (JWT Authentication)
    COINBASE_ADVANCED_KEY_NAME: Optional[str] = None
    COINBASE_ADVANCED_PRIVATE_KEY: Optional[str] = None
    COINBASE_ADVANCED_API_URL: str = "https://api.coinbase.com/api/v3/brokerage"
    
    # Coinbase Exchange (WebSocket Authentication)
    COINBASE_API_KEY: Optional[str] = None
    COINBASE_API_SECRET: Optional[str] = None
    COINBASE_API_PASSPHRASE: Optional[str] = None
    COINBASE_WS_URL: str = "wss://ws-feed.exchange.coinbase.com"
    
    @validator('COINBASE_ADVANCED_PRIVATE_KEY')
    def validate_private_key(cls, v):
        """Validate EC private key is in PEM format."""
        if not v:
            return v
            
        if not v.startswith('-----BEGIN EC PRIVATE KEY-----'):
            logger.warning("COINBASE_ADVANCED_PRIVATE_KEY does not appear to be in correct EC PEM format")
        return v
    
    @validator('COINBASE_API_SECRET')
    def validate_api_secret(cls, v):
        """Validate API secret is in base64 format."""
        if not v:
            return v
            
        try:
            import base64
            base64.b64decode(v)
        except Exception:
            logger.warning("COINBASE_API_SECRET does not appear to be valid base64")
        return v


class DatabaseSettings(BaseSettings):
    """Database settings."""
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "crypto_trading"
    DB_USER: str = "postgres"
    DB_PASSWORD: Optional[str] = None
    DB_SSL_MODE: str = "disable"
    
    # SQLAlchemy connection string
    DB_URL: Optional[str] = None
    
    @validator('DB_URL', always=True)
    def set_db_url(cls, v, values):
        """Set database URL if not provided."""
        if v:
            return v
            
        # Construct PostgreSQL connection string
        password_part = f":{values['DB_PASSWORD']}" if values.get('DB_PASSWORD') else ""
        return f"postgresql://{values['DB_USER']}{password_part}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}?sslmode={values['DB_SSL_MODE']}"


class TradingSettings(BaseSettings):
    """Trading strategy settings."""
    
    # Assets to trade
    TRADING_PAIRS: List[str] = Field(default_factory=lambda: ["BTC-USD", "ETH-USD"])
    
    # Trading parameters
    TRADING_TIMEFRAME: str = "1h"  # 1h, 4h, 1d, etc.
    TRADING_STRATEGY: str = "basic"  # Strategy name
    CAPITAL_PER_TRADE: float = 100.0  # Amount to use per trade in USD
    MAX_POSITIONS: int = 5  # Maximum number of open positions
    STOP_LOSS_PCT: float = 2.0  # Stop loss percentage
    TAKE_PROFIT_PCT: float = 5.0  # Take profit percentage
    
    # Backtesting
    BACKTEST_START_DATE: str = "2023-01-01"
    BACKTEST_END_DATE: Optional[str] = None  # Defaults to current date


class AppSettings(BaseSettings):
    """Main application settings."""
    
    # Application environment
    ENV: str = "development"  # development, production, testing
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Authentication and security
    SECRET_KEY: str = "development-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOW_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    
    # Data directory
    DATA_DIR: str = "./data"
    
    @validator('ENV')
    def validate_env(cls, v):
        """Validate environment is one of the allowed values."""
        allowed = ["development", "production", "testing"]
        if v.lower() not in allowed:
            raise ValueError(f"ENV must be one of {allowed}")
        return v.lower()
    
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        """Validate log level is one of the allowed values."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()
    
    @validator('DATA_DIR')
    def validate_data_dir(cls, v):
        """Validate data directory exists or create it."""
        if not os.path.exists(v):
            os.makedirs(v, exist_ok=True)
            logger.info(f"Created data directory: {v}")
        return v


class Settings(BaseSettings):
    """Combined settings for the entire application."""
    
    # Model configuration
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='allow'
    )
    
    app: AppSettings = Field(default_factory=AppSettings)
    coinbase: CoinbaseSettings = Field(default_factory=CoinbaseSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    trading: TradingSettings = Field(default_factory=TradingSettings)
    
    # Flag to check if all required API keys are set
    api_keys_configured: bool = False
    
    @validator('api_keys_configured', always=True)
    def check_api_keys(cls, v, values):
        """Check if all required API keys are configured."""
        coinbase = values.get('coinbase', CoinbaseSettings())
        
        # Check if either Advanced API or Exchange API is configured
        advanced_api_configured = (
            coinbase.COINBASE_ADVANCED_KEY_NAME is not None and 
            coinbase.COINBASE_ADVANCED_PRIVATE_KEY is not None
        )
        
        exchange_api_configured = (
            coinbase.COINBASE_API_KEY is not None and
            coinbase.COINBASE_API_SECRET is not None and
            coinbase.COINBASE_API_PASSPHRASE is not None
        )
        
        return advanced_api_configured or exchange_api_configured


# Create global settings instance
def get_settings() -> Settings:
    """Get application settings singleton."""
    try:
        settings = Settings()
        
        # Set up logging based on settings
        log_level = getattr(logging, settings.app.LOG_LEVEL)
        logging.basicConfig(level=log_level)
        
        # Log API configuration status
        if settings.api_keys_configured:
            logger.info("API keys configured successfully")
        else:
            logger.warning(
                "API keys not fully configured - "
                "set COINBASE_ADVANCED_KEY_NAME and COINBASE_ADVANCED_PRIVATE_KEY for Advanced API "
                "or COINBASE_API_KEY, COINBASE_API_SECRET, and COINBASE_API_PASSPHRASE for Exchange API"
            )
            
        return settings
    except Exception as e:
        logger.error(f"Error loading settings: {str(e)}")
        raise


# Export the settings instance
settings = get_settings() 