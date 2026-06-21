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
metadata:
  type: user | feedback | project | reference
---

Memory content with [[linked-memory]] references.
```

**Note**: Do NOT add `accessed` timestamp that mutates on read. If access tracking needed, use separate gitignored index or append-only event log.

**Effort**: 1 day (add created/modified fields, update memory write functions)

**Benefits**:
- Standards-aligned (future-proof)
- Git-native (no breaking changes)
- Enables time-decay scoring for forgetting experiments (if needed)

**Risks**: None (additive only, Markdown remains canonical)

---

### 2. Local Structured Telemetry (JSONL + OpenTelemetry)

**What**: File-based structured logging with OpenTelemetry-compatible schema for local analysis.

**Integration**: Scout runner wrapper captures structured CLI output/usage where available and writes to gitignored `state/telemetry/<date>/<run-id>.jsonl` with standard spans.

```python
import json
from datetime import datetime

def log_span(name, issue_id, metadata, start, end, tokens_used=None):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "span_name": name,
        "issue_id": issue_id,
        "metadata": metadata,
        "duration_ms": int((end - start) * 1000),
        "tokens_used": tokens_used if tokens_used is not None else "unknown",
        "trace_id": f"issue-{issue_id}"
    }
    # Write to gitignored state/telemetry/, not tracked in repo
    with open(f"state/telemetry/{date.today()}/{issue_id}.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
```

**Effort**: Embedded in Scout runner (Issue A.1), no separate infrastructure project

**Benefits**:
- Zero external dependencies
- Local-only (no external transmission without approval)
- OpenTelemetry-compatible (future migration path)
- Cost tracking per issue/agent/day where CLI exposes it
- Post-mortem analysis without cloud access

**Risks**: Unknown token/cost when CLI doesn't expose per-internal-call metrics (logged as "unknown")

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

### 3. Scout Holdout Evaluation Set

**What**: Independent task suite for Scout quality evaluation, avoiding answer leakage.

**Integration**: Create holdout from new tasks, NOT from completed Issues with known-good outcomes in repo history.

```yaml
# data/benchmarks/scout_holdout/task-001-new-domain.yml
task_id: scout-task-001
description: "Explore emerging observability patterns in distributed systems"
input_context: ["Current tech landscape, not in repo history"]
expected_outputs:
  - "data/exploration/daily_reports/*.md"
  - "data/exploration/reuse_maps/*.md"
success_criteria:
  - report_created: true
  - markdown_valid: true
  - frontmatter_present: true
  - evidence_links: {min: 5}
  - no_answer_leakage: true  # Verify no solution in repo history
```

**Effort**: 1 week (create independent holdout tasks, define Scout-specific metrics, run baseline)

**Benefits**:
- Measures actual Scout workflow (not generic coding)
- Validates novelty discovery, relevance filtering, evidence quality
- Avoids answer leakage (holdout independent of repo history)
- Separates Scout quality (exploration) from Builder quality (implementation)

**Risks**: Holdout design quality affects evaluation validity

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

**Reason**: SQLite task queue sufficient for current scale. Durable execution overhead not justified until bottleneck proven.

**Escalation trigger**: Task volume or coordination complexity demonstrates SQLite bottleneck (measured locally, not pre-set threshold) OR cross-host coordination needed.

---

### 13. Defer: Vector Databases

**Systems**: Pinecone, Weaviate, Qdrant

**Reason**: SQLite vector extension handles memory at current scale. External vector DB adds deployment complexity.

**Escalation trigger**: Memory count growth + measured retrieval precision degradation demonstrate semantic search necessity.

---

### 14. Defer: Proactive Scouting Infrastructure Beyond Scout Vertical Slice

**Reason**: Scout vertical slice (Phase A) delivers the core capability. Additional infrastructure (preference learner, multi-source orchestration, semantic deduplication) should be added only after Scout operational and measured needs identified.

**Escalation trigger**: Scout operational AND specific bottlenecks measured (e.g., low relevance rate, high duplicate rate, throughput insufficient).

---

### 16. Defer: Prompt Injection Defense

**Systems**: tldrsec defenses, prompt-guard

**Reason**: Claude has built-in safety. Self-evo's human-review gates catch malicious instructions.

**Escalation trigger**: Adversarial inputs become common OR multi-agent scenarios increase attack surface.

---

## Build New (No Mature Solution)

### 17. Build: Scout Runner with Bounded Execution

**Gap**: No framework provides Scout-specific bounded execution (sources, items, wall-clock, process count).

**Requirements**:
- Launch Claude CLI worker with Scout task
- Enforce: max wall-clock time, max Claude process invocations, max sources scanned, max items scanned/kept
- Capture: structured CLI output/usage where available, exit codes, duration
- Log unknown token/cost as "unknown" (hooks don't expose per-internal-LLM-call metrics)
- Terminate: signal handler for timeout, write partial results
- Resume: load cursor, skip already-processed items

**Implementation**:
```python
class ScoutRunner:
    def run(self, issue_id, config):
        # Launch Claude CLI subprocess
        # Enforce wall-clock timeout
        # Monitor process count
        # Capture structured output
        # Terminate on limits
        # Write partial results
        pass
```

**Effort**: Embedded in Scout vertical slice (Issue A.1-A.2), ~1 week

**Priority**: P0 (enables Scout vertical slice)

---

### 18. Build: Scout Cursor and Ledger System

**Gap**: No mature cursor/ledger pattern for multi-source exploration agents.

**Requirements**:
- Per-source cursor tracking (last-seen timestamp or item ID)
- Deduplication cache (by URL/ID, later semantic)
- Keep/reject ledger with evidence (every item decision logged)
- Idempotent resumption (load cursor, skip processed)
- Gitignored state (cursor, cache, ledger JSONL)

**Schema**:
```json
// state/scout_cursor.json (gitignored)
{
  "github": {"last_seen": "2026-06-21T12:00:00Z"},
  "hackernews": {"last_id": 40123456},
  "arxiv": {"last_date": "2026-06-20"}
}

// data/exploration/raw/2026-06-21-github-ledger.jsonl (gitignored)
{"item_id": "repo/123", "url": "...", "decision": "keep", "reason": "Novel observability pattern", "timestamp": "..."}
{"item_id": "repo/124", "url": "...", "decision": "reject", "reason": "Duplicate of existing source", "timestamp": "..."}
```

**Effort**: Embedded in Scout vertical slice (Issue A.2), ~1 week

**Priority**: P0 (enables idempotent Scout)

---

### 19. Build: Memory Access Tracking (Conditional)

**Gap**: Self-evo needs access/use statistics for forgetting experiments without mutating canonical Markdown.

**Requirements** (only if retrieval bottleneck measured):
- Track memory reads/uses without mutating Markdown files
- Store access events in rebuildable gitignored index or append-only log
- Enable time-decay + access-frequency scoring
- Archive policy: manual only, reversible, requires cooldown proposal + human approval

**Implementation**:
```python
# state/memory_access.db (gitignored, rebuildable)
CREATE TABLE access_log (
  memory_name TEXT,
  accessed_at INTEGER,
  access_type TEXT  -- read, update, link
);

# OR append-only event log
# state/memory_events.jsonl (gitignored)
{"memory": "okf-validates-file-first", "event": "read", "timestamp": "2026-06-21T12:00:00Z"}
```

**Effort**: 1 week (access tracking, forgetting score, archive/restore protocol)

**Priority**: P2 (conditional on measured retrieval bottleneck)

---

## Integration Order (Recommended Sequence)

### Phase A: Autonomous Scout Vertical Slice (Week 1-4)

1. **Scout source registry and runner wrapper** (1 week) — Approved sources, bounded execution, local telemetry embedded
2. **Cursor, deduplication, and keep/reject ledger** (1 week) — Idempotent resumption, evidence-backed filtering
3. **Daily decision report generation** (1 week) — Reuse map, experiment/skill/project candidate, human-reviewable output
4. **Human review label workflow** (3 days) — Feedback loop for preference learning

### Phase B: Scout Evaluation (Week 5-6, after Scout operational)

5. **Scout holdout set and quality metrics** (1 week) — Independent holdout (no answer leakage), Scout vs Builder vs human metrics
6. **Run Scout against holdout and measure** (3 days) — Success rate, cost, failure modes, comparison to human baseline

### Phase C: Conditional Improvements (triggered by observed Scout failures)

7. **Scout reliability** (1 week) — Resume, semantic deduplication, rate limit handling (only if failures observed)
8. **Memory indexing** (2 weeks) — OKF timestamps (created/modified only, no mutating reads), SQLite FTS, OpenViking comparison (only if retrieval bottleneck measured)
9. **Multi-agent coordination** (2-3 weeks) — Parallel Scouts with worktree isolation (only if throughput bottleneck proven)
10. **External observability comparison** (1 week) — Langfuse vs OpenLLMetry (only if local telemetry insufficient for debugging)
11. **Durable workflow engine** (2-3 weeks) — Temporal/Restate checkpointing (only if recovery pain measured)

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
