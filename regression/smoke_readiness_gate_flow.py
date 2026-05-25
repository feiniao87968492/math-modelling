from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from run_readiness_gate_checks import simulate_readiness_gate


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _initial_state():
    return {
        "current_stage": None,
        "updated_at": "",
        "stages": {
            "5_solution_implementation": {
                "status": "NOT_STARTED",
                "user_confirmation_status": "NOT_REQUIRED",
                "quality_status": "",
                "outputs": [],
                "memory_check": {
                    "status": "UNKNOWN",
                    "summary": "",
                    "recorded_at": "",
                },
            }
        },
        "human_interaction": {
            "pending_confirmations": [],
            "confirmed_decisions": [],
        },
    }


def _merge_gate_findings(*gates):
    merged = {
        "status": "PASS_WITH_LIMITED_CLAIMS",
        "output_claim_level": "feasible_baseline",
        "missing_requirements": [],
        "branch_tasks": [],
        "allowed_outputs": [],
        "blocked_claims": [],
    }
    for gate in gates:
        merged["missing_requirements"].extend(gate["missing_requirements"])
        merged["branch_tasks"].extend(gate["branch_tasks"])
        merged["allowed_outputs"].extend(gate["allowed_outputs"])
        merged["blocked_claims"].extend(gate["blocked_claims"])
    merged["allowed_outputs"] = list(dict.fromkeys(merged["allowed_outputs"] + ["feasible baseline solution"]))
    merged["blocked_claims"] = list(dict.fromkeys(merged["blocked_claims"] + ["true ROI breakpoint"]))
    return merged


def _pending_confirmation(gate):
    return {
        "confirmation_id": "confirm_stage5_readiness_gate_001",
        "stage": 5,
        "decision_type": "readiness_gate_branch_confirmation",
        "blocking": True,
        "question": "Stage 5 缺少支撑强结论的结构化关系数据或精确求解器，是否先完成支线任务？",
        "options_presented": [
            "A. 先完成缺失数据/求解器支线任务",
            "B. 接受 feasible_baseline 限制并继续",
            "C. 暂停 Stage 5",
        ],
        "recommended_option": "A",
        "impact_scope": [
            "stages.5_solution_implementation.readiness_gate",
            "human_interaction.pending_confirmations",
        ],
        "affected_outputs": [task["outputs"][0] for task in gate["branch_tasks"]],
        "status": "PENDING",
    }


def run_smoke_flow(project_dir: Path) -> dict:
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "memory.md").write_text("# Modeling Memory\n\n- no project-specific rule yet\n", encoding="utf-8")

    state = _initial_state()
    now = _now_iso()
    state["current_stage"] = 5
    stage5 = state["stages"]["5_solution_implementation"]
    stage5["status"] = "IN_PROGRESS"
    state["updated_at"] = now

    relationship_gate = simulate_readiness_gate(
        {
            "stage": 5,
            "requires_relationship_data": True,
            "has_structured_relationship_data": False,
            "confirmed_claim_level": "validated_optimum",
        }
    )
    solver_gate = simulate_readiness_gate(
        {
            "stage": 5,
            "confirmed_solver_class": "MILP",
            "solver_available": False,
            "fallback_solver_class": "greedy",
            "confirmed_claim_level": "global_optimum",
        }
    )
    roi_gate = simulate_readiness_gate(
        {
            "stage": 7,
            "requires_roi_breakpoint": True,
            "has_reoptimized_parameter_sweep": False,
        }
    )
    gate = _merge_gate_findings(relationship_gate, solver_gate, roi_gate)

    stage5["outputs"] = ["memory.md"]
    stage5["quality_status"] = "BLOCKED_MISSING_REQUIRED_INPUTS"
    stage5["memory_check"] = {
        "status": "NO_NEW_MEMORY",
        "summary": "no new memory",
        "recorded_at": _now_iso(),
    }
    stage5["readiness_gate"] = gate
    state["human_interaction"]["pending_confirmations"].append(_pending_confirmation(gate))
    stage5["status"] = "HUMAN_REVIEW_REQUIRED"
    stage5["user_confirmation_status"] = "PENDING"
    state["updated_at"] = _now_iso()

    state_path = project_dir / "modeling_state.yaml"
    state_path.write_text(yaml.safe_dump(state, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {"ok": True, "state_path": str(state_path), "readiness_gate": gate}


def main() -> int:
    with TemporaryDirectory(prefix="readiness-gate-smoke-") as temp_dir:
        result = run_smoke_flow(Path(temp_dir) / "project")
        print(result["state_path"])
    print("PASS readiness gate smoke flow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
