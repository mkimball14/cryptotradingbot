#!/usr/bin/env python3
import os
import sys
import logging
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_chatvbt_fix")

# Import our enhanced chat function
from scripts.strategies.edge_strategy_assistant import chat_with_vectorbt, VECTORBT_AVAILABLE, CHATVBT_AVAILABLE, API_KEY

def test_chat_functionality():
    """Test if our chat functionality works with the new implementation"""
    logger.info("Testing improved ChatVBT implementation")
    
    # Log the current state
    logger.info(f"VECTORBT_AVAILABLE: {VECTORBT_AVAILABLE}")
    logger.info(f"CHATVBT_AVAILABLE: {CHATVBT_AVAILABLE}")
    logger.info(f"API_KEY available: {API_KEY is not None}")
    
    # Simple test prompt
    test_prompt = "What are the key components of a trading strategy? Answer in one sentence."
    
    try:
        logger.info(f"Sending prompt: {test_prompt}")
        response = chat_with_vectorbt(test_prompt)
        
        if response and len(response) > 0:
            logger.info(f"Received valid response ({len(response)} chars)")
            logger.info(f"Response: {response}")
            return True
        else:
            logger.warning("Empty response received")
            return False
    except Exception as e:
        logger.error(f"Error testing chat functionality: {e}")
        return False

if __name__ == "__main__":
    # Run the test
    success = test_chat_functionality()
    
    # Print result
    if success:
        logger.info("✅ Test PASSED: ChatVBT functionality works")
        sys.exit(0)
    else:
        logger.error("❌ Test FAILED: ChatVBT functionality not working")
        sys.exit(1) 