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
logger = logging.getLogger("test_end_to_end")

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Load environment variables
load_dotenv(verbose=True)
logger.info("Environment variables loaded")

def test_end_to_end_workflow():
    """Test the entire workflow from AI optimization to strategy performance"""
    try:
        logger.info("Starting end-to-end test of enhanced AI trading system")
        
        # 1. Import necessary components
        logger.info("Importing system components")
        from scripts.strategies.edge_strategy_assistant import EnhancedEdgeStrategy
        from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
        
        # Try to import the data fetcher, with a fallback implementation if not available
        try:
            from scripts.data.fetch_data import fetch_historical_prices
        except ImportError:
            logger.warning("Could not import fetch_data module, using fallback implementation")
            
            # Fallback implementation for fetching data
            def fetch_historical_prices(symbol, start_date, end_date, granularity=86400):
                """Fallback implementation to fetch historical prices"""
                import pandas as pd
                import numpy as np
                import requests
                from datetime import datetime, timedelta
                
                logger.info(f"Fetching data for {symbol} from {start_date} to {end_date} (fallback)")
                
                # Convert dates to timestamps
                start_ts = int(pd.Timestamp(start_date).timestamp())
                end_ts = int(pd.Timestamp(end_date).timestamp())
                
                # Calculate number of days
                days = (pd.Timestamp(end_date) - pd.Timestamp(start_date)).days
                
                # If granularity is in seconds, convert to days for our estimate
                candle_count = max(10, int(days * 86400 / granularity))
                logger.info(f"Expecting approximately {candle_count} candles")
                
                # Try to get data from Coinbase API
                url = f"https://api.exchange.coinbase.com/products/{symbol}/candles"
                params = {
                    "start": pd.Timestamp(start_date).isoformat(),
                    "end": pd.Timestamp(end_date).isoformat(),
                    "granularity": granularity
                }
                
                try:
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        # Coinbase returns: [timestamp, price_low, price_high, price_open, price_close, volume]
                        data = response.json()
                        df = pd.DataFrame(data, columns=["timestamp", "low", "high", "open", "close", "volume"])
                        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
                        df.set_index("timestamp", inplace=True)
                        df.sort_index(inplace=True)
                        logger.info(f"Successfully fetched {len(df)} data points from Coinbase API")
                        return df
                    else:
                        logger.warning(f"API request failed: {response.status_code} - {response.text}")
                except Exception as e:
                    logger.warning(f"Error fetching data from API: {e}")
                
                # Fallback to generating synthetic data
                logger.warning("Using synthetic data as fallback")
                
                # Generate dates
                dates = pd.date_range(start=start_date, end=end_date, freq='D')
                
                # Generate synthetic price data with some randomness and trend
                base_price = 20000  # Starting price for BTC
                if "BTC" in symbol:
                    base_price = 20000
                elif "ETH" in symbol:
                    base_price = 1500
                else:
                    base_price = 100
                
                # Create a trend with some randomness
                np.random.seed(42)  # For reproducibility
                random_walk = np.random.normal(0, 1, size=len(dates))
                cumulative_returns = np.cumsum(random_walk) * 0.01
                trend_factor = np.linspace(0, 0.2, len(dates))  # Upward trend
                price_multiplier = 1 + cumulative_returns + trend_factor
                
                # Generate OHLCV data
                close_prices = base_price * price_multiplier
                
                # Add some randomness to open, high, low prices
                open_prices = close_prices * np.random.uniform(0.98, 1.02, size=len(dates))
                high_prices = np.maximum(open_prices, close_prices) * np.random.uniform(1.001, 1.02, size=len(dates))
                low_prices = np.minimum(open_prices, close_prices) * np.random.uniform(0.98, 0.999, size=len(dates))
                volume = np.random.uniform(100, 1000, size=len(dates)) * base_price / 1000
                
                # Create DataFrame
                df = pd.DataFrame({
                    'open': open_prices,
                    'high': high_prices,
                    'low': low_prices,
                    'close': close_prices,
                    'volume': volume
                }, index=dates)
                
                logger.info(f"Generated synthetic data with {len(df)} data points")
                return df
        
        # 2. Fetch historical data for testing
        logger.info("Fetching historical price data for BTC-USD")
        start_date = "2023-01-01"
        end_date = "2023-04-30"
        data = fetch_historical_prices('BTC-USD', start_date, end_date, granularity=86400)  # Daily data
        logger.info(f"Fetched {len(data)} data points from {start_date} to {end_date}")
        
        # Save sample of data for reference
        logger.info(f"Data sample: \n{data.head()}")
        logger.info(f"Data columns: {data.columns.tolist()}")
        
        # 3. Create baseline strategy with default parameters
        logger.info("Creating baseline strategy with default parameters")
        baseline_strategy = EdgeMultiFactorStrategy()
        logger.info(f"Baseline strategy parameters: RSI window={baseline_strategy.lookback_window}, "
                   f"Vol window={baseline_strategy.vol_filter_window}, "
                   f"Vol threshold={baseline_strategy.volatility_threshold}")
        
        # 4. Run baseline strategy backtest
        logger.info("Running baseline backtest")
        try:
            import vectorbtpro as vbt
            logger.info("Using VectorBT Pro for backtesting")
        except ImportError:
            logger.error("VectorBT Pro is required but not available")
            raise ImportError("VectorBT Pro is required for this test")
        
        # Generate signals from baseline strategy
        logger.info("Generating signals from baseline strategy")
        long_entries, short_entries, is_trending, is_ranging = baseline_strategy.generate_signals(data)
        logger.info(f"Generated {long_entries.sum()} long entries and {short_entries.sum()} short entries")
        logger.info(f"Trending periods: {is_trending.sum()} days, Ranging periods: {is_ranging.sum()} days")
        
        # Create baseline portfolio
        logger.info("Creating baseline portfolio")
        baseline_pf = vbt.Portfolio.from_signals(
            data['close'], 
            entries=long_entries,
            exits=None,
            short_entries=short_entries,
            short_exits=None,
            sl_stop=0.02,  # 2% stop loss
            tp_stop=0.04,  # 4% take profit
            freq='1D',
            init_cash=10000
        )
        
        # Calculate baseline metrics
        logger.info("Calculating baseline performance metrics")
        baseline_metrics = {
            "total_return": float(baseline_pf.total_return),
            "sharpe_ratio": float(baseline_pf.sharpe_ratio),
            "max_drawdown": float(baseline_pf.max_drawdown),
            "win_rate": float(baseline_pf.trades.win_rate) if hasattr(baseline_pf.trades, 'win_rate') else 0,
            "num_trades": len(baseline_pf.trades)
        }
        
        logger.info(f"Baseline performance: {json.dumps(baseline_metrics, indent=2)}")
        
        # 5. Initialize enhanced strategy with AI assistant
        logger.info("Creating enhanced strategy with AI assistant")
        enhanced_strategy = EnhancedEdgeStrategy()
        
        # 6. Get AI parameter suggestions (using caching)
        logger.info("Getting AI parameter suggestions")
        suggestions = enhanced_strategy.get_parameter_suggestions()
        logger.info(f"AI suggested parameter changes: {json.dumps(suggestions, indent=2)}")
        
        # 7. Apply suggestions to create optimized strategy
        logger.info("Applying AI suggestions to strategy parameters")
        optimized_strategy = EdgeMultiFactorStrategy()
        
        parameter_changes = {}
        
        # Define parameter name mappings (AI suggestion names to actual class parameter names)
        parameter_mappings = {
            "RSI Window": "lookback_window",
            "Volatility Window (ATR)": "vol_filter_window",
            "Volatility Threshold": "volatility_threshold",
            "lookback_window": "lookback_window",
            "vol_filter_window": "vol_filter_window",
            "volatility_threshold": "volatility_threshold"
        }
        
        # Debug print the structure of suggestions
        logger.info("AI suggestion structure:")
        if "parameter_suggestions" in suggestions:
            logger.info("Found 'parameter_suggestions' key")
        else:
            logger.info("Direct parameter suggestion format detected")
        
        # Handle the format where there's no 'parameter_suggestions' wrapper
        suggestion_dict = suggestions.get("parameter_suggestions", suggestions)
        logger.info(f"Suggestion keys: {list(suggestion_dict.keys())}")
        
        # Try different parameter access approaches since we're not sure of the exact format
        for param, details in suggestion_dict.items():
            logger.info(f"Processing parameter: {param}, type: {type(details)}")
            
            mapped_param = parameter_mappings.get(param, param)
            logger.info(f"Mapped to: {mapped_param}")
            
            if not hasattr(optimized_strategy, mapped_param):
                logger.info(f"Strategy does not have attribute: {mapped_param}")
                continue
                
            # Try different formats for the suggestions
            if isinstance(details, dict):
                # Format: {"SuggestedValue": value, "Explanation": "..."}
                if "SuggestedValue" in details:
                    original_value = getattr(optimized_strategy, mapped_param)
                    new_value = details["SuggestedValue"]
                    logger.info(f"Found SuggestedValue format: {new_value}")
                    # If the parameter is a window or similar that requires an integer, ensure it's an integer
                    if mapped_param in ['lookback_window', 'vol_filter_window'] and isinstance(new_value, float):
                        new_value = int(new_value)
                    setattr(optimized_strategy, mapped_param, new_value)
                    logger.info(f"Updated {mapped_param}: {original_value} -> {new_value}")
                    parameter_changes[mapped_param] = {"original": original_value, "new": new_value}
                # Format: {"suggested": value, "explanation": "..."}
                elif "suggested" in details:
                    original_value = getattr(optimized_strategy, mapped_param)
                    new_value = details["suggested"]
                    logger.info(f"Found suggested format: {new_value}")
                    # If the parameter is a window or similar that requires an integer, ensure it's an integer
                    if mapped_param in ['lookback_window', 'vol_filter_window'] and isinstance(new_value, float):
                        new_value = int(new_value)
                    setattr(optimized_strategy, mapped_param, new_value)
                    logger.info(f"Updated {mapped_param}: {original_value} -> {new_value}")
                    parameter_changes[mapped_param] = {"original": original_value, "new": new_value}
                # Format: {"current": old_value, "suggested": value, "explanation": "..."}
                elif "current" in details and "suggested" in details:
                    original_value = getattr(optimized_strategy, mapped_param)
                    new_value = details["suggested"]
                    logger.info(f"Found current/suggested format: {new_value}")
                    # If the parameter is a window or similar that requires an integer, ensure it's an integer
                    if mapped_param in ['lookback_window', 'vol_filter_window'] and isinstance(new_value, float):
                        new_value = int(new_value)
                    setattr(optimized_strategy, mapped_param, new_value)
                    logger.info(f"Updated {mapped_param}: {original_value} -> {new_value}")
                    parameter_changes[mapped_param] = {"original": original_value, "new": new_value}
            elif isinstance(details, (int, float)):
                # Direct value format
                original_value = getattr(optimized_strategy, mapped_param)
                logger.info(f"Found direct value format: {details}")
                # If the parameter is a window or similar that requires an integer, ensure it's an integer
                if mapped_param in ['lookback_window', 'vol_filter_window'] and isinstance(details, float):
                    details = int(details)
                setattr(optimized_strategy, mapped_param, details)
                logger.info(f"Updated {mapped_param}: {original_value} -> {details}")
                parameter_changes[mapped_param] = {"original": original_value, "new": details}
        
        logger.info(f"Applied parameters changes: {json.dumps(parameter_changes, indent=2)}")
        logger.info(f"Optimized strategy parameters: RSI window={optimized_strategy.lookback_window}, "
                   f"Vol window={optimized_strategy.vol_filter_window}, "
                   f"Vol threshold={optimized_strategy.volatility_threshold}")
        
        # 8. Run optimized strategy backtest
        logger.info("Running optimized backtest")
        opt_long_entries, opt_short_entries, opt_is_trending, opt_is_ranging = optimized_strategy.generate_signals(data)
        logger.info(f"Generated {opt_long_entries.sum()} long entries and {opt_short_entries.sum()} short entries")
        logger.info(f"Trending periods: {opt_is_trending.sum()} days, Ranging periods: {opt_is_ranging.sum()} days")
        
        # Create optimized portfolio
        optimized_pf = vbt.Portfolio.from_signals(
            data['close'], 
            entries=opt_long_entries,
            exits=None,
            short_entries=opt_short_entries,
            short_exits=None,
            sl_stop=0.02,
            tp_stop=0.04,
            freq='1D',
            init_cash=10000
        )
        
        # Calculate optimized metrics
        logger.info("Calculating optimized performance metrics")
        optimized_metrics = {
            "total_return": float(optimized_pf.total_return),
            "sharpe_ratio": float(optimized_pf.sharpe_ratio),
            "max_drawdown": float(optimized_pf.max_drawdown),
            "win_rate": float(optimized_pf.trades.win_rate) if hasattr(optimized_pf.trades, 'win_rate') else 0,
            "num_trades": len(optimized_pf.trades)
        }
        
        logger.info(f"Optimized performance: {json.dumps(optimized_metrics, indent=2)}")
        
        # 9. Compare results
        improvement = {
            "total_return_change": optimized_metrics["total_return"] - baseline_metrics["total_return"],
            "total_return_pct_change": (optimized_metrics["total_return"] / baseline_metrics["total_return"] - 1) * 100 if baseline_metrics["total_return"] != 0 else 0,
            "sharpe_ratio_change": optimized_metrics["sharpe_ratio"] - baseline_metrics["sharpe_ratio"],
            "drawdown_change": optimized_metrics["max_drawdown"] - baseline_metrics["max_drawdown"],
            "win_rate_change": optimized_metrics["win_rate"] - baseline_metrics["win_rate"],
            "trade_count_change": optimized_metrics["num_trades"] - baseline_metrics["num_trades"]
        }
        
        logger.info(f"Performance improvements: {json.dumps(improvement, indent=2)}")
        
        # 10. Analyze if the AI recommendations actually improved performance
        if improvement["total_return_change"] > 0 and improvement["sharpe_ratio_change"] > 0:
            logger.info("✅ AI optimization IMPROVED strategy performance!")
        else:
            logger.info("⚠️ AI optimization did NOT improve performance")
        
        # 11. Test AI analysis of results
        logger.info("Getting AI analysis of optimized results")
        analysis = enhanced_strategy.analyze_backtest_results(optimized_metrics)
        logger.info(f"AI analysis of results: {json.dumps(analysis, indent=2)}")
        
        return {
            "baseline": baseline_metrics,
            "optimized": optimized_metrics,
            "improvement": improvement,
            "parameter_changes": parameter_changes,
            "ai_suggestions": suggestions,
            "ai_analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"End-to-end test failed with error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Starting end-to-end test script")
    results = test_end_to_end_workflow()
    
    # Save results to file
    try:
        os.makedirs("test_results", exist_ok=True)
        output_file = "test_results/end_to_end_test.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving results: {e}")
    
    # Exit with success if no errors
    if "error" not in results:
        logger.info("Test completed successfully")
        sys.exit(0)
    else:
        logger.error(f"Test failed: {results.get('error', 'Unknown error')}")
        sys.exit(1) 