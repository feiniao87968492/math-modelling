from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from smoke_readiness_gate_flow import run_smoke_flow

STAGE5_REQUIRED_READS = [
    "references/protocol-human-confirmation.md",
    "references/protocol-memory-update.md",
    "references/protocol-state-writeback.md",
    "references/protocol-subagent-delegation.md",
    "references/protocol-readiness-gate.md",
    "references/protocol-rollback.md",
    "references/subagent-model-building.md",
    "references/subagent-specialists.md",
    "references/protocol-fallback-and-deviation.md",
    "references/code-review-pipeline.md",
    "references/stage-5-solution-implementation.md",
]


def parse_math_modeling_command(command_text: str) -> dict:
    parts = command_text.strip().split()
    if len(parts) == 3 and parts[0] == "/math-modeling" and parts[1] == "stage":
        return {"active_command": "stage", "stage": int(parts[2])}
    raise ValueError(f"unsupported command: {command_text}")


def required_reads_for(command: dict, overrides: list[str] | None = None) -> list[str]:
    if overrides is not None:
        return overrides
    if command["active_command"] == "stage" and command["stage"] == 5:
        return STAGE5_REQUIRED_READS
    raise ValueError(f"unsupported command: {command}")


def validate_required_reads(skill_root: Path, required_reads: list[str]) -> list[str]:
    return [path for path in required_reads if not (skill_root / path).exists()]


def owning_subagent_for_stage(stage: int) -> str:
    if 1 <= stage <= 5:
        return "Model-Building Subagent"
    if 6 <= stage <= 10:
        return "Validation-Paper Subagent"
    raise ValueError(f"unsupported stage: {stage}")


def run_command_flow(
    command_text: str,
    project_dir: Path,
    skill_root: Path,
    required_read_overrides: list[str] | None = None,
) -> dict:
    command = parse_math_modeling_command(command_text)
    reads = required_reads_for(command, required_read_overrides)
    missing = validate_required_reads(skill_root, reads)
    if missing:
        return {
            "ok": False,
            "error": "missing_required_reads",
            "command": command,
            "required_reads": reads,
            "missing_required_reads": missing,
        }

    delegation = {
        "owning_subagent": owning_subagent_for_stage(command["stage"]),
        "subagent_contract": "structured readiness_gate output; Main Orchestrator writes global state",
    }
    smoke = run_smoke_flow(project_dir)
    return {
        "ok": True,
        "command": command,
        "required_reads": reads,
        "delegation": delegation,
        "state_path": smoke["state_path"],
        "readiness_gate": smoke["readiness_gate"],
    }


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    with TemporaryDirectory(prefix="readiness-gate-command-") as temp_dir:
        result = run_command_flow("/math-modeling stage 5", Path(temp_dir) / "project", skill_root)
        if not result["ok"]:
            print(result)
            return 1
        print(result["state_path"])
    print("PASS readiness gate command flow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
