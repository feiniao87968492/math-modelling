# math-modeling — 数学建模标准化工作流 Skill

面向数学建模竞赛（CUMCM/MCM/泰迪杯等）的 10 阶段标准化工作流 agent skill。支持乱序执行、状态追踪、质量门控、创新证据链。

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

## 横向质量系统

除10阶段主流程外，内置7个横向质量系统贯穿所有阶段。这些系统**不新增独立阶段**，而是作为质量约束嵌入10阶段流程中；用户仍按10阶段推进。

| 系统 | 职责 | 核心文件 |
|------|------|----------|
| Fact Grounding | 事实锚定与反幻觉 | `data/facts/*.yaml` + `references/anti-hallucination.md` |
| Modeling Memory | 规则记忆与经验沉淀 | `memory.md` + `references/modeling-memory-template.md` |
| Data Audit | 数据审计 | `references/data-audit.md` |
| Code Review | 代码审查流水线 | `references/code-review-pipeline.md` |
| Experiment Tracking | 实验追踪与归因 | `experiments/experiment_log.yaml` |
| Claim Grounding | 结论证据绑定 | `references/claim-grounding.md` |
| Final Evidence Gate | 终稿门控 | `references/evidence-gate.md` |

## 使用

在 Claude Code 中输入：

```
/math-modeling              # 查看当前进度或初始化
/math-modeling init         # 初始化新赛题项目
/math-modeling progress     # 查看 checklist 状态
/math-modeling next         # 进入下一个推荐阶段
/math-modeling stage 3      # 进入指定阶段
/math-modeling innovate     # 进入创新设计
/math-modeling review       # 执行图片审查
/math-modeling export       # 生成论文素材索引
```

## 核心特性

### 创新设计模块

在算法选型之后、建模之前设计创新点，避免成文阶段临时包装。每个创新点经过 7 维度评分筛选（含 grounding 反幻觉评分），必须有 baseline 对照和验证方案。

### 事实锚定与反幻觉机制

所有题面事实、数据字段、模型假设、约束和论文结论都进入可追溯 registry (`data/facts/`)。任何模型组件和主要结论必须绑定事实来源或实验结果，避免 agent 凭空补充题意或过度解释。

### 敏感性分析

根据题目类型自动选择策略（评价类权重扰动、优化类参数扰动、PDE 网格敏感性、预测类交叉验证等）。

### 多层代码审查流水线

阶段5求解实现后自动执行 5 层审查：静态代码检查、数据输入检查、模型逻辑检查、结果合理性检查和复现性检查。只有通过审查的结果才能进入后续阶段。

### 实验追踪与创新归因

每次模型改动、参数调整、数据处理变化都记录到 `experiments/experiment_log.yaml`。创新点必须通过 baseline 对比、消融实验或敏感性证据证明有效，避免无法解释的结果提升。

### 图片审查

格式合规检查（坐标轴、图例、DPI、字号）+ 内容合理性判断（趋势一致性、量级合理性、异常点检测）。审查不通过自动回退重绘，最多 2 次。

### 结论证据绑定

阶段10生成 `claim_registry.yaml`，论文中的关键结论必须绑定结果文件、图表、敏感性分析或验证报告。无证据结论自动标记为不可写入。

### 配图说明

每张图自动生成 `meta.json`（含图类型、坐标轴、预期趋势、审查状态），最终汇总为 `figure_index.md`。

## 项目结构

`/math-modeling init` 生成的目录：

```
赛题目录/
├── modeling_state.yaml      ← 流程状态追踪
├── memory.md                ← 项目级规则记忆，init 时默认创建，可为空
├── data/
│   ├── raw/                 ← 原始附件
│   ├── processed/           ← 清洗数据
│   ├── facts/               ← 事实锚定（problem_facts / assumptions / constraints）
│   ├── innovation/          ← 创新设计产出
│   ├── results/             ← 求解结果 + 代码审查报告
│   ├── sensitivity/         ← 敏感性分析 + 创新归因
│   ├── figures/             ← 插图 (PNG+CSV+meta.json)
│   ├── reviews/             ← 审查报告
│   └── paper/               ← 论文素材 + claim_registry
├── experiments/             ← 实验追踪日志
├── code/
│   ├── python/
│   └── matlab/
└── logs/
```

## References 子模块

| 文件 | 职责 |
|------|------|
| `references/innovation-design.md` | 7 类创新方向、评分公式（含 grounding_score）、筛选规则 |
| `references/sensitivity-analysis.md` | 按题型自动选择敏感性策略 |
| `references/figure-review.md` | 格式检查表 + 内容审查规则 |
| `references/caption-spec.md` | meta.json schema + caption 写作规范 |
| `references/anti-hallucination.md` | 反幻觉规则、事实级别定义、阶段级落地规则 |
| `references/data-audit.md` | 数据字典、缺失值、异常值、单位、时间泄露审计 |
| `references/code-review-pipeline.md` | 5层代码审查流水线（静态检查→sanity check→复现性） |
| `references/experiment-tracking.md` | 实验日志 schema、baseline 对比、消融实验、归因 |
| `references/claim-grounding.md` | 结论证据绑定、claim registry、allowed_strength |
| `references/modeling-memory-template.md` | 规则记忆系统模板，6大领域规则 |
| `references/evidence-gate.md` | 终稿证据门控检查表 |

## 适配平台

| 平台 | 安装路径 |
|------|----------|
| Claude Code | `~/.claude/skills/math-modeling` |
| Codex CLI | `~/.agents/skills/math-modeling` |
| Cursor | `.cursor/rules/math-modeling` |
| GitHub Copilot | `.github/skills/math-modeling` |

## License

MIT
