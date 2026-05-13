# 图片审查规则

## 格式合规检查

| 检查项 | 要求 | 严重度 | 备注 |
|--------|------|--------|------|
| 坐标轴标签 | 必须有，含单位 | ERROR | 流程图/网络图标记 N/A |
| 图标题或caption | 二者至少一个完整描述内容 | ERROR | 论文终稿中图内title可省略 |
| 图例 | 多曲线时必须有 | ERROR | |
| 字号 | ≥ 10pt | WARNING | |
| DPI | < 150 ERROR; 150-299 WARNING; ≥ 300 PASS | 分级 | |
| 网格线 | 建议有 | INFO | |
| 颜色对比度 | 不同曲线可区分 | WARNING | |
| 上/右边框 | 建议去除 | INFO | |
| colorbar | 热力图/等高线必须有 | ERROR | |

### 按图类型分支检查

- `line_plot` / `scatter_plot` / `bar_chart`：检查坐标轴、图例、线型
- `heatmap` / `contour_plot`：检查 colorbar
- `radar_chart`：检查指标名称
- `flowchart` / `network_graph`：不检查坐标轴（标记 N/A）
- `map`：检查比例尺、图例、区域标注

## 内容合理性判断

读取 PNG + CSV + meta.json，检查：

1. **趋势一致性**：曲线走势是否符合 meta.json 中的 `expected_pattern`
2. **量级合理性**：数值范围是否在物理/业务合理区间（参考 `expected_pattern.range`）
3. **异常点**：是否有明显的跳变、断裂、NaN
4. **图间一致性**：同一变量在不同图中的范围是否匹配

### expected_pattern 缺失时

若 meta.json 无 `expected_pattern` 字段，仅执行：
- 数值异常检测（NaN、Inf、突变）
- 数据一致性检查
- 给出保守结论："无法判断趋势是否符合模型预期"

### expected_pattern 示例

```json
"expected_pattern": {
  "trend": "monotone_decreasing",
  "range": {"temperature": [37, 75]},
  "description": "稳态温度应由外侧向内侧整体递减"
}
```

trend 可选值：monotone_increasing, monotone_decreasing, converging, oscillating, bell_shaped, step_function, custom

## 审查状态

| 状态 | 含义 | 后续动作 |
|------|------|----------|
| PASS | 可直接使用 | 继续下一阶段 |
| PASS_WITH_WARNINGS | 可用但有轻微问题 | 记录 warnings，继续 |
| REVISE_REQUIRED | 格式或局部内容问题 | 自动回退阶段8重绘 |
| HUMAN_REVIEW_REQUIRED | 趋势/结论不确定 | 暂停等待用户确认 |
| FAIL | 文件损坏/严重错误 | 标记失败，不可使用 |

## 自动重绘机制

```yaml
auto_revision:
  enabled: true
  max_attempts: 2
  fallback_status: "HUMAN_REVIEW_REQUIRED"
```

- 阶段9审查结果为 `REVISE_REQUIRED` → 阶段8状态回退为 `NEEDS_REVISION`
- 自动重绘次数 ≤ `max_auto_revisions`（默认2次）
- 超过次数 → 状态变为 `HUMAN_REVIEW_REQUIRED`，暂停等待用户

## Caption 检查（联动 caption-spec.md）

每个 caption 应包含：
1. 图号
2. 图中展示的对象
3. 关键变量和单位
4. 主要条件或参数
5. 必要时说明主要结论

不合格示例：`"图1 温度分布图。"` — 缺少边界条件、单位、变量说明。

## 审查报告输出

每张图生成 `data/reviews/fig_xx_review.json`：

```json
{
  "figure_id": "fig_01",
  "reviewed_at": "2026-09-05T14:35:00",
  "format_checks": {
    "axis_labels": {"status": "PASS", "applicable": true},
    "legend": {"status": "PASS", "applicable": true},
    "dpi": {"status": "PASS", "value": 300},
    "font_size": {"status": "PASS", "value": 11}
  },
  "content_checks": {
    "trend_consistency": {"status": "PASS", "note": "温度单调递减，符合预期"},
    "range_validity": {"status": "PASS", "note": "温度在37-75°C范围内"},
    "anomalies": {"status": "PASS", "note": "无异常点"}
  },
  "caption_check": {
    "status": "PASS",
    "issues": []
  },
  "overall_status": "PASS",
  "revision_suggestions": []
}
```
