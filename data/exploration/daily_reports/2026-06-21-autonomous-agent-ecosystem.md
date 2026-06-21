---
title: "Daily Report: Autonomous Agent Ecosystem Research"
date: 2026-06-21
issue: 7
type: decision_report
researcher: scout-worker-01
status: complete
---

# Daily Report: Issue #7 — Autonomous Agent Ecosystem

## Executive Summary

Research into autonomous agent ecosystems reveals a maturing but hazardous landscape. Production patterns exist: durable execution platforms (Temporal 35k★), observability infrastructure (Langfuse 29k★), and GitHub-native workflows. Yet agent pilot failures are widely reported (runaway costs, infinite loops), and benchmark scores can mislead on real-world tasks.

**Core Finding**: Self-evo's file-first, human-reviewed approach aligns with cautious production patterns. The path forward is **Autonomous Scout vertical slice first**, with cost controls and bounded execution.

---

## Research Counts (With Overlap Caveat)

**Search queries executed**: 113 total across all roles
- Autonomous loops & GitHub: 35 searches, 15 deep fetches, 19 retained sources
- Multi-agent coordination: 29 searches, 23 fetched documents
- Memory & context: 27 successful deep fetches across 14 system categories
- Observability & safety: 24 repository/API inspection calls, 85 repositories surfaced, 16 selected
- Critic research: 47 repository/API inspection calls, 30 archived frameworks in sample, plus 8 papers and 4 coordination repos

**Unique systems evaluated**: 48 retained after deduplication
- 7 durable execution platforms
- 12 active multi-agent frameworks (30 archived frameworks identified in critic sample)
- 8 memory systems
- 5 observability platforms
- 6 evaluation benchmarks
- 6 safety/security tools
- 4 GitHub integration patterns

**Overlap caveat**: Same repo found via multiple queries. GitHub search returns forks and integrations. Deduplication applied; counts represent unique systems analyzed, not raw search hits.

**Deep analysis**: 10 systems with architecture-level review (Temporal, LangGraph, Mem0, ENGRAM, OpenHands, Langfuse, CrewAI, OKF, Restate, SWE-bench).

**Critic validation**: Identified 30 archived frameworks (biased search: focused on failure indicators, not representative sample). Zero public issues for "agent cost" or "coordination failure" suggests evidence gap.

---

## One Primary Route: Autonomous Scout Vertical Slice

**Approach**: Deliver the project's stated primary goal first — a proactive scouting system that explores, filters, and produces daily decision-oriented reports.

**Scout Vertical Slice Components**:

1. **Approved source registry** (`rules/RESOURCE_APPROVALS.yaml`)
   - GitHub Search / REST API
   - Hacker News API
   - arXiv API
   - Product Hunt API (public read)

2. **Manual trigger with scheduler placeholder**
   - User runs Scout worker locally
   - `rules/EXPLORATION_POLICY.md` defines approved sources, daily limits
   - Later: add scheduled invocation

3. **Incremental cursor and deduplication**
   - Track last-seen timestamps per source
   - Skip already-processed items (by URL/ID)
   - Store cursor in local gitignored `state/scout_cursor.json`

4. **Keep/reject ledger with evidence**
   - Every item: kept (with reason) or rejected (with reason)
   - Store decisions in `data/exploration/raw/<date>-<source>-ledger.jsonl`
   - Human-reviewable provenance

5. **Bounded high-token research**
   - Scout runner enforces: max wall-clock time, max sources scanned, max items kept, max Claude invocations
   - No promise of per-internal-LLM-call hard token cap (hooks can't see that)
   - Unknown token/cost goes to telemetry as "unknown" with explanation

6. **Daily decision report**
   - One reuse map (existing work survey)
   - One experiment/skill/project candidate
   - Evidence links to ledger

7. **Human review labels**
   - User reviews daily report, marks items: `relevant`, `irrelevant`, `deep-dive`, `pause`
   - Labels stored in `data/exploration/review_labels/<date>.yaml`
   - Future: preference learner summarizes patterns

**Scout Runner/Wrapper** (execution boundary):
- Local script that launches Claude CLI worker with Scout task
- Captures structured CLI output/usage where available
- Enforces: max runtime (wall clock), max Claude process invocations, max retries, scan/keep limits
- Detects: tool call repetition, no-progress, lifecycle violations
- Writes: partial results on termination, cursor/ledger to gitignored state
- Commits to repo: only summary, decisions, schemas (not growing runtime state)

**Timeline**: 3-4 weeks to working Scout vertical slice

**Tradeoffs**:
- ✅ Delivers user's primary stated goal (proactive exploration)
- ✅ Tests high-token workflow with real business value
- ✅ Embeds telemetry and budget controls into real work (not detached infrastructure)
- ✅ Produces reviewable daily output for preference learning
- ⚠️  High-token cost per run (mitigated by daily limits and runner enforcement)
- ⚠️  Requires approved external sources (mitigated by resource approval workflow)

**Success criteria** (measure after Scout operational):
- Scout produces non-empty daily report within budget
- Human review time <30 min per report
- Relevance improves over 4 weeks (measured by human labels)
- Zero runaway costs (runner termination works)

---

## Secondary Routes (After Scout Proven)

### Route B: Scout Evaluation + Holdout Set

**Trigger**: After Scout vertical slice operational, before scaling

**Scope**:
- Create holdout evaluation set (NOT from repo's solved Issues)
- Define Scout quality metrics: novelty, relevance, evidence quality, actionable conversion, duplicate rate
- Define Builder quality metrics separately (tests, acceptance)
- Include human baseline (time, quality) for comparison

**Why deferred**: Can't evaluate Scout before Scout exists

---

### Route C: Observed-Failure Reliability

**Trigger**: After Scout shows specific failure modes (crashes, duplicates, budget overruns)

**Scope**:
- Add resume from cursor (idempotent restart)
- Improve deduplication (cross-source, semantic similarity)
- Tune runner limits based on observed failures

**Why deferred**: Don't know which reliability features are needed until Scout runs

---

### Route D: Memory Indexing (Conditional)

**Trigger**: ONLY if measured retrieval failures occur (slow queries, low precision)

**Scope**:
- Add OKF timestamps (`created`, `modified`) to frontmatter
- Track access/use in gitignored local index or append-only event log (NOT by mutating Markdown)
- Experiment: SQLite FTS for keyword search
- Compare user's active OpenViking adapter
- Conditional: embeddings only if FTS insufficient

**Why deferred**: No evidence of retrieval bottleneck yet. Markdown remains canonical.

---

### Route E: Multi-Agent (Conditional)

**Trigger**: ONLY if single-agent Scout shows throughput bottleneck (queue >5 sources, can't finish daily scan)

**Scope**:
- Parallel source scanners (one per source)
- Hierarchical aggregation (manager combines reports)
- Worktree isolation for file conflicts

**Why deferred**: No evidence single-agent insufficient. Multi-agent adds coordination complexity.

---

### Route F: External Observability / Durable Workflow (Conditional)

**Trigger**: ONLY if local debugging painful OR recovery overhead high

**Scope**:
- Evaluate Langfuse (self-hosted) vs local JSONL telemetry
- Evaluate Temporal/Restate for checkpointing (if recovery pain measured)

**Why deferred**: Local telemetry and simple retry may suffice. Add external deps only when justified.

---

## Recommended Implementation Order

### Phase A: Autonomous Scout Vertical Slice (Week 1-4)

**Issue A.1**: Scout source registry and manual trigger
- Define approved sources in `rules/RESOURCE_APPROVALS.yaml`
- Build Scout runner wrapper (launch, enforce limits, capture output)
- Manual invocation: user runs `python scripts/scout_runner.py`

**Issue A.2**: Cursor, ledger, and bounded scan
- Track last-seen per source (gitignored cursor state)
- Deduplication by URL/ID
- Keep/reject ledger with evidence
- Runner enforces: max runtime, max sources, max items scanned/kept, max retries

**Issue A.3**: Daily decision report generation
- Scout worker produces: reuse map, one experiment/skill/project candidate, evidence links
- Commit summary and decisions (not raw ledger or cursor state)

**Issue A.4**: Human review label workflow
- User reviews report, adds labels (relevant/irrelevant/deep-dive/pause)
- Labels stored in `data/exploration/review_labels/<date>.yaml`

### Phase B: Scout Evaluation (Week 5-6, after Scout operational)

**Issue B.1**: Holdout set and Scout quality metrics
- Create independent holdout tasks (NOT from repo history to avoid answer leakage)
- Define Scout metrics: novelty, relevance, evidence, actionable conversion, duplicate rate
- Separate Builder metrics: test pass, acceptance
- Human baseline for comparison

**Issue B.2**: Measure Scout against holdout
- Run Scout on holdout set
- Compare to human baseline
- Document success rate, cost, failure modes

### Phase C: Conditional Improvements (triggered by observed failures)

**Issue C.1**: Resume and idempotency (if crashes observed)
**Issue C.2**: Improved deduplication (if duplicates observed)
**Issue C.3**: Memory indexing (if retrieval slow/imprecise)
**Issue C.4**: Multi-agent (if throughput bottleneck proven)
**Issue C.5**: External observability (if debugging painful)
**Issue C.6**: Durable workflow (if recovery overhead high)

---

## One Immediate Experiment

**Experiment**: Prototype Scout runner enforcement without full Scout implementation

**Hypothesis**: Runner can enforce wall-clock, process count, and lifecycle limits before building full Scout

**Method**:
1. Write minimal Scout runner wrapper (launch Claude CLI, enforce timeout)
2. Test with dummy task (e.g., "scan 5 HN items")
3. Verify: timeout works, partial results written, clean exit

**Timeline**: 1 day

**Cost**: <$5

**Success criteria**:
- Runner terminates on timeout
- Partial results preserved
- No zombie processes

**Learning outcome**: Validates enforcement approach before investing in full Scout

---

## One Skill to Learn

**Skill**: Designing idempotent exploratory agents with cursor-based resumption

**Why**: Scout will be interrupted (budget, timeout, crashes). Must resume without re-scanning.

**Learning path**:
1. Study cursor patterns (Stripe API, GitHub pagination, database offset/limit)
2. Design cursor schema for multi-source Scout (per-source last-seen timestamp/ID)
3. Implement idempotency: same input + same cursor = same output
4. Test: interrupt, resume, verify no duplicates

**Timeline**: 4 hours

**Outcome**: Understand cursor-based resumption for Scout reliability

---

## Human Decisions Requested

### Decision 1: Scout Vertical Slice Priority

**Question**: Approve Scout as first implementation priority?

**Options**:
1. **Yes, Scout first** — Delivers user's stated goal, tests high-token workflow (Recommended)
2. No, benchmark/telemetry infrastructure first — Measure before building
3. No, memory indexing first — Address retrieval before exploration

**Recommendation**: Yes, Scout first. Embed telemetry/budget into Scout runner (not detached infrastructure).

---

### Decision 2: Scout Source Approval

**Question**: Approve initial Scout sources (GitHub/HN/arXiv/Product Hunt public read)?

**Risk**: Network egress, rate limits, potential IP blocking

**Recommendation**: Approve for public read-only. No API keys required for basic access.

---

### Decision 3: Scout Budget

**Question**: Approve daily Scout budget?

**Options**:
- Option A: 2 hours wall-clock, 20 sources scanned, 50 items kept, 10 Claude invocations
- Option B: 4 hours wall-clock, 40 sources scanned, 100 items kept, 20 Claude invocations
- Option C: User-defined limits in `rules/EXPLORATION_POLICY.md`

**Recommendation**: Option A for MVP (tighter limits, iterate based on observed needs)

---

### Decision 4: Deferred Work Gates

**Question**: Confirm conditional triggers for deferred work?

**Triggers** (measure after Scout operational):
- [ ] Memory indexing: ONLY if retrieval failures measured
- [ ] Multi-agent: ONLY if throughput bottleneck proven
- [ ] External observability: ONLY if local debugging painful
- [ ] Durable workflow: ONLY if recovery pain measured

**Recommendation**: Confirm gates. Do not build speculative infrastructure.

---

## Risks and Mitigations

### Risk 1: High-token cost per Scout run

**Mitigation**: Runner enforces daily limits (sources, items, runtime). Partial results on termination.

---

### Risk 2: Scout produces low-quality reports

**Mitigation**: Human review labels provide feedback. Iterate prompts and filtering logic.

---

### Risk 3: Rate limits from external sources

**Mitigation**: Cursor-based resumption. Respect rate limit headers. Exponential backoff.

---

### Risk 4: Runner enforcement insufficient

**Mitigation**: Prototype runner with dummy task first (1 day). Validate enforcement before full Scout.

---

## Success Metrics for Scout MVP

**Quality** (measure after Scout operational):
- [ ] Daily report produced (non-empty)
- [ ] Human review time <30 min
- [ ] Relevance improves over 4 weeks (via human labels)

**Cost** (measure and enforce):
- [ ] Zero budget overruns (runner termination works)
- [ ] Cost per run: to be measured and optimized

**Reliability** (measure after Scout operational):
- [ ] Completion rate: to be measured
- [ ] Resume from interruption: to be implemented and tested

---

## What Self-Evo Will Do Differently (Survival Strategy)

**Why cautious approach matters**:
1. Agent pilot failures widely reported (runaway costs, infinite loops)
2. Fully autonomous agents with no review gates risk quality death spiral
3. Framework lock-in creates dependency risk

**Self-evo Scout strategy**:
1. **Human-review gates**: Daily report reviewed before acting on recommendations
2. **Cost controls built-in**: Runner enforces limits, no promise of unachievable per-internal-call caps
3. **File-first**: Ledger, cursor, telemetry in gitignored state; only summaries committed
4. **Primitive-based**: SQLite, git, standard tools. Not dependent on framework survival.
5. **Evidence-driven**: Deliver Scout first, measure bottlenecks, add complexity only when justified
6. **Incremental autonomy**: Manual trigger → scheduled invocation → preference learning

**Core insight**: Scout is not a generic agent framework. It's a bounded exploration workflow with human review.

---

## Next Actions (Post-Decision)

1. **Human reviews this report** → approves Scout priority, sources, budget
2. **Prototype Scout runner** → 1 day, validates enforcement
3. **Implement Scout vertical slice** → 3-4 weeks (Issues A.1-A.4)
4. **Operate Scout for 4 weeks** → collect human labels, measure quality/cost
5. **Evaluate Scout** → holdout set, metrics (Issue B.1-B.2)
6. **Conditional improvements** → based on measured failures (Phase C)

---

## Corrections from Business Review

This section documents changes made after business-logic review identified priority misalignment:

1. **Scout vertical slice moved to first priority** — Was deferred to item 15 / Phase 3. Now Phase A.

2. **Runner enforcement boundary clarified** — Cannot promise hard per-internal-LLM-call token cap (hooks don't see that). Runner enforces: wall-clock, process count, scan/keep limits, lifecycle.

3. **Benchmark answer leakage fixed** — Holdout set must be independent, not from repo's solved Issues.

4. **Memory access tracking corrected** — Do NOT mutate Markdown on read. Use gitignored index or append-only event log.

5. **Telemetry embedded in Scout** — Not detached infrastructure. Scout runner captures what CLI exposes; unknown stays unknown.

6. **state/budget.db not tracking state** — Growing runtime state (ledger, cursor, telemetry) stays gitignored. Only summaries/schemas committed.

7. **Removed proactive scouting deferral language** — Scout IS the proactive scouting. It's now first priority, not deferred.

8. **Removed fixed numeric thresholds** — No ">1000 tasks/day", "read updates accessed", etc. Measure locally, then set thresholds.

**High-confidence recommendations preserved**:
- Scout vertical slice as primary business goal
- Human review gates (daily report workflow)
- Primitives over frameworks (SQLite, git, Markdown)
- Runner-enforced limits (wall-clock, process count, scan/keep)
- Cursor-based idempotent resumption
- Markdown canonical, database as index
- Evidence-based escalation (measure bottleneck before adding complexity)

---

**End of Daily Report**
