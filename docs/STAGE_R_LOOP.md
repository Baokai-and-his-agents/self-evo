# Stage R Loop

Stage R is the first loop-native operating mode for self-evo. It lets an agent
wake up, inspect GitHub Issues in read-only mode, produce local candidate work,
ask for an advisory runtime review, and stop without changing the canonical
repository or GitHub state.

The goal is useful loop output without PR noise or accidental authority. Stage R
is intentionally smaller than the future full loop runner.

## What Stage R Does

One Stage R tick:

1. Checks that `.self-evo/runtime/` is ignored by Git.
2. Reads open GitHub Issues through `gh issue list`.
3. Selects zero or one suitable issue.
4. Writes one run directory under `.self-evo/runtime/runs/<run_id>/`.
5. Produces runtime-only candidate artifacts.
6. Runs an advisory Runtime Review pass.
7. Stops.

No-op is a valid result. A tick may decide that no issue is suitable and still
write evidence explaining that decision.

## What Stage R Does Not Do

Stage R does not:

- write tracked repository files
- write GitHub comments, labels, statuses, issues, or pull requests
- create branches, commits, pushes, or merges
- apply `proposed.patch` to the checkout
- promote runtime artifacts into canonical project files
- run as a scheduler
- run multiple workers

This boundary is the central Stage R design choice. The tick can be useful, but
it cannot silently become authoritative.

## Runtime And Canonical Records

Runtime outputs live only under:

```text
.self-evo/runtime/**
```

This path is gitignored. Runtime outputs are local, disposable, and
non-authoritative.

Canonical records live in tracked project paths such as:

```text
rules/**
data/**
state/**
docs/**
scripts/**
.github/**
```

Changing canonical records requires the normal repository workflow: branch,
commit, review, and merge. Stage R does not do that promotion step.

## Run Directory Contract

Each tick writes exactly one run directory:

```text
.self-evo/runtime/runs/<run_id>/
```

Required artifacts:

```text
input.json
decision.md
result.json
```

Conditional artifacts:

```text
work.md
evidence.md
proposed.patch
review.md
```

Artifact meanings:

- `input.json`: compact issue and runtime context used by the tick
- `decision.md`: why one issue was selected, or why the tick no-oped
- `work.md`: candidate analysis for a selected issue
- `evidence.md`: issue metadata, runtime boundary evidence, and confidence
- `proposed.patch`: candidate patch text; never applied by Stage R
- `review.md`: advisory Runtime Review output
- `result.json`: machine-readable status and artifact index

## Outcomes

`result.json.status` is one of:

```text
work
noop
error
```

Common `result.json.outcome` values:

```text
ready_for_promote
needs_revision
no_suitable_issue
fetch_failed
runtime_boundary_violation
```

`ready_for_promote` means the candidate patch passed `git apply --check` and the
runtime review approved it. It does not mean the patch has been applied, merged,
or accepted by a human.

## Runtime Review

The Runtime Review pass is advisory. It reads the runtime artifacts and writes
`review.md`.

It may say:

```text
approved
needs_revision
rejected
abstain
```

It must not edit worker artifacts, post to GitHub, apply a patch, promote files,
or replace human approval.

## Patch Handling

Stage R may write `proposed.patch`, but it never applies the patch.

Patch validation is limited to:

```bash
git apply --check .self-evo/runtime/runs/<run_id>/proposed.patch
```

The implementation also rejects unsafe patch paths such as absolute paths or
paths containing `..`. A successful check only means the patch is mechanically
applicable to the current checkout.

## Running A Tick

Manual invocation:

```bash
python scripts/loop_runtime_tick.py
python scripts/loop_runtime_tick.py --json
python scripts/loop_runtime_tick.py --label risk:low --limit 10 --json
python scripts/loop_runtime_tick.py --offline-noop --json
```

Multiple `--label` flags use GitHub CLI AND semantics: an issue must carry every
requested label.

Exit codes:

- `0`: the tick completed and wrote a success or no-op result
- `1`: the tick wrote runtime artifacts, but `result.json.status` is `error`
- `2`: the tick hit a runtime boundary violation before normal completion

## Promote Is Future Work

Promote is outside Stage R.

A future promote command may consume a reviewed Stage R run, apply
`proposed.patch` to the real checkout, run validation, create a branch, commit,
and open a draft PR. That step must be explicit and human-authorized.

Until then, Stage R output is candidate work only.

## Future Loop Map

Stage R is one manually invokable tick, not the full loop system.

Future loops may include:

- governance loop
- issue intake loop
- PR babysitter loop
- task execution loop
- memory reflection loop

Those loops should build on the Stage R boundary instead of weakening it.

## Initial Implementation

The initial Stage R implementation landed in:

- PR #24: Stage R runtime boundary and no-op tick
- PR #25: read-only issue intake, candidate artifacts, patch check, and Runtime Review

