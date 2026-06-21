# Autonomous Agent Ecosystem Exploration Brief

**Run ID**: 2026-06-21-run-003
**Worker**: scout-worker-01
**Issue**: #7
**Date**: 2026-06-21

## Objective

Determine what self-evo can adopt, adapt, or must build for a mature autonomous agent execution system.

self-evo's current state:
- File-first, GitHub-centered task coordination
- Claude Code as the primary execution agent
- Rules, permissions, memory, and state tracked in repository files
- Agent claims Issues, works on branches, submits Draft PRs
- Human reviews and merges

## Research Questions

1. **Autonomous loops**: What mature patterns exist for long-running agent loops with recovery, scheduling, and observability?

2. **Multi-agent orchestration**: How do production systems handle task claiming, leases, locks, handoffs, and conflict resolution?

3. **GitHub-agent collaboration**: Which systems use GitHub Issues/PRs as the coordination plane? What works and what doesn't?

4. **Memory and context**: What architectures scale beyond simple prompt injection? How do they handle hot/cold memory, retrieval, and context budget management?

5. **Proactive scouting**: Are there systems that actively monitor external sources (RSS, repos, releases, trends) and surface opportunities without explicit requests?

6. **Reliability boundaries**: How do mature systems handle:
   - Failed tool calls
   - API rate limits
   - Context overflow
   - Permission boundaries
   - Malicious inputs
   - Cascading failures

7. **Observability**: What logging, tracing, replay, and debugging approaches work for multi-turn agent workflows?

8. **Evaluation and safety**: How do systems measure agent quality, detect regressions, and prevent harmful actions?

## Research Method

- Primary sources first: official docs, repos, Issues, papers, maintainer posts
- Secondary sources for discovery and contrasting opinions only
- Record all searches, URLs, decisions, keep/reject reasons
- Deliberately seek failures, stale projects, and marketing overclaims
- Cross-check important technical claims

## Success Criteria

Research output enables jlcbk to decide:
- What to adopt directly
- What to adapt or combine
- What requires new self-evo implementation
- Which experiment to run first
- Which skill to learn next

Output must be decision-oriented, not a passive literature dump.
