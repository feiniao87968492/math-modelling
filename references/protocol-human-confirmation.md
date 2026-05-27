# Protocol — Human Confirmation

## Core Rule

Every blocking user decision must be recorded as a Decision Markdown document under `decisions/`. User silence never counts as confirmation.

## Decision Markdown Required Sections

A blocking decision document must include:

- `## Status`
- `## Why this blocks progress`
- `## Decision needed`
- `## Options`
- `## Recommended option`
- `## Impact scope`
- `## What will happen after confirmation`
- `## Confirmation record`

## Blocking Nodes

| Stage | Decision type | Blocking |
|---|---|---|
| 1 | problem interpretation | true |
| 2 | algorithm route selection | true |
| 3 | innovation claim selection | true |
| 4 | model assumptions and constraints | true |
| 5 | implementation readiness | true |
| 10 | final claims and export | true |

## Confirmation Record Template

```markdown
## Confirmation record
- Confirmed at: 2026-05-26
- User selected: B
- Decision summary: Continue with heuristic baseline.
- Allowed claim level: feasible_baseline
```

## Command Contract

- `/math-modeling pending`: list pending decision documents.
- `/math-modeling confirm`: append or update a confirmation record.
- `/math-modeling approve stage N`: normalize to confirmation of the recommended option.
- `/math-modeling reject stage N --reason "..."`: append a rejection record and keep downstream work blocked.

## Allowed Output While Blocked

Allowed:

- decision summary,
- options and recommendation,
- risks and impact scope,
- exact reply formats the user can use.

Forbidden:

- treating recommendation as accepted,
- continuing dependent downstream artifacts,
- treating user silence as approval.
