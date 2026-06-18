# Rule Change Proposal · 2026-06-18-clarify-branch-protection-soft-stage

- proposed_by: local-code-worker-01
- run_id: 2026-06-18-run-001
- related_issue: 1
- date: 2026-06-18
- status: implemented
- resolved_via: PR #2 (commit fd0930d, 2026-06-18) 「Tighten agent delivery and access rules」

## 目标规则文件

- `rules/GITHUB_POLICY.md`(「Main Branch」小节)

## 现状与问题

`rules/GITHUB_POLICY.md` 的「Main Branch」小节原写道:

> `main` should be protected:
> - no direct pushes
> - pull request required
> - code owner review required for `rules/**`
> - agent account cannot bypass protection

但当时 main 分支保护未在 GitHub 实际配置;`.github/CODEOWNERS` 已写入 `@jlcbk`,但只构成软提示。规则文件描述的是一个尚未落地、靠 agent 自觉与后续人工 review 兜底的状态。

风险:规则文本与现实不一致,可能让后续 worker(或多 worker 场景)误以为 `rules/**` 已有硬保护,从而降低警觉。

## 建议的修改(供用户审阅后写入)

在「Main Branch」小节增加阶段性说明,明确当前为软约束阶段:

```md
## Main Branch

`main` should be protected:

- no direct pushes
- pull request required
- code owner review required for `rules/**`
- agent account cannot bypass protection

> Stage note (2026-06-18): branch protection is not yet enforced on GitHub;
> the rules/** read-only boundary currently relies on agent discipline plus
> human PR review. Enforcing real protection is tracked under MVP 1.5.
```

## 为什么这是必要的

让规则文本与现实阶段一致,避免 worker/人类对 `rules/**` 的实际保护强度产生错误假设。

## 风险与回滚

- 风险:本提案只增加说明性文字,不改权限边界,风险极低。
- 回滚:用户可直接删除新增的 stage note,不影响其它规则。

## 相关证据

- `data/runs/2026-06-18/run-001.summary.md`
- 用户确认:`.github/CODEOWNERS` 当前为软规则约束(对话 2026-06-18)。

## Resolution (2026-06-18)

已落实(implemented)。`jlcbk` 通过 **PR #2**「Tighten agent delivery and access rules」在 `rules/GITHUB_POLICY.md`「Main Branch」小节加入了 stage note,记录了当前为软约束阶段、当前 plan 不暴露分支保护/rulesets,以及 MVP 1.5 待办。本提案建议的文字已进入 `main`,故标记为 implemented;不再需要人类对该提案做进一步决定。

真正的硬保护(GitHub branch protection / rulesets)仍留待 MVP 1.5,那属于人类在 GitHub 侧的配置动作。
