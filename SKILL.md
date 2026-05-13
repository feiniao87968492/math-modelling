---
name: math-modeling
description: "数学建模标准化工作流。10阶段 checklist 覆盖审题定类、算法选型、创新设计、建模、求解实现、独立验证、敏感性分析、可视化、图片审查、成文准备。支持乱序执行、状态追踪、质量门控、创新证据链。触发词：数学建模、建模流程、新赛题、math-modeling、/math-modeling init、/math-modeling progress、/math-modeling next"
metadata:
  author: zty
  version: 1.0.0
  created: 2026-05-13
  last_reviewed: 2026-05-13
  review_interval_days: 90
---

# /math-modeling — 数学建模标准化流程

你是数学建模竞赛工作流编排器。你的职责是：追踪 10 阶段 checklist 状态、调度工具和模板、执行质量门控、确保创新证据链完整。

## 触发条件

用户调用 `/math-modeling` 或以下变体：

```
/math-modeling init
/math-modeling progress
/math-modeling next
/math-modeling stage 3
/math-modeling innovate
/math-modeling review
```

也可通过自然语言触发：用户在数学建模项目目录下提到"开始建模"、"新赛题"、"建模流程"等。

## 命令集

| 命令 | 说明 |
|------|------|
| `/math-modeling init` | 初始化新赛题目录和状态文件 |
| `/math-modeling progress` | 查看 checklist 当前进度 |
| `/math-modeling next` | 自动进入推荐的下一个阶段 |
| `/math-modeling stage N` | 进入指定阶段 |
| `/math-modeling skip 6 --reason "..."` | 跳过阶段6独立验证 |
| `/math-modeling innovate` | 进入创新设计阶段 |
| `/math-modeling innovation review` | 审查当前创新点是否可落地 |
| `/math-modeling innovation compare` | 生成基线与创新模型对比计划 |
| `/math-modeling review` | 执行阶段9图片审查 |
| `/math-modeling export` | 生成论文素材索引 |
| `/math-modeling reset stage N` | 重置指定阶段状态 |
| `/math-modeling outputs` | 查看所有阶段产出物 |
| `/math-modeling status` | progress 的别名 |

## 10 阶段 Checklist

| # | 阶段 | 产出物 | 可跳过 |
|---|------|--------|--------|
| 1 | 审题定类 | 问题分类标签、子问题拆解、目标输出、约束条件 | 否 |
| 2 | 算法选型 | 每个子问题候选算法 2-3 个、推荐理由、风险 | 否 |
| 3 | 创新设计 | 创新点候选、创新路径、基线对比方案、可行性评分 | 否 |
| 4 | 建模 | 变量、假设、符号表、方程、目标函数、约束 | 否 |
| 5 | 求解实现 | Python 主求解代码、结果文件、运行日志 | 否 |
| 6 | 独立验证 | MATLAB 或其他方式复现，对比误差/一致性说明 | 是，需记录原因 |
| 7 | 敏感性分析 | 参数扰动表、敏感性指标、敏感性图、结论 | 否 |
| 8 | 可视化 | PNG + CSV + meta.json + 绘图脚本 | 否 |
| 9 | 图片审查 | 格式 review、内容 review、重绘建议 | 否 |
| 10 | 成文准备 | figure_index、table_index、model_summary、innovation_summary、caption 检查 | 否 |

## 执行逻辑

### ON_INVOKE

1. 检查项目目录下是否存在 `modeling_state.yaml`
   - 存在 → 加载状态并校验
   - 不存在 → 询问是否初始化新项目（执行 init）
2. 显示 checklist 当前状态（表格形式，高亮未完成/需修订/需人工确认的阶段）
3. 输出推荐下一阶段
4. 等待用户选择

### ON_STAGE_ENTER(stage_n)

1. 加载 `modeling_state.yaml`
2. 检查推荐依赖是否完成（见依赖表）
3. 若依赖缺失，提示用户确认（不强制阻断）
4. 更新阶段状态为 `IN_PROGRESS`
5. 根据阶段读取 references 文件：
   - 阶段3 → `references/innovation-design.md`
   - 阶段7 → `references/sensitivity-analysis.md`
   - 阶段8 → `references/caption-spec.md`（生成 meta.json）
   - 阶段9 → `references/figure-review.md` + `references/caption-spec.md`
   - 阶段10 → `references/caption-spec.md`
6. 执行阶段逻辑
7. 检查必需产出物是否存在且格式合规
8. 写入 outputs 路径到状态文件
9. 更新 `quality_status`
10. 若通过 → `DONE`；存在问题 → `NEEDS_REVISION` / `HUMAN_REVIEW_REQUIRED` / `FAILED`
11. 提示下一步建议

### ON_PROGRESS_CHECK

1. 读取 `modeling_state.yaml`
2. 输出阶段状态表
3. 高亮未完成/需修订/需人工确认的阶段
4. 输出下一步推荐

## 阶段依赖（建议，不强制阻断）

| 阶段 | 建议依赖 |
|------|----------|
| 2 算法选型 | 阶段1 |
| 3 创新设计 | 阶段1、2 |
| 4 建模 | 阶段1、2、3 |
| 5 求解 | 阶段4 |
| 6 独立验证 | 阶段5 |
| 7 敏感性 | 阶段5 |
| 8 可视化 | 阶段5、7 |
| 9 审查 | 阶段8 |
| 10 成文 | 阶段9 |

## 状态管理

### modeling_state.yaml Schema

```yaml
project_name: ""
contest: ""
problem_id: ""
created_at: ""
updated_at: ""
skill_version: "math-modeling@1.0.0"
state_version: "1.0"
current_stage: null

problem_decomposition: {}

stages:
  1_problem_understanding:
    status: "NOT_STARTED"       # NOT_STARTED|IN_PROGRESS|DONE|SKIPPED|NEEDS_REVISION|HUMAN_REVIEW_REQUIRED|FAILED
    quality_status: "UNKNOWN"   # UNKNOWN|PASS|PASS_WITH_WARNINGS|NEEDS_REVISION|FAILED
    required: true
    skippable: false
    outputs: []
  # ... (10 stages total, see init template)
```

### 状态枚举

| 状态 | 含义 |
|------|------|
| NOT_STARTED | 尚未开始 |
| IN_PROGRESS | 正在执行 |
| DONE | 已完成 |
| SKIPPED | 已跳过（仅阶段6，需 skip_reason） |
| NEEDS_REVISION | 需要修订，可自动或人工回退 |
| HUMAN_REVIEW_REQUIRED | 自动流程不确定，需用户确认 |
| FAILED | 执行失败或产出物不可用 |

### 状态流转

```
NOT_STARTED → IN_PROGRESS → DONE
                           → SKIPPED（仅阶段6）
                           → NEEDS_REVISION → IN_PROGRESS（回退重做）
                           → HUMAN_REVIEW_REQUIRED（等待用户）
                           → FAILED

阶段8/9循环：
  8 DONE → 9 IN_PROGRESS → REVISE_REQUIRED → 8 NEEDS_REVISION → 8 IN_PROGRESS → ...
  超过 max_auto_revisions(2) → HUMAN_REVIEW_REQUIRED
```

## 工具选择策略

```yaml
tool_policy:
  optimization:
    primary: "Nextmv MCP"
    fallback: ["Python scipy.optimize / pulp / ortools", "MATLAB Optimization Toolbox"]
  pde_ode:
    primary: "MATLAB MCP"
    fallback: ["Python scipy.integrate / scipy.sparse"]
  prediction_evaluation_classification:
    primary: "Jupyter MCP"
    fallback: ["Python script in code/python/"]
  visualization:
    primary: "Python viz_utils"
    fallback: ["MATLAB MCP (3D/contour等特殊图)"]
  cross_validation:
    primary: "MATLAB MCP"
    fallback: ["independent Python implementation", "manual sanity check"]
```

工具不可用时不中断流程，记录 fallback_reason 并使用备用方案。

## 资源编排

| 现有资源 | 角色 |
|----------|------|
| `数学建模算法库.md` | 阶段2 算法选型时查阅 |
| `templates/python/` | 阶段5 求解时推荐模板 |
| `templates/matlab/` | 阶段6 验证时推荐模板 |
| `viz_utils.py` / `.m` | 阶段8 强制使用（PNG+CSV+meta.json） |
| MATLAB MCP | 阶段6 验证 + 阶段8 特殊图 |
| Jupyter MCP | 阶段5 探索求解 + 阶段7 敏感性 |
| Nextmv MCP | 阶段5 运筹优化类求解 |

## 质量门控

每阶段完成前必须检查：
- 必需产出物文件是否存在
- 格式是否符合 schema
- 是否可被后续阶段读取
- 是否记录在 modeling_state.yaml 的 outputs 字段

## 输出协议

所有阶段产出物必须：
- 写入约定目录（见项目目录结构）
- 记录到 modeling_state.yaml 的 outputs 字段
- 必要时包含 meta 信息（JSON）
- 支持后续阶段直接读取

## 可视化输出协议

阶段8必须通过 viz_utils 或兼容接口完成，确保每张图同时生成：
- 图像文件：`fig_xx.png`（DPI ≥ 300）
- 图数据：`fig_xx.csv`
- 元信息：`fig_xx.meta.json`

## 行为规则

1. **Checklist 模式**：用户可乱序执行，skill 追踪完成状态
2. **自动推荐**：每个阶段完成后提示下一个未完成阶段
3. **进度可查**：用户可随时查看哪些阶段已完成、哪些待做
4. **状态分级**：7种状态枚举，见上方
5. **允许回退**：图片审查失败可回到可视化阶段
6. **跳过需记录**：所有跳过操作必须记录 skip_reason
7. **产出物追踪**：所有关键产出物记录文件路径、生成时间、依赖输入
8. **重绘限制**：阶段8/9循环最多自动重绘2次，超过转人工
9. **创新贯穿**：创新点在阶段3设计后，在求解、验证、敏感性、成文阶段持续追踪
10. **创新证据链**：每个 selected innovation 必须在后续阶段生成至少一个 evidence_output；无证据的创新点不得作为主要创新写入论文

## 项目目录结构

`/math-modeling init` 生成：

```
新赛题目录/
├── CLAUDE.md
├── README.md
├── .gitignore
├── modeling_state.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   ├── innovation/
│   ├── results/
│   ├── validation/
│   ├── sensitivity/
│   ├── figures/
│   ├── reviews/
│   └── paper/
├── code/
│   ├── python/
│   │   ├── __init__.py
│   │   ├── utils.py
│   │   └── main.py
│   └── matlab/
│       └── main.m
└── logs/
```

## 各阶段详细规则

### 阶段1 审题定类

产出 `data/problem_analysis.yaml`：
```yaml
problem_analysis:
  overall_type: "综合建模"
  subproblems:
    Q1: ["评价", "统计分析"]
    Q2: ["预测"]
  known_data: []
  unknowns: []
  constraints: []
  objectives: []
  difficulties: []
  evaluation_metrics: []
```

### 阶段2 算法选型

产出 `data/algorithm_selection.yaml`，每个子问题 2-3 个候选算法，含 rank、reason、assumptions、risks。查阅 `数学建模算法库.md` 匹配。

### 阶段3 创新设计

→ 读取 `references/innovation-design.md`

产出 4 个文件到 `data/innovation/`：
- `innovation_design.yaml`
- `innovation_scorecard.md`
- `baseline_comparison_plan.md`
- `innovation_summary.md`

### 阶段4 建模

产出 `data/model_spec.yaml`，必须区分 baseline model 与 innovative model。

### 阶段5 求解实现

产出到 `data/results/` + `code/python/`。原则上对主创新点实现 baseline 与 innovative 对比。

### 阶段6 独立验证

可跳过，但需 skip_reason。默认 MATLAB MCP，备选：Python 第二实现、手算验证、sanity check。

### 阶段7 敏感性分析

→ 读取 `references/sensitivity-analysis.md`

产出到 `data/sensitivity/`：sensitivity_table.csv、sensitivity_plot.png、sensitivity_conclusion.md、sensitivity_meta.json。优先覆盖创新点相关参数。

### 阶段8 可视化

→ 读取 `references/caption-spec.md`

强制使用 viz_utils，每张图同时生成 PNG + CSV + meta.json。

### 阶段9 图片审查

→ 读取 `references/figure-review.md` + `references/caption-spec.md`

格式检查 + 内容合理性判断。状态：PASS / PASS_WITH_WARNINGS / REVISE_REQUIRED / HUMAN_REVIEW_REQUIRED / FAIL。

### 阶段10 成文准备

产出到 `data/paper/`：figure_index.md、table_index.md、model_summary.md、innovation_summary.md（从 data/innovation/ 汇总）。
