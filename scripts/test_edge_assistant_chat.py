#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_edge_assistant_chat")

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv(verbose=True)
logger.info("Loaded environment variables from .env file")

def test_edge_assistant_chat():
    """Test the chat_with_vectorbt function in edge_strategy_assistant.py"""
    try:
        # Import the edge_strategy_assistant module
        from scripts.strategies.edge_strategy_assistant import chat_with_vectorbt, NATIVE_CHATVBT_AVAILABLE
        
        logger.info(f"Successfully imported edge_strategy_assistant - Native ChatVBT Available: {NATIVE_CHATVBT_AVAILABLE}")
        
        # Test simple prompt
        prompt = "What are the key components of a multi-factor trading strategy?"
        
        logger.info(f"Sending test prompt: {prompt}")
        response = chat_with_vectorbt(prompt)
        
        if response:
            logger.info(f"Received response: {response[:200]}...")
            logger.info("Test PASSED: Successfully received response from chat_with_vectorbt")
            return True
        else:
            logger.error("Test FAILED: No response received from chat_with_vectorbt")
            return False
    
    except Exception as e:
        logger.error(f"Test FAILED: Error testing edge_strategy_assistant chat: {e}")
        return False

if __name__ == "__main__":
    result = test_edge_assistant_chat()
    sys.exit(0 if result else 1) 