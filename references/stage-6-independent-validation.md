# Stage 6 - Independent Validation
## Stage Contract
This stage defines the safe work slice for independent validation. It does not own global workflow state.
## Inputs
- stage 5 results
- model specification
- claim ceiling

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-readiness-gate.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`

## Outputs
- `data/validation/validation-report.md`
- `reviews/stage6-validation-review.md`
- `claims/baseline-snapshot.md` (first PASS only, per `references/baseline-snapshot-template.md`)

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported
- use rollback documents instead of silently patching earlier-stage defects
- after main result generation, `reviews/stage6-validation-review.md` must exist before downstream interpretation continues; if missing, emit the reviewer invocation template for the required reviewer and stop downstream work

## Expert Review
Fixed or primary reviewer: Validation Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work
- on the first PASS or PASS_WITH_WARNINGS, `claims/baseline-snapshot.md` exists per `references/baseline-snapshot-template.md`

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- validation cannot support claimed strength
- independent reproduction contradicts main result
