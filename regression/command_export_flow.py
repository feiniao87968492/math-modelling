from pathlib import Path

from run_gate_and_rollback_checks import simulate_export_gate

EXPORT_REQUIRED_READS = [
    "references/protocol-markdown-audit.md",
    "references/protocol-human-confirmation.md",
    "references/protocol-readiness-gate.md",
    "references/protocol-rollback.md",
    "references/protocol-subagent-delegation.md",
    "references/evidence-gate.md",
    "references/stage-10-paper-materials.md",
]


def run_export_command_flow(
    command_text: str, project_dir: Path, skill_root: Path, scenario: dict
) -> dict:
    if command_text != "/math-modeling export":
        return {"ok": False, "error": "unsupported_command"}

    missing = [path for path in EXPORT_REQUIRED_READS if not (skill_root / path).exists()]
    if missing:
        return {"ok": False, "error": "missing_required_reads", "missing_required_reads": missing}

    gate = simulate_export_gate(scenario)
    project_dir.mkdir(parents=True, exist_ok=True)

    fixed_reviews = scenario.get("fixed_reviews", {})
    stage10_review_present = fixed_reviews.get("stage10", True)
    if not stage10_review_present:
        return {
            "ok": False,
            "command": {"active_command": "export"},
            "required_reads": EXPORT_REQUIRED_READS,
            "review_policy": {
                "main_agent_role": "final export readiness synthesis",
                "fixed_reviewers": ["Evidence/Claim Reviewer"],
                "risk_triggered_reviewers": ["Evidence-Gate Reviewer", "Figure-Review Reviewer"],
            },
            "review_required": True,
            "required_review_file": "reviews/stage10-evidence-claim-review.md",
            "required_reviewer": "Evidence/Claim Reviewer",
            "blockers": ["missing mandatory fixed-review artifact"],
            "gate_path": "gates/final-evidence-gate.md",
            "export_allowed": False,
        }

    return {
        "ok": True,
        "command": {"active_command": "export"},
        "required_reads": EXPORT_REQUIRED_READS,
        "review_policy": {
            "main_agent_role": "final export readiness synthesis",
            "fixed_reviewers": ["Evidence/Claim Reviewer"],
            "risk_triggered_reviewers": ["Evidence-Gate Reviewer", "Figure-Review Reviewer"],
        },
        "blockers": gate["blockers"],
        "gate_path": "gates/final-evidence-gate.md",
        "export_allowed": gate["status"] != "BLOCKED",
    }
