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
- The agent GitHub account `clawbie` should have write permission, not admin permission.
- Organization members receive no repository access by default; agent access is granted explicitly per repository.
- A worker that changes tracked files must create its own draft PR; `jlcbk` reviews and merges it.
- Entering `status:review` requires releasing the active claim, ending the heartbeat, and synchronizing the local task mirror.
- Read-only access to public web pages, public search, and public documentation is approved.
- Multi-agent concurrency testing is deferred until additional workers are connected.
