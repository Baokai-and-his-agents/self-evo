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

### S1: Wald (1945) - Sequential Analysis (Theory)

**URL**: https://doi.org/10.1214/aoms/1177731118 (Annals of Mathematical Statistics, Vol. 16, No. 2)
**标题**: Sequential Tests of Statistical Hypotheses (Paper)
**作者**: Abraham Wald
**机构**: Columbia University
**年份**: 1945
**备注**: "Sequential Analysis" 是 1947 年出版的书名，非本论文标题。本条目引用的是 Wald 1945 原始论文。
**证据层级**: Tier 1
**来源类型**: 同行评审期刊论文
**直接/相邻**: 相邻 - 序贯检验理论基础
**支持/反对**: 既非支持也非反对本机制 - 提供序贯决策理论框架，但未应用于交易仓位递增
**具体主张**: SPRT 在相同错误率下需要最少观测次数（最优性定理）
**局限**: 未涉及交易应用；假设每次观测成本固定，而本机制中止损成本递增
**市场**: N/A（理论）
**频率**: N/A
**样本**: N/A
**Accessed**: 2026-06-23

### S2: Barber & Odean (2000) - Trading Is Hazardous to Your Wealth

**URL**: https://faculty.haas.berkeley.edu/odean/papers/returns/returns.html
**标题**: Trading Is Hazardous to Your Wealth: The Common Stock Investment Performance of Individual Investors
**作者**: Brad M. Barber, Terrance Odean
**机构**: UC Berkeley
**年份**: 2000
**证据层级**: Tier 1
**来源类型**: 同行评审期刊 (Journal of Finance)
**直接/相邻**: 相邻 - 研究高换手率与投资表现，未直接研究亏损后仓位递增行为
**支持/反对**: 相邻证据 - 论文主题是高交易频率（turnover）导致表现更差，并非特指"亏损后增加活动"
**具体主张**: 高换手率投资者年化跑输市场 - 论文研究的是整体交易行为，非条件于亏损后的行为变化
**局限**: 未条件于"亏损后"状态；研究的是交易频率，非仓位大小递增；市场为美国股票 1991-1996
**市场**: 美国股票
**频率**: 个人投资者账户数据（月度）
**样本**: 66,465 households (1991-1996)
**Accessed**: 2026-06-23
**重要修正**: 原文不支持"亏损后增加交易活动者跑输"的主张 - 论文研究的是高换手率交易者整体表现，非亏损条件行为

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

---

## 未能重建的检索线索

以下来源在原始检索中被提及，但无法提供可追溯的 URL/DOI/ISBN，因此**不计入可追溯来源统计**：

### L1: HMM Regime Detection - GitHub regime_sizing.py

**原始线索**: GitHub 代码示例 `regime_sizing.py`
**问题**: 检索时未记录完整 GitHub URL，无法定位原始仓库
**内容摘要**: HMM 检测 BULL/SIDEWAYS/BEAR/HIGH_VOL 状态，应用 Kelly × regime multiplier（100%/60%/25%/10%）
**为何移除**: 无可验证 URL；仓位标量为示例代码，非实证结果；与本机制方向相反（高波动减仓）
**证据层级**: Tier 4（若能定位）
**直接/相邻**: 相邻但方向相反
**Accessed**: 2026-06-23（检索时未保存 URL）

### L2: ForexOp Simulation Study

**原始线索**: ForexOp 网站 Martingale vs Anti-Martingale 模拟研究
**问题**: 原始链接未记录，无法提供可追溯 URL
**内容摘要**: 1000 runs × 200 trades 模拟；Martingale Kurtosis 88.03，最坏 -772 pips/lot vs 平均 +4.48
**为何移除**: 无可验证 URL；模拟非真实市场；参数和市场模型未充分披露；具体数字无法核验
**证据层级**: Tier 4-5（若能定位）
**直接/相邻**: 直接反对（Martingale 风险）
**Accessed**: 2026-06-23（通过二手引用，原始链接未保存）

---

## 重要说明

### 无法重建的其他引用

以下在原 research 中被引用但无法提供可追溯 URL/ISBN/DOI 的内容：

- **Thorp 19.1% 年化且无亏损年**: 需要原始 Princeton-Newport 基金记录或 Thorp 本人著作具体章节页码。Titan FX 2026-04 综述提及但未给出 primary source。
- **Turtle 80%+ 年化**: Curtis Faith 书中提及但具体数字和年份范围需核验原文第 X 页；1983-1987 实盘记录非公开完整账户报表。
- **账户寿命 1-2 年**: 多个 broker/教育网站引用但未提供原始数据来源。
- **50-70% false breakout 比例**: 多个来源提及但统计方法、样本、时间范围不一致。
- **震荡占 30-40% 时间**: 行业经验数字，无 primary research 支持。

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

**可追溯来源总数**: 3 个（S1/S2/S3，均有准确 URL/DOI/ISBN 且主张与来源匹配）
**Tier 1**: 2 个（Wald 1945, Barber & Odean 2000）
**Tier 2-3**: 1 个（Curtis Faith 2007）
**不可追溯线索**: 2 个（L1/L2，移至"未能重建的检索线索"）

**直接支持本机制**: 0 个
**相邻理论（既非支持也非反对）**: 1 个（S1: SPRT 理论框架）
**相邻但方向相反**: 2 个（S2: 高换手率研究, S3: Turtle Pyramiding）
**直接反对**: 0 个可追溯来源（L2 ForexOp 模拟因无 URL 已移除）

**重要说明**:
- S1 Wald 1945: 纯理论，未应用于交易
- S2 Barber & Odean 2000: 研究高换手率，非亏损后行为，不支持也不反对本机制
- S3 Turtle: 盈利后加仓（方向相反）
- 原文中的数值（Kurtosis 88.03、30-40%、>70% 等）来自不可追溯来源或研究推断，已全部移除或标注

**阴性结果的价值**: 9个查询维度的系统检索未找到直接证据，本身是重要的研究发现。

---

*最后更新: 2026-06-23*
