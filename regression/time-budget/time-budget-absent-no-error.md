# Time Budget Fixture - Time Budget Absent (v4.1 Behavior Unchanged)

## Input scenario
- `time-budget.md` does NOT exist in the project root
- main agent invokes `/math-modeling stage 5` or `/math-modeling improve` or `/math-modeling export`
- the project has not opted into the time-budget protocol

## State dict
```python
{
    "time_budget_present": False,
    "command": "/math-modeling stage 5",  # any command
}
```

## Expected output
- the dispatcher behavior is identical to v4.1
- `time_budget_check` returns `{"ok": True, "blockers": [], "applied": False}`
- no advisory, no burn-down requirement, no hard-deadline check

## Forbidden outcomes
- inventing a default deadline when `time-budget.md` is absent
- requiring users to opt out via a marker file (the protocol is opt-in, not opt-out)
- changing any other v4 / v4.1 behavior because of time-budget protocol existence

## Why this fixture exists
v4.2 plan explicitly requires that "未配置 `time-budget.md` 的项目，行为与 v4.1 完全一致". This fixture pins that contract.
