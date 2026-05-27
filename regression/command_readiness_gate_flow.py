from pathlib import Path

from smoke_readiness_gate_flow import run_smoke_flow

STAGE_CONFIG = {
    4: {
        "required_reads": [
            "references/protocol-markdown-audit.md",
            "references/protocol-human-confirmation.md",
            "references/protocol-memory-update.md",
            "references/protocol-subagent-delegation.md",
            "references/protocol-readiness-gate.md",
            "references/subagent-model-building.md",
            "references/stage-4-model-spec.md",
        ],
        "required_review_file": "reviews/stage4-algorithm-model-review.md",
        "required_reviewer": "Algorithm/Model Reviewer",
        "risk_triggered_reviewers": ["Data-Audit Reviewer", "Literature/Method Reviewer"],
        "gate_path": "gates/stage4-model-readiness-gate.md",
    },
    5: {
        "required_reads": [
            "references/protocol-markdown-audit.md",
            "references/protocol-human-confirmation.md",
            "references/protocol-memory-update.md",
            "references/protocol-subagent-delegation.md",
            "references/protocol-readiness-gate.md",
            "references/protocol-rollback.md",
            "references/subagent-model-building.md",
            "references/subagent-specialists.md",
            "references/protocol-fallback-and-deviation.md",
            "references/stage-5-solution-implementation.md",
        ],
        "required_review_file": "reviews/stage5-implementation-readiness-review.md",
        "required_reviewer": "Implementation Readiness Reviewer",
        "risk_triggered_reviewers": ["Data-Audit Reviewer", "Code-Review Reviewer"],
        "gate_path": "gates/stage5-readiness-gate.md",
    },
    6: {
        "required_reads": [
            "references/protocol-markdown-audit.md",
            "references/protocol-human-confirmation.md",
            "references/protocol-memory-update.md",
            "references/protocol-subagent-delegation.md",
            "references/protocol-readiness-gate.md",
            "references/protocol-rollback.md",
            "references/subagent-validation-paper.md",
            "references/stage-6-independent-validation.md",
        ],
        "required_review_file": "reviews/stage6-validation-review.md",
        "required_reviewer": "Validation Reviewer",
        "risk_triggered_reviewers": ["Code-Review Reviewer", "Evidence-Gate Reviewer"],
        "gate_path": "data/validation/validation-report.md",
    },
}


def run_command_flow(
    command_text: str,
    project_dir: Path,
    skill_root: Path,
    fixed_reviews: dict | None = None,
    pending_decisions: list | None = None,
) -> dict:
    parts = command_text.split()
    if len(parts) != 3 or parts[:2] != ["/math-modeling", "stage"]:
        return {"ok": False, "error": "unsupported_command"}

    try:
        stage = int(parts[2])
    except ValueError:
        return {"ok": False, "error": "unsupported_command"}

    if stage not in STAGE_CONFIG:
        return {"ok": False, "error": "unsupported_command"}

    config = STAGE_CONFIG[stage]
    missing = [path for path in config["required_reads"] if not (skill_root / path).exists()]
    if missing:
        return {"ok": False, "error": "missing_required_reads", "missing_required_reads": missing}

    fixed_reviews = fixed_reviews or {}
    pending_decisions = pending_decisions or []
    if pending_decisions:
        return {
            "ok": False,
            "command": {"active_command": "stage", "stage": stage},
            "blockers": ["pending_decisions"],
        }

    review_key = f"stage{stage}"
    review_present = fixed_reviews.get(review_key, True)
    if not review_present:
        return {
            "ok": False,
            "command": {"active_command": "stage", "stage": stage},
            "review_required": True,
            "required_review_file": config["required_review_file"],
            "required_reviewer": config["required_reviewer"],
            "blockers": ["missing mandatory fixed-review artifact"],
        }

    smoke = run_smoke_flow(project_dir)
    return {
        "ok": True,
        "command": {"active_command": "stage", "stage": stage},
        "required_reads": config["required_reads"],
        "review_policy": {
            "main_agent_role": "workflow synthesis and Markdown audit updates",
            "fixed_reviewers": [config["required_reviewer"]],
            "risk_triggered_reviewers": config["risk_triggered_reviewers"],
        },
        "gate_path": config["gate_path"] if stage != 5 else smoke["gate_path"],
    }
