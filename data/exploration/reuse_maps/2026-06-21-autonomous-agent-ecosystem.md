---
title: "Reuse Map: Autonomous Agent Ecosystem"
date: 2026-06-21
issue: 7
type: reuse_map
status: complete
---

# Reuse Map: What Self-Evo Should Adopt, Adapt, or Build

## Decision Framework

**Adopt**: Use directly with minimal integration work
**Adapt**: Combine patterns or modify for self-evo's file-first approach
**Reject**: Not aligned with self-evo goals or architecture
**Build**: No mature solution exists, requires new implementation

---

## Directly Adopt

### 1. Google Open Knowledge Format (OKF) v0.1

**What**: Markdown+YAML memory standard with timestamps and link conventions.

**Integration**:
```yaml
---
name: short-kebab-case-slug
description: one-line summary
created: 2026-06-21T10:30:00Z
modified: 2026-06-21T15:45:00Z
accessed: 2026-06-21T16:00:00Z
metadata:
  type: user | feedback | project | reference
---

Memory content with [[linked-memory]] references.
```

**Effort**: 1 day (add timestamp fields, update memory write functions)

**Benefits**:
- Standards-aligned (future-proof)
- Git-native (no breaking changes)
- Enables forgetting mechanisms (time-decay scoring)

**Risks**: None (additive only)

---

### 2. Local Structured Telemetry (JSONL + OpenTelemetry)

**What**: File-based structured logging with OpenTelemetry-compatible schema for local analysis.

**Integration**: Write events to `state/telemetry/<date>/<issue-id>.jsonl` with standard spans.

```python
import json
from datetime import datetime

def log_span(name, issue_id, metadata, start, end, tokens_used):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "span_name": name,
        "issue_id": issue_id,
        "metadata": metadata,
        "duration_ms": int((end - start) * 1000),
        "tokens_used": tokens_used,
        "trace_id": f"issue-{issue_id}"
    }
    with open(f"state/telemetry/{date.today()}/{issue_id}.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
```

**Effort**: 2 days (schema design, logging wrapper, basic analysis scripts)

**Benefits**:
- Zero external dependencies
- Git-trackable for debugging
- OpenTelemetry-compatible (future migration path)
- Cost tracking per issue/agent/day
- Post-mortem analysis without cloud access

**Risks**: No real-time dashboard (analyze after execution)

---

### 3. ResearchPlanAssignOps Pattern

**What**: Hierarchical Issue decomposition with phase gates and human review.

**Pattern**:
1. Parent Issue filed by human
2. Scout agent researches, produces plan
3. Human reviews plan, approves phases
4. Execution agent works on approved phase
5. Draft PR created, human reviews
6. Repeat for next phase

**Integration**: Codify as `rules/ISSUE_WORKFLOW.md` with phase labels in GitHub.

**Effort**: 1 week (workflow documentation, phase transition logic, GitHub label automation)

**Benefits**:
- Aligns with self-evo's human-review principle
- Production-proven pattern (used in research automation)
- Natural checkpoint for cost control

**Risks**: None (codifies existing intent)

---

### 3. Self-Evo Native Task Benchmark

**What**: Task suite derived from self-evo's actual Issue history and workflow patterns.

**Integration**: Create benchmark from completed Issues with known-good outcomes.

```yaml
# data/benchmarks/tasks/issue-7-research.yml
task_id: issue-7-research
description: "Research autonomous agent ecosystem patterns"
input_files: [".github/ISSUE_TEMPLATE/", "data/memory/"]
expected_outputs:
  - "data/exploration/reuse_maps/*.md"
  - "data/proposals/project_candidates/*.md"
success_criteria:
  - all_files_created: true
  - markdown_valid: true
  - frontmatter_present: true
  - word_count: {min: 3000}
```

**Effort**: 1 week (extract 10-15 tasks from Issue history, define success criteria, run baseline)

**Benefits**:
- Measures actual self-evo workflows (not generic coding)
- Validates memory retrieval, exploration patterns, proposal generation
- Cheaper to run (<$10 per full eval)
- Immediate feedback loop (runs on real repo structure)

**Risks**: Small sample size initially (grows with Issue history)

---

### 4. SWE-bench Optional Comparison

**What**: Standard coding agent benchmark (500 verified tasks) for optional comparison.

**Integration**: Run after self-evo native benchmark establishes baseline.

**Effort**: 3-4 days (setup evaluation harness, run Claude Code on Verified subset, collect metrics)

**Benefits**:
- Compare self-evo coding-worker capability to industry standard
- Identify coding-specific gaps vs research/exploration patterns
- External validity (peer comparison)

**Risks**: Compute cost (~$50-100 for full Verified run)

**Priority**: P2 (optional validation, not primary measure)

---

### 5. SQLite Lease-Based Coordination

**What**: Task claiming with TTL + heartbeat for multi-agent coordination.

**Schema**:
```sql
CREATE TABLE task_claims (
  task_id TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL,
  claimed_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,
  heartbeat_at INTEGER NOT NULL
);

-- Atomic claim with CAS
INSERT OR IGNORE INTO task_claims (task_id, agent_id, claimed_at, expires_at, heartbeat_at)
VALUES (?, ?, ?, ?, ?);
```

**Integration**: `state/coordination.db` with lease library (Python implementation ~200 lines).

**Effort**: 1 week (schema, claim/release/heartbeat functions, expiry cleanup)

**Benefits**:
- No external dependencies (SQLite built-in)
- Proven pattern (AutoGPT, agent-coordinator)
- Handles agent crashes automatically

**Risks**: Single-host only (sufficient for MVP)

---

## Adapt and Combine

### 5. External Observability Comparison (Approval-Gated)

**What**: Compare Langfuse vs OpenLLMetry for production observability after local telemetry proven.

**Integration**: Only after local JSONL telemetry establishes baseline needs.

**Langfuse**:
- Pros: Rich UI, session replay, prompt versioning
- Cons: External dependency, requires self-hosting or cloud account
- Cost: ~$0-49/month (cloud) or hosting overhead

**OpenLLMetry**:
- Pros: Vendor-neutral, OpenTelemetry standard, export flexibility
- Cons: Requires separate backend (Jaeger/Zipkin/Grafana)
- Cost: Self-hosted infrastructure

**Decision criteria**:
1. Local telemetry insufficient for debugging? (Try for 2-3 Issues first)
2. Need real-time monitoring vs post-mortem? (Async analysis may suffice)
3. Multi-user access required? (Single-user MVP may not need dashboards)

**Effort**: 2-3 days per option (SDK integration, span instrumentation, dashboard setup)

**Priority**: P2 (only after local telemetry bottleneck measured)

---

### 6. Hybrid Memory Architecture (File + Index)

**Pattern**: Markdown files as source of truth, SQLite FTS + embeddings for retrieval.

**Adapted from**: Cognee (multi-store), Mem0 (extraction), ENGRAM (typed retrieval)

**Architecture**:
```
data/memory/hot/           # Canonical Markdown+YAML
state/memory_index.db      # SQLite FTS + vector extension
  - memories table (id, file_path, content_hash)
  - fts_index (full-text search)
  - embeddings (vector similarity)
```

**Integration**:
- **Phase 1**: SQLite FTS only (keyword search, 1 week)
- **Phase 2**: Add embeddings when memory count exceeds measured threshold (2 weeks) — trigger TBD by actual retrieval precision metrics
- **Phase 3**: Forgetting mechanism (time-decay + access-frequency, 1 week)

**Benefits**:
- Scales to 1000+ memories
- Preserves git-native workflow
- Database is rebuildable from files (not authoritative)

**Risks**: Index staleness (rebuild on memory changes)

---

### 7. Three-Layer Termination Defense

**Pattern**: Multiple independent safety limits to prevent runaway execution.

**Adapted from**: Autonomous-agents.io recommendations, production agent deployments

**Layers**:
1. **Per-issue token budget** (e.g., 100k tokens): Hard stop when exceeded
2. **Tool call depth limit** (e.g., 50 calls): Prevent infinite loops
3. **Wall-clock timeout** (e.g., 4 hours): Catch hung processes

**Integration**: `rules/SAFETY_LIMITS.md` enforced by task execution harness.

**Effort**: 3-4 days (budget tracking, depth counter, timeout wrapper, human override protocol)

**Benefits**:
- Prevents runaway failure modes widely reported in agent deployments
- Graceful degradation (partial results returned)
- Justifies autonomous execution to stakeholders

**Risks**: False positives (legitimate long-running tasks)

---

### 8. Forgetting Mechanism

**Pattern**: Time-decay + access-frequency scoring with archive flag.

**Adapted from**: Forgetting problem research (source study reported 3x accuracy gain 13%→39% on their test set)

**Scoring**:
```python
def memory_score(created, modified, accessed, access_count):
    age_days = (now - created).days
    recency_days = (now - accessed).days

    # Time decay: 30-day half-life
    time_factor = 0.5 ** (age_days / 30)

    # Access reinforcement: log scale
    access_factor = log(1 + access_count)

    # Recent access boost
    recency_boost = 1.5 if recency_days < 7 else 1.0

    return time_factor * access_factor * recency_boost
```

**Archive policy**: Score <0.1 → move to `data/memory/archive/`, exclude from retrieval.

**Effort**: 1 week (scoring function, archive workflow, restore protocol)

**Benefits**:
- Prevents unbounded accumulation
- Improves retrieval precision (signal-to-noise)
- Reversible (human can restore archived memories)

**Risks**: Premature archival of important memories

---

### 9. Worktree Isolation for Parallel Agents

**Pattern**: Git worktrees for file conflict prevention.

**Adapted from**: Claude Code native worktree support

**Integration**: Agents working on different Issues use separate worktrees.

```bash
# Agent 1 claims Issue #7
git worktree add .worktrees/issue-7 -b agent/worker-01/7

# Agent 2 claims Issue #8
git worktree add .worktrees/issue-8 -b agent/worker-02/8
```

**Effort**: Already available (Claude Code built-in), just codify protocol.

**Benefits**:
- Zero file conflicts
- Parallel execution without coordination overhead
- Failed agents leave cleanable worktrees

**Risks**: Disk space (worktrees are full checkouts)

---

## Reject and Defer

### 10. Reject: Graph Databases for Memory

**Systems**: Neo4j, Graphiti

**Reason**: Expensive indexing (5s for 100 facts per Graphiti benchmarks), marginal gains for single-agent. Hybrid retrieval (vector + keyword) reported by source studies to achieve comparable benefit at lower cost.

**Decision**: Use SQLite relations for explicit links (`[[name]]` syntax), not graph traversal.

---

### 11. Reject: Agent-Controlled Memory Editing

**Systems**: Letta's tool-based memory editing

**Reason**: Self-evo intentionally requires human review. Automated editing introduces hallucination accumulation.

**Decision**: Agents propose memory changes (via Draft PRs), humans approve.

---

### 12. Reject: Swarm Coordination for MVP

**Systems**: OpenAI Swarm, autonomous task claiming

**Reason**: Hierarchical patterns are prevalent in production multi-agent deployments (source-specific: autonomous-agents.io survey). Swarm adds complexity without proven benefit for self-evo's phased workflow.

**Decision**: Hierarchical assignment (manager assigns Issues to agents), not autonomous claiming.

---

### 13. Defer: Temporal/Restate Durable Execution

**Reason**: SQLite task queue sufficient for <1000 tasks/day. Durable execution overhead not justified until scale proven.

**Escalation trigger**: Task volume exceeds SQLite (>10k tasks/day) OR cross-host coordination needed.

---

### 14. Defer: Vector Databases

**Systems**: Pinecone, Weaviate, Qdrant

**Reason**: SQLite vector extension handles <10k memories. External vector DB adds deployment complexity.

**Escalation trigger**: Memory count growth + measured retrieval precision degradation demonstrate semantic search necessity.

---

### 15. Defer: Proactive Scouting

**Reason**: No mature agent-specific patterns. Human-filed Issues prove value first.

**Escalation trigger**: MVP successful AND clear demand for proactive task discovery.

---

### 16. Defer: Prompt Injection Defense

**Systems**: tldrsec defenses, prompt-guard

**Reason**: Claude has built-in safety. Self-evo's human-review gates catch malicious instructions.

**Escalation trigger**: Adversarial inputs become common OR multi-agent scenarios increase attack surface.

---

## Build New (No Mature Solution)

### 17. Build: Token Budget Enforcement

**Gap**: No framework provides per-issue or per-day token budgets with automatic halting.

**Requirements**:
- Per-issue cap (e.g., 100k tokens)
- Daily cap (e.g., 1M tokens)
- Human override protocol (approve additional budget)
- Cost tracking per agent, per Issue, per day

**Implementation**:
```python
class BudgetEnforcer:
    def check_budget(self, issue_id, tokens_requested):
        used = self.get_issue_usage(issue_id)
        if used + tokens_requested > ISSUE_CAP:
            raise BudgetExceededError(issue_id, used, ISSUE_CAP)
        return True
```

**Effort**: 1 week (budget tracking database, enforcement hooks, approval workflow)

**Priority**: P0 (prevents runaway costs)

---

### 18. Build: GitHub Issue Decomposition Protocol

**Gap**: ResearchPlanAssignOps pattern exists but not codified.

**Requirements**:
- Parent/child Issue linking
- Phase labels (research/design/implement/review)
- Transition protocol (agent signals phase complete, human approves next)
- Progress tracking (% complete per Issue)

**Schema**:
```yaml
# .github/ISSUE_TEMPLATE/agent-task.yml
labels: ["agent-task", "phase:research"]
parent_issue: 7
assigned_agent: scout-worker-01
budget_tokens: 100000
```

**Effort**: 1 week (GitHub labels, phase transition automation, progress dashboard)

**Priority**: P1 (enables multi-phase workflows)

---

### 19. Build: Memory Retrieval API

**Gap**: Self-evo has no programmatic memory retrieval (agents manually Read files).

**Requirements**:
- Keyword search (SQLite FTS)
- Semantic search (embeddings, deferred until measured threshold)
- Recency bias (recent memories ranked higher)
- Type filtering (user/feedback/project/reference)

**API**:
```python
def recall(query: str, limit: int = 5, memory_type: str = None):
    # Keyword + semantic hybrid search
    # Return top-k memories with scores
    return [Memory(name, description, content, score)]
```

**Effort**: 2 weeks (FTS integration, ranking function, API layer)

**Priority**: P1 (scales memory beyond manual lookup)

---

## Integration Order (Recommended Sequence)

### Phase 0: Foundations (Week 1-2)

1. **Self-evo native task benchmark** (1 week) — Establish baseline performance on actual workflows
2. **Local structured telemetry** (2 days) — JSONL event logging for cost/debugging
3. **Token budget enforcement** (1 week) — Hard per-issue and per-day caps with override protocol
4. **Three-layer termination defense** (3 days) — Tool depth limits, wall-clock timeouts, redundancy

### Phase 1: Core Capabilities (Week 3-5)

5. **OKF timestamps** (1 day) — Add created/modified/accessed to memory frontmatter
6. **Memory retrieval API + SQLite FTS** (2 weeks) — Keyword search experiments, measure precision
7. **ResearchPlanAssignOps protocol** (1 week) — Codify phased workflow with GitHub labels

### Phase 2: Multi-Agent Readiness (Week 6-8, only after measured bottlenecks)

8. **External observability comparison** (3 days) — Evaluate Langfuse vs OpenLLMetry if local telemetry insufficient
9. **SQLite lease coordination** (1 week) — Enable parallel agents if single-agent proven slow
10. **Worktree isolation protocol** (1 day) — Codify parallel execution without file conflicts

### Phase 3: Optimization (Future, triggered by measured need)

11. **Forgetting mechanism** (1 week) — Archive low-scoring memories when retrieval precision degrades
12. **Vector embeddings** (2 weeks) — Add semantic search if FTS precision insufficient at scale
13. **SWE-bench optional comparison** (3 days) — Validate coding-worker capability vs standard benchmark
14. **Durable execution engines** (escalate only if SQLite bottleneck proven at task volume >1000/day)
15. **Proactive scouting** (when MVP proven successful and demand clear)

---

## Missing Pieces Summary

**Critical (build now)**:
- Token budget enforcement
- Memory retrieval API

**Important (build in MVP)**:
- GitHub Issue decomposition protocol
- Forgetting mechanism

**Nice-to-have (defer)**:
- Proactive scouting
- Advanced semantic search
- Cross-host coordination

**Already available (adopt)**:
- Local structured telemetry (JSONL + OpenTelemetry schema)
- Self-evo native task benchmark
- OKF memory standard
- SQLite lease coordination
- Worktree isolation
- ResearchPlanAssignOps pattern

---

## Architecture Decision Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Memory format | Markdown+YAML (OKF) | Git-native, transparent, standards-aligned |
| Memory retrieval | SQLite FTS → embeddings | Scales to 1000+ memories, incremental complexity |
| Coordination | Lease-based (SQLite) | No external dependencies, proven pattern |
| Observability | Local JSONL → external (approval-gated) | File-first with optional cloud upgrade |
| Workflow | ResearchPlanAssignOps | Human-review gates, phased execution |
| Safety | Three-layer termination | Redundant limits, graceful degradation |
| Multi-agent | Hierarchical (defer swarm) | Hierarchical patterns prevalent in surveys |
| Durable execution | Defer (SQLite sufficient) | Escalate only if bottleneck proven |
| Evaluation | Self-evo native → SWE-bench optional | Measure actual workflows first |

---

**End of Reuse Map**
