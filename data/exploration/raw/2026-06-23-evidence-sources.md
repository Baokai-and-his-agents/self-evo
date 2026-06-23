# Evidence Sources - Progressive Probe Position Sizing

**Date:** 2026-06-23
**Worker:** scout-worker-fx-sizing-01
**Run ID:** 2026-06-23-fx-sizing-001

本文档记录用于研究结论的可追溯来源。每条记录包含 canonical URL、标题、作者/机构、年份、市场、频率、样本、来源类型、直接/相邻、支持/反对的具体主张、局限、accessed_at。

---

## 证据层级分类

**Tier 1**: 同行评审期刊论文
**Tier 2**: Working papers / 学术会议 / 硕博士论文
**Tier 3**: 实践者经验（有回测数据/代码）
**Tier 4**: 行业共识 / 教育内容 / 工程实现
**Tier 5**: 轶事 / 营销材料

---

## 来源记录

### S1: Wald (1945) - Sequential Probability Ratio Test

**URL**: https://projecteuclid.org/journals/annals-of-mathematical-statistics (Project Euclid archive)
**标题**: Sequential Analysis
**作者**: Abraham Wald
**机构**: Columbia University
**年份**: 1945
**证据层级**: Tier 1
**来源类型**: 同行评审期刊
**直接/相邻**: 相邻 - 序贯检验理论基础
**支持/反对**: 既非支持也非反对本机制 - 提供序贯决策理论框架，但未应用于交易仓位递增
**具体主张**: SPRT 在相同错误率下需要最少观测次数（最优性定理）
**局限**: 未涉及交易应用；假设每次观测成本固定，而本机制中止损成本递增
**市场**: N/A（理论）
**频率**: N/A
**样本**: N/A
**Accessed**: 2026-06-23

### S2: Barber & Odean (2000) - Trading Is Hazardous to Your Wealth

**URL**: https://faculty.haas.berkeley.edu/odean/papers (无法提供完整DOI，原文献需通过学术数据库检索)
**标题**: Trading Is Hazardous to Your Wealth: The Common Stock Investment Performance of Individual Investors
**作者**: Brad M. Barber, Terrance Odean
**机构**: UC Berkeley
**年份**: 2000
**证据层级**: Tier 1
**来源类型**: 同行评审期刊
**直接/相邻**: 相邻 - 研究亏损后交易行为，但未直接研究仓位递增
**支持/反对**: 反对 - 亏损后增加交易活动的投资者年化跑输 3.8%
**具体主张**: 亏损后增加活动的交易者表现更差
**局限**: 研究的是交易频率增加，非仓位大小递增；市场为美国股票，非外汇
**市场**: 美国股票
**频率**: 个人投资者账户数据
**样本**: 大量零售账户（具体数量需查原文）
**Accessed**: 2026-06-23（通过二手引用）

### S3: Curtis Faith - Way of the Turtle (2007)

**URL**: 书籍ISBN 978-0071486644
**标题**: Way of the Turtle: The Secret Methods that Turned Ordinary People into Legendary Traders
**作者**: Curtis Faith
**机构**: N/A（原Turtle Trading参与者）
**年份**: 2007（描述1983-1987系统）
**证据层级**: Tier 2-3
**来源类型**: 实践者回忆录
**直接/相邻**: 相邻 - Turtle Pyramiding是盈利后加仓，与本机制方向相反
**支持/反对**: 反对 - 实证支持anti-martingale（盈利后加仓），非止损后递增
**具体主张**: Pyramiding在价格朝有利方向移动0.5N时加仓；1983-1987实盘平均年化高回报（具体数字需核验原文）
**局限**: 回忆录而非实时记录；1987 crash单日亏损重大；市场环境可能不可重复
**市场**: 商品期货、外汇
**频率**: 日线Donchian breakout
**样本**: 1983-1987实盘
**Accessed**: 2026-06-23（通过二手引用和公开Turtle Rules文档）

### S4: HMM Regime Detection - GitHub regime_sizing.py

**URL**: 无法提供完整GitHub URL（检索时未记录）
**标题**: regime_sizing.py示例代码
**作者**: 不详
**机构**: N/A（开源社区）
**年份**: 不详
**证据层级**: Tier 4
**来源类型**: 工程实现
**直接/相邻**: 相邻 - Regime detection后仓位缩放，触发条件是状态识别非止损序列
**支持/反对**: 相邻但方向相反 - 高波动regime减仓（10-25%），低波动增仓（100%）
**具体主张**: HMM检测BULL/SIDEWAYS/BEAR/HIGH_VOL状态，应用Kelly乘以regime multiplier
**局限**: 无同行评审；代码实现无回测验证；仓位标量（100%/60%/25%/10%）是示例而非优化结果
**市场**: 不详
**频率**: 不详
**样本**: 无实证数据
**Accessed**: 2026-06-23

### S5: ForexOp Simulation Study

**URL**: 无法提供URL（原始链接未记录）
**标题**: Martingale vs Anti-Martingale模拟研究
**作者**: ForexOp
**机构**: N/A（教育网站）
**年份**: 不详
**证据层级**: Tier 4-5
**来源类型**: 模拟研究
**直接/相邻**: 相邻 - 对比Martingale与Anti-Martingale，但使用模拟而非真实市场
**支持/反对**: 反对Martingale - Fat tail风险（Kurtosis 88.03），最坏情况-772 pips/lot vs平均+4.48
**具体主张**: 1000 runs × 200 trades模拟；Martingale震荡市场+4.48 pips/lot，趋势市场负收益；Anti-Martingale相反
**局限**: 模拟数据非真实市场；参数设置和市场模型未充分披露；Kurtosis具体计算方法不详
**市场**: 模拟（未指定货币对）
**频率**: 模拟
**样本**: 1000×200=200k模拟交易
**Accessed**: 2026-06-23（通过二手引用）

---

## 重要说明

### 无法重建的引用

以下在原research中被引用但无法提供可追溯URL或完整引用信息的内容已从证据账本中移除：

- **Thorp 19.1%年化且无亏损年**: 需要原始Princeton-Newport基金记录或Thorp本人著作具体章节。Titan FX 2026-04综述提及但未给出primary source。
- **Turtle 80%+年化**: Curtis Faith书中提及但具体数字和年份范围需核验原文；1983-1987实盘记录非公开完整账户报表。
- **账户寿命1-2年**: 多个broker/教育网站引用但未提供原始数据来源。
- **50-70% false breakout比例**: 多个来源提及但统计方法、样本、时间范围不一致。
- **震荡占30-40%时间**: 行业经验数字，无primary research支持。
- **核心假设失败概率>70%**: 原research推断，非引用来源。
- **每10-20周期fat-tail**: 原research推断。
- **HMM仓位标量100%/60%/25%/10%**: 来自示例代码，非实证优化结果。
- **p<0.01显著性**: 原research设计参数，非引用结果。

### 检索覆盖范围

本次研究通过以下方式检索：
- Exa AI搜索引擎（Query 1-9）
- 公开网页和学术档案
- 二手引用的交叉核验

**未覆盖**：
- 付费学术数据库全文检索（JSTOR, ScienceDirect, SSRN完整库）
- 专有交易系统内部研究
- 监管机构非公开数据
- 对冲基金/Prop firm内部报告

### 阴性结果的重要性

在以下维度的检索中**未找到**直接支持"止损后递增仓位"的证据：
- Progressive position sizing after losses（Query 1）
- Increasing position size after consecutive losses（Query 2）
- Limited martingale + trend following（Query 3）
- Sequential testing应用于position sizing（Query 4）
- Change-point detection触发仓位递增（Query 5）
- HMM regime switching触发止损后增仓（Query 6）
- False breakout聚集预测趋势（Query 9）

**发现的一致模式**：
- 止损/亏损/drawdown → 减仓（风险管理共识）
- 盈利/趋势确认 → 增仓（anti-martingale, pyramiding）
- 高波动/不确定regime → 减仓
- Martingale（亏损后加仓）→ 所有来源强烈反对

---

## 证据账本统计

**独立来源总数**: 5个可追溯primary/secondary sources
**Tier 1**: 2个
**Tier 2-3**: 1个
**Tier 4-5**: 2个

**直接支持本机制**: 0个
**相邻理论（既非支持也非反对）**: 1个（SPRT）
**相邻但方向相反**: 3个（Turtle, HMM, Barber & Odean）
**直接反对**: 1个（ForexOp Martingale模拟）

**阴性结果的价值**: 9个查询维度的系统检索未找到直接证据，本身是重要的研究发现。

---

*最后更新: 2026-06-23*
