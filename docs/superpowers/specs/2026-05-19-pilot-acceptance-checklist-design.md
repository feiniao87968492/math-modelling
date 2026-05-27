# Pilot Acceptance Checklist Design

## Summary

This design adds a single self-trial checklist document for `math-modeling-v4`.

The document is meant for internal pilot use, not for external release certification.

Its job is to help a user run one real small modeling project through the v4 workflow and record:

- whether the workflow stays usable,
- whether blockers and gates behave correctly,
- whether claims stay grounded,
- whether rollback and export controls trigger at the right time,
- whether the package is ready for broader trial use.

## Goal

Add one root-level checklist document that a user can open and use directly while trialing `math-modeling-v4` on a real project.

The checklist should be:

- short enough to use during a live pilot,
- concrete enough to catch workflow failures,
- structured enough to support a go / revise / stop decision after the trial.

## Non-goals

- Do not add new runtime behavior.
- Do not redesign `README.md`, `DELIVERY.md`, or `SKILL.md`.
- Do not add a full regression dashboard.
- Do not create a general-purpose QA framework for all future skills.
- Do not require command automation for the checklist itself.

## Why This Slice

The package already has:

- onboarding instructions in `README.md`,
- package handoff guidance in `DELIVERY.md`,
- regression coverage for contract, smoke, scenario, and command-flow behavior.

What is still missing is a document for real pilot execution:

- one concrete checklist,
- one consistent way to record what happened,
- one structured way to decide whether v4 is ready for wider use.

Without this, pilot validation remains ad hoc and hard to compare across runs.

## Recommended Approach

Create one standalone root-level document:

- `PILOT_ACCEPTANCE_CHECKLIST.md`

Keep it operational and checklist-driven.

Use Markdown checkboxes and short recording slots so the user can fill it in while running a real project.

Do not place this content inside `DELIVERY.md`, because:

- `DELIVERY.md` is for current capability and handoff,
- the pilot checklist is for live evaluation and trial notes.

## Options Considered

### Option A - Standalone pilot checklist document (recommended)

Pros:

- easiest to use during a live trial,
- clean separation from delivery and onboarding docs,
- low maintenance overhead.

Cons:

- adds one more root-level file.

### Option B - Put the checklist into `DELIVERY.md`

Pros:

- fewer documents.

Cons:

- mixes handoff summary with operational evaluation,
- makes `DELIVERY.md` less scan-friendly.

### Option C - Split into template plus notes file

Pros:

- stronger separation between template and filled results.

Cons:

- too heavy for the current stage,
- slower for first trial use.

## Document Structure

Recommended sections:

- `## 试用目标`
- `## 试用前检查`
- `## 试用中观察`
- `## 关键异常记录`
- `## 试用后判定`
- `## 下一步动作`

## Content Requirements

### `试用目标`

Should capture:

- pilot project name,
- pilot date,
- operator,
- project type,
- expected trial scope,
- whether the goal is only workflow validation or also result-quality observation.

### `试用前检查`

Should include checkbox items for:

- full regression already green,
- pilot project is small and low-risk,
- user agrees to treat v4 as pilot rather than production runtime,
- required project files exist or are intentionally initialized from scratch,
- success criteria are written before starting.

### `试用中观察`

Should include checkbox items and note slots for:

- `workflow.md` becomes the clear working anchor,
- missing information creates explicit `decision` or `branch` docs,
- claim ceiling stays aligned with available evidence,
- gate blocking is explicit rather than silent,
- rollback is requested for late structural defects,
- export is blocked until final evidence is grounded,
- reviewer involvement remains understandable rather than reverting to stage-owner state-machine behavior.

### `关键异常记录`

Should include a lightweight table or bullet template capturing:

- trigger,
- expected behavior,
- actual behavior,
- severity,
- follow-up action.

### `试用后判定`

Should include a forced final choice:

- `可继续试用`
- `修正后再试`
- `暂不建议推广`

And should require a short reason.

### `下一步动作`

Should prompt the user to record:

- what to fix,
- what to monitor in the next pilot,
- whether to test against the legacy `math-modeling` package for comparison.

## Writing Style

The checklist should:

- use Chinese as the main language,
- keep command names and file paths in English where appropriate,
- be concise and operational,
- avoid marketing language,
- read like a trial worksheet rather than a product brochure.

## Discoverability

This slice may optionally add a short pointer from `DELIVERY.md` or `README.md`, but discoverability is secondary.

The primary deliverable is the standalone checklist itself.

If a pointer is added, it should be one short bullet only.

## Testing Strategy

Use a minimal documentation contract check only.

Extend `regression/test_markdown_first_contracts.py` to assert:

- `PILOT_ACCEPTANCE_CHECKLIST.md` exists,
- it contains the required section headings,
- it includes at least one reference to `workflow.md`,
- it includes at least one explicit final decision option.

Then run the full existing regression suite.

## Acceptance Criteria

This slice is complete when:

- `PILOT_ACCEPTANCE_CHECKLIST.md` exists at the package root,
- the checklist can be used directly during a pilot without extra interpretation,
- the document covers preparation, live observation, anomaly capture, and final decision,
- minimal doc contract tests pass,
- full regression still passes.

## Risks

### Risk 1: the checklist becomes too long to use live

Mitigation: keep it focused on decisions and observation points, not theory.

### Risk 2: the checklist duplicates delivery documentation

Mitigation: keep `DELIVERY.md` focused on handoff and keep the new file focused on trial execution.

### Risk 3: the checklist becomes too vague to be useful

Mitigation: require concrete checkboxes, explicit outcomes, and anomaly recording slots.
