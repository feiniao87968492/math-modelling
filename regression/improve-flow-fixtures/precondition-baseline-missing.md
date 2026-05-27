# Improve Flow Fixture - Precondition: Baseline Snapshot Missing

## Input scenario
- active command: `/math-modeling improve`
- `claims/baseline-snapshot.md` does NOT exist
- Stage 6 review concluded PASS_WITH_WARNINGS
- Stage 7 sensitivity present
- no pending decision
- no in-progress round

## State dict
```python
{
    "stage6_review_pass": True,
    "baseline_snapshot_frozen": False,
    "stage7_sensitivity_present": True,
    "pending_decisions": [],
    "in_progress_round": False,
    "critique_review_present": False,
    "skepticism_review_present": False,
}
```

## Expected output
- `ok: False`
- `blockers` contains `baseline_snapshot_missing`
- `next_action` instructs the main agent to write a blocker explanation; do not spawn Critique

## Forbidden outcomes
- proceeding to emit Critique invocation template
- treating Stage 6 PASS alone as sufficient to start improvement loop
