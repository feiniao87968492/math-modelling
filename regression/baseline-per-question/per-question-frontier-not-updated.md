# Per-Question Baseline Fixture - Per-Question Frontier Not Updated

## Input scenario
- multi-question project with `improvements/frontier-q1.md`, `frontier-q2.md`, `frontier-q3.md`
- improvement round N targets Q3 with `Cross-question impact expected: Q1 (no change), Q2 (no change)`
- user has confirmed; implementation has landed; round-N.md back 3 sections filled
- `improvements/improvement-frontier.md` index file updated
- BUT `improvements/frontier-q3.md` not updated (the proposal not moved to `Tried and kept` or `reverted`)
- `improvements/frontier-q1.md` and `frontier-q2.md` also not updated even though they were named in `Cross-question impact expected`

## State dict
```python
{
    "project_kind": "multi_question",
    "per_question_frontiers": [
        "improvements/frontier-q1.md",
        "improvements/frontier-q2.md",
        "improvements/frontier-q3.md",
    ],
    "round_n_md": {
        "target_question": "Q3",
        "cross_question_impact_list": ["Q1", "Q2"],
        "implementation_summary_filled": True,
        "before_vs_after_metrics_filled": True,
        "frontier_update_filled": True,
    },
    "improvement_log_updated": True,
    "improvement_frontier_index_updated": True,
    "per_question_frontiers_updated": [],   # none updated
}
```

## Expected output
- `ok: False`
- `blockers` contains `per_question_frontier_not_updated:Q3` (target question's file is mandatory)
- `blockers` contains `per_question_frontier_not_updated:Q1` and `per_question_frontier_not_updated:Q2` (impact list)

## Forbidden outcomes
- closing the round with only the global index updated; per-question files must reflect the actual move
- updating only the target question's file while ignoring `Cross-question impact expected` Q's
- moving a proposal to `Tried and kept` in `frontier-q3.md` while `frontier-q1.md` still lists it under `Proposed but not yet attempted`

## Why this matters
Plan 工作项 3 风险段: per-question frontier 维护噪音 → 缓解策略是"只有 round-N.md 改动跨问题时才强制对照"。这里的强制对照具体落地为：close 时检查 cross-question impact list 中每一个 Q 的 frontier file 是否更新。
