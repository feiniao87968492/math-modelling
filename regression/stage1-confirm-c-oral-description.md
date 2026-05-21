# Regression — Stage 1 Confirm C Oral Description

## Input Scenario

- pending item: `confirm_stage1_missing_problem_inputs`
- stage: `1`
- user reply:

```text
C
先按我的口头描述继续：我们要在预算固定的情况下，比较新增自动化设备和调整集包规则两种策略对效率的影响。
```

## Expected Writeback Snippet

```yaml
- decision_id: "decision_stage1_001"
  confirmation_id: "confirm_stage1_missing_problem_inputs"
  stage: 1
  decision_type: "problem_input_confirmation"
  decision: "use_oral_description"
  selected_option: "C"
  user_payload:
    oral_description_text: "先按我的口头描述继续：我们要在预算固定的情况下，比较新增自动化设备和调整集包规则两种策略对效率的影响。"
  status_after_decision: "HUMAN_REVIEW_REQUIRED"
```

## Forbidden Outcomes

- 只记录 `selected_option: "C"`，但没有 `user_payload.oral_description_text`
- 用户只回复 `C` 时仍被写成有效确认
- 把阶段直接写成 `IN_PROGRESS` 或 `DONE`
