# Review Queue

Items requiring human confirmation.

Use this for:

- unapproved resources
- rule-change requests
- protected branch or PR actions
- high-risk actions
- unclear instructions

## Pending

### R-20260618-001 — informational · public-web-read 资源未批准

- task: T-20260618-001 / Issue #1
- request: `rules/RESOURCE_APPROVALS.yaml` 中 `public-web-read` 仍为 `pending`。后续 scout / 探索类任务需联网前,请用户批准该资源(或限定 scope)。
- risk: 低。本次 dry run 不联网,未受影响;仅作为前瞻提醒。
- recommended_action: approve(或先限定 scope 再批准)

### R-20260618-002 — informational · 分支保护为软约束

- task: T-20260618-001 / Issue #1
- request: main 分支保护尚未在 GitHub 实际配置,`rules/**` 只读边界靠软规则。详见规则提案:
  `data/proposals/rule_changes/2026-06-18-clarify-branch-protection-soft-stage.md`。
- risk: 中(多 worker 场景下依赖自觉)。
- recommended_action: review proposal;并考虑推进 MVP 1.5 配置真实保护。
