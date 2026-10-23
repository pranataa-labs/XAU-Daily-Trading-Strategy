# 📊 XAU/USD Quantitative Daily Trading Strategy

### Institutional Volatility Transition Model For Gold (XAU/USD)

<div align="left">

![Asset](https://img.shields.io/badge/Asset-XAU%2FUSD%20(Gold)-ffd700?style=for-the-badge)
![Testing Horizon](https://img.shields.io/badge/Evaluated%20Days-559%20Days-blue?style=for-the-badge)
![Net Profit](https://img.shields.io/badge/Net%20Profit-%2B64.08%20R%20(%2B14%2C616%20Pips)-2ca02c?style=for-the-badge)
![Win Rate](https://img.shields.io/badge/Win%20Rate-44.2%25-green?style=for-the-badge)
![Payoff](https://img.shields.io/badge/Payoff-1%3A2.0%20Asymmetric-orange?style=for-the-badge)
![Profit Factor](https://img.shields.io/badge/Profit%20Factor-1.22-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

> **Model Overview:**  
> Institutional quantitative daily trading strategy for Gold (XAU/USD) engineered to capture session volatility transitions between the Asian close and London/New York liquidity expansions. Validated across 559 continuous trading sessions with +64.08 R (+14,616 Pips) net yield under a set-and-forget execution discipline.

---

## 📊 Key Quantitative Performance Metrics (559 Trading Days)

| Performance Parameter | Empirical Metric |
| :--- | :--- |
| **Testing Horizon** | **559 Continuous Trading Days** |
| **Total Triggered Trades** | **452 Executed Orders** |
| **Strategy Win Rate** | **44.2%** |
| **Asymmetric Payoff Structure** | **1 : 2.0 Risk-to-Reward Ratio** |
| **Net Accumulated Profit** | **+64.08 R (+14,616 Pips / +1,461.60 USD points)** |
| **Profit Factor (PF)** | **1.22** |
| **Execution Protocol** | **Zero Screen-Time Set-And-Forget** |

---

## 📐 Quantitative Thesis & Mechanics

1. **Session Volatility Expansion:** Explores predictable volatility compression during Asian hours and subsequent expansions during London and New York overlaps.
2. **Asymmetric Edge:** By enforcing a strict 1:2.0 Risk-Reward ratio, the strategy delivers robust positive expectancy (+64.08 R) even at a conservative 44.2% win rate.
3. **Execution Simplicity:** Eliminates emotional mid-trade interference through deterministic pending orders with pre-set Stop Loss and Take Profit levels.

---

## 📁 Repository Structure

```text
XAU-Daily-Trading-Strategy/
├── xau_daily_strategy_backtest.ipynb   # Master quantitative research notebook & equity curve
├── strategy_engine.py                  # Core signal generator & backtest simulator
├── historical_data_cache.csv           # Historical daily OHLCV dataset
└── README.md                           # Strategy specification and empirical verification
```

---

## 🚀 Execution & Setup Guide

```bash
# Clone repository
git clone https://github.com/pranataa-labs/XAU-Daily-Trading-Strategy.git
cd XAU-Daily-Trading-Strategy

# Install dependencies
pip install pandas numpy matplotlib seaborn jupyter

# Launch research notebook
jupyter lab
```

---

<p align="center">
  Engineered by <b><a href="https://github.com/pranataa-labs">pranataa-labs</a></b>
</p>
