---
title: "Project Candidates: Autonomous Agent Follow-up Issues"
date: 2026-06-21
parent_issue: 7
type: project_candidates
status: proposed
---

# Project Candidates: Child Issues for Autonomous Agent Ecosystem

## Overview

Based on Issue #7 research, these child Issues represent concrete implementation work. Each is scoped for incremental value with clear acceptance criteria.

**DO NOT CREATE THESE GITHUB ISSUES YET**. This document proposes candidates for human review. After approval, create Issues in recommended order.

---

## Proposed Child Issues

### Issue #7.1: Self-Evo-Native Benchmark + Local Telemetry

**Type**: Infrastructure + Evaluation
**Goal**: Establish measurable performance baseline using project-native tasks with local-only observability
**Estimated Effort**: 1-2 weeks

**Scope**:
- Create benchmark suite from self-evo issue/PR history (10-20 representative tasks)
- Extract ground truth: committed solutions, verification commands, acceptance criteria
- Build JSONL telemetry logger (traces, spans, tool calls, token counts, costs)
- Optional: Export to OpenTelemetry-compatible format for future tooling
- Run baseline: measure current agent success rate, cost per task, time per task
- Document results in `data/benchmarks/baseline-YYYY-MM-DD.md`
- Optional: Compare to SWE-bench Verified subset (informational only, not acceptance gate)

**Acceptance Criteria**:
- [ ] Benchmark suite defined with 10-20 self-evo tasks (issue resolution, PR creation, testing)
- [ ] JSONL telemetry captures: timestamps, tokens, tool calls, costs, outcomes
- [ ] Baseline run records the intervention rate without imposing a preselected success target
- [ ] Results document shows: success count, median cost, median time, failure modes
- [ ] Telemetry schema documented for future analysis
- [ ] No external API credentials or paid services required

**Technical Dependencies**: None

**Risk**: Low (read-only evaluation, no production changes)

**Permissions Required**:
- Read git history
- Create `data/benchmarks/` directory
- Write telemetry JSONL to `state/telemetry/`

**Decision Trigger**: Complete before other issues to establish value floor and measure improvements

**Recommended Order**: 1

---

### Issue #7.2: Hard Budget and Termination Controls

**Type**: Feature (Safety)
**Goal**: Prevent runaway costs and infinite loops with enforceable limits
**Estimated Effort**: 1 week

**Scope**:
- Create `state/budget.db` (SQLite) for token/cost/time tracking per Issue
- Implement configurable caps: max tokens per Issue, max wall-clock time, max tool calls
- Add budget check before LLM calls (halt with partial results if exceeded)
- Add termination detection: repeated errors, no progress, tool call loops
- Human override protocol via GitHub Issue comment (`@agent approve-budget +50k`)
- Log budget exhaustion events with context for debugging

**Acceptance Criteria**:
- [ ] Budget database tracks tokens, cost, time, tool calls per Issue
- [ ] Hard stop at configured cap (agent halts, writes partial results, exits cleanly)
- [ ] Termination detector catches: 5+ consecutive errors, 10+ identical tool calls, 60min no file writes
- [ ] Human override command increases budget mid-run
- [ ] Budget status visible in agent status updates
- [ ] Integration tests verify enforcement (mock agent hitting limits)

**Technical Dependencies**: Issue #7.1 (telemetry informs budget design)

**Risk**: Medium (may halt legitimate long tasks; requires human override availability)

**Permissions Required**:
- Create/write `state/budget.db`
- Read GitHub Issue comments for override commands
- Terminate agent process on budget exceeded

**Decision Trigger**: Complete before autonomous deployment

**Recommended Order**: 2

---

### Issue #7.3: OKF Timestamps + SQLite FTS Experiments

**Type**: Enhancement
**Goal**: Enable time-aware retrieval and investigate full-text search scaling
**Estimated Effort**: 1 week

**Scope**:
- Add `created`, `modified`, `accessed` timestamps to memory frontmatter (OKF v0.1 spec)
- Implement access tracking (update `accessed` on memory Read)
- Build forgetting score function (time-decay + access-frequency)
- Experiment: Load memories into SQLite with FTS5 extension for full-text search
- Compare retrieval approaches: file-glob vs SQLite FTS vs hybrid
- Document findings: performance at 100/500/1000 memories, query latency, recall quality
- No automatic archival (manual-only with restore protocol)

**Acceptance Criteria**:
- [ ] All existing memories migrated to OKF format with timestamps
- [ ] Memory Read operations update `accessed` timestamp
- [ ] Forgetting score calculation implemented and tested
- [ ] SQLite FTS experiment completes with documented results (query time, recall)
- [ ] Hybrid retrieval recommendation based on measured performance
- [ ] Archive/restore commands documented (manual trigger only)

**Technical Dependencies**: None

**Risk**: Low (additive only, reversible archival, experimental results inform decisions)

**Permissions Required**:
- Read/write `data/memory/`
- Create `state/memory_fts.db` for experiments
- Create `data/memory/archive/` for manual archival

**Decision Trigger**: Complete before memory count exceeds 200 items

**Recommended Order**: 3

---

### Issue #7.4: Approval-Gated External Observability Comparison

**Type**: Infrastructure (Optional)
**Goal**: Compare external observability tools (Langfuse, Braintrust, LangSmith) with clear opt-in
**Estimated Effort**: 1 week

**Scope**:
- Document comparison criteria: cost, self-hosted option, API compatibility, session replay, alerting
- Implement integration for ONE tool (recommend Langfuse self-hosted Docker)
- Run same benchmark from #7.1 with external observability enabled
- Compare to local JSONL telemetry: feature gaps, overhead, debugging workflow
- Document trade-offs and recommendation
- Require explicit user approval before external data transmission
- No API credentials assumed (user must provide if cloud option chosen)

**Acceptance Criteria**:
- [ ] Comparison document covers 3+ tools with cost/feature matrix
- [ ] One tool integrated and tested against #7.1 benchmark
- [ ] Observability data includes: traces, spans, costs, LLM I/O, tool calls
- [ ] Side-by-side comparison: local JSONL vs external tool for same benchmark run
- [ ] Recommendation documented with justification
- [ ] User opt-in gate prevents automatic external transmission
- [ ] Self-hosted option validated (Docker Compose or equivalent)

**Technical Dependencies**: Issue #7.1 (benchmark), Issue #7.2 (budget enforcement)

**Risk**: Medium (external data transmission requires approval, adds dependency)

**Permissions Required**:
- Network egress to external service (user approval required)
- Install observability SDK dependencies
- Write credentials to `.env` or config file (user-provided)

**Decision Trigger**: Complete only if debugging becomes bottleneck or multi-agent coordination planned

**Recommended Order**: 4 (optional, defer if local telemetry sufficient)

---

### Issue #7.5: Multi-Agent Coordination (Gated by Bottleneck Evidence)

**Type**: Feature (Advanced)
**Goal**: Enable parallel Issue execution only after single-agent throughput proven insufficient
**Estimated Effort**: 2-3 weeks

**Scope**:
- **GATE**: Complete only if benchmark shows single-agent can't meet throughput needs
- Design parent/child Issue tracking protocol
- Implement agent coordination: spawn child agents, aggregate results, detect conflicts
- Add file-level locking or git worktree isolation for parallel work
- Build status aggregation: parent Issue tracks child agent progress
- Test with 2-3 parallel agents on independent Issues

**Acceptance Criteria**:
- [ ] Bottleneck evidence documented: single-agent can't scale to target throughput
- [ ] Parent/child Issue protocol defined and implemented
- [ ] Agent spawning works: parent creates child agents with isolated context
- [ ] Conflict detection prevents parallel writes to same files
- [ ] Status aggregation shows per-agent progress in parent Issue
- [ ] Integration test: 3 agents complete independent Issues in parallel
- [ ] Coordination overhead measured (latency, cost) and documented

**Technical Dependencies**: Issue #7.1 (benchmark), Issue #7.2 (budget per agent)

**Risk**: High (adds complexity, requires conflict resolution, may not improve throughput)

**Permissions Required**:
- Spawn multiple agent processes
- Create git worktrees for isolation (if chosen)
- Write agent status to shared state database

**Decision Trigger**: Complete ONLY if benchmark proves single-agent insufficient

**Recommended Order**: 5 (defer until measured bottleneck)

---

### Issue #7.6: Durable Workflow Engine (Gated by Recovery Pain)

**Type**: Infrastructure (Advanced)
**Goal**: Add task recovery and checkpointing only after demonstrated need
**Estimated Effort**: 2-3 weeks

**Scope**:
- **GATE**: Complete only if agent failures cause significant rework (measured in #7.1/#7.2)
- Evaluate workflow engines: Temporal Cloud, Restate, Inngest, custom checkpointing
- Implement checkpointing: save state at phase boundaries (research → plan → implement)
- Build recovery protocol: resume from last checkpoint on crash or budget exhaustion
- Test recovery: kill agent mid-task, resume, verify no duplicate work
- Document workflow patterns for multi-step Issues

**Acceptance Criteria**:
- [ ] Recovery pain documented: X% of benchmark failures would benefit from checkpointing
- [ ] Workflow engine evaluated and one selected (or custom checkpointing designed)
- [ ] Checkpointing implemented at phase boundaries
- [ ] Recovery tested: agent resumes from checkpoint without re-doing completed work
- [ ] Cost overhead measured (workflow engine fees, checkpoint storage)
- [ ] Recommendation: when to use vs simple retry

**Technical Dependencies**: Issue #7.1 (baseline failure modes), Issue #7.2 (termination events)

**Risk**: High (adds external dependency or significant custom code, may not justify overhead)

**Permissions Required**:
- Write checkpoint state to `state/checkpoints/`
- Network access to workflow engine (if cloud option chosen)
- Resume agent execution from saved state

**Decision Trigger**: Complete ONLY if measured recovery pain is material enough to justify the added operational dependency; set the threshold after the baseline rather than in advance

**Recommended Order**: 6 (defer until recovery need proven)

---

## Implementation Order

**Phase 1: Measurement and Safety (MVP)**
1. Issue #7.1: Benchmark + Local Telemetry (establish baseline)
2. Issue #7.2: Budget + Termination Controls (prevent runaway)
3. Issue #7.3: OKF Timestamps + FTS Experiments (retrieval scaling)

**Phase 2: Observability and Scaling (Conditional)**
4. Issue #7.4: External Observability (optional, if debugging bottleneck)
5. Issue #7.5: Multi-Agent Coordination (only if throughput bottleneck proven)
6. Issue #7.6: Durable Workflows (only if recovery pain measured)

---

## Success Criteria for Phase 1 (MVP)

**After completing Issues #7.1-7.3**:
- [ ] Baseline success rate measured on self-evo tasks (no fixed target)
- [ ] Median cost per Issue documented (no fixed cap promised)
- [ ] Zero budget overruns (hard caps enforced)
- [ ] Memory retrieval scales to 200+ items with acceptable latency
- [ ] Failure modes categorized: budget exhaustion, termination, task complexity
- [ ] Decision data available for Phase 2 gates

---

## Risks and Mitigations

### Risk: Benchmark may show current approach insufficient

**Mitigation**: Issue #7.1 provides evidence for pivot decisions. May need supervised mode or architecture changes before autonomy.

---

### Risk: Budget caps halt legitimate long tasks

**Mitigation**: Issue #7.2 includes human override protocol. Budget analysis from #7.1 informs reasonable defaults.

---

### Risk: External observability adds cost and complexity

**Mitigation**: Issue #7.4 gated by opt-in and compared to local telemetry. Self-hosted option removes recurring cost.

---

### Risk: Multi-agent coordination may add more overhead than value

**Mitigation**: Issue #7.5 deferred until bottleneck proven in #7.1. May never implement if single-agent sufficient.

---

### Risk: Workflow engine overhead may exceed recovery value

**Mitigation**: Issue #7.6 deferred until failure analysis in #7.1/#7.2 shows recovery need. Simple retry may be sufficient.

---

**End of Project Candidates**

**Next Action**: Human reviews proposed Issues, approves implementation order, creates GitHub Issues.
