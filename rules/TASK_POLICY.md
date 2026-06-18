# Task Policy

GitHub Issues are the primary task entrypoint.

## Issue Types

Recommended labels:

```text
type:learn
type:build
type:scout
type:review
type:memory
type:rule-proposal
```

## Status Labels

```text
status:open
status:claimed
status:running
status:blocked
status:review
status:done
```

## Permission Labels

```text
permission:read-only
permission:data-write
permission:sandbox
permission:repo-branch-write
permission:external-resource
permission:needs-human
```

## Claim Rules

Each worker run must claim exactly one issue.

Claim comment format:

```md
Agent claim:
- worker: local-code-worker-01
- run_id: 2026-06-18-run-001
- branch: agent/local-code-worker-01/<issue-number>-<slug>
- lease_until: 2026-06-18T18:30:00+08:00
```

If an issue already has an active claim, do not work on it unless the lease has expired or the user explicitly asks you to continue it.

GitHub labels and Issue comments are authoritative. Files under `state/claims/` and `data/tasks/TASKS.md` are coordination mirrors and must be synchronized before a run stops.

## Branch Naming

Use:

```text
agent/<worker>/<issue-number>-<slug>
```

## Completion Evidence

A completed task should include:

- issue progress or completion comment
- run summary under `data/runs/`
- changed files or output locations
- draft PR created by the executing agent account whenever tracked files changed
- sources and evidence
- tests or checks when applicable
- blockers and review requests

## Review And Claim Release

When work is ready for human review:

1. Push the agent branch.
2. Create a draft PR if tracked files changed.
3. Change the Issue status to `status:review`.
4. Mark the claim record `released` or `review` and record `released_at`.
5. Mark the worker heartbeat `idle` or `stopped`.
6. Move the local task mirror to a Review section.

Do not leave an active lease or a Claimed task mirror after the Issue has entered `status:review`.

## Long-Running Directions

If an issue is a broad direction rather than a concrete task, treat it as an exploration program:

1. Write an exploration brief.
2. Build a capability map.
3. Produce an existing work survey.
4. Produce a reuse map.
5. Propose child tasks or decision options.
