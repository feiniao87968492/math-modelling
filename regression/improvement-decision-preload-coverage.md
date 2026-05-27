# Regression - Decision Preload Must Cover All Critique Blocking Risks

## Input Scenario

- active command: `/math-modeling improve` round N (synthesis step)
- `reviews/improvement-round-N-critique.md` exists and declares Blocking risks B1, B2, B3, B4
- `reviews/improvement-round-N-skepticism.md` exists and may add additional Blocking risks
- the main agent is about to write `decisions/decision-improvement-round-N.md`

## Expected Output

- `decisions/decision-improvement-round-N.md` "Pre-load Skepticism BLOCKING risks" section enumerates every Blocking risk from the Critique review (B1–B4 in this scenario), not a subset
- `decisions/decision-improvement-round-N.md` "Options" section contains at least one option that addresses each Critique finding (F1–FK), not only the first three findings
- if a Blocking risk is omitted from Pre-load, the synthesis step is rejected and the main agent must regenerate the decision document

## Forbidden Outcomes

- listing only B1, B2, B3 in Pre-load while the Critique declared B4 — silently drops a Blocking risk
- providing decision options A–E that only cover findings F1, F2, F3 while the Critique declared F4–F7 — leaves the user unable to confirm proposals that exist in the Critique
- letting the decision reach `Status: PENDING` while a Critique Blocking risk is missing from Pre-load
- relying on the user to re-read the Critique to discover unlisted Blocking risks

## Why This Matters

The decision document is the user's single page of truth at confirm time. If Pre-load drops Blocking risks, the user sees a softer choice than the Critique actually demanded; if Options drop findings, the user cannot select proposals that the Critique recommended. Both failure modes were caught by a real Skepticism Reviewer on 2026-05-27 in `练习与作业/v4.1-titanic-test/`.
