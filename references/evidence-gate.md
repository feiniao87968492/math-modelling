# 终稿证据门控 — Final Evidence Gate

## 概述

阶段10 Step 3（Paper Material Export）前必须通过 Final Evidence Gate。未通过门控检查的不得生成正式论文素材。

## 门控检查表

| 检查项 | 要求 | 证据来源 |
|--------|------|----------|
| 阶段1-5 必须 DONE | 所有核心阶段完成 | modeling_state.yaml |
| 阶段6 若 SKIPPED，必须有 skip_reason | 跳过的合理说明 | modeling_state.yaml |
| 阶段7 必须 DONE | 敏感性分析完成 | modeling_state.yaml |
| 阶段8 必须 DONE | 可视化完成 | modeling_state.yaml |
| 阶段9 所有图通过审查 | PASS 或 PASS_WITH_WARNINGS | data/reviews/*.json |
| 所有 selected innovations 有证据 | 每个创新点至少有 1 个 evidence_output 存在且非空，或至少 1 个 evidence_runs 可在 experiment_log.yaml 中找到 | innovation_design.yaml + experiments/experiment_log.yaml |
| 所有主要结论可追溯 | 结论绑定结果/图/表/敏感性/验证 | claim_registry.yaml |
| 所有假设已记录 | 假设有来源说明 | data/facts/assumptions.yaml |
| 所有约束已记录 | 约束有来源说明 | data/facts/constraints_registry.yaml |

## 检查报告模板

输出到 `data/paper/final_evidence_check.md`：

```markdown
# Final Evidence Check

## 门控检查结果

| 检查项 | 状态 | 证据位置 |
|--------|------|----------|
| 所有核心阶段完成 | PASS | modeling_state.yaml |
| 阶段6跳过原因记录 | PASS | skip_reason: ... |
| 主要创新点有证据 | PASS | data/results/comparison_q2.csv |
| 所有图通过审查 | PASS | data/reviews/*.json |
| 主要结论可追溯 | PASS | claim_registry.yaml |
| 假设已记录 | PASS | data/facts/assumptions.yaml |
| 约束已记录 | PASS | data/facts/constraints_registry.yaml |

## 未通过项

（列出 FAILED 项及原因）

## 总体结论

PASS / PASS_WITH_WARNINGS / BLOCKED
```

## 状态含义

| 状态 | 含义 | 后续动作 |
|------|------|----------|
| PASS | 所有检查通过 | 进入阶段10 Step 3 |
| PASS_WITH_WARNINGS | 有警告但不阻断 | 进入阶段10 Step 3，记录 warnings |
| BLOCKED | 存在未通过项 | 修复后重新检查 |

## 执行时机

Final Evidence Gate 在阶段10内部的 Step 1 Claim Drafting 之后、Step 3 Paper Material Export 之前执行。由 ON_STAGE_ENTER(10) 触发，但仅在完成 Drafting 后正式执行 Gate。
