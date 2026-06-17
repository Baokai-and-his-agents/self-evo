# Agent Protocol

This file is the operating manual for agents working in this repository.

`rules/START_HERE.md` is the startup card. This file is the full collaboration protocol.

## Project Purpose

This repository is a long-running personal execution system. It turns loose intent, links, skill names, and project ideas into:

- executable tasks
- reusable skills
- local experiments
- opportunity assessments
- long-term memory and decisions

The worker should produce action assets, not passive summaries.

## Worker Identity

Every run must have a worker identity and a run id.

Recommended defaults:

```text
worker_identity: local-code-worker-01
run_id: <YYYY-MM-DD>-run-<number>
```

When writing GitHub comments or run summaries, include both.

## How To Work With This Repository

1. Read `rules/START_HERE.md`.
2. Load the required rule files.
3. Inspect open GitHub Issues.
4. Claim exactly one issue.
5. Check permission and resource approvals.
6. Work under `data/**` by default.
7. Never modify `rules/**` directly.
8. Produce evidence and a run summary.
9. Ask for human approval when blocked.
10. Update the issue before stopping.

## Rule And Data Boundary

`rules/**` is the rule zone. The worker may read it but must not directly edit it.

`data/**` is the work zone. The worker may write task evidence, notes, run logs, exploration outputs, proposals, and memory candidates there when allowed by policy.

If a rule needs to change, write a proposal under:

```text
data/proposals/rule_changes/
```

The user must edit `rules/**` for the change to become official.

## GitHub Issue Workflow

GitHub Issues are the primary task entrypoint.

For every run:

1. Find candidate open issues.
2. Choose one issue.
3. Add a claim comment.
4. Create or name an agent branch if needed.
5. Work on the task.
6. Add progress or completion comments.
7. Leave clear next steps if incomplete.

Do not silently work on multiple issues in one run.

## Exploration Workflow

When an issue describes a broad direction, treat it as an exploration program.

Do not try to produce the final product immediately. First create:

- an exploration brief
- a capability map
- an existing work survey
- a reuse map
- candidate child tasks
- decision-oriented recommendations

## Reuse Existing Work First

Do not repeat work that others have already solved well.

Before building from scratch, look for:

- mature tutorials
- best-practice guides
- GitHub projects
- libraries and tools
- templates
- example workflows
- case studies and retrospectives

Then decide whether to adopt, adapt, combine, or build missing pieces.

If you recommend building from scratch, explain why existing work is not enough.

## Resource Approval Workflow

External resources must be approved in `rules/RESOURCE_APPROVALS.yaml`.

If the resource is missing, expired, over budget, or out of scope:

1. Do not use it.
2. Write a request in `data/tasks/REVIEW.md`.
3. Add a GitHub Issue comment with the request and risk.
4. Continue only with safe subtasks, or stop if blocked.

Never write secrets, tokens, passwords, or private keys into repository files.

## Run Logs And Evidence

Each run should leave enough evidence to reconstruct what happened:

- issue number
- worker identity
- run id
- goal
- files read or written
- sources used
- decisions made
- failures and blockers
- resource usage
- next steps

Write run summaries under:

```text
data/runs/<date>/<run-id>.summary.md
```

Use JSONL logs only when detailed event logs are valuable.

## Failure And Uncertainty Handling

If uncertain:

- Do not invent permissions.
- Do not modify `rules/**`.
- Do not use unapproved resources.
- Write a review request.
- Leave the issue in a clear state.

If a run is interrupted, the next worker must read the issue comments, state claims, and latest run summary before continuing.
