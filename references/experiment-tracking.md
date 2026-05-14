# 实验追踪与归因 — Experiment Tracking

## 概述

每次模型改动、参数调整、数据处理变化都记录到 experiment_log。创新点必须通过 baseline 对比、消融实验或敏感性证据证明有效，避免无法解释的结果提升。

## 目录结构

```
experiments/
├── experiment_log.yaml       ← 主日志
├── ablation_studies/         ← 消融实验
├── run_001/                  ← 每次运行记录
├── run_002/
└── metric_history.csv        ← 指标历史汇总
```

## experiment_log.yaml Schema

```yaml
experiments:
  - run_id: "run_001"
    timestamp: "2026-05-14T10:30:00"
    stage: 5
    change_summary: "使用熵权-TOPSIS baseline"
    code_version: "commit_hash_or_manual_v1"
    input_files:
      - "data/processed/q1_clean.csv"
    output_files:
      - "data/results/result_q1_run001.csv"
    metrics:
      kendall_tau_under_weight_perturbation: 0.82
      rank_flip_count: 5
    notes: "baseline 稳定性一般"

  - run_id: "run_002"
    timestamp: "2026-05-14T11:20:00"
    stage: 5
    change_summary: "加入指标相关性惩罚权重"
    changed_components:
      - "weighting_method"
      - "correlation_penalty_lambda"
    baseline_run: "run_001"
    metrics:
      kendall_tau_under_weight_perturbation: 0.91
      rank_flip_count: 2
    improvement_over_baseline:
      rank_flip_count: "-60%"
    attribution:
      likely_caused_by: "correlation_penalty_lambda"
      evidence: "ablation_studies/q1_lambda_ablation.csv"
```

## 实验记录规范

1. **每次有意义的改动产生一个新 run_id**
   - 包括：算法更换、参数调整、数据处理变化、特征工程
   - 不包括：纯重构、注释添加、代码格式化

2. **每条记录必须包含 baseline_run**
   - 首次可为空（作为全局 baseline）
   - 后续记录必须指向一个可对比的 baseline

3. **指标需与问题类型匹配**

| 题型 | 核心指标 |
|------|----------|
| 评价类 | Kendall τ、rank_flip_count、score 分布 |
| 预测类 | RMSE、MAE、MAPE、R² |
| 优化类 | objective_value、gap、solve_time、约束违反率 |
| PDE | L2_error、max_deviation、收敛时间 |

4. **记录 changed_components**
   - 列出与 baseline_run 相比具体改了哪些组件
   - 方便后续归因分析

## 和创新设计联动

阶段3选中的创新点必须在实验日志中有对应 run_id 或 ablation 证据：

```yaml
selected_innovations:
  - id: "innov_01"
    evidence_runs:
      - "run_002"
      - "run_003_ablation"
```

## 指标历史

`metric_history.csv` 汇总所有实验的核心指标，便于趋势分析：

```csv
run_id,timestamp,kendall_tau,rank_flip_count,rmse,note
run_001,2026-05-14T10:30,0.82,5,,"baseline"
run_002,2026-05-14T11:20,0.91,2,,"correlation_penalty"
```
