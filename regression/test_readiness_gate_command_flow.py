from pathlib import Path

from command_readiness_gate_flow import run_command_flow

ROOT = Path(__file__).resolve().parents[1]


def test_stage5_command_flow_uses_markdown_protocols(tmp_path):
    project_dir = tmp_path / "project"
    result = run_command_flow("/math-modeling stage 5", project_dir, ROOT)

    assert result["ok"]
    assert "references/protocol-markdown-audit.md" in result["required_reads"]
    assert "Implementation Readiness Reviewer" in result["review_policy"]["fixed_reviewers"]
    assert not (project_dir / "modeling_state.yaml").exists()


def test_stage4_command_flow_uses_markdown_protocols(tmp_path):
    project_dir = tmp_path / "project"
    result = run_command_flow("/math-modeling stage 4", project_dir, ROOT)

    assert result["ok"]
    assert "references/protocol-markdown-audit.md" in result["required_reads"]
    assert "Algorithm/Model Reviewer" in result["review_policy"]["fixed_reviewers"]
    assert not (project_dir / "modeling_state.yaml").exists()


def test_stage6_command_flow_uses_markdown_protocols(tmp_path):
    project_dir = tmp_path / "project"
    result = run_command_flow("/math-modeling stage 6", project_dir, ROOT)

    assert result["ok"]
    assert "references/protocol-markdown-audit.md" in result["required_reads"]
    assert "Validation Reviewer" in result["review_policy"]["fixed_reviewers"]
    assert not (project_dir / "modeling_state.yaml").exists()


def test_stage4_blocks_when_algorithm_review_is_missing(tmp_path):
    project_dir = tmp_path / "project"
    result = run_command_flow(
        "/math-modeling stage 4",
        project_dir,
        ROOT,
        fixed_reviews={"stage4": False},
        pending_decisions=[],
    )

    assert result["ok"] is False
    assert result["review_required"] is True
    assert result["required_review_file"] == "reviews/stage4-algorithm-model-review.md"


def test_stage5_blocks_when_implementation_review_is_missing(tmp_path):
    project_dir = tmp_path / "project"
    result = run_command_flow(
        "/math-modeling stage 5",
        project_dir,
        ROOT,
        fixed_reviews={"stage5": False},
        pending_decisions=[],
    )

    assert result["ok"] is False
    assert result["review_required"] is True
    assert result["required_review_file"] == "reviews/stage5-implementation-readiness-review.md"


def test_stage6_blocks_when_validation_review_is_missing(tmp_path):
    project_dir = tmp_path / "project"
    result = run_command_flow(
        "/math-modeling stage 6",
        project_dir,
        ROOT,
        fixed_reviews={"stage6": False},
        pending_decisions=[],
    )

    assert result["ok"] is False
    assert result["review_required"] is True
    assert result["required_review_file"] == "reviews/stage6-validation-review.md"
