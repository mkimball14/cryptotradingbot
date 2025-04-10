import pytest
from datetime import datetime, timedelta
from app.models.zone import Zone

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

def test_zone_creation(sample_supply_zone: Zone):
    """Test zone creation with all fields."""
    assert sample_supply_zone.id == "test_supply_1"
    assert sample_supply_zone.zone_type == "supply"
    assert sample_supply_zone.price_high == 120.0
    assert sample_supply_zone.price_low == 118.0
    assert isinstance(sample_supply_zone.created_at, datetime)
    assert sample_supply_zone.test_count == 0
    assert sample_supply_zone.strength == 1.0
    assert sample_supply_zone.formation_volume == 1000.0
    assert len(sample_supply_zone.formation_candles) == 1

def test_zone_update_strength(sample_supply_zone: Zone):
    """Test zone strength updates based on test results."""
    # Test successful defense of zone
    initial_strength = sample_supply_zone.strength
    sample_supply_zone.update_strength(test_result=True)
    assert sample_supply_zone.strength == initial_strength * 0.9
    assert sample_supply_zone.test_count == 1
    assert sample_supply_zone.last_tested is not None
    
    # Test zone break
    sample_supply_zone.update_strength(test_result=False)
    assert sample_supply_zone.strength == initial_strength * 0.9 * 0.5
    assert sample_supply_zone.test_count == 2

def test_zone_is_active(sample_supply_zone: Zone):
    """Test zone activity status based on age and strength."""
    # Fresh zone should be active
    assert sample_supply_zone.is_active()
    
    # Old zone should be inactive
    old_zone = sample_supply_zone.copy()
    old_zone.created_at = datetime.utcnow() - timedelta(days=8)  # > 168 hours
    assert not old_zone.is_active()
    
    # Weak zone should be inactive
    weak_zone = sample_supply_zone.copy()
    weak_zone.strength = 0.1
    assert not weak_zone.is_active()

def test_zone_price_methods(sample_supply_zone: Zone):
    """Test zone price-related methods."""
    # Test mid price calculation
    assert sample_supply_zone.get_mid_price() == 119.0
    
    # Test zone size calculation
    assert sample_supply_zone.get_size() == 2.0
    
    # Test price containment
    assert sample_supply_zone.contains_price(119.0)
    assert sample_supply_zone.contains_price(118.0)
    assert sample_supply_zone.contains_price(120.0)
    assert not sample_supply_zone.contains_price(117.9)
    assert not sample_supply_zone.contains_price(120.1)

def test_zone_overlap(sample_supply_zone: Zone):
    """Test zone overlap detection."""
    # Create overlapping zone
    overlapping_zone = Zone(
        id="test_supply_2",
        zone_type="supply",
        price_high=119.0,
        price_low=117.0
    )
    assert sample_supply_zone.overlaps_with(overlapping_zone)
    
    # Create non-overlapping zone
    non_overlapping_zone = Zone(
        id="test_supply_3",
        zone_type="supply",
        price_high=117.0,
        price_low=115.0
    )
    assert not sample_supply_zone.overlaps_with(non_overlapping_zone)

def test_zone_merge(sample_supply_zone: Zone):
    """Test merging of overlapping zones."""
    # Create overlapping zone
    overlapping_zone = Zone(
        id="test_supply_2",
        zone_type="supply",
        price_high=119.0,
        price_low=117.0,
        formation_volume=500.0,
        formation_candles=[
            {
                "timestamp": datetime.utcnow() - timedelta(hours=2),
                "open": 118.0,
                "high": 119.0,
                "low": 117.0,
                "close": 118.0,
                "volume": 500.0
            }
        ]
    )
    
    # Test successful merge
    merged_zone = sample_supply_zone.merge_with(overlapping_zone)
    assert merged_zone.price_high == 120.0
    assert merged_zone.price_low == 117.0
    assert merged_zone.formation_volume == 1500.0
    assert len(merged_zone.formation_candles) == 2
    assert 'merged_from' in merged_zone.metadata
    assert len(merged_zone.metadata['merged_from']) == 2
    
    # Test merge with non-overlapping zone
    non_overlapping_zone = Zone(
        id="test_supply_3",
        zone_type="supply",
        price_high=117.0,
        price_low=115.0
    )
    with pytest.raises(ValueError, match="Cannot merge non-overlapping zones"):
        sample_supply_zone.merge_with(non_overlapping_zone)
    
    # Test merge with different zone type
    demand_zone = Zone(
        id="test_demand_1",
        zone_type="demand",
        price_high=119.0,
        price_low=117.0
    )
    with pytest.raises(ValueError, match="Cannot merge supply and demand zones"):
        sample_supply_zone.merge_with(demand_zone)

def test_zone_serialization(sample_supply_zone: Zone):
    """Test zone serialization and deserialization."""
    # Test serialization to dict
    zone_dict = sample_supply_zone.dict()
    assert isinstance(zone_dict, dict)
    assert zone_dict['id'] == sample_supply_zone.id
    assert zone_dict['zone_type'] == sample_supply_zone.zone_type
    assert zone_dict['price_high'] == sample_supply_zone.price_high
    assert zone_dict['price_low'] == sample_supply_zone.price_low
    
    # Test deserialization from dict
    new_zone = Zone(**zone_dict)
    assert new_zone.id == sample_supply_zone.id
    assert new_zone.zone_type == sample_supply_zone.zone_type
    assert new_zone.price_high == sample_supply_zone.price_high
    assert new_zone.price_low == sample_supply_zone.price_low 