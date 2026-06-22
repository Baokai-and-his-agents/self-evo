# FX Intraday Phase A 研究报告
# 日内交易，不隔夜

**日期:** 2026-06-23  
**Worker:** scout-worker-fx-01  
**Run ID:** 2026-06-23-fx-phase-a-001  
**Issue:** #13 Phase A  
**状态:** Phase A 完成，Phase B 未启动

---

## 执行摘要

本报告系统研究外汇日内量化策略（持仓数分钟至数小时，日终前平仓），为后续回测实验建立证据充分的研究底座。研究严格串行执行，Phase A 完成，Phase B 未启动。

### 核心发现

1. **最强学术支持**: 日内时段动量（5 篇 tier1 论文）和协整配对交易（2 篇 tier1）
2. **假突破普遍**: 原始突破信号 40-55% 失败，4 小时确认可降至 34%
3. **交易成本关键**: EUR/USD ~9-10 USD/lot，新闻时 spread 扩大 10-30×
4. **Regime 依赖性**: Trend 策略在震荡市场失效，Mean Reversion 在趋势市场"接飞刀"
5. **过拟合风险**: 多来源共识检测方法（WFE > 50%, DSR > 0.95, PBO < 0.05）

### 证据覆盖

- **Tier1 学术论文**: 10 篇（独立研究）
- **Tier2-3 研究**: 8 组
- **实践者共识**: 20+ 组（交易成本、过拟合、假突破）
- **GitHub 实现**: 4 个（回测框架、配对交易系统）
- **数据驱动分析**: 240k+ 交易（ORB Setups）

---

## 策略家族总结

### Tier 1 证据（优先回测）
- **日内时段动量**: 5 篇 tier1 论文，货币在本地时段贬值
- **跨货币动量**: Menkhoff BIS，年化 10% 超额收益
- **协整配对交易**: 2 篇 tier1，市场中性

### Tier 2 证据（需验证）
- **伦敦开盘突破**: 实践共识强，学术引用存在
- **假突破过滤**: 240k+ 交易数据分析
- **均值回归**: 学术支持配对交易，日内需验证

### Tier 3 证据（需谨慎）
- **Order Flow**: 数据获取困难，latency 要求高
- **Volatility**: 波动率聚集已知，策略证据薄弱
- **Event-Driven**: 成本爆炸，不可预测性高

---

## 失败模式 Top 3

1. **Overfitting**: 最小 5 年数据，200+ 笔交易，WFE > 50%
2. **Transaction Cost**: 精确 bid/ask 建模 + slippage ≥ 0.3 pips
3. **False Breakout**: 40-55% 失败率，4h 确认 + 成交量过滤

---

## 交付文档

- `2026-06-23-fx-intraday-exploration-brief.md`
- `2026-06-23-fx-intraday-query-matrix.md`
- `2026-06-23-fx-intraday-source-decisions.md`（48 来源）
- `2026-06-23-fx-intraday-strategy-taxonomy.md`（7 家族）
- `2026-06-23-fx-intraday-failure-landscape.md`（10 模式）
- `2026-06-23-fx-intraday-evidence-map.md`（11 主张）
- 本报告

---

## 推荐后续行动

1. 获取 5+ 年历史数据（Dukascopy/TrueFX）
2. 优先回测：时段动量、协整配对、4h 确认突破
3. 应用完整验证协议（6 大类检查）
4. Phase B 在独立 run 执行

---

**Phase A 完成。Phase B 未启动。Claim 保持 active。**
