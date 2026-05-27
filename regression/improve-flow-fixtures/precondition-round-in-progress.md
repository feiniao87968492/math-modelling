# Improve Flow Fixture - Precondition: In-Progress Round

## Input scenario
- active command: `/math-modeling improve`
- baseline-snapshot frozen, Stage 7 present, Stage 6 PASS, no pending decision
- `improvements/round-1.md` exists with decision still PENDING (in-progress)

## State dict
```python
{
    "stage6_review_pass": True,
    "baseline_snapshot_frozen": True,
    "stage7_sensitivity_present": True,
    "pending_decisions": [],
    "in_progress_round": True,
}
```

## Expected output
- `ok: False`
- `blockers` contains `in_progress_round_present`

## Forbidden outcomes
- opening round-2 while round-1 is still PENDING
- silently overwriting round-1's decision document
