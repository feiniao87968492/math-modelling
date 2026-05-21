# Stage 4 — Model Specification

## Inputs
- `data/problem_analysis.yaml`
- `data/algorithm_selection.yaml`
- `data/innovation/innovation_design.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`

## Outputs
- `data/model_spec.yaml`

## Blocking Confirmation Point

模型变量、目标函数、关键约束、baseline 与 innovation 差异明确后、冻结模型结构前，若存在新增关键假设、多目标权重、软约束或结构分歧，必须阻断确认。

## Done When
- baseline 与 innovation 模型都被明确描述
- 每个关键模型组件有来源映射
- 用户已确认关键假设与模型结构
- 已执行 `memory check`

## Revision Triggers
- 用户否定关键约束或目标函数
- 发现模型组件缺少事实或假设来源
- 下游实现暴露结构性不可实现问题
