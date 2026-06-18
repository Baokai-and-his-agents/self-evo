# GitHub Policy

GitHub is the task coordination and audit plane.

## Identity Model

Use two identities when possible:

- Agent GitHub account: comments, claims, agent branches, draft PRs.
- Human GitHub account: approvals, protected branch changes, PR merges, rule changes.

The agent account may have repository write permission, but should not have admin or bypass branch protection permission.

Current expected repository roles:

- `jlcbk`: human owner and administrator.
- `clawbie`: agent account with write permission only.
- Organization default repository permission: `none`; each agent receives explicit per-repository access.

## Protected Rule Zone

`rules/**` should be owned by the human account through CODEOWNERS and branch protection.

Recommended CODEOWNERS:

```text
/rules/ @jlcbk
/.github/CODEOWNERS @jlcbk
```

## Main Branch

`main` should be protected:

- no direct pushes
- pull request required
- code owner review required for `rules/**`
- agent account cannot bypass protection

Current stage note:

- This private repository's current GitHub plan does not expose branch protection or repository rulesets.
- Until hard protection becomes available, the boundary is enforced through account role separation, agent protocol, CODEOWNERS guidance, PR review, and human-only merge decisions.
- The agent account must remain non-admin.

## PR Expectations

Any agent run that changes tracked files must create a draft PR.

The PR must be created by the same agent GitHub account that claimed and executed the task. The human account reviews and merges it. This preserves authorship and audit identity.

An Issue comment without a PR is acceptable only when no tracked files changed.

PR description should include:

- linked issue
- worker identity
- goal
- files changed
- evidence and sources
- checks run
- risks
- memory updates proposed
- human confirmation needed

The agent must not merge its own PR.
