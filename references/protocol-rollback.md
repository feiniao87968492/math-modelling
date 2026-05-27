# Protocol — Rollback

## Purpose

Define how later stages request controlled rollback when validation, sensitivity analysis, visualization, figure review, or claim grounding exposes defects in earlier modeling work.

## Core Rule

Stages 6-10 must not silently patch defects that belong to stages 1-5.

## Severity Levels

| Severity | Meaning |
|---|---|
| Minor revision | wording or formatting issue |
| Method revision | implementation or solver defect |
| Structural revision | problem interpretation, model, or method route invalid |

## Rollback Document Required Sections

- `## Trigger`
- `## Severity`
- `## Why downstream patching is not allowed`
- `## Evidence`
- `## Affected outputs`
- `## Recommended action`
- `## Requires user confirmation`
- `## Decision link`

## Confirmation Rules

- Method revision requires a blocking decision unless the user already approved the exact fallback path.
- Structural revision always requires a blocking decision.
- User silence never approves rollback.
