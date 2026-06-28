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

1. **最强学术支持**: FX 日内时段动量（5 个独立 FX 日内研究）
2. **相邻证据**: 跨货币长期动量（Menkhoff 1 研究，非日内）、协整配对交易方法（2 研究，未明确 FX 日内）
3. **假突破普遍**: 多来源定性共识，但具体 FX 率缺失（ORB Setups 数据可能非 FX）
4. **交易成本关键**: EUR/USD 估算约 9-10 USD/lot（必须用实际 broker 数据校准）
5. **Regime 依赖性**: Trend 策略在震荡市场失效，Mean Reversion 在趋势市场"接飞刀"
6. **过拟合风险**: 方法有学术基础（DSR/PBO），阈值需校准（WFE >50% 等为 practitioner heuristic）

### 证据覆盖

- **独立 Tier1 研究**: 9 个（5 个 FX 日内专门，1 个跨货币长期，1 个 ORB 期货，2 个配对交易方法）
- **Tier1 文档/URLs**: 15+ 个（同一研究的多个版本）
- **Tier2-3 研究**: 8 组
- **实践者共识**: 20+ 组（交易成本、过拟合、假突破）
- **GitHub 实现**: 4 个（回测框架、配对交易系统）
- **跨资产参考数据**: ORB Setups 240k+ 交易（可能股票/期货，非 FX）

---

## 策略家族总结

### 强 FX 日内证据（优先回测）
- **FX 日内时段动量**: 5 个独立研究，货币在本地时段贬值

### 相邻证据或方法论支持（需验证适用性）
- **跨货币长期动量**: Menkhoff BIS，长期非日内（相邻证据）
- **协整配对交易方法**: 2 个研究，未明确 FX 日内适用性
- **伦敦开盘突破**: 实践共识强，学术引用存在，参数需验证
- **均值回归**: 学术支持配对交易，日内具体胜率需验证

### 跨资产参考或低证据（需谨慎）
- **假突破过滤**: 定性共识强，但 FX 具体率缺失（ORB 数据可能非 FX）
- **Order Flow**: 数据获取困难，latency 要求高
- **Volatility**: 波动率聚集已知，策略证据薄弱
- **Event-Driven**: 成本爆炸，不可预测性高

---

## 失败模式 Top 3

1. **Overfitting**: 最小 5 年数据，200+ 笔交易；方法成熟（DSR/PBO），阈值需校准
2. **Transaction Cost**: 必须用目标 broker 历史 bid/ask 建模 + slippage，不能用估算值
3. **False Breakout**: 定性共识强（多来源），但 FX 具体率需用历史数据验证

---

## 交付文档

- `2026-06-23-fx-intraday-exploration-brief.md`
- `2026-06-23-fx-intraday-query-matrix.md`
- `2026-06-23-fx-intraday-source-decisions.md`（52 entries，9 个独立 tier1 研究）
- `2026-06-23-fx-intraday-strategy-taxonomy.md`（7 家族）
- `2026-06-23-fx-intraday-failure-landscape.md`（10 模式）
- `2026-06-23-fx-intraday-evidence-map.md`（11 主张）
- `2026-06-23-phase-a-evidence-audit.md`（证据审计修正报告）
- 本报告

---

## 推荐后续行动

1. 获取 5+ 年历史 tick 数据（Dukascopy/TrueFX）
2. 优先回测：FX 日内时段动量（5 个独立研究支持）
3. 验证适用性：伦敦突破（参数需 FX 数据验证）、协整配对（日内适用性）
4. 应用完整验证协议（6 大类检查），阈值在实验中校准
5. 交易成本必须用目标 broker 历史 bid/ask 建模
6. Phase B 在独立 run 执行

---

**Phase A 完成。Phase B 未启动。Claim 保持 active。**
