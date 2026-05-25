# Stage 5 — Solution Implementation

## Owning Subagent

Model-Building Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Model-Building Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback responses, but must not write global state.

## Inputs
- `data/model_spec.yaml`
- `data/algorithm_selection.yaml`
- `data/facts/data_dictionary.yaml`
- `data/facts/data_version.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-model-building.md`
- `references/subagent-specialists.md`
- `references/protocol-fallback-and-deviation.md`
- `references/code-review-pipeline.md`

## Outputs
- `code/python/`
- `data/results/code_review_report.md`
- `data/results/code_review_report.json`
- `data/results/result_sanity_check.json`
- `data/results/reproducibility_check.json`

## Blocking Confirmation Point

若推荐算法无法收敛、工具 fallback 改变方法、结果 sanity check 可能影响论文结论、创新对比不支持原假设，或需要在多组结果中选主结果，必须阻断确认。

## Rollback Response

If this stage receives a `rollback_request`, inspect the affected assumptions, model structure, algorithm choice, implementation outputs, and downstream dependencies before regenerating artifacts. Return a structured `rollback_response` to the Main Orchestrator; do not directly mark downstream stages complete.

## Done When
- 主求解代码与结果文件已生成
- 5 层 code review pipeline 已执行
- 必需的数据审计文件存在
- 若发生关键偏离，用户已确认处理方案
- 已执行 `memory check`

## Revision Triggers
- `blocking_errors > 0`
- 结果不支持已确认创新点
- fallback 导致方法偏离
