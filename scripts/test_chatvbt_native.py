#!/usr/bin/env python3
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Load environment variables from .env file
load_dotenv(verbose=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_chatvbt_native")

def test_native_vbt_chat():
    """Test if the native vectorbt chat functionality works"""
    try:
        import vectorbtpro as vbt
        logger.info("VectorBTPro successfully imported")
        
        # Get API key from environment (after loading .env)
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment")
            api_key = os.environ.get("OPENROUTER_API_KEY")
            if not api_key:
                logger.error("No API keys available in environment or .env file")
                return False
            else:
                logger.info("Using OPENROUTER_API_KEY")
        else:
            logger.info("Using OPENAI_API_KEY")
        
        # Log if GitHub token is available
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            logger.info("GitHub token available")
            vbt.settings.set('knowledge.assets.vbt.token', github_token)
        
        # Configure embeddings
        try:
            vbt.settings.set('knowledge.chat.embeddings_configs.openai.api_key', api_key)
            logger.info("Configured embeddings API key in vbt.settings")
            
            # If using OpenRouter, configure base URL
            if api_key == os.environ.get("OPENROUTER_API_KEY"):
                vbt.settings.set('knowledge.chat.openai_base_url', "https://openrouter.ai/api/v1")
                logger.info("Configured API base URL for OpenRouter")
        except Exception as e:
            logger.warning(f"Failed to configure embedding settings: {e}")
        
        # Test direct vbt.chat
        if hasattr(vbt, 'chat') and callable(vbt.chat):
            logger.info("Testing native vbt.chat function...")
            test_prompt = "What are the key components of a trading strategy? Answer in one sentence."
            
            try:
                response = vbt.chat(test_prompt, api_key=api_key)
                logger.info(f"Response from vbt.chat: {response}")
                return True
            except Exception as e:
                logger.error(f"vbt.chat error: {e}")
                
                # Try find_assets as an alternative
                try:
                    logger.info("Testing vbt.find_assets().chat function...")
                    assets = vbt.find_assets(test_prompt, top_k=5)
                    if assets is not None:
                        response = assets.chat(test_prompt, api_key=api_key)
                        logger.info(f"Response from find_assets().chat: {response}")
                        return True
                except Exception as e2:
                    logger.error(f"find_assets().chat error: {e2}")
        else:
            logger.error("vbt.chat function not available")
        
        return False
    except ImportError as e:
        logger.error(f"Failed to import vectorbtpro: {e}")
        return False

if __name__ == "__main__":
    success = test_native_vbt_chat()
    
    if success:
        logger.info("✅ Test PASSED: Native VectorBT chat works!")
        sys.exit(0)
    else:
        logger.error("❌ Test FAILED: Native VectorBT chat not working")
        sys.exit(1) 