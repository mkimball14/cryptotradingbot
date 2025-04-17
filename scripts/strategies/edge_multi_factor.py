import vectorbtpro as vbt
import numpy as np
import pandas as pd
import sys
import os
import logging
from pathlib import Path
import argparse
from datetime import datetime
import itertools

# --- Basic Setup ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# --- Import centralized data fetcher ---
try:
    from data.data_fetcher import fetch_historical_data, get_granularity_str, get_vbt_freq_str, GRANULARITY_MAP_SECONDS
    logger = logging.getLogger(__name__)
    logger.info("Successfully imported data_fetcher.")
except ImportError as e:
    print(f"WARNING: Could not import data_fetcher: {e}. Main block requires it.")
    def fetch_historical_data(*args, **kwargs):
        print("ERROR: fetch_historical_data is not available.")
        return None
    GRANULARITY_MAP_SECONDS = {'1h': 3600, '1d': 86400}
    def get_vbt_freq_str(*args, **kwargs): return "1h"

# ==============================================================================
# Factor Indicator Functions (Plain Python/Numba)
# ==============================================================================

def create_volatility_regime_indicator(close, lookback_window, vol_filter_window, volatility_threshold):
    """Calculates the volatility regime signal."""
    returns = close.pct_change()
    vol = returns.vbt.rolling_std(window=lookback_window, minp=lookback_window // 2)
    vol_ma = vol.vbt.rolling_mean(window=vol_filter_window, minp=vol_filter_window // 2)
    vol_ma_safe = vol_ma.replace(0, np.nan).ffill().bfill()
    vol_ratio = (vol / vol_ma_safe).fillna(1.0)
    vol_compressed = vol_ratio < volatility_threshold
    vol_expansion = vol_ratio.diff().fillna(0) > 0
    vol_signal = vol_compressed.shift(1).fillna(False) & vol_expansion
    return vol_signal

def create_consolidation_breakout_indicator(high, low, close, lookback_window):
    """Calculates consolidation breakout signals."""
    hl_range = (high - low) / close.replace(0, np.nan)
    hl_range_ma = hl_range.vbt.rolling_mean(window=lookback_window, minp=lookback_window // 2)
    is_consolidating = hl_range < hl_range_ma * 0.8
    upper_level = high.vbt.rolling_max(window=lookback_window, minp=lookback_window // 2)
    lower_level = low.vbt.rolling_min(window=lookback_window, minp=lookback_window // 2)
    upper_level_shifted = upper_level.shift(1).bfill()
    lower_level_shifted = lower_level.shift(1).bfill()
    is_consolidating_shifted = is_consolidating.shift(1).fillna(False)
    breakout_up = (close > upper_level_shifted) & is_consolidating_shifted
    breakout_down = (close < lower_level_shifted) & is_consolidating_shifted
    return breakout_up, breakout_down

def create_volume_divergence_indicator(volume, lookback_window, breakout_up, breakout_down):
    """Calculates volume confirmation signals based on pre-calculated breakouts."""
    volume_ma = volume.vbt.rolling_mean(window=lookback_window, minp=lookback_window // 2)
    volume_ma_safe = volume_ma.replace(0, np.nan).ffill().bfill()
    vol_ratio_vol = (volume / volume_ma_safe).fillna(1.0)
    volume_confirms_up = (vol_ratio_vol > 1.5) & breakout_up
    volume_confirms_down = (vol_ratio_vol > 1.5) & breakout_down
    return volume_confirms_up, volume_confirms_down

def create_market_microstructure_indicator(open, high, low, close):
    """Calculates market microstructure signals (candle shadows)."""
    upper_shadow = high - np.maximum(open, close)
    lower_shadow = np.minimum(open, close) - low
    hl_range_nonzero = (high - low).replace(0, np.nan)
    shadow_ratio = ((upper_shadow - lower_shadow) / hl_range_nonzero).fillna(0)
    buying_pressure = shadow_ratio < -0.5
    selling_pressure = shadow_ratio > 0.5
    return buying_pressure, selling_pressure

# ==============================================================================
# Combined Indicator Factory (Using plain functions)
# ==============================================================================

# --- REMOVING IndicatorFactory definition due to persistent errors ---
# EdgeFactors = vbt.IndicatorFactory(...)

# ==============================================================================
# Strategy Class using the Indicator Factory
# ==============================================================================
class EdgeMultiFactorStrategy:
    """
    Combines signals using the EdgeFactors indicator factory.
    """
    def __init__(self,
                 lookback_window=20,
                 vol_filter_window=100,
                 volatility_threshold=0.5,
                 initial_capital=3000,
                 default_factor_weights=None,
                 commission_pct=0.001,
                 slippage_pct=0.0005):

        self.lookback_window = int(lookback_window)
        self.vol_filter_window = int(vol_filter_window)
        self.volatility_threshold = float(volatility_threshold)
        self.initial_capital = float(initial_capital)
        self.commission_pct = float(commission_pct)
        self.slippage_pct = float(slippage_pct)

        if default_factor_weights is None:
            self.factor_weights = {
                'volatility_regime': 0.25,
                'consolidation_breakout': 0.25,
                'volume_divergence': 0.25,
                'market_microstructure': 0.25
            }
        else:
            total_weight = sum(default_factor_weights.values())
            if not np.isclose(total_weight, 1.0):
                print(f"Warning: Provided weights sum to {total_weight}, normalizing.")
                self.factor_weights = {k: v / total_weight for k, v in default_factor_weights.items()}
            else:
                self.factor_weights = default_factor_weights
        if not (0 < self.volatility_threshold < 1):
             raise ValueError("volatility_threshold must be between 0 and 1")
        if self.lookback_window <= 0 or self.vol_filter_window <= 0:
             raise ValueError("Window parameters must be positive integers")
        if self.initial_capital <= 0:
             raise ValueError("Initial capital must be positive")

    def generate_signals(self, data: pd.DataFrame):
        """
        Generates entry signals by directly calling factor functions.
        """
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"Data missing required columns: {set(required_cols) - set(data.columns)}")

        min_required_data = max(self.lookback_window, self.vol_filter_window) + 5
        # Use data directly, no need to copy if not modifying in place
        # price_data = data[required_cols].copy() 
        
        if len(data) < min_required_data:
             print(f"Warning: Data length ({len(data)}) might be insufficient for lookbacks ({min_required_data}).")

        # --- Call indicator functions directly ---
        vol_signal = create_volatility_regime_indicator(
            data['close'], 
            lookback_window=self.lookback_window,
            vol_filter_window=self.vol_filter_window,
            volatility_threshold=self.volatility_threshold
        )
        
        breakout_up, breakout_down = create_consolidation_breakout_indicator(
            data['high'], data['low'], data['close'], 
            lookback_window=self.lookback_window
        )
        
        volume_confirms_up, volume_confirms_down = create_volume_divergence_indicator(
            data['volume'],
            lookback_window=self.lookback_window,
            breakout_up=breakout_up, # Pass calculated result
            breakout_down=breakout_down # Pass calculated result
        )
        
        buying_pressure, selling_pressure = create_market_microstructure_indicator(
            data['open'], data['high'], data['low'], data['close']
        )
        # --- Combine signals using weights ---
        long_signal = pd.Series(0.0, index=data.index)
        short_signal = pd.Series(0.0, index=data.index)
        
        # Ensure results are float/boolean before weighting
        long_signal += vol_signal.astype(float) * self.factor_weights.get('volatility_regime', 0)
        long_signal += breakout_up.astype(float) * self.factor_weights.get('consolidation_breakout', 0)
        long_signal += volume_confirms_up.astype(float) * self.factor_weights.get('volume_divergence', 0)
        long_signal += buying_pressure.astype(float) * self.factor_weights.get('market_microstructure', 0)
        
        # Note: vol_signal might contribute to both long and short if desired, 
        # but current logic implies directionality in other factors.
        # If vol_signal is purely a filter, it might be applied differently.
        # Assuming original weighting logic for now:
        short_signal += vol_signal.astype(float) * self.factor_weights.get('volatility_regime', 0) # Re-evaluate if vol_signal should impact shorts
        short_signal += breakout_down.astype(float) * self.factor_weights.get('consolidation_breakout', 0)
        short_signal += volume_confirms_down.astype(float) * self.factor_weights.get('volume_divergence', 0)
        short_signal += selling_pressure.astype(float) * self.factor_weights.get('market_microstructure', 0)

        signal_threshold = 0.5 
        long_entries = long_signal > signal_threshold
        short_entries = short_signal > signal_threshold
        
        # Prevent simultaneous entries
        simultaneous = long_entries & short_entries
        long_entries[simultaneous] = False
        short_entries[simultaneous] = False
        
        return long_entries, short_entries

    def calculate_target_amount(self, data: pd.DataFrame, risk_fraction=0.01, atr_window=14, atr_multiple_stop=2.0):
        """
        Calculates the target position size as a dollar amount,
        based on volatility (ATR), risk fraction, and initial capital.
        Returns a Series of target dollar amounts aligned with the data index.
        """
        if data.empty:
            print("Error: Cannot calculate target amount on empty data.")
            return pd.Series(0.0, index=data.index)
        close = data['close']
        high = data['high']
        low = data['low']
        
        # Calculate ATR and stop distance in price terms
        atr = vbt.ATR.run(
            high, low, close,
            window=int(atr_window),
            wtype='wilder'
        ).atr.bfill().ffill()
        stop_distance = (atr * float(atr_multiple_stop)).replace(0, np.nan).ffill().bfill()
        
        # Calculate dollar amount to risk (using initial capital as proxy for current equity)
        dollar_risk = self.initial_capital * float(risk_fraction)
        
        # Calculate target size in base asset units, handle potential division by zero
        # Ensure stop_distance is not zero before dividing
        safe_stop_distance = stop_distance.replace(0, np.nan) # Avoid division by zero
        target_amount_asset = (dollar_risk / safe_stop_distance).fillna(0) 
        
        # Convert asset amount to quote currency amount
        target_amount_quote = (target_amount_asset * close).fillna(0)
        
        # Optional: Apply a maximum position size based on capital (e.g., max 25% of initial capital)
        max_target_amount_quote = self.initial_capital * 0.25 
        target_amount_quote = np.minimum(target_amount_quote, max_target_amount_quote)
        
        # Ensure no invalid values (e.g., negative sizes if logic allows)
        target_amount_quote = target_amount_quote.clip(lower=0)
        
        return target_amount_quote

    def optimize(self, data, param_grid, optimize_metric='sharpe_ratio',
                 risk_fraction=0.01, atr_window=14, atr_multiple=2.0,
                 weight_opt_steps=4,
                 verbose=True):
        """
        Optimization loop using the refactored strategy.
        Uses TargetPercent sizing.
        """
        if data.empty:
            if verbose: print("Error: Cannot optimize on empty data.")
            return None

        if verbose: print(f"Starting optimization with metric: {optimize_metric}")

        factor_names = ['volatility_regime', 'consolidation_breakout', 'volume_divergence', 'market_microstructure']
        optimize_weights_param = param_grid.get('factor_weights', 'auto')
        weight_combinations = []
        if optimize_weights_param == 'auto':
            if verbose: print(f"Generating weight combinations with {weight_opt_steps} steps...")
            step = 1.0 / weight_opt_steps
            points = [i * step for i in range(weight_opt_steps + 1)]
            for combo in itertools.product(points, repeat=len(factor_names)):
                if np.isclose(sum(combo), 1.0):
                    weight_combinations.append(dict(zip(factor_names, combo)))
            if not weight_combinations:
                weight_combinations.append({f: 1.0/len(factor_names) for f in factor_names})
            if verbose: print(f"Optimizing over {len(weight_combinations)} weight combinations.")
        elif isinstance(optimize_weights_param, list):
            weight_combinations = optimize_weights_param
            if verbose: print(f"Optimizing over {len(weight_combinations)} provided weight combinations.")
        else:
            weight_combinations = [None]
            if verbose: print("Factor weights optimization skipped. Using default weights.")
        param_ranges = {
            'lookback_window': param_grid.get('lookback_window', [self.lookback_window]),
            'volatility_threshold': param_grid.get('volatility_threshold', [self.volatility_threshold]),
            'tsl_stop': param_grid.get('tsl_stop', [0.05]),
            'tp_stop': param_grid.get('tp_stop', [0]), 
            'atr_multiple_sl': param_grid.get('atr_multiple_sl', [atr_multiple]), 
            'factor_weights': weight_combinations
        }
        keys = list(param_ranges.keys())
        values = [param_ranges[key] for key in keys]
        full_param_list = [dict(zip(keys, combo_values)) for combo_values in itertools.product(*values)]
        if verbose: print(f"Total optimization runs planned: {len(full_param_list)}")
        best_score = -np.inf
        best_params = None
        run_count = 0
        fixed_atr_window = True
        if 'atr_window' in param_grid:
            fixed_atr_window = False 
            logger.warning("Optimizing atr_window, ATR will be recalculated in each optimization step.")
            atr_series = None
        else:
            atr_series = vbt.ATR.run(
                data['high'], data['low'], data['close'],
                window=int(atr_window), wtype='wilder'
            ).atr.bfill().ffill()

        for params in full_param_list:
            run_count += 1
            if verbose and run_count % 50 == 0:
                print(f"Running optimization {run_count}/{len(full_param_list)}...")
            try:
                current_lookback = params['lookback_window']
                current_vol_thresh = params['volatility_threshold']
                current_weights = params['factor_weights']
                current_tsl = params['tsl_stop']
                current_tp = params['tp_stop']
                current_atr_mult_sl = params['atr_multiple_sl']
                current_atr_window = params.get('atr_window', atr_window)
                if not fixed_atr_window:
                    current_atr = vbt.ATR.run(
                        data['high'], data['low'], data['close'],
                        window=int(current_atr_window), wtype='wilder'
                    ).atr.bfill().ffill()
                else:
                    current_atr = atr_series
                temp_strategy = EdgeMultiFactorStrategy(
                    lookback_window=current_lookback,
                    vol_filter_window=self.vol_filter_window,
                    volatility_threshold=current_vol_thresh,
                    initial_capital=self.initial_capital,
                    default_factor_weights=current_weights,
                    commission_pct=self.commission_pct,
                    slippage_pct=self.slippage_pct
                )
                current_data = data.copy()
                long_entries, short_entries = temp_strategy.generate_signals(current_data)
                if long_entries.sum() + short_entries.sum() == 0:
                    continue
                target_amount = temp_strategy.calculate_target_amount(
                    current_data,
                    risk_fraction=risk_fraction,
                    atr_window=current_atr_window, 
                    atr_multiple_stop=current_atr_mult_sl
                )
                sl_stop_dist = (current_atr * float(current_atr_mult_sl))
                sl_stop_pct = (sl_stop_dist / current_data['close']).replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(0)
                sl_stop_pct = np.clip(sl_stop_pct, 0.001, 0.5)
                granularity_seconds = (current_data.index[1] - current_data.index[0]).total_seconds()
                vbt_freq = get_vbt_freq_str(granularity_seconds) or pd.infer_freq(current_data.index)
                pf = vbt.Portfolio.from_signals(
                    current_data,
                    entries=long_entries,
                    short_entries=short_entries,
                    sl_stop=sl_stop_pct,
                    tsl_stop=current_tsl if current_tsl > 0 else None,
                    tp_stop=current_tp if current_tp > 0 else None,
                    size=target_amount,
                    size_type='Amount',
                    init_cash=temp_strategy.initial_capital,
                    fees=temp_strategy.commission_pct,
                    slippage=temp_strategy.slippage_pct,
                    freq=vbt_freq,
                    save_returns=True,
                    accumulate=False,
                    stop_exit_type='close'
                )
                stats = pf.stats()
                current_score = -np.inf
                metric_value = stats.get(optimize_metric)
                if metric_value is None and optimize_metric != 'Sharpe Ratio':
                    if verbose: print(f"Warning: Metric '{optimize_metric}' not found. Falling back to Sharpe Ratio.")
                    metric_value = stats.get('Sharpe Ratio')
                if metric_value is not None and np.isfinite(metric_value):
                    current_score = -abs(metric_value) if optimize_metric == 'max_drawdown' else metric_value
                elif verbose:
                    print(f"Warning: Invalid score for metric '{optimize_metric}'. Params: {params}")
                if current_score > best_score:
                    best_score = current_score
                    best_params = params
                    if verbose:
                        print(f"New best score ({optimize_metric}): {current_score:.4f} with params: {best_params}")
            except Exception as e:
                if verbose:
                    print(f"Error optimizing params {params}: {e}")
                continue
        if best_params is not None:
            if verbose:
                display_score = -best_score if optimize_metric == 'max_drawdown' else best_score
                print(f"Optimization complete. Best {optimize_metric}: {display_score:.4f}")
                print(f"Best Parameters found: {best_params}")
        elif verbose:
            print("Optimization failed to find valid parameters.")
        return best_params

# --- Main block for single run testing ---
if __name__ == "__main__":
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description='Backtest EdgeMultiFactorStrategy.')
    parser.add_argument('--symbol', type=str, default='BTC-USD', help='Symbol to backtest')
    parser.add_argument('--start_date', type=str, default='2023-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--granularity', type=str, default='1h', help='Data granularity (e.g., 1h, 4h, 1d)')
    parser.add_argument('--initial_capital', type=float, default=3000, help='Initial capital')
    parser.add_argument('--commission', type=float, default=0.001, help='Commission per trade')
    parser.add_argument('--slippage', type=float, default=0.0005, help='Slippage per trade')
    parser.add_argument('--lookback', type=int, default=20, help='Lookback window for factors')
    parser.add_argument('--vol_filter', type=int, default=100, help='Lookback window for volatility MA filter')
    parser.add_argument('--vol_thresh', type=float, default=0.5, help='Volatility ratio threshold')
    parser.add_argument('--plot', action='store_true', help='Generate and show plot')
    parser.add_argument('--log', action='store_true', help='Enable basic logging')
    parser.add_argument('--risk_fraction', type=float, default=0.01, help='Fraction of capital to risk per trade')
    parser.add_argument('--atr_window', type=int, default=14, help='ATR window for stop loss calculation')
    parser.add_argument('--tsl_stop', type=float, default=0.05, help='Trailing stop loss percentage. Set to 0 to disable.')
    parser.add_argument('--atr_multiple_sl', type=float, default=2.0, help='ATR multiple for fixed SL calculation and sizing %')
    parser.add_argument('--tp_stop', type=float, default=0.10, help='Fixed take profit percentage. Set to 0 to disable.')

    args = parser.parse_args()

    if args.log:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.info("Logging enabled.")

    # --- Data Fetching ---
    granularity_seconds = GRANULARITY_MAP_SECONDS.get(args.granularity.lower())
    if granularity_seconds is None:
        print(f"Error: Unsupported granularity: {args.granularity}.")
        sys.exit(1)
    print(f"Fetching data for {args.symbol} from {args.start_date} to {args.end_date} ({args.granularity})...")
    price_data = fetch_historical_data(args.symbol, args.start_date, args.end_date, granularity_seconds)
    if price_data is None or price_data.empty:
        print("Failed to fetch data. Exiting.")
        sys.exit(1)
    print(f"Data fetched successfully. Shape: {price_data.shape}")
    price_data.index = pd.to_datetime(price_data.index, utc=True)

    # --- REMOVE Simple Factory Test --- 
    # print("\n--- Running Simple Factory Test ---")
    # ... (Removed test block) ...
    # Remove this potentially problematic commented line
    # print("--- End Simple Factory Test ---\n") 
    # --- End Simple Factory Test ---

    # --- Strategy Initialization ---
    print("Initializing EdgeMultiFactorStrategy...")
    # Use original parameter names now, factory is gone
    strategy = EdgeMultiFactorStrategy(
        lookback_window=args.lookback,
        vol_filter_window=args.vol_filter,
        volatility_threshold=args.vol_thresh,
        initial_capital=args.initial_capital,
        commission_pct=args.commission,
        slippage_pct=args.slippage
    )

    # --- Signal Generation --- 
    print("Generating signals...")
    long_entries, short_entries = strategy.generate_signals(price_data)
    if long_entries.sum() + short_entries.sum() == 0:
        print("No entry signals generated.")
        sys.exit(0)

    # --- Calculate Target Amount Size ---
    print("Calculating target amount size...")
    target_amount = strategy.calculate_target_amount(
        price_data,
        risk_fraction=args.risk_fraction,
        atr_window=args.atr_window,
        atr_multiple_stop=args.atr_multiple_sl
    )

    # Calculate ATR-based SL % for Portfolio call (still needed for sl_stop)
    atr = vbt.ATR.run(
        price_data['high'], price_data['low'], price_data['close'],
        window=args.atr_window, wtype='wilder'
    ).atr.bfill().ffill()
    sl_stop_dist = (atr * args.atr_multiple_sl)
    sl_stop_pct = (sl_stop_dist / price_data['close']).replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
    sl_stop_pct = np.clip(sl_stop_pct, 0.001, 0.5)

    # --- Run Backtest ---
    print(f"Running backtest with TargetAmount Sizing, SL (ATR*{args.atr_multiple_sl}), TSL ({args.tsl_stop*100:.2f}%), TP ({args.tp_stop*100:.2f}%)...")
    vbt_freq = get_vbt_freq_str(granularity_seconds) or pd.infer_freq(price_data.index)

    portfolio = vbt.Portfolio.from_signals(
        price_data['close'], # Use close price for portfolio evaluation
        entries=long_entries,
        short_entries=short_entries,
        sl_stop=sl_stop_pct, # Keep SL % for stop loss mechanism
        tsl_stop=args.tsl_stop if args.tsl_stop > 0 else None,
        tp_stop=args.tp_stop if args.tp_stop > 0 else None,
        size=target_amount, # Use calculated dollar amount
        size_type='Amount', # Set size type to Amount
        init_cash=strategy.initial_capital,
        fees=strategy.commission_pct,
        slippage=strategy.slippage_pct,
        freq=vbt_freq,
        # size_granularity might need adjustment for Amount type
        # Check docs if size_granularity applies to Amount or just TargetPercent/Value
        # Let's comment it out for now if unsure
        # size_granularity=SIZE_GRANULARITY, 
        save_returns=True,
        accumulate=False,
        stop_exit_type='close'
    )

    # --- Results --- 
    print("--- Backtest Results ---")
    stats = portfolio.stats()
    print(stats)

    # --- Plotting ---
    if args.plot:
        print("Generating plot...")
        try:
            fig = portfolio.plot(settings=dict(bm_returns=False))
            fig.show()
            fig_dd = portfolio.plot_drawdowns()
            fig_dd.show()
            fig_trades = portfolio.trades.plot()
            fig_trades.show()
        except Exception as plot_err:
            print(f"Error generating plot: {plot_err}")

    print("Script finished.") 