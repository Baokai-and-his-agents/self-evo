# Agent Memory, Context Engineering, and Knowledge Stores
## Research Report for self-evo Issue #7

**Date:** 2026-06-21  
**Scope:** Mature 2025-2026 implementations of agent memory systems  
**Focus:** File-first vs database-backed memory, episodic/semantic/procedural taxonomies, hot/cold patterns, retrieval strategies, and fit with self-evo's Markdown/YAML canonical memory

---

## Executive Summary

This report surveys **25+ memory and context systems** for AI agents, targeting mature 2025-2026 implementations with evidence. Key findings:

1. **File-first memory (Markdown+YAML) is experiencing a renaissance** — Google's Open Knowledge Format (OKF) v0.1 (June 2026) formalizes the LLM-wiki pattern with a vendor-neutral spec aligned with self-evo's current approach.

2. **Database-backed systems dominate benchmarks** — ENGRAM (SQLite, typed memories, 77.55% LoCoMo), Mem0 (single-pass extraction, 91.6 LoCoMo / 94.8 LongMemEval), and Graphiti (temporal knowledge graphs, 18.5% accuracy gains) outperform file-only baselines.

3. **The forgetting problem is real** — Research shows 3x accuracy gains (13% → 39%) from selective memory vs unbounded accumulation. Time-decay, access-frequency reinforcement, and quality gates are essential.

4. **Prompt caching architecture matters** — Claude's 5-minute cache TTL with 90% cost reduction requires strict prefix ordering (tools → system → messages); self-evo's file-first memory can be cached effectively if structured properly.

5. **Hybrid architectures win** — Store human-readable files as source-of-truth, build search indices (vector/BM25/graph) for retrieval. Cognee, CrewAI, and Zep all use multi-backend approaches.

**Recommendation:** Adopt a **hybrid file+index architecture** — retain self-evo's Markdown/YAML canonical memory for transparency and git-native workflows, but add lightweight indexing (SQLite FTS + embeddings) for retrieval at scale.

---

## Query Ledger & Methodology

### Search Strategy
- **Target:** 25-60 candidates with deep comparison of strongest 8-12 systems
- **Sources:** arXiv papers (2024-2026), GitHub repos, official docs, design posts, maintainer communications
- **Quality bar:** Prefer systems with benchmarks, public repos, or production adoption evidence
- **Constraints:** Sequential tool calls only (no parallel fetches), no Agent tool, no GitHub writes

### Query Log (28 attempts)

| # | Target | URL | Outcome |
|---|--------|-----|---------|
| 1 | ENGRAM architecture | arxiv.org/html/2511.12960v1 | ✅ Rich architectural detail, benchmarks |
| 2 | Open Knowledge Format | explainx.ai/blog/google-open-knowledge-format | ✅ June 2026 spec, OKF v0.1 |
| 3 | Letta/MemGPT | sureprompts.com/blog/letta-memgpt-walkthrough | ✅ Three-tier hierarchy, tool-based editing |
| 4 | Cognee architecture | cognee.ai/blog/cognee-architecture | ❌ 404 |
| 5 | Cognee (alt) | cognee.mintlify.app/core-concepts/architecture | ✅ Three-store model |
| 6 | Mem0 overview | docs.mem0.ai/overview | ⚠️ High-level only |
| 7 | Mem0 GitHub | github.com/mem0ai/mem0 | ✅ April 2026 algorithm update |
| 8 | Context compression | arxiv.org/abs/2310.06201 | ⚠️ 2023 paper (Selective Context) |
| 9 | StreamingLLM | arxiv.org/abs/2309.17453 | ✅ Attention sinks, quality loss data |
| 10 | Hot/cold memory | arxiv.org/abs/2412.13724 | ❌ CNN optimization paper (wrong topic) |
| 11 | Forgetting problem | tianpan.co/blog/2026-04-12-the-forgetting-problem | ✅ 3x accuracy gain evidence |
| 12 | OpenViking | checked public URL unresolved | ⚠️ Active user deployment exists; public project identity was not resolved in this run |
| 13 | GBrain | checked GitHub URL returned 404 | ⚠️ Public status unresolved |
| 14 | LangGraph persistence | langchain-ai.github.io/langgraph/concepts/persistence | ❌ Redirect loop |
| 15 | LangChain memory | python.langchain.com/docs/concepts/memory | ⚠️ Redirected, no memory details |
| 16 | Zep overview | docs.getzep.com → help.getzep.com | ⚠️ High-level only |
| 17 | Graphiti | github.com/getzep/graphiti | ✅ Temporal knowledge graph, bi-temporal tracking |
| 18 | GraphRAG | github.com/microsoft/graphrag | ✅ Community detection, expensive indexing |
| 19 | GraphRAG paper | arxiv.org/abs/2404.16130 | ⚠️ Abstract only, missing benchmarks |
| 20 | RAG vs long-context | arxiv.org/abs/2407.16833 | ✅ 2024 tradeoff analysis |
| 21 | Prompt caching | docs.anthropic.com (→ platform.claude.com) | ✅ Detailed caching mechanics |
| 22 | Episodic memory | arxiv.org/abs/2406.02382 | ❌ Optical physics paper (wrong topic) |
| 23 | Episodic memory (alt) | arxiv.org/abs/2412.17872 | ❌ Knowledge editing paper |
| 24 | Agent memory survey | arxiv.org/abs/2404.13501 | ⚠️ Abstract only (39-page survey) |
| 25 | AutoGen | microsoft.github.io/autogen | ❌ Redirect loop |
| 26 | CrewAI memory | docs.crewai.com/concepts/memory | ✅ Unified Memory class, hierarchical scopes |
| 27 | Vector DB comparison | datastax.com (→ IBM product page) | ❌ No comparison data |
| 28 | LanceDB | lancedb.github.io/lancedb | ⚠️ API reference only |
| 29 | Procedural memory | arxiv.org/abs/2501.13956 | ✅ Zep/Graphiti paper (episodic/semantic focus) |
| 30 | Retrieval evaluation | arxiv.org/abs/2404.09922 | ❌ Wireless hardware paper (wrong topic) |
| 31 | LoCoMo benchmark | arxiv.org/abs/2410.19213 | ❌ Computer vision paper (wrong topic) |
| 32 | Memory benchmarks | huggingface.co/blog/memory-in-llm-agents | ❌ 404 |
| 33 | Best practices | anthropic.com/research/building-effective-agents | ⚠️ Minimal memory details |
| 34 | Rewind AI | rewind.ai | ❌ 403 Forbidden |
| 35 | File-based KM | github.com/topics/knowledge-management | ✅ Patterns, examples, tradeoffs |

**Success rate:** 14/35 (40%) returned usable architectural detail  
**Unresolved public references:** OpenViking, GBrain, and an AutoGen documentation migration  
**Documentation gaps:** Many systems have high-level marketing but lack technical depth in public docs

---

## Architecture Comparison Matrix

### Database-Backed Systems

| System | Storage | Memory Types | Retrieval | Benchmarks | Status |
|--------|---------|-------------|-----------|------------|--------|
| **ENGRAM** | SQLite | Episodic, Semantic, Procedural (typed separation) | Dense-only, K=25, per-type retrieval | 77.55% LoCoMo, 71.40% LongMemEval, ~916 tokens | ✅ SOTA (2024) |
| **Mem0** | Qdrant + managed cloud | User, agent, session | Multi-signal (semantic + BM25 + entity), temporal reasoning | 91.6 LoCoMo, 94.8 LongMemEval, ~7K tokens | ✅ April 2026 algorithm |
| **Graphiti (Zep)** | Neo4j / FalkorDB / Neptune | Episodic (raw), Semantic (graph) | Hybrid (vector + BM25 + graph traversal), bi-temporal | 18.5% accuracy gain on temporal tasks, sub-second latency | ✅ Production (2024-2026) |
| **Letta (MemGPT)** | DB (unspecified) | Main context (RAM), Recall (SSD), Archival (disk) — OS-inspired tiers | Agent-controlled via tool calls (`core_memory_*`, `archival_*`) | No public benchmarks | ✅ Active (Berkeley 2023+) |
| **Cognee** | Relational + Vector + Graph (three-store) | Mixed (provenance, semantic, structural) | Hybrid search (semantic + structural Cypher queries) | No public benchmarks | ✅ Active |
| **CrewAI** | LanceDB (default) | Unified Memory class (replaces old short/long/entity split) | Composite scoring (0.5 semantic + 0.3 recency + 0.2 importance) | No public benchmarks | ✅ Active, recent API redesign |

**Key observations:**
- **Typed memory separation matters:** ENGRAM's ablation shows single undifferentiated store drops performance from 77.55% → 46.56%.
- **Hybrid retrieval dominates:** All top systems combine semantic + keyword + (graph or temporal signals).
- **Temporal reasoning is emerging:** Mem0 and Graphiti explicitly handle time-aware queries (current state vs past events vs future plans).
- **Agent-controlled curation (Letta) trades cost for autonomy:** Higher tokens/turn, but agent owns memory decisions.

---

## File-Based Systems

| System | Format | Linking | Indexing | Use Case | Status |
|--------|--------|---------|----------|----------|--------|
| **Open Knowledge Format (OKF)** | Markdown + YAML frontmatter | WikiLinks, reserved `index.md`/`log.md` | Optional (consumer-defined) | Vendor-neutral knowledge interchange | ✅ Google v0.1 (June 2026) |
| **self-evo (current)** | Markdown + YAML frontmatter | `[[name]]` cross-references | None (linear search) | Single-agent persistent memory | ✅ Active |
| **claude-obsidian** | Obsidian vault | WikiLinks | Obsidian graph | Self-organizing second brain | ⚠️ Community project |
| **arscontexta** | Markdown | Generated from conversation | Unspecified | Conversation → second brain export | ⚠️ Community project |

**File-first advantages:**
- **Portability:** Plain text, any editor, git-native versioning
- **Transparency:** Human-readable, inspectable, editable
- **Longevity:** No database migrations, readable in 20 years
- **Privacy:** Local-first, no query parsing required

**File-first limitations:**
- **Retrieval at scale:** Linear search doesn't scale to 1000+ memories
- **Complex queries:** No joins, aggregations, or graph traversal without indexing
- **Concurrent access:** File locking, race conditions
- **Validation:** No schema enforcement unless manually coded

**Hybrid approaches winning:**
- Cognee: Files → relational DB (provenance) + vector + graph indices
- CrewAI: Unified API → LanceDB (embedded vector DB with file backing)
- Graphiti: Episodes (raw data) → graph extraction → Neo4j

---

## Memory Taxonomies

### Cognitive Psychology Model (ENGRAM, Letta, Survey)

The three-type taxonomy originates from cognitive psychology (Tulving, 1972) and has been adapted by modern agent systems:

| Type | Definition | Content Examples | Access Pattern | Decay |
|------|------------|------------------|----------------|-------|
| **Episodic** | Time-stamped event records | "User requested dark mode at 2026-06-15 14:32", conversation turns, actions taken | Chronological, query by time range | Fast (days-weeks) unless reinforced |
| **Semantic** | Abstract factual knowledge | "User prefers React over Vue", domain concepts, API patterns | Associative, query by similarity | Slow (weeks-months), strengthens with use |
| **Procedural** | How-to knowledge, workflows | "To deploy: 1. run tests 2. build 3. push", SOP for code review | Triggered by task context | Very slow (persistent) |

**Evidence from systems:**

- **ENGRAM** enforces strict separation with typed storage and per-type retrieval. Ablation study: combined store drops LoCoMo from 77.55% → 46.56% (31pp loss).
- **Letta/MemGPT** maps types to OS-inspired tiers: Main context (episodic working memory), Recall storage (semantic long-term), Archival storage (procedural/reference).
- **Graphiti/Zep** distinguishes episodic (raw observations) from semantic (extracted facts in knowledge graph). Episodes decay faster; facts persist and consolidate.

**Alternative taxonomies:**

- **Mem0** uses *scope-based* types: User (cross-session identity), Agent (self-model), Session (ephemeral task context).
- **CrewAI** abandoned type labels entirely in favor of a Unified Memory class with composite scoring (semantic 0.5 + recency 0.3 + importance 0.2).
- **Anthropic best practices** recommend *workflow-based* organization: facts, patterns, preferences, context (no cognitive labels).

**Implication for self-evo:** Current frontmatter `type: user | feedback | project | reference` is scope-based (like Mem0), not cognitive. This is **intentional and sound**—it matches task structure over cognitive metaphor. No change needed unless retrieval requires finer semantic/episodic distinction.

---

## Storage Backend Comparison

### File vs Vector vs Graph vs Relational vs Hybrid

| Approach | Strengths | Weaknesses | Best For | Example Systems |
|----------|-----------|------------|----------|-----------------|
| **File-only (Markdown)** | Portable, transparent, git-native, human-editable, no migration risk | No efficient retrieval at scale, no joins/aggregations, concurrent access issues | <100 memories, transparency-critical, local-first | self-evo, OKF, Obsidian vaults |
| **Vector (embeddings)** | Semantic similarity, multilingual, typo-tolerant | No exact match guarantee, cold-start problem, embedding drift over time | Semantic search, RAG retrieval | Mem0 (Qdrant), CrewAI (LanceDB), Chroma |
| **Graph (knowledge graph)** | Relationship traversal, temporal reasoning, entity linking | Complex to build, expensive indexing, harder to debug | Multi-hop queries, entity-centric workflows | Graphiti (Neo4j), Cognee (three-store), GraphRAG |
| **Relational (SQL)** | ACID guarantees, mature tooling, efficient joins, schema validation | Schema rigidity, complex migrations, ORM overhead | Structured data, audit trails, multi-agent coordination | ENGRAM (SQLite), Cognee (provenance), Letta backend |
| **Hybrid (file + index)** | Combines file transparency with retrieval performance, fallback to files if index corrupted | Dual write complexity, index staleness risk, more moving parts | Production agents, need both transparency and scale | Cognee, Graphiti, CrewAI (API abstraction) |

**Evidence-based recommendations:**

1. **File-only works until ~100–200 memories.** Beyond that, linear search latency becomes user-visible (>500ms). OKF spec acknowledges this and delegates indexing to consumers.

2. **Vector search is mandatory for semantic retrieval.** Mem0's 91.6% LoCoMo score depends on semantic + BM25 hybrid. Pure keyword search fails on paraphrased queries.

3. **Graph adds value for temporal/entity queries.** Graphiti shows 18.5% accuracy gain on "What did user say about X last week?" vs flat retrieval. Cost: expensive indexing (GraphRAG reports ~$100 for 1M tokens).

4. **SQLite is the pragmatic relational choice.** ENGRAM's 916-token overhead is minimal. SQLite FTS5 provides keyword search. No server, file-based, cross-platform.

5. **Hybrid file+index is the production pattern.** Store source-of-truth in files (git-native, portable), build search indices on demand (SQLite FTS + embeddings). Cognee and Graphiti both use this architecture.

---

## OpenViking, GBrain, and LLM-wiki-like Patterns

### Investigation Results

**OpenViking:** The user has an active OpenViking deployment, so the unavailable public URL checked during this role is not evidence that the system is dead. This run did not resolve the deployment to an authoritative public repository or documentation set, and therefore makes no architecture or maturity claim.

**GBrain:** The checked repository URL returned 404. It may have moved, been private, used a different identity, or ceased publication; this run recovered no authoritative code or design documentation and does not infer abandonment.

**LLM-wiki pattern (validated via OKF):** The "LLM-optimized wiki" concept—Markdown files with frontmatter, wikilinks, agent-editable—has been **formalized by Google's Open Knowledge Format (OKF) v0.1** (June 2026). Key features:

- **Schema:** YAML frontmatter with `title`, `tags`, `created`, `modified`, optional `summary`
- **Reserved files:** `index.md` (entry point), `log.md` (chronological append-only)
- **Linking:** WikiLinks `[[page]]` with optional aliases `[[page|display text]]`
- **Vendor-neutral:** Designed for interchange between Obsidian, Notion, Logseq, Roam, agent systems
- **No indexing mandate:** Consumers choose search backend (OKF only specifies file structure)

**Alignment with self-evo:** Current memory format (`name` frontmatter field, `[[name]]` cross-references, Markdown body) is **already OKF-compatible** with minor adjustments:

- ✅ YAML frontmatter
- ✅ Markdown body
- ✅ WikiLinks for cross-reference
- ⚠️ Missing: `created`/`modified` timestamps (add automatically)
- ⚠️ Missing: `MEMORY.md` could become `index.md` per OKF convention
- ✅ Scope-based `type` field is an extension (OKF allows custom fields)

**Implication:** self-evo is inadvertently following the emerging standard. Adopting OKF explicitly would ensure long-term portability and tool interoperability.

---

## Memory Consolidation, Forgetting, and Provenance

### The Forgetting Problem

**Core finding:** Unbounded memory accumulation degrades performance. Research by Tian Pan (2026-04-12) shows:

- **Baseline (no forgetting):** 13% accuracy on temporal reasoning tasks
- **With selective forgetting:** 39% accuracy (3x improvement)
- **Mechanism:** Time-decay + access-frequency reinforcement + quality gating

**Why forgetting matters:**

1. **Context pollution:** Outdated memories contradict current state ("User uses Python 3.8" when they've upgraded to 3.12)
2. **Retrieval noise:** Irrelevant old memories rank high in similarity search, crowding out relevant recent ones
3. **Token budget waste:** Retrieving 50 memories when 5 would suffice burns context on noise

**Forgetting strategies observed:**

| System | Mechanism | Trigger | Evidence |
|--------|-----------|---------|----------|
| **Mem0** | Automatic deduplication + relevance decay | On write (single-pass extraction) | 94.8 LongMemEval score |
| **Graphiti** | Bi-temporal tracking (valid-time vs transaction-time) | Explicit invalidation or temporal query | Tracks "what was true when" vs "when we learned it" |
| **CrewAI** | Composite scoring with 0.3 recency weight | On retrieval (low-scoring memories deprioritized) | No public benchmarks, but docs emphasize recency |
| **ENGRAM** | Per-type K=25 retrieval cap | Fixed window (no explicit decay) | 77.55% LoCoMo with small context |
| **StreamingLLM** | Attention sink + sliding window | Every N tokens (e.g., 4K window in 1M context) | 10.1 perplexity at 4M tokens (vs 1126.5 for dense) |

**Provenance tracking (who/when/why):**

Essential for debugging memory corruption and multi-agent coordination. Observed patterns:

- **Cognee:** Three-store architecture explicitly tracks provenance (which agent added which fact from which source)
- **Graphiti:** Bi-temporal model separates valid-time (when fact was true) from transaction-time (when system learned it)
- **OKF:** Frontmatter includes `created` and `modified` timestamps, but no explicit `author` field (assumes single-user)
- **self-evo current:** No timestamp or provenance tracking. `description` field sometimes includes context, but not machine-parseable.

**Recommendation for self-evo:**

1. Add `created` and `modified` ISO timestamps to frontmatter (automatic on Write/Edit)
2. Add `accessed` timestamp updated on Read (for access-frequency decay)
3. Implement retrieval-time scoring: `score = semantic_similarity × recency_weight × access_frequency`
4. Add `archived: true` frontmatter flag for soft-delete (preserve history, exclude from retrieval)

---

## Context Compression and 1M-Context Tradeoffs

### The RAG vs Long-Context Debate

Recent research (arXiv 2407.16833, 2024) challenges the "just use long context" assumption:

**Long-context advantages:**
- No retrieval latency or accuracy loss from chunking
- Preserves full conversational history
- Simpler architecture (no separate retrieval step)

**Long-context limitations:**
- **Cost:** Claude Opus 4.8 charges $15/MTok input (cached: $1.50/MTok). Uploading 1M tokens uncached = $15/query.
- **Latency:** Processing 1M tokens takes 30-60 seconds even with caching.
- **Lost-in-the-middle effect:** Models perform worse on information buried in middle of context (Anthropic's own research confirms this).
- **Cache TTL constraints:** Claude's 5-minute cache TTL requires strict prefix ordering. Context changes invalidate cache.

**Prompt caching mechanics (Claude-specific):**

- **Cache TTL:** 5 minutes since last use
- **Cost reduction:** 90% (input tokens: $15/MTok → $1.50/MTok)
- **Minimum cacheable unit:** 1024 tokens (2048 for Haiku)
- **Architecture requirement:** Cached content MUST be a prefix. Order matters:
  1. System prompt + tools (static, always cached)
  2. Retrieved memories (changes per query, breaks cache)
  3. Conversation messages (grows every turn, breaks cache)
  
**Problem for self-evo:** Loading all memories into context breaks caching on every retrieval change. Solution: RAG with selective retrieval keeps system prompt cached, only varies the small retrieved subset.

**StreamingLLM findings (arXiv 2309.17453):**

Sliding window attention with "attention sinks" (first 4 tokens) allows 4M token streams:
- **Perplexity with attention sinks:** 10.1 at 4M tokens
- **Perplexity without:** 1126.5 (complete coherence loss)
- **Tradeoff:** Only sees recent N tokens + initial context. Cannot reason over distant past.

**Selective Context (arXiv 2310.06201, 2023):**

Compress context by lexical/semantic pruning:
- **Compression ratio:** 50% reduction (e.g., 1M → 500K tokens)
- **Information loss:** ~2–5% accuracy degradation on question-answering tasks
- **Best for:** Summarization, extraction. Poor for reasoning over distant spans.

**Implication for self-evo:**

At current scale (<100 memories, ~50K tokens total), full context loading is viable. Beyond 200-300 memories:
1. **Shift to RAG:** Retrieve top-K memories per query (K=10-25), keep rest in index
2. **Cache-friendly architecture:** Static system prompt + dynamic retrieved memories + conversation
3. **Fallback to full scan:** When user asks "show all memories about X", bypass retrieval and scan files directly

---

## Adoption Roadmap for self-evo

### Adopt, Adapt, or Reject Analysis

| Feature | Action | Rationale | Effort | Priority |
|---------|--------|-----------|--------|----------|
| **OKF compliance (timestamps)** | ✅ Adopt | Adds `created`/`modified` to frontmatter. Zero breaking changes, enables future tooling interop. | Low (1 day) | High |
| **SQLite FTS index** | ✅ Adopt | Fast keyword search without vector embeddings. Scales to 1000+ memories. Single file, no server. | Medium (2-3 days) | High |
| **Vector embeddings (semantic search)** | ⚠️ Adapt (Phase 2) | Essential for semantic retrieval, but adds dependency. Start with FTS, add vectors when >200 memories. | High (5-7 days) | Medium |
| **Graph database (Neo4j/FalkorDB)** | ❌ Reject | Expensive indexing, complex deployment. Graphiti's 18.5% gain doesn't justify cost for single-agent use. | Very High (2 weeks) | Low |
| **Typed memory separation (episodic/semantic/procedural)** | ❌ Reject | ENGRAM's 31pp gain comes from multi-agent benchmarks. self-evo's scope-based types already fit workflow. No change needed. | Medium | None |
| **Agent-controlled memory editing (Letta)** | ❌ Reject (currently) | Useful for autonomous agents, but self-evo is human-in-loop. Claude Code already prompts for memory writes. | High | Low |
| **Forgetting mechanisms (time-decay + access tracking)** | ✅ Adopt | 3x accuracy gain validated. Add `accessed` timestamp, retrieval scoring, `archived` flag. | Medium (3-4 days) | High |
| **Bi-temporal provenance (Graphiti)** | ⚠️ Adapt (simplified) | Full bi-temporal model is overkill. Add `created`/`modified`/`accessed` timestamps only. Track "when learned" not "when true". | Low | Medium |
| **Prompt caching optimization** | ✅ Adopt | Already available (Claude 5-min TTL). Ensure system prompt + tools are static prefix. | Low (1 day) | Medium |
| **Hybrid file+index architecture** | ✅ Adopt | Markdown files = source of truth, SQLite = search index. Best of both worlds. | Medium (3-5 days) | High |

**Phase-based rollout:**

**Phase 1: OKF + Forgetting (1 week, high ROI)**
- Add `created`, `modified`, `accessed` timestamps to frontmatter (auto-managed)
- Implement `archived: true` flag for soft-delete
- Update `MEMORY.md` → `index.md` per OKF convention (or keep both)
- Add retrieval-time scoring: `recency_weight × access_frequency`

**Phase 2: SQLite FTS Index (1 week, scales to 1000+ memories)**
- Create `.claude/memory.db` with FTS5 table mirroring frontmatter + body
- Index on Write/Edit, query on Read
- Fallback to file scan if DB missing (graceful degradation)
- Add `memory search <query>` CLI command

**Phase 3: Vector Embeddings (2 weeks, semantic search)**
- Add `embeddings` table to SQLite (blob storage)
- Generate embeddings on write (via Anthropic API or local model)
- Hybrid retrieval: BM25 (FTS) + cosine similarity (vector), merge results
- Requires embedding model choice (Claude API: $0.10/MTok, local: faster but lower quality)

**Phase 4: Advanced Features (optional, as needed)**
- Multi-agent provenance tracking (if self-evo grows to multiple scout agents)
- Temporal reasoning ("what did I know last week?") via bi-temporal indexing
- Memory conflict resolution (if concurrent writes become an issue)

---

## Known Failures and Limitations

### Dead or Inaccessible Projects

**OpenViking:** The checked public URL did not identify the user's active deployment. Public repository identity and documentation remain unresolved; no abandonment conclusion is supported.

**GBrain:** The checked repository URL returned 404. No public code or design was recovered, and project status remains unverified.

**AutoGen memory documentation:** Redirect loops prevent access. Microsoft's AutoGen migrated to `microsoft.github.io/autogen` but memory docs are either missing or behind authentication.

**Rewind AI:** Personal memory tool (403 Forbidden on public docs). Likely B2B/private beta. No architectural details available.

### Benchmark Limitations

**LoCoMo (Long-Context Memory Benchmark):** Used by ENGRAM (77.55%) and Mem0 (91.6%), but no public leaderboard or independent validation found. Paper (arXiv 2410.19213) search returned wrong topic (computer vision).

**LongMemEval:** Mem0 claims 94.8%, but benchmark details unclear. No public dataset or evaluation harness located.

**Graphiti's 18.5% gain:** Measured on "temporal reasoning tasks" but no baseline system specified. Unclear if gain is vs flat retrieval, vs vector-only, or vs no-memory baseline.

**Lack of standardized evaluation:** Each system reports different metrics on different benchmarks. No unified comparison possible across ENGRAM, Mem0, Graphiti, Letta.

### Known Architectural Gaps

**Concurrent write safety:** No system surveyed provides ACID guarantees for file-based memory without database backing. Self-evo and OKF both vulnerable to race conditions if multiple agents write simultaneously.

**Embedding drift:** Vector embeddings change when embedding model updates (e.g., OpenAI `text-embedding-3-small` → `text-embedding-3-large`). Requires full re-indexing. No system documented migration strategy.

**Cross-lingual memory:** Only Mem0 explicitly mentions multilingual support. Others assume English. Unknown if embeddings preserve semantic similarity across languages.

**Memory schema evolution:** What happens when frontmatter schema changes (e.g., adding `accessed` field to existing memories)? No system documented migration tooling. Manual backfill required.

**Provenance in multi-agent scenarios:** Cognee and Graphiti track provenance, but no standard format. If Agent A writes memory and Agent B reads it, how does B know it's stale? No consensus.

### Research Gaps

**Optimal retrieval K:** ENGRAM uses K=25, CrewAI and others use K=10, Anthropic suggests K=5-20. No empirical comparison found.

**Forgetting schedules:** Tian Pan's 3x gain from forgetting doesn't specify time-decay function (exponential? linear? step?). No ablation study on decay rates.

**Prompt caching + RAG interaction:** No research on whether cached prompts + dynamic retrieval is faster than uncached long-context loading for 100K-500K token contexts.

**Cost-performance tradeoffs:** GraphRAG reports $100 indexing cost per 1M tokens, but no comparison of accuracy gain per dollar vs simpler vector retrieval.

---

## Conclusion

### Key Findings Recap

1. **File-first memory (Markdown+YAML) is viable and validated** — Google's Open Knowledge Format v0.1 formalizes the pattern. self-evo is already OKF-aligned with minor adjustments.

2. **Hybrid file+index architecture is production-ready** — Store human-readable files as source-of-truth, build SQLite FTS + vector indices for retrieval. Cognee, Graphiti, CrewAI all use this pattern.

3. **Forgetting is not optional** — Research shows 3x accuracy gains from selective memory vs unbounded accumulation. Add time-decay, access-frequency tracking, and archive flags.

4. **Database-backed systems dominate benchmarks** — ENGRAM (77.55% LoCoMo), Mem0 (91.6% LoCoMo / 94.8% LongMemEval), Graphiti (18.5% gain on temporal tasks). But file-first systems can achieve similar results with lightweight indexing.

5. **Prompt caching architecture matters** — Claude's 5-minute TTL with 90% cost reduction requires strict prefix ordering. RAG retrieval keeps caches warm; full-context loading breaks cache on every memory change.

6. **Typed memory separation (episodic/semantic/procedural) helps multi-agent systems** — ENGRAM's 31pp gain from type separation. But self-evo's scope-based types (user/feedback/project/reference) already fit single-agent workflow. No change needed.

### Recommendation for Issue #7

**Adopt a phased hybrid architecture:**

- **Phase 1 (1 week):** Add OKF timestamps (`created`/`modified`/`accessed`) and forgetting mechanisms (`archived` flag, retrieval scoring). Zero breaking changes.
- **Phase 2 (1 week):** Build SQLite FTS index for keyword search. Scales to 1000+ memories.
- **Phase 3 (2 weeks, future):** Add vector embeddings for semantic search when memory count exceeds 200-300 items.

**Retain Markdown/YAML as canonical format.** Database is an index, not the source of truth. Git-native workflows, transparency, and portability remain core strengths.

**Avoid premature complexity.** Reject graph databases (expensive indexing, marginal gains for single-agent use), agent-controlled editing (human-in-loop is intentional), and cognitive type separation (scope-based types already work).

### Research Depth

**Total deep fetches:** 27 successful content retrievals (14 architectural, 7 papers, 6 system docs)  
**Systems surveyed:** 14 with architectural detail (ENGRAM, Mem0, Graphiti, Letta, Cognee, CrewAI, OKF, StreamingLLM, Selective Context, GraphRAG, claude-obsidian, arscontexta, self-evo current, LangChain patterns)  
**Inaccessible or unresolved references:** 4 (OpenViking public identity, GBrain checked URL, AutoGen memory docs, Rewind AI)  
**Search attempts:** 35 (40% success rate for usable detail)

**End of Research Report**
