# 创新点生成与筛选规则

## 核心原则

创新模块不是"生成亮点文案"，而是连接算法选型、建模、求解、验证和论文表达的中间层。每个创新点都必须有 baseline、有实现路径、有验证方式、有论文表达价值。

## 创新方向按题型匹配

| 题型 | 常规方法 | 推荐创新方向 |
|------|----------|-------------|
| 评价类 | 熵权法、TOPSIS、AHP | 动态组合权重、鲁棒排序、指标相关性修正 |
| 预测类 | ARIMA、LSTM、随机森林 | 分解-预测-集成、外生变量融合、不确定性区间预测 |
| 优化类 | LP、MILP、遗传算法 | 分层优化、鲁棒优化、多目标Pareto、启发式加速 |
| PDE/ODE | 数值差分、有限元 | 参数反演、边界条件自适应、数据同化 |
| 分类聚类 | KMeans、SVM、RF | 特征构造、稳定性聚类、可解释性增强 |

## 7 类创新详细规则

### 1. 模型结构创新
适用：优化/预测/方程/综合。方向：单一→分层、静态→动态、确定性→随机/鲁棒、单目标→多目标、经验→机理-数据融合。

### 2. 算法组合创新
适用：预测/评价/分类/优化。必须说明组合的必要性，不是简单堆算法。示例：ARIMA 捕捉线性趋势 + LSTM 捕捉非线性波动 + 验证误差加权集成。

### 3. 指标体系创新
适用：评价类。方向：新增贴合题意的二级指标、指标相关性惩罚、主客观组合权重、动态权重、鲁棒排序。

### 4. 约束条件创新
适用：优化类。方向：现实约束、公平性约束、容量/安全/时间窗/预算约束、软约束惩罚、鲁棒约束。

### 5. 数据处理与特征工程创新
适用：预测/分类/评价/聚类。方向：异常值识别、缺失值插补、时间序列分解、空间/滞后/交互特征构造、归一化策略比较。

### 6. 鲁棒性与不确定性创新
适用：所有题型。方向：参数扰动鲁棒性、数据噪声鲁棒性、区间预测、蒙特卡洛模拟、鲁棒优化、情景分析。

### 7. 可解释性与可视化表达创新
适用：所有题型。方向：SHAP/特征重要性、Pareto前沿图、敏感性龙卷风图、决策路径图、不确定性区间图、方案对比雷达图。

## 创新评分维度

| 维度 | 含义 | 分值 |
|------|------|------|
| novelty_score | 与常规方法相比是否有新意 | 1-5 |
| relevance_score | 是否紧扣题目目标 | 1-5 |
| feasibility_score | 是否能在竞赛时间内实现 | 1-5 |
| validation_score | 是否能通过实验/对比证明有效 | 1-5 |
| paper_value_score | 是否适合写进论文作为亮点 | 1-5 |
| risk_score | 实现失败或逻辑牵强的风险 | 1-5 |

## 综合评分公式

```
innovation_total = 0.22*novelty + 0.22*relevance + 0.18*feasibility
                 + 0.18*validation + 0.15*paper_value + 0.05*(6-risk)
```

其中 `6-risk_score` 将风险转换为正向安全性评分。总分近似在 1-5 区间，用于候选创新点相对排序。

## 筛选规则

优先选择满足以下条件的创新点：
- novelty_score ≥ 3
- feasibility_score ≥ 3
- validation_score ≥ 3
- paper_value_score ≥ 4
- risk_score ≤ 3

## innovation_design.yaml Schema

```yaml
innovation_design:
  project: "赛题名称"
  created_at: "ISO时间"

  baseline_methods:
    Q1: ["算法A", "算法B"]
    Q2: ["算法C"]

  innovation_candidates:
    - id: "innov_01"
      problem: "Q1"
      type: "创新类型（7类之一）"
      name: "创新点名称"
      description: "创新点描述"
      baseline: "对照的常规方法"
      expected_benefit: "预期收益"
      implementation_difficulty: 1-5
      novelty_score: 1-5
      relevance_score: 1-5
      feasibility_score: 1-5
      validation_score: 1-5
      paper_value_score: 1-5
      risk_score: 1-5
      innovation_total: 计算值
      comparison_method: "见下方可选值"
      evidence_outputs:
        - "data/results/comparison_q1.csv"
        - "data/figures/fig_innovation.png"
      risk: "风险描述"
      validation_plan:
        - "验证步骤1"
        - "验证步骤2"

  selected_innovations: ["innov_01"]
  rejected_innovations:
    - id: "innov_03"
      reason: "拒绝原因"
```

## comparison_method 可选值

| 值 | 含义 |
|----|------|
| baseline_vs_innovative_result | 基线与创新结果直接对比 |
| ablation_study | 消融实验 |
| sensitivity_evidence | 敏感性分析证据 |
| robustness_test | 鲁棒性测试 |
| case_comparison | 案例对比 |
| visual_explanation | 可视化解释 |
| qualitative_argument | 定性论证 |

## 阶段3 完成条件（质量门控）

- 每个核心子问题至少 1 个可行创新点，或说明不适合创新的原因
- 每个创新点必须有 baseline 对照
- 每个创新点必须有验证方案（validation_plan）
- 每个创新点必须有风险说明
- 至少选择 1-2 个主创新点进入后续建模

## 创新对后续阶段的影响

- **阶段4建模**：必须区分 baseline model 与 innovative model
- **阶段5求解**：原则上对主创新点实现 baseline 与 innovative 对比；不适用时说明 comparison_method
- **阶段6验证**：验证创新模型是否真的带来改进
- **阶段7敏感性**：优先覆盖创新点相关参数（如惩罚系数λ、不确定性半径Γ、集成权重α）
- **阶段10成文**：输出 innovation_summary.md，汇总创新证据链
