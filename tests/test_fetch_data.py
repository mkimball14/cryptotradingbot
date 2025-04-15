import os
import sys
import logging
import pandas as pd

# Add project root to sys.path to allow importing app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scripts.backtest_rsi_vbt import fetch_historical_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_fetch_historical_data():
    """Test the fetch_historical_data function with a small date range."""
    product_id = "BTC-USD"
    start_date = "2024-01-01"
    end_date = "2024-01-03"
    
    logger.info(f"Fetching historical data for {product_id} from {start_date} to {end_date}")
    
    # Call the function
    df = fetch_historical_data(
        product_id=product_id,
        start_date=start_date,
        end_date=end_date
    )
    
    # Verify the result
    if df is not None:
        logger.info(f"Successfully fetched data with shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info(f"Data types: \n{df.dtypes}")
        logger.info(f"Index type: {type(df.index).__name__}")
        
        # Check for numeric columns
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in df.columns:
                is_numeric = pd.api.types.is_numeric_dtype(df[col])
                logger.info(f"Column '{col}' is numeric: {is_numeric}")
        
        # Display a sample of the data
        logger.info("\nSample data:")
        logger.info(f"\n{df.head(3)}")
        
        return True
    else:
        logger.error("Failed to fetch data")
        return False

if __name__ == "__main__":
    test_fetch_historical_data() 