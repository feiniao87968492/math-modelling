# Regression — Stage 1 Confirm A Problem Statement

## Input Scenario

- pending item: `confirm_stage1_missing_problem_inputs`
- stage: `1`
- user reply:

```text
A
题目要求我们针对配送中心的分拣、装车和干线运输做联合优化，目标是在满足时效约束的前提下降低总成本。
```

## Expected Writeback Snippet

```yaml
- decision_id: "decision_stage1_001"
  confirmation_id: "confirm_stage1_missing_problem_inputs"
  stage: 1
  decision_type: "problem_input_confirmation"
  decision: "provide_problem_statement"
  selected_option: "A"
  user_payload:
    problem_statement_text: "题目要求我们针对配送中心的分拣、装车和干线运输做联合优化，目标是在满足时效约束的前提下降低总成本。"
  status_after_decision: "HUMAN_REVIEW_REQUIRED"
```

## Forbidden Outcomes

- 只记录 `selected_option: "A"`，但没有 `user_payload.problem_statement_text`
- 把题面正文只塞进 `decision_summary`，却不写结构化字段
- 把阶段直接写成 `IN_PROGRESS` 或 `DONE`
