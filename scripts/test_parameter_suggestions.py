#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import time
import json
from typing import Dict, Any
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('parameter_suggestions_test')

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_parameter_suggestions():
    """
    Test the enhanced parameter suggestion system
    """
    try:
        logger.info("Starting test of enhanced parameter suggestion system")
        
        # Import the parameter suggestions module
        from scripts.strategies.enhanced_parameter_suggestions import (
            get_parameter_suggestions_with_context,
            test_parameter_trade_generation,
            check_historical_performance,
            get_default_parameters
        )
        
        # Test 1: Get parameter suggestions
        logger.info("Test 1: Getting parameter suggestions for BTC-USD")
        
        # Get default parameters to start with
        current_params = get_default_parameters()
        
        # The function returns a tuple of (suggested_params, adjustment_reasons, params_changed)
        suggested_params, adjustments, params_changed = get_parameter_suggestions_with_context(
            "BTC-USD", 
            current_params=current_params
        )
        
        # Ensure all window parameters are integers to avoid type errors
        for param_name, param_value in suggested_params.items():
            if param_name.endswith('_window') and isinstance(param_value, float):
                suggested_params[param_name] = int(param_value)
                logger.info(f"Converted {param_name} from {param_value} to {int(param_value)}")
                
        # Log the suggestions
        logger.info(f"Current parameters: {json.dumps(current_params, indent=2)}")
        logger.info(f"Suggested parameters: {json.dumps(suggested_params, indent=2)}")
        logger.info("Parameter adjustments:")
        for adj in adjustments:
            logger.info(f"- {adj}")
        
        # Test 2: Test trade generation
        logger.info("\nTest 2: Testing trade generation with suggested parameters")
        
        # Set date range for testing
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Test trade generation with the correct function signature
        trades_count, updated_params = test_parameter_trade_generation(
            market="BTC-USD",
            parameters=suggested_params,
            start_date=start_date,
            end_date=end_date,
            granularity="ONE_DAY"
        )
        
        logger.info(f"Trade generation test: {trades_count} trades would be generated")
        if trades_count < 2:
            logger.warning("Very few trades would be generated with these parameters")
        
        # Test 3: Run backtest comparison
        logger.info("\nTest 3: Running backtest comparison")
        
        try:
            # Run historical performance check on both baseline and optimized parameters
            logger.info("Running historical performance check on baseline parameters")
            baseline_result = check_historical_performance("BTC-USD", current_params, lookback_days=90)
            
            logger.info("Running historical performance check on optimized parameters")
            optimized_result = check_historical_performance("BTC-USD", updated_params, lookback_days=90)
            
            # Extract metrics
            baseline_metrics = baseline_result.get("metrics", {})
            optimized_metrics = optimized_result.get("metrics", {})
            
            # Compare performance metrics
            logger.info("\n=== Performance Comparison ===")
            logger.info(f"Baseline Metrics:")
            logger.info(f"- Total Return: {baseline_metrics.get('total_return', 0) * 100:.2f}%")
            logger.info(f"- Sharpe Ratio: {baseline_metrics.get('sharpe_ratio', 0):.2f}")
            logger.info(f"- Max Drawdown: {baseline_metrics.get('max_drawdown', 0) * 100:.2f}%")
            logger.info(f"- Win Rate: {baseline_metrics.get('win_rate', 0) * 100:.2f}%")
            logger.info(f"- Trades: {baseline_metrics.get('num_trades', 0)}")
            
            logger.info(f"\nOptimized Metrics:")
            logger.info(f"- Total Return: {optimized_metrics.get('total_return', 0) * 100:.2f}%")
            logger.info(f"- Sharpe Ratio: {optimized_metrics.get('sharpe_ratio', 0):.2f}")
            logger.info(f"- Max Drawdown: {optimized_metrics.get('max_drawdown', 0) * 100:.2f}%")
            logger.info(f"- Win Rate: {optimized_metrics.get('win_rate', 0) * 100:.2f}%")
            logger.info(f"- Trades: {optimized_metrics.get('num_trades', 0)}")
            
            # Check if performance improved
            total_return_improved = optimized_metrics.get('total_return', 0) > baseline_metrics.get('total_return', 0)
            sharpe_improved = optimized_metrics.get('sharpe_ratio', 0) > baseline_metrics.get('sharpe_ratio', 0)
            drawdown_improved = optimized_metrics.get('max_drawdown', 0) > baseline_metrics.get('max_drawdown', 0)
            
            is_improved = total_return_improved and sharpe_improved
            
            logger.info(f"\nPerformance improved: {is_improved}")
            
            # Test 4: Check period-by-period performance
            period_improvements = []
            baseline_periods = baseline_result.get("period_performance", [])
            optimized_periods = optimized_result.get("period_performance", [])
            
            if baseline_periods and optimized_periods:
                logger.info("\nTest 4: Period-by-period improvements")
                
                improved_periods = 0
                for i in range(min(len(baseline_periods), len(optimized_periods))):
                    baseline_period = baseline_periods[i]
                    optimized_period = optimized_periods[i]
                    
                    # Calculate improvements for this period
                    return_change = optimized_period.get("return", 0) - baseline_period.get("return", 0)
                    
                    period_improvements.append({
                        "period": baseline_period.get("period", f"Period {i+1}"),
                        "return_change": return_change,
                        "is_improved": return_change > 0
                    })
                    
                    if return_change > 0:
                        improved_periods += 1
                    
                    period_name = baseline_period.get("period", f"Period {i+1}")
                    return_change_pct = return_change * 100  # Convert to percentage
                    
                    logger.info(f"{period_name}: Return change {return_change_pct:.2f}% - {'Improved' if return_change > 0 else 'Not improved'}")
                
                logger.info(f"\nImproved periods: {improved_periods}/{len(period_improvements)}")
            
            logger.info("\nParameter suggestions test completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error in backtest comparison: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
        
    except Exception as e:
        logger.error(f"Error testing parameter suggestions: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = test_parameter_suggestions()
    sys.exit(0 if success else 1) 