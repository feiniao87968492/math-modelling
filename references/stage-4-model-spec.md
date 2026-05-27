# Stage 4 - Model Specification
## Stage Contract
This stage defines the safe work slice for model specification. It does not own global workflow state.
## Inputs
- problem facts
- selected methods
- innovation plan

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-readiness-gate.md`
- `references/subagent-model-building.md`

## Outputs
- `data/model-spec.md`
- `gates/stage4-model-readiness-gate.md`
- `reviews/stage4-algorithm-model-review.md`

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported
- use readiness or evidence gating before strong downstream claims
- before algorithm/model freeze, `reviews/stage4-algorithm-model-review.md` must exist; if missing, emit the reviewer invocation template for the required reviewer and stop downstream work

## Expert Review
Fixed or primary reviewer: Algorithm/Model Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work

## Time budget
If `time-budget.md` exists in the project root, run `/math-modeling time start 4` and observe advisory threshold per `references/protocol-time-budget.md`. Stage 4 is typically a high-cost stage; check remaining budget before freezing the model spec.

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- objective terms incomplete
- core constraints not grounded
