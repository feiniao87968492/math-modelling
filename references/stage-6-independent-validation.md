# Stage 6 — Independent Validation

## Inputs
- 阶段 5 的主结果与代码
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`

## Outputs
- `data/validation/` 下的复现结果或对比说明
- 若跳过则写入 skip 记录

## Blocking Confirmation Point

若要跳过阶段 6，必须生成阻断型待确认项，说明跳过理由、替代验证方式、风险与对 Final Evidence Gate 的影响。

## Done When
- 已完成独立验证，或
- 用户明确确认跳过，并记录 `skip_reason`、`user_decision_id`、`alternative_validation`
- 已执行 `memory check`

## Revision Triggers
- 复现误差超出可接受范围
- 用户拒绝跳过独立验证
- 替代验证不能支撑主要结论
