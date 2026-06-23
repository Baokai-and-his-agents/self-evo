# PR #16 证据与数学修正日志

**日期:** 2026-06-23
**修正原因:** CHANGES_REQUESTED 审查 - 证据不可重建和数学表述错误
**修正范围:** 所有 Issue #15 相关文档

---

## 修正原则

1. **证据可追溯性**: 只保留可提供 canonical URL/DOI/ISBN 的来源
2. **阴性结论准确性**: "检索未找到" ≠ "事实不存在"
3. **数学严谨性**: 明确假设和适用范围，不过度概括
4. **参数候选性**: 所有数值参数标记为 illustrative/candidate
5. **下一步实证性**: 删除真实资金 pilot，只推荐 offline backtest

---

## 已删除的不可重建数字

### 来自 Thorp/Turtle 的精确收益率
- ❌ **Thorp 19.1% 年化且无亏损年** - 需 Princeton-Newport 原始基金报表或 Thorp 著作具体章节
- ❌ **Turtle 80%+ 年化** - Curtis Faith 书中提及但需核验原文；1983-1987 实盘记录非公开
- ✅ **保留**: 定性描述（"高回报""长期盈利"）和可追溯书籍引用

### 来自行业经验的统计数字
- ❌ **账户寿命 1-2 年** - 多个 broker/教育网站引用但无 primary source
- ❌ **50-70% false breakout 比例** - 统计方法、样本、时间范围不一致
- ❌ **震荡占 30-40% 时间** - 行业经验数字，无 primary research
- ❌ **每 10-20 周期 fat-tail** - 原 research 推断，非引用
- ❌ **Kurtosis 88.03** - ForexOp 模拟研究，计算方法不详，且为模拟非真实市场

### 来自原 research 推断的数字
- ❌ **核心假设失败概率 >70%** - 主观评估，非实证数据
- ❌ **p<0.01 显著性** - 实验设计参数，非已有结果
- ❌ **HMM 仓位标量 100%/60%/25%/10%** - 来自示例代码，非实证优化
- ❌ **固定 spread <0.5 pip, ADX>25, 20-day breakout** - 示例参数

---

## 已修正的阴性结论措辞

### 原措辞 → 修正后

**直接证据:**
- ❌ "止损后递增的支持证据**不存在**"
- ✅ "本次公开检索范围内**未找到**止损后递增的直接支持证据"

**核心假设:**
- ❌ "核心假设**不成立**""**不支持**"
- ✅ "核心假设（止损序列预测趋势）**未验证**；Query 9 的低等级来源不足以检验一般性的 P(trend | n stops)"

**主流共识:**
- ❌ "100% 一致""止损后增仓**不存在**"
- ✅ "在本次检索的来源中一致""止损后增仓**未见于检索到的文献**"

**False breakout:**
- ❌ "False breakout **不预测趋势**"
- ✅ "检索到的来源中，false breakout 被视为噪音而非趋势前兆信号；**本次研究未找到** false breakout 聚集预测趋势的直接证据"

**Query 9 实践来源:**
- ❌ "核心假设不支持"
- ✅ "Query 9 的实践来源（Tier 4-5）不足以检验一般性的条件概率假设 P(trend | n stops)；需要同信号 A-G 对照和序列检验"

---

## 已修正的数学表述

### 1. 几何增长与 Sharpe

**原表述（错误）:**
> "在 i.i.d. 假设下，若仓位与未来收益独立、完整周期内风险预算固定，几何增长率主要由 Sharpe ratio 决定，仓位路径不改变长期增长率"

**修正后:**
> 即使未来回报是 i.i.d.，状态依赖的仓位策略也会通过不同的 exposure 路径改变期望对数增长和风险特征。长期几何增长率应由 E[Σ log(1 + f_n X_n)] 描述，其中 f_n 依赖历史路径时，不能简化为"Sharpe 决定几何增长率"。

### 2. Risk of Ruin

**原表述（不准确）:**
> P(ruin) = (1 - p)^(K+1)

**修正后:**
> P(cycle_failure) = (1 - p)^(K+1) （单 cycle 连续 K+1 次失败概率）
>
> 真正的账户破产（risk of ruin）需定义破产阈值（如权益 < 20% × W_0），并用递归公式、Markov 链或 Monte Carlo 建模多 cycle 累积破产风险。

### 3. 偏度

**原表述（预设结论）:**
> "制造正偏度（小亏多次、大赢一次）"

**修正后:**
> 偏度取决于 payoff 结构、截断规则（K 上限）、终止条件和参数。在某些参数下可能产生正偏度（小亏多次、大赢一次），但不能预设；实际偏度需根据具体参数计算或模拟。

### 4. 完整 Cycle 期望

**修正:**
- 已添加完整公式和数值验证脚本（2026-06-23-progressive-probe-sizing-numerical-verification.py）
- 验证了索引、终端项和概率质量
- 提供可复算例子

---

## 已创建的可追溯证据账本

**新文件:** `data/exploration/raw/2026-06-23-evidence-sources.md`

**内容:**
- 5 个可追溯 primary/secondary sources
- 每条包含: URL/DOI/ISBN, 标题, 作者, 机构, 年份, 证据层级, 直接/相邻, 支持/反对, 局限, 市场, 频率, 样本, accessed_at
- 明确记录无法重建的引用
- 说明检索覆盖范围和局限
- 独立来源总数: 5 个（非原 evidence log 声称的 30+）

---

## 待完成修正（按任务清单）

### Task #2 & #3: 删除数字 + 修正措辞（批量应用到所有文件）

需修正的文件：
1. ✅ `2026-06-23-evidence-sources.md` - 已创建新可追溯账本
2. ✅ `2026-06-23-progressive-probe-sizing-mathematical-model.md` - 已修正数学表述
3. ✅ `2026-06-23-progressive-probe-sizing-numerical-verification.py` - 已创建验证脚本
4. ⏳ `2026-06-23-progressive-probe-sizing-final-report-zh.md` - 需修正
5. ⏳ `2026-06-23-pr14-revision-recommendations.md` - 需检查
6. ⏳ `2026-06-23-progressive-probe-sizing-failure-landscape.md` - 需检查
7. ⏳ `2026-06-23-progressive-probe-sizing-strategy-specification.md` - 需修正（A-G 规格）
8. ⏳ Run summary - 需同步真实结果
9. ⏳ PR body - 需更新

### Task #5: A-G 实验规格

需在 strategy-specification.md 中完整交付：
- A: 固定仓位（baseline）
- B: 算术递增 after loss
- C: 几何递增 after loss
- D: 增加 after win（anti-martingale）
- E: 放大 after independent confirmation
- F: Posterior/confidence sizing（HMM/Bayesian）
- G: Permutation/placebo（sizing-label permutation + 交易顺序置换）

所有组共享：同一 entry signal, exit, cost model, data, risk budget
唯一变化变量：sizing rule

### Task #6: 参数候选性

所有数值参数添加前缀/说明：
- "示意参数 (illustrative):"
- "候选网格 (candidate grid):"
- "需 broker/data calibration"
- 删除真实资金 pilot 建议
- 下一步仅推荐: "offline backtest/simulation/paper trading after evidence gates"

### Task #7: 流程合规

1. 新增 `state/claims/15.json` (status=released)
2. 清理 trailing whitespace: `git diff --check <base>...HEAD`
3. Run summary 删除不可重建计数（"30+ 来源""9 小时"）
4. 运行 `python scripts/validate_run.py --issue 15 --date 2026-06-23`
5. 更新 PR body
6. 留中文修正说明

---

## 修正后的核心结论模板

**适用于所有文档的标准措辞:**

### 证据检索结果

在本次公开检索范围内（Exa AI, 公开网页, 学术档案, 二手引用），针对 Query 1-9 的系统检索**未找到**止损后递增仓位的直接支持证据。

发现的一致模式：
- 止损/亏损/drawdown → 减仓（风险管理共识）
- 盈利/趋势确认 → 增仓（anti-martingale, pyramiding）
- 高波动/不确定 regime → 减仓

### 核心假设状态

本机制的核心假设（止损序列提供 regime 信息，条件概率 P(trend | n stops) 递增）**未经实证验证**。

Query 9 检索到的实践来源（Tier 4-5）将 false breakout 视为噪音而非趋势前兆，但这些低等级来源不足以检验一般性的条件概率假设。

**验证路径**: 需要 A-G 同信号对照实验、序列置换测试和条件概率直接检验。

### 风险评估

**若核心假设不成立**（止损序列不提供 regime 信息），本机制退化为有限 Martingale 变种，可能继承 Martingale 风险特征（方差增加、偏离 Kelly 最优）。

**若核心假设成立**，仓位递增可能有理论价值，但仍需实证检验。

**建议**: 在核心假设通过 A-G 对照和序列检验前，**不推荐真实资金实盘使用**。优先进行 offline backtest/simulation/paper trading。

---

*修正日志最后更新: 2026-06-23*
