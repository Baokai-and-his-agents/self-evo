# HistData 2005 Pilot Validation Correction

**Date**: 2026-06-23 (Evening Review)
**Reviewer**: Human oversight (comment #4780178611)
**Original Status**: ✅ HISTDATA_PILOT_VALIDATED (INCORRECT)
**Corrected Status**: ⚠️ **PILOT_REQUIRES_VALIDATION**

---

## Executive Summary

The original validation report contained **critical errors** that invalidated the approval for full download. The 2005 pilot data has serious data quality issues that must be investigated before proceeding.

**Decision**: ❌ **Full download NOT approved** - validation must be completed first

---

## Critical Errors in Original Validation

### 1. ❌ Weekend Data Misrepresented

**Original Claim**:
> "315 trading days" with "125% coverage" suggesting "good coverage"

**Reality**:
- **315 unique calendar dates** includes **50 Sundays + 7 Saturdays** (57 weekend dates)
- This is NOT 315 trading days
- Actual weekdays: ~258 days
- **15,924 M1 bars on weekends** (exact count to be verified)

**Impact**: The dataset includes substantial weekend activity that should not exist in a standard 24/5 FX market.

### 2. ❌ Suspicious Price Movement Not Flagged

**Bar**: 2005-01-03 01:53 EST
```
Open:  1.355500
High:  1.355500
Low:   1.346500  (90 pip drop)
Close: 1.346600
```

**Original Assessment**: "unusual but possible during news events"

**Required Action**: Must cross-check with ECB reference rate and second source before accepting as valid market data.

### 3. ❌ License Status Misrepresented

**Original Claim**:
> "✅ 无使用限制条款" (No usage restrictions)
> "无禁止自动化下载的条款" (No prohibition on automated downloads)

**Reality**:
- No Terms of Use page found (404)
- Absence of explicit prohibition ≠ explicit permission
- Status should remain: **DATA_TERMS_UNCLEAR**

**Correct Statement**: "No explicit restrictions found, but no explicit permissions either. Terms status unclear."

### 4. ❌ Daily Bar Boundary Not Defined

**Original Claim**: Uses "calendar day (00:00-23:59 EST)"

**Problem**:
- Standard FX trading day: Sunday 17:00 EST → Friday 17:00 EST
- Calendar day aggregation would create invalid bars on:
  - Sunday 00:00-23:59 (should be part of Monday session)
  - Saturday 00:00-23:59 (should not exist)

**Required**: Define proper FX session boundaries before aggregation.

---

## Data Quality Issues Found

### Issue 1: Weekend Bars

**Evidence**:
```
Unique dates by weekday:
     50 Friday
     52 Monday
      7 Saturday  ⚠️
     50 Sunday    ⚠️
     52 Thursday
     52 Tuesday
     52 Wednesday
Total: 315 dates
```

**Weekend dates sample**:
- 2005-01-08 (Saturday)
- 2005-01-09 (Sunday)
- 2005-01-15 (Saturday)
- 2005-01-16 (Sunday)
... (total 57 weekend dates)

**Questions**:
1. Are these thin/sporadic quotes or full trading activity?
2. Are they broker-specific off-market quotes?
3. Should they be filtered out before daily aggregation?
4. Do they represent valid FX activity (Middle East markets)?

**Required Investigation**:
- Count bars per weekend date
- Compare bar density: weekend vs weekday
- Check if weekend bars cluster around session rollover (Sunday 17:00 EST)

### Issue 2: Suspicious Price Jump

**Bar**: 2005-01-03 01:53 EST
- Price drop: ~90 pips in 1 minute (1.3555 → 1.3465)
- Magnitude: ~0.66% move

**Context**:
- Date: Monday, January 3, 2005
- Time: 01:53 EST (06:53 UTC) - Asian session
- Previous bar: 01:48 EST at 1.3555

**Required Verification**:
1. Download ECB reference rate for 2005-01-03
2. Check if ECB shows similar move
3. Search for news events on 2005-01-03
4. Compare with second data source (if available)

**Possible Explanations**:
- ✅ Real market event (news, flash crash)
- ❌ Data error (feed glitch, bad tick)
- ⚠️ Bid vs Mid price artifact

### Issue 3: Cache File Corruption

**Found**:
- `EURUSD_M1_2005.zip` - 31 KB (corrupt or incomplete)
- `HISTDATA_COM_MT_EURUSD_M1_2005.zip` - 2.4 MB (valid)

**SHA256**:
- Corrupt: `d602d9ea1cb46518f1582a2f5934bdf62ac725009b93897d4f3c270342825698`
- Valid: `77afb311bc09f845ee418033eb44fe81177a365fd806d77c9ca903554a1a3fab`

**Action Required**: Delete corrupt file, keep only valid ZIP.

---

## Corrected Status Assessment

### What Was Validated ✅

1. ✅ File integrity: Valid ZIP downloads and extracts
2. ✅ CSV format: Matches MetaTrader specification
3. ✅ OHLC fields: All present with 6 decimal precision
4. ✅ Timezone: EST (UTC-5) no DST documented
5. ✅ SHA256: Valid file hash recorded

### What Requires Validation ⚠️

1. ⚠️ **Weekend data**: 57 weekend dates, ~15,924 bars - nature unclear
2. ⚠️ **Price sanity**: 90 pip jump on 2005-01-03 01:53 - not verified
3. ⚠️ **Daily bar boundary**: Calendar day vs FX session - undefined
4. ⚠️ **ECB cross-check**: Not performed
5. ⚠️ **Gap analysis**: Incomplete (only >60s reported)
6. ⚠️ **Terms status**: Should be DATA_TERMS_UNCLEAR, not "approved"

---

## Required Actions Before Full Download

### Priority 1: Weekend Data Analysis

**Task**: Understand weekend bars
- [ ] Count bars per weekend date
- [ ] Compare weekend vs weekday bar density
- [ ] Check if Sunday bars cluster around 17:00 EST (market open)
- [ ] Determine if weekend bars should be filtered

**Acceptance Criteria**:
- Document bar count for each weekend date
- Explain source of weekend data (thin quotes, broker-specific, valid activity)
- Define filtering strategy (if needed)

### Priority 2: ECB Cross-Check

**Task**: Verify 2005-01-03 price jump
- [ ] Download ECB USD.EUR reference rate for 2005-01-03
- [ ] Invert to EUR/USD
- [ ] Compare with HistData close on 2005-01-03
- [ ] Check if ECB shows similar movement

**Acceptance Criteria**:
- ECB rate fetched and converted
- Price correlation calculated
- 90 pip jump explained or flagged as data error

### Priority 3: Define Daily Bar Boundary

**Task**: Clarify FX trading day definition
- [ ] Research standard FX session boundaries
- [ ] Decide: Calendar day vs FX session day
- [ ] Document rationale (must align with PR #19 if it has prior baseline)
- [ ] Implement aggregation logic

**Acceptance Criteria**:
- Clear definition: "Trading day = [start time] to [end time] EST"
- Weekend handling strategy defined
- Compatible with PR #19 strategy requirements

### Priority 4: Cache Cleanup

**Task**: Remove corrupt file
- [ ] Delete `EURUSD_M1_2005.zip` (31 KB)
- [ ] Keep `HISTDATA_COM_MT_EURUSD_M1_2005.zip` (2.4 MB)
- [ ] Update DOWNLOAD_METADATA.md

### Priority 5: Terms Status Correction

**Task**: Update license assessment
- [ ] Change status from "approved" to DATA_TERMS_UNCLEAR
- [ ] Clarify: No explicit restrictions found, but no explicit permissions
- [ ] Note: 404 on Terms of Use page

---

## Revised Recommendation

**Status**: ⚠️ **PILOT_REQUIRES_VALIDATION**

**Do NOT proceed with**:
- ❌ Full 2005-2025 download
- ❌ Paid FTP purchase ($27 USD)
- ❌ Implementation of HistData adapter
- ❌ Production use of 2005 data

**DO complete**:
- ✅ Weekend data analysis
- ✅ ECB cross-check on 2005-01-03
- ✅ Daily bar boundary definition
- ✅ Cache cleanup
- ✅ Terms status correction

**THEN**:
- If validation passes → Approve limited download (2005-2010 sample)
- If issues found → Seek alternative data source

---

## Comparison with Original Report

| Aspect | Original | Corrected |
|--------|----------|-----------|
| Status | ✅ VALIDATED | ⚠️ REQUIRES_VALIDATION |
| Trading Days | "315" | "~258 weekdays + 57 weekend dates" |
| Weekend Bars | Not mentioned | "~15,924 bars on Sat/Sun" |
| Price Jump | "Unusual but possible" | "Requires ECB verification" |
| Terms Status | "No restrictions" | "DATA_TERMS_UNCLEAR" |
| Daily Boundary | "Calendar day" | "Undefined - must clarify" |
| Recommendation | "✅ Approve full download" | "❌ Block until validation" |

---

## Updated Phase 1 Status

**Phase 1**: ⚠️ **PARTIALLY COMPLETE**

**Completed**:
- ✅ Dukascopy terms investigation (DATA_TERMS_UNCLEAR)
- ✅ ECB evaluation (cross-check only, not main source)
- ✅ HistData discovery and pilot download
- ✅ OHLC data sources matrix (framework)

**In Progress**:
- ⏳ HistData pilot validation (blocked on weekend analysis)
- ⏳ ECB cross-check implementation
- ⏳ Daily bar boundary definition

**Blocked**:
- ❌ Full download approval
- ❌ Phase 2-8 (data processing, backtest)

---

## Next Steps

1. **Complete validation tasks** (Priority 1-5 above)
2. **Generate validation report** with findings
3. **Decision gate**:
   - If pass → Approve limited download (sample years)
   - If fail → Evaluate alternative sources (OANDA v20, Alpha Vantage)
4. **Update PR #21** with corrected status

---

## Lessons Learned

### Validation Mistakes to Avoid

1. ❌ "315 days" without checking weekday composition
2. ❌ Accepting "no restrictions found" as explicit permission
3. ❌ Approving full download based on partial validation
4. ❌ Not performing ECB cross-check before approval
5. ❌ Using "calendar day" without justifying FX session boundary

### Correct Validation Process

1. ✅ Count unique dates **by weekday** (not just total)
2. ✅ Cross-check suspicious movements with second source
3. ✅ Distinguish "no explicit prohibition" from "explicit permission"
4. ✅ Define domain-specific boundaries (FX session, not calendar day)
5. ✅ Block downstream work until validation complete

---

## Related Documents

- Original (incorrect) validation: `histdata-2005-pilot-validation.md`
- HistData investigation: `histdata-investigation.md`
- PR #21 comment: #4780178611
- Issue: #20

---

**Status**: ⚠️ PILOT_REQUIRES_VALIDATION
**Blocker**: Weekend data analysis, ECB cross-check, daily boundary definition
**Next Action**: Complete Priority 1-3 validation tasks
**Updated**: 2026-06-23 (Evening)
