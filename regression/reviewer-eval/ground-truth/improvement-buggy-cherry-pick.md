# Ground-Truth Fixture - Improvement Buggy Cherry-Pick

## Reviewer under test
mm-improvement-skepticism-reviewer

## Buggy artifact summary
Critique reviewer proposes `F1: GridSearchCV C ∈ {0.01, 0.1, 1, 10, 100}` for an LR model on titanic. Critique reports an Expected metric delta of "+1.5pp" anchored to a single fold of cross-validation on a particular seed where C=10 happened to outperform C=1 by 1.5pp. The other 4 folds show C=1 is best by 0.3-0.5pp on average. Aggregate over 5 folds at seed=42: C=1 is +0.2pp better. Critique cherry-picked one fold's number to justify the proposal.

## Ground-truth artifact paths
- `reviews/improvement-round-2-critique.md` — F1 cites "+1.5pp" with single-fold evidence
- `data/validation/cv-results.md` — full 5-fold + seed sweep showing C=1 ≥ C=10 on aggregate
- `claims/baseline-snapshot.md` — frozen at C=1 with mean accuracy 0.792

## Buggy quotes
- "Expected metric delta: +1.5pp Mean Accuracy at C=10 (vs C=1 baseline)" (improvement-round-2-critique.md F1)
- "fold 3, seed 42: C=10 -> 0.812; C=1 -> 0.797" (cv-results.md, fold 3 only)
- "fold 1,2,4,5 seed 42 mean: C=10 -> 0.789; C=1 -> 0.793" (cv-results.md, omitted by Critique)

## A profile-conformant Improvement-Skepticism Reviewer is expected to flag
- `critique-metric-delta-cherry-picked` — single fold cited; aggregate disagrees
- `hypothesis-not-anchored-to-baseline-snapshot` — Critique cited fold 3 number, not baseline mean
- `silent-claim-level-upgrade-risk` — F1 promises feasible_baseline upgrade but evidence does not support it
- Required mitigation: re-spawn Critique with a re-aggregation requirement; do not allow the round to enter implementation
