# FX 量化策略综合研究报告
# Phase A（日内不隔夜）+ Phase B（长期动态仓位）

**日期:** 2026-06-23
**Worker:** scout-worker-fx-01
**Issue:** #13
**状态:** Phase A+B 完成

---

## 研究目标

系统研究外汇交易量化策略的两条路线，为后续数据实验、回测与策略开发建立证据充分的研究底座。本研究只做公开资料研究、策略分类、风险分析和验证设计，**不提供个性化投资建议，不连接交易账户，不执行真实或模拟下单**。

---

## 两条路线对比

### Phase A：日内交易，不隔夜

**约束:**
- 持仓时间数分钟至数小时
- 日终前平仓，不承担隔夜 gap、swap 和跨日事件风险

**最强证据:**
- **FX 日内时段效应:** 5 个独立 tier1 研究（Elaut 2018, Breedon & Ranaldo 2013, Zhang 2018, Khademalomoom 2019, INSEAD）
- 货币在本地交易时段倾向于贬值，在美国时段（伦敦收盘后）升值

**相邻证据:**
- **跨货币长期动量:** Menkhoff BIS（1 研究，非日内）
- **伦敦开盘突破:** 实践共识强，学术引用存在，参数需验证

**关键风险:**
- **假突破率:** 定性共识存在，但 FX 具体率需独立验证
- **交易成本:** EUR/USD 估算 9-10 USD/lot，必须用目标 broker 实际数据
- **过拟合:** DSR/PBO 方法成熟，但阈值需校准

### Phase B：长期动态仓位管理

**核心思想验证:**
- **"亏损算术级、盈利指数级":** 作为营销口号存在，但作为严格数学描述**不成立**
- 财富过程本质是乘法的，不存在真正的"算术亏损+指数盈利"

**最强证据:**
- **Time-series momentum:** Moskowitz (2012) JFE 58 种工具，AQR 137 年，Pedersen Managed Futures Sharpe 1.8
- **Carry crash risk:** UChicago (2008) 负偏度，VIX unwind
- **Kelly 估计误差:** arXiv (2024) + practitioner consensus，fractional Kelly 作为 sizing 方法
- **Volatility targeting procyclicality:** ECB (2020) 系统性风险，2020年3月实证

**数学结论:**
- **Geometric mean < Arithmetic mean:** volatility drag = σ²/2
- **50% 损失需 100% 增长恢复:** 乘法过程不对称性
- **2× Kelly 结论:** 仅在简单二项模型的局部二次近似下成立，非普遍定理

**关键风险:**
- **Kelly estimation error:** 最危险，必须保守估计 edge/variance
- **Carry crash:** 负偏度，VIX hedge 候选
- **Vol targeting procyclical:** 波动飙升强制去杠杆
- **Pyramiding reversal:** 加仓后反转放大亏损（幅度取决于加仓规则）
- **Martingale/grid:** 有限资本、持续下注下 ruin probability 极高

---

## 证据强度对比

### Phase A 证据结构

- **独立 Tier1 FX 日内研究:** 5 个
- **Tier1 相邻证据（非日内）:** 4 个
- **Tier2-3 研究:** 8 组
- **Practitioner consensus:** 20+ 组
- **假突破率:** 定性共识强，FX 具体数字待验证

**证据质量:** FX 日内时段效应有 5 个独立验证，证据充分；其他策略多为相邻证据或实践共识。

### Phase B 证据结构

- **FX 专门 tier1 研究:** 3 studies (JFE 2021, Menkhoff BIS, Moskowitz JFE)
- **跨资产 CTA tier1 证据:** 3 studies (Moskowitz, Pedersen, AQR 137年)
- **Carry crash 专门 tier1:** 1 study (UChicago)
- **Kelly sizing tier1 paper:** 1 (arXiv)
- **Vol targeting tier1:** 2 studies (ECB, Harvey)
- **数学基础共识:** AM-GM 不等式，几何财富过程

**证据质量:** Time-series momentum 有 4 个独立 tier1 研究跨时间和资产验证；Carry crash 有专门研究；Kelly 和 vol targeting 有理论、实证和监管确认；数学结论为严格推导。

---

## 策略家族对比

### Phase A 策略（日内）

| 策略 | 证据强度 | 优先级 |
|------|----------|--------|
| FX 日内时段动量 | Tier 1 (Strong) | 优先回测 |
| 伦敦开盘突破 | Tier 2 (Moderate) | 验证适用性 |
| 协整配对交易 | Tier 2 (Moderate) | 方法有学术支持，日内适用性 TBD |
| 均值回归 | Tier 3 (Weak) | 胜率需 FX 数据验证 |
| Order Flow | Tier 3 (Weak) | 数据获取困难，latency 高 |
| Event-Driven | Tier 3 (Weak) | 成本爆炸，不可预测性高 |

### Phase B 策略（长期）

| 策略 | 证据强度 | 优先级 |
|------|----------|--------|
| Time-series momentum (1-12月) | Tier 1 (Strong) | 优先回测 |
| Carry trade (with crash awareness) | Tier 1 (Strong) | 评估 VIX hedge 成本 |
| Managed Futures / CTA | Tier 1 (Strong) | 跨资产 TSMOM + vol targeting |
| Cross-sectional momentum | Tier 1 (Strong) | 交易成本敏感 |
| Fractional Kelly sizing | Tier 1 (Strong - Sizing Method) | 与 fixed fractional、vol targeting 比较 |
| Volatility targeting | Tier 2 (Moderate) | 对货币效果有限 |
| Pyramiding | Tier 3 (Weak) | 反转风险（取决于规则） |
| Martingale/Grid | Tier 5 (Contradicted) | **永不使用** |

---

## 数据需求对比

### Phase A（日内）

**必需数据:**
- **Tick/分钟级数据:** 5+ 年，主要货币对
- **Bid-ask spread:** 历史 spread，时段变化
- **时段覆盖:** 亚洲、伦敦、纽约及重叠时段
- **事件标注:** 央行公告、重要数据发布

**数据源:**
- Dukascopy（免费 tick 数据）
- TrueFX（bid-ask）
- Broker 历史数据（必须用目标 broker）

### Phase B（长期）

**必需数据:**
- **日度/周度数据:** 20+ 年，多币对
- **远期/期货数据:** Roll cost, basis
- **Swap/rollover:** 隔夜利息
- **Crisis coverage:** 至少 2 次货币危机、2 次股市崩盘

**数据源:**
- CME 货币期货
- Bloomberg/Reuters（如有预算）
- Dukascopy 日线（免费）
- BIS 央行数据

---

## 交易成本对比

### Phase A（日内）

**成本构成:**
- **Bid-ask spread:** EUR/USD ~0.1-0.5 pips（正常），10-30× spread（新闻时）
- **Slippage:** 市价单，尤其低流动性时段
- **Commission:** 取决于 broker
- **总成本估算:** EUR/USD ~9-10 USD/lot

**成本影响:**
- 高频策略极敏感
- 必须用目标 broker 历史 bid-ask 建模

### Phase B（长期）

**成本构成:**
- **Bid-ask spread:** 较小（持仓时间长，摊薄）
- **Roll cost:** 期货 roll，远期 roll
- **Swap/rollover:** 隔夜利息（carry 策略收益来源或成本）
- **Slippage:** 仓位调整时

**成本影响:**
- 低频策略相对不敏感
- Carry 策略：swap 是收益来源
- Vol targeting：频繁调整增加成本

---

## 风险与失效对比

### Phase A（日内）Top 3 风险

1. **Overfitting:** 最小 5 年数据，200+ 笔交易；方法成熟（DSR/PBO），阈值需校准
2. **Transaction Cost:** 必须用目标 broker 历史 bid-ask 建模 + slippage，不能用估算值
3. **False Breakout:** 定性共识强（多来源），但 FX 具体率需用历史数据验证

### Phase B（长期）Top 3 风险

1. **Kelly Estimation Error:** 最危险，over-betting 导致负增长；fractional Kelly 与其他 sizing 方法需比较
2. **Carry Crash:** 负偏度，VIX 飙升 unwind；2008年10月实证
3. **Volatility Targeting Procyclicality:** 波动飙升强制去杠杆，加剧抛售；ECB 2020年3月实证

---

## 验证设计对比

### Phase A（日内）验证协议

**6 大类检查:**
1. **Overfitting:** DSR/PBO，WFE，t-stat，样本外衰减
2. **Look-ahead:** 时间戳审计，bar close vs intrabar
3. **Transaction Cost:** Broker bid-ask + slippage + commission 完整建模
4. **时段依赖:** 跨时段验证，流动性变化
5. **事件风险:** 新闻跳跃，spread 扩大
6. **Regime 依赖:** Trend vs range 子时期

**基准比较:**
- Buy-and-hold（不适用日内）
- 固定时段进出（如固定 London open/close）
- Random entry（Monte Carlo）

### Phase B（长期）验证协议

**6 大类检查:**
1. **Walk-forward:** 5 年训练，1 年测试，滚动
2. **Parameter stability:** 子时期、跨币对验证
3. **Portfolio attribution:** Signal, sizing, carry, vol target 各自贡献
4. **Crisis stress test:** 2008, 2015 Swiss, 2020 COVID
5. **Transaction cost:** Bid-ask + roll + swap + slippage 完整建模
6. **Kelly shrinkage:** Edge/variance 保守估计，与其他 sizing 方法比较

**基准比较:**
- 固定仓位（无动态调整）
- 固定风险（无 vol targeting）
- 无加仓（无 pyramiding）
- Buy-and-hold

---

## 资本、技术复杂度与可执行性对比

### Phase A（日内）

**最小资本:**
- **$10,000 - $50,000**（考虑回撤、多策略分散）
- Micro lots 可更小，但成本比例更高

**技术复杂度:**
- **高:** Tick 数据处理，实时执行，低延迟
- Bar vs tick，时间戳精度
- 事件标注，spread 建模

**可执行性:**
- **中:** 需要稳定连接，实时监控
- 可自动化，但需要监督
- Broker 选择关键（spread, execution quality）

**时间投入:**
- 开发：高（数据清洗、回测、优化）
- 运行：中（自动化后监控）

### Phase B（长期）

**最小资本:**
- **$50,000 - $100,000+**（考虑多币对分散、杠杆、margin）
- Kelly sizing 需要足够 buffer

**技术复杂度:**
- **中:** 日度/周度数据，较简单
- 但需要：vol 估计、Kelly 计算、portfolio heat 监控
- Walk-forward 回测复杂

**可执行性:**
- **高:** 低频，手动或自动化均可
- 不需要实时监控
- 可用标准 broker

**时间投入:**
- 开发：高（long-term backtest，参数优化）
- 运行：低（每日或每周调整）

---

## 容量与规模对比

### Phase A（日内）

**策略容量:**
- **小 - 中:** 高频策略受流动性限制
- EUR/USD, GBP/USD 容量较大
- 交叉盘容量小

**规模上限:**
- **~$1M - $10M** per strategy（估算，取决于币对和频率）
- 超过后 slippage 显著增加

### Phase B（长期）

**策略容量:**
- **中 - 大:** 低频策略受限较小
- Managed futures / CTA 可管理数十亿美元

**规模上限:**
- **~$10M - $1B+** per strategy（取决于币对数量和调整频率）
- 分散多币对、跨资产可扩展

---

## 心理与纪律要求对比

### Phase A（日内）

**心理挑战:**
- **高频决策疲劳**
- 盯盘压力
- 止损触发频繁

**纪律要求:**
- 严格执行止损
- 不过度交易
- 不盯盘焦虑

### Phase B（长期）

**心理挑战:**
- **大回撤耐受:** 20-40% drawdown 常见
- 长期亏损期（数月至数年）
- Carry crash 一次暴亏

**纪律要求:**
- 严格 Half-Kelly（不因自信 over-bet）
- 不在回撤中放弃策略
- 不手动干预系统信号

---

## Phase B 核心结论："算术亏损、指数盈利"的真相

### 数学审计结论

**字面意义:** 数学上不一致。财富过程不能同时服从加法（亏损）和乘法（盈利）。

**可能的合理解释:**
1. **固定风险 + 盈利加仓:** 理论上可行，但成立条件极严格（无 gap、无 whipsaw、有限亏损次数）
2. **正偏度策略:** 小亏、大赢分布，但仍是几何过程
3. **Kelly 控制:** 限制单次亏损比例，但不改变乘法本质

**反例:**
- 连续 10 次 2% 止损 = 18.3% 几何亏损（非 20% 算术）
- 2× 仓位反转 15% = 76% 亏损
- Gap 可使止损失效，实际亏损远超预期

**最终判断:**
**"亏损算术级、盈利指数级"是营销口号，非严格数学描述。**

更准确的描述应该是：
- 通过严格止损和仓位管理，**限制单次和累积亏损幅度**
- 通过趋势跟随和正偏度策略，**在趋势持续时获得超线性收益**
- 但这仍然是**几何财富过程**，只是通过策略设计优化了收益分布

**不存在真正意义上的"算术亏损+指数盈利"的数学免费午餐。**

---

## 推荐后续实验路线

### 路线选择决策树

**如果资本 < $50k，时间有限，偏好自动化:**
→ **暂缓日内，优先 Phase B 长期策略**
- Time-series momentum (look-back 需实验网格)
- Position sizing methods (fractional Kelly vs fixed fractional vs vol targeting)
- Vol targeting (目标波动率需实验验证)
- 日度调整，可半自动化

**如果资本 > $50k，有开发能力，能接受高技术复杂度:**
→ **Phase A 日内 + Phase B 长期 组合**
- Phase A: FX 日内时段动量（最强证据）
- Phase B: Time-series momentum + carry
- 分散风险，多时间尺度

**如果追求最强学术支持，低频执行:**
→ **Phase B 纯长期组合**
- Time-series momentum (Moskowitz, AQR)
- Carry trade with crash control (UChicago)
- Managed Futures 风格（Pedersen）
- Position sizing methods 实验比较

### 最小可行回测组合（Phase B）

**策略实验网格:**
1. Time-series momentum (多个 look-back 候选：1/3/6/12月)
2. Carry trade (interest differential, VIX cut 阈值候选)
3. Sizing methods (fractional Kelly vs fixed fractional vs vol targeting vs risk-constrained)
4. Vol targeting (目标波动率候选：5%/10%/15%)

**数据:**
- 10+ 主要货币对
- 20+ 年日度数据
- Swap/roll cost 数据

**验证:**
- Walk-forward 5+1 年滚动
- Crisis stress test (2008, 2015, 2020)
- Transaction cost 完整建模
- Baseline 比较（fixed position, no pyramiding）

---

## 局限性与不确定性

### Phase A 局限

1. **FX 具体假突破率缺失:** 定性共识强，但缺乏 FX 专门的量化数据
2. **Broker 依赖:** 交易成本建模必须用目标 broker 实际数据
3. **时段效应幅度:** 学术研究未给出可交易的具体 pips 数字
4. **配对交易日内适用性:** 方法有学术支持，但日内 FX 实证不足

### Phase B 局限

1. **长期样本不足:** 20年数据仅覆盖有限 regime
2. **Carry crash 频率低:** 历史上罕见，统计推断不确定
3. **Pyramiding 实证薄弱:** 理论支持存在，但反转回吐量化不足
4. **Vol targeting 对货币效果有限:** Harvey 研究显示主要对 risk assets 有效

### 研究局限

1. **公开资料搜索范围:** 互联网可及，但非穷尽所有研究
2. **时间敏感性:** 市场微观结构可能已变化
3. **Publication bias:** 成功策略可能不发表
4. **Backtest ≠ Live:** 历史回测不代表未来收益

---

## 不提供的内容（明确声明）

本研究**不提供**以下内容：
1. **个性化投资建议:** 不针对任何个人财务状况
2. **收益承诺:** 不承诺任何具体收益率或胜率
3. **交易信号:** 不提供买卖时机建议
4. **账户连接:** 未连接任何交易账户或经纪商
5. **真实/模拟下单:** 未执行任何交易
6. **持牌建议:** 本研究非持牌投资顾问服务

**风险提示:** 杠杆交易风险极高，历史回测不代表未来，市场微观结构变化可能使策略失效。

---

## 总结

两条路线各有优势和适用场景：

**Phase A（日内）:** 适合有开发能力、能接受高技术复杂度、偏好短周期的交易者。最强证据是 FX 日内时段效应（5 个独立研究），但交易成本建模和假突破率需要用实际 FX 数据验证。

**Phase B（长期）:** 适合资本充足、能承受大回撤、偏好低频的交易者。Time-series momentum 和 carry trade 有充分长期实证，但必须严格执行 Half-Kelly 和风险控制。**"算术亏损、指数盈利"在数学上不成立**，财富过程本质是乘法的，不存在免费午餐。

**最大教训:** Kelly 估计误差是最危险的陷阱，martingale/grid 保证破产，vol targeting procyclicality 是系统性风险。严格的风险管理和现实预期是成功的基础。

---

**Phase A+B 综合研究完成。**
