# Progressive Probe Position Sizing - Exploration Brief

**Date:** 2026-06-23
**Worker:** scout-worker-fx-sizing-01
**Run ID:** 2026-06-23-fx-sizing-001
**Issue:** #15
**Base:** PR #14 HEAD (b17c1e2)

---

## 背景

Issue #13 / PR #14 研究结论将"亏损算术级、盈利指数级"判定为**营销口号，非严格数学描述**，并指出财富过程本质是乘法的，不存在真正意义上的"算术亏损+指数盈利"。

但该结论可能对用户真实机制理解不充分。用户机制的核心不是字面的"算术 vs 指数"财富路径，而是：

> **在震荡阶段用小仓位多次试探并止损；每次止损后，在严格上限和总风险预算内逐级提高下一次试探仓位；趋势建立后，由较大仓位获得高 R 收益，以少数大盈利覆盖此前多次小额止损。**

这是一个**状态依赖的仓位递增策略**，具有：
1. 有限递增（有上限 K，非无限 Martingale）
2. 总风险预算约束（非破产式下注）
3. 试探-确认两阶段（震荡试错 → 趋势放大）
4. 重置机制（完成周期后归零）

本研究必须：
- **精确定义该机制**，而非预先判定为 Martingale 或无效
- **数学审计其期望、方差、偏度、破产概率**
- **区分它与相关策略的连续谱关系**
- **寻找相邻理论与实证证据**
- **设计可证伪的实验协议**

---

## 核心研究问题

### 1. 机制形式化

**状态空间：**
- 震荡试探（probing）
- 趋势确认（confirmation）
- 趋势跟随（trending）
- 完成或失败（terminal）

**仓位规则：**
- 初始风险 r0（如 1%）
- 算术递增：r_n = r0 + n × d，上限 r_max = r0 + K × d
- 几何递增：r_n = r0 × m^n，上限 r_max
- 风险类型：固定金额 vs 当前权益比例

**止损与递增：**
- 第 n 次止损后，第 n+1 次仓位 = f(n, 历史止损序列)
- 递增条件：止损触发（非时间或其他）

**趋势确认：**
- 何时判定"趋势建立"？
- 价格突破、持续时间、R 倍数、技术指标？

**重置规则：**
- 成功完成：获得 > threshold R，重置到 r0
- 失败终止：累计风险 > 预算上限，停止或重置
- 时间重置：N 个交易日无新信号

**总风险预算：**
- 单周期最大累计风险：如 10% 权益
- 到达预算后：强制重置或停止

### 2. 数学分析

**Break-even 条件：**

设前 n 次止损，每次亏损 r_i，累计亏损：
```
L_n = Σ r_i  (算术风险)
或
L_n = 1 - Π(1 - r_i)  (几何风险)
```

第 n+1 次获胜，需要 R 倍数满足：
```
R × r_{n+1} ≥ L_n + C_{n+1}
```
其中 C_{n+1} 是总交易成本。

**关键问题：**
- R 需求是否随 n 线性、二次还是指数增长？
- 算术递增 vs 几何递增的 break-even R 差异？
- 上限 K 的影响？

**期望收益：**

假设前 n 次止损后，第 n+1 次：
- 条件胜率 p_{n+1}
- 盈亏比 R_{n+1}
- 仓位 r_{n+1}

期望：
```
E[G_{n+1} | n losses] = p_{n+1} × r_{n+1} × R_{n+1} - (1 - p_{n+1}) × r_{n+1}
```

**关键争议：**
- 若 p_{n+1} = 恒定 p（止损不提供信息），递增仓位是否只是重新分配风险？
- 若 p_{n+1} > p（止损提供 regime 信息），何时成立？

**方差与偏度：**
- 递增仓位是否增加方差？
- 正偏度（小亏多次、大赢一次）的量化
- 与 Kelly 准则的关系

**Risk of Ruin：**
- 连续 K 次止损，到达上限后，累计亏损 = ?
- 在总预算约束下，破产概率 P(ruin | p, R, K, budget)
- 与无限 Martingale 的对比

### 3. 策略谱系与区分

| 策略类型 | 触发条件 | 递增方向 | 上限 | 风险预算 | 本机制关系 |
|---------|---------|---------|------|---------|-----------|
| 固定仓位 | - | 无 | - | 隐式 | 基准对照 |
| Fixed Fractional | - | 无 | - | 权益比例 | 特例：d=0 |
| Martingale (无限) | 亏损 | 加倍 | 无 | 无 | **不同**：本机制有限 |
| Martingale (有限) | 亏损 | 加倍 | K 次 | 有限资本 | **相邻**：本机制算术/几何可选 |
| Anti-Martingale | 盈利 | 递增 | 可选 | 可选 | **不同**：本机制止损递增 |
| Pyramiding | 盈利 | 加仓 | 趋势反转 | 可选 | **后半段相似**：趋势跟随阶段 |
| Kelly / Fractional Kelly | - | 根据 edge/var | 隐式 | 权益比例 | **sizing 方法**：可用于 r_n |
| Vol Targeting | - | 根据波动率 | 目标 vol | 隐式 | **sizing 方法** |
| Regime-dependent sizing | 状态后验 | 根据置信度 | 可选 | 可选 | **相邻**：本机制隐含 regime 推断 |
| Sequential testing | 证据累积 | - | 停止规则 | 可选 | **理论相邻** |
| Optimal stopping | - | - | 停止规则 | 可选 | **理论相邻** |

**关键区分点：**
1. **递增触发：** 本机制 = 止损后递增（非盈利后）
2. **上限与预算：** 本机制 = 有限 K + 总预算，非无限
3. **两阶段：** 试探（小仓 → 大仓）+ 趋势（大仓保持或加仓）
4. **隐含假设：** 止损序列提供 regime 信息（震荡 → 趋势切换点）

### 4. 条件概率与信息价值

**核心问题：止损是否提供信息？**

**场景 A：止损无信息（i.i.d. 假设）**
- 每次交易胜率恒定 p，盈亏比恒定 R
- 前 n 次止损不改变 p_{n+1} = p
- 递增仓位 → 仅重新分配风险，不改变期望增长率
- **结论：无增量价值，可能增加破产风险**

**场景 B：止损提供 regime 信息**
- 假设市场在震荡/趋势间切换
- 连续止损 → 震荡持续，但趋势即将到来（hazard rate 上升）
- p_{n+1} > p 或 R_{n+1} > R
- **结论：若条件概率确实上升，递增有理论价值**

**需要证据：**
1. **Change-point detection:** 止损聚集是否预测 regime 切换？
2. **Hazard rate:** P(趋势开始 | 已 n 次止损) 是否递增？
3. **假突破聚集:** 假突破是否聚集在趋势前？
4. **自相关:** 止损序列是否负自相关（mean reversion）？

**检索关键词：**
- FX regime switching / change-point detection
- Time-to-trend after false breakouts
- Sequential hypothesis testing in trading
- Adaptive position sizing / dynamic sizing
- Martingale vs anti-martingale empirical
- Trend confirmation lag / whipsaw clustering

### 5. 失效场景与敏感性

**交易成本：**
- 每次试探成本 c，n 次累计 n × c
- break-even R 上升：R_min = (L_n + n × c) / r_n
- 高成本可能使任何 R 都不够

**滑点与 Gap：**
- 止损滑点使实际亏损 > r_i
- Gap 跳空可能直接破产
- 递增仓位放大 gap 风险

**假突破持续：**
- 若震荡持续 > K 次，到达上限
- 大仓位仍在震荡中，损失放大

**趋势延迟：**
- 趋势建立需要时间，早期仍可能止损
- 确认延迟 → 错过早期低成本入场

**趋势反转：**
- 加仓后突然反转（类似 PR #14 的 pyramiding 风险）
- 大仓位回吐

**保证金与杠杆：**
- FX 杠杆高，大仓位可能触及保证金限制
- 强制平仓风险

**重置规则敏感：**
- 重置太频繁 → 无法递增到大仓
- 重置太晚 → 累计亏损过大

### 6. 实验设计

**对照组（至少 7 组）：**

A. **固定仓位重复试探**
   - r = r0，每次相同
   - 基准：无 sizing 优化

B. **止损后算术递增（有上限）**
   - r_n = r0 + n × d，max K 次
   - 本机制核心

C. **止损后几何递增（有上限）**
   - r_n = r0 × m^n，max K 次
   - 类 Martingale，但有限

D. **盈利后加仓（anti-Martingale）**
   - 止损保持 r0，盈利后递增
   - 对照：递增方向相反

E. **固定小仓试探 + 趋势确认后一次性放大**
   - 试探期固定 r0
   - 确认后直接跳到 r_large
   - 对照：无逐级递增

F. **根据 regime posterior 调整仓位**
   - HMM / change-point 模型输出置信度
   - 仓位 = f(置信度)
   - 对照：显式 regime 推断

G. **随机置换基线**
   - 信号不变，随机打乱仓位序列
   - 或随机打乱交易顺序
   - 对照：检验路径依赖是否真实创造价值

**参数网格（实验用，非推荐）：**
- r0: 0.5%, 1%, 2%
- d (算术增量): 0.5%, 1%
- m (几何倍数): 1.5, 2.0
- K (最大档位): 3, 5, 10
- R_confirm (趋势确认 R): 2, 3, 5
- Budget (总风险预算): 5%, 10%, 15%

**数据：**
- 主要货币对：EUR/USD, GBP/USD, USD/JPY, AUD/USD
- 频率：日线或 H4（避免日内过拟合）
- 时间：20+ 年，包含多次震荡-趋势周期
- 成本：完整 bid-ask + slippage + swap 建模

**验证协议：**
1. **Walk-forward:** 5 年训练，1 年测试，滚动
2. **子时期:** Trend period vs Range period 分别测试
3. **跨币对:** 主要货币对 + 交叉盘
4. **Monte Carlo:** 随机置换止损/盈利序列
5. **Crisis stress:** 2008, 2015 Swiss, 2020 COVID
6. **成本敏感性:** 0.5× / 1× / 2× 成本

**评估指标：**
- Sharpe ratio
- Max drawdown
- Win rate
- Avg win / avg loss
- Risk of ruin (估计)
- Calmar ratio
- Sortino ratio
- Skewness / Kurtosis

---

## 证据检索策略

### 优先级 1：直接证据（最需要但可能不存在）

1. **有限递增试探仓位的学术研究**
   - "progressive position sizing after losses"
   - "adaptive sizing based on drawdown"
   - "limited martingale in trend following"

2. **止损序列的信息价值**
   - "information content of stop losses"
   - "predictive power of false breakouts"
   - "whipsaw clustering before trends"

### 优先级 2：相邻理论

3. **Sequential testing & change-point**
   - Sequential probability ratio test (SPRT)
   - Bayesian change-point detection
   - Online change-point detection algorithms

4. **Regime switching**
   - Hidden Markov Models in FX
   - Markov-switching GARCH
   - Regime-dependent position sizing

5. **Optimal stopping**
   - Optimal stopping in trading
   - Secretary problem analogues
   - Time-to-trend estimation

6. **Martingale 理论与实证**
   - Finite martingale vs infinite
   - Martingale in FX empirical tests
   - Anti-martingale vs martingale performance

7. **Trend following sizing**
   - Turtle trading units
   - Van Tharp position sizing
   - ATR-based position sizing
   - Volatility-adjusted entry

8. **Campaign trading**
   - Multiple entries in same direction
   - Layered entries
   - Building positions

### 优先级 3：实践文献

9. **Professional risk management**
   - CTA / managed futures position management
   - Professional trader position sizing rules
   - Proprietary trading desk rules

10. **历史案例**
    - Turtle traders documentation
    - Seykota, Dunn, trend followers
    - Academic case studies

### 优先级 4：数学基础

11. **Gambler's ruin with finite doubling**
12. **Kelly criterion variants**
13. **Ruin probability with budget constraints**

---

## 证据标准

**Tier 1 (Strong):**
- 学术期刊：JFE, JF, RFS, Management Science, Operations Research
- 央行/监管：BIS, Fed, ECB working papers
- 顶级会议：AFA, NBER, Econometric Society

**Tier 2 (Moderate):**
- 良好期刊：Journal of Trading, J. Portfolio Management
- Working papers (SSRN, arXiv) 有引用
- 行业白皮书：AQR, Bridgewater, Man Group

**Tier 3 (Weak):**
- SSRN/arXiv 未发表
- 行业报告无同行评审
- 书籍（非教科书）

**Tier 4 (Anecdotal):**
- 论坛、博客、培训材料
- 仅作线索，不作证据

**Tier 5 (Contradicted):**
- 已被学术研究证伪
- 已知存在严重方法论缺陷

**记录要求：**
- URL / DOI
- 标题、作者、机构、年份
- 市场、频率、样本期、样本量
- 证据层级
- 直接 / 相邻 / 反对
- 关键结论
- 局限性
- 访问时间

---

## 交付文件结构

1. **本文件：exploration brief**
2. **query_matrix.md:** 查询矩阵，覆盖边界
3. **source_decisions.md:** 证据账本
4. **mathematical_model.md:** 完整数学推导
5. **strategy_specification.md:** 状态机与伪代码
6. **failure_landscape.md:** 失败模式
7. **evidence_map.md:** 证据强度分布
8. **backtest_protocol.md:** 完整实验规格
9. **pr14_revision_recommendations.md:** PR #14 结论修订建议
10. **daily_report.md:** 研究综合报告（中文）
11. **project_candidate.md:** 代码实现项目规格
12. **run_summary.md:** 运行总结

---

## PR #14 相关结论初步判断

需要**修正或补充**的结论（待完成研究后确认）：

1. **"算术亏损、指数盈利是营销口号"**
   - 过于绝对，未充分理解用户机制
   - 应修正为：区分字面不可能 vs 合理解释空间

2. **财富过程乘法性质**
   - 数学正确，但未区分"财富累积乘法" vs "单期仓位序列可递增"
   - 应补充：仓位路径可优化收益分布

3. **Martingale 结论**
   - 正确指出无限 Martingale 在有限资本下风险极高
   - 但未讨论有限、有预算的递增与 Martingale 的区别
   - 应补充：有限递增的连续谱位置

4. **Kelly 估计误差**
   - 正确指出 over-betting 风险
   - 但未讨论递增 sizing 的 Kelly 应用
   - 应补充：动态 Kelly 或 fractional Kelly 在递增中的角色

5. **缺失讨论**
   - 止损序列的信息价值（regime 推断）
   - Sequential testing 理论
   - 两阶段策略（试探 + 趋势）
   - Campaign trading / layered entries

---

## 研究约束确认

- ✅ 严格串行、单 worker
- ✅ 不启动 subagent
- ✅ 不并行调用上游模型
- ✅ 遇到 429 使用退避
- ✅ 最大化消耗 Clawbie token 做检索、推导
- ✅ Agent-Reach/Exa、Firecrawl 用于批量检索
- ✅ Grok 仅在 X.com 核心证据必要时使用
- ✅ 不真实交易，不连接 broker
- ✅ GitHub 身份 clawbie
- ✅ 面向人类审阅内容使用中文

---

## 下一步

1. 创建 query matrix
2. 数学模型推导
3. 证据检索（分阶段，串行）
4. 失效场景分析
5. 实验协议设计
6. PR #14 修订建议
7. 综合报告与交付

**当前状态：** Exploration brief 完成，开始 query matrix 和数学模型。
