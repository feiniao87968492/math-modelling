# Stage 2 — Algorithm Selection

## Inputs
- `data/problem_analysis.yaml`
- `data/facts/problem_facts.yaml`
- 如已存在则读取 `data/facts/data_dictionary.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-fallback-and-deviation.md`
- `references/anti-hallucination.md`

## Outputs
- `data/algorithm_selection.yaml`

## Blocking Confirmation Point

候选算法表与默认推荐生成后、写入 `selected_algorithms` 前，必须生成阻断型待确认项。未确认前，阶段状态必须为 `HUMAN_REVIEW_REQUIRED`。

## Done When
- 每个子问题都有 2-3 个候选算法
- 推荐理由包含题意目标或数据特征依据
- 用户已明确确认方案
- `selected_algorithms` 已写入
- 已执行 `memory check`

## Revision Triggers
- 用户要求改算法
- Data Audit 结果推翻原推荐依据
- fallback 改变了已确认算法方案
