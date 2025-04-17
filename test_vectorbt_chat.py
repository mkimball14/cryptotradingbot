#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_vectorbt_chat")

# Load environment variables
load_dotenv(verbose=True)

# Get API keys
openai_api_key = os.environ.get("OPENAI_API_KEY")
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Log API key status
logger.info(f"OPENAI_API_KEY present: {openai_api_key is not None}")
logger.info(f"OPENROUTER_API_KEY present: {openrouter_api_key is not None}")

# Ensure we have at least one API key
if not (openai_api_key or openrouter_api_key):
    logger.error("No API keys found. Please set either OPENAI_API_KEY or OPENROUTER_API_KEY.")
    sys.exit(1)

# If OPENAI_API_KEY is missing but we have OPENROUTER_API_KEY, use that
if not openai_api_key and openrouter_api_key:
    os.environ["OPENAI_API_KEY"] = openrouter_api_key
    logger.info("Set OPENAI_API_KEY from OPENROUTER_API_KEY for compatibility.")

# Test direct OpenRouter API
if openrouter_api_key:
    try:
        from openai import OpenAI
        logger.info("Testing OpenRouter API directly...")
        
        client = OpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url
        )
        
        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=[{"role": "user", "content": "What's 2+2?"}],
            max_tokens=10
        )
        
        logger.info(f"OpenRouter direct test successful: {response.choices[0].message.content}")
    except Exception as e:
        logger.error(f"OpenRouter direct test failed: {e}")

# Test VectorBTPro chat
try:
    import vectorbtpro as vbt
    logger.info("Testing VectorBTPro configuration...")
    
    # Configure VectorBTPro with OpenRouter
    if hasattr(vbt, 'settings') and hasattr(vbt.settings, 'knowledge') and hasattr(vbt.settings.knowledge, 'chat'):
        try:
            # Try to configure knowledge.chat
            vbt.settings.knowledge.chat.openai_key = openrouter_api_key or openai_api_key
            vbt.settings.knowledge.chat.openai_base_url = openrouter_base_url
            vbt.settings.knowledge.chat.model = "openrouter/auto"
            logger.info("Configured VectorBTPro knowledge.chat settings")
            
            # Print current settings for debugging
            logger.info(f"Settings configured: key_set={vbt.settings.knowledge.chat.openai_key is not None}, "
                        f"base_url={vbt.settings.knowledge.chat.openai_base_url}, "
                        f"model={vbt.settings.knowledge.chat.model}")
        except Exception as e:
            logger.error(f"Failed to configure knowledge.chat: {e}")
    
    # Attempt to use chat directly
    if hasattr(vbt, 'chat') and callable(vbt.chat):
        try:
            logger.info("Testing vbt.chat function...")
            response = vbt.chat("What's 2+2?")
            logger.info(f"vbt.chat test successful: {response}")
        except Exception as e:
            logger.error(f"vbt.chat test failed: {e}")
    else:
        logger.error("vbt.chat function not available")
except ImportError:
    logger.error("Failed to import vectorbtpro")

logger.info("Test complete") 