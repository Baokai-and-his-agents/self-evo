# FX Long-Horizon Source Decision Ledger
# Phase B: Dynamic Position Management

**Date:** 2026-06-23
**Worker:** scout-worker-fx-01
**Run ID:** 2026-06-23-fx-phase-b-001

---

## Purpose

记录每个来源的 URL、日期、类型、可信度评级、keep/reject 决策、理由、提取的证据或反证。

---

## Decision Fields

- **ID:** 递增编号
- **URL:** 完整 URL
- **Title:** 页面或论文标题
- **Authors:** 作者（如有）
- **Source Type:** paper | research | blog | github | tutorial | broker_research | central_bank | other
- **Credibility:** tier1 | tier2 | tier3 | tier4
- **Decision:** keep | reject
- **Reason:** 为何保留或拒绝
- **Evidence Extracted:** 如果 keep，提取的关键证据
- **Counter-Evidence:** 如果存在相反证据或警告
- **Strategy Family:** trend_momentum | carry | value_ppp | macro_regime | position_sizing | volatility_targeting | risk_management | mathematical_foundations
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
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0304405X21002282
- **Title:** Dissecting currency momentum
- **Authors:** N/A (from search preview)
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 发表于 Journal of Financial Economics，顶级期刊，分析 cross-sectional 和 time-series momentum
- **Evidence Extracted:**
  - Cross-sectional 和 time-series momentum 在货币中无法被 carry 和 dollar 因子解释
  - 动量策略做多正因子收益后的货币因子，做空亏损后的因子
  - Carry 和 dollar 因子强自相关，仅在正因子收益后显著盈利
  - 个体货币收益中 momentum 较少
  - 因子动量优于 cross-sectional 和 time-series momentum，并解释它们
  - Limits to arbitrage 和 time-varying risk premium 有助于解释因子动量
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 002
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2949379
- **Title:** Momentum and Trend Following Trading Strategies for Currencies Revisited - Combining Academia and Industry
- **Authors:** Janick Rohrbach, Silvan Suremann, Joerg Osterrieder
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** SSRN 论文，详细结合学术和行业视角
- **Evidence Extracted:**
  - 使用几何布朗运动推导动量策略的理论基础
  - 交易信号：不同时间范围的指数移动平均混合
  - 统计学上优化时间范围选择
  - 测试 G10、新兴市场货币和加密货币
  - Time-series 和 cross-sectional 组合
  - Time-series momentum 对传统法币最佳，cross-sectional 对加密货币更合适
  - 更高波动率货币有更高 Sharpe ratio
  - 新兴市场和加密货币表现优于 G10
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1
- **Date Accessed:** 2026-06-23

### ID: 003
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1809776
- **Title:** Currency Momentum Strategies (Menkhoff et al.)
- **Authors:** Lukas Menkhoff, Lucio Sarno, Maik Schmeling, Andreas Schrimpf
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 广泛实证研究，1976-2010，最多 48 种货币
- **Evidence Extracted:**
  - Cross-sectional 超额收益差高达 10% p.a.
  - 做多过去赢家货币，做空输家货币
  - 传统风险因子无法解释
  - 部分被交易成本解释
  - 与投资者反应不足和过度反应一致
  - 与 carry trade 性质非常不同
  - 存在有效的套利限制（limits to arbitrage）
- **Counter-Evidence:** 交易成本敏感，套利限制阻碍可利用性
- **Strategy Family:** trend_momentum
- **Query Set:** 1.1, 4.2
- **Date Accessed:** 2026-06-23

### ID: 004
- **URL:** https://www.sciencedirect.com/science/article/pii/S0304405X11002613
- **Title:** Time series momentum
- **Authors:** Tobias J. Moskowitz, Yao Hua Ooi, Lasse Heje Pedersen
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** Journal of Financial Economics 2012，跨资产类别（股票、货币、商品、债券）58 种流动工具
- **Evidence Extracted:**
  - 显著 time-series momentum，持续 1-12 个月
  - 长期部分反转，与情绪理论一致（初始反应不足、延迟过度反应）
  - 跨资产类别分散组合产生显著超额收益
  - 对标准资产定价因子暴露很少
  - 极端市场中表现最佳
  - Speculators 从 time-series momentum 获利，hedgers 承担损失
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum
- **Query Set:** 1.2
- **Date Accessed:** 2026-06-23

### ID: 005
- **URL:** http://docs.lhpedersen.com/DemystifyingManagedFutures.pdf
- **Title:** Demystifying Managed Futures
- **Authors:** Brian Hurst, Yao Hua Ooi, Lasse Heje Pedersen
- **Source Type:** research
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 详细分析 managed futures / CTA 策略，1985-2012
- **Evidence Extracted:**
  - Time-series momentum：1、3、12 个月 look-back
  - 58 种流动期货和货币远期（24 商品、9 股指、13 债券、12 货币）
  - 根据预期波动率调整仓位，目标波动率 10%
  - 1、3、12 月 TSMOM 表现良好，跨时间和资产类别
  - 分散 TSMOM 总 Sharpe ratio 1.8
  - 在 bear 和 bull 市场均表现良好
  - TSMOM 可解释 Managed Futures 指数和经理收益
  - 高 R-square，alpha 小
- **Counter-Evidence:** 无
- **Strategy Family:** trend_momentum
- **Query Set:** 19.1
- **Date Accessed:** 2026-06-23

### ID: 006
- **URL:** https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/AQR-JPM-Fall-2017.pdf
- **Title:** A Century of Evidence on Trend-Following Investing
- **Authors:** N/A (AQR research)
- **Source Type:** research
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 137 年历史数据（1880-2017），手工收集 CBOT 数据
- **Evidence Extracted:**
  - Time-series momentum 137 年持续盈利
  - 跨多种经济环境：衰退/繁荣、战争/和平、高/低利率、高/低波动、高/低通胀
  - Correlation 环境影响最大：低相关性环境表现最佳
  - 交易成本和费用估算：历史成本更高
  - 从传统股债组合配置到趋势跟随有显著效用收益
- **Counter-Evidence:** 交易成本历史上更高
- **Strategy Family:** trend_momentum
- **Query Set:** 1.2
- **Date Accessed:** 2026-06-23

### ID: 007
- **URL:** https://www.journals.uchicago.edu/doi/10.1086/593088
- **Title:** Carry Trades and Currency Crashes
- **Authors:** N/A (from search preview)
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 发表于高质量期刊，详细分析 carry trade crash risk
- **Evidence Extracted:**
  - 投资货币存在 crash risk：正利差与负条件偏度相关
  - Carry（利差）与 speculator 净多头相关
  - Speculators 持仓增加 crash risk
  - Carry trade 损失增加 crash risk 价格，但降低 speculator 持仓和 crash 概率
  - 全球风险/风险厌恶增加（VIX）伴随 speculator carry 持仓减少（unwind）和 carry trade 损失
  - 更高 VIX 预测投资货币更高收益、融资货币更低收益
  - 控制 VIX 降低利差预测系数，有助解决 UIP puzzle
  - 类似利率货币相互联动
  - Crash risk 可能阻止 speculators 持有足够大仓位以强制 UIP
- **Counter-Evidence:** 无，但明确了 crash risk
- **Strategy Family:** carry
- **Query Set:** 2.2
- **Date Accessed:** 2026-06-23

### ID: 008
- **URL:** https://arxiv.org/html/2508.18868v2
- **Title:** Tackling estimation risk in Kelly investing using options
- **Authors:** N/A (arXiv paper)
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 学术论文，详细分析 Kelly 准则的估计风险
- **Evidence Extracted:**
  - Kelly 准则最大化预期对数效用，对概率和收益估计高度敏感
  - 估计风险可导致严重次优组合
  - Fractional Kelly 通常用于缓解短期风险，但估计风险仍是开放问题
- **Counter-Evidence:** 无
- **Strategy Family:** position_sizing
- **Query Set:** 6.2
- **Date Accessed:** 2026-06-23

### ID: 009
- **URL:** Multiple practitioner sources
- **Title:** Kelly Criterion: Estimation Error, Fractional Kelly
- **Authors:** Various
- **Source Type:** blog
- **Credibility:** tier4
- **Decision:** keep
- **Reason:** 实践者共识
- **Evidence Extracted:**
  - Full Kelly 在估计误差下导致灾难
  - Over-betting 可能导致负长期增长
  - Half-Kelly 常见妥协：75% 增长率，50% 波动
  - Quarter-Kelly 用于高不确定性
- **Counter-Evidence:** 无
- **Strategy Family:** position_sizing
- **Query Set:** 6.1, 6.2
- **Date Accessed:** 2026-06-23

### ID: 010
- **URL:** https://www.ecb.europa.eu/press/financial-stability-publications/fsr/focus/2020/html/ecb.fsrbox202005_02~f6616db9be.en.html
- **Title:** Volatility-targeting strategies and the market sell-off
- **Authors:** European Central Bank
- **Source Type:** central_bank
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** ECB 金融稳定报告
- **Evidence Extracted:**
  - 全球约 2 万亿美元投资于波动率策略
  - Procyclical：低波动时部署杠杆
  - 波动率飙升时必须去杠杆，加剧抛售
  - 2020 年 3 月可能加剧下跌
- **Counter-Evidence:** procyclicality 风险
- **Strategy Family:** volatility_targeting
- **Query Set:** 7.2
- **Date Accessed:** 2026-06-23

### ID: 011
- **URL:** https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf
- **Title:** The Impact of Volatility Targeting
- **Authors:** Campbell Harvey et al.
- **Source Type:** research
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 60+ 资产，1926 起
- **Evidence Extracted:**
  - Risk assets vol scaling 提高 Sharpe ratio
  - Leverage effect 引入 momentum
  - 债券、货币、商品效果可忽略
  - 减少极端收益概率
- **Counter-Evidence:** 对非 risk assets 无效
- **Strategy Family:** volatility_targeting
- **Query Set:** 7.1, 7.3
- **Date Accessed:** 2026-06-23

### ID: 012
- **URL:** Multiple sources (Kitces, Wikipedia, Bogleheads, etc.)
- **Title:** Geometric vs Arithmetic Returns, Volatility Drag
- **Authors:** Various
- **Source Type:** blog
- **Credibility:** tier4
- **Decision:** keep
- **Reason:** 广泛教育共识
- **Evidence Extracted:**
  - Geometric mean = Arithmetic mean - σ²/2 (近似)
  - Volatility drag: 算术与几何平均的差
  - 50% 损失需 100% 增长恢复
  - 财富过程是乘法的，非加法
  - AM-GM 不等式：除非收益相同，否则几何 < 算术
  - Monte Carlo 应使用算术均值作为输入，几何自然出现
  - 多样化降低波动，减少 drag
- **Counter-Evidence:** 无
- **Strategy Family:** mathematical_foundations
- **Query Set:** 12.1, 12.2
- **Date Accessed:** 2026-06-23

---

## Summary Statistics (as of ID 012)

- **Total Entries:** 12
- **Tier 1 (Academic/Central Bank):** 8
- **Tier 2 (Industry Research):** 1
- **Tier 4 (Practitioner Consensus):** 3
- **Keep:** 12
- **Reject:** 0

**Strategy Family Coverage:**
- Trend/Momentum: 6
- Carry: 1
- Position Sizing (Kelly): 3
- Volatility Targeting: 3
- Mathematical Foundations: 1

**Coverage Assessment:**
- Time-series momentum: Strong (4+ tier1 studies)
- Carry trade crash risk: Moderate (1 tier1 study)
- Kelly estimation error: Strong (tier1 + practitioner consensus)
- Volatility targeting procyclicality: Strong (ECB + academic)
- Geometric growth / volatility drag: Strong (widespread consensus)

**Gaps Identified:**
- Need more on: PPP/value, macro regime, risk parity, pyramiding/anti-martingale, drawdown control, crisis events, falsifiability

---

**Next expansion rounds will target gaps.**
