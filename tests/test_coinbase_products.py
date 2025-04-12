import sys
import os
import asyncio
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = script_dir  # Assuming we're in the root directory
sys.path.insert(0, project_root)

from app.core.config import Settings
from app.core.coinbase import CoinbaseClient

async def main():
    try:
        # Load settings from .env
        settings = Settings()
        client = CoinbaseClient(settings)
        
        # Try to fetch products first (simpler endpoint)
        logger.info("Attempting to fetch products...")
        products = await client.get_products()
        
        # Print the first few products
        if products and len(products) > 0:
            logger.info(f"Successfully fetched {len(products)} products!")
            logger.info(f"First few products: {json.dumps(products[:3], indent=2)}")
        else:
            logger.error(f"Got empty products response: {products}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 