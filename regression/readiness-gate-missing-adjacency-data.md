# Regression — Readiness Gate Missing Adjacency Data

## Input Scenario

- active command: `/math-modeling stage 5`
- confirmed model uses adjacency, network, distance, pairing, or neighborhood benefits
- available source is an image, prose description, or human-readable diagram only
- no machine-readable edge list, adjacency matrix, distance table, or pairing table exists

## Expected Readiness Gate Snippet

```yaml
readiness_gate:
  status: "PASS_WITH_LIMITED_CLAIMS"
  output_claim_level: "feasible_baseline"
  checked_dimensions:
    structured_relationship_data: "MISSING"
  missing_requirements:
    - requirement_id: "structured_relationship_data"
      type: "structured_relationship_data"
      required_for:
        - "adjacency benefit"
        - "network relationship claim"
  branch_tasks:
    - branch_id: "branch_stage5_relationship_data_001"
      status: "PENDING_USER_INPUT"
      outputs:
        - "data/processed/relationship_edges_template.csv"
  blocked_claims:
    - "adjacency/network benefit"
    - "validated optimal plan using relationship benefits"
```

## Forbidden Outcomes

- silently ignoring the adjacency/network term while keeping the original claim
- computing relationship benefits from a screenshot without a reproducible structured table
- marking Stage 5 as full `PASS` for a model whose confirmed objective requires missing relationship data
- delaying the missing-data warning until Stage 6 or Stage 10
