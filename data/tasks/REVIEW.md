# Review Queue

Items requiring human confirmation.

Use this for:

- unapproved resources
- rule-change requests
- protected branch or PR actions
- high-risk actions
- unclear instructions

## Pending

No pending review items.

## Resolved

### R-20260618-001 — public-web-read 资源(resolved 2026-06-18)

- 原请求:`rules/RESOURCE_APPROVALS.yaml` 中 `public-web-read` 曾为 `pending`。
- resolution: 已在 `main` 经 PR #2 批准为 read-only(`status: approved`,2026-06-18)。

### R-20260618-002 — 分支保护软约束(resolved 2026-06-18)

- 原请求:`rules/GITHUB_POLICY.md` 描述的保护未在 GitHub 实际配置。
- resolution: PR #2 已在 `rules/GITHUB_POLICY.md`「Main Branch」加入 stage note,记录当前为软约束阶段、真实保护留待 MVP 1.5。对应提案
  `data/proposals/rule_changes/2026-06-18-clarify-branch-protection-soft-stage.md`
  标记为 implemented。
