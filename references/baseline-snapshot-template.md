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

## Per-Question Baseline (v4.2)

Multi-question competitions (Q1 / Q2 / Q3 / ...) must NOT collapse all problems into a single metric table. Single-question projects keep the single-table form above. Multi-question projects use the index + per-question form below.

### When to switch to per-question

Switch when any of:

- the project has more than one question (Q1, Q2, Q3, ...) declared in `data/problem-analysis.md`
- any improvement round in `improvements/round-N.md` declares `Target question` other than `all`
- a Stage 6 review reports separate metrics per question rather than a single aggregate metric

### File layout

```text
claims/baseline-snapshot.md          ← index file, lists per-question files
claims/baseline-q1.md                ← Q1 baseline frozen at Stage 6 first PASS for Q1
claims/baseline-q2.md                ← Q2 baseline frozen at Stage 6 first PASS for Q2
claims/baseline-q3.md                ← ...
```

### Index template (`claims/baseline-snapshot.md` in multi-question form)

```markdown
# Baseline Snapshot Index

## Frozen at
- Stage: 6
- Date: YYYY-MM-DD
- Validation review: reviews/stage6-validation-review.md

## Per-question baselines
| Question | Per-question file | Primary metric | Claim level |
|---|---|---|---|
| Q1 | claims/baseline-q1.md | <metric> | <claim level> |
| Q2 | claims/baseline-q2.md | <metric> | <claim level> |
| Q3 | claims/baseline-q3.md | <metric> | <claim level> |

## Cross-question coupling
- Shared inputs / constraints / decision variables that cause Qi to affect Qj when changed.
- Example: Q3 device purchase changes the equipment pool that Q2 packaging rules consume.

## Reproducibility anchor
- Code commit: <sha>
- Input dataset hash: <hash>
- Solver version: <version>
- Random seed (if any): <seed>
```

### Per-question template (`claims/baseline-qK.md`)

```markdown
# Baseline — Q<K>

## Frozen at
- Stage: 6
- Date: YYYY-MM-DD
- Validation review section: reviews/stage6-validation-review.md#q<k>

## Primary metrics
| Metric | Value | Source artifact |
|---|---|---|
| <Q<K> primary metric A> | <value> | data/validation/validation-report.md#q<k> |
| <Q<K> primary metric B> | <value> | data/results/<file>.csv |

## Claim level
- <claim level the Stage 6 review concluded for this question>

## Cross-question impact (if any)
- Lists other Qj whose baseline could move if this Q's solution changes.
```

### Per-question forbidden behavior

- Do not overwrite `claims/baseline-qK.md` after the first Stage 6 PASS for that question. Subsequent changes belong in `improvements/round-N.md` per `protocol-improvement-loop.md`.
- Do not merge per-question baselines into a single flat table; the index file references them but does not duplicate metric rows.
- Do not declare a Q<K> claim level higher than its own Stage 6 review concluded, even if a different Q's review concluded higher.
