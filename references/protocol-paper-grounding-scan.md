# Protocol — Paper Grounding Scan

## Purpose

Before `/math-modeling export` finalizes Final Evidence Gate, every paper-facing number, formula, figure, and table in the export bundle must trace back to an audit document (`claims/claim-registry.md`, Stage 4 model spec, Stage 7 derivation, or a `.meta.json` next to a figure). This is the last layer of hallucination defense.

## Core Rule

`/math-modeling export` must run a paper grounding scan before writing or updating `gates/final-evidence-gate.md`. Any unanchored or unresolved item is a Blocking issue, not a warning. The scan is text-based and deterministic — it does not infer semantic equivalence.

## Anchor Conventions

The scanner uses HTML comments as explicit anchors. Anchors are textual, scannable by grep, and survive Markdown / docx export.

### Numbers

Every paper-facing number that asserts a result, ratio, magnitude, or count must precede with:

```html
<!-- claim: <claim-id> -->
```

`<claim-id>` must exist as a row in `claims/claim-registry.md`. Descriptive numbers without claim status (e.g., "Section 3 contains 5 subsections") do not require anchors; the scanner ignores numbers with no anchor unless an explicit `claim` anchor was missed.

Example:

```markdown
The Q1 WAPE is <!-- claim: c-q1-wape-baseline --> 0.288 on the validation split.
```

### Formulas

Every paper-facing formula must precede with:

```html
<!-- derivation: <stage-section-id> -->
```

`<stage-section-id>` is one of:

- `stage-4/<file>:<heading-id>` — refers to a heading or anchor inside a Stage 4 model spec markdown
- `stage-7/<file>:<heading-id>` — refers to a sensitivity / derivation document
- `appendix/<file>:<heading-id>` — refers to an appendix derivation file

The scanner verifies the file path exists and the heading/anchor exists inside it.

### Figures

Every figure (`![](path/to/x.png)` reference in the export markdown) must:

- have a sibling file `path/to/x.meta.json` (figure-level metadata)
- have an entry `path/to/x.png` referenced from `figures/figure-index.md` or any `claims/claim-registry.md` row

A `.png` without `.meta.json` is a Blocking issue regardless of registry entry.

### Tables

Every paper-facing claim table (a Markdown table whose rows assert results) must precede with:

```html
<!-- claim-table: <claim-id> -->
```

The `<claim-id>` rule mirrors the number rule.

## Scan Algorithm

For each export markdown / docx source file under `paper/` (or whatever path is declared in `gates/final-evidence-gate.md`):

1. Extract every `<!-- claim: ... -->`, `<!-- claim-table: ... -->`, `<!-- derivation: ... -->` anchor.
2. For `claim` and `claim-table`, verify the `<claim-id>` is registered in `claims/claim-registry.md`.
3. For `derivation`, verify the file path exists in the project and the heading id exists inside it.
4. Extract every `![](...png)` reference. For each, verify `<path>.meta.json` exists.
5. Aggregate results into a `paper_grounding_scan` dict with `unresolved_claims`, `unresolved_derivations`, `figures_without_meta`, and `unanchored_assertions` lists.

`unanchored_assertions` is best-effort. The scanner does NOT attempt to LLM-detect "this number should be anchored." That responsibility belongs to the Evidence/Claim Reviewer (Stage 10). The scanner catches anchored items that fail to resolve, plus figures missing meta.json.

## Result schema

```python
{
    "status": "PASS" | "BLOCKED",
    "unresolved_claims": [<claim-id>, ...],
    "unresolved_derivations": [<stage-section-id>, ...],
    "figures_without_meta": [<png path>, ...],
    "blocked_anchors": [<anchor text>, ...],   # malformed anchors
}
```

Any non-empty list under `unresolved_claims`, `unresolved_derivations`, `figures_without_meta`, or `blocked_anchors` produces `status: BLOCKED`.

## Boundary With Other v4 Protocols

| Concern | Owner |
|---|---|
| Anchor resolution at export time | this protocol |
| "Should be anchored but is not" semantic catch | `subagent-validation-paper.md` (Evidence/Claim Reviewer) |
| Figure metadata format | `references/stage-9-figure-review.md` (figure-level review) |
| Claim level enforcement | `references/protocol-readiness-gate.md` + `claims/claim-registry.md` |
| Final Evidence Gate writing | `references/evidence-gate.md` |

## Forbidden Behavior

- Do not run `/math-modeling export` without first running paper grounding scan.
- Do not record a scan result outside `gates/final-evidence-gate.md` `## Checks` section.
- Do not downgrade a Blocking scan result to Warning. The scan is hard gate, not advisory.
- Do not let LLM semantic equivalence substitute for anchor resolution. The scan is text-based by design.
- Do not anchor a number to a claim-id that does not exist in `claims/claim-registry.md` and treat the missing registry row as a follow-up. Either add the row first or remove the anchor.

## Why This Matters

`reviews/stage10-evidence-claim-review.md` (Evidence/Claim Reviewer) does the semantic audit: which claims should exist, whether claim levels match gate ceilings. It cannot reliably verify every numeric anchor in a 50-page paper export. The grounding scan is the deterministic complement: any number with an anchor must resolve, and any figure must have meta.json. Together they cover both "the right claims" (reviewer) and "the claims actually trace" (scanner).
