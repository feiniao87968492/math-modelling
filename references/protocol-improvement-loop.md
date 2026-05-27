# Protocol - Improvement Loop

## Purpose

Define how `/math-modeling improve` runs an additional round of work on an already-validated solution without bypassing v4 protocols. The improvement loop is additive: it reuses readiness gate, rollback, fallback, claim grounding, and Final Evidence Gate. It does not introduce a parallel state machine.

## Core Rule

An improvement round is a controlled re-entry into Stage 5/6/7/10 work, anchored to a frozen baseline, mediated by two adversarial reviewers, and gated by a user-confirmed decision document. No metric, claim, or method change is accepted without all three.

## Preconditions

The main agent must verify all of the following before spawning Improvement-Critique:

1. `gates/stage6-*` exists and concludes PASS or PASS_WITH_WARNINGS.
2. `claims/baseline-snapshot.md` exists.
3. Stage 7 sensitivity analysis report exists.
4. No blocking decision document is pending in `decisions/`.
5. There is no in-progress `improvements/round-N.md` whose decision is still PENDING or whose implementation is unfinished.

If any precondition fails, the main agent must stop and write a one-paragraph blocker explanation. It must not silently proceed.

## Recommended Flow

1. Read `improvements/improvement-frontier.md` and `claims/baseline-snapshot.md`.
2. Emit a reviewer invocation template for Improvement-Critique Reviewer. Required Reads must include the frontier path.
3. After Critique writes `reviews/improvement-round-N-critique.md`, emit a reviewer invocation template for Improvement-Skepticism Reviewer. Required Reads must include the Critique file.
4. Synthesize findings into `improvements/round-N.md` from `## Round metadata` through `## User decision link`. Leave `## Implementation summary`, `## Before vs after metrics`, and `## Frontier update` empty until after the user confirms.
5. Open `decisions/decision-improvement-round-N.md` and mark it PENDING. Front-load Skepticism blocking risks inside the decision body.
6. Stop and wait for explicit user confirmation. User silence is not confirmation.
7. After confirmation, route the change:
   - if it touches a confirmed method, model structure, or evidence path, generate a rollback document under `rollbacks/` first per `protocol-rollback.md`,
   - otherwise re-enter Stage 5/6 work slices under existing stage contracts.
8. After implementation, write `## Implementation summary`, `## Before vs after metrics`, and `## Frontier update` in `round-N.md`, update `improvement-log.md`, and update `improvement-frontier.md`.
9. Re-run Stage 6 validation review per the Stage 6 contract; reuse the v4 reviewer invocation template.
10. Run `/math-modeling improve close` to finalize the round. Final Evidence Gate must be re-checked before any subsequent export.

## Claim Level Rules

- A round may keep, downgrade, or attempt to upgrade the claim level.
- Upgrading the claim level requires a corresponding readiness or evidence gate result. Updating `claim-registry.md` without that gate is forbidden.
- Downgrading the claim level requires `claim-registry.md` to be updated in the same round and `improvement-log.md` to mark the round as `reverted` or `rejected` if the downgrade was unintended.

## Convergence Conditions

The main agent must stop opening new rounds when any of the following holds:

- the user explicitly stops the loop,
- the marginal metric delta of the most recent closed round falls below the `marginal_threshold` declared in that round's metadata,
- the current claim level reaches the `target_claim_level` declared in round-1 metadata,
- two consecutive rounds receive Skepticism BLOCKING risks that Critique cannot rebut with new evidence,
- remaining frontier entries are all `Abandoned` or block on resources the user has declined to provide.

The main agent must not auto-open the next round. Each round requires a user-initiated `/math-modeling improve` invocation.

## Boundary With v4 Protocols

| Concern | Owner |
|---|---|
| Method/model/evidence path change | `protocol-rollback.md` (rollback document required) |
| Missing data, solver, or evidence | `protocol-readiness-gate.md` (readiness gate required) |
| Fallback that changes confirmed method | `protocol-fallback-and-deviation.md` |
| Final export | `references/evidence-gate.md` (Final Evidence Gate required) |
| User decision recording | `protocol-human-confirmation.md` |
| Memory check at round close | `protocol-memory-update.md` |

The improvement loop never substitutes for these protocols. It composes with them.

## Forbidden Behavior

- Do not start an improvement round without a frozen baseline snapshot.
- Do not synthesize a proposal before both Critique and Skepticism review files exist.
- Do not mark a round implemented without before vs after metrics in `round-N.md`.
- Do not auto-open a follow-up round without user invocation.
- Do not bypass rollback when a round changes confirmed method or model structure.
- Do not raise claim level without a gate result that justifies it.
- Do not compare against the previous round; always compare against the baseline snapshot.

## Process Audit Rules

These rules cover process-level defects observed in v4.1 实战 dry-run on 2026-05-27 and are enforced as hard rules:

### Finding ID consistency

- The F-IDs in `improvements/round-N.md` "Critique findings" must match the F-IDs and proposal text in `reviews/improvement-round-N-critique.md` exactly.
- The F-IDs in `improvements/improvement-frontier.md` "Proposed but not yet attempted" must match the same Critique source.
- The decision document `decisions/decision-improvement-round-N.md` must not reference an F-ID that the Critique did not declare.
- Renumbering, compressing, or relabeling Critique F-IDs in any downstream artifact is forbidden.

### Decision pre-load coverage

- `decisions/decision-improvement-round-N.md` "Pre-load Skepticism BLOCKING risks" must enumerate every Blocking risk from `reviews/improvement-round-N-critique.md` and every Blocking risk from `reviews/improvement-round-N-skepticism.md`.
- The decision Options section must include at least one option that addresses each Critique finding F1..FK; selectively covering only F1..F3 while the Critique declared F1..F7 is forbidden.
- A decision document with missing Pre-load Blocking risks or uncovered Critique findings must not reach `Status: PENDING`.

### Frontier status tag ordering

- `improvements/improvement-frontier.md` must not annotate a proposal with "blocked by Skepticism Bk" or any Skepticism-attributed Blocking phrase before `reviews/improvement-round-N-skepticism.md` exists on disk.
- The neutral placeholder "pending Skepticism review" is permitted while waiting; substantive Skepticism risk citations are not.
- Moving a proposal to "Tried and reverted" or "Abandoned" requires both Critique and Skepticism review files to be present.
