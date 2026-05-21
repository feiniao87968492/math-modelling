# Regression — Quality Status Canonicalization

## Input Scenario

- review target: `references/protocol-state-writeback.md`
- goal: verify that new writeback guidance uses only canonical `quality_status` families

## Expected Writeback Snippet

```yaml
quality_status_examples:
  - PASS
  - PASS_WITH_WARNINGS
  - BLOCKED_MISSING_PROBLEM_INPUTS
  - PAUSED_PENDING_ORIGINAL_ATTACHMENTS
  - USING_ORAL_DESCRIPTION_DRAFT
  - FAILED_OUTPUT_GENERATION
```

## Forbidden Outcomes

- `DONE_OK`
- `IN_PROGRESS_NORMAL`
- 两个不同名字同时表达“缺题面输入”这一阻断语义
- 把非 canonical 旧名继续当成新的写回结果
