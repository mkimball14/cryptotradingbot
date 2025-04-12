import asyncio
import logging
import os
import sys
import json
from types import SimpleNamespace # To create a simple settings object

# Add project root to path to find app module
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# We no longer need get_settings from config
# from app.core.config import get_settings 
from app.core.coinbase import CoinbaseClient, CoinbaseError

# Configure logging to see debug messages
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define path to the key file (assuming it's in the project root)
KEY_FILE_PATH = "cdp_api_key.json"

async def test_get_products():
    """Test retrieving all products"""
    try:
        product_list = await client.get_products()
        logger.info(f"Successfully retrieved {len(product_list)} products")
        # Print first 3 products only to avoid flooding logs
        for i, product in enumerate(product_list[:3]):
            print(f"Product {i+1}: {product.get('product_id')} - {product.get('status')}")
        return True
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return False

async def test_get_product(product_id):
    """Test retrieving a specific product"""
    try:
        product_info = await client.get_product(product_id)
        logger.info(f"Successfully retrieved product info for {product_id}:")
        print(f"  Base Currency: {product_info.get('base_currency_id')}")
        print(f"  Quote Currency: {product_info.get('quote_currency_id')}")
        print(f"  Status: {product_info.get('status')}")
        return True
    except Exception as e:
        logger.error(f"Error getting product {product_id}: {e}")
        return False

async def test_get_accounts():
    """Test retrieving accounts"""
    try:
        accounts = await client.get_accounts()
        logger.info(f"Successfully retrieved {len(accounts)} accounts")
        # Print limited info to avoid flooding logs
        for i, account in enumerate(accounts[:3]):
            print(f"Account {i+1}: {account.get('name')} - {account.get('available_balance')}")
        return True
    except Exception as e:
        logger.error(f"Error getting accounts: {e}")
        return False

async def main():
    global client  # Make client accessible to test functions
    
    logger.info("Attempting to load credentials from JSON and initialize client...")
    try:
        # Read credentials directly from JSON
        if not os.path.exists(KEY_FILE_PATH):
            logger.error(f"Key file not found at: {KEY_FILE_PATH}")
            return
            
        with open(KEY_FILE_PATH, 'r') as f:
            key_data = json.load(f)
            
        if 'name' not in key_data or 'privateKey' not in key_data:
             logger.error(f"Key file {KEY_FILE_PATH} is missing 'name' or 'privateKey' field.")
             return
             
        # Create a temporary settings object
        temp_settings = SimpleNamespace()
        temp_settings.COINBASE_JWT_KEY_NAME = key_data['name']
        # The private key from JSON already has newlines, no need for \n conversion
        temp_settings.COINBASE_JWT_PRIVATE_KEY = key_data['privateKey'] 
        # Manually set the correct API URL
        temp_settings.COINBASE_API_URL = "https://api.coinbase.com/api/v3/brokerage"
        
        # Initialize client with temporary settings
        client = CoinbaseClient(temp_settings)
        logger.info("Client initialized using credentials from JSON.")
        
    except Exception as e:
        logger.error(f"Failed to initialize client using JSON: {e}", exc_info=True)
        return

    # Print key information about our setup
    logger.info("==== TEST CONFIGURATION ====")
    logger.info(f"API URL: {client.api_url}")
    logger.info(f"Key Name: {client.key_name}")
    logger.info(f"Private Key Type: {type(client.private_key)}")
    logger.info("============================")
    
    # Run a series of tests to verify API connectivity
    logger.info("\n==== RUNNING API TESTS ====")
    
    # Test 1: Get all products
    logger.info("\n[TEST 1] Getting all products...")
    await test_get_products()
    
    # Test 2: Get specific product
    product_id = "BTC-USD"
    logger.info(f"\n[TEST 2] Getting product {product_id}...")
    await test_get_product(product_id)
    
    # Test 3: Get accounts
    logger.info("\n[TEST 3] Getting accounts...")
    await test_get_accounts()
    
    logger.info("\n==== TESTS COMPLETE ====")

if __name__ == "__main__":
    asyncio.run(main()) 