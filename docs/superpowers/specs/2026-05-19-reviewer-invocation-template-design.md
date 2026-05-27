# Reviewer Invocation Template Design

## Summary

This design adds an explicit reviewer invocation template layer to `math-modeling-v4`.

The package already defines mandatory fixed review gates and blocks continuation when required reviewer artifacts are missing.

What is still missing is a concrete dispatcher-level rule for what the main agent must do next.

This design closes that gap by requiring the main agent to emit a standard reviewer invocation template whenever a mandatory fixed review gate is reached and the required review artifact is missing.

## Problem Statement

The package currently says:

- fixed review points are mandatory review gates,
- missing fixed-review artifacts are blockers.

However, without a concrete invocation template:

- the main agent may still only describe the need for a review,
- or produce a vague blocker message,
- instead of actually shifting into a reviewer-invocation action.

This means the package now blocks correctly, but still leaves too much ambiguity about how reviewer spawning should happen.

## Goal

Define an explicit dispatcher-level reviewer invocation template so that, at a missing fixed-review gate, the main agent's next legal action is:

- emit a structured reviewer invocation block,
- point to the exact reviewer,
- point to the exact output file path,
- define the exact review scope,
- and stop downstream work until the review artifact exists.

## Non-goals

- Do not add a new runtime subagent API.
- Do not implement real process-level orchestration hooks.
- Do not add new YAML state tracking.
- Do not change the legacy `math-modeling` package.
- Do not force risk-triggered specialists into the same invocation template unless they later need it.

## Why This Slice Is Needed

The previous hard-gate change solved one problem:

- the main agent can no longer legally continue past missing fixed-review artifacts.

But there is still a second problem:

- the blocking response is not yet standardized into a concrete reviewer-invocation action.

Without a standard invocation template, different runs may still vary in how they ask for the review, making behavior less consistent and harder to verify.

## Recommended Approach

Add a standard invocation template at the dispatcher/protocol level.

When a required fixed-review artifact is missing, the main agent must output a structured invocation block with the following fields:

- `Reviewer`
- `Trigger`
- `Required Reads`
- `Expected Output Path`
- `Review Scope`
- `Blocking Question`

This keeps the package lightweight while making reviewer-spawn intent concrete and repeatable.

## Invocation Template

The required template shape should be:

```text
Spawn Reviewer: <Reviewer Name>
Trigger: <Why this reviewer is now mandatory>
Required Reads:
- <reference/path>
- <reference/path>
- <project/path>
Expected Output Path:
- <reviews/...md>
Review Scope:
- <scope item>
- <scope item>
Blocking Question:
- <the question that must be answered before continuation>
```

The wording can vary slightly, but the structure and fields should remain stable.

## Fixed Review Gate Mapping

### Stage 4

- Reviewer: `Algorithm/Model Reviewer`
- Expected output: `reviews/stage4-algorithm-model-review.md`
- Trigger: before algorithm/model freeze, required review artifact missing

### Stage 5

- Reviewer: `Implementation Readiness Reviewer`
- Expected output: `reviews/stage5-implementation-readiness-review.md`
- Trigger: before implementation code, required review artifact missing

### Stage 6

- Reviewer: `Validation Reviewer`
- Expected output: `reviews/stage6-validation-review.md`
- Trigger: after main result generation, required review artifact missing

### Stage 10 / Export

- Reviewer: `Evidence/Claim Reviewer`
- Expected output: `reviews/stage10-evidence-claim-review.md`
- Trigger: before claim/export, required review artifact missing

## Files To Update

### Dispatcher file

- `SKILL.md`

Add a new section describing the invocation template and when it must be used.

### Delegation protocol

- `references/protocol-subagent-delegation.md`

Add a section that defines:

- invocation template structure,
- required output file mapping,
- the rule that the main agent must invoke rather than merely describe the missing review.

### Stage contracts

At minimum, update:

- `references/stage-4-model-spec.md`
- `references/stage-5-solution-implementation.md`
- `references/stage-6-independent-validation.md`
- `references/stage-10-paper-materials.md`

Each should say that, if the fixed review artifact is missing, the next action is to emit the reviewer invocation template and stop downstream work.

## Required Wording

### `SKILL.md`

Must say:

- missing fixed-review artifacts do not only block continuation,
- they also require a reviewer invocation template as the next action,
- reading reviewer profile docs is not a substitute.

### `protocol-subagent-delegation.md`

Must define:

- `## Reviewer Invocation Template`
- required fields,
- stable file mapping,
- the rule that the invocation must target the corresponding `reviews/*.md` file.

### Stage contracts

Must include language like:

- if missing, emit the reviewer invocation template and stop downstream work.

## Testing Strategy

Use minimal documentation contract tests only.

Extend `regression/test_markdown_first_contracts.py` so it asserts:

- `SKILL.md` contains a reviewer invocation template section,
- `protocol-subagent-delegation.md` contains a reviewer invocation template section,
- the four stage docs mention invocation-template behavior,
- the four stable review file paths still appear in the relevant documents.

This slice does not need new runtime behavior tests because it standardizes dispatcher wording rather than adding a new helper API.

## Acceptance Criteria

This slice is complete when:

- the dispatcher defines a reviewer invocation template,
- the protocol defines the invocation contract,
- the affected stage docs instruct the main agent to emit the invocation template when the review artifact is missing,
- documentation contract tests pass,
- full regression still passes.

## Risks

### Risk 1: template wording becomes too verbose

Mitigation: keep the template field-based and short.

### Risk 2: template wording drifts across files

Mitigation: define the field names centrally in the protocol.

### Risk 3: users mistake the template for a real runtime API

Mitigation: describe it explicitly as dispatcher-level invocation guidance, not a process orchestration hook.
