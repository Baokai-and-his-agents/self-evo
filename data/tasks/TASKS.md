# Tasks

Local mirror and summary of GitHub Issues.

This file is not the source of truth. GitHub Issues are the primary task state.

## Open

No open tasks.

## Claimed

### T-20260618-001 · Issue #1

- type: review
- status: claimed
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
- lease_until: 2026-06-18T13:36:07+0800
- claimed_at: 2026-06-18T10:36:07+0800

## Done

No completed tasks yet.
