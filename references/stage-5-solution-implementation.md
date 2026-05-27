# Stage 5 - Solution Implementation
## Stage Contract
This stage defines the safe work slice for solution implementation. It does not own global workflow state.
## Inputs
- confirmed model specification
- confirmed algorithm route
- audited data inputs
- project memory

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-readiness-gate.md`
- `references/protocol-rollback.md`
- `references/subagent-model-building.md`
- `references/subagent-specialists.md`
- `references/protocol-fallback-and-deviation.md`

## Outputs
- `code/python/`
- `gates/stage5-readiness-gate.md`
- `reviews/stage5-implementation-readiness-review.md`
- `claims/claim-registry.md`

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported
- use readiness or evidence gating before strong downstream claims
- before implementation code, `reviews/stage5-implementation-readiness-review.md` must exist; if missing, emit the reviewer invocation template for the required reviewer and stop downstream work

## Expert Review
Fixed or primary reviewer: Implementation Readiness Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work

## Time budget
If `time-budget.md` exists in the project root, run `/math-modeling time start 5` and observe advisory threshold per `references/protocol-time-budget.md`. Stage 5 is the largest planned-budget stage; consider model simplification reviewer when remaining budget < threshold.

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- solver path invalidates confirmed implementation route
- result generation reveals structural model defects
- claim support is weaker than assumed
