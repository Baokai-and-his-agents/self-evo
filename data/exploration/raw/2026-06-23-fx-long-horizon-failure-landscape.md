# FX Long-Horizon Failure Landscape
# Phase B: Dynamic Position Management

**Date:** 2026-06-23
**Worker:** scout-worker-fx-01

---

## Top 10 Failure Modes

### 1. Kelly Estimation Error
- **最危险**
- Over-estimate edge → over-bet → 负增长
- 2× Kelly = 零增长，>2× = 保证亏损
- Mitigation: Half-Kelly, shrinkage

### 2. Carry Crash
- 2008年10月，VIX 飙升，speculator unwind
- 负偏度：小赚累积，一次暴亏
- Mitigation: VIX hedge, position limits

### 3. Volatility Targeting Procyclicality
- 波动飙升 → 强制去杠杆 → 加剧抛售
- ECB: 2020年3月 risk parity 可能加剧下跌
- Mitigation: Conditional vol targeting, leverage caps

### 4. Pyramiding Reversal Drawdown
- 加仓后反转，放大亏损
- Example: 2× position, 15% reversal = 76% loss
- Mitigation: Tiered stop-loss, max leverage

### 5. Regime Shift
- Trend → Range
- Whipsaw 累积
- Mitigation: Regime filter, reduce size in low-trend

### 6. Gap & Slippage
- Weekend gap, central bank surprise
- Stop-loss 失效
- Mitigation: Avoid holding over events, buffer

### 7. Correlation Convergence
- 危机时相关性 → 1
- 分散失效
- Mitigation: Tail hedge, cross-asset

### 8. Sample Insufficiency
- 长期策略需 20+ 年数据
- Regime 覆盖不足
- Mitigation: Walk-forward, stress test

### 9. Transaction Costs
- Bid-ask, roll, swap
- 高频调整侵蚀收益
- Mitigation: Cost-aware sizing, lower turnover

### 10. Martingale / Grid
- 亏损加仓
- **保证破产**（有限资金）
- Mitigation: 永不使用
