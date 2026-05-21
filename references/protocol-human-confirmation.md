# Protocol — Human Confirmation

## Core Rule

只要当前阶段产生阻断型待确认项，必须先写入 `pending_confirmations`，再把阶段状态置为 `HUMAN_REVIEW_REQUIRED`，随后停止该阶段与所有依赖该决策的下游推进。

## Blocking Nodes

| 阶段 | 决策类型 | blocking |
|------|----------|----------|
| 1 | 题意多解 / 关键字段含义 / 关键假设确认 | true |
| 2 | 算法方案确认 | true |
| 3 | 主创新点确认 | true |
| 4 | 关键模型假设 / 目标函数 / 核心约束确认 | true |
| 6 | 跳过独立验证确认 | true |
| 7 | 扰动对象与范围确认 | false |
| 8 | 论文主图选择 | false |
| 9 | 图片警告是否接受 | false |
| 10 | 主结论与导出素材确认 | true |

## `pending_confirmations` Object

```yaml
- confirmation_id: "confirm_001"
  stage: 2
  decision_type: "algorithm_selection_confirmation"
  blocking: true
  question: "确认 Q1/Q2 推荐算法方案"
  options_presented:
    - "A. 接受默认推荐"
    - "B. 修改某个子问题算法"
    - "C. 增加候选算法"
    - "D. 暂停讨论"
  recommended_option: "A"
  impact_scope:
    - "data/algorithm_selection.yaml"
    - "stages.2_algorithm_selection"
    - "阶段3和阶段4的下游建模输入"
  affected_outputs:
    - "data/algorithm_selection.yaml"
  status: "PENDING"
```

## Decision Record Schema

`confirmed_decisions` 与 `data/interactions/user_decisions.yaml` 必须使用同一套字段，不允许 A/B/C 或不同阶段各写各的。

```yaml
- decision_id: "decision_stage2_001"
  confirmation_id: "confirm_001"
  stage: 2
  decision_type: "algorithm_selection_confirmation"
  decision: "accept_default"
  selected_option: "A"
  decision_summary: "用户接受默认推荐算法方案。"
  user_payload: {}
  impact_scope:
    - "data/algorithm_selection.yaml"
    - "stages.2_algorithm_selection"
  status_after_decision: "DONE"
  recorded_at: "2026-05-21T19:31:19+08:00"
```

字段约束：
- `decision_id`：统一主键，命名规则固定为 `decision_stage{stage}_{seq}`，例如 `decision_stage1_001`、`decision_stage2_003`；禁止混用 `decision_001`、UUID、自由文本前缀
- `confirmation_id`：必须指向被处理的 pending 项
- `decision_type`：与原 pending 项保持一致
- `decision`：使用稳定动作名，如 `accept_default`、`modify`、`reject`、`request_more_options`、`defer`、`provide_problem_statement`、`pause_until_inputs_ready`、`use_oral_description`
- `selected_option`：保留用户看到的选项字母，如 `A/B/C/D`
- `decision_summary`：一句话说明本次处理结果
- `user_payload`：结构化补充载荷；默认可为空对象 `{}`，但当确认分支依赖用户正文输入时必须写入约定字段
- `impact_scope`：写回受影响的产物或状态路径
- `status_after_decision`：写回处理后当前阶段状态，如 `DONE`、`IN_PROGRESS`、`NOT_STARTED`、`NEEDS_REVISION`、`HUMAN_REVIEW_REQUIRED`
- `recorded_at`：统一时间字段名，不再混用 `confirmed_at`、`resolved_at`、`decided_at`

## Allowed Output While Blocked

允许输出：
- 当前待确认项摘要
- 推荐方案与理由
- 备选项
- 风险与影响范围
- 用户可直接回复的选项格式

禁止输出：
- 将默认推荐视为自动同意
- 继续生成依赖该决策的正式下游产物
- 因 fallback 改方案后继续推进
- 将用户沉默解释为确认

## Confirmation Handling

所有处理分支都必须同时：
1. 按上面的统一 schema 写入 `human_interaction.confirmed_decisions`
2. 用同一对象结构写入 `data/interactions/user_decisions.yaml`
3. 更新或清理对应 `pending_confirmations` 项
4. 写回 `status_after_decision` 对应的阶段状态
5. 更新该阶段 `user_confirmation_status`
6. 若产生新的 blocking 问题，创建新的 `pending_confirmation`，而不是复用旧对象改写语义

- `accept_default` / 明确接受：更新受影响产物，阶段恢复 `IN_PROGRESS` 或直接 `DONE`
- `modify`：阶段转 `NEEDS_REVISION`
- `reject`：阶段转 `NEEDS_REVISION`
- `request_more_options`：保持 `HUMAN_REVIEW_REQUIRED`
- `defer`：保持 `HUMAN_REVIEW_REQUIRED`
- `provide_problem_statement`：基于补充题面继续 stage 1；若又生成新的关键解释待确认项，`status_after_decision` 仍应写 `HUMAN_REVIEW_REQUIRED`
- `pause_until_inputs_ready`：清空当前 pending，阶段回到 `NOT_STARTED`
- `use_oral_description`：基于口头描述继续 stage 1；若继续追问又产生新的 blocking 问题，`status_after_decision` 应写 `HUMAN_REVIEW_REQUIRED`，不得误写为 `IN_PROGRESS`
- 若 `decision: provide_problem_statement`，则 `user_payload.problem_statement_text` 必填；缺失时不得写成有效确认，阶段保持 `HUMAN_REVIEW_REQUIRED`
- 若 `decision: use_oral_description`，则 `user_payload.oral_description_text` 必填；缺失时不得写成有效确认，阶段保持 `HUMAN_REVIEW_REQUIRED`

## Command Contract

- `/math-modeling pending`：只读当前待确认项，不得写状态、不得写决策记录、不得推进阶段
- `/math-modeling confirm`：唯一处理入口；所有实际写回都必须表现为一次 confirm 处理
- `/math-modeling approve stage N`：只接受“采用当前推荐方案”的语义；底层必须规范化为 `confirm` + `decision: accept_default`
- `/math-modeling reject stage N --reason "..."`：只接受“否决当前推荐方案”的语义；底层必须规范化为 `confirm` + `decision: reject`
- 自然语言中的 `A/B/C/D`、`接受默认推荐`、`先暂停`、`先按口头描述继续` 等，都必须先映射成规范 `decision` 名称再写回
- 同一条用户回复不得同时处理多个 pending 项；若存在多个 pending，必须显式指定目标 confirmation 或保持阻断

## Branch Examples

### Stage 1 缺输入阻断的标准分支

```yaml
# A. 用户补充题面文本
- decision_id: "decision_stage1_001"
  confirmation_id: "confirm_stage1_missing_problem_inputs"
  stage: 1
  decision_type: "problem_input_confirmation"
  decision: "provide_problem_statement"
  selected_option: "A"
  decision_summary: "用户按 A 选项提供了题面文本，用于继续 stage 1 审题。"
  user_payload:
    problem_statement_text: "...用户提供的题面正文..."
  status_after_decision: "HUMAN_REVIEW_REQUIRED"

# B. 用户要求先暂停
- decision_id: "decision_stage1_001"
  confirmation_id: "confirm_stage1_missing_problem_inputs"
  stage: 1
  decision_type: "problem_input_confirmation"
  decision: "pause_until_inputs_ready"
  selected_option: "B"
  decision_summary: "用户确认原始附件稍后补充，先暂停 stage 1。"
  status_after_decision: "NOT_STARTED"

# C. 用户允许先按口头描述推进
- decision_id: "decision_stage1_001"
  confirmation_id: "confirm_stage1_missing_problem_inputs"
  stage: 1
  decision_type: "problem_input_confirmation"
  decision: "use_oral_description"
  selected_option: "C"
  decision_summary: "用户选择先用口头描述建立 stage 1 初版事实与待确认项。"
  user_payload:
    oral_description_text: "...用户提供的口头描述..."
  status_after_decision: "HUMAN_REVIEW_REQUIRED"
```

若用户回复已经能映射到 A 或 C，但未提供可写入 `user_payload` 的正文内容（例如只回复 “A” / “C” / “按这个来”），则只能更新当前 `pending_confirmations` 项，记录“选项已识别但正文载荷缺失”的阻断说明；不得写入 `confirmed_decisions`，不得写成已完成确认，也不得把阶段状态改为 `IN_PROGRESS` 或 `DONE`。
