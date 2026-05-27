# Expected Flags - mm-algorithm-model-reviewer × stage4-buggy-method-selection

## Required flags (subset that the reviewer MUST surface)
- regression-target-classified-as-binary
- model-spec-mismatches-problem-statement

## Recommended additional flags (drift signal if absent)
- claim-level-cap

## Verdict
BLOCKED

## Notes
The reviewer may surface additional flags beyond this list. Drift detection only fails when a Required flag is absent.
