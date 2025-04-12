import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.core.market_simulator import MarketSimulator

@pytest.fixture
def sample_data():
    """Create sample market data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-01-10', freq='D')
    data = pd.DataFrame({
        'timestamp': dates,
        'open': [100.0] * 10,
        'high': [105.0] * 10,
        'low': [95.0] * 10,
        'close': [102.0] * 10,
        'volume': [1000.0] * 10
    })
    return data

@pytest.fixture
def simulator(sample_data):
    """Create a MarketSimulator instance with sample data."""
    return MarketSimulator(sample_data, random_seed=42)

def test_initialization(sample_data):
    """Test MarketSimulator initialization."""
    simulator = MarketSimulator(sample_data)
    assert simulator.base_data.equals(sample_data)
    assert len(simulator.base_data) == len(sample_data)

def test_volatility_spike(simulator):
    """Test adding volatility spike to the data."""
    result = simulator.add_volatility_spike(start_idx=2, duration=3, intensity=2.0)
    
    # Check that data outside the spike period remains unchanged
    assert result.iloc[0:2].equals(simulator.base_data.iloc[0:2])
    assert result.iloc[5:].equals(simulator.base_data.iloc[5:])
    
    # Check that volatility increased during the spike period
    original_volatility = np.log(simulator.base_data['close'] / simulator.base_data['close'].shift(1)).std()
    spike_volatility = np.log(result.iloc[2:5]['close'] / result.iloc[2:5]['close'].shift(1)).std()
    assert spike_volatility > original_volatility

def test_simulate_gap(simulator):
    """Test simulating price gaps."""
    gap_percent = 5.0
    result = simulator.simulate_gap(index=3, gap_percent=gap_percent)
    
    # Check that data before the gap is unchanged
    assert result.iloc[:3].equals(simulator.base_data.iloc[:3])
    
    # Check that the gap is applied correctly
    expected_adjustment = 1 + (gap_percent / 100)
    for col in ['open', 'high', 'low', 'close']:
        assert np.allclose(
            result.iloc[3:][col] / simulator.base_data.iloc[3:][col],
            expected_adjustment
        )

def test_simulate_trend(simulator):
    """Test simulating market trends."""
    trend_strength = 0.01  # 1% daily trend
    result = simulator.simulate_trend(start_idx=2, duration=4, trend_strength=trend_strength)
    
    # Check that data outside the trend period is unchanged
    assert result.iloc[:2].equals(simulator.base_data.iloc[:2])
    assert result.iloc[6:].equals(simulator.base_data.iloc[6:])
    
    # Check that prices follow the trend
    for i in range(3, 6):
        assert result.iloc[i]['close'] > result.iloc[i-1]['close']

def test_simulate_liquidity_change(simulator):
    """Test simulating liquidity changes."""
    liquidity_factor = 0.5
    result = simulator.simulate_liquidity_change(start_idx=2, duration=3, liquidity_factor=liquidity_factor)
    
    # Check volume adjustment
    assert np.allclose(
        result.iloc[2:5]['volume'] / simulator.base_data.iloc[2:5]['volume'],
        liquidity_factor
    )
    
    # Check spread widening
    original_spreads = simulator.base_data.iloc[2:5]['high'] - simulator.base_data.iloc[2:5]['low']
    new_spreads = result.iloc[2:5]['high'] - result.iloc[2:5]['low']
    assert all(new_spreads > original_spreads)

def test_monte_carlo_simulation(simulator):
    """Test Monte Carlo simulation generation."""
    num_sims = 5
    duration = 10
    simulations = simulator.generate_monte_carlo(num_simulations=num_sims, duration=duration)
    
    # Check number of simulations
    assert len(simulations) == num_sims
    
    # Check simulation properties
    for sim in simulations:
        assert len(sim) == duration
        assert all(col in sim.columns for col in ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        assert all(sim['high'] >= sim['close'])
        assert all(sim['low'] <= sim['close'])
        assert all(sim['volume'] > 0)

def test_combine_scenarios(simulator):
    """Test combining multiple market scenarios."""
    scenarios = [
        {
            'type': 'volatility',
            'start_idx': 2,
            'duration': 2,
            'parameters': {'intensity': 2.0}
        },
        {
            'type': 'trend',
            'start_idx': 4,
            'duration': 3,
            'parameters': {'trend_strength': 0.01}
        }
    ]
    
    result = simulator.combine_scenarios(scenarios)
    
    # Check that the result has the same structure as the input data
    assert len(result) == len(simulator.base_data)
    assert all(col in result.columns for col in simulator.base_data.columns)
    
    # Check that the data is modified
    assert not result.equals(simulator.base_data)

def test_edge_cases(simulator):
    """Test edge cases and error handling."""
    # Test with invalid start index
    result = simulator.add_volatility_spike(start_idx=len(simulator.base_data) + 1, duration=3)
    assert result.equals(simulator.base_data)
    
    # Test with zero duration
    result = simulator.simulate_trend(start_idx=2, duration=0)
    assert result.equals(simulator.base_data)
    
    # Test with negative gap
    result = simulator.simulate_gap(index=3, gap_percent=-5.0)
    assert all(result.iloc[3:]['close'] < simulator.base_data.iloc[3:]['close'])

def test_reproducibility(sample_data):
    """Test that results are reproducible with the same random seed."""
    sim1 = MarketSimulator(sample_data, random_seed=42)
    sim2 = MarketSimulator(sample_data, random_seed=42)
    
    result1 = sim1.add_volatility_spike(start_idx=2, duration=3)
    result2 = sim2.add_volatility_spike(start_idx=2, duration=3)
    
    assert result1.equals(result2) 