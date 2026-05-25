from __future__ import annotations

from pathlib import Path

REQUIRED_REFERENCES = {
    "README.md": ["protocol-readiness-gate.md", "Readiness Gate"],
    "SKILL.md": ["protocol-readiness-gate.md", "readiness gate"],
    "references/protocol-subagent-delegation.md": ["readiness_gate"],
    "references/subagent-model-building.md": ["readiness_gate"],
    "references/subagent-validation-paper.md": ["readiness_gate"],
    "references/stage-4-model-spec.md": ["protocol-readiness-gate.md", "Readiness Gate"],
    "references/stage-5-solution-implementation.md": ["protocol-readiness-gate.md", "Readiness Gate"],
    "references/stage-6-independent-validation.md": ["protocol-readiness-gate.md", "Readiness Gate"],
    "references/stage-7-sensitivity-analysis.md": ["protocol-readiness-gate.md", "Readiness Gate"],
    "references/stage-10-paper-materials.md": ["protocol-readiness-gate.md", "Readiness Gate"],
    "regression/readiness-gate-missing-adjacency-data.md": ["branch_stage5_relationship_data_001"],
    "regression/readiness-gate-missing-milp-solver.md": ["branch_stage5_solver_setup_001"],
    "regression/readiness-gate-feasible-baseline-claim-limit.md": ["feasible_baseline"],
}


def check_required_references(root: Path) -> dict:
    missing = []
    checked_files = []
    for relative_path, needles in REQUIRED_REFERENCES.items():
        path = root / relative_path
        checked_files.append(relative_path)
        if not path.exists():
            missing.append({"file": relative_path, "missing": "file"})
            continue
        content = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in content:
                missing.append({"file": relative_path, "missing": needle})
    return {"ok": not missing, "missing": missing, "checked_files": checked_files}


def _limited_gate():
    return {
        "status": "PASS_WITH_LIMITED_CLAIMS",
        "output_claim_level": "feasible_baseline",
        "missing_requirements": [],
        "branch_tasks": [],
        "allowed_outputs": [],
        "blocked_claims": [],
    }


def simulate_readiness_gate(scenario: dict) -> dict:
    gate = _limited_gate()

    if scenario.get("requires_relationship_data") and not scenario.get("has_structured_relationship_data"):
        gate["missing_requirements"].append(
            {
                "requirement_id": "structured_relationship_data",
                "type": "structured_relationship_data",
                "required_for": ["adjacency benefit", "network relationship claim"],
            }
        )
        gate["branch_tasks"].append(
            {
                "branch_id": "branch_stage5_relationship_data_001",
                "status": "PENDING_USER_INPUT",
                "outputs": ["data/processed/relationship_edges_template.csv"],
            }
        )
        gate["blocked_claims"].extend(
            ["adjacency/network benefit", "validated optimal plan using relationship benefits"]
        )

    exact_solver_requested = scenario.get("confirmed_solver_class") in {"MILP", "IP", "CP-SAT", "exact"}
    if exact_solver_requested and not scenario.get("solver_available"):
        gate["missing_requirements"].append(
            {
                "requirement_id": "confirmed_exact_solver",
                "type": "solver_available",
                "required_for": ["global optimum claim", "validated optimum claim"],
            }
        )
        gate["branch_tasks"].append(
            {
                "branch_id": "branch_stage5_solver_setup_001",
                "status": "PENDING_TOOLING",
                "outputs": ["data/results/solver_availability_report.md"],
            }
        )
        gate["allowed_outputs"].extend(["feasible baseline solution", "solver setup report"])
        gate["blocked_claims"].extend(["global optimum", "validated optimal solution"])

    baseline_output = scenario.get("stage5_output_kind") in {"greedy_baseline", "heuristic", "single_scenario"}
    limited_validation = set(scenario.get("validation_scope", [])) <= {"hard_constraints", "budget", "uniqueness", "metric_reproduction"}
    if baseline_output and limited_validation:
        gate["missing_requirements"].append(
            {
                "requirement_id": "optimality_evidence",
                "type": "evidence",
                "required_for": ["global optimum claim"],
            }
        )
        gate["allowed_outputs"].extend(["feasibility validation", "baseline comparison", "limited sensitivity warning"])
        gate["blocked_claims"].extend(["global optimum", "validated optimum"])

    if scenario.get("requires_roi_breakpoint") and not scenario.get("has_reoptimized_parameter_sweep"):
        gate["missing_requirements"].append(
            {
                "requirement_id": "reoptimized_parameter_sweep",
                "type": "evidence",
                "required_for": ["true ROI breakpoint"],
            }
        )
        gate["blocked_claims"].append("true ROI breakpoint")

    gate["blocked_claims"] = list(dict.fromkeys(gate["blocked_claims"]))
    gate["allowed_outputs"] = list(dict.fromkeys(gate["allowed_outputs"]))
    return gate


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = check_required_references(root)
    if not result["ok"]:
        for item in result["missing"]:
            print(f"MISSING {item['file']}: {item['missing']}")
        return 1

    scenarios = [
        {
            "stage": 5,
            "requires_relationship_data": True,
            "has_structured_relationship_data": False,
        },
        {
            "stage": 5,
            "confirmed_solver_class": "MILP",
            "solver_available": False,
            "fallback_solver_class": "greedy",
        },
        {
            "stage": 6,
            "stage5_output_kind": "greedy_baseline",
            "validation_scope": ["hard_constraints", "budget", "uniqueness"],
            "requires_roi_breakpoint": True,
            "has_reoptimized_parameter_sweep": False,
        },
    ]
    gates = [simulate_readiness_gate(scenario) for scenario in scenarios]
    if not all(gate["branch_tasks"] or gate["blocked_claims"] for gate in gates):
        print("FAILED readiness gate branch simulation")
        return 1

    print("PASS readiness gate regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
