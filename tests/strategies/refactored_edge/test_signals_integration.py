import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import copy

from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.config import EdgeConfig, SignalStrictness
# Assuming regime enum/constants are here - adjust import if necessary
# from scripts.strategies.refactored_edge.regime import MarketRegime 
from pandas.testing import assert_series_equal

# --- Test Data Fixtures ---

@pytest.fixture
def sample_data():
    """Provides basic pandas Series data for testing."""
    index = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'])
    data = {
        'close': pd.Series([100, 101, 102, 103, 104], index=index),
        'rsi': pd.Series([40, 45, 50, 55, 60], index=index),
        'bb_upper': pd.Series([105, 106, 107, 108, 109], index=index),
        'bb_lower': pd.Series([95, 96, 97, 98, 99], index=index),
        'trend_ma': pd.Series([98, 99, 100, 101, 102], index=index),
        'demand_zone': pd.Series([False, False, True, False, False], index=index),
        'supply_zone': pd.Series([False, False, False, False, True], index=index),
    }
    return data

@pytest.fixture
def base_params():
    """Provides a base parameter dictionary."""
    return {
        'rsi_lower_threshold': 30,
        'rsi_upper_threshold': 70,
        'use_zones': True,
        'trend_strict': True,
        'min_hold_period': 2,
        'trend_threshold_pct': 0.01,
        'zone_influence': 0.5,
        'use_regime_filter': False, # Default off
        'signal_strictness': SignalStrictness.BALANCED, # Default
        # '_regime_info': {} # Not present by default
    }

@pytest.fixture
def trending_regime_info():
    return {'predominant_regime': 'trending', 'trending_pct': 75.0, 'ranging_pct': 25.0}

@pytest.fixture
def ranging_regime_info():
    return {'predominant_regime': 'ranging', 'trending_pct': 30.0, 'ranging_pct': 70.0}

@pytest.fixture
def expected_trending_params(base_params, trending_regime_info):
    """Expected parameters after trending regime adaptation."""
    params = copy.deepcopy(base_params)
    params['rsi_lower_threshold'] = max(25, base_params['rsi_lower_threshold'] - 5) # 30-5=25 -> max(25,25)=25
    params['rsi_upper_threshold'] = min(75, base_params['rsi_upper_threshold'] + 5) # 70+5=75 -> min(75,75)=75
    params['trend_strict'] = True # Stays True
    params['min_hold_period'] = max(base_params['min_hold_period'], 3) # max(2,3)=3
    params['zone_influence'] = min(0.3, base_params['zone_influence']) # min(0.3,0.5)=0.3
    # Add keys that generate_signals uses internally but aren't directly adapted
    params['_regime_info'] = trending_regime_info # Ensure this is present for the adapted case
    params['use_regime_filter'] = True
    return params

@pytest.fixture
def expected_ranging_params(base_params, ranging_regime_info):
    """Expected parameters after ranging regime adaptation."""
    params = copy.deepcopy(base_params)
    params['rsi_lower_threshold'] = min(35, base_params['rsi_lower_threshold'] + 5) # 30+5=35 -> min(35,35)=35
    params['rsi_upper_threshold'] = max(65, base_params['rsi_upper_threshold'] - 5) # 70-5=65 -> max(65,65)=65
    params['trend_strict'] = False # Changes to False
    params['min_hold_period'] = min(base_params['min_hold_period'], 2) # min(2,2)=2
    params['zone_influence'] = max(0.7, base_params['zone_influence']) # max(0.7,0.5)=0.7
    # Add keys that generate_signals uses internally but aren't directly adapted
    params['_regime_info'] = ranging_regime_info # Ensure this is present for the adapted case
    params['use_regime_filter'] = True
    return params


# --- Test Functions ---

# Mock the default underlying function (balanced signals)
@patch('scripts.strategies.refactored_edge.signals_integration.balanced_signals.generate_balanced_signals', return_value=(pd.Series(), pd.Series(), pd.Series(), pd.Series()))
@patch('scripts.strategies.refactored_edge.signals_integration.is_testing_mode', return_value=False)
def test_regime_trending_adjusts_params(mock_is_testing_mode, mock_balanced_generator, sample_data, base_params, trending_regime_info, expected_trending_params):
    """Verify params are adjusted correctly for TRENDING regime when filter is ON."""
    test_params = copy.deepcopy(base_params)
    test_params['use_regime_filter'] = True
    test_params['_regime_info'] = trending_regime_info

    generate_signals(
        close=sample_data['close'],
        rsi=sample_data['rsi'],
        bb_upper=sample_data['bb_upper'],
        bb_lower=sample_data['bb_lower'],
        trend_ma=sample_data['trend_ma'],
        price_in_demand_zone=sample_data['demand_zone'],
        price_in_supply_zone=sample_data['supply_zone'],
        params=test_params
    )

    # Assert the mock was called with the CORRECTLY ADAPTED parameters
    mock_balanced_generator.assert_called_once()
    call_args, call_kwargs = mock_balanced_generator.call_args
    # Check individual arguments passed to the mock, based on balanced_signals signature
    assert call_kwargs.get('rsi_lower_threshold') == expected_trending_params['rsi_lower_threshold']
    assert call_kwargs.get('rsi_upper_threshold') == expected_trending_params['rsi_upper_threshold']
    assert call_kwargs.get('use_zones') == expected_trending_params['use_zones']
    assert call_kwargs.get('trend_strict') == expected_trending_params['trend_strict']
    assert call_kwargs.get('min_hold_period') == expected_trending_params['min_hold_period']
    assert call_kwargs.get('trend_threshold_pct') == expected_trending_params['trend_threshold_pct']
    assert call_kwargs.get('zone_influence') == expected_trending_params['zone_influence']
    # Verify strictness is passed correctly (though not adapted by regime)
    assert call_kwargs.get('strictness') == expected_trending_params['signal_strictness']

@patch('scripts.strategies.refactored_edge.signals_integration.balanced_signals.generate_balanced_signals', return_value=(pd.Series(), pd.Series(), pd.Series(), pd.Series()))
@patch('scripts.strategies.refactored_edge.signals_integration.is_testing_mode', return_value=False)
def test_regime_ranging_adjusts_params(mock_is_testing_mode, mock_balanced_generator, sample_data, base_params, ranging_regime_info, expected_ranging_params):
    """Verify params are adjusted correctly for RANGING regime when filter is ON."""
    test_params = copy.deepcopy(base_params)
    test_params['use_regime_filter'] = True
    test_params['_regime_info'] = ranging_regime_info

    generate_signals(
        close=sample_data['close'],
        rsi=sample_data['rsi'],
        bb_upper=sample_data['bb_upper'],
        bb_lower=sample_data['bb_lower'],
        trend_ma=sample_data['trend_ma'],
        price_in_demand_zone=sample_data['demand_zone'],
        price_in_supply_zone=sample_data['supply_zone'],
        params=test_params
    )

    # Assert the mock was called with the CORRECTLY ADAPTED parameters
    mock_balanced_generator.assert_called_once()
    call_args, call_kwargs = mock_balanced_generator.call_args
    # Check individual arguments passed to the mock, based on balanced_signals signature
    assert call_kwargs.get('rsi_lower_threshold') == expected_ranging_params['rsi_lower_threshold']
    assert call_kwargs.get('rsi_upper_threshold') == expected_ranging_params['rsi_upper_threshold']
    assert call_kwargs.get('use_zones') == expected_ranging_params['use_zones']
    assert call_kwargs.get('trend_strict') == expected_ranging_params['trend_strict']
    assert call_kwargs.get('min_hold_period') == expected_ranging_params['min_hold_period']
    assert call_kwargs.get('trend_threshold_pct') == expected_ranging_params['trend_threshold_pct']
    assert call_kwargs.get('zone_influence') == expected_ranging_params['zone_influence']
    assert call_kwargs.get('strictness') == expected_ranging_params['signal_strictness']

@patch('scripts.strategies.refactored_edge.signals_integration.balanced_signals.generate_balanced_signals', return_value=(pd.Series(), pd.Series(), pd.Series(), pd.Series()))
@patch('scripts.strategies.refactored_edge.signals_integration.is_testing_mode', return_value=False)
def test_regime_filter_off_uses_base_params(mock_is_testing_mode, mock_balanced_generator, sample_data, base_params, trending_regime_info):
    """Verify base params are used when regime filter is OFF, regardless of regime info."""
    test_params = copy.deepcopy(base_params)
    test_params['use_regime_filter'] = False # Explicitly OFF
    test_params['_regime_info'] = trending_regime_info # Regime info present but filter off

    generate_signals(
        close=sample_data['close'],
        rsi=sample_data['rsi'],
        bb_upper=sample_data['bb_upper'],
        bb_lower=sample_data['bb_lower'],
        trend_ma=sample_data['trend_ma'],
        price_in_demand_zone=sample_data['demand_zone'],
        price_in_supply_zone=sample_data['supply_zone'],
        params=test_params
    )

    # Assert the mock was called with the ORIGINAL base parameters
    mock_balanced_generator.assert_called_once()
    call_args, call_kwargs = mock_balanced_generator.call_args
    # Check individual arguments passed to the mock match the original test_params
    assert call_kwargs.get('rsi_lower_threshold') == test_params['rsi_lower_threshold']
    assert call_kwargs.get('rsi_upper_threshold') == test_params['rsi_upper_threshold']
    assert call_kwargs.get('use_zones') == test_params['use_zones']
    assert call_kwargs.get('trend_strict') == test_params['trend_strict']
    assert call_kwargs.get('min_hold_period') == test_params['min_hold_period']
    assert call_kwargs.get('trend_threshold_pct') == test_params['trend_threshold_pct']
    assert call_kwargs.get('zone_influence') == test_params['zone_influence']
    assert call_kwargs.get('strictness') == test_params['signal_strictness']

@patch('scripts.strategies.refactored_edge.signals_integration.balanced_signals.generate_balanced_signals', return_value=(pd.Series(), pd.Series(), pd.Series(), pd.Series()))
@patch('scripts.strategies.refactored_edge.signals_integration.is_testing_mode', return_value=False)
def test_regime_info_missing_uses_base_params(mock_is_testing_mode, mock_balanced_generator, sample_data, base_params):
    """Verify base params are used when regime info is missing, even if filter is ON."""
    test_params = copy.deepcopy(base_params)
    test_params['use_regime_filter'] = True # Filter ON
    # _regime_info is deliberately missing from test_params
    assert '_regime_info' not in test_params

    generate_signals(
        close=sample_data['close'],
        rsi=sample_data['rsi'],
        bb_upper=sample_data['bb_upper'],
        bb_lower=sample_data['bb_lower'],
        trend_ma=sample_data['trend_ma'],
        price_in_demand_zone=sample_data['demand_zone'],
        price_in_supply_zone=sample_data['supply_zone'],
        params=test_params
    )

    # Assert the mock was called with the ORIGINAL parameters
    mock_balanced_generator.assert_called_once()
    call_args, call_kwargs = mock_balanced_generator.call_args
    # Check individual arguments passed to the mock match the original test_params
    assert call_kwargs.get('rsi_lower_threshold') == test_params['rsi_lower_threshold']
    assert call_kwargs.get('rsi_upper_threshold') == test_params['rsi_upper_threshold']
    assert call_kwargs.get('use_zones') == test_params['use_zones']
    assert call_kwargs.get('trend_strict') == test_params['trend_strict']
    assert call_kwargs.get('min_hold_period') == test_params['min_hold_period']
    assert call_kwargs.get('trend_threshold_pct') == test_params['trend_threshold_pct']
    assert call_kwargs.get('zone_influence') == test_params['zone_influence']
    assert call_kwargs.get('strictness') == test_params['signal_strictness']

# --- Test for Actual Signal Differences --- 

@patch('scripts.strategies.refactored_edge.signals_integration.is_testing_mode', return_value=False)
def test_signals_differ_between_regimes(mock_is_testing_mode, sample_data, base_params, trending_regime_info, ranging_regime_info):
    """Verify that the actual generated signals differ between regimes when the filter is ON."""
    # --- Run with TRENDING regime --- 
    trending_params = copy.deepcopy(base_params)
    trending_params['use_regime_filter'] = True
    trending_params['_regime_info'] = trending_regime_info
    
    trending_signals = generate_signals(
        close=sample_data['close'],
        rsi=sample_data['rsi'],
        bb_upper=sample_data['bb_upper'],
        bb_lower=sample_data['bb_lower'],
        trend_ma=sample_data['trend_ma'],
        price_in_demand_zone=sample_data['demand_zone'],
        price_in_supply_zone=sample_data['supply_zone'],
        params=trending_params
    )
    
    # --- Run with RANGING regime --- 
    ranging_params = copy.deepcopy(base_params)
    ranging_params['use_regime_filter'] = True
    ranging_params['_regime_info'] = ranging_regime_info
    
    ranging_signals = generate_signals(
        close=sample_data['close'],
        rsi=sample_data['rsi'],
        bb_upper=sample_data['bb_upper'],
        bb_lower=sample_data['bb_lower'],
        trend_ma=sample_data['trend_ma'],
        price_in_demand_zone=sample_data['demand_zone'],
        price_in_supply_zone=sample_data['supply_zone'],
        params=ranging_params
    )
    
    # --- Assertions --- 
    # Check that at least one set of signals (e.g., long entries) is different
    # We use .equals() for Series comparison. Assert they are NOT equal.
    # Note: This assumes the sample_data and parameter adjustments are sufficient
    # to actually cause a difference in output signals.
    
    # Compare long entries
    try:
        assert_series_equal(trending_signals[0], ranging_signals[0])
        long_entries_equal = True
    except AssertionError:
        long_entries_equal = False
        
    # Compare long exits
    try:
        assert_series_equal(trending_signals[1], ranging_signals[1])
        long_exits_equal = True
    except AssertionError:
        long_exits_equal = False

    # Compare short entries
    try:
        assert_series_equal(trending_signals[2], ranging_signals[2])
        short_entries_equal = True
    except AssertionError:
        short_entries_equal = False
        
    # Compare short exits
    try:
        assert_series_equal(trending_signals[3], ranging_signals[3])
        short_exits_equal = True
    except AssertionError:
        short_exits_equal = False

    # Assert that *at least one* pair of corresponding signals is different
    assert not (long_entries_equal and long_exits_equal and short_entries_equal and short_exits_equal), \
        "Expected signals to differ between TRENDING and RANGING regimes, but all signals were identical."
