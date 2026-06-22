# FX Long-Horizon Phase B 研究报告
# 长期动态仓位管理

**日期:** 2026-06-23
**Worker:** scout-worker-fx-01
**Run ID:** 2026-06-23-fx-phase-b-001
**Issue:** #13 Phase B
**状态:** Phase B 完成

---

## 执行摘要

本报告系统研究外汇长期动态仓位管理策略，批判性验证"亏损以算术级速度累积、盈利通过加仓/复利呈指数级扩展"的核心思想。研究结论：**该思想作为营销口号存在，但作为严格数学描述不成立**。财富过程本质是乘法的，不存在真正意义上的"算术亏损+指数盈利"。

### 核心发现

1. **数学审计结论:** 财富过程是乘法的，长期增长由几何均值决定，volatility drag = σ²/2
2. **"算术亏损、指数盈利":** 字面意义数学不一致；可能解释存在但成立条件极严格，现实中几乎不可能满足
3. **最强学术支持:** Time-series momentum（Moskowitz 2012，AQR 137年），Carry crash risk（UChicago 2008）
4. **Kelly 估计误差:** 最危险的实践陷阱，over-betting 导致负增长，Half-Kelly 是实践标准
5. **Volatility targeting procyclicality:** ECB 确认系统性风险，2020年3月 risk parity 加剧抛售
6. **反例充分:** 加仓后反转可放大亏损，martingale 在有限资本下 ruin probability 极高

### 证据覆盖

- **独立 Tier1 研究:** 8+ 个（momentum, carry, managed futures, Kelly, vol targeting, math foundations）
- **Central Bank 文档:** ECB 金融稳定报告
- **Practitioner consensus:** Kelly, volatility drag, fractional sizing
- **数学事实:** AM-GM 不等式，几何 < 算术，multiplicative wealth process

---

## 策略家族总结

### 强证据（优先回测）

**1. Time-Series Momentum (1-12月)**
- 证据：Moskowitz (2012) JFE 58种工具，AQR 137年持续盈利，Pedersen Managed Futures Sharpe 1.8
- 特点：顺势持有，长期部分反转
- 风险：Regime shift, whipsaw, 交易成本

**2. Carry Trade**
- 证据：UChicago (2008) 详细 crash 分析
- 特点：利差套利，rollover 收益
- 风险：负偏度，VIX 飙升时 unwind，2008年10月崩溃

**3. Managed Futures / CTA**
- 证据：Pedersen (2012) 详细拆解，24商品+9股指+13债券+12货币
- 特点：跨资产 TSMOM，vol targeting 候选范围 5%-15% (Pedersen source: 10%)
- 表现：分散组合 Sharpe 1.8，bear/bull 市场均表现良好

### 仓位管理方法

**1. Kelly / Fractional Kelly**
- 证据：arXiv (2024) 估计风险分析，广泛 practitioner consensus
- Full Kelly：理论最优但对估计误差极敏感，over-betting 灾难性
- Half-Kelly：标准实践，保留 75% 增长率，减少 50% 波动
- Quarter-Kelly：高不确定性环境
- **关键警告:** 在简单二项模型的局部二次近似下，2× Kelly 对应零增长，>2× Kelly 导致负增长

**2. Volatility Targeting**
- 证据：ECB (2020) 系统性风险报告，Harvey (Duke) 60+ 资产研究，Moreira & Muir (2017) JoF
- 机制：目标波动率（如 10%），动态调整杠杆
- Procyclical 风险：波动飙升时被迫去杠杆，加剧抛售
- 有效性：对 risk assets（股票、信贷）有效，对货币效果有限
- 2020年3月：ECB 确认 risk parity 可能加剧下跌

**3. Pyramiding / Anti-Martingale**
- 证据：理论支持（Kelly, trend following），但反转回吐实证不足
- 机制：盈利时加仓
- 风险：反转回吐可放大亏损（示例：2× 仓位反转 15% = 亏损 76%）
- Whipsaw：震荡市场累积成本

**4. Trailing Stops & Drawdown Control**
- 证据：实践共识，但具体参数缺乏学术验证
- 机制：ATR-based, time-based, drawdown targeting
- 风险：Gap 和 slippage 可能使止损失效

---

## 数学审计：核心结论

### 1. 财富过程的乘法性质

**基本事实:**
```
W_t = W_0 × (1 + r_1) × (1 + r_2) × ... × (1 + r_t)
```

长期增长由**几何均值**决定，非算术均值。

### 2. AM-GM 不等式与 Volatility Drag

```
Geometric Mean < Arithmetic Mean (除非零波动)
μ_geometric ≈ μ_arithmetic - σ²/2
```

**直观例子:**
- 年1: +50%，年2: -40%
- 算术均值：+5%
- 几何均值：-5.1%
- Volatility drag：10.1%

**50% 损失需 100% 增长才能恢复** — 损失的不对称性是乘法过程固有特征。

### 3. "算术亏损、指数盈利"的真相

**字面意义：** 数学上不一致。财富不能同时服从加法过程（亏损）和乘法过程（盈利）。

**可能的合理解释:**

**解释 A: 固定风险 + 盈利加仓**
- 亏损：固定 2% 止损，连续 N 次 ≈ N×2%（算术近似）
- 盈利：加仓，收益 ∝ (1+scale)^t（指数级）

**成立条件（极其严格）:**
1. 止损 100% 执行，无 gap、无滑点
2. 连续亏损次数有上界
3. 盈利加仓后无反转回吐
4. 交易成本可忽略
5. Edge 估计准确

**现实中几乎不可能同时满足所有条件。**

**反例 1: 连续止损（几何累积）**
- 10 次 2% 止损
- 算术近似：20%
- 几何实际：(1-0.02)^10 ≈ 81.7%，即亏损 18.3%

**反例 2: 加仓后反转**
- 盈利 20%，加仓至 2× 仓位
- 反转 15%
- 实际亏损：76%（从 $100k → $24k）

**反例 3: Gap**
- 设定止损 2%
- 周末 gap 开盘 -8%
- 实际亏损 8%，远超"算术级"

### 4. 最终判断

**"亏损算术级、盈利指数级"是营销口号，非严格数学描述。**

更准确的描述：
- 通过严格止损和仓位管理，**限制单次和累积亏损幅度**
- 通过趋势跟随和正偏度策略，**在趋势持续时获得超线性收益**
- 但这仍然是**几何财富过程**，只是通过策略设计优化了收益分布

**不存在真正意义上的"算术亏损+指数盈利"的数学免费午餐。**

---

## 失败模式 Top 5

### 1. Kelly Estimation Error（最危险）
- Over-estimate edge → over-bet → 负增长
- 简单模型下 2× Kelly 对应零增长
- Mitigation: Half-Kelly, shrinkage, conservative estimates

### 2. Carry Crash
- 2008年10月 VIX 飙升，speculator unwind
- 负偏度：小赚累积，一次暴亏
- Mitigation: VIX hedge, position limits, crisis scenarios

### 3. Volatility Targeting Procyclicality
- 波动飙升 → 强制去杠杆 → 加剧抛售
- ECB: 2020年3月证据
- Mitigation: Conditional targeting, leverage caps, de-risk rules

### 4. Pyramiding Reversal Drawdown
- 加仓后反转，放大亏损
- 2× position, 15% reversal = 76% loss
- Mitigation: Tiered stops, max leverage, trailing stops

### 5. Martingale / Grid（保证破产）
- 亏损加仓
- 有限资本下 ruin probability 极高
- Mitigation: **永不使用**

---

## 交付文档

Phase B 交付：
- `2026-06-23-fx-long-horizon-exploration-brief.md`
- `2026-06-23-fx-long-horizon-query-matrix.md`
- `2026-06-23-fx-long-horizon-source-decisions.md`（12+ entries，8 tier1）
- `2026-06-23-fx-long-horizon-strategy-taxonomy.md`
- `2026-06-23-fx-long-horizon-position-sizing-math.md`（核心数学分析）
- `2026-06-23-fx-long-horizon-failure-landscape.md`
- `2026-06-23-fx-long-horizon-evidence-map.md`
- 本报告

---

## 推荐后续行动

### 数据准备
1. 获取 20+ 年货币远期/期货数据（CME, Dukas copy spot）
2. Bid-ask, roll, swap 完整成本数据
3. 多 regime 覆盖：至少 2 次货币危机、2 次股市崩盘

### 优先回测策略
1. **Time-series momentum:** 候选配置 1/3/6/12 月 (source: Moskowitz 1-12月，Pedersen 实验用1月)，vol targeting 5%-15% 网格
2. **Carry trade:** 带 VIX hedge 或 drawdown cut (实验性)
3. **Half-Kelly sizing:** 保守 edge/variance 估计

### 验证协议
1. Walk-forward 多窗口比较：候选配置包括 (train:test = 5:1, 4:1, 3:1 年)，滚动验证
2. Parameter stability: 子时期、跨币对验证
3. Portfolio attribution: signal, sizing, carry, vol target 分解
4. Baseline 比较：固定仓位、无加仓、buy-and-hold
5. 交易成本：bid-ask + slippage + swap 完整建模
6. Crisis 压力测试：2008, 2015 Swiss, 2020 COVID

### 避免的陷阱
1. **Full Kelly without shrinkage**
2. **Martingale / Grid / Averaging down**
3. **Over-leverage after wins**
4. **Ignoring estimation error**
5. **Believing in "arithmetic loss, geometric gain" literally**

---

**Phase B 完成。准备 Phase A+B 综合报告。**
