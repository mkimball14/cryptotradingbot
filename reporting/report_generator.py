import pandas as pd
import logging
import numpy as np

logger = logging.getLogger(__name__)

def calculate_risk_metrics(portfolio):
    """
    Calculate key risk and performance metrics from a VectorBT portfolio.
    Handles potential missing stats gracefully.
    
    Args:
        portfolio: A vectorbtpro Portfolio object
        
    Returns:
        Dictionary with performance metrics
    """
    metrics = {
        'total_return': 0, 'sharpe': 0, 'max_dd': 0, 'win_rate': 0,
        'trades': 0, 'annual_return': 0, 'sortino': 0, 'profit_factor': 0,
        'recovery_factor': 0
    }
    if portfolio is None:
        return metrics
    try:
        stats = portfolio.stats()
        metrics['total_return'] = stats.get('Total Return [%]', 0) / 100
        metrics['sharpe'] = stats.get('Sharpe Ratio', 0)
        metrics['max_dd'] = stats.get('Max Drawdown [%]', 0) / 100
        metrics['trades'] = stats.get('Total Trades', 0)
        metrics['win_rate'] = stats.get('Win Rate [%]', 0) / 100
        metrics['profit_factor'] = stats.get('Profit Factor', 0)
        if metrics['max_dd'] > 0:
            metrics['recovery_factor'] = metrics['total_return'] / metrics['max_dd']
        else:
             metrics['recovery_factor'] = float('inf') if metrics['total_return'] > 0 else 0
        start_date = portfolio.wrapper.index[0]
        end_date = portfolio.wrapper.index[-1]
        years = (end_date - start_date).days / 365.25
        if years > 0:
             metrics['annual_return'] = (1 + metrics['total_return'])**(1/years) - 1
        else:
             metrics['annual_return'] = 0
        metrics['sortino'] = stats.get('Sortino Ratio', 0)
    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}", exc_info=True)
    return metrics 