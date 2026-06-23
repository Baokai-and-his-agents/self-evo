# Issue #15: PR #14 修订建议清单

**Date:** 2026-06-23  
**Worker:** scout-worker-fx-sizing-01  
**Run ID:** 2026-06-23-fx-sizing-001

---

## 修订建议总览

基于 Issue #15 专项研究（有限递增试探仓位），对 PR #14（外汇量化研究）的相关结论给出修订建议。

**修订原则：**
- 保留：结论正确且有证据支持
- 修正：结论方向正确但表述需更精确
- 补充：缺失重要边界条件或警告
- 替换：结论与实证不符，需重新表述

---

## 1. "算术亏损、指数盈利"表述

### 当前结论（PR #14）
> "算术亏损、指数盈利"是营销口号，非严格数学描述。财富过程本质是乘法的，不存在真正意义上的"算术亏损+指数盈利"。

### 修订建议：**修正**

**修正为：**
> "算术亏损、指数盈利"作为字面财富路径在数学上不可能（财富过程乘法性质）。但该表述可能指代**合理的机制解释空间**：
> 
> 1. **仓位路径可递增**：震荡期小仓试探（多次小亏），趋势期大仓获利（少数大赢）
> 2. **收益分布偏度**：策略可制造正偏度分布（小亏多次、大赢少次）
> 3. **与固定仓位对比**：相同信号下，动态仓位可能改变总收益分布
> 
> **关键区别：**
> - 字面不可能：单期财富变化不能同时算术和指数
> - 合理解释：仓位序列设计可优化收益分布形状
> 
> **但必须明确：**
> - 仓位递增本身不创造 edge（若信号无 edge）
> - 需要条件概率改善（止损后胜率或盈亏比上升）
> - 若条件概率恒定（i.i.d.），递增仅重新分配风险，在理想假设下不改善几何增长率
> - 实际效果需实证检验

**理由：**
- Issue #15 数学模型显示：有限递增可改变收益分布（正偏度）
- 但关键前提：止损是否提供 regime 信息
- Query 9 结果：false breakout 不预测趋势（前提不支持）

---

## 2. Martingale 风险结论

### 当前结论（PR #14）
> 无限 Martingale 在有限资本下风险极高，不应使用。

### 修订建议：**补充**

**补充内容：**
> **Martingale 风险等级分类：**
> 
> 1. **无限 Martingale（无上限）**：必然破产（有限资本下）
> 2. **有限 Martingale（有上限 K）**：延长寿命但仍有高破产风险
>    - Query 7 实证：账户平均寿命 1-2 年
>    - Fat tail 风险：小概率巨额亏损（Kurtosis 88.03）
>    - ForexOp 模拟：最坏情况 -772 pips vs 平均 +4.48 pips
> 
> 3. **有限 + 总风险预算约束**：进一步降低风险，但仍非安全
>    - P(ruin) = (1-p)^(K+1)
>    - Budget 约束限制最大亏损，但无法消除 fat tail 特征
> 
> **关键发现（Query 7）：**
> - 所有来源一致**强烈反对** Martingale（包括有限版本）
> - Trend 中失败："Doubling down against prevailing trends"
> - 唯一适用场景：理论赌场（无限资本 + 无限时间）
> 
> **有限递增试探仓位的定位：**
> - 若止损序列无预测性 → 有限 Martingale 变种
> - 继承 Martingale 风险特征（fat tail, 高破产率）
> - Query 9：止损序列预测性**未验证**

**理由：**
- PR #14 正确指出无限 Martingale 风险
- 但未充分讨论有限版本与本机制的关系
- Issue #15 发现：本机制在连续谱上介于固定仓位和有限 Martingale 之间

---

## 3. Kelly Criterion 应用

### 当前结论（PR #14）
> Kelly 估计误差导致 over-betting 风险，应使用 fractional Kelly。

### 修订建议：**补充**

**补充内容：**
> **Kelly 与动态仓位的关系：**
> 
> 1. **标准 Kelly 假设**：固定 p 和 R，推荐固定 f*
> 2. **动态 Kelly 场景**：
>    - 若 p 或 R 随状态变化 → Kelly 应动态调整
>    - 递增仓位隐含假设：p_{n+1} > p_0（止损后胜率上升）
>    - 或 R_{n+1} > R_0（止损后盈亏比改善）
> 
> 3. **Kelly 与递增仓位的冲突**（重要）：
>    - 若 p 恒定，Kelly 推荐恒定 f*，**非递增**
>    - 递增仓位要么是 Kelly 偏离（over-betting 风险）
>    - 要么隐含假设条件概率改善（需验证）
> 
> 4. **实证对比（Query 7）**：
>    - Thorp Kelly Criterion: 19.1% 年化，无亏损年（1969-1988）
>    - Kelly 根据 edge 调整，Martingale 根据历史结果调整
>    - **结论**：Kelly 是数学正确的 anti-martingale
> 
> **建议：**
> - 优先使用 fractional Kelly (1/4 - 1/2 Kelly)
> - 若使用动态仓位，必须验证条件概率确实改善
> - 递增仓位需 Kelly 上限约束（r_n ≤ Kelly-half）

**理由：**
- PR #14 正确指出 Kelly 估计误差
- 但未讨论 Kelly 与动态仓位的理论关系
- Issue #15 发现：Kelly 假设与递增仓位存在理论冲突

---

## 4. Position Sizing 方法

### 当前结论（PR #14）
> 推荐 ATR-based position sizing 和 volatility normalization。

### 修订建议：**保留并补充**

**补充内容：**
> **Position Sizing 方法分类与实证：**
> 
> **Tier 1（强实证支持）：**
> 1. **Fixed-Fractional Kelly**
>    - 理论：Kelly (1956), Thorp (1962)
>    - 实证：Thorp 19.1% 年化（1969-1988），无亏损年
>    - 适用：有 edge 的信号
> 
> 2. **Anti-Martingale（盈利后加仓）**
>    - 理论：Trend-following 标准做法
>    - 实证：Query 7 对比，Anti-Martingale 在趋势中优于 Martingale
>    - 适用：趋势市场
> 
> 3. **Turtle Pyramiding**
>    - 理论：ATR-based units + 0.5N pyramiding
>    - 实证：1983-1987 实盘 80%+ 年化
>    - 适用：突破策略 + 趋势跟随
> 
> **Tier 2（相邻理论，实践验证）：**
> 4. **HMM Regime-dependent Sizing**
>    - 理论：Regime detection → 仓位标量
>    - 实践：Bull 100% / Bear 25% / High-vol 10%（多来源一致）
>    - 适用：可靠 regime detection
> 
> 5. **VIX/Volatility Regime Sizing**
>    - 理论：波动率反比缩放
>    - 实践：VIX < 16: 1.0x, VIX > 25: 0.3x
>    - 适用：多资产组合
> 
> **Tier 3（理论上可能，实证不足）：**
> 6. **有限递增试探仓位（Issue #15 研究对象）**
>    - 理论：止损后递增，假设 regime 信息
>    - 实证：**直接支持不存在**（Query 1-9）
>    - 风险：若假设不成立，退化为有限 Martingale
>    - 状态：**不推荐实盘**，仅作研究实验
> 
> **主流共识（Query 1-9 一致）：**
> - 止损/亏损 → **减仓**（风险管理 101）
> - 盈利/趋势确认 → **增仓**（anti-martingale）
> - 高波动/不确定 → **减仓**（regime switching）

**理由：**
- PR #14 正确推荐 ATR-based sizing
- 但未完整列出 position sizing 方法谱系
- Issue #15 补充各方法的实证状态和适用边界

---

## 5. 风险管理实践

### 当前结论（PR #14）
> 建议 2% 单次风险上限，总风险控制。

### 修订建议：**保留并补充**

**补充内容：**
> **风险管理分级实践：**
> 
> **Level 1（单次交易）：**
> - 2% 单次风险上限（标准）
> - 1% 更保守（推荐 fractional Kelly）
> - 止损距离：2 ATR（Turtle 标准）
> 
> **Level 2（策略层面）：**
> - 策略 drawdown 止损：20%
> - 连续失败上限：3 个完整周期
> - 日亏损上限：5% equity
> 
> **Level 3（组合层面）：**
> - 单市场最大 units：4（Turtle）
> - 相关市场：6 units（Turtle）
> - 单方向总计：12 units（Turtle）
> 
> **Level 4（极端事件）：**
> - Gap 缓冲：Budget × 1.5
> - 避免持仓过周末（重大新闻周）
> - 新闻日历过滤：ECB, Fed, NFP 前后暂停
> 
> **动态风险调整（Query 5-6 发现）：**
> - Drawdown 5-15% → 减仓至 25%（AlgoKing 实践）
> - ADX < 20 → 减仓或暂停（震荡市场）
> - VIX > 25 → 减仓至 30-50%
> - **关键**：高不确定性 → 减仓，非增仓
> 
> **禁止行为（Query 7 Martingale 教训）：**
> - ✗ 亏损后增仓（除非有可验证的条件概率改善）
> - ✗ 超出 Kelly 上限
> - ✗ 忽略相关性（多个 correlated positions）
> - ✗ 报复性交易（revenge trading）

**理由：**
- PR #14 风险管理建议正确但简略
- Issue #15 补充分级风险控制和动态调整
- 整合 Turtle, HMM regime, Martingale 教训

---

## 6. 回测方法论

### 当前结论（PR #14）
> 需要 walk-forward validation 和跨市场验证。

### 修订建议：**保留并补充**

**补充内容：**
> **回测最佳实践（整合 Issue #15 发现）：**
> 
> **1. 数据质量：**
> - Tick data 验证关键时期（2008, 2015 Swiss, 2020 COVID）
> - Bid-ask spread 完整建模
> - 包含下市品种（survivorship bias）
> - 避免 lookahead bias
> 
> **2. 对照组设计（Issue #15 协议）：**
> - A. 固定仓位（基准）
> - B. 止损后有限递增（实验组）
> - C. 盈利后加仓（Anti-Martingale）
> - D. Turtle Pyramiding（趋势确认后）
> - E. 随机置换基线（检验路径依赖价值）
> - **必须**：同时运行所有对照组，使用相同数据和信号
> 
> **3. Walk-Forward 严格协议：**
> - 训练：5 年
> - 测试：1 年（OOS）
> - 滚动：每 1 年重新训练
> - **禁止**：测试集参数调整
> 
> **4. 极端情景测试：**
> - 2008 Financial Crisis
> - 2015-01-15 Swiss Franc unpegging
> - 2020-03 COVID crash
> - **目的**：验证 gap/极端事件下生存能力
> 
> **5. Monte Carlo 与置换测试：**
> - 1000+ runs Monte Carlo
> - 序列置换：随机打乱交易顺序
> - **检验**：路径依赖是否创造真实价值
> - 若置换后策略失效 → 可能只是曲线拟合
> 
> **6. 成本敏感性分析：**
> - 0.5× 成本（理想）
> - 1× 成本（真实）
> - 2× 成本（保守）
> - **结论必须在 1× 成本下成立**
> 
> **7. 参数稳定性测试：**
> - 参数微小变化（±10%）结果稳定性
> - 不稳定 → overfitting 警示
> - 选择参数稳定区域，非单点最优

**理由：**
- PR #14 回测方法正确但不够详细
- Issue #15 补充严格的对照组设计和验证协议
- 整合 Monte Carlo, 置换测试等反 overfitting 方法

---

## 7. 缺失讨论补充

### PR #14 未充分讨论的主题

**补充 1：Sequential Testing 理论**
> **SPRT (Sequential Probability Ratio Test)** 为相邻理论：
> - Wald 1945 最优序贯检验
> - 应用于 change-point detection（Query 4）
> - 但未见用于"止损序列 → 仓位递增"
> - **可能价值**：若能证明止损序列提供 regime 信息，SPRT 可量化后验概率

**补充 2：Change-Point Detection 应用**
> **CPD 在交易中的标准用法**（Query 5）：
> - BOCPD, PELT, DC+HMM 用于 regime 识别
> - 识别后标准反应：**减仓或策略切换**，非增仓
> - 与本机制的区别：CPD 识别变化点，本机制假设止损聚集预测变化点
> - **关键缺失**：止损聚集是否真的预测 regime 切换？Query 9 结果：否

**补充 3：Hazard Rate 与 Trend Emergence**
> **关键实证问题**（Query 9）：
> - P(趋势开始 | 已 n 次止损) 是否随 n 递增？
> - False breakout 是否聚集在趋势前？
> - **实证答案**：否
>   - 50-70% breakout 为 false（尤其 Asian session）
>   - False breakout 是噪音，非信号
>   - 主流策略：避免或 fade（mean-reversion），非利用其预测
> - **结论**：止损序列预测趋势的假设**不支持**

**补充 4：Campaign Trading / Layered Entries**
> **Turtle 风格多次入场**（Query 8）：
> - 触发条件：**盈利后**（价格移动 0.5N）
> - 最大 4 units per market
> - 与止损后递增**方向相反**
> - 实证：1983-1987 实盘 80%+ 年化

---

## 8. 修订后建议配置（实验网格，非推荐）

### 当前（PR #14）
> 提供默认推荐配置。

### 修订建议：**替换**

**替换为：仅提供实验网格，明确非推荐**

```python
# 实验网格（用于对照回测，非推荐配置）

# 对照组 A：固定仓位（基准）
config_A = {
    "type": "fixed",
    "risk_per_trade": 0.01  # 1%
}

# 对照组 B：止损后有限递增（Issue #15 实验）
config_B = {
    "type": "progressive_probe",
    "r_0": 0.01,
    "d": 0.005,  # 算术递增
    "K": 5,
    "budget": 0.10,
    "WARNING": "核心假设未验证，不推荐实盘"
}

# 对照组 C：Anti-Martingale（推荐）
config_C = {
    "type": "anti_martingale",
    "r_0": 0.01,
    "multiplier": 1.5,
    "max_risk": 0.05,
    "RECOMMENDATION": "实证支持，优先考虑"
}

# 对照组 D：Turtle Pyramiding（推荐）
config_D = {
    "type": "turtle",
    "unit_risk": 0.01,
    "max_units": 4,
    "pyramid_step": 0.5,  # 0.5N
    "RECOMMENDATION": "1983-1987 实证验证"
}
```

**理由：**
- PR #14 提供"推荐配置"可能误导（未充分验证）
- 应明确区分：实验网格 vs 推荐配置
- Issue #15 发现：止损后递增无直接实证支持

---

## 9. 最终建议总结

### 保留（无需修改）
- ✓ ATR-based position sizing 推荐
- ✓ 2% 单次风险上限
- ✓ Walk-forward validation 必要性
- ✓ 交易成本完整建模

### 修正（需更精确表述）
- ⚠ "算术亏损、指数盈利"解释：从"营销口号"改为"有合理解释空间但需验证假设"
- ⚠ Kelly 应用：补充与动态仓位的理论关系

### 补充（增加重要内容）
- ➕ Martingale 风险等级分类（无限 vs 有限 vs 有预算）
- ➕ Position sizing 方法完整谱系与实证状态
- ➕ 分级风险管理（单次/策略/组合/极端事件）
- ➕ Sequential testing, Change-point, Hazard rate 理论
- ➕ 回测严格协议（对照组、Monte Carlo、置换测试）

### 替换（需重新表述）
- ✗ "默认推荐配置"→ "实验网格（非推荐）"
- ✗ 删除任何暗示"止损后递增有效"的表述

---

## 10. PR #14 与 Issue #15 关系说明

**Issue #15 的定位：**
- 独立研究，专注"有限递增试探仓位"机制
- 不是 PR #14 的否定，而是**深化与边界澄清**
- 补充 PR #14 未充分讨论的理论与实证

**两者协同价值：**
- PR #14：外汇量化研究基础，覆盖多个策略方向
- Issue #15：深入单一机制，提供严格的实证检验框架
- **共同产出**：明确哪些策略有实证支持，哪些仅为理论假设

**对用户的价值：**
- 避免盲目实施未验证策略（如止损后递增）
- 提供实证支持的替代方案（Anti-Martingale, Turtle, Kelly）
- 建立严格的实证检验标准（对照组、Monte Carlo、置换测试）

---

## 11. 实施优先级

**高优先级（必须修正）：**
1. 删除任何"推荐止损后递增"的表述
2. 补充 Martingale 风险分级
3. 明确实验网格 vs 推荐配置

**中优先级（建议补充）：**
4. Position sizing 方法完整谱系
5. 分级风险管理
6. 回测严格协议

**低优先级（锦上添花）：**
7. Sequential testing 理论介绍
8. Hazard rate 实证讨论
9. Campaign trading 对比

---

**PR #14 修订建议清单完成。**
