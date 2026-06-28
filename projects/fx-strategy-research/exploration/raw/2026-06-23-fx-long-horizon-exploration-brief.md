# FX Long-Horizon Exploration Brief
# Phase B: Dynamic Position Management

**Date:** 2026-06-23
**Worker:** scout-worker-fx-01
**Run ID:** 2026-06-23-fx-phase-b-001
**Issue:** #13 Phase B

---

## Purpose

系统研究外汇长期动态仓位管理策略，批判性验证"亏损以算术级速度累积、盈利通过加仓/复利呈指数级扩展"的思想。不默认该思想成立，必须提供数学分析、实证证据、反例和成立条件。

---

## Research Scope

### A. 策略收益来源

- **Time-series momentum / trend following:** 持续追踪趋势，顺势加仓
- **Cross-sectional currency momentum:** 跨货币对比，做多赢家、做空输家
- **Carry trade:** 利差套利，rollover/swap 收益
- **Value & PPP (Purchasing Power Parity):** 长期均值回归，低估货币配置
- **Macro regime & central bank policy divergence:** 央行政策差异驱动汇率
- **Managed futures / CTA FX portfolios:** CTA 基金中的外汇子组合
- **Spot vs forwards vs futures:** 交易工具差异，roll/carry/funding/basis 影响

### B. 动态仓位管理

- **Pyramiding / scaling into winners / anti-martingale:** 盈利时加仓
- **Fixed fractional / fixed ratio:** 按资金固定比例配置
- **Volatility targeting:** 按波动率调整仓位
- **Risk parity / ERC (Equal Risk Contribution):** 组合风险平衡
- **Kelly / fractional Kelly / risk-constrained Kelly / optimal f:** 最优仓位理论与估计误差
- **Trailing stop / ATR stop / vol stop / time stop:** 止损机制
- **Drawdown targeting / de-risk / re-risk:** 回撤控制，动态风险调整
- **Portfolio heat / correlation clustering:** 组合过热，货币暴露净额
- **USD factor / implicit leverage:** 美元因子，隐含杠杆风险
- **CPPI / convex allocation:** 保本组合保险等相邻方法

### C. 数学与逻辑审计

- **Multiplicative wealth process:** 财富过程本质是乘法的，非加法
- **Arithmetic return vs geometric growth:** 算术收益与几何增长的差异
- **Log utility / volatility drag:** 对数效用，波动拖累
- **"Arithmetic loss, geometric gain" feasibility:** 该主张的数学可行性、成立条件和误导风险
- **Path dependence:** 路径依赖，连续亏损、趋势反转、gap 的影响
- **Stop-loss slippage / pyramiding drawback:** 止损滑点，加仓后回吐
- **Risk of ruin / maximum drawdown:** 破产风险，最大回撤
- **Expected log growth / skew / convexity:** 期望对数增长，偏度，凸性
- **Positive convexity vs positive skew vs guaranteed profit:** 区分凸性、偏度与保证盈利
- **Anti-martingale vs martingale / averaging down / grid:** 明确区分盈利加仓与亏损加仓
- **"Cut losses short, let profits run" empirical evidence:** 该格言的实证证据与交易成本/whipsaw 代价

### D. 风险和失效

- **Carry crash:** 利差套利崩溃（2008 年 10 月等事件）
- **Currency crisis:** 货币危机，贬值 20-50%+
- **Central bank intervention:** 央行干预，突然政策变化
- **Peg break / de-pegging:** 固定汇率崩溃
- **Liquidity gap / flash crash:** 流动性枯竭，闪崩
- **Regime shift:** 市场 regime 转变，策略失效
- **Crowding / correlation convergence:** 拥挤交易，相关性趋同
- **Leverage targeting feedback / procyclicality:** 波动率目标在波动突增时被迫去杠杆
- **Kelly estimation error:** Kelly 对 edge/variance/correlation 估计误差敏感
- **Long-period sample insufficiency:** 长周期样本不足
- **Backtest selection / survivorship bias / publication bias:** 回测选择、幸存偏差、发表偏差
- **Overnight/weekend gap / swap / rollover cost / broker risk:** 隔夜/周末跳空，融资成本，broker 风险

### E. 验证设计

- **Multi-regime & crisis coverage:** 至少覆盖多个主要汇率 regime 和危机时期
- **Walk-forward / purged / embargo:** 前向分析，避免数据泄漏
- **Parameter stability / subperiod validation:** 参数稳定性，子时期验证
- **Cross-pair validation:** 跨货币对验证
- **Spot vs futures/forwards data consistency:** 现货与期货/远期数据一致性
- **Bid/ask / roll / swap / slippage / leverage simulation:** 完整交易成本建模
- **Portfolio-level attribution:** 组合级归因：signal, sizing, carry, FX beta, vol target 各自贡献
- **Baseline comparison:** 与固定仓位、固定风险、无加仓基线比较
- **Falsifiability conditions:** 明确能够证伪策略的条件

---

## Research Methodology

### Sources Priority

1. **Tier 1:** 同行评审论文（Journal of Finance, JFE, RFS, JME, etc.）、央行/BIS/NBER working papers、学术期刊
2. **Tier 2:** 有方法和数据说明的行业研究、broker 执行文档、managed futures 研究
3. **Tier 3:** 成熟开源实现及可复现实验（GitHub with documented backtests）
4. **Tier 4:** 教程、博客、论坛讨论（仅作线索，不作单一证据）

### Research Tools

- **Agent-Reach / Exa:** 广泛搜索和来源发现
- **Firecrawl:** 公开网页 search、单页或批量内容提取（串行执行，避免 429）
- **GitHub:** 查找成熟回测框架、策略实现和失败案例
- **论文数据库:** SSRN, RePEc, arXiv, Google Scholar

### Recording Requirements

每个来源必须记录：
- URL, title, authors, publication venue
- Source type (paper, research, blog, github, tutorial, broker_research, central_bank, other)
- Credibility tier (tier1-tier4)
- Decision (keep/reject) and reason
- Evidence extracted (strategy description, data, conclusions, methods)
- Counter-evidence or warnings
- Strategy family
- Query set ID
- Date accessed

### Saturation Criteria

"尽可能穷尽"的停止条件：
- 连续至少三轮不同查询扩展不再产生新的主要策略类别、关键风险类别或重要验证方法
- 必须明确声明公开资料与时间范围带来的不完备性
- 记录证据饱和判断

---

## Deliverables

Phase B 至少交付：

1. **2026-06-23-fx-long-horizon-exploration-brief.md** (this file)
2. **2026-06-23-fx-long-horizon-query-matrix.md:** 查询词矩阵
3. **2026-06-23-fx-long-horizon-source-decisions.md:** 来源决策台账
4. **2026-06-23-fx-long-horizon-strategy-taxonomy.md:** 策略分类
5. **2026-06-23-fx-long-horizon-position-sizing-math.md:** 仓位管理数学分析
6. **2026-06-23-fx-long-horizon-failure-landscape.md:** 失败景观
7. **2026-06-23-fx-long-horizon-evidence-map.md:** 证据地图
8. **../daily_reports/2026-06-23-fx-long-horizon-phase-b.md:** Phase B 中文研究报告

Phase A+B 综合交付：

9. **../reuse_maps/2026-06-23-fx-quant-strategies.md:** 复用地图
10. **../daily_reports/2026-06-23-fx-quant-strategy-research.md:** 综合中文研究报告
11. **data/proposals/project_candidates/2026-06-23-fx-quant-followups.md:** 后续实验候选
12. **../../memory/2026-06-23-fx-quant-research.md:** 记忆提案

---

## Constraints and Prohibitions

### Allowed

- 公开只读网络
- Agent-Reach (不使用 Grok，当前持续 429)
- Firecrawl 已批准范围（串行执行）
- GitHub agent branch / Draft PR
- 写入 data/** 和 state/**

### Prohibited

- 私人账号
- 交易账户连接
- 付费数据新增订阅（现有批准除外）
- 真实/模拟下单
- 经纪商 API
- 未经批准的凭证
- Grok 接入点（当前暂不使用）
- 并发 Claude 会话
- 并行研究角色
- 并发 Firecrawl 批次
- 高频自动重试 429

---

## Risk Disclosure

金融研究具有高误导风险：
- 历史回测不代表未来收益
- 杠杆、交易成本、尾部事件和市场结构变化可能使策略失效
- 研究结果必须作为后续实验输入，而不是直接交易指令
- 不提供个性化投资建议
- 不承诺收益或胜率

---

**Phase B 开始执行。**
