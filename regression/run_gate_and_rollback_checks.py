from __future__ import annotations

from pathlib import Path

REQUIRED_REFERENCES = {
    "regression/rollback-late-stage-structural-defect.md": [
        "ROLLBACK_REQUIRED",
        "rollbacks/rollback-stage8-structural-defect.md",
    ],
    "regression/export-blocked-by-pending-decision.md": [
        "BLOCKED",
        "decisions/decision-stage10-export.md",
    ],
    "regression/final-evidence-gate-grounded-claims-only.md": [
        "PASS_WITH_WARNINGS",
        "BLOCKED",
        "unsupported_claims",
    ],
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


def simulate_rollback_decision(scenario: dict) -> dict:
    if scenario.get("defect_severity") == "structural_revision":
        return {
            "status": "ROLLBACK_REQUIRED",
            "rollback_path": "rollbacks/rollback-stage8-structural-defect.md",
            "requires_user_confirmation": True,
        }
    return {
        "status": "NO_ROLLBACK",
        "rollback_path": None,
        "requires_user_confirmation": False,
    }


def simulate_export_gate(scenario: dict) -> dict:
    blockers = []
    if scenario.get("pending_decisions"):
        blockers.append("pending_decisions")
    if scenario.get("final_gate_status") == "BLOCKED":
        blockers.append("final_gate_blocked")
    if not scenario.get("claims_supported", False):
        blockers.append("unsupported_claims")
    return {"status": "BLOCKED" if blockers else "READY", "blockers": blockers}


def simulate_final_evidence_gate(scenario: dict) -> dict:
    blockers = []
    if scenario.get("pending_decisions"):
        blockers.append("pending_decisions")
    if not scenario.get("claims_supported", False):
        blockers.append("unsupported_claims")
    if not scenario.get("reviews_complete", False):
        blockers.append("reviews_incomplete")
    if not scenario.get("gate_checks_complete", False):
        blockers.append("gate_checks_incomplete")
    if blockers:
        return {"status": "BLOCKED", "blockers": blockers}
    return {"status": "PASS", "blockers": []}
