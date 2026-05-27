"""Time-budget protocol simulator for v4.2 工作项 4.

Deterministic checks at three dispatcher checkpoints:
- stage switch (`/math-modeling stage N`)
- improvement round open (`/math-modeling improve`)
- export (`/math-modeling export`)

If `time-budget.md` is absent (state["time_budget_present"] == False), every
check returns `{ok: True, applied: False}` so v4.1 behavior is preserved.

If present, the simulator evaluates:
1. previous stage stopped before next-stage start
2. remaining budget vs advisory threshold (with once-per-stage rule)
3. hard deadline vs current time

The simulator does NOT track wall-clock time itself; the caller declares
`remaining_hours`, `hard_deadline_passed`, etc. in the scenario dict so the
test suite stays deterministic.
"""
from __future__ import annotations


def _not_applicable() -> dict:
    return {"ok": True, "blockers": [], "applied": False}


def check_stage_switch(state: dict) -> dict:
    if not state.get("time_budget_present", False):
        return _not_applicable()

    blockers = []

    if (
        state.get("current_stage_status") == "in_progress"
        and not state.get("stop_event_recorded_for_current_stage", False)
    ):
        blockers.append("previous_stage_not_stopped")

    advisory = _maybe_emit_advisory(state)
    if advisory.get("required"):
        blockers.append("time_pressure_advisory_required")

    if state.get("hard_deadline_passed", False):
        blockers.append("hard_deadline_passed")

    result = {"ok": not blockers, "blockers": blockers, "applied": True}
    if advisory.get("required"):
        result["advisory"] = advisory["payload"]
    if blockers:
        result["next_action"] = _next_action_for(blockers)
    return result


def check_improve_open(state: dict) -> dict:
    if not state.get("time_budget_present", False):
        return _not_applicable()

    blockers = []

    advisory = _maybe_emit_advisory(state)
    if advisory.get("required"):
        blockers.append("time_pressure_advisory_required")

    if state.get("hard_deadline_passed", False):
        blockers.append("hard_deadline_passed")

    result = {"ok": not blockers, "blockers": blockers, "applied": True}
    if advisory.get("required"):
        result["advisory"] = advisory["payload"]
    if blockers:
        result["next_action"] = _next_action_for(blockers)
    return result


def check_export(state: dict) -> dict:
    if not state.get("time_budget_present", False):
        return _not_applicable()

    blockers = []

    if state.get("hard_deadline_passed", False):
        blockers.append("hard_deadline_passed")

    advisory = _maybe_emit_advisory(state)
    if advisory.get("required"):
        blockers.append("time_pressure_advisory_required")

    result = {"ok": not blockers, "blockers": blockers, "applied": True}
    if advisory.get("required"):
        result["advisory"] = advisory["payload"]
    if blockers:
        result["next_action"] = _next_action_for(blockers)
    return result


def _maybe_emit_advisory(state: dict) -> dict:
    remaining = state.get("remaining_hours", 0)
    total = state.get("total_hours", 1)
    threshold_pct = state.get("advisory_threshold_pct", 20)
    if total <= 0:
        return {"required": False}
    pct = (remaining / total) * 100
    below_threshold = pct < threshold_pct
    if not below_threshold:
        return {"required": False}
    if state.get("advisory_already_confirmed_this_stage", False):
        return {"required": False}
    payload = {
        "remaining_hours": remaining,
        "remaining_pct": round(pct, 1),
        "threshold_pct": threshold_pct,
        "top_remaining_stages": state.get("top_remaining_stages", []),
        "user_actions": [
            "lower_target_claim_level",
            "skip_optional_stages",
            "trigger_model_simplification_reviewer",
        ],
    }
    return {"required": True, "payload": payload}


def _next_action_for(blockers: list) -> str:
    actions = []
    if "previous_stage_not_stopped" in blockers:
        actions.append("invoke `/math-modeling time stop N` for the previous stage before starting the next one")
    if "time_pressure_advisory_required" in blockers:
        actions.append("acknowledge time-pressure advisory and choose one of: lower claim level / skip optional stages / trigger model simplification reviewer")
    if "hard_deadline_passed" in blockers:
        actions.append("either explicitly extend `## Hard deadline` in time-budget.md (with acknowledgment) or accept the export as overdue")
    return "; ".join(actions)
