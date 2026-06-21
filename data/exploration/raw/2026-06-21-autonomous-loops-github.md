# Autonomous Agent Loops and GitHub-Centered Coordination: 2025-2026 Research

**Research Date:** 2026-06-21
**Researcher:** Scout Worker for self-evo Issue #7
**Scope:** Long-running autonomous agents, durable execution, GitHub as coordination plane, coding agent workflows

---

## Executive Summary

This research identifies mature patterns for autonomous agent loops and GitHub-centered coordination emerging in 2025-2026. Key findings:

1. **Durable Execution** is the critical missing piece in most agent frameworks—checkpointing alone doesn't provide automatic failure recovery
2. **GitHub as Coordination Plane** is moving from concept to production via GitHub Agentic Workflows and Copilot agent assignment
3. **Context Management** is the primary constraint for long-running coding agents, with compression triggering at ~83.5% capacity
4. **Idempotency** requires orchestration-level contracts, not just tool-level implementation
5. **Multi-Agent Orchestration** in production favors sequential and hierarchical patterns over swarm architectures (source-specific: groovyweb.co industry analysis)

---

## Search and Query Ledger

### Initial Broad Searches (Queries 1-5)

1. **"Claude Code coding agent architecture implementation"** - Discovered architecture patterns, production systems, and agent harness design
2. **"GitHub Issues PRs agent coordination workflow automation"** - Found GitHub Agentic Workflows (official), ResearchPlanAssignOps pattern, multi-agent orchestration challenges
3. **"OpenHands OpenDevin agent workflow execution"** - Identified open platform for AI software developers with stateless event-driven architecture
4. **"durable execution agents retry recovery scheduler"** - Uncovered Temporal, Conductor, DBOS, Azure Durable Task as key platforms
5. **"autonomous agent loops long-running execution 2025 2026"** - Located comprehensive guides on context overflow, drift, and economic failures

### Targeted Technical Searches (Queries 6-10)

6. **"SWE-bench agent evaluation autonomous coding"** - Found evaluation benchmarks and frontier capability assessments
7. **"GitHub Actions workflow coordination agents"** - Discovered GitHub Agentic Workflows architecture and security model
8. **"agent resumability checkpoint state persistence"** - Critical distinction between checkpointing vs. durable execution
9. **"Temporal workflow durable execution architecture 2025"** - Core concepts of event sourcing and workflow virtualization
10. **"AutoGPT autonomous agent loop implementation"** - Classic autonomous loop structure: perceive-reason-plan-act-observe

### Deep Dive on Specific Systems (Queries 11-15)

11. **"GitHub bot automation PR review coordination"** - AI-powered code review tools and automation patterns
12. **"agent failure modes error handling retry patterns"** - Exponential backoff, categorization of transient vs. permanent failures
13. **"Crew AI multi-agent orchestration workflow"** - Hierarchical manager-worker patterns for multi-agent systems
14. **"agent observability monitoring logging tracing"** - OpenTelemetry standards for AI agent observability
15. **"LangGraph agent state checkpointing production"** - Production limitations of checkpoint-based approaches

### Production Operations Focus (Queries 16-20)

16. **"agent cancellation interruption graceful shutdown"** - Partial result delivery and timeout-aware design
17. **"agent cost monitoring token usage budget control"** - Real-time cost controls and token budget management
18. **"GitHub issue automation agent assignment orchestration"** - assign-to-copilot, create-agent-session patterns
19. **"Restate durable execution workflow engine"** - Alternative to Temporal with virtual objects and durable communication
20. **"agent state machine workflow orchestration patterns"** - Five primary patterns: sequential, parallel, hierarchical, state-graph, swarm

### Detailed Implementation Patterns (Queries 21-25)

21. **"GitHub webhook agent trigger event-driven automation"** - Real-time event-driven agent triggers via webhooks
22. **"agent idempotency duplicate detection deduplication"** - Saga patterns and orchestration-level idempotency contracts
23. **"agent loop termination conditions completion detection"** - Convergence signals and no-progress detection
24. **"BabyAGI task-driven autonomous agent architecture"** - Self-prompting mechanisms and task management
25. **"agent memory persistence conversation state storage"** - Memory patterns for cross-session persistence

### Advanced Topics and Security (Queries 26-30)

26. **"GitHub GraphQL API agent automation queries"** - GraphQL advantages for agent automation
27. **"Inngest durable workflow step functions"** - Event-driven durable functions with step.run() API
28. **"agent rate limiting backoff throttling strategies"** - Multi-agent coordination challenges with shared quotas
29. **"agent context window management memory optimization"** - Hybrid memory systems, context compaction at 83.5%
30. **"agent security sandboxing isolation code execution"** - Container to microVM isolation spectrum

### Final Production Concerns (Queries 31-35)

31. **"coding agent evaluation metrics success criteria"** - Task completion, tool calling accuracy, reasoning quality
32. **"GitHub API rate limits agent automation best practices"** - 5,000 requests/hour, adaptive concurrency management
33. **"multi-agent coordination conflicts resolution GitHub PRs"** - Merge conflicts when multiple agents work same PR
34. **"agent audit trail provenance tracking"** - Decision provenance and execution tracking
35. **"agent human-in-the-loop approval patterns interruption"** - Approval workflows for consequential actions

### Deep Content Fetches (5 articles)

- **Temporal: Durable Execution for AI** - State management, automatic resilience, checkpointing
- **Restate: What is Durable Execution** - Journaling system, virtual objects, three dimensions of durability
- **GitHub Agentic Workflows** - Markdown-based workflow definitions, security architecture
- **OpenHands ArXiv Paper** - Platform capabilities and multi-agent coordination
- **LangGraph Persistence** - SqliteSaver, PostgresSaver, checkpoint bloat issues

### Additional Deep Fetches (10 articles)

- **Checkpoints vs Durable Execution** - Critical production gap analysis
- **Temporal: What is Durable Execution** - Core principles and guarantees
- **Agent Termination Conditions** - Convergence signals and three-layer defense
- **Long-Running Coding Agents Guide** - Context overflow, drift, token cost explosion
- **Idempotency in Agentic Tool Calling** - Saga patterns and compensation
- **GitHub Copilot Issue Assignment** - Limited architectural detail
- **ResearchPlanAssignOps Pattern** - Four-phase development with human checkpoints
- **Multi-Agent Orchestration Patterns** - Build cost and production usage statistics
- **OpenTelemetry Agent Observability** - Standardized telemetry conventions

---

## Source Screening Table

| # | Source | Type | Date | Keep/Reject | Reason |
|---|--------|------|------|-------------|---------|
| 1 | [Temporal: Durable Execution for AI](https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai) | Vendor Blog | 2025 | **KEEP** | Primary source on durable execution for agents, production patterns |
| 2 | [Restate: What is Durable Execution](https://restate.dev/what-is-durable-execution/) | Vendor Docs | 2025-2026 | **KEEP** | Alternative approach, virtual objects architecture |
| 3 | [GitHub Agentic Workflows](https://github.github.com/gh-aw/) | Official Docs | 2026 | **KEEP** | Official GitHub agent coordination system, public preview |
| 4 | [OpenHands ArXiv](https://arxiv.org/abs/2407.16741) | Academic | 2024 | **KEEP** | ICLR 2025 accepted, community-driven platform |
| 5 | [Diagrid: Checkpoints Are Not Durable Execution](https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows) | Analysis | 2026 | **KEEP** | Critical gap analysis, production failure modes |
| 6 | [Long-Running Coding Agents Guide](https://o-mega.ai/articles/long-running-coding-agents-the-2026-guide) | Industry Guide | 2026 | **KEEP** | Empirical findings on context management, 52-hour sessions |
| 7 | [Tian Pan: Agent Idempotency](https://tianpan.co/blog/2026-04-19-idempotency-agentic-tool-calling-saga-deduplication) | Technical Blog | 2026-04 | **KEEP** | Detailed idempotency patterns, saga compensation |
| 8 | [Tian Pan: Agent Termination](https://tianpan.co/blog/2026-05-07-tool-call-convergence-agents-stopping-criteria) | Technical Blog | 2026-05 | **KEEP** | Production termination patterns, convergence signals |
| 9 | [ResearchPlanAssignOps Pattern](http://github.github.com/gh-aw/patterns/research-plan-assign-ops/) | Official Pattern | 2026 | **KEEP** | Four-phase GitHub coordination pattern |
| 10 | [Multi-Agent Orchestration Patterns](https://www.groovyweb.co/blog/multi-agent-orchestration-patterns-supervisor-router-pipeline-swarm-2026) | Industry Analysis | 2026 | **KEEP** | Build costs, sequential/hierarchical prevalence in production |
| 11 | [OpenTelemetry: AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/) | Standards Doc | 2025 | **KEEP** | Emerging observability standards |
| 12 | [LangGraph Persistence Guide](https://markaicode.com/langgraph-persistence-checkpointing-workflows/) | Technical Guide | 2026 | **KEEP** | Production limitations of checkpointing |
| 13 | [Inngest: Durable AI Agents](https://www.inngest.com/blog/ai-agents-inngest-durable-steps) | Vendor Blog | 2025-2026 | **KEEP** | Event-driven step functions approach |
| 14 | [GitHub: Rate Limiting Controls](http://github.github.com/gh-aw/reference/rate-limiting-controls/) | Official Docs | 2026 | **KEEP** | Defense-in-depth for agent automation |
| 15 | [Multi-Agent PR Conflicts](https://medium.com/@nivedv/when-two-agents-work-the-same-pr-multi-agent-orchestration-in-github-fb77f38b3d95) | Case Study | 2025-2026 | **KEEP** | Real coordination challenges |
| 16 | [Tian Pan: Agent Sandboxing](https://tianpan.co/blog/2026-03-09-agent-sandboxing-secure-code-execution) | Technical Blog | 2026-03 | **KEEP** | Security isolation spectrum |
| 17 | [Context Engineering for Agents](https://tianpan.co/blog/2026-02-23-effective-context-engineering-for-ai-agents) | Technical Blog | 2026-02 | **KEEP** | Context window management patterns |
| 18 | [Anthropic: Context Engineering Cookbook](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) | Official Docs | 2025-2026 | **KEEP** | Compression at 83.5% capacity |
| 19 | [Agent Memory Patterns](https://understandingdata.com/posts/agent-memory-patterns/) | Technical Guide | 2025-2026 | **KEEP** | Checkpoint, resume, state persistence patterns |
| 20 | AutoGPT various sources | Multiple | 2023-2024 | REJECT | Superseded by newer architectures, early experimental phase |
| 21 | BabyAGI sources | Multiple | 2023-2024 | REJECT | Historical interest only, limited production deployment |
| 22 | CrewAI marketing materials | Vendor | 2025-2026 | REJECT | Heavy on marketing, light on architectural detail |
| 23 | Various "how to build" tutorials | Tutorial | 2025-2026 | REJECT | Basic patterns only, not production-grade |
| 24 | Generic AI agent explainers | Blog | 2025-2026 | REJECT | Conceptual overviews without technical depth |

**Screening criteria:**
- **Keep:** Official documentation, technical blogs with primary evidence, academic papers, production case studies, vendor docs with architectural detail
- **Reject:** Marketing-heavy content, superseded early experiments, basic tutorials, conceptual overviews without implementation detail

---

## Deep Analysis: Leading Systems

### 1. Durable Execution Platforms

#### Temporal

**Architecture:** Event-sourced workflow engine that virtualizes execution across processes and machines. Workers execute workflow code; the Temporal Server maintains durable event history.

**Key Mechanism:** Every workflow step is recorded to an event log. When a process crashes, a new worker reconstructs full state from the log and continues execution from the exact point of failure.

**Core Guarantees:**
- Variables maintain values across crashes (automatic state preservation)
- Execution continues until completion (time unlimited—seconds to years)
- No single process needs to stay running for entire duration
- Hardware agnostic—works on commodity infrastructure

**AI Agent Use Case:** Temporal addresses "distributed systems on steroids" problems where agents make far more external calls than traditional apps. Automatic resilience handles network glitches and rate-limiting without developer-written retry logic. Workers efficiently manage hundreds or thousands of concurrent workflows.

**Production Pattern Example:** IT support workflow processing Slack → LLM analysis → ServiceNow ticket → human approval → infrastructure provisioning as single reliable flow.

**Source:** [Temporal Blog: Durable Execution Meets AI](https://temporal.io/blog/durable-execution-meets-ai-why-temporal-is-the-perfect-foundation-for-ai) | [What is Durable Execution](https://temporal.io/blog/what-is-durable-execution)

**Technical Limitation:** Requires running Temporal Server infrastructure. Programming model requires wrapping application logic in Temporal-specific workflow and activity constructs.

---

#### Restate

**Architecture:** Journaling system where Restate Server acts as proxy managing persistent logs while services run on existing infrastructure using lightweight SDKs.

**Differentiator:** Extends durability across three dimensions:
1. **Durable execution** - steps journaled for replay
2. **Durable communication** - messages survive crashes on sender and receiver
3. **Virtual objects** - per-key state with built-in concurrency control

**Technical Approach:** Eliminates need for separate lock services or transactional outbox patterns. Positions itself as providing "expressiveness of code with reliability guarantees of workflow engine."

**Performance:** p99 latency under 100ms for 10-step workflows. Supports TypeScript, Python, Java/Kotlin, Go, Rust.

**Use Cases:**
- Multi-step business processes (seconds to weeks)
- Microservice orchestration with consistency guarantees
- Async task scheduling with fan-out/fan-in
- Exactly-once event processing
- AI agent multi-tool loops where each LLM call must survive failures

**Source:** [Restate: What is Durable Execution](https://restate.dev/what-is-durable-execution/)

**Trade-off:** Newer platform (less mature ecosystem than Temporal). Virtual objects model requires understanding of per-key concurrency semantics.

---

#### Inngest

**Architecture:** Event-driven platform with step functions using explicit `step.run()` API. Each step executes independently, caches results, and retries on failure without re-executing previous steps.

**Key Pattern:** Functions pause between steps rather than holding compute resources. Platform records each step's state, enabling failed work to retry from last successful checkpoint.

**Programming Model:** Written in standard TypeScript, Python, or Go. Wrap logic with Inngest trigger/execution metadata, expose via `serve()` or `Connect`. Platform handles invocation from its infrastructure while code runs on your compute.

**Advantages:**
- Explicit step IDs create transparent execution model (no build-time transformation)
- Compute and language agnostic
- Built-in flow control and observability

**AI Agent Application:** LLM calls, tool executions, and data operations each become durable steps. Lead enrichment pipelines with step-level checkpointing.

**Source:** [Inngest: Durable AI Agents](https://www.inngest.com/blog/ai-agents-inngest-durable-steps) | [Inngest Platform](https://www.inngest.com/platform)

**Consideration:** Requires adopting Inngest's event-driven model and hosting approach. Less suitable for purely synchronous workflows.

---

#### Critical Gap: Checkpointing vs. Durable Execution

**The Core Distinction:** Checkpointing provides state snapshots; durable execution guarantees workflows run to completion.

**What Checkpointing Provides:**
- Snapshot of state at specific points
- Manual recovery capability

**What Checkpointing Does NOT Provide:**
- Automatic failure detection (no watchdog/heartbeat)
- Automatic recovery (developer must detect, retrieve workflow ID, reinvoke)
- Duplicate prevention (no coordination to prevent simultaneous recovery attempts)
- Distributed task queue (single-process execution)

**Production Consequence:** At scale, requires "building an entire failure-detection-and-retry infrastructure yourself."

**Framework-Specific Limitations:**

**LangGraph:**
- Checkpoints save state but "makes you the orchestrator"
- No supervisor process to restart failed workflows
- Thread IDs accumulate hundreds of checkpoints requiring manual pruning
- Security issue: entire StateGraph serialized as plaintext (API keys, tokens, PII exposed)

**CrewAI:**
- `@persist` decorator saves state but "nobody restarts the flow" on crash
- No durability for autonomous agents

**Google ADK:**
- Event sourcing architecture but "caller is responsible for detecting failure and re-invoking"

**Quote from Analysis:** "The difference is between saving state and guaranteeing completion. Production needs automatic recovery where the reminder automatically reactivates the workflow and retries indefinitely, without any human or external system intervention."

**Source:** [Diagrid: Why Checkpoints Are Not Durable Execution](https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows)

**Implications for self-evo:** If building on LangGraph or similar, must implement separate supervisor process with failure detection, workflow recovery, and duplicate prevention. Consider durable execution platforms for truly autonomous long-running agents.

---

### 2. GitHub as Coordination Plane

#### GitHub Agentic Workflows

**Status:** Public Preview (2026), "may change significantly"

**Core Concept:** "Intelligent automation for GitHub" that runs AI coding agents within GitHub Actions using markdown-based workflow definitions instead of traditional YAML. Described as adding "Continuous AI" capabilities to traditional CI/CD.

**Architecture:**

**Workflow Definition:** Plain markdown describing desired automation → `gh aw` CLI compiles to hardened GitHub Actions workflows

**Supported AI Engines:** GitHub Copilot, Claude, Gemini, OpenAI Codex

**Execution Environment:** Sandboxed containers behind "Agent Workflow Firewall"

**Security Model (Layered Defense):**
1. Agents receive read-only tokens
2. Cannot directly push commits or modify issues
3. Secrets isolated in separate jobs (not in agent process)
4. All proposed actions pass through "Safe Outputs Gate" for validation
5. Dedicated threat detection job scans outputs before application
6. Compile-time validation catches misconfigurations

**Key Features:**
- Natural language workflow definitions
- Deep GitHub integration (Issues, PRs, Discussions, repository management)
- Cost management with per-run AI credit budgets
- OpenTelemetry export for observability
- Use cases: issue triage, documentation maintenance, CI diagnostics, daily reports

**Rate Limiting Controls:**
- Concurrency limits
- Timeouts
- Read-only agents when possible
- Safe output limits
- Built-in delays
- Manual review gates

**Source:** [GitHub Agentic Workflows](https://github.github.com/gh-aw/) | [Rate Limiting Controls](http://github.github.com/gh-aw/reference/rate-limiting-controls/)

**Production Readiness:** Preview status indicates API stability not guaranteed. Security architecture suggests enterprise-grade thinking, but real-world adoption data not yet available.

---

#### ResearchPlanAssignOps Pattern

**Pattern Type:** Four-phase development workflow from automated discovery to merged code with human control at decision points.

**Phase 1 - Research:**
- Scheduled workflow analyzes codebase
- Publishes findings as GitHub Discussion
- Discussion serves as "contract between research phase and everything that follows"
- Configuration: `schedule: daily on weekdays`, `cache-memory` for progress tracking, `create-discussion` safe-output

**Phase 2 - Plan:**
- Developer triggers `/plan` command on research discussion
- Workflow extracts concrete work items
- Creates up to 5 sub-issues grouped under parent tracking issue
- Configuration: Command-triggered, `create-issue` with `group: true`

**Phase 3 - Assign:**
- Issues assigned to GitHub Copilot (manually via UI or automatically via `assignees: copilot`)
- Copilot opens PR and posts progress updates
- Agent works like human developer: create branch → work → submit PR

**Phase 4 - Merge:**
- Human maintainer checks correctness, runs tests
- Merges when satisfied
- Parent tracking issue auto-closes when all sub-issues resolve

**Coordination Mechanism:**
- Each phase produces artifacts: discussions → issues → PRs
- "Every transition is a human checkpoint"
- State tracked in native GitHub primitives (not external database)

**Source:** [ResearchPlanAssignOps Pattern](http://github.github.com/gh-aw/patterns/research-plan-assign-ops/)

**Reusable for self-evo:** Pattern directly applicable. Could automate research phase as scheduled agent, use issues for task tracking, assign sub-tasks to worker agents, maintain human review gates.

---

#### GitHub Copilot Agent Assignment

**Mechanism:** Issues can be assigned directly to Copilot like a human developer.

**Workflow Actions:**
- `assign-to-agent` - Programmatically assigns Copilot to existing issues/PRs
- `create-agent-session` - Spawns new Copilot sessions for specific tasks

**Authentication:** Requires fine-grained personal access tokens

**Execution:** "Copilot will start working on the task in the background." Creates branch, implements changes, submits PR for review.

**Automation Trigger:** Can be configured to trigger "in response to events such as an issue being opened"

**Source:** [GitHub Copilot: Using Copilot to Work on an Issue](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/using-copilot-to-work-on-an-issue) | [GitHub Agentic Workflows: Assign to Copilot](http://github.github.com/gh-aw/reference/assign-to-copilot/)

**Limitation:** Documentation light on architectural details, error handling, retry behavior, and cost controls for autonomous assignment.

---

#### Multi-Agent Coordination Challenges

**Problem:** When multiple agents work on the same PR simultaneously, they can create separate PRs modifying overlapping files without awareness of each other, causing merge conflicts.

**Current State:** "Current approaches typically involve humans routing different issues to specialized agents that work in isolation and create separate PRs, with limited agent-to-agent communication."

**Coordination Gap:** No built-in mechanism prevents two agents from both attempting to fix the same issue or modifying same files in incompatible ways.

**Source:** [Medium: When Two Agents Work the Same PR](https://medium.com/@nivedv/when-two-agents-work-the-same-pr-multi-agent-orchestration-in-github-fb77f38b3d95)

**Implication for self-evo:** Need explicit task assignment tracking in Issues with claimed/in-progress states. Consider file-level or module-level locking if parallel agents work on same codebase.

---

### 3. Long-Running Coding Agent Architectures

#### The Three Failure Modes

**Context Overflow:** "The window fills, the agent loses access to information it needs." Each action (read file, run test, iterate) consumes tokens until context exhausted.

**Context Drift:** "The agent can still see its recent actions but has lost the original intent." Gradual deviation from goals stated early in multi-hour sessions.

**Token Cost Explosion:** "The economic failure" - coherent agents generating costs that don't justify output over 8+ hour runs.

**Source:** [Long-Running Coding Agents: The 2026 Guide](https://o-mega.ai/articles/long-running-coding-agents-the-2026-guide)

---

#### Production Architecture Patterns

**1. Context Compression & Memory Systems**

**Anthropic's Approach:**
- Compaction triggers at approximately **83.5% of context window**
- Trigger point determined empirically—degradation begins before advertised limit
- Converts lengthy conversation history into condensed summaries
- Tool-result clearing removes bloat from previous executions

**Mem0 Results:**
- Achieves **90% fewer tokens** through memory extraction
- Modest accuracy cost trade-off
- Enables continued operation where naive context would overflow

**Focus Architecture:**
- Retains only conclusions from investigations
- Discards full exploration traces
- Prevents context pollution with intermediate failed attempts

**Key Insight:** "Most models degrade well before their advertised limit—typically losing coherence around 65-85% of nominal capacity. A 1M-token window provides perhaps 3-4x the runtime of 200K, not the 5x raw numbers suggest."

**Source:** [Anthropic: Context Engineering](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) | [Long-Running Coding Agents Guide](https://o-mega.ai/articles/long-running-coding-agents-the-2026-guide)

---

**2. Parallel Decomposition**

**Pattern:** Rather than one agent for 10 hours, run 5 parallel agents for 2 hours each.

**Cursor's Approach:** Planner-worker pipeline
- Planners create task specifications
- Workers execute independently without coordination overhead
- Each worker has bounded scope and clean success criteria

**Benefits:**
- Faster wall-clock time
- Natural isolation boundaries
- Individual worker failures don't cascade
- Can scale by adding more workers

**Trade-offs:**
- Planning overhead
- Merge complexity for interdependent changes
- Need task decomposition that produces genuinely independent work

---

**3. Tool-Mediated Interaction (MCP Pattern)**

**Problem:** Raw data flooding context (e.g., reading entire database dump)

**Solution:** MCP (Model Context Protocol) servers process data and return concise results

**Efficiency Gain:** 10-100x reduction in context usage for data-heavy operations

**Example:** Instead of agent receiving 50MB JSON response, MCP server filters/aggregates and returns 500KB summary

**Source:** General industry pattern, multiple implementations

---

**4. Isolation Strategies**

**Cloud Sandboxes:**
- Codex, Cursor provide clean execution environments per task
- Prevents error propagation
- Fresh state for each major subtask

**Worktree Isolation:**
- Give subagents separate git branches in isolated worktrees
- Parallel modifications don't conflict at filesystem level
- Can work on incompatible approaches simultaneously

**Containerization:**
- Each agent in own container with limited resources
- Security boundary for code execution
- Resource limits prevent runaway processes

**Key Principle:** "Each isolation layer prevents error propagation across parallel work."

---

**5. Periodic Fresh Starts**

**Cursor's Discovery:** "Periodic fresh starts are essential to combat drift and tunnel vision even with large contexts."

**Phenomenon:** Agents develop inaccurate beliefs about codebases during extended runs. These beliefs compound over time, leading to incorrect assumptions in later steps.

**Solution:** Explicitly terminate long-running sessions and start fresh agents with:
- Accumulated learnings stored in external memory
- Clear objective derived from previous session's output
- Clean context without historical baggage

**Evaluation Pattern:** Use separate evaluation model (e.g., Haiku for Claude-generated code) rather than letting "working model grade its own homework." Prevents premature completion claims.

---

**6. Heterogeneous Model Teams**

**Finding:** "Experiments found specific models excel at planning vs implementation, suggesting heterogeneous model teams outperform single-model approaches."

**Pattern:**
- Strong reasoning model (Opus, O1) for planning and architecture
- Fast efficient model (Sonnet, GPT-4) for implementation
- Lightweight model (Haiku, GPT-3.5) for evaluation and validation

**Economic Benefit:** Matches model cost to task complexity. Don't pay Opus prices for routine implementation once plan is solid.

---

**Production Viability Criteria:**

**Time Test:** Agent must complete work that would take humans longer than session duration

**Cost Test:** Agent cost must be lower than equivalent engineer time

**Quality Gap:** "The gap between 'agent produced a working prototype' and 'agent produced production-ready, maintainable, secure code' remains the critical test."

**Early Evidence:** 52-hour agent sessions producing functional implementations show promise, but production-grade code quality still requires significant human review.

**Winning Pattern Summary:** "Combines large context windows for resilience with aggressive tool usage for efficiency, parallel decomposition for speed, and cross-session memory for accumulated expertise."

---

### 4. Multi-Agent Orchestration Patterns

#### Five Primary Patterns (with Production Usage Data)

**1. Sequential (Pipeline)**
- **Structure:** Linear execution A→B→C, output of one becomes input of next
- **Build Cost:** $30-50K
- **Complexity:** Simplest to build and debug
- **Failure Mode:** Single agent failure stops entire pipeline
- **Best For:** Tasks with natural ordering (research → draft → review)
- **Production Usage:** ~40% of deployments

**2. Parallel (Concurrent)**
- **Structure:** Multiple agents run simultaneously, results merged
- **Build Cost:** $50-90K
- **Benefits:** Faster wall-clock time
- **Challenges:** Merge-logic complexity, race conditions
- **Best For:** Independent subtasks (querying multiple data sources)
- **Production Usage:** ~15% of deployments

**3. Hierarchical (Supervisor)**
- **Structure:** Manager agent delegates to specialist agents
- **Build Cost:** $60-110K
- **Benefits:** Clear decision authority, specialized agents
- **Challenges:** Manager bottlenecks
- **Best For:** Customer support (route tickets to specialists)
- **Production Usage:** ~30% of deployments

**4. State-Graph**
- **Structure:** Explicit state machines with conditional transitions
- **Build Cost:** $70-130K
- **Benefits:** Human-in-loop checkpoints, conditional flows
- **Challenges:** Harder to debug, requires state replay
- **Best For:** Workflows where next step depends on intermediate state
- **Production Usage:** ~10% of deployments

**5. Swarm (Peer-to-peer)**
- **Structure:** Agents negotiate without fixed orchestrator
- **Build Cost:** $90-180K
- **Complexity:** Highest build complexity, most non-deterministic
- **Challenges:** Very hard failure recovery, unpredictability
- **Best For:** Theoretical flexibility
- **Production Usage:** ~5% of deployments

**Key Finding (source-specific: groovyweb.co):** "Sequential and hierarchical dominate in 2026—together about 70% of production orchestrations because predictability trumps flexibility in real deployments."

**Source:** [Multi-Agent Orchestration Patterns 2026](https://www.groovyweb.co/blog/multi-agent-orchestration-patterns-supervisor-router-pipeline-swarm-2026)

**Implication for self-evo:** Start with sequential or hierarchical. Swarm architectures are research curiosities, not production patterns. State-graph useful if human review gates needed.

---

#### State Management Requirements

**Critical Components:**
- **State persistence** - Maintain context across asynchronous operations
- **Checkpoints** - Enable recovery from mid-workflow failures
- **Bounded context windows** - Explicit read/write permissions per agent
- **Human-in-loop integration** - Decision points for critical actions

**LangGraph in Production:** Currently used at Uber, LinkedIn, Klarna for state-machine orchestration.

**Architecture Warning:** "Microsoft's guidance emphasizes using the simplest pattern that meets requirements, as each complexity level adds coordination overhead, latency, and cost."

**Failure Source:** "Research from Anthropic's analysis of enterprise deployments found that 57% of project failures originated in orchestration design rather than individual agent capabilities."

**Source:** [LangGraph Workflows State Machines](https://jetthoughts.com/blog/langgraph-workflows-state-machines-ai-agents/) | [Microsoft: AI Agent Design Patterns](http://docs.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

---

### 5. Agent Loop Termination and Convergence

#### The Core Problem

"Agents need explicit stopping criteria since models default to doing more." Without proper termination conditions, agents loop indefinitely or burn excessive resources on diminishing returns.

**Key Principle:** "Convergence is not a model capability problem—you must build stopping criteria the model doesn't have."

---

#### Convergence Signals

**1. Diminishing Returns Detection**
- **Metric:** "What new evidence was gained in this step?"
- **Threshold:** When information gain falls below minimum threshold
- **Application:** Research and data gathering tasks

**2. No-Progress Detection**
- **Pattern:** Same tool with same arguments twice → trigger self-correction
- **Hard Stop:** Third identical call → force stop
- **Rationale:** Agent is stuck in local minimum

**3. Coverage Thresholds**
- **Heuristic:** "Beyond three retrieval cycles, the probability of finding genuinely new information approaches zero"
- **Application:** Search and retrieval workflows
- **Empirical Basis:** Diminishing marginal returns on additional queries

**4. Confidence Convergence**
- **Method:** Run final synthesis twice with different random seeds
- **Criteria:** If outputs agree semantically, task is complete
- **Application:** Ensures stability of conclusions

---

#### Framework Termination Contracts

**LangChain:**
- `max_iterations` (default: 15)
- Hard iteration limit

**AutoGen (Composable):**
- `MaxMessageTermination` - conversation length limit
- `TokenUsageTermination` - budget-based stop
- `TimeoutTermination` - wall-clock limit
- `TextMentionTermination` - keyword-triggered completion

**Cost-Based:**
- **Soft limit:** Alert when approaching budget, continue cautiously
- **Hard limit:** Force synthesis with existing context when budget exhausted

---

#### Three-Layer Defense Architecture

**Layer 1 - Policy Gate (Before Execution):**
- Define budgets (token, time, API calls)
- Set permissions (allowed tools, data access)
- Establish risk rules (no destructive operations without approval)

**Layer 2 - Bounded Planning:**
- Generate fixed-step plan upfront
- Avoid open-ended loops
- Clear success criteria per step

**Layer 3 - Executor with Runtime Checks:**
- Apply convergence heuristics during execution
- Monitor for repetition patterns
- Emergency stops for runaway behavior

---

#### Production Minimum Requirements

1. **Cap retrieval at 3 iterations** - empirically derived threshold
2. **Detect tool repetition** - same tool + args = self-correct, then stop
3. **Monitor step count distribution** - if p95 exceeds 4x p50, convergence issues exist
4. **Set token/cost budgets** - both soft (alert) and hard (terminate) thresholds
5. **Implement timeout fallbacks** - deliver partial results instead of silent failure

**Quote:** "Beyond three retrieval cycles, the probability of finding genuinely new information approaches zero."

**Source:** [Tian Pan: Tool Call Convergence and Agent Stopping Criteria](https://tianpan.co/blog/2026-05-07-tool-call-convergence-agents-stopping-criteria)

---

### 6. Idempotency and Duplicate Prevention

#### The Structural Problem

"Agent tool calling faces idempotency challenges because frameworks retry at the LLM layer without tracking whether side effects already executed."

**Failure Scenario:**
1. Agent calls payment API
2. API returns 200 (payment processed)
3. Network timeout before confirmation stored
4. Agent framework retries
5. Payment runs again → duplicate charge

**Core Issue:** "The agent that generated the duplicate charge was following instructions correctly—it genuinely didn't know the first call succeeded." Prompt engineering cannot fix missing external state.

---

#### Three-Layer Solution

**Layer 1 - Agent Runtime:**
- Generate idempotency keys from durable state
- Format: `{workflowRunId}:{stepId}`
- Keys must be stable across retries

**Layer 2 - Tool Execution:**
- Check deduplication store before executing
- Cache results keyed by idempotency key
- Return cached result if key exists

**Layer 3 - Tool Interface:**
- Accept idempotency keys as parameters
- Implement deduplication logic at API boundary
- Use database constraints or distributed locks

**Critical Property:** "This enables aggressive retries while ensuring the economic result—one charge, one record, one email—matches the agent's intent."

---

#### Saga Pattern for Multi-Step Workflows

**Concept:** Each step has reversing action (compensation)

**Example:**
- Forward: Reserve inventory → Charge payment → Send confirmation
- Compensation: Release reservation ← Refund payment ← Cancel confirmation

**Execution:** If confirmation fails after payment succeeds, "saga executor runs compensating actions in reverse order."

**Implementation Requirement:** "Compensating actions must themselves be idempotent to avoid refund loops."

**Use Case:** Long-running business processes where partial completion must be cleanly unwound.

---

#### Orchestration-Level Contract

**Key Insight:** "Agent idempotency is an orchestration contract, not a tool property."

**Requirement:** Orchestrator (workflow engine, agent runtime) must:
- Generate stable identifiers for each step
- Pass identifiers to tool calls
- Track completion state durably
- Coordinate retries at workflow level

**Anti-Pattern:** Expecting individual tools to handle idempotency without orchestration support. Tools need workflow context to deduplicate correctly.

**Source:** [Tian Pan: Idempotency in Agentic Tool Calling](https://tianpan.co/blog/2026-04-19-idempotency-agentic-tool-calling-saga-deduplication) | [Agent Idempotency as Orchestration Contract](https://tianpan.co/blog/2026-04-23-agent-idempotency-orchestration-contract)

---

### 7. Observability and Monitoring

#### Why Agent Observability Differs

Traditional monitoring tracks system health (uptime, CPU, latency). Agent observability must also capture:
- **Reasoning processes** - why agent made specific decisions
- **Tool call chains** - multi-step execution traces
- **Non-deterministic behavior** - same input may yield different outputs
- **Context utilization** - how much of context window consumed
- **Quality metrics** - not just performance but correctness

**Critical Question:** "When autonomous agents fail or behave unexpectedly, observability helps answer why the agent made specific decisions."

---

#### Core Observability Components

**Tracing:**
- Capture multi-step reasoning chains as structured spans
- Critical for debugging non-deterministic behavior
- Foundation of agent observability

**Monitoring:**
- System health (traditional metrics)
- Agent-specific: reasoning quality, context utilization, tool success rates

**Logging:**
- Comprehensive record of agent actions
- Model calls with inputs/outputs
- Tool executions with parameters and results
- Enables post-hoc analysis

---

#### OpenTelemetry Standards (Emerging)

**Status:** GenAI SIG actively defining semantic conventions for:
- LLM calls and responses
- Vector database operations
- Agent workflow traces
- Multi-agent coordination

**Goals:**
- Standardized telemetry across frameworks
- Avoid vendor lock-in
- Enable consistent monitoring/debugging

**Dual Purpose:**
1. Operational troubleshooting (traditional)
2. Continuous improvement feedback loop (unique to AI)

**Framework vs Application Separation:**
- Application level: Individual agent behavior
- Framework level: Infrastructure managing agents
- Both need observability with appropriate conventions

**Source:** [OpenTelemetry: AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/)

**Maturity:** Standards still evolving. Expect changes through 2026 as patterns solidify.

---

### 8. Security and Sandboxing

#### The Isolation Spectrum

Agent-generated code execution requires isolation beyond basic containers. Multiple technologies provide different security guarantees:

**Standard Containers (Docker):**
- Process isolation
- Namespace separation
- Not designed for adversarial workloads

**gVisor:**
- Lightweight virtualization
- Application kernel in userspace
- Better isolation than containers

**Firecracker (MicroVMs):**
- Minimal virtual machines
- Hardware-level isolation
- Used by AWS Lambda
- ~125ms cold start

**WebAssembly (Wasm):**
- Sandboxed by design
- Near-native performance
- Limited system access

**Security Finding:** "88% of organizations experienced confirmed or suspected AI agent security incidents in past year" (source survey data)

**OWASP Classification:** Agentic Top 10 lists Unexpected Code Execution as control requiring sandboxing.

---

#### What Sandboxing Controls

Complete execution boundary management:
- **Filesystem access** - read/write permissions per directory
- **Network** - allowed endpoints, protocols
- **Secrets** - which credentials agent can access
- **File movement** - prevent exfiltration
- **Execution time** - resource limits
- **Review processes** - human approval for risky operations

**Key Principle:** "Isolation restricts these capabilities independently of the agent's own decisions."

---

#### Specific Threats from Agent-Generated Code

- Exfiltrate environment variables to external servers
- Write malicious files to arbitrary disk locations
- Establish outbound network connections for C2
- Escape to host system without proper containment
- Consume unbounded resources (CPU, memory, disk)

**Production Pattern:** Defense in depth with multiple layers:
1. Sandboxed execution environment (Firecracker/gVisor)
2. Network egress filtering
3. Filesystem mount restrictions
4. Resource quotas
5. Human approval for sensitive operations

**Source:** [Tian Pan: Agent Sandboxing](https://tianpan.co/blog/2026-03-09-agent-sandboxing-secure-code-execution) | [AI Agent Sandbox Architecture](https://medium.com/towards-artificial-intelligence/ai-agent-sandbox-architecture-how-to-let-agents-run-code-without-letting-them-run-everything-63a9293c35fb)

---

### 9. Rate Limiting and Cost Control

#### GitHub API Limits

**REST API Rate Limits:**
- Standard authenticated: 5,000 requests/hour
- Enterprise audit logs: 1,750 queries/hour per user/IP
- Git LFS: 3,000 requests/minute (authenticated), 300 (unauthenticated)

**Response Codes:** 403 or 429 when limits exceeded

**Source:** [GitHub: Rate Limits for REST API](https://docs.github.com/rest/overview/rate-limits-for-the-rest-api)

---

#### Best Practices for Agent Automation

**1. Defense-in-Depth Controls:**
- Concurrency limits (max parallel requests)
- Timeouts (prevent hanging)
- Read-only agents when possible
- Safe output limits (bounded result sizes)
- Built-in delays between operations
- Manual review gates for sensitive actions

**2. Observe-Baseline-Refine-Maintain Approach:**
- Enable log forwarding to analyze traffic patterns
- Establish baseline limits (start high)
- Refine based on actual usage
- Continuously monitor and adjust

**3. Proper Error Handling:**
- Detect rate limit responses (403, 429)
- Implement automatic retry with exponential backoff
- Add jitter to prevent thundering herd

**4. Adaptive Concurrency:**
- AIMD-based (Additive Increase Multiplicative Decrease)
- Request prioritization (critical vs. background)
- SLO-driven alerting

**5. Multi-Agent Coordination:**
- Centralized rate limit management
- Shared quota awareness
- Priority-based scheduling

**Challenge:** "9 AI Agents, One API Quota—The Rate Limiting Problem Nobody Talks About"

**Quote:** "When multiple agents share one API quota, this becomes a coordination challenge requiring centralized rate limit management rather than just retry logic."

**Source:** [GitHub Agentic Workflows: Rate Limiting Controls](http://github.github.com/gh-aw/reference/rate-limiting-controls/) | [GitHub: Best Practices for API Rate Limits](https://docs.github.com/en/enterprise-server@3.20/admin/configuring-settings/configuring-user-applications-for-your-enterprise/best-practices-for-configuring-api-rate-limits)

---

#### Token Budget Management

**Real-Time Cost Controls:**
- Track token usage per agent, per workflow, per task
- Set soft limits (alerts) and hard limits (termination)
- Attribution: which agent/task consumed which tokens
- Predictive: estimate cost before execution

**Budget-Aware Patterns:**
- Dynamic loops: `while budget.remaining() > threshold`
- Static scaling: `agents_to_spawn = budget.total / cost_per_agent`
- Graceful degradation: reduce quality when budget low

**Cost Management Architecture:**
- Centralized tracking (not per-agent accounting)
- Shared pool with allocation policies
- Priority-based spending (critical tasks first)

**Source:** [Agent Token Budget Management](https://microsoft.github.io/agent-governance-toolkit/tutorials/24-cost-and-token-budgets/) | [Budget-Aware Tool-Use](https://arxiv.org/html/2511.17006v1)

---

## Operational Failures and Hidden Costs

### Context Window Management

**Hidden Cost:** "Even coherent agents can generate costs that don't justify output over 8+ hour runs."

**The 83.5% Rule:** Anthropic triggers context compaction at approximately 83.5% of context window capacity, before degradation begins.

**Effective Capacity:** Most models degrade at 65-85% of nominal capacity. A 1M-token window provides ~3-4x runtime of 200K window, not 5x.

**Cost Arithmetic:**
- Naive long-context: 10K daily interactions × 100K tokens = $5,000/day
- Retrieval-augmented: Same workload = $333/day
- **15x cost difference**

**Performance Degradation:** "Models experience measurable accuracy drops when relevant information is positioned in the middle of very long inputs."

**Source:** [Tian Pan: Agent Memory vs Long Context Windows](https://tianpan.co/blog/2026-04-20-amortizing-context-agent-memory-vs-long-context-windows) | [Context Engineering for Agents](https://tianpan.co/blog/2026-02-23-effective-context-engineering-for-ai-agents)

---

### Checkpoint Bloat

**Problem:** "Long-running threads accumulate hundreds of checkpoints."

**LangGraph Specific:** No automatic expiration. Requires manual pruning via scheduled jobs.

**Storage Cost:** Every node transition serialized. Large state objects multiply checkpoint size.

**Security Issue:** Entire StateGraph serialized as plaintext—API keys, tokens, PII end up in database unencrypted.

**Mitigation:**
- Store large objects externally, only references in state
- Regular checkpoint cleanup jobs
- Encrypt sensitive fields before serialization
- Use meaningful thread IDs for debuggability

**Source:** [LangGraph Persistence Guide](https://markaicode.com/langgraph-persistence-checkpointing-workflows/)

---

### Multi-Agent Merge Conflicts

**Scenario:** Two agents assigned to related issues both modify overlapping files.

**Problem:** Each agent creates separate PR without awareness of other's changes. When PRs merged sequentially, second causes merge conflicts.

**Current State:** "No built-in mechanism prevents two agents from both attempting to fix the same issue or modifying same files in incompatible ways."

**Workarounds:**
- Human coordination (doesn't scale)
- File-level locking (too coarse-grained)
- Module-level ownership (requires explicit boundaries)
- Sequential execution (loses parallelism benefits)

**Production Pattern:** Hierarchical coordinator assigns non-overlapping work to workers. Requires upfront planning to identify dependencies.

**Source:** [Medium: When Two Agents Work the Same PR](https://medium.com/@nivedv/when-two-agents-work-the-same-pr-multi-agent-orchestration-in-github-fb77f38b3d95) | [ArXiv: Large-Scale Dataset of Merge Conflicts](https://arxiv.org/html/2604.03551v2)

---

### Infinite Loops and Runaway Costs

**Failure Mode:** Agent enters loop without convergence detection.

**Causes:**
- No maximum iteration limit
- Lack of progress detection
- Missing cost/time budgets
- Tool repetition not detected

**Production Incident Pattern:**
1. Agent starts task with open-ended goal
2. Makes progress initially
3. Enters local minimum (repeated failed attempts)
4. Continues indefinitely, burning tokens
5. Discovered when bill arrives or quota exhausted

**Prevention (Essential):**
- Hard iteration limits (LangChain default: 15)
- Tool repetition detection (2nd identical call = warning, 3rd = stop)
- Token budgets (soft and hard limits)
- Wall-clock timeouts
- Progress metrics (information gain per step)

**Source:** [How to Stop AI Agents from Looping Forever](https://meritshot.com/blog/ai-agent-termination-conditions) | [Fix Infinite Loops in Multi-Agent Chat](https://markaicode.com/fix-infinite-loops-multi-agent-chat/)

---

### Human-in-Loop Approval Latency

**Pattern:** Agent pauses for human approval on sensitive operations.

**Hidden Cost:** Wall-clock time extends dramatically. A 4-hour autonomous workflow becomes 3-day human-paced workflow if approvals not handled promptly.

**Failure Modes:**
- Approval request buried in notifications
- Approver in different timezone
- Context lost between pause and resume
- Workflow state expires while waiting

**Production Patterns:**
1. **Async notification:** Push notification, email, Slack with urgency indicator
2. **Batching:** Group multiple approval requests when possible
3. **Delegation:** Allow approval routing to backup approvers
4. **Timeout policies:** Default action (approve/reject) after X hours
5. **Context preservation:** Show full decision context in approval UI

**Trade-off:** More autonomy = more risk; more gates = slower execution.

**Source:** [Truto: Human-in-Loop Approval Workflows](https://www.truto.one/blog/implementing-human-in-the-loop-approval-workflows-for-consequential-saas-api-actions/) | [LangGraph: Human-in-the-Loop](https://docs.langchain.com/oss/python/langchain/frontend/human-in-the-loop)

---

### Observability Gaps

**Problem:** Agent fails or produces incorrect output. "Why did it do that?"

**Missing Visibility:**
- Reasoning trace not captured
- Tool calls logged but not rationale
- Context state at decision point unknown
- Model uncertainty not surfaced

**Production Consequence:** Debugging requires re-running with extensive logging, often non-reproducible due to non-determinism.

**Cost:** Engineering hours spent investigating inscrutable failures exceed compute costs.

**Solution Requirements:**
- Structured trace capture (OpenTelemetry spans)
- Reasoning provenance (which facts led to which decisions)
- State snapshots at key decision points
- Confidence scores surfaced to operators

**Maturity Gap:** Standards still emerging. Most production systems use ad-hoc logging.

**Source:** [OpenTelemetry: AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/) | [Agent Observability Guide](https://fast.io/resources/ai-agent-observability/)

---

## Reusable Patterns for self-evo

### Pattern 1: GitHub Issue as Work Unit

**Mechanism:**
- One Issue = one autonomous task
- Issue body contains: objective, context, success criteria
- Labels indicate: priority, agent type, status
- Comments capture: progress updates, decisions, blockers
- Closing comment: outcome summary, artifacts created

**Advantages:**
- Native GitHub primitive (no external database)
- Auditability built-in (full history)
- Human visibility (browse issues to see agent work)
- Coordination point (humans can intervene via comments)

**Implementation:**
- Agent runtime claims Issue (adds "in-progress" label)
- Periodic status updates as comments
- Structured output on completion
- Links to PRs, artifacts, related issues

**Source Pattern:** ResearchPlanAssignOps, GitHub Agentic Workflows

---

### Pattern 2: Durable Workflow for Long-Running Tasks

**When to Use:** Tasks spanning hours/days with expensive operations

**Architecture:**
- Use Temporal, Restate, or Inngest (not just checkpointing)
- Each major step is durable activity/step
- Automatic retry on transient failures
- State preserved across crashes

**Self-evo Application:**
- Research phase: multi-hour web searches, documentation reading
- Implementation phase: repeated test/fix cycles
- Review phase: multi-step validation with external tools

**Implementation:**
```
workflow ResearchTask:
  activity Search(query) -> results [retries: 3, timeout: 5min]
  activity Synthesize(results) -> report [retries: 1, timeout: 30min]
  activity StoreToGitHub(report) -> issue_url [retries: 5, timeout: 2min]
```

**Benefit:** Crash at any point = resume from last completed activity, not start over.

---

### Pattern 3: Hierarchical Agent Coordination

**Structure:**
- Coordinator agent: plans, assigns, monitors
- Worker agents: execute assigned subtasks
- No worker-to-worker communication (prevents coordination complexity)

**Self-evo Application:**
- Coordinator: reads Issue, creates execution plan, spawns workers
- Research worker: gathers information
- Implementation worker: writes code
- Review worker: validates output
- Coordinator: aggregates results, posts to Issue

**Communication:**
- Coordinator → Worker: task specification via function call
- Worker → Coordinator: structured result object
- No shared state between workers (prevents race conditions)

**Failure Handling:**
- Worker failure: Coordinator detects, retries with different worker or escalates
- Coordinator failure: Durable workflow ensures recovery with full state

**Why This Works:**
- Predictability: Deterministic flow, easy to debug
- Scalability: Add workers without changing coordinator logic
- Production usage: 30% of deployments (from research data)

**Trade-off:** Coordinator can become bottleneck. Mitigate with async worker dispatch and event-driven status updates.

**Source Pattern:** CrewAI hierarchical, Microsoft supervisor pattern

---

### Pattern 4: Context Compression at 83.5% Threshold

**Problem:** Long-running coding agents hit context limits, losing critical information.

**Solution:**
- Monitor context utilization continuously
- Trigger compression at 83.5% capacity (before degradation)
- Compress conversation history into summaries
- Clear tool results from completed subtasks
- Retain: objectives, key decisions, current state

**Implementation:**
```
if context_usage > 0.835 * context_limit:
    summary = compress_conversation_history()
    clear_old_tool_results()
    archive_to_external_memory(full_history)
    context = [summary, current_objectives, recent_state]
```

**Memory Architecture:**
- Short-term: Recent conversation (in context)
- Working: Summaries of earlier phases (in context)
- Long-term: External storage (GitHub Issue comments, database)

**Benefit:** 90% token reduction (Mem0 results) with modest accuracy trade-off. Enables continued operation vs. hard failure.

**Source Pattern:** Anthropic context engineering, Long-running agents guide

---

### Pattern 5: Three-Layer Termination Defense

**Problem:** Agents loop indefinitely or burn excessive resources.

**Solution:** Implement three independent stop mechanisms:

**Layer 1 - Policy Gate (Before Execution):**
```
policy = {
    max_iterations: 15,
    token_budget: 500_000,
    timeout_seconds: 3600,
    allowed_tools: ['read_file', 'write_file', 'run_tests']
}
```

**Layer 2 - Convergence Detection (During Execution):**
```
detect_patterns = {
    tool_repetition: same_tool_3x → force_stop,
    diminishing_returns: info_gain < threshold → warn,
    retrieval_cycles: cycles > 3 → stop,
    no_progress: 2_iterations_no_change → escalate
}
```

**Layer 3 - Budget Enforcement (Runtime Checks):**
```
if tokens_used > soft_limit:
    alert_operator()
if tokens_used > hard_limit:
    synthesize_partial_results()
    graceful_terminate()
```

**Critical:** All three layers must be present. Any single layer failure still provides protection.

**Source Pattern:** Tian Pan termination conditions, LangChain max_iterations

---

### Pattern 6: Idempotent Tool Execution

**Problem:** Network timeouts, agent retries, and workflow recovery cause duplicate operations (double payments, duplicate records).

**Solution:** Three-layer idempotency contract:

**Layer 1 - Generate Stable Keys:**
```
idempotency_key = f"{workflow_run_id}:{step_id}"
# Must be stable across retries
```

**Layer 2 - Deduplicate at Tool Layer:**
```
def execute_tool(tool_name, params, idempotency_key):
    cached = check_cache(idempotency_key)
    if cached:
        return cached.result

    result = actual_tool_execution(tool_name, params)
    store_cache(idempotency_key, result)
    return result
```

**Layer 3 - Tool Implementation:**
```
# Payment API
if idempotency_key in processed_payments:
    return existing_payment_record
else:
    charge = process_payment(params)
    mark_processed(idempotency_key, charge)
    return charge
```

**Self-evo Application:**
- GitHub Issue creation (don't create duplicate issues on retry)
- File writes (don't append twice on network failure)
- External API calls (don't double-trigger webhooks)

**Critical Property:** Enables aggressive retries while ensuring economic result matches intent (one charge, one record, one notification).

**Source Pattern:** Tian Pan idempotency patterns, Saga compensation

---

### Pattern 7: Defense-in-Depth Security

**Problem:** Agent-generated code could exfiltrate secrets, corrupt files, or compromise host.

**Solution:** Multiple independent security layers:

**Layer 1 - Execution Isolation:**
- Firecracker MicroVMs for hardware-level isolation
- Or gVisor for lightweight virtualization
- Not just Docker containers (insufficient for adversarial workloads)

**Layer 2 - Capability Restriction:**
```
sandbox_config = {
    filesystem: {
        read: ['/workspace'],
        write: ['/workspace/output'],
        deny: ['/secrets', '/home']
    },
    network: {
        allow: ['github.com', 'api.anthropic.com'],
        deny: ['*']
    },
    resources: {
        cpu: '2 cores',
        memory: '4GB',
        timeout: '30min'
    }
}
```

**Layer 3 - Output Validation:**
- Scan generated code for suspicious patterns
- Validate file paths before writes
- Check network destinations before allowing connections
- Human approval for destructive operations

**Layer 4 - Audit Trail:**
- Log all filesystem operations
- Record network requests
- Track resource consumption
- Enable forensic analysis post-incident

**Self-evo Application:**
- Worker agents run in isolated sandboxes
- No access to repository secrets
- GitHub token scoped to minimum permissions
- Generated code reviewed before merge

**Source Pattern:** GitHub Agentic Workflows firewall, OWASP Agentic Top 10

---

### Pattern 8: Adaptive Rate Limiting

**Problem:** Multiple agents sharing API quotas cause quota exhaustion and throttling.

**Solution:** Centralized rate limit coordinator with adaptive concurrency.

**Architecture:**
```
RateLimitCoordinator:
    quota_pool: shared across all agents
    current_usage: real-time tracking
    agent_priorities: critical vs. background

    request_permission(agent_id, priority):
        if quota_available:
            allocate_and_track()
            return permit
        else:
            if priority == 'critical':
                throttle_background_agents()
                return permit
            else:
                queue_request()
                return wait_signal
```

**AIMD Algorithm:**
- Additive Increase: slowly ramp up concurrency when no errors
- Multiplicative Decrease: quickly back off on rate limit responses (403, 429)

**Error Handling:**
```
on_rate_limit_error:
    exponential_backoff(base=2s, max=60s)
    add_jitter(±20%)  # prevent thundering herd
    reduce_global_concurrency(multiplier=0.5)
```

**GitHub-Specific:**
- 5,000 requests/hour authenticated
- Track per-endpoint quotas separately
- Reserve quota for critical operations (issue updates)
- Background tasks (searches) yield when quota low

**Source Pattern:** GitHub rate limiting controls, multi-agent coordination challenges

---

### Pattern 9: OpenTelemetry Observability

**Problem:** Agent failures are opaque. "Why did it do that?" requires hours of debugging.

**Solution:** Structured telemetry capture using OpenTelemetry standards.

**Trace Structure:**
```
Span: workflow_execution
├─ Span: research_phase
│  ├─ Span: web_search (attributes: query, results_count)
│  ├─ Span: llm_call (attributes: model, tokens, latency)
│  └─ Span: synthesis (attributes: sources_used, confidence)
├─ Span: implementation_phase
│  ├─ Span: write_code (attributes: files_modified, lines_changed)
│  └─ Span: run_tests (attributes: tests_run, failures)
└─ Span: review_phase
```

**Critical Attributes:**
- Reasoning provenance: which facts led to which decisions
- Context state: what information was available at decision point
- Tool calls: parameters, results, retries
- Model metadata: model name, temperature, tokens consumed
- Outcome: success/failure, confidence score

**Self-evo Application:**
- Understand why agent chose specific approach
- Debug failures without re-running (traces are durable record)
- Optimize: identify slow operations, expensive tool calls
- Improve: feed traces back into agent training/prompting

**Integration:**
- Export to Datadog, Honeycomb, Grafana, or local storage
- Standardized format enables switching vendors
- Framework-agnostic (works with any agent runtime)

**Source Pattern:** OpenTelemetry GenAI SIG conventions

---

## Recommendation Table: Adopt, Adapt, or Reject

| Pattern/Technology | Recommendation | Rationale | Implementation Effort |
|-------------------|---------------|-----------|---------------------|
| **GitHub as Coordination Plane** | **ADOPT** | Native primitive, auditability, human visibility, zero infrastructure cost | Low - API already available |
| **Issue-as-Work-Unit** | **ADOPT** | Perfect fit for self-evo task tracking, enables human oversight | Low - straightforward API usage |
| **Hierarchical Agent Coordination** | **ADOPT** | Production-proven (30% deployments), predictable, debuggable | Medium - requires coordinator logic |
| **Context Compression at 83.5%** | **ADOPT** | Essential for long-running agents, prevents hard failures | Medium - requires monitoring + compression |
| **Three-Layer Termination Defense** | **ADOPT** | Prevents runaway costs, all three layers needed | Low-Medium - mostly configuration |
| **Idempotent Tool Execution** | **ADOPT** | Critical for reliability, prevents duplicate operations | Medium - requires workflow-level support |
| **Durable Execution (Temporal/Restate)** | **ADAPT** | Powerful but heavyweight. Consider for Phase 2 when scale demands | High - new infrastructure dependency |
| **Checkpoint-Only Approaches (LangGraph)** | **ADAPT** | Useful for state but insufficient alone. Supplement with supervisor | Low-Medium - add failure detection |
| **Defense-in-Depth Security** | **ADOPT** | Essential for production. Start with sandboxing + capability limits | High - requires sandboxing infrastructure |
| **Adaptive Rate Limiting** | **ADOPT** | Required for multi-agent systems sharing quotas | Medium - centralized coordinator needed |
| **OpenTelemetry Observability** | **ADOPT** | Invaluable for debugging, optimization, improvement | Medium - instrumentation + export setup |
| **Sequential/Pipeline Orchestration** | **ADOPT** | Simplest pattern (40% production), start here before hierarchical | Low - linear execution |
| **Parallel Orchestration** | **ADAPT** | Useful for independent subtasks but adds merge complexity | Medium - requires result aggregation |
| **State-Graph Orchestration** | **ADAPT** | Overkill unless human approval gates essential | High - complex state management |
| **Swarm Orchestration** | **REJECT** | Only 5% production usage, highest complexity, poor reliability | Very High - avoid entirely |
| **AutoGPT/BabyAGI Architectures** | **REJECT** | Superseded by newer patterns, experimental phase only | N/A - historical interest |
| **Inngest Event-Driven Steps** | **ADAPT** | Good for event-triggered workflows. Evaluate vs Temporal | Medium - new platform dependency |
| **GitHub Agentic Workflows** | **ADAPT** | Preview status = unstable API. Monitor for GA release | Low-Medium - markdown-based config |
| **ResearchPlanAssignOps Pattern** | **ADOPT** | Directly applicable to self-evo. Human checkpoints at phase transitions | Low-Medium - pattern template provided |
| **Firecracker/gVisor Sandboxing** | **ADOPT** | Production-grade isolation for code execution | High - infrastructure setup |
| **Mem0 Memory Architecture** | **ADAPT** | 90% token reduction proven. Evaluate specific implementation | Medium - integration + testing |
| **Heterogeneous Model Teams** | **ADOPT** | Match model cost to task complexity (Opus plans, Sonnet implements) | Low - routing logic |
| **Saga Pattern for Compensation** | **ADAPT** | Essential for multi-step business processes. Overkill for simple workflows | High - compensation logic per step |

**Key Recommendations:**

**Phase 1 (MVP):**
- GitHub Issue coordination
- Hierarchical agent structure
- Basic termination limits
- Simple observability (logging)

**Phase 2 (Production Hardening):**
- Durable execution platform
- Full idempotency
- Security sandboxing
- OpenTelemetry observability

**Phase 3 (Scale):**
- Adaptive rate limiting
- Memory architecture optimization
- Multi-agent parallelization
- Advanced error recovery

---

## Limitations and Gaps

### 1. GitHub API as Bottleneck

**Constraint:** 5,000 requests/hour limit applies to all agents sharing authentication token.

**Impact:** High-frequency status updates or parallel agent coordination can exhaust quota quickly.

**Mitigation:** Batch updates, use GraphQL (fewer requests), implement local state cache.

**Unresolved:** No official GitHub guidance on scaling agent automation beyond single-token limits.

---

### 2. Checkpoint Security

**Problem:** LangGraph and similar frameworks serialize full state as plaintext, exposing API keys, tokens, and PII.

**Current State:** Documented issue with no built-in solution.

**Workaround:** Store secrets externally, encrypt sensitive fields manually before serialization.

**Gap:** No framework-native secure checkpoint storage.

---

### 3. Multi-Agent File Conflicts

**Problem:** No built-in mechanism prevents parallel agents from modifying same files in incompatible ways.

**Current Solutions:** All require manual implementation:
- File-level locking (too coarse)
- Module-level ownership (requires boundaries)
- Sequential execution (loses parallelism)

**Research Gap:** No production-proven coordination protocol for parallel coding agents on shared codebase.

---

### 4. Durable Execution Infrastructure Overhead

**Trade-off:** Temporal/Restate provide strong guarantees but require:
- Running separate server infrastructure
- Learning platform-specific programming models
- Operational complexity (monitoring, updates, scaling)

**Alternative:** Checkpoint + supervisor is simpler but requires custom failure detection.

**Unresolved:** No lightweight durable execution library (infrastructure-free) with full guarantees.

---

### 5. Non-Deterministic Debugging

**Challenge:** Same agent with same inputs may produce different outputs due to:
- Model non-determinism (even with temperature=0)
- External API state changes
- Race conditions in parallel execution

**Impact:** Failures difficult to reproduce and debug.

**Partial Solutions:** Seed fixing, input hashing, trace replay (all imperfect).

**Gap:** No production-grade deterministic replay for agent debugging.

---

### 6. Quality vs. Autonomy Trade-off

**Finding:** "The gap between 'agent produced a working prototype' and 'agent produced production-ready, maintainable, secure code' remains the critical test."

**Current State:** Agents good at functional implementations, struggle with:
- Security best practices
- Edge case handling
- Maintainability patterns
- Performance optimization

**Human Review Still Essential:** Even 52-hour agent sessions require significant review before production deployment.

**Unresolved:** No automated quality gate can replace human judgment for production code.

---

### 7. Context Window vs. Codebase Size Mismatch

**Problem:** Even 1M token contexts insufficient for large codebases (100K+ lines).

**Workarounds:** RAG, semantic search, focused reading (all add latency and complexity).

**Fundamental Limit:** Context compression loses information. Some tasks require holistic codebase understanding impossible with current context limits.

**Gap:** No solution for "understand entire codebase" tasks that exceed context capacity.

---

### 8. Economic Viability Unproven at Scale

**Early Evidence:** 52-hour sessions show promise, but:
- Token costs scale linearly with time
- Human review costs remain constant
- Value proposition unclear for >8 hour tasks

**Cost Arithmetic:** 10-hour agent run at $0.01/1K tokens with 500K tokens/hour = $50. If produces prototype requiring 8 hours human review ($400) vs. 12 hours human implementation ($600), modest savings.

**Unresolved:** Break-even point for different task types not empirically established.

---

### 9. Observability Standards Immature

**Status:** OpenTelemetry GenAI SIG standards "emerging" and "may change significantly through 2026."

**Impact:** Tooling fragmented, implementations non-portable, conventions still evolving.

**Risk:** Instrumentation built today may require rework as standards solidify.

**Gap:** No stable observability standard for AI agents (contrast with mature distributed tracing standards).

---

### 10. GitHub Agentic Workflows Preview Status

**Caveat:** "Public Preview—may change significantly."

**Risk:** API breaking changes, feature deprecation, pricing changes.

**Production Recommendation:** Adopt cautiously, expect migration work before GA.

**Gap:** No GA-ready GitHub-native agent orchestration platform yet available.

---

## Source Summary

**Total Searches:** 35 web searches across broad, technical, and operational domains

**Deep Fetches:** 15 detailed articles from primary sources

**Source Composition:**
- Official documentation: 6 sources (GitHub, OpenTelemetry, Anthropic)
- Technical blogs (Tian Pan, O-mega, MarkAI): 7 sources
- Vendor platforms (Temporal, Restate, Inngest): 3 sources
- Academic papers (OpenHands/ICLR): 1 source
- Industry analysis (Groovyweb, Diagrid): 2 sources
- Case studies (Medium): 2 sources

**Date Range:** Primarily 2025-2026, with selective 2024 academic work

**Source Quality:**
- **Kept:** 19 sources with architectural detail, production patterns, empirical findings
- **Rejected:** 10+ sources (marketing-heavy, superseded experiments, basic tutorials)

**Verification note:** Important claims were cross-referenced where possible. Numeric values in individual sources, such as orchestration shares or context-compression thresholds, remain source-specific observations and should not be treated as universal production statistics. GitHub API limits must be checked against the authenticated installation and current official documentation.

**Bias Notice:** Vendor sources (Temporal, Restate, Inngest) present own solutions favorably. Balanced with independent analysis (Diagrid checkpoint critique, Groovyweb orchestration costs).

---

## Conclusion

Autonomous coding agents and GitHub-centered coordination are transitioning from experimental to production-viable in 2025-2026, but with clear maturity boundaries:

### What's Production-Ready Now:

1. **GitHub as coordination substrate** - Issues, PRs, and webhooks provide durable, auditable coordination primitives with zero infrastructure cost.

2. **Hierarchical orchestration** - Proven pattern (30% production deployments) with predictable behavior and manageable complexity.

3. **Context management** - The 83.5% compression threshold and hybrid memory architectures enable extended operation beyond naive context limits.

4. **Termination controls** - Three-layer defense (policy + convergence + budget) prevents runaway costs and infinite loops.

5. **Basic idempotency** - Workflow-level idempotency keys enable reliable retry without duplicate operations.

### What Requires Careful Adaptation:

1. **Durable execution platforms** - Powerful guarantees but significant infrastructure overhead. Checkpoint-only approaches need supplementary failure detection.

2. **Multi-agent parallelization** - Coordination complexity and merge conflicts limit practical parallelism. Sequential and hierarchical patterns dominate for good reason.

3. **Security sandboxing** - Essential for production but requires infrastructure investment (Firecracker, gVisor).

### What Remains Immature:

1. **Observability standards** - OpenTelemetry conventions still evolving, tooling fragmented.

2. **GitHub Agentic Workflows** - Preview status with unstable APIs, monitor for GA.

3. **Agent quality assessment** - Gap between "working prototype" and "production-ready code" still requires human review.

4. **Economic viability at scale** - Break-even points for different task types not empirically established.

### Critical Success Factors for self-evo:

**Start Simple:** Sequential or hierarchical orchestration, GitHub Issues as work units, basic termination limits. Prove value before adding complexity.

**Build Observability Early:** Structured logging and tracing invaluable for debugging non-deterministic behavior. Investment pays back immediately.

**Defense in Depth:** Multiple independent safety layers (termination, rate limiting, sandboxing). No single layer is sufficient.

**Human Checkpoints:** ResearchPlanAssignOps pattern's phase transitions with human review match production reality better than fully autonomous loops.

**Incremental Autonomy:** Start with supervised execution, expand autonomy as reliability proven. Premature autonomy risks runaway costs.

### The Frontier:

Long-running autonomous coding agents can now operate reliably for hours to days, but the "last mile" to production-quality code remains human-intensive. The winning pattern combines:
- Large context windows for resilience
- Aggressive tool use for efficiency
- Parallel decomposition for speed
- Cross-session memory for expertise accumulation
- **Continuous human oversight** for quality assurance

The architecture patterns exist. The coordination primitives are available. The economic case is emerging. The remaining challenge is not technical—it's organizational: integrating autonomous agents into human development workflows without sacrificing code quality, security, or maintainability.

**For self-evo Issue #7:** The research supports building a GitHub-centered hierarchical agent system with durable task tracking, context management, and human review gates. Start with ResearchPlanAssignOps as template, implement three-layer termination defense, and defer durable execution infrastructure until scale demands it.

---

**End of Research Report**
**Total Word Count:** ~8,500 words
**Research Depth:** 35 searches, 15 deep fetches, 19 vetted sources
**Date Completed:** 2026-06-21
