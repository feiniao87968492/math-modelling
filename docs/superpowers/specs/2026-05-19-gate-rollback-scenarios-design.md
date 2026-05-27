# Gate And Rollback Scenarios Design

## Summary

This design defines the fourth implementation slice for `math-modeling-v4`.

Scope is intentionally narrow:

- add scenario regressions for rollback behavior,
- add scenario regressions for export blocking,
- add scenario regressions for final evidence gate pass criteria.

This slice does not redesign dispatcher semantics. It extends regression coverage around the highest-risk behaviors that could silently regress while the package keeps evolving.

## Goal

Lock down three workflow guarantees:

1. late-stage structural defects must trigger rollback instead of silent downstream patching,
2. export must stay blocked when decisions or evidence gates are not clear,
3. final evidence gate may pass only when claims are grounded by aligned Markdown evidence.

## Non-goals

- Do not rewrite `SKILL.md` command examples yet.
- Do not add a new dispatcher implementation layer.
- Do not replace existing smoke or stage-5 command regressions.
- Do not modify the old `math-modeling` skill.

## Why This Slice

Current `math-modeling-v4` already covers:

- dispatcher contract,
- Markdown-first protocol existence,
- stage contract structure,
- stage-5 readiness smoke flow,
- stage-5 command flow,
- readiness gate scenarios.

The most dangerous uncovered behaviors are downstream:

- rollback can accidentally become optional,
- export can accidentally bypass blockers,
- final evidence gate can accidentally become a prose-only check.

These are high-value regression targets because they guard paper-facing outputs.

## Approach Options

### Option A - Scenario regressions only

Add one new checker and one new test file, backed by three scenario Markdown documents.

Pros:

- smallest change surface,
- fastest signal,
- strong protection around core failure modes.

Cons:

- does not yet simulate `/math-modeling export` as a separate command flow.

### Option B - Scenario regressions plus command simulators

Add scenario regressions and new `command_export_flow.py` or `command_rollback_flow.py`.

Pros:

- closer to dispatcher runtime.

Cons:

- broader scope,
- more moving parts,
- higher review cost.

### Option C - Full docs plus regressions

Update scenario regressions and enrich `SKILL.md` with command examples in the same slice.

Pros:

- more user-facing completeness.

Cons:

- mixes behavior locking with documentation expansion,
- makes failures harder to localize.

## Recommended Approach

Choose Option A.

Reason:

- it protects the most failure-prone boundaries first,
- it keeps this phase surgical,
- it fits the current v4 bootstrap pattern where behavior is locked by small deterministic regression helpers.

## Files

### Create

- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\run_gate_and_rollback_checks.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_gate_and_rollback_checks.py`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\rollback-late-stage-structural-defect.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\export-blocked-by-pending-decision.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\final-evidence-gate-grounded-claims-only.md`

### Modify

- `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`

## Runtime Contract

### Rollback scenario contract

Input pattern:

- current stage is 6, 7, 8, 9, or 10,
- downstream review discovers a structural defect from stages 1-5,
- downstream patching would hide or bypass the original defect.

Expected output:

- result is `ROLLBACK_REQUIRED`,
- a rollback document path under `rollbacks/` is returned,
- downstream continuation is blocked until user confirmation if structural revision is required.

Forbidden behavior:

- patching later-stage artifacts and continuing,
- marking export-ready while earlier-stage defect remains unresolved.

### Export blocking contract

Input pattern:

- a pending decision exists, or
- final evidence gate is blocked, or
- claim registry exceeds supported claim level.

Expected output:

- export result is `BLOCKED`,
- blocker list is explicit,
- no export-ready status is emitted.

Forbidden behavior:

- exporting with pending decisions,
- exporting with blocked final gate,
- exporting with unsupported claims.

### Final evidence gate contract

Input pattern:

- claim registry exists,
- relevant reviews and gates exist,
- decision status is known.

Expected output:

- gate may return `PASS` or `PASS_WITH_WARNINGS` only when claims are aligned with evidence,
- blocked claims or missing evidence force `BLOCKED`.

Forbidden behavior:

- passing the gate using prose claims without aligned evidence records,
- passing the gate while blocked decisions remain.

## Checker Design

`run_gate_and_rollback_checks.py` should expose small deterministic helpers:

- `check_required_references(root: Path) -> dict`
- `simulate_rollback_decision(scenario: dict) -> dict`
- `simulate_export_gate(scenario: dict) -> dict`
- `simulate_final_evidence_gate(scenario: dict) -> dict`

The helper outputs should stay simple dictionaries, following the current bootstrap regression style.

## Scenario Markdown Design

Each scenario file should contain:

- `## Input Scenario`
- `## Expected Output`
- `## Forbidden Outcomes`

The scenarios are documentation-plus-regression anchors, not executable parsers.

## Testing Strategy

Add a new pytest module that verifies:

1. scenario references are present,
2. late-stage structural defect returns rollback-required status,
3. export stays blocked with pending decisions or blocked final gate,
4. final evidence gate passes only when claims and evidence align.

Then run the full regression suite:

```powershell
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py -q
```

## Acceptance Criteria

This slice is complete when:

- the new checker and tests exist,
- three scenario docs exist,
- all new tests pass,
- full v4 regression passes,
- rollback/export/evidence-gate boundaries are explicitly locked.

## Risks

### Risk 1: checker duplicates too much protocol logic

Mitigation: keep helpers deterministic and boundary-focused; do not simulate the entire workflow.

### Risk 2: scenario docs drift from helper logic

Mitigation: required reference checks should assert key phrases and paths.

### Risk 3: export contract becomes too broad

Mitigation: limit this slice to pending decisions, blocked final gate, and unsupported claims.
