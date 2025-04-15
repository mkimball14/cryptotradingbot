#!/usr/bin/env python

import os
import re
import glob
from pathlib import Path
from collections import defaultdict
import argparse
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_html_filename(filename):
    """Parse the HTML filename to extract strategy info."""
    # Example patterns:
    # manual_stoch_sma_wfo_oos_sharpe_ratio_1H_SL1.5_TSL2.5_SMA50_BTC-USD.html
    # manual_rsi_bb_wfo_oos_sharpe_ratio_1H_SL1.5_TSL2.0_BTC-USD.html
    # manual_ma_crossover_sma_wfo_oos_sharpe_ratio_SL1.5_TSL2.0_SMA200_BTC-USD.html
    
    basename = os.path.basename(filename)
    
    # Extract strategy type
    if "stoch_sma" in basename:
        strategy_type = "stoch_sma"
    elif "rsi_bb" in basename:
        strategy_type = "rsi_bb"
    elif "ma_crossover" in basename:
        strategy_type = "ma_crossover"
    else:
        strategy_type = "other"
    
    # Extract timeframe
    timeframe_match = re.search(r'_(\d+[HD])_', basename)
    timeframe = timeframe_match.group(1) if timeframe_match else ""
    if not timeframe:
        timeframe_match = re.search(r'ratio_(\d+[HD])', basename)
        timeframe = timeframe_match.group(1) if timeframe_match else "unknown"
    
    # Extract SL/TSL settings
    sl_match = re.search(r'SL(\d+\.\d+)', basename)
    sl = sl_match.group(1) if sl_match else "0.0"
    
    tsl_match = re.search(r'TSL(\d+\.\d+)', basename)
    tsl = tsl_match.group(1) if tsl_match else "0.0"
    
    # Extract SMA window if present
    sma_match = re.search(r'SMA(\d+)', basename)
    sma = sma_match.group(1) if sma_match else "0"
    
    # Extract symbol
    symbol_match = re.search(r'([A-Z]+-[A-Z]+)\.html', basename)
    symbol = symbol_match.group(1) if symbol_match else "unknown"
    
    # Create a key for grouping similar configs
    config_key = f"{strategy_type}_{timeframe}_{sl}_{tsl}_{sma}_{symbol}"
    
    return {
        'filename': filename,
        'strategy_type': strategy_type,
        'timeframe': timeframe,
        'sl': sl,
        'tsl': tsl,
        'sma': sma,
        'symbol': symbol,
        'config_key': config_key,
        'mtime': os.path.getmtime(filename)
    }

def cleanup_html_reports(reports_dir, keep_latest_n=1, dry_run=False, debug=False, keep_timeframe=None):
    """Clean up HTML backtest reports, keeping only the latest n for each configuration."""
    reports_path = Path(reports_dir)
    if not reports_path.exists() or not reports_path.is_dir():
        logger.error(f"Reports directory {reports_dir} does not exist")
        return
    
    # Get all HTML files
    html_files = glob.glob(str(reports_path / "*.html"))
    if not html_files:
        logger.info(f"No HTML files found in {reports_dir}")
        return
    
    logger.info(f"Found {len(html_files)} HTML files in {reports_dir}")
    
    # Parse file info and group by config
    config_groups = defaultdict(list)
    timeframe_files = defaultdict(list)
    
    # Debug: Print sample of file parsing
    if debug:
        logger.debug("Sample of file parsing:")
        for i, file in enumerate(html_files[:5]):
            file_info = parse_html_filename(file)
            logger.debug(f"File: {os.path.basename(file)}")
            logger.debug(f"  Config key: {file_info['config_key']}")
            logger.debug(f"  Strategy: {file_info['strategy_type']}")
            logger.debug(f"  Timeframe: {file_info['timeframe']}")
            logger.debug(f"  SL/TSL: {file_info['sl']}/{file_info['tsl']}")
            logger.debug(f"  SMA: {file_info['sma']}")
            logger.debug(f"  Symbol: {file_info['symbol']}")
            
    for file in html_files:
        file_info = parse_html_filename(file)
        config_groups[file_info['config_key']].append(file_info)
        timeframe_files[file_info['timeframe']].append(file_info)
    
    # Debug: Print duplicate configurations
    if debug:
        logger.debug("Duplicate configurations:")
        for config_key, files in config_groups.items():
            if len(files) > 1:
                logger.debug(f"Config: {config_key} has {len(files)} files:")
                for file_info in files:
                    logger.debug(f"  - {os.path.basename(file_info['filename'])} (mtime: {datetime.fromtimestamp(file_info['mtime'])})")
    
    # For each config group, keep only the most recent n files
    total_size_saved = 0
    files_to_delete = []
    
    # If a specific timeframe is specified, keep only files from that timeframe
    if keep_timeframe:
        for timeframe, files in timeframe_files.items():
            if timeframe != keep_timeframe:
                logger.info(f"Removing {len(files)} files from timeframe {timeframe} (keeping only {keep_timeframe})")
                for file_info in files:
                    filepath = file_info['filename']
                    size = os.path.getsize(filepath)
                    files_to_delete.append((filepath, size))
                    total_size_saved += size
    else:
        # Standard cleanup - keep the latest n files for each configuration
        for config_key, files in config_groups.items():
            # Sort by modification time (newest first)
            sorted_files = sorted(files, key=lambda x: x['mtime'], reverse=True)
            
            # Keep the most recent n files
            files_to_keep = sorted_files[:keep_latest_n]
            files_to_remove = sorted_files[keep_latest_n:]
            
            for file_info in files_to_remove:
                filepath = file_info['filename']
                size = os.path.getsize(filepath)
                files_to_delete.append((filepath, size))
                total_size_saved += size
    
    # Print summary
    logger.info(f"Found {len(config_groups)} unique configurations across {len(timeframe_files)} timeframes")
    for timeframe, files in timeframe_files.items():
        logger.info(f"  - Timeframe {timeframe}: {len(files)} files")
    
    logger.info(f"Files to delete: {len(files_to_delete)}")
    logger.info(f"Total space to be saved: {total_size_saved / (1024 * 1024):.2f} MB")
    
    # Delete files if not in dry run mode
    if not dry_run and files_to_delete:
        for filepath, _ in files_to_delete:
            try:
                os.remove(filepath)
                logger.info(f"Deleted: {os.path.basename(filepath)}")
            except Exception as e:
                logger.error(f"Error deleting {filepath}: {e}")
        logger.info(f"Cleanup complete. Deleted {len(files_to_delete)} files.")
    elif dry_run:
        logger.info("DRY RUN - no files were deleted. Files that would be deleted:")
        for filepath, size in files_to_delete:
            logger.info(f"  {os.path.basename(filepath)} ({size / (1024 * 1024):.2f} MB)")

def main():
    parser = argparse.ArgumentParser(description="Clean up old HTML backtest reports")
    parser.add_argument("--reports_dir", type=str, default="reports", 
                        help="Directory containing the HTML reports (default: reports)")
    parser.add_argument("--keep", type=int, default=1, 
                        help="Number of latest reports to keep for each configuration (default: 1)")
    parser.add_argument("--dry_run", action="store_true", 
                        help="Show what would be deleted without actually deleting files")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging")
    parser.add_argument("--keep_timeframe", type=str, default=None,
                        help="Only keep files from a specific timeframe (e.g., 1H, 1D)")
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    logger.info(f"Starting cleanup of HTML backtest reports")
    logger.info(f"Reports directory: {args.reports_dir}")
    logger.info(f"Keeping {args.keep} latest reports per configuration")
    logger.info(f"Dry run: {args.dry_run}")
    
    if args.keep_timeframe:
        logger.info(f"Only keeping timeframe: {args.keep_timeframe}")
    
    cleanup_html_reports(args.reports_dir, args.keep, args.dry_run, args.debug, args.keep_timeframe)

if __name__ == "__main__":
    main() 