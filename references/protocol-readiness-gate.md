# Protocol — Readiness Gate

## Purpose

Detect missing required data, tools, solvers, structured relationships, or evidence before a stage produces downstream-dependent outputs or paper claims.

Readiness Gate is proactive. It runs before execution. Rollback is reactive. It runs after later stages expose an earlier defect.

## Core Rule

Before stages that depend on critical inputs or tools, the owning subagent must return a `readiness_gate` object. If required items are missing and the missing items would lower claim credibility, the Main Orchestrator must either create branch tasks or generate a blocking confirmation before continuing.

Do not silently downgrade from optimal/global/claim-supporting outputs to heuristic/baseline outputs.

## Mandatory Checkpoints

| Checkpoint | Gate Focus |
|------------|------------|
| Stage 4 before freezing model structure | Are all objective terms, variables, constraints, and relationship data requirements identified? |
| Stage 5 before implementation/results | Are primary data, relationship data, solver, objective terms, and output claim level ready? |
| Stage 6 before validation conclusion | Can validation verify the claim level being made, or only a weaker baseline claim? |
| Stage 7 before sensitivity conclusion | Are perturbations re-optimized when needed, or only post-solution metric perturbations? |
| Stage 10 before paper claims/export | Are all claims supported by evidence at the required claim level? |

## Readiness Dimensions

Use these stable keys where applicable:

- `structured_primary_data`
- `structured_relationship_data`
- `solver_available`
- `objective_terms_available`
- `parameter_ranges_justified`
- `reoptimization_available`
- `validation_oracle_available`
- `figure_evidence_available`
- `claim_evidence_available`
- `output_claim_level`

## Status Values

- `PASS`: all required items for the intended claim level are available.
- `PASS_WITH_LIMITED_CLAIMS`: stage may continue, but only weaker outputs/claims are allowed.
- `BLOCKED_MISSING_REQUIRED_INPUTS`: missing data prevents intended outputs/claims.
- `BLOCKED_MISSING_REQUIRED_TOOL`: missing solver/tool prevents intended outputs/claims.
- `BLOCKED_UNJUSTIFIED_SCOPE`: perturbation ranges, assumptions, or claim scope lack support.

## Claim Levels

Use `output_claim_level` to prevent overclaiming:

- `global_optimum`
- `validated_optimum`
- `locally_optimal_solution`
- `feasible_baseline`
- `exploratory_analysis`
- `unsupported_claim`

If the readiness gate returns `feasible_baseline`, blocked claims must include any stronger claim that the result cannot support.

## Required Object Shape

```yaml
readiness_gate:
  status: "PASS_WITH_LIMITED_CLAIMS"
  output_claim_level: "feasible_baseline"
  checked_dimensions:
    structured_primary_data: "PASS"
    structured_relationship_data: "MISSING"
    solver_available: "MISSING"
    objective_terms_available: "PARTIAL"
  missing_requirements:
    - requirement_id: "courtyard_adjacency_edges"
      type: "structured_relationship_data"
      reason: "Adjacency premium requires courtyard edge list; only image is available."
      required_for:
        - "adjacency premium"
        - "Q2 revenue calculation"
        - "Q3 ROI breakpoint"
      suggested_branch: "branch_stage5_adjacency_data_001"
    - requirement_id: "milp_solver"
      type: "solver_available"
      reason: "Confirmed model is MILP but only greedy fallback is available."
      required_for:
        - "global optimum claim"
      suggested_branch: "branch_stage5_solver_setup_001"
  branch_tasks:
    - branch_id: "branch_stage5_adjacency_data_001"
      title: "Create structured courtyard adjacency edge table"
      status: "PENDING_USER_INPUT"
      outputs:
        - "data/processed/courtyard_adjacency_template.csv"
    - branch_id: "branch_stage5_solver_setup_001"
      title: "Enable exact or MILP-compatible solver"
      status: "PENDING_TOOLING"
      outputs:
        - "data/results/solver_availability_report.md"
  allowed_outputs:
    - "feasible baseline solution"
    - "data template"
    - "validation warning"
  blocked_claims:
    - "global optimum"
    - "validated optimal relocation plan"
    - "true ROI breakpoint"
  recommended_user_choices:
    - "A. Complete missing branch tasks before solving"
    - "B. Continue with baseline outputs and limited claims"
    - "C. Pause stage until data/tooling is ready"
  pending_confirmation: null
```

## Branch Task Rules

Create a branch task when a missing requirement is actionable and not derivable from current files.

Branch task minimum fields:

```yaml
branch_id: "branch_stage5_adjacency_data_001"
stage: 5
reason: "missing structured courtyard adjacency"
status: "PENDING_USER_INPUT"
required_for:
  - "adjacency premium"
  - "global ROI"
  - "Q2/Q3 final claim"
outputs:
  - "data/processed/courtyard_adjacency_template.csv"
```

Branch status values:

- `PENDING_USER_INPUT`
- `PENDING_DATA_AUDIT`
- `PENDING_TOOLING`
- `IN_PROGRESS`
- `DONE`
- `DEFERRED_WITH_LIMITED_CLAIMS`

## Blocking Confirmation Rules

Generate a blocking confirmation if any of the following is true:

1. Continuing would make the main output appear stronger than supported by evidence.
2. A fallback changes confirmed method, model structure, evidence path, or claim level.
3. The user must choose between completing branch tasks and accepting downgraded claim level.
4. Missing inputs block a required stage output.

Non-blocking continuation is allowed only when:

- `status: PASS`, or
- `status: PASS_WITH_LIMITED_CLAIMS` and the downgraded claim level is explicitly written to outputs and state.

## State Writeback Guidance

When a readiness gate finds missing requirements, Main Orchestrator should write recommended branch tasks under `quality_systems.readiness_branches` or the current stage record, depending on the project state schema.

Example:

```yaml
quality_systems:
  readiness_branches:
    - branch_id: "branch_stage5_adjacency_data_001"
      stage: 5
      status: "PENDING_USER_INPUT"
      reason: "missing structured courtyard adjacency"
      required_for:
        - "adjacency premium"
      outputs:
        - "data/processed/courtyard_adjacency_template.csv"
```

## Relationship to Fallback and Rollback

- Fallback protocol controls method deviation when execution cannot follow the planned method.
- Readiness Gate checks whether such deviation is likely before execution.
- Rollback protocol handles defects discovered after downstream validation.

If readiness gate catches the issue early, prefer branch tasks and pending confirmation over later rollback.
