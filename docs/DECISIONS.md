# Decisions

This file records confirmed long-term design decisions.

## 2026-06-18

- GitHub Issues are the primary task entrypoint.
- `rules/**` is the read-only rule zone for agents.
- `data/**` is the writable work zone for agents.
- `rules/START_HERE.md` is the single startup entrypoint for a local Code worker.
- `rules/AGENT_PROTOCOL.md` is the full operating manual.
- Agents must search for mature existing solutions before building from scratch.
- Human approval is represented by changes to `rules/**`, especially resource approvals.
