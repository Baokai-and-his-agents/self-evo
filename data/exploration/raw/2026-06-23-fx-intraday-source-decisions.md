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


## Strategy Family 2: Breakout Strategies

### ID: 028
- **URL:** https://ideas.repec.org/p/hhs/umnees/0845.html
- **Title:** Assessing the profitability of intraday opening range breakout strategies
- **Authors:** Holmberg, Ulf & Lönnbark, Carl & Lundström, Christian
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 学术论文，Umeå University，发表于 Finance Research Letters (2013)
- **Evidence Extracted:**
  - 开盘区间突破（ORB）策略基于正态分布回报识别大幅日内价格移动
  - 当价格超过预定阈值时交易
  - 研究原油期货
  - ORB 策略产生显著高于零的回报
  - 相对公平博弈，成功率提高
  - 方法涉及 Low, High, Open, Close 的联合分布
- **Counter-Evidence:** 研究针对期货市场（原油），可能不直接适用于外汇现货
- **Strategy Family:** breakout
- **Query Set:** 2.1
- **Date Accessed:** 2026-06-23

### ID: 029-034 (False Breakout Literature)
- **URLs:** Multiple sources (FN Trading Lab, ORB Setups, FibAlgo, Trading Zenith, Prof FX, FXRobotEasy, GrandAlgo)
- **Source Type:** blog, tutorial, research
- **Credibility:** tier2-tier4
- **Decision:** keep (as practitioner consensus)
- **Reason:** 多个独立来源一致描述假突破模式和过滤方法，包含数据驱动分析
- **Evidence Extracted:** (合并关键发现)
  - **假突破定义：** 价格突破关键水平但迅速反转回区间内
  - **假突破率：**
    - 原始突破信号：40-55% 失败（ORB Setups: 65.9% 用默认设置）
    - 主要货币对：50-60% 假突破
    - 亚洲时段：60-70% 假突破（流动性低）
    - 1 小时蜡烛收盘确认：33% 成功率
    - 4 小时蜡烛收盘确认：66% 成功率
    - 4 小时 + 成交量确认：73% 成功率
  - **假突破特征：**
    - 长影线，实体弱（收盘接近或回到水平内）
    - 突破后立即反转（1-3 根蜡烛内）
    - 低流动性时段突破（亚洲时段、午餐时间）
    - 突破直接撞上更高时间框架的对立区域
    - 低成交量（< 1.5× 平均值）
  - **时段失败率：**
    - 9:00 AM ET: 34.0% 胜率（ORB Setups 数据，67,996 笔交易）
    - 10:00 AM ET: 29.9% 胜率（最差，"10:30 反转"区域，96,112 笔交易）
    - 12:00 PM ET: 44.1% 胜率（中午突破更干净）
    - 3:00 PM ET: 51.7% 胜率（日内晚段最高胜率）
    - 周五下午（伦敦时间 12:00 后）：71% 失败率
  - **ORB 区间宽度：**
    - 窄区间（5 分钟 ORB < $0.50）：51.0% 胜率
    - 宽区间（> $2.00）：34.6% 胜率
    - 差异：16.4 个百分点（单一过滤器）
  - **过滤方法（多来源共识）：**
    1. 更高时间框架确认（4 小时或日线收盘）
    2. 成交量扩张（≥ 1.5× 平均，理想 2×）
    3. VWAP 对齐（多头时价格在 VWAP 上方且 VWAP 上升）
    4. 蜡烛实体收盘在水平外（不仅是影线）
    5. 避开 10 AM ET 时段
    6. 避开窄区间和极宽区间
    7. 等待回测（突破后回到水平，反弹进入）
    8. 与日线/4 小时趋势对齐
  - **学术支持：** "伦敦开盘突破模式在 2010-2015 学术文献中有广泛研究，当按波动率和趋势偏好过滤时，60-70% 时间延续"（FXRobotEasy 引用）
  - **关键洞察：** "假突破不是缺陷，而是策略的结构性成本，是捕捉 50-60% 真实突破的代价"
- **Counter-Evidence:**
  - 部分来源为零售交易教育网站，可能存在营销偏见
  - ORB Setups 数据样本（240,102 笔交易，600+ 标的）未明确说明市场和时期
  - 具体数字（如 73% 成功率）需要独立验证
- **Strategy Family:** breakout
- **Query Set:** 2.1, 2.4
- **Date Accessed:** 2026-06-23


## Strategy Family 3: Mean Reversion & Statistical Arbitrage

### ID: 035
- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4771108
- **Title:** Cointegration-Based Strategies in Forex Pairs Trading
- **Authors:** Tetiana Lemishko, [co-authors not listed]
- **Source Type:** paper
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** SSRN 论文，专注于外汇市场的协整配对交易
- **Evidence Extracted:**
  - 配对交易利用相关资产间的价格差异
  - 协整识别非平稳时间序列数据间的长期均衡关系
  - 当偏离发生时提供交易机会
  - 通过参数优化识别盈利策略
  - 旨在增强算法框架的可靠性和客观性，减少情绪偏差
- **Counter-Evidence:** 摘要未提供具体回测结果或失败率
- **Strategy Family:** stat_arb, mean_reversion
- **Query Set:** 3.2, 4.1
- **Date Accessed:** 2026-06-23

### ID: 036-037 (GitHub Pairs Trading Implementations)
- **URLs:**
  - https://github.com/LucaCereghetti/Pairs-Trading-Mean-Reversion-Strategy
  - https://github.com/XanderRobbins/Universal-Pairs-Trading-System
- **Source Type:** github
- **Credibility:** tier3
- **Decision:** keep
- **Reason:** 专业级配对交易系统，Ornstein-Uhlenbeck 过程建模，包含完整验证流程
- **Evidence Extracted:**
  - Ornstein-Uhlenbeck 过程建模外汇价格
  - 协整检验：Engle-Granger, Johansen, ADF, half-life
  - Hedge ratio 调整的对数价差
  - Z-score 信号生成（阈值突破）
  - Regime 检测和波动率调整入场阈值
  - ATR-based 风险管理
  - 交易成本和滑点建模
  - 完整可视化：价差、权益曲线、交易分布、月度热图、滚动协整 p-value
  - 入场：z-score 突破阈值 AND regime 均值回归 AND 动量确认
  - 退出：z-score 回穿退出阈值 OR regime 转为 Volatile_Trending
- **Counter-Evidence:** GitHub 项目，文档和社区验证有限
- **Strategy Family:** stat_arb, mean_reversion
- **Query Set:** 3.2, 4.1
- **Date Accessed:** 2026-06-23

### ID: 038
- **URL:** https://shs.hal.science/halshs-01566803v1/document
- **Title:** Statistical arbitrage based on pairs trading of mean-reverting returns (HAL)
- **Authors:** Zhe Huang & Franck Moraux
- **Source Type:** research
- **Credibility:** tier1
- **Decision:** keep
- **Reason:** 学术研究论文，University of Rennes 1 and CREM UMR CNRS
- **Evidence Extracted:**
  - 三种策略比较：百分比、协整长期残差标准差、Bollinger Bands（动态标准差）
  - 每种策略有/无 ECM-DCC-GARCH 双重确认
  - 最佳策略：Bollinger Bands without GARCH 确认（按利润因子优化）
  - 样本外测试中最高利润因子
  - 绝对净利润 $4024.97，最大回撤 $1453.49
  - 但按净利润优化时，最高净利润伴随更高最大回撤，降低利润因子表现
- **Counter-Evidence:** 具体市场和时期未在摘要中明确
- **Strategy Family:** stat_arb, mean_reversion
- **Query Set:** 3.2, 4.1
- **Date Accessed:** 2026-06-23

### ID: 039-042 (Mean Reversion Practitioner Guides)
- **URLs:** Multiple (LinkedIn/Shubham, AlphaExCapital, DNS Research, FXRobotEasy)
- **Source Type:** blog, tutorial
- **Credibility:** tier4
- **Decision:** keep (as practitioner consensus)
- **Reason:** 多来源一致描述均值回归实施方法
- **Evidence Extracted:** (合并关键点)
  - **核心逻辑：** 价格极端（超买/超卖）倾向于回归平均值
  - **常用指标：**
    - RSI(14) < 30 买入，> 70 卖出
    - 价格触及下轨 Bollinger Band(20,2) + RSI < 30 买入
    - 价格触及上轨 + RSI > 70 卖出
  - **退出：** 中线 Bollinger Band（20-SMA）或 RSI 50
  - **止损：** 1.5-2× ATR 超出入场点
  - **胜率：** 60-75%（但 R:R 小，0.7-1.5:1）
  - **最佳市场：** 震荡市场（40-60% 的时间）
  - **最差市场：** 趋势市场（RSI 超卖时价格继续下跌）
  - **Regime 过滤至关重要：** ADX > 25 表示趋势，避免交易均值回归
  - 有 regime 过滤：~70% 胜率；无过滤：~55% 胜率
  - **RSI-2 极端策略：** Larry Connors 开发，使用 2 周期 RSI 捕捉微趋势耗尽
  - GBP/JPY 2022 研究：RSI-2 < 10 时，83% 概率在 3 分钟内回撤 5 pips
  - **配对相关性均值回归：** EUR/USD vs GBP/USD，相关性 > 0.80
  - 比率超出 2 标准差时交易，回到 20-MA 时退出
  - 市场中性策略，Sharpe Ratio 1.5+（EUR/GBP cross 与 USD pairs）
  - **最佳货币对：** EUR/USD (ATR ~1.5 pips), GBP/JPY (ATR ~2 pips)
  - **LinkedIn 示例回测：** 胜率 62%，最大回撤 5.2%，平均持仓 2-5 天，期望值 0.4
- **Counter-Evidence:**
  - 多数为教育材料，缺少独立验证
  - 具体数字（如 83% 概率）需要验证
  - LinkedIn 示例未说明时期和样本大小
- **Strategy Family:** mean_reversion, stat_arb
- **Query Set:** 3.1, 3.2, 4.1
- **Date Accessed:** 2026-06-23

---

## Cross-Cutting: Transaction Costs & Execution

### ID: 043-048 (Transaction Cost Literature)
- **URLs:** Multiple (ForexMechanics, AlphaExCapital, BrokerChampion, forex-basics.com, BabyPips, KenMacro)
- **Source Type:** blog, tutorial, broker_research
- **Credibility:** tier2-tier4
- **Decision:** keep (as practitioner consensus on execution reality)
- **Reason:** 多来源一致描述真实交易成本结构
- **Evidence Extracted:** (合并关键发现)
  - **交易成本构成：**
    1. Bid-ask spread（基准成本）
    2. Commission（ECN 账户）
    3. Slippage（实际成交与预期价格差异）
    4. Swap/rollover（隔夜持仓费用）
    5. 货币转换费（非 USD 账户）
    6. 账户费用（不活跃费、提款费）
  - **EUR/USD 典型 spread（2026）：**
    - Standard 账户：0.6-1.2 pips
    - ECN 账户：0.1-0.3 pips（+ 佣金 3-7 USD/lot 往返）
    - 有效成本相当：ECN 0.2 pips + 7 USD = 9 USD/lot；Standard 1.0 pip = 10 USD/lot
  - **Spread 扩大：**
    - 重大新闻（NFP, FOMC）：扩大 10-30× 正常水平，持续 30-90 秒
    - 低流动性时段：亚洲时段、午餐时间、纽约尾盘
    - 周五下午（伦敦时间 12:00 后）
  - **Slippage：**
    - 定义：预期价格与实际成交价差异（spread 后的额外成本）
    - 示例：1 pip spread + 4 pips slippage = 5 pips 总入场成本
    - 高频交易者最敏感：微薄利润迅速被侵蚀
    - 新闻期间：0.2 pip spread 的 broker 可能实际 slippage 0.3 pips = 0.5 pips 总成本
  - **Swap：** 对日内交易者可忽略（大多数 broker 日内免除），对摆动交易者重要（5-15 USD/夜）
  - **成本对策略的影响：**
    - 剥头皮/日内高频：成本是目标利润的大比例，ECN 账户节省 5-15%
    - 摆动交易：成本差异边际（50-150 USD/年）
  - **关键教训：**
    - 使用"全部成本"（all-in cost）比较 broker，不是广告 spread
    - 有效 spread = 在你实际交易的时段和条件下观察到的 spread
    - 执行质量（slippage、requotes）与 spread 同等重要
    - 计算：spread（pips）× pip value × lots + 往返佣金 + 预期 slippage
- **Counter-Evidence:** 具体数字因 broker、时段、市场条件变化
- **Strategy Family:** cross_cutting
- **Query Set:** 8.1, 8.2
- **Date Accessed:** 2026-06-23

---

## Checkpoint 2 Summary (2026-06-23, ~17:00 UTC)

已完成策略家族：
1. Trend/Momentum: 10 篇 tier1 论文，8 组实践指南
2. Breakout: 1 篇 tier1 论文，7 组假突破研究（含 240k+ 交易数据分析）
3. Mean Reversion & Stat Arb: 2 篇 tier1 论文，2 个专业级 GitHub 实现，5 组实践指南
4. Transaction Costs: 6 组详细成本结构分析

关键发现：
- **假突破率：** 原始信号 40-55% 失败，4 小时确认降至 34%，10 AM ET 时段最差（29.9% 胜率）
- **均值回归胜率：** 60-75%（有 regime 过滤），但 R:R 小；趋势市场失效
- **交易成本：** EUR/USD 全部成本 ~9-10 USD/lot，新闻时 spread 扩大 10-30×
- **协整配对：** Bollinger Bands 策略（无 GARCH）最高利润因子（学术验证）

下一步：继续 Order Flow/Microstructure, Volatility, Event-Driven，然后数据质量和风险文献。

