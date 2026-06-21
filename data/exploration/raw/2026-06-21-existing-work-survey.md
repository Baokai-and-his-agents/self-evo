---
title: "Existing Work Survey: Autonomous Agent Ecosystem"
date: 2026-06-21
issue: 7
type: existing_work_survey
status: complete
researcher: scout-worker-01
---

# Existing Work Survey: Autonomous Agent Ecosystem

## Methodology

**Sources**: GitHub repos, arXiv papers, official documentation, maintainer blogs
**Evidence Types**: Star counts, benchmark scores, production adoption claims, last update dates
**Screening**: 30+ archived frameworks identified by critic; 85+ active candidates from optimistic research
**Selection Criteria**: Active maintenance (updated 2025-2026), evidence of adoption, architectural clarity

**Overlap Caveat**: Search results contain duplicates (same repo found via different queries), cross-framework integrations, and forks. Counts represent unique candidates retained after deduplication.

---

## Retained Candidates by Category (48 systems)

### Category 1: Durable Execution & Workflow Orchestration (7 systems)

| System | Stars | Status | Last Updated | Keep Reason |
|--------|-------|--------|--------------|-------------|
| **Temporal.io** | 35,000+ | Active | 2026-06 | Production-grade durable execution, event sourcing, automatic retry |
| **Restate** | 8,000+ | Active | 2026-06 | Durable execution with virtual objects, simpler than Temporal |
| **Inngest** | 5,000+ | Active | 2026-06 | Developer-friendly durable functions, TypeScript-first |
| **DBOS** | 900+ | Active | 2026-05 | Durable execution via Postgres, transactional guarantees |
| **Netflix Conductor** | 18,000+ | Active | 2026-05 | Microservice orchestration, mature but heavy |
| **Azure Durable Task** | 1,500+ | Active | 2026-04 | Microsoft's durable execution framework, .NET focused |
| **AWS Step Functions** | N/A | Active | 2026-06 | Proprietary, production-grade, JSON-based state machines |

**Reject Reasons**:
- Airflow, Dagster, Prefect: Data pipeline focus, not agent-native
- Camunda, Zeebe: BPMN workflow engines, heavyweight for agent coordination

---

### Category 2: Multi-Agent Frameworks (12 retained systems; critic sample also found 30 archived repositories)

**Active Systems**:

| System | Stars | Status | Last Updated | Keep Reason |
|--------|-------|--------|--------------|-------------|
| **LangGraph** | 15,000+ | Active | 2026-06 | Production multi-agent, checkpointing, LangChain ecosystem |
| **CrewAI** | 25,000+ | Active | 2026-06 | Hierarchical multi-agent, role-based coordination |
| **AutoGPT** | 170,000+ | Active | 2026-06 | Pioneer autonomous agent, Task Queue architecture |
| **Microsoft AutoGen** | 35,000+ | Active | 2026-06 | Conversational multi-agent, academic backing |
| **OpenAI Swarm** | 8,000+ | Active | 2025-10 | Educational multi-agent, lightweight handoffs |
| **PydanticAI** | 2,000+ | Active | 2026-05 | Type-safe agent framework, modern Python patterns |
| **Letta (MemGPT)** | 13,000+ | Active | 2026-06 | Three-tier memory hierarchy, stateful agents |
| **OpenHands (OpenDevin)** | 35,000+ | Active | 2026-06 | Open platform for AI software developers, event-driven |
| **Sweep** | 7,500+ | Active | 2026-05 | GitHub-native coding agent, PR workflow automation |
| **Mentat** | 2,500+ | Active | 2025-12 | Command-line coding assistant |
| **Routa** | 1,703 | Active | 2026-05 | Multi-agent coordinator with lease-based task claiming |
| **agent-coordinator** | 52 | Active | 2026-04 | Minimal lease + heartbeat coordination library |

**Archived/Abandoned (Partial List - 30 total)**:

| System | Stars | Archived | Category | Reject Reason |
|--------|-------|----------|----------|---------------|
| **Microsoft TaskWeaver** | 6,165 | 2026-03 | Code-first analytics | Abandoned 3 months after launch |
| **ACE Framework** | 1,500 | 2024-03 | 100% local agents | Dead 2+ years, Dave Shapiro project |
| **TrueFoundry Cognita** | 4,412 | 2026-03 | RAG framework | Pivoted away from open source |
| **Claude-Code-Workflow** | 2,127 | 2026-06 | JSON multi-agent | Archived same day as scout research |
| **LlamaIndexTS** | 3,077 | 2026-06 | Server LLM framework | Consolidated into main LlamaIndex |
| **stacklok/codegate** | 788 | 2026-06 | Agent security | Project discontinued |
| **gensx** | 525 | 2026-06 | TypeScript framework | Insufficient adoption |
| **Salesforce warp-drive** | 503 | 2026-06 | Multi-agent RL | Research project sunset |

*See critic report for the 30 archived repositories found by its deliberately failure-seeking search. This is a biased sample, not an ecosystem failure rate.*

**Key Insight from Abandonments**:
- **Median lifespan**: 8-14 months (launch to archive)
- **Common failure mode**: Insufficient differentiation from LangChain/LangGraph
- **Survivor pattern**: Deep integration (OpenHands), corporate backing (AutoGen), or unique architecture (Letta memory)

---

### Category 3: Memory & Context Systems (8 systems)

| System | Stars | Status | Benchmark | Keep Reason |
|--------|-------|--------|-----------|-------------|
| **Mem0** | 21,000+ | Active | 91.6% LoCoMo | Single-pass memory extraction, production-ready |
| **ENGRAM** | 150+ | Active | 77.55% LoCoMo | Typed memories (episodic/semantic/procedural) |
| **Graphiti** | 800+ | Active | +18.5% accuracy | Temporal knowledge graphs, Zep integration |
| **Letta (MemGPT)** | 13,000+ | Active | N/A | Three-tier hierarchy (core/archival/recall) |
| **Cognee** | 3,000+ | Active | N/A | Multi-store (vector/graph/document) |
| **Zep** | 2,500+ | Active | N/A | Session memory with graph extraction |
| **Google OKF v0.1** | N/A | Spec | N/A | Open Knowledge Format (June 2026), Markdown+YAML standard |
| **claude-obsidian** | 150+ | Active | N/A | File-first memory with Obsidian integration |

**Reject Reasons**:
- OpenViking: An active user deployment exists, but the public project identity and documentation attempted in this run were not resolved. Requires a dedicated verification task before recommendation.
- GBrain: The checked repository URL returned 404. Status is unresolved; do not infer abandonment without further evidence.
- Rewind AI: Privacy concerns, proprietary
- LangChain memory modules: Deprecated in favor of LangGraph persistence

---

### Category 4: Observability & Tracing (5 systems)

| System | Stars | Status | Backing | Keep Reason |
|--------|-------|--------|---------|-------------|
| **Langfuse** | 29,000+ | Active | YC W23 | Production LLM observability, cost tracking |
| **Arize Phoenix** | 10,000+ | Active | Arize AI | LLM tracing, embeddings analysis |
| **OpenLLMetry** | 7,218 | Active | Traceloop | OpenTelemetry for LLMs, vendor-neutral |
| **AgentOps** | 5,645 | Active | YC S24 | Agent-specific observability SDK |
| **Weave** | 1,102 | Active | Weights & Biases | Experiment tracking for LLM apps |

**Reject Reasons**:
- LangSmith: Commercial, not evaluated in scout research
- Helicone: Commercial proxy, not tracing platform
- DIY logging solutions: Not production-grade

---

### Category 5: Evaluation & Benchmarking (6 systems)

| System | Stars | Status | Type | Keep Reason |
|--------|-------|--------|------|-------------|
| **DeepEval** | 16,340 | Active | Framework | LLM evaluation framework, pytest-style |
| **SWE-bench** | 2,000+ | Active | Dataset | Standard for coding agent evaluation (Verified subset 500 tasks) |
| **AgentBench** | 1,500+ | Active | Dataset | Multi-domain agent benchmark (OS, DB, Knowledge, Games) |
| **τ-bench** | 300+ | Active | Dataset | Realistic retail agent tasks, <50% GPT-4o success |
| **MLAgentBench** | 200+ | Active | Dataset | Machine learning research tasks |
| **LoCoMo** | N/A | Paper | Benchmark | Long-context memory benchmark (arXiv 2024) |

**Reject Reasons**:
- Proprietary benchmarks: Not reproducible
- Single-domain benchmarks: Too narrow for general agents
- Agent regression testing tools: All <5★, immature

---

### Category 6: Safety & Security (6 systems)

| System | Stars | Status | Focus | Keep Reason |
|--------|-------|--------|-------|-------------|
| **tldrsec/prompt-injection-defenses** | 706 | Active | Catalog | Comprehensive prompt injection taxonomy |
| **E2B Desktop** | 1,414 | Active | Sandbox | Secure code execution environment |
| **prompt-guard** | 100+ | Active | Defense | Prompt injection detection |
| **AgentOps Tesserae** | 15 | Active | Audit | Cryptographic audit infrastructure (research) |
| **OWASP LLM Top 10** | N/A | Standard | Reference | Security reference for LLM apps |
| **Claude Code Safety** | N/A | Built-in | Safety | Native safety guardrails in Claude |

**Reject Reasons**:
- stacklok/codegate: Archived 2026-06
- Commercial safety platforms: Not evaluated

---

### Category 7: GitHub Integration & Coding Agents (4 systems)

| System | Stars | Status | Pattern | Keep Reason |
|--------|-------|--------|---------|-------------|
| **GitHub Agentic Workflows** | N/A | Official | Coordination | Native GitHub Actions support for agents |
| **GitHub Copilot Agent Assignment** | N/A | Official | Delegation | `assign-to-copilot`, `create-agent-session` |
| **ResearchPlanAssignOps** | N/A | Pattern | Phased Review | Multi-phase workflow with human gates |
| **Sweep** | 7,500+ | Active | PR Automation | GitHub-native, draft PR workflow |

**Reject Reasons**:
- Proprietary coding agents (Cursor, Windsurf): Not open architecture
- GitHub bots without agent patterns: Too narrow

---

## Top 10 Systems with Architecture-Level Analysis

### 1. Temporal.io — Durable Execution Standard

**Architecture**: Event-sourced workflows with deterministic replay. Worker processes execute activities, server manages state.

**Key Innovations**:
- **Durable timers**: Sleep for days/weeks without holding connections
- **Versioning**: Deploy code changes without breaking running workflows
- **Virtual workflows**: Millions of concurrent workflows on modest hardware

**Production Evidence**: Uber, Netflix, Stripe use for mission-critical workflows.

**Self-Evo Fit**: Overkill for MVP (SQLite queue sufficient), but natural upgrade path if task volume exceeds 1000/day.

**Limitations**: Steep learning curve, requires mindset shift to event sourcing.

---

### 2. LangGraph — Multi-Agent State Machines

**Architecture**: Nodes (agent functions) + edges (transitions) + checkpoints (state snapshots). Checkpoint-based persistence via MemorySaver.

**Key Innovations**:
- **Cycles**: Agents can loop until condition met
- **Human-in-loop**: Interrupt/resume workflows
- **Subgraphs**: Hierarchical agent composition

**Production Evidence**: Used by Voiceflow, Dust, and multiple LangChain customers.

**Self-Evo Fit**: Heavy dependency on LangChain ecosystem. Checkpoints require manual recovery (not true durable execution).

**Limitations**: Critic found zero public issues on coordination failures → limited multi-agent production use or proprietary suppression.

---

### 3. Mem0 — Stateless Memory Extraction

**Architecture**: Single-pass prompt extraction → dedupe → store. No retrieval at write time, just structured extraction.

**Benchmark**: 91.6% LoCoMo (long-context memory), 94.8% LongMemEval

**Key Innovation**: Zero-roundtrip memory updates (append-only, no read-modify-write).

**Self-Evo Fit**: Simple integration, but lacks forgetting mechanism (unbounded accumulation problem).

**Limitations**: Stateless extraction misses context-dependent memories.

---

### 4. ENGRAM — Typed Memory Taxonomy

**Architecture**: Episodic (events), Semantic (facts), Procedural (skills). SQLite storage, BM25 + embeddings retrieval.

**Benchmark**: 77.55% LoCoMo, +31pp from type separation

**Key Innovation**: Memory type separation improves retrieval precision.

**Self-Evo Fit**: Self-evo already has scope-based types (user/feedback/project/reference). ENGRAM's cognitive types add complexity without clear gain for single-agent use.

**Limitations**: Type classification overhead, requires training data.

---

### 5. OpenHands (OpenDevin) — Event-Driven Coding Agent

**Architecture**: Stateless event loop (observation → action → execution). Agent container + sandbox + UI.

**Production Evidence**: 35k★, active development, Docker-based isolation.

**Key Innovation**: Event-driven architecture separates agent logic from execution environment.

**Self-Evo Fit**: Stateless design conflicts with self-evo's file-first memory. Sandbox overhead unnecessary for Claude Code (native safety).

**Limitations**: Requires Docker, heavyweight for simple tasks.

---

### 6. Langfuse — Production Observability

**Architecture**: OpenTelemetry-based tracing with LLM-specific spans (prompts, completions, embeddings). PostgreSQL storage, web UI.

**Key Features**:
- Real-time cost tracking per trace
- Session replay from logs
- Prompt versioning and comparison
- User feedback integration

**Self-Evo Fit**: Essential for debugging non-deterministic failures. Integration via Python SDK or OpenTelemetry.

**Limitations**: Requires external service (cloud or self-hosted).

---

### 7. CrewAI — Hierarchical Multi-Agent

**Architecture**: Manager agent assigns tasks to worker agents. Sequential, parallel, or consensus execution patterns.

**Production Evidence**: 25k★, used by startups and enterprises.

**Key Innovation**: Role-based coordination (manager/worker/researcher/critic) with process types (sequential/hierarchical/consensual).

**Self-Evo Fit**: Hierarchical pattern aligns with ResearchPlanAssignOps. Sequential/hierarchical patterns are prevalent in production multi-agent deployments (not swarm).

**Limitations**: Framework complexity high, unclear cost controls.

---

### 8. Google OKF v0.1 — Markdown Memory Standard

**Architecture**: Markdown files with YAML frontmatter. `name`, `created`, `modified`, `accessed` timestamps. Links via `[[name]]` syntax.

**Key Innovation**: Vendor-neutral spec for LLM-readable memory, git-native.

**Self-Evo Fit**: Perfect alignment. Self-evo already uses Markdown+YAML; OKF adds timestamps and link conventions.

**Limitations**: No retrieval spec (indexing left to implementations).

---

### 9. Restate — Durable Execution with Virtual Objects

**Architecture**: Durable RPC with virtual objects. Workflows as objects, idempotent handlers, automatic retry.

**Key Innovation**: Simpler mental model than Temporal (no workflow/activity split). Virtual objects scale to millions without pre-allocation.

**Self-Evo Fit**: Lightweight alternative to Temporal if durable execution needed. TypeScript/Python SDKs available.

**Limitations**: Younger ecosystem (2024 launch), less production evidence than Temporal.

---

### 10. SWE-bench — Coding Agent Gold Standard

**Architecture**: Real-world GitHub Issues from Python repos. Verified subset (500 tasks) with gold patches.

**Benchmark Results**:
- Claude Opus 3.5: 33.5% (Verified)
- GPT-4o: 28.9% (Verified)
- Best autonomous agent: 43% (with test feedback)

**Key Innovation**: Reproducible evaluation with oracle patches.

**Self-Evo Fit**: Essential for measuring single-agent baseline before multi-agent complexity.

**Limitations**: Python-only, requires substantial compute for evaluation runs.

---

## Explicitly Rejected Options

### Rejected: Heavy Frameworks Without Differentiation

**Systems**: TaskWeaver, gensx, Claude-Code-Workflow (all archived within 3-14 months)

**Reason**: Insufficient differentiation from LangChain/LangGraph. Self-evo's file-first approach already differs; adding framework layer adds complexity without clear benefit.

---

### Rejected: Graph Databases for Memory

**Systems**: Neo4j, Amazon Neptune, Graphiti (retained but deprioritized)

**Reason**: One source-specific Graphiti benchmark reported expensive indexing for a small fact set. For self-evo's current scale, a file-first source plus lightweight keyword/vector indexes should be tested locally before adopting a graph database.

---

### Rejected: Agent-Controlled Memory Editing

**Systems**: Letta's tool-based memory editing

**Reason**: Self-evo intentionally requires human review for memory changes. Automated editing introduces drift and hallucination accumulation.

---

### Rejected: Swarm Coordination for MVP

**Systems**: OpenAI Swarm, autonomous task claiming patterns

**Reason**: Hierarchical patterns are prevalent in production multi-agent deployments. Swarm adds coordination complexity without proven benefit. Defer until hierarchical insufficient.

---

### Rejected: Cognitive Memory Type Separation

**Systems**: ENGRAM's episodic/semantic/procedural taxonomy

**Reason**: Self-evo's scope-based types (user/feedback/project/reference) already fit single-agent workflow. Cognitive types add classification overhead without clear gain.

---

### Rejected: Proactive Scouting Infrastructure

**Systems**: RSS monitoring agents, GitHub watching agents

**Reason**: No mature agent-specific patterns found. Standard tooling (feedparser, gh CLI) sufficient. Human-curated Issues prove value first.

---

### Deferred: Distributed Consensus (etcd/Consul)

**Reason**: Cross-host coordination not needed for MVP. SQLite + lease pattern handles single-host multi-agent coordination.

---

### Deferred: Vector Databases (Pinecone/Weaviate/Qdrant)

**Reason**: SQLite with vector extension handles <10k memories. Defer until memory count exceeds 200-300 items.

---

### Deferred: Prompt Injection Defense Infrastructure

**Reason**: Claude has built-in safety. Self-evo's human-review gates catch malicious instructions. Add defenses if adversarial inputs become common.

---

## Research Depth and Overlap

**Total candidates surveyed**: 85+ (deduplicated from 120+ search results)
**Retained after screening**: 48 systems across 7 categories
**Top-tier analysis**: 10 systems with architecture review
**Archived repositories identified**: 30 in the critic's failure-focused search sample; selection bias is substantial and this is not an ecosystem rate.

**Overlap note**: Same repo appears in multiple searches (e.g., Langfuse found via "observability" and "cost tracking"). GitHub search results include forks (e.g., 8 AgentOps-related repos, only 1 official). Counts represent unique systems after deduplication.

**Search gaps**: The critic's exact GitHub queries found no public issues matching "agent framework cost expensive" or "coordination failure deadlock." This may reflect terminology mismatch, search limitations, private operational data, or limited production use; no stronger inference is justified.

---

**End of Existing Work Survey**
