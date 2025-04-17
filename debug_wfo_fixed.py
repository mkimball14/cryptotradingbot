#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def run_debug():
    try:
        start_time = time.time()
        logging.info("Starting WFO debugger script")
        
        # Add the project root to the Python path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Import WFO module
        logging.info("Importing wfo_edge_strategy module")
        from scripts.strategies import wfo_edge_strategy
        
        # Set debug parameters
        symbol = "BTC/USD"
        timeframe = "1d"
        n_trials = 5  # Small number for quick testing
        
        # Define a simple progress callback
        def progress_callback(progress):
            logging.info(f"Optimization progress: {progress}%")
        
        # Run the optimization with a small number of trials first for debugging
        logging.info(f"Running walk-forward optimization for {symbol} on {timeframe} timeframe with {n_trials} trials")
        results = wfo_edge_strategy.run_walk_forward_optimization(
            symbol=symbol,
            timeframe=timeframe,
            n_trials=n_trials,
            in_sample_size=180,  # 6 months
            out_sample_size=30,  # 1 month
            n_windows=2,  # Just test 2 windows for debugging
            progress_callback=progress_callback,
            debug=True
        )
        
        # Log results summary
        logging.info("Optimization completed successfully")
        logging.info(f"Results contain {len(results)} windows")
        for i, window in enumerate(results):
            logging.info(f"Window {i+1}: Score: {window['score']:.4f}, "
                       f"IS Return: {window['in_sample_return']:.4f}, "
                       f"OOS Return: {window['out_of_sample_return']:.4f}")
        
        elapsed_time = time.time() - start_time
        logging.info(f"Total execution time: {elapsed_time:.2f} seconds")
        
        return True, results
        
    except Exception as e:
        logging.error(f"Error running walk-forward optimization: {str(e)}")
        logging.error(traceback.format_exc())
        return False, None

if __name__ == "__main__":
    success, results = run_debug()
    sys.exit(0 if success else 1) 