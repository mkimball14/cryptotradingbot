import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
# Remove Base definition from here
# from sqlalchemy.ext.declarative import declarative_base
import logging
from pathlib import Path
# Import Base from the new base.py file (use absolute path)
from app.core.trade_log.base import Base 

logger = logging.getLogger(__name__)

# Define the default database path relative to the project root
DEFAULT_DB_FILENAME = "trading_log.sqlite"
PROJECT_ROOT = Path(__file__).resolve().parents[3] # Adjust based on actual file location
DATABASE_PATH = PROJECT_ROOT / "data" / DEFAULT_DB_FILENAME
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# Ensure the data directory exists
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

logger.info(f"Database URL: {DATABASE_URL}")

# Create the async engine
# connect_args are specific to SQLite to improve concurrency handling if needed
engine = create_async_engine(DATABASE_URL, echo=False, future=True, connect_args={"check_same_thread": False})

# Create a session factory
# expire_on_commit=False prevents attributes from being expired after commit
AsyncSessionFactory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Ensure models are imported *before* init_db might be called (use absolute path)
from app.core.trade_log.models import TradeLog

async def get_db() -> AsyncSession:
    """Dependency function to get a database session."""
    async with AsyncSessionFactory() as session:
        yield session

async def init_db():
    """Initializes the database by creating tables based on models."""
    async with engine.begin() as conn:
        logger.info("Dropping all tables (if they exist)...") # Usually for dev/testing
        # await conn.run_sync(Base.metadata.drop_all) # Be cautious with drop_all in production
        logger.info("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created.")

# --- Test Function --- 
async def test_logging():
    """Tests creating a log entry via OrderExecutor."""
    print("--- Running Logging Test --- ")
    
    # We need OrderExecutor and a mock/real CoinbaseClient for this test
    from app.core.order_executor import OrderExecutor, OrderSide # Import necessary items
    from app.core.coinbase import CoinbaseClient # Using real client, expect API call to fail
    
    # Simulate getting a DB session
    session_generator = get_db()
    db = await session_generator.__anext__()
    
    try:
        # Instantiate CoinbaseClient (requires valid-looking dummy creds or env vars)
        # This part might fail if Settings/env vars aren't set up for direct script runs
        # Provide dummy keys if necessary for instantiation
        try:
            # Attempt to use settings if available from config
            from app.core.config import settings
            client = CoinbaseClient(settings=settings)
            print("Using CoinbaseClient with settings from config.")
        except ImportError:
             # Fallback: Create a dummy Settings object
             print("Settings object import failed, creating dummy Settings for test.")
             # We need the Settings class definition
             from app.core.config import Settings 
             dummy_settings = Settings(
                 COINBASE_JWT_KEY_NAME = "organizations/YOUR_ORG/apiKeys/DUMMY_KEY",
                 COINBASE_JWT_PRIVATE_KEY = (
                     "-----BEGIN EC PRIVATE KEY-----\n" +
                     "MIIEpQIBAAKCAQEAuZ+1Zf8Z7f...\n" +
                     "-----END EC PRIVATE KEY-----"
                 ),
                 # Add any other mandatory fields from Settings with dummy values if needed
                 TRADING_ENABLED=False # Example default for a test
             )
             client = CoinbaseClient(settings=dummy_settings)

        # Instantiate OrderExecutor
        order_executor = OrderExecutor(client=client)
        
        print("Attempting to execute a dummy market order (API call expected to fail)...")
        try:
            await order_executor.execute_market_order(
                db=db,
                product_id="BTC-USD-TEST",
                side=OrderSide.BUY,
                size=0.001,
                strategy_name="TestStrategy"
            )
            print("Log test: Order execution call completed unexpectedly (maybe succeeded?).")
        except Exception as exec_err:
            # We expect an error here, likely from the API call
            print(f"Log test: Caught expected exception during order execution: {exec_err}")
            # Check if an error log was created by execute_market_order's except block

        # Query the database to see if a log was created
        # Use absolute imports when running as a script
        from app.core.trade_log.crud import get_logs_by_event_type
        from app.core.trade_log.models import EventType
        
        logs = await get_logs_by_event_type(db, EventType.ERROR, limit=5) # Check for ERROR logs first
        if not logs:
             logs = await get_logs_by_event_type(db, EventType.ENTRY_ORDER, limit=5) # Check for ORDER logs if no errors
             
        print(f"Found {len(logs)} relevant log entries in the database:")
        for log in logs:
            print(f"  - {log}")
            
        if logs:
             print("--- Logging Test: SUCCESS (Log entry created) ---")
        else:
             print("--- Logging Test: FAILED (No relevant log entry found) ---")
             
    except ImportError as ie:
        print(f"Logging Test Aborted: Could not import necessary components ({ie}). Ensure paths are correct.")    
    except Exception as e:
        print(f"An error occurred during the logging test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up the session
        await db.close()
        print("--- Logging Test Finished --- ")


if __name__ == "__main__":
    # Example of how to initialize the database directly
    import asyncio
    
    # Removed model import from here, moved to top level
    # from app.core.trade_log import models # Import the models module
    
    async def run_init_and_test():
        print("Initializing database...")
        await init_db() # Now Base.metadata should contain the tables
        print("Database initialization complete.")
        await test_logging() # Run the test function
        
    # Configure logging for the test
    logging.basicConfig(level=logging.INFO) # Set to DEBUG to see more detail
    logger.info("Running database.py script...")
        
    asyncio.run(run_init_and_test()) 