#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Scheduled Optimization Script for Edge Trading Strategy

This script automatically runs optimization processes on a schedule, 
generates reports, and updates the strategy parameters based on current market conditions.
"""

import os
import sys
import logging
import time
import json
import schedule
import pandas as pd
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/scheduled_optimization_{datetime.datetime.now().strftime('%Y%m%d')}.log")
    ]
)
logger = logging.getLogger("ScheduledOptimization")

# Load environment variables
load_dotenv(verbose=True)
logger.info("Environment variables loaded")

# Ensure we can import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import required modules
try:
    from scripts.strategies.edge_strategy_assistant import EdgeStrategyAssistant, EnhancedEdgeStrategy
    logger.info("Successfully imported EdgeStrategyAssistant")
except ImportError as e:
    logger.error(f"Failed to import EdgeStrategyAssistant: {str(e)}")
    sys.exit(1)

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        "logs",
        "analysis_results",
        "analysis_results/archive"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("Ensured all required directories exist")

def archive_old_results():
    """Archive old optimization results"""
    now = datetime.datetime.now()
    archive_dir = Path("analysis_results/archive")
    
    # Move optimization files older than 7 days to archive
    results_dir = Path("analysis_results")
    for file_path in results_dir.glob("*.json"):
        if now - datetime.datetime.fromtimestamp(file_path.stat().st_mtime) > datetime.timedelta(days=7):
            target_path = archive_dir / file_path.name
            file_path.rename(target_path)
            logger.info(f"Archived old result: {file_path.name}")
    
    # Also archive old adaptive strategy files
    for file_path in results_dir.glob("adaptive_edge_strategy_*.py"):
        if now - datetime.datetime.fromtimestamp(file_path.stat().st_mtime) > datetime.timedelta(days=7):
            target_path = archive_dir / file_path.name
            file_path.rename(target_path)
            logger.info(f"Archived old strategy: {file_path.name}")

def save_latest_parameters(params, market_condition):
    """Save the latest optimized parameters"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save parameters for the specific market condition
    filename = f"analysis_results/latest_params_{market_condition}.json"
    with open(filename, "w") as f:
        json.dump(params, f, indent=4)
    logger.info(f"Saved latest parameters for {market_condition} market to {filename}")
    
    # Also save with timestamp for historical tracking
    filename_ts = f"analysis_results/params_{market_condition}_{timestamp}.json"
    with open(filename_ts, "w") as f:
        json.dump(params, f, indent=4)
    
    return filename

def run_optimization():
    """Run the optimization process"""
    logger.info("Starting scheduled optimization run")
    
    try:
        # Create strategy assistant
        assistant = EdgeStrategyAssistant()
        strategy = EnhancedEdgeStrategy()
        
        # Step 1: Load latest market data
        logger.info("Loading market data")
        data = strategy.load_data("BTC/USD", "1d", 365)
        if data is None or len(data) < 30:
            logger.error("Insufficient market data for optimization")
            return
        
        logger.info(f"Loaded {len(data)} data points")
        
        # Step 2: Analyze current market conditions
        logger.info("Analyzing market conditions")
        market_analysis = strategy.analyze_market_conditions(data)
        market_condition = market_analysis.get("market_regime", "unknown")
        logger.info(f"Current market condition: {market_condition}")
        
        # Step 3: Get optimized parameters for current market condition
        logger.info(f"Getting optimized parameters for {market_condition} market")
        optimized_params = strategy.get_parameters_for_market_condition(data, market_condition)
        
        # Step 4: Save the optimized parameters
        params_file = save_latest_parameters(optimized_params, market_condition)
        logger.info(f"Saved optimized parameters to {params_file}")
        
        # Step 5: Run backtest with optimized parameters
        logger.info("Running backtest with optimized parameters")
        backtest_results = strategy.backtest(data, optimized_params)
        
        # Step 6: Generate adaptive strategy file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        strategy_file = f"analysis_results/adaptive_edge_strategy_{timestamp}.py"
        with open(strategy_file, "w") as f:
            f.write(strategy.generate_adaptive_strategy(market_analysis, optimized_params))
        
        logger.info(f"Generated adaptive strategy file: {strategy_file}")
        
        # Step 7: Create symlink to latest strategy file
        latest_link = "analysis_results/adaptive_edge_strategy.py"
        if os.path.exists(latest_link):
            os.remove(latest_link)
        os.symlink(strategy_file, latest_link)
        
        # Step 8: Save complete analysis
        complete_analysis = {
            "timestamp": timestamp,
            "market_analysis": market_analysis,
            "optimized_parameters": optimized_params,
            "backtest_results": backtest_results,
            "strategy_file": strategy_file
        }
        
        with open(f"analysis_results/complete_strategy_optimization_{timestamp}.json", "w") as f:
            json.dump(complete_analysis, f, indent=4)
        
        logger.info(f"Saved complete analysis results")
        
        # Generate markdown report
        generate_markdown_report(complete_analysis)
        
        logger.info("Scheduled optimization completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error during optimization: {str(e)}", exc_info=True)
        return False

def generate_markdown_report(analysis):
    """Generate a markdown report of the optimization results"""
    timestamp = analysis["timestamp"]
    market_analysis = analysis["market_analysis"]
    optimized_params = analysis["optimized_parameters"]
    backtest_results = analysis["backtest_results"]
    
    # Create report content
    report = f"""# Strategy Optimization Report
*Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## Market Analysis

### Current Market Conditions (BTC-USD)
- **Current Price**: ${market_analysis.get("current_price", "N/A")}
- **% from 30-day High**: {market_analysis.get("percent_from_high", "N/A")}%
- **% from 30-day Low**: {market_analysis.get("percent_from_low", "N/A")}%
- **Annualized Volatility**: {market_analysis.get("annualized_volatility", "N/A")}%
- **RSI (14)**: {market_analysis.get("rsi_14", "N/A")}
- **Bollinger Band Width**: {market_analysis.get("bb_width", "N/A")}%
- **Volume Change**: {market_analysis.get("volume_change", "N/A")}%

### Market Regime
The current market is identified as **{market_analysis.get("market_regime", "unknown")}**

### Recommended Strategy Adjustments
"""
    
    # Add strategy adjustments
    for adjustment in market_analysis.get("strategy_adjustments", []):
        report += f"- {adjustment}\n"
    
    # Add optimized parameters section
    report += """
## Optimized Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
"""
    
    # Add parameter rows
    for param, value in optimized_params.items():
        description = ""
        if param == "rsi_window":
            description = "RSI calculation window"
        elif param == "rsi_entry":
            description = "RSI oversold threshold for entry"
        elif param == "rsi_exit":
            description = "RSI overbought threshold for exit"
        elif param == "bb_window":
            description = "Bollinger Bands calculation window"
        elif param == "bb_dev":
            description = "Bollinger Bands standard deviation"
        elif param == "vol_window":
            description = "Volatility (ATR) calculation window"
        elif param == "vol_threshold":
            description = "Volatility threshold for filtering trades"
        elif param == "sl_pct":
            description = "Stop loss percentage"
        elif param == "tp_pct":
            description = "Take profit percentage"
        elif param == "risk_per_trade":
            description = "Risk per trade as percentage of capital"
            
        report += f"| {param} | {value} | {description} |\n"
    
    # Add backtest results section
    report += """
## Backtest Results

"""
    
    for metric, value in backtest_results.items():
        report += f"- **{metric}**: {value}\n"
    
    # Write report to file
    report_file = f"analysis_results/strategy_optimization_report_{timestamp}.md"
    with open(report_file, "w") as f:
        f.write(report)
    
    logger.info(f"Generated markdown report: {report_file}")
    
    # Create symlink to latest report
    latest_link = "analysis_results/latest_optimization_report.md"
    if os.path.exists(latest_link):
        os.remove(latest_link)
    os.symlink(report_file, latest_link)

def daily_optimization():
    """Run daily optimization task"""
    logger.info("Running daily optimization task")
    ensure_directories()
    archive_old_results()
    return run_optimization()

def hourly_market_check():
    """Check market conditions hourly and run optimization if significant changes"""
    logger.info("Running hourly market check")
    
    try:
        # Create strategy to check market
        strategy = EnhancedEdgeStrategy()
        
        # Load latest market data
        data = strategy.load_data("BTC/USD", "1d", 90)
        if data is None or len(data) < 30:
            logger.error("Insufficient market data for market check")
            return
        
        # Analyze current market conditions
        market_analysis = strategy.analyze_market_conditions(data)
        current_condition = market_analysis.get("market_regime", "unknown")
        
        # Check if volatility has significantly increased
        volatility = market_analysis.get("annualized_volatility", 0)
        
        # Load last known market condition
        last_condition_file = "analysis_results/last_market_condition.json"
        last_condition = "unknown"
        last_volatility = 0
        
        if os.path.exists(last_condition_file):
            try:
                with open(last_condition_file, "r") as f:
                    last_data = json.load(f)
                    last_condition = last_data.get("market_regime", "unknown")
                    last_volatility = last_data.get("volatility", 0)
            except Exception as e:
                logger.error(f"Error reading last market condition: {str(e)}")
        
        # Save current market condition
        with open(last_condition_file, "w") as f:
            json.dump({
                "market_regime": current_condition,
                "volatility": volatility,
                "timestamp": datetime.datetime.now().isoformat()
            }, f, indent=4)
        
        # Check if we need to run optimization
        if (current_condition != last_condition) or (abs(volatility - last_volatility) > 10):
            logger.info(f"Market condition changed from {last_condition} to {current_condition} or volatility changed significantly")
            return run_optimization()
        
        logger.info(f"No significant market changes detected. Current: {current_condition}, volatility: {volatility}%")
        return False
    
    except Exception as e:
        logger.error(f"Error during hourly market check: {str(e)}", exc_info=True)
        return False

def main():
    """Main function to set up and run the scheduler"""
    logger.info("Starting scheduled optimization script")
    ensure_directories()
    
    # Run immediately on startup
    daily_optimization()
    
    # Schedule daily full optimization
    schedule.every().day.at("00:05").do(daily_optimization)
    
    # Schedule hourly market checks
    schedule.every().hour.do(hourly_market_check)
    
    logger.info("Scheduler set up. Running continuously...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for 60 seconds between checks

if __name__ == "__main__":
    main() 