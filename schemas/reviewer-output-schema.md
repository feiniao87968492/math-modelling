# Reviewer Output Schema (v4.2)

## Purpose

Standardize the structure of every `reviews/*.md` written by an expert reviewer subagent in math-modeling-v4. Without a shared schema, reviewer outputs drift in section names, finding granularity, and confidence expression — making automated drift detection and reviewer-eval regression impossible.

## Applies To

All 9 reviewer profiles:

- Algorithm/Model Reviewer (Stage 4)
- Implementation Readiness Reviewer (Stage 5)
- Validation Reviewer (Stage 6)
- Evidence/Claim Reviewer (Stage 10)
- Improvement-Critique Reviewer (improvement loop, red team)
- Improvement-Skepticism Reviewer (improvement loop, blue team)
- Data-Audit Reviewer (risk-triggered)
- Code-Review Reviewer (risk-triggered)
- Figure-Review Reviewer (risk-triggered)
- Literature/Method Reviewer (risk-triggered)
- Evidence-Gate Reviewer (risk-triggered)

The 6 mm-*-reviewer subagents registered under `~/.claude/agents/` already follow the section structure; this schema makes the structure machine-checkable.

## Required Sections (in this order)

```markdown
# <Review Title>

## Reviewed scope
## Findings
## Blocking risks
## Non-blocking warnings
## Required follow-up
## Reviewer recommendation

## Required reads referenced
## Confidence
## Forbidden-behavior self-check
```

The 6 sections from `## Reviewed scope` through `## Reviewer recommendation` are the v4 / v4.1 contract and continue unchanged. The 3 sections after them are v4.2 additions.

## Section Contracts

### `## Reviewed scope`

A bullet list naming every artifact actually inspected. Acceptable formats:

- `- claims/baseline-snapshot.md`
- `- reviews/improvement-round-1-critique.md (B1, B2, B3 only)`

### `## Findings`

Each finding must be a numbered or labeled subsection (e.g., `### F1 — <title>` or `### S3 — <title>`). Every finding's body MUST include these labeled fields, on their own lines:

```markdown
- Type: <e.g., "method-route-mismatch", "data-gap", "claim-level-upgrade">
- Severity: BLOCKING | WARNING | INFO
- Evidence reference: <file path or file:line or section anchor>
- Recommended action: <one sentence>
```

Reviewer profile-specific extra fields (e.g., Critique reviewer's `Hypothesis:` / `Expected metric delta:`) MUST appear inside the finding body in addition to the four labeled fields above, not in place of them.

### `## Blocking risks`

Reuses the four labeled fields from Findings. Severity field must be `BLOCKING`. Risks here mirror the corresponding Findings entry (or aggregate multiple Findings) — they are not net-new risks unmentioned in Findings.

For Improvement-Skepticism specifically, every Blocking risk must additionally contain `Required mitigation:` per `references/subagent-improvement-skepticism.md`.

### `## Non-blocking warnings`

Same labeled-field format. Severity field must be `WARNING` or `INFO`.

### `## Required follow-up`

A bullet list of concrete next actions for the main agent. Each bullet must reference an artifact path or `decisions/`, `gates/`, `branches/`, or `rollbacks/` — naked recommendations without an artifact target are not allowed.

### `## Reviewer recommendation`

One paragraph plus an explicit verdict line at the end:

```markdown
## Reviewer recommendation
<paragraph>

Verdict: PASS | PASS_WITH_WARNINGS | BLOCKED
```

The verdict word must be one of those three exactly. Reviewer profiles requiring a different verdict word (e.g., Validation Reviewer's "PASS / PASS_WITH_WARNINGS / BLOCKED" trio is identical; Evidence/Claim Reviewer's "Final Evidence Gate verdict suggestion" goes here too) reuse this slot.

### `## Required reads referenced` (v4.2)

A bullet list of every reference file the reviewer actually opened. Format:

```markdown
- references/protocol-readiness-gate.md
- references/baseline-snapshot-template.md
- claims/baseline-snapshot.md
```

Reviewers MUST NOT list a reference they did not open. Reviewers MUST NOT omit a reference whose `Mandatory reads before reviewing` section in their profile listed it.

### `## Confidence` (v4.2)

Must contain exactly one of `high`, `medium`, `low` followed by a one-sentence rationale:

```markdown
## Confidence
medium — sensitivity-report covered F1/F2/F3 directly but F4 and F7 lacked qualitative grounding rows.
```

Confidence is the reviewer's own self-assessment of the review's reliability, not the underlying artifact's claim level. A `high` confidence review may still produce a `BLOCKED` verdict; conversely, a `low` confidence review with no Blocking risks does not free the main agent from re-spawning the reviewer if the dispatcher deems confidence inadequate.

### `## Forbidden-behavior self-check` (v4.2)

A checklist of items from `schemas/reviewer-self-discipline-checklist.md`. Every item must be either `[OK]` (asserted not violated) or `[N/A]` (not applicable to this reviewer's profile). `[VIOLATED]` immediately invalidates the review and forces the main agent to re-spawn.

```markdown
## Forbidden-behavior self-check
- [OK] Did not confirm user decisions
- [OK] Did not clear blockers
- [OK] Did not increase claim level
- [OK] Did not invoke another subagent
- [OK] Did not write or edit project files outside the review output
- [N/A] Did not run without upstream Critique (only applies to Skepticism reviewer)
```

## Acceptance Algorithm

The dispatcher accepts a `reviews/*.md` artifact as a fixed-review-point pass only when ALL hold:

1. All 9 required sections are present (case-sensitive headings).
2. Every Finding subsection contains all four labeled fields.
3. Verdict line ends with `PASS`, `PASS_WITH_WARNINGS`, or `BLOCKED`.
4. Confidence value is one of `high` / `medium` / `low`.
5. `Required reads referenced` lists at least one file (empty list = reviewer didn't read its own profile, hard fail).
6. `Forbidden-behavior self-check` contains zero `[VIOLATED]` items.

If any check fails, the dispatcher MUST NOT treat the review as a fixed-review-point pass; it must re-spawn the reviewer with the missing/malformed sections in the invocation template's `Blocking Question`.

## Drift Detection

`regression/reviewer-eval/` provides ground-truth fixtures: each fixture is a buggy artifact paired with the set of flags a profile-conformant reviewer would be expected to surface. Reviewer outputs that miss expected flags are recorded as drift incidents. This is not a CI gate (reviewers may legitimately surface different findings), but it is part of v4.2's reviewer-quality monitoring loop.

## Forbidden Behavior

- Do not rename required sections (e.g., `## Findings list` instead of `## Findings`).
- Do not omit `## Required reads referenced`, `## Confidence`, or `## Forbidden-behavior self-check`.
- Do not collapse multiple findings into a single un-labeled paragraph.
- Do not fabricate `Evidence reference` paths.
- Do not mark forbidden-behavior items `[OK]` without genuine self-check (drift detection will catch repeat offenders).
