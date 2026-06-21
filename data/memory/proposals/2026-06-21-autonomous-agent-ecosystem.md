---
title: "Memory Proposals: Autonomous Agent Ecosystem Conclusions"
date: 2026-06-21
issue: 7
type: memory_proposals
status: pending_human_review
note: "These are candidate memories for merging into hot memory. Each includes provenance and confidence. Human reviews before promotion."
---

# Memory Proposals: Durable Conclusions from Issue #7

These are durable conclusions worth merging into hot memory (`data/memory/hot/`). Each conclusion includes provenance (source evidence) and confidence rating. Only promote after human review.

**Confidence Scale**:
- **High**: Multiple primary sources, benchmarks, production evidence
- **Medium**: Single strong source or consistent secondary evidence
- **Low**: Inference or weakly supported claim

---

## Proposed Memory 1: File-First Memory Is Validated by Standards

**Slug**: `okf-validates-file-first-memory`
**Type**: reference
**Confidence**: High

**Conclusion**: Self-evo's Markdown+YAML memory format is validated by Google's Open Knowledge Format (OKF) v0.1 (June 2026), a vendor-neutral standard for LLM-readable memory. Self-evo should add `created`/`modified`/`accessed` timestamps for OKF compliance and to enable forgetting mechanisms.

**Provenance**:
- OKF v0.1 specification (June 2026)
- Research file: `data/exploration/raw/2026-06-21-memory-context.md`
- Cross-referenced with ENGRAM, Mem0 architectures

**Why durable**: Standards alignment is long-lived. File-first approach won't be obsoleted; OKF formalizes the pattern self-evo already uses.

**How to apply**: Keep Markdown/YAML as canonical. Add timestamps. Don't migrate to database (use database as index only).

---

## Proposed Memory 2: Agent Framework Abandonment Is Endemic

**Slug**: `agent-framework-abandonment-risk`
**Type**: reference
**Confidence**: High

**Conclusion**: The critic-focused sample found multiple archived agent frameworks, including Microsoft TaskWeaver and ACE Framework. Because the sample was intentionally biased toward failures, it does not establish an ecosystem-wide abandonment rate or a single cause. Self-evo should still favor durable primitives (SQLite, git, Markdown) where they meet the need, reducing dependency and migration risk.

**Provenance**:
- Critic research: `data/exploration/raw/2026-06-21-critic-failure-landscape.md`
- 30 archived frameworks identified via GitHub search (biased critic sample, not exhaustive survey)
- Pattern analysis of abandonment causes

**Why durable**: Framework churn is structural, not transient. Survival strategy (primitive-based, not framework-based) applies indefinitely.

**How to apply**: Reject framework adoption. Use SQLite, git, Markdown. Infrastructure (Temporal, Langfuse) is long-lived; agent frameworks are not.

---

## Proposed Memory 3: Benchmark Scores Mislead — Measure Baseline First

**Slug**: `benchmark-real-world-gap`
**Type**: reference
**Confidence**: High

**Conclusion**: Agent benchmarks show substantial benchmark-reality gaps. AgentBench paper reports 37.5% average success (Claude Opus 3) but drops to 0% on post-training Kaggle tasks. τ-bench paper shows GPT-4o <50% success, pass^8 <25% on realistic retail tasks. SWE-bench results show best autonomous agent: 43% (with test feedback), median 25-35%. Self-evo must measure single-agent baseline before assuming multi-agent value.

**Provenance**:
- AgentBench paper (arXiv 2308.03688)
- τ-bench paper (arXiv 2406.12045)
- SWE-bench results (source-specific, various papers/leaderboards)
- Critic research: `data/exploration/raw/2026-06-21-critic-failure-landscape.md`

**Why durable**: Benchmark-reality gap is fundamental to agent evaluation. The lesson (measure baseline before scaling) applies to all future agent work.

**How to apply**: Create self-evo-native benchmark for Issue resolution workflow (primary). Optionally use SWE-bench Verified as coding benchmark (secondary). Measure single-agent baseline before multi-agent complexity.

---

## Proposed Memory 4: Cost Controls Are the Primary Failure Mode

**Slug**: `cost-controls-prevent-pilot-failure`
**Type**: project
**Confidence**: Medium-High

**Conclusion**: Runaway costs and infinite loops are primary causes of agent pilot failures. Critic found zero public GitHub issues for "agent framework cost" despite thousands of users (suggests proprietary suppression or widespread silent failures). Self-evo must build token budget enforcement, three-layer termination defense, and real-time cost monitoring BEFORE autonomous loops.

**Provenance**:
- Multi-agent coordination research: `data/exploration/raw/2026-06-21-multi-agent-coordination.md`
- Critic research: zero public cost issues (absence evidence)
- Cost control patterns from multiple frameworks

**Why durable**: Cost discipline is a permanent constraint for LLM agents. Token budgets and termination limits apply to all autonomous work.

**How to apply**: Implement budget enforcement (per-Issue, per-day caps), three-layer termination (depth + timeout + budget), structured local telemetry for cost tracking. Human approval above threshold.

---

## Proposed Memory 5: Hierarchical Beats Swarm for Multi-Agent

**Slug**: `hierarchical-multi-agent-preferred`
**Type**: reference
**Confidence**: Medium

**Conclusion**: Production multi-agent deployments predominantly use hierarchical/sequential patterns (manager assigns tasks) over swarm (autonomous claiming). Swarm adds coordination complexity (race conditions, deadlocks) without proven benefit. Self-evo should defer multi-agent entirely until single-agent bottleneck proven, then use hierarchical, not swarm.

**Provenance**:
- Multi-agent coordination research: `data/exploration/raw/2026-06-21-multi-agent-coordination.md`
- Autonomous loops research: `data/exploration/raw/2026-06-21-autonomous-loops-github.md`
- Qualitative pattern analysis across frameworks

**Why durable**: Coordination pattern tradeoffs are architectural constants. Hierarchical simplicity vs swarm flexibility is a stable tradeoff.

**How to apply**: Defer multi-agent until bottleneck. When needed, use hierarchical (manager-worker). Reject swarm for MVP.

---

## Proposed Memory 6: Durable Execution Is Available But Defer Until Scale

**Slug**: `durable-execution-defer-until-scale`
**Type**: reference
**Confidence**: High

**Conclusion**: Durable execution platforms (Temporal 35k★, Restate 8k★, Inngest 5k★) provide automatic retry and fault tolerance via event sourcing. Critical distinction: checkpointing (LangGraph) requires manual recovery; durable execution is automatic. But these add significant complexity (event-sourcing mindset). Self-evo's SQLite task queue is sufficient for current scale; escalate only when measured bottlenecks justify it.

**Provenance**:
- Autonomous loops research: `data/exploration/raw/2026-06-21-autonomous-loops-github.md`
- Multi-agent coordination research: workflow engine comparison
- Temporal/Restate architecture docs

**Why durable**: The escalation principle (SQLite → durable execution at scale) is a stable architecture decision. Platforms may evolve, but the threshold logic persists.

**How to apply**: Use SQLite task queue for MVP. Learn durable execution mental model (event sourcing). Escalate to Temporal/Restate only when measured bottlenecks justify it (cross-host coordination required, recovery pain demonstrated, or throughput/reliability limits proven).

---

## Proposed Memory 7: Hybrid Memory Architecture Scales File-First

**Slug**: `hybrid-memory-file-plus-index`
**Type**: reference
**Confidence**: High

**Conclusion**: File-first memory (Markdown) scaling depends on retrieval performance (linear scan degrades with size). Production pattern: Markdown files as source of truth + SQLite FTS (keyword) + embeddings (semantic) as rebuildable index. ENGRAM reports 77.55% LoCoMo benchmark (source-specific), Mem0 reports 91.6% (source-specific). Self-evo should consider SQLite FTS as memory count grows, with specific threshold determined by observed retrieval performance rather than fixed count.

**Provenance**:
- Memory research: `data/exploration/raw/2026-06-21-memory-context.md`
- ENGRAM paper (arXiv 2511.12960), Mem0 benchmarks (source-specific scores)
- Cognee, Graphiti architecture patterns

**Why durable**: The scaling threshold (file-only → file+index) is a stable architecture decision. The hybrid pattern (files authoritative, index rebuildable) is production-proven.

**How to apply**: Keep Markdown canonical. Add SQLite FTS index (rebuildable from files) when retrieval performance degrades. Add embeddings if keyword search proves insufficient.

---

## Proposed Memory 8: Forgetting Improves Retrieval Accuracy

**Slug**: `forgetting-improves-memory`
**Type**: reference
**Confidence**: Low

**Conclusion**: Unbounded memory accumulation may degrade retrieval. Research identifies substantial accuracy gains from selective forgetting (time-decay + access-frequency + quality gating), with one source reporting 13% → 39% improvement (unverified; source-specific). Self-evo should evaluate reversible forgetting against a baseline and adopt it only if local retrieval quality improves.

**Provenance**:
- Memory research: `data/exploration/raw/2026-06-21-memory-context.md`
- Forgetting problem analysis (one source reports 13% → 39% accuracy improvement; unverified, source-specific)
- Multiple systems implement forgetting (Mem0, Graphiti, CrewAI)

**Why durable**: The forgetting principle (selective memory beats accumulation) is supported by cognitive science and multiple agent systems, but gains are source-specific and require local validation. The experiment design is stable.

**How to apply**: Design reversible experiment: Add `accessed` timestamp, access counter. Score memories (time-decay + access-frequency). Archive low-scoring (reversible). Measure retrieval precision/recall before and after. Adopt forgetting only if local evidence shows improvement.

---

## Proposed Memory 9: Observability Is Production-Ready, Build It Early

**Slug**: `observability-build-early`
**Type**: feedback
**Confidence**: High

**Conclusion**: Production observability platforms exist (Langfuse 29k★, Arize Phoenix 10k★, OpenLLMetry 7k★, AgentOps 5k★). OpenTelemetry LLM semantic conventions are standardized. Self-evo should implement local structured telemetry first (SQLite-based session/token tracking), then evaluate external platforms (Langfuse, OpenLLMetry) only after approval and comparison. Debugging non-deterministic failures and cost tracking pay back immediately.

**Provenance**:
- Observability research: `data/exploration/raw/2026-06-21-scouting-observability-safety.md`
- Langfuse, Arize Phoenix, OpenLLMetry repos (star counts verified)
- OpenTelemetry LLM conventions

**Why durable**: Observability platforms are infrastructure (long-lived, not agent frameworks). The principle (build observability early, local-first) is a stable engineering practice.

**How to apply**: Build local structured telemetry first (SQLite session logs, token/cost tracking). Evaluate external platforms (Langfuse for cost tracking/replay, OpenLLMetry for vendor-neutrality) only after human approval and platform comparison. Don't build custom dashboards before evaluating existing tools.

---

## Proposed Memory 10: Self-Evo's Architecture Is Validated by Failures

**Slug**: `self-evo-architecture-validated`
**Type**: project
**Confidence**: Medium-High

**Conclusion**: Self-evo's core design choices (file-first, human-reviewed, GitHub-coordinated, incremental autonomy) are validated by failures of alternatives. Fully autonomous swarms show high pilot failure rates, frameworks die frequently, and benchmark-reality gaps persist. Self-evo's survival strategy: primitive-based (not framework), cost-controlled, human-gated, evidence-driven.

**Provenance**:
- Synthesis across all five research files
- Critic research (failures) + optimistic research (patterns)
- User preferences (executable artifacts, simple workflow, reuse mature work)

**Why durable**: The architectural validation is foundational. Self-evo's differentiators (file-first, human-review) are the reasons it can survive where others died.

**How to apply**: Resist pressure to add framework complexity. Maintain human-review gates. Build cost controls before autonomy. Measure before scaling.

**Confidence caveat**: This is a synthesis conclusion, not a single benchmarked claim. The component evidence is strong; the integration is reasoned inference. Treat as Medium-High.

---

## Summary of Confidence Distribution

| Memory | Type | Confidence |
|--------|------|------------|
| #1 OKF validates file-first | reference | High |
| #2 Framework abandonment | reference | High |
| #3 Benchmark-reality gap | reference | High |
| #4 Cost controls critical | project | Medium-High |
| #5 Hierarchical > swarm | reference | Medium |
| #6 Durable execution defer | reference | High |
| #7 Hybrid memory scales | reference | High |
| #8 Forgetting improves | reference | Medium |
| #9 Observability early | feedback | High |
| #10 Architecture validated | project | Medium-High |

---

## Promotion Protocol

**Do NOT auto-promote**. Human reviews each proposed memory before merging into `data/memory/hot/`.

**For each approved memory**:
1. Create file in appropriate `data/memory/hot/` subdirectory
2. Add frontmatter with `name`, `description`, `created`, `metadata.type`
3. Link related memories with `[[slug]]`
4. Add one-line pointer in `MEMORY.md` index

**Suggested placement**:
- References (#1, #2, #3, #5, #6, #7, #8): `data/memory/hot/reference/`
- Project (#4, #10): `data/memory/hot/project/`
- Feedback (#9): `data/memory/hot/feedback/`

**Confidence note**: Promote High-confidence memories first. Medium-confidence memories (#5, #8) should retain confidence caveats in their body.

---

## Research Notes: Unresolved References

**OpenViking**: Has active user deployment evidence (confirmed via exploration), but public project identity and documentation status could not be resolved during this scout run. Requires dedicated verification before citing as reference.

**GBrain**: URL checked but unavailable during this run. Status unverified.

---

**End of Memory Proposals**
