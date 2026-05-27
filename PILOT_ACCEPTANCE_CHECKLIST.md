# math-modeling-v4 试用验收清单

## 试用目标

- 试点项目：Titanic Survival Prediction (Kaggle 经典二分类)
- 试用日期：2026-05-26
- 执行人：zty (via Claude Code agent)
- 项目类型：练习/试点（非比赛级）
- 试用范围：完整 10 阶段工作流，从 init 到 final evidence gate + export
- 本轮目标：同时验证工作流 + 观察结果质量

## 试用前检查

- [x] 已运行当前全量 regression，且结果为绿色 → **24/24 passed in 0.17s**
- [x] 试点项目范围较小、风险可控 → Titanic (891 行, 12 特征, 经典 ML 问题)
- [x] 已明确本轮把 v4 视为试点流程，而不是完整 runtime engine → DELIVERY.md 已读
- [x] 已准备好项目目录，或确认从空目录按 `README.md` 初始化 → titanic 目录含 train.csv/test.csv/题目.txt
- [x] 已写清本轮成功标准 → 全部 10 阶段通过 + Final Evidence Gate PASS + 代码产出可运行结果

## 试用中观察

- [x] `workflow.md` 成为当前工作的唯一主锚点 → **是**。workflow.md 跟踪了每个阶段的 checklist、active blockers、claim ceiling、next safe action，全程无 YAML 状态文件驱动
- [x] 缺失信息时，会生成明确的 `decisions/` 或 `branches/` 文档 → **部分验证**。decisions/ 生成了 2 份（stage1 问题定性 + stage2 算法选型）；branches/ 未触发（无缺失数据/工具场景）
- [x] claim ceiling 会随证据变化而收敛，不会越界 → **是**。演化为：none → feasible_baseline → validated_baseline → sensitivity_tested → validated_baseline (export)
- [x] gate 阻断是显式的，不会静默跳过 → **是**。stage4-model-readiness-gate.md、stage5-readiness-gate.md、final-evidence-gate.md 均有明确 pass/blocked 和 checks
- [ ] 晚期发现结构性问题时，会触发 `rollbacks/` → **未触发**。Titanic 问题定义清晰、数据完整、求解路径无结构性缺陷。rollback 机制未能在本次试点中得到验证
- [x] `export` 前会检查 `gates/final-evidence-gate.md` → **是**。final-evidence-gate.md 包含 10 项 checks，全部通过后才授权 export
- [x] reviewer 参与方式清楚，没有退回 stage-owner 状态机感 → **是**。Stage 9 figure review 以 reviewer 角色独立产出 `reviews/stage9-figure-review.md`，使用 Finding/Blocking risks/Non-blocking warnings 结构化格式

记录：

- 观察到的最顺畅环节：**Markdown 文档驱动工作流**。workflow.md 作为唯一主锚点，自然语言可读，无需理解 YAML 状态机。claim-registry 的 claim ceiling 演化路径清晰可审计。
- 观察到的最卡顿环节：**Stage 1/2 的阻断确认对简单问题的摩擦**。Titanic 是定义明确的经典 ML 问题，问题定性和算法选型不存在真正的歧义。阻断确认（A/B/C 选项）在这种情况下显得机械化。用户最终通过 "skip-confirm" 跳过后续阻断才完成全流程。建议：对低歧义度问题提供 "fast-track" 模式或降低确认强度。

## 关键异常记录

- 触发点：`references/anti-hallucination.md`
  预期行为：包含反幻觉规则和检查清单
  实际行为：文件仅含标题 "Anti-Hallucination"，正文为空
  严重程度：中 — Stage 1-2 required reads 引用了空文件，但不影响主流程
  后续动作：补齐 anti-hallucination.md 内容，或从 Stage 1/2 required reads 中移除

- 触发点：v4 init 命令
  预期行为：`/math-modeling init` 自动创建 Markdown-first 骨架
  实际行为：无自动化 init 脚本；需要手动创建 workflow.md、memory.md、各目录和初始 gate/claim 文件。README.md 的 quickstart 路径虽然描述了 init → progress → next，但没有可执行的 init 命令
  严重程度：高 — 新用户启动体验受影响，README 承诺与实际体验不一致
  后续动作：补齐 init 自动化逻辑（可以是 Python 脚本或明确的模板复制步骤）

- 触发点：rollback 机制
  预期行为：Stage 6-10 发现早期结构性缺陷时触发 rollback
  实际行为：Titanic 项目无结构性缺陷，rollback 路径完全未测试
  严重程度：低（试点项目特性导致），但回归测试中应有专门场景覆盖
  后续动作：在回归中加入构造的结构性缺陷场景（如 model specification 与 implementation 不一致）

- 触发点：阻断确认的 user experience
  预期行为：Stage 1/2 blocking decision 提供结构化选项，用户选择后解除阻断
  实际行为：选项设计合理（A/B/C + 推荐），但对简单问题摩擦感明显。用户输入 "2" 时存在解析歧义（数字 vs 字母 = A/B/C）
  严重程度：中 — 不影响正确性但影响流程体验
  后续动作：考虑增加 "快速模式" (如回复 "A" / "fast-track" / "auto")，或在决策文档中改用数字标记选项而非字母

## 试用后判定

- [x] 可继续试用
- [ ] 修正后再试
- [ ] 暂不建议推广

判定理由：v4 的 Markdown-first + 规则约束 + expert review 架构运转正常。workflow.md 锚点、claim ceiling 收敛、gate 显式阻断、reviewer 独立评审等核心机制均表现良好。三个中等严重程度的异常（空 anti-hallucination.md、缺失 init 自动化、简单问题的确认摩擦）均可修复，不构成架构级问题。rollback 路径需要专门场景测试。整体判定：**可继续试用**，同时修正上述异常。

## 下一步动作

- 需要修正的问题：
  1. 补齐 `references/anti-hallucination.md` 正文内容
  2. 实现 `/math-modeling init` 的自动化骨架创建（模板复制或脚本）
  3. 为低歧义问题增加 `fast-track` 确认模式
  4. 回归测试中增加 rollback 构造场景
  5. 决策文档选项标记统一（全部用字母 A/B/C 或全部用数字 1/2/3，避免混合）
- 下一轮重点观察：rollback 触发路径、fast-track 模式效果、init 自动化体验
- 是否需要与旧版 `math-modeling` 做对照：是 — 建议下一轮用同一赛题分别跑 v3 和 v4，对比产出物数量、确认次数、总耗时、产出质量
