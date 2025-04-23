import numpy as np
import pandas as pd

def create_price_rejection_indicator(
    open_prices: pd.Series,
    high_prices: pd.Series,
    low_prices: pd.Series,
    close_prices: pd.Series,
    rejection_threshold: float = 0.6,
    body_threshold: float = 0.3,
    lookback: int = 3,
    min_rejection_ratio: float = 2.0
) -> tuple:
    """
    Creates a price rejection (pin bar) indicator that identifies candles with long wicks
    relative to their bodies, indicating potential reversals.
    
    Args:
        open_prices (pd.Series): Time series of open prices
        high_prices (pd.Series): Time series of high prices
        low_prices (pd.Series): Time series of low prices
        close_prices (pd.Series): Time series of close prices
        rejection_threshold (float): Minimum wick to candle ratio to qualify as rejection
        body_threshold (float): Maximum body to candle ratio for rejection confirmation
        lookback (int): Lookback period to identify local extremes
        min_rejection_ratio (float): Minimum ratio of rejection size to average candle size
        
    Returns:
        tuple: (
            bullish_rejection (pd.Series): Boolean series indicating bullish rejection patterns,
            bearish_rejection (pd.Series): Boolean series indicating bearish rejection patterns,
            upper_wick_ratio (pd.Series): Ratio of upper wick to total candle height,
            lower_wick_ratio (pd.Series): Ratio of lower wick to total candle height,
            body_ratio (pd.Series): Ratio of body to total candle height
        )
    """
    # Calculate candle body and wicks
    body_size = (close_prices - open_prices).abs()
    candle_high = pd.concat([open_prices, close_prices], axis=1).max(axis=1)
    candle_low = pd.concat([open_prices, close_prices], axis=1).min(axis=1)
    upper_wick = high_prices - candle_high
    lower_wick = candle_low - low_prices
    
    # Calculate total candle height
    total_candle_height = high_prices - low_prices
    
    # Handle potential division by zero
    total_candle_height = total_candle_height.replace(0, np.nan)
    
    # Calculate wick and body ratios
    upper_wick_ratio = upper_wick / total_candle_height
    lower_wick_ratio = lower_wick / total_candle_height
    body_ratio = body_size / total_candle_height
    
    # Calculate average candle size for recent periods
    avg_candle_size = total_candle_height.rolling(window=lookback).mean()
    
    # Initialize rejection signals
    bullish_rejection = pd.Series(False, index=close_prices.index)
    bearish_rejection = pd.Series(False, index=close_prices.index)
    
    # Calculate local high and local low
    local_high = high_prices.rolling(window=lookback).max()
    local_low = low_prices.rolling(window=lookback).min()
    
    # Identify bullish rejection (long lower wick) - potential reversal from downtrend
    bullish_conditions = (
        (lower_wick_ratio > rejection_threshold) &  # Long lower wick
        (body_ratio < body_threshold) &             # Small body
        (lower_wick > (min_rejection_ratio * avg_candle_size)) &  # Significant size
        (low_prices <= local_low.shift(1))          # At or near local low
    )
    bullish_rejection = bullish_conditions
    
    # Identify bearish rejection (long upper wick) - potential reversal from uptrend
    bearish_conditions = (
        (upper_wick_ratio > rejection_threshold) &  # Long upper wick
        (body_ratio < body_threshold) &             # Small body
        (upper_wick > (min_rejection_ratio * avg_candle_size)) &  # Significant size
        (high_prices >= local_high.shift(1))        # At or near local high
    )
    bearish_rejection = bearish_conditions
    
    # Handle NaN values
    bullish_rejection = bullish_rejection.fillna(False)
    bearish_rejection = bearish_rejection.fillna(False)
    
    return bullish_rejection, bearish_rejection, upper_wick_ratio, lower_wick_ratio, body_ratio


def create_engulfing_pattern_indicator(
    open_prices: pd.Series,
    close_prices: pd.Series,
    body_size_threshold: float = 0.6,
    engulf_factor: float = 1.2
) -> tuple:
    """
    Creates an engulfing pattern indicator that identifies bullish and bearish engulfing patterns.
    
    Args:
        open_prices (pd.Series): Time series of open prices
        close_prices (pd.Series): Time series of close prices
        body_size_threshold (float): Minimum ratio of body to average body size
        engulf_factor (float): How much larger the engulfing candle must be
        
    Returns:
        tuple: (
            bullish_engulfing (pd.Series): Boolean series indicating bullish engulfing patterns,
            bearish_engulfing (pd.Series): Boolean series indicating bearish engulfing patterns,
            engulfing_strength (pd.Series): Numeric strength of the engulfing pattern
        )
    """
    # Calculate bullish and bearish candles
    bullish_candle = close_prices > open_prices
    bearish_candle = close_prices < open_prices
    
    # Calculate candle body sizes
    body_size = (close_prices - open_prices).abs()
    avg_body_size = body_size.rolling(window=10).mean()
    
    # Large body condition
    large_body = body_size > (body_size_threshold * avg_body_size)
    
    # Calculate engulfing conditions
    bullish_engulfing = (
        bearish_candle.shift(1) &               # Previous candle was bearish
        bullish_candle &                         # Current candle is bullish
        (open_prices < close_prices.shift(1)) &  # Open below previous close
        (close_prices > open_prices.shift(1)) &  # Close above previous open
        (body_size > (engulf_factor * body_size.shift(1))) &  # Larger body than previous
        large_body                               # Significant body size
    )
    
    bearish_engulfing = (
        bullish_candle.shift(1) &               # Previous candle was bullish
        bearish_candle &                         # Current candle is bearish
        (open_prices > close_prices.shift(1)) &  # Open above previous close
        (close_prices < open_prices.shift(1)) &  # Close below previous open
        (body_size > (engulf_factor * body_size.shift(1))) &  # Larger body than previous
        large_body                               # Significant body size
    )
    
    # Calculate engulfing strength as a ratio of body sizes
    engulfing_strength = body_size / body_size.shift(1)
    engulfing_strength = engulfing_strength.where(bullish_engulfing | bearish_engulfing, 0)
    
    # Handle NaN values
    bullish_engulfing = bullish_engulfing.fillna(False)
    bearish_engulfing = bearish_engulfing.fillna(False)
    
    return bullish_engulfing, bearish_engulfing, engulfing_strength


def create_inside_bar_indicator(
    high_prices: pd.Series,
    low_prices: pd.Series,
    open_prices: pd.Series = None,
    close_prices: pd.Series = None,
    min_size_ratio: float = 0.4,
    lookback: int = 3
) -> tuple:
    """
    Creates an inside bar indicator that identifies when a price bar is contained
    within the range of the previous bar, often signaling consolidation before a move.
    
    Args:
        high_prices (pd.Series): Time series of high prices
        low_prices (pd.Series): Time series of low prices
        open_prices (pd.Series, optional): Time series of open prices
        close_prices (pd.Series, optional): Time series of close prices
        min_size_ratio (float): Minimum size ratio of inside bar to mother bar
        lookback (int): Lookback period to identify significant inside bars
        
    Returns:
        tuple: (
            inside_bar (pd.Series): Boolean series indicating inside bar patterns,
            inside_strength (pd.Series): Numeric strength of the inside bar pattern,
            direction_bias (pd.Series): Directional bias of the inside bar (-1=bearish, 0=neutral, 1=bullish)
        )
    """
    # Calculate basic inside bar condition
    inside_bar = (
        (high_prices < high_prices.shift(1)) &  # Current high below previous high
        (low_prices > low_prices.shift(1))      # Current low above previous low
    )
    
    # Calculate bar ranges
    current_range = high_prices - low_prices
    previous_range = high_prices.shift(1) - low_prices.shift(1)
    avg_range = current_range.rolling(window=lookback).mean()
    
    # Calculate inside bar strength based on relative size
    inside_ratio = current_range / previous_range
    significant_size = current_range > (min_size_ratio * avg_range)
    
    # Combine conditions - inside bar must be significant relative to average
    inside_bar = inside_bar & significant_size
    
    # Calculate inside bar strength (lower ratio = stronger pattern)
    inside_strength = 1 - inside_ratio
    inside_strength = inside_strength.where(inside_bar, 0)
    
    # Determine directional bias if open/close prices are available
    direction_bias = pd.Series(0, index=high_prices.index)
    
    if open_prices is not None and close_prices is not None:
        # Calculate candle direction for mother bar
        mother_bullish = close_prices.shift(1) > open_prices.shift(1)
        mother_bearish = close_prices.shift(1) < open_prices.shift(1)
        
        # Calculate position of inside bar close relative to mother bar
        relative_close_position = (close_prices - low_prices.shift(1)) / (high_prices.shift(1) - low_prices.shift(1))
        
        # Assign directional bias
        # If mother bar is bullish and inside bar closes in upper half = bullish bias
        bullish_bias = inside_bar & mother_bullish & (relative_close_position > 0.5)
        # If mother bar is bearish and inside bar closes in lower half = bearish bias
        bearish_bias = inside_bar & mother_bearish & (relative_close_position < 0.5)
        
        direction_bias = pd.Series(0, index=high_prices.index)
        direction_bias = direction_bias.mask(bullish_bias, 1)
        direction_bias = direction_bias.mask(bearish_bias, -1)
    
    # Handle NaN values
    inside_bar = inside_bar.fillna(False)
    inside_strength = inside_strength.fillna(0)
    direction_bias = direction_bias.fillna(0)
    
    return inside_bar, inside_strength, direction_bias


def create_outside_bar_indicator(
    high_prices: pd.Series,
    low_prices: pd.Series,
    open_prices: pd.Series = None,
    close_prices: pd.Series = None,
    min_size_ratio: float = 1.2,
    lookback: int = 5
) -> tuple:
    """
    Creates an outside bar indicator that identifies when a price bar completely engulfs
    the previous bar's range, often signaling a potential reversal or strong continuation.
    
    Args:
        high_prices (pd.Series): Time series of high prices
        low_prices (pd.Series): Time series of low prices
        open_prices (pd.Series, optional): Time series of open prices
        close_prices (pd.Series, optional): Time series of close prices
        min_size_ratio (float): Minimum size ratio of outside bar to previous bar
        lookback (int): Lookback period for significance evaluation
        
    Returns:
        tuple: (
            outside_bar (pd.Series): Boolean series indicating outside bar patterns,
            outside_strength (pd.Series): Numeric strength of the outside bar pattern,
            direction (pd.Series): Direction of the outside bar (-1=bearish, 0=neutral, 1=bullish)
        )
    """
    # Calculate basic outside bar condition
    outside_bar = (
        (high_prices > high_prices.shift(1)) &  # Current high above previous high
        (low_prices < low_prices.shift(1))      # Current low below previous low
    )
    
    # Calculate bar ranges
    current_range = high_prices - low_prices
    previous_range = high_prices.shift(1) - low_prices.shift(1)
    avg_range = current_range.rolling(window=lookback).mean()
    
    # Calculate size ratio - outside bar should be larger than previous
    size_ratio = current_range / previous_range
    significant_size = size_ratio > min_size_ratio
    
    # Significant outside bar must be larger than previous and significant vs average
    outside_bar = outside_bar & significant_size & (current_range > avg_range)
    
    # Calculate outside bar strength based on size ratio
    outside_strength = size_ratio - 1
    outside_strength = outside_strength.where(outside_bar, 0)
    
    # Determine directional bias if open/close prices are available
    direction = pd.Series(0, index=high_prices.index)
    
    if open_prices is not None and close_prices is not None:
        # Based on open-close relationship
        bullish_outside = outside_bar & (close_prices > open_prices) & (close_prices > close_prices.shift(1))
        bearish_outside = outside_bar & (close_prices < open_prices) & (close_prices < close_prices.shift(1))
        
        direction = pd.Series(0, index=high_prices.index)
        direction = direction.mask(bullish_outside, 1)
        direction = direction.mask(bearish_outside, -1)
    
    # Handle NaN values
    outside_bar = outside_bar.fillna(False)
    outside_strength = outside_strength.fillna(0)
    direction = direction.fillna(0)
    
    return outside_bar, outside_strength, direction


def create_swing_high_low_indicator(
    price: pd.Series,
    window: int = 5,
    min_strength: float = 0.5
) -> tuple:
    """
    Creates swing high and low indicators to identify potential reversal points.
    
    Args:
        price (pd.Series): Time series of price data
        window (int): Window size to look for swing highs/lows
        min_strength (float): Minimum strength threshold for valid swing points
        
    Returns:
        tuple: (
            swing_high (pd.Series): Boolean series indicating swing high points,
            swing_low (pd.Series): Boolean series indicating swing low points,
            swing_strength (pd.Series): Numeric strength values for the swing points
        )
    """
    # Initialize results
    swing_high = pd.Series(False, index=price.index)
    swing_low = pd.Series(False, index=price.index)
    swing_strength = pd.Series(0.0, index=price.index)
    
    # Calculate rolling max and min for the left and right windows
    left_max = price.rolling(window=window).max().shift(1)
    right_max = price.rolling(window=window).max().shift(-window+1)
    
    left_min = price.rolling(window=window).min().shift(1)
    right_min = price.rolling(window=window).min().shift(-window+1)
    
    # Calculate average price movement for normalization
    avg_movement = price.diff().abs().rolling(window=window*2).mean()
    
    # Identify swing highs
    is_local_max = (price > left_max) & (price > right_max)
    
    # Identify swing lows
    is_local_min = (price < left_min) & (price < right_min)
    
    # Calculate swing point strength (how much it stands out)
    for i in range(window, len(price)-window):
        if is_local_max.iloc[i]:
            # Calculate how much higher this point is compared to surrounding points
            left_diff = price.iloc[i] - price.iloc[i-window:i].max()
            right_diff = price.iloc[i] - price.iloc[i+1:i+window+1].max()
            strength = (left_diff + right_diff) / (2 * avg_movement.iloc[i])
            
            if strength >= min_strength:
                swing_high.iloc[i] = True
                swing_strength.iloc[i] = strength
                
        elif is_local_min.iloc[i]:
            # Calculate how much lower this point is compared to surrounding points
            left_diff = price.iloc[i-window:i].min() - price.iloc[i]
            right_diff = price.iloc[i+1:i+window+1].min() - price.iloc[i]
            strength = (left_diff + right_diff) / (2 * avg_movement.iloc[i])
            
            if strength >= min_strength:
                swing_low.iloc[i] = True
                swing_strength.iloc[i] = strength
    
    return swing_high, swing_low, swing_strength


def create_key_price_level_indicator(
    price: pd.Series,
    volume: pd.Series = None,
    window: int = 50,
    num_levels: int = 3,
    level_threshold: float = 0.2,
    use_volume: bool = True
) -> tuple:
    """
    Creates an indicator that identifies key price levels based on historical 
    price action and optional volume.
    
    Args:
        price (pd.Series): Time series of price data
        volume (pd.Series, optional): Time series of volume data
        window (int): Window size to analyze for key levels
        num_levels (int): Number of key price levels to identify
        level_threshold (float): Minimum threshold for key level significance
        use_volume (bool): Whether to use volume data in level identification
        
    Returns:
        tuple: (
            key_levels (pd.Series): Series containing primary key level for each period,
            level_strength (pd.Series): Strength value for primary key level,
            price_distance (pd.Series): Distance from current price to nearest key level
        )
    """
    if use_volume and volume is None:
        use_volume = False  # Fallback if volume data is missing
    
    # Create empty series for results
    key_levels = pd.Series(np.nan, index=price.index)
    level_strength = pd.Series(np.nan, index=price.index)
    price_distance = pd.Series(np.nan, index=price.index)
    
    # Process in rolling windows
    for i in range(window, len(price)):
        # Get window of historical data
        window_price = price.iloc[i-window:i]
        
        # Create price bins
        bins = np.linspace(window_price.min(), window_price.max(), 20)
        
        # Count price occurrences in each bin
        if use_volume:
            window_volume = volume.iloc[i-window:i]
            # Weight by volume
            weighted_counts, _ = np.histogram(window_price, bins=bins, weights=window_volume)
        else:
            # Simple count
            counts, _ = np.histogram(window_price, bins=bins)
            weighted_counts = counts
        
        # Normalize counts
        norm_counts = weighted_counts / weighted_counts.sum()
        
        # Find bins with high concentration (possible key levels)
        threshold = np.mean(norm_counts) + (np.std(norm_counts) * level_threshold)
        significant_bins = np.where(norm_counts > threshold)[0]
        
        # Get center of each significant bin
        bin_centers = [(bins[j] + bins[j+1])/2 for j in significant_bins]
        
        # Sort by bin count (highest first)
        sorted_levels = sorted(zip(bin_centers, norm_counts[significant_bins]), 
                               key=lambda x: x[1], reverse=True)
        
        # Get top N levels
        top_levels = sorted_levels[:num_levels] if len(sorted_levels) >= num_levels else sorted_levels
        
        if top_levels:
            # Store only the primary level (strongest) in the key_levels Series
            primary_level, primary_strength = top_levels[0]
            
            # Find the closest level to current price
            current_price = price.iloc[i]
            closest_level = min([level for level, _ in top_levels], key=lambda x: abs(x - current_price))
            distance = abs(closest_level - current_price) / current_price  # Normalized distance
            
            # Store results - now storing only scalar values
            key_levels.iloc[i] = primary_level
            level_strength.iloc[i] = primary_strength
            price_distance.iloc[i] = distance
    
    return key_levels, level_strength, price_distance


def create_support_resistance_indicator(
    price: pd.Series,
    window: int = 50,
    threshold: float = 0.02,
    min_touches: int = 3
) -> tuple:
    """
    Creates dynamic support and resistance indicators based on price action.
    
    Args:
        price (pd.Series): Time series of price data
        window (int): Window size to analyze
        threshold (float): Price threshold for considering levels (% of price)
        min_touches (int): Minimum number of touches required for valid S/R level
        
    Returns:
        tuple: (
            nearest_support (pd.Series): Nearest support level to current price,
            nearest_resistance (pd.Series): Nearest resistance level to current price,
            support_count (pd.Series): Number of valid support levels identified for each period,
            resistance_count (pd.Series): Number of valid resistance levels identified for each period
        )
    """
    # Initialize result series with NaN values for numeric data
    nearest_support = pd.Series(np.nan, index=price.index)
    nearest_resistance = pd.Series(np.nan, index=price.index)
    support_count = pd.Series(0, index=price.index)
    resistance_count = pd.Series(0, index=price.index)
    
    # Process data in rolling windows
    for i in range(window, len(price)):
        window_data = price.iloc[i-window:i]
        current_price = price.iloc[i]
        
        # Find swing lows as potential support
        # Get swing lows in the window
        swings = pd.Series(window_data)
        lows = []
        
        for j in range(1, len(swings)-1):
            if swings.iloc[j] < swings.iloc[j-1] and swings.iloc[j] < swings.iloc[j+1]:
                lows.append(swings.iloc[j])
        
        # Find swing highs as potential resistance
        highs = []
        for j in range(1, len(swings)-1):
            if swings.iloc[j] > swings.iloc[j-1] and swings.iloc[j] > swings.iloc[j+1]:
                highs.append(swings.iloc[j])
        
        # Cluster similar levels
        level_threshold = current_price * threshold
        
        # Cluster supports
        support_clusters = []
        for low in lows:
            found_cluster = False
            for cluster in support_clusters:
                if abs(cluster[0] - low) < level_threshold:
                    cluster.append(low)
                    found_cluster = True
                    break
            if not found_cluster:
                support_clusters.append([low])
        
        # Cluster resistances
        resistance_clusters = []
        for high in highs:
            found_cluster = False
            for cluster in resistance_clusters:
                if abs(cluster[0] - high) < level_threshold:
                    cluster.append(high)
                    found_cluster = True
                    break
            if not found_cluster:
                resistance_clusters.append([high])
        
        # Filter by minimum touches
        valid_supports = [np.mean(cluster) for cluster in support_clusters if len(cluster) >= min_touches]
        valid_resistances = [np.mean(cluster) for cluster in resistance_clusters if len(cluster) >= min_touches]
        
        # Store count of valid levels (scalar values)
        support_count.iloc[i] = len(valid_supports)
        resistance_count.iloc[i] = len(valid_resistances)
        
        # Find nearest support and resistance
        if valid_supports:
            # Only consider supports below current price
            valid_supports = [s for s in valid_supports if s < current_price]
            if valid_supports:
                nearest_support.iloc[i] = max(valid_supports)  # Highest support below price
        
        if valid_resistances:
            # Only consider resistances above current price
            valid_resistances = [r for r in valid_resistances if r > current_price]
            if valid_resistances:
                nearest_resistance.iloc[i] = min(valid_resistances)  # Lowest resistance above price
    
    return nearest_support, nearest_resistance, support_count, resistance_count 