import pytest
from src.risk_manager import calculate_position_size, calculate_stop_loss, calculate_take_profit, get_zone_confidence_tier, check_daily_drawdown, check_consecutive_losses, check_max_open_positions

# Use pytest.approx for float comparisons
from pytest import approx

# Need Zone model for confidence test
from src.database.models import Zone 

def test_calculate_position_size_long():
    """Test position sizing for a long trade."""
    balance = 10000.0
    risk_perc = 1.0  # 1% risk
    entry = 50000.0
    stop_loss = 49500.0 # $500 risk per unit
    decimals = 4 # e.g., BTC allows 0.0001 units

    expected_risk_amount = balance * (risk_perc / 100.0) # $100
    risk_per_unit = abs(entry - stop_loss) # 500.0
    expected_raw_size = expected_risk_amount / risk_per_unit # 100 / 500 = 0.2
    expected_size = 0.2000 # Already fits decimals
    expected_actual_risk = expected_size * risk_per_unit # 0.2 * 500 = 100.0

    size, risk_amount = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals)

    assert size == approx(expected_size)
    assert risk_amount == approx(expected_actual_risk)

def test_calculate_position_size_short():
    """Test position sizing for a short trade."""
    balance = 5000.0
    risk_perc = 2.0  # 2% risk
    entry = 3000.0
    stop_loss = 3050.0 # $50 risk per unit
    decimals = 2 # e.g., ETH allows 0.01 units

    expected_risk_amount = balance * (risk_perc / 100.0) # $100
    risk_per_unit = abs(entry - stop_loss) # 50.0
    expected_raw_size = expected_risk_amount / risk_per_unit # 100 / 50 = 2.0
    expected_size = 2.00 # Already fits decimals
    expected_actual_risk = expected_size * risk_per_unit # 2.0 * 50 = 100.0

    size, risk_amount = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals)

    assert size == approx(expected_size)
    assert risk_amount == approx(expected_actual_risk)

def test_calculate_position_size_rounding():
    """Test position sizing when rounding down is required."""
    balance = 10000.0
    risk_perc = 1.0  # $100 risk
    entry = 100.0
    stop_loss = 97.0 # $3 risk per unit
    decimals = 1 # e.g., Asset allows 0.1 units

    risk_per_unit = 3.0
    expected_raw_size = 100.0 / risk_per_unit # 33.333...
    # multiplier = 10^1 = 10
    # floor(33.333 * 10) / 10 = floor(333.33) / 10 = 333 / 10 = 33.3
    expected_size = 33.3 
    expected_actual_risk = expected_size * risk_per_unit # 33.3 * 3 = 99.9

    size, risk_amount = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals)

    assert size == approx(expected_size)
    assert risk_amount == approx(expected_actual_risk)
    assert risk_amount <= (balance * (risk_perc / 100.0)) # Ensure actual risk doesn't exceed target

def test_calculate_position_size_invalid_inputs():
    """Test invalid inputs return zero size and risk."""
    # Zero risk distance
    assert calculate_position_size(10000, 1, 50000, 50000) == (0.0, 0.0)
    # Negative balance
    assert calculate_position_size(-10000, 1, 50000, 49500) == (0.0, 0.0)
    # Zero risk percentage
    assert calculate_position_size(10000, 0, 50000, 49500) == (0.0, 0.0)
    # Negative price
    assert calculate_position_size(10000, 1, -50000, 49500) == (0.0, 0.0)
    assert calculate_position_size(10000, 1, 50000, -49500) == (0.0, 0.0)

def test_calculate_position_size_zero_size():
    """Test scenario resulting in zero calculated size (e.g., very small risk amount vs risk per unit)."""
    balance = 100.0
    risk_perc = 0.1 # $0.1 risk
    entry = 50000.0
    stop_loss = 49000.0 # $1000 risk per unit
    decimals = 8

    # raw size = 0.1 / 1000 = 0.0001
    # This should be calculated correctly if decimals allow
    size, risk_amount = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals)
    assert size == approx(0.0001)
    assert risk_amount == approx(0.1) 

    # Scenario where rounding leads to zero
    balance = 1000.0
    risk_perc = 0.01 # $0.1 risk
    entry = 100
    stop_loss = 90 # $10 risk per unit
    decimals = 1 # Asset allows 0.1 units
    # raw size = 0.1 / 10 = 0.01
    # floor(0.01 * 10) / 10 = floor(0.1) / 10 = 0 / 10 = 0.0
    size_zero, risk_amount_zero = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals)
    assert size_zero == 0.0
    assert risk_amount_zero == 0.0 

def test_calculate_position_size_confidence_adjustment():
    """Test position sizing adjustment based on confidence tier."""
    balance = 10000.0
    risk_perc = 1.0  # Base 1% risk -> $100
    entry = 50000.0
    stop_loss = 49500.0 # $500 risk per unit
    decimals = 4

    # High confidence (no adjustment)
    size_high, risk_high = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals, confidence_tier="high")
    assert size_high == approx(0.2000)
    assert risk_high == approx(100.0)

    # Medium confidence (0.66x adjustment)
    size_med, risk_med = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals, confidence_tier="medium")
    expected_risk_med = 100.0 * 0.66 # 66.0
    expected_raw_size_med = expected_risk_med / 500.0 # 0.132
    expected_size_med = 0.1320
    expected_actual_risk_med = expected_size_med * 500.0 # 66.0
    assert size_med == approx(expected_size_med)
    assert risk_med == approx(expected_actual_risk_med)

    # Low confidence (0.33x adjustment)
    size_low, risk_low = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals, confidence_tier="low")
    expected_risk_low = 100.0 * 0.33 # 33.0
    expected_raw_size_low = expected_risk_low / 500.0 # 0.066
    expected_size_low = 0.0660
    expected_actual_risk_low = expected_size_low * 500.0 # 33.0
    assert size_low == approx(expected_size_low)
    assert risk_low == approx(expected_actual_risk_low)

    # No confidence tier provided (should use base risk)
    size_none, risk_none = calculate_position_size(balance, risk_perc, entry, stop_loss, decimals, confidence_tier=None)
    assert size_none == approx(0.2000)
    assert risk_none == approx(100.0)

# --- Stop Loss Tests ---

def test_calculate_stop_loss_demand():
    """Test SL calculation for demand zones."""
    # No ATR
    sl1 = calculate_stop_loss(zone_type='demand', zone_low=100.0, zone_high=102.0, entry_price=101.0)
    assert sl1 == approx(100.0 - (102.0 - 100.0) * 0.1) # zone_low - 10% of height
    assert sl1 == approx(99.8)

    # With ATR
    sl2 = calculate_stop_loss(zone_type='demand', zone_low=100.0, zone_high=102.0, entry_price=101.0, atr_value=1.0, atr_multiplier=0.5)
    assert sl2 == approx(100.0 - 1.0 * 0.5)
    assert sl2 == approx(99.5)
    
    # Invalid Entry (below zone)
    assert calculate_stop_loss(zone_type='demand', zone_low=100.0, zone_high=102.0, entry_price=99.0) is None

def test_calculate_stop_loss_supply():
    """Test SL calculation for supply zones."""
    # No ATR
    sl1 = calculate_stop_loss(zone_type='supply', zone_low=200.0, zone_high=205.0, entry_price=204.0)
    assert sl1 == approx(205.0 + (205.0 - 200.0) * 0.1) # zone_high + 10% of height
    assert sl1 == approx(205.5)
    
    # With ATR
    sl2 = calculate_stop_loss(zone_type='supply', zone_low=200.0, zone_high=205.0, entry_price=204.0, atr_value=2.0, atr_multiplier=1.0)
    assert sl2 == approx(205.0 + 2.0 * 1.0)
    assert sl2 == approx(207.0)

    # Invalid Entry (above zone)
    assert calculate_stop_loss(zone_type='supply', zone_low=200.0, zone_high=205.0, entry_price=206.0) is None

def test_calculate_stop_loss_invalid_zone():
    """Test SL calculation with invalid zone inputs."""
    assert calculate_stop_loss(zone_type='demand', zone_low=100.0, zone_high=98.0, entry_price=101.0) is None # Low > High
    assert calculate_stop_loss(zone_type='demand', zone_low=-100.0, zone_high=102.0, entry_price=101.0) is None # Negative low
    assert calculate_stop_loss(zone_type='invalid', zone_low=100.0, zone_high=102.0, entry_price=101.0) is None # Invalid type

# --- Take Profit Tests ---

def test_calculate_take_profit_demand():
    """Test TP calculation for demand (long) trade."""
    entry = 101.0
    sl = 99.5 # Risk distance = 1.5
    # R:R = 2.0 (default)
    tp1 = calculate_take_profit(zone_type='demand', entry_price=entry, stop_loss_price=sl)
    assert tp1 == approx(entry + (1.5 * 2.0))
    assert tp1 == approx(104.0)

    # R:R = 3.0
    tp2 = calculate_take_profit(zone_type='demand', entry_price=entry, stop_loss_price=sl, risk_reward_ratio=3.0)
    assert tp2 == approx(entry + (1.5 * 3.0))
    assert tp2 == approx(105.5)

    # Invalid SL (>= entry)
    assert calculate_take_profit(zone_type='demand', entry_price=101.0, stop_loss_price=101.5) is None

def test_calculate_take_profit_supply():
    """Test TP calculation for supply (short) trade."""
    entry = 204.0
    sl = 207.0 # Risk distance = 3.0
    # R:R = 1.5
    tp1 = calculate_take_profit(zone_type='supply', entry_price=entry, stop_loss_price=sl, risk_reward_ratio=1.5)
    assert tp1 == approx(entry - (3.0 * 1.5))
    assert tp1 == approx(199.5)

    # R:R = 1.0
    tp2 = calculate_take_profit(zone_type='supply', entry_price=entry, stop_loss_price=sl, risk_reward_ratio=1.0)
    assert tp2 == approx(entry - (3.0 * 1.0))
    assert tp2 == approx(201.0)

    # Invalid SL (<= entry)
    assert calculate_take_profit(zone_type='supply', entry_price=204.0, stop_loss_price=203.5) is None

def test_calculate_take_profit_invalid_inputs():
    """Test TP calculation with invalid inputs."""
    assert calculate_take_profit(zone_type='demand', entry_price=100, stop_loss_price=98, risk_reward_ratio=-1.0) is None # Negative R:R
    assert calculate_take_profit(zone_type='demand', entry_price=-100, stop_loss_price=98, risk_reward_ratio=2.0) is None # Negative entry
    assert calculate_take_profit(zone_type='demand', entry_price=100, stop_loss_price=-98, risk_reward_ratio=2.0) is None # Negative SL
    assert calculate_take_profit(zone_type='invalid', entry_price=100, stop_loss_price=98, risk_reward_ratio=2.0) is None # Invalid type 

# --- Confidence Tier Tests ---

def test_get_zone_confidence_tier():
    """Test the logic for determining zone confidence tiers."""
    # High: Fresh=10, Strength > 60
    zone_high = Zone(initial_freshness_score=10, initial_strength_score=75)
    assert get_zone_confidence_tier(zone_high) == "high"

    # Medium: Fresh=5 (Strength irrelevant for this case)
    zone_med1 = Zone(initial_freshness_score=5, initial_strength_score=80)
    assert get_zone_confidence_tier(zone_med1) == "medium"
    zone_med2 = Zone(initial_freshness_score=5, initial_strength_score=40)
    assert get_zone_confidence_tier(zone_med2) == "medium"

    # Medium: Fresh=10, Strength <= 60
    zone_med3 = Zone(initial_freshness_score=10, initial_strength_score=60)
    assert get_zone_confidence_tier(zone_med3) == "medium"
    zone_med4 = Zone(initial_freshness_score=10, initial_strength_score=30)
    assert get_zone_confidence_tier(zone_med4) == "medium"

    # Low: Fresh=1 (already touched twice)
    zone_low1 = Zone(initial_freshness_score=1, initial_strength_score=90)
    assert get_zone_confidence_tier(zone_low1) == "low"
    zone_low2 = Zone(initial_freshness_score=1, initial_strength_score=20)
    assert get_zone_confidence_tier(zone_low2) == "low"

    # Low: Missing scores (defaults to 0)
    zone_low3 = Zone() # No scores set
    assert get_zone_confidence_tier(zone_low3) == "low"
    zone_low4 = Zone(initial_freshness_score=10) # Missing strength
    assert get_zone_confidence_tier(zone_low4) == "low"
    zone_low5 = Zone(initial_strength_score=80) # Missing freshness
    assert get_zone_confidence_tier(zone_low5) == "low" 

# --- Circuit Breaker Tests ---

def test_check_daily_drawdown():
    """Test daily drawdown checks."""
    start_balance = 10000
    max_dd = 5.0 # 5%

    # No drawdown
    assert check_daily_drawdown(10000, start_balance, max_dd) is False
    # Small drawdown
    assert check_daily_drawdown(9800, start_balance, max_dd) is False # 2% DD
    # Drawdown at limit
    assert check_daily_drawdown(9500, start_balance, max_dd) is True # 5% DD
    # Drawdown exceeded limit
    assert check_daily_drawdown(9400, start_balance, max_dd) is True # 6% DD
    # Balance increased (negative drawdown)
    assert check_daily_drawdown(10100, start_balance, max_dd) is False # -1% DD
    # Invalid inputs
    assert check_daily_drawdown(9500, 0, max_dd) is False # Zero start balance
    assert check_daily_drawdown(9500, start_balance, 0) is False # Zero max dd
    assert check_daily_drawdown(9500, start_balance, -5.0) is False # Negative max dd

def test_check_consecutive_losses():
    """Test consecutive loss checks."""
    max_losses = 3

    # No losses
    assert check_consecutive_losses(['win', 'win'], max_losses) is False
    # Some losses, not consecutive at end
    assert check_consecutive_losses(['loss', 'loss', 'win'], max_losses) is False
    assert check_consecutive_losses(['loss', 'win', 'loss', 'loss'], max_losses) is False # 2 consecutive
    # Exactly max losses
    assert check_consecutive_losses(['win', 'loss', 'loss', 'loss'], max_losses) is True # 3 consecutive
    # More than max losses
    assert check_consecutive_losses(['loss', 'loss', 'loss', 'loss'], max_losses) is True # 4 consecutive
    # All losses
    assert check_consecutive_losses(['loss'] * 5, max_losses) is True
    # Empty list
    assert check_consecutive_losses([], max_losses) is False
    # Invalid max_losses
    assert check_consecutive_losses(['loss', 'loss'], 0) is False
    assert check_consecutive_losses(['loss', 'loss'], -1) is False

def test_check_max_open_positions():
    """Test max open position checks."""
    max_pos = 3

    # Below limit
    assert check_max_open_positions(0, max_pos) is False
    assert check_max_open_positions(1, max_pos) is False
    assert check_max_open_positions(2, max_pos) is False
    # At limit (should return True, as opening one *more* would exceed)
    assert check_max_open_positions(3, max_pos) is True
    # Above limit (should return True)
    assert check_max_open_positions(4, max_pos) is True
    # Invalid limit
    assert check_max_open_positions(2, 0) is False
    assert check_max_open_positions(2, -1) is False 