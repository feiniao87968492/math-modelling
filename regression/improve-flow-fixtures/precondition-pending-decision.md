# Improve Flow Fixture - Precondition: Pending Decision

## Input scenario
- active command: `/math-modeling improve`
- baseline-snapshot frozen, Stage 7 present, Stage 6 PASS
- one pending decision in `decisions/decision-stage10-export.md`
- no in-progress round

## State dict
```python
{
    "stage6_review_pass": True,
    "baseline_snapshot_frozen": True,
    "stage7_sensitivity_present": True,
    "pending_decisions": ["decisions/decision-stage10-export.md"],
    "in_progress_round": False,
}
```

## Expected output
- `ok: False`
- `blockers` contains `pending_decision_present`

## Forbidden outcomes
- spawning Critique while a pending decision is unresolved
- treating an unrelated stage's pending decision as orthogonal to improve
