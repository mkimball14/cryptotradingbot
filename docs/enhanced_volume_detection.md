# Enhanced Volume Detection

This document describes the enhanced volume detection implementation in the `EdgeMultiFactorStrategy`.

## Overview

The volume detection algorithm has been enhanced to provide more sensitive and reliable volume confirmation signals. This is especially useful for detecting breakouts and trend reversals that are supported by volume.

## Key Improvements

1. **Multiple Volume Indicators**: The enhanced system now uses multiple indicators to confirm volume signals:
   - Relative volume compared to lookback period moving average
   - Relative volume compared to short-term moving average
   - Rate of change in volume (momentum)
   - Consecutive increasing volume bars

2. **Adjustable Thresholds**: The volume detection system now accepts these configurable parameters:
   - `volume_threshold`: Main volume ratio threshold (default: 1.1)
   - `volume_threshold_short`: Short-term volume ratio threshold (default: 1.05)
   - `volume_roc_threshold`: Rate of change threshold for volume (default: 0.1)

3. **More Sensitive Detection**: The thresholds have been lowered from previous settings to trigger more often, with focus on true positive signals.

4. **Market Regime Awareness**: Volume thresholds are dynamically adjusted based on market conditions:
   - During trending markets: Thresholds are increased by 20% to reduce false signals
   - During ranging markets: Thresholds are decreased by 15% to detect early breakouts
   - Adjustments apply to all volume metrics (ratio thresholds and ROC threshold)

## Using Enhanced Volume Detection

### Using the Enhanced Volume Profile

The strategy includes a new parameter profile called `enhanced_volume` that is optimized for the enhanced volume detection algorithm:

```bash
python scripts/strategies/edge_multi_factor_fixed.py --profile enhanced_volume --symbol BTC-USD
```

### Enhanced Volume Profile Configuration

```json
"enhanced_volume": {
  "description": "Parameters optimized for the enhanced volume detection algorithm with multiple confirmation sources",
  "lookback_window": 12,
  "vol_filter_window": 48,
  "volatility_threshold": 0.75,
  "signal_threshold": 0.15,
  "volume_threshold": 1.1,
  "volume_threshold_short": 1.05,
  "volume_roc_threshold": 0.1,
  "default_factor_weights": {
    "volatility_regime": 0.2,
    "consolidation_breakout": 0.2,
    "volume_divergence": 0.35,
    "market_microstructure": 0.25
  }
}
```

### Testing the Enhanced Volume Detection

A test script is provided to compare the enhanced volume detection with the original algorithm:

```bash
python scripts/test_enhanced_volume.py
```

This will generate a comparison plot showing the differences between the regime-aware and standard volume detection approaches.

## Implementation Details

The enhanced volume detection is implemented in the `create_volume_divergence_indicator` function in `scripts/strategies/edge_multi_factor_fixed.py`. The function now accepts more parameters and uses a more sophisticated approach to detect significant volume events.

### Market Regime Integration

The volume detection now takes into account whether the market is trending or ranging:

```python
# Apply market regime-based threshold adjustments
if is_trending is not None and is_ranging is not None:
    # Make volume thresholds more strict during trending periods (reduce false signals)
    trending_adjustment = 1.2  # Increase threshold by 20% during trends
    ranging_adjustment = 0.85  # Decrease threshold by 15% during ranges
    
    # Apply adjustments based on market regimes
    adapted_volume_threshold[is_trending] *= trending_adjustment
    adapted_volume_threshold[is_ranging] *= ranging_adjustment
```

This adaptive approach:
- Reduces false signals in trending markets (higher thresholds)
- Enhances sensitivity in ranging markets (lower thresholds)
- Ensures appropriate sensitivity regardless of market conditions

### Key Code Snippets

```python
# Calculate volume rate of change
volume_roc = volume.pct_change(3).fillna(0)  # 3-period rate of change
volume_increasing = volume_roc > adapted_roc_threshold  # ROC threshold

# Detect consecutive increasing volume (2 or more bars)
vol_change = volume.diff().fillna(0)
consecutive_increasing = (vol_change > 0) & (vol_change.shift(1) > 0)

# More sensitive volume confirmation using multiple indicators
volume_confirms_up = (
    (vol_ratio_vol > adapted_volume_threshold) | 
    (vol_ratio_short > adapted_volume_threshold_short) | 
    volume_increasing | 
    consecutive_increasing
) & breakout_up
```

## Recommended Use Cases

The enhanced volume detection is particularly effective for:

1. **Crypto assets with high volatility** - These often have significant volume spikes that can be better detected
2. **Breakout trading strategies** - Volume confirmation is critical for valid breakouts
3. **Short-term trading** - More sensitive volume detection helps with timely entries
4. **Range-bound markets** - Detecting volume expansion when price breaks from consolidation
5. **Adaptive trading systems** - Systems that need to adjust to changing market dynamics

## Benefits of Market Regime Awareness

1. **Reduced false signals during trends** - By increasing thresholds during trending markets
2. **Earlier breakout detection in ranges** - By lowering thresholds during ranging markets
3. **Better signal quality** - By adapting to the specific market conditions
4. **Improved win rate** - By focusing on the highest probability trading setups in each regime 