# Stage 9 — Figure Review

## Inputs
- `data/figures/` 中的图像、CSV、meta.json
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/figure-review.md`
- `references/caption-spec.md`

## Outputs
- `data/reviews/` 下的图片审查报告

## Blocking Confirmation Point

若图片趋势与 `expected_pattern` 不一致且无法判断是模型问题还是真实现象，必须阻断确认并停止进入阶段 10。

## Done When
- 所有目标图片都完成格式审查
- 内容合理性结论明确
- 需要接受的警告已获确认
- 已执行 `memory check`

## Revision Triggers
- 审查结果为 `REVISE_REQUIRED`
- 图像异常指向阶段 5 模型问题
- 警告是否接受仍不明确
