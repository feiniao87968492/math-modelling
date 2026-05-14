# 结论证据绑定 — Claim Grounding

## 核心原则

论文中的关键结论必须绑定结果文件、图表、敏感性分析或验证报告。无证据结论自动标记为不可写入。

## Claim Registry Schema

阶段10生成 `data/paper/claim_registry.yaml`：

```yaml
claims:
  - id: "claim_001"
    text: "改进模型相较基线模型提高了排名稳定性"
    claim_type: "innovation_effectiveness"
    evidence:
      - "data/results/baseline_vs_innovative_comparison.csv"
      - "data/sensitivity/sensitivity_table.csv"
    allowed_strength: "strong"

  - id: "claim_002"
    text: "模型对权重扰动具有较强鲁棒性"
    claim_type: "robustness"
    evidence:
      - "data/sensitivity/sensitivity_conclusion.md"
    allowed_strength: "moderate"

  - id: "claim_003"
    text: "该方法适用于所有类似城市评价问题"
    claim_type: "generalization"
    evidence: []
    allowed_strength: "not_allowed"
    issue: "缺少跨数据集验证，不允许写入论文"
```

## claim_type 可选值

| 类型 | 含义 |
|------|------|
| innovation_effectiveness | 创新点有效性 |
| model_performance | 模型性能 |
| robustness | 鲁棒性 |
| ranking_result | 排名/评价结果 |
| prediction_result | 预测结果 |
| optimization_result | 优化结果 |
| interpretability | 可解释性 |
| generalization | 泛化能力 |

## allowed_strength 规则

| 强度 | 论文表达限制 | 证据要求 |
|------|-------------|----------|
| strong | 可使用"显著提高""大幅优于" | ≥ 2 个独立证据来源 |
| moderate | 可使用"优于""相对提升" | ≥ 1 个证据来源 |
| weak | 仅可写"初步表明""建议进一步研究" | 有指向性证据但不够强 |
| not_allowed | 不得写入论文主结论 | 无证据或证据不相关 |

## 执行规则

1. 阶段10 Step 1（Claim Drafting）时，从所有阶段产出物自动生成 claim 候选
2. 每个可写入论文主结论的 claim 必须至少有一个 evidence 路径
3. 若 claim 无 evidence 或证据不相关，则 allowed_strength 必须设为 `not_allowed`，并记录 issue
4. evidence 指向的文件必须存在且内容非空
5. allowed_strength 由证据数量和类型自动判定
6. allowed_strength = "not_allowed" 的 claim 不得进入论文主结论
7. claim 汇总到 `data/paper/claim_registry.yaml`
