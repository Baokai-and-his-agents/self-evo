# FX Intraday Quantitative Strategy Exploration Brief
# Phase A: Intraday Trading, No Overnight Holdings

**Date:** 2026-06-23  
**Worker:** scout-worker-fx-01  
**Run ID:** 2026-06-23-fx-phase-a-001  
**Issue:** #13  
**Phase:** A only (Phase B will follow separately)

---

## Research Objective

系统研究外汇日内量化策略的理论基础、策略家族、数据需求、交易成本、风险控制和验证方法，为后续回测实验建立充分证据支持的研究底座。

**核心约束：**
- 持仓时间：数分钟至数小时
- 平仓时间：日终前（通常在当日纽约收盘前）
- 不承担：隔夜 gap、swap/rollover cost、跨日事件风险

**本研究不提供交易建议，不承诺收益，不连接交易账户，不执行下单。**

---

## Strategy Families to Cover

1. **Trend / Momentum**
   - 日内趋势识别（moving averages, MACD, ADX）
   - 动量突破（breakout of recent high/low）
   - 时段动量（session momentum, open-to-close）

2. **Breakout**
   - Range breakout（support/resistance, pivot points）
   - Volatility breakout（Bollinger Bands, ATR）
   - News-driven breakout

3. **Mean Reversion**
   - RSI/Stochastic oversold/overbought
   - Bollinger Band reversion
   - Intraday pair mean reversion（highly correlated pairs）

4. **Statistical Arbitrage**
   - Cointegration-based pairs（EUR/USD vs GBP/USD, etc.）
   - Cross-pair triangular arbitrage
   - Quote vs trade price discrepancies（low latency）

5. **Order Flow / Microstructure**
   - Bid-ask spread dynamics
   - Order imbalance（volume at bid vs ask）
   - Quote stuffing detection and fade
   - Tick direction clustering

6. **Volatility**
   - Volatility regime detection（GARCH, realized vol）
   - Volatility expansion/contraction signals
   - VIX-FX correlation（risk-off flows）

7. **Event-Driven**
   - Scheduled news（NFP, CPI, central bank announcements）
   - Pre-announcement positioning and post-release fade
   - Economic surprise indices

---

## Market and Timing Coverage

### Currency Pairs
- **Majors:** EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD
- **Crosses:** EUR/GBP, EUR/JPY, GBP/JPY, AUD/JPY
- **Liquidity差异:** majors vs minors, developed vs EM

### Trading Sessions and Overlaps
- **Asian session** (Tokyo open ~00:00 UTC, Sydney ~22:00 UTC prior day)
- **London session** (open ~07:00 UTC)
- **New York session** (open ~12:00 UTC)
- **London-New York overlap** (~12:00–16:00 UTC): highest liquidity
- **Asian-London overlap** (~07:00–09:00 UTC)
- **Session transitions:** volatility spikes, direction reversals

### Session Characteristics
- Asian: lower volatility, range-bound, mean reversion favorable
- London: trend emergence, higher volume
- NY: USD pairs most active, overlap = most liquid
- Post-NY close: liquidity drops, spread widens

---

## Transaction Costs and Execution Realities

### Spread and Slippage
- Bid-ask spread（majors: ~0.1–0.5 pips typical, but widens during news, rollover, thin hours）
- Market impact（for retail/small prop: negligible; for larger size: measurable）
- Slippage on market orders vs limit orders

### Latency and Co-location
- HFT strategies require sub-millisecond latency and co-location
- Retail/API traders face 10–100+ ms round-trip
- Strategy feasibility vs latency budget

### Rollover and Funding
- 日内策略不持仓过夜，但需注意 rollover 时间窗口（通常 17:00 ET / 21:00 UTC）
- Rollover 前后流动性暂时下降，spread 可能扩大

### News Jumps
- Scheduled events（NFP, FOMC, ECB）: spread 瞬间扩大，stop-loss 可能大幅滑点
- Flash crashes and liquidity vacuums
- Strategy need: avoid holding through high-impact news, or explicitly model event risk

---

## Data Requirements and Labeling Pitfalls

### Data Granularity
- **Tick data:** bid/ask quotes, trade prints
- **Quote data vs trade data:** FX spot is OTC, 多数为 quote-driven; trade prints 可能稀疏或仅限某些 venues
- **Bar data** (1-min, 5-min, 15-min): easier to obtain, but hides microstructure
- **Bid-ask bounce:** using mid-price can overstate returns; must use realistic fill assumptions

### Labeling and Look-Ahead Bias
- Bar close price vs actual executable price at signal time
- Using future bar's OHLC to generate entry in current bar = look-ahead
- Repainting indicators（some platforms recalculate last bar）

### Survivorship and Selection Bias
- FX pairs generally do not "delist," but liquidity and spread can deteriorate
- Broker feed differences: some brokers' historical data may be cleaned or interpolated

### Data Snooping and Multiple Testing
- Testing many parameter sets and picking best = overfitting
- Walk-forward, out-of-sample, and cross-validation are essential

---

## Risk and Failure Modes

### Regime Shift
- 策略在某市场 regime 有效（如趋势期），在另一 regime 失效（如盘整期）
- Central bank policy change, crisis events (2008, 2020 COVID) alter correlations and volatility

### Crowding
- Popular intraday strategies (e.g., London breakout) may become crowded
- When many traders use same signals, alpha decays

### Capacity
- FX spot is deep, but intraday strategies with high turnover face cumulative costs
- Each round-trip costs 2× spread + slippage
- High-frequency strategies: capacity limited by own market impact

### Model Overfitting
- High Sharpe in backtest, poor live performance
- Parameter sensitivity: small change in MA period or threshold kills alpha

### Flash Events and Fat Tails
- CHF de-peg (2015-01-15), flash crashes
- Stop-loss does not guarantee exit at intended price

---

## Validation and Testing Protocol

### Backtest Realism
- Use bid/ask, not mid-price
- Model spread as function of time-of-day and volatility
- Include slippage estimate
- Walk-forward optimization
- Out-of-sample period at least 1 year

### Performance Metrics
- Sharpe ratio (annualized)
- Maximum drawdown
- Win rate and profit factor
- Exposure time (what % of day is capital deployed)
- Turnover and transaction cost ratio

### Robustness Checks
- Parameter stability
- Subperiod analysis (does strategy work in 2015–2017, 2018–2020, 2021–2023?)
- Cross-pair stability (does EUR/USD alpha generalize to GBP/USD?)
- Monte Carlo and bootstrap

---

## Source Quality Criteria

### Priority Tiers
1. **Tier 1:** Peer-reviewed papers, central bank research (BIS, ECB, Fed), academic journals
2. **Tier 2:** Industry research with disclosed methodology (broker research, prop trading blogs with code)
3. **Tier 3:** Open-source implementations with reproducible results (GitHub with backtests)
4. **Tier 4:** Tutorials, blog posts, forum discussions — use as leads, not as sole evidence

### Rejection Criteria
- No disclosed methodology
- Marketing material ("guaranteed 80% win rate")
- Cannot reproduce or verify
- Duplicate/plagiarized content
- SEO spam

### Multi-Source Corroboration
- Each core claim (e.g., "London breakout has positive expectancy") needs at least 2 independent sources
- If only 1 source, label as hypothesis/uncertain

---

## Evidence Saturation Criterion

Stop search when:
- **至少三轮不同查询扩展** after initial broad search
- Each new round yields **no new major strategy family**
- No new major risk category
- No new validation method family

Must still declare:
- Public data and time range limitations
- Strategies not covered (proprietary HFT, dark pool order flow)
- Uncertainty around true live performance vs backtest

---

## Tools and Resources

### Approved for This Run
- **Agent-Reach / Exa:** multi-platform public search and content discovery
- **Firecrawl:** public web scraping (single-page, batch, search) — no daily USD limit, but avoid waste
- **GitHub:** search for open-source strategies, backtesting frameworks, data pipelines
- **Public web:** papers (arXiv, SSRN), BIS, central banks, broker execution docs

### Prohibited
- Grok (currently 429, not usable)
- Private accounts or login-required resources
- Trading accounts, live or demo order execution
- Paid data subscriptions (unless already approved in RESOURCE_APPROVALS.yaml)

---

## Deliverables for Phase A

1. **Query matrix** — strategy × data source × query variations
2. **Source/decision ledger** — URL, date, type, credibility, keep/reject, reason, evidence/counter-evidence
3. **Strategy taxonomy** — family tree of intraday strategies with theoretical basis
4. **Failure landscape** — documented failure modes, overfitting, crowding, regime shifts
5. **Evidence map** — which claims are well-supported, which are hypotheses, which are contradicted
6. **Daily report** — summary for Phase A with sources, saturation judgment, known gaps
7. **Run summary** — timeline, tool usage, Firecrawl usage, rate limits encountered, next steps

All human-facing synthesis in Chinese; technical identifiers may remain in English.

---

## Execution Mode

- **Strictly serial, single-threaded**
- One strategy family at a time
- After each family, write checkpoint and release context (drop raw full-text, keep structured evidence only)
- No concurrent Claude sessions, no concurrent research roles, no concurrent Firecrawl batches
- If 429 encountered, stop that resource immediately and cool down
- No high-frequency retry loops

---

## Phase Boundary

- This run covers **Phase A only**
- Phase B (long-horizon dynamic position management) is **not started** in this run
- After Phase A completion:
  - Commit and push agent branch
  - Post Phase A progress comment on Issue #13
  - Keep claim active, set heartbeat to idle/waiting-for-phase-b
  - **Do not create final PR, do not transition to review, do not release claim**
  - **Do not start Phase B searches, scrapes, or synthesis**

---

**End of Exploration Brief**
