# Regression - Improvement Round Finding ID Consistency

## Input Scenario

- active command: `/math-modeling improve` round N
- `reviews/improvement-round-N-critique.md` declares findings F1, F2, F3, F4, F5, F6, F7
- `improvements/round-N.md` "Critique findings" section attempts to summarize the proposals
- `improvements/improvement-frontier.md` "Proposed but not yet attempted" section attempts to enumerate the same proposals

## Expected Output

- the F-IDs in `improvements/round-N.md` "Critique findings" must match the F-IDs and proposal text in `reviews/improvement-round-N-critique.md` exactly
- the F-IDs in `improvements/improvement-frontier.md` must match the same Critique source
- if the Critique declares F4 = "HGBT replaces LR", then no project file may say "F2 = HGBT"
- the main agent must not reuse F2 / F3 labels for proposals that the Critique placed at F4 / F5

## Forbidden Outcomes

- summarizing the Critique with renumbered F-IDs (e.g. compressing F1–F7 into F1–F3 by renumbering)
- recording in `decisions/decision-improvement-round-N.md` an option labeled "select F2 (HGBT)" while the Critique's F2 is a different proposal
- letting the user confirm a decision option that points at a different proposal than the Critique's same-labeled finding
- any process where `frontier.md` and `round-N.md` use one numbering and `critique.md` uses another

## Why This Matters

Skepticism Reviewer attacks proposals by F-ID. If the F-IDs drift between Critique, round-N.md, frontier.md, and the decision document, Skepticism's Blocking risks become untraceable and a user reading the decision document cannot map "select F2" to the actual Critique proposal. This was caught by a real Skepticism Reviewer on 2026-05-27 in `练习与作业/v4.1-titanic-test/` and is why this fixture exists.
