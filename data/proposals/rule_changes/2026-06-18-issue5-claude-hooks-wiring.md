# Proposal — wire MVP 1.5 safety hooks into project Claude config

- proposed_at: 2026-06-18
- proposed_by: local-code-worker-01 (run 2026-06-18-run-002)
- issue: #5
- branch: agent/local-code-worker-01/5-hooks-validator
- status: proposed (awaiting `jlcbk`)
- affected_paths: `.claude/settings.json` (does not yet exist), `scripts/**`

## Why a proposal

Issue #5 requires PreToolUse and Stop hooks, and rules/PERMISSIONS.yaml treats
project-level Claude configuration as a protected zone (analogous to
`.github/**` proposal_required and `rules/**` read_only). The agent must not
edit protected configuration directly, so the wiring is proposed here for
`jlcbk` to install.

## What is being requested

1. Create `.claude/settings.json` (project-level) by copying the `hooks` block
   from `scripts/hooks/claude-settings.sample.json`.
2. On the Windows PowerShell workspace use the `pwsh -NoProfile -File
   scripts/hooks/*.ps1` command variants; on macOS/Linux use the
   `python3 scripts/hooks/*.py` variants.
3. Keep the committed rollout mode at **`audit`**
   (`scripts/hooks/config.json#rollout_mode`). Installing the hooks alone does
   not block anything in audit mode.

## What the hooks do (summary)

- PreToolUse: in audit, logs findings; in `pretool-enforce`/`full-enforce`,
  denies writes to `rules/**`, protected hook/config paths, writes outside
  authorized roots, direct `main` pushes, force pushes, and recursive
  deletions; denies reads of likely secrets.
- Stop: in `full-enforce` only, blocks Stop when lifecycle checks find BLOCK
  findings (no run summary / changed files without Draft PR / review with an
  active claim / heartbeat still running / task mirror inconsistent).
- Both are read-only w.r.t. task state; the only writes are the audit log and
  loop counter under `data/audit/` (gitignored).

## Approval gates requested from jlcbk

- [ ] Approve creating `.claude/settings.json` with the sample hooks block.
- [ ] Confirm Python 3 is available on the target workspace (documented
      prerequisite; the agent does not install it).
- [ ] Decide when (if ever) to raise the mode above `audit`. Recommendation:
      run several real runs in `audit`, review `data/audit/hook-audit.jsonl`
      for false positives, then move to `pretool-enforce` before considering
      `full-enforce`.

## Rollback

Set `SELF_EVO_ROLLOUT_MODE=audit`, or remove the `hooks` block from
`.claude/settings.json` and restart Claude Code. No task state is mutated.

## Risks

- Substring-based command matching can false-positive on benign strings and
  false-negative on obfuscated commands (see scripts/README.md).
- Secret detection is path/name heuristic; enforce modes can deny reads of
  sensibly-named non-secret files.
- A misconfigured hook could trap a worker; mitigations are the `audit`
  default, the Stop loop cap, and the `SELF_EVO_STOP_GUARD=1` escape hatch.
