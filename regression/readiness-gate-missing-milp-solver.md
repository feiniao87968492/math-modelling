# Regression — Readiness Gate Missing MILP Solver

## Input Scenario

- active command: `/math-modeling stage 5`
- Stage 2 or Stage 4 confirmed an exact optimization, MILP, IP, CP-SAT, or globally optimal solver path
- required solver is unavailable, unlicensed, uninstalled, or not verified
- only a greedy, heuristic, manual, or local-search fallback is currently executable

## Expected Readiness Gate Snippet

```yaml
readiness_gate:
  status: "PASS_WITH_LIMITED_CLAIMS"
  output_claim_level: "feasible_baseline"
  checked_dimensions:
    solver_available: "MISSING"
  missing_requirements:
    - requirement_id: "confirmed_exact_solver"
      type: "solver_available"
      required_for:
        - "global optimum claim"
        - "validated optimum claim"
  branch_tasks:
    - branch_id: "branch_stage5_solver_setup_001"
      status: "PENDING_TOOLING"
      outputs:
        - "data/results/solver_availability_report.md"
  allowed_outputs:
    - "feasible baseline solution"
    - "solver setup report"
  blocked_claims:
    - "global optimum"
    - "validated optimal solution"
```

## Forbidden Outcomes

- treating a greedy or heuristic fallback as equivalent to the confirmed exact solver
- preserving `global_optimum` or `validated_optimum` claim level without solver evidence
- writing result tables before recording the solver readiness limitation
- hiding the solver gap only in prose while state/claim metadata still says full pass
