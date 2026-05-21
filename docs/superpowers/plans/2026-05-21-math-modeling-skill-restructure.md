# math-modeling Skill Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the `math-modeling` skill into a thin dispatcher plus protocol/stage references so `memory.md` updates become mandatory, blocking confirmations actually stop the workflow, and command behavior stays consistent.

**Architecture:** Keep the existing 10-stage modeling workflow, but move detailed stage behavior out of `SKILL.md` and into focused `references/` files. Treat confirmation, memory updates, state writeback, and fallback deviations as first-class protocols that every stage must obey.

**Tech Stack:** Claude Code skill markdown files, YAML schemas embedded in markdown, PowerShell for local verification, git for change review.

---

## File Structure

### Files to modify
- `SKILL.md` — slim activation entrypoint: triggers, commands, state machine, dispatch table, hard rules, schema index.
- `README.md` — public-facing overview aligned with the new split between dispatcher, protocol files, and stage files.

### Files to create
- `references/protocol-human-confirmation.md` — blocking confirmation contract and pending object schema.
- `references/protocol-memory-update.md` — required `memory.md` read/write rules and `memory check`.
- `references/protocol-state-writeback.md` — ordered writeback rules for outputs, quality state, pending confirmations, and stage status.
- `references/protocol-fallback-and-deviation.md` — when fallback is allowed vs when it requires re-confirmation.
- `references/stage-1-problem-understanding.md`
- `references/stage-2-algorithm-selection.md`
- `references/stage-3-innovation-design.md`
- `references/stage-4-model-spec.md`
- `references/stage-5-solution-implementation.md`
- `references/stage-6-independent-validation.md`
- `references/stage-7-sensitivity-analysis.md`
- `references/stage-8-visualization.md`
- `references/stage-9-figure-review.md`
- `references/stage-10-paper-materials.md`

### Verification surface
- `SKILL.md` line count must stay under 200 lines.
- `SKILL.md` must mention all four new protocol files.
- `README.md` must document the new repo structure and behavior changes.
- Command docs for `next`, `pending`, `confirm`, and `approve/reject` must be consistent across `SKILL.md` and `README.md`.

---

### Task 1: Rewrite `SKILL.md` into a thin dispatcher

**Files:**
- Modify: `SKILL.md`
- Test: `SKILL.md` line count and content scan via PowerShell

- [ ] **Step 1: Capture the current failure state**

Run:

```powershell
(Get-Content "SKILL.md").Count
Select-String -Path "SKILL.md" -Pattern "### 阶段1", "### 阶段10", "Human Interaction Gate", "memory.md"
```

Expected:
- First command returns a count far above 200.
- Second command shows stage detail and protocol detail still embedded directly in `SKILL.md`.

- [ ] **Step 2: Replace `SKILL.md` with the thin dispatcher content**

Write this exact file content:

```markdown
---
name: math-modeling
description: "数学建模标准化工作流。10阶段 checklist 覆盖审题定类、算法选型、创新设计、建模、求解实现、独立验证、敏感性分析、可视化、图片审查、成文准备。支持强阻断人工确认、memory.md 强制读写检查、状态追踪、质量门控、创新证据链。触发词：数学建模、建模流程、新赛题、math-modeling、/math-modeling init、/math-modeling progress、/math-modeling next"
metadata:
  author: zty
  version: 2.0.0
  created: 2026-05-13
  last_reviewed: 2026-05-21
  review_interval_days: 90
---

# /math-modeling — 数学建模标准化流程

你是数学建模竞赛工作流编排器。职责：维护 10 阶段 checklist、调度协议文件与阶段文件、执行强阻断确认、强制 memory 检查、维持证据链闭环。

## 触发条件

- 显式命令：`/math-modeling`、`/math-modeling init`、`/math-modeling progress`、`/math-modeling next`
- 阶段命令：`/math-modeling stage N`、`/math-modeling review`、`/math-modeling export`
- 确认命令：`/math-modeling pending`、`/math-modeling confirm`、`/math-modeling approve stage N`、`/math-modeling reject stage N --reason "..."`
- 自然语言：在数学建模项目目录下提到“新赛题”“开始建模”“建模流程”等

## 命令入口

| 命令 | 作用 |
|------|------|
| `/math-modeling init` | 初始化新赛题目录、状态文件、memory 文件 |
| `/math-modeling progress` | 查看 10 阶段状态与推荐下一步 |
| `/math-modeling next` | 进入下一个可执行阶段，不得绕过 pending gate |
| `/math-modeling stage N` | 进入指定阶段 |
| `/math-modeling pending` | 只查看待确认项，不修改状态 |
| `/math-modeling confirm` | 处理待确认项的唯一入口 |
| `/math-modeling approve stage N` | `confirm` 的语义糖，底层仍写入决策记录 |
| `/math-modeling reject stage N --reason "..."` | `confirm` 的语义糖，底层仍写入决策记录 |
| `/math-modeling audit` | 执行数据审计 |
| `/math-modeling review` | 执行阶段 9 图片审查 |
| `/math-modeling gate` | 执行终稿证据门控 |
| `/math-modeling export` | 导出论文素材，仅在 gate 通过后允许 |

## 总状态机

阶段标准状态：`NOT_STARTED | IN_PROGRESS | DONE | SKIPPED | NEEDS_REVISION | HUMAN_REVIEW_REQUIRED | FAILED`

标准流转：
- `NOT_STARTED -> IN_PROGRESS -> DONE`
- `IN_PROGRESS -> NEEDS_REVISION -> IN_PROGRESS`
- `IN_PROGRESS -> HUMAN_REVIEW_REQUIRED -> IN_PROGRESS | DONE | NEEDS_REVISION`
- `IN_PROGRESS -> FAILED`
- `IN_PROGRESS -> SKIPPED` 仅允许阶段 6 且必须有用户确认

强阻断规则：
1. 只要生成阻断型待确认项，必须先写入 `pending_confirmations`。
2. 写入待确认项后，当前阶段立即置为 `HUMAN_REVIEW_REQUIRED`。
3. 进入 `HUMAN_REVIEW_REQUIRED` 后，只允许输出结构化待确认内容，不得继续生成依赖该决策的下游产物。
4. 沉默不等于同意；只有明确回复才可解除阻断。

## 命令分发与必读 references

| 场景 | 必读文件 |
|------|----------|
| invoke / progress / status | `references/protocol-state-writeback.md` |
| next / stage N | `references/protocol-human-confirmation.md` + `references/protocol-memory-update.md` + 对应 `references/stage-N-*.md` |
| pending / confirm / approve / reject | `references/protocol-human-confirmation.md` |
| audit | `references/data-audit.md` + `references/protocol-state-writeback.md` |
| review | `references/stage-9-figure-review.md` + `references/figure-review.md` + `references/caption-spec.md` |
| gate / export | `references/stage-10-paper-materials.md` + `references/claim-grounding.md` + `references/evidence-gate.md` + `references/protocol-state-writeback.md` |

阶段附加读取：
- 阶段 1：`references/anti-hallucination.md`
- 阶段 2：`references/anti-hallucination.md`
- 阶段 3：`references/innovation-design.md`
- 阶段 5：`references/code-review-pipeline.md`
- 阶段 7：`references/sensitivity-analysis.md`
- 阶段 8：`references/caption-spec.md`
- 阶段 9：`references/figure-review.md` + `references/caption-spec.md`
- 阶段 10：`references/claim-grounding.md` + `references/evidence-gate.md` + `references/caption-spec.md`

## 全局硬约束

1. 每次进入阶段前必须读取项目根目录 `memory.md`；若不存在，回退读取 `references/modeling-memory-template.md`。
2. 每次阶段收尾前必须执行一次 `memory check`：要么写入新规则，要么显式判定“无新增 memory”。
3. 若 fallback 不改变工具但改变已确认方法、模型结构或证据路径，必须重新触发阻断确认。
4. `pending` 只查看；`confirm` 才能修改确认状态。
5. `export` 之前必须通过 Final Evidence Gate。

## 最小 schema 索引

```yaml
human_interaction:
  pending_confirmations: []
  confirmed_decisions: []

stages:
  2_algorithm_selection:
    status: "NOT_STARTED"
    user_confirmation_status: "NOT_REQUIRED"
    outputs: []

quality_systems:
  final_evidence_gate:
    status: "UNKNOWN"
    report: "data/paper/final_evidence_check.md"
```

## Reference 地图

协议文件：
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-fallback-and-deviation.md`

阶段文件：
- `references/stage-1-problem-understanding.md`
- `references/stage-2-algorithm-selection.md`
- `references/stage-3-innovation-design.md`
- `references/stage-4-model-spec.md`
- `references/stage-5-solution-implementation.md`
- `references/stage-6-independent-validation.md`
- `references/stage-7-sensitivity-analysis.md`
- `references/stage-8-visualization.md`
- `references/stage-9-figure-review.md`
- `references/stage-10-paper-materials.md`
```

- [ ] **Step 3: Verify the dispatcher is thin and complete**

Run:

```powershell
(Get-Content "SKILL.md").Count
Select-String -Path "SKILL.md" -Pattern "protocol-human-confirmation", "protocol-memory-update", "protocol-state-writeback", "protocol-fallback-and-deviation", "pending 只查看", "沉默不等于同意"
```

Expected:
- Line count is under 200.
- All six patterns are found exactly once or more in the new dispatcher.

- [ ] **Step 4: Commit the dispatcher rewrite**

Run:

```bash
git add SKILL.md
git commit -m "refactor: slim math-modeling skill dispatcher"
```

Expected:
- Commit succeeds with only `SKILL.md` staged.

---

### Task 2: Add the blocking confirmation protocol

**Files:**
- Create: `references/protocol-human-confirmation.md`
- Test: content scan in the new protocol file

- [ ] **Step 1: Confirm the protocol file does not exist yet**

Run:

```powershell
Test-Path "references/protocol-human-confirmation.md"
```

Expected:
- Returns `False`.

- [ ] **Step 2: Create the confirmation protocol file**

Write this exact file content:

```markdown
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

- `accept_default` / 明确接受：写入 `data/interactions/user_decisions.yaml`，更新受影响产物，阶段恢复 `IN_PROGRESS` 或直接 `DONE`
- `modify`：写入决策记录，阶段转 `NEEDS_REVISION`
- `reject`：写入决策记录，阶段转 `NEEDS_REVISION`
- `request_more_options`：保持 `HUMAN_REVIEW_REQUIRED`
- `defer`：保持 `HUMAN_REVIEW_REQUIRED`

## Command Contract

- `/math-modeling pending`：只读当前待确认项
- `/math-modeling confirm`：唯一处理入口
- `/math-modeling approve stage N`：语义糖，底层仍走 `confirm`
- `/math-modeling reject stage N --reason "..."`：语义糖，底层仍走 `confirm`
```

- [ ] **Step 3: Verify the blocking protocol content**

Run:

```powershell
Select-String -Path "references/protocol-human-confirmation.md" -Pattern "HUMAN_REVIEW_REQUIRED", "pending_confirmations", "沉默解释为确认", "唯一处理入口"
```

Expected:
- All four phrases are found.

- [ ] **Step 4: Commit the protocol file**

Run:

```bash
git add references/protocol-human-confirmation.md
git commit -m "feat: add blocking confirmation protocol"
```

Expected:
- Commit succeeds with one new protocol file.

---

### Task 3: Add the memory update protocol

**Files:**
- Create: `references/protocol-memory-update.md`
- Test: content scan in the new protocol file

- [ ] **Step 1: Confirm the protocol file does not exist yet**

Run:

```powershell
Test-Path "references/protocol-memory-update.md"
```

Expected:
- Returns `False`.

- [ ] **Step 2: Create the memory update protocol**

Write this exact file content:

```markdown
# Protocol — Memory Update

## Core Rule

`memory.md` 是阶段级协议对象，不是可选附注。每次进入阶段前必须读取；每次阶段结束前必须执行 `memory check`。

## Pre-Stage Read Rule

1. 优先读取项目根目录 `memory.md`
2. 若项目中不存在 `memory.md`，读取 `references/modeling-memory-template.md`
3. 进入阶段时必须把 memory 中与当前阶段相关的规则作为额外门槛使用

## `memory check`

阶段收尾前必须判断以下四项：

1. 是否发现新的可复用规则
2. 是否发现新的常见坑点
3. 是否发现新的反例
4. 是否新增明确的用户偏好

若四项都没有新增内容，必须显式判定：`no new memory`

## Allowed Memory Categories

```markdown
## Rules
- 以后会再次影响阶段决策的规则

## Pitfalls
- 容易重复踩中的坑点

## Counterexamples
- 看似合理但被证伪的方案

## User Preferences
- 会持续影响 workflow 行为的用户偏好
```

## Forbidden Content

禁止写入：
- 当日工作总结
- 阶段流水账
- 一次性临时情况
- 文件路径罗列

## Write Timing

必须写回的时机：
- 阶段完成前
- 被用户否决或退回修订时
- 发现新规则或坑点时立即写

可选写回时机：
- 大阶段切换前
- `export` 前统一去重整理
```

- [ ] **Step 3: Verify the memory protocol content**

Run:

```powershell
Select-String -Path "references/protocol-memory-update.md" -Pattern "memory check", "no new memory", "Rules", "User Preferences"
```

Expected:
- All four phrases are found.

- [ ] **Step 4: Commit the protocol file**

Run:

```bash
git add references/protocol-memory-update.md
git commit -m "feat: add memory update protocol"
```

Expected:
- Commit succeeds with one new protocol file.

---

### Task 4: Add state writeback and fallback/deviation protocols

**Files:**
- Create: `references/protocol-state-writeback.md`
- Create: `references/protocol-fallback-and-deviation.md`
- Test: content scans in both protocol files

- [ ] **Step 1: Confirm both protocol files do not exist yet**

Run:

```powershell
Test-Path "references/protocol-state-writeback.md"
Test-Path "references/protocol-fallback-and-deviation.md"
```

Expected:
- Both commands return `False`.

- [ ] **Step 2: Create the state writeback protocol**

Write this exact file content:

```markdown
# Protocol — State Writeback

## Core Rule

任何阶段在宣布 `DONE`、`NEEDS_REVISION`、`HUMAN_REVIEW_REQUIRED` 或 `FAILED` 之前，都必须先完成状态写回。没有完整写回，不得宣布阶段完成。

## Ordered Writeback

按以下顺序执行：

1. 生成或更新阶段产物
2. 写入 `outputs`
3. 写入 `quality_status`
4. 若存在待确认项，写入 `pending_confirmations`
5. 更新阶段 `status`
6. 更新时间戳 `updated_at`

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
```

- [ ] **Step 3: Create the fallback/deviation protocol**

Write this exact file content:

```markdown
# Protocol — Fallback and Deviation

## Core Rule

工具 fallback 可以自动发生，但方法偏离不能悄悄发生。凡是 fallback 改变了已确认算法、模型结构或证据路径，都必须重新触发确认。

## Safe Fallback

以下情况允许自动 fallback，但必须记录 `fallback_reason`：
- 同一方法换实现工具
- 同一图表换绘图后端
- 同一验证逻辑换等价执行环境

## Deviation Requiring Re-Confirmation

以下情况必须重新生成阻断型待确认项：
- 已确认的算法从 ARIMA 改为 LSTM
- 已确认的优化建模结构发生本质变化
- 已确认结论的主要证据路径改变
- 原计划中的 baseline / innovation 对照方式变化

## Required Record

```yaml
fallback_event:
  original_plan: "ARIMA + 残差修正"
  fallback_tool: "Python statsmodels"
  fallback_reason: "MATLAB MCP unavailable"
  method_changed: false
  requires_confirmation: false
```

若 `method_changed: true`，则 `requires_confirmation` 必须为 `true`。
```

- [ ] **Step 4: Verify both protocol files**

Run:

```powershell
Select-String -Path "references/protocol-state-writeback.md" -Pattern "Ordered Writeback", "pending_confirmations", "没有完整写回"
Select-String -Path "references/protocol-fallback-and-deviation.md" -Pattern "method_changed", "requires_confirmation", "不能悄悄发生"
```

Expected:
- All six patterns are found across the two files.

- [ ] **Step 5: Commit both protocol files**

Run:

```bash
git add references/protocol-state-writeback.md references/protocol-fallback-and-deviation.md
git commit -m "feat: add state and fallback protocols"
```

Expected:
- Commit succeeds with two new protocol files.

---

### Task 5: Add stage references for stages 1 through 4

**Files:**
- Create: `references/stage-1-problem-understanding.md`
- Create: `references/stage-2-algorithm-selection.md`
- Create: `references/stage-3-innovation-design.md`
- Create: `references/stage-4-model-spec.md`
- Test: content scans across the four stage files

- [ ] **Step 1: Create the stage 1 file**

Write this exact file content:

```markdown
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
```

- [ ] **Step 2: Create the stage 2 file**

Write this exact file content:

```markdown
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
```

- [ ] **Step 3: Create the stage 3 file**

Write this exact file content:

```markdown
# Stage 3 — Innovation Design

## Inputs
- `data/algorithm_selection.yaml`
- `data/problem_analysis.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/innovation-design.md`

## Outputs
- `data/innovation/innovation_design.yaml`
- `data/innovation/innovation_scorecard.md`
- `data/innovation/baseline_comparison_plan.md`
- `data/innovation/innovation_summary.md`

## Blocking Confirmation Point

创新点评分与 baseline 对照计划生成后、写入 `selected_innovations` 前，必须让用户确认主创新点。

## Done When
- 候选创新点有评分
- 每个候选创新点有 baseline 对照
- 用户已确认主创新点
- `selected_innovations` 已写入
- 已执行 `memory check`

## Revision Triggers
- 用户删除或替换主创新点
- 创新点缺乏验证路径
- grounding_score 不满足准入要求
```

- [ ] **Step 4: Create the stage 4 file**

Write this exact file content:

```markdown
# Stage 4 — Model Specification

## Inputs
- `data/problem_analysis.yaml`
- `data/algorithm_selection.yaml`
- `data/innovation/innovation_design.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`

## Outputs
- `data/model_spec.yaml`

## Blocking Confirmation Point

模型变量、目标函数、关键约束、baseline 与 innovation 差异明确后、冻结模型结构前，若存在新增关键假设、多目标权重、软约束或结构分歧，必须阻断确认。

## Done When
- baseline 与 innovation 模型都被明确描述
- 每个关键模型组件有来源映射
- 用户已确认关键假设与模型结构
- 已执行 `memory check`

## Revision Triggers
- 用户否定关键约束或目标函数
- 发现模型组件缺少事实或假设来源
- 下游实现暴露结构性不可实现问题
```

- [ ] **Step 5: Verify stages 1-4**

Run:

```powershell
Select-String -Path "references/stage-1-problem-understanding.md","references/stage-2-algorithm-selection.md","references/stage-3-innovation-design.md","references/stage-4-model-spec.md" -Pattern "Blocking Confirmation Point", "memory check", "Done When"
```

Expected:
- Each file contains all three headings/phrases.

- [ ] **Step 6: Commit stages 1-4**

Run:

```bash
git add references/stage-1-problem-understanding.md references/stage-2-algorithm-selection.md references/stage-3-innovation-design.md references/stage-4-model-spec.md
git commit -m "feat: add early-stage workflow references"
```

Expected:
- Commit succeeds with four new stage files.

---

### Task 6: Add stage references for stages 5 through 7

**Files:**
- Create: `references/stage-5-solution-implementation.md`
- Create: `references/stage-6-independent-validation.md`
- Create: `references/stage-7-sensitivity-analysis.md`
- Test: content scans across the three stage files

- [ ] **Step 1: Create the stage 5 file**

Write this exact file content:

```markdown
# Stage 5 — Solution Implementation

## Inputs
- `data/model_spec.yaml`
- `data/algorithm_selection.yaml`
- `data/facts/data_dictionary.yaml`
- `data/facts/data_version.yaml`
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-fallback-and-deviation.md`
- `references/code-review-pipeline.md`

## Outputs
- `code/python/`
- `data/results/code_review_report.md`
- `data/results/code_review_report.json`
- `data/results/result_sanity_check.json`
- `data/results/reproducibility_check.json`

## Blocking Confirmation Point

若推荐算法无法收敛、工具 fallback 改变方法、结果 sanity check 可能影响论文结论、创新对比不支持原假设，或需要在多组结果中选主结果，必须阻断确认。

## Done When
- 主求解代码与结果文件已生成
- 5 层 code review pipeline 已执行
- 必需的数据审计文件存在
- 若发生关键偏离，用户已确认处理方案
- 已执行 `memory check`

## Revision Triggers
- `blocking_errors > 0`
- 结果不支持已确认创新点
- fallback 导致方法偏离
```

- [ ] **Step 2: Create the stage 6 file**

Write this exact file content:

```markdown
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
```

- [ ] **Step 3: Create the stage 7 file**

Write this exact file content:

```markdown
# Stage 7 — Sensitivity Analysis

## Inputs
- 阶段 5 结果
- 阶段 3 的创新点定义
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/sensitivity-analysis.md`

## Outputs
- `data/sensitivity/sensitivity_table.csv`
- `data/sensitivity/sensitivity_conclusion.md`
- `data/sensitivity/sensitivity_meta.json`
- `data/sensitivity/innovation_attribution.md`

## Blocking Confirmation Point

本阶段默认是非阻断确认；但若扰动范围缺乏依据且会改变结论解释方式，则应升级为阻断型待确认项。

## Done When
- 扰动对象、范围、指标已明确
- 创新点优先覆盖策略已落实
- 需要进入论文的图已注册到 `data/figures/`
- 已执行 `memory check`

## Revision Triggers
- 扰动范围没有依据
- 敏感性结果与主结论冲突
- 创新归因证据不足
```

- [ ] **Step 4: Verify stages 5-7**

Run:

```powershell
Select-String -Path "references/stage-5-solution-implementation.md","references/stage-6-independent-validation.md","references/stage-7-sensitivity-analysis.md" -Pattern "Blocking Confirmation Point", "Revision Triggers", "memory check"
```

Expected:
- Each file contains all three phrases.

- [ ] **Step 5: Commit stages 5-7**

Run:

```bash
git add references/stage-5-solution-implementation.md references/stage-6-independent-validation.md references/stage-7-sensitivity-analysis.md
git commit -m "feat: add implementation-stage workflow references"
```

Expected:
- Commit succeeds with three new stage files.

---

### Task 7: Add stage references for stages 8 through 10

**Files:**
- Create: `references/stage-8-visualization.md`
- Create: `references/stage-9-figure-review.md`
- Create: `references/stage-10-paper-materials.md`
- Test: content scans across the three stage files

- [ ] **Step 1: Create the stage 8 file**

Write this exact file content:

```markdown
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
```

- [ ] **Step 2: Create the stage 9 file**

Write this exact file content:

```markdown
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
```

- [ ] **Step 3: Create the stage 10 file**

Write this exact file content:

```markdown
# Stage 10 — Paper Materials

## Inputs
- 阶段 1-9 的产物与状态
- 项目根目录 `memory.md`

## Required Reads
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/claim-grounding.md`
- `references/evidence-gate.md`
- `references/caption-spec.md`

## Outputs
- `data/paper/claim_registry.yaml`
- `data/paper/final_evidence_check.md`
- `data/paper/figure_index.md`
- `data/paper/table_index.md`
- `data/paper/model_summary.md`
- `data/paper/innovation_summary.md`

## Blocking Confirmation Point

claim 草稿汇总后、正式导出论文素材前，必须让用户确认主结论、主图表与允许写入论文的创新表述。

## Done When
- claim registry 已生成
- Final Evidence Gate 已通过
- 用户已确认主结论与导出素材
- 正式导出文件已生成
- 已执行 `memory check`

## Revision Triggers
- gate 结果为 `BLOCKED`
- claim 证据不足
- 用户否定主结论或导出内容
```

- [ ] **Step 4: Verify stages 8-10**

Run:

```powershell
Select-String -Path "references/stage-8-visualization.md","references/stage-9-figure-review.md","references/stage-10-paper-materials.md" -Pattern "Blocking Confirmation Point", "Done When", "Revision Triggers"
```

Expected:
- Each file contains all three phrases.

- [ ] **Step 5: Commit stages 8-10**

Run:

```bash
git add references/stage-8-visualization.md references/stage-9-figure-review.md references/stage-10-paper-materials.md
git commit -m "feat: add late-stage workflow references"
```

Expected:
- Commit succeeds with three new stage files.

---

### Task 8: Sync `README.md` with the new structure

**Files:**
- Modify: `README.md`
- Test: content scan in `README.md`

- [ ] **Step 1: Capture the current README mismatch**

Run:

```powershell
Select-String -Path "README.md" -Pattern "横向质量系统", "References 子模块", "SKILL.md"
```

Expected:
- Current README still describes the old single-file-heavy structure.

- [ ] **Step 2: Replace the overview, feature, and references sections with the new structure**

Update `README.md` so these sections read exactly as follows:

```markdown
## 核心结构

本次重构后，`math-modeling` skill 采用：

- `SKILL.md`：轻量激活入口，只负责触发词、命令表、状态机、调度与全局硬约束
- `references/protocol-*.md`：横向协议层，负责确认、memory、状态写回、fallback 偏离控制
- `references/stage-*.md`：阶段层，负责各阶段输入、输出、阻断点、完成条件与回退条件
- 既有专题 references：负责数据审计、创新设计、图片审查、证据门控等专项规则

## 新增行为保证

### 1. 强阻断人工确认

关键节点一旦生成阻断型待确认项，workflow 必须进入 `HUMAN_REVIEW_REQUIRED`，不得继续自动推进。

### 2. memory.md 强制读写检查

每次进入阶段前必须读取项目根目录 `memory.md`；每次阶段收尾前必须执行一次 `memory check`。

### 3. fallback 偏离重确认

工具 fallback 可以自动发生；但若 fallback 改变了已确认算法、模型结构或证据路径，必须重新请求用户确认。

## 命令语义约束

- `/math-modeling next`：进入下一个可执行阶段，不得绕过 pending gate
- `/math-modeling pending`：只查看待确认项，不修改状态
- `/math-modeling confirm`：处理待确认项的唯一入口
- `/math-modeling approve stage N`：`confirm` 的语义糖，底层仍写入决策记录
- `/math-modeling reject stage N --reason "..."`：`confirm` 的语义糖，底层仍写入决策记录

## references 结构

### 协议文件
- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-fallback-and-deviation.md`

### 阶段文件
- `references/stage-1-problem-understanding.md`
- `references/stage-2-algorithm-selection.md`
- `references/stage-3-innovation-design.md`
- `references/stage-4-model-spec.md`
- `references/stage-5-solution-implementation.md`
- `references/stage-6-independent-validation.md`
- `references/stage-7-sensitivity-analysis.md`
- `references/stage-8-visualization.md`
- `references/stage-9-figure-review.md`
- `references/stage-10-paper-materials.md`
```

- [ ] **Step 3: Verify README consistency**

Run:

```powershell
Select-String -Path "README.md" -Pattern "强阻断人工确认", "memory.md 强制读写检查", "protocol-human-confirmation", "stage-10-paper-materials"
```

Expected:
- All four patterns are found.

- [ ] **Step 4: Commit the README sync**

Run:

```bash
git add README.md
git commit -m "docs: sync readme with modular skill structure"
```

Expected:
- Commit succeeds with only `README.md` staged.

---

### Task 9: Run consistency checks across the restructured skill

**Files:**
- Modify: none
- Test: `SKILL.md`, `README.md`, all new `references/*.md`

- [ ] **Step 1: Verify all required files exist**

Run:

```powershell
$paths = @(
  "SKILL.md",
  "README.md",
  "references/protocol-human-confirmation.md",
  "references/protocol-memory-update.md",
  "references/protocol-state-writeback.md",
  "references/protocol-fallback-and-deviation.md",
  "references/stage-1-problem-understanding.md",
  "references/stage-2-algorithm-selection.md",
  "references/stage-3-innovation-design.md",
  "references/stage-4-model-spec.md",
  "references/stage-5-solution-implementation.md",
  "references/stage-6-independent-validation.md",
  "references/stage-7-sensitivity-analysis.md",
  "references/stage-8-visualization.md",
  "references/stage-9-figure-review.md",
  "references/stage-10-paper-materials.md"
)
$paths | ForEach-Object { "$_ -> $(Test-Path $_)" }
```

Expected:
- Every line ends with `True`.

- [ ] **Step 2: Verify the dispatcher references every protocol file**

Run:

```powershell
Select-String -Path "SKILL.md" -Pattern "protocol-human-confirmation", "protocol-memory-update", "protocol-state-writeback", "protocol-fallback-and-deviation"
```

Expected:
- All four protocol filenames are found.

- [ ] **Step 3: Verify confirmation command semantics are consistent**

Run:

```powershell
Select-String -Path "SKILL.md","README.md","references/protocol-human-confirmation.md" -Pattern "pending 只查看", "confirm", "approve stage", "reject stage"
```

Expected:
- The same command semantics are documented in all relevant files.

- [ ] **Step 4: Verify `memory check` and blocking rules are visible across the workflow**

Run:

```powershell
Select-String -Path "SKILL.md","references/protocol-memory-update.md","references/stage-1-problem-understanding.md","references/stage-2-algorithm-selection.md","references/stage-10-paper-materials.md" -Pattern "memory check", "HUMAN_REVIEW_REQUIRED"
```

Expected:
- `memory check` appears in the protocol and stage files.
- `HUMAN_REVIEW_REQUIRED` appears in the dispatcher and confirmation protocol path.

- [ ] **Step 5: Review git diff and verify the working tree is clean**

Run:

```bash
git diff --stat
git status --short
```

Expected:
- `git diff --stat` shows no unexpected markdown file changes.
- `git status --short` is empty because all planned commits have already been created in earlier tasks.
```