# Protocol — State Writeback

## Core Rule

任何阶段在宣布 `DONE`、`NEEDS_REVISION`、`HUMAN_REVIEW_REQUIRED` 或 `FAILED` 之前，都必须先完成状态写回。没有完整写回，不得宣布阶段完成。

## Ordered Writeback

按以下顺序执行：

1. 生成或更新阶段产物
2. 写入 `outputs`
3. 写入 `quality_status`
4. 写入 `memory_check` 结果（`UPDATED` 或 `NO_NEW_MEMORY`）
5. 若存在待确认项，写入 `pending_confirmations`
6. 更新阶段 `status`
7. 更新时间戳 `updated_at`

## Stage Entry Writeback

`/math-modeling next` 或 `/math-modeling stage N` 一旦宣布“已进入阶段 N”，必须同步写回：

1. `current_stage: N`
2. `stages.<N>.status: "IN_PROGRESS"`（除非该阶段已经处于 `DONE`、`HUMAN_REVIEW_REQUIRED`、`NEEDS_REVISION` 或 `FAILED`）
3. `updated_at`

禁止出现“`current_stage` 已切到 N，但 `stages.<N>.status` 仍是 `NOT_STARTED`”的状态不一致。

## Quality Status Naming Rule

`quality_status` 只允许表达“质量判断 / 阻断原因 / 当前工作口径”，不允许和阶段状态混写。统一规则：

- 允许的 canonical 名称或前缀只有：
  - `PASS`
  - `PASS_WITH_WARNINGS`
  - `BLOCKED_*`
  - `PAUSED_*`
  - `USING_*`
  - `FAILED_*`
- 语义说明：
  - `PASS*`：通过类
  - `BLOCKED*`：阻断类
  - `PAUSED*`：确认暂停类
  - `USING*`：临时工作口径类
  - `FAILED*`：失败类
- 不要把阶段状态词再塞进 `quality_status`，例如禁止 `DONE_OK`、`IN_PROGRESS_NORMAL`
- 不允许同一语义保留多个近义 canonical 名称；例如若“缺题面输入”已经选定一个 `BLOCKED_*` 名称，则不得再并存第二个近义阻断态
- 不允许写成同时表达阶段结论与质量口径的复合名，例如 `DONE_WITH_BLOCKER`

## Canonical Migration Guidance

- 读取历史状态时，若发现非 canonical 旧名，解释时必须映射到唯一的 canonical 名称
- 后续新增或更新记录时，只允许写 canonical 名称，不得继续写回旧名
- 若人工回放或 headless 验收中发现旧名继续作为“新写回结果”出现，视为未通过本轮收口

## Failure Mapping

- 产物生成失败：`FAILED`
- 产物已生成但需返工：`NEEDS_REVISION`
- 生成阻断型待确认项：`HUMAN_REVIEW_REQUIRED`
- 所有检查通过：`DONE`

## Invariants

- `outputs` 中的文件路径必须真实存在
- `pending_confirmations` 中的对象必须带 `confirmation_id`
- 若进入 `HUMAN_REVIEW_REQUIRED`，必须先写 pending，再写阶段状态
- 若用户已确认，必须同步清理或更新对应 pending 对象状态
- `confirmed_decisions` 与 `data/interactions/user_decisions.yaml` 必须使用同一 decision schema
- 每条 confirmed decision 都必须带 `decision_id`、`confirmation_id`、`decision`、`selected_option`、`decision_summary`、`status_after_decision`、`recorded_at`
- `decision_id` 必须遵守 `decision_stage{stage}_{seq}` 命名规则
- `quality_status` 必须遵守 canonical naming rule；近义状态名不得并存，非 canonical 旧名不得继续作为新写回结果出现
- 任一已收尾阶段都应存在 `memory_check` 记录
- 若 `current_stage` 已指向某阶段，该阶段状态不得仍为 `NOT_STARTED`
