from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from pydantic import BaseModel, Field
import numpy as np

class MarketContext(BaseModel):
    """Market context information for zone validation."""
    overall_trend: str = Field(..., description="Overall market trend: 'bullish', 'bearish', or 'sideways'")
    volatility: float = Field(..., description="Current market volatility (e.g., ATR)")
    volume_profile: Dict[str, float] = Field(..., description="Volume profile metrics")
    regime: str = Field(..., description="Market regime: 'trending', 'ranging', 'volatile'")

class Zone(BaseModel):
    """
    Model representing a supply or demand zone in the market.
    
    A zone is an area of price where significant buying (demand) or selling (supply)
    has occurred in the past, and is likely to act as support/resistance in the future.
    """
    id: str = Field(..., description="Unique identifier for the zone")
    zone_type: str = Field(..., description="Type of zone: 'supply' or 'demand'")
    price_high: float = Field(..., description="Upper price boundary of the zone")
    price_low: float = Field(..., description="Lower price boundary of the zone")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the zone was first identified"
    )
    last_tested: Optional[datetime] = Field(
        None,
        description="Timestamp when the zone was last tested by price"
    )
    test_count: int = Field(
        default=0,
        description="Number of times price has tested this zone"
    )
    strength: float = Field(
        default=1.0,
        description="Zone strength score (0.0 to 1.0), decreases with each test"
    )
    formation_volume: Optional[float] = Field(
        None,
        description="Volume during zone formation"
    )
    formation_candles: Optional[List[Dict]] = Field(
        None,
        description="OHLCV data of candles that formed this zone"
    )
    metadata: Dict = Field(
        default_factory=dict,
        description="Additional metadata about the zone"
    )
    market_context: Optional[MarketContext] = Field(
        None,
        description="Market context when zone was formed"
    )
    cluster_strength: float = Field(
        default=1.0,
        description="Strength based on nearby zones (cluster analysis)"
    )
    
    def update_strength(self, test_result: bool, market_context: Optional[MarketContext] = None) -> None:
        """
        Update zone strength based on test result and market context.
        
        Args:
            test_result: True if zone held (price reversed), False if zone broke
            market_context: Optional current market context for strength adjustment
        """
        # Base decay factors
        base_hold_decay = 0.9
        base_break_decay = 0.5
        
        # Adjust decay based on market context if available
        if market_context:
            # Strengthen zones that align with overall trend
            trend_alignment = (
                (market_context.overall_trend == 'bullish' and self.zone_type == 'demand') or
                (market_context.overall_trend == 'bearish' and self.zone_type == 'supply')
            )
            if trend_alignment:
                base_hold_decay = min(0.95, base_hold_decay + 0.05)
                base_break_decay = min(0.6, base_break_decay + 0.1)
            
            # Adjust for volatility
            if market_context.volatility > 1.5:  # High volatility
                base_hold_decay = max(0.85, base_hold_decay - 0.05)
                base_break_decay = max(0.4, base_break_decay - 0.1)
            
            # Consider market regime
            if market_context.regime == 'ranging':
                base_hold_decay = min(0.95, base_hold_decay + 0.05)
            elif market_context.regime == 'volatile':
                base_hold_decay = max(0.85, base_hold_decay - 0.05)
        
        # Apply decay to strength
        decay_factor = base_hold_decay if test_result else base_break_decay
        self.strength *= decay_factor
        
        # Update test count and timestamp
        self.test_count += 1
        self.last_tested = datetime.utcnow()
        
        # Update market context if provided
        if market_context:
            self.market_context = market_context
    
    def calculate_age_score(self, max_age_hours: float = 168) -> float:
        """
        Calculate age-based score using a more sophisticated decay function.
        
        Args:
            max_age_hours: Maximum age in hours before zone is considered inactive
                         (default 168 = 1 week)
        
        Returns:
            float: Age score between 0 and 1
        """
        age_hours = (datetime.utcnow() - self.created_at).total_seconds() / 3600
        
        if age_hours > max_age_hours:
            return 0.0
            
        # Use a sigmoid decay function for smoother transition
        half_life = max_age_hours / 2
        decay_rate = -np.log(2) / half_life
        age_score = 1 / (1 + np.exp(-decay_rate * (max_age_hours - age_hours)))
        
        return float(age_score)
    
    def is_active(self, max_age_hours: float = 168, min_strength: float = 0.2) -> bool:
        """
        Check if the zone is still considered active using multiple criteria.
        
        Args:
            max_age_hours: Maximum age in hours before zone is considered inactive
            min_strength: Minimum strength threshold for activity
            
        Returns:
            bool: True if zone is active, False otherwise
        """
        # Check basic strength threshold
        if self.strength < min_strength:
            return False
            
        # Calculate age score
        age_score = self.calculate_age_score(max_age_hours)
        if age_score == 0:
            return False
            
        # Consider market context if available
        if self.market_context:
            # Deactivate zones that strongly oppose the overall trend
            trend_opposition = (
                (self.market_context.overall_trend == 'strongly_bullish' and self.zone_type == 'supply') or
                (self.market_context.overall_trend == 'strongly_bearish' and self.zone_type == 'demand')
            )
            if trend_opposition and self.strength < 0.4:  # Higher threshold for opposing zones
                return False
        
        return True
    
    def get_mid_price(self) -> float:
        """Get the middle price of the zone."""
        return (self.price_high + self.price_low) / 2
    
    def get_size(self) -> float:
        """Get the size (height) of the zone in price units."""
        return self.price_high - self.price_low
    
    def contains_price(self, price: float) -> bool:
        """Check if a price is within the zone."""
        return self.price_low <= price <= self.price_high
    
    def overlaps_with(self, other: 'Zone') -> bool:
        """Check if this zone overlaps with another zone."""
        return (
            self.price_low <= other.price_high and
            self.price_high >= other.price_low
        )
    
    def calculate_cluster_strength(self, nearby_zones: List['Zone'], max_distance: float = 100.0) -> float:
        """
        Calculate strength based on cluster analysis of nearby zones.
        
        Args:
            nearby_zones: List of other zones to consider
            max_distance: Maximum price distance to consider for clustering
            
        Returns:
            float: Cluster strength score between 0 and 1
        """
        if not nearby_zones:
            return self.strength
            
        cluster_scores = []
        mid_price = self.get_mid_price()
        
        for zone in nearby_zones:
            if zone.id == self.id:
                continue
                
            # Calculate price distance
            other_mid = zone.get_mid_price()
            distance = abs(mid_price - other_mid)
            
            if distance > max_distance:
                continue
                
            # Calculate distance-weighted strength contribution
            distance_factor = 1 - (distance / max_distance)
            type_alignment = 1.0 if zone.zone_type == self.zone_type else 0.5
            
            cluster_scores.append(zone.strength * distance_factor * type_alignment)
        
        if not cluster_scores:
            return self.strength
            
        # Combine individual zone strength with cluster strength
        cluster_strength = np.mean(cluster_scores)
        self.cluster_strength = (self.strength * 0.7) + (cluster_strength * 0.3)
        
        return self.cluster_strength
    
    def merge_with(self, other: 'Zone') -> 'Zone':
        """
        Merge this zone with another overlapping zone.
        
        The merged zone takes the outer boundaries of both zones and
        combines their metadata. The strength is the average weighted
        by the respective volumes.
        """
        if not self.overlaps_with(other):
            raise ValueError("Cannot merge non-overlapping zones")
            
        if self.zone_type != other.zone_type:
            raise ValueError("Cannot merge supply and demand zones")
            
        # Take outer boundaries
        merged_high = max(self.price_high, other.price_high)
        merged_low = min(self.price_low, other.price_low)
        
        # Combine formation volumes if available
        vol1 = self.formation_volume or 0
        vol2 = other.formation_volume or 0
        merged_volume = vol1 + vol2
        
        # Weight strength by volume and cluster strength
        if merged_volume > 0:
            merged_strength = (
                (self.strength * self.cluster_strength * vol1 +
                 other.strength * other.cluster_strength * vol2) /
                (merged_volume * (self.cluster_strength + other.cluster_strength) / 2)
            )
        else:
            merged_strength = (
                (self.strength * self.cluster_strength +
                 other.strength * other.cluster_strength) /
                (self.cluster_strength + other.cluster_strength)
            )
            
        # Combine formation candles
        merged_candles = []
        if self.formation_candles:
            merged_candles.extend(self.formation_candles)
        if other.formation_candles:
            merged_candles.extend(other.formation_candles)
            
        # Merge market context if available
        merged_context = None
        if self.market_context and other.market_context:
            # Take the more recent context
            merged_context = (
                self.market_context if self.created_at > other.created_at
                else other.market_context
            )
            
        # Combine metadata
        merged_metadata = {
            **self.metadata,
            **other.metadata,
            'merged_from': [self.id, other.id],
            'merged_at': datetime.utcnow().isoformat()
        }
        
        return Zone(
            id=f"merged_{self.id}_{other.id}",
            zone_type=self.zone_type,
            price_high=merged_high,
            price_low=merged_low,
            created_at=min(self.created_at, other.created_at),
            last_tested=max(
                self.last_tested or self.created_at,
                other.last_tested or other.created_at
            ),
            test_count=self.test_count + other.test_count,
            strength=merged_strength,
            formation_volume=merged_volume if merged_volume > 0 else None,
            formation_candles=merged_candles if merged_candles else None,
            metadata=merged_metadata,
            market_context=merged_context,
            cluster_strength=max(self.cluster_strength, other.cluster_strength)
        ) 