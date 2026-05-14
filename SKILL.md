---
name: math-modeling
description: "数学建模标准化工作流。10阶段 checklist 覆盖审题定类、算法选型、创新设计、建模、求解实现、独立验证、敏感性分析、可视化、图片审查、成文准备。支持乱序执行、状态追踪、质量门控、创新证据链。触发词：数学建模、建模流程、新赛题、math-modeling、/math-modeling init、/math-modeling progress、/math-modeling next"
metadata:
  author: zty
  version: 1.2.0
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
| `/math-modeling gate` | 执行 Final Evidence Gate 检查 |
| `/math-modeling facts` | 查看事实库状态 |
| `/math-modeling audit` | 执行数据审计 |
| `/math-modeling experiment` | 查看实验追踪日志 |

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
| 10 | 成文准备 | figure_index、table_index、model_summary、innovation_summary、caption 检查、claim_registry | 否 |

## 横向质量系统

除 10 阶段主流程外，所有阶段必须受以下横向系统约束。它们在各个阶段交叉执行，不独立成阶段。

### 1. Fact Grounding System — 事实锚定系统

每个阶段产生的假设、约束、结论必须锚定到事实来源。参见 `references/anti-hallucination.md`。

核心文件：
- `data/facts/problem_facts.yaml` — 从题面/附件提取的事实
- `data/facts/data_dictionary.yaml` — 数据字段解释、单位、来源
- `data/facts/assumptions.yaml` — 所有建模假设及其依据
- `data/facts/constraints_registry.yaml` — 所有约束条件及来源

### 2. Modeling Memory System — 规则记忆系统

每个阶段开始前读取项目根目录的 `memory.md` 或 skill 内置 `references/modeling-memory-template.md`，将规则作为本阶段额外质量门控。阶段结束后追加新经验。

### 3. Data Audit System — 数据审计系统

对输入数据进行系统性检查：数据字典、缺失值、异常值、单位、重复记录、时间泄露。参见 `references/data-audit.md`。

### 4. Code Review Pipeline — 代码审查流水线

阶段5求解后执行 5 层审查：静态代码检查、数据输入检查、模型逻辑检查、结果 sanity check、复现性检查。参见 `references/code-review-pipeline.md`。

### 5. Experiment Tracking System — 实验追踪系统

每次模型改动、参数调整、数据处理变化记录到 `experiments/experiment_log.yaml`。创新点必须有实验证据。参见 `references/experiment-tracking.md`。

### 6. Claim Grounding System — 结论证据绑定系统

论文中的关键结论必须绑定结果文件、图表、敏感性分析或验证报告。参见 `references/claim-grounding.md`。

### 7. Final Evidence Gate — 终稿证据门控

阶段10前执行门控检查，确保所有阶段完成、所有创新点有证据、所有结论可追溯。参见 `references/evidence-gate.md`。

## 执行逻辑

### ON_INVOKE

1. 检查项目目录下是否存在 `modeling_state.yaml`
   - 存在 → 加载状态并校验
   - 不存在 → 执行 init 流程（见 ON_INIT）
2. 显示 checklist 当前状态（表格形式，高亮未完成/需修订/需人工确认的阶段）
3. 输出推荐下一阶段
4. 等待用户选择

### ON_INIT

初始化时创建完整目录结构和状态文件：

```
新赛题目录/
├── modeling_state.yaml       ← 默认状态（全部 NOT_STARTED + quality_systems UNKNOWN）
├── memory.md                 ← 空文件，用于规则记忆
├── data/
│   ├── raw/                  ← 原始附件
│   ├── processed/            ← 清洗数据
│   ├── facts/                ← 事实锚定
│   ├── innovation/           ← 创新设计产出
│   ├── results/              ← 求解结果 + 代码审查
│   ├── validation/           ← 独立验证
│   ├── sensitivity/          ← 敏感性分析
│   ├── figures/              ← 插图
│   ├── reviews/              ← 审查报告
│   └── paper/                ← 论文素材
├── experiments/
│   ├── ablation_studies/     ← 消融实验
│   └── experiment_log.yaml   ← 空日志
├── code/
│   ├── python/
│   │   ├── __init__.py
│   │   ├── utils.py
│   │   └── main.py
│   └── matlab/
│       └── main.m
└── logs/
```

初始化配置：
- 所有 `stages.*.status = NOT_STARTED`
- 所有 `quality_systems.*.status = UNKNOWN`
- 写入 `skill_version: "math-modeling@1.2.0"`

### ON_STAGE_ENTER(stage_n)

1. 加载 `modeling_state.yaml`
2. 检查推荐依赖是否完成（见依赖表）
3. 若依赖缺失，提示用户确认（不强制阻断）
4. 更新阶段状态为 `IN_PROGRESS`
5. 读取横向质量系统文件（所有阶段通用）：
   - `references/anti-hallucination.md`（反幻觉规则）
   - 规则记忆：优先读取项目根目录 `memory.md`；若不存在则读取 `references/modeling-memory-template.md`
6. 根据阶段读取 references 文件：
   - 阶段1 → `references/anti-hallucination.md`（若原始数据已提供，另读 data-audit.md）
   - 阶段2 → `references/anti-hallucination.md`
   - 阶段3 → `references/innovation-design.md`
   - 阶段5 → `references/code-review-pipeline.md`
   - 阶段7 → `references/sensitivity-analysis.md`
   - 阶段8 → `references/caption-spec.md`（生成 meta.json）
   - 阶段9 → `references/figure-review.md` + `references/caption-spec.md`
   - 阶段10 → `references/claim-grounding.md` + `references/evidence-gate.md` + `references/caption-spec.md`
7. 执行阶段逻辑
8. 检查必需产出物是否存在且格式合规
9. 写入 outputs 路径到状态文件
10. 更新 `quality_status`
11. 若通过 → `DONE`；存在问题 → `NEEDS_REVISION` / `HUMAN_REVIEW_REQUIRED` / `FAILED`
12. 提示下一步建议

### ON_PROGRESS_CHECK

1. 读取 `modeling_state.yaml`
2. 输出阶段状态表
3. 高亮未完成/需修订/需人工确认的阶段，同时显示 quality_systems 状态
4. 输出下一步推荐

### ON_FACTS

1. 检查 `data/facts/` 目录是否创建
2. 汇总各文件状态：

   | 文件 | 状态 |
   |------|------|
   | problem_facts.yaml | 存在 / 缺失 |
   | assumptions.yaml | 存在 / 缺失 |
   | constraints_registry.yaml | 存在 / 缺失 |
   | data_dictionary.yaml | 存在 / 缺失 |

3. 统计事实级别分布：FACT 数量、DERIVED 数量、ASSUMPTION 数量、UNKNOWN 数量
4. 列出需要用户确认的 assumption
5. 若缺失关键文件，建议回到阶段1或执行 `/math-modeling audit`

### ON_AUDIT

1. 读取 `references/data-audit.md`
2. 扫描 `data/raw/` 和 `data/processed/` 目录中的数据文件
3. 生成或更新：
   - `data/facts/data_dictionary.yaml` — 字段名、含义、单位、类型
   - `data/facts/missing_values.yaml` — 缺失值统计与处理策略
   - `data/facts/outliers.yaml` — 异常值判断标准与处理
   - `data/facts/data_version.yaml` — 数据转换步骤与版本记录
4. 更新 `modeling_state.yaml` 中 `quality_systems.data_audit` 的状态

### ON_EXPERIMENT

1. 读取 `experiments/experiment_log.yaml`
2. 输出所有实验运行的摘要表格（run_id、change_summary、核心指标）
3. 显示 baseline 对比关系树状图
4. 检查 selected_innovations 是否有对应的 evidence_runs
5. 对缺失证据的创新点，提示补充实验或消融

### ON_GATE

1. 读取 `references/evidence-gate.md`
2. 若阶段10未进入，执行 **dry-run** 检查，输出阻塞项列表和修复建议，不改变任何阶段状态
3. 若阶段10已进入 IN_PROGRESS，执行正式 Final Evidence Gate（见阶段10 Step 2 规则）
4. 输出或更新 `data/paper/final_evidence_check.md`
5. 更新 `quality_systems.final_evidence_gate` 状态

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
skill_version: "math-modeling@1.2.0"
state_version: "1.2"
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

# 横向质量系统状态追踪
quality_systems:
  fact_grounding:
    status: "UNKNOWN"           # UNKNOWN|PASS|PASS_WITH_WARNINGS|NEEDS_REVISION|FAILED
    files:
      - "data/facts/problem_facts.yaml"
      - "data/facts/assumptions.yaml"
      - "data/facts/constraints_registry.yaml"
      - "data/facts/data_dictionary.yaml"

  data_audit:
    status: "UNKNOWN"
    last_run: null
    outputs: []

  code_review:
    status: "UNKNOWN"
    last_run: null
    report: null

  experiment_tracking:
    status: "UNKNOWN"
    experiment_log: "experiments/experiment_log.yaml"
    last_run_id: null

  claim_grounding:
    status: "UNKNOWN"
    claim_registry: "data/paper/claim_registry.yaml"

  final_evidence_gate:
    status: "UNKNOWN"
    report: "data/paper/final_evidence_check.md"
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

### 子系统状态映射

各子系统（图片审查、Final Gate、Code Review 等）的状态需映射到阶段标准状态：

| 子系统状态 | 阶段 status | quality_status | 说明 |
|---|---|---|---|
| PASS | DONE | PASS | 通过 |
| PASS_WITH_WARNINGS | DONE | PASS_WITH_WARNINGS | 通过但有警告 |
| REVISE_REQUIRED | NEEDS_REVISION | NEEDS_REVISION | 需回退修订 |
| BLOCKED | NEEDS_REVISION | FAILED | 阻塞，不可通过 |
| HUMAN_REVIEW_REQUIRED | HUMAN_REVIEW_REQUIRED | NEEDS_REVISION | 需人工确认 |
| FAIL / FAILED | FAILED | FAILED | 失败 |

关键映射说明：
- **Final Gate BLOCKED** → 阶段10不能进入 Paper Material Export 子步骤
- **图片审查 REVISE_REQUIRED** → 阶段8 NEEDS_REVISION，阶段9 NEEDS_REVISION
- **Code Review ERROR** → 阶段5 NEEDS_REVISION

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
11. **事实锚定**：所有假设、约束、变量定义、结论必须链接 fact_id / assumption_id / 结果文件；无依据内容不得写入主要结论
12. **实验追踪**：每次有意义的改动（算法更换、参数调整、数据处理变化）需记录到 experiment_log.yaml
13. **结论证据绑定**：阶段10生成 claim_registry，所有 main claim 必须绑定 evidence；allowed_strength = "not_allowed" 的 claim 不得进入论文
14. **Final Gate**：阶段10前自动执行证据门控，不通过不得进入成文阶段
15. **经验沉淀**：每阶段结束后检查是否发现新规则、坑点或反例，如有则追加到项目根目录 memory.md

## 项目目录结构

`/math-modeling init` 生成：

```
新赛题目录/
├── CLAUDE.md
├── README.md
├── .gitignore
├── modeling_state.yaml
├── memory.md                    ← 项目级规则记忆，init 时默认创建，可为空
├── data/
│   ├── raw/
│   ├── processed/
│   ├── facts/                   ← 事实锚定：problem_facts、assumptions、constraints_registry
│   ├── innovation/
│   ├── results/                 ← 含 code_review_report + sanity_check + reproducibility
│   ├── validation/
│   ├── sensitivity/             ← 含 innovation_attribution.md
│   ├── figures/
│   ├── reviews/
│   └── paper/                  ← 含 claim_registry.yaml + final_evidence_check.md
├── experiments/                 ← 实验追踪：experiment_log.yaml、ablation_studies/
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

→ 读取 `references/anti-hallucination.md`

若原始数据已提供（`data/raw/` 中已有文件），一并读取 `references/data-audit.md` 执行初步 Data Audit。

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

新增产出到 `data/facts/`：
- `problem_facts.yaml` — 从题面/附件提取的事实，区分 FACT/DERIVED/ASSUMPTION/UNKNOWN
- `assumptions.yaml` — 所有建模假设及其来源依据
- `constraints_registry.yaml` — 所有约束条件及来源（题目明确/数据推导/合理假设）

阶段1完成条件新增：
- 已区分题面明确事实、合理推断、不确定信息
- 所有关键约束均有来源
- 对模糊信息建立 assumption，并标记是否需要用户确认

### 阶段2 算法选型

→ 读取 `references/anti-hallucination.md`

产出 `data/algorithm_selection.yaml`，每个子问题 2-3 个候选算法，含 rank、reason、assumptions、risks。查阅 `数学建模算法库.md` 匹配。

每个算法推荐理由必须包含数据特征或题意目标的证据。算法预选时若 data_dictionary.yaml 尚未生成，可基于 problem_facts.yaml 和题面目标进行，但数据相关证据标记为 UNKNOWN，后续 Data Audit 后可回退修订。

```yaml
evidence:
  data_basis:
    source: "data_dictionary.yaml | problem_facts.yaml | problem_statement"
    data_size: "若已知则填写，否则 UNKNOWN"
    variable_type: "若已知则填写，否则 UNKNOWN"
  objective_match: "对应 problem_analysis.yaml 中的 objective_id"
  constraints_match: ["constraint_001"]
```

### 阶段3 创新设计

→ 读取 `references/innovation-design.md`

产出 4 个文件到 `data/innovation/`：
- `innovation_design.yaml`（含 grounding_score 和 evidence_runs）
- `innovation_scorecard.md`
- `baseline_comparison_plan.md`
- `innovation_summary.md`

筛选规则新增：grounding_score ≥ 3

### 阶段4 建模

产出 `data/model_spec.yaml`，必须区分 baseline model 与 innovative model。

每个模型组件应有来源映射：

```yaml
model_components:
  - id: "eq_001"
    type: "objective_function"
    expression: "min sum(c_ij x_ij)"
    description: "最小化运输成本"
    grounded_in:
      facts: ["fact_003"]
      assumptions: ["assumption_001"]
      constraints: ["constraint_002"]
```

### 阶段5 求解实现

→ 读取 `references/code-review-pipeline.md`

产出到 `data/results/` + `code/python/`。原则上对主创新点实现 baseline 与 innovative 对比。

阶段5完成前必须执行 code review pipeline（5层审查）：

1. **static_code_check** — 随机种子、路径可移植性、异常处理
2. **data_input_check** — 输入文件存在性、行列数、数值范围
3. **model_logic_check** — 目标函数与约束的实现完整性
4. **result_sanity_check** — NaN/Inf、合理范围、约束满足
5. **reproducibility_check** — 固定 seed 复现性

产出新增：
- `data/results/code_review_report.md`（可读报告）
- `data/results/code_review_report.json`（机器可读，供后续阶段自动判定）
- `data/results/result_sanity_check.json`
- `data/results/reproducibility_check.json`

判定规则（读取 code_review_report.json）：
- `blocking_errors > 0` → 阶段5 `NEEDS_REVISION`
- `overall_status = PASS_WITH_WARNINGS` → 阶段5 DONE + quality_status `PASS_WITH_WARNINGS`

阶段5完成前必须存在（Data Audit 前置要求）：
- `data/facts/data_dictionary.yaml`
- `data/facts/data_version.yaml`
若存在结构化数据，还应存在：
- `data/facts/missing_values.yaml`
- `data/facts/outliers.yaml`

Data Audit 执行时机：
1. 阶段1：若原始数据已提供，执行初步检查
2. 阶段5前：必须完成完整 Data Audit，否则阶段5不能 DONE
3. 用户可随时通过 `/math-modeling audit` 手动执行

### 阶段6 独立验证

可跳过，但需 skip_reason。默认 MATLAB MCP，备选：Python 第二实现、手算验证、sanity check。

### 阶段7 敏感性分析

→ 读取 `references/sensitivity-analysis.md`

产出到 `data/sensitivity/`：sensitivity_table.csv、sensitivity_conclusion.md、sensitivity_meta.json。

若敏感性图将用于论文，需符合阶段8/9可视化协议，生成到 `data/figures/` 并注册 meta.json：

```text
data/figures/fig_sensitivity_qx.png
data/figures/fig_sensitivity_qx.csv
data/figures/fig_sensitivity_qx.meta.json
```

`sensitivity_meta.json` 中引用图路径：
```json
{
  "sensitivity_figure": "data/figures/fig_sensitivity_q2.png"
}
```

优先覆盖创新点相关参数。

新增产出：`data/sensitivity/innovation_attribution.md`

回答核心问题：哪些改动真的带来提升？

```markdown
# Innovation Attribution

| 创新点 | baseline 指标 | innovative 指标 | 改善幅度 | 证据文件 | 可信度 |
|--------|-------------|----------------|---------|---------|--------|
| 指标相关性惩罚 | rank_flip=5 | rank_flip=2 | -60% | q1_ablation.csv | HIGH |
```

### 阶段8 可视化

→ 读取 `references/caption-spec.md`

强制使用 viz_utils，每张图同时生成 PNG + CSV + meta.json。

### 阶段9 图片审查

→ 读取 `references/figure-review.md` + `references/caption-spec.md`

格式检查 + 内容合理性判断。状态：PASS / PASS_WITH_WARNINGS / REVISE_REQUIRED / HUMAN_REVIEW_REQUIRED / FAIL。

### 阶段10 成文准备

→ 读取 `references/claim-grounding.md` + `references/evidence-gate.md`

阶段10内部严格按三步顺序执行，避免循环依赖：

**Step 1: Claim Drafting — 生成草稿 claim registry**

从前 9 阶段产出中提取论文关键结论候选，生成 `data/paper/claim_registry.yaml`。此步骤仅收集已有证据、不执行门控判断。

**Step 2: Final Evidence Gate — 执行终稿证据门控**

读取 `claim_registry.yaml`、`modeling_state.yaml`、`innovation_design.yaml`、`data/reviews/*.json`，执行门控检查：

- 阶段1-5 必须 DONE
- 阶段6 若 SKIPPED，必须有 skip_reason
- 阶段7 必须 DONE
- 阶段8 必须 DONE
- 阶段9 所有图必须 PASS 或 PASS_WITH_WARNINGS
- 所有 selected innovations 至少有 1 个 evidence_output 文件存在且非空，或至少 1 个 evidence_runs 可在 experiment_log.yaml 中找到
- 所有主要结论必须能追溯到 result 文件、figure、table、sensitivity 或 validation
- 所有假设必须记录在 assumptions.yaml

输出 `data/paper/final_evidence_check.md`。

Gate 状态：
- `PASS` / `PASS_WITH_WARNINGS` → 进入 Step 3
- `BLOCKED` → 阶段10设为 `NEEDS_REVISION`，修复后重试

**Step 3: Paper Material Export — 导出论文素材**

仅当 Gate PASS 或 PASS_WITH_WARNINGS 时执行：
- `figure_index.md`
- `table_index.md`
- `model_summary.md`
- `innovation_summary.md`（从 data/innovation/ 汇总，仅含 evidence 充分的创新点）
