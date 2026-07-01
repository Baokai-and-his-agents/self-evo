# Exploration — why a clawbie worker loop, and where it fits

- run_id: 2026-06-29-clawbie-loop-001
- worker: clawbie
- linked: #32, #28, `docs/STAGE_R_LOOP.md`, `data/proposals/rule_changes/2026-06-27-loop-operating-model.md`

## What was asked

jlcbk wants a loop that, as `clawbie`, monitors this repo's open issues and PRs
and autonomously advances suitable work. Decisions captured up front:

- **Boundary**: full clawbie worker (claim → `data/**` work → agent branch →
  draft PR → state sync; plus PR monitoring). Not Stage R's advisory-only tick.
- **Scheduling**: current-session ScheduleWakeup (session-scoped). Not launchd.

## Why this is not a Stage R reopen

Stage R (`docs/STAGE_R_LOOP.md`) is deliberately advisory-only: it writes
candidate artifacts under `.self-evo/runtime/**` and explicitly forbids writing
GitHub state, creating branches, pushing, or acting as a scheduler. Its own
Future Loop Map lists `task execution loop` and `PR babysitter loop` as deferred.

The requested loop is exactly that deferred scheduler. It reuses the existing
**full worker protocol** (`rules/START_HERE.md`, `AGENT_PROTOCOL.md`,
`GITHUB_POLICY.md`, `PERMISSIONS.yaml`) — which already permits
`push_agent_named_branch` and `create_draft_pr` without human confirmation —
and adds only: (a) a scheduler trigger, (b) a deterministic selection filter,
(c) read-only PR monitoring.

So nothing in `rules/**` needs to change to enable the loop. The new thing is an
**operating mode + scheduler**, recorded as a proposal
(`data/proposals/rule_changes/2026-06-29-clawbie-worker-loop.md`) so the
governance trail is explicit.

## Relationship to #28 (Stage R roadmap)

#28 invites discussion of Stage R milestones M1 (real worker patch generation),
M2 (promote command), M4 (Scout vs Stage R priority). **This loop does not
implement M1/M2.** Those are Stage R internals and deserve their own issues.

The loop can *later* pick #28 as a `type:scout` tick and produce the exploration
brief #28 asks for. That is the correct way to engage #28 — not by building the
loop *under* #28 (which would invert governance: claiming a roadmap epic to ship
something the roadmap hadn't approved).

## Relationship to Scout (README stage A)

README marks Autonomous Scout as the current top priority; "定时唤醒和长期无人
值守 supervisor" is listed as not-yet-implemented. This loop is a **minimal,
session-scoped** version of that supervisor, deliberately small: it does not
build Scout's source registry, runner, or dedup ledger. It only drives the
existing single-issue worker protocol on a timer. If Scout later needs a
scheduler, this loop's runbook is the natural place to extend.

## Biggest risk and how it is bounded

A ScheduleWakeup fires in a **fresh context** with no memory of these
constraints. The failure mode is an over-eager wake that invents work, broadens
scope, or touches things it shouldn't.

Mitigations (encoded in the runbook):

1. The wake prompt is a **fixed verbatim directive** pointing at the runbook —
   not an open-ended `/loop` sentinel.
2. The runbook leads with a HARD CONSTRAINTS section.
3. Issue selection is a **closed allowlist**; zero matches → forced no-op.
4. No-op ticks create **zero** branches/PRs/issues (heartbeat is local-only).
5. Strict auth discipline (`switch -u clawbie` → write → `switch -u jlcbk`).
6. Per-tick time-box (~15 min) and fail-closed guards.

## Recommendation

Accept the proposal, merge #32's PR, and arm the loop for a trial period. Expect
mostly no-ops until build issues are opened. The loop's early value is
discipline + PR babysitting, not throughput — and that is the right shape for a
first scheduler in a single-human repo.
