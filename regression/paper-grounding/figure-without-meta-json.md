# Paper Grounding Fixture - Figure Without Meta JSON

## Input scenario
- export markdown contains `![](figures/q1-residuals.png)`
- `figures/q1-residuals.png` exists
- `figures/q1-residuals.meta.json` does NOT exist
- the rest of the bundle is fine

## Scan scenario
```python
{
    "registry_claim_ids": ["c-q1-wape"],
    "derivation_targets_present": [],
    "figure_meta_present": [
        "figures/q1-cv.png",                # different figure happens to have meta
    ],
    "paper_anchors": [
        {"kind": "claim", "target": "c-q1-wape"},
    ],
    "paper_figures": [
        "figures/q1-residuals.png",         # missing meta.json
    ],
}
```

## Expected output
- `status: BLOCKED`
- `figures_without_meta` contains `figures/q1-residuals.png`
- `/math-modeling export` `export_allowed: False`

## Forbidden outcomes
- letting the figure pass because the corresponding `.png` exists (only meta.json absence matters here)
- Stage 9 figure review's existence as a substitute for meta.json (different protocol layer)
- bypass via "just regenerate the figure later"
