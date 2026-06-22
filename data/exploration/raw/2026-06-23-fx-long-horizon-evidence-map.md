# FX Long-Horizon Evidence Map
# Phase B: Dynamic Position Management

**Date:** 2026-06-23
**Worker:** scout-worker-fx-01

---

## Evidence Tiers

- **Tier 1 (Strong):** ≥2 tier1 papers + independent validation
- **Tier 2 (Moderate):** 1 tier1 or multiple tier2
- **Tier 3 (Weak):** tier4 consensus
- **Tier 4 (Hypothesis):** 理论合理但无充分实证
- **Tier 5 (Contradicted):** 存在反证

---

## Key Claims

### 1. Time-Series Momentum (1-12月)
**Evidence: Tier 1 (Strong)**
- Moskowitz (2012): JFE, 58 instruments
- AQR (2017): 137 years
- Pedersen: Managed Futures Sharpe 1.8
- 独立验证跨时间、跨资产

### 2. Currency Momentum 10% p.a.
**Evidence: Tier 1 (Strong)**
- Menkhoff BIS: 1976-2010, 48 currencies
- JFE (2021): Factor momentum
- 但交易成本敏感

### 3. Carry Crash Risk
**Evidence: Tier 1 (Strong)**
- UChicago (2008): 负偏度，VIX unwind
- 实证明确

### 4. Kelly Estimation Error
**Evidence: Tier 1 (Strong - Position Sizing Method)**
- arXiv (2024): 估计风险
- Practitioner consensus: Fractional Kelly standard
- 数学推导：简单二项模型下的局部性质
- **注：Kelly 是 sizing objective，不是 alpha 或策略**

### 5. Volatility Targeting Procyclicality
**Evidence: Tier 1 (Strong)**
- ECB (2020): 2 trillion AUM, 2020年3月
- Harvey: leverage effect on risk assets
- Moreira & Muir (2017): JoF

### 6. Geometric < Arithmetic (Volatility Drag)
**Evidence: Tier 1 (Strong - Mathematical Fact)**
- AM-GM inequality
- Widespread consensus
- μ_geo ≈ μ_arith - σ²/2

### 7. "算术亏损、指数盈利"
**Evidence: Tier 5 (Contradicted)**
- 字面意义：数学不一致
- 可能解释存在但成立条件极严格
- 反例充分（见 position sizing math）

### 8. Pyramiding Profitability
**Evidence: Tier 3 (Weak)**
- 理论支持（Kelly, trend following）
- 但反转回吐风险实证不足
- 需要具体参数验证

### 9. Martingale / Grid
**Evidence: Tier 5 (Contradicted - Mathematically)**
- 有限资本、持续下注、无有利停止规则下 ruin probability 极高
- 理论与实证一致反对

### 10. Vol Targeting on Currencies
**Evidence: Tier 2 (Moderate - Limited Effect)**
- Harvey: 对货币效果可忽略
- 主要对 risk assets 有效
- 与 carry crash risk 相关

---

## Summary

**Strong Evidence (可直接用于回测):**
- Time-series momentum
- Carry trade (with crash awareness)
- Fractional Kelly sizing (作为 sizing method 比较候选)
- Volatility drag (geometric growth)

**Moderate Evidence (需谨慎验证):**
- Vol targeting (limited FX benefit)
- Pyramiding (whipsaw cost TBD)

**Weak/Contradicted (避免或需重大修正):**
- "算术亏损、指数盈利"（营销口号）
- Martingale/grid（有限资本下 ruin probability 极高）
- Full Kelly without shrinkage（估计误差下表现极差）
