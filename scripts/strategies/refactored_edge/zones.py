# scripts/strategies/refactored_edge/zones.py

import pandas as pd
import numpy as np
import vectorbtpro as vbt
from scipy.signal import find_peaks # Added import

def find_pivot_zones(
    close: pd.Series,
    high: pd.Series, # Add high/low for zone price boundaries
    low: pd.Series,
    pivot_lookback: int,
    pivot_prominence: float,
    zone_merge_proximity: float,
    min_zone_width_candles: int,
    min_zone_strength: int,
    zone_extend_candles: int
) -> pd.DataFrame:
    """
    Identifies potential Supply (Resistance) and Demand (Support) zones
    based on pivot highs and lows using scipy.signal.find_peaks.

    Args:
        close (pd.Series): Closing prices.
        high (pd.Series): High prices.
        low (pd.Series): Low prices.
        pivot_lookback (int): Minimum distance between pivots.
        pivot_prominence (float): Required prominence of pivots relative to price range.
        zone_merge_proximity (float): Price proximity pct to merge pivots into a zone.
        min_zone_width_candles (int): Minimum candle width for a valid zone.
        min_zone_strength (int): Minimum pivots required for a valid zone.
        zone_extend_candles (int): How many candles a zone remains valid after its last pivot.

    Returns:
        pd.DataFrame: DataFrame containing zone information:
            - 'zone_type': 'supply' or 'demand'
            - 'start_idx': Index timestamp of the zone start
            - 'end_idx': Index timestamp of the zone end (potentially extended)
            - 'first_pivot_idx': Timestamp of the first pivot forming the zone
            - 'last_pivot_idx': Timestamp of the last pivot forming the zone
            - 'low_price': Lowest price within the zone pivots (low for demand, high for supply)
            - 'high_price': Highest price within the zone pivots (low for demand, high for supply)
            - 'strength': Number of pivots forming the zone
            - 'candles': Number of candles between first and last pivot
    """
    zones_data = []
    price_range = high.max() - low.min()
    if price_range == 0: # Avoid division by zero if price is flat
        prominence_threshold = 0
    else:
        prominence_threshold = price_range * pivot_prominence

    # 1. Identify Pivot Highs (for Supply Zones)
    supply_pivots_idx, supply_props = find_peaks(
        high, distance=pivot_lookback, prominence=prominence_threshold
    )
    # print(f"DEBUG: Raw supply pivots indices: {supply_pivots_idx}") # DEBUG

    # 2. Identify Pivot Lows (for Demand Zones)
    # Invert price to find lows as peaks
    demand_pivots_idx, demand_props = find_peaks(
        -low, distance=pivot_lookback, prominence=prominence_threshold
    )
    # print(f"DEBUG: Raw demand pivots indices: {demand_pivots_idx}") # DEBUG

    # 3. Group Pivots into Zones
    def group_pivots(pivot_indices, prices, zone_type):
        if pivot_indices.size == 0:
            return []

        # Create DataFrame with pivot info including original high/low for zone boundary calc
        pivot_df = pd.DataFrame({
            'idx_loc': pivot_indices,
            'timestamp': prices.index[pivot_indices],
            'price': prices.iloc[pivot_indices].values,
            'candle_high': high.iloc[pivot_indices].values, # Get original high
            'candle_low': low.iloc[pivot_indices].values   # Get original low
        })

        grouped_zones_list = []
        current_zone_pivots_df = pd.DataFrame()

        for i, pivot in pivot_df.iterrows():
            if current_zone_pivots_df.empty:
                current_zone_pivots_df = pd.concat([current_zone_pivots_df, pivot.to_frame().T])
                # print(f"DEBUG group_pivots ({zone_type}): Started zone with pivot {i} @ {pivot['timestamp']}") # DEBUG
                continue

            # Get the last pivot in the current zone
            last_pivot_in_zone = current_zone_pivots_df.iloc[-1]
            last_pivot_price = last_pivot_in_zone['price']

            # Calculate proximity threshold based on the last pivot's price
            proximity_threshold_abs = last_pivot_price * zone_merge_proximity

            # Check if the new pivot's price is close to the last pivot's price
            is_close = abs(pivot['price'] - last_pivot_price) <= proximity_threshold_abs

            if is_close:
                current_zone_pivots_df = pd.concat([current_zone_pivots_df, pivot.to_frame().T])
                # print(f"DEBUG group_pivots ({zone_type}): Added pivot {i} @ {pivot['timestamp']} to zone. Size: {len(current_zone_pivots_df)}") # DEBUG
            else:
                # Finalize the previous zone if it's valid (enough strength)
                if not current_zone_pivots_df.empty:
                    if len(current_zone_pivots_df) >= min_zone_strength:
                        grouped_zones_list.append(current_zone_pivots_df)
                    else:
                        pass # Discard zone silently or log if needed
                # Start a new zone with the current pivot
                current_zone_pivots_df = pivot.to_frame().T
                # print(f"DEBUG group_pivots ({zone_type}): Started NEW zone with pivot {i} @ {pivot['timestamp']} (Not close)") # DEBUG

        # Add the last processed zone if it's not empty and meets strength requirement
        if not current_zone_pivots_df.empty and len(current_zone_pivots_df) >= min_zone_strength:
            grouped_zones_list.append(current_zone_pivots_df)
        elif not current_zone_pivots_df.empty:
             pass # Discard zone silently or log if needed

        # Process the grouped zones into the final format
        final_zones_data = []
        # print(f"DEBUG group_pivots ({zone_type}): Processing {len(grouped_zones_list)} grouped zones...") # DEBUG
        for idx, zone_df in enumerate(grouped_zones_list):
            first_pivot = zone_df.iloc[0]
            last_pivot = zone_df.iloc[-1]
            first_pivot_ts = first_pivot['timestamp']
            last_pivot_ts = last_pivot['timestamp']
            # Ensure frequency is available for calculation, otherwise fallback
            zone_candles = 1 # Default if freq is None or calculation fails
            if close.index.freq:
                 try:
                    zone_candles = (last_pivot_ts - first_pivot_ts).total_seconds() / (pd.Timedelta(close.index.freq).total_seconds()) + 1
                 except AttributeError:
                     # Fallback if freq.delta is not available (e.g., complex freq)
                     zone_candles = len(close.loc[first_pivot_ts:last_pivot_ts])
            else:
                zone_candles = len(close.loc[first_pivot_ts:last_pivot_ts])

            # print(f"DEBUG group_pivots ({zone_type}): Zone {idx} Candidate: Start={first_pivot_ts}, End={last_pivot_ts}, Strength={len(zone_df)}, Candles={zone_candles:.2f}") # DEBUG
            if zone_candles >= min_zone_width_candles:
                # Determine actual zone boundaries from the candles involved
                zone_low = zone_df['candle_low'].min()
                zone_high = zone_df['candle_high'].max()

                # Determine start/end indices based on pivots
                start_idx = first_pivot['timestamp']
                # Extend the zone validity
                end_idx_pivot = last_pivot['timestamp']
                end_idx_loc = prices.index.get_loc(end_idx_pivot)
                extended_end_loc = min(end_idx_loc + zone_extend_candles, len(prices) - 1)
                end_idx_extended = prices.index[extended_end_loc]

                final_zones_data.append({
                    'zone_type': zone_type,
                    'start_idx': start_idx,
                    'end_idx': end_idx_extended, # Use extended end
                    'first_pivot_idx': first_pivot['timestamp'],
                    'last_pivot_idx': last_pivot['timestamp'],
                    'low_price': zone_low,
                    'high_price': zone_high,
                    'strength': len(zone_df),
                    'candles': zone_candles
                })
            else:
                pass # Skip zone if width requirement not met

        return final_zones_data

    # Group supply and demand pivots
    supply_zones_list = group_pivots(supply_pivots_idx, high, 'supply') # Use high prices for supply pivots
    demand_zones_list = group_pivots(demand_pivots_idx, low, 'demand') # Use low prices for demand pivots

    # Combine and format into DataFrame
    all_zones = pd.DataFrame(supply_zones_list + demand_zones_list)

    if all_zones.empty:
        return pd.DataFrame(columns=[
            'zone_type', 'start_idx', 'end_idx', 'first_pivot_idx',
            'last_pivot_idx', 'low_price', 'high_price', 'strength', 'candles'
        ])

    all_zones = all_zones.sort_values(by='start_idx').reset_index(drop=True)

    # TODO: Add logic to merge overlapping zones of the same type if desired

    return all_zones


def add_zone_signals(
    close: pd.Series,
    zones_df: pd.DataFrame,
    zone_proximity_pct: float
) -> pd.DataFrame:
    """
    Generates signals based on price interaction with identified zones.

    Args:
        close (pd.Series): Closing prices.
        zones_df (pd.DataFrame): DataFrame of identified zones from find_pivot_zones.
        zone_proximity_pct (float): Percentage threshold for price proximity to zone.

    Returns:
        pd.DataFrame: Boolean series indicating:
            - 'price_in_demand_zone': True if price is near/in a demand zone.
            - 'price_in_supply_zone': True if price is near/in a supply zone.
    """
    price_in_demand = pd.Series(False, index=close.index)
    price_in_supply = pd.Series(False, index=close.index)

    if zones_df.empty:
        return pd.DataFrame({
            'price_in_demand_zone': price_in_demand,
            'price_in_supply_zone': price_in_supply
        })

    for _, zone in zones_df.iterrows():
        zone_low = zone['low_price']
        zone_high = zone['high_price']
        # Use zone height for proximity calculation if height > 0, else use percentage of price
        zone_height = zone_high - zone_low
        if zone_height > 1e-9: # Avoid division by zero or tiny heights
            # Proximity based on zone height
            proximity_value = zone_height * zone_proximity_pct
        else:
            # Proximity based on price level if zone is flat
            proximity_value = zone_high * zone_proximity_pct

        # Define extended range for proximity check
        check_low = zone_low - proximity_value
        check_high = zone_high + proximity_value

        # Mask for the time period when the zone is considered active
        # A zone is active from its start index to its (potentially extended) end index
        active_mask = (close.index >= zone['start_idx']) & (close.index <= zone['end_idx'])

        if zone['zone_type'] == 'demand':
            # Price is near or within the demand zone during its active period
            is_near = (close >= check_low) & (close <= check_high)
            price_in_demand.loc[active_mask & is_near] = True # Apply only where active and near
        elif zone['zone_type'] == 'supply':
            # Price is near or within the supply zone during its active period
            is_near = (close >= check_low) & (close <= check_high)
            price_in_supply.loc[active_mask & is_near] = True # Apply only where active and near

    return pd.DataFrame({
        'price_in_demand_zone': price_in_demand,
        'price_in_supply_zone': price_in_supply
    })


# Example usage (for testing purposes)
if __name__ == '__main__':
    # Import EdgeConfig only for the test block
    from .config import EdgeConfig 
    cfg = EdgeConfig() # Use default config for testing

    # Simulate data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=500, freq='1D') # Use '1D' for clarity
    base_price = 100
    price_movements = np.random.randn(500) * 0.5 # Smaller movements
    trend = np.linspace(0, 10, 500) # Add a slight upward trend
    noise = np.random.normal(0, 1.5, 500) # Add more noise
    price_data = base_price + price_movements.cumsum() + trend + noise

    # Simulate more realistic highs and lows
    high_data = price_data + np.random.uniform(0.1, 1.0, 500)
    low_data = price_data - np.random.uniform(0.1, 1.0, 500)
    # Ensure low is never above high or close, high never below close
    low_data = np.minimum(low_data, price_data - 0.01)
    high_data = np.maximum(high_data, price_data + 0.01)
    low_data = np.minimum(low_data, high_data - 0.02)

    close_prices = pd.Series(price_data, index=dates, name='Close')
    high_prices = pd.Series(high_data, index=dates, name='High')
    low_prices = pd.Series(low_data, index=dates, name='Low')
    ohlc = pd.concat([close_prices, high_prices, low_prices], axis=1)

    print("Finding zones...")
    # Find zones using the implemented logic
    # Pass parameters from the config object
    zones = find_pivot_zones(
        close=ohlc['Close'],
        high=ohlc['High'],
        low=ohlc['Low'],
        pivot_lookback=cfg.pivot_lookback,
        pivot_prominence=cfg.pivot_prominence,
        zone_merge_proximity=cfg.zone_merge_proximity,
        min_zone_width_candles=cfg.min_zone_width_candles,
        min_zone_strength=cfg.min_zone_strength,
        zone_extend_candles=cfg.zone_extend_candles
    )

    print(f"\n{len(zones)} Zones Found:")
    if not zones.empty:
        print(zones.to_string())

    # Generate zone signals
    zone_signals = add_zone_signals(
        ohlc['Close'], zones,
        zone_proximity_pct=cfg.zone_proximity_pct # Use config default
    )

    print("\nZone Signals (Sample):")
    print(zone_signals.iloc[100:110]) # Show a sample slice

    print(f"\nPrice in Demand Zone ({zone_signals['price_in_demand_zone'].sum()} times)")
    print(f"Price in Supply Zone ({zone_signals['price_in_supply_zone'].sum()} times)")

    # Optional: Plotting for visual verification (requires matplotlib and mplfinance)
    try:
        import matplotlib.pyplot as plt
        import mplfinance as mpf

        fig, ax = plt.subplots(figsize=(18, 9))
        # Use mplfinance for candlestick plotting
        ohlc_subset = ohlc.iloc[-200:] # Plot last 200 candles for clarity
        mpf.plot(ohlc_subset, type='candle', ax=ax, style='yahoo', warn_too_much_data=2000)

        # Overlay zones on the plot
        zones_subset = zones[zones['end_idx'] >= ohlc_subset.index[0]]
        for _, zone in zones_subset.iterrows():
            start_plot = max(zone['start_idx'], ohlc_subset.index[0])
            end_plot = min(zone['end_idx'], ohlc_subset.index[-1])
            if start_plot >= end_plot:
                continue

            color = 'green' if zone['zone_type'] == 'demand' else 'red'
            ax.axhspan(zone['low_price'], zone['high_price'],
                        xmin=ohlc_subset.index.get_loc(start_plot) / len(ohlc_subset),
                        xmax=ohlc_subset.index.get_loc(end_plot) / len(ohlc_subset),
                        color=color, alpha=0.15, zorder=0) # Lower zorder to be behind candles
            # Add text label for strength
            ax.text(end_plot, (zone['low_price'] + zone['high_price']) / 2,
                    f" {zone['zone_type'][0].upper()}{zone['strength']}",
                    color=color, ha='left', va='center', fontsize=8, alpha=0.8)


        ax.set_title('Candlestick Chart with Supply/Demand Zones (Last 200 Candles)')
        ax.set_ylabel('Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.savefig('zone_visualization_mplf.png')
        # plt.show()
        print("\nPlot generated using mplfinance (comment out plt.show() or plt.savefig() to display).")

    except ImportError:
        print("\nInstall matplotlib and mplfinance to visualize zones: pip install matplotlib mplfinance")

    print("\nRun this script: conda run -n vectorbtpro --no-capture-output --live-stream python scripts/strategies/refactored_edge/zones.py")
