from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .models import Base

DATABASE_URL = "sqlite:///./crypto_bot.db"

# The connect_args argument is needed only for SQLite.
# It's needed to allow the same thread to be used for requests as it prevents
# "SQLite objects created in a thread can only be used in that same thread"
# errors when using FastAPI background tasks or similar async operations.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database by creating tables defined in models.py."""
    Base.metadata.create_all(bind=engine) 