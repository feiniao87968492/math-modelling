# Delivery Doc Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a package-level delivery handoff document for `math-modeling-v4`, link it from `README.md`, and protect the new documentation with a minimal contract test.

**Architecture:** Keep onboarding, orchestration, and handoff concerns separated. `README.md` remains the quickstart and onboarding entry, `SKILL.md` remains the dispatcher-facing document, and a new root-level `DELIVERY.md` captures current capability, trial guidance, regression coverage, and known boundaries. Add only a minimal documentation regression assertion so this handoff layer does not silently disappear later.

**Tech Stack:** Markdown documentation, Python `pytest` regression tests

---

## File Map

- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\DELIVERY.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

### Task 1: Add the failing documentation contract test

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Test: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`

- [ ] **Step 1: Read the existing test file and identify the current documentation assertions**

Review the existing structure before editing:

```python
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
README = SKILL_ROOT / "README.md"
SKILL = SKILL_ROOT / "SKILL.md"
```

Confirm where to add the new assertions without changing unrelated tests.

- [ ] **Step 2: Add a failing test for the delivery handoff document**

Append a new test like this:

```python
def test_delivery_doc_and_readme_entry_exist() -> None:
    delivery = (SKILL_ROOT / "DELIVERY.md").read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert "## 当前版本能力" in delivery
    assert "## 适合怎么试用" in delivery
    assert "## 回归覆盖概览" in delivery
    assert "## 已知边界" in delivery
    assert "## 推荐下一步" in delivery

    assert "DELIVERY.md" in readme
    assert "交付说明" in readme
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

The failure should mention missing `DELIVERY.md` or the missing delivery-doc entry in `README.md`.

- [ ] **Step 4: Commit the failing test**

```bash
git add regression/test_markdown_first_contracts.py
git commit -m "test: add delivery doc contract assertions"
```

### Task 2: Write the delivery handoff document

**Files:**
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\DELIVERY.md`

- [ ] **Step 1: Create the delivery document with the required sections**

Write the file with this structure and content:

```md
# math-modeling-v4 Delivery Notes

## 当前版本能力

- 提供 Markdown-first 的 skill 调度入口。
- 提供 rule-first 协议集合，包括 decision、gate、rollback、memory、subagent delegation。
- 提供 10 个阶段 contract 文档，覆盖审题、选型、创新、建模、求解、验证、敏感性、可视化、审图、论文素材准备。
- 提供 readiness gate、gate/rollback、export/rollback 的 scenario 与 command-flow 回归。
- 提供 quickstart 文档，支持从新项目骨架开始试用。

## 适合怎么试用

- 优先拿一个新的、小范围数学建模练习项目试用。
- 先按 `README.md` 中的 quickstart 跑通 `init -> progress -> next -> gate -> export` 路径。
- 把 command-flow helper 视为回归契约和行为样例，不要把它们误当成完整 runtime engine。
- 如果是从旧项目迁移，旧的 `modeling_state.yaml` 只作为历史上下文参考，不作为 v4 的驱动源。

## 回归覆盖概览

- contract tests: 检查 Markdown-first 文档契约、quickstart 内容、delivery 文档入口。
- smoke flow: 检查 readiness gate 的最小行为链路。
- readiness gate: 检查 claim level、required branches、阻断条件。
- gate and rollback scenarios: 检查晚期结构性缺陷、pending decision、grounded claims。
- export and rollback command-flow: 检查导出阻断与 review 触发 rollback 的命令级行为。

## 已知边界

- 当前回归 helper 仍以 deterministic simulation 为主，不是完整运行时执行器。
- 并不是每个命令都已经有独立的 command-flow helper。
- 文档、协议和回归已经接近试用状态，但真实比赛级项目仍建议先用小项目试点。

## 推荐下一步

- 选择一个新的小项目做试点试用。
- 记录试用中遇到的阻断、歧义和缺失的 command-flow。
- 根据试用结果，再决定是否扩展为更完整的 runtime execution layer。
```

- [ ] **Step 2: Keep the content concrete and non-marketing**

Before moving on, check that each section names actual implemented capabilities or actual current limits. Remove any vague wording such as:

```text
high quality
enterprise ready
fully production-ready
complete runtime support
```

- [ ] **Step 3: Commit the new delivery document**

```bash
git add DELIVERY.md
git commit -m "docs: add delivery handoff notes for v4"
```

### Task 3: Add the README entry point

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`

- [ ] **Step 1: Add a short delivery entry near the top-level onboarding sections**

Insert a short section like this in `README.md`:

```md
## 当前试用状态

- 这版 `math-modeling-v4` 已具备 Markdown-first dispatcher、协议文档、10 阶段 contract、scenario regression 和部分 command-flow regression。
- 如果你准备正式试用或交付评估，先阅读根目录下的 `DELIVERY.md`。
```

Place it near the existing overview/quickstart entry so new readers can find it before diving into command examples.

- [ ] **Step 2: Keep README as onboarding, not full handoff**

Do not duplicate the full delivery content inside `README.md`. Keep it to a short pointer and preserve the current quickstart role.

- [ ] **Step 3: Commit the README update**

```bash
git add README.md
git commit -m "docs: link delivery handoff notes from readme"
```

### Task 4: Run tests and validate the final state

**Files:**
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\regression\test_markdown_first_contracts.py`
- Create: `C:\Users\zty\.agents\skills\math-modeling-v4\DELIVERY.md`
- Modify: `C:\Users\zty\.agents\skills\math-modeling-v4\README.md`

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

- [ ] **Step 3: Review the final files for scope control**

Confirm:

- `SKILL.md` is unchanged,
- `README.md` only has a small delivery entry,
- `DELIVERY.md` contains the five required sections,
- no new runtime logic was added.

- [ ] **Step 4: Commit the finished slice**

```bash
git add README.md DELIVERY.md regression/test_markdown_first_contracts.py
git commit -m "docs: add delivery notes for v4 trial handoff"
```

## Self-Review

### Spec coverage

- Delivery handoff document: covered by Task 2.
- README discoverability entry: covered by Task 3.
- Minimal contract protection: covered by Task 1 and Task 4.
- No runtime changes: enforced in Task 3 Step 2 and Task 4 Step 3.

### Placeholder scan

No `TODO`, `TBD`, or incomplete implementation steps remain.

### Type consistency

The plan consistently uses:

- `DELIVERY.md`
- `README.md`
- `test_markdown_first_contracts.py`

No alternate names are used.
