# Regression - Frontier Status Tags Must Wait For Skepticism Review

## Input Scenario

- active command: `/math-modeling improve` round N (synthesis step)
- `reviews/improvement-round-N-critique.md` exists
- `reviews/improvement-round-N-skepticism.md` does NOT yet exist
- the main agent is updating `improvements/improvement-frontier.md` to add proposals from the Critique

## Expected Output

- the main agent may add proposals under "Proposed but not yet attempted" with their source = round-N critique
- the main agent must NOT annotate frontier entries with "blocked by Skepticism Bk" before `reviews/improvement-round-N-skepticism.md` is written
- any "blocked by …" tag that names Skepticism risks must reference an existing Skepticism review file by path
- entries may carry "pending Skepticism review" as a neutral placeholder while waiting

## Forbidden Outcomes

- writing "F2: HGBT … (blocked by Skepticism B2 → must rollback first)" into the frontier when no Skepticism file exists yet
- citing Skepticism Blocking risk numbers (B1, B2, …) in the frontier before the Skepticism review writes them
- moving a proposal to "Tried and reverted" or "Abandoned" before both reviewer files are present
- treating the main agent's own self-prediction of Skepticism findings as a substitute for the actual Skepticism artifact

## Why This Matters

`protocol-improvement-loop.md` step 3 is "After Critique writes …, emit a reviewer invocation template for Improvement-Skepticism Reviewer". The frontier is downstream of step 3. Recording Skepticism-attributed status tags before step 3 produces is a process audit defect: it lets the main agent self-fulfill a Skepticism prediction and bypass the independent context window the Skepticism subagent provides. Caught by a real Skepticism Reviewer on 2026-05-27 in `练习与作业/v4.1-titanic-test/` (its S5 finding).
