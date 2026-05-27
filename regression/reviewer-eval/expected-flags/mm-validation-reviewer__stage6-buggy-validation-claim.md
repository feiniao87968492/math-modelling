# Expected Flags - mm-validation-reviewer × stage6-buggy-validation-claim

## Required flags
- independent-reproduction-disagrees
- claim-level-exceeds-gate-ceiling

## Recommended additional flags
- baseline-snapshot-must-freeze-at-lower-claim-level
- validation-report-must-explain-reproduction-gap

## Verdict
BLOCKED

## Notes
independent-reproduction-disagrees is the headline flag — without it the reviewer effectively rubber-stamped the validation report. claim-level-exceeds-gate-ceiling is the second non-negotiable flag because the reviewer is the gatekeeper for first-PASS baseline freeze.
