# FX Data Sources Survey

**Date:** 2026-06-23
**Worker:** fx-backtest-worker-01
**Purpose:** Identify public, license-compliant FX OHLC data sources for Issue #18

## Requirements

- Public access, no login required
- License allows research/backtesting use
- OHLC format (daily or intraday)
- Major pairs: EURUSD, GBPUSD, USDJPY
- Multi-year historical coverage (ideally 10+ years)
- Clear timezone, bid/ask/mid specification
- Stable download mechanism

## Candidate Sources

### 1. Dukascopy

**URL:** https://www.dukascopy.com/swiss/english/marketwatch/historical/
**License:** XML datafeed requires registration, approval, and web attribution (https://www.dukascopy.com/plugins/cont.php?ref_id=1273)
**Format:** Tick data and aggregated OHLC via Historical Data Export tool
**Pairs:** Major FX pairs available
**Coverage:** Multi-year historical data
**Access:** Free Historical Data Export tool, CSV download
**Status:** LICENSE UNCERTAIN for offline research backtest
- XML datafeed license is for "non-commercial, temporary use" with web display and attribution
- Historical Data Export tool terms not explicitly stated for research use
- Requires manual review to determine if offline backtesting is permitted
- Terms state "may not be used to construct a database" and prohibit redistribution
**Decision:** Not using without explicit human approval

### 2. Stooq

**URL:** https://stooq.com/
**License:** Not yet verified
**Format:** CSV OHLC
**Pairs:** Multiple FX pairs
**Coverage:** Multi-year history
**Access:** Web download
**Status:** NEEDS VERIFICATION

### 3. FRED (Federal Reserve Economic Data)

**URL:** https://fred.stlouisfed.org/
**License:** Public domain US government data
**Format:** Daily exchange rates
**Pairs:** Major pairs available
**Coverage:** Decades of history
**Access:** CSV download, API available
**Limitations:** May be end-of-day rates, not OHLC; not tick/intrabar data
**Status:** LICENSE APPROVED for research, but may lack OHLC structure

### 4. Yahoo Finance (via yfinance)

**URL:** https://finance.yahoo.com/
**License:** Unclear for programmatic bulk download
**Format:** OHLC
**Pairs:** FX pairs as currency pairs (e.g., EURUSD=X)
**Coverage:** Multi-year
**Access:** Python library `yfinance` (external dependency)
**Status:** BLOCKED - requires external installation, license uncertain for bulk backtest

### 5. OANDA

**URL:** https://www.oanda.com/
**License:** May require account
**Format:** API access
**Status:** BLOCKED - likely requires authentication

### 6. AlphaVantage

**URL:** https://www.alphavantage.co/
**License:** Free tier with API key
**Format:** JSON API
**Status:** BLOCKED - requires API key registration, rate limits

## Initial Decision: Fallback to Synthetic Fixture

Given the uncertainty around public FX data licenses and stable download mechanisms, the MVP will:

1. **Implement a complete CSV data adapter** that can accept any OHLC CSV format
2. **Create deterministic synthetic fixtures** for testing the full pipeline
3. **Document the data source investigation** and what blocked real data access
4. **Provide a clear path** for the human to supply real data if available

This approach ensures:
- MVP is complete and testable
- No licensing violations
- No false claims of "backtest completed" when data is uncertain
- Clear documentation of what is needed

## Synthetic Fixture Specification

For testing, we'll generate:
- **Pair:** EURUSD (synthetic)
- **Frequency:** Daily
- **Period:** 2020-01-01 to 2022-12-31 (3 years, ~750 bars)
- **OHLC:** Deterministic price pattern with:
  - Trend phases (for Donchian breakouts)
  - Consolidation phases (for stop sequences)
  - ATR variation
  - No gaps, no missing bars
- **Purpose:** Validate full pipeline, test A/B/E/G under controlled conditions

## Real Data Path

If the human can provide or approve a specific data source:
1. Add data manifest with URL, license reference, SHA256 hash
2. Implement download script (only if license permits automation)
3. Document timezone, bid/ask/mid semantics
4. Store in `state/download-cache/fx-backtest/`
5. Keep out of Git (per Issue #18 requirement)

## Next Steps

1. Implement CSV data loader (agnostic to source)
2. Generate synthetic fixture
3. Complete backtest with fixture
4. Document real data blocking issue clearly in results
5. If time and approved resources permit, investigate Dukascopy or Stooq license terms via web research
