# Architecture

This repository separates **operating method** (the governance framework) from **operated projects** (business output). It is organized around five planes:

Operating method (stable, cross-project):

- `rules/`: read-only operating rules for agents
- `scripts/`: executable guardrails — run validator, PreToolUse/Stop hooks, Stage R tick
- `state/`: runtime claims, locks, and heartbeat files
- `.github/`: GitHub coordination templates and review boundaries
- `data/`: writable workspace for the operating method itself — system-level memory, audit, proposals, system-self exploration and runs, and tasks

Operated projects (added/removed as business evolves):

- `projects/<project>/`: writable workspace for each business project, e.g. `projects/fx-strategy-research/` holds its own experiments, exploration, runs, and memory. Each task carries a `project` field in `data/tasks/TASKS.md` to record its owner.

The current architecture is described in detail in:

```text
docs/autonomous-agent-blueprint.md
```

Loop-native runtime behavior is described in:

```text
docs/STAGE_R_LOOP.md
```

Keep this file as a short, current summary. Detailed design changes should be proposed through issues or rule-change proposals.
