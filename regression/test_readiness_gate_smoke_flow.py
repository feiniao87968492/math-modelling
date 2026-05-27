from smoke_readiness_gate_flow import run_smoke_flow


def test_stage5_smoke_flow_writes_markdown_artifacts(tmp_path):
    project_dir = tmp_path / "project"
    result = run_smoke_flow(project_dir)

    assert result["ok"]
    assert not (project_dir / "modeling_state.yaml").exists()
    assert (project_dir / "workflow.md").exists()
    assert (project_dir / "gates" / "stage5-readiness-gate.md").exists()
    assert (project_dir / "decisions" / "decision-stage5-implementation-readiness.md").exists()
