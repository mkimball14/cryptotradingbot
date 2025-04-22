#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_enhanced_assistant")

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv(verbose=True)
logger.info("Loaded environment variables from .env file")

def test_enhancements():
    """Test the enhanced features in edge_strategy_assistant.py"""
    try:
        # Import the edge_strategy_assistant module
        from scripts.strategies.edge_strategy_assistant import (
            chat_with_vectorbt, 
            parse_llm_json, 
            api_rate_limiter,
            create_task_from_strategy_insight,
            EnhancedEdgeStrategy
        )
        
        logger.info("Successfully imported enhanced edge_strategy_assistant modules")
        
        # 1. Test caching functionality
        logger.info("Testing caching functionality...")
        
        # First request should hit the API
        prompt = "What are the advantages of combining multiple indicators in a trading strategy?"
        logger.info(f"Sending first request (should use API): {prompt}")
        start_time = time.time()
        response1 = chat_with_vectorbt(prompt, use_cache=True)
        time1 = time.time() - start_time
        logger.info(f"First request completed in {time1:.2f} seconds")
        
        # Second request should use the cache
        logger.info("Sending second request (should use cache)")
        start_time = time.time()
        response2 = chat_with_vectorbt(prompt, use_cache=True)
        time2 = time.time() - start_time
        logger.info(f"Second request completed in {time2:.2f} seconds")
        
        # Check if second request was faster (indicating cache use)
        cache_working = time2 < time1
        logger.info(f"Cache test {'PASSED' if cache_working else 'FAILED'}: First request: {time1:.2f}s, Second request: {time2:.2f}s")
        
        # 2. Test JSON parsing
        logger.info("Testing JSON parsing functionality...")
        test_response = """
        Here's an analysis of the parameters:
        
        ```json
        {
          "rsi_window": {
            "current": 14,
            "suggested": 10,
            "explanation": "Shorter window for faster response"
          },
          "bb_window": {
            "current": 20,
            "suggested": 20,
            "explanation": "Standard setting works well"
          }
        }
        ```
        
        I hope this helps!
        """
        
        parsed_json = parse_llm_json(test_response)
        json_parsing_works = isinstance(parsed_json, dict) and "rsi_window" in parsed_json
        logger.info(f"JSON parsing test {'PASSED' if json_parsing_works else 'FAILED'}")
        if json_parsing_works:
            logger.info(f"Parsed JSON: {json.dumps(parsed_json, indent=2)[:100]}...")
        
        # 3. Test rate limiter (just check functionality, don't actually test limits)
        logger.info("Testing rate limiter functionality...")
        can_call_before = api_rate_limiter.can_call()
        api_rate_limiter.record_call()
        can_call_after = api_rate_limiter.can_call()
        
        rate_limiter_works = can_call_before and can_call_after  # Should still be True since we're below the limit
        logger.info(f"Rate limiter test {'PASSED' if rate_limiter_works else 'FAILED'}")
        logger.info(f"Rate limiter has registered {len(api_rate_limiter.calls)} calls")
        
        # 4. Test integration with task-master (just functionality, not actual execution)
        logger.info("Testing task creation functionality...")
        try:
            # Mock the subprocess.run function to avoid actually calling task-master
            import subprocess
            original_run = subprocess.run
            
            def mock_run(*args, **kwargs):
                logger.info(f"Would execute: {args[0] if len(args) > 0 else kwargs.get('cmd', [])}")
                from collections import namedtuple
                Result = namedtuple('Result', ['returncode', 'stdout', 'stderr'])
                return Result(0, "Task created successfully", "")
            
            # Replace subprocess.run with our mock
            subprocess.run = mock_run
            
            # Test task creation
            result = create_task_from_strategy_insight("Test insight")
            task_creation_works = result.get("success", False)
            
            # Restore original function
            subprocess.run = original_run
            
            logger.info(f"Task creation test {'PASSED' if task_creation_works else 'FAILED'}")
        except Exception as e:
            logger.error(f"Error testing task creation: {e}")
            task_creation_works = False
        
        # 5. Test EnhancedEdgeStrategy with the new functionality
        logger.info("Testing EnhancedEdgeStrategy with new parsing...")
        strategy = EnhancedEdgeStrategy()
        
        # Mock chat_with_vectorbt to avoid actual API calls
        original_chat = chat_with_vectorbt
        
        def mock_chat_with_vectorbt(*args, **kwargs):
            return json.dumps({
                "parameter_suggestions": {
                    "rsi_window": {"current": 14, "suggested": 10, "explanation": "Better for crypto"},
                    "bb_window": {"current": 20, "suggested": 18, "explanation": "More responsive"}
                }
            })
        
        # Replace chat function
        from scripts.strategies.edge_strategy_assistant import chat_with_vectorbt as module_chat
        setattr(sys.modules["scripts.strategies.edge_strategy_assistant"], "chat_with_vectorbt", mock_chat_with_vectorbt)
        
        # Test suggestion method
        suggestions = strategy.get_parameter_suggestions()
        strategy_enhancement_works = (
            isinstance(suggestions, dict) and 
            "parameter_suggestions" in suggestions and 
            isinstance(suggestions["parameter_suggestions"], dict)
        )
        
        # Restore original function
        setattr(sys.modules["scripts.strategies.edge_strategy_assistant"], "chat_with_vectorbt", original_chat)
        
        logger.info(f"Strategy enhancement test {'PASSED' if strategy_enhancement_works else 'FAILED'}")
        
        # Overall results
        all_tests_passed = all([
            cache_working,
            json_parsing_works,
            rate_limiter_works,
            task_creation_works,
            strategy_enhancement_works
        ])
        
        if all_tests_passed:
            logger.info("✅ All enhancement tests PASSED!")
        else:
            logger.warning("⚠️ Some enhancement tests FAILED")
        
        return all_tests_passed
    
    except Exception as e:
        logger.error(f"Test FAILED with error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_enhancements()
    sys.exit(0 if success else 1) 