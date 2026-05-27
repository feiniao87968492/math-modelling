# Regression - Improvement Loop Requires Frozen Baseline

## Input Scenario

- active command: `/math-modeling improve`
- `gates/stage6-*` exists and concludes PASS or PASS_WITH_WARNINGS
- `claims/baseline-snapshot.md` does not exist
- no `improvements/round-N.md` in progress

## Expected Output

- the main agent stops before spawning Improvement-Critique Reviewer
- output path: short blocker explanation referencing `claims/baseline-snapshot.md` and `references/baseline-snapshot-template.md`
- recommended next action: complete Stage 6 baseline snapshot per `references/stage-6-independent-validation.md`

## Forbidden Outcomes

- spawning Improvement-Critique Reviewer without a baseline snapshot
- writing `improvements/round-N.md` Synthesized proposal section
- comparing the round against the previous round in absence of a frozen baseline
- silently regenerating a baseline snapshot from the current Stage 6 report after improvement work has already started
