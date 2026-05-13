# 配图说明规范

## meta.json Schema

每张图生成时必须同时创建 `fig_xx.meta.json`：

```json
{
  "figure_id": "fig_01",
  "filename": "temperature_distribution.png",
  "figure_type": "line_plot",
  "problem": "Q1",
  "title": "四层材料温度分布（稳态）",
  "caption": "图1 在外界温度75°C、内侧温度37°C边界条件下，四层防护服材料的稳态温度分布。横轴为距外表面距离(mm)，纵轴为温度(°C)。",
  "axes": {
    "x": {"label": "距外表面距离", "unit": "mm"},
    "y": {"label": "温度", "unit": "°C"}
  },
  "parameters": {"T_out": 75, "T_in": 37},
  "expected_pattern": {
    "trend": "monotone_decreasing",
    "range": {"temperature": [37, 75]},
    "description": "稳态温度应由外侧向内侧整体递减，材料分界处允许斜率变化。"
  },
  "generated_by": "code/python/visualize.py",
  "generated_at": "2026-05-13T14:30:00",
  "data_file": "temperature_distribution.csv",
  "source_result_file": "data/results/result_q1.csv",
  "random_seed": 20260513,
  "review": {
    "status": "UNKNOWN",
    "review_report": null,
    "reviewed_at": null
  }
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| figure_id | 是 | 唯一标识，格式 `fig_XX` |
| filename | 是 | PNG 文件名 |
| figure_type | 是 | 图类型，见下方可选值 |
| problem | 是 | 所属子问题（Q1/Q2/...） |
| title | 是 | 图标题 |
| caption | 是 | 完整图注 |
| axes | 视图类型 | 坐标轴信息（流程图等不适用） |
| parameters | 否 | 生成该图时的关键参数 |
| expected_pattern | 否 | 预期趋势（供图片审查使用） |
| generated_by | 是 | 生成该图的脚本路径 |
| generated_at | 是 | ISO 时间戳 |
| data_file | 是 | 对应的 CSV 数据文件 |
| source_result_file | 否 | 数据来源的结果文件 |
| random_seed | 否 | 随机种子（如适用） |
| review | 是 | 审查状态（初始为 UNKNOWN） |

## figure_type 可选值

| 类型 | 说明 |
|------|------|
| line_plot | 折线图 |
| scatter_plot | 散点图 |
| bar_chart | 柱状图 |
| heatmap | 热力图 |
| boxplot | 箱线图 |
| tornado_chart | 龙卷风图（敏感性） |
| radar_chart | 雷达图 |
| surface_plot | 三维曲面图 |
| contour_plot | 等高线图 |
| flowchart | 流程图 |
| network_graph | 网络图 |
| map | 地图 |

## Caption 写作规范

每个 caption 必须包含：

1. **图号** — 如"图1"、"图2"
2. **展示对象** — 图中展示的是什么
3. **关键变量和单位** — 横纵轴变量及单位
4. **主要条件或参数** — 边界条件、模型参数等
5. **主要结论**（可选） — 必要时说明图中可观察到的主要结论

### 合格示例

```
图1 在外界温度 75°C、内侧温度 37°C 的边界条件下，四层防护服材料的稳态温度分布。
横轴为距外表面距离/mm，纵轴为温度/°C。结果显示温度沿厚度方向整体递减，
并在材料分界处出现斜率变化。
```

### 不合格示例

```
图1 温度分布图。
```

问题：缺少边界条件、单位、变量说明。

## figure_index.md 汇总格式

阶段10成文准备时，汇总所有图的索引：

```markdown
# 插图索引

| 图号 | 文件名 | 所属问题 | 图类型 | 标题 | 审查状态 | Caption状态 |
|------|--------|----------|--------|------|----------|-------------|
| fig_01 | temperature_distribution.png | Q1 | line_plot | 四层材料温度分布（稳态） | PASS | PASS |
| fig_02 | sensitivity_tornado.png | Q1 | tornado_chart | 参数敏感性龙卷风图 | PASS | PASS |
```

该文件从所有 `data/figures/fig_xx.meta.json` 自动生成。

## expected_pattern.trend 可选值

| 值 | 含义 |
|----|------|
| monotone_increasing | 单调递增 |
| monotone_decreasing | 单调递减 |
| converging | 收敛到某值 |
| oscillating | 振荡 |
| bell_shaped | 钟形/正态分布形 |
| step_function | 阶梯形 |
| custom | 自定义（需在 description 中说明） |
