# Stage 8 — Visualization

## Inputs
- 阶段 5 和阶段 7 的结果
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/caption-spec.md`

## Outputs
- `data/figures/*.png`
- `data/figures/*.csv`
- `data/figures/*.meta.json`

## Blocking Confirmation Point

本阶段默认允许非阻断确认主图选择；但若用户主图选择会改变阶段 10 的导出范围，应在导出前强制补确认。

## Done When
- 每张图同时产出 PNG、CSV、meta.json
- 候选图表清单已整理
- 主图与补充图分类明确
- 已执行 `memory check`

## Revision Triggers
- 图缺少 CSV 或 meta.json
- 图表风格与论文需求冲突
- 主图选择仍不明确
