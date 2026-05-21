# Protocol — Fallback and Deviation

## Core Rule

工具 fallback 可以自动发生，但方法偏离不能悄悄发生。凡是 fallback 改变了已确认算法、模型结构或证据路径，都必须重新触发确认。

## Safe Fallback

以下情况允许自动 fallback，但必须记录 `fallback_reason`：
- 同一方法换实现工具
- 同一图表换绘图后端
- 同一验证逻辑换等价执行环境

## Deviation Requiring Re-Confirmation

以下情况必须重新生成阻断型待确认项：
- 已确认的算法从 ARIMA 改为 LSTM
- 已确认的优化建模结构发生本质变化
- 已确认结论的主要证据路径改变
- 原计划中的 baseline / innovation 对照方式变化

## Required Record

```yaml
fallback_event:
  original_plan: "ARIMA + 残差修正"
  fallback_tool: "Python statsmodels"
  fallback_reason: "MATLAB MCP unavailable"
  method_changed: false
  requires_confirmation: false
```

若 `method_changed: true`，则 `requires_confirmation` 必须为 `true`。
