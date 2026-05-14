---
name: math-modeling
description: "数学建模竞赛标准化工作流。10阶段 checklist。**触发场景：用户在任何建模项目目录下开始新赛题、审题、算法选型、创新设计、求解实现、敏感性分析、可视化、论文准备。关键词：数学建模、建模流程、竞赛、CUMCM、MCM、泰迪杯、MathorCup、新赛题、/math-modeling。即使用户只说'开始做题'或'第一步做什么'，也应主动调用此 skill 检查进度。**"
metadata:
  author: zty
  version: 1.1.0
  created: 2026-05-13
  last_reviewed: 2026-05-14
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

### ON_INIT

1. 创建 `modeling_state.yaml` 基础结构
2. **自动检测已有文件**：
   - 若 `CLAUDE.md` 存在 → 读取并预填 `project_name`、`problem_id`、`contest`（从标题/元信息提取）
   - 若 `data/problem_analysis.yaml` 存在 → 标记阶段1为 DONE，记录 outputs
   - 若 `data/algorithm_selection.yaml` 存在 → 标记阶段2为 DONE
   - 若 `data/innovation/innovation_design.yaml` 存在 → 标记阶段3为 DONE
   - 若 `data/model_spec.yaml` 存在 → 标记阶段4为 DONE
   - 若 `data/results/` 下有结果文件 → 标记阶段5为 DONE（需用户确认是否完整）
3. 对检测到的已完成阶段，设置 `quality_status: PASS_WITH_WARNINGS`（提示用户确认）
4. 输出检测摘要："检测到阶段 X-Y 已有产出物，已自动标记。请确认是否需要重新执行。"
5. 创建缺失目录结构

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
    primary: "Gurobi (gurobipy)"
    fallback: ["Python scipy.optimize / pulp / ortools", "MATLAB Optimization Toolbox"]
    selection_criteria:
      - MILP with >1000 vars: "Gurobi"
      - LP/small MILP: "scipy.optimize.linprog / pulp"
      - NLP: "scipy.optimize.minimize"
  pde_ode:
    primary: "MATLAB MCP"
    fallback: ["Python scipy.integrate / scipy.sparse / fenics"]
  prediction:
    primary: "Python (lightgbm / scikit-learn / statsmodels)"
    fallback: ["MATLAB MCP"]
    time_series: "statsmodels.tsa + lightgbm"
    classification: "scikit-learn"
  visualization:
    primary: "Python matplotlib + seaborn"
    fallback: ["MATLAB MCP (3D/contour/heatmap)"]
  cross_validation:
    primary: "Python sklearn.model_selection / manual script"
    fallback: ["MATLAB MCP"]
```

工具不可用时不中断流程，记录 fallback_reason 并使用备用方案。

## 资源编排

| 现有资源 | 角色 |
|----------|------|
| `数学建模算法库.md` | 阶段2 算法选型时查阅 |
| `templates/python/` | 阶段5 求解时推荐模板 |
| `viz_utils.py` | 阶段8 强制使用（PNG+CSV+meta.json） |
| MATLAB MCP | 阶段6 验证 + 阶段8 特殊图（3D/contour） |
| Gurobi | 阶段5 MILP/LP 优化求解主力 |
| scikit-learn / lightgbm | 阶段5 预测类求解主力 |

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

#### 求解器选择逻辑

| 问题类型 | 推荐求解器 | 条件 |
|----------|------------|------|
| MILP（混合整数线性规划） | Gurobi | 变量数 > 1000 或有复杂约束 |
| MILP（小型） | pulp / ortools | 变量数 < 1000 |
| LP（线性规划） | scipy.optimize.linreg | 简单 LP |
| NLP（非线性规划） | scipy.optimize.minimize | 无约束或简单约束 |
| PDE/ODE | MATLAB / scipy.integrate | 数值求解 |

#### Warm Start 策略

对于优化类问题，推荐 warm start 加速收敛：

1. **贪心启发式** → 快速生成初始解
2. **松弛求解** → LP 松弛 → 固定整数变量 → 剩余 LP
3. **传递给求解器** → Gurobi `.setSolution()` / pulp `.setInitialValue()`

示例：
```python
# 贪心初始解
init_sol = greedy_heuristic(data)
model.setSolution(init_sol)
model.optimize()
```

#### 代码规范

- **严格类型**：函数签名含返回类型，变量含类型注释
- **纯函数**：只修改返回值，不修改输入参数或全局状态
- **错误处理**：仅处理外部 API / 用户输入边界，不处理不可能场景
- **无默认参数**：所有参数显式传入
- **DRY/KISS/YAGNI**：不写重复代码、不写过度抽象、不写未请求功能

#### 执行流程

1. 读取 `data/model_spec.yaml` 获取模型定义
2. 选择求解器（按上表）
3. 检查是否需要 warm start（优化类）
4. 编写求解代码到 `code/python/q{N}_solution.py`
5. 执行并保存结果到 `data/results/result_q{N}.csv`
6. 记录运行日志到 `logs/run_q{N}.log`
7. 若有创新点对比 → 生成 `data/results/baseline_vs_innov_q{N}.csv`

#### 质量门控

- [ ] 代码可执行无报错
- [ ] 结果文件存在且格式正确（CSV/YAML）
- [ ] 优化问题：检查收敛状态（Gurobi `model.status == GRB.OPTIMAL`）
- [ ] 预测问题：检查指标是否合理（WAPE/MAPE/RMSE 有值）
- [ ] 创新对比：baseline 与 innovative 结果均有

#### 输出文件 Schema

`data/results/result_q{N}.csv`：
```csv
# 基础结果：决策变量值 / 预测值
var_name,value,unit
x1,100,件
...
```

`data/results/baseline_vs_innov_q{N}.csv`（如有创新对比）：
```csv
method,metric_name,metric_value
baseline,obj_value,1000
innovative,obj_value,950
baseline,run_time_sec,5.2
innovative,run_time_sec,3.8
```

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
