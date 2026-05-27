# Time Budget Fixture - Stage Switch Without Time Update

## Input scenario
- `time-budget.md` exists in the project root
- stage 4 is in_progress (per `## Stage allocation` row)
- main agent attempts `/math-modeling stage 5`
- but `/math-modeling time stop 4` was never invoked; burn-down log has no `stop` event for stage 4

## State dict
```python
{
    "time_budget_present": True,
    "current_stage": 4,
    "current_stage_status": "in_progress",
    "stop_event_recorded_for_current_stage": False,
    "remaining_hours": 60,
    "total_hours": 72,
    "advisory_threshold_pct": 20,
    "hard_deadline_passed": False,
    "command": "/math-modeling stage 5",
}
```

## Expected output
- `ok: False`
- `blockers` contains `previous_stage_not_stopped`
- `next_action` requires `/math-modeling time stop 4` before stage 5 starts

## Forbidden outcomes
- silently advancing to stage 5 while stage 4 row still says `in_progress`
- calculating Δh after-the-fact without explicit user invocation
- letting the burn-down log accumulate untracked time
