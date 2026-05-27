# Protocol — Markdown Audit Documents

## Core Rule

`math-modeling-v4` is Markdown-first. The workflow is governed by Markdown audit documents, not by `modeling_state.yaml`, stage transition enums, or YAML confirmation queues.

## Required Project Documents

A v4 project should use these documents:

```text
workflow.md
memory.md
decisions/
gates/
branches/
rollbacks/
claims/claim-registry.md
reviews/
logs/workflow-trace.md
```

## Blocking Decision Documents

Blocking decisions live under `decisions/` and must include:

- `## Status`
- `## Why this blocks progress`
- `## Decision needed`
- `## Options`
- `## Recommended option`
- `## Impact scope`
- `## What will happen after confirmation`
- `## Confirmation record`

## Gate Documents

Gate reports live under `gates/` and must include:

- `## Gate result`
- `## Intended claim level`
- `## Supported claim level`
- `## Checks`
- `## Allowed outputs`
- `## Blocked claims`
- `## Required branches`
- `## Required decision`

## Workflow Navigation

`workflow.md` should summarize:

- current focus,
- checklist,
- active blockers,
- current claim ceiling,
- next safe action.

## Forbidden State-Machine Behavior

Do not drive v4 workflow by:

- global YAML state files,
- stage transition enums,
- YAML pending-confirmation queues,
- YAML confirmed-decision queues,
- declaring progress solely by writing a status value.
