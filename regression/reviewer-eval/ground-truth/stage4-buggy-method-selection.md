# Ground-Truth Fixture - Stage 4 Buggy Method Selection

## Reviewer under test
mm-algorithm-model-reviewer

## Buggy artifact summary
A `data/model-spec.md` claims to use a logistic regression for a regression target (continuous outcome). The target variable is described in `data/problem-analysis.md` as continuous (e.g., `predict daily WAPE between 0 and 1`), but the model spec writes a binary cross-entropy loss as if the target were classification.

## Ground-truth artifact paths (would-be inputs to the reviewer)
- `data/problem-analysis.md` — declares target as continuous
- `data/model-spec.md` — declares logistic regression with BCE loss
- `data/algorithm-selection.md` — recorded LR as the chosen algorithm with no caveat

## Buggy quotes
- "目标变量 WAPE 是连续值，落在 [0, 1] 区间内" (problem-analysis.md)
- "$\min_{w,b} \sum_i -[y_i \log \sigma(w^\top x_i + b) + (1-y_i) \log(1 - \sigma(\dots))]$" (model-spec.md)
- "Selected algorithm: Logistic Regression. Rationale: simple, interpretable, fast." (algorithm-selection.md)

## A profile-conformant Algorithm/Model Reviewer is expected to flag
- `regression-target-classified-as-binary` — BCE loss does not match continuous target
- `model-spec-mismatches-problem-statement` — header citation chain breaks
- `claim-level-cap` — cannot exceed `feasible_baseline` until algorithm is corrected

The expected-flags file lists the canonical flag set; reviewer outputs are scored as a subset relationship test.
