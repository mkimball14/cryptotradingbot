import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any

from app.core.signal_manager import SignalManager, SignalConfirmation
from app.core.risk_manager import RiskManager
from app.models.zone import Zone

@pytest.fixture
def sample_ohlcv_data() -> pd.DataFrame:
    """Create sample OHLCV data for testing."""
    # Create 100 periods of sample data
    dates = pd.date_range(end=datetime.utcnow(), periods=100, freq='1H')
    
    # Generate sample price data with a trend and some volatility
    base_price = 100
    trend = np.linspace(0, 20, 100)  # Upward trend
    noise = np.random.normal(0, 1, 100)  # Random noise
    
    closes = base_price + trend + noise
    highs = closes + abs(np.random.normal(0, 0.5, 100))
    lows = closes - abs(np.random.normal(0, 0.5, 100))
    opens = closes + np.random.normal(0, 0.5, 100)
    
    # Generate volume with some spikes
    volume = np.random.normal(1000, 200, 100)
    volume[volume < 0] = 0  # Ensure no negative volume
    
    return pd.DataFrame({
        'timestamp': dates,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volume
    })

@pytest.fixture
def sample_supply_zone() -> Zone:
    """Create a sample supply zone for testing."""
    return Zone(
        id="test_supply_1",
        zone_type="supply",
        price_high=120.0,
        price_low=118.0,
        created_at=datetime.utcnow(),
        formation_volume=1000.0,
        formation_candles=[
            {
                "timestamp": datetime.utcnow() - timedelta(hours=1),
                "open": 119.0,
                "high": 120.0,
                "low": 118.0,
                "close": 118.5,
                "volume": 1000.0
            }
        ]
    )

@pytest.fixture
def sample_demand_zone() -> Zone:
    """Create a sample demand zone for testing."""
    return Zone(
        id="test_demand_1",
        zone_type="demand",
        price_high=102.0,
        price_low=100.0,
        created_at=datetime.utcnow(),
        formation_volume=800.0,
        formation_candles=[
            {
                "timestamp": datetime.utcnow() - timedelta(hours=1),
                "open": 101.0,
                "high": 102.0,
                "low": 100.0,
                "close": 101.5,
                "volume": 800.0
            }
        ]
    )

@pytest.fixture
def signal_manager(mocker) -> SignalManager:
    """Create a SignalManager instance with a mocked RiskManager."""
    mock_risk_manager = mocker.Mock(spec=RiskManager)
    return SignalManager(risk_manager=mock_risk_manager)

async def test_confirm_zone_signal_supply(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test signal confirmation for a supply zone."""
    result = await signal_manager.confirm_zone_signal(
        zone=sample_supply_zone,
        ohlcv_data=sample_ohlcv_data
    )
    
    assert isinstance(result, SignalConfirmation)
    assert isinstance(result.is_confirmed, bool)
    assert 0 <= result.confidence_score <= 1
    assert isinstance(result.confirmation_time, datetime)
    assert isinstance(result.confirmation_factors, dict)
    assert all(0 <= score <= 1 for score in result.confirmation_factors.values())
    assert result.metadata['zone_id'] == sample_supply_zone.id
    assert result.metadata['zone_type'] == 'supply'

async def test_confirm_zone_signal_demand(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_demand_zone: Zone
):
    """Test signal confirmation for a demand zone."""
    result = await signal_manager.confirm_zone_signal(
        zone=sample_demand_zone,
        ohlcv_data=sample_ohlcv_data
    )
    
    assert isinstance(result, SignalConfirmation)
    assert isinstance(result.is_confirmed, bool)
    assert 0 <= result.confidence_score <= 1
    assert isinstance(result.confirmation_time, datetime)
    assert isinstance(result.confirmation_factors, dict)
    assert all(0 <= score <= 1 for score in result.confirmation_factors.values())
    assert result.metadata['zone_id'] == sample_demand_zone.id
    assert result.metadata['zone_type'] == 'demand'

async def test_rsi_divergence_supply(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test RSI divergence detection for supply zones."""
    # Create bearish divergence scenario with overbought RSI
    data = sample_ohlcv_data.copy()
    
    # Create price movement that makes higher highs
    data.loc[data.index[-20:-10], 'close'] += np.linspace(0, 3, 10)  # First high
    data.loc[data.index[-10:], 'close'] += np.linspace(0, 5, 10)     # Higher high
    
    # Modify recent prices to create overbought RSI (> 70)
    # We'll create a strong uptrend to push RSI higher
    data.loc[data.index[-30:], 'close'] *= 1.1  # 10% increase
    
    score = await signal_manager._check_rsi_divergence(data, sample_supply_zone)
    assert 0 <= score <= 1
    assert score > 0.5  # Should detect strong bearish divergence with overbought condition

async def test_rsi_divergence_demand(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_demand_zone: Zone
):
    """Test RSI divergence detection for demand zones."""
    # Create bullish divergence scenario with oversold RSI
    data = sample_ohlcv_data.copy()
    
    # Create price movement that makes lower lows
    data.loc[data.index[-20:-10], 'close'] -= np.linspace(0, 3, 10)  # First low
    data.loc[data.index[-10:], 'close'] -= np.linspace(0, 5, 10)     # Lower low
    
    # Modify recent prices to create oversold RSI (< 30)
    # We'll create a strong downtrend to push RSI lower
    data.loc[data.index[-30:], 'close'] *= 0.9  # 10% decrease
    
    score = await signal_manager._check_rsi_divergence(data, sample_demand_zone)
    assert 0 <= score <= 1
    assert score > 0.5  # Should detect strong bullish divergence with oversold condition

async def test_rsi_divergence_no_signal(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test RSI divergence detection when no clear signal exists."""
    # Create scenario with no divergence and neutral RSI
    data = sample_ohlcv_data.copy()
    
    # Create steady uptrend without divergence
    data.loc[data.index[-10:], 'close'] += np.linspace(0, 2, 10)
    
    score = await signal_manager._check_rsi_divergence(data, sample_supply_zone)
    assert 0 <= score <= 1
    assert score < 0.3  # Should have low score due to lack of divergence and neutral RSI

async def test_rsi_divergence_edge_cases(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone,
    sample_demand_zone: Zone
):
    """Test RSI divergence detection edge cases."""
    # Test with very small price movements
    data = sample_ohlcv_data.copy()
    data.loc[data.index[-10:], 'close'] += np.random.normal(0, 0.0001, 10)
    
    supply_score = await signal_manager._check_rsi_divergence(data, sample_supply_zone)
    demand_score = await signal_manager._check_rsi_divergence(data, sample_demand_zone)
    
    assert 0 <= supply_score <= 1
    assert 0 <= demand_score <= 1
    
    # Test with extreme RSI values
    extreme_data = sample_ohlcv_data.copy()
    
    # Create extreme overbought condition
    extreme_data.loc[extreme_data.index[-30:], 'close'] *= 1.5  # 50% increase
    
    extreme_supply_score = await signal_manager._check_rsi_divergence(
        extreme_data, sample_supply_zone
    )
    assert extreme_supply_score > 0.3  # Should detect overbought condition
    
    # Create extreme oversold condition
    extreme_data = sample_ohlcv_data.copy()
    extreme_data.loc[extreme_data.index[-30:], 'close'] *= 0.5  # 50% decrease
    
    extreme_demand_score = await signal_manager._check_rsi_divergence(
        extreme_data, sample_demand_zone
    )
    assert extreme_demand_score > 0.3  # Should detect oversold condition

async def test_volume_profile_analysis(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test volume profile analysis."""
    # Create scenario with high volume near zone
    data = sample_ohlcv_data.copy()
    zone_price = (sample_supply_zone.price_high + sample_supply_zone.price_low) / 2
    
    # Add volume spike near zone price
    mask = (data['high'] >= zone_price) & (data['low'] <= zone_price)
    data.loc[mask, 'volume'] *= 2
    
    score = await signal_manager._analyze_volume_profile(data, sample_supply_zone)
    assert 0 <= score <= 1
    assert score > 0.5  # Should indicate significant volume near zone

async def test_macd_confirmation(
    signal_manager: SignalManager,
    sample_ohlcv_data: pd.DataFrame,
    sample_supply_zone: Zone
):
    """Test MACD confirmation analysis."""
    # Create bearish MACD crossover scenario
    data = sample_ohlcv_data.copy()
    
    # Modify prices to create MACD crossover
    data.loc[data.index[-5:], 'close'] -= np.linspace(0, 2, 5)
    
    score = await signal_manager._check_macd_confirmation(data, sample_supply_zone)
    assert 0 <= score <= 1

async def test_zone_freshness(
    signal_manager: SignalManager,
    sample_supply_zone: Zone
):
    """Test zone freshness calculation."""
    # Test fresh zone
    fresh_zone = sample_supply_zone.copy()
    fresh_zone.created_at = datetime.utcnow() - timedelta(hours=1)
    fresh_zone.test_count = 0
    
    fresh_score = signal_manager._calculate_zone_freshness(fresh_zone)
    assert 0 <= fresh_score <= 1
    assert fresh_score > 0.8  # Should be very fresh
    
    # Test old zone
    old_zone = sample_supply_zone.copy()
    old_zone.created_at = datetime.utcnow() - timedelta(days=10)
    old_zone.test_count = 5
    
    old_score = signal_manager._calculate_zone_freshness(old_zone)
    assert 0 <= old_score <= 1
    assert old_score < 0.2  # Should be considered stale 