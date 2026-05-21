# Stage 1 — Problem Understanding

## Inputs
- 题面文本
- `data/raw/` 中已有的原始附件（若存在）
- 项目根目录 `memory.md` 或 `references/modeling-memory-template.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/anti-hallucination.md`
- 若 `data/raw/` 非空，再读 `references/data-audit.md`

## Outputs
- `data/problem_analysis.yaml`
- `data/facts/problem_facts.yaml`
- `data/facts/assumptions.yaml`
- `data/facts/constraints_registry.yaml`

## Blocking Confirmation Point

完成事实、未知项、关键假设抽取后，若存在题意多解、关键字段含义不明、子问题输出形式不确定或关键假设影响后续建模结构，则生成阻断型待确认项并停止推进。

## Done When
- 事实、推断、未知信息已分层
- 关键约束都有来源
- 需要确认的 assumption 已被标记
- 已执行 `memory check`

## Revision Triggers
- 发现新的题面解释
- 用户否定关键假设
- 数据字段含义被重新解释
