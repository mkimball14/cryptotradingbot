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
logger = logging.getLogger("test_direct_chat")

# Load environment variables
load_dotenv(verbose=True)

# Get API keys
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
openrouter_base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Log API key status
logger.info(f"OPENROUTER_API_KEY present: {openrouter_api_key is not None}")

# Check if OpenRouter API key is available
if not openrouter_api_key:
    logger.error("OpenRouter API key not found. Please set OPENROUTER_API_KEY in your .env file.")
    sys.exit(1)

# Create direct chat function
def create_direct_chat():
    try:
        from openai import OpenAI
        
        # Create a client with OpenRouter settings
        client = OpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url
        )
        
        # Create a chat function that uses OpenRouter directly
        def direct_chat(prompt):
            try:
                completion = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                return completion.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenRouter direct chat error: {e}")
                return f"Error: {str(e)}"
        
        logger.info("Successfully created direct_chat function")
        return direct_chat
    except Exception as e:
        logger.error(f"Failed to create direct_chat: {e}")
        return None

# Get direct chat function
direct_chat = create_direct_chat()
if direct_chat is None:
    logger.error("Failed to create direct_chat function")
    sys.exit(1)

# Test direct chat
logger.info("Testing direct chat function...")
response = direct_chat("What's 2+2? Answer in one word.")
logger.info(f"Direct chat response: {response}")

# Test with longer prompt
logger.info("Testing direct chat with a longer prompt...")
response = direct_chat("""
Please provide a simple example of a trading strategy that uses RSI and Bollinger Bands.
Keep it under 100 words.
""")
logger.info(f"Direct chat longer response: {response}")

logger.info("Test complete") 