from pathlib import Path


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_smoke_flow(project_dir: Path) -> dict:
    project_dir.mkdir(parents=True, exist_ok=True)

    _write(project_dir / "memory.md", "# Modeling Memory\n\n## Rules\n\n")
    _write(
        project_dir / "workflow.md",
        "# Modeling Workflow\n\n"
        "## Active blockers\n"
        "- decisions/decision-stage5-implementation-readiness.md\n\n"
        "## Current claim ceiling\n"
        "feasible_baseline\n\n"
        "## Next safe action\n"
        "Wait for confirmation.\n\n"
        "Memory check: no new memory\n",
    )
    _write(
        project_dir / "gates" / "stage5-readiness-gate.md",
        "# Stage 5 Readiness Gate\n\n"
        "## Gate result\n"
        "Blocked: missing required inputs and solver capability\n\n"
        "## Intended claim level\n"
        "validated_optimum\n\n"
        "## Supported claim level\n"
        "feasible_baseline\n\n"
        "## Blocked claims\n"
        "- Global optimum\n"
        "- True ROI breakpoint\n",
    )
    _write(
        project_dir / "decisions" / "decision-stage5-implementation-readiness.md",
        "# Decision: Stage 5 Implementation Readiness\n\n"
        "## Confirmation record\n"
        "Pending.\n",
    )
    _write(project_dir / "branches" / "branch-stage5-relationship-data.md", "# Branch\n")
    _write(project_dir / "branches" / "branch-stage5-solver-setup.md", "# Branch\n")
    _write(project_dir / "claims" / "claim-registry.md", "# Claim Registry\n")
    _write(project_dir / "reviews" / "stage5-implementation-readiness-review.md", "# Review\n")
    _write(project_dir / "logs" / "workflow-trace.md", "# Workflow Trace\n")

    return {
        "ok": True,
        "workflow_path": str(project_dir / "workflow.md"),
        "gate_path": str(project_dir / "gates" / "stage5-readiness-gate.md"),
        "decision_path": str(project_dir / "decisions" / "decision-stage5-implementation-readiness.md"),
        "supported_claim_level": "feasible_baseline",
    }
