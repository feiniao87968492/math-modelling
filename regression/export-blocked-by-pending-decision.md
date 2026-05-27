# Regression - Export Blocked By Pending Decision

## Input Scenario

- export is requested
- `decisions/decision-stage10-export.md` is still pending
- final gate may otherwise look passable

## Expected Output

- status: `BLOCKED`
- blocker: `pending_decisions`
- do not emit export-ready state

## Forbidden Outcomes

- exporting with a pending decision
- treating silence as approval
