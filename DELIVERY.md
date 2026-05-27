# math-modeling-v4 Delivery Notes

当前版本：**v4.1 — Improvement Loop on Rule-Constrained Workflow**

## 当前版本能力

### v4 主体（Rule-Constrained Autonomous Workflow）

- 提供 Markdown-first 的 skill 调度入口，保留旧版 `math-modeling` 并以新包独立演进。
- 提供 rule-first 协议集合，覆盖 decision、gate、rollback、memory update、subagent delegation 与 readiness gate。
- 提供 10 个阶段 contract 文档，覆盖审题、选型、创新、建模、求解、验证、敏感性、可视化、审图和论文素材准备。
- 提供 4 个 fixed review point（Stage 4/5/6/10）的 hard gate；缺 reviewer artifact 时 dispatcher 必须先 emit reviewer invocation template 再停止下游工作。
- 提供 readiness gate、gate/rollback、export/rollback 的 scenario regression 和 command-flow regression。
- 提供 quickstart 文档与最小项目骨架，支持从新项目直接试用。

### v4.1 增量（Improvement Loop）

- 新增 `/math-modeling improve` 命令族（`improve` / `improve round N` / `improve status` / `improve close`），支持 Stage 6 PASS 之后启动多轮可量化的优化迭代。
- 新增 **Improvement-Critique Reviewer**（红队）与 **Improvement-Skepticism Reviewer**（蓝队），攻守双 reviewer 配对使用，对应 `references/subagent-improvement-critique.md` 与 `references/subagent-improvement-skepticism.md`。
- 新增 `claims/baseline-snapshot.md` 强制冻结：Stage 6 第一次 PASS 时由 dispatcher 写入，所有后续 round 必须以该 snapshot 为对照，不得"和上一轮比"或主观比较。
- 新增 `improvements/` 审计目录布局：`improvement-log.md`、`improvement-frontier.md`、`round-N.md`，frontier 维护 Tried-and-kept / Tried-and-reverted / Proposed / Abandoned 四象限。
- 新增 4 条强阻断规则（`SKILL.md` §强阻断规则 第 12-15 条）：baseline 对照、双 reviewer 必经、改动若覆盖已确认方法/结构必须走 v4 既有 fallback + rollback、claim level 不得静默升级。
- 新增 `references/protocol-improvement-loop.md`，明确 improvement loop 与 v4 既有协议（rollback / readiness gate / fallback / Final Evidence Gate / human-confirmation / memory-update）的边界，确保不绕开任何 v4 护栏。
- 新增 `references/protocol-subagent-delegation.md` Risk-Triggered 表两条：`improvement opportunity proposed → Improvement-Critique Reviewer`、`improvement proposal needs adversarial check → Improvement-Skepticism Reviewer`。
- 新增 `references/stage-6-independent-validation.md` Done-When 子句：第一次 PASS 时必须写出 baseline-snapshot。

## 适合怎么试用

- 优先拿一个新的、小范围数学建模练习项目试用，而不是直接上比赛级主项目。
- 先按 `README.md` 的 quickstart 路径跑通 `init -> progress -> next -> gate -> export`。
- 完成 Stage 6 后，再用 `/math-modeling improve` 体验改进环路；至少跑一轮 Critique + Skepticism 完整流程，确认 baseline 冻结与 frontier 更新生效。
- 把现有 command-flow helper 视为回归契约和行为样例，不要把它们当成完整 runtime engine。
- 如果从旧项目迁移，旧的 `modeling_state.yaml` 仅作为历史上下文参考，不再作为 v4 的驱动源。

## 回归覆盖概览

| 维度 | 检查内容 |
|---|---|
| contract tests | Markdown-first 文档契约、quickstart 内容、交付说明入口 |
| smoke flow | readiness gate 的最小行为链路 |
| readiness gate | supported claim level、required branches、阻断条件 |
| gate and rollback scenarios | 晚期结构性缺陷、pending decision、grounded claims |
| export and rollback command-flow | 导出拦截与 review 触发 rollback 的命令级行为 |
| **v4.1 improvement loop**（新增 4 条） | baseline-snapshot 缺失阻断、Skepticism review artifact 缺失阻断 Synthesized proposal、Critique 提议命中 frontier "Tried and kept" 时 Skepticism BLOCKING、claim level 静默升级阻断 |

最新一次 `pytest -x -q` 结果：**32 passed**。

## 已知边界

- 当前 regression helper 仍以 deterministic simulation 为主，不是完整运行时执行器。
- 并不是每个命令都已经有独立的 command-flow helper；improvement loop 当前只覆盖 markdown fixture 级别的契约，没有 command-flow harness。
- 文档、协议与回归已经接近试用状态，但真实比赛级项目仍建议先用小项目试点。
- improvement loop 假设 Stage 7 sensitivity 已完成；若 sensitivity 缺席，dispatcher 会先回退到 v4 的既有路径要求补齐。

## 推荐下一步

- 选择一个新的小项目做试点试用，至少要走到 Stage 6 PASS 才能体验 v4.1 改进环路。
- 记录试用时遇到的阻断、歧义和缺失的 command-flow（特别是 `/math-modeling improve` 的命令级 harness 还没补齐，可作为 v4.2 候选）。
- 根据试用结果，再决定是否扩展为更完整的 runtime execution layer，或追加 improvement loop 的 command-flow harness。
