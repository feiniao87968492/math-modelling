# Improve Flow Fixture - Precondition: Stage 7 Sensitivity Missing

## Input scenario
- active command: `/math-modeling improve`
- baseline-snapshot frozen
- Stage 6 PASS
- Stage 7 sensitivity report missing
- no pending decision, no in-progress round

## State dict
```python
{
    "stage6_review_pass": True,
    "baseline_snapshot_frozen": True,
    "stage7_sensitivity_present": False,
    "pending_decisions": [],
    "in_progress_round": False,
}
```

## Expected output
- `ok: False`
- `blockers` contains `stage7_sensitivity_missing`

## Forbidden outcomes
- starting improvement round on the strength of Stage 6 alone
- letting Critique receive a Required Reads list with no sensitivity report
