import pandas as pd
import numpy as np
import vectorbtpro as vbt
import logging
from typing import Dict, Tuple, Optional, Any, Union
from tqdm import tqdm
from itertools import product

logger = logging.getLogger(__name__)

class StochSMAStrategy:
    def __init__(self, 
                 initial_capital=10000, 
                 commission_pct=0.001, 
                 slippage_pct=0.0005,
                 use_stops=True, 
                 sl_atr_multiplier=2.0, 
                 tsl_atr_multiplier=2.5, 
                 trend_sma_window=50,
                 **kwargs): # Absorb unused params from optimizer
        """Initialize strategy with fixed parameters."""
        self.initial_capital = initial_capital
        self.commission_pct = commission_pct
        self.slippage_pct = slippage_pct
        self.use_stops = use_stops
        self.sl_atr_multiplier = sl_atr_multiplier
        self.tsl_atr_multiplier = tsl_atr_multiplier
        self.trend_sma_window = trend_sma_window
        logger.info(f"Initialized StochSMAStrategy: Trend={self.trend_sma_window}, Stops={self.use_stops}, SL={self.sl_atr_multiplier}, TSL={self.tsl_atr_multiplier}")

    def run(self, data: pd.DataFrame, stoch_k: int, stoch_d: int, stoch_lower_th: int, stoch_upper_th: int) -> Tuple[pd.Series, pd.Series, Optional[Dict[str, pd.Series]]]:
        """
        Run the StochSMA strategy with fixed parameters and generate entry/exit signals.
        
        Args:
            data: DataFrame with OHLCV data
            stoch_k: Stochastic K period 
            stoch_d: Stochastic D period
            stoch_lower_th: Lower threshold for entry signal
            stoch_upper_th: Upper threshold for exit signal
            
        Returns:
            Tuple of (entry_signals, exit_signals, stops_info)
            where stops_info is a dict containing sl_stop and tsl_stop Series or None
        """
        if data is None or data.empty:
            logger.error("No data provided to run the strategy.")
            return None, None, None
            
        # Extract price series
        close = data['close']
        high = data['high']
        low = data['low']
        
        # Initialize stops and trend filter
        sl_stop_pct = None
        tsl_stop_pct = None
        local_use_stops = self.use_stops
        trend_filter_active = False
        trend_filter_sma = None
        
        # Initialize result variables
        entry_signal = pd.Series(False, index=close.index)
        exit_signal = pd.Series(False, index=close.index)
        
        try:
            # --- 1. Calculate Stop Levels if enabled ---
            if local_use_stops:
                try:
                    atr = vbt.ATR.run(high, low, close, window=14).atr # Default ATR period
                    if atr is not None and not atr.isnull().all():
                        if self.sl_atr_multiplier > 0:
                            sl_stop_pct = (atr * self.sl_atr_multiplier) / close
                            sl_stop_pct = sl_stop_pct.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                        if self.tsl_atr_multiplier > 0:
                            tsl_stop_pct = (atr * self.tsl_atr_multiplier) / close
                            tsl_stop_pct = tsl_stop_pct.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                        if (sl_stop_pct is not None and sl_stop_pct.isnull().all()) or \
                           (tsl_stop_pct is not None and tsl_stop_pct.isnull().all()):
                            logger.warning("Stop calculation resulted in all NaNs, disabling stops.")
                            local_use_stops = False
                            sl_stop_pct = None
                            tsl_stop_pct = None
                    else:
                        logger.warning("ATR calculation failed, disabling stops.")
                        local_use_stops = False
                except Exception as atr_err:
                    logger.warning(f"ATR error: {atr_err}, disabling stops.")
                    local_use_stops = False

            # --- 2. Calculate Trend Filter if enabled ---
            if self.trend_sma_window > 0:
                if self.trend_sma_window < 1 or self.trend_sma_window >= len(close):
                    logger.warning(f"Trend SMA window {self.trend_sma_window} invalid for data len {len(close)}. Filter disabled.")
                else:
                    try:
                        trend_filter_sma = vbt.MA.run(close, window=self.trend_sma_window).ma
                        trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                    except Exception as sma_err:
                        logger.error(f"Trend SMA calculation error: {sma_err}")
                        trend_filter_active = False
                        
            # --- 3. Calculate Stochastic Indicator ---
            logger.info(f"Calculating Stochastic with K={stoch_k}, D={stoch_d}, Lower={stoch_lower_th}, Upper={stoch_upper_th}")
            stoch_k_result = vbt.STOCH.run(
                high, low, close, stoch_k, stoch_d
            ).slow_k

            if stoch_k_result is None or stoch_k_result.isnull().all():
                logger.error("Stochastic calculation failed or returned all NaNs.")
                return entry_signal, exit_signal, None
                
            # --- 4. Generate Base Signals ---
            entry_signal = stoch_k_result.vbt.crossed_above(stoch_lower_th)
            exit_signal = stoch_k_result.vbt.crossed_below(stoch_upper_th)
            
            # --- 5. Apply Trend Filter to Entry Signal ---
            if trend_filter_active:
                # Handle potential leading NaNs in SMA
                valid_trend_idx = trend_filter_sma.dropna().index
                temp_entry = entry_signal.copy()
                temp_entry.loc[:] = False # Default to False
                
                # Only compare where both signals and trend are valid
                common_idx = valid_trend_idx.intersection(entry_signal.index)
                if not common_idx.empty:
                    trend_condition = (close.loc[common_idx] > trend_filter_sma.loc[common_idx])
                    # Apply trend condition only where signals were originally True
                    temp_entry.loc[common_idx] = entry_signal.loc[common_idx] & trend_condition
                    
                entry_signal = temp_entry
                
            # Log signal counts
            entry_count = entry_signal.sum()
            exit_count = exit_signal.sum()
            logger.info(f"Generated {entry_count} entry signals and {exit_count} exit signals.")
            
            # --- 6. Return Signals and Stops ---
            stops_info = None
            if local_use_stops:
                stops_info = {
                    'sl_stop': sl_stop_pct,
                    'tsl_stop': tsl_stop_pct
                }
            
            return entry_signal, exit_signal, stops_info
            
        except Exception as e:
            logger.error(f"Error running StochSMA strategy: {e}", exc_info=True)
            return pd.Series(False, index=close.index), pd.Series(False, index=close.index), None

    def optimize(self, data: pd.DataFrame, param_grid: Dict, optimize_metric: str, granularity_seconds: int = 86400):
        """
        Run vectorized backtest optimization using vectorbtpro.
        (Manual parameter iteration approach)

        Args:
            data: DataFrame with OHLCV data.
            param_grid: Dictionary with parameter names as keys and arrays of values to test.
            optimize_metric: The metric string used by vectorbtpro for ranking.
            granularity_seconds: Data granularity for frequency calculation.

        Returns:
            vectorbtpro Portfolio object or None on error.
        """
        from data.data_fetcher import get_vbt_freq_str  # Import here to avoid circular imports
        
        freq_str = get_vbt_freq_str(granularity_seconds)
        if not freq_str:
            logger.error(f"Invalid granularity seconds ({granularity_seconds}) for freq string. Cannot optimize.")
            return None

        close = data['close']
        high = data['high']
        low = data['low']

        logger.info(f"Running StochSMA optimization with grid (manual iteration): {param_grid}")

        # Initialize variables outside the main try block
        sl_stop_pct = None
        tsl_stop_pct = None
        local_use_stops = self.use_stops
        trend_filter_active = False
        trend_filter_sma = None

        try:
            # --- 1. Calculate Base Indicators (Stops, Trend Filter) --- 
            if local_use_stops:
                try:
                    atr = vbt.ATR.run(high, low, close, window=14).atr # Default ATR period
                    if atr is not None and not atr.isnull().all():
                        if self.sl_atr_multiplier > 0:
                            sl_stop_pct = (atr * self.sl_atr_multiplier) / close
                            sl_stop_pct = sl_stop_pct.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                        if self.tsl_atr_multiplier > 0:
                            tsl_stop_pct = (atr * self.tsl_atr_multiplier) / close
                            tsl_stop_pct = tsl_stop_pct.replace([np.inf, -np.inf], np.nan).ffill().bfill()
                        if (sl_stop_pct is not None and sl_stop_pct.isnull().all()) or \
                           (tsl_stop_pct is not None and tsl_stop_pct.isnull().all()):
                            logger.warning("Stop calculation resulted in all NaNs, disabling stops.")
                            local_use_stops = False
                            sl_stop_pct = None
                            tsl_stop_pct = None
                    else:
                        logger.warning("ATR calculation failed, disabling stops.")
                        local_use_stops = False
                except Exception as atr_err:
                    logger.warning(f"ATR error: {atr_err}, disabling stops.")
                    local_use_stops = False

            if self.trend_sma_window > 0:
                if self.trend_sma_window < 1 or self.trend_sma_window >= len(close):
                    logger.warning(f"Trend SMA window {self.trend_sma_window} invalid for data len {len(close)}. Filter disabled.")
                else:
                    try:
                        trend_filter_sma = vbt.MA.run(close, window=self.trend_sma_window).ma
                        trend_filter_active = trend_filter_sma is not None and not trend_filter_sma.isnull().all()
                    except Exception as sma_err:
                        logger.error(f"Trend SMA calculation error: {sma_err}")
                        trend_filter_active = False

            # --- 2. Generate Parameter Combinations ---
            # Ensure correct keys are present in param_grid
            required_keys = ['stoch_k', 'stoch_d', 'stoch_lower_th', 'stoch_upper_th']
            if not all(key in param_grid for key in required_keys):
                logger.error(f"Missing required keys in param_grid for StochSMA: {required_keys}")
                return None
                
            param_names = required_keys # Use defined order
            param_arrays = [param_grid[key] for key in param_names]
            param_combinations = list(product(*param_arrays))
            logger.info(f"Generated {len(param_combinations)} parameter combinations manually.")

            all_entries = []
            all_exits = []

            # --- 3. Loop Through Combinations and Generate Signals ---
            for k_w, d_w, lower_th, upper_th in tqdm(param_combinations, desc="Simulating StochSMA"):
                try:
                    # Calculate indicator for this specific combination
                    stoch_k = vbt.STOCH.run(
                        high, low, close, k_w, d_w # Use positional args k_w, d_w
                    ).slow_k

                    if stoch_k.isnull().all():
                        all_entries.append(pd.Series(False, index=close.index))
                        all_exits.append(pd.Series(False, index=close.index))
                        continue
                
                    # Generate signals
                    entry_signal = stoch_k.vbt.crossed_above(lower_th)
                    exit_signal = stoch_k.vbt.crossed_below(upper_th)

                    # Apply trend filter
                    if trend_filter_active:
                        # Ensure trend_filter_sma is aligned with close index before comparison
                        # Handle potential leading NaNs in SMA
                        valid_trend_idx = trend_filter_sma.dropna().index
                        temp_entry = entry_signal.copy()
                        temp_entry.loc[:] = False # Default to False
                        
                        # Only compare where both signals and trend are valid
                        common_idx = valid_trend_idx.intersection(entry_signal.index)
                        if not common_idx.empty:
                            trend_condition = (close.loc[common_idx] > trend_filter_sma.loc[common_idx])
                            # Apply trend condition only where signals were originally True
                            temp_entry.loc[common_idx] = entry_signal.loc[common_idx] & trend_condition
                            
                        entry_signal = temp_entry

                    all_entries.append(entry_signal)
                    all_exits.append(exit_signal)

                except Exception as loop_err:
                    logger.warning(f"Error in loop for params ({k_w},{d_w},{lower_th},{upper_th}): {loop_err}. Appending False signals.")
                    all_entries.append(pd.Series(False, index=close.index))
                    all_exits.append(pd.Series(False, index=close.index))

            if not all_entries:
                logger.error("No signals generated for any parameter combination.")
                return None
                
            # --- 4. Combine Signals ---
            param_multi_index = pd.MultiIndex.from_tuples(param_combinations, names=param_names)
            entries_output = pd.concat(all_entries, axis=1, keys=param_multi_index)
            exits_output = pd.concat(all_exits, axis=1, keys=param_multi_index)

            # --- 5. Run Portfolio Simulation ---
            pf_kwargs = {
                'close': close,
                'entries': entries_output,
                'exits': exits_output,
                'freq': freq_str,
                'init_cash': self.initial_capital,
                'fees': self.commission_pct,
                'slippage': self.slippage_pct,
            }

            if local_use_stops:
                if sl_stop_pct is not None and sl_stop_pct.notna().any():
                    pf_kwargs['sl_stop'] = sl_stop_pct
                if tsl_stop_pct is not None and tsl_stop_pct.notna().any():
                    pf_kwargs['tsl_stop'] = tsl_stop_pct

            logger.info(f"Running Portfolio.from_signals with {entries_output.shape[1]} parameter combinations.")
            pf = vbt.Portfolio.from_signals(**pf_kwargs)
            logger.info("Portfolio simulation complete.")

            # --- 6. Return Portfolio Object ---
            return pf

        except Exception as e:
            logger.error(f"Error during StochSMA optimization: {e}", exc_info=True)
            return None 