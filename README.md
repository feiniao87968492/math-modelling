# math-modeling — 数学建模标准化工作流 Skill

面向数学建模竞赛（CUMCM/MCM/泰迪杯等）的 10 阶段标准化工作流 skill。适用于新赛题启动、阶段推进、结果审查、论文素材整理，以及需要强制人工确认和证据门控的场景。

## 10 阶段 Checklist

| # | 阶段 | 核心产出 |
|---|------|----------|
| 1 | 审题定类 | 问题分类、子问题拆解、约束条件 |
| 2 | 算法选型 | 候选算法 2-3 个 + 推荐理由 + 风险 |
| 3 | 创新设计 | 创新点候选、评分筛选、基线对比方案 |
| 4 | 建模 | 变量、假设、符号表、方程/目标函数 |
| 5 | 求解实现 | Python 代码 + 结果文件 + 运行日志 |
| 6 | 独立验证 | MATLAB 复现 / 对比误差（可跳过） |
| 7 | 敏感性分析 | 扰动表 + 敏感性图 + 结论 |
| 8 | 可视化 | PNG + CSV + meta.json |
| 9 | 图片审查 | 格式检查 + 内容合理性判断 |
| 10 | 成文准备 | figure_index + model_summary + innovation_summary + claim_registry |

## 安装

### 方式一：npx skills

```bash
npx skills add feiniao87968492/math-modelling
```

### 方式二：手动安装

```bash
# Claude Code / Codex CLI
git clone https://github.com/feiniao87968492/math-modelling.git ~/.agents/skills/math-modeling

# 创建 symlink（Claude Code）
ln -sf ~/.agents/skills/math-modeling ~/.claude/skills/math-modeling
```

## 核心结构

说明：文档中所有 `references/*.md` 默认指向 **math-modeling skill 包目录**，不是赛题项目目录。

本次重构后，`math-modeling` skill 采用：

- `SKILL.md`：轻量激活入口，只负责触发词、命令表、状态机、调度与全局硬约束
- `references/protocol-*.md`：横向协议层，负责确认、memory、状态写回、fallback 偏离控制
- `references/stage-*.md`：阶段层，负责各阶段输入、输出、阻断点、完成条件与回退条件
- 既有专题 references：负责数据审计、创新设计、图片审查、证据门控等专项规则

## 新增行为保证

### 1. 强阻断人工确认

关键节点一旦生成阻断型待确认项，workflow 必须进入 `HUMAN_REVIEW_REQUIRED`，不得继续自动推进。

### 2. memory.md 强制读写检查

每次进入阶段前必须读取项目根目录 `memory.md`；每次阶段收尾前必须执行一次 `memory check`，并把结果结构化写回 `modeling_state.yaml`。

### 3. fallback 偏离重确认

工具 fallback 可以自动发生；但若 fallback 改变了已确认算法、模型结构或证据路径，必须重新请求用户确认。

## 使用

在 Claude Code 中输入：

```text
/math-modeling
/math-modeling init
/math-modeling progress
/math-modeling next
/math-modeling stage 3
/math-modeling pending
/math-modeling confirm
/math-modeling review
/math-modeling gate
/math-modeling export
```

## 命令语义约束

- `/math-modeling init`：只生成最小可用骨架（如 `modeling_state.yaml`、`memory.md`、基础交互/证据门控文件），不是一次性展开完整赛题目录树
- `/math-modeling next`：进入下一个可执行阶段，不得绕过 pending gate；一旦进入目标阶段，必须同步写回 `current_stage` 与目标阶段 `IN_PROGRESS`
- `/math-modeling pending`：只查看待确认项，不修改状态
- `/math-modeling confirm`：处理待确认项的唯一入口
- `/math-modeling approve stage N`：`confirm` 的语义糖，底层仍写入决策记录
- `/math-modeling reject stage N --reason "..."`：`confirm` 的语义糖，底层仍写入决策记录

## 横向质量系统

除 10 阶段主流程外，以下系统跨阶段生效：

| 系统 | 职责 | 核心文件 |
|------|------|----------|
| Fact Grounding | 事实锚定与反幻觉 | `data/facts/*.yaml` + `references/anti-hallucination.md` |
| Modeling Memory | 规则记忆与经验沉淀 | `memory.md` + `references/protocol-memory-update.md` |
| Data Audit | 数据审计 | `references/data-audit.md` |
| Code Review | 代码审查流水线 | `references/code-review-pipeline.md` |
| Experiment Tracking | 实验追踪与归因 | `experiments/experiment_log.yaml` + `references/experiment-tracking.md` |
| Claim Grounding | 结论证据绑定 | `references/claim-grounding.md` |
| Final Evidence Gate | 终稿门控 | `references/evidence-gate.md` |
| Human Confirmation | 强阻断人工确认 | `references/protocol-human-confirmation.md` |
| State Writeback | 状态写回一致性 | `references/protocol-state-writeback.md` |
| Fallback Control | fallback 与偏离控制 | `references/protocol-fallback-and-deviation.md` |

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

### 专题规则文件
- `references/innovation-design.md`
- `references/sensitivity-analysis.md`
- `references/figure-review.md`
- `references/caption-spec.md`
- `references/anti-hallucination.md`
- `references/data-audit.md`
- `references/code-review-pipeline.md`
- `references/experiment-tracking.md`
- `references/claim-grounding.md`
- `references/modeling-memory-template.md`
- `references/evidence-gate.md`

## 项目结构

`/math-modeling init` 默认只生成**最小可用骨架**，通常至少包含：

```text
赛题目录/
├── modeling_state.yaml
├── memory.md
└── data/
    ├── interactions/
    │   └── user_decisions.yaml
    └── paper/
        └── final_evidence_check.md
```

下面是推荐逐步补齐的**完整赛题目录结构**，用于后续阶段推进：

```text
赛题目录/
├── modeling_state.yaml
├── memory.md
├── data/
│   ├── raw/
│   ├── processed/
│   ├── facts/
│   ├── interactions/
│   ├── innovation/
│   ├── results/
│   ├── validation/
│   ├── sensitivity/
│   ├── figures/
│   ├── reviews/
│   └── paper/
├── experiments/
├── code/
│   ├── python/
│   └── matlab/
└── logs/
```

## 适配平台

| 平台 | 安装路径 |
|------|----------|
| Claude Code | `~/.claude/skills/math-modeling` |
| Codex CLI | `~/.agents/skills/math-modeling` |
| Cursor | `.cursor/rules/math-modeling` |
| GitHub Copilot | `.github/skills/math-modeling` |

## License

MIT
