# Time Budget Fixture - Export Past Hard Deadline

## Input scenario
- `time-budget.md` exists with `## Hard deadline: 2026-05-27 23:59`
- current time is 2026-05-28 00:30 (past hard deadline)
- main agent attempts `/math-modeling export`
- Final Evidence Gate would otherwise pass (no pending decision, claims grounded, etc.)

## State dict
```python
{
    "time_budget_present": True,
    "current_stage": 10,
    "current_stage_status": "in_progress",
    "stop_event_recorded_for_current_stage": True,
    "remaining_hours": 0,
    "total_hours": 72,
    "advisory_threshold_pct": 20,
    "hard_deadline_passed": True,
    "command": "/math-modeling export",
}
```

## Expected output
- `ok: False`
- `blockers` contains `hard_deadline_passed`
- `next_action` requires the user to either explicitly extend the deadline (with acknowledgment) or accept the export as overdue
- the dispatcher must NOT auto-extend the deadline

## Forbidden outcomes
- letting export proceed because Final Evidence Gate would pass
- silently shifting the `## Hard deadline` field
- treating the deadline as advisory rather than hard
