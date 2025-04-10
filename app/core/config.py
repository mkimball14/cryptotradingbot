from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, Any, Dict
from pydantic import ConfigDict, model_validator

class Settings(BaseSettings):
    """Application settings"""
    
    # Debug mode
    DEBUG: bool = False
    
    # Project info
    PROJECT_NAME: str = "Crypto Trading Bot"
    APP_VERSION: str = "1.0.0"
    
    # Coinbase API settings
    COINBASE_API_KEY: str
    COINBASE_API_SECRET: str
    COINBASE_API_PASSPHRASE: Optional[str] = None
    COINBASE_API_URL: str = "https://api.coinbase.com"  # Default API URL
    
    # Trading settings
    TRADING_ENABLED: bool = False
    MAX_OPEN_POSITIONS: int = 3
    RISK_PERCENTAGE: float = 1.0
    DEFAULT_QUOTE_CURRENCY: str = "USD"
    
    # Database Settings (for future use)
    DATABASE_URL: Optional[str] = None
    
    @model_validator(mode='before')
    @classmethod
    def parse_booleans(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse string boolean values to actual booleans and clean up API credentials
        """
        if not isinstance(data, dict):
            return data
            
        if 'DEBUG' in data and isinstance(data['DEBUG'], str):
            data['DEBUG'] = data['DEBUG'].lower() in ('true', 't', 'yes', 'y', '1')
            
        # Handle multiline PEM key
        if 'COINBASE_API_SECRET' in data and isinstance(data['COINBASE_API_SECRET'], str):
            secret = data['COINBASE_API_SECRET']
            # Remove surrounding quotes if present
            if (secret.startswith('"') and secret.endswith('"')) or (secret.startswith("'") and secret.endswith("'")):
                secret = secret[1:-1]
            # Replace escaped newlines with actual newlines
            secret = secret.replace('\\n', '\n')
            data['COINBASE_API_SECRET'] = secret
            
        # Clean up API key
        if 'COINBASE_API_KEY' in data and isinstance(data['COINBASE_API_KEY'], str):
            data['COINBASE_API_KEY'] = data['COINBASE_API_KEY'].strip('"\'')
            
        return data
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = 'allow'  # Allow extra fields from environment variables

@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    Returns:
        Settings: Application settings instance
    """
    return Settings() 