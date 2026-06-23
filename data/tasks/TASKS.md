# Tasks

Local mirror and summary of GitHub Issues.

This file is not the source of truth. GitHub Issues are the primary task state.

## Open

No open tasks.

## Claimed

### T-20260623-003 - Issue #15

- type: scout
- status: claimed
- risk: high
- permission: external-resource, repo-branch-write
- goal: 外汇有限递增试探仓位与趋势大盈亏比专项研究
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/15
- branch: agent/scout-worker-fx-sizing-01/15-progressive-probe-sizing
- github_issue: 15
- worker_identity: scout-worker-fx-sizing-01
- run_id: 2026-06-23-fx-sizing-001
- claimed_at: 2026-06-23T02:11:30Z
- lease_until: 2026-06-23T14:11:30Z
- claim: active
- heartbeat: active
- execution_strategy: strictly serial, no subagent, no parallel upstream calls
- base: PR #14 HEAD (b17c1e2)
- dependencies: conceptually follows Issue #13 / PR #14

## Review

### T-20260623-002 - Issue #13

- type: scout
- status: review
- risk: medium
- permission: external-resource, repo-branch-write
- goal: 外汇长期动态仓位管理研究 (Phase A: Intraday; Phase B: Long-term positioning)
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/13
- branch: agent/scout-worker-fx-01/13-fx-quant-research
- github_issue: 13
- worker_identity: scout-worker-fx-01
- run_id: 2026-06-23-fx-phase-b-002
- claimed_at: 2026-06-22T18:57:51Z
- released_at: 2026-06-23T06:30:00Z
- claim: released (lease removed)
- heartbeat: stopped
- execution_strategy: strictly serial, Phase A+B sequential
- delivery: Draft PR #14 opened by `clawbie`, awaiting review
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/14

## Done

### T-20260621-003 - Issue #7

- type: scout
- status: done
- risk: medium
- permission: external-resource, repo-branch-write
- goal: Survey the autonomous-agent ecosystem and propose evidence-backed next steps for self-evo
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/7
- branch: agent/scout-worker-01/7-autonomous-agent-ecosystem
- github_issue: 7
- worker_identity: scout-worker-01
- run_id: 2026-06-21-run-003
- claimed_at: 2026-06-21T08:20:56+0800
- released_at: 2026-06-21T11:41:16+0800
- claim: released (lease removed)
- heartbeat: stopped
- execution_strategy: strictly serial Claude research roles
- delivery: PR #8 merged by `jlcbk`
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/8
- merged_at: 2026-06-22T03:18:29Z
- issue_state: closed
- completed_at: 2026-06-22

### T-20260618-002 · Issue #5

- type: build
- status: done
- risk: medium
- permission: repo-branch-write
- goal: 实现 MVP 1.5 — 只读 run validator + Claude Code PreToolUse/Stop 安全 hooks，默认 rollout 模式 audit
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/5
- branch: agent/local-code-worker-01/5-hooks-validator
- github_issue: 5
- worker_identity: local-code-worker-01
- run_id: 2026-06-18-run-002
- claimed_at: 2026-06-18T17:11:00+0800
- released_at: 2026-06-18T17:36:35+0800
- claim: released (lease removed)
- heartbeat: stopped
- delivery: PR #6 merged by `jlcbk`
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/6
- merged_at: 2026-06-20T13:37:21Z
- issue_state: closed
- completed_at: 2026-06-20

### T-20260618-001 · Issue #1

- type: review
- status: done
- risk: low
- permission: data-write
- goal: 对本仓库的本地 Code worker 协议做一次低风险 dry run,验证 agent 能否按规则工作
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/1
- acceptance:
  - 本 Issue 下 claim comment
  - `data/runs/<date>/` 下 run summary
  - 必要时更新 `data/tasks/TASKS.md` / `data/tasks/REVIEW.md`
  - 简短判断仓库骨架是否符合蓝图
  - 规则问题写入 `data/proposals/rule_changes/`
- constraints: 不修改 `rules/**`;不使用外部网络搜索;不使用付费 API;不重构仓库结构
- github_issue: 1
- worker_identity: local-code-worker-01
- run_id: 2026-06-18-run-001
- branch: agent/local-code-worker-01/1-protocol-dry-run
- claimed_at: 2026-06-18T10:36:07+0800
- released_at: 2026-06-18T11:49:11+0800
- claim: released(lease removed)
- heartbeat: stopped
- delivery: PR #3 opened by `clawbie`, approved by `jlcbk`, and merged
- merge_commit: 59be7ede916493cb74e26ab633281910833cfd92
- issue_state: closed
- completed_at: 2026-06-18
