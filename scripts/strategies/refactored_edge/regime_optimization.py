"""
Regime-aware optimization for the Edge Multi-Factor strategy.

This module provides functions for optimizing strategy parameters based on market regime,
allowing for more effective parameter selection for different market conditions.
It performs separate optimizations for trending and ranging market segments and then
combines the results to create a regime-aware parameter set.
"""

import pandas as pd
import numpy as np
import optuna
from typing import Dict, List, Tuple, Any, Optional, Union, Callable
from functools import partial
import logging
from datetime import datetime

from scripts.strategies.refactored_edge.regime import (
    MarketRegimeType, determine_market_regime_advanced, simplify_regimes
)
from scripts.strategies.refactored_edge.signals_integration import generate_signals
from scripts.strategies.refactored_edge.position_sizing import (
    calculate_position_size, PositionSizeMethod, create_regime_position_config
)
from scripts.portfolio.custom_portfolio import CustomPortfolio
from scripts.utils.safe_utils import with_error_handling

# Setup logger
logger = logging.getLogger(__name__)

# ===========================================================================
# Regime-Aware Optimization Functions
# ===========================================================================

@with_error_handling
def optimize_regime_parameters(
    price_data: pd.DataFrame,
    n_trials: int = 50,
    test_split: float = 0.3,
    optimization_metric: str = 'sharpe',
    regime_split: bool = True,
    min_regime_segment: int = 30,
    use_position_sizing: bool = True,
    base_parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Optimize strategy parameters with regime-specific optimization.
    
    Args:
        price_data: DataFrame with OHLCV data
        n_trials: Number of optimization trials
        test_split: Proportion of data to use for out-of-sample testing
        optimization_metric: Metric to optimize ('sharpe', 'return', 'calmar', etc.)
        regime_split: Whether to perform separate optimizations for different regimes
        min_regime_segment: Minimum number of bars required for a regime segment
        use_position_sizing: Whether to use regime-aware position sizing
        base_parameters: Starting parameters to use for optimization
        
    Returns:
        Dictionary with optimized parameters for different regimes
    """
    # Preprocess data and calculate indicators
    data = preprocess_data(price_data)
    
    # Split data into train/test sets
    split_idx = int(len(data) * (1 - test_split))
    train_data = data.iloc[:split_idx].copy()
    test_data = data.iloc[split_idx:].copy()
    
    logger.info(f"Training data from {train_data.index[0]} to {train_data.index[-1]}")
    logger.info(f"Testing data from {test_data.index[0]} to {test_data.index[-1]}")
    
    # Determine market regimes
    train_regimes = determine_market_regime_advanced(
        adx=train_data['adx'],
        plus_di=train_data['plus_di'],
        minus_di=train_data['minus_di'],
        atr=train_data['atr'],
        close=train_data['close']
    )
    
    # Simplify regimes to basic trending/ranging for optimization
    simple_regimes = simplify_regimes(train_regimes)
    
    # Get regime segments for separate optimization
    if regime_split:
        trending_mask = (simple_regimes == MarketRegimeType.TRENDING)
        ranging_mask = (simple_regimes == MarketRegimeType.RANGING)
        
        # Only use segments with sufficient data points
        if trending_mask.sum() >= min_regime_segment and ranging_mask.sum() >= min_regime_segment:
            # Extract data segments for each regime
            trending_data = train_data[trending_mask].copy()
            ranging_data = train_data[ranging_mask].copy()
            
            logger.info(f"Trending data: {len(trending_data)} bars ({trending_mask.mean()*100:.1f}% of train data)")
            logger.info(f"Ranging data: {len(ranging_data)} bars ({ranging_mask.mean()*100:.1f}% of train data)")
            
            # Optimize parameters for each regime separately
            trending_params = run_regime_optimization(
                trending_data, 
                n_trials=n_trials//2,
                regime_type=MarketRegimeType.TRENDING,
                optimization_metric=optimization_metric,
                base_parameters=base_parameters
            )
            
            ranging_params = run_regime_optimization(
                ranging_data,
                n_trials=n_trials//2,
                regime_type=MarketRegimeType.RANGING,
                optimization_metric=optimization_metric,
                base_parameters=base_parameters
            )
            
            # Combine results
            optimized_params = {
                MarketRegimeType.TRENDING: trending_params,
                MarketRegimeType.RANGING: ranging_params
            }
        else:
            logger.warning("Insufficient data for separate regime optimization, using combined approach")
            regime_split = False
    
    # If not using regime split or insufficient data, optimize on full dataset
    if not regime_split:
        optimized_params = run_regime_optimization(
            train_data,
            n_trials=n_trials,
            regime_type=None,  # No specific regime
            optimization_metric=optimization_metric,
            base_parameters=base_parameters
        )
        
        # Format as dict with regimes
        optimized_params = {
            MarketRegimeType.TRENDING: optimized_params,
            MarketRegimeType.RANGING: optimized_params
        }
    
    # Validate the optimized parameters on test data
    test_metrics = validate_regime_parameters(
        test_data, 
        optimized_params,
        use_position_sizing=use_position_sizing
    )
    
    logger.info(f"Test metrics: {test_metrics}")
    
    # Add test metrics to results
    for regime, params in optimized_params.items():
        params.update({
            'test_metrics': test_metrics.get(regime, {})
        })
    
    return optimized_params


@with_error_handling
def run_regime_optimization(
    data: pd.DataFrame,
    n_trials: int,
    regime_type: Optional[str],
    optimization_metric: str = 'sharpe',
    base_parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Run optimization for a specific market regime.
    
    Args:
        data: DataFrame with OHLCV and indicator data
        n_trials: Number of optimization trials
        regime_type: Type of market regime being optimized for
        optimization_metric: Metric to optimize ('sharpe', 'return', 'calmar', etc.)
        base_parameters: Starting parameters to use for optimization
        
    Returns:
        Dictionary with optimized parameters for the regime
    """
    # Create Optuna study
    study_name = f"regime_optimization_{regime_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    study = optuna.create_study(
        study_name=study_name,
        direction="maximize",
        sampler=optuna.samplers.TPESampler(seed=42)
    )
    
    # Create objective function
    objective = partial(
        regime_optimization_objective,
        data=data,
        optimization_metric=optimization_metric,
        regime_type=regime_type,
        base_parameters=base_parameters or {}
    )
    
    # Run optimization
    logger.info(f"Starting optimization for regime: {regime_type} with {n_trials} trials")
    study.optimize(objective, n_trials=n_trials)
    
    # Get best parameters
    best_params = study.best_params
    
    # If we had base parameters, merge them with the optimized parameters
    if base_parameters:
        # Start with base parameters
        optimized_params = base_parameters.copy()
        # Update with optimized parameters
        optimized_params.update(best_params)
    else:
        optimized_params = best_params
    
    # Add optimization metrics
    optimized_params.update({
        'optimization_value': study.best_value,
        'optimization_metric': optimization_metric,
        'regime_type': regime_type,
        'n_trials': n_trials
    })
    
    logger.info(f"Best {optimization_metric} for {regime_type}: {study.best_value}")
    logger.info(f"Best parameters for {regime_type}: {best_params}")
    
    return optimized_params


@with_error_handling
def regime_optimization_objective(
    trial: optuna.Trial,
    data: pd.DataFrame,
    optimization_metric: str,
    regime_type: Optional[str],
    base_parameters: Dict[str, Any]
) -> float:
    """
    Objective function for Optuna optimization with regime awareness.
    
    Args:
        trial: Optuna trial object
        data: DataFrame with OHLCV and indicator data
        optimization_metric: Metric to optimize
        regime_type: Type of market regime being optimized for
        base_parameters: Base parameters to use
        
    Returns:
        Optimization metric value
    """
    # Suggest parameters for this trial
    params = suggest_parameters(trial, base_parameters, regime_type)
    
    # Generate trading signals using the suggested parameters
    signals = generate_signals(
        price=data['close'],
        high=data['high'],
        low=data['low'],
        rsi=data['rsi'],
        bb_upper=data['bb_upper'],
        bb_lower=data['bb_lower'],
        adx=data['adx'],
        atr=data['atr'],
        supply_zones=data.get('supply_zones'),
        demand_zones=data.get('demand_zones'),
        price_in_supply_zone=data.get('price_in_supply_zone'),
        price_in_demand_zone=data.get('price_in_demand_zone'),
        regimes=data.get('regimes'),  # Pass regimes if available
        **params  # Pass the suggested parameters
    )
    
    # Run backtest with the generated signals
    portfolio = CustomPortfolio.from_signals(
        close=data['close'],
        entries=signals['entries'],
        exits=signals['exits'],
        stop_loss=params.get('stop_loss', 0.05),
        take_profit=params.get('take_profit', 0.1),
        fees=0.001,
        slippage=0.001
    )
    
    # Calculate performance metrics
    metrics = calculate_performance_metrics(portfolio)
    
    # Return the targeted optimization metric
    if optimization_metric not in metrics:
        logger.warning(f"Requested metric {optimization_metric} not found in {metrics.keys()}")
        return -100.0  # Highly negative value to discourage this parameter set
    
    return metrics[optimization_metric]


@with_error_handling
def suggest_parameters(
    trial: optuna.Trial,
    base_parameters: Dict[str, Any],
    regime_type: Optional[str]
) -> Dict[str, Any]:
    """
    Suggest parameters for an optimization trial, with regime-specific modifications.
    
    Args:
        trial: Optuna trial object
        base_parameters: Base parameters to use
        regime_type: Type of market regime being optimized for
        
    Returns:
        Dictionary with suggested parameters
    """
    params = {}
    
    # RSI parameters
    if regime_type == MarketRegimeType.TRENDING:
        # For trending regimes, prefer stronger trends
        params['rsi_upper'] = trial.suggest_int('rsi_upper', 65, 85, step=5)
        params['rsi_lower'] = trial.suggest_int('rsi_lower', 20, 40, step=5)
    elif regime_type == MarketRegimeType.RANGING:
        # For ranging regimes, prefer mean reversion
        params['rsi_upper'] = trial.suggest_int('rsi_upper', 60, 75, step=5)
        params['rsi_lower'] = trial.suggest_int('rsi_lower', 25, 45, step=5)
    else:
        # Default ranges
        params['rsi_upper'] = trial.suggest_int('rsi_upper', 60, 80, step=5)
        params['rsi_lower'] = trial.suggest_int('rsi_lower', 20, 40, step=5)
    
    # Bollinger Bands parameters
    params['bb_std'] = trial.suggest_float('bb_std', 1.5, 3.0, step=0.1)
    
    # ADX parameter
    if regime_type == MarketRegimeType.TRENDING:
        # For trending regimes, allow lower ADX threshold
        params['adx_threshold'] = trial.suggest_float('adx_threshold', 20.0, 30.0, step=0.5)
    elif regime_type == MarketRegimeType.RANGING:
        # For ranging regimes, prefer higher ADX threshold
        params['adx_threshold'] = trial.suggest_float('adx_threshold', 25.0, 35.0, step=0.5)
    else:
        # Default range
        params['adx_threshold'] = trial.suggest_float('adx_threshold', 20.0, 35.0, step=0.5)
    
    # Zone parameters
    params['use_zones'] = trial.suggest_categorical('use_zones', [True, False])
    params['zone_proximity_pct'] = trial.suggest_float('zone_proximity_pct', 0.005, 0.03, step=0.005)
    
    # Position sizing
    params['stop_loss'] = trial.suggest_float('stop_loss', 0.01, 0.1, step=0.01)
    params['take_profit'] = trial.suggest_float('take_profit', 0.02, 0.2, step=0.01)
    
    # Signal generation parameters
    if regime_type == MarketRegimeType.TRENDING:
        # For trending regimes, prefer more conservative signals
        params['min_holding_period'] = trial.suggest_int('min_holding_period', 8, 24, step=2)
        params['trend_strength_weight'] = trial.suggest_float('trend_strength_weight', 0.6, 1.0, step=0.05)
        params['zone_influence'] = trial.suggest_float('zone_influence', 0.3, 0.7, step=0.05)
    elif regime_type == MarketRegimeType.RANGING:
        # For ranging regimes, prefer more frequent signals
        params['min_holding_period'] = trial.suggest_int('min_holding_period', 3, 12, step=1)
        params['trend_strength_weight'] = trial.suggest_float('trend_strength_weight', 0.3, 0.7, step=0.05)
        params['zone_influence'] = trial.suggest_float('zone_influence', 0.5, 0.9, step=0.05)
    else:
        # Default ranges
        params['min_holding_period'] = trial.suggest_int('min_holding_period', 4, 20, step=2)
        params['trend_strength_weight'] = trial.suggest_float('trend_strength_weight', 0.4, 0.9, step=0.05)
        params['zone_influence'] = trial.suggest_float('zone_influence', 0.4, 0.8, step=0.05)
    
    return params


@with_error_handling
def validate_regime_parameters(
    data: pd.DataFrame,
    regime_params: Dict[str, Dict[str, Any]],
    use_position_sizing: bool = True
) -> Dict[str, Dict[str, float]]:
    """
    Validate optimized parameters on test data with regime awareness.
    
    Args:
        data: DataFrame with OHLCV and indicator data
        regime_params: Dictionary mapping regime types to parameter sets
        use_position_sizing: Whether to use regime-aware position sizing
        
    Returns:
        Dictionary with test metrics for each regime
    """
    # Determine market regimes in test data
    test_regimes = determine_market_regime_advanced(
        adx=data['adx'],
        plus_di=data['plus_di'],
        minus_di=data['minus_di'],
        atr=data['atr'],
        close=data['close']
    )
    
    # Simplify regimes to basic trending/ranging for parameter application
    simple_regimes = simplify_regimes(test_regimes)
    
    # Generate signals with regime-aware parameters
    signals = generate_signals(
        price=data['close'],
        high=data['high'],
        low=data['low'],
        rsi=data['rsi'],
        bb_upper=data['bb_upper'],
        bb_lower=data['bb_lower'],
        adx=data['adx'],
        atr=data['atr'],
        supply_zones=data.get('supply_zones'),
        demand_zones=data.get('demand_zones'),
        price_in_supply_zone=data.get('price_in_supply_zone'),
        price_in_demand_zone=data.get('price_in_demand_zone'),
        regimes=simple_regimes,  # Pass regimes for regime-aware signal generation
        regime_params=regime_params  # Pass regime-specific parameters
    )
    
    # Calculate position sizes if enabled
    if use_position_sizing:
        # Get stop loss parameter for each regime
        trending_sl = regime_params.get(MarketRegimeType.TRENDING, {}).get('stop_loss', 0.05)
        ranging_sl = regime_params.get(MarketRegimeType.RANGING, {}).get('stop_loss', 0.05)
        
        # Calculate appropriate position sizes
        position_sizes = calculate_position_size(
            price=data['close'],
            regimes=simple_regimes,
            atr=data['atr'],
            method=PositionSizeMethod.REGIME_AWARE
        )
    else:
        # Use fixed position sizes
        position_sizes = pd.Series(1.0, index=data.index)
    
    # Run backtest with the generated signals
    portfolio = CustomPortfolio.from_signals(
        close=data['close'],
        entries=signals['entries'] * position_sizes,  # Scale entries by position size
        exits=signals['exits'],
        stop_loss=0.05,  # Use a fixed stop loss for the backtest
        take_profit=0.1,  # Use a fixed take profit for the backtest
        fees=0.001,
        slippage=0.001
    )
    
    # Calculate overall performance metrics
    overall_metrics = calculate_performance_metrics(portfolio)
    
    # Calculate regime-specific metrics
    metrics_by_regime = {}
    
    # Process trending segments
    trending_mask = (simple_regimes == MarketRegimeType.TRENDING)
    if trending_mask.sum() > 0:
        trending_metrics = calculate_segment_metrics(
            portfolio, trending_mask, "Trending"
        )
        metrics_by_regime[MarketRegimeType.TRENDING] = trending_metrics
    
    # Process ranging segments
    ranging_mask = (simple_regimes == MarketRegimeType.RANGING)
    if ranging_mask.sum() > 0:
        ranging_metrics = calculate_segment_metrics(
            portfolio, ranging_mask, "Ranging"
        )
        metrics_by_regime[MarketRegimeType.RANGING] = ranging_metrics
    
    # Add overall metrics
    metrics_by_regime['overall'] = overall_metrics
    
    return metrics_by_regime


@with_error_handling
def calculate_segment_metrics(
    portfolio: "CustomPortfolio",
    segment_mask: pd.Series,
    segment_name: str
) -> Dict[str, float]:
    """
    Calculate performance metrics for a specific segment of the portfolio.
    
    Args:
        portfolio: CustomPortfolio instance
        segment_mask: Boolean mask identifying the segment
        segment_name: Name of the segment for logging
        
    Returns:
        Dictionary of performance metrics for the segment
    """
    # Extract segment-specific equity curve
    if hasattr(portfolio, 'equity_curve'):
        equity = portfolio.equity_curve
    else:
        equity = portfolio.value
        
    # Calculate returns within the segment
    segment_equity = equity[segment_mask]
    
    if len(segment_equity) > 0:
        # Calculate segment metrics
        start_equity = segment_equity.iloc[0]
        end_equity = segment_equity.iloc[-1]
        segment_return = (end_equity / start_equity) - 1
        
        # Calculate daily returns
        daily_returns = segment_equity.pct_change().dropna()
        
        # Calculate metrics
        sharpe = calculate_sharpe_ratio(daily_returns)
        max_dd = calculate_max_drawdown(segment_equity)
        
        metrics = {
            'return': segment_return,
            'sharpe': sharpe,
            'max_drawdown': max_dd,
            'calmar': abs(segment_return) / abs(max_dd) if abs(max_dd) > 0 else 0,
            'n_bars': len(segment_equity)
        }
    else:
        # No data for this segment
        metrics = {
            'return': 0,
            'sharpe': 0,
            'max_drawdown': 0,
            'calmar': 0,
            'n_bars': 0
        }
    
    logger.info(f"{segment_name} segment metrics: {metrics}")
    return metrics


@with_error_handling
def calculate_performance_metrics(portfolio: "CustomPortfolio") -> Dict[str, float]:
    """
    Calculate standard performance metrics for a portfolio.
    
    Args:
        portfolio: CustomPortfolio instance
        
    Returns:
        Dictionary of performance metrics
    """
    # Get equity curve
    if hasattr(portfolio, 'equity_curve'):
        equity = portfolio.equity_curve
    else:
        equity = portfolio.value
    
    # Calculate returns
    returns = equity.pct_change().dropna()
    total_return = (equity.iloc[-1] / equity.iloc[0]) - 1
    
    # Extract trade statistics
    if hasattr(portfolio, 'stats') and hasattr(portfolio.stats, 'total'):
        win_rate = portfolio.stats.total.win_rate
        profit_factor = portfolio.stats.total.profit_factor
    else:
        # Calculate from trades if available
        trades_df = CustomPortfolio.get_trades_df(portfolio)
        if not trades_df.empty and 'PnL' in trades_df.columns:
            win_trades = trades_df[trades_df['PnL'] > 0]
            lose_trades = trades_df[trades_df['PnL'] < 0]
            
            win_rate = len(win_trades) / len(trades_df) if len(trades_df) > 0 else 0
            profit_factor = abs(win_trades['PnL'].sum() / lose_trades['PnL'].sum()) if lose_trades['PnL'].sum() != 0 else 0
        else:
            win_rate = 0
            profit_factor = 0
    
    # Calculate Sharpe ratio
    sharpe = calculate_sharpe_ratio(returns)
    
    # Calculate max drawdown
    max_dd = calculate_max_drawdown(equity)
    
    # Calculate Calmar ratio
    calmar = abs(total_return) / abs(max_dd) if abs(max_dd) > 0 else 0
    
    # Return metrics
    return {
        'return': total_return,
        'sharpe': sharpe,
        'max_drawdown': max_dd,
        'calmar': calmar,
        'win_rate': win_rate,
        'profit_factor': profit_factor
    }


@with_error_handling
def calculate_sharpe_ratio(returns: pd.Series) -> float:
    """
    Calculate the Sharpe ratio from a series of returns.
    
    Args:
        returns: Series of period returns
        
    Returns:
        Sharpe ratio (annualized if daily returns)
    """
    if len(returns) == 0 or returns.std() == 0:
        return 0
    
    # Calculate Sharpe ratio (return / volatility)
    sharpe = returns.mean() / returns.std()
    
    # Annualize (assuming daily returns)
    sharpe_annualized = sharpe * np.sqrt(252)
    
    return sharpe_annualized


@with_error_handling
def calculate_max_drawdown(equity: pd.Series) -> float:
    """
    Calculate the maximum drawdown from an equity curve.
    
    Args:
        equity: Series of equity values
        
    Returns:
        Maximum drawdown as a positive decimal value
    """
    # Calculate running maximum
    running_max = equity.cummax()
    
    # Calculate drawdown
    drawdown = (equity - running_max) / running_max
    
    # Get maximum drawdown
    max_dd = drawdown.min()
    
    return max_dd


@with_error_handling
def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess data for optimization by calculating necessary indicators.
    
    Args:
        data: DataFrame with OHLCV data
        
    Returns:
        DataFrame with added indicators
    """
    import vectorbtpro as vbt
    
    # Make a copy to avoid modifying the original
    df = data.copy()
    
    # Ensure we have required OHLCV columns
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            # Try case-insensitive match
            for existing_col in df.columns:
                if existing_col.lower() == col:
                    df[col] = df[existing_col]
                    break
            else:
                if col != 'volume':  # Volume is optional
                    raise ValueError(f"Required column {col} not found in data")
    
    # Calculate RSI
    rsi = vbt.talib('RSI').run(df['close'], timeperiod=14).real
    df['rsi'] = rsi
    
    # Calculate Bollinger Bands
    bbands = vbt.talib('BBANDS').run(
        df['close'], 
        timeperiod=20, 
        nbdevup=2, 
        nbdevdn=2
    )
    df['bb_upper'] = bbands.upperband
    df['bb_middle'] = bbands.middleband
    df['bb_lower'] = bbands.lowerband
    
    # Calculate ADX
    adx_indicator = vbt.talib('ADX').run(
        df['high'], 
        df['low'], 
        df['close'], 
        timeperiod=14
    )
    df['adx'] = adx_indicator.real
    
    # Calculate Directional Movement indicators
    di_plus = vbt.talib('PLUS_DI').run(
        df['high'], 
        df['low'], 
        df['close'], 
        timeperiod=14
    ).real
    di_minus = vbt.talib('MINUS_DI').run(
        df['high'], 
        df['low'], 
        df['close'], 
        timeperiod=14
    ).real
    
    df['plus_di'] = di_plus
    df['minus_di'] = di_minus
    
    # Calculate ATR
    atr = vbt.talib('ATR').run(
        df['high'], 
        df['low'], 
        df['close'], 
        timeperiod=14
    ).real
    df['atr'] = atr
    
    # Fill NaN values
    df = df.fillna(method='bfill').fillna(method='ffill')
    
    return df


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Regime optimization module loaded.")
