# Pilot Acceptance Checklist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a root-level self-trial acceptance checklist for `math-modeling-v4`, protect it with a minimal documentation contract test, and keep the change limited to pilot evaluation documentation.

**Architecture:** Introduce one operational Markdown worksheet, `PILOT_ACCEPTANCE_CHECKLIST.md`, separate from onboarding and delivery docs. The checklist focuses on live pilot execution, anomaly capture, and final go / revise / stop decisions. A small regression assertion ensures the checklist remains present and keeps its required sections over time.

**Tech Stack:** Markdown documentation, Python `pytest` regression tests

---

## File Map

- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\PILOT_ACCEPTANCE_CHECKLIST.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Optional Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\DELIVERY.md`

### Task 1: Add the failing checklist contract test

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Read the existing documentation contract tests**

Locate the current documentation assertions near:

```python
def test_delivery_doc_and_readme_entry_exist():
    delivery = (ROOT / "DELIVERY.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
```

Add the pilot checklist test after the existing doc assertions so the file stays grouped by documentation concerns.

- [ ] **Step 2: Add a failing test for the pilot checklist**

Append a new test with these assertions:

```python
def test_pilot_acceptance_checklist_exists_and_has_required_sections():
    content = (ROOT / "PILOT_ACCEPTANCE_CHECKLIST.md").read_text(encoding="utf-8")

    assert "## 试用目标" in content
    assert "## 试用前检查" in content
    assert "## 试用中观察" in content
    assert "## 关键异常记录" in content
    assert "## 试用后判定" in content
    assert "## 下一步动作" in content
    assert "workflow.md" in content
    assert "可继续试用" in content
    assert "修正后再试" in content
    assert "暂不建议推广" in content
```

- [ ] **Step 3: Run the focused test and verify it fails**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py -q
```

Expected:

```text
FAIL
```

The failure should mention missing `PILOT_ACCEPTANCE_CHECKLIST.md`.

- [ ] **Step 4: Commit the failing test**

```bash
git add regression/test_markdown_first_contracts.py
git commit -m "test: add pilot acceptance checklist contract"
```

### Task 2: Write the pilot acceptance checklist

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\PILOT_ACCEPTANCE_CHECKLIST.md`

- [ ] **Step 1: Create the checklist with the required top-level sections**

Write the file with this structure:

```md
# math-modeling-v4 试用验收清单

## 试用目标

- 试点项目：
- 试用日期：
- 执行人：
- 项目类型：
- 试用范围：
- 本轮目标：只验证工作流 / 同时观察结果质量

## 试用前检查

- [ ] 已运行当前全量 regression，且结果为绿色
- [ ] 试点项目范围较小、风险可控
- [ ] 已明确本轮把 v4 视为试点流程，而不是完整 runtime engine
- [ ] 已准备好项目目录，或确认从空目录按 `README.md` 初始化
- [ ] 已写清本轮成功标准

## 试用中观察

- [ ] `workflow.md` 成为当前工作的唯一主锚点
- [ ] 缺失信息时，会生成明确的 `decisions/` 或 `branches/` 文档
- [ ] claim ceiling 会随证据变化而收敛，不会越界
- [ ] gate 阻断是显式的，不会静默跳过
- [ ] 晚期发现结构性问题时，会触发 `rollbacks/`
- [ ] `export` 前会检查 `gates/final-evidence-gate.md`
- [ ] reviewer 参与方式清楚，没有退回 stage-owner 状态机感

记录：

- 观察到的最顺畅环节：
- 观察到的最卡顿环节：

## 关键异常记录

- 触发点：
  预期行为：
  实际行为：
  严重程度：
  后续动作：

## 试用后判定

- [ ] 可继续试用
- [ ] 修正后再试
- [ ] 暂不建议推广

判定理由：

## 下一步动作

- 需要修正的问题：
- 下一轮重点观察：
- 是否需要与旧版 `math-modeling` 做对照：
```

- [ ] **Step 2: Keep the checklist operational and concise**

Before moving on, remove any wording that sounds like product marketing or abstract methodology. Keep only:

- checkboxes,
- short prompts,
- direct pilot recording fields.

Do not add long explanations under every item.

- [ ] **Step 3: Commit the checklist**

```bash
git add PILOT_ACCEPTANCE_CHECKLIST.md
git commit -m "docs: add v4 pilot acceptance checklist"
```

### Task 3: Optionally add a light discoverability pointer

**Files:**
- Optional Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\DELIVERY.md`

- [ ] **Step 1: Decide whether a pointer is needed**

If the root-level file is already easy to discover, skip this task.

If a pointer is needed, add only one short bullet under `## 推荐下一步`, like:

```md
- 开始试点前，可先按根目录下的 `PILOT_ACCEPTANCE_CHECKLIST.md` 逐项验收。
```

- [ ] **Step 2: Keep the pointer minimal**

Do not duplicate checklist contents inside `DELIVERY.md`.

- [ ] **Step 3: Commit only if `DELIVERY.md` was changed**

```bash
git add DELIVERY.md
git commit -m "docs: link pilot checklist from delivery notes"
```

### Task 4: Run tests and validate scope control

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\PILOT_ACCEPTANCE_CHECKLIST.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Optional Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\DELIVERY.md`

- [ ] **Step 1: Run the focused documentation contract test**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py -q
```

Expected:

```text
PASS
```

- [ ] **Step 2: Run the full regression suite**

Run:

```bash
python -m pytest regression/test_markdown_first_contracts.py regression/test_readiness_gate_checks.py regression/test_readiness_gate_smoke_flow.py regression/test_readiness_gate_command_flow.py regression/test_gate_and_rollback_checks.py regression/test_export_command_flow.py regression/test_rollback_command_flow.py -q
```

Expected:

```text
all tests pass
```

- [ ] **Step 3: Review final scope**

Confirm:

- only the pilot checklist doc was added,
- only the minimal contract test was changed,
- `README.md` and `SKILL.md` remain untouched,
- any `DELIVERY.md` change is at most one bullet.

- [ ] **Step 4: Commit the final slice**

```bash
git add PILOT_ACCEPTANCE_CHECKLIST.md regression/test_markdown_first_contracts.py DELIVERY.md
git commit -m "docs: add pilot acceptance checklist"
```

## Self-Review

### Spec coverage

- Root-level pilot worksheet: covered by Task 2.
- Minimal contract protection: covered by Task 1 and Task 4.
- Live pilot structure: covered by Task 2 section requirements.
- Optional discoverability pointer: covered by Task 3.
- Scope control: covered by Task 4 Step 3.

### Placeholder scan

No placeholders remain. Optional behavior is explicitly limited to a single delivery-doc pointer and is not required for completion.

### Type consistency

The plan consistently uses:

- `PILOT_ACCEPTANCE_CHECKLIST.md`
- `test_markdown_first_contracts.py`
- `DELIVERY.md`

No alternate names are introduced.
