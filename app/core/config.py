import json
import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, Any, Dict
from pydantic import ConfigDict, model_validator

# Define the path to the JSON key file relative to the project root
# Assuming config.py is in app/core/, go up two levels
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_KEY_FILE = os.path.join(PROJECT_ROOT, "cdp_api_key.json")

class Settings(BaseSettings):
    """Application settings"""
    
    # Debug mode
    DEBUG: bool = False
    
    # Project info
    PROJECT_NAME: str = "Crypto Trading Bot"
    APP_VERSION: str = "1.0.0"
    
    # Coinbase API settings (Using Advanced Trade API / JWT)
    # These will be loaded from JSON or environment variables
    COINBASE_JWT_KEY_NAME: Optional[str] = None 
    COINBASE_JWT_PRIVATE_KEY: Optional[str] = None 
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
    
    # Run Mode
    DRY_RUN_MODE: bool = False # Set to True to simulate orders without real execution
    
    # Database Settings (for future use)
    DATABASE_URL: Optional[str] = None
    
    @model_validator(mode='before')
    @classmethod
    def parse_booleans(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse string boolean values from environment variables.
        """
        if not isinstance(data, dict):
            return data
            
        if 'DEBUG' in data and isinstance(data['DEBUG'], str):
            data['DEBUG'] = data['DEBUG'].lower() in ('true', 't', 'yes', 'y', '1')
            
        # Add other boolean parsing if needed
            
        return data
    
    class Config:
        # env_file = ".env" # Removed: We load keys manually now
        case_sensitive = True
        extra = 'allow' # Allow other settings from environment variables

@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    Loads JWT keys from JSON file first, then falls back to environment variables.
    
    Returns:
        Settings: Application settings instance
    
    Raises:
        FileNotFoundError: If cdp_api_key.json is not found.
        ValueError: If required keys are missing from JSON or environment.
    """
    key_name = None
    private_key = None

    # Try loading from JSON file first
    if os.path.exists(JSON_KEY_FILE):
        try:
            with open(JSON_KEY_FILE, 'r') as f:
                key_data = json.load(f)
            key_name = key_data.get('name')
            private_key = key_data.get('privateKey')
            if not key_name or not private_key:
                print(f"Warning: 'name' or 'privateKey' missing in {JSON_KEY_FILE}")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read or parse {JSON_KEY_FILE}: {e}")
    else:
        print(f"Warning: JSON key file not found at {JSON_KEY_FILE}. Trying environment variables.")

    # Initialize settings, allowing pydantic-settings to load from environment
    # if keys weren't successfully loaded from JSON.
    settings_data = {}
    if key_name:
        settings_data['COINBASE_JWT_KEY_NAME'] = key_name
    if private_key:
        settings_data['COINBASE_JWT_PRIVATE_KEY'] = private_key
        
    # Initialize with JSON data first, then let pydantic load env vars for others
    settings = Settings(**settings_data)
    
    # Final validation: Ensure keys are loaded either from JSON or ENV
    if not settings.COINBASE_JWT_KEY_NAME or not settings.COINBASE_JWT_PRIVATE_KEY:
         raise ValueError("COINBASE_JWT_KEY_NAME and COINBASE_JWT_PRIVATE_KEY must be set, either in "
                          f"{JSON_KEY_FILE} or as environment variables.")

    return settings 