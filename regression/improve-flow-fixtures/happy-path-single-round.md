# Improve Flow Fixture - Happy Path Single Round

## Input scenario
A complete improvement round walked through end-to-end without violations:
1. preconditions satisfied
2. Critique invocation emitted, file written
3. Skepticism invocation emitted (with Critique path in Required Reads), file written
4. round-N.md front 6 sections written; decision-improvement-round-N.md PENDING
5. user confirms
6. implementation lands; round-N.md back 3 sections filled
7. improvement-frontier.md and improvement-log.md updated
8. Stage 6 validation rerun
9. `/math-modeling improve close` invoked

## Sub-state for each stage of the dispatcher call sequence
The harness exercises the dispatcher at multiple synthetic checkpoints:

### Checkpoint A — opening (no reviews yet)
```python
{
    "stage6_review_pass": True,
    "baseline_snapshot_frozen": True,
    "stage7_sensitivity_present": True,
    "pending_decisions": [],
    "in_progress_round": False,
    "critique_review_present": False,
    "skepticism_review_present": False,
}
```
Expected: `ok=True`, `next_action` mentions "Improvement-Critique Reviewer".

### Checkpoint B — Critique written, Skepticism missing
Same as A plus `critique_review_present: True`.
Expected: `ok=True`, `next_action` mentions "Improvement-Skepticism Reviewer".

### Checkpoint C — both reviews written, round-N.md not synthesized
Add `skepticism_review_present: True` and empty `round_n_md`.
Expected: `ok=True`, `next_action` mentions "synthesize round-N.md front 6 sections".

### Checkpoint D — front 6 sections written, awaiting confirm
Add `round_n_md: {"front_six_sections_present": True, "back_three_sections_present": False}` and `decision_confirmed: False`.
Expected: `ok=True`, `blockers=["awaiting_user_confirmation"]`.

### Checkpoint E — confirm received
Set `decision_confirmed: True`.
Expected: `ok=True`, `next_action` mentions "route confirmed change via rollback if needed".

### Checkpoint F — close after full implementation
```python
{
    "decision_confirmed": True,
    "round_n_md": {
        "implementation_summary_filled": True,
        "before_vs_after_metrics_filled": True,
        "frontier_update_filled": True,
    },
    "improvement_log_updated": True,
    "improvement_frontier_updated": True,
    "stage6_validation_rerun": True,
}
```
Expected: `ok=True` for `/math-modeling improve close`.

## Forbidden outcomes
- any `ok=False` result on the happy path checkpoints
- divergence from the documented `next_action` strings (the strings are part of the contract)
