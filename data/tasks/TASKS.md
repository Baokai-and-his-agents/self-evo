# Tasks

Local mirror and summary of GitHub Issues.

This file is not the source of truth. GitHub Issues are the primary task state.

## Open

No open tasks.

## Claimed

No claimed tasks.

## Review

### T-20260618-002 · Issue #5

- type: build
- status: review
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
- delivery: Draft PR #6 opened by `clawbie`, linked to Issue #5, awaiting `jlcbk` review & merge
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/6

## Done

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
