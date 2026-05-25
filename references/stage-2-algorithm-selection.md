# Stage 2 — Algorithm Selection

## Owning Subagent

Model-Building Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the Model-Building Subagent, and receives structured outputs. The subagent may recommend state changes, pending confirmations, memory updates, and rollback responses, but must not write global state.

## Inputs
- `data/problem_analysis.yaml`
- `data/facts/problem_facts.yaml`
- 如已存在则读取 `data/facts/data_dictionary.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-subagent-delegation.md`
- `references/protocol-rollback.md`
- `references/subagent-model-building.md`
- `references/protocol-fallback-and-deviation.md`
- `references/anti-hallucination.md`

## Outputs
- `data/algorithm_selection.yaml`

## Blocking Confirmation Point

候选算法表与默认推荐生成后、写入 `selected_algorithms` 前，必须生成阻断型待确认项。未确认前，阶段状态必须为 `HUMAN_REVIEW_REQUIRED`。

## Rollback Response

If this stage receives a `rollback_request`, inspect the affected assumptions, model structure, algorithm choice, implementation outputs, and downstream dependencies before regenerating artifacts. Return a structured `rollback_response` to the Main Orchestrator; do not directly mark downstream stages complete.

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
