# Quickstart Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `math-modeling-v4` onboarding so a first-time user can understand the workflow, create the minimum project skeleton, and try the key commands immediately.

**Architecture:** Keep the change documentation-only except for minimal contract tests. Put concise operator-facing examples in `SKILL.md`, richer onboarding and skeleton examples in `README.md`, and extend the existing contract test module to prevent these must-have sections from disappearing later.

**Tech Stack:** Markdown docs, pytest contract tests.

---

## File Structure Map

### Files to modify

- `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md` - add compact workflow, command, and blocker examples.
- `C:\Users\zty\.agents\skills\math-modeling-v4\README.md` - add quickstart, skeleton, minimal file snippets, and blocker handling.
- `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py` - add doc contract assertions for onboarding content.

### Files used as reference only

- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-markdown-audit.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-human-confirmation.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-readiness-gate.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\protocol-rollback.md`
- `C:\Users\zty\.agents\skills\math-modeling-v4\references\evidence-gate.md`

---

### Task 1: Add failing contract tests for quickstart content

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Write the failing tests**

Append these tests to `regression/test_markdown_first_contracts.py`:

```python
def test_skill_contains_typical_workflow_and_command_examples():
    content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "## 典型使用流程" in content
    assert "## 命令示例" in content
    assert "/math-modeling init" in content
    assert "/math-modeling export" in content
    assert "## 阻断时会看到什么" in content


def test_readme_contains_quickstart_skeleton_and_minimal_examples():
    content = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "## 适用场景" in content
    assert "## 新项目骨架" in content
    assert "workflow.md" in content
    assert "memory.md" in content
    assert "## 5 分钟上手" in content
    assert "## 最小文件示例" in content
    assert "## 常见阻断与处理" in content
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_skill_contains_typical_workflow_and_command_examples regression/test_markdown_first_contracts.py::test_readme_contains_quickstart_skeleton_and_minimal_examples -q
```

Expected: FAIL because the current docs do not yet contain these sections.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_markdown_first_contracts.py
git commit -m "test: add failing quickstart doc contract checks"
```

---

### Task 2: Extend `SKILL.md` with operator-facing quickstart content

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Add the new sections to `SKILL.md`**

Add these sections after the command table and before the final references list:

```markdown
## 典型使用流程

1. 在项目目录运行 `/math-modeling init`
2. 查看 `workflow.md` 和 `memory.md`
3. 运行 `/math-modeling progress`
4. 运行 `/math-modeling next`
5. 按需要运行 `/math-modeling stage N`
6. 若出现阻断 decision，使用 `/math-modeling confirm`
7. 运行 `/math-modeling gate`
8. 仅在 final evidence gate 通过后运行 `/math-modeling export`

## 命令示例

`/math-modeling init`
: 创建最小 Markdown-first 骨架。

`/math-modeling progress`
: 汇总当前 blocker、claim ceiling 和 next safe action。

`/math-modeling stage 5`
: 在读取 Stage 5 合同和相关 protocol 后推进实现工作切片。

`/math-modeling confirm`
: 把用户明确选择写入 `decisions/decision-*.md`。

`/math-modeling export`
: 只有在 `gates/final-evidence-gate.md` 通过时才允许导出。

## 阻断时会看到什么

- `pending decision`：应出现 `decisions/decision-*.md`，等待用户确认。
- `readiness gate limitation`：应出现 `gates/*.md` 和必要的 `branches/*.md`。
- `rollback required`：应出现 `rollbacks/*.md`，而不是继续下游修补。

## 明确不要做什么

- 不要把用户沉默当确认。
- 不要在 blocked gate 下继续导出。
- 不要在 Stage 6-10 静默修补 Stage 1-5 的结构性缺陷。
```

- [ ] **Step 2: Run the `SKILL.md` contract test**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_skill_contains_typical_workflow_and_command_examples -q
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/SKILL.md C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_markdown_first_contracts.py
git commit -m "docs: add operator quickstart content to skill"
```

---

### Task 3: Expand `README.md` into a real quickstart

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Rewrite `README.md` with quickstart sections**

Replace the minimal README body with a version that includes these sections and content:

```markdown
## 适用场景

- 新赛题从零启动
- 课程作业或练习项目
- 已有建模项目迁移到 Markdown-first v4

## 新项目骨架

```text
project/
├── workflow.md
├── memory.md
├── decisions/
├── gates/
├── branches/
├── rollbacks/
├── claims/
│   └── claim-registry.md
└── reviews/
```

## 5 分钟上手

1. 在项目目录执行 `/math-modeling init`
2. 打开 `workflow.md`
3. 执行 `/math-modeling progress`
4. 执行 `/math-modeling next`
5. 需要指定阶段时执行 `/math-modeling stage 5`
6. 若出现 decision blocker，执行 `/math-modeling confirm`
7. 完成后执行 `/math-modeling gate`
8. gate 通过后再执行 `/math-modeling export`

## 最小文件示例

`workflow.md`

```markdown
# Modeling Workflow

## Current focus
Stage 2 algorithm selection

## Active blockers
- decisions/decision-stage2-algorithm.md

## Current claim ceiling
feasible_baseline
```

`decisions/decision-stage2-algorithm.md`

```markdown
# Decision - Stage 2 Algorithm

## Status
Pending

## Decision needed
Choose the main optimization route.
```

`gates/stage5-readiness-gate.md`

```markdown
# Stage 5 Readiness Gate

## Gate result
Blocked

## Supported claim level
feasible_baseline
```

## 常见阻断与处理

- 缺结构化数据：查看 `branches/`，补齐数据后再继续。
- 缺 solver：先接受 `feasible_baseline` 或补齐工具链。
- 出现 rollback：先处理 `rollbacks/*.md`，不要继续下游修补。
- export 被拦截：先检查 `decisions/`、`gates/final-evidence-gate.md` 和 `claims/claim-registry.md`。
```

Keep the existing regression command at the end.

- [ ] **Step 2: Run the `README.md` contract test**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py::test_readme_contains_quickstart_skeleton_and_minimal_examples -q
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/README.md C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_markdown_first_contracts.py
git commit -m "docs: add quickstart and skeleton guide to readme"
```

---

### Task 4: Run the full regression suite and perform a final doc sanity check

**Files:**
- Review only. Fix any issues found in:
  - `C:\Users\zty\.agents\skills\math-modeling-v4\SKILL.md`
  - `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`
  - `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Run the full regression suite**

Run:

```powershell
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py -q
```

Expected: PASS for all tests.

- [ ] **Step 2: Sanity check the new onboarding docs**

Run:

```powershell
python -c "from pathlib import Path; root=Path(r'C:\Users\zty\.agents\skills\math-modeling-v4'); 
for rel in ['SKILL.md','README.md']:
    text=(root/rel).read_text(encoding='utf-8')
    print(rel, '典型使用流程' in text or '适用场景' in text, 'workflow.md' in text, '/math-modeling export' in text)"
```

Expected:

- `SKILL.md` reports True for workflow/examples/export content
- `README.md` reports True for onboarding/skeleton content

- [ ] **Step 3: Commit**

```bash
git add C:/Users/zty/.agents/skills/math-modeling-v4/SKILL.md C:/Users/zty/.agents/skills/math-modeling-v4/README.md C:/Users/zty/.agents/skills/math-modeling-v4/regression/test_markdown_first_contracts.py
git commit -m "docs: make math-modeling-v4 directly trialable"
```

---

## Self-Review

### Spec coverage

- `SKILL.md` concise operator guide: Task 2.
- `README.md` onboarding quickstart: Task 3.
- minimal doc contract tests: Task 1.
- regression safety and sanity check: Task 4.

### Placeholder scan

No placeholders or TODOs remain.

### Type consistency

- command names are consistent with existing v4 command surface,
- file paths match current package layout,
- onboarding examples use the same Markdown artifact names as the existing protocols and regressions.
