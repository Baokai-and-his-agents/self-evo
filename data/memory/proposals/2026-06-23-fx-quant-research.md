---
name: fx-quant-research-2026-06-23
description: FX 量化策略研究核心原则：Kelly 估计误差、几何财富过程、策略证据强度
metadata:
  type: project
---

## FX 量化策略研究核心原则

**日期:** 2026-06-23
**来源:** Issue #13 FX 量化策略研究（Phase A+B）

### 最关键的数学事实

1. **财富过程是乘法的，非加法**
   - 长期增长由几何均值决定，非算术均值
   - Geometric mean ≈ Arithmetic mean - σ²/2（volatility drag）
   - 50% 损失需 100% 增长恢复

2. **"算术亏损、指数盈利"不成立**
   - 字面意义数学上不一致
   - 可能解释存在但成立条件极严格（无 gap、无 whipsaw、有限亏损）
   - 是营销口号，非严格数学描述

3. **Kelly 准则的致命陷阱**
   - 对估计误差极度敏感
   - 2× Kelly = 零增长，>2× Kelly = 保证长期亏损
   - **Half-Kelly 是实践强制标准**，不是可选项
   - Over-betting 比 under-betting 危险得多

### 策略证据强度分层（优先使用强证据）

**Tier 1 (Strong - 优先回测):**
- Time-series momentum（Moskowitz 2012，AQR 137 年）
- Carry trade crash risk（UChicago 2008）
- Managed Futures / CTA（Pedersen 2012）
- Half-Kelly sizing（arXiv 2024 + 广泛共识）

**Tier 2 (Moderate - 需验证):**
- FX 日内时段效应（5 个独立研究，但可交易幅度 TBD）
- Cross-sectional momentum（Menkhoff，交易成本敏感）
- Volatility targeting（对货币效果有限）

**Tier 5 (Contradicted - 永不使用):**
- Martingale / Grid / Averaging down（数学上保证破产）
- Full Kelly without shrinkage（估计误差下灾难性）

### 关键失败模式（必须避免）

1. **Kelly estimation error:** 最危险，必须保守估计 edge/variance
2. **Carry crash:** 负偏度，VIX hedge 必需
3. **Vol targeting procyclicality:** ECB 2020 实证，波动飙升强制去杠杆
4. **Pyramiding reversal:** 加仓后反转可指数级放大亏损
5. **Martingale:** 保证破产

### 验证设计强制要求

1. **Walk-forward:** 5 年训练 + 1 年测试，滚动
2. **Crisis stress test:** 2008, 2015 Swiss, 2020 COVID 必须覆盖
3. **Transaction cost:** Bid-ask + slippage + swap + roll 完整建模
4. **Kelly shrinkage:** Edge/variance 保守估计，Half-Kelly mandatory
5. **Parameter stability:** 子时期、跨币对验证

### 为何重要

外汇量化策略容易被营销口号误导（"算术亏损、指数盈利"），实际上财富过程本质是乘法的，Kelly 估计误差可能导致灾难。严格的证据分层和风险管理是成功的基础。

### 如何应用

- 所有 FX 策略开发必须从 Tier 1 证据开始
- 仓位管理强制使用 Half-Kelly 或更保守
- 任何涉及"加仓"的策略必须量化反转回吐风险
- 不使用 Martingale/Grid/Full Kelly
- 所有回测必须包含危机时期和完整交易成本

### 相关资源

- [[fx-quant-strategy-research]] 完整研究报告
- [[kelly-criterion-fractional]] Kelly 准则最佳实践
- [[geometric-growth-volatility-drag]] 几何增长与波动拖累

**Why:** FX 量化策略失败的主要原因是 Kelly over-betting、Martingale 和忽视交易成本。明确证据强度和数学事实可避免常见陷阱。

**How to apply:** 策略开发前先检查证据 tier，仓位管理强制 Half-Kelly，回测必须包含危机和完整成本。
