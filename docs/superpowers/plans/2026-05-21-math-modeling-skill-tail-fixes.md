# math-modeling Skill Tail Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tighten the `math-modeling` skill so stage 1 confirmation payloads preserve A/C branch body text in a structured schema and `quality_status` uses one canonical naming system backed by regression fixtures.

**Architecture:** Keep the existing modular skill layout and patch only the protocol layer plus a lightweight regression directory. The implementation touches two existing protocol files and adds three markdown-based regression fixtures that describe input, expected writeback, and forbidden outcomes for manual replay.

**Tech Stack:** Markdown protocol files, YAML snippets embedded in markdown, PowerShell for verification, git for change review.

---

## File Structure

### Files to modify
- `references/protocol-human-confirmation.md` — strengthen stage 1 A/C confirmation branches so `user_payload` becomes part of the unified decision schema and missing body text stays blocked.
- `references/protocol-state-writeback.md` — define the canonical `quality_status` family, banned patterns, and migration guidance from old names.

### Files to create
- `regression/stage1-confirm-a-problem-statement.md` — fixture for stage 1 option A with required `problem_statement_text` payload.
- `regression/stage1-confirm-c-oral-description.md` — fixture for stage 1 option C with required `oral_description_text` payload.
- `regression/quality-status-canonicalization.md` — fixture for allowed `quality_status` families and banned non-canonical names.

### Verification surface
- `references/protocol-human-confirmation.md` must mention `user_payload`, `problem_statement_text`, `oral_description_text`, and the rule that missing A/C body text keeps `HUMAN_REVIEW_REQUIRED`.
- `references/protocol-state-writeback.md` must enumerate the canonical families `PASS`, `PASS_WITH_WARNINGS`, `BLOCKED_*`, `PAUSED_*`, `USING_*`, `FAILED_*` and ban status/quality mixing.
- `regression/` must exist with exactly the three fixture files above.
- Static verification uses `Select-String`; final confidence comes from a manual headless replay checklist documented in the regression files.

---

### Task 1: Strengthen stage 1 confirmation payload schema

**Files:**
- Modify: `references/protocol-human-confirmation.md`
- Test: `references/protocol-human-confirmation.md`

- [ ] **Step 1: Capture the current gap in the confirmation protocol**

Run:

```powershell
Select-String -Path "references/protocol-human-confirmation.md" -Pattern "user_payload", "problem_statement_text", "oral_description_text", "正文载荷缺失"
```

Expected:
- No matches for at least the first three patterns.
- This confirms the protocol still describes A/C mostly as branch examples rather than field-level schema rules.

- [ ] **Step 2: Extend the decision record schema with `user_payload`**

In `references/protocol-human-confirmation.md`, replace the existing `Decision Record Schema` YAML example:

```yaml
- decision_id: "decision_001"
  confirmation_id: "confirm_001"
  stage: 2
  decision_type: "algorithm_selection_confirmation"
  decision: "accept_default"
  selected_option: "A"
  decision_summary: "用户接受默认推荐算法方案。"
  impact_scope:
    - "data/algorithm_selection.yaml"
    - "stages.2_algorithm_selection"
  status_after_decision: "DONE"
  recorded_at: "2026-05-21T19:31:19+08:00"
```

with this expanded example:

```yaml
- decision_id: "decision_stage2_001"
  confirmation_id: "confirm_001"
  stage: 2
  decision_type: "algorithm_selection_confirmation"
  decision: "accept_default"
  selected_option: "A"
  decision_summary: "用户接受默认推荐算法方案。"
  user_payload: {}
  impact_scope:
    - "data/algorithm_selection.yaml"
    - "stages.2_algorithm_selection"
  status_after_decision: "DONE"
  recorded_at: "2026-05-21T19:31:19+08:00"
```

Then add this bullet to the field constraints section right after `decision_summary`:

```markdown
- `user_payload`：结构化补充载荷；默认可为空对象 `{}`，但当确认分支依赖用户正文输入时必须写入约定字段
```

- [ ] **Step 3: Add hard rules for stage 1 A/C payload fields**

In the `Confirmation Handling` section, append these two rules after the existing branch list:

```markdown
- 若 `decision: provide_problem_statement`，则 `user_payload.problem_statement_text` 必填；缺失时不得写成有效确认，阶段保持 `HUMAN_REVIEW_REQUIRED`
- 若 `decision: use_oral_description`，则 `user_payload.oral_description_text` 必填；缺失时不得写成有效确认，阶段保持 `HUMAN_REVIEW_REQUIRED`
```

- [ ] **Step 4: Replace the stage 1 branch examples with payload-aware versions**

In the `Stage 1 缺输入阻断的标准分支` section, replace the A and C examples with the following exact YAML blocks:

```yaml
# A. 用户补充题面文本
- decision_id: "decision_stage1_001"
  confirmation_id: "confirm_stage1_missing_problem_inputs"
  stage: 1
  decision_type: "problem_input_confirmation"
  decision: "provide_problem_statement"
  selected_option: "A"
  decision_summary: "用户按 A 选项提供了题面文本，用于继续 stage 1 审题。"
  user_payload:
    problem_statement_text: "...用户提供的题面正文..."
  status_after_decision: "HUMAN_REVIEW_REQUIRED"

# C. 用户允许先按口头描述推进
- decision_id: "decision_stage1_001"
  confirmation_id: "confirm_stage1_missing_problem_inputs"
  stage: 1
  decision_type: "problem_input_confirmation"
  decision: "use_oral_description"
  selected_option: "C"
  decision_summary: "用户选择先用口头描述建立 stage 1 初版事实与待确认项。"
  user_payload:
    oral_description_text: "...用户提供的口头描述..."
  status_after_decision: "HUMAN_REVIEW_REQUIRED"
```

Immediately after that subsection, add this missing-body rule:

```markdown
若用户回复已经能映射到 A 或 C，但未提供可写入 `user_payload` 的正文内容（例如只回复 “A” / “C” / “按这个来”），则只能记录“选项已识别但正文载荷缺失”，不得写成已完成确认，也不得把阶段状态改为 `IN_PROGRESS` 或 `DONE`。
```

- [ ] **Step 5: Run a focused verification scan**

Run:

```powershell
Select-String -Path "references/protocol-human-confirmation.md" -Pattern "user_payload", "problem_statement_text", "oral_description_text", "正文载荷缺失", "HUMAN_REVIEW_REQUIRED"
```

Expected:
- All five patterns are present.
- `problem_statement_text` and `oral_description_text` each appear in the stage 1 branch examples.

- [ ] **Step 6: Commit the confirmation protocol change**

Run:

```bash
git add references/protocol-human-confirmation.md
git commit -m "fix: preserve stage1 confirmation payloads"
```

Expected:
- Commit succeeds with only the confirmation protocol file staged.

---

### Task 2: Canonicalize `quality_status` naming rules

**Files:**
- Modify: `references/protocol-state-writeback.md`
- Test: `references/protocol-state-writeback.md`

- [ ] **Step 1: Capture the current quality-status rule surface**

Run:

```powershell
Select-String -Path "references/protocol-state-writeback.md" -Pattern "PASS_WITH_WARNINGS", "BLOCKED_", "PAUSED_", "USING_", "FAILED_", "迁移"
```

Expected:
- Some canonical families may appear already, but there is no explicit migration guidance.
- This confirms the file still needs a tighter canonical rule section.

- [ ] **Step 2: Replace the `Quality Status Naming Rule` section with the canonical family version**

In `references/protocol-state-writeback.md`, replace the current `Quality Status Naming Rule` section body with this exact content:

```markdown
## Quality Status Naming Rule

`quality_status` 只允许表达“质量判断 / 阻断原因 / 当前工作口径”，不允许和阶段状态混写。统一规则：

- 允许的 canonical 名称或前缀只有：
  - `PASS`
  - `PASS_WITH_WARNINGS`
  - `BLOCKED_*`
  - `PAUSED_*`
  - `USING_*`
  - `FAILED_*`
- 语义说明：
  - `PASS*`：通过类
  - `BLOCKED*`：阻断类
  - `PAUSED*`：确认暂停类
  - `USING*`：临时工作口径类
  - `FAILED*`：失败类
- 不要把阶段状态词再塞进 `quality_status`，例如禁止 `DONE_OK`、`IN_PROGRESS_NORMAL`
- 不允许同一语义保留多个近义 canonical 名称；例如若“缺题面输入”已经选定一个 `BLOCKED_*` 名称，则不得再并存第二个近义阻断态
- 不允许写成同时表达阶段结论与质量口径的复合名，例如 `DONE_WITH_BLOCKER`
```

- [ ] **Step 3: Add migration guidance for old names**

Immediately after the `Quality Status Naming Rule` section, add this new section:

```markdown
## Canonical Migration Guidance

- 读取历史状态时，若发现非 canonical 旧名，解释时必须映射到唯一的 canonical 名称
- 后续新增或更新记录时，只允许写 canonical 名称，不得继续写回旧名
- 若人工回放或 headless 验收中发现旧名继续作为“新写回结果”出现，视为未通过本轮收口
```

- [ ] **Step 4: Strengthen the invariants to mention old-name rejection**

In the `Invariants` list, replace this line:

```markdown
- `quality_status` 必须遵守 canonical naming rule；近义状态名不得并存
```

with this stricter line:

```markdown
- `quality_status` 必须遵守 canonical naming rule；近义状态名不得并存，非 canonical 旧名不得继续作为新写回结果出现
```

- [ ] **Step 5: Run the canonical naming verification scan**

Run:

```powershell
Select-String -Path "references/protocol-state-writeback.md" -Pattern "PASS_WITH_WARNINGS", "BLOCKED_", "PAUSED_", "USING_", "FAILED_", "DONE_OK", "IN_PROGRESS_NORMAL", "Canonical Migration Guidance"
```

Expected:
- All canonical families and the migration section are present.
- `DONE_OK` and `IN_PROGRESS_NORMAL` appear only as banned examples.

- [ ] **Step 6: Commit the state-writeback change**

Run:

```bash
git add references/protocol-state-writeback.md
git commit -m "fix: tighten quality status canonical naming"
```

Expected:
- Commit succeeds with only the state writeback protocol file staged.

---

### Task 3: Add markdown regression fixtures for the two tail fixes

**Files:**
- Create: `regression/stage1-confirm-a-problem-statement.md`
- Create: `regression/stage1-confirm-c-oral-description.md`
- Create: `regression/quality-status-canonicalization.md`
- Test: all three files in `regression/`

- [ ] **Step 1: Create the stage 1 option A fixture**

Create `regression/stage1-confirm-a-problem-statement.md` with this exact content:

```markdown
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
```

- [ ] **Step 2: Create the stage 1 option C fixture**

Create `regression/stage1-confirm-c-oral-description.md` with this exact content:

```markdown
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
```

- [ ] **Step 3: Create the quality-status fixture**

Create `regression/quality-status-canonicalization.md` with this exact content:

```markdown
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
```

- [ ] **Step 4: Verify the regression directory and file content**

Run:

```powershell
$paths = @(
  "regression/stage1-confirm-a-problem-statement.md",
  "regression/stage1-confirm-c-oral-description.md",
  "regression/quality-status-canonicalization.md"
)
$paths | ForEach-Object { "$_ -> $(Test-Path $_)" }
Select-String -Path "regression/stage1-confirm-a-problem-statement.md","regression/stage1-confirm-c-oral-description.md","regression/quality-status-canonicalization.md" -Pattern "Input Scenario", "Expected Writeback Snippet", "Forbidden Outcomes"
```

Expected:
- Every `Test-Path` line ends with `True`.
- Each regression file contains all three required headings.

- [ ] **Step 5: Commit the regression fixtures**

Run:

```bash
git add regression/stage1-confirm-a-problem-statement.md regression/stage1-confirm-c-oral-description.md regression/quality-status-canonicalization.md
git commit -m "test: add regression fixtures for skill tail fixes"
```

Expected:
- Commit succeeds with exactly three new markdown fixture files.

---

### Task 4: Run static checks and a manual headless replay checklist

**Files:**
- Modify: none
- Test: `references/protocol-human-confirmation.md`, `references/protocol-state-writeback.md`, `regression/*.md`

- [ ] **Step 1: Run the protocol consistency scan**

Run:

```powershell
Select-String -Path "references/protocol-human-confirmation.md","references/protocol-state-writeback.md" -Pattern "user_payload", "problem_statement_text", "oral_description_text", "PASS_WITH_WARNINGS", "Canonical Migration Guidance", "HUMAN_REVIEW_REQUIRED"
```

Expected:
- All six patterns are found.
- `HUMAN_REVIEW_REQUIRED` still appears in the confirmation protocol after the new payload rules are added.

- [ ] **Step 2: Run the regression fixture scan**

Run:

```powershell
Select-String -Path "regression/stage1-confirm-a-problem-statement.md","regression/stage1-confirm-c-oral-description.md","regression/quality-status-canonicalization.md" -Pattern "problem_statement_text", "oral_description_text", "DONE_OK", "IN_PROGRESS_NORMAL", "status_after_decision: \"HUMAN_REVIEW_REQUIRED\""
```

Expected:
- `problem_statement_text` and `oral_description_text` are present in the stage 1 fixtures.
- `DONE_OK` and `IN_PROGRESS_NORMAL` appear only in the canonicalization fixture as forbidden outcomes.
- `status_after_decision: "HUMAN_REVIEW_REQUIRED"` appears in both stage 1 fixtures.

- [ ] **Step 3: Follow the manual headless replay checklist**

Run these checks manually against the fixture files rather than inventing new scenarios:

```text
1. Read regression/stage1-confirm-a-problem-statement.md and verify the expected snippet contains user_payload.problem_statement_text.
2. Read regression/stage1-confirm-c-oral-description.md and verify the expected snippet contains user_payload.oral_description_text.
3. Confirm both stage 1 fixtures keep status_after_decision at HUMAN_REVIEW_REQUIRED.
4. Read regression/quality-status-canonicalization.md and verify every allowed example matches one canonical family from protocol-state-writeback.md.
5. Confirm the forbidden examples DONE_OK and IN_PROGRESS_NORMAL are documented as banned, not allowed.
```

Expected:
- Every checklist item maps directly to the implemented protocol text.
- No additional undocumented state names are needed to explain the fixtures.

- [ ] **Step 4: Review the working tree before final handoff**

Run:

```bash
git diff -- references/protocol-human-confirmation.md references/protocol-state-writeback.md regression/stage1-confirm-a-problem-statement.md regression/stage1-confirm-c-oral-description.md regression/quality-status-canonicalization.md
git status --short
```

Expected:
- `git diff` shows only the scoped tail-fix changes.
- `git status --short` is empty if every commit in Tasks 1-3 already succeeded.

- [ ] **Step 5: Final commit if Tasks 1-3 were executed without intermediate commits**

If the earlier commit steps were intentionally skipped, use this fallback instead:

```bash
git add references/protocol-human-confirmation.md references/protocol-state-writeback.md regression/stage1-confirm-a-problem-statement.md regression/stage1-confirm-c-oral-description.md regression/quality-status-canonicalization.md
git commit -m "fix: close math-modeling skill tail issues"
```

Expected:
- Commit succeeds with only the two protocol files and three regression fixtures staged.
- Skip this step if Tasks 1-3 already created the smaller scoped commits.

---

## Self-Review

### Spec coverage
- Stage 1 A/C payload preservation: covered by Task 1 and the two stage 1 regression fixtures in Task 3.
- Missing-body handling stays blocked: covered by Task 1 Step 3 and both stage 1 fixtures.
- `quality_status` canonical family, banned patterns, migration guidance: covered by Task 2 and the canonicalization fixture in Task 3.
- Validation planning: covered by Task 4 static scans and manual replay checklist.

### Placeholder scan
- No `TBD`, `TODO`, or deferred implementation notes remain.
- Every code-edit step includes the exact markdown or YAML snippet to add or replace.
- Every verification step includes an exact command and expected outcome.

### Type consistency
- The new structured payload field is always named `user_payload`.
- Stage 1 option A always uses `problem_statement_text`.
- Stage 1 option C always uses `oral_description_text`.
- `quality_status` families are consistent across Task 2 and Task 3.
