# Protocol — Time Budget

## Purpose

Make competition hard deadlines a first-class workflow concern. Before v4.2, each stage's time consumption was an implicit user concern; with this protocol, the dispatcher reads remaining budget at every meaningful checkpoint and surfaces time-pressure advisories before the user runs out of clock.

## Core Rule

If the project root contains `time-budget.md`, the dispatcher must read remaining budget at:

- every `/math-modeling stage N` invocation (stage switch),
- every `/math-modeling improve` invocation (round open),
- every `/math-modeling export` invocation (final).

When remaining budget falls below the configured threshold (default 20% of total budget), the dispatcher must emit a time-pressure advisory and require user confirmation. User silence does not equal confirmation. If `time-budget.md` is absent, the dispatcher behaves identically to v4.1; nothing changes for projects that opt out.

## Required `time-budget.md` Sections

```markdown
# Time Budget

## Hard deadline
2026-XX-XX HH:MM (timezone)

## Total budget
72 hours (or whatever the contest allows)

## Advisory threshold
20%   <!-- optional; default 20% if omitted -->

## Stage allocation
| Stage | Planned (h) | Spent (h) | Remaining (h) | Status |
|---|---|---|---|---|
| 1 Problem Understanding | 4 | - | - | not_started |
| 2 Algorithm Selection   | 6 | - | - | not_started |
| 3 Innovation Design     | 4 | - | - | not_started |
| 4 Model Specification   | 8 | - | - | not_started |
| 5 Solution Implementation | 16 | - | - | not_started |
| 6 Independent Validation | 8 | - | - | not_started |
| 7 Sensitivity Analysis  | 6 | - | - | not_started |
| 8 Visualization         | 6 | - | - | not_started |
| 9 Figure Review         | 4 | - | - | not_started |
| 10 Paper Materials      | 10 | - | - | not_started |

## Burn-down log
| Timestamp | Stage | Event | Δh |
|---|---|---|---|
```

## Stage Status Values

- `not_started` — planning only, no clock running
- `in_progress` — `/math-modeling time start N` was invoked
- `paused` — explicit pause
- `done` — `/math-modeling time stop N` was invoked

## Burn-down Log Update Rules

Every stage transition must append to the `## Burn-down log` table:

- `start` event when `/math-modeling time start N` is invoked
- `stop` event when `/math-modeling time stop N` is invoked
- `pause` / `resume` events for explicit pauses
- `advisory` events when the dispatcher emits a time-pressure advisory

The dispatcher must refuse to advance past `/math-modeling stage M` (M > N) if the previous stage's row in `## Stage allocation` is still `in_progress` and the burn-down log has not recorded a `stop` for stage N.

## Time-Pressure Advisory

When remaining budget < threshold (default 20%), the advisory must:

- name remaining hours and percentage,
- list the 3 most expensive remaining stages by planned budget,
- offer the user three actions:
  - lower target claim level for remaining stages,
  - skip optional stages (typically Stage 7 sensitivity, Stage 9 figure review polish),
  - trigger model simplification reviewer.

The advisory is recorded as a row in the burn-down log with event = `advisory`. It must be confirmed before the original command (stage switch / improve / export) proceeds.

## Once-Per-Stage Rule

The advisory must not retrigger inside the same stage if the user already confirmed it once. Implementation: the dispatcher checks the burn-down log for an `advisory` event whose stage matches the current command's stage; if present and confirmed, the advisory is skipped this round.

## Hard Deadline Enforcement

If now > `## Hard deadline`, the dispatcher must block any `/math-modeling export` regardless of advisory state. The override path is for the user to update the deadline (with explicit acknowledgment that they are extending past the original commitment) or accept the export as overdue.

## `/math-modeling time` Subcommands

```
/math-modeling time              输出当前 burn-down 摘要 + 剩余预算 + 风险等级
/math-modeling time start N      标记 stage N 开始（写入 burn-down log）
/math-modeling time stop N       标记 stage N 结束（计算 Δh，写入 burn-down log）
/math-modeling time pause N      暂停 stage N
/math-modeling time resume N     恢复 stage N
```

## Boundary With Other v4 Protocols

| Concern | Owner |
|---|---|
| When to switch stage | this protocol + `references/stage-N-*.md` Done When |
| Whether stage work is sufficient | stage contract Done When + reviewer |
| Whether claim level should be lowered | `protocol-readiness-gate.md` |
| When to invoke model simplification | new advisory action; reuses readiness gate path |

## Forbidden Behavior

- Do not advance past a stage whose `## Stage allocation` row says `in_progress` without first running `/math-modeling time stop N`.
- Do not silently retry the original command after the user dismisses the advisory; the dispatcher must record the dismissal and stop.
- Do not auto-extend the hard deadline. Extension is an explicit user action with acknowledgment.
- Do not treat advisory threshold as a soft suggestion; it is a hard checkpoint.
- Do not enable this protocol implicitly. The dispatcher inspects `time-budget.md` existence; absent file = v4.1 behavior unchanged.

## Why This Matters

Per the v4.2 plan's "competition realism" framing, time is the largest implicit hazard in v4 / v4.1. With this protocol the dispatcher gives the user one clean signal before the budget runs out, and the burn-down log gives a post-mortem audit trail of where time actually went. Nothing in this protocol changes claim-level enforcement, reviewer obligations, or fixed-review points; it adds an orthogonal time-aware checkpoint layer.
