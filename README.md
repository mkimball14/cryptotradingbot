# Trading Signal Confirmation System

A robust system for confirming trading signals based on supply and demand zones, technical indicators, and volume analysis.

## Overview

The Signal Confirmation System is designed to validate potential trading opportunities by analyzing multiple factors:

1. Supply and Demand Zones
2. Technical Indicators (RSI, MACD)
3. Volume Profile Analysis
4. Zone Freshness and Historical Performance

## Components

### 1. Signal Manager (`app/core/signal_manager.py`)

The main component that orchestrates signal confirmation. It:
- Evaluates multiple confirmation factors
- Calculates confidence scores
- Provides a final confirmation decision

Key features:
- RSI divergence detection with overbought/oversold conditions
- Volume profile analysis with POC and value area
- MACD trend confirmation
- Zone freshness evaluation

### 2. Zone Model (`app/models/zone.py`)

Represents supply and demand zones in the market. Features:
- Price boundaries (high/low)
- Zone type (supply/demand)
- Formation data (volume, candles)
- Strength tracking
- Age-based validation
- Zone merging capabilities

### 3. Technical Indicators (`app/core/indicators.py`)

Collection of technical analysis tools:
- RSI calculation with divergence detection
- MACD with signal line crossovers
- Volume Profile with POC and value area calculation

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: TA-Lib is required. Installation instructions:
- macOS: `brew install ta-lib`
- Linux: `apt-get install ta-lib`
- Windows: Download and install from [TA-Lib](https://ta-lib.org)

## Usage

### Basic Signal Confirmation

```python
from app.core.signal_manager import SignalManager
from app.models.zone import Zone
import pandas as pd

# Initialize components
signal_manager = SignalManager(risk_manager)

# Create a zone
supply_zone = Zone(
    id="zone_1",
    zone_type="supply",
    price_high=120.0,
    price_low=118.0
)

# Get OHLCV data
ohlcv_data = pd.DataFrame(...)  # Your OHLCV data

# Confirm signal
confirmation = await signal_manager.confirm_zone_signal(
    zone=supply_zone,
    ohlcv_data=ohlcv_data
)

if confirmation.is_confirmed:
    print(f"Signal confirmed with {confirmation.confidence_score:.2%} confidence")
    print("Confirmation factors:", confirmation.confirmation_factors)
```

### Zone Management

```python
# Create zones
zone1 = Zone(id="zone1", zone_type="supply", price_high=100, price_low=98)
zone2 = Zone(id="zone2", zone_type="supply", price_high=99, price_low=97)

# Check for overlap
if zone1.overlaps_with(zone2):
    # Merge overlapping zones
    merged_zone = zone1.merge_with(zone2)

# Update zone strength after test
zone1.update_strength(test_result=True)  # Zone held
print(f"New strength: {zone1.strength}")

# Check if zone is still active
if zone1.is_active():
    print("Zone is active")
else:
    print("Zone is inactive")
```

## Testing

Run the test suite:
```bash
pytest app/tests/
```

Run with coverage:
```bash
pytest --cov=app app/tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details