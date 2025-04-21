#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional, Union
from pathlib import Path
import re
from datetime import datetime, timedelta
import copy
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("enhanced_parameter_suggestions")

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Import strategy modules
try:
    from scripts.strategies.edge_strategy_assistant import EnhancedEdgeStrategy, chat_with_vectorbt
    from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
    from scripts.strategies.chat_optimize_edge_strategy import analyze_current_market
    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    IMPORTS_AVAILABLE = False

# --- NEW JSON DEFAULT FUNCTION (Moved here) ---
def json_encoder_default(obj):
    """Custom default function for json.dump to handle non-serializable types."""
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float16, np.float32, np.float64)):
        # Handle potential infinity/NaN from numpy floats
        if np.isinf(obj) or np.isnan(obj):
            return None
        return float(obj)
    elif hasattr(np, 'floating') and isinstance(obj, np.floating):
        if np.isinf(obj) or np.isnan(obj):
            return None
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return str(obj) # Explicitly convert numpy and python bools to string
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (pd.Timestamp, datetime)):
        return obj.isoformat()
    elif isinstance(obj, (pd.Timedelta, timedelta)):
        return str(obj)
    elif pd.isna(obj):
        return None
    elif obj is pd.NA:
        return None
    # Add other specific type checks if needed
    
    # Default fallback: Raise TypeError so json.dump knows it wasn't handled
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
# --- END NEW JSON DEFAULT FUNCTION ---

# Define parameter constraints
PARAMETER_CONSTRAINTS = {
    # Parameter name: [min_value, max_value, default_value, description, category]
    'lookback_window': [5, 50, 20, 'Number of periods to look back for indicators', 'Window Size'],
    'vol_filter_window': [5, 50, 20, 'Window for volatility filter', 'Window Size'],
    'vol_window': [5, 50, 20, 'Window for volume calculations', 'Window Size'],
    'rsi_window': [5, 30, 14, 'RSI calculation window', 'Window Size'],
    'rsi_entry': [20, 40, 30, 'RSI level for trade entry', 'Entry Threshold'],
    'rsi_exit': [60, 80, 70, 'RSI level for trade exit', 'Exit Threshold'],
    'bb_dev': [1.0, 3.0, 2.0, 'Bollinger Band standard deviation multiplier', 'Volatility'],
    'volatility_threshold': [0.1, 0.5, 0.3, 'Minimum volatility required for trade entry', 'Volatility'],
    'sl_pct': [1.0, 5.0, 2.0, 'Stop loss percentage', 'Risk Management'],
    'tp_pct': [2.0, 10.0, 4.0, 'Take profit percentage', 'Risk Management'],
    'risk_per_trade': [0.01, 0.05, 0.02, 'Risk per trade (as fraction of capital)', 'Risk Management'],
    'max_active_positions': [1, 5, 3, 'Maximum number of active positions', 'Risk Management'],
}

def get_default_parameters() -> Dict[str, Any]:
    """
    Get default strategy parameters from PARAMETER_CONSTRAINTS.
    
    Returns:
        Dictionary with default parameter values
    """
    default_params = {}
    for param_name, constraints in PARAMETER_CONSTRAINTS.items():
        default_value = constraints[2]  # Default is the third element in the constraints list
        default_params[param_name] = default_value
    
    return default_params

# Define parameter relationship rules
PARAMETER_RELATIONSHIPS = [
    {
        "params": ["tp_pct", "sl_pct"],
        "rule": lambda p: p.get("tp_pct", 0) >= p.get("sl_pct", 0) * 2,
        "message": "Take profit should be at least 2x stop loss for favorable risk/reward ratio"
    },
    {
        "params": ["rsi_exit", "rsi_entry"],
        "rule": lambda p: p.get("rsi_exit", 0) - p.get("rsi_entry", 0) >= 30,
        "message": "Difference between RSI exit and entry should be at least 30 for effective trend identification"
    },
    {
        "params": ["bb_window", "lookback_window"],
        "rule": lambda p: p.get("bb_window", 0) >= p.get("lookback_window", 0) * 0.75,
        "message": "Bollinger Bands window should be at least 75% of lookback window for statistical significance"
    },
    {
        "params": ["vol_filter_window", "lookback_window"],
        "rule": lambda p: p.get("vol_filter_window", 0) >= p.get("lookback_window", 0) * 0.5,
        "message": "Volatility filter window should be at least 50% of lookback window for meaningful volatility assessment"
    },
    {
        "params": ["vol_window", "lookback_window"],
        "rule": lambda p: p.get("vol_window", 0) >= p.get("lookback_window", 0) * 0.5,
        "message": "Volume window should be at least 50% of lookback window for consistent volume analysis"
    },
    {
        "params": ["tp_pct", "volatility_threshold"],
        "rule": lambda p: p.get("tp_pct", 0) >= p.get("volatility_threshold", 0) * 4,
        "message": "Take profit should be at least 4x volatility threshold to ensure targets are aligned with expected price movement"
    },
    {
        "params": ["sl_pct", "volatility_threshold"],
        "rule": lambda p: p.get("sl_pct", 0) >= p.get("volatility_threshold", 0) * 1.5,
        "message": "Stop loss should be at least 1.5x volatility threshold to avoid premature stops from normal volatility"
    },
    {
        "params": ["bb_dev", "volatility_threshold"],
        "rule": lambda p: abs(p.get("bb_dev", 0) - p.get("volatility_threshold", 0) * 3) <= 1.5,
        "message": "Bollinger Band deviation should be roughly aligned with volatility threshold (typically 2-4x)"
    },
    {
        "params": ["risk_per_trade", "sl_pct"],
        "rule": lambda p: p.get("risk_per_trade", 0) * 10 <= p.get("sl_pct", 0),
        "message": "Risk per trade (as % of account) should generally not exceed 1/10 of stop loss percentage for proper position sizing"
    },
    {
        "params": ["rsi_window", "lookback_window"],
        "rule": lambda p: p.get("rsi_window", 0) <= p.get("lookback_window", 0),
        "message": "RSI window should not exceed lookback window for consistent indicator calculation"
    },
    {
        "params": ["rsi_entry", "rsi_exit", "rsi_window"],
        "rule": lambda p: (p.get("rsi_exit", 70) - p.get("rsi_entry", 30)) >= p.get("rsi_window", 14) * 1.5,
        "message": "RSI entry/exit gap should be at least 1.5x the RSI window size for statistical reliability"
    },
    {
        "params": ["lookback_window", "vol_filter_window", "bb_window", "vol_window", "rsi_window"],
        "rule": lambda p: min(
            p.get("lookback_window", 20), 
            p.get("vol_filter_window", 50), 
            p.get("bb_window", 20), 
            p.get("vol_window", 20),
            p.get("rsi_window", 14)
        ) >= 5,
        "message": "All window parameters should be at least 5 periods for minimum statistical validity"
    },
    {
        "params": ["tp_pct", "sl_pct", "risk_per_trade"],
        "rule": lambda p: (p.get("tp_pct", 4.0) / p.get("sl_pct", 2.0)) * p.get("risk_per_trade", 0.02) <= 0.05,
        "message": "The combination of risk/reward ratio and risk per trade should not expose more than 5% of account on a single opportunity"
    }
]

# Define expected performance metrics for different market regimes
PERFORMANCE_EXPECTATIONS = {
    "trending_bullish": {
        "win_rate": 0.65,
        "profit_factor": 2.2,
        "max_drawdown": -0.12,
        "trades_per_month": 6,
        "avg_trade_duration": 4.5,  # days
        "description": "Strong upward price movement with clear momentum and positive sentiment",
        "optimal_strategy": "Trend-following with trailing stops and pyramiding"
    },
    "trending_bullish_early": {
        "win_rate": 0.60,
        "profit_factor": 1.9,
        "max_drawdown": -0.15,
        "trades_per_month": 5,
        "avg_trade_duration": 3.5,  # days
        "description": "Early stage of bullish trend with recent breakout from consolidation",
        "optimal_strategy": "Momentum with breakout confirmation and moderate position sizing"
    },
    "trending_bullish_mature": {
        "win_rate": 0.55,
        "profit_factor": 1.6,
        "max_drawdown": -0.18,
        "trades_per_month": 4,
        "avg_trade_duration": 2.5,  # days
        "description": "Mature bullish trend showing signs of slowing momentum but still positive",
        "optimal_strategy": "Trend-following with tighter stops and reduced position size"
    },
    "trending_bearish": {
        "win_rate": 0.60,
        "profit_factor": 1.8,
        "max_drawdown": -0.18,
        "trades_per_month": 5,
        "avg_trade_duration": 3.0,  # days
        "description": "Strong downward price movement with clear negative momentum",
        "optimal_strategy": "Short positions with profit targets at support levels"
    },
    "trending_bearish_early": {
        "win_rate": 0.55,
        "profit_factor": 1.6,
        "max_drawdown": -0.20,
        "trades_per_month": 4,
        "avg_trade_duration": 2.5,  # days
        "description": "Early stage of bearish trend with recent breakdown from support",
        "optimal_strategy": "Short positions with breakdown confirmation"
    },
    "trending_bearish_mature": {
        "win_rate": 0.50,
        "profit_factor": 1.4,
        "max_drawdown": -0.22,
        "trades_per_month": 3,
        "avg_trade_duration": 2.0,  # days
        "description": "Mature bearish trend that may be approaching oversold conditions",
        "optimal_strategy": "Short positions with tighter stops and reduced size"
    },
    "volatile_high": {
        "win_rate": 0.45,
        "profit_factor": 1.4,
        "max_drawdown": -0.25,
        "trades_per_month": 10,
        "avg_trade_duration": 1.5,  # days
        "description": "High volatility with rapid price changes and potential trend reversals",
        "optimal_strategy": "Mean-reversion with strict stop losses and smaller position sizing"
    },
    "volatile_high_expanding": {
        "win_rate": 0.40,
        "profit_factor": 1.3,
        "max_drawdown": -0.28,
        "trades_per_month": 12,
        "avg_trade_duration": 1.0,  # days
        "description": "Expanding volatility with breakouts and potential regime change",
        "optimal_strategy": "Breakout strategies with very tight risk controls"
    },
    "volatile_low": {
        "win_rate": 0.50,
        "profit_factor": 1.5,
        "max_drawdown": -0.12,
        "trades_per_month": 3,
        "avg_trade_duration": 5.0,  # days
        "description": "Low volatility with moderate price changes and potential consolidation",
        "optimal_strategy": "Trend pullback strategies with wider stops"
    },
    "volatile_low_contracting": {
        "win_rate": 0.55,
        "profit_factor": 1.7,
        "max_drawdown": -0.10,
        "trades_per_month": 2,
        "avg_trade_duration": 6.0,  # days
        "description": "Contracting volatility often preceding a significant move",
        "optimal_strategy": "Breakout anticipation strategies with pending orders at boundaries"
    },
    "ranging_tight": {
        "win_rate": 0.60,
        "profit_factor": 1.7,
        "max_drawdown": -0.08,
        "trades_per_month": 8,
        "avg_trade_duration": 2.0,  # days
        "description": "Price moving within a tight range with clear support/resistance",
        "optimal_strategy": "Range trading with entries near boundaries and small targets"
    },
    "ranging_wide": {
        "win_rate": 0.50,
        "profit_factor": 1.5,
        "max_drawdown": -0.15,
        "trades_per_month": 5,
        "avg_trade_duration": 3.0,  # days
        "description": "Price moving within a wide range with multiple support/resistance levels",
        "optimal_strategy": "Mean-reversion with confirmation indicators"
    },
    "accumulation": {
        "win_rate": 0.45,
        "profit_factor": 1.3,
        "max_drawdown": -0.12,
        "trades_per_month": 3,
        "avg_trade_duration": 5.0,  # days
        "description": "Sideways price action with increasing volume suggesting accumulation",
        "optimal_strategy": "Breakout anticipation with volume confirmation"
    },
    "distribution": {
        "win_rate": 0.45,
        "profit_factor": 1.3,
        "max_drawdown": -0.15,
        "trades_per_month": 4,
        "avg_trade_duration": 3.0,  # days
        "description": "Sideways price action with increasing volume suggesting distribution",
        "optimal_strategy": "Breakdown anticipation with volume confirmation"
    },
    "reversal_potential": {
        "win_rate": 0.40,
        "profit_factor": 1.6,
        "max_drawdown": -0.18,
        "trades_per_month": 3,
        "avg_trade_duration": 4.0,  # days
        "description": "Market showing signs of potential trend reversal",
        "optimal_strategy": "Counter-trend strategies with strong confirmation signals"
    },
    "unknown": {
        "win_rate": 0.45,
        "profit_factor": 1.2,
        "max_drawdown": -0.20,
        "trades_per_month": 4,
        "avg_trade_duration": 3.0,  # days
        "description": "Undefined market regime with uncertain price direction",
        "optimal_strategy": "Reduced position sizing with diversified approach"
    }
}

def validate_and_adjust_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters against constraints and adjust if necessary.
    
    Args:
        params: Dictionary of parameters to validate
        
    Returns:
        Dictionary with validated parameters and issues
    """
    validated_params = {}
    issues = []
    
    # Check each parameter against constraints
    for param_name, value in params.items():
        if param_name in PARAMETER_CONSTRAINTS:
            constraints = PARAMETER_CONSTRAINTS[param_name]
            
            # Check if parameter is within constraints
            if value < constraints[0]:
                issues.append(f"{param_name} value {value} is below minimum of {constraints[0]}")
                validated_params[param_name] = constraints[0]
            elif value > constraints[1]:
                issues.append(f"{param_name} value {value} is above maximum of {constraints[1]}")
                validated_params[param_name] = constraints[1]
            else:
                validated_params[param_name] = value
        else:
            # Keep parameters that don't have constraints
            validated_params[param_name] = value
    
    # Add default values for missing parameters
    for param_name, constraints in PARAMETER_CONSTRAINTS.items():
        if param_name not in validated_params:
            validated_params[param_name] = constraints[2]
            issues.append(f"{param_name} was not provided, using default value of {constraints[2]}")
    
    # Validate parameter relationships
    relationship_issues = validate_parameter_relationships(validated_params)
    if relationship_issues:
        issues.extend([issue["message"] for issue in relationship_issues])
    
    return {
        "params": validated_params,
        "issues": issues,
        "relationship_issues": relationship_issues
    }

def validate_parameter_relationships(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Validate relationships between parameters.
    
    Args:
        params: Dictionary of parameters to validate
        
    Returns:
        List of relationship issues
    """
    issues = []
    
    # Check each relationship rule
    for relationship in PARAMETER_RELATIONSHIPS:
        # Check if all parameters in the relationship are present
        if all(param in params for param in relationship["params"]):
            # Evaluate the rule
            if not relationship["rule"](params):
                issues.append({
                    "params": relationship["params"],
                    "message": relationship["message"]
                })
    
    return issues

def get_enhanced_market_context(symbol: str, lookback_days: int = 30) -> Dict[str, Any]:
    """
    Get enhanced market context including price action, volatility, volume, and support/resistance.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTC-USD')
        lookback_days: Number of days to look back for market analysis
        
    Returns:
        Dictionary with market context information
    """
    try:
        # Import data fetcher (following the pattern used in other files)
        from data.data_fetcher import fetch_historical_data
        
        # Calculate start and end dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_days)
        
        # Fetch data with daily candles
        granularity = 86400  # Daily candles in seconds
        df = fetch_historical_data(
            product_id=symbol,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            granularity=granularity
        )
        
        if df.empty:
            return {"error": f"No data available for {symbol} in the specified time period"}
        
        # Calculate basic metrics
        current_price = df['close'].iloc[-1]
        start_price = df['close'].iloc[0]
        high_price = df['high'].max()
        low_price = df['low'].min()
        
        # Calculate price change
        price_change = current_price - start_price
        price_change_pct = (price_change / start_price) * 100
        
        # Add moving averages
        df['ma_20'] = df['close'].rolling(window=20).mean()
        df['ma_50'] = df['close'].rolling(window=50).mean()
        df['ma_200'] = df['close'].rolling(window=200).mean() if len(df) >= 200 else None
        
        # Calculate volatility (standard deviation of daily returns)
        daily_returns = df['close'].pct_change().dropna()
        volatility = daily_returns.std() * 100
        
        # Calculate recent volatility (last 10 days)
        recent_volatility = daily_returns.iloc[-10:].std() * 100 if len(daily_returns) >= 10 else volatility
        
        # Calculate volume metrics
        df['volume_ma_20'] = df['volume'].rolling(window=20).mean()
        start_volume = df['volume'].iloc[0]
        current_volume = df['volume'].iloc[-1]
        volume_change_pct = ((current_volume - start_volume) / start_volume) * 100 if start_volume > 0 else 0
        
        # Volume trend (increasing or decreasing)
        volume_trend = "increasing" if current_volume > df['volume_ma_20'].iloc[-1] else "decreasing"
        
        # Calculate ATR (Average True Range) for volatility assessment
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )
        df['atr_14'] = df['tr'].rolling(window=14).mean()
        current_atr = df['atr_14'].iloc[-1]
        atr_percent = (current_atr / current_price) * 100  # ATR as percentage of price
        
        # Measure volatility expansion/contraction
        recent_atr = df['atr_14'].iloc[-5:].mean()
        prev_atr = df['atr_14'].iloc[-10:-5].mean() if len(df) >= 10 else recent_atr
        volatility_expanding = recent_atr > prev_atr
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        current_rsi = df['rsi'].iloc[-1]
        
        # Determine if in a trading range
        recent_high = df['high'].iloc[-20:].max() if len(df) >= 20 else high_price
        recent_low = df['low'].iloc[-20:].min() if len(df) >= 20 else low_price
        price_range_pct = ((recent_high - recent_low) / recent_low) * 100
        
        # Detect if price is near key levels
        support_resistance = _analyze_support_resistance(df)
        near_support = False
        near_resistance = False
        
        if support_resistance:
            nearest_support = support_resistance.get('nearest_support', 0)
            nearest_resistance = support_resistance.get('nearest_resistance', 0)
            
            # Check if price is within 2% of support or resistance
            support_distance_pct = abs((current_price - nearest_support) / current_price) * 100
            resistance_distance_pct = abs((current_price - nearest_resistance) / current_price) * 100
            
            near_support = support_distance_pct < 2.0
            near_resistance = resistance_distance_pct < 2.0
        
        # Analyze market cycle
        market_cycle = _analyze_market_cycle(df)
        cycle_phase = market_cycle.get('cycle_phase', 'unknown') if market_cycle else 'unknown'
        
        # Determine trend direction and strength
        ma_20 = df['ma_20'].iloc[-1] if 'ma_20' in df and len(df) > 20 else None
        ma_50 = df['ma_50'].iloc[-1] if 'ma_50' in df and len(df) > 50 else None
        ma_200 = df['ma_200'].iloc[-1] if 'ma_200' in df and len(df) > 200 else None
        
        is_above_ma20 = current_price > ma_20 if ma_20 is not None else False
        is_above_ma50 = current_price > ma_50 if ma_50 is not None else False
        is_above_ma200 = current_price > ma_200 if ma_200 is not None else False
        
        ma20_above_ma50 = ma_20 > ma_50 if (ma_20 is not None and ma_50 is not None) else False
        ma50_above_ma200 = ma_50 > ma_200 if (ma_50 is not None and ma_200 is not None) else False
        
        # Enhanced trend detection
        if ma_20 is not None and ma_50 is not None:
            ma_20_slope = (ma_20 - df['ma_20'].iloc[-6]) / ma_20 * 100 if len(df) > 25 else 0
            ma_50_slope = (ma_50 - df['ma_50'].iloc[-6]) / ma_50 * 100 if len(df) > 55 else 0
        else:
            ma_20_slope = 0
            ma_50_slope = 0
            
        # Determine market regime based on all factors
        # Start with trend analysis
        if is_above_ma20 and is_above_ma50 and ma20_above_ma50:
            if price_change_pct > 15 and volatility < 5:
                if cycle_phase == "euphoria" or current_rsi > 70:
                    market_regime = "trending_bullish_mature"
                else:
                    market_regime = "trending_bullish"
            elif price_change_pct > 8 and volatility < 6:
                if ma_20_slope > 0.5:
                    market_regime = "trending_bullish_early"
                else:
                    market_regime = "trending_bullish"
            elif near_resistance and volume_trend == "increasing":
                market_regime = "distribution"
            elif price_range_pct < 8 and volume_trend == "increasing":
                market_regime = "accumulation"
            else:
                market_regime = "volatile_low"
        elif not is_above_ma20 and not is_above_ma50 and not ma20_above_ma50:
            if price_change_pct < -15 and volatility < 5:
                if cycle_phase == "capitulation" or current_rsi < 30:
                    market_regime = "trending_bearish_mature"
                else:
                    market_regime = "trending_bearish"
            elif price_change_pct < -8 and volatility < 6:
                if ma_20_slope < -0.5:
                    market_regime = "trending_bearish_early"
                else:
                    market_regime = "trending_bearish"
            elif near_support and volume_trend == "increasing":
                market_regime = "accumulation"
            elif price_range_pct < 8 and volume_trend == "increasing":
                market_regime = "distribution"
            else:
                market_regime = "volatile_low"
        # Check for ranging conditions
        elif abs(price_change_pct) < 8 and price_range_pct < 10:
            if price_range_pct < 5:
                market_regime = "ranging_tight"
            else:
                market_regime = "ranging_wide"
        # Check for volatility conditions
        elif volatility > 8:
            if volatility_expanding:
                market_regime = "volatile_high_expanding"
            else:
                market_regime = "volatile_high"
        elif volatility < 3:
            if volatility_expanding:
                market_regime = "volatile_low"
            else:
                market_regime = "volatile_low_contracting"
        # Check for potential reversal conditions
        elif (is_above_ma20 and not is_above_ma50) or (not is_above_ma20 and is_above_ma50):
            if (current_rsi < 30 and not is_above_ma20) or (current_rsi > 70 and is_above_ma20):
                market_regime = "reversal_potential"
            else:
                market_regime = "unknown"
        else:
            market_regime = "unknown"
        
        # Prepare comprehensive market context
        return {
            "symbol": symbol,
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "current_price": current_price,
            "price_change": price_change,
            "price_change_pct": price_change_pct,
            "high": high_price,
            "low": low_price,
            "volatility": volatility,
            "recent_volatility": recent_volatility,
            "volume_change_pct": volume_change_pct,
            "volume_trend": volume_trend,
            "atr_percent": atr_percent,
            "volatility_expanding": volatility_expanding,
            "rsi": current_rsi,
            "price_range_pct": price_range_pct,
            "near_support": near_support,
            "near_resistance": near_resistance,
            "is_above_ma20": is_above_ma20,
            "is_above_ma50": is_above_ma50,
            "is_above_ma200": is_above_ma200,
            "ma20_above_ma50": ma20_above_ma50,
            "ma50_above_ma200": ma50_above_ma200,
            "ma_20_slope": ma_20_slope,
            "ma_50_slope": ma_50_slope,
            "market_regime": market_regime,
            "support_resistance": support_resistance,
            "market_cycle": market_cycle,
            "performance_expectations": PERFORMANCE_EXPECTATIONS.get(market_regime, PERFORMANCE_EXPECTATIONS["unknown"])
        }
    
    except Exception as e:
        logger.error(f"Error getting market context: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def _analyze_support_resistance(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze support and resistance levels from historical price data.
    
    Args:
        df: DataFrame with OHLCV data
        
    Returns:
        Dictionary with support and resistance information
    """
    try:
        # Use pivot points to identify potential support and resistance levels
        highs = df['high'].values
        lows = df['low'].values
        closes = df['close'].values
        
        # Basic pivot point calculation (last day's pivot)
        last_high = highs[-2]
        last_low = lows[-2]
        last_close = closes[-2]
        
        pivot = (last_high + last_low + last_close) / 3
        
        # Support and resistance levels
        s1 = (2 * pivot) - last_high
        s2 = pivot - (last_high - last_low)
        r1 = (2 * pivot) - last_low
        r2 = pivot + (last_high - last_low)
        
        # Current price
        current_price = closes[-1]
        
        # Find nearest support and resistance
        supports = [s1, s2]
        resistances = [r1, r2]
        
        # Add recent lows as potential support
        for i in range(len(lows)-10, len(lows)-1):
            if i >= 0:
                # Check if this is a local minimum
                if i > 0 and i < len(lows)-1:
                    if lows[i] < lows[i-1] and lows[i] < lows[i+1]:
                        supports.append(lows[i])
        
        # Add recent highs as potential resistance
        for i in range(len(highs)-10, len(highs)-1):
            if i >= 0:
                # Check if this is a local maximum
                if i > 0 and i < len(highs)-1:
                    if highs[i] > highs[i-1] and highs[i] > highs[i+1]:
                        resistances.append(highs[i])
        
        # Sort supports and resistances
        supports = sorted([s for s in supports if s < current_price])
        resistances = sorted([r for r in resistances if r > current_price])
        
        # Find nearest levels
        nearest_support = supports[-1] if supports else s2
        nearest_resistance = resistances[0] if resistances else r1
        
        return {
            "pivot": pivot,
            "nearest_support": nearest_support,
            "nearest_resistance": nearest_resistance,
            "support_levels": supports[:3],  # Just the 3 strongest support levels
            "resistance_levels": resistances[:3],  # Just the 3 strongest resistance levels
            "price_to_support_pct": ((current_price - nearest_support) / current_price) * 100,
            "price_to_resistance_pct": ((nearest_resistance - current_price) / current_price) * 100
        }
    except Exception as e:
        logger.error(f"Error analyzing support and resistance: {str(e)}")
        return {}

def _analyze_market_cycle(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze market cycle to determine trend, momentum, and cycle phase.
    
    Args:
        df: DataFrame with OHLCV data
        
    Returns:
        Dictionary with market cycle information
    """
    try:
        # Calculate short and long moving averages
        df['ma_20'] = df['close'].rolling(window=20).mean()
        df['ma_50'] = df['close'].rolling(window=50).mean()
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Calculate volume trend
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        volume_trend = "increasing" if df['volume'].iloc[-1] > df['volume_ma'].iloc[-1] else "decreasing"
        
        # Calculate volatility trend
        df['volatility'] = df['close'].pct_change().rolling(window=20).std()
        volatility_trend = "increasing" if df['volatility'].iloc[-1] > df['volatility'].iloc[-5] else "decreasing"
        
        # Determine price trend based on moving averages
        if df['ma_20'].iloc[-1] > df['ma_50'].iloc[-1]:
            if df['close'].iloc[-1] > df['ma_20'].iloc[-1]:
                price_trend = "strongly_bullish"
            else:
                price_trend = "weakly_bullish"
        else:
            if df['close'].iloc[-1] < df['ma_20'].iloc[-1]:
                price_trend = "strongly_bearish"
            else:
                price_trend = "weakly_bearish"
        
        # Determine market cycle phase based on price trend and RSI
        rsi = df['rsi'].iloc[-1]
        if price_trend in ["strongly_bullish", "weakly_bullish"]:
            if rsi > 70:
                cycle_phase = "euphoria"
            elif rsi > 50:
                cycle_phase = "accumulation"
            else:
                cycle_phase = "hope"
        else:
            if rsi < 30:
                cycle_phase = "capitulation"
            elif rsi < 50:
                cycle_phase = "distribution"
            else:
                cycle_phase = "anxiety"
        
        return {
            "cycle_phase": cycle_phase,
            "price_trend": price_trend,
            "rsi": rsi,
            "volume_trend": volume_trend,
            "volatility_trend": volatility_trend,
            "ma_20_50_relationship": "bullish" if df['ma_20'].iloc[-1] > df['ma_50'].iloc[-1] else "bearish"
        }
    except Exception as e:
        logger.error(f"Error analyzing market cycle: {str(e)}")
        return {}

def generate_enhanced_prompt(market_context: Dict[str, Any], params: Dict[str, Any]) -> str:
    """
    Generate an enhanced prompt for AI assistant based on market context and parameters.
    
    Args:
        market_context: Dictionary with market context information
        params: Dictionary with current strategy parameters
        
    Returns:
        A formatted prompt string
    """
    market_regime = market_context.get('market_regime', 'unknown')
    cycle_phase = market_context.get('market_cycle', {}).get('cycle_phase', 'unknown')
    
    prompt = f"""
I need expert advice on optimizing my cryptocurrency trading strategy for the current market conditions.

## Market Context:
- Symbol: {market_context.get('symbol', 'Unknown')}
- Analysis Period: {market_context.get('period', 'Unknown')}
- Current Price: {market_context.get('current_price', 0):.2f}
- Price Change: {market_context.get('price_change_pct', 0):.2f}% over the last {market_context.get('period', '').split(' to ')[0]}
- Market Volatility: {market_context.get('volatility', 0):.2f}% (recent: {market_context.get('recent_volatility', 0):.2f}%)
- Market Regime: {market_regime}
- ATR Percentage: {market_context.get('atr_percent', 0):.2f}% 
- Volatility Trend: {"Expanding" if market_context.get('volatility_expanding', False) else "Contracting"}

## Technical Indicators:
- RSI: {market_context.get('rsi', 0):.2f}
- Price relative to MA20: {"Above" if market_context.get('is_above_ma20', False) else "Below"}
- Price relative to MA50: {"Above" if market_context.get('is_above_ma50', False) else "Below"}
- Price relative to MA200: {"Above" if market_context.get('is_above_ma200', False) else "Below"}
- MA20/MA50 Relationship: {"MA20 above MA50" if market_context.get('ma20_above_ma50', False) else "MA20 below MA50"}
- MA20 Slope: {market_context.get('ma_20_slope', 0):.2f}%
- MA50 Slope: {market_context.get('ma_50_slope', 0):.2f}%

## Market Cycle Information:
- Cycle Phase: {cycle_phase}
- Price Trend: {market_context.get('market_cycle', {}).get('price_trend', 'Unknown')}
- Volume Trend: {market_context.get('volume_trend', 'Unknown')}
- Price Range (last 20 days): {market_context.get('price_range_pct', 0):.2f}%

## Support and Resistance:
- Nearest Support: {market_context.get('support_resistance', {}).get('nearest_support', 0):.2f} ({market_context.get('support_resistance', {}).get('price_to_support_pct', 0):.2f}% below current price)
- Nearest Resistance: {market_context.get('support_resistance', {}).get('nearest_resistance', 0):.2f} ({market_context.get('support_resistance', {}).get('price_to_resistance_pct', 0):.2f}% above current price)
- Price near Support: {"Yes" if market_context.get('near_support', False) else "No"}
- Price near Resistance: {"Yes" if market_context.get('near_resistance', False) else "No"}

## Current Strategy Parameters:
"""
    
    # Add current parameters to the prompt
    for param_name, value in params.items():
        if param_name in PARAMETER_CONSTRAINTS:
            constraints = PARAMETER_CONSTRAINTS[param_name]
            prompt += f"- {param_name}: {value} (Range: {constraints[0]} to {constraints[1]}, Description: {constraints[3]})\n"
        else:
            prompt += f"- {param_name}: {value}\n"
    
    # Add performance expectations
    performance_expectations = market_context.get('performance_expectations', PERFORMANCE_EXPECTATIONS["unknown"])
    prompt += f"""
## Expected Performance for {market_regime} Market:
- Expected Win Rate: {performance_expectations.get('win_rate', 0) * 100:.2f}%
- Expected Profit Factor: {performance_expectations.get('profit_factor', 0):.2f}
- Expected Max Drawdown: {performance_expectations.get('max_drawdown', 0) * 100:.2f}%
- Expected Trades per Month: {performance_expectations.get('trades_per_month', 0)}
- Average Trade Duration: {performance_expectations.get('avg_trade_duration', 0)} days
- Optimal Strategy Approach: {performance_expectations.get('optimal_strategy', 'Balanced approach')}
- Market Description: {performance_expectations.get('description', '')}

## Questions:
"""
    
    # Add general questions for all market regimes
    prompt += """
1. Given the current market conditions, what specific parameter adjustments would you recommend to optimize performance?
2. How should I calibrate my entry and exit thresholds (RSI, Bollinger Bands) for this specific market regime?
3. What risk management settings (stop loss, take profit, risk per trade) are most appropriate right now?
"""

    # Add regime-specific questions
    if "trending_bullish" in market_regime:
        prompt += """
4. In this bullish trend, how should I adjust my parameters to maximize gains while protecting against sudden reversals?
5. What's the optimal balance between trend-following and profit-taking in the current trending market?
6. How should lookback windows be adjusted to capture this trend's momentum effectively?
7. Should I implement trailing stops instead of fixed take-profit levels in this trending market?
"""
    elif "trending_bearish" in market_regime:
        prompt += """
4. For this bearish trend, how should I optimize short entries and exits while managing elevated risk?
5. How can I adjust volatility filters to avoid false signals during bearish price action?
6. What's the ideal balance between risk per trade and stop distance in this higher-risk environment?
7. Should I use more conservative position sizing in this bearish market, and if so, how?
"""
    elif "volatile_high" in market_regime:
        prompt += """
4. Given the high volatility, what parameter adjustments would help reduce false signals and whipsaws?
5. How should I adapt position sizing in this high-volatility environment to manage risk?
6. What's the optimal balance between tight stops to control risk and giving trades room to breathe?
7. Should I consider shorter-term strategies with quicker profit targets in this volatile market?
"""
    elif "volatile_low" in market_regime:
        prompt += """
4. In this low volatility environment, how can I adjust parameters to capitalize on smaller price movements?
5. What's the most effective way to handle potentially false breakout signals during volatility contraction?
6. How should I prepare for a potential volatility expansion that might follow this low volatility period?
7. Should I widen my risk parameters given the reduced day-to-day price movement?
"""
    elif "ranging" in market_regime:
        prompt += """
4. For this range-bound market, how should I optimize parameters for mean-reversion strategies?
5. What's the ideal approach to setting take-profit targets near range extremes?
6. How should I adjust RSI thresholds to capture optimal entry and exit points within the range?
7. What warning signs should I monitor for a potential range breakout, and how should I adapt my strategy?
"""
    elif "accumulation" in market_regime or "distribution" in market_regime:
        prompt += """
4. How should I modify my parameters to identify the early stages of a breakout from this accumulation/distribution phase?
5. What volume indicators or thresholds would help confirm genuine breakout signals?
6. How can I optimize entry timing to position before a major move while minimizing false signal risk?
7. What's the appropriate risk management approach during this potentially transitional market phase?
"""
    elif "reversal" in market_regime:
        prompt += """
4. Given the potential reversal signals, how should I adjust parameters to confirm a genuine trend change?
5. What's the optimal balance between early positioning for a reversal and waiting for confirmation?
6. How should I structure my risk parameters to account for the higher uncertainty during potential reversals?
7. What technical indicators would best complement my strategy during this potential transition period?
"""
    else:
        prompt += """
4. In this uncertain market environment, what parameter adjustments would create a more robust strategy?
5. How should I modify position sizing and risk management for this unclear market direction?
6. What technical indicators would be most reliable in the current conditions?
7. How can I balance the strategy between trend-following and mean-reversion approaches?
"""

    # Add final questions for all regimes
    prompt += """
8. Based on my current settings, which specific parameters need the most urgent adjustment for the current conditions?
9. How might these parameter adjustments need to change if market conditions shift in the near future?
10. Are there any parameter relationships I should be particularly mindful of in this market environment?

Please provide specific numerical parameter recommendations with your reasoning for each adjustment. Prioritize the 3-5 most impactful changes I should make immediately.
"""
    
    return prompt

def get_parameter_suggestions_with_context(
    market: str,
    granularity: str = "ONE_DAY",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_params: Optional[Dict[str, Any]] = None,
    context_window_days: int = 30,
) -> Tuple[Dict[str, Any], List[str], bool]:
    """
    Get parameter suggestions based on market context.
    
    Args:
        market: Market symbol (e.g., "BTC-USD")
        granularity: Candle granularity
        start_date: Start date for analysis
        end_date: End date for analysis
        current_params: Current strategy parameters
        context_window_days: Number of days to analyze for context
        
    Returns:
        Tuple containing:
            - Dictionary of suggested parameters
            - List of adjustment reasons
            - Boolean indicating if suggestions are expected to improve performance
    """
    if not current_params:
        current_params = get_default_parameters()
    
    # Use a copy of current parameters as a starting point
    suggested_params = copy.deepcopy(current_params)
    
    # Set up date range if not provided
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=context_window_days)
    
    # Get market context
    market_context = get_enhanced_market_context(market, context_window_days)
    
    # --- TEMP OVERRIDE FOR TESTING --- 
    # regime = "trending_bullish" # Force regime to test bullish logic
    # logger.warning(f"<<<<< OVERRIDING MARKET REGIME TO: {regime} >>>>>")
    regime = market_context.get('market_regime', 'unknown') # Original line - Ensure this is active
    # --- END TEMP OVERRIDE ---
    
    trend_strength = market_context.get('trend_strength', 0.5)
    
    # Extract relevant context information
    volatility = market_context.get('volatility', 0.5)
    volume_profile = market_context.get('volume_trend', 'normal')
    proximity_to_support = market_context.get('near_support', False)
    proximity_to_resistance = market_context.get('near_resistance', False)
    
    # Log the identified market regime
    logger.info(f"Market regime identified: {regime}")
    
    # Initialize a list to store adjustment reasons
    adjustment_reasons = []
    
    # PARAMETER ADJUSTMENT LOGIC BASED ON MARKET REGIME
    # More aggressive parameter adjustments for different market regimes
    
    # Default lookback is 20 days for more responsive signals
    suggested_params['lookback_window'] = min(suggested_params['lookback_window'], 15)
    
    if regime == 'trending_bullish':
        # For bullish trends, we want to be more sensitive to upward movements
        suggested_params['rsi_entry'] = max(25, current_params['rsi_entry'] - 5)  # More aggressive entry
        suggested_params['rsi_exit'] = min(75, current_params['rsi_exit'] + 5)    # Hold longer
        suggested_params['bb_dev'] = max(1.5, current_params['bb_dev'] - 0.2)     # Tighter bands
        suggested_params['sl_pct'] = min(2.5, current_params['sl_pct'] * 1.2)     # Wider stop loss
        suggested_params['tp_pct'] = max(4.0, current_params['tp_pct'] * 1.2)     # Higher take profit
        suggested_params['volatility_threshold'] = min(0.35, current_params['volatility_threshold'] * 0.7)  # More permissive
        
        adjustment_reasons.append("Lowered RSI thresholds to capture more bullish momentum")
        adjustment_reasons.append("Adjusted Bollinger Bands to identify breakouts earlier")
        adjustment_reasons.append("Optimized for aggressive entries in bullish trend")
        
    elif regime == 'trending_bearish':
        # For bearish trends, focus on short opportunities
        suggested_params['rsi_entry'] = min(35, current_params['rsi_entry'] - 3)  # More sensitive entry
        suggested_params['rsi_exit'] = max(65, current_params['rsi_exit'] - 5)    # Exit earlier
        suggested_params['bb_dev'] = max(1.5, current_params['bb_dev'] - 0.2)     # Tighter bands
        suggested_params['sl_pct'] = min(3.0, current_params['sl_pct'] * 1.25)    # Wider stop loss
        suggested_params['tp_pct'] = max(4.4, current_params['tp_pct'] * 1.1)     # Higher take profit
        suggested_params['volatility_threshold'] = min(0.3, current_params['volatility_threshold'] * 0.6)  # Much more permissive
        
        adjustment_reasons.append("Slightly tightened Bollinger Bands and reduced stop loss for low volatility")
        adjustment_reasons.append("Moderately lowered RSI entry threshold due to proximity to support level")
        adjustment_reasons.append("Optimized for general bearish trend with balanced lookback and risk parameters")
        
    elif regime == 'ranging':
        # For ranging markets, focus on mean reversion
        suggested_params['rsi_entry'] = min(30, current_params['rsi_entry'] - 2)  # Lower entry for better mean reversion
        suggested_params['rsi_exit'] = max(70, current_params['rsi_exit'] + 0)    # Standard exit
        suggested_params['bb_dev'] = min(2.2, current_params['bb_dev'] + 0.1)     # Wider bands
        suggested_params['sl_pct'] = min(2.0, current_params['sl_pct'] * 1.0)     # Standard stop loss
        suggested_params['tp_pct'] = min(3.5, current_params['tp_pct'] * 0.9)     # Lower take profit
        suggested_params['volatility_threshold'] = min(0.3, current_params['volatility_threshold'] * 0.6)  # More permissive
        
        adjustment_reasons.append("Configured for mean reversion in ranging market")
        adjustment_reasons.append("Balanced RSI thresholds for both entry and exit")
        adjustment_reasons.append("Reduced volatility threshold to allow more trades")
        
    elif regime == 'volatile':
        # For volatile markets, be more conservative
        suggested_params['rsi_entry'] = min(25, suggested_params['rsi_entry'] - 5)  # More aggressive entries
        suggested_params['rsi_exit'] = max(65, suggested_params['rsi_exit'] - 5)  # Earlier exits
        suggested_params['bb_dev'] = max(2.0, current_params['bb_dev'] + 0.2)     # Wider bands
        suggested_params['sl_pct'] = min(3.5, current_params['sl_pct'] * 1.3)     # Wider stop loss
        suggested_params['tp_pct'] = max(4.5, current_params['tp_pct'] * 1.2)     # Higher take profit
        suggested_params['volatility_threshold'] = min(0.4, current_params['volatility_threshold'] * 0.8)  # More permissive
        
        adjustment_reasons.append("Widened Bollinger Bands to accommodate volatility")
        adjustment_reasons.append("Increased stop loss to avoid premature exits during volatile moves")
        adjustment_reasons.append("Optimized for capturing significant price movements in volatile conditions")
    
    # VOLUME-BASED ADJUSTMENTS
    if volume_profile == 'increasing':
        # Higher volume means more reliable signals
        suggested_params['vol_window'] = max(15, current_params['vol_window'] - 5)  # Shorter window to be more responsive
        adjustment_reasons.append("Shortened volume window to be more responsive to increasing volume")
    elif volume_profile == 'decreasing':
        # Lower volume means less reliable signals
        suggested_params['vol_window'] = min(25, current_params['vol_window'] + 5)  # Longer window
        adjustment_reasons.append("Increased volume window to filter out noise in decreasing volume")
    
    # VOLATILITY ADJUSTMENTS
    # Always make volatility threshold more permissive to generate more trades
    suggested_params['volatility_threshold'] = min(0.25, suggested_params['volatility_threshold'])
    suggested_params['vol_filter_window'] = min(30, suggested_params['vol_filter_window'])
    
    if volatility > 0.7:
        # High volatility
        suggested_params['sl_pct'] = min(4.0, current_params['sl_pct'] * 1.5)  # Much wider stop loss
        adjustment_reasons.append("Significantly increased stop loss due to high volatility")
    elif volatility < 0.3:
        # Low volatility
        suggested_params['sl_pct'] = max(1.5, current_params['sl_pct'] * 0.8)  # Tighter stop loss
        adjustment_reasons.append("Tightened stop loss due to low volatility")
    
    # PROXIMITY TO SUPPORT/RESISTANCE
    if proximity_to_support:
        # Close to support, good for long entries
        suggested_params['rsi_entry'] = max(20, suggested_params['rsi_entry'] - 5)  # More aggressive entry
        adjustment_reasons.append("Lowered RSI entry threshold due to proximity to support level")
    
    if proximity_to_resistance:
        # Close to resistance, good for short entries or taking profits
        suggested_params['rsi_exit'] = min(65, suggested_params['rsi_exit'] - 5)  # Earlier exit
        adjustment_reasons.append("Lowered RSI exit threshold due to proximity to resistance level")
    
    # RISK MANAGEMENT ADJUSTMENTS
    # Adjust risk per trade based on market conditions
    if regime == 'trending_bullish':
        suggested_params['risk_per_trade'] = min(0.025, current_params['risk_per_trade'] * 1.25)  # More aggressive
    elif regime == 'volatile':
        suggested_params['risk_per_trade'] = max(0.01, current_params['risk_per_trade'] * 0.75)  # More conservative
    else:
        suggested_params['risk_per_trade'] = min(0.015, current_params['risk_per_trade'])  # Moderate
    
    # FINAL VALIDATION: Ensure parameters are within acceptable ranges
    # Always keep lookback windows small for shorter datasets
    if suggested_params['lookback_window'] > 15:
        suggested_params['lookback_window'] = 15
        adjustment_reasons.append("Limited lookback window to 15 to maintain trade signals with limited data")
    
    if suggested_params['vol_filter_window'] > 30:
        suggested_params['vol_filter_window'] = 30
        adjustment_reasons.append("Limited volatility filter window to 30 to maintain trade signals with limited data")
    
    if suggested_params['volatility_threshold'] > 0.25:
        suggested_params['volatility_threshold'] = 0.25
        adjustment_reasons.append("Capped volatility threshold at 0.25 to ensure sufficient trade signals")
    
    # Add data-specific adjustment reason
    adjustment_reasons.append("Optimized for short data periods with aggressive trade generation")
    
    # Validate parameters against constraints
    validation_result = validate_and_adjust_parameters(suggested_params)
    suggested_params = validation_result["params"]
    
    # Add validation issues to adjustment reasons if there are any
    if validation_result["issues"]:
        adjustment_reasons.extend(validation_result["issues"])
    
    # Check if suggested parameters are actually different from current ones
    params_changed = any(suggested_params[key] != current_params[key] for key in suggested_params 
                         if key in current_params)
    if not params_changed:
        adjustment_reasons.append("No significant changes needed for current market conditions")
    
    # Return suggested parameters, adjustment reasons, and expectation of improvement
    return suggested_params, adjustment_reasons, params_changed

def test_parameter_trade_generation(
    market: str,
    parameters: Dict[str, Any],
    start_date: datetime,
    end_date: datetime,
    granularity: int = 86400 # Use integer seconds (86400 for 1 day)
) -> Tuple[int, Dict[str, Any]]:
    """
    Test if the given parameters would generate sufficient trades in the specified period.
    
    Args:
        market: Market symbol
        parameters: Strategy parameters to test
        start_date: Start date for testing
        end_date: End date for testing
        granularity: Candle granularity
        
    Returns:
        Tuple of (number of trades generated, updated parameters if needed)
    """
    # Convert datetime objects to strings for fetching data
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    # Fetch historical data
    try:
        # Import data fetcher
        from data.data_fetcher import fetch_historical_data
        
        data = fetch_historical_data(
            product_id=market,
            start_date=start_date_str,
            end_date=end_date_str,
            granularity=granularity # Pass integer seconds
        )
        
        # Create strategy instance
        from scripts.strategies.edge_multi_factor_fixed import EdgeMultiFactorStrategy
        
        strategy = EdgeMultiFactorStrategy()
        
        # Set parameters on strategy
        for param_name, param_value in parameters.items():
            if hasattr(strategy, param_name):
                # Convert any window parameters to integers
                if param_name.endswith('_window') and isinstance(param_value, float):
                    param_value = int(param_value)
                setattr(strategy, param_name, param_value)
        
        # Generate signals
        signals = strategy.generate_signals(data)
        
        # Count trades using tuple indexing
        long_entries = signals[0].sum() if signals and len(signals) > 0 else 0
        short_entries = signals[1].sum() if signals and len(signals) > 1 else 0
        total_trades = long_entries + short_entries
        
        logger.info(f"Test parameters would generate {long_entries} long entries and {short_entries} short entries over {len(data)} days")
        
        # If not enough trades, adjust parameters to be more aggressive
        updated_params = parameters.copy()
        
        if total_trades < 2 and len(data) >= 20:
            logger.warning(f"Optimized parameters would only generate {total_trades} trades in {len(data)} days")
            logger.info("Adjusting parameters to ensure sufficient trade generation")
            
            # Make parameters more aggressive
            updated_params['volatility_threshold'] = max(0.1, parameters.get('volatility_threshold', 0.3) * 0.5)
            updated_params['rsi_entry'] = max(20, parameters.get('rsi_entry', 30) - 10)
            updated_params['bb_dev'] = max(1.0, parameters.get('bb_dev', 2.0) * 0.75)
            
            # Test again with updated parameters
            return test_parameter_trade_generation(
                market, 
                updated_params,
                start_date,
                end_date,
                granularity
            )
        
        return total_trades, updated_params
        
    except Exception as e:
        logger.error(f"Error testing parameter trade generation: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 0, parameters

def test_parameter_suggestions_with_backtest() -> Dict[str, Any]:
    """
    Test parameter suggestions with backtest and validate performance improvement
    
    Returns:
        Dictionary with test results
    """
    try:
        # 1. Get enhanced parameter suggestions
        # Call the function and unpack the returned tuple
        current_params = get_default_parameters() # Get current/default parameters
        
        suggestions_result_tuple = get_parameter_suggestions_with_context(
            market="BTC-USD", 
            current_params=current_params
        )
        
        # Unpack the tuple
        suggested_params, adjustment_reasons, params_changed = suggestions_result_tuple

        # Get market context separately if needed (re-run the context part)
        # Use the correct keyword argument 'lookback_days'
        market_context = get_enhanced_market_context("BTC-USD", lookback_days=30)
        market_regime = market_context.get("market_regime", "unknown")
        
        # Use the unpacked variables
        validated_params = suggested_params # Use the unpacked suggested parameters
        original_params = current_params    # Use the original parameters fetched earlier
        adjustments = adjustment_reasons    # Use the unpacked adjustment reasons

        logger.info(f"Generated parameter suggestions for {market_regime} market")
        for adj in adjustments:
            logger.info(f"Adjustment: {adj}")

        # NEW: Test if parameters would generate sufficient trades
        # Define start/end dates for the test - Use 90 days
        end_date_test = datetime.now()
        start_date_test = end_date_test - timedelta(days=90) # Increased from 30
        
        trades_generated, validated_params = test_parameter_trade_generation(
            market="BTC-USD",
            parameters=validated_params, 
            start_date=start_date_test,
            end_date=end_date_test,
            granularity=86400 # Pass integer seconds
        )
        
        trade_test_result = {
            "is_sufficient": trades_generated >= 2, 
            "trades_generated": trades_generated
        }

        if not trade_test_result.get("is_sufficient", False):
            logger.warning(f"Optimized parameters would only generate {trade_test_result.get('trades_generated', 0)} trades in 30 days")
            logger.info("Adjusting parameters to ensure sufficient trade generation")
            
            # Make parameters less restrictive
            if validated_params.get("volatility_threshold", 0.5) > 0.4:
                validated_params["volatility_threshold"] = 0.4
                logger.info("Reduced volatility threshold to 0.4 to increase trade frequency")
                
            if validated_params.get("rsi_entry", 30) > 30:
                validated_params["rsi_entry"] = 30
                logger.info("Adjusted RSI entry to 30 to increase trade signals")
                
            if validated_params.get("bb_dev", 2.0) > 2.0:
                validated_params["bb_dev"] = 2.0
                logger.info("Set Bollinger Band deviation to 2.0 for more trade signals")
            
            # Test again after adjustments
            trades_generated, validated_params = test_parameter_trade_generation(
                market="BTC-USD",
                parameters=validated_params, 
                start_date=start_date_test,
                end_date=end_date_test,
                granularity=86400 # Pass integer seconds
            )
            trade_test_result = {
                "is_sufficient": trades_generated >= 2, 
                "trades_generated": trades_generated
            }
            logger.info(f"After adjustment: would generate {trade_test_result.get('trades_generated', 0)} trades in 30 days")
        
        # 2. Run historical performance check on both baseline and optimized parameters
        logger.info("Running historical performance check on baseline parameters")
        baseline_result = check_historical_performance("BTC-USD", original_params, lookback_days=90)
        
        if "error" in baseline_result:
            logger.error(f"Error in baseline performance check: {baseline_result['error']}")
            return {"error": baseline_result["error"]}
        
        logger.info("Running historical performance check on optimized parameters")
        optimized_result = check_historical_performance("BTC-USD", validated_params, lookback_days=90)
        
        if "error" in optimized_result:
            logger.error(f"Error in optimized performance check: {optimized_result['error']}")
            return {"error": optimized_result["error"]}
        
        # 3. Extract metrics
        baseline_metrics = baseline_result.get("metrics", {})
        optimized_metrics = optimized_result.get("metrics", {})
        
        # 4. Validate performance improvements
        logger.info("Validating performance improvements")
        is_improved, performance_analysis = validate_performance_impact(
            baseline_metrics, 
            optimized_metrics,
            market_regime
        )
        
        # 5. Calculate period-by-period improvements
        period_improvements = []
        baseline_periods = baseline_result.get("period_performance", [])
        optimized_periods = optimized_result.get("period_performance", [])
        
        for i in range(min(len(baseline_periods), len(optimized_periods))):
            baseline_period = baseline_periods[i]
            optimized_period = optimized_periods[i]
            
            # Calculate improvements for this period
            return_change = optimized_period.get("return", 0) - baseline_period.get("return", 0)
            sharpe_change = optimized_period.get("sharpe", 0) - baseline_period.get("sharpe", 0)
            win_rate_change = optimized_period.get("win_rate", 0) - baseline_period.get("win_rate", 0)
            period_improved_bool = return_change > 0 and sharpe_change > 0
            
            period_improvements.append({
                "period": baseline_period.get("period", f"Period {i+1}"),
                "start_date": baseline_period.get("start_date", ""),
                "end_date": baseline_period.get("end_date", ""),
                "return_change": return_change,
                "sharpe_change": sharpe_change,
                "win_rate_change": win_rate_change,
                "is_improved": str(period_improved_bool) # Convert boolean to string
            })
        
        # 6. Track consistency improvement
        consistency_change = optimized_metrics.get("consistency_score", 0) - baseline_metrics.get("consistency_score", 0)
        
        # 7. Generate final result
        result = {
            "market_context": market_context,
            "original_parameters": original_params,
            "suggested_parameters": validated_params,
            "parameter_adjustments": adjustments,
            "baseline_metrics": baseline_metrics,
            "optimized_metrics": optimized_metrics,
            "performance_analysis": {
                **performance_analysis,
                # Convert boolean within nested dict
                "is_close_to_expected": str(performance_analysis.get("is_close_to_expected", False))
            },
            "is_improved": str(is_improved), # Convert boolean to string
            "period_improvements": period_improvements, # Already handled above
            "consistency_change": consistency_change,
            # Convert boolean within nested dict
            "trade_generation_test": {
                **trade_test_result,
                "is_sufficient": str(trade_test_result.get("is_sufficient", False))
            },
            "timestamp": time.time()
        }
        
        # 8. If performance not improved, include recommendation
        if not is_improved:
            # Check which periods performed better with optimized parameters
            improved_periods = [p for p in period_improvements if p.get("is_improved", False) == "True"]
            
            if len(improved_periods) > 0:
                # Some periods improved, suggest targeted use
                result["recommendation"] = "The suggested parameters improved performance in some market periods but not overall. Consider using these parameters only during similar market conditions to those in the improved periods."
            else:
                # No periods improved, suggest sticking with baseline
                result["recommendation"] = "The suggested parameters did not improve performance in any tested period. Consider keeping the baseline parameters or exploring different optimization approaches."
        
        # 9. Log summary
        logger.info("\n=== Performance Summary ===")
        logger.info(f"Market Regime: {market_regime}")
        logger.info(f"Baseline Return: {baseline_metrics.get('total_return', 0) * 100:.2f}%, Win Rate: {baseline_metrics.get('win_rate', 0) * 100:.2f}%, Trades: {baseline_metrics.get('num_trades', 0)}")
        logger.info(f"Optimized Return: {optimized_metrics.get('total_return', 0) * 100:.2f}%, Win Rate: {optimized_metrics.get('win_rate', 0) * 100:.2f}%, Trades: {optimized_metrics.get('num_trades', 0)}")
        logger.info(f"Return Change: {performance_analysis.get('changes', {}).get('total_return_change', 0) * 100:.2f}%")
        logger.info(f"Is Improved: {is_improved}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error testing parameter suggestions: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def validate_performance_impact(baseline_metrics: Dict[str, Any], optimized_metrics: Dict[str, Any], market_regime: str = "unknown") -> Tuple[bool, Dict[str, Any]]:
    """
    Validate the performance impact of optimized parameters compared to baseline.
    
    Args:
        baseline_metrics: Dictionary with baseline performance metrics
        optimized_metrics: Dictionary with optimized performance metrics
        market_regime: Current market regime
        
    Returns:
        Tuple of (is_improved, performance_analysis)
    """
    try:
        logger.info("Validating performance impact of optimized parameters")
        
        # Calculate changes in metrics
        changes = {}
        if "total_return" in baseline_metrics and "total_return" in optimized_metrics:
            changes["total_return_change"] = optimized_metrics["total_return"] - baseline_metrics["total_return"]
            
        if "sharpe_ratio" in baseline_metrics and "sharpe_ratio" in optimized_metrics:
            changes["sharpe_ratio_change"] = optimized_metrics["sharpe_ratio"] - baseline_metrics["sharpe_ratio"]
            
        if "max_drawdown" in baseline_metrics and "max_drawdown" in optimized_metrics:
            changes["max_drawdown_change"] = optimized_metrics["max_drawdown"] - baseline_metrics["max_drawdown"]
            # Note: For drawdown, a positive change is worse (more negative drawdown)
            
        if "win_rate" in baseline_metrics and "win_rate" in optimized_metrics:
            changes["win_rate_change"] = optimized_metrics["win_rate"] - baseline_metrics["win_rate"]
            
        if "num_trades" in baseline_metrics and "num_trades" in optimized_metrics:
            changes["trades_change"] = optimized_metrics["num_trades"] - baseline_metrics["num_trades"]
        
        # Get expected performance for current market regime
        expected_performance = PERFORMANCE_EXPECTATIONS.get(market_regime, PERFORMANCE_EXPECTATIONS["unknown"])
        
        # Determine if performance is improved based on key metrics
        improvement_score = 0
        total_score = 0
        
        # Check total return improvement
        if "total_return_change" in changes:
            total_score += 3  # Higher weight for returns
            if changes["total_return_change"] > 0.01:  # 1% improvement threshold
                improvement_score += 3
            elif changes["total_return_change"] > 0:
                improvement_score += 1
                
        # Check Sharpe ratio improvement
        if "sharpe_ratio_change" in changes:
            total_score += 2
            if changes["sharpe_ratio_change"] > 0.2:  # Significant Sharpe improvement
                improvement_score += 2
            elif changes["sharpe_ratio_change"] > 0:
                improvement_score += 1
                
        # Check max drawdown improvement (less negative is better)
        if "max_drawdown_change" in changes:
            total_score += 1
            if changes["max_drawdown_change"] < -0.02:  # Drawdown improved by 2%
                improvement_score += 1
                
        # Check win rate improvement
        if "win_rate_change" in changes:
            total_score += 2
            if changes["win_rate_change"] > 0.05:  # 5% win rate improvement
                improvement_score += 2
            elif changes["win_rate_change"] > 0:
                improvement_score += 1
        
        # Calculate improvement percentage
        improvement_percentage = (improvement_score / total_score) if total_score > 0 else 0
        
        # Evaluate if close to expected performance
        expected_metrics = {}
        actual_metrics = {}
        
        if "win_rate" in expected_performance and "win_rate" in optimized_metrics:
            expected_metrics["win_rate"] = expected_performance["win_rate"]
            actual_metrics["win_rate"] = optimized_metrics["win_rate"]
            
        if "profit_factor" in expected_performance and "profit_factor" in optimized_metrics:
            expected_metrics["profit_factor"] = expected_performance["profit_factor"]
            actual_metrics["profit_factor"] = optimized_metrics["profit_factor"]
            
        # Determine if improvement is significant
        is_improved = improvement_percentage >= 0.5  # 50% improvement threshold
        
        # Provide detailed analysis
        analysis = {
            "changes": changes,
            "improvement_score": improvement_score,
            "total_score": total_score,
            "improvement_percentage": improvement_percentage,
            "expected_metrics": expected_metrics,
            "actual_metrics": actual_metrics,
            "is_close_to_expected": is_close_to_expected_performance(optimized_metrics, expected_performance),
            "market_regime": market_regime
        }
        
        return is_improved, analysis
        
    except Exception as e:
        logger.error(f"Error validating performance impact: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False, {"error": str(e)}

def is_close_to_expected_performance(metrics: Dict[str, Any], expected: Dict[str, Any]) -> bool:
    """
    Check if actual metrics are close to expected performance.
    
    Args:
        metrics: Actual performance metrics
        expected: Expected performance metrics
        
    Returns:
        True if metrics are close to expected, False otherwise
    """
    # Define thresholds for "close enough"
    win_rate_threshold = 0.1  # Within 10 percentage points
    profit_factor_threshold = 0.3  # Within 0.3
    
    # Check win rate
    if "win_rate" in expected and "win_rate" in metrics:
        if abs(metrics["win_rate"] - expected["win_rate"]) > win_rate_threshold:
            return False
            
    # Check profit factor
    if "profit_factor" in expected and "profit_factor" in metrics:
        if abs(metrics["profit_factor"] - expected["profit_factor"]) > profit_factor_threshold:
            return False
    
    return True

def main():
    """Main function to test the enhanced parameter suggestions"""
    logger.info("Testing enhanced parameter suggestions")
    
    try:
        # Test parameter suggestions with backtest
        result = test_parameter_suggestions_with_backtest()
        
        if "error" in result:
            logger.error(f"Error: {result['error']}")
        else:
            logger.info("Parameter suggestions test complete")
            
            # Print summary
            if result.get("is_improved", False):
                logger.info("✅ AI optimization IMPROVED strategy performance!")
            else:
                logger.info("⚠️ AI optimization did NOT improve performance")
            
            # --- Save results to file ---
            # Always save the full analysis results
            results_dir = Path("analysis_results")
            results_dir.mkdir(parents=True, exist_ok=True)
            timestamp = int(result.get("timestamp", time.time())) # Use timestamp from result if available
            analysis_filename = results_dir / f"parameter_suggestions_test_{timestamp}.json"
            try:
                with open(analysis_filename, "w") as f:
                    json.dump(result, f, indent=2, default=json_encoder_default)
                logger.info(f"Full analysis results saved to {analysis_filename}")
            except Exception as e:
                logger.error(f"Error saving full analysis results: {e}")

            # --- Conditionally save optimized parameters --- 
            if result.get("is_improved") == "True":
                params_to_save = result.get("suggested_parameters", None)
                if params_to_save:
                    config_dir = Path("config") # Define config directory
                    config_dir.mkdir(parents=True, exist_ok=True) # Create if needed
                    params_filename = config_dir / "optimized_strategy_params.json"
                    try:
                        with open(params_filename, "w") as f:
                            json.dump(params_to_save, f, indent=4)
                        logger.info(f"✅ Successfully saved improved parameters to {params_filename}")
                    except Exception as e:
                        logger.error(f"Error saving optimized parameters: {e}")
                else:
                     logger.warning("Performance improved, but no suggested parameters found in results to save.")
            else:
                logger.info("Performance not improved, optimized parameters were not saved.")

    except ValueError as ve:
        logger.error(f"Value error in parameter suggestions: {ve}")
        logger.error(traceback.format_exc())
        result = {
            "status": "error",
            "error_type": "value_error",
            "message": str(ve),
            "timestamp": datetime.now().isoformat()
        }
    except KeyError as ke:
        logger.error(f"Key error in parameter suggestions: {ke}")
        logger.error(traceback.format_exc())
        result = {
            "status": "error",
            "error_type": "key_error",
            "message": str(ke),
            "timestamp": datetime.now().isoformat()
        }
    except ImportError as ie:
        logger.error(f"Import error in parameter suggestions: {ie}")
        logger.error(traceback.format_exc())
        result = {
            "status": "error",
            "error_type": "import_error",
            "message": str(ie),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e: 
        logger.error(f"Error testing parameter suggestions: {e}")
        logger.error(traceback.format_exc())
        result = {
            "status": "error",
            "error_type": "general_exception",
            "message": str(e),
            "stack_trace": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
    finally:
        # Ensure result is always returned or used properly
        if 'result' not in locals():
            result = {
                "status": "error",
                "error_type": "unknown_error",
                "message": "An unknown error occurred without exception details",
                "timestamp": datetime.now().isoformat()
            }
        
        # Log the final result
        if result.get("status") == "error":
            logger.error(f"Parameter suggestion process failed with result: {result}")
        
        # Return or use result as needed
        return result

def check_historical_performance(symbol: str, params: Dict[str, Any], lookback_days: int = 90) -> Dict[str, Any]:
    """
    Check the historical performance of a set of parameters using past data.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTC-USD')
        params: Strategy parameters to test
        lookback_days: Number of days to look back for historical testing
        
    Returns:
        Dictionary with performance metrics
    """
    try:
        # Import necessary modules
        from data.data_fetcher import fetch_historical_data, get_vbt_freq_str
        import vectorbtpro as vbt
        
        # Force a longer lookback for more robust validation
        effective_lookback_days = max(lookback_days, 365)
        logger.info(f"Running historical performance check with effective lookback of {effective_lookback_days} days.")

        # Get historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=effective_lookback_days)
        
        # Fetch data with daily candles
        granularity = 86400  # Daily candles in seconds
        df = fetch_historical_data(
            product_id=symbol,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            granularity=granularity
        )
        
        if df.empty:
            return {"error": f"No data available for {symbol} in the specified time period"}
        
        # Create strategy with provided parameters
        strategy = EdgeMultiFactorStrategy()
        
        # Apply parameters
        for param, value in params.items():
            if hasattr(strategy, param):
                setattr(strategy, param, value)
            
        # Generate signals
        long_entries, short_entries, is_trending, is_ranging = strategy.generate_signals(df)
        
        # Create portfolio
        portfolio = vbt.Portfolio.from_signals(
            df['close'], 
            entries=long_entries,
            exits=None,
            short_entries=short_entries,
            short_exits=None,
            sl_stop=params.get('sl_pct', 2.0) / 100,  # Convert to decimal
            tp_stop=params.get('tp_pct', 4.0) / 100,  # Convert to decimal
            freq='1D',
            init_cash=10000
        )
        
        # Calculate metrics
        total_return = float(portfolio.total_return)
        sharpe_ratio = float(portfolio.sharpe_ratio)
        max_drawdown = float(portfolio.max_drawdown)
        win_rate = float(portfolio.trades.win_rate) if hasattr(portfolio.trades, 'win_rate') else 0
        num_trades = len(portfolio.trades)
        
        # Advanced metrics if available
        try:
            profit_factor = float(portfolio.trades.profit_factor) if hasattr(portfolio.trades, 'profit_factor') else 0
            avg_trade_duration = float(portfolio.trades.duration.mean()) if hasattr(portfolio.trades, 'duration') else 0
            recovery_factor = float(portfolio.recovery_factor) if hasattr(portfolio, 'recovery_factor') else 0
            calmar_ratio = float(portfolio.calmar_ratio) if hasattr(portfolio, 'calmar_ratio') else 0
        except Exception as e:
            logger.warning(f"Could not calculate some advanced metrics: {e}")
            profit_factor = 0
            avg_trade_duration = 0
            recovery_factor = 0
            calmar_ratio = 0
        
        # Check which timeframes performed better
        # Split data into chunks
        chunks = []
        chunk_size = len(df) // 3  # Split into 3 periods
        
        for i in range(3):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < 2 else len(df)
            chunk_df = df.iloc[start_idx:end_idx].copy()
            
            if len(chunk_df) > 20:  # Ensure enough data for signals
                # Get signals for chunk
                chunk_long, chunk_short, _, _ = strategy.generate_signals(chunk_df)
                
                # Create portfolio for chunk
                chunk_pf = vbt.Portfolio.from_signals(
                    chunk_df['close'], 
                    entries=chunk_long,
                    exits=None,
                    short_entries=chunk_short,
                    short_exits=None,
                    sl_stop=params.get('sl_pct', 2.0) / 100,
                    tp_stop=params.get('tp_pct', 4.0) / 100,
                    freq='1D',
                    init_cash=10000
                )
                
                # Store chunk performance
                chunks.append({
                    "period": f"Period {i+1}",
                    "start_date": chunk_df.index[0].strftime('%Y-%m-%d'),
                    "end_date": chunk_df.index[-1].strftime('%Y-%m-%d'),
                    "return": float(chunk_pf.total_return),
                    "sharpe": float(chunk_pf.sharpe_ratio),
                    "trades": len(chunk_pf.trades),
                    "win_rate": float(chunk_pf.trades.win_rate) if hasattr(chunk_pf.trades, 'win_rate') else 0
                })
        
        # Determine consistency score (how consistently the strategy performs)
        if len(chunks) > 0:
            returns = [chunk["return"] for chunk in chunks]
            consistency_score = 1.0 - np.std(returns) / (max(0.01, np.mean(np.abs(returns))))
        else:
            consistency_score = 0
        
        return {
            "symbol": symbol,
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "params": params,
            "metrics": {
                "total_return": total_return,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
                "win_rate": win_rate,
                "num_trades": num_trades,
                "profit_factor": profit_factor,
                "avg_trade_duration": avg_trade_duration, 
                "recovery_factor": recovery_factor,
                "calmar_ratio": calmar_ratio,
                "consistency_score": consistency_score
            },
            "period_performance": chunks,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error checking historical performance: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}

# --- NEW HELPER FUNCTION ---
def make_json_serializable(data):
    """Recursively converts non-serializable types to JSON-compatible types."""
    if isinstance(data, dict):
        return {k: make_json_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [make_json_serializable(elem) for elem in data]
    # Explicitly check for both Python bool and numpy.bool_
    elif isinstance(data, (bool, np.bool_)):
        return str(data)
    elif isinstance(data, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(data)
    elif isinstance(data, (np.float16, np.float32, np.float64)):
        return float(data)
    elif hasattr(np, 'floating') and isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        # Handle arrays containing booleans
        if data.dtype == np.bool_:
             return [str(item) for item in data] # Correctly indented and returning list of strings
        return data.tolist() # Convert other numpy arrays to lists
    elif isinstance(data, pd.Index):
         # Handle pandas Index containing booleans
        if data.dtype == bool or data.dtype == np.bool_:
            return [str(item) for item in data]
        return data.tolist() # Convert pandas Index to list
    elif isinstance(data, pd.Series):
        # Handle pandas Series containing booleans
        if data.dtype == bool or data.dtype == np.bool_:
             return [str(item) for item in data.where(pd.notnull(data), None)] # Handle NaN within bool series
        # Handle NaNs/NaTs within other Series types before converting to list
        try:
            if pd.api.types.is_datetime64_any_dtype(data.dtype):
                return data.apply(lambda x: x.isoformat() if pd.notnull(x) else None).tolist()
            else:
                 # Replace Inf/-Inf with None for other numeric types if needed
                data_cleaned = data.replace([np.inf, -np.inf], np.nan).where(pd.notnull(data), None)
                return data_cleaned.tolist()
        except Exception:
            # Fallback if complex type within series causes error
            return [make_json_serializable(item) for item in data]
    elif isinstance(data, (pd.Timestamp, datetime)):
        return data.isoformat()
    elif isinstance(data, (pd.Timedelta, timedelta)):
        return str(data)
    elif pd.isna(data):
        return None
    elif isinstance(data, (str, int, float, type(None))):
        return data # Already serializable
    elif data is pd.NA:
        return None # Explicitly handle pandas NA
    elif data is np.inf or data is -np.inf:
         return None # Convert infinities
    else:
        # Final fallback: try converting to string, VERY defensively
        try:
            return str(data)
        except Exception as e_str:
            logger.error(f"Failed even to convert type {type(data)} to string: {e_str}. Returning None.")
            return None
# --- END NEW HELPER FUNCTION ---

if __name__ == "__main__":
    main() 