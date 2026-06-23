# Evidence Log - Progressive Probe Position Sizing

**Date:** 2026-06-23
**Worker:** scout-worker-fx-sizing-01
**Run ID:** 2026-06-23-fx-sizing-001

---

## Query 1: "progressive position sizing after losses"

**Engine:** Exa AI
**Results:** 10 articles
**Time:** 2026-06-23

### Key Findings

**主流共识：减仓 after losses（与本机制相反）**
- Dr. Mansi progressive exposure: 连续止损后**递减** ROTE（1% → 0.5% → 0.25% → 0.12%）
- Forex Mechanics: 连续亏损后减半仓位，防止 drawdown 加深
- 普遍建议：3 连亏后减半风险百分比

**Anti-Martingale 为主流**
- 盈利后加仓，亏损后减仓
- 对比：Martingale（亏损后加仓）被明确标记为"gambler's ruin"
- 专业基金标准做法：compound sizing + floor（防止 drawdown 时仓位过小）

**相关但相反的实践**
- Dr. Mansi 系统：0.12% → 0.25% → 0.5% → 1%，但触发条件是**连续盈利**
- 触发递增的是成功，非失败
- 连续止损触发递减

**Martingale 明确否定**
- "Doubling down after losses" = fastest road to ruin
- 无限 Martingale 在有限资本下必然破产
- 所有来源一致警告

**未找到：止损后递增的直接证据**
- 无学术研究支持止损后逐级放大仓位
- 无专业交易者公开使用此机制
- 主流共识：止损后应减仓或保持，非增仓

### 证据层级

**Tier 3-4（弱/轶事）：**
- Dr. Mansi (via Substack): 实践者经验，但方向相反
- Forex 教育站点：行业共识，anti-martingale
- 无 Tier 1-2 学术来源

### 阴性结果（重要）

**"Progressive position sizing after losses" 在主流文献中：**
- 不存在作为推荐策略
- 存在作为**警告**（即 Martingale）
- 唯一递增场景：盈利后（anti-martingale）

---

## 初步结论

**维度 1 查询 Q1.1a 结果：阴性**
- 前 10 结果无相关直接证据
- 发现大量相反建议（减仓 after losses）
- 需继续其他关键词变体确认

---

## Query 2: "increasing position size consecutive losses"

**Engine:** Exa AI
**Results:** 8 articles
**Time:** 2026-06-23

### Key Findings

**明确的否定共识（更强）**
- "Increasing size after losses is one of the most dangerous responses" (DXP Analytics)
- "Fastest way to blow an account" (Otrai, M1NDTR8DE)
- "Account destruction" (multiple sources)
- Gambler's fallacy: 连续亏损不增加下次获胜概率

**实证数据（重要）**
- Barber & Odean (2000): 亏损后增加活动的交易者年化跑输 3.8%
- 专业公司强制规则：10% drawdown 后减仓 50%，15% 后减 75%
- Funded prop firms: 3 连亏后减仓 25-50%

**推荐做法（与本机制完全相反）**
- 3 连亏 → 减仓 50%
- 5 连亏 → 减仓 75% 或停止
- Daily loss limit: 2-3% 或 2-3 个完整止损

**数学论证**
- 1% 风险：10 连亏 = 10% drawdown（可控）
- 5% 风险：10 连亏 = 40% drawdown（灾难性）
- 亏损非对称：-50% 需要 +100% 恢复

**心理机制**
- Tilt: 报复性交易
- Revenge sizing: 情绪驱动的加仓
- 连亏期间决策能力下降

### 证据层级

**Tier 3（弱但一致）：**
- 行业共识（交易教育平台）
- 实践规则（prop firms）
- Barber & Odean 研究（Tier 2，但未直接针对本机制）

### 阴性结果（强）

**"Increasing position size after consecutive losses"：**
- 在所有来源中被**明确警告为危险行为**
- 无任何来源推荐或中性讨论
- 唯一出现场景：作为错误案例

**合法增仓场景：**
- 账户增长（自然的权益比例效应）
- 策略验证后（100+ 交易证明 edge）
- 波动率下降（需要更大仓位维持相同 %风险）
- **但触发条件均非"连续亏损"**

---

## Query 3: "limited martingale" + "trend following"

**Engine:** Exa AI
**Results:** 8 items
**Time:** 2026-06-23

### Key Findings

**EA 营销材料（Tier 4-5）**
- "Trend Marti EA" 系列：趋势过滤 + 有限加仓
- 明确警告："Martingale increases risk", "possible total loss"
- 建议 $2000-3000 最小账户，max 2-3 layers
- Lot multiplier: 1.2x-1.5x（非 2x doubling）

**核心机制（类似但仍危险）**
- 趋势确认后，回调时分层入场
- 每层固定距离（如 15-40 pips）
- 全局权益保护、日亏损上限
- **关键区别：先确认趋势，在趋势内加仓（非震荡试探）**

**风险警告（一致且强烈）**
- "Martingale inherently increases risk"
- "Catastrophic loss is mathematically inevitable" (Oreshnikbot)
- "Guaranteed to fail due to unchecked expansion" (Grid trading video)
- 13 年无 martingale EA 存活 = "strongest longevity signal"

**理论否定**
- Capital.com: "High-risk, unsuitable for real-world trading"
- Zaye Capital: "One of the most dangerous approaches"
- 市场趋势 ≠ 赌场随机，连亏不是独立事件

**有界变种尝试**
- AI trend filter + sideways detection (Sideways Martingale EA)
- 仅在震荡时启用 martingale，趋势时阻断
- 跨货币对对冲（JPY pairs mean reversion）
- **但这些是 EA 营销，非学术验证**

### 证据层级

**Tier 4（轶事/营销）：**
- EA 产品页面
- YouTube 教程
- 无同行评审

**Tier 5（已被反驳）：**
- 无限 martingale 在所有学术讨论中被否定
- 有限变种：未找到学术支持，仅有 EA 营销

### 阴性结果

**"Limited martingale in trend following"：**
- 无学术研究
- 仅有 EA 产品声称实现，但伴随强烈免责
- 所有来源强调风险而非优势

**发现的相邻概念（但不同）**
- Pyramiding/scaling in：盈利后在趋势中加仓（anti-martingale）
- Layered entries：多次入场，但固定仓位或递减
- **本机制（止损后递增）未出现**

---

## 阶段 1 小结（维度 1：直接证据）

**查询 Q1.1a-d 完成，饱和条件达到：**
- 前 30+ 结果无相关直接证据
- 发现大量相反建议（止损后减仓）
- 唯一相关内容为 EA 营销 + 风险警告

**核心发现：**
1. **止损后递增仓位**在主流文献/实践中**不存在作为推荐策略**
2. 存在作为**警告案例**（martingale）
3. 专业共识：止损后应减仓或保持，非增仓
4. 实证数据：亏损后加仓者年化跑输 3.8%（Barber & Odean）

**下一步：转向维度 2（相邻理论）**
- Sequential testing & change-point detection
- 可能提供理论基础（即使实践不存在）

---

## Query 4: Sequential testing in trading

**Engine:** Exa AI (via agent-reach)
**Query:** "sequential probability ratio test trading"
**Results:** 10 items
**Time:** 2026-06-23T10:15Z

### Key Findings

**SPRT 核心理论（强）**
- Abraham Wald 1945 原始论文（Project Euclid）：最优序贯检验，平均样本量比固定样本减少约 50%
- Wald-Wolfowitz 证明：SPRT 在相同错误率下需要最少观测次数（最优性定理）
- 应用领域：质量控制、医疗试验、A/B 测试、计算机化考试

**交易应用（相邻但非直接证据）**
1. **CUSUM / Girshick-Rubin 算法**（KIT 论文）：
   - 应用于 DAX 日内交易，使用 change-point detection
   - CUSUM 优于 Girshick-Rubin，在 3 种成本场景下均跑赢被动持有
   - **关键区别**：这些是 change-point 检测算法，用于识别趋势转折点，而非仓位递增策略
   - **相邻性**：提供了"序贯累积证据 → 触发交易信号"的框架，但未涉及止损后仓位递增

2. **A/B 测试中的 SPRT**（Statsig, MetricGate）：
   - 允许连续监控，无 peeking penalty
   - 使用 likelihood ratio 作为决策指标
   - 比固定样本测试更快达到结论
   - **相邻性**：序贯决策框架，但应用场景是统计推断，非交易仓位管理

3. **Modified SPRT (MSPRT)**（PMC 论文）：
   - 针对复合假设的改进版本
   - 减少样本量需求
   - 使用 Uniformly Most Powerful Bayesian Test (UMPBT) 设定备择假设
   - **相邻性**：统计方法改进，但未见交易应用

4. **Drift Diffusion Model (DDM) 连接**（Mathematical Psychology）：
   - SPRT 是 DDM 的离散时间版本
   - DDM 用于认知决策模型
   - **相邻性**：理论基础，但应用于心理学决策，非金融交易

**未找到：止损序列 → 仓位递增的直接应用**
- 无文献讨论"连续止损后增加仓位"作为 SPRT 应用
- SPRT 在交易中的应用限于：
  - Change-point detection（趋势转折识别）
  - Regime switching detection（状态切换检测）
  - 信号确认的序贯测试
- **关键缺失**：SPRT 用于"证据累积 → 决策"，但未见用于"止损序列 → 递增仓位"

### 证据层级

**Tier 1-2（理论基础强）：**
- Wald 1945 原始论文：SPRT 最优性证明
- Wald-Wolfowitz 定理：理论完备
- **但应用于交易的证据层级降为 Tier 3**

**Tier 3（相邻应用）：**
- KIT 论文：CUSUM/Girshick-Rubin 在 DAX 的实证
- 市场：德国股指，频率：日内
- 样本：1999-2012（CUSUM 论文）
- **直接证据**：序贯检测算法可盈利
- **非直接证据**：未涉及仓位递增，只有固定仓位的 binary 信号（long DAX or cash）

**Tier 4（工具/教程）：**
- Statsig, MetricGate：商业 A/B 测试工具
- 无交易应用

### 相邻理论价值

**SPRT 可能为本机制提供的理论框架：**

1. **序贯证据累积模型：**
   - 每次止损 = 一次观测
   - 累积 log-likelihood ratio：Λ_n = Σ log[P(止损 | 震荡) / P(止损 | 趋势)]
   - 当 Λ_n 跨越阈值 → 判定"仍在震荡，趋势未到"
   - **仓位递增的理论基础**：若 P(趋势即将到来 | n 次止损) 随 n 递增，可增加仓位

2. **与 Hazard Rate 的连接：**
   - SPRT 隐含假设：观测提供关于假设的信息
   - 类比：止损序列提供关于 regime 的信息
   - **前提**：必须建立 P(止损 | 震荡) ≠ P(止损 | 趋势)

3. **最优停止规则：**
   - SPRT 给出"何时停止采样"的最优解
   - 类比：本机制需要"何时停止递增"的规则（K 上限）
   - **区别**：SPRT 最小化样本量，本机制最小化累计亏损

**关键理论缺口：**
- SPRT 假设每次观测成本固定
- 本机制中，每次"观测"（止损）成本递增（r_n 递增）
- SPRT 最优性定理不直接适用于递增成本场景

### 阴性结果（重要）

**"Sequential testing for position sizing" 不存在作为研究方向**
- SPRT 在交易中的应用 = change-point detection + 信号确认
- 未见"序贯检验 → 动态仓位递增"的文献
- **结论**：SPRT 提供理论类比，但不是本机制的直接支持证据

### 下一步查询方向

**需要进一步检索：**
1. Change-point detection + position sizing（Query 2.2b）
2. Regime switching + adaptive sizing（Query 3.1a-d）
3. Hazard rate + trend emergence（Query 6.2a-c）

**当前饱和判断：**
- Sequential testing (SPRT) 理论基础已充分覆盖
- 相邻应用（change-point）已识别
- 直接应用（仓位递增）不存在
- **维度 2.1 (Sequential Hypothesis Testing) 查询饱和**

---

## Query 5: Change-point detection + position sizing

**Engine:** Exa AI (via agent-reach)
**Query:** "change point detection forex position sizing"
**Results:** 10 items
**Time:** 2026-06-23T10:30Z

### Key Findings

**Regime Detection + Dynamic Sizing（相邻证据，Tier 3-4）**

1. **HMM Regime Detection + Kelly Sizing**（多个来源）：
   - GitHub `regime_sizing.py`：HMM 检测 4 种状态（BULL/SIDEWAYS/BEAR/HIGH_VOL）
   - 仓位标量：BULL 100%, SIDEWAYS 60%, BEAR 25%, HIGH_VOL 10%
   - Kelly criterion **乘以** regime multiplier
   - **相邻性**：Regime → 仓位调整，但触发条件是**状态识别**，非连续止损

2. **VIX-Regime Position Sizing**（Trends and Breakouts, 2026-05）：
   - VIX < 16: 1.0x，VIX 16-25: 0.6-0.75x，VIX > 25: 0.3-0.5x
   - Buffer zone 避免频繁切换（15-17 之间插值）
   - **相邻性**：波动率 regime → 仓位缩放，但**减仓而非增仓**

3. **Dynamic Kelly with Regime Detection**（AlgoKing blog, 2026-03）：
   - 作者自述 2023 年固定仓位亏损 $180k
   - 改用 regime-adjusted Kelly：高波动期缩小仓位
   - Drawdown scaling：5-15% DD 时线性减仓至 25%
   - 回测对比（6 个月）：Sharpe 1.31 → 1.89，Max DD 11.4% → 7.2%
   - **相邻性**：Drawdown → 减仓，与本机制方向**相反**

**Change-Point Detection 算法应用**

4. **BOCPD (Bayesian Online Change-Point Detection)**（OSQF 2025）：
   - Adams & MacKay 2007 方法，实时检测分布参数变化
   - 应用于 SPY/IBIT 日内数据
   - 用于识别 regime 切换，配合 Matrix Profile Analysis
   - **应用场景**：检测到 change-point 后**停止交易或切换策略**，非增加仓位

5. **PELT Algorithm (Penalized Exact Linear Time)**（QuantBeckman, 2025-12）：
   - 动态规划最优分割时间序列
   - 识别 PnL 结构性漂移
   - Switch-off 决策：检测负期望后**清仓**
   - **关键逻辑**：检测恶化 regime → 风险降低，非增仓

6. **Directional Change (DC) + HMM**（arXiv 2309.15383）：
   - 改进 DC 框架：上升/下降趋势区分对待，引入衰减系数
   - HMM 检测异常市场状态以**降低风险**
   - Bayesian Optimization 优化阈值
   - 应用于 forex tick 数据，多货币对
   - **相邻性**：Regime detection → 风险控制，但未见止损递增

7. **Deep Learning + Changepoint (LSTM)**（arXiv 2105.13727）：
   - "Slow Momentum with Fast Reversion"
   - LSTM 直接学习仓位 X_t ∈ (-1, 1)
   - Changepoint score ν_t 作为特征输入
   - Gaussian Process CPD，短回溯窗口
   - **策略**：高 disequilibrium 时保守（slow momentum + fast mean-reversion）
   - **相邻性**：CPD 信号 → 策略切换，但仓位由 NN 直接输出，非递增规则

**ATR-Based Regime Sizing**（AlphaEx Capital, 2024-01）：
   - ATR > 1.5× 20日均值 → regime 变化信号
   - Trend regime: 1 ATR 止损，1% 仓位
   - Range regime: 2-3 ATR 止损，0.5% 仓位
   - **相邻性**：Regime → 仓位调整，trend 时**增仓**但触发条件是 ADX/ATR，非止损序列

**Directional Change (DC) Scaling Laws**（Voicu 2012, MSc thesis）：
   - 13 货币对验证 12 条 scaling laws
   - Coastline trader：threshold λ 触发后 pyramiding
   - **Pyramiding 定义**：趋势中加仓，期待反转前获利
   - Average duration 本身符合 scaling law
   - **相邻性**：Overshoot 后加仓，但触发条件是**趋势确认**（DC overshoot），非止损

### 证据层级

**Tier 3（实践经验，非同行评审）：**
- AlgoKing blog：个人交易记录，6 个月实盘
- QuantBeckman：Substack 技术博客，有代码但无学术验证
- Trends and Breakouts：VIX regime sizing，backtest 声称但未披露细节

**Tier 3-4（工程实现）：**
- GitHub `regime_sizing.py`：开源代码，HMM + Kelly
- FibAlgo blog：8 年 tick 数据，regime 聚类分析（73% crisis 跟随 compression）

**Tier 2-3（Working papers / arXiv）：**
- arXiv 2309.15383：Directional Change + HMM，forex tick 数据实证
- arXiv 2105.13727：LSTM + CPD，多资产回测
- OSQF 2025：BOCPD，学术会议但非期刊

**Tier 4（MSc thesis）：**
- Voicu 2012：Directional Change scaling laws，硕士论文

### 核心发现总结

**Regime detection + position sizing 的主流模式：**
1. **高波动 / 不确定 regime → 减仓**（VIX, HMM HIGH_VOL, BOCPD switch-off）
2. **趋势确认 regime → 增仓**（ATR trend, DC overshoot）
3. **Drawdown → 减仓**（AlgoKing drawdown scaling 5-15% → 25%）

**与本机制的关键区别：**
- 主流：Regime detection → 仓位调整
- 本机制：**止损序列** → 仓位递增
- 主流触发：技术指标（ATR, ADX, VIX）、HMM 状态、change-point
- 本机制触发：**连续止损事件**

**相邻但相反的证据：**
- AlgoKing：Drawdown 时**减仓**至 25%，与本机制（止损后增仓）方向相反
- VIX regime：高波动**减仓**至 30-50%，与本机制递增逻辑相反

**相邻且部分一致的证据：**
- ATR trend regime：趋势确认后 1% 仓位 vs range 时 0.5% → 趋势时**增仓**
- DC pyramiding：overshoot 确认后加仓
- **但触发条件不同**：这些是趋势**确认后**加仓，本机制是震荡试探期**止损后**递增

### 阴性结果（关键）

**"止损序列 → 仓位递增"不存在于 change-point 文献：**
- Change-point detection 用于识别 regime 切换
- 识别到 change-point 后的标准反应：
  - 切换策略（trend → mean-reversion）
  - 降低风险（switch-off, 减仓）
  - 调整参数（止损距离、持有期）
- **未见**：连续止损 → 增加仓位

**主流共识（再次确认）：**
- Drawdown / 连续亏损 → 减仓（risk management 101）
- 高不确定性 / 检测到 regime 切换 → 减仓或停止
- 趋势确认 → 增仓（但确认条件非止损序列）

### 理论相邻价值

**Change-point detection 可能为本机制提供的框架：**
1. **Regime 推断**：若止损聚集 = 震荡 regime 信号，CPD 可量化后验概率
2. **Hazard rate 建模**：P(趋势开始 | 已 n 次止损, no trend yet)
3. **最优停止**：何时放弃递增（类似 PELT 的 switch-off）

**但关键前提未验证：**
- 止损聚集是否真的预测趋势到来？
- 还是止损聚集只是震荡持续的信号？
- Change-point 文献未提供止损序列的预测性证据

### 下一步查询方向

**需要进一步检索：**
1. Regime switching + HMM 的理论基础（Query 3.1a-d）
2. Hazard rate + trend emergence（Query 6.2a-c）
3. Martingale vs anti-martingale 实证对比（Query 4.2a-c）
4. Trend following professional systems（Query 5.1a-d）

**当前饱和判断：**
- Change-point detection 理论与应用已充分覆盖
- 主流模式清晰：高不确定性 → 减仓，趋势确认 → 增仓
- 止损序列 → 递增的直接证据**仍不存在**
- **维度 2.2 (Change-Point Detection) 查询饱和**

---

## Query 6: HMM regime switching position sizing

**Engine:** Exa AI (via agent-reach)
**Query:** "hidden markov model regime switching position sizing trading"
**Results:** 10 items
**Time:** 2026-06-23T10:45Z

### Key Findings (Summary)

**HMM + Position Sizing 的主流架构（Tier 3-4，工程实现）：**

1. **Regime 检测 → 仓位缩放**（一致模式）：
   - Bull: 100% size，Bear: 25% size，High-vol: 10% size（多个来源一致）
   - Mental Momentum AI：波动率反比缩放（volatility-scaled sizing）
   - Cube.exchange：高波动 regime → 减少 leverage
   - **核心逻辑**：高不确定性/高波动 → 减仓，低波动趋势 → 增仓

2. **Soft allocation vs hard switching**（RegimeSense GitHub）：
   - 使用 HMM posterior probabilities 加权策略
   - 70% bull + 30% choppy → 混合配置
   - 避免 regime 边界的剧烈切换
   - **相邻性**：概率分配，非止损触发

3. **Regime-aware stop-loss**（QuantStart, Mental Momentum）：
   - Low-vol regime: 1 ATR 止损
   - High-vol regime: 3-4 ATR 止损（更宽）
   - **逻辑**：高波动时放宽止损避免 stop-hunting，同时减小仓位维持风险恒定

4. **Walk-forward / rolling OOS**（多个来源）：
   - HMM 需要持续重新训练（regime-switching-portfolio GitHub）
   - 避免 lookahead bias
   - Transition matrix 学习 regime 持续性（平均 33 交易日）

### 证据层级

**Tier 3-4（工程实现 + blog）：**
- GitHub 开源项目：RegimeSense, regime-switching-portfolio, market-regime-detection
- Blog 教程：PythonAndTrading, QuantInsti, QuantifiedStrategies
- 无同行评审，但有可运行代码和回测

**Tier 4（Working paper）：**
- CANA journal (2024)：NIFTY 50 HMM + Monte Carlo，Sharpe 1.05 vs 0.67

### 核心共识（再次确认）

**HMM + position sizing 的标准做法：**
1. **训练 HMM**：2-4 个状态（bull/bear/sideways/crisis）
2. **特征**：returns, volatility, correlation, VIX 等
3. **Regime → size multiplier**：
   - Calm/bull: 1.0x
   - Sideways: 0.6x
   - Bear/high-vol: 0.25-0.5x
   - Crisis: 0.1x 或退出
4. **Risk parity**：volatility scaling 保持恒定风险单位

### 与本机制的对比

**主流 HMM sizing：**
- 触发：HMM 状态识别（技术指标 + returns + volatility）
- 方向：高波动/不确定 → **减仓**
- 目标：降低 drawdown，平滑 equity curve

**本机制：**
- 触发：**连续止损序列**
- 方向：止损后 → **增仓**
- 目标：震荡期小仓试探，趋势期大仓获利

**关键区别（再次强调）：**
- HMM 文献中，止损/drawdown 是**减仓信号**
- 本机制将止损作为**增仓触发**
- 两者方向**完全相反**

### 阴性结果（持续确认）

**"止损后增仓"未出现于 HMM 文献：**
- HMM 检测到高波动/bear regime → 减仓或退出
- HMM 检测到 crisis → 减仓至 10% 或清仓
- 未见任何来源使用 HMM 检测"止损聚集"作为增仓信号

### 下一步

已完成维度 2（Sequential testing + Change-point + HMM），核心发现一致：
- 高不确定性 → 减仓
- 趋势确认 → 增仓
- 止损/drawdown → 减仓
- **止损 → 增仓的直接证据不存在**

继续检索：
- Martingale vs anti-martingale 实证（Query 4.2）
- Trend following professional systems（Query 5.1-5.3）
- 条件概率与 hazard rate（Query 6.1-6.2）

**维度 3 (Regime Switching) 查询饱和**

---

## Query 7: Martingale vs Anti-Martingale empirical

**Engine:** Exa AI (via agent-reach)
**Query:** "martingale anti-martingale forex empirical comparison performance"
**Results:** 10 items
**Time:** 2026-06-23T11:00Z

### Key Findings (Summary)

**Martingale vs Anti-Martingale 实证对比（Tier 4-5，模拟/轶事）：**

1. **ForexOp 模拟研究**（1000 runs × 200 trades = 1.2M 数据点）：
   - Martingale：Flat 市场 +4.48 pips/lot，Trending 市场 -2.56 (bull) / -3.38 (bear)
   - Anti-Martingale：Flat 市场 -6.98 pips/lot，Trending 市场 +3.55 (bull) / +3.87 (bear)
   - **结论**：Martingale 在震荡市场表现更好，Anti-Martingale 在趋势市场表现更好
   - Martingale 最坏情况：-772 pips/lot（fat tail），Kurtosis 88.03
   - Anti-Martingale：Max loss -86.8 pips/lot，Kurtosis 0.14（正态分布）

2. **Titan FX 综述**（2026-04）：
   - Edward Thorp (Princeton-Newport, 1969-1988)：19.1% 年化，无亏损年，最大月亏 -3%
   - Thorp 使用 Kelly Criterion（数学正确的 anti-martingale）
   - **核心论点**：Kelly 根据 edge 调整仓位，Martingale 根据历史结果调整（错误）
   - 建议 fractional Kelly (1/4 Kelly) 实盘使用

3. **Ichimoku + Money Management 对比**（IJSTM 2023）：
   - EURUSD H1，2015-2017 三年，初始 $10k
   - No MM: 865% ROI
   - Reverse Martingale: 2437% ROI
   - Cumulative Win: 2863% ROI
   - Max DD: No MM -15.7%, Reverse Martingale -16.2%, Cumulative Win -18.6%
   - **统计检验**：One-Way ANOVA p=0.3679 > 0.05，三者无显著差异（样本不足）

4. **MA Crossover EA 回测**（Agape.com）：
   - 原始 MA crossover：亏损
   - Reverse MA crossover + Martingale：7 个主要货币对中 6 个盈利
   - Anti-Martingale（相同信号）：总利润 3× Martingale
   - **但**：3 个账户接近爆仓
   - **结论**：Anti-Martingale 需要有 edge 的信号

5. **Fixed-Fractional vs Martingale 数学对比**（Zaye Capital, 2026-04）：
   - Martingale：7 连亏后需要 12.8 lots（超出账户容量）
   - Fixed-Fractional (1% risk)：50% drawdown 后仍存活，风险 £50
   - **结论**：Fixed-fractional 无争议地优于 Martingale

### 证据层级

**Tier 4-5（模拟研究、轶事、EA 回测）：**
- ForexOp 模拟：1000 runs，但无真实市场数据
- Ichimoku 研究：真实回测但仅 3 年，统计不显著
- EA 回测：多个来源，但无同行评审
- 无 Tier 1-2 学术期刊研究

### 核心共识（强烈一致）

**Martingale 的致命缺陷（所有来源一致）：**
1. **Fat tail risk**：小概率巨额亏损（-772 pips vs 平均 +4.48）
2. **指数级资本需求**：7-10 连亏后超出账户容量
3. **Trend 中失败**："Doubling down against prevailing trends"
4. **账户寿命短**：平均 1-2 年爆仓（broker 数据）
5. **最终期望为负**：即使短期盈利

**Anti-Martingale 的优势（所有来源一致）：**
1. **有界风险**：最大亏损 = 初始仓位
2. **趋势市场表现好**：复利盈利
3. **正态分布**：Kurtosis 接近 0，无 fat tail
4. **需要 edge**：无 edge 时期望为 0，非负无穷

**关键区别（再次明确）：**
- Martingale：亏损后加仓（与本机制相似）
- Anti-Martingale：盈利后加仓（与本机制相反）
- Fixed-Fractional Kelly：根据 edge 调整（与本机制不同）

### 与本机制的对比

**本机制 = 有限 Martingale 变种：**
- 触发：止损后递增（类 Martingale）
- 上限：K 次 + 总风险预算（有限版本）
- 递增方式：算术或几何（可选）

**Martingale 实证结论对本机制的启示：**
1. **Fat tail 风险**：即使有上限 K，仍可能在 K 次失败后累计巨额亏损
2. **Trend 中失败**：若止损序列发生在持续趋势（非震荡 → 趋势转换），会"double down against trend"
3. **账户寿命**：有限 Martingale 延长寿命，但仍有破产风险
4. **需要条件概率改善**：若止损后 p 不上升，本机制继承 Martingale 的风险特征

### 阴性结果（持续确认）

**"止损后递增"在 Martingale 文献中的定位：**
- 所有来源**强烈反对** Martingale 用于真实交易
- 建议 Anti-Martingale（盈利后加仓）或 Fixed-Fractional
- 无任何来源支持"有限 Martingale 在震荡 → 趋势场景下有优势"
- **主流共识**：Martingale 仅在理论赌场（无限资本 + 无限时间）有效

### 理论价值（相邻但警示性）

**本机制与 Martingale 的关系：**
- 本机制是 **有限、有预算的 Martingale 变种**
- 若止损后条件概率不改善，本机制**继承 Martingale 的风险**
- 关键区别：本机制假设止损序列提供 regime 信息（震荡 → 趋势切换点）
- **若假设不成立**：本机制退化为 Martingale，实证显示高破产风险

### 下一步

已完成关键实证对比，结论明确：
- Martingale：所有来源强烈反对
- Anti-Martingale：需要 edge，趋势中有效
- 本机制定位：有限 Martingale + regime 信息假设

剩余关键查询：
- Trend following professional systems (Turtle, ATR sizing)
- Hazard rate + trend emergence（止损序列是否预测趋势）
- Campaign trading / pyramiding（趋势中加仓）

**维度 4 (Martingale 实证) 查询饱和**

---

## Query 8: Turtle trading position sizing

**Engine:** Exa AI (via agent-reach)
**Query:** "turtle trading position sizing units ATR forex"
**Results:** 8 items
**Time:** 2026-06-23T11:15Z

### Key Findings (Summary - Tier 2-3, 原始规则文档)

**Turtle Trading Position Sizing（经典 trend-following system）：**

1. **N-Value (ATR 20-day)**：市场波动率标准化单位
2. **Unit 计算**：Unit = 1% of Account / (N × Dollars per Point)
3. **Pyramiding（盈利后加仓）**：
   - 初始 entry：1 unit
   - 价格朝有利方向移动 0.5N：加 1 unit
   - 最大 4 units per market
4. **Stop-loss**：2N from entry（约 2% 风险）
5. **Position limits**：
   - Single market: 4 units
   - Closely correlated: 6 units
   - Loosely correlated: 10 units
   - Single direction (long or short): 12 units

**与本机制的对比（关键）：**

| 维度 | Turtle Trading | 本机制（有限递增试探） |
|------|---------------|-------------------|
| 触发条件 | 价格朝有利方向移动 0.5N | 止损后 |
| 加仓方向 | **盈利后** | **亏损后** |
| 风险管理 | 2N 止损，总风险恒定 1% | 累计风险递增 |
| 理论基础 | Trend-following + volatility normalization | Regime 推断（假设） |
| 实证验证 | 1983-1987 平均年化 80%+ | **不存在** |

**关键区别（再次明确）：**
- Turtle：趋势**确认后**（breakout）加仓，盈利时加仓
- 本机制：震荡**试探期**止损后加仓

**Turtle Pyramiding ≠ 本机制：**
- Turtle 加仓前提：已有 1 unit 盈利 0.5N
- 本机制加仓前提：前 n 次止损
- 方向完全相反

### 证据层级

**Tier 2-3（原始文档 + 实践验证）：**
- Curtis Faith "Way of the Turtle"（2007 book）
- 原始 Turtle Rules PDF（Dennis & Eckhardt 1983）
- 1983-1987 实盘：起始 $500k-$2M，平均年化 80%+
- 但 1987 crash 单日亏损 20-40%（验证风险管理重要性）

### 阴性结果（持续确认）

**Turtle 系统中"止损后加仓"不存在：**
- Pyramiding 仅在盈利时发生
- 止损后动作：重新评估 entry signal，非增加现有仓位
- 若 4 连续 breakout 失败 → 减少 unit size 或暂停（风险控制）

**主流 trend-following 共识：**
- 盈利后加仓（anti-martingale）
- 亏损后减仓或保持
- Volatility normalization（ATR-based）

---

## 阶段性总结（Query 1-8）

**已完成维度：**
1. 直接证据（Q1-3）：**阴性**，未找到"止损后递增"的直接支持
2. Sequential testing（Q4）：相邻理论，但应用于 change-point detection，非仓位递增
3. Change-point detection（Q5）：主流应用为 regime 切换后**减仓或策略切换**
4. HMM regime switching（Q6）：高波动 regime → **减仓**，低波动 → 增仓
5. Martingale 实证（Q7）：**强烈反对**，fat tail 风险，账户寿命短
6. Turtle trading（Q8）：**Anti-martingale**（盈利后加仓），与本机制相反

**核心发现（一致且强烈）：**
- **止损/亏损 → 减仓**（风险管理 101）
- **盈利/趋势确认 → 增仓**（anti-martingale, pyramiding）
- **高不确定性/高波动 → 减仓**（regime switching）
- **止损后增仓的直接证据不存在**

**本机制的定位：**
- 有限 Martingale 变种（与主流相反）
- 关键假设：止损序列提供 regime 信息（未验证）
- 若假设不成立：继承 Martingale 风险（fat tail, 高破产概率）

**剩余关键查询（时间有限，优先级排序）：**
1. **Hazard rate + trend emergence**（Query 6.2）：止损序列是否预测趋势？**最关键**
2. Consecutive losses + subsequent win probability（Query 6.1）
3. Campaign trading / multiple entries（Query 5.3）

由于时间和 token 限制，现在优先完成 Hazard rate 查询（最关键的实证问题），然后整理交付物。

---

## Query 9: False breakout / whipsaw clustering before trends

**Engine:** Exa AI (via agent-reach)
**Query:** "false breakout whipsaw clustering predict trend forex"
**Results:** 8 items
**Time:** 2026-06-23T11:30Z

### 关键发现（Summary）

**False Breakout 统计（多个来源一致）：**

1. **高频率**（Tier 4 实践数据）：
   - 50-60% 所有 breakout 尝试为 false breakout
   - Asian session（低流动性）：60-70% 为 fakeout
   - 1H candle breakout：33% 成功率 → 67% 失败率
   - 4H candle breakout：66% 成功率（过滤后）

2. **False breakout 不预测趋势**（关键阴性结果）：
   - FibAlgo（10k+ trades, 2012-2024）：false breakout 是"最昂贵的模式"
   - 主流建议：**避免** false breakout，而非利用其预测趋势
   - False breakout 后市场行为：**随机**（可能继续震荡、反转或趋势）

3. **False breakout 成因**（所有来源一致）：
   - **Stop hunting / liquidity grab**：机构故意触发散户止损
   - **低流动性**：Asian session, 周五下午，午休时段
   - **新闻 whipsaw**：消息发布前后的剧烈波动
   - **缺乏 volume**：无真实买盘/卖盘支持

4. **过滤 false breakout 的方法**（非利用其预测）：
   - 4H candle close confirmation（将成功率从 33% 提升到 66%）
   - Volume 扩张 1.5× 平均
   - ADX > 25（趋势强度）
   - Retest 成功（突破后回测支撑/阻力）
   - 高时间框架确认

### 与本机制的关键对比

**本机制假设：**
- 连续 false breakout / 止损 → 震荡持续，但趋势即将到来
- Hazard rate 递增：P(趋势开始 | 已 n 次止损) ↑

**实证证据：**
- **False breakout 不预测趋势**（所有来源一致）
- False breakout 是**噪音**，非信号
- 主流策略：**避免** false breakout 或 **fade** false breakout（反向交易）
- **未见任何来源**支持"false breakout 聚集预测趋势到来"

**Fade false breakout 策略**（与本机制部分相似但不同）：
- 触发：价格突破后快速反转
- 动作：在反转方向入场（**非增加原方向仓位**）
- 止损：突破极值之外
- 目标：回到 range 中点
- **关键区别**：这是 **mean-reversion**，非 trend anticipation

### 证据层级

**Tier 4-5（实践经验 + 商业分析）：**
- FibAlgo：10k+ trades backtest（2012-2024）
- TradingZenith：2026 数据，73% 过滤成功率声称
- SlickTrade, FNTradingLab：教育内容，统计数据未验证

**Tier 3（arXiv working paper）：**
- BreakGPT (arXiv 2402.07536)：LLM 用于 breakout detection
- 创建 breakout dataset，但未涉及"false breakout 聚集预测趋势"

### 阴性结果（最关键）

**"False breakout 聚集预测趋势"不存在于文献：**
- False breakout 被视为**干扰**，非信号
- 无任何来源支持"连续 false breakout → 趋势概率上升"
- 相反共识：**避免 false breakout 密集区域**

**时间/流动性模式（与本机制假设相反）：**
- False breakout 聚集于**低流动性时段**（Asian session, 午休）
- 真实 breakout 聚集于**高流动性时段**（London/NY open, session overlap）
- **结论**：false breakout 聚集 = 低流动性噪音，非趋势前兆

**Regime 视角（再次确认）：**
- False breakout 聚集 = **Range-bound market**（震荡市场特征）
- 真实 breakout = **Trend initiation**（趋势启动）
- **无证据**支持"range 中 false breakout 次数 → 预测 trend 到来时间"

### 本机制核心假设的实证状态

**假设：止损序列提供 regime 信息，hazard rate 递增**
**实证结果：不支持**

1. ✗ False breakout 聚集不预测趋势
2. ✗ 止损序列被视为噪音，非信号
3. ✗ 主流建议：避免 false breakout，非增仓等待趋势
4. ✗ 无任何来源讨论"止损次数 → 趋势概率"

**若止损序列无预测性：**
- 本机制退化为有限 Martingale
- 继承 Martingale 风险（fat tail, 高破产率）
- 无增量价值，仅重新分配风险

---

## 最终证据总结（Query 1-9 完成）

### 直接证据搜索结果：阴性

**查询维度 1-3（直接证据）：**
- "Progressive position sizing after losses"：不存在，发现相反建议（减仓）
- "Increasing size after consecutive losses"：所有来源警告危险
- "Limited martingale + trend following"：仅 EA 营销，伴随强烈免责

**结论：止损后递增仓位的直接支持证据不存在**

### 相邻理论分析结果：相邻但不支持

**Sequential testing（Q4）：**
- SPRT 理论完备，应用于 change-point detection
- 未见用于"止损序列 → 仓位递增"

**Change-point detection（Q5）：**
- BOCPD, PELT, DC+HMM 应用于 regime 识别
- 识别后标准反应：减仓或策略切换，**非增仓**

**HMM regime switching（Q6）：**
- 主流架构：高波动/bear → 减仓（25-10%），低波动/bull → 增仓（100%）
- 方向与本机制**完全相反**

### 实证对比结果：强烈反对

**Martingale vs Anti-Martingale（Q7）：**
- Martingale：所有来源**强烈反对**，fat tail risk，账户寿命 1-2 年
- Anti-Martingale：需要 edge，趋势中有效
- Thorp Kelly Criterion：19.1% 年化，无亏损年（1969-1988）

**Turtle trading（Q8）：**
- Pyramiding：**盈利后**加仓（0.5N step）
- 1983-1987 实盘 80%+ 年化
- 与本机制方向**完全相反**

**False breakout（Q9）：**
- 50-70% breakout 为 false，尤其低流动性时段
- False breakout **不预测趋势**
- 主流策略：**避免**或 fade（mean-reversion）

### 核心共识（跨所有查询一致）

**风险管理铁律（所有来源）：**
1. 止损/亏损/drawdown → **减仓**
2. 盈利/趋势确认 → **增仓**（anti-martingale）
3. 高波动/不确定性 → **减仓**
4. 止损后增仓 → **不存在**

**本机制的定位：**
- 有限 Martingale 变种（与主流相反）
- 关键假设：止损序列提供 regime 信息（**实证不支持**）
- 若假设不成立：继承 Martingale 风险特征

---
