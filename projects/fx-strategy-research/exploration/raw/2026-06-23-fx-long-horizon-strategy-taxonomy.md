# FX Long-Horizon Strategy Taxonomy
# Phase B: Dynamic Position Management

**Date:** 2026-06-23
**Worker:** scout-worker-fx-01

---

## Strategy Families

### 1. Time-Series Momentum / Trend Following
- **1-12 月 look-back，顺势持有**
- Evidence: Strong (Moskowitz 2012, AQR 137年, Menkhoff BIS)
- Sharpe: ~0.5-1.0, Max DD: 20-40%

### 2. Cross-Sectional Currency Momentum
- **做多赢家货币，做空输家货币**
- Evidence: Strong (Menkhoff 10% p.a., JFE 2021)
- Cost-sensitive, limits to arbitrage

### 3. Carry Trade
- **利差套利，rollover 收益**
- Evidence: Strong (UChicago 2008 crash study)
- Crash risk: 负偏度，VIX 飙升时 unwind

### 4. Value & PPP
- **长期均值回归**
- Evidence: Moderate (PPP half-life ~3-5 年)

### 5. Managed Futures / CTA
- **多资产 TSMOM，vol targeting**
- Evidence: Strong (Pedersen Demystifying, Sharpe 1.8)

---

## Position Sizing Methods

### 1. Kelly / Fractional Kelly
- Full Kelly: 简单二项模型下最优但对估计误差敏感
- Half/Quarter Kelly: 常见 shrinkage 候选
- 需与 fixed fractional, vol targeting, risk-constrained sizing 比较

### 2. Volatility Targeting
- 目标波动率 10-15%
- Procyclical: 波动飙升时去杠杆
- Risk assets 有效，货币效果有限

### 3. Fixed Fractional / Risk Parity
- 固定风险比例
- Portfolio heat 限制

### 4. Pyramiding / Anti-Martingale
- 盈利加仓
- Whipsaw 风险，反转回吐（幅度取决于加仓规则）

---

## Risk Management

### Trailing Stops
- ATR-based, time-based
- Slippage, gap 风险

### Drawdown Targeting
- De-risk/re-risk
- Correlation clustering

### Portfolio Constraints
- Max position size
- Net currency exposure
- USD factor hedge
