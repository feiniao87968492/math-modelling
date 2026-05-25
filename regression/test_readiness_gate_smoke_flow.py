from pathlib import Path

import yaml

from smoke_readiness_gate_flow import run_smoke_flow


def test_stage5_readiness_gate_writes_branch_tasks_and_pending_confirmation(tmp_path):
    project_dir = tmp_path / "readiness-smoke-project"

    result = run_smoke_flow(project_dir)

    assert result["ok"]
    state_path = project_dir / "modeling_state.yaml"
    assert state_path.exists()

    state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    stage5 = state["stages"]["5_solution_implementation"]
    gate = stage5["readiness_gate"]

    assert state["current_stage"] == 5
    assert stage5["status"] == "HUMAN_REVIEW_REQUIRED"
    assert stage5["quality_status"] == "BLOCKED_MISSING_REQUIRED_INPUTS"
    assert gate["status"] == "PASS_WITH_LIMITED_CLAIMS"
    assert gate["output_claim_level"] == "feasible_baseline"
    assert "global optimum" in gate["blocked_claims"]
    assert "true ROI breakpoint" in gate["blocked_claims"]

    branch_ids = {task["branch_id"] for task in gate["branch_tasks"]}
    assert "branch_stage5_relationship_data_001" in branch_ids
    assert "branch_stage5_solver_setup_001" in branch_ids

    pending = state["human_interaction"]["pending_confirmations"]
    assert len(pending) == 1
    assert pending[0]["confirmation_id"] == "confirm_stage5_readiness_gate_001"
    assert pending[0]["blocking"] is True
    assert pending[0]["status"] == "PENDING"

    assert stage5["memory_check"]["status"] == "NO_NEW_MEMORY"
