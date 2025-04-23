import sys
import os
from pathlib import Path
import vectorbtpro as vbt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, List, Tuple, Optional, Callable
from dotenv import load_dotenv

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Import data fetcher
try:
    from data.data_fetcher import fetch_historical_data, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    logger = logging.getLogger(__name__)
    logger.info("Using data_fetcher from data module.")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Could not import data_fetcher: {e}. Functionality may be limited.")
    # Define dummy functions if data_fetcher is critical and missing
    def fetch_historical_data(*args, **kwargs): return None
    def get_vbt_freq_str(*args, **kwargs): return "1h"
    GRANULARITY_MAP_SECONDS = {'1h': 3600}

# Load environment variables
load_dotenv(verbose=True)

def init_logging():
    """Initialize logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    logger = logging.getLogger('wfo_edge_rebalancing')
    logger.setLevel(logging.INFO)
    
    # Set other libraries to be less verbose
    logging.getLogger('vectorbtpro').setLevel(logging.WARNING)
    logging.getLogger('numba').setLevel(logging.WARNING)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    return logger

# Global logger
logger = init_logging()

# --- Configuration Constants ---
INITIAL_CAPITAL = 10000
COMMISSION_PCT = 0.001
SLIPPAGE_PCT = 0.0005

# Data Parameters
TOTAL_HISTORY_DAYS = 365  # 1 year of data
END_DATE = datetime.now().strftime('%Y-%m-%d')
START_DATE = (datetime.now() - timedelta(days=TOTAL_HISTORY_DAYS)).strftime('%Y-%m-%d')
DEFAULT_SYMBOLS = ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD"]
GRANULARITY_STR = "1h"  # 1-hour data
try:
    GRANULARITY_SECONDS = GRANULARITY_MAP_SECONDS[GRANULARITY_STR]
except KeyError:
    logger.error(f"Invalid GRANULARITY_STR: {GRANULARITY_STR}. Defaulting to 1h (3600s).")
    GRANULARITY_SECONDS = 3600

# Portfolio Optimization Parameters
REBALANCE_FREQUENCY = "W"  # Weekly rebalancing
RISK_FREE_RATE = 0.02  # 2% annualized
LOOKBACK_WINDOW = 30  # Days to look back for optimization

# Strategy Parameters
STRATEGY_TYPE = "mean_variance"  # Options: "mean_variance", "max_sharpe", "min_variance", "equal_weight"

def fetch_data(symbols: List[str], start_date: str, end_date: str, 
               granularity_seconds: int) -> pd.DataFrame:
    """
    Fetch historical data for multiple symbols and combine into a single DataFrame.
    
    Args:
        symbols: List of symbols to fetch
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        granularity_seconds: Granularity in seconds
        
    Returns:
        DataFrame with OHLCV data for all symbols
    """
    logger.info(f"Fetching data for {len(symbols)} symbols from {start_date} to {end_date}")
    
    # Create a dictionary to store DataFrames for each symbol
    data_dict = {}
    
    # Fetch data for each symbol
    for symbol in symbols:
        try:
            symbol_data = fetch_historical_data(
                symbol, start_date, end_date, granularity_seconds
            )
            
            if symbol_data is not None and not symbol_data.empty:
                # Rename columns to include symbol name
                symbol_data.columns = [f"{col}" for col in symbol_data.columns]
                data_dict[symbol] = symbol_data
                logger.info(f"Successfully fetched {len(symbol_data)} periods for {symbol}")
            else:
                logger.warning(f"Failed to fetch data for {symbol}")
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
    
    if not data_dict:
        logger.error("Failed to fetch data for any symbols")
        return None
    
    # Create a MultiIndex DataFrame with all data
    # First, ensure all DataFrames have the same index
    common_idx = None
    for df in data_dict.values():
        if common_idx is None:
            common_idx = df.index
        else:
            common_idx = common_idx.intersection(df.index)
    
    # Reindex all DataFrames to the common index
    for symbol in data_dict:
        data_dict[symbol] = data_dict[symbol].reindex(common_idx)
    
    # Create combined DataFrame with hierarchical columns
    combined_data = pd.DataFrame()
    
    # Add close prices for each symbol
    for symbol, df in data_dict.items():
        combined_data[symbol] = df['close']
    
    logger.info(f"Created combined DataFrame with {len(combined_data)} periods")
    return combined_data

def calculate_returns(prices: pd.DataFrame, window: int = 1) -> pd.DataFrame:
    """
    Calculate returns from price data.
    
    Args:
        prices: DataFrame with price data
        window: Window for return calculation
        
    Returns:
        DataFrame with returns
    """
    returns = prices.pct_change(window).dropna()
    return returns

def allocate_equal_weight(returns: pd.DataFrame, lookback: int, 
                          current_index: int) -> np.ndarray:
    """
    Equal weight allocation function.
    
    Args:
        returns: DataFrame with returns
        lookback: Lookback window for calculation
        current_index: Current index point for allocation
        
    Returns:
        Array of weights
    """
    n_assets = returns.shape[1]
    return np.array([1/n_assets] * n_assets)

def allocate_max_sharpe(returns: pd.DataFrame, lookback: int, 
                        current_index: int, risk_free_rate: float = RISK_FREE_RATE) -> np.ndarray:
    """
    Maximize Sharpe ratio allocation function.
    
    Args:
        returns: DataFrame with returns
        lookback: Lookback window for calculation
        current_index: Current index point for allocation
        risk_free_rate: Annualized risk-free rate
        
    Returns:
        Array of weights
    """
    # Extract relevant returns
    if current_index < lookback:
        period_returns = returns.iloc[:current_index]
    else:
        period_returns = returns.iloc[current_index-lookback:current_index]
    
    if period_returns.empty:
        n_assets = returns.shape[1]
        return np.array([1/n_assets] * n_assets)
    
    # Calculate expected returns and covariance
    expected_returns = period_returns.mean() * 252  # Annualize
    cov_matrix = period_returns.cov() * 252  # Annualize
    
    try:
        # Use vectorbt's optimization function to maximize Sharpe ratio
        weights = vbt.portfolio.nb.optimize_sharpe_ratio_nb(
            expected_returns.values,
            cov_matrix.values,
            risk_free_rate=risk_free_rate
        )
        return weights
    except Exception as e:
        logger.error(f"Error in max_sharpe optimization: {str(e)}")
        # Fall back to equal weight
        n_assets = returns.shape[1]
        return np.array([1/n_assets] * n_assets)

def allocate_min_variance(returns: pd.DataFrame, lookback: int, 
                          current_index: int) -> np.ndarray:
    """
    Minimize variance allocation function.
    
    Args:
        returns: DataFrame with returns
        lookback: Lookback window for calculation
        current_index: Current index point for allocation
        
    Returns:
        Array of weights
    """
    # Extract relevant returns
    if current_index < lookback:
        period_returns = returns.iloc[:current_index]
    else:
        period_returns = returns.iloc[current_index-lookback:current_index]
    
    if period_returns.empty:
        n_assets = returns.shape[1]
        return np.array([1/n_assets] * n_assets)
    
    # Calculate covariance
    cov_matrix = period_returns.cov() * 252  # Annualize
    
    try:
        # Use vectorbt's optimization function to minimize variance
        weights = vbt.portfolio.nb.optimize_min_volatility_nb(cov_matrix.values)
        return weights
    except Exception as e:
        logger.error(f"Error in min_variance optimization: {str(e)}")
        # Fall back to equal weight
        n_assets = returns.shape[1]
        return np.array([1/n_assets] * n_assets)

def create_allocation_func(strategy_type: str, lookback: int = LOOKBACK_WINDOW, 
                          risk_free_rate: float = RISK_FREE_RATE) -> Callable:
    """
    Create allocation function based on strategy type.
    
    Args:
        strategy_type: Type of allocation strategy
        lookback: Lookback window for calculation
        risk_free_rate: Annualized risk-free rate
        
    Returns:
        Allocation function
    """
    if strategy_type == "equal_weight":
        return lambda returns, index_point: allocate_equal_weight(returns, lookback, index_point)
    elif strategy_type == "max_sharpe":
        return lambda returns, index_point: allocate_max_sharpe(returns, lookback, index_point, risk_free_rate)
    elif strategy_type == "min_variance":
        return lambda returns, index_point: allocate_min_variance(returns, lookback, index_point)
    else:
        logger.warning(f"Unknown strategy type: {strategy_type}. Using equal weight.")
        return lambda returns, index_point: allocate_equal_weight(returns, lookback, index_point)

def optimize_portfolio_rebalancing(prices: pd.DataFrame, 
                                  strategy_type: str = STRATEGY_TYPE,
                                  rebalance_freq: str = REBALANCE_FREQUENCY,
                                  lookback: int = LOOKBACK_WINDOW,
                                  risk_free_rate: float = RISK_FREE_RATE,
                                  init_cash: float = INITIAL_CAPITAL) -> vbt.Portfolio:
    """
    Optimize portfolio with periodic rebalancing.
    
    Args:
        prices: DataFrame with price data
        strategy_type: Type of allocation strategy
        rebalance_freq: Rebalancing frequency (W for weekly, M for monthly, etc.)
        lookback: Lookback window for calculation
        risk_free_rate: Annualized risk-free rate
        init_cash: Initial capital
        
    Returns:
        Portfolio object
    """
    # Calculate returns
    returns = calculate_returns(prices)
    
    # Generate rebalancing dates based on frequency
    logger.info(f"Generating rebalancing dates with frequency: {rebalance_freq}")
    
    # Determine rebalancing dates
    if rebalance_freq.lower() == 'w':
        # Weekly - group by ISO week
        rebalance_dates = pd.date_range(
            start=prices.index.min(),
            end=prices.index.max(), 
            freq='W'
        )
    elif rebalance_freq.lower() == 'm':
        # Monthly - group by month
        rebalance_dates = pd.date_range(
            start=prices.index.min(),
            end=prices.index.max(), 
            freq='MS'  # Month start
        )
    elif rebalance_freq.lower() == 'd':
        # Daily - use all days
        rebalance_dates = pd.date_range(
            start=prices.index.min(),
            end=prices.index.max(), 
            freq='D'
        )
    else:
        # Try custom frequency
        try:
            rebalance_dates = pd.date_range(
                start=prices.index.min(),
                end=prices.index.max(), 
                freq=rebalance_freq
            )
        except Exception as e:
            logger.warning(f"Could not parse frequency '{rebalance_freq}', using weekly: {str(e)}")
            rebalance_dates = pd.date_range(
                start=prices.index.min(),
                end=prices.index.max(), 
                freq='W'
            )
    
    # Filter to only include dates that are in our price index
    valid_dates = [date for date in rebalance_dates if date in prices.index]
    if not valid_dates:
        # If no valid dates, include at least the first date
        valid_dates = [prices.index[0]]
    
    logger.info(f"Found {len(valid_dates)} valid rebalancing dates")
    
    try:
        # Create allocations for each rebalancing date
        allocations = {}
        
        # For equal weight strategy
        if strategy_type == "equal_weight":
            logger.info("Using equal weight allocation strategy")
            n_symbols = len(prices.columns)
            equal_weights = np.full(n_symbols, 1/n_symbols)
            
            for date in valid_dates:
                allocations[date] = equal_weights
                
        # For max Sharpe ratio
        elif strategy_type == "max_sharpe":
            logger.info("Using maximum Sharpe ratio allocation strategy")
            
            for date in valid_dates:
                # Calculate lookback window
                start_idx = max(0, prices.index.get_loc(date) - lookback)
                if start_idx == prices.index.get_loc(date):  # Not enough history
                    # Use equal weights for the first rebalance
                    weights = np.full(len(prices.columns), 1/len(prices.columns))
                else:
                    # Get historical data for lookback period
                    hist_returns = returns.iloc[start_idx:prices.index.get_loc(date)]
                    
                    # Skip if not enough data points
                    if len(hist_returns) < 5:  # Need at least a few data points
                        weights = np.full(len(prices.columns), 1/len(prices.columns))
                    else:
                        # Calculate expected returns and covariance
                        expected_returns = hist_returns.mean() * 252  # Annualize
                        cov_matrix = hist_returns.cov() * 252  # Annualize
                        
                        try:
                            # Try to use the portfolio module's optimization functions
                            import vectorbtpro.portfolio as vbt_portfolio
                            
                            # Check if optimize_sharpe_ratio_nb exists
                            if hasattr(vbt_portfolio.nb, 'optimize_sharpe_ratio_nb'):
                                weights = vbt_portfolio.nb.optimize_sharpe_ratio_nb(
                                    expected_returns.values,
                                    cov_matrix.values,
                                    risk_free_rate=risk_free_rate
                                )
                            else:
                                # Try older optimization methods
                                from scipy.optimize import minimize
                                
                                # Objective function for negative Sharpe ratio
                                def neg_sharpe(weights, expected_returns, cov_matrix, risk_free_rate):
                                    weights = np.array(weights)
                                    port_return = np.sum(expected_returns * weights)
                                    port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                                    sharpe = (port_return - risk_free_rate) / port_vol
                                    return -sharpe
                                
                                # Constraints and bounds
                                constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
                                bounds = tuple((0, 1) for _ in range(len(prices.columns)))
                                
                                # Initial equal weights
                                init_weights = np.full(len(prices.columns), 1/len(prices.columns))
                                
                                # Optimize
                                result = minimize(
                                    neg_sharpe,
                                    init_weights,
                                    args=(expected_returns, cov_matrix, risk_free_rate),
                                    method='SLSQP',
                                    bounds=bounds,
                                    constraints=constraints
                                )
                                
                                if result.success:
                                    weights = result.x
                                else:
                                    # Fall back to equal weights
                                    weights = init_weights
                        except Exception as e:
                            logger.warning(f"Optimization failed: {str(e)}. Using equal weights.")
                            weights = np.full(len(prices.columns), 1/len(prices.columns))
                
                allocations[date] = weights
                
        # For minimum variance
        elif strategy_type == "min_variance":
            logger.info("Using minimum variance allocation strategy")
            
            for date in valid_dates:
                # Calculate lookback window
                start_idx = max(0, prices.index.get_loc(date) - lookback)
                if start_idx == prices.index.get_loc(date):  # Not enough history
                    # Use equal weights for the first rebalance
                    weights = np.full(len(prices.columns), 1/len(prices.columns))
                else:
                    # Get historical data for lookback period
                    hist_returns = returns.iloc[start_idx:prices.index.get_loc(date)]
                    
                    # Skip if not enough data points
                    if len(hist_returns) < 5:  # Need at least a few data points
                        weights = np.full(len(prices.columns), 1/len(prices.columns))
                    else:
                        # Calculate covariance
                        cov_matrix = hist_returns.cov() * 252  # Annualize
                        
                        try:
                            # Try to use the portfolio module's optimization functions
                            import vectorbtpro.portfolio as vbt_portfolio
                            
                            # Check if optimize_min_volatility_nb exists
                            if hasattr(vbt_portfolio.nb, 'optimize_min_volatility_nb'):
                                weights = vbt_portfolio.nb.optimize_min_volatility_nb(
                                    cov_matrix.values
                                )
                            else:
                                # Use scipy for optimization
                                from scipy.optimize import minimize
                                
                                # Objective function for portfolio variance
                                def portfolio_volatility(weights, cov_matrix):
                                    weights = np.array(weights)
                                    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                                
                                # Constraints and bounds
                                constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
                                bounds = tuple((0, 1) for _ in range(len(prices.columns)))
                                
                                # Initial equal weights
                                init_weights = np.full(len(prices.columns), 1/len(prices.columns))
                                
                                # Optimize
                                result = minimize(
                                    portfolio_volatility,
                                    init_weights,
                                    args=(cov_matrix,),
                                    method='SLSQP',
                                    bounds=bounds,
                                    constraints=constraints
                                )
                                
                                if result.success:
                                    weights = result.x
                                else:
                                    # Fall back to equal weights
                                    weights = init_weights
                        except Exception as e:
                            logger.warning(f"Optimization failed: {str(e)}. Using equal weights.")
                            weights = np.full(len(prices.columns), 1/len(prices.columns))
                
                allocations[date] = weights
        
        else:
            logger.warning(f"Unknown strategy type: {strategy_type}. Using equal weight.")
            n_symbols = len(prices.columns)
            equal_weights = np.full(n_symbols, 1/n_symbols)
            
            for date in valid_dates:
                allocations[date] = equal_weights
        
        # Create portfolio with calculated allocations using direct portfolio creation
        logger.info(f"Creating portfolio with {len(allocations)} rebalancing points")
        try:
            # Try to directly use Portfolio.from_allocations
            portfolio = vbt.Portfolio.from_allocations(
                prices,
                allocations,
                init_cash=init_cash,
                fees=COMMISSION_PCT/100,
                slippage=SLIPPAGE_PCT/100,
                freq=get_vbt_freq_str(GRANULARITY_STR)
            )
        except Exception as e:
            # If the above fails, try more direct approach with the portfolio module
            try:
                import vectorbtpro.portfolio as vbt_portfolio
                portfolio = vbt_portfolio.Portfolio.from_allocations(
                    prices,
                    allocations,
                    init_cash=init_cash,
                    fees=COMMISSION_PCT/100,
                    slippage=SLIPPAGE_PCT/100,
                    freq=get_vbt_freq_str(GRANULARITY_STR)
                )
            except Exception as e2:
                logger.error(f"Both portfolio creation methods failed: \nMethod 1: {str(e)}\nMethod 2: {str(e2)}")
                return None
        
        logger.info("Portfolio simulation completed successfully")
        return portfolio
    
    except Exception as e:
        logger.error(f"Error in portfolio optimization: {str(e)}")
        return None

def run_backtest(symbols: List[str] = DEFAULT_SYMBOLS,
                start_date: str = START_DATE,
                end_date: str = END_DATE,
                strategy_type: str = STRATEGY_TYPE,
                rebalance_freq: str = REBALANCE_FREQUENCY,
                lookback: int = LOOKBACK_WINDOW,
                risk_free_rate: float = RISK_FREE_RATE,
                init_cash: float = INITIAL_CAPITAL) -> Dict[str, Any]:
    """
    Run backtest with the specified parameters.
    
    Args:
        symbols: List of symbols to include
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        strategy_type: Type of allocation strategy
        rebalance_freq: Rebalancing frequency
        lookback: Lookback window for calculation
        risk_free_rate: Annualized risk-free rate
        init_cash: Initial capital
        
    Returns:
        Dictionary with backtest results
    """
    # Fetch data
    prices = fetch_data(symbols, start_date, end_date, GRANULARITY_SECONDS)
    
    if prices is None or prices.empty:
        logger.error("No data available for backtest")
        return {
            "success": False,
            "error": "No data available"
        }
    
    # Optimize portfolio
    portfolio = optimize_portfolio_rebalancing(
        prices,
        strategy_type=strategy_type,
        rebalance_freq=rebalance_freq,
        lookback=lookback,
        risk_free_rate=risk_free_rate,
        init_cash=init_cash
    )
    
    if portfolio is None:
        logger.error("Portfolio optimization failed")
        return {
            "success": False,
            "error": "Portfolio optimization failed"
        }
    
    # Calculate performance metrics
    try:
        stats = portfolio.stats()
        
        # Extract key metrics
        results = {
            "success": True,
            "total_return": stats.get("total_return", 0),
            "sharpe_ratio": stats.get("sharpe_ratio", 0),
            "max_drawdown": stats.get("max_drawdown", 0),
            "win_rate": stats.get("win_rate", 0),
            "calmar_ratio": stats.get("calmar_ratio", 0),
            "num_trades": portfolio.trades.count if hasattr(portfolio.trades, "count") else 0,
            "portfolio": portfolio,
            "allocations": portfolio.allocations.to_dict() if hasattr(portfolio, "allocations") else {},
            "strategy_type": strategy_type,
            "rebalance_freq": rebalance_freq,
            "lookback": lookback,
            "symbols": symbols
        }
        
        logger.info(f"Backtest results: Total Return: {results['total_return']:.2%}, "
                  f"Sharpe: {results['sharpe_ratio']:.2f}")
        
        return results
    
    except Exception as e:
        logger.error(f"Error calculating performance metrics: {str(e)}")
        return {
            "success": False,
            "error": f"Error calculating performance metrics: {str(e)}",
            "portfolio": portfolio
        }

def compare_strategies(symbols: List[str] = DEFAULT_SYMBOLS,
                      start_date: str = START_DATE,
                      end_date: str = END_DATE,
                      strategies: List[str] = ["equal_weight", "max_sharpe", "min_variance"],
                      rebalance_freq: str = REBALANCE_FREQUENCY) -> Dict[str, Any]:
    """
    Compare multiple portfolio optimization strategies.
    
    Args:
        symbols: List of symbols to include
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        strategies: List of strategy types to compare
        rebalance_freq: Rebalancing frequency
        
    Returns:
        Dictionary with comparison results
    """
    results = {}
    
    for strategy in strategies:
        logger.info(f"Running backtest for {strategy} strategy")
        result = run_backtest(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            strategy_type=strategy,
            rebalance_freq=rebalance_freq
        )
        
        results[strategy] = result
    
    # Compare results
    comparison = {
        "strategies": strategies,
        "rebalance_freq": rebalance_freq,
        "symbols": symbols,
        "start_date": start_date,
        "end_date": end_date,
    }
    
    # Add performance metrics for each strategy
    metrics = ["total_return", "sharpe_ratio", "max_drawdown", "win_rate", "calmar_ratio"]
    for metric in metrics:
        comparison[metric] = {
            strategy: results[strategy].get(metric, 0) if results[strategy].get("success", False) else 0
            for strategy in strategies
        }
    
    # Determine best strategy based on Sharpe ratio
    valid_strategies = [
        strategy for strategy in strategies 
        if results[strategy].get("success", False) and results[strategy].get("sharpe_ratio", 0) > 0
    ]
    
    if valid_strategies:
        best_strategy = max(
            valid_strategies,
            key=lambda s: results[s].get("sharpe_ratio", 0)
        )
        comparison["best_strategy"] = best_strategy
        comparison["best_sharpe"] = results[best_strategy].get("sharpe_ratio", 0)
    else:
        comparison["best_strategy"] = None
        comparison["best_sharpe"] = 0
    
    logger.info(f"Strategy comparison complete. Best strategy: {comparison.get('best_strategy', 'None')}")
    
    return comparison

def optimize_rebalance_frequency(symbols: List[str] = DEFAULT_SYMBOLS,
                               start_date: str = START_DATE,
                               end_date: str = END_DATE,
                               strategy_type: str = STRATEGY_TYPE,
                               frequencies: List[str] = ["D", "W", "2W", "M"]) -> Dict[str, Any]:
    """
    Optimize rebalancing frequency for a given strategy.
    
    Args:
        symbols: List of symbols to include
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        strategy_type: Type of allocation strategy
        frequencies: List of rebalancing frequencies to test
        
    Returns:
        Dictionary with optimization results
    """
    results = {}
    
    for freq in frequencies:
        logger.info(f"Testing rebalancing frequency: {freq}")
        result = run_backtest(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            strategy_type=strategy_type,
            rebalance_freq=freq
        )
        
        results[freq] = result
    
    # Compare results
    comparison = {
        "strategy_type": strategy_type,
        "frequencies": frequencies,
        "symbols": symbols,
        "start_date": start_date,
        "end_date": end_date,
    }
    
    # Add performance metrics for each frequency
    metrics = ["total_return", "sharpe_ratio", "max_drawdown", "win_rate", "calmar_ratio"]
    for metric in metrics:
        comparison[metric] = {
            freq: results[freq].get(metric, 0) if results[freq].get("success", False) else 0
            for freq in frequencies
        }
    
    # Determine best frequency based on Sharpe ratio
    valid_frequencies = [
        freq for freq in frequencies 
        if results[freq].get("success", False) and results[freq].get("sharpe_ratio", 0) > 0
    ]
    
    if valid_frequencies:
        best_freq = max(
            valid_frequencies,
            key=lambda f: results[f].get("sharpe_ratio", 0)
        )
        comparison["best_frequency"] = best_freq
        comparison["best_sharpe"] = results[best_freq].get("sharpe_ratio", 0)
    else:
        comparison["best_frequency"] = None
        comparison["best_sharpe"] = 0
    
    logger.info(f"Rebalance frequency optimization complete. Best frequency: {comparison.get('best_frequency', 'None')}")
    
    return comparison

def plot_allocations(portfolio) -> None:
    """
    Plot portfolio allocations over time.
    
    Args:
        portfolio: Portfolio object from optimization
    """
    if portfolio is None:
        logger.error("Cannot plot allocations: Portfolio is None")
        return
    
    try:
        fig = portfolio.plot_allocations()
        fig.show()
    except Exception as e:
        logger.error(f"Error plotting allocations: {str(e)}")

def plot_performance(portfolio) -> None:
    """
    Plot portfolio performance.
    
    Args:
        portfolio: Portfolio object from optimization
    """
    if portfolio is None:
        logger.error("Cannot plot performance: Portfolio is None")
        return
    
    try:
        fig = portfolio.plot()
        fig.show()
    except Exception as e:
        logger.error(f"Error plotting performance: {str(e)}")

def save_results(results: Dict[str, Any], filename: str = None) -> bool:
    """
    Save backtest results to file.
    
    Args:
        results: Dictionary with backtest results
        filename: Optional filename
        
    Returns:
        True if successful, False otherwise
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backtest_results_{timestamp}.json"
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    file_path = output_dir / filename
    
    try:
        # Convert non-serializable objects to strings or other serializable formats
        serializable_results = {}
        for k, v in results.items():
            if k == "portfolio":
                # Skip portfolio object
                continue
            elif k == "allocations" and isinstance(v, dict):
                # Convert allocations to a format that can be serialized
                serializable_results[k] = {
                    str(date): {str(symbol): weight for symbol, weight in allocation.items()}
                    for date, allocation in v.items()
                }
            elif isinstance(v, np.ndarray):
                serializable_results[k] = v.tolist()
            elif isinstance(v, (datetime, pd.Timestamp)):
                serializable_results[k] = v.isoformat()
            elif isinstance(v, (pd.Series, pd.DataFrame)):
                # Skip pandas objects
                continue
            else:
                serializable_results[k] = v
        
        # Save to file
        import json
        with open(file_path, "w") as f:
            json.dump(serializable_results, f, indent=4)
        
        logger.info(f"Results saved to {file_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="VectorBT Portfolio Rebalancing")
    parser.add_argument("--symbols", type=str, nargs="+", default=DEFAULT_SYMBOLS,
                       help="Symbols to include in portfolio")
    parser.add_argument("--start", type=str, default=START_DATE,
                       help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", type=str, default=END_DATE,
                       help="End date in YYYY-MM-DD format")
    parser.add_argument("--strategy", type=str, default=STRATEGY_TYPE,
                       choices=["equal_weight", "max_sharpe", "min_variance"],
                       help="Portfolio allocation strategy")
    parser.add_argument("--rebalance", type=str, default=REBALANCE_FREQUENCY,
                       help="Rebalancing frequency (D, W, 2W, M, etc.)")
    parser.add_argument("--lookback", type=int, default=LOOKBACK_WINDOW,
                       help="Lookback window for optimization")
    parser.add_argument("--initial", type=float, default=INITIAL_CAPITAL,
                       help="Initial capital")
    parser.add_argument("--compare", action="store_true",
                       help="Compare different strategies")
    parser.add_argument("--optimize-freq", action="store_true",
                       help="Optimize rebalancing frequency")
    parser.add_argument("--plot", action="store_true",
                       help="Plot results")
    parser.add_argument("--save", action="store_true",
                       help="Save results to file")
    
    args = parser.parse_args()
    
    # Run comparison if requested
    if args.compare:
        comparison = compare_strategies(
            symbols=args.symbols,
            start_date=args.start,
            end_date=args.end,
            rebalance_freq=args.rebalance
        )
        
        if args.save:
            save_results(comparison, "strategy_comparison.json")
    
    # Optimize rebalancing frequency if requested
    elif args.optimize_freq:
        optimization = optimize_rebalance_frequency(
            symbols=args.symbols,
            start_date=args.start,
            end_date=args.end,
            strategy_type=args.strategy
        )
        
        if args.save:
            save_results(optimization, "frequency_optimization.json")
    
    # Otherwise run single backtest
    else:
        results = run_backtest(
            symbols=args.symbols,
            start_date=args.start,
            end_date=args.end,
            strategy_type=args.strategy,
            rebalance_freq=args.rebalance,
            lookback=args.lookback,
            init_cash=args.initial
        )
        
        if results["success"] and args.plot:
            plot_allocations(results["portfolio"])
            plot_performance(results["portfolio"])
        
        if args.save:
            save_results(results) 