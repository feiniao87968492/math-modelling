"""Command-flow harness for `/math-modeling improve` and its sub-commands.

The harness is a deterministic simulation of dispatcher behavior. It accepts a
command string plus a project-state dict and returns whether the dispatcher
would proceed, block, or require user confirmation. It does not actually spawn
reviewers or execute writes; that is the main agent's responsibility at runtime.

Test fixtures live under regression/improve-flow-fixtures/. Each fixture is a
project-state dict captured as a Markdown file or inline literal.

Covered commands:
    /math-modeling improve              ── new round entry
    /math-modeling improve close        ── round closure

Covered checks:
    1. Preconditions (baseline-snapshot, Stage 7, no pending decision, no in-progress round)
    2. Reviewer dispatch order (Critique before Skepticism)
    3. round-N.md section ordering (front 6 sections before user confirm,
       back 3 sections only after implementation lands)
    4. Round close requirements (frontier + log update, before/after metrics)
"""
from __future__ import annotations

REQUIRED_PRECONDITIONS = [
    "stage6_review_pass",
    "baseline_snapshot_frozen",
    "stage7_sensitivity_present",
    "no_pending_decision",
    "no_in_progress_round",
]


def _parse_command(command_text: str) -> dict:
    parts = command_text.strip().split()
    if not parts or parts[0] != "/math-modeling":
        return {"ok": False, "error": "unsupported_command"}
    if len(parts) < 2 or parts[1] != "improve":
        return {"ok": False, "error": "unsupported_command"}
    if len(parts) == 2:
        return {"ok": True, "subcommand": "open"}
    if len(parts) == 3 and parts[2] == "close":
        return {"ok": True, "subcommand": "close"}
    if len(parts) == 3 and parts[2] == "status":
        return {"ok": True, "subcommand": "status"}
    if len(parts) == 4 and parts[2] == "round":
        try:
            return {"ok": True, "subcommand": "open", "round_number": int(parts[3])}
        except ValueError:
            return {"ok": False, "error": "unsupported_command"}
    return {"ok": False, "error": "unsupported_command"}


def _check_preconditions(state: dict) -> list:
    failed = []
    if not state.get("stage6_review_pass", False):
        failed.append("stage6_review_not_pass")
    if not state.get("baseline_snapshot_frozen", False):
        failed.append("baseline_snapshot_missing")
    if not state.get("stage7_sensitivity_present", False):
        failed.append("stage7_sensitivity_missing")
    if state.get("pending_decisions"):
        failed.append("pending_decision_present")
    if state.get("in_progress_round"):
        failed.append("in_progress_round_present")
    return failed


def run_improve_command_flow(command_text: str, state: dict) -> dict:
    parsed = _parse_command(command_text)
    if not parsed.get("ok"):
        return {"ok": False, "error": parsed.get("error", "unsupported_command")}

    sub = parsed["subcommand"]

    if sub == "status":
        return {
            "ok": True,
            "command": {"active_command": "improve", "subcommand": "status"},
            "frontier_path": "improvements/improvement-frontier.md",
            "log_path": "improvements/improvement-log.md",
        }

    if sub == "open":
        failed = _check_preconditions(state)
        if failed:
            return {
                "ok": False,
                "command": {"active_command": "improve", "subcommand": "open"},
                "blockers": failed,
                "next_action": "write blocker explanation per protocol-improvement-loop.md, do not spawn Critique",
            }

        critique_present = state.get("critique_review_present", False)
        skepticism_present = state.get("skepticism_review_present", False)

        if not critique_present:
            return {
                "ok": True,
                "command": {"active_command": "improve", "subcommand": "open"},
                "next_action": "emit reviewer invocation template for Improvement-Critique Reviewer",
                "expected_output_path": "reviews/improvement-round-N-critique.md",
                "blockers": [],
            }

        if critique_present and not skepticism_present:
            return {
                "ok": True,
                "command": {"active_command": "improve", "subcommand": "open"},
                "next_action": "emit reviewer invocation template for Improvement-Skepticism Reviewer",
                "expected_output_path": "reviews/improvement-round-N-skepticism.md",
                "required_skepticism_reads": ["reviews/improvement-round-N-critique.md"],
                "blockers": [],
            }

        round_n_state = state.get("round_n_md", {})
        front_six_present = round_n_state.get("front_six_sections_present", False)
        back_three_present = round_n_state.get("back_three_sections_present", False)
        confirmed = state.get("decision_confirmed", False)

        if back_three_present and not confirmed:
            return {
                "ok": False,
                "command": {"active_command": "improve", "subcommand": "open"},
                "blockers": ["round_n_back_sections_written_before_confirm"],
                "next_action": "remove implementation-summary / before-vs-after / frontier-update sections; restore PENDING state",
            }

        if not front_six_present:
            return {
                "ok": True,
                "command": {"active_command": "improve", "subcommand": "open"},
                "next_action": "synthesize round-N.md front 6 sections + open decision-improvement-round-N.md PENDING",
                "blockers": [],
            }

        if not confirmed:
            return {
                "ok": True,
                "command": {"active_command": "improve", "subcommand": "open"},
                "next_action": "wait for user confirm on decision-improvement-round-N.md",
                "blockers": ["awaiting_user_confirmation"],
            }

        return {
            "ok": True,
            "command": {"active_command": "improve", "subcommand": "open"},
            "next_action": "route confirmed change via rollback if needed; then re-enter Stage 5/6 work slices",
            "blockers": [],
        }

    if sub == "close":
        if not state.get("decision_confirmed", False):
            return {
                "ok": False,
                "command": {"active_command": "improve", "subcommand": "close"},
                "blockers": ["round_not_confirmed"],
                "next_action": "user must confirm decision-improvement-round-N.md before close",
            }

        round_n_state = state.get("round_n_md", {})
        impl_summary = round_n_state.get("implementation_summary_filled", False)
        before_after = round_n_state.get("before_vs_after_metrics_filled", False)
        frontier_update = round_n_state.get("frontier_update_filled", False)
        log_updated = state.get("improvement_log_updated", False)
        frontier_updated = state.get("improvement_frontier_updated", False)
        stage6_rerun = state.get("stage6_validation_rerun", False)

        missing = []
        if not impl_summary:
            missing.append("round_n_implementation_summary_missing")
        if not before_after:
            missing.append("round_n_before_vs_after_missing")
        if not frontier_update:
            missing.append("round_n_frontier_update_missing")
        if not log_updated:
            missing.append("improvement_log_not_updated")
        if not frontier_updated:
            missing.append("improvement_frontier_not_updated")
        if not stage6_rerun:
            missing.append("stage6_validation_not_rerun")

        if missing:
            return {
                "ok": False,
                "command": {"active_command": "improve", "subcommand": "close"},
                "blockers": missing,
                "next_action": "fill missing artifacts before close",
            }

        return {
            "ok": True,
            "command": {"active_command": "improve", "subcommand": "close"},
            "next_action": "Final Evidence Gate must be re-checked before any subsequent export",
            "blockers": [],
        }

    return {"ok": False, "error": "unsupported_command"}
