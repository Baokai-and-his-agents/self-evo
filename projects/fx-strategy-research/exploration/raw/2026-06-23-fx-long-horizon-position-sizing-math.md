# FX Long-Horizon Position Sizing Math
# Phase B: Dynamic Position Management

**Date:** 2026-06-23
**Worker:** scout-worker-fx-01
**Run ID:** 2026-06-23-fx-phase-b-001

---

## Purpose

批判性分析"亏损算术级、盈利指数级"的数学可行性，提供成立条件、反例和误导风险。

---

## 1. 财富过程的乘法性质

### 1.1 基本事实

财富过程本质是**乘法的**，非加法：

```
W_t = W_0 × (1 + r_1) × (1 + r_2) × ... × (1 + r_t)
```

对数形式：

```
log(W_t) = log(W_0) + Σ log(1 + r_i)
```

**结论 1:** 长期财富增长由**几何平均收益**决定，非算术平均。

### 1.2 几何与算术收益的差异

AM-GM 不等式：除非所有收益相同，否则：

```
Geometric Mean < Arithmetic Mean
```

近似关系（对数正态假设）：

```
μ_geometric ≈ μ_arithmetic - σ²/2
```

其中 σ² 是方差。

**结论 2:** 波动率越高，几何收益与算术收益的差距越大。这被称为 **volatility drag** 或 **variance drain**。

### 1.3 Volatility Drag 的直观例子

| 年份 | 收益 | 财富 |
|------|------|------|
| 0    | -    | $100 |
| 1    | +50% | $150 |
| 2    | -40% | $90  |

- 算术平均：(50% - 40%) / 2 = **+5%**
- 几何平均：(90/100)^(1/2) - 1 = **-5.1%**

**Volatility drag = 10.1%**

50% 损失需要 **100% 增长**才能恢复。损失与恢复的不对称性是乘法过程的固有特征。

---

## 2. "亏损算术级、盈利指数级"的数学审计

### 2.1 字面解释（误导版本）

如果字面理解为：
- 亏损时：W_t = W_0 - c × t（算术级）
- 盈利时：W_t = W_0 × e^(r × t)（指数级）

**数学矛盾：** 财富不能同时服从加法过程（亏损）和乘法过程（盈利）。这种描述在数学上不一致。

**结论 3:** 字面版本的"算术亏损、指数盈利"在单一财富过程中**不可能成立**。

### 2.2 可能的合理解释

#### 解释 A：固定风险损失 + 盈利加仓

- **亏损阶段：** 每次亏损固定资金比例（如 2%），连续 N 次亏损：
  ```
  Total Loss ≈ N × 2% (算术级近似，忽略复利)
  ```

- **盈利阶段：** 加仓（pyramiding），每次盈利增加仓位：
  ```
  Position_t = Position_0 × (1 + scale)^t
  Profit_t ∝ (1 + scale)^t (指数级)
  ```

**成立条件：**
1. 止损严格执行，单次亏损≤ 2%
2. 连续亏损次数有限（不能无限连亏）
3. 盈利阶段加仓不会在反转时回吐过多
4. 交易成本不抵消加仓收益

**反例场景：**
- 连续 50 次亏损：即使每次 2%，总亏损 ≈ 63.6%（几何复利）
- Whipsaw：加仓后立即反转，回吐放大损失
- Gap：止损无法以预期价格执行，实际损失 > 2%

#### 解释 B：负偏度策略 vs 正偏度策略

- **高胜率、小盈利、偶尔大亏（负偏度）：** 常见于 mean reversion, grid, martingale
  - 99 次小赢 +1%，1 次大亏 -50%
  - 总收益：0.99 × 0.01 - 0.01 × 0.50 = -0.005 = **负期望**

- **低胜率、小亏、偶尔大赢（正偏度）：** 常见于 trend following, anti-martingale
  - 60 次小亏 -1%，40 次大赢 +3%
  - 总收益：0.60 × (-0.01) + 0.40 × 0.03 = +0.006 = **正期望**

**结论 4:** 正偏度策略可以产生"小亏损累积、大盈利爆发"的表象，但这是**偏度与期望收益的组合效应**，非纯粹的"算术 vs 指数"。

#### 解释 C：Kelly / Fractional Kelly 下的财富路径

Kelly 准则最大化**对数财富的期望增长**。在简单二项模型下（已知固定胜率 p、盈亏比 b）：

```
f* = (p × b - q) / b
```

其中 p = 胜率，q = 1 - p，b = 盈亏比。

**Full Kelly 下的财富路径（简单二项模型）：**
- 盈利时：W × (1 + f* × R)
- 亏损时：W × (1 - f* × R)

**关于 2× Kelly 的结论：**

在上述简单二项模型中，围绕最优 f* 进行局部二次近似时，2× Kelly (2f*) 对应零增长，>2× Kelly 导致负增长。这是特定模型下的性质，不是普遍数学定理。

现实交易中：
- 收益分布非二项，可能有厚尾、偏度
- 参数（edge, variance）是估计量，存在估计误差
- 存在交易成本、滑点、相关性变化

**结论 5:** Kelly 准则控制单次亏损比例，但**不改变财富过程的乘法本质**。长期增长仍由几何均值决定。2× Kelly 结论仅在特定简单模型和已知参数下成立。

### 2.3 路径依赖与反例

#### 反例 1：趋势反转后的加仓回吐

假设：
1. 初始资金 $100,000
2. 趋势盈利 20%，加仓至 2× 仓位
3. 趋势反转，亏损 15%

- 第一阶段盈利：$100,000 × 1.20 = $120,000
- 加仓后资金暴露：$120,000 × 2 = $240,000（名义）
- 反转亏损：$240,000 × 0.85 - $120,000 = -$96,000（超过初始资金！）

**实际财富：** $120,000 - $96,000 = $24,000（亏损 76%）

**结论：** 加仓后的反转可以**放大亏损（幅度取决于加仓规则和反转幅度）**。

#### 反例 2：Gap 与 Slippage

- 设定止损 2%
- 周末 gap 开盘跌 8%
- 实际亏损 8%，远超"算术级 2%"

#### 反例 3：连续止损

- 10 次连续止损，每次 2%
- 算术近似：10 × 2% = 20%
- 几何实际：(1 - 0.02)^10 ≈ 81.7%，即亏损 **18.3%**

**即使止损固定，累积仍是几何的，非算术的。**

---

## 3. Anti-Martingale vs Martingale

### 3.1 Anti-Martingale（盈利加仓）

**定义：** 盈利时增加仓位，亏损时减少或保持。

**典型形式：**
- Fixed fractional: f = constant × edge / volatility
- Pyramiding: 盈利后增加固定金额或固定比例仓位
- Trend following + vol targeting

**加仓规则示例：**

1. **线性加仓：** 每次盈利后增加固定比例（如 +20% 初始仓位）
   - 反转损失 = 当前总仓位 × 反转幅度

2. **几何加仓：** 每次盈利后仓位乘以固定倍数（如 ×1.5）
   - Position_t = Position_0 × 1.5^t
   - 反转后快速回吐，但非固定"指数级"

3. **Doubling schedule：** 每次盈利后仓位加倍
   - Position_t = Position_0 × 2^t
   - 反转损失最大化

**理论优势：**
- 顺应趋势，截断亏损、让利润奔跑
- Kelly 理论支持（当 edge > 0）

**实际挑战：**
- Whipsaw：频繁假突破，加仓后立即反转
- 交易成本：高频加仓/减仓增加成本
- 估计误差：edge 和 volatility 估计不准，导致过度或不足加仓
- 心理难度：盈利后加仓放大回撤心理压力

**反转回吐取决于：**
- 加仓规则（线性、几何、doubling）
- 趋势持续时间与加仓次数
- 反转幅度
- 是否有分层止损

### 3.2 Martingale（亏损加仓）

**定义：** 亏损时增加仓位（averaging down, grid trading, doubling down）。

**Risk-of-ruin 分析：**

假设每次亏损加倍仓位，连续 N 次亏损后：
- 总投入：1 + 2 + 4 + ... + 2^N = 2^(N+1) - 1
- 如果 N = 10，总投入 2047 单位资金

**成立条件：**
- 有限资本
- 持续下注（无停止规则或停止条件不满足）
- 每次独立亏损概率 > 0
- 有限赔率（无法无限加倍）

**在上述条件下，ruin probability 可趋近 1。**

具体概率取决于：
- 初始资本与最小下注比例
- 单次亏损概率
- 加仓倍数
- 最大层级限制
- 价格过程（如均值回归 vs 趋势）

**结论 6:** Martingale 在有限资本、持续下注、无有利停止规则的条件下，长期 ruin probability 极高。

---

## 4. "Cut Losses Short, Let Profits Run" 的实证证据

### 4.1 理论基础

- Trend following: 顺势而为，趋势持续时盈利放大
- Positive skewness: 小亏损、大盈利分布
- Kelly criterion: 最优仓位在 edge > 0 时 > 0

### 4.2 实证支持

- **Moskowitz et al. (2012):** Time-series momentum 跨资产显著，58 种工具，1-12 月持续
- **AQR (2017):** 137 年 trend following 持续盈利
- **Menkhoff et al. (2012):** Currency momentum 10% p.a.，但交易成本敏感

### 4.3 实证挑战

- **Whipsaw 成本：** 震荡市场中频繁止损，累积成本高
- **交易成本：** Bid-ask spread, slippage, commission 累积
- **假突破：** 突破后回撤，止损触发
- **Regime shift：** 趋势市场转震荡市场，策略失效

**结论 7:** "Cut losses, let profits run" 在趋势市场有实证支持，但在震荡市场和高交易成本环境下可能失效。

---

## 5. Convexity, Skewness & Guaranteed Profit

### 5.1 定义区分

- **Positive Convexity:** 收益对价格变化的二阶导数 > 0（如 long option）
- **Positive Skewness:** 收益分布右偏，大盈利概率 > 大亏损概率
- **Guaranteed Profit:** 无风险正收益

**结论 8:** 三者**互不等价**：
- Positive convexity ≠ positive expected return（long option 可能 theta decay）
- Positive skewness ≠ positive expected return（lottery tickets 高偏度、负期望）
- 无单边免费的指数增长

### 5.2 Convexity 的成本

- Long options: 支付 premium（time decay）
- Convexity 来自期权费用，非免费
- Gamma scalping: 理论上可盈利，但需要频繁对冲，交易成本高

### 5.3 Trend Following 的隐含 Convexity

- 趋势持续时，盈利加速（类似 long gamma）
- 趋势反转时，止损截断（类似 option）

**但这是"合成"凸性，非真正期权：**
- 止损滑点可能导致实际亏损 > 预期
- Gap 可能跳过止损，损失放大
- Whipsaw 累积成本

**结论 9:** Trend following 类似 long straddle，但执行成本和 whipsaw 是真实代价。

---

## 6. 数学结论总结

### 6.1 核心数学事实

1. **财富过程是乘法的**，长期增长由几何均值决定
2. **Volatility drag = σ²/2**，波动率降低几何收益
3. **50% 损失需 100% 增长恢复**，损失不对称
4. **AM-GM 不等式**：几何 < 算术（除非零波动）

### 6.2 "算术亏损、指数盈利"的真相

**字面意义：** 数学上不一致，单一财富过程不能同时加法和乘法。

**可能合理解释：**
- **固定风险 + 加仓：** 理论上可行，但需严格止损、有限亏损次数、避免反转回吐
- **正偏度策略：** 小亏、大赢分布，但仍是几何过程
- **Kelly 控制：** 限制单次亏损比例，但不改变乘法本质

**成立条件（极其严格）：**
1. 止损 100% 执行，无 gap、无滑点
2. 连续亏损次数有上界
3. 盈利加仓后无反转回吐
4. 交易成本可忽略
5. Edge 估计准确，无估计误差

**现实中几乎不可能同时满足所有条件。**

### 6.3 反例与风险

- **连续亏损：** 即使固定 2%，10 次亏损 = 18.3%（几何）
- **加仓回吐：** 2× 仓位反转 15% = 亏损 76%
- **Gap：** 止损失效，实际亏损远超预期
- **Whipsaw：** 震荡市场累积成本
- **Martingale：** 在有限资本、持续下注等条件下风险敞口指数增长

### 6.4 最终判断

**"亏损算术级、盈利指数级"是营销口号，非严格数学描述。**

**更准确的描述应该是：**
- 通过严格止损和仓位管理，**限制单次和累积亏损幅度**
- 通过趋势跟随和正偏度策略，**在趋势持续时获得超线性收益**
- 但这仍然是**几何财富过程**，只是通过策略设计优化了收益分布

**不存在真正意义上的"算术亏损+指数盈利"的数学免费午餐。**

---

## 7. 实践启示

### 7.1 Position Sizing 原则

1. **Conservative estimation:** 估计 edge 和 variance 时保持保守，考虑估计误差
2. **Compare shrinkage methods:** 评估 Half-Kelly (0.5f*)、Quarter-Kelly (0.25f*)、fixed fractional、vol targeting、risk-constrained sizing
3. **Avoid over-betting:** Full Kelly 对估计误差极度敏感；在简单二项模型的局部二次近似下，2× Kelly 对应零增长
4. **Hard stop-loss:** 必须设置，但要预留 slippage buffer
5. **Portfolio heat limit:** 限制同时开仓的总风险暴露

### 7.2 避免的陷阱

1. **Martingale / Grid / Averaging Down:** 在有限资本、持续下注等条件下风险敞口指数增长
2. **Over-leverage after wins:** 加仓后反转可能放大亏损（具体幅度取决于加仓规则）
3. **Ignoring estimation error:** Full Kelly 在估计误差下表现极差
4. **Ignoring transaction costs:** 高频调整迅速侵蚀收益
5. **Believing in free convexity:** 所有 convexity 都有成本

### 7.3 Realistic Expectations

- **Trend following Sharpe ~0.5-1.0** (历史数据，考虑成本后)
- **Max drawdown 20-40%** (即使 vol targeting)
- **Win rate ~30-45%** (低胜率、高盈亏比)
- **Correlation spike risk:** 危机时相关性趋同，分散失效
- **Regime dependency:** 趋势市场有效，震荡市场亏损

**没有"算术亏损、指数盈利"的魔法，只有风险管理和耐心执行。**
