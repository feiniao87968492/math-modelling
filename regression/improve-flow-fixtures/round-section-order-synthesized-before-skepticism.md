# Improve Flow Fixture - Round Section Order Violation

## Input scenario
- active command: `/math-modeling improve`
- preconditions all satisfied
- both Critique and Skepticism review files written
- main agent has filled `improvements/round-N.md` `## Implementation summary`,
  `## Before vs after metrics`, and `## Frontier update` sections
- but the user has NOT yet confirmed `decisions/decision-improvement-round-N.md`

## State dict
```python
{
    "stage6_review_pass": True,
    "baseline_snapshot_frozen": True,
    "stage7_sensitivity_present": True,
    "pending_decisions": [],
    "in_progress_round": False,
    "critique_review_present": True,
    "skepticism_review_present": True,
    "round_n_md": {
        "front_six_sections_present": True,
        "back_three_sections_present": True,
    },
    "decision_confirmed": False,
}
```

## Expected output
- `ok: False`
- `blockers` contains `round_n_back_sections_written_before_confirm`
- `next_action` requires removing `## Implementation summary` / `## Before vs after metrics` /
  `## Frontier update` sections; restoring `decisions/decision-improvement-round-N.md` to PENDING

## Forbidden outcomes
- letting `improvements/round-N.md` carry implementation summary without a confirmed decision
- treating early metric fill-in as harmless (it normalizes silent confirmation)
- promoting the round to frontier "Tried and kept" before user confirmation
