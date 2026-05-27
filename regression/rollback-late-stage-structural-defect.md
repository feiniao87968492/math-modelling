# Regression - Rollback Late Stage Structural Defect

## Input Scenario

- active stage is 8, 9, or 10
- late review discovers an earlier structural defect
- downstream patching would hide the original defect

## Expected Output

- status: `ROLLBACK_REQUIRED`
- rollback path: `rollbacks/rollback-stage8-structural-defect.md`
- user confirmation required

## Forbidden Outcomes

- patching downstream artifacts and continuing
- exporting while the structural defect remains unresolved
