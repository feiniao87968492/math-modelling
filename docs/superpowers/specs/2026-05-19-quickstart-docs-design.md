# Quickstart Docs Design

## Summary

This design covers the next documentation-focused slice for `math-modeling-v4`.

The purpose is to make the new skill directly usable by a human reader who opens the package for the first time. The work stays documentation-only except for minimal regression checks that protect critical onboarding content from being removed later.

## Goal

Turn `math-modeling-v4` into a package that is easy to try immediately by strengthening:

- `SKILL.md` as a dispatcher plus concise operator guide,
- `README.md` as a user-facing quickstart and onboarding document.

## Non-goals

- Do not add new runtime behavior.
- Do not add new protocols.
- Do not redesign dispatcher semantics.
- Do not modify the legacy `math-modeling` skill.
- Do not expand into a full external documentation site.

## Current Gap

The package already has:

- core dispatcher semantics,
- protocol documents,
- stage contracts,
- readiness/rollback/export regression coverage.

What it lacks is onboarding clarity:

- no end-to-end command path for a first-time user,
- no minimal project skeleton shown in one place,
- no concrete sample snippets for `workflow.md`, decision docs, and gates,
- no short explanation of what blocked states look like and how to continue.

## Recommended Approach

Use a two-document structure:

### `SKILL.md`

Keep it short and operational:

- command table,
- typical workflow,
- short examples,
- blocked-state behavior,
- hard boundaries.

### `README.md`

Make it the quickstart:

- who this skill is for,
- minimal folder skeleton,
- five-minute getting-started path,
- sample Markdown artifacts,
- common blockers and what to do next,
- regression command.

This keeps `SKILL.md` useful for direct invocation while making `README.md` the main human onboarding entry point.

## Alternative Options Considered

### Option A - Strengthen only `SKILL.md`

Pros:

- fewer files,
- all key information in one place.

Cons:

- dispatcher becomes too long,
- onboarding and execution rules get mixed together.

### Option B - Strengthen `SKILL.md` and `README.md` (recommended)

Pros:

- clean split between runtime instructions and user onboarding,
- easier to maintain,
- matches current package structure.

Cons:

- some coordination needed to avoid duplication.

### Option C - Add a separate `quickstart.md`

Pros:

- keeps root docs cleaner.

Cons:

- one more entry point,
- users may miss it,
- unnecessary for current scope.

## Content Design

### `SKILL.md` additions

Add these sections:

- `## 典型使用流程`
- `## 命令示例`
- `## 阻断时会看到什么`
- `## 明确不要做什么`

Content rules:

- examples stay short,
- focus on `init -> progress -> next -> stage -> confirm -> gate -> export`,
- show what the agent should do when pending decisions, readiness gates, or rollback requests appear,
- do not duplicate full README examples.

### `README.md` additions

Add these sections:

- `## 适用场景`
- `## 新项目骨架`
- `## 5 分钟上手`
- `## 最小文件示例`
- `## 常见阻断与处理`

Content rules:

- Chinese-first prose,
- keep commands and paths in English,
- include a minimal directory tree,
- include short sample snippets for `workflow.md`, a decision document, and a gate document,
- include common blocker examples such as missing data, missing solver, and blocked export.

## Minimal Directory Skeleton

The quickstart should show a structure similar to:

```text
project/
├── workflow.md
├── memory.md
├── decisions/
├── gates/
├── branches/
├── rollbacks/
├── claims/
│   └── claim-registry.md
└── reviews/
```

## Example Flow Requirements

The docs should describe this example path:

1. run `/math-modeling init`
2. inspect `workflow.md`
3. run `/math-modeling progress`
4. run `/math-modeling next`
5. run `/math-modeling stage 5` or another stage command
6. answer a blocking decision with `/math-modeling confirm`
7. run `/math-modeling gate`
8. run `/math-modeling export` only after final evidence gate passes

## Blocked-State Requirements

The docs should explicitly show at least these blocker categories:

- pending decision,
- readiness gate limitation,
- rollback required,
- export blocked.

Each example should state:

- why the workflow is blocked,
- which Markdown file should exist,
- what the user must do next.

## Testing Strategy

Use minimal documentation contract tests only.

Extend `regression/test_markdown_first_contracts.py` so that:

- `SKILL.md` must contain the typical workflow section and command examples,
- `README.md` must contain the project skeleton, five-minute quickstart, and minimal file examples.

Then run the existing full regression suite.

## Acceptance Criteria

This slice is complete when:

- `SKILL.md` contains practical operator-facing examples,
- `README.md` can onboard a new user from zero context,
- documentation remains Chinese-first with English commands and paths,
- new contract tests pass,
- full regression suite still passes.

## Risks

### Risk 1: too much duplication between `SKILL.md` and `README.md`

Mitigation: keep `SKILL.md` concise and operational, move richer examples into `README.md`.

### Risk 2: docs become verbose but not actionable

Mitigation: every new section must include commands, file names, or concrete next actions.

### Risk 3: onboarding content drifts over time

Mitigation: add small contract tests for the must-have sections and phrases.
