import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime

class MarketSimulator:
    """
    A class to simulate different market scenarios by modifying historical price data.
    """
    
    def __init__(self, base_data: pd.DataFrame, random_seed: int = None):
        """
        Initialize the market simulator.
        
        Args:
            base_data: DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            random_seed: Seed for random number generation
        """
        self.base_data = base_data.copy()
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def add_trend(self, data: pd.DataFrame, start_idx: int, duration: int, trend_strength: float) -> pd.DataFrame:
        """Add a trend to the price data."""
        result = data.copy()
        trend = np.linspace(0, trend_strength * duration, duration)
        
        for i, strength in enumerate(trend):
            if start_idx + i < len(result):
                multiplier = 1 + strength
                result.iloc[start_idx + i, 1:5] *= multiplier  # Apply to OHLC
        
        return result
    
    def add_volatility_spike(self, data: pd.DataFrame, start_idx: int, duration: int, intensity: float) -> pd.DataFrame:
        """Add increased volatility to the price data."""
        result = data.copy()
        
        for i in range(duration):
            if start_idx + i < len(result):
                noise = np.random.normal(0, intensity/100)
                multiplier = 1 + noise
                result.iloc[start_idx + i, 1:5] *= multiplier  # Apply to OHLC
        
        return result
    
    def add_gap(self, data: pd.DataFrame, start_idx: int, gap_percent: float) -> pd.DataFrame:
        """Add a price gap to the data."""
        result = data.copy()
        
        if start_idx < len(result):
            multiplier = 1 + (gap_percent / 100)
            result.iloc[start_idx:, 1:5] *= multiplier  # Apply to OHLC
        
        return result
    
    def combine_scenarios(self, scenarios: List[Dict]) -> pd.DataFrame:
        """
        Combine multiple market scenarios.
        
        Args:
            scenarios: List of scenario dictionaries, each containing:
                - type: 'trend', 'volatility', or 'gap'
                - start_idx: Starting index for the scenario
                - duration: Length of the scenario (not used for gaps)
                - parameters: Dict of scenario-specific parameters
        """
        result = self.base_data.copy()
        
        for scenario in scenarios:
            scenario_type = scenario['type']
            start_idx = scenario['start_idx']
            
            if scenario_type == 'trend':
                result = self.add_trend(
                    result,
                    start_idx,
                    scenario['duration'],
                    scenario['parameters']['trend_strength']
                )
            elif scenario_type == 'volatility':
                result = self.add_volatility_spike(
                    result,
                    start_idx,
                    scenario['duration'],
                    scenario['parameters']['intensity']
                )
            elif scenario_type == 'gap':
                result = self.add_gap(
                    result,
                    start_idx,
                    scenario['parameters']['gap_percent']
                )
        
        return result 