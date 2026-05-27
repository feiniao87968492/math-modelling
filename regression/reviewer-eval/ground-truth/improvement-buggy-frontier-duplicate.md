# Ground-Truth Fixture - Improvement Buggy Frontier Duplicate

## Reviewer under test
mm-improvement-skepticism-reviewer

## Buggy artifact summary
Round-3 Critique reviewer proposes `F1: replace LR with HistGradientBoosting`. The same proposal already exists in `improvements/improvement-frontier.md` under "Tried and reverted" (round-1, reverted because cross-question regression on Q2). Critique did not acknowledge the prior frontier entry and re-proposes the change as if it were novel.

## Ground-truth artifact paths
- `reviews/improvement-round-3-critique.md` — F1 proposes HGBT replacement, no mention of round-1
- `improvements/improvement-frontier.md` — "Tried and reverted" lists `HGBT replacement (round-1, reverted because Q2 regression)`
- `improvements/round-1.md` — closed as `reverted` with reason
- `improvements/improvement-log.md` — Round 1 status = reverted

## Buggy quotes
- "F1 — Replace LR with HistGradientBoostingClassifier. Hypothesis: +1.0pp Mean Accuracy on Q1." (improvement-round-3-critique.md)
- "Tried and reverted: HGBT replacement (round-1, Q2 obj regressed by 3.2%)" (improvement-frontier.md)

## A profile-conformant Improvement-Skepticism Reviewer is expected to flag
- `frontier-duplicate-not-acknowledged` — Critique F1 collides with frontier "Tried and reverted" entry
- `previous-revert-reason-not-addressed` — Q2 regression that triggered round-1 revert is not discussed
- `must-recommend-decision-or-rollback` — per protocol-improvement-loop.md, contradicts an existing frontier entry → mandatory decision
- Required mitigation: open a decision document explicitly addressing the round-1 revert reason; do not enter implementation until user confirms whether the new round resolves the prior revert cause
