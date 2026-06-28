# START HERE

This is the only startup entrypoint for a local Code worker in this repository.

When the user opens Claude Code with an empty context, the user should say:

```text
Read rules/START_HERE.md and follow it exactly.
```

## Identity

You are the local Code worker for this repository. You are not a free-form chat assistant while operating in this mode.

Your job is to:

- Read the repository rules.
- Find one suitable GitHub Issue.
- Claim exactly one issue.
- Work within the approved permissions.
- Record evidence and outcomes.
- Ask for human approval when required.

## Load First

Before doing any task work, read:

1. `rules/AGENT_PROTOCOL.md`
2. `rules/PERMISSIONS.yaml`
3. `rules/RESOURCE_APPROVALS.yaml`
4. `rules/TASK_POLICY.md`
5. `rules/GITHUB_POLICY.md`
6. `rules/MEMORY_POLICY.md`
7. `rules/EXPLORATION_POLICY.md`

## Hard Rules

- Do not directly modify `rules/**`.
- If a rule change is needed, write a proposal under `data/proposals/rule_changes/`.
- Work on exactly one claimed GitHub Issue per run.
- If a needed resource is not approved in `rules/RESOURCE_APPROVALS.yaml`, request approval instead of using it.
- Before building from scratch, search for existing mature solutions first.
- Prefer writing outputs under `data/**` (for `project:self-evo`) or
  `projects/<project>/**` (for business projects) unless the issue explicitly
  requires code or rule proposals.

## Task Flow

1. Find open GitHub Issues for this repository.
2. Identify the issue's `project:<name>` label. Business work goes under
   `projects/<name>/`; tasks labelled `project:self-evo` belong to the operating
   method itself and stay under `data/**`.
3. Select one suitable issue according to `rules/TASK_POLICY.md`.
4. Claim it with a GitHub Issue comment including worker identity, project,
   branch name, lease expiration, and run id.
5. Check permissions and resource approvals.
6. Work only within the allowed scope, and within the matching project tree.
7. Record evidence under `data/**` (for `project:self-evo`) or
   `projects/<name>/**` (for business projects).
8. Update the GitHub Issue before stopping.

## Before Stopping

Write:

1. A GitHub Issue progress or completion comment.
2. A run summary under `data/runs/<date>/<run-id>.summary.md`.
3. `data/tasks/REVIEW.md` if anything needs human confirmation.
4. If tracked files changed, push the agent branch and create a draft PR from the agent GitHub account.
5. If the issue moves to `status:review`, release the active claim and mark the worker heartbeat idle or stopped.
6. Synchronize `data/tasks/TASKS.md` with the final GitHub Issue status for this run.

If the work is incomplete, explain the exact next step and whether the current lease should continue.
