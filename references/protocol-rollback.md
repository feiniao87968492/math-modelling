# Protocol — Rollback

## Purpose

Define how later stages request controlled rollback when validation, sensitivity analysis, visualization, figure review, or claim grounding exposes defects in earlier modeling work.

## Core Rule

Stages 6-10 MUST NOT silently patch defects that belong to stages 1-5.

If a defect affects problem interpretation, assumptions, model structure, algorithm choice, implementation, result stability, or claim support, the owning subagent must generate `rollback_request` and return it to the Main Orchestrator.

## Severity Levels

| Severity | Meaning | Default Target |
|----------|---------|----------------|
| `MINOR_REVISION` | Issue is limited to explanation, figure styling, caption wording, table formatting, or non-structural paper expression. | Stay in stages 6-10 |
| `METHOD_REVISION` | Algorithm, parameter bounds, solver implementation, reproducibility, result stability, or model constraint implementation is defective. | Stage 5, or Stage 4 if equations/constraints must change |
| `STRUCTURAL_REVISION` | Problem interpretation, core assumption, algorithm route, model structure, or innovation claim is invalid. | Stage 1, Stage 2, or Stage 3 |

## rollback_request Schema

```yaml
rollback_request:
  from_stage: 7
  target_stage: 5
  severity: "METHOD_REVISION"
  reason: "sensitivity analysis shows unstable output"
  evidence:
    - "data/validation/sensitivity_report.md"
  affected_outputs:
    - "data/results/main_result.csv"
    - "data/model_spec.yaml"
  requires_user_confirmation: true
  recommended_action: "rerun stage 5 with revised parameter bounds"
```

Required fields:

- `from_stage`
- `target_stage`
- `severity`
- `reason`
- `evidence`
- `affected_outputs`
- `requires_user_confirmation`
- `recommended_action`

## Confirmation Rules

- `MINOR_REVISION` may continue without blocking confirmation if no confirmed method, model structure, evidence path, or paper claim changes.
- `METHOD_REVISION` requires blocking confirmation unless the user already approved the exact fallback path.
- `STRUCTURAL_REVISION` always requires blocking confirmation.
- User silence never approves rollback.

## State Writeback Rules

When Main Orchestrator accepts a rollback request, it must:

1. Write the rollback request into `modeling_state.yaml` under `quality_systems.rollback_requests`.
2. If confirmation is required, write a blocking item into `human_interaction.pending_confirmations`.
3. Set the current stage to `HUMAN_REVIEW_REQUIRED` when confirmation is pending.
4. After confirmation, set `current_stage` to the rollback target stage.
5. Set the target stage to `NEEDS_REVISION` or `IN_PROGRESS` according to the decision.
6. Keep affected downstream stages from being marked `DONE` until regenerated or explicitly accepted by the user.

## rollback_response Contract

Stages 1-5 may receive a rollback request. Their owning subagent must return:

```yaml
rollback_response:
  target_stage: 5
  accepted_request: true
  revised_outputs:
    - "data/results/main_result.csv"
  unchanged_outputs:
    - "data/model_spec.yaml"
  downstream_invalidated:
    - 6
    - 7
    - 8
  pending_confirmation: null
  memory_check_recommendation:
    action: "write memory"
    reason: "Parameter bounds should be checked before sensitivity analysis in similar models."
```

## Non-Goals

Rollback does not replace Human Confirmation, memory check, State Writeback, Fallback Control, or Final Evidence Gate. It connects those protocols when later stages expose earlier defects.
