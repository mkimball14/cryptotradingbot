#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the improved data fetcher with JWT authentication
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to ensure imports work correctly
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(parent_dir, "test_data_fetcher.log"))
    ]
)
logger = logging.getLogger(__name__)

# Import data fetcher module
from data.data_fetcher import fetch_historical_data, get_vbt_freq_str

def test_data_fetcher_with_jwt():
    """
    Test the data fetcher with JWT authentication
    """
    # Test parameters
    product_id = "BTC-USD"
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Test different granularities
    test_granularities = [
        86400,  # 1 day - directly supported
        14400,  # 4 hours - requires resampling
        3600,   # 1 hour - directly supported
    ]
    
    results = {}
    
    for granularity in test_granularities:
        logger.info(f"Testing data fetcher with {granularity} seconds granularity ({get_vbt_freq_str(granularity)})")
        
        # Fetch data
        df = fetch_historical_data(
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity
        )
        
        # Check results
        if df is not None and not df.empty:
            logger.info(f"Successfully fetched data with shape: {df.shape}")
            logger.info(f"Date range: {df.index.min()} to {df.index.max()}")
            logger.info(f"Price range: {df['close'].min()} to {df['close'].max()}")
            results[granularity] = {
                "success": True,
                "rows": len(df),
                "start": df.index.min().strftime('%Y-%m-%d'),
                "end": df.index.max().strftime('%Y-%m-%d')
            }
        else:
            logger.error(f"Failed to fetch data for granularity {granularity}")
            results[granularity] = {
                "success": False
            }
    
    # Print summary
    logger.info("=== Test Results Summary ===")
    for granularity, result in results.items():
        status = "✅ Success" if result["success"] else "❌ Failure"
        logger.info(f"Granularity {granularity}s ({get_vbt_freq_str(granularity)}): {status}")
        if result["success"]:
            logger.info(f"  - Rows: {result['rows']}")
            logger.info(f"  - Period: {result['start']} to {result['end']}")
    
    return results

if __name__ == "__main__":
    logger.info("Starting data fetcher JWT authentication test")
    results = test_data_fetcher_with_jwt()
    logger.info("Completed data fetcher JWT authentication test") 