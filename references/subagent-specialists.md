# Subagents — Specialists

## Purpose

Define optional specialist subagents for `math-modeling`. Specialists are not always-on reviewers. Main Orchestrator invokes them only when a protocol or stage file explicitly triggers their expertise.

## Global Specialist Boundary

Specialists may return findings, risks, recommended actions, and evidence references. Specialists must not write global state, clear confirmations, execute rollback, or mark stages complete.

## Data-Audit Specialist

Trigger when raw or processed data has unclear fields, missing values, outliers, version drift, schema ambiguity, or inconsistent units.

Return:

```yaml
specialist_result:
  specialist: "Data-Audit Specialist"
  findings:
    - severity: "WARNING"
      summary: "Column units are inconsistent across files."
      evidence:
        - "data/raw/source_a.csv"
        - "data/raw/source_b.csv"
  recommended_action: "Create or revise data dictionary before algorithm selection."
  rollback_request: null
```

## Code-Review Specialist

Trigger when Stage 5 produces solver code, reproducibility checks, or blocking implementation errors.

Return:

```yaml
specialist_result:
  specialist: "Code-Review Specialist"
  findings:
    - severity: "BLOCKING"
      summary: "Solver output is not reproducible from a clean run."
      evidence:
        - "data/results/reproducibility_check.json"
  recommended_action: "Fix deterministic inputs and rerun Stage 5."
  rollback_request: null
  pending_confirmation:
    decision_type: "stage5_reproducibility_fix"
    blocking: true
    question: "Stage 5 solver output is not reproducible. Should Stage 5 be revised before downstream validation?"
    recommended_option: "Revise Stage 5 before continuing."
```

## Figure-Review Specialist

Trigger when Stage 9 reviews figure readability, caption quality, source data alignment, or claim consistency.

Return:

```yaml
specialist_result:
  specialist: "Figure-Review Specialist"
  findings:
    - severity: "WARNING"
      summary: "Figure caption does not identify the data source."
      evidence:
        - "data/figures/figure_3.meta.json"
  recommended_action: "Revise caption and metadata before paper export."
  rollback_request: null
```

## Evidence-Gate Specialist

Trigger when Stage 10 checks whether paper claims are supported by stage outputs and files.

Return:

```yaml
specialist_result:
  specialist: "Evidence-Gate Specialist"
  findings:
    - severity: "BLOCKING"
      summary: "Primary innovation claim lacks supporting comparison output."
      evidence:
        - "data/paper/claim_registry.yaml"
  recommended_action: "Return to Stage 3 or Stage 5 to generate evidence for the comparison."
  rollback_request:
    from_stage: 10
    target_stage: 3
    severity: "STRUCTURAL_REVISION"
    reason: "innovation claim lacks supporting comparison output"
    evidence:
      - "data/paper/claim_registry.yaml"
    affected_outputs:
      - "data/paper/innovation_summary.md"
    requires_user_confirmation: true
    recommended_action: "revise innovation claim or generate valid comparison evidence"
```

## Literature/Method Search Specialist

Trigger when a method background or external reference is required and cannot be answered from local materials. Network access must follow the available web-access workflow and user authorization requirements.

Return:

```yaml
specialist_result:
  specialist: "Literature/Method Search Specialist"
  findings:
    - severity: "INFO"
      summary: "A comparable method family exists and should be considered as a baseline."
      evidence:
        - "external reference captured through authorized web workflow"
  recommended_action: "Add the method as a candidate in Stage 2 before final algorithm confirmation."
  rollback_request: null
```
