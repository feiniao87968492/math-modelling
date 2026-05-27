# Ground-Truth Fixture - Stage 10 Buggy Paper Grounding

## Reviewer under test
mm-evidence-claim-reviewer

## Buggy artifact summary
Paper draft claims "WAPE reduced by 23%" but `claims/claim-registry.md` has no entry for relative WAPE reduction. The closest registered claim is `c-q1-wape-baseline = 0.288` with claim level `feasible_baseline`. Paper also includes a figure `figures/q1-residuals.png` referenced in body without `.meta.json` sibling. Stage 9 figure review file is missing.

## Ground-truth artifact paths
- `paper/main.md` — body cites "WAPE 减少 23%" without anchor
- `claims/claim-registry.md` — registers `c-q1-wape-baseline` only, no reduction-percentage row
- `figures/q1-residuals.png` — exists; `figures/q1-residuals.meta.json` missing
- `reviews/stage9-figure-review.md` — does NOT exist
- `gates/final-evidence-gate.md` — does NOT yet exist

## Buggy quotes
- "我们的方法将 WAPE 降低了 23%" (paper/main.md, no anchor preceding)
- "c-q1-wape-baseline | 0.288 | feasible_baseline" (claim-registry.md)

## A profile-conformant Evidence/Claim Reviewer is expected to flag
- `paper-claim-without-registry-entry` — "23% reduction" not registered
- `figure-without-meta-json` — q1-residuals.png lacks meta.json sibling
- `stage9-figure-review-missing` — fixed-review point unsatisfied
- `claim-level-cap` — `feasible_baseline` cannot support a "23% reduction" claim without a new readiness gate
- Verdict suggestion: BLOCKED
