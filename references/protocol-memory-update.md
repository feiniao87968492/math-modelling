# Protocol — Memory Update

## Core Rule

`memory.md` is mandatory. Every meaningful work slice must read memory before acting and run a memory check before finishing.

## Pre-Work Read Rule

1. Prefer the project root `memory.md`.
2. If the project has no `memory.md`, read `references/modeling-memory-template.md`.
3. Apply relevant memory rules as extra gates for the current work slice.

## Memory Check

Before finishing a meaningful work slice, decide whether the work discovered:

1. a reusable modeling rule,
2. a recurring pitfall,
3. a counterexample,
4. a durable user preference.

If none apply, record exactly: `Memory check: no new memory`.

## Markdown Record Locations

A memory check must be recorded in one of:

- `workflow.md`,
- the relevant decision document,
- the relevant gate document,
- the relevant review document,
- `logs/workflow-trace.md`.

## Allowed Memory Categories

- Rules
- Pitfalls
- Counterexamples
- User Preferences

## Forbidden Content

Do not write:

- daily summaries,
- stage logs,
- one-off temporary details,
- raw file path lists.
