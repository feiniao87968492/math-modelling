# Regression - Readiness Gate Missing MILP Solver

## Input Scenario

- active command: `/math-modeling stage 5`
- Stage 2 or Stage 4 confirmed an exact optimization or MILP solver path
- required solver is unavailable, unlicensed, uninstalled, or not verified
- only a greedy or heuristic fallback is currently executable

## Expected Readiness Gate Snippet

```markdown
## Supported claim level
feasible_baseline

## Required branches
- branches/branch-stage5-solver-setup.md
```

## Forbidden Outcomes

- treating a greedy or heuristic fallback as equivalent to the confirmed exact solver
- preserving optimum claims without solver evidence
- hiding the solver gap until paper export
