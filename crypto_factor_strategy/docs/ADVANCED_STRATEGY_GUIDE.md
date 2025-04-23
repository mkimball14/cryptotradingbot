# Comprehensive Guide: Building a Factor-Based Quant Strategy with Python 3.11 & VectorBT Pro

**Goal:** Implement and backtest a quantitative trading strategy that ranks cryptocurrencies based on multiple factors (e.g., momentum, volatility) and constructs a portfolio by systematically allocating capital to the top-ranked assets.

**Tools:**
*   Python 3.11 (as specified for VectorBT Pro compatibility)
*   VectorBT Pro (vbt)
*   Pandas
*   NumPy
*   (Optional) Matplotlib, Plotly for visualization
*   (Optional) Cursor AI for code implementation assistance
*   (Optional) `python-coinbase-advanced` for Coinbase integration

---

## Step 1: Project Setup & Environment

**Objective:** Create a structured project environment and install necessary libraries.

1.  **Create Project Directory:**
    ```bash
    mkdir crypto_factor_strategy
    cd crypto_factor_strategy
    ```

2.  **Set up Python Virtual Environment:** (Recommended)
    ```bash
    # Ensure you have Python 3.11 available
    python3.11 -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    ```

3.  **Install Libraries:**
    ```bash
    pip install vectorbtpro pandas numpy python-coinbase-advanced # Add other libraries as needed, e.g., ccxt, matplotlib, openpyxl, python-dotenv
    # Potentially upgrade pip and setuptools first
    pip install --upgrade pip setuptools
    ```
    *   *Note:* Ensure your `vectorbtpro` installation is compatible with Python 3.11. Check their documentation if you encounter issues.

4.  **Create Project Structure:** (Suggested)
    ```
    crypto_factor_strategy/
    ├── venv/
    ├── config/             # Configuration files (e.g., API keys - use .env)
    ├── data/               # Raw and processed data (CSV, Parquet)
    ├── notebooks/          # Jupyter notebooks for research & analysis
    ├── strategies/         # Python modules for strategy logic
    │   ├── __init__.py
    │   └── factors.py      # Factor calculation functions
    │   └── portfolio.py    # Portfolio construction logic
    │   └── data_utils.py   # Data loading functions
    │   └── backtester.py   # Backtesting execution script
    ├── .env                # Environment variables (API keys, etc.) - **Add to .gitignore!**
    ├── requirements.txt    # List of dependencies
    └── main.py             # Main script to run backtests
    ```

5.  **Generate `requirements.txt`:**
    ```bash
    pip freeze > requirements.txt
    ```

6.  **(Required for Coinbase) `.env` File:**
    Create a `.env` file in the root directory for API keys. Load them using `python-dotenv`.
    ```.env
    # Coinbase API Keys
    COINBASE_API_KEY="organizations/{org_id}/apiKeys/{key_id}"
    COINBASE_API_SECRET="-----BEGIN EC PRIVATE KEY-----\\nYOUR PRIVATE KEY\\n-----END EC PRIVATE KEY-----\\n"
    # Note the double backslash needed for newline in .env for some parsers
    ```
    Remember to add `.env` to your `.gitignore` file.

---

## Step 2: Data Acquisition & Preparation

**Objective:** Obtain and prepare historical OHLCV data for the chosen universe of assets, preferably using the Coinbase Advanced API for consistency with potential live trading.

1.  **Choose Data Source:**
    *   **Coinbase Advanced API (Recommended):** Use the official `python-coinbase-advanced` library to fetch historical data directly from the target exchange. This ensures data consistency between backtesting and live trading. Requires API Keys (configure in `.env`).
    *   **VectorBT Pro Data:** `vbt.Data.download()` can fetch from `ccxt` (if configured for Coinbase) or other sources like `yfinance` (ensure symbols match Coinbase, e.g., 'BTC-USD'). Less direct than using the official library.
    *   **CCXT Library:** A versatile library to fetch data from many exchanges, including Coinbase, but might require more setup for advanced API features.
    *   **Local Files:** Download data via Coinbase API or other sources and store locally (CSV, Parquet). Useful for offline work or very long histories.

2.  **Define Data Requirements:**
    *   **Universe:** List of symbols available on Coinbase Pro/Advanced (e.g., `['BTC-USD', 'ETH-USD', 'SOL-USD', ...]`).
    *   **Timeframe:** e.g., `'1d'`, `'4h'`, `'1h'`. Daily (`'1d'`) is recommended to start. Coinbase API uses specific granularity strings (e.g., `ONE_DAY`, `ONE_HOUR`).
    *   **Period:** Sufficient history (e.g., 3-5 years). Be mindful of Coinbase API historical data limits and fetch in chunks if necessary.
    *   **Columns:** Must include `Open`, `High`, `Low`, `Close`, `Volume`. Ensure consistent naming (lowercase `open`, `high`, `low`, `close`, `volume`).

3.  **Implement Data Loading Function:** (Place in `strategies/data_utils.py`)
    *   Create a function to load data for all symbols in the universe using the Coinbase API and combine it into a single Pandas DataFrame with a MultiIndex (`['date', 'symbol']`).

    ```python
    # In strategies/data_utils.py
    import pandas as pd
    import time
    from datetime import datetime, timezone
    import os
    from dotenv import load_dotenv
    try:
        from coinbase.rest import RESTClient
    except ImportError:
        print("Please install python-coinbase-advanced: pip install python-coinbase-advanced")
        RESTClient = None # type: ignore

    load_dotenv() # Load variables from .env

    def get_coinbase_client():
        """Initializes and returns a Coinbase RESTClient."""
        api_key = os.getenv("COINBASE_API_KEY")
        # Handle newline characters correctly from .env
        api_secret_raw = os.getenv("COINBASE_API_SECRET", "")
        api_secret = api_secret_raw.replace('\\\\n', '\\n') # Fix: Use double backslash for literal interpretation

        if not api_key or not api_secret_raw:
            print("Error: Coinbase API Key or Secret not found in .env file.")
            return None
        if RESTClient is None:
            print("Error: python-coinbase-advanced library not found.")
            return None
        try:
            client = RESTClient(api_key=api_key, api_secret=api_secret)
            return client
        except Exception as e:
            print(f"Error initializing Coinbase client: {e}")
            return None

    def load_coinbase_data(symbols, start_iso, end_iso, granularity='ONE_DAY', client=None):
        """
        Loads historical OHLCV data from Coinbase Advanced API for multiple symbols.

        Args:
            symbols (list): List of Coinbase product IDs (e.g., ['BTC-USD', 'ETH-USD']).
            start_iso (str): Start date in ISO 8601 format (e.g., '2020-01-01T00:00:00Z').
            end_iso (str): End date in ISO 8601 format (e.g., '2024-01-01T00:00:00Z').
            granularity (str): Coinbase granularity string ('ONE_MINUTE', 'FIVE_MINUTE',
                               'FIFTEEN_MINUTE', 'THIRTY_MINUTE', 'ONE_HOUR', 'TWO_HOUR',
                               'SIX_HOUR', 'ONE_DAY').
            client (RESTClient, optional): Pre-initialized Coinbase RESTClient. Defaults to None.

        Returns:
            pd.DataFrame: Multi-index DataFrame with ['date', 'symbol'] index and
                          lowercase ohlcv columns, or None if loading fails.
        """
        if client is None:
            client = get_coinbase_client()
        if client is None:
            return None

        all_data = {}
        start_ts = int(datetime.fromisoformat(start_iso.replace("Z", "+00:00")).timestamp())
        end_ts = int(datetime.fromisoformat(end_iso.replace("Z", "+00:00")).timestamp())

        # Coinbase API has a limit of 300 candles per request
        granularity_seconds_map = {
            'ONE_MINUTE': 60, 'FIVE_MINUTE': 300, 'FIFTEEN_MINUTE': 900,
            'THIRTY_MINUTE': 1800, 'ONE_HOUR': 3600, 'TWO_HOUR': 7200,
            'SIX_HOUR': 21600, 'ONE_DAY': 86400
        }
        seconds_per_candle = granularity_seconds_map.get(granularity, 86400)
        max_candles_per_req = 300
        step_seconds = max_candles_per_req * seconds_per_candle

        print(f"Fetching data for {len(symbols)} symbols from {start_iso} to {end_iso} ({granularity})...")

        for symbol in symbols:
            print(f"  Fetching {symbol}...")
            symbol_data = []
            current_start_ts = start_ts

            while current_start_ts < end_ts:
                current_end_ts = min(current_start_ts + step_seconds - seconds_per_candle, end_ts)
                print(f"    Fetching chunk: {datetime.fromtimestamp(current_start_ts, tz=timezone.utc)} to {datetime.fromtimestamp(current_end_ts, tz=timezone.utc)}")
                try:
                    candles = client.get_candles(
                        product_id=symbol,
                        start=str(current_start_ts),
                        end=str(current_end_ts),
                        granularity=granularity
                    )['candles']

                    if not candles:
                        print(f"    No data returned for chunk in {symbol}. Adjusting start or stopping fetch for {symbol}.")
                        # If it's the very first request and no data, stop for this symbol
                        if current_start_ts == start_ts:
                           break
                        # Otherwise, try advancing start time slightly beyond the failed chunk end time
                        current_start_ts = current_end_ts + seconds_per_candle
                        continue # Skip to next iteration of while loop


                    df_chunk = pd.DataFrame(candles)
                    symbol_data.append(df_chunk)

                    last_candle_ts = int(df_chunk['start'].iloc[-1])
                    current_start_ts = last_candle_ts + seconds_per_candle

                    time.sleep(0.2) # Respect rate limits

                except Exception as e:
                    print(f"    Error fetching chunk for {symbol}: {e}")
                    # Implement retry logic here (optional)
                    time.sleep(1)
                    # For simplicity, break. Robust implementation might retry or skip chunk.
                    break

            if symbol_data:
                df_symbol = pd.concat(symbol_data, ignore_index=True)
                df_symbol['start'] = pd.to_datetime(df_symbol['start'].astype(int), unit='s', utc=True)
                df_symbol = df_symbol.rename(columns={
                    'start': 'date', 'low': 'low', 'high': 'high',
                    'open': 'open', 'close': 'close', 'volume': 'volume'
                })
                df_symbol = df_symbol[['date', 'open', 'high', 'low', 'close', 'volume']]
                df_symbol[['open', 'high', 'low', 'close', 'volume']] = df_symbol[['open', 'high', 'low', 'close', 'volume']].astype(float)
                df_symbol = df_symbol.sort_values('date').drop_duplicates('date').set_index('date')
                all_data[symbol] = df_symbol
            else:
                print(f"  No data loaded for {symbol}.")


        if not all_data:
            print("Error: Failed to load data for any symbol.")
            return None

        combined_df = pd.concat(all_data, names=['symbol', 'date']).swaplevel().sort_index()

        # Data Alignment & Cleaning (Crucial!)
        combined_df_unstacked = combined_df.unstack('symbol')
        full_date_range = pd.date_range(
            start=combined_df_unstacked.index.min(),
            end=combined_df_unstacked.index.max(),
            freq=pd.Timedelta(seconds=seconds_per_candle),
            tz='UTC'
        )
        combined_df_reindexed = combined_df_unstacked.reindex(full_date_range)

        # Forward fill, then backward fill
        combined_df_filled = combined_df_reindexed.fillna(method='ffill').fillna(method='bfill')
        final_df = combined_df_filled.stack('symbol', future_stack=True).swaplevel().sort_index()

        # Final Type Conversion & Null Check
        for col in ['open', 'high', 'low', 'close', 'volume']:
             if col in final_df.columns:
                 final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
        final_df.dropna(subset=['open', 'high', 'low', 'close'], inplace=True) # Drop rows with missing core price data
        final_df['volume'] = final_df['volume'].fillna(0) # Fill missing volume with 0

        print(f"Data loading complete. Final shape after cleaning: {final_df.shape}")
        return final_df

    # --- Example Usage ---
    # universe = ['BTC-USD', 'ETH-USD', 'SOL-USD']
    # start_dt_iso = '2020-01-01T00:00:00Z'
    # end_dt_iso = '2024-01-01T00:00:00Z'
    # ohlcv_data = load_coinbase_data(universe, start_dt_iso, end_dt_iso, granularity='ONE_DAY')
    #
    # if ohlcv_data is not None:
    #     print("Data loaded and processed.")
    ```
    *   **Cursor AI Tip:** "Refine the `load_coinbase_data` function to handle potential API errors more gracefully, implement retries with exponential backoff, and ensure robust NaN handling after combining data for multiple symbols."

4.  **Data Quality Checks (Important Addition):**
    *   After loading, perform essential checks:
        *   **Missing Values:** Explicitly check for NaNs again after alignment and filling (`ohlcv_data.isnull().sum()`).
        *   **Stale Prices:** Identify periods where the price doesn't change for multiple consecutive bars (especially if volume is zero), as this might indicate bad data.
        *   **Outliers:** Check for extreme price or return values that might be errors (e.g., returns > 50% in a day).
        *   **Volume Anomalies:** Look for periods with zero volume or extremely high volume spikes.
    *   Implement logic to handle these (e.g., drop affected periods/assets, winsorize outliers) *before* calculating factors.

---

## Step 3: Universe Definition

**Objective:** Formally define the set of assets the strategy will consider.

1.  **Start Simple: Static Universe:** For initial development, use a fixed list of highly liquid cryptocurrencies available on Coinbase.
    ```python
    # Define your universe (choose symbols with good data availability on Coinbase)
    UNIVERSE = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'XRP-USD', 'DOGE-USD', 'MATIC-USD', 'DOT-USD', 'AVAX-USD', 'LINK-USD']
    # Ensure these symbols exist on Coinbase Advanced Trading and have sufficient history via API.
    ```

2.  **Refine Data:** Load data specifically for this universe using the function from Step 2. Ensure all assets have data for the desired backtest period. Filter out assets with insufficient history or excessive missing data *after* loading and cleaning.

3.  **Future Enhancement:** Consider dynamic universe selection (e.g., top N by market cap/volume traded on Coinbase, rebalanced monthly) but start static.

---

## Step 4: Factor Definition & Calculation

**Objective:** Define and calculate quantitative factors for each asset in the universe over time. **Focus on vectorization.**

1.  **Factor Ideas (Start with 2-3):**
    *   **Momentum:** Price change over a period (e.g., 3 months, 6 months).
    *   **Volatility:** Standard deviation of daily returns (e.g., over the last 1 month). Lower volatility is sometimes preferred.
    *   **Relative Strength:** Compare asset performance to a benchmark (e.g., BTC-USD) or the universe average.

2.  **Implement Factor Calculations (Vectorized):** Create functions (e.g., in `strategies/factors.py`) that take the multi-index OHLCV DataFrame and return a DataFrame of factor values, also indexed by `['date', 'symbol']`.

    ```python
    # In strategies/factors.py
    import pandas as pd
    import numpy as np
    from numba import njit # Import njit

    # Example Factor 1: Momentum (Pandas is usually efficient enough)
    def calculate_momentum(close_prices, window=63): # Approx 3 months of trading days
        """Calculates price momentum (percent change) over a window."""
        close_prices_sorted = close_prices.sort_index(level=['symbol', 'date'])
        return close_prices_sorted.groupby(level='symbol').pct_change(periods=window, fill_method=None)

    # Example Factor 2: Volatility (Pandas rolling is often efficient)
    def calculate_volatility(close_prices, window=21): # Approx 1 month
        """Calculates rolling historical volatility (std dev of daily returns)."""
        close_prices_sorted = close_prices.sort_index(level=['symbol', 'date'])
        returns = close_prices_sorted.groupby(level='symbol').pct_change(fill_method=None)
        # Use .values to potentially speed up rolling calculation if index alignment is not needed inside rolling
        volatility = returns.groupby(level='symbol').rolling(window=window, min_periods=int(window*0.8)).std()
        volatility = volatility.reset_index(level=0, drop=True) # Drop the symbol level added by rolling
        return volatility

    # Example Factor 3: Custom Factor using Numba for potential speedup
    @njit # Decorator to compile this function with Numba
    def _custom_factor_logic_nb(close_array, window):
        """Numba-compiled function for custom factor logic."""
        # Numba works best with NumPy arrays and supported operations
        num_rows = close_array.shape[0]
        output = np.full(num_rows, np.nan, dtype=np.float64)
        if window <= 0 or window > num_rows:
             return output

        for i in range(window - 1, num_rows):
            window_slice = close_array[i - window + 1 : i + 1]
            # Ignore NaNs in the window slice for max calculation
            if np.all(np.isnan(window_slice)):
                 continue # Skip if window is all NaNs
            rolling_max = np.nanmax(window_slice)
            if rolling_max > 1e-9: # Avoid division by zero or tiny numbers
                 output[i] = close_array[i] / rolling_max
        return output

    def calculate_custom_factor(close_prices, window=30):
         """Calculates a custom factor, using Numba for core logic."""
         # Apply the Numba function to the NumPy array of each group
         return close_prices.groupby(level='symbol', group_keys=False).apply(
             lambda x: pd.Series(_custom_factor_logic_nb(x.to_numpy(), window), index=x.index)
         )

    # --- Example Usage within a class or main script ---
    # Assuming 'ohlcv_data' is your cleaned multi-index DataFrame
    # close = ohlcv_data['close']
    # mom_factor = calculate_momentum(close, window=63)
    # vol_factor = calculate_volatility(close, window=21)
    # custom_factor = calculate_custom_factor(close, window=30)
    #
    # factor_data = pd.DataFrame({
    #     'momentum_3m': mom_factor,
    #     'volatility_1m': vol_factor,
    #     'custom_factor': custom_factor
    # }).dropna() # Drop rows with NaNs from factor calculation lookbacks
    #
    # print("Factor data sample:")
    # print(factor_data.head())
    ```
    *   **Numba Optimization Note:** While standard Pandas/NumPy operations are often fast, for computationally intensive custom factor logic involving loops or complex calculations not easily vectorized, decorating your core calculation function with `@njit` from Numba can provide significant speedups (approaching C/C++ speeds). Ensure your Numba function works primarily with NumPy arrays and supported operations, and handle NaNs appropriately within the Numba code.
    *   **Crucial:** Use `groupby(level='symbol')` before applying Pandas time-series functions. Sorting the index first (`sort_index(level=['symbol', 'date'])`) is important. Use `fill_method=None` in `pct_change` to avoid incorrect calculations over gaps. Handle NaNs resulting from lookback periods *after* calculation.
    *   **Cursor AI Tip:** Ask Cursor: "Write a vectorized Python function using Pandas to calculate the 3-month annualized volatility (standard deviation of daily returns * sqrt(365)) for a multi-index DataFrame `ohlcv_data` with levels 'date' and 'symbol', containing a 'close' column, ensuring calculations are independent for each symbol."

3.  **Factor Research & Validation (New Subsection):**
    *   **Rationale:** Don't pick factors arbitrarily. They should ideally have a sound economic or behavioral basis (e.g., momentum reflecting behavioral herding, value reflecting reversion to fundamental worth).
    *   **Empirical Testing:** Before combining factors, test them individually. Calculate the Information Coefficient (IC - correlation between factor value at time `t` and forward returns at `t+1`) or simulate portfolios based on single-factor ranks (`vbt.Portfolio.from_quantile`, `vbt.Portfolio.from_factor`). This helps identify factors with actual predictive power in your universe and timeframe.
    *   **Out-of-Sample Validation:** The most rigorous test is validating factor performance on data not used during initial research (e.g., using Walk-Forward Optimization as discussed later).

---

## Step 5: Factor Preprocessing & Combination

**Objective:** Clean factor data, make factors comparable, and combine them into a single score.

1.  **Handle Missing Factor Values:** Address NaNs resulting from lookback windows *before* cross-sectional operations. Dropping rows with any NaN factor is often the safest approach initially.
    ```python
    # Example: Drop rows where any factor is NaN BEFORE ranking/scoring
    # original_count = len(factor_data)
    # factor_data = factor_data.dropna()
    # print(f"Dropped {original_count - len(factor_data)} rows with NaNs in factors.")
    # Ensure index is aligned with ohlcv data if needed later
    # ohlcv_data_aligned = ohlcv_data.loc[factor_data.index]
    ```

2.  **Standardize Factors (Cross-Sectionally):** Make factors comparable at each time step. Apply *after* handling NaNs.
    *   **Ranking:** Rank assets based on each factor from 1 to N. Simple, robust to outliers.
    *   **Z-Scoring:** Subtract the cross-sectional mean and divide by the cross-sectional standard deviation. Assumes normality, sensitive to outliers. Handle potential division by zero if standard deviation is zero for a given date.

    ```python
    # In strategies/factors.py (or utils)
    def cross_sectional_rank(factor_series):
        """Ranks factor values cross-sectionally at each time step."""
        return factor_series.groupby(level='date').rank(method='first', pct=True, na_option='keep')

    def cross_sectional_zscore(factor_series):
        """Z-scores factor values cross-sectionally at each time step."""
        group = factor_series.groupby(level='date')
        # Handle dates with zero std dev robustly
        def zscore(x):
            std = x.std()
            if std < 1e-8: # Check for near-zero std dev
                return np.zeros_like(x)
            return (x - x.mean()) / std
        return group.transform(zscore)

    # --- Apply to factors ---
    # processed_factors = pd.DataFrame(index=factor_data.index)
    # processed_factors['momentum_rank'] = cross_sectional_rank(factor_data['momentum_3m'])
    # # Invert volatility rank if lower is better
    # processed_factors['volatility_rank'] = cross_sectional_rank(-factor_data['volatility_1m'])
    # # Drop any potential remaining NaNs (should be fewer now)
    # processed_factors = processed_factors.dropna()

    # print("Processed (ranked) factor data sample:")
    # print(processed_factors.head())
    ```

3.  **Combine Factors:** Create a single composite score. Apply *after* processing individual factors.
    *   **Equal Weighting (Start Simple):** Average the processed factor scores/ranks. Ensure alignment if rows were dropped.

    ```python
    # Example combining ranks
    # Ensure processed_factors index aligns with the rows you intend to score
    # num_factors = len(processed_factors.columns)
    # combined_score = processed_factors.sum(axis=1) / num_factors

    # Add to the main factor data frame (or keep separate)
    # factor_data = factor_data.loc[combined_score.index] # Align index after drops/preprocessing
    # factor_data['combined_score'] = combined_score
    # print("Combined score sample:")
    # print(factor_data[['combined_score']].head())
    ```
    *   **Future:** Explore weighted combinations or ML models.
    *   **Cursor AI Tip:** "Given a DataFrame `processed_factors` with standardized factor columns (ranks or z-scores), write code to calculate an equal-weighted combined score, ensuring that NaNs in individual factor columns are handled appropriately (e.g., ignored in the sum/count for that row)."

---

## Step 6: Portfolio Construction

**Objective:** Define rules to translate factor scores into target portfolio weights, incorporating basic risk controls.

1.  **Choose Construction Rule:**
    *   **Long Top N:** Rank by `combined_score` each day/week. Allocate equal weight to the top N assets (e.g., top 3). Simple, long-only.
    *   **Quintile/Decile Spread (More Advanced):** Rank, go long top quintile (20%), short bottom quintile (20%). Aims for market neutrality. Requires shorting capability (check if available/allowed on Coinbase for your account).

2.  **Implement Weight Calculation (Vectorized):** (Place in `strategies/portfolio.py`)

    ```python
    # In strategies/portfolio.py
    import pandas as pd
    import numpy as np # Import numpy

    def calculate_top_n_weights(scores, n=3, max_weight_per_asset=None):
        """Calculates equal weights for the top N assets based on score, with optional capping."""
        ranks = scores.dropna().groupby(level='date').rank(ascending=False, method='first')
        is_top_n = (ranks <= n)
        
        # Count number of assets selected each day
        assets_per_day = is_top_n.groupby(level='date').sum()
        
        # Calculate base equal weight
        base_weight = (1.0 / assets_per_day).replace([np.inf, -np.inf, np.nan], 0) # Handle division by zero if no assets selected

        # Apply weights only to top N
        target_weights = is_top_n.mul(base_weight, level='date', axis=0)

        # Apply max weight cap if specified
        if max_weight_per_asset is not None:
             target_weights = target_weights.clip(upper=max_weight_per_asset)
             # Optional: Re-normalize weights per day if capping occurred (more complex)
             # total_weight_per_day = target_weights.groupby(level='date').sum()
             # target_weights = target_weights.div(total_weight_per_day, level='date', axis=0)

        return target_weights.reindex(scores.index).fillna(0.0)

    def calculate_long_short_quintile_weights(scores, leverage=1.0):
        """Calculates weights for a long/short portfolio based on score quintiles."""
        ranks = scores.dropna().groupby(level='date').rank(method='first', pct=True) # Ranks 0-1

        long_quintile = ranks >= 0.8
        short_quintile = ranks <= 0.2

        raw_weights = pd.Series(0.0, index=scores.index)
        raw_weights[long_quintile] = 1.0
        raw_weights[short_quintile] = -1.0

        # Normalize weights daily to be dollar neutral and apply leverage
        def normalize_ls_weights(group):
            longs = group[group > 0]
            shorts = group[group < 0]
            # Equal weight longs, scaled by leverage/2
            group[group > 0] = (leverage / 2.0) / len(longs) if len(longs) > 0 else 0
            # Equal weight shorts, scaled by leverage/2
            group[group < 0] = (-leverage / 2.0) / len(shorts) if len(shorts) > 0 else 0
            return group

        target_weights = raw_weights.groupby(level='date').transform(normalize_ls_weights)
        return target_weights.reindex(scores.index).fillna(0.0)


    # --- Example Usage ---
    # combined_score = factor_data['combined_score']
    # target_weights_top3 = calculate_top_n_weights(combined_score, n=3, max_weight_per_asset=0.5) # Cap at 50%
    # target_weights_ls = calculate_long_short_quintile_weights(combined_score, leverage=1.0) # Dollar neutral

    # print("Top 3 Target weights sample:")
    # print(target_weights_top3.unstack('symbol').head())
    # print("\nLong/Short Quintile Target weights sample:")
    # print(target_weights_ls.unstack('symbol').head())
    ```

3.  **Define Rebalancing Frequency:** How often will you recalculate factors and adjust portfolio weights? (e.g., `'D'`, `'W'`, `'M'`). Daily or weekly is common.

4.  **Risk Management Rules within Construction (New Subsection):**
    *   **Position Concentration:** As shown in `calculate_top_n_weights`, add a `max_weight_per_asset` parameter to cap exposure to any single asset. Decide whether to simply cap or to redistribute the excess weight proportionally among other selected assets (more complex).
    *   **Volatility Targeting / Leverage Control (Advanced):** You *could* scale the final `target_weights` DataFrame up or down based on predicted portfolio volatility to maintain a more consistent risk level. For example, if target volatility is 15% annualized and predicted volatility is 30%, scale all weights by 0.5. This typically requires a volatility prediction model. Start without this.
    *   **Factor Exposure Constraints (Advanced):** Ensure the resulting portfolio doesn't have excessive unintended exposure to other factors (e.g., ensure a momentum portfolio isn't unintentionally massively short volatility). Requires more sophisticated portfolio optimization techniques.

---

## Step 7: Backtesting with VectorBT Pro

**Objective:** Simulate the strategy's performance using historical data.

1.  **Choose Portfolio Method:** `vbt.Portfolio.from_holding` remains suitable.

2.  **Set Simulation Parameters:**
    *   `init_cash`, `fees`, `slippage`, `freq`: As before.
    *   `close`: Aligned close price DataFrame.
    *   `cash_sharing=True`: Important for multi-asset portfolios; allows cash from closing one position to be used for opening another in the same rebalancing step.
    *   `group_by=True` (Optional but recommended): Groups orders by timestamp for more realistic simulation if cash_sharing is True.

3.  **Run Simulation:** (Place in `strategies/backtester.py`)

    ```python
    # In strategies/backtester.py
    import vectorbtpro as vbt
    import pandas as pd

    def run_factor_backtest(close_prices, target_weights, init_cash=100000, fees=0.001, slippage=0.0005, freq='D'):
        """Runs a backtest using target weights."""

        # --- Data Alignment (CRITICAL) ---
        weights_unstacked = target_weights.unstack('symbol')
        close_unstacked = close_prices.unstack('symbol')
        common_index = weights_unstacked.index.intersection(close_unstacked.index)
        common_symbols = weights_unstacked.columns.intersection(close_unstacked.columns)

        if len(common_index) == 0 or len(common_symbols) == 0:
             print("Error: No common dates or symbols found between weights and prices.")
             return None

        weights_aligned = weights_unstacked.loc[common_index, common_symbols].fillna(0.0)
        close_aligned = close_unstacked.loc[common_index, common_symbols]

        if weights_aligned.empty or close_aligned.empty:
            print("Error: Data alignment resulted in empty DataFrames.")
            return None
        close_aligned = close_aligned.dropna(axis=1, how='all')
        weights_aligned = weights_aligned[close_aligned.columns]


        print(f"Running backtest on {len(common_index)} dates and {len(common_symbols)} symbols.")
        print(f"Rebalancing frequency: {freq}")

        try:
            portfolio = vbt.Portfolio.from_holding(
                close=close_aligned,
                holding=weights_aligned,
                init_cash=init_cash,
                fees=fees,
                slippage=slippage,
                freq=freq,
                cash_sharing=True, # Allow cash reuse within a rebalance step
                group_by=True      # Group orders by timestamp
            )
            print("Backtest complete.")
            return portfolio
        except Exception as e:
            print(f"Error during backtest execution: {e}")
            import traceback
            print(traceback.format_exc())
            return None

    # --- Example Usage ---
    # ... (load data, calculate weights) ...
    # portfolio = run_factor_backtest(...)
    # if portfolio: print("Portfolio simulation successful.")
    ```
    *   **Important Note:** The backtest simulation typically assumes trades execute at the `close` price of the rebalancing period (or `open` of the next, depending on settings). Real-world execution involves delays and slippage. Account for this potential difference.
    *   **Cursor AI Tip:** "Show me how to configure `vbt.Portfolio.from_holding` with `cash_sharing=True` and `group_by=True` for a more realistic multi-asset backtest."

---

## Step 8: Performance Analysis

**Objective:** Evaluate the backtest results thoroughly, including benchmark comparison and parameter sweep analysis.

1.  **Key Metrics:** Use `portfolio.stats()`.
    ```python
    if portfolio:
        stats_df = portfolio.stats()
        print(stats_df)
        # ... (extract specific metrics as before) ...
    else:
        print("Backtest did not produce a valid portfolio.")
    ```

2.  **Benchmarking (New Subsection):**
    *   **Why:** To understand if the strategy adds value (alpha) beyond simply holding a market proxy. A strategy can be profitable but still underperform a simple buy-and-hold benchmark.
    *   **Choose Benchmark:**
        *   `BTC-USD`: A common choice for crypto.
        *   Equal-Weighted Universe Index: Calculate the daily return of holding an equal amount of each asset in your `UNIVERSE`.
    *   **Implementation:**
        ```python
        if portfolio and 'BTC-USD' in close_aligned.columns: # Check if BTC is in aligned data
             # Calculate benchmark returns (simple buy-and-hold BTC)
             btc_returns = close_aligned['BTC-USD'].pct_change()
             # Add benchmark returns to portfolio object for comparison plots/stats
             portfolio.benchmark_returns = btc_returns.loc[portfolio.returns.index] # Align benchmark dates

             # Recalculate stats including benchmark comparison
             stats_with_benchmark = portfolio.stats()
             print("\\n--- Stats with Benchmark ---")
             print(stats_with_benchmark)

             # Access benchmark-relative metrics
             alpha = stats_with_benchmark.get('Alpha', 'N/A') # .get() handles missing keys
             beta = stats_with_benchmark.get('Beta', 'N/A')
             print(f"Alpha: {alpha}")
             print(f"Beta: {beta}")

             # Plot against benchmark
             try:
                 fig = portfolio.plot(settings=dict(bm_returns=True)) # Now includes benchmark automatically
                 fig.show()
             except Exception as e:
                 print(f"Error plotting with benchmark: {e}")

        elif portfolio:
             print("BTC-USD not found in data for benchmarking.")

        ```
    *   **Cursor AI Tip:** "How can I calculate the daily returns of an equal-weighted portfolio of my `UNIVERSE` assets using my `ohlcv_data` DataFrame and add it as `benchmark_returns` to my VectorBT Pro `portfolio` object?"

3.  **Visualization:** Use `portfolio.plot()` (now potentially with benchmark), `plot_asset_value()`, `plot_underwater()`.

4.  **Analyzing Parameter Sweep Results (New Subsection):**
    *   If your backtest involved running multiple parameter combinations (e.g., using `vbt.Portfolio.from_signals` or `from_holding` with parameter lists passed to indicators/weight functions, often via `vbt.IndicatorFactory` or loops), the resulting `portfolio.stats()` will contain results for each combination, indexed by the parameters.
    *   **Finding Best Parameters:** Use Pandas on the `stats_df` to find top performers based on your chosen metric (e.g., Sharpe Ratio, Total Return).
        ```python
        # Assuming 'portfolio' is the result of a parameter sweep
        if portfolio and isinstance(portfolio.stats_summary.index, pd.MultiIndex): # Check if params were varied
            stats_df = portfolio.stats() # Get DataFrame of stats per parameter set
            print("\\n--- Parameter Sweep Analysis ---")
            # Sort by Sharpe Ratio (or your preferred metric)
            best_params_df = stats_df.sort_values('Sharpe Ratio', ascending=False)
            print("Top 5 Parameter Combinations by Sharpe Ratio:")
            print(best_params_df.head())

            # Example: Get the parameters of the absolute best run
            if not best_params_df.empty:
                 best_run_params = best_params_df.index[0]
                 print(f"\\nBest Parameter Set: {best_run_params}")
            else:
                 print("No valid parameter sets found in sweep results.")
                 best_run_params = None
        ```
    *   **Parameter Sensitivity:** Analyze how metrics change across different parameter values. Use `groupby()` on `stats_df`.
        ```python
        # Example: Analyze Sharpe Ratio grouped by momentum window parameter
        # Assuming 'momentum_window' was one of the varied parameters in the index name
        # parameter_level_name = 'momentum_window' # Replace with your actual parameter name in the index
        # if portfolio and isinstance(portfolio.stats_summary.index, pd.MultiIndex) and parameter_level_name in stats_df.index.names:
        #     print(f"\\nAverage Sharpe Ratio by {parameter_level_name}:")
        #     # Group by the specific parameter level in the MultiIndex
        #     print(stats_df['Sharpe Ratio'].groupby(level=parameter_level_name).mean())
        # else:
        #     print(f"Cannot group by {parameter_level_name} - not found in index or not a parameter sweep.")
        ```
    *   **Visualizing Specific Runs:** Plot the equity curve or signals for a specific, interesting parameter combination found during the sweep.
        ```python
        # Example: Plot equity for the best parameter set found above
        if portfolio and 'best_run_params' in locals() and best_run_params is not None:
             try:
                 print(f"\\nPlotting equity for params: {best_run_params}")
                 # Method 1: Selecting the column (might create a new portfolio object)
                 # portfolio[best_run_params].plot().show()
                 # Method 2: Using the column argument (often more efficient)
                 portfolio.plot(column=best_run_params).show()
             except Exception as e:
                 print(f"Error plotting specific parameter run: {e}")
        ```
    *   **Benchmark Comparison:** Remember that even the "best" parameter set from a sweep might still underperform a simple benchmark (like Buy & Hold BTC), reinforcing the need for careful validation and realistic expectations.

---

## Step 9: Iteration & Refinement

**Objective:** Improve the strategy based on analysis, considering parameter robustness and potential overfitting.

1.  **Analyze Results:** As before (vs benchmark, consistency, factor contribution, turnover, drawdowns).

2.  **Refine:** As before (Factors, Combination, Portfolio Construction, Universe, Rebalancing, Risk).

3.  **Parameter Sensitivity, Optimization & Robustness (Enhanced Subsection):**
    *   **Overfitting Risk:** Finding parameters that work perfectly on historical data is easy but dangerous (**overfitting** or **curve fitting**). These parameters often fail on new, unseen data because they captured noise rather than a true, persistent edge. Avoid excessive tweaking based solely on backtest results.
    *   **Sensitivity Analysis:** Test how sensitive performance is to small parameter changes (e.g., momentum window +/- 10%, N +/- 1). Robust strategies show reasonably stable performance around their optimal parameters. Analyze the parameter sweep results (Step 8.4) to understand sensitivity.
    *   **Robust Optimization (Cross-Validation):** Don't optimize parameters using your entire historical dataset at once, as this leads to overfitting.
        *   **Walk-Forward Optimization (WFO):** **Strongly recommended** for time-series data like financial markets. Divide data into sequential training and testing periods (e.g., train on 2 years, test on next 6 months, slide forward by 6 months). Optimize parameters *only* on the training data, then evaluate performance on the *next unseen* testing period. Repeat this process. Average the performance across all out-of-sample test periods for a more realistic estimate of future performance and find parameters that are robust across different regimes. *(Refer to WFO implementations like the one in `wfo_edge_strategy.py` for practical examples).*
        *   **Other CV Methods:** K-fold cross-validation can also be used but needs careful implementation for time-series (e.g., Purged K-Fold) to avoid lookahead bias.
    *   **Memory Considerations (Note):** Running backtests across many parameter combinations and long time periods can consume significant RAM (potentially GBs). If you hit memory limits:
        *   Reduce the number of parameter combinations tested simultaneously.
        *   Shorten the backtest period for initial exploration.
        *   Use data types like `float32` instead of `float64` where precision allows.
        *   (Advanced) Techniques like chunking the backtest or building combined Numba pipelines (wrapping signal/factor generation and simulation together, returning only summary stats) can drastically reduce memory for very large-scale optimization, but add significant implementation complexity.
    *   **Cursor AI Tip:** "Explain the concept of overfitting in trading strategy backtesting and why Walk-Forward Optimization helps mitigate it. Provide a simple conceptual example."

4.  **Repeat:** Iterate on refinements, always validating changes with robust backtesting methods like WFO. Use version control (Git) to track strategy evolution.

---

## Step 10: Live Trading Integration Considerations

**Objective:** Outline the key components and challenges involved in transitioning the backtested factor strategy to live trading using Coinbase APIs.

**Disclaimer:** Live trading involves significant risks, including potential loss of capital. Thorough testing, robust error handling, and careful risk management are essential. This is *not* a complete guide to building a live system but highlights key areas.

1.  **Core Components:**
    *   **Data Feed (Historical & Real-time):**
        *   **Historical Data:** Use `RESTClient` (as in `load_coinbase_data`) to fetch data for periodic factor recalculation (e.g., end-of-day for daily rebalancing).
        *   **Real-time Data (Optional but Recommended):** Use `WSClient` from `python-coinbase-advanced` to get real-time prices for position monitoring, risk checks, and potentially faster execution timing (though the core logic rebalances periodically).
    *   **Strategy Logic Execution:**
        *   Schedule the factor calculation (Steps 4-5) and portfolio construction (Step 6) to run based on your chosen `rebalancing frequency` (e.g., a daily script).
    *   **Order Execution:**
        *   **Calculate Target vs. Current Holdings:** Compare the newly calculated `target_weights` with your current portfolio holdings (fetched via `RESTClient.get_accounts()`).
        *   **Generate Orders:** Determine the necessary buy/sell orders (Market or Limit) to align current holdings with target weights. Calculate order sizes based on target weights, current prices, and available capital/buying power.
        *   **Place Orders:** Use `RESTClient.market_order_buy/sell` or `limit_order_gtc_buy/sell`. Handle potential errors and confirmations.
    *   **Position & Risk Management:**
        *   Continuously or periodically monitor open positions, unrealized P&L, and overall portfolio exposure using REST API calls (`get_accounts`, potentially mapping fills to positions).
        *   Implement pre-trade risk checks (e.g., calculated order size vs. max allowed size, available balance).
        *   Track order statuses (`get_order`) and handle partial fills if using limit orders.
    *   **Infrastructure:**
        *   A reliable server/cloud instance (e.g., AWS EC2, GCP Compute Engine, VPS) to run the bot 24/7.
        *   Robust logging (file-based and potentially external services like Datadog/Sentry).
        *   Monitoring and alerting (e.g., notifications on errors, large P&L swings, connection losses).
        *   Secure management and deployment of API keys (e.g., using cloud secret managers).

2.  **Key Challenges:**
    *   **Data Consistency:** Ensuring historical data used for calculation matches the format and timing of real-time data used for execution.
    *   **Latency:** Delays between fetching data, calculating signals, receiving API confirmation, and market data updates. Can lead to slippage.
    *   **Slippage:** Difference between the expected execution price (e.g., last close used for calculation) and the actual fill price. Market orders on volatile assets are particularly susceptible. Factor expected slippage into backtest assumptions.
    *   **API Rate Limits:** Coinbase imposes limits on requests per second. Implement proper delays and potentially exponential backoff in your API interaction logic.
    *   **API Errors & Downtime:** Handle various HTTP errors, exchange maintenance periods, or unexpected API responses gracefully (e.g., retry logic, circuit breakers).
    *   **Data Feed Reliability:** WebSocket connections can drop. Implement automatic, robust reconnection logic with state synchronization.
    *   **Order Atomicity:** Ensuring that the set of orders needed for rebalancing is executed as intended, even if some individual orders fail or are partially filled.
    *   **Real-time Calculation:** Ensure factor calculations and portfolio logic can run reliably within the rebalancing interval.
    *   **Infrastructure Management:** Keeping the bot running reliably 24/7 requires system administration, monitoring, and maintenance.

3.  **Transition Strategy:**
    *   **Paper Trading:** Strongly recommended. Utilize Coinbase's sandbox environment (check availability and limitations) or a dedicated paper trading simulator that uses live market data to test the *full* live trading logic (data fetching, calculation, order generation, monitoring) without risking real capital.
    *   **Start Small:** Begin live trading with a significantly reduced amount of capital to validate the system's real-world behavior and identify unforeseen issues.
    *   **Monitor Closely:** Initially, manually verify the bot's actions against its logs and expected behavior. Set up alerts for any discrepancies or errors. Gradually increase capital allocation as confidence grows.

---

## Conclusion

This guide provides a comprehensive framework for building a factor-based quantitative strategy using VectorBT Pro and Python 3.11, with specific considerations for using Coinbase data and transitioning towards live trading. Remember that successful quant trading is an iterative process involving rigorous research, careful implementation, robust backtesting, realistic cost/slippage assumptions, and continuous refinement. Leverage tools like Cursor AI to accelerate the coding and analysis stages, allowing you to focus on the core strategic decisions and factor research. Good luck! 