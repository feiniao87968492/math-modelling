from pathlib import Path

from run_time_budget_checks import (
    check_export,
    check_improve_open,
    check_stage_switch,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "regression" / "time-budget"


def test_time_budget_protocol_doc_is_registered():
    proto = ROOT / "references" / "protocol-time-budget.md"
    assert proto.exists()
    content = proto.read_text(encoding="utf-8")
    assert "## Required `time-budget.md` Sections" in content
    assert "## Time-Pressure Advisory" in content
    assert "## Hard Deadline Enforcement" in content
    assert "/math-modeling time" in content
    assert "20%" in content


def test_time_budget_fixtures_directory_is_registered():
    expected = {
        "stage-switch-without-time-update.md",
        "improve-with-low-remaining-budget.md",
        "export-past-hard-deadline.md",
        "time-budget-absent-no-error.md",
    }
    actual = {p.name for p in FIXTURES.glob("*.md")}
    missing = expected - actual
    assert not missing, f"missing fixture files: {sorted(missing)}"


def test_time_budget_absent_preserves_v41_behavior_for_stage():
    state = {"time_budget_present": False}
    result = check_stage_switch(state)
    assert result["ok"] is True
    assert result["blockers"] == []
    assert result["applied"] is False


def test_time_budget_absent_preserves_v41_behavior_for_improve():
    state = {"time_budget_present": False}
    result = check_improve_open(state)
    assert result["ok"] is True
    assert result["applied"] is False


def test_time_budget_absent_preserves_v41_behavior_for_export():
    state = {"time_budget_present": False}
    result = check_export(state)
    assert result["ok"] is True
    assert result["applied"] is False


def test_stage_switch_blocks_when_previous_stage_not_stopped():
    state = {
        "time_budget_present": True,
        "current_stage": 4,
        "current_stage_status": "in_progress",
        "stop_event_recorded_for_current_stage": False,
        "remaining_hours": 60,
        "total_hours": 72,
        "advisory_threshold_pct": 20,
        "hard_deadline_passed": False,
    }
    result = check_stage_switch(state)
    assert result["ok"] is False
    assert "previous_stage_not_stopped" in result["blockers"]
    assert "/math-modeling time stop N" in result["next_action"]


def test_stage_switch_passes_when_previous_stage_stopped():
    state = {
        "time_budget_present": True,
        "current_stage": 4,
        "current_stage_status": "done",
        "stop_event_recorded_for_current_stage": True,
        "remaining_hours": 60,
        "total_hours": 72,
        "advisory_threshold_pct": 20,
        "hard_deadline_passed": False,
    }
    result = check_stage_switch(state)
    assert result["ok"] is True
    assert result["applied"] is True


def test_improve_emits_time_pressure_advisory_when_under_threshold():
    state = {
        "time_budget_present": True,
        "current_stage": 7,
        "remaining_hours": 12,
        "total_hours": 72,
        "advisory_threshold_pct": 20,
        "hard_deadline_passed": False,
        "advisory_already_confirmed_this_stage": False,
        "top_remaining_stages": ["10", "5", "8"],
    }
    result = check_improve_open(state)
    assert result["ok"] is False
    assert "time_pressure_advisory_required" in result["blockers"]
    assert result["advisory"]["remaining_hours"] == 12
    assert result["advisory"]["remaining_pct"] == 16.7
    assert "lower_target_claim_level" in result["advisory"]["user_actions"]


def test_improve_does_not_retrigger_advisory_after_confirmation():
    state = {
        "time_budget_present": True,
        "current_stage": 7,
        "remaining_hours": 12,
        "total_hours": 72,
        "advisory_threshold_pct": 20,
        "hard_deadline_passed": False,
        "advisory_already_confirmed_this_stage": True,
    }
    result = check_improve_open(state)
    assert result["ok"] is True
    assert result["blockers"] == []
    assert "advisory" not in result


def test_improve_does_not_emit_advisory_when_above_threshold():
    state = {
        "time_budget_present": True,
        "current_stage": 7,
        "remaining_hours": 30,
        "total_hours": 72,
        "advisory_threshold_pct": 20,
        "hard_deadline_passed": False,
        "advisory_already_confirmed_this_stage": False,
    }
    result = check_improve_open(state)
    assert result["ok"] is True
    assert "advisory" not in result


def test_export_blocks_when_hard_deadline_passed():
    state = {
        "time_budget_present": True,
        "current_stage": 10,
        "current_stage_status": "in_progress",
        "remaining_hours": 0,
        "total_hours": 72,
        "advisory_threshold_pct": 20,
        "hard_deadline_passed": True,
    }
    result = check_export(state)
    assert result["ok"] is False
    assert "hard_deadline_passed" in result["blockers"]
    assert "explicitly extend" in result["next_action"]


def test_export_passes_when_deadline_intact_and_budget_remaining():
    state = {
        "time_budget_present": True,
        "current_stage": 10,
        "remaining_hours": 5,
        "total_hours": 72,
        "advisory_threshold_pct": 20,
        "hard_deadline_passed": False,
        "advisory_already_confirmed_this_stage": True,
    }
    result = check_export(state)
    assert result["ok"] is True


def test_skill_md_contains_time_command_and_rule_22():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "/math-modeling time" in skill
    assert "/math-modeling time start N" in skill
    assert "/math-modeling time stop N" in skill
    # rule 22 wording
    assert "time-budget.md" in skill
    assert "时 dispatcher 在每次 stage 切换" in skill or "stage 切换" in skill


def test_all_stage_docs_mention_time_budget():
    for n in range(1, 11):
        stage_glob = list(
            (ROOT / "references").glob(f"stage-{n}-*.md")
        )
        assert len(stage_glob) == 1, f"stage-{n} doc not unique"
        content = stage_glob[0].read_text(encoding="utf-8")
        assert "## Time budget" in content, f"stage-{n} missing Time budget section"
        assert "time-budget.md" in content, f"stage-{n} does not reference time-budget.md"
