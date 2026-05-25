# Lean Swarm Math Modeling Design

日期：2026-05-25
范围：`C:\Users\zty\.claude\skills\math-modeling`
目标：在现有 10 阶段数学建模工作流上增加轻量 subagent 编排层，并吸收 `using-superpowers` 的 protocol-first 思想，提高阶段执行稳定性、回滚可控性与质量门控可靠性。

## 1. 背景

当前 `math-modeling` skill 已完成结构性重构：`SKILL.md` 作为薄调度入口，详细规则下沉到 `references/` 中的 protocol 与 stage 文件。现有结构解决了主文件过重、确认协议不稳定、memory 检查不明确等问题。

下一步优化目标不是扩大工作流范围，而是提升执行组织方式：让不同阶段由不同 subagent 承担，并明确 subagent 与主编排器的边界。

## 2. 设计目标

1. 保留现有 10 阶段数学建模流程。
2. 将阶段 1-5 与阶段 6-10 分配给不同主 subagent。
3. 引入 Lean Swarm，而不是复杂 full swarm。
4. 将 `using-superpowers` 的“先检查适用协议，再行动”思想内化为 `math-modeling` 的 protocol-first 规则。
5. 增加 rollback 协议，处理后半阶段发现前半阶段缺陷的情况。
6. 保证主编排器仍然唯一负责全局状态、用户确认、状态写回与回滚执行。

## 3. 总体架构

采用三层结构：

```text
Main Orchestrator
  ├─ Model-Building Subagent：阶段 1-5
  ├─ Validation-Paper Subagent：阶段 6-10
  └─ Optional Specialists：按协议触发
```

### 3.1 Main Orchestrator

主编排器负责：

- 识别命令、当前阶段与适用 protocol；
- 加载 `SKILL.md` dispatch table 指定的 reference 文件；
- 决定调用哪个 subagent；
- 管理 `modeling_state.yaml` 状态流转；
- 执行 `memory.md` 阶段前读取与阶段后 memory check；
- 管理 `pending_confirmations`；
- 判断并执行 rollback；
- 与用户进行阻断确认交互。

主编排器是唯一可以修改全局状态的角色。

### 3.2 Model-Building Subagent

负责阶段 1-5：

1. Problem Understanding
2. Algorithm Selection
3. Innovation Design
4. Model Specification
5. Solution Implementation

输出偏构造性：

- problem analysis
- fact and assumption extraction
- algorithm candidates and recommendation
- innovation plan
- model specification
- solution implementation plan/code/results
- result sanity check
- rollback response

### 3.3 Validation-Paper Subagent

负责阶段 6-10：

6. Independent Validation
7. Sensitivity Analysis
8. Visualization
9. Figure Review
10. Paper Materials

输出偏审查与交付：

- independent validation report
- sensitivity analysis report
- visualization plan
- figure review report
- claim registry
- final evidence gate report
- rollback request
- paper material summary

### 3.4 Optional Specialists

specialist 不是常驻角色，只在协议或阶段文件明确触发时调用：

- Data-Audit Specialist：数据字段、缺失值、异常值、数据版本问题。
- Code-Review Specialist：阶段 5 求解代码质量、复现性与阻断错误。
- Figure-Review Specialist：阶段 9 图表可读性、caption、证据一致性。
- Evidence-Gate Specialist：阶段 10 claim 是否被证据支撑。
- Literature/Method Search Specialist：确需联网或外部方法背景时。

specialist 返回结构化审查结果，不参与全局状态决策。

## 4. 阶段分工合理性

阶段 1-5 与 6-10 的划分合理，因为它们对应两种不同心智模型：

- 阶段 1-5 是“构造主线”：理解题目、选择算法、设计创新、建立模型并求解。
- 阶段 6-10 是“验证交付主线”：验证结果、分析稳健性、制作图表、审查表达并准备论文素材。

该划分不应被理解为单向瀑布。数学建模中，后半阶段发现前半阶段缺陷是正常情况，尤其阶段 6 独立验证与阶段 7 敏感性分析可能触发回滚。

## 5. Rollback 协议

新增 `references/protocol-rollback.md`。

后五阶段如果发现前五阶段问题，不允许静默修补下游产物，必须生成 `rollback_request` 交给主编排器判断。

### 5.1 回滚等级

```text
MINOR_REVISION：问题局限在解释、图表、caption、论文表达或非结构性参数说明，留在阶段 6-10 内修正。
METHOD_REVISION：算法、参数、求解实现、结果稳定性或模型约束实现存在问题，回到阶段 5，必要时回到阶段 4。
STRUCTURAL_REVISION：题意理解、核心假设、算法路线、模型结构或创新点不成立，回到阶段 1-3。
```

### 5.2 rollback_request schema

```yaml
rollback_request:
  from_stage: 7
  target_stage: 5
  severity: "METHOD_REVISION"
  reason: "sensitivity analysis shows unstable output"
  evidence:
    - "data/validation/sensitivity_report.md"
  affected_outputs:
    - "data/results/main_result.csv"
    - "data/model_spec.yaml"
  requires_user_confirmation: true
  recommended_action: "rerun stage 5 with revised parameter bounds"
```

### 5.3 执行边界

- Subagent 可以提出 `rollback_request`。
- Subagent 不得直接改写前序阶段状态。
- 只有 Main Orchestrator 可以确认 rollback 等级、写入状态、触发用户确认并重新调度阶段。
- `METHOD_REVISION` 与 `STRUCTURAL_REVISION` 默认需要阻断确认。

## 6. Protocol-First Rule

将 `using-superpowers` 的核心思想内化到 `math-modeling`：

```text
Before answering, editing, calculating, coding, visualizing, validating, or exporting, identify the active command/stage/protocol and read the required reference files.
```

规则含义：

1. 不依赖模型对 skill 的记忆。
2. 当前 reference 文件始终是权威来源。
3. 只要某个 protocol 或 stage 可能适用，就先加载对应文件。
4. 阶段执行前必须明确当前 active stage、required reads、expected outputs 与 blocking confirmation point。

## 7. Subagent Delegation Policy

建议在 `SKILL.md` 中新增：

```markdown
## Subagent Delegation Policy

Default mode is Lean Swarm.

- Stages 1-5 MUST be delegated to Model-Building Subagent.
- Stages 6-10 MUST be delegated to Validation-Paper Subagent.
- Specialist subagents MAY be invoked only when their protocol is explicitly triggered.
- Subagents must return structured outputs, not free-form discussion.
- Subagents may recommend state changes, but only Main Orchestrator can write global state.
- Subagents may propose `rollback_request`, but cannot execute rollback directly.
```

## 8. 文件修改计划

### 8.1 新增文件

```text
references/protocol-subagent-delegation.md
references/protocol-rollback.md
references/subagent-model-building.md
references/subagent-validation-paper.md
references/subagent-specialists.md
```

### 8.2 修改文件

```text
SKILL.md
README.md
references/stage-1-problem-understanding.md
references/stage-2-algorithm-selection.md
references/stage-3-innovation-design.md
references/stage-4-model-spec.md
references/stage-5-solution-implementation.md
references/stage-6-independent-validation.md
references/stage-7-sensitivity-analysis.md
references/stage-8-visualization.md
references/stage-9-figure-review.md
references/stage-10-paper-materials.md
```

## 9. Stage 文件更新规则

每个 stage 文件需要新增或对齐三类信息：

1. `Owning Subagent`
2. `Delegation Contract`
3. `Rollback Triggers`

示例：

```markdown
## Owning Subagent

Model-Building Subagent

## Delegation Contract

The Main Orchestrator loads required protocols, passes scoped inputs to the owning subagent, and receives structured outputs. The subagent may recommend state changes but must not write global state.

## Rollback Triggers

If this stage receives a rollback request, inspect the affected assumptions, model structure, algorithm choice, or implementation outputs before regenerating downstream artifacts.
```

阶段 6-10 的 rollback trigger 应额外强调：发现前序缺陷时必须生成 `rollback_request`，不得静默修补。

## 10. 为什么不引入外部 full swarm prompt

暂不引入外部“蜂群”提示词。

原因：

1. 当前目标是提升流程稳定性，不是扩大角色数量。
2. 数学建模竞赛更需要证据链、状态写回、确认门控和回滚路径，而不是大量角色讨论。
3. 外部蜂群 prompt 可能增加观点冲突、重复工作、token 成本和状态漂移。
4. 两个主 subagent + 可选 specialist 已能覆盖主要质量风险。

后续如果真实赛题显示需要多个建模路线并行竞争、论文审稿式多角色辩论或复杂外部方法检索，再考虑升级为 full swarm。

## 11. 验收标准

实现后应满足：

1. `SKILL.md` 明确包含 Subagent Delegation Policy 与 Protocol-First Rule。
2. `SKILL.md` dispatch table 包含 subagent delegation 与 rollback protocol。
3. 阶段 1-5 文件声明 Model-Building Subagent。
4. 阶段 6-10 文件声明 Validation-Paper Subagent。
5. 阶段 6-10 文件包含 rollback trigger。
6. `protocol-rollback.md` 定义 severity、schema 与执行边界。
7. `protocol-subagent-delegation.md` 定义主编排器与 subagent 的权限边界。
8. subagent prompt 文件要求返回结构化产物，而不是自由讨论。
9. README 说明 Lean Swarm 的默认模式与不使用 full swarm 的理由。

## 12. 非目标

本次不做：

- 不新增 10 个阶段专属 subagent。
- 不引入外部 full swarm prompt。
- 不改变 10 阶段主流程。
- 不取消现有 Human Interaction Gate、memory check、Final Evidence Gate。
- 不让 subagent 直接写全局状态。
