from pathlib import Path

from command_export_flow import run_export_command_flow

ROOT = Path(__file__).resolve().parents[1]


def test_export_command_flow_blocks_when_pending_decision_exists(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": ["decisions/decision-stage10-export.md"],
            "final_gate_status": "PASS",
            "claims_supported": True,
        },
    )

    assert result["ok"]
    assert result["export_allowed"] is False
    assert "pending_decisions" in result["blockers"]
    assert "references/evidence-gate.md" in result["required_reads"]


def test_export_command_flow_allows_export_when_gate_is_clear(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": [],
            "final_gate_status": "PASS",
            "claims_supported": True,
            "paper_grounding_scenario": {
                "registry_claim_ids": ["c-q1-wape-baseline"],
                "derivation_targets_present": [],
                "figure_meta_present": [],
                "paper_anchors": [
                    {"kind": "claim", "target": "c-q1-wape-baseline"},
                ],
                "paper_figures": [],
            },
        },
    )

    assert result["ok"]
    assert result["export_allowed"] is True
    assert result["blockers"] == []
    assert result["paper_grounding_scan"]["status"] == "PASS"


def test_export_blocks_when_evidence_claim_review_is_missing(tmp_path):
    project_dir = tmp_path / "project"
    result = run_export_command_flow(
        "/math-modeling export",
        project_dir,
        ROOT,
        {
            "pending_decisions": [],
            "final_gate_status": "PASS",
            "claims_supported": True,
            "fixed_reviews": {"stage10": False},
        },
    )

    assert result["ok"] is False
    assert result["export_allowed"] is False
    assert result["review_required"] is True
    assert result["required_review_file"] == "reviews/stage10-evidence-claim-review.md"
