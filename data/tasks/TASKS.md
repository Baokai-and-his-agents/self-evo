# Tasks

Local mirror and summary of GitHub Issues.

This file is not the source of truth. GitHub Issues are the primary task state.

## Open

### T-20260704-001 - Issue #38

- project: self-evo
- type: build
- status: open
- risk: medium
- permission: data-write, repo-branch-write, public-web-read
- goal: 交付 Autonomous Scout Runner (Stage A) 垂直切片
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/38
- branch: agent/refactor-worker-01/scout-runner-stage-a
- github_issue: 38
- worker_identity: refactor-worker-01
- run_id: 2026-07-04-refactor-001
- claimed_at: 2026-07-04T19:18:00+0800
- released_at: 2026-07-04T23:10:00+0800
- claim: released
- heartbeat: stopped
- execution_strategy: GLM 主导 + Codex 独立审查(4 轮,实验性,非强制流程)
- delivery: Draft PR #37 opened by clawbie, awaiting jlcbk review
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/37
- scope_note: 本 PR 仅含 data/scripts/state 实现;README/.gitignore/docs 改动拆到单独的文档 PR

## Claimed

No claimed tasks.

## Review

### T-20260710-002 - Issue #42

- project: content-operator
- type: scout
- status: review
- risk: medium
- permission: external-resource, repo-branch-write
- goal: 调研 AI Agent 内容方法并生成首批候选选题
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/42
- branch: agent/content-scout-worker-01/42-ai-agent-content-research
- github_issue: 42
- worker_identity: content-scout-worker-01
- run_id: 2026-07-10-content-scout-001
- claimed_at: 2026-07-10T06:28:00+0800
- released_at: 2026-07-10T07:05:00+0800
- claim: released
- heartbeat: stopped
- delivery: Draft PR #43 opened by clawbie, awaiting jlcbk topic selection
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/43

### T-20260710-001 - Issue #40

- project: content-operator
- type: scout
- status: review
- risk: low
- permission: external-resource, repo-branch-write
- goal: 建立 AI Agent 内容生产项目与首轮调研契约
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/40
- branch: agent/local-code-worker-01/40-content-operator-bootstrap
- github_issue: 40
- worker_identity: local-code-worker-01
- run_id: 2026-07-10-run-001
- claimed_at: 2026-07-10T06:19:39+0800
- released_at: 2026-07-10T06:30:00+0800
- claim: released
- heartbeat: stopped
- delivery: Draft PR #41 opened by clawbie, awaiting jlcbk review
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/41

### T-20260623-004 - Issue #18

- project: fx-strategy-research
- type: build
- status: review
- risk: high
- permission: data-write, sandbox, external-resource, repo-branch-write
- goal: 外汇仓位管理对照回测 MVP：核心条件概率与 A/B/E/G
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/18
- branch: agent/fx-backtest-worker-01/18-fx-backtest-mvp
- github_issue: 18
- worker_identity: fx-backtest-worker-01
- run_id: 2026-06-23-fx-backtest-001
- claimed_at: 2026-06-23T19:00:00Z
- released_at: 2026-06-23T20:15:00Z
- claim: released
- heartbeat: stopped
- execution_strategy: strictly serial, no subagent, no parallel model calls
- dependencies: Issue #15 merged mathematical model and strategy specification
- delivery: Draft PR #19 opened by clawbie, corrected implementation ready for final review
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/19
- status_update: 核心架构修正进行中，已完成事件模型、cycle管理、G置换逻辑、成本单位统一

### T-20260623-003 - Issue #15

- project: fx-strategy-research
- type: scout
- status: review
- risk: high
- permission: external-resource, repo-branch-write
- goal: 外汇有限递增试探仓位与趋势大盈亏比专项研究
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/15
- branch: agent/scout-worker-fx-sizing-01/15-progressive-probe-sizing
- github_issue: 15
- worker_identity: scout-worker-fx-sizing-01
- run_id: 2026-06-23-fx-sizing-001
- claimed_at: 2026-06-23T02:11:30Z
- released_at: 2026-06-23T11:52:00Z
- claim: released (lease removed)
- heartbeat: stopped
- execution_strategy: strictly serial, no subagent, no parallel upstream calls
- base: PR #14 HEAD (b17c1e2)
- dependencies: conceptually follows Issue #13 / PR #14
- delivery: Draft PR #16 opened by `clawbie`, awaiting review
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/16

### T-20260623-002 - Issue #13

- project: fx-strategy-research
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

### T-20260629-002 - Issue #28

- project: self-evo
- type: scout
- status: done
- risk: low
- goal: Stage R roadmap 探索 brief —— M1/M2/M4 在 worker loop 落地后的重框定
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/28
- branch: agent/clawbie/28-stage-r-roadmap-brief
- github_issue: 28
- worker_identity: clawbie
- run_id: 2026-06-29-clawbie-loop-002
- claimed_at: 2026-06-28T23:37:44Z
- released_at: 2026-07-02T00:00:00Z
- claim: released
- heartbeat: stopped
- delivery: PR #34 merged by jlcbk
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/34
- completed_at: 2026-07-02

### T-20260629-001 - Issue #32

- project: self-evo
- type: build
- status: done
- risk: low
- permission: data-write, repo-branch-write
- goal: 引入 clawbie 会话级 worker loop（runbook + 授权提案 + 首次 dry-run）
- source: https://github.com/Baokai-and-his-agents/self-evo/issues/32
- branch: agent/clawbie/32-worker-loop
- github_issue: 32
- worker_identity: clawbie
- run_id: 2026-06-29-clawbie-loop-001
- claimed_at: 2026-06-28T23:23:00Z
- released_at: 2026-07-02T00:00:00Z
- claim: released
- heartbeat: stopped
- execution_strategy: bootstrap delivery; scheduler NOT armed (awaiting jlcbk go)
- delivery: PR #33 merged by jlcbk
- pr: https://github.com/Baokai-and-his-agents/self-evo/pull/33
- completed_at: 2026-07-02

### T-20260621-003 - Issue #7

- project: self-evo
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

- project: self-evo
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

- project: self-evo
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
