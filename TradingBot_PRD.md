
# 📄 Product Requirements Document (PRD)

## 🎯 Project Title  
**Multi-Strategy AI-Powered Trading Bot**  
**Platform**: Coinbase Advanced Trade API  
**Workspace**: Cursor

---

## 🧩 Overview

This project aims to build a modular trading bot that:

- ✅ Executes RSI momentum trades with market regime filtering  
- ✅ Trades Bollinger Band mean reversions during sideways conditions  
- ✅ Adapts dynamically using ML (LSTM + Clustering)  
- ✅ Adds a supply/demand strategy using volume or AI-driven zone detection  
- ✅ Runs in backtest, paper, or live mode through Coinbase Advanced API  

---

## 📁 Project Structure

```
project/
├── .env
├── requirements.txt
├── utils/
│   └── data.py
│   └── ml.py
├── strategies/
│   └── rsi_regime.py
│   └── bollinger.py
│   └── lstm_filter.py
│   └── supply_demand.py
├── backtest/
│   └── runner.py
│   └── compare.py
├── live/
│   └── paper_trader.py
│   └── live_trader.py
```

---

## ✅ Core Strategy Stack

### 1. RSI + Market Regime Momentum
- Trades long during “uptrend” regime
- RSI(14) cross above 55 → buy
- Exit on RSI < 45 or regime change
- Avoids signals during downtrends

### 2. Bollinger Band Mean Reversion
- Active during sideways regimes
- Buy when price closes below lower BB + RSI < 30
- Exit when price returns to the mean or RSI > 50
- Stop-loss set below swing low

### 3. Volatility Squeeze Breakout (Short Bias)
- Detects tight BB contraction (low volatility)
- Short when price breaks below range with volume spike
- Requires RSI/MACD confirmation
- Exit using 2:1 reward/risk and volatility filter

### 4. Supply & Demand Zone Bounces
- Detects recent high-volume reversal areas
- Buy near demand zones with bullish confirmation
- Confirmed by candle patterns, RSI > 30, or MACD cross
- Stop-loss slightly below the zone, exit mid-range

### 5. LSTM / ML Confirmation (Optional)
- Predicts next candle’s direction (1 = up, 0 = down)
- Filters trades from other strategies based on prediction
- Trained on historical OHLCV + indicators
- Run live or update weekly

---

## 🔐 Risk Management
- Max 1–2% risk per trade
- Circuit breaker after N losses
- Dynamic sizing based on volatility or zone strength
- Position limit per asset + overall exposure cap

---

## 🧪 Backtesting System
- Run historical simulations for any strategy
- Output: total return, Sharpe, drawdown, trades, win rate
- Includes slippage + fee simulation
- Option for walk-forward testing and strategy comparison

---

## 🧠 Machine Learning Additions

### LSTM Module
- Predict next 4h candle direction
- Filter or confirm entries
- Trained on windowed OHLCV + indicators

### Market Regime Clustering
- k-means or HMM clustering based on ATR, slope, volume
- Replaces hard-coded regime filters
- Used to switch between strategies

---

## 📟 Monitoring & Dashboard

- Streamlit/FastAPI dashboard
- Shows live positions, active strategy, equity curve
- Displays regime, S/D zones, indicators
- Control panel to toggle strategies, pause, dry-run

---

## 🚀 Advanced Additions for Strategic Expansion

### ✅ 1. Multi-Asset Support & Strategy Rotation

**Goal**: Trade the most favorable assets in real-time.

- Add support for BTC, ETH, SOL, LTC, etc.
- Rank assets by volatility, volume, or ML score
- Run strategies per asset with independent risk caps
- Rotate to high-confidence coins and pause underperformers

---

### ✅ 2. Trade Journal + Meta Logging System

**Goal**: Log detailed trade metadata and improve with reviews.

- Log: strategy name, regime, RSI, MACD, LSTM score, zone quality
- Weekly review report: Sharpe, R:R, max loss streak, % hit targets
- Optional tags: “perfect trade,” “premature exit,” “bad zone”

---

### ✅ 3. Strategy Ensemble Voting Engine

**Goal**: Only trade when strategies agree for high-confidence entries.

- Each strategy outputs vote: buy, hold, or sell
- Only enter trades when 2+ agree (or confidence threshold met)
- Weighted votes (e.g., RSI = 1, ML = 1.5, S/D = 2)
- Prevents low-confidence solo strategies from triggering risk

---

## 📊 Metrics to Track

- Total Return (%)
- Sharpe Ratio
- Max Drawdown
- Win Rate (%)
- Trades per strategy
- Avg. Reward:Risk
- Trade duration distribution

---

## 🛠 Technical Architecture

- Python (3.10+), TA-Lib, scikit-learn
- Coinbase Advanced REST + WebSocket
- SQLite or JSON logs
- ML: LSTM, k-means, or XGBoost
- UI: Streamlit or FastAPI dashboard
- Optional: Telegram/Discord integration

---

## 🛠 Development Roadmap

### Phase 1 – Foundation
- [x] Coinbase API client
- [x] RSI + regime strategy
- [x] Backtester
- [ ] Bollinger strategy
- [ ] Supply/Demand module
- [ ] Risk engine

### Phase 2 – Interface + Strategy Engine
- [ ] Dashboard UI
- [ ] Trade logger + visual equity curves
- [ ] Multi-strategy controller

### Phase 3 – Machine Learning
- [ ] LSTM model + live filtering
- [ ] Regime clustering
- [ ] Walk-forward validator

### Phase 4 – Advanced Logic
- [ ] Strategy voting engine
- [ ] Multi-asset trade allocator
- [ ] Meta logging + journal
- [ ] Ensemble performance tracker

---

## 🧠 Future Ideas

- Reinforcement learning-based strategy selector
- Sentiment/NLP signal layer
- Book imbalance + real-time Level 2 filter
- Decentralized exchange integrations
- Plug-and-play module for hedge ratio / pairs trading

---

## ✅ Success Criteria

- ≥10 trades per strategy logged with risk-managed execution
- Live system runs 24h with no failures
- Sharpe > 1.2 over 60-day backtest
- Bot survives a bear phase with <10% drawdown
- Modular and safe enough to deploy with real capital

---
