# FX Intraday Strategy Taxonomy
# Phase A: Day Trading, No Overnight

**Date:** 2026-06-23  
**Worker:** scout-worker-fx-01  
**Run ID:** 2026-06-23-fx-phase-a-001

---

## Purpose

对外汇日内策略家族进行系统分类，建立理论依据、信号逻辑、数据需求、交易成本敏感性和验证状态的清晰映射。

---

## Classification Framework

每个策略家族按以下维度分类：

1. **理论依据**（为什么应该有效）
2. **信号生成**（如何识别入场/退出）
3. **最佳市场 Regime**（何时有效）
4. **数据需求**（粒度、类型）
5. **交易成本敏感性**（高/中/低）
6. **持仓时间**（典型）
7. **胜率 vs R:R 特征**
8. **学术验证状态**（tier1 证据数量）
9. **主要失败模式**

---

## 1. Trend / Momentum

### 理论依据
- 行为金融：投资者反应不足（under-reaction）和过度反应（over-reaction）
- 信息扩散延迟：新信息在市场参与者间逐步传播
- 时段效应：本币在本地交易时段倾向于贬值（多项学术证实）

### 信号生成
- **移动平均交叉**：5-MA × 20-MA
- **时段动量**：首个半小时收益 vs 最后半小时收益正相关
- **货币对动量**：做多过去赢家，做空过去输家（跨货币）
- **Session breakout**：亚洲区间在伦敦开盘时突破

### 最佳 Regime
- 趋势市场
- 高流动性时段（伦敦开盘、伦敦-纽约重叠）

### 数据需求
- **最小**：1 分钟或 5 分钟 OHLC
- **理想**：Tick 数据或 quote 数据（捕捉时段效应）

### 交易成本敏感性
**中等**：动量策略通常持仓数小时，成本占目标利润比例适中

### 持仓时间
1-4 小时（日内）

### 胜率 vs R:R
- 胜率：45-55%
- R:R：1.5:1 - 2.5:1

### 学术验证
**强（5 篇 tier1 论文）**
- Elaut et al. (2018): 日内动量由流动性提供者风险厌恶驱动
- Breedon & Ranaldo (2013): 时段效应，货币在本地时段贬值
- Zhang (2018): 16 种货币的日内模式，与已实现波动率相关
- Khademalomoom & Narayan (2019): 三种新的日内效应
- Menkhoff et al. (BIS): 货币动量年化 10% 超额收益，但交易成本敏感

### 主要失败模式
- **Regime shift**：趋势转为震荡时连续亏损
- **拥挤交易**：伦敦开盘突破成为零售标准策略，alpha 衰减
- **交易成本侵蚀**：高频版本被 spread + slippage 侵蚀
- **假突破**：亚洲区间窄或极宽时突破失败率高

---

## 2. Breakout

### 理论依据
- 市场在震荡（consolidation）和扩张（expansion）间振荡
- 价格突破区间边界时，流动性和动量共同推动持续移动
- 技术分析自我实现：大量交易者在相同水平设置入场，产生真实突破

### 信号生成
- **Opening Range Breakout (ORB)**：标记开盘 N 分钟区间，蜡烛收盘突破时入场
- **支撑/阻力突破**：前高/低、pivot points、心理水平（1.1000, 1.2000）
- **Bollinger Band 突破**：价格突破 2 标准差带
- **伦敦开盘突破**：亚洲区间在伦敦 7:00-10:00 UTC 突破

### 最佳 Regime
- 波动率扩张期
- 高流动性时段（伦敦、纽约）
- 与更高时间框架趋势对齐时

### 数据需求
- **最小**：5 分钟或 15 分钟 OHLC
- **理想**：成交量数据（确认突破）

### 交易成本敏感性
**中等**：突破策略目标通常是区间宽度的 1-2 倍，成本占比适中

### 持仓时间
0.5-3 小时

### 胜率 vs R:R
- 胜率：40-55%（原始信号）；55-65%（4 小时确认）
- R:R：1.5:1 - 3:1

### 学术验证
**中等（1 篇 tier1 + 学术引用）**
- Holmberg et al. (2013): ORB 策略显著高于零的回报（原油期货）
- 学术文献 2010-2015：伦敦开盘突破 60-70% 持续（按波动率和趋势过滤）
- 但具体外汇现货的 tier1 证据有限

### 主要失败模式
- **假突破（fakeout）**：40-55% 原始突破失败
- **流动性扫荡（liquidity sweep）**：价格突破触发止损后反转
- **时段失败率差异**：10 AM ET 最差（29.9% 胜率），下午最佳（51.7%）
- **区间宽度影响**：窄区间（< $0.50）51% 胜率；宽区间（> $2.00）34.6% 胜率
- **低流动性突破**：亚洲时段 60-70% 假突破率
- **新闻前后**：spread 扩大 10-30×，slippage 激增

---

## 3. Mean Reversion

### 理论依据
- 统计回归：价格偏离均值后倾向于回归
- 超买/超卖修正：极端情绪不可持续
- 震荡市场结构：无方向性趋势时，价格在区间内反弹

### 信号生成
- **RSI 极端**：RSI(14) < 30 买入，> 70 卖出
- **Bollinger Band 触及**：价格触及下轨 + RSI < 30 买入
- **Stochastic 超卖/超买**
- **配对价差回归**：EUR/USD vs GBP/USD 比率超出 2 标准差

### 最佳 Regime
- **震荡市场**（40-60% 的时间）
- **低波动率时段**（亚洲时段，majors）
- **ADX < 25**（非趋势）

### 数据需求
- **最小**：5 分钟或 15 分钟 OHLC
- **配对交易**：两个货币对的同步 tick/quote 数据

### 交易成本敏感性
**高**：均值回归目标小（0.5-1× ATR），胜率虽高但 R:R 小，成本占比大

### 持仓时间
0.5-2 小时（快速回归）

### 胜率 vs R:R
- 胜率：60-75%（有 regime 过滤）；55% 无过滤
- R:R：0.7:1 - 1.5:1

### 学术验证
**中等（2 篇 tier1）**
- Lemishko (SSRN): 协整配对交易，参数优化识别盈利策略
- Huang & Moraux (HAL): Bollinger Bands 策略（无 GARCH）最高利润因子
- 但具体外汇日内的 tier1 证据有限

### 主要失败模式
- **趋势市场崩溃**：RSI 超卖时价格继续下跌，连续亏损
- **"接飞刀"（catching falling knife）**：强趋势中逆势交易
- **假均值回归**：价格触及极端后继续极端（momentum 延续）
- **缺少 regime 过滤**：无 ADX 或趋势过滤时胜率下降 15 个百分点
- **交易成本吞噬**：小目标被 spread + slippage 吞噬

---

## 4. Statistical Arbitrage / Pairs Trading

### 理论依据
- **协整**：两个非平稳序列间的长期均衡关系
- **Law of One Price**：相关资产价格差异应收敛
- **市场中性**：对冲方向性风险，只赚取相对价格修正

### 信号生成
- **协整检验**：Engle-Granger, Johansen, ADF
- **价差 z-score**：hedge ratio 调整的对数价差，z > 2 或 < -2
- **Ornstein-Uhlenbeck 过程**：建模价差均值回归
- **Bollinger Bands on spread**：价差触及 2 标准差带

### 最佳 Regime
- **高相关性维持期**（correlation > 0.80）
- **震荡市场**（两个标的均无强趋势）
- **低波动率时段**

### 数据需求
- **最小**：两个货币对的同步 5 分钟 OHLC
- **理想**：Tick 数据（精确 hedge ratio 计算和入场时机）

### 交易成本敏感性
**非常高**：同时交易两个货币对，成本加倍；价差目标小

### 持仓时间
1-4 小时（等待价差收敛）

### 胜率 vs R:R
- 胜率：65-75%（市场中性优势）
- R:R：0.8:1 - 1.2:1（价差收敛有限）

### 学术验证
**强（2 篇 tier1 + GitHub 专业实现）**
- Lemishko (SSRN): 协整配对交易框架
- Huang & Moraux (HAL): Bollinger Bands 策略验证
- GitHub: Ornstein-Uhlenbeck 过程，完整验证流程

### 主要失败模式
- **协整崩溃（cointegration breakdown）**：regime shift 导致相关性崩溃
- **价差扩大而非收敛**：单边移动持续，价差继续扩大，止损
- **交易成本加倍**：两个货币对的 spread + slippage + commission
- **Hedge ratio 漂移**：最优对冲比率随时间变化，静态比率失效
- **流动性差异**：两个货币对流动性不匹配，slippage 不对称

---

## 5. Order Flow / Microstructure

### 理论依据
- **信息内容**：订单流反映知情交易者的意图
- **流动性不平衡**：bid 侧 vs ask 侧成交量不平衡预示方向
- **Tick 方向聚集**：连续相同方向的 tick 表明持续压力

### 信号生成
- **订单不平衡**：bid volume - ask volume
- **Tick 方向**：uptick vs downtick 聚集
- **Bid-ask spread 动态**：spread 扩大表明不确定性
- **Quote stuffing 检测**：异常高频 quote 更新后 fade

### 最佳 Regime
- **高流动性时段**（伦敦、纽约）
- **新闻发布前后**（订单流信号最强）

### 数据需求
- **必需**：Tick 数据或 Level 2 order book 数据
- **不适合** bar 数据（丢失 microstructure 信息）

### 交易成本敏感性
**极高**：通常需要高频执行，latency 敏感，成本占比极大

### 持仓时间
数秒至数分钟

### 胜率 vs R:R
- 胜率：55-65%（信息优势小但真实）
- R:R：0.5:1 - 1:1（高频小目标）

### 学术验证
**中等（间接证据）**
- Breedon & Ranaldo (2013): 订单流与时段模式相关
- 但具体日内订单流策略的 tier1 证据有限

### 主要失败模式
- **Latency 劣势**：零售交易者 latency 10-100+ ms，HFT < 1 ms，信息优势已被套利
- **数据获取困难**：真实 order book 数据昂贵或不可用
- **Microstructure noise**：tick 数据噪声大，信号提取困难
- **交易成本吞噬**：高频小目标被 spread 完全吞噬
- **Co-location 需求**：无 co-location 时策略不可行

---

## 6. Volatility-Based

### 理论依据
- **Volatility clustering**：高波动率倾向于持续
- **Volatility regime shift**：低波动率后常跟随高波动率（expansion）
- **VIX-FX 相关性**：风险厌恶时 USD/JPY/CHF 作为避险货币

### 信号生成
- **ATR expansion**：ATR 突破 N 日高点
- **Bollinger Band squeeze**：带宽收窄至极低水平后扩张
- **GARCH 预测**：已实现波动率 vs 预测波动率
- **VIX spike**：VIX 跳升，做多 JPY/CHF，做空高 beta 货币

### 最佳 Regime
- **波动率 regime 转换期**
- **风险事件前后**（央行决议、重大数据）

### 数据需求
- **最小**：15 分钟或 1 小时 OHLC（计算 ATR）
- **理想**：高频数据（计算已实现波动率）

### 交易成本敏感性
**中等**：波动率扩张时目标较大，成本占比适中

### 持仓时间
1-4 小时（捕捉波动率扩张）

### 胜率 vs R:R
- 胜率：45-55%
- R:R：1.5:1 - 2.5:1

### 学术验证
**弱（无专门 tier1 日内研究）**
- 波动率聚集是已知现象，但具体日内策略证据有限

### 主要失败模式
- **假扩张（false expansion）**：Bollinger squeeze 后价格未扩张，继续震荡
- **Whipsaw**：波动率扩张但无方向，来回止损
- **GARCH 预测误差**：Regime shift 时模型失效
- **VIX-FX 相关性崩溃**：危机期间相关性不稳定

---

## 7. Event-Driven

### 理论依据
- **信息冲击**：预定宏观数据发布引发价格重定价
- **预期 vs 实际**：经济惊喜指数（actual - forecast）驱动方向
- **Post-announcement drift**：价格反应延续或超调后反转

### 信号生成
- **经济日历**：NFP, CPI, FOMC, ECB 决议前后
- **Pre-positioning**：新闻前 15-30 分钟的方向性偏好
- **Post-release fade**：新闻后初始移动的反转
- **Economic surprise index**：Citi 惊喜指数

### 最佳 Regime
- **预定数据发布窗口**
- **高影响事件**（Tier 1 新闻）

### 数据需求
- **最小**：1 分钟 OHLC + 经济日历
- **理想**：Tick 数据（捕捉新闻跳跃）

### 交易成本敏感性
**极高**：新闻时 spread 扩大 10-30×，slippage 激增

### 持仓时间
数分钟至 1 小时

### 胜率 vs R:R
- 胜率：高度不确定（40-60%）
- R:R：高度可变（0.5:1 - 5:1）

### 学术验证
**弱（无专门 tier1 日内新闻策略）**
- 新闻对价格影响是已知现象，但可交易性证据薄弱

### 主要失败模式
- **不可预测性**：惊喜方向和幅度难以预测
- **Spread 爆炸**：新闻时 spread 扩大 10-30×，入场成本激增
- **Slippage 灾难**：市场订单在新闻时可能滑点 5-10 pips
- **Stop-loss 失效**：价格跳空，止损无法在预定价格成交
- **"数据正确，方向错误"**：数据符合预期但市场反向移动（已 priced in）
- **Flash 反转**：初始移动后 30-60 秒内完全反转

---

## Strategy Interaction Matrix

| 策略 A | 策略 B | 关系 | 说明 |
|--------|--------|------|------|
| Trend/Momentum | Breakout | **互补** | Breakout 可视为 momentum 的触发器 |
| Trend/Momentum | Mean Reversion | **对立** | 不同 regime 有效，组合可平滑收益 |
| Breakout | Mean Reversion | **对立** | Breakout 押注延续，Mean Reversion 押注反转 |
| Stat Arb | Mean Reversion | **相似** | 都基于价格回归，但 Stat Arb 市场中性 |
| Order Flow | All | **正交** | Microstructure 信号可增强任何策略 |
| Volatility | Trend/Breakout | **增强** | 波动率扩张时 trend/breakout 更可靠 |
| Event-Driven | All | **扰动** | 新闻时段应暂停其他策略（成本爆炸）|

---

## Recommended Portfolio Construction

### 目标：跨 Regime 稳健

1. **Trend/Momentum**（40% 资金）：趋势市场主力
2. **Mean Reversion**（30% 资金）：震荡市场主力
3. **Breakout**（20% 资金）：捕捉波动率扩张
4. **Stat Arb**（10% 资金）：市场中性对冲

### Regime Detection
- **ADX(14)**：> 25 趋势，< 20 震荡
- **ATR 百分位**：高波动率 vs 低波动率
- **相关性监控**：Stat Arb 协整 p-value 滚动监控

### Risk Management
- 单策略最大回撤限制：15%
- 组合最大回撤目标：< 20%
- Regime 转换时动态调整资金分配

---

## Data Requirements Summary

| 策略家族 | 最小数据 | 理想数据 | 可用性 |
|----------|----------|----------|--------|
| Trend/Momentum | 1-min OHLC | Tick/quote | 容易 |
| Breakout | 5-min OHLC | + Volume | 容易 |
| Mean Reversion | 5-min OHLC | Tick | 容易 |
| Stat Arb | 5-min OHLC (双货币对) | Tick (双货币对) | 中等 |
| Order Flow | Tick | Level 2 order book | 困难 |
| Volatility | 15-min OHLC | High-freq for realized vol | 容易 |
| Event-Driven | 1-min OHLC + calendar | Tick | 容易 |

**关键缺口：** Order flow / microstructure 策略需要 Level 2 数据，零售交易者通常无法获取或成本高昂。

---

## Academic Validation Summary

| 策略家族 | Tier1 论文数 | 验证状态 | 主要证据来源 |
|----------|--------------|----------|--------------|
| Trend/Momentum | 5 | **强** | Elaut 2018, Breedon 2013, Zhang 2018, Menkhoff BIS |
| Breakout | 1 | **中等** | Holmberg 2013（期货），学术引用 2010-2015 |
| Mean Reversion | 2 | **中等** | Lemishko SSRN, Huang HAL |
| Stat Arb | 2 | **强** | 同 Mean Reversion（协整框架） |
| Order Flow | 0（间接 1） | **弱** | Breedon 2013 提及订单流但非策略 |
| Volatility | 0 | **弱** | 波动率聚集已知，但无日内策略验证 |
| Event-Driven | 0 | **弱** | 新闻影响已知，但可交易性未验证 |

**总结：** Trend/Momentum 和 Stat Arb 有最强学术支持。Breakout 和 Mean Reversion 有中等支持。Order Flow, Volatility, Event-Driven 主要依赖实践者证据。

---

**End of Strategy Taxonomy**
