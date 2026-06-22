# FX Intraday Source Decision Ledger
# Phase A: Day Trading, No Overnight

**Date:** 2026-06-23  
**Worker:** scout-worker-fx-01  
**Run ID:** 2026-06-23-fx-phase-a-001

---

## Purpose

记录每个来源的 URL、日期、类型、可信度评级、keep/reject 决策、理由、提取的证据或反证。

---

## Decision Fields

- **ID:** 递增编号
- **URL:** 完整 URL
- **Title:** 页面或论文标题
- **Source Type:** paper | research | blog | github | tutorial | broker_research | central_bank | other
- **Credibility:** tier1 | tier2 | tier3 | tier4
- **Decision:** keep | reject
- **Reason:** 为何保留或拒绝
- **Evidence Extracted:** 如果 keep，提取的关键证据（策略描述、数据、结论、方法）
- **Counter-Evidence:** 如果存在相反证据或警告
- **Strategy Family:** trend_momentum | breakout | mean_reversion | stat_arb | order_flow | volatility | event_driven | cross_cutting
- **Query Set:** 对应 query matrix 中的编号
- **Date Accessed:** YYYY-MM-DD

---

## Credibility Tiers

- **tier1:** 同行评审论文、央行/BIS 研究、学术期刊
- **tier2:** 有方法和数据说明的行业研究、broker 执行文档
- **tier3:** 成熟开源实现及可复现实验（GitHub with documented backtests）
- **tier4:** 教程、博客、论坛讨论（仅作线索，不作单一证据）

---

## Entries

### ID: 001
- **URL:** https://ideas.repec.org/a/eee/finmar/v37y2018icp35-51.html
- **Title:** Intraday momentum in FX markets: Disentangling informed trading from liquidity provision
- **Authors:** Elaut, Gert & Frömmel, Michael & Lampaert, Kevin
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 同行评审论文，发表于 Journal of Financial Markets (2018)，使用交易级数据，方法明确
- **Evidence Extracted:**
  - 研究 RUB-USD 市场（Moscow Interbank Currency Exchange，2005-2014）
  - 定义日内动量：首个半小时收益与最后半小时收益显著正相关
  - 发现：日内动量由流动性提供者的隔夜持仓风险厌恶驱动，而非知情交易
  - 交易时段集中度对日内动量有影响
  - 金融危机期间效应更明显
- **Counter-Evidence:** 研究仅限于单一货币对（RUB-USD），新兴市场，可能不适用于主要货币对
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 002
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2694985
- **Title:** Intraday Momentum in FX Markets: Disentangling Informed Trading from Liquidity Provision
- **Authors:** Elaut, Gert & Frömmel, Michael & Lampaert, Kevin
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** SSRN 工作论文版本，与 ID 001 相同研究
- **Evidence Extracted:** 同 ID 001
- **Counter-Evidence:** 同 ID 001
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 003
- **URL:** https://onlinelibrary.wiley.com/doi/10.1111/jmcb.12032
- **Title:** Intraday Patterns in FX Returns and Order Flow
- **Authors:** Breedon, F. & Ranaldo, A.
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 发表于 Journal of Money, Credit and Banking (2013)，高质量学术期刊
- **Evidence Extracted:**
  - 使用高频 FX 数据集
  - 发现显著的时段效应（time-of-day effects）：货币在本地交易时段倾向于贬值
  - 模式在多个货币和时区中得到确认
  - 模式反映在订单流中：市场参与者在自己的交易时段倾向于净购买外汇
  - 单一做市商数据证实了这一解释
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 004
- **URL:** https://www.bayes.city.ac.uk/__data/assets/pdf_file/0006/111120/fxmom_final_cepr.pdf
- **Title:** Currency Momentum Strategies
- **Authors:** Menkhoff, Lukas & Sarno, Lucio & Schmeling, Maik & Schrimpf, Andreas
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 广泛的货币动量策略实证研究，跨期（1976-2010）和跨币种（最多 48 种货币）
- **Evidence Extracted:**
  - 货币动量策略年化超额收益高达 10%
  - 做多过去赢家货币，做空过去输家货币
  - 传统风险因子无法解释收益差
  - 部分由交易成本解释
  - 行为与投资者反应不足和过度反应一致
  - 货币动量与 carry trade 性质非常不同，与技术交易规则相关性不高
  - 存在有效的套利限制（limits to arbitrage）
- **Counter-Evidence:** 交易成本敏感，套利限制阻碍可利用性
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 005
- **URL:** https://openaccess.city.ac.uk/id/eprint/3296/1/Currency%20Momentum%20Strategies.pdf
- **Title:** Currency Momentum Strategies
- **Authors:** 同 ID 004
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 同 ID 004，开放获取版本
- **Evidence Extracted:** 同 ID 004
- **Counter-Evidence:** 同 ID 004
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 006
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3138756
- **Title:** Intraday Patterns in Foreign Exchange Returns and Realized Volatility
- **Authors:** Zhang, Hao
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** SSRN 论文，使用高频数据（2010-2015），样本涵盖 16 种货币
- **Evidence Extracted:**
  - 本币在本国交易时段倾向于贬值
  - 本币在美国交易时段（伦敦市场关闭后）倾向于升值
  - 日内模式存在于许多国家，包括有资本管制的国家
  - 日内模式与已实现波动率显著相关，反映订单流风险和市场对订单流的敏感性
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 007
- **URL:** https://ideas.repec.org/a/eee/intfin/v58y2019icp65-77.html
- **Title:** Intraday effects of the currency market
- **Authors:** Khademalomoom, Siroos & Narayan, Paresh Kumar
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 发表于 Journal of International Financial Markets, Institutions and Money (2019)
- **Evidence Extracted:**
  - 使用每小时汇率（6 种最具流动性货币，2004-2014）
  - 发现强烈的时段效应（time-of-the-day effects）
  - 三种新的日内效应：
    1. 本地市场开盘后效应（local markets post-opening effect）
    2. 主要市场活动效应（major markets activities effect）
    3. 市场重叠时段效应（markets overlapping times effect）
  - 这些日内效应对投资者有实际影响
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum
- **Query Set:** 1.2
- **Date Accessed:** 2026-06-23

### ID: 008
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1971680
- **Title:** Currency Momentum Strategies (BIS Working Paper)
- **Authors:** Menkhoff, Lukas & Sarno, Lucio & Schmeling, Maik & Schrimpf, Andreas
- **Source Type:** research
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** BIS Working Paper No. 366，央行/国际清算银行研究
- **Evidence Extracted:** 同 ID 004（相同研究的 BIS 版本）
- **Counter-Evidence:** 同 ID 004
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 009
- **URL:** https://sites.insead.edu/facultyresearch/research/file.cfm?fid=66802
- **Title:** Intraday currency returns and benchmark fixings
- **Authors:** 未明确列出
- **Source Type:** research
- **Credibility:** tier2
- **Decision:** keep
- **Reason:** INSEAD 研究，关于基准定价时段的价格反转
- **Evidence Extracted:**
  - 新发现：日内货币收益在主要基准定价（benchmark fixings）前后显示持续反转
  - 美元在定价前升值，定价后贬值
  - 这是系统性特征：每周、每月、样本 20 年内都存在
  - 证据支持库存风险模型：日内美元订单不平衡与跨时区价格反转相关
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum, mean_reversion
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 010
- **URL:** https://sah.borca.ai/papers/67764116
- **Title:** Do Momentum-Based Strategies Still Work in Foreign Currency Markets?
- **Authors:** 未明确列出
- **Source Type:** paper
- **Credibility:** tier2
- **Decision:** keep
- **Reason:** 学术论文（2003），跨越 1970s-1990s 的长期验证
- **Evidence Extracted:**
  - 动量交易策略在 1970s 和 1980s 的盈利能力在整个 1990s 持续存在
  - 对交易规则规格和基准货币不敏感
  - 表现不是由时变风险溢价引起，而是依赖于货币收益的自相关结构
  - 支持股票市场动量研究：动量策略盈利性也适用于货币
- **Counter-Evidence:** 无明确反证，但论文较早（2003），需要更新数据验证
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23


### ID: 011-017 (London Session Materials)
- **URLs:** Multiple broker/education sites (ThinkMarkets, ForexCracked, KW Markets Lab, Titan FX, LiquidityScan, Fazen Capital, Investopedia, KenMacro)
- **Title:** Various "London Breakout Strategy" and "London Kill Zone" guides
- **Source Type:** tutorial, broker_research
- **Credibility:** tier4
- **Decision:** keep (as leads only, not primary evidence)
- **Reason:** 一致描述伦敦开盘突破模式，但属于教育/营销材料，无学术方法验证
- **Evidence Extracted:**
  - 伦敦时段占全球外汇交易量 43%（引用 BIS）
  - "London Kill Zone" 时间窗口：07:00-10:00 UTC（或 08:00-11:00 夏令时）
  - 常见模式：亚洲时段形成窄幅区间，伦敦开盘时突破
  - 最佳突破窗口：伦敦开盘后 1-2 小时
  - 风险过滤：亚洲区间应在 20-60 pips（过窄或过宽降低成功率）
  - 需与更高时间框架趋势对齐
  - "Judas Swing" 概念：伦敦开盘时先假突破（扫止损），然后反向
  - 最佳货币对：EUR/USD, GBP/USD, EUR/GBP
  - 伦敦-纽约重叠时段（12:00-16:00 UTC）流动性最高
- **Counter-Evidence:** 所有材料均为实践指南，缺少回测数据、样本外验证、失败率统计
- **Strategy Family:** breakout, trend_momentum
- **Query Set:** 1.2
- **Date Accessed:** 2026-06-23

### ID: 018-019 (GitHub Implementations)
- **URLs:** 
  - https://github.com/vighneshiyer/forex-backtester-python (archived)
  - https://github.com/GeniusMathematicsConsultants/ForexBacktestingPython
- **Source Type:** github
- **Credibility:** tier3
- **Decision:** keep (as reference implementations)
- **Reason:** 开源回测框架，可用于验证策略，但文档有限
- **Evidence Extracted:**
  - forex-backtester-python: 基于历史数据的基本策略回测（已归档，最后更新 2025-10）
  - ForexBacktestingPython: 移动平均策略优化示例（更新至 2024-06）
- **Counter-Evidence:** 项目较简单，缺少复杂策略和交易成本建模
- **Strategy Family:** cross_cutting
- **Query Set:** 1.4
- **Date Accessed:** 2026-06-23

### ID: 020
- **URL:** https://vikofintech.com/en/posts/algo-trading-overfitting-vermeiden-regime-wechsel/
- **Title:** How to Stop Your Intraday Trading Strategy From Fooling You: Overfitting, Regime Shifts, Concentration Risk
- **Source Type:** blog
- **Credibility:** tier2
- **Decision:** keep
- **Reason:** 系统讨论过拟合检测方法，引用社区讨论和 regime-aware 验证
- **Evidence Extracted:**
  - 过拟合定义：模型学习了训练数据中的噪声而非信号
  - Walk-forward 验证的盲点：如果训练期和测试期处于同一市场 regime，样本外测试实际是"样本内"
  - 需要跨 regime 测试（趋势 vs 均值回归，高波动 vs 低波动，相关 vs 不相关）
  - 集中度风险：如果 1000 笔交易中大部分 P&L 来自 10 笔，统计基础薄弱
  - 修复方法：减少参数数量，压力测试（移除最佳交易后 Sharpe 是否崩溃），regime-diverse 测试
- **Counter-Evidence:** 无
- **Strategy Family:** cross_cutting
- **Query Set:** 1.3, 9.2
- **Date Accessed:** 2026-06-23

### ID: 021-027 (Overfitting & Backtest Failure Literature)
- **URLs:** Multiple sources on overfitting detection (ForexWink, ForexRobotEasy, FXTool, ForexRobotLab, METAtronics, CuteMarkets, TrustedQuant)
- **Source Type:** blog, tutorial
- **Credibility:** tier2-tier4
- **Decision:** keep (as practitioner consensus)
- **Reason:** 多个独立来源一致描述过拟合检测方法和最佳实践
- **Evidence Extracted:** (合并关键点)
  - 参数敏感性测试：±10% 参数变化时表现是否崩溃？健壮策略有"参数平台"而非单一峰值
  - 样本外测试：70/30 分割，OOS 下降 30-50% 可接受，完全逆转为亏损则过拟合
  - 胜率 > 85% + 高 P&L 通常是过拟合信号
  - Walk-Forward Efficiency > 50% 表明真实边缘
  - 最小样本：100-200 笔交易，日线 10 年，日内 5 年，跨越完整市场周期
  - 参数预算：不超过 1 参数 / 200-300 笔交易
  - DSR (Deflated Sharpe Ratio) > 0.95 才能排除纯选择效应
  - PBO (Probability of Backtest Overfitting) < 0.05 可接受
  - 关键洞察："过拟合通常看起来像进步"
- **Counter-Evidence:** 部分材料针对零售 EA 市场，可能过度简化
- **Strategy Family:** cross_cutting
- **Query Set:** 1.3, 9.2, 9.3
- **Date Accessed:** 2026-06-23

---

## Checkpoint 1 Summary (2026-06-23, ~15:30 UTC)

已完成：
- Strategy Family 1 (Trend/Momentum Intraday): 学术文献 10 篇 (tier1)，实践指南 8 组 (tier4)
- Cross-cutting: Overfitting 和验证方法文献 8 组 (tier2-tier4)
- GitHub 实现: 2 个回测框架 (tier3)

关键发现：
1. **日内动量存在**：多篇 tier1 论文（Elaut 2018, Breedon 2013, Zhang 2018, Khademalomoom 2019）证实时段效应和日内动量
2. **货币动量策略**：Menkhoff et al. (BIS) 显示跨货币动量年化 10% 超额收益，但交易成本敏感
3. **时段模式**：本币在本国交易时段贬值，美国时段升值（多个独立来源）
4. **伦敦开盘突破**：实践者广泛描述，但缺少学术验证
5. **过拟合风险**：多个来源一致强调参数敏感性、walk-forward、regime-diverse 测试的重要性

下一步：继续 Strategy Family 2 (Breakout)，然后 3-7，最后跨领域主题（交易成本、数据、风险）。

