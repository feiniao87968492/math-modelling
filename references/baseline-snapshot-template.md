# Baseline Snapshot Template

## Purpose

Freeze the primary metrics of the first Stage 6 PASS so all later improvement rounds compare against the same fixed reference.

## File

`claims/baseline-snapshot.md`

## When To Write

Stage 6 must write this file the first time a validation review concludes PASS or PASS_WITH_WARNINGS. The Stage 6 contract Done When list includes this file.

## Required Sections

- `## Frozen at`
- `## Primary metrics`
- `## Claim level`
- `## Reproducibility anchor`

## Template

```markdown
# Baseline Snapshot

## Frozen at
- Stage: 6
- Date: YYYY-MM-DD
- Validation review: reviews/stage6-validation-review.md

## Primary metrics
| Metric | Value | Source artifact |
|---|---|---|
| <metric A> | <value> | data/validation/validation-report.md |
| <metric B> | <value> | data/results/<file>.csv |

## Claim level
- <claim level the Stage 6 review concluded at>

## Reproducibility anchor
- Code commit: <sha>
- Input dataset hash: <hash>
- Solver version: <version>
- Random seed (if any): <seed>
```

## Forbidden Behavior

- Do not overwrite this file in later rounds. Once frozen, only `improvements/round-N.md` records changes.
- Do not list metrics that the Stage 6 validation review did not actually report.
- Do not declare a claim level higher than the Stage 6 review concluded.

## Why This Matters

Without a frozen baseline, improvement rounds drift into "feels better than last time" comparisons. v4.1 enforces baseline-anchored comparison through this snapshot.
