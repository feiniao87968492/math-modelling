# Stage 6 — Independent Validation

## Owning Subagent

Validation-Paper Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Validation-Paper Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback requests, but must not write global state.

## Inputs
- 阶段 5 的主结果与代码
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`

## Outputs
- `data/validation/` 下的复现结果或对比说明
- 若跳过则写入 skip 记录

## Blocking Confirmation Point

若要跳过阶段 6，必须生成阻断型待确认项，说明跳过理由、替代验证方式、风险与对 Final Evidence Gate 的影响。

## Rollback Triggers

If validation, sensitivity analysis, visualization, figure review, claim grounding, or evidence gating exposes a defect in assumptions, model structure, algorithm choice, implementation, result stability, or evidence support from stages 1-5, generate a structured `rollback_request` instead of silently patching downstream artifacts.

## Done When
- 已完成独立验证，或
- 用户明确确认跳过，阶段状态为 `SKIPPED`，并记录 `skip_reason`、`user_decision_id`、`alternative_validation`
- 已执行 `memory check`

## Revision Triggers
- 复现误差超出可接受范围
- 用户拒绝跳过独立验证
- 替代验证不能支撑主要结论
