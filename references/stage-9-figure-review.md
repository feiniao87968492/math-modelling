# Stage 9 - Figure Review
## Stage Contract
This stage defines the safe work slice for figure review. It does not own global workflow state.
## Inputs
- figure files
- captions
- source CSV/meta files

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`
- `references/subagent-specialists.md`

## Outputs
- `reviews/stage9-figure-review.md`

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported
- use rollback documents instead of silently patching earlier-stage defects

## Expert Review
Fixed or primary reviewer: Figure-Review Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- caption claim exceeds evidence
- blocking figure defects remain unresolved
