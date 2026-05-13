# math-modeling — 数学建模标准化工作流 Skill

面向数学建模竞赛（CUMCM/MCM/泰迪杯等）的 10 阶段标准化工作流 agent skill。支持乱序执行、状态追踪、质量门控、创新证据链。

## 10 阶段 Checklist

| # | 阶段 | 核心产出 |
|---|------|----------|
| 1 | 审题定类 | 问题分类、子问题拆解、约束条件 |
| 2 | 算法选型 | 候选算法 2-3 个 + 推荐理由 + 风险 |
| 3 | 创新设计 | 创新点候选、评分筛选、基线对比方案 |
| 4 | 建模 | 变量、假设、符号表、方程/目标函数 |
| 5 | 求解实现 | Python 代码 + 结果文件 + 运行日志 |
| 6 | 独立验证 | MATLAB 复现 / 对比误差（可跳过） |
| 7 | 敏感性分析 | 扰动表 + 敏感性图 + 结论 |
| 8 | 可视化 | PNG + CSV + meta.json |
| 9 | 图片审查 | 格式检查 + 内容合理性判断 |
| 10 | 成文准备 | figure_index + model_summary + innovation_summary |

## 安装

### 方式一：npx skills

```bash
npx skills add feiniao87968492/math-modelling
```

### 方式二：手动安装

```bash
# Claude Code / Codex CLI
git clone https://github.com/feiniao87968492/math-modelling.git ~/.agents/skills/math-modeling

# 创建 symlink（Claude Code）
ln -sf ~/.agents/skills/math-modeling ~/.claude/skills/math-modeling
```

## 使用

在 Claude Code 中输入：

```
/math-modeling              # 查看当前进度或初始化
/math-modeling init         # 初始化新赛题项目
/math-modeling progress     # 查看 checklist 状态
/math-modeling next         # 进入下一个推荐阶段
/math-modeling stage 3      # 进入指定阶段
/math-modeling innovate     # 进入创新设计
/math-modeling review       # 执行图片审查
/math-modeling export       # 生成论文素材索引
```

## 核心特性

### 创新设计模块

在算法选型之后、建模之前设计创新点，避免成文阶段临时包装。每个创新点经过 6 维度评分筛选，必须有 baseline 对照和验证方案。

### 敏感性分析

根据题目类型自动选择策略（评价类权重扰动、优化类参数扰动、PDE 网格敏感性、预测类交叉验证等）。

### 图片审查

格式合规检查（坐标轴、图例、DPI、字号）+ 内容合理性判断（趋势一致性、量级合理性、异常点检测）。审查不通过自动回退重绘，最多 2 次。

### 配图说明

每张图自动生成 `meta.json`（含图类型、坐标轴、预期趋势、审查状态），最终汇总为 `figure_index.md`。

## 项目结构

`/math-modeling init` 生成的目录：

```
赛题目录/
├── modeling_state.yaml      ← 流程状态追踪
├── data/
│   ├── raw/                 ← 原始附件
│   ├── processed/           ← 清洗数据
│   ├── innovation/          ← 创新设计产出
│   ├── results/             ← 求解结果
│   ├── sensitivity/         ← 敏感性分析
│   ├── figures/             ← 插图 (PNG+CSV+meta.json)
│   ├── reviews/             ← 审查报告
│   └── paper/               ← 论文素材
├── code/
│   ├── python/
│   └── matlab/
└── logs/
```

## References 子模块

| 文件 | 职责 |
|------|------|
| `references/innovation-design.md` | 7 类创新方向、评分公式、筛选规则 |
| `references/sensitivity-analysis.md` | 按题型自动选择敏感性策略 |
| `references/figure-review.md` | 格式检查表 + 内容审查规则 |
| `references/caption-spec.md` | meta.json schema + caption 写作规范 |

## 适配平台

| 平台 | 安装路径 |
|------|----------|
| Claude Code | `~/.claude/skills/math-modeling` |
| Codex CLI | `~/.agents/skills/math-modeling` |
| Cursor | `.cursor/rules/math-modeling` |
| GitHub Copilot | `.github/skills/math-modeling` |

## License

MIT
