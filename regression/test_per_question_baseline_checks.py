from pathlib import Path

from run_per_question_baseline_checks import (
    check_cross_question_baseline_comparison,
    check_per_question_frontier_close,
    check_target_question_declared,
    is_multi_question,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "regression" / "baseline-per-question"


def test_per_question_fixtures_directory_is_registered():
    expected = {
        "target-question-missing.md",
        "cross-question-regression-not-flagged.md",
        "per-question-frontier-not-updated.md",
    }
    actual = {p.name for p in FIXTURES.glob("*.md")}
    missing = expected - actual
    assert not missing, f"missing fixture files: {sorted(missing)}"


def test_single_question_project_bypasses_per_question_checks():
    state = {
        "project_kind": "single_question",
        "per_question_baselines": [],
        "round_n_md": {
            "target_question_declared": False,
            "cross_question_impact_declared": False,
        },
    }
    assert is_multi_question(state) is False

    result = check_target_question_declared(state)
    assert result["ok"] is True
    assert result["blockers"] == []


def test_target_question_missing_blocks_synthesis():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": [
            "claims/baseline-q1.md",
            "claims/baseline-q2.md",
            "claims/baseline-q3.md",
        ],
        "round_n_md": {
            "target_question_declared": False,
            "cross_question_impact_declared": False,
        },
    }
    result = check_target_question_declared(state)
    assert result["ok"] is False
    assert "target_question_missing" in result["blockers"]
    assert "cross_question_impact_missing" in result["blockers"]


def test_target_question_present_passes():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": ["claims/baseline-q1.md"],
        "round_n_md": {
            "target_question_declared": True,
            "target_question": "Q1",
            "cross_question_impact_declared": True,
            "cross_question_impact_list": [],
        },
    }
    result = check_target_question_declared(state)
    assert result["ok"] is True


def test_cross_question_baseline_comparison_missing_blocks_confirm():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": [
            "claims/baseline-q1.md",
            "claims/baseline-q2.md",
            "claims/baseline-q3.md",
        ],
        "round_n_md": {
            "target_question_declared": True,
            "target_question": "Q3",
            "cross_question_impact_declared": True,
            "cross_question_impact_list": ["Q1", "Q2"],
            "risk_assessment_per_question_rows": [],
        },
        "actual_metric_movements": {},
    }
    result = check_cross_question_baseline_comparison(state)
    assert result["ok"] is False
    assert "cross_question_baseline_comparison_missing:Q1" in result["blockers"]
    assert "cross_question_baseline_comparison_missing:Q2" in result["blockers"]


def test_cross_question_actual_regression_caught():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": [
            "claims/baseline-q1.md",
            "claims/baseline-q2.md",
            "claims/baseline-q3.md",
        ],
        "round_n_md": {
            "target_question_declared": True,
            "target_question": "Q3",
            "cross_question_impact_declared": True,
            "cross_question_impact_list": ["Q1", "Q2"],
            "risk_assessment_per_question_rows": [],
        },
        "actual_metric_movements": {
            "Q1": {"baseline": 0.288, "after": 0.305, "regressed": True},
            "Q2": {"baseline": 9016061, "after": 9016061, "regressed": False},
            "Q3": {"baseline": 9893432, "after": 9700000, "regressed": False},
        },
    }
    result = check_cross_question_baseline_comparison(state)
    assert result["ok"] is False
    assert "cross_question_baseline_comparison_missing:Q1" in result["blockers"]
    assert "cross_question_baseline_comparison_missing:Q2" in result["blockers"]
    assert "cross_question_regression_unflagged:Q1" in result["blockers"]
    assert "cross_question_regression_unflagged:Q2" not in result["blockers"]


def test_cross_question_baseline_comparison_passes_when_rows_present():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": [
            "claims/baseline-q1.md",
            "claims/baseline-q2.md",
            "claims/baseline-q3.md",
        ],
        "round_n_md": {
            "target_question_declared": True,
            "target_question": "Q3",
            "cross_question_impact_declared": True,
            "cross_question_impact_list": ["Q1", "Q2"],
            "risk_assessment_per_question_rows": ["Q1", "Q2"],
        },
        "actual_metric_movements": {
            "Q1": {"baseline": 0.288, "after": 0.288, "regressed": False},
            "Q2": {"baseline": 9016061, "after": 9016061, "regressed": False},
        },
    }
    result = check_cross_question_baseline_comparison(state)
    assert result["ok"] is True


def test_per_question_frontier_not_updated_blocks_close():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": [
            "claims/baseline-q1.md",
            "claims/baseline-q2.md",
            "claims/baseline-q3.md",
        ],
        "round_n_md": {
            "target_question": "Q3",
            "cross_question_impact_list": ["Q1", "Q2"],
        },
        "per_question_frontiers_updated": [],
    }
    result = check_per_question_frontier_close(state)
    assert result["ok"] is False
    assert "per_question_frontier_not_updated:Q3" in result["blockers"]
    assert "per_question_frontier_not_updated:Q1" in result["blockers"]
    assert "per_question_frontier_not_updated:Q2" in result["blockers"]


def test_per_question_frontier_partial_update_still_blocks():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": [
            "claims/baseline-q1.md",
            "claims/baseline-q2.md",
            "claims/baseline-q3.md",
        ],
        "round_n_md": {
            "target_question": "Q3",
            "cross_question_impact_list": ["Q1", "Q2"],
        },
        "per_question_frontiers_updated": ["Q3"],
    }
    result = check_per_question_frontier_close(state)
    assert result["ok"] is False
    assert "per_question_frontier_not_updated:Q3" not in result["blockers"]
    assert "per_question_frontier_not_updated:Q1" in result["blockers"]
    assert "per_question_frontier_not_updated:Q2" in result["blockers"]


def test_per_question_frontier_full_update_passes():
    state = {
        "project_kind": "multi_question",
        "per_question_baselines": [
            "claims/baseline-q1.md",
            "claims/baseline-q2.md",
            "claims/baseline-q3.md",
        ],
        "round_n_md": {
            "target_question": "Q3",
            "cross_question_impact_list": ["Q1", "Q2"],
        },
        "per_question_frontiers_updated": ["Q1", "Q2", "Q3"],
    }
    result = check_per_question_frontier_close(state)
    assert result["ok"] is True
