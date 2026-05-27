# Improvements Templates

## Purpose

Define the Markdown templates used by the v4.1 improvement loop. The main agent populates these templates inside the project `improvements/` directory. They are audit documents, not state-machine fields.

## Files

| Template | Path under project |
|---|---|
| Improvement log | `improvements/improvement-log.md` |
| Improvement frontier | `improvements/improvement-frontier.md` |
| Single-round record | `improvements/round-N.md` |

## improvement-log.md Template

```markdown
# Improvement Log

## Conventions

- Round 0 is always the frozen baseline.
- A round may be in `proposed`, `confirmed`, `implemented`, `rejected`, or `reverted` state.
- Rejected and reverted rounds remain in the log permanently.

## Rounds

| Round | Status | Started | Closed | Method change | Decision link |
|---|---|---|---|---|---|
| 0 | baseline | YYYY-MM-DD | - | (frozen baseline) | - |
| 1 | implemented | YYYY-MM-DD | YYYY-MM-DD | <one-line change> | decisions/decision-improvement-round-1.md |
```

## improvement-frontier.md Template

```markdown
# Improvement Frontier

## Tried and kept
- <method change> (round N)

## Tried and reverted
- <method change> (round N, reverted because ...)

## Proposed but not yet attempted
- <proposal> (source: round N critique)

## Abandoned
- <method change> (decision: decisions/decision-improvement-round-N.md, reason: ...)
```

The main agent must read this file before spawning the Improvement-Critique Reviewer and pass its path inside the reviewer invocation template's Required Reads.

## round-N.md Template

```markdown
# Improvement Round N

## Round metadata
- Round number: N
- Opened at: YYYY-MM-DD
- Target question: Q<K> | all                     ← v4.2: required
- Cross-question impact expected: <list>          ← v4.2: required
- Target metric: <metric>
- Marginal threshold: <e.g. WAPE absolute reduction >= 0.01>
- Target claim level ceiling: <claim level the user wants this round to attempt>

## Baseline reference
- Snapshot file: claims/baseline-snapshot.md
- Frozen metrics referenced: <list>

## Critique findings
- Source review: reviews/improvement-round-N-critique.md
- Top proposals (one-line each)

## Skepticism findings
- Source review: reviews/improvement-round-N-skepticism.md
- Blocking risks
- Non-blocking warnings

## Synthesized proposal
- Selected change: <method change>
- Hypothesis: <expected before -> after metric>
- Required new data or solver: <yes/no, branches/...md>
- Touches confirmed method or model structure: <yes/no, fallback/rollback link>

## Risk assessment
- Worst-case metric impact: <value>
- Worst-case claim level impact: <claim level>

## Required readiness or rollback
- Readiness gate: gates/...md or `none`
- Rollback document: rollbacks/...md or `none`

## Claim level delta
- Before: <claim level>
- After (intended): <claim level>
- Gate justifying upgrade: <gate path or `none`>

## User decision link
- decisions/decision-improvement-round-N.md
- Status: PENDING / CONFIRMED / REJECTED

## Implementation summary
- <appended after user confirms and code lands>

## Before vs after metrics
| Metric | Baseline | This round | Delta |
|---|---|---|---|

## Frontier update
- Moved to "Tried and kept" / "Tried and reverted" / "Abandoned"
- Frontier file updated at: YYYY-MM-DD
```

## Section Order Rules

- The sections from `## Round metadata` through `## User decision link` must exist before the user is asked to confirm.
- The sections `## Implementation summary`, `## Before vs after metrics`, and `## Frontier update` are appended only after the user confirms and the implementation closes.
- The main agent must not write `## Synthesized proposal` until both Critique and Skepticism review files exist.

## Forbidden Behavior

- Do not compare against the previous round; comparison must reference `claims/baseline-snapshot.md`.
- Do not omit Skepticism findings when blocking risks exist.
- Do not record a claim level delta upward without a gate file in Required readiness.
- Do not close a round without updating `improvement-log.md` and `improvement-frontier.md`.

## Per-Question Frontier (v4.2)

Multi-question projects must NOT collapse Tried-and-kept / Tried-and-reverted / Proposed / Abandoned into one global file. Single-question projects keep the single-file form above. Multi-question projects use the index + per-question form.

### When to switch to per-question

Switch when:

- `claims/baseline-snapshot.md` is in index form (i.e. lists `claims/baseline-qK.md` per-question files), or
- any closed round in `improvement-log.md` declared `Target question` other than `all`.

### File layout

```text
improvements/improvement-frontier.md    ← index file
improvements/frontier-q1.md             ← Q1 four-quadrant frontier
improvements/frontier-q2.md             ← Q2 ...
improvements/frontier-q3.md             ← Q3 ...
```

### Index template (`improvements/improvement-frontier.md` in multi-question form)

```markdown
# Improvement Frontier Index

## Per-question frontiers
| Question | Per-question file | Active rounds |
|---|---|---|
| Q1 | improvements/frontier-q1.md | round-2 (closed), round-5 (closed) |
| Q2 | improvements/frontier-q2.md | round-3 (closed) |
| Q3 | improvements/frontier-q3.md | round-1 (closed), round-4 (in progress) |

## Cross-question proposals
- Proposals that target multiple questions simultaneously live here.
- Each entry must link to its `improvements/round-N.md` and the per-question entries it touches.
```

### Per-question template (`improvements/frontier-qK.md`)

```markdown
# Frontier — Q<K>

## Tried and kept
- <method change> (round N, gate ref)

## Tried and reverted
- <method change> (round N, reverted because ...)

## Proposed but not yet attempted
- <proposal> (source: round N critique)

## Abandoned
- <method change> (decision: decisions/decision-improvement-round-N.md, reason: ...)
```

### Per-question forbidden behavior

- Do not duplicate a frontier entry across `improvements/frontier-qK.md` and the index file. The index references but does not enumerate per-question entries.
- Do not move a proposal to "Tried and kept" in `improvements/frontier-qK.md` while round-N.md `Cross-question impact expected` still has unresolved entries on Q<j ≠ K>.
- Do not abandon a proposal silently — closing a round without writing the proposal to one of the four quadrants in the correct per-question file is forbidden.
