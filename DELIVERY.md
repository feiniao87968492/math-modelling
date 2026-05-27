# math-modeling-v4 Delivery Notes

当前版本：**v4.2 — Improvement Hardening + Competition Realism**

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
- 新增 `references/protocol-improvement-loop.md`，明确 improvement loop 与 v4 既有协议的边界。

### v4.2 增量（Improvement Hardening + Competition Realism）

v4.2 把 v4.1 协议从"靠主 agent 自觉"提升到"自动验证 + 真实比赛约束对齐"，五项工作项独立 ship 且全部落地：

#### #1 — `/math-modeling improve` 命令级 harness
- 新增 `regression/command_improve_flow.py` 与 `regression/test_improve_command_flow.py`。
- 新增 8 条 fixture：`precondition-baseline-missing` / `precondition-stage7-missing` / `precondition-pending-decision` / `precondition-round-in-progress` / `reviewer-order-skepticism-before-critique` / `round-section-order-synthesized-before-skepticism` / `round-close-frontier-not-updated` / `happy-path-single-round`。
- dispatcher 在 round 启动 / reviewer 顺序 / round-N.md 段落顺序 / round close 四个 checkpoint 上的行为现在可被自动校验。

#### #2 — Reviewer 输出 schema + reviewer-eval regression
- 新增 `schemas/reviewer-output-schema.md`：9 段必填章节（v4 6 段 + v4.2 三段：Required reads referenced / Confidence / Forbidden-behavior self-check）；每条 Finding 含 Type / Severity / Evidence reference / Recommended action 四字段；Verdict 取值锁 PASS|PASS_WITH_WARNINGS|BLOCKED；Confidence 取值锁 high|medium|low。
- 新增 `schemas/reviewer-self-discipline-checklist.md`：通用 + 各 reviewer profile 专属的 forbidden behavior 自检清单。
- 新增 `regression/reviewer-eval/ground-truth/` × 6 条 buggy artifact + `expected-flags/` × 6 条 reviewer × fixture 的期望 flag 集合。
- reviewer 漏掉 required flag 即记录漂移；这是 reviewer profile 改动的回归网。

#### #3 — Per-question baseline 与 per-question frontier
- 升级 `references/baseline-snapshot-template.md`：多问赛题使用 `claims/baseline-snapshot.md` 索引 + `claims/baseline-q1.md` / `baseline-q2.md` / `baseline-q3.md` 多表布局。
- 升级 `references/improvements-templates.md`：多问赛题使用 `improvements/improvement-frontier.md` 索引 + `improvements/frontier-q1.md` / 等多表布局；round-N.md 元数据强制 `Target question` 与 `Cross-question impact expected` 字段。
- 升级 `references/protocol-improvement-loop.md`：新增"Per-question round metadata (v4.2)"段，定义 hard gate 行为。
- 新增 3 条 fixture：`target-question-missing` / `cross-question-regression-not-flagged` / `per-question-frontier-not-updated`。
- 单问项目（无 `claims/baseline-qK.md`）行为不变。

#### #4 — Stage-level time budget
- 新增 `references/protocol-time-budget.md`：opt-in 协议（`time-budget.md` 缺失即 v4.1 行为不变）。
- 升级 10 个 stage contract，每个追加 `## Time budget` 子段，引用 protocol。
- 新增 `/math-modeling time` 子命令族（`time` / `time start N` / `time stop N` / `time pause N` / `time resume N`），写入 burn-down 日志。
- 新增 4 条 fixture：`stage-switch-without-time-update` / `improve-with-low-remaining-budget` / `export-past-hard-deadline` / `time-budget-absent-no-error`。
- dispatcher 在 stage 切换 / improve 启动 / export 之前读取剩余预算；低于阈值（默认 20%）emit advisory；超过 hard deadline 阻断 export。
- 一旦用户在同 stage 内确认了一次 advisory，重复触发被抑制。

#### #5 — Export-time paper grounding scanner
- 新增 `references/protocol-paper-grounding-scan.md`：HTML 注释 anchor 约定（`<!-- claim: -->` / `<!-- claim-table: -->` / `<!-- derivation: -->`）+ deterministic 文本扫描（不做 LLM 语义匹配）。
- 升级 `regression/command_export_flow.py` 挂入 grounding scan 作为 hard gate；scan 缺失或不通过即阻断 export。
- 新增 4 条 fixture：`happy-path-all-grounded` / `number-without-claim-entry` / `figure-without-meta-json` / `formula-without-derivation-link`。
- 升级 `references/evidence-gate.md` 在 Gate Checks 列表追加 grounding scan 项。

#### v4.2 强阻断规则总览（追加到 SKILL.md §强阻断规则 第 16-22 条）

```
16. Critique F-ID 是唯一来源，下游 round-N.md / frontier / decision 不得重新编号或重贴标签
17. decision-improvement-round-N.md Pre-load 必须列全 Critique + Skepticism BLOCKING；
    Options 必须覆盖 Critique 全部 finding
18. improvement-frontier.md 不得在 Skepticism review 写入磁盘前出现 Skepticism Bk 引用；
    "pending Skepticism review" 中立占位允许
19. 多问赛题 improvement round 必须声明 Target question 并附 per-question baseline 对照
20. /math-modeling export 必须先跑 paper-grounding scan；任一项缺 grounding 即阻断
21. reviewer 输出必须遵循 schemas/reviewer-output-schema.md（9 段必填 / Finding 4 字段 /
    Confidence 取值 / 自检无 [VIOLATED]）
22. time-budget.md 存在时 dispatcher 在 stage 切换 / improve 启动 / export 之前
    必须读取剩余预算并按阈值 emit advisory；hard deadline 阻断 export
```

注：第 16-18 条是 v4.1 实战 dry-run 在 `练习与作业/v4.1-titanic-test/` 真 spawn Skepticism 时被独立 reviewer 抓到的 process audit 缺陷的硬规则化。

## 适合怎么试用

- 优先拿一个新的、小范围数学建模练习项目试用，而不是直接上比赛级主项目。
- 先按 `README.md` 的 quickstart 路径跑通 `init -> progress -> next -> gate -> export`。
- 完成 Stage 6 后，再用 `/math-modeling improve` 体验改进环路；至少跑一轮 Critique + Skepticism 完整流程。
- 多问赛题（Q1/Q2/Q3）启动时建议直接采用 `claims/baseline-qK.md` 多表布局；单问项目保留单表即可。
- 比赛模式下建议启用 `time-budget.md`；练习项目可以省略此文件让协议保持 v4.1 行为。
- 把现有 command-flow helper 视为回归契约和行为样例，不要把它们当成完整 runtime engine。
- 如果从旧项目迁移，旧的 `modeling_state.yaml` 仅作为历史上下文参考，不再作为 v4 的驱动源。

## 回归覆盖概览

| 维度 | 检查内容 | passed |
|---|---|---|
| contract tests | Markdown-first 文档契约、quickstart 内容、交付说明入口、fixed review hard gate | 12 |
| smoke flow | readiness gate 的最小行为链路 | 1 |
| readiness gate | supported claim level、required branches、阻断条件、命令级 stage 4/5/6 行为 | 10 |
| gate and rollback scenarios | 晚期结构性缺陷、pending decision、grounded claims | 4 |
| export and rollback command-flow | 导出拦截与 review 触发 rollback 的命令级行为 | 5 |
| v4.1 improvement loop（markdown fixture） | baseline 缺失、双 reviewer、frontier duplicate、claim level 静默升级 | 4 |
| **v4.2 #1 improve command-flow harness** | precondition × 4 + reviewer order + round section order + round close + happy-path | 13 |
| **v4.2 #2 reviewer schema + eval** | schema acceptance × 5 + reviewer-eval coverage × 4 + 注册 / 索引 × 7 | 16 |
| **v4.2 #3 per-question baseline** | target-question-missing × 2 + cross-question regression × 3 + frontier-not-updated × 3 + 单问 bypass × 1 + 注册 × 1 | 10 |
| **v4.2 #5 paper grounding scanner** | scan PASS / unresolved-claim / figure-no-meta / unresolved-derivation / malformed-anchor / export-flow integration × 3 + 注册 × 3 | 11 |
| **v4.2 #4 stage-level time budget** | absent-no-error × 3 + stage-switch × 2 + advisory × 3 + hard-deadline × 2 + 注册 + skill 文本 + stage 文本 | 14 |
| 处理 v4.1 实战 dry-run process audit 缺陷的 fixture | finding-id-consistency × 2 + decision-preload × 2 + frontier 抢跑 × 3 + 注册 × 1 | 8 |

最新一次 `pytest -x -q` 结果：**104 passed**。

## 已知边界

- 当前 regression helper 仍以 deterministic simulation 为主，不是完整运行时执行器。
- v4.2 完成后所有命令（`stage` / `improve` / `improve close` / `export`）都已有命令级 harness；命令级 harness 是契约样例，不是完整 runtime。
- reviewer-eval 是漂移监控基准，不是 CI 强制 gate；reviewer 可以合法地 surface 不同 finding，required flag 缺失只作为审计能力削弱信号。
- paper grounding scanner 不做 LLM 语义匹配；"应该 anchor 但未 anchor"由 Stage 10 Evidence/Claim Reviewer 负责，scanner 与 reviewer 互补。
- time-budget 协议是 opt-in；未配置 `time-budget.md` 的项目行为与 v4.1 完全一致。
- improvement loop 假设 Stage 7 sensitivity 已完成；若 sensitivity 缺席，dispatcher 会先回退到 v4 的既有路径要求补齐。

## 推荐下一步

- 在 v4.1-titanic-test 之外选择一个真实赛题或练习项目跑一次 v4.2 dry-run，验证 reviewer schema、paper-grounding anchor 与 per-question baseline 在真 LLM 输出下能否被严格遵循。
- 记录 v4.2 试用时遇到的阻断、歧义和不便利点；reviewer-eval 在真实 spawn 下记录的漂移可以反过来 inform 下一版 reviewer profile 改进。
- v4.2 plan 已 100% 落地；下一档（v4.3）的候选方向：runtime execution engine（把 deterministic simulation 升级为真实 runtime）、跨项目 baseline 复用、长期 frontier 持久化、sensitivity-driven model simplification reviewer 的具体实现。
