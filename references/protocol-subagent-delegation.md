# Protocol — Subagent Delegation

## Purpose

Define how `math-modeling` uses Lean Swarm delegation while keeping the Main Orchestrator responsible for global state, user confirmations, memory checks, and rollback execution.

## Default Mode

Default mode is Lean Swarm.

- Stages 1-5 MUST be delegated to Model-Building Subagent.
- Stages 6-10 MUST be delegated to Validation-Paper Subagent.
- Specialist subagents MAY be invoked only when explicitly triggered by a protocol or stage file.
- Subagents must return structured outputs, not free-form discussion.
- Subagents may recommend state changes, but only Main Orchestrator can write global state.
- Subagents may propose `rollback_request`, but cannot execute rollback directly.

## Authority Boundary

Main Orchestrator owns:

- active command and stage detection
- required reference loading
- `modeling_state.yaml` writes
- `memory.md` read and memory check
- `pending_confirmations`
- user-facing blocking confirmation
- rollback classification and execution
- final stage status transitions

Subagents own:

- scoped analysis for their assigned stage group
- candidate recommendations
- structured output drafts
- quality findings
- rollback recommendations or rollback requests

Subagents MUST NOT:

- mark a stage `DONE`
- write `modeling_state.yaml`
- clear `pending_confirmations`
- treat user silence as approval
- execute rollback without Main Orchestrator approval
- skip required protocol reads

## Routing Map

| Stage | Owning Subagent |
|-------|-----------------|
| 1 | Model-Building Subagent |
| 2 | Model-Building Subagent |
| 3 | Model-Building Subagent |
| 4 | Model-Building Subagent |
| 5 | Model-Building Subagent |
| 6 | Validation-Paper Subagent |
| 7 | Validation-Paper Subagent |
| 8 | Validation-Paper Subagent |
| 9 | Validation-Paper Subagent |
| 10 | Validation-Paper Subagent |

## Specialist Trigger Map

| Specialist | Trigger |
|------------|---------|
| Data-Audit Specialist | Raw or processed data has unclear fields, missing values, outliers, version drift, or schema ambiguity. |
| Code-Review Specialist | Stage 5 produces solver code, reproducibility checks, or blocking implementation errors. |
| Figure-Review Specialist | Stage 9 reviews figure readability, caption quality, and evidence consistency. |
| Evidence-Gate Specialist | Stage 10 checks whether claims are supported by files and stage outputs. |
| Literature/Method Search Specialist | A method background or external reference is required and cannot be answered from local materials. |

## Delegation Input Contract

When delegating, Main Orchestrator must provide:

```yaml
delegation_request:
  active_stage: 7
  stage_name: "Sensitivity Analysis"
  owning_subagent: "Validation-Paper Subagent"
  required_reads:
    - "references/protocol-human-confirmation.md"
    - "references/protocol-memory-update.md"
    - "references/protocol-state-writeback.md"
    - "references/protocol-subagent-delegation.md"
    - "references/protocol-rollback.md"
    - "references/stage-7-sensitivity-analysis.md"
  available_inputs:
    - "data/results/main_result.csv"
    - "data/model_spec.yaml"
  expected_outputs:
    - "data/sensitivity/sensitivity_table.csv"
    - "data/sensitivity/sensitivity_conclusion.md"
    - "data/sensitivity/sensitivity_meta.json"
    - "data/sensitivity/innovation_attribution.md"
  blocking_confirmation_policy: "Generate pending confirmation before downstream-dependent decisions."
  state_write_policy: "Recommend changes only; Main Orchestrator writes global state."
```

## Delegation Output Contract

Subagents must return:

```yaml
subagent_result:
  owning_subagent: "Validation-Paper Subagent"
  active_stage: 7
  status_recommendation: "DONE"
  outputs:
    - path: "data/sensitivity/sensitivity_table.csv"
      purpose: "Record parameter perturbation values and observed metrics."
    - path: "data/sensitivity/sensitivity_conclusion.md"
      purpose: "Summarize parameter sensitivity findings."
    - path: "data/sensitivity/sensitivity_meta.json"
      purpose: "Record perturbation settings and reproducibility metadata."
    - path: "data/sensitivity/innovation_attribution.md"
      purpose: "Connect sensitivity findings to confirmed innovation claims."
  findings:
    - severity: "INFO"
      summary: "Main result is stable within tested perturbation bounds."
      evidence:
        - "data/sensitivity/perturbation_table.csv"
  readiness_gate:
    status: "PASS_WITH_LIMITED_CLAIMS"
    output_claim_level: "feasible_baseline"
    missing_requirements: []
    branch_tasks: []
    allowed_outputs: []
    blocked_claims: []
  pending_confirmation: null
  rollback_request: null
  memory_check_recommendation:
    action: "no new memory"
    reason: "No reusable modeling rule was discovered."
```

If required inputs, tools, relationship data, solver capability, or evidence are missing, `readiness_gate` must describe the missing requirements, branch tasks, allowed outputs, and blocked claims according to `references/protocol-readiness-gate.md`.

If a blocking decision is needed, `pending_confirmation` must be populated. If a previous stage must be revisited, `rollback_request` must be populated according to `references/protocol-rollback.md`.
