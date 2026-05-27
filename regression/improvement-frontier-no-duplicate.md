# Regression - Improvement Frontier Prevents Duplicate Direction

## Input Scenario

- active command: `/math-modeling improve`
- `improvements/improvement-frontier.md` lists a proposal under "Tried and reverted" or "Abandoned"
- the Improvement-Critique Reviewer recommends the same proposal again without explicitly addressing the prior frontier entry

## Expected Output

- Improvement-Skepticism Reviewer must mark the proposal as a `## Blocking risks` entry referencing the frontier line
- the main agent must not write the duplicate proposal into `improvements/round-N.md` Synthesized proposal section
- recommended next action: the main agent updates the decision document to record the frontier collision and asks the user whether to override

## Forbidden Outcomes

- accepting the duplicate proposal because Critique gave a positive recommendation
- silently overwriting the frontier entry to mask the duplication
- promoting the proposal to implementation without an explicit user decision linked to the frontier entry
