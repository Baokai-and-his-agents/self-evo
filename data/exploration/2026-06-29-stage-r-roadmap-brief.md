# Exploration Brief — Stage R roadmap (#28) re-framed

- run_id: 2026-06-29-clawbie-loop-002
- worker: clawbie
- issue: #28 ([Epic] Stage R loop runtime — roadmap & milestones)
- type: scout (exploration; no code changes)
- date: 2026-06-29

> Responds to #28's invitation: "M1/M2/M4 是否值得做？优先级如何排序？Stage R
> 与 Scout 的关系：先行、并行、还是合并？"

## TL;DR

Since #28 was filed, the repo gained a second execution facility — the **clawbie
session-level worker loop** (#32 / PR #33). That changes the trade-offs for
M1/M2. **Recommendation:** deprioritize M1/M2 inside Stage R (the worker loop
already provides a direct claim→PR path), and reframe M4 from "Stage R vs Scout"
into **a three-facility division of labor** (Scout feeds → worker loop executes →
Stage R is an optional advisory pre-flight for high-risk work). Ship Scout and
the worker loop first; revisit M1/M2 only after evidence shows a need for an
advisory dry-run layer.

## Facility inventory (what exists now)

| facility | direction | writes GitHub? | status |
|---|---|---|---|
| **Stage R** (`loop_runtime_tick.py`) | inward, advisory | no (runtime-only) | merged (#24/#25/#27) |
| **clawbie worker loop** (#33) | inward, executing | yes (claim/branch/draft PR) | proposed, awaiting merge |
| **Scout** | outward (opportunity recon) | n/a | not built (README stage A = top priority) |

## M1 — real worker patch generation

- **Status (per #28):** `run_stage_r_tick`'s `proposed_patch_text` is not exposed
  on the CLI, so real runs always produce an empty patch → `outcome` is always
  `needs_revision`, and `ready_for_promote` is only reachable via test injection.
- **Impact of the worker loop:** the worker loop already does the thing M1 was
  meant to unlock — produce real delivery against a selected issue and ship it as
  a draft PR. So M1 is no longer "the key that unlocks Stage R's value"; it is now
  only "a low-risk read-only rehearsal before a real claim."
- **Recommendation:** **deprioritize.** If built later, frame it as an optional
  pre-flight for the worker loop (produce candidate patch, run
  `git apply --check`, then decide whether to claim) — not as an independent
  milestone of Stage R.

## M2 — promote command

- **Status:** apply a review-approved `proposed.patch`, validate, branch, draft
  PR. `STAGE_R_LOOP.md` mandates explicit human authorization; not implemented.
- **Impact of the worker loop:** the worker loop already ships canonical draft
  PRs directly — it does not need a promote step because it never confined itself
  to advisory output. Promote is Stage-R-specific (the advisory→canonical bridge).
- **Recommendation:** **defer.** Only needed if Stage R becomes a mandatory
  advisory pre-flight layer in front of the worker loop. Today it is not.

## M3 — claim-aware selection ✅ already resolved (#27)

No action. `_has_active_claim` is on `origin/main`. (Note: the worker loop
re-derives claim status itself and does not call `select_issue`.)

## M4 — relationship to Scout (and now the worker loop)

This is now the most worthwhile question, and it must be expanded: it is no
longer two-way (Stage R ↔ Scout), it is three-way.

Proposed division of labor:

```
Scout (outward)  ──feeds──►  backlog of GitHub issues
                                   │
                                   ▼
                          clawbie worker loop (executes)
                          claim → data/** → draft PR
                                   │
                                   ▼  (for high-risk issues only)
                          Stage R advisory pre-flight (optional)
                          candidate patch + git apply --check
```

- **Scout first** — README already sets it as top priority; it generates the
  backlog the other two consume.
- **Worker loop executes** the backlog — the default, low/medium-risk path.
- **Stage R is an optional advisory buffer** for high-risk issues where a
  read-only rehearsal is worth the overhead before committing to a claim.

So: **Scout → worker loop → (Stage R as advisory pre-flight for risky work)**.
Not parallel, not merged — a pipeline with Stage R as an optional stage.

## Priority recommendation

1. **Merge worker loop (#33)** and **land a Scout vertical slice** (README stage
   A). These two are the execution backbone.
2. **Defer M1/M2.** Revisit only after the worker loop is stable AND there is
   evidence that high-risk issues would benefit from an advisory pre-flight.
3. **Do not run Stage R M1 and Scout in parallel** — complexity should be
   triggered by evidence (README's own principle), not by roadmap ambition.

## Recommended child issues

- **Do not** open M1/M2 issues yet (insufficient evidence; the worker loop
  covers the execution need).
- **Do** open the Scout runner vertical slice (README stage A already implies it)
  — this is the genuine next build task and will feed the worker loop.
- **Later**, after the worker loop is stable, open a single issue to decide
  whether Stage R should become the high-risk advisory pre-flight layer (and only
  then scope M1).

## Existing work surveyed (reuse, don't rebuild)

- `scripts/loop_runtime_tick.py` — `RuntimeWriter` boundary + `_has_active_claim`
  are reusable primitives.
- `data/proposals/rule_changes/2026-06-27-loop-operating-model.md` — Stage R
  scope/non-goals already encode most of M1/M2's constraints.
- `data/runbooks/clawbie-worker-loop.md` (#33) — the execution procedure M1 was
  meant to enable, now realized.

## Risks

- **Role overlap confusion:** Stage R and the worker loop both "look at issues
  and produce work." Without an explicit division (advisory vs executing), future
  contributors will be unsure which to extend. Mitigation: once #33 merges, add a
  short architecture note to `docs/ARCHITECTURE.md` clarifying the three-facility
  pipeline (this is a docs change → proposal path).

## Open questions for jlcbk

1. Accept the three-facility framing (Scout feeds → worker loop executes → Stage
   R optional advisory pre-flight)?
2. Confirm Scout is the next build priority (over M1/M2)?
3. Should the worker loop's selection filter eventually exclude `type:scout`
   issues (so Scout briefs are produced by a dedicated Scout runner, not the
   worker loop)? — this is open question 2 of the worker-loop proposal too.
