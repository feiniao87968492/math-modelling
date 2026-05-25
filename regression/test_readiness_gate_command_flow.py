from pathlib import Path

import yaml

from command_readiness_gate_flow import run_command_flow

ROOT = Path(__file__).resolve().parents[1]


def test_stage5_command_flow_loads_protocols_delegates_and_writes_gate(tmp_path):
    project_dir = tmp_path / "command-flow-project"

    result = run_command_flow("/math-modeling stage 5", project_dir, ROOT)

    assert result["ok"]
    assert result["command"]["stage"] == 5
    assert result["command"]["active_command"] == "stage"
    assert result["delegation"]["owning_subagent"] == "Model-Building Subagent"
    assert "references/protocol-readiness-gate.md" in result["required_reads"]
    assert "references/stage-5-solution-implementation.md" in result["required_reads"]
    assert "references/subagent-model-building.md" in result["required_reads"]

    state = yaml.safe_load((project_dir / "modeling_state.yaml").read_text(encoding="utf-8"))
    stage5 = state["stages"]["5_solution_implementation"]

    assert state["current_stage"] == 5
    assert stage5["status"] == "HUMAN_REVIEW_REQUIRED"
    assert stage5["user_confirmation_status"] == "PENDING"
    assert stage5["readiness_gate"]["output_claim_level"] == "feasible_baseline"
    assert "global optimum" in stage5["readiness_gate"]["blocked_claims"]
    assert state["human_interaction"]["pending_confirmations"][0]["decision_type"] == "readiness_gate_branch_confirmation"


def test_stage5_command_flow_fails_if_required_reference_is_missing(tmp_path):
    project_dir = tmp_path / "command-flow-project"

    result = run_command_flow(
        "/math-modeling stage 5",
        project_dir,
        ROOT,
        required_read_overrides=["references/missing-readiness-gate.md"],
    )

    assert not result["ok"]
    assert result["error"] == "missing_required_reads"
    assert "references/missing-readiness-gate.md" in result["missing_required_reads"]
