# Progressive Probe Position Sizing - Query Matrix

**Date:** 2026-06-23
**Worker:** scout-worker-fx-sizing-01
**Run ID:** 2026-06-23-fx-sizing-001

---

## 查询矩阵说明

本矩阵覆盖**直接证据**和**相邻理论证据**的查询空间。每个查询记录：
- 关键词组合
- 预期证据类型
- 饱和指标（何时停止该方向搜索）

**不追求穷尽**，而是：
1. 系统覆盖核心维度
2. 明确边界和饱和条件
3. 记录未找到的查询（阴性结果同样重要）

---

## 维度 1：直接证据 - 有限递增试探仓位

### 1.1 核心机制

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q1.1a | "progressive position sizing" + "after losses" | 直接讨论 | 找到 3 个独立来源或前 50 结果无相关 |
| Q1.1b | "adaptive position sizing" + "drawdown" | 相关方法 | 同上 |
| Q1.1c | "increasing position size" + "consecutive losses" | 直接描述 | 同上 |
| Q1.1d | "limited martingale" + "trend following" | 有限变种 | 同上 |
| Q1.1e | "probe position" + "trend confirmation" | 两阶段策略 | 同上 |

**搜索通道：**
- Google Scholar
- SSRN
- arXiv (q-fin)
- Web search (学术站点)

### 1.2 止损序列信息价值

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q1.2a | "stop loss sequence" + "predictive power" | 序列预测性 | 3 个来源或 50 结果无 |
| Q1.2b | "consecutive stop losses" + "regime change" | Regime 关系 | 同上 |
| Q1.2c | "false breakout clustering" + forex | 假突破聚集 | 同上 |
| Q1.2d | "whipsaw" + "precede trend" | Whipsaw 与趋势关系 | 同上 |
| Q1.2e | "drawdown" + "precursor" + trend | 回撤作为前兆 | 同上 |

---

## 维度 2：相邻理论 - Sequential Testing

### 2.1 Sequential Hypothesis Testing

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q2.1a | "sequential probability ratio test" + trading | SPRT 应用 | 找到 2 个应用案例或理论基础 |
| Q2.1b | "sequential testing" + "financial markets" | 金融应用 | 同上 |
| Q2.1c | "adaptive sampling" + trading | 自适应采样 | 同上 |
| Q2.1d | "optimal stopping" + "trading strategy" | 最优停止 | 同上 |

### 2.2 Change-Point Detection

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q2.2a | "change point detection" + forex | FX 应用 | 3 个研究或前 50 无 |
| Q2.2b | "regime change detection" + "position sizing" | 与 sizing 结合 | 同上 |
| Q2.2c | "bayesian change point" + trading | 贝叶斯方法 | 同上 |
| Q2.2d | "online change point detection" + markets | 在线检测 | 同上 |

---

## 维度 3：相邻理论 - Regime Switching

### 3.1 HMM & Regime Models

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q3.1a | "hidden markov model" + forex + "position sizing" | HMM sizing | 2 个研究或理论框架 |
| Q3.1b | "markov switching" + "adaptive trading" | Markov 自适应 | 同上 |
| Q3.1c | "regime dependent position sizing" | Regime sizing | 同上 |
| Q3.1d | "state dependent risk management" | 状态依赖 | 同上 |

### 3.2 Regime Identification

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q3.2a | "trend vs range detection" + forex | 趋势/震荡识别 | 3 个方法或前 50 无 |
| Q3.2b | "market regime classification" | Regime 分类 | 同上 |
| Q3.2c | "volatility regime switching" + FX | 波动率 regime | 同上 |

---

## 维度 4：Martingale 理论与实证

### 4.1 理论基础

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q4.1a | "finite martingale" + "bounded capital" | 有限 Martingale | 数学理论 1-2 篇 |
| Q4.1b | "martingale betting" + "stop loss limit" | 带止损的 Martingale | 同上 |
| Q4.1c | "gambler's ruin" + "finite doubling" | 有限加倍破产 | 同上 |
| Q4.1d | "limited martingale" + "risk budget" | 预算约束 | 同上 |

### 4.2 实证研究

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q4.2a | "martingale strategy" + forex + empirical | FX 实证 | 3 个研究 |
| Q4.2b | "anti-martingale" + "trend following" + performance | Anti-M 表现 | 同上 |
| Q4.2c | "martingale vs anti-martingale" + comparison | 对比研究 | 同上 |
| Q4.2d | "doubling down" + forex + "risk of ruin" | 加倍风险 | 同上 |

---

## 维度 5：Trend Following Position Management

### 5.1 Professional Systems

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q5.1a | "turtle trading" + "unit sizing" | Turtle 系统 | 原始规则文档 |
| Q5.1b | "ATR position sizing" + forex | ATR sizing | 2-3 个应用 |
| Q5.1c | "volatility scaled position sizing" | Vol scaling | 同上 |
| Q5.1d | "CTA position management" | CTA 实践 | 2-3 个来源 |

### 5.2 Pyramiding & Scaling In

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q5.2a | "pyramiding" + "trend following" + risk | 加仓风险 | 3 个讨论 |
| Q5.2b | "scaling in" + "multiple entries" | 多次入场 | 同上 |
| Q5.2c | "adding to winners" + "position management" | 盈利加仓 | 同上 |
| Q5.2d | "layered entry" + forex | 分层入场 | 同上 |

### 5.3 Campaign Trading

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q5.3a | "campaign trading" | Campaign 概念 | 定义和案例 1-2 个 |
| Q5.3b | "series of trades" + "same direction" | 系列交易 | 同上 |
| Q5.3c | "building position" + "trend following" | 建仓过程 | 同上 |

---

## 维度 6：条件概率与自相关

### 6.1 Loss Streaks

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q6.1a | "losing streak" + "subsequent win probability" | 连亏后胜率 | 2-3 个研究 |
| Q6.1b | "consecutive losses" + "mean reversion" | 均值回归 | 同上 |
| Q6.1c | "negative autocorrelation" + "trading outcomes" | 负自相关 | 同上 |
| Q6.1d | "gambler's fallacy" + trading | 赌徒谬误 | 同上（警示） |

### 6.2 Hazard Rate

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q6.2a | "hazard rate" + "trend emergence" | 趋势 hazard | 1-2 个框架 |
| Q6.2b | "time to trend" + forex | 趋势到达时间 | 同上 |
| Q6.2c | "waiting time" + "regime change" | 等待时间 | 同上 |

---

## 维度 7：Kelly Criterion Variants

### 7.1 Dynamic Kelly

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q7.1a | "dynamic kelly" + "time varying" | 动态 Kelly | 2-3 个研究 |
| Q7.1b | "adaptive kelly criterion" | 自适应 Kelly | 同上 |
| Q7.1c | "kelly criterion" + "regime dependent" | Regime Kelly | 同上 |
| Q7.1d | "fractional kelly" + "estimation error" | Fractional 与误差 | 同上 |

### 7.2 Path-Dependent Sizing

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q7.2a | "path dependent position sizing" | 路径依赖 | 2 个研究 |
| Q7.2b | "history dependent" + "bet sizing" | 历史依赖 | 同上 |
| Q7.2c | "state dependent kelly" | 状态 Kelly | 同上 |

---

## 维度 8：Risk Management Theory

### 8.1 Drawdown Control

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q8.1a | "drawdown control" + "position sizing" | DD 控制 | 2-3 个方法 |
| Q8.1b | "risk budget" + "dynamic allocation" | 动态风险预算 | 同上 |
| Q8.1c | "portfolio heat" + management | 组合热度 | 同上 |

### 8.2 Risk of Ruin

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q8.2a | "risk of ruin" + "position sizing" | Ruin 与 sizing | 理论 2 篇 |
| Q8.2b | "ruin probability" + "trading strategy" | Ruin 概率 | 同上 |
| Q8.2c | "survival probability" + martingale | 生存概率 | 同上 |

---

## 维度 9：实证案例与专业文献

### 9.1 Professional Traders

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q9.1a | "Van Tharp" + "position sizing" | Van Tharp 方法 | 1-2 个来源 |
| Q9.1b | "Larry Williams" + "money management" | Williams 方法 | 同上 |
| Q9.1c | "Ed Seykota" + "position management" | Seykota 实践 | 同上 |
| Q9.1d | "Richard Dennis" + turtles + sizing | Dennis/Turtle | 同上 |

### 9.2 Industry White Papers

| 查询组 | 关键词 | 预期 | 饱和条件 |
|--------|--------|------|----------|
| Q9.2a | "AQR" + "position sizing" OR "risk management" | AQR 文献 | 1-2 篇 |
| Q9.2b | "Man Group" + "trend following" + sizing | Man Group | 同上 |
| Q9.2c | "Winton" + "risk management" | Winton | 同上 |

---

## 查询执行策略

### 阶段 1：直接证据搜索（维度 1）
- 优先级最高
- 用尽所有查询组合
- 记录阴性结果

### 阶段 2：相邻理论（维度 2-3）
- Sequential testing & change-point
- Regime switching
- 建立理论基础

### 阶段 3：Martingale 与 TF（维度 4-5）
- Martingale 对比
- Trend following 实践
- 识别连续谱位置

### 阶段 4：条件概率（维度 6）
- 关键：止损是否提供信息
- 自相关、hazard rate

### 阶段 5：Sizing 理论（维度 7-8）
- Kelly variants
- Risk management

### 阶段 6：实践文献（维度 9）
- Professional traders
- Industry papers

### 饱和判断

每个维度达到以下之一即认为饱和：
1. 找到预期数量的相关来源
2. 前 50 个结果无新相关内容
3. 重复出现相同来源/引用
4. 查询变体不产生新结果

### 阴性结果记录

若某查询组无相关结果，记录：
- 查询关键词
- 搜索引擎/数据库
- 前 N 个结果的主题分布
- 结论：该方向证据缺失

**阴性结果与阳性结果同样重要**，说明研究空白。

---

## 搜索工具与通道

### 学术搜索
- Google Scholar
- SSRN (Social Science Research Network)
- arXiv (q-fin, stat.ML)
- JSTOR（如可访问）
- RePEc

### 专业数据库
- BIS (Bank for International Settlements)
- Fed papers
- ECB working papers

### Web Search
- Google（限定学术站点）
- Semantic Scholar

### 行业资源
- CFA Institute
- AQR, Man Group, Winton 网站
- Quantocracy（聚合器）

### 社区（低优先级）
- Quantitative Finance Stack Exchange
- Elite Trader (archive)
- 仅作线索，不作证据

---

## 执行约束

- **严格串行**：一次一个查询维度
- **批量检索**：可用 Agent-Reach/Exa 批量抓取候选
- **Firecrawl**：批量页面内容提取
- **Grok**：仅在 X.com 有核心证据必要时使用
- **退避**：遇到 429 等待，不密集重试
- **记录**：所有查询和结果，包括阴性

---

**Query Matrix 完成。下一步：分阶段执行证据检索。**
