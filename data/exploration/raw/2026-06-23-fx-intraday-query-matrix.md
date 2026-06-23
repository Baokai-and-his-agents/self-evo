# FX Intraday Query Matrix
# Phase A: Day Trading, No Overnight

**Date:** 2026-06-23
**Worker:** scout-worker-fx-01
**Run ID:** 2026-06-23-fx-phase-a-001

---

## Strategy Families × Query Dimensions

每个策略家族将通过多个查询维度进行串行探索，每完成一个家族后释放上下文，仅保留结构化证据。

---

## 1. Trend / Momentum Intraday

### Query Set 1.1: Academic and Practitioner Research
- `"intraday momentum" "foreign exchange" (paper OR research OR study)`
- `"day trading momentum" forex (academic OR journal OR SSRN)`
- `"intraday trend following" FX (backtest OR empirical)`
- `"moving average crossover" intraday forex (performance OR Sharpe)`

### Query Set 1.2: Session-Specific Momentum
- `"London session momentum" forex strategy`
- `"New York open" momentum FX intraday`
- `"Asian session" range trading vs momentum`
- `"session overlap" momentum EUR/USD GBP/USD`

### Query Set 1.3: Implementation and Failure
- `"intraday momentum" forex (overfitting OR failure OR crowded)`
- `"moving average" day trading (slippage OR transaction cost)`
- `"momentum decay" FX intraday (regime shift OR drawdown)`

### Query Set 1.4: GitHub and Code
- `github.com "intraday momentum" forex python (backtest OR strategy)`
- `github.com "moving average" FX day trading (live OR paper trading)`
- `github.com "trend following" forex 1-minute OR 5-minute`

---

## 2. Breakout Strategies

### Query Set 2.1: Range and Level Breakout
- `"range breakout" intraday forex (support resistance OR pivot points)`
- `"London breakout" strategy EUR/USD GBP/USD`
- `"opening range breakout" FX (backtest OR performance)`

### Query Set 2.2: Volatility Breakout
- `"Bollinger Band breakout" intraday forex`
- `"ATR breakout" day trading FX (strategy OR indicator)`
- `"volatility expansion" forex intraday signal`

### Query Set 2.3: News-Driven Breakout
- `"news breakout" forex intraday (NFP OR CPI OR central bank)`
- `"event-driven" FX day trading (scheduled release OR economic calendar)`
- `"post-announcement drift" forex intraday`

### Query Set 2.4: Failure Modes
- `"false breakout" forex day trading (stop loss OR whipsaw)`
- `"breakout failure rate" FX intraday`
- `"fakeout" forex intraday strategy (risk OR drawdown)`

### Query Set 2.5: GitHub
- `github.com "breakout strategy" forex intraday python`
- `github.com "range breakout" FX day trading backtest`

---

## 3. Mean Reversion

### Query Set 3.1: Indicator-Based Reversion
- `"RSI mean reversion" forex intraday (overbought oversold)`
- `"Bollinger Band reversion" FX day trading`
- `"stochastic oscillator" forex intraday mean reversion`

### Query Set 3.2: Pair and Cross-Pair Reversion
- `"pair trading" forex intraday (EUR/USD GBP/USD OR correlation)`
- `"mean reversion" currency pairs intraday (cointegration OR spread)`
- `"cross-pair arbitrage" FX intraday`

### Query Set 3.3: Session and Regime
- `"Asian session" mean reversion forex (range bound OR consolidation)`
- `"overnight gap" forex intraday reversion (open-to-close)`
- `"regime switching" mean reversion FX intraday`

### Query Set 3.4: Failure and Crowding
- `"mean reversion failure" forex (trending market OR regime shift)`
- `"RSI strategy" forex intraday (overfitting OR parameter sensitivity)`

### Query Set 3.5: GitHub
- `github.com "mean reversion" forex python intraday`
- `github.com "RSI strategy" FX day trading backtest`

---

## 4. Statistical Arbitrage

### Query Set 4.1: Cointegration and Pairs
- `"cointegration" forex pairs intraday (EUR/USD GBP/USD OR spread trading)`
- `"statistical arbitrage" FX intraday (pairs OR portfolio)`
- `"cross-currency arbitrage" intraday (triangular OR synthetic)`

### Query Set 4.2: Latency and Execution
- `"latency arbitrage" forex (tick data OR quote vs trade)`
- `"triangular arbitrage" FX (feasibility OR transaction cost)`
- `"statistical arbitrage" forex (HFT OR high frequency OR co-location)`

### Query Set 4.3: Failure and Capacity
- `"cointegration breakdown" forex (regime shift OR correlation collapse)`
- `"arbitrage capacity" FX intraday (market impact OR slippage)`

### Query Set 4.4: GitHub
- `github.com "statistical arbitrage" forex python (pairs OR cointegration)`
- `github.com "triangular arbitrage" FX (live OR backtest)`

---

## 5. Order Flow / Microstructure

### Query Set 5.1: Bid-Ask and Order Imbalance
- `"order flow" forex intraday (bid-ask OR imbalance)`
- `"order book" FX trading (depth OR liquidity OR microstructure)`
- `"volume at bid vs ask" forex intraday signal`

### Query Set 5.2: Tick and Quote Dynamics
- `"tick direction" forex (clustering OR autocorrelation)`
- `"quote stuffing" FX (detection OR fade strategy)`
- `"bid-ask bounce" forex (bias OR correction)`

### Query Set 5.3: Latency and HFT
- `"high frequency trading" forex microstructure (order flow OR adverse selection)`
- `"low latency" forex trading (co-location OR execution speed)`

### Query Set 5.4: Data and Failure
- `"order flow data" forex (availability OR vendor OR API)`
- `"microstructure noise" FX intraday (signal extraction OR filtering)`

### Query Set 5.5: GitHub and Papers
- `github.com "order flow" forex python (tick data OR L2)`
- `"market microstructure" forex (paper OR research OR BIS)`

---

## 6. Volatility-Based Strategies

### Query Set 6.1: Volatility Regime
- `"volatility regime" forex intraday (GARCH OR realized volatility)`
- `"volatility clustering" FX day trading (signal OR forecast)`
- `"volatility breakout vs reversion" forex intraday`

### Query Set 6.2: Volatility Expansion/Contraction
- `"ATR expansion" forex intraday strategy`
- `"volatility contraction" FX (squeeze OR breakout setup)`
- `"Bollinger Band squeeze" forex day trading`

### Query Set 6.3: Risk-Off Flows
- `"VIX" forex correlation (risk-off OR safe haven OR USD JPY CHF)`
- `"volatility spike" forex intraday (flight to quality OR risk aversion)`

### Query Set 6.4: Failure
- `"volatility strategy" forex intraday (whipsaw OR false signal)`
- `"GARCH forecast" forex (accuracy OR regime change)`

### Query Set 6.5: GitHub
- `github.com "volatility strategy" forex python (GARCH OR realized vol)`
- `github.com "ATR" forex intraday backtest`

---

## 7. Event-Driven Strategies

### Query Set 7.1: Scheduled Macro Releases
- `"NFP" forex intraday strategy (non-farm payroll OR employment)`
- `"CPI" forex day trading (inflation release OR reaction)`
- `"central bank announcement" FX intraday (FOMC OR ECB OR BOJ)`

### Query Set 7.2: Pre/Post-Event Positioning
- `"pre-announcement positioning" forex (bias OR drift)`
- `"post-release fade" forex intraday (reversal OR overreaction)`
- `"economic surprise" forex (Citi surprise index OR forecast error)`

### Query Set 7.3: Execution Risk
- `"news trading" forex (spread widening OR slippage OR liquidity)`
- `"volatility spike" scheduled event forex (stop loss OR gap)`

### Query Set 7.4: Failure
- `"news trading" forex intraday (failure OR unpredictable OR random walk)`
- `"event-driven" FX (overfitting OR selection bias)`

### Query Set 7.5: GitHub and Data
- `github.com "news trading" forex python (event calendar OR API)`
- `"economic calendar API" forex real-time (ForexFactory OR Bloomberg)`

---

## 8. Cross-Cutting: Transaction Costs and Execution

### Query Set 8.1: Spread and Slippage
- `"bid-ask spread" forex intraday (time-of-day OR volatility OR liquidity)`
- `"slippage" forex day trading (market order OR limit order OR execution)`
- `"transaction cost" FX intraday (broker comparison OR rebate)`

### Query Set 8.2: Latency
- `"latency" forex trading (API OR VPS OR co-location)`
- `"execution speed" FX intraday (millisecond OR sub-second)`

### Query Set 8.3: Rollover and Funding
- `"rollover time" forex (5pm ET OR 21:00 UTC OR swap point)`
- `"funding cost" FX intraday (avoided OR timing OR liquidity drop)`

### Query Set 8.4: Market Impact
- `"market impact" forex (order size OR slippage model)`
- `"liquidity" FX intraday (depth OR spread OR venue)`

---

## 9. Cross-Cutting: Data and Backtesting

### Query Set 9.1: Data Sources and Quality
- `"tick data" forex (vendor OR free OR Dukascopy OR FXCM OR TrueFX)`
- `"historical forex data" intraday (bid-ask OR quote vs trade)`
- `"FX data quality" (cleaning OR interpolation OR survivorship)`

### Query Set 9.2: Backtest Pitfalls
- `"look-ahead bias" forex backtest (bar close OR repainting)`
- `"overfitting" forex intraday (parameter optimization OR walk-forward)`
- `"data snooping" trading strategy (multiple testing OR p-hacking)`

### Query Set 9.3: Validation Frameworks
- `"walk-forward" forex backtest (optimization OR out-of-sample)`
- `"cross-validation" trading strategy (time series OR Monte Carlo)`
- `"backtest realism" forex (transaction cost OR bid-ask OR slippage)`

### Query Set 9.4: GitHub Tools
- `github.com "backtest" forex python (vectorbt OR backtrader OR zipline)`
- `github.com "forex data" pipeline (tick OR OHLC OR API)`

---

## 10. Cross-Cutting: Risk and Failure Literature

### Query Set 10.1: Overfitting and Parameter Sensitivity
- `"overfitting" forex strategy (robustness OR parameter stability)`
- `"parameter sensitivity" forex intraday (optimization OR curve fitting)`

### Query Set 10.2: Regime Shift
- `"regime shift" forex (central bank policy OR crisis OR volatility change)`
- `"structural break" forex strategy (performance decay OR alpha decay)`

### Query Set 10.3: Crowding
- `"crowded trade" forex intraday (alpha decay OR capacity)`
- `"strategy crowding" FX (front-running OR adverse selection)`

### Query Set 10.4: Flash Events
- `"flash crash" forex (CHF de-peg OR liquidity vacuum)`
- `"fat tail" forex intraday (stop loss failure OR gap risk)`

### Query Set 10.5: Broker and Venue Differences
- `"broker comparison" forex intraday (spread OR execution OR rebate)`
- `"ECN vs market maker" forex (execution quality OR slippage)`

---

## 11. Institutional and Academic Literature

### Query Set 11.1: Central Banks and BIS
- `site:bis.org "foreign exchange" (microstructure OR intraday OR trading)`
- `site:ecb.europa.eu forex (volatility OR liquidity OR market structure)`
- `site:federalreserve.gov "FX market" (intraday OR execution)`

### Query Set 11.2: Academic Journals
- `"Journal of Finance" OR "Journal of Financial Economics" forex intraday`
- `"Review of Financial Studies" currency trading (momentum OR reversion)`
- `SSRN forex intraday (momentum OR breakout OR mean reversion)`

### Query Set 11.3: Broker Research
- `"CME" OR "LMAX" OR "EBS" forex market structure (liquidity OR execution)`
- `broker research forex intraday (execution quality OR slippage OR spread)`

---

## Search Execution Plan

### Round 1: Broad Discovery (Strategy Families 1–7)
- Execute Query Sets 1.1–7.5 in serial order
- Use Agent-Reach / Exa for initial wide search
- Use Firecrawl for promising URLs that need full-text extraction
- Use GitHub search for code implementations
- Record all sources in decision ledger with keep/reject and reasoning

### Round 2: Cross-Cutting Deep Dive (8–10)
- Transaction costs, data quality, backtesting, risk and failure modes
- Focus on sources that provide methodological guidance and empirical evidence

### Round 3: Institutional and Academic (11)
- Central bank papers, BIS research, academic journals
- Prioritize peer-reviewed and official publications

### Round 4: Expansion and Validation
- Based on gaps found in Rounds 1–3, design additional queries
- Target: no new major strategy family, risk category, or validation method
- If Round 4 yields significant new categories, continue to Round 5
- Stop after at least 3 consecutive rounds with no major new discoveries

---

## Evidence Recording

For each query:
- **Query string** and **tool used** (Agent-Reach, Firecrawl, GitHub, direct web search)
- **Results returned** (count)
- **Sources examined** (URLs)
- **Keep decisions** (URL, reason, evidence extracted)
- **Reject decisions** (URL, reason: duplicate, no methodology, marketing, irrelevant)
- **Gaps identified** (missing strategy, missing risk, missing validation method)

After each strategy family or query set, write a checkpoint summary and drop raw full-text from context.

---

## Saturation Criterion

Research is saturated when:
1. At least **3 rounds of expansion** beyond initial broad search
2. Each of the last 3 rounds yields **no new major strategy family**
3. No new major **risk category** (beyond overfitting, regime shift, crowding, flash events, capacity, data quality)
4. No new major **validation method** (beyond walk-forward, cross-validation, transaction cost modeling, parameter sensitivity, out-of-sample)

Even after saturation, must acknowledge:
- Public sources and time range limitations
- Proprietary strategies (dark pool, HFT order flow) not accessible
- True live performance vs backtest gap remains uncertain

---

**End of Query Matrix**
