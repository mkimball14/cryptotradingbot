from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from pydantic import BaseModel, Field
import numpy as np
import pandas as pd

from app.models.zone import Zone, MarketContext
from app.core.indicators import calculate_rsi, calculate_macd, VolumeProfile
# Import risk management functions directly
from app.core.risk_manager import (
    calculate_position_size, 
    get_zone_confidence_tier, 
    # Add other functions if needed by SignalManager later
)

logger = logging.getLogger(__name__)

class SignalConfirmation(BaseModel):
    """Model representing the confirmation status of a trading signal."""
    is_confirmed: bool = Field(..., description="Whether the signal is confirmed")
    confidence_score: float = Field(..., description="Confidence score (0.0 to 1.0)")
    confirmation_time: datetime = Field(default_factory=datetime.utcnow)
    confirmation_factors: Dict[str, float] = Field(
        ...,
        description="Individual confirmation factor scores"
    )
    metadata: Dict = Field(default_factory=dict)

class SignalManager:
    """Manages signal confirmation using multiple technical indicators and market context."""
    
    def __init__(self):
        """Initialize the SignalManager."""
        # No risk_manager instance needed if functions are imported directly
        pass 
        
    def analyze_market_context(
        self,
        prices: List[float],
        volumes: List[float],
        timeframe_minutes: int
    ) -> MarketContext:
        """
        Analyze current market context using multiple indicators.
        
        Args:
            prices: List of closing prices
            volumes: List of volume data
            timeframe_minutes: Timeframe in minutes
            
        Returns:
            MarketContext: Current market context
        """
        # Calculate trend using multiple timeframes
        short_ma = np.mean(prices[-20:])
        medium_ma = np.mean(prices[-50:])
        long_ma = np.mean(prices[-200:]) if len(prices) >= 200 else medium_ma
        
        # Determine trend strength and direction
        trend_strength = abs((short_ma - long_ma) / long_ma)
        if trend_strength < 0.01:
            trend = 'sideways'
        elif short_ma > long_ma:
            trend = 'strongly_bullish' if trend_strength > 0.03 else 'bullish'
        else:
            trend = 'strongly_bearish' if trend_strength > 0.03 else 'bearish'
            
        # Calculate volatility using ATR-based method
        high_prices = [p * 1.001 for p in prices]  # Simulate high prices
        low_prices = [p * 0.999 for p in prices]   # Simulate low prices
        ranges = []
        for i in range(1, len(prices)):
            true_range = max(
                high_prices[i] - low_prices[i],
                abs(high_prices[i] - prices[i-1]),
                abs(low_prices[i] - prices[i-1])
            )
            ranges.append(true_range)
        volatility = np.mean(ranges[-14:]) / prices[-1]  # 14-period ATR
        
        # Analyze volume profile
        volume_profile = VolumeProfile(prices[-100:], volumes[-100:])
        profile_metrics = {
            'poc_price': volume_profile.point_of_control,
            'value_area_high': volume_profile.value_area_high,
            'value_area_low': volume_profile.value_area_low,
            'volume_concentration': volume_profile.calculate_concentration()
        }
        
        # Determine market regime
        if volatility > 0.015:  # High volatility threshold
            regime = 'volatile'
        elif trend in ['strongly_bullish', 'strongly_bearish']:
            regime = 'trending'
        else:
            regime = 'ranging'
            
        return MarketContext(
            overall_trend=trend,
            volatility=volatility,
            volume_profile=profile_metrics,
            regime=regime
        )
    
    async def confirm_zone_signal(
        self,
        zone: Zone,
        prices: List[float],
        volumes: List[float],
        timeframe_minutes: int
    ) -> SignalConfirmation:
        """
        Confirm a trading signal based on zone analysis and multiple indicators.
        
        Args:
            zone: The supply/demand zone to analyze
            prices: List of closing prices
            volumes: List of volume data
            timeframe_minutes: Timeframe in minutes
            
        Returns:
            SignalConfirmation: Signal confirmation status and details
        """
        confirmation_factors = {}
        
        # Get current market context
        market_context = self.analyze_market_context(prices, volumes, timeframe_minutes)
        
        # 1. Zone Strength Analysis (25% weight)
        zone_strength = zone.strength * zone.cluster_strength
        confirmation_factors['zone_strength'] = zone_strength
        
        # 2. RSI Analysis with Divergence (20% weight)
        rsi_values = calculate_rsi(prices)
        rsi_score = self._analyze_rsi(
            prices, rsi_values, zone.zone_type == 'demand'
        )
        confirmation_factors['rsi_analysis'] = rsi_score
        
        # 3. MACD Analysis (15% weight)
        macd_line, signal_line, histogram = calculate_macd(prices)
        macd_score = self._analyze_macd(
            macd_line, signal_line, histogram,
            zone.zone_type == 'demand'
        )
        confirmation_factors['macd_analysis'] = macd_score
        
        # 4. Volume Profile Analysis (15% weight)
        volume_score = self._analyze_volume_profile(
            zone, market_context.volume_profile
        )
        confirmation_factors['volume_analysis'] = volume_score
        
        # 5. Market Context Alignment (15% weight)
        context_score = self._analyze_market_context(
            zone, market_context
        )
        confirmation_factors['context_alignment'] = context_score
        
        # 6. Age-based Analysis (10% weight)
        age_score = zone.calculate_age_score()
        confirmation_factors['age_analysis'] = age_score
        
        # Calculate weighted confidence score
        weights = {
            'zone_strength': 0.25,
            'rsi_analysis': 0.20,
            'macd_analysis': 0.15,
            'volume_analysis': 0.15,
            'context_alignment': 0.15,
            'age_analysis': 0.10
        }
        
        confidence_score = sum(
            score * weights[factor]
            for factor, score in confirmation_factors.items()
        )
        
        # Update zone with current market context
        zone.update_strength(True, market_context)
        
        # Determine if signal is confirmed
        is_confirmed = (
            confidence_score >= 0.7 and  # High overall confidence
            zone_strength >= 0.5 and     # Strong zone
            context_score >= 0.6         # Good market alignment
        )
        
        return SignalConfirmation(
            is_confirmed=is_confirmed,
            confidence_score=confidence_score,
            confirmation_factors=confirmation_factors,
            metadata={
                'market_context': market_context.dict(),
                'timeframe_minutes': timeframe_minutes,
                'current_price': prices[-1],
                'zone_id': zone.id
            }
        )
    
    def _analyze_rsi(
        self,
        prices: List[float],
        rsi_values: List[float],
        is_demand: bool
    ) -> float:
        """
        Analyze RSI values for signal confirmation.
        
        Args:
            prices: List of closing prices
            rsi_values: List of RSI values
            is_demand: Whether this is a demand zone
            
        Returns:
            float: RSI analysis score (0.0 to 1.0)
        """
        if len(rsi_values) < 2:
            return 0.0
            
        current_rsi = rsi_values[-1]
        
        # Check for oversold/overbought conditions
        if is_demand and current_rsi < 30:
            base_score = 0.8
        elif not is_demand and current_rsi > 70:
            base_score = 0.8
        else:
            base_score = 0.5
            
        # Check for divergence
        price_change = (prices[-1] - prices[-2]) / prices[-2]
        rsi_change = rsi_values[-1] - rsi_values[-2]
        
        if is_demand:
            # Bullish divergence (price lower but RSI higher)
            if price_change < 0 and rsi_change > 0:
                base_score += 0.2
        else:
            # Bearish divergence (price higher but RSI lower)
            if price_change > 0 and rsi_change < 0:
                base_score += 0.2
                
        return min(base_score, 1.0)
    
    def _analyze_macd(
        self,
        macd_line: List[float],
        signal_line: List[float],
        histogram: List[float],
        is_demand: bool
    ) -> float:
        """
        Analyze MACD for signal confirmation.
        
        Args:
            macd_line: MACD line values
            signal_line: Signal line values
            histogram: MACD histogram values
            is_demand: Whether this is a demand zone
            
        Returns:
            float: MACD analysis score (0.0 to 1.0)
        """
        if len(histogram) < 2:
            return 0.0
            
        # Check for crossover
        current_hist = histogram[-1]
        prev_hist = histogram[-2]
        
        if is_demand:
            # Bullish crossover (histogram turns positive)
            if prev_hist < 0 and current_hist > 0:
                base_score = 0.8
            elif current_hist > 0:
                base_score = 0.6
            else:
                base_score = 0.4
        else:
            # Bearish crossover (histogram turns negative)
            if prev_hist > 0 and current_hist < 0:
                base_score = 0.8
            elif current_hist < 0:
                base_score = 0.6
            else:
                base_score = 0.4
                
        # Check for momentum
        momentum_factor = min(abs(current_hist) / 0.01, 0.2)  # Cap at 0.2
        
        return min(base_score + momentum_factor, 1.0)
    
    def _analyze_volume_profile(
        self,
        zone: Zone,
        volume_profile: Dict[str, float]
    ) -> float:
        """
        Analyze volume profile for signal confirmation.
        
        Args:
            zone: The zone being analyzed
            volume_profile: Current volume profile metrics
            
        Returns:
            float: Volume profile analysis score (0.0 to 1.0)
        """
        # Check if zone overlaps with value area
        zone_mid = zone.get_mid_price()
        in_value_area = (
            volume_profile['value_area_low'] <= zone_mid <= 
            volume_profile['value_area_high']
        )
        
        # Check proximity to POC
        poc_distance = abs(zone_mid - volume_profile['poc_price'])
        poc_proximity = max(0, 1 - (poc_distance / zone_mid * 100))
        
        # Consider volume concentration
        volume_concentration = volume_profile['volume_concentration']
        
        # Combine factors
        base_score = 0.4  # Base score
        if in_value_area:
            base_score += 0.3
        base_score += poc_proximity * 0.2
        base_score += volume_concentration * 0.1
        
        return min(base_score, 1.0)
    
    def _analyze_market_context(
        self,
        zone: Zone,
        market_context: MarketContext
    ) -> float:
        """
        Analyze market context alignment with the zone.
        
        Args:
            zone: The zone being analyzed
            market_context: Current market context
            
        Returns:
            float: Market context alignment score (0.0 to 1.0)
        """
        base_score = 0.5
        
        # Trend alignment
        trend_alignment = (
            (market_context.overall_trend in ['bullish', 'strongly_bullish'] and
             zone.zone_type == 'demand') or
            (market_context.overall_trend in ['bearish', 'strongly_bearish'] and
             zone.zone_type == 'supply')
        )
        if trend_alignment:
            base_score += 0.2
        elif market_context.overall_trend == 'sideways':
            base_score += 0.1
            
        # Volatility consideration
        if market_context.volatility < 0.01:  # Low volatility
            base_score += 0.1
        elif market_context.volatility > 0.02:  # High volatility
            base_score -= 0.1
            
        # Market regime alignment
        if market_context.regime == 'ranging':
            base_score += 0.1
        elif market_context.regime == 'volatile':
            base_score -= 0.1
            
        return max(0.0, min(base_score, 1.0))