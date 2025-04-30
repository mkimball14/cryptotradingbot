#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Regime-Aware Parameter Adaptation Evaluation Runner

This script executes the comprehensive evaluation framework for testing
the regime-aware parameter adaptation system across multiple assets 
and timeframes.

Author: Max Kimball  
Date: 2025-04-30
"""

import os
import sys
import logging
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the evaluation modules
from scripts.strategies.refactored_edge.regime_evaluation import run_comparative_evaluation
from scripts.strategies.refactored_edge.test_regime_detection import create_synthetic_data
from scripts.strategies.refactored_edge.wfo_utils import ensure_output_dir

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/regime_evaluation_{datetime.now().strftime('%Y%m%d_%H%M')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("regime_evaluation_runner")

def ensure_dirs_exist():
    """Create necessary directories."""
    # Use the utility function from wfo_utils
    ensure_output_dir('logs')
    ensure_output_dir('data/results/regime_evaluation')

def create_synthetic_data_for_evaluation(days=100):
    """Create synthetic data for evaluation."""
    df = create_synthetic_data(days=days)
    return df

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run regime-aware parameter adaptation evaluation')
    
    parser.add_argument('--symbols', nargs='+', default=['BTC-USD', 'ETH-USD', 'SOL-USD'],
                        help='Trading symbols to test (default: BTC-USD ETH-USD SOL-USD)')
    
    parser.add_argument('--timeframes', nargs='+', default=['1h', '4h', '1d'],
                        help='Timeframes to test (default: 1h 4h 1d)')
    
    parser.add_argument('--start-date', type=str, default='2022-01-01',
                        help='Start date for evaluation (default: 2022-01-01)')
    
    parser.add_argument('--end-date', type=str, default='2025-04-15',
                        help='End date for evaluation (default: 2025-04-15)')
    
    parser.add_argument('--train-ratio', type=float, default=0.7, 
                        help='Proportion of data used for training')
    
    parser.add_argument('--capital', type=float, default=10000,
                        help='Initial capital for testing (default: 10000)')
    
    parser.add_argument('--quick-test', action='store_true',
                        help='Run a quick test with synthetic data and fewer splits')
    
    parser.add_argument('--synthetic', action='store_true',
                        help='Use synthetic data instead of fetching real data')
    
    return parser.parse_args()

def main():
    """Main execution function."""
    # Ensure necessary directories exist
    ensure_dirs_exist()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # If quick test mode, override with minimal settings
    if args.quick_test:
        args.symbols = ['SYNTHETIC']
        args.timeframes = ['1h']
        args.synthetic = True
        # Set environment variable for testing mode
        os.environ['REGIME_TESTING_MODE'] = 'True'
        logger.info("Running in quick test mode with synthetic data and 1h timeframe only - TESTING MODE ENABLED")
    
    # Log the settings
    logger.info(f"Starting regime evaluation with the following settings:")
    logger.info(f"Symbols: {args.symbols}")
    logger.info(f"Timeframes: {args.timeframes}")
    logger.info(f"Date range: {args.start_date} to {args.end_date}")
    logger.info(f"Initial capital: ${args.capital}")
    
    # Run the evaluation
    start_time = datetime.now()
    logger.info(f"Evaluation started at {start_time}")
    
    try:
        # Update the regime_evaluation module's constants with our arguments
        import scripts.strategies.refactored_edge.regime_evaluation as re
        re.SYMBOLS = args.symbols
        re.TIMEFRAMES = args.timeframes
        re.START_DATE = args.start_date
        re.END_DATE = args.end_date
        re.INITIAL_CAPITAL = args.capital
        
        # Run the evaluation
        if args.synthetic or 'SYNTHETIC' in args.symbols:
            data = create_synthetic_data_for_evaluation()
            results = run_comparative_evaluation(data=data)
        else:
            results = run_comparative_evaluation()
        
        # Log completion
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Evaluation completed at {end_time}")
        logger.info(f"Total duration: {duration}")
        logger.info(f"Results saved to: {re.RESULTS_DIR}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error during evaluation: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    main()
