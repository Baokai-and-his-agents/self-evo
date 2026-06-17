# Exploration Policy

Exploration should be broad enough to discover useful paths, but always reviewable and decision-oriented.

## Core Principle

Do not repeat work that already exists.

Before building from scratch, perform an existing work survey:

- mature tutorials
- best-practice guides
- GitHub repositories
- libraries and tools
- templates
- example workflows
- case studies and retrospectives

## Exploration Program

When an issue describes a long-running direction, produce:

1. exploration brief
2. capability map
3. existing work survey
4. reuse map
5. candidate child tasks
6. decision options for the user

## Reuse Map

Write reuse maps under:

```text
data/exploration/reuse_maps/
```

Each reuse map should include:

- directly reusable resources
- resources that can be adapted or combined
- rejected resources and reasons
- missing parts that may require new work
- recommended next step

## Exploration Records

Use:

- `data/exploration/raw/` for raw links, search terms, and source notes
- `data/exploration/daily_reports/` for summaries
- `data/exploration/review_labels/` for user review labels
- `data/exploration/preference_analysis/` for later preference learning

## Output Standard

Exploration output must become a next action. Do not leave only a pile of notes.
