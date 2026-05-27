# Per-Question Baseline Fixture - Target Question Missing

## Input scenario
- multi-question project (Q1, Q2, Q3 each have a `claims/baseline-qK.md`)
- main agent opens `improvements/round-N.md` for a new round
- main agent forgets to declare `Target question` in `## Round metadata`
- `Cross-question impact expected` is also absent

## State dict
```python
{
    "project_kind": "multi_question",
    "per_question_baselines": ["claims/baseline-q1.md", "claims/baseline-q2.md", "claims/baseline-q3.md"],
    "round_n_md": {
        "target_question_declared": False,
        "cross_question_impact_declared": False,
        "risk_assessment_per_question_rows": [],
    },
}
```

## Expected output
- `ok: False`
- `blockers` contains `target_question_missing`
- `next_action` requires the main agent to fill `Target question` (and `Cross-question impact expected`) before synthesizing the round

## Forbidden outcomes
- treating missing `Target question` as default `all` for multi-question projects (only single-question projects are allowed that default)
- letting Critique reviewer be spawned without `Target question` declared
- moving any proposal into a per-question frontier without an explicit target

## Why this matters
Without `Target question`, Skepticism reviewer cannot opine on cross-question regression risk, and the per-question frontier files cannot be correctly updated at close. Caught conceptually by v4.2 plan 工作项 3 risk段; this fixture pins it.
