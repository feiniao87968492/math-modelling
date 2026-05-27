# Paper Grounding Fixture - Number Without Claim Entry

## Input scenario
- export markdown contains `<!-- claim: c-q1-wape -->` followed by 0.288
- but `claims/claim-registry.md` has no row with id `c-q1-wape`
- main agent forgot to add the row before exporting

## Scan scenario
```python
{
    "registry_claim_ids": ["c-q2-obj", "c-q3-obj"],         # c-q1-wape missing
    "derivation_targets_present": [],
    "figure_meta_present": [],
    "paper_anchors": [
        {"kind": "claim", "target": "c-q1-wape"},
    ],
    "paper_figures": [],
}
```

## Expected output
- `status: BLOCKED`
- `unresolved_claims` contains `c-q1-wape`
- `/math-modeling export` `export_allowed: False`

## Forbidden outcomes
- letting the export proceed because the rest of the bundle is fine
- treating "registry will be updated later" as acceptable (the protocol forbids registering after-the-fact)
- downgrading to Warning instead of Blocking
