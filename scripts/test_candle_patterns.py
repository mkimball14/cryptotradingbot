import sys
import os
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the system path to import our modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import the candle pattern functions
from scripts.indicators.candle_patterns import (
    extract_candle_patterns,
    get_candle_pattern_strength,
    generate_candle_pattern_signals,
    optimize_pattern_signal_parameters
)

def load_test_data():
    """Load sample data for testing candle patterns"""
    try:
        # Try to load from a CSV file if available
        csv_path = Path(__file__).resolve().parent / 'test_data' / 'sample_ohlc_data.csv'
        
        if csv_path.exists():
            logger.info(f"Loading test data from {csv_path}")
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            return df
        
        # If no CSV exists, generate synthetic data
        logger.info("Generating synthetic test data")
        
        # Generate datetime index
        days = pd.date_range(start='2020-01-01', periods=500, freq='D')
        
        # Generate synthetic price data with some patterns
        np.random.seed(42)  # For reproducibility
        
        # Start with a base price and add random walk
        close = 100.0
        closes = [close]
        
        for _ in range(1, 500):
            # Random walk with some mean reversion
            pct_change = np.random.normal(0, 0.015)  # 1.5% daily volatility
            if close > 150:  # Mean reversion if price gets too high
                pct_change -= 0.002
            elif close < 50:  # Mean reversion if price gets too low
                pct_change += 0.002
                
            close = close * (1 + pct_change)
            closes.append(close)
        
        # Generate OHLC data with some realistic candle patterns
        df = pd.DataFrame(index=days)
        df['close'] = closes
        
        # Generate realistic open, high, low values
        for i in range(len(df)):
            # First day
            if i == 0:
                df.loc[df.index[i], 'open'] = df.loc[df.index[i], 'close'] * (1 - 0.005)
                continue
                
            # Other days: open near previous close
            prev_close = df.loc[df.index[i-1], 'close']
            
            # Occasionally create gaps up or down (10% chance)
            if np.random.random() < 0.1:
                gap_factor = np.random.normal(0, 0.01)  # 1% gap on average
                df.loc[df.index[i], 'open'] = prev_close * (1 + gap_factor)
            else:
                # Open near previous close
                df.loc[df.index[i], 'open'] = prev_close * (1 + np.random.normal(0, 0.003))
                
            # Determine if bullish or bearish candle
            is_bullish = df.loc[df.index[i], 'close'] > df.loc[df.index[i], 'open']
            
            # Generate high and low
            daily_volatility = abs(df.loc[df.index[i], 'close'] - df.loc[df.index[i], 'open']) * 2
            if daily_volatility < 0.001 * df.loc[df.index[i], 'close']:
                daily_volatility = 0.001 * df.loc[df.index[i], 'close']  # Minimum volatility
                
            # Occasionally create long wicks (hammer, shooting star, etc.)
            upper_wick = daily_volatility * np.random.exponential(0.5)
            lower_wick = daily_volatility * np.random.exponential(0.5)
            
            # 5% chance of a doji
            if np.random.random() < 0.05:
                df.loc[df.index[i], 'open'] = df.loc[df.index[i], 'close'] * (1 + np.random.normal(0, 0.001))
                # Doji often have long wicks
                upper_wick = daily_volatility * np.random.exponential(1.5)
                lower_wick = daily_volatility * np.random.exponential(1.5)
            
            # Set high and low
            if is_bullish:
                df.loc[df.index[i], 'high'] = max(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) + upper_wick
                df.loc[df.index[i], 'low'] = min(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) - lower_wick
            else:
                df.loc[df.index[i], 'high'] = max(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) + upper_wick
                df.loc[df.index[i], 'low'] = min(df.loc[df.index[i], 'open'], df.loc[df.index[i], 'close']) - lower_wick
                
        # Add volume data for completeness
        df['volume'] = np.random.exponential(scale=1000000, size=len(df))
        
        # Occasionally make volume spikes on big price moves
        big_moves = abs(df['close'].pct_change()) > 0.02
        df.loc[big_moves, 'volume'] = df.loc[big_moves, 'volume'] * 2.5
                
        # Save data for future use
        os.makedirs(Path(__file__).resolve().parent / 'test_data', exist_ok=True)
        df.to_csv(csv_path)
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading/generating test data: {str(e)}")
        # Return minimal viable test data
        return pd.DataFrame({
            'open': [100, 101, 99, 102, 103],
            'high': [105, 103, 100, 104, 105],
            'low': [98, 98, 95, 100, 101],
            'close': [101, 99, 100, 103, 102],
            'volume': [1000000, 1200000, 900000, 1500000, 1100000]
        }, index=pd.date_range(start='2020-01-01', periods=5))

def test_extract_candle_patterns():
    """Test the extract_candle_patterns function"""
    logger.info("Testing extract_candle_patterns function")
    
    # Load test data
    df = load_test_data()
    
    # Test with default parameters (all patterns)
    result_df = extract_candle_patterns(df)
    
    # Check if CDL columns were added
    pattern_cols = [col for col in result_df.columns if col.startswith('CDL')]
    logger.info(f"Extracted {len(pattern_cols)} candle patterns")
    
    if len(pattern_cols) == 0:
        logger.error("No patterns were extracted!")
    else:
        # Log the first 5 patterns
        logger.info(f"First 5 pattern columns: {pattern_cols[:5]}")
        
        # Count non-zero pattern instances
        non_zero_counts = {col: (result_df[col] != 0).sum() for col in pattern_cols}
        logger.info(f"Patterns with most occurrences: {sorted(non_zero_counts.items(), key=lambda x: x[1], reverse=True)[:5]}")
    
    # Test with specific patterns
    specific_patterns = ['doji', 'hammer', 'engulfing', 'morningstar']
    logger.info(f"Testing extraction of specific patterns: {specific_patterns}")
    specific_result = extract_candle_patterns(df, pattern_list=specific_patterns)
    
    specific_pattern_cols = [col for col in specific_result.columns if col.startswith('CDL')]
    logger.info(f"Extracted {len(specific_pattern_cols)} specific patterns: {specific_pattern_cols}")
    
    return result_df

def test_pattern_strength():
    """Test the pattern strength calculation function"""
    logger.info("Testing pattern strength calculation")
    
    # First get patterns
    df = load_test_data()
    df_with_patterns = extract_candle_patterns(df)
    
    # Calculate pattern strength
    df_with_strength = get_candle_pattern_strength(df_with_patterns, lookback=20)
    
    # Check if strength columns were added
    strength_cols = [col for col in df_with_strength.columns if col.endswith('_strength')]
    logger.info(f"Generated {len(strength_cols)} pattern strength columns")
    
    if len(strength_cols) == 0:
        logger.error("No strength columns were generated!")
    else:
        # Count non-zero strength values
        non_zero_counts = {col: (df_with_strength[col] != 0).sum() for col in strength_cols}
        logger.info(f"Strength columns with most non-zero values: {sorted(non_zero_counts.items(), key=lambda x: x[1], reverse=True)[:5]}")
        
        # Show max strength values
        max_strengths = {col: df_with_strength[col].max() for col in strength_cols if df_with_strength[col].max() > 0}
        logger.info(f"Top 5 patterns by maximum strength: {sorted(max_strengths.items(), key=lambda x: x[1], reverse=True)[:5]}")
    
    return df_with_strength

def test_signal_generation():
    """Test the signal generation function"""
    logger.info("Testing signal generation")
    
    # Get data with patterns and strength
    df = load_test_data()
    df_with_patterns = extract_candle_patterns(df)
    df_with_strength = get_candle_pattern_strength(df_with_patterns, lookback=20)
    
    # Generate signals with default parameters
    buy_signals, sell_signals = generate_candle_pattern_signals(df_with_strength)
    
    # Count signals
    buy_count = buy_signals.sum()
    sell_count = sell_signals.sum()
    
    logger.info(f"Generated {buy_count} buy signals and {sell_count} sell signals with default parameters")
    
    # Test with different strength thresholds
    min_strengths = [0.0, 0.01, 0.05, 0.1]
    for min_strength in min_strengths:
        buy_sigs, sell_sigs = generate_candle_pattern_signals(df_with_strength, min_strength=min_strength)
        logger.info(f"With min_strength={min_strength}: {buy_sigs.sum()} buy signals, {sell_sigs.sum()} sell signals")
    
    # Test without using strength
    buy_sigs_raw, sell_sigs_raw = generate_candle_pattern_signals(df_with_strength, use_strength=False)
    logger.info(f"Without using strength: {buy_sigs_raw.sum()} buy signals, {sell_sigs_raw.sum()} sell signals")
    
    return buy_signals, sell_signals

def test_parameter_optimization():
    """Test the parameter optimization function"""
    logger.info("Testing parameter optimization")
    
    # Prepare data
    df = load_test_data()
    df_with_patterns = extract_candle_patterns(df)
    
    # Only run optimization if we have enough data
    if len(df_with_patterns) < 252:
        logger.warning("Not enough data for optimization test. Skipping.")
        return None
    
    # Run optimization with a smaller search space for testing
    logger.info("Running parameter optimization (this may take a while)...")
    best_params = optimize_pattern_signal_parameters(
        df_with_patterns,
        test_length=min(252, len(df_with_patterns) // 2),
        min_trades=5
    )
    
    logger.info(f"Optimized parameters: {best_params}")
    
    return best_params

def main():
    """Run all tests"""
    logger.info("Starting candle pattern function tests")
    
    # Test pattern extraction
    df_with_patterns = test_extract_candle_patterns()
    
    # Test pattern strength calculation
    df_with_strength = test_pattern_strength()
    
    # Test signal generation
    buy_signals, sell_signals = test_signal_generation()
    
    # Test parameter optimization
    best_params = test_parameter_optimization()
    
    logger.info("All tests completed")
    
    # Return results for inspection
    return {
        "df_with_patterns": df_with_patterns,
        "df_with_strength": df_with_strength,
        "buy_signals": buy_signals,
        "sell_signals": sell_signals,
        "best_params": best_params
    }

if __name__ == "__main__":
    test_results = main() 