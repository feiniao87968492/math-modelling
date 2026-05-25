# Stage 8 — Visualization

## Owning Subagent

Validation-Paper Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Validation-Paper Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback requests, but must not write global state.

## Inputs
- 阶段 5 和阶段 7 的结果
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/caption-spec.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`

## Outputs
- `data/figures/*.png`
- `data/figures/*.csv`
- `data/figures/*.meta.json`

## Blocking Confirmation Point

本阶段默认允许非阻断确认主图选择；但若用户主图选择会改变阶段 10 的导出范围，应在导出前强制补确认。

## Rollback Triggers

If validation, sensitivity analysis, visualization, figure review, claim grounding, or evidence gating exposes a defect in assumptions, model structure, algorithm choice, implementation, result stability, or evidence support from stages 1-5, generate a structured `rollback_request` instead of silently patching downstream artifacts.

## Done When
- 每张图同时产出 PNG、CSV、meta.json
- 候选图表清单已整理
- 主图与补充图分类明确
- 已执行 `memory check`

## Revision Triggers
- 图缺少 CSV 或 meta.json
- 图表风格与论文需求冲突
- 主图选择仍不明确
