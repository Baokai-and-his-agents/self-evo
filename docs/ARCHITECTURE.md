# Architecture

This repository is organized around four planes:

- `rules/`: read-only operating rules for agents
- `data/`: writable workspace for task outputs, memory, notes, and exploration
- `state/`: runtime claims, locks, and heartbeat files
- `.github/`: GitHub coordination templates and review boundaries

The current architecture is described in detail in:

```text
docs/autonomous-agent-blueprint.md
```

Loop-native runtime behavior is described in:

```text
docs/STAGE_R_LOOP.md
```

Keep this file as a short, current summary. Detailed design changes should be proposed through issues or rule-change proposals.
