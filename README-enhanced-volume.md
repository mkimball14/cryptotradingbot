# Enhanced Volume Detection for Crypto Trading Bot

## Overview

This project implements an enhanced volume detection system for the Crypto Trading Bot's EdgeMultiFactorStrategy. The enhancements provide more sensitive and reliable volume signals for identifying breakouts and trend confirmations.

## Key Features

- **Multi-factor volume detection**: Combines different volume indicators for stronger confirmation
- **Adjustable sensitivity parameters**: Fine-tune detection to match market conditions
- **Better breakout detection**: More reliable identification of valid breakouts with volume confirmation
- **Customized parameter profile**: Pre-configured settings optimized for volume-based trading

## Implementation Details

The enhanced volume detection system consists of:

1. **Core Components:**
   - Updated `create_volume_divergence_indicator` function in `edge_multi_factor_fixed.py`
   - New `enhanced_volume` parameter profile in `config/strategy_params.json`
   - Test script in `scripts/test_enhanced_volume.py`
   - Documentation in `docs/enhanced_volume_detection.md` and `docs/enhanced_volume_test_results.md`

2. **Volume Indicators Used:**
   - Volume ratio compared to lookback moving average
   - Volume ratio compared to short-term moving average
   - Volume Rate of Change (ROC)
   - Consecutive volume increases

3. **Parameter Configuration:**
   - `volume_threshold`: 1.1 (main volume ratio threshold)
   - `volume_threshold_short`: 1.05 (short-term MA volume ratio threshold)
   - `volume_roc_threshold`: 0.1 (rate of change threshold)

## How to Use

### Running with Enhanced Volume Profile

```bash
python scripts/strategies/edge_multi_factor_fixed.py --profile enhanced_volume --symbol BTC-USD
```

### Testing the Enhanced Volume Detection

```bash
python scripts/test_enhanced_volume.py
```

This will:
1. Run both enhanced and original volume detection algorithms
2. Generate a visual comparison of the signals
3. Create performance metrics for analysis
4. Save comparison visualizations to `enhanced_vs_original_volume.png`

### Customizing Parameters

You can modify the parameters in `config/strategy_params.json` to adjust sensitivity:

```json
"enhanced_volume": {
  "volume_threshold": 1.1,        // Increase for less sensitivity, decrease for more
  "volume_threshold_short": 1.05, // Short-term threshold
  "volume_roc_threshold": 0.1     // Rate of change threshold
}
```

## Results Summary

Testing shows the enhanced volume detection generates approximately 7.4% more signals than the original algorithm, with significant improvements in early detection of volume spikes. For detailed results, see `docs/enhanced_volume_test_results.md`.

## Future Development

Planned improvements include:
1. Adaptive volume thresholds based on market conditions
2. Time-based filtering to focus on high-liquidity periods
3. Market regime-specific volume sensitivity
4. Volume-based exit strategies

## Documentation

- `docs/enhanced_volume_detection.md`: Technical implementation details
- `docs/enhanced_volume_test_results.md`: Test results and analysis
- `docs/strategy_architecture.md`: Overall strategy architecture 