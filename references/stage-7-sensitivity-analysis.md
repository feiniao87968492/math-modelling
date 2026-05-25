# Stage 7 — Sensitivity Analysis

## Owning Subagent

Validation-Paper Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Validation-Paper Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback requests, but must not write global state.

## Inputs
- 阶段 5 结果
- 阶段 3 的创新点定义
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/sensitivity-analysis.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-validation-paper.md`

## Outputs
- `data/sensitivity/sensitivity_table.csv`
- `data/sensitivity/sensitivity_conclusion.md`
- `data/sensitivity/sensitivity_meta.json`
- `data/sensitivity/innovation_attribution.md`

## Blocking Confirmation Point

本阶段默认是非阻断确认；但若扰动范围缺乏依据且会改变结论解释方式，则应升级为阻断型待确认项。

## Rollback Triggers

If validation, sensitivity analysis, visualization, figure review, claim grounding, or evidence gating exposes a defect in assumptions, model structure, algorithm choice, implementation, result stability, or evidence support from stages 1-5, generate a structured `rollback_request` instead of silently patching downstream artifacts.

## Done When
- 扰动对象、范围、指标已明确
- 创新点优先覆盖策略已落实
- 需要进入论文的图已注册到 `data/figures/`
- 已执行 `memory check`

## Revision Triggers
- 扰动范围没有依据
- 敏感性结果与主结论冲突
- 创新归因证据不足
