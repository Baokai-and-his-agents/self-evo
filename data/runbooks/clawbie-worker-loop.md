# Runbook — clawbie worker loop

This is the single source of truth for one tick of the clawbie session-level
worker loop. The ScheduleWake prompt points here verbatim. A fresh-context wake
must be able to execute one tick by reading this file alone.

- owner: jlcbk (human)
- worker: clawbie (agent GitHub account, write permission, non-admin)
- scheduler: current Claude Code session via ScheduleWakeup (session-scoped only)
- authorizing proposal: `data/proposals/rule_changes/2026-06-29-clawbie-worker-loop.md`
- relationship to Stage R: this loop is the **future scheduler that Stage R
  explicitly deferred** (`docs/STAGE_R_LOOP.md` § "Stage R is not a scheduler").
  It is a separate operating mode. It does NOT modify, call, or reopen Stage R's
  advisory tick.

## HARD CONSTRAINTS — read first or abort

These are non-negotiable. If any cannot be honored, abort to a no-op (Step 5)
and stop.

1. **One issue per tick, or zero.** Never batch. Zero is a valid, expected
   outcome (no-op).
2. **Never open a new GitHub issue.** Manufacturing work by opening issues is
   forbidden. (The only exception was the one-time bootstrap issue #32, already
   done — do not repeat it.)
3. **Never merge a PR. Never mark a PR ready for review.** Both are
   `requires_human_confirmation` in `rules/PERMISSIONS.yaml`.
4. **Never touch `rules/**`, `.github/**`, `docs/**` directly.** `rules/` is
   read-only; `.github/` and `docs/` are `proposal_required`. Changes there go
   through `data/proposals/` only.
5. **Never touch a PR or claim you did not create in THIS tick.** PR #31 and all
   prior released claims are off-limits. The loop observes them read-only.
6. **Never use unapproved external resources.** Check
   `rules/RESOURCE_APPROVALS.yaml`; if missing/expired/out-of-scope, write to
   `data/tasks/REVIEW.md` and no-op.
7. **Never push to `main` or any protected branch.** Only `agent/clawbie/<n>-<slug>`.
8. **Auth discipline.** `gh auth switch -u clawbie` before any GitHub write;
   switch back to `jlcbk` at tick end. Auth state leaks across ticks otherwise.
9. **Lease default: 4 hours.** `lease_until = now + 4h`, ISO-8601 UTC (`Z`).
10. **Time-box: one tick ≤ ~15 minutes of work.** If exceeded, commit what
    exists, set heartbeat `running` with a note, stop.
11. **Fail closed.** If `gh auth switch`, `gh issue list`, or `git pull` fails,
    abort to no-op with an error heartbeat. Never proceed on partial state.
12. **Start every tick from clean `origin/main`.** Never run from a feature
    branch. `git checkout main && git pull --ff-only`; non-fast-forward → abort.

## Per-tick flow

### Step 0 — bootstrap guards (every tick)

```
cd /Users/cui/Documents/self-evo/source
git rev-parse --is-inside-work-dir || abort
gh auth status | grep -q 'account clawbie' || gh auth switch -u clawbie
# if switch fails → abort, write error heartbeat, switch back to jlcbk, stop
git status --porcelain
# if there are changes NOT owned by this tick → abort (do not stash others' work)
git fetch origin --quiet
git checkout main && git pull --ff-only origin main
# if pull is not fast-forward → abort (human needed)
```

Re-read HARD CONSTRAINTS.

### Step 1 — sense (read-only)

```
gh issue list --repo Baokai-and-his-agents/self-evo --state open \
  --json number,title,labels,state,assignees,updatedAt --limit 50
gh pr list --repo Baokai-and-his-agents/self-evo --state open \
  --json number,title,headRefName,author,isDraft,reviews --limit 50
```

For each open PR authored by `clawbie` that is not in a "waiting on human"
state: mark **in-flight, do not touch**. (Today: #31.)

### Step 2 — decide (deterministic selection)

Apply the selection filter (§Selection filter). Result is exactly 0 or 1 issue.

- 0 → Step 5 (no-op).
- 1 → that is the target. Re-check it is not actively claimed (§Active-claim
  check). If actively claimed with valid lease → Step 5 (no-op). If lease
  expired → Step 5 with a recommendation (do NOT auto-reclaim silently).

### Step 3 — claim (write to GitHub + mirror)

Compose the claim comment per `rules/TASK_POLICY.md`:

```
Agent claim:
- worker: clawbie
- run_id: <YYYY-MM-DD>-clawbie-loop-<NNN>
- branch: agent/clawbie/<n>-<slug>
- lease_until: <now+4h ISO-8601 Z>
```

```
gh issue comment <n> --repo Baokai-and-his-agents/self-evo --body-file -
gh issue edit <n> --repo Baokai-and-his-agents/self-evo --add-label status:claimed
git checkout -b agent/clawbie/<n>-<slug>   # from clean main
```

`run_id` sequence: increment the `NNN` from the last run summary under
`data/runs/`. worker identity is always `clawbie`.

### Step 4 — work + ship

- Do the issue's work under `data/**` only (or `state/**` for claims/heartbeat).
  - `type:scout` → exploration brief under `data/exploration/`.
  - `type:build` → the files the issue names.
  - Stay inside the issue's stated scope. Do not overreach.
- Write `state/claims/<n>.json` (mirror) and update `state/heartbeat.json`
  (clawbie worker → `running`, `last_seen` now ISO-8601 Z).
- Write `data/runs/<date>/<run-id>.summary.md`.
- Append one row to `data/runs/<date>/pr-monitor.md` (§PR monitoring).
- Ship:
  ```
  git add <precise data/ and state/ paths only>
  git commit -m "clawbie: <one-line>"
  git push -u origin agent/clawbie/<n>-<slug>
  gh pr create --draft --base main --head agent/clawbie/<n>-<slug> \
    --title "..." --body "..."   # body: Closes #<n> + GITHUB_POLICY fields
  ```
  PR body must include: linked issue, worker `clawbie`, goal, files changed,
  evidence/sources, checks run, risks, memory updates proposed,
  human-confirmation-needed.
- Issue closing comment: PR url, summary, next step, "lease held until <ts>".
- Do **not** set `status:review`, do **not** release the claim until the work is
  truly complete across ticks. Set heartbeat `running`.

### Step 5 — no-op path

Triggered when: 0 candidate issues, or target is actively claimed, or any guard
failed.

- Write `state/heartbeat.json`: clawbie worker → `idle`, `last_seen` now, `note`:
  reason (e.g. "no claimable issue; #28 is type:scout (needs scout acceptance or
  relabel); PR #31 in-flight under review").
- Write `data/runs/<date>/<run-id>.summary.md` with read summary + PR-monitor
  table + recommendation.
- **Do NOT open a PR, do NOT create a branch, do NOT commit for a no-op tick.**
  Heartbeat is written locally only; it rides along on the next real tick that
  already has a branch+PR (avoids a stream of heartbeat PRs).
- If a guard failed: set heartbeat `note` to the error, do not retry mid-tick.

### Step 6 — teardown (every tick)

```
gh auth switch -u jlcbk
```

Re-arm the next wake with ScheduleWakeup: `delaySeconds 2700`,
`reason "clawbie-worker-loop-tick"`, prompt = the fixed wake prompt (§Wake
prompt). Then stop.

## Selection filter

A candidate issue must satisfy ALL:

- `state == OPEN`
- has label `status:open` (not `claimed/running/blocked/review/done`)
- has label `project:self-evo`
- `assignees` is empty
- has a `type:` label
- `risk` label ∈ {`risk:low`, `risk:medium`}
- does not require `permission:external-resource` unless that resource is in
  `rules/RESOURCE_APPROVALS.yaml`
- is not an issue opened by clawbie in this tick (no self-manufactured work)

If multiple pass: pick the **lowest number** (oldest). Deterministic, no scoring.

**If zero pass: the tick is a forced no-op.** You may not broaden the filter,
lower the risk bar, or claim #28 for build work. (#28 is `type:scout`; it may
only be picked as a scout tick that produces a brief under `data/exploration/`.)

## Active-claim check

Re-derive yourself; do not trust `select_issue` (it belongs to the advisory
Stage R tool). An issue is actively claimed iff ANY holds:

- has label `status:claimed` / `status:running` / `status:blocked`, OR
- `assignees` is non-empty, OR
- its most recent `Agent claim:`-formatted comment has `lease_until` in the
  future.

Lease expired → do NOT auto-reclaim; no-op with a recommendation that jlcbk
confirm reassignment.

## PR monitoring

On every tick (work or no-op), append one row to
`data/runs/<date>/pr-monitor.md` (create if absent):

```
| ts | pr# | title | author | draft? | last_review | clawbie_action |
|----|-----|-------|--------|--------|-------------|---------------|
| 2026-06-29T03:23Z | 31 | 项目化机制... | clawbie | yes | none | waiting on jlcbk |
```

This is the loop's read-only contribution to "PR babysitter". Never act on a PR
you did not create this tick.

## Scheduling parameters

- `delaySeconds`: **2700** (45 min). Constant — do not self-edit cadence.
- `reason`: `clawbie-worker-loop-tick`.
- The loop survives only while the Claude Code session that armed it is running.
  Closing Claude kills it. Persistence beyond session (launchd/cron + headless)
  is explicitly out of scope; it requires a separate rule change.

## Wake prompt (verbatim — what ScheduleWakeup fires)

```
clawbie worker loop tick. Execute exactly one tick of the loop defined in
/Users/cui/Documents/self-evo/source/data/runbooks/clawbie-worker-loop.md.

Hard rules for this wake:
- Read the runbook FIRST. Follow its steps in order. Do not improvise.
- At most one issue is claimed and worked; zero is a valid outcome (no-op).
- Do not open new issues. Do not merge. Do not mark PRs ready. Do not touch rules/, .github/, docs/ directly.
- Do not touch PR #31 or any claim/PR you did not create in this tick.
- Auth: gh auth switch -u clawbie before writes; switch back to jlcbk before stopping.
- Time-box: ~15 min. If exceeded, commit what exists, set heartbeat running, stop.
- When done, schedule the next wake with the SAME reason and this SAME prompt, delaySeconds 2700.
- If anything is ambiguous or a guard fails, abort to no-op, record in heartbeat + run summary, stop.
```

Do NOT use `/loop`'s `<<autonomous-loop-dynamic>>` sentinel. That skill is
designed for open-ended autonomy — exactly the failure mode this runbook
prevents. This loop is a fixed, bounded, policy-constrained tick.
