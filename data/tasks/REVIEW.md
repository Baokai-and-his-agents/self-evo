# Review Queue

Items requiring human confirmation.

Use this for:

- unapproved resources
- rule-change requests
- protected branch or PR actions
- high-risk actions
- unclear instructions

## Pending

### R-20260618-003 — 项目级 Claude hooks 接线(待 jlcbk 确认)

- 来源:Issue #5,run 2026-06-18-run-002。
- 请求:`jlcbk` 将 `scripts/hooks/claude-settings.sample.json` 的 `hooks` 块安装到受保护的 `.claude/settings.json`;确认目标工作区存在 Python 3(文档化前置,agent 不安装);决定何时(是否)将 rollout 模式从 `audit` 提升。
- 更新(iteration 2):`hooks` 块现为本机可直接安装的 exec-form `python` 配置(无需 `python3`/`pwsh`,Windows PowerShell 5.1 + `python` 即可)。
- 详情:`data/proposals/rule_changes/2026-06-18-issue5-claude-hooks-wiring.md`。
- 风险:子串式命令匹配与启发式密钥检测存在误报/漏报;enforce 模式可能拒读命名合理的非密钥文件。提升模式前建议先在 `audit` 下审阅 `data/audit/hook-audit.jsonl`。

## Resolved

### R-20260618-001 — public-web-read 资源(resolved 2026-06-18)

- 原请求:`rules/RESOURCE_APPROVALS.yaml` 中 `public-web-read` 曾为 `pending`。
- resolution: 已在 `main` 经 PR #2 批准为 read-only(`status: approved`,2026-06-18)。

### R-20260618-002 — 分支保护软约束(resolved 2026-06-18)

- 原请求:`rules/GITHUB_POLICY.md` 描述的保护未在 GitHub 实际配置。
- resolution: PR #2 已在 `rules/GITHUB_POLICY.md`「Main Branch」加入 stage note,记录当前为软约束阶段、真实保护留待 MVP 1.5。对应提案
  `data/proposals/rule_changes/2026-06-18-clarify-branch-protection-soft-stage.md`
  标记为 implemented。
