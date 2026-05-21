# math-modeling skill 尾项修复设计

日期：2026-05-21
范围：`C:\Users\zty\.agents\skills\math-modeling`
目标：收口 v2.0.0 结构重构后的两个未完成尾项：stage 1 `confirm` 正文载荷解析，以及 runtime `quality_status` canonical 命名。

## 1. 背景

当前 skill 的协议层已经把两个问题定义清楚，但运行时约束还不够硬，导致仍存在两类风险：

1. stage 1 在缺输入阻断场景下，用户走 A/C 分支时，回复中的正文载荷可能只被识别为“选了 A 或 C”，却没有稳定落进统一 decision schema。
2. `quality_status` 已要求使用 canonical 全大写蛇形命名，但文档层仍缺少足够明确的允许值边界与近义名收口规则，后续 runtime 容易继续漂移。

这两个问题都属于“协议已在、执行口径未完全收口”，因此本轮不做新一轮大结构改造，只补执行层约束与最小回归资产。

## 2. 本轮目标

1. 明确 stage 1 `confirm` 在 A/C 分支下的正文载荷必须写入统一 decision record。
2. 明确 A/C 分支若缺少正文，不得误写为已确认完成。
3. 明确 `quality_status` 的 canonical 集合、禁用近义名与迁移解释规则。
4. 新增一个独立的最小回归目录，用于人工回放和后续验收，不引入测试框架。

## 3. 非目标

本轮明确不做以下事项：

- 不重写 10 阶段结构。
- 不新增新的 workflow 命令。
- 不引入 Python/Node 测试框架。
- 不扩大到其它阶段的 decision payload 结构重做，除非是为了和 stage 1 保持字段一致。

## 4. 方案选择

本轮比较过三种路径：

### 方案 A：只改文档说明

优点：改动最小。
缺点：不能真正防止 runtime 在 headless `claude -p` 场景继续丢正文。

### 方案 B：补运行时约束层 + 最小回归目录（推荐）

优点：
- 直接对准真实尾项。
- 改动范围小，仍停留在 skill 文档/协议层。
- 可用最小回归资产锁住行为，降低后续漂移风险。

缺点：
- 仍需要后续实际回放验证，不能只靠静态文档自证。

### 方案 C：顺手扩到更多阶段和命令收口

优点：一次性补更多漏洞。
缺点：scope 失控，会把“尾项修复”重新扩成大改。

最终选定：**方案 B**。

## 5. 设计概览

本轮改动分为两部分：

1. **协议收口**：在现有 `references/protocol-human-confirmation.md` 与 `references/protocol-state-writeback.md` 上补硬约束。
2. **最小回归资产**：新增一个独立目录，存放输入场景、期望写回片段与禁止出现的错误状态。

## 6. stage 1 confirm 正文载荷设计

### 6.1 问题点

根据现有协议，stage 1 缺输入阻断存在三条标准分支：

- A：`provide_problem_statement`
- B：`pause_until_inputs_ready`
- C：`use_oral_description`

其中 A/C 都依赖用户在确认时附带正文。但现有协议更多是在分支示例层表达，没有把“正文必须进入哪个字段”写成强约束。

### 6.2 设计原则

- 保持统一 decision schema，不为 stage 1 另起一套记录结构。
- 选项字母和动作名仍沿用现有约定。
- 正文载荷进入明确字段，避免只在 `decision_summary` 中隐式出现。
- 若识别到 A/C 但正文缺失，必须保持阻断，而不是错误放行。

### 6.3 decision record 扩展

在不破坏现有主字段的前提下，为 A/C 分支增加结构化载荷字段：

```yaml
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
```

```yaml
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

### 6.4 缺正文处理

新增硬规则：

- 若用户回复被映射为 `provide_problem_statement`，则 `user_payload.problem_statement_text` 必填。
- 若用户回复被映射为 `use_oral_description`，则 `user_payload.oral_description_text` 必填。
- 若 A/C 被识别但正文为空、缺失、或仅有无信息量占位语，不得写成已完成确认。
- 此时应保持 `HUMAN_REVIEW_REQUIRED`，并显式提示“选项已识别，但正文载荷缺失，无法继续写回为有效确认”。

### 6.5 与现有状态机的关系

A/C 分支即便正文齐全，也不自动意味着 stage 1 完成，只表示当前缺输入阻断被正确消费。是否继续留在 `HUMAN_REVIEW_REQUIRED`，取决于新的题面文本或口头描述是否又引出新的待确认问题。

因此：

- A：通常仍写 `status_after_decision: HUMAN_REVIEW_REQUIRED`
- C：通常仍写 `status_after_decision: HUMAN_REVIEW_REQUIRED`
- B：保持 `status_after_decision: NOT_STARTED`

## 7. quality_status canonical 收口设计

### 7.1 问题点

当前规则已要求 `quality_status` 使用 canonical 全大写蛇形命名，但还缺一个足够明确的“允许值边界 + 近义名处理原则”，导致后续实现和回放时容易出现：

- 阶段状态词混入质量状态
- 同一阻断语义出现多个近义名
- 文档审查通过但 runtime 输出口径继续漂移

### 7.2 设计原则

- `quality_status` 只表达质量判断、阻断原因或当前工作口径。
- 阶段生命周期状态只由 `status` 表达，不再混入 `quality_status`。
- 同一语义只保留一个 canonical 名称。
- 对历史旧名给出迁移解释，便于回放或人工验收时判定。

### 7.3 canonical 集合

本轮将 `quality_status` 约束为以下集合或前缀：

- `PASS`
- `PASS_WITH_WARNINGS`
- `BLOCKED_*`
- `PAUSED_*`
- `USING_*`
- `FAILED_*`

其中：

- `PASS*`：表示质量判断通过
- `BLOCKED*`：表示存在阻断原因
- `PAUSED*`：表示经确认后暂停
- `USING*`：表示临时工作口径
- `FAILED*`：表示产物或检查失败

### 7.4 禁用规则

明确禁止以下模式：

- 混入阶段状态词：如 `DONE_OK`、`IN_PROGRESS_NORMAL`
- 同义阻断态并存：如两个都表达“缺题面输入”的不同名字同时存在
- 既表达状态又表达结论的复合口径：如 `DONE_WITH_BLOCKER`

### 7.5 迁移解释

本轮不做大规模历史状态重写，但协议需要给出迁移解释规则：

- 若读到旧名，解释时必须映射到唯一 canonical 名称
- 后续新增或更新记录时，只允许写 canonical 名称
- 验收时若发现旧名继续作为新写回结果出现，视为未通过

## 8. 最小回归目录设计

### 8.1 设计目标

skill 不是传统代码库，本轮不引入测试框架，而是放一个独立最小回归目录，用来承载：

- 输入场景
- 期望写回片段
- 禁止出现的错误结果

### 8.2 目录建议

建议新增：

```text
regression/
├── stage1-confirm-a-problem-statement.md
├── stage1-confirm-c-oral-description.md
└── quality-status-canonicalization.md
```

### 8.3 单文件结构

每个回归文件固定三段：

1. **输入场景**：给出用户回复和目标 pending 场景。
2. **期望写回片段**：给出应出现的 decision record 或 canonical status。
3. **禁止出现的错误结果**：列出本轮要防住的回归。

### 8.4 三个最小回归用例

#### 用例 1：stage 1 / A 分支 / 题面正文

验证点：
- 能识别为 `provide_problem_statement`
- `selected_option` 为 `A`
- `user_payload.problem_statement_text` 被保留
- 不会只留下“选了 A”但正文消失

#### 用例 2：stage 1 / C 分支 / 口头描述

验证点：
- 能识别为 `use_oral_description`
- `selected_option` 为 `C`
- `user_payload.oral_description_text` 被保留
- 缺正文时不得误写为有效确认

#### 用例 3：quality_status canonicalization

验证点：
- 文档中的允许值只来自 canonical 集合
- 新写回结果不再出现近义旧名
- 不把阶段状态语义塞进 `quality_status`

## 9. 验收标准

本轮通过的最低标准：

1. stage 1 选 A 并附正文时，decision record 必须保留题面正文载荷。
2. stage 1 选 C 并附正文时，decision record 必须保留口头描述载荷。
3. stage 1 选 A/C 但无正文时，不得误写为已确认完成。
4. `quality_status` 文档只保留 canonical 命名，不再接受近义重复或阶段状态混写。
5. 仓库中存在独立最小回归目录，覆盖上述三类场景。

## 10. 实施顺序

建议按以下顺序实施：

1. 更新 `references/protocol-human-confirmation.md`，把 A/C 正文载荷从分支示例升级为字段级硬约束。
2. 更新 `references/protocol-state-writeback.md`，补 canonical 集合、禁用规则与迁移解释。
3. 新增 `regression/` 目录及三份最小回归文件。
4. 用 headless `claude -p` 相关场景做一次人工回放验收。

## 11. 风险与控制

### 风险 1：字段扩展破坏统一 schema

控制：仅在统一 decision record 内新增 `user_payload`，不新增平行结构。

### 风险 2：canonical 规则写得过大，变成新一轮抽象工程

控制：本轮只收口允许前缀、禁用模式与最小迁移解释，不设计更复杂状态分类体系。

### 风险 3：回归目录变成第二套文档

控制：每个用例只保留“输入 / 期望写回 / 禁止结果”三段，不写长篇解释。

## 12. 结论

本轮是一次针对尾项的窄范围收口：

- 用字段级硬约束修复 stage 1 `confirm` 的正文载荷丢失问题
- 用 canonical 集合和禁用规则收口 `quality_status`
- 用最小回归目录把这两个行为锁住

这样可以在不重新扩大结构改造范围的前提下，把 v2.0.0 剩余的两个关键尾项真正补齐。