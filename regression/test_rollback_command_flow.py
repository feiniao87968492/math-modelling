from pathlib import Path

from command_rollback_flow import run_rollback_command_flow

ROOT = Path(__file__).resolve().parents[1]


def test_rollback_command_flow_requires_rollback_for_structural_defect(tmp_path):
    project_dir = tmp_path / "project"
    result = run_rollback_command_flow(
        "/math-modeling review",
        project_dir,
        ROOT,
        {
            "stage": 8,
            "defect_severity": "structural_revision",
            "downstream_patch_possible": True,
        },
    )

    assert result["ok"]
    assert result["rollback_required"] is True
    assert result["rollback_path"] == "rollbacks/rollback-stage8-structural-defect.md"
    assert result["requires_user_confirmation"] is True
    assert "references/protocol-rollback.md" in result["required_reads"]


def test_rollback_command_flow_returns_no_rollback_when_no_structural_defect(tmp_path):
    project_dir = tmp_path / "project"
    result = run_rollback_command_flow(
        "/math-modeling review",
        project_dir,
        ROOT,
        {
            "stage": 8,
            "defect_severity": "minor_revision",
            "downstream_patch_possible": True,
        },
    )

    assert result["ok"]
    assert result["rollback_required"] is False
    assert result["rollback_path"] is None
    assert result["requires_user_confirmation"] is False
