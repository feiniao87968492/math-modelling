# Expected Flags - mm-implementation-readiness-reviewer × stage5-buggy-implementation-mismatch

## Required flags
- solver-route-mismatches-spec
- dt-divergence-from-spec

## Recommended additional flags
- cfl-violation-risk
- implementation-must-not-proceed-without-rollback

## Verdict
BLOCKED

## Notes
solver-route-mismatches-spec and dt-divergence-from-spec are the two flags that any reviewer reading the model spec carefully should produce. CFL stability is more domain-specific and listed as recommended.
