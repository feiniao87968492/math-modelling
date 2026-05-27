# Stage 10 - Paper Materials
## Stage Contract
This stage defines the safe work slice for paper materials. It does not own global workflow state.
## Inputs
- claim registry
- review outputs
- figure review
- validation and sensitivity evidence

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-readiness-gate.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`
- `references/evidence-gate.md`

## Outputs
- `claims/claim-registry.md`
- `gates/final-evidence-gate.md`
- `reviews/stage10-evidence-claim-review.md`
- `data/paper/figure-index.md`
- `data/paper/table-index.md`
- `data/paper/model-summary.md`
- `data/paper/innovation-summary.md`

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported
- use readiness or evidence gating before strong downstream claims
- use rollback documents instead of silently patching earlier-stage defects
- before claim or export, `reviews/stage10-evidence-claim-review.md` must exist; if missing, emit the reviewer invocation template for the required reviewer and stop downstream work

## Expert Review
Fixed or primary reviewer: Evidence/Claim Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- export attempted before final evidence gate
- paper-facing claims exceed supported claim level
