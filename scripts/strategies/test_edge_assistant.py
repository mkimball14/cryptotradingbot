#!/usr/bin/env python3
import os
import sys
import logging
import json
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_edge_assistant")

# Check for API keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not OPENAI_API_KEY and not OPENROUTER_API_KEY:
    logger.warning("Neither OPENAI_API_KEY nor OPENROUTER_API_KEY found in environment variables")
    logger.warning("Chat functionality will be limited")

# Try to import necessary modules
try:
    import vectorbtpro as vbt
    from scripts.strategies.edge_strategy_assistant import (
        EnhancedEdgeStrategy, 
        chat_with_vectorbt, 
        search_vectorbt_docs
    )
    VECTORBT_AVAILABLE = True
    logger.info("VectorBTpro successfully imported")
except ImportError as e:
    logger.warning(f"Could not import VectorBTpro: {e}")
    logger.warning("Will test without VectorBT functionality")
    VECTORBT_AVAILABLE = False

def test_chat_functionality():
    """Test the basic chat functionality"""
    logger.info("Testing basic chat functionality")
    
    # Simple test query
    test_prompt = "What are the key components of a trading strategy using RSI and Bollinger Bands?"
    
    try:
        response = chat_with_vectorbt(test_prompt)
        
        if response and len(response) > 50:
            logger.info(f"Received valid response ({len(response)} chars)")
            logger.info(f"Response snippet: {response[:100]}...")
            return True
        else:
            logger.warning(f"Response seems too short or empty: {response}")
            return False
    except Exception as e:
        logger.error(f"Error in chat functionality: {e}")
        return False

def test_search_functionality():
    """Test the search functionality"""
    logger.info("Testing search functionality")
    
    if not VECTORBT_AVAILABLE:
        logger.warning("VectorBT not available, skipping search test")
        return False
    
    try:
        # Test with simple query
        search_query = "RSI indicator settings"
        results = search_vectorbt_docs(search_query)
        
        if results and "results" in results and len(results["results"]) > 0:
            logger.info(f"Search returned {len(results['results'])} results")
            return True
        else:
            logger.warning(f"Search returned no results: {results}")
            return False
    except Exception as e:
        logger.error(f"Error in search functionality: {e}")
        return False

def test_enhanced_strategy_creation():
    """Test creating an EnhancedEdgeStrategy"""
    logger.info("Testing EnhancedEdgeStrategy creation")
    
    if not VECTORBT_AVAILABLE:
        logger.warning("VectorBT not available, skipping strategy test")
        return False
    
    try:
        # Create strategy with default parameters
        strategy = EnhancedEdgeStrategy()
        
        # Check if basic attributes are set
        attributes = [
            "rsi_window", "rsi_entry", "rsi_exit", 
            "bb_window", "bb_dev", 
            "vol_window", "vol_threshold",
            "sl_pct", "tp_pct", "risk_per_trade"
        ]
        
        missing_attrs = [attr for attr in attributes if not hasattr(strategy, attr)]
        
        if not missing_attrs:
            logger.info("Successfully created EnhancedEdgeStrategy with all required attributes")
            logger.info(f"Strategy parameters: RSI({strategy.rsi_window}, {strategy.rsi_entry}, {strategy.rsi_exit}), BB({strategy.bb_window}, {strategy.bb_dev})")
            return True
        else:
            logger.warning(f"Strategy missing attributes: {missing_attrs}")
            return False
    except Exception as e:
        logger.error(f"Error creating EnhancedEdgeStrategy: {e}")
        return False

def test_parameter_suggestions():
    """Test getting parameter suggestions from the strategy"""
    logger.info("Testing parameter suggestions")
    
    if not VECTORBT_AVAILABLE:
        logger.warning("VectorBT not available, skipping parameter suggestions test")
        return False
    
    try:
        # Create strategy
        strategy = EnhancedEdgeStrategy()
        
        # Get parameter suggestions
        suggestions = strategy.get_parameter_suggestions()
        
        if suggestions:
            logger.info("Successfully received parameter suggestions")
            logger.info(f"Suggestions type: {type(suggestions)}")
            
            # Print first few keys
            if isinstance(suggestions, dict):
                logger.info(f"Suggestion keys: {list(suggestions.keys())[:5]}")
            
            return True
        else:
            logger.warning("Received empty parameter suggestions")
            return False
    except Exception as e:
        logger.error(f"Error getting parameter suggestions: {e}")
        return False

def test_market_condition_optimization():
    """Test optimizing for specific market conditions"""
    logger.info("Testing market condition optimization")
    
    if not VECTORBT_AVAILABLE:
        logger.warning("VectorBT not available, skipping market condition optimization test")
        return False
    
    try:
        # Create strategy
        strategy = EnhancedEdgeStrategy()
        
        # Get optimizations for trending market
        trending_opts = strategy.optimize_for_market_condition("trending")
        
        if trending_opts:
            logger.info("Successfully received trending market optimization")
            logger.info(f"Optimization type: {type(trending_opts)}")
            
            # Print first few keys
            if isinstance(trending_opts, dict):
                logger.info(f"Optimization keys: {list(trending_opts.keys())[:5]}")
            
            return True
        else:
            logger.warning("Received empty trending market optimization")
            return False
    except Exception as e:
        logger.error(f"Error optimizing for market condition: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    logger.info("Starting EdgeStrategyAssistant tests")
    
    # Store test results
    results = {
        "chat_functionality": test_chat_functionality(),
        "search_functionality": test_search_functionality() if VECTORBT_AVAILABLE else "SKIPPED",
        "enhanced_strategy_creation": test_enhanced_strategy_creation() if VECTORBT_AVAILABLE else "SKIPPED",
        "parameter_suggestions": test_parameter_suggestions() if VECTORBT_AVAILABLE else "SKIPPED",
        "market_condition_optimization": test_market_condition_optimization() if VECTORBT_AVAILABLE else "SKIPPED"
    }
    
    # Calculate success rate
    success_count = sum(1 for result in results.values() if result is True)
    total_tests = sum(1 for result in results.values() if result != "SKIPPED")
    
    if total_tests > 0:
        success_rate = (success_count / total_tests) * 100
    else:
        success_rate = 0
    
    # Print summary
    logger.info("==== TEST RESULTS SUMMARY ====")
    for test_name, result in results.items():
        logger.info(f"{test_name}: {result}")
    
    logger.info(f"Success rate: {success_rate:.1f}% ({success_count}/{total_tests})")
    
    return results

if __name__ == "__main__":
    run_all_tests() 