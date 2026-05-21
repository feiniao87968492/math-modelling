# math-modeling skill 结构性重构设计

日期：2026-05-21
范围：`C:\Users\zty\.claude\skills\math-modeling`
目标：通过“薄 `SKILL.md` + 厚 `references/` + 明确协议文件”的结构性重构，修复实际使用中暴露出的执行可靠性问题，并降低后续维护成本。

## 1. 背景与问题陈述

在实际调用 `math-modeling` skill 后，已确认存在以下问题：

1. `memory.md` 很少真正被更新，导致经验沉淀无法稳定参与后续阶段决策。
2. 在需要用户交互确认的关键节点（例如阶段2算法计划确认）没有真正停下工作流等待用户确认，Human Interaction Gate 偏文档化而非协议化。
3. 当前 skill 的主规范过于集中在 `SKILL.md` 中，导致激活内容过重、执行漂移风险高、规则虽存在但实际运行时不稳定生效。

此外，预判还存在以下高风险漏洞：

- 命令语义重叠，导致确认与状态更新不一致。
- 状态写回不原子，造成“做了但没记 / 记了但没做”。
- fallback 可能悄悄偏离用户已确认方案。
- 乱序执行时上游依赖过软，影响后续阶段质量。
- evidence gate 可能只检查文件存在，不检查证据是否足以支撑结论。
- 用户确认交互可能过重，拖慢流程效率。
- `memory.md` 在修复“不更新”后可能反向膨胀成流水账。

## 2. 设计目标

本次重构的目标不是增加更多功能，而是提高 workflow 的执行可靠性、可维护性和效率。

具体目标：

1. 将 `SKILL.md` 从“大而全规范文档”重构为“轻量激活入口 + 总状态机 + 调度规则”。
2. 将阶段细则与横向协议拆分到 `references/`，实现按需加载。
3. 将 Human Interaction Gate 升级为强阻断协议：关键节点未获用户明确确认时，必须停下工作流。
4. 将 `memory.md` 更新机制协议化：阶段开始前必读、阶段结束前必检。
5. 为状态写回、fallback 偏离、证据门控建立单独协议，减少 workflow 漏洞。
6. 保持现有 10 阶段框架不变，优先修复执行层问题，而不是扩大 scope。

## 3. 方案选择

已在设计阶段比较三类方案：

- 最小修补：只补三个问题，不改结构。
- 中度重构：保留框架，重写状态机与确认机制。
- 结构性重构：压缩 `SKILL.md`，细则下沉到 `references/`，同步修复执行缺陷。

最终选定：**结构性重构**。

原因：

- 当前 `SKILL.md` 过长，激活时更容易出现“知道规则存在，但不稳定执行”的漂移。
- `memory.md` 更新与 Human Interaction Gate 都不是局部规则缺失，而是入口级与协议级约束不足。
- 结构分层后，更容易持续维护和继续补洞，而不是继续向一个超长主文件堆规则。

## 4. 目标架构

### 4.1 总体原则

重构后采用：

- 薄 `SKILL.md`
- 厚 `references/`
- 协议文件（protocols）与阶段文件（stages）分离

`SKILL.md` 负责“调度与约束”，`references/` 负责“阶段细则与执行协议”。

### 4.2 `SKILL.md` 保留内容

重构后的 `SKILL.md` 仅保留六类内容：

1. frontmatter 与触发条件
2. 命令入口总表
3. 总状态机
4. 命令分发与 reference 加载表
5. 全局硬约束
6. 最小 schema 索引

不再保留：

- 超长阶段细则正文
- 大量 YAML 长样例
- 详尽子系统说明段落
- 冗长执行示例

`SKILL.md` 应像“工作流调度宪法”，而不是百科全书。

## 5. 文件拆分设计

### 5.1 保留并重写

- `SKILL.md`

### 5.2 保留但同步校正

- `README.md`

### 5.3 保留的现有 references

- `references/anti-hallucination.md`
- `references/innovation-design.md`
- `references/data-audit.md`
- `references/code-review-pipeline.md`
- `references/sensitivity-analysis.md`
- `references/figure-review.md`
- `references/caption-spec.md`
- `references/claim-grounding.md`
- `references/evidence-gate.md`
- `references/experiment-tracking.md`
- `references/modeling-memory-template.md`

### 5.4 新增协议文件

- `references/protocol-human-confirmation.md`
- `references/protocol-memory-update.md`
- `references/protocol-state-writeback.md`
- `references/protocol-fallback-and-deviation.md`

### 5.5 新增阶段文件

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

## 6. 状态机与强阻断确认机制

### 6.1 核心规则

新增硬规则：

> 只要当前阶段生成了阻断型待确认项，就必须先写入状态文件并把该阶段置为 `HUMAN_REVIEW_REQUIRED`，随后停止该阶段和所有依赖该决策的后续阶段推进。

这意味着：

- 不允许“先给用户看一下，同时继续往后做一点”。
- 不允许把沉默视为默认同意。
- 不允许在 pending 存在时继续执行依赖性下游步骤。

### 6.2 `pending_confirmations` 升格为核心对象

每个待确认项至少包含以下字段：

- `confirmation_id`
- `stage`
- `decision_type`
- `blocking`
- `question`
- `options_presented`
- `recommended_option`
- `impact_scope`
- `affected_outputs`
- `status`

推荐状态：`PENDING | CONFIRMED | REJECTED | REVISED`

### 6.3 阻断状态的行为边界

进入 `HUMAN_REVIEW_REQUIRED` 后：

允许：

- 输出结构化待确认项
- 说明推荐理由、风险、影响范围
- 给出明确选项
- 引导用户如何确认

禁止：

- 自动采用默认方案
- 继续生成依赖该决策的正式下游产物
- 使用 fallback 悄悄改方案并继续推进
- 将未明确回复解释为“默认接受”

### 6.4 恢复规则

用户回复后统一按以下流转处理：

- 接受默认推荐 → 写决策记录，恢复 `IN_PROGRESS` 或直接 `DONE`
- 修改方案 → 记录决策，状态转 `NEEDS_REVISION`
- 拒绝方案 → 记录决策，状态转 `NEEDS_REVISION`
- 请求更多候选 → 保持 `HUMAN_REVIEW_REQUIRED`
- 暂缓决定 → 保持 `HUMAN_REVIEW_REQUIRED`

### 6.5 阻断点定位原则

每个阶段文件都需明确：确认点发生在本阶段哪一步之后、哪一步之前。

例如：

- 阶段2：候选算法和默认推荐生成后、写 `selected_algorithms` 前
- 阶段3：创新评分完成后、确定 `selected_innovations` 前
- 阶段4：模型骨架明确后、冻结方程和约束前
- 阶段10：claim 汇总后、正式 export 前

## 7. `memory.md` 协议化更新机制

### 7.1 核心原则

`memory.md` 升级为阶段级协议对象：

- 阶段开始前必须读
- 阶段结束前必须检查是否写
- 若不写，也必须显式判断“无可沉淀新规则”

### 7.2 固定动作：memory check

每个阶段末尾执行一次 `memory check`，至少判断：

1. 是否发现新的可复用规则
2. 是否发现新的常见坑/反例
3. 是否新增用户偏好或决策偏好
4. 是否出现“下次应提前检查”的问题

### 7.3 允许沉淀的内容类型

只允许写入四类内容：

- 规则
- 坑点
- 反例
- 用户偏好

禁止写入：

- 阶段摘要
- 当日工作流水账
- 单次临时情况
- 文件路径罗列

### 7.4 写回时机

强制写回点：

- 阶段完成前
- 被用户否决或退回修订时
- 发现新规则/坑点时立即写

可选写回点：

- 大阶段切换前
- export 前做一次去重整理

### 7.5 结构建议

建议将项目中的 `memory.md` 固定为以下结构：

```markdown
## Rules
- ...

## Pitfalls
- ...

## Counterexamples
- ...

## User Preferences
- ...
```

同时要求：

- 新内容优先合并到已有条目
- 避免同义重复
- 每阶段默认新增 1-3 条，除非确有必要

## 8. 其他高风险漏洞与补丁

### 8.1 命令语义重叠

风险：`confirm`、`approve stage N`、`pending`、`next` 之间可能出现状态处理不一致。

补丁：

- `pending` 只查看
- `confirm` 作为唯一待确认项处理入口
- `approve/reject stage N` 作为 `confirm` 的语义糖，底层仍走同一协议
- `next` 不得绕过 pending gate

### 8.2 状态写回不原子

补丁：固定写回顺序：

1. 生成或更新产物
2. 写 `outputs`
3. 写 `quality_status`
4. 若有确认项，写 `pending_confirmations`
5. 更新阶段 `status`
6. 更新时间戳 `updated_at`

无完整写回，不得宣布阶段完成。

### 8.3 fallback 悄悄偏离方案

补丁：区分两类 fallback：

- 不改变方法本质 → 可自动执行，但必须记录 `fallback_reason`
- 改变已确认算法/模型结构/证据路径 → 必须重新触发阻断确认

### 8.4 乱序执行依赖过软

补丁：将依赖划分为硬依赖与软依赖。

例：

- 阶段5 对 Data Audit：硬依赖
- 阶段10 对阶段1-5、7-9：硬依赖
- 阶段8 对部分敏感性图：可视情况软依赖

### 8.5 evidence gate 只看存在性

补丁：证据检查至少分三层：

- 存在性
- 关联性
- 强度

### 8.6 用户确认负担过重

补丁：确认输出默认轻量，只展示：

- 推荐方案
- 备选项
- 风险
- 影响范围
- 回复方式

完整评分表按需展开。

### 8.7 `memory.md` 膨胀

补丁：增加“以后会再次影响决策”这一准入标准，并定期去重合并。

### 8.8 confirmation deadlock

补丁：每次阻断都必须输出当前 `confirmation_id`、所属阶段、影响范围，便于把用户自然语言回复映射到正确待确认对象。

## 9. 阶段文件设计原则

每个 `stage-*.md` 仅回答五个问题：

1. 进入本阶段前需要什么输入
2. 本阶段要读哪些横向协议
3. 本阶段生成哪些产物
4. 本阶段在哪个点可能触发阻断确认
5. 完成条件与失败/回退条件是什么

这样可避免阶段说明过重，并提升按需加载稳定性。

## 10. 实施顺序

建议按以下顺序执行，降低改坏 skill 的风险：

1. 重写 `SKILL.md` 骨架
2. 新增 4 个 protocol 文件
3. 拆分 10 个 stage 文件
4. 同步修订 `README.md`
5. 做一致性检查：
   - 版本号
   - 命令表
   - 状态枚举
   - references 路径
   - README 与 SKILL 是否一致

## 11. 本轮明确不做的事项

为避免 scope 失控，本轮不纳入：

- sprint mode / 标准模式双轨
- 新增更多命令
- 调整新赛题项目模板目录结构
- 额外平台适配扩展

本轮目标是：先把工作流执行可靠性修复到位。

## 12. 预期收益

完成本次重构后，预期获得以下收益：

- `SKILL.md` 激活更轻，执行更稳
- `memory.md` 从“偶尔更新”变成“阶段退出必检”
- Human Interaction Gate 从“文档说明”变成“状态机强阻断协议”
- fallback、状态写回、依赖与证据检查更可控
- 后续继续补规则时，不再需要向超长 `SKILL.md` 继续堆内容

## 13. 验收标准

本次重构完成后，至少满足以下验收标准：

1. `SKILL.md` 明显缩短，并只承担入口、调度和总状态机职责。
2. 关键确认节点可稳定进入 `HUMAN_REVIEW_REQUIRED`，且不会自动推进。
3. 任一阶段结束前都包含显式 `memory check` 规则。
4. fallback 若改变已确认方案，会触发重新确认。
5. `next`、`confirm`、`pending`、`approve/reject` 的职责边界清晰一致。
6. `README.md` 与 `SKILL.md`、`references/` 结构保持一致。
