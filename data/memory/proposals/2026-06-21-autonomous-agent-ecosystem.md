---
title: "记忆提案：自主 Agent 生态系统结论"
date: 2026-06-21
issue: 7
type: memory_proposals
status: pending_human_review
note: "这些是合并到热记忆的候选记忆。每个包括出处和置信度。人工审查后提升。"
---

# 记忆提案：Issue #7 的持久结论

这些是值得合并到热记忆（`data/memory/hot/`）的持久结论。每个结论包括出处（来源证据）和置信度评级。仅在人工审查后提升。

**置信度标度**：
- **高**：多个主要来源、基准测试、生产证据
- **中**：单一强来源或一致的次要证据
- **低**：推断或弱支持的声明

---

## 提案记忆 1：File-First 记忆被标准验证

**Slug**：`okf-validates-file-first-memory`
**类型**：reference
**置信度**：高

**结论**：Self-evo 的 Markdown+YAML 记忆格式被 Google 的 Open Knowledge Format (OKF) v0.1（2026年6月）验证，这是 LLM 可读记忆的供应商中立标准。Self-evo 应添加 `created`/`modified` 时间戳（仅稳定内容字段）。不要添加会在读取时修改的 `accessed` 时间戳；遗忘实验的访问/使用跟踪必须使用 gitignored 索引或仅追加事件日志。

**出处**：
- OKF v0.1 规范（2026年6月）
- 研究文件：`data/exploration/raw/2026-06-21-memory-context.md`
- 与 ENGRAM、Mem0 架构交叉引用

**为何持久**：标准对齐是长期的。File-first 方法不会过时；OKF 正式化了 self-evo 已使用的模式。

**如何应用**：保持 Markdown/YAML 作为权威。添加 `created`/`modified` 时间戳到 frontmatter（稳定内容字段）。对于访问/使用统计，使用 gitignored 可重建索引（`state/memory_access.db`）或仅追加事件日志，永不在读取时修改 Markdown。不要迁移到数据库（仅使用数据库作为索引）。

---

## 提案记忆 2：Agent 框架放弃是地方性的

**Slug**：`agent-framework-abandonment-risk`
**类型**：reference
**置信度**：高

**结论**：批评者聚焦样本发现多个归档的 agent 框架，包括 Microsoft TaskWeaver 和 ACE Framework。因为样本故意偏向失败，它不建立生态系统范围的放弃率或单一原因。Self-evo 仍应在满足需求时偏好持久原语（SQLite、git、Markdown），减少依赖和迁移风险。

**出处**：
- 批评者研究：`data/exploration/raw/2026-06-21-critic-failure-landscape.md`
- 通过 GitHub 搜索识别的 30 个归档框架（偏向批评者样本，非详尽调查）
- 放弃原因的模式分析

**为何持久**：框架流失是结构性的，非暂时的。生存策略（基于原语，非基于框架）无限期适用。

**如何应用**：拒绝框架采用。使用 SQLite、git、Markdown。基础设施（Temporal、Langfuse）是长期的；agent 框架不是。

---

## 提案记忆 3：Benchmark Scores Mislead — Measure Baseline First

**Slug**：`benchmark-real-world-gap`
**类型**：reference
**置信度**：High

**结论**：Agent benchmarks show substantial benchmark-reality gaps. AgentBench paper reports 37.5% average success (Claude Opus 3) but drops to 0% on post-training Kaggle tasks. τ-bench paper shows GPT-4o <50% success, pass^8 <25% on realistic retail tasks. SWE-bench results show best autonomous agent: 43% (with test feedback), median 25-35%. Self-evo must measure single-agent baseline before assuming multi-agent value.

**出处**：
- AgentBench paper (arXiv 2308.03688)
- τ-bench paper (arXiv 2406.12045)
- SWE-bench results (source-specific, various papers/leaderboards)
- Critic research: `data/exploration/raw/2026-06-21-critic-failure-landscape.md`

**为何持久**：Benchmark-reality gap is fundamental to agent evaluation. The lesson (measure baseline before scaling) applies to all future agent work.

**如何应用**：Create self-evo-native benchmark for Issue resolution workflow (primary). Optionally use SWE-bench Verified as coding benchmark (secondary). Measure single-agent baseline before multi-agent complexity.

---

## 提案记忆 4：Cost Controls Are the Primary Failure Mode

**Slug**：`cost-controls-prevent-pilot-failure`
**类型**：project
**置信度**：Medium-High

**结论**：Runaway costs and infinite loops are primary causes of agent pilot failures. Critic found zero public GitHub issues for "agent framework cost" despite thousands of users (suggests proprietary suppression or widespread silent failures). Self-evo must build token budget enforcement, three-layer termination defense, and real-time cost monitoring BEFORE autonomous loops.

**出处**：
- Multi-agent coordination research: `data/exploration/raw/2026-06-21-multi-agent-coordination.md`
- Critic research: zero public cost issues (absence evidence)
- Cost control patterns from multiple frameworks

**为何持久**：Cost discipline is a permanent constraint for LLM agents. Token budgets and termination limits apply to all autonomous work.

**如何应用**：Implement budget enforcement (per-Issue, per-day caps), three-layer termination (depth + timeout + budget), structured local telemetry for cost tracking. Human approval above threshold.

---

## 提案记忆 5：Hierarchical Beats Swarm for Multi-Agent

**Slug**：`hierarchical-multi-agent-preferred`
**类型**：reference
**置信度**：Medium

**结论**：Production multi-agent deployments predominantly use hierarchical/sequential patterns (manager assigns tasks) over swarm (autonomous claiming). Swarm adds coordination complexity (race conditions, deadlocks) without proven benefit. Self-evo should defer multi-agent entirely until single-agent bottleneck proven, then use hierarchical, not swarm.

**出处**：
- Multi-agent coordination research: `data/exploration/raw/2026-06-21-multi-agent-coordination.md`
- Autonomous loops research: `data/exploration/raw/2026-06-21-autonomous-loops-github.md`
- Qualitative pattern analysis across frameworks

**为何持久**：Coordination pattern tradeoffs are architectural constants. Hierarchical simplicity vs swarm flexibility is a stable tradeoff.

**如何应用**：Defer multi-agent until bottleneck. When needed, use hierarchical (manager-worker). Reject swarm for MVP.

---

## 提案记忆 6：Durable Execution Is Available But Defer Until Scale

**Slug**：`durable-execution-defer-until-scale`
**类型**：reference
**置信度**：High

**结论**：Durable execution platforms (Temporal 35k★, Restate 8k★, Inngest 5k★) provide automatic retry and fault tolerance via event sourcing. Critical distinction: checkpointing (LangGraph) requires manual recovery; durable execution is automatic. But these add significant complexity (event-sourcing mindset). Self-evo's SQLite task queue is sufficient for current scale; escalate only when measured bottlenecks justify it.

**出处**：
- Autonomous loops research: `data/exploration/raw/2026-06-21-autonomous-loops-github.md`
- Multi-agent coordination research: workflow engine comparison
- Temporal/Restate architecture docs

**为何持久**：The escalation principle (SQLite → durable execution at scale) is a stable architecture decision. Platforms may evolve, but the threshold logic persists.

**如何应用**：Use SQLite task queue for MVP. Learn durable execution mental model (event sourcing). Escalate to Temporal/Restate only when measured bottlenecks justify it (cross-host coordination required, recovery pain demonstrated, or throughput/reliability limits proven).

---

## 提案记忆 7：Hybrid Memory Architecture Scales File-First

**Slug**：`hybrid-memory-file-plus-index`
**类型**：reference
**置信度**：High

**结论**：File-first memory (Markdown) scaling depends on retrieval performance (linear scan degrades with size). Production pattern: Markdown files as source of truth + SQLite FTS (keyword) + embeddings (semantic) as rebuildable gitignored index. ENGRAM reports 77.55% LoCoMo benchmark (source-specific), Mem0 reports 91.6% (source-specific). Self-evo should consider SQLite FTS only if retrieval bottleneck measured, with specific threshold determined by observed performance rather than fixed count.

**出处**：
- Memory research: `data/exploration/raw/2026-06-21-memory-context.md`
- ENGRAM paper (arXiv 2511.12960), Mem0 benchmarks (source-specific scores)
- Cognee, Graphiti architecture patterns

**为何持久**：The scaling threshold (file-only → file+index) is a stable architecture decision. The hybrid pattern (files authoritative, index rebuildable and gitignored) is production-proven.

**如何应用**：Keep Markdown canonical. Add SQLite FTS index (gitignored, rebuildable from files) only if retrieval bottleneck measured. Add embeddings if keyword search proves insufficient. Compare user's active OpenViking adapter.

---

## 提案记忆 8：Forgetting Mechanism (Experimental, Conditional)

**Slug**：`forgetting-improves-memory`
**类型**：reference
**置信度**：Low

**结论**：Unbounded memory accumulation may degrade retrieval. Research identifies potential accuracy gains from selective forgetting (time-decay + access-frequency + quality gating), with one source reporting 13% → 39% improvement (unverified; source-specific). Self-evo should evaluate reversible forgetting only if local retrieval quality problems measured, tracking access/use in gitignored index or append-only event log (NOT by mutating Markdown on read). Adopt forgetting only if local evidence shows improvement.

**出处**：
- Memory research: `data/exploration/raw/2026-06-21-memory-context.md`
- Forgetting problem analysis (one source reports 13% → 39% accuracy improvement; unverified, source-specific)
- Multiple systems implement forgetting (Mem0, Graphiti, CrewAI)

**为何持久**：The forgetting principle (selective memory may improve retrieval) is supported by cognitive science and multiple agent systems, but gains are source-specific and require local validation. The experiment design (track access without mutating files, reversible archival) is stable.

**如何应用**：Design reversible experiment only if retrieval problems measured: Add OKF timestamps (`created`, `modified` only, NOT `accessed`). Track access/use in gitignored local index (`state/memory_access.db`) or append-only event log. Score memories (time-decay + access-frequency). Archive low-scoring (reversible, manual approval required). Measure retrieval precision/recall before and after. Adopt forgetting only if local evidence shows improvement.

---

## 提案记忆 9：Observability Is Production-Ready, Build It Early

**Slug**：`observability-build-early`
**类型**：feedback
**置信度**：High

**结论**：Production observability platforms exist (Langfuse 29k★, Arize Phoenix 10k★, OpenLLMetry 7k★, AgentOps 5k★). OpenTelemetry LLM semantic conventions are standardized. Self-evo should implement local structured telemetry first (SQLite-based session/token tracking), then evaluate external platforms (Langfuse, OpenLLMetry) only after approval and comparison. Debugging non-deterministic failures and cost tracking pay back immediately.

**出处**：
- Observability research: `data/exploration/raw/2026-06-21-scouting-observability-safety.md`
- Langfuse, Arize Phoenix, OpenLLMetry repos (star counts verified)
- OpenTelemetry LLM conventions

**为何持久**：Observability platforms are infrastructure (long-lived, not agent frameworks). The principle (build observability early, local-first) is a stable engineering practice.

**如何应用**：Build local structured telemetry first (SQLite session logs, token/cost tracking). Evaluate external platforms (Langfuse for cost tracking/replay, OpenLLMetry for vendor-neutrality) only after human approval and platform comparison. Don't build custom dashboards before evaluating existing tools.

---

## 提案记忆 10：Self-Evo's Architecture Is Validated by Failures

**Slug**：`self-evo-architecture-validated`
**类型**：project
**置信度**：Medium-High

**结论**：Self-evo's core design choices (file-first, human-reviewed, GitHub-coordinated, incremental autonomy) are validated by failures of alternatives. Fully autonomous swarms show high pilot failure rates, frameworks die frequently, and benchmark-reality gaps persist. Self-evo's survival strategy: primitive-based (not framework), cost-controlled, human-gated, evidence-driven.

**出处**：
- Synthesis across all five research files
- Critic research (failures) + optimistic research (patterns)
- User preferences (executable artifacts, simple workflow, reuse mature work)

**为何持久**：The architectural validation is foundational. Self-evo's differentiators (file-first, human-review) are the reasons it can survive where others died.

**如何应用**：Resist pressure to add framework complexity. Maintain human-review gates. Build cost controls before autonomy. Measure before scaling.

**置信度警告**：This is a synthesis conclusion, not a single benchmarked claim. The component evidence is strong; the integration is reasoned inference. Treat as Medium-High.

---

## 置信度分布摘要

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

## 升级协议

**Do NOT auto-promote**. Human reviews each proposed memory before merging into `data/memory/hot/`.

**For each approved memory**:
1. Create file in appropriate `data/memory/hot/` subdirectory
2. Add frontmatter with `name`, `description`, `created`, `metadata.type`
3. Link related memories with `[[slug]]`
4. Add one-line pointer in `MEMORY.md` index

**目标路径**：
- References (#1, #2, #3, #5, #6, #7, #8): `data/memory/hot/reference/`
- Project (#4, #10): `data/memory/hot/project/`
- Feedback (#9): `data/memory/hot/feedback/`

**置信度注意**：Promote High-confidence memories first. Medium-confidence memories (#5, #8) should retain confidence caveats in their body.

---

## 研究注释：未完全解析项

**OpenViking**: Has active user deployment evidence (confirmed via exploration), but public project identity and documentation status could not be resolved during this scout run. Requires dedicated verification before citing as reference.

**GBrain**: URL checked but unavailable during this run. Status unverified.

---

**记忆提案结束**
