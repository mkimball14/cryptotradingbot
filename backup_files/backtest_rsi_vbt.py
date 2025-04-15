import json

def optimize_rsi_strategy(data, param_grid, min_trades=5, metric='sharpe'):
    """
    Optimize RSI strategy parameters using vectorbtpro.

    Args:
        data (pd.DataFrame): OHLCV data.
        param_grid (dict): Dictionary of parameters to test (e.g., {'window': [10, 20]}).
        min_trades (int): Minimum number of trades required for a result to be considered valid.
        metric (str): Metric to optimize for (e.g., 'sharpe', 'total_return').

    Returns:
        dict: Dictionary containing best parameters, metrics, and portfolio, or None if no valid result.
    """
    logger.info(f"Optimizing parameters: {param_grid}")
    
    if not isinstance(data, pd.DataFrame) or not all(c in data.columns for c in ['open', 'high', 'low', 'close', 'volume']):
        logger.error("Optimization requires DataFrame with OHLCV columns.")
        return None

    # Extract parameter combinations
    rsi_windows = param_grid.get('window', [14])
    lower_thresholds = param_grid.get('lower_threshold', [30])
    upper_thresholds = param_grid.get('upper_threshold', [70])

    # Store all parameter combinations and their results
    all_results = []
    best_metric_value = -float('inf')  # Start with worst possible value for maximization
    best_params = None
    best_portfolio = None
    best_metrics = None

    # Loop through all parameter combinations
    logger.info(f"Testing {len(rsi_windows) * len(lower_thresholds) * len(upper_thresholds)} parameter combinations...")
    
    for window in rsi_windows:
        for lower_th in lower_thresholds:
            for upper_th in upper_thresholds:
                # Run the RSI strategy with this parameter set
                strategy = RSIMomentumVBT(
                    window=window,
                    wtype='wilder',
                    lower_threshold=lower_th,
                    upper_threshold=upper_th,
                    ma_window=20,
                    ma_type='sma',
                    initial_capital=10000.0
                )
                
                try:
                    # Run the strategy using the run_with_params method
                    result = strategy.run_with_params(data, window=window, lower_threshold=lower_th, upper_threshold=upper_th)
                    
                    # Skip if no valid portfolio
                    if not isinstance(result, dict) or 'portfolio' not in result or result['portfolio'] is None:
                        continue
                        
                    portfolio = result['portfolio']
                    
                    # Check if minimum trade count is met
                    trade_count = 0
                    try:
                        if hasattr(portfolio.trades, 'count'):
                            trade_count = portfolio.trades.count()
                        elif hasattr(portfolio.trades, 'records') and len(portfolio.trades.records) > 0:
                            trade_count = len(portfolio.trades.records)
                        else:
                            trade_count = len(portfolio.trades)
                    except:
                        continue  # Skip if cannot determine trade count
                    
                    if trade_count < min_trades:
                        continue
                    
                    # Calculate metrics
                    metrics = calculate_risk_metrics(portfolio)
                    
                    # Determine which metric to optimize
                    metric_value = metrics[metric] if metric in metrics else metrics.get('sharpe', 0)
                    
                    # Store result data for dashboard
                    result_data = {
                        'window': window,
                        'lower_threshold': lower_th,
                        'upper_threshold': upper_th,
                        'metrics': metrics,
                        'trade_count': trade_count
                    }
                    all_results.append(result_data)
                    
                    # Check if this is the best result so far
                    if metric_value > best_metric_value:
                        best_metric_value = metric_value
                        best_params = {
                            'window': window,
                            'lower_threshold': lower_th,
                            'upper_threshold': upper_th
                        }
                        best_portfolio = portfolio
                        best_metrics = metrics
                except Exception as e:
                    logger.debug(f"Error testing parameters (window={window}, lower_th={lower_th}, upper_th={upper_th}): {e}")
                    continue
    
    # Check if we found valid parameters
    if best_params is None:
        logger.warning("No valid parameter combination found.")
        return None
    
    # Get best parameters with string representations for logging
    best_window = best_params['window']
    best_lower_th = best_params['lower_threshold']
    best_upper_th = best_params['upper_threshold']
    
    logger.info(f"Optimization complete. Found {len(all_results)} valid parameter combinations.")
    logger.info(f"Best parameters: window={best_window}, lower_th={best_lower_th}, upper_th={best_upper_th}")
    
    return {
        'best_params': best_params,
        'best_metrics': best_metrics,
        'portfolio': best_portfolio,
        'all_results': all_results,  # Include all results for heatmap creation
        'price_data': data,  # Include price data for dashboard
        'rsi_indicator': strategy.run_with_params(data, window=best_window, lower_threshold=best_lower_th, upper_threshold=best_upper_th).get('rsi_indicator', None)  # Include RSI indicator for dashboard
    }

def fetch_historical_data(product_id, start_date, end_date, granularity=86400):
    """
    Fetch historical price data from Coinbase or from cache
    
    Parameters:
    -----------
    product_id : str
        The product ID (e.g., 'BTC-USD')
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    granularity : int
        Granularity in seconds (default: 86400 for daily)
        
    Returns:
    --------
    DataFrame
        Historical price data with columns: open, high, low, close, volume
    """
    # Create cache directory if it doesn't exist
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Define cache file path
    cache_file = cache_dir / f"{product_id.replace('-', '')}_{start_date}_{end_date}_{granularity}.csv"

    # Check sample data cache
    sample_cache = cache_dir / f"sample_{start_date}_{end_date}.csv"
    if sample_cache.exists():
        logger.info(f"Loading cached sample data from: {sample_cache}")
        try:
            # Read the CSV file
            raw_data = pd.read_csv(sample_cache)
            
            # Convert string JSON to dictionaries
            candles = []
            for _, row in raw_data.iterrows():
                try:
                    # Remove any single quotes and replace with double quotes for valid JSON
                    candle_str = row['candle'].replace("'", '"')
                    candle = json.loads(candle_str)
                    candles.append(candle)
                except Exception as e:
                    logger.warning(f"Error parsing candle data: {e}")
                    continue
            
            # Convert list of dictionaries to DataFrame
            if candles:
                data = pd.DataFrame(candles)
                
                # Convert timestamp to datetime index
                data['start'] = pd.to_datetime(data['start'])
                data.set_index('start', inplace=True)
                
                # Ensure all required columns exist and are numeric
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    if col in data.columns:
                        data[col] = pd.to_numeric(data[col], errors='coerce')
                    else:
                        logger.warning(f"Missing column {col} in data")
                        data[col] = np.nan
                
                logger.info(f"Successfully loaded and parsed {len(data)} candles from cache")
                return data
            else:
                raise ValueError("No valid candle data found in cache")
                
        except Exception as e:
            logger.warning(f"Error loading sample cache: {e}")
            
    # Try to load API credentials
    logger.info("Loading credentials from cdp_api_key.json...")
    if not os.path.exists("cdp_api_key.json"):
        logger.warning("Credentials file not found: cdp_api_key.json")
        logger.info("Generating sample data instead")
        return create_sample_data(start_date, end_date)

    # Generate sample data as we don't have actual API integration in this example
    logger.info("API integration not implemented - generating sample data")
    return create_sample_data(start_date, end_date)


def create_sample_data(start_date, end_date):
    """
    Create sample price data for backtesting when no real data is available.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        DataFrame with OHLCV data
    """
    logger.info(f"Creating sample BTC-USD price data for backtesting...")
    
    # Create directory for cached data if it doesn't exist
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if we have cached sample data
    cache_file = cache_dir / f"sample_{start_date}_{end_date}.csv"
    
    if cache_file.exists():
        logger.info(f"Loading cached sample data from: {cache_file}")
        try:
            data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            
            # Ensure all required columns exist
            if 'close' not in data.columns and 'Close' in data.columns:
                data['close'] = data['Close']
                data.drop('Close', axis=1, inplace=True, errors='ignore')
            
            # Check for missing OHLCV columns
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in data.columns for col in required_columns):
                logger.warning(f"Cached data missing required columns. Available columns: {data.columns}")
                logger.info("Regenerating sample data...")
                # Delete invalid cache file
                try:
                    cache_file.unlink()
                except:
                    pass
            else:
                logger.info(f"Loaded {len(data)} days of cached sample data")
                return data
        except Exception as e:
            logger.error(f"Error loading cached data: {e}")
    
    # Create date range
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    daterange = pd.date_range(start=start, end=end, freq='D')
    
    # Generate random price data with realistic properties
    np.random.seed(42)  # For reproducibility
    
    # Start with a price and add random changes
    price = 20000.0  # Starting price for BTC
    daily_volatility = 0.02  # 2% daily volatility
    
    prices = []
    for _ in range(len(daterange)):
        daily_return = np.random.normal(0.0002, daily_volatility)  # Slight upward drift
        price *= (1 + daily_return)
        prices.append(price)
    
    close_prices = pd.Series(prices, index=daterange)
    
    # Generate OHLCV data
    data = pd.DataFrame(index=daterange)
    data['close'] = close_prices
    data['high'] = data['close'] * (1 + np.random.uniform(0, 0.03, len(data)))
    data['low'] = data['close'] * (1 - np.random.uniform(0, 0.03, len(data)))
    data['open'] = data['close'].shift(1)
    
    # Handle first row
    data.loc[data.index[0], 'open'] = data.loc[data.index[0], 'close'] * 0.99
    
    # Add volume (proportional to price changes)
    price_changes = np.abs(data['close'].pct_change().fillna(0.01))
    base_volume = 1000  # Base volume in BTC
    data['volume'] = base_volume * (1 + 5 * price_changes)  # Higher volume on bigger price moves
    
    # Cache the generated data
    try:
        data.to_csv(cache_file)
        logger.info(f"Cached sample data to: {cache_file}")
    except Exception as e:
        logger.error(f"Error caching sample data: {e}")
    
    logger.info(f"Generated {len(data)} days of sample price data")
    return data 