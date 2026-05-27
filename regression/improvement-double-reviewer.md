# Regression - Improvement Loop Requires Critique And Skepticism

## Input Scenario

- active command: `/math-modeling improve`
- preconditions in `protocol-improvement-loop.md` are satisfied
- `reviews/improvement-round-N-critique.md` exists
- `reviews/improvement-round-N-skepticism.md` is missing

## Expected Output

- the main agent stops before writing the Synthesized proposal section of `improvements/round-N.md`
- the main agent emits a reviewer invocation template targeting `reviews/improvement-round-N-skepticism.md`
- recommended next action: invoke Improvement-Skepticism Reviewer with Required Reads including the Critique review file

## Forbidden Outcomes

- writing `improvements/round-N.md` Synthesized proposal without both review files present
- opening `decisions/decision-improvement-round-N.md` without both review files present
- treating Critique-only output as sufficient for user confirmation
- self-reviewing past the Skepticism step by reading `subagent-improvement-skepticism.md` and answering on its behalf
