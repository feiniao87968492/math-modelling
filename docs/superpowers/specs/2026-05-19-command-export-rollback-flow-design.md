# Command Export And Rollback Flow Design

## Summary

This design adds command-level regression coverage for two user-facing behaviors in `math-modeling-v4`:

- `/math-modeling export`
- rollback-triggering late-stage review flow

The goal is to move these boundaries one level closer to runtime semantics by introducing command-flow helpers that match the style already used by `command_readiness_gate_flow.py`.

## Goal

Add deterministic command-flow regressions that verify:

1. export stays blocked when final gate or pending decisions are not clear,
2. rollback is required when late-stage review discovers an upstream structural defect,
3. both flows return the same style of metadata already used by the stage-5 command regression.

## Non-goals

- Do not redesign the dispatcher.
- Do not add real runtime command execution.
- Do not replace scenario regressions already added for readiness, gate, or rollback.
- Do not modify the legacy `math-modeling` skill.

## Why This Slice

The package already has:

- scenario regressions for readiness, rollback, export blocking, and final evidence gate,
- one command-style regression for `/math-modeling stage 5`.

The current gap is that:

- export and rollback are still tested mainly as scenario logic,
- there is not yet a command-level contract for how these commands should read references and report blockers.

This slice fills that gap without trying to simulate the entire workflow engine.

## Options Considered

### Option A - New command-flow helpers for export and rollback (recommended)

Add:

- `command_export_flow.py`
- `command_rollback_flow.py`
- two matching pytest modules

Pros:

- consistent with current stage-5 command regression,
- easy to understand and extend,
- separates command contracts from scenario contracts.

Cons:

- adds a few more files.

### Option B - Fold command behavior into scenario helpers

Pros:

- fewer files.

Cons:

- mixes scenario and command layers,
- harder to read and evolve.

### Option C - Tests only, no helper modules

Pros:

- smallest code surface.

Cons:

- weaker structure,
- less reusable than dedicated command helpers.

## Recommended Approach

Use Option A.

Keep the same return-shape style as `command_readiness_gate_flow.py`, but tailored to export and rollback semantics.

## Files

### Create

- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_export_flow.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\command_rollback_flow.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_export_command_flow.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_rollback_command_flow.py`

### Reuse as dependencies

- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\run_gate_and_rollback_checks.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\run_readiness_gate_checks.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\evidence-gate.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-rollback.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-subagent-delegation.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-10-paper-materials.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-8-visualization.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\stage-9-figure-review.md`

## Contract Style

The new helpers should return dictionaries with the same broad pattern as the existing command-flow helper:

- `ok`
- `command`
- `required_reads`
- `review_policy`
- artifact path fields

And then command-specific fields:

### Export flow fields

- `blockers`
- `gate_path`
- `export_allowed`

### Rollback flow fields

- `rollback_required`
- `rollback_path`
- `requires_user_confirmation`

## Export Flow Design

### Input

Command text:

- `/math-modeling export`

Scenario input:

- pending decisions may or may not exist,
- final evidence gate may be `PASS`, `PASS_WITH_WARNINGS`, or `BLOCKED`,
- claims may or may not be fully supported.

### Required reads

The helper should require existence of:

- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-readiness-gate.md`
- `references/protocol-rollback.md`
- `references/protocol-subagent-delegation.md`
- `references/evidence-gate.md`
- `references/stage-10-paper-materials.md`

### Output contract

If blockers exist, return:

- `ok: True`
- `export_allowed: False`
- `blockers: [...]`

If no blockers exist, return:

- `ok: True`
- `export_allowed: True`
- `blockers: []`

### Blocker rules

Export must be blocked when:

- pending decisions exist,
- final gate status is `BLOCKED`,
- claims are not supported.

## Rollback Flow Design

### Input

Command text:

- use a review-triggering flow such as `/math-modeling review`

Scenario input:

- stage is 8, 9, or 10,
- a late-stage review discovers a structural defect from upstream stages,
- downstream patching appears possible but must not be used.

### Required reads

The helper should require existence of:

- `references/protocol-markdown-audit.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/stage-8-visualization.md`
- `references/stage-9-figure-review.md`
- `references/subagent-validation-paper.md`

### Output contract

When structural defect exists:

- `ok: True`
- `rollback_required: True`
- `rollback_path: rollbacks/rollback-stage8-structural-defect.md`
- `requires_user_confirmation: True`

When no rollback is required:

- `ok: True`
- `rollback_required: False`
- `rollback_path: None`
- `requires_user_confirmation: False`

## Testing Strategy

Add two dedicated pytest modules.

### Export tests

- blocks when pending decision exists,
- blocks when final gate is blocked,
- blocks when claims are unsupported,
- allows export when all conditions are clear.

### Rollback tests

- requires rollback for structural defect,
- does not require rollback for non-structural or absent defect,
- returns required reads and reviewer policy fields.

Then run the full regression suite.

## Acceptance Criteria

This slice is complete when:

- the two command-flow helpers exist,
- the two new pytest modules exist,
- export and rollback command contracts are covered,
- full regression still passes.

## Risks

### Risk 1: command helper duplicates too much scenario logic

Mitigation: call the existing scenario helpers where useful, keep command helpers thin.

### Risk 2: command shape drifts from existing stage-5 helper

Mitigation: explicitly match the existing `ok / command / required_reads / review_policy` style.

### Risk 3: rollback command choice becomes ambiguous

Mitigation: document that the helper models a review-triggered rollback path using `/math-modeling review`.
