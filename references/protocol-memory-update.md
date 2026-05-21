# Protocol — Memory Update

## Core Rule

`memory.md` 是阶段级协议对象，不是可选附注。每次进入阶段前必须读取；每次阶段结束前必须执行 `memory check`。

## Pre-Stage Read Rule

1. 优先读取项目根目录 `memory.md`
2. 若项目中不存在 `memory.md`，读取 `references/modeling-memory-template.md`
3. 进入阶段时必须把 memory 中与当前阶段相关的规则作为额外门槛使用

## `memory check`

阶段收尾前必须判断以下四项：

1. 是否发现新的可复用规则
2. 是否发现新的常见坑点
3. 是否发现新的反例
4. 是否新增明确的用户偏好

若四项都没有新增内容，必须显式判定：`no new memory`

## Persistent Record

`memory check` 不能只停留在口头说明，必须把结果结构化写回 `modeling_state.yaml`。最小记录建议为：

```yaml
stages:
  2_algorithm_selection:
    memory_check:
      status: "UPDATED" | "NO_NEW_MEMORY"
      summary: "新增 1 条规则" | "no new memory"
      recorded_at: "2026-05-21T19:31:19+08:00"
      memory_targets:
        - "memory.md"
```

要求：
- 若没有新增内容，`summary` 必须显式写出 `no new memory`
- 若有新增内容，`memory_targets` 必须指出写入位置，通常包含 `memory.md`
- 任一阶段宣布 `DONE`、`NEEDS_REVISION`、`HUMAN_REVIEW_REQUIRED` 或 `FAILED` 前，都应已有对应的 `memory_check` 记录

## Allowed Memory Categories

```markdown
## Rules
- 以后会再次影响阶段决策的规则

## Pitfalls
- 容易重复踩中的坑点

## Counterexamples
- 看似合理但被证伪的方案

## User Preferences
- 会持续影响 workflow 行为的用户偏好
```

## Forbidden Content

禁止写入：
- 当日工作总结
- 阶段流水账
- 一次性临时情况
- 文件路径罗列

## Write Timing

必须写回的时机：
- 阶段完成前
- 被用户否决或退回修订时
- 发现新规则或坑点时立即写

可选写回时机：
- 大阶段切换前
- `export` 前统一去重整理
