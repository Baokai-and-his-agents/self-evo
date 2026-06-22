# FX 量化策略后续实验候选
# Project Candidates for FX Quantitative Strategies

**日期:** 2026-06-23
**Worker:** scout-worker-fx-01

---

## 候选项目分类

### A. 高优先级（强证据，可立即开始）

#### A1. Time-Series Momentum Baseline
- **目标:** 实现并验证多参数 TSMOM
- **数据:** 10+ 主要货币对，20+ 年日度数据
- **方法:** Look-back 候选网格 (1/3/6/12月，source: Moskowitz 1-12月验证)，Vol targeting 候选范围 (5%/10%/15%，source: Pedersen 实验用10%)，Sizing 方法比较 (fractional Kelly/fixed fractional/vol targeting)，walk-forward 多窗口比较 (train:test = 5:1, 4:1, 3:1 年)
- **预期时间:** 6-8 周
- **成功标准:** Sharpe > 0.5，max DD < 30%，walk-forward 稳定

#### A2. Carry Trade with Crash Protection
- **目标:** 利差套利 + crash control 实验候选
- **数据:** 货币对 + swap rates + VIX 历史
- **方法:** 做多高利差货币，测试多种 crash control 实验候选 (VIX 阈值网格、no hedge baseline、其他 risk control)
- **预期时间:** 4-6 周
- **成功标准:** 正期望收益，2008 年回撤可控，比较各 hedge 成本

#### A3. Position Sizing Methods Comparison
- **目标:** 比较多种 sizing 方法
- **数据:** 策略历史收益
- **方法:** 实现并比较 fractional Kelly (多个 fraction 候选)、fixed fractional、vol targeting、risk-constrained sizing
- **预期时间:** 2-4 周
- **成功标准:** 保守估计 edge/variance，各方法 risk-return profile 清晰

### B. 中优先级（需适配验证）

#### B1. FX Intraday Time-of-Day Momentum
- **目标:** 验证货币在本地时段贬值效应
- **数据:** 5+ 年 tick/分钟数据，多时区货币
- **方法:** 时段划分，交易成本完整建模
- **预期时间:** 8-10 周
- **成功标准:** 时段效应显著，净收益 > 0（扣除成本）

#### B2. London Breakout Parameter Validation
- **目标:** 验证伦敦开盘突破的 FX 具体参数
- **数据:** 5+ 年分钟数据，亚洲+伦敦时段
- **方法:** 区间宽度优化，假突破率统计
- **预期时间:** 4-6 周
- **成功标准:** 假突破率 < 60%，净收益 > 0

#### B3. Cross-Sectional Currency Momentum
- **目标:** 跨货币动量组合
- **数据:** 20+ 种货币，20+ 年
- **方法:** 做多赢家、做空输家，月度 rebalance
- **预期时间:** 6-8 周
- **成功标准:** 年化超额收益 > 5%（扣除成本）

### C. 探索性（高不确定性）

#### C1. Volatility Targeting for Currencies
- **目标:** 测试 vol targeting 对货币的实际效果
- **数据:** 多货币对，20+ 年
- **方法:** 目标波动率，动态杠杆
- **预期时间:** 4-6 周
- **成功标准:** 确认效果有限（Harvey 结论），或发现特定条件下有效

#### C2. Pyramiding with Tiered Stops
- **目标:** 盈利加仓 + 分层止损，量化反转回吐
- **数据:** Trend-following 策略历史
- **方法:** 加仓规则，分层止损，回撤统计
- **预期时间:** 6-8 周
- **成功标准:** 反转回吐量化，净收益 vs baseline

#### C3. Cointegration Pairs (Intraday FX)
- **目标:** 验证协整配对交易的日内 FX 适用性
- **数据:** 高相关货币对，tick/分钟数据
- **方法:** Engle-Granger, Johansen, Bollinger Bands
- **预期时间:** 6-8 周
- **成功标准:** 稳定协整关系，净收益 > 0

### D. 基础设施与工具

#### D1. Transaction Cost Model
- **目标:** 完整交易成本建模框架
- **数据:** Broker bid-ask, slippage 统计, swap rates
- **方法:** 时段变化建模，流动性影响
- **预期时间:** 3-4 周
- **成功标准:** 可复用的成本模块

#### D2. Walk-Forward Engine
- **目标:** 自动化 walk-forward 分析
- **数据:** 任意策略收益序列
- **方法:** 滚动窗口，参数稳定性检测
- **预期时间:** 2-3 周
- **成功标准:** 可复用的验证引擎

#### D3. Crisis Stress Test Suite
- **目标:** 标准化危机压力测试
- **数据:** 2008, 2015 Swiss, 2020 COVID, 其他危机
- **方法:** 极端情景，correlation spike, drawdown 分析
- **预期时间:** 2-3 周
- **成功标准:** 可复用的压力测试模块

---

## 推荐实施路径

### 路径 1: 长期策略优先（推荐）

**Phase 1 (2-3 个月):**
- A3: Position Sizing Methods Comparison
- A1: Time-Series Momentum Baseline
- D1: Transaction Cost Model

**Phase 2 (2-3 个月):**
- A2: Carry Trade with Crash Protection
- D2: Walk-Forward Engine
- D3: Crisis Stress Test Suite

**Phase 3 (2-3 个月):**
- B3: Cross-Sectional Momentum
- C1: Vol Targeting for Currencies
- C2: Pyramiding with Tiered Stops

**Phase 4 (按需):**
- 日内策略（B1, B2）
- 探索性策略（C3）

**总计: 6-9 个月**

### 路径 2: 日内+长期并行

**Phase 1 (2-3 个月):**
- A3: Half-Kelly Framework
- D1: Transaction Cost Model
- B1: Intraday Time-of-Day（并行）

**Phase 2 (2-3 个月):**
- A1: Time-Series Momentum
- B2: London Breakout（并行）
- D2: Walk-Forward Engine

**Phase 3 (2-3 个月):**
- A2: Carry Trade
- B3: Cross-Sectional Momentum
- D3: Crisis Stress Test

**总计: 6-9 个月**

---

## 数据采购计划

### 免费数据源（优先）
- **Dukascopy:** Tick/日线，主要货币对，2000+
- **TrueFX:** Bid-ask，2009+
- **BIS:** 央行数据，长期历史
- **FRED:** 利率，宏观数据

### 付费数据源（按需）
- **CME DataMine:** 货币期货完整历史
- **Bloomberg/Reuters:** 专业数据（如有预算）
- **TickData.com:** 高质量 tick 数据

### 数据优先级
1. **必需（立即）:** 主要货币对日度数据（20+ 年）
2. **重要（1-2 月内）:** Swap rates, roll costs
3. **有用（3+ 月）:** Tick 数据（日内策略）
4. **可选:** 高频 order book（研究用）

---

## 验收标准模板

### 策略验收标准
1. **Sharpe ratio:** > 0.5 (long-term), > 1.0 (intraday)
2. **Max drawdown:** < 30% (long-term), < 20% (intraday)
3. **Walk-forward:** 参数稳定，样本外 Sharpe > 样本内 × 50%
4. **Transaction cost:** 完整建模，净收益为正
5. **Crisis test:** 2008, 2015, 2020 回撤可控

### 基础设施验收标准
1. **可复用性:** 模块化，易于集成
2. **文档完整:** 使用说明，假设说明
3. **测试覆盖:** 单元测试，集成测试
4. **性能:** 回测速度可接受

---

## 资源需求估算

### 人力
- **全职开发:** 1 人，6-9 个月
- **或兼职:** 2-3 人，6-9 个月

### 计算
- **本地机器:** 足够（日度回测）
- **云计算:** 可选（加速）

### 数据
- **免费数据:** $0
- **付费数据:** $0 - $5,000（按需）

### 总成本估算
- **最小:** $0（纯时间投入 + 免费数据）
- **推荐:** $1,000 - $5,000（付费数据 + 云计算）

---

## 风险与不确定性

### 技术风险
- **数据质量:** 免费数据可能有缺失或错误
- **回测框架:** 开源工具可能有 bug
- **Look-ahead bias:** 需要仔细审计

### 策略风险
- **Regime shift:** 历史有效策略可能失效
- **Overfitting:** 过度优化导致样本外失败
- **Cost increase:** 实盘成本可能高于历史估算

### 市场风险
- **Liquidity:** 危机时流动性枯竭
- **Gap:** 止损失效
- **Correlation spike:** 分散失效

---

## 不推荐的项目

### X1. Martingale/Grid 系统
- **原因:** 有限资本下 ruin probability 极高

### X2. Full Kelly without Shrinkage
- **原因:** 估计误差下灾难性

### X3. "算术亏损、指数盈利"字面实现
- **原因:** 数学上不一致

### X4. 高频 HFT（微秒级）
- **原因:** 超出 scope，需专业基础设施

### X5. 新闻/情绪 NLP
- **原因:** 证据不足，超出 scope

---

## 总结

**推荐起点:**
1. A3: Position Sizing Methods Comparison（2-4 周）
2. A1: Time-Series Momentum Baseline（6-8 周）
3. D1: Transaction Cost Model（3-4 周）

**总计: 11-16 周（3-4 个月）**

完成后评估结果，决定是否继续 carry trade、cross-sectional momentum 或日内策略。

**关键成功因素:**
- 保守的参数估计
- 完整的成本建模
- 严格的 walk-forward
- 危机覆盖
- 纪律执行

**最大教训:**
- Kelly 估计误差最危险
- Martingale 在有限资本下 ruin probability 极高
- "算术亏损、指数盈利"是营销口号
- 财富过程本质是乘法的

---

**候选项目完成。建议从 Position Sizing Comparison + TSMOM + Cost Model 开始。**
