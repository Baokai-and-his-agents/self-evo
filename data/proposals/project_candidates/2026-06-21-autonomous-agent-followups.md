---
title: "Project Candidates: Autonomous Agent Follow-up Issues"
date: 2026-06-21
parent_issue: 7
type: project_candidates
status: proposed
---

# 项目候选：自主 Agent 生态系统后续 Issues

## 概述

Based on Issue #7 research, these child Issues represent concrete implementation work. **Priority reordered after business review**: Autonomous Scout vertical slice is now first, with generic infrastructure deferred until triggered by measured needs.

**DO NOT CREATE THESE GITHUB ISSUES YET**. This document proposes candidates for human review. After approval, create Issues in recommended order.

---

## 阶段 A：自主 Scout 垂直切片（主要业务目标）

### Issue #A.1：Scout 源注册和 Runner Wrapper

**类型**：Feature (Scout MVP)
**目标**：Enable bounded Scout execution with approved sources
**预计工期**：1 week

**范围**：
- Define approved sources in `rules/RESOURCE_APPROVALS.yaml`: GitHub Search/REST, HN API, arXiv API; Product Hunt only when resource approval and API access available
- Build Scout runner wrapper script (`scripts/scout_runner.py`)
- Runner launches Claude CLI worker with Scout task
- Runner enforces: max wall-clock time (configurable, e.g., 2 hours), max Claude process invocations (e.g., 10), max retries (e.g., 3)
- Runner captures: structured CLI output/usage where available, exit codes, wall-clock duration
- Unknown token/cost logged as "unknown" with explanation (hooks don't expose per-internal-call metrics)
- Manual invocation: user runs `python scripts/scout_runner.py --issue <N>`

**验收标准**：
- [ ] `rules/RESOURCE_APPROVALS.yaml` contains Scout source approvals (GitHub/HN/arXiv; Product Hunt gated on approval+API)
- [ ] Scout runner script exists and launches Claude CLI
- [ ] Runner enforces wall-clock timeout (terminates process on exceed)
- [ ] Runner enforces max invocations (stops after N Claude processes)
- [ ] Runner captures CLI output and writes run telemetry to gitignored `state/telemetry/<date>/<run-id>.jsonl`
- [ ] Runner writes partial results on termination (signal handler)
- [ ] Manual invocation documented in `rules/EXPLORATION_POLICY.md`

**前置依赖**：None

**风险**：Low (manual trigger, approved sources only, bounded execution)

**所需权限**：
- Network egress to approved sources (public read-only)
- Launch Claude CLI subprocess
- Write to `state/telemetry/` (gitignored)
- Kill subprocess on timeout

**推荐顺序**：A.1 (first)

---

### Issue #A.2：Cursor、去重和保留/拒绝账本

**类型**：Feature (Scout MVP)
**目标**：Enable idempotent resumption and evidence-backed filtering
**预计工期**：1 week

**范围**：
- Track last-seen cursor per source in gitignored `state/scout_cursor.json` (timestamp or item ID)
- Deduplication: skip already-processed items by URL/ID (exact match, gitignored cache)
- Keep/reject ledger: every item decision logged with reason in gitignored `data/exploration/raw/<date>-<source>-ledger.jsonl`
- Runner enforces: max sources scanned (e.g., 20), max items scanned per source (e.g., 100), max items kept (e.g., 50)
- Resume: on next run, load cursor and skip already-processed
- Commit to repo: only aggregated summary and decisions (not raw ledger or cursor state)

**验收标准**：
- [ ] Cursor tracking: Scout stores last-seen per source in `state/scout_cursor.json` (gitignored)
- [ ] Deduplication: repeated items skipped on resume (verified by test)
- [ ] Ledger: every item logged with keep/reject decision and reason in gitignored JSONL
- [ ] Runner enforces scan/keep limits (stops when exceeded)
- [ ] Resume: Scout resumes from cursor without re-scanning (verified by test)
- [ ] Only summary committed: gitignored state (cursor, ledger, cache) excluded from repo

**前置依赖**：Issue #A.1 (runner wrapper)

**风险**：Medium (cursor schema must handle diverse source formats, deduplication may miss semantic duplicates)

**所需权限**：
- Read/write `state/scout_cursor.json` (gitignored)
- Write ledger to `data/exploration/raw/` (gitignored JSONL)
- Commit summary to repo (tracked files only)

**推荐顺序**：A.2 (second)

---

### Issue #A.3：每日决策报告生成

**类型**：Feature (Scout MVP)
**目标**：Produce human-reviewable actionable output
**预计工期**：1 week

**范围**：
- Scout worker synthesizes scan results into daily decision report
- Report structure: reuse map (existing work survey), one experiment/skill/project candidate, evidence links to ledger
- Report stored in tracked `data/exploration/daily_reports/<date>-<topic>.md`
- Report frontmatter: date, issue, status, researcher
- Runner verifies report exists before completing run

**验收标准**：
- [ ] Daily report generated with required structure (reuse map, candidate, evidence)
- [ ] Report frontmatter includes: date, issue, status, researcher
- [ ] Report stored in tracked `data/exploration/daily_reports/`
- [ ] Evidence links reference ledger items (by ID or URL)
- [ ] Runner verifies report file exists before marking run complete
- [ ] Report is human-readable Markdown (no raw JSON dumps)

**前置依赖**：Issue #A.2 (ledger provides evidence)

**风险**：Low (report generation is synthesis task, Claude excels at this)

**所需权限**：
- Write to `data/exploration/daily_reports/` (tracked)
- Read ledger from `data/exploration/raw/` (gitignored)

**推荐顺序**：A.3 (third)

---

### Issue #A.4：人工审查标签工作流

**类型**：Feature (Scout MVP)
**目标**：Enable feedback loop for preference learning
**预计工期**：3 days

**范围**：
- User reviews daily report and adds labels: `relevant`, `irrelevant`, `deep-dive`, `pause`
- Labels stored in tracked `data/exploration/review_labels/<date>.yaml`
- Label schema: item_id, item_url, label, reason (optional)
- Future: preference learner analyzes label history to improve filtering
- For MVP: manual labeling only, no automated preference learning

**验收标准**：
- [ ] Label schema documented in `data/exploration/review_labels/README.md`
- [ ] Example label file created
- [ ] User workflow documented: review report → add labels to YAML file → commit
- [ ] Labels stored in tracked `data/exploration/review_labels/`
- [ ] No automated preference learning in MVP (future enhancement)

**前置依赖**：Issue #A.3 (report provides items to label)

**风险**：Low (manual workflow, no automation)

**所需权限**：
- Read daily reports
- Write to `data/exploration/review_labels/` (tracked)

**推荐顺序**：A.4 (fourth)

---

## 阶段 B：Scout 留出评估（Scout 运行后）

### Issue #B.1：Scout 留出集和质量指标

**类型**：Evaluation
**目标**：Measure Scout quality independently of training data
**预计工期**：1 week

**范围**：
- Create independent holdout set (NOT from repo's solved Issues to avoid answer leakage)
- Define Scout quality metrics: novelty (% new findings), relevance (% human-approved), evidence quality (links valid, claims supported), actionable conversion (% leading to experiments/skills), duplicate rate (% redundant)
- Define Builder quality metrics separately: test pass rate, acceptance criteria met
- Include human baseline: human performs same Scout task, compare time and quality

**验收标准**：
- [ ] Holdout set created with 10-20 independent Scout tasks
- [ ] Holdout tasks have no solutions in repo history (verified by git grep)
- [ ] Scout metrics defined and documented
- [ ] Builder metrics defined separately
- [ ] Human baseline protocol documented
- [ ] Holdout set stored in `data/benchmarks/scout_holdout/`

**前置依赖**：Scout vertical slice operational (Issues A.1-A.4)

**风险**：Medium (holdout set quality depends on task selection, metrics may need iteration)

**所需权限**：
- Read repo history (to verify no answer leakage)
- Write to `data/benchmarks/scout_holdout/` (tracked)

**触发条件**：Complete after Scout operational, before scaling

**推荐顺序**：B.1 (fifth)

---

### Issue #B.2：在留出集上运行 Scout 并测量

**类型**：Evaluation
**目标**：Quantify Scout success rate, cost, failure modes
**预计工期**：3 days

**范围**：
- Run Scout on holdout set (10-20 tasks)
- Measure: success rate (% tasks with valid output), novelty rate, relevance rate, actionable conversion, duplicate rate, cost per task, time per task
- Compare to human baseline: quality delta, time delta
- Document failure modes: rate limits, low-quality sources, irrelevant findings
- Produce evaluation report in `data/benchmarks/scout_eval_<date>.md`

**验收标准**：
- [ ] Scout run on all holdout tasks
- [ ] Metrics collected: success, novelty, relevance, actionable conversion, duplicates, cost, time
- [ ] Human baseline comparison included
- [ ] Failure modes categorized with examples
- [ ] Evaluation report documents findings and recommendations
- [ ] Decision: proceed to scaling, iterate prompts, or pivot approach

**前置依赖**：Issue #B.1 (holdout set)

**风险**：Low (read-only evaluation, no production changes)

**所需权限**：
- Run Scout (consumes budget)
- Write to `data/benchmarks/` (tracked)

**触发条件**：Complete after Scout operational, before scaling

**推荐顺序**：B.2 (sixth)

---

## 阶段 C：可靠性改进（观察到的失败触发）

### Issue #C.1：Scout 可靠性（恢复、去重）

**类型**：Enhancement
**目标**：Address observed failure modes from Scout operation
**预计工期**：1 week

**Scope** (conditional on observed failures):
- If crashes observed: improve resume robustness, verify cursor correctness
- If duplicates observed: add semantic deduplication (embedding similarity)
- If rate limits observed: add exponential backoff, respect rate limit headers
- If no-progress observed: detect and terminate stuck scans

**验收标准**：
- [ ] Failure modes from Scout operation documented
- [ ] Targeted fixes implemented (only for observed failures)
- [ ] Regression tests added for fixed failure modes
- [ ] Scout reliability metrics improve (measured on holdout or live runs)

**前置依赖**：Scout vertical slice operational, evaluation complete

**风险**：Low (targeted fixes, driven by evidence)

**所需权限**：Same as Scout vertical slice

**触发条件**：Complete ONLY if specific reliability failures observed in Scout operation or evaluation

**推荐顺序**：C.1 (seventh, conditional)

---

### Issue #C.2：内存索引（条件性）

**类型**：Enhancement
**目标**：Address retrieval performance only if measured as bottleneck
**预计工期**：2 weeks

**范围** (conditional on measured retrieval failures):
- Add OKF timestamps (`created`, `modified`) to memory frontmatter (do NOT add `accessed` or mutate on read)
- Track access/use in gitignored local index (`state/memory_access.db`) or append-only event log
- Experiment: SQLite FTS for keyword search, measure precision/recall
- Compare to user's active OpenViking adapter (if available)
- Conditional: add embeddings only if FTS precision insufficient
- Archive/restore protocol: manual only, reversible, requires cooldown proposal + human approval

**验收标准**：
- [ ] Retrieval bottleneck measured and documented (slow queries, low precision)
- [ ] OKF timestamps added to memories (created, modified only)
- [ ] Access tracking in gitignored index (Markdown files not mutated)
- [ ] SQLite FTS experiment complete with documented results
- [ ] OpenViking comparison (if available)
- [ ] Recommendation: adopt FTS, adopt embeddings, or keep file-only
- [ ] Archive/restore protocol documented (manual, reversible)

**前置依赖**：None (memory system independent)

**风险**：Low (additive only, Markdown remains canonical)

**所需权限**：
- Read/write `data/memory/` (frontmatter only)
- Create `state/memory_access.db` (gitignored)
- Create `state/memory_fts.db` for experiments (gitignored)

**触发条件**：Complete ONLY if retrieval failures measured (slow, imprecise, or recall issues)

**推荐顺序**：C.2 (eighth, conditional)

---

### Issue #C.3：多 Agent 协调（条件性）

**类型**：Enhancement
**目标**：Enable parallel Scout execution only if throughput bottleneck proven
**预计工期**：2-3 weeks

**范围** (conditional on measured throughput bottleneck):
- Parallel source scanners: one Scout worker per source
- Hierarchical aggregation: manager Scout combines per-source reports
- Worktree isolation: each Scout worker in separate git worktree
- Coordination: SQLite lease-based claiming (state/coordination.db, gitignored)
- Status aggregation: parent Issue tracks child Scout progress

**验收标准**：
- [ ] Throughput bottleneck documented: single Scout can't scan all sources in time budget
- [ ] Parallel Scouts implemented with worktree isolation
- [ ] Manager Scout aggregates per-source reports
- [ ] SQLite lease coordination prevents duplicate scans
- [ ] Integration test: 3 Scouts scan different sources in parallel, manager combines
- [ ] Coordination overhead measured and acceptable (<30% of total time)

**前置依赖**：Scout vertical slice operational, evaluation complete

**风险**：High (coordination complexity, worktree overhead, may not improve throughput)

**所需权限**：
- Create git worktrees
- Write to `state/coordination.db` (gitignored)
- Spawn multiple Scout processes

**触发条件**：Complete ONLY if Scout evaluation shows throughput bottleneck (can't scan all sources in budget)

**推荐顺序**：C.3 (ninth, conditional)

---

### Issue #C.4：外部可观测性对比（条件性）

**类型**：Infrastructure (Optional)
**目标**：Evaluate external platforms only if local telemetry insufficient
**预计工期**：1 week

**范围** (conditional on debugging pain):
- Compare Langfuse (self-hosted), Arize Phoenix, OpenLLMetry
- Integrate ONE platform (recommend Langfuse self-hosted Docker)
- Run Scout with external observability enabled
- Compare to local JSONL telemetry: features, overhead, debugging workflow
- Require explicit user approval before external data transmission

**验收标准**：
- [ ] Local telemetry bottleneck documented (insufficient for debugging)
- [ ] Comparison document covers 3+ tools with cost/feature matrix
- [ ] One tool integrated and tested
- [ ] Side-by-side comparison: local vs external for same Scout run
- [ ] Recommendation with justification
- [ ] User opt-in gate prevents automatic external transmission
- [ ] Self-hosted option validated (Docker Compose)

**前置依赖**：Scout vertical slice operational with local telemetry

**风险**：Medium (external dependency, data transmission requires approval)

**所需权限**：
- Network egress to external service (user approval required)
- Install observability SDK
- Write credentials to config (user-provided)

**触发条件**：Complete ONLY if local telemetry insufficient for debugging Scout failures

**推荐顺序**：C.4 (tenth, conditional)

---

### Issue #C.5：持久工作流引擎（条件性）

**类型**：Infrastructure (Advanced)
**目标**：Add checkpointing only if recovery pain measured
**预计工期**：2-3 weeks

**范围** (conditional on recovery pain):
- Evaluate Temporal, Restate, Inngest, or custom checkpointing
- Implement checkpointing at Scout phase boundaries (scan → synthesize → report)
- Recovery protocol: resume from checkpoint on crash or timeout
- Test: kill Scout mid-run, resume, verify no duplicate work

**验收标准**：
- [ ] Recovery pain documented: X% of Scout runs would benefit from checkpointing
- [ ] Workflow engine evaluated and one selected (or custom designed)
- [ ] Checkpointing implemented at phase boundaries
- [ ] Recovery tested: Scout resumes without re-doing completed work
- [ ] Cost overhead measured and acceptable
- [ ] Recommendation: when to use vs simple retry

**前置依赖**：Scout vertical slice operational, failure modes measured

**风险**：High (external dependency or significant custom code)

**所需权限**：
- Write checkpoint state to `state/checkpoints/` (gitignored)
- Network access to workflow engine (if cloud)
- Resume Scout execution from saved state

**触发条件**：Complete ONLY if Scout recovery pain measured as material (set threshold after observing failures, not in advance)

**推荐顺序**：C.5 (eleventh, conditional)

---

## 实施顺序摘要

**Phase A: Autonomous Scout Vertical Slice (MVP)** — 3-4 weeks
1. Issue #A.1: Scout source registry and runner wrapper
2. Issue #A.2: Cursor, deduplication, and keep/reject ledger
3. Issue #A.3: Daily decision report generation
4. Issue #A.4: Human review label workflow

**Phase B: Scout Evaluation** — 1-2 weeks (after Scout operational)
5. Issue #B.1: Scout holdout set and quality metrics
6. Issue #B.2: Run Scout against holdout and measure

**Phase C: Conditional Improvements** — triggered by measured failures
7. Issue #C.1: Scout reliability (only if specific failures observed)
8. Issue #C.2: Memory indexing (only if retrieval bottleneck measured)
9. Issue #C.3: Multi-agent coordination (only if throughput bottleneck proven)
10. Issue #C.4: External observability (only if local telemetry insufficient)
11. Issue #C.5: Durable workflow (only if recovery pain measured)

---

## 阶段 A（Scout MVP）的成功标准

**完成 Issues #A.1-A.4 后**：
- [ ] Scout produces daily decision report within budget
- [ ] Human review time <30 min per report
- [ ] Zero budget overruns (runner termination works)
- [ ] Scout resumes from interruption without duplicates
- [ ] User can label items for future preference learning

---

## 风险和缓解

### 风险：Scout 产生的不相关发现

**缓解**：Human review labels provide feedback. Iterate prompts and filtering logic. Measure quality with holdout (Phase B).

---

### 风险：每日 Scout 运行的高 token 成本

**缓解**：Runner enforces daily limits (sources, items, runtime). Partial results on termination. Tune limits based on observed costs.

---

### 风险：依赖外部资源的可用性问题

**缓解**：Cursor-based resumption. Respect rate limit headers. Exponential backoff. Future: cache and incremental refresh.

---

### 风险：Runner 强制执行不足

**缓解**：Test runner with dummy task before full Scout. Validate timeout, process termination, partial results.

---

## 业务逻辑修订

This document was reordered after business-logic review identified priority misalignment:

1. **Autonomous Scout vertical slice moved to Phase A (first priority)** — Was items 15+ / Phase 3. Now issues A.1-A.4.

2. **Generic infrastructure deferred to Phase C (conditional)** — Benchmark, telemetry, memory indexing, multi-agent, observability, durable workflow now triggered by measured needs, not built speculatively.

3. **Scout runner enforcement boundary clarified** — Cannot promise hard per-internal-LLM-call token cap. Runner enforces: wall-clock, process count, scan/keep limits, lifecycle.

4. **Benchmark answer leakage fixed** — Holdout set must be independent, not from repo's solved Issues (Issue B.1).

5. **Memory access tracking corrected** — Do NOT mutate Markdown on read. Use gitignored index or append-only event log (Issue C.2).

6. **Telemetry embedded in Scout runner** — Not detached infrastructure. Scout runner captures what CLI exposes; unknown stays unknown (Issue A.1).

7. **state/ files clarified as gitignored** — Growing runtime state (cursor, ledger, telemetry, coordination.db) stays gitignored. Only summaries/schemas committed.

8. **Removed fixed numeric thresholds** — No "1000 tasks/day", "read updates accessed timestamp", "fixed success rates". Measure locally, then set thresholds.

9. **Evaluation tracks separated** — Scout quality (novelty, relevance, evidence, actionable conversion, duplicate rate) vs Builder quality (tests, acceptance) vs human baseline (Issue B.1-B.2).

**业务的核心架构推荐**：
- Scout vertical slice as first priority (delivers user's stated goal)
- Runner-enforced limits (wall-clock, process count, scan/keep)
- Cursor-based idempotent resumption
- Human review gates (daily report workflow)
- Markdown canonical, database as gitignored index
- Evidence-based escalation (measure bottleneck before adding complexity)
- Primitives over frameworks (SQLite, git, Markdown)

---

**项目候选结束**

**下一步行动**：Human reviews proposed Issues, approves implementation order, creates GitHub Issues for Phase A.
