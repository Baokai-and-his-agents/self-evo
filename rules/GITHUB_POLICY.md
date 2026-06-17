# GitHub Policy

GitHub is the task coordination and audit plane.

## Identity Model

Use two identities when possible:

- Agent GitHub account: comments, claims, agent branches, draft PRs.
- Human GitHub account: approvals, protected branch changes, PR merges, rule changes.

The agent account may have repository write permission, but should not have admin or bypass branch protection permission.

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

## PR Expectations

Agent PRs should be draft by default.

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
