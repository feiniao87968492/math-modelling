# Stage 3 - Innovation Design
## Stage Contract
This stage defines the safe work slice for innovation design. It does not own global workflow state.
## Inputs
- selected algorithms
- baseline plan
- contest goals

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/subagent-model-building.md`

## Outputs
- `data/innovation/innovation-design.md`
- `reviews/stage3-innovation-review.md`

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported

## Expert Review
Fixed or primary reviewer: Algorithm/Model Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work

## Time budget
If `time-budget.md` exists in the project root, run `/math-modeling time start 3` and observe advisory threshold per `references/protocol-time-budget.md`.

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- innovation is wording-only
- no evidence generation path exists
