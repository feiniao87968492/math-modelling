# Stage 1 - Problem Understanding
## Stage Contract
This stage defines the safe work slice for problem understanding. It does not own global workflow state.
## Inputs
- problem statement
- raw materials
- project memory

## Required Reads
- `references/protocol-markdown-audit.md`
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-subagent-delegation.md`
- `references/subagent-model-building.md`
- `references/anti-hallucination.md`

## Outputs
- `data/problem-analysis.md`
- `data/facts/problem-facts.md`
- `data/facts/assumptions.md`

## Blocking Rules
- stop when a blocking decision document is pending
- do not produce artifacts that imply a stronger claim than supported

## Expert Review
Fixed or primary reviewer: Algorithm/Model Reviewer.

## Done When
- required artifacts for the stage exist
- blocking issues are either resolved or explicitly documented
- supported claim level is clear for downstream work

## Memory Check
Before finishing this stage work slice, update `memory.md` if a reusable rule, pitfall, counterexample, or user preference was found. Otherwise record `Memory check: no new memory`.

## Revision or Rollback Triggers
- ambiguity in problem interpretation
- missing key input definitions
