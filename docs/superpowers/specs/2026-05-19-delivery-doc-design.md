# Delivery Doc Design

## Summary

This design defines the final packaging-oriented documentation slice for `math-modeling-v4`.

The purpose is to make the package easier to hand off, evaluate, and trial by adding a dedicated delivery document that summarizes what the package currently supports, how it should be tried, what regression coverage exists, and what boundaries still remain.

This slice is documentation-focused and intentionally small.

## Goal

Add a package-level delivery document so that a reader can quickly answer:

- what `math-modeling-v4` can do right now,
- what kinds of projects it fits,
- what has already been regression-tested,
- what is still simulated rather than fully runtime-driven,
- how to trial it safely.

## Non-goals

- Do not add new runtime behavior.
- Do not add new regression helpers unless needed for a minimal doc contract check.
- Do not redesign `README.md` or `SKILL.md`.
- Do not modify the legacy `math-modeling` package.
- Do not create a full changelog or release management system.

## Why This Slice

The package now already includes:

- Markdown-first dispatcher and protocols,
- stage contracts,
- scenario regressions,
- command-flow regressions,
- quickstart onboarding docs.

What it still lacks is a package-level handoff document for trial adoption.

Right now, a new reader can learn how to use it, but still has to infer:

- how complete the package is,
- which pieces are most mature,
- where the current boundaries are,
- how to evaluate readiness for real trial usage.

## Recommended Approach

Add one focused root-level document:

- `DELIVERY.md`

Then add a small entry point in `README.md` so the document is discoverable.

This keeps:

- `SKILL.md` focused on orchestration behavior,
- `README.md` focused on onboarding,
- `DELIVERY.md` focused on handoff and evaluation.

## Options Considered

### Option A - Add `DELIVERY.md` and a README entry (recommended)

Pros:

- clean separation of concerns,
- easy to scan,
- suitable for trial handoff.

Cons:

- one more root-level document.

### Option B - Put delivery content into `README.md`

Pros:

- fewer files.

Cons:

- README becomes crowded,
- onboarding and delivery evaluation mix together.

### Option C - Add only a regression index

Pros:

- stronger testing navigation.

Cons:

- does not solve handoff clarity,
- weaker for trial decision-making.

## Document Structure

### `DELIVERY.md`

Recommended sections:

- `## 当前版本能力`
- `## 适合怎么试用`
- `## 回归覆盖概览`
- `## 已知边界`
- `## 推荐下一步`

### `README.md`

Add a short entry section that points to `DELIVERY.md`, for example:

- current trial status,
- where to read the handoff summary,
- recommendation to read `DELIVERY.md` before formal trial use.

## Content Requirements

### `当前版本能力`

Should summarize:

- dispatcher and protocol availability,
- stage contract coverage,
- readiness/gate/rollback/export scenario coverage,
- stage-5/export/rollback command-flow coverage,
- quickstart availability.

### `适合怎么试用`

Should explain:

- start with a new small project,
- prefer low-risk practice topics before full contest workflows,
- use the documented command path from `README.md`,
- treat current command-flow helpers as regression contracts, not full runtime execution.

### `回归覆盖概览`

Should group regression types:

- contract tests,
- smoke flow,
- readiness gate,
- gate and rollback scenarios,
- export and rollback command-flow.

### `已知边界`

Should explicitly state:

- some helpers are deterministic simulation layers,
- not every command has a full command-flow helper yet,
- real-world trial should still start with a controlled small project.

### `推荐下一步`

Should suggest:

- use one small new project as pilot,
- collect gaps encountered during trial,
- decide later whether to build a more complete runtime execution layer.

## Testing Strategy

Add only minimal documentation contract checks.

Extend `regression/test_markdown_first_contracts.py` so that:

- `README.md` contains a delivery-doc entry,
- `DELIVERY.md` exists and contains the key sections.

Then run the existing full regression suite.

## Acceptance Criteria

This slice is complete when:

- `DELIVERY.md` exists,
- `README.md` links or points to it clearly,
- the document explains current capability, fit-for-trial guidance, regression coverage, and boundaries,
- minimal doc contract tests pass,
- full regression still passes.

## Risks

### Risk 1: duplicate too much content from README

Mitigation: keep `README.md` as onboarding and keep `DELIVERY.md` as evaluation/handoff only.

### Risk 2: delivery document becomes vague marketing text

Mitigation: require concrete coverage and boundary sections.

### Risk 3: delivery document drifts as the package evolves

Mitigation: add a small doc contract test and keep the sections stable.
