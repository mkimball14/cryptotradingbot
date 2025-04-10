import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from app.core.data_processor import OHLCVProcessor

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing"""
    data = [
        {
            'timestamp': '2024-01-01T00:00:00Z',
            'open': '29100.00',
            'high': '29500.00',
            'low': '29000.00',
            'close': '29400.00',
            'volume': '150.5'
        },
        {
            'timestamp': '2024-01-01T01:00:00Z',
            'open': '29400.00',
            'high': '29800.00',
            'low': '29300.00',
            'close': '29700.00',
            'volume': '220.3'
        },
        {
            'timestamp': '2024-01-01T02:00:00Z',
            'open': '29700.00',
            'high': '30100.00',
            'low': '29600.00',
            'close': '30000.00',
            'volume': '310.8'
        }
    ]
    return pd.DataFrame(data)

@pytest.fixture
def processor():
    """Create an OHLCVProcessor instance"""
    return OHLCVProcessor(decimal_places=2)

def test_normalize_data(processor, sample_df):
    """Test data normalization"""
    df = processor.normalize_data(sample_df)
    
    # Check data types
    assert pd.api.types.is_datetime64_any_dtype(df['timestamp'])
    assert all(pd.api.types.is_float_dtype(df[col]) for col in ['open', 'high', 'low', 'close', 'volume'])
    
    # Check UTC timezone
    assert df['timestamp'].dt.tz == timezone.utc
    
    # Check decimal places
    assert all(df['open'].apply(lambda x: len(str(x).split('.')[-1])) <= 2)
    assert all(df['volume'].apply(lambda x: len(str(x).split('.')[-1])) <= 8)
    
    # Check sorting
    assert df['timestamp'].is_monotonic_increasing

def test_validate_data_clean(processor, sample_df):
    """Test validation with clean data"""
    df = processor.normalize_data(sample_df)
    issues = processor.validate_data(df)
    
    # Should have no issues
    assert all(len(issues[key]) == 0 for key in issues.keys())

def test_validate_data_with_issues():
    """Test validation with problematic data"""
    # Create DataFrame with various issues
    data = [
        {
            'timestamp': '2024-01-01T00:00:00Z',
            'open': np.nan,  # Missing value
            'high': '28000.00',  # Price anomaly
            'low': '29000.00',  # High/low violation
            'close': '29400.00',
            'volume': '1500000.0'  # Volume anomaly
        },
        {
            'timestamp': '2024-01-01T03:00:00Z',  # Time gap
            'open': '29400.00',
            'high': '29300.00',  # High/low violation
            'low': '29500.00',
            'close': '29700.00',
            'volume': '220.3'
        }
    ]
    df = pd.DataFrame(data)
    processor = OHLCVProcessor()
    df = processor.normalize_data(df)
    issues = processor.validate_data(df)
    
    # Check for expected issues
    assert len(issues['missing_values']) > 0
    assert len(issues['high_low_violations']) > 0
    assert len(issues['timestamp_gaps']) > 0
    assert len(issues['volume_anomalies']) > 0

def test_clean_data(processor):
    """Test data cleaning"""
    # Create DataFrame with issues to clean
    data = [
        {
            'timestamp': '2024-01-01T00:00:00Z',
            'open': np.nan,
            'high': '29500.00',
            'low': '29000.00',
            'close': '29400.00',
            'volume': '150.5'
        },
        {
            'timestamp': '2024-01-01T01:00:00Z',
            'open': '29400.00',
            'high': '29300.00',  # Invalid high
            'low': '29500.00',   # Invalid low
            'close': '29700.00',
            'volume': '220.3'
        }
    ]
    df = pd.DataFrame(data)
    df = processor.normalize_data(df)
    cleaned_df = processor.clean_data(df)
    
    # Check that missing values were handled
    assert not cleaned_df['open'].isnull().any()
    
    # Check that high/low violations were fixed
    assert all(cleaned_df['high'] >= cleaned_df['low'])
    assert all(cleaned_df['high'] >= cleaned_df['open'])
    assert all(cleaned_df['high'] >= cleaned_df['close'])
    assert all(cleaned_df['low'] <= cleaned_df['open'])
    assert all(cleaned_df['low'] <= cleaned_df['close'])

def test_enrich_data(processor, sample_df):
    """Test data enrichment"""
    df = processor.normalize_data(sample_df)
    enriched_df = processor.enrich_data(df)
    
    # Check that new columns were added
    expected_columns = [
        'typical_price', 'body_size', 'upper_shadow', 'lower_shadow',
        'price_change', 'returns', 'volume_ma', 'volume_std', 'is_doji'
    ]
    for col in expected_columns:
        assert col in enriched_df.columns
    
    # Check calculations
    assert enriched_df['typical_price'].equals(
        (enriched_df['high'] + enriched_df['low'] + enriched_df['close']) / 3
    )
    assert enriched_df['body_size'].equals(
        abs(enriched_df['close'] - enriched_df['open'])
    )

def test_process_ohlcv(processor, sample_df):
    """Test complete processing pipeline"""
    processed_df = processor.process_ohlcv(sample_df)
    
    # Check that all processing steps were applied
    assert pd.api.types.is_datetime64_any_dtype(processed_df['timestamp'])
    assert all(pd.api.types.is_float_dtype(processed_df[col]) for col in ['open', 'high', 'low', 'close', 'volume'])
    assert 'typical_price' in processed_df.columns
    assert not processed_df.isnull().any().any()
    assert all(processed_df['high'] >= processed_df['low'])

def test_error_handling(processor):
    """Test error handling with invalid input"""
    # Test with invalid DataFrame
    with pytest.raises(Exception):
        processor.process_ohlcv(pd.DataFrame({'invalid': [1, 2, 3]}))
    
    # Test with empty DataFrame
    empty_df = processor.process_ohlcv(pd.DataFrame())
    assert len(empty_df) == 0
    
    # Test with missing required columns
    invalid_df = pd.DataFrame({
        'timestamp': ['2024-01-01T00:00:00Z'],
        'open': [100.0]
        # Missing other required columns
    })
    with pytest.raises(Exception):
        processor.process_ohlcv(invalid_df) 