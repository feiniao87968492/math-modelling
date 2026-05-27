# Time Budget Fixture - Improve With Low Remaining Budget

## Input scenario
- `time-budget.md` exists, total budget 72 h
- remaining budget 12 h (= 16.7%, below default 20% threshold)
- no advisory was emitted in the current stage yet
- main agent attempts `/math-modeling improve`

## State dict
```python
{
    "time_budget_present": True,
    "current_stage": 7,
    "current_stage_status": "in_progress",
    "stop_event_recorded_for_current_stage": False,
    "remaining_hours": 12,
    "total_hours": 72,
    "advisory_threshold_pct": 20,
    "hard_deadline_passed": False,
    "advisory_already_confirmed_this_stage": False,
    "command": "/math-modeling improve",
}
```

## Expected output
- `ok: False`
- `blockers` contains `time_pressure_advisory_required`
- `advisory` field present with `remaining_hours=12`, `remaining_pct=16.7`, `top_remaining_stages`
- `next_action` requires user to choose lower-claim-level / skip-optional / model-simplification before improve proceeds
- after user confirms once, the same command in the same stage skips the advisory (handled by `advisory_already_confirmed_this_stage: True` path; covered in test)

## Forbidden outcomes
- proceeding with `/math-modeling improve` without emitting advisory
- emitting advisory but allowing the command silently to proceed (must be explicit user confirmation)
- retriggering the advisory after a one-time confirmation in the same stage
