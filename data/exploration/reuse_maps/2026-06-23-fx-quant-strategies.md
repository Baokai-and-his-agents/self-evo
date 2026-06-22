# FX 量化策略复用地图
# Reuse Map for FX Quantitative Strategies

**日期:** 2026-06-23
**Worker:** scout-worker-fx-01

---

## 可直接复用的成熟研究

### 1. Time-Series Momentum (Moskowitz et al. 2012)
- **来源:** Journal of Financial Economics
- **复用:** 1/3/12 月 look-back，vol targeting 10%
- **适用:** 货币、商品、股指、债券
- **实现:** Pedersen "Demystifying Managed Futures" 完整描述

### 2. Currency Momentum (Menkhoff et al. 2012)
- **来源:** BIS Working Paper 366
- **复用:** Cross-sectional momentum，做多赢家、做空输家
- **适用:** 48 种货币，1976-2010 验证
- **注意:** 交易成本敏感

### 3. Carry Trade Crash Risk (UChicago 2008)
- **来源:** Journal of Financial Economics
- **复用:** VIX hedge, crash risk monitoring
- **适用:** 高 carry 货币组合
- **注意:** 负偏度，需止损

### 4. Kelly Criterion & Fractional Kelly
- **来源:** 广泛文献 + practitioner consensus
- **复用:** Half-Kelly (0.5f*) 或 Quarter-Kelly (0.25f*)
- **适用:** 所有策略的仓位管理
- **注意:** 估计误差敏感，必须保守

### 5. Volatility Targeting (Moreira & Muir 2017)
- **来源:** Journal of Finance
- **复用:** 目标波动率，动态杠杆
- **适用:** Risk assets（股票、信贷）有效，货币效果有限
- **注意:** Procyclicality 风险

### 6. Volatility Drag 公式
- **来源:** 数学事实（AM-GM 不等式）
- **复用:** μ_geo ≈ μ_arith - σ²/2
- **适用:** 所有策略的长期收益预测
- **注意:** 对数正态假设近似

---

## 需要适配的相邻研究

### 1. FX Intraday Time-of-Day Effects
- **来源:** Breedon & Ranaldo (2013), Zhang (2018)
- **复用:** 货币在本地时段贬值，美国时段升值
- **适配:** 具体时段边界、可交易幅度需验证
- **适用:** 日内策略

### 2. Managed Futures / CTA Framework
- **来源:** Pedersen (2012)
- **复用:** 跨资产 TSMOM，58 种工具
- **适配:** 选择适合的货币远期/期货
- **适用:** 长期组合

### 3. Walk-Forward Analysis
- **来源:** 标准回测方法
- **复用:** 5 年训练，1 年测试，滚动
- **适配:** 根据数据频率调整窗口
- **适用:** 所有策略验证

---

## 需要谨慎验证的假设

### 1. London Breakout Strategy
- **来源:** 实践者共识（tier4）
- **验证需求:** 用 FX 历史数据验证具体参数
- **风险:** 假突破率、spread 扩大

### 2. Cointegration Pairs Trading (Intraday)
- **来源:** 学术方法（Bollinger Bands, GARCH）
- **验证需求:** 日内 FX 适用性
- **风险:** 协整关系可能不稳定

### 3. Pyramiding / Anti-Martingale
- **来源:** 理论支持（Kelly, trend following）
- **验证需求:** 反转回吐量化
- **风险:** Whipsaw, 交易成本

---

## 明确避免的方法

### 1. Martingale / Grid Trading / Averaging Down
- **原因:** 有限资本下 ruin probability 极高
- **替代:** Anti-martingale（盈利加仓）

### 2. Full Kelly without Shrinkage
- **原因:** 估计误差下灾难性
- **替代:** Half-Kelly, Quarter-Kelly

### 3. "算术亏损、指数盈利"字面实现
- **原因:** 数学上不一致
- **替代:** 严格风险管理 + 正偏度策略

---

## 可复用的开源工具

### 数据源
- **Dukascopy:** 免费 tick/日线数据
- **TrueFX:** 免费 bid-ask
- **CME:** 货币期货历史数据

### 回测框架
- **Backtrader:** Python，灵活
- **QuantConnect:** 云端，多资产
- **Zipline:** Quantopian 遗产

### 风险管理
- **Kelly 计算器:** 开源实现
- **Volatility targeting:** 简单公式
- **Walk-forward:** 标准方法

---

## 实施顺序建议

### Phase 1: 基础设施（2-4 周）
1. 数据获取与清洗
2. 回测框架搭建
3. 交易成本建模

### Phase 2: 基准策略（4-6 周）
1. Time-series momentum (1/3/12月)
2. Half-Kelly sizing
3. Vol targeting 10%
4. Walk-forward 验证

### Phase 3: 扩展策略（6-8 周）
1. Carry trade with VIX hedge
2. Cross-sectional momentum
3. 组合优化

### Phase 4: 风险控制（2-4 周）
1. Crisis stress test
2. Correlation clustering
3. Portfolio heat monitoring

### Phase 5: 实盘准备（4-6 周）
1. Broker 集成
2. 实时监控
3. Paper trading

**总计: 18-28 周（4.5-7 个月）**

---

## 关键成功因素

1. **保守的 edge/variance 估计:** 避免 Kelly over-betting
2. **完整的交易成本建模:** Bid-ask + slippage + swap + roll
3. **严格的 walk-forward:** 不能用未来数据
4. **Crisis 覆盖:** 至少 2 次货币危机回测
5. **纪律执行:** 不手动干预系统信号

---

## 避免的陷阱

1. **Overfitting:** 过多参数优化
2. **Look-ahead bias:** 使用未来数据
3. **Survivorship bias:** 仅用存活货币
4. **Ignoring costs:** 理论收益 vs 实际收益
5. **Psychological override:** 回撤中放弃系统

---

**复用地图完成。建议从 Time-series momentum + Half-Kelly 开始。**
