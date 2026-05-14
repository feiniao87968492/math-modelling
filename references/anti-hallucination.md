# 反幻觉规则 — Anti-Hallucination Rules

## 核心原则

数学建模中最易产生幻觉的环节：题意误读、凭空补充约束、数据字段含义猜错、模型假设无来源、结果趋势强行解释、创新点无法验证、未验证内容写成结论。

本文件定义强制规则以对抗这些幻觉。

## 通用规则

1. **不得凭空添加数据字段或约束** — 所有变量、参数、约束必须源自题面、数据或经用户确认的假设
2. **不得在未检查数据范围前解释趋势** — 先描述数据特征，再基于数据建模
3. **不得把未验证的创新点写成论文主要贡献** — 创新点必须有 baseline 对比或消融实验证据
4. **所有结论必须指向证据** — 结论必须绑定结果文件、图表、统计检验或事实来源
5. **不确定信息必须标记** — 对模糊的题目信息、数据含义、参数取值，建立 assumption 并标记是否需要用户确认
6. **不得伪造来源** — 不得编造不存在的题面页码、附件字段、论文引用、文件路径或运行结果。若无法访问原始来源，必须标记为 UNKNOWN 或 USER_CONFIRMATION_REQUIRED
7. **来源必须可检查** — 所有 source_file、evidence_file、result_file 必须是项目目录中真实存在的文件；如果只是计划生成，状态必须标记为 PLANNED，不得标记为 evidence

## 事实锚定规则

任何模型假设、约束、变量定义、结论解释都必须链接到至少一个 `fact_id`、`assumption_id` 或结果文件。没有依据的内容不得写入主要结论。

### 事实级别

| 级别 | 含义 | 示例 |
|------|------|------|
| FACT | 题面或附件明确给出 | "附件表1包含2019-2023年30个省份的指标数据" |
| DERIVED | 从数据统计或简单计算得出 | "数据缺失率约3.2%，采用中位数插补" |
| ASSUMPTION | 合理推断，需用户确认 | "假设运输成本与距离成正比" |
| UNKNOWN | 不确定信息，待定 | "题目未说明异常值处理方式" |

### 事实文件 Schema

#### `data/facts/problem_facts.yaml`

```yaml
facts:
  - id: "fact_001"
    level: "FACT"              # FACT|DERIVED|ASSUMPTION|UNKNOWN
    content: "附件1包含2019-2023年各地区指标数据"
    source_type: "problem_statement"  # problem_statement|data_file|derived|user_confirmed
    source_file: "data/raw/problem_statement.pdf"
    location: "page 2 paragraph 3"
    confidence: "HIGH"         # HIGH|MEDIUM|LOW
    used_by:
      - "stage_1"
      - "stage_2"

unknown_or_ambiguous:
  - id: "amb_001"
    issue: "题目未明确缺失值处理方式"
    proposed_handling: "采用中位数插补，并在敏感性分析中验证"
    requires_user_confirmation: false
```

#### `data/facts/assumptions.yaml`

```yaml
assumptions:
  - id: "assumption_001"
    content: "缺失值采用中位数插补"
    basis:
      - "fact_005"
      - "data/facts/missing_values.yaml"
    requires_user_confirmation: false
    status: "ACTIVE"           # PROPOSED|ACTIVE|REJECTED
    used_in:
      - "data/model_spec.yaml"
```

#### `data/facts/constraints_registry.yaml`

```yaml
constraints:
  - id: "constraint_001"
    content: "所有分配变量必须非负"
    source_level: "MODEL_REQUIRED"  # PROBLEM_GIVEN|DATA_DERIVED|ASSUMPTION|MODEL_REQUIRED
    source:
      - "assumption_002"
    mathematical_form: "x_ij >= 0"
    used_in:
      - "data/model_spec.yaml"
      - "code/python/main.py"
```

## 阶段级规则

### 阶段1 审题

- 必须区分"题面明确给出"和"我推断的"
- 对每个子问题，明确列出输入、输出、评价标准
- 如果题目目标含糊，给出可执行解释并标记为 assumption

### 阶段2 算法选型

- 每个算法推荐必须有数据特征或题意目标的理由
- 不得推荐与问题类型无关的复杂算法

### 阶段3 创新设计

- 创新点必须与题面目标相关（grounding_score ≥ 3）
- 创新点必须说明 baseline 是什么
- 声称"效果好"必须说明如何验证

### 阶段4 建模

- 每个变量必须有单位、含义、取值范围
- 每个约束必须说明来源：题目明确、数据推导、合理假设、模型需要
- baseline model 必须足够简单且可复现

### 阶段5 求解

- 硬编码路径不允许
- 随机种子必须固定
- 结果必须记录运行参数

### 阶段7 敏感性

- 敏感参数必须解释来源
- 扰动范围必须有依据

### 阶段10 成文

- "显著"、"明显优于"、"鲁棒"等词必须有指标支撑
- 创新点必须有对比实验或消融实验证据
- 图注必须包含变量、单位和参数条件
- 无证据的 claim 不得写入论文主结论
