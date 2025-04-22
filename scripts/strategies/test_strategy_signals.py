import sys
import logging
from pathlib import Path
import pandas as pd

# Setup Paths and Logging (similar to wfo_edge_strategy.py)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('test_strategy_signals')

# Import necessary functions/classes
try:
    # Assuming standard structure
    from scripts.strategies.wfo_edge_strategy import load_data
    from scripts.strategies.edge_strategy_assistant import create_portfolio
    # from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy # Keep for Option 2 if needed
    logger.info("Successfully imported necessary components.")
except ImportError as e:
    logger.critical(f"Failed to import components: {e}. Ensure script is run from project root or paths are correct.")
    sys.exit(1)

# --- Test Configuration ---
SYMBOL = "BTC/USD" # Same as WFO
TIMEFRAME = "1h"   # Changed from 1d to 1h for more granular data
# Use a longer period for hourly data
LOOKBACK_DAYS_FOR_TEST = 90 # Increased from 30 to 90 for sufficient lookback data
DATA_SLICE_DAYS = 60      # Adjusted for hourly timeframe

# --- Fixed Default Parameters (similar to WFO fallback) ---
# Note: Need to check what parameters create_portfolio expects.
# Based on wfo_edge_strategy's create_pf_for_params and its fallback:
default_params_for_create_portfolio = {
    'lookback_window': 20,
    'vol_filter_window': 100,
    'volatility_threshold': 0.0175,
    'initial_capital': 3000,
    'commission_pct': 0.001,
    'slippage_pct': 0.0005,
    'default_factor_weights': {
        'volatility_regime': 0.25,
        'consolidation_breakout': 0.25,
        'volume_divergence': 0.25,
        'market_microstructure': 0.25
    }
    # Removed parameters not used by EdgeMultiFactorStrategy constructor:
    # 'rsi_lower': 30,
    # 'rsi_upper': 70,
    # 'bb_window': 20,
    # 'bb_alpha': 2.0,
    # 'stop_loss_pct': 0.05,
    # 'take_profit_pct': 0.1,
    # 'size_pct': 0.3,
    # 'max_holdings': 1
}
logger.info(f"Using fixed parameters: {default_params_for_create_portfolio}")

# Create additional parameter sets for testing
test_params = [
    # Test set 1: Optimized based on debugging results
    {
        'lookback_window': 20,
        'vol_filter_window': 100,
        'volatility_threshold': 0.8,    # Higher volatility threshold based on analysis
        'initial_capital': 3000,
        'commission_pct': 0.001,
        'slippage_pct': 0.0005,
        'signal_threshold': 0.1,        # Lower signal threshold
        'default_factor_weights': {
            'volatility_regime': 0.25,
            'consolidation_breakout': 0.25,
            'volume_divergence': 0.1,
            'market_microstructure': 0.4 # Increased weight for market microstructure
        }
    },
    
    # Test set 2: Focus on market microstructure with other improvements
    {
        'lookback_window': 15,          # Reduced lookback for faster response
        'vol_filter_window': 50,        # Reduced filter window
        'volatility_threshold': 0.7,    # Optimized volatility threshold
        'initial_capital': 3000,
        'commission_pct': 0.001,
        'slippage_pct': 0.0005,
        'signal_threshold': 0.1,        # Very low threshold for more signals
        'default_factor_weights': {
            'volatility_regime': 0.2,
            'consolidation_breakout': 0.1,
            'volume_divergence': 0.1,
            'market_microstructure': 0.6 # Heavily weighted toward microstructure
        }
    }
]

param_names = [
    "Optimized Parameter Set",
    "Market Microstructure Focus"
]

# --- Main Test Logic ---
if __name__ == "__main__":
    logger.info(f"Loading data for {SYMBOL}...")
    # Load enough data for lookbacks + test period
    full_data = load_data(SYMBOL, TIMEFRAME, LOOKBACK_DAYS_FOR_TEST)

    if full_data is None or 'close' not in full_data or full_data['close'].empty:
        logger.critical("Failed to load data for testing.")
        sys.exit(1)

    # Take a slice of data (e.g., the most recent DATA_SLICE_DAYS)
    # Ensure the slice is long enough AFTER accounting for NaNs from indicators
    # Indicators might consume initial rows, let's take data from the end
    if len(full_data['close']) > DATA_SLICE_DAYS:
        test_data_dict = {}
        # Ensure we have enough data for the longest lookback (e.g., 105) *before* the slice starts
        required_lookback = 105 # Example based on previous warnings
        slice_start_min_index = required_lookback
        if len(full_data['close']) > DATA_SLICE_DAYS + slice_start_min_index:
            start_idx = len(full_data['close']) - DATA_SLICE_DAYS
        else:
            logger.warning(f"Not enough data for required lookback before slice. Using available data.")
            start_idx = max(0, len(full_data['close']) - DATA_SLICE_DAYS) # Fallback

        logger.info(f"Creating data slice from index {start_idx}...")

        for key, series in full_data.items():
            if isinstance(series, pd.Series):
                test_data_dict[key] = series.iloc[start_idx:].copy() # Use copy to avoid SettingWithCopyWarning
            else:
                 test_data_dict[key] = series # Keep non-series data as is
        logger.info(f"Using data slice of length {len(test_data_dict['close'])} starting {test_data_dict['close'].index[0]} ending on {test_data_dict['close'].index[-1]}")

        # Add conversion to DataFrame if create_portfolio expects it
        try:
            test_data_df = pd.DataFrame(test_data_dict)
            logger.info("Converted test data dict to DataFrame.")
        except Exception as df_err:
            logger.error(f"Could not convert data dict to DataFrame: {df_err}. Trying with dict.")
            test_data_df = test_data_dict # Fallback to dict

    else:
        logger.warning(f"Loaded data ({len(full_data['close'])}) is not longer than slice ({DATA_SLICE_DAYS}). Using all loaded data.")
        # Convert full data if using it all
        try:
            test_data_df = pd.DataFrame(full_data)
        except Exception as df_err:
             logger.error(f"Could not convert full_data dict to DataFrame: {df_err}.")
             sys.exit(1)


    logger.info("Attempting to create portfolio and generate signals...")

    # Call create_portfolio with different parameter sets
    results_summary = []
    
    for i, (params, name) in enumerate(zip(test_params, param_names)):
        logger.info(f"\n\n===== TESTING PARAMETER SET {i+1}: {name} =====")
        
        for key, value in params.items():
            if key != 'default_factor_weights':
                logger.info(f"  {key}: {value}")
            else:
                logger.info(f"  Factor weights: {value}")
                
        try:
            # Pass the DataFrame slice with the current parameter set
            portfolio, success = create_portfolio(test_data_df, params)
            
            # Store results summary
            result = {
                "parameter_set": name,
                "success": success,
                "portfolio_created": portfolio is not None
            }
            
            if success and portfolio is not None:
                logger.info(f"Portfolio created successfully with parameter set {i+1}.")
                
                # Check if signals were generated (indirectly by checking trades)
                if hasattr(portfolio, 'trades'):
                    # Handle different versions of VectorBT with different trade object structures
                    trade_count = 0
                    try:
                        # Try to access as attribute (newer vectorbt)
                        if hasattr(portfolio.trades, 'count'):
                            if callable(portfolio.trades.count):
                                trade_count = portfolio.trades.count()
                            else:
                                trade_count = portfolio.trades.count
                        # Try to access as method (older vectorbt)
                        elif hasattr(portfolio.trades, 'get_count'):
                            trade_count = portfolio.trades.get_count()
                        # Try to access length
                        elif hasattr(portfolio.trades, '__len__'):
                            trade_count = len(portfolio.trades)
                        else:
                            # Get count by iterating over records if possible
                            if hasattr(portfolio.trades, 'records'):
                                if hasattr(portfolio.trades.records, '__len__'):
                                    trade_count = len(portfolio.trades.records)
                                    
                        logger.info(f"Strategy generated {trade_count} trades.")
                        result["trades"] = trade_count
                        
                        print(f"\n--- Trades for Parameter Set {i+1} ({name}) ---")
                        # Make sure to handle potential large output
                        try:
                            if hasattr(portfolio.trades, 'records_readable'):
                                print(portfolio.trades.records_readable.to_string())
                            elif hasattr(portfolio.trades, 'data'):
                                print(portfolio.trades.data.to_string())
                            else:
                                print(f"Trade count: {trade_count} (cannot print trade details)")
                        except Exception as e:
                            print(f"Could not print trades DataFrame: {e}")

                        # Check for entry/exit signals
                        if hasattr(portfolio, 'entries'):
                            entry_count = portfolio.entries.sum()
                            print(f"\nEntry signals count: {entry_count}")
                            result["entries"] = int(entry_count)
                            
                        if hasattr(portfolio, 'exits'):
                            exit_count = portfolio.exits.sum()
                            print(f"Exit signals count: {exit_count}")
                            result["exits"] = int(exit_count)
                            
                    except Exception as e:
                        logger.error(f"Error processing trades: {e}")
                        result["trades"] = 0
                        
                else:
                    logger.warning(f"Portfolio created with parameter set {i+1}, but no 'trades' attribute found.")
                    result["trades"] = 0

            else:
                error_msg = "Portfolio creation failed" if not success else "Portfolio is None but success reported"
                logger.error(f"{error_msg} with parameter set {i+1}.")
                result["trades"] = 0
                result["entries"] = 0
                result["exits"] = 0
            
            results_summary.append(result)
                
        except Exception as e:
            logger.error(f"An error occurred testing parameter set {i+1}: {e}", exc_info=True)
            results_summary.append({
                "parameter_set": name,
                "success": False,
                "error": str(e),
                "trades": 0,
                "entries": 0,
                "exits": 0
            })
    
    # Print summary of all parameter sets
    print("\n\n===== SUMMARY OF ALL PARAMETER SETS =====")
    for result in results_summary:
        ps = result["parameter_set"]
        status = "✅ Success" if result.get("success", False) else "❌ Failed"
        trades = result.get("trades", 0)
        entries = result.get("entries", 0)
        exits = result.get("exits", 0)
        
        print(f"{ps}: {status}, Trades: {trades}, Entries: {entries}, Exits: {exits}")
    
    # Direct signal analysis
    print("\n\n===== DIRECT SIGNAL ANALYSIS =====")
    print("Analyzing signals directly from strategy without portfolio creation")
    
    for i, (params, name) in enumerate(zip(test_params, param_names)):
        print(f"\n--- Parameter Set {i+1}: {name} ---")
        
        try:
            # Import strategy directly
            from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
            
            # Create strategy instance with parameters
            strategy = EdgeMultiFactorStrategy(**params)
            
            # Generate signals directly
            long_entries, short_entries, is_trending, is_ranging = strategy.generate_signals(test_data_df)
            
            # Print signal summary
            print(f"Long entries: {long_entries.sum()} ({long_entries.sum()/len(long_entries)*100:.2f}%)")
            print(f"Short entries: {short_entries.sum()} ({short_entries.sum()/len(short_entries)*100:.2f}%)")
            
            # Total signal count
            total_signals = long_entries.sum() + short_entries.sum()
            print(f"Total signals: {total_signals} ({total_signals/len(long_entries)*100:.2f}%)")
            
            # Calculate signal distribution by market regime
            trend_up_signals = long_entries[is_trending & (test_data_df['close'] > test_data_df['close'].shift(strategy.lookback_window))].sum()
            trend_down_signals = short_entries[is_trending & (test_data_df['close'] < test_data_df['close'].shift(strategy.lookback_window))].sum()
            ranging_long_signals = long_entries[is_ranging].sum()
            ranging_short_signals = short_entries[is_ranging].sum()
            
            print(f"Signal distribution by market regime:")
            print(f"  Uptrend long signals: {trend_up_signals}")
            print(f"  Downtrend short signals: {trend_down_signals}")
            print(f"  Ranging long signals: {ranging_long_signals}")
            print(f"  Ranging short signals: {ranging_short_signals}")
            
            # Print signal dates (max 5)
            if long_entries.sum() > 0:
                print(f"Long entry dates (first 5): {long_entries[long_entries].index[:5].tolist()}")
            if short_entries.sum() > 0:
                print(f"Short entry dates (first 5): {short_entries[short_entries].index[:5].tolist()}")
            
        except Exception as e:
            print(f"Error during direct signal generation: {e}")

    logger.info("Test script finished.") 