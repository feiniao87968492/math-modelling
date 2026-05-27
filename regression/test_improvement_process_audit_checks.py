from pathlib import Path

from run_improvement_process_audit_checks import (
    check_required_references,
    simulate_decision_preload_coverage,
    simulate_finding_id_check,
    simulate_frontier_premature_tag_check,
)

ROOT = Path(__file__).resolve().parents[1]


def test_improvement_process_audit_references_are_registered():
    result = check_required_references(ROOT)
    assert result["ok"], result["missing"]


def test_finding_id_drift_between_critique_and_round_n_blocks_synthesis():
    result = simulate_finding_id_check(
        {
            "critique_finding_ids": ["F1", "F2", "F3", "F4", "F5", "F6", "F7"],
            "round_n_finding_ids": ["F1", "F2", "F3"],
            "frontier_finding_ids": ["F1", "F2", "F3"],
            "decision_option_target_ids": ["F2"],
        }
    )
    assert result["status"] == "PASS"

    result = simulate_finding_id_check(
        {
            "critique_finding_ids": ["F1", "F2", "F3", "F4", "F5", "F6", "F7"],
            "round_n_finding_ids": ["F1", "F2", "F3"],
            "frontier_finding_ids": ["F1", "F2", "F3"],
            "decision_option_target_ids": ["F8"],
        }
    )
    assert result["status"] == "BLOCKED"
    assert "decision_option_targets_unknown_F:F8" in result["drift"]


def test_finding_id_renumbering_caught():
    result = simulate_finding_id_check(
        {
            "critique_finding_ids": ["F1", "F2", "F3", "F4", "F5", "F6", "F7"],
            "round_n_finding_ids": ["F1", "F2_HGBT", "F3_XGBoost"],
            "frontier_finding_ids": ["F1", "F2_HGBT", "F3_XGBoost"],
            "decision_option_target_ids": [],
        }
    )
    assert result["status"] == "BLOCKED"
    assert "round_n_has_unknown_F_ids" in result["drift"]
    assert "frontier_has_unknown_F_ids" in result["drift"]


def test_decision_preload_must_cover_all_critique_blocking_risks():
    result = simulate_decision_preload_coverage(
        {
            "critique_blocking_ids": ["B1", "B2", "B3", "B4"],
            "decision_preload_blocking_ids": ["B1", "B2", "B3"],
            "critique_finding_ids": ["F1", "F2", "F3", "F4", "F5", "F6", "F7"],
            "decision_option_target_ids": ["F1", "F2", "F3"],
        }
    )
    assert result["status"] == "BLOCKED"

    blocking_gap = next(
        (gap for gap in result["gaps"] if "missing_blocking" in gap), None
    )
    assert blocking_gap is not None
    assert blocking_gap["missing_blocking"] == ["B4"]

    findings_gap = next(
        (gap for gap in result["gaps"] if "uncovered_findings" in gap), None
    )
    assert findings_gap is not None
    assert findings_gap["uncovered_findings"] == ["F4", "F5", "F6", "F7"]


def test_decision_preload_passes_when_full_coverage():
    result = simulate_decision_preload_coverage(
        {
            "critique_blocking_ids": ["B1", "B2"],
            "decision_preload_blocking_ids": ["B1", "B2"],
            "critique_finding_ids": ["F1", "F2"],
            "decision_option_target_ids": ["F1", "F2"],
        }
    )
    assert result["status"] == "PASS"
    assert result["gaps"] == []


def test_frontier_must_not_cite_skepticism_before_review_exists():
    result = simulate_frontier_premature_tag_check(
        {
            "skepticism_review_present": False,
            "frontier_entries": [
                {
                    "id": "F2_HGBT",
                    "annotation": "blocked by Skepticism B2 -> must rollback first",
                }
            ],
        }
    )
    assert result["status"] == "BLOCKED"
    assert len(result["violations"]) == 1
    assert "Skepticism" in result["violations"][0]["annotation"]


def test_frontier_passes_when_skepticism_review_exists():
    result = simulate_frontier_premature_tag_check(
        {
            "skepticism_review_present": True,
            "frontier_entries": [
                {
                    "id": "F2_HGBT",
                    "annotation": "blocked by Skepticism B2 (see reviews/improvement-round-1-skepticism.md)",
                }
            ],
        }
    )
    assert result["status"] == "PASS"


def test_frontier_passes_with_neutral_pending_placeholder():
    result = simulate_frontier_premature_tag_check(
        {
            "skepticism_review_present": False,
            "frontier_entries": [
                {
                    "id": "F2_HGBT",
                    "annotation": "pending Skepticism review",
                }
            ],
        }
    )
    assert result["status"] == "PASS"
    assert result["violations"] == []
