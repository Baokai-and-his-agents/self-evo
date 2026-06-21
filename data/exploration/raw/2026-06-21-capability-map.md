---
title: "Capability Map for Autonomous Agent Ecosystem"
date: 2026-06-21
issue: 7
type: capability_assessment
status: complete
---

# Capability Map: Self-Evo Autonomous Agent Requirements

## Maturity Assessment Framework

**Rating Scale:**
- **Proven**: Production deployments, benchmarks, active maintenance
- **Emerging**: Working implementations, limited production use
- **Experimental**: Research prototypes, no production evidence
- **Gap**: No mature implementations found

**Evidence Confidence:**
- **High**: Primary sources (repos, papers, official docs)
- **Medium**: Secondary sources, maintainer claims
- **Low**: Inference from adjacent systems

---

## Core Capabilities Required by Self-Evo

### 1. Autonomous Loop Execution

**Requirement**: Long-running agents that survive crashes, context overflow, and API failures with automatic recovery.

**Maturity**: Emerging → Proven (infrastructure exists, integration challenging)

**Key Findings**:
- **Durable execution platforms exist**: Temporal.io (35k★), Restate (8k★), Inngest (5k★), DBOS (900★)
- **Critical distinction**: Checkpointing ≠ durable execution. LangGraph checkpoints require manual recovery; Temporal provides automatic retry with event sourcing.
- **Context overflow**: Trigger at ~83.5% capacity in production. Claude Code's compaction handles this, but cross-session memory requires external state.
- **Economic constraint**: runaway costs and non-terminating loops recur across practitioner reports. One secondary source claimed a 95% pilot-failure rate, but this run could not verify that figure from primary evidence, so it is not used as a planning baseline.

**Evidence**:
- Primary: Temporal blog (durable execution for AI agents), Restate architecture docs, autonomous-agents.io failure analysis
- Note: Context overflow threshold (83.5%) is source-specific heuristic, not universal
- Confidence: High (production deployment evidence)

**Gap Assessment**:
- ✅ Infrastructure available (Temporal/Restate/Inngest)
- ⚠️  Integration complexity high (event sourcing mental model shift)
- ❌ Cost controls not standard (no framework provides built-in token budgets)

**Recommendation**: Start with **SQLite-backed task queue + heartbeats** (proven at AutoGPT, OpenHands scale) before escalating to Temporal. Self-evo's GitHub-first coordination reduces need for heavy workflow engines.

---

### 2. Multi-Agent Coordination

**Requirement**: Task claiming, leases, locks, handoffs, conflict resolution for parallel agent execution.

**Maturity**: Proven (primitives) / Emerging (frameworks)

**Key Findings**:
- **Lease-based coordination**: TTL + heartbeat pattern (agent-coordinator 52★, Routa 1,703★)
- **Worktree isolation**: Claude Code's native worktree support prevents file conflicts
- **Distributed systems primitives**: etcd/Consul for cross-host coordination (production-grade)
- **Framework reality check**: 30 agent frameworks archived 2024-2026, including Microsoft TaskWeaver (6,165★) and ACE Framework (1,500★)

**Evidence**:
- Primary: agent-coordinator repo, Routa architecture, Claude Code worktree docs
- Critic finding: Zero public GitHub issues for "coordination failure deadlock" despite thousands of framework users → suggests proprietary suppression or limited real-world multi-agent use
- Confidence: High (primitives), Low (production multi-agent success stories)

**Gap Assessment**:
- ✅ Lease primitives mature (SQLite + atomic CAS)
- ✅ Worktree isolation native to Claude Code
- ⚠️  The surveyed production-oriented systems more often document sequential or manager-worker coordination than unconstrained swarm execution; this is a qualitative observation, not an ecosystem-wide adoption rate
- ❌ No evidence of GitHub Issues-based multi-agent coordination at scale

**Recommendation**: **Single-agent baseline first**. Prove value before adding coordination overhead. When multi-agent needed, use hierarchical (manager assigns tasks) over swarm (autonomous claiming).

---

### 3. GitHub-Centered Coordination

**Requirement**: GitHub Issues as task entrypoint, branches for isolation, Draft PRs for review.

**Maturity**: Emerging → Proven

**Key Findings**:
- **GitHub Agentic Workflows**: Official GitHub feature (2025) with `assign-to-copilot`, `create-agent-session` actions
- **ResearchPlanAssignOps pattern**: Phase transitions with human review gates (production pattern)
- **Draft PR workflow**: Standard in coding agent systems (OpenHands, Sweep, Mentat)

**Evidence**:
- Primary: GitHub Actions docs, GitHub Copilot agent assignment, OpenHands architecture
- Confidence: High (official GitHub support + multiple implementations)

**Gap Assessment**:
- ✅ GitHub Issues/PRs as coordination plane (proven)
- ✅ Branch isolation standard
- ⚠️  Agent-to-agent handoff via GitHub comments exists but not standardized
- ❌ Multi-agent claiming of sub-tasks within one Issue (no mature pattern)

**Recommendation**: **Adopt ResearchPlanAssignOps pattern** — hierarchical Issue decomposition with phase gates. One agent per Issue, human review between phases.

---

### 4. Memory and Context Management

**Requirement**: Persistent memory across sessions, retrieval at scale, hot/cold separation, forgetting mechanisms.

**Maturity**: Proven (architecture) / Emerging (standards)

**Key Findings**:
- **File-first memory renaissance**: Google's Open Knowledge Format (OKF) v0.1 (June 2026) formalizes Markdown+YAML for LLM memory
- **Database-backed retrieval**: ENGRAM (77.55% LoCoMo benchmark), Mem0 (91.6% LoCoMo benchmark), Graphiti (+18.5% accuracy in their evaluation) outperform file-only approaches in source-specific testing
- **Forgetting mechanisms**: Source-specific study showed accuracy improvement (13% → 39%) from selective memory vs unbounded accumulation; gains may vary by task
- **Prompt caching**: Claude's 5-min TTL + up to 90% cost reduction requires strict prefix ordering

**Evidence**:
- Primary: OKF spec, ENGRAM paper (arXiv 2511.12960), Mem0 repo (21k★), forgetting problem analysis
- Confidence: High (benchmarks + production systems)

**Gap Assessment**:
- ✅ File-first (Markdown/YAML) validated by OKF standard
- ✅ Hybrid architecture pattern proven (file + index)
- ⚠️  Forgetting mechanisms not standardized (time-decay, access-frequency, quality scoring all viable)
- ❌ Self-evo lacks retrieval index (linear scan limits scalability)

**Recommendation**: **Phase 1**: Add OKF timestamps + forgetting flags (1 week, zero breaking changes). **Phase 2**: SQLite FTS index (1 week, scales to 1000+ memories). **Phase 3**: Vector embeddings when memory count and retrieval needs justify it.

---

### 5. Proactive Scouting and Monitoring

**Requirement**: RSS/repo/release monitoring, trend detection, opportunity surfacing without explicit requests.

**Maturity**: Experimental

**Key Findings**:
- **RSS monitoring**: Standard pattern (feedparser library, no agent-specific innovation)
- **GitHub watching**: `gh api` + webhooks for releases, Issues, PRs
- **Trend detection**: No mature agent-specific systems found; relies on human-curated sources

**Evidence**:
- Primary: Standard tooling (feedparser, gh CLI)
- Secondary: Agentic AI blog recommendations
- Confidence: Medium (tooling exists, no agent integration patterns)

**Gap Assessment**:
- ✅ RSS/GitHub monitoring primitives available
- ❌ No mature "agent discovers tasks" systems
- ❌ Signal-to-noise filtering immature (requires human curation)

**Recommendation**: **Defer**. Start with human-filed Issues. Add proactive scouting after MVP proves value.

---

### 6. Observability and Tracing

**Requirement**: Structured logging, trace replay, debugging support, cost tracking, error attribution.

**Maturity**: Proven

**Key Findings**:
- **Production platforms**: Langfuse (29k★), Arize Phoenix (10k★), OpenLLMetry (7k★), AgentOps (5k★), Weave (1k★)
- **OpenTelemetry standard**: LLM tracing spans for prompts, completions, tool calls
- **Cost tracking**: Real-time token usage monitoring (Langfuse, AgentOps)
- **Replay**: Session reconstruction from trace logs

**Evidence**:
- Primary: Langfuse docs, Arize Phoenix repo, OpenLLMetry integration guides
- Confidence: High (YC-backed platforms, production deployments)

**Gap Assessment**:
- ✅ Production-grade platforms available
- ✅ OpenTelemetry LLM semantic conventions standardized
- ⚠️  Claude Code integration via MCP possible but not documented in scout research
- ❌ Self-evo has no observability instrumentation

**Recommendation**: **Establish local structured telemetry baseline first** — JSONL logs with OpenTelemetry-compatible structure (trace_id, span_id, timestamps, token counts). Verify local debugging workflows. After approval and comparison of integration options, consider external platforms (Langfuse, OpenLLMetry) for advanced features. Structured logging provides immediate debugging value.

---

### 7. Safety and Evaluation

**Requirement**: Regression testing, harmful action prevention, prompt injection defense, cost overrun protection.

**Maturity**: Emerging (evaluation) / Experimental (security)

**Key Findings**:
- **Evaluation platforms**: DeepEval (16k★), SWE-bench, AgentBench, τ-bench
- **Benchmark reality**: AgentBench reports 37.5% avg success (Claude Opus 3), drops to 0% on post-training Kaggle. τ-bench shows <50% GPT-4o success on realistic tasks.
- **Prompt injection defenses**: tldrsec catalog (706★), prompt-guard tools (niche adoption)
- **Sandboxing**: E2B Desktop (1,414★), Docker/Firecracker for code execution
- **Cost controls**: No standard framework provides token budget enforcement

**Evidence**:
- Primary: AgentBench paper, τ-bench results, tldrsec repo, E2B docs
- Critic finding: Zero public issues for "agent framework cost expensive" or "token budget exceeded"
- Confidence: High (benchmarks), Low (production cost control patterns)

**Gap Assessment**:
- ✅ Evaluation benchmarks mature (SWE-bench standard for coding agents)
- ⚠️  Prompt injection defenses exist but not standardized
- ❌ Cost overrun protection immature (no framework standard)
- ❌ Regression testing for agents nascent

**Recommendation**: 
- **Cost controls**: Build token budget enforcement into MVP (per-issue cap, daily cap, human approval above threshold)
- **Evaluation**: Establish self-evo-native benchmark for autonomous loop performance as primary metric; SWE-bench optional for coding task comparison
- **Security**: Defer prompt injection defenses until after MVP (Claude has built-in safety)

---

## Capability Summary Matrix

| Capability | Maturity | Evidence Confidence | Self-Evo Gap | Priority |
|------------|----------|---------------------|--------------|----------|
| Autonomous loops | Emerging | High | SQLite queue needed | P0 |
| Multi-agent coordination | Proven (primitives) | Medium | Not needed for MVP | P2 |
| GitHub-centered | Proven | High | Already aligned | P0 |
| Memory management | Proven | High | Index needed | P1 |
| Proactive scouting | Experimental | Low | Not needed for MVP | P3 |
| Observability | Proven | High | No instrumentation | P0 |
| Safety/evaluation | Emerging | Medium | Cost controls missing | P0 |

---

## Critical Gaps Requiring New Self-Evo Work

1. **Token budget enforcement**: No mature framework provides this. Must build custom.
2. **GitHub Issue decomposition protocol**: ResearchPlanAssignOps pattern exists but not codified.
3. **Forgetting mechanism**: Time-decay + access-frequency scoring for memory pruning.
4. **Self-evo-native benchmark**: Establish performance baseline for autonomous loop capabilities before adding complexity.

---

## What Not to Build (Mature Reuse Available)

1. **Durable execution**: Use Temporal/Restate if needed (defer until SQLite inadequate)
2. **Observability**: Establish local JSONL baseline; external platforms (Langfuse, OpenLLMetry) available for integration after approval
3. **Lease-based coordination**: Use agent-coordinator pattern if multi-agent needed
4. **Memory retrieval**: Use SQLite FTS + embeddings, don't build custom vector DB

---

**End of Capability Map**
