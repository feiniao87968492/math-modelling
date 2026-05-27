# Improve Flow Fixture - Reviewer Order Violation

## Input scenario
- active command: `/math-modeling improve`
- preconditions all satisfied
- main agent attempts to spawn Skepticism reviewer before Critique writes its review file
- `reviews/improvement-round-N-critique.md` does NOT exist yet
- `reviews/improvement-round-N-skepticism.md` does NOT exist yet

## State dict (when dispatcher is called for the first time)
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

## Expected output
- `ok: True`
- `next_action` instructs Critique invocation template (NOT Skepticism)
- `expected_output_path` is `reviews/improvement-round-N-critique.md`

## Forbidden outcomes
- emitting a Skepticism invocation template before any Critique file exists
- letting Skepticism Required Reads omit the Critique path
- the dispatcher allowing parallel reviewer spawn (Critique || Skepticism)
