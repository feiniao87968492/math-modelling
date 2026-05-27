# Paper Grounding Fixture - Happy Path All Grounded

## Input scenario
- export bundle has 3 number anchors, 2 derivation anchors, 4 figures
- every claim-id resolves in `claims/claim-registry.md`
- every derivation target resolves to an existing stage-4 / stage-7 anchor
- every figure has its sibling `.meta.json`

## Scan scenario
```python
{
    "registry_claim_ids": ["c-q1-wape", "c-q2-obj", "c-q3-obj"],
    "derivation_targets_present": [
        "stage-4/model-q1.md:loss-function",
        "stage-7/sensitivity-q1.md:c-grid-search",
    ],
    "figure_meta_present": [
        "figures/q1-residuals.png",
        "figures/q1-cv.png",
        "figures/q2-packaging.png",
        "figures/q3-equipment.png",
    ],
    "paper_anchors": [
        {"kind": "claim", "target": "c-q1-wape"},
        {"kind": "claim-table", "target": "c-q2-obj"},
        {"kind": "claim", "target": "c-q3-obj"},
        {"kind": "derivation", "target": "stage-4/model-q1.md:loss-function"},
        {"kind": "derivation", "target": "stage-7/sensitivity-q1.md:c-grid-search"},
    ],
    "paper_figures": [
        "figures/q1-residuals.png",
        "figures/q1-cv.png",
        "figures/q2-packaging.png",
        "figures/q3-equipment.png",
    ],
}
```

## Expected output
- `status: PASS`
- all four lists empty
- `/math-modeling export` `export_allowed: True`

## Forbidden outcomes
- BLOCKED status when every anchor and figure resolves
- silent downgrade of `c-q3-obj` claim level even though scan passes (claim level enforcement is a different protocol)
