# 敏感性分析策略库

## 自动策略选择

根据阶段1确定的题目类型，自动匹配敏感性分析策略。

| 题目类型 | 扰动对象 | 扰动方式 | 评价指标 |
|----------|----------|----------|----------|
| 评价类（AHP/TOPSIS/熵权法） | 权重 w_i | 单个 ±10%/±20% 后归一化；或 Dirichlet 随机扰动 | 排名翻转次数、Kendall τ |
| 优化类（LP/MILP/NLP） | 目标系数、约束右端项 | ±10%/±20% | 最优值变化率、决策变量变化率、活跃约束变化、方案是否切换 |
| PDE/ODE 类 | 物理参数 + 数值参数（Δt、Δx） | ±10%/±20% + 网格加密 | 最大偏差、L2误差、稳态值变化、收敛时间 |
| 预测类（普通） | 训练集划分 | K-fold / repeated split | RMSE/MAE/R² 的变异系数 |
| 预测类（时间序列） | 窗口划分 | 滚动窗口 / expanding window | RMSE/MAE/MAPE 均值和标准差 |
| 分类类 | 特征噪声、超参数 | ±5%/±10% 噪声、bootstrap | F1/AUC/混淆矩阵变化 |
| 聚类类 | 聚类数k、初始中心、标准化方式 | k±1、多次随机初始化 | 轮廓系数、ARI/NMI 稳定性 |

## 评价类权重扰动归一化规则

1. 选定某个权重 w_i
2. 令 w_i' = w_i × (1 + δ)，其中 δ ∈ {-0.2, -0.1, +0.1, +0.2}
3. 对 w' 重新归一化使 sum(w') = 1
4. 重新计算综合得分和排序
5. 记录排名变化

或采用 Dirichlet 随机扰动生成多组合法权重，统计排名稳定性。

## 优化类补充指标

除最优值变化率外，还应检查：
- 决策变量变化率
- 活跃约束是否改变
- 可行性是否丧失
- 最优方案是否切换（方案级变化比数值变化更重要）

## PDE/ODE 类补充

除物理参数外，还应检查数值参数敏感性：
- 时间步长 Δt 减半/加倍
- 空间步长 Δx 减半/加倍
- 网格密度加倍

确保数值解不是"网格伪影"。

## 预测类区分

- 普通回归/分类预测：K-fold 或 repeated train/test split
- 时间序列预测：滚动窗口 / expanding window（不可随机划分，避免数据泄露）

## 创新参数优先

若阶段3选定了创新点，敏感性分析应优先覆盖创新相关参数：
- 相关性惩罚系数 λ
- 鲁棒优化不确定性半径 Γ
- 集成模型权重 α
- 聚类数 k
- 特征选择阈值

## 标准输出

| 文件 | 内容 |
|------|------|
| `data/sensitivity/sensitivity_table.csv` | 参数名、扰动值、输出指标值 |
| `data/sensitivity/sensitivity_conclusion.md` | 一段话总结哪些参数敏感 |
| `data/sensitivity/sensitivity_meta.json` | 扰动设置元信息 |
| `data/figures/fig_sensitivity_qx.png` | 若用于论文，按阶段8规范生成（含 CSV + meta.json） |
| `data/figures/fig_sensitivity_qx.csv` | 图数据 |
| `data/figures/fig_sensitivity_qx.meta.json` | 图元信息 |

## sensitivity_meta.json Schema

```json
{
  "problem": "Q2",
  "model_type": "optimization",
  "base_case_file": "data/results/result_q2.csv",
  "perturbation_method": "one_at_a_time",
  "perturbation_levels": [-0.2, -0.1, 0, 0.1, 0.2],
  "parameters_tested": ["demand_growth_rate", "transport_cost"],
  "metrics": ["objective_change_rate", "solution_change_rate"],
  "random_seed": 20260513,
  "innovation_parameters": ["lambda_correlation_penalty"]
}
```
