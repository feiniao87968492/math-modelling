# math-modeling-v4 Design

## Summary

`math-modeling-v4` is a new skill package that coexists with the existing `math-modeling` skill.

The new package keeps the 10-stage mathematical modeling workflow and the familiar `/math-modeling ...` command surface, but changes the runtime model from a YAML state-machine into a Markdown-first, rule-constrained, high-autonomy workflow:

> Main agent autonomy + hard workflow rules + Markdown audit documents + multi-expert review

The old skill is preserved unchanged. The new skill lives in its own directory and becomes the place for v4 experimentation and migration.

## Goals

- Create a new skill package at `C:\Users\zty\.agents\skills\math-modeling-v4`.
- Do not overwrite or break the existing `math-modeling` skill.
- Replace YAML state-machine execution with Markdown audit documents.
- Preserve the 10-stage checklist and user-facing command vocabulary.
- Keep hard blockers for user confirmation, readiness, rollback, claim grounding, and final evidence gate.
- Shift subagents from stage owners to expert reviewers.
- Make the main agent feel like a modeling lead rather than a schema-maintenance bot.

## Non-goals

- Do not refactor or delete the old `math-modeling` package.
- Do not remove the 10 modeling stages.
- Do not weaken safety gates just to increase autonomy.
- Do not let subagents independently clear blockers or raise claim strength.
- Do not require a compatibility bridge that keeps `modeling_state.yaml` as an active source of truth.

## Coexistence Strategy

The old and new skills must coexist.

| Package | Purpose |
|---|---|
| `math-modeling` | Stable existing skill, remains untouched. |
| `math-modeling-v4` | New Markdown-first skill for the redesigned runtime. |

Rules:

- No existing file inside `C:\Users\zty\.agents\skills\math-modeling` is modified as part of the new package setup.
- Any reused content must be copied into the new package and then evolved there.
- The new package may mention old concepts only in migration or historical notes.
- Old project folders that still contain `modeling_state.yaml` may treat it as historical context, not as the v4 workflow driver.

## Runtime Model

### Rule-First

The v4 orchestrator does not progress by writing stage enums such as `IN_PROGRESS` or `DONE`.

Instead, it:

1. identifies the active command and relevant checklist item,
2. reads the required protocol and stage references,
3. checks current blockers and claim limits from Markdown documents,
4. chooses the next safe work slice,
5. stops when a blocking user decision or unsupported claim is encountered.

### Markdown-First

Workflow state is represented by auditable Markdown documents:

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

### Expert-Review Mode

The main agent owns workflow synthesis, user-facing blocker handling, document updates, and continuation decisions.

Subagents become reviewers:

- fixed reviewers at major checkpoints,
- risk-triggered reviewers for data, code, figures, evidence, and literature.

They return findings and recommendations, but do not own stages.

## Command Surface

The new skill keeps the existing command vocabulary conceptually:

- `/math-modeling init`
- `/math-modeling progress`
- `/math-modeling next`
- `/math-modeling stage N`
- `/math-modeling pending`
- `/math-modeling confirm`
- `/math-modeling approve stage N`
- `/math-modeling reject stage N --reason "..."`
- `/math-modeling audit`
- `/math-modeling review`
- `/math-modeling gate`
- `/math-modeling export`

The commands now operate on Markdown audit documents rather than `modeling_state.yaml`.

## Required Audit Documents

### `workflow.md`

Navigation summary, not a state machine.

Minimum sections:

- `## Current focus`
- `## Checklist`
- `## Active blockers`
- `## Current claim ceiling`
- `## Next safe action`

### `decisions/decision-*.md`

Blocking decision documents with explicit confirmation record.

Minimum sections:

- `## Status`
- `## Why this blocks progress`
- `## Decision needed`
- `## Options`
- `## Recommended option`
- `## Impact scope`
- `## What will happen after confirmation`
- `## Confirmation record`

### `gates/*.md`

Readiness and evidence gate reports.

Minimum sections:

- `## Gate result`
- `## Intended claim level`
- `## Supported claim level`
- `## Checks`
- `## Allowed outputs`
- `## Blocked claims`
- `## Required branches`
- `## Required decision`

### `branches/*.md`

Actionable missing-input or missing-tool branches.

Minimum sections:

- `## Why this branch exists`
- `## Required for`
- `## Current blocker`
- `## Expected output`
- `## Status`
- `## Return condition`

### `rollbacks/*.md`

Controlled rollback requests.

Minimum sections:

- `## Trigger`
- `## Severity`
- `## Why downstream patching is not allowed`
- `## Evidence`
- `## Affected outputs`
- `## Recommended action`
- `## Requires user confirmation`
- `## Decision link`

### `claims/claim-registry.md`

Paper-facing claims and evidence binding. Claim strength must never exceed gate-supported strength.

### `reviews/*.md`

Expert reviewer outputs.

Minimum sections:

- `## Reviewed scope`
- `## Findings`
- `## Blocking risks`
- `## Non-blocking warnings`
- `## Required follow-up`
- `## Reviewer recommendation`

## Hard Rules

The v4 package must preserve these hard workflow boundaries:

1. User silence never counts as confirmation.
2. Any blocking decision must be written to a Markdown decision document.
3. Unconfirmed blocking decisions prevent dependent downstream work.
4. Stage 5 code writing requires implementation-readiness confirmation or equivalent explicit approval.
5. Missing data, solver capability, tool support, or evidence must trigger readiness handling before strong claims are produced.
6. Fallback that changes method, model structure, evidence path, or claim level must trigger a new blocking decision.
7. Stages 6-10 must not silently patch defects from stages 1-5; they must use rollback documents when required.
8. Claims must not exceed supported claim level.
9. `/math-modeling export` requires a passed final evidence gate.
10. Every meaningful work slice must end with a memory check.

## Fixed Review Points

| Workflow point | Reviewer |
|---|---|
| Before algorithm/model freeze | Algorithm/Model Reviewer |
| Before implementation/code writing | Implementation Readiness Reviewer |
| After main result generation | Validation Reviewer |
| Before claim/export | Evidence/Claim Reviewer |

## Risk-Triggered Reviewers

| Risk | Reviewer |
|---|---|
| unclear or inconsistent data | Data-Audit Reviewer |
| solver or reproducibility risk | Code-Review Reviewer |
| figure or caption risk | Figure-Review Reviewer |
| unsupported claims | Evidence-Gate Reviewer |
| missing method background | Literature/Method Reviewer |

## Implementation Strategy

The migration for the new skill is intentionally staged.

### Phase 1 — New package and core runtime contract

- Create `math-modeling-v4` package skeleton.
- Write new `SKILL.md`.
- Write new `CLAUDE.md`.
- Add `references/protocol-markdown-audit.md`.
- Add minimal contract regression tests.

### Phase 2 — Core protocol rewrite

- Human confirmation
- Readiness gate
- Rollback
- Memory update
- Expert review delegation

### Phase 3 — Runtime simulation and regression

- Markdown-first smoke flow
- Markdown-first command flow
- Contract tests for dispatcher and protocols

### Phase 4 — Stage contracts and package docs

- Rewrite stage docs into contract style
- Rewrite README
- Rewrite final evidence gate guidance
- Update scenario docs and scans

## Acceptance Criteria

The new package is acceptable when:

- `math-modeling-v4` exists as a separate skill package.
- The old `math-modeling` package remains untouched.
- The new dispatcher no longer depends on YAML stage-machine concepts.
- Blocking decisions, gates, branches, rollbacks, claims, and reviews are Markdown-first.
- Regression tests cover the new Markdown contract.
- The new package clearly enforces hard blockers without requiring `modeling_state.yaml`.

## Risks

### Risk 1: Documentation drift inside the new package

Mitigation: use regression tests for required phrases, headings, and forbidden old terms.

### Risk 2: Excessive autonomy causes over-progression

Mitigation: keep hard stop rules and claim ceilings explicit in protocols.

### Risk 3: Reviewer role becomes vague

Mitigation: define fixed review points, risk triggers, and forbidden reviewer behavior.

### Risk 4: Migration scope becomes too large in one step

Mitigation: implement the new package in phases, starting from runtime contracts and only then rewriting peripheral docs.
