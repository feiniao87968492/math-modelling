from pathlib import Path

from run_readiness_gate_checks import (
    check_required_references,
    simulate_readiness_gate,
)

ROOT = Path(__file__).resolve().parents[1]


def test_required_references_are_registered():
    result = check_required_references(ROOT)

    assert result["ok"], result["missing"]
    assert "README.md" in result["checked_files"]
    assert "SKILL.md" in result["checked_files"]


def test_missing_adjacency_data_creates_branch_and_blocks_network_claims():
    gate = simulate_readiness_gate(
        {
            "stage": 5,
            "requires_relationship_data": True,
            "has_structured_relationship_data": False,
            "confirmed_claim_level": "validated_optimum",
        }
    )

    assert gate["status"] == "PASS_WITH_LIMITED_CLAIMS"
    assert gate["supported_claim_level"] == "feasible_baseline"
    assert gate["required_branches"][0]["path"] == "branches/branch-stage5-relationship-data.md"
    assert "adjacency/network benefit" in gate["blocked_claims"]


def test_missing_milp_solver_creates_tooling_branch_and_blocks_global_claims():
    gate = simulate_readiness_gate(
        {
            "stage": 5,
            "confirmed_solver_class": "MILP",
            "solver_available": False,
            "fallback_solver_class": "greedy",
            "confirmed_claim_level": "global_optimum",
        }
    )

    assert gate["status"] == "PASS_WITH_LIMITED_CLAIMS"
    assert gate["required_branches"][0]["path"] == "branches/branch-stage5-solver-setup.md"
    assert "global optimum" in gate["blocked_claims"]
    assert "validated optimal solution" in gate["blocked_claims"]


def test_feasible_baseline_validation_limits_claims():
    gate = simulate_readiness_gate(
        {
            "stage": 6,
            "stage5_output_kind": "greedy_baseline",
            "validation_scope": ["hard_constraints", "budget", "uniqueness"],
            "requires_roi_breakpoint": True,
            "has_reoptimized_parameter_sweep": False,
        }
    )

    assert gate["status"] == "PASS_WITH_LIMITED_CLAIMS"
    assert gate["supported_claim_level"] == "feasible_baseline"
    assert "true ROI breakpoint" in gate["blocked_claims"]
    assert "feasibility validation" in gate["allowed_outputs"]
