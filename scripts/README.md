# Scripts — run validator & Claude Code safety hooks (Issue #5)

MVP 1.5 turns the repository rules into executable guardrails. This directory
holds:

- a **read-only run validator** (`validate_run.py` / `validate-run.ps1`)
- a **PreToolUse** hook (`hooks/pretooluse.py` / `pretool-use.ps1`)
- a **Stop** hook (`hooks/stop.py` / `stop.ps1`)
- the **shared guardrail contract** (`policy.json`) and pure logic (`_policy.py`)
- a **Stage R runtime-confined no-op tick** (`loop_runtime_tick.py`)
- an **offline deterministic test matrix** (`tests/test_matrix.py`)
- **real-git / subprocess integration tests** (`tests/test_integration.py`)

## Design: one implementation, PowerShell entrypoints

The canonical logic is Python 3 (stdlib only — no `pip install`, no global
software). The `.ps1` files are thin wrappers that resolve `python`/`python3`
(or `py -3`) and forward stdin/args. Hooks, validator, and tests all import the
same `_policy.py` and read the same `policy.json`, so the three surfaces cannot
drift on what counts as dangerous.

**Prerequisite:** Python 3 on `PATH` (`python` on Windows; `python3` on
macOS/Linux). The agent does not install it. On the Windows workspace this is
Windows PowerShell 5.1 + `python`; `pwsh` (PowerShell 7) and `python3` are **not**
required and are not assumed anywhere.

## Installation (project-level hook wiring)

Project-level Claude configuration (`.claude/settings.json`) is a protected
path under this repo's policy, so the agent does **not** wire it directly.
`jlcbk` installs the hooks by copying the `hooks` block from
`hooks/claude-settings.sample.json` into `.claude/settings.json` (or merging
it). See the governance proposal:

```text
data/proposals/rule_changes/2026-06-18-issue5-claude-hooks-wiring.md
```

The sample's `hooks` block is **directly installable on the Windows workspace**.
It uses the official **exec form** (`command` + `args`) with the
`${CLAUDE_PROJECT_DIR}` placeholder — the form the Claude Code docs recommend
for path placeholders. No shell is involved, so there are no quoting, `pwsh`, or
`python3` pitfalls:

```jsonc
"hooks": {
  "PreToolUse": [
    { "matcher": "*", "hooks": [
      { "type": "command", "command": "python",
        "args": ["${CLAUDE_PROJECT_DIR}/scripts/hooks/pretooluse.py"] }
    ] }
  ],
  "Stop": [
    { "hooks": [
      { "type": "command", "command": "python",
        "args": ["${CLAUDE_PROJECT_DIR}/scripts/hooks/stop.py"] }
    ] }
  ]
}
```

(`Stop` has no matcher: it is ignored for Stop, which always fires.)

A non-Windows (bash + `python3`) alternative and a `.ps1`-via-`powershell.exe`
Windows alternative are kept in the sample under separate top-level keys — never
inside an executable hook object, and never mixed into the Windows `hooks`
block.

### Issue / base-ref overrides (env)

- `SELF_EVO_ISSUE=<n>` — tell the Stop hook and validator which issue a run
  targets when it cannot be read from the agent branch name (a branch named
  `<n>-...`). Standard Claude Stop payloads carry no issue field, so the issue
  is otherwise derived from the branch or the active claim/heartbeat.
- `SELF_EVO_BASE_REF=<ref>` — override the validator's PR base ref (otherwise
  resolved as `origin/main` → `main` → …).

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
export SELF_EVO_ROLLOUT_MODE=pretool-enforce      # Windows PS: $env:SELF_EVO_ROLLOUT_MODE='pretool-enforce'

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

A Stop-hook loop can always be escaped with `SELF_EVO_STOP_GUARD=1`, the hook
self-caps consecutive blocks at `stop_loop_block_limit` (default 2), and Claude
Code additionally self-caps at 8 consecutive blocks.

## Running the validator

```bash
python scripts/validate_run.py --issue 5            # human-readable
python scripts/validate_run.py --issue 5 --json     # machine-readable
python scripts/validate_run.py                      # issue derived from SELF_EVO_ISSUE / branch / claim
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate-run.ps1 -Issue 5   # Windows wrapper
```

It reports structured `PASS` / `WARN` / `BLOCK` findings and never repairs
state. Exit code is 0 for a normal report (read the JSON `summary` for the worst
level), or 2 only when the active issue cannot be determined. Changed files are
computed as the committed branch diff vs the resolved base ref **unioned with**
staged/unstaged/untracked/renamed/deleted working-tree files — so a clean
committed PR branch no longer looks like "zero changes".

## Running the Stage R no-op tick

Stage R PR 1 adds only the runtime boundary skeleton. It writes one gitignored
run directory under `.self-evo/runtime/runs/<run_id>/` and produces:

```text
input.json
decision.md
result.json
```

Manual invocation:

```bash
python scripts/loop_runtime_tick.py
python scripts/loop_runtime_tick.py --json
python scripts/loop_runtime_tick.py --run-id 2026-06-28T00-00-00Z --json
```

The tick fails fast unless `.self-evo/runtime/` is ignored by Git. This PR 1
entrypoint does not fetch GitHub issues, select work, run a worker, run the
Runtime Review Agent, promote files, create branches, commit, push, or open PRs.

## Running the tests

```bash
python scripts/tests/test_matrix.py         # offline deterministic matrix (pure classifier + faked state)
python scripts/tests/test_integration.py    # real-git + real-subprocess integration tests
python scripts/tests/test_loop_runtime_tick.py  # Stage R runtime boundary + no-op contract
```

The matrix never executes destructive commands. The integration tests create
throwaway git repositories under the system temp dir (never the repo) and run
real `git`/`python`/hook subprocesses; they assert the changed-files union, the
Windows subprocess UTF-8 path, the hook output contract, the audit-log secrecy,
and the draft-PR / run-identity specificity.

## JSON input/output contract (current official Claude Code hook schema)

**PreToolUse** — stdin: `{"session_id","tool_name","tool_input", ...}`.
Both the `Bash` tool and the first-class `PowerShell` tool (Claude Code 2.1.174+)
carry a `command` string and are inspected identically.

```jsonc
// allow (audit, or clean action)
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":"audit: ..."}}
// deny (pretool/full enforce) — exit 0, reason is shown to Claude
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"write_to_rules: ..."}}
```

Exit `0` always (allow **or** structured deny). We intentionally do **not**
exit `2` for denials: per the official docs, exit-2 stdout JSON is ignored and
only stderr is surfaced, which would silently drop the deny reason. The deny is
expressed via `permissionDecision` instead.

**Stop** — stdin: the standard Stop payload (no `issue` field). The active
issue is derived (`SELF_EVO_ISSUE` > agent branch > active claim/heartbeat).
Top-level `decision` (Stop does **not** use `hookSpecificOutput`):

```jsonc
// block stop (full-enforce, within the loop cap) — exit 0, reason shown to Claude
{"decision":"block","reason":"self-evo Stop hook BLOCKING stop ... <findings>"}
// allow stop — exit 0, no decision block
{}
// advisory / ambiguous-context / loop-cap allowance — shown to the user, not Claude
{"systemMessage":"self-evo Stop hook: ..."}
```

Finding codes include: `write_to_rules`, `write_to_protected_hook_impl`,
`write_outside_authorized`, `write_proposal_required`, `shell_write_to_rules`,
`shell_write_to_protected`, `shell_write_outside`, `shell_write_proposal_required`,
`protected_branch_push`, `force_push`, `dangerous_recursive_delete`,
`read_likely_secret`.

## Audit log

Findings are appended to `data/audit/hook-audit.jsonl` (audit zone, **not** task
state; gitignored). **The log never records raw commands, file contents, or
secrets** — only minimal safe metadata: the event, mode, tool name, decision,
finding codes, a path *zone* (never the path), and for shell tools a command
*length* plus a *sha256 prefix* (never the command text). Tokens,
`Authorization`/`Bearer` values, passwords, and command payloads therefore
cannot appear in the log. The Stop-loop counter lives at
`data/audit/stop-loop.counter`. Hooks never mutate `state/**` task state, never
create commits, and never open PRs.

## Known limitations & false-positive risks

- **Command classification is substring-based.** `git push --force` is caught,
  but a contrived `git push origin +main` or a force-push spelled via an alias
  may evade it. Conversely, a benign string that happens to contain `push origin main`
  inside a larger command (e.g. inside an `echo` or comment) could be flagged.
- **Shell-write detection is best-effort, not a parser.** Obvious redirections
  (`>`/`>>`), `tee`/`Tee-Object`, the PowerShell content cmdlets
  (`Set-Content`/`Add-Content`/`Out-File`/`New-Item`), `cp`/`mv`/`Copy-Item`/
  `Move-Item` destinations, `[System.IO.File]::WriteAllText`, and the common
  `python|node|perl -c "...open(...)..."` inline pattern are caught. **Arbitrary
  interpreter writes cannot be perfectly classified before execution.** The
  reliable backstop is the Stop hook's committed-diff check: any protected or
  out-of-zone write that lands on the branch (committed or uncommitted) is
  caught there. Bypass regression tests cover PowerShell `Set-Content`/
  redirection, Bash redirection, and interpreter writes.
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
- **Validator reflects live state.** Findings depend on the current branch,
  claim files, labels, and PRs; it is deterministic *given that state*, not
  state-independent.
- **Windows console encoding.** The validator decodes `git`/`gh` output
  explicitly as UTF-8 with a safe fallback, so it runs on a Windows/GBK (Chinese
  locale) machine; human-readable output is ASCII-only to avoid console
  mojibake.
