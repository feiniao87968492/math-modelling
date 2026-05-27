"""Per-question baseline / frontier checks for v4.2 工作项 3.

Multi-question competitions must keep separate baselines and frontiers per
question. This module simulates dispatcher behavior at three checkpoints:

1. Open round: refuse if round-N.md is missing `Target question` for a
   multi-question project.
2. Pre-confirm: refuse if `Cross-question impact expected` is non-empty but
   `## Risk assessment` lacks per-question baseline comparison rows for those
   questions, OR if a metric actually regressed on a non-target question and
   the regression is not cited.
3. Round close: refuse if `Cross-question impact expected` named Q's whose
   per-question frontier file was not updated.

Single-question projects (no `claims/baseline-qK.md` files) bypass these
checks entirely.
"""
from __future__ import annotations


def is_multi_question(state: dict) -> bool:
    return state.get("project_kind") == "multi_question" or bool(
        state.get("per_question_baselines")
    )


def check_target_question_declared(state: dict) -> dict:
    if not is_multi_question(state):
        return {"ok": True, "blockers": []}

    round_n = state.get("round_n_md", {})
    blockers = []
    if not round_n.get("target_question_declared", False):
        blockers.append("target_question_missing")
    if not round_n.get("cross_question_impact_declared", False):
        blockers.append("cross_question_impact_missing")
    if blockers:
        return {
            "ok": False,
            "blockers": blockers,
            "next_action": "fill `Target question` and `Cross-question impact expected` in round-N.md `## Round metadata` before synthesizing the round",
        }
    return {"ok": True, "blockers": []}


def check_cross_question_baseline_comparison(state: dict) -> dict:
    if not is_multi_question(state):
        return {"ok": True, "blockers": []}

    round_n = state.get("round_n_md", {})
    if not round_n.get("target_question_declared", False):
        return {"ok": False, "blockers": ["target_question_missing"]}

    impact_list = round_n.get("cross_question_impact_list", [])
    rows = round_n.get("risk_assessment_per_question_rows", [])

    blockers = []

    missing_rows = [q for q in impact_list if q not in rows]
    for q in missing_rows:
        blockers.append(f"cross_question_baseline_comparison_missing:{q}")

    movements = state.get("actual_metric_movements", {})
    for q, movement in movements.items():
        if q == round_n.get("target_question"):
            continue
        if movement.get("regressed") and q not in rows:
            blockers.append(f"cross_question_regression_unflagged:{q}")

    if blockers:
        return {
            "ok": False,
            "blockers": blockers,
            "next_action": "add per-question baseline comparison rows to round-N.md `## Risk assessment`; if any non-target question regressed, the row must explicitly cite the regression",
        }
    return {"ok": True, "blockers": []}


def check_per_question_frontier_close(state: dict) -> dict:
    if not is_multi_question(state):
        return {"ok": True, "blockers": []}

    round_n = state.get("round_n_md", {})
    target_question = round_n.get("target_question")
    impact_list = round_n.get("cross_question_impact_list", [])
    updated = set(state.get("per_question_frontiers_updated", []))

    blockers = []
    if target_question and target_question not in updated:
        blockers.append(f"per_question_frontier_not_updated:{target_question}")
    for q in impact_list:
        if q not in updated:
            blockers.append(f"per_question_frontier_not_updated:{q}")

    if blockers:
        return {
            "ok": False,
            "blockers": blockers,
            "next_action": "update `improvements/frontier-qK.md` for the target question and every Q listed in cross-question impact before closing the round",
        }
    return {"ok": True, "blockers": []}
