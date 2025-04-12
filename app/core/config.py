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
    
    # Coinbase API settings (Using Advanced Trade API / JWT)
    COINBASE_JWT_KEY_NAME: str
    COINBASE_JWT_PRIVATE_KEY: str # Should be the full PEM key string
    COINBASE_API_URL: str = "https://api.coinbase.com/api/v3/brokerage" 
    COINBASE_WS_URL: str = "wss://advanced-trade-ws.coinbase.com"
    # COINBASE_API_KEY: str # Old
    # COINBASE_API_SECRET: str # Old
    # COINBASE_API_PASSPHRASE: Optional[str] = None # Old
    
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
        if 'COINBASE_JWT_PRIVATE_KEY' in data and isinstance(data['COINBASE_JWT_PRIVATE_KEY'], str):
            private_key = data['COINBASE_JWT_PRIVATE_KEY']
            # Remove surrounding quotes if present
            if (private_key.startswith('"') and private_key.endswith('"')) or (private_key.startswith("'") and private_key.endswith("'")):
                private_key = private_key[1:-1]
            # Replace escaped newlines with actual newlines
            private_key = private_key.replace('\\n', '\n')
            data['COINBASE_JWT_PRIVATE_KEY'] = private_key
            
        # Clean up JWT key name
        if 'COINBASE_JWT_KEY_NAME' in data and isinstance(data['COINBASE_JWT_KEY_NAME'], str):
            data['COINBASE_JWT_KEY_NAME'] = data['COINBASE_JWT_KEY_NAME'].strip('"\'')

        # Remove old parser logic if it conflicts or is not needed
        # if 'COINBASE_API_SECRET' in data and isinstance(data['COINBASE_API_SECRET'], str):
        #     secret = data['COINBASE_API_SECRET']
        #     if (secret.startswith('"') and secret.endswith('"')) or (secret.startswith("'") and secret.endswith("'")):
        #         secret = secret[1:-1]
        #     secret = secret.replace('\\n', '\n')
        #     data['COINBASE_API_SECRET'] = secret
        # if 'COINBASE_API_KEY' in data and isinstance(data['COINBASE_API_KEY'], str):
        #     data['COINBASE_API_KEY'] = data['COINBASE_API_KEY'].strip('"\'')
            
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