# Scripts — run validator & Claude Code safety hooks (Issue #5)

MVP 1.5 turns the repository rules into executable guardrails. This directory
holds:

- a **read-only run validator** (`validate_run.py` / `validate-run.ps1`)
- a **PreToolUse** hook (`hooks/pretooluse.py` / `pretool-use.ps1`)
- a **Stop** hook (`hooks/stop.py` / `stop.ps1`)
- the **shared guardrail contract** (`policy.json`) and pure logic (`_policy.py`)
- an **offline deterministic test matrix** (`tests/test_matrix.py`)

## Design: one implementation, PowerShell entrypoints

The canonical logic is Python 3 (stdlib only — no `pip install`, no global
software). The `.ps1` files are thin wrappers that resolve `python`/`python3`
(or `py -3`) and forward stdin/args, because Issue #5 prefers a PowerShell
entrypoint for the Windows workspace. Hooks, validator, and tests all import
the same `_policy.py` and read the same `policy.json`, so the three surfaces
cannot drift on what counts as dangerous.

**Prerequisite:** Python 3 on `PATH`. The agent does not install it.

## Installation (project-level hook wiring)

Project-level Claude configuration (`.claude/settings.json`) is a protected
path under this repo's policy, so the agent does **not** wire it directly.
`jlcbk` should install the hooks by copying `hooks/claude-settings.sample.json`
into `.claude/settings.json` (or merging its `hooks` block). See the governance
proposal:

```text
data/proposals/rule_changes/2026-06-18-issue5-claude-hooks-wiring.md
```

Windows hook commands (PowerShell):

```jsonc
"hooks": {
  "PreToolUse": [{ "matcher": "*", "hooks": [{ "type": "command",
    "command": "pwsh -NoProfile -File scripts/hooks/pretool-use.ps1" }] }],
  "Stop":      [{ "matcher": "",  "hooks": [{ "type": "command",
    "command": "pwsh -NoProfile -File scripts/hooks/stop.ps1" }] }]
}
```

macOS/Linux hook commands (bash):

```jsonc
"hooks": {
  "PreToolUse": [{ "matcher": "*", "hooks": [{ "type": "command",
    "command": "python3 scripts/hooks/pretooluse.py" }] }],
  "Stop":      [{ "matcher": "",  "hooks": [{ "type": "command",
    "command": "python3 scripts/hooks/stop.py" }] }]
}
```

## Rollout modes

Mode precedence: env `SELF_EVO_ROLLOUT_MODE` > `hooks/config.json` >
`policy.json#default_rollout_mode`. The **committed default is `audit`** and
must stay that way until `jlcbk` approves enforcement.

| mode | PreToolUse blocks? | Stop blocks? | use when |
|------|--------------------|--------------|----------|
| `audit` (default) | no | no | baseline; only logs findings |
| `pretool-enforce` | yes | no | rules writes / force pushes are blocked; a bad hook still can't trap the worker in a run |
| `full-enforce` | yes | yes | only after audit has proven acceptable false-positive rates |

**Enabling a mode** (pick one):

```bash
# 1) temporary, per-shell (recommended for evaluation):
export SELF_EVO_ROLLOUT_MODE=pretool-enforce

# 2) committed: edit scripts/hooks/config.json -> {"rollout_mode":"pretool-enforce"}
#    (this file is protected hook implementation; a worker cannot flip it silently)
```

**Disabling / rollback:**

```bash
# Roll back to pure audit immediately:
export SELF_EVO_ROLLOUT_MODE=audit
# Or, to fully detach the hooks, remove the hooks block from .claude/settings.json
# and restart Claude Code. No task state is mutated by removal.
```

A Stop-hook loop can always be escaped with `SELF_EVO_STOP_GUARD=1`, and the
hook self-caps consecutive blocks at `stop_loop_block_limit` (default 2).

## Running the validator

```bash
python3 scripts/validate_run.py --issue 5            # human-readable
python3 scripts/validate_run.py --issue 5 --json     # machine-readable
pwsh    scripts/validate-run.ps1 -Issue 5            # Windows entrypoint
```

It reports structured `PASS` / `WARN` / `BLOCK` findings and never repairs
state. Exit code is always 0 (read-only reporter); read the JSON `summary`
field for the worst level.

## Running the tests

```bash
python3 scripts/tests/test_matrix.py                 # prints PASS/FAIL table
```

The matrix is deterministic and never executes destructive commands. It feeds
command **strings** into the pure classifier and injects fake repo state into
the validator; no `git`/`gh` subprocess and no repo write is performed by the
cases under test.

## JSON input/output contract

**PreToolUse** — stdin: `{"session_id","tool_name","tool_input", ...}`.
stdout (only when there is something to report):

```jsonc
// allow (audit, or clean action)
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":"audit: write_to_rules"}}
// block (pretool/full enforce)
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"write_to_rules: ..."}}
```

Exit `0` = allow, `2` = block (Claude Code convention).

**Stop** — stdin: `{"session_id", ...}` (optional `"issue"`). Explanation is
written to **stderr**. Exit `0` = allow stop, `2` = block stop (full-enforce
only, subject to the loop cap). Finding codes include: `write_to_rules`,
`write_to_protected_hook_impl`, `write_outside_authorized`,
`write_proposal_required`, `protected_branch_push`, `force_push`,
`dangerous_recursive_delete`, `read_likely_secret`.

## Audit log

Findings are appended to `data/audit/hook-audit.jsonl` (audit zone, **not**
task state). The Stop-loop counter lives at `data/audit/stop-loop.counter`.
Both are gitignored runtime diagnostics. Hooks never mutate `state/**` task
state, never create commits, and never open PRs.

## Known limitations & false-positive risks

- **Command classification is substring-based.** `git push --force` is caught,
  but a contrived `git push origin +main` or a force-push spelled via an alias
  may evade it. Conversely, a benign string that happens to contain `push origin main`
  inside a larger command (e.g. inside an `echo` or comment) could be flagged.
- **Secret detection is path/name heuristic.** A file named `token-cache.json`
  in `data/` would trip `read_likely_secret` on read (WARN in audit). In
  enforce modes that read would be denied — review before enabling enforce.
- **`.github/**` and `docs/**` are `proposal_required`, surfaced as WARN**,
  not blocked, so template edits are visible without trapping the worker.
- **`scripts/**` is protected hook implementation.** In enforce modes a worker
  cannot edit the hooks/config via the editor tools — intentional, so a
  confused worker cannot disable the guardrails. Development of these files
  happens in `audit` mode on an agent branch via `git` (the hook inspects tool
  calls, not commits).
- **Windows-only enforcement surface.** The `.ps1` wrappers assume Python 3 on
  `PATH`; without it, the wrappers error and (depending on hook config) may
  default to non-blocking. Verify Python 3 before enabling enforce.
- **Validator reflects live state.** Findings depend on the current branch,
  claim files, labels, and PRs; it is deterministic *given that state*, not
  state-independent.
