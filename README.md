# math-modeling-v4 - Markdown-first workflow skill

这是一个新的 skill 包，与旧版 `math-modeling` 并存，面向使用 Markdown 审计文档推进数学建模流程的工作方式。

当前版本：**v4.2 — Improvement Hardening + Competition Realism**。在 v4 + v4.1 全部硬护栏的基础上把 v4.1 协议从"靠主 agent 自觉"提升到"自动验证 + 真实比赛约束对齐"：improve 命令级 harness、reviewer 输出 schema + reviewer-eval、per-question baseline 与 frontier、stage-level time budget（opt-in）、export-time paper grounding scanner。新增 7 条强阻断规则（第 16-22 条），命令表追加 `/math-modeling time` 子命令族。

## 当前试用状态

- v4 主体：Markdown-first dispatcher、协议文档、10 阶段 contract、scenario regression、command-flow regression。
- v4.1 增量：`/math-modeling improve` 命令、`claims/baseline-snapshot.md` 冻结、Improvement-Critique 与 Improvement-Skepticism 双 reviewer、`improvements/` 审计目录、4 条新强阻断规则（SKILL.md §强阻断规则 第 12-15 条）。
- **v4.2 增量**：5 项硬化全部落地（improve harness / reviewer schema / per-question baseline / time budget / paper grounding scanner）+ 7 条新强阻断规则（第 16-22 条）+ regression 32 → **104 passed**。
- 如果你准备正式试用或交付评估，先阅读根目录下的 `DELIVERY.md` 交付说明。

## 适用场景

- 新赛题从零启动
- 课程作业或练习项目
- 已有建模项目迁移到 Markdown-first v4

## Markdown-first v4

- `workflow.md`
- `memory.md`
- `decisions/`
- `gates/`
- `gates/final-evidence-gate.md`
- `branches/`
- `rollbacks/`
- `claims/claim-registry.md`
- `claims/baseline-snapshot.md` (Stage 6 第一次 PASS 冻结)
- `reviews/`
- `improvements/` (v4.1 改进环路审计目录)

## 10-stage checklist

1. Problem Understanding
2. Algorithm Selection
3. Innovation Design
4. Model Specification
5. Solution Implementation
6. Independent Validation
7. Sensitivity Analysis
8. Visualization
9. Figure Review
10. Paper Materials

## 新项目骨架

```text
project/
├── workflow.md
├── memory.md
├── decisions/
├── gates/
├── branches/
├── rollbacks/
├── claims/
│   ├── claim-registry.md
│   └── baseline-snapshot.md      ← Stage 6 第一次 PASS 后冻结
├── reviews/
└── improvements/                 ← v4.1: 改进环路审计目录
    ├── improvement-log.md
    ├── improvement-frontier.md
    └── round-N.md
```

## 5 分钟上手

1. 在项目目录执行 `/math-modeling init`
2. 打开 `workflow.md`
3. 执行 `/math-modeling progress`
4. 执行 `/math-modeling next`
5. 需要指定阶段时执行 `/math-modeling stage 5`
6. 若出现 decision blocker，执行 `/math-modeling confirm`
7. 完成后执行 `/math-modeling gate`
8. gate 通过后再执行 `/math-modeling export`

## v4.1 改进环路（Stage 6 PASS 之后才可用）

1. Stage 6 第一次 PASS 时，dispatcher 强制写入 `claims/baseline-snapshot.md`，冻结主指标。
2. 自然语言触发"还能更好吗""做下一轮""reduce WAPE 再试一次"，或显式执行 `/math-modeling improve`。
3. dispatcher 校验前置条件（baseline-snapshot 已冻结、Stage 7 sensitivity 已写入、无 pending decision、当前没有进行中的 round），任一不满足即阻断说明。
4. 主 agent emit reviewer invocation template 调度 **Improvement-Critique Reviewer**（红队，提议改进方向）。
5. Critique 输出后再 emit reviewer invocation template 调度 **Improvement-Skepticism Reviewer**（蓝队，反驳提议）。
6. 主 agent 综合两份 review 写 `improvements/round-N.md` 前 6 段，并把 Skepticism BLOCKING risks 前置到 `decisions/decision-improvement-round-N.md`。
7. 阻断等待用户 confirm。沉默不算 confirm。
8. confirm 后：
   - 若改动落入已确认方法/模型结构/证据路径，先按 `protocol-rollback.md` 生成 rollback 文档；
   - 否则按 Stage 5/6 既有合同重做相关切片。
9. 实现完成后写 round-N.md 后 3 段（implementation summary / before vs after metrics / frontier update），更新 `improvement-log.md` 与 `improvement-frontier.md`。
10. 复跑 Stage 6 validation review，通过后执行 `/math-modeling improve close` 收尾；后续 export 必须再次过 Final Evidence Gate。

### improve 命令变体

| 命令 | 作用 |
|---|---|
| `/math-modeling improve` | 进入下一轮 improvement，自动选择 round 编号 |
| `/math-modeling improve round N` | 显式指定 round 编号 |
| `/math-modeling improve status` | 输出 frontier + log 摘要 |
| `/math-modeling improve close` | 关闭当前 round，写 before-vs-after 与 frontier 更新 |

### 收敛条件

`/math-modeling improve` 在以下任一条件触发时不再追加新 round：

- 用户主动 stop；
- 边际收益小于 round-1 元数据里的 `marginal_threshold`；
- 当前 claim level 已达 round-1 元数据里的 `target_claim_level`；
- 连续 K 轮（默认 K=2）Skepticism BLOCKING 且 Critique 无新证据反驳；
- 剩余 frontier 全部位于 `Abandoned` 或被用户标记拒绝资源。

主 agent 不会自动开下一轮，每一轮都需要用户主动调用 `/math-modeling improve`。

## 最小文件示例

`workflow.md`

```markdown
# Modeling Workflow

## Current focus
Stage 2 algorithm selection

## Active blockers
- decisions/decision-stage2-algorithm.md

## Current claim ceiling
feasible_baseline
```

`decisions/decision-stage2-algorithm.md`

```markdown
# Decision - Stage 2 Algorithm

## Status
Pending

## Decision needed
Choose the main optimization route.
```

`gates/stage5-readiness-gate.md`

```markdown
# Stage 5 Readiness Gate

## Gate result
Blocked

## Supported claim level
feasible_baseline
```

## 常见阻断与处理

- 缺结构化数据：查看 `branches/`，补齐数据后再继续。
- 缺 solver：先接受 `feasible_baseline` 或补齐工具链。
- 出现 rollback：先处理 `rollbacks/*.md`，不要继续下游修补。
- export 被拦截：先检查 `decisions/`、`gates/final-evidence-gate.md` 和 `claims/claim-registry.md`。
- `/math-modeling improve` 被拒：检查 `claims/baseline-snapshot.md` 是否存在、Stage 7 sensitivity 是否完成、是否有 pending decision、当前是否有未关闭的 round-N.md。
- improvement round 想升级 claim level：必须有对应 readiness 或 evidence gate 重新评估通过，禁止静默修改 `claim-registry.md`。

## Regression

```powershell
python -m pytest -x -q
```

预期当前为 **104 passed**，覆盖 markdown contract、readiness gate、gate/rollback、export/rollback command-flow、v4.1 improvement fixture，以及 v4.2 五项硬化的 fixture：

- v4.1 markdown fixture（4 条）：
  - `regression/improvement-baseline-required.md`
  - `regression/improvement-double-reviewer.md`
  - `regression/improvement-frontier-no-duplicate.md`
  - `regression/improvement-claim-level-no-silent-upgrade.md`
- v4.1 实战 dry-run process audit fixture（3 条）：
  - `regression/improvement-finding-id-consistency.md`
  - `regression/improvement-decision-preload-coverage.md`
  - `regression/improvement-frontier-no-premature-skepticism-tag.md`
- v4.2 #1 improve command-flow（8 条）：`regression/improve-flow-fixtures/`
- v4.2 #2 reviewer schema + eval（6 ground-truth + 6 expected-flags）：`regression/reviewer-eval/`
- v4.2 #3 per-question baseline（3 条）：`regression/baseline-per-question/`
- v4.2 #4 time budget（4 条）：`regression/time-budget/`
- v4.2 #5 paper grounding scanner（4 条）：`regression/paper-grounding/`

## v4.2 关键参考

- `docs/v4.2-improvement-hardening-plan.md` — v4.2 设计与文件清单
- `references/protocol-paper-grounding-scan.md` — paper grounding scanner 协议
- `references/protocol-time-budget.md` — time budget 协议（opt-in）
- `schemas/reviewer-output-schema.md` — reviewer 输出结构化 schema
- `schemas/reviewer-self-discipline-checklist.md` — reviewer forbidden behavior 自检清单
- SKILL.md §强阻断规则 第 16-22 条 — v4.2 七条硬规则

## v4.1 关键参考

- `docs/v4.1-improvement-loop-plan.md` — v4.1 设计与文件清单
- `references/protocol-improvement-loop.md` — improve 命令的协议级流程
- `references/baseline-snapshot-template.md` — Stage 6 baseline 冻结模板
- `references/improvements-templates.md` — log / frontier / round-N 模板
- `references/subagent-improvement-critique.md` — 红队 reviewer profile
- `references/subagent-improvement-skepticism.md` — 蓝队 reviewer profile
- `SKILL.md` §强阻断规则 第 12-15 条 — improvement loop 的 4 条硬规则

