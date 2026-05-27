# Stage 7 - Sensitivity Analysis
## Stage Contract
This stage defines the safe work slice for sensitivity analysis. It does not own global workflow state.
## Inputs
- validated results
- parameter ranges
- claim registry

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-readiness-gate.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`

## Outputs
- `data/sensitivity/sensitivity-report.md`
- `data/sensitivity/sensitivity-table.csv`
- `data/sensitivity/sensitivity-meta.json`

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported
- use rollback documents instead of silently patching earlier-stage defects

## Expert Review
Fixed or primary reviewer: Validation Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work

## Time budget
If `time-budget.md` exists in the project root, run `/math-modeling time start 7` and observe advisory threshold per `references/protocol-time-budget.md`. Stage 7 is one of the candidates for partial skip when remaining budget is low (with explicit user confirmation and claim level downgrade).

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- sensitivity undermines stability claims
- perturbation method mismatches claim type
