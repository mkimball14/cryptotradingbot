import vectorbtpro as vbt
import pandas as pd
import numpy as np
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def run_factor_backtest(close_prices, target_weights, init_cash=100000, fees=0.001, slippage=0.0005, freq='D'):
    """Runs a backtest using target weights with a simplified custom implementation.
    
    Args:
        close_prices (pd.DataFrame): Multi-index DataFrame with ['date', 'symbol'] index and close prices.
        target_weights (pd.Series): Multi-index Series with ['date', 'symbol'] index and target portfolio weights.
        init_cash (float): Initial cash amount for the simulation. Default 100,000.
        fees (float): Trading fee rate (e.g., 0.001 = 0.1%). Default 0.1%.
        slippage (float): Estimated slippage rate (e.g., 0.0005 = 0.05%). Default 0.05%.
        freq (str): Frequency string for the time series (e.g., 'D' for daily). Default 'D'.
    
    Returns:
        object: Custom Portfolio object with backtest results or None if failed.
    """
    # --- Critical: Data Alignment ---
    try:
        logger.info(f"Aligning price and weight data for backtest...")
        
        # 1. Unstack to create date index and symbol columns (easier to inspect)
        if isinstance(target_weights, pd.Series):
            weights_unstacked = target_weights.unstack('symbol')
        else:
            # Handle case where weights might already be unstacked
            weights_unstacked = target_weights
            
        if isinstance(close_prices, pd.Series):
            close_unstacked = close_prices.unstack('symbol')
        else:
            # Handle case where close might already be unstacked or have columns
            close_unstacked = close_prices
            
        # 2. Find common dates and symbols
        common_index = weights_unstacked.index.intersection(close_unstacked.index)
        common_symbols = weights_unstacked.columns.intersection(close_unstacked.columns)

        if len(common_index) == 0:
            logger.error("No common dates found between weights and prices.")
            return None
            
        if len(common_symbols) == 0:
            logger.error("No common symbols found between weights and prices.")
            return None
            
        # 3. Align and fill missing values appropriately
        weights_aligned = weights_unstacked.loc[common_index, common_symbols].fillna(0.0)
        close_aligned = close_unstacked.loc[common_index, common_symbols]
        
        # 4. Check for NaNs in price data and remove affected columns if needed
        na_cols = close_aligned.columns[close_aligned.isna().any()]
        if len(na_cols) > 0:
            logger.warning(f"Removing {len(na_cols)} assets with NaN prices: {na_cols.tolist()}")
            close_aligned = close_aligned.drop(columns=na_cols)
            weights_aligned = weights_aligned.drop(columns=na_cols)
            common_symbols = [col for col in common_symbols if col not in na_cols]

        # 5. Final data validation
        if weights_aligned.empty or close_aligned.empty:
            logger.error("Data alignment resulted in empty DataFrames.")
            return None
            
        if len(common_symbols) == 0:
            logger.error("No valid symbols remain after alignment and NaN removal.")
            return None
            
        # Get all dates for backtest period
        dates = sorted(common_index)
        symbols = common_symbols
        
        logger.info(f"Running backtest on {len(dates)} dates and {len(symbols)} symbols.")
        logger.info(f"Backtest period: {dates[0]} to {dates[-1]}")
        logger.info(f"Rebalancing frequency: {freq}")
        logger.info(f"Fee rate: {fees*100:.2f}%, Slippage rate: {slippage*100:.2f}%")
    
        # --- Run simple portfolio simulation ---
        try:
            # Initialize portfolio
            portfolio_value = init_cash
            cash = init_cash
            holdings = {symbol: 0 for symbol in symbols}
            
            # Initialize returns array to match dates
            equity_curve = [portfolio_value]  # Initial value
            returns = []  # Empty initially - we'll calculate later
            
            # Calculate 1-day returns for benchmark calculation
            price_returns = close_aligned.pct_change().fillna(0)
            
            # Loop through each date
            prev_date = None
            for date_idx, date in enumerate(dates):
                if date_idx == 0:
                    # First day - just record initial values
                    # equity_curve[0] is already set
                    prev_date = date
                    continue
                
                # Get current prices and target weights
                current_prices = close_aligned.loc[date]
                target_weights_today = weights_aligned.loc[date]
                
                # Calculate current value of holdings
                holdings_value = sum(holdings[symbol] * current_prices[symbol] for symbol in symbols)
                
                # New portfolio value = cash + holdings
                portfolio_value = cash + holdings_value
                
                # Record portfolio value
                equity_curve.append(portfolio_value)
                
                # Calculate daily return
                daily_return = (portfolio_value / equity_curve[-2]) - 1
                returns.append(daily_return)
                
                # Rebalance portfolio based on target weights
                for symbol in symbols:
                    target_value = portfolio_value * target_weights_today[symbol]
                    current_value = holdings[symbol] * current_prices[symbol]
                    
                    # Calculate trade amount (positive for buy, negative for sell)
                    trade_value = target_value - current_value
                    
                    # Skip small trades
                    if abs(trade_value) < 1.0:
                        continue
                    
                    # Calculate number of shares to trade
                    trade_shares = trade_value / current_prices[symbol]
                    
                    # Apply slippage (reduces shares bought or increases shares sold)
                    if trade_shares > 0:
                        trade_shares *= (1 - slippage)
                    else:
                        trade_shares *= (1 + slippage)
                    
                    # Calculate trading fees
                    fee_amount = abs(trade_value) * fees
                    
                    # Update holdings and cash
                    holdings[symbol] += trade_shares
                    cash -= (trade_value + fee_amount)
                
                prev_date = date
            
            # Create results object with equity curve and key metrics
            results = {
                'equity_curve': pd.Series(equity_curve, index=dates),
                'returns': pd.Series(returns, index=dates[1:]),  # Returns start from second day
                'final_value': portfolio_value,
                'profit_loss': portfolio_value - init_cash,
                'total_return_pct': (portfolio_value / init_cash - 1) * 100,
                'benchmark_returns': price_returns,
                'symbols': symbols,
                'dates': dates,
                'weights': weights_aligned,
                'prices': close_aligned
            }
            
            # Calculate additional metrics
            if len(returns) > 0:
                annual_factor = {'D': 252, 'H': 252 * 24, 'W': 52, 'M': 12}.get(freq, 252)
                
                # Basic metrics
                results['volatility'] = np.std(returns) * np.sqrt(annual_factor) * 100
                results['sharpe_ratio'] = (np.mean(returns) * annual_factor) / (np.std(returns) * np.sqrt(annual_factor)) if np.std(returns) > 0 else 0
                
                # Maximum drawdown calculation
                equity_array = np.array(equity_curve)
                max_drawdown = 0
                peak = equity_array[0]
                
                for value in equity_array:
                    if value > peak:
                        peak = value
                    drawdown = (peak - value) / peak
                    max_drawdown = max(max_drawdown, drawdown)
                
                results['max_drawdown_pct'] = max_drawdown * 100
            
            # Create a simple wrapper object
            class SimplePortfolio:
                def __init__(self, results_dict):
                    self.results = results_dict
                    self.equity = results_dict['equity_curve']
                    self.returns = results_dict['returns']
                    
                def stats(self):
                    return {
                        'Total Return [%]': self.results['total_return_pct'],
                        'Annual Return [%]': np.mean(self.returns) * 252 * 100 if len(self.returns) > 0 else 0,
                        'Annual Volatility [%]': self.results.get('volatility', 0),
                        'Sharpe Ratio': self.results.get('sharpe_ratio', 0),
                        'Max Drawdown [%]': self.results.get('max_drawdown_pct', 0),
                        'Win Rate [%]': (self.returns > 0).mean() * 100 if len(self.returns) > 0 else 0
                    }
                    
                def plot(self, **kwargs):
                    try:
                        # Add the needed imports
                        import matplotlib.pyplot as plt
                        from matplotlib.figure import Figure
                        import matplotlib.dates as mdates
                        import io
                        
                        # Create the figure
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.plot(self.equity.index, self.equity.values)
                        ax.set_title('Portfolio Equity Curve')
                        ax.set_xlabel('Date')
                        ax.set_ylabel('Value ($)')
                        ax.grid(True)
                        
                        # Format x-axis as dates
                        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                        plt.xticks(rotation=45)
                        
                        plt.tight_layout()
                        
                        # Add a write_image method that is compatible with VectorBT's API
                        def write_image(path):
                            plt.savefig(path, bbox_inches='tight')
                            logger.info(f"Saved plot to {path}")
                            
                        # Attach the method to the figure
                        fig.write_image = write_image
                        
                        return fig
                    except Exception as e:
                        logger.error(f"Error plotting: {e}")
                        import traceback
                        logger.error(traceback.format_exc())
                        return None
            
            portfolio = SimplePortfolio(results)
            logger.info("Custom backtest completed successfully.")
            return portfolio
            
        except Exception as e:
            logger.error(f"Error running custom backtest: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
            
    except Exception as e:
        logger.error(f"Error during data preparation for backtest: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None


# --- Basic Analysis Functions ---

def analyze_portfolio_performance(portfolio, benchmark_returns=None):
    """Calculates and prints key performance metrics from a VectorBT portfolio.
    
    Args:
        portfolio (vbt.Portfolio): VectorBT portfolio object from a backtest.
        benchmark_returns (pd.Series, optional): Daily returns of a benchmark like BTC-USD.
            Should have the same index as portfolio.returns.
    
    Returns:
        dict: Dictionary of key metrics.
    """
    if portfolio is None:
        logger.error("Cannot analyze portfolio - portfolio object is None")
        return None
        
    try:
        # Calculate basic metrics
        stats = portfolio.stats()
        
        # Create dictionary of selected metrics
        results = {
            'Total Return (%)': stats.get('Total Return [%]', 'N/A'),
            'CAGR (%)': stats.get('Annual Return [%]', 'N/A'),
            'Sharpe Ratio': stats.get('Sharpe Ratio', 'N/A'),
            'Sortino Ratio': stats.get('Sortino Ratio', 'N/A'),
            'Max Drawdown (%)': stats.get('Max Drawdown [%]', 'N/A'),
            'Win Rate (%)': stats.get('Win Rate [%]', 'N/A'),
            'Avg Win/Loss Ratio': stats.get('Avg Win/Loss Ratio', 'N/A'),
            'Avg Turnover (%)': stats.get('Avg Turnover [%]', 'N/A'),
            'Total Trades': stats.get('Total Trades', 'N/A')
        }
        
        # Add benchmark comparison if provided
        if benchmark_returns is not None:
            # Add benchmark returns to the portfolio for comparison
            portfolio.benchmark_returns = benchmark_returns.loc[portfolio.returns.index]
            
            # Update stats to include benchmark comparison
            stats_with_benchmark = portfolio.stats()
            
            # Add benchmark metrics
            results.update({
                'Alpha': stats_with_benchmark.get('Alpha', 'N/A'),
                'Beta': stats_with_benchmark.get('Beta', 'N/A'),
                'Correlation': stats_with_benchmark.get('Correlation', 'N/A'),
                'Information Ratio': stats_with_benchmark.get('Information Ratio', 'N/A')
            })
        
        # Print key metrics for console output
        print("\n--- Portfolio Performance Summary ---")
        for metric, value in results.items():
            print(f"{metric}: {value}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error calculating portfolio metrics: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None


# --- Example Usage --- (Commented out, to be run from main.py)
# if __name__ == '__main__':
#     # This would require data and weights to be already calculated
#     # For testing with dummy data
#     dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
#     symbols = ['BTC-USD', 'ETH-USD']
#     
#     # Fake price data
#     close_data = np.array([
#         [40000, 2000],  # Day 1
#         [41000, 2050],  # Day 2
#         [42000, 2100],  # Day 3
#         [40000, 2000],  # Day 4
#         [41000, 2050],  # Day 5
#         [43000, 2200],  # Day 6
#         [44000, 2300],  # Day 7
#         [45000, 2350],  # Day 8
#         [44000, 2300],  # Day 9 
#         [46000, 2400],  # Day 10
#     ])
#     close_df = pd.DataFrame(close_data, index=dates, columns=symbols)
#     
#     # Fake weight data (alternate between BTC and ETH)
#     weights_data = np.array([
#         [1.0, 0.0],  # Day 1 - 100% BTC
#         [1.0, 0.0],  # Day 2 - 100% BTC
#         [0.0, 1.0],  # Day 3 - 100% ETH
#         [0.0, 1.0],  # Day 4 - 100% ETH
#         [1.0, 0.0],  # Day 5 - 100% BTC
#         [1.0, 0.0],  # Day 6 - 100% BTC
#         [0.0, 1.0],  # Day 7 - 100% ETH
#         [0.0, 1.0],  # Day 8 - 100% ETH
#         [1.0, 0.0],  # Day 9 - 100% BTC
#         [1.0, 0.0],  # Day 10 - 100% BTC
#     ])
#     weights_df = pd.DataFrame(weights_data, index=dates, columns=symbols)
#     
#     # Run backtest
#     portfolio = run_factor_backtest(
#         close_prices=close_df,
#         target_weights=weights_df,
#         init_cash=100000,
#         fees=0.001,
#         slippage=0.0005,
#         freq='D'
#     )
#     
#     # Analyze performance
#     if portfolio:
#         analyze_portfolio_performance(portfolio)
#         
#         # Plot equity curve
#         try:
#             print("\nGenerating equity curve plot (will save to file if not in interactive mode)...")
#             fig = portfolio.plot()
#             # fig.write_image("equity_curve.png") # Save to file if needed
#         except Exception as e:
#             print(f"Error generating plot: {e}") 