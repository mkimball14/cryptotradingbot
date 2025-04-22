#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_enhanced_parameters")

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Load environment variables
load_dotenv(verbose=True)
logger.info("Environment variables loaded")

# Import necessary modules
try:
    from scripts.strategies.enhanced_parameter_suggestions import (
        get_enhanced_market_context,
        get_parameter_suggestions_with_context,
        validate_performance_impact,
        test_parameter_suggestions_with_backtest,
        validate_parameter_relationships,
        PARAMETER_RELATIONSHIPS
    )
    from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
    from scripts.strategies.edge_strategy_assistant import EnhancedEdgeStrategy
    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    IMPORTS_AVAILABLE = False

def test_enhanced_parameter_workflow():
    """
    Test the enhanced parameter suggestion workflow with backtest validation
    """
    if not IMPORTS_AVAILABLE:
        logger.error("Required imports not available")
        return {"error": "Required imports not available"}
    
    try:
        logger.info("Starting enhanced parameter suggestion test")
        
        # 1. Get enhanced market context
        logger.info("Getting enhanced market context")
        market_context = get_enhanced_market_context("BTC-USD", 60)
        
        if "error" in market_context:
            logger.error(f"Error getting market context: {market_context['error']}")
            return {"error": market_context["error"]}
        
        market_regime = market_context.get("market_regime", "unknown")
        logger.info(f"Identified market regime: {market_regime}")
        
        # 2. Get parameter suggestions with context
        logger.info("Getting parameter suggestions with enhanced context")
        suggestions_result = get_parameter_suggestions_with_context()
        
        if "error" in suggestions_result:
            logger.error(f"Error getting suggestions: {suggestions_result['error']}")
            return {"error": suggestions_result["error"]}
        
        validated_params = suggestions_result.get("validation_result", {}).get("validated_parameters", {})
        adjustments = suggestions_result.get("validation_result", {}).get("adjustments", [])
        
        logger.info(f"Received {len(validated_params)} validated parameters")
        if adjustments:
            logger.info(f"Made {len(adjustments)} parameter adjustments to comply with constraints")
            for adj in adjustments:
                logger.info(f"  - {adj['parameter']}: {adj['original_suggestion']} → {adj['adjusted_value']} ({adj['reason']})")
        
        # 3. Run full backtest
        logger.info("Running full backtest with validated parameters")
        backtest_result = test_parameter_suggestions_with_backtest()
        
        if "error" in backtest_result:
            logger.error(f"Error in backtest: {backtest_result['error']}")
            return {"error": backtest_result["error"]}
        
        # 4. Analyze performance impact
        baseline_metrics = backtest_result.get("baseline_metrics", {})
        optimized_metrics = backtest_result.get("optimized_metrics", {})
        performance_analysis = backtest_result.get("performance_analysis", {})
        is_improved = backtest_result.get("is_improved", False)
        
        logger.info("\n=== Performance Comparison ===")
        logger.info(f"Market Regime: {market_regime}")
        logger.info(f"Baseline Total Return: {baseline_metrics.get('total_return', 0) * 100:.2f}%")
        logger.info(f"Optimized Total Return: {optimized_metrics.get('total_return', 0) * 100:.2f}%")
        logger.info(f"Return Change: {performance_analysis.get('changes', {}).get('total_return_change', 0) * 100:.2f}%")
        logger.info(f"Baseline Sharpe Ratio: {baseline_metrics.get('sharpe_ratio', 0):.2f}")
        logger.info(f"Optimized Sharpe Ratio: {optimized_metrics.get('sharpe_ratio', 0):.2f}")
        logger.info(f"Sharpe Ratio Change: {performance_analysis.get('changes', {}).get('sharpe_ratio_change', 0):.2f}")
        logger.info(f"Baseline Win Rate: {baseline_metrics.get('win_rate', 0) * 100:.2f}%")
        logger.info(f"Optimized Win Rate: {optimized_metrics.get('win_rate', 0) * 100:.2f}%")
        logger.info(f"Win Rate Change: {performance_analysis.get('changes', {}).get('win_rate_change', 0) * 100:.2f}%")
        
        if is_improved:
            logger.info("✅ AI optimization IMPROVED strategy performance!")
        else:
            logger.info("⚠️ AI optimization did NOT improve performance")
            
            # If not improved, get the recommendation
            if "recommendation" in backtest_result:
                logger.info(f"Recommendation: {backtest_result['recommendation']}")
        
        # 5. Save results to file
        try:
            os.makedirs("analysis_results", exist_ok=True)
            result_file = "analysis_results/enhanced_parameter_test_results.json"
            with open(result_file, "w") as f:
                json.dump(backtest_result, f, indent=2)
            logger.info(f"Results saved to {result_file}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
        
        return backtest_result
    
    except Exception as e:
        logger.error(f"Error in enhanced parameter workflow: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def compare_with_standard_workflow():
    """
    Compare enhanced parameter workflow with the standard workflow
    """
    if not IMPORTS_AVAILABLE:
        logger.error("Required imports not available")
        return {"error": "Required imports not available"}
    
    try:
        logger.info("Starting comparison of enhanced vs standard parameter suggestions")
        
        # Import standard workflow
        from scripts.test_end_to_end import test_end_to_end_workflow
        
        # 1. Run standard workflow
        logger.info("Running standard parameter suggestion workflow")
        standard_results = test_end_to_end_workflow()
        
        if "error" in standard_results:
            logger.error(f"Error in standard workflow: {standard_results['error']}")
            return {"error": standard_results["error"]}
        
        # 2. Run enhanced workflow
        logger.info("Running enhanced parameter suggestion workflow")
        enhanced_results = test_enhanced_parameter_workflow()
        
        if "error" in enhanced_results:
            logger.error(f"Error in enhanced workflow: {enhanced_results['error']}")
            return {"error": enhanced_results["error"]}
        
        # 3. Compare results
        standard_baseline = standard_results.get("baseline", {})
        standard_optimized = standard_results.get("optimized", {})
        standard_improvement = standard_results.get("improvement", {})
        
        enhanced_baseline = enhanced_results.get("baseline_metrics", {})
        enhanced_optimized = enhanced_results.get("optimized_metrics", {})
        enhanced_improvement = enhanced_results.get("performance_analysis", {}).get("changes", {})
        
        # 4. Calculate which approach was better
        standard_total_return_change = standard_improvement.get("total_return_change", 0)
        enhanced_total_return_change = enhanced_improvement.get("total_return_change", 0)
        
        standard_sharpe_change = standard_improvement.get("sharpe_ratio_change", 0)
        enhanced_sharpe_change = enhanced_improvement.get("sharpe_ratio_change", 0)
        
        standard_win_rate_change = standard_improvement.get("win_rate_change", 0)
        enhanced_win_rate_change = enhanced_improvement.get("win_rate_change", 0)
        
        # 5. Determine overall winner
        standard_score = 0
        enhanced_score = 0
        
        if standard_total_return_change > enhanced_total_return_change:
            standard_score += 1
        else:
            enhanced_score += 1
            
        if standard_sharpe_change > enhanced_sharpe_change:
            standard_score += 1
        else:
            enhanced_score += 1
            
        if standard_win_rate_change > enhanced_win_rate_change:
            standard_score += 1
        else:
            enhanced_score += 1
        
        # 6. Output comparison
        logger.info("\n=== COMPARISON RESULTS ===")
        logger.info("Standard Approach:")
        logger.info(f"  Total Return Change: {standard_total_return_change * 100:.2f}%")
        logger.info(f"  Sharpe Ratio Change: {standard_sharpe_change:.2f}")
        logger.info(f"  Win Rate Change: {standard_win_rate_change * 100:.2f}%")
        logger.info("Enhanced Approach:")
        logger.info(f"  Total Return Change: {enhanced_total_return_change * 100:.2f}%")
        logger.info(f"  Sharpe Ratio Change: {enhanced_sharpe_change:.2f}")
        logger.info(f"  Win Rate Change: {enhanced_win_rate_change * 100:.2f}%")
        
        logger.info(f"WINNER: {'Enhanced Approach' if enhanced_score > standard_score else 'Standard Approach'} ({enhanced_score} vs {standard_score})")
        
        # 7. Save comparison to file
        comparison_result = {
            "standard_workflow": {
                "baseline": standard_baseline,
                "optimized": standard_optimized,
                "improvement": standard_improvement
            },
            "enhanced_workflow": {
                "baseline": enhanced_baseline,
                "optimized": enhanced_optimized,
                "improvement": enhanced_improvement
            },
            "comparison": {
                "standard_score": standard_score,
                "enhanced_score": enhanced_score,
                "winner": "enhanced" if enhanced_score > standard_score else "standard"
            }
        }
        
        try:
            os.makedirs("analysis_results", exist_ok=True)
            comparison_file = "analysis_results/workflow_comparison_results.json"
            with open(comparison_file, "w") as f:
                json.dump(comparison_result, f, indent=2)
            logger.info(f"Comparison saved to {comparison_file}")
        except Exception as e:
            logger.error(f"Error saving comparison: {e}")
        
        return comparison_result
        
    except Exception as e:
        logger.error(f"Error comparing workflows: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def test_parameter_relationships():
    """
    Test the parameter relationship validation functionality
    """
    if not IMPORTS_AVAILABLE:
        logger.error("Required imports not available")
        return {"error": "Required imports not available"}
    
    try:
        logger.info("Testing parameter relationship validation")
        
        # Test case 1: Valid parameters
        test_params = {
            "tp_pct": 4.0,  # 2x stop loss
            "sl_pct": 2.0,
            "rsi_exit": 70,  # 40 points higher than entry
            "rsi_entry": 30,
            "bb_window": 15,  # >75% of lookback window
            "lookback_window": 20
        }
        
        issues = validate_parameter_relationships(test_params)
        logger.info(f"Test case 1 (valid parameters): {len(issues)} issues found")
        
        # Test case 2: Invalid parameters
        invalid_params = {
            "tp_pct": 2.0,  # Only 1x stop loss (should be at least 2x)
            "sl_pct": 2.0,
            "rsi_exit": 65,  # Only 35 points higher than entry (should be at least 30)
            "rsi_entry": 30,
            "bb_window": 5,  # <75% of lookback window
            "lookback_window": 20
        }
        
        issues = validate_parameter_relationships(invalid_params)
        logger.info(f"Test case 2 (invalid parameters): {len(issues)} issues found")
        for issue in issues:
            logger.info(f"  - {issue['message']}")
        
        # Test case 3: Missing parameters
        missing_params = {
            "tp_pct": 4.0,
            # sl_pct is missing
            "rsi_exit": 70,
            "rsi_entry": 30
            # bb_window and lookback_window are missing
        }
        
        issues = validate_parameter_relationships(missing_params)
        logger.info(f"Test case 3 (missing parameters): {len(issues)} issues found")
        
        return {
            "success": True,
            "message": "Parameter relationship validation tests completed"
        }
        
    except Exception as e:
        logger.error(f"Error testing parameter relationships: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def test_enhanced_market_context():
    """
    Test the enhanced market context functionality
    """
    if not IMPORTS_AVAILABLE:
        logger.error("Required imports not available")
        return {"error": "Required imports not available"}
    
    try:
        logger.info("Testing enhanced market context")
        
        # Get market context
        market_context = get_enhanced_market_context("BTC-USD", 30)
        
        if "error" in market_context:
            logger.error(f"Error getting market context: {market_context['error']}")
            return {"error": market_context["error"]}
        
        # Log market regime detection
        market_regime = market_context.get("market_regime", "unknown")
        logger.info(f"Detected market regime: {market_regime}")
        
        # Verify new context fields
        logger.info("Checking for new context fields:")
        for field in ["support_resistance", "market_cycle"]:
            if field in market_context:
                logger.info(f"  ✅ {field}: {market_context[field]}")
            else:
                logger.warning(f"  ❌ {field} missing from context")
                
        return {
            "success": True,
            "market_regime": market_regime,
            "context_fields": list(market_context.keys())
        }
        
    except Exception as e:
        logger.error(f"Error testing enhanced market context: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def test_parameter_validation():
    """Test parameter validation with the enhanced constraints"""
    from scripts.strategies.enhanced_parameter_suggestions import validate_and_adjust_parameters
    
    # Test valid parameters
    test_params = {
        "lookback_window": 20,
        "vol_filter_window": 50,
        "volatility_threshold": 0.5,
        "rsi_window": 14,
        "rsi_entry": 30,
        "rsi_exit": 70,
        "bb_window": 20,
        "bb_dev": 2.0,
        "vol_window": 20,
        "sl_pct": 2.0,
        "tp_pct": 4.0,
        "risk_per_trade": 0.02
    }
    
    result = validate_and_adjust_parameters(test_params)
    logger.info("Valid parameters test:")
    logger.info(f"Original parameters: {test_params}")
    logger.info(f"Validated parameters: {result}")
    logger.info(f"All parameters valid: {not any(result.get('issues', []))}")
    
    # Test invalid parameters
    invalid_params = {
        "lookback_window": 5,  # Too small
        "vol_filter_window": 5,  # Too small
        "volatility_threshold": 0.1,  # Too small
        "rsi_window": 2,  # Too small
        "rsi_entry": 20,  # Too small
        "rsi_exit": 60,  # Too small
        "bb_window": 5,  # Too small
        "bb_dev": 1.0,  # Too small
        "vol_window": 5,  # Too small
        "sl_pct": 0.5,  # Too small
        "tp_pct": 1.0,  # Too small
        "risk_per_trade": 0.005  # Too small
    }
    
    result = validate_and_adjust_parameters(invalid_params)
    logger.info("\nInvalid parameters test:")
    logger.info(f"Original parameters: {invalid_params}")
    logger.info(f"Validated parameters: {result}")
    logger.info(f"Issues found: {len(result.get('issues', []))}")
    for issue in result.get('issues', []):
        logger.info(f"Issue: {issue}")
    
    return True

def test_parameter_suggestions():
    """Test parameter suggestions with enhanced context"""
    from scripts.strategies.enhanced_parameter_suggestions import get_parameter_suggestions_with_context
    
    # Test for BTC-USD
    suggestions = get_parameter_suggestions_with_context("BTC-USD")
    
    logger.info("\nParameter suggestions test:")
    if "error" in suggestions:
        logger.error(f"Error getting suggestions: {suggestions['error']}")
        return False
    
    logger.info(f"Market context: {suggestions.get('context', {}).get('market_regime')}")
    logger.info(f"Suggested parameters: {json.dumps(suggestions.get('suggested_params', {}), indent=2)}")
    
    # Check for relationship issues
    relationship_issues = suggestions.get('relationship_issues', [])
    if relationship_issues:
        logger.warning(f"Relationship issues found: {len(relationship_issues)}")
        for issue in relationship_issues:
            logger.warning(f"Issue: {issue}")
    else:
        logger.info("No relationship issues found in suggested parameters")
    
    return True

def main():
    """Main function to run the test script"""
    logger.info("Starting enhanced parameter testing")
    
    # Choose which test to run
    test_type = os.getenv("TEST_TYPE", "enhanced").lower()
    
    if test_type == "enhanced":
        logger.info("Running enhanced parameter workflow test")
        result = test_enhanced_parameter_workflow()
    elif test_type == "compare":
        logger.info("Running comparison between standard and enhanced workflows")
        result = compare_with_standard_workflow()
    elif test_type == "relationships":
        logger.info("Testing parameter relationship validation")
        result = test_parameter_relationships()
    elif test_type == "market_context":
        logger.info("Testing enhanced market context")
        result = test_enhanced_market_context()
    elif test_type == "validation":
        logger.info("Testing parameter validation")
        result = test_parameter_validation()
    elif test_type == "suggestions":
        logger.info("Testing parameter suggestions")
        result = test_parameter_suggestions()
    else:
        logger.error(f"Unknown test type: {test_type}")
        result = {"error": f"Unknown test type: {test_type}"}
    
    if "error" in result:
        logger.error(f"Test failed: {result['error']}")
        sys.exit(1)
    else:
        logger.info("Test completed successfully")
        sys.exit(0)

if __name__ == "__main__":
    main() 