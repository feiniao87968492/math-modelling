from pathlib import Path

from run_gate_and_rollback_checks import simulate_rollback_decision

ROLLBACK_REQUIRED_READS = [
    "references/protocol-markdown-audit.md",
    "references/protocol-memory-update.md",
    "references/protocol-subagent-delegation.md",
    "references/protocol-rollback.md",
    "references/stage-8-visualization.md",
    "references/stage-9-figure-review.md",
    "references/subagent-validation-paper.md",
]


def run_rollback_command_flow(
    command_text: str, project_dir: Path, skill_root: Path, scenario: dict
) -> dict:
    if command_text != "/math-modeling review":
        return {"ok": False, "error": "unsupported_command"}

    missing = [path for path in ROLLBACK_REQUIRED_READS if not (skill_root / path).exists()]
    if missing:
        return {"ok": False, "error": "missing_required_reads", "missing_required_reads": missing}

    rollback = simulate_rollback_decision(scenario)
    project_dir.mkdir(parents=True, exist_ok=True)

    return {
        "ok": True,
        "command": {"active_command": "review"},
        "required_reads": ROLLBACK_REQUIRED_READS,
        "review_policy": {
            "main_agent_role": "late-stage review synthesis and rollback handling",
            "fixed_reviewers": ["Validation Reviewer"],
            "risk_triggered_reviewers": ["Figure-Review Reviewer", "Evidence-Gate Reviewer"],
        },
        "rollback_required": rollback["status"] == "ROLLBACK_REQUIRED",
        "rollback_path": rollback["rollback_path"],
        "requires_user_confirmation": rollback["requires_user_confirmation"],
    }
