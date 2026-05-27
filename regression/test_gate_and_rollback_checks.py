from pathlib import Path

from run_gate_and_rollback_checks import (
    check_required_references,
    simulate_export_gate,
    simulate_final_evidence_gate,
    simulate_rollback_decision,
)

ROOT = Path(__file__).resolve().parents[1]


def test_gate_and_rollback_references_are_registered():
    result = check_required_references(ROOT)
    assert result["ok"], result["missing"]


def test_late_stage_structural_defect_requires_rollback():
    result = simulate_rollback_decision(
        {
            "stage": 8,
            "defect_severity": "structural_revision",
            "downstream_patch_possible": True,
        }
    )
    assert result["status"] == "ROLLBACK_REQUIRED"
    assert result["rollback_path"] == "rollbacks/rollback-stage8-structural-defect.md"
    assert result["requires_user_confirmation"] is True


def test_export_is_blocked_by_pending_decision():
    result = simulate_export_gate(
        {
            "pending_decisions": ["decisions/decision-stage10-export.md"],
            "final_gate_status": "PASS",
            "claims_supported": True,
        }
    )
    assert result["status"] == "BLOCKED"
    assert "pending_decisions" in result["blockers"]


def test_final_evidence_gate_requires_grounded_claims():
    result = simulate_final_evidence_gate(
        {
            "pending_decisions": [],
            "claims_supported": False,
            "reviews_complete": True,
            "gate_checks_complete": True,
        }
    )
    assert result["status"] == "BLOCKED"
    assert "unsupported_claims" in result["blockers"]
