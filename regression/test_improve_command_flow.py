from pathlib import Path

from command_improve_flow import run_improve_command_flow

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "regression" / "improve-flow-fixtures"


def test_improve_flow_fixtures_directory_is_registered():
    expected = {
        "precondition-baseline-missing.md",
        "precondition-stage7-missing.md",
        "precondition-pending-decision.md",
        "precondition-round-in-progress.md",
        "reviewer-order-skepticism-before-critique.md",
        "round-section-order-synthesized-before-skepticism.md",
        "round-close-frontier-not-updated.md",
        "happy-path-single-round.md",
    }
    actual = {p.name for p in FIXTURES.glob("*.md")}
    missing = expected - actual
    assert not missing, f"missing fixture files: {sorted(missing)}"


def test_improve_blocks_when_baseline_snapshot_missing():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": False,
        "stage7_sensitivity_present": True,
        "pending_decisions": [],
        "in_progress_round": False,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is False
    assert "baseline_snapshot_missing" in result["blockers"]


def test_improve_blocks_when_stage7_sensitivity_missing():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": False,
        "pending_decisions": [],
        "in_progress_round": False,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is False
    assert "stage7_sensitivity_missing" in result["blockers"]


def test_improve_blocks_when_pending_decision_present():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": True,
        "pending_decisions": ["decisions/decision-stage10-export.md"],
        "in_progress_round": False,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is False
    assert "pending_decision_present" in result["blockers"]


def test_improve_blocks_when_round_in_progress():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": True,
        "pending_decisions": [],
        "in_progress_round": True,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is False
    assert "in_progress_round_present" in result["blockers"]


def test_improve_emits_critique_template_first():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": True,
        "pending_decisions": [],
        "in_progress_round": False,
        "critique_review_present": False,
        "skepticism_review_present": False,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is True
    assert "Improvement-Critique Reviewer" in result["next_action"]
    assert result["expected_output_path"] == "reviews/improvement-round-N-critique.md"


def test_improve_emits_skepticism_template_only_after_critique():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": True,
        "pending_decisions": [],
        "in_progress_round": False,
        "critique_review_present": True,
        "skepticism_review_present": False,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is True
    assert "Improvement-Skepticism Reviewer" in result["next_action"]
    assert result["expected_output_path"] == "reviews/improvement-round-N-skepticism.md"
    assert "reviews/improvement-round-N-critique.md" in result["required_skepticism_reads"]


def test_improve_blocks_when_back_sections_written_before_confirm():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": True,
        "pending_decisions": [],
        "in_progress_round": False,
        "critique_review_present": True,
        "skepticism_review_present": True,
        "round_n_md": {
            "front_six_sections_present": True,
            "back_three_sections_present": True,
        },
        "decision_confirmed": False,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is False
    assert "round_n_back_sections_written_before_confirm" in result["blockers"]


def test_improve_waits_for_user_confirmation_after_synthesis():
    state = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": True,
        "pending_decisions": [],
        "in_progress_round": False,
        "critique_review_present": True,
        "skepticism_review_present": True,
        "round_n_md": {
            "front_six_sections_present": True,
            "back_three_sections_present": False,
        },
        "decision_confirmed": False,
    }
    result = run_improve_command_flow("/math-modeling improve", state)
    assert result["ok"] is True
    assert "awaiting_user_confirmation" in result["blockers"]


def test_improve_close_blocks_when_frontier_not_updated():
    state = {
        "decision_confirmed": True,
        "round_n_md": {
            "implementation_summary_filled": True,
            "before_vs_after_metrics_filled": True,
            "frontier_update_filled": True,
        },
        "improvement_log_updated": True,
        "improvement_frontier_updated": False,
        "stage6_validation_rerun": False,
    }
    result = run_improve_command_flow("/math-modeling improve close", state)
    assert result["ok"] is False
    assert "improvement_frontier_not_updated" in result["blockers"]
    assert "stage6_validation_not_rerun" in result["blockers"]


def test_improve_close_blocks_when_round_not_confirmed():
    state = {"decision_confirmed": False}
    result = run_improve_command_flow("/math-modeling improve close", state)
    assert result["ok"] is False
    assert "round_not_confirmed" in result["blockers"]


def test_improve_happy_path_walks_through_all_checkpoints():
    base = {
        "stage6_review_pass": True,
        "baseline_snapshot_frozen": True,
        "stage7_sensitivity_present": True,
        "pending_decisions": [],
        "in_progress_round": False,
    }

    a = run_improve_command_flow(
        "/math-modeling improve",
        {**base, "critique_review_present": False, "skepticism_review_present": False},
    )
    assert a["ok"] is True and "Improvement-Critique Reviewer" in a["next_action"]

    b = run_improve_command_flow(
        "/math-modeling improve",
        {**base, "critique_review_present": True, "skepticism_review_present": False},
    )
    assert b["ok"] is True and "Improvement-Skepticism Reviewer" in b["next_action"]

    c = run_improve_command_flow(
        "/math-modeling improve",
        {**base, "critique_review_present": True, "skepticism_review_present": True},
    )
    assert c["ok"] is True and "synthesize" in c["next_action"]

    d = run_improve_command_flow(
        "/math-modeling improve",
        {
            **base,
            "critique_review_present": True,
            "skepticism_review_present": True,
            "round_n_md": {
                "front_six_sections_present": True,
                "back_three_sections_present": False,
            },
            "decision_confirmed": False,
        },
    )
    assert d["ok"] is True and "awaiting_user_confirmation" in d["blockers"]

    e = run_improve_command_flow(
        "/math-modeling improve",
        {
            **base,
            "critique_review_present": True,
            "skepticism_review_present": True,
            "round_n_md": {
                "front_six_sections_present": True,
                "back_three_sections_present": False,
            },
            "decision_confirmed": True,
        },
    )
    assert e["ok"] is True and "route confirmed change" in e["next_action"]

    f = run_improve_command_flow(
        "/math-modeling improve close",
        {
            "decision_confirmed": True,
            "round_n_md": {
                "implementation_summary_filled": True,
                "before_vs_after_metrics_filled": True,
                "frontier_update_filled": True,
            },
            "improvement_log_updated": True,
            "improvement_frontier_updated": True,
            "stage6_validation_rerun": True,
        },
    )
    assert f["ok"] is True
    assert "Final Evidence Gate" in f["next_action"]


def test_improve_status_subcommand_is_recognized():
    result = run_improve_command_flow("/math-modeling improve status", {})
    assert result["ok"] is True
    assert result["frontier_path"] == "improvements/improvement-frontier.md"
    assert result["log_path"] == "improvements/improvement-log.md"
