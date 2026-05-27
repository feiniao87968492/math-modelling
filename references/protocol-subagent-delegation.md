# Protocol — Expert Review

## Purpose

Define how `math-modeling-v4` uses subagents as expert reviewers while the main agent remains responsible for workflow synthesis, user confirmations, artifact updates, and final continuation decisions.

## Core Rule

Subagents are expert reviewers, not stage owners. Expert Review findings inform the main agent; they do not clear blockers, confirm decisions, increase claim level, or independently continue downstream work.

## Main Agent Owns

- active command and relevant stage detection,
- required reference loading,
- Markdown audit document updates,
- user-facing blocking confirmations,
- synthesis of expert findings,
- final judgement on whether work may continue,
- memory checks,
- claim-level enforcement.

## Expert Reviewers Own

- independent scoped review,
- findings and evidence references,
- blocking risks and non-blocking warnings,
- recommended actions,
- recommendations for decision, gate, branch, rollback, or claim updates.

## Fixed Review Points

| Workflow point | Reviewer |
|---|---|
| Before algorithm/model freeze | Algorithm/Model Reviewer |
| Before implementation/code writing | Implementation Readiness Reviewer |
| After main result generation | Validation Reviewer |
| Before claim/export | Evidence/Claim Reviewer |

## Mandatory Review Gates

| Workflow point | Required reviewer | Required file |
|---|---|---|
| Before algorithm/model freeze | Algorithm/Model Reviewer | `reviews/stage4-algorithm-model-review.md` |
| Before implementation/code writing | Implementation Readiness Reviewer | `reviews/stage5-implementation-readiness-review.md` |
| After main result generation | Validation Reviewer | `reviews/stage6-validation-review.md` |
| Before claim/export | Evidence/Claim Reviewer | `reviews/stage10-evidence-claim-review.md` |

If a required fixed-review artifact is missing, the main agent must stop and spawn the required reviewer before proceeding.

## Reviewer Invocation Template

When a mandatory fixed-review artifact is missing, the main agent must emit a reviewer invocation template instead of only describing the blocker.

Required fields:

- `Reviewer`
- `Trigger`
- `Required Reads`
- `Expected Output Path`
- `Review Scope`
- `Blocking Question`

Template:

```text
Spawn Reviewer: <Reviewer Name>
Trigger: <Why this reviewer is now mandatory>
Required Reads:
- <reference/path>
- <reference/path>
- <project/path>
Expected Output Path:
- <reviews/...md>
Review Scope:
- <scope item>
- <scope item>
Blocking Question:
- <question that must be answered before continuation>
```

| Workflow point | Reviewer | Expected output path |
|---|---|---|
| Stage 4 pre-freeze | Algorithm/Model Reviewer | `reviews/stage4-algorithm-model-review.md` |
| Stage 5 pre-implementation | Implementation Readiness Reviewer | `reviews/stage5-implementation-readiness-review.md` |
| Stage 6 post-result | Validation Reviewer | `reviews/stage6-validation-review.md` |
| Stage 10 pre-claim/export | Evidence/Claim Reviewer | `reviews/stage10-evidence-claim-review.md` |

The main agent must invoke the corresponding reviewer template and target the mapped `reviews/*.md` path. It must not stop at a generic blocker message.

## Risk-Triggered Reviewers

| Risk | Reviewer |
|---|---|
| unclear or inconsistent data | Data-Audit Reviewer |
| solver or reproducibility risk | Code-Review Reviewer |
| figure or caption risk | Figure-Review Reviewer |
| unsupported claims | Evidence-Gate Reviewer |
| missing method background | Literature/Method Reviewer |
| improvement opportunity proposed on a validated solution | Improvement-Critique Reviewer |
| improvement proposal needs adversarial check | Improvement-Skepticism Reviewer |

## Review Document Required Sections

- `## Reviewed scope`
- `## Findings`
- `## Blocking risks`
- `## Non-blocking warnings`
- `## Required follow-up`
- `## Reviewer recommendation`
- `## Required reads referenced` (v4.2)
- `## Confidence` (v4.2)
- `## Forbidden-behavior self-check` (v4.2)

The full output schema and per-section contracts live in `schemas/reviewer-output-schema.md`. The forbidden-behavior items each reviewer must enumerate live in `schemas/reviewer-self-discipline-checklist.md`. A review missing v4.2 sections, malformed Findings, or any `[VIOLATED]` self-check item is NOT a fixed-review-point pass; the main agent must re-spawn the reviewer.

## Forbidden Reviewer Behavior

Expert reviewers must not:

- confirm user decisions,
- clear blockers,
- mark stages complete,
- increase claim level,
- continue downstream work on behalf of the main agent.

## Forbidden Bypass Behavior

The main agent must not:

- satisfy a fixed review gate by only reading reviewer profile documents,
- self-review past a mandatory fixed-review checkpoint,
- treat a missing fixed review as a warning instead of a blocker.
