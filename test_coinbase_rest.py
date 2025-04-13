import asyncio
import logging
import os
import sys
import json
import pytest
from types import SimpleNamespace # To create a simple settings object

# Add project root to path to find app module
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# We no longer need get_settings from config
# from app.core.config import get_settings 
from app.core.coinbase import CoinbaseClient

# Configure logging to see debug messages
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define path to the key file (assuming it's in the project root)
KEY_FILE_PATH = "cdp_api_key.json"

@pytest.fixture(scope="module")
def coinbase_client():
    """Pytest fixture to initialize the CoinbaseClient once per module."""
    logger.info("Attempting to load credentials from JSON and initialize client for tests...")
    try:
        # Read credentials directly from JSON
        if not os.path.exists(KEY_FILE_PATH):
            logger.error(f"Key file not found at: {KEY_FILE_PATH}")
            pytest.fail(f"Key file not found: {KEY_FILE_PATH}")

        with open(KEY_FILE_PATH, 'r') as f:
            key_data = json.load(f)

        if 'name' not in key_data or 'privateKey' not in key_data:
             logger.error(f"Key file {KEY_FILE_PATH} is missing 'name' or 'privateKey' field.")
             pytest.fail(f"Key file {KEY_FILE_PATH} is missing 'name' or 'privateKey' field.")

        # Create a temporary settings object
        temp_settings = SimpleNamespace()
        temp_settings.COINBASE_JWT_KEY_NAME = key_data['name']
        temp_settings.COINBASE_JWT_PRIVATE_KEY = key_data['privateKey']
        # TODO: Get API URL from settings or constants, avoid hardcoding if possible
        temp_settings.COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage"

        # Initialize client with temporary settings
        client = CoinbaseClient(temp_settings)
        logger.info("Client initialized successfully for tests.")
        return client # Provide the client to tests
    except Exception as e:
        logger.error(f"Failed to initialize client for tests: {e}", exc_info=True)
        pytest.fail(f"Client initialization failed: {e}")

# Removed async marker as test function is now sync
def test_get_products(coinbase_client):
    """Test retrieving all products"""
    try:
        product_list = coinbase_client.get_products()
        logger.info(f"Successfully retrieved {len(product_list)} products")
        # Print first 3 products only to avoid flooding logs
        for i, product in enumerate(product_list[:3]):
            print(f"Product {i+1}: {product.get('product_id')} - {product.get('status')}")
        assert product_list is not None # Basic assertion
        assert len(product_list) > 0 # Ensure we got some products
        assert 'product_id' in product_list[0] # Check structure of first product
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        pytest.fail(f"Test failed due to exception: {e}")

# Removed async marker as test function is now sync
def test_get_product(coinbase_client):
    """Test retrieving a specific product"""
    product_id = "BTC-USD" # Define product ID inside the test
    try:
        product_info = coinbase_client.get_product(product_id)
        logger.info(f"Successfully retrieved product info for {product_id}:")
        print(f"  Base Currency: {product_info.get('base_currency_id')}")
        print(f"  Quote Currency: {product_info.get('quote_currency_id')}")
        print(f"  Status: {product_info.get('status')}")
        assert product_info is not None
        assert product_info.get('product_id') == product_id
        assert product_info.get('base_currency_id') == "BTC"
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        pytest.fail(f"Test failed due to exception: {e}")

# Removed async marker as test function is now sync
def test_get_accounts(coinbase_client):
    """Test retrieving accounts"""
    try:
        accounts = coinbase_client.get_accounts()
        account_list = getattr(accounts, 'accounts', []) # Access the list via attribute
        logger.info(f"Successfully retrieved {len(account_list)} accounts")
        # Print limited info to avoid flooding logs
        for i, account_obj in enumerate(account_list[:3]):
            # Access account attributes directly or via .to_dict()
            account_dict = account_obj.to_dict() if hasattr(account_obj, 'to_dict') else vars(account_obj)
            print(f"Account {i+1}: {account_dict.get('name')} - {account_dict.get('available_balance')}")

        assert accounts is not None
        # Add more specific assertions if needed, e.g., check for expected keys
        assert hasattr(accounts, 'accounts') # Check the attribute exists
        if len(account_list) > 0:
            # Check keys in the dictionary representation of the first account
            first_account_dict = account_list[0].to_dict() if hasattr(account_list[0], 'to_dict') else vars(account_list[0])
            assert 'uuid' in first_account_dict
            assert 'currency' in first_account_dict
    except Exception as e:
        logger.error(f"Error getting accounts: {e}")
        pytest.fail(f"Test failed due to exception: {e}")

# Removed main() function and if __name__ == "__main__" block
# Pytest will now discover and run the decorated test functions 