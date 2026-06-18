# Rule Change Proposal · 2026-06-18-clarify-branch-protection-soft-stage

- proposed_by: local-code-worker-01
- run_id: 2026-06-18-run-001
- related_issue: 1
- date: 2026-06-18
- status: proposed

## 目标规则文件

- `rules/GITHUB_POLICY.md`(「Main Branch」小节)

## 现状与问题

`rules/GITHUB_POLICY.md` 的「Main Branch」小节写道:

> `main` should be protected:
> - no direct pushes
> - pull request required
> - code owner review required for `rules/**`
> - agent account cannot bypass protection

但当前仓库的 main 分支保护**未在 GitHub 实际配置**;`.github/CODEOWNERS` 已写入 `@jlcbk`,但只构成软提示。也就是说,规则文件描述的是一个尚未落地、靠 agent 自觉与后续人工 review 兜底的状态。

风险:规则文本与现实不一致,可能让后续 worker(或多 worker 场景)误以为 `rules/**` 已有硬保护,从而降低警觉;也可能误导人类协作者。

## 建议的修改(供用户审阅后写入)

在「Main Branch」小节增加阶段性说明,明确当前为软约束阶段,例如:

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

## 备注

本提案仅为「阶段说明」的增量。真正的修复是落实 MVP 1.5(GitHub 分支保护 / rulesets),那是配置动作,不属于 agent 可直接执行的范围,需用户在 GitHub 侧操作。
