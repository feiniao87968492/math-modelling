# Regression — Readiness Gate Feasible Baseline Claim Limit

## Input Scenario

- active command: `/math-modeling stage 6`, `/math-modeling stage 7`, or `/math-modeling gate`
- Stage 5 output is a hard-constraint-valid baseline, greedy solution, heuristic solution, or single-scenario computation
- validation checks feasibility, budget, uniqueness, or metric reproduction only
- no evidence exists for global optimality, re-optimized sensitivity, or parameterized ROI breakpoint

## Expected Readiness Gate Snippet

```yaml
readiness_gate:
  status: "PASS_WITH_LIMITED_CLAIMS"
  output_claim_level: "feasible_baseline"
  missing_requirements:
    - requirement_id: "optimality_evidence"
      type: "evidence"
      required_for:
        - "global optimum claim"
    - requirement_id: "reoptimized_parameter_sweep"
      type: "evidence"
      required_for:
        - "true ROI breakpoint"
  allowed_outputs:
    - "feasibility validation"
    - "baseline comparison"
    - "limited sensitivity warning"
  blocked_claims:
    - "global optimum"
    - "validated optimum"
    - "true ROI breakpoint"
```

## Forbidden Outcomes

- marking validation as fully supporting paper claims when it only checks hard constraints
- using post-solution metric perturbation as evidence for strategy stability under re-optimization
- exporting a claim registry with stronger claims than the readiness gate permits
- burying claim downgrades in prose while `claim_registry` keeps stronger labels
