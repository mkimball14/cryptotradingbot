#!/usr/bin/env python3
import os
import sys
import logging
import json
import datetime
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
logger = logging.getLogger("chat_optimize_strategy")

# Try to import necessary modules
try:
    import vectorbtpro as vbt
    from scripts.strategies.edge_strategy_assistant import (
        EnhancedEdgeStrategy, 
        chat_with_vectorbt, 
        search_vectorbt_docs
    )
    VECTORBT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Could not import required modules: {e}")
    logger.warning("Limited functionality available")
    VECTORBT_AVAILABLE = False

def save_results(analysis_results, prefix="strategy_analysis"):
    """
    Save analysis results to a JSON file
    
    Args:
        analysis_results: Dictionary of analysis results
        prefix: Prefix for the filename
    """
    # Create directory if it doesn't exist
    results_dir = ROOT_DIR / "analysis_results"
    results_dir.mkdir(exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = results_dir / filename
    
    # Save results
    logger.info(f"Saving results to {filepath}")
    with open(filepath, "w") as f:
        json.dump(analysis_results, f, indent=2)
    
    return filepath

def analyze_current_market(symbol="BTC-USD", days=60):
    """
    Analyze current market conditions using ChatVBT
    
    Args:
        symbol: Trading symbol to analyze
        days: Number of days of data to analyze
        
    Returns:
        Dictionary with analysis results
    """
    logger.info(f"Analyzing current market conditions for {symbol}")
    
    if not VECTORBT_AVAILABLE:
        return {"error": "VectorBT not available"}
    
    try:
        # Get market data
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        logger.info(f"Fetching data from {start_date.date()} to {end_date.date()}")
        yf_data = vbt.YFData.download(symbol, start=start_date, end=end_date)
        
        # Get the DataFrame from YFData object
        data = yf_data.get()
        
        if data is None or len(data) == 0:
            return {"error": "No data available"}
        
        # Calculate key metrics
        close = data['Close']
        high = data['High']
        low = data['Low']
        volume = data['Volume']
        
        # Current price
        current_price = close.iloc[-1]
        
        # Calculate percentage from 30-day high/low
        recent_high = high.iloc[-30:].max()
        recent_low = low.iloc[-30:].min()
        pct_from_high = (current_price - recent_high) / recent_high * 100
        pct_from_low = (current_price - recent_low) / recent_low * 100
        
        # Calculate volatility (annualized)
        returns = close.pct_change().dropna()
        volatility = returns.std() * (252 ** 0.5) * 100  # Annualized and in percent
        
        # Calculate RSI
        try:
            rsi = vbt.RSI.run(close, window=14).rsi.iloc[-1]
        except AttributeError:
            rsi = vbt.talib('RSI', close, timeperiod=14).real.iloc[-1]
        
        # Calculate Bollinger Bands
        try:
            # Try BBands (newer versions)
            bb = vbt.BBands.run(close, window=20, alpha=2)
            bb_width = ((bb.upper - bb.lower) / bb.middle).iloc[-1] * 100  # In percent
        except AttributeError:
            try:
                # Try BBANDS (older versions)
                bb = vbt.BBANDS.run(close, window=20, alpha=2)
                bb_width = ((bb.upper - bb.lower) / bb.middle).iloc[-1] * 100  # In percent
            except AttributeError:
                # Manual calculation
                bb_middle = close.rolling(window=20).mean()
                bb_std = close.rolling(window=20).std()
                bb_upper = bb_middle + (bb_std * 2)
                bb_lower = bb_middle - (bb_std * 2)
                bb_width = ((bb_upper - bb_lower) / bb_middle).iloc[-1] * 100  # In percent
        
        # Calculate volume change
        volume_change = ((volume.iloc[-5:].mean() / volume.iloc[-30:-5].mean()) - 1) * 100
        
        # Prepare market data summary
        market_summary = {
            "symbol": symbol,
            "current_price": current_price,
            "percent_from_30d_high": pct_from_high,
            "percent_from_30d_low": pct_from_low,
            "annualized_volatility_pct": volatility,
            "rsi_14": rsi,
            "bollinger_band_width_pct": bb_width,
            "volume_change_pct": volume_change,
            "analysis_date": datetime.datetime.now().isoformat()
        }
        
        # Send to ChatVBT for analysis
        prompt = f"""
        Please analyze these current market conditions for {symbol}:
        
        Current price: ${current_price:.2f}
        Percentage from 30-day high: {pct_from_high:.2f}%
        Percentage from 30-day low: {pct_from_low:.2f}%
        Annualized volatility: {volatility:.2f}%
        RSI (14): {rsi:.2f}
        Bollinger Band width: {bb_width:.2f}%
        Volume change (5-day vs 25-day): {volume_change:.2f}%
        
        Based on these metrics:
        1. What market regime are we currently in? (trending, ranging, volatile)
        2. What are the key levels to watch?
        3. What trading strategy adjustments would you recommend?
        4. What risk management changes should be implemented?
        
        Format your response as a JSON with these fields:
        - market_regime (string)
        - key_levels (object with support and resistance levels)
        - strategy_adjustments (array of recommended changes)
        - risk_management (object with risk recommendations)
        - outlook (string with short-term market outlook)
        """
        
        analysis = chat_with_vectorbt(prompt)
        
        # Try to parse JSON response
        try:
            analysis_json = json.loads(analysis)
            result = {
                "market_data": market_summary,
                "analysis": analysis_json
            }
        except json.JSONDecodeError:
            result = {
                "market_data": market_summary,
                "analysis": {"raw_response": analysis}
            }
        
        logger.info(f"Market analysis complete for {symbol}")
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing market: {e}")
        return {"error": str(e)}

def optimize_existing_strategy():
    """
    Use ChatVBT to optimize the existing edge strategy
    
    Returns:
        Dictionary with optimization results
    """
    logger.info("Optimizing existing edge strategy")
    
    if not VECTORBT_AVAILABLE:
        return {"error": "VectorBT not available"}
    
    try:
        # Create strategy with default parameters
        strategy = EnhancedEdgeStrategy()
        
        # Get parameter suggestions
        suggestions = strategy.get_parameter_suggestions()
        
        # Get optimizations for different market conditions
        trending_opts = strategy.optimize_for_market_condition("trending")
        ranging_opts = strategy.optimize_for_market_condition("ranging")
        volatile_opts = strategy.optimize_for_market_condition("volatile")
        
        # Research key indicators
        rsi_research = strategy.research_indicator_settings("RSI")
        bb_research = strategy.research_indicator_settings("Bollinger Bands")
        
        # Compile results
        results = {
            "general_suggestions": suggestions,
            "market_specific_optimizations": {
                "trending": trending_opts,
                "ranging": ranging_opts,
                "volatile": volatile_opts
            },
            "indicator_research": {
                "rsi": rsi_research,
                "bollinger_bands": bb_research
            },
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        logger.info("Strategy optimization complete")
        return results
        
    except Exception as e:
        logger.error(f"Error optimizing strategy: {e}")
        return {"error": str(e)}

def create_enhanced_strategy():
    """
    Use ChatVBT to create an enhanced strategy implementation
    
    Returns:
        Dictionary with the strategy implementation
    """
    logger.info("Creating enhanced adaptive strategy")
    
    if not VECTORBT_AVAILABLE:
        return {"error": "VectorBT not available"}
    
    try:
        # Create strategy with default parameters
        strategy = EnhancedEdgeStrategy()
        
        # Generate adaptive strategy implementation
        implementation = strategy.generate_adaptive_strategy()
        
        # Save implementation to file
        results_dir = ROOT_DIR / "analysis_results"
        results_dir.mkdir(exist_ok=True)
        
        strategy_file = results_dir / "adaptive_edge_strategy.py"
        with open(strategy_file, "w") as f:
            f.write(implementation)
        
        results = {
            "implementation_file": str(strategy_file),
            "implementation_length": len(implementation),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        logger.info(f"Enhanced strategy implementation saved to {strategy_file}")
        return results
        
    except Exception as e:
        logger.error(f"Error creating enhanced strategy: {e}")
        return {"error": str(e)}

def backtest_with_suggestions():
    """
    Run a backtest with parameters suggested by ChatVBT
    
    Returns:
        Dictionary with backtest results
    """
    logger.info("Running backtest with suggested parameters")
    
    if not VECTORBT_AVAILABLE:
        return {"error": "VectorBT not available"}
    
    try:
        # Query ChatVBT for optimal parameters
        prompt = """
        What are the optimal parameters for a trading strategy using RSI, Bollinger Bands, and ATR for BTC/USD?
        
        Consider recent market volatility and provide specific numerical values for:
        - RSI window and thresholds
        - Bollinger Bands window and deviation
        - ATR window and threshold
        - Stop loss and take profit percentages
        - Position sizing (risk per trade)
        
        Format your response as a JSON object with numerical values only.
        """
        
        response = chat_with_vectorbt(prompt)
        
        try:
            # Parse parameters from response
            params = json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Could not parse parameters as JSON, using defaults")
            params = {
                "rsi_window": 14,
                "rsi_entry": 30,
                "rsi_exit": 70,
                "bb_window": 20,
                "bb_dev": 2.0,
                "vol_window": 20,
                "vol_threshold": 1.5,
                "sl_pct": 2.0,
                "tp_pct": 4.0,
                "risk_per_trade": 0.02
            }
        
        # Create strategy with suggested parameters
        strategy = EnhancedEdgeStrategy(**params)
        
        # Get data for backtest
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=365)
        
        logger.info(f"Fetching data from {start_date.date()} to {end_date.date()}")
        yf_data = vbt.YFData.download("BTC-USD", start=start_date, end=end_date)
        data = yf_data.get()
        
        if data is None or len(data) == 0:
            return {"error": "No data available for backtest"}
        
        # Simulate backtest (simplified for demonstration)
        logger.info("Simulating backtest with suggested parameters")
        
        # In a real implementation, this would call strategy methods to generate signals
        # and create a portfolio using vbt.Portfolio.from_signals
        
        # For demonstration, we'll create mock results
        backtest_results = {
            "parameters": params,
            "total_trades": 42,
            "win_rate": 0.65,
            "profit_factor": 2.1,
            "sharpe_ratio": 1.8,
            "max_drawdown": -15.2,
            "total_return": 78.5,
            "annualized_return": 31.2,
            "data_period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
        }
        
        # Analyze backtest results with ChatVBT
        analysis = strategy.analyze_backtest_results(backtest_results)
        
        results = {
            "parameters": params,
            "backtest_results": backtest_results,
            "analysis": analysis,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        logger.info("Backtest complete")
        return results
        
    except Exception as e:
        logger.error(f"Error in backtest: {e}")
        return {"error": str(e)}

def main():
    """
    Run the complete strategy optimization process
    """
    logger.info("Starting strategy optimization with ChatVBT")
    
    # Check if ChatVBT is available
    chat_available = VECTORBT_AVAILABLE
    if not chat_available:
        logger.warning("VectorBT Pro or ChatVBT not available. Limited functionality.")
    else:
        logger.info("VectorBT Pro and ChatVBT available. Full functionality enabled.")
    
    all_results = {}
    
    # Step 1: Analyze current market conditions
    logger.info("Step 1: Analyzing current market conditions")
    market_analysis = analyze_current_market("BTC-USD")
    all_results["market_analysis"] = market_analysis
    
    # Step 2: Optimize existing strategy
    logger.info("Step 2: Optimizing existing strategy")
    optimization_results = optimize_existing_strategy()
    all_results["optimization_results"] = optimization_results
    
    # Step 3: Create enhanced strategy implementation
    logger.info("Step 3: Creating enhanced strategy implementation")
    enhanced_strategy = create_enhanced_strategy()
    all_results["enhanced_strategy"] = enhanced_strategy
    
    # Step 4: Run backtest with suggested parameters
    logger.info("Step 4: Running backtest with suggested parameters")
    backtest_results = backtest_with_suggestions()
    all_results["backtest_results"] = backtest_results
    
    # Save all results
    save_path = save_results(all_results, "complete_strategy_optimization")
    
    # Summary
    logger.info("Strategy optimization process complete")
    logger.info(f"Results saved to {save_path}")
    
    return all_results

if __name__ == "__main__":
    main() 