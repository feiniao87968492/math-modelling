# Paper Grounding Fixture - Formula Without Derivation Link

## Input scenario
- export markdown contains a formula with anchor `<!-- derivation: stage-7/sensitivity-q1.md:c-grid-search -->`
- the file `stage-7/sensitivity-q1.md` exists in the project but the `c-grid-search` heading anchor inside it does NOT exist (e.g., misnamed or moved)
- another formula's `<!-- derivation: stage-4/model-q1.md:loss-function -->` resolves correctly

## Scan scenario
```python
{
    "registry_claim_ids": [],
    "derivation_targets_present": [
        "stage-4/model-q1.md:loss-function",
    ],
    "figure_meta_present": [],
    "paper_anchors": [
        {"kind": "derivation", "target": "stage-4/model-q1.md:loss-function"},
        {"kind": "derivation", "target": "stage-7/sensitivity-q1.md:c-grid-search"},
    ],
    "paper_figures": [],
}
```

## Expected output
- `status: BLOCKED`
- `unresolved_derivations` contains `stage-7/sensitivity-q1.md:c-grid-search`
- `unresolved_derivations` does NOT contain `stage-4/model-q1.md:loss-function`
- `/math-modeling export` `export_allowed: False`

## Forbidden outcomes
- accepting "the file exists" as resolution; the heading anchor inside the file must also exist
- LLM-equivalent resolution ("they probably meant `c-search-grid`")
- promoting the formula to "ungrounded but cited in spec" (not a category — it's just BLOCKED)
