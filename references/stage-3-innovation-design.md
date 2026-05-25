# Stage 3 — Innovation Design

## Owning Subagent

Model-Building Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Model-Building Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback responses, but must not write global state.

## Inputs
- `data/algorithm_selection.yaml`
- `data/problem_analysis.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-model-building.md`
- `references/innovation-design.md`

## Outputs
- `data/innovation/innovation_design.yaml`
- `data/innovation/innovation_scorecard.md`
- `data/innovation/baseline_comparison_plan.md`
- `data/innovation/innovation_summary.md`

## Blocking Confirmation Point

创新点评分与 baseline 对照计划生成后、写入 `selected_innovations` 前，必须让用户确认主创新点。

## Rollback Response

If this stage receives a `rollback_request`, inspect the affected assumptions, model structure, algorithm choice, implementation outputs, and downstream dependencies before regenerating artifacts. Return a structured `rollback_response` to the Main Orchestrator; do not directly mark downstream stages complete.

## Done When
- 候选创新点有评分
- 每个候选创新点有 baseline 对照
- 用户已确认主创新点
- `selected_innovations` 已写入
- 已执行 `memory check`

## Revision Triggers
- 用户删除或替换主创新点
- 创新点缺乏验证路径
- grounding_score 不满足准入要求
