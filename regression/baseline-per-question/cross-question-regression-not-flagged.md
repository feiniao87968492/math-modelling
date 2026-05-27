# Per-Question Baseline Fixture - Cross-Question Regression Not Flagged

## Input scenario
- multi-question project: Q1 baseline metric WAPE = 0.288, Q2 obj = 9,016,061, Q3 obj = 9,893,432
- improvement round N targets Q3 (Target question: Q3)
- main agent declares `Cross-question impact expected: Q1 (no change), Q2 (no change)`
- but the round implementation actually moves Q1 WAPE from 0.288 to 0.305 (regression)
- `## Risk assessment` in round-N.md still says "no Q1 / Q2 impact expected" without per-question baseline comparison rows
- Skepticism reviewer opined that Q1 regression risk was unaddressed

## State dict
```python
{
    "project_kind": "multi_question",
    "per_question_baselines": ["claims/baseline-q1.md", "claims/baseline-q2.md", "claims/baseline-q3.md"],
    "round_n_md": {
        "target_question_declared": True,
        "target_question": "Q3",
        "cross_question_impact_declared": True,
        "cross_question_impact_list": ["Q1", "Q2"],
        "risk_assessment_per_question_rows": [],   # missing
    },
    "actual_metric_movements": {
        "Q1": {"baseline": 0.288, "after": 0.305, "regressed": True},
        "Q2": {"baseline": 9016061, "after": 9016061, "regressed": False},
        "Q3": {"baseline": 9893432, "after": 9700000, "regressed": False},
    },
    "skepticism_blocking_includes_q1_regression": True,
}
```

## Expected output
- `ok: False`
- `blockers` contains `cross_question_baseline_comparison_missing` (covers `Q1`, `Q2`)
- `blockers` may additionally contain `cross_question_regression_unflagged` because Q1 actually regressed

## Forbidden outcomes
- closing the round with a Q1 regression that the round-N.md `## Risk assessment` did not cite
- treating "no impact expected" as a substitute for an actual per-question baseline comparison row
- promoting the round to `Tried and kept` in `improvements/frontier-q3.md` without first updating `frontier-q1.md` to reflect Q1 regression

## Why this matters
Plan 工作项 3 identifies "Q3 改进可能反向影响 Q1 但单一 baseline 不会让 reviewer 注意到 'Q3 提升 Q1 退步' 这种 Pareto 退化" as the headline competition realism gap.
