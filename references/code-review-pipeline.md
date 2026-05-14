# 代码审查流水线 — Code Review Pipeline

## 概述

阶段5求解实现完成后、进入阶段6/7前，必须执行 5 层代码审查。任一 ERROR 不通过则阶段5状态设为 NEEDS_REVISION。

## 5 层审查

### Layer 1：静态代码检查

| 检查项 | 严重度 | 说明 |
|--------|--------|------|
| 随机种子固定 | ERROR | 所有含随机性的代码必须设置 `random_seed`；若模型和数据处理完全确定性，可标记 N/A 并在报告中说明无随机分量 |
| 路径可移植 | ERROR | 禁止硬编码绝对路径，使用 `pathlib` 或相对路径 |
| 异常处理 | WARNING | 文件读取、API调用等必须有 try/except |
| 未定义变量 | ERROR | 所有变量在使用前已定义 |
| 运行参数记录 | WARNING | 关键运行参数需输出到日志或结果文件 |
| 主要结果输出 | ERROR | 脚本必须输出约定格式的结果文件 |
| 不可复现实验 | ERROR | 随机算法必须记录 seed |

### Layer 2：数据输入检查

| 检查项 | 严重度 | 说明 |
|--------|--------|------|
| 输入文件存在 | ERROR | 检查所有依赖的输入文件路径 |
| 行列数符合预期 | WARNING | 读取后检查 shape 与 data_audit 记录一致 |
| 缺失值比例 | WARNING | 超过阈值需处理 |
| 数值范围合理 | WARNING | 检查是否存在超出物理/业务范围的值 |
| 单位匹配 | ERROR | 与 data_dictionary 中的单位一致 |
| 类别变量取值合法 | WARNING | 类别值不在预期集合中需报警 |

### Layer 3：模型逻辑检查

| 检查项 | 严重度 | 说明 |
|--------|--------|------|
| 目标函数与 model_spec 一致 | ERROR | 检查目标函数表达式与建模阶段一致 |
| 约束全部实现 | ERROR | model_spec 中的每条约束在代码中有对应实现 |
| 变量单位一致 | ERROR | 目标函数与约束中的变量单位匹配 |
| baseline vs innovative 可比 | WARNING | 两者差异仅限创新点，控制变量一致 |
| 子问题输出无遗漏 | ERROR | 每个子问题生成对应结果文件 |

### Layer 4：结果 Sanity Check

| 检查项 | 严重度 | 说明 |
|--------|--------|------|
| NaN / Inf | ERROR | 结果文件中不允许 NaN 或 Inf |
| 结果在合理范围 | WARNING | 指标值符合物理/业务常识 |
| 排名/预测/优化符合常识 | WARNING | 如预测值不为负、排名有区分度 |
| 优化解满足约束 | ERROR | 检查约束违反率，应 < 1e-6 |
| 预测无数据泄露 | ERROR | 时间序列预测检查时间顺序 |
| 评价权重归一化 | WARNING | 所有权重和应为 1 |

### Layer 5：复现性检查

| 检查项 | 严重度 | 说明 |
|--------|--------|------|
| 固定 seed 结果一致 | ERROR | 相同代码 + 相同 seed → 相同结果 |
| 换 seed 结果稳定 | WARNING | 不同 seed 下结果在合理范围内波动 |
| 再次运行文件一致 | WARNING | 重新运行生成相同结构的结果文件 |
| 输出文件 hash 记录 | INFO | 记录输出文件的 MD5/SHA256 |

## 审查报告输出

输出到 `data/results/code_review_report.md`：

```markdown
# Code Review Report

## 1. Static Code Check
| 检查项 | 状态 | 说明 |
|--------|------|------|
| 随机种子固定 | PASS | random_seed=20260513 |
| ... | ... | ... |

## 2. Data Input Check
| 数据文件 | 行数 | 列数 | 缺失值 | 状态 |
|---------|-----|-----|-------|------|
| ... | ... | ... | ... | ... |

## 3. Model Logic Check
- 目标函数与 model_spec 一致：PASS
- 约束实现完整性：PASS
- baseline/innovative 对比公平性：PASS

## 4. Result Sanity Check
- NaN/Inf：无
- 指标范围：合理
- ...

## 5. Reproducibility Check
- 固定 seed 复现：PASS
- 输出文件 hash 已记录：PASS

## Overall Status
PASS / PASS_WITH_WARNINGS / NEEDS_REVISION / FAILED
```

## 机器可读 JSON 输出

除 Markdown 报告外，输出 `code_review_report.json` 供 agent 自动判定：

```json
{
  "overall_status": "PASS_WITH_WARNINGS",
  "blocking_errors": 0,
  "layers": {
    "static_code_check": {
      "status": "PASS",
      "errors": [],
      "warnings": ["部分文件读取未捕获异常"]
    },
    "data_input_check": {
      "status": "PASS",
      "errors": [],
      "warnings": []
    },
    "model_logic_check": {
      "status": "PASS",
      "errors": [],
      "warnings": []
    },
    "result_sanity_check": {
      "status": "PASS_WITH_WARNINGS",
      "errors": [],
      "warnings": ["部分指标接近边界值"]
    },
    "reproducibility_check": {
      "status": "PASS",
      "errors": [],
      "warnings": []
    }
  }
}
```

## 状态判别

| 结果 | 含义 |
|------|------|
| PASS | 所有 ERROR 检查通过 |
| PASS_WITH_WARNINGS | 所有 ERROR 通过，存在 WARNING |
| NEEDS_REVISION | 存在 ERROR，需回退修改 |
| FAILED | 严重错误（文件缺失、代码无法运行） |

阶段5判定规则：
- `code_review_report.json` 中 `blocking_errors > 0` → 阶段5 `NEEDS_REVISION`
- `overall_status = PASS_WITH_WARNINGS` → 阶段5 DONE + quality_status `PASS_WITH_WARNINGS`
