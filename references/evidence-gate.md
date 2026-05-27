# Final Evidence Gate

## Purpose

Before `/math-modeling export`, verify that paper-facing claims, figures, tables, and summaries are supported by auditable Markdown documents and evidence files.

## Core Rule

Do not export paper materials unless `gates/final-evidence-gate.md` explicitly concludes `PASS` or `PASS_WITH_WARNINGS` and no blocking decision remains pending.

## Required Inputs

- `workflow.md`
- `claims/claim-registry.md`
- `gates/*.md`
- `decisions/*.md`
- `reviews/*.md`
- `figures/figure-index.md`

## Gate Checks

- no active blockers
- claims grounded
- claim level respected
- figures reviewed
- assumptions and constraints recorded
- paper grounding scan PASS (v4.2; see `references/protocol-paper-grounding-scan.md`)

## Final Evidence Gate Report Template

Write to `gates/final-evidence-gate.md` with:

- `## Gate result`
- `## Checks`
- `## Blocking issues`
- `## Warnings`
- `## Export decision`

## Result Values

- `PASS`
- `PASS_WITH_WARNINGS`
- `BLOCKED`
