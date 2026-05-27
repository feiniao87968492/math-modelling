from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_new_package_has_core_files():
    required = [
        ROOT / "SKILL.md",
        ROOT / "CLAUDE.md",
        ROOT / "README.md",
        ROOT / "references" / "protocol-markdown-audit.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, missing


def test_dispatcher_is_markdown_first_and_not_yaml_state_machine():
    content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "Markdown-first" in content
    assert "Rule-First Execution" in content
    assert "Expert Review Policy" in content
    assert "总状态机" not in content
    assert "pending_confirmations" not in content


def test_core_protocols_exist_and_use_markdown_contracts():
    protocol_paths = [
        ROOT / "references" / "protocol-markdown-audit.md",
        ROOT / "references" / "protocol-human-confirmation.md",
        ROOT / "references" / "protocol-readiness-gate.md",
        ROOT / "references" / "protocol-rollback.md",
        ROOT / "references" / "protocol-memory-update.md",
        ROOT / "references" / "protocol-subagent-delegation.md",
    ]
    missing = [str(path) for path in protocol_paths if not path.exists()]
    assert not missing, missing

    audit = (ROOT / "references" / "protocol-markdown-audit.md").read_text(encoding="utf-8")
    assert "Markdown Audit Documents" in audit
    assert "workflow.md" in audit
    assert "Forbidden State-Machine Behavior" in audit


def test_stage5_and_reviewer_docs_exist():
    required = [
        ROOT / "references" / "subagent-model-building.md",
        ROOT / "references" / "subagent-validation-paper.md",
        ROOT / "references" / "subagent-specialists.md",
        ROOT / "references" / "stage-5-solution-implementation.md",
        ROOT / "references" / "evidence-gate.md",
        ROOT / "references" / "modeling-memory-template.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, missing


def test_stage_docs_use_contracts_not_state_machine_language():
    stage_files = sorted((ROOT / "references").glob("stage-*.md"))
    assert len(stage_files) == 10

    forbidden = [
        "Owning Subagent",
        "Delegation Contract",
        "HUMAN_REVIEW_REQUIRED",
        "IN_PROGRESS",
        "status must be",
        "pending_confirmations",
    ]
    required = [
        "## Stage Contract",
        "## Inputs",
        "## Required Reads",
        "## Outputs",
        "## Blocking Rules",
        "## Done When",
        "## Memory Check",
    ]

    for path in stage_files:
        content = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in content, {"file": path.name, "forbidden": needle}
        for heading in required:
            assert heading in content, {"file": path.name, "missing": heading}


def test_readme_and_evidence_gate_are_markdown_first():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    evidence_gate = (ROOT / "references" / "evidence-gate.md").read_text(encoding="utf-8")

    assert "Markdown-first" in readme
    assert "workflow.md" in readme
    assert "decisions/" in readme
    assert "gates/final-evidence-gate.md" in readme
    assert "modeling_state.yaml" not in readme

    assert "workflow.md" in evidence_gate
    assert "claims/claim-registry.md" in evidence_gate
    assert "gates/final-evidence-gate.md" in evidence_gate
    assert "modeling_state.yaml" not in evidence_gate


def test_skill_contains_typical_workflow_and_command_examples():
    content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "## 典型使用流程" in content
    assert "## 命令示例" in content
    assert "/math-modeling init" in content
    assert "/math-modeling export" in content
    assert "## 阻断时会看到什么" in content


def test_readme_contains_quickstart_skeleton_and_minimal_examples():
    content = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "## 适用场景" in content
    assert "## 新项目骨架" in content
    assert "workflow.md" in content
    assert "memory.md" in content
    assert "## 5 分钟上手" in content
    assert "## 最小文件示例" in content
    assert "## 常见阻断与处理" in content


def test_delivery_doc_and_readme_entry_exist():
    delivery = (ROOT / "DELIVERY.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "## 当前版本能力" in delivery
    assert "## 适合怎么试用" in delivery
    assert "## 回归覆盖概览" in delivery
    assert "## 已知边界" in delivery
    assert "## 推荐下一步" in delivery

    assert "DELIVERY.md" in readme
    assert "交付说明" in readme


def test_pilot_acceptance_checklist_exists_and_has_required_sections():
    content = (ROOT / "PILOT_ACCEPTANCE_CHECKLIST.md").read_text(encoding="utf-8")

    assert "## 试用目标" in content
    assert "## 试用前检查" in content
    assert "## 试用中观察" in content
    assert "## 关键异常记录" in content
    assert "## 试用后判定" in content
    assert "## 下一步动作" in content
    assert "workflow.md" in content
    assert "可继续试用" in content
    assert "修正后再试" in content
    assert "暂不建议推广" in content


def test_fixed_review_points_are_mandatory_hard_gates():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    protocol = (ROOT / "references" / "protocol-subagent-delegation.md").read_text(
        encoding="utf-8"
    )
    stage5 = (ROOT / "references" / "stage-5-solution-implementation.md").read_text(
        encoding="utf-8"
    )
    stage10 = (ROOT / "references" / "stage-10-paper-materials.md").read_text(
        encoding="utf-8"
    )

    assert "fixed review points are mandatory review gates" in skill
    assert "actual subagent-produced review artifacts" in claude
    assert "## Mandatory Review Gates" in protocol
    assert "reviews/stage5-implementation-readiness-review.md" in protocol
    assert "reviews/stage10-evidence-claim-review.md" in protocol
    assert "must stop and spawn the required reviewer" in protocol
    assert "reviews/stage5-implementation-readiness-review.md" in stage5
    assert "reviews/stage10-evidence-claim-review.md" in stage10


def test_reviewer_invocation_template_is_defined_for_fixed_review_gates():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    protocol = (ROOT / "references" / "protocol-subagent-delegation.md").read_text(
        encoding="utf-8"
    )
    stage4 = (ROOT / "references" / "stage-4-model-spec.md").read_text(encoding="utf-8")
    stage5 = (ROOT / "references" / "stage-5-solution-implementation.md").read_text(
        encoding="utf-8"
    )
    stage6 = (ROOT / "references" / "stage-6-independent-validation.md").read_text(
        encoding="utf-8"
    )
    stage10 = (ROOT / "references" / "stage-10-paper-materials.md").read_text(
        encoding="utf-8"
    )

    assert "## Reviewer Invocation Template" in skill
    assert "Spawn Reviewer:" in skill
    assert "Expected Output Path:" in skill
    assert "## Reviewer Invocation Template" in protocol
    assert "Blocking Question:" in protocol
    assert "reviews/stage4-algorithm-model-review.md" in protocol
    assert "reviews/stage5-implementation-readiness-review.md" in protocol
    assert "reviews/stage6-validation-review.md" in protocol
    assert "reviews/stage10-evidence-claim-review.md" in protocol
    assert "emit the reviewer invocation template" in stage4
    assert "emit the reviewer invocation template" in stage5
    assert "emit the reviewer invocation template" in stage6
    assert "emit the reviewer invocation template" in stage10
