# Improve Flow Fixture - Round Close Without Frontier Update

## Input scenario
- active command: `/math-modeling improve close`
- decision-improvement-round-N.md was confirmed
- `improvements/round-N.md` `## Implementation summary` and `## Before vs after metrics` filled
- `improvements/round-N.md` `## Frontier update` section also filled
- BUT `improvements/improvement-frontier.md` not actually updated on disk
- Stage 6 validation NOT yet rerun

## State dict
```python
{
    "decision_confirmed": True,
    "round_n_md": {
        "implementation_summary_filled": True,
        "before_vs_after_metrics_filled": True,
        "frontier_update_filled": True,
    },
    "improvement_log_updated": True,
    "improvement_frontier_updated": False,
    "stage6_validation_rerun": False,
}
```

## Expected output
- `ok: False`
- `blockers` contains both `improvement_frontier_not_updated` and `stage6_validation_not_rerun`
- `next_action` requires filling the missing artifacts before close

## Forbidden outcomes
- closing the round while the frontier file does not reflect "Tried and kept" / "reverted" / "Abandoned" status
- skipping Stage 6 validation rerun on the post-implementation result
- letting Final Evidence Gate run on stale frontier state
