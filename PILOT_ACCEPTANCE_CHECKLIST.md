# math-modeling-v4 试用验收清单

**当前文档版本：v4.2 — Improvement Hardening + Competition Realism**

本清单适用于 v4.2 pilot 试用。历史 v4 阶段试用记录见文末归档。

## 试用目标

- 试点项目：__________ (建议：练习项目或小型新赛题，避免直接上比赛级主项目)
- 试用日期：__________
- 执行人：__________
- 项目类型：练习/试点 / 比赛级（请选）
- 试用范围：完整 10 阶段工作流 + improve loop 至少一轮 + final evidence gate + export
- 项目类型：单问 / 多问（请选；多问启用 per-question baseline）
- 时间预算：启用 / 不启用（启用则需配置 `time-budget.md`）
- 本轮目标：验证 v4.2 全部硬化在真实项目下表现正常

## 试用前检查

- [ ] 已运行当前全量 regression，且结果为绿色 → 期望 **104 passed**（`pytest -x -q`）
- [ ] 试点项目范围较小、风险可控
- [ ] 已明确本轮把 v4.2 视为试点流程，而不是完整 runtime engine → DELIVERY.md 已读
- [ ] 已确认 6 个 reviewer subagent 注册在 `~/.claude/agents/mm-*-reviewer.md` 并可在新 session 中识别
- [ ] 已写清本轮成功标准（最少：改进环路至少跑一轮 / Final Evidence Gate PASS / 至少触发一次 readiness gate / 至少触发一次 fixed-review reviewer 真 spawn）

## 试用中观察 — v4 + v4.1 基础项

- [ ] `workflow.md` 成为当前工作的唯一主锚点（无 YAML 状态机驱动）
- [ ] 缺失信息时会生成明确的 `decisions/` 或 `branches/` 文档
- [ ] claim ceiling 会随证据变化而收敛，不会越界
- [ ] gate 阻断是显式的，不会静默跳过
- [ ] 晚期发现结构性问题时会触发 `rollbacks/`
- [ ] `/math-modeling export` 前会检查 `gates/final-evidence-gate.md`
- [ ] reviewer 参与方式清楚（独立 subagent 输出 review markdown）
- [ ] **Stage 4/5/6/10 缺 fixed-review artifact 时主 agent emit reviewer invocation template 然后真 spawn reviewer**（不得自审越过）

## 试用中观察 — v4.1 improvement loop

- [ ] Stage 6 第一次 PASS / PASS_WITH_WARNINGS 时 dispatcher 自动冻结 `claims/baseline-snapshot.md`
- [ ] `/math-modeling improve` 校验 5 个前置条件（Stage 6 PASS / baseline-snapshot / Stage 7 / 无 pending decision / 无 in-progress round）
- [ ] Critique reviewer 串行先行，Skepticism 后行（Skepticism Required Reads 包含 Critique 路径）
- [ ] `improvements/round-N.md` 前 6 段在 confirm 前写完，后 3 段（Implementation summary / Before vs after metrics / Frontier update）只在 confirm 后填
- [ ] `decisions/decision-improvement-round-N.md` Pre-load 列全 Critique + Skepticism 全部 BLOCKING；Options 覆盖全部 Critique finding
- [ ] 沉默不算 confirm
- [ ] round close 时 `improvement-frontier.md` 与 `improvement-log.md` 都得到更新；Stage 6 validation 重跑
- [ ] claim level 升级必须由 readiness 或 evidence gate 重新评估通过

## 试用中观察 — v4.2 hardening

### #1 improve command-flow harness
- [ ] 8 条 fixture 行为在真实运行中对应（precondition 缺失 / reviewer 顺序违规 / round-N.md section order / round close requirements 都按 hard gate 阻断）

### #2 reviewer schema + reviewer-eval
- [ ] 每份 `reviews/*.md` 含 9 段必填章节（v4 6 段 + v4.2 三段：Required reads referenced / Confidence / Forbidden-behavior self-check）
- [ ] 每条 Finding 含 Type / Severity / Evidence reference / Recommended action 四字段
- [ ] Verdict 行严格取 PASS|PASS_WITH_WARNINGS|BLOCKED
- [ ] Confidence 严格取 high|medium|low
- [ ] Forbidden-behavior self-check 无 `[VIOLATED]` 项；如出现则主 agent 重新 spawn
- [ ] reviewer-eval 在真 spawn 下表现：是否能稳定 surface required flags（用 `regression/reviewer-eval/ground-truth/` 作为 LLM 输入对照）

### #3 per-question baseline + frontier（仅多问项目触发）
- [ ] `claims/baseline-snapshot.md` 改造为索引；存在 `claims/baseline-q1.md` / `baseline-q2.md` / ...
- [ ] `improvements/round-N.md` 元数据声明 `Target question` 与 `Cross-question impact expected`
- [ ] `## Risk assessment` 含跨问题 baseline 对照行（target question 之外的每个 Q 都有对照行）
- [ ] round close 时 target question 与 cross-question impact 列出的所有 Q 的 per-question frontier 都得到更新
- [ ] Skepticism reviewer 对跨问题影响发表意见（多问场景下尤其要 surface "Q3 改进可能撞 Q1" 类风险）

### #4 stage-level time budget（仅启用 `time-budget.md` 触发）
- [ ] `time-budget.md` 含 Hard deadline / Total budget / Stage allocation / Burn-down log 四段
- [ ] `/math-modeling time start N` / `stop N` 写入 burn-down log
- [ ] 切换 stage 前必须先 stop 上一个 stage（previous_stage_not_stopped 阻断）
- [ ] 剩余预算 < 阈值（默认 20%）时 emit time-pressure advisory 并要求 confirm
- [ ] 同 stage 内 advisory 不重复触发（一次 confirm 后抑制）
- [ ] 超过 hard deadline 时 export 阻断（`hard_deadline_passed`）
- [ ] `time-budget.md` 缺失时整个协议是 no-op（v4.1 行为不变）

### #5 paper grounding scanner
- [ ] 论文 markdown 中的数字使用 `<!-- claim: <claim-id> -->` anchor
- [ ] 论文中的公式使用 `<!-- derivation: stage-{4,7}/<file>:<heading> -->` anchor
- [ ] 论文中的表使用 `<!-- claim-table: <claim-id> -->` anchor
- [ ] `figures/*.png` 都有对应的 `*.meta.json` 兄弟文件
- [ ] export 前 scanner 跑出 PASS（任一 unresolved 即 BLOCKED）
- [ ] scanner 不做 LLM 语义匹配（应当 anchor 但未 anchor 由 Stage 10 reviewer 负责）

## v4.2 process audit 规则（v4.1 实战发现 + v4.2 硬化）

- [ ] F-ID 一致性：critique / round-N.md / frontier / decision 之间 F-ID 不被重新编号或重贴
- [ ] decision Pre-load 列全 Critique + Skepticism 全部 BLOCKING；Options 覆盖 Critique 全部 finding
- [ ] frontier 不得在 Skepticism review 写入磁盘前出现"blocked by Skepticism Bk"；中立"pending Skepticism review"允许

## 关键异常记录

格式参考下面归档段落里的 v4 阶段记录。每条异常列：触发点 / 预期行为 / 实际行为 / 严重程度 / 后续动作。

## 试用后判定

- [ ] 可继续试用
- [ ] 修正后再试
- [ ] 暂不建议推广

判定理由：__________

## 下一步动作

- 需要修正的问题：__________
- 下一轮重点观察：__________
- 是否需要与旧版 v4 / v4.1 做对照：__________
- v4.3 候选方向：__________

---

# 历史归档：v4 阶段试用记录（2026-05-26）

> 以下内容是 v4 主体（无 v4.1 improvement loop / 无 v4.2 hardening）阶段在 Titanic 上的早期试点记录，保留供对照。此时 regression 24 passed。

## 试用目标（v4 阶段）

- 试点项目：Titanic Survival Prediction (Kaggle 经典二分类)
- 试用日期：2026-05-26
- 执行人：zty (via Claude Code agent)
- 项目类型：练习/试点（非比赛级）
- 试用范围：完整 10 阶段工作流，从 init 到 final evidence gate + export
- 本轮目标：同时验证工作流 + 观察结果质量

## 试用前检查（v4 阶段）

- [x] 已运行当前全量 regression，且结果为绿色 → **24/24 passed in 0.17s**
- [x] 试点项目范围较小、风险可控 → Titanic (891 行, 12 特征, 经典 ML 问题)
- [x] 已明确本轮把 v4 视为试点流程，而不是完整 runtime engine → DELIVERY.md 已读
- [x] 已准备好项目目录，或确认从空目录按 `README.md` 初始化 → titanic 目录含 train.csv/test.csv/题目.txt
- [x] 已写清本轮成功标准 → 全部 10 阶段通过 + Final Evidence Gate PASS + 代码产出可运行结果

## 试用中观察（v4 阶段）

- [x] `workflow.md` 成为当前工作的唯一主锚点 → **是**。
- [x] 缺失信息时，会生成明确的 `decisions/` 或 `branches/` 文档 → **部分验证**（branches/ 未触发）。
- [x] claim ceiling 会随证据变化而收敛，不会越界 → **是**。
- [x] gate 阻断是显式的，不会静默跳过 → **是**。
- [ ] 晚期发现结构性问题时，会触发 `rollbacks/` → **未触发**（Titanic 无结构性缺陷）。
- [x] `export` 前会检查 `gates/final-evidence-gate.md` → **是**。
- [x] reviewer 参与方式清楚 → **是**。

## 关键异常记录（v4 阶段）

- 触发点：`references/anti-hallucination.md` 正文为空 — 后已补齐
- 触发点：v4 init 命令缺自动化 — 已记录待办
- 触发点：rollback 机制未在 Titanic 试点触发 — v4.1 实战回归在 `练习与作业/v4.1-titanic-test/` 用人工构造场景补齐验证
- 触发点：阻断确认的 user experience — 数字 vs 字母选项混淆问题待优化

## 试用后判定（v4 阶段）

- [x] 可继续试用
- 判定理由：v4 的 Markdown-first + 规则约束 + expert review 架构运转正常。三个中等严重程度的异常均可修复，不构成架构级问题。判定：**可继续试用**。

## 后续演进（v4 → v4.1 → v4.2）

- 2026-05-27：v4.1 Improvement Loop ship；新增 `/math-modeling improve` 命令族 + 双 reviewer + baseline-snapshot 冻结 + 4 条新强阻断规则。
- 2026-05-27（晚）：v4.1 实战 dry-run 在 `练习与作业/v4.1-titanic-test/`；52 项 checklist 全部命中；真 spawn 三次 reviewer 抓出 3 条 process audit 缺陷。
- 2026-05-28：v4.2 Improvement Hardening + Competition Realism ship；五项工作项 100% 落地；新增 7 条强阻断规则；regression 32 → 104 passed。

进一步 v4.3 候选方向：runtime execution engine（把 deterministic simulation 升级为真实 runtime）、跨项目 baseline 复用、长期 frontier 持久化、sensitivity-driven model simplification reviewer 的具体实现。
