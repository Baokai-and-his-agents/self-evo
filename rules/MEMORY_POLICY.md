# Memory Policy

Memory is file-first, reviewable, and split into hot and cold zones.

## Hot Memory

Hot memory lives under:

```text
data/memory/hot/
```

Use it for frequently needed context:

- user preferences
- active project goals
- decisions
- reusable skills
- current learnings

New durable memory should normally start as a proposal before being merged into hot memory.

## Cold Memory

Cold memory lives under:

```text
data/memory/cold/
```

Use it for lower-frequency or archived content that should not load by default.

Before moving hot memory to cold memory:

1. Write a cooldown proposal under `data/memory/proposals/cooldown/`.
2. Notify the user in `data/tasks/REVIEW.md` or the relevant GitHub Issue.
3. Wait for approval.

## Memory Proposals

Write memory candidates under:

```text
data/memory/proposals/memory/
```

Do not convert a one-off failure into a permanent rule without review.

## Startup Loading Priority

Load in this order:

1. `rules/START_HERE.md`
2. Required rule files
3. current GitHub Issue
4. relevant hot memory
5. recent run summaries
6. cold memory only when needed
