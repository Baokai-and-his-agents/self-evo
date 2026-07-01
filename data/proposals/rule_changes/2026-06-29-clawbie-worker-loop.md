# Proposal — clawbie session-level worker loop (scheduler authorization)

- proposed_at: 2026-06-29
- proposed_by: clawbie (run 2026-06-29-clawbie-loop-001), at jlcbk's request
- status: proposed (awaiting `jlcbk`)
- authorizing_issue: #32
- related_context:
  - `docs/STAGE_R_LOOP.md`
  - `data/proposals/rule_changes/2026-06-27-loop-operating-model.md` (Stage R proposal, Future Loop Map)
  - #28 (Stage R roadmap epic)
- affected_paths_if_accepted:
  - `data/runbooks/clawbie-worker-loop.md` (new convention: loop operating manuals live under `data/runbooks/`)
  - future scheduler wiring (session-level only at first)

## What this proposal is

Introduce a **clawbie session-level worker loop**: a loop driven by the current
Claude Code session's ScheduleWakeup, where each tick performs one **full worker
run** as `clawbie` (not a Stage R advisory tick):

```
tick:
  read rules + GitHub Issues/PRs (read-only)
  choose 0 or 1 suitable unclaimed issue
  if 1: claim -> work under data/** -> push agent/clawbie/<n>-<slug> -> draft PR -> sync state
  if 0: no-op (heartbeat + PR monitoring record)
  stop
```

## Framing vs Stage R (read this before reviewing)

This proposal does **not** reopen Stage R. `docs/STAGE_R_LOOP.md` states:

> Stage R is not a scheduler. It is one manually invokable loop tick. A future
> scheduler may call it later, after the tick behavior is stable.

and lists `task execution loop` and `PR babysitter loop` in its Future Loop Map.

This loop **is that deferred future scheduler**, scoped down to:

- session-level scheduling only (ScheduleWakeup in an attended Claude Code session),
- full worker runs under the **existing** `rules/PERMISSIONS.yaml` envelope
  (`push_agent_named_branch`, `create_draft_pr`, `write_data_files` are already
  `allowed_without_human_confirmation`),
- read-only PR observation (no acting on others' PRs).

Stage R remains advisory-only and untouched. The two modes coexist: Stage R is
the runtime-confined candidate producer; this loop is the scheduler that drives
real (canonical, PR-reviewed) worker runs.

## Accepted scope (what is authorized if jlcbk accepts)

1. The runbook at `data/runbooks/clawbie-worker-loop.md` is the authoritative
   tick procedure; wake prompts point to it verbatim.
2. clawbie may, per tick, claim one unclaimed low/medium-risk issue, work under
   `data/**`, push an `agent/clawbie/**` branch, and open a draft PR.
3. clawbie may record PR monitoring rows under `data/runs/<date>/pr-monitor.md`.
4. Scheduling is session-scoped ScheduleWakeup only.

## Non-Goals / Hard boundaries (encoded in the runbook)

The loop must NOT:

- merge PRs, mark PRs ready, push `main`, or bypass protection,
- touch `rules/**`, `.github/**`, `docs/**` directly (proposal path only),
- touch any PR/claim it did not create in the current tick (incl. #31),
- open new issues to manufacture work (bootstrap #32 was the only exception),
- use unapproved external resources,
- run as launchd/cron or headless `claude -p` (out of scope; needs separate rule change),
- broaden its own selection filter or lower the risk bar when no issue qualifies,
- hold a cross-tick lease longer than the stated 4h default without re-claiming cleanly,
- survive the Claude Code session that armed it.

## Why now

- `jlcbk` explicitly requested a clawbie-driven loop that monitors issues/PRs and
  advances suitable work autonomously.
- The full-worker path is already policy-approved; only the *scheduling* and the
  *operating mode* are new, and Stage R already forecast them.
- The loop's early value is **discipline** (clean no-ops, PR babysitting), not
  throughput — most early ticks will be no-ops until build issues are opened.

## Rollback

- Stop invoking the wake (do not re-arm ScheduleWakeup).
- clawbie finishes or releases any in-flight claim via the normal review transition.
- Canonical files are unchanged by ticks that only wrote `data/**` + `state/**`
  and were merged through normal PR review; unmerged agent branches can be deleted.

## Open questions for `jlcbk`

1. Is session-level scheduling sufficient for now, or should a launchd/cron
   variant be proposed soon?
2. Should the selection filter be widened to `type:scout` issues that produce
   briefs (so the loop can productively tick on #28), or kept to `type:build`
   until Scout lands?
3. Is 45 min the right cadence, or prefer 30 / 60?
4. When the loop's own draft PR (this one) is merged, should the wake be armed
   automatically on next session, or always require an explicit jlcbk "go"?
