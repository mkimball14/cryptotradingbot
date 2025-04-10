import math
import logging
from typing import Optional, Literal, List

# Import Zone model for type hinting
from src.database.models import Zone 

logger = logging.getLogger(__name__)

# Confidence Tier type hint
ConfidenceTier = Literal["high", "medium", "low"]

def get_zone_confidence_tier(zone: Zone) -> ConfidenceTier:
    """Determines a confidence tier ('high', 'medium', 'low') based on zone scores.
    
    Simple initial logic:
    - High: Freshness=10 AND Strength>60
    - Medium: Freshness=5 OR (Freshness=10 AND Strength<=60)
    - Low: Freshness=1 (already touched twice)
    (RSI not included in this basic version)
    """
    # Get raw scores, defaulting to None if attribute doesn't exist at all
    raw_freshness = getattr(zone, 'initial_freshness_score', None)
    raw_strength = getattr(zone, 'initial_strength_score', None)

    # Check if essential scores are missing
    if raw_freshness is None or raw_strength is None:
        return "low" # Assign low confidence if either score is missing
        
    # Now we know scores are not None, proceed with logic
    freshness = raw_freshness
    strength = raw_strength

    if freshness == 10 and strength > 60:
        return "high"
    elif freshness == 5 or (freshness == 10 and strength <= 60):
        return "medium"
    else: # Includes freshness == 1 
        return "low"

def calculate_position_size(
    account_balance: float,
    risk_percentage: float,
    entry_price: float,
    stop_loss_price: float,
    asset_decimals: int = 8, # Default to 8 for many cryptos
    confidence_tier: Optional[ConfidenceTier] = None # Added confidence tier
) -> tuple[float, float]:
    """Calculates the position size based on account risk, stop-loss distance, and optional confidence adjustment.

    Args:
        account_balance: The total available trading capital.
        risk_percentage: The BASE percentage of account balance to risk (e.g., 1.0 for 1%).
        entry_price: The intended entry price for the trade.
        stop_loss_price: The price where the stop-loss order will be placed.
        asset_decimals: The number of decimal places the asset quantity allows.
        confidence_tier: Optional confidence tier ('high', 'medium', 'low') to adjust risk.

    Returns:
        A tuple containing:
          - position_size (float): The calculated size of the position in the asset's units,
                                   rounded down to allowed decimals.
          - risk_amount_per_trade (float): The actual monetary amount risked (based on adjusted risk %).
        Returns (0.0, 0.0) if inputs are invalid or risk cannot be calculated.
    """
    if account_balance <= 0 or risk_percentage <= 0:
        logger.error("Account balance and base risk percentage must be positive.")
        return 0.0, 0.0
    
    if entry_price <= 0 or stop_loss_price <= 0:
        logger.error("Entry price and stop-loss price must be positive.")
        return 0.0, 0.0

    # Determine risk per unit based on trade direction (implied by SL relative to entry)
    risk_per_unit = abs(entry_price - stop_loss_price)

    if risk_per_unit <= 0:
        logger.error("Stop-loss price is too close to or the same as entry price. Cannot calculate position size.")
        return 0.0, 0.0

    # Adjust risk percentage based on confidence
    adjusted_risk_percentage = risk_percentage
    if confidence_tier == "medium":
        adjusted_risk_percentage *= 0.66 # Example: Reduce risk for medium confidence
        logger.info(f"Confidence tier is 'medium', adjusting risk percentage to {adjusted_risk_percentage:.2f}%")
    elif confidence_tier == "low":
        adjusted_risk_percentage *= 0.33 # Example: Reduce risk further for low confidence
        logger.info(f"Confidence tier is 'low', adjusting risk percentage to {adjusted_risk_percentage:.2f}%")
    elif confidence_tier == "high":
         logger.info("Confidence tier is 'high', using base risk percentage.")
    # else: No tier provided or invalid, use base risk percentage

    # Ensure adjusted risk is not negative (shouldn't happen)
    adjusted_risk_percentage = max(0.0, adjusted_risk_percentage)

    risk_amount_per_trade = account_balance * (adjusted_risk_percentage / 100.0)
    
    raw_position_size = risk_amount_per_trade / risk_per_unit

    # Adjust size based on allowed decimals (round down)
    if asset_decimals >= 0:
        multiplier = 10 ** asset_decimals
        position_size = math.floor(raw_position_size * multiplier) / multiplier
    else:
        # If decimals is negative or not specified appropriately, just floor to integer?
        # Or maybe treat as 0 decimals. Let's assume floor for now.
        position_size = math.floor(raw_position_size)
        
    # Ensure calculated size is not negative (shouldn't happen with checks above, but safety)
    position_size = max(0.0, position_size)

    # Recalculate actual risk amount based on rounded position size
    actual_risk_amount = position_size * risk_per_unit

    if position_size == 0:
        logger.warning(f"Calculated position size is zero for balance {account_balance}, adj. risk {adjusted_risk_percentage:.2f}%, entry {entry_price}, SL {stop_loss_price}")
        return 0.0, 0.0

    logger.info(f"Calculated Position Size: {position_size:.{asset_decimals}f}, Actual Risk Amount: {actual_risk_amount:.2f} (Adj. Risk %: {adjusted_risk_percentage:.2f})")
    return position_size, actual_risk_amount 

def calculate_stop_loss(
    zone_type: str,
    zone_low: float,
    zone_high: float,
    entry_price: float, # Optional, but good for validation
    atr_value: Optional[float] = None,
    atr_multiplier: float = 0.5
) -> Optional[float]:
    """Calculates the stop-loss price based on a supply/demand zone.

    Args:
        zone_type: 'supply' or 'demand'.
        zone_low: The low price of the zone.
        zone_high: The high price of the zone.
        entry_price: The entry price of the trade (used for validation).
        atr_value: Optional Average True Range value for buffer calculation.
        atr_multiplier: Multiplier for the ATR buffer.

    Returns:
        The calculated stop-loss price, or None if inputs are invalid.
    """
    if zone_type not in ['supply', 'demand']:
        logger.error(f"Invalid zone_type: {zone_type}")
        return None
    if zone_low <= 0 or zone_high <= 0 or zone_high <= zone_low:
        logger.error(f"Invalid zone prices: Low={zone_low}, High={zone_high}")
        return None
    if entry_price <= 0:
         logger.error(f"Invalid entry price: {entry_price}")
         return None
    if atr_value is not None and atr_value < 0:
        logger.warning("ATR value cannot be negative. Ignoring ATR buffer.")
        atr_value = None
    if atr_multiplier < 0:
        logger.warning("ATR multiplier cannot be negative. Using default 0.5.")
        atr_multiplier = 0.5
        
    buffer = 0.0
    if atr_value is not None:
        buffer = atr_value * atr_multiplier
    else:
        # Fallback buffer if ATR is not available (e.g., a small percentage of zone height or fixed pips)
        # Using a small percentage of zone height as a simple fallback
        zone_height = zone_high - zone_low
        buffer = zone_height * 0.1 # 10% of zone height as buffer
        if buffer == 0: # If zone height is tiny, use a minimal absolute buffer (needs context/config)
             # This part is tricky without knowing the asset's typical price range/volatility
             # Let's just log a warning if buffer ends up zero
             logger.warning("Calculated buffer is zero (ATR not provided and zone height is minimal).")

    stop_loss = None
    if zone_type == 'demand': # Buy trade, SL below zone low
        if entry_price < zone_low:
            logger.warning(f"Entry price {entry_price} is below demand zone low {zone_low}. Invalid trade setup for SL calc.")
            return None
        stop_loss = zone_low - buffer
    elif zone_type == 'supply': # Sell trade, SL above zone high
        if entry_price > zone_high:
             logger.warning(f"Entry price {entry_price} is above supply zone high {zone_high}. Invalid trade setup for SL calc.")
             return None
        stop_loss = zone_high + buffer

    # Ensure stop loss isn't negative and makes sense relative to entry
    if stop_loss is None or stop_loss <= 0:
        logger.error(f"Calculated stop loss {stop_loss} is invalid (zero or negative).")
        return None
    if zone_type == 'demand' and stop_loss >= entry_price:
         logger.error(f"Calculated stop loss {stop_loss} for demand is not below entry price {entry_price}.")
         return None
    if zone_type == 'supply' and stop_loss <= entry_price:
          logger.error(f"Calculated stop loss {stop_loss} for supply is not above entry price {entry_price}.")
          return None

    logger.info(f"Calculated SL for {zone_type} zone [{zone_low}-{zone_high}] with buffer {buffer:.5f}: {stop_loss:.5f}")
    return stop_loss 

def calculate_take_profit(
    zone_type: str,
    entry_price: float,
    stop_loss_price: float,
    risk_reward_ratio: float = 2.0
) -> Optional[float]:
    """Calculates the take-profit price based on entry, stop-loss, and R:R ratio.

    Args:
        zone_type: 'supply' or 'demand'. Determines trade direction.
        entry_price: The intended entry price for the trade.
        stop_loss_price: The calculated stop-loss price.
        risk_reward_ratio: The desired risk-to-reward ratio (e.g., 2.0 for 1:2).

    Returns:
        The calculated take-profit price, or None if inputs are invalid.
    """
    if zone_type not in ['supply', 'demand']:
        logger.error(f"Invalid zone_type: {zone_type}")
        return None
    if entry_price <= 0 or stop_loss_price <= 0:
        logger.error(f"Entry price {entry_price} or stop-loss {stop_loss_price} must be positive.")
        return None
    if risk_reward_ratio <= 0:
        logger.error(f"Risk-reward ratio {risk_reward_ratio} must be positive.")
        return None

    risk_distance = abs(entry_price - stop_loss_price)
    if risk_distance == 0: # Should be caught by SL calc, but double-check
        logger.error("Risk distance is zero. Cannot calculate take-profit.")
        return None

    profit_distance = risk_distance * risk_reward_ratio
    take_profit = None

    if zone_type == 'demand': # Buy trade
        if stop_loss_price >= entry_price: # SL should be below entry
             logger.error(f"Stop-loss {stop_loss_price} is not below entry {entry_price} for demand trade.")
             return None
        take_profit = entry_price + profit_distance
    elif zone_type == 'supply': # Sell trade
        if stop_loss_price <= entry_price: # SL should be above entry
             logger.error(f"Stop-loss {stop_loss_price} is not above entry {entry_price} for supply trade.")
             return None
        take_profit = entry_price - profit_distance
        
    # Ensure take_profit is positive
    if take_profit is None or take_profit <= 0:
        logger.error(f"Calculated take-profit {take_profit} is invalid (zero or negative).")
        return None
        
    logger.info(f"Calculated TP for {zone_type} trade (Entry: {entry_price}, SL: {stop_loss_price}, R:R: {risk_reward_ratio}): {take_profit:.5f}")
    return take_profit 

# --- Circuit Breaker / Advanced Controls ---

def check_daily_drawdown(
    current_balance: float, 
    start_of_day_balance: float, 
    max_drawdown_perc: float
) -> bool:
    """Checks if the maximum daily drawdown percentage has been exceeded.

    Args:
        current_balance: The current account balance.
        start_of_day_balance: The account balance at the start of the trading day.
        max_drawdown_perc: The maximum allowed drawdown percentage (e.g., 5.0 for 5%).

    Returns:
        True if drawdown is exceeded, False otherwise.
    """
    if start_of_day_balance <= 0 or max_drawdown_perc <= 0:
        logger.warning("Invalid inputs for drawdown check (start balance or max % <= 0).")
        return False # Cannot calculate drawdown reliably
        
    drawdown = (start_of_day_balance - current_balance) / start_of_day_balance * 100.0
    
    if drawdown >= max_drawdown_perc:
        logger.warning(f"CIRCUIT BREAKER: Daily drawdown {drawdown:.2f}% exceeded limit {max_drawdown_perc:.2f}%")
        return True
    return False

def check_consecutive_losses(
    recent_trade_outcomes: List[Literal["win", "loss"]], 
    max_consecutive_losses: int
) -> bool:
    """Checks if the maximum number of consecutive losses has been reached.

    Args:
        recent_trade_outcomes: A list of recent trade outcomes ('win' or 'loss'), 
                               ordered from oldest to newest.
        max_consecutive_losses: The maximum allowed consecutive losses.

    Returns:
        True if the limit is reached or exceeded, False otherwise.
    """
    if max_consecutive_losses <= 0:
        return False # Limit not set or invalid
        
    consecutive_losses = 0
    # Iterate backwards through the list to find the most recent consecutive losses
    for outcome in reversed(recent_trade_outcomes):
        if outcome == 'loss':
            consecutive_losses += 1
        else:
            # Stop counting as soon as we hit a win
            break 
            
    if consecutive_losses >= max_consecutive_losses:
        logger.warning(f"CIRCUIT BREAKER: Consecutive losses ({consecutive_losses}) reached limit ({max_consecutive_losses}).")
        return True
    return False

def check_max_open_positions(
    current_open_positions: int, 
    max_positions_allowed: int
) -> bool:
    """Checks if the maximum number of open positions would be exceeded by opening one more.

    Args:
        current_open_positions: The number of positions currently open.
        max_positions_allowed: The maximum number of positions allowed to be open simultaneously.

    Returns:
        True if opening another position would exceed the limit, False otherwise.
    """
    if max_positions_allowed <= 0:
        logger.debug("Max open positions limit not set or invalid (<=0).")
        return False # No limit enforced
        
    if current_open_positions >= max_positions_allowed:
        logger.warning(f"CANNOT OPEN: Max open positions ({max_positions_allowed}) reached.")
        return True
    return False