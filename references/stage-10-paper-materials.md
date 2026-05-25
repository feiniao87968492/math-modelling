# Stage 10 — Paper Materials

## Owning Subagent

Validation-Paper Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Validation-Paper Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback requests, but must not write global state.

## Inputs
- 阶段 1-9 的产物与状态
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/claim-grounding.md`
- `references/evidence-gate.md`
- `references/caption-spec.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`

## Outputs
- `data/paper/claim_registry.yaml`
- `data/paper/final_evidence_check.md`
- `data/paper/figure_index.md`
- `data/paper/table_index.md`
- `data/paper/model_summary.md`
- `data/paper/innovation_summary.md`

## Blocking Confirmation Point

claim 草稿汇总后、正式导出论文素材前，必须让用户确认主结论、主图表与允许写入论文的创新表述。

## Rollback Triggers

If validation, sensitivity analysis, visualization, figure review, claim grounding, or evidence gating exposes a defect in assumptions, model structure, algorithm choice, implementation, result stability, or evidence support from stages 1-5, generate a structured `rollback_request` instead of silently patching downstream artifacts.

## Done When
- claim registry 已生成
- Final Evidence Gate 已通过
- 用户已确认主结论与导出素材
- 正式导出文件已生成
- 已执行 `memory check`

## Revision Triggers
- gate 结果为 `BLOCKED`
- claim 证据不足
- 用户否定主结论或导出内容
