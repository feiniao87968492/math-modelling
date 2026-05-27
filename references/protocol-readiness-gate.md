# Protocol — Readiness Gate

## Purpose

Detect missing required data, tools, solvers, structured relationships, or evidence before a stage produces downstream-dependent outputs or paper claims.

## Core Rule

Readiness results must be recorded as a Markdown gate report under `gates/`. Do not silently downgrade from optimal/global outputs to heuristic or baseline outputs.

## Mandatory Checkpoints

| Checkpoint | Gate focus |
|---|---|
| Stage 4 before model freeze | variables, constraints, objective terms, relationship-data requirements |
| Stage 5 before implementation | data, solver, objective terms, supported claim level |
| Stage 10 before export | claims supported by evidence |

## Markdown gate report Required Sections

- `## Gate result`
- `## Intended claim level`
- `## Supported claim level`
- `## Checks`
- `## Allowed outputs`
- `## Blocked claims`
- `## Required branches`
- `## Required decision`

## Claim Levels

- `global_optimum`
- `validated_optimum`
- `locally_optimal_solution`
- `feasible_baseline`
- `exploratory_analysis`
- `unsupported_claim`

## Branch Rules

Create a branch document when a missing requirement is actionable and not derivable from current files.

## Blocking Confirmation Rules

Generate a blocking decision document if:

1. continuing would make the main output appear stronger than supported,
2. fallback changes confirmed method, model structure, evidence path, or claim level,
3. the user must choose between completing branches and accepting downgraded claims,
4. missing inputs block a required stage output.
