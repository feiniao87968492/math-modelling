# Ground-Truth Fixture - Stage 6 Buggy Validation Claim

## Reviewer under test
mm-validation-reviewer

## Buggy artifact summary
Stage 6 validation report claims `Mean Accuracy = 0.83` from a 5-fold CV on titanic. Independent re-implementation in a separate notebook produces `Mean Accuracy = 0.79` on the same fold split. The discrepancy is not addressed in the validation report. Author proposes `validated_optimum` claim level despite Stage 4 readiness gate ceiling at `locally_optimal_solution`.

## Ground-truth artifact paths
- `data/validation/validation-report.md` — claims 0.83 mean accuracy
- `data/validation/cross-check-notebook.ipynb` — independent reproduction at 0.79
- `gates/stage4-model-readiness-gate.md` — ceiling = `locally_optimal_solution`
- `claims/claim-registry.md` — proposed claim level = `validated_optimum`

## Buggy quotes
- "5-fold StratifiedKFold (seed=42) Mean Accuracy: 0.83 ± 0.02" (validation-report.md)
- "Cross-check on same fold split: 0.79 ± 0.03" (cross-check-notebook ipynb cell 14)
- "Proposed claim level: validated_optimum" (claim-registry.md row C1)

## A profile-conformant Validation Reviewer is expected to flag
- `independent-reproduction-disagrees` — 4pp gap between primary and independent runs
- `claim-level-exceeds-gate-ceiling` — `validated_optimum` not supported by Stage 4 ceiling
- `baseline-snapshot-must-freeze-at-lower-claim-level` — first PASS should freeze at most `locally_optimal_solution`, here the gap means PASS_WITH_WARNINGS at `feasible_baseline` is the upper bound
- `validation-report-must-explain-reproduction-gap`
