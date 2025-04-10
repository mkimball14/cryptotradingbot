from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger, UniqueConstraint, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Candle(Base):
    __tablename__ = 'candles'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    granularity = Column(String, index=True, nullable=False)
    timestamp = Column(BigInteger, index=True, nullable=False)  # Store Unix timestamp (seconds)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('symbol', 'granularity', 'timestamp', name='_symbol_granularity_timestamp_uc'),
    )

    def __repr__(self):
        return f"<Candle(symbol='{self.symbol}', granularity='{self.granularity}', timestamp={self.timestamp}, close={self.close})>"

class Zone(Base):
    __tablename__ = 'zones'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    timeframe = Column(String, index=True, nullable=False) # e.g., '1h', '15m'
    type = Column(String, index=True, nullable=False) # 'supply' or 'demand'
    
    zone_low = Column(Float, nullable=False)
    zone_high = Column(Float, nullable=False)
    
    # Timestamps (Unix seconds) of key candles in the pattern
    leg_in_timestamp = Column(BigInteger, nullable=False)
    base_start_timestamp = Column(BigInteger, nullable=False)
    base_end_timestamp = Column(BigInteger, nullable=False)
    formation_timestamp = Column(BigInteger, index=True, nullable=False) # Timestamp of leg-out candle

    # Scoring and status
    initial_freshness_score = Column(Integer) # Score at formation
    initial_strength_score = Column(Integer)  # Score at formation
    rsi_at_formation = Column(Float, nullable=True) # RSI(14) at formation candle
    is_active = Column(Boolean, default=True, index=True)
    num_touches = Column(Integer, default=0)
    last_tested_timestamp = Column(BigInteger, nullable=True)

    # Unique constraint to avoid storing the exact same zone multiple times
    # Based on type, timeframe, symbol, and formation time
    __table_args__ = (
        UniqueConstraint('symbol', 'timeframe', 'type', 'formation_timestamp', name='_zone_formation_uc'),
    )

    def __repr__(self):
        return f"<Zone(id={self.id}, type='{self.type}', symbol='{self.symbol}', timeframe='{self.timeframe}', high={self.zone_high}, low={self.zone_low}, formed={self.formation_timestamp}, active={self.is_active})>" 