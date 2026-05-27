# Mandatory Subagent Review Gates Design

## Summary

This design upgrades the fixed expert review points in `math-modeling-v4` from soft policy language into hard execution gates.

Today, the package says expert reviewers should be used at fixed workflow points, but the main agent can still read the reviewer documents as guidance and continue alone without actually spawning a reviewer subagent.

This design closes that gap by making the fixed review points mandatory.

## Problem Statement

The current behavior gap is:

- `SKILL.md` and `protocol-subagent-delegation.md` describe fixed reviewer checkpoints,
- but no hard rule says missing reviewer output must block progress,
- so the main agent can continue by doing the reasoning itself,
- which defeats the intended expert-review architecture.

As a result, reviewer profiles are treated as optional methodology references rather than executable review gates.

## Goal

Make the four fixed review points mandatory hard gates:

- before algorithm/model freeze,
- before implementation/code writing,
- after main result generation,
- before claim/export.

At each fixed point:

- a corresponding review file must exist,
- that file must be treated as subagent-produced expert review output,
- if the file is missing, the main agent must stop and spawn the required reviewer first,
- the main agent must not silently self-review and continue.

## Non-goals

- Do not make all risk-triggered specialist reviewers mandatory.
- Do not reintroduce a YAML workflow state machine.
- Do not turn expert reviewers into stage owners.
- Do not modify the legacy `math-modeling` package.
- Do not require a full runtime orchestration engine beyond current v4 document-and-contract style.

## Why This Change Is Needed

The current v4 design intentionally gives the main agent high autonomy.

That autonomy is valuable, but without mandatory review gates it creates a predictable failure mode:

- the main agent chooses the most efficient path,
- reads reviewer protocol docs,
- performs the reasoning itself,
- and never actually triggers reviewer subagents.

This means the package looks like it supports multi-expert review, but the real execution path remains single-agent.

## Recommended Approach

Implement mandatory review gates at three levels:

1. **Protocol layer**
   - define the fixed review points as hard gates,
   - define required review file paths,
   - define missing-review behavior as blocking.

2. **Stage contract layer**
   - add explicit blocking rules to the affected stages,
   - require the review file before downstream work can continue.

3. **Dispatcher / package rules**
   - forbid treating reviewer profiles as informational-only substitutes,
   - require actual reviewer invocation before continuation.

Then add regression coverage so the behavior cannot silently regress.

## Fixed Mandatory Review Gates

The fixed review points should map to concrete files:

| Workflow point | Required reviewer | Required file |
|---|---|---|
| Before algorithm/model freeze | Algorithm/Model Reviewer | `reviews/stage4-algorithm-model-review.md` |
| Before implementation/code writing | Implementation Readiness Reviewer | `reviews/stage5-implementation-readiness-review.md` |
| After main result generation | Validation Reviewer | `reviews/stage6-validation-review.md` |
| Before claim/export | Evidence/Claim Reviewer | `reviews/stage10-evidence-claim-review.md` |

These file names should be explicit and stable so contracts and regression tests can target them directly.

## Execution Rule

At a fixed review point:

- if the required review file exists, the main agent may read it and continue under the normal rules,
- if the required review file does not exist, the main agent must stop and spawn the required reviewer subagent,
- the main agent must not replace this by performing the review itself without reviewer output.

## Forbidden Bypass Behavior

The following must be explicitly forbidden:

- reading `subagent-*.md` as if that alone satisfies the review requirement,
- continuing because the main agent believes it already knows the answer,
- writing implementation code before the required implementation-readiness review exists,
- exporting because the main agent believes the evidence is sufficient without the required evidence/claim review,
- treating a missing fixed review as a warning instead of a blocker.

## Files To Update

### Core dispatcher files

- `SKILL.md`
- `CLAUDE.md`

### Protocol files

- `references/protocol-subagent-delegation.md`

### Stage contracts

At minimum, update:

- `references/stage-4-model-spec.md`
- `references/stage-5-solution-implementation.md`
- `references/stage-6-independent-validation.md`
- `references/stage-10-paper-materials.md`

If needed, stage 4 may include the pre-freeze requirement while stage 5 references the implementation-readiness gate as the hard precondition for code work.

### Regression files

- `regression/test_markdown_first_contracts.py`
- readiness / command-flow / gate regressions if needed for behavioral coverage

## Required Wording Changes

### `SKILL.md`

The expert review section must state that:

- fixed review points are mandatory review gates,
- missing fixed review output blocks continuation,
- the main agent must spawn the reviewer before proceeding.

### `CLAUDE.md`

The package rules must state that:

- reviewer profiles are not just reference reading,
- fixed review gates require actual subagent-produced review artifacts.

### `protocol-subagent-delegation.md`

This protocol must include:

- a `Mandatory Review Gates` section,
- the four required file paths,
- missing-review blocking behavior,
- explicit bypass prohibitions.

### Stage contracts

The stage contracts must include blocking rules such as:

- before implementation code, `reviews/stage5-implementation-readiness-review.md` must exist,
- before export, `reviews/stage10-evidence-claim-review.md` must exist.

The wording should clearly describe the blocker and the required next action.

## Testing Strategy

Regression should cover both documentation contract and behavior contract.

### Contract tests

Check that:

- `protocol-subagent-delegation.md` includes mandatory review gate language,
- `SKILL.md` and `CLAUDE.md` include non-bypass language,
- the affected stage docs mention the required review files.

### Behavior tests

At minimum, add or update regression helpers so that:

- entering Stage 5 without `reviews/stage5-implementation-readiness-review.md` returns blocked behavior,
- entering export flow without `reviews/stage10-evidence-claim-review.md` returns blocked behavior.

If feasible, also add:

- a Stage 4 pre-freeze review blocker,
- a Stage 6 post-result validation-review blocker.

## Acceptance Criteria

This change is complete when:

- fixed review points are documented as hard gates,
- required review file names are explicit,
- stage contracts block continuation when the required review is missing,
- dispatcher rules forbid self-review bypass,
- regression tests fail without the mandatory-review logic and pass after it is added,
- the old `math-modeling` package remains untouched.

## Risks

### Risk 1: workflow becomes too heavy

Mitigation: only fixed review points become mandatory; risk-triggered specialists remain flexible.

### Risk 2: the package drifts back toward stage ownership

Mitigation: keep the rule that reviewers only produce findings and recommendations, not workflow ownership.

### Risk 3: documents say “mandatory” but runtime still does not enforce it

Mitigation: add behavior-focused regression checks for missing fixed-review artifacts.
