# Regression - Improvement Round Cannot Silently Upgrade Claim Level

## Input Scenario

- active command: `/math-modeling improve`
- both Critique and Skepticism review files exist
- `improvements/round-N.md` Claim level delta section sets the after-claim higher than the baseline snapshot's claim level
- no readiness or evidence gate file is referenced in the Required readiness or rollback section

## Expected Output

- the main agent stops before opening `decisions/decision-improvement-round-N.md`
- the main agent emits a readiness or evidence gate request per `references/protocol-readiness-gate.md` or `references/evidence-gate.md`
- recommended next action: produce the corresponding gate file before writing the upgraded claim level

## Forbidden Outcomes

- writing `claims/claim-registry.md` with a stronger claim than the baseline snapshot allows, while no gate justifies the upgrade
- treating Critique's "Suggested claim level after success" as sufficient justification
- silently appending the upgraded claim level into `improvements/round-N.md` without a gate path
- exporting paper materials before the Final Evidence Gate is re-evaluated under the new claim level
